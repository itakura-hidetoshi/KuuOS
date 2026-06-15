from __future__ import annotations
import json
import pathlib
import sys
import tempfile
from typing import Any, Mapping
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runtime.kuuos_indra_qi_longitudinal_mirror_noninterference_core_v0_23 import LICENSE_VERSION, PLAN_VERSION, REPORT_VERSION, REQUIRED_BOUNDARY, cycle_digest, plan_digest, report_digest, sha
from runtime.kuuos_indra_qi_longitudinal_mirror_noninterference_runtime_v0_23 import BLOCKED, READY, build_longitudinal_mirror_noninterference

def write(path: pathlib.Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(dict(value), ensure_ascii=False, sort_keys=True), encoding='utf-8')

def sources(root: pathlib.Path, decision: str) -> dict[str, Any]:
    world = {'version': 'indra_qi_world_model_v0_1', 'world_model_id': 'world-a', 'mandala_inclusion': {'multi_world_noncollapse': True, 'single_ontology_forced': False}, 'epoch': 1}
    world['indra_qi_world_state_digest'] = sha(world)
    analysis = {'mirror_event_count': 12, 'capture_fraction': 0.1, 'source_allocation': {'l0': 0.34, 'l1': 0.33, 'l2': 0.33}, 'mirror_allocation': {'l0': 0.34, 'l1': 0.33, 'l2': 0.33}, 'maximum_allocation_drift': 0.01, 'schedule_agreement_ratio': 1.0, 'source_jain_fairness_index': 1.0, 'mirror_jain_fairness_index': 0.99, 'fairness_preservation_ratio': 0.99, 'maximum_latency_delta_ratio': 0.05, 'maximum_output_divergence_score': 0.02, 'redaction_failure_ratio': 0.0, 'live_response_influence_ratio': 0.0, 'mirror_delivery_failure_ratio': 0.0, 'boundary_breach_count': 0, 'mirror_events': [], 'diversity_gates': {}, 'mirror_gates': {}, 'all_gates': {}}
    summary = {'version': 'indra_qi_licensed_mirror_observation_admission_summary_v0_22', 'mirror_program_id': 'mirror-program-a', 'mirror_admission_id': 'mirror-admission-3', 'world_model_id': 'world-a', 'source_dry_run_decision': 'plural_routing_dry_run_ready', 'source_world_state_digest': world['indra_qi_world_state_digest'], 'source_dry_run_summary_digest': sha({'dry-summary': 1}), 'source_dry_run_state_digest': sha({'dry-state': 1}), 'source_dry_run_recommendation_digest': sha({'dry-rec': 1}), 'mirror_observation_report_digest': sha({'mirror-report': 3}), 'mirror_analysis': analysis, 'raw_payload_stored': False, 'live_response_influenced': False, 'feedback_to_live_path_enabled': False, 'routing_activated': False, 'winner_selected': False, 'external_actuation_enabled': False, 'world_update_enabled': False, 'recommendation_only': True, 'epoch': 30}
    summary['mirror_observation_summary_digest'] = sha(summary)
    state = {'version': 'indra_qi_licensed_mirror_observation_admission_state_v0_22', 'mirror_program_id': 'mirror-program-a', 'world_model_id': 'world-a', 'last_mirror_admission_id': 'mirror-admission-3', 'latest_mirror_observation_decision': decision, 'latest_mirror_observation_summary_digest': summary['mirror_observation_summary_digest'], 'epoch': 31}
    state['mirror_observation_state_digest'] = sha(state)
    recommendation = {'version': 'indra_qi_licensed_mirror_observation_admission_recommendation_v0_22', 'mirror_program_id': 'mirror-program-a', 'mirror_admission_id': 'mirror-admission-3', 'world_model_id': 'world-a', 'source_dry_run_decision': 'plural_routing_dry_run_ready', 'decision': decision, 'decision_reasons': ['test'], 'mirror_admission_ready': decision == 'mirror_observation_admission_ready', 'live_response_influenced': False, 'routing_activated': False, 'winner_selected': False, 'mirror_observation_summary_digest': summary['mirror_observation_summary_digest'], 'mirror_analysis': analysis, 'source_world_state_digest': world['indra_qi_world_state_digest'], 'recommendation_only': True, 'mirror_observation_not_live_intervention': True, 'direct_live_response_influence_authority': False, 'direct_feedback_to_live_path_authority': False, 'direct_routing_activation_authority': False, 'direct_winner_selection_authority': False, 'direct_lineage_selection_authority': False, 'direct_lineage_execution_authority': False, 'direct_world_update_authority': False, 'direct_external_actuation_authority': False, 'direct_promotion_authority': False, 'direct_rollback_authority': False, 'direct_quarantine_authority': False, 'truth_authority': False, 'epoch': 31}
    recommendation['mirror_observation_recommendation_digest'] = sha(recommendation)
    write(root / 'ku_indra_qi_noncommutative_mandala_world_state.json', world)
    write(root / 'indra_qi_licensed_mirror_observation_admission_summary_v0_22.json', summary)
    write(root / 'indra_qi_licensed_mirror_observation_admission_state_v0_22.json', state)
    write(root / 'indra_qi_licensed_mirror_observation_admission_recommendation_v0_22.json', recommendation)
    return {'world': world, 'summary': summary, 'state': state, 'recommendation': recommendation}

