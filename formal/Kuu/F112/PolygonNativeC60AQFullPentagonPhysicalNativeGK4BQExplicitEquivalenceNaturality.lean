import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BPExplicitInverseTargetNaturality
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.NatIso
import Mathlib.Tactic

/-!
F112-P94D3GK4BQ — genuine natural unit/counit isomorphisms for the
EXPLICIT GK4BP factor inverse and the original GK4BM forward
precomposition, triangle coherence, and comparison with GK4BM's
arbitrarily chosen asEquivalence quasi-inverse via actual NatIso.

S is the original independently sourced, F45-dependently typed
structural category. A_att is the genuinely attained old-AH
matrix category, not all ambient integer matrices. The compatible
category is a true Mathlib ObjectProperty.FullSubcategory of S ⥤ T,
not the whole source functor category. C_T is GK4BM genuine
forward precomposition and P_T is the explicitly constructed
GK4BP factorization inverse.

The concrete unit/counit components use actual NatIso identities
on original typed objects, whose NATURALITY is certified by the
GK4BK original structural Hom preimage and factor-map theorem.
The resulting genuine Equivalence has both triangles; the selected
GK4BM inverse and the EXPLICIT GK4BP inverse are only compared
by a natural isomorphism, never identified definitionally.

No original S faithfulness, raw F54/F55 Type-valued 3-cells,
source Q category axioms, unreached matrices, Gray reconstruction
or higher hyperdescent. Append-only/tighten-only/same-root107.
Lean v4.30.0-rc2; pinned mathlib
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

section ExplicitEquivalenceUnitCounit
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- At an actually attained old-AH functor G, the explicit
factor of the original structural precomposition is naturally
isomorphic to G. The identity component is justified on every
attained AH Hom by GK4BK's real structural preimage. -/
noncomputable def nativeGK4BQAttainedUnitComponent
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    G ≅ ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
      nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G) := by
  refine NatIso.ofComponents (fun X => Iso.refl (G.obj X)) ?_
  intro X Y f
  change G.map f ≫ 𝟙 _ =
    𝟙 _ ≫ G.map ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map
      (nativeGK4BKPreimage p ma mb pa pb X Y f))
  simp only [Category.comp_id, Category.id_comp]
  rw [nativeGK4BKPreimage_spec]
  rfl

