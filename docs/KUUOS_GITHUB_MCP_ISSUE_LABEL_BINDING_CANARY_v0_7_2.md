# KuuOS GitHub MCP Issue–Label Binding Canary v0.7.2

v0.7.2 preserves the v0.7 cross-resource transaction and adds an explicit GitHub repository-label name bound.

## Completed live evidence that required this patch

The v0.7.1 live request Issue #1361 was bound to exact `main` SHA `0c4c93dd96b310b7f16f95a16eb5ab1c36609263` and nonce `binding-v07-887dc1eaafb2ec40`.

The official MCP sequence successfully verified:

- exact owner request Issue identity,
- initially empty Issue label set,
- nonce repository-label absence.

`label_write(method=create)` then returned `Name is too long (maximum is 50 characters)`. The run completed as `KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_COMPENSATED`; the Issue label set was reobserved empty and the repository label was reobserved absent. No residual resource remained.

## Bounded label-name contract

v0.7.2 uses the fixed prefix:

`kuuos-mcp-bind-`

The request nonce remains restricted to 8–32 ASCII letters, digits, or hyphens. Therefore:

- prefix length: 15,
- maximum nonce length: 32,
- maximum generated label-name length: 47,
- GitHub maximum: 50.

The runtime blocks any plan whose generated label name exceeds 50 characters. The merged v0.7 workflow plan is normalized to the bounded prefix before the existing plan validator and transaction run, and the normalized plan is written into the evidence artifact.

## Unchanged authority boundary

The patch does not weaken the v0.7 transaction:

1. exact owner request Issue identity is reobserved,
2. initial Issue label set must be empty,
3. repository label must be absent,
4. the bounded label is created and reobserved exactly,
5. it is attached and reobserved as the exact singleton Issue label set,
6. it is detached and the Issue label set is reobserved empty,
7. the repository label is deleted and reobserved absent.

Compensation remains a non-success closeout. Preexisting Issue labels and repository labels remain non-destructive blockers. The GitHub token is never serialized.
