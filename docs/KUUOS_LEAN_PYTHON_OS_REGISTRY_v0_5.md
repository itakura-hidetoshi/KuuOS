# KuuOS — Lean4証明と各OSのPython契約索引 v0.5

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 正本

- Repository: https://github.com/itakura-hidetoshi/KuuOS
- Canonical branch: main. This index was added after main commit 8346fe07075e3cf260ffb922a79d08b8e74e306d.
- Lean: v4.30.0-rc2; mathlib: 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
- Public formal root: formal/KuuOSFormal.lean. No second root is introduced.
- All actual theorem statements, definitions, universes, hypotheses and proofs remain in their original Lean source files. Source filenames and declaration names are identifiers, **not** a new proof of interpretation, runtime implementation, or Lean→Python refinement.
- Operational invariants: append-only / tighten-only / overwrite-forbidden / same-root. Protected PR #1558 remains separate.
- The index and its dispatcher are Python-only; docs or runtime contracts are **not** justification for rerunning Strict Lean or for making new mathematical claims.

## 構造化されたPython正本

The authoritative machine-readable entry is
[runtime/kuuos_lean_python_os_registry_v0_5.py](../runtime/kuuos_lean_python_os_registry_v0_5.py).

Its immutable OS_BINDINGS index is **derived** from the already-integrated v0.1
formal/runtime bindings and the v0.3 exact mediator mapping. It preserves their
original theorem names and runtime modules rather than copying abstract prose
into each OS kernel. The EDGES index is derived from the typed v0.2/v0.3
handoffs, with the v0.4 Plan→Act admission boundary. This is a selected
contract index, not a listing of all KuuOS Lean theorems.

| OS | Formal source | Existing Python kernel | Executable projection |
|---|---|---|---|
| ObserveOS | formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean | runtime/kuuos_observe_os_kernel_v0_1.py | original state validation; Act→Observe and Observe→Verify links |
| BeliefOS | formal/KUOS/BeliefOS/RelationalConditionalKernelV0_1.lean | runtime/kuuos_belief_os_kernel_v0_1.py | original phase/authority state validation |
| DecisionOS | formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean | runtime/kuuos_decision_os_kernel_v0_1.py | original state validation; no direct Plan shortcut |
| DecisionOSPlural | formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean | runtime/kuuos_decision_os_plural_kernel_v0_2.py | Decision→Plural edge only, not an invented full-state proof |
| DecisionOSWa | formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean | runtime/kuuos_decision_os_wa_kernel_v0_3.py | Plural→Wa edge only; veto/appeal history retained |
| PlanOS | formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean | runtime/kuuos_plan_os_kernel_v0_1.py | existing state/DAG validation; Wa→Plan and Plan→Act links |
| ActOS | formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean | runtime/kuuos_act_os_kernel_v0_1.py | original state/authority validation; admission is not invocation |
| VerifyOS | formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean | runtime/kuuos_verify_os_kernel_v0_1.py | original state; requires committed observation |
| LearnOS | formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean | runtime/kuuos_learn_os_kernel_v0_1.py | original state; learning inactive until replan |
| MemoryOS | formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean | runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py | blocker projection only; cannot release blocker or rewrite WORLD |
| CodeAI | formal/KUOS/CodeAI/EvidenceWeightedSelectionAbstentionV0_1.lean | runtime/kuuos_codeai_evidence_weighted_selection_abstention_v0_1.py | selection/evidence boundary only; score is not correctness or authority |
| WORLD | formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean | runtime/kuuos_authorized_atomic_world_commit_v0_34.py | source link only; standalone runtime proof status is NO_DATA |

## Typed edges — source constraints must not be skipped

1. DecisionOS → DecisionOSPlural → DecisionOSWa → PlanOS. Wa→Plan
   requires the original replan activation receipt.
2. PlanOS → ActOS requires the original PlanOS activation receipt and
   initial ActOS bind snapshot. It **does not** validate later execution or a
   host license.
3. ActOS → ObserveOS → VerifyOS → LearnOS requires the exact original
   source and target states, original validators, and preserved lineage.
4. DecisionOS → PlanOS directly, WORLD→anything and any unregistered edge
   are NO_DATA rather than assumed valid.

The module does not produce events, issue authorizations, invoke hosts,
mutate stores, automatically commit states, or change the original kernels.
A missing intermediate layer/receipt remains NO_DATA; a failed comparison is
BLOCKED (operational contradiction, **not** a theorem of impossibility).

## Read-only runtime usage

From the repository root (with existing runtime modules installed):

~~~python
from runtime.kuuos_lean_python_os_registry_v0_5 import (
    list_os, list_edges, get_os, audit_os, audit_edge,
)

print(list_os())           # the 12 selected named OS
print(list_edges())        # exactly seven typed handoffs
print(get_os("PlanOS"))    # original Lean / original Python identities

a = audit_os("PlanOS", observed_original_plan_state)
b = audit_edge(
    "PlanOS", "ActOS", observed_original_plan_state,
    observed_initial_act_state,
    activation_receipt=observed_original_plan_activation_receipt,
)
# a.status/b.status describe only executed Python checks on supplied snapshots.
# Neither successful result grants execution, truth or merge authority.
~~~

For direct v0.1-v0.4 APIs, their detailed condition/field specs and historical
source commits are preserved in existing documents:

- [v0.1 — Core OS, MemoryOS, CodeAI](KUUOS_LEAN_PYTHON_RUNTIME_CONTRACT_BRIDGE_v0_1.md)
- [v0.2 — Act/Observe/Verify/Learn lineage](KUUOS_LEAN_PYTHON_LINEAGE_HANDOFF_v0_2.md)
- [v0.3 — Decision/Plural/Wa/Plan](KUUOS_LEAN_PYTHON_DECISION_PLAN_HANDOFF_v0_3.md)
- [v0.4 — Plan activation / Act admission](KUUOS_LEAN_PYTHON_PLAN_ACT_ADMISSION_v0_4.md)

## Evidence and verification

Existing v0.1-v0.4 code was integrated in PRs
[#3563](https://github.com/itakura-hidetoshi/KuuOS/pull/3563),
[#3564](https://github.com/itakura-hidetoshi/KuuOS/pull/3564), and
[#3565](https://github.com/itakura-hidetoshi/KuuOS/pull/3565).
For v0.4, exact-source Governance
[#44069876836](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44069876836)
and independent post-merge Runtime Full Check
[#44071041584](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44071041584)
completed SUCCESS at main commit 8346fe07075e3cf260ffb922a79d08b8e74e306d.
The v0.5 evidence must be checked **separately** on its own exact source
and merge tree; historical green does not certify this change.

Check from the actual repository:

~~~sh
python3 scripts/check_kuuos_lean_python_os_registry_v0_5.py
python3 -m unittest -v tests.test_kuuos_lean_python_os_registry_v0_5
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
~~~

The static checker confirms only named Lean declarations, original Python
module paths, mediator edges, and retained cumulative registration.
It is **not** Lean elaboration, a full all-theorem audit, proof of Python's
semantic equivalence, or proof that an external receipt was actually issued.
No source being declared in this index can elevate an unverified claim.

## Explicitly unresolved

- A formal Lean refinement proof for these Python functions.
- Cryptographic authenticity of externally provided original phase receipts.
- Comprehensive coverage of all formal/KUOS proofs and each specialized OS.
- Full execution authority, effect verification, institutional/clinical claims.
- World-wide gluing/descent conditions not already established by specific Lean
  theorems and typed context witness.
