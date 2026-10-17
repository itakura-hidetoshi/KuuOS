# KuuOS: independent foundation and retained public mathematics

The user's 2026-10-17 correction supersedes the blanket exclusion of old public roots in the 2026-10-16 migration design. Removing Gray as the basis of Kuu does NOT retire any other previously proved theorem.

- `formal/KuuOSStrict.lean` and `formal/Kuu/` are the independent core. Never introduce GrayGrade, GradedThreeCell, Gray/F51/F77 evaluation or phase-reconstruction dependencies into that core, directly or transitively.
- **Mathlib is welcome and encouraged** throughout existing and new Lean4 proofs, including `import Mathlib` and targeted `import Mathlib.*`. Favor focused imports for incremental build speed when convenient, but never prohibit the umbrella import or interpret it as a Gray dependency. Reuse mathlib category theory, bicategories, (∞-)category/simplicial tools, localization, homotopy, algebra and topology whenever mathematically appropriate.
- `formal/KuuOSFormal.lean` is the PUBLIC aggregate: independent Kuu plus the original aggregate imports. `lakefile.toml` publishes all 107 previous roots plus KuuOSStrict and Kuu. Do not replace this with a core-only package.
- `formal/KUOS/` and the retained public roots are live source and established mathematics, with their original stated assumptions. The KUOS namespace is NOT a Gray-dependency test. Check actual dependencies when changing the core.
- `legacy/v5.291` is an immutable reproducibility copy, not a demotion of the matching live proofs. Do not require the user to re-prove or revalidate existing results because of our build-wiring mistakes.
- Use `python3 scripts/check_public_proof_roots.py` and the existing configuration regressions to check OUR wiring changes. They do not reset proof acceptance. Keep independent-core and public-API checks separate.
- All ordinary retained consumers use the current repository package. Explicit `--legacy` remains only for intentionally reproducing a recorded snapshot. Preserve unrelated runtime permissions and evidence bindings.
- Do not infer old/new source-type equality from a restored import, and do not equate all raw proof histories. Scope every actual mathematical claim to its statement.
- Preserve Lean v4.30.0-rc2, the committed mathlib manifest, original theorem bodies and names, copyright and licenses. No sorry/admit/new axioms in new proofs. PR #1558 stays validation-only; #2339 remains separate.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
