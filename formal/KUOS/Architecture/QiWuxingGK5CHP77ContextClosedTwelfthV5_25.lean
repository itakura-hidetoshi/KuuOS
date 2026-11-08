import KUOS.Architecture.QiWuxingGK5CHP77WhiskerContextTailObstructionV5_24

/-!
Qi v5.25: the least typed outer-whisker closure of the existing framed
12D presentation. Every old 6D--14D Type and proof history is unchanged.

A boundary-indexed packet stores ONLY actual original 7D--11D witnesses.
The new 12D grammar embeds old framed proofs as proof-relevant data and
adds precisely left/right context closure at matching original boundaries.
The missing v5.24 inner triple face is DERIVED by context closure of an
actual old doubleWhisker, not introduced as a special-case constructor.

The old quotient maps noninjectively to the new quotient: its tail observer
cannot survive this repair. Three original event counts DO survive, and an
original tenSymm obstruction remains. Left/right actions on fixed-boundary
quotients now exist. No arbitrary cross-boundary operation, strict raw
identity/associativity law, or automatic 13D/14D coherence is asserted.
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

/-- Original proof data at fixed SIX-dimensional source/target. The two
seventh words and every higher witness remain independent Type values. -/
structure ContextFrameEleven (W : Type uSix) (l r : W) {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) : Type uSix where
  s : SevenRewrite W l r c d
  t : SevenRewrite W l r c d
  q₀ : PentagonAssocEightCell W l r s t
  q₁ : PentagonAssocEightCell W l r s t
  alpha : MixedCancelNineCell W l r q₀ q₁
  beta : MixedCancelNineCell W l r q₀ q₁
  xi : MixedUnitAssocTenCell W l r alpha beta
  zeta : MixedUnitAssocTenCell W l r alpha beta
  H : MixedExchangeUnitElevenCell W l r xi zeta

def contextFrameOfRaw (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    ContextFrameEleven W l r c d :=
  ⟨s, t, q, q', alpha, beta, xi, zeta, H⟩

def contextFramePack (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) : FramedEleven W l r :=
  framedEleven_ofRaw l r F.H

def contextFrameLeft (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (F : ContextFrameEleven W l r c d) : ContextFrameEleven W l r b d :=
  contextFrameOfRaw l r (.whiskerLeft before F.H)

def contextFrameRight (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d)
    (after : SevenRewrite W l r d e) : ContextFrameEleven W l r c e :=
  contextFrameOfRaw l r (.whiskerRight F.H after)

/-- Exactly two context-closure rules are new; all old proof terms are
stored in previous. No new raw Eq or special missing-face axiom. -/
inductive ContextClosedFramedTwelve (W : Type uSix) (l r : W) :
    FramedEleven W l r → FramedEleven W l r → Type uSix where
  | strict (F : FramedEleven W l r) : ContextClosedFramedTwelve W l r F F
  | previous {F G : FramedEleven W l r}
      (T : FramedDoubleWhiskerTwelveCell W l r F G) :
      ContextClosedFramedTwelve W l r F G
  | reverse {F G : FramedEleven W l r}
      (T : ContextClosedFramedTwelve W l r F G) :
      ContextClosedFramedTwelve W l r G F
  | chain {F G K : FramedEleven W l r}
      (T : ContextClosedFramedTwelve W l r F G)
      (U : ContextClosedFramedTwelve W l r G K) :
      ContextClosedFramedTwelve W l r F K
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      (T : ContextClosedFramedTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)) :
      ContextClosedFramedTwelve W l r
        (contextFramePack l r (contextFrameLeft l r before F))
        (contextFramePack l r (contextFrameLeft l r before G))
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      (T : ContextClosedFramedTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G))
      (after : SevenRewrite W l r d e) :
      ContextClosedFramedTwelve W l r
        (contextFramePack l r (contextFrameRight l r F after))
        (contextFramePack l r (contextFrameRight l r G after))

