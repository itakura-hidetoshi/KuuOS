# GK4AZ — pinned-mathlib formal Sanov free-product injection on integral shears

**2026-10-31 JST.** [Lean PR #2836](https://github.com/itakura-hidetoshi/KuuOS/pull/2836) **MERGED**, theorem squash `16585324b45863be3a4cc3faabbf59bb9be7cda8`.

[Formal Lean proof](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AZShearFreeProduct.lean)

## Exact theorem

For `U_n(x,y)=(x+2ny,y)`, `L_n(x,y)=(x,y+2nx)`, GK4AY proves all positive and negative nonzero exponent cone-transfer inequalities, invertibility and additivity. GK4AZ defines:
- Two independently defined monoid/group homomorphisms `Multiplicative ℤ →* Equiv.Perm (ℤ×ℤ)`: `nativeGK4AZUpperHom`, `nativeGK4AZLowerHom`.
- Boolean-labeled factors `nativeGK4AZFactors` and two disjoint nonempty strict cones `nativeGK4AZCones`.
- A finite 3-element injection into `Multiplicative ℤ` establishing the nontrivial-size hypothesis of mathlib ping-pong.
- The **full pointwise cross-cone condition for every nontrivial element of either cyclic factor**: `nativeGK4AZPingPong`.

The final theorem, **directly using the pinned mathlib lemma** `Monoid.CoprodI.lift_injective_of_ping_pong`, is

```lean
theorem nativeGK4AZFreeProduct_injective :
    Function.Injective
      (Monoid.CoprodI.lift nativeGK4AZFactors :
        Monoid.CoprodI (fun _ : Bool => Multiplicative Int) →
          Equiv.Perm (Int × Int))
```

Mathematically this provides an actual `ℤ * ℤ ↪ Perm(ℤ²)` faithful free-product action. **No new axiom/assumption of Sanov freeness was inserted**.

## Syntax and elaboration lessons (not assumptions)

The first exact-source CI failed, revealing five actual Lean elaboration issues:
- `ext z` decomposed product-coordinate extensionality too early; repaired with `apply Equiv.ext; intro z`, then definally matching the full permutation equality.
- `on` syntax requires `open scoped Function` with `autoImplicit false`.
- Pointwise action of a group on `Set` requires `open scoped Pointwise`; `HSMul` is not available otherwise.
- Cardinal `#(Multiplicative Int)` uses `open Cardinal` and `Cardinal.mk_le_of_injective`.
- Inverse action rewrites must be specialized *after* Bool case analysis to the actual upper/lower group hom, not kept as an abstract conditional `Factors` expression.

The final source uses the unchanged mathematical assumptions, preserves the complete original file and includes every declaration in `#print axioms`; no `sorry` or `admit`.

## Exact-source CI

- First source `f058c19c50494003e58d7485533f16b246373618`: **FAILURE** on the five syntax/elaboration issues, not retained as a successful proof.
- Final source `1d77015d43f5e6a37ea17a17f7cf811b3ace5a03`.
- CI test-merge checkout `cf1aa3d2a6335abde8b6006242fc7f334cd82484`.
- **Both exact Git trees** `b21f63a14261e655f689048137639cacbedf08b5`.
- [Run #41212234574](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41212234574) **Strict Lean 3789/3789 SUCCESS** and Governance **SUCCESS**.
- New Lean **9 declarations**, standard `propext`, `Classical.choice`, `Quot.sound` only; `sorryAx` 0; changed Lean warning/error 0/0.
- Pin Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, public roots 107, #1558 Draft/OPEN/unmerged.

## Precise unproved bridge and next stage

**GK4BA (planned, not yet Lean proved):** transfer the faithful free-product integer shear action to the full original GK4AV polynomial-matrix observer on ALL genuine F54-dependent paths. Construct a strict source-word/syntax map for the original generators `C`, `F=C⁻¹`, `R(X)`, and prove a commuting square from their `t=4` matrix image to the faithful shear action (coordinate rescaling) across original `RotationEdge`, `RotationChain`, `DepthRotationRoute` and typed `castDepths`, context and trans constructors.

Only after proving this bridge may one claim generally
```text
P_u(4) = P_v(4)  ==> P_u(X) = P_v(X).
```
At this stage neither the full existing K_AI polynomial descent nor source Type-valued 3-cells nor original Q category laws follow from matrix equality. Earlier two-point collision examples remain **unproved candidates**, not discoveries.

Strict 空 center, independent Kuu one presentation, append-only, tighten-only, overwrite-forbidden, same roots107. No Gray.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
