# KuuOS workflow index

This file records the canonical GitHub Actions entry points and the consolidation rules used for `.github/workflows`.

## Canonical consolidated workflows

| Workflow | Responsibility |
| --- | --- |
| `all_governance_validation.yml` | Top-level governance, AI Yogacara, core governance, Physical Quantum Qi, and audit-chain checks |
| `kuuos_runtime_full_check.yml` | Cumulative KuuOS runtime and unit-test regression |
| `lean-formal-validation.yml` | Aggregate strict Lean validation |
| `decision-os-validation.yml` | DecisionOS v0.1-v0.3 matrix validation with per-version logs |
| `evidence-cycle-os-validation.yml` | ActOS, ObserveOS, VerifyOS, and LearnOS matrix validation with per-component logs |
| `plan-os-validation.yml` | PlanOS v0.1-v0.17 validation through `scripts/run_plan_os_full_checks_v0_17.py` |
| `world-v053-v059-main-validation.yml` | Integrated WORLD validation for the current formal series |

## Retention rule

A separate workflow is retained only when it provides at least one capability not preserved by a consolidated workflow:

- release, deployment, Pages, or publication authority
- unique unit-test coverage
- unique strict Lean target coverage
- required generated artifacts or diagnostic packets
- environment-specific or scheduled operation

## Consolidation rule

1. Use one workflow per subsystem family.
2. Put version lists and sequential validation logic in `scripts/`, not duplicated YAML.
3. Use a matrix for independent variants that should remain isolated and parallel.
4. Preserve diagnostic logs when old workflows uploaded them.
5. Prefer stable filenames without a terminal version number for cumulative workflows.
6. Delete superseded workflow files immediately after their validation paths are migrated.

## Naming convention

- cumulative subsystem workflow: `<subsystem>-validation.yml`
- repository-wide regression: `<scope>-full-check.yml`
- release or deployment workflow: retain the explicit release or deployment name
- temporary diagnostic workflow: never commit permanently
