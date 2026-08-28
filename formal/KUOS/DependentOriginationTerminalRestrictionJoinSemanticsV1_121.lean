import KUOS.DependentOriginationTerminalFibrancyNonfaithfulPresentationOrderV1_120
import Mathlib.Order.CompleteLattice.Lemmas

namespace KUOS.DependentOriginationTerminalRestrictionJoinSemanticsV1_121

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85
open KUOS.DependentOriginationGeneratedPresentationCompleteLatticeV1_86
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
open KUOS.DependentOriginationStandardCanonicalOrthogonalityDiamondV1_119
open KUOS.DependentOriginationTerminalFibrancyNonfaithfulPresentationOrderV1_120

universe u

noncomputable section

/-!
# Terminal restriction and join semantics v1.121

Version v1.120 exhibits the first concrete loss of information after passing
from a generated presentation to its fibrant objects:

```text
C < U = S ⊔ C,
but Fib_C = Fib_U.
```

The present file locates that loss exactly.  Before restricting to terminal
maps, the generated right class is a faithful coordinate: v1.83-v1.85 identify
presentation order with reverse inclusion of the saturated right class.  The
forgetful step is therefore the restriction

```text
R |-> { X | R (X -> *) }.
```

We name this map and factor fibrant-object semantics through it.  We then prove
that the restriction itself is neither injective nor order-reflecting, using
the v1.120 canonical/upper-envelope pair as the witness.

The second half extracts the general lattice mechanism behind v1.120.  For
arbitrary generated presentations `P,Q`,

```text
R_(P ⊔ Q) = R_P ∩ R_Q
```

and therefore

```text
Fib_(P ⊔ Q)(X) <-> Fib_P(X) and Fib_Q(X).
```

Hence whenever `Q`-fibrancy implies `P`-fibrancy, the join is absorbed on
terminal semantics:

```text
Fib_(P ⊔ Q) = Fib_Q.
```

Thus the standard/canonical collapse is an instance of a general theorem, not
an accidental property of those two presentations.
-/

/-! ## Full right semantics and terminal restriction -/

/-- The full generated-right morphism semantics of a presentation.  Unlike
terminal fibrant-object semantics, this coordinate is faithful. -/
def fullRightSemantics
    (P : GeneratedScaledAnodynePresentation.{u}) :
    MorphismProperty (ScaledSSet.{u}) :=
  generatedFibrationClass P

/-- Restrict an arbitrary morphism property to terminal maps.  This is exactly
the operation which forgets all nonterminal lifting information. -/
def terminalRestriction
    (R : MorphismProperty (ScaledSSet.{u})) : Set (ScaledSSet.{u}) :=
  {X | R (ScaledSSet.toPoint X)}

/-- The full right coordinate is right-orthogonally saturated, so it really
lands in the fixed-point carrier of v1.85. -/
theorem fullRightSemantics_isRightOrthogonallySaturated
    (P : GeneratedScaledAnodynePresentation.{u}) :
    IsRightOrthogonallySaturated (fullRightSemantics P) := by
  exact generatedFibrationClass_isRightOrthogonallySaturated P

/-- The v1.85 order isomorphism has `fullRightSemantics` as its underlying
morphism property. -/
@[simp]
theorem presentationToSaturatedFibration_val_eq_fullRightSemantics
    (P : GeneratedScaledAnodynePresentation.{u}) :
    (presentationToSaturatedFibration P).1 = fullRightSemantics P :=
  rfl

/-- Equality of full right semantics is exactly equality of generated
presentations. -/
@[simp]
theorem fullRightSemantics_eq_iff
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    fullRightSemantics P = fullRightSemantics Q ↔ P = Q := by
  exact (eq_iff_generatedFibrationClass_eq P Q).symm

/-- In particular the full right semantic coordinate is injective. -/
theorem fullRightSemantics_injective :
    Function.Injective (fullRightSemantics (u := u)) := by
  intro P Q h
  exact (fullRightSemantics_eq_iff P Q).1 h

