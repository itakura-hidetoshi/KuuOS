import KUOS.Architecture.QiWuxingGK5CHP77MixedResidueMinimalHigherCompletionV5_07

/-!
Qi v5.07 supplementary certificate — salvage the genuinely nonduplicated
balanced-unit overlap and integer-V non-descent from abandoned variant
PR #3238, relative to the verified canonical Qi v5.07 theorem PR #3237.

Only the already certified MixedResidueEightCell and its one original
mixedResidue comparison generator are used. This file adds no primitive
to that independent eighth-cell presentation, does not recreate the
thirty duplicate declarations of #3238, and makes no assertion about
universal parallel histories, ninth cells or source strict equality.

Original F55/P77/GK5CG source, old comparison Type values, public root
107, Lean/mathlib pins, and protected validation-only PR #1558 remain
unchanged. Append-only / tighten-only / overwrite-forbidden / same-root.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- Even the unmodded integer V cannot be representative-independent:
the genuine new witness has V=3 versus V=5. This is a corollary of
the verified strong witness, not a new source comparison assumption. -/
theorem mixedResidueHistoryClass_noIntegerVDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      mixedResidueHistoryClass s = mixedResidueHistoryClass t →
        sevenTotalReductionCharge s = sevenTotalReductionCharge t) := by
  intro preserve
  have heq := (mixedResidueHistoryClass_strictlyNew
    (long := l) (short := r) l).1
  have h := preserve
    (sevenMixedResidueFirst (long := l) (short := r) l)
    (sevenMixedResidueSecond (long := l) (short := r) l) heq
  have vals := sevenMixedResidue_totalValues (long := l) (short := r) l
  rw [vals.1, vals.2] at h
  norm_num at h

/-- The balanced-unit seventh histories are original typed evidence,
and differ from the separately verified unit-diamond overlap. -/
def mixedResidueBalancedFirst (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (balancedUnitInvisibleSource (long := long) (short := short) w))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (balancedUnitInvisibleTarget (long := long) (short := short) w)) :=
  .congrComp (sevenMixedResidueFirst w) (sevenBalancedUnitInvisibleFirst w)

def mixedResidueBalancedSecond (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (balancedUnitInvisibleSource (long := long) (short := short) w))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (balancedUnitInvisibleTarget (long := long) (short := short) w)) :=
  .congrComp (sevenMixedResidueSecond w) (sevenBalancedUnitInvisibleSecond w)

/-- The old balanced-unit generator is transported through the
existing previous layers, with no additional mixed comparison axiom. -/
def mixedResidueBalanced_fill (w : W) :
    MixedResidueEightCell W long short
      (mixedResidueBalancedFirst (long := long) (short := short) w)
      (mixedResidueBalancedSecond (long := long) (short := short) w) :=
  .compositeContext (.mixedResidue w)
    (.previous (.previous (.balancedUnit w)))

theorem mixedResidueBalanced_noPrevious (w : W) :
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueBalancedFirst (long := long) (short := short) w)
      (mixedResidueBalancedSecond (long := long) (short := short) w)) := by
  exact mixedResidue_withPrevious_noOld
    (DoubleCompositeEightCell.previous (BalancedUnitEightCell.balancedUnit w))

/-- The balanced-unit peak is genuinely new relative to v5.05:
old V modulo four forbids a previous comparison, while the existing
one-generator mixed-residue completion connects the typed histories. -/
theorem mixedResidueBalanced_newVsOld (w : W) :
    Nonempty (MixedResidueEightCell W long short
      (mixedResidueBalancedFirst (long := long) (short := short) w)
      (mixedResidueBalancedSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueBalancedFirst (long := long) (short := short) w)
      (mixedResidueBalancedSecond (long := long) (short := short) w)) ∧
    sevenTotalReductionParity
        (mixedResidueBalancedFirst (long := long) (short := short) w) =
      sevenTotalReductionParity
        (mixedResidueBalancedSecond (long := long) (short := short) w) :=
  ⟨⟨mixedResidueBalanced_fill w⟩,
    mixedResidueBalanced_noPrevious w,
    mixedResidueEightCell_preservesVParity (mixedResidueBalanced_fill w)⟩

theorem mixedResidueBalanced_classGap (w : W) :
    mixedResidueHistoryClass
        (mixedResidueBalancedFirst (long := long) (short := short) w) =
      mixedResidueHistoryClass
        (mixedResidueBalancedSecond (long := long) (short := short) w) ∧
    doubleCompositeHistoryClass
        (mixedResidueBalancedFirst (long := long) (short := short) w) ≠
      doubleCompositeHistoryClass
        (mixedResidueBalancedSecond (long := long) (short := short) w) := by
  constructor
  · exact (mixedResidueHistoryClass_eq_iff _ _).2 ⟨mixedResidueBalanced_fill w⟩
  · intro h
    exact mixedResidueBalanced_noPrevious
      (long := long) (short := short) w
      ((doubleCompositeHistoryClass_eq_iff _ _).1 h)

/-- Restricted balanced-unit extension of the ALREADY PROVED local
critical family. This is not an assertion of global thinness. -/
inductive MixedResidueBalancedCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueCriticalPeak W l r s t) :
      MixedResidueBalancedCriticalPeak W l r s t
  | mixedBalanced (w : W) :
      MixedResidueBalancedCriticalPeak W l r
        (mixedResidueBalancedFirst (long := l) (short := r) w)
        (mixedResidueBalancedSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueBalancedCriticalPeak W l r s t) :
      MixedResidueBalancedCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : MixedResidueBalancedCriticalPeak W l r s t)
      (q' : MixedResidueBalancedCriticalPeak W l r t u) :
      MixedResidueBalancedCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : MixedResidueBalancedCriticalPeak W l r s t) :
      MixedResidueBalancedCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueBalancedCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      MixedResidueBalancedCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueBalancedCriticalPeak W l r s t) :
      MixedResidueBalancedCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : MixedResidueBalancedCriticalPeak W l r s s')
      (q' : MixedResidueBalancedCriticalPeak W l r t t') :
      MixedResidueBalancedCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

def mixedResidueBalancedCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedResidueBalancedCriticalPeak W long short s t) :
    MixedResidueEightCell W long short s t := by
  induction p with
  | previous q => exact mixedResidueCriticalPeak_fill q
  | mixedBalanced w => exact mixedResidueBalanced_fill w
  | reverse q ih => exact .reverse ih
  | chain q q' ih ih' => exact .chain ih ih'
  | whiskerLeft before q ih => exact .whiskerLeft before ih
  | whiskerRight q after ih => exact .whiskerRight ih after
  | inverseContext q ih => exact .inverseContext ih
  | compositeContext q q' ih ih' => exact .compositeContext ih ih'

theorem mixedResidueBalancedCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedResidueBalancedCriticalPeak W long short s t) :
    Nonempty (MixedResidueEightCell W long short s t) :=
  ⟨mixedResidueBalancedCriticalPeak_fill p⟩

theorem mixedResidueBalancedCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedResidueBalancedCriticalPeak W long short s t) :
    mixedResidueHistoryClass s = mixedResidueHistoryClass t :=
  (mixedResidueHistoryClass_eq_iff s t).2
    (mixedResidueBalancedCriticalPeak_joinable p)

#print axioms mixedResidueHistoryClass_noIntegerVDescent
#print axioms mixedResidueBalancedFirst
#print axioms mixedResidueBalancedSecond
#print axioms mixedResidueBalanced_fill
#print axioms mixedResidueBalanced_noPrevious
#print axioms mixedResidueBalanced_newVsOld
#print axioms mixedResidueBalanced_classGap
#print axioms MixedResidueBalancedCriticalPeak
#print axioms mixedResidueBalancedCriticalPeak_fill
#print axioms mixedResidueBalancedCriticalPeak_joinable
#print axioms mixedResidueBalancedCriticalPeak_classEq

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
