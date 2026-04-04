# English Defense Deck Audit

## Build Scope

- New English-only defense deck built from the latest locked thesis state.
- No thesis source was modified during this build.
- No experiments were rerun.
- No benchmark CSV, runtime CSV, or thesis figure/table values were changed.
- No demo logic was modified.

## Locked-State Verification

- Verified: Figure 1.1 uses ../../1.png
- Verified: Chapter 4 is the dispatch demo chapter
- Verified: Chapter 4 highlights five quantities
- Verified: Chapter 4 distinguishes Q_high from K
- Verified: Table 5.2 wording uses absolute percentage-point differences
- Verified: EuroSAT fine contract count is 6
- Verified: Appendix A includes formal input data
- Verified: Appendix A includes contract construction details
- Verified: Appendix A includes fresh output locations
- Verified: Appendix A includes non-git provenance boundary
- Verified: Contents page contains References and Appendix
- Verified: Latest thesis PDF detected (62 pages)

### Locked-state warning

- Prompt signature 8 is stale relative to the final teacher-request patch. The actual locked Contents page shows 'References' then 'Appendix' only.

## Source Files Used

- `LaTeX_Thesis2026/LaTeX_Thesis2026/main_Thesis_2026.pdf`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/chapter_1_Introduction.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/chapter_3_OSAG_Framework.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/chapter_4_Demo_System.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/chapter_5_Experiments_and_Discussion.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/appendix_a_reproducibility.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_contract_design_summary.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_paper_main_results.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_real_relative_gains.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_real_contract_ablation.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_runtime_summary.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_backbone_extension.tex`
- `LaTeX_Thesis2026/LaTeX_Thesis2026/tables/table_demo_results.tex`
- `results/tables/rerun_20260321_combined_main5/fresh_main_results.csv`
- `results/runtime/rerun_20260321_combined_main5/runtime_summary.csv`
- `osag_demo/visual_outputs/dispatch_policy_summary.csv`
- `reports/demo_reliability_sensitivity.md`
- `reports/thesis_lock_report.md`
- `reports/final_micro_patch_report.md`
- `reports/ultra_micro_patch_report.md`

## Slide-by-Slide Provenance

- Slide 1 (main): Title page / Figure 1.1
- Slide 2 (main): Chapter 1
- Slide 3 (main): Chapter 1
- Slide 4 (main): Chapter 1
- Slide 5 (main): Figure 1.1 / Chapter 1
- Slide 6 (main): Chapter 3
- Slide 7 (main): Chapter 5 / Appendix A
- Slide 8 (main): Table 5.1 / fresh_main_results.csv
- Slide 9 (main): Figure 5.1 / Table 5.2
- Slide 10 (main): Table 5.3 / Table 5.4 / Table 5.5
- Slide 11 (main): Chapter 4
- Slide 12 (main): Table 4.1 / Figure 4.2 / sensitivity audit
- Slide 13 (main): Chapter 4 / Chapter 5 / Appendix A
- Slide 14 (main): Appendix A
- Slide 15 (main): Chapters 1, 4, 5, Appendix A
- Slide 16 (main): Closing slide
- Slide 17 (backup): Chapter 3
- Slide 18 (backup): Chapter 5
- Slide 19 (backup): Appendix A
- Slide 20 (backup): Chapter 5
- Slide 21 (backup): Chapter 4 / sensitivity audit
- Slide 22 (backup): Appendix A

## Key Consistency Checks

- Figure 1.1 is taken from the final root-level `1.png` that is wired into the thesis.
- Chapter 4 content is the dispatch / emergency scheduling demo, not the deprecated synthetic-only narrative.
- The dashboard is described as highlighting five quantities.
- `Q_high` is kept distinct from the critical-capture term `K` everywhere in the deck.
- EuroSAT fine contract count is presented as 6 everywhere in the deck.
- Table 5.2 is described correctly as absolute percentage-point differences, not relative percentage changes.
- The HSI split limitation is stated correctly as pixel-stratified rather than spatial-blocked.
- Runtime wording avoids any claim that OSAG is intrinsically faster than Random.
- The deck states that the main benchmark uses a lightweight MLP to isolate governance effects.
- The deck states that the ResMLP study is a scoped robustness extension.
- The deck states that the dispatch demo supplements, but does not replace, the real benchmark.
- The deck states that reproducibility relies on scripts, manifests, configs, logs, and stage reports rather than a git commit ledger in the thesis workspace.

## Language and Rendering Audit

- All visible slide text is English only.
- Slide text was rendered into preview images before insertion into the PPTX to avoid font-substitution and glyph corruption.
- Fonts used for rendering are Windows Latin fonts (`Calibri` and `Cambria Bold`).
- No garbled characters, replacement glyphs, or question-mark placeholders were intentionally emitted.
- No AI-use disclosure or AI-trace wording appears in the deck, notes, or this audit.

## Timing Audit

- Main-deck slide count: 16
- Backup slide count: 6
- Total main-deck speaking time from notes: 15.25 minutes
- Result: suitable for an approximately 15-minute oral defense.

## Output Files

- PPTX: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en.pptx`
- PDF preview: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en.pdf`
- Notes: `C:\Users\Du\Downloads\gp\reports\osag_defense_deck_notes_en.md`
- Preview directory: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_preview`
- PDF page count: 22
- Preview image count: 22

## Remaining Risks

- The prompt's Contents-page signature mentioning `A Reproducibility and Artifact Guide` under the Contents page does not match the actual final locked thesis state after the teacher-request Appendix-heading patch. The deck follows the actual locked thesis.
- Because the deck is image-rendered for text safety, slide text is not individually editable inside PowerPoint. This was chosen deliberately to avoid glyph corruption and to keep the PDF preview identical to the slide previews.