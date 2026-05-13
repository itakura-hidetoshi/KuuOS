# MGAP4D Normalization Convention Record v0.1

This document records the normalization-convention surface for the MGAP4D 4D mass gap proof program as tracked from the KuuOS public core.

It is a normalization record. It does not claim final theorem completion by itself.

## Purpose

The purpose of this record is to keep the following statuses separate:

```text
internal normalized target
  != physical-unit interpretation
  != final theorem statement
  != final release
  != public theorem boundary opened
```

The value `33/20` is tracked as an internal normalized target inside the MGAP4D proof architecture unless and until a separate physical-unit interpretation is explicitly recorded.

## Current Boundary Status

```text
spectral gap formalization: CI green
Phase 3 release gate: spectral gap formalization gate included
R1--R7 release-evidence map: created
proof artifact map: created
normalization convention record: created
final theorem boundary decision record: created
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Core Normalization Objects

The current proof-memory surface uses the following objects:

```text
H_phys
Omega
Omega_perp
m_gap
psi_*
A_{p,g}
rho_{A_{p,g}}
```

Current convention status:

| Object | Role | Current convention status |
|---|---|---|
| H_phys | physical Hamiltonian in proof architecture | internal normalization tracked; final physical-unit convention not opened here |
| Omega | vacuum / ground sector | proof-memory symbol tracked |
| Omega_perp | vacuum-orthogonal sector | proof-memory symbol tracked |
| m_gap | spectral gap target | internal normalized value tracked |
| 33/20 | gap target value | internal normalized units only here |
| psi_* | target eigenvector witness | existence target tracked, not final release claim here |
| A_{p,g} | compactly supported smeared centered plaquette observable | observable target tracked |
| rho_{A_{p,g}}({33/20}) > 0 | spectral-weight target | internal target tracked |

## Internal Normalized Target

The inherited target statement is recorded as:

```text
m_gap = 33/20
```

inside the MGAP4D proof architecture and in MGAP4D internal normalized units.

The witness target is:

```text
exists psi_* in Omega_perp,
  ||psi_*|| = 1
  and H_phys psi_* = (33/20) psi_*
```

The observable-weight target is:

```text
rho_{A_{p,g}}({33/20}) > 0
```

## Physical-Unit Boundary

This document does not assign a physical-unit value to `33/20`.

A physical-unit interpretation requires a separate record specifying:

- Hamiltonian normalization
- lattice/continuum scaling convention
- coupling convention
- volume or thermodynamic-limit convention
- unit conversion rule
- relation to any external mass unit
- error or uncertainty convention if applicable

Until such a record exists, `33/20` should be read as an internal normalized value.

## Required Fields for Future Final Normalization

A future final theorem normalization record should include:

```yaml
normalization_id: null
hamiltonian_symbol: H_phys
hamiltonian_domain: null
vacuum_sector_symbol: Omega
orthogonal_sector_symbol: Omega_perp
internal_gap_value: 33/20
internal_units: MGAP4D_internal_normalized_units
physical_units: not_opened_here
coupling_convention: null
scaling_convention: null
continuum_limit_convention: null
observable_normalization: null
spectral_measure_convention: null
release_commit: null
ci_evidence: null
boundary_status: held
```

## Relation to Existing Documents

This normalization record supports the following documents:

```text
docs/MGAP4D_4D_MASS_GAP_PROOF_MEMORY_v0_1.md
docs/MGAP4D_R1_R7_RELEASE_EVIDENCE_MAP_v0_1.md
docs/MGAP4D_PROOF_ARTIFACT_MAP_v0_1.md
docs/MGAP4D_FINAL_THEOREM_BOUNDARY_DECISION_RECORD_v0_1.md
```

It supplies a normalization surface. It does not fill all final-release fields by itself.

## Non-Promotion Rule

The following are not enough to open final theorem normalization:

- numerical value alone
- internal target statement alone
- artifact path alone
- CI success alone
- KuuOS interpretation alone
- physical analogy alone

## KuuOS Reading

In KuuOS terms, normalization is a boundary membrane between internal proof architecture and public claim language.

It preserves this order:

```text
internal normalized target
  -> normalization convention
  -> theorem statement
  -> release packet
  -> public theorem boundary
```

The membrane prevents a symbolic or internal value from being prematurely treated as an externally normalized physical claim.

## Fixed Boundary

```text
normalization convention record: created
physical-unit interpretation: not opened here
final theorem statement: not opened here
final release: not opened
public theorem boundary: held
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
