import KUOS.Architecture.QiWuxingGK5CHP77UnitDiamondFourTorsionObstructionV5_00

/-!
Qi v5.01 — MINIMAL UNIT-DIAMOND HIGHER COMPLETION.

The v5.00 theorem proves a genuine obstruction for the ORIGINAL
v4.98 IdentityEightCell comparison grammar: the two freely generated
leftUnit(refl(w)) and rightUnit(refl(w)) seven-cell histories have
identical raw six-cell boundaries and v4.99 R-parity, but different
Z/4 torsion values and NO old eighth-level comparison.

We adjoin precisely ONE primitive comparison family, unitDiamond,
to a NEW SEPARATE UnitDiamondEightCell presentation. Every old
IdentityEightCell proof is retained by the explicit previous injection;
all old Type-valued source, identities and quotient classes are intact.
The new grammar has only reflexive/symmetric/transitive/congruence
closure, as supplied by the unchanged typed constructor scheme.

The chosen quotient is STRICTLY coarser. Its v5.00 Z/4 observer fails
descent (witness 0 versus 2), while the original v4.99 R mod 2 Bool
observer STILL descends by induction over every constructor.

Three genuine, type-indexed mixed unit diamonds (identityDouble,
left inverseComp/unit and left involution/cancellation) are filled by
OLD comparison witnesses pasted with the one NEW unitDiamond.
Each remains nonjoinable in the prior IdentityEightCell grammar by
the v5.00 Z/4 invariant. A restricted critical family admits explicit
comparison witnesses by constructor induction. No universal
all-parallel-history completeness, ninth-cell or thinness is asserted.

Transport to EACH actual original P77 terminal raw index reuses the
true GK5CG five-cell source and retains its strict source Eq no-go.
Append-only/tighten-only/overwrite-forbidden/same-root, root107.
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

/-- A new independent eighth-level Type, including ALL old chosen
v4.98 comparisons and precisely one new unit unit-diamond generator,
together with the same typed congruence/equivalence contexts.
The older IdentityEightCell definition is not modified. -/
inductive UnitDiamondEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityEightCell W l r s t) :
      UnitDiamondEightCell W l r s t
  | unitDiamond (w : W) :
      UnitDiamondEightCell W l r
        (sevenUnitDiamondLeft (long := l) (short := r) w)
        (sevenUnitDiamondRight (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondEightCell W l r s t) :
      UnitDiamondEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : UnitDiamondEightCell W l r s t)
      (q' : UnitDiamondEightCell W l r t u) :
      UnitDiamondEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : UnitDiamondEightCell W l r s t) :
      UnitDiamondEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      UnitDiamondEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondEightCell W l r s t) :
      UnitDiamondEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : UnitDiamondEightCell W l r s s')
      (q' : UnitDiamondEightCell W l r t t') :
      UnitDiamondEightCell W l r
        (.congrComp s t) (.congrComp s' t')

/-- Fully typed identity certificate from original eighth-level
reflexivity, through all intermediate independent presentations. -/
def unitDiamondEightCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    UnitDiamondEightCell W long short s s :=
  .previous (.previous (.previous (.previous (.original (.reflexive s)))))

/-- The old v4.98 grammar injects without coercing any source value. -/
def unitDiamondEightCell_ofIdentity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    UnitDiamondEightCell W long short s t :=
  .previous q

/-- Minimality is certified by the actual Z/4 impossibility from v5.00. -/
theorem unitDiamondEightCell_strictlyNew (w : W) :
    Nonempty (UnitDiamondEightCell W long short
      (sevenUnitDiamondLeft (long := long) (short := short) w)
      (sevenUnitDiamondRight (long := long) (short := short) w)) ∧
    ¬ Nonempty (IdentityEightCell W long short
      (sevenUnitDiamondLeft (long := long) (short := short) w)
      (sevenUnitDiamondRight (long := long) (short := short) w)) :=
  ⟨⟨.unitDiamond w⟩,
    sevenUnitDiamond_noIdentityComparison (long := long) (short := short) w⟩

