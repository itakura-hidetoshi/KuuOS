from __future__ import annotations
from hashlib import sha256
from itertools import permutations
import json
from typing import Any, Mapping
SCHEMA_VERSION = 'kuuos.memoryos.two-history-candidate-gram-factorization-reconstruction-certificate.v0.1'
SOURCE_MEMORYOS_V047_SCHEMA_VERSION = 'kuuos.memoryos.candidate-triple-gram-determinant-joint-coherence-compatibility-certificate.v0.1'
SOURCE_MEMORYOS_V045_SCHEMA_VERSION = 'kuuos.memoryos.candidate-gram-lift-decisionos-relational-coherence-kernel-certificate.v0.1'
EXPECTED_CANDIDATE_IDS = ['continue', 'hold', 'reobserve', 'terminate_candidate']
MAXIMUM_CANDIDATE_COUNT = 128
MAXIMUM_HISTORY_COUNT = 128
MAXIMUM_DEPHASING_STEP_COUNT = 64
MAXIMUM_ABSOLUTE_INTEGER = 10000000

def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return sha256(encoded).hexdigest()

def _blocked(*blockers: str) -> dict[str, Any]:
    return {'accepted': False, 'schema_version': SCHEMA_VERSION, 'blockers': sorted(set(blockers)), 'observables': {}, 'certificate_digest': None}

def _integer(value: Any, field: str, *, nonnegative: bool=False) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(field + '_invalid')
    if abs(value) > MAXIMUM_ABSOLUTE_INTEGER:
        raise ValueError(field + '_out_of_bounds')
    if nonnegative and value < 0:
        raise ValueError(field + '_negative')
    return value

def _string_ids(value: Any, field: str, maximum: int) -> list[str]:
    if not isinstance(value, list) or not value or len(value) > maximum or (len(value) != len(set(value))) or any((not isinstance(item, str) or not item for item in value)):
        raise ValueError(field + '_invalid')
    return list(value)

def _review_ids(observables: Mapping[str, Any], field: str, candidate_ids: list[str], prefix: str) -> list[str]:
    value = observables.get(field)
    if not isinstance(value, list) or len(value) != len(set(value)) or any((item not in candidate_ids for item in value)):
        raise ValueError(prefix + '_' + field + '_invalid')
    return list(value)

def _complex_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] + right[0], left[1] + right[1])

def _complex_sub(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] - right[0], left[1] - right[1])

def _complex_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0])

def _complex_scale(coefficient: int, value: tuple[int, int]) -> tuple[int, int]:
    return (coefficient * value[0], coefficient * value[1])

def _complex_abs_square(value: tuple[int, int]) -> int:
    return value[0] * value[0] + value[1] * value[1]

def _permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum((1 for left_index in range(len(values)) for right_index in range(left_index + 1, len(values)) if values[left_index] > values[right_index]))
    return -1 if inversions % 2 else 1

def _complex_determinant4(entries: Mapping[tuple[str, str], tuple[int, int]], candidate_ids: list[str]) -> tuple[int, int]:
    if len(candidate_ids) != 4:
        raise ValueError('candidate_count_not_four')
    total = (0, 0)
    for permutation in permutations(range(4)):
        term = (1, 0)
        for row_index, column_index in enumerate(permutation):
            term = _complex_mul(term, entries[candidate_ids[row_index], candidate_ids[column_index]])
        total = _complex_add(total, _complex_scale(_permutation_sign(permutation), term))
    return total

def _candidate_entry_map(raw_entries: Any, *, candidate_ids: list[str], prefix: str) -> dict[tuple[str, str], tuple[int, int]]:
    if not isinstance(raw_entries, list):
        raise ValueError(prefix + '_entries_invalid')
    expected = {(left, right) for left in candidate_ids for right in candidate_ids}
    result: dict[tuple[str, str], tuple[int, int]] = {}
    for raw in raw_entries:
        if not isinstance(raw, Mapping):
            raise ValueError(prefix + '_entry_invalid')
        item = dict(raw)
        left_id = item.get('left_candidate_id')
        right_id = item.get('right_candidate_id')
        if left_id not in candidate_ids or right_id not in candidate_ids:
            raise ValueError(prefix + '_pair_invalid')
        pair = (left_id, right_id)
        if pair in result:
            raise ValueError(prefix + '_pair_duplicate')
        result[pair] = (_integer(item.get('real_numerator'), prefix + '_real'), _integer(item.get('imag_numerator'), prefix + '_imag'))
    if set(result) != expected:
        raise ValueError(prefix + '_pair_support_mismatch')
    for left_id in candidate_ids:
        diagonal = result[left_id, left_id]
        if diagonal[1] != 0 or diagonal[0] < 0:
            raise ValueError(prefix + '_diagonal_invalid')
        for right_id in candidate_ids:
            forward = result[left_id, right_id]
            reverse = result[right_id, left_id]
            if forward[0] != reverse[0] or forward[1] != -reverse[1]:
                raise ValueError(prefix + '_not_hermitian')
    return result