/-- Presentation order is reflected exactly as reverse inclusion of the full
right semantic coordinate. -/
@[simp]
theorem le_iff_fullRightSemantics_reverse_le
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    P ≤ Q ↔ fullRightSemantics Q ≤ fullRightSemantics P := by
  exact le_iff_generatedFibrationClass_reverse_le P Q

/-- Membership after terminal restriction is exactly quotient-level fibrancy. -/
@[simp]
theorem terminalRestriction_fullRightSemantics_mem_iff
    (P : GeneratedScaledAnodynePresentation.{u})
    (X : ScaledSSet.{u}) :
    X ∈ terminalRestriction (fullRightSemantics P) ↔ isFibrant X P := by
  change
    generatedFibrationClass P (ScaledSSet.toPoint X) ↔ isFibrant X P
  exact (isFibrant_iff X P).symm

/-- The v1.120 fibrant-object semantics factors exactly through the full right
class followed by terminal restriction. -/
theorem fibrantObjectSemantics_eq_terminalRestriction_fullRightSemantics
    (P : GeneratedScaledAnodynePresentation.{u}) :
    fibrantObjectSemantics P =
      terminalRestriction (fullRightSemantics P) := by
  ext X
  exact (terminalRestriction_fullRightSemantics_mem_iff P X).symm

/-- Terminal restriction preserves intersections of morphism properties. -/
@[simp]
theorem terminalRestriction_inf
    (R S : MorphismProperty (ScaledSSet.{u})) :
    terminalRestriction (R ⊓ S) =
      terminalRestriction R ∩ terminalRestriction S := by
  ext X
  rfl

/-! ## Generic join semantics -/

/-- Binary specialization of the v1.86 arbitrary-join formula: full right
semantics sends presentation joins to intersections. -/
@[simp]
theorem fullRightSemantics_sup
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    fullRightSemantics (P ⊔ Q) =
      fullRightSemantics P ⊓ fullRightSemantics Q := by
  unfold fullRightSemantics
  rw [sup_eq_iSup]
  rw [generatedFibrationClass_iSup]
  rw [iInf_bool_eq]
  simp

/-- Fibrancy for a binary presentation join is exactly simultaneous fibrancy
for both factors. -/
theorem isFibrant_sup_iff
    (X : ScaledSSet.{u})
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    isFibrant X (P ⊔ Q) ↔ isFibrant X P ∧ isFibrant X Q := by
  rw [isFibrant_iff]
  change
    fullRightSemantics (P ⊔ Q) (ScaledSSet.toPoint X) ↔
      isFibrant X P ∧ isFibrant X Q
  rw [fullRightSemantics_sup]
  change
    (fullRightSemantics P (ScaledSSet.toPoint X) ∧
      fullRightSemantics Q (ScaledSSet.toPoint X)) ↔
        isFibrant X P ∧ isFibrant X Q
  rw [isFibrant_iff, isFibrant_iff]

/-- Set-valued fibrant-object semantics sends presentation joins to literal
set intersection. -/
@[simp]
theorem fibrantObjectSemantics_sup
    (P Q : GeneratedScaledAnodynePresentation.{u}) :
    fibrantObjectSemantics (P ⊔ Q) =
      fibrantObjectSemantics P ∩ fibrantObjectSemantics Q := by
  ext X
  change
    isFibrant X (P ⊔ Q) ↔
      isFibrant X P ∧ isFibrant X Q
  exact isFibrant_sup_iff X P Q

/-- If `Q`-fibrancy semantically implies `P`-fibrancy, then the `P` factor is
redundant after taking the join and restricting to terminal maps. -/
theorem isFibrant_sup_iff_right_of_imp
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (h : ∀ X : ScaledSSet.{u}, isFibrant X Q → isFibrant X P)
    (X : ScaledSSet.{u}) :
    isFibrant X (P ⊔ Q) ↔ isFibrant X Q := by
  rw [isFibrant_sup_iff]
  constructor
  · exact And.right
  · intro hQ
    exact ⟨h X hQ, hQ⟩

/-- Set-level form of terminal join absorption. -/
theorem fibrantObjectSemantics_sup_eq_right_of_subset
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (h : fibrantObjectSemantics Q ⊆ fibrantObjectSemantics P) :
    fibrantObjectSemantics (P ⊔ Q) = fibrantObjectSemantics Q := by
  rw [fibrantObjectSemantics_sup]
  exact Set.inter_eq_right.mpr h

