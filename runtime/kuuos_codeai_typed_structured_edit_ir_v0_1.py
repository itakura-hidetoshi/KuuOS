#!/usr/bin/env python3
from __future__ import annotations
import ast
from dataclasses import dataclass
import hashlib
import json
import re
from pathlib import PurePosixPath
from typing import Any, Mapping, Sequence
VERSION = 'kuuos_codeai_typed_structured_edit_ir_v0_1'
SCHEMA_VERSION = 'v0.1'
PROFILE_VERSION = 'CodeAI Typed Structured Edit IR v0.1'
STATUS_READY = 'ready'
STATUS_BLOCKED = 'blocked'
MODE_TYPED_IR_ONLY = 'typed_ir_only'
DISPOSITION_NORMALIZED = 'typed_structured_edit_ir_normalized'
CONTEXT_PACK_DIGEST_FIELD = 'codeai_selective_repository_semantic_context_pack_digest'
CONTEXT_RECEIPT_DIGEST_FIELD = 'codeai_selective_repository_semantic_context_receipt_digest'
PROPOSAL_DIGEST_FIELD = 'codeai_typed_structured_edit_proposal_digest'
POLICY_DIGEST_FIELD = 'codeai_typed_structured_edit_policy_digest'
IR_DIGEST_FIELD = 'codeai_typed_structured_edit_ir_digest'
RECEIPT_DIGEST_FIELD = 'codeai_typed_structured_edit_ir_receipt_digest'
OP_CREATE_FILE = 'create_file'
OP_REPLACE_SYMBOL = 'replace_symbol'
OP_INSERT_BEFORE_SYMBOL = 'insert_before_symbol'
OP_INSERT_AFTER_SYMBOL = 'insert_after_symbol'
OP_DELETE_SYMBOL = 'delete_symbol'
SYMBOL_OPERATIONS = {OP_REPLACE_SYMBOL, OP_INSERT_BEFORE_SYMBOL, OP_INSERT_AFTER_SYMBOL, OP_DELETE_SYMBOL}
ALLOWED_OPERATIONS = {OP_CREATE_FILE, *SYMBOL_OPERATIONS}
ALLOWED_LANGUAGES = {'python', 'lean'}
PRECONDITION_PATH_ABSENT = 'path_absent'
PRECONDITION_SYMBOL_EXACT = 'symbol_exact'
PROPOSAL_FIELDS = {'proposal_id', 'proposal_revision', 'expected_context_pack_digest', 'expected_context_receipt_digest', 'repository_snapshot_digest', 'source_commit_sha', 'supporting_context_paths', 'operations', 'requirement_trace_ids', 'test_plan_ids', 'risk_labels', 'unresolved_edit_questions', 'prior_ir_digests', 'proposal_created_epoch', 'claims_authority', PROPOSAL_DIGEST_FIELD}
OPERATION_FIELDS = {'operation_id', 'operation', 'path', 'language', 'precondition_kind', 'anchor_kind', 'anchor_symbol', 'expected_file_digest', 'expected_anchor_digest', 'expected_start_line', 'expected_end_line', 'new_text', 'requirement_trace_ids', 'test_plan_ids', 'risk_labels'}
POLICY_FIELDS = {'expected_repository_full_name', 'expected_source_commit_sha', 'allowed_repository_path_prefixes', 'forbidden_repository_path_prefixes', 'allowed_operations', 'allowed_languages', 'maximum_operations', 'maximum_new_text_bytes_per_operation', 'maximum_total_new_text_bytes', 'maximum_supporting_context_paths', 'maximum_anchor_span_lines', 'maximum_requirement_trace_ids_per_operation', 'maximum_test_plan_ids_per_operation', 'maximum_risk_labels_per_operation', 'maximum_request_age', 'evaluation_epoch', 'require_context_path_for_existing_edit', 'allow_create_file', 'allow_delete_symbol', 'allow_repository_mutation', 'allow_provider_invocation', 'allow_verification_runner_invocation', 'allow_candidate_selection_authority', 'allow_execution_authority', POLICY_DIGEST_FIELD}
_SHA40 = re.compile('^[0-9a-f]{40}$')
_SHA256 = re.compile('^[0-9a-f]{64}$')
_LEAN_DECL = re.compile("^\\s*(?:private\\s+|protected\\s+)?(?:noncomputable\\s+)?(def|theorem|lemma|structure|inductive|abbrev|class|instance)\\s+([A-Za-z_][A-Za-z0-9_'.]*)")

@dataclass(frozen=True)
class SymbolLocation:
    kind: str
    name: str
    start_line: int
    end_line: int
    digest: str

@dataclass(frozen=True)
class CodeAITypedStructuredEditIRResult:
    status: str
    issues: tuple[str, ...]
    typed_edit_ir: dict[str, Any] | None
    receipt: dict[str, Any] | None

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()

def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})

def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result

def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None

