import KUOS.Architecture.QiWuxingGK5CHP77BalancedInverseUnitCountObstructionV5_02

/-!
Qi v5.03 — MINIMAL BALANCED-UNIT HIGHER COMPLETION.

Qi v5.02 proved a genuinely typed three-factor pair of parallel
original seventh-level histories with the SAME old (T,J,K) charges
and old R mod-2 parity but unit-step counts U=1 and U=3.
It proved NO comparison exists in the full v5.01 UnitDiamondEightCell
grammar by induction over every old eighth-cell constructor.

We first transport THIS STRONG three-charge/parity-invisible pair to
every actual original P77 final raw source index, retaining the
unchanged GK5CG five-cell Type and its strict equality no-go.

We then add exactly ONE new comparison family, balancedUnit(w), in
a SEPARATE BalancedUnitEightCell presentation, leaving all old Type
signatures, original source words, old eighth-level grammars, old
quotients and evidence histories untouched. All old UnitDiamondEightCell
comparisons inject by previous. The new chosen quotient is STRICTLY
coarser: old U cannot descend, while U modulo 2 and the old R parity
still descend by all-constructor induction and Quotient.lift.

Explicit new/old typed comparisons for the source-contextual strong
pair and two genuine mixed peaks (balancedUnit × identityDouble,
balancedUnit × unitDiamond) use ONLY the one new primitive and already
available old higher witnesses. A restricted mixed critical family is
filled by structural induction; no arbitrary parallel-seven-history
comparison, global thinness or ninth cell is asserted.

Append-only / tighten-only / overwrite-forbidden / same-root;
public proof roots 107. Validation PR #1558 remains Draft/OPEN.
Pinned Lean v4.30.0-rc2 / mathlib
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

/-- The SAME old strong v5.02 obstruction, now horizontally pasted
with any actual original P77/GK5CG six-cell source value c. -/
def sevenBalancedStrongSourceFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans
        (balancedUnitInvisibleSource (long := long) (short := short) w) c)
      (.trans
        (balancedUnitInvisibleTarget (long := long) (short := short) w) c) :=
  .congrComp (sevenBalancedUnitInvisibleFirst w) (.refl c)

def sevenBalancedStrongSourceSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans
        (balancedUnitInvisibleSource (long := long) (short := short) w) c)
      (.trans
        (balancedUnitInvisibleTarget (long := long) (short := short) w) c) :=
  .congrComp (sevenBalancedUnitInvisibleSecond w) (.refl c)

