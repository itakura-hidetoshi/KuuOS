import KUOS.DependentOriginationCoherentBiadjunctionTwoStageMateComparisonPastingV5_120

namespace KUOS.DependentOriginationCoherentBiadjunctionMateComparisonFactorizationIndependenceV5_121

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionTwoStageMateComparisonPastingV5_120.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F24 / v5.121: factorization-independent original mate comparison pasting

F23 provides expanded 2-stage comparison squares as well as the same
square with composite F/G comparison cells. Here we prove that the
LEFT and RIGHT boundaries of those two squares coincide as actual
2-morphisms, using the pinned mathlib whiskering composition laws.
Consequently TWO INDEPENDENT factorizations through possibly different
intermediate 1-cells have IDENTICAL pasted boundaries whenever their
composite F isomorphisms and G 2-cells agree.

The G-side comparisons are never required invertible. All original
F/G, source eta / target epsilon, chosen object adjunctions, and
nonstrict mapId/mapComp are retained, with LAX right mates.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The expanded F23 left boundary is exactly the F22 composite-cell
left boundary: the F correction composes in inverse order and the G
comparison composes in its original noninvertible direction. -/
theorem globalConjugateBiComparisonLeftPastingNormalize
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
      (((m.app X ▷ lF ≫ dσ.right.app X ◁ (p.trans t).inv) ≫
          dσ.right.naturality f) ≫
        (q ≫ r) ▷ dσ.right.app Y) := by
  have hWhisker :
      dσ.right.app X ◁ (t.inv ≫ p.inv) =
        (dσ.right.app X ◁ t.inv) ≫ (dσ.right.app X ◁ p.inv) :=
    Bicategory.whiskerLeft_comp (dσ.right.app X) t.inv p.inv
  simp only [Iso.trans_inv, Bicategory.comp_whiskerRight, Category.assoc]
  rw [hWhisker]

/-- The independent right boundary also normalizes to the composite
F ISO / G 2-cell. It includes the actual outer G-side whiskering by
the original right-mate modification. -/
theorem globalConjugateBiComparisonRightPastingNormalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    (p : F.map f ≅ kF) (t : kF ≅ lF)
    {kG lG : G.obj X ⟶ G.obj Y}
    (q : G.map f ⟶ kG) (r : kG ⟶ lG) :
    let m := rightModification dσ dθ Γ
    (((((dθ.right.app X ◁ t.inv ≫ dθ.right.app X ◁ p.inv) ≫
          dθ.right.naturality f) ≫
        q ▷ dθ.right.app Y) ≫ r ▷ dθ.right.app Y) ≫
          lG ◁ m.app Y) =
      (((dθ.right.app X ◁ (p.trans t).inv ≫
          dθ.right.naturality f) ≫
        (q ≫ r) ▷ dθ.right.app Y) ≫ lG ◁ m.app Y) := by
  have hWhisker :
      dθ.right.app X ◁ (t.inv ≫ p.inv) =
        (dθ.right.app X ◁ t.inv) ≫ (dθ.right.app X ◁ p.inv) :=
    Bicategory.whiskerLeft_comp (dθ.right.app X) t.inv p.inv
  simp only [Iso.trans_inv, Bicategory.comp_whiskerRight, Category.assoc]
  rw [hWhisker]

/-- Two completely DIFFERENT factorizations through independent F/G
intermediate 1-cells yield the SAME expanded left and right pastings
if their composite F isomorphisms and composite G 2-cells agree.
No inverse is assumed for any of q1,r1,q2,r2. -/
theorem globalConjugateBiComparisonFactorizationIndependent
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF1 kF2 lF : F.obj X ⟶ F.obj Y}
    (p1 : F.map f ≅ kF1) (t1 : kF1 ≅ lF)
    (p2 : F.map f ≅ kF2) (t2 : kF2 ≅ lF)
    {kG1 kG2 lG : G.obj X ⟶ G.obj Y}
    (q1 : G.map f ⟶ kG1) (r1 : kG1 ⟶ lG)
    (q2 : G.map f ⟶ kG2) (r2 : kG2 ⟶ lG)
    (hp : p1.trans t1 = p2.trans t2)
    (hq : q1 ≫ r1 = q2 ≫ r2) :
    let m := rightModification dσ dθ Γ
    (((((m.app X ▷ lF ≫ dσ.right.app X ◁ t1.inv) ≫
          dσ.right.app X ◁ p1.inv) ≫ dσ.right.naturality f) ≫
        q1 ▷ dσ.right.app Y) ≫ r1 ▷ dσ.right.app Y) =
      (((((m.app X ▷ lF ≫ dσ.right.app X ◁ t2.inv) ≫
          dσ.right.app X ◁ p2.inv) ≫ dσ.right.naturality f) ≫
        q2 ▷ dσ.right.app Y) ≫ r2 ▷ dσ.right.app Y)
    ∧
    (((((dθ.right.app X ◁ t1.inv ≫ dθ.right.app X ◁ p1.inv) ≫
          dθ.right.naturality f) ≫
        q1 ▷ dθ.right.app Y) ≫ r1 ▷ dθ.right.app Y) ≫
          lG ◁ m.app Y) =
      (((((dθ.right.app X ◁ t2.inv ≫ dθ.right.app X ◁ p2.inv) ≫
          dθ.right.naturality f) ≫
        q2 ▷ dθ.right.app Y) ≫ r2 ▷ dθ.right.app Y) ≫
          lG ◁ m.app Y) := by
  let m := rightModification dσ dθ Γ
  constructor
  · calc
      _ = (((m.app X ▷ lF ≫ dσ.right.app X ◁ (p1.trans t1).inv) ≫
            dσ.right.naturality f) ≫
            (q1 ≫ r1) ▷ dσ.right.app Y) :=
        globalConjugateBiComparisonLeftPastingNormalize dσ dθ Γ f p1 t1 q1 r1
      _ = (((m.app X ▷ lF ≫ dσ.right.app X ◁ (p2.trans t2).inv) ≫
            dσ.right.naturality f) ≫
            (q2 ≫ r2) ▷ dσ.right.app Y) := by rw [hp, hq]
      _ = _ :=
        (globalConjugateBiComparisonLeftPastingNormalize dσ dθ Γ f p2 t2 q2 r2).symm
  · calc
      _ = (((dθ.right.app X ◁ (p1.trans t1).inv ≫
            dθ.right.naturality f) ≫
            (q1 ≫ r1) ▷ dθ.right.app Y) ≫ lG ◁ m.app Y) :=
        globalConjugateBiComparisonRightPastingNormalize dσ dθ Γ f p1 t1 q1 r1
      _ = (((dθ.right.app X ◁ (p2.trans t2).inv ≫
            dθ.right.naturality f) ≫
            (q2 ≫ r2) ▷ dθ.right.app Y) ≫ lG ◁ m.app Y) := by rw [hp, hq]
      _ = _ :=
        (globalConjugateBiComparisonRightPastingNormalize dσ dθ Γ f p2 t2 q2 r2).symm

