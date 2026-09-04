import KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80
import KUOS.DependentOriginationScaledColimitsPresentabilityV1_45

namespace KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledColimitsPresentabilityV1_45
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80
open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.GeneratedScaledAnodynePresentationEquivalence
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79

universe u

/-!
# Generated-presentation quotient invariant v1.81

Version v1.80 proved that the literal generator list is not the invariant
object.  If two generator properties `E` and `F` mutually generate each
other's orthogonal left closures,

```text
E <= F.rlp.llp
F <= E.rlp.llp,
```

then both the generated left classes and the right lifting classes agree.
Consequently endpoint Leibniz stability, endpoint lifting, fibrancy, and the
weak-factorization-system property are all invariant under that relation.

This file turns that theorem collection into an actual quotient object.
Presentations are identified precisely by mutual generation.  The quotient
therefore remembers the generated lifting theory while forgetting the chosen
list of generating cells.

The main outputs are:

* a `Setoid` of scaled-anodyne presentations;
* the quotient type of generated presentations;
* well-defined quotient-level generated left and right classes;
* quotient-level endpoint generator membership, stability, lifting,
  fibrancy, and WFS predicates;
* the standard A/B/C quotient point carrying the v1.77 endpoint theorem;
* the canonical KuuOS quotient point carrying the unconditional v1.45 WFS;
* exact transfer theorems showing that equality of those quotient points
  combines the two packages of structure.

The final equality is deliberately not asserted.  A positive v1.79 comparison
certificate is exposed only as a sufficient witness for it.  Thus the
presentation-independent object exists unconditionally, while the stronger
standard-vs-canonical identification remains an honest geometric theorem.
-/

/-! ## The setoid of generated presentations -/

/-- Literal scaled-anodyne generator presentations. -/
abbrev ScaledAnodynePresentation :=
  MorphismProperty (ScaledSSet.{u})

/-- Two presentations are related exactly when they mutually generate each
other's orthogonally generated left class. -/
def generatedPresentationSetoid : Setoid ScaledAnodynePresentation.{u} where
  r E F := GeneratedScaledAnodynePresentationEquivalence E F
  iseqv := by
    constructor
    · intro E
      exact GeneratedScaledAnodynePresentationEquivalence.refl E
    · intro E F h
      exact h.symm
    · intro E F G hEF hFG
      exact hEF.trans hFG

/-- The presentation-independent carrier: generator lists modulo mutual
orthogonal generation. -/
def GeneratedScaledAnodynePresentation : Type _ :=
  Quotient (generatedPresentationSetoid.{u})

/-- Canonical projection of a literal presentation to its generated theory. -/
def presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    GeneratedScaledAnodynePresentation.{u} :=
  Quotient.mk (generatedPresentationSetoid.{u}) E

/-- Equality in the quotient is exactly v1.80 mutual generation. -/
theorem presentationClass_eq_iff
    (E F : ScaledAnodynePresentation.{u}) :
    presentationClass E = presentationClass F ↔
      GeneratedScaledAnodynePresentationEquivalence E F := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- Equivalently, two representatives define the same quotient point exactly
when their generated left classes agree. -/
theorem presentationClass_eq_iff_generatedAnodyne_eq
    (E F : ScaledAnodynePresentation.{u}) :
    presentationClass E = presentationClass F ↔
      externalGeneratedScaledAnodyne E =
        externalGeneratedScaledAnodyne F := by
  rw [presentationClass_eq_iff]
  exact GeneratedScaledAnodynePresentationEquivalence.iff_generatedAnodyne_eq

/-! ## Generated left and right classes descend to the quotient -/

/-- The generated left class is a genuine function of the quotient
presentation, not of a representative. -/
def generatedAnodyneClass :
    GeneratedScaledAnodynePresentation.{u} →
      MorphismProperty (ScaledSSet.{u}) :=
  Quotient.lift
    externalGeneratedScaledAnodyne
    (by
      intro E F h
      exact h.generatedAnodyne_eq)