/-- Unlike the earlier TWO-factor P77 transfer, this is the genuine
THREE-factor source-contextual pair, carrying BOTH the original
three-charge and fourth R-parity equalities and the U=1/3 gap. -/
theorem sevenBalancedStrongSource_values {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenChargeTriple (sevenBalancedStrongSourceFirst c) =
        sevenChargeTriple (sevenBalancedStrongSourceSecond c) ∧
    sevenIdentityParity (sevenBalancedStrongSourceFirst c) =
        sevenIdentityParity (sevenBalancedStrongSourceSecond c) ∧
    (sevenUnitStepCharge (sevenBalancedStrongSourceFirst c) = 1 ∧
     sevenUnitStepCharge (sevenBalancedStrongSourceSecond c) = 3) := by
  constructor
  · simpa [sevenBalancedStrongSourceFirst, sevenBalancedStrongSourceSecond,
      sevenChargeTriple, sevenTriangleCharge, sevenInvolutionCharge,
      sevenInverseCompCharge] using
        (sevenBalancedUnitInvisible_sameTriple
          (long := long) (short := short) w)
  constructor
  · simpa [sevenBalancedStrongSourceFirst, sevenBalancedStrongSourceSecond,
      sevenIdentityParity, sevenIdentityBalance] using
        (sevenBalancedUnitInvisible_sameParity
          (long := long) (short := short) w)
  · constructor <;>
      norm_num [sevenBalancedStrongSourceFirst,
        sevenBalancedStrongSourceSecond, sevenUnitStepCharge,
        (sevenBalancedUnitInvisible_unitValues
          (long := long) (short := short) w).1,
        (sevenBalancedUnitInvisible_unitValues
          (long := long) (short := short) w).2]

/-- U conservation of EVERY old v5.01 higher comparison rules out
comparison even after transport along an authentic source six-cell. -/
theorem sevenBalancedStrongSource_noPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (UnitDiamondEightCell W long short
      (sevenBalancedStrongSourceFirst c)
      (sevenBalancedStrongSourceSecond c)) := by
  rintro ⟨q⟩
  have h := unitDiamondEightCell_preservesUnitStepCharge q
  have vals := (sevenBalancedStrongSource_values c).2.2
  rw [vals.1, vals.2] at h
  norm_num at h

/-- New, independent selected higher presentation. The ONLY new
primitive is balancedUnit; all old source-typed comparison values
are included without identifying raw seventh history syntax. -/
inductive BalancedUnitEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondEightCell W l r s t) :
      BalancedUnitEightCell W l r s t
  | balancedUnit (w : W) :
      BalancedUnitEightCell W l r
        (sevenBalancedUnitInvisibleFirst (long := l) (short := r) w)
        (sevenBalancedUnitInvisibleSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitEightCell W l r s t) :
      BalancedUnitEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : BalancedUnitEightCell W l r s t)
      (q' : BalancedUnitEightCell W l r t u) :
      BalancedUnitEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : BalancedUnitEightCell W l r s t) :
      BalancedUnitEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      BalancedUnitEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitEightCell W l r s t) :
      BalancedUnitEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : BalancedUnitEightCell W l r s s')
      (q' : BalancedUnitEightCell W l r t t') :
      BalancedUnitEightCell W l r
        (.congrComp s t) (.congrComp s' t')

/-- Every old proof survives unchanged, as a genuinely typed value. -/
def balancedUnitEightCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : UnitDiamondEightCell W long short s t) :
    BalancedUnitEightCell W long short s t :=
  .previous q

def balancedUnitEightCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    BalancedUnitEightCell W long short s s :=
  .previous (unitDiamondEightCell_refl s)

/-- Only the single v5.02 CERTIFIED pair is made comparable. -/
theorem balancedUnitEightCell_strictlyNew (w : W) :
    Nonempty (BalancedUnitEightCell W long short
      (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w)
      (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (UnitDiamondEightCell W long short
      (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w)
      (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w)) :=
  ⟨⟨.balancedUnit w⟩,
    sevenBalancedUnitInvisible_noComparison (long := long) (short := short) w⟩

theorem balancedUnitEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      BalancedUnitEightCell W l r s t →
        UnitDiamondEightCell W l r s t) := by
  rintro ⟨interpret⟩
  have q : UnitDiamondEightCell W l r
      (sevenBalancedUnitInvisibleFirst (long := l) (short := r) l)
      (sevenBalancedUnitInvisibleSecond (long := l) (short := r) l) :=
    interpret _ _ (.balancedUnit l)
  exact sevenBalancedUnitInvisible_noComparison (long := l) (short := r) l ⟨q⟩

theorem balancedUnitEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      BalancedUnitEightCell W l r s t → s = t) := by
  intro interpret
  apply unitDiamondEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t (.previous q)

/-- The fourth R mod-two observer survives ALL new higher
constructors, not just the new primitive comparison. -/
theorem balancedUnitEightCell_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : BalancedUnitEightCell W long short s t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  induction q with
  | previous q => exact unitDiamondEightCell_preservesParity q
  | balancedUnit w => exact sevenBalancedUnitInvisible_sameParity w
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

/-- The old integer U is destroyed by the new comparison, but its
residue mod 2 survives the EXACT new jump U=1 against U=3. -/
def sevenUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  sevenUnitStepCharge s % 2

