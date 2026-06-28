# KuuOS workflow index

This file records the canonical GitHub Actions entry points and the consolidation rules used for `.github/workflows`.

## Validation boundary

```text
local change != global re-audit
receipt preservation != repeated execution
validation != truth
CI pass != theorem authority
selection optimization != authority expansion
```

The impact selector changes when checks are recomputed.

It does not expand execution authority, theorem authority, release authority, institutional authority, or truth claims.

Unknown or unmapped impact fails closed to the full audit set.

## Execution tiers

### Pull request gate

`pr-governance-gate.yml` is the single canonical pull-request entry point.

It reads `ci/check_registry.yaml`, computes the changed-path impact set and transitive dependency closure, runs independent Python checks with bounded parallelism, runs Lean only when selected, and publishes one audit report.

The machine-readable and human-readable outputs are:

- `audit-summary.json`
- `audit-report.md`
- one `receipt.json` and `check.log` for each selected check

### Main integration validation

Subsystem workflows run on relevant pushes to `main` and by manual dispatch.

They preserve stable workflow URLs and integration-level diagnostics without duplicating pull-request execution.

### Full audit

`all_governance_validation.yml` runs on relevant pushes to `main` and by manual dispatch.

It retains the repository-wide governance runner and forces a complete workflow-reference scan.

Changes to the selector, registry, audit runner, audit summary, pull-request gate, full-audit workflow, workflow index, or Makefile require the full audit set on the pull request.

## Canonical workflows

| Workflow | Pull request | Main or manual responsibility |
| --- | --- | --- |
| `pr-governance-gate.yml` | Canonical impact-selected gate | Manual comparison run is also available |
| `all_governance_validation.yml` | No direct trigger | Repository-wide governance and complete workflow-reference audit |
| `core_governance_validation.yml` | No direct trigger | Stable manual Core Governance entry point |
| `kuuos_runtime_full_check.yml` | Selected through the PR gate | Cumulative runtime regression on `main` or manual dispatch |
| `lean-formal-validation.yml` | Selected through the PR gate | Aggregate strict Lean validation on `main` or manual dispatch |
| `decision-os-validation.yml` | Selected through the PR gate | DecisionOS v0.1-v0.4 cumulative validation on `main` or manual dispatch |
| `evidence-cycle-os-validation.yml` | Selected through the PR gate | ActOS, ObserveOS, VerifyOS, and LearnOS cumulative validation on `main` or manual dispatch |
| `plan-os-validation.yml` | Selected through the PR gate | PlanOS v0.1-v0.23 cumulative validation on `main` or manual dispatch |
| `world-v053-v059-main-validation.yml` | Retained scoped behavior | Integrated WORLD v0.53-v0.59 strict validation |
| `world-four-great-phase-dynamics-v0-59.yml` | Retained scoped behavior | Stable WORLD v0.59 Four-Great validation entry point |

## Check registry

`ci/check_registry.yaml` is JSON encoded inside a YAML-compatible file so the selector remains standard-library only.

Each check declares:

- stable check identifier
- runner and command
- subsystem group and audit tier
- changed-path patterns
- dependency checks
- pull-request-only duplicate suppression
- timeout metadata
- full-audit membership

`pr_supersedes` is applied only to ordinary pull requests.

It is not applied during Full Audit, so a local subsystem check can replace a broad runtime rerun on ordinary changes without reducing the full-audit surface.

## Integrity guard

`scripts/check_workflow_consolidation_integrity.py` verifies:

- canonical workflows, runners, registry, selector, summary builder, and tests exist
- superseded legacy files remain deleted
- registered commands and dependency targets resolve
- required fail-closed and non-authority markers remain present
- workflows migrated to the PR gate do not regain independent `pull_request` triggers
- workflow references resolve

Ordinary pull requests scan changed files and canonical control files.

Full Audit scans the complete repository.

## Retention rule

A separate workflow is retained only when it provides at least one capability not preserved by the pull-request gate:

- release, deployment, Pages, or publication authority
- unique strict Lean or environment-specific execution
- required generated artifacts or diagnostic packets
- scheduled or post-merge integration operation
- a stable externally referenced Actions URL

A retained stable workflow must not duplicate pull-request execution already represented in the registry.

## Consolidation rule

1. Use `pr-governance-gate.yml` as the single canonical pull-request gate.
2. Use one registry entry per independently auditable check surface.
3. Put version lists and sequential validation logic in `scripts/`, not duplicated YAML.
4. Use bounded matrices only for independent checks.
5. Preserve diagnostic logs and emit a standardized receipt.
6. Prefer stable filenames without a terminal version number for cumulative workflows.
7. Keep stable external workflow URLs as `main` or manual entry points when required.
8. Preserve both legacy underscore names and compact subsystem names in path patterns while both conventions exist.
9. Treat unknown paths, unmapped paths, diff failures, and audit-control changes as Full Audit.
10. Never interpret a green check as truth, theorem acceptance, institutional approval, or unrestricted execution authority.

## Naming convention

- pull-request gate: `pr-governance-gate.yml`
- cumulative subsystem workflow: `<subsystem>-validation.yml`
- repository-wide regression: `<scope>-full-check.yml`
- cumulative runner: `run_<subsystem>_full_checks.py`
- release or deployment workflow: retain the explicit release or deployment name
- retained stable workflow: retain the externally referenced filename and document its trigger scope
- temporary diagnostic workflow: never commit permanently
