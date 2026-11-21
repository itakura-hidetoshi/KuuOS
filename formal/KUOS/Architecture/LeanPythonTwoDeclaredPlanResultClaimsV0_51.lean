import Mathlib
import KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50
import KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.51: Two declared PlanOS result claims; agreement versus obstruction

The native PlanOS v1.03 output lacks three resulting Finsets.
The v0.50 supplementary result evidence is caller-declared unless independently
equipped with an EvidenceMatchesOriginal proof. Claim IDs, claimed issuer
labels and matching digests do NOT authenticate an issuer or prove causality.

All theorem terms import the ORIGINAL Lean PlanOS certificate and the
previously certified typed supplementary-evidence interface. No handwritten
stand-in for the original certificate or its full serializer is introduced.
-/

namespace KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51

open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50
open KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49
open KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48

/-- A caller-declared observation. Its issuer label is a STRING, never an
authenticated issuer identity or an authority-bearing capability. -/
structure DeclaredPlanResultClaim where
  claimId : String
  claimedIssuerLabel : String
  sourceVerifyDigest : String
  sourcePlanDigest : String
  evidence : ExplicitPlanResultEvidence

/-- Two source strings agree; this says nothing about true event identity. -/
def sourceLabelsAgree (a b : DeclaredPlanResultClaim) : Prop :=
  a.sourceVerifyDigest = b.sourceVerifyDigest ∧
  a.sourcePlanDigest = b.sourcePlanDigest

/-- Actual typed equality of all three supplementary result sets. -/
def threeResultSetsAgree (a b : DeclaredPlanResultClaim) : Prop :=
  a.evidence.resultingLineage = b.evidence.resultingLineage ∧
  a.evidence.resultingDissent = b.evidence.resultingDissent ∧
  a.evidence.resultingMinority = b.evidence.resultingMinority

/-- Preserve the exact obstruction rather than select a preferred claimant. -/
def threeResultSetsConflict (a b : DeclaredPlanResultClaim) : Prop :=
  a.evidence.resultingLineage ≠ b.evidence.resultingLineage ∨
  a.evidence.resultingDissent ≠ b.evidence.resultingDissent ∨
  a.evidence.resultingMinority ≠ b.evidence.resultingMinority

/-- A certified SAME original PlanOS certificate yields agreement.
The equality proofs are extra obligations and cannot be produced by a
matching caller-supplied digest alone. -/
theorem two_matches_one_original_imply_result_agreement
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (a b : DeclaredPlanResultClaim)
    (ha : EvidenceMatchesOriginal p a.evidence)
    (hb : EvidenceMatchesOriginal p b.evidence) :
    threeResultSetsAgree a b := by
  exact ⟨ha.lineage.trans hb.lineage.symm,
    ha.dissent.trans hb.dissent.symm,
    ha.minority.trans hb.minority.symm⟩

/-- A concrete conflict prevents both claims from being exact matches to
one original typed certificate, regardless of labels or vote counts. -/
theorem conflicting_claims_cannot_both_match_original
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (a b : DeclaredPlanResultClaim)
    (hConflict : threeResultSetsConflict a b)
    (ha : EvidenceMatchesOriginal p a.evidence)
    (hb : EvidenceMatchesOriginal p b.evidence) : False := by
  have agree := two_matches_one_original_imply_result_agreement p a b ha hb
  rcases hConflict with lineage | dissent | minority
  · exact lineage agree.1
  · exact dissent agree.2.1
  · exact minority agree.2.2

/-- Construct declaration-shaped records FROM known formal certificates.
No external claim is thereby proven to exist or to originate from an issuer. -/
def declareOriginalCertificate (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (claimId issuerLabel verifyDigest planDigest : String) :
    DeclaredPlanResultClaim where
  claimId := claimId
  claimedIssuerLabel := issuerLabel
  sourceVerifyDigest := verifyDigest
  sourcePlanDigest := planDigest
  evidence := explicitResultEvidence p

/-- Even identical declared source digests can accompany incompatible
results (under a genuinely fresh lineage element) in the v0.49 model.
The two declared issuer strings are no more than caller-provided labels. -/
theorem source_label_agreement_does_not_imply_result_agreement
    (v : KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4.MiddleWayContinuityCertificate)
    (l d m : String)
    (fresh : l ∉ v.resultingLineage)
    (claimA claimB issuerA issuerB verifyDigest planDigest : String) :
    let a := declareOriginalCertificate (inertPlanOfVerify v)
      claimA issuerA verifyDigest planDigest
    let b := declareOriginalCertificate (widenedPlanOfVerify v l d m)
      claimB issuerB verifyDigest planDigest
    sourceLabelsAgree a b ∧ threeResultSetsConflict a b := by
  constructor
  · exact ⟨rfl, rfl⟩
  · left
    change (inertPlanOfVerify v).resultingLineage ≠
      (widenedPlanOfVerify v l d m).resultingLineage
    exact different_resulting_lineage_if_fresh v l d m fresh

/-- Consensus among caller declarations does not create host permission;
only a separately validated ORIGINAL certificate has this no-authority fact. -/
theorem declared_agreement_no_host_authority
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (a b : DeclaredPlanResultClaim)
    (_agreement : threeResultSetsAgree a b)
    (_aMatch : EvidenceMatchesOriginal p a.evidence)
    (_bMatch : EvidenceMatchesOriginal p b.evidence)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p) :
    p.executionPermission = false ∧
    p.executionAuthorityGranted = false ∧
    p.selectionAuthorityGrantedToPlanOS = false ∧
    p.planSynthesisPerformed = false := by
  exact ⟨valid.execution_permission_false,
    valid.execution_authority_not_granted,
    valid.selection_authority_not_granted,
    valid.plan_synthesis_not_performed⟩

end KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51

#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.sourceLabelsAgree
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.threeResultSetsAgree
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.threeResultSetsConflict
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.two_matches_one_original_imply_result_agreement
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.conflicting_claims_cannot_both_match_original
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.declareOriginalCertificate
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.source_label_agreement_does_not_imply_result_agreement
#print axioms KUOS.Architecture.LeanPythonTwoDeclaredPlanResultClaimsV0_51.declared_agreement_no_host_authority