theorem balancedUnitEightCell_preservesUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : BalancedUnitEightCell W long short s t) :
    sevenUnitCountParity s = sevenUnitCountParity t := by
  induction q with
  | previous q =>
      exact congrArg (fun n : ℤ => n % 2)
        (unitDiamondEightCell_preservesUnitStepCharge q)
  | balancedUnit w =>
      have vals := sevenBalancedUnitInvisible_unitValues
        (long := long) (short := short) w
      norm_num [sevenUnitCountParity, vals.1, vals.2]
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

/-- Chosen, separate v5.03 history quotient; old v5.01 quotient
and every higher raw Type retain their original definitions. -/
def balancedUnitHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (BalancedUnitEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨balancedUnitEightCell_refl s⟩
    · intro s t h
      rcases h with ⟨q⟩
      exact ⟨.reverse q⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def balancedUnitHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (balancedUnitHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem balancedUnitHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    balancedUnitHistoryClass s = balancedUnitHistoryClass t ↔
      Nonempty (BalancedUnitEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem unitDiamondHistoryClass_descendsToBalanced {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : unitDiamondHistoryClass s = unitDiamondHistoryClass t) :
    balancedUnitHistoryClass s = balancedUnitHistoryClass t := by
  rcases (unitDiamondHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (balancedUnitHistoryClass_eq_iff s t).2 ⟨.previous q⟩

theorem balancedUnitHistoryClass_strictlyNew (w : W) :
    (balancedUnitHistoryClass
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) =
      balancedUnitHistoryClass
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w)) ∧
    (unitDiamondHistoryClass
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) ≠
      unitDiamondHistoryClass
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w)) :=
  ⟨(balancedUnitHistoryClass_eq_iff _ _).2 ⟨.balancedUnit w⟩,
    sevenBalancedUnitInvisible_distinctClasses (long := long) (short := short) w⟩

theorem balancedUnitHistoryClass_noPreviousReturn (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      balancedUnitHistoryClass s = balancedUnitHistoryClass t →
        unitDiamondHistoryClass s = unitDiamondHistoryClass t) := by
  intro interpret
  have witness := (balancedUnitHistoryClass_strictlyNew
    (long := l) (short := r) l)
  exact witness.2 (interpret
    (sevenBalancedUnitInvisibleFirst (long := l) (short := r) l)
    (sevenBalancedUnitInvisibleSecond (long := l) (short := r) l) witness.1)

theorem balancedUnitHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      balancedUnitHistoryClass s = balancedUnitHistoryClass t → s = t) := by
  intro interpret
  apply balancedUnitEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((balancedUnitHistoryClass_eq_iff s t).2 ⟨q⟩)

/-- Integer U itself no longer descends: the new primitive relates
the old genuinely different classes with U=1 versus U=3. -/
theorem balancedUnitHistoryClass_noIntegerUnitDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      balancedUnitHistoryClass s = balancedUnitHistoryClass t →
        sevenUnitStepCharge s = sevenUnitStepCharge t) := by
  intro preserve
  have heq := (balancedUnitHistoryClass_strictlyNew
    (long := l) (short := r) l).1
  have h := preserve
    (sevenBalancedUnitInvisibleFirst (long := l) (short := r) l)
    (sevenBalancedUnitInvisibleSecond (long := l) (short := r) l) heq
  have vals := sevenBalancedUnitInvisible_unitValues (long := l) (short := r) l
  rw [vals.1, vals.2] at h
  norm_num at h

def balancedUnitHistoryParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (balancedUnitHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenIdentityParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (balancedUnitEightCell_preservesParity q))

def balancedUnitHistoryUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (balancedUnitHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenUnitCountParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (balancedUnitEightCell_preservesUnitCountParity q))

theorem balancedUnitHistoryParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    balancedUnitHistoryParity
      (balancedUnitHistoryClass (long := long) (short := short) s) =
        decide (sevenIdentityParity s = 1) :=
  rfl

theorem balancedUnitHistoryUnitCountParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    balancedUnitHistoryUnitCountParity
      (balancedUnitHistoryClass (long := long) (short := short) s) =
        decide (sevenUnitCountParity s = 1) :=
  rfl

