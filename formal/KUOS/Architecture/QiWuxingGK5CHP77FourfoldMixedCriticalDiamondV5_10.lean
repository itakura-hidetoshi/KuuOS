import KUOS.Architecture.QiWuxingGK5CHP77FourfoldPentagonMinimalHigherCompletionV5_09

/-!
Qi v5.10 — ORIGINAL FOURFOLD-PENTAGON × MIXED-RESIDUE CRITICAL DIAMOND.

Use exactly the true Qi v5.08 three-/two-associator SevenRewrite
values and the original Qi v5.06 mixed-residue pair. Their four
type-correct congrComp combinations constitute a concrete critical
square in the same original, free sixth-cell source and target.

The two one-step branches (pentagon then mixed, or mixed then
pentagon) have an explicit common endpoint in the v5.09
PentagonAssocEightCell grammar. The pentagon-directed edges
remain IMPOSSIBLE in the predecessor MixedResidueEightCell
grammar, even though the mixed-directed edges already exist there.

For a precise next-level obstruction, trace the occurrences of
the two actual primitive types through the free eighth-cell proof
trees: true = the single newly adjoined fourfoldPentagon generator,
false = the original mixedResidue generator. All other old
generators and reflexive comparisons contribute no event.
The two completing eighth-cell proofs have traces [true,false]
and [false,true]; hence they are NOT strictly equal as original
free eighth-cell values. This is an obstruction to RAW proof
equality only, NOT a claim that a ninth-cell coherence is impossible
and NOT an additional ninth-cell constructor.

No changes to original F55/P77/GK5CG, previous independent
presentations, source strict Eq, or chosen history quotient.
No global thinness, no axioms. append-only / tighten-only /
overwrite-forbidden / same-root; root107.
Lean v4.30.0-rc2; pinned mathlib
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

universe uSix
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- North-east vertex: change the actual fourfold pentagon but
retain the original first mixed-residue history. -/
def fourfoldMixedCriticalNE (l r : W) :
    SevenRewrite W l r
      (.trans (fourfoldInversePentagonSource l r)
        (mixedResidueSource (long := l) (short := r) r))
      (.trans (fourfoldInversePentagonTarget l r)
        (mixedResidueTarget (long := l) (short := r) r)) :=
  .congrComp (sevenFourfoldInversePentagonTwo l r)
    (sevenMixedResidueFirst (long := l) (short := r) r)

/-- South-west vertex: change the actual mixed-residue history
but retain the original three-associator fourfold pentagon. -/
def fourfoldMixedCriticalSW (l r : W) :
    SevenRewrite W l r
      (.trans (fourfoldInversePentagonSource l r)
        (mixedResidueSource (long := l) (short := r) r))
      (.trans (fourfoldInversePentagonTarget l r)
        (mixedResidueTarget (long := l) (short := r) r)) :=
  .congrComp (sevenFourfoldInversePentagonThree l r)
    (sevenMixedResidueSecond (long := l) (short := r) r)

/-- Existing mixed-residue primitive, whiskered with reflexivity
of the original two-associator history. Entirely OLD eighth cell. -/
def fourfoldMixedCriticalOldEast (l r : W) :
    MixedResidueEightCell W l r
      (fourfoldMixedCriticalNE l r)
      (fourfoldMixedResidueSecond l r) :=
  .compositeContext
    (mixedResidueEightCell_refl (sevenFourfoldInversePentagonTwo l r))
    (.mixedResidue r)

/-- Existing mixed-residue primitive, whiskered with reflexivity
of the original three-associator history. Entirely OLD eighth cell. -/
def fourfoldMixedCriticalOldWest (l r : W) :
    MixedResidueEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedCriticalSW l r) :=
  .compositeContext
    (mixedResidueEightCell_refl (sevenFourfoldInversePentagonThree l r))
    (.mixedResidue r)

/-- NORTH: genuinely new fourfold-pentagon comparison with the
actual first mixed-residue seven-cell witness held fixed. -/
def fourfoldMixedCriticalNorth (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedCriticalNE l r) :=
  .compositeContext (.fourfoldPentagon)
    (.previous (mixedResidueEightCell_refl
      (sevenMixedResidueFirst (long := l) (short := r) r)))

/-- SOUTH: the same newly adjoined generator after the original
mixed-residue comparison. -/
def fourfoldMixedCriticalSouth (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedCriticalSW l r)
      (fourfoldMixedResidueSecond l r) :=
  .compositeContext (.fourfoldPentagon)
    (.previous (mixedResidueEightCell_refl
      (sevenMixedResidueSecond (long := l) (short := r) r)))

