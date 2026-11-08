import KUOS.Architecture.QiWuxingGK5CHP77InverseContextNaturalityV5_21

/-!
Qi v5.22: original ordered-whisker defect, genuine twelfth
naturality in both orders, and a selected higher coherence cell.

The original 7D through 12D witnesses are never changed.
A defect certificate records precisely the whiskerPrefix added to the
original ordered 10D whiskering history. Its composition reverses
whiskerPrefix order, as required by the original prepend constructors.

For any genuine ORIGINAL v5.17 twelfth proof T : H => K and
any genuine before/after seventh contexts, both doubled
whiskerings of T exist in the old 12D proof Type, but in
DIFFERENT original dependent fibers. Their fully framed square
has four actual 12D edges and two composed 12D routes.

Both routes have the same framed 11D endpoints, but distinct
ORIGINAL 12D syntax. A selected new 13D generator may compare
them WITHOUT identifying the raw 12D paths; neither endpoint
can be connected using ONLY inherited old-fiber twelfth proofs,
because the two true 10D order prefixes are incompatible.

The selected 13D coherence is explicitly NEW presentation data:
no full old 13D coherence, raw Eq, higher thinness, or automatic
8D boundary-associator-to-11D-transport is asserted.
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

/-- Original raw-ordered trace transition: a certified whiskerPrefix is
additional provenance data, NOT an equality of proof terms. -/
structure OrderedWhiskerDefect (source target : List Bool) : Type where
  whiskerPrefix : List Bool
  exact_target : target = whiskerPrefix ++ source

def orderedWhiskerDefectId (t : List Bool) :
    OrderedWhiskerDefect t t :=
  ⟨[], by simp⟩

/-- A later certified ordered whisker prefix is placed before the earlier prefix.
This is a genuine noncommutative composition convention. -/
def orderedWhiskerDefectComp {a b c : List Bool}
    (A : OrderedWhiskerDefect a b)
    (B : OrderedWhiskerDefect b c) :
    OrderedWhiskerDefect a c where
  whiskerPrefix := B.whiskerPrefix ++ A.whiskerPrefix
  exact_target := by
    calc
      c = B.whiskerPrefix ++ b := B.exact_target
      _ = B.whiskerPrefix ++ (A.whiskerPrefix ++ a) :=
        congrArg (fun t : List Bool => B.whiskerPrefix ++ t) A.exact_target
      _ = (B.whiskerPrefix ++ A.whiskerPrefix) ++ a := by simp only [List.append_assoc]

theorem orderedWhiskerDefectComp_prefix {a b c : List Bool}
    (A : OrderedWhiskerDefect a b)
    (B : OrderedWhiskerDefect b c) :
    (orderedWhiskerDefectComp A B).whiskerPrefix = B.whiskerPrefix ++ A.whiskerPrefix := rfl

/-- The certified whisker prefix length is the exact raw trace length
increment. No rewriting through any selected twelfth quotient. -/
theorem orderedWhiskerDefect_length {a b : List Bool}
    (D : OrderedWhiskerDefect a b) :
    b.length = D.whiskerPrefix.length + a.length := by
  calc
    b.length = (D.whiskerPrefix ++ a).length :=
      congrArg List.length D.exact_target
    _ = D.whiskerPrefix.length + a.length := by
      simp only [List.length_append]

/-- A single original left whisker prefixes exactly false. -/
def originalLeftWhiskerDefect (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta) :
    OrderedWhiskerDefect
      (mixedTenWhiskerRawTrace xi)
      (mixedTenWhiskerRawTrace (.whiskerLeft before xi)) :=
  ⟨[false], rfl⟩

