import Mathlib
import KUOS.WORLD.PetzRecoverySufficiencyBridgeV0_35

/-!
Kū–Indra WORLD conditional-expectation, sufficient-subalgebra, and Takesaki
invariance bridge v0.36.

Lean directly verifies the algebraic projection content of a state-pair
preserving conditional expectation onto a sufficient subalgebra: range
containment, pointwise fixation, idempotence, fixed-point/range
characterizations, bimodule laws, compatibility with the v0.35 Petz recovered
channel, and modular invariance of the subalgebra. Normal complete positivity,
the analytic Takesaki equivalence, and uniqueness remain external receipts.
-/

namespace KUOS
namespace WORLD

structure WorldConditionalExpectationTakesakiBridge
    {C : RealHilbertL2Carrier}
    {W : WorldNoncommutativeOperatorAlgebra C}
    [PartialOrder W.Region]
    {B : WorldCStarLocalNetBridge C W}
    {V : WorldVonNeumannBicommutantBridge B}
    {M : WorldStandardFormModularFlowBridge V}
    {R : WorldModularStateKMSRelativeFlowBridge M}
    {E : WorldArakiRelativeEntropyBridge R}
    (P : WorldPetzRecoverySufficiencyBridge E) where
  sufficientSubalgebra : Subalgebra ℂ B.A
  sufficientSubalgebra_star_closed : ∀ {a : B.A},
    a ∈ sufficientSubalgebra → star a ∈ sufficientSubalgebra
  conditionalExpectation : B.A →ₗ[ℂ] B.A
  conditionalExpectation_one : conditionalExpectation 1 = 1
  maps_into_sufficientSubalgebra : ∀ a,
    conditionalExpectation a ∈ sufficientSubalgebra
  fixes_sufficientSubalgebra : ∀ {a : B.A},
    a ∈ sufficientSubalgebra → conditionalExpectation a = a
  conditionalExpectation_star : ∀ a,
    conditionalExpectation (star a) = star (conditionalExpectation a)
  left_bimodule : ∀ {b : B.A},
    b ∈ sufficientSubalgebra → ∀ a,
      conditionalExpectation (b * a) = b * conditionalExpectation a
  right_bimodule : ∀ {b : B.A},
    b ∈ sufficientSubalgebra → ∀ a,
      conditionalExpectation (a * b) = conditionalExpectation a * b
  referenceState_preserved : ∀ a,
    R.referenceState (conditionalExpectation a) = R.referenceState a
  comparisonState_preserved : ∀ a,
    R.comparisonState (conditionalExpectation a) = R.comparisonState a
  coarseChannel_eq_conditionalExpectation :
    P.coarseChannel = conditionalExpectation
  petzRecovery_fixes_sufficientSubalgebra : ∀ {a : B.A},
    a ∈ sufficientSubalgebra → P.petzRecovery a = a
  modularInvariant : ∀ (t : ℝ) {a : B.A},
    a ∈ sufficientSubalgebra →
      M.modularFlow t a ∈ sufficientSubalgebra
  conditionalExpectationPositiveClaim : Prop
  conditionalExpectationPositiveProof :
    conditionalExpectationPositiveClaim
  conditionalExpectationCompletelyPositiveClaim : Prop
  conditionalExpectationCompletelyPositiveProof :
    conditionalExpectationCompletelyPositiveClaim
  conditionalExpectationNormalClaim : Prop
  conditionalExpectationNormalProof :
    conditionalExpectationNormalClaim
  sufficientSubalgebraWeaklyClosedClaim : Prop
  sufficientSubalgebraWeaklyClosedProof :
    sufficientSubalgebraWeaklyClosedClaim
  referenceStateFaithfulNormalClaim : Prop
  referenceStateFaithfulNormalProof :
    referenceStateFaithfulNormalClaim
  takesakiInvariantIffExpectationClaim : Prop
  takesakiInvariantIffExpectationProof :
    takesakiInvariantIffExpectationClaim
  statePreservingExpectationUniqueClaim : Prop
  statePreservingExpectationUniqueProof :
    statePreservingExpectationUniqueClaim
  entropyEqualityIffSufficientSubalgebraClaim : Prop
  entropyEqualityIffSufficientSubalgebraProof :
    entropyEqualityIffSufficientSubalgebraClaim
  runtimeConstructsConditionalExpectation : Bool
  runtimeClaimsTakesakiTheorem : Bool
  runtimeClaimsSufficientSubalgebraTheorem : Bool
  runtimeUpdatesWorld : Bool
  noRuntimeConditionalExpectationConstruction :
    runtimeConstructsConditionalExpectation = false
  noRuntimeTakesakiTheoremClaim :
    runtimeClaimsTakesakiTheorem = false
  noRuntimeSufficientSubalgebraTheoremClaim :
    runtimeClaimsSufficientSubalgebraTheorem = false
  noRuntimeWorldUpdate : runtimeUpdatesWorld = false
  worldNotIdentifiedWithSufficientSubalgebra : Prop
  worldNotIdentifiedProof : worldNotIdentifiedWithSufficientSubalgebra
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

