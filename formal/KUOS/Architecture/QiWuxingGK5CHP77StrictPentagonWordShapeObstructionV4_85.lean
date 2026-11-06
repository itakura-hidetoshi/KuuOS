import KUOS.Architecture.QiWuxingGK5CHP77OriginalFiveCellLoopObstructionV4_84

/-!
Qi v4.85 — GENUINE ORIGINAL GK5CG FIVE-CELL WORD SHAPE OBSTRUCTION.

The original NativeGK5CGConservativeFiveCell is a freely presented
INDUCTIVE TYPE with distinct trans/symm/refl constructors. The v4.84
three-edge and two-edge pentagon composites live at the SAME genuine
final P77 raw four-cell and can be probed without any invented quotient.

A finite BOOLEAN constructor-shape observation distinguishes their
actual Type-valued five-cell constructor words at EVERY target index.
The existing real raw-tree index is inhabited even at partial states,
so v4.84's strict selected-word coherence is constructively false.
The difference loop is also not literally the refl constructor.

This is ONLY a theorem about exact ORIGINAL free 5-cell syntax.
NO nonexistence of a higher 6-cell filler, quotient pentagonator,
homotopy, or observational descent is inferred. Independent F112/GK5CG
source four-proof charge +1 no-go remains separately authoritative.
No weakening of existing theorems, new axiom, sorry, or root change.
Append-only/tighten-only/same-root; strict 空 center; independent Kuu
is presentation. Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6;
root 107, protected validation-only #1558 Draft/open/unmerged.
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

universe uD vD uE vE
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

/-- Probe only whether the root of a GENUINE original conservative
five-cell free constructor word is trans. Do not quotient its witnesses. -/
def originalConservativeFiveCell_rootTrans
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {a b : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {w z : NativeF55RawVerticalFourCell first last a b}
    (cell : NativeGK5CGConservativeFiveCell first last w z) : Bool :=
  match cell with
  | .trans _ _ => true
  | _ => false

/-- A structural probe on the exact constructor word: if its top-level
right child is trans, test the root constructor of that child's LEFT
subword. The charge and all source/target Type values are preserved. -/
def originalConservativeFiveCell_rightLeftTrans
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {a b : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {w z : NativeF55RawVerticalFourCell first last a b}
    (cell : NativeGK5CGConservativeFiveCell first last w z) : Bool :=
  match cell with
  | .trans _ (.trans left _) =>
      originalConservativeFiveCell_rootTrans left
  | _ => false

section ActualPentagonWordShape
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

/-- The THREE-edge genuinely selected original five-cell word has
a trans at the root of its top-right-left subterm:
  trans edge01 (trans (trans (symm u12) v12) edge23).
Proof depends ONLY on original constructors, not on raw source
witness extensionality, a normalization quotient, or a higher filler. -/
theorem pentagonLongFiveCell_wordShape_true
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    originalConservativeFiveCell_rightLeftTrans
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i) = true :=
  rfl

/-- The TWO-edge actual original five-cell word has a symm at the
corresponding top-right-left position:
  trans edge04 (trans (symm u43) v43).
The two original proof words therefore have DISTINCT constructor shape. -/
theorem pentagonShortFiveCell_wordShape_false
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    originalConservativeFiveCell_rightLeftTrans
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i) = false :=
  rfl

/-- Main v4.85 theorem: native original GK5CG five-cell constructor
words selected along the two genuine pentagon routes are NEVER STRICTLY
EQUAL at any final raw index. This does NOT exclude a 6-cell between them. -/
theorem pentagonOriginalFiveCell_words_ne
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonLongConservativeFiveCell f g h k A B C D₄ i ≠
      pentagonShortConservativeFiveCell f g h k A B C D₄ i := by
  intro hEq
  have hProbe := congrArg
    (fun cell => originalConservativeFiveCell_rightLeftTrans cell) hEq
  change originalConservativeFiveCell_rightLeftTrans
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i) =
    originalConservativeFiveCell_rightLeftTrans
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i) at hProbe
  rw [pentagonLongFiveCell_wordShape_true f g h k A B C D₄ i,
      pentagonShortFiveCell_wordShape_false f g h k A B C D₄ i] at hProbe
  cases hProbe

