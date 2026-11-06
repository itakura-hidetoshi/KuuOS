import KUOS.Architecture.QiWuxingGK5CHP77FiniteDirectNormalChainsV4_81

/-!
Qi v4.82 — ACTUAL TYPED BINARY BRACKET TREES FOR FINITE FRONT-NORMAL CHAINS.
Every leaf retains an original FrontNormal, every internal node retains the
actual intermediate Family and partial State in dependent Type indices.
Flattening keeps the ordered original finite chain; evaluation retains the
chosen, potentially non-definitional, original reassociation route/schedules.
Any two finite bracket trees whose flattenings are the SAME original chain
have identical full-domain raw-index and genuine source-witness observations.
Neither FrontNormal words, GK5CG five-cell Type values, nor their loops are
identified. No higher pentagon filler or strict associativity is postulated.
Append-only, tighten-only, same-root; strict 空 center; Kuu is presentation.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Public roots107; protected validation-only PR #1558 stays Draft/open/unmerged.
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

/-- A genuine typed binary tree of original direct normals, NOT a tree of
quotient morphisms. Each node has its actual shared partial Family and State.
The nil constructor records an empty chain at any original partial state. -/
inductive DirectNormalBracketTree
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex} :
    (source : Family f g h k u v) → State f g h k source →
    (target : Family f g h k u v) → State f g h k target →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | nil (family : Family f g h k u v) (s : State f g h k family) :
      DirectNormalBracketTree f g h k family s family s
  | atom {source target : Family f g h k u v}
      {s : State f g h k source} {t : State f g h k target}
      (normal : FrontNormal f g h k source s target t) :
      DirectNormalBracketTree f g h k source s target t
  | node {source middle target : Family f g h k u v}
      {s : State f g h k source} {m : State f g h k middle}
      {t : State f g h k target}
      (left : DirectNormalBracketTree f g h k source s middle m)
      (right : DirectNormalBracketTree f g h k middle m target t) :
      DirectNormalBracketTree f g h k source s target t

