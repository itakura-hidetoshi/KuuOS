from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Protocol

from runtime.kuuos_operational_agent_types_v1_1 import build_adapter_result, sha

ADAPTER_CONTRACT_VERSION = "kuuos_operational_agent_adapter_contract_v1_1"
OBSERVATION_VERSION = "kuuos_operational_agent_observation_v1_1"
VERIFICATION_VERSION = "kuuos_operational_agent_verification_v1_1"
LEARNING_VERSION = "kuuos_operational_agent_future_learning_v1_1"


class OperationalAdapter(Protocol):
    adapter_kind: str

    def stage(self, intent: Mapping[str, Any]) -> Mapping[str, Any]: ...


class Observer(Protocol):
    def observe(
        self, *, intent: Mapping[str, Any], adapter_result: Mapping[str, Any]
    ) -> Mapping[str, Any]: ...


class Verifier(Protocol):
    def verify(
        self,
        *,
        intent: Mapping[str, Any],
        adapter_result: Mapping[str, Any],
        observation: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...


class Learner(Protocol):
    def learn(
        self,
        *,
        intent: Mapping[str, Any],
        observation: Mapping[str, Any],
        verification: Mapping[str, Any],
    ) -> Mapping[str, Any]: ...


class DeterministicStagedAdapter:
    """Reference adapter with a strict staged-only effect ceiling."""

    adapter_kind = "DETERMINISTIC_STAGED"

    def stage(self, intent: Mapping[str, Any]) -> dict[str, Any]:
        packet = deepcopy(dict(intent))
        effect_digest = sha(
            {
                "kind": "staged_effect",
                "intent_digest": packet["intent_digest"],
                "operation": packet["operation"],
                "resource": packet["resource"],
                "payload_digest": packet["payload_digest"],
            }
        )
        # This is an adapter-produced trace only.  The controller never treats it as
        # the independent ObserveOS evidence used for verification.
        adapter_trace_digest = sha(
            {
                "kind": "adapter_trace",
                "effect_digest": effect_digest,
                "external_commit_performed": False,
            }
        )
        return build_adapter_result(
            adapter_kind=self.adapter_kind,
            intent_digest=str(packet["intent_digest"]),
            effect_digest=effect_digest,
            evidence_digest=adapter_trace_digest,
            staged=True,
        )


class DeterministicIndependentObserver:
    """Reference ObserveOS-side observer, distinct from the adapter."""

    observer_kind = "DETERMINISTIC_INDEPENDENT_OBSERVER"

    def observe(
        self, *, intent: Mapping[str, Any], adapter_result: Mapping[str, Any]
    ) -> dict[str, Any]:
        value = {
            "version": OBSERVATION_VERSION,
            "observer_kind": self.observer_kind,
            "intent_digest": str(intent["intent_digest"]),
            "effect_digest": str(adapter_result["effect_digest"]),
            "adapter_result_digest": str(adapter_result["adapter_result_digest"]),
            "independent_from_adapter": True,
            "external_commit_observed": False,
            "observation_digest": "",
        }
        value["observation_digest"] = sha(
            {key: item for key, item in value.items() if key != "observation_digest"}
        )
        return value


class DeterministicEvidenceVerifier:
    verifier_kind = "DETERMINISTIC_EVIDENCE_VERIFIER"

    def verify(
        self,
        *,
        intent: Mapping[str, Any],
        adapter_result: Mapping[str, Any],
        observation: Mapping[str, Any],
    ) -> dict[str, Any]:
        passed = (
            observation.get("independent_from_adapter") is True
            and observation.get("external_commit_observed") is False
            and observation.get("intent_digest") == intent.get("intent_digest")
            and observation.get("effect_digest") == adapter_result.get("effect_digest")
        )
        value = {
            "version": VERIFICATION_VERSION,
            "verifier_kind": self.verifier_kind,
            "observation_digest": str(observation.get("observation_digest", "")),
            "passed": passed,
            "truth_authority_granted": False,
            "root_rewrite_authority_granted": False,
            "verification_digest": "",
        }
        value["verification_digest"] = sha(
            {key: item for key, item in value.items() if key != "verification_digest"}
        )
        return value


class DeterministicFutureOnlyLearner:
    learner_kind = "DETERMINISTIC_FUTURE_ONLY_LEARNER"

    def learn(
        self,
        *,
        intent: Mapping[str, Any],
        observation: Mapping[str, Any],
        verification: Mapping[str, Any],
    ) -> dict[str, Any]:
        value = {
            "version": LEARNING_VERSION,
            "learner_kind": self.learner_kind,
            "intent_digest": str(intent["intent_digest"]),
            "observation_digest": str(observation["observation_digest"]),
            "verification_digest": str(verification["verification_digest"]),
            "future_only": True,
            "current_cycle_mutated": False,
            "learning_digest": "",
        }
        value["learning_digest"] = sha(
            {key: item for key, item in value.items() if key != "learning_digest"}
        )
        return value
