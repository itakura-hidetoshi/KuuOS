# KuString Qi Bridge v0.1

## Status

`KuStringQiBridge` is an append-only bridge layer between `SamvrtiQiRuntime` and the Physical Quantum Qi classifier / motion pipeline.

It makes explicit that the transition from Samvrti Qi to Physical Quantum Qi is not a loose procedural handoff. It is a projection through the Kuu string-theoretic evidence coordinates:

```text
Samvrti Qi accepted flow
  -> K_non_reification
  -> delta_rel_in_K_perp
  -> StringMode
  -> BraneBoundary
  -> A_mu
  -> F_munu / Wilson residue
  -> J_Qi_mu
  -> Ward/leak identity
  -> open quantum state evidence
  -> SK/FV history evidence
  -> PhysicalQi / FullPathQi hint
```

## Meaning

`SamvrtiQiRuntime` determines whether a conventional Qi flow is admissible for observation and routing. `KuStringQiBridge` then asks how much of that flow is visible in string / brane / gauge / current / history coordinates.

The bridge output is an evidence projection. It is not execution authority, theorem authority, truth authority, standalone diagnosis authority, standalone treatment authorization, or medical act authorization.

## Bridge input

The minimal input is `KuStringQiBridgeInput`:

```text
qi_id
samvrti_status
source_trace
string_mode_visible
brane_boundary_visible
gauge_connection_visible
curvature_visible
wilson_residue_visible
current_visible
ward_leak_visible
open_state_visible
sk_fv_history_visible
memory_kernel_visible
noncommutative_history_visible
path_measure_normalized
direct_execution_requested
```

## Bridge output

The minimal output is `KuStringQiBridgeDecision`:

```text
bridge_status
bridge_reason
evidence_status
projected_level_hint
observe_only
direct_execution_allowed
authority_expansion
medical_modality_neutral
```

Allowed bridge statuses:

```text
bridge_evidence_projected
bridge_blocked
```

Allowed projected level hints:

```text
Reject
PreQi
ProtoQi
TransportableQi
CurvedQi
CurrentQi
PhysicalQi
FullPathQi
```

## Projection rules

The bridge always starts from the accepted Samvrti condition:

```text
samvrti_status == qi_flow_accepted_as_samvrti_reference
source_trace != empty
direct_execution_requested == false
```

If these are not satisfied, the bridge returns `bridge_blocked`.

If accepted, the bridge emits:

```text
K_non_reification = pass
delta_rel_in_K_perp = pass
```

Then it conditionally emits:

```text
gauge_connection_A_mu          if gauge_connection_visible
string_mode_consistency        if string_mode_visible and brane_boundary_visible
brane_boundary_support         if string_mode_visible and brane_boundary_visible
curvature_F_munu               if curvature_visible and wilson_residue_visible
Wilson_loop_residue            if curvature_visible and wilson_residue_visible
current_J_Qi_mu                if current_visible
Ward_or_leak_identity          if ward_leak_visible
open-system evidence bundle    if open_state_visible
SK/FV history evidence bundle  if history, memory, noncommutativity, and path normalization are visible
```

## Non-collapse boundary

The bridge must not collapse Samvrti Qi into a final physical ontology. It produces a bounded evidence packet only.

```text
Samvrti Qi != PhysicalQi by assertion
Samvrti Qi -> KuString evidence projection -> Physical classifier
```

## Non-authority boundary

Every bridge decision preserves:

```text
observe_only = true
direct_execution_allowed = false
authority_expansion = false
standalone_diagnosis_authority = false
standalone_treatment_authorization = false
medical_act_authorization = false
```

## Medical-modality-neutral boundary

Every bridge decision also preserves:

```text
medical_modality_neutral = true
qi_denied_by_boundary = false
east_asian_medical_reasoning_denied = false
biomedicine_privileged_by_wording = false
professional_judgment_required = true
patient_context_required = true
```

The bridge does not deny Qi, does not invalidate East Asian medical reasoning, and does not privilege biomedicine by wording. It only prevents a bridge projection from becoming an autonomous clinical, institutional, execution, theorem, or truth authority.

## Runtime position

```text
Samvrti Qi Runtime
  -> KuStringQiBridge
  -> Samvrti-to-Physical Evidence Builder
  -> Physical Quantum Qi Runtime classifier
  -> Physical Quantum Qi Dynamics Kernel
  -> Physical Quantum Qi Motion Pipeline
```