/-- The strong v5.02 witness is transported with the SAME genuine
original six-cell c, without requiring source Eq or new syntax. -/
def balancedUnitSource_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    BalancedUnitEightCell W long short
      (sevenBalancedStrongSourceFirst c)
      (sevenBalancedStrongSourceSecond c) :=
  .compositeContext (.balancedUnit w)
    (balancedUnitEightCell_refl (.refl c))

theorem balancedUnitSource_strictComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (BalancedUnitEightCell W long short
      (sevenBalancedStrongSourceFirst c)
      (sevenBalancedStrongSourceSecond c)) ∧
    ¬ Nonempty (UnitDiamondEightCell W long short
      (sevenBalancedStrongSourceFirst c)
      (sevenBalancedStrongSourceSecond c)) ∧
    sevenChargeTriple (sevenBalancedStrongSourceFirst c) =
      sevenChargeTriple (sevenBalancedStrongSourceSecond c) ∧
    sevenIdentityParity (sevenBalancedStrongSourceFirst c) =
      sevenIdentityParity (sevenBalancedStrongSourceSecond c) :=
  ⟨⟨balancedUnitSource_fill c⟩,
    sevenBalancedStrongSource_noPrevious c,
    (sevenBalancedStrongSource_values c).1,
    (sevenBalancedStrongSource_values c).2.1⟩

/-- First mixed critical pair: the new balancedUnit and the OLD
genuine identityDouble comparison in one typed composite context. -/
def mixedBalancedIdentityFirst (w : W) :
    SevenRewrite W long short
      (.trans (balancedUnitInvisibleSource (long := long) (short := short) w)
        (.symm (.symm (.refl w))))
      (.trans (balancedUnitInvisibleTarget (long := long) (short := short) w)
        (.refl w)) :=
  .congrComp (sevenBalancedUnitInvisibleFirst w) (sevenIdentityDoubleDirect w)

def mixedBalancedIdentitySecond (w : W) :
    SevenRewrite W long short
      (.trans (balancedUnitInvisibleSource (long := long) (short := short) w)
        (.symm (.symm (.refl w))))
      (.trans (balancedUnitInvisibleTarget (long := long) (short := short) w)
        (.refl w)) :=
  .congrComp (sevenBalancedUnitInvisibleSecond w) (sevenIdentityDoubleVia w)

def mixedBalancedIdentity_fill (w : W) :
    BalancedUnitEightCell W long short
      (mixedBalancedIdentityFirst (long := long) (short := short) w)
      (mixedBalancedIdentitySecond (long := long) (short := short) w) :=
  .compositeContext (.balancedUnit w)
    (.previous (.previous (.identityDouble w)))

