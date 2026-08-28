import KUOS.DependentOriginationStandardCanonicalOrthogonalityDiamondV1_119
import Mathlib.Order.CompleteLattice.Lemmas

namespace KUOS.DependentOriginationTerminalFibrancyNonfaithfulPresentationOrderV1_120

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
open KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115
open KUOS.DependentOriginationStandardCanonicalOrthogonalityDiamondV1_119

universe u

noncomputable section

/-!
# Terminal fibrancy does not faithfully reflect presentation order v1.120

Version v1.119 proves that the standard A/B/C presentation `S` and canonical
KuuOS presentation `C` form a strict orthogonality diamond.  In particular,
for the upper envelope

```text
U := S ⊔ C
```

we have the strict presentation inequality `C < U`.

At the level of full right classes, v1.86 computes a presentation join by
intersection:

```text
R_U = R_S ∩ R_C.
```

But v1.115 proves that on terminal maps canonical fibrancy already implies
standard A/B/C fibrancy.  Hence the standard factor in this intersection is
redundant after restricting to terminal maps:

```text
X is U-fibrant
  ↔ X is S-fibrant ∧ X is C-fibrant
  ↔ X is C-fibrant.
```

Thus `C` and the strictly larger presentation `U` have exactly the same
fibrant objects.  The map from generated presentations to their terminal
fibrant-object semantics is therefore neither injective nor order-reflecting.
This is the exact sense in which terminal semantics forgets genuine
presentation-level orthogonality information.
-/

/-! ## The upper-envelope right class is the intersection -/

/-- The standard quotient point has exactly the concrete standard A/B/C right
class. -/
@[simp]
theorem generatedFibrationClass_standardABCPresentation :
    generatedFibrationClass
        (standardABCPresentation :
          GeneratedScaledAnodynePresentation.{u}) =
      standardGeneratedScaledFibrationABC :=
  rfl

/-- The canonical quotient point has exactly the native canonical right class. -/
@[simp]
theorem generatedFibrationClass_canonicalKuuOSPresentation :
    generatedFibrationClass
        (canonicalKuuOSPresentation :
          GeneratedScaledAnodynePresentation.{u}) =
      canonicalGeneratedScaledFibration :=
  rfl

/-- Specializing the v1.86 arbitrary-join formula to the binary
standard/canonical join gives the exact full right-class intersection. -/
theorem generatedFibrationClass_upperEnvelope :
    generatedFibrationClass
        (standardCanonicalUpperEnvelope :
          GeneratedScaledAnodynePresentation.{u}) =
      standardGeneratedScaledFibrationABC ⊓
        (canonicalGeneratedScaledFibration :
          MorphismProperty (ScaledSSet.{u})) := by
  rw [standardCanonicalUpperEnvelope, sup_eq_iSup]
  rw [generatedFibrationClass_iSup]
  rw [iInf_bool_eq]
  simp

/-! ## Terminal fibrancy of the join -/

/-- Quotient fibrancy at the standard point is the concrete standard A/B/C
terminal-right predicate from v1.115. -/
theorem standardABCPresentation_isFibrant_iff_standardABCFibrant
    (X : ScaledSSet.{u}) :
    isFibrant X standardABCPresentation ↔ IsStandardABCFibrant X := by
  rw [isFibrant_iff]
  rfl

/-- Quotient fibrancy at the canonical point is exactly attachment fibrancy. -/
theorem canonicalKuuOSPresentation_isFibrant_iff_attachmentFibrant
    (X : ScaledSSet.{u}) :
    isFibrant X canonicalKuuOSPresentation ↔ IsAttachmentFibrant X := by
  rw [isFibrant_iff]
  rfl

