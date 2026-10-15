import KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteConcatenatedOriginalUnitCounitV5_123

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F26 / v5.123: actual source eta and target epsilon concatenated mate chains

These six proof constants specialize F26's genuinely composed finite
comparison paths to the original F14 source unit eta and target counit
epsilon. Original mapId/mapComp remain literal, nonstrict comparison
cells, and arbitrary further subdivisions are retained. The generic
F-side steps are invertible, but G-side steps may be noninvertible.
No reselected adjunctions and no upgrade of the original LAX mates.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Original SOURCE η finite concatenation, with all comparison choices retained. -/
def actualLiftSourceFiniteAppendNaturality
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
    (head : BiComparisonChain f ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) kF kG)
    {lF : X ⟶ Y}    {lG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteAppendNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f head tail

/-- Original TARGET ε finite concatenation, with all comparison choices retained. -/
def actualLiftTargetFiniteAppendNaturality
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
    (head : BiComparisonChain ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f) f kF kG)
    {lF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Y}    {lG : X ⟶ Y}
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteAppendNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f head tail

/-- Original SOURCE η finite concatenation, with all comparison choices retained. -/
def actualLiftSourceFiniteAppendMapIdNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {kF : X ⟶ X}
    {kG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X}
    (head : BiComparisonChain (𝟙 X) (𝟙 ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)) kF kG)
    {lF : X ⟶ X}    {lG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X}
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteOriginalMapIdNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X (Chains.append head tail)

/-- Original TARGET ε finite concatenation, with all comparison choices retained. -/
def actualLiftTargetFiniteAppendMapIdNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    {kF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X}
    {kG : X ⟶ X}
    (head : BiComparisonChain (𝟙 ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X)) (𝟙 X) kF kG)
    {lF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X}    {lG : X ⟶ X}
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteOriginalMapIdNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X (Chains.append head tail)

/-- Original SOURCE η finite concatenation, with all comparison choices retained. -/
def actualLiftSourceFiniteAppendMapCompNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : X ⟶ Z}
    {kG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z}
    (head : BiComparisonChain (f ≫ g)
      ((actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map g) kF kG)
    {lF : X ⟶ Z}    {lG : (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftSourceRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z}
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteOriginalMapCompNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g (Chains.append head tail)

/-- Original TARGET ε finite concatenation, with all comparison choices retained. -/
def actualLiftTargetFiniteAppendMapCompNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z}
    {kG : X ⟶ Z}
    (head : BiComparisonChain
      ((actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map f ≫ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).map g) (f ≫ g) kF kG)
    {lF : (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj X ⟶ (actualLiftTargetRoundtrip.{u, v, uH, vH, uW, uP} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).obj Z}    {lG : X ⟶ Z}
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteOriginalMapCompNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g (Chains.append head tail)

#print axioms actualLiftSourceFiniteAppendNaturality
#print axioms actualLiftTargetFiniteAppendNaturality
#print axioms actualLiftSourceFiniteAppendMapIdNaturality
#print axioms actualLiftTargetFiniteAppendMapIdNaturality
#print axioms actualLiftSourceFiniteAppendMapCompNaturality
#print axioms actualLiftTargetFiniteAppendMapCompNaturality

end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteConcatenatedOriginalUnitCounitV5_123
