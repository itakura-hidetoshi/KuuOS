# F112-P94D3GK5AR / Qi v4.11 — exact P94A context-unit count parity normal form

**Verified:** 2026-11-03 JST. Canonical repository `itakura-hidetoshi/KuuOS` / `main`.
Authoritative mathematical theorem: independent Kuu GK5AR; one-way downstream
physical interpretation: Qi v4.11. Strict 空 authority remains separate.

Fixed Lean `v4.30.0-rc2` and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Public `KuuOSFormal` root **107** unchanged. Protected PR #1558 remains
Draft/OPEN/unmerged. Original F54/F55/P80/P87/P89, selected P92B/P93/P94A,
GK5AO/GK5AP/GK5AQ and Qi v4.8–v4.10 are historical, unchanged.
No sorry/admit/native_decide, added logical axioms, Gray or universal gluing.

## 1. Independent GK5AR theorem — MERGED

| Item | Exact verified state |
| --- | --- |
| Theorem PR | [#3001](https://github.com/itakura-hidetoshi/KuuOS/pull/3001) **MERGED** |
| Exact final source HEAD | `70cbebe189a9020199a9246a5aa09cde8730334b` |
| Theorem squash SHA | `5b66547d70a78e36e683079021f146bd8d23e5d6` |
| Exact-source Governance | [#41554552929](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41554552929) **SUCCESS** |
| Strict Lean / `KuuOSFormal` | **9240 / 9240 SUCCESS** |
| Added `#print axioms` declarations | **13 / 13**, only `propext`, `Classical.choice`, `Quot.sound` |
| Governance | **30 / 30 SUCCESS** |
| New logical axioms / sorryAx / changed Lean errors or warnings | **0 / 0 / 0** |
| Changes | New independent Kuu Lean module; one public aggregate import |

**[Lean4 source — GK5AR context-unit parity normal form](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ARContextUnitParityNormalForm.lean)**

### 1.1 Why the exact provenance grade is stronger than GK5AP

GK5AP established **minimal counts** for a particular normalization:
every selected P94A 4-cell normalizing a genuine left-context identity
must use `leftContextUnit` at least once; the right case is symmetric.
The *minimum* is one, even if both other selected units are available.

GK5AR now proves a universal **mod-two provenance law for each of
the all nineteen actual proof-relevant P94A four-cell constructors**.
Write `I_L` for GK5AP's leftContext/precompose observer and `I_R`
for its rightContext/postcompose observer on raw P92B proof histories.
Write `N_L(w)` and `N_R(w)` for the EXACT natural-number occurrence
counts of the two selected context-unit 4-generators in a P94A proof
term `w` (not numerical C60 shadows).

For every genuinely typed four-cell `w : P94A(f,g)`:

```text
(N_L(w) mod 2, N_R(w) mod 2)
  = (I_L(g) - I_L(f), I_R(g) - I_R(f)) in (ZMod 2) × (ZMod 2).
```

These endpoint-difference identities are the Lean theorem
`NativeF55P94UnitFourCell.gk5arContextParity_normalForm`.
They are the actual selected P94A proof-term provenance; no
raw F55 or original P89 proof terms were erased or identified.

The proof handles **all** constructors: `old` P93, reflexivity,
symmetry, vertical composition and units/associativity, both
whiskers and both contexts, F54 pre/post route actions, both
horizontal contexts, genuine interchange and the three
explicit P94A unit primitives.

In particular, for *any* two P94A certificates `w₁,w₂` with
the **same dependent P92B 3-cell source and target**:

```text
N_L(w₁) mod 2 = N_L(w₂) mod 2
N_R(w₁) mod 2 = N_R(w₂) mod 2
```

This is `gk5arContextParity_rigid`: **different higher
histories have the same grade**, not the same raw proof term.

### 1.2 Exact normalization signatures

| Original selected P94A unit normalization | `N_L mod 2` | `N_R mod 2` |
| --- | --- | --- |
| `leftContext(refl u, later) → refl(leftContext u later)` | **1 (odd)** | **0 (even)** |
| `rightContext(earlier, refl v) → refl(rightContext earlier v)` | **0 (even)** | **1 (odd)** |
| `horizontal(refl u,refl v) → refl(horizontalRoute u v)` | **0 (even)** | **0 (even)** |

All **possible** certificates for each true source/target have those
parities, independent of additional P93 evidence or arbitrary use
of other P94A generators. This strengthens GK5AP/GK5AO, not by
asserting a strict higher category, but by certifying the
source-provenance grade of every derivation.

**Important boundary:** GK5AO proves the horizontalUnit primitive
has minimum count **one**, but GK5AR does *not* prove a mod-two
rigidity theorem for horizontalUnit count. Only the two
context-unit counts have the displayed mod-two rigidity.

### 1.3 Pinned Lean elaboration repair

The initial GK5AR source had `rw` failures in eight whiskering,
context and pre/post route-action branches: after dependent
recursor compilation, the raw expression appeared as an
unfolded `NativeF55P92AssocComparison.rec` rather than the
syntactic induction-hypothesis term.

A first repair using `congrArg` and `convert` reduced the
problem but six conversion-side goals remained. The exact
stable fix was to expose four **definitionally true** P92B
constructor equations by `rfl`:

```text
gk5arLeftContext_parity
gk5arRightContext_parity
gk5arPrecompose_parity
gk5arPostcompose_parity
```

Then `simp only` with the named constructor law, the
induction hypothesis, and the abelian-group tactic establishes
the equality, without unfolding the entire dependent recursor.
The final source HEAD above passed full `KuuOSFormal` with
zero new Lean warnings/errors and permitted axiom output.

## 2. Qi v4.11 — true north C60 integration, MERGED

| Item | Exact verified state |
| --- | --- |
| Qi PR | [#3002](https://github.com/itakura-hidetoshi/KuuOS/pull/3002) **MERGED** |
| Exact final source HEAD | `4dee8377adeab0a66ed0256dbe000d69a2a5e25e` |
| Qi squash SHA | `f807ed50bf61f8fa637935f36ed5b67de59cacb2` |
| Exact-source Governance | [#41555305551](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41555305551) **SUCCESS** |
| Strict Lean | **10167 / 10167 jobs successfully built** |
| Added `#print axioms` | **4 / 4**, permitted dependencies only |
| Governance | **30 / 30 SUCCESS** |
| New logical axioms / sorryAx / changed Lean errors | **0 / 0 / 0** |
| Changes | New Qi module and one additive `KuuOSFormal` import |

**[Lean4 source — Qi v4.11 genuine north C60](../../formal/KUOS/Architecture/QiWuxingGK5ARNorthContextParityNormalFormV4_11.lean)**

Qi v4.11 uses the SAME true first and second adjacent north-C60
native F45 stages, historical dual-Nat F54 unit routes, two
original Site categories, selected P94A comparison and full
19-constructor proof histories as Qi v4.8/v4.9. For *all*
actual north certificates, it proves the exact left/right
context count grade and retains the GK5AO/GK5AP positive
minimal primitive-count lower bounds.

In the combined physical theorem
`fivefoldGK5ARNorthPhysicalGradedReflection`, these three
unit-grade claims coexist with:

- the EXACT **conditional** Qi v4.10 original P89→P94A nonreflection
  `BadPair` ↔ noninjectivity iff;
- the genuine fifth-around physical north `Dart × Dart` closure,
  including index `i+4` and endpoint `i`;
- reversed physical categorical e04/e43 orientations;
- the unconditional GK5AN original P89→selected P94A structural
  four-cell lift.

No physical edge, signed shadow equality or primitive grade
creates a previously missing original P89 four-cell. In
particular **existence of an actual P89→P94A nonreflection
bad pair is still open**; GK5AR does not settle unconditional
injectivity or noninjectivity.

## 3. Next research: GK5AS (working name)

Use this invariant grade as a **source-local filter** when
seeking a genuine P89→P94A comparison-normalization theorem:
identify whether full selected P94A witness paths whose
intermediate 3-cells are not structural `φ`-images can still
be normalized through source-saturated segments. Explore
typed generator-level reflection or an explicit bad pair,
while retaining the existing selected P92B `assocNaturality`
non-surjectivity and the exact original-source P89 boundary.

The grade is a necessary consistency constraint; by itself
it does NOT construct a globally source-saturated witness,
a universal inverse to `φ`, a terminal obstruction or
a canonical higher proof normalization.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
