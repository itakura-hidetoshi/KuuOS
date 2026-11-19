"""Executable, fail-closed regression for selected Lean obligations in every OS.

These are Python conditional data checks and native validator dispatches:
NEVER a claim of Lean-certified Python semantics or external authority.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import FrozenInstanceError
from importlib import import_module
import unittest

from runtime import kuuos_lean_python_per_os_contracts_v0_27 as core
from runtime.kuuos_lean_python_os_registry_v0_5 import OS_BINDINGS

MODULES = {
    "BeliefOS": "belief",
    "DecisionOS": "decision",
    "PlanOS": "plan",
    "ActOS": "act",
    "ObserveOS": "observe",
    "VerifyOS": "verify",
    "LearnOS": "learn",
    "MemoryOS": "memory",
    "CodeAI": "codeai",
    "DecisionOSPlural": "decision_plural",
    "DecisionOSWa": "decision_wa",
    "WORLD": "world",
}

VALID = {
    "BeliefOS": dict(priorCount=3, nextCount=4, futureOnly=True,
                     memoryOverwrite=False, activationBoundaryIsReplan=True),
    "DecisionOS": dict(missionAllowed=True, prohibited=False,
                       authorityClaimed=False, withinBudget=True,
                       withinRisk=True, recoverable=True, reversible=True,
                       evidencePresent=True, futureOnly=True,
                       memoryOverwrite=False, decisionNotExecution=True),
    "PlanOS": dict(effectful=True, rollbackPresent=False,
                   humanReviewRequired=True, externalLicenseRequired=True,
                   stopConditionPresent=True, checkpointPresent=True,
                   planIsExecution=False),
    "ActOS": dict(committedPlanBound=True, exactStepBound=True,
                  actPhaseBound=True, hostLicenseBound=True,
                  projectionReceiptBound=True, singleUse=True,
                  doesNotWidenLicense=True, jobsClaimed=1, slicesRun=1),
    "ObserveOS": dict(committedActState=True, effectRecorded=True,
                      canonicalReadyReceipt=True, comparisonIsVerification=False,
                      verdict="matched", observationDebtDischarged=True,
                      reobservationRequired=False, verificationRequired=True),
    "VerifyOS": dict(verdict="passed", sourceMatched=True,
                     sourceDivergent=False, corroborationAdmissible=True,
                     criterionSatisfied=True, falsifierTriggered=False,
                     verificationIsTruth=False, causalAttributionGranted=False,
                     verificationDebtDischarged=True, verificationRequired=False,
                     reobservationRequired=False, correctiveActionRequired=False,
                     learningRequired=True),
    "LearnOS": dict(futureOnly=True, memoryOverwrite=False,
                    activeNow=False, activationRequiresReplan=True,
                    scopeWidening=False, invariantRemoval=False,
                    currentCycleMutation=False, pastRecordMutation=False,
                    reversalConditionVisible=True, expirationConditionVisible=True),
    "MemoryOS": dict(blockerStoredAsContext=True, blockerReleasedByMemory=False,
                     missingEvidenceSilentlyRepaired=False,
                     worldProjectionReadOnly=True, worldChangedByMemory=False,
                     retrievalCandidateOnly=True, durableAppendClaimed=False),
    "CodeAI": dict(candidateId="candidate-1",
                   sourceClassification="admissible", evidenceStatus="allPassed",
                   evidenceScore=6, maximumEvidenceScore=10, decision="selected",
                   scoreTreatedAsProbability=False,
                   scoreTreatedAsCorrectnessProof=False,
                   selectionTreatedAsCorrectnessProof=False,
                   abstentionTreatedAsRejection=False),
    "DecisionOSPlural": dict(optionInSourceField=True,
                             missionBoundConstraint=True,
                             stakeholderProtectedConstraint=True,
                             evidencePresent=True, grantsAuthority=False,
                             excludesConsensusOption=True),
    "DecisionOSWa": dict(confirmedFalseHarmony=False, minorityPreserved=True,
                         dissentConsidered=True, minimumWaPassed=True,
                         weakestDimensionPassed=True,
                         sourcePluralIdentityPreserved=True),
    "WORLD": dict(localCommitAuthorizationFinite=True,
                  localCommitAuthorizationSingleUse=True,
                  openHorizonPreserved=True, globalCycleLimitAbsent=True,
                  globalGenerationLimitAbsent=True,
                  globalTimeHorizonLimitAbsent=True, atomicReplaceCommitted=True,
                  oneAtomicStoreAndReceiptState=True,
                  appendOnlyHistoryPreserved=True, immutableCommitReceipt=True,
                  sameRootPreserved=True, constitutionalRootRewritten=False,
                  memoryHistoryOverwritten=False,
                  rollbackReferencePreserved=True,
                  rollbackRequiresFreshAuthorization=True,
                  rollbackDeletesHistory=False,
                  automaticRollbackPerformed=False),
}


def mod(name):
    return import_module(
        "runtime.kuuos_lean_python_" + MODULES[name] + "_obligations_v0_27"
    )


class PerOSProofContractsTests(unittest.TestCase):
    def test_all_original_twelve_os_have_distinct_python_obligation_module(self):
        self.assertEqual(set(MODULES), set(OS_BINDINGS))
        self.assertEqual(set(VALID), set(MODULES))
        for name in MODULES:
            with self.subTest(os=name):
                module = mod(name)
                self.assertEqual(module.OS_NAME, name)
                self.assertTrue(core.require_original_binding(name, module.LEAN_FILE))
                self.assertTrue(set(module.THEOREMS))
                self.assertEqual(set(module.FIELDS), set(VALID[name]))

    def test_each_os_checks_its_distinct_lean_structure_fields(self):
        for name in MODULES:
            with self.subTest(os=name):
                input_data = deepcopy(VALID[name])
                checked = mod(name).audit_witness(input_data)
                self.assertEqual(checked.status, core.LOCAL)
                self.assertTrue(checked.local_conditions_checked)
                self.assertTrue(checked.checked_fields)
                self.assertEqual(checked.lean_file, mod(name).LEAN_FILE)
                self.assertEqual(input_data, VALID[name])
                self.assertFalse(checked.lean_python_refinement_proved)
                self.assertFalse(checked.lean_proof_term_constructed)
                self.assertFalse(checked.source_issuer_authenticated)
                self.assertFalse(checked.effect_completed)
                self.assertFalse(checked.execution_authority_granted)
                self.assertFalse(checked.truth_authority_granted)

    def test_missing_required_field_keeps_no_data_per_os(self):
        for name in MODULES:
            with self.subTest(os=name):
                data = deepcopy(VALID[name])
                data.pop(next(iter(data)))
                result = mod(name).audit_witness(data)
                self.assertEqual(result.status, core.NO_DATA)
                self.assertFalse(result.local_conditions_checked)

    def test_required_bool_as_integer_fails_closed(self):
        for name in MODULES:
            with self.subTest(os=name):
                data = deepcopy(VALID[name])
                flag = next(k for k, v in data.items() if type(v) is bool)
                data[flag] = 1
                result = mod(name).audit_witness(data)
                self.assertEqual(result.status, core.BLOCKED)

    def test_wrong_non_boolean_conclusion_is_blocked_for_all_os(self):
        changes = {
            "BeliefOS": ("nextCount", 0),
            "DecisionOS": ("prohibited", True),
            "PlanOS": ("stopConditionPresent", False),
            "ActOS": ("hostLicenseBound", False),
            "ObserveOS": ("effectRecorded", False),
            "VerifyOS": ("criterionSatisfied", False),
            "LearnOS": ("activeNow", True),
            "MemoryOS": ("blockerReleasedByMemory", True),
            "CodeAI": ("sourceClassification", "rejected"),
            "DecisionOSPlural": ("grantsAuthority", True),
            "DecisionOSWa": ("confirmedFalseHarmony", True),
            "WORLD": ("memoryHistoryOverwritten", True),
        }
        for name, (key, value) in changes.items():
            with self.subTest(os=name):
                data = deepcopy(VALID[name])
                data[key] = value
                result = mod(name).audit_witness(data)
                self.assertEqual(result.status, core.BLOCKED)
                self.assertFalse(result.execution_authority_granted)

    def test_unknown_authority_flags_not_accepted_as_lean_structure(self):
        for name in MODULES:
            with self.subTest(os=name):
                data = deepcopy(VALID[name])
                data["executionAuthorityGranted"] = True
                self.assertEqual(mod(name).audit_witness(data).status, core.BLOCKED)

    def test_no_witness_and_non_plain_mapping_do_not_pass(self):
        for name in MODULES:
            with self.subTest(os=name):
                self.assertEqual(mod(name).audit_witness(None).status, core.NO_DATA)
                self.assertEqual(mod(name).audit_witness([VALID[name]]).status, core.BLOCKED)

    def test_cycle_or_custom_object_fails_before_lean_claim(self):
        for name in ("PlanOS", "ActOS", "WORLD"):
            with self.subTest(os=name):
                packet = deepcopy(VALID[name])
                packet["untrusted"] = packet
                self.assertEqual(mod(name).audit_witness(packet).status, core.BLOCKED)
                packet = deepcopy(VALID[name])
                packet["unknown"] = object()
                self.assertEqual(mod(name).audit_witness(packet).status, core.BLOCKED)

    def test_plan_non_effectful_branch_does_not_require_effect_guards(self):
        data = deepcopy(VALID["PlanOS"])
        data.update(effectful=False, rollbackPresent=False,
                    humanReviewRequired=False, externalLicenseRequired=False,
                    stopConditionPresent=False, checkpointPresent=False)
        self.assertEqual(mod("PlanOS").audit_witness(data).status, core.LOCAL)

    def test_plan_effectful_without_rollback_or_review_is_blocked(self):
        data = deepcopy(VALID["PlanOS"])
        data["humanReviewRequired"] = False
        self.assertEqual(mod("PlanOS").audit_witness(data).status, core.BLOCKED)

    def test_act_single_use_and_one_slice_are_bounded(self):
        for key in ("jobsClaimed", "slicesRun"):
            data = deepcopy(VALID["ActOS"])
            data[key] = 2
            self.assertEqual(mod("ActOS").audit_witness(data).status, core.BLOCKED)
        data = deepcopy(VALID["ActOS"])
        data["jobsClaimed"] = True
        self.assertEqual(mod("ActOS").audit_witness(data).status, core.BLOCKED)

    def test_observe_inconclusive_retains_debt_and_reobservation(self):
        data = deepcopy(VALID["ObserveOS"])
        data.update(verdict="inconclusive", observationDebtDischarged=False,
                    reobservationRequired=True)
        self.assertEqual(mod("ObserveOS").audit_witness(data).status, core.LOCAL)
        data["reobservationRequired"] = False
        self.assertEqual(mod("ObserveOS").audit_witness(data).status, core.BLOCKED)

    def test_verify_failed_and_indeterminate_have_distinct_debts(self):
        failed = deepcopy(VALID["VerifyOS"])
        failed.update(verdict="failed", sourceMatched=False,
                      sourceDivergent=True, criterionSatisfied=False,
                      verificationDebtDischarged=True,
                      correctiveActionRequired=True)
        self.assertEqual(mod("VerifyOS").audit_witness(failed).status, core.LOCAL)
        failed["sourceDivergent"] = False
        failed["criterionSatisfied"] = True
        self.assertEqual(mod("VerifyOS").audit_witness(failed).status, core.BLOCKED)
        ind = deepcopy(VALID["VerifyOS"])
        ind.update(verdict="indeterminate", corroborationAdmissible=False,
                   verificationDebtDischarged=False,
                   verificationRequired=True, reobservationRequired=True)
        self.assertEqual(mod("VerifyOS").audit_witness(ind).status, core.LOCAL)

    def test_codeai_high_score_never_overrides_ineligibility(self):
        data = deepcopy(VALID["CodeAI"])
        data["evidenceScore"] = 100_000
        data["sourceClassification"] = "repairable"
        self.assertEqual(mod("CodeAI").audit_witness(data).status, core.BLOCKED)
        data["decision"] = "abstained"
        self.assertEqual(mod("CodeAI").audit_witness(data).status, core.LOCAL)
        data["scoreTreatedAsCorrectnessProof"] = True
        self.assertEqual(mod("CodeAI").audit_witness(data).status, core.BLOCKED)

    def test_world_does_not_become_runtime_refinement(self):
        projected = mod("WORLD").audit_witness(VALID["WORLD"])
        self.assertEqual(projected.status, core.LOCAL)
        self.assertFalse(projected.lean_python_refinement_proved)
        original = mod("WORLD").audit_native_state({})
        self.assertEqual(original.status, core.NO_DATA)

    def test_original_native_state_checker_retains_missing_state(self):
        for name in MODULES:
            with self.subTest(os=name):
                original = mod(name).audit_native_state(None)
                self.assertEqual(original.status, core.NO_DATA)
                self.assertFalse(original.execution_authority_granted)

    def test_plural_and_wa_do_not_skip_original_typed_mediator_edge(self):
        for name in ("DecisionOSPlural", "DecisionOSWa"):
            with self.subTest(os=name):
                self.assertEqual(
                    mod(name).audit_native_edge(None, None).status, core.NO_DATA
                )

    def test_projection_result_is_immutable(self):
        result = mod("LearnOS").audit_witness(VALID["LearnOS"])
        with self.assertRaises(FrozenInstanceError):
            result.execution_authority_granted = True


if __name__ == "__main__":
    unittest.main()
