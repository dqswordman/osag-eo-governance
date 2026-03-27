from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import tifffile
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.io import loadmat
from sklearn.model_selection import StratifiedShuffleSplit
from torch.utils.data import DataLoader
from torch.utils.data import Dataset as TorchDataset
from torch.utils.data import WeightedRandomSampler
import yaml


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / "artifacts" / "real_experiments"
CACHE_ROOT = ARTIFACT_ROOT / "cache"
DEFAULT_CONFIG = ROOT / "configs" / "osag_real_experiments.yaml"


@dataclass(frozen=True)
class MethodSpec:
    method: str
    alpha: float
    lambda_c: float
    display: str
    family: str


@dataclass(frozen=True)
class ExperimentConfig:
    epochs: int = 60
    batch_size_hsi: int = 512
    batch_size_eurosat: int = 256
    lr_hsi: float = 1e-3
    lr_eurosat: float = 1.2e-3
    weight_decay: float = 1e-4
    dropout: float = 0.1
    hidden_dim: int = 256
    eurosat_pool: int = 4
    grid_rows: int = 4
    grid_cols: int = 4
    rare_ratio: float = 0.2
    seeds: tuple[int, ...] = (13, 21, 42)


def load_yaml_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def config_from_yaml(config_dict: dict[str, Any], args: argparse.Namespace | None = None) -> ExperimentConfig:
    exp_cfg = dict(config_dict.get("experiment", {}))
    if args is not None:
        if getattr(args, "epochs", None) is not None:
            exp_cfg["epochs"] = args.epochs
        if getattr(args, "eurosat_pool", None) is not None:
            exp_cfg["eurosat_pool"] = args.eurosat_pool
        if getattr(args, "seeds", None):
            exp_cfg["seeds"] = tuple(args.seeds)
    if "seeds" in exp_cfg and not isinstance(exp_cfg["seeds"], tuple):
        exp_cfg["seeds"] = tuple(exp_cfg["seeds"])
    return ExperimentConfig(**exp_cfg)


METHODS = [
    MethodSpec("baseline_random", 1.0, 0.0, "Random", "baseline"),
    MethodSpec("baseline_class_balanced", 1.0, 0.0, "Class-Balanced", "baseline"),
    MethodSpec("baseline_uniform_contract", 1.0, 0.0, "Uniform-Contract", "baseline"),
    MethodSpec("baseline_contract_priority", 1.0, 0.0, "Contract-Priority", "baseline"),
    MethodSpec("osag_priority_mix", 0.25, 0.0, "OSAG-Mix (a=0.25)", "alpha"),
    MethodSpec("osag_priority_mix", 0.50, 0.0, "OSAG-Mix (a=0.50)", "alpha"),
    MethodSpec("osag_priority_mix", 0.75, 0.0, "OSAG-Mix (a=0.75)", "alpha"),
    MethodSpec("osag_priority", 1.0, 0.0, "OSAG", "alpha"),
    MethodSpec("osag_priority_fairloss", 1.0, 0.5, "OSAG-FairLoss (l=0.5)", "lambda"),
    MethodSpec("osag_priority_fairloss", 1.0, 1.0, "OSAG-FairLoss (l=1.0)", "lambda"),
]


