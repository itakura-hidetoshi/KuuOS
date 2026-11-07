import KUOS.Architecture.QiWuxingGK5CHP77MixedInverseCompResidueObstructionV5_06

/-!
Qi v5.07 — MINIMAL MIXED-RESIDUE HIGHER COMPLETION.

Qi v5.06 constructed genuine original six-cell-indexed three-factor
parallel SevenRewrite histories H₁/H₂. The old (T,J,K)=(2,0,1)
and both R mod2=0 and U mod2=1 coincide, but V mod4 is 3 against 1.
V mod4 is invariant under the ENTIRE v5.05 DoubleCompositeEightCell
grammar, so no chosen old higher comparison can possibly exist.
The original GK5CG/P77 source transport and the source strict
equality-interpreter no-go are already formally certified.

This module adds exactly ONE primitive higher comparison family
mixedResidue(w) in a NEW SEPARATE MixedResidueEightCell Type.
All earlier DoubleCompositeEightCell values survive via previous,
with the exact same typed reversal, composition and whiskering
constructors. None of the original F55/P77/GK5CG source, seven-cell
free history, old presentation, old quotient, or imports are edited.

The new quotient is STRICTLY coarser, and the old V mod4 charge
PROVABLY does not descend, since the new generator identifies the
old V mod4 classes 3 and 1. V mod2 still survives. Both old
R mod2 and U mod2 observers still survive, and all three observables
descend via independent, type-correct Quotient.lift certificates.

Two genuine mixed critical pairs, mixedResidue × doubleComposite
and mixedResidue × unitDiamond, are non-comparable in the old chosen
grammar but filled in the new grammar using the single new primitive
and old type-preserving previous comparisons. A restricted critical
family receives a complete structural-induction filler. The same
strong witness is transported into EVERY genuine original P77
terminal raw index, preserving the strict source EqualityInterpreter
impossibility. NO universal thinness, ninth cell, or arbitrary
all-parallel-history completeness is asserted.

Append-only / tighten-only / overwrite-forbidden / same-root.
Public root107; protected validation-only PR #1558 Draft/open.
Pinned Lean 4.30.0-rc2, mathlib
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

/-- The old selected eighth grammar is retained, including its
type-indexed original GK5CG/source endpoint histories. The ONLY new
primitive compares the already certified v5.06 mixed-residue pair. -/
inductive MixedResidueEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeEightCell W l r s t) :
      MixedResidueEightCell W l r s t
  | mixedResidue (w : W) :
      MixedResidueEightCell W l r
        (sevenMixedResidueFirst (long := l) (short := r) w)
        (sevenMixedResidueSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueEightCell W l r s t) :
      MixedResidueEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : MixedResidueEightCell W l r s t)
      (q' : MixedResidueEightCell W l r t u) :
      MixedResidueEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : MixedResidueEightCell W l r s t) :
      MixedResidueEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      MixedResidueEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueEightCell W l r s t) :
      MixedResidueEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : MixedResidueEightCell W l r s s')
      (q' : MixedResidueEightCell W l r t t') :
      MixedResidueEightCell W l r
        (.congrComp s t) (.congrComp s' t')

def mixedResidueEightCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : DoubleCompositeEightCell W long short s t) :
    MixedResidueEightCell W long short s t :=
  .previous q

def mixedResidueEightCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    MixedResidueEightCell W long short s s :=
  .previous (doubleCompositeEightCell_refl s)

/-- Old V-mod-four non-comparability proves that the one NEW
mixedResidue generator is not already expressible by old grammar. -/
theorem mixedResidueEightCell_strictlyNew (w : W) :
    Nonempty (MixedResidueEightCell W long short
      (sevenMixedResidueFirst (long := long) (short := short) w)
      (sevenMixedResidueSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (sevenMixedResidueFirst (long := long) (short := short) w)
      (sevenMixedResidueSecond (long := long) (short := short) w)) :=
  ⟨⟨.mixedResidue w⟩,
    sevenMixedResidue_noDoubleCompositeComparison
      (long := long) (short := short) w⟩

theorem mixedResidueEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      MixedResidueEightCell W l r s t →
        DoubleCompositeEightCell W l r s t) := by
  rintro ⟨interpret⟩
  have q : DoubleCompositeEightCell W l r
      (sevenMixedResidueFirst (long := l) (short := r) l)
      (sevenMixedResidueSecond (long := l) (short := r) l) :=
    interpret _ _ (.mixedResidue l)
  exact sevenMixedResidue_noDoubleCompositeComparison
    (long := l) (short := r) l ⟨q⟩

