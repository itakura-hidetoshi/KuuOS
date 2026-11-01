import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BOTargetActionFunctor
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BP — explicitly chosen factor-Functor inverse on genuine
AH-compatible FUNCTORS and natural transformations, with strict
target-category naturality, without assuming naturality of the
arbitrarily chosen GK4BM asEquivalence inverse.

GK4BJ: the actual original F45-typed observer F : S ⥤ A_att
is object-surjective and full on typed Hom.
GK4BK: H : S ⥤ T factors uniquely through A_att when it
annihilates the original S-side attained-AH observation kernel.
GK4BL: real natural transformations descend along F.
GK4BM: honest equivalence between A_att ⥤ T and the genuine
FullSubcategory of AH-kernel-compatible S ⥤ T.
GK4BN–GK4BO: strict target postcomposition, naturality and
a true target-functor-category action with interchange.

GK4BP constructs a separate EXPLICIT chosen inverse Functor
from compatible S ⥤ T objects to genuine A_att ⥤ T functors.
On source natural transformations it uses their components
at each actual original F45 endpoint and proves naturality
on an actual GK4BK structural preimage of every AH arrow.
The two object-level inverse triangles, actual componentwise
counit, strict target postcomposition and target-NatTrans
compatibility are then verified for THIS explicit inverse.
We do not identify it definitionally with the arbitrary
quasi-inverse selected by the GK4BM asEquivalence.

No source S faithfulness, original Q category laws, raw F54/F55
Type-valued 3-cells, unfilled integer matrices, global Gray
coherence or hyperdescent. Append-only, tighten-only,
overwrite-forbidden, same-root107. Strict 空 center, independent
Kuu one presentation, no Gray reintroduction.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU

section ExplicitInverseTargetNaturality
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]

/-- A genuinely attained-AH natural transformation descending
an ACTUAL natural transformation of kernel-compatible original
structural functors. It is defined at the original typed F45
representative, not by inventing a new F54 higher filler. -/
noncomputable def nativeGK4BPFactorNat
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K) :
    nativeGK4BKFactorFunctor p ma mb pa pb H.obj H.property ⟶
      nativeGK4BKFactorFunctor p ma mb pa pb K.obj K.property where
  app X := η.hom.app X.original
  naturality := by
    intro X Y f
    let s := nativeGK4BKPreimage p ma mb pa pb X Y f
    exact η.hom.naturality s

/-- The descended genuine NatTrans has exactly the original
source component at each actually reached AH object. -/
@[simp] theorem nativeGK4BPFactorNat_app
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    (nativeGK4BPFactorNat p ma mb pa pb H K η).app X =
      η.hom.app X.original := rfl

/-- ACTUAL explicit inverse on the compatible full-subcategory
including its true natural-transformation Hom action. The
arbitrarily selected GK4BM quasi-inverse is left untouched. -/
noncomputable def nativeGK4BPExplicitInverseFunctor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
      (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) where
  obj H := nativeGK4BKFactorFunctor p ma mb pa pb H.obj H.property
  map η := nativeGK4BPFactorNat p ma mb pa pb _ _ η
  map_id := by
    intro H
    ext X
    rfl
  map_comp := by
    intro H K L η θ
    ext X
    rfl

/-- Its object action is exactly the original GK4BK CHOSEN factor. -/
@[simp] theorem nativeGK4BPExplicitInverse_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    (nativeGK4BPExplicitInverseFunctor p ma mb pa pb).obj H =
      nativeGK4BKFactorFunctor p ma mb pa pb H.obj H.property := rfl

/-- Its Hom action is exactly the newly descended NatTrans. -/
@[simp] theorem nativeGK4BPExplicitInverse_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K) :
    (nativeGK4BPExplicitInverseFunctor p ma mb pa pb).map η =
      nativeGK4BPFactorNat p ma mb pa pb H K η := rfl

/-- The explicit inverse respects the identity of every actual
compatible functor as a whole NatTrans. -/
theorem nativeGK4BPExplicitInverse_map_id
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    nativeGK4BPFactorNat p ma mb pa pb H H (𝟙 H) =
      𝟙 (nativeGK4BKFactorFunctor p ma mb pa pb H.obj H.property) :=
  (nativeGK4BPExplicitInverseFunctor p ma mb pa pb).map_id H

