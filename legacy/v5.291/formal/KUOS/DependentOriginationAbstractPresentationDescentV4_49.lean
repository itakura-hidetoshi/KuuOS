import KUOS.DependentOriginationStageIIOrbitOrientationDescentV4_48
import Mathlib

namespace KUOS.DependentOriginationAbstractPresentationDescentV4_49

open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
open KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
open KUOS.DependentOriginationStageIIGeometricOrientationV4_46
open KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47
open KUOS.DependentOriginationStageIIOrbitOrientationDescentV4_48

set_option autoImplicit false

noncomputable section

/-!
# Abstract presentation descent for dependent origination v4.49

The v4.4x geometric program produced a concrete pattern:

* many representatives;
* an explicit presentation relation;
* a quotient/orbit carrier;
* semantic data that may or may not descend;
* an obstruction exactly when related presentations receive unequal values.

This file removes every geometric and Stage-II-specific ingredient from the
core theorem.

Let P be any type of presentations and S any Setoid on P.  For any semantic
map

  semantic : P → Y

define:

* presentation invariance:
    related presentations have equal semantics;

* quotient factorization:
    semantic factors through Quotient S;

* descent obstruction:
    two S-related presentations have unequal semantics.

The main universal theorem is

  factorization through Quotient S
    ↔ presentation invariance,

with uniqueness of the descended semantic.  The exact obstruction theorem is

  no factorization
    ↔ there exists a related pair with unequal semantics.

This is the first theorem unit after the geometric detour whose primary
statements are presentation-general.  The Stage-II orbit is retained only as a
specialization proving that v4.48 is an instance of the general descent law.
-/

universe u v

variable {Presentation : Type u} {Semantic : Type v}

/-- A semantic map is presentation-invariant when it gives equal values to
all representatives identified by the chosen presentation setoid. -/
def IsPresentationInvariant
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic) : Prop :=
  ∀ p q : Presentation, S.r p q → semantic p = semantic q

/-- Existence of a semantic factorization through the quotient of
presentations. -/
def HasPresentationQuotientFactorization
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic) : Prop :=
  ∃ quotientSemantic : Quotient S → Semantic,
    ∀ p : Presentation,
      quotientSemantic (Quotient.mk S p) = semantic p

/-- A concrete descent obstruction is a related pair of presentations carrying
different semantic values. -/
def HasPresentationDescentObstruction
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic) : Prop :=
  ∃ p q : Presentation,
    S.r p q ∧ semantic p ≠ semantic q

/-- Canonical descent of an invariant semantic map to the presentation
quotient. -/
def presentationDescend
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hInvariant : IsPresentationInvariant S semantic) :
    Quotient S → Semantic :=
  Quotient.lift semantic (by
    intro p q hpq
    exact hInvariant p q hpq)

/-- The canonical descended semantic recovers the original value on every
presentation representative. -/
@[simp] theorem presentationDescend_mk
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hInvariant : IsPresentationInvariant S semantic)
    (p : Presentation) :
    presentationDescend S semantic hInvariant (Quotient.mk S p) =
      semantic p := by
  rfl

/-- Any presentation-invariant semantic map has a quotient factorization. -/
theorem hasPresentationQuotientFactorization_of_invariant
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hInvariant : IsPresentationInvariant S semantic) :
    HasPresentationQuotientFactorization S semantic := by
  exact
    ⟨presentationDescend S semantic hInvariant,
      by intro p; rfl⟩

/-- Conversely, any quotient factorization forces presentation invariance. -/
theorem isPresentationInvariant_of_factorization
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hFactor : HasPresentationQuotientFactorization S semantic) :
    IsPresentationInvariant S semantic := by
  rcases hFactor with ⟨quotientSemantic, hquot⟩
  intro p q hpq
  have hclass :
      Quotient.mk S p = Quotient.mk S q :=
    Quotient.sound hpq
  calc
    semantic p = quotientSemantic (Quotient.mk S p) := (hquot p).symm
    _ = quotientSemantic (Quotient.mk S q) := congrArg quotientSemantic hclass
    _ = semantic q := hquot q

