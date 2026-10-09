import KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106

namespace KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107

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
open KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106
open KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106.Generic

set_option autoImplicit false
noncomputable section

/-!
# Original source and target identity naturality as corrected right mates (v5.107, F11)

F9 and F10 retain the genuine source and target mapComp correction.
The identity counterpart must likewise retain BOTH original mapId cells.

Target: the original R_E.mapId acts by a left whisker BEFORE the
right mate of the target counit.

Source: the original R_L.mapId acts by a right whisker AFTER the
right mate of the source unit.

The respective resulting mate pastes are exactly the right-then-left
unitor comparison for the ORIGINAL chosen right-adjoint leg. No
strictification, new adjunction, or replacement of the original eta,
epsilon, F, G, object equivalences or triangulators occurs.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d : B}
variable {l₁ : a ⟶ b} {r₁ : b ⟶ a}
variable {l₂ : c ⟶ d} {r₂ : d ⟶ c}
variable {g : a ⟶ c} {h₁ h₂ : b ⟶ d}

/-- A 2-cell on the RIGHT vertical leg of a left-adjoint square
becomes a right whisker of the corresponding right mate. This is
the complementary law to F10's mateEquiv_precompose and uses the
bicategorical interchange, not only associator/unitor coherence. -/
theorem mateEquiv_postcompose
    (adj₁ : Bicategory.Adjunction l₁ r₁)
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (α : g ≫ l₂ ⟶ l₁ ≫ h₁)
    (θ : h₁ ⟶ h₂) :
    Bicategory.mateEquiv adj₁ adj₂ (α ≫ l₁ ◁ θ) =
      Bicategory.mateEquiv adj₁ adj₂ α ≫ θ ▷ r₂ := by
  simp only [Bicategory.mateEquiv_apply']
  calc
    _ = 𝟙 _ ⊗≫
          r₁ ◁ g ◁ adj₂.unit ⊗≫
          r₁ ◁ α ▷ r₂ ⊗≫
          (((r₁ ≫ l₁) ◁ θ ≫ adj₁.counit ▷ h₂) ▷ r₂) ⊗≫ 𝟙 _ := by
      bicategory
    _ = 𝟙 _ ⊗≫
          r₁ ◁ g ◁ adj₂.unit ⊗≫
          r₁ ◁ α ▷ r₂ ⊗≫
          ((adj₁.counit ▷ h₁ ≫ (𝟙 b) ◁ θ) ▷ r₂) ⊗≫ 𝟙 _ := by
      rw [Bicategory.whisker_exchange adj₁.counit θ]
    _ = _ := by
      bicategory

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

section Target

variable (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel)

/-- The ORIGINAL target counit naturality square at the identity,
under the unchanged native mate equivalence, equals the right-adjoint
whisker of the ORIGINAL non-strict target mapId followed by the native
right/left unitor comparison of the chosen target right leg. -/
theorem actualLiftTargetCounitRightMate_id_mapId :
    actualLiftTargetCounitRightMate (W := W) A (𝟙 X) =
      ((actualLiftTargetNativeAdjHom (W := W) A X).r ◁
          ((actualLiftTargetRoundtrip (W := W) A).mapId X).hom) ≫
        (ρ_ (actualLiftTargetNativeAdjHom (W := W) A X).r).hom ≫
          (λ_ (actualLiftTargetNativeAdjHom (W := W) A X).r).inv := by
  let e := actualLiftTargetNativeAdjHom (W := W) A X
  let R := actualLiftTargetRoundtrip (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  let eps := actualLiftTargetRoundtripCounit (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  have hNat :
      ((eps.naturality (𝟙 X)).hom) =
        (R.mapId X).hom ▷ eps.app X ≫
          (λ_ (eps.app X)).hom ≫ (ρ_ (eps.app X)).inv := by
    have hId :
        ((Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)).mapId X).hom =
          𝟙 (𝟙 X) := rfl
    have hNative := eps.naturality_id X
    rw [hId] at hNative
    simpa only [Bicategory.whiskerLeft_id, Category.comp_id] using hNative
  change (Bicategory.mateEquiv e.adj e.adj)
      ((eps.naturality (𝟙 X)).hom) = _
  calc
    _ = (Bicategory.mateEquiv e.adj e.adj)
        ((R.mapId X).hom ▷ eps.app X ≫
          (λ_ (eps.app X)).hom ≫ (ρ_ (eps.app X)).inv) := by
      exact congrArg (Bicategory.mateEquiv e.adj e.adj) hNat
    _ = (e.r ◁ (R.mapId X).hom) ≫
          (Bicategory.mateEquiv e.adj e.adj)
            ((λ_ (eps.app X)).hom ≫ (ρ_ (eps.app X)).inv) := by
      exact mateEquiv_precompose e.adj e.adj
        (R.mapId X).hom
        ((λ_ (eps.app X)).hom ≫ (ρ_ (eps.app X)).inv)
    _ = _ := by
      simpa only [e] using
        congrArg (fun t => e.r ◁ (R.mapId X).hom ≫ t)
          (Bicategory.mateEquiv_leftUnitor_hom_rightUnitor_inv e.adj)

end Target

section Source

variable (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel)

/-- The source identity mate needs the original non-strict R_L.mapId
AFTER the right mate, as a genuine right whisker. The resulting
composite is the unitor paste of the same chosen source right leg. -/
theorem actualLiftSourceUnitRightMate_id_mapId :
    actualLiftSourceUnitRightMate (W := W) A (𝟙 X) ≫
        ((actualLiftSourceRoundtrip (W := W) A).mapId X).hom ▷
          (actualLiftSourceNativeAdjHom (W := W) A X).r =
      (ρ_ (actualLiftSourceNativeAdjHom (W := W) A X).r).hom ≫
        (λ_ (actualLiftSourceNativeAdjHom (W := W) A X).r).inv := by
  let e := actualLiftSourceNativeAdjHom (W := W) A X
  let R := actualLiftSourceRoundtrip (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  let eta := actualLiftSourceRoundtripUnit (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  have hNat :
      ((eta.naturality (𝟙 X)).hom) ≫
        eta.app X ◁ (R.mapId X).hom =
          (λ_ (eta.app X)).hom ≫ (ρ_ (eta.app X)).inv := by
    have hId :
        ((Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)).mapId X).hom =
          𝟙 (𝟙 X) := rfl
    have hNative := eta.naturality_id X
    rw [hId] at hNative
    simpa only [Bicategory.id_whiskerRight, Category.id_comp] using hNative
  change (Bicategory.mateEquiv e.adj e.adj)
      ((eta.naturality (𝟙 X)).hom) ≫
        (R.mapId X).hom ▷ e.r = _
  calc
    _ = (Bicategory.mateEquiv e.adj e.adj)
        (((eta.naturality (𝟙 X)).hom) ≫ eta.app X ◁ (R.mapId X).hom) := by
      exact (Generic.mateEquiv_postcompose e.adj e.adj
        ((eta.naturality (𝟙 X)).hom) ((R.mapId X).hom)).symm
    _ = (Bicategory.mateEquiv e.adj e.adj)
        ((λ_ (eta.app X)).hom ≫ (ρ_ (eta.app X)).inv) := by
      exact congrArg (Bicategory.mateEquiv e.adj e.adj) hNat
    _ = _ := by
      exact Bicategory.mateEquiv_leftUnitor_hom_rightUnitor_inv e.adj

end Source

#print axioms Generic.mateEquiv_postcompose
#print axioms actualLiftTargetCounitRightMate_id_mapId
#print axioms actualLiftSourceUnitRightMate_id_mapId

end

end KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107