@[simp]
theorem generatedAnodyneClass_presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    generatedAnodyneClass (presentationClass E) =
      externalGeneratedScaledAnodyne E :=
  rfl

/-- The right lifting class descends independently. -/
def generatedFibrationClass :
    GeneratedScaledAnodynePresentation.{u} →
      MorphismProperty (ScaledSSet.{u}) :=
  Quotient.lift
    externalGeneratedScaledFibration
    (by
      intro E F h
      exact h.generatedFibration_eq)

@[simp]
theorem generatedFibrationClass_presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    generatedFibrationClass (presentationClass E) =
      externalGeneratedScaledFibration E :=
  rfl

/-! ## Endpoint and WFS predicates descend as quotient invariants -/

/-- Quotient-level membership of the whole standard type-(A) endpoint Leibniz
family in the generated left class. -/
def typeAEndpointGeneratorsGenerated :
    GeneratedScaledAnodynePresentation.{u} → Prop :=
  Quotient.lift
    (fun E => TypeAEndpointLeibnizGeneratorsGeneratedBy E)
    (by
      intro E F h
      exact propext h.typeAEndpointLeibnizGeneratorsGenerated_iff)

@[simp]
theorem typeAEndpointGeneratorsGenerated_presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    typeAEndpointGeneratorsGenerated (presentationClass E) ↔
      TypeAEndpointLeibnizGeneratorsGeneratedBy E :=
  Iff.rfl

/-- Endpoint Leibniz stability is a property of a generated-presentation
class. -/
def typeAEndpointStable :
    GeneratedScaledAnodynePresentation.{u} → Prop :=
  Quotient.lift
    (fun E => TypeAEndpointLeibnizStableForPresentation E)
    (by
      intro E F h
      exact propext h.typeAEndpointLeibnizStable_iff)

@[simp]
theorem typeAEndpointStable_presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    typeAEndpointStable (presentationClass E) ↔
      TypeAEndpointLeibnizStableForPresentation E :=
  Iff.rfl

/-- The right-lifting formulation is also quotient-level data. -/
def typeAEndpointLifting :
    GeneratedScaledAnodynePresentation.{u} → Prop :=
  Quotient.lift
    (fun E => TypeAEndpointLeibnizLiftingForPresentation E)
    (by
      intro E F h
      exact propext h.typeAEndpointLeibnizLifting_iff)

@[simp]
theorem typeAEndpointLifting_presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    typeAEndpointLifting (presentationClass E) ↔
      TypeAEndpointLeibnizLiftingForPresentation E :=
  Iff.rfl

/-- Weak-factorization-system structure depends only on the generated left and
right classes and therefore descends to the quotient. -/
def isWeakFactorizationSystem :
    GeneratedScaledAnodynePresentation.{u} → Prop :=
  Quotient.lift
    (fun E =>
      MorphismProperty.IsWeakFactorizationSystem
        (externalGeneratedScaledAnodyne E)
        (externalGeneratedScaledFibration E))
    (by
      intro E F h
      exact propext h.weakFactorizationSystem_iff)

@[simp]
theorem isWeakFactorizationSystem_presentationClass
    (E : ScaledAnodynePresentation.{u}) :
    isWeakFactorizationSystem (presentationClass E) ↔
      MorphismProperty.IsWeakFactorizationSystem
        (externalGeneratedScaledAnodyne E)
        (externalGeneratedScaledFibration E) :=
  Iff.rfl

/-- Fibrancy of a fixed scaled simplicial set is a quotient-level predicate on
presentations. -/
def isFibrant
    (X : ScaledSSet.{u}) :
    GeneratedScaledAnodynePresentation.{u} → Prop :=
  Quotient.lift
    (fun E => IsFibrantForExternalGenerators E X)
    (by
      intro E F h
      exact propext (h.fibrantForExternalGenerators_iff X))

