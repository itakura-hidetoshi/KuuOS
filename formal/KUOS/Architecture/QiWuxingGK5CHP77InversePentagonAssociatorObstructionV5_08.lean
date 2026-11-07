import KUOS.Architecture.QiWuxingGK5CHP77MixedResidueBalancedUnitSupplementV5_07

/-!
Qi v5.08 — ORIGINAL FREE-ASSOCIATOR FIVEFOLD PATH OBSTRUCTION.

For four actual six-cell words alternating the original adjoined pentagon
generator and its inverse, construct the two classical pentagon pasting
routes as ORIGINAL SevenRewrite values. Their source and target are
strictly the SAME free six-cell words; no six-cell quotient is used.

A new structure-sensitive integer fingerprint counts exactly the
associator redex (symm pentagon, pentagon, symm pentagon). This is
NOT the old total T charge; the marker respects even the v4.91
zigzagDiamond (c,symm c,c) and both v4.93 unit-triangle generators.
All actual chosen comparison constructors through Qi v5.07, including
the one mixedResidue generator, preserve the marker by COMPLETE
structural induction over all old and new higher presentations.
The two fourfold pasting routes have marker values 1 and 0, so
the CURRENT MixedResidueEightCell cannot join them.

Yet the remaining V mod2, R mod2, U mod2 observations coincide, all
equal 0. Their equality is therefore NOT a complete characterization
of the current chosen eighth comparison relation.

No arbitrary parallel-history thinness, no new ninth cell, no added
higher comparison primitive, no source strict equality. The abstract
counterexample works for any original l,r and so specializes to
EVERY genuinely sourced P77/GK5CG final raw index using the same
definitional original adjoined pentagon generator.

append-only / tighten-only / overwrite-forbidden / same-root, root107;
Lean v4.30.0-rc2, pinned mathlib
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

/-- The exact original free pentagon constructor, not an arbitrary
six-cell of matching degree. -/
def sixIsRawPentagon {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) : Bool :=
  match c with
  | .pentagon => true
  | _ => false

/-- Exactly one raw inverse of the original pentagon; note that a
DOUBLE inverse is a different unquotiented six-cell constructor. -/
def sixIsRawInversePentagon {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) : Bool :=
  match c with
  | .symm d => sixIsRawPentagon d
  | _ => false

/-- Typed local associator fingerprint; the ONLY nonzero atomic
redex is assoc (symm pentagon) pentagon (symm pentagon).
This is deliberately much finer than the old uniform T count. -/
def sevenInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenInversePentagonAssociatorCharge s
  | .trans s t =>
      sevenInversePentagonAssociatorCharge s +
        sevenInversePentagonAssociatorCharge t
  | .congrInv s => sevenInversePentagonAssociatorCharge s
  | .congrComp s t =>
      sevenInversePentagonAssociatorCharge s +
        sevenInversePentagonAssociatorCharge t
  | .leftUnit _ => 0
  | .rightUnit _ => 0
  | .assoc c d e =>
      if sixIsRawInversePentagon c && sixIsRawPentagon d &&
          sixIsRawInversePentagon e then 1 else 0
  | .inverseRight _ => 0
  | .inverseLeft _ => 0
  | .doubleInverse _ => 0
  | .inverseId _ => 0
  | .inverseComp _ _ => 0

/-- All 22 original v4.91 comparison constructors preserve the
shape-sensitive fingerprint. In particular zigzagDiamond compares
assoc(c,symm(c),c), NEVER our exact inverse/pentagon/inverse triple. -/
theorem eightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | reverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ => -n) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'
  | unitLeft s => simp [sevenInversePentagonAssociatorCharge]
  | unitRight s => simp [sevenInversePentagonAssociatorCharge]
  | associate s t u =>
      simp [sevenInversePentagonAssociatorCharge, add_assoc]
  | cancelRight s => simp [sevenInversePentagonAssociatorCharge]
  | cancelLeft s => simp [sevenInversePentagonAssociatorCharge]
  | involute s => simp [sevenInversePentagonAssociatorCharge]
  | inverseIdentity c => simp [sevenInversePentagonAssociatorCharge]
  | inverseComposite s t =>
      simp [sevenInversePentagonAssociatorCharge] <;> abel
  | inverseCongruenceIdentity c =>
      simp [sevenInversePentagonAssociatorCharge]
  | inverseCongruenceChain s t =>
      simp [sevenInversePentagonAssociatorCharge]
  | compositeCongruenceIdentity c d =>
      simp [sevenInversePentagonAssociatorCharge]
  | compositeCongruenceChain s s' t t' =>
      simp [sevenInversePentagonAssociatorCharge] <;> abel
  | interchange s t =>
      simp [sevenInversePentagonAssociatorCharge] <;> abel
  | zigzagDiamond c =>
      simp [sevenInversePentagonAssociatorCharge,
        sixIsRawInversePentagon, sixIsRawPentagon]

