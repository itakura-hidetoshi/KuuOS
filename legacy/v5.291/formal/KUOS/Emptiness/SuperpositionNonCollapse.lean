/-
KuuOS Emptiness Superposition Non-Collapse v0.2

Minimal public Lean surface for the catuskoti superposition non-collapse layer.

This file is intentionally dependency-light. It is a structural governance spine,
not a claim of completed mathematical, Buddhist, physical, clinical, or execution authority.
-/

namespace KUOS
namespace Emptiness
namespace SuperpositionNonCollapse

inductive CatuskotiBasis where
  | selfOrigin
  | otherOrigin
  | bothOrigin
  | noCauseOrigin
  deriving DecidableEq, Repr

inductive Route where
  | hold
  | review
  | reobserve
  | contextualCollapseWithReceipt
  | truthRelease
  | proofAuthority
  | executionAuthority
  | clinicalAuthority
  | worldAuthority
  deriving DecidableEq, Repr

structure SupportProfile where
  hasSelf : Bool
  hasOther : Bool
  hasBoth : Bool
  hasNoCause : Bool
  deriving Repr

structure CollapseReceipt where
  hasContext : Bool
  hasProjectorOrBasis : Bool
  hasSupportTrace : Bool
  hasScope : Bool
  hasResidualAmplitudes : Bool
  hasNonAuthorityBoundary : Bool
  deriving Repr

def boolToNat (b : Bool) : Nat :=
  if b then 1 else 0

def nonzeroSupportCount (s : SupportProfile) : Nat :=
  boolToNat s.hasSelf +
  boolToNat s.hasOther +
  boolToNat s.hasBoth +
  boolToNat s.hasNoCause

def competingSupport (s : SupportProfile) : Prop :=
  nonzeroSupportCount s >= 2

def completeReceipt (r : CollapseReceipt) : Prop :=
  r.hasContext = true ∧
  r.hasProjectorOrBasis = true ∧
  r.hasSupportTrace = true ∧
  r.hasScope = true ∧
  r.hasResidualAmplitudes = true ∧
  r.hasNonAuthorityBoundary = true

def forbiddenDirectRoute : Route -> Prop
  | Route.truthRelease => True
  | Route.proofAuthority => True
  | Route.executionAuthority => True
  | Route.clinicalAuthority => True
  | Route.worldAuthority => True
  | _ => False

def allowedNonCollapseRoute : Route -> Prop
  | Route.hold => True
  | Route.review => True
  | Route.reobserve => True
  | Route.contextualCollapseWithReceipt => True
  | _ => False

/--
KuuOS governance theorem surface:
when competing catuskoti support is present, forbidden direct authority routes are blocked.
-/
def noncollapseBlocksForbiddenDirectRoute
    (s : SupportProfile) (route : Route) : Prop :=
  competingSupport s -> forbiddenDirectRoute route -> route ≠ Route.truthRelease ∧ route ≠ Route.proofAuthority ∧ route ≠ Route.executionAuthority ∧ route ≠ Route.clinicalAuthority ∧ route ≠ Route.worldAuthority

/--
A contextual collapse can be considered only with a complete receipt.
This is still conventional and does not grant ultimate authority.
-/
def contextualCollapseRequiresReceipt
    (route : Route) (receipt : CollapseReceipt) : Prop :=
  route = Route.contextualCollapseWithReceipt -> completeReceipt receipt

/-- Example support profile with S and O both nonzero. -/
def exampleCompetingSupport : SupportProfile :=
  { hasSelf := true, hasOther := true, hasBoth := false, hasNoCause := false }

/-- Example complete receipt. -/
def exampleCompleteReceipt : CollapseReceipt :=
  { hasContext := true,
    hasProjectorOrBasis := true,
    hasSupportTrace := true,
    hasScope := true,
    hasResidualAmplitudes := true,
    hasNonAuthorityBoundary := true }

/-- Structural theorem: truth release is a forbidden direct route. -/
theorem truth_release_is_forbidden_direct_route :
    forbiddenDirectRoute Route.truthRelease := by
  trivial

/-- Structural theorem: hold is an allowed non-collapse route. -/
theorem hold_is_allowed_noncollapse_route :
    allowedNonCollapseRoute Route.hold := by
  trivial

/-- Structural theorem: the example profile has competing support. -/
theorem example_profile_has_competing_support :
    competingSupport exampleCompetingSupport := by
  unfold competingSupport nonzeroSupportCount exampleCompetingSupport boolToNat
  decide

/-- Structural theorem: contextual collapse route requires complete receipt under the contract. -/
theorem example_contextual_collapse_has_complete_receipt :
    contextualCollapseRequiresReceipt Route.contextualCollapseWithReceipt exampleCompleteReceipt := by
  intro h
  unfold completeReceipt exampleCompleteReceipt
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · rfl
  · rfl

end SuperpositionNonCollapse
end Emptiness
end KUOS
