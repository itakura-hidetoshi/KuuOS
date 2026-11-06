import KUOS.Architecture.QiWuxingGK5CHP77SevenRewriteNormalizationCompletenessV4_90

/-!
Qi v4.91 — HISTORY-PRESERVING TYPE-VALUED EIGHT-CELL LOCAL COHERENCE.

The v4.89 SevenRewrite is a freely generated, thirteen-rule seventh-level
presentation of rewrites between ORIGINAL (unquotiented) six-cell words.
The v4.90 normalization shows existence and local completeness of its
SEVEN-cell comparisons when distinguished ORIGINAL GK5CG five-cell
endpoints differ. Existence does NOT make two distinct SevenRewrite
derivations definitionally equal.

This file freely adjoins a NEW EIGHT-cell Type indexed by both full
seven-cell proof histories. Its generators are specifically displayed
higher structural coherences: groupoid laws, congruence, functoriality,
independent-step interchange and the two ways to cancel c;c⁻¹;c.
There is NO constructor "all parallel seven-cell histories compare".
The zigzag diamond and interchange are explicit HIGHER generators,
not a consequence of strict equality of seven-cell raw syntax.

Crucially, an inhabited EightCell does NOT give strict equality of its
two original SevenRewrite indices. No extra GK5CG source five/six/seven/
eight-cell constructor or source equality interpreter is introduced.
No global eight-cell thinness or completeness is claimed.

Append-only / tighten-only / same-root; strict 空 center; independent
Kuu is presentation. Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6;
public roots107, protected #1558 Draft/open/unmerged.
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