/-- Fibrant-object semantics is antitone in presentation order. -/
theorem fibrantObjectSemantics_antitone
    {P Q : GeneratedScaledAnodynePresentation.{u}}
    (hPQ : P ≤ Q) :
    fibrantObjectSemantics Q ⊆ fibrantObjectSemantics P := by
  intro X hX
  change isFibrant X P
  exact isFibrant_antitone hPQ X hX

/-! ## Locate the information loss exactly at terminal restriction -/

/-- The canonical point and its upper envelope have different full right
semantics.  Faithfulness is still intact before restricting to terminal maps. -/
theorem fullRightSemantics_canonical_ne_upperEnvelope :
    fullRightSemantics
        (canonicalKuuOSPresentation :
          GeneratedScaledAnodynePresentation.{u}) ≠
      fullRightSemantics standardCanonicalUpperEnvelope := by
  intro h
  apply canonicalKuuOSPresentation_ne_upperEnvelope
  exact fullRightSemantics_injective h

/-- Nevertheless terminal restriction identifies those two distinct full right
classes exactly. -/
theorem terminalRestriction_canonical_eq_upperEnvelope :
    terminalRestriction
        (fullRightSemantics
          (canonicalKuuOSPresentation :
            GeneratedScaledAnodynePresentation.{u})) =
      terminalRestriction
        (fullRightSemantics standardCanonicalUpperEnvelope) := by
  calc
    terminalRestriction
        (fullRightSemantics
          (canonicalKuuOSPresentation :
            GeneratedScaledAnodynePresentation.{u})) =
        fibrantObjectSemantics canonicalKuuOSPresentation :=
      (fibrantObjectSemantics_eq_terminalRestriction_fullRightSemantics
        canonicalKuuOSPresentation).symm
    _ = fibrantObjectSemantics standardCanonicalUpperEnvelope :=
      fibrantObjectSemantics_canonical_eq_upperEnvelope
    _ = terminalRestriction
        (fullRightSemantics standardCanonicalUpperEnvelope) :=
      fibrantObjectSemantics_eq_terminalRestriction_fullRightSemantics
        standardCanonicalUpperEnvelope

/-- Terminal restriction itself is non-injective.  Thus the information loss
is not caused by the presentation-to-right-class coordinate, but by forgetting
all nonterminal morphisms. -/
theorem terminalRestriction_not_injective :
    ¬ Function.Injective (terminalRestriction (u := u)) := by
  intro hinj
  apply fullRightSemantics_canonical_ne_upperEnvelope
  exact hinj terminalRestriction_canonical_eq_upperEnvelope

/-- Terminal restriction is also not order-reflecting on arbitrary morphism
properties.  The same canonical/upper-envelope pair gives the obstruction. -/
theorem terminalRestriction_not_orderReflecting :
    ¬ (∀ R S : MorphismProperty (ScaledSSet.{u}),
      terminalRestriction R ⊆ terminalRestriction S → R ≤ S) := by
  intro hreflect
  have hsubset :
      terminalRestriction
          (fullRightSemantics
            (canonicalKuuOSPresentation :
              GeneratedScaledAnodynePresentation.{u})) ⊆
        terminalRestriction
          (fullRightSemantics standardCanonicalUpperEnvelope) := by
    rw [terminalRestriction_canonical_eq_upperEnvelope]
  have hright :
      fullRightSemantics
          (canonicalKuuOSPresentation :
            GeneratedScaledAnodynePresentation.{u}) ≤
        fullRightSemantics standardCanonicalUpperEnvelope :=
    hreflect _ _ hsubset
  have hbad :
      (standardCanonicalUpperEnvelope :
          GeneratedScaledAnodynePresentation.{u}) ≤
        canonicalKuuOSPresentation := by
    exact le_of_generatedFibrationClass_reverse hright
  exact (not_le_of_gt canonicalKuuOS_lt_upperEnvelope) hbad

/-! ## One coherent semantic factorization certificate -/

