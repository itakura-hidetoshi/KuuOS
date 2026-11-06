import KUOS.Architecture.QiWuxingGK5CHP77ThreeChargeFiltrationRigidityV4_96

/-!
Qi v4.97 — THREE-CHARGE-INVISIBLE CRITICAL PEAKS AND IDENTITY BALANCE.

A fourth signed observation on the original THIRTEEN-constructor
SevenRewrite syntax counts inverseId positively and inverseComp
negatively. The two new v4.95 inverse-composition/unit peaks have
one of EACH on the long branch, so this balance is conserved by
every v4.95 InverseCompEightCell constructor.

We construct two explicit parallel seventh histories by putting
three independent genuine overlaps into three typed six-cell factors:
  * doubleInverse(refl) versus two inverseId reductions;
  * the existing left double-inverse/cancellation overlap;
  * the existing left triangle/unit/associator overlap.
Their T,J,K triples coincide, but their new balance values are 0
and 2. Consequently NO eighth-cell comparison in the COMPLETE
v4.95 chosen higher grammar joins these particular histories.
Even an arbitrary nonlinear map out of the triple cannot recover
this fourth charge on all raw seventh histories.

In contrast, a two-inverseId interchange is positively joined by
the already existing ORIGINAL EightCell.interchange constructor.
Thus joinability and a certified obstruction are kept separate.

The source is the unchanged GK5CG original five-cell Type. No
new eighth-cell constructor, nine-cell, source equality, quotient
replacement, or universal thinness is assumed or added.
Append-only / tighten-only / same-root; public root107.
Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Signed identity/composition balance on RAW seven-cell histories.
The opposite weights are essential: the old v4.95 overlap spends
one inverseComp together with one inverseId. -/
def sevenIdentityBalance {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenIdentityBalance s
  | .trans s t => sevenIdentityBalance s + sevenIdentityBalance t
  | .congrInv s => sevenIdentityBalance s
  | .congrComp s t => sevenIdentityBalance s + sevenIdentityBalance t
  | .leftUnit _ => 0
  | .rightUnit _ => 0
  | .assoc _ _ _ => 0
  | .inverseRight _ => 0
  | .inverseLeft _ => 0
  | .doubleInverse _ => 0
  | .inverseId _ => 1
  | .inverseComp _ _ => -1

/-- All original twenty-two eighth-level rules conserve identity
balance. In particular the interchange and zigzag diamond are
checked, not assumed. -/
theorem eightCell_preservesIdentityBalance {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenIdentityBalance s = sevenIdentityBalance t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => sevenIdentityBalance before + v) ih
  | whiskerRight q after ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => v + sevenIdentityBalance after) ih
  | reverseContext q ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => -v) ih
  | inverseContext q ih =>
      simpa [sevenIdentityBalance] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenIdentityBalance] using
        congrArg₂ (fun v u : ℤ => v + u) ih ih'
  | unitLeft s => simp [sevenIdentityBalance]
  | unitRight s => simp [sevenIdentityBalance]
  | associate s t u => simp [sevenIdentityBalance, add_assoc]
  | cancelRight s => simp [sevenIdentityBalance]
  | cancelLeft s => simp [sevenIdentityBalance]
  | involute s => simp [sevenIdentityBalance]
  | inverseIdentity c => simp [sevenIdentityBalance]
  | inverseComposite s t =>
      simp [sevenIdentityBalance] <;> abel
  | inverseCongruenceIdentity c => simp [sevenIdentityBalance]
  | inverseCongruenceChain s t => simp [sevenIdentityBalance]
  | compositeCongruenceIdentity c d => simp [sevenIdentityBalance]
  | compositeCongruenceChain s s' t t' =>
      simp [sevenIdentityBalance] <;> abel
  | interchange s t =>
      simp [sevenIdentityBalance] <;> abel
  | zigzagDiamond c => simp [sevenIdentityBalance]

/-- Both triangle-overlap filling rules preserve this new fourth
charge, independently of the earlier T obstruction. -/
theorem triangleEightCell_preservesIdentityBalance {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenIdentityBalance s = sevenIdentityBalance t := by
  induction q with
  | original q => exact eightCell_preservesIdentityBalance q
  | leftTriangle c d =>
      simp [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenIdentityBalance]
  | rightTriangle c d =>
      simp [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenIdentityBalance]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => sevenIdentityBalance before + v) ih
  | whiskerRight q after ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => v + sevenIdentityBalance after) ih
  | inverseContext q ih =>
      simpa [sevenIdentityBalance] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenIdentityBalance] using
        congrArg₂ (fun v u : ℤ => v + u) ih ih'

