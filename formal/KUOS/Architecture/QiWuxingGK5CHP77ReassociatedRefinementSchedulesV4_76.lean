import KUOS.Architecture.QiWuxingGK5CHP77RecutIndexCoherenceV4_76

/-!
Qi v4.76 — REASSOCIATION OF ACTUAL FINITE REFINEMENT SCHEDULES.
Finite reassociation words preserve the chosen local plans and spatial order.
Every partial state, original step and finite schedule is transported.
Full-domain raw-index and actual source-tuple naturality is structural.
The old normalization-generated recuts supply two actual GK5CG five-cell
sides and their loop; no equality of five-cell histories is asserted.
Append-only same-root; strict 空 center; independent Kuu is a presentation.
Pinned Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Finite words in both directions of reassociation, at arbitrary depth.
The exact original local plans and their spatial order are unchanged. -/
inductive ReassocRoute
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} →
      Family f g h k u v → Family f g h k u v →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | refl {u v : FivefoldPathVertex} (family : Family f g h k u v) :
      ReassocRoute f g h k family family
  | assoc {u v w t : FivefoldPathVertex}
      (left : Family f g h k u v) (middle : Family f g h k v w)
      (right : Family f g h k w t) :
      ReassocRoute f g h k (.node (.node left middle) right)
        (.node left (.node middle right))
  | unassoc {u v w t : FivefoldPathVertex}
      (left : Family f g h k u v) (middle : Family f g h k v w)
      (right : Family f g h k w t) :
      ReassocRoute f g h k (.node left (.node middle right))
        (.node (.node left middle) right)
  | trans {u v : FivefoldPathVertex} {source middle target : Family f g h k u v}
      (firstRoute : ReassocRoute f g h k source middle)
      (secondRoute : ReassocRoute f g h k middle target) :
      ReassocRoute f g h k source target
  | left {u v w : FivefoldPathVertex}
      {source target : Family f g h k u v}
      (route : ReassocRoute f g h k source target) (right : Family f g h k v w) :
      ReassocRoute f g h k (.node source right) (.node target right)
  | right {u v w : FivefoldPathVertex}
      (left : Family f g h k u v) {source target : Family f g h k v w}
      (route : ReassocRoute f g h k source target) :
      ReassocRoute f g h k (.node left source) (.node left target)

