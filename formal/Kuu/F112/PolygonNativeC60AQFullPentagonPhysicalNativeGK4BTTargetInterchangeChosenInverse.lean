import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BSWholeTargetNatTransCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BT — real vertical and horizontal target
natural-transformation pasting coherence of the entire explicit
old-AH unit/counit, and a NATURAL ISO target-change comparison
for the arbitrary choice-based GK4BM quasi-inverse.

GK4BJ: original fully F45-dependent independent structural S
and genuine attained old-AH category A, with the true observer.
GK4BM: actual AH-kernel-compatible FullSubcategory Comp_T and
forward precomposition C_T.
GK4BP: explicitly constructed factorization inverse P_T, strictly
natural under target functors and target natural transformations.
GK4BQ: true natural unit/counit, equivalence triangles, and a
genuine NatIso k_T : Q_T ≅ P_T from the arbitrary GK4BM
choice-based inverse Q_T to the explicit inverse P_T.
GK4BO: complete target-functor-category action and genuine
target NatTrans identity, vertical composition and interchange.
GK4BS: whole-NatTrans unit/counit target squares, and equality
of this specific adjointified and concrete unit.

Here target changes and transformations are pasted *inside the
existing Mathlib functor categories*, not as invented original
raw F54/F55/P92B 3-cells. The choice inverse is transported
via its actual NatIso comparison, NEVER claimed definitionally
strict under arbitrary target postcomposition.

No unconditional original S faithfulness, original Q category laws,
unattained integer matrices, global Gray coherence or hyperdescent.
Strict 空 center, independent Kuu one presentation, no Gray.
Append-only / tighten-only / overwrite-forbidden / same-root107.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only PR #1558 Draft/OPEN/unmerged.
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

section TargetPastingAndChosenInverse
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- Actual attained-AH target-action natural transformations
respect identity as WHOLE Mathlib NatTrans. -/
theorem nativeGK4BTAttainedNat_id
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    nativeGK4BNPostcompAttainedNat p ma mb pa pb (𝟙 R) =
      𝟙 (nativeGK4BNPostcompAttained p ma mb pa pb R) := by
  change (nativeGK4BOTargetActionAttained p ma mb pa pb).map (𝟙 R) =
    𝟙 ((nativeGK4BOTargetActionAttained p ma mb pa pb).obj R)
  exact (nativeGK4BOTargetActionAttained p ma mb pa pb).map_id R

/-- Actual attained-AH target action respects VERTICAL
composition, as equality of entire natural transformations. -/
theorem nativeGK4BTAttainedNat_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' R'' : T ⥤ U}
    (ρ : R ⟶ R') (σ : R' ⟶ R'') :
    nativeGK4BNPostcompAttainedNat p ma mb pa pb (ρ ≫ σ) =
      nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ ≫
        nativeGK4BNPostcompAttainedNat p ma mb pa pb σ := by
  change (nativeGK4BOTargetActionAttained p ma mb pa pb).map (ρ ≫ σ) =
    (nativeGK4BOTargetActionAttained p ma mb pa pb).map ρ ≫
      (nativeGK4BOTargetActionAttained p ma mb pa pb).map σ
  exact (nativeGK4BOTargetActionAttained p ma mb pa pb).map_comp ρ σ

/-- Compatible full-subcategory target natural transformations
respect VERTICAL composition as genuine Mathlib NatTrans. -/
theorem nativeGK4BTCompatibleNat_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' R'' : T ⥤ U}
    (ρ : R ⟶ R') (σ : R' ⟶ R'') :
    nativeGK4BNPostcompCompatibleNat p ma mb pa pb (ρ ≫ σ) =
      nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ ≫
        nativeGK4BNPostcompCompatibleNat p ma mb pa pb σ :=
  nativeGK4BOTargetActionCompatible_map_comp p ma mb pa pb ρ σ

/-- Genuine vertical pasting of TWO target transformations
is compatible with the entire ADJOINTIFIED GK4BQ unit on the
actually attained old-AH functor category. -/
theorem nativeGK4BTUnit_vertical_pasting
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' R'' : T ⥤ U}
    (ρ : R ⟶ R') (σ : R' ⟶ R'')
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    ((nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app G ≫
      (nativeGK4BNPostcompAttainedNat p ma mb pa pb σ).app G) ≫
      (nativeGK4BQTriangleUnitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompAttained p ma mb pa pb R'').obj G) =
    (nativeGK4BQTriangleUnitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb R).obj G) ≫
      ((nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app
        ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
          nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G) ≫
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb σ).app
          ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
            nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G)) := by
  have h := nativeGK4BSAdjointifiedUnit_targetNat_square
    p ma mb pa pb (ρ ≫ σ) G
  rw [nativeGK4BTAttainedNat_comp p ma mb pa pb ρ σ] at h
  simpa only [NatTrans.comp_app] using h

/-- Genuine vertical pasting of TWO target natural transformations
is compatible with the whole GK4BQ counit, in the actual
AH-kernel-compatible Mathlib FullSubcategory (not raw S Homs). -/
theorem nativeGK4BTCounit_vertical_pasting
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' R'' : T ⥤ U}
    (ρ : R ⟶ R') (σ : R' ⟶ R'')
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    ((nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app
      ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
        nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H) ≫
      (nativeGK4BNPostcompCompatibleNat p ma mb pa pb σ).app
        ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
          nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H)) ≫
      (nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompCompatible p ma mb pa pb R'').obj H) =
    (nativeGK4BQExplicitCounitIso (T := U) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H) ≫
      ((nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app H ≫
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb σ).app H) := by
  have h := nativeGK4BSWholeCounit_targetNat_square p ma mb pa pb (ρ ≫ σ) H
  rw [nativeGK4BTCompatibleNat_comp p ma mb pa pb ρ σ] at h
  simpa only [NatTrans.comp_app] using h

