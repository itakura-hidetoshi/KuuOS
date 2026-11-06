import KUOS.Architecture.QiWuxingGK5CHP77UnitDiamondMinimalHigherCompletionV5_01

/-!
Qi v5.02 — BALANCED INVERSE / UNIT-COUNT RESIDUAL OBSTRUCTION.

The v5.01 independent UnitDiamondEightCell presentation adjoins
exactly the leftUnit(refl) / rightUnit(refl) comparison while preserving
the old R mod 2 observer. Equal residual parity is NOT yet known to
force a new eighth-level comparison.

We prove a NEW INTEGER observation, the signed total number of
leftUnit and rightUnit primitives in the unchanged original 13-rule
SevenRewrite history. Its value is invariant under ALL v4.91 original
22 comparison rules, triangle, involution, inverseComp, identityDouble,
and the v5.01 unitDiamond primitive and their full typed contexts.

A concrete pair with identical genuine six-cell endpoints uses TWO
independent inverse-cancellation/unit overlaps:
  inverseLeft(refl) versus inverseId ; leftUnit,
  inverseRight(refl) versus inverseId ; rightUnit.
Paste the direct reductions horizontally on the first path, and the
two alternative reductions on the second. The old T charge differs by 1 on this two-factor precursor. Add a
third ACTUAL left-triangle comparison to balance T, leaving an explicit
three-charge AND residual-parity invisible unit-count obstruction.
The all-constructor unit-count conservation proves that NO
UnitDiamondEightCell joins this actual pair. Thus residual parity
remains INCOMPLETE after v5.01, without any new primitive or axiom.

We construct a genuine Z-valued quotient observer by Quotient.lift,
a nonlinear non-factorization certificate, and transport the obstruction
to EVERY original P77 terminal raw index using the original GK5CG
source Type without promoting quotient equality to source strict Eq.

Append-only / tighten-only / overwrite-forbidden / same-root;
public root107, protected validation PR #1558 untouched.
Pinned Lean 4.30.0-rc2; mathlib
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

/-- Signed total of the TWO existing unit eliminations in the
original raw seven-cell rewrite history; all other primitives are 0.
The charge is not an equality of raw proof histories. -/
def sevenUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenUnitStepCharge s
  | .trans s t => sevenUnitStepCharge s + sevenUnitStepCharge t
  | .congrInv s => sevenUnitStepCharge s
  | .congrComp s t => sevenUnitStepCharge s + sevenUnitStepCharge t
  | .leftUnit _ => 1
  | .rightUnit _ => 1
  | .assoc _ _ _ => 0
  | .inverseRight _ => 0
  | .inverseLeft _ => 0
  | .doubleInverse _ => 0
  | .inverseId _ => 0
  | .inverseComp _ _ => 0