/-- Faithfulness here is ONLY for the embedding of old RAW PROOF VALUES;
the induced quotient map below is deliberately proved noninjective. -/
theorem contextClosed_previous_injective (l r : W)
    {F G : FramedEleven W l r} :
    Function.Injective (fun T : FramedDoubleWhiskerTwelveCell W l r F G =>
      ContextClosedFramedTwelve.previous T) := by
  intro T U h
  cases h
  rfl

/-- A candidate relation with exactly the required original-context laws. -/
structure IsTypedWhiskerCongruence (l r : W)
    (R : FramedEleven W l r → FramedEleven W l r → Prop) : Prop where
  refl : ∀ F, R F F
  symm : ∀ {F G}, R F G → R G F
  trans : ∀ {F G K}, R F G → R G K → R F K
  previous : ∀ {F G}, FramedDoubleWhiskerTwelveCell W l r F G → R F G
  left : ∀ {w z : W} {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c) (F G : ContextFrameEleven W l r c d),
    R (contextFramePack l r F) (contextFramePack l r G) →
      R (contextFramePack l r (contextFrameLeft l r before F))
        (contextFramePack l r (contextFrameLeft l r before G))
  right : ∀ {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d),
    R (contextFramePack l r F) (contextFramePack l r G) →
      ∀ (after : SevenRewrite W l r d e),
        R (contextFramePack l r (contextFrameRight l r F after))
          (contextFramePack l r (contextFrameRight l r G after))

/-- Leastness among all relations containing the old grammar and closed
under the stated, genuinely boundary-compatible original contexts. -/
theorem contextClosed_least (l r : W)
    (R : FramedEleven W l r → FramedEleven W l r → Prop)
    (hR : IsTypedWhiskerCongruence l r R)
    {F G : FramedEleven W l r} (T : ContextClosedFramedTwelve W l r F G) :
    R F G := by
  induction T with
  | strict F => exact hR.refl F
  | previous T => exact hR.previous T
  | reverse T ih => exact hR.symm ih
  | chain T U ih ih' => exact hR.trans ih ih'
  | whiskerLeft before F G T ih => exact hR.left before F G ih
  | whiskerRight F G T after ih => exact hR.right F G ih after

def contextClosedSetoid (W : Type uSix) (l r : W) :
    Setoid (FramedEleven W l r) where
  r := fun F G => Nonempty (ContextClosedFramedTwelve W l r F G)
  iseqv := by
    constructor
    · intro F
      exact ⟨.strict F⟩
    · intro F G h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro F G K h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

def contextClosedClass (l r : W) (F : FramedEleven W l r) :
    Quotient (contextClosedSetoid W l r) := Quotient.mk _ F

theorem contextClosedClass_eq_iff (l r : W) (F G : FramedEleven W l r) :
    contextClosedClass l r F = contextClosedClass l r G ↔
      Nonempty (ContextClosedFramedTwelve W l r F G) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

section MissingFace
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

/-- The missing inner face is obtained from an actual old doubleWhisker
and ONE new context rule, carrying the full old proof term inside it. -/
def contextClosed_innerFace :
    ContextClosedFramedTwelve W l r
      (tripleWhiskerFrameRLR l r before H inner outer)
      (tripleWhiskerFrameRRL l r before H inner outer) :=
  .whiskerRight
    (contextFrameOfRaw l r (.whiskerLeft before (.whiskerRight H inner)))
    (contextFrameOfRaw l r (.whiskerRight (.whiskerLeft before H) inner))
    (.previous (.doubleWhisker before H inner)) outer

/-- Both adjacent faces now compose; this is a constructed path,
not strict equality of the three original dependent packets. -/
def contextClosed_fullTriplePath :
    ContextClosedFramedTwelve W l r
      (tripleWhiskerFrameLRR l r before H inner outer)
      (tripleWhiskerFrameRRL l r before H inner outer) :=
  .chain (.previous (tripleWhisker_outerAdjacentFace l r before H inner outer))
    (contextClosed_innerFace l r before H inner outer)

