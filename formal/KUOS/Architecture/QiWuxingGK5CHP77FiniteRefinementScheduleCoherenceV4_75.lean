import KUOS.Architecture.QiWuxingGK5CHP77TerminalCertifiedRefinementHierarchyV4_74
import Mathlib.Tactic

/-!
Qi v4.75 — FINITE ORIGINAL P77 REFINEMENT SCHEDULES.

A finite endpoint-typed family retains each chosen original refinement plan.
A Boolean at each active leaf records pending/completed status; fixed leaves
allow zero operations. A step executes exactly one pending leaf. Finite
schedules retain every intermediate state and actual operation order.
Every state has a recursively constructed completion.

All complete schedules induce the same full-tuple forward/backward coverage
maps and the same reconstructed Type-valued source witness, proved by
structural recursion rather than raw-history proof irrelevance. Their actual
GK5CG five-cell values remain separately retained. Shared recut/presentation
histories preserve these conclusions, terminal certification, original paths
and designated factorwise obstruction.

Append-only same-root; strict 空 center; independent Kuu is a presentation.
Original F55/P77/P94A, physical C60 and north C60 CRT keep their own types.
Public root107; protected #1558 stays validation-only Draft/open/unmerged.
No sorry/admit/new axioms/native_decide. Lean v4.30.0-rc2;
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- A finite composable family of independent, genuinely chosen plans.
A fixed tree contributes no operation. Leaf plans may themselves contain
arbitrary finite subdivision, recut and presentation histories. -/
inductive Family
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    FivefoldPathVertex → FivefoldPathVertex →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | fixed {u v : FivefoldPathVertex}
      (base : FivefoldP77RawPatchCutTree f g h k u v) : Family f g h k u v
  | leaf {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
      Family f g h k u v
  | node {u v w : FivefoldPathVertex}
      (left : Family f g h k u v) (right : Family f g h k v w) :
      Family f g h k u w

/-- Pending/completed flags, retaining the family's parenthesization. -/
def State {u v : FivefoldPathVertex} (family : Family f g h k u v) : Type :=
  match family with
  | .fixed _ => PUnit
  | .leaf _ => Bool
  | .node left right => State f g h k left × State f g h k right

/-- The actual original cut tree at a partially executed state. -/
def tree {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    State f g h k family → FivefoldP77RawPatchCutTree f g h k u v := by
  induction family with
  | fixed base => exact fun _ => base
  | @leaf u v source target plan =>
      exact fun done => match done with
        | false => source
        | true => target
  | node left right ihLeft ihRight =>
      exact fun state => .node (ihLeft state.1) (ihRight state.2)

/-- No chosen local plan has yet been executed. -/
def initial {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    State f g h k family :=
  match family with
  | .fixed _ => PUnit.unit
  | .leaf _ => false
  | .node left right => (initial f g h k left, initial f g h k right)

/-- Every chosen local plan has been executed. -/
def terminal {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    State f g h k family :=
  match family with
  | .fixed _ => PUnit.unit
  | .leaf _ => true
  | .node left right => (terminal f g h k left, terminal f g h k right)

/-- Execute one pending factor, at any depth. There is no true-to-false
constructor, so a local operation cannot be silently repeated or undone. -/
inductive Step
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} → (family : Family f g h k u v) →
      State f g h k family → State f g h k family →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | leaf {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
      Step f g h k (.leaf plan) false true
  | left {u v w : FivefoldPathVertex}
      {left : Family f g h k u v} (right : Family f g h k v w)
      {s t : State f g h k left}
      (step : Step f g h k left s t) (rs : State f g h k right) :
      Step f g h k (.node left right) (s, rs) (t, rs)
  | right {u v w : FivefoldPathVertex}
      (left : Family f g h k u v) {right : Family f g h k v w}
      (ls : State f g h k left) {s t : State f g h k right}
      (step : Step f g h k right s t) :
      Step f g h k (.node left right) (ls, s) (ls, t)

/-- Interpret one executed factor using the original plan and actual
left/right five-cell whiskering, without postulating new comparison data. -/
def stepPlan {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (step : Step f g h k family s t) :
    FivefoldP77RawPatchRefinementPlan f g h k
      (tree f g h k family s) (tree f g h k family t) := by
  induction step with
  | leaf plan => exact plan
  | left right step rs ih => exact .left ih (tree f g h k right rs)
  | right left ls step ih => exact .right (tree f g h k left ls) ih

/-- A finite actual schedule, indexed by its initial and final states.
The list of intermediate states and order of individual steps are retained. -/
inductive Schedule
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} → (family : Family f g h k u v) →
      State f g h k family → State f g h k family →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | nil {u v : FivefoldPathVertex}
      (family : Family f g h k u v) (s : State f g h k family) :
      Schedule f g h k family s s
  | cons {u v : FivefoldPathVertex} {family : Family f g h k u v}
      {s m t : State f g h k family}
      (step : Step f g h k family s m)
      (rest : Schedule f g h k family m t) :
      Schedule f g h k family s t

/-- The finite scheduler compiles to the unchanged v4.74 plan Type. -/
def schedulePlan {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (schedule : Schedule f g h k family s t) :
    FivefoldP77RawPatchRefinementPlan f g h k
      (tree f g h k family s) (tree f g h k family t) := by
  induction schedule with
  | nil family s => exact .presentation (.recut (.refl (tree f g h k family s)))
  | cons step rest ih => exact .trans (stepPlan f g h k step) ih

/-- Concatenate actual finite schedules at their exact common state. -/
def append {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s m t : State f g h k family}
    (firstSchedule : Schedule f g h k family s m)
    (secondSchedule : Schedule f g h k family m t) :
    Schedule f g h k family s t := by
  induction firstSchedule with
  | nil => exact secondSchedule
  | cons step rest ih => exact .cons step ih

/-- Lift every individual step into a fixed right state. -/
def left {u v w : FivefoldPathVertex} {leftFamily : Family f g h k u v}
    {s t : State f g h k leftFamily}
    (schedule : Schedule f g h k leftFamily s t)
    (rightFamily : Family f g h k v w) (rs : State f g h k rightFamily) :
    Schedule f g h k (.node leftFamily rightFamily) (s, rs) (t, rs) := by
  induction schedule with
  | nil family s => exact .nil (.node family rightFamily) (s, rs)
  | cons step rest ih => exact .cons (.left rightFamily step rs) ih

/-- Lift every individual step into a fixed left state. -/
def right {u v w : FivefoldPathVertex}
    (leftFamily : Family f g h k u v) (ls : State f g h k leftFamily)
    {rightFamily : Family f g h k v w} {s t : State f g h k rightFamily}
    (schedule : Schedule f g h k rightFamily s t) :
    Schedule f g h k (.node leftFamily rightFamily) (ls, s) (ls, t) := by
  induction schedule with
  | nil family s => exact .nil (.node leftFamily family) (ls, s)
  | cons step rest ih => exact .cons (.right leftFamily ls step) ih

/-- Every partial state has an ACTUAL finite completion. Thus the subsequent
universal order results do not quantify over an empty schedule Type. -/
def complete {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    (s : State f g h k family) →
      Schedule f g h k family s (terminal f g h k family) := by
  induction family with
  | fixed base =>
      intro s
      cases s
      exact .nil (.fixed base) PUnit.unit
  | leaf plan =>
      intro s
      cases s with
      | false => exact .cons (.leaf plan) (.nil (.leaf plan) true)
      | true => exact .nil (.leaf plan) true
  | node leftFamily rightFamily ihLeft ihRight =>
      intro s
      exact append f g h k
        (left f g h k (ihLeft s.1) rightFamily s.2)
        (right f g h k leftFamily (terminal f g h k leftFamily) (ihRight s.2))

/-- Direct terminal-to-state coverage, calculated independently factor by
factor. These maps are not assumed bijective. -/
def forward {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    (s : State f g h k family) →
      FivefoldP77RawPatchTreeIndex f g h k
        (tree f g h k family (terminal f g h k family)) →
      FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family s) := by
  induction family with
  | fixed base => exact fun _ i => i
  | leaf plan =>
      intro s
      cases s with
      | false => exact (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan).forwardIndex
      | true => exact fun i => i
  | node leftFamily rightFamily ihLeft ihRight =>
      exact fun s i => (ihLeft s.1 i.1, ihRight s.2 i.2)

/-- Independent reverse coverage from the initial raw index tuple. -/
def backward {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    (s : State f g h k family) →
      FivefoldP77RawPatchTreeIndex f g h k
        (tree f g h k family (initial f g h k family)) →
      FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family s) := by
  induction family with
  | fixed base => exact fun _ i => i
  | leaf plan =>
      intro s
      cases s with
      | false => exact fun i => i
      | true => exact (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan).backwardIndex
  | node leftFamily rightFamily ihLeft ihRight =>
      exact fun s i => (ihLeft s.1 i.1, ihRight s.2 i.2)

/-- Direct terminal-to-state reconstruction of the ACTUAL source Type value.
No source-witness subsingleton is used in schedule order independence. -/
def pullback {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    (s : State f g h k family) →
      FivefoldP77RawPatchTreeWitness f g h k
        (tree f g h k family (terminal f g h k family)) →
      FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family s) := by
  induction family with
  | fixed base => exact fun _ witness => witness
  | leaf plan =>
      intro s
      cases s with
      | false => exact fivefoldP77RawPatchRefinementPlanPullback f g h k plan
      | true => exact fun witness => witness
  | node leftFamily rightFamily ihLeft ihRight =>
      exact fun s witness => (ihLeft s.1 witness.1, ihRight s.2 witness.2)

/-- Direct coverage is the identity at the terminal state. -/
theorem forward_terminal {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    ∀ i, forward f g h k family (terminal f g h k family) i = i := by
  induction family with
  | fixed base => intro i; rfl
  | leaf plan => intro i; rfl
  | node leftFamily rightFamily ihLeft ihRight =>
      intro i
      exact Prod.ext (ihLeft i.1) (ihRight i.2)

/-- Reverse coverage is the identity at the initial state. -/
theorem backward_initial {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    ∀ i, backward f g h k family (initial f g h k family) i = i := by
  induction family with
  | fixed base => intro i; rfl
  | leaf plan => intro i; rfl
  | node leftFamily rightFamily ihLeft ihRight =>
      intro i
      exact Prod.ext (ihLeft i.1) (ihRight i.2)

/-- Direct source reconstruction is the identity at the terminal state. -/
theorem pullback_terminal {u v : FivefoldPathVertex} (family : Family f g h k u v) :
    ∀ witness, pullback f g h k family (terminal f g h k family) witness = witness := by
  induction family with
  | fixed base => intro witness; rfl
  | leaf plan => intro witness; rfl
  | node leftFamily rightFamily ihLeft ihRight =>
      intro witness
      exact Prod.ext (ihLeft witness.1) (ihRight witness.2)

/-- One actual step respects the independent terminal-to-state index map. -/
theorem step_forward {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (step : Step f g h k family s t) :
    ∀ i, (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (stepPlan f g h k step)).forwardIndex (forward f g h k family t i) =
        forward f g h k family s i := by
  induction step with
  | leaf plan => intro i; rfl
  | left rightFamily step rs ih =>
      intro i
      exact Prod.ext (ih i.1) rfl
  | right leftFamily ls step ih =>
      intro i
      exact Prod.ext rfl (ih i.2)

/-- One actual step respects the independent initial-to-state reverse map. -/
theorem step_backward {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (step : Step f g h k family s t) :
    ∀ i, (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (stepPlan f g h k step)).backwardIndex (backward f g h k family s i) =
        backward f g h k family t i := by
  induction step with
  | leaf plan => intro i; rfl
  | left rightFamily step rs ih =>
      intro i
      exact Prod.ext (ih i.1) rfl
  | right leftFamily ls step ih =>
      intro i
      exact Prod.ext rfl (ih i.2)

/-- One step reconstructs the exact source tuple by structural calculation. -/
theorem step_pullback {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (step : Step f g h k family s t) :
    ∀ witness, fivefoldP77RawPatchRefinementPlanPullback f g h k
      (stepPlan f g h k step) (pullback f g h k family t witness) =
        pullback f g h k family s witness := by
  induction step with
  | leaf plan => intro witness; rfl
  | left rightFamily step rs ih =>
      intro witness
      exact Prod.ext (ih witness.1) rfl
  | right leftFamily ls step ih =>
      intro witness
      exact Prod.ext rfl (ih witness.2)

/-- Finite schedule coherence on EVERY terminal raw index tuple. -/
theorem schedule_forward {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (schedule : Schedule f g h k family s t) :
    ∀ i, (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k schedule)).forwardIndex (forward f g h k family t i) =
        forward f g h k family s i := by
  induction schedule with
  | nil family s => intro i; rfl
  | cons step rest ih =>
      intro i
      change (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (stepPlan f g h k step)).forwardIndex
          ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
            (schedulePlan f g h k rest)).forwardIndex _) = _
      rw [ih]
      exact step_forward f g h k step i

/-- Finite schedule coherence for the separately retained reverse coverage. -/
theorem schedule_backward {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (schedule : Schedule f g h k family s t) :
    ∀ i, (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k schedule)).backwardIndex (backward f g h k family s i) =
        backward f g h k family t i := by
  induction schedule with
  | nil family s => intro i; rfl
  | cons step rest ih =>
      intro i
      change (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (schedulePlan f g h k rest)).backwardIndex
          ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k
            (stepPlan f g h k step)).backwardIndex _) = _
      rw [step_backward]
      exact ih i

/-- Every intermediate state recovers the SAME actual terminal factor data. -/
theorem schedule_pullback {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s t : State f g h k family} (schedule : Schedule f g h k family s t) :
    ∀ witness, fivefoldP77RawPatchRefinementPlanPullback f g h k
      (schedulePlan f g h k schedule) (pullback f g h k family t witness) =
        pullback f g h k family s witness := by
  induction schedule with
  | nil family s => intro witness; rfl
  | cons step rest ih =>
      intro witness
      change fivefoldP77RawPatchRefinementPlanPullback f g h k
        (stepPlan f g h k step)
          (fivefoldP77RawPatchRefinementPlanPullback f g h k
            (schedulePlan f g h k rest) _) = _
      rw [ih]
      exact step_pullback f g h k step witness


/-- A complete schedule has the directly calculated full forward coverage. -/
theorem complete_forward {u v : FivefoldPathVertex} {family : Family f g h k u v}
    (schedule : Schedule f g h k family
      (initial f g h k family) (terminal f g h k family))
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family (terminal f g h k family))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k schedule)).forwardIndex i =
        forward f g h k family (initial f g h k family) i := by
  have hs := schedule_forward f g h k schedule i
  rw [forward_terminal f g h k family] at hs
  exact hs

/-- A complete schedule has the directly calculated full reverse coverage. -/
theorem complete_backward {u v : FivefoldPathVertex} {family : Family f g h k u v}
    (schedule : Schedule f g h k family
      (initial f g h k family) (terminal f g h k family))
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family (initial f g h k family))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k schedule)).backwardIndex i =
        backward f g h k family (terminal f g h k family) i := by
  have hs := schedule_backward f g h k schedule i
  rw [backward_initial f g h k family] at hs
  exact hs

/-- Arbitrary finite complete orders reconstruct the direct source tuple. -/
theorem complete_pullback {u v : FivefoldPathVertex} {family : Family f g h k u v}
    (schedule : Schedule f g h k family
      (initial f g h k family) (terminal f g h k family))
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k family (terminal f g h k family))) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (schedulePlan f g h k schedule) witness =
        pullback f g h k family (initial f g h k family) witness := by
  have hs := schedule_pullback f g h k schedule witness
  rw [pullback_terminal f g h k family] at hs
  exact hs