/-- The full original 22-rule EIGHT comparison grammar preserves
integer unit count: zigzagDiamond has one unit step on BOTH branches.
No additional original eighth-level comparison is assumed. -/
theorem eightCell_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => sevenUnitStepCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => n + sevenUnitStepCharge after) ih
  | reverseContext q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => -n) ih
  | inverseContext q ih =>
      simpa [sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenUnitStepCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'
  | unitLeft s => simp [sevenUnitStepCharge]
  | unitRight s => simp [sevenUnitStepCharge]
  | associate s t u =>
      simp [sevenUnitStepCharge, add_assoc]
  | cancelRight s => simp [sevenUnitStepCharge]
  | cancelLeft s => simp [sevenUnitStepCharge]
  | involute s => simp [sevenUnitStepCharge]
  | inverseIdentity c => simp [sevenUnitStepCharge]
  | inverseComposite s t =>
      simp only [sevenUnitStepCharge] <;> omega
  | inverseCongruenceIdentity c =>
      simp [sevenUnitStepCharge]
  | inverseCongruenceChain s t =>
      simp [sevenUnitStepCharge]
  | compositeCongruenceIdentity c d =>
      simp [sevenUnitStepCharge]
  | compositeCongruenceChain s s' t t' =>
      simp only [sevenUnitStepCharge] <;> omega
  | interchange s t =>
      simp only [sevenUnitStepCharge] <;> omega
  | zigzagDiamond c =>
      norm_num [sevenUnitStepCharge]

/-- Both genuine triangle overlaps consume the same one unit.
All contexts remain type-indexed. -/
theorem triangleEightCell_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  induction q with
  | original q => exact eightCell_preservesUnitStepCharge q
  | leftTriangle c d =>
      norm_num [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenUnitStepCharge]
  | rightTriangle c d =>
      norm_num [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenUnitStepCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => sevenUnitStepCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => n + sevenUnitStepCharge after) ih
  | inverseContext q ih =>
      simpa [sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenUnitStepCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The two genuine double-inversion/cancellation comparisons contain
no added unit primitive; the previous comparison proof is inherited. -/
theorem involutionEightCell_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  induction q with
  | previous q => exact triangleEightCell_preservesUnitStepCharge q
  | leftOverlap c =>
      norm_num [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
        sevenUnitStepCharge]
  | rightOverlap c =>
      norm_num [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
        sevenUnitStepCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => sevenUnitStepCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => n + sevenUnitStepCharge after) ih
  | inverseContext q ih =>
      simpa [sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenUnitStepCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The two original inverseComposite/unit overlaps exchange one
unit against another; hence integer unit count is still conserved. -/
theorem inverseCompEightCell_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InverseCompEightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  induction q with
  | previous q => exact involutionEightCell_preservesUnitStepCharge q
  | leftOverlap c =>
      norm_num [sevenInvCompLeftDirect, sevenInvCompLeftVia,
        sevenUnitStepCharge]
  | rightOverlap c =>
      norm_num [sevenInvCompRightDirect, sevenInvCompRightVia,
        sevenUnitStepCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => sevenUnitStepCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => n + sevenUnitStepCharge after) ih
  | inverseContext q ih =>
      simpa [sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenUnitStepCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The v4.98 identityDouble primitive contributes no unit on EITHER
side; all other comparison generators are inherited and type-sound. -/
theorem identityEightCell_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  induction q with
  | previous q => exact inverseCompEightCell_preservesUnitStepCharge q
  | identityDouble w =>
      norm_num [sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
        sevenUnitStepCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => sevenUnitStepCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => n + sevenUnitStepCharge after) ih
  | inverseContext q ih =>
      simpa [sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenUnitStepCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The FINAL v5.01 UnitDiamondEightCell grammar preserves this
genuinely integer-valued new observation under ALL constructors.
The v5.01 unitDiamond maps a left unit to a right unit, charge 1=1. -/
theorem unitDiamondEightCell_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : UnitDiamondEightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  induction q with
  | previous q => exact identityEightCell_preservesUnitStepCharge q
  | unitDiamond w =>
      norm_num [sevenUnitDiamondLeft, sevenUnitDiamondRight,
        sevenUnitStepCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => sevenUnitStepCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenUnitStepCharge] using
        congrArg (fun n : ℤ => n + sevenUnitStepCharge after) ih
  | inverseContext q ih =>
      simpa [sevenUnitStepCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenUnitStepCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- A genuine integer observer on the v5.01 new quotient: descent is
by Quotient.lift, not by strict equality of raw seven-cell syntax. -/
def unitDiamondHistoryUnitCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (unitDiamondHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenUnitStepCharge s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact unitDiamondEightCell_preservesUnitStepCharge q)

theorem unitDiamondHistoryUnitCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    unitDiamondHistoryUnitCount
        (unitDiamondHistoryClass (long := long) (short := short) s) =
      sevenUnitStepCharge s :=
  rfl

theorem unitDiamondHistoryClass_eq_preservesUnitStepCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : unitDiamondHistoryClass s = unitDiamondHistoryClass t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t := by
  rcases (unitDiamondHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact unitDiamondEightCell_preservesUnitStepCharge q

/-- Direct reduction of (symm refl(w));refl(w) via original inverseLeft. -/
def sevenInverseUnitLeftDirect (w : W) :
    SevenRewrite W long short
      (.trans (.symm (.refl w)) (.refl w)) (.refl w) :=
  .inverseLeft (.refl w)

/-- An independent original route via inverseId THEN leftUnit.
All intermediate six-cell raw words remain explicit and typed. -/
def sevenInverseUnitLeftVia (w : W) :
    SevenRewrite W long short
      (.trans (.symm (.refl w)) (.refl w)) (.refl w) :=
  .trans
    (.congrComp (.inverseId w) (.refl (.refl w)))
    (.leftUnit (.refl w))

/-- Direct reduction of refl(w);(symm refl(w)) via inverseRight. -/
def sevenInverseUnitRightDirect (w : W) :
    SevenRewrite W long short
      (.trans (.refl w) (.symm (.refl w))) (.refl w) :=
  .inverseRight (.refl w)

/-- Parallel right route via inverseId THEN rightUnit. -/
def sevenInverseUnitRightVia (w : W) :
    SevenRewrite W long short
      (.trans (.refl w) (.symm (.refl w))) (.refl w) :=
  .trans
    (.congrComp (.refl (.refl w)) (.inverseId w))
    (.rightUnit (.refl w))

/-- Two independent cancellation peaks, glued horizontally, form
one ACTUAL same-endpoint seven-cell pair with two alternative routes. -/
def sevenBalancedInverseUnitFirst (w : W) :
    SevenRewrite W long short
      (.trans
        (.trans (.symm (.refl w)) (.refl w))
        (.trans (.refl w) (.symm (.refl w))))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenInverseUnitLeftDirect w)
    (sevenInverseUnitRightDirect w)

def sevenBalancedInverseUnitSecond (w : W) :
    SevenRewrite W long short
      (.trans
        (.trans (.symm (.refl w)) (.refl w))
        (.trans (.refl w) (.symm (.refl w))))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenInverseUnitLeftVia w)
    (sevenInverseUnitRightVia w)

/-- Direct branch has zero unit reductions; alternative branch
contains exactly two genuine unit reductions, one of each hand. -/
theorem sevenBalancedInverseUnit_unitValues (w : W) :
    sevenUnitStepCharge
        (sevenBalancedInverseUnitFirst (long := long) (short := short) w) = 0 ∧
    sevenUnitStepCharge
        (sevenBalancedInverseUnitSecond (long := long) (short := short) w) = 2 := by
  constructor <;>
    norm_num [sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenUnitStepCharge]

/-- R gives 0 and 2, so both histories have SAME parity zero. -/
theorem sevenBalancedInverseUnit_parityValues (w : W) :
    sevenIdentityParity
        (sevenBalancedInverseUnitFirst (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenBalancedInverseUnitSecond (long := long) (short := short) w) = 0 := by
  constructor <;>
    norm_num [sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenIdentityParity, sevenIdentityBalance]

theorem sevenBalancedInverseUnit_sameParity (w : W) :
    sevenIdentityParity
        (sevenBalancedInverseUnitFirst (long := long) (short := short) w) =
      sevenIdentityParity
        (sevenBalancedInverseUnitSecond (long := long) (short := short) w) := by
  exact (sevenBalancedInverseUnit_parityValues (long := long) (short := short) w).1.trans
    (sevenBalancedInverseUnit_parityValues (long := long) (short := short) w).2.symm

/-- The two-factor precursor is NOT three-charge invisible:
old T is 1 versus 0. The genuine triangle comparison below compensates. -/
theorem sevenBalancedInverseUnit_tripleValues (w : W) :
    sevenChargeTriple
        (sevenBalancedInverseUnitFirst (long := long) (short := short) w) =
        (1, 0, 0) ∧
    sevenChargeTriple
        (sevenBalancedInverseUnitSecond (long := long) (short := short) w) =
        (0, 0, 0) := by
  constructor <;>
    norm_num [sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenChargeTriple, sevenTriangleCharge, sevenInvolutionCharge,
      sevenInverseCompCharge]

/-- This is a PROVED remaining obstruction after v5.01, not a
failure to search for a comparison: any existing comparison must
preserve integer unit count, contradicting the real 0/2 pair. -/
theorem sevenBalancedInverseUnit_noComparison (w : W) :
    ¬ Nonempty (UnitDiamondEightCell W long short
      (sevenBalancedInverseUnitFirst (long := long) (short := short) w)
      (sevenBalancedInverseUnitSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := unitDiamondEightCell_preservesUnitStepCharge q
  have vals := sevenBalancedInverseUnit_unitValues (long := long) (short := short) w
  rw [vals.1, vals.2] at h
  norm_num at h

theorem sevenBalancedInverseUnit_distinctClasses (w : W) :
    unitDiamondHistoryClass
        (sevenBalancedInverseUnitFirst (long := long) (short := short) w) ≠
      unitDiamondHistoryClass
        (sevenBalancedInverseUnitSecond (long := long) (short := short) w) := by
  intro h
  exact sevenBalancedInverseUnit_noComparison (long := long) (short := short) w
    ((unitDiamondHistoryClass_eq_iff _ _).1 h)

/-- Refutes the universal claim that equal residual parity alone
implies a new v5.01 eighth-cell witness for arbitrary parallel
histories. Both counterexample paths are genuine and typed. -/
theorem sevenIdentityParity_notCompleteAfterUnitDiamond (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      sevenIdentityParity s = sevenIdentityParity t →
        Nonempty (UnitDiamondEightCell W l r s t)) := by
  intro every
  exact sevenBalancedInverseUnit_noComparison (long := l) (short := r) l
    (every
      (sevenBalancedInverseUnitFirst (long := l) (short := r) l)
      (sevenBalancedInverseUnitSecond (long := l) (short := r) l)
      (sevenBalancedInverseUnit_sameParity (long := l) (short := r) l))

/-- Even an arbitrary NONLINEAR function of the old parity cannot
recover integer unit-count universally on the genuine raw histories. -/
theorem sevenUnitStepCharge_notFactorThroughParity (l r : W) :
    ¬ ∃ F : ℤ → ℤ,
      ∀ {w z : W}
        {c d : PentagonAdjoinedSixCell W l r w z}
        (s : SevenRewrite W l r c d),
        sevenUnitStepCharge s = F (sevenIdentityParity s) := by
  rintro ⟨F, factor⟩
  have h₁ := factor (sevenBalancedInverseUnitFirst (long := l) (short := r) l)
  have h₂ := factor (sevenBalancedInverseUnitSecond (long := l) (short := r) l)
  have hp := sevenBalancedInverseUnit_sameParity (long := l) (short := r) l
  have eq :
      sevenUnitStepCharge
          (sevenBalancedInverseUnitFirst (long := l) (short := r) l) =
        sevenUnitStepCharge
          (sevenBalancedInverseUnitSecond (long := l) (short := r) l) := by
    calc
      _ = F (sevenIdentityParity
            (sevenBalancedInverseUnitFirst (long := l) (short := r) l)) := h₁
      _ = F (sevenIdentityParity
            (sevenBalancedInverseUnitSecond (long := l) (short := r) l)) :=
        congrArg F hp
      _ = _ := h₂.symm
  have vals := sevenBalancedInverseUnit_unitValues (long := l) (short := r) l
  rw [vals.1, vals.2] at eq
  norm_num at eq

/-- Paste the new certified obstruction into an ACTUAL original
P77/GK5CG six-cell source context, preserving exact raw endpoints. -/
def sevenBalancedInverseUnitCompositeFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans
        (.trans
          (.trans (.symm (.refl w)) (.refl w))
          (.trans (.refl w) (.symm (.refl w))))
        c)
      (.trans (.trans (.refl w) (.refl w)) c) :=
  .congrComp (sevenBalancedInverseUnitFirst w) (.refl c)

def sevenBalancedInverseUnitCompositeSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans
        (.trans
          (.trans (.symm (.refl w)) (.refl w))
          (.trans (.refl w) (.symm (.refl w))))
        c)
      (.trans (.trans (.refl w) (.refl w)) c) :=
  .congrComp (sevenBalancedInverseUnitSecond w) (.refl c)

theorem sevenBalancedInverseUnitComposite_values {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    (sevenUnitStepCharge (sevenBalancedInverseUnitCompositeFirst c) = 0 ∧
      sevenUnitStepCharge (sevenBalancedInverseUnitCompositeSecond c) = 2) ∧
    sevenIdentityParity (sevenBalancedInverseUnitCompositeFirst c) =
      sevenIdentityParity (sevenBalancedInverseUnitCompositeSecond c) := by
  constructor
  · constructor <;>
      norm_num [sevenBalancedInverseUnitCompositeFirst,
        sevenBalancedInverseUnitCompositeSecond,
        sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
        sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
        sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
        sevenUnitStepCharge]
  · simp [sevenBalancedInverseUnitCompositeFirst,
      sevenBalancedInverseUnitCompositeSecond,
      sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenIdentityParity, sevenIdentityBalance]

theorem sevenBalancedInverseUnitComposite_noComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (UnitDiamondEightCell W long short
      (sevenBalancedInverseUnitCompositeFirst c)
      (sevenBalancedInverseUnitCompositeSecond c)) := by
  rintro ⟨q⟩
  have h := unitDiamondEightCell_preservesUnitStepCharge q
  have vals := (sevenBalancedInverseUnitComposite_values c).1
  rw [vals.1, vals.2] at h
  norm_num at h


/-- Original three-charge compensation with an ACTUAL left unit /
associativity critical pair, never with a fabricated T certificate. -/
def balancedUnitInvisibleSource (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans
    (.trans
      (.trans (.symm (.refl w)) (.refl w))
      (.trans (.refl w) (.symm (.refl w))))
    (.trans (.trans (.refl w) (.refl w)) (.refl w))

def balancedUnitInvisibleTarget (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans
    (.trans (.refl w) (.refl w))
    (.trans (.refl w) (.refl w))

/-- Old T: two-factor FIRST=1 and triangle DIRECT=0. -/
def sevenBalancedUnitInvisibleFirst (w : W) :
    SevenRewrite W long short
      (balancedUnitInvisibleSource (long := long) (short := short) w)
      (balancedUnitInvisibleTarget (long := long) (short := short) w) :=
  .congrComp (sevenBalancedInverseUnitFirst w)
    (sevenLeftTriangleDirect (.refl w) (.refl w))

/-- Old T: two-factor SECOND=0 and triangle VIA=1. -/
def sevenBalancedUnitInvisibleSecond (w : W) :
    SevenRewrite W long short
      (balancedUnitInvisibleSource (long := long) (short := short) w)
      (balancedUnitInvisibleTarget (long := long) (short := short) w) :=
  .congrComp (sevenBalancedInverseUnitSecond w)
    (sevenLeftTriangleViaAssoc (.refl w) (.refl w))

/-- The old T,J,K tuple is exactly (1,0,0) on BOTH routes. -/
theorem sevenBalancedUnitInvisible_tripleValues (w : W) :
    sevenChargeTriple
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) =
        (1, 0, 0) ∧
    sevenChargeTriple
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) =
        (1, 0, 0) := by
  constructor <;>
    norm_num [sevenBalancedUnitInvisibleFirst, sevenBalancedUnitInvisibleSecond,
      sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
      sevenChargeTriple, sevenTriangleCharge, sevenInvolutionCharge,
      sevenInverseCompCharge]

theorem sevenBalancedUnitInvisible_sameTriple (w : W) :
    sevenChargeTriple
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) =
      sevenChargeTriple
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) := by
  exact (sevenBalancedUnitInvisible_tripleValues
    (long := long) (short := short) w).1.trans
    (sevenBalancedUnitInvisible_tripleValues
      (long := long) (short := short) w).2.symm

/-- One old unit step on both triangle branches, but an additional two
genuine unit steps in the second inverse-unit cancellation route. -/
theorem sevenBalancedUnitInvisible_unitValues (w : W) :
    sevenUnitStepCharge
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) = 1 ∧
    sevenUnitStepCharge
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) = 3 := by
  constructor <;>
    norm_num [sevenBalancedUnitInvisibleFirst, sevenBalancedUnitInvisibleSecond,
      sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
      sevenUnitStepCharge]

theorem sevenBalancedUnitInvisible_parityValues (w : W) :
    sevenIdentityParity
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) = 0 := by
  constructor <;>
    norm_num [sevenBalancedUnitInvisibleFirst, sevenBalancedUnitInvisibleSecond,
      sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
      sevenIdentityParity, sevenIdentityBalance]

theorem sevenBalancedUnitInvisible_sameParity (w : W) :
    sevenIdentityParity
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) =
      sevenIdentityParity
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) := by
  exact (sevenBalancedUnitInvisible_parityValues
    (long := long) (short := short) w).1.trans
    (sevenBalancedUnitInvisible_parityValues
      (long := long) (short := short) w).2.symm