/-- The actual reversible product reassociation of all pending/completed flags. -/
def reassocStateEquiv {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    State f g h k source ≃ State f g h k target := by
  induction route with
  | refl family => exact Equiv.refl _
  | assoc left middle right => exact Equiv.prodAssoc _ _ _
  | unassoc left middle right => exact (Equiv.prodAssoc _ _ _).symm
  | trans firstRoute secondRoute ihFirst ihSecond => exact ihFirst.trans ihSecond
  | left route right ih => exact Equiv.prodCongr ih (Equiv.refl _)
  | right left route ih => exact Equiv.prodCongr (Equiv.refl _) ih

/-- Reassociation preserves the wholly pending state. -/
theorem reassocState_initial {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    reassocStateEquiv f g h k route (initial f g h k source) =
      initial f g h k target := by
  induction route with
  | refl family => rfl
  | assoc left middle right => rfl
  | unassoc left middle right => rfl
  | trans firstRoute secondRoute ihFirst ihSecond =>
      exact (congrArg (reassocStateEquiv f g h k secondRoute) ihFirst).trans ihSecond
  | left route right ih => exact Prod.ext ih rfl
  | right left route ih => exact Prod.ext rfl ih

/-- Reassociation preserves the wholly completed state. -/
theorem reassocState_terminal {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    reassocStateEquiv f g h k route (terminal f g h k source) =
      terminal f g h k target := by
  induction route with
  | refl family => rfl
  | assoc left middle right => rfl
  | unassoc left middle right => rfl
  | trans firstRoute secondRoute ihFirst ihSecond =>
      exact (congrArg (reassocStateEquiv f g h k secondRoute) ihFirst).trans ihSecond
  | left route right ih => exact Prod.ext ih rfl
  | right left route ih => exact Prod.ext rfl ih

/-- Every partial state carries an ACTUAL original cut-route value. -/
def reassocCutRoute {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    (s : State f g h k source) →
      FivefoldP77RawPatchCutRoute f g h k (tree f g h k source s)
        (tree f g h k target (reassocStateEquiv f g h k route s)) := by
  induction route with
  | refl family => intro s; exact .refl _
  | assoc left middle right =>
      intro s
      exact .assoc (tree f g h k left s.1.1)
        (tree f g h k middle s.1.2) (tree f g h k right s.2)
  | unassoc left middle right =>
      intro s
      exact .symm (.assoc (tree f g h k left s.1)
        (tree f g h k middle s.2.1) (tree f g h k right s.2.2))
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro s
      exact .trans (ihFirst s) (ihSecond (reassocStateEquiv f g h k firstRoute s))
  | left route right ih =>
      intro s
      exact .left (ih s.1) (tree f g h k right s.2)
  | right left route ih =>
      intro s
      exact .right (tree f g h k left s.1) (ih s.2)

/-- Reindex all original raw tuples by the actual statewise cut route. -/
def reassocIndexEquiv {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) (s : State f g h k source) :
    FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s) ≃
      FivefoldP77RawPatchTreeIndex f g h k
        (tree f g h k target (reassocStateEquiv f g h k route s)) :=
  fivefoldP77RawPatchCutRouteIndexEquiv f g h k (reassocCutRoute f g h k route s)

/-- Reassociate the genuine source Type value using the original CutRoute Equiv. -/
def reassocWitnessEquiv {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) (s : State f g h k source) :
    FivefoldP77RawPatchTreeWitness f g h k (tree f g h k source s) ≃
      FivefoldP77RawPatchTreeWitness f g h k
        (tree f g h k target (reassocStateEquiv f g h k route s)) :=
  fivefoldP77RawPatchCutRouteEquiv f g h k (reassocCutRoute f g h k route s)

/-- Move the SAME actual local operation to its reassociated position. -/
def reassocStep {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    ∀ {s t : State f g h k source}, Step f g h k source s t →
      Step f g h k target (reassocStateEquiv f g h k route s)
        (reassocStateEquiv f g h k route t) := by
  induction route with
  | refl family => intro s t step; exact step
  | assoc left middle right =>
      intro s t step
      exact match step with
        | .left _ (.left _ inner ms) rs =>
            .left (.node middle right) inner (ms, rs)
        | .left _ (.right _ ls inner) rs =>
            .right left ls (.left right inner rs)
        | .right _ ls inner =>
            .right left ls.1 (.right middle ls.2 inner)
  | unassoc left middle right =>
      intro s t step
      exact match step with
        | .left _ inner rs =>
            .left right (.left middle inner rs.1) rs.2
        | .right _ ls (.left _ inner rs) =>
            .left right (.right left ls inner) rs
        | .right _ ls (.right _ ms inner) =>
            .right (.node left middle) (ls, ms) inner
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro s t step
      exact ihSecond (ihFirst step)
  | left route right ih =>
      intro s t step
      exact match step with
        | .left _ inner rs => .left right (ih inner) rs
        | .right _ ls inner => .right _ (reassocStateEquiv f g h k route ls) inner
  | right left route ih =>
      intro s t step
      exact match step with
        | .left _ inner rs => .left _ inner (reassocStateEquiv f g h k route rs)
        | .right _ ls inner => .right left ls (ih inner)

/-- Transport a finite schedule, retaining all actual intermediate states. -/
def reassocSchedule {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s t : State f g h k source} (schedule : Schedule f g h k source s t) :
    Schedule f g h k target (reassocStateEquiv f g h k route s)
      (reassocStateEquiv f g h k route t) := by
  induction schedule with
  | nil s => exact .nil target (reassocStateEquiv f g h k route s)
  | cons step rest ih => exact .cons (reassocStep f g h k route step) ih

/-- Transport preserves the actual finite concatenation of schedules. -/
theorem reassocSchedule_append {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s m t : State f g h k source}
    (firstSchedule : Schedule f g h k source s m)
    (secondSchedule : Schedule f g h k source m t) :
    reassocSchedule f g h k route (append f g h k firstSchedule secondSchedule) =
      append f g h k (reassocSchedule f g h k route firstSchedule)
        (reassocSchedule f g h k route secondSchedule) := by
  induction firstSchedule with
  | nil => rfl
  | cons step rest ih =>
      exact congrArg (fun q => Schedule.cons (reassocStep f g h k route step) q)
        (ih secondSchedule)

/-- In particular an actual complete order transports to an actual complete order. -/
def reassocComplete {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    (schedule : Schedule f g h k source (initial f g h k source)
      (terminal f g h k source)) :
    Schedule f g h k target (initial f g h k target) (terminal f g h k target) := by
  simpa only [reassocState_initial, reassocState_terminal] using
    reassocSchedule f g h k route schedule

/-- Full-domain forward naturality for one actual step, proved structurally. -/
theorem reassocStep_forward {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    ∀ {s t : State f g h k source} (step : Step f g h k source s t)
      (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source t)),
      reassocIndexEquiv f g h k route s
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k step)).forwardIndex i) =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k (reassocStep f g h k route step))).forwardIndex (reassocIndexEquiv f g h k route t i) := by
  induction route with
  | refl family => intro s t step i; rfl
  | assoc left middle right =>
      intro s t step
      match step with
      | .left _ (.left _ inner ms) rs => intro i; rfl
      | .left _ (.right _ ls inner) rs => intro i; rfl
      | .right _ ls inner => intro i; rfl
  | unassoc left middle right =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; rfl
      | .right _ ls (.left _ inner rs) => intro i; rfl
      | .right _ ls (.right _ ms inner) => intro i; rfl
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro s t step i
      exact (congrArg
        (reassocIndexEquiv f g h k secondRoute (reassocStateEquiv f g h k firstRoute s))
        (ihFirst step i)).trans
          (ihSecond (reassocStep f g h k firstRoute step)
            (reassocIndexEquiv f g h k firstRoute t i))
  | left route right ih =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; exact Prod.ext (ih inner i.1) rfl
      | .right _ ls inner => intro i; rfl
  | right left route ih =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; rfl
      | .right _ ls inner => intro i; exact Prod.ext rfl (ih inner i.2)

