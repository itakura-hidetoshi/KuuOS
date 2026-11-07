import KUOS.Architecture.QiWuxingGK5CHP77MixedResidueV2CompatibilityPR3238
import KUOS.Architecture.QiWuxingGK5CHP77InversePentagonAssociatorObstructionV5_08

/-!
Qi v5.09 — SINGLE-PRIMITIVE FOURFOLD PENTAGON EIGHTH COMPLETION.

The genuine Qi v5.08 original SevenRewrite three-associator and
two-associator histories on the alternating raw adjoined pentagon/
inverse-pentagon word have identical raw sixth-cell endpoints,
equal V/R/U residual mod-two observers, but a PROVED distinguishing
integer associator fingerprint Phi=1 vs0. No current
MixedResidueEightCell comparison can connect those histories.

Add one AND ONLY ONE original-pair comparison in a new independent
Type-valued PentagonAssocEightCell. All old MixedResidueEightCell
evidence is retained through previous; the original F55/P77/GK5CG
source, raw seventh histories, old independent eighth grammar,
its quotient, and original source strict Eq remain unchanged.

Prove strict quotient coarsening, failure of Phi descent, and
full-constructor preservation plus genuine quotient descents of
the three previous mod-two observers. Add one real typed overlap
with the existing mixedResidue generator, still impossible in
the OLD comparison grammar but fillable in the new one.

No universal higher thinness, no ninth cell, no original source
strict equality promotion, no imported extra axioms. Preserve
root107, pinned Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6,
validation-only protected #1558 Draft/open/unmerged.
append-only / tighten-only / overwrite-forbidden / same-root.
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

/-- Independent higher comparison grammar: precisely ONE new
generator, the genuine original fourfold pentagon-associator pair. -/
inductive PentagonAssocEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedResidueEightCell W l r s t) :
      PentagonAssocEightCell W l r s t
  | fourfoldPentagon :
      PentagonAssocEightCell W l r
        (sevenFourfoldInversePentagonThree l r)
        (sevenFourfoldInversePentagonTwo l r)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : PentagonAssocEightCell W l r s t) :
      PentagonAssocEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : PentagonAssocEightCell W l r s t)
      (q' : PentagonAssocEightCell W l r t u) :
      PentagonAssocEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : PentagonAssocEightCell W l r s t) :
      PentagonAssocEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : PentagonAssocEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      PentagonAssocEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : PentagonAssocEightCell W l r s t) :
      PentagonAssocEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : PentagonAssocEightCell W l r s s')
      (q' : PentagonAssocEightCell W l r t t') :
      PentagonAssocEightCell W l r
        (.congrComp s t) (.congrComp s' t')

def pentagonAssocEightCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    PentagonAssocEightCell W long short s t :=
  .previous q

def pentagonAssocEightCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    PentagonAssocEightCell W long short s s :=
  .previous (mixedResidueEightCell_refl s)

/-- One new comparison is PROVABLY not constructible from all
prior higher comparisons: Phi=1 vs0 from actual v5.08 source. -/
theorem pentagonAssocEightCell_strictlyNew (l r : W) :
    Nonempty (PentagonAssocEightCell W l r
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonTwo l r)) ∧
    ¬ Nonempty (MixedResidueEightCell W l r
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonTwo l r)) :=
  ⟨⟨.fourfoldPentagon⟩,
    sevenFourfoldInversePentagon_noMixedResidueComparison l r⟩

theorem pentagonAssocEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      PentagonAssocEightCell W l r s t →
        MixedResidueEightCell W l r s t) := by
  rintro ⟨interpret⟩
  exact sevenFourfoldInversePentagon_noMixedResidueComparison l r
    ⟨interpret _ _ (.fourfoldPentagon)⟩

theorem pentagonAssocEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      PentagonAssocEightCell W l r s t → s = t) := by
  intro interpret
  apply mixedResidueEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t (.previous q)