/-- Forget ONLY the binary brackets, retaining every genuine ordered
FrontNormal leaf and all dependent intermediate partial source data. -/
def bracketFlatten {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (T : DirectNormalBracketTree f g h k source s target t) :
    DirectNormalChain f g h k source s target t := by
  induction T with
  | nil family state =>
      exact .nil family state
  | atom normal =>
      exact directChainSingleton f g h k normal
  | node left right ihLeft ihRight =>
      exact directChainAppend f g h k ihLeft ihRight

/-- Evaluate the REAL typed binary tree by direct normal composition.
Unlike flattening, the bracket structure remains in the chosen route word
and in the source Schedule, and is NOT asserted to be unique. -/
def bracketEval {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (T : DirectNormalBracketTree f g h k source s target t) :
    FrontNormal f g h k source s target t := by
  induction T with
  | nil family state =>
      exact directNormalUnit f g h k family state
  | atom normal =>
      exact normal
  | node left right ihLeft ihRight =>
      exact directComposeFrontNormal f g h k ihLeft ihRight

/-- Node evaluation explicitly retains the non-strict original route
constructor rather than treating parenthesized routes as equal. -/
theorem bracketEval_node_route {u v : FivefoldPathVertex}
    {source middle target : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    {t : State f g h k target}
    (L : DirectNormalBracketTree f g h k source s middle m)
    (R : DirectNormalBracketTree f g h k middle m target t) :
    (bracketEval f g h k (.node L R)).route =
      .trans (bracketEval f g h k L).route
        (bracketEval f g h k R).route := rfl

/-- THE MAIN INDUCTION: evaluation of ANY finite typed bracketing agrees
observationally with the v4.81 right fold of its ordered original chain.
The atom case uses the genuine right-unit observation, and the node case
uses actual direct composition and finite-chain append observations. -/
theorem bracketEval_fold_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (T : DirectNormalBracketTree f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k T))
      (frontPlan f g h k
        (directChainFold f g h k (bracketFlatten f g h k T))) := by
  induction T with
  | nil family state =>
      exact planObservedEq_refl f g h k _
  | atom normal =>
      exact planObservedEq_symm f g h k
        (directChainSingleton_observed f g h k normal)
  | node left right ihLeft ihRight =>
      exact planObservedEq_trans f g h k
        (directComposeFrontNormal_observed f g h k
          (bracketEval f g h k left) (bracketEval f g h k right))
        (planObservedEq_trans f g h k
          (planObservedEq_comp f g h k ihLeft ihRight)
          (planObservedEq_symm f g h k
            (directChainFold_append_observed f g h k
              (bracketFlatten f g h k left)
              (bracketFlatten f g h k right))))

/-- Every actual finite chain admits a canonical right-spine bracketing.
No existence assumptions on the intermediate partial states are introduced. -/
def bracketRight {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (C : DirectNormalChain f g h k source s target t) :
    DirectNormalBracketTree f g h k source s target t := by
  induction C with
  | nil family state =>
      exact .nil family state
  | cons normal rest ih =>
      exact .node (.atom normal) ih

/-- Right-spine embedding loses no original normal leaf or its dependent
source/target indices: flattening is strictly equal as a CHAIN value. -/
theorem bracketRight_flatten {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (C : DirectNormalChain f g h k source s target t) :
    bracketFlatten f g h k (bracketRight f g h k C) = C := by
  induction C with
  | nil family state => rfl
  | cons normal rest ih =>
      change DirectNormalChain.cons normal
        (bracketFlatten f g h k (bracketRight f g h k rest)) =
        DirectNormalChain.cons normal rest
      exact congrArg (fun tail => DirectNormalChain.cons normal tail) ih

/-- The canonical right-spine evaluates to the original v4.81 fold on the
FULL observation domains, without claiming equality of normal Type values. -/
theorem bracketRight_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (C : DirectNormalChain f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (bracketRight f g h k C)))
      (frontPlan f g h k (directChainFold f g h k C)) := by
  simpa only [bracketRight_flatten] using
    (bracketEval_fold_observed f g h k (bracketRight f g h k C))

/-- MAIN v4.82 BRACKETING INDEPENDENCE: equality of the actual ordered
source chain, not just equality of lengths or of quotient classes, suffices
for agreement of every genuine raw index and Type-valued witness pullback. -/
theorem bracketSameChain_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (L R : DirectNormalBracketTree f g h k source s target t)
    (hFlat : bracketFlatten f g h k L = bracketFlatten f g h k R) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k L))
      (frontPlan f g h k (bracketEval f g h k R)) := by
  have hL := bracketEval_fold_observed f g h k L
  have hR := bracketEval_fold_observed f g h k R
  rw [hFlat] at hL
  exact planObservedEq_trans f g h k hL
    (planObservedEq_symm f g h k hR)

/-- A fixed ACTUAL finite chain may be given any two distinct genuine
binary tree presentations: both have identical complete observations. -/
theorem bracketOverChain_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (C : DirectNormalChain f g h k source s target t)
    (L R : DirectNormalBracketTree f g h k source s target t)
    (hL : bracketFlatten f g h k L = C)
    (hR : bracketFlatten f g h k R = C) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k L))
      (frontPlan f g h k (bracketEval f g h k R)) :=
  bracketSameChain_observed f g h k L R (hL.trans hR.symm)

/-- For THREE arbitrary typed subtrees, the two parenthesizations flatten
to exactly the SAME original chain, using the strict append law only in the
syntax of CHAIN values, not in their normal-form evaluations. -/
theorem bracketNode_assoc_flatten {u v : FivefoldPathVertex}
    {family₀ family₁ family₂ family₃ : Family f g h k u v}
    {s₀ : State f g h k family₀} {s₁ : State f g h k family₁}
    {s₂ : State f g h k family₂} {s₃ : State f g h k family₃}
    (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
    (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
    (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃) :
    bracketFlatten f g h k (.node (.node A B) C) =
      bracketFlatten f g h k (.node A (.node B C)) :=
  directChainAppend_assoc f g h k
    (bracketFlatten f g h k A) (bracketFlatten f g h k B)
    (bracketFlatten f g h k C)

/-- The associator law holds for arbitrary finite SUBTREES, not only the
three single-link normals treated in v4.80. Its claim is observational. -/
theorem bracketNode_assoc_observed {u v : FivefoldPathVertex}
    {family₀ family₁ family₂ family₃ : Family f g h k u v}
    {s₀ : State f g h k family₀} {s₁ : State f g h k family₁}
    {s₂ : State f g h k family₂} {s₃ : State f g h k family₃}
    (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
    (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
    (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (.node (.node A B) C)))
      (frontPlan f g h k (bracketEval f g h k (.node A (.node B C)))) :=
  bracketSameChain_observed f g h k _ _
    (bracketNode_assoc_flatten f g h k A B C)

section BracketingConsequences
variable {u v : FivefoldPathVertex}
variable {source target : Family f g h k u v}
variable {s : State f g h k source} {t : State f g h k target}
variable (L R : DirectNormalBracketTree f g h k source s target t)
variable (hFlat : bracketFlatten f g h k L = bracketFlatten f g h k R)

/-- Original forward raw maps agree at EVERY target index. -/
theorem bracketSameChain_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (bracketEval f g h k L))).forwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (bracketEval f g h k R))).forwardIndex i :=
  (bracketSameChain_observed f g h k L R hFlat).forward i

