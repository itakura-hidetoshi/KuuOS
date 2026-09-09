import KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic

namespace KUOS.DependentOriginationUnitIsoAdjunctionCarrierTransferV2_38

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
open KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36
open KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH uB vB wB

/-!
# Unit-isomorphism adjunction carrier transfer v2.38

The v2.37 layer identified a concrete one-sided cancellation mechanism for
transporting Stage III essential uniqueness from a completed weak carrier to the
fixed coherent carrier:

```text
U.chosen --p--> C.chosen --q--> U.chosen
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift.
```

This file derives that split comparison from more intrinsic bicategorical data.
The minimal structured hypothesis used here is an adjunction

```text
p.hom ⊣ q.hom
```

whose unit

```text
𝟙 U.chosen.lift ⟶ p.hom ≫ q.hom
```

is invertible.  Its inverse is exactly the v2.37 retract isomorphism.  Thus no
second inverse equation is needed for the cancellation theorem.

A stronger route is also formalized.  If genuine factor morphisms `p` and `q`
carry two-sided 2-isomorphisms

```text
𝟙 U.chosen.lift ≅ p.hom ≫ q.hom,
q.hom ≫ p.hom ≅ 𝟙 C.chosen.lift,
```

Mathlib's `Bicategory.Equivalence.mkOfAdjointifyCounit` upgrades them to an actual
adjoint equivalence, adjusting the counit so that the triangle identity holds.
This gives a principled equivalence-based sufficient condition for the v2.37
split transport.

The file does not prove that arbitrary completed carriers admit either an
invertible-unit adjunction or two-sided equivalence data.  Those remain genuine
existence questions.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A factor-level adjunction from the fixed coherent carrier to another weak
Stage II carrier whose unit is invertible.

The factor morphisms retain the v2.18 objectwise comparison triangles.  The
adjunction lives on their underlying StrongTrans 1-cells.  Only the unit is
required to be an isomorphism; the counit need not be invertible. -/
structure HigherFixedChosenUnitIsoAdjunctionComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) where
  forward : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen
  backward : HigherLocalizationFactorMorphism (W := W) C.chosen U.chosen
  adj : Bicategory.Adjunction forward.hom backward.hom
  unit_isIso : IsIso adj.unit

/-- An invertible-unit adjunction canonically supplies the one-sided split
comparison required by v2.37. -/
noncomputable def splitCarrierComparisonOfUnitIsoAdjunction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (A : HigherFixedChosenUnitIsoAdjunctionComparison (W := W) U C) :
    HigherFixedChosenSplitCarrierComparison (W := W) U C where
  forward := A.forward
  backward := A.backward
  fixed_retract := by
    letI : IsIso A.adj.unit := A.unit_isIso
    exact ⟨(asIso A.adj.unit).symm⟩

/-- Therefore Stage III essential uniqueness transports along an invertible-unit
factor adjunction. -/
theorem fixedChosenEssentialUniqueness_of_unitIsoAdjunction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (A : HigherFixedChosenUnitIsoAdjunctionComparison (W := W) U C) :
    HigherFixedChosenEssentialUniqueness (W := W) U :=
  fixedChosenEssentialUniqueness_of_splitCarrierComparison
    (W := W) U C hUnique
    (splitCarrierComparisonOfUnitIsoAdjunction (W := W) A)

/-- Completion condition using invertible-unit factor adjunctions on all completed
weak carriers. -/
def HigherFixedChosenUnitIsoAdjunctionComparisonCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) →
      Nonempty (HigherFixedChosenUnitIsoAdjunctionComparison (W := W) U C)

/-- Invertible-unit adjunction completion implies the v2.37 split-comparison
completion condition. -/
theorem splitCarrierComparisonCompletion_of_unitIsoAdjunctionCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hAdj : HigherFixedChosenUnitIsoAdjunctionComparisonCompletion (W := W) U) :
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U := by
  intro C hUnique
  rcases hAdj C hUnique with ⟨A⟩
  exact ⟨splitCarrierComparisonOfUnitIsoAdjunction (W := W) A⟩

