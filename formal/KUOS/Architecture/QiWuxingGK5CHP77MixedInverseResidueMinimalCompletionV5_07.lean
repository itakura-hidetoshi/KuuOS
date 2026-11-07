import KUOS.Architecture.QiWuxingGK5CHP77MixedInverseCompResidueObstructionV5_06

/-!
Qi v5.07 — MINIMAL MIXED INVERSE-COMPOSITE RESIDUE COMPLETION.

Qi v5.06 constructed two genuine three-factor original SevenRewrite
histories with identical original six-cell raw endpoints, old
(T,J,K)=(2,0,1) on both paths, R mod2=0 and U mod2=1 on both,
but original V=3 versus V=5 (and V mod4=3 versus V mod4=1).
The COMPLETE previous DoubleCompositeEightCell grammar conserves
V modulo FOUR, so the comparison is mathematically impossible in
that former independent presentation; this was formalized and
transferred to all actual P77/GK5CG final raw indices.

The present independent MixedResidueEightCell Type adds exactly ONE
new comparison family, mixedResidue(w), whose genuine endpoints are
those already certified by Qi v5.06. All earlier DoubleCompositeEightCell
comparison evidence survives via previous; only reverse, chain,
whisker and typed inverse/composition contexts close the grammar.
No existing raw six-cell, seventh history, old eighth presentation,
old quotient, strict source value or original evidence is replaced.

The newly chosen quotient is STRICTLY coarser: the old V modulo FOUR
cannot descend (3 versus 1), nor can the unreduced integer V (3 versus
5). Yet V mod TWO and the prior R/U parities are preserved by ALL
new typed comparison constructors and descend through Quotient.lift.
The R/U parity coupling on fixed original six-cell endpoints remains.

We exhibit two genuine mixed overlaps, mixedResidue × doubleComposite
and mixedResidue × balancedUnit, and fill a restricted critical family
via full constructor induction. The old grammar cannot compare either
mixed overlap by the certified V-mod-four invariant; the new grammar
fills both by its ONE new primitive and existing typed comparisons.

At EACH original P77 terminal raw index, the authentic source
GK5CG six-cell generator transports the SAME strong source-specific
comparison and preserves ¬ original strict EqualityInterpreter.
No global thinness, arbitrary parallel-history completeness,
ninth cell, or source strict Eq promotion is assumed.

Append-only / tighten-only / overwrite-forbidden / same-root;
public proof roots 107; protected validation-only #1558 stays Draft/open.
Lean v4.30.0-rc2; mathlib
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

/-- A completely separate higher presentation. Its ONLY NEW
elementary comparison is the actual v5.06 three-factor witness.
All former comparison witnesses retain their original source types. -/
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

/-- The old no-comparison theorem certifies that this is a GENUINELY
new comparison, not a syntactic alias for an existing eighth cell. -/
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

/-- Prior R mod-two parity is preserved by the single new comparison,
the full previous grammar and every new typed context. -/
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

/-- The former V modulo FOUR does NOT descend, but V modulo TWO is
invariant across the certified V=3 and V=5 original source histories. -/
def sevenTotalReductionParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  sevenTotalReductionCharge s % 2

theorem sevenMixedResidue_totalParityValues (w : W) :
    sevenTotalReductionParity
        (sevenMixedResidueFirst (long := long) (short := short) w) = 1 ∧
    sevenTotalReductionParity
        (sevenMixedResidueSecond (long := long) (short := short) w) = 1 := by
  have vals := sevenMixedResidue_totalValues (long := long) (short := short) w
  constructor <;> norm_num [sevenTotalReductionParity, vals.1, vals.2]

theorem mixedResidueEightCell_preservesTotalReductionParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    sevenTotalReductionParity s = sevenTotalReductionParity t := by
  induction q with
  | previous q =>
      have h := doubleCompositeEightCell_preservesTotalReductionResidue q
      simp only [sevenTotalReductionResidue] at h
      simp only [sevenTotalReductionParity]
      omega
  | mixedResidue w =>
      exact (sevenMixedResidue_totalParityValues
        (long := long) (short := short) w).1.trans
        (sevenMixedResidue_totalParityValues
          (long := long) (short := short) w).2.symm
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenTotalReductionParity] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | whiskerRight q after ih =>
      simp only [sevenTotalReductionParity] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | inverseContext q ih =>
      simpa [sevenTotalReductionParity, sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenTotalReductionParity] at ih ih' ⊢
      simp only [sevenTotalReductionCharge]
      omega

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
  have witness := mixedResidueHistoryClass_strictlyNew (long := l) (short := r) l
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

/-- The old V mod FOUR is no longer representative-independent in the
new selected quotient because the genuine new comparison relates 3/1. -/
theorem mixedResidueHistoryClass_noV4Descent (l r : W) :
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

def mixedResidueHistoryV2 {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenTotalReductionParity s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact mixedResidueEightCell_preservesTotalReductionParity q)

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

def mixedResidueHistoryUnitCountParity {w z : W}
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

