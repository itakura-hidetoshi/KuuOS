import Mathlib
import KUOS.OpenHorizon.MemoryOSForgettingAwareAdmissionV0_67

namespace KUOS.OpenHorizon.MemoryOSProvenanceDAGRevocationV0_68

universe u v w x

structure ProvenanceNode
    (Claim : Type u) (Value : Type v) (Source : Type w) (Scope : Type x) where
  nodeId : ℕ
  claim : Claim
  value : Value
  source : Source
  scope : Scope
  version : ℕ
  confidence : ℚ
  valid : Bool
  revoked : Bool
  parentNodeIds : Finset ℕ
deriving DecidableEq

section Provenance

variable {Claim : Type u} {Value : Type v} {Source : Type w} {Scope : Type x}
variable [DecidableEq Claim] [DecidableEq Value] [DecidableEq Source]
variable [DecidableEq Scope]

abbrev Node := ProvenanceNode Claim Value Source Scope


def Conflicts (left right : Node) : Prop :=
  left.claim = right.claim ∧
    left.scope = right.scope ∧
    left.value ≠ right.value


def DependsOn (parent child : Node) : Prop :=
  parent.nodeId ∈ child.parentNodeIds ∧
    parent.version < child.version ∧
    parent.scope = child.scope


inductive ProvenancePrecedes : Node → Node → Prop
  | refl (node : Node) : ProvenancePrecedes node node
  | step {parent child descendant : Node}
      (hdependency : DependsOn parent child)
      (htail : ProvenancePrecedes child descendant) :
      ProvenancePrecedes parent descendant


theorem conflicts_symmetric
    {left right : Node} (h : Conflicts left right) :
    Conflicts right left := by
  exact ⟨h.1.symm, h.2.1.symm, Ne.symm h.2.2⟩


theorem depends_on_version_strict
    {parent child : Node} (h : DependsOn parent child) :
    parent.version < child.version :=
  h.2.1


theorem depends_on_irreflexive (node : Node) :
    ¬ DependsOn node node := by
  intro h
  exact Nat.lt_irrefl node.version h.2.1


theorem provenance_precedes_refl (node : Node) :
    ProvenancePrecedes node node :=
  ProvenancePrecedes.refl node


theorem provenance_precedes_trans :
    ∀ {first second third : Node},
      ProvenancePrecedes first second →
      ProvenancePrecedes second third →
      ProvenancePrecedes first third
  | _, _, _, .refl _, hsecond => hsecond
  | _, _, _, .step hdependency htail, hsecond =>
      .step hdependency (provenance_precedes_trans htail hsecond)


theorem provenance_precedes_eq_or_version_lt :
    ∀ {first second : Node},
      ProvenancePrecedes first second →
      first = second ∨ first.version < second.version
  | _, _, .refl _ => Or.inl rfl
  | _, _, .step hdependency htail => by
      rcases provenance_precedes_eq_or_version_lt htail with heq | hlt
      · subst_vars
        exact Or.inr hdependency.2.1
      · exact Or.inr (lt_trans hdependency.2.1 hlt)


theorem provenance_precedes_antisymm
    {first second : Node}
    (hforward : ProvenancePrecedes first second)
    (hbackward : ProvenancePrecedes second first) :
    first = second := by
  rcases provenance_precedes_eq_or_version_lt hforward with heq | hforwardlt
  · exact heq
  rcases provenance_precedes_eq_or_version_lt hbackward with heq | hbackwardlt
  · subst second
    omega
  · omega


theorem provenance_strict_cycle_impossible
    {first second : Node}
    (hne : first ≠ second) :
    ¬ (ProvenancePrecedes first second ∧
        ProvenancePrecedes second first) := by
  rintro ⟨hforward, hbackward⟩
  exact hne (provenance_precedes_antisymm hforward hbackward)


def RevocationAffected
    (archive : Finset Node) (node : Node) : Prop :=
  ∃ ancestor ∈ archive,
    ancestor.revoked = true ∧
      ProvenancePrecedes ancestor node


def ProvenanceAdmissible
    (archive : Finset Node)
    (queryScope : Scope)
    (matchesQuery : Node → Prop)
    (node : Node) : Prop :=
  node ∈ archive ∧
    node.valid = true ∧
    node.revoked = false ∧
    node.scope = queryScope ∧
    matchesQuery node ∧
    ¬ RevocationAffected archive node


theorem revocation_affected_propagates
    {archive : Finset Node} {upstream downstream : Node}
    (hupstream : RevocationAffected archive upstream)
    (hpath : ProvenancePrecedes upstream downstream) :
    RevocationAffected archive downstream := by
  rcases hupstream with ⟨ancestor, hancestor, hrevoked, hancestorPath⟩
  exact ⟨ancestor, hancestor, hrevoked,
    provenance_precedes_trans hancestorPath hpath⟩


