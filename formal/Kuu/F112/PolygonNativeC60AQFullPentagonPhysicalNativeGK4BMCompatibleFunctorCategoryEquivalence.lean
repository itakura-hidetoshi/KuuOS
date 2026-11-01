import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BLNaturalTransformationDescent
import Mathlib.CategoryTheory.ObjectProperty.FullSubcategory
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK4BM — a GENUINE Mathlib category equivalence
between the functor category of ACTUALLY attained old-AH matrices,
and the FULL SUBCATEGORY of the independently sourced F45-typed
structural functor category whose objects kill the original
S-side AH equality kernel.

GK4BJ: F : S -> A_att is a TRUE Mathlib Functor, literally
surjective on objects and surjective on each original typed Hom,
with exact original structural-AH observation equality kernel.
GK4BK: every F-kernel-compatible H : S -> T uniquely factors
as F ⋙ G = H for a G : A_att -> T.
GK4BL: precomposition by F is fully faithful on natural
transformation Homs for any target Mathlib category T.

Here the RHS is explicitly Mathlib
ObjectProperty.FullSubcategory (AHKernelCompatible), not the
whole S -> T functor category. The lifted precomposition is
an ACTUAL Functor between the stated categories; we prove
genuine Mathlib FullyFaithful, literal object-surjectivity,
IsEquivalence, asEquivalence, the true quasi-inverse Functor,
unit/counit NatIsos and triangle coherence.

This is ordinary 1-category/functor-category descent, NOT
source S -> A equivalence, raw Type-valued F54 equality,
original Q category laws, any F55/P92B Type witness filler,
all ambient integer-matrix reachability, global strict
higher coherence or hyperdescent.
Append-only/tighten-only/overwrite-forbidden/same-root107.
Strict 空 centered; independent Kuu one presentation; no Gray.
Pinned Lean v4.30.0-rc2 / mathlib
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
universe uD vD uE vE uT vT

section GenuineCompatibleFunctorCategoryEquivalence
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- The exact original S-side AH observation-kernel compatibility
as a pinned-Mathlib PROPERTY of real functor objects, NOT a
new postulated equation on original structural source routes. -/
def nativeGK4BMCompatibleProperty
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    ObjectProperty (NativeGK4IStage p ma mb pa pb ⥤ T) :=
  fun H => nativeGK4BKAHKernelCompatible p ma mb pa pb H

/-- The actual full subcategory in the S -> T functor category.
Its Homs are the EXISTING natural transformations between its
underlying functors; no further arrow equations are imposed. -/
abbrev NativeGK4BMCompatibleFunctorCategory
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :=
  (nativeGK4BMCompatibleProperty (T := T) p ma mb pa pb).FullSubcategory

/-- The actual pinned-Mathlib inclusion from the full subcategory
of AH-kernel-compatible structural functors, not an inclusion of
source raw path types. -/
def nativeGK4BMCompatibleInclusion
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
      (NativeGK4IStage p ma mb pa pb ⥤ T) :=
  ObjectProperty.ι (nativeGK4BMCompatibleProperty (T := T) p ma mb pa pb)

/-- The true old-AH precomposition functor, LIFTED through the
exact proven kernel-compatible object property by Mathlib
ObjectProperty.lift. No change to the original GK4BL functor. -/
def nativeGK4BMPrecompositionLift
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ⥤
      NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb :=
  ObjectProperty.lift
    (nativeGK4BMCompatibleProperty (T := T) p ma mb pa pb)
    (nativeGK4BLPrecomposition (T := T) p ma mb pa pb)
    (by
      intro G
      exact nativeGK4BKKernelNecessary p ma mb pa pb
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G) G rfl)

/-- The object of the genuinely compatible full subcategory
really is the source-side functor G after the actual observation F.
This is an equality of WHOLE functors. -/
@[simp] theorem nativeGK4BMPrecomposition_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj G).obj =
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G := rfl

/-- After inclusion of the actual compatible full subcategory,
the lifted precomposition is EXACTLY the old GK4BL precomposition,
not an arbitrary isomorphic replacement. -/
theorem nativeGK4BMPrecomposition_inclusion
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
      nativeGK4BMCompatibleInclusion (T := T) p ma mb pa pb =
        nativeGK4BLPrecomposition (T := T) p ma mb pa pb := rfl

/-- Every natural transformation Hom in the compatible category
really is an existing natural transformation in the source
functor category. No fabricated 2-cell types. -/
@[simp] theorem nativeGK4BMInclusion_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : X ⟶ Y) :
    (nativeGK4BMCompatibleInclusion (T := T) p ma mb pa pb).map η =
      η.hom := rfl

