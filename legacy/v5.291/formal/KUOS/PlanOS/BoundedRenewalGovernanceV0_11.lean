import Mathlib
import KUOS.PlanOS.ScopedCapabilityLeaseV0_10

namespace KUOS.PlanOS

structure RenewalCeiling where
  maxRenewals : Nat
  maxAddedUses : Nat
  maxAddedCost : Nat
  absoluteExpiry : Nat
  cooldown : Nat

structure RenewalHistory where
  renewalCount : Nat
  cumulativeAddedUses : Nat
  cumulativeAddedCost : Nat
  lastRenewedAt : Nat

structure RenewalRequest where
  additionalUses : Nat
  additionalCost : Nat
  newExpiry : Nat
  requestedAt : Nat
  ownerMatches : Bool
  epochMatches : Bool
  scopeMatches : Bool
  authorityMatches : Bool
  automaticRenewal : Bool


def boundedRenewalAdmissible
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest) : Prop :=
  history.renewalCount + 1 ≤ ceiling.maxRenewals ∧
  history.cumulativeAddedUses + request.additionalUses ≤ ceiling.maxAddedUses ∧
  history.cumulativeAddedCost + request.additionalCost ≤ ceiling.maxAddedCost ∧
  request.newExpiry ≤ ceiling.absoluteExpiry ∧
  history.lastRenewedAt + ceiling.cooldown ≤ request.requestedAt ∧
  request.ownerMatches = true ∧
  request.epochMatches = true ∧
  request.scopeMatches = true ∧
  request.authorityMatches = true ∧
  request.automaticRenewal = false


theorem admissible_renewal_respects_count_ceiling
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    history.renewalCount + 1 ≤ ceiling.maxRenewals := by
  exact h.1


theorem admissible_renewal_respects_use_ceiling
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    history.cumulativeAddedUses + request.additionalUses ≤
      ceiling.maxAddedUses := by
  exact h.2.1


theorem admissible_renewal_respects_cost_ceiling
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    history.cumulativeAddedCost + request.additionalCost ≤
      ceiling.maxAddedCost := by
  exact h.2.2.1


theorem admissible_renewal_respects_absolute_expiry
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    request.newExpiry ≤ ceiling.absoluteExpiry := by
  exact h.2.2.2.1


theorem admissible_renewal_respects_cooldown
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    history.lastRenewedAt + ceiling.cooldown ≤ request.requestedAt := by
  exact h.2.2.2.2.1


theorem admissible_renewal_revalidates_identity
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    request.ownerMatches = true ∧
    request.epochMatches = true ∧
    request.scopeMatches = true ∧
    request.authorityMatches = true := by
  exact ⟨h.2.2.2.2.2.1,
    h.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.1⟩


theorem admissible_renewal_is_never_automatic
    (ceiling : RenewalCeiling)
    (history : RenewalHistory)
    (request : RenewalRequest)
    (h : boundedRenewalAdmissible ceiling history request) :
    request.automaticRenewal = false := by
  exact h.2.2.2.2.2.2.2.2.2

structure RenewalAuthorityBoundary where
  executionGranted : Bool
  hostAccessGranted : Bool
  approvalGranted : Bool
  memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostAccess : hostAccessGranted = false
  noApproval : approvalGranted = false
  noOverwrite : memoryOverwrite = false


theorem renewal_governor_grants_no_authority
    (boundary : RenewalAuthorityBoundary) :
    boundary.executionGranted = false ∧
    boundary.hostAccessGranted = false ∧
    boundary.approvalGranted = false ∧
    boundary.memoryOverwrite = false := by
  exact ⟨boundary.noExecution, boundary.noHostAccess,
    boundary.noApproval, boundary.noOverwrite⟩

end KUOS.PlanOS
