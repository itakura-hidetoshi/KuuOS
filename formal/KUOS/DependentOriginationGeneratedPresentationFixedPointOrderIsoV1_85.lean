import KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84

namespace KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84

universe u

/-!
# Generated presentations as orthogonal fixed points v1.85

The quotient of literal presentations is already ordered by its generated left
class, and v1.84 identifies this order with one-sided orthogonal generation on
representatives.  The intrinsic object can now be identified exactly.

A generated left class is fixed by

```text
L |-> L.rlp.llp,
```

and a generated right class is fixed by

```text
R |-> R.llp.rlp.
```

This file proves that the quotient of generator presentations is order
isomorphic to the left fixed-point space and, dually, order isomorphic to the
order dual of the right fixed-point space.  Thus a generated presentation is
not merely represented by an orthogonal pair: it is canonically the same
ordered invariant as either member of that pair.
-/

/-! ## Left and right fixed-point carriers -/

/-- Orthogonally saturated generated-left classes. -/
abbrev OrthogonallySaturatedScaledAnodyne :=
  { L : MorphismProperty (ScaledSSet.{u}) // IsOrthogonallySaturated L }

/-- Right classes fixed by left-then-right orthogonality. -/
def IsRightOrthogonallySaturated
    (R : MorphismProperty (ScaledSSet.{u})) : Prop :=
  R.llp.rlp = R

/-- Orthogonally saturated generated-right classes. -/
abbrev OrthogonallySaturatedScaledFibration :=
  { R : MorphismProperty (ScaledSSet.{u}) // IsRightOrthogonallySaturated R }

/-- Every quotient-generated left class is an orthogonal fixed point. -/
theorem generatedAnodyneClass_isOrthogonallySaturated
    (P : GeneratedScaledAnodynePresentation.{u}) :
    IsOrthogonallySaturated (generatedAnodyneClass P) := by
  refine Quotient.inductionOn P ?_
  intro E
  change IsOrthogonallySaturated (externalGeneratedScaledAnodyne E)
  exact externalGeneratedScaledAnodyne_isOrthogonallySaturated E

/-- Every quotient-generated right class is a right orthogonal fixed point. -/
theorem generatedFibrationClass_isRightOrthogonallySaturated
    (P : GeneratedScaledAnodynePresentation.{u}) :
    IsRightOrthogonallySaturated (generatedFibrationClass P) := by
  refine Quotient.inductionOn P ?_
  intro E
  change
    (externalGeneratedScaledFibration E).llp.rlp =
      externalGeneratedScaledFibration E
  unfold externalGeneratedScaledFibration
  exact MorphismProperty.rlp_llp_rlp E

/-! ## The left fixed-point order model -/

/-- Send a quotient presentation to its canonical generated-left fixed point. -/
def presentationToSaturatedAnodyne
    (P : GeneratedScaledAnodynePresentation.{u}) :
    OrthogonallySaturatedScaledAnodyne.{u} :=
  ⟨generatedAnodyneClass P,
    generatedAnodyneClass_isOrthogonallySaturated P⟩

/-- Any saturated left class presents itself. -/
def saturatedAnodyneToPresentation
    (L : OrthogonallySaturatedScaledAnodyne.{u}) :
    GeneratedScaledAnodynePresentation.{u} :=
  presentationClass L.1

/-- Re-presenting a quotient point by its generated left class changes nothing. -/
@[simp]
theorem saturatedAnodyneToPresentation_presentationToSaturatedAnodyne
    (P : GeneratedScaledAnodynePresentation.{u}) :
    saturatedAnodyneToPresentation (presentationToSaturatedAnodyne P) = P := by
  change presentationClass (generatedAnodyneClass P) = P
  apply eq_of_generatedAnodyneClass_eq
  rw [generatedAnodyneClass_presentationClass]
  exact generatedAnodyneClass_isOrthogonallySaturated P

/-- Taking the generated left class of a saturated self-presentation returns
that same saturated class. -/
@[simp]
theorem presentationToSaturatedAnodyne_saturatedAnodyneToPresentation
    (L : OrthogonallySaturatedScaledAnodyne.{u}) :
    presentationToSaturatedAnodyne (saturatedAnodyneToPresentation L) = L := by
  apply Subtype.ext
  change externalGeneratedScaledAnodyne L.1 = L.1
  exact L.2

/-- The quotient presentation poset is exactly the poset of orthogonally
saturated generated-left classes. -/
noncomputable def generatedPresentationSaturatedAnodyneOrderIso :
    GeneratedScaledAnodynePresentation.{u} ≃o
      OrthogonallySaturatedScaledAnodyne.{u} where
  toFun := presentationToSaturatedAnodyne
  invFun := saturatedAnodyneToPresentation
  left_inv := saturatedAnodyneToPresentation_presentationToSaturatedAnodyne
  right_inv := presentationToSaturatedAnodyne_saturatedAnodyneToPresentation
  map_rel_iff' := by
    intro P Q
    change
      generatedAnodyneClass P ≤ generatedAnodyneClass Q ↔ P ≤ Q
    exact (le_iff_generatedAnodyneClass_le P Q).symm

@[simp]
theorem generatedPresentationSaturatedAnodyneOrderIso_apply_val
    (P : GeneratedScaledAnodynePresentation.{u}) :
    (generatedPresentationSaturatedAnodyneOrderIso P).1 =
      generatedAnodyneClass P :=
  rfl

/-! ## The dual right fixed-point order model -/

/-- Send a quotient presentation to its generated-right fixed point. -/
def presentationToSaturatedFibration
    (P : GeneratedScaledAnodynePresentation.{u}) :
    OrthogonallySaturatedScaledFibration.{u} :=
  ⟨generatedFibrationClass P,
    generatedFibrationClass_isRightOrthogonallySaturated P⟩

/-- A saturated right class is presented by its left orthogonal. -/
def saturatedFibrationToPresentation
    (R : OrthogonallySaturatedScaledFibration.{u}) :
    GeneratedScaledAnodynePresentation.{u} :=
  presentationClass R.1.llp

/-- Re-presenting a quotient point by the left orthogonal of its right class
returns the original quotient point. -/
@[simp]
theorem saturatedFibrationToPresentation_presentationToSaturatedFibration
    (P : GeneratedScaledAnodynePresentation.{u}) :
    saturatedFibrationToPresentation (presentationToSaturatedFibration P) = P := by
  change presentationClass ((generatedFibrationClass P).llp) = P
  rw [generatedFibrationClass_llp]
  exact saturatedAnodyneToPresentation_presentationToSaturatedAnodyne P

/-- Taking the right class of a saturated right self-presentation returns the
same right fixed point. -/
@[simp]
theorem presentationToSaturatedFibration_saturatedFibrationToPresentation
    (R : OrthogonallySaturatedScaledFibration.{u}) :
    presentationToSaturatedFibration (saturatedFibrationToPresentation R) = R := by
  apply Subtype.ext
  change externalGeneratedScaledFibration R.1.llp = R.1
  exact R.2

/-- The presentation order is dually the reverse-inclusion order on saturated
right classes. -/
noncomputable def generatedPresentationSaturatedFibrationOrderIso :
    GeneratedScaledAnodynePresentation.{u} ≃o
      OrderDual (OrthogonallySaturatedScaledFibration.{u}) where
  toFun := presentationToSaturatedFibration
  invFun := saturatedFibrationToPresentation
  left_inv := saturatedFibrationToPresentation_presentationToSaturatedFibration
  right_inv := presentationToSaturatedFibration_saturatedFibrationToPresentation
  map_rel_iff' := by
    intro P Q
    change
      generatedFibrationClass Q ≤ generatedFibrationClass P ↔ P ≤ Q
    exact (le_iff_generatedFibrationClass_reverse_le P Q).symm

@[simp]
theorem generatedPresentationSaturatedFibrationOrderIso_apply_val
    (P : GeneratedScaledAnodynePresentation.{u}) :
    ((generatedPresentationSaturatedFibrationOrderIso P :
      OrderDual (OrthogonallySaturatedScaledFibration.{u}))).1 =
        generatedFibrationClass P :=
  rfl

/-! ## Orthogonality duality without presentation choices -/

/-- Passing through the presentation quotient identifies saturated left classes
with the order dual of saturated right classes. -/
noncomputable def saturatedAnodyneFibrationOrderIso :
    OrthogonallySaturatedScaledAnodyne.{u} ≃o
      OrderDual (OrthogonallySaturatedScaledFibration.{u}) :=
  generatedPresentationSaturatedAnodyneOrderIso.symm.trans
    generatedPresentationSaturatedFibrationOrderIso

/-- Equality of generated presentations can therefore be checked on the
canonical saturated-left fixed point. -/
theorem presentation_eq_iff_saturatedAnodyne_eq
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P = Q ↔
      presentationToSaturatedAnodyne P = presentationToSaturatedAnodyne Q := by
  constructor
  · rintro rfl
    rfl
  · intro h
    exact generatedPresentationSaturatedAnodyneOrderIso.injective h

/-- Or, equivalently, on the canonical saturated-right fixed point. -/
theorem presentation_eq_iff_saturatedFibration_eq
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P = Q ↔
      presentationToSaturatedFibration P = presentationToSaturatedFibration Q := by
  constructor
  · rintro rfl
    rfl
  · intro h
    exact generatedPresentationSaturatedFibrationOrderIso.injective h

/-!
The presentation-independent object is now explicit:

```text
GeneratedScaledAnodynePresentation
  ≃o { L // L.rlp.llp = L }
  ≃o OrderDual { R // R.llp.rlp = R }.
```

The standard A/B/C and canonical KuuOS generator lists are therefore merely two
possible coordinates for points in this fixed-point order.  Their equality
problem remains geometric, but all endpoint, fibrancy, order, and comparison
statements can now be phrased directly on the canonical fixed-point invariant.
-/

end KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85
