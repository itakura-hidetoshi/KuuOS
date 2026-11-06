import KUOS.Architecture.QiWuxingGK5CHP77BalancedUnitMinimalHigherCompletionV5_03

/-!
Qi v5.04 — DOUBLE COMPOSITE CANCELLATION RESIDUAL OBSTRUCTION.

We work in the UNCHANGED original thirteen-rule typed SevenRewrite
and the independent v5.03 BalancedUnitEightCell comparison grammar.

First, a parity cocycle for source/target SIX-cell word shapes shows
that the two old Bool observations, R mod 2 and U mod 2, are coupled
on EVERY fixed source/target pair. It is therefore incorrect to
assume that they provide two unconstrained independent bits for
parallel seventh histories.

Second, we define a DIFFERENT signed integer observable V: count
leftUnit, rightUnit, inverseLeft, and inverseRight with weight +1;
all other primitive generators have weight zero. Reversal negates,
typed vertical and horizontal composition add, and inverse-context
preserves the value.

We prove V conservation for ALL old original EightCell constructors,
all triangle, involution, inverseComp, identityDouble, unitDiamond,
and balancedUnit comparisons and every typed context. Quotient.lift
then yields a true Z-valued observer on the chosen v5.03 quotient.

A genuine original seven-cell critical peak removes a composite
inverse in one step (V=1), or expands the inverse and sequentially
cancels its two factors (V=3). This single peak has old R and U
residual-parity jumps of one. We paste TWO independent copies in a
fully typed horizontal context: their R/U parities now BOTH agree,
while V differs by 2 versus 6. No old BalancedUnitEightCell can
compare the pair because ALL its constructors preserve V.

The counterexample is transported to EACH original P77 final raw
index using the true GK5CG source six-cell and retaining the strict
source Eq-interpreter obstruction. No new eighth- or ninth-cell primitive,
global thinness, or new source equality is asserted.

Append-only / tighten-only / overwrite-forbidden / same-root.
Public root107 and protected validation-only PR #1558 retained.
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

/-- Integer size of the original FREE six-cell raw syntax counting
the constructors symm and trans; no six-cell quotient is taken. -/
def sixRawShapeWeight {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) : ℤ :=
  match c with
  | .refl _ => 0
  | .pentagon => 0
  | .symm c => sixRawShapeWeight c + 1
  | .trans c d => sixRawShapeWeight c + sixRawShapeWeight d + 1

