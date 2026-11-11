import KUOS.Architecture.QiWuxingGK5CHP77OriginalStrictPaddingCollisionReflectionV5_95

/-!
Qi v5.96 — genuine old18D mixed strict-padding orientation obstruction.

Work only in the SAME actual original dependent old18D J->N fiber.
For genuine source M,L with the SAME original nonassociative v5.73
bracket and a positive original unit count, a left strict padding
of M and a right strict padding of L have identical source bracket
if and only if BOTH padding lengths are zero.

This is more precise than v5.95's same-orientation rigidity:
the two OPPOSITE placements cannot secretly generate a new
same-bracket source collision after any nonzero padding.  The
full ORIGINAL v5.92 dependent unit history, with its actual
before/F/G/C/after source parameters and typed raw17D endpoints,
still agrees when it agreed for M and L.

The same statement yields an impossibility theorem for a deliberately
restricted mixed-padding ONE-UNIT collision presentation, without
settling the unresolved genuine v5.93 source collision existence.
Actual unitLeft / unitRight original generators are checked separately.

No cross-fiber equality, extra 19D comparison, quotient relation,
source type change, root change, or global WORLD descent occurs.
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

section SameOriginalFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (M L : SelectedLocalEighteen W l r J N)

/-- Any genuine ORIGINAL unit-bearing old18D proof has an
actual v5.73 inner-bracket different from a bare strict leaf.
Unlike an untyped source tag, this uses its true original unit count. -/
theorem selectedV596PositiveUnitBracket_neStrict
    (hunit : 0 < selectedV589OriginalUnitCount l r M) :
    selectedLocalEighteenInnerBracket l r M ≠
      SelectedInheritedOldInnerBracket.oldStrict := by
  intro hbr
  have hz :
      selectedV588InnerUnitCount
          (selectedLocalEighteenInnerBracket l r M) = 0 := by
    rw [hbr]
    rfl
  have ho := selectedV589OriginalUnitCount_observed l r M
  omega

/-- At every POSITIVE common index, the top left branch of a
prefix is the strict leaf, whereas the top left branch of a
suffix still contains a positive unit count from the ORIGINAL L.
This does not require an equality between M and L. -/
theorem selectedV596PositiveMixedAtSameIndex_bracketNe
    (n : Nat) (hn : 0 < n)
    (hLunit : 0 < selectedV589OriginalUnitCount l r L) :
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M n) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n) := by
  cases n with
  | zero => omega
  | succ k =>
      intro hbr
      change SelectedInheritedOldInnerBracket.oldJoined
          .oldStrict
          (selectedLocalEighteenInnerBracket l r
            (selectedV594StrictPrefix l r J M k)) =
        .oldJoined
          (selectedLocalEighteenInnerBracket l r
            (selectedV594StrictSuffix l r N L k))
          .oldStrict at hbr
      have hleft :
          SelectedInheritedOldInnerBracket.oldStrict =
            selectedLocalEighteenInnerBracket l r
              (selectedV594StrictSuffix l r N L k) := by
        injection hbr with hfirst hsecond
      have hremain :
          0 < selectedV589OriginalUnitCount l r
            (selectedV594StrictSuffix l r N L k) := by
        rw [selectedV594Suffix_unitCount l r J N L k]
        exact hLunit
      exact
        (selectedV596PositiveUnitBracket_neStrict l r J N
          (selectedV594StrictSuffix l r N L k) hremain)
          hleft.symm

