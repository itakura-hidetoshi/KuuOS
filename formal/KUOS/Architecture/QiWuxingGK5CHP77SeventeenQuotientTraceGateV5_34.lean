import KUOS.Architecture.QiWuxingGK5CHP77ContextualSixteenSeventeenV5_33

/-!
Qi v5.34 — proof-relevant SELECTED seventeen comparison quotient,
necessary and sufficient observable-descent condition, ordered outer
context trace invariance, and a precise mixed higher-gluing gate.

The new object is the quotient of ACTUAL v5.33 selected contextual
sixteenth proof values by existing, properly indexed v5.33 local
seventeenth proof values.  We do not change or identify any source
sixteenth proof terms: equivalence means NONEMPTY local 17D evidence,
not raw equality or a silently strengthened original type.

The ordered external seventh-context List Bool trace of raw 16D
witnesses is preserved by ALL FIVE v5.33 selected local 17D
constructors (strict, left unit, right unit, reverse, chain).  It
therefore descends as a genuine Quotient.lift.  Arbitrary target
observations descend precisely if they respect this selected 17D
relation.  The raw SIXTEENTH first-constructor tag demonstrably
does NOT descend: true 17D selected unit-pasting witness connects
raw16D tags 3 and 0.  Thus the quotient is nontrivial and nonfaithful.

The two v5.33 mixed LEFT-after-RIGHT versus RIGHT-after-LEFT 16D
transports have different DEPENDENT 15D endpoint indices.  We keep
them separate but compare their class-level trace values in the
common List Bool observation type: opposite first two events differ,
although their lengths and left/right event counts agree.

An explicit *trace-respecting mixed higher-gluing gate* carries the
ACTUAL v5.33 lower 12D–14D witness packet together with the required
equality of the two high-order traces.  The lower witness packet
always exists under its original typed hypotheses; the additional
trace-respecting gate is impossible by the proved order obstruction.
This is an obstruction to THAT precise authority-preserving gate;
it is not a theorem that all potential higher exchange presentations
or all trace-changing high-cell mediators are impossible.

All original F55/P77/GK5CG sources and raw 6D–16D witnesses remain
unaltered.  No global 17D coherence, unconditional mixed exchange,
new axioms, sorry, proof erasure or implicit strictification.
Append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix uObs

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

/-- Each and every SELECTED old 17D generator preserves the
EXISTING raw16D outer-context order witness. This is a theorem
ABOUT THE CHOSEN PRESENTATION, not a global coherence claim. -/
theorem selectedSeventeen_preservesSixteenTrace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedLocalSeventeen W l r H K) :
    selectedContextSixteenTrace l r H = selectedContextSixteenTrace l r K := by
  induction J with
  | strict H => rfl
  | unitLeft before F G C after => rfl
  | unitRight before F G C after => rfl
  | reverse J ih => exact ih.symm
  | chain J M ih ih' => exact ih.trans ih'

/-- Unlike v5.31's FOURTEENTH quotient by 15D and v5.33's
FIFTEENTH quotient by 16D, this quotient relates genuine
PARALLEL SIXTEENTH raw proof values by actual local 17D evidence. -/
def selectedSeventeenSetoid (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    Setoid (SelectedContextualSixteen W l r T U) where
  r := fun H K => Nonempty (SelectedLocalSeventeen W l r H K)
  iseqv := by
    constructor
    · intro H
      exact ⟨.strict H⟩
    · intro H K h
      rcases h with ⟨J⟩
      exact ⟨.reverse J⟩
    · intro H K M h h'
      rcases h with ⟨J⟩
      rcases h' with ⟨N⟩
      exact ⟨.chain J N⟩

def selectedSeventeenClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    Quotient (selectedSeventeenSetoid l r T U) :=
  Quotient.mk _ H

theorem selectedSeventeenClass_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U) :
    selectedSeventeenClass l r H = selectedSeventeenClass l r K ↔
      Nonempty (SelectedLocalSeventeen W l r H K) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- Any observer constant along ALL selected local 17D
