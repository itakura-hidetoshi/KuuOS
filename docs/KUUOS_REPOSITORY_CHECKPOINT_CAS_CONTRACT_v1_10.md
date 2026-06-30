# KuuOS Repository Checkpoint CAS Contract v1.10

## Purpose

v1.10 defines the smallest safe interface boundary between a confirmed v1.09 checkpoint candidate and any future checkpoint update adapter.

It is a specification layer only. It does not grant repository-change authority, invoke Git, or mutate a reference.

## Outcomes

- `CHECKPOINT_CAS_CONTRACT_READY`: the candidate is valid, the repository and checkpoint binding are exact, and a fresh observation equals the expected current OID.
- `CHECKPOINT_CAS_CONTRACT_CONFLICT`: the observed current OID is nonzero but differs from the expected current OID.
- `CHECKPOINT_CAS_CONTRACT_NONE`: no ready v1.09 candidate exists.
- `CHECKPOINT_CAS_CONTRACT_REJECTED`: evidence or policy validation failed.

## Safety boundary

A ready contract records that compare-and-swap would be required by a later adapter. It is not an authorization and it is not an attempted update.

Every outcome keeps these fields false:

- `repository_change_authority_granted`
- `execution_performed`
- `live_git_command_invoked`

The contract is restricted to the checkpoint namespace and does not reuse the v0.97 branch-only execution policy.

## Formal claims

The Lean model proves that:

- a ready contract is checkpoint-only and nonexecuting;
- a ready contract has distinct nonzero expected and proposed OIDs;
- a conflict never requests compare-and-swap;
- identical inputs derive identical contracts.
