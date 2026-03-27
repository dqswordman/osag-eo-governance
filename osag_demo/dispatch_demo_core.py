from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DispatchConfig:
    grid_rows: int = 12
    grid_cols: int = 12
    steps: int = 10
    observe_budget: int = 14
    annotate_budget: int = 6
    knowledge_init: float = 0.46
    knowledge_gain: float = 0.08
    knowledge_decay: float = 0.012


POLICIES = [
    {"policy": "baseline_random", "display": "Random", "family": "baseline"},
    {"policy": "baseline_contract_priority", "display": "Contract-Priority", "family": "baseline"},
    {"policy": "osag_dispatch", "display": "OSAG", "family": "osag"},
]


CONTRACTS = [
    {"contract_id": 0, "contract_name": "Medical Core", "priority": 3, "target_weight": 0.22, "deadline_steps": 1, "palette": "#d1495b"},
    {"contract_id": 1, "contract_name": "Industrial Fire Belt", "priority": 3, "target_weight": 0.20, "deadline_steps": 1, "palette": "#edae49"},
    {"contract_id": 2, "contract_name": "Evacuation Corridor", "priority": 3, "target_weight": 0.18, "deadline_steps": 2, "palette": "#00798c"},
    {"contract_id": 3, "contract_name": "Residential South", "priority": 2, "target_weight": 0.16, "deadline_steps": 2, "palette": "#30638e"},
    {"contract_id": 4, "contract_name": "Floodplain East", "priority": 2, "target_weight": 0.14, "deadline_steps": 2, "palette": "#73a942"},
    {"contract_id": 5, "contract_name": "Perimeter Background", "priority": 1, "target_weight": 0.10, "deadline_steps": 4, "palette": "#6c757d"},
]


def gaussian_2d(rows: np.ndarray, cols: np.ndarray, center_r: float, center_c: float, sigma: float) -> np.ndarray:
    return np.exp(-(((rows - center_r) ** 2 + (cols - center_c) ** 2) / (2.0 * sigma**2)))


