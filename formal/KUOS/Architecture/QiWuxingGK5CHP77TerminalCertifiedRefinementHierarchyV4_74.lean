import KUOS.Architecture.QiWuxingGK5CHP77CertifiedMixedSubdivisionFiveCellV4_73
import Mathlib.Logic.Equiv.Prod
import Mathlib.Tactic

/-!
Qi v4.74 — TERMINAL-CERTIFIED HIERARCHICAL ORIGINAL P77 REFINEMENT.

A directed finite refinement plan retains all chosen original raw five-cell
comparisons but does not assume fine source certificates at each split.
Actual final factorwise source data pull back through the entire hierarchy
by genuine gluing, deriving every intermediate certificate and a v4.70
certified route. Recut and covered presentation changes remain reversible;
uncertified subdivision has no free inverse constructor.

The certified interpretation preserves the plan's EXACT raw comparison,
including both index maps and chosen original five-cell values. This is
agreement of two interpretations of ONE plan, not equality of different
raw histories. All designated hierarchy levels are compatible exactly when
the terminal fine tree is compatible. A genuine coarse witness alone
does not remove a terminal factorwise obstruction.

Independent left/right refinements construct both operation orders, with
equal full-tuple index maps and two retained actual five-cell histories.
No new interchange five-cell equality or higher coherence is postulated.

Append-only same-root. Strict 空 center; independent Kuu is a presentation.
Original F55/P77/P94A, physical C60 and north C60 CRT remain distinct.
Public root 107; protected #1558 validation-only Draft/open/unmerged.
No new axioms, sorry, admit or native_decide. Lean v4.30.0-rc2;
pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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




