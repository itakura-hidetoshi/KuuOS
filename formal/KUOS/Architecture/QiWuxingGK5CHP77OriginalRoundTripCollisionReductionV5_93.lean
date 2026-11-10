import KUOS.Architecture.QiWuxingGK5CHP77OriginalUnitParameterHistoryV5_92

/-!
Qi v5.93 — exact one-unit source-ambiguity criterion for genuinely
typed TWO-unit roundtrip fingerprint collisions in TWO SEPARATE
original old18D raw17D endpoint fibers.

Start with actual original dependent old18D source values
M L : SelectedLocalEighteen W l r J N.
Without inventing any equality between distinct raw17D endpoints,
prove that each ACTUAL old18D roundtrip constructor

  forward(M)  = chain M (reverse M) : J -> J
  backward(M) = chain (reverse M) M : N -> N

both REFLECT raw proof equality and reflect equality of the
nonassociative v5.73 original inner-bracket observation.
Thus a collision in the selected roundtrip IMAGE is equivalent
to an actual source collision in the SAME original J->N Type.

If an original source-pair collision with exactly one unit atom
were genuinely supplied, it would generate TWO genuine two-unit
same-fiber collisions, one in J->J and one in N->N; v5.91 proves
J != N. We do NOT assert that the required source-pair collision
exists. No unsupported gluing of those two different fibers,
selected19 equivalence or global WORLD/20D authority is claimed.

This is a conditional exact criterion, not a construction of a
same-bracket collision. The independent NO_DATA of actual one-unit
source-pair ambiguity is exposed rather than silently discharged.

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

section SourcePairRoundtripReflection

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The actual original dependent old18D chain constructor is
injective in its first explicit raw proof argument when the genuine
J,N indices are fixed. No reverse-involution equation is used. -/
theorem selectedV593ForwardRoundTrip_rawEq_iff
    (M L : SelectedLocalEighteen W l r J N) :
    selectedV591ForwardRoundTrip l r M =
        selectedV591ForwardRoundTrip l r L ↔ M = L := by
  constructor
  · intro h
    change (SelectedLocalEighteen.chain M (.reverse M) :
        SelectedLocalEighteen W l r J J) =
      SelectedLocalEighteen.chain L (.reverse L) at h
    injection h with hfirst hsecond
  · intro h
    cases h
    rfl

/-- Independent reverse-then-chain source-equality reflection,
now in the genuine OTHER N->N raw17D fiber. -/
theorem selectedV593BackwardRoundTrip_rawEq_iff
    (M L : SelectedLocalEighteen W l r J N) :
    selectedV591BackwardRoundTrip l r M =
        selectedV591BackwardRoundTrip l r L ↔ M = L := by
  constructor
  · intro h
    change (SelectedLocalEighteen.chain (.reverse M) M :
        SelectedLocalEighteen W l r N N) =
      SelectedLocalEighteen.chain (.reverse L) L at h
    injection h with hfirst hsecond
  · intro h
    cases h
    rfl

/-- Forward roundtrip nonassociative source-inner-bracket equality
is equivalent to equality of the ORIGINAL source brackets.
This is NOT a statement about original source raw proof equality. -/
theorem selectedV593ForwardRoundTrip_bracketEq_iff
    (M L : SelectedLocalEighteen W l r J N) :
    selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r L) ↔
      selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L := by
  constructor
  · intro h
    change SelectedInheritedOldInnerBracket.oldJoined
        (selectedLocalEighteenInnerBracket l r M)
        (.oldReversed (selectedLocalEighteenInnerBracket l r M)) =
      .oldJoined
        (selectedLocalEighteenInnerBracket l r L)
        (.oldReversed (selectedLocalEighteenInnerBracket l r L)) at h
    injection h with hfirst hsecond
  · intro h
    change SelectedInheritedOldInnerBracket.oldJoined
        (selectedLocalEighteenInnerBracket l r M)
        (.oldReversed (selectedLocalEighteenInnerBracket l r M)) =
      .oldJoined
        (selectedLocalEighteenInnerBracket l r L)
        (.oldReversed (selectedLocalEighteenInnerBracket l r L))
    exact congrArg
      (fun b : SelectedInheritedOldInnerBracket =>
        SelectedInheritedOldInnerBracket.oldJoined b (.oldReversed b)) h

