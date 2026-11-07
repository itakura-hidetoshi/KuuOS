import KUOS.Architecture.QiWuxingGK5CHP77PMUnitExchangeMinimalEleventhV5_16

/-!
Qi v5.17 — ORIGINAL ELEVENTH INVERSE ROUNDS AND WHISKER-UNIT TWELFTH CELLS.

The original Qi v5.16 P/M-unit eleventh generator compares genuinely
distinct raw tenth witnesses. Its right and left inverse roundtrips
are genuine, distinct raw eleventh evidence from their eleventh
reflexivities; adjoin only the TWO selected inverse cancellations.
The eleventh left/right whisker of strict evidence is not definitionally
the corresponding strict eleventh evidence: add precisely typed
whisker-unit comparison generators, not equality of raw evidence.

All old sixth through eleventh proof types stay UNMODIFIED. New
twelfth closure preserves eleven-level operations and contexts.
One Nat-valued observer counting actual tenSymm wrappers survives
the ENTIRE selected twelfth grammar via Quotient.lift, leaving a
concrete original critical loop unequal to reflexivity in the
selected quotient. Global thinness and universal inverse cancellation
are NOT claimed. A left-right interchanger between distinct raw
whiskering boundary presentations is also NOT assumed.

append-only / tighten-only / overwrite-forbidden / same-root.
Public root107. Lean v4.30.0-rc2; mathlib
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

/-- The original right inverse loop at the genuinely typed
P/M-exchange / left-unit critical tenth witness. -/
def twelfthOriginalExchangeRightLoop (l r : W) :
    MixedExchangeUnitElevenCell W l r
      (pmLeftUnitCriticalExchangeThenUnit l r)
      (pmLeftUnitCriticalExchangeThenUnit l r) :=
  .chain .exchangeUnit (.reverse .exchangeUnit)

/-- The distinct original left inverse loop at the other critical
tenth witness. No raw eleventh equality is added. -/
def twelfthOriginalExchangeLeftLoop (l r : W) :
    MixedExchangeUnitElevenCell W l r
      (pmLeftUnitCriticalUnitThenExchange l r)
      (pmLeftUnitCriticalUnitThenExchange l r) :=
  .chain (.reverse .exchangeUnit) .exchangeUnit

theorem twelfthOriginalExchangeRightRawGap (l r : W) :
    twelfthOriginalExchangeRightLoop l r ≠
      mixedExchangeUnitElevenCell_refl
        (pmLeftUnitCriticalExchangeThenUnit l r) := by
  intro h
  cases h

theorem twelfthOriginalExchangeLeftRawGap (l r : W) :
    twelfthOriginalExchangeLeftLoop l r ≠
      mixedExchangeUnitElevenCell_refl
        (pmLeftUnitCriticalUnitThenExchange l r) := by
  intro h
  cases h

