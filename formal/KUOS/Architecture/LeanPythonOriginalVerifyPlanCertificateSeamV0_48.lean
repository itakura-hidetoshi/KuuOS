import Mathlib
import KUOS.Architecture.LeanPythonOriginalDecisionTypeBridgeV0_47
import KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45
import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.48 — Original VerifyOS/PlanOS certificate seam (not a CPython refinement)

The original Lean certificate *types*, not copies of their fields, are
imported. Equality of the specified source/target fields is an explicit,
typed seam. Without a seam, no cross-OS descent is asserted.

An inert PlanOS receipt is constructed as a formal witness, not as proof that
a Python kernel or an external plan/host action actually executed.
The Python observer separately tests projections of original native receipts.
In particular, its PlanOS output does not separately expose every resulting
Lean Finset; the unobserved fields remain NO_DATA at the Python layer.
-/

namespace KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48

open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45

/-- Conditional, exact-typed handoff of provenance from original VerifyOS
to original PlanOS. There is no implicit equality between their certificates. -/
structure OriginalCertificateSeam
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate) : Prop where
  transition : p.sourceTransitionKind = v.transitionKind
  conditionalStatus : p.sourceConditionalValidityStatus = v.conditionalValidityStatus
  sourceLineage : p.sourceLineage = v.resultingLineage
  predecessor : p.predecessorReference = v.predecessorReference
  sourceResponsibility : p.sourceResponsibility = v.resultingResponsibility
  sourceDissent : p.sourceDissent = v.resultingDissent
  sourceMinority : p.sourceMinorityEvidence = v.resultingMinorityEvidence

/-- Exact equality of the original transition status is necessary for gluing. -/
theorem original_status_transport
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (s : OriginalCertificateSeam v p) :
    p.sourceConditionalValidityStatus = statusForTransition v.transitionKind := by
  calc
    p.sourceConditionalValidityStatus = v.conditionalValidityStatus := s.conditionalStatus
    _ = statusForTransition v.transitionKind := v.transitionStatusMatches

/-- The imported PlanOS disposition is governed by the ORIGINAL VerifyOS kind. -/
theorem original_disposition_transport
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (s : OriginalCertificateSeam v p) :
    p.intakeDisposition = dispositionForStatus (statusForTransition v.transitionKind) := by
  calc
    p.intakeDisposition = dispositionForStatus p.sourceConditionalValidityStatus :=
      p.dispositionMatches
    _ = dispositionForStatus (statusForTransition v.transitionKind) := by
      rw [original_status_transport v p s]

/-- Conditional PlanOS admission is exactly the original VerifyOS retain case.
It is not plan synthesis, permission, or an execution authority. -/
theorem original_only_retain_admitted
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (s : OriginalCertificateSeam v p) :
    p.boundedSynthesisRequestAdmitted = true ↔ v.transitionKind = .retain := by
  rw [p.admissionExact, original_status_transport v p s]
  exact onlyRetainRouteAdmitted v.transitionKind

/-- Finset monotonicity descends across this exact typed seam only. -/
theorem original_lineage_transport
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (s : OriginalCertificateSeam v p)
    (digest : String) (h : digest ∈ v.sourceLineage) :
    digest ∈ p.resultingLineage := by
  have hv : digest ∈ v.resultingLineage := v.lineageMonotone h
  have hp : digest ∈ p.sourceLineage := by
    simpa only [s.sourceLineage] using hv
  exact p.lineageMonotone hp

/-- The explicit predecessor reference survives the second original kernel. -/
theorem original_predecessor_transport
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (s : OriginalCertificateSeam v p) :
    v.predecessorReference ∈ p.resultingLineage := by
  simpa only [s.predecessor] using p.predecessorPreserved

/-- Source responsibility, dissent and minority evidence remain distinguishable. -/
theorem original_responsibility_dissent_minority_transport
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (s : OriginalCertificateSeam v p)
    (responsibility dissent minority : String)
    (hr : responsibility ∈ v.sourceResponsibility)
    (hd : dissent ∈ v.sourceDissent)
    (hm : minority ∈ v.sourceMinorityEvidence) :
    responsibility ∈ p.resultingResponsibility ∧
    dissent ∈ p.resultingDissent ∧
    minority ∈ p.resultingMinorityEvidence := by
  refine ⟨?_, ?_, ?_⟩
  · exact p.responsibilityMonotone (by
      simpa only [s.sourceResponsibility] using v.responsibilityPreserved hr)
  · exact p.dissentMonotone (by
      simpa only [s.sourceDissent] using v.dissentPreserved hd)
  · exact p.minorityEvidenceMonotone (by
      simpa only [s.sourceMinority] using v.minorityEvidencePreserved hm)

