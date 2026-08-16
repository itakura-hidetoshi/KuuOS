# Gauge-Invariant Dependent Origination Descent v0.1

## Status

This document is an append-only extension of the KuuOS / 空OS dependent-origination surface.

It does not overwrite:

- `docs/EMPTINESS_DEPENDENT_ORIGINATION_KERNEL_v0_1.md`
- the existing dependent-origination sheaf/gauge runtime
- the Fourfold Core
- the Two Truths boundary

The extension is tighten-only: a gauge connection by itself is no longer enough for a claim of global relational meaning. A global claim must expose the local-to-global conditions under which gauge-invariant meaning is generated.

## Mathematical bridge

This extension is informed by the formal gauge-invariance route in `itakura-hidetoshi/4d-mass-gap`, authoritative branch:

```text
formal/real-hilbert-uniform-coercive-strong-limit
```

Bridge commit:

```text
52e45c33b56a34c905c94b63d4ced7cbbb5a29d2
```

Relevant Mathlib-formalized results include:

```text
boundedContinuous_gaugeInvariant_of_dense_interpolation
boundedContinuous_gaugeInvariant_of_dense_interpolation_readout
interpolationReadoutCompatible_of_boundedContinuous_readout
observable_unique_of_dense_interpolation
```

The KuuOS use of these results is a bridge interpretation. The KuuOS runtime does not acquire Lean theorem authority merely by citing them.

## 1. Extension of 縁起

The previous KuuOS kernel reads dependent origination as traceable relational conditioning.

This extension sharpens it to:

```text
Dependent Origination / 縁起
  = gauge-aware local relational conditioning
  + exact same-root readout
  + local gauge invariance
  + equivariant transport
  + cross-scale compatibility
  + dense local-to-global coverage
  + continuous global extension
  + uniqueness on the resulting conventional surface
```

The core principle is:

> A local representative is not the relational meaning. Relational meaning is what is preserved under admissible changes of local frame and what descends coherently from local/finite readouts to a global conventional surface.

## 2. Mathematical carrier

Let:

- `X` be a conventional global configuration/world surface,
- `G` be a gauge/symmetry group acting on `X`,
- `X_n` be local or finite-scale configuration spaces,
- `ι_n : X_n -> X` be interpolation/realization maps,
- `r_n : X_n -> Y` be local relational readouts,
- `R : X -> Y` be a candidate global relational readout.

The gauge action is written

```text
g · x
```

and the local gauge action at scale `n` is written

```text
g_n · u.
```

## 3. No privileged representative

KuuOS emptiness requires:

```text
x is not privileged over g · x merely because x is the current representation.
```

Thus:

```text
空 = no privileged gauge representative.
```

This is a de-reification rule. It does not assert that every representative is operationally identical; it asserts that representation choice alone cannot become independent essence or self-authority.

## 4. Invariant meaning and equivariant presentation

The extension separates two different requirements.

### 4.1 Semantic invariance

A semantic or relational observable `R` is gauge invariant when

```text
R(g · x) = R(x).
```

This is the appropriate law for meaning that is supposed to survive a change of local frame.

### 4.2 Presentation equivariance

A presentation-bearing surface `P` may transform nontrivially:

```text
P(g · x) = rho(g) · P(x).
```

Therefore KuuOS does **not** require every field to be invariant.

The rule is:

```text
meaning: invariant when declared gauge-independent
presentation/state coordinates: equivariant when representation-bearing
```

Conflating these two is a modeling error.

## 5. Local-to-global descent conditions

A global relational claim requires the following conditions when the claim relies on finite/local approximants.

### D0. Non-reification

No local representative, global representative, orbit, quotient, gauge choice, or runtime surface may be promoted to independent essence.

### D1. Exact same-root readout

For every scale `n` and local state `u`:

```text
R(ι_n(u)) = r_n(u).
```

The global and local readouts must refer to the same declared relational quantity. Arbitrary equivalence or semantic substitution is insufficient.

### D2. Equivariant interpolation

The local and global gauge actions must commute with interpolation:

```text
ι_n(g_n · u) = g · ι_n(u).
```

### D3. Local gauge invariance

For every scale:

```text
r_n(g_n · u) = r_n(u).
```

### D4. Dense local-to-global coverage

The union of local realization images

```text
D = union_n image(ι_n)
```

must be dense in the global conventional carrier when density is the mechanism used to extend equality.

A single local image is not silently treated as globally dense.

### D5. Continuous global extension witness

A global readout `R` must actually exist in the declared continuous class.

Cross-scale compatibility and density do not, by themselves, prove existence of a continuous extension.

This distinction is mandatory.

### D6. Cross-scale compatibility

