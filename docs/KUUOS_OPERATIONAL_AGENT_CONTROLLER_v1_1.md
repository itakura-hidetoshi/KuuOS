# KuuOS Operational Agent Controller v1.1

## Purpose

This additive layer turns Adaptive Agent Reference Architecture v1.0 into a finite operational orchestration surface without changing ownership of BeliefOS, DecisionOS, PlanOS, ActOS, ObserveOS, VerifyOS or LearnOS.

```text
committed decision
  -> bounded plan
  -> active capability record
  -> fresh capability epoch
  -> finite execution lease
  -> active session
  -> ActOS staged adapter call
  -> independent ObserveOS evidence
  -> VerifyOS evaluation
  -> future-only LearnOS delta
  -> next PlanOS basis
```

The controller owns ordering only. It does not mint truth, capability, execution authority, host access, external commit, root rewrite or successor-cycle authority.

## Authorization conjunction

Adapter staging is permitted only when all of the following hold:

1. the adaptive state is valid, active, at `PLAN`, leased, and has an active session;
2. owner, lineage and session bindings match exactly;
3. the capability is registered and active;
4. capability, intent, lease and adaptive state share a fresh epoch;
5. adapter kind, operation and resource match both capability and lease;
6. the requested effect is below both capability and lease ceilings;
7. the lease is active in its finite sequence window and retains use budget;
8. the host-license digest is present;
9. the idempotency key has not been consumed;
10. no external commit is requested.

`capability present != execution authorized`.

## Operational separation

The staged adapter returns a tool trace, not a world fact. A distinct observer produces the evidence committed to the adaptive transition kernel. VerifyOS checks that independent evidence, and LearnOS produces a future-only delta.

```text
adapter result != observation
observation != truth
verification passed != root rewrite
learning delta != current-cycle mutation
closed receipt != successor authority
```

## Effect boundary

The reference adapter supports deterministic staged effects only. `EXTERNAL_COMMIT` is blocked before adapter invocation and routed to `REQUEST_HUMAN`. A future effectful adapter requires a separate adapter contract, fresh capability epoch, scoped lease, explicit host license, observation/reconciliation contract and dedicated review.

## Replay and restart safety

Lease use is reserved in an append-only ledger before the adapter call. The JSONL ledger and receipt store flush and `fsync` each append. Restart therefore does not reopen a consumed action budget or idempotency key.

The receipt chain records:

1. cycle opening;
2. authorization outcome;
3. lease-use reservation;
4. ActOS staged effect;
5. independent ObserveOS evidence;
6. VerifyOS disposition;
7. LearnOS future-only delta;
8. cycle closure or bounded stop.

## Recovery routing

- stale capability epoch -> `REROTATE`
- expired, exhausted or replayed lease -> `REVALIDATE`
- incompatible adapter, operation, resource or effect ceiling -> `REPLAN`
- external commit or authority-binding problem -> `REQUEST_HUMAN`
- invalid or authority-escalating adapter output -> `ABORT`

Recovery classification is not recovery execution. The existing adaptive kernel still requires fresh authority, lineage, activation and session where applicable.

## Validation

```bash
PYTHONPATH=. python3 scripts/validate_operational_agent_controller_manifest_v1_1.py
PYTHONPATH=. python3 scripts/check_operational_agent_controller_v1_1.py
PYTHONPATH=. python3 -m unittest -v tests.test_operational_agent_controller_v1_1
python3 scripts/run_kuuos_runtime_full_check_v1_1.py
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.OperationalAgentControllerV1_1
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

A green check is a reproducible consistency receipt. It is not unrestricted execution permission or an external truth certificate.
