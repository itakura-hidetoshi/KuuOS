# F112-P94D3GK4T — verified structural-to-observer-kernel comparison

**2026-10-31 JST**, `itakura-hidetoshi/KuuOS`, authoritative theorem branch `main`.
[Theorem PR #2773](https://github.com/itakura-hidetoshi/KuuOS/pull/2773) **MERGED**.
Exact-source PR HEAD `e02ea84432050d55bc6672339d049a8bb6189bc0`.
Theorem squash SHA `74a22a0dfe54e253740a82374dca41240a0c93d9`, independently equal to canonical `main` HEAD immediately after theorem merge.
[Exact-source Strict Lean / Governance #41166852221](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41166852221): **3725/3725 scoped SUCCESS**, **5/5 Governance jobs completed SUCCESS** (all required steps successful; path-specific cache-miss actions skipped as configured). All **17** fresh declarations checked by `#print axioms`: only `propext`, `Classical.choice`, `Quot.sound` as dependencies, **no `sorryAx`**, changed Lean source warning/error **0/0**. Pinned Lean v4.30.0-rc2 / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.

## Precise theorem and three authority boundaries

[GK4T source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4TStructuralKernelComparison.lean) imports GK4S and Mathlib.Tactic, in one new append-only Lean file (no old source overwrite). Keep exact typed original F45 first/last, independent original D/E categories and all Blocks/Nat depths. The three distinct genuine quotients are:

- `Q = NativeF55P92AssocRouteClasses first last`: original Type-valued P92B comparison **existence** quotient, not its raw 3-cell.
- `S = NativeGK4EStructuralRouteClasses first last`: independently extended actual F54 structural-comparison existence quotient.
- `K_O = NativeGK4SKernelClasses observe first last`: *second quotient* of Q by `q∼r ↔ O(q)=O(r)`; GK4S establishes `K_O ≃ Im(O)`, not `S≃K_O`.

The exact canonical surjections are `π:Q→S` (GK4E), `κ:Q→K_O` (GK4S). We proved at all actual typed F45 boundaries:

```text
(∃ F : S → K_O, ∀ q : Q, F (π q) = κ q)
  ↔ ∀ actual original F54 structural seam r s,
         O([r]) = O([s]).
```

The construction `nativeGK4TComparison` is the actual structural `Quotient.lift` of `r ↦ κ([r])`. Well-definedness is justified by GK4N induction over the three genuine structural comparison constructors, not by synthetic conversion from observed equalities to P92B Type-valued 3-cells. The proof additionally gives the exact π-fiber criterion, map-level commuting triangle, uniqueness via GK4E surjectivity, existence-unique iff all seams, F surjectivity, F injectivity iff observed equality reflects actual structural equality, and the GK4Q image-level commuting triangle.

## Positive and negative tests

- The true GK4G Boolean rotation-zero observer respects all original 14 F54 structural seam constructors, so the comparison exists uniquely on every typed original F45 boundary.
- The true GK4K Option Nat observer does **not** admit any such F on any inhabited original F45 self-Hom. One actual F54 leftUnit seam relates original zero-rotation routes with observational values `some 2` and `some 1`.
- At the actual physical north C60 F45 triple these statements hold unconditionally. In the **same** example, the original Q→Boolean K_O projection is noninjective (GK4S). This does not show F itself is noninjective.

## Initial CI failure, exact repair and strict exclusions

Initial PR source HEAD `6e80b4108e6dde4b20dcbf4c3b44c31a14bc6aa4` failed **one** Lean proof at `nativeGK4TComparison_class`: a `simpa only` simplifier did not normalize the two nested quotient lifts after `Quotient.inductionOn`, leaving the actual route-class equality unsolved. After examining the **whole new file**, GK4E quotient constructors, GK4N seam theorem, GK4S equality, and pinned Lean's quotient calculation, replace the local tactic with `rfl`, using the primitive definitional reduction `Quot.lift f h (Quot.mk _ route) ≡ f route`. The final exact-source HEAD `e02ea84432050d55bc6672339d049a8bb6189bc0` passed all checks. The first failed CI receipt must not be confused with the green source.

Neither source P92B associativity nor source left/right unitality is established. Nor are alternative original source composition, historical complete P92B/F19/F28/F54/F55 typed equivalence, unconditional original 14D Countable, original 19D filler, global strict n or hyperdescent proved. The observer-kernel quotient and independently extended structural quotient are NOT generally identified. Keep 107 public roots, strict 空 central, independent Kuu one presentation, no Gray, and validation-only #1558 Draft/open/unmerged.

**Possible next problem, NOT proved:** conditional interoperability between GK4T comparison and GK4I structural composition / GK4S observation-kernel composition, with explicit typed observation/kernel laws and without claiming original P92B algebraic laws.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