/-- A NEW mixed-orientation precise result for genuinely SAME
source brackets: matching padded original brackets forces both
padding lengths to vanish. Equal source strict counts follow from
the ACTUAL source bracket equality; no general cross-source
length rigidity is asserted without that premise. -/
theorem selectedV596MixedCrossIndex_bracketEq_iff
    (hbase : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hunit : 0 < selectedV589OriginalUnitCount l r M)
    (m n : Nat) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n)) ↔
      (m = 0 ∧ n = 0) := by
  constructor
  · intro hbr
    have hc := congrArg selectedV594InnerStrictCount hbr
    rw [selectedV594Prefix_innerStrictCount l r J N M m,
      selectedV594Suffix_innerStrictCount l r J N L n] at hc
    have hsc := congrArg selectedV594InnerStrictCount hbase
    have hmn : m = n := by omega
    subst n
    cases m with
    | zero => exact ⟨rfl, rfl⟩
    | succ k =>
        have hcounts :=
          selectedV590BracketEq_originalCountEq l r M L hbase
        have hLunit : 0 < selectedV589OriginalUnitCount l r L := by
          omega
        exact False.elim
          ((selectedV596PositiveMixedAtSameIndex_bracketNe
            l r J N M L (k + 1) (by omega) hLunit) hbr)
  · rintro ⟨hm, hn⟩
    subst m
    subst n
    change selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L
    exact hbase

/-- The common-bracket-positive-unit restriction makes actual
raw equality across opposite padding orientations equivalent
to the ZERO/ZERO case AND ORIGINAL source raw equality.
This only uses the original old18D Type, never any quotient law. -/
theorem selectedV596MixedCrossIndex_rawEq_iff
    (hbase : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hunit : 0 < selectedV589OriginalUnitCount l r M)
    (m n : Nat) :
    (selectedV594StrictPrefix l r J M m =
      selectedV594StrictSuffix l r N L n) ↔
      (m = 0 ∧ n = 0 ∧ M = L) := by
  constructor
  · intro heq
    have hbr := congrArg (selectedLocalEighteenInnerBracket l r) heq
    obtain ⟨hm, hn⟩ :=
      (selectedV596MixedCrossIndex_bracketEq_iff
        l r J N M L hbase hunit m n).mp hbr
    have hsource : M = L := by
      rw [hm, hn] at heq
      exact heq
    exact ⟨hm, hn, hsource⟩
  · rintro ⟨hm, hn, hsource⟩
    rw [hm, hn]
    exact hsource

/-- In the SAME real old18D fiber, any ORIGINAL source that
contains a genuine unit has two mixed padding families which
share the full typed original unit payload history but have
different brackets and raw proof values as soon as m+n>0. -/
theorem selectedV596PositiveSameSourceMixedGap
    (hunit : 0 < selectedV589OriginalUnitCount l r M)
    (m n : Nat) (hpos : 0 < m + n) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M n) ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M n) ∧
    selectedV594StrictPrefix l r J M m ≠
      selectedV594StrictSuffix l r N M n := by
  have hh := (selectedV595Mixed_historyEq_iff l r J N M M m n).mpr rfl
  have hiff := selectedV596MixedCrossIndex_bracketEq_iff
    l r J N M M rfl hunit m n
  have hbne :
      selectedLocalEighteenInnerBracket l r
          (selectedV594StrictPrefix l r J M m) ≠
        selectedLocalEighteenInnerBracket l r
          (selectedV594StrictSuffix l r N M n) := by
    intro hbr
    have hz := hiff.mp hbr
    omega
  refine ⟨hh, hbne, ?_⟩
  intro hraw
  exact hbne (congrArg (selectedLocalEighteenInnerBracket l r) hraw)

/-- A HYPOTHETICAL one-unit source collision with *identical*
actual typed unit payload histories cannot be converted into
a new cross-orientation equal-bracket collision by positive
strict padding. The premise is NOT constructed. -/
theorem selectedV596ConditionalOneUnitMixedGap
    (hone : selectedV589OriginalUnitCount l r M = 1)
    (hbase : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hhistory : selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r L)
    (hne : M ≠ L)
    (m n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n) ∧
    ((selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n)) ↔
      (m = 0 ∧ n = 0)) ∧
    selectedV594StrictPrefix l r J M m ≠
      selectedV594StrictSuffix l r N L n := by
  have hunit : 0 < selectedV589OriginalUnitCount l r M := by
    omega
  refine ⟨(selectedV595Mixed_historyEq_iff l r J N M L m n).mpr
      hhistory, (selectedV596MixedCrossIndex_bracketEq_iff
      l r J N M L hbase hunit m n), ?_⟩
  intro hraw
  have hdecode := (selectedV596MixedCrossIndex_rawEq_iff
    l r J N M L hbase hunit m n).mp hraw
  exact hne hdecode.2.2

