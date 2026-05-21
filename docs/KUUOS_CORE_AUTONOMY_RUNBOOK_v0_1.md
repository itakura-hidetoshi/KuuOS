# KuuOS Core Autonomy Runbook v0.1

Status: CORE_AUTONOMY_MINIMAL_BASELINE

Repository: itakura-hidetoshi/KuuOS

This runbook describes the minimal local autonomy layer for KuuOS core governance.

## Meaning of autonomy in this baseline

Core autonomy means that the repository can run a bounded local self-check loop:

```text
sense -> contract_check -> validate -> decide -> audit
```

The loop checks repository readiness, validates the core governance surface, decides `PASS` or `HOLD`, and writes an append-only JSONL audit event with a SHA-256 event hash.

It does not grant execution authority, clinical authority, theorem truth, institutional authority, legal authority, memory overwrite authority, or governance bypass authority.

## Files

```text
specs/kuuos_core_autonomy_contract_v0_1.json
scripts/run_kuuos_core_autonomy_v0_1.py
scripts/validate_kuuos_core_autonomy_contract_v0_1.py
docs/KUUOS_CORE_AUTONOMY_RUNBOOK_v0_1.md
.github/workflows/kuuos_core_autonomy_validation.yml
```

## Fast structural validation

```bash
python3 scripts/validate_kuuos_core_autonomy_contract_v0_1.py
```

This validates the contract shape and runs the autonomy runner in `--self-test-check` mode.

## One-shot autonomous core cycle

```bash
python3 scripts/run_kuuos_core_autonomy_v0_1.py --mode once
```

Default behavior:

- uses only Python standard library
- calls `python3 scripts/run_core_governance_full_checks_v0_1.py`
- writes `audit/kuuos_core_autonomy_audit_v0_1.jsonl`
- exits `0` on `PASS`
- exits nonzero on `HOLD`

## Fast one-shot self-test

```bash
python3 scripts/run_kuuos_core_autonomy_v0_1.py \
  --mode once \
  --self-test-check \
  --audit-log /tmp/kuuos_core_autonomy_audit_v0_1.jsonl
```

This does not run the full core governance suite. It checks the autonomy runner, contract, audit event emission, and event hash path quickly.

## Bounded daemon mode

```bash
python3 scripts/run_kuuos_core_autonomy_v0_1.py \
  --mode daemon \
  --max-cycles 3 \
  --interval-seconds 300
```

The daemon mode is intentionally bounded by `--max-cycles`. It is suitable for local supervision loops and CI smoke tests, not for unrestricted background execution.

## Custom validation command

```bash
python3 scripts/run_kuuos_core_autonomy_v0_1.py \
  --mode once \
  --command python3 scripts/run_core_governance_full_checks_v0_1.py
```

Arguments after `--command` are treated as the validation command.

## Audit event

Each cycle appends one canonical JSON line. The event includes:

```text
schema
timestamp_utc
cycle_id
contract_id
runtime_mode
phase_results
decision_state
safety_stop
previous_event_hash
event_hash
```

`event_hash` is computed as:

```text
sha256(canonical_json(event_without_event_hash))
```

When an existing audit log is used, the previous event hash is copied into `previous_event_hash`.

## Fail-closed behavior

If sensing, contract checking, validation, or audit continuity fails, the decision state becomes `HOLD` and `safety_stop` becomes `true`.

The first baseline supports only local self-checking. Future versions may add repair proposal generation, but repair output must remain candidate-only unless separately licensed by governance and human/institutional boundary rules.

## Boundary

```text
autonomy != execution authority
validation != truth
CI pass != theorem proof
core PASS != clinical decision
core PASS != medical act authorization
audit event != external audit acceptance
local daemon != production AGI runtime
```

This baseline makes KuuOS able to run its core self-checking loop locally while preserving the repository's non-authority policy.
