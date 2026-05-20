# Physical Quantum Qi Motion Pipeline v0.1

## Status

This is an append-only integration layer connecting the existing evidence-bound `Physical Quantum Qi Runtime v0.1` classifier to `Physical Quantum Qi Dynamics Kernel v0.1`.

The purpose is to make the movement of Qi operationally grounded:

```text
physical_qi_packet
  -> evidence-bound validated_type
  -> licensed_dynamics_terms
  -> qi_motion_candidate
  -> observe_only routing
```

## Core principle

Qi does not move because a packet claims to be Qi. Qi movement is permitted only when the evidence-bound classifier produces a validated type, and that type licenses the corresponding motion terms.

```text
claimed_type != authority
validated_type == dynamics_license_source
```

## Pipeline stages

### Stage 1: Evidence-bound classification

The pipeline reads the same evidence fields used by `physical_quantum_qi_runtime_contract_v0_1`.

```text
NonQi
PreQi
ProtoQi
TransportableQi
CurvedQi
CurrentQi
PhysicalQi
FullPathQi
```

The classification remains evidence-bound and claim-independent.

### Stage 2: Dynamics license resolution

The resulting `validated_type` is passed into the dynamics kernel.

```text
validated_type -> LICENSED_TERMS_BY_TYPE[validated_type]
```

Unlicensed terms must be ignored even if they are numerically present.

### Stage 3: Motion candidate generation

The dynamics kernel produces:

```text
motion_status
motion_score
active_terms
ignored_terms
reason_codes
```

The output is a bounded motion candidate, not an execution order.

## FullPathQi meaning

`FullPathQi` is the first level where Qi may move as a history-bearing process. It licenses:

- `sk_fv_history_flow`
- `memory_kernel_backflow`
- `noise_kernel_diffusion`
- `observation_backaction_term`
- `noncommutative_order_correction`
- `path_measure_normalization_guard`

This is where the Qi implementation can represent non-Markovian memory and process-tensor-style temporal structure.

## Non-authority boundary

The pipeline must preserve:

```text
execution_authority = false
belief_commit_authority = false
memory_overwrite_authority = false
world_root_rewrite_authority = false
safety_override_authority = false
direct_execution_allowed = false
authority_expansion = false
observe_only = true
```

## Fail-closed rule

The pipeline returns HOLD or BLOCKED if:

- classification rejects the packet
- required evidence is missing for the selected dynamics level
- authority expansion is attempted
- direct execution is requested
- unresolved blockers are present
- the validated type is unknown

## Why this matters

Before this pipeline, KuuOS could classify Physical Quantum Qi evidence. With this pipeline, KuuOS can also explain what kind of movement is licensed by that evidence.

Thus the operational root becomes:

```text
evidence -> validated_type -> licensed dynamics -> bounded movement
```
