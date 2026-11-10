import KUOS.Architecture.QiWuxingGK5CHP77SameFiberUnitCollisionNecessityV5_90

/-!
Qi v5.91 — the ACTUAL original old18D dependent proof family admits
NO one-unit closed raw17D loop, while two-unit original roundtrips
exist whenever actual old18D unitLeft or unitRight evidence is
supplied with its genuine dependent contexts.

All five ORIGINAL old18D constructors are handled in the induction:
strict has count zero; original unitLeft and unitRight have genuinely
distinct raw17D endpoints by the certified v5.35 lemmas; reverse
preserves the count and exchanges endpoints; chain adds counts.
If chain has exactly one unit, the other leg has zero units and
therefore has EQUAL original raw17D endpoints by v5.89. No 17D
quotient equality is substituted for a raw endpoint equality.

This yields the exact-loop original unit-count dichotomy
    count = 0 or count >= 2.
The unit-bound is SHARP conditionally on the real supplied contexts:
the roundtrips A ; reverse(A) and reverse(A) ; A of actual original
unitLeft/right generators each have precisely two unit atoms,
and their two loops live in DISTINCT genuine raw17D endpoint fibers.

Combine this result with the v5.90 necessary collision obstruction:
a hypothetical raw-distinct equal-bracket old18D pair in ONE N->N
fiber, or an old-five/new-seven quotient collapse of that pair,
has original unit count at least TWO on BOTH sides.
This remains a NECESSARY condition. No actual same-fiber fingerprint
collision, original 19D comparison inhabitance, or global descent
is asserted by these theorems.

No original definitions or comparisons changed; no false pasting of
the two raw-distinct loop endpoint fibers; no WORLD/20D authority.
append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section OriginalDependentSource

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Structural theorem for the UNMODIFIED original dependent 18D
evidence. A proof with EXACTLY ONE actual unit constructor must
connect different ORIGINAL raw17D endpoint values. The unit-case
inequalities are the real v5.35 proofs, while zero-unit chain legs
use the v5.89 genuine endpoint-equality witness. -/
theorem selectedV591OneUnitEndpointsDistinct
    (M : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1) :
    J ≠ N := by
  induction M with
  | strict _ =>
      have hbad : (0 : Nat) = 1 := hone
      cases hbad
  | unitLeft before F G C after =>
      exact selectedSeventeenUnitLeft_rawDistinct l r before F G C after
  | unitRight before F G C after =>
      exact selectedSeventeenUnitRight_rawDistinct l r before F G C after
  | reverse M ih =>
      have hs : selectedV589OriginalUnitCount l r M = 1 := by
        simpa only [selectedV589OriginalUnitCount] using hone
      intro h
      exact ih hs h.symm
  | chain A B ihA ihB =>
      have hsum :
          selectedV589OriginalUnitCount l r A +
            selectedV589OriginalUnitCount l r B = 1 := by
        simpa only [selectedV589OriginalUnitCount] using hone
      intro heq
      by_cases ha0 : selectedV589OriginalUnitCount l r A = 0
      · have hb1 : selectedV589OriginalUnitCount l r B = 1 := by
          omega
        obtain ⟨hleft, _, _⟩ :=
          selectedV589OriginalFree_exhausted l r A ha0
        exact ihB hb1 (hleft.symm.trans heq)
      · have ha1 : selectedV589OriginalUnitCount l r A = 1 := by
          omega
        have hb0 : selectedV589OriginalUnitCount l r B = 0 := by
          omega
        obtain ⟨hright, _, _⟩ :=
          selectedV589OriginalFree_exhausted l r B hb0
        exact ihA ha1 (heq.trans hright.symm)

/-- A genuine old18D raw N->N LOOP cannot have exactly one
original unitLeft or unitRight generator, even when hidden under
arbitrary raw reverse and nonassociative raw chain syntax. -/
theorem selectedV591LoopUnitCount_ne_one
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r N N) :
    selectedV589OriginalUnitCount l r M ≠ 1 := by
  intro hone
  exact (selectedV591OneUnitEndpointsDistinct l r M hone) rfl