theorem unitDiamondEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      UnitDiamondEightCell W l r s t → IdentityEightCell W l r s t) := by
  rintro ⟨interpret⟩
  have q : IdentityEightCell W l r
      (sevenUnitDiamondLeft (long := l) (short := r) l)
      (sevenUnitDiamondRight (long := l) (short := r) l) :=
    interpret _ _ (.unitDiamond l)
  exact sevenUnitDiamond_noIdentityComparison (long := l) (short := r) l ⟨q⟩

/-- The new comparison is NOT raw seventh proof-history equality. -/
theorem unitDiamondEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      UnitDiamondEightCell W l r s t → s = t) := by
  intro interpret
  apply identityEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t (.previous q)

/-- Every constructor of the newly adjoined eighth grammar preserves
the OLD R mod 2 obstruction, including the unique unit diamond. -/
theorem unitDiamondEightCell_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : UnitDiamondEightCell W long short s t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  induction q with
  | previous q => exact identityEightCell_preservesParity q
  | unitDiamond w => exact sevenUnitDiamond_sameParity w
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

/-- Newly chosen quotient, no replacement of old quotients or raw Type. -/
def unitDiamondHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (UnitDiamondEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨unitDiamondEightCell_refl s⟩
    · intro s t h
      rcases h with ⟨q⟩
      exact ⟨.reverse q⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def unitDiamondHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (unitDiamondHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem unitDiamondHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    unitDiamondHistoryClass s = unitDiamondHistoryClass t ↔
      Nonempty (UnitDiamondEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem identityHistoryClass_descendsToUnitDiamond {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : identityHistoryClass s = identityHistoryClass t) :
    unitDiamondHistoryClass s = unitDiamondHistoryClass t := by
  rcases (identityHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (unitDiamondHistoryClass_eq_iff s t).2 ⟨.previous q⟩

/-- The chosen quotient is strictly coarser, with a concrete old
class inequivalence certified by the previously proved Z/4 invariant. -/
theorem unitDiamondHistoryClass_strictlyNew (w : W) :
    (unitDiamondHistoryClass
        (sevenUnitDiamondLeft (long := long) (short := short) w) =
      unitDiamondHistoryClass
        (sevenUnitDiamondRight (long := long) (short := short) w)) ∧
    (identityHistoryClass
        (sevenUnitDiamondLeft (long := long) (short := short) w) ≠
      identityHistoryClass
        (sevenUnitDiamondRight (long := long) (short := short) w)) :=
  ⟨(unitDiamondHistoryClass_eq_iff _ _).2 ⟨.unitDiamond w⟩,
    sevenUnitDiamond_distinctIdentityClasses (long := long) (short := short) w⟩

theorem unitDiamondHistoryClass_noPreviousReturn (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      unitDiamondHistoryClass s = unitDiamondHistoryClass t →
        identityHistoryClass s = identityHistoryClass t) := by
  intro interpret
  have witness := (unitDiamondHistoryClass_strictlyNew
    (long := l) (short := r) l)
  exact witness.2 (interpret
    (sevenUnitDiamondLeft (long := l) (short := r) l)
    (sevenUnitDiamondRight (long := l) (short := r) l) witness.1)

theorem unitDiamondHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      unitDiamondHistoryClass s = unitDiamondHistoryClass t → s = t) := by
  intro interpret
  apply unitDiamondEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((unitDiamondHistoryClass_eq_iff s t).2 ⟨q⟩)

/-- Old R mod 2 continues to descend, in contrast with Z/4 below. -/
theorem unitDiamondHistoryClass_eq_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : unitDiamondHistoryClass s = unitDiamondHistoryClass t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  rcases (unitDiamondHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact unitDiamondEightCell_preservesParity q

def unitDiamondHistoryParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (unitDiamondHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenIdentityParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (unitDiamondEightCell_preservesParity q))

theorem unitDiamondHistoryParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    unitDiamondHistoryParity
      (unitDiamondHistoryClass (long := long) (short := short) s) =
      decide (sevenIdentityParity s = 1) :=
  rfl

/-- The NEW primitive unit diamond has Z/4 jump 2. The unchanged
four-torsion observer therefore DOES NOT descend into the new quotient. -/
theorem unitDiamondHistoryClass_noFourTorsionDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      unitDiamondHistoryClass s = unitDiamondHistoryClass t →
        sevenUnitTorsionResidue s = sevenUnitTorsionResidue t) := by
  intro preserve
  have h := (unitDiamondHistoryClass_strictlyNew
    (long := l) (short := r) l).1
  have hbad := preserve
    (sevenUnitDiamondLeft (long := l) (short := r) l)
    (sevenUnitDiamondRight (long := l) (short := r) l) h
  have vals := sevenUnitDiamond_torsionValues (long := l) (short := r) l
  rw [vals.1, vals.2] at hbad
  norm_num at hbad

/-- Unit diamond pasted with the PREVIOUS identity/doubleInverse peak.
No new mixed primitive is necessary: existing typed contexts suffice. -/
def mixedUnitIdentityDoubleFirst (w : W) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) (.refl w))
        (.symm (.symm (.refl w))))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenUnitDiamondLeft w) (sevenIdentityDoubleDirect w)

