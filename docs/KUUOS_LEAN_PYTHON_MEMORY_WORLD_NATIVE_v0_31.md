# KuuOS Lean→Python v0.31 — MemoryOS and WORLD original native-source proof conditions

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Scope and governance

The aim is to translate existing KuuOS Lean theorem *data conditions*
into **the actual Python OS implementations**, using their original
state, store and receipts, not synthetic witness dictionaries.

Research parent: staged v0.30 CodeAI source SHA
`6efdff6a1675fc561615623a1541a5a875cd487c` on
`feat/lean-python-native-codeai-selection-v0-30`.
Do not create a v0.31 PR or assert formal adoption until v0.30 has
terminal independent Governance SUCCESS, been merged to canonical main,
and this staging branch has been reconnected to that exact main.
Lean v4.30.0-rc2, mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.

**Seven purely additive files; no old Lean/source/OS kernel, host
implementation, store, history or runtime governance overwritten.**

## MemoryOS — v0.35

Original Lean:
`formal/KUOS/OpenHorizon/MemoryOSQiWorldBlockerIntegrationKernelV0_35.lean`.

Original native:
`runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py`.

Source-bound adapter:
`runtime/kuuos_lean_python_memory_native_binding_v0_31.py`.

The adapter accepts one **original** MemoryOS blocker/qi/WORLD
snapshot and its separately recorded retrieval packet.
The two original native validators must succeed. The retrieval is
recomputed using the **unchanged** native read-only retrieval
constructor and its exact saved source snapshot; route, blocker
coverage and all recorded fields must match.

The adapter then checks:
- native `qi_context.process_history_preserved` true,
  `snapshot_replacement_used` false;
- source active blocker preserved as context; no silent discharge
  or missing-evidence repair;
- WORLD is only a projection: no WORLD commit/rewrite claimed;
- retrieval is only a candidate, does not cause automatic plan
  mutation, WORLD commit, tool execution or truth promotion;
- memory append candidate is append-only, not a claim that this kernel
  actually performed durable persistence.

Those seven **flat data conditions** correspond to the projection
in the existing v0.27
`kuuos_lean_python_memory_obligations_v0_27.audit_witness`.

The original v0.35 Lean structure also contains nested
`NonMarkovMemoryBoundary`, `QiProcessTensorBoundary`,
`CrossCycleBlockerCertificate` and
`AuthorizedAtomicWorldCommitKernelV034` fields. A local snapshot
does **not** construct their dependent Lean proof objects.
Therefore `nested_lean_proof_structures_constructed` remains false,
even when the flat native source check succeeds.

Incomplete upstream blocker evidence is `NO_DATA`, never an
authorization to release the blocker. This test fixture uses the
original MemoryOS builder/validator but mocks external upstream
validators, as openly recorded in the original v0.35 unit tests.
It does not authenticate those external source packets.

## WORLD — v0.34

Original Lean:
`formal/KUOS/OpenHorizon/AuthorizedAtomicWorldCommitKernelV0_34.lean`.

Original Python:
`runtime/kuuos_authorized_atomic_world_commit_v0_34.py`,
`runtime/kuuos_authorized_atomic_world_commit_entry_v0_34.py`.

New binding module:
`runtime/kuuos_lean_python_world_native_binding_v0_31.py`.

This adapter requires all five original source/envelope records:
**verified disposition candidate, finite single-use authorization,
exactly reconstructible request, immutable recorded atomic commit
receipt, and the full persisted WORLD store**.

The unchanged WORLD source validators verify all of these, including
all historic store commits, generation/fencing/lease monotonicity,
same root, receipt hash chain and absence of history deletion.
The original request builder must independently reconstruct the
given request from the source disposition and authorization. Their
hashes and original store's last receipt must match exactly.
A genesis store with no committed receipt returns `NO_DATA`.

Selected native source conditions are then fed into the existing
`kuuos_lean_python_world_obligations_v0_27.audit_witness`:
- local finite single-use authorization does **not** place a global
  time, cycle or generation bound on the open horizon;
- an atomic commit preserves one store/receipt state, immutable
  append-only history and the exact constitutional root;
- rollback references are retained and require fresh authorization,
  never silently delete the original history or trigger rollback;
- a WORLD record neither asserts absolute truth nor grants
  plan/ActOS execution rights.

The adapter does not call the native *write* function and itself
performs no new store or host effect. It does not certify that the
original `issued_by` fields represent an externally authenticated
issuer, or construct Lean's nested
`VerifiedDisposition` dependent proof structure.

Original native source tests use the full v0.34 disposition→
authorization→request→commit builder in a temporary store.
Unlike MemoryOS's upstream fixture, WORLD tests do not monkey-patch
the original WORLD validators. They explicitly check the persisted
original store bytes before and after auditing.

## Static source and runtime release gates

The v0.31 checker inherits all exact v0.30 source pins and adds twelve
original MemoryOS/WORLD/Lean/fixture source pins, two original-source
adapter entrypoints and both new test class inventories.
Twenty-four new regression tests (15 runtime and 9 source tests)
cover genuine native local results, history/source immutable checks,
quarantine, missing records, forged receipt/authorization/issuer flags,
same-root and non-authority boundaries.

```sh
python3 scripts/check_kuuos_lean_python_memory_world_native_sources_v0_31.py
python3 -m unittest -v tests.lean_python_extensions.test_memory_world_native_bindings_v0_31
python3 -m unittest -v tests.lean_python_extensions.test_memory_world_native_sources_v0_31
```

None of these static checks are a new Lean compiler certificate.
No original Lean source is changed; Strict Lean should skip in
Python-only PR validation. Do not claim a new Lean theorem is
proved merely because the corresponding Python test passes.

**NO PR / NO MERGE until staging ancestry is reconciled to the
independently certified merged v0.30 main.** Then require exact
submitted-head Python cumulative Runtime, exact Git source/test-merge
tree match, all paginated Governance jobs and terminal workflow
completed/SUCCESS. Keep any failing stage in the SAME PR, no excess
red PR proliferation.

All source-bound statements preserve distinction between:
local original Python validation; Lean theorem consequences only
under their hypotheses; unconstructed dependent proof objects;
external signer authenticity; and host/decision authority.