/-- Backward roundtrip fingerprint equality reflects source
fingerprint equality independently, not by identifying its
endpoint fiber with the forward fiber. -/
theorem selectedV593BackwardRoundTrip_bracketEq_iff
    (M L : SelectedLocalEighteen W l r J N) :
    selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r L) ↔
      selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L := by
  constructor
  · intro h
    change SelectedInheritedOldInnerBracket.oldJoined
        (.oldReversed (selectedLocalEighteenInnerBracket l r M))
        (selectedLocalEighteenInnerBracket l r M) =
      .oldJoined
        (.oldReversed (selectedLocalEighteenInnerBracket l r L))
        (selectedLocalEighteenInnerBracket l r L) at h
    injection h with hfirst hsecond
  · intro h
    change SelectedInheritedOldInnerBracket.oldJoined
        (.oldReversed (selectedLocalEighteenInnerBracket l r M))
        (selectedLocalEighteenInnerBracket l r M) =
      .oldJoined
        (.oldReversed (selectedLocalEighteenInnerBracket l r L))
        (selectedLocalEighteenInnerBracket l r L)
    exact congrArg
      (fun b : SelectedInheritedOldInnerBracket =>
        SelectedInheritedOldInnerBracket.oldJoined (.oldReversed b) b) h

/-- EXACT collision equivalence in the forward roundtrip image:
a same-bracket/different-raw forward pair exists exactly for a
same-bracket/different-raw original source pair supplied at J->N. -/
theorem selectedV593ForwardRoundTrip_collision_iff
    (M L : SelectedLocalEighteen W l r J N) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r L) ∧
      selectedV591ForwardRoundTrip l r M ≠
        selectedV591ForwardRoundTrip l r L) ↔
    (selectedLocalEighteenInnerBracket l r M =
       selectedLocalEighteenInnerBracket l r L ∧ M ≠ L) := by
  constructor
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV593ForwardRoundTrip_bracketEq_iff l r M L).mp hbr, ?_⟩
    intro h
    exact hne ((selectedV593ForwardRoundTrip_rawEq_iff l r M L).mpr h)
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV593ForwardRoundTrip_bracketEq_iff l r M L).mpr hbr, ?_⟩
    intro h
    exact hne ((selectedV593ForwardRoundTrip_rawEq_iff l r M L).mp h)

/-- Same exact collision equivalence inside the independently
indexed reverse roundtrip image N->N. -/
theorem selectedV593BackwardRoundTrip_collision_iff
    (M L : SelectedLocalEighteen W l r J N) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r L) ∧
      selectedV591BackwardRoundTrip l r M ≠
        selectedV591BackwardRoundTrip l r L) ↔
    (selectedLocalEighteenInnerBracket l r M =
       selectedLocalEighteenInnerBracket l r L ∧ M ≠ L) := by
  constructor
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV593BackwardRoundTrip_bracketEq_iff l r M L).mp hbr, ?_⟩
    intro h
    exact hne ((selectedV593BackwardRoundTrip_rawEq_iff l r M L).mpr h)
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV593BackwardRoundTrip_bracketEq_iff l r M L).mpr hbr, ?_⟩
    intro h
    exact hne ((selectedV593BackwardRoundTrip_rawEq_iff l r M L).mp h)

/-- Exactly one source unit creates exactly two genuinely original
unit atoms in its own forward roundtrip, by the certified v5.91 count. -/
theorem selectedV593ForwardTwoUnits_ofOne
    (M : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1) :
    selectedV589OriginalUnitCount l r
      (selectedV591ForwardRoundTrip l r M) = 2 := by
  rw [selectedV591ForwardRoundTrip_unitCount l r M, hone]

theorem selectedV593BackwardTwoUnits_ofOne
    (M : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1) :
    selectedV589OriginalUnitCount l r
      (selectedV591BackwardRoundTrip l r M) = 2 := by
  rw [selectedV591BackwardRoundTrip_unitCount l r M, hone]

