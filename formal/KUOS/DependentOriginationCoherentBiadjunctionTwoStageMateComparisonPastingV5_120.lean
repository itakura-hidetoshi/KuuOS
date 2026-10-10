import KUOS.DependentOriginationCoherentBiadjunctionBiComparisonMateNaturalityV5_119

namespace KUOS.DependentOriginationCoherentBiadjunctionTwoStageMateComparisonPastingV5_120

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
# F23 / v5.120: two-stage horizontal mate-comparison pasting

F22 proved the simultaneous F-domain ISO and arbitrary G-codomain
comparison naturality for genuine lax right mates. Here each comparison
is allowed an additional, INDEPENDENT second stage. The expanded
pasting equation below is proved with both mathlib whisker-exchange
laws and the genuine F22 simultaneous square. The intermediate 1-cells
are retained, with no strictification or invertibility imposed on the
two G-side 2-cells.

We also recover the composite (single-step) statement and specialize
the true original mapId/mapComp cells for F14 source eta and target
epsilon, without reselecting adjunctions or changing the right laxity.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Two-stage pasting of an invertible F-domain comparison and an
arbitrary (possibly NONINVERTIBLE) G-codomain comparison is globally
natural for the same original right-mate modification. This equality
retains EACH intermediate whiskering and its original orientation. -/
theorem globalConjugateBiComparisonTwoStageNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    (p : F.map f ≅ kF) (t : kF ≅ lF)
    {kG lG : G.obj X ⟶ G.obj Y}
    (q : G.map f ⟶ kG) (r : kG ⟶ lG) :
    let m := rightModification dσ dθ Γ
    (((((m.app X ▷ lF ≫ dσ.right.app X ◁ t.inv) ≫
          dσ.right.app X ◁ p.inv) ≫ dσ.right.naturality f) ≫
        q ▷ dσ.right.app Y) ≫ r ▷ dσ.right.app Y) =
      (((((dθ.right.app X ◁ t.inv ≫ dθ.right.app X ◁ p.inv) ≫
          dθ.right.naturality f) ≫ q ▷ dθ.right.app Y) ≫
        r ▷ dθ.right.app Y) ≫ lG ◁ m.app Y) := by
  let m := rightModification dσ dθ Γ
  change
    (((((m.app X ▷ lF ≫ dσ.right.app X ◁ t.inv) ≫
          dσ.right.app X ◁ p.inv) ≫ dσ.right.naturality f) ≫
        q ▷ dσ.right.app Y) ≫ r ▷ dσ.right.app Y) =
      (((((dθ.right.app X ◁ t.inv ≫ dθ.right.app X ◁ p.inv) ≫
          dθ.right.naturality f) ≫ q ▷ dθ.right.app Y) ≫
        r ▷ dθ.right.app Y) ≫ lG ◁ m.app Y)
  calc
    _ = (((((dθ.right.app X ◁ t.inv ≫ m.app X ▷ kF) ≫
              dσ.right.app X ◁ p.inv) ≫ dσ.right.naturality f) ≫
            q ▷ dσ.right.app Y) ≫ r ▷ dσ.right.app Y) := by
      rw [(Bicategory.whisker_exchange (m.app X) t.inv).symm]
    _ = (dθ.right.app X ◁ t.inv) ≫
          (((((m.app X ▷ kF ≫ dσ.right.app X ◁ p.inv) ≫
              dσ.right.naturality f) ≫ q ▷ dσ.right.app Y) ≫
            r ▷ dσ.right.app Y)) := by
      simp only [Category.assoc]
    _ = (dθ.right.app X ◁ t.inv) ≫
          (((((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
              q ▷ dθ.right.app Y) ≫ kG ◁ m.app Y) ≫
            r ▷ dσ.right.app Y)) := by
      exact congrArg (fun z =>
        (dθ.right.app X ◁ t.inv) ≫ (z ≫ r ▷ dσ.right.app Y))
        (globalConjugateBiComparisonNaturality dσ dθ Γ f p q)
    _ = (dθ.right.app X ◁ t.inv) ≫
          (((((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
              q ▷ dθ.right.app Y) ≫ r ▷ dθ.right.app Y) ≫
            lG ◁ m.app Y)) := by
      apply congrArg (fun z => (dθ.right.app X ◁ t.inv) ≫ z)
      calc
        _ = ((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
              q ▷ dθ.right.app Y) ≫
              (kG ◁ m.app Y ≫ r ▷ dσ.right.app Y) := by
          simp only [Category.assoc]
        _ = ((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
              q ▷ dθ.right.app Y) ≫
              (r ▷ dθ.right.app Y ≫ lG ◁ m.app Y) := by
          exact congrArg (fun z =>
            ((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
              q ▷ dθ.right.app Y) ≫ z)
            (Bicategory.whisker_exchange r (m.app Y))
        _ = _ := by simp only [Category.assoc]
    _ = _ := by simp only [Category.assoc]

/-- The same two comparisons can be composed into a single F ISO
and G 2-cell. This is the exact F22 square on the composed cells, so
the effective pasting makes no G comparison invertible. -/
theorem globalConjugateBiComparisonCompositeNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    (p : F.map f ≅ kF) (t : kF ≅ lF)
    {kG lG : G.obj X ⟶ G.obj Y}
    (q : G.map f ⟶ kG) (r : kG ⟶ lG) :
    let m := rightModification dσ dθ Γ
    (((m.app X ▷ lF ≫ dσ.right.app X ◁ (p.trans t).inv) ≫
        dσ.right.naturality f) ≫
      (q ≫ r) ▷ dσ.right.app Y) =
      (((dθ.right.app X ◁ (p.trans t).inv ≫
          dθ.right.naturality f) ≫
        (q ≫ r) ▷ dθ.right.app Y) ≫ lG ◁ m.app Y) := by
  exact globalConjugateBiComparisonNaturality dσ dθ Γ f (p.trans t) (q ≫ r)

/-- Two genuine mapId comparison cells followed by independent new
source ISO and target (not necessarily invertible) corrections. -/
def globalConjugateBiMapIdTwoStageNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {lF : F.obj X ⟶ F.obj X} (t : 𝟙 (F.obj X) ≅ lF)
    {lG : G.obj X ⟶ G.obj X} (r : 𝟙 (G.obj X) ⟶ lG) :=
  globalConjugateBiComparisonTwoStageNaturality dσ dθ Γ
    (𝟙 X) (F.mapId X) t (G.toOplax.mapId X) r

/-- F and G original non-strict mapComp corrections each followed by
one additional independent comparison; right mates stay lax. -/
def globalConjugateBiMapCompTwoStageNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {lF : F.obj X ⟶ F.obj Z}
    (t : (F.map f ≫ F.map g) ≅ lF)
    {lG : G.obj X ⟶ G.obj Z}
    (r : (G.map f ≫ G.map g) ⟶ lG) :=
  globalConjugateBiComparisonTwoStageNaturality dσ dθ Γ
    (f ≫ g) (F.mapComp f g) t (G.toOplax.mapComp f g) r

#print axioms globalConjugateBiComparisonTwoStageNaturality
#print axioms globalConjugateBiComparisonCompositeNaturality
#print axioms globalConjugateBiMapIdTwoStageNaturality
#print axioms globalConjugateBiMapCompTwoStageNaturality

end Generic

end

/-! ## Original source η and target ε: unchanged selected adjunctions.

Partial application exposes the full dependent family of arbitrary
second-stage comparison cells while avoiding WHNF expansion of the
refinement-indexed equality in a handwritten declaration header.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Original SOURCE eta: mapId followed by both arbitrary extra cells. -/
def actualLiftSourceBiMapIdTwoStageNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  Generic.globalConjugateBiMapIdTwoStageNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- Original SOURCE eta: mapComp followed by both arbitrary extra cells. -/
def actualLiftSourceBiMapCompTwoStageNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  Generic.globalConjugateBiMapCompTwoStageNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

/-- Original TARGET epsilon: mapId with arbitrary F/G second stages. -/
def actualLiftTargetBiMapIdTwoStageNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  Generic.globalConjugateBiMapIdTwoStageNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- Original TARGET epsilon: mapComp with arbitrary F/G second stages. -/
def actualLiftTargetBiMapCompTwoStageNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  Generic.globalConjugateBiMapCompTwoStageNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

#print axioms actualLiftSourceBiMapIdTwoStageNaturality
#print axioms actualLiftSourceBiMapCompTwoStageNaturality
#print axioms actualLiftTargetBiMapIdTwoStageNaturality
#print axioms actualLiftTargetBiMapCompTwoStageNaturality

end KUOS.DependentOriginationCoherentBiadjunctionTwoStageMateComparisonPastingV5_120
