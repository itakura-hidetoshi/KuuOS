import KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107

namespace KUOS.DependentOriginationCoherentBiadjunctionNativeMatesTwoCellNaturalityV5_108

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104
open KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107.Generic

set_option autoImplicit false
noncomputable section

/-!
# Right-mate two-cell naturality of original actual lifts (v5.108 / F12)

v5.104 transported the original StrongTrans naturality-naturality
equation UNDER mateEquiv. v5.106 and v5.107 established the two
genuine bicategorical mate whiskering laws. Here their combination
produces the DIRECT right-adjoint naturality square.

The source compares theta with R_L.map₂ theta; the target reverses
these roles and compares R_E.map₂ theta with theta. Both sides
retain the original chosen right adjoints, F/G, eta/epsilon and all
pseudofunctor comparison cells. No additional strictification,
invertibility assertion, choice, or axiom is introduced.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d : B}
variable {l₁ : a ⟶ b} {r₁ : b ⟶ a}
variable {l₂ : c ⟶ d} {r₂ : d ⟶ c}
variable {g₁ g₂ : a ⟶ c} {h₁ h₂ : b ⟶ d}

/-- A commutative square of ORIGINAL left-adjoint 2-cells has a
commutative square of their genuine right mates, with the left and
right vertical 2-cells transported by the appropriate whiskers.
The 2-cells need not be invertible. -/
theorem rightMate_naturality_of_leftSquare
    (adj₁ : Bicategory.Adjunction l₁ r₁)
    (adj₂ : Bicategory.Adjunction l₂ r₂)
    (θ : g₁ ⟶ g₂) (φ : h₁ ⟶ h₂)
    (α : g₁ ≫ l₂ ⟶ l₁ ≫ h₁)
    (β : g₂ ≫ l₂ ⟶ l₁ ≫ h₂)
    (h : θ ▷ l₂ ≫ β = α ≫ l₁ ◁ φ) :
    (r₁ ◁ θ) ≫ Bicategory.mateEquiv adj₁ adj₂ β =
      Bicategory.mateEquiv adj₁ adj₂ α ≫ φ ▷ r₂ := by
  calc
    _ = Bicategory.mateEquiv adj₁ adj₂ (θ ▷ l₂ ≫ β) :=
      (mateEquiv_precompose adj₁ adj₂ θ β).symm
    _ = Bicategory.mateEquiv adj₁ adj₂ (α ≫ l₁ ◁ φ) :=
      congrArg (Bicategory.mateEquiv adj₁ adj₂) h
    _ = _ := mateEquiv_postcompose adj₁ adj₂ α φ

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

section Source

variable {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- F12 source: a DIRECT right-mate naturality square.
The original source theta is whiskered on the left by eta_X's
chosen right adjoint; the actual R_L.map₂ theta is whiskered
on the right by eta_Y's chosen right adjoint. -/
theorem actualLiftSourceUnitRightMate_naturality₂_explicit
    {f g : X ⟶ Y} (θ : f ⟶ g) :
    ((actualLiftSourceNativeAdjHom (W := W) A X).r ◁ θ) ≫
        actualLiftSourceUnitRightMate (W := W) A g =
      actualLiftSourceUnitRightMate (W := W) A f ≫
        (actualLiftSourceRoundtrip (W := W) A).map₂ θ ▷
          (actualLiftSourceNativeAdjHom (W := W) A Y).r := by
  exact Generic.rightMate_naturality_of_leftSquare
    (actualLiftSourceNativeAdjHom (W := W) A X).adj
    (actualLiftSourceNativeAdjHom (W := W) A Y).adj
    θ
    ((actualLiftSourceRoundtrip (W := W) A).map₂ θ)
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality g).hom
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality_naturality θ)

end Source

section Target

variable {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- F12 target: a DIRECT right-mate naturality square.
The actual R_E.map₂ theta is whiskered on the left by epsilon_X's
chosen right adjoint; the original theta is whiskered on the
right by epsilon_Y's chosen right adjoint. -/
theorem actualLiftTargetCounitRightMate_naturality₂_explicit
    {f g : X ⟶ Y} (θ : f ⟶ g) :
    ((actualLiftTargetNativeAdjHom (W := W) A X).r ◁
        (actualLiftTargetRoundtrip (W := W) A).map₂ θ) ≫
        actualLiftTargetCounitRightMate (W := W) A g =
      actualLiftTargetCounitRightMate (W := W) A f ≫
        θ ▷ (actualLiftTargetNativeAdjHom (W := W) A Y).r := by
  exact Generic.rightMate_naturality_of_leftSquare
    (actualLiftTargetNativeAdjHom (W := W) A X).adj
    (actualLiftTargetNativeAdjHom (W := W) A Y).adj
    ((actualLiftTargetRoundtrip (W := W) A).map₂ θ)
    θ
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality_naturality θ)

end Target

#print axioms Generic.rightMate_naturality_of_leftSquare
#print axioms actualLiftSourceUnitRightMate_naturality₂_explicit
#print axioms actualLiftTargetCounitRightMate_naturality₂_explicit

end

end KUOS.DependentOriginationCoherentBiadjunctionNativeMatesTwoCellNaturalityV5_108