/-- The two horizontal pasting presentations of genuine target
rho and sigma yield EXACTLY THE SAME whole attained-AH target
action NatTrans. The only interchange is pinned Mathlib's. -/
theorem nativeGK4BTAttained_horizontal_interchange
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {Q Q' : U ⥤ V} (σ : Q ⟶ Q') :
    nativeGK4BNPostcompAttainedNat p ma mb pa pb
      (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ) =
    nativeGK4BNPostcompAttainedNat p ma mb pa pb
      (Functor.whiskerLeft R σ ≫ Functor.whiskerRight ρ Q') := by
  exact congrArg
    (fun τ : (R ⋙ Q) ⟶ (R' ⋙ Q') =>
      nativeGK4BNPostcompAttainedNat p ma mb pa pb τ)
    (Functor.whiskerLeft_comp_whiskerRight ρ σ).symm

/-- The SAME horizontal interchange at the original genuinely
compatible FullSubcategory target-action NatTrans level. -/
theorem nativeGK4BTCompatible_horizontal_interchange
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {Q Q' : U ⥤ V} (σ : Q ⟶ Q') :
    nativeGK4BNPostcompCompatibleNat p ma mb pa pb
      (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ) =
    nativeGK4BNPostcompCompatibleNat p ma mb pa pb
      (Functor.whiskerLeft R σ ≫ Functor.whiskerRight ρ Q') := by
  exact congrArg
    (fun τ : (R ⋙ Q) ⟶ (R' ⋙ Q') =>
      nativeGK4BNPostcompCompatibleNat p ma mb pa pb τ)
    (Functor.whiskerLeft_comp_whiskerRight ρ σ).symm

/-- The genuine horizontally composed target transformation
pastes with the FULL ADJOINTIFIED unit at every original
attained-AH functor G, with both endpoint functor changes. -/
theorem nativeGK4BTUnit_horizontal_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {Q Q' : U ⥤ V} (σ : Q ⟶ Q')
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    (nativeGK4BNPostcompAttainedNat p ma mb pa pb
      (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ)).app G ≫
      (nativeGK4BQTriangleUnitIso (T := V) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompAttained p ma mb pa pb (R' ⋙ Q')).obj G) =
    (nativeGK4BQTriangleUnitIso (T := V) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ Q)).obj G) ≫
      (nativeGK4BNPostcompAttainedNat p ma mb pa pb
        (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ)).app
          ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
            nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb).obj G) :=
  nativeGK4BSAdjointifiedUnit_targetNat_square
    p ma mb pa pb (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ) G

/-- The horizontally composed target transformation preserves
the full compatible-category COUNit square on all genuine
original typed F45 functor Homs. -/
theorem nativeGK4BTCounit_horizontal_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {Q Q' : U ⥤ V} (σ : Q ⟶ Q')
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
      (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ)).app
        ((nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
          nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj H) ≫
      (nativeGK4BQExplicitCounitIso (T := V) p ma mb pa pb).hom.app
        ((nativeGK4BNPostcompCompatible p ma mb pa pb (R' ⋙ Q')).obj H) =
    (nativeGK4BQExplicitCounitIso (T := V) p ma mb pa pb).hom.app
      ((nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ Q)).obj H) ≫
      (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
        (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ)).app H :=
  nativeGK4BSWholeCounit_targetNat_square
    p ma mb pa pb (Functor.whiskerRight ρ Q ≫ Functor.whiskerLeft R' σ) H

/-- Unlike an unsupported STRICT target postcomposition equation
for GK4BM's arbitrary choice-based quasi-inverse, this is a
GENUINE WHOLE Mathlib NATURAL ISOMORPHISM. It is obtained by
transport through the existing GK4BQ comparison with the
explicit inverse and the strict GK4BP factorization square. -/
noncomputable def nativeGK4BTChosenInverse_targetNatIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb R ⋙
      nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb R) :=
  Functor.isoWhiskerLeft
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BQChosenInverseComparisonIso (T := U) p ma mb pa pb) ≪≫
  eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R) ≪≫
  Functor.isoWhiskerRight
    (nativeGK4BQChosenInverseComparisonIso (T := T) p ma mb pa pb).symm
    (nativeGK4BNPostcompAttained p ma mb pa pb R)

/-- The transported chosen-inverse target comparison is
natural on ALL actual compatible source-functor natural
transformations; no chosen reverse-functor strictness is used. -/
theorem nativeGK4BTChosenInverse_targetNatIso_naturality
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb R ⋙
      nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb).map η ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom.app K =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom.app H ≫
      (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
        nativeGK4BNPostcompAttained p ma mb pa pb R).map η :=
  (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom.naturality η

end TargetPastingAndChosenInverse

#print axioms nativeGK4BTAttainedNat_id
#print axioms nativeGK4BTAttainedNat_comp
#print axioms nativeGK4BTCompatibleNat_comp
#print axioms nativeGK4BTUnit_vertical_pasting
#print axioms nativeGK4BTCounit_vertical_pasting
#print axioms nativeGK4BTAttained_horizontal_interchange
#print axioms nativeGK4BTCompatible_horizontal_interchange
#print axioms nativeGK4BTUnit_horizontal_square
#print axioms nativeGK4BTCounit_horizontal_square
#print axioms nativeGK4BTChosenInverse_targetNatIso
#print axioms nativeGK4BTChosenInverse_targetNatIso_naturality

end
end Kuu.F112.Physical
