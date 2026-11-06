import KUOS.Architecture.QiWuxingGK5CHP77TypedBinaryNormalBracketTreesV4_82

/-!
Qi v4.83 — ACTUAL FOUR-FACTOR TYPED PENTAGON: TWO OBSERVATION ROUTES.
Five genuine bracket-tree Type values for FOUR arbitrary original, typed
subtrees (each may itself be an arbitrarily long finite chain) carry their
actual intermediate Family, partial State, ReassocRoute and Schedule data.
Five primitive associahedral edges agree after flattening the ORIGINAL
ordered source chain, not merely after quotient or length projection.
The three-edge and two-edge routes around the pentagon yield independently
constructed full-domain original PlanObservedEq certificates. Genuine
GK5CG five-cell raw square/loop Type values remain distinct on every edge.
No equality of selected five-cell values, loop triviality, global obstruction
transport, pentagonator, or higher filler is claimed or inserted as an axiom.
Append-only, tighten-only, same-root; strict 空 center; Kuu presentation.
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

section FourFactorPentagon
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

/-- Vertex 0: (((A B) C) D), left-spine actual route word. -/
def pentagonV0 : DirectNormalBracketTree f g h k family₀ s₀ family₄ s₄ :=
  .node (.node (.node A B) C) D₄

/-- Vertex 1: ((A (B C)) D). -/
def pentagonV1 : DirectNormalBracketTree f g h k family₀ s₀ family₄ s₄ :=
  .node (.node A (.node B C)) D₄

/-- Vertex 2: (A ((B C) D)). -/
def pentagonV2 : DirectNormalBracketTree f g h k family₀ s₀ family₄ s₄ :=
  .node A (.node (.node B C) D₄)

/-- Vertex 3: (A (B (C D))), right-spine route word. -/
def pentagonV3 : DirectNormalBracketTree f g h k family₀ s₀ family₄ s₄ :=
  .node A (.node B (.node C D₄))

/-- Vertex 4: ((A B) (C D)), the second pentagon side. -/
def pentagonV4 : DirectNormalBracketTree f g h k family₀ s₀ family₄ s₄ :=
  .node (.node A B) (.node C D₄)

/-- Edge 0→1: original 3-subtree rotation, whiskered by the actual D subtree. -/
theorem pentagonFlatten01 :
    bracketFlatten f g h k (pentagonV0 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV1 f g h k A B C D₄) := by
  change
    directChainAppend f g h k
      (bracketFlatten f g h k (.node (.node A B) C))
      (bracketFlatten f g h k D₄) =
    directChainAppend f g h k
      (bracketFlatten f g h k (.node A (.node B C)))
      (bracketFlatten f g h k D₄)
  exact congrArg
    (fun X => directChainAppend f g h k X (bracketFlatten f g h k D₄))
    (bracketNode_assoc_flatten f g h k A B C)

/-- Edge 1→2: original rotation of A, the actual (B C) subtree, and D. -/
theorem pentagonFlatten12 :
    bracketFlatten f g h k (pentagonV1 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV2 f g h k A B C D₄) := by
  change
    bracketFlatten f g h k (.node (.node A (.node B C)) D₄) =
      bracketFlatten f g h k (.node A (.node (.node B C) D₄))
  exact bracketNode_assoc_flatten f g h k A (.node B C) D₄

/-- Edge 2→3: rotate the last three genuine subtrees, whiskered by A. -/
theorem pentagonFlatten23 :
    bracketFlatten f g h k (pentagonV2 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV3 f g h k A B C D₄) := by
  change
    directChainAppend f g h k
      (bracketFlatten f g h k A)
      (bracketFlatten f g h k (.node (.node B C) D₄)) =
    directChainAppend f g h k
      (bracketFlatten f g h k A)
      (bracketFlatten f g h k (.node B (.node C D₄)))
  exact congrArg
    (fun X => directChainAppend f g h k (bracketFlatten f g h k A) X)
    (bracketNode_assoc_flatten f g h k B C D₄)

/-- Edge 0→4: genuine rotation of (A B), C, and D. -/
theorem pentagonFlatten04 :
    bracketFlatten f g h k (pentagonV0 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV4 f g h k A B C D₄) := by
  change
    bracketFlatten f g h k (.node (.node (.node A B) C) D₄) =
      bracketFlatten f g h k (.node (.node A B) (.node C D₄))
  exact bracketNode_assoc_flatten f g h k (.node A B) C D₄

