# KuuOS Lean→Python v0.6 — typed path composition and gluing obstruction

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source and status

Canonical repository: itakura-hidetoshi/KuuOS; baseline main:
ffd6835d182df791d971c199750d5e9e38a32741 (v0.5).
Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6, protected
PR #1558 and all original Lean/OS runtime kernels remain unchanged.

The sole new code implementation:
[runtime/kuuos_lean_python_os_path_composition_v0_6.py](../runtime/kuuos_lean_python_os_path_composition_v0_6.py).

This is a **read-only scoped path auditor**, not a formal theorem, new
Lean proof, global descent theorem or certification of Python refinement.

## Precisely eight named OS in order

~~~
DecisionOS → DecisionOSPlural → DecisionOSWa → PlanOS
                                         → ActOS → ObserveOS → VerifyOS → LearnOS
~~~

The runtime auditor uses the seven exact *existing* edges from
[kuuos_lean_python_os_registry_v0_5.py](../runtime/kuuos_lean_python_os_registry_v0_5.py).
No shortcut DecisionOS→PlanOS, no invented WORLD-to-OS gluing,
no direct MemoryOS/CodeAI execution bridge.

**An audit of only one contiguous subpath is explicitly scoped**; it cannot
be passed off as a verification of the entire eight-OS route.

Original receipts are inputs, never synthesized:

- DecisionOSWa->PlanOS: original Wa replan activation receipt;
- PlanOS->ActOS: original PlanOS plan-phase activation receipt.

The caller must provide the *same original intermediate snapshot* shared by
two adjacent edges. The auditor creates independent, bounded, finite
JSON-only copies for each existing typed edge audit, checks every available
edge and independently compares lineage ID, mission contract digest, and
nondecreasing updated timestamps across nodes. It retains an input SHA-256
for each observed state and required receipt. Hashes bind the supplied
snapshot; they **do not authenticate external issuer/provenance**.

## Outcomes

- SCOPED_PATH_CHECKED: every edge in the **explicitly named** contiguous
  subpath passed its real existing Python auditor, those auditors reported
  runtime checks completed, and the additional cross-node context checks
  agree; no corresponding Lean descent, real-world truth or execution
  authority follows.
- NO_DATA: an original state, required original receipt, typed edge
  proof/runtime mapping, runtime validation, or intermediate is missing.
- BLOCKED: an observed contradiction, changed context, time reversal,
  rejected runtime check, invalid JSON or attempted mutation; this is **not**
  a Lean proof of mathematical impossibility.

Observations of contradictions and missing evidence are stored
**simultaneously**; a contradiction is not erased by a separate absence.

Every result explicitly keeps:
formal_descent_certified=False,
lean_python_refinement_proved=False,
external_receipt_authenticated=False,
execution_authority_granted=False,
truth_authority_granted=False,
merge_authority_granted=False.

## Tests and preservation

New independent module:
[tests/test_kuuos_lean_python_os_path_composition_v0_6.py](../tests/test_kuuos_lean_python_os_path_composition_v0_6.py).

It includes a fully synthetic seven-edge *dispatcher* test using explicit
test doubles (not a real full-route validation); fail-closed missing,
blocker, mutation, context, timestamp and schema tests; and genuine original
repository constructor/validator tests on **five valid contiguous
subpaths**, namely:

- Decision→Plural→Wa→Plan (3 edges, genuine Wa replan receipt);
- Plan→Act (1 edge, genuine plan activation receipt);
- Act→Observe, Observe→Verify and Verify→Learn (1 edge each).

The actual genuine subpaths are separately constructed. **They cannot
be pasted together** as one genuine end-to-end eight-OS positive witness.
Such a witness is not supplied, and a global Lean descent theorem remains
NO_DATA. A passing per-edge test is not an authority transfer.

The old v0.5 static checker requires exactly the original list of cumulative
runner entries. Rather than weaken the checker or edit the fixed runner,
the v0.6 test classes are imported additively by the *already registered*
tests.test_kuuos_lean_python_os_registry_v0_5 module. Python unittest
discovers these imported TestCase classes. The original 21 v0.5 tests and
all prior v0.1–v0.4 tests remain in the cumulative run, with no skipped
native tests.

Run inside the complete repository:

~~~sh
python3 scripts/check_kuuos_lean_python_os_registry_v0_5.py
python3 -m unittest -v tests.test_kuuos_lean_python_os_registry_v0_5
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
~~~

Require completed exact-head independent GitHub workflow/job/step logs,
original native test pass, source/test-merge Git tree equality and
post-merge independent push CI. A prior v0.5 green does not certify v0.6.

## Use with original states and receipts

~~~python
from runtime.kuuos_lean_python_os_path_composition_v0_6 import audit_typed_path

audit = audit_typed_path(
    {
        "PlanOS": committed_original_plan_state,
        "ActOS": original_initial_act_state,
    },
    receipts={"PlanOS->ActOS": original_plan_phase_activation_receipt},
    start="PlanOS",
    end="ActOS",
)
# This verifies only the PlanOS→ActOS admission path.
# It never invokes ActOS or grants a host license.
~~~

## Remaining obstruction

A genuine, provenance-matched end-to-end witness across all seven edges,
including a committed PlanOS that is the *same* PlanOS consumed by ActOS,
and a committed ActOS effect subsequently consumed by ObserveOS, is still
unconstructed in this change. Separate fixture positives are local, and
cannot be promoted to a global construction by convenience or preference.
The corresponding Lean/Python semantic refinement is also unproved.
