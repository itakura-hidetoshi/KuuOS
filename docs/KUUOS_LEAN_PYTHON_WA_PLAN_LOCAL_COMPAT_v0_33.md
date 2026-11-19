# KuuOS Lean→Python v0.33 — original Wa→PlanOS local source compatibility

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source and scope

Canonical main parent: `cc5093e37adf01f7eec583b0a7ac4c99517d9368`.
v0.32 MemoryOS↔WORLD native local compatibility passed independent
CI #44467776621 (95 successes, one intentional Strict Lean skip), was
merged from PR #3593, and its merge tree matched exact audited source.

Pinned Lean v4.30.0-rc2; mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.
No Lean theorem or original OS kernel/store modifications; new Python
source, checker, regression tests and this document only.

## Why a new v0.33 stage

v0.29 connected actual original DecisionOSPlural→DecisionOSWa states to
the WaEndorsementGate selected Lean data conditions. v0.28 independently
connected an original committed PlanOS step DAG to EffectGuard and
plan-not-execution conditions. v0.3 had already registered precisely the
Wa→Plan edge including a required replan activation receipt.

**Independent local validity never licenses automatic gluing.** This
read-only adapter checks all three original components against the
same exact supplied records, using the existing actual validators.
It adds no DecisionOS→Plan shortcut or synthetic Lean proof.

The order is:
1. Validate a finite, built-in source copy of Plural/Wa/Plan/replan.
2. Run original Plural→Wa native endorsement projection (v0.29).
3. Run original Plan effect-guard projection (v0.28).
4. Run original registered Wa→Plan edge with the *separately supplied*
   replan receipt (v0.3). Missing receipt is NO_DATA.
5. Recheck every typed Wa→Plan field equality in the original
   `EDGE_SPECS`, original source fingerprints, and the exact Plan
   `replan_activation_receipt_digest`.
6. Return SCOPED_WA_PLAN_SOURCE_COMPATIBLE only for this local source
   relationship. Valid but incompatible objects are BLOCKED; missing
   evidence is NO_DATA.

This carries conditions corresponding to original Lean statements in:
- `formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean`
- `formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean`

It does **not** construct Lean dependent proof fields, authenticate an
external signer, prove complete Python semantics or global descent,
authorize execution, grant host permission, or overwrite history.
Every authority/refinement flag is false by construction.

## Native fixture provenance and gap

Tests use the original
`build_native_full_cycle_receipt` in an isolated temp store, with original
Plural, Wa and Plan commit source records and original validators.
The v1.3 fixture does not retain its locally constructed *replan*
activation receipt in `native_artifacts`. For tests, we reproduce that
receipt with the original v0.3 constructor and **the same fixture
parameters** found in its `_build_plan`. This proves local compatibility
for test data; it is **not** a recovered original signed or external
receipt. Runtime callers must supply the actual receipt separately.
No receipt, incomplete source or unverified source is not silently
promoted to a global success.

Native regression covers source preservation, direct Decision→Plan
shortcut rejection, missing replan/Plural data, invalid or forged
receipt, altered Plan guard, altered source Wa and non-escalation of
Lean, host, truth and repository authority.

## Validation and CI gate

```sh
python3 scripts/check_kuuos_lean_python_wa_plan_local_compat_sources_v0_33.py
python3 -m unittest -v tests.lean_python_extensions.test_wa_plan_local_compat_v0_33
python3 -m unittest -v tests.lean_python_extensions.test_wa_plan_local_compat_sources_v0_33
```

Eight exact original native/Lean blobs are pinned, all prior v0.32 and
earlier source pins are inherited. No original source file is modified.
The new two regression modules must not import another `TestCase`
class as a fixture, preventing duplicate test IDs.

**Release gate**: Draft/NO MERGE until identical submitted HEAD/test
merge Git tree, cumulative Python Runtime, independently completed
all-job Governance, and exact-head terminal SUCCESS. Strict Lean
is intentionally skipped for Python/docs-only changes and that skip
is not a new theorem certification.
