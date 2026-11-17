# KuuOS — Lean → Python runtime contract bridge v0.1

Source: [`itakura-hidetoshi/KuuOS`](https://github.com/itakura-hidetoshi/KuuOS),
main observed at `1a03908757fd0fcdb1acd5199b51dffd5208c3f8` (2026-11-17 JST).

## Scope and authority

This is an **append-only optional bridge**, not a rewrite of proven Lean or the
existing Python state machines. A Lean theorem proves its own exact statement
under its explicit structure hypotheses; a Python runtime contract check is
**not** a proof of Python/Lean semantic equivalence, an independent CI receipt,
a completed effect, truth authority, or permission to merge.

The bridge keeps independent slots for (1) source-pinned Lean declaration,
(2) existing Python implementation, (3) runtime-observed input, (4) pass,
block, or missing data, and (5) independent Lean/CI certification (not supplied
by this bridge). It never treats a model-generated description as evidence.

## Direct core OS coverage

| OS | Lean source | Runtime source | Primary projection |
| --- | --- | --- | --- |
| BeliefOS | `formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean` | `runtime/kuuos_belief_os_kernel_v0_1.py` | conditional transitions, truth/act boundary |
| DecisionOS | `formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean` | `runtime/kuuos_decision_os_kernel_v0_1.py` | no phase skips, decision ≠ execution |
| PlanOS | `formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean` | `runtime/kuuos_plan_os_kernel_v0_1.py` | DAG/phase progression, plan ≠ execution |
| ActOS | `formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean` | `runtime/kuuos_act_os_kernel_v0_1.py` | exact authorized state, no truth promotion |
| ObserveOS | `formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean` | `runtime/kuuos_observe_os_kernel_v0_1.py` | observation ≠ verification/truth |
| VerifyOS | `formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean` | `runtime/kuuos_verify_os_kernel_v0_1.py` | criterion/challenge and truth boundary |
| LearnOS | `formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean` | `runtime/kuuos_learn_os_kernel_v0_1.py` | future-only activation/no overwrite |

The bridge imports each core OS's **existing** state validator, reads its
`PHASES`, `NON_AUTHORITY_FLAGS`, and `REQUIRED_BOUNDARY`, and does not weaken
those checks. `audit_core_state` requires the original validator to return no
issues. `audit_core_transition` independently checks the append-only one-event
transition projection. Use **both** to validate a complete transition; neither
creates host authority or executes the event. Actual source-level source-of-truth
checks still reside in the original runtime modules.

### Additional limited projections

- **MemoryOS**: `OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean`
  and existing `runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py`.
  `memory_blocker_boundary_check` only checks a named boundary projection:
  memory cannot discharge blocker, forge missing evidence, or rewrite WORLD.
- **CodeAI**: `CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean`
  and its existing Python selection implementation.
  `codeai_candidate_eligible` mirrors Lean's strict `Eligible` predicate;
  even a high score cannot override inadmissible/incomplete evidence.
  `codeai_selection_boundary_check` confirms receipt no-effect flags, but
  does not decide whether external evidence is valid.
- **WORLD**: source and Python linkage registered only; full dependent
  source/receipt checks remain with the original WORLD kernel. **NO_DATA** for
  any unimplemented Python runtime equivalence claim.

## Example (read-only)

```python
from runtime.kuuos_lean_python_contract_bridge_v0_1 import (
    audit_core_state, audit_core_transition,
)

state_result = audit_core_state("DecisionOS", existing_state)
transition_result = audit_core_transition(
    "DecisionOS", existing_state, existing_event, existing_apply_result
)
# Inspect .status/.issues. A PASS is advisory evidence, never permission.
```

## Validation levels

- `RUNTIME_CHECK_PASSED`: exactly the Python checks performed on provided payload
- `BLOCKED`: a contradiction, malformed state, or violated invariant observed
- `NO_DATA`: required payload, dependency, or specialized verification unavailable

A PASS is **not** Lean-certified Python. Before any merge or stronger claim,
check the exact upstream source SHA, source imports, Lean theorem hypotheses,
changed Python file, full regression tests and the independent CI workflow/job/
Lean-step receipt. The bridge does not run Strict Lean for Python-only edits.

## Checks

```
python3 -m unittest tests.test_kuuos_lean_python_contract_bridge_v0_1
python3 scripts/check_kuuos_lean_python_contract_bindings_v0_1.py
```

These tests and static linkage checks are **scoped Python/source checks**, not
Lean kernel checks, proof/axiom audit, or the independent push CI receipt.

## Limitations / next stage

The direct bridge covers seven core OS kernels and two specialized payload
projections. WORLD is linked only. Other OSs and the 4,000+ Python modules / all
retained Lean theorems are **not** automatically certified. Extend theorem-by-
theorem with typed input maps, premise verification, counterexample tests,
nonvacuity, independent CI, and if whole-Python proof is desired, a verified
Python semantics/Lean refinement theorem. Preserve append-only, tighten-only,
overwrite-forbidden, same-root throughout.
