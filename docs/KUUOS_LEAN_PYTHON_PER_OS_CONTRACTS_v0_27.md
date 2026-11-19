# KuuOS Lean→Python v0.27 — Per-OS proof-obligation code (return to original research aim)

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical source and scope

Repository: `itakura-hidetoshi/KuuOS`. Initial base: canonical `main`
`c25f03b8ecc33df82c8ef678243cc66f0ecec90b` (Wa v0.26 already merged).
Lean v4.30.0-rc2, mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root. Protected
PR #1558 remains untouched.

**Purpose:** move beyond repeated Wa arithmetic releases. Preserve the
original existing KuuOS Lean statements as the source of obligation
definitions, then implement their *selected observable data conditions*
in distinct importable Python modules next to the existing OS runtime.

**Not a proof translation.** Lean's proof fields and dependent types
cannot be reconstructed by checking Python Boolean/dictionary payloads.
A `LOCAL_CONDITIONS_CHECKED` response certifies only the stated
Python **input data checks** under the explicitly named source.
It never means the Python program implements Lean semantics in general.

No original Lean theorem file, original Python kernel, state validator,
store, ledger, source registry, CI entrypoint or mission authority is
changed by this stage. A new optional common verifier and distinct
per-OS modules are additive. Original core validators remain authoritative
for local runtime state acceptance.

## Specific Python modules by OS

Each module exports `OS_NAME`, `LEAN_FILE`, `THEOREMS`, `FIELDS`,
`audit_witness(witness)`, and `audit_native_state(state)`. Each
theorem is grounded by an exact pinned Lean source blob and declaration
name; the static checker rejects missing or changed source files.

| OS | Python module | Selected Lean-structure obligations |
|---|---|---|
| BeliefOS | `runtime/kuuos_lean_python_belief_obligations_v0_27.py` | counterevidence count append-only; future-only belief commit; no memory overwrite; replan required |
| DecisionOS | `runtime/kuuos_lean_python_decision_obligations_v0_27.py` | admissibility gate; prohibited/authority claims excluded; future-only decision without execution/overwrite |
| PlanOS | `runtime/kuuos_lean_python_plan_obligations_v0_27.py` | each *effectful* step requires rollback or human review plus external license, stop condition and checkpoint |
| ActOS | `runtime/kuuos_lean_python_act_obligations_v0_27.py` | all five typed invocation bindings; single-use authorization; at most one claimed job and one slice |
| ObserveOS | `runtime/kuuos_lean_python_observe_obligations_v0_27.py` | committed effect/canonical receipt; comparison not verification; matched/divergent vs inconclusive/conflicted observation debts |
| VerifyOS | `runtime/kuuos_lean_python_verify_obligations_v0_27.py` | matched admissible evidence/criterion on pass; conclusive failure basis; indeterminate debts; every verdict requires learning |
| LearnOS | `runtime/kuuos_lean_python_learn_obligations_v0_27.py` | future-only learning; replan before activation; no current/past change, overwrite or invariant removal |
| MemoryOS | `runtime/kuuos_lean_python_memory_obligations_v0_27.py` | blockers retained as context, not silently released; read-only WORLD candidate boundary |
| CodeAI | `runtime/kuuos_lean_python_codeai_obligations_v0_27.py` | high score cannot bypass source admissibility and all-passed evidence; abstention is not rejection; score is not proof |
| DecisionOSPlural | `runtime/kuuos_lean_python_decision_plural_obligations_v0_27.py` | mission/stakeholder/evidence validation before protective veto; raw veto grants no authority |
| DecisionOSWa | `runtime/kuuos_lean_python_decision_wa_obligations_v0_27.py` | excludes confirmed false harmony; preserves minorities/dissent/source plurality identity |
| WORLD | `runtime/kuuos_lean_python_world_obligations_v0_27.py` | only caller-declared atomic/root/append-only and local authorization conditions; existing independent WORLD state equivalence remains NO_DATA |

