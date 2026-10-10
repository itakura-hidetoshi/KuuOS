import KUOS.DependentOriginationCoherentBiadjunctionMateForgetfulHorizontalWhiskeringV5_117

namespace KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionMateForgetfulHorizontalWhiskeringV5_117.Generic

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

end KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118