class SimpleMLP(nn.Module):
    def __init__(self, in_dim: int, num_classes: int, hidden_dim: int = 256, dropout: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ArrayContractDataset(TorchDataset):
    def __init__(self, X: np.ndarray, y: np.ndarray, meta: pd.DataFrame, indices: np.ndarray):
        self.X = X
        self.y = y
        self.meta = meta.reset_index(drop=True)
        self.indices = np.asarray(indices, dtype=np.int64)

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        global_idx = int(self.indices[idx])
        row = self.meta.iloc[global_idx]
        return (
            torch.from_numpy(self.X[global_idx]).float(),
            torch.tensor(int(self.y[global_idx]), dtype=torch.long),
            torch.tensor(int(row["contract_id"]), dtype=torch.long),
            torch.tensor(float(row["priority"]), dtype=torch.float32),
        )


class LocalEuroSATDataset(TorchDataset):
    def __init__(
        self,
        meta: pd.DataFrame,
        indices: np.ndarray,
        mean: np.ndarray,
        std: np.ndarray,
        pool_size: int,
    ):
        self.meta = meta.reset_index(drop=True)
        self.indices = np.asarray(indices, dtype=np.int64)
        self.mean = mean.astype(np.float32)
        self.std = std.astype(np.float32)
        self.pool_size = int(pool_size)

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        global_idx = int(self.indices[idx])
        row = self.meta.iloc[global_idx]
        arr = tifffile.imread(str(row["image_path"])).astype(np.float32)
        feat = pool_and_flatten(arr, self.pool_size)
        feat = (feat - self.mean) / self.std
        return (
            torch.from_numpy(feat).float(),
            torch.tensor(int(row["class_id"]), dtype=torch.long),
            torch.tensor(int(row["contract_id"]), dtype=torch.long),
            torch.tensor(float(row["priority"]), dtype=torch.float32),
        )


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_first_mat_array(path: Path) -> np.ndarray:
    data = loadmat(path)
    arrays: list[np.ndarray] = []
    for key, value in data.items():
        if key.startswith("__"):
            continue
        if isinstance(value, np.ndarray) and value.ndim in (2, 3):
            arrays.append(value)
    if not arrays:
        raise RuntimeError(f"No usable ndarray found in {path}")
    return arrays[0]


def compute_rare_classes(labels: np.ndarray, rare_ratio: float) -> set[int]:
    values, counts = np.unique(labels, return_counts=True)
    order = np.argsort(counts)
    k = max(1, int(math.ceil(len(values) * rare_ratio)))
    return {int(v) for v in values[order[:k]]}


def build_contract_table_from_meta(meta: pd.DataFrame, key_cols: list[str], priority_rule) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta = meta.copy()
    meta["contract_key"] = meta[key_cols].astype(str).agg("|".join, axis=1)
    unique_keys = meta["contract_key"].unique().tolist()
    key_to_id = {key: idx for idx, key in enumerate(unique_keys)}
    meta["contract_id"] = meta["contract_key"].map(key_to_id).astype(int)
    grouped = meta.groupby("contract_id", sort=True)
    num_samples = grouped.size().rename("num_samples")
    priorities = grouped.apply(priority_rule, include_groups=False).rename("priority")
    df_contracts = pd.concat([num_samples, priorities], axis=1).reset_index()
    df_contracts["raw_weight"] = df_contracts["priority"] * df_contracts["num_samples"]
    df_contracts["target_weight"] = df_contracts["raw_weight"] / df_contracts["raw_weight"].sum()
    priority_map = dict(zip(df_contracts["contract_id"], df_contracts["priority"]))
    meta["priority"] = meta["contract_id"].map(priority_map).astype(float)
    return meta, df_contracts[["contract_id", "num_samples", "priority", "target_weight"]]


def make_stratified_split(y: np.ndarray) -> np.ndarray:
    idx_all = np.arange(len(y))
    splitter1 = StratifiedShuffleSplit(n_splits=1, test_size=0.4, random_state=42)
    train_idx, temp_idx = next(splitter1.split(idx_all, y))
    splitter2 = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=42)
    val_rel_idx, test_rel_idx = next(splitter2.split(temp_idx, y[temp_idx]))
    val_idx = temp_idx[val_rel_idx]
    test_idx = temp_idx[test_rel_idx]
    split = np.full(len(y), "train", dtype=object)
    split[val_idx] = "val"
    split[test_idx] = "test"
    return split


