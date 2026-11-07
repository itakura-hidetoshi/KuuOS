import KUOS.Architecture.QiWuxingGK5CHP77DoubleCompositeCancellationResidualV5_04

/-!
Qi v5.05 — MINIMAL DOUBLE-COMPOSITE HIGHER COMPLETION.

Qi v5.04 produced two genuine same-endpoint original seven-cell
histories of paired composite inverse cancellation. The histories
have equal old R and U parities (both zero), but different original
integer total-reduction charge V=2 versus V=6. A full constructor
induction proved that no v5.03 BalancedUnitEightCell comparison can
join them; the obstruction was also transported with genuine GK5CG
source Type values to every original P77 terminal raw index.

Here we add precisely ONE comparison family doubleComposite(w)
to a NEW INDEPENDENT DoubleCompositeEightCell Type. The previous
BalancedUnitEightCell presentation and all original source Types,
raw histories, old quotients and strict equality boundaries remain
untouched. Existing typed old comparisons embed with previous and
the new comparison admits only reversible/chain and typed context
closures. The selected quotient is proved STRICTLY coarser.

The full new higher grammar conserves V modulo FOUR and both the old
R mod-two and U mod-two observations. All three observables descend
to the new selected quotient by genuine Quotient.lift. The previous
unreduced integer V provably DOES NOT descend, because 2 != 6.

Two original mixed critical pairs are filled using ONLY this one
new primitive and the pre-existing balancedUnit or unitDiamond
comparisons; the same pairs cannot be filled in the old chosen
grammar by the original integer V obstruction. A restricted typed
critical family admits a constructive all-constructor filler.
At every original P77 terminal raw index the actual GK5CG source
witness transports the old/no-old/new comparison distinction, while
the original strict source equality interpreter remains impossible.

No arbitrary all-parallel-history comparison, ninth cell, global
thinness or source Eq promotion is asserted.
Append-only / tighten-only / overwrite-forbidden / same-root.
Public root107; protected validation-only #1558 Draft/OPEN.
Pinned Lean v4.30.0-rc2 and mathlib
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

/-- The NEW independent higher presentation includes every old
BalancedUnitEightCell through previous, and introduces precisely ONE
genuinely new primitive, the certified v5.04 double cancellation
comparison. Other generators are ordinary typed coherence contexts.
No old source or previous higher Type is changed or replaced. -/
inductive DoubleCompositeEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitEightCell W l r s t) :
      DoubleCompositeEightCell W l r s t
  | doubleComposite (w : W) :
      DoubleCompositeEightCell W l r
        (sevenDoubleCompositeCancelFirst (long := l) (short := r) w)
        (sevenDoubleCompositeCancelSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeEightCell W l r s t) :
      DoubleCompositeEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : DoubleCompositeEightCell W l r s t)
      (q' : DoubleCompositeEightCell W l r t u) :
      DoubleCompositeEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : DoubleCompositeEightCell W l r s t) :
      DoubleCompositeEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      DoubleCompositeEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeEightCell W l r s t) :
      DoubleCompositeEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : DoubleCompositeEightCell W l r s s')
      (q' : DoubleCompositeEightCell W l r t t') :
      DoubleCompositeEightCell W l r
        (.congrComp s t) (.congrComp s' t')

def doubleCompositeEightCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : BalancedUnitEightCell W long short s t) :
    DoubleCompositeEightCell W long short s t :=
  .previous q

def doubleCompositeEightCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    DoubleCompositeEightCell W long short s s :=
  .previous (balancedUnitEightCell_refl s)