comparisons descends. This is a CONDITION, not an automatic
claim that arbitrary history survives the new quotient. -/
def selectedSeventeenQuotientLift (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {A : Type uObs}
    (obs : SelectedContextualSixteen W l r T U → A)
    (compatible : ∀ (H K : SelectedContextualSixteen W l r T U),
      SelectedLocalSeventeen W l r H K → obs H = obs K) :
    Quotient (selectedSeventeenSetoid l r T U) → A :=
  Quotient.lift obs (by
    intro H K h
    rcases h with ⟨J⟩
    exact compatible H K J)

theorem selectedSeventeenQuotientLift_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {A : Type uObs}
    (obs : SelectedContextualSixteen W l r T U → A)
    (compatible : ∀ (H K : SelectedContextualSixteen W l r T U),
      SelectedLocalSeventeen W l r H K → obs H = obs K)
    (H : SelectedContextualSixteen W l r T U) :
    selectedSeventeenQuotientLift l r obs compatible
      (selectedSeventeenClass l r H) = obs H :=
  rfl

/-- The COMPLETE ordered exterior Bool history descends through
this SPECIFIC selected 17D presentation, not through arbitrary
future quotient extensions. -/
def selectedSeventeenTraceOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    Quotient (selectedSeventeenSetoid l r T U) → List Bool :=
  selectedSeventeenQuotientLift l r
    (selectedContextSixteenTrace l r)
    (by
      intro H K J
      exact selectedSeventeen_preservesSixteenTrace l r J)

theorem selectedSeventeenTrace_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    selectedSeventeenTraceOnQuotient l r T U
      (selectedSeventeenClass l r H) =
        selectedContextSixteenTrace l r H :=
  rfl

/-- Coarse left/right context event counts also descend as a
composition of the FINE trace with the finite counting observer. -/
def selectedSeventeenCountsOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    (T U : SelectedContextualFifteen W l r V X) :
    Quotient (selectedSeventeenSetoid l r T U) → Nat × Nat :=
  fun cls => selectedFifteenTraceCounts
    (selectedSeventeenTraceOnQuotient l r T U cls)

theorem selectedSeventeenCounts_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U) :
    selectedSeventeenCountsOnQuotient l r T U
      (selectedSeventeenClass l r H) =
        selectedFifteenTraceCounts (selectedContextSixteenTrace l r H) :=
  rfl

/-- Descended trace distinguishes classes whenever their raw
outer-context histories differ AND their original FIFTEENTH
endpoints are EXACTLY the same. -/
theorem selectedSeventeen_distinctClass_of_traceNe (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H K : SelectedContextualSixteen W l r T U)
    (h : selectedContextSixteenTrace l r H ≠
      selectedContextSixteenTrace l r K) :
    selectedSeventeenClass l r H ≠ selectedSeventeenClass l r K := by
  intro eq
  exact h (congrArg (selectedSeventeenTraceOnQuotient l r T U) eq)

/-- An ACTUAL v5.33 selected 17D local unit compares two
distinct original 16D proof terms in the NEW quotient. -/
theorem selectedSeventeenLeftUnit_classEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSeventeenClass l r
        (selectedSixteenUnitPrependLeft l r before F G C after) =
      selectedSeventeenClass l r
        (selectedSixteenUnitAppendLeft l r before F G C after) :=
  Quotient.sound ⟨SelectedLocalSeventeen.unitLeft before F G C after⟩

