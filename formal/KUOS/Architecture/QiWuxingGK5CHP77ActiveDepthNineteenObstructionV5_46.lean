import KUOS.Architecture.QiWuxingGK5CHP77FourNineteenReverseLeftObstructionV5_45

/-!
Qi v5.46 — active chain DEPTH as a sixth exact-fiber selected
19D quotient observable after the four-coordinate boundary
and the independent ReverseLeftCount obstruction.

The old five actual selected local 19D comparison constructors
preserve the sum of ancestor/descendant pairs of active raw
18D chain nodes. This value is NOT the old ActiveChainCount:
it records nesting depth as distinct typed proof history.
Its Quotient.lift is constructed with actual Type-valued 19D
proof comparisons, not observational or global gluing axioms.

A further concrete same-17D-fiber witness is built from
B = chain X (reverse X) and A = reverse B and strict J.
The two bracketings chain (chain A B) (strict J) and
chain A (chain B (strict J)) have the same ordered trace,
active chain count, raw reverse-node count, left nested
count and reverse-left count. Their active-depth values,
however, differ by the genuinely positive ActiveChain(B).
This supplies a new obstruction to the four-observable
boundary AND to the five-observable observation that also
records ReverseLeftCount, without adding unrestricted
associativity or 20D gluing.

The original F55/P77/GK5CG, 6D–19D Type values,
independent selected presentations, public root107,
pinned Lean/mathlib and protected #1558 are unchanged.
Append-only / tighten-only / overwrite-forbidden / same-root.
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

