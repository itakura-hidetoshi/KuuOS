import KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftStagewiseHexagonV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132 — ORIGINAL source η and target ε on the stagewise
F31/F34 mixed natural HEXAGON

F35-D's complete stagewise quotient NatIso higher coherence preserves
the ACTUAL original lax right-mate modification boundary naturality,
including nonstrict original mapId/mapComp. Specialize these results to
the SAME original source-unit η and target-counit ε presentations and
their fixed chosen right mates.

These function-valued declarations retain all original external
1-cells and arbitrary quotient arrows as remaining explicit arguments;
no pointwise restriction to identities and no newly selected adjuncts.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Original SOURCE General higher coherence of the
real four-stage F35 quotient NatIso with unchanged η/ε lax right-mate
data. All remaining external comparison arrows stay general. -/
def actualLiftSourceStagewiseHexagonGeneralMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :=
  kernelStagewiseHexagonOriginalMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f

/-- Original SOURCE MapId higher coherence of the
real four-stage F35 quotient NatIso with unchanged η/ε lax right-mate
data. All remaining external comparison arrows stay general. -/
def actualLiftSourceStagewiseHexagonMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  kernelStagewiseHexagonOriginalMapIdMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ X

/-- Original SOURCE MapComp higher coherence of the
real four-stage F35 quotient NatIso with unchanged η/ε lax right-mate
data. All remaining external comparison arrows stay general. -/
def actualLiftSourceStagewiseHexagonMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  kernelStagewiseHexagonOriginalMapCompMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f g

/-- Original TARGET General higher coherence of the
real four-stage F35 quotient NatIso with unchanged η/ε lax right-mate
data. All remaining external comparison arrows stay general. -/
def actualLiftTargetStagewiseHexagonGeneralMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :=
  kernelStagewiseHexagonOriginalMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f

/-- Original TARGET MapId higher coherence of the
real four-stage F35 quotient NatIso with unchanged η/ε lax right-mate
data. All remaining external comparison arrows stay general. -/
def actualLiftTargetStagewiseHexagonMapIdMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  kernelStagewiseHexagonOriginalMapIdMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ X

/-- Original TARGET MapComp higher coherence of the
real four-stage F35 quotient NatIso with unchanged η/ε lax right-mate
data. All remaining external comparison arrows stay general. -/
def actualLiftTargetStagewiseHexagonMapCompMateNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  kernelStagewiseHexagonOriginalMapCompMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH}
      (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) Γ f g
#print axioms actualLiftSourceStagewiseHexagonGeneralMateNaturality
#print axioms actualLiftSourceStagewiseHexagonMapIdMateNaturality
#print axioms actualLiftSourceStagewiseHexagonMapCompMateNaturality
#print axioms actualLiftTargetStagewiseHexagonGeneralMateNaturality
#print axioms actualLiftTargetStagewiseHexagonMapIdMateNaturality
#print axioms actualLiftTargetStagewiseHexagonMapCompMateNaturality

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftStagewiseHexagonV5_132
