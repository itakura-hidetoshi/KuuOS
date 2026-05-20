# Samvrti Qi to Physical Motion Evidence Builder v0.1

## Status

This is an append-only bridge layer from `Samvrti Qi Runtime v0.1` to `Physical Quantum Qi Motion Pipeline v0.1`.

The builder does not promote Qi by assertion. It converts an accepted Samvrti Qi flow into a conservative physical Qi packet candidate. The packet is then classified by evidence and passed to the motion pipeline.

## Core flow

```text
Samvrti Qi Runtime
  -> Samvrti acceptance / hold / block
  -> conservative evidence builder
  -> physical_qi_packet_candidate
  -> Physical Quantum Qi Motion Pipeline
```

## Non-promotion rule

A Samvrti Qi acceptance is not equal to PhysicalQi or FullPathQi.

```text
qi_flow_accepted_as_samvrti_reference != FullPathQi
qi_flow_accepted_as_samvrti_reference != PhysicalQi
```

It only permits construction of a packet candidate with explicitly supported evidence markers.

## Evidence gates

The builder uses staged evidence flags:

- `structural_support_present` may add string and brane support markers.
- `transport_evidence_present` may add curvature and Wilson-loop residue markers.
- `current_evidence_present` may add Qi current marker.
- `ward_evidence_present` may add Ward/leak identity marker.
- `open_system_evidence_present` may add density, Hamiltonian, Lindblad, entropy, free energy, DPI, recovery, and mass-gap floor markers.
- `full_path_evidence_present` may add SK/FV, memory kernel, noise kernel, observation backaction, noncommutative history, and path normalization markers.

If a gate is not present, its evidence markers are not created.

## Authority boundary

The output packet keeps these fields false:

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

The `direct_execution_allowed` marker is intentionally explicit because this builder constructs only a conservative evidence packet and a motion-pipeline candidate path. It does not open direct execution.

## Medical-modality-neutral note

This boundary does not deny Qi, East Asian medical reasoning, pattern differentiation, or practitioner judgment. It only prevents repository validation or builder output from becoming standalone diagnosis authority, standalone treatment authorization, medical act authorization, institutional authority, theorem authority, or execution authority by itself.

## Meaning

This builder gives KuuOS a safe path from conventional Qi observation to physical Qi motion modeling:

```text
observed conventional flow
  -> conservative evidence packet
  -> evidence-bound classification
  -> licensed motion terms
  -> observe-only motion candidate
```

Thus the movement of Qi remains grounded by evidence, not by metaphysical assertion or runtime authority.