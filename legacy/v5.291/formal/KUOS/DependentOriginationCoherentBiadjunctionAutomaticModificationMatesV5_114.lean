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
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
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


/-! ## General unrestricted transport from arbitrary strong modifications -/

universe uB' vB' wB' uC' vC' wC'
variable {B' : Type uB'} [Bicategory.{wB', vB'} B']
variable {C' : Type uC'} [Bicategory.{wC', vC'} C']
variable {F G : Pseudofunctor B' C'}
variable {σ θ ι : Pseudofunctor.StrongTrans F G}

/-- F17: the exact F16 compatibility obstruction ALWAYS vanishes for
arbitrary original strong modifications whose pointwise adjunct data
have the genuine `mateEquiv` naturality guaranteed by
`RightMateLaxData`. No invertibility of Γ is required. -/
theorem compatible_of_modification
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) :
    Compatible dσ dθ Γ := by
  intro X Y f
  change
    (Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)) ▷ F.map f ≫
        dσ.right.naturality f =
      dθ.right.naturality f ≫
        G.map f ◁ (Bicategory.conjugateEquiv (dθ.adj Y) (dσ.adj Y) (Γ.app Y))
  rw [dσ.naturality_eq_mate f, dθ.naturality_eq_mate f]
  exact mate_naturality_of_modification
    (dσ.adj X) (dθ.adj X) (dσ.adj Y) (dθ.adj Y)
    (Γ.app X) (Γ.app Y)
    ((σ.naturality f).hom) ((θ.naturality f).hom)
    (Γ.naturality f)

/-- Fully automatic contravariant transport of ANY strong modification
to an actual mathlib lax modification, with no manually supplied
`Compatible` witness. All original pseudofunctor compositors remain. -/
def rightModification
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) :
    Oplax.LaxTrans.Modification dθ.right dσ.right :=
  toRightModification dσ dθ Γ (compatible_of_modification dσ dθ Γ)

/-- Genuine identity law on automatic lax modification transport. -/
theorem rightModification_id (dσ : RightMateLaxData σ) :
    rightModification dσ dσ
        (Pseudofunctor.StrongTrans.Modification.id σ) =
      Oplax.LaxTrans.Modification.id dσ.right := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  change Bicategory.conjugateEquiv (dσ.adj X) (dσ.adj X) (𝟙 _) = 𝟙 _
  exact Bicategory.conjugateEquiv_id (dσ.adj X)

/-- Contravariant vertical composition of arbitrary modifications,
as an equality of full mathlib lax modifications, without manually
supplying a compatibility condition for any factor. -/
theorem rightModification_vcomp
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (dι : RightMateLaxData ι)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (deltaMod : Pseudofunctor.StrongTrans.Modification θ ι) :
    rightModification dσ dι
        (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) =
      Oplax.LaxTrans.Modification.vcomp
        (rightModification dθ dι deltaMod)
        (rightModification dσ dθ Γ) := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact conjugateComponent_vcomp dσ dθ dι Γ deltaMod X

end Generic


universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- F17 for ANY original source-unit endomodification (not only the
unit's normalized triangle): the right-mate naturality equation is
automatically certified by the same original objectwise adjunctions. -/
theorem actualLiftSourceArbitraryModification_compatible
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) :
    Compatible
      (actualLiftSourceRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ :=
  Generic.compatible_of_modification _ _ Γ

/-- The unchanged F14 SOURCE lax right mate receives every original
source-unit endomodification as a genuine natural modification. -/
def actualLiftSourceArbitraryModification_rightMate
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) :
    Oplax.LaxTrans.Modification
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) :=
  Generic.rightModification
    (actualLiftSourceRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ

/-- F17 for ANY original target-counit endomodification, retaining
the genuine non-strict R_E compositor. -/
theorem actualLiftTargetArbitraryModification_compatible
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) :
    Compatible
      (actualLiftTargetRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ :=
  Generic.compatible_of_modification _ _ Γ

/-- The unchanged F14 TARGET lax right mate receives every
original target-counit endomodification automatically. -/
def actualLiftTargetArbitraryModification_rightMate
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))) :
    Oplax.LaxTrans.Modification
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) :=
  Generic.rightModification
    (actualLiftTargetRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ

#print axioms Generic.mateEquiv_conjugate_source
#print axioms Generic.mateEquiv_conjugate_target
#print axioms Generic.mate_naturality_of_modification
#print axioms Generic.compatible_of_modification
#print axioms Generic.rightModification
#print axioms Generic.rightModification_id
#print axioms Generic.rightModification_vcomp
#print axioms actualLiftSourceArbitraryModification_compatible
#print axioms actualLiftSourceArbitraryModification_rightMate
#print axioms actualLiftTargetArbitraryModification_compatible
#print axioms actualLiftTargetArbitraryModification_rightMate

end

end KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114
