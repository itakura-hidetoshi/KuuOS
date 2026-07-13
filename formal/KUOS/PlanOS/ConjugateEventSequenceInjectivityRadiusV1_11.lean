import Mathlib
import KUOS.PlanOS.SecondVariationMorseIndexV1_10

namespace KUOS.PlanOS.ConjugateEventSequenceInjectivityRadiusV1_11

structure ConjugateEvent where
  parameter : ℝ
  multiplicity : ℕ
  morseIndexBefore : ℕ
  morseIndexAfter : ℕ
  nullityAtEvent : ℕ

inductive CutCause where
  | conjugate
  | multipleGeodesic
  deriving DecidableEq, Repr

structure CutLocusCandidate where
  parameter : ℝ
  cause : CutCause
  competingGeodesicCount : ℕ

structure PiecewiseGeodesicSegment where
  startParameter : ℝ
  endParameter : ℝ
  length : ℝ

structure ConjugateEventSequenceInjectivityRadiusCertificate where
  piecewiseGeodesicSegmentsContiguous : Bool
  junctionPositionCompatible : Bool
  junctionTangentJumpBounded : Bool
  conjugateEventSequenceStrictlyOrdered : Bool
  morseIndexJumpMatchesMultiplicity : Bool
  eventNullityMatchesMultiplicity : Bool
  finiteWindowMorseIndexConsistent : Bool
  cutLocusCandidatesRetained : Bool
  injectivityRadiusLowerBoundCertified : Bool
  conjugateEventsLocalOnly : Bool
  cutLocusCandidatesLocalOnly : Bool
  injectivityRadiusBoundLocalOnly : Bool
  candidateIdentityRetained : Bool
  sourceMorseIndexCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  morseIndexGrantsNoAuthority : Bool
  conjugateEventGrantsNoAuthority : Bool
  cutLocusGrantsNoAuthority : Bool
  injectivityRadiusGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- A conjugate event has the expected finite-window Morse-index jump. -/
def ValidMorseJump (event : ConjugateEvent) : Prop :=
  event.morseIndexAfter = event.morseIndexBefore + event.multiplicity

/-- The event nullity agrees with the retained local multiplicity candidate. -/
def NullityMatchesMultiplicity (event : ConjugateEvent) : Prop :=
  event.nullityAtEvent = event.multiplicity

/-- Total retained multiplicity of a finite conjugate-event list. -/
def eventMultiplicitySum (events : List ConjugateEvent) : ℕ :=
  (events.map fun event => event.multiplicity).sum

/-- Finite-window Morse-index value predicted by the retained event multiplicities. -/
def predictedFinalMorseIndex
    (initialIndex : ℕ)
    (events : List ConjugateEvent) : ℕ :=
  initialIndex + eventMultiplicitySum events

/-- A segment has positive parameter extent and the retained length matches it. -/
def ValidSegment (segment : PiecewiseGeodesicSegment) : Prop :=
  segment.startParameter < segment.endParameter ∧
    segment.length = segment.endParameter - segment.startParameter

/-- Every retained conjugate event lies at or beyond the certified radius. -/
def EventFreeThrough (events : List ConjugateEvent) (radius : ℝ) : Prop :=
  ∀ event ∈ events, radius ≤ event.parameter

/-- Every retained cut-locus candidate lies at or beyond the certified radius. -/
def CutFreeThrough (candidates : List CutLocusCandidate) (radius : ℝ) : Prop :=
  ∀ candidate ∈ candidates, radius ≤ candidate.parameter

/-- No retained conjugate or cut obstruction occurs before the radius. -/
def ObstructionFreeThrough
    (events : List ConjugateEvent)
    (candidates : List CutLocusCandidate)
    (radius : ℝ) : Prop :=
  EventFreeThrough events radius ∧ CutFreeThrough candidates radius

/-- A positive obstruction-free radius is a local injectivity-radius lower-bound witness. -/
def LocalInjectivityLowerBound
    (events : List ConjugateEvent)
    (candidates : List CutLocusCandidate)
    (radius : ℝ) : Prop :=
  0 < radius ∧ ObstructionFreeThrough events candidates radius

@[simp] theorem eventMultiplicitySum_nil :
    eventMultiplicitySum [] = 0 := by
  simp [eventMultiplicitySum]

@[simp] theorem eventMultiplicitySum_cons
    (event : ConjugateEvent)
    (events : List ConjugateEvent) :
    eventMultiplicitySum (event :: events) =
      event.multiplicity + eventMultiplicitySum events := by
  simp [eventMultiplicitySum]

@[simp] theorem predictedFinalMorseIndex_nil
    (initialIndex : ℕ) :
    predictedFinalMorseIndex initialIndex [] = initialIndex := by
  simp [predictedFinalMorseIndex]