/-- A single original right whisker prefixes exactly true. -/
def originalRightWhiskerDefect (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (after : SevenRewrite W l r d e) :
    OrderedWhiskerDefect
      (mixedTenWhiskerRawTrace xi)
      (mixedTenWhiskerRawTrace (.whiskerRight xi after)) :=
  ⟨[true], rfl⟩

/-- Exact two-step certificate, right applied FIRST, left LAST.
The actual seventh boundary is right associated. -/
def doubleWhiskerDefectLeftAfterRight (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (after : SevenRewrite W l r e f₆) :
    OrderedWhiskerDefect
      (mixedTenWhiskerRawTrace xi)
      (mixedTenWhiskerRawTrace
        (.whiskerLeft before (.whiskerRight xi after))) :=
  orderedWhiskerDefectComp
    (originalRightWhiskerDefect l r xi after)
    (originalLeftWhiskerDefect l r before (.whiskerRight xi after))

/-- Exact two-step certificate, left applied FIRST, right LAST.
The actual seventh boundary is left associated. -/
def doubleWhiskerDefectRightAfterLeft (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (after : SevenRewrite W l r e f₆) :
    OrderedWhiskerDefect
      (mixedTenWhiskerRawTrace xi)
      (mixedTenWhiskerRawTrace
        (.whiskerRight (.whiskerLeft before xi) after)) :=
  orderedWhiskerDefectComp
    (originalLeftWhiskerDefect l r before xi)
    (originalRightWhiskerDefect l r (.whiskerLeft before xi) after)

/-- The two genuine raw certified prefixes are opposite ordered
words, although their Nat lengths are identical. -/
theorem doubleWhiskerDefect_orderedValues (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (after : SevenRewrite W l r e f₆) :
    (doubleWhiskerDefectLeftAfterRight l r before xi after).whiskerPrefix =
      [false, true] ∧
    (doubleWhiskerDefectRightAfterLeft l r before xi after).whiskerPrefix =
      [true, false] :=
  ⟨rfl, rfl⟩

theorem doubleWhiskerDefect_notCommutative (t : List Bool) :
    ([false, true] ++ t) ≠ ([true, false] ++ t) := by
  intro h
  cases h

theorem doubleWhiskerDefect_lengthCollision (t : List Bool) :
    ([false, true] ++ t).length = ([true, false] ++ t).length := rfl

/-- Original tenth-trace order is visible at the genuine 11D
frames even where both selected twelfth classes coincide. -/
theorem doubleWhiskerDefect_actualFrameOrder (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    framedWhiskerRawTrace
        (doubleWhiskerLeftAfterRightFrame l r before H after) =
        [false, true] ++ mixedTenWhiskerRawTrace xi ∧
    framedWhiskerRawTrace
        (doubleWhiskerRightAfterLeftFrame l r before H after) =
        [true, false] ++ mixedTenWhiskerRawTrace xi :=
  doubleWhiskerRawTraceValues l r before H after

/-- Two genuine ORIGINAL twelfth whiskerings exist in the
right-then-left dependent original 11D fiber. -/
def originalTwelfthRightThenLeft (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    MixedExchangeInverseTwelveCell W l r
      (.whiskerLeft before (.whiskerRight H after))
      (.whiskerLeft before (.whiskerRight K after)) :=
  .whiskerLeft before (.whiskerRight T after)

/-- Original opposite-order twelfth whiskering has a DIFFERENT
dependent original 11D fiber, not an Eq-cast of the prior type. -/
def originalTwelfthLeftThenRight (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    MixedExchangeInverseTwelveCell W l r
      (.whiskerRight (.whiskerLeft before H) after)
      (.whiskerRight (.whiskerLeft before K) after) :=
  .whiskerRight (.whiskerLeft before T) after

/-- Original twelfth right-then-left gives a framed twelfth
comparison along the upper edge of the true naturality square. -/
def framedTwelfthRightThenLeft (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    FramedDoubleWhiskerTwelveCell W l r
      (doubleWhiskerLeftAfterRightFrame l r before H after)
      (doubleWhiskerLeftAfterRightFrame l r before K after) := by
  change FramedDoubleWhiskerTwelveCell W l r
    (framedEleven_ofRaw l r
      (.whiskerLeft before (.whiskerRight H after)))
    (framedEleven_ofRaw l r
      (.whiskerLeft before (.whiskerRight K after)))
  exact .previous (originalTwelfthRightThenLeft l r before T after)

/-- Original twelfth left-then-right yields the lower edge. -/
def framedTwelfthLeftThenRight (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    FramedDoubleWhiskerTwelveCell W l r
      (doubleWhiskerRightAfterLeftFrame l r before H after)
      (doubleWhiskerRightAfterLeftFrame l r before K after) := by
  change FramedDoubleWhiskerTwelveCell W l r
    (framedEleven_ofRaw l r
      (.whiskerRight (.whiskerLeft before H) after))
    (framedEleven_ofRaw l r
      (.whiskerRight (.whiskerLeft before K) after))
  exact .previous (originalTwelfthLeftThenRight l r before T after)

/-- The first framed 12D route: old transport, then the new
framed interchanger on the transported target K. -/
def framedWhiskerSquareUpperRoute (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    FramedDoubleWhiskerTwelveCell W l r
      (doubleWhiskerLeftAfterRightFrame l r before H after)
      (doubleWhiskerRightAfterLeftFrame l r before K after) :=
  .chain (framedTwelfthRightThenLeft l r before T after)
    (.doubleWhisker before K after)

/-- Second framed 12D route: framed interchanger at H first,
then genuine original opposite-order transported twelfth T. -/
def framedWhiskerSquareLowerRoute (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    FramedDoubleWhiskerTwelveCell W l r
      (doubleWhiskerLeftAfterRightFrame l r before H after)
      (doubleWhiskerRightAfterLeftFrame l r before K after) :=
  .chain (.doubleWhisker before H after)
    (framedTwelfthLeftThenRight l r before T after)

/-- Both framed 12D paths exist, but their ORIGINAL selected raw
twelfth proof syntax is not strictly equal. The equal-target
square is a candidate for a NEW 13D comparison, never an Eq. -/
theorem framedWhiskerSquareRoutes_rawDistinct (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    framedWhiskerSquareUpperRoute l r before T after ≠
      framedWhiskerSquareLowerRoute l r before T after := by
  intro h
  cases h

/-- Noncommuting ordered prefixes prevent ANY inherited-only
old 12D comparison across the diagonal of the square, even
when an actual old twelfth proof T : H => K exists. -/
theorem framedWhiskerSquare_noInheritedDiagonal (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H K : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    ¬ Nonempty (FramedInheritedTwelfth W l r
      (doubleWhiskerLeftAfterRightFrame l r before H after)
      (doubleWhiskerRightAfterLeftFrame l r before K after)) := by
  rintro ⟨U⟩
  have he := framedInheritedTwelfth_preservesSpine l r U
  have ht := congrArg
    (fun S : FramedElevenExactSpine W l r =>
      mixedTenWhiskerRawTrace S.xi) he
  change framedWhiskerRawTrace
      (doubleWhiskerLeftAfterRightFrame l r before H after) =
    framedWhiskerRawTrace
      (doubleWhiskerRightAfterLeftFrame l r before K after) at ht
  rw [(doubleWhiskerRawTraceValues l r before H after).1,
    (doubleWhiskerRawTraceValues l r before K after).2] at ht
  cases ht

/-- Precisely ONE new local 13D primitive fills the genuine old
twelfth/whisker-interchanger naturality square. The raw twelfth
routes and original fiber indices remain untouched. -/
inductive SelectedWhiskerNaturalityThirteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    FramedDoubleWhiskerTwelveCell W l r F G →
    FramedDoubleWhiskerTwelveCell W l r F G → Type uSix where
  | strict {F G : FramedEleven W l r}
      (P : FramedDoubleWhiskerTwelveCell W l r F G) :
      SelectedWhiskerNaturalityThirteen W l r P P
  | naturality {w z : W}
      {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K)
      (after : SevenRewrite W l r e f₆) :
      SelectedWhiskerNaturalityThirteen W l r
        (framedWhiskerSquareUpperRoute l r before T after)
        (framedWhiskerSquareLowerRoute l r before T after)
  | reverse {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : SelectedWhiskerNaturalityThirteen W l r P Q) :
      SelectedWhiskerNaturalityThirteen W l r Q P
  | chain {F G : FramedEleven W l r}
      {P Q R : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : SelectedWhiskerNaturalityThirteen W l r P Q)
      (D : SelectedWhiskerNaturalityThirteen W l r Q R) :
      SelectedWhiskerNaturalityThirteen W l r P R

/-- The selected higher 13D comparison exists at EVERY actual
old twelfth witness T and pair of typed seventh contexts; it
is not an inherited original 12D Eq or universal higher law. -/
theorem selectedWhiskerNaturality_relativeNecessity (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    Nonempty (SelectedWhiskerNaturalityThirteen W l r
      (framedWhiskerSquareUpperRoute l r before T after)
      (framedWhiskerSquareLowerRoute l r before T after)) ∧
    framedWhiskerSquareUpperRoute l r before T after ≠
      framedWhiskerSquareLowerRoute l r before T after :=
  ⟨⟨.naturality before T after⟩,
    framedWhiskerSquareRoutes_rawDistinct l r before T after⟩

/-- Three different levels of authority, simultaneously:
 genuine 8D boundary compatibility, a selected 13D square filler,
 and failure of descent to inherited-only old-fiber comparison.
 No full old 13D coherence or quotient retraction follows. -/
theorem selectedWhiskerNaturality_boundaryAndObstruction (l r : W)
    {w z : W} {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (after : SevenRewrite W l r e f₆) :
    (Nonempty (EightCell W l r
      (.trans before (.trans s after))
      (.trans (.trans before s) after)) ∧
     Nonempty (EightCell W l r
      (.trans before (.trans t after))
      (.trans (.trans before t) after))) ∧
    Nonempty (SelectedWhiskerNaturalityThirteen W l r
      (framedWhiskerSquareUpperRoute l r before T after)
      (framedWhiskerSquareLowerRoute l r before T after)) ∧
    ¬ Nonempty (FramedInheritedTwelfth W l r
      (doubleWhiskerLeftAfterRightFrame l r before H after)
      (doubleWhiskerRightAfterLeftFrame l r before K after)) :=
  ⟨doubleWhiskerBoundaryCompatibility l r before after,
    (selectedWhiskerNaturality_relativeNecessity l r before T after).1,
    framedWhiskerSquare_noInheritedDiagonal l r before H K after⟩

/-- A concrete NONREFLEXIVE original old twelfth witness:
 v5.17 exchange-unit right cancellation. Its two framed
 naturality routes are raw unequal but get exactly ONE selected
 13D generator; no new original old-fiber comparison is made. -/
theorem originalExchangeRightCancellationThirteenCompletion (l r : W) :
    Nonempty (SelectedWhiskerNaturalityThirteen W l r
      (framedWhiskerSquareUpperRoute l r (.refl _)
        (.cancelExchangeRight) (.refl _))
      (framedWhiskerSquareLowerRoute l r (.refl _)
        (.cancelExchangeRight) (.refl _))) ∧
    framedWhiskerSquareUpperRoute l r (.refl _)
        (.cancelExchangeRight) (.refl _) ≠
      framedWhiskerSquareLowerRoute l r (.refl _)
        (.cancelExchangeRight) (.refl _) :=
  selectedWhiskerNaturality_relativeNecessity l r
    (.refl _) (.cancelExchangeRight) (.refl _)

/-- There is no sound interpretation of ALL newly selected
13D naturality certificates as equality of the original raw
framed twelfth paths, witnessed by actual v5.17 cancellation. -/
theorem selectedWhiskerNaturality_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {F G : FramedEleven W l r}
      (P Q : FramedDoubleWhiskerTwelveCell W l r F G),
      SelectedWhiskerNaturalityThirteen W l r P Q → P = Q) := by
  intro interpret
  exact (originalExchangeRightCancellationThirteenCompletion l r).2
    (interpret _ _ (.naturality (.refl _)
      (.cancelExchangeRight) (.refl _)))

#print axioms PentagonAdjoinedSixCell.OrderedWhiskerDefect
#print axioms PentagonAdjoinedSixCell.orderedWhiskerDefectId
#print axioms PentagonAdjoinedSixCell.orderedWhiskerDefectComp
#print axioms PentagonAdjoinedSixCell.orderedWhiskerDefectComp_prefix
#print axioms PentagonAdjoinedSixCell.orderedWhiskerDefect_length
#print axioms PentagonAdjoinedSixCell.originalLeftWhiskerDefect
#print axioms PentagonAdjoinedSixCell.originalRightWhiskerDefect
#print axioms PentagonAdjoinedSixCell.doubleWhiskerDefectLeftAfterRight
#print axioms PentagonAdjoinedSixCell.doubleWhiskerDefectRightAfterLeft
#print axioms PentagonAdjoinedSixCell.doubleWhiskerDefect_orderedValues
#print axioms PentagonAdjoinedSixCell.doubleWhiskerDefect_notCommutative
#print axioms PentagonAdjoinedSixCell.doubleWhiskerDefect_lengthCollision
#print axioms PentagonAdjoinedSixCell.doubleWhiskerDefect_actualFrameOrder
#print axioms PentagonAdjoinedSixCell.originalTwelfthRightThenLeft
#print axioms PentagonAdjoinedSixCell.originalTwelfthLeftThenRight
#print axioms PentagonAdjoinedSixCell.framedTwelfthRightThenLeft
#print axioms PentagonAdjoinedSixCell.framedTwelfthLeftThenRight
#print axioms PentagonAdjoinedSixCell.framedWhiskerSquareUpperRoute
#print axioms PentagonAdjoinedSixCell.framedWhiskerSquareLowerRoute
#print axioms PentagonAdjoinedSixCell.framedWhiskerSquareRoutes_rawDistinct
#print axioms PentagonAdjoinedSixCell.framedWhiskerSquare_noInheritedDiagonal
#print axioms PentagonAdjoinedSixCell.SelectedWhiskerNaturalityThirteen
#print axioms PentagonAdjoinedSixCell.selectedWhiskerNaturality_relativeNecessity
#print axioms PentagonAdjoinedSixCell.selectedWhiskerNaturality_boundaryAndObstruction
#print axioms PentagonAdjoinedSixCell.originalExchangeRightCancellationThirteenCompletion
#print axioms PentagonAdjoinedSixCell.selectedWhiskerNaturality_noRawEqualityInterpreter

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
