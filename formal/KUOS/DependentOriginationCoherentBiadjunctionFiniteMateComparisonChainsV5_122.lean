import KUOS.DependentOriginationCoherentBiadjunctionMateComparisonFactorizationIndependenceV5_121

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionBiComparisonMateNaturalityV5_119.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F25 / v5.122: arbitrary finite nonstrict comparison chains

F22--F24 establish comparison naturality and factorization independence
for a fixed two-stage pasting. Now each comparison is an actual
recursively constructed FINITE CHAIN in the native hom categories:
  * every F-side step is a genuine isomorphism,
  * every G-side step is an arbitrary 2-cell (NOT required invertible),
  * endpoints and every intermediate 1-cell remain explicitly typed.

The folded LEFT correction uses reversed F inverses; the folded RIGHT
correction retains forward G order. Both folds are proved equal to
whiskering the genuine composite cells by induction, for any finite
depth, and the original F22 right-mate square gives global naturality
and comparison-factorization independence for arbitrary such chains.

No strictification, reselected adjunction, new axioms, or upgrade of
right mates from LAX to strong. True F/G mapId/mapComp comparisons
can be prepended to ANY finite continuation.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- A genuinely dependent finite list of paired comparison 2-cells.
Each successive F comparison is invertible; each G comparison may
be noninvertible. The indexes remember every intermediate 1-cell. -/
inductive BiComparisonChain
    {aF bF aG bG : C}
    (fF : aF ⟶ bF) (fG : aG ⟶ bG) :
    (kF : aF ⟶ bF) → (kG : aG ⟶ bG) → Type (max vC wC) where
  | nil : BiComparisonChain fF fG fF fG
  | snoc {kF kG lF lG}
      (previous : BiComparisonChain fF fG kF kG)
      (t : kF ≅ lF) (r : kG ⟶ lG) :
      BiComparisonChain fF fG lF lG

namespace BiComparisonChain

variable {aF bF aG bG : C}
variable {fF : aF ⟶ bF} {fG : aG ⟶ bG}

/-- Genuine length, including zero and all positive finite depths. -/
def depth {kF : aF ⟶ bF} {kG : aG ⟶ bG}
    : BiComparisonChain fF fG kF kG → ℕ
  | .nil => 0
  | .snoc previous _ _ => depth previous + 1

/-- F-side composite ISO, in forward order. -/
def fComposite {kF : aF ⟶ bF} {kG : aG ⟶ bG} :
    BiComparisonChain fF fG kF kG → (fF ≅ kF)
  | .nil => Iso.refl fF
  | .snoc previous t _ => (fComposite previous).trans t

/-- G-side composite 2-cell, in forward order with no inverses. -/
def gComposite {kF : aF ⟶ bF} {kG : aG ⟶ bG} :
    BiComparisonChain fF fG kF kG → (fG ⟶ kG)
  | .nil => 𝟙 fG
  | .snoc previous _ r => gComposite previous ≫ r

/-- Actual expanded F correction: each new F inverse is whiskered
on the left of the entire previous correction. -/
def leftCorrection {a : C} (d : a ⟶ aF)
    {kF : aF ⟶ bF} {kG : aG ⟶ bG} :
    (c : BiComparisonChain fF fG kF kG) →
      ((d ≫ kF) ⟶ (d ≫ fF))
  | .nil => 𝟙 (d ≫ fF)
  | .snoc previous t _ => (d ◁ t.inv) ≫ leftCorrection d previous

/-- Actual expanded G correction: each new arbitrary G 2-cell is
whiskered on the RIGHT after the entire previous correction. -/
def rightCorrection {e : C} (h : bG ⟶ e)
    {kF : aF ⟶ bF} {kG : aG ⟶ bG} :
    (c : BiComparisonChain fF fG kF kG) →
      ((fG ≫ h) ⟶ (kG ≫ h))
  | .nil => 𝟙 (fG ≫ h)
  | .snoc previous _ r => rightCorrection h previous ≫ r ▷ h

