# KuuOS workflow index

This file records the canonical GitHub Actions entry points and the consolidation rules used for `.github/workflows`.

## Canonical consolidated workflows

| Workflow | Responsibility |
| --- | --- |
| `all_governance_validation.yml` | Top-level governance checks and workflow-consolidation integrity audit |
| `core_governance_validation.yml` | Stable compatibility entry point for manual Core Governance validation; automatic execution is limited to changes to this workflow itself |
| `kuuos_runtime_full_check.yml` | Cumulative KuuOS runtime and unit-test regression |
| `lean-formal-validation.yml` | Aggregate strict Lean validation |
| `decision-os-validation.yml` | DecisionOS v0.1-v0.4 validation with per-version logs for v0.1-v0.3 |
| `evidence-cycle-os-validation.yml` | ActOS v0.1-v0.4, ObserveOS v0.1-v0.4, VerifyOS v0.1-v0.3, and LearnOS v0.1-v0.3 |
| `plan-os-validation.yml` | PlanOS v0.1-v0.23 through `scripts/run_plan_os_full_checks.py` |
| `world-v053-v059-main-validation.yml` | Integrated WORLD v0.53-v0.59 strict validation |

## Integrity guard

`scripts/check_workflow_consolidation_integrity.py` verifies that canonical workflows and the guarded Core Governance compatibility entry point exist, superseded files stay deleted, failure propagation remains enabled, and the migrated validation markers remain present.

## Retention rule

A separate workflow is retained only when it provides at least one capability not preserved by a consolidated workflow:

- release, deployment, Pages, or publication authority
- unique unit-test coverage
- unique strict Lean target coverage
- required generated artifacts or diagnostic packets
- environment-specific or scheduled operation
- a stable externally referenced Actions URL whose automatic triggers are restricted to avoid duplicate validation

## Consolidation rule

1. Use one workflow per subsystem family.
2. Put version lists and sequential validation logic in `scripts/`, not duplicated YAML.
3. Use a matrix for independent variants that should remain isolated and parallel.
4. Preserve diagnostic logs when old workflows uploaded them.
5. Prefer stable filenames without a terminal version number for cumulative workflows.
6. Delete superseded workflow files immediately after their validation paths are migrated, unless a guarded compatibility entry point is required to preserve a stable external URL.
7. Preserve both legacy underscore names and compact subsystem names in path filters while both conventions exist.
8. Use fail-fast shell settings when a step contains more than one validation command.
9. Restrict compatibility workflows to `workflow_dispatch` and self-path triggers so they do not duplicate canonical subsystem validation.

## Naming convention

- cumulative subsystem workflow: `<subsystem>-validation.yml`
- repository-wide regression: `<scope>-full-check.yml`
- cumulative runner: `run_<subsystem>_full_checks.py`
- release or deployment workflow: retain the explicit release or deployment name
- guarded compatibility workflow: retain the externally referenced stable filename and document its restricted triggers
- temporary diagnostic workflow: never commit permanently
