import KUOS.Architecture.QiWuxingGK5CHP77FourfoldMixedCriticalDiamondV5_10

/-!
Qi v5.11 — MINIMAL TYPED NINTH-CELL COMPLETION OF THE ACTUAL
ORIGINAL FOURFOLD-PENTAGON AND MIXED-RESIDUE CRITICAL DIAMOND.

Qi v5.10 proved that the two genuine eighth-cell completion
histories P-then-M and M-then-P have precisely the same typed
SevenRewrite endpoints but are different ORIGINAL free eighth
proof values, distinguished by event order [P,M] versus [M,P].

Add ONE independent, explicitly typed primitive ninth comparison
only between those two genuine eighth-cell values. Retain raw
eighth proofs and all old source data. Close under strict-equality
witnesses, direction reversal, chains, and the matching eighth-cell
contexts. No global thinness is introduced.

Prove that the selected new quotient identifies these two eighth
histories although their raw strict equality is impossible.
Event ORDER no longer descends. Nevertheless each separate
primitive event MULTIPLICITY descends, by full constructor
induction, and gives a new concrete obstruction: the raw
pentagon-comparison roundtrip is NOT ninth-comparable to
the old reflexive eighth comparison. A universal ninth comparison
interpreter is therefore impossible in the chosen free presentation.

This is a mathematical construction of a selected comparison
presentation, not proof of pre-existing canonical ninth-cell
coherence, nor source-level seven/eighth equality.
No old Lean edits, no added axioms, no assumptions weakened.
append-only / tighten-only / overwrite-forbidden / same-root.
root107, pinned Lean v4.30.0-rc2 and mathlib
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

