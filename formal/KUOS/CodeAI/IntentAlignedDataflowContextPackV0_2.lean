import Mathlib

namespace KUOS.CodeAI.IntentAlignedDataflowContextPackV0_2

inductive QueryStage where
  | intent
  | hypothesis
  | symbol
  | dependency
  | dataflow
  deriving DecidableEq

structure QueryNode where
  stage : QueryStage
  parentCount : Nat
  termCount : Nat
  deriving DecidableEq

/-- The first query is the intent root and every expansion is parent-grounded. -/
def LineageGrounded : List QueryNode → Prop
  | [] => False
  | first :: rest =>
      first.stage = .intent ∧
      first.parentCount = 0 ∧
      0 < first.termCount ∧
      ∀ node ∈ rest,
        node.stage ≠ .intent ∧
        0 < node.parentCount ∧
        0 < node.termCount

instance instDecidableLineageGrounded (nodes : List QueryNode) :
    Decidable (LineageGrounded nodes) := by
  cases nodes <;> unfold LineageGrounded <;> infer_instance

theorem lineage_root_is_intent
    {first : QueryNode}
    {rest : List QueryNode}
    (h : LineageGrounded (first :: rest)) :
    first.stage = .intent := by
  exact h.1

theorem lineage_expansion_has_parent
    {first node : QueryNode}
    {rest : List QueryNode}
    (h : LineageGrounded (first :: rest))
    (hMember : node ∈ rest) :
    0 < node.parentCount := by
  exact (h.2.2.2 node hMember).2.1

structure EvidenceItem where
  intentEvidenceScore : Nat
  excerptBytes : Nat
  hasSymbolDigest : Bool
  hasDependencyPath : Bool
  deriving DecidableEq

/-- Every selected file carries positive intent evidence and retrieval provenance. -/
def EvidenceGrounded (item : EvidenceItem) : Prop :=
  0 < item.intentEvidenceScore ∧
  item.hasSymbolDigest = true ∧
  item.hasDependencyPath = true

instance instDecidableEvidenceGrounded (item : EvidenceItem) :
    Decidable (EvidenceGrounded item) := by
  unfold EvidenceGrounded
  infer_instance

/-- File-count and total-context byte budgets are preserved. -/
def PackBounded
    (maximumFiles maximumBytes : Nat)
    (items : List EvidenceItem) : Prop :=
  items.length ≤ maximumFiles ∧
  (items.map EvidenceItem.excerptBytes).sum ≤ maximumBytes

instance instDecidablePackBounded
    (maximumFiles maximumBytes : Nat)
    (items : List EvidenceItem) :
    Decidable (PackBounded maximumFiles maximumBytes items) := by
  unfold PackBounded
  infer_instance

def AllEvidenceGrounded (items : List EvidenceItem) : Prop :=
  ∀ item ∈ items, EvidenceGrounded item

instance instDecidableAllEvidenceGrounded (items : List EvidenceItem) :
    Decidable (AllEvidenceGrounded items) := by
  unfold AllEvidenceGrounded
  infer_instance

theorem selected_file_count_bounded
    {maximumFiles maximumBytes : Nat}
    {items : List EvidenceItem}
    (h : PackBounded maximumFiles maximumBytes items) :
    items.length ≤ maximumFiles := by
  exact h.1

theorem selected_context_bytes_bounded
    {maximumFiles maximumBytes : Nat}
    {items : List EvidenceItem}
    (h : PackBounded maximumFiles maximumBytes items) :
    (items.map EvidenceItem.excerptBytes).sum ≤ maximumBytes := by
  exact h.2

theorem selected_evidence_has_provenance
    {items : List EvidenceItem}
    {item : EvidenceItem}
    (h : AllEvidenceGrounded items)
    (hMember : item ∈ items) :
    item.hasSymbolDigest = true ∧ item.hasDependencyPath = true := by
  exact (h item hMember).2

structure Boundary where
  repositoryMutationPerformed : Bool
  networkAccessPerformed : Bool
  secretMaterialRead : Bool
  candidateSelectionAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  gitEffectPerformed : Bool
  correctnessClaimed : Bool
  completenessClaimed : Bool
  representativenessClaimed : Bool
  deriving DecidableEq

/-- Retrieval remains read-only and makes no correctness or coverage overclaim. -/
def BoundaryPreserved (boundary : Boundary) : Prop :=
  boundary.repositoryMutationPerformed = false ∧
  boundary.networkAccessPerformed = false ∧
  boundary.secretMaterialRead = false ∧
  boundary.candidateSelectionAuthorityGranted = false ∧
  boundary.executionAuthorityGranted = false ∧
  boundary.gitEffectPerformed = false ∧
  boundary.correctnessClaimed = false ∧
  boundary.completenessClaimed = false ∧
  boundary.representativenessClaimed = false

instance instDecidableBoundaryPreserved (boundary : Boundary) :
    Decidable (BoundaryPreserved boundary) := by
  unfold BoundaryPreserved
  infer_instance

/-! ### Actual reference intent-aligned dataflow context pack -/

def actualQueryLineage : List QueryNode :=
  [ { stage := .intent, parentCount := 0, termCount := 4 },
    { stage := .hypothesis, parentCount := 1, termCount := 3 },
    { stage := .hypothesis, parentCount := 1, termCount := 3 },
    { stage := .symbol, parentCount := 2, termCount := 8 },
    { stage := .dependency, parentCount := 1, termCount := 14 },
    { stage := .dataflow, parentCount := 1, termCount := 12 } ]

def actualEvidence : List EvidenceItem :=
  [ { intentEvidenceScore := 43, excerptBytes := 283,
      hasSymbolDigest := true, hasDependencyPath := true },
    { intentEvidenceScore := 34, excerptBytes := 247,
      hasSymbolDigest := true, hasDependencyPath := true },
    { intentEvidenceScore := 32, excerptBytes := 374,
      hasSymbolDigest := true, hasDependencyPath := true },
    { intentEvidenceScore := 26, excerptBytes := 250,
      hasSymbolDigest := true, hasDependencyPath := true },
    { intentEvidenceScore := 22, excerptBytes := 260,
      hasSymbolDigest := true, hasDependencyPath := true },
    { intentEvidenceScore := 24, excerptBytes := 125,
      hasSymbolDigest := true, hasDependencyPath := true } ]

def actualBoundary : Boundary :=
  { repositoryMutationPerformed := false,
    networkAccessPerformed := false,
    secretMaterialRead := false,
    candidateSelectionAuthorityGranted := false,
    executionAuthorityGranted := false,
    gitEffectPerformed := false,
    correctnessClaimed := false,
    completenessClaimed := false,
    representativenessClaimed := false }

theorem actual_query_lineage_grounded :
    LineageGrounded actualQueryLineage := by
  native_decide

theorem actual_pack_bounded :
    PackBounded 6 16384 actualEvidence := by
  native_decide

theorem actual_evidence_grounded :
    AllEvidenceGrounded actualEvidence := by
  native_decide

theorem actual_boundary_preserved :
    BoundaryPreserved actualBoundary := by
  native_decide

end KUOS.CodeAI.IntentAlignedDataflowContextPackV0_2
