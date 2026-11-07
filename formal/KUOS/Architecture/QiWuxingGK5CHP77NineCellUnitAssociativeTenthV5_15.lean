import KUOS.Architecture.QiWuxingGK5CHP77PMCriticalDiamondMinimalTenthComparisonV5_14

/-!
Qi v5.15 — NINTH-CELL UNIT AND ASSOCIATIVITY TENTH COMPLETION.

Preserve all old source Type-valued evidence and all prior tenth
comparisons, and adjoin precisely leftUnit, rightUnit and assoc
as new primitive typed tenth comparison kinds. The former ninth
free-chain structural charge does NOT descend across the new unit.
The two separate P/M primitive-cancellation counts DO descend
through every old/new tenth constructor, via actual Quotient.lift.
Two original cancel-and-reverse loops retain separate 2-vs-0
obstructions. A local exchange-versus-unit critical overlap has
two strictly different raw tenth paths with the same ninth bounds:
a possible 11th-cell problem, with no 11th-cell no-go asserted.

No weakening, raw Eq coercion, extra axioms, or global thinness.
append-only / tighten-only / overwrite-forbidden / same-root.
Public root107; Lean v4.30.0-rc2; pinned mathlib
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

/-- The new selected tenth comparison with three typed unit/assoc laws. -/
inductive MixedUnitAssocTenCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    {q q' : PentagonAssocEightCell W l r s t} →
    MixedCancelNineCell W l r q q' →
    MixedCancelNineCell W l r q q' → Type uSix where
  | strict {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (heq : alpha = beta) :
      MixedUnitAssocTenCell W l r alpha beta
  | previous {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta) :
      MixedUnitAssocTenCell W l r alpha beta
  | leftUnit {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q') :
      MixedUnitAssocTenCell W l r
        (.chain (mixedCancelNineCell_refl q) alpha) alpha
  | rightUnit {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q') :
      MixedUnitAssocTenCell W l r
        (.chain alpha (mixedCancelNineCell_refl q')) alpha
  | assoc {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q₀ q₁ q₂ q₃ : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q₀ q₁)
      (beta : MixedCancelNineCell W l r q₁ q₂)
      (gamma : MixedCancelNineCell W l r q₂ q₃) :
      MixedUnitAssocTenCell W l r
        (.chain (.chain alpha beta) gamma)
        (.chain alpha (.chain beta gamma))
  | symm {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta) :
      MixedUnitAssocTenCell W l r beta alpha
  | trans {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta gamma : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta)
      (zeta : MixedUnitAssocTenCell W l r beta gamma) :
      MixedUnitAssocTenCell W l r alpha gamma
  | nineReverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta) :
      MixedUnitAssocTenCell W l r
        (.reverse alpha) (.reverse beta)
  | nineChain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' q'' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r q' q''}
      (xi : MixedUnitAssocTenCell W l r alpha beta)
      (zeta : MixedUnitAssocTenCell W l r gamma delta) :
      MixedUnitAssocTenCell W l r
        (.chain alpha gamma) (.chain beta delta)
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta) :
      MixedUnitAssocTenCell W l r
        (.reverseContext alpha) (.reverseContext beta)
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      (xi : MixedUnitAssocTenCell W l r alpha beta)
      (zeta : MixedUnitAssocTenCell W l r gamma delta) :
      MixedUnitAssocTenCell W l r
        (.chainContext alpha gamma) (.chainContext beta delta)
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta) :
      MixedUnitAssocTenCell W l r
        (.whiskerLeft before alpha) (.whiskerLeft before beta)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta)
      (after : SevenRewrite W l r d e) :
      MixedUnitAssocTenCell W l r
        (.whiskerRight alpha after) (.whiskerRight beta after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta) :
      MixedUnitAssocTenCell W l r
        (.inverseContext alpha) (.inverseContext beta)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      {q q' : PentagonAssocEightCell W l r s s'}
      {b b' : PentagonAssocEightCell W l r t t'}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      (xi : MixedUnitAssocTenCell W l r alpha beta)
      (zeta : MixedUnitAssocTenCell W l r gamma delta) :
      MixedUnitAssocTenCell W l r
        (.compositeContext alpha gamma)
        (.compositeContext beta delta)


def mixedUnitAssocTenCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    MixedUnitAssocTenCell W long short alpha alpha :=
  .strict rfl

/-- New unit strictly coarsens v5.14: its actual reflexive ninth
free-chain pair had NO old tenth comparison. -/
theorem mixedUnitAssocTenCell_strictlyNew (l r : W) :
    Nonempty (MixedUnitAssocTenCell W l r
      (tenthDoubleReflexiveNine l r)
      (mixedCancelNineCell_refl (ninthPentagonReflexive l r))) ∧
    ¬ Nonempty (MixedInterchangeTenCell W l r
      (tenthDoubleReflexiveNine l r)
      (mixedCancelNineCell_refl (ninthPentagonReflexive l r))) :=
  ⟨⟨.leftUnit (mixedCancelNineCell_refl (ninthPentagonReflexive l r))⟩,
    tenthDoubleReflexive_noInterchangeTenComparison l r⟩

theorem mixedUnitAssocTenCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha beta : MixedCancelNineCell W l r q q'),
      MixedUnitAssocTenCell W l r alpha beta →
        MixedInterchangeTenCell W l r alpha beta) := by
  rintro ⟨interpret⟩
  exact tenthDoubleReflexive_noInterchangeTenComparison l r
    ⟨interpret _ _ (.leftUnit
      (mixedCancelNineCell_refl (ninthPentagonReflexive l r)))⟩

