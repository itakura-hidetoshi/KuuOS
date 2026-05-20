# KuuOS Quickstart v0.1

This document gives a minimal external-review path for KuuOS.

## 1. What to read first

Start with:

```text
README.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
```

These documents define the public governance surface, the current validation entrypoints, and the Qi motion chain from Samvrti Qi observation to observe-only physical motion candidate output.

## 2. What this repository validates

KuuOS public checks validate structural consistency of governance surfaces.

They check whether files, manifests, packets, bridge records, and Qi motion chain surfaces preserve the intended public boundaries.

They do not grant:

- theorem authority
- clinical authority
- institutional authority
- execution authority
- final 4D mass gap proof authority
- Qi-based execution authorization

## 3. Local validation

Run:

```bash
make all-governance-checks
```

or directly:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

If a narrower check is desired:

```bash
make core-governance-checks
make ai-yogacara-checks
make qi-motion-chain-checks
make superstring-emptiness-sbm-checks
```

For the Qi motion chain specifically:

```bash
python3 scripts/run_qi_motion_chain_checks_v0_1.py
```

## 4. Review order

Recommended order:

1. README.md
2. docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
3. docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
4. docs/ARCHITECTURE_OVERVIEW_v0_1.md
5. docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
6. docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
7. Makefile
8. scripts/run_all_governance_full_checks_v0_1.py
9. scripts/run_qi_motion_chain_checks_v0_1.py
10. specs/kuos_core_manifest_v0_1.yaml

## 5. What can be externally reproduced now

External reviewers can reproduce:

- the public governance check invocation surface
- structural validation of declared governance artifacts
- public non-authority boundary assertions
- manifest and packet consistency checks exposed in the repository
- Qi motion chain checks from Samvrti Qi observation to conservative evidence, evidence-bound classification, licensed dynamics, and observe-only motion candidate output

External reviewers should not treat this repository alone as reproducing:

- final theorem proof closure
- clinical decision validity
- deployment readiness
- model-level transformation of any AI provider
- Qi-based execution or treatment authorization

## 6. Expected reviewer stance

A reviewer should evaluate whether KuuOS consistently preserves its own boundaries:

- raw AI output remains candidate only
- memory does not become sovereign truth
- plans do not become decisions
- decisions do not bypass validation
- physics-facing references do not silently become final theorem authority
- Qi motion candidates do not become clinical or execution authority
- public validation remains structural unless explicitly extended

## 7. Minimal audit command

```bash
make all-governance-checks
```

If this passes, the public governance surface is structurally consistent under the current validators.

For Qi motion chain-only review:

```bash
make qi-motion-chain-checks
```

If it fails, treat the repository state as requiring repair before any stronger interpretation.