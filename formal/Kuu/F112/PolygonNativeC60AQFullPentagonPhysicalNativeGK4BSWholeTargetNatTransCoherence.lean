import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BRUnitCounitTargetCoherence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BS — whole-NatTrans target coherence for the
CONCRETE unit and counit of the genuinely explicit attained-AH
category equivalence.

GK4BQ constructs natural unit/counit isomorphisms for the
explicit GK4BP inverse P_T of the original F45 structural
observation precomposition C_T.
GK4BR verifies target R and rho component squares at EVERY
genuinely attained AH / typed original F45 object.
GK4BS lifts those typed component equations into equalities
of entire Mathlib NatTrans Homs, including compatible full-
subcategory morphisms. There is no new raw source 3-cell,
and no assumption that GK4BM's arbitrarily chosen quasi-inverse
is definitionally the explicit GK4BP inverse.

Do not confuse GK4BQ's concrete unadjusted unit with the
adjointified unit selected by CategoryTheory.Equivalence.mk.
No global modification assertion is inferred for the latter
without its own separate Lean proof. Original source S is not
assumed faithful; only original AH-observation-kernel-compatible
source functors are considered. No original Q category laws,
ambient unattained integer matrices, Gray reconstruction,
unfilled F54/F55/P92B Type-valued fillers or hyperdescent.

Strict 空 center; independent Kuu one presentation.
Append-only / tighten-only / overwrite-forbidden / same-root107.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV

section WholeTargetNaturality
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- The true GK4BQ concrete UNIT commutes with ANY target R
as an equality of WHOLE natural transformations on the actual
attained-AH category, not merely on its chosen components. -/
theorem nativeGK4BSWholeUnit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U) :
    Functor.whiskerRight
      ((nativeGK4BQExplicitUnitIso (T := T) p ma mb pa pb).hom.app G) R =
    (nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G) := by
  ext X
  exact (nativeGK4BRWholeUnit_postcompose p ma mb pa pb G R X).symm

/-- The actual compatible full-subcategory COUNit preserves
target R as an equality of WHOLE existing Hom morphisms
(underlying Mathlib natural transformations), not a raw F54
Type-valued comparison. -/
theorem nativeGK4BSWholeCounit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (R : T ⥤ U) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb R).map
      ((nativeGK4BQExplicitCounitIso (T := T) p ma mb pa pb).hom.app H) =
    (nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H) := by
  apply ObjectProperty.hom_ext
  ext X
  exact (nativeGK4BRWholeCounit_postcompose p ma mb pa pb H R X).symm

/-- The GK4BR unit target-NatTrans square is an equality of
WHOLE Mathlib natural transformations, for every real attained
old-AH source functor G and every rho:R⟶R'. -/
theorem nativeGK4BSWholeUnit_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app G ≫
      (nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompAttained p ma mb pa pb R').obj G) =
    (nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G) ≫
      (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app
        ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
          nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G) := by
  ext X
  exact nativeGK4BRUnit_targetNat_square p ma mb pa pb ρ G X

/-- The genuine compatible COUNit rho square is equality of
WHOLE Mathlib FullSubcategory Hom transformations; the .hom
projection is used to compare original fully dependent F45
source natural transformations. -/
theorem nativeGK4BSWholeCounit_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app
      ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
        nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H) ≫
      (nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompCompatible p ma mb pa pb R').obj H) =
    (nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H) ≫
      (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app H := by
  apply ObjectProperty.hom_ext
  ext X
  exact nativeGK4BRCounit_targetNat_square p ma mb pa pb ρ H X

/-- Even the INVERSE of the concrete unit NatIso commutes with
postcomposition at the WHOLE Mathlib natural-transformation level. -/
theorem nativeGK4BSWholeUnitInv_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U) :
    Functor.whiskerRight
      ((nativeGK4BQExplicitUnitIso (T := T) p ma mb pa pb).inv.app G) R =
    (nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).inv.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G) := by
  ext X
  change R.map (𝟙 (G.obj X)) = 𝟙 (R.obj (G.obj X))
  simp

/-- Even the INVERSE of the concrete compatible counit has a
WHOLE Hom-level target-postcomposition equation. -/
theorem nativeGK4BSWholeCounitInv_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (R : T ⥤ U) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb R).map
      ((nativeGK4BQExplicitCounitIso (T := T) p ma mb pa pb).inv.app H) =
    (nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).inv.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H) := by
  apply ObjectProperty.hom_ext
  ext X
  change R.map (𝟙 (H.obj.obj X)) = 𝟙 (R.obj (H.obj.obj X))
  simp

/-- Concrete unit target coherence for TWO genuine target
changes, lifted to equality of WHOLE natural transformations. -/
theorem nativeGK4BSWholeUnit_twoTargets
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U) (Q : U ⥤ V) :
    Functor.whiskerRight
      ((nativeGK4BQExplicitUnitIso (T := T) p ma mb pa pb).hom.app G) (R ⋙ Q) =
    (nativeGK4BQExplicitUnitIso (T := V) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ Q)).obj G) := by
  ext X
  exact (nativeGK4BRUnit_twoTargets p ma mb pa pb G R Q X).symm