/-- Hence invertible-unit adjunction completion is sufficient for fixed-carrier
Stage III uniqueness transfer. -/
theorem carrierUniquenessTransfer_of_unitIsoAdjunctionCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hAdj : HigherFixedChosenUnitIsoAdjunctionComparisonCompletion (W := W) U) :
    HigherFixedChosenCarrierUniquenessTransfer (W := W) U :=
  carrierUniquenessTransfer_of_splitCarrierComparisonCompletion
    (W := W) U
    (splitCarrierComparisonCompletion_of_unitIsoAdjunctionCompletion
      (W := W) U hAdj)

/-- Consequently, invertible-unit adjunction completion closes the coherent route
for the fixed datum. -/
theorem routeCompleteness_of_unitIsoAdjunctionCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hAdj : HigherFixedChosenUnitIsoAdjunctionComparisonCompletion (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  routeCompleteness_of_splitCarrierComparisonCompletion
    (W := W) U
    (splitCarrierComparisonCompletion_of_unitIsoAdjunctionCompletion
      (W := W) U hAdj)

/-- Convert a Mathlib bicategorical adjoint equivalence into its underlying
adjunction.  This is internal to the existing bicategory API: the unit and counit
are the hom 2-cells of the stored isomorphisms, and both triangle identities are
already theorems of `Bicategory.Equivalence`. -/
def adjunctionOfAdjointEquivalence
    {B : Type uB} [Bicategory.{wB, vB} B]
    {a b : B} (e : Bicategory.Equivalence a b) :
    Bicategory.Adjunction e.hom e.inv where
  unit := e.unit.hom
  counit := e.counit.hom
  left_triangle := Bicategory.Equivalence.left_triangle_hom e
  right_triangle := Bicategory.Equivalence.right_triangle_hom e

/-- Stronger two-sided equivalence data on genuine factor morphisms.

No triangle identity is required as input.  Mathlib can adjointify the counit to
produce an actual bicategorical equivalence. -/
structure HigherFixedChosenTwoSidedCarrierEquivalenceData
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) where
  forward : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen
  backward : HigherLocalizationFactorMorphism (W := W) C.chosen U.chosen
  unit : 𝟙 U.chosen.lift ≅ forward.hom ≫ backward.hom
  counit : backward.hom ≫ forward.hom ≅ 𝟙 C.chosen.lift

/-- Two-sided carrier equivalence data canonically yields an actual Mathlib
adjoint equivalence.  The given unit is retained; the counit may be adjusted by
`mkOfAdjointifyCounit` to satisfy the triangle law. -/
noncomputable def adjointEquivalenceOfTwoSidedCarrierData
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (E : HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) :
    Bicategory.Equivalence U.chosen.lift C.chosen.lift :=
  Bicategory.Equivalence.mkOfAdjointifyCounit E.unit E.counit

@[simp] theorem adjointEquivalenceOfTwoSidedCarrierData_hom
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (E : HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) :
    (adjointEquivalenceOfTwoSidedCarrierData (W := W) E).hom = E.forward.hom := by
  rfl

@[simp] theorem adjointEquivalenceOfTwoSidedCarrierData_inv
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (E : HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) :
    (adjointEquivalenceOfTwoSidedCarrierData (W := W) E).inv = E.backward.hom := by
  rfl

@[simp] theorem adjointEquivalenceOfTwoSidedCarrierData_unit
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (E : HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) :
    (adjointEquivalenceOfTwoSidedCarrierData (W := W) E).unit = E.unit := by
  rfl

/-- Two-sided equivalence data already contains the retract required by v2.37:
the inverse of its unit. -/
noncomputable def splitCarrierComparisonOfTwoSidedCarrierData
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R}
    {C : WeakHigherLocalizationUniversalCandidate (W := W) R}
    (E : HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) :
    HigherFixedChosenSplitCarrierComparison (W := W) U C where
  forward := E.forward
  backward := E.backward
  fixed_retract := ⟨E.unit.symm⟩

