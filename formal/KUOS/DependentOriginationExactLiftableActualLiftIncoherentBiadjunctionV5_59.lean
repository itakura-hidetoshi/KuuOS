import KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58

namespace KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29
open KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
open KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.Generic

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift incoherent biadjunction datum v5.59

v5.57 already packages the same Whitehead datum, forward pseudofunctor F,
quasi-inverse pseudofunctor G, source unit eta, target counit eps, both actual
triangle StrongTrans values, and both global invertible modifications.

v5.58 re-exposes the two triangle modifications as native invertible 2-cells
in Mathlib's bicategories of pseudofunctors.

This file joins those two interfaces.  The generic structure below contains

* one Whitehead/unit/counit base;
* one native triangulator for F;
* one native triangulator for G.

The word "incoherent" is deliberate: no swallowtail relation between the two
triangulators is included.  Thus this is a typed input for the next
higher-coherence theorem, not a claim that a coherent biadjoint
biequivalence has already been constructed.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Unit/counit data and the two native triangle contractions, without a
swallowtail law relating the contractions. -/
structure IncoherentBiadjunctionDatum
    (B : Type uB) [Bicategory.{wB, vB} B]
    (C : Type uC) [Bicategory.{wC, vC} C] where
  base : WhiteheadUnitCounitCertificate B C
  triangulators :
    FunctorBicategoryTriangulatorPair
      base.whitehead.forward
      base.quasiInverse

namespace IncoherentBiadjunctionDatum

/-- Every v5.31-level triangle certificate canonically determines the
corresponding incoherent biadjunction datum.  No data are re-chosen. -/
def ofTriangleCertificate
    (P : WhiteheadTriangleRepresentativeCertificate B C) :
    IncoherentBiadjunctionDatum B C where
  base := P.base
  triangulators :=
    { forward :=
        { triangle := P.forwardTriangleRepresentative
          contraction := P.forwardTriangleModification }
      reverse :=
        { triangle := P.quasiInverseTriangleRepresentative
          contraction := P.quasiInverseTriangleModification } }

@[simp] theorem ofTriangleCertificate_base
    (P : WhiteheadTriangleRepresentativeCertificate B C) :
    (ofTriangleCertificate P).base = P.base :=
  rfl

@[simp] theorem ofTriangleCertificate_forward_triangle
    (P : WhiteheadTriangleRepresentativeCertificate B C) :
    (ofTriangleCertificate P).triangulators.forward.triangle =
      P.forwardTriangleRepresentative :=
  rfl

@[simp] theorem ofTriangleCertificate_forward_contraction
    (P : WhiteheadTriangleRepresentativeCertificate B C) :
    (ofTriangleCertificate P).triangulators.forward.contraction =
      P.forwardTriangleModification :=
  rfl

@[simp] theorem ofTriangleCertificate_reverse_triangle
    (P : WhiteheadTriangleRepresentativeCertificate B C) :
    (ofTriangleCertificate P).triangulators.reverse.triangle =
      P.quasiInverseTriangleRepresentative :=
  rfl

@[simp] theorem ofTriangleCertificate_reverse_contraction
    (P : WhiteheadTriangleRepresentativeCertificate B C) :
    (ofTriangleCertificate P).triangulators.reverse.contraction =
      P.quasiInverseTriangleModification :=
  rfl

end IncoherentBiadjunctionDatum

end Generic

open Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The v5.57 actual-lift certificate viewed as an incoherent biadjunction
datum.  This is a pure packaging operation. -/
def exactLiftableActualLiftIncoherentBiadjunctionDatum :
    IncoherentBiadjunctionDatum
      (ActualLiftSource (W := W) A WorldLabel PresentationLabel)
      (ActualLiftTarget (W := W) A WorldLabel PresentationLabel) :=
  IncoherentBiadjunctionDatum.ofTriangleCertificate
    (exactLiftableActualLiftCoherentBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-! ## The base is exactly the original F/G/eta/eps package -/

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_base :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base =
      exactLiftableActualLiftUnitCounitCertificate
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_forward :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.whitehead.forward =
      actualLiftForwardPseudofunctor
        (W := W) A WorldLabel PresentationLabel :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_quasiInverse :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.quasiInverse =
      actualLiftQuasiInversePseudofunctor
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_unit :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.unit =
      actualLiftSourceRoundtripUnit
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_counit :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.counit =
      actualLiftTargetRoundtripCounit
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

/-! ## The triangulators are exactly the v5.58 pair -/

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_triangulators :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).triangulators =
      actualLiftTriangulatorPair
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_forward_triangle :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).triangulators.forward.triangle =
      actualLiftForwardTriangle
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_forward_contraction :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).triangulators.forward.contraction =
      actualLiftForwardTriangleModificationIso
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_reverse_triangle :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).triangulators.reverse.triangle =
      actualLiftQuasiInverseTriangle
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem exactLiftableActualLiftIncoherentBiadjunctionDatum_reverse_contraction :
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).triangulators.reverse.contraction =
      actualLiftQuasiInverseTriangleModificationIso
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

/-!
## Boundary after v5.59

The same actual-lift F, G, eta, eps and the two native invertible triangle
contractions are now one typed datum.  No component has been reconstructed,
and the v5.57/v5.58 whole-record identities are preserved by rfl.

The remaining higher-coherence obstruction is now isolated: a coherent
biadjunction would require an additional law relating these two stored
triangulators.  That law is intentionally absent here and is the next
formal target.
-/

#print axioms Generic.IncoherentBiadjunctionDatum
#print axioms Generic.IncoherentBiadjunctionDatum.ofTriangleCertificate
#print axioms exactLiftableActualLiftIncoherentBiadjunctionDatum
#print axioms exactLiftableActualLiftIncoherentBiadjunctionDatum_base
#print axioms exactLiftableActualLiftIncoherentBiadjunctionDatum_triangulators
#print axioms exactLiftableActualLiftIncoherentBiadjunctionDatum_forward_triangle
#print axioms exactLiftableActualLiftIncoherentBiadjunctionDatum_reverse_triangle

end

end KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
