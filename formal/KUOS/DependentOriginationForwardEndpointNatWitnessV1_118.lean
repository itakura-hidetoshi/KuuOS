import KUOS.DependentOriginationScaledTerminalRLPV1_41
import KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
import Mathlib.CategoryTheory.Bicategory.Strict.Basic
import Mathlib.AlgebraicTopology.SimplicialSet.Dimension

namespace KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49

noncomputable section

/-!
# Small exact-source B²ℕ witness for the v1.118 forward endpoint cylinder

This source retains the local explicit additive bicategory and thinness
proof constructions of v1.95 and v1.96 (source is retained unchanged).
Only the dependent standard A/B/C separator-certificate imports are omitted.
The comparison-1 Duskin triangle is proved non-thin, not hypothesized.

Original proof sources and author provenance:
DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
-/

/-! ## The one-cell hom-category with additive natural 2-cells -/

/-- The unique 1-cell in the additive double delooping. -/
inductive NatOneCell : Type where
  | star
deriving DecidableEq

namespace NatOneCell

instance : Subsingleton NatOneCell :=
  ⟨by intro x y; cases x; cases y; rfl⟩

/-- The hom-category of 1-cells has `Nat` as every 2-hom set, identity `0`,
and vertical composition given by addition. -/
instance : Category.{0} NatOneCell where
  Hom _ _ := Nat
  id _ := 0
  comp f g := f + g
  id_comp := by intros; exact Nat.zero_add _
  comp_id := by intros; exact Nat.add_zero _
  assoc := by intros; exact Nat.add_assoc _ _ _

@[simp]
theorem id_eq_zero (f : NatOneCell) : (𝟙 f : f ⟶ f) = 0 := rfl

@[simp]
theorem comp_eq_add {f g h : NatOneCell} (α : f ⟶ g) (β : g ⟶ h) :
    α ≫ β = α + β := rfl

end NatOneCell

/-! ## The additive double delooping bicategory -/

/-- The unique object of the additive double delooping. -/
inductive NatDoubleDelooping : Type where
  | star
deriving DecidableEq

namespace NatDoubleDelooping

instance : Subsingleton NatDoubleDelooping :=
  ⟨by intro x y; cases x; cases y; rfl⟩

/-- One object, one 1-cell, and additive natural-number 2-cells form a strict
bicategory.  The exchange law is exactly commutativity of addition. -/
instance : Bicategory.{0,0} NatDoubleDelooping where
  Hom _ _ := NatOneCell
  id _ := NatOneCell.star
  comp _ _ := NatOneCell.star
  homCategory _ _ := inferInstance
  whiskerLeft := by intros; assumption
  whiskerRight := by intros; assumption
  associator _ _ _ := Iso.refl _
  leftUnitor _ := Iso.refl _
  rightUnitor _ := Iso.refl _
  whiskerLeft_id := by intros; rfl
  whiskerLeft_comp := by intros; rfl
  id_whiskerLeft := by intros; simp
  comp_whiskerLeft := by intros; simp
  id_whiskerRight := by intros; rfl
  comp_whiskerRight := by intros; rfl
  whiskerRight_id := by intros; simp
  whiskerRight_comp := by intros; simp
  whisker_assoc := by intros; simp
  whisker_exchange := by
    intros
    change _ + _ = _ + _
    exact Nat.add_comm _ _
  pentagon := by intros; simp
  triangle := by intros; simp

/-- The double delooping is strict: all 1-cell unit and associativity equations
are definitional because there is only one 1-cell. -/
instance : Bicategory.Strict NatDoubleDelooping where
  id_comp _ := rfl
  comp_id _ := rfl
  assoc _ _ _ := rfl
  leftUnitor_eqToIso _ := rfl
  rightUnitor_eqToIso _ := rfl
  associator_eqToIso _ _ _ := rfl

/-- The 2-cell `1` is not invertible in the additive natural hom-category. -/
theorem one_twoCell_not_isIso :
    ¬ IsIso
      (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star) := by
  intro h
  letI : IsIso
      (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star) := h
  have hinv := IsIso.hom_inv_id
    (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star)
  change 1 + inv
      (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star) = 0 at hinv
  omega

end NatDoubleDelooping

/-! ## A normal-lax triangle with comparison `1` -/

