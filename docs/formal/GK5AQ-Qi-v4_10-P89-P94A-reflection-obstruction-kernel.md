# F112-P94D3GK5AQ / Qi v4.10 — exact original-P89 to selected-P94A reflection obstruction

**Verified:** 2026-11-03 JST. Canonical `itakura-hidetoshi/KuuOS` / `main`.
Authority: independent Kuu GK5AQ, used one-way by Qi v4.10. Original
F54/F55/P80/P87/P89, selected P92B/P93/P94A, previous GK5AO/GK5AP
and Qi v4.8/v4.9 are unchanged. The exact theorem is a **necessary and
sufficient criterion**, not a claim that P89→P94A is unconditionally
noninjective.

Lean `v4.30.0-rc2`, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Public `KuuOSFormal` root **107** maintained, protected #1558 remains
Draft/OPEN/unmerged. Strict 空 authority remains independent,
independent Kuu → Qi only. No source overwrites, sorry/admit,
`native_decide`, added logical axioms, Gray or global higher gluing.

## 1. Independent Kuu GK5AQ — MERGED

| Evidence | Verified |
| --- | --- |
| Theorem PR | [#2998](https://github.com/itakura-hidetoshi/KuuOS/pull/2998) **MERGED** |
| Exact-source final PR HEAD | `da2c6726002e4b6307f9ae74fd514cb21ae83455` |
| Squash SHA | `b668e879f56f949dae95c86fe6ffd6bb1c3cbf04` |
| Exact-source Governance | [41544750455](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41544750455) **terminal SUCCESS** |
| Strict Lean / KuuOSFormal | **9238 / 9238 SUCCESS** |
| `#print axioms` new results | **10 / 10**, only permitted `propext`, `Classical.choice`, `Quot.sound` |
| New logical axioms / sorryAx / changed Lean errors | **0 / 0 / 0** |
| Governance jobs | **30 / 30 SUCCESS** |
| Code changes | New original-dependent Kuu module and one additive public import |

[Authoritative GK5AQ Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AQP89P94ReflectionObstruction.lean)

### 1.1 The actual typed obstruction

Let `f,g` be **original F55 Type-valued 3-proof terms** on exactly
the same genuine F54 two-Nat source/target trees and route endpoints,
and `φ` the constructor-recursive GK5AI map into P92B.

```text
BadPair(f,g) :=
  Nonempty (P94AFourCell (φ f) (φ g))
  ∧ ¬ Nonempty (P89FourCell f g).
```

`nativeGK5AQBadPair` is a statement about genuine four-cell evidence,
not shadow equality, false conflation of `.original f` with `φ f`,
or a physical C60 Edge asserted to be an abstract NatIso.

The source P89 quotient → selected P94A quotient map was
unconditionally constructed by GK5AN. GK5AQ proves, at every
correctly dependent typed F54 boundary:

```text
(∃ original f g, BadPair(f,g))
    ↔ ¬ Function.Injective(P89ToP94AFourClassMap).
```

`nativeGK5AQBadPair_iff_class_gap` further characterizes a bad pair
as **two unequal original P89 classes with equal selected P94A images**.

### 1.2 Stable kernel and shadow invisibility

The true bad-pair property is symmetric. If `f~f'` and `g'~g`
in genuine original P89, then a bad pair `(f',g')` transports to
a bad pair `(f,g)`, via GK5AN's fully typed P89 4-cell lift.

Every bad pair also satisfies:

```text
f.nativeShadow = g.nativeShadow
```

for the entire original signed pentagon, signed square, and
odd `ZMod 2` phase triple. This uses genuine P94A four-cell
shadow soundness and GK5AJ structural preservation. **The
numerical/full signed observer is therefore incapable of
distinguishing a bad pair, if such a pair exists.** The theorem
does not manufacture a bad pair from coincident shadows.

### 1.3 Why the three P94A unit primitives are not automatically bad

GK5AO/GK5AP proved separate irredundancy of all three selected P94A
primitives (`horizontalUnit`, `leftContextUnit`,
`rightContextUnit`), relative to the existing P94A presentation.

But the **original** P89 already embeds all three corresponding
P80 unit 4-cell witnesses. GK5AQ constructs original P89 witnesses
and selected P94A witnesses for all three source primitive families,
and proves **none is a BadPair**. A counterexample to old
P93→new P94A faithfulness cannot simply be substituted into
the different original P89→P94A map. Extra, genuinely nonreflecting
comparisons remain to be found or excluded.

### 1.4 The distinct P92B associator-naturality obstruction

On the **actual north C60 first three F45 stages**, the selected
P92B `assocNaturality` constructor has genuine proof evidence,
whereas the original F55 associator-naturality source type is
**uninhabited**, by the independently proved original no-go.

Thus the original F55 → P92B proof-term structural `φ` map is
**not surjective at that exact typed slot** and no total function
reconstructing old original F55 evidence from *all* selected
P92B evidence of that slot can exist. This rules out a naive
global inverse-on-witnesses argument, **but by itself does not
show noninjectivity** of the original P89→P94A four-class map.

The initial GK5AQ Lean attempt used `¬(Selected → Original)`,
which is ill-typed because `Selected → Original : Type` and
Lean's negation requires a `Prop`. The corrected exact-source
definition uses `¬ Nonempty (Selected → Original)`; it compiled
without changing the mathematical obligation or relying on `sorryAx`.

## 2. Qi v4.10 — actual north C60 physical interpretation, MERGED

| Evidence | Verified |
| --- | --- |
| Qi PR | [#2999](https://github.com/itakura-hidetoshi/KuuOS/pull/2999) **MERGED** |
| Exact-source final PR HEAD | `2a389e247a145124ca0efca859c54207384b4572` |
| Squash SHA | `127ec02c99b254522c21e8359549a84bb6ceeff8` |
| Exact-source Governance | [41545634041](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41545634041) **terminal SUCCESS** |
| Strict Lean | **10165 / 10165 jobs successfully built** |
| New `#print axioms` | **7 / 7**, only permitted dependencies |
| New logical axioms / sorryAx / changed Lean errors | **0 / 0 / 0** |
| Governance jobs | **30 / 30 SUCCESS** |
| Code changes | New Qi v4.10 module and one additive public import |

[Qi v4.10 true north-C60 Lean source](../../formal/KUOS/Architecture/QiWuxingGK5AQNorthP89P94ReflectionObstructionV4_10.lean)

Qi instantiates the **same original four-sector north pentagon**,
its exact 3-vs-2 F54 long/short depth-rotation routes,
the genuine original P89 proof classes, and P94A via `φ`.
No source type or physical orientation is replaced.

`fivefoldGK5AQNorthPhysical_noninjective_iff_bad` establishes:

```text
¬ Injective(northPhysicalFourClassMap frame index)
    ↔ ∃ genuine original north BadPair.
```

The right side contains **no** selected gauge frame or fifth-around
Dart index. Therefore `fivefoldGK5AQNorthPhysical_injectivity_frame_independent`
proves that physical map faithfulness is identical for any two
genuine north frames and indices. If a bad pair exists, all
physical frames produce the same `(Dart×Dart) × P94A`
output for its two source P89 classes, even though those
classes remain distinct and have the same full F55 shadow.

The actual north fifth-around Dart closure, physically reversed
04/43 categorical orientations, GK5AN unconditional P89
structural lift and previous Qi v4.9 three-unit minimality
are retained. Physical evidence alone does not establish or
erase a higher Type-valued P89 four-cell.

## 3. Precise remaining mathematical boundary

**Proven:** the exact bad-pair iff, source-congruence stability,
full signed/odd shadow equality, original primitive-unit
reflectability, the north local failure of total 3-proof
recovery, and complete physical frame independence.

**Not proven:** existence of an original P89/P94A bad pair,
unconditional P89→P94A noninjectivity, unconditional injectivity,
or a universal normal form / global reflection theorem.

**Next investigation (GK5AR candidate):** analyze whether
selected P94A 4-cell comparison derivations between `φ`-images
can be normalized to original P89 comparisons. Target either an
explicit genuinely typed nonreflection witness, or a sufficient
source-saturated reflection/normalization criterion with a
separately identified obstruction. Preserve `assocNaturality`
as selected proof data and never silently backport it into
the original F55 source.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