/-- Independently adjoined twelfth comparison of ORIGINAL eleventh
proof values, indexed by their FULL raw tenth source and target.
The only new inverse relations are the two EXACT original
exchange-unit roundtrips, not a generic groupoid axiom.
The only new whisker-unit comparisons reconcile whiskered strict
with strict at the WHISKERED original tenth witness. -/
inductive MixedExchangeInverseTwelveCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    {q q' : PentagonAssocEightCell W l r s t} →
    {alpha beta : MixedCancelNineCell W l r q q'} →
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta} →
    MixedExchangeUnitElevenCell W l r xi zeta →
    MixedExchangeUnitElevenCell W l r xi zeta → Type uSix where
  | strict {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (heq : H = K) :
      MixedExchangeInverseTwelveCell W l r H K
  | cancelExchangeRight :
      MixedExchangeInverseTwelveCell W l r
        (twelfthOriginalExchangeRightLoop l r)
        (mixedExchangeUnitElevenCell_refl
          (pmLeftUnitCriticalExchangeThenUnit l r))
  | cancelExchangeLeft :
      MixedExchangeInverseTwelveCell W l r
        (twelfthOriginalExchangeLeftLoop l r)
        (mixedExchangeUnitElevenCell_refl
          (pmLeftUnitCriticalUnitThenExchange l r))
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r K H
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K L : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K)
      (U : MixedExchangeInverseTwelveCell W l r K L) :
      MixedExchangeInverseTwelveCell W l r H L
  | elevenReverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r (.reverse H) (.reverse K)
  | elevenChain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r alpha beta}
      {H H' : MixedExchangeUnitElevenCell W l r xi zeta}
      {K K' : MixedExchangeUnitElevenCell W l r zeta zeta'}
      (T : MixedExchangeInverseTwelveCell W l r H H')
      (U : MixedExchangeInverseTwelveCell W l r K K') :
      MixedExchangeInverseTwelveCell W l r
        (.chain H K) (.chain H' K')
  | tenSymm {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r
        (.tenSymm H) (.tenSymm K)
  | tenTrans {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta gamma : MixedCancelNineCell W l r q q'}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r beta gamma}
      {H H' : MixedExchangeUnitElevenCell W l r xi xi'}
      {K K' : MixedExchangeUnitElevenCell W l r zeta zeta'}
      (T : MixedExchangeInverseTwelveCell W l r H H')
      (U : MixedExchangeInverseTwelveCell W l r K K') :
      MixedExchangeInverseTwelveCell W l r
        (.tenTrans H K) (.tenTrans H' K')
  | nineReverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r
        (.nineReverse H) (.nineReverse K)
  | nineChain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q₀ q₁ q₂ : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q₀ q₁}
      {gamma delta : MixedCancelNineCell W l r q₁ q₂}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r gamma delta}
      {H H' : MixedExchangeUnitElevenCell W l r xi xi'}
      {K K' : MixedExchangeUnitElevenCell W l r zeta zeta'}
      (T : MixedExchangeInverseTwelveCell W l r H H')
      (U : MixedExchangeInverseTwelveCell W l r K K') :
      MixedExchangeInverseTwelveCell W l r
        (.nineChain H K) (.nineChain H' K')
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r
        (.reverseContext H) (.reverseContext K)
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r gamma delta}
      {H H' : MixedExchangeUnitElevenCell W l r xi xi'}
      {K K' : MixedExchangeUnitElevenCell W l r zeta zeta'}
      (T : MixedExchangeInverseTwelveCell W l r H H')
      (U : MixedExchangeInverseTwelveCell W l r K K') :
      MixedExchangeInverseTwelveCell W l r
        (.chainContext H K) (.chainContext H' K')
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r
        (.whiskerLeft before H) (.whiskerLeft before K)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K)
      (after : SevenRewrite W l r d e) :
      MixedExchangeInverseTwelveCell W l r
        (.whiskerRight H after) (.whiskerRight K after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      MixedExchangeInverseTwelveCell W l r
        (.inverseContext H) (.inverseContext K)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      {q q' : PentagonAssocEightCell W l r s s'}
      {b b' : PentagonAssocEightCell W l r t t'}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r gamma delta}
      {H H' : MixedExchangeUnitElevenCell W l r xi xi'}
      {K K' : MixedExchangeUnitElevenCell W l r zeta zeta'}
      (T : MixedExchangeInverseTwelveCell W l r H H')
      (U : MixedExchangeInverseTwelveCell W l r K K') :
      MixedExchangeInverseTwelveCell W l r
        (.compositeContext H K) (.compositeContext H' K')
  | whiskerLeftStrict {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta) :
      MixedExchangeInverseTwelveCell W l r
        (.whiskerLeft before (.strict (xi := xi) rfl))
        (.strict rfl)
  | whiskerRightStrict {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta)
      (after : SevenRewrite W l r d e) :
      MixedExchangeInverseTwelveCell W l r
        (.whiskerRight (.strict (xi := xi) rfl) after)
        (.strict rfl)

def mixedExchangeInverseTwelveCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    (H : MixedExchangeUnitElevenCell W long short xi zeta) :
    MixedExchangeInverseTwelveCell W long short H H :=
  .strict rfl

/-- Only the selected original right/left eleventh inverse loops
are identified with strict in this new twelfth presentation. -/
theorem twelfthOriginalInverseComparison (l r : W) :
    Nonempty (MixedExchangeInverseTwelveCell W l r
      (twelfthOriginalExchangeRightLoop l r)
      (mixedExchangeUnitElevenCell_refl
        (pmLeftUnitCriticalExchangeThenUnit l r))) ∧
    Nonempty (MixedExchangeInverseTwelveCell W l r
      (twelfthOriginalExchangeLeftLoop l r)
      (mixedExchangeUnitElevenCell_refl
        (pmLeftUnitCriticalUnitThenExchange l r))) ∧
    twelfthOriginalExchangeRightLoop l r ≠
      mixedExchangeUnitElevenCell_refl
        (pmLeftUnitCriticalExchangeThenUnit l r) :=
  ⟨⟨.cancelExchangeRight⟩, ⟨⟨.cancelExchangeLeft⟩,
    twelfthOriginalExchangeRightRawGap l r⟩⟩

/-- Four new generators are local: the original two inverse
cancellations, and strict-compatibility under each whisker. -/
theorem twelfthLeftWhiskerStrictCritical
    {w z : W}
    {c d e : PentagonAdjoinedSixCell W long short w z}
    (before : SevenRewrite W long short c d)
    {s t : SevenRewrite W long short d e}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) :
    Nonempty (MixedExchangeInverseTwelveCell W long short
      (.whiskerLeft before (mixedExchangeUnitElevenCell_refl xi))
      (mixedExchangeUnitElevenCell_refl (.whiskerLeft before xi))) ∧
    (show MixedExchangeUnitElevenCell W long short
        (.whiskerLeft before xi) (.whiskerLeft before xi) from
          .whiskerLeft before (mixedExchangeUnitElevenCell_refl xi)) ≠
      mixedExchangeUnitElevenCell_refl (.whiskerLeft before xi) := by
  constructor
  · exact ⟨.whiskerLeftStrict before xi⟩
  · intro h
    cases h

theorem twelfthRightWhiskerStrictCritical
    {w z : W}
    {c d e : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta)
    (after : SevenRewrite W long short d e) :
    Nonempty (MixedExchangeInverseTwelveCell W long short
      (.whiskerRight (mixedExchangeUnitElevenCell_refl xi) after)
      (mixedExchangeUnitElevenCell_refl (.whiskerRight xi after))) ∧
    (show MixedExchangeUnitElevenCell W long short
        (.whiskerRight xi after) (.whiskerRight xi after) from
          .whiskerRight (mixedExchangeUnitElevenCell_refl xi) after) ≠
      mixedExchangeUnitElevenCell_refl (.whiskerRight xi after) := by
  constructor
  · exact ⟨.whiskerRightStrict xi after⟩
  · intro h
    cases h

/-- A selected twelfth comparison is a genuine Setoid only on
parallel original eleventh proofs, NEVER on raw tenth/ninth values. -/
def mixedExchangeInverseTwelfthSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta} :
    Setoid (MixedExchangeUnitElevenCell W l r xi zeta) where
  r := fun H K => Nonempty (MixedExchangeInverseTwelveCell W l r H K)
  iseqv := by
    constructor
    · intro H
      exact ⟨.strict rfl⟩
    · intro H K h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro H K L h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

def mixedExchangeInverseTwelfthClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    (H : MixedExchangeUnitElevenCell W long short xi zeta) :
    Quotient (mixedExchangeInverseTwelfthSetoid W long short
      (xi := xi) (zeta := zeta)) :=
  Quotient.mk _ H

theorem mixedExchangeInverseTwelfthClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    (H K : MixedExchangeUnitElevenCell W long short xi zeta) :
    mixedExchangeInverseTwelfthClass H =
      mixedExchangeInverseTwelfthClass K ↔
      Nonempty (MixedExchangeInverseTwelveCell W long short H K) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem mixedExchangeInverseTwelfthClass_cancelsOriginalRight (l r : W) :
    mixedExchangeInverseTwelfthClass
        (twelfthOriginalExchangeRightLoop l r) =
      mixedExchangeInverseTwelfthClass
        (mixedExchangeUnitElevenCell_refl
          (pmLeftUnitCriticalExchangeThenUnit l r)) :=
  (mixedExchangeInverseTwelfthClass_eq_iff _ _).2
    ⟨.cancelExchangeRight⟩

theorem mixedExchangeInverseTwelfthClass_cancelsOriginalLeft (l r : W) :
    mixedExchangeInverseTwelfthClass
        (twelfthOriginalExchangeLeftLoop l r) =
      mixedExchangeInverseTwelfthClass
        (mixedExchangeUnitElevenCell_refl
          (pmLeftUnitCriticalUnitThenExchange l r)) :=
  (mixedExchangeInverseTwelfthClass_eq_iff _ _).2
    ⟨.cancelExchangeLeft⟩

/-- Count occurrences of the ACTUAL inherited eleven-cell tenSymm
constructor, not reverse or exchange operations. The chosen new
inverse and whisker-unit generators have equal tenSymm count. -/
def eleventhTenSymmEventCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    (H : MixedExchangeUnitElevenCell W long short xi zeta) : Nat :=
  match H with
  | .strict _ => 0
  | .exchangeUnit => 0
  | .reverse H => eleventhTenSymmEventCount H
  | .chain H K => eleventhTenSymmEventCount H + eleventhTenSymmEventCount K
  | .tenSymm H => eleventhTenSymmEventCount H + 1
  | .tenTrans H K => eleventhTenSymmEventCount H + eleventhTenSymmEventCount K
  | .nineReverse H => eleventhTenSymmEventCount H
  | .nineChain H K => eleventhTenSymmEventCount H + eleventhTenSymmEventCount K
  | .reverseContext H => eleventhTenSymmEventCount H
  | .chainContext H K => eleventhTenSymmEventCount H + eleventhTenSymmEventCount K
  | .whiskerLeft _ H => eleventhTenSymmEventCount H
  | .whiskerRight H _ => eleventhTenSymmEventCount H
  | .inverseContext H => eleventhTenSymmEventCount H
  | .compositeContext H K =>
      eleventhTenSymmEventCount H + eleventhTenSymmEventCount K

/-- Prove compatibility with ALL nineteen selected twelfth
constructors (four local generators and fifteen closures). -/
theorem mixedExchangeInverseTwelveCell_preservesTenSymmCount
    {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    {H K : MixedExchangeUnitElevenCell W long short xi zeta}
    (T : MixedExchangeInverseTwelveCell W long short H K) :
    eleventhTenSymmEventCount H = eleventhTenSymmEventCount K := by
  induction T with
  | strict heq => cases heq; rfl
  | cancelExchangeRight => rfl
  | cancelExchangeLeft => rfl
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'
  | elevenReverse T ih =>
      simpa only [eleventhTenSymmEventCount] using ih
  | elevenChain T U ih ih' =>
      simpa only [eleventhTenSymmEventCount] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | tenSymm T ih =>
      simpa only [eleventhTenSymmEventCount] using
        congrArg (fun n : Nat => n + 1) ih
  | tenTrans T U ih ih' =>
      simpa only [eleventhTenSymmEventCount] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | nineReverse T ih =>
      simpa only [eleventhTenSymmEventCount] using ih
  | nineChain T U ih ih' =>
      simpa only [eleventhTenSymmEventCount] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | reverseContext T ih =>
      simpa only [eleventhTenSymmEventCount] using ih
  | chainContext T U ih ih' =>
      simpa only [eleventhTenSymmEventCount] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | whiskerLeft before T ih =>
      simpa only [eleventhTenSymmEventCount] using ih
  | whiskerRight T after ih =>
      simpa only [eleventhTenSymmEventCount] using ih
  | inverseContext T ih =>
      simpa only [eleventhTenSymmEventCount] using ih
  | compositeContext T U ih ih' =>
      simpa only [eleventhTenSymmEventCount] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | whiskerLeftStrict before xi => rfl
  | whiskerRightStrict xi after => rfl

/-- Actual Quotient.lift descent of an invariant after imposing
ONLY the selected twelfth comparisons. -/
def mixedExchangeInverseTwelfthTenSymmCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta} :
    Quotient (mixedExchangeInverseTwelfthSetoid W long short
      (xi := xi) (zeta := zeta)) → Nat :=
  Quotient.lift
    (fun H : MixedExchangeUnitElevenCell W long short xi zeta =>
      eleventhTenSymmEventCount H)
    (by
      intro H K h
      rcases h with ⟨T⟩
      exact mixedExchangeInverseTwelveCell_preservesTenSymmCount T)

theorem mixedExchangeInverseTwelfthTenSymmCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    (H : MixedExchangeUnitElevenCell W long short xi zeta) :
    mixedExchangeInverseTwelfthTenSymmCount
        (mixedExchangeInverseTwelfthClass H) =
      eleventhTenSymmEventCount H := rfl

/-- A genuine old tenth symm wrapper of strict eleventh proof is
still not twelfth-comparable to the strict eleventh proof at the
same old tenth source and target. -/
def twelfthOriginalTenSymmStrictLoop (l r : W) :
    MixedExchangeUnitElevenCell W l r
      (.symm (pmLeftUnitCriticalExchangeThenUnit l r))
      (.symm (pmLeftUnitCriticalExchangeThenUnit l r)) :=
  .tenSymm (.strict rfl)

theorem twelfthOriginalTenSymmStrictLoop_counts (l r : W) :
    eleventhTenSymmEventCount (twelfthOriginalTenSymmStrictLoop l r) = 1 ∧
    eleventhTenSymmEventCount
      (mixedExchangeUnitElevenCell_refl
        (.symm (pmLeftUnitCriticalExchangeThenUnit l r))) = 0 := by
  constructor <;> rfl

theorem twelfthOriginalTenSymmStrictLoop_noComparison (l r : W) :
    ¬ Nonempty (MixedExchangeInverseTwelveCell W l r
      (twelfthOriginalTenSymmStrictLoop l r)
      (mixedExchangeUnitElevenCell_refl
        (.symm (pmLeftUnitCriticalExchangeThenUnit l r)))) := by
  rintro ⟨T⟩
  have h := mixedExchangeInverseTwelveCell_preservesTenSymmCount T
  rw [(twelfthOriginalTenSymmStrictLoop_counts l r).1,
    (twelfthOriginalTenSymmStrictLoop_counts l r).2] at h
  omega

theorem twelfthOriginalTenSymmStrictLoop_distinctClass (l r : W) :
    mixedExchangeInverseTwelfthClass
        (twelfthOriginalTenSymmStrictLoop l r) ≠
      mixedExchangeInverseTwelfthClass
        (mixedExchangeUnitElevenCell_refl
          (.symm (pmLeftUnitCriticalExchangeThenUnit l r))) := by
  intro h
  exact twelfthOriginalTenSymmStrictLoop_noComparison l r
    ((mixedExchangeInverseTwelfthClass_eq_iff _ _).1 h)

theorem mixedExchangeInverseTwelveCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H K : MixedExchangeUnitElevenCell W l r xi zeta),
      Nonempty (MixedExchangeInverseTwelveCell W l r H K)) := by
  intro interpret
  exact twelfthOriginalTenSymmStrictLoop_noComparison l r
    (interpret _ _)

/-- Whisker 12D comparison to the original 11D strict witness:
the new whiskerStrict is ESSENTIAL in the last step. -/
theorem twelfthLeftWhiskeredCancellation
    {w z : W}
    {c d e : PentagonAdjoinedSixCell W long short w z}
    (before : SevenRewrite W long short c d)
    {s t : SevenRewrite W long short d e}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta)
    (H : MixedExchangeUnitElevenCell W long short xi xi)
    (T : MixedExchangeInverseTwelveCell W long short H
      (mixedExchangeUnitElevenCell_refl xi)) :
    Nonempty (MixedExchangeInverseTwelveCell W long short
      (.whiskerLeft before H)
      (mixedExchangeUnitElevenCell_refl (.whiskerLeft before xi))) :=
  ⟨.chain (.whiskerLeft before T) (.whiskerLeftStrict before xi)⟩

theorem twelfthRightWhiskeredCancellation
    {w z : W}
    {c d e : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta)
    (H : MixedExchangeUnitElevenCell W long short xi xi)
    (T : MixedExchangeInverseTwelveCell W long short H
      (mixedExchangeUnitElevenCell_refl xi))
    (after : SevenRewrite W long short d e) :
    Nonempty (MixedExchangeInverseTwelveCell W long short
      (.whiskerRight H after)
      (mixedExchangeUnitElevenCell_refl (.whiskerRight xi after))) :=
  ⟨.chain (.whiskerRight T after) (.whiskerRightStrict xi after)⟩

theorem mixedExchangeInverseTwelfthClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
      Quotient (mixedExchangeInverseTwelfthSetoid W l r
        (xi := pmLeftUnitCriticalExchangeThenUnit l r)
        (zeta := pmLeftUnitCriticalExchangeThenUnit l r)) →
      MixedExchangeUnitElevenCell W l r
        (pmLeftUnitCriticalExchangeThenUnit l r)
        (pmLeftUnitCriticalExchangeThenUnit l r)),
      ∀ (H : MixedExchangeUnitElevenCell W l r
        (pmLeftUnitCriticalExchangeThenUnit l r)
        (pmLeftUnitCriticalExchangeThenUnit l r)),
        decode (mixedExchangeInverseTwelfthClass H) = H := by
  rintro ⟨decode, inv⟩
  apply twelfthOriginalExchangeRightRawGap l r
  calc
    twelfthOriginalExchangeRightLoop l r =
        decode (mixedExchangeInverseTwelfthClass
          (twelfthOriginalExchangeRightLoop l r)) := (inv _).symm
    _ = decode (mixedExchangeInverseTwelfthClass
          (mixedExchangeUnitElevenCell_refl
            (pmLeftUnitCriticalExchangeThenUnit l r))) :=
      congrArg decode (mixedExchangeInverseTwelfthClass_cancelsOriginalRight l r)
    _ = mixedExchangeUnitElevenCell_refl
          (pmLeftUnitCriticalExchangeThenUnit l r) := inv _

/-- No 12D comparison changes either genuinely original v5.16
non-comparable tenth roundtrip (2,0) / (0,2) pair. -/
theorem mixedExchangeInverseTwelveCell_retainsOriginalTenthObstructions
    (l r : W) :
    ¬ Nonempty (MixedExchangeUnitElevenCell W l r
      (eleventhOriginalPMTenRoundtrip l r)
      (mixedUnitAssocTenCell_refl (originalDoubleCancellationPThenM l r))) ∧
    ¬ Nonempty (MixedExchangeUnitElevenCell W l r
      (eleventhOriginalUnitTenRoundtrip l r)
      (mixedUnitAssocTenCell_refl
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r)))) :=
  ⟨eleventhOriginalPMTenRoundtrip_noComparison l r,
    eleventhOriginalUnitTenRoundtrip_noComparison l r⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77TwelfthCompletion
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

/-- Every actual original P77 final index supplies genuine
GK5CG long/short TYPE values; the new twelfth inverse comparison
does not imply any original F55/P77 strict equality interpreter. -/
theorem pentagonActualOriginalExchangeTwelfthCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.MixedExchangeInverseTwelveCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.twelfthOriginalExchangeRightLoop
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_refl
        (PentagonAdjoinedSixCell.pmLeftUnitCriticalExchangeThenUnit
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.cancelExchangeRight⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.twelfthOriginalExchangeRightLoop
#print axioms PentagonAdjoinedSixCell.twelfthOriginalExchangeLeftLoop
#print axioms PentagonAdjoinedSixCell.twelfthOriginalExchangeRightRawGap
#print axioms PentagonAdjoinedSixCell.twelfthOriginalExchangeLeftRawGap
#print axioms PentagonAdjoinedSixCell.MixedExchangeInverseTwelveCell
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelveCell_refl
#print axioms PentagonAdjoinedSixCell.twelfthOriginalInverseComparison
#print axioms PentagonAdjoinedSixCell.twelfthLeftWhiskerStrictCritical
#print axioms PentagonAdjoinedSixCell.twelfthRightWhiskerStrictCritical
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthSetoid
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthClass
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthClass_cancelsOriginalRight
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthClass_cancelsOriginalLeft
#print axioms PentagonAdjoinedSixCell.eleventhTenSymmEventCount
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelveCell_preservesTenSymmCount
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthTenSymmCount
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthTenSymmCount_onClass
#print axioms PentagonAdjoinedSixCell.twelfthOriginalTenSymmStrictLoop
#print axioms PentagonAdjoinedSixCell.twelfthOriginalTenSymmStrictLoop_counts
#print axioms PentagonAdjoinedSixCell.twelfthOriginalTenSymmStrictLoop_noComparison
#print axioms PentagonAdjoinedSixCell.twelfthOriginalTenSymmStrictLoop_distinctClass
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelveCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.twelfthLeftWhiskeredCancellation
#print axioms PentagonAdjoinedSixCell.twelfthRightWhiskeredCancellation
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelfthClass_noRawRetraction
#print axioms PentagonAdjoinedSixCell.mixedExchangeInverseTwelveCell_retainsOriginalTenthObstructions
#print axioms pentagonActualOriginalExchangeTwelfthCompletion

end ActualOriginalP77TwelfthCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
