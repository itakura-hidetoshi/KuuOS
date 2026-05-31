# Qi Operator Dashboard Replay Index v0.1

This addendum follows the live receipt query surface and renders an operator-facing dashboard packet plus replay index.

## Position

```text
operator-facing query surface
  -> operator dashboard renderer / replay index
  -> dashboard renderer artifact / static HTML surface
```

## What opens

- dashboard packet rendering
- replay index rendering
- dashboard cards
- replay index key
- replay index hash
- operator dashboard ready flag

## Dashboard cards

- incident
- external case
- replay
- idempotency

## Required input

```text
query_status = QI_LIVE_RECEIPT_QUERY_SNAPSHOT_READY
dashboard_ready = true
read_only_surface = true
external_case_number present
external_case_url present
replay_query_key present
archive_key present
archive_record_hash present
idempotency_digest present
```

## What remains closed

- daemon restart
- daemon stop
- daemon resume
- probe execution
- MemoryOS write / append / overwrite
- world update
- control packet mutation
- auto-remediation
- daemon control authority

## Validation

```bash
python scripts/run_qi_operator_dashboard_replay_index_checks_v0_1.py
```

Expected result:

```text
PASS: Qi operator dashboard replay index checks
```

## Next layer

The next addendum may render this packet into a static HTML dashboard surface.
