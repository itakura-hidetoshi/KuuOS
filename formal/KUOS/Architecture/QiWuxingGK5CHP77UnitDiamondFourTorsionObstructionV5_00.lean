import KUOS.Architecture.QiWuxingGK5CHP77MixedIdentityParityDescentV4_99

/-!
Qi v5.00 — FOUR-TORSION UNIT DIAMOND BEYOND RESIDUAL PARITY.

The identity-completed v4.98 eighth-cell presentation still has a
genuine higher obstruction invisible to the v4.99 mod-two R observer.

We construct a signed integer weight on ALL thirteen constructors of
the original freely generated SevenRewrite Type, with local weights
  leftUnit=0, rightUnit=2, assoc=0,
  inverseRight=0, inverseLeft=2, doubleInverse=2,
  inverseId=1, inverseComp=1.
Its residue modulo FOUR, not the unreduced integer weight, is
preserved by EVERY original, triangle, involution, inverseComp, and
identityDouble eighth-cell constructor and its typed contexts.

At the ACTUAL common six-cell endpoints
  (refl(w) ; refl(w))  -->  refl(w),
the two genuine primitive seventh histories
  leftUnit(refl(w))  and  rightUnit(refl(w))
both have residual v4.99 identity parity zero and the SAME previously
studied three integer charges, but their four-torsion values are 0,2.
Thus NO chosen IdentityEightCell compares these histories. This
refutes parity completeness with an explicit proof, not by non-discovery.

We further paste this unit diamond against the original, genuinely
sourced P77/GK5CG six-cell generator at EVERY terminal raw index.
No previous presentation, source Type, equality authority or public
root is replaced, and NO new primitive eighth-cell is postulated.
A possible local completion is deferred until the obstruction is proved.

Append-only / tighten-only / overwrite-forbidden / same-root; root107.
Pinned Lean v4.30.0-rc2, mathlib
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

