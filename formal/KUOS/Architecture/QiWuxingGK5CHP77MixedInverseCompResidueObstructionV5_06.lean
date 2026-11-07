import KUOS.Architecture.QiWuxingGK5CHP77DoubleCompositeMinimalHigherCompletionV5_05

/-!
Qi v5.06 — MIXED INVERSE-COMPOSITE RESIDUE OBSTRUCTION.

The v5.05 independent DoubleCompositeEightCell grammar was constructed
with one new double-composite cancellation generator; it preserves
the original R and U mod-two observations and V modulo four. We do
NOT assume equality of these observations suffices for an eighth
comparison. Instead we construct a GENUINE new counterexample.

Combine the one-copy original inverse-of-composite cancellation
critical pair from v5.04 (direct versus expanded), with the one-copy
right inverse/identity critical pair from v5.02 (inverseRight(refl)
versus inverseId followed by rightUnit). Their R and U parity jumps
are individually odd but CANCEL when horizontally composed.
The V differences do NOT cancel: the mixed pair has V=2 versus 4,
hence V mod FOUR is 2 versus 0.

Crucially, the mixed pair initially has old K=0 versus K=1. We
compensate this exact gap using a THIRD, genuinely typed original
left inverseComposite/unit critical pair from v4.95, in REVERSE
branch order. Its K=1 versus K=0 but its R/U parities and integer V
agree. The resulting THREE-factor pair has:
   original (T,J,K)=(2,0,1) on both paths,
   old R mod2=0 on both paths,
   old U mod2=1 on both paths,
   V=3 versus 5, and V mod4=3 versus 1.

Full-constructor V-mod-four preservation from v5.05 proves that NO
existing DoubleCompositeEightCell joins this pair. Thus EVEN joint
agreement of old T/J/K, both residual parities and identical original
raw six-cell endpoints fails to force comparison. The V-mod-four
observer does not factor (even nonlinearly) through those old values.

We also paste the SAME strong obstruction into EACH actual original
P77 final raw index, using genuine GK5CG source Type evidence and
retaining its source strict EqualityInterpreter impossibility.

NO new eighth or ninth comparison generator or axiom is added:
the v5.05 presentation, quotient and earlier original typed histories
remain untouched. No global thinness or all-parallel completeness.
Append-only/tighten-only/overwrite-forbidden/same-root, root107.
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