@[simp]
theorem isFibrant_presentationClass
    (X : ScaledSSet.{u})
    (E : ScaledAnodynePresentation.{u}) :
    isFibrant X (presentationClass E) ↔
      IsFibrantForExternalGenerators E X :=
  Iff.rfl

/-! ## A compact quotient-level theory record -/

/-- All representative-independent data used in the current lifting-theoretic
spine, evaluated at one quotient presentation. -/
structure GeneratedPresentationTheory where
  generatedAnodyne : MorphismProperty (ScaledSSet.{u})
  generatedFibration : MorphismProperty (ScaledSSet.{u})
  endpointGeneratorsGenerated : Prop
  endpointStable : Prop
  endpointLifting : Prop
  isWFS : Prop

/-- Package the descended invariants into one quotient-level theory object. -/
def generatedTheory
    (P : GeneratedScaledAnodynePresentation.{u}) :
    GeneratedPresentationTheory.{u} where
  generatedAnodyne := generatedAnodyneClass P
  generatedFibration := generatedFibrationClass P
  endpointGeneratorsGenerated := typeAEndpointGeneratorsGenerated P
  endpointStable := typeAEndpointStable P
  endpointLifting := typeAEndpointLifting P
  isWFS := isWeakFactorizationSystem P

/-! ## Distinguished standard and canonical quotient points -/

/-- The presentation class represented by the explicit standard A/B/C
family. -/
def standardABCPresentation :
    GeneratedScaledAnodynePresentation.{u} :=
  presentationClass
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u}))

/-- The presentation class represented by the stronger canonical KuuOS family
of minimally-scaled horn-cylinder attachments with arbitrary simplex scaling. -/
def canonicalKuuOSPresentation :
    GeneratedScaledAnodynePresentation.{u} :=
  presentationClass
    (scaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u}))

/-- The v1.77 theorem is now literally a proposition about the standard
quotient point. -/
theorem standardABCPresentation_endpointGeneratorsGenerated :
    typeAEndpointGeneratorsGenerated standardABCPresentation := by
  change
    TypeAEndpointLeibnizGeneratorsGeneratedBy
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  exact standardABC_typeAEndpointLeibnizGeneratorsGenerated

/-- The standard quotient point carries endpoint Leibniz stability. -/
theorem standardABCPresentation_endpointStable :
    typeAEndpointStable standardABCPresentation := by
  change
    TypeAEndpointLeibnizStableForPresentation
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  exact standardABC_typeAEndpointLeibnizStable

/-- And the equivalent endpoint right-lifting statement. -/
theorem standardABCPresentation_endpointLifting :
    typeAEndpointLifting standardABCPresentation := by
  change
    TypeAEndpointLeibnizLiftingForPresentation
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  exact standardABC_typeAEndpointLeibnizLifting

/-- The canonical quotient point carries an unconditional native WFS by the
v1.45 small-object argument. -/
theorem canonicalKuuOSPresentation_isWFS :
    isWeakFactorizationSystem canonicalKuuOSPresentation := by
  change
    MorphismProperty.IsWeakFactorizationSystem
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration :
        MorphismProperty (ScaledSSet.{u}))
  exact canonicalGeneratedScaledWeakFactorizationSystem_unconditional

/-! ## Equality of quotient points transfers their complementary strengths -/

/-- Equality of the standard and canonical quotient points is exactly mutual
generation of their literal presentations. -/
theorem standardABC_eq_canonical_iff_mutualGeneration :
    standardABCPresentation = canonicalKuuOSPresentation ↔
      GeneratedScaledAnodynePresentationEquivalence
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))
        (scaledHornAttachmentGenerators :
          MorphismProperty (ScaledSSet.{u})) := by
  exact presentationClass_eq_iff _ _

/-- Equivalently, the quotient points coincide exactly when the two generated
left classes coincide. -/
theorem standardABC_eq_canonical_iff_generatedAnodyne_eq :
    standardABCPresentation = canonicalKuuOSPresentation ↔
      standardGeneratedScaledAnodyneABC =
        (canonicalGeneratedScaledAnodyne :
          MorphismProperty (ScaledSSet.{u})) := by
  exact presentationClass_eq_iff_generatedAnodyne_eq _ _

