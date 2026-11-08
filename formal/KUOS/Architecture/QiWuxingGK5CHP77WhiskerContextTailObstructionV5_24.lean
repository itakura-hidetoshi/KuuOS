import KUOS.Architecture.QiWuxingGK5CHP77CompositionalNaturalityCriticalCubeV5_23

/-!
Qi v5.24: a preserved tail detects an actual missing triple-whisker face.

No comparison constructor is added. Every original sixth through twelfth
Type and both selected thirteenth/fourteenth presentations stay unchanged.
The FULL existing framed twelfth grammar preserves the original tenth
whiskering trace after dropping its first two entries. This invariant
therefore descends to its existing quotient, unlike the full raw trace.

The three packets LRR, RLR, RRL below are named by OUTSIDE-IN constructor
order, not chronological application order. An authentic framed twelfth
face LRR -> RLR exists. No such face RLR -> RRL exists, even using ALL
previous/reverse/chain rules, because their preserved tails differ.

Actual left/right identity-boundary whiskering transports the inherited-only
old twelfth grammar, but cannot transport the full framed grammar or descend
to its quotient. Higher selected 13D/14D comparisons do not manufacture the
missing lower-dimensional boundary. No completeness of the invariant and
no impossibility in a future enriched presentation are asserted.
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

/-- Unlike the complete ordered trace, its suffix after two entries
is preserved by EVERY existing framed twelfth comparison. -/
def framedWhiskerTailInvariant (l r : W)
    (F : FramedEleven W l r) : List Bool :=
  (framedWhiskerRawTrace F).drop 2

theorem framedDoubleWhisker_preservesTail (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedDoubleWhiskerTwelveCell W l r F G) :
    framedWhiskerTailInvariant l r F = framedWhiskerTailInvariant l r G := by
  induction T with
  | strict F => rfl
  | previous T => rfl
  | doubleWhisker before H after => rfl
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'

/-- Genuine descent to the EXISTING full framed twelfth quotient. -/
def framedDoubleWhiskerTail (l r : W) :
    Quotient (framedDoubleWhiskerSetoid W l r) → List Bool :=
  Quotient.lift (framedWhiskerTailInvariant l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact framedDoubleWhisker_preservesTail l r T)

theorem framedDoubleWhiskerTail_onClass (l r : W)
    (F : FramedEleven W l r) :
    framedDoubleWhiskerTail l r (framedDoubleWhiskerClass F) =
      framedWhiskerTailInvariant l r F := rfl

theorem framedTailGap_noTwelfth (l r : W)
    {F G : FramedEleven W l r}
    (gap : framedWhiskerTailInvariant l r F ≠ framedWhiskerTailInvariant l r G) :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r F G) := by
  rintro ⟨T⟩
  exact gap (framedDoubleWhisker_preservesTail l r T)

/-- A selected 14D comparison needs actual parallel 12D boundary paths.
The v5.23 constructors cannot supply those paths across a tail gap. -/
theorem framedTailGap_noSelectedFourteen (l r : W)
    {F G : FramedEleven W l r}
    (gap : framedWhiskerTailInvariant l r F ≠ framedWhiskerTailInvariant l r G) :
    ¬ (∃ (P Q : FramedDoubleWhiskerTwelveCell W l r F G)
      (C D : CompositionalWhiskerThirteen W l r P Q),
      Nonempty (SelectedCompositionFourteen W l r C D)) := by
  rintro ⟨P, _, _, _, _⟩
  exact gap (framedDoubleWhisker_preservesTail l r P)

