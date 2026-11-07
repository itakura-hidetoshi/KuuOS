import KUOS.Architecture.QiWuxingGK5CHP77MixedRoundtripUnitMinimalNinthCompletionV5_13

/-!
Qi v5.14 — ORIGINAL P/M CRITICAL-DIAMOND MINIMAL TENTH COMPARISON.

Qi v5.13 gives two independently constructed genuine ninth-cell paths
PThenM and MThenP at the SAME original eighth-cell endpoints, proves
their raw proof histories differ, and never claims a tenth-cell no-go.

Add exactly ONE genuinely typed tenth-cell primitive exchangePM
relating these two original ninth histories. Keep the original
MixedCancelNineCell freely generated evidence untouched. Close this
new tenth comparison only under typed symmetry, transitivity and
the operations already present on ninth-cell proof values.

The selected tenth quotient identifies the two original completion
paths, but does not identify their raw values. The original P/M
ninth-event order cannot descend to this quotient. In contrast,
a new nonnegative ninth-chain count descends through EVERY tenth
constructor. Its 1-vs-0 witness proves that the tenth completion
is not globally thin. The old eighth residual obstruction persists
unchanged, as does the strict original P77/GK5CG source boundary.

append-only / tighten-only / overwrite-forbidden / same-root.
Public root 107; Lean v4.30.0-rc2; pinned mathlib
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

/-- The selected, freely generated tenth comparison. The ONLY
non-strict generating tenth cell is exchangePM, with the genuinely
typed original v5.13 ninth critical-diamond boundary. -/
inductive MixedInterchangeTenCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    {q q' : PentagonAssocEightCell W l r s t} →
    MixedCancelNineCell W l r q q' →
    MixedCancelNineCell W l r q q' → Type uSix where
  | strict {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (heq : alpha = beta) :
      MixedInterchangeTenCell W l r alpha beta
  | exchangePM :
      MixedInterchangeTenCell W l r
        (originalDoubleCancellationPThenM l r)
        (originalDoubleCancellationMThenP l r)
  | symm {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta) :
      MixedInterchangeTenCell W l r beta alpha
  | trans {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta gamma : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta)
      (zeta : MixedInterchangeTenCell W l r beta gamma) :
      MixedInterchangeTenCell W l r alpha gamma
  | nineReverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta) :
      MixedInterchangeTenCell W l r
        (.reverse alpha) (.reverse beta)
  | nineChain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' q'' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r q' q''}
      (xi : MixedInterchangeTenCell W l r alpha beta)
      (zeta : MixedInterchangeTenCell W l r gamma delta) :
      MixedInterchangeTenCell W l r
        (.chain alpha gamma) (.chain beta delta)
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta) :
      MixedInterchangeTenCell W l r
        (.reverseContext alpha) (.reverseContext beta)
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      (xi : MixedInterchangeTenCell W l r alpha beta)
      (zeta : MixedInterchangeTenCell W l r gamma delta) :
      MixedInterchangeTenCell W l r
        (.chainContext alpha gamma) (.chainContext beta delta)
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta) :
      MixedInterchangeTenCell W l r
        (.whiskerLeft before alpha) (.whiskerLeft before beta)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta)
      (after : SevenRewrite W l r d e) :
      MixedInterchangeTenCell W l r
        (.whiskerRight alpha after) (.whiskerRight beta after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedInterchangeTenCell W l r alpha beta) :
      MixedInterchangeTenCell W l r
        (.inverseContext alpha) (.inverseContext beta)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      {q q' : PentagonAssocEightCell W l r s s'}
      {b b' : PentagonAssocEightCell W l r t t'}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {gamma delta : MixedCancelNineCell W l r b b'}
      (xi : MixedInterchangeTenCell W l r alpha beta)
      (zeta : MixedInterchangeTenCell W l r gamma delta) :
      MixedInterchangeTenCell W l r
        (.compositeContext alpha gamma)
        (.compositeContext beta delta)

def mixedInterchangeTenCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    MixedInterchangeTenCell W long short alpha alpha :=
  .strict rfl

/-- Strict equality of the two original ninth proofs is impossible,
although their explicit new tenth comparison is inhabited. -/
theorem mixedInterchangeTenCell_relativeNecessity (l r : W) :
    Nonempty (MixedInterchangeTenCell W l r
      (originalDoubleCancellationPThenM l r)
      (originalDoubleCancellationMThenP l r)) ∧
    originalDoubleCancellationPThenM l r ≠
      originalDoubleCancellationMThenP l r :=
  ⟨⟨.exchangePM⟩, originalDoubleCancellationRawNineGap l r⟩

/-- There is no global interpreter of the new tenth witness as
equality of the untouched ninth proof terms. -/
theorem mixedInterchangeTenCell_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha beta : MixedCancelNineCell W l r q q'),
      MixedInterchangeTenCell W l r alpha beta → alpha = beta) := by
  intro interpret
  exact originalDoubleCancellationRawNineGap l r
    (interpret _ _ (.exchangePM))