end SameOriginalFiber

section RestrictedMixedCollisionPresentation

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- A deliberately RESTRICTED mixed-prefix/suffix one-unit
source collision presentation. Base source brackets are REQUIRED
to agree; this predicate is not all old18D source collisions. -/
def selectedV596MixedOneUnitCollisionExists
    (J N : SelectedContextualSeventeen W l r H K)
    (m n : Nat) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV589OriginalUnitCount l r M = 1 ∧
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n) ∧
    selectedV594StrictPrefix l r J M m ≠
      selectedV594StrictSuffix l r N L n

/-- Exact classification in this restricted original dependent
presentation: a mixed strict padding collision exists iff it is
entirely unpadded and the still-UNRESOLVED v5.93 original
one-unit collision exists. -/
theorem selectedV596MixedOneUnitCollisionExists_iff
    (J N : SelectedContextualSeventeen W l r H K)
    (m n : Nat) :
    selectedV596MixedOneUnitCollisionExists l r J N m n ↔
      (m = 0 ∧ n = 0 ∧
        selectedV593OneUnitSourceCollisionExists l r J N) := by
  constructor
  · rintro ⟨M, L, hone, hbase, hpadded, hraw⟩
    have hunit : 0 < selectedV589OriginalUnitCount l r M := by
      omega
    obtain ⟨hm, hn⟩ :=
      (selectedV596MixedCrossIndex_bracketEq_iff
        l r J N M L hbase hunit m n).mp hpadded
    have hne : M ≠ L := by
      intro heq
      apply hraw
      rw [hm, hn]
      exact heq
    exact ⟨hm, hn, ⟨M, L, hone, hbase, hne⟩⟩
  · rintro ⟨hm, hn, ⟨M, L, hone, hbase, hne⟩⟩
    subst m
    subst n
    exact ⟨M, L, hone, hbase, hbase, hne⟩

/-- In this precisely specified one-unit same-base-bracket
presentation, EVERY positive mixed padding is IMPOSSIBLE.
The unpadded original v5.93 source collision remains NO_DATA. -/
theorem selectedV596MixedPositiveOneUnitCollision_impossible
    (J N : SelectedContextualSeventeen W l r H K)
    (m n : Nat) (hpos : 0 < m + n) :
    ¬ selectedV596MixedOneUnitCollisionExists l r J N m n := by
  intro h
  obtain ⟨hm, hn, _⟩ :=
    (selectedV596MixedOneUnitCollisionExists_iff
      l r J N m n).mp h
  omega

end RestrictedMixedCollisionPresentation

section GenuineOriginalUnitParameters

