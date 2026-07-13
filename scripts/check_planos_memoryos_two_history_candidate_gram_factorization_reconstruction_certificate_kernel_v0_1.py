#!/usr/bin/env python3
from __future__ import annotations
import copy
from itertools import permutations
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runtime.kuuos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate
from runtime.kuuos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1 import issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate
from runtime.kuuos_memoryos_two_history_candidate_gram_factorization_reconstruction_certificate_kernel_v0_1 import EXPECTED_CANDIDATE_IDS, SCHEMA_VERSION, canonical_digest, issue_two_history_candidate_gram_factorization_reconstruction_certificate
from scripts.check_planos_memoryos_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate_kernel_v0_1 import build_reference_payload as build_memoryos_v045_payload
from scripts.check_planos_memoryos_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate_kernel_v0_1 import build_reference_payload as build_memoryos_v047_payload
CANDIDATE_IDS = EXPECTED_CANDIDATE_IDS

def source_memoryos_v045_certificate() -> dict:
    result = issue_candidate_gram_lift_decisionos_relational_coherence_kernel_certificate(build_memoryos_v045_payload())
    assert result['accepted'], result['blockers']
    return result

def source_memoryos_v047_certificate() -> dict:
    result = issue_candidate_triple_gram_determinant_joint_coherence_compatibility_certificate(build_memoryos_v047_payload())
    assert result['accepted'], result['blockers']
    return result

def _complex_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] + right[0], left[1] + right[1])

def _complex_sub(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] - right[0], left[1] - right[1])

def _complex_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0])

def _complex_scale(coefficient: int, value: tuple[int, int]) -> tuple[int, int]:
    return (coefficient * value[0], coefficient * value[1])

def _permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum((1 for left_index in range(len(values)) for right_index in range(left_index + 1, len(values)) if values[left_index] > values[right_index]))
    return -1 if inversions % 2 else 1

def _determinant4(entries: dict[tuple[str, str], tuple[int, int]]) -> tuple[int, int]:
    total = (0, 0)
    for permutation in permutations(range(4)):
        term = (1, 0)
        for row_index, column_index in enumerate(permutation):
            term = _complex_mul(term, entries[CANDIDATE_IDS[row_index], CANDIDATE_IDS[column_index]])
        total = _complex_add(total, _complex_scale(_permutation_sign(permutation), term))
    return total

def _coupling_map(source_v045: dict) -> tuple[list[str], dict[str, tuple[int, int]]]:
    observables = source_v045['observables']
    history_ids = list(observables['retained_history_ids'])
    result: dict[str, tuple[int, int]] = {}
    for item in observables['candidate_history_couplings']:
        coefficients = item['history_coefficients']
        result[item['candidate_id']] = (coefficients[history_ids[0]], coefficients[history_ids[1]])
    return (history_ids, result)

def _entry_map(step: dict) -> dict[tuple[str, str], tuple[int, int]]:
    return {(item['left_candidate_id'], item['right_candidate_id']): (item['real_numerator'], item['imag_numerator']) for item in step['candidate_kernel_entries']}

