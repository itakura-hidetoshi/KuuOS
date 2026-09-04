import KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82

namespace KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55
open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80
open KUOS.DependentOriginationGeneratedPresentationEndpointInvariantV1_80.GeneratedScaledAnodynePresentationEquivalence
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81

universe u

/-!
# Generated-presentation posetal reflection v1.83

Version v1.81 quotiented literal scaled-anodyne generator families by mutual
orthogonal generation.  Version v1.82 then showed that the canonical KuuOS
quotient point has the endpoint Leibniz theorem independently of its comparison
with the standard A/B/C point.

The quotient therefore admits a sharper intrinsic structure.  For a generated
presentation `P`, write

```text
L_P := generatedAnodyneClass P
R_P := generatedFibrationClass P.
```

Every quotient point is an orthogonal pair:

```text
L_P.rlp = R_P,
R_P.llp = L_P.
```

We order quotient presentations by inclusion of their generated left classes,

```text
P <= Q  iff  L_P <= L_Q.
```

Because the quotient has already identified presentations with equal generated
left class, this preorder is antisymmetric and hence is a genuine partial
order.  Orthogonality gives the dual characterization

```text
P <= Q  iff  R_Q <= R_P.
```

Thus the quotient is exactly the posetal reflection naturally carried by the
orthogonality Galois connection.

This also isolates the valid one-sided transport laws.  Endpoint generator
membership and endpoint right lifting are covariant in this order, whereas
fibrancy is contravariant.  Endpoint stability and weak-factorization-system
structure are intentionally not assigned a one-sided transport theorem here:
their existing quotient invariance is an equality-level statement.
-/

/-! ## Orthogonal pair attached to every quotient point -/

/-- The generated right class of a quotient presentation is the right
orthogonal of its generated left class. -/
theorem generatedAnodyneClass_rlp
    (P : GeneratedScaledAnodynePresentation.{u}) :
    (generatedAnodyneClass P).rlp = generatedFibrationClass P := by
  refine Quotient.inductionOn P ?_
  intro E
  change
    (externalGeneratedScaledAnodyne E).rlp =
      externalGeneratedScaledFibration E
  unfold externalGeneratedScaledAnodyne externalGeneratedScaledFibration
  exact MorphismProperty.rlp_llp_rlp E

/-- Dually, the generated left class is the left orthogonal of the generated
right class. -/
theorem generatedFibrationClass_llp
    (P : GeneratedScaledAnodynePresentation.{u}) :
    (generatedFibrationClass P).llp = generatedAnodyneClass P := by
  refine Quotient.inductionOn P ?_
  intro E
  change
    (externalGeneratedScaledFibration E).llp =
      externalGeneratedScaledAnodyne E
  rfl

/-! ## The generated left class separates quotient points -/

/-- Equality of generated left classes already forces equality of quotient
presentations. -/
theorem eq_of_generatedAnodyneClass_eq
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (h : generatedAnodyneClass P = generatedAnodyneClass Q) :
    P = Q := by
  revert h
  refine Quotient.inductionOn₂ P Q ?_
  intro E F h
  exact (presentationClass_eq_iff_generatedAnodyne_eq E F).2 h

/-- Extensional characterization of equality by the generated left class. -/
theorem eq_iff_generatedAnodyneClass_eq
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P = Q ↔ generatedAnodyneClass P = generatedAnodyneClass Q := by
  constructor
  · rintro rfl
    rfl
  · exact eq_of_generatedAnodyneClass_eq

/-! ## Posetal reflection -/

/-- The quotient of presentations by mutual generation is ordered by inclusion
of generated left classes. -/
instance : PartialOrder GeneratedScaledAnodynePresentation.{u} where
  le P Q := generatedAnodyneClass P ≤ generatedAnodyneClass Q
  le_refl P := le_rfl
  le_trans P Q R hPQ hQR := hPQ.trans hQR
  le_antisymm P Q hPQ hQP :=
    eq_of_generatedAnodyneClass_eq (le_antisymm hPQ hQP)

/-- The order is definitionally the inclusion order on generated left classes. -/
@[simp]
theorem le_iff_generatedAnodyneClass_le
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P ≤ Q ↔ generatedAnodyneClass P ≤ generatedAnodyneClass Q :=
  Iff.rfl

/-- Left-class inclusion reverses the generated right classes. -/
theorem generatedFibrationClass_antitone
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (hPQ : P ≤ Q) :
    generatedFibrationClass Q ≤ generatedFibrationClass P := by
  rw [← generatedAnodyneClass_rlp Q, ← generatedAnodyneClass_rlp P]
  exact MorphismProperty.antitone_rlp hPQ

/-- Conversely, reverse inclusion of the generated right classes recovers the
presentation order. -/
theorem le_of_generatedFibrationClass_reverse
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (hQP : generatedFibrationClass Q ≤ generatedFibrationClass P) :
    P ≤ Q := by
  change generatedAnodyneClass P ≤ generatedAnodyneClass Q
  rw [← generatedFibrationClass_llp P, ← generatedFibrationClass_llp Q]
  exact MorphismProperty.antitone_llp hQP

/-- Orthogonal Galois duality: ordering by the generated left class is exactly
reverse ordering by the generated right class. -/
@[simp]
theorem le_iff_generatedFibrationClass_reverse_le
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P ≤ Q ↔ generatedFibrationClass Q ≤ generatedFibrationClass P := by
  constructor
  · exact generatedFibrationClass_antitone
  · exact le_of_generatedFibrationClass_reverse

