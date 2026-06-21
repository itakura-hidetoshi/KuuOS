# KuuOS Finite-Cycle Continuity Kernel v0.27

## Purpose

v0.27 composes the v0.20–v0.26 contracts into a restart-safe sequence of separately bounded cycles.

```text
mission contract
→ observation and belief
→ semantic plan and independent verification
→ bounded memory and learning
→ transactional effect reconciliation
→ wake-up, user control, and resource admission
→ governed change review
→ checkpointed next cycle
```

The kernel does not turn a cycle into an unrestricted process. Continuity is represented as a repeatable sequence in which every cycle has a fresh receipt, finite cost, finite step count, finite duration, and finite resource lease.

## Lower-contract binding

The integrated contract binds exact digests for:

- v0.20 mission contract
- v0.21 observation and belief state
- v0.22 semantic planner and verifier
- v0.23 cognitive memory and credit
- v0.24 transaction and world-effect reconciliation
- v0.25 event, foreground control, and resource governance
- v0.26 governed change management

No lower receipt is replaced by the v0.27 summary.

## Cycle boundary

Every committed cycle binds:

- exact mission and lineage
- exact finite lease
- fresh cycle authorization
- exact host license
- all seven lower-layer receipt digests
- finite cost, steps, and duration
- route and checkpoint
- user-control observation

Supported routes are:

```text
CONTINUE
PAUSE
RENEWAL_REQUIRED
TERMINATE
HANDOVER
```

## Renewal

Renewal is external and explicit. A renewal receipt creates another finite lease and leaves the state paused. A separate resume command is required before another cycle.

There is no fixed total cycle counter in the kernel, but each lease and each cycle remain finite. Repeatability therefore does not remove local resource or authority boundaries.

## Restart recovery

### Process restart

```text
ledger replay
→ checkpoint verification
→ process epoch increment
→ PAUSED
→ explicit resume
```

### Host restart

```text
ledger replay
→ checkpoint verification
→ host epoch increment
→ fresh host license required
→ host rebind receipt
→ PAUSED
→ explicit resume
```

Completed cycle count and lower receipts remain unchanged across recovery.

## Foreground control

The following controls remain available independently of queued work:

```text
pause
resume
terminate
handover
request_renewal
renew
```

Handover preserves the latest checkpoint. Termination remains reachable at every nonterminal checkpoint.

## Persistence

```text
finite-cycle-initial.json
finite-cycle-ledger.jsonl
finite-cycle-snapshot.json
```

The ledger is authoritative. Duplicate events replay without another append. Stale events are rejected. Snapshot disagreement fails closed and can be repaired only by explicit ledger replay.

## Formalization

Lean module:

```text
KUOS.OpenHorizon.FiniteCycleContinuityKernelV0_27
```

Key theorems:

```lean
every_cycle_remains_finite
repeatable_cycles_preserve_local_bounds
restart_recovery_preserves_cycle_history
foreground_controls_remain_available
continuity_history_is_replay_safe
lower_contracts_remain_composed
integrated_finite_cycle_continuity_boundary
```

`every_cycle_remains_finite` is quantified over `Fin n`, so the theorem applies to every finite prefix length while preserving the same local cycle boundary.

## Validation

```bash
PYTHONPATH=. python scripts/check_integrated_long_duration_operation_v0_27.py
PYTHONPATH=. python -m unittest -v tests.test_integrated_long_duration_operation_v0_27
PYTHONPATH=. python scripts/check_governed_self_modification_v0_26.py
PYTHONPATH=. python scripts/check_event_wakeup_control_resource_v0_25.py
PYTHONPATH=. python scripts/check_transactional_effect_reconciliation_v0_24.py
PYTHONPATH=. python scripts/check_nonmarkov_cognitive_loop_v0_23.py
PYTHONPATH=. python scripts/check_semantic_planner_verifier_kernel_v0_22.py
PYTHONPATH=. python scripts/check_observation_belief_state_kernel_v0_21.py
PYTHONPATH=. python scripts/check_mission_contract_kernel_v0_20.py
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.FiniteCycleContinuityKernelV0_27
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
