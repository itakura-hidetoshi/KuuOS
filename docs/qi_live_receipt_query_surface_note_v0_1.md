# Qi Live Receipt Query Surface v0.1

This addendum follows live receipt ingestion and exposes a read-only operator-facing query / replay surface.

## Position

```text
live receipt ingestion
  -> operator-facing query surface
  -> operator dashboard renderer / replay index
```

## What opens

- live receipt query snapshot
- replay packet rendering
- replay query key
- operator summary
- dashboard-ready flag
- read-only surface invariant

## Required input

```text
ingestion_status = QI_LIVE_RECEIPT_INGESTION_READY
live_receipt_ingested = true
external_case_number present
external_case_url present
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
python scripts/run_qi_live_receipt_query_surface_checks_v0_1.py
```

Expected result:

```text
PASS: Qi live receipt query surface checks
```

## Next layer

The next addendum may render an operator dashboard or build a replay index from this query surface.