theorem contextClosed_innerFace_strictExtension :
    Nonempty (ContextClosedFramedTwelve W l r
      (tripleWhiskerFrameRLR l r before H inner outer)
      (tripleWhiskerFrameRRL l r before H inner outer)) ∧
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (tripleWhiskerFrameRLR l r before H inner outer)
      (tripleWhiskerFrameRRL l r before H inner outer)) :=
  ⟨⟨contextClosed_innerFace l r before H inner outer⟩,
    tripleWhisker_missingInnerFace l r before H inner outer⟩

end MissingFace

/-- Fully inhabited counterexample using the ACTUAL original exchangeUnit. -/
def contextMissingSource (l r : W) : FramedEleven W l r :=
  tripleWhiskerFrameRLR l r (.refl _) (.exchangeUnit) (.refl _) (.refl _)

def contextMissingTarget (l r : W) : FramedEleven W l r :=
  tripleWhiskerFrameRRL l r (.refl _) (.exchangeUnit) (.refl _) (.refl _)

def contextMissingCompletion (l r : W) :
    ContextClosedFramedTwelve W l r
      (contextMissingSource l r) (contextMissingTarget l r) :=
  contextClosed_innerFace l r (.refl _) (.exchangeUnit) (.refl _) (.refl _)

theorem contextMissing_oldObstruction (l r : W) :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (contextMissingSource l r) (contextMissingTarget l r)) :=
  tripleWhisker_missingInnerFace l r
    (.refl _) (.exchangeUnit) (.refl _) (.refl _)

theorem contextMissing_tailGap (l r : W) :
    framedWhiskerTailInvariant l r (contextMissingSource l r) ≠
      framedWhiskerTailInvariant l r (contextMissingTarget l r) := by
  intro h
  change (true :: _) = (false :: _) at h
  cases h

theorem contextMissing_rawGap (l r : W) :
    contextMissingSource l r ≠ contextMissingTarget l r := by
  intro h
  exact contextMissing_tailGap l r
    (congrArg (framedWhiskerTailInvariant l r) h)

/-- Canonical old-to-new quotient map; raw old proofs stay inside previous. -/
def oldToContextClosedQuotient (l r : W) :
    Quotient (framedDoubleWhiskerSetoid W l r) →
      Quotient (contextClosedSetoid W l r) :=
  Quotient.lift (contextClosedClass l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact Quotient.sound ⟨.previous T⟩)

theorem oldToContextClosedQuotient_onClass (l r : W)
    (F : FramedEleven W l r) :
    oldToContextClosedQuotient l r (framedDoubleWhiskerClass F) =
      contextClosedClass l r F := rfl

theorem oldToContextClosedQuotient_notInjective (l r : W) :
    ¬ Function.Injective (oldToContextClosedQuotient l r) := by
  intro hinj
  have imageEq :
      oldToContextClosedQuotient l r
          (framedDoubleWhiskerClass (contextMissingSource l r)) =
        oldToContextClosedQuotient l r
          (framedDoubleWhiskerClass (contextMissingTarget l r)) :=
    Quotient.sound ⟨contextMissingCompletion l r⟩
  exact contextMissing_oldObstruction l r (Quotient.exact (hinj imageEq))

theorem contextClosed_noOldReflection (l r : W) :
    ¬ (∀ {F G : FramedEleven W l r},
      ContextClosedFramedTwelve W l r F G →
        Nonempty (FramedDoubleWhiskerTwelveCell W l r F G)) := by
  intro reflect
  exact contextMissing_oldObstruction l r (reflect (contextMissingCompletion l r))

