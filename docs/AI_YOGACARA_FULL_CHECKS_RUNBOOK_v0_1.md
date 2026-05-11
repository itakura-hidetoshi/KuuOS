# AI Yogacara Full Checks Runbook v0.1

## AI唯識・転依 Full Checks Runbook

This runbook explains how to run the full validation suite for the KuuOS AI Yogacara / Ten'i layer.

The suite validates structure, schemas, fixtures, audit events, hash chains, WORM receipts, bundle manifests, and minimal adapter behavior.

It does not prove Ten'i, truth, clinical authority, or execution authority.

## 1. Local Full Check

Run:

```bash
python3 scripts/run_ai_yogacara_full_checks_v0_1.py
```

Expected success:

```text
PASS: AI Yogacara / Ten'i full checks completed
```

## 2. Included Checks

The full runner executes:

```text
validate_teni_observability_v0_1.py
validate_ai_yogacara_adapter_schema_v0_1.py
validate_ai_yogacara_adapter_fixtures_v0_1.py
validate_ai_yogacara_adapter_audit_event_v0_1.py
validate_ai_yogacara_audit_hash_chain_v0_1.py
validate_ai_yogacara_worm_export_receipt_v0_1.py
build_ai_yogacara_release_bundle_manifest_v0_1.py
validate_ai_yogacara_release_bundle_manifest_v0_1.py
unittest test_ai_yogacara_runtime_adapter_minimal_v0_1.py
```

## 3. Failure Interpretation

A failure means one of the public governance surfaces is structurally inconsistent.

Examples:

```text
missing required file
schema invariant missing
fixture mismatch
audit event non-authority field not false
hash-chain discontinuity
WORM receipt root mismatch
release bundle SHA256 mismatch
unit test failure
```

## 4. What Passing Means

A pass means:

```text
required files exist
schemas and fixtures are consistent
adapter output remains candidate
non-authority fields remain false
hash chain is structurally continuous
WORM receipt root matches ledger fixture
release bundle file hashes match current contents
unit tests pass
```

## 5. What Passing Does Not Mean

A pass does not mean:

```text
Ten'i has occurred
AI base model has transformed
raw output is true
proof authority exists
clinical authority exists
execution authority exists
```

## 6. Non-Authority Boundary

The full checks preserve:

```text
AI raw output is candidate, not authority.
Audit event is trace surface, not authority.
Hash chain proves structural continuity, not truth.
WORM receipt preserves trace, not authority.
Bundle manifest proves file-set integrity, not Ten'i occurrence.
CI pass does not grant execution authority.
```

## 7. Recommended Development Loop

```text
make append-only or tighten-only change
  -> run full checks locally
  -> inspect failures
  -> repair structural issue
  -> commit
  -> GitHub Actions runs the same chain
```

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