/-- Exact numerical gap for every genuinely indexed old18D loop.
The zero-unit side is precisely the faithful v5.89 source image.
A positive-unit loop must contain at least TWO original unit atoms. -/
theorem selectedV591LoopZeroOrAtLeastTwo
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r N N) :
    selectedV589OriginalUnitCount l r M = 0 ∨
      2 ≤ selectedV589OriginalUnitCount l r M := by
  by_cases hz : selectedV589OriginalUnitCount l r M = 0
  · exact Or.inl hz
  · have hne := selectedV591LoopUnitCount_ne_one l r N M
    exact Or.inr (by omega)

/-- A genuinely original unit-bearing old18D N->N loop has
at least two unit occurrences; it does not follow that two
unit atoms are sufficient to make a fingerprint collision. -/
theorem selectedV591LoopPositiveAtLeastTwo
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r N N)
    (hpos : 0 < selectedV589OriginalUnitCount l r M) :
    2 ≤ selectedV589OriginalUnitCount l r M := by
  rcases selectedV591LoopZeroOrAtLeastTwo l r N M with hz | htwo
  · omega
  · exact htwo

/-- Canonical roundtrip of a genuinely typed original old18D
source A:J->N, living in its true START-endpoint J->J fiber. -/
def selectedV591ForwardRoundTrip
    (M : SelectedLocalEighteen W l r J N) :
    SelectedLocalEighteen W l r J J :=
  .chain M (.reverse M)

/-- The reversed roundtrip lives at the actual TARGET endpoint
N->N. We do not claim its fiber equals the forward roundtrip's. -/
def selectedV591BackwardRoundTrip
    (M : SelectedLocalEighteen W l r J N) :
    SelectedLocalEighteen W l r N N :=
  .chain (.reverse M) M

/-- The two true dependent roundtrips have double the original
unit count, with the full original source preserved in both. -/
theorem selectedV591ForwardRoundTrip_unitCount
    (M : SelectedLocalEighteen W l r J N) :
    selectedV589OriginalUnitCount l r
      (selectedV591ForwardRoundTrip l r M) =
        2 * selectedV589OriginalUnitCount l r M := by
  change selectedV589OriginalUnitCount l r M +
      selectedV589OriginalUnitCount l r M =
        2 * selectedV589OriginalUnitCount l r M
  omega

theorem selectedV591BackwardRoundTrip_unitCount
    (M : SelectedLocalEighteen W l r J N) :
    selectedV589OriginalUnitCount l r
      (selectedV591BackwardRoundTrip l r M) =
        2 * selectedV589OriginalUnitCount l r M := by
  change selectedV589OriginalUnitCount l r M +
      selectedV589OriginalUnitCount l r M =
        2 * selectedV589OriginalUnitCount l r M
  omega

/-- No original old18D source data are rewritten: v5.73 observes
the actual nonassociative chain brackets and raw reverse wrappers. -/
theorem selectedV591ForwardRoundTrip_bracket
    (M : SelectedLocalEighteen W l r J N) :
    selectedLocalEighteenInnerBracket l r
      (selectedV591ForwardRoundTrip l r M) =
        .oldJoined
          (selectedLocalEighteenInnerBracket l r M)
          (.oldReversed (selectedLocalEighteenInnerBracket l r M)) :=
  rfl

theorem selectedV591BackwardRoundTrip_bracket
    (M : SelectedLocalEighteen W l r J N) :
    selectedLocalEighteenInnerBracket l r
      (selectedV591BackwardRoundTrip l r M) =
        .oldJoined
          (.oldReversed (selectedLocalEighteenInnerBracket l r M))
          (selectedLocalEighteenInnerBracket l r M) :=
  rfl

/-- A supplied original one-unit source produces genuinely typed
TWO-unit loops, but at different raw17D endpoint fibers. The
original endpoint inequality is retained as an obstruction. -/
theorem selectedV591SingleUnitSourceRoundTrips
    (M : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1) :
    J ≠ N ∧
    selectedV589OriginalUnitCount l r
      (selectedV591ForwardRoundTrip l r M) = 2 ∧
    selectedV589OriginalUnitCount l r
      (selectedV591BackwardRoundTrip l r M) = 2 := by
  refine ⟨selectedV591OneUnitEndpointsDistinct l r M hone, ?_, ?_⟩
  · rw [selectedV591ForwardRoundTrip_unitCount l r M, hone]
  · rw [selectedV591BackwardRoundTrip_unitCount l r M, hone]

end OriginalDependentSource

section ActualOriginalUnitGenerators