/-- An equal-source-bracket pair with one original unit on the
left automatically has one on the right. No unit-source pair's
existence is inferred from this conditional theorem. -/
theorem selectedV593BracketEq_oneUnitOnBoth
    (M L : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L) :
    selectedV589OriginalUnitCount l r L = 1 := by
  exact (selectedV590BracketEq_originalCountEq l r M L hbr).symm.trans hone

/-- CONDITIONAL sharp reduction: if two DISTINCT original J->N
one-unit witnesses with the SAME original bracket are supplied,
they yield distinct original old18D two-unit loops with SAME
bracket in BOTH endpoint fibers, with J != N certified.

The premise is not constructed. In particular it does not
prove a same-fiber collision exists without that premise. -/
theorem selectedV593OneUnitSourceAmbiguity_givesDualTwoUnitCollisions
    (M L : SelectedLocalEighteen W l r J N)
    (hone : selectedV589OriginalUnitCount l r M = 1)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hne : M ≠ L) :
    J ≠ N ∧
    (selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r L) ∧
      selectedV591ForwardRoundTrip l r M ≠
        selectedV591ForwardRoundTrip l r L ∧
      selectedV589OriginalUnitCount l r
        (selectedV591ForwardRoundTrip l r M) = 2 ∧
      selectedV589OriginalUnitCount l r
        (selectedV591ForwardRoundTrip l r L) = 2) ∧
    (selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r L) ∧
      selectedV591BackwardRoundTrip l r M ≠
        selectedV591BackwardRoundTrip l r L ∧
      selectedV589OriginalUnitCount l r
        (selectedV591BackwardRoundTrip l r M) = 2 ∧
      selectedV589OriginalUnitCount l r
        (selectedV591BackwardRoundTrip l r L) = 2) := by
  have honeL := selectedV593BracketEq_oneUnitOnBoth l r M L hone hbr
  have hf := (selectedV593ForwardRoundTrip_collision_iff l r M L).mpr
    ⟨hbr, hne⟩
  have hb := (selectedV593BackwardRoundTrip_collision_iff l r M L).mpr
    ⟨hbr, hne⟩
  refine ⟨selectedV591OneUnitEndpointsDistinct l r M hone,
    ⟨hf.1, hf.2, selectedV593ForwardTwoUnits_ofOne l r M hone,
      selectedV593ForwardTwoUnits_ofOne l r L honeL⟩,
    ⟨hb.1, hb.2, selectedV593BackwardTwoUnits_ofOne l r M hone,
      selectedV593BackwardTwoUnits_ofOne l r L honeL⟩⟩

end SourcePairRoundtripReflection

section ExactConditionalExistence

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Does the ACTUAL fixed genuine source Type contain two
one-unit, same-fingerprint, raw-distinct values? A proposition,
NOT a constructed witness. -/
def selectedV593OneUnitSourceCollisionExists
    (J N : SelectedContextualSeventeen W l r H K) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV589OriginalUnitCount l r M = 1 ∧
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L ∧
    M ≠ L

/-- Existential collision of FORWARD genuine two-unit loops
restricted to source pairs with a one-unit original witness.
The roundtrip loops are at J->J, not in a fabricated 17D fiber. -/
def selectedV593ForwardTwoUnitCollisionExists
    (J N : SelectedContextualSeventeen W l r H K) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV589OriginalUnitCount l r M = 1 ∧
    selectedLocalEighteenInnerBracket l r
      (selectedV591ForwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591ForwardRoundTrip l r L) ∧
    selectedV591ForwardRoundTrip l r M ≠
      selectedV591ForwardRoundTrip l r L

/-- Existential collision of BACKWARD genuine two-unit loops
restricted to source pairs with a one-unit original witness, at
the separately indexed N->N fiber. -/
def selectedV593BackwardTwoUnitCollisionExists
    (J N : SelectedContextualSeventeen W l r H K) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV589OriginalUnitCount l r M = 1 ∧
    selectedLocalEighteenInnerBracket l r
      (selectedV591BackwardRoundTrip l r M) =
      selectedLocalEighteenInnerBracket l r
        (selectedV591BackwardRoundTrip l r L) ∧
    selectedV591BackwardRoundTrip l r M ≠
      selectedV591BackwardRoundTrip l r L