/-- Adding one event advances the predicted index by its multiplicity. -/
theorem predictedFinalMorseIndex_cons
    (initialIndex : ℕ)
    (event : ConjugateEvent)
    (events : List ConjugateEvent) :
    predictedFinalMorseIndex initialIndex (event :: events) =
      predictedFinalMorseIndex
        (initialIndex + event.multiplicity) events := by
  simp [predictedFinalMorseIndex, eventMultiplicitySum, Nat.add_assoc]

/-- A valid event jump cannot decrease the finite-window Morse index. -/
theorem validMorseJump_non_decreasing
    (event : ConjugateEvent)
    (hvalid : ValidMorseJump event) :
    event.morseIndexBefore ≤ event.morseIndexAfter := by
  unfold ValidMorseJump at hvalid
  omega

/-- Positive multiplicity makes a valid event jump strictly increase the index. -/
theorem validMorseJump_strict
    (event : ConjugateEvent)
    (hvalid : ValidMorseJump event)
    (hmultiplicity : 0 < event.multiplicity) :
    event.morseIndexBefore < event.morseIndexAfter := by
  unfold ValidMorseJump at hvalid
  omega

/-- Matching positive multiplicity gives positive local nullity. -/
theorem positive_nullity_of_matching_multiplicity
    (event : ConjugateEvent)
    (hnullity : NullityMatchesMultiplicity event)
    (hmultiplicity : 0 < event.multiplicity) :
    0 < event.nullityAtEvent := by
  unfold NullityMatchesMultiplicity at hnullity
  omega

/-- One valid event agrees with the additive predicted final index. -/
theorem one_event_index_matches_prediction
    (event : ConjugateEvent)
    (hvalid : ValidMorseJump event) :
    event.morseIndexAfter =
      predictedFinalMorseIndex event.morseIndexBefore [event] := by
  simpa [predictedFinalMorseIndex, eventMultiplicitySum] using hvalid

/-- A valid piecewise-geodesic segment has strictly positive retained length. -/
theorem validSegment_positive_length
    (segment : PiecewiseGeodesicSegment)
    (hvalid : ValidSegment segment) :
    0 < segment.length := by
  rcases hvalid with ⟨horder, hlength⟩
  rw [hlength]
  exact sub_pos.mpr horder

@[simp] theorem eventFreeThrough_nil (radius : ℝ) :
    EventFreeThrough [] radius := by
  simp [EventFreeThrough]

@[simp] theorem cutFreeThrough_nil (radius : ℝ) :
    CutFreeThrough [] radius := by
  simp [CutFreeThrough]

/-- Lowering an obstruction-free radius preserves obstruction freedom. -/
theorem obstructionFreeThrough_mono
    (events : List ConjugateEvent)
    (candidates : List CutLocusCandidate)
    {smaller larger : ℝ}
    (horder : smaller ≤ larger)
    (hfree : ObstructionFreeThrough events candidates larger) :
    ObstructionFreeThrough events candidates smaller := by
  constructor
  · intro event hevent
    exact le_trans horder (hfree.1 event hevent)
  · intro candidate hcandidate
    exact le_trans horder (hfree.2 candidate hcandidate)

/-- Every certified local injectivity lower bound is positive. -/
theorem localInjectivityLowerBound_positive
    (events : List ConjugateEvent)
    (candidates : List CutLocusCandidate)
    (radius : ℝ)
    (hbound : LocalInjectivityLowerBound events candidates radius) :
    0 < radius := by
  exact hbound.1

/-- Every certified local injectivity lower bound is obstruction-free. -/
theorem localInjectivityLowerBound_obstruction_free
    (events : List ConjugateEvent)
    (candidates : List CutLocusCandidate)
    (radius : ℝ)
    (hbound : LocalInjectivityLowerBound events candidates radius) :
    ObstructionFreeThrough events candidates radius := by
  exact hbound.2

/-- Event, cut-locus, and injectivity-radius evidence grants no authority. -/
theorem geometric_obstruction_evidence_grants_no_authority
    (certificate : ConjugateEventSequenceInjectivityRadiusCertificate)
    (hevent : certificate.conjugateEventGrantsNoAuthority = true)
    (hcut : certificate.cutLocusGrantsNoAuthority = true)
    (hradius : certificate.injectivityRadiusGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.conjugateEventGrantsNoAuthority = true ∧
      certificate.cutLocusGrantsNoAuthority = true ∧
      certificate.injectivityRadiusGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hevent, hcut, hradius, hselection, hexecution⟩

/-- The v1.11 certificate remains read-only, future-only, and inactive. -/
theorem conjugate_event_certificate_is_future_only
    (certificate : ConjugateEventSequenceInjectivityRadiusCertificate)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.ConjugateEventSequenceInjectivityRadiusV1_11