/-- Induction over arbitrary finite depth: the entire expanded
F-domain correction is the left whisker of the inverse composite ISO. -/
theorem leftCorrection_eq_whisker {a : C} (d : a ⟶ aF)
    {kF : aF ⟶ bF} {kG : aG ⟶ bG}
    (c : BiComparisonChain fF fG kF kG) :
    leftCorrection d c = d ◁ (fComposite c).inv := by
  induction c with
  | nil =>
      change (𝟙 (d ≫ fF)) = d ◁ (Iso.refl fF).inv
      simp only [Iso.refl_inv, Bicategory.whiskerLeft_id]
  | snoc previous t r ih =>
      change (d ◁ t.inv) ≫ leftCorrection d previous =
        d ◁ ((fComposite previous).trans t).inv
      calc
        _ = (d ◁ t.inv) ≫ (d ◁ (fComposite previous).inv) := by rw [ih]
        _ = d ◁ (t.inv ≫ (fComposite previous).inv) :=
          (Bicategory.whiskerLeft_comp d t.inv (fComposite previous).inv).symm
        _ = _ := by rw [Iso.trans_inv]

/-- Induction over arbitrary finite depth: the expanded G correction
is the RIGHT whisker of the original composite, no inverse needed. -/
theorem rightCorrection_eq_whisker {e : C} (h : bG ⟶ e)
    {kF : aF ⟶ bF} {kG : aG ⟶ bG}
    (c : BiComparisonChain fF fG kF kG) :
    rightCorrection h c = (gComposite c) ▷ h := by
  induction c with
  | nil =>
      change (𝟙 (fG ≫ h)) = (𝟙 fG) ▷ h
      simp only [Bicategory.id_whiskerRight]
  | snoc previous t r ih =>
      change rightCorrection h previous ≫ r ▷ h =
        (gComposite previous ≫ r) ▷ h
      calc
        _ = (gComposite previous ▷ h) ≫ r ▷ h := by rw [ih]
        _ = _ := (Bicategory.comp_whiskerRight (gComposite previous) r h).symm

/-- Prepend a genuinely original comparison, preserving ALL later
intermediate 1-cells rather than collapsing the continuation. -/
def prepend
    {mF lF : aF ⟶ bF} {mG lG : aG ⟶ bG}
    (p : fF ≅ mF) (q : fG ⟶ mG)
    (c : BiComparisonChain mF mG lF lG) :
    BiComparisonChain fF fG lF lG :=
  match c with
  | .nil => .snoc .nil p q
  | .snoc previous t r => .snoc (prepend p q previous) t r

#print axioms depth
#print axioms fComposite
#print axioms gComposite
#print axioms leftCorrection
#print axioms rightCorrection
#print axioms leftCorrection_eq_whisker
#print axioms rightCorrection_eq_whisker
#print axioms prepend

end BiComparisonChain

variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Actual left boundary of every native finite chain, with every
F inverse and G comparison retained in the recursive correction. -/
def finiteLeftBoundary
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :=
  let m := rightModification dσ dθ Γ
  ((m.app X ▷ kF ≫ c.leftCorrection (dσ.right.app X)) ≫
    dσ.right.naturality f) ≫ c.rightCorrection (dσ.right.app Y)

/-- Actual opposite/right boundary, including the unchanged outer
whiskering by the full original F17 right-mate modification. -/
def finiteRightBoundary
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :=
  let m := rightModification dσ dθ Γ
  ((c.leftCorrection (dθ.right.app X) ≫
      dθ.right.naturality f) ≫
    c.rightCorrection (dθ.right.app Y)) ≫ kG ◁ m.app Y

/-- The expanded left boundary normalizes to the SAME original F22
comparison on the genuinely composed F ISO and G 2-cell. -/
theorem finiteLeftBoundary_normalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    finiteLeftBoundary dσ dθ Γ f c =
      (((rightModification dσ dθ Γ).app X ▷ kF ≫
          dσ.right.app X ◁ (c.fComposite).inv) ≫
        dσ.right.naturality f) ≫
          c.gComposite ▷ dσ.right.app Y := by
  simp only [finiteLeftBoundary, BiComparisonChain.leftCorrection_eq_whisker,
    BiComparisonChain.rightCorrection_eq_whisker]
  rfl