/-- Edge 4→3: rotate A, B, and the actual (C D) subtree. -/
theorem pentagonFlatten43 :
    bracketFlatten f g h k (pentagonV4 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV3 f g h k A B C D₄) := by
  change
    bracketFlatten f g h k (.node (.node A B) (.node C D₄)) =
      bracketFlatten f g h k (.node A (.node B (.node C D₄)))
  exact bracketNode_assoc_flatten f g h k A B (.node C D₄)

/-- Strict equality of the true ORIGINAL chain along the 3-edge side only. -/
theorem pentagonFlatten_long :
    bracketFlatten f g h k (pentagonV0 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV3 f g h k A B C D₄) :=
  (pentagonFlatten01 f g h k A B C D₄).trans
    ((pentagonFlatten12 f g h k A B C D₄).trans
      (pentagonFlatten23 f g h k A B C D₄))

/-- Strict equality of the true ORIGINAL chain along the 2-edge side only.
This is not strict equality of the resulting FrontNormal route words. -/
theorem pentagonFlatten_short :
    bracketFlatten f g h k (pentagonV0 f g h k A B C D₄) =
      bracketFlatten f g h k (pentagonV3 f g h k A B C D₄) :=
  (pentagonFlatten04 f g h k A B C D₄).trans
    (pentagonFlatten43 f g h k A B C D₄)

/- Each of the FIVE original edge comparisons retains full-domain genuine
source witness pullback. No pentagonator is silently constructed. -/

/-- Genuine original typed pentagon edge 0→1, observational only. -/
theorem pentagonEdge01_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV1 f g h k A B C D₄))) :=
  bracketSameChain_observed f g h k
    (pentagonV0 f g h k A B C D₄)
    (pentagonV1 f g h k A B C D₄)
    (pentagonFlatten01 f g h k A B C D₄)

/-- Genuine original typed pentagon edge 1→2, observational only. -/
theorem pentagonEdge12_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV1 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV2 f g h k A B C D₄))) :=
  bracketSameChain_observed f g h k
    (pentagonV1 f g h k A B C D₄)
    (pentagonV2 f g h k A B C D₄)
    (pentagonFlatten12 f g h k A B C D₄)

/-- Genuine original typed pentagon edge 2→3, observational only. -/
theorem pentagonEdge23_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV2 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) :=
  bracketSameChain_observed f g h k
    (pentagonV2 f g h k A B C D₄)
    (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten23 f g h k A B C D₄)

/-- Genuine original typed pentagon edge 0→4, observational only. -/
theorem pentagonEdge04_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV4 f g h k A B C D₄))) :=
  bracketSameChain_observed f g h k
    (pentagonV0 f g h k A B C D₄)
    (pentagonV4 f g h k A B C D₄)
    (pentagonFlatten04 f g h k A B C D₄)

/-- Genuine original typed pentagon edge 4→3, observational only. -/
theorem pentagonEdge43_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV4 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) :=
  bracketSameChain_observed f g h k
    (pentagonV4 f g h k A B C D₄)
    (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten43 f g h k A B C D₄)

/-- The explicit THREE-EDGE path 0→1→2→3 around the original pentagon. -/
theorem pentagonLong_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV0 f g h k (DirectNormalBracketTree.nil family s) (DirectNormalBracketTree.nil family s) (DirectNormalBracketTree.nil family s) (DirectNormalBracketTree.nil family s))))
      (frontPlan f g h k (bracketEval f g h k
        (pentagonV3 f g h k (DirectNormalBracketTree.nil family s) (DirectNormalBracketTree.nil family s) (DirectNormalBracketTree.nil family s) (DirectNormalBracketTree.nil family s)))) :=
  planObservedEq_trans f g h k
    (pentagonEdge01_observed f g h k A B C D₄)
    (planObservedEq_trans f g h k
      (pentagonEdge12_observed f g h k A B C D₄)
      (pentagonEdge23_observed f g h k A B C D₄))

/-- The independent TWO-EDGE path 0→4→3 around the original pentagon. -/
theorem pentagonShort_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) :=
  planObservedEq_trans f g h k
    (pentagonEdge04_observed f g h k A B C D₄)
    (pentagonEdge43_observed f g h k A B C D₄)

