# MGAP4D Canonical Proof Repository Reference v0.1

This document records the repository relationship between KuuOS and the canonical 4D mass gap proof repository.

## Canonical Proof Repository

The canonical Lean proof repository for the 4D mass gap proof architecture is:

```text
itakura-hidetoshi/4d-mass-gap
```

Canonical public URL:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

The canonical repository contains the active GitHub-native Lean project, including:

```text
MGAP4D.lean
MGAP4D/Phase3ReleaseGate.lean
MGAP4D/Spectral.lean
MGAP4D/Spectral/GapFormalization.lean
MGAP4D/SpectralGapFormalizationGate.lean
```

## KuuOS Role

KuuOS references the 4D mass gap proof architecture as a physics-facing bridge and public-core governance surface.

KuuOS may maintain interpretation, governance, proof-memory, artifact-map, normalization, and boundary-decision documents, but those documents do not replace the canonical proof repository.

## Direction of Authority

```text
itakura-hidetoshi/4d-mass-gap
  -> canonical Lean proof source

itakura-hidetoshi/KuuOS
  -> public-core governance / interpretation / bridge reference
```

## Cross-Repository Bridge

The canonical proof repository records the KuuOS bridge at:

```text
itakura-hidetoshi/4d-mass-gap: docs/kuuos_reference_bridge.md
```

KuuOS records the canonical proof repository here:

```text
itakura-hidetoshi/KuuOS: docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md
```

## Boundary

KuuOS reference documents do not independently open final theorem release.

Current boundary:

```text
canonical Lean proof repo: itakura-hidetoshi/4d-mass-gap
KuuOS reference bridge: present
spectral gap formalization: CI green in canonical proof repo
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
