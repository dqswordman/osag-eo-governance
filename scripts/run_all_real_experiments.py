from __future__ import annotations

import argparse
import contextlib
import json
import shutil
import sys
import time
from pathlib import Path

import yaml

import generate_real_result_assets as assets
import reproduce_osag_real as core
import summarize_runtime as runtime_tools


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data: str) -> None:
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="One-click fresh rerun for OSAG real experiments.")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "osag_real_experiments.yaml")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seeds", type=int, nargs="+", default=None)
    parser.add_argument("--eurosat-pool", type=int, default=None)
    parser.add_argument("--skip-main", action="store_true")
    parser.add_argument("--skip-ablation", action="store_true")
    parser.add_argument("--run-name", type=str, default=None)
    return parser.parse_args()


def latest_file(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime)
    if not matches:
        raise FileNotFoundError(f"No files matching {pattern} in {directory}")
    return matches[-1]


def main() -> None:
    args = parse_args()
    config_dict = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    config = core.config_from_yaml(config_dict, args)
    project_root = core.resolve_repo_path(config_dict["paths"]["project_root"])
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    run_name = args.run_name if args.run_name else f"rerun_{timestamp}"

    raw_dir = project_root / "results" / "raw" / run_name
    hsi_dir = project_root / "results" / "hsi" / run_name
    euro_dir = project_root / "results" / "eurosat" / run_name
    tables_dir = project_root / "results" / "tables" / run_name
    figures_dir = project_root / "results" / "figures" / run_name
    runtime_dir = project_root / "results" / "runtime" / run_name
    logs_dir = project_root / "logs" / run_name
    manifest_dir = project_root / "artifacts" / "manifests"

    for path in [raw_dir, hsi_dir, euro_dir, tables_dir, figures_dir, runtime_dir, logs_dir, manifest_dir]:
        path.mkdir(parents=True, exist_ok=True)

    shutil.copy2(args.config, raw_dir / "config_snapshot.yaml")
    log_path = logs_dir / "run_all_real_experiments.log"

    with log_path.open("w", encoding="utf-8") as log_fh:
        tee = Tee(sys.stdout, log_fh)
        with contextlib.redirect_stdout(tee), contextlib.redirect_stderr(tee):
            print(f"Run name: {run_name}")
            print(f"Config: {args.config}")
            print(f"Resolved config: {config}")
            hsi_results = None
            euro_results = None
            summary_csv = None
            ablation_csv = None
            if not args.skip_main:
                hsi_results, euro_results, summary_csv = core.run_main_experiments(config, config_dict, raw_dir)
            if not args.skip_ablation:
                ablation_csv = core.run_eurosat_contract_ablation(config, config_dict, raw_dir)

            hsi_epoch = latest_file(raw_dir, "osag_contracts_indian_salinas_epoch_*.csv")
            euro_epoch = latest_file(raw_dir, "osag_contracts_eurosat_msi_epoch_*.csv")

            for path in raw_dir.glob("osag_contracts_indian_salinas*"):
                shutil.copy2(path, hsi_dir / path.name)
            for path in raw_dir.glob("indian_salinas_contracts_*.csv"):
                shutil.copy2(path, hsi_dir / path.name)
            for path in raw_dir.glob("osag_contracts_eurosat_msi*"):
                shutil.copy2(path, euro_dir / path.name)
            for path in raw_dir.glob("eurosat_msi_contracts_*.csv"):
                shutil.copy2(path, euro_dir / path.name)
            for path in raw_dir.glob("eurosat_contracts_*"):
                shutil.copy2(path, euro_dir / path.name)

            runtime_csv, runtime_md = runtime_tools.summarize_runtime([hsi_epoch, euro_epoch], runtime_dir)
            if hsi_results is None or euro_results is None:
                raise RuntimeError("Main experiment outputs are required to build tables and figures.")
            table_csv, table_md = assets.save_main_tables(assets.aggregate(hsi_results), assets.aggregate(euro_results), tables_dir)
            tradeoff = assets.plot_tradeoff(assets.aggregate(hsi_results), assets.aggregate(euro_results), figures_dir)
            sweeps = assets.plot_policy_sweeps(assets.aggregate(hsi_results), assets.aggregate(euro_results), figures_dir)
            ablation_fig = assets.plot_ablation(ablation_csv, figures_dir) if ablation_csv is not None else None

            run_manifest = {
                "run_name": run_name,
                "config": str(args.config),
                "python_executable": sys.executable,
                "device": str(core.DEVICE),
                "argv": sys.argv,
                "resolved_config": core.asdict(config),
                "paths": {
                    "raw_dir": str(raw_dir),
                    "hsi_dir": str(hsi_dir),
                    "eurosat_dir": str(euro_dir),
                    "tables_dir": str(tables_dir),
                    "figures_dir": str(figures_dir),
                    "runtime_dir": str(runtime_dir),
                    "logs_dir": str(logs_dir),
                },
                "outputs": {
                    "hsi_results": str(hsi_results),
                    "eurosat_results": str(euro_results),
                    "summary_csv": str(summary_csv),
                    "ablation_csv": str(ablation_csv),
                    "runtime_csv": str(runtime_csv),
                    "runtime_md": str(runtime_md),
                    "table_csv": str(table_csv),
                    "table_md": str(table_md),
                    "tradeoff_figure": str(tradeoff),
                    "sweeps_figure": str(sweeps),
                    "ablation_figure": str(ablation_fig) if ablation_fig else None,
                },
            }
            run_manifest_path = manifest_dir / f"{run_name}_manifest.json"
            run_manifest_path.write_text(json.dumps(run_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Run manifest: {run_manifest_path}")


if __name__ == "__main__":
    main()
