import KUOS.DependentOriginationClassificationTriangleCoherenceV5_30
import Mathlib

namespace KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationClassificationWhiteheadBiequivalenceV5_27
open KUOS.DependentOriginationClassificationCanonicalSectionV5_28
open KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29
open KUOS.DependentOriginationClassificationTriangleCoherenceV5_30

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Coherent classification biequivalence certificate v5.31

v5.27--v5.30 establish, in separate theorem units:

* local equivalence on every classification hom category;
* essential surjectivity on localized classification objects;
* an explicit label-preserving quasi-inverse pseudofunctor;
* a source unit and target counit StrongTrans;
* coherent forward and quasi-inverse triangle representatives;
* native invertible modifications from those representatives to identity.

This file does not strengthen any of those claims.  It packages them into one
universe-explicit certificate using exactly the native Mathlib structures that
already validated the individual theorem units.

The generic package intentionally stores triangle *representatives* and their
invertible StrongTrans isomorphisms to identity.  This is the same strength as
v5.16/v5.30 and does not manufacture an adjoint-biequivalence or tricategory
object that is absent from the current Mathlib API.
-/

universe uB uC vB vC wB wC
universe u v uH vH uW uP

/-! ## Generic package at the currently available Mathlib coherence level -/

/-- Whitehead/unit/counit data together with coherent triangle representatives
and native invertible StrongTrans isomorphisms to identity. -/
structure WhiteheadTriangleRepresentativeCertificate
    (B : Type uB) [Bicategory.{wB, vB} B]
    (C : Type uC) [Bicategory.{wC, vC} C] where
  base : WhiteheadUnitCounitCertificate B C
  forwardTriangleRepresentative :
    Pseudofunctor.StrongTrans
      base.whitehead.forward
      base.whitehead.forward
  forwardTriangleModification :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        base.whitehead.forward
        base.whitehead.forward)
      (Pseudofunctor.StrongTrans.homCategory
        (F := base.whitehead.forward)
        (G := base.whitehead.forward))
      forwardTriangleRepresentative
      (Pseudofunctor.StrongTrans.id base.whitehead.forward)
  quasiInverseTriangleRepresentative :
    Pseudofunctor.StrongTrans
      base.quasiInverse
      base.quasiInverse
  quasiInverseTriangleModification :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        base.quasiInverse
        base.quasiInverse)
      (Pseudofunctor.StrongTrans.homCategory
        (F := base.quasiInverse)
        (G := base.quasiInverse))
      quasiInverseTriangleRepresentative
      (Pseudofunctor.StrongTrans.id base.quasiInverse)

/-! ## Classification specialization -/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

abbrev ClassificationSource
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  ExactUniversalClassificationObject
    (W := W) A WorldLabel PresentationLabel

abbrev ClassificationTarget
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  LocalizedClassificationObject
    (W := W) A WorldLabel PresentationLabel

/-- The full current labelled-classification biequivalence/coherence package.