/-- Full-domain backward naturality for one actual step, proved structurally. -/
theorem reassocStep_backward {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    ∀ {s t : State f g h k source} (step : Step f g h k source s t)
      (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)),
      reassocIndexEquiv f g h k route t
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k step)).backwardIndex i) =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k (reassocStep f g h k route step))).backwardIndex (reassocIndexEquiv f g h k route s i) := by
  induction route with
  | refl family => intro s t step i; rfl
  | assoc left middle right =>
      intro s t step
      match step with
      | .left _ (.left _ inner ms) rs => intro i; rfl
      | .left _ (.right _ ls inner) rs => intro i; rfl
      | .right _ ls inner => intro i; rfl
  | unassoc left middle right =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; rfl
      | .right _ ls (.left _ inner rs) => intro i; rfl
      | .right _ ls (.right _ ms inner) => intro i; rfl
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro s t step i
      exact (congrArg
        (reassocIndexEquiv f g h k secondRoute (reassocStateEquiv f g h k firstRoute t))
        (ihFirst step i)).trans
          (ihSecond (reassocStep f g h k firstRoute step)
            (reassocIndexEquiv f g h k firstRoute s i))
  | left route right ih =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; exact Prod.ext (ih inner i.1) rfl
      | .right _ ls inner => intro i; rfl
  | right left route ih =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; rfl
      | .right _ ls inner => intro i; exact Prod.ext rfl (ih inner i.2)

