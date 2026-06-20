from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from runtime.kuuos_observation_belief_state_kernel_v0_21 import (
    apply_observation,
    build_initial_belief_state,
    mark_stale_claims,
    observation_digest,
    validate_belief_state,
)
from runtime.kuuos_observation_belief_state_scenarios_v0_21 import (
    _fixture,
    _observation,
    run_observation_belief_state_scenarios,
)
from runtime.kuuos_observation_belief_state_store_v0_21 import (
    apply_observation_persisted,
    initialize_belief_store,
    recover_belief_store,
)


class ObservationBeliefStateV021Tests(unittest.TestCase):
    def test_full_scenarios(self) -> None:
        result = run_observation_belief_state_scenarios()
        self.assertEqual(
            "KUUOS_OBSERVATION_BELIEF_STATE_V0_21_OK", result["status"]
        )
        self.assertTrue(result["unknown_status_preserved"])
        self.assertTrue(result["stale_status_produced"])
        self.assertFalse(result["truth_authority_granted"])

    def test_unknown_does_not_create_negative_evidence(self) -> None:
        contract, mission_state = _fixture()
        state = build_initial_belief_state(
            contract=contract,
            mission_state=mission_state,
            chart_id="github-main",
            now_ms=2,
        )
        unknown = _observation(
            contract,
            mission_state,
            observation_id="unknown-only",
            claim_id="release-ready",
            proposition="The release is ready",
            relation="unknown",
            observed_at_ms=3,
            valid_until_ms=100,
            confidence=0.0,
        )
        state = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=state,
            observation=unknown,
        )["result_state"]
        claim = state["claims"]["release-ready"]
        self.assertEqual("unknown", claim["status"])
        self.assertEqual([], claim["oppose_evidence_digests"])
        self.assertEqual([], validate_belief_state(state, contract, mission_state))

    def test_contradiction_and_staleness_remain_visible(self) -> None:
        contract, mission_state = _fixture()
        state = build_initial_belief_state(
            contract=contract,
            mission_state=mission_state,
            chart_id="github-main",
            now_ms=2,
        )
        for relation, observation_id in (("supports", "support"), ("opposes", "oppose")):
            observation = _observation(
                contract,
                mission_state,
                observation_id=observation_id,
                claim_id="ci-green",
                proposition="CI is green",
                relation=relation,
                observed_at_ms=3 if relation == "supports" else 4,
                valid_until_ms=100,
                confidence=0.9,
            )
            state = apply_observation(
                contract=contract,
                mission_state=mission_state,
                belief_state=state,
                observation=observation,
            )["result_state"]
        self.assertEqual("contradicted", state["claims"]["ci-green"]["status"])
        self.assertEqual(1, len(state["contradiction_residues"]))

        short = _observation(
            contract,
            mission_state,
            observation_id="short-lived",
            claim_id="dependency-fresh",
            proposition="Dependency is fresh",
            relation="supports",
            observed_at_ms=5,
            valid_until_ms=6,
            confidence=0.8,
        )
        state = apply_observation(
            contract=contract,
            mission_state=mission_state,
            belief_state=state,
            observation=short,
        )["result_state"]
        stale = mark_stale_claims(
            contract=contract,
            mission_state=mission_state,
            belief_state=state,
            now_ms=7,
        )["result_state"]
        claim = stale["claims"]["dependency-fresh"]
        self.assertEqual("stale", claim["status"])
        self.assertEqual("observed_positive", claim["prior_status"])

    def test_store_replay_and_explicit_snapshot_repair(self) -> None:
        contract, mission_state = _fixture()
        with TemporaryDirectory() as directory:
            initialize_belief_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                chart_id="github-main",
                now_ms=2,
            )
            observation = _observation(
                contract,
                mission_state,
                observation_id="persisted",
                claim_id="ci-green",
                proposition="CI is green",
                relation="supports",
                observed_at_ms=3,
                valid_until_ms=100,
                confidence=0.9,
            )
            first = apply_observation_persisted(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                observation=observation,
            )
            replay = apply_observation_persisted(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                observation=observation,
            )
            self.assertEqual("APPLIED", first["status"])
            self.assertEqual("REPLAYED", replay["status"])
            self.assertEqual(
                1,
                len(
                    (Path(directory) / "observation-ledger.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ),
            )
            (Path(directory) / "snapshot.json").write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "snapshot_ledger_mismatch"):
                recover_belief_store(
                    store_dir=directory,
                    contract=contract,
                    mission_state=mission_state,
                )
            repaired = recover_belief_store(
                store_dir=directory,
                contract=contract,
                mission_state=mission_state,
                repair_snapshot=True,
            )
            self.assertEqual(
                first["result_state"]["observation_belief_state_digest"],
                repaired["observation_belief_state_digest"],
            )

    def test_chart_and_mission_binding_fail_closed(self) -> None:
        contract, mission_state = _fixture()
        state = build_initial_belief_state(
            contract=contract,
            mission_state=mission_state,
            chart_id="github-main",
            now_ms=2,
        )
        observation = _observation(
            contract,
            mission_state,
            observation_id="wrong-chart",
            claim_id="ci-green",
            proposition="CI is green",
            relation="supports",
            observed_at_ms=3,
            valid_until_ms=100,
            confidence=0.9,
        )
        wrong_chart = deepcopy(observation)
        wrong_chart["chart_id"] = "another-chart"
        wrong_chart["observation_digest"] = ""
        wrong_chart["observation_digest"] = observation_digest(wrong_chart)
        with self.assertRaisesRegex(ValueError, "observation_chart_mismatch"):
            apply_observation(
                contract=contract,
                mission_state=mission_state,
                belief_state=state,
                observation=wrong_chart,
            )


if __name__ == "__main__":
    unittest.main()
