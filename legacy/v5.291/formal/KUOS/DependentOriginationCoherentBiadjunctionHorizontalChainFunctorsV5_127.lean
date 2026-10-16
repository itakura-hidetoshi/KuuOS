import KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalChainFunctorsV5_127

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic

set_option autoImplicit false
noncomputable section

/-!
# F30 / v5.127: horizontal whiskering as native finite-chain functors

Neither horizontal functor is obtained by discarding the intermediate
comparisons. Instead, each maps all successive 2-isomorphisms on the
F side and arbitrary, potentially NONINVERTIBLE, G-side 2-cells,
preserving genuine typed finite concatenation and its composite.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Actual horizontal left-whiskering of EVERY comparison stage. -/
def leftWhiskerChain
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG) :
    BiComparisonChain fF fG kF kG →
      BiComparisonChain (uF ≫ fF) (uG ≫ fG) (uF ≫ kF) (uG ≫ kG)
  | .nil => .nil
  | .snoc previous p q => .snoc (leftWhiskerChain uF uG previous)
      (Bicategory.whiskerLeftIso uF p) (uG ◁ q)

/-- Actual horizontal right-whiskering of EVERY comparison stage. -/
def rightWhiskerChain
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG) :
    BiComparisonChain fF fG kF kG →
      BiComparisonChain (fF ≫ vF) (fG ≫ vG) (kF ≫ vF) (kG ≫ vG)
  | .nil => .nil
  | .snoc previous p q => .snoc (rightWhiskerChain vF vG previous)
      (Bicategory.whiskerRightIso p vF) (q ▷ vG)

/-- The true original F-side ISO composite of left-whiskered
finite chains is the whisker of the original ISO composite. -/
theorem leftWhiskerChain_fComposite
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (c : BiComparisonChain fF fG kF kG) :
    (leftWhiskerChain uF uG c).fComposite =
      Bicategory.whiskerLeftIso uF c.fComposite := by
  induction c with
  | nil =>
      apply Iso.ext
      change (𝟙 (uF ≫ fF)) = uF ◁ (𝟙 fF)
      exact (Bicategory.whiskerLeft_id uF fF).symm
  | snoc previous p q ih =>
      change ((leftWhiskerChain uF uG previous).fComposite).trans
        (Bicategory.whiskerLeftIso uF p) =
          Bicategory.whiskerLeftIso uF (previous.fComposite.trans p)
      rw [ih]
      apply Iso.ext
      change (uF ◁ previous.fComposite.hom) ≫ (uF ◁ p.hom) =
        uF ◁ (previous.fComposite.hom ≫ p.hom)
      exact (Bicategory.whiskerLeft_comp uF _ _).symm

/-- Noninvertible G-side forward composite is preserved under left whiskering. -/
theorem leftWhiskerChain_gComposite
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (c : BiComparisonChain fF fG kF kG) :
    (leftWhiskerChain uF uG c).gComposite =
      uG ◁ c.gComposite := by
  induction c with
  | nil =>
      change (𝟙 (uG ≫ fG)) = uG ◁ (𝟙 fG)
      exact (Bicategory.whiskerLeft_id uG fG).symm
  | snoc previous p q ih =>
      change (leftWhiskerChain uF uG previous).gComposite ≫
        uG ◁ q = uG ◁ (previous.gComposite ≫ q)
      rw [ih]
      exact (Bicategory.whiskerLeft_comp uG _ _).symm

/-- Original F composite ISO is preserved under right whiskering. -/
theorem rightWhiskerChain_fComposite
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (c : BiComparisonChain fF fG kF kG) :
    (rightWhiskerChain vF vG c).fComposite =
      Bicategory.whiskerRightIso c.fComposite vF := by
  induction c with
  | nil =>
      apply Iso.ext
      change (𝟙 (fF ≫ vF)) = (𝟙 fF) ▷ vF
      exact (Bicategory.id_whiskerRight fF vF).symm
  | snoc previous p q ih =>
      change ((rightWhiskerChain vF vG previous).fComposite).trans
        (Bicategory.whiskerRightIso p vF) =
          Bicategory.whiskerRightIso (previous.fComposite.trans p) vF
      rw [ih]
      apply Iso.ext
      change (previous.fComposite.hom ▷ vF) ≫ (p.hom ▷ vF) =
        (previous.fComposite.hom ≫ p.hom) ▷ vF
      exact (Bicategory.comp_whiskerRight _ _ vF).symm