theorem triangleEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | original q => exact eightCell_preservesInversePentagonAssociatorCharge q
  | leftTriangle c d =>
      simp [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenInversePentagonAssociatorCharge,
        sixIsRawInversePentagon]
  | rightTriangle c d =>
      simp [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenInversePentagonAssociatorCharge,
        sixIsRawInversePentagon]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem involutionEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact triangleEightCell_preservesInversePentagonAssociatorCharge q
  | leftOverlap c =>
      simp [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
        sevenInversePentagonAssociatorCharge]
  | rightOverlap c =>
      simp [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
        sevenInversePentagonAssociatorCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem inverseCompEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InverseCompEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact involutionEightCell_preservesInversePentagonAssociatorCharge q
  | leftOverlap c =>
      simp [sevenInvCompLeftDirect, sevenInvCompLeftVia,
        sevenInversePentagonAssociatorCharge]
  | rightOverlap c =>
      simp [sevenInvCompRightDirect, sevenInvCompRightVia,
        sevenInversePentagonAssociatorCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem identityEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact inverseCompEightCell_preservesInversePentagonAssociatorCharge q
  | identityDouble w =>
      simp [sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
        sevenInversePentagonAssociatorCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem unitDiamondEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : UnitDiamondEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact identityEightCell_preservesInversePentagonAssociatorCharge q
  | unitDiamond w =>
      simp [sevenUnitDiamondLeft, sevenUnitDiamondRight,
        sevenInversePentagonAssociatorCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem balancedUnitEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : BalancedUnitEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact unitDiamondEightCell_preservesInversePentagonAssociatorCharge q
  | balancedUnit w =>
      simp [sevenBalancedUnitInvisibleFirst,
        sevenBalancedUnitInvisibleSecond,
        sevenBalancedInverseUnitFirst, sevenBalancedInverseUnitSecond,
        sevenInverseUnitLeftDirect, sevenInverseUnitLeftVia,
        sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
        sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenInversePentagonAssociatorCharge,
        sixIsRawInversePentagon]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem doubleCompositeEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : DoubleCompositeEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact balancedUnitEightCell_preservesInversePentagonAssociatorCharge q
  | doubleComposite w =>
      simp [sevenDoubleCompositeCancelFirst,
        sevenDoubleCompositeCancelSecond,
        sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
        sevenInversePentagonAssociatorCharge,
        sixIsRawInversePentagon]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

theorem sevenMixedResidue_inversePentagonAssociatorValues (w : W) :
    sevenInversePentagonAssociatorCharge
      (sevenMixedResidueFirst (long := long) (short := short) w) = 0 ∧
    sevenInversePentagonAssociatorCharge
      (sevenMixedResidueSecond (long := long) (short := short) w) = 0 := by
  constructor <;>
    simp [sevenMixedResidueFirst, sevenMixedResidueSecond,
      sevenMixedCancellationFirst, sevenMixedCancellationSecond,
      sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenInvCompLeftVia, sevenInvCompLeftDirect,
      sevenInversePentagonAssociatorCharge,
      sixIsRawInversePentagon]

/-- The COMPLETE current eighth presentation preserves the original
raw associator fingerprint, including its ONE new mixedResidue and
all inherited eighth comparison constructors and typed contexts. -/
theorem mixedResidueEightCell_preservesInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    sevenInversePentagonAssociatorCharge s =
      sevenInversePentagonAssociatorCharge t := by
  induction q with
  | previous q =>
      exact doubleCompositeEightCell_preservesInversePentagonAssociatorCharge q
  | mixedResidue w =>
      have vals := sevenMixedResidue_inversePentagonAssociatorValues
        (long := long) (short := short) w
      exact vals.1.trans vals.2.symm
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          sevenInversePentagonAssociatorCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg (fun n : ℤ =>
          n + sevenInversePentagonAssociatorCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInversePentagonAssociatorCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInversePentagonAssociatorCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- It genuinely descends to the currently selected history quotient;
this is NOT descent of the actual original source six-cell value. -/
def mixedResidueHistoryInversePentagonAssociatorCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      sevenInversePentagonAssociatorCharge s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact mixedResidueEightCell_preservesInversePentagonAssociatorCharge q)

theorem mixedResidueHistoryInversePentagonAssociatorCharge_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryInversePentagonAssociatorCharge
      (mixedResidueHistoryClass (long := long) (short := short) s) =
    sevenInversePentagonAssociatorCharge s := rfl

/-- Four alternating copies of the ACTUAL adjoined pentagon and inverse.
The source and target are original FREE six-cell words at short. -/
def fourfoldInversePentagonSource (l r : W) :
    PentagonAdjoinedSixCell W l r r r :=
  .trans
    (.trans (.trans (.symm .pentagon) .pentagon) (.symm .pentagon))
    .pentagon

def fourfoldInversePentagonTarget (l r : W) :
    PentagonAdjoinedSixCell W l r r r :=
  .trans (.symm .pentagon)
    (.trans .pentagon (.trans (.symm .pentagon) .pentagon))

/-- Three-associator (upper) route in the genuine Stasheff pentagon. -/
def sevenFourfoldInversePentagonThree (l r : W) :
    SevenRewrite W l r
      (fourfoldInversePentagonSource l r)
      (fourfoldInversePentagonTarget l r) := by
  let a : PentagonAdjoinedSixCell W l r r l := .symm .pentagon
  let b : PentagonAdjoinedSixCell W l r l r := .pentagon
  let c : PentagonAdjoinedSixCell W l r r l := .symm .pentagon
  let d : PentagonAdjoinedSixCell W l r l r := .pentagon
  exact .trans
    (.congrComp (.assoc a b c) (.refl d))
    (.trans
      (.assoc a (.trans b c) d)
      (.congrComp (.refl a) (.assoc b c d)))

/-- Two-associator (lower) route with exactly the SAME free endpoints. -/
def sevenFourfoldInversePentagonTwo (l r : W) :
    SevenRewrite W l r
      (fourfoldInversePentagonSource l r)
      (fourfoldInversePentagonTarget l r) := by
  let a : PentagonAdjoinedSixCell W l r r l := .symm .pentagon
  let b : PentagonAdjoinedSixCell W l r l r := .pentagon
  let c : PentagonAdjoinedSixCell W l r r l := .symm .pentagon
  let d : PentagonAdjoinedSixCell W l r l r := .pentagon
  exact .trans
    (.assoc (.trans a b) c d)
    (.assoc a b (.trans c d))

/-- The exact local associator fingerprint detects 1 vs 0. -/
theorem sevenFourfoldInversePentagon_chargeValues (l r : W) :
    sevenInversePentagonAssociatorCharge
      (sevenFourfoldInversePentagonThree l r) = 1 ∧
    sevenInversePentagonAssociatorCharge
      (sevenFourfoldInversePentagonTwo l r) = 0 := by
  constructor <;>
    norm_num [sevenFourfoldInversePentagonThree,
      sevenFourfoldInversePentagonTwo,
      sevenInversePentagonAssociatorCharge,
      sixIsRawInversePentagon, sixIsRawPentagon]

/-- Both genuine paths are completely invisible to the residual
V mod2 and two coupled R/U parity observers. -/
theorem sevenFourfoldInversePentagon_sameResiduals (l r : W) :
    sevenTotalReductionParity
        (sevenFourfoldInversePentagonThree l r) =
      sevenTotalReductionParity
        (sevenFourfoldInversePentagonTwo l r) ∧
    sevenIdentityParity
        (sevenFourfoldInversePentagonThree l r) =
      sevenIdentityParity
        (sevenFourfoldInversePentagonTwo l r) ∧
    sevenUnitCountParity
        (sevenFourfoldInversePentagonThree l r) =
      sevenUnitCountParity
        (sevenFourfoldInversePentagonTwo l r) := by
  simp [sevenFourfoldInversePentagonThree, sevenFourfoldInversePentagonTwo,
    sevenTotalReductionParity, sevenTotalReductionResidue,
    sevenTotalReductionCharge, sevenIdentityParity, sevenIdentityBalance,
    sevenUnitCountParity, sevenUnitStepCharge]

/-- The CURRENT entire Qi v5.07 eighth comparison grammar cannot
fill the genuine fourfold associator pentagon. The impossibility is
proved from full-constructor conservation, not from search failure. -/
theorem sevenFourfoldInversePentagon_noMixedResidueComparison (l r : W) :
    ¬ Nonempty (MixedResidueEightCell W l r
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonTwo l r)) := by
  rintro ⟨q⟩
  have h := mixedResidueEightCell_preservesInversePentagonAssociatorCharge q
  have vals := sevenFourfoldInversePentagon_chargeValues l r
  rw [vals.1, vals.2] at h
  norm_num at h

theorem sevenFourfoldInversePentagon_classGap (l r : W) :
    mixedResidueHistoryClass
        (sevenFourfoldInversePentagonThree l r) ≠
      mixedResidueHistoryClass
        (sevenFourfoldInversePentagonTwo l r) := by
  intro h
  exact sevenFourfoldInversePentagon_noMixedResidueComparison l r
    ((mixedResidueHistoryClass_eq_iff _ _).1 h)

/-- Joint equality of all remaining old residual observers is NOT
sufficient to infer the current chosen higher comparison. -/
theorem mixedResidueThreeResiduals_notComplete (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      sevenTotalReductionParity s = sevenTotalReductionParity t →
      sevenIdentityParity s = sevenIdentityParity t →
      sevenUnitCountParity s = sevenUnitCountParity t →
      Nonempty (MixedResidueEightCell W l r s t)) := by
  intro hypothetical
  have h := sevenFourfoldInversePentagon_sameResiduals l r
  exact sevenFourfoldInversePentagon_noMixedResidueComparison l r
    (hypothetical
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonTwo l r)
      h.1 h.2.1 h.2.2)

/-- No (even nonlinear) recovery of the new associator fingerprint
from the triple of surviving integer residual observers is possible
over all actual original SevenRewrite histories. -/
theorem sevenInversePentagonAssociator_notFactorThroughResiduals (l r : W) :
    ¬ ∃ F : ℤ × ℤ × ℤ → ℤ,
      ∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
        (s : SevenRewrite W l r c d),
        sevenInversePentagonAssociatorCharge s =
          F (sevenTotalReductionParity s,
            sevenIdentityParity s, sevenUnitCountParity s) := by
  rintro ⟨F, factor⟩
  have h₁ := factor (sevenFourfoldInversePentagonThree l r)
  have h₂ := factor (sevenFourfoldInversePentagonTwo l r)
  have hp := sevenFourfoldInversePentagon_sameResiduals l r
  have heq :
      sevenInversePentagonAssociatorCharge
          (sevenFourfoldInversePentagonThree l r) =
        sevenInversePentagonAssociatorCharge
          (sevenFourfoldInversePentagonTwo l r) := by
    rw [h₁, h₂, hp.1, hp.2.1, hp.2.2]
  have vals := sevenFourfoldInversePentagon_chargeValues l r
  rw [vals.1, vals.2] at heq
  norm_num at heq

end PentagonAdjoinedSixCell

section ActualOriginalP77FourfoldAssocObstruction
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

/-- At EVERY genuine original P77 final raw index, the SAME actual
GK5CG-source-generated l/r values support the exact fourfold pentagon
obstruction in the independent free six/seven/eight presentation.
This preserves the strict original-source Eq interpreter obstruction. -/
theorem pentagonActualFourfoldInversePentagonObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (PentagonAdjoinedSixCell.sevenTotalReductionParity
        (PentagonAdjoinedSixCell.sevenFourfoldInversePentagonThree
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)) =
      PentagonAdjoinedSixCell.sevenTotalReductionParity
        (PentagonAdjoinedSixCell.sevenFourfoldInversePentagonTwo
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ Nonempty (PentagonAdjoinedSixCell.MixedResidueEightCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.sevenFourfoldInversePentagonThree
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.sevenFourfoldInversePentagonTwo
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨(PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_sameResiduals
      _ _).1,
    PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_noMixedResidueComparison
      _ _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sixIsRawPentagon
#print axioms PentagonAdjoinedSixCell.sixIsRawInversePentagon
#print axioms PentagonAdjoinedSixCell.sevenInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.eightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.involutionEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.identityEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.unitDiamondEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.balancedUnitEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.doubleCompositeEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_inversePentagonAssociatorValues
#print axioms PentagonAdjoinedSixCell.mixedResidueEightCell_preservesInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryInversePentagonAssociatorCharge
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryInversePentagonAssociatorCharge_onClass
#print axioms PentagonAdjoinedSixCell.fourfoldInversePentagonSource
#print axioms PentagonAdjoinedSixCell.fourfoldInversePentagonTarget
#print axioms PentagonAdjoinedSixCell.sevenFourfoldInversePentagonThree
#print axioms PentagonAdjoinedSixCell.sevenFourfoldInversePentagonTwo
#print axioms PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_chargeValues
#print axioms PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_sameResiduals
#print axioms PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_noMixedResidueComparison
#print axioms PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_classGap
#print axioms PentagonAdjoinedSixCell.mixedResidueThreeResiduals_notComplete
#print axioms PentagonAdjoinedSixCell.sevenInversePentagonAssociator_notFactorThroughResiduals
#print axioms pentagonActualFourfoldInversePentagonObstruction

end ActualOriginalP77FourfoldAssocObstruction
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
