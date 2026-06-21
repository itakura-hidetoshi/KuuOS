# KuuOS Governed Self-Modification Gate v0.26

## Purpose

v0.26 permits bounded system improvement without granting the system authority to rewrite itself.

```text
proposal
→ static analysis
→ isolated sandbox
→ regression suite
→ formal/property checks
→ bounded canary
→ external approval when required
→ limited deployment authorization
→ rollback or externally verified closure
```

The gate produces evidence and authorization records. It performs neither production deployment nor rollback itself.

## Permanent prohibitions

The following actions are rejected at static analysis and can never be approved by later evidence:

```text
widen_own_authority
delete_hard_gate
disable_audit
erase_provenance
remove_rollback
grant_unrestricted_shell
grant_unrestricted_network
redefine_success_to_hide_failure
```

## Proposal boundary

Every proposal binds:

- exact v0.25 source state and transaction receipt
- immutable base, candidate, and rollback artifact digests
- changed paths
- intended improvement and success criteria
- requested actions
- finite canary percentage, deployment cycles, and rollback window
- external-approval policy

A proposal is non-executing and does not alter the running system.

## Evidence chain

Evidence must be submitted in strict order:

```text
static_analysis
sandbox
regression
formal_property
canary
```

Each stage binds the predecessor state, isolated environment, evaluator identity, evidence digests, findings, and a pass/fail result. Failed evidence cannot be hidden by a later stage.

Canary success is evidence, not truth or permanent renewal.

## External approval

When policy requires approval, a bounded external approval receipt must be present before limited deployment can be authorized. Approval neither executes nor self-authorizes the proposal.

## Limited deployment

Authorization remains finite:

- canary percentage is at most 10% and no larger than the proposal limit
- deployment cycles are finite
- expiry is finite
- rollback window is finite and nonzero
- exact rollback artifact is immutable
- separate ActOS authorization and transaction are required
- production-wide deployment is not authorized
- user pause/cancel/handover remains available

## Rollback

Rollback requires an external ActOS receipt and preserves failure evidence and provenance. The governance gate never performs automatic rollback or directly mutates the running system.

## Persistence

```text
self-modification-initial.json
self-modification-ledger.jsonl
self-modification-snapshot.json
```

The ledger is authoritative. Duplicate events replay idempotently; stale events are rejected; snapshot repair is explicit.

## Formalization

Lean module:

```text
KUOS.OpenHorizon.GovernedSelfModificationKernelV0_26
```

Final theorem:

```lean
governed_self_modification_boundary
```

It composes the v0.25 foreground-control boundary with proposal, permanent-prohibition, validation-chain, external-approval, limited-deployment, rollback, and append-only persistence boundaries.

## Validation

```bash
PYTHONPATH=. python scripts/check_governed_self_modification_v0_26.py
PYTHONPATH=. python -m unittest -v tests.test_governed_self_modification_v0_26
PYTHONPATH=. python scripts/check_event_wakeup_control_resource_v0_25.py
PYTHONPATH=. python scripts/check_transactional_effect_reconciliation_v0_24.py
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.GovernedSelfModificationKernelV0_26
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
