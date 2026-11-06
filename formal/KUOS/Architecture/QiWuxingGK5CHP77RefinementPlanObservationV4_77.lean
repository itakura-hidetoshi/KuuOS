import KUOS.Architecture.QiWuxingGK5CHP77ReassociatedRefinementSchedulesV4_76

/-!
Qi v4.77 — full-domain observations of original refinement plans.
Composition laws preserve actual five-cell histories as separate Type values.
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

/-- Three full-domain observations of ORIGINAL plans with the same endpoints.
No equality of their raw five-cell values or their history constructors is included. -/
structure PlanObservedEq {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (firstPlan secondPlan : FivefoldP77RawPatchRefinementPlan f g h k source target) : Prop where
  forward : ∀ i : FivefoldP77RawPatchTreeIndex f g h k target,
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).forwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan).forwardIndex i
  backward : ∀ i : FivefoldP77RawPatchTreeIndex f g h k source,
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).backwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan).backwardIndex i
  pullback : ∀ witness : FivefoldP77RawPatchTreeWitness f g h k target,
    fivefoldP77RawPatchRefinementPlanPullback f g h k firstPlan witness =
      fivefoldP77RawPatchRefinementPlanPullback f g h k secondPlan witness

/-- Reflexivity of the three observations. -/
theorem planObservedEq_refl {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    PlanObservedEq f g h k plan plan :=
  ⟨fun _ => rfl, fun _ => rfl, fun _ => rfl⟩

/-- Symmetry of observations does not invert a directed refinement plan. -/
theorem planObservedEq_symm {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    {firstPlan secondPlan : FivefoldP77RawPatchRefinementPlan f g h k source target}
    (same : PlanObservedEq f g h k firstPlan secondPlan) :
    PlanObservedEq f g h k secondPlan firstPlan :=
  ⟨fun i => (same.forward i).symm, fun i => (same.backward i).symm,
    fun witness => (same.pullback witness).symm⟩

/-- Transitivity retains full domains in all three observations. -/
theorem planObservedEq_trans {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    {firstPlan middlePlan lastPlan : FivefoldP77RawPatchRefinementPlan f g h k source target}
    (sameFirst : PlanObservedEq f g h k firstPlan middlePlan)
    (sameSecond : PlanObservedEq f g h k middlePlan lastPlan) :
    PlanObservedEq f g h k firstPlan lastPlan :=
  ⟨fun i => (sameFirst.forward i).trans (sameSecond.forward i),
    fun i => (sameFirst.backward i).trans (sameSecond.backward i),
    fun witness => (sameFirst.pullback witness).trans (sameSecond.pullback witness)⟩

/-- Sequential composition respects observations. Forward and pullback compose
contravariantly; the independently retained backward maps compose covariantly. -/
theorem planObservedEq_comp {u v : FivefoldPathVertex}
    {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
    {firstPlan firstPlan' : FivefoldP77RawPatchRefinementPlan f g h k source middle}
    {secondPlan secondPlan' : FivefoldP77RawPatchRefinementPlan f g h k middle target}
    (sameFirst : PlanObservedEq f g h k firstPlan firstPlan')
    (sameSecond : PlanObservedEq f g h k secondPlan secondPlan') :
    PlanObservedEq f g h k (.trans firstPlan secondPlan) (.trans firstPlan' secondPlan') := by
  constructor
  · intro i
    exact (sameFirst.forward
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan).forwardIndex i)).trans
      (congrArg
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan').forwardIndex
        (sameSecond.forward i))
  · intro i
    exact (sameSecond.backward
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).backwardIndex i)).trans
      (congrArg
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan').backwardIndex
        (sameFirst.backward i))
  · intro witness
    exact (sameFirst.pullback
      (fivefoldP77RawPatchRefinementPlanPullback f g h k secondPlan witness)).trans
      (congrArg (fivefoldP77RawPatchRefinementPlanPullback f g h k firstPlan')
        (sameSecond.pullback witness))

/-- Associativity at the level of observations, without equating plan syntax
or the two parenthesized raw five-cell composites. -/
theorem planObservedEq_assoc {u v : FivefoldPathVertex}
    {source middle₁ middle₂ target : FivefoldP77RawPatchCutTree f g h k u v}
    (firstPlan : FivefoldP77RawPatchRefinementPlan f g h k source middle₁)
    (secondPlan : FivefoldP77RawPatchRefinementPlan f g h k middle₁ middle₂)
    (thirdPlan : FivefoldP77RawPatchRefinementPlan f g h k middle₂ target) :
    PlanObservedEq f g h k (.trans (.trans firstPlan secondPlan) thirdPlan)
      (.trans firstPlan (.trans secondPlan thirdPlan)) :=
  ⟨fun _ => rfl, fun _ => rfl, fun _ => rfl⟩

/-- The original normalization-based reflexive recut is a left unit on
observations. Its chosen raw five-cell value is not replaced by reflexivity. -/
theorem planObservedEq_left_refl {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    PlanObservedEq f g h k (.trans (.presentation (.recut (.refl source))) plan) plan := by
  constructor
  · intro i
    exact recutRefl_forward f g h k source
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan).forwardIndex i)
  · intro i
    exact congrArg
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan).backwardIndex
      (recutRefl_backward f g h k source i)
  · intro witness
    rfl

/-- The same original reflexive recut is also a right unit on observations. -/
theorem planObservedEq_right_refl {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    PlanObservedEq f g h k (.trans plan (.presentation (.recut (.refl target)))) plan := by
  constructor
  · intro i
    exact congrArg
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan).forwardIndex
      (recutRefl_forward f g h k target i)
  · intro i
    exact recutRefl_backward f g h k target
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan).backwardIndex i)
  · intro witness
    rfl

/-- Two original recut plans have the observations of the composed CutRoute.
The normalization-generated five-cell histories remain distinct actual values. -/
theorem planObservedEq_recut_trans {u v : FivefoldPathVertex}
    {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
    (firstRoute : FivefoldP77RawPatchCutRoute f g h k source middle)
    (secondRoute : FivefoldP77RawPatchCutRoute f g h k middle target) :
    PlanObservedEq f g h k
      (.trans (.presentation (.recut firstRoute)) (.presentation (.recut secondRoute)))
      (.presentation (.recut (.trans firstRoute secondRoute))) := by
  constructor
  · intro i
    change (fivefoldP77RawPatchCutRouteRawComparison f g h k firstRoute).forwardIndex
      ((fivefoldP77RawPatchCutRouteRawComparison f g h k secondRoute).forwardIndex i) =
      (fivefoldP77RawPatchCutRouteRawComparison f g h k
        (.trans firstRoute secondRoute)).forwardIndex i
    simp only [fivefoldP77RawPatchCutRouteRawComparison_forwardIndex] <;> rfl
  · intro i
    change (fivefoldP77RawPatchCutRouteRawComparison f g h k secondRoute).backwardIndex
      ((fivefoldP77RawPatchCutRouteRawComparison f g h k firstRoute).backwardIndex i) =
      (fivefoldP77RawPatchCutRouteRawComparison f g h k
        (.trans firstRoute secondRoute)).backwardIndex i
    simp only [fivefoldP77RawPatchCutRouteRawComparison_backwardIndex] <;> rfl
  · intro witness
    rfl

/-- Move one actual Step past its ending-state recut, retaining exactly that
Step at the reassociated position. All three observations have full domains. -/
theorem planObservedEq_reassocStep {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s m : State f g h k source} (step : Step f g h k source s m) :
    PlanObservedEq f g h k
      (.trans (stepPlan f g h k step)
        (.presentation (.recut (reassocCutRoute f g h k route m))))
      (.trans (.presentation (.recut (reassocCutRoute f g h k route s)))
        (stepPlan f g h k (reassocStep f g h k route step))) := by
  constructor
  · intro i
    change (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (stepPlan f g h k step)).forwardIndex
        ((fivefoldP77RawPatchCutRouteRawComparison f g h k
          (reassocCutRoute f g h k route m)).forwardIndex i) =
      (fivefoldP77RawPatchCutRouteRawComparison f g h k
        (reassocCutRoute f g h k route s)).forwardIndex
          ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
            (stepPlan f g h k (reassocStep f g h k route step))).forwardIndex i)
    simp only [fivefoldP77RawPatchCutRouteRawComparison_forwardIndex]
    change (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (stepPlan f g h k step)).forwardIndex
        ((reassocIndexEquiv f g h k route m).symm i) =
      (reassocIndexEquiv f g h k route s).symm
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (stepPlan f g h k (reassocStep f g h k route step))).forwardIndex i)
    apply (reassocIndexEquiv f g h k route s).injective
    rw [Equiv.apply_symm_apply]
    simpa only [Equiv.apply_symm_apply] using
      reassocStep_forward f g h k route step ((reassocIndexEquiv f g h k route m).symm i)
  · intro i
    change (fivefoldP77RawPatchCutRouteRawComparison f g h k
      (reassocCutRoute f g h k route m)).backwardIndex
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (stepPlan f g h k step)).backwardIndex i) =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k (reassocStep f g h k route step))).backwardIndex
          ((fivefoldP77RawPatchCutRouteRawComparison f g h k
            (reassocCutRoute f g h k route s)).backwardIndex i)
    simpa only [fivefoldP77RawPatchCutRouteRawComparison_backwardIndex] using
      reassocStep_backward f g h k route step i
  · intro witness
    change fivefoldP77RawPatchRefinementPlanPullback f g h k
      (stepPlan f g h k step) ((reassocWitnessEquiv f g h k route m).symm witness) =
      (reassocWitnessEquiv f g h k route s).symm
        (fivefoldP77RawPatchRefinementPlanPullback f g h k
          (stepPlan f g h k (reassocStep f g h k route step)) witness)
    apply (reassocWitnessEquiv f g h k route s).injective
    rw [Equiv.apply_symm_apply]
    simpa only [Equiv.apply_symm_apply] using
      reassocStep_pullback f g h k route step
        ((reassocWitnessEquiv f g h k route m).symm witness)

#print axioms PlanObservedEq
#print axioms planObservedEq_refl
#print axioms planObservedEq_symm
#print axioms planObservedEq_trans
#print axioms planObservedEq_comp
#print axioms planObservedEq_assoc
#print axioms planObservedEq_left_refl
#print axioms planObservedEq_right_refl
#print axioms planObservedEq_recut_trans
#print axioms planObservedEq_reassocStep

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