def mixedUnitIdentityDoubleSecond (w : W) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) (.refl w))
        (.symm (.symm (.refl w))))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenUnitDiamondRight w) (sevenIdentityDoubleVia w)

def mixedUnitIdentityDouble_fill (w : W) :
    UnitDiamondEightCell W long short
      (mixedUnitIdentityDoubleFirst (long := long) (short := short) w)
      (mixedUnitIdentityDoubleSecond (long := long) (short := short) w) :=
  .compositeContext (.unitDiamond w) (.previous (.identityDouble w))

theorem mixedUnitIdentityDouble_torsionValues (w : W) :
    sevenUnitTorsionResidue
        (mixedUnitIdentityDoubleFirst (long := long) (short := short) w) = 2 ∧
    sevenUnitTorsionResidue
        (mixedUnitIdentityDoubleSecond (long := long) (short := short) w) = 0 := by
  constructor <;>
    norm_num [mixedUnitIdentityDoubleFirst, mixedUnitIdentityDoubleSecond,
      sevenUnitDiamondLeft, sevenUnitDiamondRight,
      sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
      sevenUnitTorsionResidue, sevenUnitTorsionWeight]

theorem mixedUnitIdentityDouble_noPrevious (w : W) :
    ¬ Nonempty (IdentityEightCell W long short
      (mixedUnitIdentityDoubleFirst (long := long) (short := short) w)
      (mixedUnitIdentityDoubleSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := identityEightCell_preservesUnitTorsionResidue q
  have vals := mixedUnitIdentityDouble_torsionValues
    (long := long) (short := short) w
  rw [vals.1, vals.2] at h
  norm_num at h

/-- A second, genuinely typed mixing of unitDiamond and the OLD
left inverseComp/unit overlap at z -> w. -/
def mixedUnitInvCompLeftFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.refl z) (.refl z))
        (.symm (.trans (.refl w) c)))
      (.trans (.refl z) (.symm c)) :=
  .congrComp (sevenUnitDiamondLeft z) (sevenInvCompLeftDirect c)

def mixedUnitInvCompLeftSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.refl z) (.refl z))
        (.symm (.trans (.refl w) c)))
      (.trans (.refl z) (.symm c)) :=
  .congrComp (sevenUnitDiamondRight z) (sevenInvCompLeftVia c)

def mixedUnitInvCompLeft_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    UnitDiamondEightCell W long short
      (mixedUnitInvCompLeftFirst (long := long) (short := short) c)
      (mixedUnitInvCompLeftSecond (long := long) (short := short) c) :=
  .compositeContext (.unitDiamond z) (.previous (.previous (.leftOverlap c)))

theorem mixedUnitInvCompLeft_torsionValues {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenUnitTorsionResidue
        (mixedUnitInvCompLeftFirst (long := long) (short := short) c) = 0 ∧
    sevenUnitTorsionResidue
        (mixedUnitInvCompLeftSecond (long := long) (short := short) c) = 2 := by
  constructor <;>
    norm_num [mixedUnitInvCompLeftFirst, mixedUnitInvCompLeftSecond,
      sevenUnitDiamondLeft, sevenUnitDiamondRight,
      sevenInvCompLeftDirect, sevenInvCompLeftVia,
      sevenUnitTorsionResidue, sevenUnitTorsionWeight]

theorem mixedUnitInvCompLeft_noPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (IdentityEightCell W long short
      (mixedUnitInvCompLeftFirst (long := long) (short := short) c)
      (mixedUnitInvCompLeftSecond (long := long) (short := short) c)) := by
  rintro ⟨q⟩
  have h := identityEightCell_preservesUnitTorsionResidue q
  have vals := mixedUnitInvCompLeft_torsionValues c
  rw [vals.1, vals.2] at h
  norm_num at h

/-- A third mixed unitDiamond with the old left double-inversion and
inverse-cancellation critical pair. -/
def mixedUnitInvolutionLeftFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) (.refl w))
        (.trans (.symm (.symm c)) (.symm c)))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenUnitDiamondLeft w) (sevenLeftDoubleInverseDirect c)

def mixedUnitInvolutionLeftSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) (.refl w))
        (.trans (.symm (.symm c)) (.symm c)))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenUnitDiamondRight w) (sevenLeftDoubleInverseVia c)

def mixedUnitInvolutionLeft_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    UnitDiamondEightCell W long short
      (mixedUnitInvolutionLeftFirst (long := long) (short := short) c)
      (mixedUnitInvolutionLeftSecond (long := long) (short := short) c) :=
  .compositeContext (.unitDiamond w)
    (.previous (.previous (.previous (.leftOverlap c))))

theorem mixedUnitInvolutionLeft_torsionValues {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenUnitTorsionResidue
        (mixedUnitInvolutionLeftFirst (long := long) (short := short) c) = 2 ∧
    sevenUnitTorsionResidue
        (mixedUnitInvolutionLeftSecond (long := long) (short := short) c) = 0 := by
  constructor <;>
    norm_num [mixedUnitInvolutionLeftFirst, mixedUnitInvolutionLeftSecond,
      sevenUnitDiamondLeft, sevenUnitDiamondRight,
      sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
      sevenUnitTorsionResidue, sevenUnitTorsionWeight]

theorem mixedUnitInvolutionLeft_noPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (IdentityEightCell W long short
      (mixedUnitInvolutionLeftFirst (long := long) (short := short) c)
      (mixedUnitInvolutionLeftSecond (long := long) (short := short) c)) := by
  rintro ⟨q⟩
  have h := identityEightCell_preservesUnitTorsionResidue q
  have vals := mixedUnitInvolutionLeft_torsionValues c
  rw [vals.1, vals.2] at h
  norm_num at h

/-- The three mixed critical families require NO extra primitive
beyond unitDiamond; each is new-vs-old and parity-compatible. -/
theorem mixedUnitIdentityDouble_newVsOld (w : W) :
    Nonempty (UnitDiamondEightCell W long short
      (mixedUnitIdentityDoubleFirst (long := long) (short := short) w)
      (mixedUnitIdentityDoubleSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (IdentityEightCell W long short
      (mixedUnitIdentityDoubleFirst (long := long) (short := short) w)
      (mixedUnitIdentityDoubleSecond (long := long) (short := short) w)) ∧
    sevenIdentityParity
        (mixedUnitIdentityDoubleFirst (long := long) (short := short) w) =
      sevenIdentityParity
        (mixedUnitIdentityDoubleSecond (long := long) (short := short) w) :=
  ⟨⟨mixedUnitIdentityDouble_fill w⟩,
    mixedUnitIdentityDouble_noPrevious w,
    unitDiamondEightCell_preservesParity (mixedUnitIdentityDouble_fill w)⟩

theorem mixedUnitInvCompLeft_newVsOld {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (UnitDiamondEightCell W long short
      (mixedUnitInvCompLeftFirst (long := long) (short := short) c)
      (mixedUnitInvCompLeftSecond (long := long) (short := short) c)) ∧
    ¬ Nonempty (IdentityEightCell W long short
      (mixedUnitInvCompLeftFirst (long := long) (short := short) c)
      (mixedUnitInvCompLeftSecond (long := long) (short := short) c)) ∧
    sevenIdentityParity (mixedUnitInvCompLeftFirst c) =
      sevenIdentityParity (mixedUnitInvCompLeftSecond c) :=
  ⟨⟨mixedUnitInvCompLeft_fill c⟩,
    mixedUnitInvCompLeft_noPrevious c,
    unitDiamondEightCell_preservesParity (mixedUnitInvCompLeft_fill c)⟩

theorem mixedUnitInvolutionLeft_newVsOld {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (UnitDiamondEightCell W long short
      (mixedUnitInvolutionLeftFirst (long := long) (short := short) c)
      (mixedUnitInvolutionLeftSecond (long := long) (short := short) c)) ∧
    ¬ Nonempty (IdentityEightCell W long short
      (mixedUnitInvolutionLeftFirst (long := long) (short := short) c)
      (mixedUnitInvolutionLeftSecond (long := long) (short := short) c)) ∧
    sevenIdentityParity (mixedUnitInvolutionLeftFirst c) =
      sevenIdentityParity (mixedUnitInvolutionLeftSecond c) :=
  ⟨⟨mixedUnitInvolutionLeft_fill c⟩,
    mixedUnitInvolutionLeft_noPrevious c,
    unitDiamondEightCell_preservesParity (mixedUnitInvolutionLeft_fill c)⟩

/-- Selected local critical family: previously certified v4.98 and
v4.99 peaks, the only new primitive, three new mixed overlaps, and
explicit typed contexts. NO global all-history completeness. -/
inductive UnitDiamondCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityCriticalPeak W l r s t) :
      UnitDiamondCriticalPeak W l r s t
  | previousMixed {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedIdentityCriticalPeak W l r s t) :
      UnitDiamondCriticalPeak W l r s t
  | unitDiamond (w : W) :
      UnitDiamondCriticalPeak W l r
        (sevenUnitDiamondLeft (long := l) (short := r) w)
        (sevenUnitDiamondRight (long := l) (short := r) w)
  | mixedIdentityDouble (w : W) :
      UnitDiamondCriticalPeak W l r
        (mixedUnitIdentityDoubleFirst (long := l) (short := r) w)
        (mixedUnitIdentityDoubleSecond (long := l) (short := r) w)
  | mixedInvCompLeft {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
      UnitDiamondCriticalPeak W l r
        (mixedUnitInvCompLeftFirst (long := l) (short := r) c)
        (mixedUnitInvCompLeftSecond (long := l) (short := r) c)
  | mixedInvolutionLeft {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
      UnitDiamondCriticalPeak W l r
        (mixedUnitInvolutionLeftFirst (long := l) (short := r) c)
        (mixedUnitInvolutionLeftSecond (long := l) (short := r) c)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondCriticalPeak W l r s t) :
      UnitDiamondCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : UnitDiamondCriticalPeak W l r s t)
      (q' : UnitDiamondCriticalPeak W l r t u) :
      UnitDiamondCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : UnitDiamondCriticalPeak W l r s t) :
      UnitDiamondCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      UnitDiamondCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : UnitDiamondCriticalPeak W l r s t) :
      UnitDiamondCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : UnitDiamondCriticalPeak W l r s s')
      (q' : UnitDiamondCriticalPeak W l r t t') :
      UnitDiamondCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

/-- Complete induction OVER THE SELECTED family, constructing actual
Type-valued eighth comparisons and never postulating equality. -/
def unitDiamondCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : UnitDiamondCriticalPeak W long short s t) :
    UnitDiamondEightCell W long short s t := by
  induction p with
  | previous q => exact .previous (identityCriticalPeak_fill q)
  | previousMixed q => exact .previous (mixedIdentityCriticalPeak_fill q)
  | unitDiamond w => exact .unitDiamond w
  | mixedIdentityDouble w => exact mixedUnitIdentityDouble_fill w
  | mixedInvCompLeft c => exact mixedUnitInvCompLeft_fill c
  | mixedInvolutionLeft c => exact mixedUnitInvolutionLeft_fill c
  | reverse q ih => exact .reverse ih
  | chain q q' ih ih' => exact .chain ih ih'
  | whiskerLeft before q ih => exact .whiskerLeft before ih
  | whiskerRight q after ih => exact .whiskerRight ih after
  | inverseContext q ih => exact .inverseContext ih
  | compositeContext q q' ih ih' => exact .compositeContext ih ih'

theorem unitDiamondCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : UnitDiamondCriticalPeak W long short s t) :
    Nonempty (UnitDiamondEightCell W long short s t) :=
  ⟨unitDiamondCriticalPeak_fill p⟩

theorem unitDiamondCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : UnitDiamondCriticalPeak W long short s t) :
    unitDiamondHistoryClass s = unitDiamondHistoryClass t :=
  (unitDiamondHistoryClass_eq_iff s t).2 (unitDiamondCriticalPeak_joinable p)

