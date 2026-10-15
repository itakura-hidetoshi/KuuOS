import KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14

namespace KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientWhiteheadDataV5_10
open KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
open KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13
open KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient biequivalence certificate v5.15

v5.10 gives the ambient Whitehead-style certificate for the exact-universal
realization.  v5.12 constructs a genuine ambient quasi-inverse pseudofunctor,
v5.13 supplies the ambient counit StrongTrans, and v5.14 supplies the source
unit StrongTrans despite the change of source labels.

This file packages those four already-validated objects into one explicit
ambient biequivalence certificate, in direct analogy with the object-labelled
v4.89 certificate.

The structure records a forward pseudofunctor with local hom equivalences and
ambient object coverage, an explicit quasi-inverse pseudofunctor, and native
StrongTrans unit/counit.  It still does not assert a stronger tricategorical
adjoint-biequivalence package with separately formalized triangle
modifications.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-- Ambient analogue of the v4.89 object-labelled certificate. -/
structure ExactUniversalAmbientBiequivalenceCertificate where
  whitehead :
    WhiteheadBiequivalenceData
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A)
  quasiInverse :
    Pseudofunctor
      (DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A)
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
  unit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A))
      (Pseudofunctor.comp whitehead.forward quasiInverse)
  counit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp quasiInverse whitehead.forward)
      (Pseudofunctor.id
        (DependentOriginationCompletion2.{u, v, uH, uH, vH}
          (W := W) A))

/-- Complete ambient exact-universal biequivalence certificate assembled from
v5.10-v5.14. -/
noncomputable def exactUniversalAmbientBiequivalenceCertificate :
    ExactUniversalAmbientBiequivalenceCertificate (W := W) A where
  whitehead :=
    exactUniversalAmbientCanonicalWhiteheadBiequivalenceData
      (W := W) A
  quasiInverse :=
    exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A
  unit := by
    change
      Pseudofunctor.StrongTrans
        (Pseudofunctor.id (Source (W := W) A))
        (exactUniversalSourceAmbientRoundtrip (W := W) A)
    exact exactUniversalSourceAmbientRoundtripUnit (W := W) A
  counit := by
    change
      Pseudofunctor.StrongTrans
        (exactUniversalAmbientRoundtrip (W := W) A)
        (Pseudofunctor.id (Ambient (W := W) A))
    exact exactUniversalAmbientRoundtripCounit (W := W) A

/-- The forward pseudofunctor is exactly the strict exact-universal
realization. -/
@[simp] theorem exactUniversalAmbientBiequivalenceCertificate_forward :
    (exactUniversalAmbientBiequivalenceCertificate
      (W := W) A).whitehead.forward =
      (exactUniversalRealization (W := W) A).toPseudofunctor := by
  exact
    exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_forward
      (W := W) A

/-- The explicit quasi-inverse is the canonical ambient section from v5.12. -/
@[simp] theorem exactUniversalAmbientBiequivalenceCertificate_quasiInverse :
    (exactUniversalAmbientBiequivalenceCertificate
      (W := W) A).quasiInverse =
      exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A := by
  rfl

/-- The certificate carries exactly the v5.14 source unit. -/
theorem exactUniversalAmbientBiequivalenceCertificate_unit :
    (exactUniversalAmbientBiequivalenceCertificate
      (W := W) A).unit =
      exactUniversalSourceAmbientRoundtripUnit
        (W := W) A := by
  rfl

/-- The certificate carries exactly the v5.13 ambient counit. -/
theorem exactUniversalAmbientBiequivalenceCertificate_counit :
    (exactUniversalAmbientBiequivalenceCertificate
      (W := W) A).counit =
      exactUniversalAmbientRoundtripCounit
        (W := W) A := by
  rfl

/-- Local hom equivalence remains the v5.10 exact-universal ambient one. -/
theorem exactUniversalAmbientBiequivalenceCertificate_homEquiv
    (X Y : Source (W := W) A) :
    (exactUniversalAmbientBiequivalenceCertificate
      (W := W) A).whitehead.homEquiv X Y =
      exactUniversalAmbientHomEquivalence (W := W) A X Y := by
  exact
    exactUniversalAmbientCanonicalWhiteheadBiequivalenceData_homEquiv
      (W := W) A X Y

/-- Ambient object coverage is inherited unchanged from the v5.10 Whitehead
datum. -/
theorem exactUniversalAmbientBiequivalenceCertificate_object_essentially_surjective
    (Z : Ambient (W := W) A) :
    ∃ X : Source (W := W) A,
      Nonempty (Bicategory.Equivalence X.carrier Z) := by
  exact
    exactUniversalAmbientCanonicalWhitehead_object_essentially_surjective
      (W := W) A Z

/-! ## Regression checks -/

#print axioms ExactUniversalAmbientBiequivalenceCertificate
#print axioms exactUniversalAmbientBiequivalenceCertificate
#print axioms exactUniversalAmbientBiequivalenceCertificate_forward
#print axioms exactUniversalAmbientBiequivalenceCertificate_quasiInverse
#print axioms exactUniversalAmbientBiequivalenceCertificate_unit
#print axioms exactUniversalAmbientBiequivalenceCertificate_counit
#print axioms exactUniversalAmbientBiequivalenceCertificate_homEquiv
#print axioms exactUniversalAmbientBiequivalenceCertificate_object_essentially_surjective

end

end KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15