/-- Local selected quotient on ORIGINAL ninth-cell proof values.
No quotient is imposed on original eighth evidence or its sources. -/
def mixedInterchangeTenthSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t} :
    Setoid (MixedCancelNineCell W l r q q') where
  r := fun alpha beta =>
    Nonempty (MixedInterchangeTenCell W l r alpha beta)
  iseqv := by
    constructor
    · intro alpha
      exact ⟨.strict rfl⟩
    · intro alpha beta h
      rcases h with ⟨xi⟩
      exact ⟨.symm xi⟩
    · intro alpha beta gamma h h'
      rcases h with ⟨xi⟩
      rcases h' with ⟨zeta⟩
      exact ⟨.trans xi zeta⟩

def mixedInterchangeTenthClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    Quotient (mixedInterchangeTenthSetoid W long short
      (q := q) (q' := q')) :=
  Quotient.mk _ alpha

theorem mixedInterchangeTenthClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha beta : MixedCancelNineCell W long short q q') :
    mixedInterchangeTenthClass alpha =
      mixedInterchangeTenthClass beta ↔
      Nonempty (MixedInterchangeTenCell W long short alpha beta) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem mixedInterchangeTenthClass_criticalDiamond (l r : W) :
    mixedInterchangeTenthClass (originalDoubleCancellationPThenM l r) =
      mixedInterchangeTenthClass (originalDoubleCancellationMThenP l r) :=
  (mixedInterchangeTenthClass_eq_iff _ _).2 ⟨.exchangePM⟩

/-- The original ordered ninth-event trace is NOT a tenth-quotient
invariant, because the actual original P,M and M,P paths differ. -/
theorem mixedInterchangeTenthClass_noTraceDescent (l r : W) :
    ¬ ∃ (observe :
      Quotient (mixedInterchangeTenthSetoid W l r
        (q := originalDoubleCancellationTop l r)
        (q' := originalDoubleCancellationBottom l r)) → List Bool),
      ∀ (alpha : MixedCancelNineCell W l r
        (originalDoubleCancellationTop l r)
        (originalDoubleCancellationBottom l r)),
        observe (mixedInterchangeTenthClass alpha) =
          mixedCancelNinePrimitiveTrace alpha := by
  rintro ⟨observe, compatible⟩
  have heq := congrArg observe
    (mixedInterchangeTenthClass_criticalDiamond l r)
  rw [compatible (originalDoubleCancellationPThenM l r),
    compatible (originalDoubleCancellationMThenP l r),
    (originalDoubleCancellationTraceValues l r).1,
    (originalDoubleCancellationTraceValues l r).2] at heq
  cases heq

/-- A RAW ninth proof's nonnegative free-chain complexity.
Inherited v5.12 ninth proof witnesses count as atomic syntax here;
the new M generator is also atomic. Only actual NEW ninth chains
contribute +1, and all eight-proof contexts are structural. -/
def tenthResidualNineChainCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') : ℕ :=
  match alpha with
  | .previous _ => 0
  | .cancelMixed => 0
  | .reverse alpha => tenthResidualNineChainCharge alpha
  | .chain alpha beta =>
      tenthResidualNineChainCharge alpha +
        tenthResidualNineChainCharge beta + 1
  | .reverseContext alpha => tenthResidualNineChainCharge alpha
  | .chainContext alpha beta =>
      tenthResidualNineChainCharge alpha +
        tenthResidualNineChainCharge beta
  | .whiskerLeft _ alpha => tenthResidualNineChainCharge alpha
  | .whiskerRight alpha _ => tenthResidualNineChainCharge alpha
  | .inverseContext alpha => tenthResidualNineChainCharge alpha
  | .compositeContext alpha beta =>
      tenthResidualNineChainCharge alpha +
        tenthResidualNineChainCharge beta

theorem tenthCriticalDiamondChainChargeValues (l r : W) :
    tenthResidualNineChainCharge (originalDoubleCancellationPThenM l r) = 1 ∧
    tenthResidualNineChainCharge (originalDoubleCancellationMThenP l r) = 1 :=
  ⟨rfl, rfl⟩

/-- A full-constructor proof: the selected tenth exchange is
compatible with the free ninth-chain count in EVERY typed context. -/
theorem mixedInterchangeTenCell_preservesNinthChainCharge
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    {alpha beta : MixedCancelNineCell W long short q q'}
    (xi : MixedInterchangeTenCell W long short alpha beta) :
    tenthResidualNineChainCharge alpha =
      tenthResidualNineChainCharge beta := by
  induction xi with
  | strict heq => cases heq; rfl
  | exchangePM => rfl
  | symm xi ih => exact ih.symm
  | trans xi zeta ih ih' => exact ih.trans ih'
  | nineReverse xi ih =>
      simpa only [tenthResidualNineChainCharge] using ih
  | nineChain xi zeta ih ih' =>
      simpa only [tenthResidualNineChainCharge] using
        congrArg₂ (fun a b : ℕ => a + b + 1) ih ih'
  | reverseContext xi ih =>
      simpa only [tenthResidualNineChainCharge] using ih
  | chainContext xi zeta ih ih' =>
      simpa only [tenthResidualNineChainCharge] using
        congrArg₂ (fun a b : ℕ => a + b) ih ih'
  | whiskerLeft before xi ih =>
      simpa only [tenthResidualNineChainCharge] using ih
  | whiskerRight xi after ih =>
      simpa only [tenthResidualNineChainCharge] using ih
  | inverseContext xi ih =>
      simpa only [tenthResidualNineChainCharge] using ih
  | compositeContext xi zeta ih ih' =>
      simpa only [tenthResidualNineChainCharge] using
        congrArg₂ (fun a b : ℕ => a + b) ih ih'

/-- Genuine quotient descent, rather than declaring raw nine-cell
proof terms extensionally equal. -/
def mixedInterchangeTenthNinthChainCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t} :
    Quotient (mixedInterchangeTenthSetoid W long short
      (q := q) (q' := q')) → ℕ :=
  Quotient.lift
    (fun alpha : MixedCancelNineCell W long short q q' =>
      tenthResidualNineChainCharge alpha)
    (by
      intro alpha beta h
      rcases h with ⟨xi⟩
      exact mixedInterchangeTenCell_preservesNinthChainCharge xi)

theorem mixedInterchangeTenthNinthChainCharge_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    mixedInterchangeTenthNinthChainCharge (mixedInterchangeTenthClass alpha) =
      tenthResidualNineChainCharge alpha := rfl

/-- The same original ninth reflexivity evidence chained twice
is a new raw ninth value at identical original eighth boundaries. -/
def tenthDoubleReflexiveNine (l r : W) :
    MixedCancelNineCell W l r
      (ninthPentagonReflexive l r)
      (ninthPentagonReflexive l r) :=
  .chain (mixedCancelNineCell_refl (ninthPentagonReflexive l r))
    (mixedCancelNineCell_refl (ninthPentagonReflexive l r))

theorem tenthDoubleReflexiveNineChainChargeValues (l r : W) :
    tenthResidualNineChainCharge (tenthDoubleReflexiveNine l r) = 1 ∧
    tenthResidualNineChainCharge
      (mixedCancelNineCell_refl (ninthPentagonReflexive l r)) = 0 :=
  ⟨rfl, rfl⟩

/-- The requested tenth generator is genuinely MINIMAL: it does
not force every parallel pair of ninth proofs to be comparable. -/
theorem tenthDoubleReflexive_noInterchangeTenComparison (l r : W) :
    ¬ Nonempty (MixedInterchangeTenCell W l r
      (tenthDoubleReflexiveNine l r)
      (mixedCancelNineCell_refl (ninthPentagonReflexive l r))) := by
  rintro ⟨xi⟩
  have h := mixedInterchangeTenCell_preservesNinthChainCharge xi
  have vals := tenthDoubleReflexiveNineChainChargeValues l r
  rw [vals.1, vals.2] at h
  omega

theorem tenthDoubleReflexive_distinctInterchangeClass (l r : W) :
    mixedInterchangeTenthClass (tenthDoubleReflexiveNine l r) ≠
      mixedInterchangeTenthClass
        (mixedCancelNineCell_refl (ninthPentagonReflexive l r)) := by
  intro h
  exact tenthDoubleReflexive_noInterchangeTenComparison l r
    ((mixedInterchangeTenthClass_eq_iff _ _).1 h)

theorem mixedInterchangeTenCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha beta : MixedCancelNineCell W l r q q'),
      Nonempty (MixedInterchangeTenCell W l r alpha beta)) := by
  intro interpret
  exact tenthDoubleReflexive_noInterchangeTenComparison l r
    (interpret _ _)

/-- The v5.13 eighth free-chain obstruction survives exactly,
because adjoining a comparison BETWEEN ninth proofs cannot
manufacture previously impossible ninth evidence. -/
theorem mixedInterchangeTenCell_retainsEighthObstruction (l r : W) :
    ¬ Nonempty (MixedCancelNineCell W l r
      (ninthDoubleReflexiveChain l r)
      (ninthPentagonReflexive l r)) :=
  ninthDoubleReflexive_noMixedCancelComparison l r

/-- Any proposed left inverse to the selected tenth quotient would
collapse the original two unequal raw ninth histories. -/
theorem mixedInterchangeTenthClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
      Quotient (mixedInterchangeTenthSetoid W l r
        (q := originalDoubleCancellationTop l r)
        (q' := originalDoubleCancellationBottom l r)) →
      MixedCancelNineCell W l r
        (originalDoubleCancellationTop l r)
        (originalDoubleCancellationBottom l r)),
      ∀ (alpha : MixedCancelNineCell W l r
        (originalDoubleCancellationTop l r)
        (originalDoubleCancellationBottom l r)),
        decode (mixedInterchangeTenthClass alpha) = alpha := by
  rintro ⟨decode, inv⟩
  apply originalDoubleCancellationRawNineGap l r
  calc
    originalDoubleCancellationPThenM l r =
        decode (mixedInterchangeTenthClass
          (originalDoubleCancellationPThenM l r)) := (inv _).symm
    _ = decode (mixedInterchangeTenthClass
          (originalDoubleCancellationMThenP l r)) :=
      congrArg decode (mixedInterchangeTenthClass_criticalDiamond l r)
    _ = originalDoubleCancellationMThenP l r := inv _

end PentagonAdjoinedSixCell

section ActualOriginalP77TenthCompletion
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

/-- All ORIGINAL P77 final raw indices inherit the genuine
GK5CG long/short Type-valued tenth critical diamond, without
promoting old source evidence to strict equality. -/
theorem pentagonActualPMCriticalDiamondTenthCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.MixedInterchangeTenCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.originalDoubleCancellationPThenM
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.originalDoubleCancellationMThenP
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.exchangePM⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.MixedInterchangeTenCell
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_refl
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_relativeNecessity
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthSetoid
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthClass
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthClass_criticalDiamond
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthClass_noTraceDescent
#print axioms PentagonAdjoinedSixCell.tenthResidualNineChainCharge
#print axioms PentagonAdjoinedSixCell.tenthCriticalDiamondChainChargeValues
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_preservesNinthChainCharge
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthNinthChainCharge
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthNinthChainCharge_onClass
#print axioms PentagonAdjoinedSixCell.tenthDoubleReflexiveNine
#print axioms PentagonAdjoinedSixCell.tenthDoubleReflexiveNineChainChargeValues
#print axioms PentagonAdjoinedSixCell.tenthDoubleReflexive_noInterchangeTenComparison
#print axioms PentagonAdjoinedSixCell.tenthDoubleReflexive_distinctInterchangeClass
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenCell_retainsEighthObstruction
#print axioms PentagonAdjoinedSixCell.mixedInterchangeTenthClass_noRawRetraction
#print axioms pentagonActualPMCriticalDiamondTenthCompletion

end ActualOriginalP77TenthCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