/-- A genuine P77 source-pasted unit diamond uses precisely the
one new primitive and a previous identity reflexivity witness. -/
def unitDiamondComposite_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    UnitDiamondEightCell W long short
      (sevenUnitDiamondCompositeLeft (long := long) (short := short) c)
      (sevenUnitDiamondCompositeRight (long := long) (short := short) c) :=
  .compositeContext (.unitDiamond w)
    (unitDiamondEightCell_refl (.refl c))

theorem unitDiamondComposite_strictNew {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (UnitDiamondEightCell W long short
      (sevenUnitDiamondCompositeLeft (long := long) (short := short) c)
      (sevenUnitDiamondCompositeRight (long := long) (short := short) c)) ∧
    ¬ Nonempty (IdentityEightCell W long short
      (sevenUnitDiamondCompositeLeft (long := long) (short := short) c)
      (sevenUnitDiamondCompositeRight (long := long) (short := short) c)) ∧
    sevenIdentityParity (sevenUnitDiamondCompositeLeft c) =
      sevenIdentityParity (sevenUnitDiamondCompositeRight c) :=
  ⟨⟨unitDiamondComposite_fill c⟩,
    sevenUnitDiamondComposite_noIdentityComparison c,
    unitDiamondEightCell_preservesParity (unitDiamondComposite_fill c)⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77UnitDiamondCompletion
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

/-- For EVERY original P77 terminal raw index, the true GK5CG source
provides an actual TYPE-indexed sixth-cell generator: the new
comparison exists, the former comparison does not, residual parity
is equal, and the strict original equality-interpreter remains absent. -/
theorem pentagonActualUnitDiamondCompletionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.UnitDiamondEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeLeft c)
        (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeRight c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.IdentityEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeLeft c)
        (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeRight c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.unitDiamondComposite_fill _⟩,
    PentagonAdjoinedSixCell.sevenUnitDiamondComposite_noIdentityComparison _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.UnitDiamondEightCell
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_refl
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_ofIdentity
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_preservesParity
#print axioms PentagonAdjoinedSixCell.unitDiamondHistorySetoid
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_descendsToUnitDiamond
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_noPreviousReturn
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_noStrictReturn
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_eq_preservesParity
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryParity
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryParity_onClass
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_noFourTorsionDescent
#print axioms PentagonAdjoinedSixCell.mixedUnitIdentityDoubleFirst
#print axioms PentagonAdjoinedSixCell.mixedUnitIdentityDoubleSecond
#print axioms PentagonAdjoinedSixCell.mixedUnitIdentityDouble_fill
#print axioms PentagonAdjoinedSixCell.mixedUnitIdentityDouble_torsionValues
#print axioms PentagonAdjoinedSixCell.mixedUnitIdentityDouble_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedUnitInvCompLeftFirst
#print axioms PentagonAdjoinedSixCell.mixedUnitInvCompLeftSecond
#print axioms PentagonAdjoinedSixCell.mixedUnitInvCompLeft_fill
#print axioms PentagonAdjoinedSixCell.mixedUnitInvCompLeft_torsionValues
#print axioms PentagonAdjoinedSixCell.mixedUnitInvCompLeft_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedUnitInvolutionLeftFirst
#print axioms PentagonAdjoinedSixCell.mixedUnitInvolutionLeftSecond
#print axioms PentagonAdjoinedSixCell.mixedUnitInvolutionLeft_fill
#print axioms PentagonAdjoinedSixCell.mixedUnitInvolutionLeft_torsionValues
#print axioms PentagonAdjoinedSixCell.mixedUnitInvolutionLeft_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedUnitIdentityDouble_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedUnitInvCompLeft_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedUnitInvolutionLeft_newVsOld
#print axioms PentagonAdjoinedSixCell.UnitDiamondCriticalPeak
#print axioms PentagonAdjoinedSixCell.unitDiamondCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.unitDiamondCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.unitDiamondCriticalPeak_classEq
#print axioms PentagonAdjoinedSixCell.unitDiamondComposite_fill
#print axioms PentagonAdjoinedSixCell.unitDiamondComposite_strictNew
#print axioms pentagonActualUnitDiamondCompletionWithSourceObstruction

end ActualOriginalP77UnitDiamondCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