/-- The explicit inverse respects vertical composition of
real compatible source NatTrans, including all attained-AH Homs. -/
theorem nativeGK4BPExplicitInverse_map_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H K L : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K) (θ : K ⟶ L) :
    nativeGK4BPFactorNat p ma mb pa pb H L (η ≫ θ) =
      nativeGK4BPFactorNat p ma mb pa pb H K η ≫
        nativeGK4BPFactorNat p ma mb pa pb K L θ :=
  (nativeGK4BPExplicitInverseFunctor p ma mb pa pb).map_comp η θ

/-- At every compatible source functor, explicit factorization
and genuine precomposition return that same original source
Functor, as an equality of WHOLE underlying functors. -/
theorem nativeGK4BPExplicitInverse_compat_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    ((nativeGK4BPExplicitInverseFunctor p ma mb pa pb ⋙
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H) = H := by
  apply ObjectProperty.FullSubcategory.ext
  exact nativeGK4BKFactor_functor p ma mb pa pb H.obj H.property

/-- Conversely, on every truly attained AH functor G, source
precomposition followed by this EXPLICIT inverse recovers G
by the exact GK4BK uniqueness theorem; no chosen inverse
naturality has been assumed. -/
theorem nativeGK4BPExplicitInverse_attained_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
      nativeGK4BPExplicitInverseFunctor p ma mb pa pb).obj G) = G := by
  change nativeGK4BKFactorFunctor p ma mb pa pb
      (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G)
      ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj G).property = G
  exact (nativeGK4BKFactor_unique p ma mb pa pb
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G)
    ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj G).property
    G rfl).symm

/-- The composite of the explicit inverse and the forward
equivalence acts as the ORIGINAL natural transformation at
every actual source F45 object (a componentwise counit). -/
theorem nativeGK4BPExplicitInverse_compat_map_app
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K)
    (X : NativeGK4IStage p ma mb pa pb) :
    (((nativeGK4BPExplicitInverseFunctor p ma mb pa pb ⋙
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).map η).hom).app X =
        η.hom.app X := rfl

/-- Strict equality of WHOLE Mathlib functors: explicitly
chosen inverse factorization commutes with arbitrary target
postcomposition, on BOTH objects and natural-transformation
Homs, without postulating pseudonaturality of asEquivalence. -/
theorem nativeGK4BPExplicitInverse_target_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    nativeGK4BNPostcompCompatible p ma mb pa pb R ⋙
      nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb =
    nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb R := by
  apply CategoryTheory.Functor.toPrefunctor_injective
  refine Prefunctor.ext (fun H => rfl) ?_
  intro H K η
  rfl

/-- The strict target square on the actual morphism action:
the chosen NatTrans descent commutes with right whiskering. -/
theorem nativeGK4BPFactorNat_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K)
    (R : T ⥤ U) :
    (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb).map
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).map η) =
    Functor.whiskerRight
      ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).map η) R := by
  ext X
  rfl

/-- The induced natural transformation for a change of target
functor is preserved at each ACTUALLY attained AH object by
the explicit inverse; this is not raw F54 path coherence. -/
theorem nativeGK4BPExplicitInverse_targetNat_app
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    ((nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb).map
      ((nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app H)).app X =
        ρ.app (H.obj.obj X.original) := rfl

/-- Strong target NatTrans square for the EXPLICIT inverse,
not an unjustified assertion for the arbitrary chosen GK4BM
asEquivalence inverse. The two whole NatTrans have all
components equal at all genuinely attained AH objects. -/
theorem nativeGK4BPExplicitInverse_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    Functor.whiskerLeft
      (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
      (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) =
    Functor.whiskerRight
      (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
      (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb) := by
  ext H X
  rfl

end ExplicitInverseTargetNaturality

#print axioms nativeGK4BPFactorNat
#print axioms nativeGK4BPFactorNat_app
#print axioms nativeGK4BPExplicitInverseFunctor
#print axioms nativeGK4BPExplicitInverse_obj
#print axioms nativeGK4BPExplicitInverse_map
#print axioms nativeGK4BPExplicitInverse_map_id
#print axioms nativeGK4BPExplicitInverse_map_comp
#print axioms nativeGK4BPExplicitInverse_compat_obj
#print axioms nativeGK4BPExplicitInverse_attained_obj
#print axioms nativeGK4BPExplicitInverse_compat_map_app
#print axioms nativeGK4BPExplicitInverse_target_square
#print axioms nativeGK4BPFactorNat_postcompose
#print axioms nativeGK4BPExplicitInverse_targetNat_app
#print axioms nativeGK4BPExplicitInverse_targetNat_square

end
end Kuu.F112.Physical