/-- Before using the terminal-map collapse, fibrancy for the upper envelope is
literally the conjunction of standard and canonical terminal fibrancy. -/
theorem upperEnvelope_isFibrant_iff_standard_and_canonical
    (X : ScaledSSet.{u}) :
    isFibrant X standardCanonicalUpperEnvelope ↔
      IsStandardABCFibrant X ∧ IsAttachmentFibrant X := by
  rw [isFibrant_iff, generatedFibrationClass_upperEnvelope]
  rfl

/-- On terminal maps the standard factor in the upper-envelope intersection is
redundant: canonical fibrancy already implies standard A/B/C fibrancy by
v1.115. -/
theorem upperEnvelope_isFibrant_iff_canonical
    (X : ScaledSSet.{u}) :
    isFibrant X standardCanonicalUpperEnvelope ↔
      isFibrant X canonicalKuuOSPresentation := by
  rw [upperEnvelope_isFibrant_iff_standard_and_canonical,
    canonicalKuuOSPresentation_isFibrant_iff_attachmentFibrant]
  constructor
  · exact And.right
  · intro hX
    exact ⟨attachmentFibrant_implies_standardABCFibrant hX, hX⟩

/-- The central phenomenon: the canonical point is strictly below the upper
envelope as a generated presentation, while every scaled simplicial set has
identical fibrancy semantics at the two points. -/
theorem canonical_lt_upperEnvelope_but_same_fibrant_objects :
    (canonicalKuuOSPresentation :
        GeneratedScaledAnodynePresentation.{u}) <
      standardCanonicalUpperEnvelope ∧
    (∀ X : ScaledSSet.{u},
      isFibrant X canonicalKuuOSPresentation ↔
        isFibrant X standardCanonicalUpperEnvelope) := by
  exact ⟨canonicalKuuOS_lt_upperEnvelope,
    fun X => (upperEnvelope_isFibrant_iff_canonical X).symm⟩

/-! ## Fibrant-object semantics is non-faithful -/

/-- Terminal/fibrant-object semantics of a generated presentation. -/
def fibrantObjectSemantics
    (P : GeneratedScaledAnodynePresentation.{u}) : Set (ScaledSSet.{u}) :=
  {X | isFibrant X P}

/-- The canonical presentation and its strict upper envelope have exactly the
same terminal fibrant-object semantics. -/
theorem fibrantObjectSemantics_canonical_eq_upperEnvelope :
    fibrantObjectSemantics
        (canonicalKuuOSPresentation :
          GeneratedScaledAnodynePresentation.{u}) =
      fibrantObjectSemantics standardCanonicalUpperEnvelope := by
  ext X
  exact (upperEnvelope_isFibrant_iff_canonical X).symm

/-- Consequently terminal fibrant-object semantics is not injective on the
presentation lattice. -/
theorem fibrantObjectSemantics_not_injective :
    ¬ Function.Injective (fibrantObjectSemantics (u := u)) := by
  intro hinj
  apply canonicalKuuOSPresentation_ne_upperEnvelope
  exact hinj fibrantObjectSemantics_canonical_eq_upperEnvelope

/-- More strongly, the contravariant semantic order does not reflect the
presentation order.  Equality of terminal semantics supplies an inclusion in
the reverse semantic order, but it cannot force the false comparison
`U ≤ C`. -/
theorem fibrantObjectSemantics_not_orderReflecting :
    ¬ (∀ P Q : GeneratedScaledAnodynePresentation.{u},
      fibrantObjectSemantics Q ⊆ fibrantObjectSemantics P → P ≤ Q) := by
  intro hreflect
  have hsubset :
      fibrantObjectSemantics
          (canonicalKuuOSPresentation :
            GeneratedScaledAnodynePresentation.{u}) ⊆
        fibrantObjectSemantics standardCanonicalUpperEnvelope := by
    rw [fibrantObjectSemantics_canonical_eq_upperEnvelope]
  have hbad :
      (standardCanonicalUpperEnvelope :
          GeneratedScaledAnodynePresentation.{u}) ≤
        canonicalKuuOSPresentation :=
    hreflect standardCanonicalUpperEnvelope canonicalKuuOSPresentation hsubset
  exact (not_le_of_gt canonicalKuuOS_lt_upperEnvelope) hbad