/-- At each compatible original structural functor H, the
explicitly chosen factor followed by original observation is
naturally isomorphic to H via actual original F45 components.
Naturality is the GK4BK factor-map theorem on genuine S Hom. -/
noncomputable def nativeGK4BQCompatibleCounitComponent
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H) ≅ H := by
  let i :
      (((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
        nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H).obj) ≅ H.obj :=
    NatIso.ofComponents (fun X => Iso.refl (H.obj.obj X)) (by
      intro X Y f
      change (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙
          nativeGK4BKFactorFunctor p ma mb pa pb H.obj H.property).map f ≫ 𝟙 _ =
        𝟙 _ ≫ H.obj.map f
      simp only [Category.comp_id, Category.id_comp]
      exact nativeGK4BKFactor_map p ma mb pa pb H.obj H.property X Y f)
  exact {
    hom := ObjectProperty.homMk i.hom
    inv := ObjectProperty.homMk i.inv
    hom_inv_id := by
      apply ObjectProperty.hom_ext
      exact i.hom_inv_id
    inv_hom_id := by
      apply ObjectProperty.hom_ext
      exact i.inv_hom_id
  }

/-- A TRUE natural UNIT isomorphism for the actual explicit
GK4BP inverse, on the entire attained AH functor category.
The components are genuine NatIsos, not just object equalities. -/
noncomputable def nativeGK4BQExplicitUnitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    𝟭 (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ≅
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
        nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb := by
  refine NatIso.ofComponents
    (fun G => nativeGK4BQAttainedUnitComponent p ma mb pa pb G) ?_
  intro G H η
  ext X
  change η.app X ≫ 𝟙 _ = 𝟙 _ ≫ η.app X
  simp

/-- A TRUE natural COUNit isomorphism, in the actual GK4BM
compatible FullSubcategory, for the explicit GK4BP inverse. -/
noncomputable def nativeGK4BQExplicitCounitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ≅
      𝟭 (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) := by
  refine NatIso.ofComponents
    (fun H => nativeGK4BQCompatibleCounitComponent p ma mb pa pb H) ?_
  intro H K η
  apply ObjectProperty.hom_ext
  ext X
  change η.hom.app X ≫ 𝟙 _ = 𝟙 _ ≫ η.hom.app X
  simp

/-- This is a new genuine Mathlib equivalence with the
EXPLICIT GK4BP chosen inverse, not the choice-based asEquivalence
inverse. Mathlib Equivalence.mk adjointifies the unit and proves
the required triangle coherence WITHOUT changing either functor. -/
noncomputable def nativeGK4BQExplicitFunctorEquivalence
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ≌
      NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb :=
  CategoryTheory.Equivalence.mk
    (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb)
    (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
    (nativeGK4BQExplicitUnitIso p ma mb pa pb)
    (nativeGK4BQExplicitCounitIso p ma mb pa pb)

/-- The forward of this new equivalence is definitionally
the original GK4BM fully faithful source precomposition. -/
@[simp] theorem nativeGK4BQExplicitFunctorEquivalence_functor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor =
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb := rfl

/-- Its inverse is definitionally the explicit GK4BP factor
functor, not the arbitrary GK4BM asEquivalence inverse. -/
@[simp] theorem nativeGK4BQExplicitFunctorEquivalence_inverse
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).inverse =
      nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb := rfl

/-- The ACTUAL adjusted unit of the explicit equivalence. -/
noncomputable def nativeGK4BQTriangleUnitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    𝟭 (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ≅
      (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor ⋙
        (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).inverse :=
  (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).unitIso

/-- The ACTUAL counit of the new explicit equivalence. -/
noncomputable def nativeGK4BQTriangleCounitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).inverse ⋙
      (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor ≅
        𝟭 (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :=
  (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).counitIso

/-- FORWARD triangle identity, on every genuine attained old-AH
functor G. This is a true equation of Mathlib NatTrans Homs. -/
theorem nativeGK4BQForward_triangle
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor.map
      ((nativeGK4BQTriangleUnitIso p ma mb pa pb).hom.app G) ≫
        (nativeGK4BQTriangleCounitIso p ma mb pa pb).hom.app
          ((nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor.obj G) =
      𝟙 ((nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor.obj G) :=
  (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).functor_unitIso_comp G

/-- INVERSE triangle identity, on every genuine compatible
S ⥤ T functor H, beyond the weaker GK4BP object equalities. -/
theorem nativeGK4BQInverse_triangle
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    (nativeGK4BQTriangleUnitIso p ma mb pa pb).hom.app
      ((nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).inverse.obj H) ≫
    (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).inverse.map
      ((nativeGK4BQTriangleCounitIso p ma mb pa pb).hom.app H) =
    𝟙 ((nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).inverse.obj H) :=
  (nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb).unit_inverse_comp H

/-- The GK4BM choice-based inverse and the GK4BP EXPLICIT
inverse are NATURALLY ISOMORPHIC. This is not equality of
definitions and does not assume target-naturality of the chosen
inverse. The comparison is the pinned Mathlib uniqueness of
quasi-inverses for equivalences with the same forward functor. -/
noncomputable def nativeGK4BQChosenInverseComparisonIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ≅
      nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb := by
  let e := nativeGK4BMCompatibleFunctorEquivalence (T := T) p ma mb pa pb
  let e' := nativeGK4BQExplicitFunctorEquivalence (T := T) p ma mb pa pb
  exact Iso.isoInverseOfIsoFunctor (G := e) (G' := e') (Iso.refl _)

end ExplicitEquivalenceUnitCounit

#print axioms nativeGK4BQAttainedUnitComponent
#print axioms nativeGK4BQCompatibleCounitComponent
#print axioms nativeGK4BQExplicitUnitIso
#print axioms nativeGK4BQExplicitCounitIso
#print axioms nativeGK4BQExplicitFunctorEquivalence
#print axioms nativeGK4BQExplicitFunctorEquivalence_functor
#print axioms nativeGK4BQExplicitFunctorEquivalence_inverse
#print axioms nativeGK4BQTriangleUnitIso
#print axioms nativeGK4BQTriangleCounitIso
#print axioms nativeGK4BQForward_triangle
#print axioms nativeGK4BQInverse_triangle
#print axioms nativeGK4BQChosenInverseComparisonIso

end
end Kuu.F112.Physical