theorem selectedSeventeenRightUnit_classEq (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    selectedSeventeenClass l r
        (selectedSixteenUnitPrependRight l r before F G C after) =
      selectedSeventeenClass l r
        (selectedSixteenUnitAppendRight l r before F G C after) :=
  Quotient.sound ⟨SelectedLocalSeventeen.unitRight before F G C after⟩

/-- The quotient projection is NOT injective on this genuine
local unit critical pair, although prior raw evidence is preserved
in its original Type outside the quotient. -/
theorem selectedSeventeenLeftUnit_projectionNotInjective (l r : W)
    {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ Function.Injective (fun H : SelectedContextualSixteen W l r
      (selectedFifteenUnitRoundtrip l r before F G C after)
      (SelectedContextualFifteen.strict
        (selectedMixedFourteenUnitPrepend l r before F G C after)) =>
      selectedSeventeenClass l r H) := by
  intro injective
  exact selectedSixteenUnitLeft_rawDistinct l r before F G C after
    (injective (selectedSeventeenLeftUnit_classEq l r before F G C after))

/-- Old raw SIXTEENTH first-constructor tag is NOT compatible
with selected 17D: true 17D unit evidence relates tag 3 to 0. -/
theorem selectedSeventeen_noFirstTagDescent (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∃ g : Quotient (selectedSeventeenSetoid l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))) → Nat,
      ∀ (H : SelectedContextualSixteen W l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))),
        g (selectedSeventeenClass l r H) =
          selectedContextSixteenFirstAtomTag l r H) := by
  rintro ⟨g, hg⟩
  have ht : selectedContextSixteenFirstAtomTag l r
      (selectedSixteenUnitPrependLeft l r before F G C after) =
        selectedContextSixteenFirstAtomTag l r
          (selectedSixteenUnitAppendLeft l r before F G C after) := by
    calc
      _ = g (selectedSeventeenClass l r
          (selectedSixteenUnitPrependLeft l r before F G C after)) :=
        (hg _).symm
      _ = g (selectedSeventeenClass l r
          (selectedSixteenUnitAppendLeft l r before F G C after)) :=
        congrArg g (selectedSeventeenLeftUnit_classEq l r before F G C after)
      _ = _ := hg _
  change (3 : Nat) = 0 at ht
  cases ht