/-- CERTIFIED: same old triple, same R parity, different integer count,
and NO UnitDiamondEightCell comparison in the entire chosen grammar. -/
theorem sevenBalancedUnitInvisible_noComparison (w : W) :
    ¬ Nonempty (UnitDiamondEightCell W long short
      (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w)
      (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := unitDiamondEightCell_preservesUnitStepCharge q
  have vals := sevenBalancedUnitInvisible_unitValues
    (long := long) (short := short) w
  rw [vals.1, vals.2] at h
  norm_num at h

theorem sevenBalancedUnitInvisible_distinctClasses (w : W) :
    unitDiamondHistoryClass
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) ≠
      unitDiamondHistoryClass
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) := by
  intro h
  exact sevenBalancedUnitInvisible_noComparison (long := long) (short := short) w
    ((unitDiamondHistoryClass_eq_iff _ _).1 h)

/-- Joint old T,J,K and residual parity still DO NOT classify the
chosen v5.01 eighth-history quotient. -/
theorem sevenTripleAndParity_notCompleteAfterUnitDiamond (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      sevenChargeTriple s = sevenChargeTriple t →
      sevenIdentityParity s = sevenIdentityParity t →
        Nonempty (UnitDiamondEightCell W l r s t)) := by
  intro all
  exact sevenBalancedUnitInvisible_noComparison (long := l) (short := r) l
    (all
      (sevenBalancedUnitInvisibleFirst (long := l) (short := r) l)
      (sevenBalancedUnitInvisibleSecond (long := l) (short := r) l)
      (sevenBalancedUnitInvisible_sameTriple (long := l) (short := r) l)
      (sevenBalancedUnitInvisible_sameParity (long := l) (short := r) l))

