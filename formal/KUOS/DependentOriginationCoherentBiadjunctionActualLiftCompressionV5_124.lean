import KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftCompressionV5_124

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F27: original source eta / target epsilon compression and mate descent

These two concrete compression functors use the UNCHANGED original
roundtrip pseudofunctors. Two corresponding mate-boundary descent
theorems preserve the original F14 source-unit and target-counit,
objectwise selected adjunctions, mapId/mapComp, and LAX right mates.

Both source and target paths may have arbitrary finite length, and all
G comparison 2-cells remain potentially noninvertible. Equality of
actual compressed functor maps suffices for equality of BOTH genuine
finite right-mate pastings. The conclusion type is inferred to prevent
huge refinement-indexed whnf reduction in theorem headers.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Genuine compression functor for the ORIGINAL source classification
and the unchanged source roundtrip pseudofunctor. -/
def actualLiftSourceCompressionFunctor
    (X Y : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  comparisonCompressionFunctor X Y (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y

/-- Genuine compression functor for the ORIGINAL target classification
and the unchanged target roundtrip pseudofunctor. -/
def actualLiftTargetCompressionFunctor
    (X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel) :=
  comparisonCompressionFunctor (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y X Y

/-- Equality in the original SOURCE compressed category
forces equality of both original source/target mate pasting boundaries. -/
def actualLiftSourceMateCompressionDescent
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
    (c₁ c₂ : BiComparisonChain f ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) kF kG)
    (h : (actualLiftSourceCompressionFunctor (W := W) A X Y).map
      (X := ⟨f, (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f⟩) (Y := ⟨kF, kG⟩) c₁ =
      (actualLiftSourceCompressionFunctor (W := W) A X Y).map
      (X := ⟨f, (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f⟩) (Y := ⟨kF, kG⟩) c₂) :=
  finiteMateBoundaries_eq_of_compression_map_eq
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c₁ c₂ h

/-- Equality in the original TARGET compressed category
forces equality of both original source/target mate pasting boundaries. -/
def actualLiftTargetMateCompressionDescent
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
    (c₁ c₂ : BiComparisonChain ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) f kF kG)
    (h : (actualLiftTargetCompressionFunctor (W := W) A X Y).map
      (X := ⟨(actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f, f⟩) (Y := ⟨kF, kG⟩) c₁ =
      (actualLiftTargetCompressionFunctor (W := W) A X Y).map
      (X := ⟨(actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f, f⟩) (Y := ⟨kF, kG⟩) c₂) :=
  finiteMateBoundaries_eq_of_compression_map_eq
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f c₁ c₂ h

#print axioms actualLiftSourceCompressionFunctor
#print axioms actualLiftTargetCompressionFunctor
#print axioms actualLiftSourceMateCompressionDescent
#print axioms actualLiftTargetMateCompressionDescent

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftCompressionV5_124
