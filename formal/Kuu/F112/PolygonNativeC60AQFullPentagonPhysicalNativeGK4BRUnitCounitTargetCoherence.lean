import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BQExplicitEquivalenceNaturality
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BR — precise target-category naturality of the
CONCRETE GK4BQ unit and counit for the GK4BP explicit inverse.

The original physical F45-dependent S, actually attained old-AH A,
original AH observation F : S ⥤ A and the compatible GK4BM
FullSubcategory remain unchanged. C_T is actual precomposition by F,
P_T is the explicit GK4BP factor functor. GK4BQ constructs genuine
natural unit/counit isomorphisms, an adjointified Equivalence and
a NatIso comparison with the unrelated asEquivalence chosen inverse.

Here the concrete unit/counit component *identity morphisms* are
proved to commute with arbitrary genuine R : T ⥤ U and arbitrary
rho : R ⟶ R', at ALL original typed or genuinely attained objects.
The relevant target naturality squares use GK4BN's actual
whiskering and GK4BO's verified target action. Neither the
choice-based GK4BM inverse nor a source Type-valued 3-cell is
identified definitionally. Adjointified-unit modification coherence
is a separate boundary.

No unconditional S faithfulness, original Q laws, raw F54/F55
higher fillers, ambient unattained integer matrices, Gray structure,
global strict coherence or hyperdescent.
Append-only/tighten-only/overwrite-forbidden/same-root107.
Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 stays Draft/OPEN/unmerged.
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

section ConcreteUnitCounitTargetNaturality
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- The true GK4BQ concrete attained-AH unit has genuine
IDENTITY components on every actually attained AH object. -/
@[simp] theorem nativeGK4BRUnitComponent_hom
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    (nativeGK4BQAttainedUnitComponent p ma mb pa pb G).hom.app X =
      𝟙 (G.obj X) := rfl

/-- Its actual inverse component is also the original identity. -/
@[simp] theorem nativeGK4BRUnitComponent_inv
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    (nativeGK4BQAttainedUnitComponent p ma mb pa pb G).inv.app X =
      𝟙 (G.obj X) := rfl

/-- The true GK4BQ compatible counit has an underlying
identity NatTrans component on EVERY original typed F45 stage. -/
@[simp] theorem nativeGK4BRCounitComponent_hom
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (X : NativeGK4IStage p ma mb pa pb) :
    ((nativeGK4BQCompatibleCounitComponent p ma mb pa pb H).hom).hom.app X =
      𝟙 (H.obj.obj X) := rfl

/-- The inverse of the compatible concrete counit is also
identity on the actual F45 structural source object. -/
@[simp] theorem nativeGK4BRCounitComponent_inv
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (X : NativeGK4IStage p ma mb pa pb) :
    ((nativeGK4BQCompatibleCounitComponent p ma mb pa pb H).inv).hom.app X =
      𝟙 (H.obj.obj X) := rfl

/-- Arbitrary target postcomposition preserves each concrete
attained-AH UNIT component, using only a true R.map_id. -/
theorem nativeGK4BRUnit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    (nativeGK4BQAttainedUnitComponent p ma mb pa pb (G ⋙ R)).hom.app X =
      R.map ((nativeGK4BQAttainedUnitComponent p ma mb pa pb G).hom.app X) := by
  change 𝟙 (R.obj (G.obj X)) = R.map (𝟙 (G.obj X))
  simp

/-- Arbitrary target postcomposition preserves each true
compatible COUNIT component on the original S-side. -/
theorem nativeGK4BRCounit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (R : T ⥤ U)
    (X : NativeGK4IStage p ma mb pa pb) :
    ((nativeGK4BQCompatibleCounitComponent p ma mb pa pb
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H)).hom).hom.app X =
      R.map (((nativeGK4BQCompatibleCounitComponent p ma mb pa pb H).hom).hom.app X) := by
  change 𝟙 (R.obj (H.obj.obj X)) = R.map (𝟙 (H.obj.obj X))
  simp

