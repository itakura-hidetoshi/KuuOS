# F112-P94D3GK5AM — Context parity excludes source P80 context-unit four-cell structural lifts into selected P93

**Date:** 2026-11-03 JST. **Authority:** independent Kuu theorem source on `itakura-hidetoshi/KuuOS` canonical `main`. Qi may consume this theorem but no Qi-to-Kuu reverse dependency is permitted. Strict 空 remains independent. Root107 public API retained.

**Lean source:** [GK5AM context-parity actual obstruction](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AMContextParityNoStructuralLift.lean).

**Pins:** Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; protected PR #1558 Draft/OPEN/unmerged. Additive new module and one `KuuOSFormal` import. No sorry, native_decide, added axioms or historical frozen-repo rewrites.

## 1. Exact-source and CI evidence

| Evidence | GK5AM |
| --- | --- |
| Formal theorem PR | [#2984](https://github.com/itakura-hidetoshi/KuuOS/pull/2984) MERGED |
| Final exact-source HEAD | `554b198aa3c34cae52b5de63d64635ef5cb9a515` |
| Final source/test-merge Git tree | `cd9c2468e237fcb71178d5e566d0b7c8846601b2`, exact equality |
| Squash SHA | `8f67d37798d21b25b0d0f54c53e0a9e48a8dcbbb` |
| Final exact-source CI | [#41525719415](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41525719415) SUCCESS |
| Strict Lean / KuuOSFormal | **9230 / 9230 SUCCESS** |
| New `#print axioms` | **8/8**, each subset of `{propext, Classical.choice, Quot.sound}` |
| New `sorryAx` / Lean errors / Lean warnings | **0 / 0 / 0** |
| Governance | **30 / 30 terminal SUCCESS** |

The initial CI failed at dependent `change` elaboration in the P93 interchange parity case, not at the mathematical invariant. A first attempt to unfold the full dependent recursor generated an opaque recursive expression not normalized by `abel`; this was corrected by proving an explicit typed `gk5amTrans_contextParity` constructor equation and rewriting with `gk5amHorizontal_contextParity` before `abel`. The final run validated the complete new file, dependencies, pinned mathlib API, and root aggregation without weakening hypotheses.

## 2. Actual Type-valued ZMod 2 context invariant

Write `φ` for the **GK5AI structural** original F55→selected P92B 3-cell translation (not `NativeF55P92AssocComparison.original`). Define

```text
π(original F55 cell) = 0
π(adjoined P92B assocNaturality) = 0
π(refl) = 0
π(symm f) = -π(f)
π(trans f g) = π(f) + π(g)
π(leftContext f later) = π(f) + 1
π(rightContext earlier f) = π(f) + 1
π(precompose, postcompose f) = π(f).
```

All equalities occur in `ZMod 2`. Derived P92B horizontal composition contains one actual left-context and one actual right-context contribution; therefore

```text
π(horizontal f g) = π(f) + π(g)
```

since `1+1=0`. The raw proof history is preserved: this is a new source-sensitive invariant, not the existing signed pentagon/square/odd-hexagon three-coordinate C60 shadow.

Theorem `NativeF55P93AssocFourCell.gk5amContextParity_sound` proves that **all 16 true P93 four-cell constructors** preserve `π`: inherited old P89 generators, reflexivity, symmetry, transitivity, left/right vertical units, vertical associativity, both whiskerings, left/right F54 contexts, pre/post-composition, both horizontal whiskerings, and horizontal interchange. In particular, the inherited P93 `.old` constructor connects distinct `.original` endpoints of parity zero; it does not silently identify a structural `φ(f)` with `.original(f)`.

## 3. Concrete non-descent on original P80 primitive context units

On every genuinely well-typed original F54 route `u` and compatible later tree `L`, the TRUE original P80 primitive 4-cell is

```text
source: leftContext(ident u, L)
target: ident(leftContext(u, L)).
```

The GK5AI *structural* images into P92B have `π=1` and `π=0`, respectively. If a P93 selected four-cell joined them, P93 parity soundness would imply `1=0` in `ZMod 2`, contradiction. The theorem `nativeGK5AMLeftContextUnit_no_P93` formalizes `¬Nonempty(P93FourCell(φ(source),φ(target)))`. The theorem `nativeGK5AMRightContextUnit_no_P93` proves the symmetric obstruction for every matching original right-context unit.

The original source P80 and P87 Type-valued four-cell witnesses **do exist** (GK5AL/Qi v4.5); what fails is the target *structural* selected-P93 lift. We neither alter their source terms nor insert fabricated target four-cell constructors.

By GK5AL's exact three-primitive boundary theorem, one genuine left-context witness already establishes

```text
¬Nonempty(NativeGK5AKP87StructuralBoundary p)
¬Nonempty(NativeGK5AKP89StructuralBoundary p)
```

for its true fixed category and polygon source. This is formalized as `nativeGK5AMP87_no_structural_lift_of_leftContext` and `nativeGK5AMP89_no_structural_lift_of_leftContext`. The P89 horizontal interchange 4-cell itself remains unconditionally constructible by GK5AK; the obstruction applies to **the whole structural translation of all P89 constructors**.

## 4. Interpretation and exact scope

**Proved:** with an actually available typed context, the present *selected P93 four-cell presentation* cannot structurally transport all old P87/P89 four-cells. This is stronger than GK5AL's conditional equivalence. It isolates the first obstruction at the P80 left/right context unit boundary, expressed as `ZMod 2` witness-sensitive parity and a Lean-backed impossibility theorem.

**Not claimed:** failure of every possible P93 extension or alternate structural map; impossibility of the genuinely old original-P89 or P93 horizontal interchange; global invalidity of Qi's physical fifth-Dart data; an unconditional reflection/fidelity theorem for the source four-cell quotient; any general higher filler, Gray reconstruction or unrestricted gluing. The current Qi v4.5 physical four-class map is a function that takes an explicitly supplied three-unit compatibility argument, not a promise that such an argument is inhabited.

**Next Qi v4.6 candidate:** instantiate the new GK5AM actual no-lift with Qi v4.5's verified north C60 first/second F45 stage typed P80 left/right context witnesses to prove an explicit **north C60 uninhabited primitive boundary** and refine the physical comparison interface without losing 04/43 reversed orientations or original F54/F55 histories.

Historical GK5AL/Qi v4.5 [proof record](GK5AL-Qi-v4_5-primitive-P80-unit-structural-boundary.md) remains authoritative for the prior necessary-and-sufficient conditional reduction.
