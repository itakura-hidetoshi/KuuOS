import KUOS.DependentOriginationForwardSwallowtailPredicateV5_65

namespace KUOS.DependentOriginationReverseSwallowtailPredicateV5_66

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Reverse swallowtail predicate v5.66

v5.65 fixes the source/unit swallowtail as an exact equality between a
normalized unit-centered interchanger paste and the v5.64 source triangulator
paste.

This file records the target/counit counterpart.  The two v5.64 target
triangulators are followed by the stored counit

  eps : G ; F => id_C,

giving two StrongTrans values from the target roundtrip G ; F to id_C.
Right-whiskering the v5.64 target horizontal paste by eps then gives the
triangulator side of the reverse swallowtail law.

As in v5.65, the canonical counit-centered interchanger paste itself is not
postulated and is not reconstructed pointwise.  We expose only its exact type
and the proposition that the canonical inhabitant, once constructed, must
equal the stored triangulator paste.

This remains an interface theorem: no coherent biadjunction is claimed.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The target-side forward triangle representative followed by the counit. -/
def reverseSwallowtailLeft :
    Pseudofunctor.StrongTrans
      (targetRoundtrip D)
      (Pseudofunctor.id C) :=
  Pseudofunctor.StrongTrans.vcomp
    (targetForwardTriangulator D).triangle
    D.base.counit

/-- The target-side reverse triangle representative followed by the counit. -/
def reverseSwallowtailRight :
    Pseudofunctor.StrongTrans
      (targetRoundtrip D)
      (Pseudofunctor.id C) :=
  Pseudofunctor.StrongTrans.vcomp
    (targetReverseTriangulator D).triangle
    D.base.counit

/-! As in v5.64 and v5.65, keep the native StrongTrans hom category explicit
at the generic universe boundary. -/

local instance reverseSwallowtailHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip D)
        (Pseudofunctor.id C)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := C) (C := C)
    (F := targetRoundtrip D)
    (G := Pseudofunctor.id C)

/-- Exact type of the normalized counit-centered interchanger paste required
by the reverse swallowtail equation. -/
abbrev ReverseSwallowtailInterchanger :=
  @CategoryTheory.Iso
    (Pseudofunctor.StrongTrans
      (targetRoundtrip D)
      (Pseudofunctor.id C))
    (Pseudofunctor.StrongTrans.homCategory
      (B := C) (C := C)
      (F := targetRoundtrip D)
      (G := Pseudofunctor.id C))
    (reverseSwallowtailLeft D)
    (reverseSwallowtailRight D)

/-- Right-whisker the v5.64 target horizontal triangulator paste by the stored
counit. -/
def reverseTriangulatorPaste :
    ReverseSwallowtailInterchanger D :=
  Bicategory.whiskerRightIso
    (targetHorizontalPaste D)
    D.base.counit

/-- The reverse swallowtail equation as an exact typed proposition.

The interchanger is oriented in the same direction as the right-whiskered
v5.64 target paste.  Thus the usual normalized
`interchanger⁻¹ ; triangulator-paste = identity` law is represented by
plain equality of the two invertible modifications. -/
def ReverseSwallowtailPredicate
    (Sigma : ReverseSwallowtailInterchanger D) : Prop :=
  Sigma = reverseTriangulatorPaste D

@[simp] theorem reverseTriangulatorPaste_hom :
    (reverseTriangulatorPaste D).hom =
      (Bicategory.whiskerRightIso
        (targetHorizontalPaste D)
        D.base.counit).hom :=
  rfl

@[simp] theorem reverseSwallowtailPredicate_iff
    (Sigma : ReverseSwallowtailInterchanger D) :
    ReverseSwallowtailPredicate D Sigma ↔
      Sigma = reverseTriangulatorPaste D :=
  Iff.rfl

end IncoherentBiadjunctionDatum

end Generic

open Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The unchanged actual-lift incoherent biadjunction datum used by the
reverse swallowtail interface. -/
abbrev actualLiftReverseSwallowtailDatum :=
  exactLiftableActualLiftIncoherentBiadjunctionDatum
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

/-- Exact type of a candidate actual-lift normalized counit-centered
interchanger paste. -/
abbrev ActualLiftReverseSwallowtailInterchanger :=
  Generic.IncoherentBiadjunctionDatum.ReverseSwallowtailInterchanger
    (actualLiftReverseSwallowtailDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- Reverse swallowtail predicate specialized to the unchanged actual-lift
F, G, eta, eps and the v5.64 target horizontal paste. -/
def actualLiftReverseSwallowtailPredicate
    (Sigma :
      ActualLiftReverseSwallowtailInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) : Prop :=
  Generic.IncoherentBiadjunctionDatum.ReverseSwallowtailPredicate
    (actualLiftReverseSwallowtailDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    Sigma

/-!
## Boundary after v5.66

Both swallowtail laws now exist as exact typed propositions:

* v5.65: source/unit predicate;
* v5.66: target/counit predicate.

Neither canonical interchanger paste has been assumed or proved to satisfy its
predicate.  The next substantive step is to construct the actual-lift
unit-centered interchanger from the already stored eta naturality and the
native pseudofunctor mapComp/associator cells, then prove modification
naturality.

For the standard Gray-categorical coherence theorem, one swallowtail equation
can determine the other after the appropriate coherence hypotheses are in
place.  KuuOS does not use that theorem as a shortcut here: both typed
boundaries are retained explicitly until their assumptions have themselves
been formalized.
-/

#print axioms Generic.IncoherentBiadjunctionDatum.reverseSwallowtailLeft
#print axioms Generic.IncoherentBiadjunctionDatum.reverseSwallowtailRight
#print axioms Generic.IncoherentBiadjunctionDatum.reverseTriangulatorPaste
#print axioms Generic.IncoherentBiadjunctionDatum.ReverseSwallowtailPredicate
#print axioms actualLiftReverseSwallowtailPredicate

end

end KUOS.DependentOriginationReverseSwallowtailPredicateV5_66
