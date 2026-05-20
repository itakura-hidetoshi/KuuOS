# Physical Quantum Qi Dynamics Kernel v0.1

## Status

This is an append-only dynamics layer for the KuuOS Qi implementation.

`Physical Quantum Qi Runtime v0.1` classifies a packet from `NonQi` to `FullPathQi` by evidence. This kernel explains and implements what that classification permits dynamically: each validated Qi type licenses a bounded set of motion terms. The validated type is therefore not just a label; it is a dynamics license.

## Core principle

Qi movement is not inferred from a claimed type. Qi movement is grounded by the evidence-bound validated type.

```text
validated_type
  -> licensed_dynamics_terms
  -> bounded Qi motion candidate
  -> observe_only routing surface
```

The dynamics kernel grants no execution authority, no belief commit authority, no memory overwrite authority, no world-root rewrite authority, no standalone diagnosis authority, no standalone treatment authorization, and no medical act authorization.

## Dynamics ladder

### NonQi

No Qi motion is licensed.

```text
licensed_terms = []
```

### PreQi

Only pre-organization is visible. Transport is not licensed.

```text
licensed_terms = [pre_organization]
```

### ProtoQi

A gauge connection is present, so local connection-sensitive tendency can be observed. Curvature transport is not yet licensed.

```text
licensed_terms = [pre_organization, gauge_connection_tendency]
```

### TransportableQi

Curvature or Wilson-loop residue is present, so path-dependent transport can be observed.

```text
licensed_terms = [pre_organization, gauge_connection_tendency, curvature_transport]
```

### CurvedQi

A Qi current is present, so current-coupled local flow can be observed.

```text
licensed_terms = [pre_organization, gauge_connection_tendency, curvature_transport, current_flow]
```

### CurrentQi

Ward/leak identity is present, so continuity/leak balance can be observed.

```text
licensed_terms = [pre_organization, gauge_connection_tendency, curvature_transport, current_flow, ward_leak_balance]
```

### PhysicalQi

Density state, Hamiltonian, Lindblad generator, entropy production, free energy, DPI gap, recovery margin, and mass-gap floor evidence are present. The kernel may use open-system physical motion terms.

```text
licensed_terms = [
  pre_organization,
  gauge_connection_tendency,
  curvature_transport,
  current_flow,
  ward_leak_balance,
  open_quantum_state_drift,
  entropy_free_energy_gradient,
  dpi_recovery_constraint,
  mass_gap_floor_stabilizer
]
```

### FullPathQi

Schwinger-Keldysh plus/minus branches, Feynman-Vernon influence functional, memory kernel, noise kernel, observation backaction, noncommutative operation history, and path-measure normalization are present. The kernel may use history-bearing non-Markov/process-tensor-style motion terms.

```text
licensed_terms = [
  pre_organization,
  gauge_connection_tendency,
  curvature_transport,
  current_flow,
  ward_leak_balance,
  open_quantum_state_drift,
  entropy_free_energy_gradient,
  dpi_recovery_constraint,
  mass_gap_floor_stabilizer,
  sk_fv_history_flow,
  memory_kernel_backflow,
  noise_kernel_diffusion,
  observation_backaction_term,
  noncommutative_order_correction,
  path_measure_normalization_guard
]
```

## Minimal scalar surrogate

The reference implementation uses a deliberately small scalar surrogate to make the dynamics testable without external dependencies.

```text
motion_score = base_flow
             + gauge_connection_tendency
             + curvature_transport
             + current_flow
             + ward_leak_balance
             + open_quantum_state_drift
             + entropy_free_energy_gradient
             + dpi_recovery_constraint
             + mass_gap_floor_stabilizer
             + sk_fv_history_flow
             + memory_kernel_backflow
             + noise_kernel_diffusion
             + observation_backaction_term
             + noncommutative_order_correction
             - path_measure_normalization_guard_penalty
```

Only terms licensed by `validated_type` may contribute. Unlicensed terms must be ignored even if numerical fields are present.

## Why this grounds the movement of Qi

The classifier says which evidence exists. The dynamics kernel converts that evidence into allowed motion operators.

- Gauge evidence grounds connection-sensitive movement.
- Curvature and Wilson-loop evidence ground path dependence.
- Current evidence grounds local flow.
- Ward/leak identity grounds continuity with leakage.
- Open-system evidence grounds Hamiltonian/Lindblad/free-energy/recovery dynamics.
- SK/FV/process-history evidence grounds non-Markov memory, noise, backaction, and noncommutative order dependence.

Thus, `FullPathQi` is the first level where Qi can move as a history-bearing process rather than a merely local current.

## Fail-closed constraints

The kernel returns HOLD or BLOCKED if:

- the validated type is unknown
- authority expansion is attempted
- direct execution is requested
- unresolved blockers are present
- required evidence for the selected type is missing
- the path measure is marked unnormalized for FullPathQi

## Non-authority boundary

Even when the motion status is `qi_motion_candidate_ready`, the output remains observe-only.

```text
direct_execution_allowed = false
authority_expansion = false
observe_only = true
standalone_diagnosis_authority = false
standalone_treatment_authorization = false
medical_act_authorization = false
```

## Medical-modality-neutral boundary

The dynamics kernel must preserve:

```text
medical_modality_neutral = true
qi_denied_by_boundary = false
east_asian_medical_reasoning_denied = false
biomedicine_privileged_by_wording = false
professional_judgment_required = true
patient_context_required = true
```

This keeps the dynamics decision usable as structured observation and reasoning support while preventing it from becoming standalone diagnosis, standalone treatment authorization, or medical act authorization. It does not deny Qi, does not invalidate East Asian medical reasoning, and does not privilege biomedicine by wording.