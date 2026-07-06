#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import command_digest, valid_digest
from runtime.kuuos_causal_world_model_os_v14_0 import build_kuuos_causal_world_model_os_v14_0

WORLD_ID = "FormalResearchWorld"
PROCESS_CONTEXT = {
    "process_tensor_digest": "hamiltonian-handoff-process-v14-digest",
    "memory_kernel_digest": "hamiltonian-handoff-memory-v14-digest",
    "history_window_digest": "hamiltonian-handoff-history-v14-digest",
    "instrument_trace_digest": "hamiltonian-handoff-instrument-v14-digest",
    "non_markov_context_digest": "hamiltonian-handoff-non-markov-v14-digest",
}
VARIABLES = [
    "HamiltonianLabelAPI",
    "HPhysLabel",
    "HamiltonianSpectralWitnessLink",
    "HamiltonianOperatorNormalizationAPI",
    "VacuumOrthogonalClosedHamiltonianAPI",
    "HamiltonianRayleighLowerBoundAPI",
    "HamiltonianSelfAdjointnessBoundary",
    "HamiltonianSpectralGapBoundary",
    "PhysicalMassGapClaimBoundary",
]
PROTECTED_VARIABLES = [
    "HamiltonianSelfAdjointnessBoundary",
    "HamiltonianSpectralGapBoundary",
    "PhysicalMassGapClaimBoundary",
]


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def command(kind: str, transaction_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    value: dict[str, Any] = {
        "version": "kuuos_causal_world_model_command_v14_0",
        "kind": kind,
        "transaction_id": transaction_id,
        "world_id": WORLD_ID,
        "payload": payload,
        "process_tensor_context": dict(PROCESS_CONTEXT),
    }
    value["command_digest"] = command_digest(value)
    return value


def license_packet(cmd: dict[str, Any]) -> dict[str, Any]:
    return {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "bound_command_digest": cmd["command_digest"],
        "allowed_command_kinds": ["initialize", "observe", "intervene", "undo", "counterfactual", "inspect"],
        "allowed_variables": list(VARIABLES),
        "protected_variables": list(PROTECTED_VARIABLES),
        "max_variables": 16,
        "max_mechanisms": 16,
        "state_read_allowed": True,
        "state_write_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "snapshot_write_allowed": True,
        "snapshot_read_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "initialize_allowed": True,
        "observation_update_allowed": True,
        "intervention_allowed": True,
        "undo_allowed": True,
        "counterfactual_allowed": True,
        "inspect_allowed": True,
    }


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "kuuos_causal_world_model_os_v14_0_enabled": True,
        "apply_kuuos_causal_world_model_os_v14_0": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, cmd: dict[str, Any]) -> dict[str, Any]:
    return build_kuuos_causal_world_model_os_v14_0(
        runtime_context=context(root),
        command=cmd,
        license_packet=license_packet(cmd),
    ).to_dict()