/-- A directed finite refinement hierarchy. Original raw comparisons are
data at every split; factorwise source certificates are deliberately not
assumed. A free inverse would invalidate terminal-to-intermediate descent. -/
inductive FivefoldP77RawPatchRefinementPlan
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    {u v : FivefoldPathVertex} →
      FivefoldP77RawPatchCutTree f g h k u v →
      FivefoldP77RawPatchCutTree f g h k u v →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | presentation {u v : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (route : FivefoldP77RawPatchPresentationRoute f g h k source target) :
      FivefoldP77RawPatchRefinementPlan f g h k source target
  | subdivide {u v : FivefoldPathVertex}
      (block : FivefoldP77RawPatchBlock f g h k u v)
      (tree : FivefoldP77RawPatchCutTree f g h k u v)
      (comparison : FivefoldP77RawPatchBlockComparison f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k tree)) block) :
      FivefoldP77RawPatchRefinementPlan f g h k
        (fivefoldP77RawPatchBlockTree f g h k block) tree
  | trans {u v : FivefoldPathVertex}
      {source middle target : FivefoldP77RawPatchCutTree f g h k u v}
      (firstPlan : FivefoldP77RawPatchRefinementPlan f g h k source middle)
      (secondPlan : FivefoldP77RawPatchRefinementPlan f g h k middle target) :
      FivefoldP77RawPatchRefinementPlan f g h k source target
  | left {u v w : FivefoldPathVertex}
      {source target : FivefoldP77RawPatchCutTree f g h k u v}
      (plan : FivefoldP77RawPatchRefinementPlan f g h k source target)
      (right : FivefoldP77RawPatchCutTree f g h k v w) :
      FivefoldP77RawPatchRefinementPlan f g h k
        (.node source right) (.node target right)
  | right {u v w : FivefoldPathVertex}
      (left : FivefoldP77RawPatchCutTree f g h k u v)
      {source target : FivefoldP77RawPatchCutTree f g h k v w}
      (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
      FivefoldP77RawPatchRefinementPlan f g h k
        (.node left source) (.node left target)

/-- Retain the genuine original five-cells of the plan before any source
certificate is supplied, at every tuple of original raw patch indices. -/
def fivefoldP77RawPatchRefinementPlanRawComparison
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    FivefoldP77RawPatchBlockComparison f g h k
      (fivefoldP77RawPatchTreeRawBlock f g h k source)
      (fivefoldP77RawPatchTreeRawBlock f g h k target) := by
  induction plan with
  | presentation route =>
      exact fivefoldP77RawPatchPresentationRouteRawComparison f g h k route
  | subdivide block tree comparison =>
      exact fivefoldP77RawPatchTreeSubdivisionRawComparison f g h k
        block tree comparison
  | trans firstPlan secondPlan ihFirst ihSecond =>
      exact fivefoldP77RawPatchBlockComparisonTrans f g h k ihFirst ihSecond
  | left plan right ih =>
      exact fivefoldP77RawPatchTreeRawComparison_left f g h k ih right
  | right left plan ih =>
      exact fivefoldP77RawPatchTreeRawComparison_right f g h k left ih

/-- Final genuine factorwise witnesses glue backwards through EVERY chosen
intermediate level. This is a map of actual source witness Types, and is
defined even if those Types are empty. -/
def fivefoldP77RawPatchRefinementPlanPullback
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    FivefoldP77RawPatchTreeWitness f g h k target →
      FivefoldP77RawPatchTreeWitness f g h k source := by
  induction plan with
  | presentation route =>
      exact fun witness =>
        (fivefoldP77RawPatchPresentationRouteEquiv f g h k route).symm witness
  | subdivide block tree comparison =>
      intro witness
      exact (fivefoldP77RawPatchBlockTreeEquiv f g h k block).symm
        (fivefoldP77RawPatchSubdivisionGlue f g h k
          (fivefoldP77RawPatchTreeFlatten f g h k tree) block comparison
          (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness))
  | trans firstPlan secondPlan ihFirst ihSecond =>
      exact fun witness => ihFirst (ihSecond witness)
  | left plan right ih =>
      exact fun witness => (ih witness.1, witness.2)
  | right left plan ih =>
      exact fun witness => (witness.1, ih witness.2)

/-- Recursive gluing keeps the exact original typed source path, not only
its conservative class or associator charge. -/
theorem fivefoldP77RawPatchRefinementPlanPullback_path
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    ∀ witness : FivefoldP77RawPatchTreeWitness f g h k target,
      fivefoldP77RawPatchTreePath f g h k source
          (fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness) =
        fivefoldP77RawPatchTreePath f g h k target witness := by
  induction plan with
  | presentation route =>
      intro witness
      have hpath := fivefoldP77RawPatchPresentationRoute_path f g h k route
        ((fivefoldP77RawPatchPresentationRouteEquiv f g h k route).symm witness)
      simpa only [Equiv.apply_symm_apply] using hpath.symm
  | subdivide block tree comparison =>
      intro witness
      change fivefoldP77RawPatchTreePath f g h k
          (fivefoldP77RawPatchBlockTree f g h k block)
          ((fivefoldP77RawPatchBlockTreeEquiv f g h k block).symm
            (fivefoldP77RawPatchSubdivisionGlue f g h k
              (fivefoldP77RawPatchTreeFlatten f g h k tree) block comparison
              (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness))) =
        fivefoldP77RawPatchTreePath f g h k tree witness
      rw [fivefoldP77RawPatchBlockTree_path, Equiv.apply_symm_apply]
      exact (fivefoldP77RawPatchTreePath_normalize f g h k tree witness).symm
  | trans firstPlan secondPlan ihFirst ihSecond =>
      intro witness
      exact (ihFirst (fivefoldP77RawPatchRefinementPlanPullback
        f g h k secondPlan witness)).trans (ihSecond witness)
  | left plan right ih =>
      intro witness
      exact congrArg
        (fun path => path.comp (fivefoldP77RawPatchTreePath f g h k right witness.2))
        (ih witness.1)
  | right left plan ih =>
      intro witness
      exact congrArg
        (fun path => (fivefoldP77RawPatchTreePath f g h k left witness.1).comp path)
        (ih witness.2)

/-- Compile the WHOLE hierarchy to the existing certified mixed-route Type.
In a sequential plan, the later gluing derives the earlier terminal witness;
no intermediate source witness or certified route is postulated. -/
def fivefoldP77RawPatchRefinementPlanCertify
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    FivefoldP77RawPatchTreeWitness f g h k target →
      FivefoldP77RawPatchSubdivisionRoute f g h k source target := by
  induction plan with
  | presentation route =>
      exact fun _ => .presentation route
  | subdivide block tree comparison =>
      exact fun witness => .subdivide block tree comparison
        (fivefoldP77RawPatchTreeNormalizeEquiv f g h k tree witness)
  | trans firstPlan secondPlan ihFirst ihSecond =>
      exact fun witness => .trans
        (ihFirst (fivefoldP77RawPatchRefinementPlanPullback
          f g h k secondPlan witness)) (ihSecond witness)
  | left plan right ih =>
      exact fun witness => .left (ih witness.1) right
  | right left plan ih =>
      exact fun witness => .right left (ih witness.2)

/-- Certification preserves the EXACT chosen raw comparison of THIS plan:
both index maps and its actual Type-valued five-cell history fields. -/
theorem fivefoldP77RawPatchRefinementPlanCertify_raw
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    ∀ witness : FivefoldP77RawPatchTreeWitness f g h k target,
      fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
          (fivefoldP77RawPatchRefinementPlanCertify f g h k plan witness) =
        fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan := by
  induction plan with
  | presentation route => intro witness; rfl
  | subdivide block tree comparison => intro witness; rfl
  | trans firstPlan secondPlan ihFirst ihSecond =>
      intro witness
      change fivefoldP77RawPatchBlockComparisonTrans f g h k
          (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
            (fivefoldP77RawPatchRefinementPlanCertify f g h k firstPlan
              (fivefoldP77RawPatchRefinementPlanPullback f g h k secondPlan witness)))
          (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
            (fivefoldP77RawPatchRefinementPlanCertify f g h k secondPlan witness)) =
        fivefoldP77RawPatchBlockComparisonTrans f g h k
          (fivefoldP77RawPatchRefinementPlanRawComparison f g h k firstPlan)
          (fivefoldP77RawPatchRefinementPlanRawComparison f g h k secondPlan)
      rw [ihFirst, ihSecond]
  | left plan right ih =>
      intro witness
      change fivefoldP77RawPatchTreeRawComparison_left f g h k
          (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
            (fivefoldP77RawPatchRefinementPlanCertify f g h k plan witness.1)) right =
        fivefoldP77RawPatchTreeRawComparison_left f g h k
          (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan) right
      rw [ih]
  | right left plan ih =>
      intro witness
      change fivefoldP77RawPatchTreeRawComparison_right f g h k left
          (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
            (fivefoldP77RawPatchRefinementPlanCertify f g h k plan witness.2)) =
        fivefoldP77RawPatchTreeRawComparison_right f g h k left
          (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan)
      rw [ih]

/-- The compiled route sends the derived coarse witness back to the supplied
terminal Type value, using original source faithfulness only at witness level. -/
theorem fivefoldP77RawPatchRefinementPlanCertify_terminal
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k target) :
    fivefoldP77RawPatchSubdivisionRouteEquiv f g h k
        (fivefoldP77RawPatchRefinementPlanCertify f g h k plan witness)
        (fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness) = witness := by
  letI := fivefoldP77RawPatchTree_witness_subsingleton f g h k target
  exact Subsingleton.elim _ _

