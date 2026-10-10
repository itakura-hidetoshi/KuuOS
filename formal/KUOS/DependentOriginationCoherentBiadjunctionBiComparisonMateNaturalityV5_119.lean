import KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118

namespace KUOS.DependentOriginationCoherentBiadjunctionBiComparisonMateNaturalityV5_119

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F22 / v5.119: simultaneous two-sided non-strict mate naturality

F21 treated the original F-domain isomorphism and G-codomain lax
comparison separately. Here both are pasted into ONE right-mate
modification square. The G comparison is an arbitrary 2-cell: it is
not assumed invertible, including when the original right mate is
only LAX. The F comparison uses its inverse only because the
pseudofunctor mapId/mapComp correction changes the source of the
naturality square.

The original source-unit eta / target-counit epsilon, original F/G,
chosen adjunctions, mapId/mapComp, and right-mate laxity are unchanged.
This is not a new biequivalence of B and C.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The SAME F17 right-mate modification is natural after BOTH an
invertible F-side domain correction and an arbitrary G-side codomain
correction. The comparison on G need not be invertible. -/
theorem globalConjugateBiComparisonNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} (p : F.map f ≅ kF)
    {kG : G.obj X ⟶ G.obj Y} (q : G.map f ⟶ kG) :
    let m := rightModification dσ dθ Γ
    (((m.app X ▷ kF ≫ dσ.right.app X ◁ p.inv) ≫
        dσ.right.naturality f) ≫ q ▷ dσ.right.app Y) =
      (((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
          q ▷ dθ.right.app Y) ≫ kG ◁ m.app Y) := by
  let m := rightModification dσ dθ Γ
  change
    (((m.app X ▷ kF ≫ dσ.right.app X ◁ p.inv) ≫
        dσ.right.naturality f) ≫ q ▷ dσ.right.app Y) =
      (((dθ.right.app X ◁ p.inv ≫ dθ.right.naturality f) ≫
          q ▷ dθ.right.app Y) ≫ kG ◁ m.app Y)
  calc
    _ = ((dθ.right.app X ◁ p.inv) ≫
          (dθ.right.naturality f ≫ G.map f ◁ m.app Y)) ≫
          q ▷ dσ.right.app Y := by
      exact congrArg (fun t => t ≫ q ▷ dσ.right.app Y)
        (globalConjugateDomainComparisonNaturality dσ dθ Γ f p)
    _ = (dθ.right.app X ◁ p.inv) ≫
          (dθ.right.naturality f ≫
            ((G.map f ◁ m.app Y) ≫ q ▷ dσ.right.app Y)) := by
      simp only [Category.assoc]
    _ = (dθ.right.app X ◁ p.inv) ≫
          (dθ.right.naturality f ≫
            (q ▷ dθ.right.app Y ≫ kG ◁ m.app Y)) := by
      exact congrArg (fun t =>
        (dθ.right.app X ◁ p.inv) ≫ (dθ.right.naturality f ≫ t))
        (Bicategory.whisker_exchange q (m.app Y))
    _ = _ := by
      simp only [Category.assoc]

/-- The original non-strict F.mapId ISO and the original G.mapId LAX
correction appear simultaneously in the same global mate square. -/
theorem globalConjugateBiMapIdNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B) :
    let m := rightModification dσ dθ Γ
    (((m.app X ▷ (𝟙 (F.obj X)) ≫
        dσ.right.app X ◁ (F.mapId X).inv) ≫
          dσ.right.naturality (𝟙 X)) ≫
        (G.toOplax.mapId X) ▷ dσ.right.app X) =
      (((dθ.right.app X ◁ (F.mapId X).inv ≫
          dθ.right.naturality (𝟙 X)) ≫
            (G.toOplax.mapId X) ▷ dθ.right.app X) ≫
        (𝟙 (G.obj X)) ◁ m.app X) := by
  exact globalConjugateBiComparisonNaturality dσ dθ Γ (𝟙 X)
    (F.mapId X) (G.toOplax.mapId X)

/-- The original F.mapComp ISO and G.mapComp comparison are pasted
at ONCE, with the genuine non-strict compositors and mate orientation. -/
theorem globalConjugateBiMapCompNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z) :
    let m := rightModification dσ dθ Γ
    (((m.app X ▷ (F.map f ≫ F.map g) ≫
        dσ.right.app X ◁ (F.mapComp f g).inv) ≫
          dσ.right.naturality (f ≫ g)) ≫
        (G.toOplax.mapComp f g) ▷ dσ.right.app Z) =
      (((dθ.right.app X ◁ (F.mapComp f g).inv ≫
          dθ.right.naturality (f ≫ g)) ≫
            (G.toOplax.mapComp f g) ▷ dθ.right.app Z) ≫
        (G.map f ≫ G.map g) ◁ m.app Z) := by
  exact globalConjugateBiComparisonNaturality dσ dθ Γ (f ≫ g)
    (F.mapComp f g) (G.toOplax.mapComp f g)

#print axioms globalConjugateBiComparisonNaturality
#print axioms globalConjugateBiMapIdNaturality
#print axioms globalConjugateBiMapCompNaturality

end Generic

end

/-! ## Genuine original source eta and target epsilon specializations

The result types of these four proof constants are inferred from
the generic theorems to avoid expensive WHNF expansion of the exact
refinement-indexed dependent equalities already checked in F21. -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- SOURCE eta, including BOTH the original source roundtrip mapId
and the identity pseudofunctor's genuine source comparison. -/
def actualLiftSourceBiMapIdNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  Generic.globalConjugateBiMapIdNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- SOURCE eta, with both original mapComp comparison cells. -/
def actualLiftSourceBiMapCompNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  Generic.globalConjugateBiMapCompNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

/-- TARGET epsilon, including the original target roundtrip mapId ISO
and the unchanged identity-side lax mapId correction. -/
def actualLiftTargetBiMapIdNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  Generic.globalConjugateBiMapIdNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- TARGET epsilon, with both original mapComp comparison cells. -/
def actualLiftTargetBiMapCompNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  Generic.globalConjugateBiMapCompNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

#print axioms actualLiftSourceBiMapIdNaturality
#print axioms actualLiftSourceBiMapCompNaturality
#print axioms actualLiftTargetBiMapIdNaturality
#print axioms actualLiftTargetBiMapCompNaturality

end KUOS.DependentOriginationCoherentBiadjunctionBiComparisonMateNaturalityV5_119