/-- Raw integer charge BEFORE reduction modulo four. It is not
claimed to descend as an integer to the chosen history quotient. -/
def sevenUnitTorsionWeight {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenUnitTorsionWeight s
  | .trans s t => sevenUnitTorsionWeight s + sevenUnitTorsionWeight t
  | .congrInv s => sevenUnitTorsionWeight s
  | .congrComp s t => sevenUnitTorsionWeight s + sevenUnitTorsionWeight t
  | .leftUnit _ => 0
  | .rightUnit _ => 2
  | .assoc _ _ _ => 0
  | .inverseRight _ => 0
  | .inverseLeft _ => 2
  | .doubleInverse _ => 2
  | .inverseId _ => 1
  | .inverseComp _ _ => 1

/-- A canonical integer representative of a Z/4Z-valued charge. -/
def sevenUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  sevenUnitTorsionWeight s % 4

/-- All 22 ORIGINAL eighth-cell rules preserve the four-torsion
charge. The zigzag diamond is essential: its weights are 0 versus 4,
so the integer weight itself would NOT be invariant. -/
theorem eightCell_preservesUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | whiskerRight q after ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | reverseContext q ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | inverseContext q ih =>
      simpa [sevenUnitTorsionResidue, sevenUnitTorsionWeight] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenUnitTorsionResidue] at ih ih' ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | unitLeft s => simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | unitRight s => simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | associate s t u =>
      simp only [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
      omega
  | cancelRight s =>
      simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | cancelLeft s =>
      simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | involute s =>
      simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | inverseIdentity c =>
      simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | inverseComposite s t =>
      simp only [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
      omega
  | inverseCongruenceIdentity c =>
      simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | inverseCongruenceChain s t =>
      simp only [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
      omega
  | compositeCongruenceIdentity c d =>
      simp [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | compositeCongruenceChain s s' t t' =>
      simp only [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
      omega
  | interchange s t =>
      simp only [sevenUnitTorsionResidue, sevenUnitTorsionWeight]
      omega
  | zigzagDiamond c =>
      norm_num [sevenUnitTorsionResidue, sevenUnitTorsionWeight]

/-- Both triangle/unit critical comparisons preserve the four-torsion
charge, even though they destroy the original T coordinate. -/
theorem triangleEightCell_preservesUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t := by
  induction q with
  | original q => exact eightCell_preservesUnitTorsionResidue q
  | leftTriangle c d =>
      norm_num [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | rightTriangle c d =>
      norm_num [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | whiskerRight q after ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | inverseContext q ih =>
      simpa [sevenUnitTorsionResidue, sevenUnitTorsionWeight] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenUnitTorsionResidue] at ih ih' ⊢
      simp only [sevenUnitTorsionWeight]
      omega

/-- Both inverse/cancellation overlaps respect the torsion residue;
on the right peak the integer charges differ by four. -/
theorem involutionEightCell_preservesUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t := by
  induction q with
  | previous q => exact triangleEightCell_preservesUnitTorsionResidue q
  | leftOverlap c =>
      norm_num [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | rightOverlap c =>
      norm_num [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | whiskerRight q after ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | inverseContext q ih =>
      simpa [sevenUnitTorsionResidue, sevenUnitTorsionWeight] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenUnitTorsionResidue] at ih ih' ⊢
      simp only [sevenUnitTorsionWeight]
      omega

/-- Both inverseComp/unit comparisons preserve the residue, even
where the integer weights jump by four on the left peak. -/
theorem inverseCompEightCell_preservesUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InverseCompEightCell W long short s t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t := by
  induction q with
  | previous q => exact involutionEightCell_preservesUnitTorsionResidue q
  | leftOverlap c =>
      norm_num [sevenInvCompLeftDirect, sevenInvCompLeftVia,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | rightOverlap c =>
      norm_num [sevenInvCompRightDirect, sevenInvCompRightVia,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | whiskerRight q after ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | inverseContext q ih =>
      simpa [sevenUnitTorsionResidue, sevenUnitTorsionWeight] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenUnitTorsionResidue] at ih ih' ⊢
      simp only [sevenUnitTorsionWeight]
      omega

/-- The full chosen IdentityEightCell grammar, INCLUDING the only
new identityDouble generator and ALL contexts, preserves Z/4Z. -/
theorem identityEightCell_preservesUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t := by
  induction q with
  | previous q =>
      exact inverseCompEightCell_preservesUnitTorsionResidue q
  | identityDouble w =>
      norm_num [sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | whiskerRight q after ih =>
      simp only [sevenUnitTorsionResidue] at ih ⊢
      simp only [sevenUnitTorsionWeight]
      omega
  | inverseContext q ih =>
      simpa [sevenUnitTorsionResidue, sevenUnitTorsionWeight] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenUnitTorsionResidue] at ih ih' ⊢
      simp only [sevenUnitTorsionWeight]
      omega

/-- The four-torsion charge genuinely descends to the final chosen
quotient, unlike the original unreduced R integer. -/
theorem identityHistoryClass_eq_preservesUnitTorsionResidue {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : identityHistoryClass s = identityHistoryClass t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t := by
  rcases (identityHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact identityEightCell_preservesUnitTorsionResidue q

/-- Quotient.lift of the four-torsion observable, without identifying
either raw seventh histories or original GK5CG source equality. -/
def identityHistoryUnitTorsion {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (identityHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenUnitTorsionResidue s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact identityEightCell_preservesUnitTorsionResidue q)

theorem identityHistoryUnitTorsion_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    identityHistoryUnitTorsion
      (identityHistoryClass (long := long) (short := short) s) =
      sevenUnitTorsionResidue s :=
  rfl

/-- Degenerate but genuinely typed LEFT unit history, with the
ACTUAL common six-cell endpoints refl(w);refl(w) --> refl(w). -/
def sevenUnitDiamondLeft (w : W) :
    SevenRewrite W long short
      (.trans (.refl w) (.refl w)) (.refl w) :=
  .leftUnit (.refl w)

/-- A DIFFERENT right-unit history, not a definitional identification
or a newly invented higher comparison. -/
def sevenUnitDiamondRight (w : W) :
    SevenRewrite W long short
      (.trans (.refl w) (.refl w)) (.refl w) :=
  .rightUnit (.refl w)

/-- A certified difference of exactly two in Z/4Z. -/
theorem sevenUnitDiamond_torsionValues (w : W) :
    sevenUnitTorsionResidue
        (sevenUnitDiamondLeft (long := long) (short := short) w) = 0 ∧
    sevenUnitTorsionResidue
        (sevenUnitDiamondRight (long := long) (short := short) w) = 2 := by
  constructor <;>
    norm_num [sevenUnitDiamondLeft, sevenUnitDiamondRight,
      sevenUnitTorsionResidue, sevenUnitTorsionWeight]

/-- Both histories are invisible to the v4.99 residual parity. -/
theorem sevenUnitDiamond_parityValues (w : W) :
    sevenIdentityParity
        (sevenUnitDiamondLeft (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenUnitDiamondRight (long := long) (short := short) w) = 0 := by
  constructor <;>
    norm_num [sevenUnitDiamondLeft, sevenUnitDiamondRight,
      sevenIdentityParity, sevenIdentityBalance]

theorem sevenUnitDiamond_sameParity (w : W) :
    sevenIdentityParity
        (sevenUnitDiamondLeft (long := long) (short := short) w) =
      sevenIdentityParity
        (sevenUnitDiamondRight (long := long) (short := short) w) := by
  exact (sevenUnitDiamond_parityValues (long := long) (short := short) w).1.trans
    (sevenUnitDiamond_parityValues (long := long) (short := short) w).2.symm

/-- Even the older T,J,K triple agrees: the obstruction belongs
to a genuinely different (torsion) observation. -/
theorem sevenUnitDiamond_sameTriple (w : W) :
    sevenChargeTriple
        (sevenUnitDiamondLeft (long := long) (short := short) w) =
      sevenChargeTriple
        (sevenUnitDiamondRight (long := long) (short := short) w) := by
  simp [sevenUnitDiamondLeft, sevenUnitDiamondRight,
    sevenChargeTriple, sevenTriangleCharge,
    sevenInvolutionCharge, sevenInverseCompCharge]

/-- No v4.98 IdentityEightCell exists: EVERY possible constructor of
that grammar conserves four-torsion, but the two witnesses differ. -/
theorem sevenUnitDiamond_noIdentityComparison (w : W) :
    ¬ Nonempty (IdentityEightCell W long short
      (sevenUnitDiamondLeft (long := long) (short := short) w)
      (sevenUnitDiamondRight (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have hv := identityEightCell_preservesUnitTorsionResidue q
  have vals := sevenUnitDiamond_torsionValues (long := long) (short := short) w
  rw [vals.1, vals.2] at hv
  norm_num at hv

theorem sevenUnitDiamond_distinctIdentityClasses (w : W) :
    identityHistoryClass
        (sevenUnitDiamondLeft (long := long) (short := short) w) ≠
      identityHistoryClass
        (sevenUnitDiamondRight (long := long) (short := short) w) := by
  intro h
  exact sevenUnitDiamond_noIdentityComparison (long := long) (short := short) w
    ((identityHistoryClass_eq_iff _ _).1 h)

/-- Residual parity equality is NOT sufficient for chosen eighth-cell
comparison, even for two honest histories of the same raw endpoints. -/
theorem sevenIdentityParity_notCompleteForIdentity (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      sevenIdentityParity s = sevenIdentityParity t →
        Nonempty (IdentityEightCell W l r s t)) := by
  intro all
  exact sevenUnitDiamond_noIdentityComparison (long := l) (short := r) l
    (all
      (sevenUnitDiamondLeft (long := l) (short := r) l)
      (sevenUnitDiamondRight (long := l) (short := r) l)
      (sevenUnitDiamond_sameParity (long := l) (short := r) l))

/-- No possibly nonlinear function of the parity observer alone
recovers the new four-torsion observation on ALL typed histories. -/
theorem sevenUnitTorsion_notFactorThroughParity (l r : W) :
    ¬ ∃ F : ℤ → ℤ,
      ∀ {w z : W}
        {c d : PentagonAdjoinedSixCell W l r w z}
        (s : SevenRewrite W l r c d),
        sevenUnitTorsionResidue s = F (sevenIdentityParity s) := by
  rintro ⟨F, factor⟩
  have h₁ := factor (sevenUnitDiamondLeft (long := l) (short := r) l)
  have h₂ := factor (sevenUnitDiamondRight (long := l) (short := r) l)
  have hp := sevenUnitDiamond_sameParity (long := l) (short := r) l
  have heq :
      sevenUnitTorsionResidue
          (sevenUnitDiamondLeft (long := l) (short := r) l) =
        sevenUnitTorsionResidue
          (sevenUnitDiamondRight (long := l) (short := r) l) := by
    calc
      _ = F (sevenIdentityParity
            (sevenUnitDiamondLeft (long := l) (short := r) l)) := h₁
      _ = F (sevenIdentityParity
            (sevenUnitDiamondRight (long := l) (short := r) l)) := congrArg F hp
      _ = _ := h₂.symm
  have vals := sevenUnitDiamond_torsionValues (long := l) (short := r) l
  rw [vals.1, vals.2] at heq
  norm_num at heq

/-- A genuinely sourced composite context: paste either identity
unit reduction with the SAME original six-cell arrow c. -/
def sevenUnitDiamondCompositeLeft {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) (.refl w)) c)
      (.trans (.refl w) c) :=
  .congrComp (sevenUnitDiamondLeft w) (.refl c)

def sevenUnitDiamondCompositeRight {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) (.refl w)) c)
      (.trans (.refl w) c) :=
  .congrComp (sevenUnitDiamondRight w) (.refl c)

/-- Contextualized at an ORIGINAL six-cell source, the residue gap
survives and the v4.99 parity still agrees. -/
theorem sevenUnitDiamondComposite_torsionAndParity {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    (sevenUnitTorsionResidue (sevenUnitDiamondCompositeLeft c) = 0 ∧
     sevenUnitTorsionResidue (sevenUnitDiamondCompositeRight c) = 2) ∧
    sevenIdentityParity (sevenUnitDiamondCompositeLeft c) =
      sevenIdentityParity (sevenUnitDiamondCompositeRight c) := by
  constructor
  · constructor <;>
      norm_num [sevenUnitDiamondCompositeLeft, sevenUnitDiamondCompositeRight,
        sevenUnitDiamondLeft, sevenUnitDiamondRight,
        sevenUnitTorsionResidue, sevenUnitTorsionWeight]
  · simp [sevenUnitDiamondCompositeLeft, sevenUnitDiamondCompositeRight,
      sevenUnitDiamondLeft, sevenUnitDiamondRight,
      sevenIdentityParity, sevenIdentityBalance]

theorem sevenUnitDiamondComposite_noIdentityComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (IdentityEightCell W long short
      (sevenUnitDiamondCompositeLeft c)
      (sevenUnitDiamondCompositeRight c)) := by
  rintro ⟨q⟩
  have hv := identityEightCell_preservesUnitTorsionResidue q
  have vals := (sevenUnitDiamondComposite_torsionAndParity c).1
  rw [vals.1, vals.2] at hv
  norm_num at hv

end PentagonAdjoinedSixCell

section ActualOriginalP77UnitDiamondFourTorsion
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

/-- At EVERY original P77 terminal raw index, the genuine GK5CG
six-cell generator yields a contextual unit diamond with identical
residual parity but NO v4.98 eighth-cell comparison. The independent
original source equality interpreter remains impossible. -/
theorem pentagonActualUnitDiamondFourTorsionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeLeft c) =
        PentagonAdjoinedSixCell.sevenIdentityParity
          (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeRight c) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.IdentityEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeLeft c)
        (PentagonAdjoinedSixCell.sevenUnitDiamondCompositeRight c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    (PentagonAdjoinedSixCell.sevenUnitDiamondComposite_torsionAndParity _).2,
    PentagonAdjoinedSixCell.sevenUnitDiamondComposite_noIdentityComparison _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sevenUnitTorsionWeight
#print axioms PentagonAdjoinedSixCell.sevenUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.eightCell_preservesUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.involutionEightCell_preservesUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_preservesUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.identityEightCell_preservesUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_eq_preservesUnitTorsionResidue
#print axioms PentagonAdjoinedSixCell.identityHistoryUnitTorsion
#print axioms PentagonAdjoinedSixCell.identityHistoryUnitTorsion_onClass
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamondLeft
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamondRight
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamond_torsionValues
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamond_parityValues
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamond_sameParity
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamond_sameTriple
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamond_noIdentityComparison
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamond_distinctIdentityClasses
#print axioms PentagonAdjoinedSixCell.sevenIdentityParity_notCompleteForIdentity
#print axioms PentagonAdjoinedSixCell.sevenUnitTorsion_notFactorThroughParity
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamondCompositeLeft
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamondCompositeRight
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamondComposite_torsionAndParity
#print axioms PentagonAdjoinedSixCell.sevenUnitDiamondComposite_noIdentityComparison
#print axioms pentagonActualUnitDiamondFourTorsionWithSourceObstruction

end ActualOriginalP77UnitDiamondFourTorsion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
