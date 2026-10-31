# F112-P94D3GK4Z — actual backward F54 rotation count and infinite residual enhanced-observation fiber

**2026-10-31 JST** — `itakura-hidetoshi/KuuOS`, canonical theorem-bearing branch `main`.
[GK4Z theorem PR #2785](https://github.com/itakura-hidetoshi/KuuOS/pull/2785) **MERGED**.
Final verified PR source HEAD **`85e393966e9040cb62c8dbff8eeea6104f912576`**.
Theorem squash SHA **`f9e0c45fc18d2c1951b1c05579a3b90b87d00e5a`**, independently verified equal to canonical `main` immediately after theorem merge.
[Exact-source Strict Lean and Governance CI #41174633574](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41174633574): **3736/3736 Strict Lean SUCCESS**, **all 5 Governance jobs completed SUCCESS**, each of **40 new Lean declarations checked via `#print axioms`**, dependencies subsets of `propext`, `Classical.choice`, `Quot.sound`, **sorryAx 0**, changed Lean warning/error **0/0**.

## Strict authority: original proofs and distinct quotients

GK4Z does not identify the original Type-valued F54 route syntax, original P92B 3-cell proof syntax, the P92B existence quotient `Q`, the independently extended F54 structural comparison existence quotient `S`, or GK4X/GK4Y's TRUE second observational kernel quotient `K_X`.

All original F45 source and target trees, D/E categories, four original Blocks, BOTH Nat-depth axes, genuinely witnessed original forward/backward local rotations, and actual P92B comparison constructors are retained. Equality of observed values alone NEVER fabricates an original Type-valued P92B 3-cell.

## New backward rotation count, with FULL source-level soundness

[GK4Z BackwardCountInvariant Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ZBackwardCountInvariant.lean) defines the precise raw counts:

```text
backwardCount(.forward actual LocalRotation witness) = 0
backwardCount(.backward actual LocalRotation witness) = 1
backwardCount(.refl original F45 tree) = 0
backwardCount(.snoc actual original chain edge) =
    backwardCount(chain) + backwardCount(edge)

backwardCount(.chain actual original RotationChain) = backwardCount(chain)
backwardCount(.castDepths hn hm original F45 tree) = 0
backwardCount(.trans left right) = backwardCount(left) + backwardCount(right)
backwardCount(.leftContext route actual later tree) = backwardCount(route)
backwardCount(.rightContext actual earlier tree route) = backwardCount(route)
```

This counts ACTUAL backward physical F54 rotation-edge witnesses. It is not physical rotation count, not the signed GK4W `castCharge = castCount - physicalRotationCount`, and not an arbitrary Boolean shadow.

The genuine original F54 associator `.assoc t₁ t₂ t₃` contributes ZERO backwards: its actual single physical rotation is FORWARD. The real F55 3-vs-2 pentagon has zero backwards on both paths, as does the real disjoint-context square. Both P90 genuine associator-naturality routes have the very SAME original source u/v/w backwards counts and one forward associator, independent of their different typed source paths.

Formally verify by Type-valued induction on ALL actual comparison constructors:

- Original **F55 PresentedCell: all 9**, including the genuinely typed pentagon, disjoint square, pre/postcomposition, context, symm/trans, ident.
- Original **P92B AssocComparison: all 9**, including the actual P90 assocNaturality source.
- Independent genuine **F54 StructuralSeam: all 14**, including full reassoc, left/right unit, both context distribution/congruences and genuine pre/postcomposition.
- Extended **F55 StructuralComparison: all 3**: original, structural, trans.

Therefore EVERY actual original P92B comparison and EVERY independent additional F54 structural seam preserves backwardCount. Use the same raw witness, separately and canonically, to descend this NEW Nat invariant by `Quotient.lift` to both original `Q` and independent structural `S`, with actual `Q→S` commuting triangle, genuine structural composition additivity and witnessed structural identity 0.

The proof NEVER concludes that equal backward counts imply genuine source comparison or category equivalence.

## Construct genuine SAME (Boolean,castCharge) but DISTINCT structural routes

[GK4Z ResidualNonfaithfulness Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ZResidualNonfaithfulness.lean) starts with GK4F's *actual* `nativeGK4FBacktrack rot`: a two-edge `.forward rot` then `.backward rot` original RotationChain on any witnessed local rotation `rot : LocalRotation p before after`:

```text
rotationCount(B) = 2
backwardCount(B) = 1
castCharge(B) = -2
```

Define a SECOND genuine F54 proof word (not an ambient formal symbol):

```text
C = trans (castDepths rfl rfl before)
          (trans (castDepths rfl rfl before) B)
```

It consists of TWO actual explicit original Nat-depth cast witnesses and the same genuine forward/backward physical backtrack, so its exact measurements are:

```text
rotationCount(C) = 2
backwardCount(C) = 1
castCharge(C) = 0
```

Build original finite dependent F54 words by genuinely typed recursion on Nat:

```text
R_0 = B
R_(k+1) = trans C R_k

backwardCount(R_k) = k + 1
castCharge(R_k) = -2
rotationCount(R_k) = 2 * (k + 1)
GK4XEnhancedStructural([R_k]_S) = (false,-2)
```

These are all on the SAME genuine original dependent F45 self-Hom. Their original raw proof histories retain all actual F54 casts and backward rotations. GK4Z's new **FULL Type-valued structural comparison backward-count soundness** proves `[R_i]_S ≠ [R_j]_S` for `i ≠ j`, even though GK4X strengthened observation is IDENTICAL.

GK4X's independently proven exact structural→actual second-kernel comparison equality theorem then proves:

```text
For ALL i,j : Nat:
  F_X([R_i]_S) = F_X([R_j]_S)  in REAL K_X.
But i != j implies [R_i]_S != [R_j]_S in REAL S.
```

**Consequently GK4Y's real `S→K_X` structural comparison Functor is NOT faithful on the self-Hom of ANY original F45 tree admitting a genuinely witnessed `LocalRotation`.** This is a stronger absolute answer to the earlier GK4Y/GK4X unresolved comparison-faithfulness question at those actual contexts, not the invalid inference from unrelated original `Q→K_X` noninjectivity.

The new residual fiber `{s:S(before,before) // O_X(s)=(false,-2)}` receives an actual injection `Nat→fiber` via the original balanced tower. There is no generic countability upper bound on this S fiber without suitable original source D/E hypotheses.

## Actual physical C60 north theorem: residual fiber = aleph-null

The *real* `northHexagonNativeLeftRotation` is a witnessed F54 local rotation on the actual north-hexagon source triple `nativeGK4FPhysicalNorthTriple`. Thus the same GK4Z tower gives unconditional local nonfaithfulness at the true C60 physical source.

GK4G independently proved Countable of the genuine physical north STRUCTURAL existence quotient `S` from original Site/Blocks/Hom data. The new Nat tower injects into the exact same-enhanced-value residual fiber; that fiber as a Subtype of countable S is also Countable, so:

```text
Cardinal.mk (NativeGK4ZResidualStructuralFiber
    nativeGK4FPhysicalNorthTriple) = Cardinal.aleph0
```

The Lean theorem also constructs explicitly ONE actual `z:K_X` and a Nat-injective original structural `tower:Nat→S` such that `∀k,F_X(tower k)=z`, demonstrating that a SINGLE actual enhanced-observer second-kernel class has infinitely many distinct structural preimages.

**Important scope:** This cardinality concerns the genuinely typed *independent structural* quotient S fiber at the real C60 north site, NOT the original P92B Q→S collapsed fiber, NOT the historical original 14D `NativeK5FifteenFourteenFiber` unconditional Countable, and NOT generic S countability on arbitrary D/E categories. The strong old GK4Y result about K_X→K_B countable forgetful-unit fiber is separate.

## CI correction: mathematical laws preserved; Lean notation repaired

First PR HEAD `66a40ce315e041b81ae69720211c32136df6a5e5` FAILED Strict Lean due to GK4Z second-file elaboration; the ENTIRE first-file invariant and original/source/structural soundness successfully compiled. The second file initially attempted to rewrite `nativeGK4WCastRoute_charge` twice after Lean had ALREADY substituted both original cast occurrences; and referred to nonexistent `decide_False` after rewriting a proven nonzero rotation count. It also relied on Lean to retain a `rot` local rotation parameter in a declaration where it was not used in the RESULT TYPE (Lean omits such unused section arguments), and incorrectly applied the residual-fiber subtype to `rot` rather than to the actual original source F45 tree.

Fixed final exact PR HEAD `85e393966e9040cb62c8dbff8eeea6104f912576`: remove redundant rewrite, use `simp [hk]` for nonzero decidable equality, explicitly bind the original `rot` evidence in the local nonfaithfulness theorem, and index the residual fiber by the original physical tree `before` (or true north tree), not by the local-rotation witness. No axioms, assumptions, original paths, original F54 proof constructors, expected theorem goals or mathematical structures were weakened. The final CI #41174633574 independently completed **3736/3736** with all 40 axiom prints, no sorryAx and no changed-file warnings/errors; Governance **5/5 SUCCESS**. The initial failed run is NOT a completion receipt.

## Formal authority and successor

No original Q associativity, original Q left/right unit or replacement composition, historic full P92B/F19/F28/F54/F55 typed equivalence, genuinely original 14D unconditional Countable, original 19D filler, global strict n or hyperdescent was added or concluded. Do not infer source Type-valued cell existence from observational coincidences or classify all structural S homs from only these three invariants.

Keep canonical `main`, strict 空 central, independent Kuu one presentation; append-only, tighten-only, overwrite-forbidden, same-root, 107 public roots untouched. No Gray. Lean `v4.30.0-rc2` and mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Protected validation-only PR #1558 stays Draft/open/unmerged.

**Next candidate GK4AA (NOT proved):** Add genuine backwardCount to the Bool×Int observation as a third Nat coordinate, construct a typed compositional/fiber-conditional observer from original Q through S to a separate attained second kernel, and investigate residual same-triple observational obstructions without asserting generic faithfulness.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
