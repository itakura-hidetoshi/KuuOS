import KUOS.Architecture.QiWuxingGK5CHP77FrontNormalAppendCoherenceV4_78

/-!
Qi v4.79 — DIRECT ORIGINAL FRONT-NORMAL COMPOSITION.
Compose the actual ReassocRoute words directly and append the first actual
Schedule, transported by the second route, to the second actual Schedule.
No embedding into histories or rerun of normalization defines this operation.
Its original Plan has the full-domain observations of sequential plans,
the v4.78 history-defined composite, and normalized original history append.
Both original GK5CG five-cell values, source witnesses and final obstruction
remain explicit. Observation equality is not equality of five-cell histories.
Append-only, same-root, strict 空 center; independent Kuu is a presentation.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Public roots107; protected1558 stays validation-only Draft/open/unmerged.
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

/-- Actual schedule concatenation compiles to sequential plans on all three
observation domains. The empty schedule retains the old recut-refl value. -/
theorem schedulePlan_append_observed {u v : FivefoldPathVertex}
    {family : Family f g h k u v} {s m t : State f g h k family}
    (firstSchedule : Schedule f g h k family s m)
    (secondSchedule : Schedule f g h k family m t) :
    PlanObservedEq f g h k
      (schedulePlan f g h k (append f g h k firstSchedule secondSchedule))
      (.trans (schedulePlan f g h k firstSchedule)
        (schedulePlan f g h k secondSchedule)) := by
  induction firstSchedule with
  | nil state =>
      exact planObservedEq_symm f g h k
        (planObservedEq_left_refl f g h k (schedulePlan f g h k secondSchedule))
  | cons operation rest ih =>
      have hStep := planObservedEq_comp f g h k
        (planObservedEq_refl f g h k (stepPlan f g h k operation))
        (ih secondSchedule)
      have hAssoc := planObservedEq_assoc f g h k
        (stepPlan f g h k operation) (schedulePlan f g h k rest)
        (schedulePlan f g h k secondSchedule)
      exact planObservedEq_trans f g h k hStep
        (planObservedEq_symm f g h k hAssoc)

/-- Package the original v4.76 recut/schedule square as full observations.
No equality of its two actual raw five-cell histories is introduced. -/
theorem planObservedEq_reassocSchedule {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s t : State f g h k source} (schedule : Schedule f g h k source s t) :
    PlanObservedEq f g h k (scheduleThenRecut f g h k route schedule)
      (recutThenSchedule f g h k route schedule) :=
  ⟨reassocSquare_forward f g h k route schedule,
    reassocSquare_backward f g h k route schedule,
    reassocSquare_pullback f g h k route schedule⟩

/-- Put an observational square inside actual prefix/suffix plans. This is
only an observation law, not a higher-cell coherence or syntax equality. -/
theorem planObservedEq_whiskerSquare {u v : FivefoldPathVertex}
    {source squareSource firstMiddle secondMiddle squareTarget target :
      FivefoldP77RawPatchCutTree f g h k u v}
    (prefix : FivefoldP77RawPatchRefinementPlan f g h k source squareSource)
    (firstLeft : FivefoldP77RawPatchRefinementPlan f g h k squareSource firstMiddle)
    (firstRight : FivefoldP77RawPatchRefinementPlan f g h k firstMiddle squareTarget)
    (secondLeft : FivefoldP77RawPatchRefinementPlan f g h k squareSource secondMiddle)
    (secondRight : FivefoldP77RawPatchRefinementPlan f g h k secondMiddle squareTarget)
    (suffix : FivefoldP77RawPatchRefinementPlan f g h k squareTarget target)
    (square : PlanObservedEq f g h k (.trans firstLeft firstRight)
      (.trans secondLeft secondRight)) :
    PlanObservedEq f g h k
      (.trans (.trans prefix firstLeft) (.trans firstRight suffix))
      (.trans (.trans prefix secondLeft) (.trans secondRight suffix)) := by
  have h₁ := planObservedEq_assoc f g h k prefix firstLeft (.trans firstRight suffix)
  have h₂ := planObservedEq_comp f g h k
    (planObservedEq_refl f g h k prefix)
    (planObservedEq_symm f g h k (planObservedEq_assoc f g h k firstLeft firstRight suffix))
  have h₃ := planObservedEq_comp f g h k
    (planObservedEq_refl f g h k prefix)
    (planObservedEq_comp f g h k square (planObservedEq_refl f g h k suffix))
  have h₄ := planObservedEq_comp f g h k
    (planObservedEq_refl f g h k prefix)
    (planObservedEq_assoc f g h k secondLeft secondRight suffix)
  have h₅ := planObservedEq_symm f g h k
    (planObservedEq_assoc f g h k prefix secondLeft (.trans secondRight suffix))
  exact planObservedEq_trans f g h k h₁
    (planObservedEq_trans f g h k h₂
      (planObservedEq_trans f g h k h₃ (planObservedEq_trans f g h k h₄ h₅)))

