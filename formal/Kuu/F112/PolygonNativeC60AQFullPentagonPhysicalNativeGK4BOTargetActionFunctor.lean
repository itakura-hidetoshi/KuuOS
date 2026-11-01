import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BNTargetPostcompositionNaturality
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BO — the genuine target-functor-category action,
packaged as one Mathlib Functor, with vertical composition and
interchange for actual target natural transformations.

The original independently sourced fully typed F45 structural
category S, its genuinely attained old-AH observation category A,
and the actual kernel-compatible FullSubcategory of S ⥤ T
are those already constructed in GK4BJ–GK4BN.

GK4BN proves postcomposition and the induced natural transformation
separately. GK4BO packages these as a SINGLE true Functor
  (T ⥤ U) ⥤ (Compatible(S,T) ⥤ Compatible(S,U)),
checks target identity and vertical composition, and verifies
Mathlib's interchange on the genuine compatible categories.
The analogous attained-AH action is the pinned Mathlib
whiskeringRight functor itself. The GK4BM forward equivalence
square remains strict on target transformations.

This bounded 1-category/functor-category statement does NOT
assert unconditional faithfulness of S, new F54/F55 raw Type
equalities, source-Q category laws, an equivalence of S and A,
unattained ambient integer matrices, global 3-cells,
Gray coherence or higher hyperdescent.

Append-only / tighten-only / overwrite-forbidden / same-root107.
Strict 空 center, independent Kuu one presentation, no Gray.
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
universe uD vD uE vE uT vT uU vU uV vV

section TargetActionFunctor
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- The *single genuine Mathlib functor* packaging GK4BN's
postcomposition on compatible objects AND its action on all
target natural transformations, with both category laws. -/
def nativeGK4BOTargetActionCompatible
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (T ⥤ U) ⥤
      (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
        NativeGK4BMCompatibleFunctorCategory (T := U) p ma mb pa pb) where
  obj R := nativeGK4BNPostcompCompatible p ma mb pa pb R
  map ρ := nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ
  map_id := by
    intro R
    apply NatTrans.ext
    intro H
    apply ObjectProperty.hom_ext
    rfl
  map_comp := by
    intro R R' R'' ρ σ
    apply NatTrans.ext
    intro H
    apply ObjectProperty.hom_ext
    rfl

/-- The genuinely attained old-AH target action is the full pinned
Mathlib whiskeringRight Functor, not an imitation on raw paths. -/
def nativeGK4BOTargetActionAttained
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (T ⥤ U) ⥤
      ((NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ⥤
        (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ U)) :=
  Functor.whiskeringRight _ _ _

/-- The new packaged object action is the SAME GK4BN
compatible postcomposition functor, definitionally. -/
@[simp] theorem nativeGK4BOTargetActionCompatible_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    (nativeGK4BOTargetActionCompatible p ma mb pa pb).obj R =
      nativeGK4BNPostcompCompatible p ma mb pa pb R := rfl

/-- The new packaged Hom action is the SAME GK4BN target
natural transformation, not a synthetic higher cell. -/
@[simp] theorem nativeGK4BOTargetActionCompatible_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    (nativeGK4BOTargetActionCompatible p ma mb pa pb).map ρ =
      nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ := rfl

/-- The actual attained-AH object action agrees with GK4BN. -/
@[simp] theorem nativeGK4BOTargetActionAttained_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    (nativeGK4BOTargetActionAttained p ma mb pa pb).obj R =
      nativeGK4BNPostcompAttained p ma mb pa pb R := rfl

/-- The actual attained-AH transformation action agrees with
GK4BN and the pinned Mathlib whiskeringRight. -/
@[simp] theorem nativeGK4BOTargetActionAttained_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    (nativeGK4BOTargetActionAttained p ma mb pa pb).map ρ =
      nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ := rfl

/-- Target IDENTITY transformations act as real identity
natural transformations of the compatible postcomposition. -/
theorem nativeGK4BOTargetActionCompatible_map_id
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    nativeGK4BNPostcompCompatibleNat p ma mb pa pb (𝟙 R) =
      𝟙 (nativeGK4BNPostcompCompatible p ma mb pa pb R) := by
  change (nativeGK4BOTargetActionCompatible p ma mb pa pb).map (𝟙 R) =
    𝟙 ((nativeGK4BOTargetActionCompatible p ma mb pa pb).obj R)
  exact (nativeGK4BOTargetActionCompatible p ma mb pa pb).map_id R

/-- VERTICAL COMPOSITION of real target transformations is
preserved as equality of whole natural transformations. -/
theorem nativeGK4BOTargetActionCompatible_map_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' R'' : T ⥤ U}
    (ρ : R ⟶ R') (σ : R' ⟶ R'') :
    nativeGK4BNPostcompCompatibleNat p ma mb pa pb (ρ ≫ σ) =
      nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ ≫
        nativeGK4BNPostcompCompatibleNat p ma mb pa pb σ := by
  change (nativeGK4BOTargetActionCompatible p ma mb pa pb).map (ρ ≫ σ) =
    (nativeGK4BOTargetActionCompatible p ma mb pa pb).map ρ ≫
      (nativeGK4BOTargetActionCompatible p ma mb pa pb).map σ
  exact (nativeGK4BOTargetActionCompatible p ma mb pa pb).map_comp ρ σ

/-- The GK4BM forward equivalence's STRICT naturality square
is compatible with both fully packaged target-action functors.
No pseudo-natural inverse is assumed or invented. -/
theorem nativeGK4BOForward_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    Functor.whiskerLeft
      (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb)
      ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map ρ) =
    Functor.whiskerRight
      ((nativeGK4BOTargetActionAttained p ma mb pa pb).map ρ)
      (nativeGK4BMPrecompositionLift (T := U) p ma mb pa pb) := by
  exact nativeGK4BNPostcomp_nat_square p ma mb pa pb ρ

