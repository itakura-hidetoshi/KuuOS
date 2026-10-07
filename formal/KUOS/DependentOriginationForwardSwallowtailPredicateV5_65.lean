import KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64

namespace KUOS.DependentOriginationForwardSwallowtailPredicateV5_65

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Forward swallowtail predicate v5.65

v5.64 constructs, for every incoherent biadjunction datum, an invertible
modification comparing the two horizontally whiskered triangle
representatives on the source roundtrip.

The coherent forward swallowtail law is not merely the assertion that this
comparison is an identity.  In the standard Gray-categorical formulation, the
unit is horizontally composed with itself in two different orders.  The
resulting interchanger, together with the required associator/unitor and
counit whiskering corrections, gives a canonical comparison between the two
full unit-followed-by-triangle paths.  The swallowtail equation compares that
canonical interchanger paste with the paste of the two triangulators; the
resulting defect must be the identity modification of the unit.

At the current KuuOS boundary the generic StrongTrans pre/postcomposition
machinery and the v5.64 triangulator paste are available, while the canonical
unit-centered interchanger paste (including its structural correction cells)
has not yet been constructed as a generic KuuOS operation.  This file therefore isolates the exact typed equation without
postulating that missing cell:

* the two boundary StrongTrans values are fixed by the stored unit and the
  two v5.64 source-roundtrip triangle representatives;
* a candidate unit-centered interchanger must have exactly that boundary;
* the forward swallowtail predicate says that this candidate is exactly the
  left whisker of the v5.64 triangulator paste.

Because all cells involved are invertible, this equality is equivalent to the
usual normalized form

  interchanger⁻¹ ; triangulator-paste = identity.

No swallowtail proof and no canonical interchanger construction is claimed in
this file.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The unit followed by the forward triangle representative transported to
the source roundtrip.  This is one side of the forward swallowtail boundary. -/
def forwardSwallowtailLeft :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id B)
      (sourceRoundtrip D) :=
  Pseudofunctor.StrongTrans.vcomp
    D.base.unit
    (sourceForwardTriangulator D).triangle

/-- The unit followed by the reverse triangle representative transported to
the source roundtrip.  This is the other side of the forward swallowtail
boundary. -/
def forwardSwallowtailRight :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id B)
      (sourceRoundtrip D) :=
  Pseudofunctor.StrongTrans.vcomp
    D.base.unit
    (sourceReverseTriangulator D).triangle

/-! The modification category is a scoped Mathlib instance.  Keep the native
hom category explicit at this generic universe boundary, following the same
rule used in v5.61--v5.64. -/

local instance forwardSwallowtailHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (sourceRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B)
    (G := sourceRoundtrip D)

/-- The exact type required of the unit-centered interchanger paste in the forward
swallowtail equation.

The construction of the canonical inhabitant from the pseudonaturality of the
stored unit is deliberately left to the next step. -/
abbrev ForwardSwallowtailInterchanger :=
  @CategoryTheory.Iso
    (Pseudofunctor.StrongTrans
      (Pseudofunctor.id B)
      (sourceRoundtrip D))
    (Pseudofunctor.StrongTrans.homCategory
      (B := B) (C := B)
      (F := Pseudofunctor.id B)
      (G := sourceRoundtrip D))
    (forwardSwallowtailLeft D)
    (forwardSwallowtailRight D)

/-- Whisker the v5.64 source-roundtrip triangulator paste on the left by the
stored unit.  This is the triangulator side of the forward swallowtail law. -/
def forwardTriangulatorPaste :
    ForwardSwallowtailInterchanger D :=
  Bicategory.whiskerLeftIso
    D.base.unit
    (sourceHorizontalPaste D)

/-- The forward swallowtail equation as an exact typed proposition.

Our interchanger is oriented from the forward-whiskered triangle path to the
reverse-whiskered triangle path.  In this orientation the conventional
`Sigma⁻¹ ; paste = id` law is equivalently written `Sigma = paste`. -/
def ForwardSwallowtailPredicate
    (Sigma : ForwardSwallowtailInterchanger D) : Prop :=
  Sigma = forwardTriangulatorPaste D

@[simp] theorem forwardTriangulatorPaste_hom :
    (forwardTriangulatorPaste D).hom =
      (Bicategory.whiskerLeftIso
        D.base.unit
        (sourceHorizontalPaste D)).hom :=
  rfl

@[simp] theorem forwardSwallowtailPredicate_iff
    (Sigma : ForwardSwallowtailInterchanger D) :
    ForwardSwallowtailPredicate D Sigma ↔
      Sigma = forwardTriangulatorPaste D :=
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
forward swallowtail interface. -/
abbrev actualLiftForwardSwallowtailDatum :=
  exactLiftableActualLiftIncoherentBiadjunctionDatum
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

/-- Exact type of a candidate actual-lift unit-centered interchanger paste. -/
abbrev ActualLiftForwardSwallowtailInterchanger :=
  Generic.IncoherentBiadjunctionDatum.ForwardSwallowtailInterchanger
    (actualLiftForwardSwallowtailDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- Forward swallowtail predicate specialized to the unchanged actual-lift
F, G, eta, eps and the v5.64 source horizontal paste. -/
def actualLiftForwardSwallowtailPredicate
    (Sigma :
      ActualLiftForwardSwallowtailInterchanger
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) : Prop :=
  Generic.IncoherentBiadjunctionDatum.ForwardSwallowtailPredicate
    (actualLiftForwardSwallowtailDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    Sigma

/-!
## Boundary after v5.65

The forward swallowtail is now a genuine Lean proposition with fixed source,
target and modification universe.

What remains is mathematical rather than terminological:

1. construct the canonical unit-centered interchanger paste from the stored unit
   pseudonaturality, retaining the eta/eta interchanger, all pseudofunctor
   mapId/mapComp cells, the required counit whiskering, and
   associator/unitor corrections;
2. specialize it to the actual-lift datum;
3. prove that this canonical interchanger equals
   `forwardTriangulatorPaste`.

Until step 3 is complete, KuuOS still has an incoherent biadjunction datum plus
a typed swallowtail predicate, not a coherent biadjunction.
-/

#print axioms Generic.IncoherentBiadjunctionDatum.forwardSwallowtailLeft
#print axioms Generic.IncoherentBiadjunctionDatum.forwardSwallowtailRight
#print axioms Generic.IncoherentBiadjunctionDatum.forwardTriangulatorPaste
#print axioms Generic.IncoherentBiadjunctionDatum.ForwardSwallowtailPredicate
#print axioms actualLiftForwardSwallowtailPredicate

end

end KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
