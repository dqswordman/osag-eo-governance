# Dataset Layout

This directory is reserved for the formal local inputs expected by the public rerun pipeline.

Required files:

- `Indian_pines_corrected.mat`
- `Indian_pines_gt.mat`
- `Salinas_corrected.mat`
- `Salinas_gt.mat`
- `EuroSAT_MS.zip`

The repository does not redistribute these datasets. Use the canonical download script in `scripts/download_canonical_data.py` or place the files manually from the official sources listed in `configs/osag_real_experiments.yaml`.
