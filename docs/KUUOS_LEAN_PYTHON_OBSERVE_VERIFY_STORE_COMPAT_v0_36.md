# Lean→Python v0.36 — Original ObserveOS→VerifyOS persisted typed source compatibility

**Scope:** bounded, read-only comparison of real original ObserveStore and
VerifyStore genesis/append-only ledger/snapshot records. The source is the
committed original ObserveOS final state; the receiver's initial VerifyOS
genesis must preserve that exact typed source. The original VerifyOS final
state is then independently replayed and checked for evidence adjudication,
verification debt and non-authority.

## Source and canonical constraints

- Repository: `itakura-hidetoshi/KuuOS`; canonical branch `main`.
- Parent: `269648c480cffd8f35d7cccdd0feaacf6ffb1e07`
  (merged v0.35, PR #3596).
- Lean v4.30.0-rc2; mathlib
  `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
- Append-only / tighten-only / overwrite-forbidden / same-root.
- No changes to original OS kernels, native stores, source Lean files,
  prior checks, source fixtures or protected PR #1558.
- Python/doc-only stage: do not run unnecessary Strict Lean.

## Exact original Lean conditions

`formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean` provides:

| Structure | Local condition represented |
| --- | --- |
| `SourceObservationBinding` | Committed, recorded ObserveOS state, verification required, preserved source effect, canonical comparison receipt, evidence and quality digests |
| `CriterionBinding` | Criterion/method/success/failure/falsification/evidence requirements fixed before adjudication; no causal permission |
| `ChallengeRequirements` | Falsification attempt, independent assessors and receipts, preserved counterevidence, disclosed conflict |
| `CorroborationSurface` | Admissibility entails sufficient evidence, no unresolved conflict and discharged observation debt |
| `AdjudicationBoundary` | PASSED requires matched/admissible/satisfied/unfalsified; FAILED requires conclusive failure basis; INDETERMINATE is non-conclusive |
| `VerificationDebtSemantics` | PASSED and FAILED discharge verification debt (FAILED requires corrective action); INDETERMINATE retains verification and reobservation obligations; learning always required |
| `VerifyNonAuthority` | No truth, causal, execution, clinical, legal or other authority promotion |
| `VerifyHistory` | Recovery and snapshot count equations are premises, not automatic properties of arbitrary external histories |

The original Lean proofs establish implications under their typed premises;
they do **not** certify this Python implementation or any external issuer.

## Original Python state correspondence

1. Read and replay `ObserveStore`'s genesis, ledger and snapshot through
   original `_recover_unlocked`, verifying the original event, chain and
   snapshot invariants. Do the same independently for `VerifyStore`.
2. Match both user-supplied committed native states exactly to their
   individually replayed final records. Missing paths or uncommitted
   histories produce `NO_DATA`; malformed or contradictory sources
   produce `BLOCKED`.
3. Check `audit_handoff("ObserveOS", "VerifyOS", observe_final, verify_genesis)`
   using the pre-existing registered contract. Bind source identity,
   lineage, criterion, comparison receipt, host receipt, evidence,
   quality report and observation debt **at receiver genesis**.
4. Check the existing `audit_native_verify_from_observe(observe_final,
   verify_final)` which validates the original native states/edge, the
   criterion-conditioned adjudication receipts, final verdict and
   verification debt projection against the existing v0.27 Python
   Lean-premise checker.
5. For every registered source→target field, additionally verify
   `ObserveOS final == VerifyOS genesis == VerifyOS final`.
   Check that neither store's source bytes changed during the audit.
   The stores are distinct and this is **not** a globally atomic snapshot.

A successful result is only `SCOPED_OBSERVE_VERIFY_STORE_COMPATIBLE`.
It never asserts the independent correctness of a host effect, a real-world
fact, an issuer signature, a universal Lean→Python refinement or global
descent/gluing. Verification is not truth, causality or permission to execute.

## New files (only)

- `runtime/kuuos_lean_python_observe_verify_store_compat_v0_36.py`
- `scripts/check_kuuos_lean_python_observe_verify_store_sources_v0_36.py`
- `tests/lean_python_extensions/test_observe_verify_store_compat_v0_36.py`
- `tests/lean_python_extensions/test_observe_verify_store_sources_v0_36.py`
- `docs/KUUOS_LEAN_PYTHON_OBSERVE_VERIFY_STORE_COMPAT_v0_36.md`

All v0.35-and-earlier source integrity rules are inherited. Eleven
additional original Lean/native/source checker blobs are pinned exactly.
Regression tests exercise a full original v1.3 source flow, admissible
PASSED, failed corrective action, indeterminate verification debt,
missing/altered sources, genuine `pathlib.Path`, string paths, malicious
custom paths, symlinks, ledger/snapshot corruption, and unchanged
persisted bytes.

## Merge gate

Keep this PR Draft, OPEN and **not merged** until its exact HEAD has
independent cumulative Python Runtime + Governance success, every paginated
job accounted for, original source pins, test-merge Git tree match, and
exact-head terminal SUCCESS. On failure, fix the same PR after inspecting
the entire changed source, its dependent contracts and the structural
cause, then certify the new exact HEAD.

## Open obstructions retained

- External issuer authenticity and real host execution are not proved.
- ActOS numerical jobs/slices vs Lean witnesses remain unproved.
- The v0.3 BeliefOS gerbe to v0.1 formal correspondence remains unproved.
- Python interpreter/Lean semantic refinement and all-volume/global
  descent or gluing remain unproved.
- No verification receipt is truth, clinical/legal authority or a host
  execution license; the adapter does not change the original stores.
