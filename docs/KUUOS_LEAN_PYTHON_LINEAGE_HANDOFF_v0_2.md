# KuuOS — Lean→Python lineage handoff bridge v0.2

## Source and status

Target: `itakura-hidetoshi/KuuOS` canonical `main`, source pinned to `1a03908757fd0fcdb1acd5199b51dffd5208c3f8` in v0.1. This is an additive, optional Python read-only audit. Formal proof bodies, source OS kernels and their validators, public import roots, pinned Lean/mathlib, and protected PR #1558 are unchanged.

Status is **local contract tests only until exact-HEAD independent CI completes**. These Python checks do not prove Python correctness in Lean, do not execute host effects, and do not grant truth/verification/clinical/commit/Git authority. `RUNTIME_CHECK_PASSED` means the *observed Python objects* passed only the named runtime checks; `BLOCKED` preserves contradictions; `NO_DATA` preserves missing or unsupported inputs.

## Three exact handoff edges

| Source → target | Formal source and premises | Existing Python state constructor | Checked typed binding |
| --- | --- | --- | --- |
| ActOS → ObserveOS | `ObserveOS/EffectGroundedObservationV0_1.lean`: `observation_requires_committed_effect`, `observation_preserves_effect_identity` | `build_initial_observe_state` | committed effect, ready/relevant source validators, act ID/digest/version, host receipt + invocation, selected step, operation, criterion, mission context |
| ObserveOS → VerifyOS | `VerifyOS/EvidenceBoundVerificationV0_1.lean`: `verification_requires_committed_observation`, `verification_preserves_observation_identity` | `build_initial_verify_state` | committed observation, verification debt, comparison/evidence/quality digests, original ActOS lineage and mission |
| VerifyOS → LearnOS | `LearnOS/FutureOnlyEvidenceLearningV0_1.lean`: `learning_requires_committed_verification`, `learning_preserves_verification_lineage` | `build_initial_learn_state` | completed verification, learning debt, criterion/challenge/corroboration/adjudication digests and future-only inactive delta |

All 3 edges require the unmodified source **and** target Python state validators to return no errors. The bridge audits *deep-copies*, rejects inconsistent provenance, stale binding and time regression, and checks fields in their existing constructors with an AST-based static checker. A passing receipt does not upgrade the authority of its inputs. The existing validators own receipt and state digest validation; no replacement/synthesis of evidence is performed by the bridge.

Direct DecisionOS → PlanOS is intentionally **NO_DATA**: the existing path is mediated by WaOS, and one must not invent a typed direct handoff without an independently justified source structure. WORLD, MemoryOS and CodeAI remain limited to v0.1 declared scopes until their specialized source structures have been mapped.

## Commands, test limitation and CI

```
python3 scripts/check_kuuos_lean_python_contract_bindings_v0_1.py
python3 -m unittest -v tests.test_kuuos_lean_python_contract_bridge_v0_1
python3 scripts/check_kuuos_lean_python_lineage_bindings_v0_2.py
python3 -m unittest -v tests.test_kuuos_lean_python_lineage_handoff_v0_2
```

The two test modules use isolated mock validators to check bridge **policy**, not complete original OS state schemas. They are additionally registered under the existing cumulative runtime validation root so the independent CI executes them on the real repository files. The static checker reads Lean declaration names, and verifies source and target field presence in the original Python constructors; it does not prove a semantic equivalence and does not run Strict Lean for Python-only changes.

## Further research / kept obstruction

Theorem-to-Python semantic refinement, full receipt/effect provenance soundness, and Decision→Wa→Plan connection remain unproved. Any future strengthening must preserve the original typed source, preconditions, pre/postconditions, counterevidence, source dependencies and proof root, rather than treating a named Lean theorem as a global Python theorem.
