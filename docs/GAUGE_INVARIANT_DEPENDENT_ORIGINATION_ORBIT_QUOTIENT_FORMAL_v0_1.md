# Gauge-Invariant Dependent Origination — Orbit Quotient Formalization v0.1

## Purpose

This package tightens the integrated dense-descent theorem of PR #1387.

The previous theorem establishes that dense local realization, equivariant transport, local gauge invariance, continuity, and an explicit global semantic extension generate global semantic gauge invariance.

This package proves the next universal-property statement:

> a semantic map is gauge invariant exactly when it factors through the gauge-orbit quotient.

Thus KuuOS can formalize the anti-reification statement

```text
no gauge representative is semantically privileged
```

without asserting that the quotient is Paramartha or an ultimate substance.

## Formal chain

Let a group `Gauge` act on a representative carrier `X`.

Define

```text
x ~ y  iff  exists g, g • x = y.
```

The Lean package proves that this is a Setoid and forms

```text
GaugeOrbit Gauge X := Quotient gaugeOrbitSetoid.
```

For semantics `S : X → Y`, gauge invariance

```text
S (g • x) = S x
```

is equivalent to the existence of an orbit-level map

```text
Sbar : GaugeOrbit Gauge X → Y
```

with

```text
Sbar [x] = S x.
```

The orbit-level map is unique.

## Main theorems

- `semantic_factors_through_orbit_iff`
- `existsUnique_orbitSemantic_of_invariant`
- `dense_descent_existsUnique_orbitSemantic`
- `dense_descent_orbitSemantic_and_crossScaleCompatibility`

The last theorem combines the #1387 dense local-to-global result with quotient factorization:

```text
local exact readout
+ local gauge invariance
+ equivariant realization
+ dense realization union
+ explicit continuous global extension
=>
unique semantic map on gauge orbits
+ cross-scale compatibility.
```

## KuuOS interpretation

```text
空
= no representative has independent semantic authority

縁起
= locally conditioned appearances glue/descent to semantics that depend only on relational gauge orbit

二諦 gap
= orbit-level conventional invariance is not promoted into ultimate substance

中道
= preserve invariant relational content without reifying either a representative or the quotient construction
```

A concise operational statement is:

```text
presentation may be equivariant;
meaning factors through the invariant orbit.
```

## Boundary

This is an abstract Mathlib theorem package.

It does not claim:

- that every compatible local family admits a global continuous extension;
- that a coarse orbit quotient retains all stabilizer, isotropy, holonomy, or stack-level information;
- that the quotient is an ultimate ontology;
- that this KuuOS theorem itself proves a physical Yang–Mills statement.

The coarse orbit quotient is intentionally only the next formal step. A later groupoid/stack refinement may retain isotropy and descent data that a coarse quotient forgets.

## Lineage

- KuuOS base: `main@65cb4906fa597f167ded4fa774c0142ef02cf55c`
- predecessor: PR #1387
- motivating 4d-mass-gap bridge: `52e45c33b56a34c905c94b63d4ced7cbbb5a29d2`
- update mode: append-only / tighten-only
- overwrite: forbidden
- same-root required: true

Author: Hidetoshi Itakura / 板倉英俊
Date: 2026-08-16
