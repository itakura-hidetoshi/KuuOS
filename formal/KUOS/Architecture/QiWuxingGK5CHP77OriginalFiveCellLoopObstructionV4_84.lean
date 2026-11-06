import KUOS.Architecture.QiWuxingGK5CHP77ActualTypedPentagonObservationV4_83

/-!
Qi v4.84 — GENUINE GK5CG CONSERVATIVE FIVE-CELL LOOP COMPOSITION
AND THE EXACT STRICT-WORD COHERENCE / OBSTRUCTION BOUNDARY.

The actual v4.83 five pentagon edges already retain the ORIGINAL
NativeGK5CGConservativeFiveCell Type values. Their raw loops all share
the SAME actual P77 target raw four-proof, so the existing native
GK5CG .trans/.symm constructors compose them without casts or
subsingleton assumptions. The three-edge and two-edge raw-loop words
and their signed difference are distinct, original Type-valued values.

Strict equality of those selected 5-cell words is introduced only as
an EXPLICIT proposition (not as an axiom or theorem), with its precise
counterexample/existence obstruction. No higher 6-cell, five-cell word
equality, loop triviality, new pentagonator, or source reconstruction
is asserted.

Separately, the independent F112 GK5CG genuine ORIGINAL F55/P77
3-versus-2 FOUR-PROOF charge defect remains +1, so its upper/lower
four proofs admit NO conservative original five-cell. The new
self-loops are NOT identified with those upper/lower four-proof terms:
their existence is compatible with the authoritative no-go.

Append-only, tighten-only, same-root, strict 空 center, Kuu presentation.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Public roots107; validation-only PR #1558 remains Draft/open/unmerged.
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

section ActualConservativePentagon
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

/-- The ORIGINAL GK5CG Type of conservative self-five-cells on the
ACTUAL terminal P77 raw four-proof. No new raw presentation is added. -/
abbrev pentagonFinalConservativeLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  NativeGK5CGConservativeFiveCell first last
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i)
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i)

/-- The actual THREE-edge native conservative GK5CG composite.
Each component is the genuine v4.83 edge loop; intermediate raw
four-proof endpoints are literally the common target value. -/
def pentagonLongConservativeFiveCell
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonFinalConservativeLoop f g h k i :=
  .trans
    (pentagonEdge01_rawLoop f g h k A B C D₄ i)
    (.trans (pentagonEdge12_rawLoop f g h k A B C D₄ i)
      (pentagonEdge23_rawLoop f g h k A B C D₄ i))

/-- The separate genuine TWO-edge native conservative GK5CG composite.
We do NOT assert that it equals the three-edge constructor word. -/
def pentagonShortConservativeFiveCell
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonFinalConservativeLoop f g h k i :=
  .trans
    (pentagonEdge04_rawLoop f g h k A B C D₄ i)
    (pentagonEdge43_rawLoop f g h k A B C D₄ i)

/-- Difference of the ACTUAL two conservative five-cell loop words,
still a fifth-dimensional endomorphism of the terminal raw four-proof.
This IS NOT a sixth-dimensional filler or a claim of nullhomotopy. -/
def pentagonDifferenceConservativeFiveCell
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonFinalConservativeLoop f g h k i :=
  .trans (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (.symm (pentagonShortConservativeFiveCell f g h k A B C D₄ i))

/-- The reverse difference is a separately retained native Type value. -/
def pentagonReverseDifferenceConservativeFiveCell
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    pentagonFinalConservativeLoop f g h k i :=
  .trans (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (.symm (pentagonLongConservativeFiveCell f g h k A B C D₄ i))

/-- An actual original fifth-dimensional certificate can be constructed
along the upper three edges without adding any new higher generator. -/
theorem pentagonLongConservativeFiveCell_nonempty
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (pentagonFinalConservativeLoop f g h k i) :=
  ⟨pentagonLongConservativeFiveCell f g h k A B C D₄ i⟩

/-- Same existence for the independent lower two-edge loop word. -/
theorem pentagonShortConservativeFiveCell_nonempty
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (pentagonFinalConservativeLoop f g h k i) :=
  ⟨pentagonShortConservativeFiveCell f g h k A B C D₄ i⟩

/-- Original 4-associator charge is preserved by the actual upper 5-cell,
by the authoritative inductive GK5CG conservation theorem. -/
theorem pentagonLongConservativeFiveCell_charge_sound
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i).gk5cgAssocCharge =
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i).gk5cgAssocCharge :=
  (pentagonLongConservativeFiveCell f g h k A B C D₄ i).assocCharge_sound

/-- Original 4-associator charge conservation along the lower 5-cell. -/
theorem pentagonShortConservativeFiveCell_charge_sound
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i).gk5cgAssocCharge =
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i).gk5cgAssocCharge :=
  (pentagonShortConservativeFiveCell f g h k A B C D₄ i).assocCharge_sound

/-- The native signed difference is also charge-preserving at its exact
four-cell endpoints, but such preservation does not imply it is refl. -/
theorem pentagonDifferenceConservativeFiveCell_charge_sound
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i).gk5cgAssocCharge =
    (fivefoldP77RawPatchTreeRaw f g h k
      (tree f g h k family₄ s₄) i).gk5cgAssocCharge :=
  (pentagonDifferenceConservativeFiveCell f g h k A B C D₄ i).assocCharge_sound