/-- Concrete compatible counit coherence for TWO target changes
as an equality of WHOLE actual subcategory morphisms. -/
theorem nativeGK4BSWholeCounit_twoTargets
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (R : T ⥤ U) (Q : U ⥤ V) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ Q)).map
      ((nativeGK4BQExplicitCounitIso (T := T) p ma mb pa pb).hom.app H) =
    (nativeGK4BQExplicitCounitIso (T := V) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ Q)).obj H) := by
  apply ObjectProperty.hom_ext
  ext X
  exact (nativeGK4BRCounit_twoTargets p ma mb pa pb H R Q X).symm


/-- The ADJOINTIFIED unit of GK4BQ's genuine Equivalence has
identity components at every genuinely attained AH object.
The proof uses the actual forward triangle, not any unsupported
definitional equality of source functors: the genuine counit
at the original typed F45 representative is an identity Hom. -/
theorem nativeGK4BSAdjointifiedUnit_component_hom
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    ((nativeGK4BQTriangleUnitIso p ma mb pa pb).hom.app G).app X =
      𝟙 (G.obj X) := by
  have h := nativeGK4BQForward_triangle p ma mb pa pb G
  have hX := congrArg (fun φ => φ.hom.app X.original) h
  change ((nativeGK4BQTriangleUnitIso p ma mb pa pb).hom.app G).app X ≫
      𝟙 (G.obj X) = 𝟙 (G.obj X) at hX
  exact (Category.comp_id
    (((nativeGK4BQTriangleUnitIso p ma mb pa pb).hom.app G).app X)).symm.trans hX

/-- The original concrete GK4BQ unit is ALREADY half-adjoint
for the true explicit inverse. Consequently Mathlib's
adjointification leaves its whole NatIso literally equal,
although this equality was not presumed in GK4BQ/GK4BR. -/
theorem nativeGK4BSAdjointifiedUnit_eq_concrete
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BQTriangleUnitIso (T := T) p ma mb pa pb =
      nativeGK4BQExplicitUnitIso (T := T) p ma mb pa pb := by
  apply Iso.ext
  ext G X
  exact (nativeGK4BSAdjointifiedUnit_component_hom p ma mb pa pb G X).trans
    (nativeGK4BRUnitComponent_hom p ma mb pa pb G X).symm

/-- The ADJOINTIFIED genuine unit, not just its raw precursor,
commutes with arbitrary target postcomposition as equality
of WHOLE NatTrans Homs. -/
theorem nativeGK4BSAdjointifiedUnit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U) :
    Functor.whiskerRight
      ((nativeGK4BQTriangleUnitIso (T := T) p ma mb pa pb).hom.app G) R =
    (nativeGK4BQTriangleUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G) := by
  rw [nativeGK4BSAdjointifiedUnit_eq_concrete (T := T) p ma mb pa pb,
      nativeGK4BSAdjointifiedUnit_eq_concrete (T := U) p ma mb pa pb]
  exact nativeGK4BSWholeUnit_postcompose p ma mb pa pb G R

/-- The GK4BQ ADJOINTIFIED unit has a full Mathlib NatTrans
target-rho square, not only a componentwise identity. -/
theorem nativeGK4BSAdjointifiedUnit_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app G ≫
      (nativeGK4BQTriangleUnitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompAttained p ma mb pa pb R').obj G) =
    (nativeGK4BQTriangleUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G) ≫
      (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app
        ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
          nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G) := by
  rw [nativeGK4BSAdjointifiedUnit_eq_concrete (T := U) p ma mb pa pb]
  exact nativeGK4BSWholeUnit_targetNat_square p ma mb pa pb ρ G

/-- Two successive target functors also preserve the genuine
ADJOINTIFIED unit on the whole attained-AH NatTrans Hom. -/
theorem nativeGK4BSAdjointifiedUnit_twoTargets
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U) (Q : U ⥤ V) :
    Functor.whiskerRight
      ((nativeGK4BQTriangleUnitIso (T := T) p ma mb pa pb).hom.app G) (R ⋙ Q) =
    (nativeGK4BQTriangleUnitIso (T := V) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ Q)).obj G) := by
  rw [nativeGK4BSAdjointifiedUnit_eq_concrete (T := T) p ma mb pa pb,
      nativeGK4BSAdjointifiedUnit_eq_concrete (T := V) p ma mb pa pb]
  exact nativeGK4BSWholeUnit_twoTargets p ma mb pa pb G R Q

end WholeTargetNaturality

#print axioms nativeGK4BSWholeUnit_postcompose
#print axioms nativeGK4BSWholeCounit_postcompose
#print axioms nativeGK4BSWholeUnit_targetNat_square
#print axioms nativeGK4BSWholeCounit_targetNat_square
#print axioms nativeGK4BSWholeUnitInv_postcompose
#print axioms nativeGK4BSWholeCounitInv_postcompose
#print axioms nativeGK4BSWholeUnit_twoTargets
#print axioms nativeGK4BSWholeCounit_twoTargets
#print axioms nativeGK4BSAdjointifiedUnit_component_hom
#print axioms nativeGK4BSAdjointifiedUnit_eq_concrete
#print axioms nativeGK4BSAdjointifiedUnit_postcompose
#print axioms nativeGK4BSAdjointifiedUnit_targetNat_square
#print axioms nativeGK4BSAdjointifiedUnit_twoTargets

end
end Kuu.F112.Physical