/-- The plan's own genuine five-cell comparison commutes with gluing of
the derived coarse and supplied terminal source witnesses. -/
theorem fivefoldP77RawPatchRefinementPlanRawGlue
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k target) :
    fivefoldP77RawPatchBlockComparisonEquiv f g h k
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan)
        (fivefoldP77RawPatchTreeRawGlue f g h k source
          (fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness)) =
      fivefoldP77RawPatchTreeRawGlue f g h k target witness := by
  have hn := fivefoldP77RawPatchSubdivisionRouteRawGlue_natural f g h k
    (fivefoldP77RawPatchRefinementPlanCertify f g h k plan witness)
    (fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness)
  rw [fivefoldP77RawPatchRefinementPlanCertify_raw,
    fivefoldP77RawPatchRefinementPlanCertify_terminal] at hn
  exact hn

/-- Every original source-certified partial Hom is preserved by the derived
terminal-to-coarse map through all designated intermediate levels. -/
theorem fivefoldP77RawPatchRefinementPlanPullback_certified
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (witness : FivefoldP77RawPatchTreeWitness f g h k target) :
    fivefoldP77RawPatchTreeCertified f g h k source
        (fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness) =
      fivefoldP77RawPatchTreeCertified f g h k target witness := by
  have hn := fivefoldP77RawPatchSubdivisionRoute_certified f g h k
    (fivefoldP77RawPatchRefinementPlanCertify f g h k plan witness)
    (fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness)
  rw [fivefoldP77RawPatchRefinementPlanCertify_terminal] at hn
  exact hn.symm

/-- Fine compatibility propagates backwards; the converse requires the
specified factorwise source data and is not asserted. -/
theorem fivefoldP77RawPatchRefinementPlan_sourceCompatible
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (hc : fivefoldP77RawPatchTreeCompatible f g h k target) :
    fivefoldP77RawPatchTreeCompatible f g h k source := by
  obtain ⟨witness⟩ := (fivefoldP77RawPatchTree_witness_iff f g h k target).2 hc
  exact (fivefoldP77RawPatchTree_witness_iff f g h k source).1
    ⟨fivefoldP77RawPatchRefinementPlanPullback f g h k plan witness⟩

/-- Track compatibility at EVERY prescribed hierarchy stage, including
both endpoints of each elementary step and unchanged contextual factors. -/
def fivefoldP77RawPatchRefinementPlanAllCompatible
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) : Prop := by
  induction plan with
  | @presentation u v source target route =>
      exact fivefoldP77RawPatchTreeCompatible f g h k source ∧
        fivefoldP77RawPatchTreeCompatible f g h k target
  | subdivide block tree comparison =>
      exact fivefoldP77RawPatchTreeCompatible f g h k
          (fivefoldP77RawPatchBlockTree f g h k block) ∧
        fivefoldP77RawPatchTreeCompatible f g h k tree
  | trans firstPlan secondPlan ihFirst ihSecond =>
      exact ihFirst ∧ ihSecond
  | left plan right ih =>
      exact ih ∧ fivefoldP77RawPatchTreeCompatible f g h k right
  | right left plan ih =>
      exact fivefoldP77RawPatchTreeCompatible f g h k left ∧ ih

/-- Exact hierarchical descent criterion: genuine terminal factorwise
compatibility derives ALL earlier intermediate compatibility conditions. -/
theorem fivefoldP77RawPatchRefinementPlan_allCompatible_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    fivefoldP77RawPatchRefinementPlanAllCompatible f g h k plan ↔
      fivefoldP77RawPatchTreeCompatible f g h k target := by
  induction plan with
  | presentation route =>
      exact ⟨fun hc => hc.2, fun hc =>
        ⟨fivefoldP77RawPatchRefinementPlan_sourceCompatible f g h k
          (.presentation route) hc, hc⟩⟩
  | subdivide block tree comparison =>
      exact ⟨fun hc => hc.2, fun hc =>
        ⟨fivefoldP77RawPatchRefinementPlan_sourceCompatible f g h k
          (.subdivide block tree comparison) hc, hc⟩⟩
  | trans firstPlan secondPlan ihFirst ihSecond =>
      change (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k firstPlan ∧
        fivefoldP77RawPatchRefinementPlanAllCompatible f g h k secondPlan) ↔ _
      rw [ihFirst, ihSecond]
      exact ⟨fun hc => hc.2, fun hc =>
        ⟨fivefoldP77RawPatchRefinementPlan_sourceCompatible f g h k
          secondPlan hc, hc⟩⟩
  | left plan right ih => exact and_congr ih Iff.rfl
  | right left plan ih => exact and_congr Iff.rfl ih

/-- Failure at some specified hierarchy stage is precisely terminal
factorwise obstruction, not merely failure of coarse raw reachability. -/
theorem fivefoldP77RawPatchRefinementPlan_obstructed_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target) :
    ¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k plan ↔
      fivefoldP77RawPatchTreeObstructed f g h k target := by
  rw [fivefoldP77RawPatchTree_obstructed_iff]
  exact not_congr (fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k plan)

/-- With an actual coarse source witness, a certified route preserving THIS
plan's exact original five-cell comparison exists iff its designated finest
factors descend. No arbitrary certified route is assumed in the reverse direction. -/
theorem fivefoldP77RawPatchRefinementPlan_certification_iff
    {u v : FivefoldPathVertex}
    {source target : FivefoldP77RawPatchCutTree f g h k u v}
    (plan : FivefoldP77RawPatchRefinementPlan f g h k source target)
    (coarse : FivefoldP77RawPatchTreeWitness f g h k source) :
    (∃ route : FivefoldP77RawPatchSubdivisionRoute f g h k source target,
      fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k route =
        fivefoldP77RawPatchRefinementPlanRawComparison f g h k plan) ↔
      fivefoldP77RawPatchTreeCompatible f g h k target := by
  constructor
  · rintro ⟨route, _⟩
    exact (fivefoldP77RawPatchTree_witness_iff f g h k target).1
      ⟨fivefoldP77RawPatchSubdivisionRouteEquiv f g h k route coarse⟩
  · intro hc
    obtain ⟨fine⟩ := (fivefoldP77RawPatchTree_witness_iff f g h k target).2 hc
    exact ⟨fivefoldP77RawPatchRefinementPlanCertify f g h k plan fine,
      fivefoldP77RawPatchRefinementPlanCertify_raw f g h k plan fine⟩