/-- No new primitive is added to address this genuine obstruction. -/

end PentagonAdjoinedSixCell

section ActualOriginalP77BalancedInverseUnit
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

/-- At EVERY original P77 terminal raw index, the unchanged GK5CG
five-cell source yields an explicit genuine parallel seven-cell pair
of equal R-parity which cannot be compared in the full chosen v5.01
UnitDiamondEightCell Type. The original strict Eq interpreter no-go
remains independent and unchanged. -/
theorem pentagonActualBalancedInverseUnitWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenBalancedInverseUnitCompositeFirst c) =
        PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenBalancedInverseUnitCompositeSecond c) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.UnitDiamondEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenBalancedInverseUnitCompositeFirst c)
        (PentagonAdjoinedSixCell.sevenBalancedInverseUnitCompositeSecond c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    (PentagonAdjoinedSixCell.sevenBalancedInverseUnitComposite_values _).2,
    PentagonAdjoinedSixCell.sevenBalancedInverseUnitComposite_noComparison _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sevenUnitStepCharge
#print axioms PentagonAdjoinedSixCell.eightCell_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.involutionEightCell_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.identityEightCell_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryUnitCount
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryUnitCount_onClass
#print axioms PentagonAdjoinedSixCell.unitDiamondHistoryClass_eq_preservesUnitStepCharge
#print axioms PentagonAdjoinedSixCell.sevenInverseUnitLeftDirect
#print axioms PentagonAdjoinedSixCell.sevenInverseUnitLeftVia
#print axioms PentagonAdjoinedSixCell.sevenInverseUnitRightDirect
#print axioms PentagonAdjoinedSixCell.sevenInverseUnitRightVia
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnitFirst
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnitSecond
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnit_unitValues
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnit_parityValues
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnit_sameParity
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnit_tripleValues
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnit_noComparison
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnit_distinctClasses
#print axioms PentagonAdjoinedSixCell.sevenIdentityParity_notCompleteAfterUnitDiamond
#print axioms PentagonAdjoinedSixCell.sevenUnitStepCharge_notFactorThroughParity
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnitCompositeFirst
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnitCompositeSecond
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnitComposite_values
#print axioms PentagonAdjoinedSixCell.sevenBalancedInverseUnitComposite_noComparison
#print axioms PentagonAdjoinedSixCell.balancedUnitInvisibleSource
#print axioms PentagonAdjoinedSixCell.balancedUnitInvisibleTarget
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisibleFirst
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisibleSecond
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_tripleValues
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_sameTriple
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_unitValues
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_parityValues
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_sameParity
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_noComparison
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_distinctClasses
#print axioms PentagonAdjoinedSixCell.sevenTripleAndParity_notCompleteAfterUnitDiamond
#print axioms pentagonActualBalancedInverseUnitWithSourceObstruction

end ActualOriginalP77BalancedInverseUnit
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