/-- The expanded right boundary normalizes independently, retaining
the final genuine G-side whiskering rather than strictifying it. -/
theorem finiteRightBoundary_normalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    finiteRightBoundary dσ dθ Γ f c =
      (((dθ.right.app X ◁ (c.fComposite).inv ≫
          dθ.right.naturality f) ≫
        c.gComposite ▷ dθ.right.app Y) ≫
          kG ◁ (rightModification dσ dθ Γ).app Y) := by
  simp only [finiteRightBoundary, BiComparisonChain.leftCorrection_eq_whisker,
    BiComparisonChain.rightCorrection_eq_whisker]
  rfl

/-- Original F22 simultaneous comparison naturality now holds for
the genuinely EXPANDED boundaries of EVERY finite comparison chain. -/
theorem finiteBiComparisonNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    finiteLeftBoundary dσ dθ Γ f c =
      finiteRightBoundary dσ dθ Γ f c := by
  unfold finiteLeftBoundary finiteRightBoundary
  simpa only [BiComparisonChain.leftCorrection_eq_whisker,
    BiComparisonChain.rightCorrection_eq_whisker] using
    (globalConjugateBiComparisonNaturality dσ dθ Γ f c.fComposite c.gComposite)

/-- Any TWO finite subdivision paths with the same original 1-cell
endpoints and identical composite comparisons have identical
expanded LEFT and RIGHT boundaries, at arbitrary and unequal depths. -/
theorem finiteBiComparisonFactorizationIndependent
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c₁ c₂ : BiComparisonChain (F.map f) (G.map f) kF kG)
    (hp : c₁.fComposite = c₂.fComposite)
    (hq : c₁.gComposite = c₂.gComposite) :
    finiteLeftBoundary dσ dθ Γ f c₁ =
      finiteLeftBoundary dσ dθ Γ f c₂ ∧
    finiteRightBoundary dσ dθ Γ f c₁ =
      finiteRightBoundary dσ dθ Γ f c₂ := by
  constructor
  · simp only [finiteLeftBoundary_normalize, hp, hq]
  · simp only [finiteRightBoundary_normalize, hp, hq]

/-- REAL original F.mapId/G.mapId cells can be prepended to ANY finite
tail, keeping their authentic orientations and all intermediate cells. -/
def originalMapIdFiniteChain (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (tail : BiComparisonChain (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :
    BiComparisonChain (F.map (𝟙 X)) (G.map (𝟙 X)) kF kG :=
  BiComparisonChain.prepend (F.mapId X) (G.toOplax.mapId X) tail

/-- REAL original F.mapComp/G.mapComp cells can likewise be prepended
to an arbitrary finite tail without imposing G invertibility. -/
def originalMapCompFiniteChain {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (tail : BiComparisonChain
      (F.map f ≫ F.map g) (G.map f ≫ G.map g) kF kG) :
    BiComparisonChain (F.map (f ≫ g)) (G.map (f ≫ g)) kF kG :=
  BiComparisonChain.prepend (F.mapComp f g) (G.toOplax.mapComp f g) tail

/-- Original mapId followed by arbitrarily many F/G comparisons. -/
def finiteOriginalMapIdNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (tail : BiComparisonChain (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :=
  finiteBiComparisonNaturality dσ dθ Γ (𝟙 X)
    (originalMapIdFiniteChain (F := F) (G := G) X tail)

/-- Original mapComp followed by arbitrarily many F/G comparisons. -/
def finiteOriginalMapCompNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (tail : BiComparisonChain
      (F.map f ≫ F.map g) (G.map f ≫ G.map g) kF kG) :=
  finiteBiComparisonNaturality dσ dθ Γ (f ≫ g)
    (originalMapCompFiniteChain (F := F) (G := G) f g tail)

#print axioms finiteLeftBoundary
#print axioms finiteRightBoundary
#print axioms finiteLeftBoundary_normalize
#print axioms finiteRightBoundary_normalize
#print axioms finiteBiComparisonNaturality
#print axioms finiteBiComparisonFactorizationIndependent
#print axioms originalMapIdFiniteChain
#print axioms originalMapCompFiniteChain
#print axioms finiteOriginalMapIdNaturality
#print axioms finiteOriginalMapCompNaturality

end Generic

end KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122
