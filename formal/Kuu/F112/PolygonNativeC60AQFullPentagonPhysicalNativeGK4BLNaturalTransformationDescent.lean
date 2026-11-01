import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BKUniversalAHFactorization
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BL — natural-transformation descent across the
genuinely attained old-AH quotient, at every original typed F45
object and in every target Mathlib category T.

GK4BJ constructs the ACTUAL structural quotient S -> attained AH
Functor F, surjective on objects and on every genuinely typed Hom.
GK4BK proves exact unique factorization of every AH-kernel-compatible
Functor S -> T. This sequel proves the 2-dimensional NATURALITY
obligation: whiskering along F is bijective on natural transformations
between arbitrary functors A_AH^att -> T. We construct an actual
inverse NatTrans by original typed object components, prove
naturality on every reached AH morphism by a genuine S preimage,
both inverse laws, and the pinned Mathlib FullyFaithful property
of the precomposition functor on the entire functor category.
Identity and vertical composition are preserved at NatTrans level.

Neither raw original F54 paths nor original F55/P92B Type-valued
3-cells are identified. This is 1-categorical functor-category
descent, NOT global strict higher coherence nor hyperdescent.
No assertion of S faithfulness, original Q category axioms, or
unattained ambient integer matrices. Append-only/tighten-only/
overwrite-forbidden/same-root107. Strict 空 central;
independent Kuu one presentation, Gray not reintroduced.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect validation-only #1558 Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT

section ActualNaturalTransformationDescent
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- Actual precomposition by the EXISTING GK4BJ structural-to-
attained-AH functor, on arbitrary Mathlib target T functors. -/
def nativeGK4BLPrecomposition
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ⥤
      (NativeGK4IStage p ma mb pa pb ⥤ T) :=
  (Functor.whiskeringLeft _ _ _).obj
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb)

/-- Its object action is EXACTLY the genuine composite functor,
not merely a natural-isomorphic comparison. -/
@[simp] theorem nativeGK4BLPrecomposition_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (nativeGK4BLPrecomposition (T := T) p ma mb pa pb).obj G =
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G := rfl

/-- The action on natural transformations is the PINNED Mathlib
left-whiskering by the true original structural comparison. -/
@[simp] theorem nativeGK4BLPrecomposition_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (α : G ⟶ H) :
    (nativeGK4BLPrecomposition (T := T) p ma mb pa pb).map α =
      Functor.whiskerLeft
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb) α := rfl

/-- Every natural transformation between actual source
precompositions uniquely determines a natural transformation
between the original attained AH functors. For each A-object
we use its original F45 typed boundary, NOT a synthetic object. -/
noncomputable def nativeGK4BLNatTransLift
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (η : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G ⟶
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H) :
    G ⟶ H where
  app X := η.app X.original
  naturality := by
    intro X Y f
    let s := nativeGK4BKPreimage p ma mb pa pb X Y f
    have hs : (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s = f :=
      nativeGK4BKPreimage_spec p ma mb pa pb X Y f
    have hn := η.naturality s
    change G.map ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s) ≫
        η.app Y.original =
      η.app X.original ≫
        H.map ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s) at hn
    rw [hs] at hn
    exact hn

/-- The lifted transformation's component at a genuine attained
AH object is exactly its source transformation component at the
original F45 stage, not a new proof witness. -/
@[simp] theorem nativeGK4BLNatTransLift_app
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (η : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G ⟶
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    (nativeGK4BLNatTransLift p ma mb pa pb G H η).app X =
      η.app X.original := rfl

/-- Whiskering the lifted transformation returns the ORIGINAL
source transformation on ALL actual S objects and Homs. -/
theorem nativeGK4BLWhisker_lift
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (η : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G ⟶
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H) :
    Functor.whiskerLeft
      (nativeGK4BJStructuralAHFunctor p ma mb pa pb)
      (nativeGK4BLNatTransLift p ma mb pa pb G H η) = η := by
  ext X
  rfl

/-- Conversely, lifting the old structural whiskering returns
the EXACT original attained AH natural transformation, since
the attained objects retain their genuine original F45 stages. -/
theorem nativeGK4BLLift_whisker
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (α : G ⟶ H) :
    nativeGK4BLNatTransLift p ma mb pa pb G H
      (Functor.whiskerLeft
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb) α) = α := by
  ext X
  rfl