theorem mixedUnitAssocTenCell_rawUnitGap (l r : W) :
    tenthDoubleReflexiveNine l r ≠
      mixedCancelNineCell_refl (ninthPentagonReflexive l r) := by
  intro h
  have hc := congrArg tenthResidualNineChainCharge h
  have vals := tenthDoubleReflexiveNineChainChargeValues l r
  rw [vals.1, vals.2] at hc
  omega

theorem mixedUnitAssocTenCell_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha beta : MixedCancelNineCell W l r q q'),
      MixedUnitAssocTenCell W l r alpha beta → alpha = beta) := by
  intro interpret
  exact mixedUnitAssocTenCell_rawUnitGap l r
    (interpret _ _ (.leftUnit
      (mixedCancelNineCell_refl (ninthPentagonReflexive l r))))

/-- This is an honest nonempty-typed comparison relation, not
equality imposed on the untouched original raw ninth proof Type. -/
def mixedUnitAssocTenthSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t} :
    Setoid (MixedCancelNineCell W l r q q') where
  r := fun alpha beta => Nonempty (MixedUnitAssocTenCell W l r alpha beta)
  iseqv := by
    constructor
    · intro alpha
      exact ⟨.strict rfl⟩
    · intro alpha beta h
      rcases h with ⟨xi⟩
      exact ⟨.symm xi⟩
    · intro alpha beta gamma h h'
      rcases h with ⟨xi⟩
      rcases h' with ⟨zeta⟩
      exact ⟨.trans xi zeta⟩

def mixedUnitAssocTenthClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    Quotient (mixedUnitAssocTenthSetoid W long short
      (q := q) (q' := q')) :=
  Quotient.mk _ alpha

theorem mixedUnitAssocTenthClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha beta : MixedCancelNineCell W long short q q') :
    mixedUnitAssocTenthClass alpha =
      mixedUnitAssocTenthClass beta ↔
      Nonempty (MixedUnitAssocTenCell W long short alpha beta) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem mixedInterchangeTenthClass_descendsToUnitAssoc {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha beta : MixedCancelNineCell W long short q q')
    (h : mixedInterchangeTenthClass alpha =
      mixedInterchangeTenthClass beta) :
    mixedUnitAssocTenthClass alpha =
      mixedUnitAssocTenthClass beta := by
  rcases (mixedInterchangeTenthClass_eq_iff alpha beta).1 h with ⟨xi⟩
  exact (mixedUnitAssocTenthClass_eq_iff alpha beta).2
    ⟨.previous xi⟩

theorem mixedUnitAssocTenthClass_strictlyNew (l r : W) :
    (mixedUnitAssocTenthClass (tenthDoubleReflexiveNine l r) =
      mixedUnitAssocTenthClass
        (mixedCancelNineCell_refl (ninthPentagonReflexive l r))) ∧
    (mixedInterchangeTenthClass (tenthDoubleReflexiveNine l r) ≠
      mixedInterchangeTenthClass
        (mixedCancelNineCell_refl (ninthPentagonReflexive l r))) :=
  ⟨(mixedUnitAssocTenthClass_eq_iff _ _).2
    ⟨.leftUnit (mixedCancelNineCell_refl (ninthPentagonReflexive l r))⟩,
    tenthDoubleReflexive_distinctInterchangeClass l r⟩

/-- Original nonnegative ninth-chain structural charge becomes
NON-DESCENDING after the genuine new unit comparison. -/
theorem mixedUnitAssocTenthClass_noOldChainChargeDescent (l r : W) :
    ¬ ∃ (observe :
      Quotient (mixedUnitAssocTenthSetoid W l r
        (q := ninthPentagonReflexive l r)
        (q' := ninthPentagonReflexive l r)) → Nat),
      ∀ (alpha : MixedCancelNineCell W l r
        (ninthPentagonReflexive l r)
        (ninthPentagonReflexive l r)),
        observe (mixedUnitAssocTenthClass alpha) =
          tenthResidualNineChainCharge alpha := by
  rintro ⟨observe, compatible⟩
  have heq := congrArg observe
    (mixedUnitAssocTenthClass_strictlyNew l r).1
  rw [compatible (tenthDoubleReflexiveNine l r),
    compatible (mixedCancelNineCell_refl (ninthPentagonReflexive l r)),
    (tenthDoubleReflexiveNineChainChargeValues l r).1,
    (tenthDoubleReflexiveNineChainChargeValues l r).2] at heq
  omega

/-- TRUE is P; FALSE is M. Count original cancellers in the
unchanged raw ninth proof Type, not in a fabricated source. -/
def ninthCancellationCount (isP : Bool) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') : Nat :=
  ninthPrimitiveEventCount isP (mixedCancelNinePrimitiveTrace alpha)

theorem ninthCancellationCount_refl (isP : Bool) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    ninthCancellationCount isP (mixedCancelNineCell_refl q) = 0 := rfl

/-- Full 12-constructor proof for the EXISTING tenth grammar.
The original P/M exchange changes order but not either count. -/
theorem mixedInterchangeTenCell_preservesCancellationCount
    (isP : Bool) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedInterchangeTenCell W long short alpha beta) :
    ninthCancellationCount isP alpha =
      ninthCancellationCount isP beta := by
  induction xi with
  | strict heq => cases heq; rfl
  | exchangePM => cases isP <;> rfl
  | symm xi ih => exact ih.symm
  | trans xi zeta ih ih' => exact ih.trans ih'
  | nineReverse xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_reverse] using ih
  | nineChain xi zeta ih ih' =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | reverseContext xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | chainContext xi zeta ih ih' =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | whiskerLeft before xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | whiskerRight xi after ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | inverseContext xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | compositeContext xi zeta ih ih' =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'

/-- Complete structural induction: BOTH P/M cancellation counts
survive all fifteen new tenth constructors and source contexts. -/
theorem mixedUnitAssocTenCell_preservesCancellationCount
    (isP : Bool) {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) :
    ninthCancellationCount isP alpha =
      ninthCancellationCount isP beta := by
  induction xi with
  | strict heq => cases heq; rfl
  | previous xi =>
      exact mixedInterchangeTenCell_preservesCancellationCount isP xi
  | leftUnit alpha =>
      simp [ninthCancellationCount, mixedCancelNinePrimitiveTrace,
        mixedCancelNineCell_refl, pentagonCancelNineCell_refl,
        oldPentagonCancellationTrace, ninthPrimitiveEventCount_append]
  | rightUnit alpha =>
      simp [ninthCancellationCount, mixedCancelNinePrimitiveTrace,
        mixedCancelNineCell_refl, pentagonCancelNineCell_refl,
        oldPentagonCancellationTrace, ninthPrimitiveEventCount_append]
  | assoc alpha beta gamma =>
      simp only [ninthCancellationCount, mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append, Nat.add_assoc]
  | symm xi ih => exact ih.symm
  | trans xi zeta ih ih' => exact ih.trans ih'
  | nineReverse xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_reverse] using ih
  | nineChain xi zeta ih ih' =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | reverseContext xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | chainContext xi zeta ih ih' =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'
  | whiskerLeft before xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | whiskerRight xi after ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | inverseContext xi ih =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace] using ih
  | compositeContext xi zeta ih ih' =>
      simpa only [ninthCancellationCount,
        mixedCancelNinePrimitiveTrace,
        ninthPrimitiveEventCount_append] using
        congrArg₂ (fun a b : Nat => a + b) ih ih'

/-- Two genuinely separate Quotient.lift observers on tenth classes. -/
def mixedUnitAssocTenthPCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t} :
    Quotient (mixedUnitAssocTenthSetoid W long short
      (q := q) (q' := q')) → Nat :=
  Quotient.lift
    (fun alpha : MixedCancelNineCell W long short q q' =>
      ninthCancellationCount true alpha)
    (by
      intro alpha beta h
      rcases h with ⟨xi⟩
      exact mixedUnitAssocTenCell_preservesCancellationCount true xi)

def mixedUnitAssocTenthMCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t} :
    Quotient (mixedUnitAssocTenthSetoid W long short
      (q := q) (q' := q')) → Nat :=
  Quotient.lift
    (fun alpha : MixedCancelNineCell W long short q q' =>
      ninthCancellationCount false alpha)
    (by
      intro alpha beta h
      rcases h with ⟨xi⟩
      exact mixedUnitAssocTenCell_preservesCancellationCount false xi)

theorem mixedUnitAssocTenthPCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    mixedUnitAssocTenthPCount (mixedUnitAssocTenthClass alpha) =
      ninthCancellationCount true alpha := rfl

theorem mixedUnitAssocTenthMCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    mixedUnitAssocTenthMCount (mixedUnitAssocTenthClass alpha) =
      ninthCancellationCount false alpha := rfl

/-- Genuine original M-cancel and its reversed raw ninth witness. -/
def ninthOriginalMixedCancelLoop (l r : W) :
    MixedCancelNineCell W l r
      (ninthMixedRoundtrip l r)
      (ninthMixedRoundtrip l r) :=
  .chain (.cancelMixed) (.reverse (.cancelMixed))

/-- Genuine original P-cancel and reversed raw ninth witness. -/
def ninthOriginalPentagonCancelLoop (l r : W) :
    MixedCancelNineCell W l r
      (ninthPentagonRoundtrip l r)
      (ninthPentagonRoundtrip l r) :=
  .chain (.previous (.cancelPentagon))
    (.reverse (.previous (.cancelPentagon)))