/-- Original G composite 2-cell is preserved under right whiskering. -/
theorem rightWhiskerChain_gComposite
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (c : BiComparisonChain fF fG kF kG) :
    (rightWhiskerChain vF vG c).gComposite =
      c.gComposite ▷ vG := by
  induction c with
  | nil =>
      change (𝟙 (fG ≫ vG)) = (𝟙 fG) ▷ vG
      exact (Bicategory.id_whiskerRight fG vG).symm
  | snoc previous p q ih =>
      change (rightWhiskerChain vF vG previous).gComposite ≫
        q ▷ vG = (previous.gComposite ≫ q) ▷ vG
      rw [ih]
      exact (Bicategory.comp_whiskerRight _ _ vG).symm

/-- Left whiskering preserves actual F26 path concatenation,
including all intermediate dependent 1-cells. -/
theorem leftWhiskerChain_append
    {aF bF aG bG : C}
    {fF kF lF : aF ⟶ bF} {fG kG lG : aG ⟶ bG}
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    leftWhiskerChain uF uG (Chains.append head tail) =
      Chains.append (leftWhiskerChain uF uG head)
        (leftWhiskerChain uF uG tail) := by
  induction tail with
  | nil => rfl
  | snoc previous p q ih =>
      change BiComparisonChain.snoc
        (leftWhiskerChain uF uG (Chains.append head previous))
        (Bicategory.whiskerLeftIso uF p) (uG ◁ q) =
        BiComparisonChain.snoc
          (Chains.append (leftWhiskerChain uF uG head)
            (leftWhiskerChain uF uG previous))
          (Bicategory.whiskerLeftIso uF p) (uG ◁ q)
      rw [ih]

/-- Right whiskering likewise preserves native F26 concatenation. -/
theorem rightWhiskerChain_append
    {aF bF aG bG : C}
    {fF kF lF : aF ⟶ bF} {fG kG lG : aG ⟶ bG}
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    rightWhiskerChain vF vG (Chains.append head tail) =
      Chains.append (rightWhiskerChain vF vG head)
        (rightWhiskerChain vF vG tail) := by
  induction tail with
  | nil => rfl
  | snoc previous p q ih =>
      change BiComparisonChain.snoc
        (rightWhiskerChain vF vG (Chains.append head previous))
        (Bicategory.whiskerRightIso p vF) (q ▷ vG) =
        BiComparisonChain.snoc
          (Chains.append (rightWhiskerChain vF vG head)
            (rightWhiskerChain vF vG previous))
          (Bicategory.whiskerRightIso p vF) (q ▷ vG)
      rw [ih]

/-- Actual original finite-chain category LEFT whiskering functor. -/
def leftPathWhiskerFunctor (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG) :
    ComparisonPair aF bF aG bG ⥤ ComparisonPair eF bF eG bG where
  obj x := ⟨uF ≫ x.fF, uG ≫ x.fG⟩
  map {_ _} c := leftWhiskerChain uF uG c
  map_id _ := rfl
  map_comp c d := leftWhiskerChain_append uF uG c d

/-- Actual original finite-chain category RIGHT whiskering functor. -/
def rightPathWhiskerFunctor (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG) :
    ComparisonPair aF bF aG bG ⥤ ComparisonPair aF eF aG eG where
  obj x := ⟨x.fF ≫ vF, x.fG ≫ vG⟩
  map {_ _} c := rightWhiskerChain vF vG c
  map_id _ := rfl
  map_comp c d := rightWhiskerChain_append vF vG c d

#print axioms leftWhiskerChain
#print axioms rightWhiskerChain
#print axioms leftWhiskerChain_fComposite
#print axioms leftWhiskerChain_gComposite
#print axioms rightWhiskerChain_fComposite
#print axioms rightWhiskerChain_gComposite
#print axioms leftWhiskerChain_append
#print axioms rightWhiskerChain_append
#print axioms leftPathWhiskerFunctor
#print axioms rightPathWhiskerFunctor

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalChainFunctorsV5_127