/-- The direct reconstructed witness keeps the exact original source path
at EVERY partially executed state, via its constructed finite completion. -/
theorem pullback_path {u v : FivefoldPathVertex} (family : Family f g h k u v)
    (s : State f g h k family)
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k family (terminal f g h k family))) :
    fivefoldP77RawPatchTreePath f g h k (tree f g h k family s)
      (pullback f g h k family s witness) =
        fivefoldP77RawPatchTreePath f g h k
          (tree f g h k family (terminal f g h k family)) witness := by
  have hs := schedule_pullback f g h k (complete f g h k family s) witness
  rw [pullback_terminal f g h k family] at hs
  have hp := fivefoldP77RawPatchRefinementPlanPullback_path f g h k
    (schedulePlan f g h k (complete f g h k family s)) witness
  rw [hs] at hp
  exact hp

/-- Equal coverage aligns endpoints of two ACTUAL original five-cell values.
The index equality is explicit input; no equality of five-cell values is used. -/
def planRawSquare {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (firstPlan secondPlan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (sameIndex : ∀ i,
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).forwardIndex i =
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan).forwardIndex i)
    (i : FivefoldP77RawPatchTreeIndex f g h k target) :
    let Cell := NativeGK5CGConservativeFiveCell first last
      (fivefoldP77RawPatchTreeRaw f g h k source
        ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).forwardIndex i))
      (fivefoldP77RawPatchTreeRaw f g h k target i)
    Cell × Cell := by
  refine ⟨(fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).forwardCell i, ?_⟩
  have hc := (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan).forwardCell i
  rw [← sameIndex i] at hc
  exact hc