/-- A new proof Type witness genuinely exists, whereas the earlier
selected eighth-cell grammar cannot possibly express its comparison. -/
theorem doubleCompositeEightCell_strictlyNew (w : W) :
    Nonempty (DoubleCompositeEightCell W long short
      (sevenDoubleCompositeCancelFirst (long := long) (short := short) w)
      (sevenDoubleCompositeCancelSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (BalancedUnitEightCell W long short
      (sevenDoubleCompositeCancelFirst (long := long) (short := short) w)
      (sevenDoubleCompositeCancelSecond (long := long) (short := short) w)) :=
  ⟨⟨.doubleComposite w⟩,
    sevenDoubleCompositeCancel_noComparison (long := long) (short := short) w⟩

theorem doubleCompositeEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      DoubleCompositeEightCell W l r s t →
        BalancedUnitEightCell W l r s t) := by
  rintro ⟨interpret⟩
  have q : BalancedUnitEightCell W l r
      (sevenDoubleCompositeCancelFirst (long := l) (short := r) l)
      (sevenDoubleCompositeCancelSecond (long := l) (short := r) l) :=
    interpret _ _ (.doubleComposite l)
  exact sevenDoubleCompositeCancel_noComparison (long := l) (short := r) l ⟨q⟩

theorem doubleCompositeEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      DoubleCompositeEightCell W l r s t → s = t) := by
  intro interpret
  apply balancedUnitEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t (.previous q)

/-- The old R mod-two observation survives the ONE new primitive and
all chosen typed contexts of the independent new higher grammar. -/
theorem doubleCompositeEightCell_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : DoubleCompositeEightCell W long short s t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  induction q with
  | previous q => exact balancedUnitEightCell_preservesParity q
  | doubleComposite w =>
      exact (sevenDoubleCompositeCancel_sameParities
        (long := long) (short := short) w).1
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenIdentityParity] at ih ⊢
      simp only [sevenIdentityBalance]
      omega
  | whiskerRight q after ih =>
      simp only [sevenIdentityParity] at ih ⊢
      simp only [sevenIdentityBalance]
      omega
  | inverseContext q ih =>
      simpa [sevenIdentityParity, sevenIdentityBalance] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenIdentityParity] at ih ih' ⊢
      simp only [sevenIdentityBalance]
      omega

/-- The old U mod-two observation survives the same new grammar.
This is a separate descent, not an unjustified independent-bit claim. -/
theorem doubleCompositeEightCell_preservesUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : DoubleCompositeEightCell W long short s t) :
    sevenUnitCountParity s = sevenUnitCountParity t := by
  induction q with
  | previous q => exact balancedUnitEightCell_preservesUnitCountParity q
  | doubleComposite w =>
      exact (sevenDoubleCompositeCancel_sameParities
        (long := long) (short := short) w).2
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenUnitCountParity] at ih ⊢
      simp only [sevenUnitStepCharge]
      omega
  | whiskerRight q after ih =>
      simp only [sevenUnitCountParity] at ih ⊢
      simp only [sevenUnitStepCharge]
      omega
  | inverseContext q ih =>
      simpa [sevenUnitCountParity, sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenUnitCountParity] at ih ih' ⊢
      simp only [sevenUnitStepCharge]
      omega

/-- The exact old unreduced V charge is destroyed by 2 versus 6,
but V modulo FOUR remains equal on that new primitive. -/
def sevenTotalReductionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  sevenTotalReductionCharge s % 4

theorem sevenDoubleCompositeCancel_residueValues (w : W) :
    sevenTotalReductionResidue
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) = 2 ∧
    sevenTotalReductionResidue
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) = 2 := by
  have vals := sevenDoubleCompositeCancel_values
    (long := long) (short := short) w
  constructor <;>
    norm_num [sevenTotalReductionResidue, vals.1, vals.2.1]

/-- The ENTIRE chosen higher comparison grammar conserves V mod 4.
The new doubleComposite has V=2 vs 6; all earlier comparisons
conserve unreduced V, by the v5.04 theorem. -/
theorem doubleCompositeEightCell_preservesTotalReductionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : DoubleCompositeEightCell W long short s t) :
    sevenTotalReductionResidue s = sevenTotalReductionResidue t := by
  induction q with
  | previous q =>
      exact congrArg (fun n : ℤ => n % 4)
        (balancedUnitEightCell_preservesTotalReductionCharge q)
  | doubleComposite w =>
      exact (sevenDoubleCompositeCancel_residueValues
        (long := long) (short := short) w).1.trans
        (sevenDoubleCompositeCancel_residueValues
          (long := long) (short := short) w).2.symm
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenTotalReductionResidue] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | whiskerRight q after ih =>
      simp only [sevenTotalReductionResidue] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | inverseContext q ih =>
      simpa [sevenTotalReductionResidue, sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenTotalReductionResidue] at ih ih' ⊢
      simp only [sevenTotalReductionCharge]
      omega