variable (l r : W)
variable {w z : W}
variable {b c d e : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable (C : SelectedContextualThirteen W l r P Q)
variable (after : SevenRewrite W l r d e)

/-- Actual original left-unit comparison has DISTINCT raw17D
endpoints, yet its genuine forward and backward raw18D roundtrip
loops both contain exactly two unit atoms. Bracket positions stay
ordered and are not collapsed into an inverse/unit law. -/
theorem selectedV591ActualLeftUnitTwoRoundTrips :
    selectedSeventeenUnitPrependLeft l r before F G C after ≠
      selectedSeventeenUnitAppendLeft l r before F G C after ∧
    selectedV589OriginalUnitCount l r
      (selectedV591ForwardRoundTrip l r
        (SelectedLocalEighteen.unitLeft before F G C after)) = 2 ∧
    selectedV589OriginalUnitCount l r
      (selectedV591BackwardRoundTrip l r
        (SelectedLocalEighteen.unitLeft before F G C after)) = 2 ∧
    selectedLocalEighteenInnerBracket l r
      (selectedV591ForwardRoundTrip l r
        (SelectedLocalEighteen.unitLeft before F G C after)) =
          .oldJoined .oldUnitLeft (.oldReversed .oldUnitLeft) ∧
    selectedLocalEighteenInnerBracket l r
      (selectedV591BackwardRoundTrip l r
        (SelectedLocalEighteen.unitLeft before F G C after)) =
          .oldJoined (.oldReversed .oldUnitLeft) .oldUnitLeft := by
  refine ⟨selectedSeventeenUnitLeft_rawDistinct l r before F G C after,
    ?_, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · rfl
  · rfl

/-- The separate genuine right-unit source also yields two
minimal positive-unit roundtrips at its OWN raw endpoints. -/
theorem selectedV591ActualRightUnitTwoRoundTrips :
    selectedSeventeenUnitPrependRight l r before F G C after ≠
      selectedSeventeenUnitAppendRight l r before F G C after ∧
    selectedV589OriginalUnitCount l r
      (selectedV591ForwardRoundTrip l r
        (SelectedLocalEighteen.unitRight before F G C after)) = 2 ∧
    selectedV589OriginalUnitCount l r
      (selectedV591BackwardRoundTrip l r
        (SelectedLocalEighteen.unitRight before F G C after)) = 2 ∧
    selectedLocalEighteenInnerBracket l r
      (selectedV591ForwardRoundTrip l r
        (SelectedLocalEighteen.unitRight before F G C after)) =
          .oldJoined .oldUnitRight (.oldReversed .oldUnitRight) ∧
    selectedLocalEighteenInnerBracket l r
      (selectedV591BackwardRoundTrip l r
        (SelectedLocalEighteen.unitRight before F G C after)) =
          .oldJoined (.oldReversed .oldUnitRight) .oldUnitRight := by
  refine ⟨selectedSeventeenUnitRight_rawDistinct l r before F G C after,
    ?_, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · rfl
  · rfl

end ActualOriginalUnitGenerators

section NecessaryUnitThresholdForCollisions

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Sharpen the v5.90 hypothetical fingerprint-collision condition:
in an ACTUAL common N->N raw17D fiber BOTH distinct original
sources must contain at least TWO original unit generators. -/
theorem selectedV591BracketCollision_requiresTwoUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hne : M ≠ L) :
    2 ≤ selectedV589OriginalUnitCount l r M ∧
      2 ≤ selectedV589OriginalUnitCount l r L := by
  have hp := selectedV590BracketCollision_requiresPositiveUnits
    l r N M L hbr hne
  exact ⟨selectedV591LoopPositiveAtLeastTwo l r N M hp.1,
    selectedV591LoopPositiveAtLeastTwo l r N L hp.2⟩

/-- Independent OLD five-generator selected19 quotient, with its
actual inherited-source observation and ORIGINAL old18D proofs. -/
theorem selectedV591OldClassCollision_requiresTwoUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedNineteenClass l r (.inherited M) =
        selectedNineteenClass l r (.inherited L))
    (hne : M ≠ L) :
    2 ≤ selectedV589OriginalUnitCount l r M ∧
      2 ≤ selectedV589OriginalUnitCount l r L := by
  have hp := selectedV590OldClassCollision_requiresPositiveUnits
    l r N M L hclass hne
  exact ⟨selectedV591LoopPositiveAtLeastTwo l r N M hp.1,
    selectedV591LoopPositiveAtLeastTwo l r N L hp.2⟩