/-- The obstructed inverse-e01 then forward-e01 factorization is a real
directed raw plan. Planning still does not supply its missing source factor. -/
def fivefoldP77ReverseForwardRefinementPlan :
    FivefoldP77RawPatchRefinementPlan f g h k
      (fivefoldP77RawPatchBlockTree f g h k
        (fivefoldP77RawPatchCompositeBlock f g h k
          (fivefoldP77ReverseForwardPatchChain f g h k)))
      (.leaf (fivefoldP77ReverseForwardPatchChain f g h k)) :=
  .subdivide
    (fivefoldP77RawPatchCompositeBlock f g h k
      (fivefoldP77ReverseForwardPatchChain f g h k))
    (.leaf (fivefoldP77ReverseForwardPatchChain f g h k))
    (fivefoldP77RawPatchBlockComparisonRefl f g h k
      (fivefoldP77RawPatchCompositeBlock f g h k
        (fivefoldP77ReverseForwardPatchChain f g h k)))

/-- The genuine coarse witness and genuine raw plan cannot repair the
designated terminal reverse-edge obstruction. -/
theorem fivefoldP77ReverseForwardRefinementPlan_obstructed :
    ¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (fivefoldP77ReverseForwardRefinementPlan f g h k) := by
  intro hc
  have hfine := (fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k
    (fivefoldP77ReverseForwardRefinementPlan f g h k)).1 hc
  exact fivefoldP77ReverseForwardPatchChain_noWitness f g h k
    ((fivefoldP77RawPatchTree_witness_iff f g h k
      (.leaf (fivefoldP77ReverseForwardPatchChain f g h k))).2 hfine)

section RefinementOrder

variable {u v w : FivefoldPathVertex}
variable {left₀ left₁ : FivefoldP77RawPatchCutTree f g h k u v}
variable {right₀ right₁ : FivefoldP77RawPatchCutTree f g h k v w}
variable (leftPlan : FivefoldP77RawPatchRefinementPlan f g h k left₀ left₁)
variable (rightPlan : FivefoldP77RawPatchRefinementPlan f g h k right₀ right₁)

/-- Construct the first genuine refinement order: change the left factor,
then the right factor, preserving both chosen local comparison histories. -/
def fivefoldP77RawPatchRefinementLeftThenRight :
    FivefoldP77RawPatchRefinementPlan f g h k
      (.node left₀ right₀) (.node left₁ right₁) :=
  .trans (.left leftPlan right₀) (.right left₁ rightPlan)

/-- Construct the other order from the SAME local refinement data.
The two finite history values are retained separately. -/
def fivefoldP77RawPatchRefinementRightThenLeft :
    FivefoldP77RawPatchRefinementPlan f g h k
      (.node left₀ right₀) (.node left₁ right₁) :=
  .trans (.right left₀ rightPlan) (.left leftPlan right₁)

/-- Both constructed orders cover each target raw index tuple by exactly
the same original source tuple. No bijectivity of coverage maps is assumed. -/
theorem fivefoldP77RawPatchRefinementOrder_forwardIndex
    (i : FivefoldP77RawPatchTreeIndex f g h k left₁)
    (j : FivefoldP77RawPatchTreeIndex f g h k right₁) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (fivefoldP77RawPatchRefinementLeftThenRight f g h k leftPlan rightPlan)).forwardIndex
        (i, j) =
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k leftPlan).forwardIndex i,
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k rightPlan).forwardIndex j) ∧
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (fivefoldP77RawPatchRefinementRightThenLeft f g h k leftPlan rightPlan)).forwardIndex
        (i, j) =
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k leftPlan).forwardIndex i,
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k rightPlan).forwardIndex j) :=
  ⟨rfl, rfl⟩

/-- The independently retained reverse coverage maps also agree on every
original source tuple; this does not identify their five-cell histories. -/
theorem fivefoldP77RawPatchRefinementOrder_backwardIndex
    (i : FivefoldP77RawPatchTreeIndex f g h k left₀)
    (j : FivefoldP77RawPatchTreeIndex f g h k right₀) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (fivefoldP77RawPatchRefinementLeftThenRight f g h k leftPlan rightPlan)).backwardIndex
        (i, j) =
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k leftPlan).backwardIndex i,
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k rightPlan).backwardIndex j) ∧
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (fivefoldP77RawPatchRefinementRightThenLeft f g h k leftPlan rightPlan)).backwardIndex
        (i, j) =
      ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k leftPlan).backwardIndex i,
        (fivefoldP77RawPatchRefinementPlanRawComparison f g h k rightPlan).backwardIndex j) :=
  ⟨rfl, rfl⟩

/-- An ACTUAL original raw square: the two orders give two chosen GK5CG
five-cell values with the SAME full-tuple raw four-cell endpoints. Their
values remain a pair, not an equality or an assumed higher interchange. -/
def fivefoldP77RawPatchRefinementOrderRawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k left₁)
    (j : FivefoldP77RawPatchTreeIndex f g h k right₁) :
    let Cell := NativeGK5CGConservativeFiveCell first last
      (.trans
        (fivefoldP77RawPatchTreeRaw f g h k left₀
          ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k leftPlan).forwardIndex i))
        (fivefoldP77RawPatchTreeRaw f g h k right₀
          ((fivefoldP77RawPatchRefinementPlanRawComparison f g h k rightPlan).forwardIndex j)))
      (.trans (fivefoldP77RawPatchTreeRaw f g h k left₁ i)
        (fivefoldP77RawPatchTreeRaw f g h k right₁ j))
    Cell × Cell :=
  ⟨(fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (fivefoldP77RawPatchRefinementLeftThenRight f g h k leftPlan rightPlan)).forwardCell (i, j),
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (fivefoldP77RawPatchRefinementRightThenLeft f g h k leftPlan rightPlan)).forwardCell (i, j)⟩

/-- The discrepancy between the two chosen comparison paths is retained
as a genuine raw five-cell loop. Its equality with refl is NOT asserted. -/
def fivefoldP77RawPatchRefinementOrderRawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k left₁)
    (j : FivefoldP77RawPatchTreeIndex f g h k right₁) :
    NativeGK5CGConservativeFiveCell first last
      (.trans (fivefoldP77RawPatchTreeRaw f g h k left₁ i)
        (fivefoldP77RawPatchTreeRaw f g h k right₁ j))
      (.trans (fivefoldP77RawPatchTreeRaw f g h k left₁ i)
        (fivefoldP77RawPatchTreeRaw f g h k right₁ j)) :=
  .trans
    (fivefoldP77RawPatchRefinementOrderRawSquare f g h k leftPlan rightPlan i j).1.symm
    (fivefoldP77RawPatchRefinementOrderRawSquare f g h k leftPlan rightPlan i j).2

/-- The terminal pair reconstructs the SAME exact coarse pair in either
order, before invoking any source-witness subsingleton argument. -/
theorem fivefoldP77RawPatchRefinementOrder_pullback
    (leftFine : FivefoldP77RawPatchTreeWitness f g h k left₁)
    (rightFine : FivefoldP77RawPatchTreeWitness f g h k right₁) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
        (fivefoldP77RawPatchRefinementLeftThenRight f g h k leftPlan rightPlan)
        (leftFine, rightFine) =
      (fivefoldP77RawPatchRefinementPlanPullback f g h k leftPlan leftFine,
        fivefoldP77RawPatchRefinementPlanPullback f g h k rightPlan rightFine) ∧
    fivefoldP77RawPatchRefinementPlanPullback f g h k
        (fivefoldP77RawPatchRefinementRightThenLeft f g h k leftPlan rightPlan)
        (leftFine, rightFine) =
      (fivefoldP77RawPatchRefinementPlanPullback f g h k leftPlan leftFine,
        fivefoldP77RawPatchRefinementPlanPullback f g h k rightPlan rightFine) :=
  ⟨rfl, rfl⟩

