import KUOS.DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105

namespace KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105

set_option autoImplicit false
noncomputable section

/-!
# Target compositor-corrected native right mate pasting (v5.106, F10)

F9 kept the original non-strict target compositor on the LEFT side of
the mate equation. F10 transfers that exact correction to the RIGHT
side and gives an explicit typed formula in terms of the original
two right mates and the original R_E.mapComp cell.

The statement does NOT discard the pseudofunctor compositor or
identify unrelated mates with isomorphisms. No F/G, eta/epsilon,
objectwise equivalence, triangulator, toolchain, or axiom is modified.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d : B}
variable {l₁ : a ⟶ b} {r₁ : b ⟶ a}
variable {l₂ : c ⟶ d} {r₂ : d ⟶ c}
variable {g₁ g₂ : a ⟶ c} {h : b ⟶ d}

/-- Naturality of native bicategorical mates in the left vertical
one-morphism: a source-side precomposition becomes a right-adjoint
left whisker, with the same comparison 2-cell and its direction. -/
theorem mateEquiv_precompose
    (adj₁ : Bicategory.Adjunction l₁ r₁)
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (θ : g₁ ⟶ g₂)
    (α : g₂ ≫ l₂ ⟶ l₁ ≫ h) :
    Bicategory.mateEquiv adj₁ adj₂ (θ ▷ l₂ ≫ α) =
      (r₁ ◁ θ) ≫ Bicategory.mateEquiv adj₁ adj₂ α := by
  simp only [Bicategory.mateEquiv_apply']
  calc
    _ = 𝟙 _ ⊗≫
        (r₁ ◁ (g₁ ◁ adj₂.unit ≫ θ ▷ (l₂ ≫ r₂))) ⊗≫
        r₁ ◁ α ▷ r₂ ⊗≫ adj₁.counit ▷ h ▷ r₂ ⊗≫ 𝟙 _ := by
      bicategory
    _ = 𝟙 _ ⊗≫
        (r₁ ◁ (θ ▷ (𝟙 c) ≫ g₂ ◁ adj₂.unit)) ⊗≫
        r₁ ◁ α ▷ r₂ ⊗≫ adj₁.counit ▷ h ▷ r₂ ⊗≫ 𝟙 _ := by
      rw [Bicategory.whisker_exchange θ adj₂.unit]
    _ = _ := by
      bicategory

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}
variable {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- The ORIGINAL target roundtrip compositor, transported to the
right-mate source by the ORIGINAL chosen right adjoint at X. -/
def actualLiftTargetCounitRightMapCompWhisker
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftTargetNativeAdjHom (W := W) A X).r ≫
        ((actualLiftTargetRoundtrip (W := W) A).map (f ≫ g)) ⟶
      (actualLiftTargetNativeAdjHom (W := W) A X).r ≫
        (((actualLiftTargetRoundtrip (W := W) A).map f) ≫
          ((actualLiftTargetRoundtrip (W := W) A).map g)) :=
  (actualLiftTargetNativeAdjHom (W := W) A X).r ◁
    ((actualLiftTargetRoundtrip (W := W) A).mapComp f g).hom

/-- Explicit compositor-corrected RIGHT mate paste, not the bare
vertical composite and not the strictification of R_E. -/
def actualLiftTargetCounitRightCorrectedVComp
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftTargetNativeAdjHom (W := W) A X).r ≫
        ((actualLiftTargetRoundtrip (W := W) A).map (f ≫ g)) ⟶
      (f ≫ g) ≫ (actualLiftTargetNativeAdjHom (W := W) A Z).r :=
  actualLiftTargetCounitRightMapCompWhisker (W := W) A f g ≫
    actualLiftTargetCounitMateVComp (W := W) A f g

/-- The mate of the ORIGINAL compositor-corrected left paste IS the
typed, compositor-corrected right paste. -/
theorem actualLiftTargetCounitCorrectedLeftMate_eq_rightPaste
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
        (actualLiftTargetNativeAdjHom (W := W) A X).adj
        (actualLiftTargetNativeAdjHom (W := W) A Z).adj)
      (((actualLiftTargetRoundtrip (W := W) A).mapComp f g).hom ▷
          (actualLiftTargetRoundtripCounit (W := W) A).app Z ≫
        Bicategory.leftAdjointSquare.vcomp
          ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
          ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom) =
      actualLiftTargetCounitRightCorrectedVComp (W := W) A f g := by
  calc
    _ = (actualLiftTargetCounitRightMapCompWhisker (W := W) A f g) ≫
        (Bicategory.mateEquiv
          (actualLiftTargetNativeAdjHom (W := W) A X).adj
          (actualLiftTargetNativeAdjHom (W := W) A Z).adj)
          (Bicategory.leftAdjointSquare.vcomp
            ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
            ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom) := by
      exact Generic.mateEquiv_precompose
        (actualLiftTargetNativeAdjHom (W := W) A X).adj
        (actualLiftTargetNativeAdjHom (W := W) A Z).adj
        ((actualLiftTargetRoundtrip (W := W) A).mapComp f g).hom
        (Bicategory.leftAdjointSquare.vcomp
          ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
          ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom)
    _ = _ := by
      have hMate := actualLiftTargetCounitMateVComp_eq (W := W) A f g
      simpa only [actualLiftTargetCounitRightCorrectedVComp] using
        congrArg
          (fun t => actualLiftTargetCounitRightMapCompWhisker (W := W) A f g ≫ t)
          hMate

/-- F10 target naturality_comp theorem: the ORIGINAL counit square at
f ≫ g, with its (identity-pseudofunctor) right correction, mates to the
right paste of both original target mates AFTER the genuine R_E
mapComp left-whisker. -/
theorem actualLiftTargetCounitMateComp_correctedRight
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
        (actualLiftTargetNativeAdjHom (W := W) A X).adj
        (actualLiftTargetNativeAdjHom (W := W) A Z).adj)
      (((actualLiftTargetRoundtripCounit (W := W) A).naturality (f ≫ g)).hom ≫
        (actualLiftTargetRoundtripCounit (W := W) A).app X ◁ 𝟙 (f ≫ g)) =
      actualLiftTargetCounitRightCorrectedVComp (W := W) A f g := by
  exact (actualLiftTargetCounitMateComp_native (W := W) A f g).trans
    (actualLiftTargetCounitCorrectedLeftMate_eq_rightPaste (W := W) A f g)

#print axioms Generic.mateEquiv_precompose
#print axioms actualLiftTargetCounitRightMapCompWhisker
#print axioms actualLiftTargetCounitRightCorrectedVComp
#print axioms actualLiftTargetCounitCorrectedLeftMate_eq_rightPaste
#print axioms actualLiftTargetCounitMateComp_correctedRight

end

end KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106
