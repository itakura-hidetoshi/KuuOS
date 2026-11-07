import KUOS.Architecture.QiWuxingGK5CHP77ExchangeInverseMinimalTwelfthV5_17

/-!
Qi v5.18 — ORIGINAL LEFT/RIGHT DOUBLE WHISKER: FRAMED TWELFTH COMPLETION.

The TWO ordered whiskerings of an original eleventh witness are NOT
parallel 11D proofs in the old fiber: their seventh boundary indices
are (before ≫ (s ≫ after)) and ((before ≫ s) ≫ after).
The existing genuine EIGHTH associator connects those raw seventh
boundary presentations without equating either raw source.

Package ALL ORIGINAL sixth/seventh/eighth/ninth/tenth/eleventh
Type-valued indices in FramedEleven. Adjoin ONE local double-whisker
comparison in a NEW FRAMED twelfth presentation. Inherit the existing
Qi v5.17 twelfth proof Type through a typed previous constructor.
The selected framed 12D quotient identifies both ordered whiskering
packets, but their raw witnesses and order traces remain unequal.

Two genuine v5.16 event counts (old/unit) and the v5.17 tenSymm
event count are preserved under EVERY framed 12D constructor, with
three actual Quotient.lift observers. A tenSymm 1-vs-0 critical
witness remains noncomparable: this framed completion is NOT thin.
No ordinary same-fiber twelfth equality, universal interchanger,
original-source equality, or unconditional reindexing is asserted.

append-only / tighten-only / overwrite-forbidden / same-root.
Public root107. Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uSix
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- Heterogeneous family packaging, NOT a quotient or Eq coercion:
every field is the ORIGINAL unmodified dependent Type-valued witness.
The new comparison will be on these fully indexed packets. -/
structure FramedEleven (W : Type uSix) (l r : W) : Type uSix where
  w : W
  z : W
  c : PentagonAdjoinedSixCell W l r w z
  d : PentagonAdjoinedSixCell W l r w z
  s : SevenRewrite W l r c d
  t : SevenRewrite W l r c d
  q₀ : PentagonAssocEightCell W l r s t
  q₁ : PentagonAssocEightCell W l r s t
  alpha : MixedCancelNineCell W l r q₀ q₁
  beta : MixedCancelNineCell W l r q₀ q₁
  xi : MixedUnitAssocTenCell W l r alpha beta
  zeta : MixedUnitAssocTenCell W l r alpha beta
  H : MixedExchangeUnitElevenCell W l r xi zeta