/-- The additive comparison attached to a composable pair in `[2]`: it is one
exactly when both steps strictly increase the ordinal, and zero otherwise.
For `Fin 3`, the only such pair is `0 -> 1 -> 2`. -/
def natTriangleMapComp
    {a b c : DuskinOrdinal 2}
    (_f : a ⟶ b) (_g : b ⟶ c) : Nat :=
  if a.as < b.as ∧ b.as < c.as then 1 else 0

/-- The normal-lax core of the concrete non-invertible Duskin triangle. -/
def natNoninvertibleTriangleCore :
    StrictlyUnitaryLaxFunctorCore (DuskinOrdinal 2) NatDoubleDelooping where
  obj _ := NatDoubleDelooping.star
  map _ := NatOneCell.star
  map_id _ := rfl
  map₂ _ := 0
  map₂_id _ := rfl
  map₂_comp _ _ := rfl
  mapComp f g := natTriangleMapComp f g
  mapComp_naturality_left := by
    intros
    simp [natTriangleMapComp]
  mapComp_naturality_right := by
    intros
    simp [natTriangleMapComp]
  map₂_leftUnitor := by
    intros
    simp [natTriangleMapComp]
  map₂_rightUnitor := by
    intros
    simp [natTriangleMapComp]
  map₂_associator := by
    intro a b c d f g h
    have hab : a.as ≤ b.as := f.as.le
    have hbc : b.as ≤ c.as := g.as.le
    have hcd : c.as ≤ d.as := h.as.le
    have ha := a.as.isLt
    have hb := b.as.isLt
    have hc := c.as.isLt
    have hd := d.as.isLt
    simp only [natTriangleMapComp]
    split_ifs <;> omega

/-- The concrete Duskin 2-simplex with comparison label `1`. -/
def natNoninvertibleTriangle :
    DuskinSimplex NatDoubleDelooping 2 :=
  StrictlyUnitaryLaxFunctor.mk' natNoninvertibleTriangleCore

@[simp]
theorem natNoninvertibleTriangle_comparison :
    duskinComparison natNoninvertibleTriangle =
      (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star) := by
  rfl

/-- Its intrinsic comparison 2-cell is not invertible. -/
theorem natNoninvertibleTriangle_comparison_not_isIso :
    ¬ IsIso (duskinComparison natNoninvertibleTriangle) := by
  rw [natNoninvertibleTriangle_comparison]
  exact NatDoubleDelooping.one_twoCell_not_isIso

/-! ## Degeneracy is now the only possible source of thinness -/

/-- For this displayed triangle, Duskin thinness is equivalent to simplicial
degeneracy because the invertible-comparison branch has been ruled out. -/
theorem natNoninvertibleTriangle_thin_iff_degenerate :
    (duskinScaling NatDoubleDelooping).thin natNoninvertibleTriangle ↔
      IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle := by
  change
    (IsIso (duskinComparison natNoninvertibleTriangle) ∨
      IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle) ↔
      IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle
  constructor
  · intro h
    rcases h with hIso | hdeg
    · exact False.elim (natNoninvertibleTriangle_comparison_not_isIso hIso)
    · exact hdeg
  · exact Or.inr

/-- Once nondegeneracy is established, the concrete triangle is non-thin. -/
theorem natNoninvertibleTriangle_not_thin_of_nondegenerate
    (hnd : ¬ IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle) :
    ¬ (duskinScaling NatDoubleDelooping).thin natNoninvertibleTriangle := by
  rw [natNoninvertibleTriangle_thin_iff_degenerate]
  exact hnd

/-- Bundle the concrete global scaled Duskin nerve. -/
def natDoubleDeloopingScaledDuskin : ScaledSSet :=
  ScaledSSet.of
    (duskinNerve NatDoubleDelooping)
    (duskinScaling NatDoubleDelooping)


namespace NatDoubleDelooping

/-- A natural-number 2-cell in the additive double delooping is invertible
exactly when it is zero. -/
theorem twoCell_isIso_iff_eq_zero
    {f g : NatOneCell} (alpha : f ⟶ g) :
    IsIso alpha ↔ alpha = 0 := by
  constructor
  · intro h
    letI : IsIso alpha := h
    have hinv := IsIso.hom_inv_id alpha
    change alpha + inv alpha = 0 at hinv
    omega
  · intro h
    have hfg : f = g := Subsingleton.elim _ _
    subst g
    rw [h]
    change IsIso (𝟙 f)
    infer_instance

