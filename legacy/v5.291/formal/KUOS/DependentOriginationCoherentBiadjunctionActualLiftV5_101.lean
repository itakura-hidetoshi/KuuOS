import KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93
import KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100

namespace KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66
open KUOS.DependentOriginationForwardCanonicalNaturalityV5_87
open KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93
open KUOS.DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96
open KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100

set_option autoImplicit false
noncomputable section

/-!
# The original actual-lift coherent biadjunction certificate (v5.101)

This is a *carrier* for the chosen KuuOS unit/counit and both native
triangulator modifications, equipped with the original, independently
constructed F3 (unit-centered) and F4 (counit-centered) interchangers.
Its two equations are exactly the v5.65 and v5.66 swallowtail
predicates, not weaker pointwise stand-ins.

v5.93 proves the forward law, and v5.100 proves the reverse law.
The base is the original v5.59 datum: no strictification of G,
object-equivalence replacement, or new axiom is introduced.
-/

namespace Generic

universe uB vB wB uC vC wC

/-- A native incoherent datum supplemented with both original
unit/counit-centered interchangers and both corresponding swallowtail laws.
The word "coherent" here refers precisely to these two typed KuuOS
swallowtail interfaces. -/
structure CoherentBiadjunctionDatum
    (B : Type uB) [Bicategory.{wB, vB} B]
    (C : Type uC) [Bicategory.{wC, vC} C] where
  datum : IncoherentBiadjunctionDatum B C
  forwardInterchanger :
    KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum.ForwardSwallowtailInterchanger datum
  reverseInterchanger :
    KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum.ReverseSwallowtailInterchanger datum
  forward_swallowtail :
    KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum.ForwardSwallowtailPredicate datum forwardInterchanger
  reverse_swallowtail :
    KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum.ReverseSwallowtailPredicate datum reverseInterchanger

end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The native F/G/eta/eps and original triangulators become a coherent
biadjunction by the two proved actual-lift swallowtail laws.
Both interchangers are the ones already constructed in v5.87 and
v5.96, not artificially selected to be the triangulator pastes. -/
def actualLiftCoherentBiadjunctionDatum :
    Generic.CoherentBiadjunctionDatum
      (ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ActualLiftTarget.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  datum :=
    exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  forwardInterchanger :=
    actualLiftForwardSwallowtailCanonicalIso
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  reverseInterchanger :=
    actualLiftReverseSwallowtailInterchangerOfNaturality
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
      (actualLiftReverseNaturality
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
  forward_swallowtail :=
    actualLiftForwardSwallowtail
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)
  reverse_swallowtail :=
    actualLiftReverseSwallowtail
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)

/-- Strict identity with the unchanged v5.59 datum, including all original
F/G/eta/eps choices and their native invertible triangle modifications. -/
@[simp] theorem actualLiftCoherentBiadjunctionDatum_base :
    (actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).datum =
    exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  rfl

/-- This theorem asserts existence of both original swallowtail laws for
the same unmodified actual-lift datum, not merely separate propositions
over potentially independently chosen base certificates. -/
theorem actualLiftCoherentBiadjunction_exists :
    Nonempty
      (Generic.CoherentBiadjunctionDatum
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)) :=
  ⟨actualLiftCoherentBiadjunctionDatum (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)⟩

#print axioms Generic.CoherentBiadjunctionDatum
#print axioms actualLiftCoherentBiadjunctionDatum
#print axioms actualLiftCoherentBiadjunctionDatum_base
#print axioms actualLiftCoherentBiadjunction_exists

end

end KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
