import KUOS.Architecture.QiWuxingGK5CHP77NineCellUnitAssociativeTenthV5_15

/-!
Qi v5.16 — ORIGINAL P/M EXCHANGE × NINTH UNIT MINIMAL ELEVENTH CELL.

Qi v5.15 constructed two parallel genuinely typed tenth proof paths,
exchange then left unit and left unit then exchange. Their raw Type
values are distinct. Add EXACTLY ONE new independently typed 11D
generator exchangeUnit comparing those original tenth proof values,
without changing any existing F55/P77/GK5CG or 6D–10D source.

The selected 11D quotient equates the two tenth histories but does
not equate raw evidence. Ordered [old,unit] versus [unit,old] tenth
traces fail to descend. TWO separate event-count observers, counting
the inherited tenth wrapper and the new ninth-unit constructor,
are preserved by EVERY 11D grammar constructor and descend via
genuine Quotient.lift. Actual old P/M tenth exchange-and-reverse
and new unit-and-reverse loops carry (2,0) and (0,2) versus
reflexive (0,0), providing two independent residual obstructions.
No global thinness, arbitrary 11D coherence, groupoid inverse
cancellation or old strict source equality is asserted.

append-only / tighten-only / overwrite-forbidden / same-root.
Public root107. Lean v4.30.0-rc2, pinned mathlib
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

