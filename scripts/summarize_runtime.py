from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def summarize_runtime(epoch_csvs: list[Path], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = [pd.read_csv(path) for path in epoch_csvs]
    df = pd.concat(frames, ignore_index=True)
    per_seed = (
        df.groupby(["dataset", "display", "method", "alpha", "lambda_c", "seed"], as_index=False)
        .agg(
            avg_epoch_time_sec=("epoch_time_sec", "mean"),
            total_training_time_sec=("epoch_time_sec", "sum"),
            epochs=("epoch", "max"),
        )
    )
    summary = (
        per_seed.groupby(["dataset", "display", "method", "alpha", "lambda_c"], as_index=False)
        .agg(
            avg_epoch_time_sec_mean=("avg_epoch_time_sec", "mean"),
            avg_epoch_time_sec_std=("avg_epoch_time_sec", "std"),
            total_training_time_sec_mean=("total_training_time_sec", "mean"),
            total_training_time_sec_std=("total_training_time_sec", "std"),
            seeds=("seed", "count"),
            epochs=("epochs", "max"),
        )
        .sort_values(["dataset", "total_training_time_sec_mean", "display"])
        .reset_index(drop=True)
    )

    csv_path = output_dir / "runtime_summary.csv"
    md_path = output_dir / "runtime_summary.md"
    per_seed.to_csv(output_dir / "runtime_per_seed.csv", index=False)
    summary.to_csv(csv_path, index=False)

    lines = [
        "# Runtime Summary",
        "",
        "| Dataset | Policy | Seeds | Epochs | Avg/Epoch (s) | Total (s) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for _, row in summary.iterrows():
        lines.append(
            f"| {row['dataset']} | {row['display']} | {int(row['seeds'])} | {int(row['epochs'])} | "
            f"{row['avg_epoch_time_sec_mean']:.3f} | {row['total_training_time_sec_mean']:.3f} |"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return csv_path, md_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize runtime statistics from epoch CSV files.")
    parser.add_argument("--epoch-csv", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_path, md_path = summarize_runtime(args.epoch_csv, args.output_dir)
    print(csv_path)
    print(md_path)


if __name__ == "__main__":
    main()