/-- The original R and U mod-two observations satisfy a coboundary
constraint determined ONLY by the genuine raw source/target words.
This is proved over ALL thirteen SevenRewrite constructors, not
postulated as a property of an arbitrary quotient. -/
theorem sevenRawBoundaryParitySound {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    (sixRawShapeWeight c + sevenIdentityBalance s +
        sevenUnitStepCharge s) % 2 =
      sixRawShapeWeight d % 2 := by
  induction s with
  | refl c =>
      simp [sevenIdentityBalance, sevenUnitStepCharge]
  | symm s ih =>
      simp only [sevenIdentityBalance, sevenUnitStepCharge]
      omega
  | trans s t ihs iht =>
      simp only [sevenIdentityBalance, sevenUnitStepCharge]
      omega
  | congrInv s ih =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | congrComp s t ihs iht =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | leftUnit c =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | rightUnit c =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | assoc c d e =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | inverseRight c =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | inverseLeft c =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | doubleInverse c =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega
  | inverseId w =>
      norm_num [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
  | inverseComp c d =>
      simp only [sixRawShapeWeight, sevenIdentityBalance,
        sevenUnitStepCharge]
      omega

/-- On every parallel pair, the total parity R+U depends only
on the fixed original six-cell raw endpoints, not on the history. -/
theorem sevenParallelBoundaryParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    (sevenIdentityParity s + sevenUnitCountParity s) % 2 =
      (sevenIdentityParity t + sevenUnitCountParity t) % 2 := by
  have hs := sevenRawBoundaryParitySound (long := long) (short := short) s
  have ht := sevenRawBoundaryParitySound (long := long) (short := short) t
  simp only [sevenIdentityParity, sevenUnitCountParity]
  omega

/-- A notable refinement: the two surviving mod-two observations
are NOT independent over a fixed typed hom. Equality in one is
equivalent to equality in the other for ANY two parallel histories,
even when no higher comparison is available. -/
theorem sevenParallelParityCoupling {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    sevenIdentityParity s = sevenIdentityParity t ↔
      sevenUnitCountParity s = sevenUnitCountParity t := by
  have h := sevenParallelBoundaryParity (long := long) (short := short) s t
  have hsR : 0 ≤ sevenIdentityParity s ∧ sevenIdentityParity s < 2 := by
    simp [sevenIdentityParity]
    omega
  have htR : 0 ≤ sevenIdentityParity t ∧ sevenIdentityParity t < 2 := by
    simp [sevenIdentityParity]
    omega
  have hsU : 0 ≤ sevenUnitCountParity s ∧ sevenUnitCountParity s < 2 := by
    simp [sevenUnitCountParity]
    omega
  have htU : 0 ≤ sevenUnitCountParity t ∧ sevenUnitCountParity t < 2 := by
    simp [sevenUnitCountParity]
    omega
  constructor <;> intro hh <;> omega

/-- Signed total of unit eliminations AND inverse cancellations on the
original 13-rule history. Unlike old U, this integer remains invariant
under the v5.03 balancedUnit comparison. -/
def sevenTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenTotalReductionCharge s
  | .trans s t => sevenTotalReductionCharge s + sevenTotalReductionCharge t
  | .congrInv s => sevenTotalReductionCharge s
  | .congrComp s t => sevenTotalReductionCharge s + sevenTotalReductionCharge t
  | .leftUnit _ => 1
  | .rightUnit _ => 1
  | .assoc _ _ _ => 0
  | .inverseRight _ => 1
  | .inverseLeft _ => 1
  | .doubleInverse _ => 0
  | .inverseId _ => 0
  | .inverseComp _ _ => 0

/-- All original 22 eighth-level comparison rules preserve V.
The zigzag diamond has V=2 on BOTH its independently sourced paths. -/
theorem eightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | reverseContext q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => -n) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'
  | unitLeft s => simp [sevenTotalReductionCharge]
  | unitRight s => simp [sevenTotalReductionCharge]
  | associate s t u => simp [sevenTotalReductionCharge, add_assoc]
  | cancelRight s => simp [sevenTotalReductionCharge]
  | cancelLeft s => simp [sevenTotalReductionCharge]
  | involute s => simp [sevenTotalReductionCharge]
  | inverseIdentity c => simp [sevenTotalReductionCharge]
  | inverseComposite s t =>
      simp [sevenTotalReductionCharge] <;> omega
  | inverseCongruenceIdentity c =>
      simp [sevenTotalReductionCharge]
  | inverseCongruenceChain s t =>
      simp [sevenTotalReductionCharge]
  | compositeCongruenceIdentity c d =>
      simp [sevenTotalReductionCharge]
  | compositeCongruenceChain s s' t t' =>
      simp [sevenTotalReductionCharge] <;> omega
  | interchange s t =>
      simp [sevenTotalReductionCharge] <;> omega
  | zigzagDiamond c =>
      norm_num [sevenTotalReductionCharge]

theorem triangleEightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | original q => exact eightCell_preservesTotalReductionCharge q
  | leftTriangle c d =>
      norm_num [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenTotalReductionCharge]
  | rightTriangle c d =>
      norm_num [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenTotalReductionCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem involutionEightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | previous q => exact triangleEightCell_preservesTotalReductionCharge q
  | leftOverlap c =>
      norm_num [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
        sevenTotalReductionCharge]
  | rightOverlap c =>
      norm_num [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
        sevenTotalReductionCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem inverseCompEightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InverseCompEightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | previous q => exact involutionEightCell_preservesTotalReductionCharge q
  | leftOverlap c =>
      norm_num [sevenInvCompLeftDirect, sevenInvCompLeftVia,
        sevenTotalReductionCharge]
  | rightOverlap c =>
      norm_num [sevenInvCompRightDirect, sevenInvCompRightVia,
        sevenTotalReductionCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem identityEightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | previous q => exact inverseCompEightCell_preservesTotalReductionCharge q
  | identityDouble w =>
      norm_num [sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
        sevenTotalReductionCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem unitDiamondEightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : UnitDiamondEightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | previous q => exact identityEightCell_preservesTotalReductionCharge q
  | unitDiamond w =>
      norm_num [sevenUnitDiamondLeft, sevenUnitDiamondRight,
        sevenTotalReductionCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The v5.03 NEW balancedUnit primitive preserves this genuinely
different integer value, even while destroying old integer U. -/
theorem sevenBalancedUnitInvisible_totalValues (w : W) :
    sevenTotalReductionCharge
        (sevenBalancedUnitInvisibleFirst (long := long) (short := short) w) = 3 ∧
    sevenTotalReductionCharge
        (sevenBalancedUnitInvisibleSecond (long := long) (short := short) w) = 3 := by
  constructor <;>
    norm_num [sevenBalancedUnitInvisibleFirst,
      sevenBalancedUnitInvisibleSecond,
      sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
      sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
      sevenTotalReductionCharge]

theorem balancedUnitEightCell_preservesTotalReductionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : BalancedUnitEightCell W long short s t) :
    sevenTotalReductionCharge s = sevenTotalReductionCharge t := by
  induction q with
  | previous q => exact unitDiamondEightCell_preservesTotalReductionCharge q
  | balancedUnit w =>
      exact (sevenBalancedUnitInvisible_totalValues
        (long := long) (short := short) w).1.trans
          (sevenBalancedUnitInvisible_totalValues
            (long := long) (short := short) w).2.symm
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => sevenTotalReductionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTotalReductionCharge] using
        congrArg (fun n : ℤ => n + sevenTotalReductionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTotalReductionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The new integer observer genuinely descends into the v5.03
chosen higher-history quotient, without identifying the raw syntax. -/
def balancedUnitHistoryTotalReduction {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (balancedUnitHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenTotalReductionCharge s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact balancedUnitEightCell_preservesTotalReductionCharge q)

theorem balancedUnitHistoryTotalReduction_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    balancedUnitHistoryTotalReduction
        (balancedUnitHistoryClass (long := long) (short := short) s) =
      sevenTotalReductionCharge s :=
  rfl

/-- The raw source of an actual inverse-cancellation/composite peak.
Only the original free .refl/.trans/.symm constructors occur. -/
def compositeInverseCancelSource (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans (.trans (.refl w) (.refl w))
    (.symm (.trans (.refl w) (.refl w)))

/-- One-step cancellation of the exact six-cell composite word. -/
def sevenCompositeInverseCancelDirect (w : W) :
    SevenRewrite W long short
      (compositeInverseCancelSource (long := long) (short := short) w)
      (.refl w) :=
  .inverseRight (.trans (.refl w) (.refl w))

/-- Competing original path: expand inverseComposite; reassociate
both ways to expose two inverse cancellations; consume the middle
left unit, then cancel the remaining inverse. All steps have exact
original raw six-cell indices, not a quotient-normalized substitute. -/
def sevenCompositeInverseCancelVia (w : W) :
    SevenRewrite W long short
      (compositeInverseCancelSource (long := long) (short := short) w)
      (.refl w) :=
  let c : PentagonAdjoinedSixCell W long short w w := .refl w
  .trans
    (.congrComp (.refl (.trans c c)) (.inverseComp c c))
    (.trans
      (.assoc c c (.trans (.symm c) (.symm c)))
      (.trans
        (.congrComp (.refl c)
          (.symm (.assoc c (.symm c) (.symm c))))
        (.trans
          (.congrComp (.refl c)
            (.congrComp (.inverseRight c) (.refl (.symm c))))
          (.trans
            (.congrComp (.refl c) (.leftUnit (.symm c)))
            (.inverseRight c)))))

/-- The one-factor pair has V=1 versus V=3; its R/U parities
differ, so it alone is NOT the sought parity-invisible obstruction. -/
theorem sevenCompositeInverseCancel_values (w : W) :
    sevenTotalReductionCharge
        (sevenCompositeInverseCancelDirect (long := long) (short := short) w) = 1 ∧
    sevenTotalReductionCharge
        (sevenCompositeInverseCancelVia (long := long) (short := short) w) = 3 ∧
    sevenIdentityParity
        (sevenCompositeInverseCancelDirect (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenCompositeInverseCancelVia (long := long) (short := short) w) = 1 ∧
    sevenUnitCountParity
        (sevenCompositeInverseCancelDirect (long := long) (short := short) w) = 0 ∧
    sevenUnitCountParity
        (sevenCompositeInverseCancelVia (long := long) (short := short) w) = 1 := by
  simp [sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
    sevenTotalReductionCharge, sevenIdentityParity, sevenUnitCountParity,
    sevenIdentityBalance, sevenUnitStepCharge]

/-- Two genuinely independent, horizontally pasted copies of the
same original typed composite-inverse critical pair. -/
def sevenDoubleCompositeCancelFirst (w : W) :
    SevenRewrite W long short
      (.trans
        (compositeInverseCancelSource (long := long) (short := short) w)
        (compositeInverseCancelSource (long := long) (short := short) w))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenCompositeInverseCancelDirect w)
    (sevenCompositeInverseCancelDirect w)

def sevenDoubleCompositeCancelSecond (w : W) :
    SevenRewrite W long short
      (.trans
        (compositeInverseCancelSource (long := long) (short := short) w)
        (compositeInverseCancelSource (long := long) (short := short) w))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenCompositeInverseCancelVia w)
    (sevenCompositeInverseCancelVia w)

/-- The NEW actual parity-invisible certificate: both residual
parities are ZERO in both parallel seventh histories, while the
genuine integer V observer differs 2 versus 6. -/
theorem sevenDoubleCompositeCancel_values (w : W) :
    sevenTotalReductionCharge
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) = 2 ∧
    sevenTotalReductionCharge
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) = 6 ∧
    sevenIdentityParity
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) = 0 ∧
    sevenUnitCountParity
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) = 0 ∧
    sevenUnitCountParity
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) = 0 := by
  simp [sevenDoubleCompositeCancelFirst, sevenDoubleCompositeCancelSecond,
    sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
    sevenTotalReductionCharge, sevenIdentityParity, sevenUnitCountParity,
    sevenIdentityBalance, sevenUnitStepCharge]

theorem sevenDoubleCompositeCancel_sameParities (w : W) :
    sevenIdentityParity
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) =
      sevenIdentityParity
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) ∧
    sevenUnitCountParity
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) =
      sevenUnitCountParity
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) := by
  have h := sevenDoubleCompositeCancel_values (long := long) (short := short) w
  exact ⟨h.2.2.1.trans h.2.2.2.1.symm,
    h.2.2.2.2.1.trans h.2.2.2.2.2.symm⟩