/-- Fundamental 0-level dependent-origination descent law:
factorization through the quotient is equivalent to presentation invariance. -/
theorem presentationQuotientFactorization_iff_invariant
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic) :
    HasPresentationQuotientFactorization S semantic ↔
      IsPresentationInvariant S semantic := by
  constructor
  · exact isPresentationInvariant_of_factorization S semantic
  · exact hasPresentationQuotientFactorization_of_invariant S semantic

/-- The canonical quotient semantic is unique among all maps agreeing with the
original semantic on representatives. -/
theorem presentationDescend_unique
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hInvariant : IsPresentationInvariant S semantic)
    (candidate : Quotient S → Semantic)
    (hcandidate :
      ∀ p : Presentation,
        candidate (Quotient.mk S p) = semantic p) :
    candidate = presentationDescend S semantic hInvariant := by
  funext q
  refine Quotient.inductionOn q ?_
  intro p
  change
    candidate (Quotient.mk S p) =
      presentationDescend S semantic hInvariant (Quotient.mk S p)
  rw [hcandidate]
  rfl

/-- Invariant semantics have one unique descended quotient semantic. -/
theorem existsUnique_presentationQuotientSemantic_of_invariant
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hInvariant : IsPresentationInvariant S semantic) :
    ∃! quotientSemantic : Quotient S → Semantic,
      ∀ p : Presentation,
        quotientSemantic (Quotient.mk S p) = semantic p := by
  refine
    ⟨presentationDescend S semantic hInvariant, ?_, ?_⟩
  · intro p
    rfl
  · intro candidate hcandidate
    exact presentationDescend_unique S semantic hInvariant candidate hcandidate

/-- Any explicit related unequal pair obstructs quotient factorization. -/
theorem noPresentationQuotientFactorization_of_obstruction
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hObstruction : HasPresentationDescentObstruction S semantic) :
    ¬ HasPresentationQuotientFactorization S semantic := by
  rintro ⟨quotientSemantic, hquot⟩
  rcases hObstruction with ⟨p, q, hpq, hneq⟩
  apply hneq
  have hclass :
      Quotient.mk S p = Quotient.mk S q :=
    Quotient.sound hpq
  calc
    semantic p = quotientSemantic (Quotient.mk S p) := (hquot p).symm
    _ = quotientSemantic (Quotient.mk S q) := congrArg quotientSemantic hclass
    _ = semantic q := hquot q

/-- Failure of quotient factorization produces an explicit related pair with
unequal semantic values. -/
theorem obstruction_of_noPresentationQuotientFactorization
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic)
    (hNoFactor : ¬ HasPresentationQuotientFactorization S semantic) :
    HasPresentationDescentObstruction S semantic := by
  classical
  by_contra hNoObstruction
  apply hNoFactor
  apply hasPresentationQuotientFactorization_of_invariant S semantic
  intro p q hpq
  by_contra hneq
  exact hNoObstruction ⟨p, q, hpq, hneq⟩

/-- Exact obstruction criterion:
a semantic map fails to descend iff some identified presentations carry
different values. -/
theorem noPresentationQuotientFactorization_iff_obstruction
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic) :
    (¬ HasPresentationQuotientFactorization S semantic) ↔
      HasPresentationDescentObstruction S semantic := by
  constructor
  · exact obstruction_of_noPresentationQuotientFactorization S semantic
  · exact noPresentationQuotientFactorization_of_obstruction S semantic

/-- Equivalent exact criterion stated positively. -/
theorem noPresentationDescentObstruction_iff_factorization
    (S : Setoid Presentation)
    (semantic : Presentation → Semantic) :
    (¬ HasPresentationDescentObstruction S semantic) ↔
      HasPresentationQuotientFactorization S semantic := by
  constructor
  · intro hNoObstruction
    apply hasPresentationQuotientFactorization_of_invariant S semantic
    intro p q hpq
    by_contra hneq
    exact hNoObstruction ⟨p, q, hpq, hneq⟩
  · intro hFactor hObstruction
    exact
      noPresentationQuotientFactorization_of_obstruction
        S semantic hObstruction hFactor