/-- If the quotient points coincide, the canonical KuuOS presentation inherits
the already-proved standard endpoint stability theorem without replaying any
boundary-prism filtration. -/
theorem canonicalKuuOSPresentation_endpointStable_of_eq
    (h : standardABCPresentation = canonicalKuuOSPresentation) :
    typeAEndpointStable canonicalKuuOSPresentation := by
  rw [← h]
  exact standardABCPresentation_endpointStable

/-- The endpoint lifting formulation transfers at the same quotient equality. -/
theorem canonicalKuuOSPresentation_endpointLifting_of_eq
    (h : standardABCPresentation = canonicalKuuOSPresentation) :
    typeAEndpointLifting canonicalKuuOSPresentation := by
  rw [← h]
  exact standardABCPresentation_endpointLifting

/-- Conversely the standard A/B/C quotient point inherits the canonical native
WFS as soon as the two generated presentations are identified. -/
theorem standardABCPresentation_isWFS_of_eq
    (h : standardABCPresentation = canonicalKuuOSPresentation) :
    isWeakFactorizationSystem standardABCPresentation := by
  rw [h]
  exact canonicalKuuOSPresentation_isWFS

/-! ## The positive v1.79 comparison as a sufficient equality witness -/

/-- The positive canonical comparison certificate maps the two literal
presentations to the same quotient point.  This is only a sufficient theorem;
v1.81 does not assert that the certificate is inhabited. -/
theorem standardABC_eq_canonical_of_positiveComparison
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    standardABCPresentation = canonicalKuuOSPresentation :=
  Quotient.sound
    (KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.StandardABCCanonicalPositiveComparisonCertificate.toGeneratedPresentationEquivalence K)

/-- Under a positive comparison, the canonical presentation inherits the
standard endpoint stability invariant. -/
theorem canonicalKuuOSPresentation_endpointStable_of_positiveComparison
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    typeAEndpointStable canonicalKuuOSPresentation :=
  canonicalKuuOSPresentation_endpointStable_of_eq
    (standardABC_eq_canonical_of_positiveComparison K)

/-- Under the same comparison, the canonical presentation inherits endpoint
right lifting. -/
theorem canonicalKuuOSPresentation_endpointLifting_of_positiveComparison
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    typeAEndpointLifting canonicalKuuOSPresentation :=
  canonicalKuuOSPresentation_endpointLifting_of_eq
    (standardABC_eq_canonical_of_positiveComparison K)

/-- Dually, the standard presentation inherits the unconditional canonical WFS
once the positive comparison identifies the quotient points. -/
theorem standardABCPresentation_isWFS_of_positiveComparison
    (K : StandardABCCanonicalPositiveComparisonCertificate.{u}) :
    isWeakFactorizationSystem standardABCPresentation :=
  standardABCPresentation_isWFS_of_eq
    (standardABC_eq_canonical_of_positiveComparison K)

/-!
The new invariant frontier is therefore exact:

```text
literal presentations E, F
        |
        | mutual orthogonal generation
        v
[E] = [F]  in GeneratedScaledAnodynePresentation
        |
        +--> generated left class
        +--> generated right class
        +--> endpoint generator membership
        +--> endpoint stability
        +--> endpoint lifting
        +--> fibrancy
        +--> weak factorization system.
```

Two distinguished points carry complementary unconditional results:

```text
[standard A/B/C] : endpoint Leibniz stability/lifting  (v1.77)
[canonical KuuOS] : native weak factorization system   (v1.45)
```

The remaining standard-vs-canonical geometric comparison is precisely the
question whether these two quotient points coincide.  A v1.79 positive
comparison certificate is one sufficient witness, but the quotient formalism
itself does not privilege that presentation of the proof.
-/

end KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