/-- The full ordered LR/RL 16D-context traces remain different
when each is mapped through its OWN exactly typed selected 17D
quotient. The two quotient types are generally different! Only
their images in the COMMON List Bool are compared. -/
theorem selectedSeventeenMixedOrder_traceObstruction (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    selectedSeventeenTraceOnQuotient l r _ _
        (selectedSeventeenClass l r
          (selectedSixteenLeftAfterRight l r left F G H right)) ≠
      selectedSeventeenTraceOnQuotient l r _ _
        (selectedSeventeenClass l r
          (selectedSixteenRightAfterLeft l r left F G H right)) := by
  change selectedContextSixteenTrace l r
      (selectedSixteenLeftAfterRight l r left F G H right) ≠
        selectedContextSixteenTrace l r
          (selectedSixteenRightAfterLeft l r left F G H right)
  exact selectedSixteenMixedTrace_obstruction l r left F G H right

theorem selectedSeventeenMixedOrder_countAgreement (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    selectedSeventeenCountsOnQuotient l r _ _
        (selectedSeventeenClass l r
          (selectedSixteenLeftAfterRight l r left F G H right)) =
      selectedSeventeenCountsOnQuotient l r _ _
        (selectedSeventeenClass l r
          (selectedSixteenRightAfterLeft l r left F G H right)) := by
  change selectedFifteenTraceCounts
      (selectedContextSixteenTrace l r
        (selectedSixteenLeftAfterRight l r left F G H right)) =
        selectedFifteenTraceCounts
          (selectedContextSixteenTrace l r
            (selectedSixteenRightAfterLeft l r left F G H right))
  rw [(selectedSixteenMixedTraceValues l r left F G H right).1,
    (selectedSixteenMixedTraceValues l r left F G H right).2]
  simp [selectedFifteenTraceCounts]

/-- Trace-respecting mixed gluing gate: in addition to the entire
REAL original 12D–selected14D packet, a proposed higher mediation
must preserve the SAME ordered 16D exterior-context trace on
its two different dependently typed boundary presentations.
This is a PRECISE conditional gate, not a universal definition
of all conceivable higher-comparison Types. -/
structure SelectedMixedTraceRespectingHigherGate (l r : W)
    {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    {E D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r E D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) : Type uSix where
  lower : SelectedMixedLowerHigherPacket l r left F G C right
  orderedTraceCompatibility :
    selectedContextSixteenTrace l r
        (selectedSixteenLeftAfterRight l r left F G H right) =
      selectedContextSixteenTrace l r
        (selectedSixteenRightAfterLeft l r left F G H right)

/-- Any gluing certificate with the above explicitly required
trace compatibility is obstructed by the actual LR/RL history.
No assumption about an arbitrary trace-CHANGING comparison is made. -/
theorem selectedMixedTraceRespectingHigherGate_empty (l r : W)
    {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    {E D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r E D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    ¬ Nonempty (SelectedMixedTraceRespectingHigherGate l r
      left F G C H right) := by
  rintro ⟨gate⟩
  exact selectedSixteenMixedTrace_obstruction l r left F G H right
    gate.orderedTraceCompatibility

/-- All the required ACTUAL lower witnesses are AVAILABLE,
yet that suffices neither to identify raw 15D endpoints nor
to construct a TRACE-PRESERVING high-level mixed gluing. -/
theorem selectedMixedLowerCompatible_butHigherTraceObstructed (l r : W)
    {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    {E D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r E D}
    {T U : SelectedContextualFifteen W l r V X}
    (H : SelectedContextualSixteen W l r T U)
    (right : SevenRewrite W l r c d) :
    Nonempty (SelectedMixedLowerHigherPacket l r left F G C right) ∧
      ¬ Nonempty (SelectedMixedTraceRespectingHigherGate l r
        left F G C H right) :=
  ⟨⟨selectedMixedLowerHigherPacket l r left F G C right⟩,
    selectedMixedTraceRespectingHigherGate_empty l r left F G C H right⟩

/-- Selected 17D comparison cannot universally be read as raw
16D equality, even in the most restrictive exact 15D unit fiber. -/
theorem selectedSeventeen_noRawEqualityInterpreter (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F G : ContextFrameEleven W l r c d)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (C : SelectedContextualThirteen W l r P Q)
    (after : SevenRewrite W l r d e) :
    ¬ (∀
      (H K : SelectedContextualSixteen W l r
        (selectedFifteenUnitRoundtrip l r before F G C after)
        (SelectedContextualFifteen.strict
          (selectedMixedFourteenUnitPrepend l r before F G C after))),
      SelectedLocalSeventeen W l r H K → H = K) := by
  intro interpret
  exact selectedSixteenUnitLeft_rawDistinct l r before F G C after
    (interpret _ _ (.unitLeft before F G C after))

#print axioms PentagonAdjoinedSixCell.selectedSeventeen_preservesSixteenTrace
#print axioms PentagonAdjoinedSixCell.selectedSeventeenSetoid
#print axioms PentagonAdjoinedSixCell.selectedSeventeenClass
#print axioms PentagonAdjoinedSixCell.selectedSeventeenClass_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedSeventeenQuotientLift
#print axioms PentagonAdjoinedSixCell.selectedSeventeenQuotientLift_onClass
#print axioms PentagonAdjoinedSixCell.selectedSeventeenTraceOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedSeventeenTrace_onClass
#print axioms PentagonAdjoinedSixCell.selectedSeventeenCountsOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedSeventeenCounts_onClass
#print axioms PentagonAdjoinedSixCell.selectedSeventeen_distinctClass_of_traceNe
#print axioms PentagonAdjoinedSixCell.selectedSeventeenLeftUnit_classEq
#print axioms PentagonAdjoinedSixCell.selectedSeventeenRightUnit_classEq
#print axioms PentagonAdjoinedSixCell.selectedSeventeenLeftUnit_projectionNotInjective
#print axioms PentagonAdjoinedSixCell.selectedSeventeen_noFirstTagDescent
#print axioms PentagonAdjoinedSixCell.selectedSeventeenMixedOrder_traceObstruction
#print axioms PentagonAdjoinedSixCell.selectedSeventeenMixedOrder_countAgreement
#print axioms PentagonAdjoinedSixCell.SelectedMixedTraceRespectingHigherGate
#print axioms PentagonAdjoinedSixCell.selectedMixedTraceRespectingHigherGate_empty
#print axioms PentagonAdjoinedSixCell.selectedMixedLowerCompatible_butHigherTraceObstructed
#print axioms PentagonAdjoinedSixCell.selectedSeventeen_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
