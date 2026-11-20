import Mathlib
import KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48
import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.49: original PlanOS resulting-set observation obstruction

All structures are the ACTUAL pinned original Lean certificate types.
The bounded source projection records fields represented by the current
Python PlanOS receipt. Resulting PlanOS lineage, dissent and minority
Finsets are not independently emitted by the original native Python kernel.

This formal proof constructs distinguishable original-type PlanOS certificates
whose deliberately scoped source projection agrees. It does NOT assert that
all possible serializers or external receipts are non-injective.
-/

namespace KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49

open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48

/-- Bounded typed source projection: no invented resulting PlanOS Finsets.
It models observed source routing and the explicit responsibility result,
not the entire native JSON serializer or its digest. -/
structure VisiblePlanSourceProjection where
  transitionKind : TransitionKind
  conditionalStatus : ConditionalValidityStatus
  disposition : IntakeDisposition
  sourceLineage : Finset String
  predecessor : String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceDissent : Finset String
  sourceMinority : Finset String
  boundedAdmitted : Bool
  selectionGranted : Bool
  planSynthesisPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  activeNow : Bool

def visiblePlanSourceProjection (p : MiddleWayBoundedSynthesisIntakeCertificate) :
    VisiblePlanSourceProjection where
  transitionKind := p.sourceTransitionKind
  conditionalStatus := p.sourceConditionalValidityStatus
  disposition := p.intakeDisposition
  sourceLineage := p.sourceLineage
  predecessor := p.predecessorReference
  sourceResponsibility := p.sourceResponsibility
  resultingResponsibility := p.resultingResponsibility
  sourceDissent := p.sourceDissent
  sourceMinority := p.sourceMinorityEvidence
  boundedAdmitted := p.boundedSynthesisRequestAdmitted
  selectionGranted := p.selectionAuthorityGrantedToPlanOS
  planSynthesisPerformed := p.planSynthesisPerformed
  executionAuthorityGranted := p.executionAuthorityGranted
  executionPermission := p.executionPermission
  activeNow := p.activeNow

/-- A second ORIGINAL PlanOS certificate: its three resulting Finsets may
contain extra history, while all source relations and no-authority flags
remain fixed. Nothing here asserts that a Python call produced this result. -/
def widenedPlanOfVerify (v : MiddleWayContinuityCertificate)
    (lineageExtra dissentExtra minorityExtra : String) :
    MiddleWayBoundedSynthesisIntakeCertificate where
  sourceTransitionKind := v.transitionKind
  sourceConditionalValidityStatus := v.conditionalValidityStatus
  intakeDisposition := dispositionForStatus v.conditionalValidityStatus
  sourceLineage := v.resultingLineage
  resultingLineage := insert lineageExtra v.resultingLineage
  predecessorReference := v.predecessorReference
  sourceResponsibility := v.resultingResponsibility
  resultingResponsibility := v.resultingResponsibility
  sourceDissent := v.resultingDissent
  resultingDissent := insert dissentExtra v.resultingDissent
  sourceMinorityEvidence := v.resultingMinorityEvidence
  resultingMinorityEvidence := insert minorityExtra v.resultingMinorityEvidence
  transitionStatusMatches := v.transitionStatusMatches
  dispositionMatches := rfl
  lineageMonotone := by
    intro a ha
    exact Finset.mem_insert_of_mem ha
  predecessorPreserved := Finset.mem_insert_of_mem v.predecessorPreserved
  responsibilityMonotone := by intro _ ha; exact ha
  dissentMonotone := by
    intro a ha
    exact Finset.mem_insert_of_mem ha
  minorityEvidenceMonotone := by
    intro a ha
    exact Finset.mem_insert_of_mem ha
  boundedSynthesisRequestAdmitted := admittedForStatus v.conditionalValidityStatus
  admissionExact := rfl
  selectionAuthorityGrantedToPlanOS := false
  planSynthesisPerformed := false
  concretePlanIssued := false
  executionAuthorityGranted := false
  executionPermission := false
  persistentWorldStateChanged := false
  activeNow := false

theorem widened_plan_valid (v : MiddleWayContinuityCertificate)
    (l d m : String) :
    MiddleWayBoundedSynthesisIntakeCertificateValid (widenedPlanOfVerify v l d m) := by
  exact {
    selection_authority_not_granted := rfl
    plan_synthesis_not_performed := rfl
    concrete_plan_not_issued := rfl
    execution_authority_not_granted := rfl
    execution_permission_false := rfl
    persistent_world_state_unchanged := rfl
    active_now_false := rfl
  }

theorem widened_plan_preserves_original_seam (v : MiddleWayContinuityCertificate)
    (l d m : String) :
    OriginalCertificateSeam v (widenedPlanOfVerify v l d m) := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- This scoped projection agrees even when the three unobserved resulting
