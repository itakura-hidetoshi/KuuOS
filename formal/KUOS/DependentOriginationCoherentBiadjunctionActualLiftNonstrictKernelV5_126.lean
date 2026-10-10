import KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftNonstrictKernelV5_126

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

set_option autoImplicit false
noncomputable section

/-!
# F29 / v5.126: native original eta/epsilon nonstrict kernel descent

These declarations specialize the TRUE F29 kernel-quotient mapId/mapComp
operations and their descended lax right-mate naturality to the original
source unit eta and target counit epsilon, not replacement strong
transformations or strict comparison choices. Full dependent Hom
types remain inferred from the proved generic theorem.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- SOURCE eta: original nonstrict mapId on kernel classes, with both
genuine mate boundaries descending to the same cell. -/
def actualLiftSourceMapIdQuotientNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  originalMapIdQuotientMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- TARGET epsilon: its actual roundtrip mapId and identity-side
comparisons are unchanged; the original lax mate square descends. -/
def actualLiftTargetMapIdQuotientNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    (X : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  originalMapIdQuotientMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ X

/-- SOURCE eta: the complete original nonstrict mapComp pair acts on
kernel classes and respects both native original mate boundaries. -/
def actualLiftSourceMapCompQuotientNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRoundtripUnit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  originalMapCompQuotientMateNaturality
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

/-- TARGET epsilon: the unchanged mapComp cells and arbitrarily
noninvertible G comparisons are compatible with kernel mate descent. -/
def actualLiftTargetMapCompQuotientNaturality
    (Γ : Pseudofunctor.StrongTrans.Modification
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRoundtripCounit.{u, v, uH, vH, uW, uP} (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))
    {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :=
  originalMapCompQuotientMateNaturality
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetRightMateData.{u, v, uH, uW, uP, vH} (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    Γ f g

#print axioms actualLiftSourceMapIdQuotientNaturality
#print axioms actualLiftTargetMapIdQuotientNaturality
#print axioms actualLiftSourceMapCompQuotientNaturality
#print axioms actualLiftTargetMapCompQuotientNaturality

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftNonstrictKernelV5_126
