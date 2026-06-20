from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from runtime.kuuos_mission_contract_types_v0_20 import (
    build_authority_scope,
    build_evidence_policy,
    build_goal_policy,
    build_mission_contract,
    build_override_policy,
    build_renewal_policy,
    build_resource_envelope,
    sha,
)
from runtime.kuuos_mission_state_v0_20 import build_initial_mission_state
from runtime.kuuos_observation_belief_state_kernel_v0_21 import (
    apply_observation,
    build_observation,
    mark_stale_claims,
    observation_digest,
    state_digest,
    validate_belief_state,
)
from runtime.kuuos_observation_belief_state_store_v0_21 import (
    apply_observation_persisted,
    initialize_belief_store,
    recover_belief_store,
)


def _fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    contract = build_mission_contract(
        mission_id="mission-observation-belief-v021",
        lineage_id="lineage-observation-belief-v021",
        revision=0,
        parent_contract_digest="",
        issuer_id="owner-1",
        issuer_role="owner",
        governance_root_digest="governance-root-v021",
        purpose="Maintain an evidence-bound local belief state",
        success_criteria=["belief_state_is_provenance_bound"],
        failure_criteria=["unknown_collapses_to_false"],
        invariants=[
            "unknown_is_not_false",
            "contradiction_remains_visible",
            "belief_is_not_truth_authority",
        ],
        prohibited_outcomes=["unlicensed_effect", "memory_overwrite"],
        resource_envelope=build_resource_envelope(
            max_total_cost=100.0,
            max_cycle_cost=10.0,
            max_cycles_before_renewal=10,
            max_active_goals=3,
            max_goal_count=6,
            reserve_floor=5.0,
        ),
        authority_scope=build_authority_scope(
            domain_scope=["software_runtime"],
            requested_capabilities=["observe.read"],
        ),
        renewal_policy=build_renewal_policy(
            max_renewals=2,
            renewal_window_ms=1_000,
            authorized_roles=["owner"],
        ),
        override_policy=build_override_policy(
            {
                "owner": [
                    "pause",
                    "resume",
                    "terminate",
                    "handover",
                    "request_renewal",
                    "renew",
                ]
            }
        ),
        evidence_policy=build_evidence_policy(
            completion_roles=["verifier"],
            failure_roles=["verifier"],
            invariant_roles=["verifier"],
            minimum_confidence=0.8,
        ),
        goal_policy=build_goal_policy(plurality_floor=0.05),
        created_at_ms=0,
        valid_from_ms=0,
        expires_at_ms=100_000,
    )
    return contract, build_initial_mission_state(contract, now_ms=1)


def _observation(
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    *,
    observation_id: str,
    claim_id: str,
    proposition: str,
    relation: str,
    observed_at_ms: int,
    valid_until_ms: int,
    confidence: float,
) -> dict[str, Any]:
    return build_observation(
        contract=contract,
        mission_state=mission_state,
        observation_id=observation_id,
        chart_id="github-main",
        claim_id=claim_id,
        proposition=proposition,
        relation=relation,
        source_id=f"source-{observation_id}",
        source_kind="system",
        raw_artifact_digest=sha({"observation_id": observation_id}),
        provenance_digests=[
            sha({"source": observation_id}),
            sha({"collector": "github-adapter"}),
        ],
        observed_at_ms=observed_at_ms,
        valid_until_ms=valid_until_ms,
        confidence=confidence,
    )