theorem mixedResidueEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      MixedResidueEightCell W l r s t → s = t) := by
  intro interpret
  apply doubleCompositeEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t (.previous q)

/-- Full original R-mod-two preservation over every generator and
every typed context, not only the new primitive. -/
theorem mixedResidueEightCell_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  induction q with
  | previous q => exact doubleCompositeEightCell_preservesParity q
  | mixedResidue w =>
      exact (sevenMixedResidue_sameParities
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

/-- All original U mod-two comparisons remain valid independently,
while the existing v5.04 boundary coupling is retained. -/
theorem mixedResidueEightCell_preservesUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    sevenUnitCountParity s = sevenUnitCountParity t := by
  induction q with
  | previous q => exact doubleCompositeEightCell_preservesUnitCountParity q
  | mixedResidue w =>
      exact (sevenMixedResidue_sameParities
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

/-- A canonical integer representative of V modulo TWO. The
previous V modulo FOUR quotient observer is no longer invariant. -/
def sevenTotalReductionParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  sevenTotalReductionResidue s % 2

theorem sevenMixedResidue_vParityValues (w : W) :
    sevenTotalReductionParity
        (sevenMixedResidueFirst (long := long) (short := short) w) = 1 ∧
    sevenTotalReductionParity
        (sevenMixedResidueSecond (long := long) (short := short) w) = 1 := by
  have vals := sevenMixedResidue_residueValues
    (long := long) (short := short) w
  constructor <;>
    norm_num [sevenTotalReductionParity, vals.1, vals.2]

/-- V modulo TWO survives the NEW primitive (3 versus 1 mod 4),
all previous old comparisons and every typed higher context. -/
theorem mixedResidueEightCell_preservesVParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    sevenTotalReductionParity s = sevenTotalReductionParity t := by
  induction q with
  | previous q =>
      exact congrArg (fun n : ℤ => n % 2)
        (doubleCompositeEightCell_preservesTotalReductionResidue q)
  | mixedResidue w =>
      exact (sevenMixedResidue_vParityValues
        (long := long) (short := short) w).1.trans
        (sevenMixedResidue_vParityValues
          (long := long) (short := short) w).2.symm
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenTotalReductionParity, sevenTotalReductionResidue] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | whiskerRight q after ih =>
      simp only [sevenTotalReductionParity, sevenTotalReductionResidue] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | inverseContext q ih =>
      simpa [sevenTotalReductionParity, sevenTotalReductionResidue,
        sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenTotalReductionParity, sevenTotalReductionResidue]
        at ih ih' ⊢
      simp only [sevenTotalReductionCharge]
      omega

/-- A new chosen quotient with old history Type and all its
original raw endpoint indices unchanged. -/
def mixedResidueHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (MixedResidueEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨mixedResidueEightCell_refl s⟩
    · intro s t h
      rcases h with ⟨q⟩
      exact ⟨.reverse q⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def mixedResidueHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem mixedResidueHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    mixedResidueHistoryClass s = mixedResidueHistoryClass t ↔
      Nonempty (MixedResidueEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem doubleCompositeHistoryClass_descendsToMixedResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : doubleCompositeHistoryClass s = doubleCompositeHistoryClass t) :
    mixedResidueHistoryClass s = mixedResidueHistoryClass t := by
  rcases (doubleCompositeHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (mixedResidueHistoryClass_eq_iff s t).2 ⟨.previous q⟩

theorem mixedResidueHistoryClass_strictlyNew (w : W) :
    (mixedResidueHistoryClass
        (sevenMixedResidueFirst (long := long) (short := short) w) =
      mixedResidueHistoryClass
        (sevenMixedResidueSecond (long := long) (short := short) w)) ∧
    (doubleCompositeHistoryClass
        (sevenMixedResidueFirst (long := long) (short := short) w) ≠
      doubleCompositeHistoryClass
        (sevenMixedResidueSecond (long := long) (short := short) w)) :=
  ⟨(mixedResidueHistoryClass_eq_iff _ _).2 ⟨.mixedResidue w⟩,
    sevenMixedResidue_distinctDoubleCompositeClasses
      (long := long) (short := short) w⟩

theorem mixedResidueHistoryClass_noPreviousReturn (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      mixedResidueHistoryClass s = mixedResidueHistoryClass t →
        doubleCompositeHistoryClass s = doubleCompositeHistoryClass t) := by
  intro interpret
  have witness := mixedResidueHistoryClass_strictlyNew
    (long := l) (short := r) l
  exact witness.2 (interpret
    (sevenMixedResidueFirst (long := l) (short := r) l)
    (sevenMixedResidueSecond (long := l) (short := r) l) witness.1)

theorem mixedResidueHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      mixedResidueHistoryClass s = mixedResidueHistoryClass t → s = t) := by
  intro interpret
  apply mixedResidueEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((mixedResidueHistoryClass_eq_iff s t).2 ⟨q⟩)

/-- The chosen new primitive destroys old V modulo FOUR descent,
because the old residue values are exactly 3 and 1. -/
theorem mixedResidueHistoryClass_noVFourDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      mixedResidueHistoryClass s = mixedResidueHistoryClass t →
        sevenTotalReductionResidue s = sevenTotalReductionResidue t) := by
  intro preserve
  have heq := (mixedResidueHistoryClass_strictlyNew
    (long := l) (short := r) l).1
  have h := preserve
    (sevenMixedResidueFirst (long := l) (short := r) l)
    (sevenMixedResidueSecond (long := l) (short := r) l) heq
  have vals := sevenMixedResidue_residueValues (long := l) (short := r) l
  rw [vals.1, vals.2] at h
  norm_num at h

/-- Genuine nonrepresentative-dependent V modulo TWO observer. -/
def mixedResidueHistoryVParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenTotalReductionParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (mixedResidueEightCell_preservesVParity q))

def mixedResidueHistoryParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenIdentityParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (mixedResidueEightCell_preservesParity q))

def mixedResidueHistoryUnitParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenUnitCountParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (mixedResidueEightCell_preservesUnitCountParity q))

theorem mixedResidueHistoryVParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryVParity
        (mixedResidueHistoryClass (long := long) (short := short) s) =
      decide (sevenTotalReductionParity s = 1) :=
  rfl

theorem mixedResidueHistoryParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryParity
        (mixedResidueHistoryClass (long := long) (short := short) s) =
      decide (sevenIdentityParity s = 1) :=
  rfl

theorem mixedResidueHistoryUnitParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryUnitParity
        (mixedResidueHistoryClass (long := long) (short := short) s) =
      decide (sevenUnitCountParity s = 1) :=
  rfl

/-- The old P77/GK5CG source is pasted into the same specific new
mixed-residue comparison, without any new raw original source Eq. -/
def mixedResidueSource_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    MixedResidueEightCell W long short
      (sevenMixedResidueCompositeFirst c)
      (sevenMixedResidueCompositeSecond c) :=
  .compositeContext (.mixedResidue w)
    (mixedResidueEightCell_refl (.refl c))

theorem mixedResidueSource_strictComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (MixedResidueEightCell W long short
      (sevenMixedResidueCompositeFirst c)
      (sevenMixedResidueCompositeSecond c)) ∧
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (sevenMixedResidueCompositeFirst c)
      (sevenMixedResidueCompositeSecond c)) ∧
    sevenChargeTriple (sevenMixedResidueCompositeFirst c) =
      sevenChargeTriple (sevenMixedResidueCompositeSecond c) ∧
    sevenIdentityParity (sevenMixedResidueCompositeFirst c) =
      sevenIdentityParity (sevenMixedResidueCompositeSecond c) ∧
    sevenUnitCountParity (sevenMixedResidueCompositeFirst c) =
      sevenUnitCountParity (sevenMixedResidueCompositeSecond c) :=
  ⟨⟨mixedResidueSource_fill c⟩,
    sevenMixedResidueComposite_noDoubleCompositeComparison c,
    (sevenMixedResidueComposite_values c).1,
    (sevenMixedResidueComposite_values c).2.1,
    (sevenMixedResidueComposite_values c).2.2.1⟩

/-- General typed mixed obstruction lemma. Whiskering the new
mixed-residue pair on the right by ANY old DoubleCompositeEightCell
preserves the old V mod4 gap 3 versus 1. -/
theorem mixedResidue_withPrevious_noOld {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (qOld : DoubleCompositeEightCell W long short s t) :
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (.congrComp (sevenMixedResidueFirst w) s)
      (.congrComp (sevenMixedResidueSecond w) t)) := by
  rintro ⟨q⟩
  have hc := doubleCompositeEightCell_preservesTotalReductionResidue q
  have he := doubleCompositeEightCell_preservesTotalReductionResidue qOld
  have vals := sevenMixedResidue_residueValues (long := long) (short := short) w
  simp only [sevenTotalReductionResidue, sevenTotalReductionCharge] at hc
  simp only [sevenTotalReductionResidue] at he vals
  omega