variable (l r : W)
variable {w z : W}
variable {b c d e : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable (C : SelectedContextualThirteen W l r P Q)
variable (after : SevenRewrite W l r d e)

/-- The genuine LEFT unit source's v5.92 singleton payload stores
the ORIGINAL raw17D source/target and the actual dependent term,
which retains its exact before/F/G/C/after parameters. -/
theorem selectedV596ActualLeft_originalTypedPayload :
    let J := selectedSeventeenUnitPrependLeft l r before F G C after
    let N := selectedSeventeenUnitAppendLeft l r before F G C after
    let U := SelectedLocalEighteen.unitLeft before F G C after
    selectedV592OriginalUnitHistory l r U =
      [⟨J, ⟨N, U⟩⟩] := by
  rfl

/-- The independent genuine RIGHT unit source has its own actual
raw17D endpoints, without identifying LEFT and RIGHT source Types. -/
theorem selectedV596ActualRight_originalTypedPayload :
    let J := selectedSeventeenUnitPrependRight l r before F G C after
    let N := selectedSeventeenUnitAppendRight l r before F G C after
    let U := SelectedLocalEighteen.unitRight before F G C after
    selectedV592OriginalUnitHistory l r U =
      [⟨J, ⟨N, U⟩⟩] := by
  rfl

/-- Actual left and right unit SOURCES have independently typed
endpoints. Their common observation codomain separates unit side
labels; no ill-typed cross-fiber raw equality is asserted. -/
theorem selectedV596ActualLeftRight_bracketSideDistinct :
    selectedLocalEighteenInnerBracket l r
        (SelectedLocalEighteen.unitLeft before F G C after) ≠
      selectedLocalEighteenInnerBracket l r
        (SelectedLocalEighteen.unitRight before F G C after) := by
  change SelectedInheritedOldInnerBracket.oldUnitLeft ≠ .oldUnitRight
  decide

/-- Concrete genuine original left one-unit source: for ANY
strict prefix/suffix indices with m+n>0, the complete typed
payload histories agree but the exact old18D inner brackets
AND raw dependent proofs differ inside this SAME J->N fiber. -/
theorem selectedV596ActualLeft_positiveMixedGap
    (m n : Nat) (hpos : 0 < m + n) :
    let J := selectedSeventeenUnitPrependLeft l r before F G C after
    let N := selectedSeventeenUnitAppendLeft l r before F G C after
    let U := SelectedLocalEighteen.unitLeft before F G C after
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J U m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N U n) ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J U m) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N U n) ∧
    selectedV594StrictPrefix l r J U m ≠
      selectedV594StrictSuffix l r N U n := by
  dsimp only
  exact selectedV596PositiveSameSourceMixedGap l r
    (selectedSeventeenUnitPrependLeft l r before F G C after)
    (selectedSeventeenUnitAppendLeft l r before F G C after)
    (SelectedLocalEighteen.unitLeft before F G C after)
    (by decide) m n hpos

/-- Right original unit generator, with its own actual before,
frame, comparison and after parameters and endpoint indices. -/
theorem selectedV596ActualRight_positiveMixedGap
    (m n : Nat) (hpos : 0 < m + n) :
    let J := selectedSeventeenUnitPrependRight l r before F G C after
    let N := selectedSeventeenUnitAppendRight l r before F G C after
    let U := SelectedLocalEighteen.unitRight before F G C after
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J U m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N U n) ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J U m) ≠
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N U n) ∧
    selectedV594StrictPrefix l r J U m ≠
      selectedV594StrictSuffix l r N U n := by
  dsimp only
  exact selectedV596PositiveSameSourceMixedGap l r
    (selectedSeventeenUnitPrependRight l r before F G C after)
    (selectedSeventeenUnitAppendRight l r before F G C after)
    (SelectedLocalEighteen.unitRight before F G C after)
    (by decide) m n hpos

end GenuineOriginalUnitParameters

#print axioms PentagonAdjoinedSixCell.selectedV596PositiveUnitBracket_neStrict
#print axioms PentagonAdjoinedSixCell.selectedV596PositiveMixedAtSameIndex_bracketNe
#print axioms PentagonAdjoinedSixCell.selectedV596MixedCrossIndex_bracketEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV596MixedCrossIndex_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV596PositiveSameSourceMixedGap
#print axioms PentagonAdjoinedSixCell.selectedV596ConditionalOneUnitMixedGap
#print axioms PentagonAdjoinedSixCell.selectedV596MixedOneUnitCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV596MixedOneUnitCollisionExists_iff
#print axioms PentagonAdjoinedSixCell.selectedV596MixedPositiveOneUnitCollision_impossible
#print axioms PentagonAdjoinedSixCell.selectedV596ActualLeft_originalTypedPayload
#print axioms PentagonAdjoinedSixCell.selectedV596ActualRight_originalTypedPayload
#print axioms PentagonAdjoinedSixCell.selectedV596ActualLeftRight_bracketSideDistinct
#print axioms PentagonAdjoinedSixCell.selectedV596ActualLeft_positiveMixedGap
#print axioms PentagonAdjoinedSixCell.selectedV596ActualRight_positiveMixedGap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