/-- No v5.03 eighth-cell comparison is possible: its complete
grammar preserves V but this actual pair differs by FOUR. -/
theorem sevenDoubleCompositeCancel_noComparison (w : W) :
    ¬ Nonempty (BalancedUnitEightCell W long short
      (sevenDoubleCompositeCancelFirst (long := long) (short := short) w)
      (sevenDoubleCompositeCancelSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := balancedUnitEightCell_preservesTotalReductionCharge q
  have vals := sevenDoubleCompositeCancel_values (long := long) (short := short) w
  rw [vals.1, vals.2.1] at h
  norm_num at h

theorem sevenDoubleCompositeCancel_distinctClasses (w : W) :
    balancedUnitHistoryClass
        (sevenDoubleCompositeCancelFirst (long := long) (short := short) w) ≠
      balancedUnitHistoryClass
        (sevenDoubleCompositeCancelSecond (long := long) (short := short) w) := by
  intro h
  exact sevenDoubleCompositeCancel_noComparison (long := long) (short := short) w
    ((balancedUnitHistoryClass_eq_iff _ _).1 h)

/-- Simultaneous equality of BOTH surviving Bool observers is
INSUFFICIENT for general comparison in the v5.03 chosen grammar. -/
theorem sevenDoubleParity_notCompleteForBalancedUnit (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      sevenIdentityParity s = sevenIdentityParity t →
      sevenUnitCountParity s = sevenUnitCountParity t →
        Nonempty (BalancedUnitEightCell W l r s t)) := by
  intro every
  have vals := sevenDoubleCompositeCancel_sameParities
    (long := l) (short := r) l
  exact sevenDoubleCompositeCancel_noComparison (long := l) (short := r) l
    (every
      (sevenDoubleCompositeCancelFirst (long := l) (short := r) l)
      (sevenDoubleCompositeCancelSecond (long := l) (short := r) l)
      vals.1 vals.2)

/-- Even a nonlinear function of the TWO old parity values cannot
recover V universally on all genuine original typed histories. -/
theorem sevenTotalReduction_notFactorThroughParities (l r : W) :
    ¬ ∃ F : (ℤ × ℤ) → ℤ,
      ∀ {w z : W}
        {c d : PentagonAdjoinedSixCell W l r w z}
        (s : SevenRewrite W l r c d),
        sevenTotalReductionCharge s =
          F (sevenIdentityParity s, sevenUnitCountParity s) := by
  rintro ⟨F, factor⟩
  have h₁ := factor (sevenDoubleCompositeCancelFirst (long := l) (short := r) l)
  have h₂ := factor (sevenDoubleCompositeCancelSecond (long := l) (short := r) l)
  have hp := sevenDoubleCompositeCancel_sameParities (long := l) (short := r) l
  have hEq :
      sevenTotalReductionCharge
          (sevenDoubleCompositeCancelFirst (long := l) (short := r) l) =
        sevenTotalReductionCharge
          (sevenDoubleCompositeCancelSecond (long := l) (short := r) l) := by
    calc
      _ = F (sevenIdentityParity
            (sevenDoubleCompositeCancelFirst (long := l) (short := r) l),
            sevenUnitCountParity
            (sevenDoubleCompositeCancelFirst (long := l) (short := r) l)) := h₁
      _ = F (sevenIdentityParity
            (sevenDoubleCompositeCancelSecond (long := l) (short := r) l),
            sevenUnitCountParity
            (sevenDoubleCompositeCancelSecond (long := l) (short := r) l)) :=
        congrArg F (Prod.ext hp.1 hp.2)
      _ = _ := h₂.symm
  have vals := sevenDoubleCompositeCancel_values (long := l) (short := r) l
  rw [vals.1, vals.2.1] at hEq
  norm_num at hEq

/-- Paste the two-copy obstruction along an arbitrary ORIGINAL
P77/GK5CG-source six-cell, preserving exact source/target raw indices. -/
def sevenDoubleCompositeSourceFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w)) c)
      (.trans (.trans (.refl w) (.refl w)) c) :=
  .congrComp (sevenDoubleCompositeCancelFirst w) (.refl c)

def sevenDoubleCompositeSourceSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans
        (.trans
          (compositeInverseCancelSource (long := long) (short := short) w)
          (compositeInverseCancelSource (long := long) (short := short) w)) c)
      (.trans (.trans (.refl w) (.refl w)) c) :=
  .congrComp (sevenDoubleCompositeCancelSecond w) (.refl c)

theorem sevenDoubleCompositeSource_values {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    (sevenIdentityParity (sevenDoubleCompositeSourceFirst c) =
       sevenIdentityParity (sevenDoubleCompositeSourceSecond c) ∧
     sevenUnitCountParity (sevenDoubleCompositeSourceFirst c) =
       sevenUnitCountParity (sevenDoubleCompositeSourceSecond c)) ∧
    (sevenTotalReductionCharge (sevenDoubleCompositeSourceFirst c) = 2 ∧
     sevenTotalReductionCharge (sevenDoubleCompositeSourceSecond c) = 6) := by
  constructor
  · simpa [sevenDoubleCompositeSourceFirst, sevenDoubleCompositeSourceSecond,
      sevenIdentityParity, sevenUnitCountParity, sevenIdentityBalance,
      sevenUnitStepCharge] using
        (sevenDoubleCompositeCancel_sameParities
          (long := long) (short := short) w)
  · constructor <;>
      norm_num [sevenDoubleCompositeSourceFirst, sevenDoubleCompositeSourceSecond,
        sevenTotalReductionCharge,
        (sevenDoubleCompositeCancel_values (long := long) (short := short) w).1,
        (sevenDoubleCompositeCancel_values (long := long) (short := short) w).2.1]

theorem sevenDoubleCompositeSource_noComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (BalancedUnitEightCell W long short
      (sevenDoubleCompositeSourceFirst c)
      (sevenDoubleCompositeSourceSecond c)) := by
  rintro ⟨q⟩
  have h := balancedUnitEightCell_preservesTotalReductionCharge q
  have vals := (sevenDoubleCompositeSource_values c).2
  rw [vals.1, vals.2] at h
  norm_num at h

end PentagonAdjoinedSixCell

section ActualOriginalP77DoubleCompositeResidual
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

/-- At EVERY genuine P77 final raw index, BOTH v5.03 residual
Bool observers agree on two true typed original seventh histories,
yet the full existing eighth grammar cannot compare them. The actual
GK5CG five-cell source and its original strict Eq no-go are retained. -/
theorem pentagonActualDoubleCompositeResidualWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      (PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c) =
        PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c) ∧
       PentagonAdjoinedSixCell.sevenUnitCountParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c) =
        PentagonAdjoinedSixCell.sevenUnitCountParity
          (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.BalancedUnitEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst c)
        (PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    (PentagonAdjoinedSixCell.sevenDoubleCompositeSource_values _).1,
    PentagonAdjoinedSixCell.sevenDoubleCompositeSource_noComparison _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sixRawShapeWeight
#print axioms PentagonAdjoinedSixCell.sevenRawBoundaryParitySound
#print axioms PentagonAdjoinedSixCell.sevenParallelBoundaryParity
#print axioms PentagonAdjoinedSixCell.sevenParallelParityCoupling
#print axioms PentagonAdjoinedSixCell.sevenTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.eightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.involutionEightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.identityEightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.sevenBalancedUnitInvisible_totalValues
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_preservesTotalReductionCharge
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryTotalReduction
#print axioms PentagonAdjoinedSixCell.balancedUnitHistoryTotalReduction_onClass
#print axioms PentagonAdjoinedSixCell.compositeInverseCancelSource
#print axioms PentagonAdjoinedSixCell.sevenCompositeInverseCancelDirect
#print axioms PentagonAdjoinedSixCell.sevenCompositeInverseCancelVia
#print axioms PentagonAdjoinedSixCell.sevenCompositeInverseCancel_values
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancelFirst
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancelSecond
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancel_values
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancel_sameParities
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancel_noComparison
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeCancel_distinctClasses
#print axioms PentagonAdjoinedSixCell.sevenDoubleParity_notCompleteForBalancedUnit
#print axioms PentagonAdjoinedSixCell.sevenTotalReduction_notFactorThroughParities
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeSourceFirst
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeSourceSecond
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeSource_values
#print axioms PentagonAdjoinedSixCell.sevenDoubleCompositeSource_noComparison
#print axioms pentagonActualDoubleCompositeResidualWithSourceObstruction

end ActualOriginalP77DoubleCompositeResidual
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
