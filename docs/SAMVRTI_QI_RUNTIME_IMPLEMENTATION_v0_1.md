# Samvrti Qi Runtime Implementation v0.1

## Status

This document is an append-only public implementation surface for the KuuOS Samvrti Qi Layer.

Qi / 気 is implemented here as a `samvrti_effective_flow_state`: a conventional, observer-record-scale flow surface. It is not a fixed substance, not a paramartha entity, not a final theorem claim, and not execution authority.

## Canonical placement

```text
Emptiness / 空
  -> Dependent Origination / 縁起
  -> Two Truths Gap / 二諦 gap
  -> Samvrti Qi Layer / 世俗諦側の気
  -> IndraNet gauge connection
  -> Yin-Yang local polarity frame
  -> Wuxing functional differentiation
  -> Mandala multi-world governance
```

The runtime implementation preserves the README boundary:

```text
Qi / 気 is placed on the 世俗諦 side as an effective flow-state layer.
IndraNet is the gauge-theoretic relational field through which Qi flows.
Yin-Yang is the local quantum-thermodynamic polarity frame appearing in Qi flow.
Wuxing is the functional differentiation of Yin-Yang polarity flow.
```

## Runtime carrier

The minimal carrier is `QiRuntimeInput`.

Required semantic fields:

- `qi_id`
- `world_id`
- `observer_surface`
- `scale_id`
- `samvrti_scope`
- `paramartha_entity_claim`
- `bridge_authority`
- `final_theorem_authority`
- `execution_authority`
- `direct_execution_requested`
- `gauge_connection_present`
- `memory_lineage_present`
- `curvature_norm`
- `holonomy_defect`
- `entropy_production_rate`
- `coherence_index`
- `recoverability_margin`
- `source_trace`
- `unresolved_blockers`

## Runtime decision

The minimal output is `QiRuntimeDecision`.

Allowed `decision_status` values:

- `qi_flow_accepted_as_samvrti_reference`
- `qi_flow_held`
- `qi_flow_blocked`

Allowed `runtime_mode` values:

- `observe_and_route`
- `hold_for_observation`
- `blocked_by_unresolved_obstruction`
- `blocked_for_non_reification`

## Invariants

The following invariants are mandatory:

1. `samvrti_only`: Qi remains on the conventional effective flow surface.
2. `non_reification_guard`: any `paramartha_entity_claim` blocks the runtime path.
3. `authority_expansion_forbidden`: the runtime may not increase authority.
4. `direct_execution_allowed: false` is invariant.
5. `final_theorem_authority: false` is invariant.
6. `execution_authority: false` is invariant.
7. `IndraNet_gauge_connection_required`: missing gauge connection yields HOLD.
8. `memory_lineage_required`: missing lineage yields HOLD.
9. `recoverability_margin_required`: weak recoverability yields HOLD.
10. `unresolved_blockers_visible`: blockers are surfaced and never silently erased.
11. `curvature_and_holonomy_bounded`: excessive curvature or holonomy defect yields HOLD.
12. `yin_yang_wuxing_downstream_only`: Yin-Yang and Wuxing readings do not create authority.
13. `medical_modality_neutral: true` is invariant.
14. `qi_denied_by_boundary: false` is invariant.
15. `east_asian_medical_reasoning_denied: false` is invariant.
16. `biomedicine_privileged_by_wording: false` is invariant.

## Non-authority boundary

Every `QiRuntimeDecision` preserves:

```text
observe_only: true
direct_execution_allowed: false
authority_expansion: false
standalone_diagnosis_authority: false
standalone_treatment_authorization: false
medical_act_authorization: false
```

## Medical-modality-neutral boundary

Every `QiRuntimeDecision` also preserves:

```text
medical_modality_neutral: true
qi_denied_by_boundary: false
east_asian_medical_reasoning_denied: false
biomedicine_privileged_by_wording: false
professional_judgment_required: true
patient_context_required: true
```

This boundary does not deny Qi, does not invalidate East Asian medical reasoning, and does not privilege biomedicine by wording. It only prevents a Samvrti Qi runtime decision from becoming standalone diagnosis authority, standalone treatment authorization, medical act authorization, institutional authority, theorem authority, or execution authority by itself.

## Minimal implementation files

```text
specs/samvrti_qi_runtime_contract_v0_1.yaml
examples/samvrti_qi_runtime_adapter_minimal.py
validation_cases/samvrti_qi_runtime_validation_cases_v0_1.yaml
scripts/validate_samvrti_qi_runtime_v0_1.py
```

## Runtime meaning

`qi_flow_accepted_as_samvrti_reference` means only this:

```text
A conventional Qi flow is sufficiently traced, gauge-linked, bounded, and recoverable to be observed and routed within KuuOS governance.
```

It does not mean:

```text
truth authority
proof authority
standalone diagnosis authority
standalone treatment authorization
medical act authorization
institutional authority
execution authority
final theorem authority
```

## Fail-closed rule

When evidence, gauge connection, memory lineage, curvature, holonomy, coherence, recoverability, or blocker status is insufficient, the runtime returns HOLD or BLOCKED. It does not silently upgrade weak Qi evidence into a strong release surface.