section TripleFaces
variable (l r : W) {w z : W}
variable {b c d e f₆ : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable {s t : SevenRewrite W l r c d}
variable {q q' : PentagonAssocEightCell W l r s t}
variable {alpha beta : MixedCancelNineCell W l r q q'}
variable {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
variable (H : MixedExchangeUnitElevenCell W l r xi zeta)
variable (inner : SevenRewrite W l r d e)
variable (outer : SevenRewrite W l r e f₆)

/-- Three authentic original 11D packets, preserving all dependent indices. -/
def tripleWhiskerFrameLRR : FramedEleven W l r :=
  framedEleven_ofRaw l r
    (.whiskerLeft before (.whiskerRight (.whiskerRight H inner) outer))

def tripleWhiskerFrameRLR : FramedEleven W l r :=
  framedEleven_ofRaw l r
    (.whiskerRight (.whiskerLeft before (.whiskerRight H inner)) outer)

def tripleWhiskerFrameRRL : FramedEleven W l r :=
  framedEleven_ofRaw l r
    (.whiskerRight (.whiskerRight (.whiskerLeft before H) inner) outer)

/-- This is an EXISTING doubleWhisker generator with an actual right
whisker INSIDE its argument. No closure under OUTER contexts is assumed. -/
def tripleWhisker_outerAdjacentFace :
    FramedDoubleWhiskerTwelveCell W l r
      (tripleWhiskerFrameLRR l r before H inner outer)
      (tripleWhiskerFrameRLR l r before H inner outer) := by
  change FramedDoubleWhiskerTwelveCell W l r
    (doubleWhiskerLeftAfterRightFrame l r before (.whiskerRight H inner) outer)
    (doubleWhiskerRightAfterLeftFrame l r before (.whiskerRight H inner) outer)
  exact .doubleWhisker before (.whiskerRight H inner) outer

theorem tripleWhisker_tailValues :
    framedWhiskerTailInvariant l r
        (tripleWhiskerFrameLRR l r before H inner outer) =
        true :: mixedTenWhiskerRawTrace xi ∧
    framedWhiskerTailInvariant l r
        (tripleWhiskerFrameRLR l r before H inner outer) =
        true :: mixedTenWhiskerRawTrace xi ∧
    framedWhiskerTailInvariant l r
        (tripleWhiskerFrameRRL l r before H inner outer) =
        false :: mixedTenWhiskerRawTrace xi :=
  ⟨rfl, rfl, rfl⟩

/-- Stronger than raw inequality: NO composite existing framed 12D
proof fills the inner adjacent exchange under the outer right context. -/
theorem tripleWhisker_missingInnerFace :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (tripleWhiskerFrameRLR l r before H inner outer)
      (tripleWhiskerFrameRRL l r before H inner outer)) := by
  rintro ⟨T⟩
  have h := framedDoubleWhisker_preservesTail l r T
  change (true :: mixedTenWhiskerRawTrace xi) =
    (false :: mixedTenWhiskerRawTrace xi) at h
  cases h

theorem tripleWhisker_firstLastDisconnected :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (tripleWhiskerFrameLRR l r before H inner outer)
      (tripleWhiskerFrameRRL l r before H inner outer)) := by
  rintro ⟨T⟩
  have h := framedDoubleWhisker_preservesTail l r T
  change (true :: mixedTenWhiskerRawTrace xi) =
    (false :: mixedTenWhiskerRawTrace xi) at h
  cases h

/-- Exact class splitting for these three ACTUAL packets: the first
two coincide in the existing quotient, the third is separate from both. -/
theorem tripleWhisker_threeClassSplit :
    framedDoubleWhiskerClass (tripleWhiskerFrameLRR l r before H inner outer) =
      framedDoubleWhiskerClass (tripleWhiskerFrameRLR l r before H inner outer) ∧
    framedDoubleWhiskerClass (tripleWhiskerFrameRLR l r before H inner outer) ≠
      framedDoubleWhiskerClass (tripleWhiskerFrameRRL l r before H inner outer) ∧
    framedDoubleWhiskerClass (tripleWhiskerFrameLRR l r before H inner outer) ≠
      framedDoubleWhiskerClass (tripleWhiskerFrameRRL l r before H inner outer) := by
  constructor
  · exact (framedDoubleWhiskerClass_eq_iff _ _).2
      ⟨tripleWhisker_outerAdjacentFace l r before H inner outer⟩
  · constructor
    · intro h
      exact tripleWhisker_missingInnerFace l r before H inner outer
        ((framedDoubleWhiskerClass_eq_iff _ _).1 h)
    · intro h
      exact tripleWhisker_firstLastDisconnected l r before H inner outer
        ((framedDoubleWhiskerClass_eq_iff _ _).1 h)

/-- Selected higher comparison cannot repair this missing LOWER face
without changing the existing framed twelfth presentation. -/
theorem tripleWhisker_noSelectedFourteenthOverMissingFace :
    ¬ (∃
      (P Q : FramedDoubleWhiskerTwelveCell W l r
        (tripleWhiskerFrameRLR l r before H inner outer)
        (tripleWhiskerFrameRRL l r before H inner outer))
      (C D : CompositionalWhiskerThirteen W l r P Q),
      Nonempty (SelectedCompositionFourteen W l r C D)) := by
  apply framedTailGap_noSelectedFourteen l r
  intro h
  change (true :: mixedTenWhiskerRawTrace xi) =
    (false :: mixedTenWhiskerRawTrace xi) at h
  cases h

end TripleFaces

/-- Actual ORIGINAL right whiskering by the reflexive seventh boundary.
This is globally defined on packets, but is not a raw identity operation. -/
def framedUnitRightWhisker (l r : W)
    (F : FramedEleven W l r) : FramedEleven W l r :=
  framedEleven_ofRaw l r (.whiskerRight F.H (.refl F.d))

def framedUnitLeftWhisker (l r : W)
    (F : FramedEleven W l r) : FramedEleven W l r :=
  framedEleven_ofRaw l r (.whiskerLeft (.refl F.c) F.H)

theorem framedUnitRightWhisker_trace (l r : W)
    (F : FramedEleven W l r) :
    framedWhiskerRawTrace (framedUnitRightWhisker l r F) =
      true :: framedWhiskerRawTrace F := rfl

theorem framedUnitLeftWhisker_trace (l r : W)
    (F : FramedEleven W l r) :
    framedWhiskerRawTrace (framedUnitLeftWhisker l r F) =
      false :: framedWhiskerRawTrace F := rfl

/-- The OLD inherited-only grammar really DOES transport. The proof
uses only genuine original twelfth whiskering and its old closure. -/
def framedUnitRightWhiskerInherited (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    FramedInheritedTwelfth W l r
      (framedUnitRightWhisker l r F) (framedUnitRightWhisker l r G) := by
  induction T with
  | strict F => exact .strict _
  | previous T => exact .previous (.whiskerRight T (.refl _))
  | reverse T ih => exact .reverse ih
  | chain T U ih ih' => exact .chain ih ih'

def framedUnitLeftWhiskerInherited (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    FramedInheritedTwelfth W l r
      (framedUnitLeftWhisker l r F) (framedUnitLeftWhisker l r G) := by
  induction T with
  | strict F => exact .strict _
  | previous T => exact .previous (.whiskerLeft (.refl _) T)
  | reverse T ih => exact .reverse ih
  | chain T U ih ih' => exact .chain ih ih'

section ContextGap
variable (l r : W) {w z : W}
variable {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r c d)
variable {s t : SevenRewrite W l r d e}
variable {q q' : PentagonAssocEightCell W l r s t}
variable {alpha beta : MixedCancelNineCell W l r q q'}
variable {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
variable (H : MixedExchangeUnitElevenCell W l r xi zeta)
variable (after : SevenRewrite W l r e f₆)

/-- Even an OUTER right identity-boundary context destroys the
existing full comparison of the original double-whisker pair. -/
theorem framedRightUnit_doubleWhiskerGap :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (framedUnitRightWhisker l r
        (doubleWhiskerLeftAfterRightFrame l r before H after))
      (framedUnitRightWhisker l r
        (doubleWhiskerRightAfterLeftFrame l r before H after))) := by
  rintro ⟨T⟩
  have h := framedDoubleWhisker_preservesTail l r T
  change (true :: mixedTenWhiskerRawTrace xi) =
    (false :: mixedTenWhiskerRawTrace xi) at h
  cases h

/-- The same obstruction holds for an OUTER left identity context. -/
theorem framedLeftUnit_doubleWhiskerGap :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (framedUnitLeftWhisker l r
        (doubleWhiskerLeftAfterRightFrame l r before H after))
      (framedUnitLeftWhisker l r
        (doubleWhiskerRightAfterLeftFrame l r before H after))) := by
  rintro ⟨T⟩
  have h := framedDoubleWhisker_preservesTail l r T
  change (true :: mixedTenWhiskerRawTrace xi) =
    (false :: mixedTenWhiskerRawTrace xi) at h
  cases h

end ContextGap

/-- A universally defined raw packet operation need not act on the
selected comparison relation. Genuine exchangeUnit supplies the counterexample. -/
theorem framedRightWhisker_noFullLift (l r : W) :
    ¬ (∀ {F G : FramedEleven W l r},
      FramedDoubleWhiskerTwelveCell W l r F G →
      Nonempty (FramedDoubleWhiskerTwelveCell W l r
        (framedUnitRightWhisker l r F) (framedUnitRightWhisker l r G))) := by
  intro lift
  exact framedRightUnit_doubleWhiskerGap l r
    (.refl _) (.exchangeUnit) (.refl _)
    (lift (.doubleWhisker (.refl _) (.exchangeUnit) (.refl _)))

theorem framedLeftWhisker_noFullLift (l r : W) :
    ¬ (∀ {F G : FramedEleven W l r},
      FramedDoubleWhiskerTwelveCell W l r F G →
      Nonempty (FramedDoubleWhiskerTwelveCell W l r
        (framedUnitLeftWhisker l r F) (framedUnitLeftWhisker l r G))) := by
  intro lift
  exact framedLeftUnit_doubleWhiskerGap l r
    (.refl _) (.exchangeUnit) (.refl _)
    (lift (.doubleWhisker (.refl _) (.exchangeUnit) (.refl _)))

/-- There is NO operation on the existing full quotient whose value
on every class is the class of the genuine right-whiskered packet. -/
theorem framedRightWhisker_noQuotientDescent (l r : W) :
    ¬ (∃ phi : Quotient (framedDoubleWhiskerSetoid W l r) →
          Quotient (framedDoubleWhiskerSetoid W l r),
      ∀ F : FramedEleven W l r,
        phi (framedDoubleWhiskerClass F) =
          framedDoubleWhiskerClass (framedUnitRightWhisker l r F)) := by
  rintro ⟨phi, hphi⟩
  have h := congrArg phi (framedDoubleWhiskerClass_originalCritical l r)
  have imageEq :
      framedDoubleWhiskerClass
          (framedUnitRightWhisker l r (originalDoubleWhiskerLeftFrame l r)) =
        framedDoubleWhiskerClass
          (framedUnitRightWhisker l r (originalDoubleWhiskerRightFrame l r)) :=
    (hphi _).symm.trans (h.trans (hphi _))
  exact framedRightUnit_doubleWhiskerGap l r
    (.refl _) (.exchangeUnit) (.refl _)
    ((framedDoubleWhiskerClass_eq_iff _ _).1 imageEq)

theorem framedLeftWhisker_noQuotientDescent (l r : W) :
    ¬ (∃ phi : Quotient (framedDoubleWhiskerSetoid W l r) →
          Quotient (framedDoubleWhiskerSetoid W l r),
      ∀ F : FramedEleven W l r,
        phi (framedDoubleWhiskerClass F) =
          framedDoubleWhiskerClass (framedUnitLeftWhisker l r F)) := by
  rintro ⟨phi, hphi⟩
  have h := congrArg phi (framedDoubleWhiskerClass_originalCritical l r)
  have imageEq :
      framedDoubleWhiskerClass
          (framedUnitLeftWhisker l r (originalDoubleWhiskerLeftFrame l r)) =
        framedDoubleWhiskerClass
          (framedUnitLeftWhisker l r (originalDoubleWhiskerRightFrame l r)) :=
    (hphi _).symm.trans (h.trans (hphi _))
  exact framedLeftUnit_doubleWhiskerGap l r
    (.refl _) (.exchangeUnit) (.refl _)
    ((framedDoubleWhiskerClass_eq_iff _ _).1 imageEq)

#print axioms PentagonAdjoinedSixCell.framedWhiskerTailInvariant
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_preservesTail
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerTail
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerTail_onClass
#print axioms PentagonAdjoinedSixCell.framedTailGap_noTwelfth
#print axioms PentagonAdjoinedSixCell.framedTailGap_noSelectedFourteen
#print axioms PentagonAdjoinedSixCell.tripleWhiskerFrameLRR
#print axioms PentagonAdjoinedSixCell.tripleWhiskerFrameRLR
#print axioms PentagonAdjoinedSixCell.tripleWhiskerFrameRRL
#print axioms PentagonAdjoinedSixCell.tripleWhisker_outerAdjacentFace
#print axioms PentagonAdjoinedSixCell.tripleWhisker_tailValues
#print axioms PentagonAdjoinedSixCell.tripleWhisker_missingInnerFace
#print axioms PentagonAdjoinedSixCell.tripleWhisker_firstLastDisconnected
#print axioms PentagonAdjoinedSixCell.tripleWhisker_threeClassSplit
#print axioms PentagonAdjoinedSixCell.tripleWhisker_noSelectedFourteenthOverMissingFace
#print axioms PentagonAdjoinedSixCell.framedUnitRightWhisker
#print axioms PentagonAdjoinedSixCell.framedUnitLeftWhisker
#print axioms PentagonAdjoinedSixCell.framedUnitRightWhisker_trace
#print axioms PentagonAdjoinedSixCell.framedUnitLeftWhisker_trace
#print axioms PentagonAdjoinedSixCell.framedUnitRightWhiskerInherited
#print axioms PentagonAdjoinedSixCell.framedUnitLeftWhiskerInherited
#print axioms PentagonAdjoinedSixCell.framedRightUnit_doubleWhiskerGap
#print axioms PentagonAdjoinedSixCell.framedLeftUnit_doubleWhiskerGap
#print axioms PentagonAdjoinedSixCell.framedRightWhisker_noFullLift
#print axioms PentagonAdjoinedSixCell.framedLeftWhisker_noFullLift
#print axioms PentagonAdjoinedSixCell.framedRightWhisker_noQuotientDescent
#print axioms PentagonAdjoinedSixCell.framedLeftWhisker_noQuotientDescent

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
