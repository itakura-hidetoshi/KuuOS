# F112-P94D3GK5AS / Qi v4.12 — local P89 reflection and zero-grade no-descent

**Verified:** 2026-11-03 JST. Canonical repository `itakura-hidetoshi/KuuOS` / `main`.
Authoritative independent Kuu theorem: GK5AS; genuine north C60 physical
integration: Qi v4.12, in the direction **independent Kuu → Qi** only.

Original F54/F55/P80/P87/P89, selected P92B/P93/P94A, all prior
GK5AO/GK5AP/GK5AQ/GK5AR and Qi v4.8–v4.11 source declarations are
unchanged. Lean `v4.30.0-rc2`, pinned mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Public `KuuOSFormal` root **107** retained. #1558 remains
Draft/OPEN/unmerged. Strict 空 authority is not identified with a
physical C60 observation or a selected presentation.
No sorry/admit/native_decide, new axioms, Gray, rewriting of history,
or unconditional higher gluing.

## 1. Independent GK5AS — MERGED

| Evidence | Verified |
| --- | --- |
| Theorem PR | [#3004](https://github.com/itakura-hidetoshi/KuuOS/pull/3004) **MERGED** |
| Final exact source HEAD | `3f6ca612ac7bffb73533f8aee5b0d2a8105c3862` |
| Theorem squash SHA | `9059c792ad36767a1a93501b8262ab3e5f458be5` |
| Exact-head Governance | [41562024529](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41562024529) terminal **SUCCESS** |
| Strict Lean / `KuuOSFormal` | **9242 / 9242 SUCCESS** |
| New `#print axioms` | **9 / 9**, only `propext`, `Classical.choice`, `Quot.sound`, or none |
| Changed Lean errors/warnings / sorryAx | **0 / 0 / 0** |
| Governance | **30 / 30 terminal SUCCESS** |
| Source changes | One new independent Kuu Lean module; one additive public aggregate import |

**[GK5AS Lean proof source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ASSourceVertexObstructionLocalization.lean)**

### 1.1 Finite four-cell comparison chains with ORIGINAL source vertices

Fix the genuine original F54 dependent long/short route endpoints,
including both Nat depth indices, original Blocks and two Site
categories. An indexed `NativeGK5ASSourceVertexChain f g` connects
two **original F55 Type-valued 3-proof terms** `f` and `g`.

Each step has another original F55 proof `h` as a source vertex
and an **actual selected Type-valued P94A 4-cell**

```text
w : P94A(φ f, φ h),
```

where `φ` is the constructor-recursive original F55→P92B
structural map proven in GK5AI. This is not a numerical C60
shadow, Eq-only observation, or inferred original source cell.

`toSelected` composes all such source-vertex steps vertically
into a true selected P94A four-cell between the structural images
of the chain endpoints.

A `HasBadStep` witness is a **local selected P94A comparison
between consecutive original F55 proofs** for which no genuine
original P89 Type-valued 4-cell comparison exists.

The central GK5AS constructor-induction dichotomy is:

```text
For every source-vertex comparison chain(f,g):
  Nonempty(P89FourCell(f,g)) OR HasBadStep(chain).
```

In particular:

- If `¬ HasBadStep(chain)`, the full chain reflects to an
  original P89 4-cell at its endpoints.
- If original `BadPair(f,g)` holds, then **every provided**
  source-vertex chain `f→g` has at least one bad local step.
  This is conditional on such a chain having been supplied; no
  assertion that every selected P94A witness admits such a
  decomposition is made.
- Conversely, a bad local step supplies a genuine GK5AQ
  nonreflection bad pair among original F55 terms.

The theorem `nativeGK5ASAllSourceVertexChains_noBad_iff_injective`
makes this an exact criterion for injectivity of the **original
P89→selected P94A four-class quotient**: it is injective iff
no source-vertex chain of any length contains a bad step.
The singleton-chain case recovers GK5AQ's reflection condition.
This does NOT assert either side holds unconditionally.

### 1.2 Why selected intermediate P92B histories remain an obstruction

A source-vertex chain is an **outer decomposition** with original
F55 proof terms at its marked intermediate vertices. A single
selected P94A four-cell edge can still contain internally
non-source P92B evidence, and its existence does not provide
an original P89 4-cell. No "all P94A witnesses normalize
into primitive source-saturated chains" theorem is claimed.

This distinction prevents circularly assuming the missing
reflection certificate when investigating the original
P89→P94A bad-pair boundary.

### 1.3 A concrete zero-grade but nonrecoverable north C60 witness

For the REAL three adjacent north C60 F45 stages, selected P92B
has an adjoined, genuine `assocNaturality` 3-cell. Original F55
has **no** corresponding Type-valued 3-proof term.

Nevertheless, P94A has the selected reflexive 4-cell:

```text
refl : P94A(assocNaturality, assocNaturality).
```

GK5AR's exact two-component context-unit count parity law proves
that **every** P94A loop 4-cell at this selected 3-proof endpoint
has grade:

```text
(N_L(w) mod 2, N_R(w) mod 2) = (0, 0).
```

The theorem `nativeGK5ASNorthZeroGrade_not_sourceRecovery`
combines (1) the existence of a selected 4-cell; (2) the zero
grade for every selected loop 4-cell at that endpoint; and
(3) the **nonexistence of an original F55 source preimage**.

Therefore **zero context-unit grade is not a sufficient criterion
for descent or original evidence recovery.** Since the selected
3-proof is not in the original `φ` image, this is **not** a
counterexample to the original P89→P94A class map's injectivity:
GK5AQ bad pairs require **two genuine original source terms**.

### 1.4 Lean4 elaboration repair, no assumption weakening

The first GK5AS exact-source CI reported an unresolvable
`Category` typeclass metavariable from an insufficiently typed
local `Nonempty(P89FourCell _ _)` decision in dependent
chain induction. Giving named implicit constructor binders in
the tactic branch was not valid Lean4 tactic syntax.

The stable repair factors the **fully original-source-typed
local edge reflection decision** into a separate private
`nativeGK5ASReflectsOrBadStep_cons` theorem. The outer
chain induction then applies that theorem directly; it no
longer guesses the dependent source proof endpoints.
The corrected full source compiled without `sorryAx`,
errors or warnings. Full original F55/P89 and selected P94A
dependent endpoint definitions remain unchanged.

## 2. Qi v4.12 — genuine north C60 integration, MERGED

| Evidence | Verified |
| --- | --- |
| Qi PR | [#3005](https://github.com/itakura-hidetoshi/KuuOS/pull/3005) **MERGED** |
| Final exact source HEAD | `11b7e68d232ee3a5420f020933cd76c4e4f88de6` |
| Qi squash SHA | `5553d82ad232346db7b677d6c568a3e7e1539f5d` |
| Exact-head Governance | [41562639289](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41562639289) terminal **SUCCESS** |
| Strict Lean | **10169 / 10169 jobs successfully built** |
| New `#print axioms` | **4 / 4**, permitted logical dependencies only |
| Changed Lean errors/warnings / sorryAx | **0 / 0 / 0** |
| Governance | **30 / 30 terminal SUCCESS** |
| Source changes | New Qi v4.12 module + one additive public import |

**[Qi v4.12 Lean source](../../formal/KUOS/Architecture/QiWuxingGK5ASNorthSourceVertexNoDescentV4_12.lean)**

Qi uses the ORIGINAL genuine north four-sector pentagon
long/short F54 routes and original F55 proof terms to instantiate
the local-chain dichotomy and bad-pair locality. The REAL
north first-three-stage `assocNaturality` selected 3-proof
provides a grade-zero yet original-source-nonrecoverable
example on the same physical north C60 geometry.

`fivefoldGK5ASNorthPhysicalLocalityAndNoDescent` retains
the exact Qi v4.10 **conditional** noninjectivity iff for
the physical Dart-decorated original P89→P94A quotient,
the true fifth-around north `Dart×Dart` closure, GK5AN's
unconditional original P89 structural lift and both physically
reversed categorical e04/e43 orientations. Qi v4.11's
three-unit primitive count minimum/parity evidence remains
separate and unchanged.

No observed physical equality automatically creates or
recovers a missing Type-valued source witness. In particular
the existence of an actual original P89/P94A bad pair remains
**open**.

## 3. Next research — GK5AT (working name)

Study actual P94A **internal** 4-cell proof syntax (rather than
only source-labeled outer vertices): locate exactly which
selected intermediate P92B proofs have original F55 preimages,
and characterize a typed certificate permitting the entire
4-cell derivation to be normalized through original-source
generators. Either establish a sufficiently strong, separately
stated source-saturated comparison theorem or construct a
genuinely typed P89→P94A nonreflection bad pair.

No unconditional source recovery, universal source saturation,
P89→P94A noninjectivity or injectivity is asserted by GK5AS.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