/-- Full-domain pullback naturality for one actual step, proved structurally. -/
theorem reassocStep_pullback {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) :
    ∀ {s t : State f g h k source} (step : Step f g h k source s t)
      (i : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k source t)),
      reassocWitnessEquiv f g h k route s
        (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (stepPlan f g h k step) i) =
      fivefoldP77RawPatchRefinementPlanPullback f g h k
        (stepPlan f g h k (reassocStep f g h k route step)) (reassocWitnessEquiv f g h k route t i) := by
  induction route with
  | refl family => intro s t step i; rfl
  | assoc left middle right =>
      intro s t step
      match step with
      | .left _ (.left _ inner ms) rs => intro i; rfl
      | .left _ (.right _ ls inner) rs => intro i; rfl
      | .right _ ls inner => intro i; rfl
  | unassoc left middle right =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; rfl
      | .right _ ls (.left _ inner rs) => intro i; rfl
      | .right _ ls (.right _ ms inner) => intro i; rfl
  | trans firstRoute secondRoute ihFirst ihSecond =>
      intro s t step i
      exact (congrArg
        (reassocWitnessEquiv f g h k secondRoute (reassocStateEquiv f g h k firstRoute s))
        (ihFirst step i)).trans
          (ihSecond (reassocStep f g h k firstRoute step)
            (reassocWitnessEquiv f g h k firstRoute t i))
  | left route right ih =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; exact Prod.ext (ih inner i.1) rfl
      | .right _ ls inner => intro i; rfl
  | right left route ih =>
      intro s t step
      match step with
      | .left _ inner rs => intro i; rfl
      | .right _ ls inner => intro i; exact Prod.ext rfl (ih inner i.2)


/-- Reassociation commutes with every finite PARTIAL schedule on every target
raw tuple. No completeness or surjectivity hypothesis is required. -/
theorem reassocSchedule_forward {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s t : State f g h k source} (schedule : Schedule f g h k source s t) :
    ∀ i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source t),
      reassocIndexEquiv f g h k route s
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k schedule)).forwardIndex i) =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (schedulePlan f g h k (reassocSchedule f g h k route schedule))).forwardIndex
          (reassocIndexEquiv f g h k route t i) := by
  induction schedule with
  | nil s =>
      intro i
      change reassocIndexEquiv f g h k route s
        ((fivefoldP77RawPatchCutRouteRawComparison f g h k
          (.refl (tree f g h k source s))).forwardIndex i) =
        (fivefoldP77RawPatchCutRouteRawComparison f g h k
          (.refl (tree f g h k target (reassocStateEquiv f g h k route s)))).forwardIndex
            (reassocIndexEquiv f g h k route s i)
      simp only [recutRefl_forward]
  | cons step rest ih =>
      intro i
      exact (reassocStep_forward f g h k route step
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k rest)).forwardIndex i)).trans
        (congrArg
          (fun j => (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
            (stepPlan f g h k (reassocStep f g h k route step))).forwardIndex j)
          (ih i))

/-- The separate reverse coverage maps also commute on their entire domain. -/
theorem reassocSchedule_backward {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s t : State f g h k source} (schedule : Schedule f g h k source s t) :
    ∀ i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s),
      reassocIndexEquiv f g h k route t
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k schedule)).backwardIndex i) =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (schedulePlan f g h k (reassocSchedule f g h k route schedule))).backwardIndex
          (reassocIndexEquiv f g h k route s i) := by
  induction schedule with
  | nil s =>
      intro i
      change reassocIndexEquiv f g h k route s
        ((fivefoldP77RawPatchCutRouteRawComparison f g h k
          (.refl (tree f g h k source s))).backwardIndex i) =
        (fivefoldP77RawPatchCutRouteRawComparison f g h k
          (.refl (tree f g h k target (reassocStateEquiv f g h k route s)))).backwardIndex
            (reassocIndexEquiv f g h k route s i)
      simp only [recutRefl_backward]
  | cons step rest ih =>
      intro i
      exact (ih ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k step)).backwardIndex i)).trans
        (congrArg
          (fun j => (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
            (schedulePlan f g h k (reassocSchedule f g h k route rest))).backwardIndex j)
          (reassocStep_backward f g h k route step i))