/-! ## Coherent final certificate -/

/-- A single certificate recording the complete v1.120 phenomenon: full
right-class intersection at the join, terminal collapse to the canonical
factor, strict presentation inequality, and non-faithfulness of the resulting
fibrant-object semantics. -/
structure TerminalFibrancyNonfaithfulPresentationOrder : Prop where
  upperRightClassIntersection :
    generatedFibrationClass
        (standardCanonicalUpperEnvelope :
          GeneratedScaledAnodynePresentation.{u}) =
      standardGeneratedScaledFibrationABC ⊓
        (canonicalGeneratedScaledFibration :
          MorphismProperty (ScaledSSet.{u}))
  terminalCollapse :
    ∀ X : ScaledSSet.{u},
      isFibrant X standardCanonicalUpperEnvelope ↔
        isFibrant X canonicalKuuOSPresentation
  strictPresentationGap :
    (canonicalKuuOSPresentation :
        GeneratedScaledAnodynePresentation.{u}) <
      standardCanonicalUpperEnvelope
  semanticEquality :
    fibrantObjectSemantics
        (canonicalKuuOSPresentation :
          GeneratedScaledAnodynePresentation.{u}) =
      fibrantObjectSemantics standardCanonicalUpperEnvelope
  semanticsNotInjective :
    ¬ Function.Injective (fibrantObjectSemantics (u := u))
  semanticsNotOrderReflecting :
    ¬ (∀ P Q : GeneratedScaledAnodynePresentation.{u},
      fibrantObjectSemantics Q ⊆ fibrantObjectSemantics P → P ≤ Q)

/-- The v1.120 non-faithfulness certificate is inhabited unconditionally. -/
def terminalFibrancyNonfaithfulPresentationOrder :
    TerminalFibrancyNonfaithfulPresentationOrder.{u} where
  upperRightClassIntersection := generatedFibrationClass_upperEnvelope
  terminalCollapse := upperEnvelope_isFibrant_iff_canonical
  strictPresentationGap := canonicalKuuOS_lt_upperEnvelope
  semanticEquality := fibrantObjectSemantics_canonical_eq_upperEnvelope
  semanticsNotInjective := fibrantObjectSemantics_not_injective
  semanticsNotOrderReflecting := fibrantObjectSemantics_not_orderReflecting

/-! ## Final theorem surface -/

/-- Presentation inequality need not survive passage to terminal semantics:
there are distinct, strictly ordered generated presentations with exactly the
same fibrant objects. -/
theorem presentationOrder_not_detected_by_terminalFibrancy :
    ∃ P Q : GeneratedScaledAnodynePresentation.{u},
      P < Q ∧
      (∀ X : ScaledSSet.{u}, isFibrant X P ↔ isFibrant X Q) := by
  exact ⟨canonicalKuuOSPresentation, standardCanonicalUpperEnvelope,
    canonicalKuuOS_lt_upperEnvelope,
    fun X => (upperEnvelope_isFibrant_iff_canonical X).symm⟩

/-!
The resulting semantic picture is exact:

```text
presentation lattice:
  C < U = S ⊔ C

full right classes:
  R_U = R_S ∩ R_C

terminal maps:
  Fib_C ⊆ Fib_S,
  therefore Fib_U = Fib_C.
```

Hence the assignment

```text
P |-> { X | X is P-fibrant }
```

forgets genuine presentation-level information.  It is antitone, but it is
neither injective nor order-reflecting.  The strict standard/canonical
orthogonality diamond of v1.119 therefore coexists with an exact collapse of
one of its upper edges after restriction to terminal maps.
-/

end

end KUOS.DependentOriginationTerminalFibrancyNonfaithfulPresentationOrderV1_120
