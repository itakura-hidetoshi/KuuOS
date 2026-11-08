import KUOS.Architecture.QiWuxingGK5CHP77OrderedWhiskerDefectNaturalityV5_22

/-!
Qi v5.23 — authentic triple-whiskering order traces and conditional
compositional naturality critical cube.

This module never alters the original sixth through twelfth proof grammar,
the v5.18 framed comparison, or the v5.22 selected thirteenth comparison.

Three successive original whiskerings preserve their exact ordered tenth
trace. The old twelfth transport of a vertical composition is NOT the raw
twelfth composition of two transported witnesses. The missing functorial
comparison and horizontal/vertical pasting are therefore introduced in an
explicit, separately typed extension of the selected thirteenth presentation.

Two thirteenth witnesses, one from v5.22 naturality of (T.chain U) and
one from pasting the genuine naturality squares for T and U, share exactly
the same framed twelfth endpoints but retain distinct raw proof histories.
A NEW, explicitly selected fourteenth-cell constructor relates them.
No equality of old twelfth/thirteenth syntax or globally coherent
fourteenth interchange is claimed.
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

/-- An actual original twelfth proof carried through right, left,
and right whiskerings, in that application order. -/
def originalTripleWhiskerRLR (l r : W) {w z : W}
    {b c d e f : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (inner : SevenRewrite W l r d e)
    (outer : SevenRewrite W l r e f) :
    MixedExchangeInverseTwelveCell W l r
      (.whiskerRight (.whiskerLeft before (.whiskerRight H inner)) outer)
      (.whiskerRight (.whiskerLeft before (.whiskerRight K inner)) outer) :=
  .whiskerRight (.whiskerLeft before (.whiskerRight T inner)) outer

/-- A second genuine original twelfth transport, applying the
same contexts as right, right, left. Its raw fiber is not coerced
into the first one's original dependent Type. -/
def originalTripleWhiskerRRL (l r : W) {w z : W}
    {b c d e f : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K)
    (inner : SevenRewrite W l r d e)
    (outer : SevenRewrite W l r e f) :
    MixedExchangeInverseTwelveCell W l r
      (.whiskerRight (.whiskerRight (.whiskerLeft before H) inner) outer)
      (.whiskerRight (.whiskerRight (.whiskerLeft before K) inner) outer) :=
  .whiskerRight (.whiskerRight (.whiskerLeft before T) inner) outer

/-- The actual original tenth witnesses distinguish two
three-step transports by their complete ordered Boolean prefixes. -/
theorem originalTripleWhisker_traceValues (l r : W) {w z : W}
    {b c d e f : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (inner : SevenRewrite W l r d e)
    (outer : SevenRewrite W l r e f) :
    mixedTenWhiskerRawTrace
        (.whiskerRight (.whiskerLeft before (.whiskerRight xi inner)) outer) =
        [true, false, true] ++ mixedTenWhiskerRawTrace xi ∧
    mixedTenWhiskerRawTrace
        (.whiskerRight (.whiskerRight (.whiskerLeft before xi) inner) outer) =
        [true, true, false] ++ mixedTenWhiskerRawTrace xi :=
  ⟨rfl, rfl⟩

theorem originalTripleWhisker_orderObstruction (trace : List Bool) :
    ([true, false, true] ++ trace) ≠
      ([true, true, false] ++ trace) := by
  intro h
  cases h

theorem originalTripleWhisker_lengthCollision (trace : List Bool) :
    ([true, false, true] ++ trace).length =
      ([true, true, false] ++ trace).length := rfl

/-- Add only the missing chosen composition/pasting capabilities to
v5.22's selected 13D presentation. These are NEW presentation
constructors, not equations inherited from the original old twelfth. -/
inductive CompositionalWhiskerThirteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    FramedDoubleWhiskerTwelveCell W l r F G →
    FramedDoubleWhiskerTwelveCell W l r F G → Type uSix where
  | strict {F G : FramedEleven W l r}
      (P : FramedDoubleWhiskerTwelveCell W l r F G) :
      CompositionalWhiskerThirteen W l r P P
  | selected {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : SelectedWhiskerNaturalityThirteen W l r P Q) :
      CompositionalWhiskerThirteen W l r P Q
  | reverse {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : CompositionalWhiskerThirteen W l r P Q) :
      CompositionalWhiskerThirteen W l r Q P
  | chain {F G : FramedEleven W l r}
      {P Q R : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : CompositionalWhiskerThirteen W l r P Q)
      (D : CompositionalWhiskerThirteen W l r Q R) :
      CompositionalWhiskerThirteen W l r P R
  | prepend {F G H : FramedEleven W l r}
      (A : FramedDoubleWhiskerTwelveCell W l r F G)
      {P Q : FramedDoubleWhiskerTwelveCell W l r G H}
      (C : CompositionalWhiskerThirteen W l r P Q) :
      CompositionalWhiskerThirteen W l r (.chain A P) (.chain A Q)
  | append {F G H : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : CompositionalWhiskerThirteen W l r P Q)
      (A : FramedDoubleWhiskerTwelveCell W l r G H) :
      CompositionalWhiskerThirteen W l r (.chain P A) (.chain Q A)
  | associator {F G H I : FramedEleven W l r}
      (A : FramedDoubleWhiskerTwelveCell W l r F G)
      (B : FramedDoubleWhiskerTwelveCell W l r G H)
      (C : FramedDoubleWhiskerTwelveCell W l r H I) :
      CompositionalWhiskerThirteen W l r
        (.chain (.chain A B) C) (.chain A (.chain B C))
  | rightTransportComp {w z : W}
      {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K L : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K)
      (U : MixedExchangeInverseTwelveCell W l r K L)
      (after : SevenRewrite W l r e f₆) :
      CompositionalWhiskerThirteen W l r
        (framedTwelfthRightThenLeft l r before (.chain T U) after)
        (.chain (framedTwelfthRightThenLeft l r before T after)
          (framedTwelfthRightThenLeft l r before U after))
  | leftTransportComp {w z : W}
      {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K L : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K)
      (U : MixedExchangeInverseTwelveCell W l r K L)
      (after : SevenRewrite W l r e f₆) :
      CompositionalWhiskerThirteen W l r
        (framedTwelfthLeftThenRight l r before (.chain T U) after)
        (.chain (framedTwelfthLeftThenRight l r before T after)
          (framedTwelfthLeftThenRight l r before U after))

section CompositeCube
variable (l r : W) {w z : W}
variable {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r c d)
variable {s t : SevenRewrite W l r d e}
variable {q q' : PentagonAssocEightCell W l r s t}
variable {alpha beta : MixedCancelNineCell W l r q q'}
variable {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
variable {H K L : MixedExchangeUnitElevenCell W l r xi zeta}
variable (T : MixedExchangeInverseTwelveCell W l r H K)
variable (U : MixedExchangeInverseTwelveCell W l r K L)
variable (after : SevenRewrite W l r e f₆)

/-- The two old transported twelfth constructions are syntactically
distinct: whiskering a chain is NOT itself the old chain of whiskerings. -/
theorem oldRightTransportComp_rawDistinct :
    originalTwelfthRightThenLeft l r before (.chain T U) after ≠
      .chain (originalTwelfthRightThenLeft l r before T after)
        (originalTwelfthRightThenLeft l r before U after) := by
  intro h
  cases h

theorem oldLeftTransportComp_rawDistinct :
    originalTwelfthLeftThenRight l r before (.chain T U) after ≠
      .chain (originalTwelfthLeftThenRight l r before T after)
        (originalTwelfthLeftThenRight l r before U after) := by
  intro h
  cases h

/-- Pasting the two actual v5.22 squares with typed 12D path
composition and two fresh, explicitly selected 13D associators.
Each step is a genuine, endpoint-compatible higher proof term. -/
def pastedNaturalityMiddle :
    CompositionalWhiskerThirteen W l r
      (.chain
        (.chain (framedTwelfthRightThenLeft l r before T after)
          (framedTwelfthRightThenLeft l r before U after))
        (.doubleWhisker before L after))
      (.chain (.doubleWhisker before H after)
        (.chain (framedTwelfthLeftThenRight l r before T after)
          (framedTwelfthLeftThenRight l r before U after))) :=
  .chain
    (.associator
      (framedTwelfthRightThenLeft l r before T after)
      (framedTwelfthRightThenLeft l r before U after)
      (.doubleWhisker before L after))
    (.chain
      (.prepend
        (framedTwelfthRightThenLeft l r before T after)
        (.selected (.naturality before U after)))
      (.chain
        (.reverse (.associator
          (framedTwelfthRightThenLeft l r before T after)
          (.doubleWhisker before K after)
          (framedTwelfthLeftThenRight l r before U after)))
        (.chain
          (.append (.selected (.naturality before T after))
            (framedTwelfthLeftThenRight l r before U after))
          (.associator
            (.doubleWhisker before H after)
            (framedTwelfthLeftThenRight l r before T after)
            (framedTwelfthLeftThenRight l r before U after)))))

/-- The pasted 13D proof genuinely starts and ends at EXACTLY the
same raw framed 12D terms as direct naturality of the original
twelfth composite (.chain T U). Neither is an old raw equality. -/
def pastedCompositionalNaturality :
    CompositionalWhiskerThirteen W l r
      (framedWhiskerSquareUpperRoute l r before (.chain T U) after)
      (framedWhiskerSquareLowerRoute l r before (.chain T U) after) :=
  .chain
    (.append (.rightTransportComp before T U after)
      (.doubleWhisker before L after))
    (.chain (pastedNaturalityMiddle l r before T U after)
      (.reverse (.prepend (.doubleWhisker before H after)
        (.leftTransportComp before T U after))))

/-- Independent/direct 13D route, preserving the original 12D
chain as one old witness. -/
def directCompositionalNaturality :
    CompositionalWhiskerThirteen W l r
      (framedWhiskerSquareUpperRoute l r before (.chain T U) after)
      (framedWhiskerSquareLowerRoute l r before (.chain T U) after) :=
  .selected (.naturality before (.chain T U) after)

/-- Free proof history obstructs strict identification of the direct
and pasted 13D routes. -/
theorem directPastedThirteen_rawDistinct :
    directCompositionalNaturality l r before T U after ≠
      pastedCompositionalNaturality l r before T U after := by
  intro h
  cases h

end CompositeCube

/-- New, selected FOURTEENTH comparison. Its criticalCube generator
is conditional on an actual pair of composable original 12D proof
terms T and U, with matching full original 6D–11D fiber indices.
It NEVER asserts direct=pasted as original 13D raw proof terms. -/
inductive SelectedCompositionFourteen (W : Type uSix) (l r : W) :
    {F G : FramedEleven W l r} →
    {P Q : FramedDoubleWhiskerTwelveCell W l r F G} →
    CompositionalWhiskerThirteen W l r P Q →
    CompositionalWhiskerThirteen W l r P Q → Type uSix where
  | strict {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      (C : CompositionalWhiskerThirteen W l r P Q) :
      SelectedCompositionFourteen W l r C C
  | criticalCube {w z : W}
      {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K L : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K)
      (U : MixedExchangeInverseTwelveCell W l r K L)
      (after : SevenRewrite W l r e f₆) :
      SelectedCompositionFourteen W l r
        (directCompositionalNaturality l r before T U after)
        (pastedCompositionalNaturality l r before T U after)
  | reverse {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      {C D : CompositionalWhiskerThirteen W l r P Q}
      (V : SelectedCompositionFourteen W l r C D) :
      SelectedCompositionFourteen W l r D C
  | chain {F G : FramedEleven W l r}
      {P Q : FramedDoubleWhiskerTwelveCell W l r F G}
      {C D E : CompositionalWhiskerThirteen W l r P Q}
      (V : SelectedCompositionFourteen W l r C D)
      (X : SelectedCompositionFourteen W l r D E) :
      SelectedCompositionFourteen W l r C E

section FourteenResults
variable (l r : W) {w z : W}
variable {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r c d)
variable {s t : SevenRewrite W l r d e}
variable {q q' : PentagonAssocEightCell W l r s t}
variable {alpha beta : MixedCancelNineCell W l r q q'}
variable {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
variable {H K L : MixedExchangeUnitElevenCell W l r xi zeta}
variable (T : MixedExchangeInverseTwelveCell W l r H K)
variable (U : MixedExchangeInverseTwelveCell W l r K L)
variable (after : SevenRewrite W l r e f₆)

/-- A conditional 14D filler exists, AND its 13D boundary paths
remain raw-distinct. This is selected presentation data, not an
inherited old theorem about all fourteenth coherences. -/
theorem selectedCompositionFourteen_conditionalCube :
    Nonempty (SelectedCompositionFourteen W l r
      (directCompositionalNaturality l r before T U after)
      (pastedCompositionalNaturality l r before T U after)) ∧
    directCompositionalNaturality l r before T U after ≠
      pastedCompositionalNaturality l r before T U after :=
  ⟨⟨.criticalCube before T U after⟩,
    directPastedThirteen_rawDistinct l r before T U after⟩

/-- Even with an actual old 12D composite, the chosen 14D
comparison cannot be faithfully interpreted as strict original
13D syntactic equality. -/
theorem selectedCompositionFourteen_noRawEqualityAtCube :
    ¬ (∀
      (C D : CompositionalWhiskerThirteen W l r
        (framedWhiskerSquareUpperRoute l r before (.chain T U) after)
        (framedWhiskerSquareLowerRoute l r before (.chain T U) after)),
      SelectedCompositionFourteen W l r C D → C = D) := by
  intro interpret
  exact (directPastedThirteen_rawDistinct l r before T U after)
    (interpret _ _ (.criticalCube before T U after))

end FourteenResults

#print axioms PentagonAdjoinedSixCell.originalTripleWhiskerRLR
#print axioms PentagonAdjoinedSixCell.originalTripleWhiskerRRL
#print axioms PentagonAdjoinedSixCell.originalTripleWhisker_traceValues
#print axioms PentagonAdjoinedSixCell.originalTripleWhisker_orderObstruction
#print axioms PentagonAdjoinedSixCell.originalTripleWhisker_lengthCollision
#print axioms PentagonAdjoinedSixCell.CompositionalWhiskerThirteen
#print axioms PentagonAdjoinedSixCell.oldRightTransportComp_rawDistinct
#print axioms PentagonAdjoinedSixCell.oldLeftTransportComp_rawDistinct
#print axioms PentagonAdjoinedSixCell.pastedNaturalityMiddle
#print axioms PentagonAdjoinedSixCell.pastedCompositionalNaturality
#print axioms PentagonAdjoinedSixCell.directCompositionalNaturality
#print axioms PentagonAdjoinedSixCell.directPastedThirteen_rawDistinct
#print axioms PentagonAdjoinedSixCell.SelectedCompositionFourteen
#print axioms PentagonAdjoinedSixCell.selectedCompositionFourteen_conditionalCube
#print axioms PentagonAdjoinedSixCell.selectedCompositionFourteen_noRawEqualityAtCube

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