The precise Lean theorem declaration inventory is in each Python module's
`THEOREMS`. The theorem-name list is **not** a proof that every field
of the whole original Lean structure was checked; it specifies the
*selected observable consequence* being projected. In particular
the MemoryOS nested Qi/WORLD boundary, CodeAI Receipt.WellFormed and
WORLD's full typed commit protocol contain additional preconditions
not constructed by this adapter.

### Typed handoffs stay distinct

`DecisionOSPlural.audit_native_edge(...)` delegates to the existing
`DecisionOS→DecisionOSPlural` audit.
`DecisionOSWa.audit_native_edge(...)` delegates to
`DecisionOSPlural→DecisionOSWa`. These checks do not authorize a direct
`DecisionOS→PlanOS` shortcut. The existing Wa→Plan receipt requirement,
Plan→Act activation receipt, and Act→Observe→Verify→Learn lineage checks
remain under `kuuos_lean_python_os_registry_v0_5.py`.

## How to use a per-OS executable data contract

```python
from runtime.kuuos_lean_python_plan_obligations_v0_27 import (
    audit_witness, audit_native_state,
)

# This verifies selected data obligations corresponding to Lean's
# PlanOS.EffectGuard; it is NOT a proof of an original source event.
sample = {
    "effectful": True,
    "rollbackPresent": False,
    "humanReviewRequired": True,
    "externalLicenseRequired": True,
    "stopConditionPresent": True,
    "checkpointPresent": True,
    "planIsExecution": False,
}
observed = audit_witness(sample)
assert observed.status == "LOCAL_CONDITIONS_CHECKED"
assert not observed.lean_python_refinement_proved
assert not observed.execution_authority_granted

# For an actual OS, validate the original runtime state independently:
original_state_result = audit_native_state(observed_original_plan_state)
# Conditional packet consistency does not imply this state audit passed.
```

Invalid required values give `BLOCKED`; absent required evidence gives
`NO_DATA`. Python booleans must be actual `bool`, not `int`;
naturals must be actual nonnegative integers. Lists, custom JSON
objects, nonfinite numbers, cyclic references, unknown fields and
untrusted callers cannot bypass the checks.

## Proof status and external authority

**Lean source**: Original theorem statements and pinned source blobs
are primary evidence of the claimed mathematical content. Their
machine-verified status must be anchored to actual independent Lean
compiler runs; the source scanner below does not itself compile them.

**Python source**: These modules actively execute their conditions.
They are not pseudocode descriptions. The original kernel state
audit and typed handoff audit must be used separately where applicable.
Even both checks passing cannot prove bisimulation or dependent
semantic preservation between Lean and all CPython executions.

**Authority**: No result supplies issuer authenticity, signed receipt
validity, execution/host permission, full provenance, clinical/legal
authority, truth authority, or Git merge permission.

## Tests and release

```sh
python3 scripts/check_kuuos_lean_python_per_os_contracts_v0_27.py
python3 -m unittest -v tests.lean_python_extensions.test_per_os_contracts_v0_27
python3 -m unittest -v tests.lean_python_extensions.test_per_os_contract_sources_v0_27
```

The static checker exact-pins 12 unchanged original Lean blobs, 3
previous Lean→Python runtime registry files and 12 distinct Python
obligation modules, and checks named theorem declarations/AST.
New tests include success, missing, contradiction, wrong Python
types, adversarial evidence, per-OS restrictions and original
runtime NO_DATA semantics.

This is a **Python-only additive PR**; unchanged Lean source must not
be represented as newly proved or force Strict Lean unnecessarily.
Require exact-source Python Runtime and Governance independent CI.
Any old HEAD's CI SUCCESS remains restricted to that old HEAD.

## Subsequent research, not silently done

- Extend beyond the 12 already integrated OS source bindings to other
  specialized KuuOS OSs, with source/typed-precondition inventory.
- Replace declared witness packets with explicit, source-bound original
  runtime fields where schemas support it, without forging provenance.
- Add formal Lean-to-Python semantics/refinement only if actual
  operational semantics and exact source equivalence are constructed.
- Preserve NO_DATA for unavailable OSs, incomplete typed handoffs and
  external issuer/authority gaps.