If two local representatives realize the same global point,

```text
ι_n(u) = ι_m(v),
```

then their readouts must agree:

```text
r_n(u) = r_m(v).
```

When one exact global readout `R` satisfying D1 already exists, this compatibility is theorem-generated rather than an additional independent assumption.

## 6. Dependent Origination Gauge-Descent Theorem Schema

Under D1-D5, local gauge invariance generates global gauge invariance:

```text
for all g, x:
  R(g · x) = R(x).
```

The proof schema is:

```text
local gauge invariance
  + interpolation equivariance
  -> equality on every local interpolation image
  -> equality on their dense union
  + continuity
  -> equality on the whole conventional carrier.
```

This is the KuuOS gauge-descent reading of the Mathlib `Continuous.ext_on` route used in the 4d-mass-gap formalization.

## 7. Uniqueness without false existence

If `R1` and `R2` are continuous global readouts with the same exact local readouts and the interpolation-image union is dense, then:

```text
R1 = R2.
```

Thus density can remove ambiguity of a global extension once an extension exists.

It must **not** be misread as:

```text
cross-scale compatibility + density -> existence of a global continuous extension.
```

Existence remains a separate model-facing obligation unless independently established.

## 8. Action-groupoid reading

The gauge action defines an action groupoid

```text
G ⋉ X.
```

Objects are representatives `x`.
Arrows are admissible gauge transports

```text
x -> g · x.
```

A gauge-invariant semantic readout is constant along these arrows.

The dependent-origination object is therefore not merely a point and not merely a flat graph node. It includes:

- local representatives,
- admissible transformations,
- stabilizers,
- transport,
- curvature,
- holonomy,
- gluing data,
- same-root readout compatibility.

A coarse orbit set may be useful, but KuuOS should preserve groupoid/sheaf information whenever stabilizer, transport, gluing, or obstruction data matter.

## 9. Sheaf/gauge descent reading

The existing KuuOS dependent-origination runtime already requires site/cover structure, local sections, restriction maps, overlap compatibility, cocycle conditions, gluing, fibered context, gauge connection, transport, holonomy, and curvature visibility.

This extension adds the semantic descent condition:

```text
local sections may vary by gauge,
local presentations may transform equivariantly,
but declared gauge-independent relational meaning must agree on overlaps and descend to one global conventional readout when a global extension is claimed.
```

## 10. Two Truths boundary

Gauge invariance does not convert a conventional observable into an ultimate substance.

KuuOS therefore preserves:

```text
Paramartha / 勝義諦:
  no representative, orbit, quotient, observable, or gauge-invariant class has svabhava merely because it is invariant.

Samvrti / 世俗諦:
  gauge-invariant, same-root, scale-coherent relational observables may serve as stable conventional structure.
```

The Two Truths gap remains non-collapsing.

## 11. Middle Way

The extension rejects both extremes:

```text
representation absolutism:
  one local frame is the real one.

relational nihilism:
  because no frame is absolute, no stable relational meaning can exist.
```

The middle route is:

```text
no privileged representative
  + admissible relational transport
  + gauge-invariant/equivariant distinction
  + local-to-global descent
  + explicit extension obligations.
```

## 12. Runtime admission rule

A KuuOS runtime claim of global gauge-independent relational meaning must HOLD or REJECT rather than silently promote when any required condition is absent.

In particular:

```text
missing exact same-root readout -> HOLD
missing interpolation equivariance -> HOLD
missing local gauge invariance -> HOLD
missing density evidence when density is invoked -> HOLD
missing continuous global extension witness -> HOLD
representative privileged as essence -> REJECT
quotient/orbit reified as ultimate substance -> REJECT
invariance/equivariance conflated -> REPAIR
```

## 13. Compact formulation

The extended KuuOS principle is:

> 空 means that no gauge representative is self-existing or privileged merely as a representation. 縁起 means that relational meaning is reconstructed from conditioned local data and, where a global claim is made, descends coherently through admissible gauge transport, exact same-root readout, scale compatibility, density, and continuous extension. Gauge-invariant meaning is stable on the conventional side without being reified as ultimate substance.

In formula form:

```text
空:      no privileged representative
縁起:    gauge-aware relational descent
二諦:    invariant conventional structure != ultimate substance
中道:    neither representation absolutism nor relational nihilism
```

## 14. Authority boundary

This KuuOS extension is an architectural and runtime-governance specification.

It does not itself grant:

- Lean theorem authority,
- mathematical proof authority beyond the cited formal source,
- physical-model validity beyond the bridge scope,
- clinical authority,
- institutional authority,
- execution authority.

Version: v0.1
Date: 2026-08-16
Author: Hidetoshi Itakura / 板倉英俊
