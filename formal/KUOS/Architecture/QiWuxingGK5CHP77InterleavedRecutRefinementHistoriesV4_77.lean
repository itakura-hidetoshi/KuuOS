import KUOS.Architecture.QiWuxingGK5CHP77RefinementPlanObservationV4_77

/-!
Qi v4.77 — ORIGINAL P77 INTERLEAVED RECUT/REFINEMENT HISTORIES.
Finite typed histories retain actual recuts, local steps and intermediate states.
Suffix recursion constructs a separate recut-first form with a transported schedule.
Full-domain index and exact source reconstruction agree by v4.76 naturality.
Both original GK5CG raw five-cell values and their loop are retained separately.
Final-factor obstruction and same-side source certification are preserved.
Append-only same-root; strict 空 center; independent Kuu is a presentation.
Public roots107; protected1558 validation-only Draft/open/unmerged.
Lean v4.30.0-rc2; mathlib5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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


/-- An actual finite interleaving of local execution and reassociation.
All intermediate families, partial states, Step values and recut words remain
in this Type. The normal form does not replace or quotient this original value. -/
inductive InterleavedHistory
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex} :
    (source : Family f g h k u v) → State f g h k source →
    (target : Family f g h k u v) → State f g h k target →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | nil (family : Family f g h k u v) (s : State f g h k family) :
      InterleavedHistory f g h k family s family s
  | step {source target : Family f g h k u v}
      {s m : State f g h k source} {t : State f g h k target}
      (operation : Step f g h k source s m)
      (rest : InterleavedHistory f g h k source m target t) :
      InterleavedHistory f g h k source s target t
  | recut {source middle target : Family f g h k u v}
      (route : ReassocRoute f g h k source middle)
      (s : State f g h k source) {t : State f g h k target}
      (rest : InterleavedHistory f g h k middle
        (reassocStateEquiv f g h k route s) target t) :
      InterleavedHistory f g h k source s target t