section DirectComposition
variable {u v : FivefoldPathVertex}
variable {source middle target : Family f g h k u v}
variable {s : State f g h k source} {m : State f g h k middle}
variable {t : State f g h k target}
variable (N₁ : FrontNormal f g h k source s middle m)
variable (N₂ : FrontNormal f g h k middle m target t)

/-- DIRECT composition: retain the two actual route words under trans;
transport every first-schedule Step by the second route, then append the
second schedule. Dependent endpoints match by the original trans computation.
No normalizer, history embedding, inverse-state cast or extra hypothesis. -/
def directComposeFrontNormal : FrontNormal f g h k source s target t where
  route := .trans N₁.route N₂.route
  schedule := append f g h k
    (reassocSchedule f g h k N₂.route N₁.schedule) N₂.schedule

/-- The selected cumulative route is exactly the original trans constructor. -/
theorem directComposeFrontNormal_route :
    (directComposeFrontNormal f g h k N₁ N₂).route =
      ReassocRoute.trans N₁.route N₂.route := rfl

/-- The selected actual schedule is exactly transport followed by append.
This limited projection equality does not identify the old normal-form word. -/
theorem directComposeFrontNormal_schedule :
    (directComposeFrontNormal f g h k N₁ N₂).schedule =
      append f g h k (reassocSchedule f g h k N₂.route N₁.schedule) N₂.schedule := rfl

/-- The direct construction realizes the two sequential original front plans
on ALL raw indices and genuine source witnesses, including partial endpoints. -/
theorem directComposeFrontNormal_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))
      (.trans (frontPlan f g h k N₁) (frontPlan f g h k N₂)) := by
  have hSquare := planObservedEq_reassocSchedule f g h k N₂.route N₁.schedule
  have hSplice := planObservedEq_whiskerSquare f g h k
    (.presentation (.recut (reassocCutRoute f g h k N₁.route s)))
    (schedulePlan f g h k N₁.schedule)
    (.presentation (.recut (reassocCutRoute f g h k N₂.route m)))
    (.presentation (.recut (reassocCutRoute f g h k N₂.route
      (reassocStateEquiv f g h k N₁.route s))))
    (schedulePlan f g h k (reassocSchedule f g h k N₂.route N₁.schedule))
    (schedulePlan f g h k N₂.schedule) hSquare
  have hRoutes := planObservedEq_recut_trans f g h k
    (reassocCutRoute f g h k N₁.route s)
    (reassocCutRoute f g h k N₂.route (reassocStateEquiv f g h k N₁.route s))
  have hSchedules := schedulePlan_append_observed f g h k
    (reassocSchedule f g h k N₂.route N₁.schedule) N₂.schedule
  have hCollapse := planObservedEq_comp f g h k hRoutes
    (planObservedEq_symm f g h k hSchedules)
  exact planObservedEq_symm f g h k
    (planObservedEq_trans f g h k hSplice hCollapse)

/-- MAIN comparison: directly chosen route/schedule data and the v4.78
history-defined composite agree observationally, without equating their words. -/
theorem directComposeFrontNormal_historyObserved :
    PlanObservedEq f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))
      (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) :=
  planObservedEq_trans f g h k (directComposeFrontNormal_observed f g h k N₁ N₂)
    (planObservedEq_symm f g h k (composeFrontNormal_observed f g h k N₁ N₂))

/-- Every target raw index agrees between the direct and history constructions. -/
theorem directComposeFrontNormal_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))).forwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂))).forwardIndex i :=
  (directComposeFrontNormal_historyObserved f g h k N₁ N₂).forward i

/-- Every source raw index agrees, without asserting that coverage is invertible. -/
theorem directComposeFrontNormal_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))).backwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂))).backwardIndex i :=
  (directComposeFrontNormal_historyObserved f g h k N₁ N₂).backward i

