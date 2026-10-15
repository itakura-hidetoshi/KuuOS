import Mathlib
import KUOS.OpenHorizon.MemoryOSContinuousLogMGFConvexityV0_66

namespace KUOS.OpenHorizon.MemoryOSForgettingAwareAdmissionV0_67

universe u v w

structure MemoryRecord (Key : Type u) (Value : Type v) (Scope : Type w) where
  key : Key
  value : Value
  scope : Scope
  version : ℕ
  valid : Bool
deriving DecidableEq

section Admission

variable {Key : Type u} {Value : Type v} {Scope : Type w}
variable [DecidableEq Key] [DecidableEq Value] [DecidableEq Scope]


def Contradicts
    (older newer : MemoryRecord Key Value Scope) : Prop :=
  older.key = newer.key ∧ older.value ≠ newer.value


def Supersedes
    (older newer : MemoryRecord Key Value Scope) : Prop :=
  Contradicts older newer ∧
    older.version < newer.version ∧
    newer.valid = true


def Effective
    (archive : Finset (MemoryRecord Key Value Scope))
    (record : MemoryRecord Key Value Scope) : Prop :=
  record ∈ archive ∧
    record.valid = true ∧
    ¬ ∃ newer ∈ archive, Supersedes record newer


def QueryAdmissible
    (archive : Finset (MemoryRecord Key Value Scope))
    (queryScope : Scope)
    (matchesQuery : MemoryRecord Key Value Scope → Prop)
    (record : MemoryRecord Key Value Scope) : Prop :=
  Effective archive record ∧
    record.scope = queryScope ∧
    matchesQuery record


def appendRecord
    (archive : Finset (MemoryRecord Key Value Scope))
    (record : MemoryRecord Key Value Scope) :
    Finset (MemoryRecord Key Value Scope) :=
  insert record archive


theorem query_admissible_mem_archive
    {archive : Finset (MemoryRecord Key Value Scope)}
    {queryScope : Scope}
    {matchesQuery : MemoryRecord Key Value Scope → Prop}
    {record : MemoryRecord Key Value Scope}
    (h : QueryAdmissible archive queryScope matchesQuery record) :
    record ∈ archive :=
  h.1.1


theorem query_admissible_valid
    {archive : Finset (MemoryRecord Key Value Scope)}
    {queryScope : Scope}
    {matchesQuery : MemoryRecord Key Value Scope → Prop}
    {record : MemoryRecord Key Value Scope}
    (h : QueryAdmissible archive queryScope matchesQuery record) :
    record.valid = true :=
  h.1.2.1


theorem query_admissible_scope_exact
    {archive : Finset (MemoryRecord Key Value Scope)}
    {queryScope : Scope}
    {matchesQuery : MemoryRecord Key Value Scope → Prop}
    {record : MemoryRecord Key Value Scope}
    (h : QueryAdmissible archive queryScope matchesQuery record) :
    record.scope = queryScope :=
  h.2.1


theorem query_admissible_matches_query
    {archive : Finset (MemoryRecord Key Value Scope)}
    {queryScope : Scope}
    {matchesQuery : MemoryRecord Key Value Scope → Prop}
    {record : MemoryRecord Key Value Scope}
    (h : QueryAdmissible archive queryScope matchesQuery record) :
    matchesQuery record :=
  h.2.2


theorem query_admissible_has_no_superseder
    {archive : Finset (MemoryRecord Key Value Scope)}
    {queryScope : Scope}
    {matchesQuery : MemoryRecord Key Value Scope → Prop}
    {record : MemoryRecord Key Value Scope}
    (h : QueryAdmissible archive queryScope matchesQuery record) :
    ¬ ∃ newer ∈ archive, Supersedes record newer :=
  h.1.2.2


theorem superseded_not_effective
    {archive : Finset (MemoryRecord Key Value Scope)}
    {record newer : MemoryRecord Key Value Scope}
    (hrecord : record ∈ archive)
    (hnewer : newer ∈ archive)
    (hsupersedes : Supersedes record newer) :
    ¬ Effective archive record := by
  intro heffective
  exact heffective.2.2 ⟨newer, hnewer, hsupersedes⟩


theorem superseded_not_query_admissible
    {archive : Finset (MemoryRecord Key Value Scope)}
    {queryScope : Scope}
    {matchesQuery : MemoryRecord Key Value Scope → Prop}
    {record newer : MemoryRecord Key Value Scope}
    (hrecord : record ∈ archive)
    (hnewer : newer ∈ archive)
    (hsupersedes : Supersedes record newer) :
    ¬ QueryAdmissible archive queryScope matchesQuery record := by
  intro hadmissible
  exact superseded_not_effective hrecord hnewer hsupersedes hadmissible.1


theorem append_record_retains_prior
    {archive : Finset (MemoryRecord Key Value Scope)}
    {record newRecord : MemoryRecord Key Value Scope}
    (hrecord : record ∈ archive) :
    record ∈ appendRecord archive newRecord := by
  exact Finset.mem_insert_of_mem hrecord