theorem mixedResidueHistoryV2_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryV2
      (mixedResidueHistoryClass (long := long) (short := short) s) =
      sevenTotalReductionParity s :=
  rfl

theorem mixedResidueHistoryParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryParity
      (mixedResidueHistoryClass (long := long) (short := short) s) =
      decide (sevenIdentityParity s = 1) :=
  rfl

theorem mixedResidueHistoryUnitCountParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryUnitCountParity
      (mixedResidueHistoryClass (long := long) (short := short) s) =
      decide (sevenUnitCountParity s = 1) :=
  rfl

/-- Mixed v5.06 source-pasted comparison, retaining the SAME original
six-cell c and its unquotiented old type evidence on each side. -/
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

/-- First mixed critical pair: the one new mixed-residue comparison
whiskered against an existing DoubleCompositeEightCell primitive. -/
def mixedResidueDoubleFirst (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w)))
      (.trans (mixedResidueTarget (long := long) (short := short) w)
        (.trans (.refl w) (.refl w))) :=
  .congrComp (sevenMixedResidueFirst w) (sevenDoubleCompositeCancelFirst w)

def mixedResidueDoubleSecond (w : W) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w)
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
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
  rintro ⟨q⟩
  have h := doubleCompositeEightCell_preservesTotalReductionResidue q
  have mv := sevenMixedResidue_totalValues (long := long) (short := short) w
  have dv := sevenDoubleCompositeCancel_values (long := long) (short := short) w
  norm_num [mixedResidueDoubleFirst, mixedResidueDoubleSecond,
    sevenTotalReductionResidue, sevenTotalReductionCharge,
    mv.1, mv.2, dv.1, dv.2.1] at h

/-- Second mixed critical pair against the v5.03 balanced-unit
primitive, embedded through TWO independent old presentations. -/
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
  rintro ⟨q⟩
  have h := doubleCompositeEightCell_preservesTotalReductionResidue q
  have mv := sevenMixedResidue_totalValues (long := long) (short := short) w
  have bv := sevenBalancedUnitInvisible_totalValues
    (long := long) (short := short) w
  norm_num [mixedResidueBalancedFirst, mixedResidueBalancedSecond,
    sevenTotalReductionResidue, sevenTotalReductionCharge,
    mv.1, mv.2, bv.1, bv.2] at h

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
    mixedResidueEightCell_preservesTotalReductionParity (mixedResidueDouble_fill w)⟩

theorem mixedResidueBalanced_newVsOld (w : W) :
    Nonempty (MixedResidueEightCell W long short
      (mixedResidueBalancedFirst (long := long) (short := short) w)
      (mixedResidueBalancedSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (mixedResidueBalancedFirst (long := long) (short := short) w)
      (mixedResidueBalancedSecond (long := long) (short := short) w)) ∧
    sevenTotalReductionParity (mixedResidueBalancedFirst w) =
      sevenTotalReductionParity (mixedResidueBalancedSecond w) :=
  ⟨⟨mixedResidueBalanced_fill w⟩,
    mixedResidueBalanced_noPrevious w,
    mixedResidueEightCell_preservesTotalReductionParity (mixedResidueBalanced_fill w)⟩

/-- A SELECTED original typed critical family, NOT a completeness axiom. -/
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
  | mixedBalanced (w : W) :
      MixedResidueCriticalPeak W l r
        (mixedResidueBalancedFirst (long := l) (short := r) w)
        (mixedResidueBalancedSecond (long := l) (short := r) w)
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
  | mixedBalanced w => exact mixedResidueBalanced_fill w
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

/-- At EVERY real original P77 terminal raw index: the source-carrying
strong three-factor Qi v5.06 history is now comparable in the NEW
selected higher Type but NOT in the old one. Old T/J/K, residual
R and U parity agree, and the original source strict Eq no-go remains. -/
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
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_totalParityValues
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_preservesTotalReductionParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistorySetoid
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.doubleCompositeHistoryClass_descendsToMixedResidue
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noPreviousReturn
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noStrictReturn
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noV4Descent
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_noIntegerVDescent
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryV2
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryUnitCountParity
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryV2_onClass
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryUnitCountParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedResidueSource_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueSource_strictComparison
#print axioms PentagonAdjoinedSixCell.mixedResidueDoubleFirst
#print axioms PentagonAdjoinedSixCell.mixedResidueDoubleSecond
#print axioms PentagonAdjoinedSixCell.mixedResidueDouble_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueDouble_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedResidueBalancedFirst
#print axioms PentagonAdjoinedSixCell.mixedResidueBalancedSecond
#print axioms PentagonAdjoinedSixCell.mixedResidueBalanced_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueBalanced_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedResidueDouble_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedResidueBalanced_newVsOld
#print axioms PentagonAdjoinedSixCell.MixedResidueCriticalPeak
#print axioms PentagonAdjoinedSixCell.mixedResidueCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.mixedResidueCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.mixedResidueCriticalPeak_classEq
#print axioms pentagonActualMixedResidueCompletionWithSourceObstruction

end ActualOriginalP77MixedResidueCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
