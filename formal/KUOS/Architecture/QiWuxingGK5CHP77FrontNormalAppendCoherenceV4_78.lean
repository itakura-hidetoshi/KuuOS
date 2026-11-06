import KUOS.Architecture.QiWuxingGK5CHP77InterleavedRecutRefinementHistoriesV4_77

/-!
Qi v4.78 — ORIGINAL INTERLEAVED HISTORY APPEND / FRONT-NORMAL COMPOSITION.
Two independently typed front normals compose through their actual
reassociation and transported-step histories. The original values stay
distinct, while all forward/backward raw indices and exact source pullbacks
are equal after normalization, on their FULL domains.
No equality of five-cell Type values, raw loops, history constructors or
higher coherence cells is inferred from PlanObservedEq.
Append-only, same-root, strict 空 center, independent Kuu = presentation.
Pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Public roots 107; validation-only PR #1558 stays Draft/open/unmerged.
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

/-- Embed a separately retained front normal in an ACTUAL Type-valued history:
its original recut followed by each of its transported, typed local steps.
No quotienting or erasure of either presentation takes place. -/
def frontNormalHistory {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (normal : FrontNormal f g h k source s target t) :
    InterleavedHistory f g h k source s target t :=
  .recut normal.route s (historyOfSchedule f g h k normal.schedule)

/-- The embedded original history compiles to exactly the front-normal plan;
this is a plan-value equality, NOT a five-cell equality across histories. -/
theorem frontNormalHistory_plan {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (normal : FrontNormal f g h k source s target t) :
    historyPlan f g h k (frontNormalHistory f g h k normal) =
      frontPlan f g h k normal := by
  change
    FivefoldP77RawPatchRefinementPlan.trans
      (.presentation (.recut (reassocCutRoute f g h k normal.route s)))
      (historyPlan f g h k (historyOfSchedule f g h k normal.schedule)) =
    FivefoldP77RawPatchRefinementPlan.trans
      (.presentation (.recut (reassocCutRoute f g h k normal.route s)))
      (schedulePlan f g h k normal.schedule)
  rw [historyPlan_ofSchedule]

/-- Composition of two actual front normals: concatenate their original,
typed recut-then-step histories, then apply the v4.77 suffix normalizer.
The normalizer recursively composes the cumulative ReassocRoute and transports
the first schedule's Step values across all subsequent recuts; it deliberately
does NOT assert equality with a chosen simplified route word. -/
def composeFrontNormal {u v : FivefoldPathVertex}
    {source middle target : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    {t : State f g h k target}
    (firstNormal : FrontNormal f g h k source s middle m)
    (secondNormal : FrontNormal f g h k middle m target t) :
    FrontNormal f g h k source s target t :=
  normalizeFront f g h k
    (historyAppend f g h k (frontNormalHistory f g h k firstNormal)
      (frontNormalHistory f g h k secondNormal))

/-- The composed front normal realizes sequential normal plans up to ALL three
original observations. The proof transports no extra assumptions or axioms. -/
theorem composeFrontNormal_observed {u v : FivefoldPathVertex}
    {source middle target : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    {t : State f g h k target}
    (firstNormal : FrontNormal f g h k source s middle m)
    (secondNormal : FrontNormal f g h k middle m target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (composeFrontNormal f g h k firstNormal secondNormal))
      (.trans (frontPlan f g h k firstNormal) (frontPlan f g h k secondNormal)) := by
  have hNormal := normalizeFront_observed f g h k
    (historyAppend f g h k
      (frontNormalHistory f g h k firstNormal)
      (frontNormalHistory f g h k secondNormal))
  have hAppend := historyPlan_append f g h k
    (frontNormalHistory f g h k firstNormal)
    (frontNormalHistory f g h k secondNormal)
  have hBoth := planObservedEq_trans f g h k
    (planObservedEq_symm f g h k hNormal) hAppend
  simpa only [composeFrontNormal, frontNormalHistory_plan] using hBoth

section AppendCoherence
variable {u v : FivefoldPathVertex}
variable {source middle target : Family f g h k u v}
variable {s : State f g h k source}
variable {m : State f g h k middle}
variable {t : State f g h k target}
variable (H₁ : InterleavedHistory f g h k source s middle m)
variable (H₂ : InterleavedHistory f g h k middle m target t)

/-- MAIN v4.78: normalize the actual concatenation, or normalize both
original histories first and compose their front normals. These TWO distinct
normal-form Type values have equal full-domain Plan observations only. -/
theorem normalizeAppend_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) := by
  have hWhole := normalizeFront_observed f g h k
    (historyAppend f g h k H₁ H₂)
  have hAppend := historyPlan_append f g h k H₁ H₂
  have hParts := planObservedEq_comp f g h k
    (normalizeFront_observed f g h k H₁)
    (normalizeFront_observed f g h k H₂)
  have hCompose := composeFrontNormal_observed f g h k
    (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)
  exact planObservedEq_trans f g h k
    (planObservedEq_trans f g h k
      (planObservedEq_symm f g h k hWhole) hAppend)
    (planObservedEq_trans f g h k hParts
      (planObservedEq_symm f g h k hCompose))

/-- The original unnormalized concatenation also agrees with the composite
of the independently normalized plans, not merely with the first normal. -/
theorem originalAppend_composite_observed :
    PlanObservedEq f g h k
      (historyPlan f g h k (historyAppend f g h k H₁ H₂))
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) := by
  exact planObservedEq_trans f g h k
    (historyPlan_append f g h k H₁ H₂)
    (planObservedEq_trans f g h k
      (planObservedEq_comp f g h k
        (normalizeFront_observed f g h k H₁)
        (normalizeFront_observed f g h k H₂))
      (planObservedEq_symm f g h k
        (composeFrontNormal_observed f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))))

/-- Forward raw-index equality on EVERY index of the actual target tree. -/
theorem normalizeAppend_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))).forwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))).forwardIndex i :=
  (normalizeAppend_observed f g h k H₁ H₂).forward i

