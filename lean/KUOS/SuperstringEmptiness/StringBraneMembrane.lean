namespace KUOS
namespace SuperstringEmptiness
namespace StringBraneMembrane

/-!
Lean skeleton for Superstring Emptiness String / Brane / Membrane Runtime.

v0.1: base structures and admission predicates.
v0.3: refined collapse predicates and theorem surfaces.

This file is intentionally lightweight and avoids external dependencies.
-/

inductive AdmissionDecision where
  | reject
  | hold
  | admitAsCandidate
  | admitAsConventionalRuntimeSurface
  deriving Repr, DecidableEq

inductive RuntimeClaim where
  | ordinaryCandidate
  | substanceClaim
  | absoluteWorldClaim
  | finalAuthorityClaim
  | graphOnlyIndraNetReduction
  | obstructionErasureClaim
  | directExecutionAuthorityClaim
  | transportEquivalenceClaim
  deriving Repr, DecidableEq

inductive WorldScope where
  | candidateEffectiveSurface
  | conventionalEffectiveSurface
  | localEffectiveWorldSurface
  | absoluteWorld
  deriving Repr, DecidableEq

inductive RollbackOrHoldRoute where
  | hold
  | rollback
  | holdOrRollback
  | finalAuthority
  deriving Repr, DecidableEq

structure EmptinessString where
  stringId : String
  sourceConditionsPresent : Bool
  targetSurfacePresent : Bool
  boundaryConditionsPresent : Bool
  observerRecordSurfacePresent : Bool
  consistencyWitnessesPresent : Bool
  nonReificationGuard : Bool
  twoTruthsGapGuard : Bool
  claim : RuntimeClaim := RuntimeClaim.ordinaryCandidate
  deriving Repr

structure DependentOriginationBrane where
  braneId : String
  worldScopePresent : Bool
  worldScope : WorldScope := WorldScope.candidateEffectiveSurface
  supportingConditionsPresent : Bool
  admissibleStringsPresent : Bool
  recordSurfacePresent : Bool
  scaleRegimePresent : Bool
  qiFlowInterfacePresent : Bool
  indraGaugeInterfacePresent : Bool
  governanceBoundaryPresent : Bool
  claim : RuntimeClaim := RuntimeClaim.ordinaryCandidate
  deriving Repr

structure LayerMembrane where
  membraneId : String
  fromLayerPresent : Bool
  toLayerPresent : Bool
  permeabilityRulePresent : Bool
  obstructionVisibilityRulePresent : Bool
  gluingRulePresent : Bool
  backactionBudgetPresent : Bool
  authorityNonExpansionGuard : Bool
  rollbackOrHoldRoutePresent : Bool
  rollbackOrHoldRoute : RollbackOrHoldRoute := RollbackOrHoldRoute.hold
  claim : RuntimeClaim := RuntimeClaim.ordinaryCandidate
  deriving Repr

structure StringBraneMembranePacket where
  s : EmptinessString
  b : DependentOriginationBrane
  m : LayerMembrane
  dependentOriginationTracePresent : Bool
  obstructionVisibilityPreserved : Bool
  observerRecordScaleBridgePresent : Bool := true
  decision : AdmissionDecision
  claim : RuntimeClaim := RuntimeClaim.ordinaryCandidate
  deriving Repr

def IsConventionalOrCandidateScope (w : WorldScope) : Prop :=
  w = WorldScope.candidateEffectiveSurface ∨
  w = WorldScope.conventionalEffectiveSurface ∨
  w = WorldScope.localEffectiveWorldSurface

def IsSafeRollbackOrHoldRoute (r : RollbackOrHoldRoute) : Prop :=
  r = RollbackOrHoldRoute.hold ∨
  r = RollbackOrHoldRoute.rollback ∨
  r = RollbackOrHoldRoute.holdOrRollback

def NoForbiddenRuntimeClaim (c : RuntimeClaim) : Prop :=
  c ≠ RuntimeClaim.substanceClaim ∧
  c ≠ RuntimeClaim.absoluteWorldClaim ∧
  c ≠ RuntimeClaim.finalAuthorityClaim ∧
  c ≠ RuntimeClaim.graphOnlyIndraNetReduction ∧
  c ≠ RuntimeClaim.obstructionErasureClaim ∧
  c ≠ RuntimeClaim.directExecutionAuthorityClaim ∧
  c ≠ RuntimeClaim.transportEquivalenceClaim

def StringAdmissible (s : EmptinessString) : Prop :=
  s.sourceConditionsPresent = true ∧
  s.targetSurfacePresent = true ∧
  s.boundaryConditionsPresent = true ∧
  s.observerRecordSurfacePresent = true ∧
  s.consistencyWitnessesPresent = true ∧
  s.nonReificationGuard = true ∧
  s.twoTruthsGapGuard = true ∧
  NoForbiddenRuntimeClaim s.claim

def BraneAdmissible (b : DependentOriginationBrane) : Prop :=
  b.worldScopePresent = true ∧
  IsConventionalOrCandidateScope b.worldScope ∧
  b.supportingConditionsPresent = true ∧
  b.admissibleStringsPresent = true ∧
  b.recordSurfacePresent = true ∧
  b.scaleRegimePresent = true ∧
  b.qiFlowInterfacePresent = true ∧
  b.indraGaugeInterfacePresent = true ∧
  b.governanceBoundaryPresent = true ∧
  NoForbiddenRuntimeClaim b.claim