/-!
## Stage-II specialization

The following theorems are not part of the abstract statement.  They verify
that the concrete geometric orbit developed in v4.47-v4.48 is one exact
instance of the presentation-general law above.
-/

/-- The middle-switch setoid is now viewed simply as one presentation setoid. -/
abbrev stageIIGeometricPresentationSetoid :
    Setoid StageIIGeometricCantorCarrier :=
  stageIIGeometricMiddleSwitchSetoid

/-- Integer orientation supplies an explicit abstract presentation-descent
obstruction at every finite depth. -/
theorem stageIIIntegerOrientation_has_abstractPresentationObstruction
    (depth : Nat) :
    HasPresentationDescentObstruction
      stageIIGeometricPresentationSetoid
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationIntCoeff p depth) := by
  rcases XInfinityGeometricFractal_nonempty with ⟨z, hz⟩
  let p : StageIIGeometricCantorCarrier := ⟨z, hz⟩
  refine
    ⟨p, stageIIGeometricCarrierMiddleSwitch p, ?_, ?_⟩
  · exact Or.inr rfl
  · exact
      (stageIIGeometricCarrierOrientationIntCoeff_middleSwitch_ne
        p depth).symm

/-- The abstract obstruction theorem reproduces the concrete non-descent of
integer orientation from v4.48. -/
theorem stageIIIntegerOrientation_no_factorization_from_abstractDescent
    (depth : Nat) :
    ¬ HasPresentationQuotientFactorization
      stageIIGeometricPresentationSetoid
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationIntCoeff p depth) := by
  exact
    noPresentationQuotientFactorization_of_obstruction
      stageIIGeometricPresentationSetoid
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationIntCoeff p depth)
      (stageIIIntegerOrientation_has_abstractPresentationObstruction depth)

/-- Mod-two orientation is presentation-invariant in the general sense. -/
theorem stageIIModTwoOrientation_is_abstractPresentationInvariant
    (depth : Nat) :
    IsPresentationInvariant
      stageIIGeometricPresentationSetoid
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationModTwo p depth) := by
  intro p q hpq
  rcases hpq with hpq | hpq
  · rw [hpq]
  · rw [hpq]
    exact
      (stageIIGeometricCarrierOrientationModTwo_invariant depth p).symm

/-- Therefore the generic universal descent theorem gives the unique mod-two
orbit semantic, independently of the Stage-II-specific quotient proof. -/
theorem stageIIModTwoOrientation_existsUnique_abstractPresentationDescent
    (depth : Nat) :
    ∃! quotientSemantic :
        Quotient stageIIGeometricPresentationSetoid → ZMod 2,
      ∀ p : StageIIGeometricCantorCarrier,
        quotientSemantic
            (Quotient.mk stageIIGeometricPresentationSetoid p) =
          stageIIGeometricCarrierOrientationModTwo p depth := by
  exact
    existsUnique_presentationQuotientSemantic_of_invariant
      stageIIGeometricPresentationSetoid
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationModTwo p depth)
      (stageIIModTwoOrientation_is_abstractPresentationInvariant depth)

/-!
## Boundary after v4.49

The formal spine has now returned from one concrete geometric realization to a
presentation-general dependent-origination statement.

The primary theorem no longer mentions Stage-II, Cantor geometry, truncated
icosahedra, or middle-switches:

  semantic factors through presentation quotient
    <-> semantic is invariant under presentation change,

and

  semantic fails to factor
    <-> there is an identified pair of presentations with unequal semantics.

This gives an exact 0-level universal property and an exact obstruction
criterion for arbitrary presentation systems.

The Stage-II construction now serves as a certified instance rather than the
definition of the general theory.

The next theorem unit should categorify this interface: replace
Presentation -> Semantic by Cat-valued higher contextual systems and connect
the abstract presentation-invariance/descent pattern to
HigherLocalizationFactorization, stack descent, and the long-range
Dependent Origination universality program.
-/

end

end KUOS.DependentOriginationAbstractPresentationDescentV4_49
