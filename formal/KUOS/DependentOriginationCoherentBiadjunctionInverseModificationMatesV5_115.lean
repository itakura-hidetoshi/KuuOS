import KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114

namespace KUOS.DependentOriginationCoherentBiadjunctionInverseModificationMatesV5_115

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic

set_option autoImplicit false
noncomputable section

/-!
# F18 / v5.115: lossless inverse right-mate modification correspondence

F17 automatically turns any (not necessarily invertible) modification of
original strong transformations into a modification of their original
right-mate LAX transformations, reversing its direction.

This file proves the inverse without postulating right naturality:
  1. Unmate an arbitrary right-mate modification naturality square, using
     the exact non-strict mixed-adjunction mate laws of F17 and injectivity
     of the native mathlib mate equivalence.
  2. Construct the ORIGINAL left strong modification from the pointwise
     inverse of `Bicategory.conjugateEquiv`.
  3. Prove inverse-on-both-sides, producing an actual 2-Hom-type equivalence.
  4. Prove contravariant vertical composition also for the inverse.
  5. Specialize losslessly to the unchanged source η and target ε.

All constructions use the same F/G, η/ε, original selected adjunctions,
non-strict mapId/mapComp, both triangulators, and pinned mathlib.
No invertibility of naturality squares or arbitrary modifications is assumed.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d : B}
variable {l₁ l₂ : a ⟶ b} {r₁ r₂ : b ⟶ a}
variable {l₃ l₄ : c ⟶ d} {r₃ r₄ : d ⟶ c}
variable {g : a ⟶ c} {h : b ⟶ d}

/-- Converse of F17's general mate naturality square.
The right 2-cells need not be invertible. The original strong left
naturality equation is RECOVERED (not independently assumed). -/
theorem left_naturality_of_right_mate
    (adj₁ : Bicategory.Adjunction l₁ r₁)
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (adj₃ : Bicategory.Adjunction l₃ r₃)
    (adj₄ : Bicategory.Adjunction l₄ r₄)
    (tauX : r₂ ⟶ r₁) (tauY : r₄ ⟶ r₃)
    (alpha : g ≫ l₃ ⟶ l₁ ≫ h)
    (beta : g ≫ l₄ ⟶ l₂ ≫ h)
    (hRight :
      tauX ▷ g ≫ Bicategory.mateEquiv adj₁ adj₃ alpha =
        Bicategory.mateEquiv adj₂ adj₄ beta ≫ h ◁ tauY) :
    g ◁ (Bicategory.conjugateEquiv adj₄ adj₃).symm tauY ≫ beta =
      alpha ≫
        (Bicategory.conjugateEquiv adj₂ adj₁).symm tauX ▷ h := by
  let gammaX : l₁ ⟶ l₂ :=
    (Bicategory.conjugateEquiv adj₂ adj₁).symm tauX
  let gammaY : l₃ ⟶ l₄ :=
    (Bicategory.conjugateEquiv adj₄ adj₃).symm tauY
  change g ◁ gammaY ≫ beta = alpha ≫ gammaX ▷ h
  apply (Bicategory.mateEquiv adj₂ adj₃).injective
  calc
    _ = Bicategory.mateEquiv adj₂ adj₄ beta ≫
          h ◁ Bicategory.conjugateEquiv adj₄ adj₃ gammaY :=
      mateEquiv_conjugate_target adj₂ adj₃ adj₄ gammaY beta
    _ = (Bicategory.conjugateEquiv adj₂ adj₁ gammaX) ▷ g ≫
          Bicategory.mateEquiv adj₁ adj₃ alpha := by
      dsimp only [gammaX, gammaY]
      simpa only [Equiv.apply_symm_apply] using hRight.symm
    _ = Bicategory.mateEquiv adj₂ adj₃ (alpha ≫ gammaX ▷ h) :=
      mateEquiv_conjugate_source adj₁ adj₂ adj₃ gammaX alpha

