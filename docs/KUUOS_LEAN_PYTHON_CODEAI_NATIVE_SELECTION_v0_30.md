# KuuOS Lean→Python v0.30 — original CodeAI candidate selection source binding

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Stage gate and canonical provenance

This branch is deliberately **staged without a new PR** while v0.29
Belief→Decision→Plural→Wa is awaiting its independent terminal CI and
main integration. The canonical v0.29 merged main SHA is
`7a7c6412858710c344a6bd26613e687cbe6fa9aa`.
Its previously certified source SHA was
`52691b7a98a289dc154950dfef097bef7ecb4fb4`.

Lean: v4.30.0-rc2; mathlib:
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.
Protected PR #1558 stays unmerged.

Original goal: translate already-proved Lean data obligations
into **actual Python OS modules** whose inputs come from KuuOS
native source states/receipts, not arbitrary dictionaries or renamed
concepts. In this stage the target is CodeAI.

## Lean scope

Source:
`formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean`

Lean distinguishes `SourceClassification.admissible` from
`repairable`, `hold`, `rejected`, and distinguishes
`EvidenceStatus.allPassed` from incomplete/failed evidence.
The source proves that neither a high score nor incomplete evidence
can bypass eligibility, and proves conditional consequences of a
`Receipt.WellFormed` source.

An original Python CodeAI scorecard uses different strings:
`candidate_static_admissibility_confirmed`,
`candidate_static_preflight_repair_required`,
`candidate_static_preflight_held`, and
`candidate_static_preflight_rejected`. These are **explicitly**
mapped to the four Lean classification names; they are not assumed
type-identical.

All-passed evidence is inferred only when the original independent
candidate obligation counts are exhaustive and all passed, with no
failed/inconclusive/skipped obligations. The independent native
selector's eligibility flag must agree exactly with the stricter
classification-and-evidence gate, **not** a floating or Bayesian
interpretation of its numerical evidence score.

## Original native Python construction

New module:
`runtime/kuuos_lean_python_codeai_native_selection_v0_30.py`

Requires five genuine original source packets:
`strengthening_plan`, `strengthening_receipt`,
`evidence_packet`, `selection_request`, `selection_policy`.

Requires separately supplied ORIGINAL recorded decision and receipt;
missing output stays `NO_DATA`. Source data are strict built-in JSON,
not dynamic objects with arbitrary serialization hooks.

The module invokes the **unchanged** original
`build_codeai_evidence_weighted_selection_abstention` with
the exact provided source packets, requiring all its native
source-lineage, evidence coverage, independent-runner metadata and
selection-policy validation to pass. Recomputed deterministic
decision and receipt must byte-semantically agree with the observed
sealed outputs. Altering an output without resealing is BLOCKED;
locally consistent hashes do not authenticate an external issuer.

For every candidate:
- original source-classification matches its original plan entry;
- counts of passed/failed/inconclusive/skipped source obligations are
  exhaustive; scores are nonnegative and bounded by their maximum;
- the native eligible flag agrees with admissible + allPassed,
  regardless of raw score.

For the **actual selected candidate only**, those original source
values are projected to the existing
`kuuos_lean_python_codeai_obligations_v0_27.audit_witness`.
Do not falsely label every nonselected candidate an "abstained" global
decision. For a true global abstention, no selected-candidate theorem
witness is claimed.

The original CodeAI receipt's non-effect boundary is independently
checked with `codeai_selection_boundary_check`. No host effects,
repair, repository mutation, Git authority, truth claim, or
correctness-as-probability is permitted.

## Concrete regression and source pins

The new tests use the existing
`tests/test_kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py`
fixture builder and original independent-evidence/selector implementation.
They cover selected, high-score but inadmissible, no eligible,
threshold abstention, input/receipt drift, caller mutation prevention,
missing source, and no authority escalation.

An independent source checker inherits all v0.29 previous-source
pins, then exact-pins ten original CodeAI and Lean files (plus the
v0.29 source checker), verifies named original theorem declarations,
and checks the new Python module and new tests' AST inventories.

The independent CI for v0.30 is **not certified** until this staging
branch is reconciled to the exact main descendant of formally
certified v0.29, and the actual PR's full Runtime and Governance
workflows reach terminal success.

## Remaining obstructions

Even a passing original deterministic Python selector does not mean
external independent runner/reviewer attestations are cryptographically
authentic. The source packet *reports* independence; a Python
data check alone does not prove its external origin.

The Python program does NOT construct Lean proof fields, prove a
general Lean↔CPython refinement, or establish that the source category
strings are definitionally identical to the Lean inductive types.
Scores are not probabilities, correctness proofs, truth authority
or permission for new CodeAI actions.

MemoryOS and WORLD retain their separate original-source,
independent proof/data correspondence as further tasks. Do not
promote the v0.30 CodeAI local result to their authority scope.
