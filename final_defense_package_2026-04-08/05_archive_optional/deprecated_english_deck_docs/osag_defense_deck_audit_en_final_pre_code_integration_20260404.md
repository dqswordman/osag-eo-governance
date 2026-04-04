# OSAG English Defense Deck Audit (Final Code-Integrated Version)

## Locked Thesis Verification

- Figure 1.1 uses ../../1.png
- Chapter 4 is the dispatch demo chapter
- Chapter 4 highlights five quantities
- Chapter 4 distinguishes Q_high from K
- Table 5.2 wording uses absolute percentage-point differences
- EuroSAT fine contract count is 6
- Appendix A includes formal input data
- Appendix A includes contract construction details
- Appendix A includes fresh output locations
- Appendix A includes non-git provenance boundary
- Contents page contains References and Appendix
- Latest thesis PDF detected (63 pages)

## Locked-State Warnings

- Prompt signature 8 is stale relative to the final teacher-request patch. The actual locked Contents page shows 'References' then 'Appendix' only.

## Deck Shape and Timing

- Total slide count: 28
- Main-deck slide count: 25
- Backup slide count: 3
- Estimated main-deck speaking time: 35.70 minutes
- Main deck alone fits the 28-33 minute requirement: no
- Live demo time is not counted in the estimate.

## Code-Integration Confirmation

- The official current deck includes code explanation in the main presentation, not only in backup slides.
- The code slides are based on the actual current codebase, especially reproduce_osag_real.py, run_all_real_experiments.py, dispatch_demo_core.py, run_dispatch_demo.py, and dispatch_demo_assets.py.
- The code slides show real function names, real entry points, and real output paths rather than invented pseudocode.

## Integrity Confirmation

- All key numbers remain thesis-consistent.
- EuroSAT fine contract count remains 6 everywhere in the deck.
- Table 5.2 is described as absolute percentage-point differences, not relative changes.
- The HSI split limitation is handled correctly as pixel-stratified rather than spatial-blocked.
- The official current Figure 1 is used consistently on the title slide and the methodology slide.
- No experiments were rerun.
- No numerical result changed.
- No thesis source was modified in this build step.
- No thesis claim changed.
- No AI wording or disclosure appears anywhere in the deck package.
- Slide-level source footnotes and clipped provenance labels are absent from the deck visuals.
- The deck remains English only.
- No garbled glyphs or replacement characters were introduced in the visible slide text.

## Slide-by-Slide Provenance

- Slide 1: `Title with Advisor Signature` <- Title page / final Figure 1.1
- Slide 2: `Talk Roadmap` <- presentation roadmap
- Slide 3: `Background and Motivation` <- Chapter 1
- Slide 4: `Research Gap and Guiding Questions` <- Chapter 1
- Slide 5: `Thesis Contributions` <- Chapter 1
- Slide 6: `Figure 1.1 Method Overview` <- Figure 1.1 / Chapter 1
- Slide 7: `Why Ordinary EO Training Is Service-Blind` <- Chapter 1 / Chapter 3
- Slide 8: `Core Concepts and Control Logic` <- Chapter 3
- Slide 9: `Benchmarks and Data Sources` <- Chapter 5 / Appendix A
- Slide 10: `Contract Construction and Target-Share Policy` <- Appendix A / Table 2.1
- Slide 11: `Repository and Code Architecture` <- actual codebase structure
- Slide 12: `Code View: Contracts and Target Service Shares` <- reproduce_osag_real.py / dispatch_demo_core.py
- Slide 13: `Code View: OSAG Sampler, Fairness, and Coverage Monitor` <- dispatch_demo_core.py / reproduce_osag_real.py
- Slide 14: `Code View: Benchmark and Demo Execution Path` <- entry scripts and output paths
- Slide 15: `Main HSI Benchmark Results` <- Table 5.1 / fresh rerun CSV
- Slide 16: `Main EuroSAT MSI Results` <- Table 5.1 / fresh rerun CSV
- Slide 17: `Why Accuracy Alone Is Not Enough` <- Figure 5.1 / Table 5.2
- Slide 18: `Contract-Design Ablation` <- Table 5.3 / Figure 5.4
- Slide 19: `Runtime and Backbone Robustness` <- Table 5.4 / Table 5.5
- Slide 20: `Why the Dispatch Demo Is Needed` <- Chapter 4
- Slide 21: `Dispatch Demo Setup and Scenario` <- Chapter 4
- Slide 22: `Dispatch Demo Results and Interpretation` <- Table 4.1 / Figure 4.2 / sensitivity note
- Slide 23: `Limitations and Claim Boundaries` <- Chapter 4 / Chapter 5 / Appendix A
- Slide 24: `Reproducibility and Public Release` <- Appendix A
- Slide 25: `Final Takeaways and Transition` <- closing summary
- Slide 26: `Backup: Where Is the Graph Really?` <- Chapter 3
- Slide 27: `Backup: HSI Split and Spatial Leakage Boundary` <- Chapter 5
- Slide 28: `Backup: Demo Metrics, Reliability, Q_high, and Sensitivity` <- Chapter 4 / sensitivity note

## Output Files

- PPTX: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_final.pptx`
- PDF: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_final.pdf`
- Preview directory: `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_final_preview`
- Notes: `C:\Users\Du\Downloads\gp\reports\osag_defense_deck_notes_en_final.md`
- Audit: `C:\Users\Du\Downloads\gp\reports\osag_defense_deck_audit_en_final.md`
- PPT slide count check: 28
- PDF page count check: 28