def run_observation_belief_state_scenarios() -> dict[str, Any]:
    contract, mission_state = _fixture()
    with TemporaryDirectory(prefix="kuuos-observation-belief-v021-") as directory:
        state = initialize_belief_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            chart_id="github-main",
            now_ms=2,
        )
        positive = _observation(
            contract,
            mission_state,
            observation_id="obs-positive",
            claim_id="ci-green",
            proposition="The dedicated CI is green",
            relation="supports",
            observed_at_ms=10,
            valid_until_ms=1_000,
            confidence=0.95,
        )
        result = apply_observation_persisted(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            observation=positive,
        )
        assert result["status"] == "APPLIED"
        state = result["result_state"]
        assert state["claims"]["ci-green"]["status"] == "observed_positive"

        replay = apply_observation_persisted(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            observation=positive,
        )
        assert replay["status"] == "REPLAYED"

        opposing = _observation(
            contract,
            mission_state,
            observation_id="obs-opposing",
            claim_id="ci-green",
            proposition="The dedicated CI is green",
            relation="opposes",
            observed_at_ms=12,
            valid_until_ms=1_000,
            confidence=0.9,
        )
        result = apply_observation_persisted(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            observation=opposing,
        )
        state = result["result_state"]
        assert state["claims"]["ci-green"]["status"] == "contradicted"
        assert len(state["contradiction_residues"]) == 1

        unknown = _observation(
            contract,
            mission_state,
            observation_id="obs-unknown",
            claim_id="deployment-ready",
            proposition="The deployment is ready",
            relation="unknown",
            observed_at_ms=13,
            valid_until_ms=1_000,
            confidence=0.0,
        )
        result = apply_observation_persisted(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            observation=unknown,
        )
        state = result["result_state"]
        claim = state["claims"]["deployment-ready"]
        assert claim["status"] == "unknown"
        assert claim["oppose_evidence_digests"] == []

        expiring = _observation(
            contract,
            mission_state,
            observation_id="obs-expiring",
            claim_id="dependency-fresh",
            proposition="The dependency snapshot is fresh",
            relation="supports",
            observed_at_ms=14,
            valid_until_ms=20,
            confidence=0.8,
        )
        result = apply_observation_persisted(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            observation=expiring,
        )
        state = result["result_state"]
        stale = mark_stale_claims(
            contract=contract,
            mission_state=mission_state,
            belief_state=state,
            now_ms=100,
        )
        assert stale["status"] == "STALE_APPLIED"
        stale_state = stale["result_state"]
        assert stale_state["claims"]["dependency-fresh"]["status"] == "stale"
        assert stale_state["claims"]["dependency-fresh"]["prior_status"] == "observed_positive"
        assert len(stale_state["staleness_residues"]) == 1

        recovered = recover_belief_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
        )
        assert recovered == state
        ledger_lines = (
            Path(directory) / "observation-ledger.jsonl"
        ).read_text(encoding="utf-8").splitlines()
        assert len(ledger_lines) == 4

        tampered = deepcopy(state)
        tampered["non_authority"]["grants_truth_authority"] = True
        tampered["observation_belief_state_digest"] = ""
        tampered["observation_belief_state_digest"] = state_digest(tampered)
        assert "belief_state_non_authority_invalid" in validate_belief_state(
            tampered, contract, mission_state
        )

        stale_event = deepcopy(positive)
        stale_event["source_mission_state_digest"] = "0" * 64
        stale_event["observation_digest"] = ""
        stale_event["observation_digest"] = observation_digest(stale_event)
        try:
            apply_observation(
                contract=contract,
                mission_state=mission_state,
                belief_state=state,
                observation=stale_event,
            )
            raise AssertionError("stale mission-state observation must fail")
        except ValueError as exc:
            assert "observation_mission_state_stale" in str(exc)

        return {
            "status": "KUUOS_OBSERVATION_BELIEF_STATE_V0_21_OK",
            "belief_state_digest": state["observation_belief_state_digest"],
            "revision": state["revision"],
            "claim_count": len(state["claims"]),
            "observation_count": len(state["observation_history"]),
            "contradiction_count": len(state["contradiction_residues"]),
            "unknown_status_preserved": claim["status"] == "unknown",
            "stale_status_produced": (
                stale_state["claims"]["dependency-fresh"]["status"] == "stale"
            ),
            "truth_authority_granted": False,
        }


__all__ = ["run_observation_belief_state_scenarios"]