/-- Reconstruct the SAME original source tuple along either side of the
transported schedule. The proof uses only structural componentwise naturality. -/
theorem reassocSchedule_pullback {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target)
    {s t : State f g h k source} (schedule : Schedule f g h k source s t) :
    ∀ witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k source t),
      reassocWitnessEquiv f g h k route s
        (fivefoldP77RawPatchRefinementPlanPullback f g h k
          (schedulePlan f g h k schedule) witness) =
      fivefoldP77RawPatchRefinementPlanPullback f g h k
        (schedulePlan f g h k (reassocSchedule f g h k route schedule))
          (reassocWitnessEquiv f g h k route t witness) := by
  induction schedule with
  | nil s => intro witness; rfl
  | cons step rest ih =>
      intro witness
      exact (reassocStep_pullback f g h k route step
        (fivefoldP77RawPatchRefinementPlanPullback f g h k
          (schedulePlan f g h k rest) witness)).trans
        (congrArg
          (fivefoldP77RawPatchRefinementPlanPullback f g h k
            (stepPlan f g h k (reassocStep f g h k route step)))
          (ih witness))

/-- The genuine original source path survives the statewise original recut. -/
theorem reassocState_path {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) (s : State f g h k source)
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k source s)) :
    fivefoldP77RawPatchTreePath f g h k
      (tree f g h k target (reassocStateEquiv f g h k route s))
      (reassocWitnessEquiv f g h k route s witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k source s) witness :=
  fivefoldP77RawPatchCutRoute_path f g h k (reassocCutRoute f g h k route s) witness

/-- Factorwise compatibility is unchanged at EVERY partial state. -/
theorem reassocState_compatible_iff {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) (s : State f g h k source) :
    fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k source s) ↔
      fivefoldP77RawPatchTreeCompatible f g h k
        (tree f g h k target (reassocStateEquiv f g h k route s)) :=
  fivefoldP77RawPatchCutRoute_compatible_iff f g h k (reassocCutRoute f g h k route s)

/-- The designated factorwise obstruction is unchanged at every partial state. -/
theorem reassocState_obstructed_iff {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    (route : ReassocRoute f g h k source target) (s : State f g h k source) :
    fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k source s) ↔
      fivefoldP77RawPatchTreeObstructed f g h k
        (tree f g h k target (reassocStateEquiv f g h k route s)) := by
  rw [fivefoldP77RawPatchTree_obstructed_iff, fivefoldP77RawPatchTree_obstructed_iff]
  exact not_congr (reassocState_compatible_iff f g h k route s)

section ReassocSquare
variable {u v : FivefoldPathVertex} {source target : Family f g h k u v}
variable (route : ReassocRoute f g h k source target)
variable {s t : State f g h k source} (schedule : Schedule f g h k source s t)

/-- First execute the original schedule, then the actual target-state recut. -/
def scheduleThenRecut :
    FivefoldP77RawPatchRefinementPlan f g h k (tree f g h k source s)
      (tree f g h k target (reassocStateEquiv f g h k route t)) :=
  .trans (schedulePlan f g h k schedule)
    (.presentation (.recut (reassocCutRoute f g h k route t)))

/-- First recut the actual source state, then execute every transported step. -/
def recutThenSchedule :
    FivefoldP77RawPatchRefinementPlan f g h k (tree f g h k source s)
      (tree f g h k target (reassocStateEquiv f g h k route t)) :=
  .trans (.presentation (.recut (reassocCutRoute f g h k route s)))
    (schedulePlan f g h k (reassocSchedule f g h k route schedule))