/-- Retain the loop between the two chosen five-cell histories; neither
triviality nor nontriviality of this loop is asserted. -/
def planRawLoop {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (firstPlan secondPlan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (sameIndex : ∀ i,
      (fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan).forwardIndex i =
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan).forwardIndex i)
    (i : FivefoldP77RawPatchTreeIndex f g h k target) :
    NativeGK5CGConservativeFiveCell first last
      (fivefoldP77RawPatchTreeRaw f g h k target i)
      (fivefoldP77RawPatchTreeRaw f g h k target i) :=
  .trans (planRawSquare f g h k firstPlan secondPlan sameIndex i).1.symm
    (planRawSquare f g h k firstPlan secondPlan sameIndex i).2

section CompleteOrders
variable {u v : FivefoldPathVertex} {family : Family f g h k u v}
variable (firstSchedule secondSchedule : Schedule f g h k family
  (initial f g h k family) (terminal f g h k family))

/-- ANY two complete schedules agree on every forward raw index tuple. -/
theorem order_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family (terminal f g h k family))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k firstSchedule)).forwardIndex i =
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k secondSchedule)).forwardIndex i :=
  (complete_forward f g h k firstSchedule i).trans
    (complete_forward f g h k secondSchedule i).symm

/-- Reverse coverage is also order-independent without assuming an inverse. -/
theorem order_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family (initial f g h k family))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k firstSchedule)).backwardIndex i =
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k secondSchedule)).backwardIndex i :=
  (complete_backward f g h k firstSchedule i).trans
    (complete_backward f g h k secondSchedule i).symm

