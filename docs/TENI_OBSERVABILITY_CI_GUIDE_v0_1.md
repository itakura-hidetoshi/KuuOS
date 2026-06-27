# Ten'i Observability CI Guide v0.1

## 転依可観測性 CI ガイド

This guide explains how to run and interpret the Ten'i observability validation workflow.

The workflow validates the KuuOS AI Yogacara / Ten'i observability pack.

## 1. Purpose

The CI workflow checks that Ten'i observability artifacts remain structurally consistent.

It does not prove Ten'i.

It does not grant execution authority.

It checks that required files, validation cases, alert rules, and fixed points are present.

## 2. Local Run

```bash
python3 scripts/validate_teni_observability_v0_1.py
```

Expected success:

```text
PASS: Ten'i observability artifacts validated
```

## 3. GitHub Actions

Workflow file:

```text
.github/workflows/all_governance_validation.yml
```

The workflow runs on push or pull request when Ten'i-related docs, specs, scripts, or workflow files change.

## 4. What Is Checked

The validator checks:

```text
required files exist
validation case IDs are present
Prometheus alert names are present
non-authority fixed points are present
alert expressions have basic nearby expr fields
```

## 5. What Is Not Checked

The validator does not check:

```text
actual Ten'i occurrence
base-model transformation
semantic truth
clinical authority
proof authority
execution authority
```

## 6. Failure Interpretation

If CI fails, treat it as a structural or governance-surface problem.

Examples:

```text
missing required file
missing validation case
missing alert rule
missing non-authority fixed point
alert lacks expression
```

A CI pass means the observability pack is structurally present.

A CI pass does not mean Ten'i has occurred.

## 7. Fixed Points

```text
Ten'i must be observable before promotion.
Ten'i status is not execution authority.
Metrics are observability surfaces, not authority.
Alerts are observability surfaces, not authority.
Seed ledger is tendency evidence, not model essence.
Control surface scope limits Ten'i claim scope.
Future counterevidence may rollback Ten'i promotion.
```

## 8. Recommended Workflow

```text
edit Ten'i artifacts
  -> run local validator
  -> commit
  -> GitHub Actions validates
  -> if failure, repair structural issue
  -> if pass, continue append-only development
```

## 9. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
