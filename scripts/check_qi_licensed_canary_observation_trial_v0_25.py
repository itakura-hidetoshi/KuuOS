#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import tempfile

from qi_licensed_canary_observation_trial_fixtures_v0_25 import *

def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(
            root, "bounded_canary_observation_proposal_ready", "ready"
        )
        assert result.status == READY
        assert result.decision == "licensed_canary_observation_trial_ready"
        summary = json.loads(
            (root / "indra_qi_licensed_canary_observation_trial_summary_v0_25.json").read_text()
        )
        recommendation = json.loads(
            (root / "indra_qi_licensed_canary_observation_trial_recommendation_v0_25.json").read_text()
        )
        assert summary["observation_copy_trial_completed"] is True
        assert summary["live_canary_activated"] is False
        assert summary["live_response_influenced"] is False
        assert recommendation["direct_live_canary_activation_authority"] is False
        replay = build_licensed_canary_observation_trial(
            runtime_context=context(root),
            canary_trial_plan=plan_value,
            canary_trial_license=license_value(plan_value, report_value, source),
            canary_trial_report=report_value,
        )
        assert replay.status == BLOCKED
        assert "canary_trial_replay_detected" in replay.blockers

    for mode, expected in (
        ("fraction", "redesign_canary_observation_trial_recommended"),
        ("duration", "redesign_canary_observation_trial_recommended"),
        ("budget", "redesign_canary_observation_trial_recommended"),
        ("missing-minority", "restore_shadow_diversity_recommended"),
        ("unfair", "restore_shadow_diversity_recommended"),
        ("latency", "redesign_canary_observation_trial_recommended"),
        ("divergence", "redesign_canary_observation_trial_recommended"),
        ("redaction", "redesign_canary_observation_trial_recommended"),
        ("nondeterministic", "redesign_canary_observation_trial_recommended"),
        ("rollback", "redesign_canary_observation_trial_recommended"),
        ("revocation", "redesign_canary_observation_trial_recommended"),
        ("restore", "redesign_canary_observation_trial_recommended"),
        ("live", "quarantine_recommended"),
        ("activate", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(
                pathlib.Path(directory), "bounded_canary_observation_proposal_ready", mode
            )
            assert result.status == READY
            assert result.decision == expected, (mode, result)

    for source_decision, expected in (
        ("hold_for_observation", "hold_for_observation"),
        ("extend_mirror_observation_recommended", "extend_mirror_observation_recommended"),
        (
            "redesign_bounded_canary_observation_proposal_recommended",
            "redesign_canary_observation_trial_recommended",
        ),
        ("restore_shadow_diversity_recommended", "restore_shadow_diversity_recommended"),
        ("rollback_recommended", "rollback_recommended"),
        ("quarantine_recommended", "quarantine_recommended"),
    ):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, "ready")
            assert result.status == READY
            assert result.decision == expected

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "bounded_canary_observation_proposal_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value["trial_events"][0]["replica_restored"] = False
        result = build_licensed_canary_observation_trial(
            runtime_context=context(root),
            canary_trial_plan=plan_value,
            canary_trial_license=license_value(plan_value, report_value, source),
            canary_trial_report=report_value,
        )
        assert result.status == BLOCKED
        assert "canary_trial_report_digest_invalid" in result.blockers

    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, "bounded_canary_observation_proposal_ready")
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source["world"]["world_model_id"] = "tampered"
        write(root / "ku_indra_qi_noncommutative_mandala_world_state.json", source["world"])
        result = build_licensed_canary_observation_trial(
            runtime_context=context(root),
            canary_trial_plan=plan_value,
            canary_trial_license=license_value(plan_value, report_value, source),
            canary_trial_report=report_value,
        )
        assert result.status == BLOCKED
        assert "canary_trial_source_world_invalid" in result.blockers

    manifest = json.loads(
        (ROOT / "manifests/qi_licensed_canary_observation_trial_v0_25.json").read_text()
    )
    assert manifest["status"] == "READY"
    for group in ("runtime", "scripts", "docs", "example"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print("qi_licensed_canary_observation_trial_v0_25 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
