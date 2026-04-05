# Current Artifacts Verification

## Thesis current path

Verified current thesis path:

- `thesis_current/main_Thesis_2026_current.pdf`

Checks:

- SHA-256 matches the locked thesis source:
  - `thesis_current/main_Thesis_2026_current.pdf`
  - `LaTeX_Thesis2026/LaTeX_Thesis2026/main_Thesis_2026.pdf`
  - `latex_submission_2025/main_Thesis_2026.pdf`
- PDF page count:
  - `61`

Result:

- thesis current path works

## Presentation current path

Verified current presentation paths:

- `presentation_current/osag_defense_deck_en_current.pptx`
- `presentation_current/osag_defense_deck_en_current.pdf`

Checks:

- PDF page count:
  - `16`
- PPTX zip-integrity test:
  - no compressed-data errors reported by `unzip -t`

Result:

- presentation current path works

## Demo current path

Verified current demo path:

- `demo_current/index.html`

Checks:

- `index.html` references only local files:
  - `assets/style.css`
  - `assets/scenarios.js`
  - `assets/app.js`
- missing referenced local files:
  - none
- external network URLs referenced by `index.html`:
  - none
- launcher scripts both target the same local entry:
  - `demo_current/open_demo.bat`
  - `demo_current/open_demo.ps1`
  - both open `index.html`

Result:

- demo current path works
- demo remains offline and relative-path based

## Reading current completeness

Verified current reading folder:

- `reading_current/`

Check:

- current reading file count:
  - `17`

Result:

- `reading_current` is complete for current rehearsal and support use

## Submission current completeness

Verified submission folder:

- `submission_current/`

Checks:

- current submission file count:
  - `6`
- `latex_submission_2025.zip` is present and readable
- zip listing confirms thesis package contents are present

Result:

- `submission_current` is complete

## Summary

Explicit confirmations:

1. demo current path works
2. presentation current path works
3. thesis current path works
4. `reading_current` is complete
5. `submission_current` is complete