def _nat(value: Any, *, positive: bool=False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value

def _strings(value: Any, *, nonempty: bool=False) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    if not all((isinstance(item, str) and item for item in value)):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)) or (nonempty and (not parsed)):
        return None
    return parsed

def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + '_missing_fields:' + ','.join(sorted(missing)))
    if extra:
        issues.append(prefix + '_extra_fields:' + ','.join(sorted(extra)))
    return issues

def _canonical_path(path: Any) -> bool:
    if not isinstance(path, str) or not path or path.startswith('/') or path.endswith('/'):
        return False
    if any((char in path for char in ('\\', '\x00', '\n', '\r'))):
        return False
    return all((part not in ('', '.', '..') for part in path.split('/')))

def _canonical_text(value: Any, *, allow_empty: bool=True) -> bool:
    return isinstance(value, str) and '\x00' not in value and ('\r' not in value) and (allow_empty or bool(value)) and (not value or value.endswith('\n'))

def _path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip('/')
    return path == normalized or path.startswith(normalized + '/')

def _file_digest(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def _language_for_path(path: str) -> str | None:
    return {'.py': 'python', '.lean': 'lean'}.get(PurePosixPath(path).suffix.lower())

def _slice_digest(content: str, start_line: int, end_line: int) -> str:
    lines = content.splitlines(keepends=True)
    selected = ''.join(lines[start_line - 1:end_line])
    return hashlib.sha256(selected.encode('utf-8')).hexdigest()

def _python_locations(content: str) -> list[SymbolLocation]:
    tree = ast.parse(content)
    result: list[SymbolLocation] = []
    for node in tree.body:
        kind = ''
        names: list[str] = []
        if isinstance(node, ast.FunctionDef):
            kind = 'function'
            names = [node.name]
        elif isinstance(node, ast.AsyncFunctionDef):
            kind = 'async_function'
            names = [node.name]
        elif isinstance(node, ast.ClassDef):
            kind = 'class'
            names = [node.name]
        elif isinstance(node, ast.Assign):
            kind = 'assignment'
            names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            kind = 'assignment'
            names = [node.target.id]
        else:
            continue
        start = int(getattr(node, 'lineno', 0))
        decorators = getattr(node, 'decorator_list', ())
        if decorators:
            start = min(start, *(int(item.lineno) for item in decorators))
        end = int(getattr(node, 'end_lineno', start))
        for name in names:
            result.append(SymbolLocation(kind, name, start, end, _slice_digest(content, start, end)))
    return result

def _lean_locations(content: str) -> list[SymbolLocation]:
    lines = content.splitlines(keepends=True)
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines, start=1):
        match = _LEAN_DECL.match(line)
        if match:
            starts.append((index, match.group(1), match.group(2)))
    result: list[SymbolLocation] = []
    for index, (start, kind, name) in enumerate(starts):
        end = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        while end > start and (not lines[end - 1].strip()):
            end -= 1
        result.append(SymbolLocation(kind, name, start, end, _slice_digest(content, start, end)))
    return result

def _locations(language: str, content: str) -> list[SymbolLocation]:
    if language == 'python':
        return _python_locations(content)
    if language == 'lean':
        return _lean_locations(content)
    raise ValueError('unsupported_language')