def plan(source: Mapping[str, Any], run_id: str='longitudinal-mirror-run-a') -> dict[str, Any]:
    value = {'version': PLAN_VERSION, 'evidence_program_id': 'longitudinal-mirror-program-a', 'evidence_run_id': run_id, 'world_model_id': 'world-a', 'expected_source_world_state_digest': source['world']['indra_qi_world_state_digest'], 'expected_mirror_summary_digest': source['summary']['mirror_observation_summary_digest'], 'expected_source_mirror_state_digest': source['state']['mirror_observation_state_digest'], 'expected_source_mirror_recommendation_digest': source['recommendation']['mirror_observation_recommendation_digest'], 'evidence_policy': {'minimum_evidence_cycles': 3, 'maximum_evidence_cycles': 12, 'maximum_mean_latency_delta_ratio': 0.2, 'maximum_cumulative_latency_delta_ratio': 0.5, 'maximum_mean_output_divergence_score': 0.1, 'maximum_cumulative_output_divergence_score': 0.25, 'maximum_mean_allocation_drift': 0.1, 'maximum_fairness_decay': 0.1, 'minimum_schedule_agreement_ratio': 1.0, 'minimum_fairness_preservation_ratio': 0.8, 'maximum_redaction_failure_ratio': 0.0, 'maximum_live_response_influence_ratio': 0.0, 'maximum_mirror_delivery_failure_ratio': 0.0, 'minimum_replica_restore_ratio': 1.0, 'minimum_deterministic_replay_ratio': 1.0, 'require_cycle_chain': True, 'require_monotonic_cycle_index': True, 'require_monotonic_epoch': True, 'require_raw_payload_absent': True, 'require_live_response_unchanged': True, 'require_feedback_to_live_path_disabled': True, 'require_routing_activation_disabled': True, 'require_external_actuation_disabled': True, 'require_world_update_disabled': True, 'require_policy_boundary_preserved': True}, 'boundary': dict(REQUIRED_BOUNDARY)}
    value['longitudinal_mirror_plan_digest'] = plan_digest(value)
    return value