/-- New selected quotient as a separate construction. Every old
higher comparison class equality remains valid in the new quotient. -/
def doubleCompositeHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (DoubleCompositeEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨doubleCompositeEightCell_refl s⟩
    · intro s t h
      rcases h with ⟨q⟩
      exact ⟨.reverse q⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def doubleCompositeHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (doubleCompositeHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem doubleCompositeHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    doubleCompositeHistoryClass s = doubleCompositeHistoryClass t ↔
      Nonempty (DoubleCompositeEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem balancedUnitHistoryClass_descendsToDoubleComposite {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : balancedUnitHistoryClass s = balancedUnitHistoryClass t) :
    doubleCompositeHistoryClass s = doubleCompositeHistoryClass t := by
  rcases (balancedUnitHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (doubleCompositeHistoryClass_eq_iff s t).2 ⟨.previous q⟩

theorem doubleCompositeHistoryClass_strictlyNew (w : W) :
    (doubleCompositeHistoryClass
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) =
      doubleCompositeHistoryClass
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w)) ∧
    (balancedUnitHistoryClass
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) ≠
      balancedUnitHistoryClass
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w)) :=
  ⟨(doubleCompositeHistoryClass_eq_iff _ _).2 ⟨.doubleComposite w⟩,
    sevenDoubleCompositeCancel_distinctClasses (long := long) (short := short) w⟩

theorem doubleCompositeHistoryClass_noPreviousReturn (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      doubleCompositeHistoryClass s = doubleCompositeHistoryClass t →
        balancedUnitHistoryClass s = balancedUnitHistoryClass t) := by
  intro interpret
  have witness := doubleCompositeHistoryClass_strictlyNew
    (long := l) (short := r) l
  exact witness.2 (interpret
    (sevenDoubleCompositeCancelFirst (long := l) (short := r) l)
    (sevenDoubleCompositeCancelSecond (long := l) (short := r) l) witness.1)

theorem doubleCompositeHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      doubleCompositeHistoryClass s = doubleCompositeHistoryClass t → s = t) := by
  intro interpret
  apply doubleCompositeEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((doubleCompositeHistoryClass_eq_iff s t).2 ⟨q⟩)

/-- Integer V does NOT descend into the strictly coarser quotient. -/
theorem doubleCompositeHistoryClass_noIntegerVDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      doubleCompositeHistoryClass s = doubleCompositeHistoryClass t →
        sevenTotalReductionCharge s = sevenTotalReductionCharge t) := by
  intro preserve
  have h := (doubleCompositeHistoryClass_strictlyNew
    (long := l) (short := r) l).1
  have heq := preserve
    (sevenDoubleCompositeCancelFirst (long := l) (short := r) l)
    (sevenDoubleCompositeCancelSecond (long := l) (short := r) l) h
  have vals := sevenDoubleCompositeCancel_values (long := l) (short := r) l
  rw [vals.1, vals.2.1] at heq
  norm_num at heq

