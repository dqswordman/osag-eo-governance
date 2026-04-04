# Figure 1 Replacement Report

- Old figure file replaced: the previous master Figure 1 asset at `C:\Users\Du\Downloads\gp\1.png` was replaced in place by the newly approved figure.
- Thesis usage:
  - `C:\Users\Du\Downloads\gp\LaTeX_Thesis2026\LaTeX_Thesis2026\chapter_1_Introduction.tex` still points Figure 1.1 to `../../1.png`.
  - The rebuilt thesis PDF at `C:\Users\Du\Downloads\gp\LaTeX_Thesis2026\LaTeX_Thesis2026\main_Thesis_2026.pdf` now compiles with that updated `1.png`.
- English defense deck usage:
  - `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en.pptx` and `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en.pdf` were rebuilt.
  - `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_25to32min.pptx` and `C:\Users\Du\Downloads\gp\deliverables\osag_defense_deck_en_25to32min.pdf` were rebuilt.
  - In both English deck build paths, the methodology slide uses the full master figure from `C:\Users\Du\Downloads\gp\1.png`.
  - In both English deck build paths, the title slide uses a cropped supporting visual derived from the same `C:\Users\Du\Downloads\gp\1.png`, with the crop now computed from the new figure dimensions rather than the old fixed pixel box.
- Older Figure 1 visibility:
  - No older Figure 1 asset remains visibly in use in the rebuilt thesis PDF or the rebuilt English deck outputs.
  - The current visible Figure 1 path for thesis and deck generation is the root-level `C:\Users\Du\Downloads\gp\1.png`.
- Visibility confirmation:
  - No thesis wording changed.
  - No numerical results changed.
  - No benchmark claims changed.
  - No experiments were rerun.