Finsets are changed. This is a claim about this explicit model only. -/
theorem same_visible_projection (v : MiddleWayContinuityCertificate)
    (l d m : String) :
    visiblePlanSourceProjection (inertPlanOfVerify v) =
      visiblePlanSourceProjection (widenedPlanOfVerify v l d m) := by
  rfl

theorem different_resulting_lineage_if_fresh
    (v : MiddleWayContinuityCertificate) (l d m : String)
    (fresh : l ∉ v.resultingLineage) :
    (inertPlanOfVerify v).resultingLineage ≠
      (widenedPlanOfVerify v l d m).resultingLineage := by
  intro hEq
  have added : l ∈ (widenedPlanOfVerify v l d m).resultingLineage := by
    simp [widenedPlanOfVerify]
  have old : l ∈ (inertPlanOfVerify v).resultingLineage := by
    rw [hEq]
    exact added
  exact fresh (by simpa [inertPlanOfVerify] using old)

theorem different_resulting_dissent_if_fresh
    (v : MiddleWayContinuityCertificate) (l d m : String)
    (fresh : d ∉ v.resultingDissent) :
    (inertPlanOfVerify v).resultingDissent ≠
      (widenedPlanOfVerify v l d m).resultingDissent := by
  intro hEq
  have added : d ∈ (widenedPlanOfVerify v l d m).resultingDissent := by
    simp [widenedPlanOfVerify]
  have old : d ∈ (inertPlanOfVerify v).resultingDissent := by
    rw [hEq]
    exact added
  exact fresh (by simpa [inertPlanOfVerify] using old)

theorem different_resulting_minority_if_fresh
    (v : MiddleWayContinuityCertificate) (l d m : String)
    (fresh : m ∉ v.resultingMinorityEvidence) :
    (inertPlanOfVerify v).resultingMinorityEvidence ≠
      (widenedPlanOfVerify v l d m).resultingMinorityEvidence := by
  intro hEq
  have added : m ∈ (widenedPlanOfVerify v l d m).resultingMinorityEvidence := by
    simp [widenedPlanOfVerify]
  have old : m ∈ (inertPlanOfVerify v).resultingMinorityEvidence := by
    rw [hEq]
    exact added
  exact fresh (by simpa [inertPlanOfVerify] using old)

/-- An explicit non-injective witness on the inhabited, compatible original
certificate family, conditional on a genuinely absent lineage element. -/
theorem compatible_certificates_with_same_projection_can_differ
    (v : MiddleWayContinuityCertificate) (l d m : String)
    (fresh : l ∉ v.resultingLineage) :
    visiblePlanSourceProjection (inertPlanOfVerify v) =
        visiblePlanSourceProjection (widenedPlanOfVerify v l d m) ∧
      inertPlanOfVerify v ≠ widenedPlanOfVerify v l d m := by
  constructor
  · exact same_visible_projection v l d m
  · intro h
    have hResult := congrArg
      MiddleWayBoundedSynthesisIntakeCertificate.resultingLineage h
    exact (different_resulting_lineage_if_fresh v l d m fresh) hResult

/-- No decoder of this particular bounded projection can agree on both
valid originals. The missing result fields are a concrete obstruction. -/
theorem no_total_exact_decoder_on_both_originals
    (v : MiddleWayContinuityCertificate) (l d m : String)
    (fresh : l ∉ v.resultingLineage)
    (decode : VisiblePlanSourceProjection → MiddleWayBoundedSynthesisIntakeCertificate)
    (hInert : decode (visiblePlanSourceProjection (inertPlanOfVerify v)) =
      inertPlanOfVerify v)
    (hWidened : decode (visiblePlanSourceProjection (widenedPlanOfVerify v l d m)) =
      widenedPlanOfVerify v l d m) : False := by
  have same := same_visible_projection v l d m
  have hCertificates : inertPlanOfVerify v = widenedPlanOfVerify v l d m := by
    calc
      inertPlanOfVerify v =
          decode (visiblePlanSourceProjection (inertPlanOfVerify v)) := hInert.symm
      _ = decode (visiblePlanSourceProjection (widenedPlanOfVerify v l d m)) :=
        congrArg decode same
      _ = widenedPlanOfVerify v l d m := hWidened
  exact (compatible_certificates_with_same_projection_can_differ v l d m fresh).2
    hCertificates

end KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49

#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.visiblePlanSourceProjection
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.widenedPlanOfVerify
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.widened_plan_valid
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.widened_plan_preserves_original_seam
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.same_visible_projection
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.different_resulting_lineage_if_fresh
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.different_resulting_dissent_if_fresh
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.different_resulting_minority_if_fresh
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.compatible_certificates_with_same_projection_can_differ
#print axioms KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49.no_total_exact_decoder_on_both_originals