/-- Selected independently typed 11D comparison on ORIGINAL
10D witness terms at fixed ORIGINAL 9D source and target.
Only exchangeUnit is a new nonstrict comparison primitive.
All other constructors are typed structural closures. -/
inductive MixedExchangeUnitElevenCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    {q q' : PentagonAssocEightCell W l r s t} →
    {alpha beta : MixedCancelNineCell W l r q q'} →
    MixedUnitAssocTenCell W l r alpha beta →
    MixedUnitAssocTenCell W l r alpha beta → Type uSix where
  | strict {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (heq : xi = zeta) :
      MixedExchangeUnitElevenCell W l r xi zeta
  | exchangeUnit :
      MixedExchangeUnitElevenCell W l r
        (pmLeftUnitCriticalExchangeThenUnit l r)
        (pmLeftUnitCriticalUnitThenExchange l r)
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta) :
      MixedExchangeUnitElevenCell W l r zeta xi
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta theta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta)
      (K : MixedExchangeUnitElevenCell W l r zeta theta) :
      MixedExchangeUnitElevenCell W l r xi theta
  | tenSymm {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta) :
      MixedExchangeUnitElevenCell W l r
        (.symm xi) (.symm zeta)
  | tenTrans {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta gamma : MixedCancelNineCell W l r q q'}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r beta gamma}
      (H : MixedExchangeUnitElevenCell W l r xi xi')
      (K : MixedExchangeUnitElevenCell W l r zeta zeta') :
      MixedExchangeUnitElevenCell W l r
        (.trans xi zeta) (.trans xi' zeta')
  | nineReverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta) :
      MixedExchangeUnitElevenCell W l r
        (.nineReverse xi) (.nineReverse zeta)
  | nineChain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q₀ q₁ q₂ : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q₀ q₁}
      {gamma delta : MixedCancelNineCell W l r q₁ q₂}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r gamma delta}
      (H : MixedExchangeUnitElevenCell W l r xi xi')
      (K : MixedExchangeUnitElevenCell W l r zeta zeta') :
      MixedExchangeUnitElevenCell W l r
        (.nineChain xi zeta) (.nineChain xi' zeta')
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta) :
      MixedExchangeUnitElevenCell W l r
        (.reverseContext xi) (.reverseContext zeta)
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      {xi xi' : MixedUnitAssocTenCell W l r alpha beta}
      {zeta zeta' : MixedUnitAssocTenCell W l r gamma delta}
      (H : MixedExchangeUnitElevenCell W l r xi xi')
      (K : MixedExchangeUnitElevenCell W l r zeta zeta') :
      MixedExchangeUnitElevenCell W l r
        (.chainContext xi zeta) (.chainContext xi' zeta')
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta) :
      MixedExchangeUnitElevenCell W l r
        (.whiskerLeft before xi) (.whiskerLeft before zeta)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta)
      (after : SevenRewrite W l r d e) :
      MixedExchangeUnitElevenCell W l r
        (.whiskerRight xi after) (.whiskerRight zeta after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      (H : MixedExchangeUnitElevenCell W l r xi zeta) :
      MixedExchangeUnitElevenCell W l r
        (.inverseContext xi) (.inverseContext zeta)
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
      (H : MixedExchangeUnitElevenCell W l r xi xi')
      (K : MixedExchangeUnitElevenCell W l r zeta zeta') :
      MixedExchangeUnitElevenCell W l r
        (.compositeContext xi zeta)
        (.compositeContext xi' zeta')

def mixedExchangeUnitElevenCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) :
    MixedExchangeUnitElevenCell W long short xi xi :=
  .strict rfl

/-- This generator connects ACTUAL Qi v5.15 original tenth
values. Their raw Type-valued inequality is retained. -/
theorem mixedExchangeUnitElevenCell_relativeNecessity (l r : W) :
    Nonempty (MixedExchangeUnitElevenCell W l r
      (pmLeftUnitCriticalExchangeThenUnit l r)
      (pmLeftUnitCriticalUnitThenExchange l r)) ∧
    pmLeftUnitCriticalExchangeThenUnit l r ≠
      pmLeftUnitCriticalUnitThenExchange l r :=
  ⟨⟨.exchangeUnit⟩, pmLeftUnitCriticalRawTenGap l r⟩

theorem mixedExchangeUnitElevenCell_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi zeta : MixedUnitAssocTenCell W l r alpha beta),
      MixedExchangeUnitElevenCell W l r xi zeta → xi = zeta) := by
  intro interpret
  exact pmLeftUnitCriticalRawTenGap l r
    (interpret _ _ (.exchangeUnit))

/-- Exact chosen equivalence on ORIGINAL parallel tenth witnesses.
Neither original ninth nor tenth raw Type is modified. -/
def mixedExchangeUnitEleventhSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'} :
    Setoid (MixedUnitAssocTenCell W l r alpha beta) where
  r := fun xi zeta => Nonempty (MixedExchangeUnitElevenCell W l r xi zeta)
  iseqv := by
    constructor
    · intro xi
      exact ⟨.strict rfl⟩
    · intro xi zeta h
      rcases h with ⟨H⟩
      exact ⟨.reverse H⟩
    · intro xi zeta theta h h'
      rcases h with ⟨H⟩
      rcases h' with ⟨K⟩
      exact ⟨.chain H K⟩

def mixedExchangeUnitEleventhClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) :
    Quotient (mixedExchangeUnitEleventhSetoid W long short
      (alpha := alpha) (beta := beta)) :=
  Quotient.mk _ xi

theorem mixedExchangeUnitEleventhClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi zeta : MixedUnitAssocTenCell W long short alpha beta) :
    mixedExchangeUnitEleventhClass xi =
      mixedExchangeUnitEleventhClass zeta ↔
      Nonempty (MixedExchangeUnitElevenCell W long short xi zeta) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem mixedExchangeUnitEleventhClass_criticalDiamond (l r : W) :
    mixedExchangeUnitEleventhClass
        (pmLeftUnitCriticalExchangeThenUnit l r) =
      mixedExchangeUnitEleventhClass
        (pmLeftUnitCriticalUnitThenExchange l r) :=
  (mixedExchangeUnitEleventhClass_eq_iff _ _).2 ⟨.exchangeUnit⟩

/-- The old tenth-event ORDER cannot descend: chosen 11D
equivalence identifies genuinely different raw histories. -/
theorem mixedExchangeUnitEleventhClass_noRawTraceDescent (l r : W) :
    ¬ ∃ (observe :
      Quotient (mixedExchangeUnitEleventhSetoid W l r
        (alpha := .chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r))
        (beta := originalDoubleCancellationMThenP l r)) → List Bool),
      ∀ (xi : MixedUnitAssocTenCell W l r
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r))
        (originalDoubleCancellationMThenP l r)),
        observe (mixedExchangeUnitEleventhClass xi) =
          mixedUnitAssocTenRawTrace xi := by
  rintro ⟨observe, compatible⟩
  have h := congrArg observe
    (mixedExchangeUnitEleventhClass_criticalDiamond l r)
  rw [compatible (pmLeftUnitCriticalExchangeThenUnit l r),
    compatible (pmLeftUnitCriticalUnitThenExchange l r),
    (pmLeftUnitCriticalTraceValues l r).1,
    (pmLeftUnitCriticalTraceValues l r).2] at h
  cases h