/-- The two ORIGINAL plans of the recut/schedule square agree on every target
raw index, using the proved normalization bridge for the existing recut data. -/
theorem reassocSquare_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (scheduleThenRecut f g h k route schedule)).forwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (recutThenSchedule f g h k route schedule)).forwardIndex i := by
  change (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
    (schedulePlan f g h k schedule)).forwardIndex
      ((fivefoldP77RawPatchCutRouteRawComparison f g h k
        (reassocCutRoute f g h k route t)).forwardIndex i) =
    (fivefoldP77RawPatchCutRouteRawComparison f g h k
      (reassocCutRoute f g h k route s)).forwardIndex
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k (reassocSchedule f g h k route schedule))).forwardIndex i)
  simp only [fivefoldP77RawPatchCutRouteRawComparison_forwardIndex]
  change (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
    (schedulePlan f g h k schedule)).forwardIndex
      ((reassocIndexEquiv f g h k route t).symm i) =
    (reassocIndexEquiv f g h k route s).symm
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (schedulePlan f g h k (reassocSchedule f g h k route schedule))).forwardIndex i)
  apply (reassocIndexEquiv f g h k route s).injective
  rw [Equiv.apply_symm_apply]
  simpa only [Equiv.apply_symm_apply] using
    reassocSchedule_forward f g h k route schedule
      ((reassocIndexEquiv f g h k route t).symm i)

/-- The separately retained reverse raw maps agree on the entire source domain. -/
theorem reassocSquare_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (scheduleThenRecut f g h k route schedule)).backwardIndex i =
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (recutThenSchedule f g h k route schedule)).backwardIndex i := by
  change (fivefoldP77RawPatchCutRouteRawComparison f g h k
    (reassocCutRoute f g h k route t)).backwardIndex
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (schedulePlan f g h k schedule)).backwardIndex i) =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k (reassocSchedule f g h k route schedule))).backwardIndex
        ((fivefoldP77RawPatchCutRouteRawComparison f g h k
          (reassocCutRoute f g h k route s)).backwardIndex i)
  simpa only [fivefoldP77RawPatchCutRouteRawComparison_backwardIndex] using
    reassocSchedule_backward f g h k route schedule i

/-- Recut-before and recut-after reconstruct the same exact source witness.
The proof is the structural source naturality square and Equiv inverse laws. -/
theorem reassocSquare_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (scheduleThenRecut f g h k route schedule) witness =
      fivefoldP77RawPatchRefinementPlanPullback f g h k
        (recutThenSchedule f g h k route schedule) witness := by
  change fivefoldP77RawPatchRefinementPlanPullback f g h k
    (schedulePlan f g h k schedule) ((reassocWitnessEquiv f g h k route t).symm witness) =
    (reassocWitnessEquiv f g h k route s).symm
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (schedulePlan f g h k (reassocSchedule f g h k route schedule)) witness)
  apply (reassocWitnessEquiv f g h k route s).injective
  rw [Equiv.apply_symm_apply]
  simpa only [Equiv.apply_symm_apply] using
    reassocSchedule_pullback f g h k route schedule
      ((reassocWitnessEquiv f g h k route t).symm witness)

/-- Two genuine GK5CG five-cell sides with the SAME actual raw four-cell
endpoints. Both original normalization-generated recut histories are retained. -/
def reassocRawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :=
  planRawSquare f g h k (scheduleThenRecut f g h k route schedule)
    (recutThenSchedule f g h k route schedule)
    (reassocSquare_forward f g h k route schedule) i

/-- The actual five-cell loop of the two sides; no triviality is asserted. -/
def reassocRawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :=
  planRawLoop f g h k (scheduleThenRecut f g h k route schedule)
    (recutThenSchedule f g h k route schedule)
    (reassocSquare_forward f g h k route schedule) i