/-- Genuine V mod 4 observer on the new selected quotient. -/
def doubleCompositeHistoryV4 {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (doubleCompositeHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenTotalReductionResidue s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact doubleCompositeEightCell_preservesTotalReductionResidue q)

theorem doubleCompositeHistoryV4_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    doubleCompositeHistoryV4
        (doubleCompositeHistoryClass (long := long) (short := short) s) =
      sevenTotalReductionResidue s :=
  rfl

/-- Retain old R mod 2 and old U mod 2 as separate, but not
independent, Bool-valued quotient observations. -/
def doubleCompositeHistoryParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (doubleCompositeHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenIdentityParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (doubleCompositeEightCell_preservesParity q))

def doubleCompositeHistoryUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (doubleCompositeHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenUnitCountParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (doubleCompositeEightCell_preservesUnitCountParity q))

theorem doubleCompositeHistoryParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    doubleCompositeHistoryParity
      (doubleCompositeHistoryClass (long := long) (short := short) s) =
        decide (sevenIdentityParity s = 1) :=
  rfl

theorem doubleCompositeHistoryUnitCountParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    doubleCompositeHistoryUnitCountParity
      (doubleCompositeHistoryClass (long := long) (short := short) s) =
        decide (sevenUnitCountParity s = 1) :=
  rfl

/-- Source transport of the one new primitive: the ACTUAL
GK5CG/P77 six-cell value c is unchanged on both sides. -/
def doubleCompositeSource_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DoubleCompositeEightCell W long short
      (sevenDoubleCompositeSourceFirst c)
      (sevenDoubleCompositeSourceSecond c) :=
  .compositeContext (.doubleComposite w)
    (doubleCompositeEightCell_refl (.refl c))

theorem doubleCompositeSource_strictComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (DoubleCompositeEightCell W long short
      (sevenDoubleCompositeSourceFirst c)
      (sevenDoubleCompositeSourceSecond c)) ∧
    ¬ Nonempty (BalancedUnitEightCell W long short
      (sevenDoubleCompositeSourceFirst c)
      (sevenDoubleCompositeSourceSecond c)) ∧
    sevenIdentityParity (sevenDoubleCompositeSourceFirst c) =
      sevenIdentityParity (sevenDoubleCompositeSourceSecond c) ∧
    sevenUnitCountParity (sevenDoubleCompositeSourceFirst c) =
      sevenUnitCountParity (sevenDoubleCompositeSourceSecond c) :=
  ⟨⟨doubleCompositeSource_fill c⟩,
    sevenDoubleCompositeSource_noComparison c,
    (sevenDoubleCompositeSource_values c).1.1,
    (sevenDoubleCompositeSource_values c).1.2⟩

/-- First actually typed MIXED comparison: new doubleComposite
against the old balancedUnit generator in a horizontal context. -/
def mixedDoubleCompositeBalancedFirst (w : W) :
    SevenRewrite W long short
      (.trans
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w))
        (balancedUnitInvisibleSource (long := long) (short := short) w))
      (.trans (.trans (.refl w) (.refl w))
        (balancedUnitInvisibleTarget (long := long) (short := short) w)) :=
  .congrComp (sevenDoubleCompositeCancelFirst w)
    (sevenBalancedUnitInvisibleFirst w)

def mixedDoubleCompositeBalancedSecond (w : W) :
    SevenRewrite W long short
      (.trans
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w))
        (balancedUnitInvisibleSource (long := long) (short := short) w))
      (.trans (.trans (.refl w) (.refl w))
        (balancedUnitInvisibleTarget (long := long) (short := short) w)) :=
  .congrComp (sevenDoubleCompositeCancelSecond w)
    (sevenBalancedUnitInvisibleSecond w)

def mixedDoubleCompositeBalanced_fill (w : W) :
    DoubleCompositeEightCell W long short
      (mixedDoubleCompositeBalancedFirst (long := long) (short := short) w)
      (mixedDoubleCompositeBalancedSecond (long := long) (short := short) w) :=
  .compositeContext (.doubleComposite w) (.previous (.balancedUnit w))

theorem mixedDoubleCompositeBalanced_noPrevious (w : W) :
    ¬ Nonempty (BalancedUnitEightCell W long short
      (mixedDoubleCompositeBalancedFirst (long := long) (short := short) w)
      (mixedDoubleCompositeBalancedSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := balancedUnitEightCell_preservesTotalReductionCharge q
  have vals := sevenDoubleCompositeCancel_values (long := long) (short := short) w
  have bw := sevenBalancedUnitInvisible_totalValues
    (long := long) (short := short) w
  norm_num [mixedDoubleCompositeBalancedFirst,
    mixedDoubleCompositeBalancedSecond, sevenTotalReductionCharge,
    vals.1, vals.2.1, bw.1, bw.2] at h

/-- Second actual MIXED comparison: new doubleComposite and the
previously verified v5.01 left/right unit diamond comparison. -/
def mixedDoubleCompositeUnitFirst (w : W) :
    SevenRewrite W long short
      (.trans
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w))
        (.trans (.refl w) (.refl w)))
      (.trans (.trans (.refl w) (.refl w)) (.refl w)) :=
  .congrComp (sevenDoubleCompositeCancelFirst w) (sevenUnitDiamondLeft w)

def mixedDoubleCompositeUnitSecond (w : W) :
    SevenRewrite W long short
      (.trans
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w))
        (.trans (.refl w) (.refl w)))
      (.trans (.trans (.refl w) (.refl w)) (.refl w)) :=
  .congrComp (sevenDoubleCompositeCancelSecond w) (sevenUnitDiamondRight w)