/-- TRUE counts the genuine new ninth-unit tenth constructors;
FALSE counts inherited v5.14 tenth proof occurrences. The raw
ordered list may vary across exchangeUnit; each occurrence count
is invariant under this selected 11D grammar. -/
def eleventhTenthEventCount (isUnit : Bool) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) : Nat :=
  ninthPrimitiveEventCount isUnit (mixedUnitAssocTenRawTrace xi)

theorem eleventhOriginalPMUnitEventCounts (l r : W) :
    eleventhTenthEventCount false
      (pmLeftUnitCriticalExchangeThenUnit l r) = 1 ∧
    eleventhTenthEventCount true
      (pmLeftUnitCriticalExchangeThenUnit l r) = 1 ∧
    eleventhTenthEventCount false
      (pmLeftUnitCriticalUnitThenExchange l r) = 1 ∧
    eleventhTenthEventCount true
      (pmLeftUnitCriticalUnitThenExchange l r) = 1 := by
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  · rfl

/-- Full structural induction over ALL fourteen constructors.
This is the new observer's compatibility/descent certificate. -/
theorem mixedExchangeUnitElevenCell_preservesTenthEventCount
    (isUnit : Bool) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    {xi zeta : MixedUnitAssocTenCell W long short alpha beta}
    (H : MixedExchangeUnitElevenCell W long short xi zeta) :
    eleventhTenthEventCount isUnit xi =
      eleventhTenthEventCount isUnit zeta := by
  induction H with
  | strict heq => cases heq; rfl
  | exchangeUnit => cases isUnit <;> rfl
  | reverse H ih => exact ih.symm
  | chain H K ih ih' => exact ih.trans ih'
  | tenSymm H ih =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace,
        ninthPrimitiveEventCount_reverse] using ih
  | tenTrans H K ih ih' =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | nineReverse H ih =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace] using ih
  | nineChain H K ih ih' =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | reverseContext H ih =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace] using ih
  | chainContext H K ih ih' =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | whiskerLeft before H ih =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace] using ih
  | whiskerRight H after ih =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace] using ih
  | inverseContext H ih =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace] using ih
  | compositeContext H K ih ih' =>
      simpa only [eleventhTenthEventCount,
        mixedUnitAssocTenRawTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'

/-- Inherited-v5.14 and new-unit event counts separately descend,
using actual Nat-valued Quotient.lift. -/
def mixedExchangeUnitEleventhOldCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'} :
    Quotient (mixedExchangeUnitEleventhSetoid W long short
      (alpha := alpha) (beta := beta)) → Nat :=
  Quotient.lift
    (fun xi : MixedUnitAssocTenCell W long short alpha beta =>
      eleventhTenthEventCount false xi)
    (by
      intro xi zeta h
      rcases h with ⟨H⟩
      exact mixedExchangeUnitElevenCell_preservesTenthEventCount false H)

def mixedExchangeUnitEleventhUnitCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'} :
    Quotient (mixedExchangeUnitEleventhSetoid W long short
      (alpha := alpha) (beta := beta)) → Nat :=
  Quotient.lift
    (fun xi : MixedUnitAssocTenCell W long short alpha beta =>
      eleventhTenthEventCount true xi)
    (by
      intro xi zeta h
      rcases h with ⟨H⟩
      exact mixedExchangeUnitElevenCell_preservesTenthEventCount true H)

theorem mixedExchangeUnitEleventhOldCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) :
    mixedExchangeUnitEleventhOldCount (mixedExchangeUnitEleventhClass xi) =
      eleventhTenthEventCount false xi := rfl

theorem mixedExchangeUnitEleventhUnitCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) :
    mixedExchangeUnitEleventhUnitCount (mixedExchangeUnitEleventhClass xi) =
      eleventhTenthEventCount true xi := rfl

/-- Original P/M exchange followed by its actual reversed tenth
proof: both original nine endpoints are the v5.13 PThenM witness. -/
def eleventhOriginalPMTenRoundtrip (l r : W) :
    MixedUnitAssocTenCell W l r
      (originalDoubleCancellationPThenM l r)
      (originalDoubleCancellationPThenM l r) :=
  .trans
    (.previous (.exchangePM))
    (.symm (.previous (.exchangePM)))

theorem eleventhOriginalPMTenRoundtripCounts (l r : W) :
    eleventhTenthEventCount false
      (eleventhOriginalPMTenRoundtrip l r) = 2 ∧
    eleventhTenthEventCount false
      (mixedUnitAssocTenCell_refl (originalDoubleCancellationPThenM l r)) = 0 ∧
    eleventhTenthEventCount true
      (eleventhOriginalPMTenRoundtrip l r) = 0 := by
  constructor
  · rfl
  constructor <;> rfl

theorem eleventhOriginalPMTenRoundtrip_noComparison (l r : W) :
    ¬ Nonempty (MixedExchangeUnitElevenCell W l r
      (eleventhOriginalPMTenRoundtrip l r)
      (mixedUnitAssocTenCell_refl (originalDoubleCancellationPThenM l r))) := by
  rintro ⟨H⟩
  have h := mixedExchangeUnitElevenCell_preservesTenthEventCount false H
  have vals := eleventhOriginalPMTenRoundtripCounts l r
  rw [vals.1, vals.2.1] at h
  omega

/-- The genuinely NEW Qi v5.15 left-unit primitive roundtrip.
Its initial ninth proof is the actual original P/M typed context. -/
def eleventhOriginalUnitTenRoundtrip (l r : W) :
    MixedUnitAssocTenCell W l r
      (.chain
        (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
        (originalDoubleCancellationPThenM l r))
      (.chain
        (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
        (originalDoubleCancellationPThenM l r)) :=
  .trans
    (.leftUnit (originalDoubleCancellationPThenM l r))
    (.symm (.leftUnit (originalDoubleCancellationPThenM l r)))

theorem eleventhOriginalUnitTenRoundtripCounts (l r : W) :
    eleventhTenthEventCount true
      (eleventhOriginalUnitTenRoundtrip l r) = 2 ∧
    eleventhTenthEventCount true
      (mixedUnitAssocTenCell_refl
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r))) = 0 ∧
    eleventhTenthEventCount false
      (eleventhOriginalUnitTenRoundtrip l r) = 0 := by
  constructor
  · rfl
  constructor <;> rfl

theorem eleventhOriginalUnitTenRoundtrip_noComparison (l r : W) :
    ¬ Nonempty (MixedExchangeUnitElevenCell W l r
      (eleventhOriginalUnitTenRoundtrip l r)
      (mixedUnitAssocTenCell_refl
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r)))) := by
  rintro ⟨H⟩
  have h := mixedExchangeUnitElevenCell_preservesTenthEventCount true H
  have vals := eleventhOriginalUnitTenRoundtripCounts l r
  rw [vals.1, vals.2.1] at h
  omega

theorem eleventhOriginalPMTenRoundtrip_distinctClass (l r : W) :
    mixedExchangeUnitEleventhClass (eleventhOriginalPMTenRoundtrip l r) ≠
      mixedExchangeUnitEleventhClass
        (mixedUnitAssocTenCell_refl (originalDoubleCancellationPThenM l r)) := by
  intro h
  exact eleventhOriginalPMTenRoundtrip_noComparison l r
    ((mixedExchangeUnitEleventhClass_eq_iff _ _).1 h)

theorem eleventhOriginalUnitTenRoundtrip_distinctClass (l r : W) :
    mixedExchangeUnitEleventhClass (eleventhOriginalUnitTenRoundtrip l r) ≠
      mixedExchangeUnitEleventhClass
        (mixedUnitAssocTenCell_refl
          (.chain
            (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
            (originalDoubleCancellationPThenM l r))) := by
  intro h
  exact eleventhOriginalUnitTenRoundtrip_noComparison l r
    ((mixedExchangeUnitEleventhClass_eq_iff _ _).1 h)

theorem mixedExchangeUnitElevenCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi zeta : MixedUnitAssocTenCell W l r alpha beta),
      Nonempty (MixedExchangeUnitElevenCell W l r xi zeta)) := by
  intro interpret
  exact eleventhOriginalPMTenRoundtrip_noComparison l r
    (interpret _ _)

