# KuuOS Repository Governance

## Purpose

This repository publishes the public core governance surface of KuuOS / 空OS.

The repository is managed under the following principles:

- append-only evolution where possible
- tighten-only governance changes by default
- provenance preservation
- fail-closed validation behavior
- non-authority preservation
- explicit boundary documentation

## Authority Boundary

Repository validation does not grant:

- theorem authority
- institutional authority
- execution authority
- deployment approval
- standalone diagnosis authority
- standalone treatment authorization
- medical act authorization
- Qi-based execution authorization

This is a medical-modality-neutral boundary. It does not assert that biomedicine is superior, nor that Qi or East Asian medical reasoning is false. It states only that repository validation alone is not a complete professional diagnosis, treatment decision, treatment authorization, or medical act authorization.

KuuOS governance artifacts are public structural surfaces unless an external validation process explicitly grants stronger status.

## Qi Motion Chain Boundary

The Qi motion chain is a governed, observe-only candidate surface.

Its public chain is:

```text
Samvrti Qi Runtime
  -> Samvrti Qi to Physical Motion Evidence Builder
  -> Physical Quantum Qi Runtime
  -> Physical Quantum Qi Dynamics Kernel
  -> Physical Quantum Qi Motion Pipeline
  -> observe-only bounded motion candidate
```

Governance requires:

```text
Samvrti Qi acceptance is not FullPathQi promotion.
Qi classification is evidence-bound, not claim-bound.
Validated Qi type licenses dynamics terms.
Unlicensed dynamics terms must be ignored.
Qi motion candidate remains observe-only.
Qi motion validation does not by itself grant standalone diagnosis, standalone treatment authorization, medical act authorization, institutional authority, theorem authority, or execution authority.
```

Changes touching this chain should run:

```bash
make qi-motion-chain-checks
```

## Change Classes

### Documentation Changes

Documentation may clarify existing boundaries, improve reviewer access, and add public explanations.

Documentation must not silently expand authority.

### Validator Changes

Validator changes should preserve or tighten checks.

A validator change that weakens an existing check should clearly explain why the old check was incorrect, overbroad, or obsolete.

### Specification Changes

Specification changes should be additive or tightening by default.

Breaking changes require explicit versioning.

### Formal Artifacts

Formal artifacts should indicate whether they are:

- stub
- sketch
- checked proof
- externally reviewed proof
- canonical proof reference

## Pull Request Review Expectations

Review should ask:

1. Does this change preserve non-authority boundaries?
2. Does it preserve provenance?
3. Does it avoid silent escalation from candidate to authority?
4. Does it keep physics-facing bridges distinct from canonical theorem repositories?
5. Does it preserve fail-closed behavior?
6. If Qi motion chain surfaces are touched, does it preserve observe-only, evidence-bound, licensed-dynamics behavior?
7. If medical language is touched, does it remain modality-neutral and avoid implying that Qi or East Asian medical reasoning is false?

## Release Expectations

A public release should include:

- release notes
- governance index pointer
- validator run instructions
- known limitations
- non-authority statement
- reproducibility notes

## Canonical Boundary

The canonical Lean proof repository for the 4D mass gap proof architecture remains:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

KuuOS may reference that repository, but does not replace it.