/-- True F.mapId and G.mapId followed by independent corrections
normalize to the single composite-cell F22 boundary. -/
def globalConjugateBiMapIdLeftPastingNormalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {lF : F.obj X ⟶ F.obj X} (t : 𝟙 (F.obj X) ≅ lF)
    {lG : G.obj X ⟶ G.obj X} (r : 𝟙 (G.obj X) ⟶ lG) :=
  globalConjugateBiComparisonLeftPastingNormalize dσ dθ Γ (𝟙 X)
    (F.mapId X) t (G.toOplax.mapId X) r

/-- True F.mapComp and G.mapComp followed by independent corrections
normalize with the original nonstrict composition cells retained. -/
def globalConjugateBiMapCompLeftPastingNormalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {lF : F.obj X ⟶ F.obj Z}
    (t : (F.map f ≫ F.map g) ≅ lF)
    {lG : G.obj X ⟶ G.obj Z}
    (r : (G.map f ≫ G.map g) ⟶ lG) :=
  globalConjugateBiComparisonLeftPastingNormalize dσ dθ Γ
    (f ≫ g) (F.mapComp f g) t (G.toOplax.mapComp f g) r

#print axioms globalConjugateBiComparisonLeftPastingNormalize
#print axioms globalConjugateBiComparisonRightPastingNormalize
#print axioms globalConjugateBiComparisonFactorizationIndependent
#print axioms globalConjugateBiMapIdLeftPastingNormalize
#print axioms globalConjugateBiMapCompLeftPastingNormalize

end Generic

end

/-! ## Original source unit η and target counit ε: original comparison cells. -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- F24: same original SOURCE η mapId cell;
the two-stage expanded left boundary equals its composite-cell normal form. -/
def actualLiftSourceBiMapIdPastingNormalize
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {lF : X ⟶ X} (t : 𝟙 X ≅ lF)
    {lG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X}
    (r : (𝟙 ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)) ⟶ lG) :=
  Generic.globalConjugateBiMapIdLeftPastingNormalize
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X t r


/-- F24: same original SOURCE η mapComp cell;
the two-stage expanded left boundary equals its composite-cell normal form. -/
def actualLiftSourceBiMapCompPastingNormalize
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    {lF : X ⟶ Z} (t : (f ≫ g) ≅ lF)
    {lG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z}
    (r : ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map g) ⟶ lG) :=
  Generic.globalConjugateBiMapCompLeftPastingNormalize
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g t r


/-- F24: same original TARGET ε mapId cell;
the two-stage expanded left boundary equals its composite-cell normal form. -/
def actualLiftTargetBiMapIdPastingNormalize
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {lF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X}
    (t : (𝟙 ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)) ≅ lF)
    {lG : X ⟶ X} (r : 𝟙 X ⟶ lG) :=
  Generic.globalConjugateBiMapIdLeftPastingNormalize
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X t r


/-- F24: same original TARGET ε mapComp cell;
the two-stage expanded left boundary equals its composite-cell normal form. -/
def actualLiftTargetBiMapCompPastingNormalize
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    {lF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z}
    (t : ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map g) ≅ lF)
    {lG : X ⟶ Z} (r : (f ≫ g) ⟶ lG) :=
  Generic.globalConjugateBiMapCompLeftPastingNormalize
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g t r


#print axioms actualLiftSourceBiMapIdPastingNormalize
#print axioms actualLiftSourceBiMapCompPastingNormalize
#print axioms actualLiftTargetBiMapIdPastingNormalize
#print axioms actualLiftTargetBiMapCompPastingNormalize

end KUOS.DependentOriginationCoherentBiadjunctionMateComparisonFactorizationIndependenceV5_121