/-- Strict equality of the TWO SELECTED original five-cell grammar words
is a separate, intentionally UNSOLVED claim. It is NOT implied by
the verified v4.83 PlanObservedEq, which only observes raw indices/witnesses. -/
def PentagonStrictFiveCellCoherence : Prop :=
  ∀ i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄),
    pentagonLongConservativeFiveCell f g h k A B C D₄ i =
      pentagonShortConservativeFiveCell f g h k A B C D₄ i

/-- The exact local obstruction to the above strong *syntax-word equality*.
It is NOT by itself a theorem that a higher six-cell filler fails to exist. -/
def PentagonStrictFiveCellObstruction : Prop :=
  ∃ i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄),
    pentagonLongConservativeFiveCell f g h k A B C D₄ i ≠
      pentagonShortConservativeFiveCell f g h k A B C D₄ i

/-- Necessary-and-sufficient logical gate for strict selected five-cell
equality; no choice of true/false side is asserted without evidence. -/
theorem pentagonStrictFiveCellObstruction_iff :
    PentagonStrictFiveCellObstruction f g h k A B C D₄ ↔
      ¬ PentagonStrictFiveCellCoherence f g h k A B C D₄ := by
  constructor
  · rintro ⟨i, hDiff⟩ hAll
    exact hDiff (hAll i)
  · intro hNot
    classical
    by_contra hNoWitness
    apply hNot
    intro i
    by_contra hDiff
    exact hNoWitness ⟨i, hDiff⟩

/-- The new typed original five-cell compositions coexist with the
independent F112 REAL original P77 four-proof charge gap. The loops
above are NOT a conservative cell between those distinct four-proofs. -/
theorem pentagonSourceChargeGap_exact :
    (nativeGK5CFP77UpperPath f g h k).gk5cgAssocCharge -
      (nativeGK5CFP77LowerPath f g h k).gk5cgAssocCharge = 1 :=
  nativeGK5CGOriginalPentagon_charge_defect_one f g h k

/-- The already proved genuine original P77 conservative no-go
remains valid: a +1 four-proof charge mismatch forbids any old-language
GK5CG cell joining the ORIGINAL upper/lower P77 proof histories. -/
theorem pentagonOriginalSource_noConservativePentagonator :
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) :=
  nativeGK5CGOriginalPentagon_noConservativeFiveCell f g h k

/-- FULL boundary in one typed statement. Genuine conservative
ENDOMORPHISM five-cell words exist along both observed Qi pentagon
routes; nevertheless no conservative five-cell joins the DIFFERENT
original P77 four-proof upper/lower paths with their charge gap.
We do not identify those distinct source and target four-proofs. -/
theorem pentagonLoopComposition_withSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (pentagonFinalConservativeLoop f g h k i) ∧
    ((nativeGK5CFP77UpperPath f g h k).gk5cgAssocCharge -
      (nativeGK5CFP77LowerPath f g h k).gk5cgAssocCharge = 1) ∧
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) :=
  ⟨pentagonLongConservativeFiveCell_nonempty f g h k A B C D₄ i,
    pentagonSourceChargeGap_exact f g h k,
    pentagonOriginalSource_noConservativePentagonator f g h k⟩

/-- The v4.83 full-domain observations also remain separately proven
along BOTH genuine pentagon paths. Their evidence is not a five-cell
syntax-word equality nor a sixth-dimensional filler. -/
theorem pentagonObservedTwoRoutes_retained :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV3 f g h k A B C D₄))) ∧
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV3 f g h k A B C D₄))) :=
  ⟨pentagonLong_observed f g h k A B C D₄,
    pentagonShort_observed f g h k A B C D₄⟩

end ActualConservativePentagon

/- Regression on the TRUE empty partial state: both original conservative
five-cell compositions remain genuinely typed without requiring
a completed refinement or fabricated original source witness. -/
example {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family)
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family s)) :
    Nonempty (pentagonFinalConservativeLoop f g h k i) :=
  pentagonShortConservativeFiveCell_nonempty f g h k
    (.nil family s) (.nil family s) (.nil family s) (.nil family s) i

#print axioms pentagonFinalConservativeLoop
#print axioms pentagonLongConservativeFiveCell
#print axioms pentagonShortConservativeFiveCell
#print axioms pentagonDifferenceConservativeFiveCell
#print axioms pentagonReverseDifferenceConservativeFiveCell
#print axioms pentagonLongConservativeFiveCell_nonempty
#print axioms pentagonShortConservativeFiveCell_nonempty
#print axioms pentagonLongConservativeFiveCell_charge_sound
#print axioms pentagonShortConservativeFiveCell_charge_sound
#print axioms pentagonDifferenceConservativeFiveCell_charge_sound
#print axioms PentagonStrictFiveCellCoherence
#print axioms PentagonStrictFiveCellObstruction
#print axioms pentagonStrictFiveCellObstruction_iff
#print axioms pentagonSourceChargeGap_exact
#print axioms pentagonOriginalSource_noConservativePentagonator
#print axioms pentagonLoopComposition_withSourceObstruction
#print axioms pentagonObservedTwoRoutes_retained

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
