from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def aggregate(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return (
        df.groupby(["dataset", "display", "method", "alpha", "lambda_c"], as_index=False)
        .agg(
            test_acc_all_mean=("test_acc_all", "mean"),
            test_acc_all_std=("test_acc_all", "std"),
            test_acc_high_contract_mean=("test_acc_high_contract", "mean"),
            test_acc_high_contract_std=("test_acc_high_contract", "std"),
            priority_coverage_error_mean_mean=("priority_coverage_error_mean", "mean"),
            priority_coverage_error_mean_std=("priority_coverage_error_mean", "std"),
        )
        .reset_index(drop=True)
    )


def pick(df: pd.DataFrame, display: str) -> pd.Series:
    sub = df[df["display"] == display]
    if sub.empty:
        raise KeyError(display)
    return sub.iloc[0]


def save_main_tables(hsi: pd.DataFrame, euro: pd.DataFrame, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    table_rows = []
    for dataset_name, df in [("Indian+Salinas", hsi), ("EuroSAT MSI", euro)]:
        ordered = df.sort_values(
            ["priority_coverage_error_mean_mean", "test_acc_high_contract_mean"],
            ascending=[True, False],
        )
        for _, row in ordered.iterrows():
            table_rows.append(
                {
                    "dataset": dataset_name,
                    "policy": row["display"],
                    "acc_all_mean": row["test_acc_all_mean"],
                    "acc_all_std": row["test_acc_all_std"],
                    "acc_high_mean": row["test_acc_high_contract_mean"],
                    "acc_high_std": row["test_acc_high_contract_std"],
                    "prio_cov_err_mean": row["priority_coverage_error_mean_mean"],
                    "prio_cov_err_std": row["priority_coverage_error_mean_std"],
                }
            )

    out_csv = output_dir / "fresh_main_results.csv"
    out_md = output_dir / "fresh_main_results.md"
    pd.DataFrame(table_rows).to_csv(out_csv, index=False)

    lines = [
        "# Fresh Main Results",
        "",
        "| Dataset | Policy | Accall | Acchigh | PrioCovErr |",
        "|---|---|---:|---:|---:|",
    ]
    for row in table_rows:
        lines.append(
            f"| {row['dataset']} | {row['policy']} | "
            f"{100.0 * row['acc_all_mean']:.2f} +/- {100.0 * row['acc_all_std']:.2f} | "
            f"{100.0 * row['acc_high_mean']:.2f} +/- {100.0 * row['acc_high_std']:.2f} | "
            f"{100.0 * row['prio_cov_err_mean']:.2f} +/- {100.0 * row['prio_cov_err_std']:.2f} |"
        )
    out_md.write_text("\n".join(lines), encoding="utf-8")
    return out_csv, out_md


def plot_tradeoff(hsi: pd.DataFrame, euro: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.5), sharey=True)
    datasets = [("Indian+Salinas", hsi), ("EuroSAT MSI", euro)]
    for ax, (title, df) in zip(axes, datasets):
        for _, row in df.iterrows():
            x = 100.0 * row["priority_coverage_error_mean_mean"]
            y = 100.0 * row["test_acc_high_contract_mean"]
            ax.scatter(x, y, s=80)
            ax.annotate(row["display"], (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)
        ax.set_title(title)
        ax.set_xlabel("PrioCovErr (%)")
        ax.grid(alpha=0.2)
    axes[0].set_ylabel("Acchigh (%)")
    fig.tight_layout()
    out = output_dir / "fresh_tradeoff.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    return out


def plot_policy_sweeps(hsi: pd.DataFrame, euro: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 8.2))
    for col, (title, df) in enumerate([("Indian+Salinas", hsi), ("EuroSAT MSI", euro)]):
        alpha_labels = ["Random", "OSAG-Mix (a=0.25)", "OSAG-Mix (a=0.50)", "OSAG-Mix (a=0.75)", "OSAG"]
        alpha_rows = [pick(df, label) for label in alpha_labels if not df[df["display"] == label].empty]
        ax = axes[0, col]
        ax.plot(
            [100.0 * row["priority_coverage_error_mean_mean"] for row in alpha_rows],
            [100.0 * row["test_acc_high_contract_mean"] for row in alpha_rows],
            "-o",
            linewidth=2.0,
        )
        for row in alpha_rows:
            ax.annotate(
                row["display"],
                (100.0 * row["priority_coverage_error_mean_mean"], 100.0 * row["test_acc_high_contract_mean"]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
            )
        ax.set_title(f"{title}: alpha sweep")
        ax.set_xlabel("PrioCovErr (%)")
        ax.set_ylabel("Acchigh (%)")
        ax.grid(alpha=0.2)

        lambda_labels = ["OSAG", "OSAG-FairLoss (l=0.5)", "OSAG-FairLoss (l=1.0)"]
        lambda_rows = [pick(df, label) for label in lambda_labels if not df[df["display"] == label].empty]
        ax = axes[1, col]
        ax.plot(
            [100.0 * row["test_acc_all_mean"] for row in lambda_rows],
            [100.0 * row["test_acc_high_contract_mean"] for row in lambda_rows],
            "-o",
            linewidth=2.0,
        )
        for row in lambda_rows:
            ax.annotate(
                row["display"],
                (100.0 * row["test_acc_all_mean"], 100.0 * row["test_acc_high_contract_mean"]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
            )
        ax.set_title(f"{title}: lambda sweep")
        ax.set_xlabel("Accall (%)")
        ax.set_ylabel("Acchigh (%)")
        ax.grid(alpha=0.2)
    fig.tight_layout()
    out = output_dir / "fresh_policy_sweeps.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    return out


def plot_ablation(ablation_csv: Path | None, output_dir: Path) -> Path | None:
    if ablation_csv is None or not ablation_csv.exists():
        return None
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(ablation_csv)
    final_df = df.sort_values("epoch").groupby(["run_tag", "display", "seed", "variant"], as_index=False).tail(1)
    grouped = final_df.groupby(["variant", "display"], as_index=False).agg(
        test_acc_all_mean=("test_acc_all", "mean"),
        priority_coverage_error_mean_mean=("priority_coverage_error_mean", "mean"),
    )
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for _, row in grouped.iterrows():
        ax.scatter(100.0 * row["priority_coverage_error_mean_mean"], 100.0 * row["test_acc_all_mean"], s=80)
        ax.annotate(
            f"{row['variant']}:{row['display']}",
            (100.0 * row["priority_coverage_error_mean_mean"], 100.0 * row["test_acc_all_mean"]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
        )
    ax.set_xlabel("PrioCovErr (%)")
    ax.set_ylabel("Accall (%)")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    out = output_dir / "fresh_eurosat_ablation.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate tables and figures from OSAG rerun CSV files.")
    parser.add_argument("--hsi-results", type=Path, required=True)
    parser.add_argument("--eurosat-results", type=Path, required=True)
    parser.add_argument("--ablation-csv", type=Path, default=None)
    parser.add_argument("--tables-dir", type=Path, required=True)
    parser.add_argument("--figures-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hsi = aggregate(args.hsi_results)
    euro = aggregate(args.eurosat_results)
    table_csv, table_md = save_main_tables(hsi, euro, args.tables_dir)
    tradeoff = plot_tradeoff(hsi, euro, args.figures_dir)
    sweeps = plot_policy_sweeps(hsi, euro, args.figures_dir)
    ablation = plot_ablation(args.ablation_csv, args.figures_dir)
    print(table_csv)
    print(table_md)
    print(tradeoff)
    print(sweeps)
    if ablation is not None:
        print(ablation)


if __name__ == "__main__":
    main()
