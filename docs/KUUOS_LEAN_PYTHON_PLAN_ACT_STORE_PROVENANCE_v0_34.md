# KuuOS Lean→Python v0.34 — original Plan→Act persisted store provenance

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical provenance and fixed scope

Canonical parent: `6f4e3b5f89ef7090839c76ffabdf409ee12adbf7`,
merged PR #3594 v0.33 local Wa→PlanOS typed source compatibility
from independent 97-job exact-head Governance SUCCESS and exact matching
merge tree. Fixed Lean v4.30.0-rc2 and pinned mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only, tighten-only, overwrite-forbidden, same-root.
Existing Lean declarations, OS kernels, ActStore implementation, and
original source files are untouched.

## Why this stage is different

v0.4 verifies *only* original Plan→Act **initial bind admission**.
v0.28 checks real **final ActOS** local authorization and host receipts
but correctly returns NO_DATA for actual numerical jobsClaimed/slicesRun
and original activation issuer authentication. Comparing unrelated
initial and final snapshots would be an invalid descent.

v0.34 ties these separate conditions to the **same genuine ActStore**
source:
1. Finite snapshots of the original committed Plan, separately supplied
   original activation receipt, and observed final Act.
2. Read exactly the existing `act-genesis.json`, `act-ledger.jsonl`,
   and `act-snapshot.json` under one bounded root. Missing files:
   NO_DATA. Symlinks/invalid records: BLOCKED.
3. Replay the entire ledger through **the original ActStore**
   `_recover_unlocked` logic (read-only; no new commits or host calls);
   assert the recovered state equals both original persisted snapshot
   and caller-supplied final Act state. Verify original commit indices.
   Recheck all three file byte streams for changes.
4. Apply original v0.28 Plan guard auditor, original v0.4
   Plan→genesis Act admission auditor, and original v0.28 final Act
   authorization auditor against these exact records. Check all results
   and carry forward explicit numeric/issuer NO_DATA obstructions.
5. Report `SCOPED_PLAN_ACT_STORE_COMPATIBLE` **only for this observed
   source relationship**; no host execution, Lean proof construction,
   general semantic refinement, independent issuer authentication or
   global gluing is authorized.

The record contains `missing_lean_witnesses`:
- `ActOS:actual_jobsClaimed_numeric_witness_unavailable`
- `ActOS:actual_slicesRun_numeric_witness_unavailable`
- `ActOS:original_activation_receipt_issuer_unverified`

Every formal, authority, issuer, and numeric full-proof field remains
false; a local source-consistency result never promotes any of them.

## Native fixture restriction

Tests use original `build_native_full_cycle_receipt` states and
actual file-backed ActStore on a temporary directory. The v1.3 fixture
does not retain its Plan activation receipt inside `native_artifacts`;
the test reproduces it using the original PlanOS constructor with the
same parameters in original `_build_plan`. This is a local fixture
receipt, **not** an externally authenticated or retrieved issuance.
Runtime callers must supply the actual receipt, or receive NO_DATA.
The source auditor does not reproduce missing receipts on its own.

`_recover_unlocked` is used to avoid even creating/touching a lock
file during audit. Pre/post byte equality detects changed observations,
but this is not a multi-process atomic snapshot or concurrency safety
proof. Read-only local replay cannot establish physical host jobs
executed, even if claim flags say at most one job/slice.

## Source pin and CI gate

10 unchanged original native/Lean blobs are pinned; full v0.33-and-earlier
source-pin chain is inherited. New files only: runtime, static checker,
two test modules, documentation. No original modifications.

```sh
python3 scripts/check_kuuos_lean_python_plan_act_store_sources_v0_34.py
python3 -m unittest -v tests.lean_python_extensions.test_plan_act_store_provenance_v0_34
python3 -m unittest -v tests.lean_python_extensions.test_plan_act_store_sources_v0_34
```

Keep PR Draft and NO MERGE until the exact submitted source HEAD,
test-merge Git tree, cumulative Python Runtime, all-page Governance
terminal SUCCESS, and exact-head terminal SUCCESS are independently
checked. Python/docs only, so Strict Lean skip is intentional, not a
new formal theorem certification.