/-- Both independently assembled routes agree at every final original raw
index. We assert the endpoint equality twice as separate proof routes,
NOT the equality of higher Type-valued compositions of five-cells. -/
theorem pentagonTwoPaths_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family₄ s₄)) :
    (((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))).forwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄)))).forwardIndex i) ∧
     ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))).forwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄)))).forwardIndex i)) :=
  ⟨(pentagonLong_observed f g h k A B C D₄).forward i,
    (pentagonShort_observed f g h k A B C D₄).forward i⟩

/-- Independent three- and two-edge proofs of full source raw-index equality. -/
theorem pentagonTwoPaths_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family₀ s₀)) :
    (((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))).backwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄)))).backwardIndex i) ∧
     ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))).backwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄)))).backwardIndex i)) :=
  ⟨(pentagonLong_observed f g h k A B C D₄).backward i,
    (pentagonShort_observed f g h k A B C D₄).backward i⟩

/-- The ACTUAL original source witness pullback matches along both routes;
we never assume witness subsingletonness, invertible coverage, or a filler. -/
theorem pentagonTwoPaths_pullback
    (w : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₄ s₄)) :
    ((fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) w =
      fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) w) ∧
     (fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) w =
      fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) w)) :=
  ⟨(pentagonLong_observed f g h k A B C D₄).pullback w,
    (pentagonShort_observed f g h k A B C D₄).pullback w⟩

/-- Both genuine endpoint plans preserve original P77 Quiver.Path. -/
theorem pentagonEndpoint_path
    (w : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₄ s₄)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) w) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k family₄ s₄) w) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) w) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k family₄ s₄) w) :=
  bracketSameChain_path f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄) w

/-- Both genuine endpoint plans retain original source-certified P77 Hom. -/
theorem pentagonEndpoint_certified
    (w : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₄ s₄)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) w) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₄ s₄) w) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) w) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₄ s₄) w) :=
  bracketSameChain_certified f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄) w

/-- Each endpoint retains ITS OWN original raw comparison under certification.
No inter-side GK5CG Type-valued certificate is identified. -/
theorem pentagonEndpoint_certify_raw
    (w : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₄ s₄)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) w) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) w) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄)))) :=
  bracketSameChain_certify_raw f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄) w

/-- Exact compatibility is controlled by the SHARED original final tree;
no global refinement obstruction invariance or descent is invented. -/
theorem pentagonEndpoint_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k family₄ s₄)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k family₄ s₄)) :=
  bracketSameChain_allCompatible_iff f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄)

/-- Original obstruction at the same final tree controls either endpoint.
This does NOT identify the five edge GK5CG loops or produce a higher filler. -/
theorem pentagonEndpoint_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄))) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k family₄ s₄)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k family₄ s₄)) :=
  bracketSameChain_obstructed_iff f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄)

/- Retain the FIVE truly source-based GK5CG raw-square and loop Type values.
Each edge certificate is a separate actual value. Existence of a higher cell
relating their compositions remains a distinct UNPROVED obstruction problem. -/

/-- Original GK5CG raw square for pentagon edge 0→1. -/
def pentagonEdge01_rawSquare
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawSquare f g h k
    (pentagonV0 f g h k A B C D₄)
    (pentagonV1 f g h k A B C D₄)
    (pentagonFlatten01 f g h k A B C D₄) idx

/-- Original GK5CG potentially nontrivial loop for pentagon edge 0→1. -/
def pentagonEdge01_rawLoop
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawLoop f g h k
    (pentagonV0 f g h k A B C D₄)
    (pentagonV1 f g h k A B C D₄)
    (pentagonFlatten01 f g h k A B C D₄) idx

/-- Original GK5CG raw square for pentagon edge 1→2. -/
def pentagonEdge12_rawSquare
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawSquare f g h k
    (pentagonV1 f g h k A B C D₄)
    (pentagonV2 f g h k A B C D₄)
    (pentagonFlatten12 f g h k A B C D₄) idx

/-- Original GK5CG potentially nontrivial loop for pentagon edge 1→2. -/
def pentagonEdge12_rawLoop
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawLoop f g h k
    (pentagonV1 f g h k A B C D₄)
    (pentagonV2 f g h k A B C D₄)
    (pentagonFlatten12 f g h k A B C D₄) idx