/-- V mod2 is preserved by ALL old constructors plus the one new
pentagon-associator comparison and all typed higher contexts. -/
theorem pentagonAssocEightCell_preservesVParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    sevenTotalReductionParity s = sevenTotalReductionParity t := by
  induction q with
  | previous q => exact mixedResidueEightCell_preservesVParity q
  | fourfoldPentagon =>
      exact (sevenFourfoldInversePentagon_sameResiduals long short).1
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenTotalReductionParity, sevenTotalReductionResidue] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | whiskerRight q after ih =>
      simp only [sevenTotalReductionParity, sevenTotalReductionResidue] at ih ⊢
      simp only [sevenTotalReductionCharge]
      omega
  | inverseContext q ih =>
      simpa [sevenTotalReductionParity, sevenTotalReductionResidue,
        sevenTotalReductionCharge] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenTotalReductionParity, sevenTotalReductionResidue]
        at ih ih' ⊢
      simp only [sevenTotalReductionCharge]
      omega

theorem pentagonAssocEightCell_preservesRParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  induction q with
  | previous q => exact mixedResidueEightCell_preservesParity q
  | fourfoldPentagon =>
      exact (sevenFourfoldInversePentagon_sameResiduals long short).2.1
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

theorem pentagonAssocEightCell_preservesUParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    sevenUnitCountParity s = sevenUnitCountParity t := by
  induction q with
  | previous q => exact mixedResidueEightCell_preservesUnitCountParity q
  | fourfoldPentagon =>
      exact (sevenFourfoldInversePentagon_sameResiduals long short).2.2
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

def pentagonAssocHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (PentagonAssocEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨pentagonAssocEightCell_refl s⟩
    · intro s t h
      rcases h with ⟨q⟩
      exact ⟨.reverse q⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def pentagonAssocHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (pentagonAssocHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem pentagonAssocHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    pentagonAssocHistoryClass s = pentagonAssocHistoryClass t ↔
      Nonempty (PentagonAssocEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem mixedResidueHistoryClass_descendsToPentagonAssoc {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : mixedResidueHistoryClass s = mixedResidueHistoryClass t) :
    pentagonAssocHistoryClass s = pentagonAssocHistoryClass t := by
  rcases (mixedResidueHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (pentagonAssocHistoryClass_eq_iff s t).2 ⟨.previous q⟩

theorem pentagonAssocHistoryClass_strictlyNew (l r : W) :
    (pentagonAssocHistoryClass
      (sevenFourfoldInversePentagonThree l r) =
      pentagonAssocHistoryClass
        (sevenFourfoldInversePentagonTwo l r)) ∧
    (mixedResidueHistoryClass
      (sevenFourfoldInversePentagonThree l r) ≠
      mixedResidueHistoryClass
        (sevenFourfoldInversePentagonTwo l r)) :=
  ⟨(pentagonAssocHistoryClass_eq_iff _ _).2 ⟨.fourfoldPentagon⟩,
    sevenFourfoldInversePentagon_classGap l r⟩

/-- The old shape-sensitive Phi observer is NO LONGER invariant
on the selected new quotient: its actual values are 1 and 0. -/
theorem pentagonAssocHistoryClass_noPhiDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      pentagonAssocHistoryClass s = pentagonAssocHistoryClass t →
        sevenInversePentagonAssociatorCharge s =
          sevenInversePentagonAssociatorCharge t) := by
  intro preserve
  have hEq := (pentagonAssocHistoryClass_strictlyNew l r).1
  have h := preserve
    (sevenFourfoldInversePentagonThree l r)
    (sevenFourfoldInversePentagonTwo l r) hEq
  have vals := sevenFourfoldInversePentagon_chargeValues l r
  rw [vals.1, vals.2] at h
  norm_num at h

/-- New selected quotient with genuine ℤ-valued V mod2 descent. -/
def pentagonAssocHistoryV2 {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (pentagonAssocHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenTotalReductionParity s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact pentagonAssocEightCell_preservesVParity q)

def pentagonAssocHistoryR2 {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (pentagonAssocHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenIdentityParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (pentagonAssocEightCell_preservesRParity q))

def pentagonAssocHistoryU2 {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (pentagonAssocHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenUnitCountParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (pentagonAssocEightCell_preservesUParity q))

theorem pentagonAssocHistoryV2_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    pentagonAssocHistoryV2
      (pentagonAssocHistoryClass (long := long) (short := short) s) =
      sevenTotalReductionParity s := rfl

theorem pentagonAssocHistoryR2_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    pentagonAssocHistoryR2
      (pentagonAssocHistoryClass (long := long) (short := short) s) =
      decide (sevenIdentityParity s = 1) := rfl

theorem pentagonAssocHistoryU2_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    pentagonAssocHistoryU2
      (pentagonAssocHistoryClass (long := long) (short := short) s) =
      decide (sevenUnitCountParity s = 1) := rfl

/-- One concrete typed overlap between the one new fourfold-pentagon
comparison and the ALREADY PROVED old mixedResidue comparison. -/
def fourfoldMixedResidueFirst (l r : W) :
    SevenRewrite W l r
      (.trans (fourfoldInversePentagonSource l r)
        (mixedResidueSource (long := l) (short := r) r))
      (.trans (fourfoldInversePentagonTarget l r)
        (mixedResidueTarget (long := l) (short := r) r)) :=
  .congrComp (sevenFourfoldInversePentagonThree l r)
    (sevenMixedResidueFirst (long := l) (short := r) r)

def fourfoldMixedResidueSecond (l r : W) :
    SevenRewrite W l r
      (.trans (fourfoldInversePentagonSource l r)
        (mixedResidueSource (long := l) (short := r) r))
      (.trans (fourfoldInversePentagonTarget l r)
        (mixedResidueTarget (long := l) (short := r) r)) :=
  .congrComp (sevenFourfoldInversePentagonTwo l r)
    (sevenMixedResidueSecond (long := l) (short := r) r)

def fourfoldMixedResidue_fill (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .compositeContext (.fourfoldPentagon) (.previous (.mixedResidue r))

theorem fourfoldMixedResidue_noPrevious (l r : W) :
    ¬ Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r)) := by
  rintro ⟨q⟩
  have h := mixedResidueEightCell_preservesInversePentagonAssociatorCharge q
  change
    sevenInversePentagonAssociatorCharge
        (sevenFourfoldInversePentagonThree l r) +
      sevenInversePentagonAssociatorCharge
        (sevenMixedResidueFirst (long := l) (short := r) r) =
    sevenInversePentagonAssociatorCharge
        (sevenFourfoldInversePentagonTwo l r) +
      sevenInversePentagonAssociatorCharge
        (sevenMixedResidueSecond (long := l) (short := r) r) at h
  have v := sevenFourfoldInversePentagon_chargeValues l r
  have m := sevenMixedResidue_inversePentagonAssociatorValues
    (long := l) (short := r) r
  rw [v.1, v.2, m.1, m.2] at h
  norm_num at h

theorem fourfoldMixedResidue_newVsOld (l r : W) :
    Nonempty (PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r)) ∧
    ¬ Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r)) ∧
    sevenTotalReductionParity (fourfoldMixedResidueFirst l r) =
      sevenTotalReductionParity (fourfoldMixedResidueSecond l r) :=
  ⟨⟨fourfoldMixedResidue_fill l r⟩,
    fourfoldMixedResidue_noPrevious l r,
    pentagonAssocEightCell_preservesVParity (fourfoldMixedResidue_fill l r)⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77FourfoldPentagonCompletion
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

/-- The SAME independent one-primitive higher presentation exists at
each original P77 final raw index, using actual source long/short
five-cell values, without claiming source strict equality. -/
theorem pentagonActualFourfoldPentagonCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.PentagonAssocEightCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.sevenFourfoldInversePentagonThree
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
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
  refine ⟨⟨PentagonAdjoinedSixCell.PentagonAssocEightCell.fourfoldPentagon⟩,
    PentagonAdjoinedSixCell.sevenFourfoldInversePentagon_noMixedResidueComparison
      _ _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.PentagonAssocEightCell
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_refl
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_preservesVParity
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_preservesRParity
#print axioms PentagonAdjoinedSixCell.pentagonAssocEightCell_preservesUParity
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistorySetoid
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryClass
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.mixedResidueHistoryClass_descendsToPentagonAssoc
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryClass_noPhiDescent
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryV2
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryR2
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryU2
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryV2_onClass
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryR2_onClass
#print axioms PentagonAdjoinedSixCell.pentagonAssocHistoryU2_onClass
#print axioms PentagonAdjoinedSixCell.fourfoldMixedResidueFirst
#print axioms PentagonAdjoinedSixCell.fourfoldMixedResidueSecond
#print axioms PentagonAdjoinedSixCell.fourfoldMixedResidue_fill
#print axioms PentagonAdjoinedSixCell.fourfoldMixedResidue_noPrevious
#print axioms PentagonAdjoinedSixCell.fourfoldMixedResidue_newVsOld
#print axioms pentagonActualFourfoldPentagonCompletion

end ActualOriginalP77FourfoldPentagonCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