/-- Route 1: the actual new pentagon comparison, THEN the
pre-existing old mixed-residue comparison. -/
def fourfoldMixedCriticalPThenM (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .chain (fourfoldMixedCriticalNorth l r)
    (.previous (fourfoldMixedCriticalOldEast l r))

/-- Route 2: the pre-existing old mixed-residue comparison,
THEN the actual new pentagon comparison. -/
def fourfoldMixedCriticalMThenP (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .chain (.previous (fourfoldMixedCriticalOldWest l r))
    (fourfoldMixedCriticalSouth l r)

/-- The first genuinely new edge cannot exist in the old eighth
grammar: composing it with the already-existing old East edge
would contradict the v5.09 original diagonal obstruction. -/
theorem fourfoldMixedCriticalNorth_noOld (l r : W) :
    ¬ Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedCriticalNE l r)) := by
  rintro ⟨q⟩
  exact fourfoldMixedResidue_noPrevious l r
    ⟨.chain q (fourfoldMixedCriticalOldEast l r)⟩

/-- The second genuinely new edge also cannot exist in the old
grammar; compose after the original old West comparison. -/
theorem fourfoldMixedCriticalSouth_noOld (l r : W) :
    ¬ Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedCriticalSW l r)
      (fourfoldMixedResidueSecond l r)) := by
  rintro ⟨q⟩
  exact fourfoldMixedResidue_noPrevious l r
    ⟨.chain (fourfoldMixedCriticalOldWest l r) q⟩

/-- Local joinability in the NEW independent eighth grammar,
with a strictly OLD-versus-NEW distinction on the four edges.
This says nothing about equality between the two eighth proofs. -/
theorem fourfoldMixedCriticalLocalDiamond (l r : W) :
    Nonempty (PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedCriticalNE l r)) ∧
    Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedCriticalSW l r)) ∧
    Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedCriticalNE l r)
      (fourfoldMixedResidueSecond l r)) ∧
    Nonempty (PentagonAssocEightCell W l r
      (fourfoldMixedCriticalSW l r)
      (fourfoldMixedResidueSecond l r)) ∧
    ¬ Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedCriticalNE l r)) ∧
    ¬ Nonempty (MixedResidueEightCell W l r
      (fourfoldMixedCriticalSW l r)
      (fourfoldMixedResidueSecond l r)) :=
  ⟨⟨fourfoldMixedCriticalNorth l r⟩,
    ⟨fourfoldMixedCriticalOldWest l r⟩,
    ⟨fourfoldMixedCriticalOldEast l r⟩,
    ⟨fourfoldMixedCriticalSouth l r⟩,
    fourfoldMixedCriticalNorth_noOld l r,
    fourfoldMixedCriticalSouth_noOld l r⟩

/-- All four genuine vertices represent one element in the
v5.09 chosen quotient. Nothing is identified in raw SevenRewrite. -/
theorem fourfoldMixedCriticalClassDiamond (l r : W) :
    pentagonAssocHistoryClass (fourfoldMixedResidueFirst l r) =
      pentagonAssocHistoryClass (fourfoldMixedCriticalNE l r) ∧
    pentagonAssocHistoryClass (fourfoldMixedResidueFirst l r) =
      pentagonAssocHistoryClass (fourfoldMixedCriticalSW l r) ∧
    pentagonAssocHistoryClass (fourfoldMixedCriticalNE l r) =
      pentagonAssocHistoryClass (fourfoldMixedResidueSecond l r) ∧
    pentagonAssocHistoryClass (fourfoldMixedCriticalSW l r) =
      pentagonAssocHistoryClass (fourfoldMixedResidueSecond l r) :=
  ⟨(pentagonAssocHistoryClass_eq_iff _ _).2 ⟨fourfoldMixedCriticalNorth l r⟩,
    (pentagonAssocHistoryClass_eq_iff _ _).2
      ⟨.previous (fourfoldMixedCriticalOldWest l r)⟩,
    (pentagonAssocHistoryClass_eq_iff _ _).2
      ⟨.previous (fourfoldMixedCriticalOldEast l r)⟩,
    (pentagonAssocHistoryClass_eq_iff _ _).2 ⟨fourfoldMixedCriticalSouth l r⟩⟩