def mixedDoubleCompositeUnit_fill (w : W) :
    DoubleCompositeEightCell W long short
      (mixedDoubleCompositeUnitFirst (long := long) (short := short) w)
      (mixedDoubleCompositeUnitSecond (long := long) (short := short) w) :=
  .compositeContext (.doubleComposite w) (.previous (.previous (.unitDiamond w)))

theorem mixedDoubleCompositeUnit_noPrevious (w : W) :
    ¬ Nonempty (BalancedUnitEightCell W long short
      (mixedDoubleCompositeUnitFirst (long := long) (short := short) w)
      (mixedDoubleCompositeUnitSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := balancedUnitEightCell_preservesTotalReductionCharge q
  have vals := sevenDoubleCompositeCancel_values (long := long) (short := short) w
  norm_num [mixedDoubleCompositeUnitFirst, mixedDoubleCompositeUnitSecond,
    sevenTotalReductionCharge, sevenUnitDiamondLeft, sevenUnitDiamondRight,
    vals.1, vals.2.1] at h

theorem mixedDoubleCompositeBalanced_newVsOld (w : W) :
    Nonempty (DoubleCompositeEightCell W long short
      (mixedDoubleCompositeBalancedFirst (long := long) (short := short) w)
      (mixedDoubleCompositeBalancedSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (BalancedUnitEightCell W long short
      (mixedDoubleCompositeBalancedFirst (long := long) (short := short) w)
      (mixedDoubleCompositeBalancedSecond (long := long) (short := short) w)) ∧
    sevenTotalReductionResidue
        (mixedDoubleCompositeBalancedFirst (long := long) (short := short) w) =
      sevenTotalReductionResidue
        (mixedDoubleCompositeBalancedSecond (long := long) (short := short) w) :=
  ⟨⟨mixedDoubleCompositeBalanced_fill w⟩,
    mixedDoubleCompositeBalanced_noPrevious w,
    doubleCompositeEightCell_preservesTotalReductionResidue
      (mixedDoubleCompositeBalanced_fill w)⟩

theorem mixedDoubleCompositeUnit_newVsOld (w : W) :
    Nonempty (DoubleCompositeEightCell W long short
      (mixedDoubleCompositeUnitFirst (long := long) (short := short) w)
      (mixedDoubleCompositeUnitSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (BalancedUnitEightCell W long short
      (mixedDoubleCompositeUnitFirst (long := long) (short := short) w)
      (mixedDoubleCompositeUnitSecond (long := long) (short := short) w)) ∧
    sevenTotalReductionResidue
        (mixedDoubleCompositeUnitFirst (long := long) (short := short) w) =
      sevenTotalReductionResidue
        (mixedDoubleCompositeUnitSecond (long := long) (short := short) w) :=
  ⟨⟨mixedDoubleCompositeUnit_fill w⟩,
    mixedDoubleCompositeUnit_noPrevious w,
    doubleCompositeEightCell_preservesTotalReductionResidue
      (mixedDoubleCompositeUnit_fill w)⟩

/-- A selected local critical family; previous v5.03 witnesses,
ONE new primitive and two genuinely mixed pairs plus full typed
context closure. NO arbitrary comparison constructor is allowed. -/
inductive DoubleCompositeCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitCriticalPeak W l r s t) :
      DoubleCompositeCriticalPeak W l r s t
  | doubleComposite (w : W) :
      DoubleCompositeCriticalPeak W l r
        (sevenDoubleCompositeCancelFirst (long := l) (short := r) w)
        (sevenDoubleCompositeCancelSecond (long := l) (short := r) w)
  | mixedBalanced (w : W) :
      DoubleCompositeCriticalPeak W l r
        (mixedDoubleCompositeBalancedFirst (long := l) (short := r) w)
        (mixedDoubleCompositeBalancedSecond (long := l) (short := r) w)
  | mixedUnitDiamond (w : W) :
      DoubleCompositeCriticalPeak W l r
        (mixedDoubleCompositeUnitFirst (long := l) (short := r) w)
        (mixedDoubleCompositeUnitSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeCriticalPeak W l r s t) :
      DoubleCompositeCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : DoubleCompositeCriticalPeak W l r s t)
      (q' : DoubleCompositeCriticalPeak W l r t u) :
      DoubleCompositeCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : DoubleCompositeCriticalPeak W l r s t) :
      DoubleCompositeCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      DoubleCompositeCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeCriticalPeak W l r s t) :
      DoubleCompositeCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : DoubleCompositeCriticalPeak W l r s s')
      (q' : DoubleCompositeCriticalPeak W l r t t') :
      DoubleCompositeCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

def doubleCompositeCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : DoubleCompositeCriticalPeak W long short s t) :
    DoubleCompositeEightCell W long short s t := by
  induction p with
  | previous q => exact .previous (balancedUnitCriticalPeak_fill q)
  | doubleComposite w => exact .doubleComposite w
  | mixedBalanced w => exact mixedDoubleCompositeBalanced_fill w
  | mixedUnitDiamond w => exact mixedDoubleCompositeUnit_fill w
  | reverse q ih => exact .reverse ih
  | chain q q' ih ih' => exact .chain ih ih'
  | whiskerLeft before q ih => exact .whiskerLeft before ih
  | whiskerRight q after ih => exact .whiskerRight ih after
  | inverseContext q ih => exact .inverseContext ih
  | compositeContext q q' ih ih' => exact .compositeContext ih ih'

theorem doubleCompositeCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : DoubleCompositeCriticalPeak W long short s t) :
    Nonempty (DoubleCompositeEightCell W long short s t) :=
  ⟨doubleCompositeCriticalPeak_fill p⟩

theorem doubleCompositeCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : DoubleCompositeCriticalPeak W long short s t) :
    doubleCompositeHistoryClass s = doubleCompositeHistoryClass t :=
  (doubleCompositeHistoryClass_eq_iff s t).2
    (doubleCompositeCriticalPeak_joinable p)

