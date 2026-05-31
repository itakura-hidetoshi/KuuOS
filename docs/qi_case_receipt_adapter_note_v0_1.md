# Qi Case Receipt Adapter v0.1

This addendum follows the Qi review request packet and introduces an approved case receipt adapter.

## Position

```text
review request packet
  -> approved case receipt adapter
  -> external connector binding / outbox delivery adapter
```

## What opens

- approval-gated case receipt generation
- approved local case-open state in the receipt
- idempotency key requirement
- approval receipt SHA requirement
- dry-run path
- blocked path for missing idempotency or approval evidence

## What remains closed

- external API call
- outbound delivery
- daemon restart
- daemon stop
- daemon resume
- probe execution
- MemoryOS write / append / overwrite
- world update
- control packet mutation
- auto-remediation
- daemon control authority

## Boundary

This adapter can mark `case_opened: true` only in the local receipt after approval and idempotency gates are satisfied. It does not call an external ticketing system, webhook, email service, chat service, or incident platform.

## Validation

```bash
python scripts/run_qi_case_receipt_adapter_checks_v0_1.py
```

Expected result:

```text
PASS: Qi case receipt adapter checks
```

## Next layer

The next addendum may bind this receipt to an external connector or outbox delivery adapter. That layer must preserve idempotency and produce an external delivery receipt.
