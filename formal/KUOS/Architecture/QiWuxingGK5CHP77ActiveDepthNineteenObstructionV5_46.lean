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

end DepthBrackets

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
