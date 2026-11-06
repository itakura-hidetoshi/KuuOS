import KUOS.Architecture.QiWuxingGK5CHP77AdjoinedSixCellPresentationV4_86

/-!
Qi v4.87 — FREE SIX-CELL PROOF WORDS, COHERENCE QUOTIENT,
AND CONDITIONALLY DESCENDING OBSERVATIONS.

The v4.86 six-cell grammar is a NEW presentation. Its raw constructor
words are not definitionally or strictly equal under cancellation.
A signed degree gives an explicit, separately defined coherence relation
on parallel words. The quotient of proof words by that relation has
well-defined identity, composition and inverse, with groupoid laws
PROVED in the quotient, not postulated in the old GK5CG source.

For a map from original five-cell values into any observation type,
the new six-cell words descend to equality of observations IFF the
observation identifies the two actual original long/short values.
The v4.85 strict inequality therefore obstructs every such descent
through an INJECTIVE observation, without obstructing coarser ones.
We also exhibit the new endpoint quotient and its universal factor map.

This neither adds six-cells to old F55/P77/GK5CG nor asserts strict
six-cell word laws. Original source authority is unchanged.
Append-only / tighten-only / same-root; strict 空 center;
independent Kuu is presentation. Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6;
public root count 107. Protected PR #1558 stays Draft/unmerged.
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

universe uD vD uE vE uSix uObs
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

/-- A signed syntactic invariant of words in the NEW six-cell grammar.
The old GK5CG source does not carry this sixth-dimensional degree. -/
def degree {w z : W} : PentagonAdjoinedSixCell W long short w z → ℤ
  | .refl _ => 0
  | .symm c => -degree c
  | .trans c d => degree c + degree d
  | .pentagon => 1

/-- Coherence of parallel six-cell proof words is an explicitly CHOSEN
relation, not Lean equality of raw words and not old five-cell equality. -/
def DegreeCoherent {w z : W}
    (c d : PentagonAdjoinedSixCell W long short w z) : Prop :=
  degree c = degree d