/-- A new 11D relation between original 10D values cannot conjure
an old 10D witness between two originally noncomparable 9D
values: the independently proven P/M ninth-loop obstruction holds. -/
theorem mixedExchangeUnitElevenCell_retainsNinthObstruction (l r : W) :
    ¬ Nonempty (MixedUnitAssocTenCell W l r
      (ninthOriginalMixedCancelLoop l r)
      (mixedCancelNineCell_refl (ninthMixedRoundtrip l r))) :=
  ninthOriginalMixedLoop_noUnitAssocComparison l r

theorem mixedExchangeUnitElevenCell_retainsEighthObstruction (l r : W) :
    ¬ Nonempty (MixedCancelNineCell W l r
      (ninthDoubleReflexiveChain l r)
      (ninthPentagonReflexive l r)) :=
  mixedUnitAssocTenCell_retainsEighthObstruction l r

/-- No left inverse on all raw tenth values of the local chosen
eleventh quotient: original proof-history information is lost. -/
theorem mixedExchangeUnitEleventhClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
      Quotient (mixedExchangeUnitEleventhSetoid W l r
        (alpha := .chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r))
        (beta := originalDoubleCancellationMThenP l r)) →
      MixedUnitAssocTenCell W l r
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r))
        (originalDoubleCancellationMThenP l r)),
      ∀ (xi : MixedUnitAssocTenCell W l r
        (.chain
          (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
          (originalDoubleCancellationPThenM l r))
        (originalDoubleCancellationMThenP l r)),
        decode (mixedExchangeUnitEleventhClass xi) = xi := by
  rintro ⟨decode, inv⟩
  apply pmLeftUnitCriticalRawTenGap l r
  calc
    pmLeftUnitCriticalExchangeThenUnit l r =
        decode (mixedExchangeUnitEleventhClass
          (pmLeftUnitCriticalExchangeThenUnit l r)) := (inv _).symm
    _ = decode (mixedExchangeUnitEleventhClass
          (pmLeftUnitCriticalUnitThenExchange l r)) :=
      congrArg decode (mixedExchangeUnitEleventhClass_criticalDiamond l r)
    _ = pmLeftUnitCriticalUnitThenExchange l r := inv _

end PentagonAdjoinedSixCell

section ActualOriginalP77EleventhCompletion
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

/-- All ORIGINAL P77 final raw indices realize the independent
eleventh P/M-unit exchange, with actual GK5CG long/short Type
source evidence and strict F55/P77 equality obstruction unchanged. -/
theorem pentagonActualPMUnitEleventhCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.MixedExchangeUnitElevenCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.pmLeftUnitCriticalExchangeThenUnit
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.pmLeftUnitCriticalUnitThenExchange
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.exchangeUnit⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.MixedExchangeUnitElevenCell
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_refl
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_relativeNecessity
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhSetoid
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhClass
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhClass_eq_iff
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhClass_criticalDiamond
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhClass_noRawTraceDescent
#print axioms PentagonAdjoinedSixCell.eleventhTenthEventCount
#print axioms PentagonAdjoinedSixCell.eleventhOriginalPMUnitEventCounts
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_preservesTenthEventCount
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhOldCount
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhUnitCount
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhOldCount_onClass
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhUnitCount_onClass
#print axioms PentagonAdjoinedSixCell.eleventhOriginalPMTenRoundtrip
#print axioms PentagonAdjoinedSixCell.eleventhOriginalPMTenRoundtripCounts
#print axioms PentagonAdjoinedSixCell.eleventhOriginalPMTenRoundtrip_noComparison
#print axioms PentagonAdjoinedSixCell.eleventhOriginalUnitTenRoundtrip
#print axioms PentagonAdjoinedSixCell.eleventhOriginalUnitTenRoundtripCounts
#print axioms PentagonAdjoinedSixCell.eleventhOriginalUnitTenRoundtrip_noComparison
#print axioms PentagonAdjoinedSixCell.eleventhOriginalPMTenRoundtrip_distinctClass
#print axioms PentagonAdjoinedSixCell.eleventhOriginalUnitTenRoundtrip_distinctClass
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_retainsNinthObstruction
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitElevenCell_retainsEighthObstruction
#print axioms PentagonAdjoinedSixCell.mixedExchangeUnitEleventhClass_noRawRetraction
#print axioms pentagonActualPMUnitEleventhCompletion

end ActualOriginalP77EleventhCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