/-- Total number of strict ancestor/descendant pairs of ACTIVE
chain nodes in the raw contextual proof tree. -/
def selectedContextEighteenActiveDepth (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ M => selectedContextEighteenActiveDepth l r M
  | .whiskerRight _ _ M _ => selectedContextEighteenActiveDepth l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenActiveDepth l r M
  | .chain M L =>
      selectedContextEighteenActiveDepth l r M +
        selectedContextEighteenActiveDepth l r L +
        selectedContextEighteenActiveChainCount l r M +
        selectedContextEighteenActiveChainCount l r L

/-- Check all FIVE genuine 19D comparison constructors, including
the two old inherited-only unit insertions, without new axioms. -/
theorem selectedLocalNineteen_preservesActiveDepth (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenActiveDepth l r M =
      selectedContextEighteenActiveDepth l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Exact-dependent-fiber descent. Not an assertion of raw 18D
proof equality or inter-fiber 20D coherence. -/
def selectedNineteenActiveDepthOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenActiveDepth l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesActiveDepth l r A)

/-- ActiveDepth is evaluated on the ORIGINAL raw contextual
proof value, not on a fabricated or erased replacement. -/
theorem selectedNineteenActiveDepth_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenActiveDepthOnQuotient l r J N
      (selectedNineteenClass l r M) =
      selectedContextEighteenActiveDepth l r M :=
  rfl

section DepthBrackets

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Genuine self-loop B from the old typed contextual witness. -/
def selectedDepthLoop
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J J :=
  .chain M (.reverse M)

/-- The two exact-same-fiber raw 18D bracketings.
A = reverse B has top reverse and B has top chain. -/
def selectedDepthBracketLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J J :=
  .chain (.chain (.reverse (selectedDepthLoop l r M))
      (selectedDepthLoop l r M)) (.strict J)

def selectedDepthBracketRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J J :=
  .chain (.reverse (selectedDepthLoop l r M))
    (.chain (selectedDepthLoop l r M) (.strict J))

/-- The SAME complete ordered original exterior history. -/
theorem selectedDepthBrackets_trace
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenTrace l r (selectedDepthBracketRight l r M) := by
  change ((selectedContextEighteenTrace l r (selectedDepthLoop l r M) ++
      selectedContextEighteenTrace l r (selectedDepthLoop l r M)) ++ []) =
    selectedContextEighteenTrace l r (selectedDepthLoop l r M) ++
      (selectedContextEighteenTrace l r (selectedDepthLoop l r M) ++ [])
  simp only [List.append_assoc]

/-- The reverse nodes are identical in both bracketings. -/
theorem selectedDepthBrackets_reverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseCount l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenReverseCount l r (selectedDepthBracketRight l r M) := by
  change ((selectedContextEighteenReverseCount l r (selectedDepthLoop l r M) + 1) +
      selectedContextEighteenReverseCount l r (selectedDepthLoop l r M)) + 0 =
    (selectedContextEighteenReverseCount l r (selectedDepthLoop l r M) + 1) +
      (selectedContextEighteenReverseCount l r (selectedDepthLoop l r M) + 0)
  omega

/-- Left-nesting count in the two proof values is the same:
their one extra left-nested node occurs at DIFFERENT positions. -/
theorem selectedDepthBrackets_leftNested
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenLeftNestedCount l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenLeftNestedCount l r (selectedDepthBracketRight l r M) := by
  let n := selectedContextEighteenLeftNestedCount l r (selectedDepthLoop l r M)
  change (n + n + 0) + 0 + 1 = n + (n + 0 + 1) + 0
  omega

/-- The v5.45 fifth observation ReverseLeftCount is ALSO equal:
left bracket contributes at the inner node, right at the outer. -/
theorem selectedDepthBrackets_reverseLeft
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseLeftCount l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenReverseLeftCount l r (selectedDepthBracketRight l r M) := by
  let n := selectedContextEighteenReverseLeftCount l r (selectedDepthLoop l r M)
  change (n + n + 1) + 0 + 0 = n + (n + 0 + 0) + 1
  omega

/-- The old typed loop has nonempty exterior history whenever
its actual input proof has an exterior event. -/
theorem selectedDepthLoop_tracePositive
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    0 < (selectedContextEighteenTrace l r (selectedDepthLoop l r M)).length := by
  change 0 < (selectedContextEighteenTrace l r M ++
    selectedContextEighteenTrace l r M).length
  simp only [List.length_append]
  omega

/-- Both bracketings have precisely the same active-chain
count; no new local associativity comparison is postulated. -/
theorem selectedDepthBrackets_active
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedContextEighteenActiveChainCount l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenActiveChainCount l r (selectedDepthBracketRight l r M) := by
  let B := selectedDepthLoop l r M
  let t := (selectedContextEighteenTrace l r B).length
  let a := selectedContextEighteenActiveChainCount l r B
  have ht : 0 < t := selectedDepthLoop_tracePositive l r M hpos
  change (a + a + (if 0 < t + t then 1 else 0)) + 0 +
      (if 0 < (selectedContextEighteenTrace l r B ++
          selectedContextEighteenTrace l r B).length + 0 then 1 else 0) =
    a + (a + 0 + (if 0 < t + 0 then 1 else 0)) +
      (if 0 < t +
          (selectedContextEighteenTrace l r B ++ []).length then 1 else 0)
  dsimp only [t] at ht ⊢
  simp only [List.length_append, List.length_nil, Nat.add_zero]
  have hsum : 0 < (selectedContextEighteenTrace l r B).length +
      (selectedContextEighteenTrace l r B).length := by omega
  simp only [if_pos ht, if_pos hsum]
  all_goals omega

/-- The active depth changes by exactly the positive active
count of the old source loop B, despite all former observations
remaining equal. -/
theorem selectedDepthBrackets_depthDiff
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedContextEighteenActiveDepth l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenActiveDepth l r (selectedDepthBracketRight l r M) +
        selectedContextEighteenActiveChainCount l r (selectedDepthLoop l r M) := by
  let B := selectedDepthLoop l r M
  let d := selectedContextEighteenActiveDepth l r B
  let a := selectedContextEighteenActiveChainCount l r B
  let t := (selectedContextEighteenTrace l r B).length
  have ht : 0 < t := selectedDepthLoop_tracePositive l r M hpos
  have htwo : 0 < t + t := by omega
  have hleft : selectedContextEighteenActiveChainCount l r
      (SelectedContextualEighteen.chain (.reverse B) B) = a + a + 1 := by
    change a + a + (if 0 < t + t then 1 else 0) = a + a + 1
    simp only [if_pos htwo]
  have hright : selectedContextEighteenActiveChainCount l r
      (SelectedContextualEighteen.chain B (.strict J)) = a + 1 := by
    change a + 0 + (if 0 < t + 0 then 1 else 0) = a + 1
    simp [ht]
  change (d + d + a + a) + 0 +
      selectedContextEighteenActiveChainCount l r
        (SelectedContextualEighteen.chain (.reverse B) B) + 0 =
    d + (d + 0 + a + 0) + a +
      selectedContextEighteenActiveChainCount l r
        (SelectedContextualEighteen.chain B (.strict J)) + a
  rw [hleft, hright]
  omega

theorem selectedDepthLoop_activePositive
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    0 < selectedContextEighteenActiveChainCount l r (selectedDepthLoop l r M) := by
  let a := selectedContextEighteenActiveChainCount l r M
  have htwo : 0 < (selectedContextEighteenTrace l r M).length +
      (selectedContextEighteenTrace l r M).length := by omega
  change 0 < a + a +
    (if 0 < (selectedContextEighteenTrace l r M).length +
      (selectedContextEighteenTrace l r M).length then 1 else 0)
  simp only [if_pos htwo]
  omega

/-- The two actual same-fiber proof values have unequal active
depths, even though their four- and five-coordinate observations
will be shown identical. -/
theorem selectedDepthBrackets_depthDistinct
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedContextEighteenActiveDepth l r (selectedDepthBracketLeft l r M) ≠
      selectedContextEighteenActiveDepth l r (selectedDepthBracketRight l r M) := by
  intro h
  rw [selectedDepthBrackets_depthDiff l r M hpos] at h
  have hp := selectedDepthLoop_activePositive l r M hpos
  omega

/-- Equality of the four genuine quotient-stable coordinates
is preserved by these two different raw proof bracketings. -/
theorem selectedDepthBrackets_fourEq
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedContextEighteenFour l r (selectedDepthBracketLeft l r M) =
      selectedContextEighteenFour l r (selectedDepthBracketRight l r M) := by
  exact Prod.ext
    (Prod.ext
      (Prod.ext
        (congrArg List.length (selectedDepthBrackets_trace l r M))
        (selectedDepthBrackets_active l r M hpos))
      (selectedDepthBrackets_reverse l r M))
    (selectedDepthBrackets_leftNested l r M)

/-- Actual old 19D comparison values cannot relate these raw
terms, since the fifth-independent depth quotient separates them. -/
theorem selectedDepthBrackets_classDistinct
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedNineteenClass l r (selectedDepthBracketLeft l r M) ≠
      selectedNineteenClass l r (selectedDepthBracketRight l r M) := by
  intro h
  have hc := congrArg (selectedNineteenActiveDepthOnQuotient l r _ _) h
  change selectedContextEighteenActiveDepth l r (selectedDepthBracketLeft l r M) =
    selectedContextEighteenActiveDepth l r (selectedDepthBracketRight l r M) at hc
  exact (selectedDepthBrackets_depthDistinct l r M hpos) hc

/-- The actual selected-local 19D Type-valued proof remains
uninhabited between the two equal-observation raw bracketings. -/
theorem selectedDepthBrackets_noLocal
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedDepthBracketLeft l r M)
      (selectedDepthBracketRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedDepthBrackets_classDistinct l r M hpos) (Quotient.sound ⟨A⟩)

