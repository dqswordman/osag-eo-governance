# OSAG Current English Defense Deck Audit

## Build Scope

- This deck is the official current short English defense deck.
- It realigns the previous long code-integrated deck to the new 15-20 minute presentation requirement.
- The long 25-32 minute / code-integrated deck is no longer presented as the current version.
- The current short deck remains thesis-consistent and English only.
- No thesis source was modified.
- No experiments were rerun.
- No benchmark CSV, runtime CSV, demo logic, or numerical result was changed.

## Locked-Thesis Verification

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
- Verified: Latest thesis PDF detected (61 pages)

## Locked-State Warnings

- Prompt signature 8 is stale relative to the final teacher-request patch. The actual locked Contents page shows 'References' then 'Appendix' only.

## Slide Inventory

- Total slide count: 20
- Main-deck slide count: 17
- Backup slide count: 3
- Estimated main-deck speaking time: 17.30 minutes
- Main-deck timing inside 15-20 minutes: yes
- Live demo time is not counted in the estimate.

## Slide-by-Slide Provenance

- Slide 1 (main): locked thesis title / Figure 1.1 master asset
- Slide 2 (main): presentation structure
- Slide 3 (main): Chapter 1
- Slide 4 (main): Chapter 1
- Slide 5 (main): Figure 1.1 / Chapter 1
- Slide 6 (main): Chapter 3
- Slide 7 (main): Chapter 5 / Appendix A
- Slide 8 (main): Table 5.1 / fresh_main_results.csv
- Slide 9 (main): Table 5.1 / fresh_main_results.csv
- Slide 10 (main): Figure 5.1 / Table 5.2
- Slide 11 (main): Table 5.3 / Table 5.4 / Table 5.5
- Slide 12 (main): Chapter 4
- Slide 13 (main): Table 4.1 / Figure 4.2 / sensitivity audit
- Slide 14 (main): current codebase structure
- Slide 15 (main): Chapter 4 / Chapter 5 / Appendix A
- Slide 16 (main): Appendix A
- Slide 17 (main): closing synthesis
- Slide 18 (backup): Chapter 3
- Slide 19 (backup): Chapter 5
- Slide 20 (backup): Chapter 4 / sensitivity audit

## Consistency Checks

- EuroSAT fine contract count is 6 everywhere.
- Table 5.2 is described as absolute percentage-point differences, not relative percentage changes.
- Chapter 4 demo terminology stays aligned with the dispatch / emergency scheduling version.
- `Q_high` is treated as distinct from the critical-capture term `K`.
- The HSI split limitation is stated correctly as pixel-stratified rather than spatial-blocked.
- The runtime discussion is limited to comparable overhead and does not claim that OSAG is faster than Random.
- The current deck includes one concise code-architecture slide in the main presentation.
- Detailed code walkthrough and live-demo materials still exist for the later defense stage.

## Language and Rendering Audit

- All visible slide text is English only.
- Slides are rendered as images before insertion into the PPTX to avoid font substitution and garbled glyphs.
- No slide-level source footnotes or clipped provenance labels were used.
- No AI wording or AI-use disclosure appears in the deck, notes, or audit.

## Output Files

- PPTX: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_current.pptx`
- PDF: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_current.pdf`
- Preview directory: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_current_preview`
- Notes: `C:\Users\Du\Downloads\gp\reports\osag_defense_deck_notes_en_current.md`
- Bilingual script: `C:\Users\Du\Downloads\gp\reports\defense_script_bilingual_slide_by_slide_current.md`
- PDF page count: 20
- Preview image count: 20

## Remaining Risks

- The demo still uses a hand-set reliability score, so the slide explains the sensitivity boundary rather than overclaiming objectivity.
- The HSI split remains pixel-stratified; this is acknowledged explicitly rather than hidden.