/-- Independent backward raw-index equality on EVERY original source index. -/
theorem normalizeAppend_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))).backwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))).backwardIndex i :=
  (normalizeAppend_observed f g h k H₁ H₂).backward i

/-- BOTH constructions recover the same actual source Type-valued witness. -/
theorem normalizeAppend_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂))) witness =
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) witness :=
  (normalizeAppend_observed f g h k H₁ H₂).pullback witness

/-- Keep the two ORIGINAL GK5CG raw five-cell constructions in a typed square.
Only their forward endpoints are aligned by the proved observation theorem. -/
def normalizeAppend_rawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawSquare f g h k
    (frontPlan f g h k (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))
    (frontPlan f g h k
      (composeFrontNormal f g h k
        (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))
    (normalizeAppend_forward f g h k H₁ H₂) i

/-- The distinct five-cell histories form an original loop; no loop
triviality or new higher cell is asserted. -/
def normalizeAppend_rawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawLoop f g h k
    (frontPlan f g h k (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))
    (frontPlan f g h k
      (composeFrontNormal f g h k
        (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))
    (normalizeAppend_forward f g h k H₁ H₂) i

/-- Both candidate plans certify the ORIGINAL source path at every target witness. -/
theorem normalizeAppend_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k
          (normalizeFront f g h k (historyAppend f g h k H₁ H₂))) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k
          (composeFrontNormal f g h k
            (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness⟩

/-- Genuine source-certified P77 partial Homs remain the same across both
normalizations; no reconstruction of the interleaving positions is needed. -/
theorem normalizeAppend_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k
          (normalizeFront f g h k (historyAppend f g h k H₁ H₂))) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k
          (composeFrontNormal f g h k
            (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness⟩

/-- Each original plan certifies its OWN raw comparison without equating
its chosen five-cell history to the other side's history. -/
theorem normalizeAppend_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k
          (normalizeFront f g h k (historyAppend f g h k H₁ H₂))) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k
          (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k
          (composeFrontNormal f g h k
            (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k
          (composeFrontNormal f g h k
            (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness⟩

/-- Both plans are compatible iff the SAME original final factor family is.
No claim of obstruction invariance through arbitrary intermediate refinements. -/
theorem normalizeAppend_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂))) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _⟩

/-- The common FINAL factor obstruction equivalently obstructs either full
plan. Source obstruction is not invented, ignored or globally erased. -/
theorem normalizeAppend_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂))) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k
        (composeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _⟩

end AppendCoherence

#print axioms frontNormalHistory
#print axioms frontNormalHistory_plan
#print axioms composeFrontNormal
#print axioms composeFrontNormal_observed
#print axioms normalizeAppend_observed
#print axioms originalAppend_composite_observed
#print axioms normalizeAppend_forward
#print axioms normalizeAppend_backward
#print axioms normalizeAppend_pullback
#print axioms normalizeAppend_rawSquare
#print axioms normalizeAppend_rawLoop
#print axioms normalizeAppend_path
#print axioms normalizeAppend_certified
#print axioms normalizeAppend_certify_raw
#print axioms normalizeAppend_allCompatible_iff
#print axioms normalizeAppend_obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