/-- The complete v1.121 picture: presentations have a faithful full-right
coordinate; fibrant semantics is its terminal restriction; joins become
intersections; and the restriction is the precise non-faithful step. -/
structure TerminalRestrictionJoinSemantics : Prop where
  fullRightFaithful :
    Function.Injective (fullRightSemantics (u := u))
  fullRightOrderReflection :
    ∀ P Q : GeneratedScaledAnodynePresentation.{u},
      P ≤ Q ↔ fullRightSemantics Q ≤ fullRightSemantics P
  factorization :
    ∀ P : GeneratedScaledAnodynePresentation.{u},
      fibrantObjectSemantics P = terminalRestriction (fullRightSemantics P)
  joinRightIntersection :
    ∀ P Q : GeneratedScaledAnodynePresentation.{u},
      fullRightSemantics (P ⊔ Q) =
        fullRightSemantics P ⊓ fullRightSemantics Q
  joinTerminalIntersection :
    ∀ P Q : GeneratedScaledAnodynePresentation.{u},
      fibrantObjectSemantics (P ⊔ Q) =
        fibrantObjectSemantics P ∩ fibrantObjectSemantics Q
  restrictionNotInjective :
    ¬ Function.Injective (terminalRestriction (u := u))
  restrictionNotOrderReflecting :
    ¬ (∀ R S : MorphismProperty (ScaledSSet.{u}),
      terminalRestriction R ⊆ terminalRestriction S → R ≤ S)

/-- The v1.121 semantic factorization certificate is inhabited
unconditionally. -/
def terminalRestrictionJoinSemantics :
    TerminalRestrictionJoinSemantics.{u} where
  fullRightFaithful := fullRightSemantics_injective
  fullRightOrderReflection := le_iff_fullRightSemantics_reverse_le
  factorization :=
    fibrantObjectSemantics_eq_terminalRestriction_fullRightSemantics
  joinRightIntersection := fullRightSemantics_sup
  joinTerminalIntersection := fibrantObjectSemantics_sup
  restrictionNotInjective := terminalRestriction_not_injective
  restrictionNotOrderReflecting := terminalRestriction_not_orderReflecting

/-! ## Final theorem surface -/

/-- There exist distinct full right morphism properties which become equal
exactly after terminal restriction. -/
theorem terminalRestriction_identifies_distinct_fullRightSemantics :
    ∃ R S : MorphismProperty (ScaledSSet.{u}),
      R ≠ S ∧ terminalRestriction R = terminalRestriction S := by
  exact
    ⟨fullRightSemantics canonicalKuuOSPresentation,
      fullRightSemantics standardCanonicalUpperEnvelope,
      fullRightSemantics_canonical_ne_upperEnvelope,
      terminalRestriction_canonical_eq_upperEnvelope⟩

/-- The exact information-flow statement: the full right coordinate remains
faithful, and non-faithfulness appears only after terminal restriction. -/
theorem terminalRestriction_is_information_loss_locus :
    Function.Injective (fullRightSemantics (u := u)) ∧
      (¬ Function.Injective (terminalRestriction (u := u))) ∧
      (∃ R S : MorphismProperty (ScaledSSet.{u}),
        R ≠ S ∧ terminalRestriction R = terminalRestriction S) := by
  exact ⟨fullRightSemantics_injective,
    terminalRestriction_not_injective,
    terminalRestriction_identifies_distinct_fullRightSemantics⟩

/-!
The semantic hierarchy is now explicit:

```text
GeneratedScaledAnodynePresentation
       |
       | faithful, reverse-order full right coordinate
       v
saturated generated right morphism property
       |
       | terminalRestriction
       v
set of fibrant objects.
```

The first arrow loses no information: v1.85 is an order isomorphism onto the
saturated right fixed points.  The second arrow does lose information, as the
canonical point and its strict upper envelope show.

At the same time terminal restriction retains a clean part of the complete
lattice structure:

```text
Fib_(P ⊔ Q) = Fib_P ∩ Fib_Q.
```

This gives a general absorption principle and isolates a natural next question:
which additional lattice structure, especially meet structure, survives after
passing to terminal semantics?
-/

end

end KUOS.DependentOriginationTerminalRestrictionJoinSemanticsV1_121