/-- The v5.24 tail is lost at the new quotient, not deleted from raw packets. -/
theorem contextClosed_noTailDescent (l r : W) :
    ¬ (∃ observe : Quotient (contextClosedSetoid W l r) → List Bool,
      ∀ F, observe (contextClosedClass l r F) = framedWhiskerTailInvariant l r F) := by
  rintro ⟨observe, onClass⟩
  have h := congrArg observe
    ((contextClosedClass_eq_iff l r _ _).2 ⟨contextMissingCompletion l r⟩)
  exact contextMissing_tailGap l r
    ((onClass _).symm.trans (h.trans (onClass _)))

/-- Three genuinely pre-existing original observers, not newly chosen labels. -/
def framedContextEventCounts (l r : W) (F : FramedEleven W l r) : Nat × Nat × Nat :=
  (framedOldTenthEventCount F, framedUnitTenthEventCount F, framedTenSymmEventCount F)

theorem contextClosed_preservesEventCounts (l r : W)
    {F G : FramedEleven W l r} (T : ContextClosedFramedTwelve W l r F G) :
    framedContextEventCounts l r F = framedContextEventCounts l r G := by
  induction T with
  | strict F => rfl
  | previous T =>
      exact Prod.ext (framedDoubleWhisker_preservesOldCount T)
        (Prod.ext (framedDoubleWhisker_preservesUnitCount T)
          (framedDoubleWhisker_preservesTenSymmCount T))
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'
  | whiskerLeft before F G T ih => exact ih
  | whiskerRight F G T after ih => exact ih

def contextClosedEventCounts (l r : W) :
    Quotient (contextClosedSetoid W l r) → Nat × Nat × Nat :=
  Quotient.lift (framedContextEventCounts l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact contextClosed_preservesEventCounts l r T)

theorem contextClosedEventCounts_onClass (l r : W) (F : FramedEleven W l r) :
    contextClosedEventCounts l r (contextClosedClass l r F) =
      framedContextEventCounts l r F := rfl

/-- The repair is NOT indiscriminate comparison of every original packet. -/
theorem contextClosed_retainsTenSymmObstruction (l r : W) :
    ¬ Nonempty (ContextClosedFramedTwelve W l r
      (framedOriginalTenSymmCriticalLoop l r)
      (framedOriginalTenSymmCriticalRefl l r)) := by
  rintro ⟨T⟩
  have h := congrArg (fun n : Nat × Nat × Nat => n.2.2)
    (contextClosed_preservesEventCounts l r T)
  change (1 : Nat) = 0 at h
  cases h

