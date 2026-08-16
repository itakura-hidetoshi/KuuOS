import Mathlib
import KUOS.Architecture.QiWuxingGenerationControlCoherenceV2_6

/-!
# Qi Wuxing relation-word protected history v2.7

This additive layer lifts the v2.6 single-relation shifts to finite words of
Wuxing relations.  The phase coordinate and protected-history event count are
kept separate throughout.

The central result is structural: every relation contributes exactly one
protected-history event.  Therefore a nonempty relation word can be closed in
the `ZMod 5` phase projection while still having a nonzero protected shift.
Phase cancellation does not erase relational history.

This is a finite algebraic statement about the KuuOS architecture model.  It
does not identify classical Wuxing with a physical gauge theory, does not turn
history count into Qi quantity, and grants no clinical, execution, WORLD, or
external theorem authority.
-/

namespace KUOS.Architecture

/-- A finite compositional word of canonical v2.6 Wuxing relations. -/
abbrev WuxingRelationWord := List WuxingRelation

/-- Total protected shift of a finite relation word. -/
def relationWordShift : WuxingRelationWord → WuxingShift
  | [] => 0
  | relation :: rest => relationShift relation + relationWordShift rest

@[simp] theorem relationWordShift_nil : relationWordShift [] = 0 := rfl

@[simp] theorem relationWordShift_cons
    (relation : WuxingRelation) (rest : WuxingRelationWord) :
    relationWordShift (relation :: rest) =
      relationShift relation + relationWordShift rest := rfl

/-- Each canonical relation contributes exactly one protected-history event. -/
@[simp] theorem relationShift_history_event
    (relation : WuxingRelation) :
    (relationShift relation).2 = 1 := by
  cases relation <;> rfl

/-- Concatenation of relation words is sent to addition of protected shifts. -/
@[simp] theorem relationWordShift_append
    (first second : WuxingRelationWord) :
    relationWordShift (first ++ second) =
      relationWordShift first + relationWordShift second := by
  induction first with
  | nil =>
      simp [relationWordShift]
  | cons relation rest ih =>
      simp [relationWordShift, ih, add_assoc]

/-- The protected-history coordinate of a word shift is exactly word length. -/
@[simp] theorem relationWordShift_history_count
    (word : WuxingRelationWord) :
    (relationWordShift word).2 = word.length := by
  induction word with
  | nil =>
      simp [relationWordShift]
  | cons relation rest ih =>
      cases relation <;>
        simp [relationWordShift, relationShift, ih, Nat.add_comm]

/-- Execute a finite relation word in temporal order. -/
def applyRelationWord :
    WuxingRelationWord → WuxingFibonacciState → WuxingFibonacciState
  | [], state => state
  | relation :: rest, state =>
      applyRelationWord rest (applyShift (relationShift relation) state)

/-- Finite word execution is exactly the v2.6 action of its total shift. -/
theorem applyRelationWord_eq_applyShift
    (word : WuxingRelationWord) (state : WuxingFibonacciState) :
    applyRelationWord word state = applyShift (relationWordShift word) state := by
  induction word generalizing state with
  | nil =>
      simp [applyRelationWord, relationWordShift, applyShift]
  | cons relation rest ih =>
      simp only [applyRelationWord, relationWordShift_cons]
      rw [ih]
      exact
        (applyShift_add
          (relationShift relation) (relationWordShift rest) state).symm

/-- Word concatenation acts by sequential composition. -/
theorem applyRelationWord_append
    (first second : WuxingRelationWord) (state : WuxingFibonacciState) :
    applyRelationWord (first ++ second) state =
      applyRelationWord second (applyRelationWord first state) := by
  induction first generalizing state with
  | nil =>
      simp [applyRelationWord]
  | cons relation rest ih =>
      simp [applyRelationWord, ih]

/-- A finite word advances protected history by exactly its number of events. -/
theorem applyRelationWord_history
    (word : WuxingRelationWord) (state : WuxingFibonacciState) :
    (applyRelationWord word state).history =
      advanceHistoryN word.length state.history := by
  rw [applyRelationWord_eq_applyShift]
  simp [applyShift]

/-- The phase endpoint is the initial phase plus the projected word shift. -/
theorem applyRelationWord_phase
    (word : WuxingRelationWord) (state : WuxingFibonacciState) :
    (applyRelationWord word state).phase =
      state.phase + (relationWordShift word).1 := by
  rw [applyRelationWord_eq_applyShift]
  rfl

