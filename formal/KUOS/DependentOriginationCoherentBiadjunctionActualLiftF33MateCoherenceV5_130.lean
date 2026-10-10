import KUOS.DependentOriginationCoherentBiadjunctionF32NonstrictPentagonTriangleMatesV5_130

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftF33MateCoherenceV5_130

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionF32NonstrictPentagonTriangleMatesV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
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
# F33/v5.130 — unchanged original source eta/target epsilon higher mate coherence

The general F33 theorem proves native F32 quotient pentagon and
triangle equality through the original F29 mapId/mapComp as actual
right-mate boundary equations. We specialize to the SAME chosen
source unit η, target counit ε, chosen objectwise adjunctions and
original roundtrip pseudofunctors, without replacing any F/G comparison.

Source: F = original identity, G = original roundtrip.
Target: F = original roundtrip, G = original identity.
The F-side uses its original isomorphism; G-side comparisons remain
arbitrary (potentially noninvertible) forward 2-cells.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- ORIGINAL SOURCE η/ε Pentagon with nonstrict MapId:
both authentic lax right-mate boundaries and the F/G compressed
comparison remain equal between long/short quotient routes. -/
def actualLiftSourcePentagonMapIdMateCompatibility
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel)
    {bF cF dF bG cG dG : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ bF) (vF : bF ⟶ cF)
    (wF : cF ⟶ dF) (zF : dF ⟶ X)
    (uG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ bG) (vG : bG ⟶ cG)
    (wG : cG ⟶ dG) (zG : dG ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)
    (prefix :
      (⟨⟨𝟙 (X), 𝟙 ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)⟩⟩ : compressionKernelCategory (X) (X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)) ⟶
      (⟨⟨(((uF ≫ vF) ≫ wF) ≫ zF), (((uG ≫ vG) ≫ wG) ≫ zG)⟩⟩ : compressionKernelCategory (X) (X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X))) :=
  originalPentagonMapIdMateCompatibility
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ X uF vF wF zF uG vG wG zG prefix

/-- ORIGINAL SOURCE η/ε Triangle with nonstrict MapComp:
both authentic lax right-mate boundaries and the F/G compressed
comparison remain equal between long/short quotient routes. -/
def actualLiftSourceTriangleMapCompMateCompatibility
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {bF bG : ActualLiftSource.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel}
    (uF : X ⟶ bF) (vF : bF ⟶ Z)
    (uG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ bG) (vG : bG ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z)
    (prefix :
      (⟨⟨f ≫ g, (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map g⟩⟩ : compressionKernelCategory (X) (Z) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z)) ⟶
      (⟨⟨((uF ≫ 𝟙 bF) ≫ vF), ((uG ≫ 𝟙 bG) ≫ vG)⟩⟩ : compressionKernelCategory (X) (Z) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z))) :=
  originalTriangleMapCompMateCompatibility
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f g uF vF uG vG prefix

/-- ORIGINAL TARGET η/ε Pentagon with nonstrict MapId:
both authentic lax right-mate boundaries and the F/G compressed
comparison remain equal between long/short quotient routes. -/
def actualLiftTargetPentagonMapIdMateCompatibility
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel)
    {bF cF dF bG cG dG : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel}
    (uF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ bF) (vF : bF ⟶ cF)
    (wF : cF ⟶ dF) (zF : dF ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)
    (uG : X ⟶ bG) (vG : bG ⟶ cG)
    (wG : cG ⟶ dG) (zG : dG ⟶ X)
    (prefix :
      (⟨⟨𝟙 ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X), 𝟙 (X)⟩⟩ : compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) (X) (X)) ⟶
      (⟨⟨(((uF ≫ vF) ≫ wF) ≫ zF), (((uG ≫ vG) ≫ wG) ≫ zG)⟩⟩ : compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) (X) (X))) :=
  originalPentagonMapIdMateCompatibility
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ X uF vF wF zF uG vG wG zG prefix

/-- ORIGINAL TARGET η/ε Triangle with nonstrict MapComp:
both authentic lax right-mate boundaries and the F/G compressed
comparison remain equal between long/short quotient routes. -/
def actualLiftTargetTriangleMapCompMateCompatibility
    (Γ : Pseudofunctor.StrongTrans.Modification (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z)
    {bF bG : ActualLiftTarget.{u, v, uH, vH, uW, uP} (W := W) A WorldLabel PresentationLabel}
    (uF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ bF) (vF : bF ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z)
    (uG : X ⟶ bG) (vG : bG ⟶ Z)
    (prefix :
      (⟨⟨(actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map g, f ≫ g⟩⟩ : compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z) (X) (Z)) ⟶
      (⟨⟨((uF ≫ 𝟙 bF) ≫ vF), ((uG ≫ 𝟙 bG) ≫ vG)⟩⟩ : compressionKernelCategory ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X) ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z) (X) (Z))) :=
  originalTriangleMapCompMateCompatibility
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) Γ f g uF vF uG vG prefix
#print axioms actualLiftSourcePentagonMapIdMateCompatibility
#print axioms actualLiftSourceTriangleMapCompMateCompatibility
#print axioms actualLiftTargetPentagonMapIdMateCompatibility
#print axioms actualLiftTargetTriangleMapCompMateCompatibility

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftF33MateCoherenceV5_130