/-- Every ACTUAL final raw P77 cut tree has a real raw index even when
the intermediate refinement states are not all terminal. -/
theorem pentagonFinalRawIndex_nonempty :
    Nonempty (FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  fivefoldP77RawPatchTreeIndex_nonempty f g h k
    (tree f g h k family₄ s₄)

/-- Constructive witness to the v4.84 strict SELECTED-WORD obstruction.
We do not replace the original source/target four-cell evidence by Prop. -/
theorem pentagonStrictFiveCellObstruction_exists :
    PentagonStrictFiveCellObstruction f g h k A B C D₄ := by
  obtain ⟨i⟩ := pentagonFinalRawIndex_nonempty f g h k
  exact ⟨i, pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i⟩

/-- Therefore the v4.84 strict original free-word equality proposition
is false, without using a blanket claim that higher coherence fails. -/
theorem pentagonStrictFiveCellCoherence_false :
    ¬ PentagonStrictFiveCellCoherence f g h k A B C D₄ :=
  (pentagonStrictFiveCellObstruction_iff f g h k A B C D₄).mp
    (pentagonStrictFiveCellObstruction_exists f g h k A B C D₄)

/-- The actual delta loop is a trans-constructor word. -/
theorem pentagonDifferenceFiveCell_rootTrans
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    originalConservativeFiveCell_rootTrans
      (pentagonDifferenceConservativeFiveCell f g h k A B C D₄ i) = true :=
  rfl

/-- The actual original identity five-cell uses the distinct refl
constructor; even this is NOT a six-dimensional nullhomotopy decision. -/
theorem pentagonReflexiveFiveCell_rootTrans
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    originalConservativeFiveCell_rootTrans
      (NativeGK5CGConservativeFiveCell.refl
        (fivefoldP77RawPatchTreeRaw f g h k
          (tree f g h k family₄ s₄) i)) = false :=
  rfl

/-- Exact, original free constructor syntax difference from literal refl.
The delta remains a possibly higher-nullhomotopic Type value. -/
theorem pentagonDifferenceFiveCell_not_refl
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonDifferenceConservativeFiveCell f g h k A B C D₄ i ≠
      NativeGK5CGConservativeFiveCell.refl
        (fivefoldP77RawPatchTreeRaw f g h k
          (tree f g h k family₄ s₄) i) := by
  intro hEq
  have hProbe := congrArg
    (fun cell => originalConservativeFiveCell_rootTrans cell) hEq
  change originalConservativeFiveCell_rootTrans
      (pentagonDifferenceConservativeFiveCell f g h k A B C D₄ i) =
    originalConservativeFiveCell_rootTrans
      (NativeGK5CGConservativeFiveCell.refl
        (fivefoldP77RawPatchTreeRaw f g h k
          (tree f g h k family₄ s₄) i)) at hProbe
  rw [pentagonDifferenceFiveCell_rootTrans f g h k A B C D₄ i,
      pentagonReflexiveFiveCell_rootTrans f g h k i] at hProbe
  cases hProbe

/-- The original source AUTHORITATIVE charge obstruction remains
independent of this new strictly syntactic five-cell distinction. -/
theorem pentagonSyntaxObstruction_and_originalSourceNoGo :
    PentagonStrictFiveCellObstruction f g h k A B C D₄ ∧
    (nativeGK5CFP77UpperPath f g h k).gk5cgAssocCharge -
      (nativeGK5CFP77LowerPath f g h k).gk5cgAssocCharge = 1 ∧
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) :=
  ⟨pentagonStrictFiveCellObstruction_exists f g h k A B C D₄,
    pentagonSourceChargeGap_exact f g h k,
    pentagonOriginalSource_noConservativePentagonator f g h k⟩

/-- Full-domain v4.83 observations still agree, while the TWO actual
selected original GK5CG Type-valued words are not strictly equal.
This is the precise boundary; it says NOTHING about higher fillers. -/
theorem pentagonObservationsAgree_butFiveCellWordsDiffer :
    (PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV3 f g h k A B C D₄)))) ∧
    ¬ PentagonStrictFiveCellCoherence f g h k A B C D₄ :=
  ⟨pentagonLong_observed f g h k A B C D₄,
    pentagonStrictFiveCellCoherence_false f g h k A B C D₄⟩

end ActualPentagonWordShape

/-- Regression at an arbitrary genuine PARTIAL source state.
The v4.84 long/short five-cell words are non-identical even when
all four original typed subtrees are actual empty histories. -/
example {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family)
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family s)) :
    pentagonLongConservativeFiveCell f g h k
      (.nil family s) (.nil family s) (.nil family s) (.nil family s) i ≠
    pentagonShortConservativeFiveCell f g h k
      (.nil family s) (.nil family s) (.nil family s) (.nil family s) i :=
  pentagonOriginalFiveCell_words_ne f g h k
    (.nil family s) (.nil family s) (.nil family s) (.nil family s) i

#print axioms originalConservativeFiveCell_rootTrans
#print axioms originalConservativeFiveCell_rightLeftTrans
#print axioms pentagonLongFiveCell_wordShape_true
#print axioms pentagonShortFiveCell_wordShape_false
#print axioms pentagonOriginalFiveCell_words_ne
#print axioms pentagonFinalRawIndex_nonempty
#print axioms pentagonStrictFiveCellObstruction_exists
#print axioms pentagonStrictFiveCellCoherence_false
#print axioms pentagonDifferenceFiveCell_rootTrans
#print axioms pentagonReflexiveFiveCell_rootTrans
#print axioms pentagonDifferenceFiveCell_not_refl
#print axioms pentagonSyntaxObstruction_and_originalSourceNoGo
#print axioms pentagonObservationsAgree_butFiveCellWordsDiffer

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
