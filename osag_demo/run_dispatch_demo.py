from __future__ import annotations

import argparse
from pathlib import Path

from dispatch_demo_assets import (
    build_dashboard,
    plot_contract_gap,
    plot_policy_timeline,
    plot_step_comparison,
    save_tables,
    save_text_summary,
)
from dispatch_demo_core import run_dispatch_simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the emergency dispatch OSAG demo.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "visual_outputs")
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    root = Path(__file__).resolve().parents[1]
    results = run_dispatch_simulation(root)
    save_tables(results, output_dir)
    plot_policy_timeline(results, output_dir)
    plot_step_comparison(results, output_dir, step=7)
    plot_contract_gap(results, output_dir, step=7)
    save_text_summary(results, output_dir)
    build_dashboard(results, output_dir)

    print(results["summary"].to_string(index=False))
    print(f"\nDispatch demo artifacts saved to: {output_dir}")


if __name__ == "__main__":
    main()