/-- Equality of genuine source tuples is derived componentwise; no
subsingleton argument is used for this finite order theorem. -/
theorem order_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k family (terminal f g h k family))) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (schedulePlan f g h k firstSchedule) witness =
        fivefoldP77RawPatchRefinementPlanPullback f g h k
          (schedulePlan f g h k secondSchedule) witness :=
  (complete_pullback f g h k firstSchedule witness).trans
    (complete_pullback f g h k secondSchedule witness).symm

/-- Two arbitrary finite orders retain two original five-cell values with
the same actual raw four-cell endpoints at every terminal index tuple. -/
def orderRawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family (terminal f g h k family))) :=
  planRawSquare f g h k (schedulePlan f g h k firstSchedule)
    (schedulePlan f g h k secondSchedule)
    (order_forward f g h k firstSchedule secondSchedule) i

/-- The actual five-cell loop of any two complete orders remains data. -/
def orderRawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family (terminal f g h k family))) :=
  planRawLoop f g h k (schedulePlan f g h k firstSchedule)
    (schedulePlan f g h k secondSchedule)
    (order_forward f g h k firstSchedule secondSchedule) i
end CompleteOrders

section AdjacentExchange
variable {u v w : FivefoldPathVertex}
variable {leftFamily : Family f g h k u v} {rightFamily : Family f g h k v w}
variable {ls lt : State f g h k leftFamily} {rs rt : State f g h k rightFamily}
variable (leftStep : Step f g h k leftFamily ls lt)
variable (rightStep : Step f g h k rightFamily rs rt)