theorem append_preserves_effective_of_not_superseded
    {archive : Finset (MemoryRecord Key Value Scope)}
    {record newRecord : MemoryRecord Key Value Scope}
    (heffective : Effective archive record)
    (hnot : ¬ Supersedes record newRecord) :
    Effective (appendRecord archive newRecord) record := by
  refine ⟨append_record_retains_prior heffective.1, heffective.2.1, ?_⟩
  rintro ⟨candidate, hcandidate, hsupersedes⟩
  rw [appendRecord] at hcandidate
  rcases Finset.mem_insert.mp hcandidate with heq | hold
  · subst candidate
    exact hnot hsupersedes
  · exact heffective.2.2 ⟨candidate, hold, hsupersedes⟩


theorem append_superseder_invalidates
    {archive : Finset (MemoryRecord Key Value Scope)}
    {record newRecord : MemoryRecord Key Value Scope}
    (hrecord : record ∈ archive)
    (hsupersedes : Supersedes record newRecord) :
    ¬ Effective (appendRecord archive newRecord) record := by
  apply superseded_not_effective
    (archive := appendRecord archive newRecord)
    (record := record)
    (newer := newRecord)
  · exact append_record_retains_prior hrecord
  · simp [appendRecord]
  · exact hsupersedes


structure FreshestAdmissible
    (archive : Finset (MemoryRecord Key Value Scope))
    (queryScope : Scope)
    (matchesQuery : MemoryRecord Key Value Scope → Prop) where
  record : MemoryRecord Key Value Scope
  admissible : QueryAdmissible archive queryScope matchesQuery record
  maximal :
    ∀ candidate,
      QueryAdmissible archive queryScope matchesQuery candidate →
      candidate.version ≤ record.version


theorem freshest_admissible_exists
    (archive : Finset (MemoryRecord Key Value Scope))
    (queryScope : Scope)
    (matchesQuery : MemoryRecord Key Value Scope → Prop)
    (hnonempty : ∃ record, QueryAdmissible archive queryScope matchesQuery record) :
    Nonempty (FreshestAdmissible archive queryScope matchesQuery) := by
  classical
  let candidates : Finset (MemoryRecord Key Value Scope) :=
    archive.filter (fun record =>
      QueryAdmissible archive queryScope matchesQuery record)
  have hcandidates : candidates.Nonempty := by
    rcases hnonempty with ⟨record, hadmissible⟩
    refine ⟨record, Finset.mem_filter.mpr ?_⟩
    exact ⟨hadmissible.1.1, hadmissible⟩
  let versions : Finset ℕ :=
    candidates.image (fun record => record.version)
  have hversions : versions.Nonempty := by
    rcases hcandidates with ⟨record, hrecord⟩
    refine ⟨record.version, Finset.mem_image.mpr ?_⟩
    exact ⟨record, hrecord, rfl⟩
  have hmaxmem : versions.max' hversions ∈ versions :=
    Finset.max'_mem versions hversions
  rcases Finset.mem_image.mp hmaxmem with
    ⟨record, hrecord, hrecordVersion⟩
  refine ⟨{
    record := record
    admissible := (Finset.mem_filter.mp hrecord).2
    maximal := ?_
  }⟩
  intro candidate hadmissible
  have hcandidate : candidate ∈ candidates :=
    Finset.mem_filter.mpr ⟨hadmissible.1.1, hadmissible⟩
  have hcandidateVersion : candidate.version ∈ versions :=
    Finset.mem_image.mpr ⟨candidate, hcandidate, rfl⟩
  have hle : candidate.version ≤ versions.max' hversions :=
    Finset.le_max' versions _ hcandidateVersion
  exact hle.trans_eq hrecordVersion.symm


def forgettingAwareLoss
    (recallError obsoleteReusePenalty : ℚ) : ℚ :=
  recallError + obsoleteReusePenalty


theorem forgetting_aware_loss_nonnegative
    {recallError obsoleteReusePenalty : ℚ}
    (hrecall : 0 ≤ recallError)
    (hobsolete : 0 ≤ obsoleteReusePenalty) :
    0 ≤ forgettingAwareLoss recallError obsoleteReusePenalty := by
  unfold forgettingAwareLoss
  exact add_nonneg hrecall hobsolete


theorem forgetting_aware_loss_eq_recall_without_obsolete_reuse
    (recallError : ℚ) :
    forgettingAwareLoss recallError 0 = recallError := by
  simp [forgettingAwareLoss]


theorem forgetting_aware_loss_strictly_increases_with_obsolete_reuse
    (recallError obsoleteReusePenalty : ℚ)
    (hobsolete : 0 < obsoleteReusePenalty) :
    recallError < forgettingAwareLoss recallError obsoleteReusePenalty := by
  unfold forgettingAwareLoss
  linarith


structure ForgettingAwareAdmissionCertificate where
  sourceMemoryOSV066Bound : Bool
  appendOnlyArchiveExact : Bool
  supersessionExcludesObsolete : Bool
  queryConditionedAdmissionExact : Bool
  freshestAdmissibleExists : Bool
  forgettingAwareLossExact : Bool
  provenanceDigestBound : Bool
  obsoleteMemoryAdmitted : Bool
  crossScopeLeakageAllowed : Bool
  similarityAloneGrantsAdmission : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool


theorem certificate_grants_no_authority
    (certificate : ForgettingAwareAdmissionCertificate)
    (hranking : certificate.candidateRankingPerformed = false)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hranking, hpruning, hselection, hcommit, hactivation,
    hexecution, hworld, hverification, htruth⟩

end Admission

end KUOS.OpenHorizon.MemoryOSForgettingAwareAdmissionV0_67