def MembraneAdmissible (m : LayerMembrane) : Prop :=
  m.fromLayerPresent = true ∧
  m.toLayerPresent = true ∧
  m.permeabilityRulePresent = true ∧
  m.obstructionVisibilityRulePresent = true ∧
  m.gluingRulePresent = true ∧
  m.backactionBudgetPresent = true ∧
  m.authorityNonExpansionGuard = true ∧
  m.rollbackOrHoldRoutePresent = true ∧
  IsSafeRollbackOrHoldRoute m.rollbackOrHoldRoute ∧
  NoForbiddenRuntimeClaim m.claim

def PacketAdmissible (p : StringBraneMembranePacket) : Prop :=
  StringAdmissible p.s ∧
  BraneAdmissible p.b ∧
  MembraneAdmissible p.m ∧
  p.dependentOriginationTracePresent = true ∧
  p.obstructionVisibilityPreserved = true ∧
  p.observerRecordScaleBridgePresent = true ∧
  NoForbiddenRuntimeClaim p.claim

/-- Missing string non-reification guard blocks admission. -/
theorem non_reification_required
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.s.nonReificationGuard = true := by
  exact h.1.2.2.2.2.2.1

/-- Missing two-truths gap guard blocks admission. -/
theorem two_truths_gap_required
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.s.twoTruthsGapGuard = true := by
  exact h.1.2.2.2.2.2.2.1

/-- Membrane admission preserves authority non-expansion. -/
theorem membrane_authority_non_expansion_required
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.m.authorityNonExpansionGuard = true := by
  exact h.2.2.1.2.2.2.2.2.1

/-- Packet admission preserves obstruction visibility. -/
theorem obstruction_visibility_required
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.obstructionVisibilityPreserved = true := by
  exact h.2.2.2.2.2.1

/-- Observer-record-scale support is required for packet admission. -/
theorem observer_record_scale_bridge_required
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.observerRecordScaleBridgePresent = true := by
  exact h.2.2.2.2.2.2.1

/-- A string cannot be treated as substance inside this runtime. -/
theorem string_substance_claim_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.s.claim ≠ RuntimeClaim.substanceClaim := by
  exact h.1.2.2.2.2.2.2.2.1

/-- A brane cannot be treated as an absolute world inside this runtime. -/
theorem brane_absolute_world_claim_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.b.claim ≠ RuntimeClaim.absoluteWorldClaim := by
  exact h.2.1.2.2.2.2.2.2.2.2.2.1.2.1

/-- An admissible brane cannot have absolute-world scope. -/
theorem brane_absolute_world_scope_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.b.worldScope ≠ WorldScope.absoluteWorld := by
  intro hw
  have hs : IsConventionalOrCandidateScope p.b.worldScope := h.2.1.2.1
  cases hs with
  | inl h0 => rw [h0] at hw; contradiction
  | inr hs2 =>
    cases hs2 with
    | inl h1 => rw [h1] at hw; contradiction
    | inr h2 => rw [h2] at hw; contradiction

/-- A membrane cannot open final authority inside this runtime. -/
theorem membrane_final_authority_claim_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.m.claim ≠ RuntimeClaim.finalAuthorityClaim := by
  exact h.2.2.1.2.2.2.2.2.2.2.2.1.2.2.1

/-- An admissible membrane cannot use final-authority as its rollback/hold route. -/
theorem membrane_final_authority_route_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.m.rollbackOrHoldRoute ≠ RollbackOrHoldRoute.finalAuthority := by
  intro hr
  have hs : IsSafeRollbackOrHoldRoute p.m.rollbackOrHoldRoute := h.2.2.1.2.2.2.2.2.2.1
  cases hs with
  | inl h0 => rw [h0] at hr; contradiction
  | inr hs2 =>
    cases hs2 with
    | inl h1 => rw [h1] at hr; contradiction
    | inr h2 => rw [h2] at hr; contradiction

/-- Graph-only IndraNet reduction is forbidden. -/
theorem indranet_graph_only_reduction_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.claim ≠ RuntimeClaim.graphOnlyIndraNetReduction := by
  exact h.2.2.2.2.2.2.2.2.2.2.2

/-- Gluing does not erase obstruction visibility in an admissible packet. -/
theorem gluing_obstruction_erasure_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.claim ≠ RuntimeClaim.obstructionErasureClaim := by
  exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.2.1

/-- Direct execution authority is not opened by this physics-facing runtime. -/
theorem direct_execution_authority_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.claim ≠ RuntimeClaim.directExecutionAuthorityClaim := by
  exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.1

/-- Transport success is not an equivalence certificate. -/
theorem transport_equivalence_claim_forbidden
    (p : StringBraneMembranePacket)
    (h : PacketAdmissible p) :
    p.claim ≠ RuntimeClaim.transportEquivalenceClaim := by
  exact h.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2.2

end StringBraneMembrane
end SuperstringEmptiness
end KUOS