Its mathematical content is entirely inherited from v5.27--v5.30. -/
noncomputable def exactUniversalClassificationCoherentBiequivalenceCertificate
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    WhiteheadTriangleRepresentativeCertificate
      (ClassificationSource
        (W := W) A WorldLabel PresentationLabel)
      (ClassificationTarget
        (W := W) A WorldLabel PresentationLabel) where
  base :=
    exactUniversalClassificationBiequivalenceCertificate
      (W := W) A
  forwardTriangleRepresentative := by
    change
      Pseudofunctor.StrongTrans
        (exactUniversalClassificationRealization
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).toPseudofunctor
        (exactUniversalClassificationRealization
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).toPseudofunctor
    exact
      exactUniversalClassificationForwardTriangleStrongTrans
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
  forwardTriangleModification := by
    change
      @CategoryTheory.Iso
        (Pseudofunctor.StrongTrans
          (exactUniversalClassificationRealization
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).toPseudofunctor
          (exactUniversalClassificationRealization
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).toPseudofunctor)
        (Pseudofunctor.StrongTrans.homCategory
          (F :=
            (exactUniversalClassificationRealization
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel)).toPseudofunctor)
          (G :=
            (exactUniversalClassificationRealization
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel)).toPseudofunctor))
        (exactUniversalClassificationForwardTriangleStrongTrans
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (Pseudofunctor.StrongTrans.id
          (exactUniversalClassificationRealization
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).toPseudofunctor)
    exact
      exactUniversalClassificationForwardTriangleModification
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
  quasiInverseTriangleRepresentative := by
    change
      Pseudofunctor.StrongTrans
        (exactUniversalClassificationCanonicalSection
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (exactUniversalClassificationCanonicalSection
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
    exact
      exactUniversalClassificationQuasiInverseTriangleStrongTrans
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
  quasiInverseTriangleModification := by
    change
      @CategoryTheory.Iso
        (Pseudofunctor.StrongTrans
          (exactUniversalClassificationCanonicalSection
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel))
          (exactUniversalClassificationCanonicalSection
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
        (Pseudofunctor.StrongTrans.homCategory
          (F :=
            exactUniversalClassificationCanonicalSection
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel))
          (G :=
            exactUniversalClassificationCanonicalSection
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel)))
        (exactUniversalClassificationQuasiInverseTriangleStrongTrans
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (Pseudofunctor.StrongTrans.id
          (exactUniversalClassificationCanonicalSection
            (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
    exact
      exactUniversalClassificationQuasiInverseTriangleModification
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)

/-! ## Projection theorems -/

@[simp] theorem
    exactUniversalClassificationCoherentBiequivalenceCertificate_base
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationCoherentBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base =
      exactUniversalClassificationBiequivalenceCertificate
        (W := W) A :=
  rfl

@[simp] theorem
    exactUniversalClassificationCoherentBiequivalenceCertificate_forward
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationCoherentBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.whitehead.forward =
      (exactUniversalClassificationRealization
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).toPseudofunctor :=
  rfl

@[simp] theorem
    exactUniversalClassificationCoherentBiequivalenceCertificate_quasiInverse
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationCoherentBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).base.quasiInverse =
      exactUniversalClassificationCanonicalSection
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

theorem
    exactUniversalClassificationCoherentBiequivalenceCertificate_forwardTriangle
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationCoherentBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).forwardTriangleRepresentative =
      exactUniversalClassificationForwardTriangleStrongTrans
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

theorem
    exactUniversalClassificationCoherentBiequivalenceCertificate_quasiInverseTriangle
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationCoherentBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseTriangleRepresentative =
      exactUniversalClassificationQuasiInverseTriangleStrongTrans
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

/-! ## Link the packaged representatives back to the actual triangle composites -/

/-- The actual forward triangle component is the component stored by the
coherent certificate. -/
theorem exactUniversalClassificationActualForwardTriangle_matches_certificate
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ClassificationSource
        (W := W) A WorldLabel PresentationLabel) :
    exactUniversalClassificationForwardTriangleApp
        (W := W) A X =
      (exactUniversalClassificationCoherentBiequivalenceCertificate
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).forwardTriangleRepresentative.app X := by
  change
    exactUniversalClassificationForwardTriangleApp
        (W := W) A X =
      (exactUniversalClassificationForwardTriangleStrongTrans
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app X
  exact
    exactUniversalClassificationForwardTriangleApp_eq_representative
      (W := W) A X

/-- The actual quasi-inverse triangle component has the canonical v5.30
comparison to the component stored by the coherent certificate. -/
noncomputable def
    exactUniversalClassificationActualQuasiInverseTriangle_certificateIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z :
      ClassificationTarget
        (W := W) A WorldLabel PresentationLabel) :
    exactUniversalClassificationQuasiInverseTriangleApp
        (W := W) A Z ≅
      (exactUniversalClassificationCoherentBiequivalenceCertificate
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).quasiInverseTriangleRepresentative.app Z := by
  change
    exactUniversalClassificationQuasiInverseTriangleApp
        (W := W) A Z ≅
      (exactUniversalClassificationQuasiInverseTriangleStrongTrans
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app Z
  exact
    exactUniversalClassificationQuasiInverseTriangleRepresentativeIso
      (W := W) A Z

/-!
## Boundary after v5.31

The full labelled classification theorem is now available through one formal
certificate containing:

* Whitehead local equivalence and object coverage;
* explicit label-preserving quasi-inverse;
* source unit and target counit;
* coherent forward/quasi-inverse triangle representatives;
* native invertible modifications of both representatives to identity.

This is the strongest package currently justified by the existing Mathlib
bicategory/StrongTrans API used by the repository.  No stronger tricategorical
structure is asserted, and no statement about arbitrary weak semantic or
merely exact-liftable raw systems is added.  The v5.19 alignment boundary
remains unchanged.
-/

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ClassificationSource
        (W := W) A WorldLabel PresentationLabel)
    (Z :
      ClassificationTarget
        (W := W) A WorldLabel PresentationLabel)

example :
    WhiteheadTriangleRepresentativeCertificate
      (ClassificationSource
        (W := W) A WorldLabel PresentationLabel)
      (ClassificationTarget
        (W := W) A WorldLabel PresentationLabel) :=
  exactUniversalClassificationCoherentBiequivalenceCertificate
    (W := W) A

example :
    exactUniversalClassificationForwardTriangleApp
        (W := W) A X =
      (exactUniversalClassificationCoherentBiequivalenceCertificate
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).forwardTriangleRepresentative.app X :=
  exactUniversalClassificationActualForwardTriangle_matches_certificate
    (W := W) A X

example :
    Nonempty
      (exactUniversalClassificationQuasiInverseTriangleApp
          (W := W) A Z ≅
        (exactUniversalClassificationCoherentBiequivalenceCertificate
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).quasiInverseTriangleRepresentative.app Z) :=
  ⟨exactUniversalClassificationActualQuasiInverseTriangle_certificateIso
    (W := W) A Z⟩

end Regression

#print axioms WhiteheadTriangleRepresentativeCertificate
#print axioms exactUniversalClassificationCoherentBiequivalenceCertificate
#print axioms exactUniversalClassificationActualForwardTriangle_matches_certificate
#print axioms exactUniversalClassificationActualQuasiInverseTriangle_certificateIso

end

end KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31