/-- Ninth-cell grammar between two actual eighth-cell proof VALUES.
The only genuinely new primitive is the selected P/M interchange.
The equality constructor merely retains reflexivity of old proofs.
Every other constructor is typed structural closure, not an
unrestricted comparison between arbitrary parallel eighth cells. -/
inductive FourfoldMixedNineCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    PentagonAssocEightCell W l r s t →
    PentagonAssocEightCell W l r s t → Type uSix where
  | strict {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (heq : q = q') : FourfoldMixedNineCell W l r q q'
  | interchange :
      FourfoldMixedNineCell W l r
        (fourfoldMixedCriticalPThenM l r)
        (fourfoldMixedCriticalMThenP l r)
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q') :
      FourfoldMixedNineCell W l r q' q
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' q'' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q')
      (beta : FourfoldMixedNineCell W l r q' q'') :
      FourfoldMixedNineCell W l r q q''
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q') :
      FourfoldMixedNineCell W l r (.reverse q) (.reverse q')
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      (alpha : FourfoldMixedNineCell W l r q q')
      (beta : FourfoldMixedNineCell W l r b b') :
      FourfoldMixedNineCell W l r (.chain q b) (.chain q' b')
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q') :
      FourfoldMixedNineCell W l r
        (.whiskerLeft before q) (.whiskerLeft before q')
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q')
      (after : SevenRewrite W l r d e) :
      FourfoldMixedNineCell W l r
        (.whiskerRight q after) (.whiskerRight q' after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q') :
      FourfoldMixedNineCell W l r
        (.inverseContext q) (.inverseContext q')
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      {q q' : PentagonAssocEightCell W l r s s'}
      {b b' : PentagonAssocEightCell W l r t t'}
      (alpha : FourfoldMixedNineCell W l r q q')
      (beta : FourfoldMixedNineCell W l r b b') :
      FourfoldMixedNineCell W l r
        (.compositeContext q b) (.compositeContext q' b')

def fourfoldMixedNineCell_ofStrict {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (heq : q = q') :
    FourfoldMixedNineCell W long short q q' :=
  .strict heq

def fourfoldMixedNineCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    FourfoldMixedNineCell W long short q q :=
  .strict rfl

/-- Exact new primitive is inhabited, while original raw equality
between these two eighth proofs is PROVED impossible in v5.10. -/
theorem fourfoldMixedNineCell_strictlyNew (l r : W) :
    Nonempty (FourfoldMixedNineCell W l r
      (fourfoldMixedCriticalPThenM l r)
      (fourfoldMixedCriticalMThenP l r)) ∧
    fourfoldMixedCriticalPThenM l r ≠
      fourfoldMixedCriticalMThenP l r :=
  ⟨⟨.interchange⟩, fourfoldMixedCriticalRawEightGap l r⟩

theorem fourfoldMixedNineCell_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      FourfoldMixedNineCell W l r q q' → q = q') := by
  intro interpret
  exact fourfoldMixedCriticalRawEightGap l r
    (interpret _ _ (.interchange))

/-- Selected setoid on the ACTUAL free eighth proof Type, not on
the original source six or seven values. -/
def fourfoldMixedNinthSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d} :
    Setoid (PentagonAssocEightCell W l r s t) where
  r := fun q q' => Nonempty (FourfoldMixedNineCell W l r q q')
  iseqv := by
    constructor
    · intro q
      exact ⟨.strict rfl⟩
    · intro q q' h
      rcases h with ⟨alpha⟩
      exact ⟨.reverse alpha⟩
    · intro q q' q'' h h'
      rcases h with ⟨alpha⟩
      rcases h' with ⟨beta⟩
      exact ⟨.chain alpha beta⟩

def fourfoldMixedNinthClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    Quotient (fourfoldMixedNinthSetoid W long short (s := s) (t := t)) :=
  Quotient.mk _ q

theorem fourfoldMixedNinthClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q q' : PentagonAssocEightCell W long short s t) :
    fourfoldMixedNinthClass q = fourfoldMixedNinthClass q' ↔
      Nonempty (FourfoldMixedNineCell W long short q q') := by
  constructor
  · intro heq
    exact Quotient.exact heq
  · intro h
    exact Quotient.sound h

theorem fourfoldMixedNinthClass_selectedGap (l r : W) :
    (fourfoldMixedNinthClass (fourfoldMixedCriticalPThenM l r) =
      fourfoldMixedNinthClass (fourfoldMixedCriticalMThenP l r)) ∧
    (fourfoldMixedCriticalPThenM l r ≠
      fourfoldMixedCriticalMThenP l r) :=
  ⟨(fourfoldMixedNinthClass_eq_iff _ _).2 ⟨.interchange⟩,
    fourfoldMixedCriticalRawEightGap l r⟩

/-- No global recovery map from the chosen ninth quotient to
every ORIGINAL raw eighth proof can be a left inverse. -/
theorem fourfoldMixedNinthClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
      Quotient (fourfoldMixedNinthSetoid W l r
        (s := fourfoldMixedResidueFirst l r)
        (t := fourfoldMixedResidueSecond l r)) →
      PentagonAssocEightCell W l r
        (fourfoldMixedResidueFirst l r)
        (fourfoldMixedResidueSecond l r)),
      ∀ (q : PentagonAssocEightCell W l r
        (fourfoldMixedResidueFirst l r)
        (fourfoldMixedResidueSecond l r)),
        decode (fourfoldMixedNinthClass q) = q := by
  rintro ⟨decode, inverse⟩
  apply fourfoldMixedCriticalRawEightGap l r
  calc
    fourfoldMixedCriticalPThenM l r =
        decode (fourfoldMixedNinthClass (fourfoldMixedCriticalPThenM l r)) :=
      (inverse _).symm
    _ = decode (fourfoldMixedNinthClass (fourfoldMixedCriticalMThenP l r)) :=
      congrArg decode (fourfoldMixedNinthClass_selectedGap l r).1
    _ = fourfoldMixedCriticalMThenP l r := inverse _

/-- Count a specified original generator kind without identifying
its position in the ORIGINAL ordered trace. -/
def ninthPrimitiveEventCount (b : Bool) : List Bool → Nat
  | [] => 0
  | x :: xs => (if x == b then 1 else 0) + ninthPrimitiveEventCount b xs

theorem ninthPrimitiveEventCount_append (b : Bool)
    (xs ys : List Bool) :
    ninthPrimitiveEventCount b (xs ++ ys) =
      ninthPrimitiveEventCount b xs +
        ninthPrimitiveEventCount b ys := by
  induction xs with
  | nil => simp only [List.nil_append, ninthPrimitiveEventCount, Nat.zero_add]
  | cons x xs ih =>
      simp only [List.cons_append, ninthPrimitiveEventCount, ih]
      omega

theorem ninthPrimitiveEventCount_reverse (b : Bool)
    (xs : List Bool) :
    ninthPrimitiveEventCount b xs.reverse =
      ninthPrimitiveEventCount b xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      simp only [List.reverse_cons, ninthPrimitiveEventCount_append,
        ninthPrimitiveEventCount, ih]
      omega

/-- This observer is proved invariant under ALL nine-cell
constructors: old Eq, one new interchange, both comparison
directions, chains, reverse-context, whiskers, inverse and
composite contexts. -/
theorem fourfoldMixedNineCell_preservesEventCount (b : Bool)
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : FourfoldMixedNineCell W long short q q') :
    ninthPrimitiveEventCount b (pentagonAssocPrimitiveTrace q) =
      ninthPrimitiveEventCount b (pentagonAssocPrimitiveTrace q') := by
  induction alpha with
  | strict heq =>
      cases heq
      rfl
  | interchange =>
      rw [(fourfoldMixedCriticalTraceValues _ _).1,
        (fourfoldMixedCriticalTraceValues _ _).2]
      cases b <;> decide
  | reverse alpha ih => exact ih.symm
  | chain alpha beta ih ih' => exact ih.trans ih'
  | reverseContext alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_reverse] using ih
  | chainContext alpha beta ih ih' =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_append] using congrArg₂ Nat.add ih ih'
  | whiskerLeft before alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | whiskerRight alpha after ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | inverseContext alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | compositeContext alpha beta ih ih' =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_append] using congrArg₂ Nat.add ih ih'

/-- Both counts (P=true and M=false), not only their sum,
genuinely descend to the SELECTED ninth-cell quotient. -/
def fourfoldMixedNinthEventCount (b : Bool)
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d} :
    Quotient (fourfoldMixedNinthSetoid W long short (s := s) (t := t)) →
      Nat :=
  Quotient.lift
    (fun q : PentagonAssocEightCell W long short s t =>
      ninthPrimitiveEventCount b (pentagonAssocPrimitiveTrace q))
    (by
      intro q q' h
      rcases h with ⟨alpha⟩
      exact fourfoldMixedNineCell_preservesEventCount b alpha)

theorem fourfoldMixedNinthEventCount_onClass (b : Bool)
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    fourfoldMixedNinthEventCount b (fourfoldMixedNinthClass q) =
      ninthPrimitiveEventCount b (pentagonAssocPrimitiveTrace q) := rfl

theorem fourfoldMixedNinthSelectedEventCounts (l r : W) :
    fourfoldMixedNinthEventCount true
        (fourfoldMixedNinthClass (fourfoldMixedCriticalPThenM l r)) = 1 ∧
    fourfoldMixedNinthEventCount false
        (fourfoldMixedNinthClass (fourfoldMixedCriticalPThenM l r)) = 1 ∧
    fourfoldMixedNinthEventCount true
        (fourfoldMixedNinthClass (fourfoldMixedCriticalMThenP l r)) = 1 ∧
    fourfoldMixedNinthEventCount false
        (fourfoldMixedNinthClass (fourfoldMixedCriticalMThenP l r)) = 1 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    simp only [fourfoldMixedNinthEventCount_onClass,
      (fourfoldMixedCriticalTraceValues l r).1,
      (fourfoldMixedCriticalTraceValues l r).2] <;>
    rfl

/-- Ordered event trace is NOT a well-defined observer on the
selected ninth quotient: the exact two histories are identified
but have different raw trace order. -/
theorem fourfoldMixedNinthClass_noOrderedTraceDescent (l r : W) :
    ¬ ∃ (observe :
      Quotient (fourfoldMixedNinthSetoid W l r
        (s := fourfoldMixedResidueFirst l r)
        (t := fourfoldMixedResidueSecond l r)) → List Bool),
      ∀ (q : PentagonAssocEightCell W l r
        (fourfoldMixedResidueFirst l r)
        (fourfoldMixedResidueSecond l r)),
        observe (fourfoldMixedNinthClass q) =
          pentagonAssocPrimitiveTrace q := by
  rintro ⟨observe, compatible⟩
  have heq := congrArg observe
    (fourfoldMixedNinthClass_selectedGap l r).1
  rw [compatible, compatible,
      (fourfoldMixedCriticalTraceValues l r).1,
      (fourfoldMixedCriticalTraceValues l r).2] at heq
  cases heq

/-- The freely generated strict eighth-cell proof of a pentagon
comparison followed by its REVERSE. It has the same seven-cell
endpoints as a reflexive comparison but TWO P events. -/
def ninthPentagonRoundtrip (l r : W) :
    PentagonAssocEightCell W l r
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonThree l r) :=
  .chain (.fourfoldPentagon) (.reverse (.fourfoldPentagon))

def ninthPentagonReflexive (l r : W) :
    PentagonAssocEightCell W l r
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonThree l r) :=
  pentagonAssocEightCell_refl (sevenFourfoldInversePentagonThree l r)

theorem ninthPentagonRoundtripVsReflexiveCounts (l r : W) :
    ninthPrimitiveEventCount true
      (pentagonAssocPrimitiveTrace (ninthPentagonRoundtrip l r)) = 2 ∧
    ninthPrimitiveEventCount true
      (pentagonAssocPrimitiveTrace (ninthPentagonReflexive l r)) = 0 := by
  constructor <;> rfl

/-- Genuine RESIDUAL ninth obstruction after adding the one
interchange: no chosen ninth proof can connect the pentagon
roundtrip with an old reflexive eighth proof. This prevents
arbitrary-parallel-eighth-cell global thinness. -/
theorem ninthPentagonRoundtrip_noNineComparison (l r : W) :
    ¬ Nonempty (FourfoldMixedNineCell W l r
      (ninthPentagonRoundtrip l r)
      (ninthPentagonReflexive l r)) := by
  rintro ⟨alpha⟩
  have h := fourfoldMixedNineCell_preservesEventCount true alpha
  have vals := ninthPentagonRoundtripVsReflexiveCounts l r
  rw [vals.1, vals.2] at h
  omega

theorem ninthPentagonRoundtrip_distinctClass (l r : W) :
    fourfoldMixedNinthClass (ninthPentagonRoundtrip l r) ≠
      fourfoldMixedNinthClass (ninthPentagonReflexive l r) := by
  intro heq
  exact ninthPentagonRoundtrip_noNineComparison l r
    ((fourfoldMixedNinthClass_eq_iff _ _).1 heq)

/-- A restricted local completion does not yield a universal
nine-cell interpreter, even though its selected source P/M
critical square is now compared by a genuine typed ninth cell. -/
theorem fourfoldMixedNineCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      Nonempty (FourfoldMixedNineCell W l r q q')) := by
  intro interpret
  exact ninthPentagonRoundtrip_noNineComparison l r
    (interpret _ _)

/-- The actual v5.10 overlapping fourfold pentagon / mixed-residue
two routes are compared by one primitive but preserve the proven
v5.09 V/R/U mod-two observations on their seven-cell endpoints. -/
theorem fourfoldMixedNineCell_observationCompatibility (l r : W) :
    Nonempty (FourfoldMixedNineCell W l r
      (fourfoldMixedCriticalPThenM l r)
      (fourfoldMixedCriticalMThenP l r)) ∧
    sevenTotalReductionParity (fourfoldMixedResidueFirst l r) =
      sevenTotalReductionParity (fourfoldMixedResidueSecond l r) ∧
    sevenIdentityParity (fourfoldMixedResidueFirst l r) =
      sevenIdentityParity (fourfoldMixedResidueSecond l r) ∧
    sevenUnitCountParity (fourfoldMixedResidueFirst l r) =
      sevenUnitCountParity (fourfoldMixedResidueSecond l r) :=
  ⟨⟨.interchange⟩,
    (fourfoldMixedCriticalParityCompatibility l r).1,
    (fourfoldMixedCriticalParityCompatibility l r).2.1,
    (fourfoldMixedCriticalParityCompatibility l r).2.2⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77FourfoldMixedNinthCompletion
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

/-- At EVERY original P77 final raw index, the selected ninth-cell
comparison exists on the true GK5CG-sourced long/short Type values,
without asserting the ORIGINAL source's strict equality. -/
theorem pentagonActualFourfoldMixedNinthCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.FourfoldMixedNineCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.fourfoldMixedCriticalPThenM
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.fourfoldMixedCriticalMThenP
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.interchange⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.FourfoldMixedNineCell
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_ofStrict
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_refl
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthSetoid
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthClass
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthClass_selectedGap
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthClass_noRawRetraction
#print axioms PentagonAdjoinedSixCell.ninthPrimitiveEventCount
#print axioms PentagonAdjoinedSixCell.ninthPrimitiveEventCount_append
#print axioms PentagonAdjoinedSixCell.ninthPrimitiveEventCount_reverse
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_preservesEventCount
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthEventCount
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthEventCount_onClass
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthSelectedEventCounts
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNinthClass_noOrderedTraceDescent
#print axioms PentagonAdjoinedSixCell.ninthPentagonRoundtrip
#print axioms PentagonAdjoinedSixCell.ninthPentagonReflexive
#print axioms PentagonAdjoinedSixCell.ninthPentagonRoundtripVsReflexiveCounts
#print axioms PentagonAdjoinedSixCell.ninthPentagonRoundtrip_noNineComparison
#print axioms PentagonAdjoinedSixCell.ninthPentagonRoundtrip_distinctClass
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_observationCompatibility
#print axioms pentagonActualFourfoldMixedNinthCompletion

end ActualOriginalP77FourfoldMixedNinthCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