def build_dispatch_grid(config: DispatchConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    contracts_df = pd.DataFrame(CONTRACTS)
    rows = []
    cell_id = 0
    for r in range(config.grid_rows):
        for c in range(config.grid_cols):
            if r <= 2 and c <= 3:
                contract_id = 0
            elif r <= 3 and c >= 8:
                contract_id = 1
            elif 4 <= r <= 7 and 4 <= c <= 7:
                contract_id = 2
            elif r >= 8 and c <= 5:
                contract_id = 3
            elif c >= 9 and 4 <= r <= 10:
                contract_id = 4
            else:
                contract_id = 5
            contract = contracts_df.iloc[contract_id]
            pop = 0.35 + 0.05 * np.sin((r + 1) * 0.7) + 0.06 * np.cos((c + 1) * 0.5)
            if contract_id in {0, 2, 3}:
                pop += 0.28
            criticality = 0.22 + 0.07 * np.cos((r + c + 1) * 0.55)
            if contract_id in {0, 1, 2}:
                criticality += 0.36
            cloud_bias = 0.18 + 0.06 * np.sin((r - c) * 0.4)
            rows.append(
                {
                    "cell_id": cell_id,
                    "row": r,
                    "col": c,
                    "contract_id": contract_id,
                    "contract_name": contract["contract_name"],
                    "priority": int(contract["priority"]),
                    "target_weight": float(contract["target_weight"]),
                    "deadline_steps": int(contract["deadline_steps"]),
                    "palette": contract["palette"],
                    "population": float(np.clip(pop, 0.12, 0.92)),
                    "criticality": float(np.clip(criticality, 0.08, 0.96)),
                    "cloud_bias": float(np.clip(cloud_bias, 0.05, 0.32)),
                }
            )
            cell_id += 1
    return pd.DataFrame(rows), contracts_df


def compute_environment(grid_df: pd.DataFrame, step: int) -> pd.DataFrame:
    rows = grid_df["row"].to_numpy(dtype=np.float64)
    cols = grid_df["col"].to_numpy(dtype=np.float64)
    fire = 1.45 * gaussian_2d(rows, cols, 1.6 + 0.55 * step, 9.6 - 0.30 * step, sigma=1.9)
    corridor = 1.10 * gaussian_2d(rows, cols, 5.2 + 0.18 * step, 5.3 + 0.12 * step, sigma=2.4)
    flood = 0.95 * gaussian_2d(rows, cols, 7.4 + 0.16 * step, 10.2, sigma=2.2)
    hazard = fire + corridor + flood
    cloud = 0.18 + 0.14 * np.sin(0.62 * step + rows * 0.42 - cols * 0.21) + grid_df["cloud_bias"].to_numpy()
    visibility = np.clip(1.0 - cloud, 0.48, 0.98)
    urgency = hazard * (0.45 + grid_df["population"].to_numpy() + grid_df["criticality"].to_numpy()) * visibility
    active = urgency >= np.quantile(urgency, 0.72)
    out = grid_df.copy()
    out["step"] = step
    out["hazard"] = hazard
    out["visibility"] = visibility
    out["urgency"] = urgency
    out["is_active"] = active.astype(int)
    return out


def choose_observations(
    env_df: pd.DataFrame,
    policy: str,
    rng: np.random.Generator,
    observed_counts: dict[int, int],
    last_seen: dict[int, int],
    knowledge: dict[int, float],
    config: DispatchConfig,
) -> tuple[np.ndarray, dict[int, float], dict[int, float]]:
    total_selected = max(sum(observed_counts.values()), 1)
    target_counts = {
        cid: total_selected * float(target)
        for cid, target in env_df.groupby("contract_id")["target_weight"].first().to_dict().items()
    }
    deadline_pressure = {}
    coverage_gap = {}
    score = np.zeros(len(env_df), dtype=np.float64)
    priority_norm = (env_df["priority"].to_numpy(dtype=np.float64) - 1.0) / 2.0

    for cid, group in env_df.groupby("contract_id", sort=True):
        deadline = int(group["deadline_steps"].iloc[0])
        since = max(0, env_df["step"].iloc[0] - last_seen.get(int(cid), -1) - 1)
        deadline_pressure[int(cid)] = float(max(0.0, since - deadline + 1) / max(deadline, 1))
        coverage_gap[int(cid)] = float(max(target_counts[int(cid)] - observed_counts.get(int(cid), 0), 0.0))

    urgency = env_df["urgency"].to_numpy(dtype=np.float64)
    if policy == "baseline_random":
        probs = np.ones(len(env_df), dtype=np.float64)
        chosen = rng.choice(env_df["cell_id"].to_numpy(), size=config.observe_budget, replace=False, p=probs / probs.sum())
        return chosen, deadline_pressure, coverage_gap

    for idx, row in env_df.iterrows():
        cid = int(row["contract_id"])
        dpress = deadline_pressure[cid]
        gap = coverage_gap[cid]
        uncertainty = 1.0 - knowledge[cid]
        if policy == "baseline_contract_priority":
            score[idx] = 1.22 * row["priority"] + 0.68 * row["urgency"] + 0.18 * dpress + 0.05 * uncertainty
        elif policy == "osag_dispatch":
            score[idx] = (
                1.44 * row["urgency"]
                + 1.30 * dpress
                + 0.86 * gap / max(config.observe_budget, 1)
                + 0.46 * uncertainty
                + 0.44 * priority_norm[idx]
            )
        else:
            raise ValueError(f"Unknown policy: {policy}")
    order = np.argsort(score)[::-1]
    chosen = env_df.iloc[order[: config.observe_budget]]["cell_id"].to_numpy(dtype=np.int64)
    return chosen, deadline_pressure, coverage_gap


def visibility_safe(x: np.ndarray) -> np.ndarray:
    out = np.clip(x.astype(np.float64), 1e-6, None)
    return out / out.sum()


def choose_annotations(observed_df: pd.DataFrame, knowledge: dict[int, float], config: DispatchConfig) -> np.ndarray:
    if observed_df.empty:
        return np.array([], dtype=np.int64)
    score = (
        0.90 * observed_df["urgency"].to_numpy(dtype=np.float64)
        + 0.55 * (observed_df["priority"].to_numpy(dtype=np.float64) - 1.0)
        + 0.65 * np.array([1.0 - knowledge[int(cid)] for cid in observed_df["contract_id"]], dtype=np.float64)
    )
    order = np.argsort(score)[::-1]
    return observed_df.iloc[order[: config.annotate_budget]]["cell_id"].to_numpy(dtype=np.int64)


def run_dispatch_simulation(root: Path, config: DispatchConfig | None = None) -> dict[str, pd.DataFrame]:
    config = config or DispatchConfig()
    grid_df, contracts_df = build_dispatch_grid(config)
    rng_master = np.random.default_rng(20260321)
    frame_rows = []
    timeline_rows = []
    contract_rows = []
    summary_rows = []

    for policy_spec in POLICIES:
        policy = policy_spec["policy"]
        display = policy_spec["display"]
        rng = np.random.default_rng(rng_master.integers(0, 1_000_000))
        observed_counts = {int(cid): 0 for cid in contracts_df["contract_id"]}
        annotation_counts = {int(cid): 0 for cid in contracts_df["contract_id"]}
        last_seen = {int(cid): -9 for cid in contracts_df["contract_id"]}
        knowledge = {int(cid): float(config.knowledge_init + 0.02 * (contracts_df.loc[contracts_df["contract_id"] == cid, "priority"].iloc[0] - 1)) for cid in contracts_df["contract_id"]}
        missed_total = 0
        response_total = 0.0
        protected_total = 0.0
        active_total = 0.0

        for step in range(config.steps):
            env_df = compute_environment(grid_df, step)
            chosen_ids, deadline_pressure, coverage_gap = choose_observations(
                env_df=env_df,
                policy=policy,
                rng=rng,
                observed_counts=observed_counts,
                last_seen=last_seen,
                knowledge=knowledge,
                config=config,
            )
            chosen_set = set(int(x) for x in chosen_ids.tolist())
            observed_df = env_df[env_df["cell_id"].isin(chosen_set)].copy()
            annotated_ids = choose_annotations(observed_df, knowledge, config)
            annotated_set = set(int(x) for x in annotated_ids.tolist())

            step_gain = 0.0
            for cid, group in observed_df.groupby("contract_id", sort=True):
                cid = int(cid)
                observed_counts[cid] += int(len(group))
                last_seen[cid] = step
                reliability = 0.52 + 0.48 * knowledge[cid]
                step_gain += float((group["urgency"] * reliability * group["visibility"]).sum())
            response_total += step_gain

            for cid, count in observed_df.groupby("contract_id").size().to_dict().items():
                cid = int(cid)
                ann = sum(1 for cell in observed_df[observed_df["contract_id"] == cid]["cell_id"] if int(cell) in annotated_set)
                annotation_counts[cid] += ann
                gain = config.knowledge_gain * ann * (1.0 + 0.12 * (contracts_df.loc[contracts_df["contract_id"] == cid, "priority"].iloc[0] - 1))
                knowledge[cid] = float(min(0.985, knowledge[cid] + gain * (1.0 - knowledge[cid])))

            for cid in knowledge:
                if last_seen[cid] != step:
                    priority = int(contracts_df.loc[contracts_df["contract_id"] == cid, "priority"].iloc[0])
                    decay = config.knowledge_decay * (1.15 if priority >= 3 else 1.0)
                    knowledge[cid] = float(max(0.30, knowledge[cid] - decay))

            active_high = env_df[(env_df["priority"] >= 3) & (env_df["is_active"] == 1)]
            protected = active_high["cell_id"].isin(chosen_set).sum()
            active_total += float(len(active_high))
            protected_total += float(protected)

            total_obs = max(sum(observed_counts.values()), 1)
            observed_share = {
                cid: observed_counts[cid] / total_obs
                for cid in observed_counts
            }
            target_share = contracts_df.set_index("contract_id")["target_weight"].to_dict()

            missed_contracts = 0
            missed_contract_ids: set[int] = set()
            for cid, group in env_df.groupby("contract_id", sort=True):
                cid = int(cid)
                deadline = int(group["deadline_steps"].iloc[0])
                priority = int(group["priority"].iloc[0])
                if priority < 3:
                    continue
                active_cells = group[group["is_active"] == 1]
                active_contract = not active_cells.empty
                since = step - last_seen[cid]
                observed_active = int(active_cells["cell_id"].isin(chosen_set).sum())
                required_active = max(1, int(np.ceil(len(active_cells) * 0.30)))
                under_served = observed_counts[cid] < max(1.0, total_obs * target_share[cid] * 0.92)
                missed = active_contract and (observed_active < required_active or since >= deadline or under_served)
                if missed:
                    missed_contracts += 1
                    missed_contract_ids.add(cid)
            missed_total += missed_contracts

            coverage_error = float(sum(abs(observed_share[cid] - target_share[cid]) for cid in observed_share))
            service_compliance = float(
                np.mean(
                    [
                        max(0.0, 1.0 - abs(observed_share[int(cid)] - target_share[int(cid)]) / max(target_share[int(cid)], 1e-6))
                        for cid in contracts_df["contract_id"]
                    ]
                )
            )

            for _, row in env_df.iterrows():
                cid = int(row["contract_id"])
                frame_rows.append(
                    {
                        "step": step,
                        "policy": policy,
                        "display": display,
                        "cell_id": int(row["cell_id"]),
                        "row": int(row["row"]),
                        "col": int(row["col"]),
                        "contract_id": cid,
                        "contract_name": row["contract_name"],
                        "priority": int(row["priority"]),
                        "hazard": float(row["hazard"]),
                        "urgency": float(row["urgency"]),
                        "visibility": float(row["visibility"]),
                        "observed": int(int(row["cell_id"]) in chosen_set),
                        "annotated": int(int(row["cell_id"]) in annotated_set),
                        "is_active": int(row["is_active"]),
                        "knowledge": float(knowledge[cid]),
                        "deadline_pressure": float(deadline_pressure[cid]),
                        "coverage_gap": float(coverage_gap[cid]),
                        "missed_contract": int(cid in missed_contract_ids),
                    }
                )

            for cid, contract in contracts_df.set_index("contract_id").iterrows():
                contract_rows.append(
                    {
                        "step": step,
                        "policy": policy,
                        "display": display,
                        "contract_id": int(cid),
                        "contract_name": contract["contract_name"],
                        "priority": int(contract["priority"]),
                        "target_weight": float(contract["target_weight"]),
                        "observed_count": int(observed_counts[int(cid)]),
                        "annotation_count": int(annotation_counts[int(cid)]),
                        "observed_share": float(observed_share[int(cid)]),
                        "coverage_gap": float(target_share[int(cid)] * total_obs - observed_counts[int(cid)]),
                        "deadline_pressure": float(deadline_pressure[int(cid)]),
                        "knowledge": float(knowledge[int(cid)]),
                    }
                )

            timeline_rows.append(
                {
                    "step": step,
                    "policy": policy,
                    "display": display,
                    "service_gain_step": float(step_gain),
                    "service_gain_cum": float(response_total),
                    "critical_capture_rate": float(protected / max(len(active_high), 1)),
                    "critical_capture_cum": float(protected_total / max(active_total, 1.0)),
                    "missed_service_step": int(missed_contracts),
                    "missed_service_cum": int(missed_total),
                    "coverage_error": coverage_error,
                    "service_compliance": service_compliance,
                    "budget_obs_used": int(len(chosen_set)),
                    "budget_ann_used": int(len(annotated_set)),
                    "model_quality_high": float(np.mean([knowledge[int(cid)] for cid in contracts_df.loc[contracts_df["priority"] >= 3, "contract_id"]])),
                }
            )

        final = pd.DataFrame(timeline_rows)
        last = final[final["policy"] == policy].sort_values("step").iloc[-1]
        summary_rows.append(
            {
                "policy": policy,
                "display": display,
                "family": policy_spec["family"],
                "total_service_gain": float(last["service_gain_cum"]),
                "final_coverage_error": float(last["coverage_error"]),
                "missed_service_total": int(last["missed_service_cum"]),
                "critical_capture_rate": float(last["critical_capture_cum"]),
                "service_compliance": float(last["service_compliance"]),
                "avg_budget_obs": float(
                    pd.DataFrame(timeline_rows).query("policy == @policy")["budget_obs_used"].mean()
                ),
                "avg_budget_ann": float(
                    pd.DataFrame(timeline_rows).query("policy == @policy")["budget_ann_used"].mean()
                ),
                "final_model_quality_high": float(last["model_quality_high"]),
            }
        )

    timeline_df = pd.DataFrame(timeline_rows)
    max_cov = max(float(timeline_df["coverage_error"].max()), 1e-6)
    max_missed = max(int(timeline_df["missed_service_cum"].max()), 1)
    timeline_df["reliability_score"] = 100.0 * (
        0.42 * timeline_df["service_compliance"]
        + 0.28 * (1.0 - timeline_df["coverage_error"] / max_cov)
        + 0.18 * (1.0 - timeline_df["missed_service_cum"] / max_missed)
        + 0.12 * timeline_df["critical_capture_cum"]
    )
    summary_df = pd.DataFrame(summary_rows)
    summary_df["reliability_score"] = 100.0 * (
        0.42 * summary_df["service_compliance"]
        + 0.28 * (1.0 - summary_df["final_coverage_error"] / max_cov)
        + 0.18 * (1.0 - summary_df["missed_service_total"] / max_missed)
        + 0.12 * summary_df["critical_capture_rate"]
    )

    real_table_path = root / "results" / "tables" / "rerun_20260321_combined_main5" / "fresh_main_results.csv"
    real_summary = pd.read_csv(real_table_path) if real_table_path.exists() else pd.DataFrame()

    return {
        "config": pd.DataFrame(
            [
                {
                    "steps": config.steps,
                    "observe_budget": config.observe_budget,
                    "annotate_budget": config.annotate_budget,
                    "grid_rows": config.grid_rows,
                    "grid_cols": config.grid_cols,
                }
            ]
        ),
        "grid": grid_df,
        "contracts": contracts_df,
        "frames": pd.DataFrame(frame_rows),
        "timeline": timeline_df,
        "contract_state": pd.DataFrame(contract_rows),
        "summary": summary_df.sort_values(["reliability_score", "final_coverage_error"], ascending=[False, True]),
        "real_summary": real_summary,
    }