/-- Compile the ORIGINAL interleaving at its actual states to the old Plan Type.
In particular each recut keeps its original normalization-generated five-cell. -/
def historyPlan {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (history : InterleavedHistory f g h k source s target t) :
    FivefoldP77RawPatchRefinementPlan f g h k
      (tree f g h k source s) (tree f g h k target t) := by
  induction history with
  | nil family state =>
      exact .presentation (.recut (.refl (tree f g h k family state)))
  | step operation rest ih => exact .trans (stepPlan f g h k operation) ih
  | recut route state rest ih =>
      exact .trans (.presentation (.recut (reassocCutRoute f g h k route state))) ih

/-- Concatenate actual histories at the exact shared family and partial state. -/
def historyAppend {u v : FivefoldPathVertex}
    {source middle : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    (firstHistory : InterleavedHistory f g h k source s middle m) :
    ∀ {target : Family f g h k u v} {t : State f g h k target},
      InterleavedHistory f g h k middle m target t →
        InterleavedHistory f g h k source s target t := by
  induction firstHistory with
  | nil family state =>
      intro target t secondHistory
      exact secondHistory
  | step operation rest ih =>
      intro target t secondHistory
      exact .step operation (ih secondHistory)
  | recut route state rest ih =>
      intro target t secondHistory
      exact .recut route state (ih secondHistory)

/-- Actual concatenation has the full-domain observations of sequential plans.
Its empty-case raw history is handled by the proved original recut unit law. -/
theorem historyPlan_append {u v : FivefoldPathVertex}
    {source middle : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    (firstHistory : InterleavedHistory f g h k source s middle m) :
    ∀ {target : Family f g h k u v} {t : State f g h k target}
      (secondHistory : InterleavedHistory f g h k middle m target t),
      PlanObservedEq f g h k
        (historyPlan f g h k (historyAppend f g h k firstHistory secondHistory))
        (.trans (historyPlan f g h k firstHistory) (historyPlan f g h k secondHistory)) := by
  induction firstHistory with
  | nil family state =>
      intro target t secondHistory
      exact planObservedEq_symm f g h k
        (planObservedEq_left_refl f g h k (historyPlan f g h k secondHistory))
  | step operation rest ih =>
      intro target t secondHistory
      exact planObservedEq_trans f g h k
        (planObservedEq_comp f g h k
          (planObservedEq_refl f g h k (stepPlan f g h k operation))
          (ih secondHistory))
        (planObservedEq_symm f g h k (planObservedEq_assoc f g h k _ _ _))
  | recut route state rest ih =>
      intro target t secondHistory
      exact planObservedEq_trans f g h k
        (planObservedEq_comp f g h k
          (planObservedEq_refl f g h k
            (.presentation (.recut (reassocCutRoute f g h k route state))))
          (ih secondHistory))
        (planObservedEq_symm f g h k (planObservedEq_assoc f g h k _ _ _))

/-- Every old finite schedule is an actual history without interposed recuts. -/
def historyOfSchedule {u v : FivefoldPathVertex}
    {family : Family f g h k u v} {s t : State f g h k family}
    (schedule : Schedule f g h k family s t) :
    InterleavedHistory f g h k family s family t := by
  induction schedule with
  | nil state => exact .nil family state
  | cons operation rest ih => exact .step operation ih

/-- Embedding an old schedule retains its exact original Plan value. -/
theorem historyPlan_ofSchedule {u v : FivefoldPathVertex}
    {family : Family f g h k u v} {s t : State f g h k family}
    (schedule : Schedule f g h k family s t) :
    historyPlan f g h k (historyOfSchedule f g h k schedule) =
      schedulePlan f g h k schedule := by
  induction schedule with
  | nil state => rfl
  | cons operation rest ih =>
      exact congrArg
        (fun plan => FivefoldP77RawPatchRefinementPlan.trans (stepPlan f g h k operation) plan)
        ih

/-- A separate recut-first normal form: the cumulative actual recut word,
followed by the transported finite schedule in the final family.
No reconstruction of the original interleaving positions is asserted. -/
structure FrontNormal {u v : FivefoldPathVertex}
    (source : Family f g h k u v) (s : State f g h k source)
    (target : Family f g h k u v) (t : State f g h k target) where
  route : ReassocRoute f g h k source target
  schedule : Schedule f g h k target (reassocStateEquiv f g h k route s) t

/-- Normalize from the suffix. Steps cross the accumulated recut using their
actual transported positions. Recut composition needs no inverse-state cast. -/
def normalizeFront {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (history : InterleavedHistory f g h k source s target t) :
    FrontNormal f g h k source s target t := by
  induction history with
  | nil family state => exact ⟨.refl family, .nil family state⟩
  | step operation rest ih =>
      exact ⟨ih.route, .cons (reassocStep f g h k ih.route operation) ih.schedule⟩
  | recut route state rest ih => exact ⟨.trans route ih.route, ih.schedule⟩

/-- Interpret the separate normal form using the original recut and schedule. -/
def frontPlan {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (normal : FrontNormal f g h k source s target t) :
    FivefoldP77RawPatchRefinementPlan f g h k
      (tree f g h k source s) (tree f g h k target t) :=
  .trans (.presentation (.recut (reassocCutRoute f g h k normal.route s)))
    (schedulePlan f g h k normal.schedule)

/-- Every arbitrary finite interleaving agrees with its recut-first form on
ALL raw indices and actual source witnesses. This uses compositional
observations and v4.76 naturality, never source-witness subsingletonness. -/
theorem normalizeFront_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (history : InterleavedHistory f g h k source s target t) :
    PlanObservedEq f g h k (historyPlan f g h k history)
      (frontPlan f g h k (normalizeFront f g h k history)) := by
  induction history with
  | nil family state =>
      exact planObservedEq_symm f g h k
        (planObservedEq_left_refl f g h k
          (.presentation (.recut (.refl (tree f g h k family state)))))
  | step operation rest ih =>
      exact planObservedEq_trans f g h k
        (planObservedEq_comp f g h k
          (planObservedEq_refl f g h k (stepPlan f g h k operation)) ih)
        (planObservedEq_trans f g h k
          (planObservedEq_symm f g h k (planObservedEq_assoc f g h k _ _ _))
          (planObservedEq_trans f g h k
            (planObservedEq_comp f g h k
              (planObservedEq_reassocStep f g h k
                (normalizeFront f g h k rest).route operation)
              (planObservedEq_refl f g h k
                (schedulePlan f g h k (normalizeFront f g h k rest).schedule)))
            (planObservedEq_assoc f g h k _ _ _)))
  | recut route state rest ih =>
      exact planObservedEq_trans f g h k
        (planObservedEq_comp f g h k
          (planObservedEq_refl f g h k
            (.presentation (.recut (reassocCutRoute f g h k route state)))) ih)
        (planObservedEq_trans f g h k
          (planObservedEq_symm f g h k (planObservedEq_assoc f g h k _ _ _))
          (planObservedEq_comp f g h k
            (planObservedEq_recut_trans f g h k
              (reassocCutRoute f g h k route state)
              (reassocCutRoute f g h k (normalizeFront f g h k rest).route
                (reassocStateEquiv f g h k route state)))
            (planObservedEq_refl f g h k
              (schedulePlan f g h k (normalizeFront f g h k rest).schedule))))

section HistoryConsequences
variable {u v : FivefoldPathVertex} {source target : Family f g h k u v}
variable {s : State f g h k source} {t : State f g h k target}
variable (history : InterleavedHistory f g h k source s target t)

/-- Full target-index coverage agreement, with no completeness assumption. -/
theorem normalizeFront_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (historyPlan f g h k history)).forwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (normalizeFront f g h k history))).forwardIndex i :=
  (normalizeFront_observed f g h k history).forward i

/-- Full source-index coverage agreement. No inverse law for general
refinement coverage is assumed. -/
theorem normalizeFront_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (historyPlan f g h k history)).backwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (normalizeFront f g h k history))).backwardIndex i :=
  (normalizeFront_observed f g h k history).backward i

