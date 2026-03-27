from __future__ import annotations

import argparse
import hashlib
import json
import time
import zipfile
from pathlib import Path
from typing import Any

import requests
import yaml
from requests.exceptions import ChunkedEncodingError, ConnectionError, ReadTimeout
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def head_content_length(session: requests.Session, url: str) -> int | None:
    try:
        resp = session.head(url, allow_redirects=True, timeout=60)
        resp.raise_for_status()
        content_length = resp.headers.get("Content-Length")
        return int(content_length) if content_length is not None else None
    except Exception:
        return None


def verify_mat_variable(path: Path, variable: str) -> tuple[bool, str]:
    try:
        data = loadmat(path)
        if variable not in data:
            return False, f"missing variable `{variable}`"
        arr = data[variable]
        return True, f"{variable} shape={arr.shape} dtype={arr.dtype}"
    except Exception as exc:
        return False, f"loadmat failed: {exc}"


def verify_md5_zip(path: Path, expected_md5: str) -> tuple[bool, str]:
    digest = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    actual = digest.hexdigest()
    if actual != expected_md5:
        return False, f"md5 mismatch: expected {expected_md5}, got {actual}"
    if not zipfile.is_zipfile(path):
        return False, "downloaded file is not a valid zip archive"
    return True, f"md5={actual}"


def verify_file(path: Path, verify_cfg: dict[str, Any]) -> tuple[bool, str]:
    kind = str(verify_cfg["kind"])
    if kind == "mat_variable":
        return verify_mat_variable(path, str(verify_cfg["variable"]))
    if kind == "md5_zip":
        return verify_md5_zip(path, str(verify_cfg["md5"]))
    raise ValueError(f"Unknown verification kind: {kind}")


def extract_zip_if_needed(zip_path: Path, extract_root: Path) -> str:
    target_dir = extract_root / "EuroSAT_MS"
    if target_dir.exists() and any(target_dir.iterdir()):
        return f"extraction already present at {target_dir}"
    extract_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_root)
    return f"extracted archive to {extract_root}"


def download_with_retries(url: str, target: Path, expected_bytes: int | None, retries: int) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    for attempt in range(1, retries + 1):
        existing = target.stat().st_size if target.exists() else 0
        if expected_bytes is not None and existing > expected_bytes:
            target.unlink(missing_ok=True)
            existing = 0

        headers = {"Range": f"bytes={existing}-"} if existing > 0 else {}
        mode = "ab"
        try:
            with session.get(url, headers=headers, allow_redirects=True, stream=True, timeout=120) as resp:
                resp.raise_for_status()
                if resp.status_code == 200:
                    mode = "wb"
                with target.open(mode) as fh:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            fh.write(chunk)
        except (ChunkedEncodingError, ConnectionError, ReadTimeout) as exc:
            print(f"Attempt {attempt}/{retries} interrupted for {target.name}: {exc}")
            time.sleep(2)
            continue

        size = target.stat().st_size if target.exists() else 0
        if expected_bytes is None or size == expected_bytes:
            return
        print(f"Attempt {attempt}/{retries} incomplete for {target.name}: {size}/{expected_bytes} bytes")
        time.sleep(2)
    raise RuntimeError(f"Failed to download complete file for {target.name} after {retries} attempts")


def process_dataset(key: str, spec: dict[str, Any], retries: int, force: bool) -> dict[str, Any]:
    if not bool(spec.get("canonical", False)):
        raise RuntimeError(f"{key} is not canonical and cannot be used by this downloader")

    source_url = str(spec["source_url"])
    target = resolve_repo_path(spec["local_path"])
    verify_cfg = dict(spec["verify"])
    session = requests.Session()
    expected_bytes = head_content_length(session, source_url)

    if target.exists() and not force:
        ok, detail = verify_file(target, verify_cfg)
        if ok:
            return {
                "dataset_key": key,
                "status": "already_valid",
                "local_path": str(target),
                "detail": detail,
                "source_url": source_url,
                "expected_bytes": expected_bytes,
            }

    if force and target.exists():
        target.unlink()

    download_with_retries(source_url, target, expected_bytes, retries)
    ok, detail = verify_file(target, verify_cfg)
    if not ok:
        raise RuntimeError(f"Verification failed for {key}: {detail}")
    extraction_detail = None
    if verify_cfg["kind"] == "md5_zip" and "extracted_path" in spec:
        extraction_detail = extract_zip_if_needed(target, resolve_repo_path(spec["extracted_path"]))
    return {
        "dataset_key": key,
        "status": "downloaded",
        "local_path": str(target),
        "detail": detail,
        "extraction_detail": extraction_detail,
        "source_url": source_url,
        "expected_bytes": expected_bytes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download canonical OSAG datasets and verify them.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "configs" / "osag_real_experiments.yaml",
    )
    parser.add_argument("--dataset", action="append", help="Specific dataset key from the config. Repeatable.")
    parser.add_argument("--retries", type=int, default=12)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    dataset_specs = dict(config["datasets"])
    selected = args.dataset if args.dataset else list(dataset_specs.keys())
    results = []
    for key in selected:
        if key not in dataset_specs:
            raise SystemExit(f"Unknown dataset key: {key}")
        spec = dataset_specs[key]
        print(f"Processing {key}")
        result = process_dataset(key, spec, retries=args.retries, force=args.force)
        print(f"  {result['status']}: {result['detail']}")
        results.append(result)

    manifest = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": str(args.config),
        "results": results,
    }
    artifact_root = resolve_repo_path(config["paths"]["artifact_root"])
    artifact_root.mkdir(parents=True, exist_ok=True)
    manifest_path = artifact_root / f"canonical_download_manifest_{time.strftime('%Y%m%d_%H%M%S')}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Manifest written to: {manifest_path}")


if __name__ == "__main__":
    main()