def _validate_context_pack(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    required = (CONTEXT_PACK_DIGEST_FIELD, 'repository_full_name', 'source_commit_sha', 'repository_snapshot_digest', 'selected_entries', 'selected_file_count', 'codeai_disposition', 'operating_mode', 'repository_snapshot_read_only', 'provider_invoked', 'repository_mutation_performed', 'git_effect_performed', 'candidate_selection_authority_granted', 'execution_authority_granted')
    for field in required:
        if field not in value:
            issues.append('context_pack_missing_field:' + field)
    if issues:
        return issues
    if not isinstance(value[CONTEXT_PACK_DIGEST_FIELD], str) or not _SHA256.fullmatch(value[CONTEXT_PACK_DIGEST_FIELD]):
        issues.append('context_pack_digest_invalid')
    elif value[CONTEXT_PACK_DIGEST_FIELD] != digest_without(value, CONTEXT_PACK_DIGEST_FIELD):
        issues.append('context_pack_digest_mismatch')
    if not isinstance(value['repository_full_name'], str) or not value['repository_full_name']:
        issues.append('context_pack_repository_invalid')
    if not isinstance(value['source_commit_sha'], str) or not _SHA40.fullmatch(value['source_commit_sha']):
        issues.append('context_pack_source_commit_invalid')
    if not isinstance(value['repository_snapshot_digest'], str) or not _SHA256.fullmatch(value['repository_snapshot_digest']):
        issues.append('context_pack_repository_snapshot_digest_invalid')
    if value['codeai_disposition'] != 'selective_repository_semantic_context_pack_built':
        issues.append('context_pack_not_built')
    if value['operating_mode'] != 'context_only':
        issues.append('context_pack_not_context_only')
    if value['repository_snapshot_read_only'] is not True:
        issues.append('context_pack_not_read_only')
    for field in ('provider_invoked', 'repository_mutation_performed', 'git_effect_performed', 'candidate_selection_authority_granted', 'execution_authority_granted'):
        if value[field] is not False:
            issues.append('context_pack_effect_or_authority_present:' + field)
    entries = value['selected_entries']
    if not isinstance(entries, list):
        issues.append('context_pack_selected_entries_not_list')
    else:
        if value['selected_file_count'] != len(entries) or not entries:
            issues.append('context_pack_selected_file_count_invalid')
        paths: set[str] = set()
        for index, entry in enumerate(entries):
            if not isinstance(entry, Mapping):
                issues.append(f'context_pack_entry[{index}]_not_mapping')
                continue
            path = entry.get('path')
            digest = entry.get('content_digest')
            language = entry.get('language')
            declared = entry.get('declared_symbols')
            if not _canonical_path(path):
                issues.append(f'context_pack_entry[{index}]_path_invalid')
            elif path in paths:
                issues.append(f'context_pack_entry[{index}]_duplicate_path')
            else:
                paths.add(path)
            if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
                issues.append(f'context_pack_entry[{index}]_content_digest_invalid')
            if language not in {'python', 'lean', 'json', 'toml', 'yaml', 'markdown', 'text', 'restructuredtext'}:
                issues.append(f'context_pack_entry[{index}]_language_invalid')
            if _strings(declared) is None:
                issues.append(f'context_pack_entry[{index}]_declared_symbols_invalid')
    return issues

def _validate_context_receipt(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    required = (CONTEXT_RECEIPT_DIGEST_FIELD, 'context_pack_digest', 'repository_full_name', 'source_commit_sha', 'repository_snapshot_digest', 'selected_paths', 'codeai_disposition', 'operating_mode', 'repository_snapshot_read_only', 'provider_invoked', 'repository_mutation_performed', 'git_effect_performed', 'candidate_selection_authority_granted', 'execution_authority_granted')
    for field in required:
        if field not in value:
            issues.append('context_receipt_missing_field:' + field)
    if issues:
        return issues
    if not isinstance(value[CONTEXT_RECEIPT_DIGEST_FIELD], str) or not _SHA256.fullmatch(value[CONTEXT_RECEIPT_DIGEST_FIELD]):
        issues.append('context_receipt_digest_invalid')
    elif value[CONTEXT_RECEIPT_DIGEST_FIELD] != digest_without(value, CONTEXT_RECEIPT_DIGEST_FIELD):
        issues.append('context_receipt_digest_mismatch')
    for field in ('context_pack_digest', 'repository_snapshot_digest'):
        if not isinstance(value[field], str) or not _SHA256.fullmatch(value[field]):
            issues.append('context_receipt_invalid_digest:' + field)
    if not isinstance(value['repository_full_name'], str) or not value['repository_full_name']:
        issues.append('context_receipt_repository_invalid')
    if not isinstance(value['source_commit_sha'], str) or not _SHA40.fullmatch(value['source_commit_sha']):
        issues.append('context_receipt_source_commit_invalid')
    if value['codeai_disposition'] != 'selective_repository_semantic_context_pack_built':
        issues.append('context_receipt_not_built')
    if value['operating_mode'] != 'context_only':
        issues.append('context_receipt_not_context_only')
    if value['repository_snapshot_read_only'] is not True:
        issues.append('context_receipt_not_read_only')
    if _strings(value['selected_paths'], nonempty=True) is None:
        issues.append('context_receipt_selected_paths_invalid')
    for field in ('provider_invoked', 'repository_mutation_performed', 'git_effect_performed', 'candidate_selection_authority_granted', 'execution_authority_granted'):
        if value[field] is not False:
            issues.append('context_receipt_effect_or_authority_present:' + field)
    return issues

def _validate_repository(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    for path, content in value.items():
        if not _canonical_path(path):
            issues.append('repository_file_path_invalid:' + str(path))
        if not _canonical_text(content):
            issues.append('repository_file_content_invalid:' + str(path))
    return issues

def _validate_operation(value: Mapping[str, Any], index: int) -> list[str]:
    prefix = f'typed_edit_operation[{index}]'
    issues = _exact_fields(value, OPERATION_FIELDS, prefix)
    if issues:
        return issues
    for field in ('operation_id', 'operation', 'path', 'language', 'precondition_kind'):
        if not isinstance(value[field], str) or not value[field]:
            issues.append(prefix + '_invalid_string:' + field)
    if not _canonical_path(value['path']):
        issues.append(prefix + '_path_invalid')
    if value['operation'] not in ALLOWED_OPERATIONS:
        issues.append(prefix + '_operation_invalid')
    if value['language'] not in ALLOWED_LANGUAGES:
        issues.append(prefix + '_language_invalid')
    if value['precondition_kind'] not in {PRECONDITION_PATH_ABSENT, PRECONDITION_SYMBOL_EXACT}:
        issues.append(prefix + '_precondition_kind_invalid')
    for field in ('anchor_kind', 'anchor_symbol', 'expected_file_digest', 'expected_anchor_digest'):
        if not isinstance(value[field], str):
            issues.append(prefix + '_invalid_string:' + field)
    for field in ('expected_start_line', 'expected_end_line'):
        if _nat(value[field]) is None:
            issues.append(prefix + '_invalid_nat:' + field)
    if not _canonical_text(value['new_text']):
        issues.append(prefix + '_new_text_invalid')
    for field in ('requirement_trace_ids', 'test_plan_ids', 'risk_labels'):
        if _strings(value[field]) is None:
            issues.append(prefix + '_invalid_string_list:' + field)
    return issues

def _validate_proposal(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, PROPOSAL_FIELDS, 'typed_edit_proposal')
    if issues:
        return issues
    for field in ('proposal_id', 'proposal_revision', 'expected_context_pack_digest', 'expected_context_receipt_digest', 'repository_snapshot_digest', 'source_commit_sha'):
        if not isinstance(value[field], str) or not value[field]:
            issues.append('typed_edit_proposal_invalid_string:' + field)
    for field in ('expected_context_pack_digest', 'expected_context_receipt_digest', 'repository_snapshot_digest'):
        if not _SHA256.fullmatch(value[field]):
            issues.append('typed_edit_proposal_invalid_digest:' + field)
    if not _SHA40.fullmatch(value['source_commit_sha']):
        issues.append('typed_edit_proposal_invalid_source_commit')
    for field in ('supporting_context_paths', 'requirement_trace_ids', 'test_plan_ids', 'risk_labels', 'unresolved_edit_questions', 'prior_ir_digests'):
        if _strings(value[field], nonempty=field == 'supporting_context_paths') is None:
            issues.append('typed_edit_proposal_invalid_string_list:' + field)
    if not isinstance(value['operations'], list) or not value['operations']:
        issues.append('typed_edit_proposal_operations_invalid')
    else:
        for index, operation in enumerate(value['operations']):
            if not isinstance(operation, Mapping):
                issues.append(f'typed_edit_operation[{index}]_not_mapping')
            else:
                issues.extend(_validate_operation(operation, index))
    if _nat(value['proposal_created_epoch']) is None:
        issues.append('typed_edit_proposal_created_epoch_invalid')
    if not isinstance(value['claims_authority'], bool):
        issues.append('typed_edit_proposal_claims_authority_invalid')
    if value[PROPOSAL_DIGEST_FIELD] != digest_without(value, PROPOSAL_DIGEST_FIELD):
        issues.append('typed_edit_proposal_digest_mismatch')
    return issues

def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, 'typed_edit_policy')
    if issues:
        return issues
    for field in ('expected_repository_full_name', 'expected_source_commit_sha'):
        if not isinstance(value[field], str) or not value[field]:
            issues.append('typed_edit_policy_invalid_string:' + field)
    if not _SHA40.fullmatch(value['expected_source_commit_sha']):
        issues.append('typed_edit_policy_source_commit_invalid')
    for field in ('allowed_repository_path_prefixes', 'forbidden_repository_path_prefixes', 'allowed_operations', 'allowed_languages'):
        if _strings(value[field], nonempty=field != 'forbidden_repository_path_prefixes') is None:
            issues.append('typed_edit_policy_invalid_string_list:' + field)
    if any((item not in ALLOWED_OPERATIONS for item in value['allowed_operations'])):
        issues.append('typed_edit_policy_operation_invalid')
    if any((item not in ALLOWED_LANGUAGES for item in value['allowed_languages'])):
        issues.append('typed_edit_policy_language_invalid')
    for field in ('maximum_operations', 'maximum_new_text_bytes_per_operation', 'maximum_total_new_text_bytes', 'maximum_supporting_context_paths', 'maximum_anchor_span_lines', 'maximum_requirement_trace_ids_per_operation', 'maximum_test_plan_ids_per_operation', 'maximum_risk_labels_per_operation', 'maximum_request_age'):
        if _nat(value[field], positive=True) is None:
            issues.append('typed_edit_policy_invalid_positive_nat:' + field)
    if _nat(value['evaluation_epoch']) is None:
        issues.append('typed_edit_policy_evaluation_epoch_invalid')
    for field in ('require_context_path_for_existing_edit', 'allow_create_file', 'allow_delete_symbol', 'allow_repository_mutation', 'allow_provider_invocation', 'allow_verification_runner_invocation', 'allow_candidate_selection_authority', 'allow_execution_authority'):
        if not isinstance(value[field], bool):
            issues.append('typed_edit_policy_invalid_bool:' + field)
    if any((not _canonical_path(prefix.rstrip('/')) for prefix in value['allowed_repository_path_prefixes'])):
        issues.append('typed_edit_policy_allowed_prefix_invalid')
    if any((not _canonical_path(prefix.rstrip('/')) for prefix in value['forbidden_repository_path_prefixes'])):
        issues.append('typed_edit_policy_forbidden_prefix_invalid')
    if value[POLICY_DIGEST_FIELD] != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append('typed_edit_policy_digest_mismatch')
    return issues

def _selected_entries(pack: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(item['path']): item for item in pack['selected_entries']}

def _path_allowed(path: str, policy: Mapping[str, Any]) -> bool:
    return any((_path_has_prefix(path, prefix) for prefix in policy['allowed_repository_path_prefixes'])) and (not any((_path_has_prefix(path, prefix) for prefix in policy['forbidden_repository_path_prefixes'])))

def _normalize_symbol_operation(operation: Mapping[str, Any], repository: Mapping[str, str], selected: Mapping[str, Mapping[str, Any]], policy: Mapping[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    operation_id = str(operation['operation_id'])
    path = str(operation['path'])
    issues: list[str] = []
    if path not in repository:
        return (None, [operation_id + ':target_path_missing'])
    if policy['require_context_path_for_existing_edit'] is True and path not in selected:
        issues.append(operation_id + ':target_path_not_in_context_pack')
    if path in selected and selected[path].get('content_digest') != _file_digest(repository[path]):
        issues.append(operation_id + ':context_entry_content_digest_mismatch')
    language = str(operation['language'])
    if path in selected and selected[path].get('language') != language:
        issues.append(operation_id + ':context_entry_language_mismatch')
    inferred = _language_for_path(path)
    if inferred != language:
        issues.append(operation_id + ':target_language_mismatch')
    if operation['precondition_kind'] != PRECONDITION_SYMBOL_EXACT:
        issues.append(operation_id + ':symbol_precondition_kind_required')
    file_digest = _file_digest(repository[path])
    if operation['expected_file_digest'] != file_digest:
        issues.append(operation_id + ':expected_file_digest_mismatch')
    try:
        matches = [item for item in _locations(language, repository[path]) if item.kind == operation['anchor_kind'] and item.name == operation['anchor_symbol']]
    except (SyntaxError, ValueError) as exc:
        return (None, [operation_id + ':target_parse_failed:' + type(exc).__name__])
    if not matches:
        return (None, issues + [operation_id + ':anchor_not_found'])
    if len(matches) != 1:
        return (None, issues + [operation_id + ':anchor_ambiguous'])
    anchor = matches[0]
    if operation['expected_anchor_digest'] != anchor.digest:
        issues.append(operation_id + ':expected_anchor_digest_mismatch')
    if operation['expected_start_line'] != anchor.start_line:
        issues.append(operation_id + ':expected_start_line_mismatch')
    if operation['expected_end_line'] != anchor.end_line:
        issues.append(operation_id + ':expected_end_line_mismatch')
    if anchor.end_line - anchor.start_line + 1 > int(policy['maximum_anchor_span_lines']):
        issues.append(operation_id + ':anchor_span_budget_exceeded')
    if operation['operation'] == OP_DELETE_SYMBOL:
        if policy['allow_delete_symbol'] is not True:
            issues.append(operation_id + ':delete_symbol_not_allowed')
        if operation['new_text'] != '':
            issues.append(operation_id + ':delete_symbol_requires_empty_new_text')
    elif not _canonical_text(operation['new_text'], allow_empty=False):
        issues.append(operation_id + ':nondelete_requires_nonempty_new_text')
    if issues:
        return (None, issues)
    if operation['operation'] == OP_INSERT_BEFORE_SYMBOL:
        application_start = anchor.start_line
        application_end = anchor.start_line - 1
    elif operation['operation'] == OP_INSERT_AFTER_SYMBOL:
        application_start = anchor.end_line + 1
        application_end = anchor.end_line
    else:
        application_start = anchor.start_line
        application_end = anchor.end_line
    normalized = {'operation_id': operation_id, 'operation': operation['operation'], 'path': path, 'language': language, 'precondition_kind': PRECONDITION_SYMBOL_EXACT, 'anchor_kind': anchor.kind, 'anchor_symbol': anchor.name, 'resolved_start_line': anchor.start_line, 'resolved_end_line': anchor.end_line, 'application_start_line': application_start, 'application_end_line': application_end, 'file_digest': file_digest, 'anchor_digest': anchor.digest, 'context_entry_content_digest': selected[path]['content_digest'] if path in selected else '', 'new_text': operation['new_text'], 'new_text_digest': hashlib.sha256(operation['new_text'].encode('utf-8')).hexdigest(), 'new_text_bytes': len(operation['new_text'].encode('utf-8')), 'requirement_trace_ids': list(operation['requirement_trace_ids']), 'test_plan_ids': list(operation['test_plan_ids']), 'risk_labels': list(operation['risk_labels'])}
    return (normalized, [])

def _normalize_create_operation(operation: Mapping[str, Any], repository: Mapping[str, str], policy: Mapping[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    operation_id = str(operation['operation_id'])
    path = str(operation['path'])
    issues: list[str] = []
    if policy['allow_create_file'] is not True:
        issues.append(operation_id + ':create_file_not_allowed')
    if path in repository:
        issues.append(operation_id + ':create_file_path_already_exists')
    inferred = _language_for_path(path)
    if inferred != operation['language']:
        issues.append(operation_id + ':create_file_language_mismatch')
    if operation['precondition_kind'] != PRECONDITION_PATH_ABSENT:
        issues.append(operation_id + ':create_file_path_absent_precondition_required')
    for field in ('anchor_kind', 'anchor_symbol', 'expected_file_digest', 'expected_anchor_digest'):
        if operation[field] != '':
            issues.append(operation_id + ':create_file_requires_empty_' + field)
    if operation['expected_start_line'] != 0 or operation['expected_end_line'] != 0:
        issues.append(operation_id + ':create_file_requires_zero_lines')
    if not _canonical_text(operation['new_text'], allow_empty=False):
        issues.append(operation_id + ':create_file_requires_nonempty_new_text')
    if issues:
        return (None, issues)
    normalized = {'operation_id': operation_id, 'operation': OP_CREATE_FILE, 'path': path, 'language': operation['language'], 'precondition_kind': PRECONDITION_PATH_ABSENT, 'anchor_kind': '', 'anchor_symbol': '', 'resolved_start_line': 0, 'resolved_end_line': 0, 'application_start_line': 0, 'application_end_line': 0, 'file_digest': '', 'anchor_digest': '', 'context_entry_content_digest': '', 'new_text': operation['new_text'], 'new_text_digest': hashlib.sha256(operation['new_text'].encode('utf-8')).hexdigest(), 'new_text_bytes': len(operation['new_text'].encode('utf-8')), 'requirement_trace_ids': list(operation['requirement_trace_ids']), 'test_plan_ids': list(operation['test_plan_ids']), 'risk_labels': list(operation['risk_labels'])}
    return (normalized, [])

def _normalize_operations(proposal: Mapping[str, Any], repository: Mapping[str, str], pack: Mapping[str, Any], policy: Mapping[str, Any]) -> tuple[list[dict[str, Any]] | None, tuple[str, ...]]:
    selected = _selected_entries(pack)
    issues: list[str] = []
    normalized: list[dict[str, Any]] = []
    ids: set[str] = set()
    targets: set[tuple[str, str, str]] = set()
    create_paths: set[str] = set()
    total_new_text_bytes = 0
    for operation in proposal['operations']:
        operation_id = str(operation['operation_id'])
        if operation_id in ids:
            issues.append('duplicate_operation_id:' + operation_id)
            continue
        ids.add(operation_id)
        if operation['operation'] not in policy['allowed_operations']:
            issues.append(operation_id + ':operation_not_allowed')
        if operation['language'] not in policy['allowed_languages']:
            issues.append(operation_id + ':language_not_allowed')
        if not _path_allowed(operation['path'], policy):
            issues.append(operation_id + ':target_path_not_allowed')
        new_text_bytes = len(operation['new_text'].encode('utf-8'))
        if new_text_bytes > int(policy['maximum_new_text_bytes_per_operation']):
            issues.append(operation_id + ':new_text_budget_exceeded')
        total_new_text_bytes += new_text_bytes
        for field, maximum in (('requirement_trace_ids', policy['maximum_requirement_trace_ids_per_operation']), ('test_plan_ids', policy['maximum_test_plan_ids_per_operation']), ('risk_labels', policy['maximum_risk_labels_per_operation'])):
            if len(operation[field]) > int(maximum):
                issues.append(operation_id + ':' + field + '_budget_exceeded')
        if operation['operation'] == OP_CREATE_FILE:
            if operation['path'] in create_paths:
                issues.append(operation_id + ':duplicate_create_path')
            create_paths.add(operation['path'])
            item, item_issues = _normalize_create_operation(operation, repository, policy)
        else:
            target = (str(operation['path']), str(operation['anchor_kind']), str(operation['anchor_symbol']))
            if target in targets:
                issues.append(operation_id + ':duplicate_symbol_target')
            targets.add(target)
            item, item_issues = _normalize_symbol_operation(operation, repository, selected, policy)
        issues.extend(item_issues)
        if item is not None:
            normalized.append(item)
    if len(proposal['operations']) > int(policy['maximum_operations']):
        issues.append('typed_edit_operation_budget_exceeded')
    if total_new_text_bytes > int(policy['maximum_total_new_text_bytes']):
        issues.append('typed_edit_total_new_text_budget_exceeded')
    if issues:
        return (None, tuple(sorted(set(issues))))
    normalized.sort(key=lambda item: (item['path'], -int(item['application_start_line']), item['operation_id']))
    for index, item in enumerate(normalized, start=1):
        item['application_sequence'] = index
    return (normalized, ())

def _build_ir(pack: Mapping[str, Any], receipt: Mapping[str, Any], proposal: Mapping[str, Any], policy: Mapping[str, Any], operations: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    total_new_text_bytes = sum((int(item['new_text_bytes']) for item in operations))
    value = {'schema_version': SCHEMA_VERSION, 'profile_version': PROFILE_VERSION, 'context_pack_digest': pack[CONTEXT_PACK_DIGEST_FIELD], 'context_receipt_digest': receipt[CONTEXT_RECEIPT_DIGEST_FIELD], 'repository_full_name': pack['repository_full_name'], 'source_commit_sha': pack['source_commit_sha'], 'repository_snapshot_digest': pack['repository_snapshot_digest'], 'typed_edit_proposal_digest': proposal[PROPOSAL_DIGEST_FIELD], 'typed_edit_policy_digest': policy[POLICY_DIGEST_FIELD], 'proposal_id': proposal['proposal_id'], 'proposal_revision': proposal['proposal_revision'], 'supporting_context_paths': list(proposal['supporting_context_paths']), 'operation_count': len(operations), 'total_new_text_bytes': total_new_text_bytes, 'operations': list(operations), 'requirement_trace_ids': list(proposal['requirement_trace_ids']), 'test_plan_ids': list(proposal['test_plan_ids']), 'risk_labels': list(proposal['risk_labels']), 'unresolved_edit_questions': [], 'codeai_disposition': DISPOSITION_NORMALIZED, 'operating_mode': MODE_TYPED_IR_ONLY, 'typed_operations_only': True, 'whole_file_modify_allowed': False, 'symbol_preconditions_verified': True, 'context_lineage_verified': True, 'repository_snapshot_read_only': True, 'provider_invoked': False, 'verification_runner_invoked': False, 'repository_mutation_performed': False, 'git_effect_performed': False, 'network_access_performed': False, 'secret_access_performed': False, 'candidate_selected': False, 'candidate_selection_authority_granted': False, 'execution_authority_granted': False, 'merge_authority_granted': False, 'deployment_authority_granted': False, 'typed_ir_treated_as_correctness_proof': False, 'precondition_match_treated_as_semantic_correctness': False, 'history_read_only': True, 'future_only': True, 'active_now': False}
    return seal(value, IR_DIGEST_FIELD)

def _build_receipt(pack: Mapping[str, Any], context_receipt: Mapping[str, Any], proposal: Mapping[str, Any], policy: Mapping[str, Any], typed_ir: Mapping[str, Any]) -> dict[str, Any]:
    value = {'schema_version': SCHEMA_VERSION, 'profile_version': PROFILE_VERSION, 'context_pack_digest': pack[CONTEXT_PACK_DIGEST_FIELD], 'context_receipt_digest': context_receipt[CONTEXT_RECEIPT_DIGEST_FIELD], 'typed_edit_proposal_digest': proposal[PROPOSAL_DIGEST_FIELD], 'typed_edit_policy_digest': policy[POLICY_DIGEST_FIELD], 'typed_edit_ir_digest': typed_ir[IR_DIGEST_FIELD], 'repository_full_name': pack['repository_full_name'], 'source_commit_sha': pack['source_commit_sha'], 'repository_snapshot_digest': pack['repository_snapshot_digest'], 'operation_count': typed_ir['operation_count'], 'operation_ids': [item['operation_id'] for item in typed_ir['operations']], 'target_paths': sorted({item['path'] for item in typed_ir['operations']}), 'total_new_text_bytes': typed_ir['total_new_text_bytes'], 'codeai_disposition': DISPOSITION_NORMALIZED, 'operating_mode': MODE_TYPED_IR_ONLY, 'route_receipt_recorded': True, 'typed_structured_edit_ir_emitted': True, 'typed_operations_only': True, 'whole_file_modify_allowed': False, 'symbol_preconditions_verified': True, 'context_lineage_verified': True, 'repository_snapshot_read_only': True, 'provider_invoked': False, 'verification_runner_invoked': False, 'repository_mutation_performed': False, 'git_effect_performed': False, 'network_access_performed': False, 'secret_access_performed': False, 'candidate_selected': False, 'candidate_selection_authority_granted': False, 'execution_authority_granted': False, 'merge_authority_granted': False, 'deployment_authority_granted': False, 'typed_ir_treated_as_correctness_proof': False, 'precondition_match_treated_as_semantic_correctness': False, 'history_read_only': True, 'future_only': True, 'active_now': False}
    return seal(value, RECEIPT_DIGEST_FIELD)

def build_codeai_typed_structured_edit_ir(*, context_pack: Any, context_receipt: Any, repository_files: Any, typed_edit_proposal: Any, typed_edit_policy: Any) -> CodeAITypedStructuredEditIRResult:
    pack = _mapping(context_pack)
    receipt = _mapping(context_receipt)
    repository = _mapping(repository_files)
    proposal = _mapping(typed_edit_proposal)
    policy = _mapping(typed_edit_policy)
    issues: list[str] = []
    if pack is None:
        issues.append('context_pack_not_mapping')
    else:
        issues.extend(_validate_context_pack(pack))
    if receipt is None:
        issues.append('context_receipt_not_mapping')
    else:
        issues.extend(_validate_context_receipt(receipt))
    if repository is None:
        issues.append('repository_files_not_mapping')
    else:
        issues.extend(_validate_repository(repository))
    if proposal is None:
        issues.append('typed_edit_proposal_not_mapping')
    else:
        issues.extend(_validate_proposal(proposal))
    if policy is None:
        issues.append('typed_edit_policy_not_mapping')
    else:
        issues.extend(_validate_policy(policy))
    if issues or None in (pack, receipt, repository, proposal, policy):
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, tuple(sorted(set(issues))), None, None)
    assert pack is not None and receipt is not None and (repository is not None)
    assert proposal is not None and policy is not None
    effect_fields = ('allow_repository_mutation', 'allow_provider_invocation', 'allow_verification_runner_invocation', 'allow_candidate_selection_authority', 'allow_execution_authority')
    if any((policy[field] is True for field in effect_fields)):
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, ('typed_edit_policy_effect_or_authority_enabled',), None, None)
    if proposal['claims_authority'] is True:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, ('typed_edit_proposal_claims_authority',), None, None)
    if proposal['unresolved_edit_questions']:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, ('typed_edit_unresolved_questions_present',), None, None)
    selected_paths = [item['path'] for item in pack['selected_entries']]
    correspondence = (('context_pack_digest_mismatch', proposal['expected_context_pack_digest'], pack[CONTEXT_PACK_DIGEST_FIELD]), ('context_receipt_digest_mismatch', proposal['expected_context_receipt_digest'], receipt[CONTEXT_RECEIPT_DIGEST_FIELD]), ('context_receipt_pack_digest_mismatch', receipt['context_pack_digest'], pack[CONTEXT_PACK_DIGEST_FIELD]), ('repository_full_name_mismatch', policy['expected_repository_full_name'], pack['repository_full_name']), ('source_commit_sha_mismatch', proposal['source_commit_sha'], pack['source_commit_sha']), ('policy_source_commit_sha_mismatch', policy['expected_source_commit_sha'], pack['source_commit_sha']), ('repository_snapshot_digest_mismatch', proposal['repository_snapshot_digest'], canonical_digest(repository)), ('context_pack_repository_snapshot_digest_mismatch', pack['repository_snapshot_digest'], canonical_digest(repository)), ('context_receipt_repository_snapshot_digest_mismatch', receipt['repository_snapshot_digest'], canonical_digest(repository)), ('context_receipt_selected_paths_mismatch', receipt['selected_paths'], selected_paths))
    mismatches = tuple((issue for issue, expected, observed in correspondence if expected != observed))
    if mismatches:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, mismatches, None, None)
    supporting = tuple(proposal['supporting_context_paths'])
    if len(supporting) > int(policy['maximum_supporting_context_paths']):
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, ('supporting_context_path_budget_exceeded',), None, None)
    missing_support = sorted(set(supporting).difference(selected_paths))
    if missing_support:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, tuple(('supporting_context_path_not_selected:' + path for path in missing_support)), None, None)
    selected_entry_map = _selected_entries(pack)
    support_digest_drift = sorted((path for path in supporting if path not in repository or selected_entry_map[path].get('content_digest') != _file_digest(repository[path])))
    if support_digest_drift:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, tuple(('supporting_context_content_digest_mismatch:' + path for path in support_digest_drift)), None, None)
    existing_targets = {operation['path'] for operation in proposal['operations'] if operation['operation'] in SYMBOL_OPERATIONS}
    unsupported_targets = sorted(existing_targets.difference(supporting))
    if policy['require_context_path_for_existing_edit'] is True and unsupported_targets:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, tuple(('existing_target_not_declared_as_support:' + path for path in unsupported_targets)), None, None)
    evaluation = int(policy['evaluation_epoch'])
    created = int(proposal['proposal_created_epoch'])
    if not evaluation - int(policy['maximum_request_age']) <= created <= evaluation:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, ('typed_edit_proposal_window_invalid',), None, None)
    operations, operation_issues = _normalize_operations(proposal, repository, pack, policy)
    if operations is None:
        return CodeAITypedStructuredEditIRResult(STATUS_BLOCKED, operation_issues, None, None)
    typed_ir = _build_ir(pack, receipt, proposal, policy, operations)
    route_receipt = _build_receipt(pack, receipt, proposal, policy, typed_ir)
    return CodeAITypedStructuredEditIRResult(STATUS_READY, (), typed_ir, route_receipt)
__all__ = [name for name in globals() if name.isupper()] + ['CodeAITypedStructuredEditIRResult', 'SymbolLocation', 'build_codeai_typed_structured_edit_ir', 'canonical_digest', 'canonical_json', 'digest_without', 'seal']
