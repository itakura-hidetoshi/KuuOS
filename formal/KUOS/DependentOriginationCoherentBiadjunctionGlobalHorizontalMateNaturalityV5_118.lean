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
      rw [Bicategory.whisker_exchange q (m.app Y)]
    _ = _ := by rw [Category.assoc]

#print axioms globalConjugateNaturality
#print axioms globalConjugateWhiskerLeftNaturality
#print axioms globalConjugateWhiskerRightNaturality
#print axioms globalConjugateComparisonNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionGlobalHorizontalMateNaturalityV5_118