/-- Two-sided factor equivalence data transports Stage III uniqueness to the
fixed carrier. -/
theorem fixedChosenEssentialUniqueness_of_twoSidedCarrierEquivalenceData
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (E : HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C) :
    HigherFixedChosenEssentialUniqueness (W := W) U :=
  fixedChosenEssentialUniqueness_of_splitCarrierComparison
    (W := W) U C hUnique
    (splitCarrierComparisonOfTwoSidedCarrierData (W := W) E)

/-- Completion condition using two-sided factor equivalence data. -/
def HigherFixedChosenTwoSidedCarrierEquivalenceCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) →
      Nonempty (HigherFixedChosenTwoSidedCarrierEquivalenceData (W := W) U C)

/-- Two-sided equivalence completion implies split-comparison completion. -/
theorem splitCarrierComparisonCompletion_of_twoSidedEquivalenceCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hEq : HigherFixedChosenTwoSidedCarrierEquivalenceCompletion (W := W) U) :
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U := by
  intro C hUnique
  rcases hEq C hUnique with ⟨E⟩
  exact ⟨splitCarrierComparisonOfTwoSidedCarrierData (W := W) E⟩

/-- Therefore two-sided factor equivalence completion is sufficient for carrier
uniqueness transfer. -/
theorem carrierUniquenessTransfer_of_twoSidedEquivalenceCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hEq : HigherFixedChosenTwoSidedCarrierEquivalenceCompletion (W := W) U) :
    HigherFixedChosenCarrierUniquenessTransfer (W := W) U :=
  carrierUniquenessTransfer_of_splitCarrierComparisonCompletion
    (W := W) U
    (splitCarrierComparisonCompletion_of_twoSidedEquivalenceCompletion
      (W := W) U hEq)

/-- Hence two-sided factor equivalence completion closes coherent route
completeness. -/
theorem routeCompleteness_of_twoSidedEquivalenceCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hEq : HigherFixedChosenTwoSidedCarrierEquivalenceCompletion (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  routeCompleteness_of_splitCarrierComparisonCompletion
    (W := W) U
    (splitCarrierComparisonCompletion_of_twoSidedEquivalenceCompletion
      (W := W) U hEq)

/-- Global invertible-unit adjunction completion principle.  This remains an
explicit hypothesis, not a theorem for arbitrary coherent universal data. -/
def HigherFixedChosenUnitIsoAdjunctionComparisonCompletionPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFixedChosenUnitIsoAdjunctionComparisonCompletion (W := W) U

/-- Global two-sided factor equivalence completion principle. -/
def HigherFixedChosenTwoSidedCarrierEquivalenceCompletionPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFixedChosenTwoSidedCarrierEquivalenceCompletion (W := W) U

/-!
## Boundary after v2.38

There are now two explicit intrinsic routes into the v2.37 split-cancellation
mechanism:

```text
factor adjunction p ⊣ q + invertible unit
                |
                v
         p ≫ q ≅ id
                |
                v
      fixed Stage III uniqueness
                |
                v
       coherent route completeness
```

and the stronger route

```text
two-sided factor 2-isomorphisms
  id ≅ p ≫ q,  q ≫ p ≅ id
                |
                | Mathlib mkOfAdjointifyCounit
                v
      actual adjoint equivalence
                |
                v
         p ≫ q ≅ id
                |
                v
       coherent route completeness.
```

The remaining open problem is now sharper: derive one of these comparison
structures for arbitrary completed carriers from a justified universal,
fully-faithful/conservative, strict-sector, or other bicategorical property.  In
particular, mutual existence of weak factor morphisms alone still does not imply
that the adjunction unit is invertible.
-/

end KUOS.DependentOriginationUnitIsoAdjunctionCarrierTransferV2_38