/-- Both sides preserve the exact original source path. -/
theorem reassocSquare_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (scheduleThenRecut f g h k route schedule) witness) =
      fivefoldP77RawPatchTreePath f g h k
        (tree f g h k target (reassocStateEquiv f g h k route t)) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (recutThenSchedule f g h k route schedule) witness) =
      fivefoldP77RawPatchTreePath f g h k
        (tree f g h k target (reassocStateEquiv f g h k route t)) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k
      (scheduleThenRecut f g h k route schedule) witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k
      (recutThenSchedule f g h k route schedule) witness⟩

/-- Both sides preserve the original source-certified P77 partial Hom. -/
theorem reassocSquare_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (scheduleThenRecut f g h k route schedule) witness) =
      fivefoldP77RawPatchTreeCertified f g h k
        (tree f g h k target (reassocStateEquiv f g h k route t)) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (recutThenSchedule f g h k route schedule) witness) =
      fivefoldP77RawPatchTreeCertified f g h k
        (tree f g h k target (reassocStateEquiv f g h k route t)) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k
      (scheduleThenRecut f g h k route schedule) witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k
      (recutThenSchedule f g h k route schedule) witness⟩

/-- Actual terminal evidence certifies each side while preserving that SAME
side's exact chosen raw comparison, including its five-cell Type values. -/
theorem reassocSquare_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k target (reassocStateEquiv f g h k route t))) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (scheduleThenRecut f g h k route schedule) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (scheduleThenRecut f g h k route schedule)) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (recutThenSchedule f g h k route schedule) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (recutThenSchedule f g h k route schedule)) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k
      (scheduleThenRecut f g h k route schedule) witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k
      (recutThenSchedule f g h k route schedule) witness⟩

/-- Compatibility of every intermediate level of either side is equivalent
to the ORIGINAL endpoint factor family, before the final reassociation. -/
theorem reassocSquare_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (scheduleThenRecut f g h k route schedule) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k source t)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (recutThenSchedule f g h k route schedule) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k source t)) :=
  ⟨(fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k
      (scheduleThenRecut f g h k route schedule)).trans
      (reassocState_compatible_iff f g h k route t).symm,
    (fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k
      (recutThenSchedule f g h k route schedule)).trans
      (reassocState_compatible_iff f g h k route t).symm⟩

/-- A designated original endpoint factor obstruction survives on either side.
Moving the recut across a finite schedule does not manufacture missing evidence. -/
theorem reassocSquare_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (scheduleThenRecut f g h k route schedule) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k source t)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (recutThenSchedule f g h k route schedule) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k source t)) :=
  ⟨(fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k
      (scheduleThenRecut f g h k route schedule)).trans
      (reassocState_obstructed_iff f g h k route t).symm,
    (fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k
      (recutThenSchedule f g h k route schedule)).trans
      (reassocState_obstructed_iff f g h k route t).symm⟩

end ReassocSquare

#print axioms ReassocRoute
#print axioms reassocStateEquiv
#print axioms reassocState_initial
#print axioms reassocState_terminal
#print axioms reassocCutRoute
#print axioms reassocIndexEquiv
#print axioms reassocWitnessEquiv
#print axioms reassocStep
#print axioms reassocSchedule
#print axioms reassocSchedule_append
#print axioms reassocComplete
#print axioms reassocStep_forward
#print axioms reassocStep_backward
#print axioms reassocStep_pullback
#print axioms reassocSchedule_forward
#print axioms reassocSchedule_backward
#print axioms reassocSchedule_pullback
#print axioms reassocState_path
#print axioms reassocState_compatible_iff
#print axioms reassocState_obstructed_iff
#print axioms scheduleThenRecut
#print axioms recutThenSchedule
#print axioms reassocSquare_forward
#print axioms reassocSquare_backward
#print axioms reassocSquare_pullback
#print axioms reassocRawSquare
#print axioms reassocRawLoop
#print axioms reassocSquare_path
#print axioms reassocSquare_certified
#print axioms reassocSquare_certify_raw
#print axioms reassocSquare_allCompatible_iff
#print axioms reassocSquare_obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified



