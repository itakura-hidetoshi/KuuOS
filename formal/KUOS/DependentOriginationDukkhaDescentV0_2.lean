import KUOS.DependentOriginationDukkhaResilienceV0_1
import Kuu.LivingEngi.ScopedGluing

namespace KUOS.DependentOriginationDukkhaDescentV0_2

open KUOS.DependentOriginationDukkhaResilienceV0_1
open KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
open KUOS.DependentOriginationGrayC60WuxingFeedbackBalanceV5_169
open KUOS.Architecture
open Kuu.LivingEngi

set_option autoImplicit false
noncomputable section

/-!
# Dukkha resilience v0.2: original-source gluing, not aggregate-score agreement

Reuse the ORIGINAL v0.1 DukkhaResilienceFrame and YinYangProcessBlockerState,
and the ORIGINAL LivingEngi function-sheaf gluing/evidence gate. No old
field, theorem, assumption, source history, or public root is replaced.

Scope: all functions on a specified set cover, with values in ONE common
original-record type. Exact overlap agreement retains context, history,
the entire residual readout, all eight components, signal, and gate.
Differing-context transports, higher-stack effectivity, physical ODE
stability, empirical observability, harm elimination and execution
permission are NOT consequences of this construction. The v0.1 legacy
CoreGovernance import obstruction remains; no bridge to that type is claimed.

The counterexample uses actual v0.1 frames: equal totals, equal zero
quadratic-rate proxies and valid budgets do NOT preserve direct harm,
and therefore cannot certify original-source gluing.
-/

universe u v w y

/-- Labels only: the component values remain projections of the original record. -/
inductive DukkhaComponent
  | harm | attach | collapse | memory | authority | glue | transport | obstruction
  deriving DecidableEq, Repr

def componentValue (r : DukkhaResidual) : DukkhaComponent → WuxingPhase → ℝ
  | .harm => r.harm
  | .attach => r.attach
  | .collapse => r.collapse
  | .memory => r.memory
  | .authority => r.authority
  | .glue => r.glue
  | .transport => r.transport
  | .obstruction => r.obstruction

/-- A product of the two existing types, not a surrogate score or Boolean model. -/
abbrev PatchValue (Context : Type u) (History : Type v) :=
  DukkhaResilienceFrame Context History × YinYangProcessBlockerState

/-- Rate-budget certification and process/capacity certification stay separate. -/
def LocalLicense {Context : Type u} {History : Type v}
    (s : PatchValue Context History) : Prop :=
  s.1.CouplingBudget ∧ s.2.CoupledAdmissible

section Descent

variable {X : Type w} {I : Type y}
variable {Context : Type u} {History : Type v}

/-- Exact agreement with ALL original local values and a scoped license
    at every covered point. No external authority is included. -/
def LicensedGlobal (U : I → Set X)
    (s : LocalSections U (PatchValue Context History)) : Prop :=
  ∃ g : X → PatchValue Context History,
    (∀ (i : I) (x : {z : X // z ∈ U i}), g x.1 = s i x) ∧
    ∀ x : X, LocalLicense (g x)

/-- The original gluing construction transports a local certificate by
    exact equality; no averaging or witness erasure is performed. -/
theorem glued_localLicense
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) (hs : Compatible U s)
    (hl : ∀ i x, LocalLicense (s i x)) (x : X) :
    LocalLicense (glue U s hc hs x) := by
  obtain ⟨i, hi⟩ := hc x
  rw [glue_agrees U s hc hs i ⟨x, hi⟩]
  exact hl i ⟨x, hi⟩

/-- Exact necessary and sufficient conditions within the stated
    function-sheaf scope: compatibility AND all local licenses. -/
theorem licensedGlobal_iff_compatible_and_local
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) :
    LicensedGlobal U s ↔
      Compatible U s ∧ ∀ i x, LocalLicense (s i x) := by
  constructor
  · rintro ⟨g, hg, hl⟩
    refine ⟨global_implies_compatible U s ⟨g, hg⟩, ?_⟩
    intro i x
    have h := hl x.1
    rw [hg i x] at h
    exact h
  · rintro ⟨hs, hl⟩
    refine ⟨glue U s hc hs, ?_, ?_⟩
    · intro i x
      exact glue_agrees U s hc hs i x
    · exact glued_localLicense U s hc hs hl

/-- A global value matching the original locals is unique, not merely
    unique after observation or after taking a total suffering score. -/
theorem source_global_unique
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) {g₁ g₂ : X → PatchValue Context History}
    (h₁ : ∀ i x, g₁ x.1 = s i x)
    (h₂ : ∀ i x, g₂ x.1 = s i x) : g₁ = g₂ :=
  global_unique U s hc h₁ h₂

/-- Each of the eight original components is preserved, at every phase
    and on every local chart, including direct harm. -/
theorem glued_component_eq
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) (hs : Compatible U s)
    (i : I) (x : {z : X // z ∈ U i})
    (k : DukkhaComponent) (p : WuxingPhase) :
    componentValue (glue U s hc hs x.1).1.residual k p =
      componentValue (s i x).1.residual k p :=
  congrArg (fun a : PatchValue Context History => componentValue a.1.residual k p)
    (glue_agrees U s hc hs i x)

/-- Context, Type-valued history, the whole residual function and signal
    are retained, rather than reconstructed from an aggregate. -/
theorem glued_provenance_eq
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) (hs : Compatible U s)
    (i : I) (x : {z : X // z ∈ U i}) :
    (glue U s hc hs x.1).1.context = (s i x).1.context ∧
    (glue U s hc hs x.1).1.history = (s i x).1.history ∧
    (glue U s hc hs x.1).1.residualOf = (s i x).1.residualOf ∧
    (glue U s hc hs x.1).1.signal = (s i x).1.signal := by
  have h := glue_agrees U s hc hs i x
  exact ⟨congrArg (fun a : PatchValue Context History => a.1.context) h,
    congrArg (fun a : PatchValue Context History => a.1.history) h,
    congrArg (fun a : PatchValue Context History => a.1.residualOf) h,
    congrArg (fun a : PatchValue Context History => a.1.signal) h⟩

/-- The scoped v0.1 rate budget transfers pointwise after exact descent. -/
theorem glued_quadraticRate_nonpositive
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) (hs : Compatible U s)
    (hl : ∀ i x, LocalLicense (s i x)) (x : X) :
    (glue U s hc hs x).1.quadraticRate ≤ 0 :=
  (glue U s hc hs x).1.quadraticRate_nonpositive_of_budget
    (glued_localLicense U s hc hs hl x).1

/-- A nonnegative weighted finite sum of the certified pointwise proxies
    is nonpositive. The converse and harm removal are not asserted. -/
theorem glued_weighted_rate_nonpositive
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) (hs : Compatible U s)
    (hl : ∀ i x, LocalLicense (s i x))
    (T : Finset X) (weight : X → ℝ)
    (hw : ∀ x ∈ T, 0 ≤ weight x) :
    (∑ x ∈ T, weight x * (glue U s hc hs x).1.quadraticRate) ≤ 0 := by
  apply Finset.sum_nonpos
  intro x hx
  exact mul_nonpos_of_nonneg_of_nonpos (hw x hx)
    (glued_quadraticRate_nonpositive U s hc hs hl x)

/-- The original Yin/Yang gate and both visibility fields survive descent;
    mathematical descent confers neither truth nor execution authority. -/
theorem glued_yinyang_and_visibility
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (hc : Covers U) (hs : Compatible U s)
    (hl : ∀ i x, LocalLicense (s i x)) (x : X) :
    (glue U s hc hs x).2.effectiveQi = (glue U s hc hs x).2.qiIntensity ∧
    (glue U s hc hs x).2.grantsExecution = false ∧
    (glue U s hc hs x).2.grantsTruth = false ∧
    (glue U s hc hs x).1.dukkhaVisible = true ∧
    (glue U s hc hs x).1.harmVisible = true := by
  have hlx := glued_localLicense U s hc hs hl x
  exact ⟨(glue U s hc hs x).2.effectiveQi_eq_of_admissible hlx.2,
    (glue U s hc hs x).2.no_execution_authority,
    (glue U s hc hs x).2.no_truth_authority,
    (glue U s hc hs x).1.dukkhaVisibilityCertified,
    (glue U s hc hs x).1.harmVisibilityCertified⟩

/-- A mismatch in even one original component obstructs source gluing. -/
theorem component_disagreement_blocks_global
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (i j : I) (x : X) (hi : x ∈ U i) (hj : x ∈ U j)
    (k : DukkhaComponent) (p : WuxingPhase)
    (hne : componentValue (s i ⟨x, hi⟩).1.residual k p ≠
      componentValue (s j ⟨x, hj⟩).1.residual k p) :
    ¬ HasGlobal U s := by
  apply no_global_of_disagreement U s i j x hi hj
  intro heq
  exact hne (congrArg
    (fun a : PatchValue Context History => componentValue a.1.residual k p) heq)

/-- The original three-state evidence gate rejects the refuted source
    promotion. No proof of nonexistence is inferred from mere uncertainty. -/
theorem component_disagreement_blocks_promotion
    (U : I → Set X) (s : LocalSections U (PatchValue Context History))
    (i j : I) (x : X) (hi : x ∈ U i) (hj : x ∈ U j)
    (k : DukkhaComponent) (p : WuxingPhase)
    (hne : componentValue (s i ⟨x, hi⟩).1.residual k p ≠
      componentValue (s j ⟨x, hj⟩).1.residual k p)
    (e : PromotionEvidence (HasGlobal U s)) : ¬ Admissible e := by
  intro he
  exact component_disagreement_blocks_global U s i j x hi hj k p hne
    (admitted_sound e he)

end Descent

/-! ## Concrete original-frame obstruction: equal total is not equal harm. -/

/-- Same total residual as the original positiveHarmAtRest, but assigned
    to attachment rather than direct harm. This is a DIFFERENT source,
    not a proposed repair or a relabeling licensed by this module. -/
def attachmentAtRest : DukkhaResilienceFrame Unit Unit where
  context := ()
  history := ()
  signal := fun _ => 0
  residualOf := fun _ _ =>
    { harm := fun _ => 0
      attach := positiveHarmAtRest.residual.harm
      collapse := fun _ => 0
      memory := fun _ => 0
      authority := fun _ => 0
      glue := fun _ => 0
      transport := fun _ => 0
      obstruction := fun _ => 0 }
  residualNonnegative := by
    intro p
    cases p <;> norm_num [DukkhaResidual.Nonnegative,
      DukkhaResilienceFrame.residual, positiveHarmAtRest, positiveHarmFrame]
  dukkhaVisible := true
  harmVisible := true
  dukkhaVisibilityCertified := rfl
  harmVisibilityCertified := rfl

theorem rest_frames_same_total (p : WuxingPhase) :
    positiveHarmAtRest.internalPressure p = attachmentAtRest.internalPressure p := by
  cases p <;> norm_num [DukkhaResilienceFrame.internalPressure,
    DukkhaResilienceFrame.residual, DukkhaResidual.totalAt,
    positiveHarmAtRest, positiveHarmFrame, attachmentAtRest]

theorem attachmentAtRest_rate_zero : attachmentAtRest.quadraticRate = 0 := by
  norm_num [DukkhaResilienceFrame.quadraticRate,
    DukkhaResilienceFrame.sufferingCoupling, attachmentAtRest,
    wuxingQuadraticWork, wuxingSquaredMass, wuxingSignedFeedback]

/-- Both original frames satisfy the algebraic budget despite disagreeing on harm. -/
theorem rest_frames_both_budgets :
    positiveHarmAtRest.CouplingBudget ∧ attachmentAtRest.CouplingBudget := by
  exact ⟨(positiveHarmAtRest.couplingBudget_iff_quadraticRate_nonpositive).mpr
      (le_of_eq positiveHarmAtRest_quadraticRate_zero),
    (attachmentAtRest.couplingBudget_iff_quadraticRate_nonpositive).mpr
      (le_of_eq attachmentAtRest_rate_zero)⟩

theorem rest_frames_harm_distinct :
    positiveHarmAtRest.residual.harm ≠ attachmentAtRest.residual.harm := by
  intro h
  have hwood := congrFun h WuxingPhase.wood
  change (3 : ℝ) = 0 at hwood
  norm_num at hwood

theorem rest_frames_distinct : positiveHarmAtRest ≠ attachmentAtRest := by
  intro h
  exact rest_frames_harm_distinct
    (congrArg (fun s : DukkhaResilienceFrame Unit Unit => s.residual.harm) h)

/-- Direct harm cannot be reconstructed as a function of total pressure
    on all original frames: an explicit fiber collision prevents descent. -/
theorem harm_does_not_factor_through_total :
    ¬ Factors
      (fun s : DukkhaResilienceFrame Unit Unit => s.internalPressure)
      (fun s : DukkhaResilienceFrame Unit Unit => s.residual.harm) :=
  no_factor_of_collision
    (fun s : DukkhaResilienceFrame Unit Unit => s.internalPressure)
    (fun s : DukkhaResilienceFrame Unit Unit => s.residual.harm)
    positiveHarmAtRest attachmentAtRest
    (funext rest_frames_same_total) rest_frames_harm_distinct

def overlapCover : Bool → Set Unit := fun _ => Set.univ

def overlapFrames : LocalSections overlapCover (DukkhaResilienceFrame Unit Unit) :=
  fun i _ => match i with
    | false => positiveHarmAtRest
    | true => attachmentAtRest

def overlapTotals : LocalSections overlapCover (WuxingPhase → ℝ) :=
  fun i x => (overlapFrames i x).internalPressure

theorem overlapCover_covers : Covers overlapCover := by
  intro x
  exact ⟨false, Set.mem_univ x⟩

theorem overlapTotals_compatible : Compatible overlapCover overlapTotals := by
  intro i j x hi hj
  cases i <;> cases j
  · rfl
  · exact funext rest_frames_same_total
  · exact (funext rest_frames_same_total).symm
  · rfl

/-- Total observations really do glue on this genuine two-chart cover. -/
theorem overlapTotals_haveGlobal : HasGlobal overlapCover overlapTotals :=
  (compatible_iff_hasGlobal overlapCover overlapTotals overlapCover_covers).mp
    overlapTotals_compatible

/-- Yet the ORIGINAL frame-valued sections have no global extension. -/
theorem overlapFrames_noGlobal : ¬ HasGlobal overlapCover overlapFrames :=
  no_global_of_disagreement overlapCover overlapFrames false true ()
    (Set.mem_univ ()) (Set.mem_univ ()) rest_frames_distinct

theorem overlapFrames_all_budgets : ∀ i x, (overlapFrames i x).CouplingBudget := by
  intro i x
  cases i with
  | false => exact rest_frames_both_budgets.1
  | true => exact rest_frames_both_budgets.2

/-- Even an actual admissible common gate does not repair source mismatch. -/
def overlapStates (gate : YinYangProcessBlockerState) :
    LocalSections overlapCover (PatchValue Unit Unit) :=
  fun i x => (overlapFrames i x, gate)

theorem overlapStates_all_licensed (gate : YinYangProcessBlockerState)
    (hg : gate.CoupledAdmissible) :
    ∀ i x, LocalLicense (overlapStates gate i x) := by
  intro i x
  exact ⟨overlapFrames_all_budgets i x, hg⟩

theorem overlapStates_noGlobal (gate : YinYangProcessBlockerState) :
    ¬ HasGlobal overlapCover (overlapStates gate) := by
  apply no_global_of_disagreement overlapCover (overlapStates gate)
    false true () (Set.mem_univ ()) (Set.mem_univ ())
  intro h
  exact rest_frames_distinct (congrArg Prod.fst h)

theorem overlapStates_noPromotion (gate : YinYangProcessBlockerState)
    (e : PromotionEvidence (HasGlobal overlapCover (overlapStates gate))) :
    ¬ Admissible e := by
  intro he
  exact overlapStates_noGlobal gate (admitted_sound e he)

#print axioms glued_localLicense
#print axioms licensedGlobal_iff_compatible_and_local
#print axioms source_global_unique
#print axioms glued_component_eq
#print axioms glued_provenance_eq
#print axioms glued_quadraticRate_nonpositive
#print axioms glued_weighted_rate_nonpositive
#print axioms glued_yinyang_and_visibility
#print axioms component_disagreement_blocks_global
#print axioms component_disagreement_blocks_promotion
#print axioms rest_frames_same_total
#print axioms attachmentAtRest_rate_zero
#print axioms rest_frames_both_budgets
#print axioms rest_frames_harm_distinct
#print axioms rest_frames_distinct
#print axioms harm_does_not_factor_through_total
#print axioms overlapCover_covers
#print axioms overlapTotals_compatible
#print axioms overlapTotals_haveGlobal
#print axioms overlapFrames_noGlobal
#print axioms overlapFrames_all_budgets
#print axioms overlapStates_all_licensed
#print axioms overlapStates_noGlobal
#print axioms overlapStates_noPromotion

end
end KUOS.DependentOriginationDukkhaDescentV0_2