def initialize_command() -> dict[str, Any]:
    return command(
        "initialize",
        "txHamiltonianHandoffInit",
        {
            "variables": {
                "HamiltonianLabelAPI": {
                    "value": "present",
                    "uncertainty": 0.0,
                    "unit": "formal-hamiltonian-label-api",
                    "provenance": ["MGAP4D.Hamiltonian.Basic.HamiltonianLabel"],
                },
                "HPhysLabel": {
                    "value": "H_phys",
                    "uncertainty": 0.0,
                    "unit": "formal-hamiltonian-label",
                    "provenance": ["MGAP4D.Hamiltonian.Basic.Hphys"],
                },
                "HamiltonianSpectralWitnessLink": {
                    "value": "present",
                    "uncertainty": 0.0,
                    "unit": "formal-spectral-witness-link",
                    "provenance": [
                        "MGAP4D.Hamiltonian.Physical.physicalGap3320Record",
                        "MGAP4D.Hamiltonian.Physical.physicalGap3320_value",
                    ],
                },
                "HamiltonianOperatorNormalizationAPI": {
                    "value": "present",
                    "uncertainty": 0.0,
                    "unit": "formal-operator-normalization-api",
                    "provenance": ["PhysicalHamiltonianOperatorNormalizationData"],
                },
                "VacuumOrthogonalClosedHamiltonianAPI": {
                    "value": "conditional-present",
                    "uncertainty": 0.0,
                    "unit": "formal-closed-operator-api",
                    "provenance": ["vacuumOrthogonalClosedRightHamiltonian"],
                },
                "HamiltonianRayleighLowerBoundAPI": {
                    "value": "conditional-present",
                    "uncertainty": 0.0,
                    "unit": "formal-rayleigh-lower-bound-api",
                    "provenance": ["FiniteVolumeVacuumGapTransfer.vacuumOrthogonalClosedRightHamiltonian_gap"],
                },
                "HamiltonianSelfAdjointnessBoundary": {
                    "value": "conditional-on-formal-adjoint-input",
                    "uncertainty": 0.0,
                    "unit": "non-claim-boundary",
                    "provenance": ["vacuumOrthogonalClosedRightHamiltonian_isFormalAdjoint"],
                },
                "HamiltonianSpectralGapBoundary": {
                    "value": "witness-surface-not-external-consensus",
                    "uncertainty": 0.0,
                    "unit": "non-claim-boundary",
                    "provenance": ["physicalGap3320_value"],
                },
                "PhysicalMassGapClaimBoundary": {
                    "value": "not-established-as-external-consensus",
                    "uncertainty": 0.0,
                    "unit": "non-claim-boundary",
                    "provenance": ["4d-mass-gap:README-non-claims"],
                },
            },
            "mechanisms": {},
        },
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory) / "hamiltonian_handoff_world"
        state_path = root / "kuuos_causal_world_model_state_v14_0.json"

        init = initialize_command()
        result = run(root, init)
        assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
        assert result["state_mutated"] is True
        assert result["revision"] == 1

        state = read_json(state_path)
        assert valid_digest(state, "world_model_digest")
        assert state["world_id"] == WORLD_ID
        assert state["variables"]["HamiltonianLabelAPI"]["value"] == "present"
        assert state["variables"]["HPhysLabel"]["value"] == "H_phys"
        assert state["variables"]["HamiltonianSpectralWitnessLink"]["value"] == "present"
        assert state["variables"]["HamiltonianOperatorNormalizationAPI"]["value"] == "present"
        assert state["variables"]["VacuumOrthogonalClosedHamiltonianAPI"]["value"] == "conditional-present"
        assert state["variables"]["HamiltonianRayleighLowerBoundAPI"]["value"] == "conditional-present"
        assert state["variables"]["HamiltonianSelfAdjointnessBoundary"]["value"] == "conditional-on-formal-adjoint-input"
        assert state["variables"]["HamiltonianSpectralGapBoundary"]["value"] == "witness-surface-not-external-consensus"
        assert state["variables"]["PhysicalMassGapClaimBoundary"]["value"] == "not-established-as-external-consensus"
        assert state["boundary"]["world_model_state_not_truth_authority"] is True

        inspect = command("inspect", "txHamiltonianHandoffInspect", {})
        inspect_result = run(root, inspect)
        assert inspect_result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", inspect_result
        written = read_json(root / "kuuos_causal_world_model_results_v14_0" / "txHamiltonianHandoffInspect.json")
        variables = written["operation_result"]["variables"]
        assert variables["HPhysLabel"]["unit"] == "formal-hamiltonian-label"
        assert variables["HamiltonianOperatorNormalizationAPI"]["unit"] == "formal-operator-normalization-api"

        blocked = command(
            "observe",
            "txHamiltonianBoundaryOverwrite",
            {"values": {"HamiltonianSpectralGapBoundary": "external-consensus-established"}},
        )
        blocked_result = run(root, blocked)
        assert blocked_result["status"].endswith("BLOCKED"), blocked_result
        assert "causal_world_model_protected_variable_mutation" in blocked_result["blockers"]
        assert read_json(state_path)["variables"]["HamiltonianSpectralGapBoundary"]["value"] == "witness-surface-not-external-consensus"

    print("KuuOS WORLD Hamiltonian handoff bridge v14.0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
