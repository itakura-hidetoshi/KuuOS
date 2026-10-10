import KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

namespace KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F17 / v5.114: automatic naturality of arbitrary right-mate modifications

The F16 compatibility condition follows from arbitrary strong modification
naturality whenever the chosen original objectwise adjunctions really
induce the right lax naturality squares by mathlib `mateEquiv`.
We prove the two missing mixed-adjunction pasting laws explicitly from
`Bicategory.mateEquiv_vcomp`, the genuine F10/F11 mate-whiskering
lemmas, and non-strict unitors.

No invertibility of arbitrary modification components or right-mate
naturality is assumed.  This closes the F16 compatibility boundary
rather than assuming a separate right-side naturality condition.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d : B}
variable {l₁ l₂ : a ⟶ b} {r₁ r₂ : b ⟶ a}
variable {l₃ l₄ : c ⟶ d} {r₃ r₄ : d ⟶ c}
variable {g : a ⟶ c} {h : b ⟶ d}

/-- Changing the SOURCE adjunction of a left square by an arbitrary
2-cell becomes conjugation followed by the unchanged right mate. -/
theorem mateEquiv_conjugate_source
    (adj₁ : Bicategory.Adjunction l₁ r₁)
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (adj₃ : Bicategory.Adjunction l₃ r₃)
    (γ : l₁ ⟶ l₂)
    (α : g ≫ l₃ ⟶ l₁ ≫ h) :
    (Bicategory.conjugateEquiv adj₂ adj₁ γ) ▷ g ≫
        Bicategory.mateEquiv adj₁ adj₃ α =
      Bicategory.mateEquiv adj₂ adj₃ (α ≫ γ ▷ h) := by
  let square : (𝟙 a) ≫ l₁ ⟶ l₂ ≫ (𝟙 b) :=
    (λ_ l₁).hom ≫ γ ≫ (ρ_ l₂).inv
  have hNorm :
      (λ_ g).inv ▷ l₃ ≫
        Bicategory.leftAdjointSquare.vcomp square α ≫
          l₂ ◁ (λ_ h).hom = α ≫ γ ▷ h := by
    dsimp [square, Bicategory.leftAdjointSquare.vcomp]
    bicategory
  symm
  calc
    _ = Bicategory.mateEquiv adj₂ adj₃
        ((λ_ g).inv ▷ l₃ ≫
          Bicategory.leftAdjointSquare.vcomp square α ≫
            l₂ ◁ (λ_ h).hom) := congrArg _ hNorm.symm
    _ = (r₂ ◁ (λ_ g).inv) ≫
          (Bicategory.mateEquiv adj₂ adj₃
            (Bicategory.leftAdjointSquare.vcomp square α)) ≫
          (λ_ h).hom ▷ r₃ := by
      rw [mateEquiv_precompose, mateEquiv_postcompose]
    _ = (r₂ ◁ (λ_ g).inv) ≫
          Bicategory.rightAdjointSquare.vcomp
            (Bicategory.mateEquiv adj₂ adj₁ square)
            (Bicategory.mateEquiv adj₁ adj₃ α) ≫
          (λ_ h).hom ▷ r₃ := by
      rw [Bicategory.mateEquiv_vcomp]
    _ = (Bicategory.conjugateEquiv adj₂ adj₁ γ) ▷ g ≫
          Bicategory.mateEquiv adj₁ adj₃ α := by
      dsimp only [square, Bicategory.rightAdjointSquare.vcomp]
      rw [Bicategory.conjugateEquiv_apply]
      bicategory

/-- Changing the TARGET adjunction of a left square becomes the
right mate followed by left whiskering of the conjugate 2-cell. -/
theorem mateEquiv_conjugate_target
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (adj₃ : Bicategory.Adjunction l₃ r₃)
    (adj₄ : Bicategory.Adjunction l₄ r₄)
    (γ : l₃ ⟶ l₄)
    (β : g ≫ l₄ ⟶ l₂ ≫ h) :
    Bicategory.mateEquiv adj₂ adj₃ (g ◁ γ ≫ β) =
      Bicategory.mateEquiv adj₂ adj₄ β ≫
        h ◁ (Bicategory.conjugateEquiv adj₄ adj₃ γ) := by
  let square : (𝟙 c) ≫ l₃ ⟶ l₄ ≫ (𝟙 d) :=
    (λ_ l₃).hom ≫ γ ≫ (ρ_ l₄).inv
  have hNorm :
      (ρ_ g).inv ▷ l₃ ≫
        Bicategory.leftAdjointSquare.vcomp β square ≫
          l₂ ◁ (ρ_ h).hom = g ◁ γ ≫ β := by
    dsimp [square, Bicategory.leftAdjointSquare.vcomp]
    bicategory
  calc
    _ = Bicategory.mateEquiv adj₂ adj₃
        ((ρ_ g).inv ▷ l₃ ≫
          Bicategory.leftAdjointSquare.vcomp β square ≫
            l₂ ◁ (ρ_ h).hom) := congrArg _ hNorm.symm
    _ = (r₂ ◁ (ρ_ g).inv) ≫
          (Bicategory.mateEquiv adj₂ adj₃
            (Bicategory.leftAdjointSquare.vcomp β square)) ≫
          (ρ_ h).hom ▷ r₃ := by
      rw [mateEquiv_precompose, mateEquiv_postcompose]
    _ = (r₂ ◁ (ρ_ g).inv) ≫
          Bicategory.rightAdjointSquare.vcomp
            (Bicategory.mateEquiv adj₂ adj₄ β)
            (Bicategory.mateEquiv adj₄ adj₃ square) ≫
          (ρ_ h).hom ▷ r₃ := by
      rw [Bicategory.mateEquiv_vcomp]
    _ = Bicategory.mateEquiv adj₂ adj₄ β ≫
          h ◁ (Bicategory.conjugateEquiv adj₄ adj₃ γ) := by
      dsimp only [square, Bicategory.rightAdjointSquare.vcomp]
      rw [Bicategory.conjugateEquiv_apply]
      bicategory

/-- A square of strong-transformation modifications becomes an
automatically commuting square of right mates. -/
theorem mate_naturality_of_modification
    (adj₁ : Bicategory.Adjunction l₁ r₁)
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (adj₃ : Bicategory.Adjunction l₃ r₃)
    (adj₄ : Bicategory.Adjunction l₄ r₄)
    (γX : l₁ ⟶ l₂) (γY : l₃ ⟶ l₄)
    (α : g ≫ l₃ ⟶ l₁ ≫ h)
    (β : g ≫ l₄ ⟶ l₂ ≫ h)
    (hnat : g ◁ γY ≫ β = α ≫ γX ▷ h) :
    (Bicategory.conjugateEquiv adj₂ adj₁ γX) ▷ g ≫
        Bicategory.mateEquiv adj₁ adj₃ α =
      Bicategory.mateEquiv adj₂ adj₄ β ≫
        h ◁ (Bicategory.conjugateEquiv adj₄ adj₃ γY) := by
  calc
    _ = Bicategory.mateEquiv adj₂ adj₃ (α ≫ γX ▷ h) :=
      mateEquiv_conjugate_source adj₁ adj₂ adj₃ γX α
    _ = Bicategory.mateEquiv adj₂ adj₃ (g ◁ γY ≫ β) :=
      congrArg _ hnat.symm
    _ = _ := mateEquiv_conjugate_target adj₂ adj₃ adj₄ γY β

end Generic

#print axioms Generic.mateEquiv_conjugate_source
#print axioms Generic.mateEquiv_conjugate_target
#print axioms Generic.mate_naturality_of_modification

end

end KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114