/-- FIRST genuinely typed original source of the new MIXED pair. -/
def mixedCancellationSource (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans
    (compositeInverseCancelSource (long := long) (short := short) w)
    (.trans (.refl w) (.symm (.refl w)))

def mixedCancellationTarget (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans (.refl w) (.refl w)

/-- Two-factor precursor, direct/direct branch: V=2, R=U=0 mod2.
No free six-cell endpoint is identified by equality here. -/
def sevenMixedCancellationFirst (w : W) :
    SevenRewrite W long short
      (mixedCancellationSource (long := long) (short := short) w)
      (mixedCancellationTarget (long := long) (short := short) w) :=
  .congrComp (sevenCompositeInverseCancelDirect w)
    (sevenInverseUnitRightDirect w)

/-- Competing ORIGINAL path, expanded inverse-comp and inverseId/unit.
It has V=4, R=U=0 mod2, and K=1 rather than K=0. -/
def sevenMixedCancellationSecond (w : W) :
    SevenRewrite W long short
      (mixedCancellationSource (long := long) (short := short) w)
      (mixedCancellationTarget (long := long) (short := short) w) :=
  .congrComp (sevenCompositeInverseCancelVia w)
    (sevenInverseUnitRightVia w)

theorem sevenMixedCancellation_values (w : W) :
    sevenTotalReductionCharge
        (sevenMixedCancellationFirst (long := long) (short := short) w) = 2 ∧
    sevenTotalReductionCharge
        (sevenMixedCancellationSecond (long := long) (short := short) w) = 4 ∧
    sevenIdentityParity
        (sevenMixedCancellationFirst (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenMixedCancellationSecond (long := long) (short := short) w) = 0 ∧
    sevenUnitCountParity
        (sevenMixedCancellationFirst (long := long) (short := short) w) = 0 ∧
    sevenUnitCountParity
        (sevenMixedCancellationSecond (long := long) (short := short) w) = 0 := by
  simp [sevenMixedCancellationFirst, sevenMixedCancellationSecond,
    sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
    sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
    sevenTotalReductionCharge, sevenIdentityParity, sevenIdentityBalance,
    sevenUnitCountParity, sevenUnitStepCharge]

/-- The old T/J already agree; the previous K observation does NOT.
This explicit diagnosis is retained and compensated below. -/
theorem sevenMixedCancellation_tripleValues (w : W) :
    sevenChargeTriple
        (sevenMixedCancellationFirst (long := long) (short := short) w) =
        (2, 0, 0) ∧
    sevenChargeTriple
        (sevenMixedCancellationSecond (long := long) (short := short) w) =
        (2, 0, 1) := by
  constructor <;>
    norm_num [sevenMixedCancellationFirst, sevenMixedCancellationSecond,
      sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenChargeTriple, sevenTriangleCharge, sevenInvolutionCharge,
      sevenInverseCompCharge]

/-- The old v4.95 inverseComp LEFT critical pair has exactly the
opposite old K gap and no V or parity gap, so it supplies a genuinely
typed, old-eighth-cell comparison for compensating the K charge. -/
theorem sevenInvCompLeft_compensationValues (w : W) :
    sevenChargeTriple
        (sevenInvCompLeftVia (long := long) (short := short) (.refl w)) =
        (0, 0, 1) ∧
    sevenChargeTriple
        (sevenInvCompLeftDirect (long := long) (short := short) (.refl w)) =
        (0, 0, 0) := by
  constructor <;>
    norm_num [sevenInvCompLeftVia, sevenInvCompLeftDirect,
      sevenChargeTriple, sevenTriangleCharge, sevenInvolutionCharge,
      sevenInverseCompCharge]

def mixedResidueSource (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans (mixedCancellationSource (long := long) (short := short) w)
    (.symm (.trans (.refl w) (.refl w)))

def mixedResidueTarget (w : W) :
    PentagonAdjoinedSixCell W long short w w :=
  .trans (mixedCancellationTarget (long := long) (short := short) w)
    (.symm (.refl w))

/-- Strong three-factor witness: mixed inverse cancellation FIRST,
followed by the v4.95 left-overlap VIA branch, K=1. -/
def sevenMixedResidueFirst (w : W) :
    SevenRewrite W long short
      (mixedResidueSource (long := long) (short := short) w)
      (mixedResidueTarget (long := long) (short := short) w) :=
  .congrComp (sevenMixedCancellationFirst w)
    (sevenInvCompLeftVia (.refl w))

/-- Strong three-factor witness: mixed inverse cancellation SECOND,
followed by the v4.95 left-overlap DIRECT branch, K=1. -/
def sevenMixedResidueSecond (w : W) :
    SevenRewrite W long short
      (mixedResidueSource (long := long) (short := short) w)
      (mixedResidueTarget (long := long) (short := short) w) :=
  .congrComp (sevenMixedCancellationSecond w)
    (sevenInvCompLeftDirect (.refl w))

/-- Old three integer charges AGREE on the full genuinely typed
three-factor witness: K difference from the two-factor precursor
has been cancelled by an ACTUAL old inverseComp comparison. -/
theorem sevenMixedResidue_tripleValues (w : W) :
    sevenChargeTriple
        (sevenMixedResidueFirst (long := long) (short := short) w) =
        (2, 0, 1) ∧
    sevenChargeTriple
        (sevenMixedResidueSecond (long := long) (short := short) w) =
        (2, 0, 1) := by
  constructor <;>
    norm_num [sevenMixedResidueFirst, sevenMixedResidueSecond,
      sevenMixedCancellationFirst, sevenMixedCancellationSecond,
      sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenInvCompLeftVia, sevenInvCompLeftDirect,
      sevenChargeTriple, sevenTriangleCharge, sevenInvolutionCharge,
      sevenInverseCompCharge]

theorem sevenMixedResidue_sameTriple (w : W) :
    sevenChargeTriple
        (sevenMixedResidueFirst (long := long) (short := short) w) =
      sevenChargeTriple
        (sevenMixedResidueSecond (long := long) (short := short) w) :=
  (sevenMixedResidue_tripleValues (long := long) (short := short) w).1.trans
    (sevenMixedResidue_tripleValues (long := long) (short := short) w).2.symm

/-- The original R mod-two values remain zero on BOTH strong paths.
The original U mod-two values are one on BOTH, not independent bits. -/
theorem sevenMixedResidue_parityValues (w : W) :
    sevenIdentityParity
        (sevenMixedResidueFirst (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenMixedResidueSecond (long := long) (short := short) w) = 0 ∧
    sevenUnitCountParity
        (sevenMixedResidueFirst (long := long) (short := short) w) = 1 ∧
    sevenUnitCountParity
        (sevenMixedResidueSecond (long := long) (short := short) w) = 1 := by
  simp [sevenMixedResidueFirst, sevenMixedResidueSecond,
    sevenMixedCancellationFirst, sevenMixedCancellationSecond,
    sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
    sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
    sevenInvCompLeftVia, sevenInvCompLeftDirect,
    sevenIdentityParity, sevenIdentityBalance,
    sevenUnitCountParity, sevenUnitStepCharge]

theorem sevenMixedResidue_sameParities (w : W) :
    sevenIdentityParity
        (sevenMixedResidueFirst (long := long) (short := short) w) =
      sevenIdentityParity
        (sevenMixedResidueSecond (long := long) (short := short) w) ∧
    sevenUnitCountParity
        (sevenMixedResidueFirst (long := long) (short := short) w) =
      sevenUnitCountParity
        (sevenMixedResidueSecond (long := long) (short := short) w) := by
  have vals := sevenMixedResidue_parityValues (long := long) (short := short) w
  exact ⟨vals.1.trans vals.2.1.symm, vals.2.2.1.trans vals.2.2.2.symm⟩

/-- Integer V=3 versus 5 and NEW V modulo four=3 versus 1. -/
theorem sevenMixedResidue_totalValues (w : W) :
    sevenTotalReductionCharge
        (sevenMixedResidueFirst (long := long) (short := short) w) = 3 ∧
    sevenTotalReductionCharge
        (sevenMixedResidueSecond (long := long) (short := short) w) = 5 := by
  constructor <;>
    norm_num [sevenMixedResidueFirst, sevenMixedResidueSecond,
      sevenMixedCancellationFirst, sevenMixedCancellationSecond,
      sevenCompositeInverseCancelDirect, sevenCompositeInverseCancelVia,
      sevenInverseUnitRightDirect, sevenInverseUnitRightVia,
      sevenInvCompLeftVia, sevenInvCompLeftDirect, sevenTotalReductionCharge]

theorem sevenMixedResidue_residueValues (w : W) :
    sevenTotalReductionResidue
        (sevenMixedResidueFirst (long := long) (short := short) w) = 3 ∧
    sevenTotalReductionResidue
        (sevenMixedResidueSecond (long := long) (short := short) w) = 1 := by
  have vals := sevenMixedResidue_totalValues (long := long) (short := short) w
  constructor <;>
    norm_num [sevenTotalReductionResidue, vals.1, vals.2]

/-- Non-comparison is a THEOREM, not a missing search result:
every chosen v5.05 DoubleCompositeEightCell constructor preserves
V modulo FOUR, contradicting the ACTUAL 3 versus 1 raw histories. -/
theorem sevenMixedResidue_noDoubleCompositeComparison (w : W) :
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (sevenMixedResidueFirst (long := long) (short := short) w)
      (sevenMixedResidueSecond (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have h := doubleCompositeEightCell_preservesTotalReductionResidue q
  have vals := sevenMixedResidue_residueValues (long := long) (short := short) w
  rw [vals.1, vals.2] at h
  norm_num at h

theorem sevenMixedResidue_distinctDoubleCompositeClasses (w : W) :
    doubleCompositeHistoryClass
        (sevenMixedResidueFirst (long := long) (short := short) w) ≠
      doubleCompositeHistoryClass
        (sevenMixedResidueSecond (long := long) (short := short) w) := by
  intro h
  exact sevenMixedResidue_noDoubleCompositeComparison
    (long := long) (short := short) w
    ((doubleCompositeHistoryClass_eq_iff _ _).1 h)

/-- Old T/J/K, old R parity AND old U parity agreement together are
NOT enough for v5.05 chosen eighth-cell comparability. -/
theorem sevenTripleAndParities_notCompleteAfterDoubleComposite (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      sevenChargeTriple s = sevenChargeTriple t →
      sevenIdentityParity s = sevenIdentityParity t →
      sevenUnitCountParity s = sevenUnitCountParity t →
      Nonempty (DoubleCompositeEightCell W l r s t)) := by
  intro all
  have hs := sevenMixedResidue_sameParities (long := l) (short := r) l
  exact sevenMixedResidue_noDoubleCompositeComparison (long := l) (short := r) l
    (all
      (sevenMixedResidueFirst (long := l) (short := r) l)
      (sevenMixedResidueSecond (long := l) (short := r) l)
      (sevenMixedResidue_sameTriple (long := l) (short := r) l)
      hs.1 hs.2)

/-- Even a potentially nonlinear function of the complete previously
used (T,J,K,Rmod2,Umod2) observation vector cannot recover the new
selected Vmod4 charge on ALL genuinely typed original histories. -/
theorem sevenTotalReductionResidue_notFactorThroughOldObservations (l r : W) :
    ¬ ∃ F : ((ℤ × ℤ × ℤ) × ℤ × ℤ) → ℤ,
      ∀ {w z : W}
        {c d : PentagonAdjoinedSixCell W l r w z}
        (s : SevenRewrite W l r c d),
        sevenTotalReductionResidue s =
          F (sevenChargeTriple s, sevenIdentityParity s, sevenUnitCountParity s) := by
  rintro ⟨F, factor⟩
  have h₁ := factor (sevenMixedResidueFirst (long := l) (short := r) l)
  have h₂ := factor (sevenMixedResidueSecond (long := l) (short := r) l)
  have hT := sevenMixedResidue_sameTriple (long := l) (short := r) l
  have hP := sevenMixedResidue_sameParities (long := l) (short := r) l
  have heq :
      sevenTotalReductionResidue
          (sevenMixedResidueFirst (long := l) (short := r) l) =
        sevenTotalReductionResidue
          (sevenMixedResidueSecond (long := l) (short := r) l) := by
    calc
      _ = F (sevenChargeTriple (sevenMixedResidueFirst (long := l) (short := r) l),
          sevenIdentityParity (sevenMixedResidueFirst (long := l) (short := r) l),
          sevenUnitCountParity (sevenMixedResidueFirst (long := l) (short := r) l)) := h₁
      _ = F (sevenChargeTriple (sevenMixedResidueSecond (long := l) (short := r) l),
          sevenIdentityParity (sevenMixedResidueSecond (long := l) (short := r) l),
          sevenUnitCountParity (sevenMixedResidueSecond (long := l) (short := r) l)) := by
            rw [hT, hP.1, hP.2]
      _ = _ := h₂.symm
  have vals := sevenMixedResidue_residueValues (long := l) (short := r) l
  rw [vals.1, vals.2] at heq
  norm_num at heq

/-- Paste the SAME strong triple-and-parity-invisible v5.06
obstruction against ANY genuine sixth-cell source c, retaining the
unquotiented original raw source/target words and evidence history. -/
def sevenMixedResidueCompositeFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w) c)
      (.trans (mixedResidueTarget (long := long) (short := short) w) c) :=
  .congrComp (sevenMixedResidueFirst w) (.refl c)

def sevenMixedResidueCompositeSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (mixedResidueSource (long := long) (short := short) w) c)
      (.trans (mixedResidueTarget (long := long) (short := short) w) c) :=
  .congrComp (sevenMixedResidueSecond w) (.refl c)

theorem sevenMixedResidueComposite_values {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenChargeTriple (sevenMixedResidueCompositeFirst c) =
      sevenChargeTriple (sevenMixedResidueCompositeSecond c) ∧
    sevenIdentityParity (sevenMixedResidueCompositeFirst c) =
      sevenIdentityParity (sevenMixedResidueCompositeSecond c) ∧
    sevenUnitCountParity (sevenMixedResidueCompositeFirst c) =
      sevenUnitCountParity (sevenMixedResidueCompositeSecond c) ∧
    (sevenTotalReductionResidue (sevenMixedResidueCompositeFirst c) = 3 ∧
     sevenTotalReductionResidue (sevenMixedResidueCompositeSecond c) = 1) := by
  constructor
  · simpa [sevenMixedResidueCompositeFirst, sevenMixedResidueCompositeSecond,
      sevenChargeTriple, sevenTriangleCharge,
      sevenInvolutionCharge, sevenInverseCompCharge] using
        (sevenMixedResidue_sameTriple (long := long) (short := short) w)
  constructor
  · simpa [sevenMixedResidueCompositeFirst, sevenMixedResidueCompositeSecond,
      sevenIdentityParity, sevenIdentityBalance] using
        (sevenMixedResidue_sameParities (long := long) (short := short) w).1
  constructor
  · simpa [sevenMixedResidueCompositeFirst, sevenMixedResidueCompositeSecond,
      sevenUnitCountParity, sevenUnitStepCharge] using
        (sevenMixedResidue_sameParities (long := long) (short := short) w).2
  · have hv := sevenMixedResidue_totalValues (long := long) (short := short) w
    constructor <;>
      norm_num [sevenMixedResidueCompositeFirst,
        sevenMixedResidueCompositeSecond, sevenTotalReductionResidue,
        sevenTotalReductionCharge, hv.1, hv.2]

theorem sevenMixedResidueComposite_noDoubleCompositeComparison {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (DoubleCompositeEightCell W long short
      (sevenMixedResidueCompositeFirst c)
      (sevenMixedResidueCompositeSecond c)) := by
  rintro ⟨q⟩
  have h := doubleCompositeEightCell_preservesTotalReductionResidue q
  have vals := (sevenMixedResidueComposite_values c).2.2.2
  rw [vals.1, vals.2] at h
  norm_num at h

end PentagonAdjoinedSixCell

section ActualOriginalP77MixedResidueObstruction
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

/-- At EVERY original P77 final raw index, authentic GK5CG source
provides two actually typed seventh histories with identical
T/J/K, R and U parities, but different Vmod4; no chosen v5.05
eighth-level comparison exists, and source strict Eq is impossible.
This is not a quotient-level assumption or a new primitive cell. -/
theorem pentagonActualMixedResidueWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
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
      ¬ Nonempty (PentagonAdjoinedSixCell.DoubleCompositeEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst c)
        (PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    (PentagonAdjoinedSixCell.sevenMixedResidueComposite_values _).1,
    (PentagonAdjoinedSixCell.sevenMixedResidueComposite_values _).2.1,
    (PentagonAdjoinedSixCell.sevenMixedResidueComposite_values _).2.2.1,
    PentagonAdjoinedSixCell.sevenMixedResidueComposite_noDoubleCompositeComparison _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.mixedCancellationSource
#print axioms PentagonAdjoinedSixCell.mixedCancellationTarget
#print axioms PentagonAdjoinedSixCell.sevenMixedCancellationFirst
#print axioms PentagonAdjoinedSixCell.sevenMixedCancellationSecond
#print axioms PentagonAdjoinedSixCell.sevenMixedCancellation_values
#print axioms PentagonAdjoinedSixCell.sevenMixedCancellation_tripleValues
#print axioms PentagonAdjoinedSixCell.sevenInvCompLeft_compensationValues
#print axioms PentagonAdjoinedSixCell.mixedResidueSource
#print axioms PentagonAdjoinedSixCell.mixedResidueTarget
#print axioms PentagonAdjoinedSixCell.sevenMixedResidueFirst
#print axioms PentagonAdjoinedSixCell.sevenMixedResidueSecond
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_tripleValues
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_sameTriple
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_parityValues
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_sameParities
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_totalValues
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_residueValues
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_noDoubleCompositeComparison
#print axioms PentagonAdjoinedSixCell.sevenMixedResidue_distinctDoubleCompositeClasses
#print axioms PentagonAdjoinedSixCell.sevenTripleAndParities_notCompleteAfterDoubleComposite
#print axioms PentagonAdjoinedSixCell.sevenTotalReductionResidue_notFactorThroughOldObservations
#print axioms PentagonAdjoinedSixCell.sevenMixedResidueCompositeFirst
#print axioms PentagonAdjoinedSixCell.sevenMixedResidueCompositeSecond
#print axioms PentagonAdjoinedSixCell.sevenMixedResidueComposite_values
#print axioms PentagonAdjoinedSixCell.sevenMixedResidueComposite_noDoubleCompositeComparison
#print axioms pentagonActualMixedResidueWithSourceObstruction

end ActualOriginalP77MixedResidueObstruction
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
