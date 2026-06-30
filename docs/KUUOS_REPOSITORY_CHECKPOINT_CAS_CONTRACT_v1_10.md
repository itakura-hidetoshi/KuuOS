# KuuOS Repository Checkpoint CAS Contract v1.10

## Purpose

v1.10 defines the smallest safe interface boundary between a confirmed v1.09 checkpoint candidate and any future checkpoint update adapter.

It is a specification layer only. It does not grant repository-change authority, invoke Git, or mutate a reference.

## Outcomes

- `CHECKPOINT_CAS_CONTRACT_READY`: the candidate is valid at the v1.10 trust boundary, the repository and checkpoint binding are exact, and a separate observation equals the expected current OID.
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

## Candidate trust boundary

v1.10 verifies the immutable candidate digest and local candidate invariants. It does not replay the complete v1.06 through v1.09 derivation chain.

This limitation is safe within v1.10 because the contract remains nonauthorizing and nonexecuting. A separate v1.11 validation receipt will perform complete upstream candidate revalidation before any future adapter or authorization layer may consume the contract.

## Formal claims

The Lean model proves that:

- a ready contract is checkpoint-only and nonexecuting;
- a ready contract has distinct nonzero expected and proposed OIDs;
- a conflict never requests compare-and-swap;
- identical inputs derive identical contracts.