/-- Both constructions recover the SAME original source Type-valued witness. -/
theorem directComposeFrontNormal_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂)) witness =
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) witness :=
  (directComposeFrontNormal_historyObserved f g h k N₁ N₂).pullback witness

/-- Keep both original GK5CG five-cell values at aligned actual raw endpoints. -/
def directComposeFrontNormal_rawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawSquare f g h k
    (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))
    (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂))
    (directComposeFrontNormal_forward f g h k N₁ N₂) i

/-- Their original five-cell loop, with no triviality or higher-cell assertion. -/
def directComposeFrontNormal_rawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawLoop f g h k
    (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))
    (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂))
    (directComposeFrontNormal_forward f g h k N₁ N₂) i

/-- Both original plans preserve the genuine source path. -/
theorem directComposeFrontNormal_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness⟩

/-- Both original plans preserve the source-certified P77 partial Hom. -/
theorem directComposeFrontNormal_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness⟩

/-- Certification retains each SAME side's chosen raw comparison and five-cells. -/
theorem directComposeFrontNormal_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂))) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness⟩

/-- Both full plans are compatible exactly when the SAME final factor tree is.
The common final state need not be the family's fully completed state. -/
theorem directComposeFrontNormal_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _⟩

/-- The common final-factor obstruction obstructs either full plan. This does
not claim obstruction invariance across arbitrary intervening refinements. -/
theorem directComposeFrontNormal_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (composeFrontNormal f g h k N₁ N₂)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _⟩

end DirectComposition

section DirectAppend
variable {u v : FivefoldPathVertex}
variable {source middle target : Family f g h k u v}
variable {s : State f g h k source} {m : State f g h k middle}
variable {t : State f g h k target}
variable (H₁ : InterleavedHistory f g h k source s middle m)
variable (H₂ : InterleavedHistory f g h k middle m target t)

/-- Normalize the actual appended history, or DIRECTLY compose the two
separate normal forms: all three full-domain observations agree. -/
theorem normalizeAppend_direct_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (normalizeFront f g h k (historyAppend f g h k H₁ H₂)))
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) :=
  planObservedEq_trans f g h k (normalizeAppend_observed f g h k H₁ H₂)
    (planObservedEq_symm f g h k
      (directComposeFrontNormal_historyObserved f g h k
        (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))

/-- The unnormalized ORIGINAL appended Plan is retained and has these same
observations; no original history reconstruction from a normal is assumed. -/
theorem originalAppend_direct_observed :
    PlanObservedEq f g h k
      (historyPlan f g h k (historyAppend f g h k H₁ H₂))
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (normalizeFront f g h k H₁) (normalizeFront f g h k H₂))) :=
  planObservedEq_trans f g h k (originalAppend_composite_observed f g h k H₁ H₂)
    (planObservedEq_symm f g h k
      (directComposeFrontNormal_historyObserved f g h k
        (normalizeFront f g h k H₁) (normalizeFront f g h k H₂)))

end DirectAppend

/-- Regression at arbitrary, possibly partial states: two empty histories
require no completeness or nonemptiness of the actual source witness type. -/
example {u v : FivefoldPathVertex} (family : Family f g h k u v)
    (s : State f g h k family) :
    PlanObservedEq f g h k
      (frontPlan f g h k (normalizeFront f g h k (.nil family s)))
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (normalizeFront f g h k (.nil family s))
          (normalizeFront f g h k (.nil family s)))) :=
  normalizeAppend_direct_observed f g h k (.nil family s) (.nil family s)

#print axioms schedulePlan_append_observed
#print axioms planObservedEq_reassocSchedule
#print axioms planObservedEq_whiskerSquare
#print axioms directComposeFrontNormal
#print axioms directComposeFrontNormal_route
#print axioms directComposeFrontNormal_schedule
#print axioms directComposeFrontNormal_observed
#print axioms directComposeFrontNormal_historyObserved
#print axioms directComposeFrontNormal_forward
#print axioms directComposeFrontNormal_backward
#print axioms directComposeFrontNormal_pullback
#print axioms directComposeFrontNormal_rawSquare
#print axioms directComposeFrontNormal_rawLoop
#print axioms directComposeFrontNormal_path
#print axioms directComposeFrontNormal_certified
#print axioms directComposeFrontNormal_certify_raw
#print axioms directComposeFrontNormal_allCompatible_iff
#print axioms directComposeFrontNormal_obstructed_iff
#print axioms normalizeAppend_direct_observed
#print axioms originalAppend_direct_observed

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