/-- One actual adjacent order, with its mixed intermediate state. -/
def adjacentLeftFirst :
    Schedule f g h k (.node leftFamily rightFamily) (ls, rs) (lt, rt) :=
  .cons (.left rightFamily leftStep rs)
    (.cons (.right leftFamily lt rightStep) (.nil _ (lt, rt)))

/-- The exchanged adjacent order retains the other mixed intermediate state. -/
def adjacentRightFirst :
    Schedule f g h k (.node leftFamily rightFamily) (ls, rs) (lt, rt) :=
  .cons (.right leftFamily ls rightStep)
    (.cons (.left rightFamily leftStep rt) (.nil _ (lt, rt)))

/-- Adjacent exchange is valid on every raw tuple even in a partial schedule. -/
theorem adjacent_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k (.node leftFamily rightFamily) (lt, rt))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k (adjacentLeftFirst f g h k leftStep rightStep))).forwardIndex i =
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k (adjacentRightFirst f g h k leftStep rightStep))).forwardIndex i :=
  rfl

/-- The independently retained reverse maps also commute by computation. -/
theorem adjacent_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k (.node leftFamily rightFamily) (ls, rs))) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (schedulePlan f g h k (adjacentLeftFirst f g h k leftStep rightStep))).backwardIndex i =
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k (adjacentRightFirst f g h k leftStep rightStep))).backwardIndex i :=
  rfl

