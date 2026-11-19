# Lean→Python v0.37 — Original VerifyOS→LearnOS persisted typed source compatibility

## Scope and binding

This is a read-only comparison of the actual original VerifyStore and
LearnStore genesis/append-only ledger/snapshot records. Source is the
original **committed** VerifyOS final state; the receiver is the actual
**initial** LearnOS genesis. We separately validate the native **final**
LearnOS state and its future-only learning delta. No source reconstruction
or implicit direct skipping of the intermediate OS is permitted.

Canonical parent: `itakura-hidetoshi/KuuOS` main
`6672365b1bba5739d7fd1b30a250395647d46c89`,
v0.36 PR #3597 merged. Lean v4.30.0-rc2; pinned mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only, tighten-only, overwrite-forbidden, same-root.
Protected PR #1558 remains excluded. No original Lean/kernel/store source
is edited; only five new files are added. Docs/Python-only: Strict Lean
skipped intentionally.

## Exact original Lean conditions

`formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean`
imports `KUOS.VerifyOS.EvidenceBoundVerificationV0_1` and defines
conditions and theorems for the following *conditional* structures:

| Source formal structure | Bounded Python interpretation/check |
| --- | --- |
| `VerifySourceBinding` | Committed verification, recorded result, required learning, evidence/criterion/challenge/corroboration/adjudication and mission lineage bound |
| `EvidenceAbstractionBoundary` | Original evidence and counterevidence kept; uncertainty and source context remain visible; summaries do not replace sources |
| `LearningChallengeBoundary` | Competing explanations, anti-overgeneralization tests, distribution shift and negative transfer considered |
| `VerdictKindCompatibility` | PASSED→reinforcement/hold; FAILED→repair/hold; INDETERMINATE→reobservation/hold |
| `LearningDeltaBoundary` | Future-only, inactive now, replan required for activation, no memory overwrite, scope widening, present-cycle or past-history mutations |
| `TwoTruthsMiddleWayBoundary` | Conditional admissibility retains both usable candidate and non-reification; it does not turn a candidate into truth |
| `LearningDebtSemantics` | Committed learning debt discharged; replan debt remains; repair/reobservation candidate routes retain respective obligations |
| `LearnNonAuthority` | No truth, causal, execution, clinical, policy, self-modification or memory-overwrite authority |
| `LearnHistory` | Recovery and snapshot count equality is conditional on proof fields, not inherent in every external history |

Lean proves implications given their premises. Its proof terms have
not been compiled into or formally connected to Python.

## Actual native source comparison

1. Independently replay original VerifyStore and LearnStore
   genesis/ledger/snapshot through the existing original replay functions.
   Require immutable commit chain indices, digest links and exactly matching
   original snapshots; never call apply, repair, initialize or host.
2. Require the supplied VerifyOS and LearnOS states to equal their own
   replayed final states exactly.
3. Audit `audit_handoff("VerifyOS", "LearnOS", verify_final, learn_genesis)`.
   Compare the originally registered fields (lineage, mission contract,
   version, verification evidence, criterion, challenge, corroboration,
   adjudication, downstream debt identities) and preserve every field from
   receiver genesis through final history.
4. Reuse `audit_native_learn_from_verify(verify_final, learn_final)` to check
   the original learning-delta digest, original source identity, native
   future-only fields, non-activation and the preexisting v0.27 Lean-named
   data obligations. Do not promote its local result to a Lean theorem.
5. In addition to those existing checks, bind real Verify challenge
   counterevidence, its digest and unresolved conflict to both initial and
   final Learn state; check the original verdict→kind and gate→route
   compatibility, learning recorded/debt discharged, replan required,
   current/past unchanged and no activation.
6. Compare the six original store files' bytes before and after the audit,
   without pretending this establishes a globally atomic snapshot.

The only local positive result is
`SCOPED_VERIFY_LEARN_STORE_COMPATIBLE`. Missing original source stays
`NO_DATA`; incompatible/forged/corrupt source is `BLOCKED`.

## Newly added files only

- `runtime/kuuos_lean_python_verify_learn_store_compat_v0_37.py`
- `scripts/check_kuuos_lean_python_verify_learn_store_sources_v0_37.py`
- `tests/lean_python_extensions/test_verify_learn_store_compat_v0_37.py`
- `tests/lean_python_extensions/test_verify_learn_store_sources_v0_37.py`
- `docs/KUUOS_LEAN_PYTHON_VERIFY_LEARN_STORE_COMPAT_v0_37.md`

Fourteen original Lean/native/source-checker blobs are pinned by Git
blob digest on top of every inherited v0.36-and-earlier pin.
Runtime tests exercise the real full v1.3 native process, PASSED
reinforcement, FAILED repair, INDETERMINATE reobservation,
failed gate HOLD, counterevidence/conflict preservation, missing/corrupt/
symlinked source, no original writes and explicit non-authority.

## Independent certification and merger gate

Keep PR as Draft/OPEN/NO MERGE until the exact submitted head has
independent cumulative Python Runtime and full paginated Governance
completed/SUCCESS, exact submitted-head/test-merge Git tree equality,
and exact-head terminal SUCCESS. Strict Lean is intentionally skipped
only because the change does not alter formal Lean files.
Failure requires a repair **within the same PR**, inspecting entire
modified files, imported contracts, dependencies and root causes.

## Obstructions retained

- Verification/learning results do not authenticate external issuers or
  physical effects.
- ActOS jobs and slices numerical correspondence with Lean witness remains
  unproved.
- BeliefOS gerbe v0.3→v0.1 correspondence remains unproved.
- The entire Python interpreter vs Lean semantics, and global
  descent/gluing of these local interfaces, are unproved.
- An admissible candidate still has no present activation, execution,
  clinical, institutional, legal, Git, memory overwrite or self-modification
  authority.