/-- Five-dimensional observable: the v5.45 FOUR coordinates
together with its separately descended ReverseLeftCount. -/
def selectedNineteenFiveObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      (((Nat × Nat) × Nat) × Nat) × Nat :=
  fun q => (selectedNineteenFourObservation l r J N q,
    selectedNineteenReverseLeftOnQuotient l r J N q)

/-- The two true source classes have equal five-observations,
including reverse-left, but remain distinct by active depth. -/
theorem selectedDepthBrackets_fiveEq
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedNineteenFiveObservation l r J J
      (selectedNineteenClass l r (selectedDepthBracketLeft l r M)) =
    selectedNineteenFiveObservation l r J J
      (selectedNineteenClass l r (selectedDepthBracketRight l r M)) := by
  change (selectedContextEighteenFour l r (selectedDepthBracketLeft l r M),
      selectedContextEighteenReverseLeftCount l r (selectedDepthBracketLeft l r M)) =
    (selectedContextEighteenFour l r (selectedDepthBracketRight l r M),
      selectedContextEighteenReverseLeftCount l r (selectedDepthBracketRight l r M))
  exact Prod.ext (selectedDepthBrackets_fourEq l r M hpos)
    (selectedDepthBrackets_reverseLeft l r M)

/-- Concrete proof that the actual five-number observation
has NONTRIVIAL fibers for every source proof with nonempty history.
No inference to nonexistence of every possible faithful boundary. -/
theorem selectedNineteenFive_notInjective_of_tracePositive
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    ¬ Function.Injective (selectedNineteenFiveObservation l r J J) := by
  intro hi
  exact (selectedDepthBrackets_classDistinct l r M hpos)
    (hi (selectedDepthBrackets_fiveEq l r M hpos))

end DepthBrackets

#print axioms PentagonAdjoinedSixCell.selectedDepthLoop_tracePositive
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_active
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_depthDiff
#print axioms PentagonAdjoinedSixCell.selectedDepthLoop_activePositive
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_depthDistinct
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_fourEq
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_noLocal
#print axioms PentagonAdjoinedSixCell.selectedNineteenFiveObservation
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_fiveEq
#print axioms PentagonAdjoinedSixCell.selectedNineteenFive_notInjective_of_tracePositive
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenActiveDepth
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesActiveDepth
#print axioms PentagonAdjoinedSixCell.selectedNineteenActiveDepthOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedNineteenActiveDepth_onClass
#print axioms PentagonAdjoinedSixCell.selectedDepthLoop
#print axioms PentagonAdjoinedSixCell.selectedDepthBracketLeft
#print axioms PentagonAdjoinedSixCell.selectedDepthBracketRight
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_trace
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_reverse
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_leftNested
#print axioms PentagonAdjoinedSixCell.selectedDepthBrackets_reverseLeft
end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