theorem ninthOriginalMixedCancelLoopCounts (l r : W) :
    ninthCancellationCount true (ninthOriginalMixedCancelLoop l r) = 0 ∧
    ninthCancellationCount false (ninthOriginalMixedCancelLoop l r) = 2 ∧
    ninthCancellationCount true
      (mixedCancelNineCell_refl (ninthMixedRoundtrip l r)) = 0 ∧
    ninthCancellationCount false
      (mixedCancelNineCell_refl (ninthMixedRoundtrip l r)) = 0 := by
  constructor
  · rfl
  constructor
  · rfl
  constructor <;> rfl

theorem ninthOriginalPentagonCancelLoopCounts (l r : W) :
    ninthCancellationCount true (ninthOriginalPentagonCancelLoop l r) = 2 ∧
    ninthCancellationCount false (ninthOriginalPentagonCancelLoop l r) = 0 ∧
    ninthCancellationCount true
      (mixedCancelNineCell_refl (ninthPentagonRoundtrip l r)) = 0 ∧
    ninthCancellationCount false
      (mixedCancelNineCell_refl (ninthPentagonRoundtrip l r)) = 0 := by
  constructor
  · rfl
  constructor
  · rfl
  constructor <;> rfl

theorem ninthOriginalMixedLoop_noUnitAssocComparison (l r : W) :
    ¬ Nonempty (MixedUnitAssocTenCell W l r
      (ninthOriginalMixedCancelLoop l r)
      (mixedCancelNineCell_refl (ninthMixedRoundtrip l r))) := by
  rintro ⟨xi⟩
  have hc := mixedUnitAssocTenCell_preservesCancellationCount false xi
  have vals := ninthOriginalMixedCancelLoopCounts l r
  rw [vals.2.1, vals.2.2.2] at hc
  omega