def _normalize_source_memoryos_v045(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError('source_memoryos_v045_certificate_invalid')
    source = dict(value)
    if source.get('accepted') is not True:
        raise ValueError('source_memoryos_v045_not_accepted')
    if source.get('schema_version') != SOURCE_MEMORYOS_V045_SCHEMA_VERSION:
        raise ValueError('source_memoryos_v045_schema_invalid')
    digest = source.get('certificate_digest')
    if not isinstance(digest, str) or not digest:
        raise ValueError('source_memoryos_v045_certificate_digest_missing')
    unsigned = dict(source)
    unsigned.pop('certificate_digest', None)
    if canonical_digest(unsigned) != digest:
        raise ValueError('source_memoryos_v045_certificate_digest_mismatch')
    observables = source.get('observables')
    if not isinstance(observables, Mapping):
        raise ValueError('source_memoryos_v045_observables_invalid')
    observables = dict(observables)
    for field in ('all_candidate_pair_support_retained', 'all_candidate_kernels_hermitian', 'all_candidate_kernels_psd_by_gram_lift', 'all_candidate_diagonals_match_v044_quadratic_evidence', 'all_decision_candidates_retained', 'all_planos_histories_retained', 'relational_frontier_preserved', 'required_review_set_preserved', 'dissent_visibility_preserved', 'minority_visibility_preserved', 'candidate_pair_coherence_advisory_only', 'candidate_gram_kernel_not_relational_order', 'future_only', 'read_only'):
        if observables.get(field) is not True:
            raise ValueError('source_memoryos_v045_required_' + field)
    for field in ('candidate_ranking_performed', 'candidate_pruning_performed', 'candidate_selection_performed', 'decision_commit_performed', 'decision_receipt_issued', 'plan_synthesis_performed', 'activation_performed', 'execution_permission', 'source_memoryos_v043_mutated', 'source_memoryos_v044_mutated', 'source_decisionos_v06_mutated', 'persistent_world_state_mutated', 'verification_result_claimed', 'truth_authority_granted'):
        if observables.get(field) is not False:
            raise ValueError('source_memoryos_v045_forbidden_' + field)
    candidate_ids = _string_ids(observables.get('retained_decision_candidate_ids'), 'source_memoryos_v045_candidate_ids', MAXIMUM_CANDIDATE_COUNT)
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        raise ValueError('source_memoryos_v045_candidate_order_mismatch')
    history_ids = _string_ids(observables.get('retained_history_ids'), 'source_memoryos_v045_history_ids', MAXIMUM_HISTORY_COUNT)
    if len(history_ids) != 2:
        raise ValueError('source_memoryos_v045_history_count_not_two')
    raw_couplings = observables.get('candidate_history_couplings')
    if not isinstance(raw_couplings, list) or len(raw_couplings) != len(candidate_ids):
        raise ValueError('source_memoryos_v045_couplings_incomplete')
    coupling_map: dict[str, tuple[int, int]] = {}
    for raw in raw_couplings:
        if not isinstance(raw, Mapping):
            raise ValueError('source_memoryos_v045_coupling_invalid')
        item = dict(raw)
        candidate_id = item.get('candidate_id')
        coefficients = item.get('history_coefficients')
        if candidate_id not in candidate_ids or candidate_id in coupling_map:
            raise ValueError('source_memoryos_v045_coupling_candidate_invalid')
        if not isinstance(coefficients, Mapping) or set(coefficients) != set(history_ids):
            raise ValueError('source_memoryos_v045_coupling_history_support_mismatch')
        coupling_map[candidate_id] = (_integer(coefficients[history_ids[0]], 'source_memoryos_v045_first_history_coefficient'), _integer(coefficients[history_ids[1]], 'source_memoryos_v045_second_history_coefficient'))
    expected_couplings = {'continue': (1, 1), 'hold': (1, -1), 'reobserve': (1, 0), 'terminate_candidate': (0, 1)}
    if coupling_map != expected_couplings:
        raise ValueError('source_memoryos_v045_reference_coupling_mismatch')
    raw_trajectory = observables.get('candidate_gram_kernel_trajectory')
    if not isinstance(raw_trajectory, list) or not raw_trajectory or len(raw_trajectory) > MAXIMUM_DEPHASING_STEP_COUNT:
        raise ValueError('source_memoryos_v045_trajectory_invalid')
    kernel_digest = observables.get('candidate_gram_kernel_digest')
    if not isinstance(kernel_digest, str) or not kernel_digest:
        raise ValueError('source_memoryos_v045_kernel_digest_missing')
    if canonical_digest(raw_trajectory) != kernel_digest:
        raise ValueError('source_memoryos_v045_kernel_digest_mismatch')
    trajectory: list[dict[str, Any]] = []
    previous_dephasing_numerator: int | None = None
    for index, raw_step in enumerate(raw_trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError('source_memoryos_v045_step_invalid')
        step = dict(raw_step)
        if step.get('step_index') != index:
            raise ValueError('source_memoryos_v045_step_index_invalid')
        for field in ('candidate_pair_support_complete', 'candidate_kernel_hermitian', 'candidate_kernel_positive_semidefinite_by_gram_lift', 'candidate_kernel_diagonal_matches_v044_quadratic_evidence'):
            if step.get(field) is not True:
                raise ValueError('source_memoryos_v045_step_required_' + field)
        denominator = _integer(step.get('kernel_entry_denominator'), 'source_memoryos_v045_denominator')
        if denominator <= 0:
            raise ValueError('source_memoryos_v045_denominator_nonpositive')
        dephasing_numerator = _integer(step.get('dephasing_numerator'), 'source_memoryos_v045_dephasing_numerator', nonnegative=True)
        if previous_dephasing_numerator is not None and dephasing_numerator >= previous_dephasing_numerator:
            raise ValueError('source_memoryos_v045_dephasing_not_strictly_decreasing')
        previous_dephasing_numerator = dephasing_numerator
        trajectory.append({'step_index': index, 'dephasing_numerator': dephasing_numerator, 'kernel_entry_denominator': denominator, 'entries': _candidate_entry_map(step.get('candidate_kernel_entries'), candidate_ids=candidate_ids, prefix='source_memoryos_v045')})
    review_fields = {field: _review_ids(observables, field, candidate_ids, 'source_memoryos_v045') for field in ('source_relational_frontier_candidate_ids', 'source_required_review_candidate_ids', 'source_dissent_review_candidate_ids', 'source_minority_protection_candidate_ids')}
    return {'certificate_digest': digest, 'observables': observables, 'candidate_ids': candidate_ids, 'history_ids': history_ids, 'coupling_map': coupling_map, 'trajectory': trajectory, 'kernel_digest': kernel_digest, **review_fields}

def _normalize_source_memoryos_v047(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError('source_memoryos_v047_certificate_invalid')
    source = dict(value)
    if source.get('accepted') is not True:
        raise ValueError('source_memoryos_v047_not_accepted')
    if source.get('schema_version') != SOURCE_MEMORYOS_V047_SCHEMA_VERSION:
        raise ValueError('source_memoryos_v047_schema_invalid')
    digest = source.get('certificate_digest')
    if not isinstance(digest, str) or not digest:
        raise ValueError('source_memoryos_v047_certificate_digest_missing')
    unsigned = dict(source)
    unsigned.pop('certificate_digest', None)
    if canonical_digest(unsigned) != digest:
        raise ValueError('source_memoryos_v047_certificate_digest_mismatch')
    observables = source.get('observables')
    if not isinstance(observables, Mapping):
        raise ValueError('source_memoryos_v047_observables_invalid')
    observables = dict(observables)
    for field in ('all_ordered_candidate_triple_support_retained', 'all_candidate_triple_principal_minors_nonnegative', 'all_candidate_triple_determinants_zero', 'all_pairwise_envelopes_jointly_compatible', 'candidate_gram_rank_at_most_two_witness', 'all_repeated_candidate_triples_degenerate', 'all_distinct_candidate_triples_rank_two_saturated', 'source_candidate_pair_envelope_exact', 'relational_frontier_preserved', 'required_review_set_preserved', 'dissent_visibility_preserved', 'minority_visibility_preserved', 'joint_coherence_compatibility_advisory_only', 'triple_cyclic_product_not_group_preference', 'rank_two_saturation_not_candidate_consensus', 'future_only', 'read_only'):
        if observables.get(field) is not True:
            raise ValueError('source_memoryos_v047_required_' + field)
    for field in ('candidate_ranking_performed', 'candidate_pruning_performed', 'candidate_selection_performed', 'decision_commit_performed', 'decision_receipt_issued', 'plan_synthesis_performed', 'activation_performed', 'execution_permission', 'source_memoryos_v046_mutated', 'source_decisionos_v06_mutated', 'persistent_world_state_mutated', 'verification_result_claimed', 'truth_authority_granted'):
        if observables.get(field) is not False:
            raise ValueError('source_memoryos_v047_forbidden_' + field)
    candidate_ids = _string_ids(observables.get('retained_decision_candidate_ids'), 'source_memoryos_v047_candidate_ids', MAXIMUM_CANDIDATE_COUNT)
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        raise ValueError('source_memoryos_v047_candidate_order_mismatch')
    raw_trajectory = observables.get('candidate_triple_gram_determinant_trajectory')
    if not isinstance(raw_trajectory, list) or not raw_trajectory or len(raw_trajectory) > MAXIMUM_DEPHASING_STEP_COUNT:
        raise ValueError('source_memoryos_v047_trajectory_invalid')
    triple_digest = observables.get('candidate_triple_gram_determinant_digest')
    if not isinstance(triple_digest, str) or not triple_digest:
        raise ValueError('source_memoryos_v047_triple_digest_missing')
    if canonical_digest(raw_trajectory) != triple_digest:
        raise ValueError('source_memoryos_v047_triple_digest_mismatch')
    expected_triples = {(first, second, third) for first in candidate_ids for second in candidate_ids for third in candidate_ids}
    trajectory: list[dict[str, Any]] = []
    previous_dephasing_numerator: int | None = None
    for index, raw_step in enumerate(raw_trajectory):
        if not isinstance(raw_step, Mapping):
            raise ValueError('source_memoryos_v047_step_invalid')
        step = dict(raw_step)
        if step.get('step_index') != index:
            raise ValueError('source_memoryos_v047_step_index_invalid')
        for field in ('ordered_candidate_triple_support_complete', 'all_step_candidate_triple_principal_minors_nonnegative', 'all_step_candidate_triple_determinants_zero', 'all_step_pairwise_envelopes_jointly_compatible'):
            if step.get(field) is not True:
                raise ValueError('source_memoryos_v047_step_required_' + field)
        denominator = _integer(step.get('source_kernel_entry_denominator'), 'source_memoryos_v047_denominator')
        if denominator <= 0:
            raise ValueError('source_memoryos_v047_denominator_nonpositive')
        dephasing_numerator = _integer(step.get('dephasing_numerator'), 'source_memoryos_v047_dephasing_numerator', nonnegative=True)
        if previous_dephasing_numerator is not None and dephasing_numerator >= previous_dephasing_numerator:
            raise ValueError('source_memoryos_v047_dephasing_not_strictly_decreasing')
        previous_dephasing_numerator = dephasing_numerator
        raw_records = step.get('candidate_triple_gram_determinant_records')
        if not isinstance(raw_records, list):
            raise ValueError('source_memoryos_v047_triple_records_invalid')
        records: dict[tuple[str, str, str], dict[str, Any]] = {}
        for raw_record in raw_records:
            if not isinstance(raw_record, Mapping):
                raise ValueError('source_memoryos_v047_triple_record_invalid')
            record = dict(raw_record)
            triple = (record.get('first_candidate_id'), record.get('second_candidate_id'), record.get('third_candidate_id'))
            if triple not in expected_triples:
                raise ValueError('source_memoryos_v047_triple_invalid')
            if triple in records:
                raise ValueError('source_memoryos_v047_triple_duplicate')
            distinct = len(set(triple)) == 3
            if record.get('candidate_ids_distinct') is not distinct:
                raise ValueError('source_memoryos_v047_distinct_flag_mismatch')
            first_diagonal = _integer(record.get('first_diagonal_numerator'), 'source_memoryos_v047_first_diagonal', nonnegative=True)
            second_diagonal = _integer(record.get('second_diagonal_numerator'), 'source_memoryos_v047_second_diagonal', nonnegative=True)
            third_diagonal = _integer(record.get('third_diagonal_numerator'), 'source_memoryos_v047_third_diagonal', nonnegative=True)
            first_second = (_integer(record.get('first_second_real_numerator'), 'source_memoryos_v047_first_second_real'), _integer(record.get('first_second_imag_numerator'), 'source_memoryos_v047_first_second_imag'))
            second_third = (_integer(record.get('second_third_real_numerator'), 'source_memoryos_v047_second_third_real'), _integer(record.get('second_third_imag_numerator'), 'source_memoryos_v047_second_third_imag'))
            third_first = (_integer(record.get('third_first_real_numerator'), 'source_memoryos_v047_third_first_real'), _integer(record.get('third_first_imag_numerator'), 'source_memoryos_v047_third_first_imag'))
            cyclic = _complex_mul(_complex_mul(first_second, second_third), third_first)
            diagonal_cubic = first_diagonal * second_diagonal * third_diagonal
            first_subtraction = first_diagonal * _complex_abs_square(second_third)
            second_subtraction = second_diagonal * _complex_abs_square(third_first)
            third_subtraction = third_diagonal * _complex_abs_square(first_second)
            determinant = diagonal_cubic + 2 * cyclic[0] - first_subtraction - second_subtraction - third_subtraction
            expected_fields = {'cyclic_product_real_numerator': cyclic[0], 'cyclic_product_imag_numerator': cyclic[1], 'twice_cyclic_product_real_numerator': 2 * cyclic[0], 'diagonal_cubic_numerator': diagonal_cubic, 'first_diagonal_times_second_third_magnitude_square_numerator': first_subtraction, 'second_diagonal_times_third_first_magnitude_square_numerator': second_subtraction, 'third_diagonal_times_first_second_magnitude_square_numerator': third_subtraction, 'candidate_triple_gram_determinant_numerator': determinant, 'candidate_triple_gram_determinant_denominator': denominator ** 3, 'candidate_triple_principal_minor_nonnegative': determinant >= 0, 'candidate_triple_rank_two_determinant_zero': determinant == 0, 'pairwise_envelopes_jointly_compatible': determinant >= 0, 'triple_retained': True}
            for field, expected in expected_fields.items():
                if record.get(field) != expected:
                    raise ValueError('source_memoryos_v047_' + field + '_mismatch')
            if determinant != 0:
                raise ValueError('source_memoryos_v047_triple_determinant_nonzero')
            records[triple] = {'first_diagonal': first_diagonal, 'second_diagonal': second_diagonal, 'third_diagonal': third_diagonal, 'first_second': first_second, 'second_third': second_third, 'third_first': third_first, 'determinant': determinant}
        if set(records) != expected_triples:
            raise ValueError('source_memoryos_v047_triple_support_mismatch')
        trajectory.append({'step_index': index, 'dephasing_numerator': dephasing_numerator, 'kernel_entry_denominator': denominator, 'records': records})
    source_v045_digest = observables.get('source_memoryos_v045_certificate_digest')
    source_kernel_digest = observables.get('source_memoryos_v045_candidate_gram_kernel_digest')
    if not isinstance(source_v045_digest, str) or not source_v045_digest:
        raise ValueError('source_memoryos_v047_v045_digest_missing')
    if not isinstance(source_kernel_digest, str) or not source_kernel_digest:
        raise ValueError('source_memoryos_v047_v045_kernel_digest_missing')
    return {'certificate_digest': digest, 'observables': observables, 'candidate_ids': candidate_ids, 'trajectory': trajectory, 'triple_digest': triple_digest, 'source_memoryos_v045_certificate_digest': source_v045_digest, 'source_memoryos_v045_candidate_gram_kernel_digest': source_kernel_digest}

def _factorized_entry(history_metric: Mapping[tuple[int, int], tuple[int, int]], left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    total = (0, 0)
    for row_index, left_coefficient in enumerate(left):
        for column_index, right_coefficient in enumerate(right):
            total = _complex_add(total, _complex_scale(left_coefficient * right_coefficient, history_metric[row_index, column_index]))
    return total

def issue_two_history_candidate_gram_factorization_reconstruction_certificate(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return _blocked('payload_invalid')
    blockers: list[str] = []
    if payload.get('schema_version') != SCHEMA_VERSION:
        blockers.append('schema_version_invalid')
    try:
        source_v047 = _normalize_source_memoryos_v047(payload.get('source_memoryos_v047_certificate'))
        source_v045 = _normalize_source_memoryos_v045(payload.get('source_memoryos_v045_certificate'))
    except ValueError as exc:
        return _blocked(*blockers + [str(exc)])
    if source_v047['source_memoryos_v045_certificate_digest'] != source_v045['certificate_digest']:
        blockers.append('source_v047_v045_certificate_binding_mismatch')
    if source_v047['source_memoryos_v045_candidate_gram_kernel_digest'] != source_v045['kernel_digest']:
        blockers.append('source_v047_v045_kernel_binding_mismatch')
    if source_v047['candidate_ids'] != source_v045['candidate_ids']:
        blockers.append('source_v047_v045_candidate_support_mismatch')
    if len(source_v047['trajectory']) != len(source_v045['trajectory']):
        blockers.append('source_v047_v045_trajectory_length_mismatch')
    if blockers:
        return _blocked(*blockers)
    candidate_ids = source_v045['candidate_ids']
    history_ids = source_v045['history_ids']
    coupling_map = source_v045['coupling_map']
    factor_matrix = [{'candidate_id': candidate_id, 'first_history_coefficient': coupling_map[candidate_id][0], 'second_history_coefficient': coupling_map[candidate_id][1]} for candidate_id in candidate_ids]
    factorization_trajectory: list[dict[str, Any]] = []
    all_entries_reconstructed = True
    all_row_relations = True
    all_column_relations = True
    all_determinants_zero = True
    all_triples_bound = True
    for source_step, triple_step in zip(source_v045['trajectory'], source_v047['trajectory'], strict=True):
        if source_step['step_index'] != triple_step['step_index'] or source_step['dephasing_numerator'] != triple_step['dephasing_numerator'] or source_step['kernel_entry_denominator'] != triple_step['kernel_entry_denominator']:
            return _blocked('source_v047_v045_step_binding_mismatch')
        entries = source_step['entries']
        history_metric = {(0, 0): entries['reobserve', 'reobserve'], (0, 1): entries['reobserve', 'terminate_candidate'], (1, 0): entries['terminate_candidate', 'reobserve'], (1, 1): entries['terminate_candidate', 'terminate_candidate']}
        history_metric_records = [{'row_history_id': history_ids[row_index], 'column_history_id': history_ids[column_index], 'real_numerator': history_metric[row_index, column_index][0], 'imag_numerator': history_metric[row_index, column_index][1]} for row_index in range(2) for column_index in range(2)]
        reconstruction_records: list[dict[str, Any]] = []
        reconstructed_entries: dict[tuple[str, str], tuple[int, int]] = {}
        for left_id in candidate_ids:
            for right_id in candidate_ids:
                reconstructed = _factorized_entry(history_metric, coupling_map[left_id], coupling_map[right_id])
                source_entry = entries[left_id, right_id]
                exact = reconstructed == source_entry
                reconstructed_entries[left_id, right_id] = reconstructed
                reconstruction_records.append({'left_candidate_id': left_id, 'right_candidate_id': right_id, 'left_first_history_coefficient': coupling_map[left_id][0], 'left_second_history_coefficient': coupling_map[left_id][1], 'right_first_history_coefficient': coupling_map[right_id][0], 'right_second_history_coefficient': coupling_map[right_id][1], 'source_real_numerator': source_entry[0], 'source_imag_numerator': source_entry[1], 'reconstructed_real_numerator': reconstructed[0], 'reconstructed_imag_numerator': reconstructed[1], 'factorization_reconstruction_exact': exact, 'pair_retained': True})
                all_entries_reconstructed = all_entries_reconstructed and exact
        row_relation_records: list[dict[str, Any]] = []
        column_relation_records: list[dict[str, Any]] = []
        step_rows_exact = True
        step_columns_exact = True
        for other_id in candidate_ids:
            continue_row = entries['continue', other_id]
            hold_row = entries['hold', other_id]
            reobserve_row = entries['reobserve', other_id]
            terminate_row = entries['terminate_candidate', other_id]
            continue_row_exact = continue_row == _complex_add(reobserve_row, terminate_row)
            hold_row_exact = hold_row == _complex_sub(reobserve_row, terminate_row)
            row_relation_records.append({'right_candidate_id': other_id, 'continue_equals_reobserve_plus_terminate': continue_row_exact, 'hold_equals_reobserve_minus_terminate': hold_row_exact})
            step_rows_exact = step_rows_exact and continue_row_exact and hold_row_exact
            continue_column = entries[other_id, 'continue']
            hold_column = entries[other_id, 'hold']
            reobserve_column = entries[other_id, 'reobserve']
            terminate_column = entries[other_id, 'terminate_candidate']
            continue_column_exact = continue_column == _complex_add(reobserve_column, terminate_column)
            hold_column_exact = hold_column == _complex_sub(reobserve_column, terminate_column)
            column_relation_records.append({'left_candidate_id': other_id, 'continue_equals_reobserve_plus_terminate': continue_column_exact, 'hold_equals_reobserve_minus_terminate': hold_column_exact})
            step_columns_exact = step_columns_exact and continue_column_exact and hold_column_exact
        all_row_relations = all_row_relations and step_rows_exact
        all_column_relations = all_column_relations and step_columns_exact
        determinant = _complex_determinant4(entries, candidate_ids)
        determinant_zero = determinant == (0, 0)
        all_determinants_zero = all_determinants_zero and determinant_zero
        step_triples_bound = True
        for triple, triple_record in triple_step['records'].items():
            first_id, second_id, third_id = triple
            expected_binding = triple_record['first_diagonal'] == entries[first_id, first_id][0] and triple_record['second_diagonal'] == entries[second_id, second_id][0] and (triple_record['third_diagonal'] == entries[third_id, third_id][0]) and (triple_record['first_second'] == entries[first_id, second_id]) and (triple_record['second_third'] == entries[second_id, third_id]) and (triple_record['third_first'] == entries[third_id, first_id]) and (triple_record['determinant'] == 0)
            step_triples_bound = step_triples_bound and expected_binding
        all_triples_bound = all_triples_bound and step_triples_bound
        factorization_trajectory.append({'step_index': source_step['step_index'], 'dephasing_numerator': source_step['dephasing_numerator'], 'kernel_entry_denominator': source_step['kernel_entry_denominator'], 'history_metric_entries': history_metric_records, 'candidate_factor_rows': factor_matrix, 'candidate_kernel_reconstruction_records': reconstruction_records, 'candidate_row_relation_records': row_relation_records, 'candidate_column_relation_records': column_relation_records, 'all_step_candidate_entries_reconstructed': all((item['factorization_reconstruction_exact'] for item in reconstruction_records)), 'all_step_candidate_row_relations_exact': step_rows_exact, 'all_step_candidate_column_relations_exact': step_columns_exact, 'candidate_four_by_four_determinant_real_numerator': determinant[0], 'candidate_four_by_four_determinant_imag_numerator': determinant[1], 'candidate_four_by_four_determinant_denominator': source_step['kernel_entry_denominator'] ** 4, 'candidate_four_by_four_determinant_zero': determinant_zero, 'all_step_v047_triple_records_bound_to_factorization': step_triples_bound, 'candidate_gram_rank_at_most_two_by_factorization': all((item['factorization_reconstruction_exact'] for item in reconstruction_records)) and determinant_zero})
    input_digest = canonical_digest({'schema_version': SCHEMA_VERSION, 'source_memoryos_v047_certificate_digest': source_v047['certificate_digest'], 'source_memoryos_v045_certificate_digest': source_v045['certificate_digest'], 'source_memoryos_v045_candidate_gram_kernel_digest': source_v045['kernel_digest'], 'candidate_ids': candidate_ids, 'history_ids': history_ids, 'candidate_factor_matrix': factor_matrix})
    factorization_digest = canonical_digest(factorization_trajectory)
    observables = {'input_digest': input_digest, 'source_memoryos_v047_certificate_digest': source_v047['certificate_digest'], 'source_memoryos_v047_candidate_triple_digest': source_v047['triple_digest'], 'source_memoryos_v045_certificate_digest': source_v045['certificate_digest'], 'source_memoryos_v045_candidate_gram_kernel_digest': source_v045['kernel_digest'], 'retained_history_ids': history_ids, 'retained_decision_candidate_ids': candidate_ids, 'history_anchor_candidate_ids': ['reobserve', 'terminate_candidate'], 'candidate_factor_matrix': factor_matrix, 'two_history_candidate_gram_factorization_trajectory': factorization_trajectory, 'two_history_candidate_gram_factorization_digest': factorization_digest, 'candidate_factor_row_count': len(candidate_ids), 'history_factor_dimension': len(history_ids), 'candidate_kernel_entry_count_per_step': len(candidate_ids) ** 2, 'source_memoryos_v047_exact': True, 'source_memoryos_v045_exact': True, 'fixed_candidate_history_factor_rows_exact': coupling_map == {'continue': (1, 1), 'hold': (1, -1), 'reobserve': (1, 0), 'terminate_candidate': (0, 1)}, 'all_candidate_kernel_entries_reconstructed': all_entries_reconstructed, 'all_candidate_row_relations_exact': all_row_relations, 'all_candidate_column_relations_exact': all_column_relations, 'all_candidate_four_by_four_determinants_zero': all_determinants_zero, 'all_v047_triple_records_bound_to_factorization': all_triples_bound, 'candidate_gram_rank_at_most_two_by_explicit_factorization': all_entries_reconstructed and all_determinants_zero, 'all_decision_candidates_retained': True, 'all_planos_histories_retained': True, 'source_relational_frontier_candidate_ids': source_v045['source_relational_frontier_candidate_ids'], 'source_required_review_candidate_ids': source_v045['source_required_review_candidate_ids'], 'source_dissent_review_candidate_ids': source_v045['source_dissent_review_candidate_ids'], 'source_minority_protection_candidate_ids': source_v045['source_minority_protection_candidate_ids'], 'relational_frontier_preserved': True, 'required_review_set_preserved': True, 'dissent_visibility_preserved': True, 'minority_visibility_preserved': True, 'factorization_witness_advisory_only': True, 'history_coordinate_anchors_not_candidate_priority': True, 'rank_factorization_not_candidate_consensus': True, 'candidate_ranking_performed': False, 'candidate_pruning_performed': False, 'candidate_selection_performed': False, 'decision_commit_performed': False, 'decision_receipt_issued': False, 'plan_synthesis_performed': False, 'activation_performed': False, 'execution_permission': False, 'source_memoryos_v047_mutated': False, 'source_memoryos_v045_mutated': False, 'source_decisionos_v06_mutated': False, 'persistent_world_state_mutated': False, 'verification_result_claimed': False, 'truth_authority_granted': False, 'future_only': True, 'read_only': True}
    for field in ('source_memoryos_v047_exact', 'source_memoryos_v045_exact', 'fixed_candidate_history_factor_rows_exact', 'all_candidate_kernel_entries_reconstructed', 'all_candidate_row_relations_exact', 'all_candidate_column_relations_exact', 'all_candidate_four_by_four_determinants_zero', 'all_v047_triple_records_bound_to_factorization', 'candidate_gram_rank_at_most_two_by_explicit_factorization', 'all_decision_candidates_retained', 'all_planos_histories_retained', 'relational_frontier_preserved', 'required_review_set_preserved', 'dissent_visibility_preserved', 'minority_visibility_preserved', 'factorization_witness_advisory_only', 'history_coordinate_anchors_not_candidate_priority', 'rank_factorization_not_candidate_consensus', 'future_only', 'read_only'):
        if observables[field] is not True:
            blockers.append('observable_required_' + field)
    claims = payload.get('claims')
    if not isinstance(claims, Mapping):
        blockers.append('claims_invalid')
    else:
        for field, expected in observables.items():
            if claims.get(field) != expected:
                blockers.append('claim_mismatch_' + field)
        extra = sorted(set(claims) - set(observables))
        if extra:
            blockers.append('claim_extra_field_' + extra[0])
    if blockers:
        return _blocked(*blockers)
    certificate = {'accepted': True, 'schema_version': SCHEMA_VERSION, 'blockers': [], 'observables': observables}
    certificate['certificate_digest'] = canonical_digest(certificate)
    return certificate
__all__ = ['SCHEMA_VERSION', 'SOURCE_MEMORYOS_V047_SCHEMA_VERSION', 'SOURCE_MEMORYOS_V045_SCHEMA_VERSION', 'EXPECTED_CANDIDATE_IDS', 'canonical_digest', 'issue_two_history_candidate_gram_factorization_reconstruction_certificate']