/-- Independently the NEW seven-generator raw congruence quotient
has the same necessary threshold; old/new Types stay separate. -/
theorem selectedV591NewClassCollision_requiresTwoUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedRawCongruentClass l r (.inherited M) =
        selectedRawCongruentClass l r (.inherited L))
    (hne : M ≠ L) :
    2 ≤ selectedV589OriginalUnitCount l r M ∧
      2 ≤ selectedV589OriginalUnitCount l r L := by
  have hp := selectedV590NewClassCollision_requiresPositiveUnits
    l r N M L hclass hne
  exact ⟨selectedV591LoopPositiveAtLeastTwo l r N M hp.1,
    selectedV591LoopPositiveAtLeastTwo l r N L hp.2⟩

/-- A truly GIVEN OLD selected19 Type comparison of different
same-fiber inherited raw sources also requires two unit atoms
per original source. No comparison inhabitance is constructed. -/
theorem selectedV591OldTypedCollision_requiresTwoUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hcomp : Nonempty (SelectedLocalNineteen W l r
      (.inherited M) (.inherited L)))
    (hne : M ≠ L) :
    2 ≤ selectedV589OriginalUnitCount l r M ∧
      2 ≤ selectedV589OriginalUnitCount l r L := by
  have hp := selectedV590OldTypedCollision_requiresPositiveUnits
    l r N M L hcomp hne
  exact ⟨selectedV591LoopPositiveAtLeastTwo l r N M hp.1,
    selectedV591LoopPositiveAtLeastTwo l r N L hp.2⟩

/-- Same conditional obstruction for the actual NEW seven-generator
Type19 comparison, not an unproved cross-Type19 identification. -/
theorem selectedV591NewTypedCollision_requiresTwoUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hcomp : Nonempty (SelectedRawCongruentNineteen W l r N N
      (.inherited M) (.inherited L)))
    (hne : M ≠ L) :
    2 ≤ selectedV589OriginalUnitCount l r M ∧
      2 ≤ selectedV589OriginalUnitCount l r L := by
  have hp := selectedV590NewTypedCollision_requiresPositiveUnits
    l r N M L hcomp hne
  exact ⟨selectedV591LoopPositiveAtLeastTwo l r N M hp.1,
    selectedV591LoopPositiveAtLeastTwo l r N L hp.2⟩

end NecessaryUnitThresholdForCollisions

#print axioms PentagonAdjoinedSixCell.selectedV591OneUnitEndpointsDistinct
#print axioms PentagonAdjoinedSixCell.selectedV591LoopUnitCount_ne_one
#print axioms PentagonAdjoinedSixCell.selectedV591LoopZeroOrAtLeastTwo
#print axioms PentagonAdjoinedSixCell.selectedV591LoopPositiveAtLeastTwo
#print axioms PentagonAdjoinedSixCell.selectedV591ForwardRoundTrip
#print axioms PentagonAdjoinedSixCell.selectedV591BackwardRoundTrip
#print axioms PentagonAdjoinedSixCell.selectedV591ForwardRoundTrip_unitCount
#print axioms PentagonAdjoinedSixCell.selectedV591BackwardRoundTrip_unitCount
#print axioms PentagonAdjoinedSixCell.selectedV591ForwardRoundTrip_bracket
#print axioms PentagonAdjoinedSixCell.selectedV591BackwardRoundTrip_bracket
#print axioms PentagonAdjoinedSixCell.selectedV591SingleUnitSourceRoundTrips
#print axioms PentagonAdjoinedSixCell.selectedV591ActualLeftUnitTwoRoundTrips
#print axioms PentagonAdjoinedSixCell.selectedV591ActualRightUnitTwoRoundTrips
#print axioms PentagonAdjoinedSixCell.selectedV591BracketCollision_requiresTwoUnits
#print axioms PentagonAdjoinedSixCell.selectedV591OldClassCollision_requiresTwoUnits
#print axioms PentagonAdjoinedSixCell.selectedV591NewClassCollision_requiresTwoUnits
#print axioms PentagonAdjoinedSixCell.selectedV591OldTypedCollision_requiresTwoUnits
#print axioms PentagonAdjoinedSixCell.selectedV591NewTypedCollision_requiresTwoUnits

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
