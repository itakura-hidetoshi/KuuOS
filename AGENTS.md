# KuuOS: independent foundation and retained public mathematics

The user's 2026-10-17 correction supersedes the blanket exclusion of old public roots in the 2026-10-16 migration design. Removing Gray as the basis of Kuu does NOT retire any other previously proved theorem.

- There is **one canonical public formal entry**, `formal/KuuOSFormal.lean`. `formal/Kuu/` is part of that same theorem library. `formal/KuuOSStrict.lean` remains an INTERNAL import aggregate for source/CI compatibility, not another theorem authority or public Lake root. Check real transitive dependencies, never require GrayGrade, GradedThreeCell, Gray/F51/F77 evaluation or phase-reconstruction to define Kuu.
- **Mathlib is welcome and encouraged** throughout existing and new Lean4 proofs, including `import Mathlib` and targeted `import Mathlib.CategoryTheory.Quotient` (and other named submodules). Favor focused imports for incremental build speed when convenient, but never prohibit the umbrella import or interpret it as a Gray dependency. Reuse mathlib category theory, bicategories, (∞-)category/simplicial tools, localization, homotopy, algebra and topology whenever mathematically appropriate.
- `formal/KuuOSFormal.lean` is the PUBLIC aggregate: all existing proven modules plus the new Kuu modules. `lakefile.toml` retains the 107 previous public roots, without publishing KuuOSStrict or Kuu as additional standalone roots. `lake build` and `lake build KuuOSFormal` are the same canonical build. Targeted compilation of an internal module is merely a build optimization.
- `formal/KUOS/` and the retained public roots are live source and established mathematics, with their original stated assumptions. The KUOS namespace is NOT a Gray-dependency test. Check actual dependencies when changing the core.
- `legacy/v5.291` is an immutable reproducibility copy, not a demotion of the matching live proofs. Do not require the user to re-prove or revalidate existing results because of our build-wiring mistakes.
- Use `python3 scripts/check_public_proof_roots.py` and existing regressions to check OUR wiring changes. They do not reset proof acceptance. A focused dependency scan is an engineering check inside the same unified theorem library, never a distinct mathematical authority.
- All ordinary retained consumers use the current repository package. Explicit `--legacy` remains only for intentionally reproducing a recorded snapshot. Preserve unrelated runtime permissions and evidence bindings.
- Do not infer old/new source-type equality from a restored import, and do not equate all raw proof histories. Scope every actual mathematical claim to its statement.
- Preserve Lean v4.30.0-rc2, the committed mathlib manifest, original theorem bodies and names, copyright and licenses. No sorry/admit/new axioms in new proofs. PR #1558 stays validation-only; #2339 remains separate.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Mandatory research prior-proof recall (2026-11-24, additive)

Before suggesting or generating any new mathematical research candidate, use
GitHub MCP to reobserve canonical main, recall prior workbench/MemoryOS records,
and search existing Lean sources across **all** relevant families (including
KUOS/Architecture, Kuu/F112, GK5, and previous proof/obstruction stages). Read
the actual signatures, assumptions, definitions, imports and proof history.
Do not treat a new name, a finite carrier adapter or a successful CI as
mathematical novelty. Existing proofs are to be reused, not reproved.

Use the versioned prior-proof recall gate documented in
`docs/KUUOS_CODEAI_PRIOR_PROOF_RECALL_GATE_v0_1.md` before provider/candidate
generation. On a materialized exact canonical source, record its retrieval
receipt and review for each proposed proposition; in MCP-only sessions, collect
the corresponding exact source/blob/signature comparisons via MCP and record
them, without claiming the local scanner ran. Search misses, stale evidence,
unresolved comparisons or missing history must not be promoted to novelty.
Retain the separate statuses REUSE_EXISTING, necessary typed bridge (not a
new mathematical result), reviewed unproved delta, and HOLD/NO_DATA. Only a
documented residual obligation or necessary bridge may proceed to CodeAI
candidate generation; then direct Lean, real Lean MCP and independent CI
remain distinct. Do not modify historical theorem bodies or proof pins.

