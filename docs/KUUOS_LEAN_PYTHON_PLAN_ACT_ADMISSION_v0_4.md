# Lean/Python v0.4: exact PlanOS to initial ActOS admission

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Scope and source

Canonical base: `0d77ba4c72d0d183ec76cb14df18dbf50630ec74` on
`itakura-hidetoshi/KuuOS` main. Lean v4.30.0-rc2 and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6` remain unchanged.
No Lean theorem, old OS kernel, archive or protected PR #1558 is changed.

This optional read-only auditor covers only:
`committed PLAN_CANDIDATE -> PlanOS activation receipt -> initial ActOS bind/PENDING`.
Later ActOS snapshots require the actual initial snapshot and are out of scope.
It never applies events, creates authorizations, invokes hosts, writes stores,
or grants truth, proof, clinical, execution or merge authority.

`inspect_plan_act_admission(plan, receipt, act)` returns at most `LINKS_MATCH`.
`audit_plan_act_admission(plan, receipt, act)` additionally invokes the original
`validate_plan_state` and `validate_act_state` on independent copies. Only
successful, correctly typed, nonmutating validator results permit `PASS`.
Missing evidence/dependencies remain `NO_DATA`; observed contradiction is
`BLOCKED`. Both missing and contradictory evidence are retained. BLOCKED is not
a theorem of mathematical impossibility. Complete input snapshot hashes bind the
result to supplied data, not to external authenticity.

## Schema repair of the earlier uncommitted candidate

The earlier local candidate incorrectly required `step_digests` in the PlanOS
activation receipt and used `replan_receipt_digest` where the actual constructor
uses `replan_activation_receipt_digest`. Its synthetic tests copied the same
mistake; they were not evidence of native compatibility.

The current candidate uses the actual constructor schema. The original receipt
binds the full PlanOS snapshot through `plan_state_digest` and carries the exact
`topological_order`; it has no `step_digests` field. No invented field is added to
the original kernel. A genuine-constructor schema parity test now guards this
boundary. Missing real references are not filled with fabricated replacements.

## Conditional formal grounding

`KUOS.PlanOS.ReplanBoundSynthesisV0_1` supplies conditional nonexecution,
future-only, plan-phase and replan-receipt boundaries.
`KUOS.ActOS.AuthorityBoundInvocationV0_1` separates committed plan, exact step,
Act phase, host license and projection receipt bindings. The admission auditor
does not discharge these five invocation obligations. Source correspondence is
not a Lean proof of Python refinement, proof of receipt authenticity, or evidence
of an actual effect.

The inspector checks exact versions, strict Boolean boundaries, inherited
references, hashes, time order, plan-step ID coverage and initial empty/no-effect
ActOS fields. Unknown receipt and initial-Act fields are rejected. The complete
PlanOS schema remains the original validator's responsibility. Validated input
is finite built-in JSON (64-level and 200,000-value limits); these are engineering
bounds, not Lean theorems. Custom mappings, cyclic/nonfinite values, invalid UTF-8
and unserializable integers fail closed. This is not a sandbox for hostile Python
validators or import-path replacement.

## Verification and acceptance

The native-schema fixture first reproduced a failing test against the old
candidate; the repaired local unit/checker suite then passed 45 tests. Seven
native integration cases are mandatory, including real constructors, unmodified
validators, exact schema parity, resealed substitutions and no host invocation.
Native dependencies are unavailable in the local partial checkout; no local
native or full-regression success is claimed.

The cumulative runner retains its original eleven frontier checker/test pairs
and appends three pairs for unit, checker-mechanism and native tests. Missing
native dependencies fail rather than silently skip. The checker pins nine
source blobs and eleven named theorem declarations; it does not run Lean.

Run in a complete checkout:

```sh
python3 scripts/check_kuuos_lean_python_plan_act_bindings_v0_4.py
python3 -m unittest -v tests.test_kuuos_lean_python_plan_act_admission_v0_4 tests.test_kuuos_lean_python_plan_act_checker_v0_4 tests.test_kuuos_lean_python_plan_act_native_v0_4
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

Require exact-head GitHub workflow/job/step completion, actual native-test and
cumulative logs, and source/test-merge tree equality before integration. Prior
main or v0.3 green does not certify this candidate. Python-only changes do not
add a Lean compilation or refinement claim. Final CI status belongs in the
source-bound PR evidence; this document does not predict success.