/-- Adjacent independent operations restore the same exact source tuple. -/
theorem adjacent_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k (.node leftFamily rightFamily) (lt, rt))) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (schedulePlan f g h k (adjacentLeftFirst f g h k leftStep rightStep)) witness =
        fivefoldP77RawPatchRefinementPlanPullback f g h k
          (schedulePlan f g h k (adjacentRightFirst f g h k leftStep rightStep)) witness :=
  rfl

/-- An adjacent exchange has two real five-cell sides, without identifying them. -/
def adjacentRawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k (.node leftFamily rightFamily) (lt, rt))) :=
  planRawSquare f g h k
    (schedulePlan f g h k (adjacentLeftFirst f g h k leftStep rightStep))
    (schedulePlan f g h k (adjacentRightFirst f g h k leftStep rightStep))
    (adjacent_forward f g h k leftStep rightStep) i
end AdjacentExchange

/-- Supply the actual terminal source witness to certify a finite schedule. -/
def certify {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s : State f g h k family}
    (schedule : Schedule f g h k family s (terminal f g h k family))
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k family (terminal f g h k family))) :
    FivefoldP77RawPatchSubdivisionRoute f g h k
      (tree f g h k family s)
      (tree f g h k family (terminal f g h k family)) :=
  fivefoldP77RawPatchRefinementPlanCertify f g h k
    (schedulePlan f g h k schedule) witness

/-- Certification preserves THIS schedule's exact chosen raw five-cell data. -/
theorem certify_raw {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s : State f g h k family}
    (schedule : Schedule f g h k family s (terminal f g h k family))
    (witness : FivefoldP77RawPatchTreeWitness f g h k
      (tree f g h k family (terminal f g h k family))) :
    fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (certify f g h k schedule witness) =
        fivefoldP77RawPatchRefinementPlanRawComparison f g h k
          (schedulePlan f g h k schedule) :=
  fivefoldP77RawPatchRefinementPlanCertify_raw f g h k
    (schedulePlan f g h k schedule) witness

/-- Every prescribed stage of ANY complete order is compatible exactly when
the actual terminal factor family is compatible. -/
theorem allCompatible_iff {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s : State f g h k family}
    (schedule : Schedule f g h k family s (terminal f g h k family)) :
    fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (schedulePlan f g h k schedule) ↔
        fivefoldP77RawPatchTreeCompatible f g h k
          (tree f g h k family (terminal f g h k family)) :=
  fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k
    (schedulePlan f g h k schedule)

/-- The terminal factorwise obstruction survives every finite execution order. -/
theorem obstructed_iff {u v : FivefoldPathVertex} {family : Family f g h k u v}
    {s : State f g h k family}
    (schedule : Schedule f g h k family s (terminal f g h k family)) :
    ¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (schedulePlan f g h k schedule) ↔
        fivefoldP77RawPatchTreeObstructed f g h k
          (tree f g h k family (terminal f g h k family)) :=
  fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k
    (schedulePlan f g h k schedule)


#print axioms Family
#print axioms State
#print axioms tree
#print axioms initial
#print axioms terminal
#print axioms Step
#print axioms stepPlan
#print axioms Schedule
#print axioms schedulePlan
#print axioms append
#print axioms left
#print axioms right
#print axioms complete
#print axioms forward
#print axioms backward
#print axioms pullback
#print axioms forward_terminal
#print axioms backward_initial
#print axioms pullback_terminal
#print axioms step_forward
#print axioms step_backward
#print axioms step_pullback
#print axioms schedule_forward
#print axioms schedule_backward
#print axioms schedule_pullback
#print axioms complete_forward
#print axioms complete_backward
#print axioms complete_pullback
#print axioms pullback_path
#print axioms planRawSquare
#print axioms planRawLoop
#print axioms order_forward
#print axioms order_backward
#print axioms order_pullback
#print axioms orderRawSquare
#print axioms orderRawLoop
#print axioms adjacentLeftFirst
#print axioms adjacentRightFirst
#print axioms adjacent_forward
#print axioms adjacent_backward
#print axioms adjacent_pullback
#print axioms adjacentRawSquare
#print axioms certify
#print axioms certify_raw
#print axioms allCompatible_iff
#print axioms obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
