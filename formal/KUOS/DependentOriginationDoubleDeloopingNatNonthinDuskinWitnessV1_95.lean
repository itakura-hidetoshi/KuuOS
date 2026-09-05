import KUOS.DependentOriginationAtomicTwoSimplexUniversalScalingObstructionV1_94
import Mathlib.CategoryTheory.Bicategory.Strict.Basic

namespace KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationPresentationIndependentInvariantV1_25
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationAtomicTwoSimplexUniversalScalingObstructionV1_94

/-!
# A concrete additive double-delooping non-thin Duskin witness v1.95

Version v1.94 reduced the complete arbitrary-scaling obstruction to a single
question: does every standard A/B/C-right map reflect thin 2-simplices?  To
separate the standard and canonical presentations it is therefore enough to
produce one standard-right map carrying one non-thin source triangle to a thin
target triangle.

This file makes the *geometric witness* completely concrete before attacking
its remaining standard-rightness theorem.

We construct the strict additive double delooping

```text
B^2 N
```

with one object, one 1-cell, and natural numbers as 2-endomorphisms.  Vertical
composition and both whiskerings are additive.  The only invertible 2-cell is
zero.  We then construct a normal-lax `Delta[2]`-simplex whose unique genuine
composition comparison is `1`.

Thus the comparison 2-cell is provably non-invertible.  The file also packages
the exact implication needed by v1.94: once the terminal map of this concrete
scaled Duskin nerve is proved standard A/B/C-right and the displayed triangle
is proved nondegenerate, canonical-to-standard comparison fails.

No standard fibrancy of this model is asserted here without its A/B/C lifting
proof.  No presentation inequality is concluded unconditionally.
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
instance : Category NatOneCell where
  Hom _ _ := Nat
  id _ := 0
  comp f g := f + g
  id_comp := by
    intro X Y f
    exact Nat.zero_add f
  comp_id := by
    intro X Y f
    exact Nat.add_zero f
  assoc := by
    intro W X Y Z f g h
    exact Nat.add_assoc f g h

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
instance : Bicategory NatDoubleDelooping where
  Hom _ _ := NatOneCell
  id _ := NatOneCell.star
  comp _ _ := NatOneCell.star
  homCategory _ _ := inferInstance
  whiskerLeft {_ _ _} _ {_ _} η := by
    change Nat at η ⊢
    exact η
  whiskerRight {_ _ _} {_ _} η _ := by
    change Nat at η ⊢
    exact η
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
  change
    (1 : Nat) +
      (inv (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star) : Nat) = 0
      at hinv
  omega

end NatDoubleDelooping

/-! ## A normal-lax triangle with comparison `1` -/

/-- The additive comparison attached to a composable pair in `[2]`: it is one
exactly when both steps strictly increase the ordinal, and zero otherwise.
For `Fin 3`, the only such pair is `0 -> 1 -> 2`. -/
def natTriangleMapComp
    {a b c : DuskinOrdinal 2}
    (_f : a ⟶ b) (_g : b ⟶ c) : Nat :=
  if a.as < b.as then
    if b.as < c.as then 1 else 0
  else 0

/-- The comparison labels satisfy the normal-lax associativity equation on
all nondecreasing quadruples of vertices in `[2]`. -/
theorem natTriangleMapComp_cocycle
    {a b c d : DuskinOrdinal 2}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d) :
    natTriangleMapComp f g + natTriangleMapComp (f ≫ g) h =
      natTriangleMapComp g h + natTriangleMapComp f (g ≫ h) := by
  have hab : a.as ≤ b.as := f.as.le
  have hbc : b.as ≤ c.as := g.as.le
  have hcd : c.as ≤ d.as := h.as.le
  by_cases habEq : a.as = b.as
  · have habObj : a = b := LocallyDiscrete.ext habEq
    subst b
    simp [natTriangleMapComp]
  by_cases hbcEq : b.as = c.as
  · have hbcObj : b = c := LocallyDiscrete.ext hbcEq
    subst c
    simp [natTriangleMapComp]
  by_cases hcdEq : c.as = d.as
  · have hcdObj : c = d := LocallyDiscrete.ext hcdEq
    subst d
    simp [natTriangleMapComp]
  have hablt : a.as < b.as := by omega
  have hbclt : b.as < c.as := by omega
  have hcdlt : c.as < d.as := by omega
  have haclt : a.as < c.as := lt_trans hablt hbclt
  have hbdlt : b.as < d.as := lt_trans hbclt hcdlt
  simp [natTriangleMapComp, hablt, hbclt, hcdlt, haclt, hbdlt]