Use the research-specific `build_research_structured_edit_synthesis` entry in
`runtime/kuuos_codeai_research_structured_edit_synthesis_v0_1.py` for new
mathematical provider proposals, not the ungated generic software synthesis
entry. It consumes the fresh reviewed recall receipt and verifies the prior
source texts in the actual provider context before calling the original
CodeAI kernel. Do not use an old research replay to bypass this gate.

## Subject-first prior-proof recall v0.2 (additive)

For C60/Qi/GK5/F112 mathematical research, start from the research subject,
not from remembered declaration names. Use the source-anchored catalog
`memoryos/research_prior_proof_subject_index_v0_2.json` and
`runtime/kuuos_codeai_prior_proof_subject_gate_v0_2.py` (or the equivalent
exact-source GitHub MCP procedure). Compare each retrieved declaration,
including existing negative/obstruction results, before proposing a new
result. The subject gate adds to, not replaces, v0.1 and ordinary repair
memory. An unknown topic is NO_DATA, not mathematical novelty. A stale
anchor requires source re-observation, not automatic re-proving.
See `docs/KUUOS_CODEAI_PRIOR_PROOF_SUBJECT_RECALL_v0_2.md`.

## Whole-library prior-proof recall v0.3 (additive)

Before new mathematical research, supplement the curated subject catalog with
exact-tree-bound repository-wide recall described in
`docs/KUUOS_CODEAI_PRIOR_PROOF_LIBRARY_INDEX_v0_3.md`.
The automatic lexical catalog must be tied to the current GitHub-observed
source tree; search by research concepts, not only remembered declaration
names. Review all retrieved declarations and preserve parser gaps. New
mathematical provider proposals use `build_library_research_synthesis` in
`runtime/kuuos_codeai_prior_proof_library_index_v0_3.py` in addition to the
existing v0.1/v0.2 gates. An MCP-only session must conduct equivalent broad
source retrieval and comparison without claiming this scanner executed.
Neither lexical previews nor module-import candidates replace actual Lean
elaboration, proof history or mathematical comparison. Search miss or
truncation is NO_DATA/HOLD; no automatic novelty or authority.

## Selected historical kernel memory review v0.4 (additive)

When preparing a new mathematical research candidate, use the v0.4
`recall_kernel_memory` entry and `build_kernel_memory_research_synthesis`
in the kernel-memory/research-gate modules before the existing v0.3/v0.2/v0.1
gates. Review matching actual historical Lean type and direct proof-reference
observations, bind the exact observation digest and comparison, and include
the read-only context from `kernel_context_text` in the provider request.
Keep all unobserved hits explicit; do not claim their kernel certification.
A changed source/dependency scope requires re-observation. Existing review,
provider, direct Lean, real Lean MCP, independent CI, and authority boundaries
remain unchanged. No mathematical novelty follows from a memory hit or miss.
An MCP-only session can reproduce these exact-source comparisons without
claiming it executed the runtime.

## Combined historical kernel memory review v0.5 (additive)

For new mathematical research, use the v0.5 `recall_kernel_memory`
and `build_kernel_memory_research_synthesis` entry points in
`runtime/kuuos_codeai_prior_proof_kernel_memory_v0_5.py` and
`runtime/kuuos_codeai_prior_proof_kernel_research_gate_v0_5.py`.
The combined lookup preserves the separately certified v0.4 and v0.5
packets without rewriting either; the v0.3/v0.2/v0.1 gates remain.
Review the exact elaborated types, assumptions, conclusions, reported
axioms and direct proof references of every match, and acknowledge all
unobserved hits. Scope drift, stale or truncated recall, incomplete
comparison and duplicate NEW requests must hold. Reviewable residual
obligations may proceed only through existing CodeAI and verification
gates. Direct references are not the transitive dependency closure.
Neither a match nor a miss certifies novelty or authority. See
`docs/CodeAI/PRIOR_PROOF_KERNEL_MEMORY_v0_5.md`. The deterministic provider replay is a synthetic
scope/review fixture only, not an external model call or proof.