/-- NEW freely generated eighth-level local coherence. Both indices
are actual, complete seventh-level derivation syntax, NOT their
quotient classes or their equality. Only the listed finite rules
produce eight-cell comparisons. -/
inductive EightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | reflexive {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) :
      EightCell W l r s s
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (e : EightCell W l r s t) :
      EightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (e : EightCell W l r s t) (e' : EightCell W l r t u) :
      EightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d)
      {t u : SevenRewrite W l r d e}
      (q : EightCell W l r t u) :
      EightCell W l r (.trans s t) (.trans s u)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : EightCell W l r s t)
      (u : SevenRewrite W l r d e) :
      EightCell W l r (.trans s u) (.trans t u)
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : EightCell W l r s t) :
      EightCell W l r (.symm s) (.symm t)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : EightCell W l r s t) :
      EightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : EightCell W l r s s')
      (q' : EightCell W l r t t') :
      EightCell W l r (.congrComp s t) (.congrComp s' t')
  | unitLeft {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) :
      EightCell W l r (.trans (.refl c) s) s
  | unitRight {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) :
      EightCell W l r (.trans s (.refl d)) s
  | associate {w z : W}
      {c d e f : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d)
      (t : SevenRewrite W l r d e)
      (u : SevenRewrite W l r e f) :
      EightCell W l r (.trans (.trans s t) u)
        (.trans s (.trans t u))
  | cancelRight {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) :
      EightCell W l r (.trans s (.symm s)) (.refl c)
  | cancelLeft {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) :
      EightCell W l r (.trans (.symm s) s) (.refl d)
  | involute {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) :
      EightCell W l r (.symm (.symm s)) s
  | inverseIdentity {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      EightCell W l r (.symm (.refl c)) (.refl c)
  | inverseComposite {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d)
      (t : SevenRewrite W l r d e) :
      EightCell W l r (.symm (.trans s t))
        (.trans (.symm t) (.symm s))
  | inverseCongruenceIdentity {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      EightCell W l r (.congrInv (.refl c)) (.refl (.symm c))
  | inverseCongruenceChain {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d)
      (t : SevenRewrite W l r d e) :
      EightCell W l r (.congrInv (.trans s t))
        (.trans (.congrInv s) (.congrInv t))
  | compositeCongruenceIdentity {w x z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x z) :
      EightCell W l r (.congrComp (.refl c) (.refl d))
        (.refl (.trans c d))
  | compositeCongruenceChain {w x z : W}
      {c₀ c₁ c₂ : PentagonAdjoinedSixCell W l r w x}
      {d₀ d₁ d₂ : PentagonAdjoinedSixCell W l r x z}
      (s : SevenRewrite W l r c₀ c₁)
      (s' : SevenRewrite W l r c₁ c₂)
      (t : SevenRewrite W l r d₀ d₁)
      (t' : SevenRewrite W l r d₁ d₂) :
      EightCell W l r
        (.congrComp (.trans s s') (.trans t t'))
        (.trans (.congrComp s t) (.congrComp s' t'))
  | interchange {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      (s : SevenRewrite W l r c c')
      (t : SevenRewrite W l r d d') :
      EightCell W l r
        (.trans (.congrComp s (.refl d))
          (.congrComp (.refl c') t))
        (.trans (.congrComp (.refl c) t)
          (.congrComp s (.refl d')))
  | zigzagDiamond {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      EightCell W l r
        (.trans
          (.congrComp (.inverseRight c) (.refl c))
          (.leftUnit c))
        (.trans (.assoc c (.symm c) c)
          (.trans
            (.congrComp (.refl c) (.inverseLeft c))
            (.rightUnit c)))

/-- Explicit equality of original seven-cell terms gives an eight-cell
reflexivity witness. The converse will be refuted below. -/
def eightCell_ofEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (eq : s = t) : EightCell W long short s t := by
  cases eq
  exact .reflexive s

/-- The second explicit seventh-level history for cancelling
(c ; c⁻¹) ; c: first reassociate, then cancel c⁻¹ ; c. -/
def sevenZigzagViaAssoc {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans c (.symm c)) c) c :=
  .trans (.assoc c (.symm c) c)
    (.trans
      (.congrComp (.refl c) (.inverseLeft c))
      (.rightUnit c))

/-- A concrete NEW eighth-level diamond joins the two actual
seventh-level proof histories without identifying their syntax. -/
def eightZigzagCoherence {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    EightCell W long short
      (sevenRewrite_zigzagRight c)
      (sevenZigzagViaAssoc c) :=
  .zigzagDiamond c

/-- The two distinct orders for independent local seventh-level
steps have a specified, nontrivial eighth-level interchange cell. -/
def eightIndependentInterchange {w x z : W}
    {c c' : PentagonAdjoinedSixCell W long short w x}
    {d d' : PentagonAdjoinedSixCell W long short x z}
    (s : SevenRewrite W long short c c')
    (t : SevenRewrite W long short d d') :
    EightCell W long short
      (.trans (.congrComp s (.refl d))
        (.congrComp (.refl c') t))
      (.trans (.congrComp (.refl c) t)
        (.congrComp s (.refl d'))) :=
  .interchange s t

/-- The two explicit seventh-level zigzag derivations are NOT
definitionally or propositionally equal as freely generated
SEVENTH-level raw syntax. Their comparison is genuinely higher. -/
theorem sevenZigzag_twoHistories_notStrict {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenRewrite_zigzagRight c ≠ sevenZigzagViaAssoc c := by
  intro heq
  cases heq

/-- The local zigzag diamond has an actual Type-valued eighth-cell
witness, even though the raw seventh-level histories differ. -/
theorem eightZigzag_exists_notStrict {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (EightCell W long short
      (sevenRewrite_zigzagRight c) (sevenZigzagViaAssoc c)) ∧
    sevenRewrite_zigzagRight c ≠ sevenZigzagViaAssoc c :=
  ⟨⟨eightZigzagCoherence c⟩, sevenZigzag_twoHistories_notStrict c⟩

/-- Even the new local EIGHT-cell coherence cannot be reinterpreted
as strict equality of all original seventh-level derivation words.
The elementary seventh-level left-unit coherence is a counterexample. -/
theorem eightCell_noStrictSevenInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      EightCell W l r s t → s = t) := by
  intro interpret
  let c : PentagonAdjoinedSixCell W l r l l := .refl l
  have hBad :
      (SevenRewrite.trans (SevenRewrite.refl c) (SevenRewrite.refl c) :
        SevenRewrite W l r c c) = SevenRewrite.refl c :=
    interpret _ _ (.unitLeft (SevenRewrite.refl c))
  cases hBad

end PentagonAdjoinedSixCell

section ActualOriginalP77EightCellLocalCoherence
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

/-- At EVERY genuine P77 terminal raw index, the two explicit
higher histories for the pentagon generator zigzag admit a NEW
eighth-level coherence witness. OLD GK5CG endpoints are retained. -/
def pentagonActualEightCell_zigzagDiamond
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    PentagonAdjoinedSixCell.EightCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonActualSevenRewrite_zigzag f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.sevenZigzagViaAssoc
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)) :=
  PentagonAdjoinedSixCell.eightZigzagCoherence
    (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)

/-- New higher coherence is compatible with every actual original
P77 index, while the existing GK5CG source equality interpreter is
still obstructed. No descent from eighth cells to old strict Eq. -/
theorem pentagonActualEightCell_withOriginalNoGo
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.EightCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonActualSevenRewrite_zigzag f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.sevenZigzagViaAssoc
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨pentagonActualEightCell_zigzagDiamond f g h k A B C D₄ i⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.EightCell
#print axioms PentagonAdjoinedSixCell.eightCell_ofEq
#print axioms PentagonAdjoinedSixCell.sevenZigzagViaAssoc
#print axioms PentagonAdjoinedSixCell.eightZigzagCoherence
#print axioms PentagonAdjoinedSixCell.eightIndependentInterchange
#print axioms PentagonAdjoinedSixCell.sevenZigzag_twoHistories_notStrict
#print axioms PentagonAdjoinedSixCell.eightZigzag_exists_notStrict
#print axioms PentagonAdjoinedSixCell.eightCell_noStrictSevenInterpreter
#print axioms pentagonActualEightCell_zigzagDiamond
#print axioms pentagonActualEightCell_withOriginalNoGo

end ActualOriginalP77EightCellLocalCoherence
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