/-- The normal-lax core of the concrete non-invertible Duskin triangle. -/
def natNoninvertibleTriangleCore :
    StrictlyUnitaryLaxFunctorCore (DuskinOrdinal 2) NatDoubleDelooping where
  obj _ := NatDoubleDelooping.star
  map _ := NatOneCell.star
  map_id _ := rfl
  map₂ _ := by
    change Nat
    exact 0
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
    change
      natTriangleMapComp f g + natTriangleMapComp (f ≫ g) h + 0 =
        0 + natTriangleMapComp g h + natTriangleMapComp f (g ≫ h)
    simpa only [Nat.add_zero, Nat.zero_add] using
      natTriangleMapComp_cocycle f g h

/-- The concrete Duskin 2-simplex with comparison label `1`. -/
def natNoninvertibleTriangle :
    DuskinSimplex NatDoubleDelooping 2 :=
  StrictlyUnitaryLaxFunctor.mk' natNoninvertibleTriangleCore

@[simp]
theorem natNoninvertibleTriangle_comparison :
    duskinComparison natNoninvertibleTriangle =
      (1 : (NatOneCell.star : NatOneCell) ⟶ NatOneCell.star) := by
  change natTriangleMapComp edge01 edge12 = 1
  simp [natTriangleMapComp, edge01, edge12]

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
def natDoubleDeloopingScaledDuskin : ScaledSSet.{0} :=
  ScaledSSet.of
    (duskinNerve NatDoubleDelooping)
    (duskinScaling NatDoubleDelooping)

/-! ## Exact remaining separation certificate -/

/-- A theorem-level certificate isolates the only two facts still needed to
turn the concrete additive model into a strict standard/canonical separator:
nondegeneracy of the displayed comparison-`1` triangle, and standard A/B/C
terminal fibrancy of the model. -/
structure NatDoubleDeloopingStandardSeparatorCertificate : Prop where
  nondegenerate :
    ¬ IsDegenerateDuskinTwoSimplex natNoninvertibleTriangle
  standardRight :
    (standardGeneratedScaledAnodyneABC :
      MorphismProperty (ScaledSSet.{0})).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)

/-- A completed certificate immediately gives a standard-right map which fails
thinness reflection. -/
theorem certificate_terminal_not_reflects
    (C : NatDoubleDeloopingStandardSeparatorCertificate) :
    ¬ ReflectsThinTwoSimplices
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  apply (not_reflectsThinTwoSimplices_iff_exists
    (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)).2
  refine ⟨natNoninvertibleTriangle, ?_, ?_⟩
  · exact ScaledSimplicialSet.maximal_thin _ _
  · exact natNoninvertibleTriangle_not_thin_of_nondegenerate C.nondegenerate

/-- Therefore the certificate opens the entire v1.94 pure-scaling waypoint. -/
theorem not_standardArbitraryScalingObstructionClosed_of_certificate
    (C : NatDoubleDeloopingStandardSeparatorCertificate) :
    ¬ StandardArbitraryScalingObstructionClosed.{0} := by
  apply
    (not_standardArbitraryScalingObstructionClosed_iff_exists_standardRight_nonreflecting.{0}).2
  refine ⟨natDoubleDeloopingScaledDuskin, ScaledSSet.point,
    ScaledSSet.toPoint natDoubleDeloopingScaledDuskin,
    natNoninvertibleTriangle, C.standardRight, ?_, ?_⟩
  · exact ScaledSimplicialSet.maximal_thin _ _
  · exact natNoninvertibleTriangle_not_thin_of_nondegenerate C.nondegenerate

/-- In particular the same certificate disproves the forward presentation
order `canonical <= standard`. -/
theorem not_canonicalKuuOS_le_standardABC_of_certificate
    (C : NatDoubleDeloopingStandardSeparatorCertificate) :
    ¬ canonicalKuuOSPresentation.{0} ≤ standardABCPresentation.{0} := by
  exact not_canonicalKuuOS_le_standardABC_of_standardRLP_nonreflecting.{0}
    C.standardRight natNoninvertibleTriangle
    (ScaledSimplicialSet.maximal_thin _ _)
    (natNoninvertibleTriangle_not_thin_of_nondegenerate C.nondegenerate)

/-!
The abstract obstruction has now been reduced to a concrete arithmetic model:

```text
B^2 N
  one object
  one 1-cell
  2-cells = N under addition

sigma : Delta[2] -> B^2 N
  comparison(sigma) = 1
  1 is not invertible

remaining concrete obligations:
  (1) sigma is nondegenerate;
  (2) N_D(B^2 N) -> * is standard A/B/C-right.

(1) is a finite simplicial calculation.  (2) is the substantive standard
scaled-anodyne fibrancy theorem; in this additive strict model its coherence
reduces to finite equations in natural-number addition.
```

No part of (2) is hidden in the certificate or promoted to an axiom: the
certificate is only an interface whose fields must be supplied by later Lean
theorems before either separation conclusion can be instantiated.
-/

end KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