theorem degreeCoherent_refl {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DegreeCoherent c c := rfl

theorem degreeCoherent_symm {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (hc : DegreeCoherent c d) :
    DegreeCoherent (.symm c) (.symm d) := by
  change -(degree c) = -(degree d)
  exact congrArg (fun t : ℤ => -t) hc

theorem degreeCoherent_comp {w x z : W}
    {c c' : PentagonAdjoinedSixCell W long short w x}
    {d d' : PentagonAdjoinedSixCell W long short x z}
    (hc : DegreeCoherent c c') (hd : DegreeCoherent d d') :
    DegreeCoherent (.trans c d) (.trans c' d') := by
  change degree c + degree d = degree c' + degree d'
  exact congrArg₂ (· + ·) hc hd

theorem degreeCoherent_leftUnit {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DegreeCoherent (.trans (.refl w) c) c := by
  change (0 : ℤ) + degree c = degree c
  exact zero_add _

theorem degreeCoherent_rightUnit {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DegreeCoherent (.trans c (.refl z)) c := by
  change degree c + (0 : ℤ) = degree c
  exact add_zero _

theorem degreeCoherent_assoc {w x y z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x y)
    (e : PentagonAdjoinedSixCell W long short y z) :
    DegreeCoherent (.trans (.trans c d) e)
      (.trans c (.trans d e)) := by
  change (degree c + degree d) + degree e =
    degree c + (degree d + degree e)
  exact add_assoc _ _ _

theorem degreeCoherent_inverseRight {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DegreeCoherent (.trans c (.symm c)) (.refl w) := by
  change degree c + -(degree c) = (0 : ℤ)
  exact add_neg_cancel _

theorem degreeCoherent_inverseLeft {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DegreeCoherent (.trans (.symm c) c) (.refl z) := by
  change -(degree c) + degree c = (0 : ℤ)
  exact neg_add_cancel _

theorem degreeCoherent_doubleInverse {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    DegreeCoherent (.symm (.symm c)) c := by
  change -(-(degree c)) = degree c
  exact neg_neg _

/-- The fresh raw six-cell grammar does NOT satisfy cancellation as a
strict equality of constructor words, even for the adjoined generator. -/
theorem raw_inverseCancellation_notStrict (l r : W) :
    (show PentagonAdjoinedSixCell W l r l l from
      .trans (.pentagon) (.symm (.pentagon))) ≠
      (PentagonAdjoinedSixCell.refl l) := by
  intro hEq
  cases hEq

/-- Quotient of PARALLEL proof words by signed-degree coherence.
A seventh-dimensional equality is not attributed to the old source. -/
abbrev CoherentHom (W : Type uSix) (l r w z : W) : Type uSix :=
  Quot (fun c d : PentagonAdjoinedSixCell W l r w z => DegreeCoherent c d)

def homMk {w z : W} (c : PentagonAdjoinedSixCell W long short w z) :
    CoherentHom W long short w z :=
  Quot.mk _ c

def homId (w : W) : CoherentHom W long short w w :=
  homMk (.refl w)

def homInv {w z : W} (c : CoherentHom W long short w z) :
    CoherentHom W long short z w :=
  Quot.liftOn c (fun a => homMk (.symm a)) (by
    intro a b hab
    exact Quot.sound (degreeCoherent_symm hab))

def homComp {w x z : W}
    (c : CoherentHom W long short w x)
    (d : CoherentHom W long short x z) :
    CoherentHom W long short w z :=
  Quot.liftOn₂ c d (fun a b => homMk (.trans a b)) (by
    intro a a' b b' ha hb
    exact Quot.sound (degreeCoherent_comp ha hb))

theorem hom_leftUnit {w z : W}
    (c : CoherentHom W long short w z) :
    homComp (homId w) c = c := by
  refine Quot.inductionOn c ?_
  intro a
  exact Quot.sound (degreeCoherent_leftUnit a)

theorem hom_rightUnit {w z : W}
    (c : CoherentHom W long short w z) :
    homComp c (homId z) = c := by
  refine Quot.inductionOn c ?_
  intro a
  exact Quot.sound (degreeCoherent_rightUnit a)

theorem hom_assoc {w x y z : W}
    (c : CoherentHom W long short w x)
    (d : CoherentHom W long short x y)
    (e : CoherentHom W long short y z) :
    homComp (homComp c d) e = homComp c (homComp d e) := by
  refine Quot.inductionOn c ?_
  intro a
  refine Quot.inductionOn d ?_
  intro b
  refine Quot.inductionOn e ?_
  intro t
  exact Quot.sound (degreeCoherent_assoc a b t)

theorem hom_inverseRight {w z : W}
    (c : CoherentHom W long short w z) :
    homComp c (homInv c) = homId w := by
  refine Quot.inductionOn c ?_
  intro a
  exact Quot.sound (degreeCoherent_inverseRight a)

theorem hom_inverseLeft {w z : W}
    (c : CoherentHom W long short w z) :
    homComp (homInv c) c = homId z := by
  refine Quot.inductionOn c ?_
  intro a
  exact Quot.sound (degreeCoherent_inverseLeft a)

theorem hom_doubleInverse {w z : W}
    (c : CoherentHom W long short w z) :
    homInv (homInv c) = c := by
  refine Quot.inductionOn c ?_
  intro a
  exact Quot.sound (degreeCoherent_doubleInverse a)

/-- The exact necessary-and-sufficient gate for an observation of old
endpoint VALUES to respect EVERY fresh six-cell word. -/
theorem observationDescent_iff (l r : W) {X : Type uObs}
    (observe : W → X) :
    (∀ (w z : W), PentagonAdjoinedSixCell W l r w z →
      observe w = observe z) ↔ observe l = observe r := by
  constructor
  · intro h
    exact h l r (.pentagon)
  · intro hp w z c
    induction c with
    | refl _ => rfl
    | symm c ih => exact ih.symm
    | trans c d ihc ihd => exact ihc.trans ihd
    | pentagon => exact hp

theorem noInjectiveObservationDescent (l r : W)
    (hNe : l ≠ r) {X : Type uObs}
    (observe : W → X) (hInj : Function.Injective observe) :
    ¬ (∀ (w z : W), PentagonAdjoinedSixCell W l r w z →
      observe w = observe z) := by
  intro h
  exact hNe (hInj (h l r (.pentagon)))

/-- A distinct quotient of the original five-cell endpoint values.
It is an observation target, NOT old strict equality. -/
abbrev EndpointQuot (W : Type uSix) (l r : W) : Type uSix :=
  Quot (fun w z : W => Nonempty (PentagonAdjoinedSixCell W l r w z))

def endpointMk (l r : W) (w : W) : EndpointQuot W l r :=
  Quot.mk _ w

theorem endpointSound (l r : W) {w z : W}
    (c : PentagonAdjoinedSixCell W l r w z) :
    endpointMk l r w = endpointMk l r z :=
  Quot.sound ⟨c⟩

theorem endpointGeneratorEq (l r : W) :
    endpointMk l r l = endpointMk l r r :=
  endpointSound l r (.pentagon)

theorem endpointMk_notInjective (l r : W) (hNe : l ≠ r) :
    ¬ Function.Injective (endpointMk l r) := by
  intro hInj
  exact hNe (hInj (endpointGeneratorEq l r))

/-- Every observation satisfying the precise generator gate factors
through the NEW endpoint quotient. This does not return to source Eq. -/
def endpointLift (l r : W) {X : Type uObs}
    (observe : W → X) (hp : observe l = observe r) :
    EndpointQuot W l r → X :=
  Quot.lift observe (by
    intro w z hRel
    rcases hRel with ⟨c⟩
    exact (observationDescent_iff l r observe).2 hp w z c)

theorem endpointLift_mk (l r : W) {X : Type uObs}
    (observe : W → X) (hp : observe l = observe r) (w : W) :
    endpointLift l r observe hp (endpointMk l r w) = observe w :=
  rfl

end PentagonAdjoinedSixCell

section ActualSourceSixCellWordCoherence
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

/-- The actual source-indexed new roundtrip coheres with identity in
the quotient; it is not strict raw-word equality. -/
theorem pentagonActualSixCell_roundtrip_degreeCoherent
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    PentagonAdjoinedSixCell.DegreeCoherent
      (pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i)
      (.refl (pentagonLongConservativeFiveCell f g h k A B C D₄ i)) := by
  exact PentagonAdjoinedSixCell.degreeCoherent_inverseRight
    (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)

/-- The same actual roundtrip is NOT the strict raw identity word. -/
theorem pentagonActualSixCell_roundtrip_notStrict
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i ≠
      (PentagonAdjoinedSixCell.refl
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)) := by
  intro heq
  cases heq

/-- Exact conditional observation-descent gate at EVERY actual raw
P77 index. The observed type may be strictly coarser than the old W. -/
theorem pentagonActualSixCell_observationDescent_iff
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {X : Type uObs}
    (observe : pentagonFinalConservativeLoop f g h k i → X) :
    (∀ (w z : pentagonFinalConservativeLoop f g h k i),
      pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z →
      observe w = observe z) ↔
    observe (pentagonLongConservativeFiveCell f g h k A B C D₄ i) =
      observe (pentagonShortConservativeFiveCell f g h k A B C D₄ i) :=
  PentagonAdjoinedSixCell.observationDescent_iff
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    observe

/-- v4.85 prevents interpreting ALL new six-cell words into any
injective observation of the ACTUAL original five-cell values. -/
theorem pentagonActualSixCell_noInjectiveObservationDescent
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {X : Type uObs}
    (observe : pentagonFinalConservativeLoop f g h k i → X)
    (hInj : Function.Injective observe) :
    ¬ (∀ (w z : pentagonFinalConservativeLoop f g h k i),
      pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z →
      observe w = observe z) := by
  exact PentagonAdjoinedSixCell.noInjectiveObservationDescent
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i)
    observe hInj

/-- The ACTUAL old long/short values become equal only in the NEW,
separately constructed endpoint quotient. -/
theorem pentagonActualSixCell_endpointQuotEq
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    PentagonAdjoinedSixCell.endpointMk
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i) =
    PentagonAdjoinedSixCell.endpointMk
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i) :=
  PentagonAdjoinedSixCell.endpointGeneratorEq _ _

#print axioms PentagonAdjoinedSixCell.degree
#print axioms PentagonAdjoinedSixCell.DegreeCoherent
#print axioms PentagonAdjoinedSixCell.degreeCoherent_assoc
#print axioms PentagonAdjoinedSixCell.raw_inverseCancellation_notStrict
#print axioms PentagonAdjoinedSixCell.homComp
#print axioms PentagonAdjoinedSixCell.hom_leftUnit
#print axioms PentagonAdjoinedSixCell.hom_rightUnit
#print axioms PentagonAdjoinedSixCell.hom_assoc
#print axioms PentagonAdjoinedSixCell.hom_inverseRight
#print axioms PentagonAdjoinedSixCell.hom_inverseLeft
#print axioms PentagonAdjoinedSixCell.hom_doubleInverse
#print axioms PentagonAdjoinedSixCell.observationDescent_iff
#print axioms PentagonAdjoinedSixCell.noInjectiveObservationDescent
#print axioms PentagonAdjoinedSixCell.endpointGeneratorEq
#print axioms PentagonAdjoinedSixCell.endpointLift
#print axioms pentagonActualSixCell_roundtrip_degreeCoherent
#print axioms pentagonActualSixCell_roundtrip_notStrict
#print axioms pentagonActualSixCell_observationDescent_iff
#print axioms pentagonActualSixCell_noInjectiveObservationDescent
#print axioms pentagonActualSixCell_endpointQuotEq

end ActualSourceSixCellWordCoherence
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
