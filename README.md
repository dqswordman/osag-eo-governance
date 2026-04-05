# OSAG EO Governance

OSAG EO Governance is the public code-and-artifact release for governance-aware Earth Observation learning built around **Observed Service Agreement Graphs (OSAG)**. The repository combines:

- a script-driven rerun pipeline for contract-governed HSI and EuroSAT MSI experiments, and
- a runnable offline dispatch demo that explains the same governance idea in an operational setting.

## Current-facing entrypoints

Use these folders first. They are the clean current-facing layer for the published repository.

- Current thesis PDF:
  - `thesis_current/main_Thesis_2026_current.pdf`
- Current defense deck:
  - `presentation_current/osag_defense_deck_en_current.pptx`
  - `presentation_current/osag_defense_deck_en_current.pdf`
- Current defense notes and audit:
  - `presentation_current/osag_defense_deck_notes_en_current.md`
  - `presentation_current/osag_defense_deck_audit_en_current.md`
- Current offline demo:
  - `demo_current/index.html`
- Current reading materials:
  - `reading_current/`
- Current submission artifacts:
  - `submission_current/`
- Current organization and verification reports:
  - `reports_current/`

## Highlights

- Contract-governed training over semantically meaningful service units.
- Thesis-aligned result snapshots for quick public inspection.
- Lightweight benchmarking scripts that wrap standard classifiers rather than introducing a new backbone family.
- A browser-friendly offline demo for budgets, deadlines, coverage gaps, and missed service.

## Repository layout

```text
osag-eo-governance/
|-- archive/
|-- configs/
|-- dataset/
|-- demo_current/
|-- docs/
|   `-- images/
|-- osag_demo/
|-- presentation_current/
|-- reading_current/
|-- reports_current/
|-- results_snapshot/
|-- submission_current/
|-- scripts/
`-- thesis_current/
```

- `thesis_current/` is the clean thesis entrypoint for readers.
- `presentation_current/` contains the official current defense deck set.
- `demo_current/` contains the official current offline demo package.
- `reading_current/` contains the current Chinese rehearsal and support materials.
- `submission_current/` contains the current submission-facing thesis package.
- `reports_current/` contains current organization, verification, and rebuild reports.
- `archive/` marks legacy or superseded materials and points to older archive locations.
- `configs/` contains the experiment configuration used by the public release.
- `dataset/` is the expected location for canonical local inputs. Data are not redistributed here.
- `scripts/` contains the main rerun, download, runtime, and asset-generation utilities.
- `osag_demo/` contains the emergency dispatch simulation and dashboard entry points.
- `results_snapshot/` contains small thesis-aligned CSV snapshots for quick inspection.
- `docs/images/` contains figures used in this README.

## Current thesis, deck, and demo

- Current official thesis PDF:
  - `thesis_current/main_Thesis_2026_current.pdf`
- Current official defense deck:
  - `presentation_current/osag_defense_deck_en_current.pptx`
  - `presentation_current/osag_defense_deck_en_current.pdf`
- Current official demo:
  - `demo_current/index.html`

The current deck is the final clean English deck. The current demo is the latest offline engineered demo package.

## Reading and submission materials

- Current reading materials:
  - `reading_current/`
- Current submission package:
  - `submission_current/`

Start reading with:

1. `reading_current/00_reading_order_cn.md`
2. `reading_current/01_thesis_core_story_cn.md`
3. `reading_current/02_defense_faq_cn.md`

## Archived and legacy materials

Older package-oriented materials remain available for history and audit, but they are not the current-facing entrypoints:

- `final_defense_package_2026-04-08/`
- `final_defense_package_2026-04-08/05_archive_optional/`
- `archive/`

## What this release covers

This public repository focuses on the main thesis-aligned workflow:

1. canonical data download and verification,
2. script-based rerun of the main benchmark,
3. runtime summarization and result-table generation,
4. dispatch-demo generation and visualization,
5. small result snapshots and documentation assets.

The repository is intentionally focused on the main public workflow rather than on every internal thesis-side utility.

## Environment

The original thesis reruns were executed in a CUDA-enabled Python 3.9 environment with PyTorch 2.8.0+cu128. The code can also run in any equivalent environment that satisfies the dependencies in `requirements.txt`.

Install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Canonical data layout

Place the formal inputs under `dataset/`:

- `dataset/Indian_pines_corrected.mat`
- `dataset/Indian_pines_gt.mat`
- `dataset/Salinas_corrected.mat`
- `dataset/Salinas_gt.mat`
- `dataset/EuroSAT_MS.zip`

You can also download the canonical sources directly with:

```powershell
python .\scripts\download_canonical_data.py --config .\configs\osag_real_experiments.yaml
```

For EuroSAT, the downloader verifies the official MD5 and extracts the archive to `data/raw/eurosat/`.

## Running the main benchmark

The default configuration is set up for the thesis-aligned five-seed main rerun.

```powershell
python .\scripts\run_all_real_experiments.py --config .\configs\osag_real_experiments.yaml --run-name rerun_main5
```

Key outputs will be written under:

- `results/raw/<run_name>/`
- `results/tables/<run_name>/`
- `results/figures/<run_name>/`
- `results/runtime/<run_name>/`
- `logs/<run_name>/`

## Running the current demo

Open the current offline demo directly:

```powershell
start .\demo_current\index.html
```

or use:

```powershell
.\demo_current\open_demo.bat
```

The current demo is static and offline. No backend or network is required.

For the script-driven demo builder in the codebase, generate the dispatch dashboard with:

```powershell
python .\osag_demo\run_visual_demo.py
python .\osag_demo\launch_visual_demo.py
```

The builder writes its artifacts to `osag_demo/visual_outputs/`.

## Thesis-aligned result snapshot

The `results_snapshot/` directory includes compact CSV exports from the locked thesis workspace:

- `fresh_main_results.csv`
- `runtime_summary.csv`
- `demo_dispatch_summary.csv`
- `demo_dispatch_contracts.csv`
- `eurosat_backbone_comparison.csv`

These files are included for inspection and documentation. They are not a substitute for rerunning the pipeline from canonical inputs.

## Selected figures

### Governance Pipeline

![Governance pipeline](docs/images/pipeline.png)

### Benchmark Frontier

![Benchmark trade-off](docs/images/benchmark_tradeoff.png)

### Dispatch Timeline

![Dispatch timeline](docs/images/dispatch_timeline.png)

### Dispatch Step Comparison

![Dispatch step comparison](docs/images/dispatch_step8_comparison.png)

## Operational interpretation

The dispatch demo is not a replacement for the benchmark. Its purpose is to visualize the operational consequence of governance:

- which contracts are being served,
- where coverage deviates from target,
- how deadline pressure changes behavior,
- and why explicit governance differs from both Random and heuristic Contract-Priority dispatch.

## Citation

If you use this code or the public release structure, please cite the associated thesis and the conference-paper lineage described in the thesis bibliography.

## License

This repository is released under the MIT License. See `LICENSE`.

## GitHub tag

Current published cleanup tag:

- `v2026-final-cleanup`