/-- A word is phase-closed when its total `ZMod 5` displacement vanishes. -/
def PhaseClosedWord (word : WuxingRelationWord) : Prop :=
  (relationWordShift word).1 = 0

/-- A phase-closed word returns the phase coordinate. -/
theorem phaseClosedWord_phase_returns
    (word : WuxingRelationWord) (state : WuxingFibonacciState)
    (hclosed : PhaseClosedWord word) :
    (applyRelationWord word state).phase = state.phase := by
  change (relationWordShift word).1 = 0 at hclosed
  rw [applyRelationWord_phase, hclosed]
  simp

/-- Any nonempty finite relation word has a nonzero protected shift. -/
theorem relationWordShift_ne_zero_of_nonempty
    (word : WuxingRelationWord) (hword : word ≠ []) :
    relationWordShift word ≠ 0 := by
  cases word with
  | nil =>
      exact (hword rfl).elim
  | cons relation rest =>
      intro hzero
      have hcount :
          (relationWordShift (relation :: rest)).2 = 0 := by
        exact congrArg Prod.snd hzero
      simp at hcount

/-- A nonempty phase-closed word has zero phase displacement but positive
protected-history event count, hence is not the zero protected shift. -/
theorem phaseClosedWord_has_protected_residue
    (word : WuxingRelationWord)
    (hclosed : PhaseClosedWord word)
    (hword : word ≠ []) :
    (relationWordShift word).1 = 0 ∧
      0 < (relationWordShift word).2 ∧
      relationWordShift word ≠ 0 := by
  change (relationWordShift word).1 = 0 at hclosed
  constructor
  · exact hclosed
  constructor
  · rw [relationWordShift_history_count]
    cases word with
    | nil =>
        exact (hword rfl).elim
    | cons relation rest =>
        simp
  · exact relationWordShift_ne_zero_of_nonempty word hword

/-- Different word lengths force distinct protected shifts. -/
theorem relationWordShift_ne_of_length_ne
    (first second : WuxingRelationWord)
    (hlength : first.length ≠ second.length) :
    relationWordShift first ≠ relationWordShift second := by
  intro hshift
  have hcount :
      (relationWordShift first).2 = (relationWordShift second).2 := by
    exact congrArg Prod.snd hshift
  rw [relationWordShift_history_count, relationWordShift_history_count] at hcount
  exact hlength hcount

/-- If two words share a phase endpoint but have different lengths, phase
projection has forgotten protected-history information. -/
theorem same_phase_distinct_protected_shift_of_length_ne
    (first second : WuxingRelationWord)
    (hphase : (relationWordShift first).1 = (relationWordShift second).1)
    (hlength : first.length ≠ second.length) :
    (relationWordShift first).1 = (relationWordShift second).1 ∧
      relationWordShift first ≠ relationWordShift second := by
  exact ⟨hphase, relationWordShift_ne_of_length_ne first second hlength⟩

/-- The canonical control-then-insult word is phase-closed. -/
@[simp] theorem control_insult_word_phase_closed :
    PhaseClosedWord [.control, .insult] := by
  simp [PhaseClosedWord, relationWordShift, relationShift]

/-- The same phase-closed word still carries two protected-history events. -/
@[simp] theorem control_insult_word_history_count :
    (relationWordShift [.control, .insult]).2 = 2 := by
  simp [relationWordShift, relationShift]

/-- Control followed by insult is not the zero protected shift. -/
theorem control_insult_word_shift_ne_zero :
    relationWordShift [.control, .insult] ≠ 0 := by
  exact relationWordShift_ne_zero_of_nonempty [.control, .insult] (by simp)

/-- The control-insult loop returns phase while advancing protected history by
two events. -/
theorem control_insult_word_phase_returns_history_advances
    (state : WuxingFibonacciState) :
    (applyRelationWord [.control, .insult] state).phase = state.phase ∧
      (applyRelationWord [.control, .insult] state).history =
        advanceHistoryN 2 state.history := by
  constructor
  · exact phaseClosedWord_phase_returns
      [.control, .insult] state control_insult_word_phase_closed
  · exact applyRelationWord_history [.control, .insult] state

/-- One control event and two generation events agree after phase projection
but remain distinct protected shifts because their event counts differ. -/
theorem control_word_two_generations_same_phase_distinct_shift :
    (relationWordShift [.control]).1 =
        (relationWordShift [.generation, .generation]).1 ∧
      relationWordShift [.control] ≠
        relationWordShift [.generation, .generation] := by
  apply same_phase_distinct_protected_shift_of_length_ne
  · native_decide
  · decide

end KUOS.Architecture
