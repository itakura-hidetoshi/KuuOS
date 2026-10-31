# F112-P94D3GK4W — genuine F54 cast-depth charge and nonfaithful structural Boolean observation

**2026-10-31 JST.** Repository `itakura-hidetoshi/KuuOS`, canonical theorem carrier `main`.
[Theorem PR #2779](https://github.com/itakura-hidetoshi/KuuOS/pull/2779) **MERGED**.
Exact final PR source HEAD: `86b0ed53f0e214513f02050a34ff1e39d7fd2160`.
Theorem squash SHA `a19ae676144ac5f1e40bd9443f43e776afcb9915`, independently verified equal to canonical `main` HEAD immediately after theorem merge.
[Exact-source Strict Lean and Governance run #41170191145](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41170191145): **3730/3730 scoped Strict Lean SUCCESS**, **5/5 Governance jobs completed SUCCESS**, all required steps completed successfully; all **30** declarations audited with explicit `#print axioms`, dependencies are subsets of `propext`, `Classical.choice`, `Quot.sound`; `sorryAx` absent, changed Lean warning/error **0/0**.

## Genuine Type-valued source theorem, not a shadow

[GK4W cast-charge Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4WCastChargeInvariant.lean) introduces precisely:

```text
castCount : original dependent F54 route -> Nat
castCount(.chain original finite rotation path) = 0
castCount(.castDepths hn hm actual original F45 tree) = 1
castCount(.trans r s) = castCount(r) + castCount(s)
castCount(.leftContext r context) = castCount(r)
castCount(.rightContext context r) = castCount(r)

castCharge(r) = (castCount(r) : Int) - (rotationCount(r) : Int)
```

The actual F54 associator `.assoc first second third` is a TRUE original cast of both depth equalities followed by one true primitive local rotation, so castCharge = 0. The actual original 3-edge versus 2-edge pentagon uses respectively three versus two of these real associators; both sides have castCharge = 0. Genuine F55 disjoint-square has two physical rotations and no `castDepths` on both orders, so both have charge -2.

The Lean code proves signed charge additivity for actual vertical `trans`, genuine horizontal `nativeF54P90HorizontalRoute`, left/right F45 contexts, and the actual source `nativeF54P90AssocNaturalityLeftRoute` vs `RightRoute` equality. It then performs COMPLETE constructor induction on the independent original Type-valued witnesses:

- all **9 original F55 PresentedCell** constructors (including pentagon and disjoint square),
- all **9 original P92B AssocComparison** constructors (including the extra genuine P90 associator-naturality source),
- all **14 F54 structural seam** constructors (reassoc, left/right units, pre/post, context transport and congruences, reflexive/symmetric/transitive closures),
- all **3 extended F55 StructuralComparison** constructors.

Therefore **EVERY original extended structural comparison necessarily preserves castCharge**. The source original P92B quotient `Q` and the separate extended structural-comparison quotient `S` retain their provenance and are NEVER identified with the second observational quotient `K_Bool`. Equality of integer charges alone is never upgraded into a new original Type-valued P92B 3-cell.

## Actual nonfaithfulness witness, all inhabited F45 stages

[GK4W cast tower / nonfaithfulness Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4WCastTowerNonfaithfulness.lean) defines an ACTUAL original F54 self-route:

```lean
def nativeGK4WCastRoute (tree : ...) :
    DepthRotationRoute p tree tree := .castDepths rfl rfl tree
```

For every real typed F45 tree, this route has **castCharge=1** and **rotationCount=0**. The actual `.chain (.refl tree)` identity REPRESENTATIVE of the independent structural category has **castCharge=0** and **rotationCount=0**. Structural charge soundness proves their genuine independent structural quotient classes **UNEQUAL**, while original GK4G Boolean grading gives `true` for BOTH.

Together with GK4V's proved exact observation kernel equation `F(u)=F(v) iff structuralGrade(u)=structuralGrade(v)`, GK4W proves GK4T/GK4U's **ACTUAL structural→second-Boolean-kernel comparison is NOT injective** on the self-Hom of EVERY inhabited original F45 stage. It also proves GK4U's true Mathlib functor's Hom map at any such actual self-Hom is noninjective, so the functor is **NOT FAITHFUL**. This is **not** inferred from prior original P92B `Q→K_Bool` noninjectivity; the witnesses themselves are already distinct in the independent S quotient. It does NOT claim that the original P92B source is a category or infer a source identity law.

## Actual infinite one-grade structural quotient fiber

Let `T₀` be the genuine original zero-edge chain and `T_{k+1}=castDepths(rfl,rfl,tree) ≫ T_k`, with `≫` the genuine ORIGINAL F54 route trans. GK4W proves by original dependent recursive definitions:

```text
castCharge(T_k) = k : Int
rotationCount(T_k) = 0
structuralGrade([T_k]_S) = true
Injective (k : Nat -> [T_k]_S)
```

The actual Boolean-true structural fiber `{s:S // structuralGrade(s)=true}` thus receives a genuinely injective map from `Nat` at EVERY inhabited original F45 tree. At the real C60 north-hexagon original F45 triple, prior GK4G provides **Countable of the genuine structural route quotient** from the true Site and all Hom countability proofs. The true Boolean-true fiber as a Subtype is countable, while the new tower establishes infinity. Hence:

```text
Cardinal.mk (NativeGK4WTrueStructuralFiber
    nativeGK4FPhysicalNorthTriple) = Cardinal.aleph0
```

This cardinality is NOT the old original 14D `NativeK5FifteenFourteenFiber W` unconditional Countable, nor the original Q→S collapse fiber cardinality.

## First CI elaboration failure, exact correction

The initial source `2b7e544b729660acc14fda4191756dfcc8a70183` compiled the full 12-declaration cast-charge invariant file AND the genuinely unequal yet equal-grade structural witness and nonfaithfulness theorems. The remaining cast-tower definition used an **overapplied internal recursive call** `nativeGK4WCastTower tree k` within Lean4's equation compiler. At that point, the actual recursive function already captured `tree`, so the expected next argument was `k : Nat`, not `tree`. This failure led to `sorryAx` in the rejected intermediate build and a downstream `change` failure in the rotation lemma. After examining the entire changed source, dependent tree signatures and exact Lean error, the corrected internal call is `nativeGK4WCastTower k`, leaving the public generated function with its full `tree` parameter. The next **exact-source** HEAD `86b0ed53f0e214513f02050a34ff1e39d7fd2160` passed full Strict Lean 3730/3730 and governance 5/5 with NO sorryAx. The initial failed run is NOT a completion receipt.

## Still unproved, governance and next research

Unproved: original P92B quotient composition associativity and left/right identity laws, arbitrary alternative original source composition, historic full P92B/F19/F28/F54/F55 typed equivalence, original 14D unconditional Countable, original 19D filler, global strict n or hyperdescent. The new signed cast-charge is a necessary invariant for original structural comparison, NOT a complete classifier for genuine Type-valued proof classes. A Boolean-plus-charge observation might separate more structural classes, but its full faithfulness or equivalence is NOT proved.

Keep strict 空 central, independent Kuu one presentation, no Gray, append-only / tighten-only / same-root / overwrite-forbidden, 107 public roots, Lean v4.30.0-rc2 and mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Protected validation-only PR #1558 stays Draft/open/unmerged.

**GK4X proposed only:** Formalize the charge-enhanced observation (Boolean, signed charge) as a genuinely typed structural/category functor and characterize remaining equality-kernel obstructions without claiming historical full typed recovery.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