/-- Quotient within an exact original six-boundary, using the NEW relation.
Its higher proof fields remain arbitrary, not identified before quotienting. -/
def contextBoundarySetoid (W : Type uSix) (l r : W) {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    Setoid (ContextFrameEleven W l r c d) where
  r := fun F G => Nonempty (ContextClosedFramedTwelve W l r
    (contextFramePack l r F) (contextFramePack l r G))
  iseqv := by
    constructor
    · intro F
      exact ⟨.strict _⟩
    · intro F G h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro F G K h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

/-- Boundary-compatible arbitrary LEFT contexts really descend now. -/
def contextClosedLeftAction (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c) :
    Quotient (contextBoundarySetoid W l r c d) →
      Quotient (contextBoundarySetoid W l r b d) :=
  Quotient.lift (fun F => Quotient.mk _ (contextFrameLeft l r before F)) (by
    intro F G h
    rcases h with ⟨T⟩
    exact Quotient.sound ⟨.whiskerLeft before F G T⟩)

/-- Boundary-compatible arbitrary RIGHT contexts really descend now. -/
def contextClosedRightAction (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (after : SevenRewrite W l r d e) :
    Quotient (contextBoundarySetoid W l r c d) →
      Quotient (contextBoundarySetoid W l r c e) :=
  Quotient.lift (fun F => Quotient.mk _ (contextFrameRight l r F after)) (by
    intro F G h
    rcases h with ⟨T⟩
    exact Quotient.sound ⟨.whiskerRight F G T after⟩)

theorem contextClosedLeftAction_onClass (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c) (F : ContextFrameEleven W l r c d) :
    contextClosedLeftAction l r before (Quotient.mk _ F) =
      Quotient.mk _ (contextFrameLeft l r before F) := rfl

theorem contextClosedRightAction_onClass (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) (after : SevenRewrite W l r d e) :
    contextClosedRightAction l r after (Quotient.mk _ F) =
      Quotient.mk _ (contextFrameRight l r F after) := rfl

/-- Opposite-side context actions commute on the new boundary quotient,
using the genuine OLD doubleWhisker comparison, not equality of raw frames. -/
theorem contextClosedActions_commute (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c) (after : SevenRewrite W l r d e)
    (x : Quotient (contextBoundarySetoid W l r c d)) :
    contextClosedLeftAction l r before (contextClosedRightAction l r after x) =
      contextClosedRightAction l r after (contextClosedLeftAction l r before x) := by
  refine Quotient.inductionOn x ?_
  intro F
  exact Quotient.sound ⟨.previous (.doubleWhisker before F.H after)⟩

#print axioms PentagonAdjoinedSixCell.ContextFrameEleven
#print axioms PentagonAdjoinedSixCell.contextFrameOfRaw
#print axioms PentagonAdjoinedSixCell.contextFramePack
#print axioms PentagonAdjoinedSixCell.contextFrameLeft
#print axioms PentagonAdjoinedSixCell.contextFrameRight
#print axioms PentagonAdjoinedSixCell.ContextClosedFramedTwelve
#print axioms PentagonAdjoinedSixCell.contextClosed_previous_injective
#print axioms PentagonAdjoinedSixCell.IsTypedWhiskerCongruence
#print axioms PentagonAdjoinedSixCell.contextClosed_least
#print axioms PentagonAdjoinedSixCell.contextClosedSetoid
#print axioms PentagonAdjoinedSixCell.contextClosedClass
#print axioms PentagonAdjoinedSixCell.contextClosedClass_eq_iff
#print axioms PentagonAdjoinedSixCell.contextClosed_innerFace
#print axioms PentagonAdjoinedSixCell.contextClosed_fullTriplePath
#print axioms PentagonAdjoinedSixCell.contextClosed_innerFace_strictExtension
#print axioms PentagonAdjoinedSixCell.contextMissingSource
#print axioms PentagonAdjoinedSixCell.contextMissingTarget
#print axioms PentagonAdjoinedSixCell.contextMissingCompletion
#print axioms PentagonAdjoinedSixCell.contextMissing_oldObstruction
#print axioms PentagonAdjoinedSixCell.contextMissing_tailGap
#print axioms PentagonAdjoinedSixCell.contextMissing_rawGap
#print axioms PentagonAdjoinedSixCell.oldToContextClosedQuotient
#print axioms PentagonAdjoinedSixCell.oldToContextClosedQuotient_onClass
#print axioms PentagonAdjoinedSixCell.oldToContextClosedQuotient_notInjective
#print axioms PentagonAdjoinedSixCell.contextClosed_noOldReflection
#print axioms PentagonAdjoinedSixCell.contextClosed_noTailDescent
#print axioms PentagonAdjoinedSixCell.framedContextEventCounts
#print axioms PentagonAdjoinedSixCell.contextClosed_preservesEventCounts
#print axioms PentagonAdjoinedSixCell.contextClosedEventCounts
#print axioms PentagonAdjoinedSixCell.contextClosedEventCounts_onClass
#print axioms PentagonAdjoinedSixCell.contextClosed_retainsTenSymmObstruction
#print axioms PentagonAdjoinedSixCell.contextBoundarySetoid
#print axioms PentagonAdjoinedSixCell.contextClosedLeftAction
#print axioms PentagonAdjoinedSixCell.contextClosedRightAction
#print axioms PentagonAdjoinedSixCell.contextClosedLeftAction_onClass
#print axioms PentagonAdjoinedSixCell.contextClosedRightAction_onClass
#print axioms PentagonAdjoinedSixCell.contextClosedActions_commute

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
