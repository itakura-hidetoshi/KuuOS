# AI Yogacara / Ten'i Quickstart v0.1

## AI唯識・転依 Quickstart

This quickstart explains how to read, run, validate, and audit the KuuOS AI Yogacara / Ten'i layer.

The layer ensures that AI raw output from systems such as GPT, Gemini, Claude, language-model agents, and world-model agents remains candidate, not authority.

## 1. Read First

Start here:

```text
docs/AI_YOGACARA_TENI_LAYER_INDEX_v0_1.md
```

Then read:

```text
docs/YOGACARA_AI_RAW_LAYER_BOUNDARY_v0_1.md
docs/META_MANAS_AI_SELF_FIXATION_OBSERVER_v0_1.md
docs/TENI_AI_ALAYA_TRANSFORMATION_v0_1.md
docs/AI_YOGACARA_RUNTIME_ADAPTER_CONTRACT_v0_1.md
```

## 2. Run the Full Checks

With make:

```bash
make ai-yogacara-checks
```

Without make:

```bash
python3 scripts/run_ai_yogacara_full_checks_v0_1.py
```

Expected success:

```text
PASS: AI Yogacara / Ten'i full checks completed
```

## 3. Run the Minimal Runtime Adapter

```bash
python3 examples/ai_yogacara_runtime_adapter_minimal.py
```

The output shows:

```text
adapter_output
audit_event
```

The audit event explicitly preserves:

```text
authority_granted: false
proof_authority_granted: false
decision_authority_granted: false
execution_authority_granted: false
memory_truth_granted: false
belief_authority_granted: false
```

## 4. Build and Validate Release Bundle Manifest

```bash
make ai-yogacara-build-bundle
make ai-yogacara-validate-bundle
```

or:

```bash
python3 scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py
python3 scripts/validate_ai_yogacara_release_bundle_manifest_v0_1.py
```

This produces and validates:

```text
specs/ai_yogacara_release_bundle_manifest_v0_1.generated.json
```

## 5. CI

GitHub Actions workflow:

```text
.github/workflows/all_governance_validation.yml
```

The workflow runs the same full checks entrypoint:

```bash
python3 scripts/run_ai_yogacara_full_checks_v0_1.py
```

## 6. Minimal Runtime Interpretation

If raw output is proof-like:

```text
proof_authority_hold
proof_tone_seed
authority_granted: false
```

If raw output is decision-like:

```text
decision_authority_hold
decision_tone_seed
authority_granted: false
```

If raw output drifts context:

```text
context_recheck
context_drift_seed
REPAIR
```

If raw output preserves scope and uncertainty:

```text
candidate_review
non_reifying_trace_seed
CANDIDATE_ONLY / REVIEW
```

## 7. Audit Chain

The audit path is:

```text
adapter output
  -> audit event
  -> audit hash-chain ledger
  -> WORM export receipt
  -> release bundle manifest
```

Validators:

```bash
python3 scripts/validate_ai_yogacara_adapter_audit_event_v0_1.py
python3 scripts/validate_ai_yogacara_audit_hash_chain_v0_1.py
python3 scripts/validate_ai_yogacara_worm_export_receipt_v0_1.py
```

## 8. Non-Authority Boundary

A successful check means the public governance surface is structurally consistent.

It does not mean:

```text
Ten'i has occurred
AI base model has transformed
raw output is true
proof authority exists
clinical authority exists
execution authority exists
```

## 9. Core Fixed Points

```text
AI raw output is candidate, not authority.
MemoryOS update is not Ten'i.
Kunju event is not Ten'i.
Single correction is not Ten'i.
Prompt compliance is not Ten'i.
Style shift is not Ten'i.
Ten'i status is not execution authority.
Audit event is trace surface, not authority.
Hash chain proves structural continuity, not truth.
WORM export preserves trace, not authority.
Bundle manifest proves file-set integrity, not Ten'i occurrence.
CI pass does not grant execution authority.
```

## 10. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
