# KuuOS workflow index

This file records the canonical GitHub Actions entry points and the consolidation rules used for `.github/workflows`.

## Validation boundary

```text
local change != global re-audit
receipt preservation != repeated execution
validation != truth
CI pass != theorem authority
selection optimization != authority expansion
sharding != authority expansion
```

The selector and shard scheduler change when checks are recomputed.

They do not expand execution authority, theorem authority, release authority, institutional authority, or truth claims.

Unknown or unmapped impact fails closed to the full audit set.

## Pull request gate

`pr-governance-gate.yml` is the single canonical pull-request entry point.

It reads `ci/check_registry.yaml`, computes changed-path impact and dependency closure, expands sharded checks, runs independent Python checks with bounded parallelism, runs Lean only when selected, and publishes one audit report.

Outputs are:

- `audit-summary.json`
- `audit-report.md`
- one `receipt.json` and `check.log` for each concrete check or shard

## Full audit v0.2

`all_governance_sharded_v0_2.yml` is the canonical post-merge Full Audit workflow.

It runs on relevant pushes to `main`, by manual dispatch, or as a reusable workflow.

The repository-wide command inventory remains in `scripts/run_all_governance_full_checks_v0_1.py`.

`scripts/run_all_governance_shard_v0_2.py` partitions that inventory deterministically into eight round-robin shards.

At most four shards run concurrently.

Each shard continues after an individual validator failure and records all visible failures in its receipt and command summary.

`all_governance_validation.yml` remains the stable manual Actions URL and delegates to the sharded workflow.

## Main integration validation

Subsystem workflows run on relevant pushes to `main` and by manual dispatch.

They preserve stable workflow URLs and integration diagnostics without duplicating pull-request execution.

Regge Zero governance remains available through `regge_zero_governance_validation.yml` on relevant `main` changes and manual dispatch.

Its Pull Request coverage is provided by the registered `regge-zero` check in the central gate.

## Canonical workflows

| Workflow | Pull request | Main or manual responsibility |
| --- | --- | --- |
| `pr-governance-gate.yml` | Canonical impact-selected gate | Manual comparison run |
| `all_governance_sharded_v0_2.yml` | Full Audit shards selected through the gate | Canonical post-merge and reusable Full Audit |
| `all_governance_validation.yml` | No direct trigger | Stable manual URL delegating to sharded Full Audit |
| `core_governance_validation.yml` | Selected through the gate | Stable manual Core Governance entry point |
| `regge_zero_governance_validation.yml` | Selected as `regge-zero` through the gate | Regge Zero integration validation on `main` or manual dispatch |
| `kuuos_runtime_full_check.yml` | Selected through the gate | Cumulative runtime regression on `main` or manual dispatch |
| `lean-formal-validation.yml` | Selected through the gate | Aggregate strict Lean validation on `main` or manual dispatch |
| `decision-os-validation.yml` | Selected through the gate | DecisionOS cumulative validation on `main` or manual dispatch |
| `evidence-cycle-os-validation.yml` | Selected through the gate | Evidence Cycle OS cumulative validation on `main` or manual dispatch |
| `plan-os-validation.yml` | Selected through the gate | PlanOS cumulative validation on `main` or manual dispatch |
| `world-v053-v059-main-validation.yml` | Retained scoped behavior | Integrated WORLD strict validation |
| `world-four-great-phase-dynamics-v0-59.yml` | Retained scoped behavior | Stable WORLD Four-Great validation entry point |

## Check registry

`ci/check_registry.yaml` is JSON encoded inside a YAML-compatible file so selection remains standard-library only.

Each check declares:

- stable identifier
- runner and command
- subsystem group and audit tier
- changed-path patterns
- dependencies
- pull-request-only duplicate suppression
- timeout metadata
- Full Audit membership

A `python-sharded` entry also declares `shard_count` and a command template containing `{index}` and `{count}`.

The selector expands the parent entry into concrete receipt identities such as `full-governance-00` through `full-governance-07`.

`pr_supersedes` is applied only to ordinary Pull Requests.

It is not applied during Full Audit.

## Integrity guard

`scripts/check_workflow_consolidation_integrity.py` verifies:

- canonical workflows, runners, registry, selector, summary builders, and tests exist
- superseded files remain deleted
- registered commands and dependency targets resolve
- sharded command templates and positive shard counts are valid
- fail-closed and non-authority markers remain present
- migrated workflows do not regain independent `pull_request` triggers
- workflow references resolve

Ordinary Pull Requests scan changed files and canonical control files.

Full Audit scans the complete repository.

## Retention rule

A separate workflow is retained only when it provides a capability not preserved by the Pull Request gate:

- release, deployment, Pages, or publication authority
- unique strict Lean or environment-specific execution
- required generated artifacts or diagnostic packets
- scheduled or post-merge integration operation
- a stable externally referenced Actions URL

A retained workflow must not duplicate Pull Request execution already represented in the registry.

## Consolidation rule

1. Use `pr-governance-gate.yml` as the single canonical Pull Request gate.
2. Use one registry entry per independently auditable check surface.
3. Expand large independent inventories into deterministic bounded shards.
4. Put version lists and sequential validation logic in `scripts/`, not duplicated YAML.
5. Continue independent checks after failure and aggregate all visible failures.
6. Preserve diagnostic logs and emit standardized receipts.
7. Keep stable external workflow URLs as integration or manual entry points.
8. Treat unknown paths, unmapped paths, diff failures, and audit-control changes as Full Audit.
9. Never interpret a green check as truth, theorem acceptance, institutional approval, or unrestricted execution authority.

## Naming convention

- Pull Request gate: `pr-governance-gate.yml`
- sharded Full Audit: `all_governance_sharded_v0_2.yml`
- cumulative subsystem workflow: `<subsystem>-validation.yml`
- cumulative runner: `run_<subsystem>_full_checks.py`
- shard runner: `run_<scope>_shard_<version>.py`
- retained stable workflow: retain the externally referenced filename and document its trigger scope
