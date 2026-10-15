import Mathlib
import KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7

namespace KUOS.DependentOriginationRelationalFeedbackSemanticsV0_1

open KUOS.DependentOriginationHistorySensitiveTransportV0_5

/-!
# Relational feedback semantics v0.1

This file extracts the useful structural content of an external relational-field
behavioral surrogate into the non-quantum dependent-origination layer.

The imported ideas are structural only:

* body, episodic memory, structural memory, and relation are distinct context
  coordinates;
* the present self-state is a derived readout of context, not an independently
  stored causal scalar;
* one encounter follows observation -> evidence -> unresolved difference -> gate
  -> action -> feedback;
* feedback changes the context used by future encounters;
* high uncertainty may be constrained to a reversible probe by an explicit
  policy certificate;
* repeated encounters form an exact finite-history transport.

No numerical coefficients, psychological validity claim, clinical claim, hidden
model-state claim, or comparison against an official KuuOS runtime is imported.
-/

/--
Context coordinates kept separate so sensitivity to body, episodic memory,
structural memory, and relation can be stated without collapsing them into one
scalar state.
-/
structure RelationalContext
    (Body EpisodeMemory StructuralMemory Relation : Type*) where
  body : Body
  episodeMemory : EpisodeMemory
  structuralMemory : StructuralMemory
  relation : Relation

/-- A closed-loop encounter supplies an external stimulus and the later outcome. -/
abbrev Encounter (Stimulus Outcome : Type*) := Stimulus × Outcome

/--
The complete readout of the feed-forward part of one encounter before feedback.
`current` is deliberately derived from context by the system below.
-/
structure RelationalSnapshot
    (INow Observation Evidence Delta Gate Action : Type*) where
  current : INow
  observation : Observation
  evidence : Evidence
  unresolved : Delta
  gate : Gate
  action : Action

section

variable
    {Body EpisodeMemory StructuralMemory Relation : Type*}
    {Stimulus INow Observation Evidence Delta Gate Action Outcome : Type*}

abbrev Context :=
  RelationalContext Body EpisodeMemory StructuralMemory Relation

/--
Abstract relational closed-loop semantics.

The important causal choice is that `observe` receives the derived `INow` value.
Thus a theorem claiming that feedback changes the next response must expose the
condition under which feedback changes `currentSelf`; the present-state readout
cannot remain epiphenomenal.
-/
structure RelationalFeedbackSystem where
  currentSelf : Context → INow
  observe : Stimulus → INow → Observation
  evidence : Stimulus → Observation → Evidence
  unresolved : Stimulus → Observation → Evidence → Delta
  gate : INow → Observation → Evidence → Delta → Gate
  selectAction : Gate → Action
  feedback :
    Context → Stimulus → Observation → Evidence → Delta → Gate → Action →
      Outcome → Context

namespace RelationalFeedbackSystem

variable (S : RelationalFeedbackSystem
  (Body := Body)
  (EpisodeMemory := EpisodeMemory)
  (StructuralMemory := StructuralMemory)
  (Relation := Relation)
  (Stimulus := Stimulus)
  (INow := INow)
  (Observation := Observation)
  (Evidence := Evidence)
  (Delta := Delta)
  (Gate := Gate)
  (Action := Action)
  (Outcome := Outcome))

/-- Evaluate the observation/evidence/gate/action portion of one encounter. -/
def evaluate (stimulus : Stimulus) (context : Context) :
    RelationalSnapshot INow Observation Evidence Delta Gate Action :=
  let current := S.currentSelf context
  let observation := S.observe stimulus current
  let evidence := S.evidence stimulus observation
  let unresolved := S.unresolved stimulus observation evidence
  let gate := S.gate current observation evidence unresolved
  let action := S.selectAction gate
  {
    current := current
    observation := observation
    evidence := evidence
    unresolved := unresolved
    gate := gate
    action := action
  }

/-- Observable response to one stimulus at the present relational context. -/
def response (stimulus : Stimulus) (context : Context) : Observation :=
  S.observe stimulus (S.currentSelf context)

/--
One closed-loop encounter: evaluate the present context, select an action, then
feed the observed outcome back into the next context.
-/
def step (stimulus : Stimulus) (outcome : Outcome) (context : Context) : Context :=
  let snapshot := S.evaluate stimulus context
  S.feedback context stimulus snapshot.observation snapshot.evidence
    snapshot.unresolved snapshot.gate snapshot.action outcome

/-- Event form of `step`, suitable for the existing finite-history transport. -/
def encounterStep : Encounter Stimulus Outcome → Context → Context :=
  fun encounter context => S.step encounter.1 encounter.2 context

/--
The relational feedback loop is an ordinary KuuOS finite-history transport on
its full context carrier.
-/
def toHistoryTransport : HistoryTransport (Encounter Stimulus Outcome) Context :=
  HistoryTransport.ofSingleEventTransport S.encounterStep

@[simp] theorem toHistoryTransport_eval_singleton
    (stimulus : Stimulus) (outcome : Outcome) (context : Context) :
    S.toHistoryTransport.eval [(stimulus, outcome)] context =
      S.step stimulus outcome context :=
  rfl

/-- Exact trajectory composition inherited from the free history transport. -/
theorem history_eval_append
    (left right : List (Encounter Stimulus Outcome))
    (context : Context) :
    S.toHistoryTransport.eval (left ++ right) context =
      S.toHistoryTransport.eval left
        (S.toHistoryTransport.eval right context) :=
  S.toHistoryTransport.eval_append_apply left right context