/-- Each intermediate corner receives its actual mixed coarse/fine pair.
The unrefined factor is recovered from its own terminal certificate. -/
theorem fivefoldP77RawPatchRefinementOrder_intermediate
    (leftFine : FivefoldP77RawPatchTreeWitness f g h k left₁)
    (rightFine : FivefoldP77RawPatchTreeWitness f g h k right₁) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
        (.right left₁ rightPlan) (leftFine, rightFine) =
      (leftFine, fivefoldP77RawPatchRefinementPlanPullback f g h k rightPlan rightFine) ∧
    fivefoldP77RawPatchRefinementPlanPullback f g h k
        (.left leftPlan right₁) (leftFine, rightFine) =
      (fivefoldP77RawPatchRefinementPlanPullback f g h k leftPlan leftFine, rightFine) :=
  ⟨rfl, rfl⟩

/-- Compilation of the left-first order yields exactly these two original
certified edges. No independently postulated intermediate witness is needed. -/
theorem fivefoldP77RawPatchRefinementLeftThenRight_certify
    (leftFine : FivefoldP77RawPatchTreeWitness f g h k left₁)
    (rightFine : FivefoldP77RawPatchTreeWitness f g h k right₁) :
    fivefoldP77RawPatchRefinementPlanCertify f g h k
        (fivefoldP77RawPatchRefinementLeftThenRight f g h k leftPlan rightPlan)
        (leftFine, rightFine) =
      FivefoldP77RawPatchSubdivisionRoute.trans
        (.left (fivefoldP77RawPatchRefinementPlanCertify f g h k leftPlan leftFine) right₀)
        (.right left₁ (fivefoldP77RawPatchRefinementPlanCertify f g h k rightPlan rightFine)) :=
  rfl

/-- Compilation of the right-first order retains the opposite two-edge
history, while using the SAME chosen local terminal certificates. -/
theorem fivefoldP77RawPatchRefinementRightThenLeft_certify
    (leftFine : FivefoldP77RawPatchTreeWitness f g h k left₁)
    (rightFine : FivefoldP77RawPatchTreeWitness f g h k right₁) :
    fivefoldP77RawPatchRefinementPlanCertify f g h k
        (fivefoldP77RawPatchRefinementRightThenLeft f g h k leftPlan rightPlan)
        (leftFine, rightFine) =
      FivefoldP77RawPatchSubdivisionRoute.trans
        (.right left₀ (fivefoldP77RawPatchRefinementPlanCertify f g h k rightPlan rightFine))
        (.left (fivefoldP77RawPatchRefinementPlanCertify f g h k leftPlan leftFine) right₁) :=
  rfl

end RefinementOrder

#print axioms FivefoldP77RawPatchRefinementPlan
#print axioms fivefoldP77RawPatchRefinementPlanRawComparison
#print axioms fivefoldP77RawPatchRefinementPlanPullback
#print axioms fivefoldP77RawPatchRefinementPlanPullback_path
#print axioms fivefoldP77RawPatchRefinementPlanCertify
#print axioms fivefoldP77RawPatchRefinementPlanCertify_raw
#print axioms fivefoldP77RawPatchRefinementPlanCertify_terminal
#print axioms fivefoldP77RawPatchRefinementPlanRawGlue
#print axioms fivefoldP77RawPatchRefinementPlanPullback_certified
#print axioms fivefoldP77RawPatchRefinementPlan_sourceCompatible
#print axioms fivefoldP77RawPatchRefinementPlanAllCompatible
#print axioms fivefoldP77RawPatchRefinementPlan_allCompatible_iff
#print axioms fivefoldP77RawPatchRefinementPlan_obstructed_iff
#print axioms fivefoldP77RawPatchRefinementPlan_certification_iff
#print axioms fivefoldP77ReverseForwardRefinementPlan
#print axioms fivefoldP77ReverseForwardRefinementPlan_obstructed
#print axioms fivefoldP77RawPatchRefinementLeftThenRight
#print axioms fivefoldP77RawPatchRefinementRightThenLeft
#print axioms fivefoldP77RawPatchRefinementOrder_forwardIndex
#print axioms fivefoldP77RawPatchRefinementOrder_backwardIndex
#print axioms fivefoldP77RawPatchRefinementOrderRawSquare
#print axioms fivefoldP77RawPatchRefinementOrderRawLoop
#print axioms fivefoldP77RawPatchRefinementOrder_pullback
#print axioms fivefoldP77RawPatchRefinementOrder_intermediate
#print axioms fivefoldP77RawPatchRefinementLeftThenRight_certify
#print axioms fivefoldP77RawPatchRefinementRightThenLeft_certify

end
end KUOS.Architecture.WuxingPentagonUnified