/-- Even two native valid certificates and a seam transfer no host authority. -/
theorem original_seam_no_execution_authority
    (v : MiddleWayContinuityCertificate)
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (_s : OriginalCertificateSeam v p)
    (hv : MiddleWayContinuityCertificateValid v)
    (hp : MiddleWayBoundedSynthesisIntakeCertificateValid p) :
    v.executionPermission = false ∧
    p.executionPermission = false ∧
    p.selectionAuthorityGrantedToPlanOS = false ∧
    p.executionAuthorityGranted = false ∧
    p.planSynthesisPerformed = false ∧
    p.persistentWorldStateChanged = false := by
  exact ⟨hv.execution_permission_false, hp.execution_permission_false,
    hp.selection_authority_not_granted, hp.execution_authority_not_granted,
    hp.plan_synthesis_not_performed, hp.persistent_world_state_unchanged⟩

/-- One explicitly constructed inert original PlanOS receipt for a given
VerifyOS certificate. This is a formal construction, not a native kernel run. -/
def inertPlanOfVerify (v : MiddleWayContinuityCertificate) :
    MiddleWayBoundedSynthesisIntakeCertificate where
  sourceTransitionKind := v.transitionKind
  sourceConditionalValidityStatus := v.conditionalValidityStatus
  intakeDisposition := dispositionForStatus v.conditionalValidityStatus
  sourceLineage := v.resultingLineage
  resultingLineage := v.resultingLineage
  predecessorReference := v.predecessorReference
  sourceResponsibility := v.resultingResponsibility
  resultingResponsibility := v.resultingResponsibility
  sourceDissent := v.resultingDissent
  resultingDissent := v.resultingDissent
  sourceMinorityEvidence := v.resultingMinorityEvidence
  resultingMinorityEvidence := v.resultingMinorityEvidence
  transitionStatusMatches := v.transitionStatusMatches
  dispositionMatches := rfl
  lineageMonotone := by intro _ h; exact h
  predecessorPreserved := v.predecessorPreserved
  responsibilityMonotone := by intro _ h; exact h
  dissentMonotone := by intro _ h; exact h
  minorityEvidenceMonotone := by intro _ h; exact h
  boundedSynthesisRequestAdmitted := admittedForStatus v.conditionalValidityStatus
  admissionExact := rfl
  selectionAuthorityGrantedToPlanOS := false
  planSynthesisPerformed := false
  concretePlanIssued := false
  executionAuthorityGranted := false
  executionPermission := false
  persistentWorldStateChanged := false
  activeNow := false

theorem inert_plan_valid (v : MiddleWayContinuityCertificate) :
    MiddleWayBoundedSynthesisIntakeCertificateValid (inertPlanOfVerify v) := by
  exact {
    selection_authority_not_granted := rfl
    plan_synthesis_not_performed := rfl
    concrete_plan_not_issued := rfl
    execution_authority_not_granted := rfl
    execution_permission_false := rfl
    persistent_world_state_unchanged := rfl
    active_now_false := rfl
  }

theorem inert_plan_exact_seam (v : MiddleWayContinuityCertificate) :
    OriginalCertificateSeam v (inertPlanOfVerify v) := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Canonical limited admission also remains conditional on VerifyOS retain. -/
theorem inert_plan_retain_iff (v : MiddleWayContinuityCertificate) :
    (inertPlanOfVerify v).boundedSynthesisRequestAdmitted = true ↔
      v.transitionKind = .retain := by
  exact original_only_retain_admitted v (inertPlanOfVerify v)
    (inert_plan_exact_seam v)

end KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48

#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_status_transport
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_disposition_transport
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_only_retain_admitted
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_lineage_transport
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_predecessor_transport
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_responsibility_dissent_minority_transport
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.original_seam_no_execution_authority
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.inertPlanOfVerify
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.inert_plan_valid
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.inert_plan_exact_seam
#print axioms KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48.inert_plan_retain_iff
