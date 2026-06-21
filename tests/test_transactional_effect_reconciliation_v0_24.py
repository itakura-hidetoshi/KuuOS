from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_act_os_fixture_v0_1 import (
    host_inputs,
    prepared_project_state,
    source_plan,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_transactional_effect_reconciliation_kernel_v0_24 import (
    build_compensation_request,
    build_connector_contract,
    build_initial_transaction_state,
    build_transaction_intent,
    validate_connector_contract,
    validate_transaction_intent,
    validate_transaction_state,
)
from runtime.kuuos_transactional_effect_scenarios_v0_24 import (
    run_transactional_effect_scenarios,
)


class TransactionalEffectReconciliationV024Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_transactional_effect_scenarios()
        self.assertEqual(
            "KUUOS_TRANSACTIONAL_EFFECT_RECONCILIATION_V0_24_OK",
            result["status"],
        )
        self.assertEqual("EFFECT_CONFIRMED", result["confirmed_route"])
        self.assertEqual("COMPENSATION_PROPOSED", result["compensation_route"])
        self.assertEqual("HANDOVER_REQUIRED", result["handover_route"])
        self.assertEqual("REOBSERVATION_REQUIRED", result["reobservation_route"])
        self.assertEqual("NO_EFFECT_RECORDED", result["no_effect_route"])
        self.assertEqual("REPLAYED", result["replay_status"])
        self.assertTrue(result["tool_response_success_not_world_confirmation"])
        self.assertFalse(result["automatic_compensation"])
        self.assertFalse(result["automatic_rollback"])
        self.assertFalse(result["execution_authority_granted"])

    def test_connector_requires_explicit_noncompensability(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "noncompensability_reason_digest_required"
        ):
            with TemporaryDirectory() as directory:
                root = Path(directory)
                plan_state, activation = source_plan(root / "plan")
                _, _, host_license, projection = host_inputs(job_id="no-reason-job")
                _, prepared_act = prepared_project_state(
                    root=root / "act",
                    act_id="no-reason-act",
                    plan_state=plan_state,
                    plan_activation=activation,
                    job_id="no-reason-job",
                    host_license=host_license,
                    projection=projection,
                )
                connector = build_connector_contract(
                    connector_id="no-reason-connector",
                    adapter_kind="fixture",
                    trusted_registry_entry_digest=sha("registry"),
                    operation_allowlist=["fixture.success"],
                    compensation_mode="noncompensable",
                    compensation_operation_allowlist=[],
                    observation_channel_ids=["system-output"],
                )
                build_transaction_intent(
                    transaction_id="no-reason-transaction",
                    prepared_act_state=prepared_act,
                    connector_contract=connector,
                    intended_effect_digest=sha("effect"),
                    idempotency_key=prepared_act["step_authorization"][
                        "invocation_id"
                    ],
                    timeout_ms=1_000,
                    max_retries=0,
                    prepared_at_ms=90_003,
                )

    def test_idempotency_key_must_bind_lower_invocation(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            plan_state, activation = source_plan(root / "plan")
            _, _, host_license, projection = host_inputs(job_id="idempotency-job")
            _, prepared_act = prepared_project_state(
                root=root / "act",
                act_id="idempotency-act",
                plan_state=plan_state,
                plan_activation=activation,
                job_id="idempotency-job",
                host_license=host_license,
                projection=projection,
            )
            connector = build_connector_contract(
                connector_id="idempotency-connector",
                adapter_kind="fixture",
                trusted_registry_entry_digest=sha("registry"),
                operation_allowlist=["fixture.success"],
                compensation_mode="manual_handover",
                compensation_operation_allowlist=[],
                observation_channel_ids=["system-output"],
            )
            with self.assertRaisesRegex(
                ValueError,
                "transaction_idempotency_key_must_bind_lower_invocation",
            ):
                build_transaction_intent(
                    transaction_id="idempotency-transaction",
                    prepared_act_state=prepared_act,
                    connector_contract=connector,
                    intended_effect_digest=sha("effect"),
                    idempotency_key="substituted-idempotency-key",
                    timeout_ms=1_000,
                    max_retries=0,
                    noncompensability_reason_digest=sha("manual-handover"),
                    prepared_at_ms=90_003,
                )

    def test_connector_contract_is_read_only_non_authority(self) -> None:
        connector = build_connector_contract(
            connector_id="boundary-connector",
            adapter_kind="fixture",
            trusted_registry_entry_digest=sha("registry"),
            operation_allowlist=["fixture.success"],
            compensation_mode="manual_handover",
            compensation_operation_allowlist=[],
            observation_channel_ids=["system-output"],
        )
        self.assertEqual([], validate_connector_contract(connector))
        self.assertTrue(connector["connector_contract_read_only"])
        self.assertTrue(connector["hidden_connector_call_forbidden"])
        self.assertFalse(connector["direct_connector_call_performed"])
        self.assertFalse(connector["non_authority"]["grants_execution_authority"])

        tampered = deepcopy(connector)
        tampered["direct_connector_call_performed"] = True
        self.assertIn(
            "connector_direct_call_forbidden",
            validate_connector_contract(tampered),
        )

    def test_initial_state_does_not_call_connector(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            plan_state, activation = source_plan(root / "plan")
            _, _, host_license, projection = host_inputs(job_id="prepare-job")
            _, prepared_act = prepared_project_state(
                root=root / "act",
                act_id="prepare-act",
                plan_state=plan_state,
                plan_activation=activation,
                job_id="prepare-job",
                host_license=host_license,
                projection=projection,
            )
            connector = build_connector_contract(
                connector_id="prepare-connector",
                adapter_kind="fixture",
                trusted_registry_entry_digest=sha("registry"),
                operation_allowlist=["fixture.success"],
                compensation_mode="manual_handover",
                compensation_operation_allowlist=[],
                observation_channel_ids=["system-output"],
            )
            intent = build_transaction_intent(
                transaction_id="prepare-transaction",
                prepared_act_state=prepared_act,
                connector_contract=connector,
                intended_effect_digest=sha("effect"),
                idempotency_key=prepared_act["step_authorization"][
                    "invocation_id"
                ],
                timeout_ms=1_000,
                max_retries=0,
                noncompensability_reason_digest=sha("manual-handover"),
                prepared_at_ms=90_003,
            )
            self.assertEqual([], validate_transaction_intent(intent, connector))
            state = build_initial_transaction_state(
                intent=intent,
                connector_contract=connector,
                prepared_act_state=prepared_act,
                now_ms=90_003,
            )
            self.assertEqual([], validate_transaction_state(state))
            self.assertEqual("prepared", state["current_phase"])
            self.assertFalse(state["hidden_connector_call_performed"])
            self.assertFalse(state["effect_recorded"])
            self.assertFalse(state["automatic_compensation"])
            self.assertFalse(state["automatic_rollback"])

    def test_compensation_request_never_executes_itself(self) -> None:
        fake_state = {
            "current_phase": "verified",
            "transaction_id": "tx",
            "transaction_state_digest": sha("state"),
            "transaction_intent_digest": sha("intent"),
            "reconciliation_receipt_digest": sha("reconciliation"),
            "verify_state_digest": sha("verify"),
            "transaction_intent": {
                "connector_id": "connector",
                "compensation_mode": "explicit_operation",
                "compensation_operation_id": "fixture.success",
                "compensation_input_digest": sha("compensation-input"),
                "idempotency_key": "original-key",
            },
        }
        request = build_compensation_request(
            state=fake_state,
            request_id="request",
            new_idempotency_key="new-key",
            proposed_plan_lineage_id="new-lineage",
            rationale_digest=sha("rationale"),
            requested_at_ms=1,
        )
        self.assertTrue(request["proposal_only"])
        self.assertTrue(request["requires_new_planos_synthesis"])
        self.assertTrue(request["requires_new_decisionos_selection"])
        self.assertTrue(request["requires_new_actos_authorization"])
        self.assertTrue(request["requires_new_capability_lease"])
        self.assertTrue(request["same_transaction_execution_forbidden"])
        self.assertFalse(request["automatic_execution"])
        self.assertFalse(request["automatic_rollback"])


if __name__ == "__main__":
    unittest.main()