/-- Every two attained-AH functors have an actual BIJECTION of
their genuine Mathlib natural-transformation Hom with their
original structurally precomposed natural transformations. -/
noncomputable def nativeGK4BLNatTransEquiv
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (G ⟶ H) ≃
      (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G ⟶
        nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H) where
  toFun α := Functor.whiskerLeft
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb) α
  invFun η := nativeGK4BLNatTransLift p ma mb pa pb G H η
  left_inv α := nativeGK4BLLift_whisker p ma mb pa pb G H α
  right_inv η := nativeGK4BLWhisker_lift p ma mb pa pb G H η

/-- Strongest actual Mathlib statement: PRECOMPOSITION by the
genuine, full/object-surjective source observer is FULLY FAITHFUL
on the entire Functor category, though S itself is NOT claimed
faithful to A. This is nonvacuous 2-dimensional descent. -/
noncomputable def nativeGK4BLPrecomposition_fullyFaithful
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BLPrecomposition (T := T) p ma mb pa pb).FullyFaithful where
  preimage {G H} η := nativeGK4BLNatTransLift p ma mb pa pb G H η
  map_preimage {G H} η :=
    nativeGK4BLWhisker_lift p ma mb pa pb G H η
  preimage_map {G H} α :=
    nativeGK4BLLift_whisker p ma mb pa pb G H α

/-- Actual natural transformation identity is preserved
UNDER INVERSE DESCENT, not merely forward whiskering. -/
theorem nativeGK4BLNatTransLift_id
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    nativeGK4BLNatTransLift p ma mb pa pb G G
      (𝟙 (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G)) = 𝟙 G := by
  ext X
  rfl

/-- Actual vertical composition of natural transformations is
preserved by the inverse descent on ALL attained AH objects. -/
theorem nativeGK4BLNatTransLift_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H K : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (η : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G ⟶
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H)
    (θ : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H ⟶
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ K) :
    nativeGK4BLNatTransLift p ma mb pa pb G K (η ≫ θ) =
      nativeGK4BLNatTransLift p ma mb pa pb G H η ≫
        nativeGK4BLNatTransLift p ma mb pa pb H K θ := by
  ext X
  rfl

/-- The exact same natural-transform Hom Equiv is the induced
equivalence supplied by pinned Mathlib's FullyFaithful structure. -/
theorem nativeGK4BLPrecomposition_homEquiv
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (α : G ⟶ H) :
    (nativeGK4BLPrecomposition_fullyFaithful (T := T)
      p ma mb pa pb).homEquiv α =
        Functor.whiskerLeft
          (nativeGK4BJStructuralAHFunctor p ma mb pa pb) α := rfl

/-- The compatible FUNCTOR objects are exactly the actual
object image of precomposition. This is BK's universal
factorization condition, not a faithfulness assumption. -/
theorem nativeGK4BLPrecomposition_obj_image_iff
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T) :
    (∃ G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T,
      (nativeGK4BLPrecomposition (T := T) p ma mb pa pb).obj G = H) ↔
        nativeGK4BKAHKernelCompatible p ma mb pa pb H :=
  nativeGK4BKFactor_exists_iff p ma mb pa pb H

/-- Every AH-kernel-compatible S->T functor has one and only
one actual precomposition preimage at the functor OBJECT level. -/
theorem nativeGK4BLPrecomposition_obj_unique
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H) :
    ∃! G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T,
      (nativeGK4BLPrecomposition (T := T) p ma mb pa pb).obj G = H :=
  nativeGK4BKFactor_existsUnique p ma mb pa pb H h

end ActualNaturalTransformationDescent

#print axioms nativeGK4BLPrecomposition
#print axioms nativeGK4BLPrecomposition_obj
#print axioms nativeGK4BLPrecomposition_map
#print axioms nativeGK4BLNatTransLift
#print axioms nativeGK4BLNatTransLift_app
#print axioms nativeGK4BLWhisker_lift
#print axioms nativeGK4BLLift_whisker
#print axioms nativeGK4BLNatTransEquiv
#print axioms nativeGK4BLPrecomposition_fullyFaithful
#print axioms nativeGK4BLNatTransLift_id
#print axioms nativeGK4BLNatTransLift_comp
#print axioms nativeGK4BLPrecomposition_homEquiv
#print axioms nativeGK4BLPrecomposition_obj_image_iff
#print axioms nativeGK4BLPrecomposition_obj_unique

end
end Kuu.F112.Physical