namespace WorldConditionalExpectationTakesakiBridge

variable {C : RealHilbertL2Carrier}
variable {W : WorldNoncommutativeOperatorAlgebra C}
variable [PartialOrder W.Region]
variable {B : WorldCStarLocalNetBridge C W}
variable {V : WorldVonNeumannBicommutantBridge B}
variable {M : WorldStandardFormModularFlowBridge V}
variable {R : WorldModularStateKMSRelativeFlowBridge M}
variable {E : WorldArakiRelativeEntropyBridge R}
variable {P : WorldPetzRecoverySufficiencyBridge E}
variable (T : WorldConditionalExpectationTakesakiBridge P)

 theorem conditionalExpectation_unital :
    T.conditionalExpectation 1 = 1 :=
  T.conditionalExpectation_one

 theorem conditionalExpectation_idempotent (a : B.A) :
    T.conditionalExpectation (T.conditionalExpectation a) =
      T.conditionalExpectation a :=
  T.fixes_sufficientSubalgebra
    (T.maps_into_sufficientSubalgebra a)

 theorem mem_sufficientSubalgebra_iff_fixed (a : B.A) :
    a ∈ T.sufficientSubalgebra ↔ T.conditionalExpectation a = a := by
  constructor
  · exact T.fixes_sufficientSubalgebra
  · intro h
    rw [← h]
    exact T.maps_into_sufficientSubalgebra a

 theorem mem_sufficientSubalgebra_iff_exists_image (a : B.A) :
    a ∈ T.sufficientSubalgebra ↔
      ∃ x : B.A, T.conditionalExpectation x = a := by
  constructor
  · intro ha
    exact ⟨a, T.fixes_sufficientSubalgebra ha⟩
  · rintro ⟨x, hx⟩
    rw [← hx]
    exact T.maps_into_sufficientSubalgebra x

 theorem star_mem_sufficientSubalgebra
    {a : B.A} (ha : a ∈ T.sufficientSubalgebra) :
    star a ∈ T.sufficientSubalgebra :=
  T.sufficientSubalgebra_star_closed ha

 theorem conditionalExpectation_preserves_star (a : B.A) :
    T.conditionalExpectation (star a) =
      star (T.conditionalExpectation a) :=
  T.conditionalExpectation_star a

 theorem conditionalExpectation_left_module
    {b : B.A} (hb : b ∈ T.sufficientSubalgebra) (a : B.A) :
    T.conditionalExpectation (b * a) =
      b * T.conditionalExpectation a :=
  T.left_bimodule hb a

 theorem conditionalExpectation_right_module
    {b : B.A} (hb : b ∈ T.sufficientSubalgebra) (a : B.A) :
    T.conditionalExpectation (a * b) =
      T.conditionalExpectation a * b :=
  T.right_bimodule hb a

 theorem conditionalExpectation_two_sided_module
    {b c : B.A}
    (hb : b ∈ T.sufficientSubalgebra)
    (hc : c ∈ T.sufficientSubalgebra)
    (a : B.A) :
    T.conditionalExpectation (b * a * c) =
      b * T.conditionalExpectation a * c := by
  rw [T.right_bimodule hc (b * a)]
  rw [T.left_bimodule hb a]

 theorem referenceState_exactly_preserved (a : B.A) :
    R.referenceState (T.conditionalExpectation a) = R.referenceState a :=
  T.referenceState_preserved a

 theorem comparisonState_exactly_preserved (a : B.A) :
    R.comparisonState (T.conditionalExpectation a) = R.comparisonState a :=
  T.comparisonState_preserved a

 theorem distinguished_state_pair_preserved :
    (∀ a, R.referenceState (T.conditionalExpectation a) =
      R.referenceState a) ∧
    (∀ a, R.comparisonState (T.conditionalExpectation a) =
      R.comparisonState a) :=
  ⟨T.referenceState_preserved, T.comparisonState_preserved⟩

 theorem coarseChannel_maps_into_sufficientSubalgebra (a : B.A) :
    P.coarseChannel a ∈ T.sufficientSubalgebra := by
  rw [T.coarseChannel_eq_conditionalExpectation]
  exact T.maps_into_sufficientSubalgebra a

 theorem recoveredChannel_eq_conditionalExpectation_apply (a : B.A) :
    P.recoveredChannel a = T.conditionalExpectation a := by
  change P.petzRecovery (P.coarseChannel a) = T.conditionalExpectation a
  rw [T.coarseChannel_eq_conditionalExpectation]
  exact T.petzRecovery_fixes_sufficientSubalgebra
    (T.maps_into_sufficientSubalgebra a)

 theorem recoveredChannel_fixed_points_are_sufficient
    {a : B.A} (ha : a ∈ T.sufficientSubalgebra) :
    P.recoveredChannel a = a := by
  rw [T.recoveredChannel_eq_conditionalExpectation_apply]
  exact T.fixes_sufficientSubalgebra ha

 theorem sufficient_subalgebra_entropy_equality :
    P.coarseRelativeEntropy = E.globalRelativeEntropy :=
  P.entropyEquality

 theorem modularFlow_preserves_sufficientSubalgebra
    (t : ℝ) {a : B.A} (ha : a ∈ T.sufficientSubalgebra) :
    M.modularFlow t a ∈ T.sufficientSubalgebra :=
  T.modularInvariant t ha

 theorem modularFlow_preserves_sufficient_star
    (t : ℝ) {a : B.A} (ha : a ∈ T.sufficientSubalgebra) :
    M.modularFlow t (star a) ∈ T.sufficientSubalgebra := by
  apply T.modularInvariant t
  exact T.sufficientSubalgebra_star_closed ha

 theorem analytic_receipts_complete :
    T.conditionalExpectationPositiveClaim ∧
    T.conditionalExpectationCompletelyPositiveClaim ∧
    T.conditionalExpectationNormalClaim ∧
    T.sufficientSubalgebraWeaklyClosedClaim ∧
    T.referenceStateFaithfulNormalClaim ∧
    T.takesakiInvariantIffExpectationClaim ∧
    T.statePreservingExpectationUniqueClaim ∧
    T.entropyEqualityIffSufficientSubalgebraClaim :=
  ⟨T.conditionalExpectationPositiveProof,
    T.conditionalExpectationCompletelyPositiveProof,
    T.conditionalExpectationNormalProof,
    T.sufficientSubalgebraWeaklyClosedProof,
    T.referenceStateFaithfulNormalProof,
    T.takesakiInvariantIffExpectationProof,
    T.statePreservingExpectationUniqueProof,
    T.entropyEqualityIffSufficientSubalgebraProof⟩

 theorem runtime_grants_no_conditional_expectation_authority :
    T.runtimeConstructsConditionalExpectation = false ∧
    T.runtimeClaimsTakesakiTheorem = false ∧
    T.runtimeClaimsSufficientSubalgebraTheorem = false ∧
    T.runtimeUpdatesWorld = false :=
  ⟨T.noRuntimeConditionalExpectationConstruction,
    T.noRuntimeTakesakiTheoremClaim,
    T.noRuntimeSufficientSubalgebraTheoremClaim,
    T.noRuntimeWorldUpdate⟩

 theorem representation_boundary_preserved :
    T.worldNotIdentifiedWithSufficientSubalgebra ∧
    T.multiWorldNoncollapsePreserved ∧
    T.twoTruthsGapPreserved :=
  ⟨T.worldNotIdentifiedProof, T.multiWorldNoncollapseProof,
    T.twoTruthsGapProof⟩

end WorldConditionalExpectationTakesakiBridge
end WORLD
end KUOS