/-- Embed an existing ORIGINAL eleventh proof, retaining its whole
sixth through tenth fiber and its raw eleventh history. -/
def framedEleven_ofRaw (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    FramedEleven W l r :=
  { w := w, z := z, c := c, d := d,
    s := s, t := t, q₀ := q, q₁ := q',
    alpha := alpha, beta := beta, xi := xi, zeta := zeta, H := H }

/-- The existing eighth-level associator is a genuine
boundary-compatibility witness, NOT equality of the raw seventh
words. This orientation is left-then-right → right-then-left. -/
def doubleWhiskerSourceBoundaryAssociate (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    (s : SevenRewrite W l r d e)
    (after : SevenRewrite W l r e f₆) :
    EightCell W l r
      (.trans before (.trans s after))
      (.trans (.trans before s) after) :=
  .reverse (.associate before s after)

def doubleWhiskerTargetBoundaryAssociate (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    (t : SevenRewrite W l r d e)
    (after : SevenRewrite W l r e f₆) :
    EightCell W l r
      (.trans before (.trans t after))
      (.trans (.trans before t) after) :=
  .reverse (.associate before t after)

/-- Two ORIGINAL raw 11D whiskerings, left applied LAST.
Its seventh boundary is right-associated, retained verbatim. -/
def doubleWhiskerLeftAfterRightFrame (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    FramedEleven W l r :=
  { w := w, z := z, c := c, d := f₆,
    s := .trans before (.trans s after),
    t := .trans before (.trans t after),
    q₀ := .whiskerLeft before (.whiskerRight q after),
    q₁ := .whiskerLeft before (.whiskerRight q' after),
    alpha := .whiskerLeft before (.whiskerRight alpha after),
    beta := .whiskerLeft before (.whiskerRight beta after),
    xi := .whiskerLeft before (.whiskerRight xi after),
    zeta := .whiskerLeft before (.whiskerRight zeta after),
    H := .whiskerLeft before (.whiskerRight H after) }

/-- The competing ORIGINAL 11D raw whiskerings, right applied LAST.
Its seventh boundary is left-associated; it is NOT definitionally
identical to the prior packet's boundary. -/
def doubleWhiskerRightAfterLeftFrame (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    FramedEleven W l r :=
  { w := w, z := z, c := c, d := f₆,
    s := .trans (.trans before s) after,
    t := .trans (.trans before t) after,
    q₀ := .whiskerRight (.whiskerLeft before q) after,
    q₁ := .whiskerRight (.whiskerLeft before q') after,
    alpha := .whiskerRight (.whiskerLeft before alpha) after,
    beta := .whiskerRight (.whiskerLeft before beta) after,
    xi := .whiskerRight (.whiskerLeft before xi) after,
    zeta := .whiskerRight (.whiskerLeft before zeta) after,
    H := .whiskerRight (.whiskerLeft before H) after }

/-- Original seventh boundaries are aligned ONLY by typed eighth
associators, in BOTH source and target. -/
theorem doubleWhiskerBoundaryCompatibility (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    (after : SevenRewrite W l r e f₆) :
    Nonempty (EightCell W l r
      (.trans before (.trans s after))
      (.trans (.trans before s) after)) ∧
    Nonempty (EightCell W l r
      (.trans before (.trans t after))
      (.trans (.trans before t) after)) :=
  ⟨⟨doubleWhiskerSourceBoundaryAssociate l r before s after⟩,
    ⟨doubleWhiskerTargetBoundaryAssociate l r before t after⟩⟩

/-- Record only the ORDER of tenth-level whisker contexts.
Unlike counts this is an intentionally raw syntax trace. -/
def mixedTenWhiskerRawTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) : List Bool :=
  match xi with
  | .strict _ => []
  | .previous _ => []
  | .leftUnit _ => []
  | .rightUnit _ => []
  | .assoc _ _ _ => []
  | .symm xi => mixedTenWhiskerRawTrace xi
  | .trans xi zeta =>
      mixedTenWhiskerRawTrace xi ++ mixedTenWhiskerRawTrace zeta
  | .nineReverse xi => mixedTenWhiskerRawTrace xi
  | .nineChain xi zeta =>
      mixedTenWhiskerRawTrace xi ++ mixedTenWhiskerRawTrace zeta
  | .reverseContext xi => mixedTenWhiskerRawTrace xi
  | .chainContext xi zeta =>
      mixedTenWhiskerRawTrace xi ++ mixedTenWhiskerRawTrace zeta
  | .whiskerLeft _ xi => false :: mixedTenWhiskerRawTrace xi
  | .whiskerRight xi _ => true :: mixedTenWhiskerRawTrace xi
  | .inverseContext xi => mixedTenWhiskerRawTrace xi
  | .compositeContext xi zeta =>
      mixedTenWhiskerRawTrace xi ++ mixedTenWhiskerRawTrace zeta

def framedWhiskerRawTrace (F : FramedEleven W long short) : List Bool :=
  mixedTenWhiskerRawTrace F.xi

theorem doubleWhiskerRawTraceValues (l r : W) {w z : W}
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
        false :: true :: mixedTenWhiskerRawTrace xi ∧
    framedWhiskerRawTrace
        (doubleWhiskerRightAfterLeftFrame l r before H after) =
        true :: false :: mixedTenWhiskerRawTrace xi :=
  ⟨rfl, rfl⟩

/-- The genuine raw frame packets are DIFFERENT, since their
ordered tenth context syntax is distinct before any new quotient. -/
theorem doubleWhiskerRawFrameGap (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    doubleWhiskerLeftAfterRightFrame l r before H after ≠
      doubleWhiskerRightAfterLeftFrame l r before H after := by
  intro h
  have ht := congrArg framedWhiskerRawTrace h
  rw [(doubleWhiskerRawTraceValues l r before H after).1,
    (doubleWhiskerRawTraceValues l r before H after).2] at ht
  cases ht

/-- EXACT original v5.16 exchangeUnit with ACTUAL raw type indices.
Reflexive seven-cell whiskering gives one concrete local peak. -/
def originalDoubleWhiskerLeftFrame (l r : W) : FramedEleven W l r :=
  doubleWhiskerLeftAfterRightFrame l r
    (.refl _) (.exchangeUnit) (.refl _)

def originalDoubleWhiskerRightFrame (l r : W) : FramedEleven W l r :=
  doubleWhiskerRightAfterLeftFrame l r
    (.refl _) (.exchangeUnit) (.refl _)

/-- A separately typed framed 12D comparison on the complete
dependent 11D packets, rather than an ill-typed SAME-FIBER claim.
PREVIOUS embeds the entire existing v5.17 twelfth grammar.
Only doubleWhisker is a genuinely new local primitive. -/
inductive FramedDoubleWhiskerTwelveCell (W : Type uSix) (l r : W) :
    FramedEleven W l r → FramedEleven W l r → Type uSix where
  | strict (F : FramedEleven W l r) :
      FramedDoubleWhiskerTwelveCell W l r F F
  | previous {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      FramedDoubleWhiskerTwelveCell W l r
        (framedEleven_ofRaw l r H) (framedEleven_ofRaw l r K)
  | doubleWhisker {w z : W}
      {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta)
      (after : SevenRewrite W l r e f₆) :
      FramedDoubleWhiskerTwelveCell W l r
        (doubleWhiskerLeftAfterRightFrame l r before H after)
        (doubleWhiskerRightAfterLeftFrame l r before H after)
  | reverse {F G : FramedEleven W l r}
      (T : FramedDoubleWhiskerTwelveCell W l r F G) :
      FramedDoubleWhiskerTwelveCell W l r G F
  | chain {F G K : FramedEleven W l r}
      (T : FramedDoubleWhiskerTwelveCell W l r F G)
      (U : FramedDoubleWhiskerTwelveCell W l r G K) :
      FramedDoubleWhiskerTwelveCell W l r F K

theorem originalDoubleWhiskerFramedCompletion (l r : W) :
    Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (originalDoubleWhiskerLeftFrame l r)
      (originalDoubleWhiskerRightFrame l r)) ∧
    originalDoubleWhiskerLeftFrame l r ≠
      originalDoubleWhiskerRightFrame l r :=
  ⟨⟨.doubleWhisker (.refl _) (.exchangeUnit) (.refl _)⟩,
    doubleWhiskerRawFrameGap l r (.refl _) (.exchangeUnit) (.refl _)⟩

/-- The new framed relation cannot be interpreted as literal Eq
of the original indexed packets. -/
theorem framedDoubleWhisker_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ (F G : FramedEleven W l r),
      FramedDoubleWhiskerTwelveCell W l r F G → F = G) := by
  intro interpret
  exact (originalDoubleWhiskerFramedCompletion l r).2
    (interpret _ _ (.doubleWhisker (.refl _) (.exchangeUnit) (.refl _)))

def framedDoubleWhiskerSetoid (W : Type uSix) (l r : W) :
    Setoid (FramedEleven W l r) where
  r := fun F G => Nonempty (FramedDoubleWhiskerTwelveCell W l r F G)
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

def framedDoubleWhiskerClass (F : FramedEleven W long short) :
    Quotient (framedDoubleWhiskerSetoid W long short) :=
  Quotient.mk _ F

theorem framedDoubleWhiskerClass_eq_iff
    (F G : FramedEleven W long short) :
    framedDoubleWhiskerClass F = framedDoubleWhiskerClass G ↔
      Nonempty (FramedDoubleWhiskerTwelveCell W long short F G) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem framedDoubleWhiskerClass_originalCritical (l r : W) :
    framedDoubleWhiskerClass (originalDoubleWhiskerLeftFrame l r) =
      framedDoubleWhiskerClass (originalDoubleWhiskerRightFrame l r) :=
  (framedDoubleWhiskerClass_eq_iff _ _).2
    (originalDoubleWhiskerFramedCompletion l r).1

/-- Ordered raw tenth whisker trace does NOT descend over the new
framed quotient: actual left/right original exchange frames coincide
only after the new interchanger. -/
theorem framedDoubleWhiskerClass_noRawTraceDescent (l r : W) :
    ¬ ∃ (observe : Quotient (framedDoubleWhiskerSetoid W l r) →
      List Bool),
      ∀ (F : FramedEleven W l r),
        observe (framedDoubleWhiskerClass F) =
          framedWhiskerRawTrace F := by
  rintro ⟨observe, compatible⟩
  have h := congrArg observe
    (framedDoubleWhiskerClass_originalCritical l r)
  rw [compatible (originalDoubleWhiskerLeftFrame l r),
    compatible (originalDoubleWhiskerRightFrame l r)] at h
  change (false :: true :: mixedTenWhiskerRawTrace
      (pmLeftUnitCriticalExchangeThenUnit l r)) =
    (true :: false :: mixedTenWhiskerRawTrace
      (pmLeftUnitCriticalExchangeThenUnit l r)) at h
  cases h

/-- Two inherited tenth-operation observers, on the ORIGINAL
tenth source member of each full witness packet. -/
def framedOldTenthEventCount (F : FramedEleven W long short) : Nat :=
  eleventhTenthEventCount false F.xi

def framedUnitTenthEventCount (F : FramedEleven W long short) : Nat :=
  eleventhTenthEventCount true F.xi

/-- A third independent observer on the ORIGINAL eleventh witness
history, obtained from the genuinely established v5.17 invariant. -/
def framedTenSymmEventCount (F : FramedEleven W long short) : Nat :=
  eleventhTenSymmEventCount F.H

theorem framedDoubleWhisker_preservesOldCount
    {F G : FramedEleven W long short}
    (T : FramedDoubleWhiskerTwelveCell W long short F G) :
    framedOldTenthEventCount F = framedOldTenthEventCount G := by
  induction T with
  | strict F => rfl
  | previous T => rfl
  | doubleWhisker before H after => rfl
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'

theorem framedDoubleWhisker_preservesUnitCount
    {F G : FramedEleven W long short}
    (T : FramedDoubleWhiskerTwelveCell W long short F G) :
    framedUnitTenthEventCount F = framedUnitTenthEventCount G := by
  induction T with
  | strict F => rfl
  | previous T => rfl
  | doubleWhisker before H after => rfl
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'

theorem framedDoubleWhisker_preservesTenSymmCount
    {F G : FramedEleven W long short}
    (T : FramedDoubleWhiskerTwelveCell W long short F G) :
    framedTenSymmEventCount F = framedTenSymmEventCount G := by
  induction T with
  | strict F => rfl
  | previous T =>
      exact mixedExchangeInverseTwelveCell_preservesTenSymmCount T
  | doubleWhisker before H after => rfl
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'

def framedDoubleWhiskerOldCount :
    Quotient (framedDoubleWhiskerSetoid W long short) → Nat :=
  Quotient.lift
    (fun F : FramedEleven W long short => framedOldTenthEventCount F)
    (by
      intro F G h
      rcases h with ⟨T⟩
      exact framedDoubleWhisker_preservesOldCount T)

def framedDoubleWhiskerUnitCount :
    Quotient (framedDoubleWhiskerSetoid W long short) → Nat :=
  Quotient.lift
    (fun F : FramedEleven W long short => framedUnitTenthEventCount F)
    (by
      intro F G h
      rcases h with ⟨T⟩
      exact framedDoubleWhisker_preservesUnitCount T)

def framedDoubleWhiskerTenSymmCount :
    Quotient (framedDoubleWhiskerSetoid W long short) → Nat :=
  Quotient.lift
    (fun F : FramedEleven W long short => framedTenSymmEventCount F)
    (by
      intro F G h
      rcases h with ⟨T⟩
      exact framedDoubleWhisker_preservesTenSymmCount T)

theorem framedDoubleWhiskerOldCount_onClass
    (F : FramedEleven W long short) :
    framedDoubleWhiskerOldCount (framedDoubleWhiskerClass F) =
      framedOldTenthEventCount F := rfl

theorem framedDoubleWhiskerUnitCount_onClass
    (F : FramedEleven W long short) :
    framedDoubleWhiskerUnitCount (framedDoubleWhiskerClass F) =
      framedUnitTenthEventCount F := rfl

theorem framedDoubleWhiskerTenSymmCount_onClass
    (F : FramedEleven W long short) :
    framedDoubleWhiskerTenSymmCount (framedDoubleWhiskerClass F) =
      framedTenSymmEventCount F := rfl

theorem originalDoubleWhiskerThreeCounts (l r : W) :
    framedOldTenthEventCount (originalDoubleWhiskerLeftFrame l r) = 1 ∧
    framedUnitTenthEventCount (originalDoubleWhiskerLeftFrame l r) = 1 ∧
    framedTenSymmEventCount (originalDoubleWhiskerLeftFrame l r) = 0 ∧
    framedOldTenthEventCount (originalDoubleWhiskerRightFrame l r) = 1 ∧
    framedUnitTenthEventCount (originalDoubleWhiskerRightFrame l r) = 1 ∧
    framedTenSymmEventCount (originalDoubleWhiskerRightFrame l r) = 0 := by
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  · rfl

/-- A genuine original v5.17 tenSymm wrapper and its own strict
reflexive 11D proof live in the same designated original ninth/tenth
context. Their retained 1-vs-0 count obstructs ALL framed 12D paths. -/
def framedOriginalTenSymmCriticalLoop (l r : W) : FramedEleven W l r :=
  framedEleven_ofRaw l r (twelfthOriginalTenSymmStrictLoop l r)

def framedOriginalTenSymmCriticalRefl (l r : W) : FramedEleven W l r :=
  framedEleven_ofRaw l r
    (mixedExchangeUnitElevenCell_refl
      (.symm (pmLeftUnitCriticalExchangeThenUnit l r)))

theorem framedOriginalTenSymmCountGap (l r : W) :
    framedTenSymmEventCount (framedOriginalTenSymmCriticalLoop l r) = 1 ∧
    framedTenSymmEventCount (framedOriginalTenSymmCriticalRefl l r) = 0 :=
  ⟨rfl, rfl⟩

theorem framedOriginalTenSymm_noComparison (l r : W) :
    ¬ Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (framedOriginalTenSymmCriticalLoop l r)
      (framedOriginalTenSymmCriticalRefl l r)) := by
  rintro ⟨T⟩
  have h := framedDoubleWhisker_preservesTenSymmCount T
  rw [(framedOriginalTenSymmCountGap l r).1,
    (framedOriginalTenSymmCountGap l r).2] at h
  omega

theorem framedOriginalTenSymm_distinctClass (l r : W) :
    framedDoubleWhiskerClass (framedOriginalTenSymmCriticalLoop l r) ≠
      framedDoubleWhiskerClass (framedOriginalTenSymmCriticalRefl l r) := by
  intro h
  exact framedOriginalTenSymm_noComparison l r
    ((framedDoubleWhiskerClass_eq_iff _ _).1 h)

theorem framedDoubleWhisker_notGloballyThin (l r : W) :
    ¬ (∀ (F G : FramedEleven W l r),
      Nonempty (FramedDoubleWhiskerTwelveCell W l r F G)) := by
  intro interpret
  exact framedOriginalTenSymm_noComparison l r
    (interpret _ _)

/-- No global decoder recovers raw packets from the selected
new framed twelfth quotient: exact original order is lost. -/
theorem framedDoubleWhiskerClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
        Quotient (framedDoubleWhiskerSetoid W l r) →
          FramedEleven W l r),
      ∀ (F : FramedEleven W l r),
        decode (framedDoubleWhiskerClass F) = F := by
  rintro ⟨decode, inv⟩
  apply (originalDoubleWhiskerFramedCompletion l r).2
  calc
    originalDoubleWhiskerLeftFrame l r =
        decode (framedDoubleWhiskerClass
          (originalDoubleWhiskerLeftFrame l r)) := (inv _).symm
    _ = decode (framedDoubleWhiskerClass
          (originalDoubleWhiskerRightFrame l r)) :=
      congrArg decode (framedDoubleWhiskerClass_originalCritical l r)
    _ = originalDoubleWhiskerRightFrame l r := inv _

/-- Adjoining the single framed interchanger changes no OLD
same-fiber 11D comparison. In particular both old tenth inverse
roundtrip barriers are retained, not silently filled by reindexing. -/
theorem framedDoubleWhisker_retainsOriginalTenthBarriers (l r : W) :
    ¬ Nonempty (MixedExchangeUnitElevenCell W l r
      (eleventhOriginalPMTenRoundtrip l r)
      (mixedUnitAssocTenCell_refl (originalDoubleCancellationPThenM l r))) ∧
    ¬ Nonempty (MixedExchangeUnitElevenCell W l r
      (eleventhOriginalUnitTenRoundtrip l r)
      (mixedUnitAssocTenCell_refl
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r)))) :=
  mixedExchangeInverseTwelveCell_retainsOriginalTenthObstructions l r

end PentagonAdjoinedSixCell

section ActualOriginalP77DoubleWhiskerFramedCompletion
variable {u v : FivefoldPathVertex}
variable {family₀ family₁ family₂ family₃ family₄ : Family f g h k u v}
variable {s₀ : State f g h k family₀}
variable {s₁ : State f g h k family₁}
variable {s₂ : State f g h k family₂}
variable {s₃ : State f g h k family₃}
variable {s₄ : State f g h k family₄}
variable (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
variable (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
variable (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃)
variable (D₄ : DirectNormalBracketTree f g h k family₃ s₃ family₄ s₄)

/-- Every ORIGINAL P77 final raw index instantiates the newly
framed 12D double-whisker interchanger with genuine GK5CG long/short
Type-valued endpoints, but still does not admit an old source
strict-equality interpreter. -/
theorem pentagonActualDoubleWhiskerFramedCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.FramedDoubleWhiskerTwelveCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.originalDoubleWhiskerLeftFrame
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.originalDoubleWhiskerRightFrame
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨(PentagonAdjoinedSixCell.originalDoubleWhiskerFramedCompletion
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)).1,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.FramedEleven
#print axioms PentagonAdjoinedSixCell.framedEleven_ofRaw
#print axioms PentagonAdjoinedSixCell.doubleWhiskerSourceBoundaryAssociate
#print axioms PentagonAdjoinedSixCell.doubleWhiskerTargetBoundaryAssociate
#print axioms PentagonAdjoinedSixCell.doubleWhiskerLeftAfterRightFrame
#print axioms PentagonAdjoinedSixCell.doubleWhiskerRightAfterLeftFrame
#print axioms PentagonAdjoinedSixCell.doubleWhiskerBoundaryCompatibility
#print axioms PentagonAdjoinedSixCell.mixedTenWhiskerRawTrace
#print axioms PentagonAdjoinedSixCell.framedWhiskerRawTrace
#print axioms PentagonAdjoinedSixCell.doubleWhiskerRawTraceValues
#print axioms PentagonAdjoinedSixCell.doubleWhiskerRawFrameGap
#print axioms PentagonAdjoinedSixCell.originalDoubleWhiskerLeftFrame
#print axioms PentagonAdjoinedSixCell.originalDoubleWhiskerRightFrame
#print axioms PentagonAdjoinedSixCell.FramedDoubleWhiskerTwelveCell
#print axioms PentagonAdjoinedSixCell.originalDoubleWhiskerFramedCompletion
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerSetoid
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerClass
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerClass_eq_iff
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerClass_originalCritical
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerClass_noRawTraceDescent
#print axioms PentagonAdjoinedSixCell.framedOldTenthEventCount
#print axioms PentagonAdjoinedSixCell.framedUnitTenthEventCount
#print axioms PentagonAdjoinedSixCell.framedTenSymmEventCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_preservesOldCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_preservesUnitCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_preservesTenSymmCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerOldCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerUnitCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerTenSymmCount
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerOldCount_onClass
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerUnitCount_onClass
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerTenSymmCount_onClass
#print axioms PentagonAdjoinedSixCell.originalDoubleWhiskerThreeCounts
#print axioms PentagonAdjoinedSixCell.framedOriginalTenSymmCriticalLoop
#print axioms PentagonAdjoinedSixCell.framedOriginalTenSymmCriticalRefl
#print axioms PentagonAdjoinedSixCell.framedOriginalTenSymmCountGap
#print axioms PentagonAdjoinedSixCell.framedOriginalTenSymm_noComparison
#print axioms PentagonAdjoinedSixCell.framedOriginalTenSymm_distinctClass
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_notGloballyThin
#print axioms PentagonAdjoinedSixCell.framedDoubleWhiskerClass_noRawRetraction
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_retainsOriginalTenthBarriers
#print axioms pentagonActualDoubleWhiskerFramedCompletion

end ActualOriginalP77DoubleWhiskerFramedCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