universe uB' vB' wB' uC' vC' wC'
variable {B' : Type uB'} [Bicategory.{wB', vB'} B']
variable {C' : Type uC'} [Bicategory.{wC', vC'} C']
variable {F G : Pseudofunctor B' C'}
variable {σ θ ι : Pseudofunctor.StrongTrans F G}

/-- Recover a full ORIGINAL left strong modification from an arbitrary
RIGHT lax modification, by the inverse mathlib conjugate equivalence.
The naturality proof is the genuinely unmated right naturality square. -/
def leftModification
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (m : Oplax.LaxTrans.Modification dθ.right dσ.right) :
    Pseudofunctor.StrongTrans.Modification σ θ where
  app X :=
    (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X)).symm (m.app X)
  naturality {X Y} f := by
    have hRight := m.naturality f
    rw [dσ.naturality_eq_mate f, dθ.naturality_eq_mate f] at hRight
    exact left_naturality_of_right_mate
      (dσ.adj X) (dθ.adj X) (dσ.adj Y) (dθ.adj Y)
      (m.app X) (m.app Y)
      ((σ.naturality f).hom) ((θ.naturality f).hom)
      hRight

/-- Left-after-right recovers ANY original strong modification in full. -/
theorem leftModification_rightModification
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) :
    leftModification dσ dθ (rightModification dσ dθ Γ) = Γ := by
  apply Pseudofunctor.StrongTrans.Modification.ext
  funext X
  exact Equiv.symm_apply_apply _ _

/-- Right-after-left recovers ANY right lax modification in full.
No extra `Compatible` witness is imposed on the right modification. -/
theorem rightModification_leftModification
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (m : Oplax.LaxTrans.Modification dθ.right dσ.right) :
    rightModification dσ dθ (leftModification dσ dθ m) = m := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact Equiv.apply_symm_apply _ _

/-- Lossless 2-Hom equivalence. The right modification direction
reverses, exactly as required by the native bicategorical mates. -/
def modificationEquiv
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ) :
    (Pseudofunctor.StrongTrans.Modification σ θ) ≃
      (Oplax.LaxTrans.Modification dθ.right dσ.right) where
  toFun := rightModification dσ dθ
  invFun := leftModification dσ dθ
  left_inv := leftModification_rightModification dσ dθ
  right_inv := rightModification_leftModification dσ dθ

/-- Inverse mate transport respects composition in the opposite order,
at the level of WHOLE original strong modifications. -/
theorem leftModification_vcomp
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (dι : RightMateLaxData ι)
    (m : Oplax.LaxTrans.Modification dθ.right dσ.right)
    (n : Oplax.LaxTrans.Modification dι.right dθ.right) :
    leftModification dσ dι (Oplax.LaxTrans.Modification.vcomp n m) =
      Pseudofunctor.StrongTrans.Modification.vcomp
        (leftModification dσ dθ m)
        (leftModification dθ dι n) := by
  apply Pseudofunctor.StrongTrans.Modification.ext
  funext X
  change
    (Bicategory.conjugateEquiv (dι.adj X) (dσ.adj X)).symm
        (n.app X ≫ m.app X) =
      (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X)).symm (m.app X) ≫
        (Bicategory.conjugateEquiv (dι.adj X) (dθ.adj X)).symm (n.app X)
  exact (Bicategory.conjugateEquiv_symm_comp
    (dι.adj X) (dθ.adj X) (dσ.adj X)
    (n.app X) (m.app X)).symm

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Every modification of the original SOURCE right lax mate is
losslessly equivalent to an original source-unit strong modification.
All chosen η_X adjunctions remain exactly the old ones. -/
def actualLiftSourceModificationEquiv :
    (Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) ≃
    (Oplax.LaxTrans.Modification
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) :=
  Generic.modificationEquiv
    (actualLiftSourceRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

/-- The original target counit's full 2-Hom of modifications is
equivalent to that of its actual lax right mate, retaining R_E.mapComp. -/
def actualLiftTargetModificationEquiv :
    (Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) ≃
    (Oplax.LaxTrans.Modification
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) :=
  Generic.modificationEquiv
    (actualLiftTargetRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

#print axioms Generic.left_naturality_of_right_mate
#print axioms Generic.leftModification
#print axioms Generic.leftModification_rightModification
#print axioms Generic.rightModification_leftModification
#print axioms Generic.modificationEquiv
#print axioms Generic.leftModification_vcomp
#print axioms actualLiftSourceModificationEquiv
#print axioms actualLiftTargetModificationEquiv

end

end KUOS.DependentOriginationCoherentBiadjunctionInverseModificationMatesV5_115