/-- Both histories reconstruct the same EXACT original source Type value. -/
theorem normalizeFront_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (historyPlan f g h k history) witness =
      fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (normalizeFront f g h k history)) witness :=
  (normalizeFront_observed f g h k history).pullback witness

/-- The ORIGINAL interleaved five-cell and the normal-form five-cell are both
retained, with endpoints aligned by the proved full-domain forward equality. -/
def historyRawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawSquare f g h k (historyPlan f g h k history)
    (frontPlan f g h k (normalizeFront f g h k history))
    (normalizeFront_forward f g h k history) i

/-- Their actual GK5CG five-cell loop, with no triviality or higher equality. -/
def historyRawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawLoop f g h k (historyPlan f g h k history)
    (frontPlan f g h k (normalizeFront f g h k history))
    (normalizeFront_forward f g h k history) i

/-- Both actual plans preserve the original source path. -/
theorem history_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (historyPlan f g h k history) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (normalizeFront f g h k history)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k
      (historyPlan f g h k history) witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k
      (frontPlan f g h k (normalizeFront f g h k history)) witness⟩

/-- Both plans preserve the original source-certified P77 partial Hom. -/
theorem history_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (historyPlan f g h k history) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (normalizeFront f g h k history)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k
      (historyPlan f g h k history) witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k
      (frontPlan f g h k (normalizeFront f g h k history)) witness⟩

/-- Real final factor evidence certifies both sides, preserving each SAME
side's raw comparison and five-cell values rather than equating the sides. -/
theorem history_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (historyPlan f g h k history) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (historyPlan f g h k history)) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (normalizeFront f g h k history)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (normalizeFront f g h k history))) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k
      (historyPlan f g h k history) witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k
      (frontPlan f g h k (normalizeFront f g h k history)) witness⟩

/-- All designated hierarchy levels, endpoints and fixed contexts of each
plan are compatible exactly when the SAME final factor tree is compatible.
The final state t may be partial, not the family's terminal state. -/
theorem history_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (historyPlan f g h k history) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (normalizeFront f g h k history)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k
      (historyPlan f g h k history),
    fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k
      (frontPlan f g h k (normalizeFront f g h k history))⟩

/-- Missing final factor evidence obstructs both entire plans in exactly the
same sense. No obstruction invariance across arbitrary refinement steps is
asserted, and no missing fine factor evidence is manufactured. -/
theorem history_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (historyPlan f g h k history) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (normalizeFront f g h k history)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k
      (historyPlan f g h k history),
    fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k
      (frontPlan f g h k (normalizeFront f g h k history))⟩

end HistoryConsequences

#print axioms InterleavedHistory
#print axioms historyPlan
#print axioms historyAppend
#print axioms historyPlan_append
#print axioms historyOfSchedule
#print axioms historyPlan_ofSchedule
#print axioms FrontNormal
#print axioms normalizeFront
#print axioms frontPlan
#print axioms normalizeFront_observed
#print axioms normalizeFront_forward
#print axioms normalizeFront_backward
#print axioms normalizeFront_pullback
#print axioms historyRawSquare
#print axioms historyRawLoop
#print axioms history_path
#print axioms history_certified
#print axioms history_certify_raw
#print axioms history_allCompatible_iff
#print axioms history_obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