theorem revoked_ancestor_blocks_admission
    {archive : Finset Node}
    {queryScope : Scope} {matchesQuery : Node → Prop}
    {ancestor node : Node}
    (hancestor : ancestor ∈ archive)
    (hrevoked : ancestor.revoked = true)
    (hpath : ProvenancePrecedes ancestor node) :
    ¬ ProvenanceAdmissible archive queryScope matchesQuery node := by
  rintro ⟨_, _, _, _, _, hclear⟩
  exact hclear ⟨ancestor, hancestor, hrevoked, hpath⟩


theorem revoked_parent_blocks_child_admission
    {archive : Finset Node}
    {queryScope : Scope} {matchesQuery : Node → Prop}
    {parent child : Node}
    (hparent : parent ∈ archive)
    (hrevoked : parent.revoked = true)
    (hdependency : DependsOn parent child) :
    ¬ ProvenanceAdmissible archive queryScope matchesQuery child := by
  apply revoked_ancestor_blocks_admission hparent hrevoked
  exact ProvenancePrecedes.step hdependency (ProvenancePrecedes.refl child)


theorem provenance_admissible_not_revocation_affected
    {archive : Finset Node}
    {queryScope : Scope} {matchesQuery : Node → Prop}
    {node : Node}
    (h : ProvenanceAdmissible archive queryScope matchesQuery node) :
    ¬ RevocationAffected archive node :=
  h.2.2.2.2.2


structure SourceEvidence where
  sourceId : ℕ
  weight : ℚ
  confidence : ℚ
deriving DecidableEq


def totalWeight (evidence : Finset SourceEvidence) : ℚ :=
  ∑ item ∈ evidence, item.weight


def weightedConfidenceNumerator
    (evidence : Finset SourceEvidence) : ℚ :=
  ∑ item ∈ evidence, item.weight * item.confidence


def aggregateConfidence (evidence : Finset SourceEvidence) : ℚ :=
  weightedConfidenceNumerator evidence / totalWeight evidence


theorem weighted_confidence_numerator_nonnegative
    (evidence : Finset SourceEvidence)
    (hbounded : ∀ item ∈ evidence,
      0 ≤ item.weight ∧ 0 ≤ item.confidence ∧ item.confidence ≤ 1) :
    0 ≤ weightedConfidenceNumerator evidence := by
  unfold weightedConfidenceNumerator
  apply Finset.sum_nonneg
  intro item hitem
  exact mul_nonneg (hbounded item hitem).1 (hbounded item hitem).2.1


theorem weighted_confidence_numerator_le_total_weight
    (evidence : Finset SourceEvidence)
    (hbounded : ∀ item ∈ evidence,
      0 ≤ item.weight ∧ 0 ≤ item.confidence ∧ item.confidence ≤ 1) :
    weightedConfidenceNumerator evidence ≤ totalWeight evidence := by
  unfold weightedConfidenceNumerator totalWeight
  apply Finset.sum_le_sum
  intro item hitem
  have h := hbounded item hitem
  have hmul := mul_le_mul_of_nonneg_left h.2.2 h.1
  simpa using hmul


theorem aggregate_confidence_nonnegative
    (evidence : Finset SourceEvidence)
    (hbounded : ∀ item ∈ evidence,
      0 ≤ item.weight ∧ 0 ≤ item.confidence ∧ item.confidence ≤ 1)
    (htotal : 0 < totalWeight evidence) :
    0 ≤ aggregateConfidence evidence := by
  unfold aggregateConfidence
  exact div_nonneg
    (weighted_confidence_numerator_nonnegative evidence hbounded)
    (le_of_lt htotal)


theorem aggregate_confidence_le_one
    (evidence : Finset SourceEvidence)
    (hbounded : ∀ item ∈ evidence,
      0 ≤ item.weight ∧ 0 ≤ item.confidence ∧ item.confidence ≤ 1)
    (htotal : 0 < totalWeight evidence) :
    aggregateConfidence evidence ≤ 1 := by
  unfold aggregateConfidence
  apply (div_le_iff₀ htotal).2
  simpa using weighted_confidence_numerator_le_total_weight evidence hbounded


theorem aggregate_confidence_mem_unit_interval
    (evidence : Finset SourceEvidence)
    (hbounded : ∀ item ∈ evidence,
      0 ≤ item.weight ∧ 0 ≤ item.confidence ∧ item.confidence ≤ 1)
    (htotal : 0 < totalWeight evidence) :
    aggregateConfidence evidence ∈ Set.Icc (0 : ℚ) 1 := by
  exact ⟨aggregate_confidence_nonnegative evidence hbounded htotal,
    aggregate_confidence_le_one evidence hbounded htotal⟩


structure ProvenanceDAGRevocationCertificate where
  sourceMemoryOSV067Bound : Bool
  provenanceDAGPartialOrderExact : Bool
  conflictComponentsRetained : Bool
  weightedConfidenceExact : Bool
  revocationPropagationExact : Bool
  revokedDescendantAdmitted : Bool
  cycleAccepted : Bool
  sourceRecordDeletedByRevocation : Bool
  similarityAloneGrantsAdmission : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end Provenance

end KUOS.OpenHorizon.MemoryOSProvenanceDAGRevocationV0_68
