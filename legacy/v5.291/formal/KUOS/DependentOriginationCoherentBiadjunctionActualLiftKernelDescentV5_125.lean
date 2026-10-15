import KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftKernelDescentV5_125

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F28/v5.125: native source η / target ε compression-kernel descent

The F28 quotient-category equivalence and quotient-level mate
boundary naturality are specialized to the UNCHANGED original source
unit eta and target counit epsilon, including the original F/G,
mapId/mapComp, chosen adjunctions and LAX right mates.

Only the auxiliary comparison categories are quotient-equivalent,
not the original ambient bicategories.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Original SOURCE comparison-category kernel quotient equivalence. -/
def actualLiftSourceKernelEquivalence
    (X Y : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  comparisonKernelEquivalence X Y (R.obj X) (R.obj Y)

/-- Original SOURCE kernel-quotient mate descent, preserving LAX orientation. -/
def actualLiftSourceQuotientMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {kF : X ⟶ Y}
    {kG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    (c : KernelHom f ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) kF kG) :=
  quotientMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c

/-- Original SOURCE kernel-quotient mate descent, preserving LAX orientation. -/
def actualLiftSourceQuotientLeftBoundaryEqCompressed
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {kF : X ⟶ Y}
    {kG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    (c : KernelHom f ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) kF kG) :=
  quotientLeftMateBoundary_eq_compressed
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c

/-- Original SOURCE kernel-quotient mate descent, preserving LAX orientation. -/
def actualLiftSourceQuotientRightBoundaryEqCompressed
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {kF : X ⟶ Y}
    {kG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    (c : KernelHom f ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) kF kG) :=
  quotientRightMateBoundary_eq_compressed
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c

/-- Original TARGET comparison-category kernel quotient equivalence. -/
def actualLiftTargetKernelEquivalence
    (X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  comparisonKernelEquivalence (R.obj X) (R.obj Y) X Y

/-- Original TARGET kernel-quotient mate descent, preserving LAX orientation. -/
def actualLiftTargetQuotientMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {kF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    {kG : X ⟶ Y}
    (c : KernelHom ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) f kF kG) :=
  quotientMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c

/-- Original TARGET kernel-quotient mate descent, preserving LAX orientation. -/
def actualLiftTargetQuotientLeftBoundaryEqCompressed
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {kF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    {kG : X ⟶ Y}
    (c : KernelHom ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) f kF kG) :=
  quotientLeftMateBoundary_eq_compressed
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c

/-- Original TARGET kernel-quotient mate descent, preserving LAX orientation. -/
def actualLiftTargetQuotientRightBoundaryEqCompressed
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y)
    {kF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    {kG : X ⟶ Y}
    (c : KernelHom ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) f kF kG) :=
  quotientRightMateBoundary_eq_compressed
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c

#print axioms actualLiftSourceKernelEquivalence
#print axioms actualLiftSourceQuotientMateNaturality
#print axioms actualLiftSourceQuotientLeftBoundaryEqCompressed
#print axioms actualLiftSourceQuotientRightBoundaryEqCompressed
#print axioms actualLiftTargetKernelEquivalence
#print axioms actualLiftTargetQuotientMateNaturality
#print axioms actualLiftTargetQuotientLeftBoundaryEqCompressed
#print axioms actualLiftTargetQuotientRightBoundaryEqCompressed

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftKernelDescentV5_125