def cycle(index: int, source: Mapping[str, Any], previous: str, *, mode: str='ready') -> dict[str, Any]:
    latency = 0.05 + 0.01 * (index - 1)
    divergence = 0.02 + 0.005 * (index - 1)
    allocation = 0.01
    fairness = 0.99
    influence = 0.0
    raw_payload = False
    feedback = False
    routing = False
    if mode == 'latency':
        latency = 0.3
    elif mode == 'divergence':
        divergence = 0.15
    elif mode == 'fairness':
        fairness = 0.7 if index == 3 else 0.99
        allocation = 0.2 if index == 3 else 0.01
    elif mode == 'live':
        influence = 1.0 if index == 2 else 0.0
        feedback = index == 2
    value = {'cycle_index': index, 'mirror_admission_id': f'mirror-admission-{index}', 'source_mirror_summary_digest': source['summary']['mirror_observation_summary_digest'] if index == 3 else sha({'mirror-summary': index}), 'latency_delta_ratio': latency, 'output_divergence_score': divergence, 'allocation_drift': allocation, 'schedule_agreement_ratio': 1.0, 'fairness_preservation_ratio': fairness, 'redaction_failure_ratio': 0.0, 'live_response_influence_ratio': influence, 'mirror_delivery_failure_ratio': 0.0, 'replica_restore_ratio': 1.0, 'deterministic_replay_ratio': 1.0, 'raw_payload_stored': raw_payload, 'live_response_influenced': influence > 0, 'feedback_to_live_path_enabled': feedback, 'routing_activated': routing, 'external_actuation_enabled': False, 'world_update_enabled': False, 'winner_selected': False, 'policy_boundary_preserved': True, 'prev_mirror_cycle_digest': previous, 'epoch': 100 + index}
    value['mirror_cycle_digest'] = cycle_digest(value)
    return value

def report(plan_value: Mapping[str, Any], source: Mapping[str, Any], mode: str='ready') -> dict[str, Any]:
    cycles: list[dict[str, Any]] = []
    previous = 'GENESIS'
    for index in range(1, 4):
        current = cycle(index, source, previous, mode=mode)
        cycles.append(current)
        previous = current['mirror_cycle_digest']
    value = {'version': REPORT_VERSION, 'evidence_run_id': plan_value['evidence_run_id'], 'latest_mirror_summary_digest': source['summary']['mirror_observation_summary_digest'], 'cycles': cycles}
    value['longitudinal_mirror_report_digest'] = report_digest(value)
    return value

def license_value(plan_value: Mapping[str, Any], report_value: Mapping[str, Any], source: Mapping[str, Any]) -> dict[str, Any]:
    return {'version': LICENSE_VERSION, 'license_id': 'license-' + str(plan_value['evidence_run_id']), 'bound_longitudinal_mirror_plan_digest': plan_value['longitudinal_mirror_plan_digest'], 'bound_longitudinal_mirror_report_digest': report_value['longitudinal_mirror_report_digest'], 'bound_source_world_state_digest': source['world']['indra_qi_world_state_digest'], 'bound_mirror_summary_digest': source['summary']['mirror_observation_summary_digest'], 'bound_source_mirror_state_digest': source['state']['mirror_observation_state_digest'], 'bound_source_mirror_recommendation_digest': source['recommendation']['mirror_observation_recommendation_digest'], 'state_write_allowed': True, 'summary_write_allowed': True, 'ledger_append_allowed': True, 'recommendation_write_allowed': True, 'receipt_write_allowed': True, 'audit_append_allowed': True, 'live_response_influence_authority_granted': False, 'feedback_to_live_path_authority_granted': False, 'routing_activation_authority_granted': False, 'winner_selection_authority_granted': False, 'external_actuation_authority_granted': False, 'world_update_authority_granted': False, 'lineage_selection_authority_granted': False, 'lineage_execution_authority_granted': False, 'truth_authority_granted': False, 'direct_promotion_authority_granted': False, 'direct_rollback_authority_granted': False, 'direct_quarantine_authority_granted': False}

def context(root: pathlib.Path) -> dict[str, Any]:
    return {'runtime_root': str(root), 'indra_qi_longitudinal_mirror_noninterference_v0_23_enabled': True, 'apply_indra_qi_longitudinal_mirror_noninterference_v0_23': True}