theorem ninthOriginalPentagonLoop_noUnitAssocComparison (l r : W) :
    ¬ Nonempty (MixedUnitAssocTenCell W l r
      (ninthOriginalPentagonCancelLoop l r)
      (mixedCancelNineCell_refl (ninthPentagonRoundtrip l r))) := by
  rintro ⟨xi⟩
  have hc := mixedUnitAssocTenCell_preservesCancellationCount true xi
  have vals := ninthOriginalPentagonCancelLoopCounts l r
  rw [vals.1, vals.2.2.1] at hc
  omega

theorem ninthOriginalMixedLoop_distinctUnitAssocClass (l r : W) :
    mixedUnitAssocTenthClass (ninthOriginalMixedCancelLoop l r) ≠
      mixedUnitAssocTenthClass
        (mixedCancelNineCell_refl (ninthMixedRoundtrip l r)) := by
  intro h
  exact ninthOriginalMixedLoop_noUnitAssocComparison l r
    ((mixedUnitAssocTenthClass_eq_iff _ _).1 h)

theorem ninthOriginalPentagonLoop_distinctUnitAssocClass (l r : W) :
    mixedUnitAssocTenthClass (ninthOriginalPentagonCancelLoop l r) ≠
      mixedUnitAssocTenthClass
        (mixedCancelNineCell_refl (ninthPentagonRoundtrip l r)) := by
  intro h
  exact ninthOriginalPentagonLoop_noUnitAssocComparison l r
    ((mixedUnitAssocTenthClass_eq_iff _ _).1 h)

theorem mixedUnitAssocTenCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha beta : MixedCancelNineCell W l r q q'),
      Nonempty (MixedUnitAssocTenCell W l r alpha beta)) := by
  intro interpret
  exact ninthOriginalMixedLoop_noUnitAssocComparison l r
    (interpret _ _)

theorem mixedUnitAssocTenCell_retainsEighthObstruction (l r : W) :
    ¬ Nonempty (MixedCancelNineCell W l r
      (ninthDoubleReflexiveChain l r)
      (ninthPentagonReflexive l r)) :=
  ninthDoubleReflexive_noMixedCancelComparison l r

