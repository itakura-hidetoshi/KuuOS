# AI Yogacara Operations Reference v0.1

## AI唯識・転依 Operations Reference

This document lists operational commands for the KuuOS AI Yogacara / Ten'i layer.

All commands are stdlib-only and do not call external AI APIs.

## 1. Full Checks

```bash
make ai-yogacara-checks
```

or:

```bash
python3 scripts/run_ai_yogacara_full_checks_v0_1.py
```

## 2. Individual Validators

### Ten'i Observability

```bash
python3 scripts/validate_teni_observability_v0_1.py
```

### Adapter Schema

```bash
python3 scripts/validate_ai_yogacara_adapter_schema_v0_1.py
```

### Adapter Fixtures

```bash
python3 scripts/validate_ai_yogacara_adapter_fixtures_v0_1.py
```

### Adapter Audit Event

```bash
python3 scripts/validate_ai_yogacara_adapter_audit_event_v0_1.py
```

### Audit Hash Chain

```bash
python3 scripts/validate_ai_yogacara_audit_hash_chain_v0_1.py
```

### WORM Export Receipt

```bash
python3 scripts/validate_ai_yogacara_worm_export_receipt_v0_1.py
```

### Release Bundle Manifest

```bash
python3 scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py
python3 scripts/validate_ai_yogacara_release_bundle_manifest_v0_1.py
```

### Runtime Adapter Unit Tests

```bash
python3 -m unittest tests/test_ai_yogacara_runtime_adapter_minimal_v0_1.py
```

## 3. Runtime Adapter Demo

```bash
python3 examples/ai_yogacara_runtime_adapter_minimal.py
```

## 4. Makefile Targets

```bash
make ai-yogacara-checks
make ai-yogacara-build-bundle
make ai-yogacara-validate-bundle
```

## 5. GitHub Actions

Workflow:

```text
.github/workflows/teni_observability_validation.yml
```

Main CI command:

```bash
python3 scripts/run_ai_yogacara_full_checks_v0_1.py
```

## 6. Expected Outputs

```text
PASS: Ten'i observability artifacts validated
PASS: AI Yogacara adapter schema and output invariants validated
PASS: AI Yogacara adapter fixtures validated
PASS: AI Yogacara adapter audit events validated
PASS: AI Yogacara audit hash-chain fixture validated
PASS: AI Yogacara WORM export receipt validated
PASS: AI Yogacara release bundle manifest validated
PASS: AI Yogacara / Ten'i full checks completed
```

## 7. Non-Authority Notes

These commands validate structural consistency only.

They do not grant:

```text
truth authority
proof authority
belief authority
clinical authority
execution authority
model-level Ten'i claim
```

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