def execute(root: pathlib.Path, source_decision: str, mode: str='ready'):
    source = sources(root, source_decision)
    plan_value = plan(source)
    report_value = report(plan_value, source, mode)
    names = ('ku_indra_qi_noncommutative_mandala_world_state.json', 'indra_qi_licensed_mirror_observation_admission_summary_v0_22.json', 'indra_qi_licensed_mirror_observation_admission_state_v0_22.json', 'indra_qi_licensed_mirror_observation_admission_recommendation_v0_22.json')
    before = {name: (root / name).read_bytes() for name in names}
    result = build_longitudinal_mirror_noninterference(runtime_context=context(root), longitudinal_mirror_plan=plan_value, longitudinal_mirror_license=license_value(plan_value, report_value, source), longitudinal_mirror_report=report_value)
    after = {name: (root / name).read_bytes() for name in names}
    assert before == after
    return (source, plan_value, report_value, result)

def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source, plan_value, report_value, result = execute(root, 'mirror_observation_admission_ready', 'ready')
        assert result.status == READY
        assert result.decision == 'longitudinal_mirror_noninterference_ready'
        summary = json.loads((root / 'indra_qi_longitudinal_mirror_noninterference_summary_v0_23.json').read_text())
        recommendation = json.loads((root / 'indra_qi_longitudinal_mirror_noninterference_recommendation_v0_23.json').read_text())
        assert summary['raw_payload_stored'] is False
        assert summary['live_response_influenced'] is False
        assert recommendation['direct_live_response_influence_authority'] is False
        replay = build_longitudinal_mirror_noninterference(runtime_context=context(root), longitudinal_mirror_plan=plan_value, longitudinal_mirror_license=license_value(plan_value, report_value, source), longitudinal_mirror_report=report_value)
        assert replay.status == BLOCKED
        assert 'longitudinal_mirror_replay_detected' in replay.blockers
    for mode, expected in (('latency', 'redesign_longitudinal_mirror_observation_recommended'), ('divergence', 'redesign_longitudinal_mirror_observation_recommended'), ('fairness', 'restore_shadow_diversity_recommended'), ('live', 'quarantine_recommended')):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), 'mirror_observation_admission_ready', mode)
            assert result.status == READY
            assert result.decision == expected, (mode, result)
    for source_decision, expected in (('hold_for_observation', 'hold_for_observation'), ('redesign_mirror_observation_admission_recommended', 'redesign_longitudinal_mirror_observation_recommended'), ('extend_longitudinal_observation_recommended', 'extend_mirror_observation_recommended'), ('restore_shadow_diversity_recommended', 'restore_shadow_diversity_recommended'), ('rollback_recommended', 'rollback_recommended'), ('quarantine_recommended', 'quarantine_recommended')):
        with tempfile.TemporaryDirectory() as directory:
            _, _, _, result = execute(pathlib.Path(directory), source_decision, 'ready')
            assert result.status == READY
            assert result.decision == expected
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, 'mirror_observation_admission_ready')
        plan_value = plan(source)
        report_value = report(plan_value, source)
        report_value['cycles'][0]['latency_delta_ratio'] = 0.9
        result = build_longitudinal_mirror_noninterference(runtime_context=context(root), longitudinal_mirror_plan=plan_value, longitudinal_mirror_license=license_value(plan_value, report_value, source), longitudinal_mirror_report=report_value)
        assert result.status == BLOCKED
        assert 'longitudinal_mirror_report_digest_invalid' in result.blockers
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        source = sources(root, 'mirror_observation_admission_ready')
        plan_value = plan(source)
        report_value = report(plan_value, source)
        source['world']['world_model_id'] = 'tampered'
        write(root / 'ku_indra_qi_noncommutative_mandala_world_state.json', source['world'])
        result = build_longitudinal_mirror_noninterference(runtime_context=context(root), longitudinal_mirror_plan=plan_value, longitudinal_mirror_license=license_value(plan_value, report_value, source), longitudinal_mirror_report=report_value)
        assert result.status == BLOCKED
        assert 'longitudinal_mirror_source_world_invalid' in result.blockers
    manifest = json.loads((ROOT / 'manifests/qi_longitudinal_mirror_noninterference_v0_23.json').read_text())
    assert manifest['status'] == 'READY'
    for group in ('runtime', 'scripts', 'docs', 'example'):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
    print('qi_longitudinal_mirror_noninterference_v0_23 checks passed')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