/-- A syntax-level event trace for the ORIGINAL mixed-residue
generator. Other existing primitives and old identities contribute
no event, but nested old occurrences retain their order. -/
def mixedResiduePrimitiveTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) : List Bool :=
  match q with
  | .previous _ => []
  | .mixedResidue _ => [false]
  | .reverse q => (mixedResiduePrimitiveTrace q).reverse
  | .chain q q' => mixedResiduePrimitiveTrace q ++ mixedResiduePrimitiveTrace q'
  | .whiskerLeft _ q => mixedResiduePrimitiveTrace q
  | .whiskerRight q _ => mixedResiduePrimitiveTrace q
  | .inverseContext q => mixedResiduePrimitiveTrace q
  | .compositeContext q q' =>
      mixedResiduePrimitiveTrace q ++ mixedResiduePrimitiveTrace q'

/-- Event trace for the ACTUAL two primitive types in the
independent v5.09 eighth grammar. This is NOT asserted to descend
through any future ninth-cell quotient. -/
def pentagonAssocPrimitiveTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) : List Bool :=
  match q with
  | .previous q => mixedResiduePrimitiveTrace q
  | .fourfoldPentagon => [true]
  | .reverse q => (pentagonAssocPrimitiveTrace q).reverse
  | .chain q q' => pentagonAssocPrimitiveTrace q ++ pentagonAssocPrimitiveTrace q'
  | .whiskerLeft _ q => pentagonAssocPrimitiveTrace q
  | .whiskerRight q _ => pentagonAssocPrimitiveTrace q
  | .inverseContext q => pentagonAssocPrimitiveTrace q
  | .compositeContext q q' =>
      pentagonAssocPrimitiveTrace q ++ pentagonAssocPrimitiveTrace q'

/-- Two concrete, type-correct fillings of the SAME critical
diamond, but with the two original primitive types in opposite
pasting orders. -/
theorem fourfoldMixedCriticalTraceValues (l r : W) :
    pentagonAssocPrimitiveTrace (fourfoldMixedCriticalPThenM l r) =
      [true, false] ∧
    pentagonAssocPrimitiveTrace (fourfoldMixedCriticalMThenP l r) =
      [false, true] := by
  constructor <;> rfl

/-- Residual HIGHER obstruction is only to strict RAW eighth-cell
proof equality. Local joinability was already positively proved;
no nonexistence claim for ninth-cell witnesses is made. -/
theorem fourfoldMixedCriticalRawEightGap (l r : W) :
    fourfoldMixedCriticalPThenM l r ≠
      fourfoldMixedCriticalMThenP l r := by
  intro heq
  have h := congrArg pentagonAssocPrimitiveTrace heq
  rw [(fourfoldMixedCriticalTraceValues l r).1,
    (fourfoldMixedCriticalTraceValues l r).2] at h
  cases h

/-- The completed diamond preserves all three genuinely descended
v5.09 observers, by the proven full-constructor invariance theorem.
The higher raw-proof obstruction is compatible with local descent. -/
theorem fourfoldMixedCriticalParityCompatibility (l r : W) :
    sevenTotalReductionParity (fourfoldMixedResidueFirst l r) =
      sevenTotalReductionParity (fourfoldMixedResidueSecond l r) ∧
    sevenIdentityParity (fourfoldMixedResidueFirst l r) =
      sevenIdentityParity (fourfoldMixedResidueSecond l r) ∧
    sevenUnitCountParity (fourfoldMixedResidueFirst l r) =
      sevenUnitCountParity (fourfoldMixedResidueSecond l r) :=
  ⟨pentagonAssocEightCell_preservesVParity (fourfoldMixedCriticalPThenM l r),
    pentagonAssocEightCell_preservesRParity (fourfoldMixedCriticalPThenM l r),
    pentagonAssocEightCell_preservesUParity (fourfoldMixedCriticalPThenM l r)⟩

#print axioms fourfoldMixedCriticalNE
#print axioms fourfoldMixedCriticalSW
#print axioms fourfoldMixedCriticalOldEast
#print axioms fourfoldMixedCriticalOldWest
#print axioms fourfoldMixedCriticalNorth
#print axioms fourfoldMixedCriticalSouth
#print axioms fourfoldMixedCriticalPThenM
#print axioms fourfoldMixedCriticalMThenP
#print axioms fourfoldMixedCriticalNorth_noOld
#print axioms fourfoldMixedCriticalSouth_noOld
#print axioms fourfoldMixedCriticalLocalDiamond
#print axioms fourfoldMixedCriticalClassDiamond
#print axioms mixedResiduePrimitiveTrace
#print axioms pentagonAssocPrimitiveTrace
#print axioms fourfoldMixedCriticalTraceValues
#print axioms fourfoldMixedCriticalRawEightGap
#print axioms fourfoldMixedCriticalParityCompatibility

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