/-- Any invertible 2-cell in the additive double delooping is literally zero. -/
theorem isIso_twoCell_eq_zero
    {f g : NatOneCell} (alpha : f ⟶ g) [IsIso alpha] :
    alpha = 0 :=
  (twoCell_isIso_iff_eq_zero alpha).1 inferInstance

end NatDoubleDelooping

/-! ## Locally discrete 2-cells map to zero -/

/-- The source ordinal is locally discrete, so every source 2-cell is an
identity after identifying its endpoints.  Any Duskin simplex into `B^2 N`
therefore sends every source 2-cell to the additive identity `0`. -/
theorem natDuskin_map₂_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} {f g : a ⟶ b}
    (eta : f ⟶ g) :
    sigma.map₂ eta = 0 := by
  have hfg : f = g := LocallyDiscrete.eq_of_hom eta
  subst g
  have heta : eta = 𝟙 f := Subsingleton.elim _ _
  rw [heta, sigma.map₂_id]
  rfl

/-! ## Normality forces identity comparisons to zero -/

/-- The comparison with an identity on the left is zero. -/
theorem natDuskin_mapComp_id_left_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (g : a ⟶ b) :
    sigma.mapComp (𝟙 a) g = 0 := by
  have h := sigma.map₂_leftUnitor g
  have hmap₂ : sigma.map₂ (λ_ g).inv = 0 :=
    natDuskin_map₂_eq_zero sigma _
  have hλ : (λ_ (sigma.map g)).inv = 0 :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  have heq : eqToHom (by rw [sigma.map_id a]) =
      (0 : (sigma.map (𝟙 a)) ⟶ 𝟙 (sigma.obj a)) :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  rw [hmap₂, hλ, heq] at h
  simpa using h.symm

/-- The comparison with an identity on the right is zero. -/
theorem natDuskin_mapComp_id_right_eq_zero
    {n : Nat}
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    sigma.mapComp f (𝟙 b) = 0 := by
  have h := sigma.map₂_rightUnitor f
  have hmap₂ : sigma.map₂ (ρ_ f).inv = 0 :=
    natDuskin_map₂_eq_zero sigma _
  have hρ : (ρ_ (sigma.map f)).inv = 0 :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  have heq : eqToHom (by rw [sigma.map_id b]) =
      (0 : (sigma.map (𝟙 b)) ⟶ 𝟙 (sigma.obj b)) :=
    NatDoubleDelooping.isIso_twoCell_eq_zero _
  rw [hmap₂, hρ, heq] at h
  simpa using h.symm

/-! ## Every comparison in degree one is zero -/

/-- In `[1]`, a composable pair cannot contain two strict increases.  Hence at
least one arrow is an identity, and normality forces every comparison of a
Duskin 1-simplex to be zero. -/
theorem natOneSimplex_mapComp_eq_zero
    (sigma : DuskinSimplex NatDoubleDelooping 1)
    {a b c : DuskinOrdinal 1}
    (f : a ⟶ b) (g : b ⟶ c) :
    sigma.mapComp f g = 0 := by
  have hab : a.as ≤ b.as := f.as.le
  have hbc : b.as ≤ c.as := g.as.le
  have heq : a.as = b.as ∨ b.as = c.as := by
    by_cases h : a.as = b.as
    · exact Or.inl h
    · right
      apply Fin.ext
      have hne : a.as.val ≠ b.as.val := by
        intro hv
        apply h
        exact Fin.ext hv
      have ha := a.as.isLt
      have hb := b.as.isLt
      have hc := c.as.isLt
      omega
  rcases heq with habEq | hbcEq
  · have habObj : a = b := LocallyDiscrete.ext habEq
    subst b
    have hf : f = 𝟙 a := Subsingleton.elim _ _
    rw [hf]
    exact natDuskin_mapComp_id_left_eq_zero sigma g
  · have hbcObj : b = c := LocallyDiscrete.ext hbcEq
    subst c
    have hg : g = 𝟙 b := Subsingleton.elim _ _
    rw [hg]
    exact natDuskin_mapComp_id_right_eq_zero sigma f

/-! ## Degeneracies have zero comparison -/

