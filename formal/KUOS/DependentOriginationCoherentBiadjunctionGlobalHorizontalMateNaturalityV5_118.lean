import KUOS.DependentOriginationCoherentBiadjunctionMateForgetfulHorizontalWhiskeringV5_117

namespace KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionMateForgetfulHorizontalWhiskeringV5_117.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F21: global whiskered right-mate modification naturality

The F20 pointwise horizontal exchange now extends to genuine global
lax modification naturality for every source 1-cell and for arbitrary
external left or right whiskers. The right mates are not strengthened.
A universal bicategorical comparison square below additionally preserves
arbitrary (possibly noninvertible) 2-cells in the original G map.
The original F/G, eta, epsilon, mapId/mapComp and adjunctions are fixed.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Global naturality of F17's original conjugated mate modification. -/
theorem globalConjugateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y) :
    (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷ F.map f ≫
        dσ.right.naturality f =
      dθ.right.naturality f ≫
        G.map f ◁
          (Bicategory.conjugateEquiv (dθ.adj Y) (dσ.adj Y) (Γ.app Y)) := by
  exact (rightModification dσ dθ Γ).naturality f

/-- Whiskering the entire original mate modification naturality
square on the LEFT retains the bicategorical associators. -/
theorem globalConjugateWhiskerLeftNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {e : C} (k : e ⟶ G.obj X) :
    k ◁ (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷ F.map f ≫
      k ◁ dσ.right.naturality f =
    k ◁ dθ.right.naturality f ≫
      k ◁ G.map f ◁
        (Bicategory.conjugateEquiv (dθ.adj Y) (dσ.adj Y) (Γ.app Y)) := by
  exact (rightModification dσ dθ Γ).whiskerLeft_naturality k f

/-- Right whiskering of the full arbitrary mate naturality square. -/
theorem globalConjugateWhiskerRightNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {e : C} (k : F.obj Y ⟶ e) :
    (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷ F.map f ▷ k ≫
        dσ.right.naturality f ▷ k =
      dθ.right.naturality f ▷ k ≫
        (G.map f ◁
          (Bicategory.conjugateEquiv (dθ.adj Y) (dσ.adj Y) (Γ.app Y))) ▷ k := by
  exact (rightModification dσ dθ Γ).whiskerRight_naturality f k

/-- An arbitrary 2-cell changing G.map(f) respects the FULL transported
modification. Uses native bicategorical interchange; no inverse of q. -/
theorem globalConjugateComparisonNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {k : G.obj X ⟶ G.obj Y} (q : G.map f ⟶ k) :
    ((Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷ F.map f ≫
        dσ.right.naturality f) ≫ q ▷ dσ.right.app Y =
      (dθ.right.naturality f ≫ q ▷ dθ.right.app Y) ≫
        k ◁ (Bicategory.conjugateEquiv (dθ.adj Y) (dσ.adj Y) (Γ.app Y)) := by
  let m := rightModification dσ dθ Γ
  change (m.app X ▷ F.map f ≫ dσ.right.naturality f) ≫
    q ▷ dσ.right.app Y =
    (dθ.right.naturality f ≫ q ▷ dθ.right.app Y) ≫ k ◁ m.app Y
  calc
    _ = (dθ.right.naturality f ≫ G.map f ◁ m.app Y) ≫
        q ▷ dσ.right.app Y := by
      exact congrArg (fun t => t ≫ q ▷ dσ.right.app Y) (m.naturality f)
    _ = dθ.right.naturality f ≫
        ((G.map f ◁ m.app Y) ≫ q ▷ dσ.right.app Y) := by
      rw [Category.assoc]
    _ = dθ.right.naturality f ≫
        (q ▷ dθ.right.app Y ≫ k ◁ m.app Y) := by
      exact congrArg (fun t => dθ.right.naturality f ≫ t)
        (Bicategory.whisker_exchange q (m.app Y))
    _ = _ := by rw [Category.assoc]

/-- Non-strict G.mapId is a particular arbitrary comparison 2-cell.
The original pseudofunctor identity correction is retained literally. -/
theorem globalConjugateMapIdNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) (X : B) :
    ((Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷
          F.map (𝟙 X) ≫ dσ.right.naturality (𝟙 X)) ≫
        (G.toOplax.mapId X) ▷ dσ.right.app X =
      (dθ.right.naturality (𝟙 X) ≫
          (G.toOplax.mapId X) ▷ dθ.right.app X) ≫
        (𝟙 (G.obj X)) ◁
          (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) := by
  exact globalConjugateComparisonNaturality dσ dθ Γ (𝟙 X)
    (G.toOplax.mapId X)

/-- Non-strict G.mapComp remains in the GLOBAL composition-corrected
right-mate modification square, without replacing it by the identity. -/
theorem globalConjugateMapCompNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷
          F.map (f ≫ g) ≫ dσ.right.naturality (f ≫ g)) ≫
        (G.toOplax.mapComp f g) ▷ dσ.right.app Z =
      (dθ.right.naturality (f ≫ g) ≫
          (G.toOplax.mapComp f g) ▷ dθ.right.app Z) ≫
        (G.map f ≫ G.map g) ◁
          (Bicategory.conjugateEquiv (dθ.adj Z) (dσ.adj Z) (Γ.app Z)) := by
  exact globalConjugateComparisonNaturality dσ dθ Γ (f ≫ g)
    (G.toOplax.mapComp f g)

/-- DUAL comparison: a fixed INVERTIBLE 2-cell on the original F-map
may be moved across the right-mate square. Its inverse is used only
because this case changes the domain of the lax naturality square. -/
theorem globalConjugateDomainComparisonNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {k : F.obj X ⟶ F.obj Y} (p : F.map f ≅ k) :
    (((Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷ k) ≫
        dσ.right.app X ◁ p.inv) ≫ dσ.right.naturality f =
      (dθ.right.app X ◁ p.inv) ≫
        (dθ.right.naturality f ≫
          G.map f ◁
            (Bicategory.conjugateEquiv (dθ.adj Y) (dσ.adj Y) (Γ.app Y))) := by
  let m := rightModification dσ dθ Γ
  change ((m.app X ▷ k) ≫ dσ.right.app X ◁ p.inv) ≫ dσ.right.naturality f =
    (dθ.right.app X ◁ p.inv) ≫
      (dθ.right.naturality f ≫ G.map f ◁ m.app Y)
  calc
    _ = ((dθ.right.app X ◁ p.inv) ≫ (m.app X ▷ F.map f)) ≫
        dσ.right.naturality f := by
      exact congrArg (fun t => t ≫ dσ.right.naturality f)
        (Bicategory.whisker_exchange (m.app X) p.inv).symm
    _ = (dθ.right.app X ◁ p.inv) ≫
        ((m.app X ▷ F.map f) ≫ dσ.right.naturality f) := by
      rw [Category.assoc]
    _ = (dθ.right.app X ◁ p.inv) ≫
        (dθ.right.naturality f ≫ G.map f ◁ m.app Y) := by
      exact congrArg (fun t => (dθ.right.app X ◁ p.inv) ≫ t)
        (m.naturality f)

/-- Identity comparison on the original F-side, using the original
non-strict PSEUDOFUNCTOR mapId isomorphism. -/
theorem globalConjugateDomainMapIdNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) (X : B) :
    (((Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷
          (𝟙 (F.obj X))) ≫
        dσ.right.app X ◁ (F.mapId X).inv) ≫
          dσ.right.naturality (𝟙 X) =
      (dθ.right.app X ◁ (F.mapId X).inv) ≫
        (dθ.right.naturality (𝟙 X) ≫
          G.map (𝟙 X) ◁
            (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X))) := by
  exact globalConjugateDomainComparisonNaturality dσ dθ Γ (𝟙 X) (F.mapId X)

/-- Composition comparison on the original F-side, retaining the
true non-strict F.mapComp ISO and its prescribed inverse orientation. -/
theorem globalConjugateDomainMapCompNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (((Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷
          (F.map f ≫ F.map g)) ≫
        dσ.right.app X ◁ (F.mapComp f g).inv) ≫
          dσ.right.naturality (f ≫ g) =
      (dθ.right.app X ◁ (F.mapComp f g).inv) ≫
        (dθ.right.naturality (f ≫ g) ≫
          G.map (f ≫ g) ◁
            (Bicategory.conjugateEquiv (dθ.adj Z) (dσ.adj Z) (Γ.app Z))) := by
  exact globalConjugateDomainComparisonNaturality dσ dθ Γ (f ≫ g)
    (F.mapComp f g)

#print axioms globalConjugateNaturality
#print axioms globalConjugateWhiskerLeftNaturality
#print axioms globalConjugateWhiskerRightNaturality
#print axioms globalConjugateComparisonNaturality
#print axioms globalConjugateMapIdNaturality
#print axioms globalConjugateMapCompNaturality
#print axioms globalConjugateDomainComparisonNaturality
#print axioms globalConjugateDomainMapIdNaturality
#print axioms globalConjugateDomainMapCompNaturality

end Generic

end

/-! ## Genuine original source η and target ε specializations -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- SOURCE: original R_L.mapId is explicitly present in the naturality
of EVERY modification on the original source-unit η. No strictification. -/
theorem actualLiftSourceGlobalMapIdNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    let D := actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let m := rightModification D D Γ
    ((m.app X ▷ (𝟙 X) ≫ D.right.naturality (𝟙 X)) ≫
        (R.mapId X).hom ▷ D.right.app X) =
      (D.right.naturality (𝟙 X) ≫ (R.mapId X).hom ▷ D.right.app X) ≫
        (𝟙 X) ◁ m.app X := by
  exact Generic.globalConjugateMapIdNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- SOURCE: retain the ORIGINAL R_L.mapComp after the full mate
naturality square on each arbitrary composite source 1-morphism. -/
theorem actualLiftSourceGlobalMapCompNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    let D := actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let m := rightModification D D Γ
    ((m.app X ▷ (f ≫ g) ≫ D.right.naturality (f ≫ g)) ≫
        (R.mapComp f g).hom ▷ D.right.app Z) =
      (D.right.naturality (f ≫ g) ≫
        (R.mapComp f g).hom ▷ D.right.app Z) ≫
          (R.map f ≫ R.map g) ◁ m.app Z := by
  exact Generic.globalConjugateMapCompNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

/-- TARGET: the ORIGINAL non-strict R_E.mapId inverse is kept on the
source side of the original target-counit's right-mate square. -/
theorem actualLiftTargetGlobalMapIdNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    let D := actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let m := rightModification D D Γ
    ((m.app X ▷ (𝟙 X) ≫ D.right.app X ◁ (R.mapId X).inv) ≫
        D.right.naturality (𝟙 X)) =
      (D.right.app X ◁ (R.mapId X).inv) ≫
        (D.right.naturality (𝟙 X) ≫ (𝟙 X) ◁ m.app X) := by
  exact Generic.globalConjugateDomainMapIdNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- TARGET: the ORIGINAL R_E.mapComp inverse is kept on the source
side, dual to the source-unit R_L.mapComp correction. -/
theorem actualLiftTargetGlobalMapCompNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    let D := actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let m := rightModification D D Γ
    ((m.app X ▷ (R.map f ≫ R.map g) ≫
        D.right.app X ◁ (R.mapComp f g).inv) ≫
          D.right.naturality (f ≫ g)) =
      (D.right.app X ◁ (R.mapComp f g).inv) ≫
        (D.right.naturality (f ≫ g) ≫
          (f ≫ g) ◁ m.app Z) := by
  exact Generic.globalConjugateDomainMapCompNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

#print axioms actualLiftSourceGlobalMapIdNaturality
#print axioms actualLiftSourceGlobalMapCompNaturality
#print axioms actualLiftTargetGlobalMapIdNaturality
#print axioms actualLiftTargetGlobalMapCompNaturality

end KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118