/-- The generated right class also separates quotient points. -/
theorem eq_iff_generatedFibrationClass_eq
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P = Q ↔ generatedFibrationClass P = generatedFibrationClass Q := by
  constructor
  · rintro rfl
    rfl
  · intro h
    apply eq_of_generatedAnodyneClass_eq
    rw [← generatedFibrationClass_llp P, ← generatedFibrationClass_llp Q, h]

/-- Equality in the quotient is equivalently mutual comparison in the new
partial order. -/
theorem eq_iff_le_and_le
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P = Q ↔ P ≤ Q ∧ Q ≤ P := by
  constructor
  · rintro rfl
    exact ⟨le_rfl, le_rfl⟩
  · rintro ⟨hPQ, hQP⟩
    exact le_antisymm hPQ hQP

/-! ## Quotient predicates in left/right-class form -/

/-- Endpoint generator membership is exactly inclusion of the fixed endpoint
family in the generated left class. -/
theorem typeAEndpointGeneratorsGenerated_iff
    (P : GeneratedScaledAnodynePresentation.{u}) :
    typeAEndpointGeneratorsGenerated P ↔
      (standardTypeAScaledLeibnizPushoutProductGenerators :
        MorphismProperty (ScaledSSet.{u})) ≤ generatedAnodyneClass P := by
  refine Quotient.inductionOn P ?_
  intro E
  rfl

/-- Endpoint right lifting can be read directly from the generated right
class of the quotient point. -/
theorem typeAEndpointLifting_iff
    (P : GeneratedScaledAnodynePresentation.{u}) :
    typeAEndpointLifting P ↔
      ∀ (g : StandardTypeAHornAttachmentGeneratorIndex)
        {X Y : ScaledSSet.{u}} (p : X ⟶ Y),
        generatedFibrationClass P p →
          HasLiftingProperty
            (standardTypeAEndpointScaledLeibnizPushoutProductHom g) p := by
  refine Quotient.inductionOn P ?_
  intro E
  rfl

/-- Fibrancy of `X` is membership of its terminal map in the quotient right
class. -/
theorem isFibrant_iff
    (X : ScaledSSet.{u})
    (P : GeneratedScaledAnodynePresentation.{u}) :
    isFibrant X P ↔
      generatedFibrationClass P (ScaledSSet.toPoint X) := by
  refine Quotient.inductionOn P ?_
  intro E
  rfl

/-! ## Valid one-sided transport laws -/

/-- Membership of the fixed endpoint Leibniz generator family is covariant in
the presentation order. -/
theorem typeAEndpointGeneratorsGenerated_mono
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (hPQ : P ≤ Q)
    (hP : typeAEndpointGeneratorsGenerated P) :
    typeAEndpointGeneratorsGenerated Q := by
  rw [typeAEndpointGeneratorsGenerated_iff] at hP ⊢
  exact hP.trans hPQ

/-- Endpoint right lifting is covariant: a larger generated left class has a
smaller right class, so a lifting theorem for `P` automatically applies to
`Q`. -/
theorem typeAEndpointLifting_mono
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (hPQ : P ≤ Q)
    (hP : typeAEndpointLifting P) :
    typeAEndpointLifting Q := by
  rw [typeAEndpointLifting_iff] at hP ⊢
  intro g X Y p hp
  exact hP g p (generatedFibrationClass_antitone hPQ hp)

/-- Fibrancy is contravariant in the presentation order, exactly because right
classes reverse inclusions. -/
theorem isFibrant_antitone
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (hPQ : P ≤ Q)
    (X : ScaledSSet.{u})
    (hQ : isFibrant X Q) :
    isFibrant X P := by
  rw [isFibrant_iff] at hQ ⊢
  exact generatedFibrationClass_antitone hPQ hQ

/-! ## Standard/canonical comparison is now purely order-theoretic -/

/-- Equality of the standard A/B/C and canonical KuuOS presentation points is
exactly the conjunction of the two directional presentation comparisons. -/
theorem standardABC_eq_canonical_iff_mutual_le :
    standardABCPresentation.{u} = canonicalKuuOSPresentation.{u} ↔
      standardABCPresentation.{u} ≤ canonicalKuuOSPresentation.{u} ∧
        canonicalKuuOSPresentation.{u} ≤ standardABCPresentation.{u} :=
  eq_iff_le_and_le _ _

/-!
The v1.83 spine is therefore:

```text
quotient presentation P
  |-- L_P = generatedAnodyneClass P
  `-- R_P = generatedFibrationClass P

orthogonal pair:
  L_P.rlp = R_P
  R_P.llp = L_P

posetal reflection:
  P <= Q
    <-> L_P <= L_Q
    <-> R_Q <= R_P

one-sided transport:
  endpoint generator membership : P -> Q
  endpoint right lifting        : P -> Q
  fibrancy                      : Q -> P

standard/canonical identification:
  standard = canonical
    <-> standard <= canonical and canonical <= standard
```

The endpoint theorem and the canonical WFS remain unconditional at the
canonical point by v1.82 and v1.45 respectively.  The unresolved standard vs
canonical geometry is now cleanly confined to proving the two order directions
when full presentation identification is desired.
-/

end KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