theorem mixedBalancedIdentity_noPrevious (w : W) :
    ¬ Nonempty (UnitDiamondEightCell W long short
      (mixedBalancedIdentityFirst (long := long) (short := short) w)
      (mixedBalancedIdentitySecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := unitDiamondEightCell_preservesUnitStepCharge q
  have vals := sevenBalancedUnitInvisible_unitValues
    (long := long) (short := short) w
  norm_num [mixedBalancedIdentityFirst, mixedBalancedIdentitySecond,
    sevenUnitStepCharge, sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
    vals.1, vals.2] at h

/-- Second mixed critical pair: new balancedUnit against the v5.01
unitDiamond witness, with all raw six-cell endpoints retained. -/
def mixedBalancedUnitDiamondFirst (w : W) :
    SevenRewrite W long short
      (.trans (balancedUnitInvisibleSource (long := long) (short := short) w)
        (.trans (.refl w) (.refl w)))
      (.trans (balancedUnitInvisibleTarget (long := long) (short := short) w)
        (.refl w)) :=
  .congrComp (sevenBalancedUnitInvisibleFirst w) (sevenUnitDiamondLeft w)

def mixedBalancedUnitDiamondSecond (w : W) :
    SevenRewrite W long short
      (.trans (balancedUnitInvisibleSource (long := long) (short := short) w)
        (.trans (.refl w) (.refl w)))
      (.trans (balancedUnitInvisibleTarget (long := long) (short := short) w)
        (.refl w)) :=
  .congrComp (sevenBalancedUnitInvisibleSecond w) (sevenUnitDiamondRight w)

def mixedBalancedUnitDiamond_fill (w : W) :
    BalancedUnitEightCell W long short
      (mixedBalancedUnitDiamondFirst (long := long) (short := short) w)
      (mixedBalancedUnitDiamondSecond (long := long) (short := short) w) :=
  .compositeContext (.balancedUnit w) (.previous (.unitDiamond w))

theorem mixedBalancedUnitDiamond_noPrevious (w : W) :
    ¬ Nonempty (UnitDiamondEightCell W long short
      (mixedBalancedUnitDiamondFirst (long := long) (short := short) w)
      (mixedBalancedUnitDiamondSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := unitDiamondEightCell_preservesUnitStepCharge q
  have vals := sevenBalancedUnitInvisible_unitValues
    (long := long) (short := short) w
  norm_num [mixedBalancedUnitDiamondFirst, mixedBalancedUnitDiamondSecond,
    sevenUnitDiamondLeft, sevenUnitDiamondRight, sevenUnitStepCharge,
    vals.1, vals.2] at h

/-- The exact selected critical family is restricted: old v5.01
coherence, one genuine new primitive and two actually sourced mixed
peaks, together with explicitly typed contexts. No universal
all-parallel-comparison axiom or constructor. -/
inductive BalancedUnitCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondCriticalPeak W l r s t) :
      BalancedUnitCriticalPeak W l r s t
  | balancedUnit (w : W) :
      BalancedUnitCriticalPeak W l r
        (sevenBalancedUnitInvisibleFirst (long := l) (short := r) w)
        (sevenBalancedUnitInvisibleSecond (long := l) (short := r) w)
  | mixedIdentity (w : W) :
      BalancedUnitCriticalPeak W l r
        (mixedBalancedIdentityFirst (long := l) (short := r) w)
        (mixedBalancedIdentitySecond (long := l) (short := r) w)
  | mixedUnitDiamond (w : W) :
      BalancedUnitCriticalPeak W l r
        (mixedBalancedUnitDiamondFirst (long := l) (short := r) w)
        (mixedBalancedUnitDiamondSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitCriticalPeak W l r s t) :
      BalancedUnitCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : BalancedUnitCriticalPeak W l r s t)
      (q' : BalancedUnitCriticalPeak W l r t u) :
      BalancedUnitCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : BalancedUnitCriticalPeak W l r s t) :
      BalancedUnitCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      BalancedUnitCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : BalancedUnitCriticalPeak W l r s t) :
      BalancedUnitCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : BalancedUnitCriticalPeak W l r s s')
      (q' : BalancedUnitCriticalPeak W l r t t') :
      BalancedUnitCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

def balancedUnitCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : BalancedUnitCriticalPeak W long short s t) :
    BalancedUnitEightCell W long short s t := by
  induction p with
  | previous q => exact .previous (unitDiamondCriticalPeak_fill q)
  | balancedUnit w => exact .balancedUnit w
  | mixedIdentity w => exact mixedBalancedIdentity_fill w
  | mixedUnitDiamond w => exact mixedBalancedUnitDiamond_fill w
  | reverse q ih => exact .reverse ih
  | chain q q' ih ih' => exact .chain ih ih'
  | whiskerLeft before q ih => exact .whiskerLeft before ih
  | whiskerRight q after ih => exact .whiskerRight ih after
  | inverseContext q ih => exact .inverseContext ih
  | compositeContext q q' ih ih' => exact .compositeContext ih ih'

theorem balancedUnitCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : BalancedUnitCriticalPeak W long short s t) :
    Nonempty (BalancedUnitEightCell W long short s t) :=
  ⟨balancedUnitCriticalPeak_fill p⟩

