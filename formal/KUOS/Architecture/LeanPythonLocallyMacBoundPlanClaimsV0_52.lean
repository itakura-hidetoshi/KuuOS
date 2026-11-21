import Mathlib
import KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51
import KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.52 — Local MAC evidence is not original PlanOS semantics

A Python verifier can check an HMAC relative to an externally provisioned
symmetric key. This Lean module does NOT model or prove HMAC-SHA256 security,
trusted key provisioning, issuer identity, replay immunity, or native issuance.
The Boolean check flag is a *local report*, not a proof term that the original
PlanOS produced any of its three missing resulting Finsets.

The original Lean certificate and previous v0.50/v0.51 typed interfaces are
imported. Any matching to the ORIGINAL certificate still requires independent
EvidenceMatchesOriginal proofs.
-/

namespace KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52

open KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51
open KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50
open KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49
open KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48
open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-- Non-authoritative local verification report, distinct from a proof of
authentic issuer identity, causal event identity, or original Lean validity. -/
structure ReportedMacBoundClaim where
  declared : DeclaredPlanResultClaim
  keyId : String
  contextId : String
  sequence : Nat
  localMacCheckPassed : Bool

def localMacPassed (r : ReportedMacBoundClaim) : Prop :=
  r.localMacCheckPassed = true

/-- Conditional result agreement comes from the two EXACT original matches,
not from the presence of MAC status flags. -/
theorem exact_original_matches_agree_despite_mac_report
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (r s : ReportedMacBoundClaim)
    (_rMac : localMacPassed r)
    (_sMac : localMacPassed s)
    (hr : EvidenceMatchesOriginal p r.declared.evidence)
    (hs : EvidenceMatchesOriginal p s.declared.evidence) :
    threeResultSetsAgree r.declared s.declared := by
  exact two_matches_one_original_imply_result_agreement p r.declared s.declared hr hs

/-- An observed conflict blocks simultaneous exact original matches even
if two local MAC checks report success. -/
theorem mac_reports_cannot_erase_original_obstruction
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (r s : ReportedMacBoundClaim)
    (_rMac : localMacPassed r)
    (_sMac : localMacPassed s)
    (diff : threeResultSetsConflict r.declared s.declared)
    (hr : EvidenceMatchesOriginal p r.declared.evidence)
    (hs : EvidenceMatchesOriginal p s.declared.evidence) : False := by
  exact conflicting_claims_cannot_both_match_original p r.declared s.declared diff hr hs

/-- A constructive counterexample: matching declared sources, same key label,
same context, and two positive locally declared MAC flags do not imply
agreement of the original-type result sets. The flags are NOT cryptographic
proofs in Lean. This preserves v0.49's fresh-element obstruction. -/
theorem mac_flags_and_matching_labels_do_not_force_result_agreement
    (v : KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4.MiddleWayContinuityCertificate)
    (l d m : String)
    (fresh : l ∉ v.resultingLineage)
    (keyId context verifyDigest planDigest : String) :
    ∃ (r s : ReportedMacBoundClaim),
      localMacPassed r ∧
      localMacPassed s ∧
      r.keyId = s.keyId ∧
      r.contextId = s.contextId ∧
      sourceLabelsAgree r.declared s.declared ∧
      threeResultSetsConflict r.declared s.declared := by
  let a := declareOriginalCertificate (inertPlanOfVerify v)
    "claim-A" "caller-A" verifyDigest planDigest
  let b := declareOriginalCertificate (widenedPlanOfVerify v l d m)
    "claim-B" "caller-B" verifyDigest planDigest
  have hs : sourceLabelsAgree a b ∧ threeResultSetsConflict a b :=
    source_label_agreement_does_not_imply_result_agreement
      v l d m fresh "claim-A" "claim-B" "caller-A" "caller-B" verifyDigest planDigest
  let r : ReportedMacBoundClaim :=
    { declared := a, keyId := keyId, contextId := context,
      sequence := 1, localMacCheckPassed := true }
  let s : ReportedMacBoundClaim :=
    { declared := b, keyId := keyId, contextId := context,
      sequence := 1, localMacCheckPassed := true }
  refine ⟨r, s, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rfl
  · rfl
  · rfl
  · rfl
  · exact hs.1
  · exact hs.2

/-- Even an independently matched original certificate plus a positive local
MAC report cannot supply authorization absent from the original valid state. -/
theorem local_mac_does_not_grant_execution
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (r : ReportedMacBoundClaim)
    (_mac : localMacPassed r)
    (_match : EvidenceMatchesOriginal p r.declared.evidence)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false ∧
    p.planSynthesisPerformed = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted,
    valid.plan_synthesis_not_performed⟩

end KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52

#print axioms KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52.localMacPassed
#print axioms KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52.exact_original_matches_agree_despite_mac_report
#print axioms KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52.mac_reports_cannot_erase_original_obstruction
#print axioms KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52.mac_flags_and_matching_labels_do_not_force_result_agreement
#print axioms KUOS.Architecture.LeanPythonLocallyMacBoundPlanClaimsV0_52.local_mac_does_not_grant_execution