/-- INTERCHANGE for genuine target natural transformations.
Two target changes T -> U -> V can be pasted in either order.
This is a real equality of natural transformations between
functors on the compatible Mathlib full-subcategories.
No F54 raw Type-valued 3-cell is added. -/
theorem nativeGK4BOTargetAction_interchange
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {Q Q' : U ⥤ V} (σ : Q ⟶ Q') :
    Functor.whiskerRight
      ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map ρ)
      ((nativeGK4BOTargetActionCompatible p ma mb pa pb).obj Q) ≫
      Functor.whiskerLeft
        ((nativeGK4BOTargetActionCompatible p ma mb pa pb).obj R')
        ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map σ) =
    Functor.whiskerLeft
      ((nativeGK4BOTargetActionCompatible p ma mb pa pb).obj R)
      ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map σ) ≫
      Functor.whiskerRight
        ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map ρ)
        ((nativeGK4BOTargetActionCompatible p ma mb pa pb).obj Q') := by
  exact (Functor.whiskerLeft_comp_whiskerRight
    ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map ρ)
    ((nativeGK4BOTargetActionCompatible p ma mb pa pb).map σ)).symm

/-- At target identity functors the packaged action retains
GK4BN's exact strict object-and-Hom identity law. -/
theorem nativeGK4BOTargetAction_strict_id
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BOTargetActionCompatible p ma mb pa pb).obj (𝟭 T) =
      𝟭 (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :=
  nativeGK4BNPostcompCompatible_id p ma mb pa pb

/-- Two successive genuine target functors retain strict
whole-functor composition under the packaged action. -/
theorem nativeGK4BOTargetAction_strict_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (Q : U ⥤ V) :
    (nativeGK4BOTargetActionCompatible p ma mb pa pb).obj (R ⋙ Q) =
      (nativeGK4BOTargetActionCompatible p ma mb pa pb).obj R ⋙
        (nativeGK4BOTargetActionCompatible p ma mb pa pb).obj Q :=
  nativeGK4BNPostcompCompatible_comp p ma mb pa pb R Q

end TargetActionFunctor

#print axioms nativeGK4BOTargetActionCompatible
#print axioms nativeGK4BOTargetActionAttained
#print axioms nativeGK4BOTargetActionCompatible_obj
#print axioms nativeGK4BOTargetActionCompatible_map
#print axioms nativeGK4BOTargetActionAttained_obj
#print axioms nativeGK4BOTargetActionAttained_map
#print axioms nativeGK4BOTargetActionCompatible_map_id
#print axioms nativeGK4BOTargetActionCompatible_map_comp
#print axioms nativeGK4BOForward_targetNat_square
#print axioms nativeGK4BOTargetAction_interchange
#print axioms nativeGK4BOTargetAction_strict_id
#print axioms nativeGK4BOTargetAction_strict_comp

end
end Kuu.F112.Physical