/-- The *outer* GK4BQ unit NatIso, not only its inner component
Iso, has target-postcomposition naturality at every G and X. -/
theorem nativeGK4BRWholeUnit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    ((nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G)).app X =
    R.map (((nativeGK4BQExplicitUnitIso (T := T) p ma mb pa pb).hom.app G).app X) :=
  nativeGK4BRUnit_postcompose p ma mb pa pb G R X

/-- The outer GK4BQ COUNIT NatIso has the corresponding target
postcomposition law inside the genuine compatible subcategory. -/
theorem nativeGK4BRWholeCounit_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (R : T ⥤ U)
    (X : NativeGK4IStage p ma mb pa pb) :
    (((nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H)).hom).app X =
    R.map ((((nativeGK4BQExplicitCounitIso (T := T) p ma mb pa pb).hom.app H).hom).app X) :=
  nativeGK4BRCounit_postcompose p ma mb pa pb H R X

/-- Target natural transformations preserve the explicit
unit in a genuine two-stage target square at EVERY reached AH
object. Both paths have the original rho.app component. -/
theorem nativeGK4BRUnit_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    ((nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app G).app X ≫
      ((nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompAttained p ma mb pa pb R').obj G)).app X =
    ((nativeGK4BQExplicitUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G)).app X ≫
      ((nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app
        ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
          nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G)).app X := by
  change ρ.app (G.obj X) ≫ 𝟙 _ = 𝟙 _ ≫ ρ.app (G.obj X)
  simp

/-- Target natural transformations preserve the explicit
counit on original F45 typed objects, using genuine compatible
FullSubcategory arrows, not a raw F54 source 3-cell. -/
theorem nativeGK4BRCounit_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (X : NativeGK4IStage p ma mb pa pb) :
    ((nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app
      ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
        nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H)).hom.app X ≫
      (((nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompCompatible p ma mb pa pb R').obj H)).hom).app X =
    (((nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H)).hom).app X ≫
      ((nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app H).hom.app X := by
  change ρ.app (H.obj.obj X) ≫ 𝟙 _ = 𝟙 _ ≫ ρ.app (H.obj.obj X)
  simp

/-- Coherence of the concrete unit with TWO target changes:
R : T ⥤ U and Q : U ⥤ V, at all attained AH objects. -/
theorem nativeGK4BRUnit_twoTargets
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (R : T ⥤ U) (Q : U ⥤ V)
    (X : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    (nativeGK4BQAttainedUnitComponent p ma mb pa pb (G ⋙ (R ⋙ Q))).hom.app X =
      Q.map (R.map ((nativeGK4BQAttainedUnitComponent p ma mb pa pb G).hom.app X)) := by
  change 𝟙 (Q.obj (R.obj (G.obj X))) = Q.map (R.map (𝟙 (G.obj X)))
  simp

/-- Coherence of the concrete counit with TWO target changes
on every real original F45 typed structural object. -/
theorem nativeGK4BRCounit_twoTargets
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (R : T ⥤ U) (Q : U ⥤ V)
    (X : NativeGK4IStage p ma mb pa pb) :
    ((nativeGK4BQCompatibleCounitComponent p ma mb pa pb
      ((nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ Q)).obj H)).hom).hom.app X =
      Q.map (R.map (((nativeGK4BQCompatibleCounitComponent p ma mb pa pb H).hom).hom.app X)) := by
  change 𝟙 (Q.obj (R.obj (H.obj.obj X))) = Q.map (R.map (𝟙 (H.obj.obj X)))
  simp

end ConcreteUnitCounitTargetNaturality

#print axioms nativeGK4BRUnitComponent_hom
#print axioms nativeGK4BRUnitComponent_inv
#print axioms nativeGK4BRCounitComponent_hom
#print axioms nativeGK4BRCounitComponent_inv
#print axioms nativeGK4BRUnit_postcompose
#print axioms nativeGK4BRCounit_postcompose
#print axioms nativeGK4BRWholeUnit_postcompose
#print axioms nativeGK4BRWholeCounit_postcompose
#print axioms nativeGK4BRUnit_targetNat_square
#print axioms nativeGK4BRCounit_targetNat_square
#print axioms nativeGK4BRUnit_twoTargets
#print axioms nativeGK4BRCounit_twoTargets

end
end Kuu.F112.Physical
