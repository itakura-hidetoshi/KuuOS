import Mathlib
import KUOS.WORLD.KuuOSNonMarkovMemoryConnectionV0_72

/-!
# KuuOS finite memory evaluation v0.73

This layer evaluates a finite family of read-only memory-kernel deformations.
The ordering is deterministic: score, changed-term count, then canonical digest
rank.  The score is an evaluation observable only; no theorem identifies a
lower score with truth.
-/

namespace KUOS.WORLD.KuuOSFiniteMemoryEvaluationV0_73

variable {ι G : Type*}

structure EvaluationData (ι : Type*) where
  score : ι → ℝ
  changedTerms : ι → ℕ
  digestRank : ι → ℕ
  accepted : ι → Prop


def Better (data : EvaluationData ι) (left right : ι) : Prop :=
  data.score left < data.score right ∨
    (data.score left = data.score right ∧
      (data.changedTerms left < data.changedTerms right ∨
        (data.changedTerms left = data.changedTerms right ∧
          data.digestRank left < data.digestRank right)))


structure SelectionCertificate [DecidableEq ι]
    (family : Finset ι)
    (data : EvaluationData ι) where
  selected : ι
  selected_mem : selected ∈ family
  selected_accepted : data.accepted selected
  no_better_accepted :
    ∀ member ∈ family, data.accepted member → ¬ Better data member selected


theorem valid_selection_is_accepted
    [DecidableEq ι]
    (family : Finset ι)
    (data : EvaluationData ι)
    (certificate : SelectionCertificate family data) :
    data.accepted certificate.selected := by
  exact certificate.selected_accepted


theorem valid_selection_has_no_better_accepted_member
    [DecidableEq ι]
    (family : Finset ι)
    (data : EvaluationData ι)
    (certificate : SelectionCertificate family data)
    (member : ι)
    (hMember : member ∈ family)
    (hAccepted : data.accepted member) :
    ¬ Better data member certificate.selected := by
  exact certificate.no_better_accepted member hMember hAccepted


structure SourceRetentionCertificate [DecidableEq ι]
    (family : Finset ι)
    (data : EvaluationData ι) where
  no_accepted_member : ∀ member ∈ family, ¬ data.accepted member


theorem source_retention_is_fail_closed
    [DecidableEq ι]
    (family : Finset ι)
    (data : EvaluationData ι)
    (certificate : SourceRetentionCertificate family data)
    (member : ι)
    (hMember : member ∈ family) :
    ¬ data.accepted member := by
  exact certificate.no_accepted_member member hMember


def GaugeInvariantScore (score : G → ι → ℝ) : Prop :=
  ∀ first second member, score first member = score second member


theorem gauge_invariant_score_preserves_order
    (score : G → ι → ℝ)
    (hInvariant : GaugeInvariantScore score)
    (first second : G)
    (left right : ι) :
    score first left ≤ score first right ↔
      score second left ≤ score second right := by
  rw [hInvariant first second left, hInvariant first second right]


theorem gauge_invariant_score_preserves_strict_order
    (score : G → ι → ℝ)
    (hInvariant : GaugeInvariantScore score)
    (first second : G)
    (left right : ι) :
    score first left < score first right ↔
      score second left < score second right := by
  rw [hInvariant first second left, hInvariant first second right]


structure EvaluationBoundary where
  sourceHistoryUnchanged : Prop
  sourceKernelUnchanged : Prop
  candidateOnly : Prop
  writesDisabled : Prop
  liveApplicationDisabled : Prop
  permissionExpansionDisabled : Prop


structure EvaluationBoundary.Valid (boundary : EvaluationBoundary) : Prop where
  sourceHistoryUnchanged : boundary.sourceHistoryUnchanged
  sourceKernelUnchanged : boundary.sourceKernelUnchanged
  candidateOnly : boundary.candidateOnly
  writesDisabled : boundary.writesDisabled
  liveApplicationDisabled : boundary.liveApplicationDisabled
  permissionExpansionDisabled : boundary.permissionExpansionDisabled


theorem valid_evaluation_boundary_has_no_live_effect
    (boundary : EvaluationBoundary)
    (h : boundary.Valid) :
    boundary.sourceHistoryUnchanged ∧
      boundary.sourceKernelUnchanged ∧
      boundary.candidateOnly ∧
      boundary.writesDisabled ∧
      boundary.liveApplicationDisabled ∧
      boundary.permissionExpansionDisabled := by
  exact ⟨h.sourceHistoryUnchanged, h.sourceKernelUnchanged,
    h.candidateOnly, h.writesDisabled, h.liveApplicationDisabled,
    h.permissionExpansionDisabled⟩

end KUOS.WORLD.KuuOSFiniteMemoryEvaluationV0_73
