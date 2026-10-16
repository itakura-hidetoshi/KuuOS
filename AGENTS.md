# KuuOS current formal architecture

The current mathematical foundation is `formal/Kuu/`, reached only through `formal/KuuOSFormal.lean` -> `KuuOSStrict`. The root Lake package exposes only these roots.

- Start from boundary-typed generating graphs, declared replacement relations and their universal quotient. Prove composition, units and strict interchange directly.
- Do not import `KUOS.*`, F51, F77, GrayGrade, GradedThreeCell, phase-reconstruction carriers or historical observation kernels into the current foundation, directly OR transitively.
- Do not solve this prohibition by renaming an old module, adding a phase factor, replacing physical geometry by a convenient proxy, or asserting a desired equation as an axiom.
- `legacy/v5.291/` is a separately reproducible snapshot. Existing `formal/KUOS/` files are historical compatibility mirrors, not the current build surface or theorem authority. A theorem proved there is not automatically a theorem of the new independent theory.
- Changing the current foundation requires `python3 scripts/check_kuu_foundation.py`, `python3 -m unittest discover -s tests -p test_kuu_foundation.py` and the pinned strict Lean build. Do not weaken these checks to restore legacy dependencies.
- Preserve Lean v4.30.0-rc2 and the committed mathlib manifest. PR #1558 remains validation-only, draft and unmerged.
- No `sorry`, `admit`, new axioms or `native_decide` in the independent core. Check `#print axioms` and exact-source-head CI before merge.
- Do not call the existing strict two-dimensional comparison calculus a completed proof-relevant global strict 3-category. That requires separately constructed 3-cells, boundaries, all compositions and coherence proofs.
- Copyright of KuuOS: Hidetoshi Itakura / 板倉英俊. Preserve existing license and attribution.
