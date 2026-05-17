# Superstring Emptiness String / Brane / Membrane Lean Predicate Refinement v0.3

## Purpose

This document records the v0.3 refinement of the Lean theorem surface for the Superstring Emptiness String / Brane / Membrane Runtime.

v0.1 introduced the basic Lean skeleton.
v0.2 strengthened runtime validation.
v0.3 reflects the v0.2 fail-closed cases into Lean-level predicates and theorem targets.

## Refined Lean Objects

The Lean file is:

```text
lean/KUOS/SuperstringEmptiness/StringBraneMembrane.lean
```

v0.3 adds three key typed surfaces.

### 1. RuntimeClaim

```text
ordinaryCandidate
substanceClaim
absoluteWorldClaim
finalAuthorityClaim
graphOnlyIndraNetReduction
obstructionErasureClaim
directExecutionAuthorityClaim
transportEquivalenceClaim
```

This separates ordinary candidate runtime packets from collapse-producing claims.

### 2. WorldScope

```text
candidateEffectiveSurface
conventionalEffectiveSurface
localEffectiveWorldSurface
absoluteWorld
```

`absoluteWorld` is intentionally present as a forbidden boundary case so that it can be excluded by theorem.

### 3. RollbackOrHoldRoute

```text
hold
rollback
holdOrRollback
finalAuthority
```

`finalAuthority` is intentionally present as a forbidden boundary case so that it can be excluded by theorem.

## Refined Predicates

### IsConventionalOrCandidateScope

A brane scope is admissible only if it remains on:

```text
candidateEffectiveSurface
conventionalEffectiveSurface
localEffectiveWorldSurface
```

It must not become `absoluteWorld`.

### IsSafeRollbackOrHoldRoute

A membrane route is admissible only if it is:

```text
hold
rollback
holdOrRollback
```

It must not become `finalAuthority`.

### NoForbiddenRuntimeClaim

A runtime claim is admissible only if it is not one of:

```text
substanceClaim
absoluteWorldClaim
finalAuthorityClaim
graphOnlyIndraNetReduction
obstructionErasureClaim
directExecutionAuthorityClaim
transportEquivalenceClaim
```

## v0.3 Theorem Surface

The v0.3 Lean surface now includes theorem targets for:

- `non_reification_required`
- `two_truths_gap_required`
- `membrane_authority_non_expansion_required`
- `obstruction_visibility_required`
- `observer_record_scale_bridge_required`
- `string_substance_claim_forbidden`
- `brane_absolute_world_claim_forbidden`
- `brane_absolute_world_scope_forbidden`
- `membrane_final_authority_claim_forbidden`
- `membrane_final_authority_route_forbidden`
- `indranet_graph_only_reduction_forbidden`
- `gluing_obstruction_erasure_forbidden`
- `direct_execution_authority_forbidden`
- `transport_equivalence_claim_forbidden`

## Semantic Meaning

v0.3 shifts the runtime from informal non-collapse language to typed proof targets:

```text
string-as-substance
  -> forbidden RuntimeClaim

brane-as-absolute-world
  -> forbidden RuntimeClaim + forbidden WorldScope

membrane-as-final-authority
  -> forbidden RuntimeClaim + forbidden RollbackOrHoldRoute

graph-only IndraNet reduction
  -> forbidden RuntimeClaim

gluing erases obstruction
  -> forbidden RuntimeClaim

direct execution authority
  -> forbidden RuntimeClaim

transport as equivalence certificate
  -> forbidden RuntimeClaim
```

## Boundary

This is still a lightweight Lean skeleton, not a complete mathlib-based formalization.

It intentionally avoids external dependencies so that the repository can keep a low-friction public proof surface.

Future v0.4+ work may add:

- theorem proof cleanup,
- dedicated helper lemmas for nested conjunction extraction,
- mathlib-compatible structure if the repository adopts a full Lean project layout,
- Coq parallel predicates.

## Version

Version: v0.3
Date: 2026-05-17
Author: Hidetoshi Itakura / 板倉英俊