def pool_and_flatten(arr: np.ndarray, pool_size: int) -> np.ndarray:
    if pool_size <= 1:
        return arr.reshape(-1).astype(np.float32)
    height, width, channels = arr.shape
    if height % pool_size != 0 or width % pool_size != 0:
        raise ValueError(f"Invalid pool_size={pool_size} for shape {arr.shape}")
    pooled = arr.reshape(height // pool_size, pool_size, width // pool_size, pool_size, channels).mean(axis=(1, 3))
    return pooled.reshape(-1).astype(np.float32)


def scan_eurosat_records(config_dict: dict[str, Any]) -> pd.DataFrame:
    dataset_cfg = config_dict["datasets"]["eurosat_ms_zip"]
    extract_root = resolve_repo_path(dataset_cfg["extracted_path"])
    base_dir = extract_root / "EuroSAT_MS" if (extract_root / "EuroSAT_MS").exists() else extract_root
    if not base_dir.exists():
        raise RuntimeError(f"EuroSAT extracted directory not found: {base_dir}")

    folder_to_label = {
        "AnnualCrop": "Annual Crop",
        "Forest": "Forest",
        "HerbaceousVegetation": "Herbaceous Vegetation",
        "Highway": "Highway",
        "Industrial": "Industrial Buildings",
        "Pasture": "Pasture",
        "PermanentCrop": "Permanent Crop",
        "Residential": "Residential Buildings",
        "River": "River",
        "SeaLake": "SeaLake",
    }
    class_folders = [p for p in sorted(base_dir.iterdir()) if p.is_dir()]
    label_to_id = {folder_to_label[p.name]: idx for idx, p in enumerate(class_folders)}

    records = []
    for class_dir in class_folders:
        class_name = folder_to_label[class_dir.name]
        class_id = label_to_id[class_name]
        for image_path in sorted(class_dir.glob("*.tif")):
            records.append(
                {
                    "dataset": "eurosat_msi",
                    "class_id": class_id,
                    "class_name": class_name,
                    "folder_name": class_dir.name,
                    "image_path": str(image_path.resolve()),
                    "filename": image_path.name,
                }
            )
    if not records:
        raise RuntimeError(f"No EuroSAT TIFF files found under {base_dir}")
    return pd.DataFrame(records)


def load_or_build_eurosat_feature_cache(meta: pd.DataFrame, pool_size: int) -> np.ndarray:
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    features_path = CACHE_ROOT / f"eurosat_msi_pool{pool_size}_features.npy"
    manifest_path = CACHE_ROOT / f"eurosat_msi_pool{pool_size}_manifest.json"

    if features_path.exists():
        X_all = np.load(features_path)
        if X_all.shape[0] != len(meta):
            raise RuntimeError(
                f"Cached EuroSAT feature count mismatch: cache has {X_all.shape[0]}, metadata has {len(meta)}"
            )
        return X_all.astype(np.float32, copy=False)

    first_feat = pool_and_flatten(tifffile.imread(str(meta.iloc[0]["image_path"])).astype(np.float32), pool_size)
    feature_dim = int(first_feat.shape[0])
    mmap = np.lib.format.open_memmap(features_path, mode="w+", dtype=np.float32, shape=(len(meta), feature_dim))
    mmap[0] = first_feat
    for idx in range(1, len(meta)):
        arr = tifffile.imread(str(meta.iloc[idx]["image_path"])).astype(np.float32)
        mmap[idx] = pool_and_flatten(arr, pool_size)
        if idx % 2500 == 0:
            print(f"[eurosat_msi][cache] built {idx}/{len(meta)} feature vectors")
    del mmap

    manifest_path.write_text(
        json.dumps(
            {
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "pool_size": int(pool_size),
                "num_samples": int(len(meta)),
                "feature_dim": int(feature_dim),
                "features_path": str(features_path),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return np.load(features_path).astype(np.float32, copy=False)


def load_hsi_bundle(config: ExperimentConfig, config_dict: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame, pd.DataFrame]:
    dataset_cfg = config_dict["datasets"]
    X_i = load_first_mat_array(resolve_repo_path(dataset_cfg["indian_pines_corrected"]["local_path"]))
    y_i = load_first_mat_array(resolve_repo_path(dataset_cfg["indian_pines_gt"]["local_path"]))
    X_s = load_first_mat_array(resolve_repo_path(dataset_cfg["salinas_corrected"]["local_path"]))
    y_s = load_first_mat_array(resolve_repo_path(dataset_cfg["salinas_gt"]["local_path"]))

    common_bands = min(int(X_i.shape[2]), int(X_s.shape[2]))
    X_i = X_i[:, :, :common_bands]
    X_s = X_s[:, :, :common_bands]

    def flatten_labeled_pixels(X: np.ndarray, y: np.ndarray, dataset_name: str) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
        height, width, bands = X.shape
        X_flat = X.reshape(-1, bands)
        y_flat = y.reshape(-1)
        mask = y_flat > 0
        X_flat = X_flat[mask]
        y_flat = y_flat[mask] - 1
        rows = np.repeat(np.arange(height), width)[mask]
        cols = np.tile(np.arange(width), height)[mask]
        meta = pd.DataFrame(
            {
                "dataset": dataset_name,
                "row": rows,
                "col": cols,
                "class_id": y_flat.astype(np.int64),
            }
        )
        return X_flat.astype(np.float32), y_flat.astype(np.int64), meta

    X_i_flat, y_i_flat, meta_i = flatten_labeled_pixels(X_i, y_i, "indian")
    X_s_flat, y_s_flat, meta_s = flatten_labeled_pixels(X_s, y_s, "salinas")

    def assign_grid(meta: pd.DataFrame, height: int, width: int) -> pd.DataFrame:
        meta = meta.copy()
        meta["grid_row"] = (meta["row"].to_numpy() * config.grid_rows) // height
        meta["grid_col"] = (meta["col"].to_numpy() * config.grid_cols) // width
        return meta

    meta_i = assign_grid(meta_i, X_i.shape[0], X_i.shape[1])
    meta_s = assign_grid(meta_s, X_s.shape[0], X_s.shape[1])

    X_all = np.concatenate([X_i_flat, X_s_flat], axis=0).astype(np.float32)
    y_all = np.concatenate([y_i_flat, y_s_flat], axis=0).astype(np.int64)
    meta_all = pd.concat([meta_i, meta_s], ignore_index=True)
    meta_all["split"] = make_stratified_split(y_all)

    rare_flags = np.zeros(len(meta_all), dtype=np.int64)
    for dataset_name in ["indian", "salinas"]:
        mask_dataset = meta_all["dataset"] == dataset_name
        mask_train = mask_dataset & (meta_all["split"] == "train")
        rare_classes = compute_rare_classes(y_all[mask_train.to_numpy()], config.rare_ratio)
        rare_flags[mask_dataset.to_numpy()] = meta_all.loc[mask_dataset, "class_id"].isin(rare_classes).astype(np.int64)
    meta_all["is_rare_class"] = rare_flags

    def priority_rule(group: pd.DataFrame) -> float:
        return 3.0 if group["is_rare_class"].mean() > 0 else 1.0

    meta_all, df_contracts = build_contract_table_from_meta(
        meta_all,
        key_cols=["dataset", "grid_row", "grid_col", "is_rare_class"],
        priority_rule=priority_rule,
    )

    train_mask = meta_all["split"] == "train"
    mean = X_all[train_mask.to_numpy()].mean(axis=0, keepdims=True)
    std = X_all[train_mask.to_numpy()].std(axis=0, keepdims=True) + 1e-6
    X_all = ((X_all - mean) / std).astype(np.float32)
    return X_all, y_all, meta_all, df_contracts


def compute_eurosat_normalization(X: np.ndarray, split: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    train_mask = split == "train"
    mean = X[train_mask].mean(axis=0, keepdims=True)
    std = X[train_mask].std(axis=0, keepdims=True) + 1e-6
    return mean.astype(np.float32), std.astype(np.float32)


def prepare_eurosat_base_bundle(config: ExperimentConfig, config_dict: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame, int]:
    meta_all = scan_eurosat_records(config_dict)
    split = make_stratified_split(meta_all["class_id"].to_numpy(np.int64))
    meta_all["split"] = split

    train_rare = compute_rare_classes(meta_all.loc[meta_all["split"] == "train", "class_id"].to_numpy(np.int64), config.rare_ratio)
    meta_all["is_rare_class"] = meta_all["class_id"].isin(train_rare).astype(np.int64)

    def map_scene_group(name: str) -> str:
        name_lower = name.lower()
        if "annual" in name_lower or "pasture" in name_lower or "permanent" in name_lower:
            return "agri"
        if "residential" in name_lower or "industrial" in name_lower or "highway" in name_lower:
            return "urban"
        if "river" in name_lower or "sea" in name_lower or "lake" in name_lower:
            return "water"
        if "forest" in name_lower or "herbaceous" in name_lower:
            return "natural"
        return "other"

    meta_all["scene_group"] = meta_all["class_name"].apply(map_scene_group)
    X_all = load_or_build_eurosat_feature_cache(meta_all, config.eurosat_pool)
    mean, std = compute_eurosat_normalization(X_all, meta_all["split"].to_numpy())
    X_all = ((X_all - mean) / std).astype(np.float32)
    y_all = meta_all["class_id"].to_numpy(np.int64)
    feature_dim = int(X_all.shape[1])
    return X_all, y_all, meta_all, feature_dim


def load_eurosat_bundle(config: ExperimentConfig, config_dict: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, pd.DataFrame, pd.DataFrame, int]:
    X_all, y_all, meta_base, feature_dim = prepare_eurosat_base_bundle(config, config_dict)

    def priority_rule(group: pd.DataFrame) -> float:
        return 2.0 if group["is_rare_class"].mean() > 0 else 1.0

    meta_all, df_contracts = build_contract_table_from_meta(
        meta_base,
        key_cols=["dataset", "scene_group", "is_rare_class"],
        priority_rule=priority_rule,
    )
    return X_all, y_all, meta_all, df_contracts, feature_dim


def build_eurosat_contract_variant(meta: pd.DataFrame, variant: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    if variant == "fine":
        key_cols = ["dataset", "scene_group", "is_rare_class"]

        def priority_rule(group: pd.DataFrame) -> float:
            return 2.0 if group["is_rare_class"].mean() > 0 else 1.0

    elif variant == "coarse":
        key_cols = ["dataset", "scene_group"]

        def priority_rule(group: pd.DataFrame) -> float:
            return 2.0 if group["scene_group"].iloc[0] in {"urban", "water"} else 1.0

    else:
        raise ValueError(f"Unknown variant: {variant}")
    return build_contract_table_from_meta(meta, key_cols=key_cols, priority_rule=priority_rule)


def build_sample_weights(method: str, meta_train: pd.DataFrame, df_contracts: pd.DataFrame, alpha: float) -> np.ndarray:
    num_samples = len(meta_train)
    if method == "baseline_random":
        weights = np.ones(num_samples, dtype=np.float32)
        return weights / weights.sum()
    if method == "baseline_class_balanced":
        counts = meta_train["class_id"].value_counts().to_dict()
        weights = meta_train["class_id"].map(lambda cls: 1.0 / counts[int(cls)]).to_numpy(np.float32)
        return weights / weights.sum()

    contract_counts = meta_train["contract_id"].value_counts().to_dict()
    contract_tbl = df_contracts.set_index("contract_id")
    uniform_contract = np.array([1.0 / contract_counts[int(cid)] for cid in meta_train["contract_id"]], dtype=np.float32)
    uniform_contract /= uniform_contract.sum()
    contract_priority = np.array(
        [float(contract_tbl.loc[int(cid), "priority"]) / contract_counts[int(cid)] for cid in meta_train["contract_id"]],
        dtype=np.float32,
    )
    contract_priority /= contract_priority.sum()
    osag = np.array(
        [float(contract_tbl.loc[int(cid), "target_weight"]) / contract_counts[int(cid)] for cid in meta_train["contract_id"]],
        dtype=np.float32,
    )
    osag /= osag.sum()

    if method == "baseline_uniform_contract":
        return uniform_contract
    if method == "baseline_contract_priority":
        return contract_priority
    if method in {"osag_priority", "osag_priority_fairloss"}:
        return osag
    if method == "osag_priority_mix":
        random_weights = np.ones(num_samples, dtype=np.float32)
        random_weights /= random_weights.sum()
        mixed = alpha * osag + (1.0 - alpha) * random_weights
        return mixed / mixed.sum()
    raise ValueError(f"Unknown method: {method}")


def create_dataloaders(
    dataset_name: str,
    X: np.ndarray | None,
    y: np.ndarray | None,
    meta: pd.DataFrame,
    df_contracts: pd.DataFrame,
    method: MethodSpec,
    batch_size: int,
    mean: np.ndarray | None = None,
    std: np.ndarray | None = None,
    pool_size: int | None = None,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    idx_all = np.arange(len(meta))
    train_idx = idx_all[meta["split"].to_numpy() == "train"]
    val_idx = idx_all[meta["split"].to_numpy() == "val"]
    test_idx = idx_all[meta["split"].to_numpy() == "test"]
    meta_train = meta.iloc[train_idx].reset_index(drop=True)
    weights = build_sample_weights(method.method, meta_train, df_contracts, method.alpha)
    sampler = WeightedRandomSampler(weights=torch.from_numpy(weights), num_samples=len(weights), replacement=True)

    if X is not None and y is not None:
        train_ds = ArrayContractDataset(X, y, meta, train_idx)
        val_ds = ArrayContractDataset(X, y, meta, val_idx)
        test_ds = ArrayContractDataset(X, y, meta, test_idx)
    elif dataset_name == "eurosat_msi":
        assert mean is not None and std is not None and pool_size is not None
        train_ds = LocalEuroSATDataset(meta, train_idx, mean, std, pool_size)
        val_ds = LocalEuroSATDataset(meta, val_idx, mean, std, pool_size)
        test_ds = LocalEuroSATDataset(meta, test_idx, mean, std, pool_size)
    else:
        raise ValueError(f"Unknown dataset_name: {dataset_name}")

    return (
        DataLoader(train_ds, batch_size=batch_size, sampler=sampler, num_workers=0, pin_memory=torch.cuda.is_available()),
        DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=torch.cuda.is_available()),
        DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=torch.cuda.is_available()),
    )


def compute_coverage_errors(contract_counts: np.ndarray, df_contracts: pd.DataFrame) -> dict[str, float]:
    num_contracts = len(df_contracts)
    total = contract_counts.sum() + 1e-12
    q_hat = contract_counts / total
    ordered = df_contracts.sort_values("contract_id")
    target = ordered["target_weight"].to_numpy(np.float64)
    prio_err = np.abs(q_hat - target)
    uniform_target = np.ones_like(target) / num_contracts
    uniform_err = np.abs(q_hat - uniform_target)
    return {
        "priority_coverage_error_mean": float(prio_err.sum()),
        "priority_coverage_error_max": float(prio_err.max()),
        "priority_coverage_error_std": float(prio_err.std()),
        "uniform_coverage_error_mean": float(uniform_err.sum()),
        "uniform_coverage_error_max": float(uniform_err.max()),
        "uniform_coverage_error_std": float(uniform_err.std()),
    }


def evaluate_model(model: nn.Module, loader: DataLoader) -> tuple[float, pd.DataFrame]:
    model.eval()
    correct = 0
    total = 0
    per_contract_correct: dict[int, int] = defaultdict(int)
    per_contract_total: dict[int, int] = defaultdict(int)
    with torch.no_grad():
        for X_b, y_b, cid_b, _prio_b in loader:
            X_b = X_b.to(DEVICE)
            y_b = y_b.to(DEVICE)
            logits = model(X_b)
            preds = logits.argmax(dim=1)
            correct += int((preds == y_b).sum().item())
            total += int(len(y_b))
            for cid, y_true, y_pred in zip(cid_b.cpu().tolist(), y_b.cpu().tolist(), preds.cpu().tolist()):
                per_contract_total[int(cid)] += 1
                if int(y_true) == int(y_pred):
                    per_contract_correct[int(cid)] += 1
    rows = []
    for cid, tot in per_contract_total.items():
        rows.append({"contract_id": cid, "correct": per_contract_correct[cid], "total": tot, "acc": per_contract_correct[cid] / max(tot, 1)})
    return correct / max(total, 1), pd.DataFrame(rows)


def run_one(
    dataset_name: str,
    num_classes: int,
    feature_dim: int,
    meta: pd.DataFrame,
    df_contracts: pd.DataFrame,
    method: MethodSpec,
    seed: int,
    config: ExperimentConfig,
    X: np.ndarray | None = None,
    y: np.ndarray | None = None,
    mean: np.ndarray | None = None,
    std: np.ndarray | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    set_seed(seed)
    batch_size = config.batch_size_hsi if dataset_name == "indian_salinas" else config.batch_size_eurosat
    lr = config.lr_hsi if dataset_name == "indian_salinas" else config.lr_eurosat
    train_loader, val_loader, test_loader = create_dataloaders(
        dataset_name=dataset_name,
        X=X,
        y=y,
        meta=meta,
        df_contracts=df_contracts,
        method=method,
        batch_size=batch_size,
        mean=mean,
        std=std,
        pool_size=config.eurosat_pool,
    )

    model = SimpleMLP(feature_dim, num_classes, hidden_dim=config.hidden_dim, dropout=config.dropout).to(DEVICE)
    optim = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=config.weight_decay)
    ordered_contracts = df_contracts.sort_values("contract_id").reset_index(drop=True)
    contract_counts = np.zeros(len(ordered_contracts), dtype=np.int64)

    epoch_rows: list[dict[str, Any]] = []
    coverage_rows: list[dict[str, Any]] = []
    for epoch in range(1, config.epochs + 1):
        model.train()
        epoch_loss = 0.0
        epoch_correct = 0
        epoch_total = 0
        t0 = time.time()
        for X_b, y_b, cid_b, prio_b in train_loader:
            X_b = X_b.to(DEVICE, non_blocking=True)
            y_b = y_b.to(DEVICE, non_blocking=True)
            cid_b = cid_b.to(DEVICE, non_blocking=True)
            prio_b = prio_b.to(DEVICE, non_blocking=True)
            optim.zero_grad()
            logits = model(X_b)
            losses = F.cross_entropy(logits, y_b, reduction="none")
            loss = losses.mean()
            if method.method == "osag_priority_fairloss" and method.lambda_c > 0.0:
                high_mask = prio_b >= 2.0
                low_mask = prio_b < 2.0
                if bool(high_mask.any()) and bool(low_mask.any()):
                    fair_penalty = torch.clamp(losses[high_mask].mean() - losses[low_mask].mean(), min=0.0)
                    loss = loss + method.lambda_c * fair_penalty
            loss.backward()
            optim.step()

            preds = logits.argmax(dim=1)
            epoch_loss += float(loss.item()) * len(y_b)
            epoch_correct += int((preds == y_b).sum().item())
            epoch_total += int(len(y_b))
            for cid in cid_b.cpu().tolist():
                contract_counts[int(cid)] += 1

        train_acc = epoch_correct / max(epoch_total, 1)
        val_acc, _ = evaluate_model(model, val_loader)
        test_acc, df_contract_acc = evaluate_model(model, test_loader)
        coverage_metrics = compute_coverage_errors(contract_counts, ordered_contracts)
        if len(df_contract_acc) > 0:
            df_contract_acc = df_contract_acc.merge(ordered_contracts, on="contract_id", how="left")
            high_mask = df_contract_acc["priority"] >= 2.0
            low_mask = ~high_mask
            test_high = float(df_contract_acc.loc[high_mask, "acc"].mean())
            test_low = float(df_contract_acc.loc[low_mask, "acc"].mean())
        else:
            test_high = float("nan")
            test_low = float("nan")

        epoch_row = {
            "dataset": dataset_name,
            "display": method.display,
            "family": method.family,
            "method": method.method,
            "seed": seed,
            "alpha": method.alpha,
            "lambda_c": method.lambda_c,
            "epoch": epoch,
            "train_loss": epoch_loss / max(epoch_total, 1),
            "train_acc": train_acc,
            "val_acc": val_acc,
            "test_acc_all": test_acc,
            "test_acc_high_contract": test_high,
            "test_acc_low_contract": test_low,
            "epoch_time_sec": time.time() - t0,
            **coverage_metrics,
        }
        epoch_rows.append(epoch_row)

        observed = contract_counts / max(contract_counts.sum(), 1.0)
        for idx, row in ordered_contracts.iterrows():
            coverage_rows.append(
                {
                    "dataset": dataset_name,
                    "display": method.display,
                    "method": method.method,
                    "seed": seed,
                    "alpha": method.alpha,
                    "lambda_c": method.lambda_c,
                    "epoch": epoch,
                    "contract_id": int(row["contract_id"]),
                    "priority": float(row["priority"]),
                    "target_weight": float(row["target_weight"]),
                    "observed_coverage": float(observed[idx]),
                }
            )

        print(
            f"[{dataset_name}][{method.display}][seed={seed}] "
            f"epoch {epoch:02d}/{config.epochs} "
            f"train_loss={epoch_loss / max(epoch_total, 1):.4f} "
            f"train_acc={train_acc:.4f} val_acc={val_acc:.4f} "
            f"test_acc={test_acc:.4f} pce={coverage_metrics['priority_coverage_error_mean']:.4f}"
        )

    final_contract_rows = []
    final_acc, df_contract_acc = evaluate_model(model, test_loader)
    if len(df_contract_acc) > 0:
        df_contract_acc = df_contract_acc.merge(ordered_contracts, on="contract_id", how="left")
        for _, row in df_contract_acc.iterrows():
            final_contract_rows.append(
                {
                    "dataset": dataset_name,
                    "display": method.display,
                    "method": method.method,
                    "seed": seed,
                    "alpha": method.alpha,
                    "lambda_c": method.lambda_c,
                    "contract_id": int(row["contract_id"]),
                    "priority": float(row["priority"]),
                    "contract_acc": float(row["acc"]),
                    "contract_total": int(row["total"]),
                }
            )
        high_acc = float(df_contract_acc.loc[df_contract_acc["priority"] >= 2.0, "acc"].mean())
        low_acc = float(df_contract_acc.loc[df_contract_acc["priority"] < 2.0, "acc"].mean())
    else:
        high_acc = float("nan")
        low_acc = float("nan")

    final_result = {
        "dataset": dataset_name,
        "display": method.display,
        "family": method.family,
        "method": method.method,
        "seed": seed,
        "alpha": method.alpha,
        "lambda_c": method.lambda_c,
        "epochs": config.epochs,
        "test_acc_all": final_acc,
        "test_acc_high_contract": high_acc,
        "test_acc_low_contract": low_acc,
        **compute_coverage_errors(contract_counts, ordered_contracts),
    }
    return final_result, epoch_rows, coverage_rows, final_contract_rows


def aggregate_results(final_df: pd.DataFrame) -> pd.DataFrame:
    return (
        final_df.groupby(["dataset", "display", "family", "method", "alpha", "lambda_c"], as_index=False)
        .agg(
            test_acc_all_mean=("test_acc_all", "mean"),
            test_acc_all_std=("test_acc_all", "std"),
            test_acc_high_contract_mean=("test_acc_high_contract", "mean"),
            test_acc_high_contract_std=("test_acc_high_contract", "std"),
            test_acc_low_contract_mean=("test_acc_low_contract", "mean"),
            test_acc_low_contract_std=("test_acc_low_contract", "std"),
            priority_coverage_error_mean_mean=("priority_coverage_error_mean", "mean"),
            priority_coverage_error_mean_std=("priority_coverage_error_mean", "std"),
            priority_coverage_error_max_mean=("priority_coverage_error_max", "mean"),
            uniform_coverage_error_mean_mean=("uniform_coverage_error_mean", "mean"),
            uniform_coverage_error_mean_std=("uniform_coverage_error_mean", "std"),
        )
        .sort_values(["dataset", "priority_coverage_error_mean_mean", "test_acc_high_contract_mean"], ascending=[True, True, False])
        .reset_index(drop=True)
    )


def save_manifest(out_dir: Path, config: ExperimentConfig, extra: dict[str, Any]) -> None:
    manifest = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "device": str(DEVICE),
        "config": asdict(config),
        **extra,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def run_main_experiments(config: ExperimentConfig, config_dict: dict[str, Any], out_dir: Path) -> tuple[Path, Path, Path]:
    hsi_X, hsi_y, hsi_meta, hsi_contracts = load_hsi_bundle(config, config_dict)
    euro_X, euro_y, euro_meta, euro_contracts, euro_dim = load_eurosat_bundle(config, config_dict)
    hsi_dim = int(hsi_X.shape[1])
    hsi_classes = int(hsi_y.max() + 1)
    euro_classes = int(euro_y.max() + 1)

    hsi_final_rows: list[dict[str, Any]] = []
    hsi_epoch_rows: list[dict[str, Any]] = []
    hsi_cov_rows: list[dict[str, Any]] = []
    hsi_contract_acc_rows: list[dict[str, Any]] = []
    euro_final_rows: list[dict[str, Any]] = []
    euro_epoch_rows: list[dict[str, Any]] = []
    euro_cov_rows: list[dict[str, Any]] = []
    euro_contract_acc_rows: list[dict[str, Any]] = []

    for method in METHODS:
        for seed in config.seeds:
            final_row, epoch_rows, cov_rows, contract_rows = run_one(
                dataset_name="indian_salinas",
                num_classes=hsi_classes,
                feature_dim=hsi_dim,
                meta=hsi_meta,
                df_contracts=hsi_contracts,
                method=method,
                seed=seed,
                config=config,
                X=hsi_X,
                y=hsi_y,
            )
            hsi_final_rows.append(final_row)
            hsi_epoch_rows.extend(epoch_rows)
            hsi_cov_rows.extend(cov_rows)
            hsi_contract_acc_rows.extend(contract_rows)

    for method in METHODS:
        for seed in config.seeds:
            final_row, epoch_rows, cov_rows, contract_rows = run_one(
                dataset_name="eurosat_msi",
                num_classes=euro_classes,
                feature_dim=euro_dim,
                meta=euro_meta,
                df_contracts=euro_contracts,
                method=method,
                seed=seed,
                config=config,
                X=euro_X,
                y=euro_y,
            )
            euro_final_rows.append(final_row)
            euro_epoch_rows.extend(epoch_rows)
            euro_cov_rows.extend(cov_rows)
            euro_contract_acc_rows.extend(contract_rows)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    hsi_results_path = out_dir / f"osag_contracts_indian_salinas_experiments_{timestamp}.csv"
    euro_results_path = out_dir / f"osag_contracts_eurosat_msi_experiments_{timestamp}.csv"
    hsi_epoch_path = out_dir / f"osag_contracts_indian_salinas_epoch_{timestamp}.csv"
    euro_epoch_path = out_dir / f"osag_contracts_eurosat_msi_epoch_{timestamp}.csv"
    hsi_cov_path = out_dir / f"osag_contracts_indian_salinas_coverage_{timestamp}.csv"
    euro_cov_path = out_dir / f"osag_contracts_eurosat_msi_coverage_{timestamp}.csv"
    hsi_contract_path = out_dir / f"osag_contracts_indian_salinas_contract_acc_{timestamp}.csv"
    euro_contract_path = out_dir / f"osag_contracts_eurosat_msi_contract_acc_{timestamp}.csv"
    hsi_contract_table_path = out_dir / f"indian_salinas_contracts_{timestamp}.csv"
    euro_contract_table_path = out_dir / f"eurosat_msi_contracts_{timestamp}.csv"

    pd.DataFrame(hsi_final_rows).to_csv(hsi_results_path, index=False)
    pd.DataFrame(euro_final_rows).to_csv(euro_results_path, index=False)
    pd.DataFrame(hsi_epoch_rows).to_csv(hsi_epoch_path, index=False)
    pd.DataFrame(euro_epoch_rows).to_csv(euro_epoch_path, index=False)
    pd.DataFrame(hsi_cov_rows).to_csv(hsi_cov_path, index=False)
    pd.DataFrame(euro_cov_rows).to_csv(euro_cov_path, index=False)
    pd.DataFrame(hsi_contract_acc_rows).to_csv(hsi_contract_path, index=False)
    pd.DataFrame(euro_contract_acc_rows).to_csv(euro_contract_path, index=False)
    hsi_contracts.to_csv(hsi_contract_table_path, index=False)
    euro_contracts.to_csv(euro_contract_table_path, index=False)

    summary_path = out_dir / f"osag_main_summary_{timestamp}.csv"
    summary = aggregate_results(pd.concat([pd.DataFrame(hsi_final_rows), pd.DataFrame(euro_final_rows)], ignore_index=True))
    summary.to_csv(summary_path, index=False)
    save_manifest(
        out_dir,
        config,
        {
            "data_sources": config_dict["datasets"],
            "main_outputs": {
                "indian_salinas_results": str(hsi_results_path),
                "eurosat_results": str(euro_results_path),
                "indian_salinas_epochs": str(hsi_epoch_path),
                "eurosat_epochs": str(euro_epoch_path),
                "summary": str(summary_path),
                "eurosat_pool": config.eurosat_pool,
            }
        },
    )
    return hsi_results_path, euro_results_path, summary_path


def run_eurosat_contract_ablation(config: ExperimentConfig, config_dict: dict[str, Any], out_dir: Path) -> Path:
    euro_X, euro_y, euro_meta, _contracts, euro_dim = load_eurosat_bundle(config, config_dict)
    euro_classes = int(euro_y.max() + 1)
    ablation_methods = [
        MethodSpec("baseline_random", 1.0, 0.0, "Random", "baseline"),
        MethodSpec("baseline_class_balanced", 1.0, 0.0, "Class-Balanced", "baseline"),
        MethodSpec("baseline_uniform_contract", 1.0, 0.0, "Uniform-Contract", "baseline"),
        MethodSpec("baseline_contract_priority", 1.0, 0.0, "Contract-Priority", "baseline"),
        MethodSpec("osag_priority", 1.0, 0.0, "OSAG", "alpha"),
        MethodSpec("osag_priority_fairloss", 1.0, 0.5, "OSAG-FairLoss (l=0.5)", "lambda"),
    ]
    rows: list[dict[str, Any]] = []
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    contract_csvs: dict[str, Path] = {}

    for variant in ["coarse", "fine"]:
        variant_meta, df_contracts = build_eurosat_contract_variant(euro_meta, variant)
        contract_csv = out_dir / f"eurosat_contracts_{variant}_{timestamp}.csv"
        df_contracts.to_csv(contract_csv, index=False)
        contract_csvs[variant] = contract_csv
        for method in ablation_methods:
            for seed in config.seeds:
                _final_result, epoch_rows, _cov_rows, _contract_rows = run_one(
                    dataset_name="eurosat_msi",
                    num_classes=euro_classes,
                    feature_dim=euro_dim,
                    meta=variant_meta,
                    df_contracts=df_contracts,
                    method=method,
                    seed=seed,
                    config=config,
                    X=euro_X,
                    y=euro_y,
                )
                for row in epoch_rows:
                    rows.append(
                        {
                            "run_tag": f"eurosat_msi_{variant}",
                            "variant": variant,
                            "contracts_csv": str(contract_csv),
                            **row,
                            "test_acc_last": row["test_acc_all"],
                        }
                    )

    out_path = out_dir / f"osag_contracts_eurosat_coarse_fine_ablation_{timestamp}.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    manifest_path = out_dir / f"eurosat_ablation_manifest_{timestamp}.json"
    manifest_path.write_text(
        json.dumps(
            {
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "device": str(DEVICE),
                "config": asdict(config),
                "output_csv": str(out_path),
                "contract_tables": {k: str(v) for k, v in contract_csvs.items()},
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reproduce OSAG real-data experiments from official data sources.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seeds", type=int, nargs="+", default=None)
    parser.add_argument("--eurosat-pool", type=int, default=None)
    parser.add_argument("--skip-main", action="store_true")
    parser.add_argument("--skip-ablation", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_dict = load_yaml_config(args.config)
    config = config_from_yaml(config_dict, args)
    output_dir = args.output_dir if args.output_dir is not None else resolve_repo_path(config_dict["paths"]["artifact_root"])
    print(f"Using device: {DEVICE}")
    print(f"Config path: {args.config}")
    print(f"Output dir: {output_dir}")
    print(f"Config: {config}")
    if not args.skip_main:
        hsi_csv, euro_csv, summary_csv = run_main_experiments(config, config_dict, output_dir)
        print(f"Saved main results: {hsi_csv}")
        print(f"Saved main results: {euro_csv}")
        print(f"Saved summary: {summary_csv}")
    if not args.skip_ablation:
        ablation_csv = run_eurosat_contract_ablation(config, config_dict, output_dir)
        print(f"Saved ablation results: {ablation_csv}")


if __name__ == "__main__":
    main()