/-- Derived present-state readout after a finite encounter history. -/
def currentSelfAfterHistory
    (word : List (Encounter Stimulus Outcome))
    (initial : Context) : INow :=
  S.currentSelf (S.toHistoryTransport.eval word initial)

/-- Response to a new stimulus after a finite encounter history. -/
def responseAfterHistory
    (word : List (Encounter Stimulus Outcome))
    (initial : Context)
    (stimulus : Stimulus) : Observation :=
  S.response stimulus (S.toHistoryTransport.eval word initial)

/--
History splitting for future response: the right history prepares the context
on which the left history and the new readout depend.
-/
theorem responseAfterHistory_append
    (left right : List (Encounter Stimulus Outcome))
    (initial : Context)
    (stimulus : Stimulus) :
    S.responseAfterHistory (left ++ right) initial stimulus =
      S.responseAfterHistory left
        (S.toHistoryTransport.eval right initial) stimulus := by
  unfold responseAfterHistory
  rw [S.toHistoryTransport.eval_append_apply]

/-- Contexts differing only in body, with the other coordinates fixed. -/
def SameExceptBody (left right : Context) : Prop :=
  left.episodeMemory = right.episodeMemory ∧
  left.structuralMemory = right.structuralMemory ∧
  left.relation = right.relation ∧
  left.body ≠ right.body

/-- Contexts differing only in episodic memory. -/
def SameExceptEpisodeMemory (left right : Context) : Prop :=
  left.body = right.body ∧
  left.structuralMemory = right.structuralMemory ∧
  left.relation = right.relation ∧
  left.episodeMemory ≠ right.episodeMemory

/-- Contexts differing only in structural memory. -/
def SameExceptStructuralMemory (left right : Context) : Prop :=
  left.body = right.body ∧
  left.episodeMemory = right.episodeMemory ∧
  left.relation = right.relation ∧
  left.structuralMemory ≠ right.structuralMemory

/-- Contexts differing only in the relation coordinate. -/
def SameExceptRelation (left right : Context) : Prop :=
  left.body = right.body ∧
  left.episodeMemory = right.episodeMemory ∧
  left.structuralMemory = right.structuralMemory ∧
  left.relation ≠ right.relation

/--
A coordinate relation is causally visible at the present-self layer when two
related contexts produce different derived present states.
-/
def CurrentSelfSensitiveAlong (R : Context → Context → Prop) : Prop :=
  ∃ left right : Context,
    R left right ∧ S.currentSelf left ≠ S.currentSelf right

/--
If the observation map for a fixed stimulus separates present states, every
present-self sensitivity witness becomes a same-stimulus response witness.
-/
theorem response_sensitive_along
    (R : Context → Context → Prop)
    (hSensitive : S.CurrentSelfSensitiveAlong R)
    (stimulus : Stimulus)
    (hObserve : Function.Injective (S.observe stimulus)) :
    ∃ left right : Context,
      R left right ∧
        S.response stimulus left ≠ S.response stimulus right := by
  rcases hSensitive with ⟨left, right, hR, hCurrent⟩
  refine ⟨left, right, hR, ?_⟩
  intro hResponse
  apply hCurrent
  apply hObserve
  simpa [response] using hResponse

/--
A genuine feedback-induced change of the derived present state changes the next
response to the same fixed stimulus whenever that observation map is injective.

This is the theorem-level replacement for merely recording two different
`I_now` numbers in a behavioral surrogate.
-/
theorem response_changes_after_step_of_currentSelf_changes
    (previousStimulus nextStimulus : Stimulus)
    (outcome : Outcome)
    (context : Context)
    (hCurrent :
      S.currentSelf (S.step previousStimulus outcome context) ≠
        S.currentSelf context)
    (hObserve : Function.Injective (S.observe nextStimulus)) :
    S.response nextStimulus (S.step previousStimulus outcome context) ≠
      S.response nextStimulus context := by
  intro hResponse
  apply hCurrent
  apply hObserve
  simpa [response] using hResponse

/--
Policy-level certificate for the Middle-Way pattern
`high uncertainty -> probe -> reversible action`.

The uncertainty predicate, probe predicate, and reversibility predicate remain
abstract.  No arbitrary numeric threshold is promoted into KuuOS semantics.
-/
structure ReversibleProbePolicy
    (HighUncertainty : Delta → Prop)
    (Probe Reversible : Action → Prop) where
  selectedProbe : ∀ stimulus context,
    HighUncertainty (S.evaluate stimulus context).unresolved →
      Probe (S.evaluate stimulus context).action
  probeReversible : ∀ action, Probe action → Reversible action

namespace ReversibleProbePolicy

variable
    {HighUncertainty : Delta → Prop}
    {Probe Reversible : Action → Prop}
    (P : S.ReversibleProbePolicy HighUncertainty Probe Reversible)

/-- High uncertainty therefore certifies reversibility of the selected action. -/
theorem selectedAction_reversible_of_highUncertainty
    (stimulus : Stimulus)
    (context : Context)
    (h : HighUncertainty (S.evaluate stimulus context).unresolved) :
    Reversible (S.evaluate stimulus context).action :=
  P.probeReversible _ (P.selectedProbe stimulus context h)

end ReversibleProbePolicy

end RelationalFeedbackSystem

end

end KUOS.DependentOriginationRelationalFeedbackSemanticsV0_1