/-- Either simplicial degeneracy of a Duskin 1-simplex has comparison zero.
The reindexing contribution is also sent to zero because its source is locally
discrete. -/
theorem natDegeneracy_comparison_eq_zero
    (e : DuskinSimplex NatDoubleDelooping 1)
    (i : Fin 2) :
    duskinComparison ((duskinNerve NatDoubleDelooping).σ i e) = 0 := by
  change
    (((duskinReindex (SimplexCategory.σ i).op).comp e).mapComp
      edge01 edge12) = 0
  change
    (e.mapComp
        ((duskinReindex (SimplexCategory.σ i).op).map edge01)
        ((duskinReindex (SimplexCategory.σ i).op).map edge12) ≫
      e.map₂
        ((duskinReindex (SimplexCategory.σ i).op).mapComp edge01 edge12)) = 0
  rw [natOneSimplex_mapComp_eq_zero, natDuskin_map₂_eq_zero]
  rfl

/-- Every degenerate Duskin 2-simplex in `B^2 N` has zero comparison. -/
theorem natDegenerate_comparison_eq_zero
    (sigma : DuskinSimplex NatDoubleDelooping 2)
    (hdeg : IsDegenerateDuskinTwoSimplex sigma) :
    duskinComparison sigma = 0 := by
  rcases hdeg with ⟨e, rfl⟩ | ⟨e, rfl⟩
  · exact natDegeneracy_comparison_eq_zero e 0
  · exact natDegeneracy_comparison_eq_zero e 1

/-! ## Exact thinness characterization -/

/-- In the additive double delooping, the global Duskin scaling is exactly the
zero locus of the comparison label. -/
theorem natDuskin_thin_iff_comparison_eq_zero
    (sigma : DuskinSimplex NatDoubleDelooping 2) :
    (duskinScaling NatDoubleDelooping).thin sigma ↔
      duskinComparison sigma = 0 := by
  change
    (IsIso (duskinComparison sigma) ∨
      IsDegenerateDuskinTwoSimplex sigma) ↔
      duskinComparison sigma = 0
  constructor
  · intro h
    rcases h with hIso | hdeg
    · exact
        (NatDoubleDelooping.twoCell_isIso_iff_eq_zero
          (duskinComparison sigma)).1 hIso
    · exact natDegenerate_comparison_eq_zero sigma hdeg
  · intro hzero
    exact Or.inl
      ((NatDoubleDelooping.twoCell_isIso_iff_eq_zero
        (duskinComparison sigma)).2 hzero)

/-- The comparison-`1` simplex of v1.95 is therefore nondegenerate without any
additional simplicial hypothesis. -/
theorem natNoninvertibleTriangle_nondegenerate :
    ¬ IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle := by
  intro hdeg
  have hzero := natDegenerate_comparison_eq_zero
    natNoninvertibleTriangle hdeg
  rw [natNoninvertibleTriangle_comparison] at hzero
  omega

/-- The same simplex is unconditionally non-thin. -/
theorem natNoninvertibleTriangle_not_thin :
    ¬ (duskinScaling NatDoubleDelooping).thin natNoninvertibleTriangle := by
  rw [natDuskin_thin_iff_comparison_eq_zero,
    natNoninvertibleTriangle_comparison]
  omega


/-! ## Degree-two type-(A) identity triangle, independent of v1.91/v1.93 -/

/-- The Yoneda identity triangle in Δ[2]. -/
def identityTwoSimplex :
    (Δ[2] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.objEquiv.symm (𝟙 ⦋2⦌)

/-- The distinguished type-(A) identity triangle is thin. -/
theorem identityTwoSimplex_isStandardTypeADistinguishedTriangle :
    IsStandardTypeADistinguishedTriangle
      (1 : Fin 3) (identityTwoSimplex : (Δ[2] : SSet).obj (op ⦋2⦌)) := by
  simp [IsStandardTypeADistinguishedTriangle, identityTwoSimplex]

theorem identityTwoSimplex_standardTypeA_thin :
    (standardTypeASimplexScaling (1 : Fin 3)).thin
      (identityTwoSimplex : (Δ[2] : SSet).obj (op ⦋2⦌)) := by
  exact Or.inr identityTwoSimplex_isStandardTypeADistinguishedTriangle


#print axioms natNoninvertibleTriangle_comparison
#print axioms natNoninvertibleTriangle_not_thin
#print axioms identityTwoSimplex_standardTypeA_thin

end
end KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118
