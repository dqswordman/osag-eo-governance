from __future__ import annotations

from pathlib import Path
import webbrowser


def main() -> None:
    dashboard = Path(__file__).resolve().parent / "visual_outputs" / "demo_dashboard.html"
    if not dashboard.exists():
        raise SystemExit("Dashboard not found. Run `python .\\osag_demo\\run_visual_demo.py` first.")
    webbrowser.open(dashboard.as_uri())
    print(f"Opened: {dashboard}")


if __name__ == "__main__":
    main()