/-- Original backward raw maps agree at EVERY source index. -/
theorem bracketSameChain_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (bracketEval f g h k L))).backwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (bracketEval f g h k R))).backwardIndex i :=
  (bracketSameChain_observed f g h k L R hFlat).backward i

/-- The genuine ORIGINAL P77 source-witness Type value is recovered equally. -/
theorem bracketSameChain_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (bracketEval f g h k L)) witness =
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (bracketEval f g h k R)) witness :=
  (bracketSameChain_observed f g h k L R hFlat).pullback witness

/-- Both ORIGINAL five-cell Type values coexist in an endpoint-aligned
raw square; the equality above is ONLY of raw indices, not of five-cells. -/
def bracketSameChain_rawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawSquare f g h k
    (frontPlan f g h k (bracketEval f g h k L))
    (frontPlan f g h k (bracketEval f g h k R))
    (bracketSameChain_forward f g h k L R hFlat) i

/-- The possibly NONTRIVIAL original GK5CG five-cell loop is retained.
This is not an assertion of a higher coherence filler or a nullhomotopy. -/
def bracketSameChain_rawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawLoop f g h k
    (frontPlan f g h k (bracketEval f g h k L))
    (frontPlan f g h k (bracketEval f g h k R))
    (bracketSameChain_forward f g h k L R hFlat) i

/-- Both actual bracket plans preserve the SAME ORIGINAL source path. -/
theorem bracketSameChain_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (bracketEval f g h k L)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (bracketEval f g h k R)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness⟩

/-- Both real source-certified partial Hom values are preserved. -/
theorem bracketSameChain_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (bracketEval f g h k L)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (bracketEval f g h k R)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness⟩

/-- Certification keeps each ORIGINAL side's own raw comparison and actual
five-cell history; no two chosen Type-valued certificates are equated. -/
theorem bracketSameChain_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (bracketEval f g h k L)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k L))) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (bracketEval f g h k R)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (bracketEval f g h k R))) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness⟩

/-- Full-plan compatibility depends on the COMMON final original factor
tree, not on choosing a bracket structure or assuming complete states. -/
theorem bracketSameChain_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (bracketEval f g h k L)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (bracketEval f g h k R)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _⟩

/-- Exact final-factor obstruction is shared by both plans; no global
obstruction invariance through arbitrary refinements is claimed. -/
theorem bracketSameChain_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (bracketEval f g h k L)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (bracketEval f g h k R)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _⟩

end BracketingConsequences

/- Regression: actual empty, arbitrary partially typed state, not a phantom
inhabited witness or an additional quotient constructor. -/
example {u v : FivefoldPathVertex} (family : Family f g h k u v)
    (s : State f g h k family) :
    bracketFlatten f g h k (DirectNormalBracketTree.nil family s) =
      DirectNormalChain.nil family s := rfl

/- Regression: both sides of one binary rebracketing may have genuine
different route syntax; the proof only uses the exact original flattening. -/
example {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (C : DirectNormalChain f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (bracketEval f g h k (bracketRight f g h k C)))
      (frontPlan f g h k (directChainFold f g h k C)) :=
  bracketRight_observed f g h k C

#print axioms DirectNormalBracketTree
#print axioms bracketFlatten
#print axioms bracketEval
#print axioms bracketEval_node_route
#print axioms bracketEval_fold_observed
#print axioms bracketRight
#print axioms bracketRight_flatten
#print axioms bracketRight_observed
#print axioms bracketSameChain_observed
#print axioms bracketOverChain_observed
#print axioms bracketNode_assoc_flatten
#print axioms bracketNode_assoc_observed
#print axioms bracketSameChain_forward
#print axioms bracketSameChain_backward
#print axioms bracketSameChain_pullback
#print axioms bracketSameChain_rawSquare
#print axioms bracketSameChain_rawLoop
#print axioms bracketSameChain_path
#print axioms bracketSameChain_certified
#print axioms bracketSameChain_certify_raw
#print axioms bracketSameChain_allCompatible_iff
#print axioms bracketSameChain_obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