/-- Genuine local critical overlap: exchange first in the left
ninth context, then unit reduction. -/
def pmLeftUnitCriticalExchangeThenUnit (l r : W) :
    MixedUnitAssocTenCell W l r
      (.chain (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
        (originalDoubleCancellationPThenM l r))
      (originalDoubleCancellationMThenP l r) :=
  .trans
    (.nineChain
      (.strict rfl)
      (.previous (.exchangePM)))
    (.leftUnit (originalDoubleCancellationMThenP l r))

/-- Competing path: left unit first, then original P/M exchange.
The ORIGINAL ninth endpoints are exactly the same. -/
def pmLeftUnitCriticalUnitThenExchange (l r : W) :
    MixedUnitAssocTenCell W l r
      (.chain (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
        (originalDoubleCancellationPThenM l r))
      (originalDoubleCancellationMThenP l r) :=
  .trans
    (.leftUnit (originalDoubleCancellationPThenM l r))
    (.previous (.exchangePM))

theorem pmLeftUnitCriticalDiamond (l r : W) :
    Nonempty (MixedUnitAssocTenCell W l r
      (.chain (mixedCancelNineCell_refl (originalDoubleCancellationTop l r))
        (originalDoubleCancellationPThenM l r))
      (originalDoubleCancellationMThenP l r)) :=
  ⟨pmLeftUnitCriticalExchangeThenUnit l r⟩

/-- false records an inherited raw tenth wrapper, true a new
tenth unit operation. A syntactic witness, NOT an 11D invariant. -/
def mixedUnitAssocTenRawTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedUnitAssocTenCell W long short alpha beta) : List Bool :=
  match xi with
  | .strict _ => []
  | .previous _ => [false]
  | .leftUnit _ => [true]
  | .rightUnit _ => [true]
  | .assoc _ _ _ => []
  | .symm xi => (mixedUnitAssocTenRawTrace xi).reverse
  | .trans xi zeta =>
      mixedUnitAssocTenRawTrace xi ++ mixedUnitAssocTenRawTrace zeta
  | .nineReverse xi => mixedUnitAssocTenRawTrace xi
  | .nineChain xi zeta =>
      mixedUnitAssocTenRawTrace xi ++ mixedUnitAssocTenRawTrace zeta
  | .reverseContext xi => mixedUnitAssocTenRawTrace xi
  | .chainContext xi zeta =>
      mixedUnitAssocTenRawTrace xi ++ mixedUnitAssocTenRawTrace zeta
  | .whiskerLeft _ xi => mixedUnitAssocTenRawTrace xi
  | .whiskerRight xi _ => mixedUnitAssocTenRawTrace xi
  | .inverseContext xi => mixedUnitAssocTenRawTrace xi
  | .compositeContext xi zeta =>
      mixedUnitAssocTenRawTrace xi ++ mixedUnitAssocTenRawTrace zeta

theorem pmLeftUnitCriticalTraceValues (l r : W) :
    mixedUnitAssocTenRawTrace (pmLeftUnitCriticalExchangeThenUnit l r) =
      [false, true] ∧
    mixedUnitAssocTenRawTrace (pmLeftUnitCriticalUnitThenExchange l r) =
      [true, false] := by
  constructor <;> rfl

/-- Eleven-cell comparison CANDIDATE (not an eleventh no-go):
two differently ordered RAW tenth pastings at the same bounds. -/
theorem pmLeftUnitCriticalRawTenGap (l r : W) :
    pmLeftUnitCriticalExchangeThenUnit l r ≠
      pmLeftUnitCriticalUnitThenExchange l r := by
  intro h
  have ht := congrArg mixedUnitAssocTenRawTrace h
  rw [(pmLeftUnitCriticalTraceValues l r).1,
    (pmLeftUnitCriticalTraceValues l r).2] at ht
  cases ht

end PentagonAdjoinedSixCell

section ActualOriginalP77UnitAssocTenth
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

/-- Every actual original P77 raw index retains GK5CG source
history and has a new typed ninth left-unit tenth comparison. -/
theorem pentagonActualNineUnitAssocTenthCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.MixedUnitAssocTenCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.tenthDoubleReflexiveNine
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.mixedCancelNineCell_refl
        (PentagonAdjoinedSixCell.ninthPentagonReflexive
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.leftUnit _⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.MixedUnitAssocTenCell
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_refl
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_rawUnitGap
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthSetoid
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthClass
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthClass_descendsToUnitAssoc
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthClass_noOldChainChargeDescent
#print axioms PentagonAdjoinedSixCell.ninthCancellationCount
#print axioms PentagonAdjoinedSixCell.ninthCancellationCount_refl
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_preservesCancellationCount
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_preservesCancellationCount
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthPCount
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthMCount
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthPCount_onClass
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenthMCount_onClass
#print axioms PentagonAdjoinedSixCell.ninthOriginalMixedCancelLoop
#print axioms PentagonAdjoinedSixCell.ninthOriginalPentagonCancelLoop
#print axioms PentagonAdjoinedSixCell.ninthOriginalMixedCancelLoopCounts
#print axioms PentagonAdjoinedSixCell.ninthOriginalPentagonCancelLoopCounts
#print axioms PentagonAdjoinedSixCell.ninthOriginalMixedLoop_noUnitAssocComparison
#print axioms PentagonAdjoinedSixCell.ninthOriginalPentagonLoop_noUnitAssocComparison
#print axioms PentagonAdjoinedSixCell.ninthOriginalMixedLoop_distinctUnitAssocClass
#print axioms PentagonAdjoinedSixCell.ninthOriginalPentagonLoop_distinctUnitAssocClass
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenCell_retainsEighthObstruction
#print axioms PentagonAdjoinedSixCell.pmLeftUnitCriticalExchangeThenUnit
#print axioms PentagonAdjoinedSixCell.pmLeftUnitCriticalUnitThenExchange
#print axioms PentagonAdjoinedSixCell.pmLeftUnitCriticalDiamond
#print axioms PentagonAdjoinedSixCell.mixedUnitAssocTenRawTrace
#print axioms PentagonAdjoinedSixCell.pmLeftUnitCriticalTraceValues
#print axioms PentagonAdjoinedSixCell.pmLeftUnitCriticalRawTenGap
#print axioms pentagonActualNineUnitAssocTenthCompletion

end ActualOriginalP77UnitAssocTenth
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