end PentagonAdjoinedSixCell

section ActualOriginalP77DoubleCompositeCompletion
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

/-- At EVERY original P77 terminal raw index, the SAME truly sourced
v5.04 two-copy original history is newly comparable in the independent
selected v5.05 grammar but not under old v5.03 comparisons.
Both previously proven residual parities are preserved; the original
strict GK5CG source EqualityInterpreter remains impossible. -/
theorem pentagonActualDoubleCompositeCompletionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.DoubleCompositeEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c)
        (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.BalancedUnitEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c)
        (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c)) ∧
      PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c) =
        PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c) ∧
      PentagonAdjoinedSixCell.sevenUnitCountParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c) =
        PentagonAdjoinedSixCell.sevenUnitCountParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.doubleCompositeSource_fill _⟩,
    PentagonAdjoinedSixCell.sevenDoubleCompositeSource_noComparison _,
    (PentagonAdjoinedSixCell.sevenDoubleCompositeSource_values _).1.1,
    (PentagonAdjoinedSixCell.sevenDoubleCompositeSource_values _).1.2,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.DoubleCompositeEightCell
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_refl
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_preservesParity
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_preservesUnitCountParity
#print axioms PentagonAdjoinedSixCell.sevenTotalReductionResidue
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancel_residueValues
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_preservesTotalReductionResidue
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistorySetoid
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass_descendsToDoubleComposite
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_noPreviousReturn
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_noStrictReturn
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_noIntegerVDescent
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryV4
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryV4_onClass
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryParity
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryUnitCountParity
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryParity_onClass
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryUnitCountParity_onClass
#print axioms PentagonAdjoinedSixCell.doubleCompositeSource_fill
#print axioms PentagonAdjoinedSixCell.doubleCompositeSource_strictComparison
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeBalancedFirst
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeBalancedSecond
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeBalanced_fill
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeBalanced_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeUnitFirst
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeUnitSecond
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeUnit_fill
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeUnit_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeBalanced_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedDoubleCompositeUnit_newVsOld
#print axioms PentagonAdjoinedSixCell.DoubleCompositeCriticalPeak
#print axioms PentagonAdjoinedSixCell.doubleCompositeCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.doubleCompositeCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.doubleCompositeCriticalPeak_classEq
#print axioms pentagonActualDoubleCompositeCompletionWithSourceObstruction

end ActualOriginalP77DoubleCompositeCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