/-- EXACT existence iff for the ORIGINAL forward roundtrip
IMAGE, without asserting that either side is inhabited. -/
theorem selectedV593ForwardTwoUnitCollisionExists_iff
    (J N : SelectedContextualSeventeen W l r H K) :
    selectedV593ForwardTwoUnitCollisionExists l r J N ↔
      selectedV593OneUnitSourceCollisionExists l r J N := by
  constructor
  · rintro ⟨M, L, hone, hbr, hne⟩
    have h := (selectedV593ForwardRoundTrip_collision_iff l r M L).mp
      ⟨hbr, hne⟩
    exact ⟨M, L, hone, h.1, h.2⟩
  · rintro ⟨M, L, hone, hbr, hne⟩
    have h := (selectedV593ForwardRoundTrip_collision_iff l r M L).mpr
      ⟨hbr, hne⟩
    exact ⟨M, L, hone, h.1, h.2⟩

/-- The separately indexed backward roundtrip IMAGE has the
same exact genuine source-pair existence criterion. -/
theorem selectedV593BackwardTwoUnitCollisionExists_iff
    (J N : SelectedContextualSeventeen W l r H K) :
    selectedV593BackwardTwoUnitCollisionExists l r J N ↔
      selectedV593OneUnitSourceCollisionExists l r J N := by
  constructor
  · rintro ⟨M, L, hone, hbr, hne⟩
    have h := (selectedV593BackwardRoundTrip_collision_iff l r M L).mp
      ⟨hbr, hne⟩
    exact ⟨M, L, hone, h.1, h.2⟩
  · rintro ⟨M, L, hone, hbr, hne⟩
    have h := (selectedV593BackwardRoundTrip_collision_iff l r M L).mpr
      ⟨hbr, hne⟩
    exact ⟨M, L, hone, h.1, h.2⟩

/-- The TWO original endpoint-fiber roundtrip-image collision
existence conditions are equivalent, but this is NOT a claim
that J= N or that the original proofs in the fibers are equal. -/
theorem selectedV593TwoRoundTripCollisionExists_iff
    (J N : SelectedContextualSeventeen W l r H K) :
    selectedV593ForwardTwoUnitCollisionExists l r J N ↔
      selectedV593BackwardTwoUnitCollisionExists l r J N := by
  exact (selectedV593ForwardTwoUnitCollisionExists_iff l r J N).trans
    (selectedV593BackwardTwoUnitCollisionExists_iff l r J N).symm

end ExactConditionalExistence

#print axioms PentagonAdjoinedSixCell.selectedV593ForwardRoundTrip_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV593BackwardRoundTrip_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV593ForwardRoundTrip_bracketEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV593BackwardRoundTrip_bracketEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV593ForwardRoundTrip_collision_iff
#print axioms PentagonAdjoinedSixCell.selectedV593BackwardRoundTrip_collision_iff
#print axioms PentagonAdjoinedSixCell.selectedV593ForwardTwoUnits_ofOne
#print axioms PentagonAdjoinedSixCell.selectedV593BackwardTwoUnits_ofOne
#print axioms PentagonAdjoinedSixCell.selectedV593BracketEq_oneUnitOnBoth
#print axioms PentagonAdjoinedSixCell.selectedV593OneUnitSourceAmbiguity_givesDualTwoUnitCollisions
#print axioms PentagonAdjoinedSixCell.selectedV593OneUnitSourceCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV593ForwardTwoUnitCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV593BackwardTwoUnitCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV593ForwardTwoUnitCollisionExists_iff
#print axioms PentagonAdjoinedSixCell.selectedV593BackwardTwoUnitCollisionExists_iff
#print axioms PentagonAdjoinedSixCell.selectedV593TwoRoundTripCollisionExists_iff

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