def _factorized_entry(history_metric: dict[tuple[int, int], tuple[int, int]], left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    total = (0, 0)
    for row_index, left_coefficient in enumerate(left):
        for column_index, right_coefficient in enumerate(right):
            total = _complex_add(total, _complex_scale(left_coefficient * right_coefficient, history_metric[row_index, column_index]))
    return total

def _triple_map(step: dict) -> dict[tuple[str, str, str], dict]:
    return {(item['first_candidate_id'], item['second_candidate_id'], item['third_candidate_id']): item for item in step['candidate_triple_gram_determinant_records']}

def expected_factorization_trajectory(source_v045: dict, source_v047: dict) -> list[dict]:
    history_ids, coupling_map = _coupling_map(source_v045)
    factor_matrix = [{'candidate_id': candidate_id, 'first_history_coefficient': coupling_map[candidate_id][0], 'second_history_coefficient': coupling_map[candidate_id][1]} for candidate_id in CANDIDATE_IDS]
    result: list[dict] = []
    v045_steps = source_v045['observables']['candidate_gram_kernel_trajectory']
    v047_steps = source_v047['observables']['candidate_triple_gram_determinant_trajectory']
    for source_step, triple_step in zip(v045_steps, v047_steps, strict=True):
        entries = _entry_map(source_step)
        history_metric = {(0, 0): entries['reobserve', 'reobserve'], (0, 1): entries['reobserve', 'terminate_candidate'], (1, 0): entries['terminate_candidate', 'reobserve'], (1, 1): entries['terminate_candidate', 'terminate_candidate']}
        history_metric_records = [{'row_history_id': history_ids[row_index], 'column_history_id': history_ids[column_index], 'real_numerator': history_metric[row_index, column_index][0], 'imag_numerator': history_metric[row_index, column_index][1]} for row_index in range(2) for column_index in range(2)]
        reconstruction_records: list[dict] = []
        for left_id in CANDIDATE_IDS:
            for right_id in CANDIDATE_IDS:
                reconstructed = _factorized_entry(history_metric, coupling_map[left_id], coupling_map[right_id])
                source_entry = entries[left_id, right_id]
                reconstruction_records.append({'left_candidate_id': left_id, 'right_candidate_id': right_id, 'left_first_history_coefficient': coupling_map[left_id][0], 'left_second_history_coefficient': coupling_map[left_id][1], 'right_first_history_coefficient': coupling_map[right_id][0], 'right_second_history_coefficient': coupling_map[right_id][1], 'source_real_numerator': source_entry[0], 'source_imag_numerator': source_entry[1], 'reconstructed_real_numerator': reconstructed[0], 'reconstructed_imag_numerator': reconstructed[1], 'factorization_reconstruction_exact': reconstructed == source_entry, 'pair_retained': True})
        row_relations: list[dict] = []
        column_relations: list[dict] = []
        for other_id in CANDIDATE_IDS:
            row_relations.append({'right_candidate_id': other_id, 'continue_equals_reobserve_plus_terminate': entries['continue', other_id] == _complex_add(entries['reobserve', other_id], entries['terminate_candidate', other_id]), 'hold_equals_reobserve_minus_terminate': entries['hold', other_id] == _complex_sub(entries['reobserve', other_id], entries['terminate_candidate', other_id])})
            column_relations.append({'left_candidate_id': other_id, 'continue_equals_reobserve_plus_terminate': entries[other_id, 'continue'] == _complex_add(entries[other_id, 'reobserve'], entries[other_id, 'terminate_candidate']), 'hold_equals_reobserve_minus_terminate': entries[other_id, 'hold'] == _complex_sub(entries[other_id, 'reobserve'], entries[other_id, 'terminate_candidate'])})
        determinant = _determinant4(entries)
        triples = _triple_map(triple_step)
        triples_bound = all((record['first_diagonal_numerator'] == entries[first_id, first_id][0] and record['second_diagonal_numerator'] == entries[second_id, second_id][0] and (record['third_diagonal_numerator'] == entries[third_id, third_id][0]) and ((record['first_second_real_numerator'], record['first_second_imag_numerator']) == entries[first_id, second_id]) and ((record['second_third_real_numerator'], record['second_third_imag_numerator']) == entries[second_id, third_id]) and ((record['third_first_real_numerator'], record['third_first_imag_numerator']) == entries[third_id, first_id]) and (record['candidate_triple_gram_determinant_numerator'] == 0) for (first_id, second_id, third_id), record in triples.items()))
        all_reconstructed = all((item['factorization_reconstruction_exact'] for item in reconstruction_records))
        all_rows = all((item['continue_equals_reobserve_plus_terminate'] and item['hold_equals_reobserve_minus_terminate'] for item in row_relations))
        all_columns = all((item['continue_equals_reobserve_plus_terminate'] and item['hold_equals_reobserve_minus_terminate'] for item in column_relations))
        result.append({'step_index': source_step['step_index'], 'dephasing_numerator': source_step['dephasing_numerator'], 'kernel_entry_denominator': source_step['kernel_entry_denominator'], 'history_metric_entries': history_metric_records, 'candidate_factor_rows': factor_matrix, 'candidate_kernel_reconstruction_records': reconstruction_records, 'candidate_row_relation_records': row_relations, 'candidate_column_relation_records': column_relations, 'all_step_candidate_entries_reconstructed': all_reconstructed, 'all_step_candidate_row_relations_exact': all_rows, 'all_step_candidate_column_relations_exact': all_columns, 'candidate_four_by_four_determinant_real_numerator': determinant[0], 'candidate_four_by_four_determinant_imag_numerator': determinant[1], 'candidate_four_by_four_determinant_denominator': source_step['kernel_entry_denominator'] ** 4, 'candidate_four_by_four_determinant_zero': determinant == (0, 0), 'all_step_v047_triple_records_bound_to_factorization': triples_bound, 'candidate_gram_rank_at_most_two_by_factorization': all_reconstructed and determinant == (0, 0)})
    return result

def expected_claims(source_v045: dict, source_v047: dict) -> dict:
    history_ids, coupling_map = _coupling_map(source_v045)
    factor_matrix = [{'candidate_id': candidate_id, 'first_history_coefficient': coupling_map[candidate_id][0], 'second_history_coefficient': coupling_map[candidate_id][1]} for candidate_id in CANDIDATE_IDS]
    trajectory = expected_factorization_trajectory(source_v045, source_v047)
    source_v045_obs = source_v045['observables']
    source_v047_obs = source_v047['observables']
    input_digest = canonical_digest({'schema_version': SCHEMA_VERSION, 'source_memoryos_v047_certificate_digest': source_v047['certificate_digest'], 'source_memoryos_v045_certificate_digest': source_v045['certificate_digest'], 'source_memoryos_v045_candidate_gram_kernel_digest': source_v045_obs['candidate_gram_kernel_digest'], 'candidate_ids': CANDIDATE_IDS, 'history_ids': history_ids, 'candidate_factor_matrix': factor_matrix})
    return {'input_digest': input_digest, 'source_memoryos_v047_certificate_digest': source_v047['certificate_digest'], 'source_memoryos_v047_candidate_triple_digest': source_v047_obs['candidate_triple_gram_determinant_digest'], 'source_memoryos_v045_certificate_digest': source_v045['certificate_digest'], 'source_memoryos_v045_candidate_gram_kernel_digest': source_v045_obs['candidate_gram_kernel_digest'], 'retained_history_ids': history_ids, 'retained_decision_candidate_ids': CANDIDATE_IDS, 'history_anchor_candidate_ids': ['reobserve', 'terminate_candidate'], 'candidate_factor_matrix': factor_matrix, 'two_history_candidate_gram_factorization_trajectory': trajectory, 'two_history_candidate_gram_factorization_digest': canonical_digest(trajectory), 'candidate_factor_row_count': 4, 'history_factor_dimension': 2, 'candidate_kernel_entry_count_per_step': 16, 'source_memoryos_v047_exact': True, 'source_memoryos_v045_exact': True, 'fixed_candidate_history_factor_rows_exact': True, 'all_candidate_kernel_entries_reconstructed': True, 'all_candidate_row_relations_exact': True, 'all_candidate_column_relations_exact': True, 'all_candidate_four_by_four_determinants_zero': True, 'all_v047_triple_records_bound_to_factorization': True, 'candidate_gram_rank_at_most_two_by_explicit_factorization': True, 'all_decision_candidates_retained': True, 'all_planos_histories_retained': True, 'source_relational_frontier_candidate_ids': source_v045_obs['source_relational_frontier_candidate_ids'], 'source_required_review_candidate_ids': source_v045_obs['source_required_review_candidate_ids'], 'source_dissent_review_candidate_ids': source_v045_obs['source_dissent_review_candidate_ids'], 'source_minority_protection_candidate_ids': source_v045_obs['source_minority_protection_candidate_ids'], 'relational_frontier_preserved': True, 'required_review_set_preserved': True, 'dissent_visibility_preserved': True, 'minority_visibility_preserved': True, 'factorization_witness_advisory_only': True, 'history_coordinate_anchors_not_candidate_priority': True, 'rank_factorization_not_candidate_consensus': True, 'candidate_ranking_performed': False, 'candidate_pruning_performed': False, 'candidate_selection_performed': False, 'decision_commit_performed': False, 'decision_receipt_issued': False, 'plan_synthesis_performed': False, 'activation_performed': False, 'execution_permission': False, 'source_memoryos_v047_mutated': False, 'source_memoryos_v045_mutated': False, 'source_decisionos_v06_mutated': False, 'persistent_world_state_mutated': False, 'verification_result_claimed': False, 'truth_authority_granted': False, 'future_only': True, 'read_only': True}

def build_reference_payload() -> dict:
    source_v045 = source_memoryos_v045_certificate()
    source_v047 = source_memoryos_v047_certificate()
    return {'schema_version': SCHEMA_VERSION, 'source_memoryos_v047_certificate': source_v047, 'source_memoryos_v045_certificate': source_v045, 'claims': expected_claims(source_v045, source_v047)}

def _resign(certificate: dict) -> None:
    certificate.pop('certificate_digest', None)
    certificate['certificate_digest'] = canonical_digest(certificate)

def _resign_v045(certificate: dict) -> None:
    trajectory = certificate['observables']['candidate_gram_kernel_trajectory']
    certificate['observables']['candidate_gram_kernel_digest'] = canonical_digest(trajectory)
    _resign(certificate)

def _resign_v047(certificate: dict) -> None:
    trajectory = certificate['observables']['candidate_triple_gram_determinant_trajectory']
    certificate['observables']['candidate_triple_gram_determinant_digest'] = canonical_digest(trajectory)
    _resign(certificate)

def assert_rejects(payload: dict, blocker: str) -> None:
    result = issue_two_history_candidate_gram_factorization_reconstruction_certificate(payload)
    assert not result['accepted'], result
    assert blocker in result['blockers'], result['blockers']

def _history_metric_trajectory(steps: list[dict], row: int, column: int) -> list[int]:
    result: list[int] = []
    for step in steps:
        record = step['history_metric_entries'][2 * row + column]
        result.append(record['real_numerator'])
    return result

def _recompute_triple_record(record: dict, denominator: int) -> None:
    first_diagonal = record['first_diagonal_numerator']
    second_diagonal = record['second_diagonal_numerator']
    third_diagonal = record['third_diagonal_numerator']
    first_second = (record['first_second_real_numerator'], record['first_second_imag_numerator'])
    second_third = (record['second_third_real_numerator'], record['second_third_imag_numerator'])
    third_first = (record['third_first_real_numerator'], record['third_first_imag_numerator'])
    cyclic = _complex_mul(_complex_mul(first_second, second_third), third_first)
    abs_square = lambda value: value[0] * value[0] + value[1] * value[1]
    diagonal_cubic = first_diagonal * second_diagonal * third_diagonal
    first_subtraction = first_diagonal * abs_square(second_third)
    second_subtraction = second_diagonal * abs_square(third_first)
    third_subtraction = third_diagonal * abs_square(first_second)
    determinant = diagonal_cubic + 2 * cyclic[0] - first_subtraction - second_subtraction - third_subtraction
    record['cyclic_product_real_numerator'] = cyclic[0]
    record['cyclic_product_imag_numerator'] = cyclic[1]
    record['twice_cyclic_product_real_numerator'] = 2 * cyclic[0]
    record['diagonal_cubic_numerator'] = diagonal_cubic
    record['first_diagonal_times_second_third_magnitude_square_numerator'] = first_subtraction
    record['second_diagonal_times_third_first_magnitude_square_numerator'] = second_subtraction
    record['third_diagonal_times_first_second_magnitude_square_numerator'] = third_subtraction
    record['candidate_triple_gram_determinant_numerator'] = determinant
    record['candidate_triple_gram_determinant_denominator'] = denominator ** 3
    record['candidate_triple_principal_minor_nonnegative'] = determinant >= 0
    record['candidate_triple_rank_two_determinant_zero'] = determinant == 0
    record['pairwise_envelopes_jointly_compatible'] = determinant >= 0

def main() -> int:
    payload = build_reference_payload()
    certificate = issue_two_history_candidate_gram_factorization_reconstruction_certificate(payload)
    assert certificate['accepted'], certificate['blockers']
    obs = certificate['observables']
    steps = obs['two_history_candidate_gram_factorization_trajectory']
    assert len(steps) == 3
    assert obs['history_factor_dimension'] == 2
    assert obs['candidate_factor_row_count'] == 4
    assert obs['candidate_kernel_entry_count_per_step'] == 16
    assert obs['candidate_factor_matrix'] == [{'candidate_id': 'continue', 'first_history_coefficient': 1, 'second_history_coefficient': 1}, {'candidate_id': 'hold', 'first_history_coefficient': 1, 'second_history_coefficient': -1}, {'candidate_id': 'reobserve', 'first_history_coefficient': 1, 'second_history_coefficient': 0}, {'candidate_id': 'terminate_candidate', 'first_history_coefficient': 0, 'second_history_coefficient': 1}]
    assert _history_metric_trajectory(steps, 0, 0) == [2, 2, 2]
    assert _history_metric_trajectory(steps, 0, 1) == [2, 1, 0]
    assert _history_metric_trajectory(steps, 1, 0) == [2, 1, 0]
    assert _history_metric_trajectory(steps, 1, 1) == [2, 2, 2]
    assert [step['candidate_four_by_four_determinant_real_numerator'] for step in steps] == [0, 0, 0]
    assert [step['candidate_four_by_four_determinant_imag_numerator'] for step in steps] == [0, 0, 0]
    assert all((len(step['candidate_kernel_reconstruction_records']) == 16 and step['all_step_candidate_entries_reconstructed'] and step['all_step_candidate_row_relations_exact'] and step['all_step_candidate_column_relations_exact'] and step['candidate_four_by_four_determinant_zero'] and step['all_step_v047_triple_records_bound_to_factorization'] for step in steps))
    assert obs['candidate_gram_rank_at_most_two_by_explicit_factorization']
    assert obs['source_relational_frontier_candidate_ids'] == ['reobserve']
    assert obs['source_dissent_review_candidate_ids'] == ['continue']
    assert obs['source_minority_protection_candidate_ids'] == ['hold']
    tampered = copy.deepcopy(payload)
    tampered['source_memoryos_v047_certificate']['accepted'] = False
    assert_rejects(tampered, 'source_memoryos_v047_not_accepted')
    tampered = copy.deepcopy(payload)
    tampered['source_memoryos_v045_certificate']['certificate_digest'] = 'substituted'
    assert_rejects(tampered, 'source_memoryos_v045_certificate_digest_mismatch')
    tampered = copy.deepcopy(payload)
    couplings = tampered['source_memoryos_v045_certificate']['observables']['candidate_history_couplings']
    hold = next((item for item in couplings if item['candidate_id'] == 'hold'))
    second_history_id = tampered['source_memoryos_v045_certificate']['observables']['retained_history_ids'][1]
    hold['history_coefficients'][second_history_id] = 1
    _resign(tampered['source_memoryos_v045_certificate'])
    assert_rejects(tampered, 'source_memoryos_v045_reference_coupling_mismatch')
    tampered = copy.deepcopy(payload)
    v045 = tampered['source_memoryos_v045_certificate']
    step = v045['observables']['candidate_gram_kernel_trajectory'][1]
    for item in step['candidate_kernel_entries']:
        pair = (item['left_candidate_id'], item['right_candidate_id'])
        if pair in {('continue', 'reobserve'), ('reobserve', 'continue')}:
            item['real_numerator'] = 2
            item['imag_numerator'] = 0
    _resign_v045(v045)
    v047 = tampered['source_memoryos_v047_certificate']
    v047['observables']['source_memoryos_v045_certificate_digest'] = v045['certificate_digest']
    v047['observables']['source_memoryos_v045_candidate_gram_kernel_digest'] = v045['observables']['candidate_gram_kernel_digest']
    _resign_v047(v047)
    assert_rejects(tampered, 'observable_required_all_candidate_kernel_entries_reconstructed')
    tampered = copy.deepcopy(payload)
    v047 = tampered['source_memoryos_v047_certificate']
    step = v047['observables']['candidate_triple_gram_determinant_trajectory'][0]
    record = next((item for item in step['candidate_triple_gram_determinant_records'] if item['first_candidate_id'] == 'continue' and item['second_candidate_id'] == 'continue' and (item['third_candidate_id'] == 'continue')))
    for field in ('first_diagonal_numerator', 'second_diagonal_numerator', 'third_diagonal_numerator', 'first_second_real_numerator', 'second_third_real_numerator', 'third_first_real_numerator'):
        record[field] = 7
    for field in ('first_second_imag_numerator', 'second_third_imag_numerator', 'third_first_imag_numerator'):
        record[field] = 0
    _recompute_triple_record(record, step['source_kernel_entry_denominator'])
    _resign_v047(v047)
    assert_rejects(tampered, 'observable_required_all_v047_triple_records_bound_to_factorization')
    for field in ('candidate_ranking_performed', 'candidate_pruning_performed', 'candidate_selection_performed', 'decision_commit_performed', 'decision_receipt_issued', 'plan_synthesis_performed', 'activation_performed', 'execution_permission', 'source_memoryos_v047_mutated', 'source_memoryos_v045_mutated', 'source_decisionos_v06_mutated', 'persistent_world_state_mutated', 'verification_result_claimed', 'truth_authority_granted'):
        tampered = copy.deepcopy(payload)
        tampered['claims'][field] = True
        assert_rejects(tampered, 'claim_mismatch_' + field)
    print(json.dumps({'status': 'PASS', 'schema_version': SCHEMA_VERSION, 'candidate_count': len(CANDIDATE_IDS), 'history_factor_dimension': 2, 'candidate_kernel_entry_count_per_step': 16, 'dephasing_step_count': len(steps), 'four_by_four_determinant_numerators': [step['candidate_four_by_four_determinant_real_numerator'] for step in steps], 'certificate_digest': certificate['certificate_digest']}, ensure_ascii=False, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
