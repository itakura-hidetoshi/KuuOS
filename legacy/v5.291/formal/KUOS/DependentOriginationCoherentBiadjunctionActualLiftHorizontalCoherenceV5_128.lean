import KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientUnitorV5_128

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalCoherenceV5_128

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientAssociatorV5_128.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientUnitorV5_128.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F31/v5.128: the actual source eta / target epsilon presentations

Specialize the native F31 horizontal associator/unitor natural
isomorphisms to the SAME original source/target roundtrip pseudofunctors
used by F14, F28 and F29. The associated chosen adjunctions and LAX
right mates remain untouched. G-side arbitrary comparisons are not
required to be invertible, even though the STRUCTURAL associator
and unitor have actual bicategorical inverses.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Original SOURCE presentation: true two-stage left
horizontal associator on the actual F28 comparison-kernel quotient. -/
def actualLiftSourceLeftKernelAssociatorNatIso
    (X Y U V : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) (f : U ⟶ X) (g : V ⟶ U) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  leftKernelQuotientAssociatorNatIso X Y (R.obj X) (R.obj Y) f (R.map f) g (R.map g)

/-- Original SOURCE presentation: true two-stage right
horizontal associator, with the original roundtrip G/F orientations. -/
def actualLiftSourceRightKernelAssociatorNatIso
    (X Y Z T : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) (f : Y ⟶ Z) (g : Z ⟶ T) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  rightKernelQuotientAssociatorNatIso X Y (R.obj X) (R.obj Y) f (R.map f) g (R.map g)

/-- Original SOURCE left unitor as a native quotient
natural isomorphism rather than an identity strictification. -/
def actualLiftSourceLeftKernelUnitorNatIso
    (X Y : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  leftKernelQuotientUnitorNatIso X Y (R.obj X) (R.obj Y)

/-- Original SOURCE right unitor, retaining all
original nonstrict F/G comparison presentations. -/
def actualLiftSourceRightKernelUnitorNatIso
    (X Y : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  rightKernelQuotientUnitorNatIso X Y (R.obj X) (R.obj Y)

/-- Original TARGET presentation: true two-stage left
horizontal associator on the actual F28 comparison-kernel quotient. -/
def actualLiftTargetLeftKernelAssociatorNatIso
    (X Y U V : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) (f : U ⟶ X) (g : V ⟶ U) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  leftKernelQuotientAssociatorNatIso (R.obj X) (R.obj Y) X Y (R.map f) f (R.map g) g

/-- Original TARGET presentation: true two-stage right
horizontal associator, with the original roundtrip G/F orientations. -/
def actualLiftTargetRightKernelAssociatorNatIso
    (X Y Z T : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) (f : Y ⟶ Z) (g : Z ⟶ T) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  rightKernelQuotientAssociatorNatIso (R.obj X) (R.obj Y) X Y (R.map f) f (R.map g) g

/-- Original TARGET left unitor as a native quotient
natural isomorphism rather than an identity strictification. -/
def actualLiftTargetLeftKernelUnitorNatIso
    (X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  leftKernelQuotientUnitorNatIso (R.obj X) (R.obj Y) X Y

/-- Original TARGET right unitor, retaining all
original nonstrict F/G comparison presentations. -/
def actualLiftTargetRightKernelUnitorNatIso
    (X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  rightKernelQuotientUnitorNatIso (R.obj X) (R.obj Y) X Y

#print axioms actualLiftSourceLeftKernelAssociatorNatIso
#print axioms actualLiftSourceRightKernelAssociatorNatIso
#print axioms actualLiftSourceLeftKernelUnitorNatIso
#print axioms actualLiftSourceRightKernelUnitorNatIso
#print axioms actualLiftTargetLeftKernelAssociatorNatIso
#print axioms actualLiftTargetRightKernelAssociatorNatIso
#print axioms actualLiftTargetLeftKernelUnitorNatIso
#print axioms actualLiftTargetRightKernelUnitorNatIso

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftHorizontalCoherenceV5_128