/-- The lift from GK4BL gives an ACTUAL fully faithful Functor
into the compatible FULL SUBCATEGORY, whose source Homs are
natural transformations on the genuinely attained AH category.
The inverse on Homs comes from real typed F45 source objects. -/
noncomputable def nativeGK4BMPrecomposition_fullyFaithful
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).FullyFaithful where
  preimage {G H} η :=
    nativeGK4BLNatTransLift p ma mb pa pb G H η.hom
  map_preimage {G H} η := by
    apply ObjectProperty.hom_ext
    exact nativeGK4BLWhisker_lift p ma mb pa pb G H η.hom
  preimage_map {G H} α :=
    nativeGK4BLLift_whisker p ma mb pa pb G H α

/-- Every AH-compatible FUNCTOR in the full subcategory is
LITERALLY the image of a uniquely given old-AH factored functor,
not only isomorphic to such an image. GK4BK provides the actual
factor, so this uses NO source S faithfulness assumption. -/
theorem nativeGK4BMPrecomposition_surjective_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Function.Surjective
      (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj := by
  intro Y
  refine ⟨nativeGK4BKFactorFunctor p ma mb pa pb Y.obj Y.property, ?_⟩
  apply ObjectProperty.FullSubcategory.ext
  exact nativeGK4BKFactor_functor p ma mb pa pb Y.obj Y.property

/-- The pinned Mathlib IsEquivalence structure is built from
explicit FULLY FAITHFUL natural transformation descent and literal
surjectivity on compatible functor objects, not postulated. -/
@[implicit_reducible] noncomputable def nativeGK4BMPrecomposition_isEquivalence
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).IsEquivalence := by
  let hFF := nativeGK4BMPrecomposition_fullyFaithful (T := T) p ma mb pa pb
  exact {
    faithful := hFF.faithful
    full := hFF.full
    essSurj := Functor.essSurj_of_surj
      (nativeGK4BMPrecomposition_surjective_obj (T := T) p ma mb pa pb) }

/-- MAIN GK4BM RESULT: a TRUE Mathlib category equivalence between
FUNCTORS on the genuinely attained old AH-image and the precise
FULL SUBCATEGORY of original AH-kernel-compatible S -> T functors.
This is NOT an equivalence between the original source categories
S and A, nor with the entire unrestricted S -> T functor category. -/
noncomputable def nativeGK4BMCompatibleFunctorEquivalence
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ≌
      NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb := by
  letI :
      (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).IsEquivalence :=
    nativeGK4BMPrecomposition_isEquivalence (T := T) p ma mb pa pb
  exact (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).asEquivalence

/-- The equivalence's forward functor is DEFINITIONALLY the original
precomposition lifted to the actual compatibility full subcategory. -/
@[simp] theorem nativeGK4BMCompatibleFunctorEquivalence_functor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor =
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb := rfl

/-- Actual Mathlib quasi-inverse on the compatible functor category,
not an inverse of original raw F54 paths. -/
noncomputable def nativeGK4BMCompatibleReverseFunctor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
      (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :=
  (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).inverse

/-- Genuine natural unit isomorphism of GK4BM's category equivalence. -/
noncomputable def nativeGK4BMUnitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    𝟭 (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ≅
      (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor ⋙
        nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb :=
  (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).unitIso

/-- Genuine natural counit iso, ON the exact compatible subcategory. -/
noncomputable def nativeGK4BMCounitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor ≅
        𝟭 (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :=
  (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).counitIso

/-- Exact triangle coherence for the forward equivalence, at each
genuine attained AH -> T functor object G, not a weakened
iso-existence claim. -/
theorem nativeGK4BM_triangle
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor.map
      ((nativeGK4BMUnitIso (T := T) p ma mb pa pb).hom.app G) ≫
        (nativeGK4BMCounitIso (T := T) p ma mb pa pb).hom.app
          ((nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor.obj G) =
      𝟙 ((nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor.obj G) :=
  (nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb).functor_unitIso_comp G

end GenuineCompatibleFunctorCategoryEquivalence

#print axioms nativeGK4BMCompatibleProperty
#print axioms nativeGK4BMCompatibleInclusion
#print axioms nativeGK4BMPrecompositionLift
#print axioms nativeGK4BMPrecomposition_obj
#print axioms nativeGK4BMPrecomposition_inclusion
#print axioms nativeGK4BMInclusion_map
#print axioms nativeGK4BMPrecomposition_fullyFaithful
#print axioms nativeGK4BMPrecomposition_surjective_obj
#print axioms nativeGK4BMPrecomposition_isEquivalence
#print axioms nativeGK4BMCompatibleFunctorEquivalence
#print axioms nativeGK4BMCompatibleFunctorEquivalence_functor
#print axioms nativeGK4BMCompatibleReverseFunctor
#print axioms nativeGK4BMUnitIso
#print axioms nativeGK4BMCounitIso
#print axioms nativeGK4BM_triangle

end
end Kuu.F112.Physical
