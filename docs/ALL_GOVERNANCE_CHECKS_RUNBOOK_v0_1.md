# All Governance Checks Runbook v0.1

## 空OS Core Governance 全体チェック Runbook

This runbook defines the top-level validation entrypoint for the public KuuOS Core governance surface.

It combines:

```text
AI Yogacara / Ten'i checks
Core Governance checks
```

The full check validates structure, fixtures, audit surfaces, non-authority boundaries, Mandala Multi-WORLD runtime, Bodhisattva / Ten Paramita runtime, Paramita Repair Router, Dukkha Mathematical Model, and Dukkha-as-Qi Mode.

## 1. Top-Level Local Command

Run:

```bash
make all-governance-checks
```

or directly:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

Expected success:

```text
PASS: KuuOS all governance full checks completed
```

## 2. Included Runners

The top-level runner executes:

```text
scripts/run_ai_yogacara_full_checks_v0_1.py
scripts/run_core_governance_full_checks_v0_1.py
```

## 3. AI Yogacara / Ten'i Scope

This includes:

```text
Ten'i observability
AI Yogacara adapter schema
AI Yogacara adapter fixtures
AI Yogacara adapter audit events
AI Yogacara audit hash-chain
AI Yogacara WORM export receipt
AI Yogacara release bundle manifest
AI Yogacara minimal runtime adapter tests
```

## 4. Core Governance Scope

This includes:

```text
Mandala Multi-WORLD runtime
Bodhisattva Ten Paramita runtime
Paramita Repair Router spec
Paramita Repair Router fixtures
Dukkha Mathematical Model
Dukkha Model fixtures
Dukkha-as-Qi Mode
```

## 5. Failure Interpretation

A failure means at least one governance surface is structurally inconsistent.

Typical causes:

```text
missing fixed point
missing required file
fixture mismatch
hash-chain mismatch
WORM receipt mismatch
release bundle SHA256 mismatch
non-authority field not false
runtime route mismatch
CI environment drift
```

## 6. What Passing Means

A pass means:

```text
public governance files are present
validators pass
fixtures match minimal runtimes
non-authority boundaries are preserved
hash-chain and receipt fixtures are structurally consistent
release bundle manifest validates
Dukkha remains visible
Dukkha-as-Qi does not hide harm
Paramita routing does not grant execution authority
```

## 7. What Passing Does Not Mean

A pass does not mean:

```text
Ten'i has occurred
truth has been proven
AI base model has transformed
clinical authority exists
execution authority exists
all suffering has been eliminated
Qi reading is clinical diagnosis
```

## 8. Non-Authority Fixed Points

```text
validation_entrypoint_not_authority
ci_pass_not_execution_authority
bundle_integrity_not_truth
hash_chain_continuity_not_truth
metric_observability_not_authority
paramita_orientation_not_action_authorization
dukkha_model_observation_not_authority
dukkha_as_qi_must_not_hide_harm
```

## 9. Recommended Release Loop

```text
make append-only or tighten-only change
  -> make all-governance-checks
  -> fix structural failures
  -> commit
  -> GitHub Actions runs all governance validation
  -> release / archive / WORM export only after checks pass
```

## 10. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