/-- MIXED 1: existing v5.05 doubleComposite source pair against one
new mixed-residue comparison, retaining original raw six-cell indices. -/
def mixedResidueDoubleFirst (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (.trans (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w)))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (.trans (.refl w) (.refl w))) :=
  .congrComp (sevenMixedResidueFirst w) (sevenDoubleCompositeCancelFirst w)

def mixedResidueDoubleSecond (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (.trans (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w)))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (.trans (.refl w) (.refl w))) :=
  .congrComp (sevenMixedResidueSecond w) (sevenDoubleCompositeCancelSecond w)

def mixedResidueDouble_fill (w : W) :
    MixedResidueEightCell W long short
      (mixedResidueDoubleFirst (long := long) (short := short) w)
      (mixedResidueDoubleSecond (long := long) (short := short) w) :=
  .compositeContext (.mixedResidue w) (.previous (.doubleComposite w))

theorem mixedResidueDouble_noPrevious (w : W) :
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueDoubleFirst (long := long) (short := short) w)
      (mixedResidueDoubleSecond (long := long) (short := short) w)) := by
  exact mixedResidue_withPrevious_noOld (.doubleComposite w)

/-- MIXED 2: the original v5.01 unitDiamond is explicitly inherited
through two previous layers, with the same source and target raw words. -/
def mixedResidueUnitFirst (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (.trans (.refl w) (.refl w)))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (.refl w)) :=
  .congrComp (sevenMixedResidueFirst w) (sevenUnitDiamondLeft w)

def mixedResidueUnitSecond (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (.trans (.refl w) (.refl w)))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (.refl w)) :=
  .congrComp (sevenMixedResidueSecond w) (sevenUnitDiamondRight w)

def mixedResidueUnit_fill (w : W) :
    MixedResidueEightCell W long short
      (mixedResidueUnitFirst (long := long) (short := short) w)
      (mixedResidueUnitSecond (long := long) (short := short) w) :=
  .compositeContext (.mixedResidue w)
    (.previous (.previous (.previous (.unitDiamond w))))

theorem mixedResidueUnit_noPrevious (w : W) :
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueUnitFirst (long := long) (short := short) w)
      (mixedResidueUnitSecond (long := long) (short := short) w)) := by
  exact mixedResidue_withPrevious_noOld
    (DoubleCompositeEightCell.previous (BalancedUnitEightCell.previous
      (UnitDiamondEightCell.unitDiamond w)))

theorem mixedResidueDouble_newVsOld (w : W) :
    Nonempty (MixedResidueEightCell W long short
      (mixedResidueDoubleFirst (long := long) (short := short) w)
      (mixedResidueDoubleSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueDoubleFirst (long := long) (short := short) w)
      (mixedResidueDoubleSecond (long := long) (short := short) w)) ∧
    sevenTotalReductionParity (mixedResidueDoubleFirst w) =
      sevenTotalReductionParity (mixedResidueDoubleSecond w) :=
  ⟨⟨mixedResidueDouble_fill w⟩,
    mixedResidueDouble_noPrevious w,
    mixedResidueEightCell_preservesVParity (mixedResidueDouble_fill w)⟩

theorem mixedResidueUnit_newVsOld (w : W) :
    Nonempty (MixedResidueEightCell W long short
      (mixedResidueUnitFirst (long := long) (short := short) w)
      (mixedResidueUnitSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueUnitFirst (long := long) (short := short) w)
      (mixedResidueUnitSecond (long := long) (short := short) w)) ∧
    sevenTotalReductionParity (mixedResidueUnitFirst w) =
      sevenTotalReductionParity (mixedResidueUnitSecond w) :=
  ⟨⟨mixedResidueUnit_fill w⟩,
    mixedResidueUnit_noPrevious w,
    mixedResidueEightCell_preservesVParity (mixedResidueUnit_fill w)⟩

/-- Only the selected newly proved obstruction, old v5.05 selected
critical family and two genuine mixed comparisons, with typed closure. -/
inductive MixedResidueCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : DoubleCompositeCriticalPeak W l r s t) :
      MixedResidueCriticalPeak W l r s t
  | mixedResidue (w : W) :
      MixedResidueCriticalPeak W l r
        (sevenMixedResidueFirst (long := l) (short := r) w)
        (sevenMixedResidueSecond (long := l) (short := r) w)
  | mixedDouble (w : W) :
      MixedResidueCriticalPeak W l r
        (mixedResidueDoubleFirst (long := l) (short := r) w)
        (mixedResidueDoubleSecond (long := l) (short := r) w)
  | mixedUnitDiamond (w : W) :
      MixedResidueCriticalPeak W l r
        (mixedResidueUnitFirst (long := l) (short := r) w)
        (mixedResidueUnitSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueCriticalPeak W l r s t) :
      MixedResidueCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : MixedResidueCriticalPeak W l r s t)
      (q' : MixedResidueCriticalPeak W l r t u) :
      MixedResidueCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : MixedResidueCriticalPeak W l r s t) :
      MixedResidueCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      MixedResidueCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueCriticalPeak W l r s t) :
      MixedResidueCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : MixedResidueCriticalPeak W l r s s')
      (q' : MixedResidueCriticalPeak W l r t t') :
      MixedResidueCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

def mixedResidueCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedResidueCriticalPeak W long short s t) :
    MixedResidueEightCell W long short s t := by
  induction p with
  | previous q => exact .previous (doubleCompositeCriticalPeak_fill q)
  | mixedResidue w => exact .mixedResidue w
  | mixedDouble w => exact mixedResidueDouble_fill w
  | mixedUnitDiamond w => exact mixedResidueUnit_fill w
  | reverse q ih => exact .reverse ih
  | chain q q' ih ih' => exact .chain ih ih'
  | whiskerLeft before q ih => exact .whiskerLeft before ih
  | whiskerRight q after ih => exact .whiskerRight ih after
  | inverseContext q ih => exact .inverseContext ih
  | compositeContext q q' ih ih' => exact .compositeContext ih ih'

theorem mixedResidueCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedResidueCriticalPeak W long short s t) :
    Nonempty (MixedResidueEightCell W long short s t) :=
  ⟨mixedResidueCriticalPeak_fill p⟩

theorem mixedResidueCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedResidueCriticalPeak W long short s t) :
    mixedResidueHistoryClass s = mixedResidueHistoryClass t :=
  (mixedResidueHistoryClass_eq_iff s t).2 (mixedResidueCriticalPeak_joinable p)

end PentagonAdjoinedSixCell

section ActualOriginalP77MixedResidueCompletion
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

/-- For EVERY actual original P77 final raw index the same genuine
v5.06 GK5CG-source-bearing mixed-residue pair is NEWLY comparable,
OLD non-comparable, with all old T/J/K and two R/U parities equal;
the source strict Eq interpreter remains proven impossible. -/
theorem pentagonActualMixedResidueCompletionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.MixedResidueEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst c)
        (PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.DoubleCompositeEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst c)
        (PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond c)) ∧
      PentagonAdjoinedSixCell.sevenChargeTriple
          (PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst c) =
        PentagonAdjoinedSixCell.sevenChargeTriple
          (PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond c) ∧
      PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst c) =
        PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond c) ∧
      PentagonAdjoinedSixCell.sevenUnitCountParity
          (PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst c) =
        PentagonAdjoinedSixCell.sevenUnitCountParity
          (PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond c) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.mixedResidueSource_fill _⟩,
    PentagonAdjoinedSixCell.sevenMixedResidueComposite_noDoubleCompositeComparison _,
    (PentagonAdjoinedSixCell.sevenMixedResidueComposite_values _).1,
    (PentagonAdjoinedSixCell.sevenMixedResidueComposite_values _).2.1,
    (PentagonAdjoinedSixCell.sevenMixedResidueComposite_values _).2.2.1,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.MixedResidueEightCell
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_refl
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_preservesParity
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_preservesUnitCountParity
#print axioms PentagonAdjoinedSixCell.sevenTotalReductionParity
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_vParityValues
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_preservesVParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistorySetoid
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_descendsToMixedResidue
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noPreviousReturn
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noStrictReturn
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noVFourDescent
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryVParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryUnitParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryVParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryUnitParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedResidueSource_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueSource_strictComparison
#print axioms PentagonAdjoinedSixCell.mixedResidue_withPrevious_noOld
#print axioms PentagonAdjoinedSixCell.mixedResidueDoubleFirst
#print axioms PentagonAdjoinedSixCell.mixedResidueDoubleSecond
#print axioms PentagonAdjoinedSixCell.mixedResidueDouble_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueDouble_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedResidueUnitFirst
#print axioms PentagonAdjoinedSixCell.mixedResidueUnitSecond
#print axioms PentagonAdjoinedSixCell.mixedResidueUnit_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueUnit_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedResidueDouble_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedResidueUnit_newVsOld
#print axioms PentagonAdjoinedSixCell.MixedResidueCriticalPeak
#print axioms PentagonAdjoinedSixCell.mixedResidueCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.mixedResidueCriticalPeak_classEq
#print axioms pentagonActualMixedResidueCompletionWithSourceObstruction

end ActualOriginalP77MixedResidueCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
