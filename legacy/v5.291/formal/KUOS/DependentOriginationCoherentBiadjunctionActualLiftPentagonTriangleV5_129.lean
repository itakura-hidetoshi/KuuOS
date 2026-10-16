import KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftPentagonTriangleV5_129

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F32/v5.129: actual source eta and target epsilon pentagon/triangle

Retain the original F14 source/target roundtrip pseudofunctors and
their selected right-mate data. These proofs use the EXACT original
F- and G-side images of composable 1-cells, without pretending that
the nonstrict mapComp cells are identities.

The genuine F28 quotient pentagon and triangle laws therefore apply to
the original source eta and target epsilon presentations, with no
replacement functor or newly selected adjunction. Arbitrary G comparison
2-cells in these categories remain potentially NONINVERTIBLE.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The actual SOURCE eta roundtrip's F32 PENTAGON equality on the
genuine kernel quotient, using the original R.map and base 1-cells. -/
def actualLiftSourceKernelPentagon
    {X Y Z T U : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) (i : T ⟶ U) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
    (W := W) A (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  kernelQuotientPentagon f g h i (R.map f) (R.map g) (R.map h) (R.map i)

/-- The actual TARGET epsilon roundtrip's F32 PENTAGON equality,
preserving the original F=R and G=identity orientation. -/
def actualLiftTargetKernelPentagon
    {X Y Z T U : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) (i : T ⟶ U) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
    (W := W) A (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  kernelQuotientPentagon (R.map f) (R.map g) (R.map h) (R.map i) f g h i

/-- SOURCE eta genuine kernel-quotient TRIANGLE for arbitrary
original composable source 1-cells. -/
def actualLiftSourceKernelTriangle
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  let R := actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP}
    (W := W) A (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  kernelQuotientTriangle f g (R.map f) (R.map g)

/-- TARGET epsilon genuine kernel-quotient TRIANGLE, preserving
original F=R and target G comparison directions. -/
def actualLiftTargetKernelTriangle
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  let R := actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP}
    (W := W) A (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  kernelQuotientTriangle (R.map f) (R.map g) f g

#print axioms actualLiftSourceKernelPentagon
#print axioms actualLiftTargetKernelPentagon
#print axioms actualLiftSourceKernelTriangle
#print axioms actualLiftTargetKernelTriangle

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftPentagonTriangleV5_129
