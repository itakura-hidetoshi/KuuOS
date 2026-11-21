import Mathlib
import KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49
import KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48
import KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

/-!
# v0.50 — Explicit supplementary PlanOS result evidence, conditional only

The original native PlanOS v1.03 Python output does not serialize the three
resulting Finsets. v0.49 proved noninjectivity for one bounded projection.
We retain that obstruction, and add a separate, *explicitly supplied* typed
result bundle. Equations connecting this bundle to an original Lean
certificate are assumptions/proof obligations, not automatically obtained
from a caller's Python dictionary, digest, or external identity.
-/

namespace KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50

open KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
open KUOS.Architecture.LeanPythonOriginalVerifyPlanCertificateSeamV0_48
open KUOS.Architecture.LeanPythonPlanResultObservationObstructionV0_49

/-- Separately expressed result sets. Not a native Python PlanOS output. -/
structure ExplicitPlanResultEvidence where
  visibleSource : VisiblePlanSourceProjection
  resultingLineage : Finset String
  resultingDissent : Finset String
  resultingMinority : Finset String

/-- If an original typed certificate is supplied, a full result bundle can
be constructed formally; this does not certify any external Python input. -/
def explicitResultEvidence (p : MiddleWayBoundedSynthesisIntakeCertificate) :
    ExplicitPlanResultEvidence where
  visibleSource := visiblePlanSourceProjection p
  resultingLineage := p.resultingLineage
  resultingDissent := p.resultingDissent
  resultingMinority := p.resultingMinorityEvidence

/-- Three added result equalities are proof obligations, not inferred from
the bounded visible source projection or an unsigned JSON object. -/
structure EvidenceMatchesOriginal
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (e : ExplicitPlanResultEvidence) : Prop where
  source : e.visibleSource = visiblePlanSourceProjection p
  lineage : e.resultingLineage = p.resultingLineage
  dissent : e.resultingDissent = p.resultingDissent
  minority : e.resultingMinority = p.resultingMinorityEvidence

theorem explicit_result_evidence_matches_original
    (p : MiddleWayBoundedSynthesisIntakeCertificate) :
    EvidenceMatchesOriginal p (explicitResultEvidence p) := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- The *additional typed equalities*, not the old projection alone, make
the three original result sets uniquely determined within their scope. -/
theorem matching_explicit_evidence_determines_result_sets
    (p q : MiddleWayBoundedSynthesisIntakeCertificate)
    (e : ExplicitPlanResultEvidence)
    (hp : EvidenceMatchesOriginal p e)
    (hq : EvidenceMatchesOriginal q e) :
    p.resultingLineage = q.resultingLineage ∧
    p.resultingDissent = q.resultingDissent ∧
    p.resultingMinorityEvidence = q.resultingMinorityEvidence := by
  exact ⟨hp.lineage.symm.trans hq.lineage,
    hp.dissent.symm.trans hq.dissent,
    hp.minority.symm.trans hq.minority⟩

theorem explicit_evidence_distinguishes_fresh_lineage
    (v : KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4.MiddleWayContinuityCertificate)
    (l d m : String)
    (fresh : l ∉ v.resultingLineage) :
    explicitResultEvidence (inertPlanOfVerify v) ≠
      explicitResultEvidence (widenedPlanOfVerify v l d m) := by
  intro h
  have hLineage := congrArg ExplicitPlanResultEvidence.resultingLineage h
  apply different_resulting_lineage_if_fresh v l d m fresh
  simpa only [explicitResultEvidence] using hLineage

/-- The v0.49 ambiguity is resolved only when one common result evidence
has proofs of exact agreement with BOTH original-type certificates. -/
theorem no_common_exact_evidence_for_distinct_original_results
    (v : KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4.MiddleWayContinuityCertificate)
    (l d m : String)
    (fresh : l ∉ v.resultingLineage)
    (e : ExplicitPlanResultEvidence)
    (hi : EvidenceMatchesOriginal (inertPlanOfVerify v) e)
    (hw : EvidenceMatchesOriginal (widenedPlanOfVerify v l d m) e) : False := by
  have h := (matching_explicit_evidence_determines_result_sets
    (inertPlanOfVerify v) (widenedPlanOfVerify v l d m) e hi hw).1
  exact different_resulting_lineage_if_fresh v l d m fresh h

/-- The actual source-only observation is still ambiguous: the additional
fields are not retroactively present in the original Python output. -/
theorem original_bounded_projection_still_ambiguous
    (v : KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4.MiddleWayContinuityCertificate)
    (l d m : String) :
    visiblePlanSourceProjection (inertPlanOfVerify v) =
      visiblePlanSourceProjection (widenedPlanOfVerify v l d m) := by
  exact same_visible_projection v l d m

/-- No evidence bundle itself is an execution license. Such authority cannot
be deduced from supplied results without separately established valid state. -/
theorem matched_evidence_does_not_transfer_execution_authority
    (p : MiddleWayBoundedSynthesisIntakeCertificate)
    (e : ExplicitPlanResultEvidence)
    (_match : EvidenceMatchesOriginal p e)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid p) :
    p.executionAuthorityGranted = false ∧
    p.executionPermission = false ∧
    p.selectionAuthorityGrantedToPlanOS = false ∧
    p.planSynthesisPerformed = false := by
  exact ⟨valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.selection_authority_not_granted,
    valid.plan_synthesis_not_performed⟩

end KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50

#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.explicitResultEvidence
#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.explicit_result_evidence_matches_original
#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.matching_explicit_evidence_determines_result_sets
#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.explicit_evidence_distinguishes_fresh_lineage
#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.no_common_exact_evidence_for_distinct_original_results
#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.original_bounded_projection_still_ambiguous
#print axioms KUOS.Architecture.LeanPythonExplicitPlanResultEvidenceV0_50.matched_evidence_does_not_transfer_execution_authority
