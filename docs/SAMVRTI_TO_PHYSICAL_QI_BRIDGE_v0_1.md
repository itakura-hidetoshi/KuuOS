# Samvrti to Physical Quantum Qi Bridge v0.1

## Status

This document is an append-only bridge surface from `Samvrti Qi Runtime v0.1` to the existing `Physical Quantum Qi Runtime v0.1`.

The bridge does not upgrade Qi into a substance. It maps a conventional Qi flow into a physical evidence packet candidate only when the Samvrti runtime has accepted the flow as a bounded, traced, gauge-linked, recoverable reference.

## Source and target

Source:

```text
Samvrti Qi Runtime
  decision_status: qi_flow_accepted_as_samvrti_reference
  runtime_mode: observe_and_route
  direct_execution_allowed: false
  authority_expansion: false
```

Target:

```text
Physical Quantum Qi Runtime
  validated_type in NonQi / PreQi / ProtoQi / TransportableQi / CurvedQi / CurrentQi / PhysicalQi / FullPathQi
  classification by evidence, not claim
```

## Bridge principle

The bridge is a projection, not a promotion.

```text
samvrti_effective_flow_state
  -> evidence-bound physical_qi_packet_candidate
  -> Physical Quantum Qi validator
```

A Samvrti Qi acceptance only opens the right to build a packet candidate. The final `validated_type` still belongs to the Physical Quantum Qi runtime classifier.

## Mandatory non-authority boundary

The following must remain false across the bridge:

```text
execution_authority
belief_commit_authority
memory_overwrite_authority
world_root_rewrite_authority
safety_override_authority
final_theorem_authority
direct_execution_allowed
```

## Required bridge checks

The bridge requires:

1. `samvrti_acceptance_required`
2. `source_trace_required`
3. `IndraNet_gauge_connection_required`
4. `memory_lineage_required`
5. `recoverability_margin_required`
6. `authority_nonexpansion_required`
7. `mass_gap_floor_is_floor_not_source`
8. `physical_type_claim_not_authoritative`
9. `unresolved_blockers_visible`
10. `validator_handoff_required`

## Evidence mapping

A bounded Samvrti Qi flow may seed evidence fields such as:

- `K_non_reification`
- `delta_rel_in_K_perp`
- `gauge_connection_A_mu`
- `curvature_F_munu`
- `Wilson_loop_residue`
- `entropy_production_Sigma`
- `DPI_gap`
- `recovery_margin`
- `mass_gap_floor_33_20`

But these mapped markers remain candidate evidence until the Physical Quantum Qi runtime classifies the packet.

## Runtime outcomes

Allowed bridge statuses:

- `bridge_ready_for_physical_qi_validation`
- `bridge_held_for_samvrti_observation`
- `bridge_blocked_by_authority_or_reification`

`bridge_ready_for_physical_qi_validation` does not mean PhysicalQi or FullPathQi. It means only that a packet candidate can be handed to the Physical Quantum Qi validator.

## Fail-closed rule

If the Samvrti source is held or blocked, the bridge is held or blocked. If the bridge would create authority, it is blocked. If unresolved blockers exist, they remain visible and the bridge does not silently erase them.
