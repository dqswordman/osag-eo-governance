# Project Current State Map

## Current official thesis artifacts

- Current thesis PDF:
  - `thesis_current/main_Thesis_2026_current.pdf`
- Factual authority source:
  - `LaTeX_Thesis2026/LaTeX_Thesis2026/main_Thesis_2026.pdf`
- Matching submission-side PDF source:
  - `latex_submission_2025/main_Thesis_2026.pdf`

The locked thesis PDF and the submission-side PDF match by hash. The older package copy `archive/packages_old/final_defense_package_2026-04-08/01_thesis/main_Thesis_2026_final.pdf` does not match the locked thesis hash and is therefore deprecated as a current-facing thesis entrypoint.

## Current official presentation artifacts

- Current PPT:
  - `presentation_current/osag_defense_deck_en_current.pptx`
- Current PDF:
  - `presentation_current/osag_defense_deck_en_current.pdf`
- Current notes:
  - `presentation_current/osag_defense_deck_notes_en_current.md`
- Current audit:
  - `presentation_current/osag_defense_deck_audit_en_current.md`

These files are copied from the final clean deck outputs:

- `deliverables/osag_defense_deck_en_final_clean.pptx`
- `deliverables/osag_defense_deck_en_final_clean.pdf`

Deprecated deck variants were moved under `archive/decks_old/`.

## Current official demo artifacts

- Current demo folder:
  - `demo_current/`
- Current demo entry:
  - `demo_current/index.html`

Source note:

- `demo_current/` is copied from the latest offline engineered demo package.
- `demo_latest` and `demo_engineered_v2` were compared and found identical, so `demo_current/` is the single current-facing demo location.

## Current reading and support materials

- Current reading folder:
  - `reading_current/`
- Current reading set includes:
  - thesis story and FAQ notes in Chinese
  - code walkthrough and demo code-mapping notes
  - demo explanation and committee question notes
  - bilingual slide-by-slide script
  - final clean deck notes and audit

## Current submission artifacts

- Current submission folder:
  - `submission_current/`
- Included:
  - current thesis PDF
  - `latex_submission_2025.zip`
  - submission manifest and zip verification
  - supervisor-facing corrections report

## Reports, manifests, and audit files

- Current organization and verification reports:
  - `reports/`
- Current-facing report copies:
  - `reports_current/`

## Deprecated or archived materials

Deprecated or superseded materials were moved out of the current-facing surface:

- Older deck families:
  - `archive/decks_old/`
- Older notes, audits, and rebuild reports:
  - `archive/reports_old/`
- Superseded convenience bundles:
  - `archive/packages_old/final_defense_package_2026-04-08/`
  - `archive/packages_old/latest_needed_files_2026-04-05/`
- Older package-level or reference archives:
  - `archive/packages_old/audit_bundle/`
  - `archive/packages_old/igarss-eo11.29-12.4/`

## Folders safe to treat as archive

The following are no longer current-facing entry layers and can be treated as archive or historical reference:

- `archive/decks_old/`
- `archive/reports_old/`
- `archive/packages_old/`

## GitHub repository boundary

The outer workspace is not itself a git repository. The tracked GitHub repository for publication is:

- `osag-eo-governance/`

That repository receives a mirrored current-facing structure for GitHub publication.