/-- Both double-inversion overlap generators also preserve the
balance. Their additional constructors use no inverseId. -/
theorem involutionEightCell_preservesIdentityBalance {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    sevenIdentityBalance s = sevenIdentityBalance t := by
  induction q with
  | previous q => exact triangleEightCell_preservesIdentityBalance q
  | leftOverlap c =>
      simp [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
        sevenIdentityBalance]
  | rightOverlap c =>
      simp [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
        sevenIdentityBalance]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => sevenIdentityBalance before + v) ih
  | whiskerRight q after ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => v + sevenIdentityBalance after) ih
  | inverseContext q ih =>
      simpa [sevenIdentityBalance] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenIdentityBalance] using
        congrArg₂ (fun v u : ℤ => v + u) ih ih'

/-- The full, CHOSEN v4.95 final eighth-level grammar preserves the
fourth charge. The two new genuine inverseComp/unit peaks have
balance -1+1=0 on their via branches. -/
theorem inverseCompEightCell_preservesIdentityBalance {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InverseCompEightCell W long short s t) :
    sevenIdentityBalance s = sevenIdentityBalance t := by
  induction q with
  | previous q => exact involutionEightCell_preservesIdentityBalance q
  | leftOverlap c =>
      simp [sevenInvCompLeftDirect, sevenInvCompLeftVia,
        sevenIdentityBalance] <;> omega
  | rightOverlap c =>
      simp [sevenInvCompRightDirect, sevenInvCompRightVia,
        sevenIdentityBalance] <;> omega
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => sevenIdentityBalance before + v) ih
  | whiskerRight q after ih =>
      simpa [sevenIdentityBalance] using
        congrArg (fun v : ℤ => v + sevenIdentityBalance after) ih
  | inverseContext q ih =>
      simpa [sevenIdentityBalance] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenIdentityBalance] using
        congrArg₂ (fun v u : ℤ => v + u) ih ih'