theorem balancedUnitCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : BalancedUnitCriticalPeak W long short s t) :
    balancedUnitHistoryClass s = balancedUnitHistoryClass t :=
  (balancedUnitHistoryClass_eq_iff s t).2 (balancedUnitCriticalPeak_joinable p)

end PentagonAdjoinedSixCell

section ActualOriginalP77BalancedUnitCompletion
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

/-- At EVERY genuine original P77 final raw index: the strong
three-charge AND R-parity invisible v5.02 pair, with source-carrying
GK5CG Type evidence, is now comparable in the NEW selected independent
presentation, NOT comparable in v5.01, and has no source strict Eq
interpreter. No source equality or arbitrary higher thinness is added. -/
theorem pentagonActualStrongBalancedUnitCompletionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.BalancedUnitEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenBalancedStrongSourceFirst c)
        (PentagonAdjoinedSixCell.sevenBalancedStrongSourceSecond c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.UnitDiamondEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenBalancedStrongSourceFirst c)
        (PentagonAdjoinedSixCell.sevenBalancedStrongSourceSecond c)) ∧
      PentagonAdjoinedSixCell.sevenChargeTriple
          (PentagonAdjoinedSixCell.sevenBalancedStrongSourceFirst c) =
        PentagonAdjoinedSixCell.sevenChargeTriple
          (PentagonAdjoinedSixCell.sevenBalancedStrongSourceSecond c) ∧
      PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenBalancedStrongSourceFirst c) =
        PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenBalancedStrongSourceSecond c) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.balancedUnitSource_fill _⟩,
    PentagonAdjoinedSixCell.sevenBalancedStrongSource_noPrevious _,
    (PentagonAdjoinedSixCell.sevenBalancedStrongSource_values _).1,
    (PentagonAdjoinedSixCell.sevenBalancedStrongSource_values _).2.1,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sevenBalancedStrongSourceFirst
#print axioms PentagonAdjoinedSixCell.sevenBalancedStrongSourceSecond
#print axioms PentagonAdjoinedSixCell.sevenBalancedStrongSource_values
#print axioms PentagonAdjoinedSixCell.sevenBalancedStrongSource_noPrevious
#print axioms PentagonAdjoinedSixCell.BalancedUnitEightCell
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_refl
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_preservesParity
#print axioms PentagonAdjoinedSixCell.sevenUnitCountParity
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_preservesUnitCountParity
#print axioms PentagonAdjoinedSixCell.balancedUnitHistorySetoid
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_descendsToBalanced
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass_noPreviousReturn
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass_noStrictReturn
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryClass_noIntegerUnitDescent
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryParity
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryUnitCountParity
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryParity_onClass
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryUnitCountParity_onClass
#print axioms PentagonAdjoinedSixCell.balancedUnitSource_fill
#print axioms PentagonAdjoinedSixCell.balancedUnitSource_strictComparison
#print axioms PentagonAdjoinedSixCell.mixedBalancedIdentityFirst
#print axioms PentagonAdjoinedSixCell.mixedBalancedIdentitySecond
#print axioms PentagonAdjoinedSixCell.mixedBalancedIdentity_fill
#print axioms PentagonAdjoinedSixCell.mixedBalancedIdentity_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedBalancedUnitDiamondFirst
#print axioms PentagonAdjoinedSixCell.mixedBalancedUnitDiamondSecond
#print axioms PentagonAdjoinedSixCell.mixedBalancedUnitDiamond_fill
#print axioms PentagonAdjoinedSixCell.mixedBalancedUnitDiamond_noPrevious
#print axioms PentagonAdjoinedSixCell.BalancedUnitCriticalPeak
#print axioms PentagonAdjoinedSixCell.balancedUnitCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.balancedUnitCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.balancedUnitCriticalPeak_classEq
#print axioms pentagonActualStrongBalancedUnitCompletionWithSourceObstruction

end ActualOriginalP77BalancedUnitCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
