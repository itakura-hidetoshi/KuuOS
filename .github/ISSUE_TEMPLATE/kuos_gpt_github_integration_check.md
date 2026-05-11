---
name: KuuOS GPT GitHub Integration Check
about: Check GPT-assisted GitHub interaction against KuuOS governance invariants
title: "[GPT-GitHub Integration]: "
labels: ["kuos", "gpt-github", "governance", "invariant"]
---

## Summary

Describe the repository interaction, PR, issue, CI failure, documentation change, or formal-surface question.

## Target Surface

```text
Repository:
Path or PR:
Related workflow or validator:
```

## Canonical Read Order

- [ ] README.md
- [ ] docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
- [ ] docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
- [ ] docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
- [ ] docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md when formal or proof-facing

## Invariant Surface

- [ ] fourfold core preserved
- [ ] two truths gap preserved
- [ ] Middle Way preserved
- [ ] AI raw output remains candidate, not authority
- [ ] non-authority boundary preserved
- [ ] Dukkha visibility preserved
- [ ] Qi language does not hide harm
- [ ] Mandala center is not replaced by a WORLD
- [ ] Paramita orientation is not action authorization
- [ ] validation pass is not treated as truth
- [ ] CI pass is not treated as execution authority
- [ ] append-only / tighten-only release mode preserved

## GPT Non-Authority Fixed Points

- [ ] GPT_reading_not_authority
- [ ] GPT_summary_not_authority
- [ ] GPT_review_not_authority
- [ ] GPT_issue_draft_not_authority
- [ ] GPT_PR_draft_not_authority
- [ ] GPT_CI_interpretation_not_authority
- [ ] ci_pass_not_execution_authority

## Validation

Run when applicable:

```bash
make gpt-github-integration-checks
make all-governance-checks
```

Expected GPT integration validator result:

```text
PASS: KuuOS GPT GitHub integration surface v0.1 validates
```

## GPT Review Request

```text
Review this issue under KuuOS GPT GitHub integration.
Classify it as PASS / HOLD / REPAIR / REJECT / QUARANTINE.
Cite the affected files and identify which invariants are touched.
```

## Proposed Classification

```text
PASS / HOLD / REPAIR / REJECT / QUARANTINE
```

## Notes

A GPT review, CI pass, or validator pass does not grant truth, proof, clinical authority, Ten'i, or execution authority.
