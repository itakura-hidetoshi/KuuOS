# KuuOS Lean→Python v0.35 — original ActOS→ObserveOS persisted typed handoff

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Fixed source and goal

Canonical parent main: `b782f5a34607ff645e7bccb9d8934b38301517a1`.
v0.34 PR #3595 merged after 98-job exact-head Governance SUCCESS
(97 SUCCESS, one intentional Lean skip), cumulative Python Runtime
788/788, additional regressions 264/264, exact matching Git trees.
Lean v4.30.0-rc2 and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6` pinned.
Append-only / tighten-only / overwrite-forbidden / same-root.
Original Lean source, OS kernels, stores and prior validators unchanged.

The aim is to convert verified Lean conditions for each OS into
source-bound original Python structures, not rewrite Lean as prose.

## New local source compatibility check

v0.34 joined original Plan→Act initial admission and the actual
file-backed final ActOS source with the original ActStore replay.
v0.35 extends the *registered* original ActOS→ObserveOS handoff to
**both original file-backed OS stores**, never a direct synthetic edge:

1. Require caller-supplied committed original Act and Observe states,
   plus distinct existing ActStore and ObserveStore roots.
2. Read all three original persisted files from **each** store, check
   symlink/size/missingness, and use native `_recover_unlocked` for
   the full original genesis→commit replay. Check snapshot equality,
   commit indices, supplied final states and unchanged file bytes.
3. Apply the original `audit_handoff("ActOS","ObserveOS", act,
   observe_genesis)` — this checks the typed source-to-initial-Observe
   compatibility, including original Act/Observe validators, selected
   step/host receipt identity and time/lineage constraints.
4. Apply original v0.28
   `audit_native_observe_from_act(act, final_observe)`,
   preserving the original final comparison-receipt digest,
   verdict/debt conditions, and original typed handoff.
5. Require the registered `HANDOFF_CONTRACTS` source-field equalities
   from original Act to Observe genesis, and the same fields retained
   at final Observe.
6. Only then report `SCOPED_ACT_OBSERVE_STORE_COMPATIBLE`.

Missing source or uncommitted store: NO_DATA.
Contradictory native records, mismatched stores and invalid digests:
BLOCKED. Passed local source relations are limited to exactly observed
states and current unmodified native pinned definitions.

## Remaining formal and external obstructions

- Observed original host receipts are not external issuer signatures.
- An effect claim is not a newly proved numeric jobsClaimed/slicesRun
  witness in Lean's `ActOS.BoundedInvocation`.
- ObserveOS does not establish VerifyOS acceptance, independent truth,
  causal attribution or completion of PlanOS.
- Native Python state checks and persisted replay are not a formal
  semantics-preserving Lean→Python compiler or a general global
  gluing/descent proof.
- Read-only replay is not a multi-process atomic cross-root snapshot;
  racing external writers could invalidate the observation.

All authority and global/formal boolean fields remain false.

## Original native regression scope

The original `build_native_full_cycle_receipt` fixture generates
file-backed ActStore at `root/act` and ObserveStore at
`root/downstream/observe`; both original OS kernels and all native
validators are unmodified. The tests cover valid replay, missing
source, wrong roots, source substitution, receipt mutation, ledger
or snapshot tampering, symlinks, byte preservation, and no authority
escalation. No external issuance is claimed.

Nine exact original Lean/native Git blobs are newly pinned, and all
existing v0.34-and-earlier source pins remain active. Five additive
files only: one runtime auditor, one source checker, two test modules,
one document.

```sh
python3 scripts/check_kuuos_lean_python_act_observe_store_sources_v0_35.py
python3 -m unittest -v tests.lean_python_extensions.test_act_observe_store_compat_v0_35
python3 -m unittest -v tests.lean_python_extensions.test_act_observe_store_sources_v0_35
```

**Release gate:** keep Draft and NO MERGE until exact submitted HEAD,
matching test-merge Git tree, full cumulative Python Runtime,
independent all-job Governance completed/SUCCESS, and exact-head
terminal SUCCESS. This is Python/docs only: intentional Strict Lean
skip is NOT a new Lean theorem certification.