theorem inverseCompHistoryClass_eq_preservesIdentityBalance {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (eq : inverseCompHistoryClass s = inverseCompHistoryClass t) :
    sevenIdentityBalance s = sevenIdentityBalance t := by
  rcases (inverseCompHistoryClass_eq_iff s t).1 eq with ⟨q⟩
  exact inverseCompEightCell_preservesIdentityBalance q

/-- Genuine identity/double-inversion peak, first route. -/
def sevenIdentityDoubleDirect (w : W) :
    SevenRewrite W long short
      (.symm (.symm (.refl w))) (.refl w) :=
  .doubleInverse (.refl w)

/-- Alternative reduction uses two actual inverseId steps and zero
doubleInverse steps, with the SAME six-cell raw endpoints. -/
def sevenIdentityDoubleVia (w : W) :
    SevenRewrite W long short
      (.symm (.symm (.refl w))) (.refl w) :=
  .trans (.congrInv (.inverseId w)) (.inverseId w)

/-- Actual three-factor six-cell source of the hidden composite
critical pair. Every factor is a typed loop at the SAME vertex. -/
def hiddenCriticalSource (w : W) : PentagonAdjoinedSixCell W long short w w :=
  .trans
    (.trans
      (.symm (.symm (.refl w)))
      (.trans (.symm (.symm (.refl w))) (.symm (.refl w))))
    (.trans (.trans (.refl w) (.refl w)) (.refl w))

def hiddenCriticalTarget (w : W) : PentagonAdjoinedSixCell W long short w w :=
  .trans
    (.trans (.refl w) (.refl w))
    (.trans (.refl w) (.refl w))

/-- Route A: doubleInverse; direct left cancellation; triangle via
associator. Its triple is (1,1,0) and identity balance is 0. -/
def sevenHiddenCriticalFirst (w : W) :
    SevenRewrite W long short
      (hiddenCriticalSource w) (hiddenCriticalTarget w) :=
  .congrComp
    (.congrComp
      (sevenIdentityDoubleDirect w)
      (sevenLeftDoubleInverseDirect (.refl w)))
    (sevenLeftTriangleViaAssoc (.refl w) (.refl w))

/-- Route B: two inverseId reductions; doubleInverse via; direct
triangle. Same endpoints and same three old charges, different
new identity balance. -/
def sevenHiddenCriticalSecond (w : W) :
    SevenRewrite W long short
      (hiddenCriticalSource w) (hiddenCriticalTarget w) :=
  .congrComp
    (.congrComp
      (sevenIdentityDoubleVia w)
      (sevenLeftDoubleInverseVia (.refl w)))
    (sevenLeftTriangleDirect (.refl w) (.refl w))

/-- The old triple is unable even to distinguish these explicit
parallel derivations; both evaluate to (1,1,0). -/
theorem sevenHiddenCritical_threeChargeValues (w : W) :
    sevenChargeTriple (sevenHiddenCriticalFirst w) = (1, 1, 0) ∧
    sevenChargeTriple (sevenHiddenCriticalSecond w) = (1, 1, 0) := by
  constructor <;>
    simp [sevenHiddenCriticalFirst, sevenHiddenCriticalSecond,
      sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
      sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
      sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
      sevenChargeTriple, sevenTriangleCharge,
      sevenInvolutionCharge, sevenInverseCompCharge]

theorem sevenHiddenCritical_sameTriple (w : W) :
    sevenChargeTriple (sevenHiddenCriticalFirst w) =
      sevenChargeTriple (sevenHiddenCriticalSecond w) := by
  exact (sevenHiddenCritical_threeChargeValues w).1.trans
    (sevenHiddenCritical_threeChargeValues w).2.symm

/-- The genuinely independent fourth observation separates the two
raw histories, and even their v4.95 higher-history classes. -/
theorem sevenHiddenCritical_balanceValues (w : W) :
    sevenIdentityBalance (sevenHiddenCriticalFirst w) = 0 ∧
    sevenIdentityBalance (sevenHiddenCriticalSecond w) = 2 := by
  constructor <;>
    norm_num [sevenHiddenCriticalFirst, sevenHiddenCriticalSecond,
      sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
      sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
      sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
      sevenIdentityBalance]

theorem sevenHiddenCritical_noComparison (w : W) :
    ¬ Nonempty (InverseCompEightCell W long short
      (sevenHiddenCriticalFirst w) (sevenHiddenCriticalSecond w)) := by
  rintro ⟨q⟩
  have hb := inverseCompEightCell_preservesIdentityBalance q
  have vals := sevenHiddenCritical_balanceValues w
  rw [vals.1, vals.2] at hb
  norm_num at hb

theorem sevenHiddenCritical_notStrict (w : W) :
    sevenHiddenCriticalFirst w ≠ sevenHiddenCriticalSecond w := by
  intro eq
  have hb := congrArg (fun s => sevenIdentityBalance s) eq
  have vals := sevenHiddenCritical_balanceValues w
  rw [vals.1, vals.2] at hb
  norm_num at hb

theorem sevenHiddenCritical_distinctClasses (w : W) :
    inverseCompHistoryClass (sevenHiddenCriticalFirst w) ≠
      inverseCompHistoryClass (sevenHiddenCriticalSecond w) := by
  intro eq
  exact sevenHiddenCritical_noComparison w
    ((inverseCompHistoryClass_eq_iff
      (sevenHiddenCriticalFirst w) (sevenHiddenCriticalSecond w)).1 eq)

/-- Same old triple does NOT imply final higher comparison. The
counterexample is constructive and does not assume any unproved
global equality of the free seventh syntax. -/
theorem sevenChargeTriple_notCompleteForInverseComp (l r : W) :
    ¬ (∀ {w z : W}
        {c d : PentagonAdjoinedSixCell W l r w z}
        (s t : SevenRewrite W l r c d),
        sevenChargeTriple s = sevenChargeTriple t →
          Nonempty (InverseCompEightCell W l r s t)) := by
  intro every
  exact sevenHiddenCritical_noComparison (long := l) (short := r) l
    (every (sevenHiddenCriticalFirst (long := l) (short := r) l)
      (sevenHiddenCriticalSecond (long := l) (short := r) l)
      (sevenHiddenCritical_sameTriple (long := l) (short := r) l))

/-- Stronger than v4.96 linear rigidity: even an ARBITRARY nonlinear
function on Z^3 cannot reconstruct the fourth identity charge on
all original typed seventh histories. -/
theorem sevenIdentityBalance_notFactorThroughTriple (l r : W) :
    ¬ ∃ F : (ℤ × ℤ × ℤ) → ℤ,
      ∀ {w z : W}
        {c d : PentagonAdjoinedSixCell W l r w z}
        (s : SevenRewrite W l r c d),
          sevenIdentityBalance s = F (sevenChargeTriple s) := by
  rintro ⟨F, factor⟩
  have ha := factor (sevenHiddenCriticalFirst (long := l) (short := r) l)
  have hb := factor (sevenHiddenCriticalSecond (long := l) (short := r) l)
  rw [sevenHiddenCritical_sameTriple (long := l) (short := r) l] at ha
  have both := ha.trans hb.symm
  have vals := sevenHiddenCritical_balanceValues (long := l) (short := r) l
  rw [vals.1, vals.2] at both
  norm_num at both

/-- In contrast, this independent two-inverseId interchange is
already filled by the ORIGINAL v4.91 EightCell rule. It is not
mistaken for the new hidden obstruction. -/
def sevenIdentityInterchangeFirst (w : W) :
    SevenRewrite W long short
      (.trans (.symm (.refl w)) (.symm (.refl w)))
      (.trans (.refl w) (.refl w)) :=
  .trans
    (.congrComp (.inverseId w) (.refl (.symm (.refl w))))
    (.congrComp (.refl (.refl w)) (.inverseId w))

def sevenIdentityInterchangeSecond (w : W) :
    SevenRewrite W long short
      (.trans (.symm (.refl w)) (.symm (.refl w)))
      (.trans (.refl w) (.refl w)) :=
  .trans
    (.congrComp (.refl (.symm (.refl w))) (.inverseId w))
    (.congrComp (.inverseId w) (.refl (.refl w)))

theorem sevenIdentityInterchange_joined (w : W) :
    Nonempty (InverseCompEightCell W long short
      (sevenIdentityInterchangeFirst w)
      (sevenIdentityInterchangeSecond w)) :=
  ⟨.previous (.previous (.original
    (.interchange (.inverseId w) (.inverseId w))))⟩

theorem sevenIdentityInterchange_sameTriple (w : W) :
    sevenChargeTriple (sevenIdentityInterchangeFirst w) =
      sevenChargeTriple (sevenIdentityInterchangeSecond w) := by
  simp [sevenIdentityInterchangeFirst, sevenIdentityInterchangeSecond,
    sevenChargeTriple, sevenTriangleCharge,
    sevenInvolutionCharge, sevenInverseCompCharge]

end PentagonAdjoinedSixCell

section ActualOriginalP77IdentityBalance
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

/-- For every genuine final original P77 raw index, the three
existing charges remain insufficient to characterize equality
of the final chosen higher-history quotient. The independent
GK5CG original source-equality obstruction is retained. -/
theorem pentagonActualThreeChargeIncompleteWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (¬ ∀ {w z : pentagonFinalConservativeLoop f g h k i}
        {c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z}
        (s t : PentagonAdjoinedSixCell.SevenRewrite
          (pentagonFinalConservativeLoop f g h k i)
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i) c d),
        PentagonAdjoinedSixCell.sevenChargeTriple s =
          PentagonAdjoinedSixCell.sevenChargeTriple t →
          Nonempty (PentagonAdjoinedSixCell.InverseCompEightCell
            (pentagonFinalConservativeLoop f g h k i)
            (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
            (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
            s t)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  exact ⟨PentagonAdjoinedSixCell.sevenChargeTriple_notCompleteForInverseComp
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i),
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sevenIdentityBalance
#print axioms PentagonAdjoinedSixCell.eightCell_preservesIdentityBalance
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesIdentityBalance
#print axioms PentagonAdjoinedSixCell.involutionEightCell_preservesIdentityBalance
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_preservesIdentityBalance
#print axioms PentagonAdjoinedSixCell.inverseCompHistoryClass_eq_preservesIdentityBalance
#print axioms PentagonAdjoinedSixCell.sevenIdentityDoubleDirect
#print axioms PentagonAdjoinedSixCell.sevenIdentityDoubleVia
#print axioms PentagonAdjoinedSixCell.hiddenCriticalSource
#print axioms PentagonAdjoinedSixCell.hiddenCriticalTarget
#print axioms PentagonAdjoinedSixCell.sevenHiddenCriticalFirst
#print axioms PentagonAdjoinedSixCell.sevenHiddenCriticalSecond
#print axioms PentagonAdjoinedSixCell.sevenHiddenCritical_threeChargeValues
#print axioms PentagonAdjoinedSixCell.sevenHiddenCritical_sameTriple
#print axioms PentagonAdjoinedSixCell.sevenHiddenCritical_balanceValues
#print axioms PentagonAdjoinedSixCell.sevenHiddenCritical_noComparison
#print axioms PentagonAdjoinedSixCell.sevenHiddenCritical_notStrict
#print axioms PentagonAdjoinedSixCell.sevenHiddenCritical_distinctClasses
#print axioms PentagonAdjoinedSixCell.sevenChargeTriple_notCompleteForInverseComp
#print axioms PentagonAdjoinedSixCell.sevenIdentityBalance_notFactorThroughTriple
#print axioms PentagonAdjoinedSixCell.sevenIdentityInterchangeFirst
#print axioms PentagonAdjoinedSixCell.sevenIdentityInterchangeSecond
#print axioms PentagonAdjoinedSixCell.sevenIdentityInterchange_joined
#print axioms PentagonAdjoinedSixCell.sevenIdentityInterchange_sameTriple
#print axioms pentagonActualThreeChargeIncompleteWithSourceObstruction

end ActualOriginalP77IdentityBalance
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