/-- Original GK5CG raw square for pentagon edge 2→3. -/
def pentagonEdge23_rawSquare
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawSquare f g h k
    (pentagonV2 f g h k A B C D₄)
    (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten23 f g h k A B C D₄) idx

/-- Original GK5CG potentially nontrivial loop for pentagon edge 2→3. -/
def pentagonEdge23_rawLoop
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawLoop f g h k
    (pentagonV2 f g h k A B C D₄)
    (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten23 f g h k A B C D₄) idx

/-- Original GK5CG raw square for pentagon edge 0→4. -/
def pentagonEdge04_rawSquare
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawSquare f g h k
    (pentagonV0 f g h k A B C D₄)
    (pentagonV4 f g h k A B C D₄)
    (pentagonFlatten04 f g h k A B C D₄) idx

/-- Original GK5CG potentially nontrivial loop for pentagon edge 0→4. -/
def pentagonEdge04_rawLoop
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawLoop f g h k
    (pentagonV0 f g h k A B C D₄)
    (pentagonV4 f g h k A B C D₄)
    (pentagonFlatten04 f g h k A B C D₄) idx

/-- Original GK5CG raw square for pentagon edge 4→3. -/
def pentagonEdge43_rawSquare
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawSquare f g h k
    (pentagonV4 f g h k A B C D₄)
    (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten43 f g h k A B C D₄) idx

/-- Original GK5CG potentially nontrivial loop for pentagon edge 4→3. -/
def pentagonEdge43_rawLoop
    (idx : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawLoop f g h k
    (pentagonV4 f g h k A B C D₄)
    (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten43 f g h k A B C D₄) idx

/-- Original raw square between the shared endpoints, using the actual
three-edge observation certificate, NOT higher five-cell composition. -/
def pentagonEndpoint_rawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawSquare f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten_long f g h k A B C D₄) i

/-- The original endpoint loop stays a genuine potentially NONTRIVIAL
Type value; a five-cell pentagonator or nullhomotopy is not deduced. -/
def pentagonEndpoint_rawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :=
  bracketSameChain_rawLoop f g h k
    (pentagonV0 f g h k A B C D₄) (pentagonV3 f g h k A B C D₄)
    (pentagonFlatten_short f g h k A B C D₄) i

end FourFactorPentagon

/- Regression: no object inhabitation requirement, all four subtrees may
be the REAL empty tree on an arbitrary genuine partial state. -/
example {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (pentagonV0 f g h k A B C D₄)))
      (frontPlan f g h k (bracketEval f g h k (pentagonV3 f g h k A B C D₄))) :=
  pentagonLong_observed f g h k
    (.nil family s) (.nil family s) (.nil family s) (.nil family s)

#print axioms pentagonV0
#print axioms pentagonV1
#print axioms pentagonV2
#print axioms pentagonV3
#print axioms pentagonV4
#print axioms pentagonFlatten01
#print axioms pentagonFlatten12
#print axioms pentagonFlatten23
#print axioms pentagonFlatten04
#print axioms pentagonFlatten43
#print axioms pentagonFlatten_long
#print axioms pentagonFlatten_short
#print axioms pentagonEdge01_observed
#print axioms pentagonEdge12_observed
#print axioms pentagonEdge23_observed
#print axioms pentagonEdge04_observed
#print axioms pentagonEdge43_observed
#print axioms pentagonLong_observed
#print axioms pentagonShort_observed
#print axioms pentagonTwoPaths_forward
#print axioms pentagonTwoPaths_backward
#print axioms pentagonTwoPaths_pullback
#print axioms pentagonEndpoint_path
#print axioms pentagonEndpoint_certified
#print axioms pentagonEndpoint_certify_raw
#print axioms pentagonEndpoint_allCompatible_iff
#print axioms pentagonEndpoint_obstructed_iff
#print axioms pentagonEdge01_rawSquare
#print axioms pentagonEdge01_rawLoop
#print axioms pentagonEdge12_rawSquare
#print axioms pentagonEdge12_rawLoop
#print axioms pentagonEdge23_rawSquare
#print axioms pentagonEdge23_rawLoop
#print axioms pentagonEdge04_rawSquare
#print axioms pentagonEdge04_rawLoop
#print axioms pentagonEdge43_rawSquare
#print axioms pentagonEdge43_rawLoop
#print axioms pentagonEndpoint_rawSquare
#print axioms pentagonEndpoint_rawLoop

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
