#!/usr/bin/env python3
from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import json
import re
import tomllib
from pathlib import PurePosixPath
from typing import Any, Mapping, Sequence

VERSION = "kuuos_codeai_selective_repository_semantic_context_pack_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Selective Repository Semantic Context Pack v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_CONTEXT_ONLY = "context_only"
MODE_ABSTAIN = "abstain"
DISPOSITION_BUILT = "selective_repository_semantic_context_pack_built"
DISPOSITION_ABSTAINED = "no_relevant_repository_semantic_context_abstained"

SOURCE_RECEIPT_DIGEST_FIELD = "codeai_intent_repository_observation_receipt_digest"
REQUEST_DIGEST_FIELD = "codeai_selective_repository_semantic_context_request_digest"
POLICY_DIGEST_FIELD = "codeai_selective_repository_semantic_context_policy_digest"
PACK_DIGEST_FIELD = "codeai_selective_repository_semantic_context_pack_digest"
RECEIPT_DIGEST_FIELD = "codeai_selective_repository_semantic_context_receipt_digest"

REQUEST_FIELDS = {
    "request_id",
    "request_revision",
    "intent_text",
    "query_terms",
    "target_path_prefixes",
    "target_symbols",
    "test_plan_ids",
    "required_roles",
    "request_created_epoch",
    "repository_snapshot_digest",
    "expected_source_observation_receipt_digest",
    "prior_pack_digests",
    "unresolved_context_questions",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "allowed_repository_path_prefixes",
    "forbidden_repository_path_prefixes",
    "supported_file_suffixes",
    "maximum_repository_snapshot_bytes",
    "maximum_candidate_files",
    "maximum_selected_files",
    "maximum_file_bytes",
    "maximum_excerpt_bytes",
    "maximum_total_context_bytes",
    "maximum_symbols_per_file",
    "maximum_imports_per_file",
    "maximum_query_terms",
    "maximum_request_age",
    "evaluation_epoch",
    "allow_text_fallback",
    "require_relevant_context",
    "allow_empty_context_abstention",
    "allow_repository_mutation",
    "allow_network_access",
    "allow_secret_access",
    "allow_candidate_selection_authority",
    "allow_execution_authority",
    POLICY_DIGEST_FIELD,
}

_ALLOWED_ROLES = {"source", "test", "formal", "config", "workflow", "documentation"}
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_LEAN_IMPORT = re.compile(r"^\s*import\s+([A-Za-z0-9_.'/-]+)")
_LEAN_DECL = re.compile(
    r"^\s*(?:private\s+|protected\s+)?(?:noncomputable\s+)?"
    r"(?:def|theorem|lemma|structure|inductive|abbrev|class|instance)\s+"
    r"([A-Za-z_][A-Za-z0-9_'.]*)"
)


@dataclass(frozen=True)
class CodeAISelectiveRepositorySemanticContextResult:
    status: str
    issues: tuple[str, ...]
    context_pack: dict[str, Any] | None
    receipt: dict[str, Any] | None


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def digest_without(value: Mapping[str, Any], field: str) -> str:
    return canonical_digest({key: item for key, item in value.items() if key != field})


def seal(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = canonical_digest(result)
    return result


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def _strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    if not all(isinstance(item, str) and item for item in value):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)) or (nonempty and not parsed):
        return None
    return parsed


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _canonical_path(path: Any) -> bool:
    if not isinstance(path, str) or not path or path.startswith("/") or path.endswith("/"):
        return False
    if any(char in path for char in ("\\", "\0", "\n", "\r")):
        return False
    return all(part not in ("", ".", "..") for part in path.split("/"))


def _canonical_text(value: Any) -> bool:
    return isinstance(value, str) and "\0" not in value and "\r" not in value and (
        not value or value.endswith("\n")
    )


def _path_has_prefix(path: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/")
    return path == normalized or path.startswith(normalized + "/")


def _validate_source_receipt(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    required = (
        SOURCE_RECEIPT_DIGEST_FIELD,
        "codeai_disposition",
        "operating_mode",
        "repository_observation_read_only",
        "repository_mutation_performed",
        "repository_full_name",
        "source_commit_sha",
        "tree_digest",
    )
    for field in required:
        if field not in value:
            issues.append("source_observation_receipt_missing_field:" + field)
    if issues:
        return issues
    if not isinstance(value[SOURCE_RECEIPT_DIGEST_FIELD], str) or not _SHA256.fullmatch(
        value[SOURCE_RECEIPT_DIGEST_FIELD]
    ):
        issues.append("source_observation_receipt_digest_invalid")
    elif value[SOURCE_RECEIPT_DIGEST_FIELD] != digest_without(
        value, SOURCE_RECEIPT_DIGEST_FIELD
    ):
        issues.append("source_observation_receipt_digest_mismatch")
    if value["codeai_disposition"] != "intent_repository_observation_supported":
        issues.append("source_observation_receipt_not_supported")
    if value["operating_mode"] != "read_only" or value["repository_observation_read_only"] is not True:
        issues.append("source_observation_receipt_not_read_only")
    if value["repository_mutation_performed"] is not False:
        issues.append("source_observation_receipt_reports_mutation")
    if not isinstance(value["repository_full_name"], str) or not value["repository_full_name"]:
        issues.append("source_observation_receipt_repository_invalid")
    if not isinstance(value["source_commit_sha"], str) or not _SHA40.fullmatch(
        value["source_commit_sha"]
    ):
        issues.append("source_observation_receipt_commit_invalid")
    if not isinstance(value["tree_digest"], str) or not value["tree_digest"]:
        issues.append("source_observation_receipt_tree_digest_invalid")
    return issues


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "context_request")
    if issues:
        return issues
    for field in ("request_id", "request_revision", "intent_text"):
        if not isinstance(value[field], str) or not value[field]:
            issues.append("context_request_invalid_string:" + field)
    for field in (
        "query_terms",
        "target_path_prefixes",
        "target_symbols",
        "test_plan_ids",
        "required_roles",
        "prior_pack_digests",
        "unresolved_context_questions",
    ):
        parsed = _strings(value[field], nonempty=(field == "query_terms"))
        if parsed is None:
            issues.append("context_request_invalid_string_list:" + field)
    if _nat(value["request_created_epoch"]) is None:
        issues.append("context_request_invalid_created_epoch")
    for field in ("repository_snapshot_digest", "expected_source_observation_receipt_digest"):
        if not isinstance(value[field], str) or not _SHA256.fullmatch(value[field]):
            issues.append("context_request_invalid_digest:" + field)
    if any(role not in _ALLOWED_ROLES for role in value["required_roles"]):
        issues.append("context_request_invalid_required_role")
    if any(not _canonical_path(prefix.rstrip("/")) for prefix in value["target_path_prefixes"]):
        issues.append("context_request_invalid_target_path_prefix")
    if value[REQUEST_DIGEST_FIELD] != digest_without(value, REQUEST_DIGEST_FIELD):
        issues.append("context_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "context_policy")
    if issues:
        return issues
    for field in ("expected_repository_full_name", "expected_source_commit_sha"):
        if not isinstance(value[field], str) or not value[field]:
            issues.append("context_policy_invalid_string:" + field)
    if not _SHA40.fullmatch(value["expected_source_commit_sha"]):
        issues.append("context_policy_invalid_source_commit")
    for field in (
        "allowed_repository_path_prefixes",
        "forbidden_repository_path_prefixes",
        "supported_file_suffixes",
    ):
        parsed = _strings(value[field], nonempty=(field != "forbidden_repository_path_prefixes"))
        if parsed is None:
            issues.append("context_policy_invalid_string_list:" + field)
    for field in (
        "maximum_repository_snapshot_bytes",
        "maximum_candidate_files",
        "maximum_selected_files",
        "maximum_file_bytes",
        "maximum_excerpt_bytes",
        "maximum_total_context_bytes",
        "maximum_symbols_per_file",
        "maximum_imports_per_file",
        "maximum_query_terms",
        "maximum_request_age",
    ):
        if _nat(value[field], positive=True) is None:
            issues.append("context_policy_invalid_positive_nat:" + field)
    if _nat(value["evaluation_epoch"]) is None:
        issues.append("context_policy_invalid_evaluation_epoch")
    for field in (
        "allow_text_fallback",
        "require_relevant_context",
        "allow_empty_context_abstention",
        "allow_repository_mutation",
        "allow_network_access",
        "allow_secret_access",
        "allow_candidate_selection_authority",
        "allow_execution_authority",
    ):
        if not isinstance(value[field], bool):
            issues.append("context_policy_invalid_bool:" + field)
    if any(not suffix.startswith(".") for suffix in value["supported_file_suffixes"]):
        issues.append("context_policy_invalid_supported_suffix")
    if any(not _canonical_path(prefix.rstrip("/")) for prefix in value["allowed_repository_path_prefixes"]):
        issues.append("context_policy_invalid_allowed_prefix")
    if any(not _canonical_path(prefix.rstrip("/")) for prefix in value["forbidden_repository_path_prefixes"]):
        issues.append("context_policy_invalid_forbidden_prefix")
    if value[POLICY_DIGEST_FIELD] != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("context_policy_digest_mismatch")
    return issues


def _validate_repository(value: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    for path, content in value.items():
        if not _canonical_path(path):
            issues.append("repository_file_path_invalid:" + str(path))
        if not _canonical_text(content):
            issues.append("repository_file_content_invalid:" + str(path))
    return issues


def _role(path: str) -> str:
    pure = PurePosixPath(path)
    suffix = pure.suffix.lower()
    parts = pure.parts
    name = pure.name.lower()
    if path.startswith(".github/workflows/"):
        return "workflow"
    if "tests" in parts or name.startswith("test_") or name.endswith("_test.py"):
        return "test"
    if "formal" in parts or suffix == ".lean":
        return "formal"
    if suffix in {".json", ".toml", ".yaml", ".yml"}:
        return "config"
    if suffix in {".md", ".rst", ".txt"}:
        return "documentation"
    return "source"


def _language(path: str) -> str:
    suffix = PurePosixPath(path).suffix.lower()
    return {
        ".py": "python",
        ".lean": "lean",
        ".json": "json",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".md": "markdown",
        ".rst": "restructuredtext",
        ".txt": "text",
    }.get(suffix, "text")


def _python_semantics(content: str) -> tuple[list[str], list[str], str]:
    tree = ast.parse(content)
    imports: list[str] = []
    symbols: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets: Sequence[ast.expr]
            if isinstance(node, ast.Assign):
                targets = node.targets
            else:
                targets = [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id.isidentifier():
                    symbols.append(target.id)
    return imports, symbols, "parsed"


def _lean_semantics(content: str) -> tuple[list[str], list[str], str]:
    imports: list[str] = []
    symbols: list[str] = []
    for line in content.splitlines():
        match = _LEAN_IMPORT.match(line)
        if match:
            imports.append(match.group(1))
        match = _LEAN_DECL.match(line)
        if match:
            symbols.append(match.group(1))
    return imports, symbols, "parsed"


def _config_semantics(language: str, content: str) -> tuple[list[str], list[str], str]:
    if language == "json":
        parsed = json.loads(content)
        symbols = list(parsed.keys()) if isinstance(parsed, dict) else []
        return [], [str(item) for item in symbols], "parsed"
    if language == "toml":
        parsed = tomllib.loads(content)
        return [], [str(item) for item in parsed.keys()], "parsed"
    return [], [], "fallback"


def _generic_semantics(content: str) -> tuple[list[str], list[str], str]:
    headings: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                headings.append(heading)
    return [], headings, "fallback"


def _semantic_facts(
    path: str, content: str, allow_text_fallback: bool
) -> tuple[list[str], list[str], str, str | None]:
    language = _language(path)
    try:
        if language == "python":
            imports, symbols, status = _python_semantics(content)
        elif language == "lean":
            imports, symbols, status = _lean_semantics(content)
        elif language in {"json", "toml", "yaml"}:
            imports, symbols, status = _config_semantics(language, content)
        else:
            imports, symbols, status = _generic_semantics(content)
        return imports, symbols, status, None
    except (SyntaxError, ValueError, tomllib.TOMLDecodeError) as exc:
        if allow_text_fallback:
            imports, symbols, _ = _generic_semantics(content)
            return imports, symbols, "fallback", type(exc).__name__
        return [], [], "parse_failed", type(exc).__name__


def _unique_limited(items: Sequence[str], limit: int) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item and item not in seen:
            result.append(item)
            seen.add(item)
            if len(result) >= limit:
                break
    return result


def _score(
    *,
    path: str,
    role: str,
    content: str,
    imports: Sequence[str],
    symbols: Sequence[str],
    request: Mapping[str, Any],
) -> tuple[int, list[str], set[int]]:
    score = 0
    reasons: list[str] = []
    line_hits: set[int] = set()
    lowered_path = path.casefold()
    lowered_content = content.casefold()
    lines = content.splitlines()

    for prefix in request["target_path_prefixes"]:
        if _path_has_prefix(path, prefix):
            reasons.append("target_path_scope:" + prefix)

    symbols_folded = {item.casefold(): item for item in symbols}
    for symbol in request["target_symbols"]:
        folded = symbol.casefold()
        if folded in symbols_folded:
            score += 80
            reasons.append("target_symbol:" + symbol)
        for index, line in enumerate(lines, start=1):
            if folded in line.casefold():
                line_hits.add(index)

    import_text = " ".join(imports).casefold()
    symbol_text = " ".join(symbols).casefold()
    for term in request["query_terms"]:
        folded = term.casefold()
        if folded in lowered_path:
            score += 30
            reasons.append("query_path:" + term)
        if folded in symbol_text:
            score += 20
            reasons.append("query_symbol:" + term)
        if folded in import_text:
            score += 15
            reasons.append("query_import:" + term)
        if folded in lowered_content:
            score += 5
            reasons.append("query_content:" + term)
        for index, line in enumerate(lines, start=1):
            if folded in line.casefold():
                line_hits.add(index)

    if score > 0 and role in request["required_roles"]:
        score += 20
        reasons.append("required_role:" + role)
    if score > 0 and request["test_plan_ids"] and role == "test":
        score += 10
        reasons.append("test_plan_support")
    return score, sorted(set(reasons)), line_hits


def _excerpt_lines(
    content: str, line_hits: set[int], maximum_excerpt_bytes: int
) -> tuple[list[dict[str, Any]], int]:
    lines = content.splitlines()
    selected: set[int] = set()
    for line in line_hits:
        selected.update(item for item in (line - 1, line, line + 1) if 1 <= item <= len(lines))
    if not selected:
        selected.update(range(1, min(len(lines), 12) + 1))
    result: list[dict[str, Any]] = []
    used = 0
    for line_number in sorted(selected):
        item = {"line": line_number, "text": lines[line_number - 1]}
        size = len(canonical_json(item).encode("utf-8"))
        if result and used + size > maximum_excerpt_bytes:
            break
        if not result and size > maximum_excerpt_bytes:
            encoded = item["text"].encode("utf-8")[: max(0, maximum_excerpt_bytes // 2)]
            item["text"] = encoded.decode("utf-8", errors="ignore")
            size = len(canonical_json(item).encode("utf-8"))
        result.append(item)
        used += size
    return result, used


def _build_pack(
    source: Mapping[str, Any],
    repository: Mapping[str, str],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, tuple[str, ...]]:
    supported_suffixes = set(policy["supported_file_suffixes"])
    allowed = tuple(policy["allowed_repository_path_prefixes"])
    forbidden = tuple(policy["forbidden_repository_path_prefixes"])
    candidates: list[dict[str, Any]] = []
    issues: list[str] = []
    oversized_paths: list[str] = []

    for path in sorted(repository):
        suffix = PurePosixPath(path).suffix.lower()
        if suffix not in supported_suffixes:
            continue
        if not any(_path_has_prefix(path, prefix) for prefix in allowed):
            continue
        if any(_path_has_prefix(path, prefix) for prefix in forbidden):
            continue
        content = repository[path]
        file_bytes = len(content.encode("utf-8"))
        if file_bytes > int(policy["maximum_file_bytes"]):
            oversized_paths.append(path)
            continue
        imports, symbols, parse_status, parse_error = _semantic_facts(
            path, content, bool(policy["allow_text_fallback"])
        )
        score, reasons, line_hits = _score(
            path=path,
            role=_role(path),
            content=content,
            imports=imports,
            symbols=symbols,
            request=request,
        )
        if score <= 0:
            continue
        if parse_status == "parse_failed":
            issues.append("semantic_parse_failed:" + path + ":" + str(parse_error))
            continue
        excerpt, excerpt_bytes = _excerpt_lines(
            content, line_hits, int(policy["maximum_excerpt_bytes"])
        )
        candidates.append(
            {
                "path": path,
                "content_digest": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                "language": _language(path),
                "role": _role(path),
                "score": score,
                "selection_reasons": reasons,
                "parse_status": parse_status,
                "parse_error_type": parse_error or "",
                "imports": _unique_limited(imports, int(policy["maximum_imports_per_file"])),
                "declared_symbols": _unique_limited(
                    symbols, int(policy["maximum_symbols_per_file"])
                ),
                "excerpt_lines": excerpt,
                "excerpt_bytes": excerpt_bytes,
            }
        )

    if issues:
        return None, tuple(sorted(set(issues)))
    if len(candidates) > int(policy["maximum_candidate_files"]):
        return None, ("semantic_candidate_file_budget_exceeded",)

    candidates.sort(key=lambda item: (-int(item["score"]), item["path"]))
    selected: list[dict[str, Any]] = []
    total_bytes = 0
    omitted_relevant = 0
    for candidate in candidates:
        if len(selected) >= int(policy["maximum_selected_files"]):
            omitted_relevant += 1
            continue
        entry_bytes = len(canonical_json(candidate).encode("utf-8"))
        if selected and total_bytes + entry_bytes > int(policy["maximum_total_context_bytes"]):
            omitted_relevant += 1
            continue
        if not selected and entry_bytes > int(policy["maximum_total_context_bytes"]):
            omitted_relevant += 1
            continue
        selected.append(candidate)
        total_bytes += entry_bytes

    if not selected and policy["require_relevant_context"] is True:
        if policy["allow_empty_context_abstention"] is not True:
            return None, ("no_relevant_semantic_context",)

    disposition = DISPOSITION_BUILT if selected else DISPOSITION_ABSTAINED
    operating_mode = MODE_CONTEXT_ONLY if selected else MODE_ABSTAIN
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_observation_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "repository_full_name": source["repository_full_name"],
        "source_commit_sha": source["source_commit_sha"],
        "source_tree_digest": source["tree_digest"],
        "repository_snapshot_digest": request["repository_snapshot_digest"],
        "context_request_digest": request[REQUEST_DIGEST_FIELD],
        "context_policy_digest": policy[POLICY_DIGEST_FIELD],
        "query_terms": list(request["query_terms"]),
        "target_path_prefixes": list(request["target_path_prefixes"]),
        "target_symbols": list(request["target_symbols"]),
        "test_plan_ids": list(request["test_plan_ids"]),
        "required_roles": list(request["required_roles"]),
        "selected_file_count": len(selected),
        "selected_total_context_bytes": total_bytes,
        "relevant_candidate_count": len(candidates),
        "omitted_relevant_file_count": omitted_relevant,
        "oversized_eligible_paths": oversized_paths,
        "selected_entries": selected,
        "unresolved_context_questions": list(request["unresolved_context_questions"]),
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "selective_retrieval_performed": True,
        "full_repository_forwarded": False,
        "repository_snapshot_read_only": True,
        "provider_invoked": False,
        "verification_runner_invoked": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "network_access_performed": False,
        "secret_access_performed": False,
        "context_selection_authority_only": True,
        "candidate_selection_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "repository_content_treated_as_truth": False,
        "semantic_match_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, PACK_DIGEST_FIELD), ()


def _receipt(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    pack: Mapping[str, Any],
) -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_observation_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "context_request_digest": request[REQUEST_DIGEST_FIELD],
        "context_policy_digest": policy[POLICY_DIGEST_FIELD],
        "context_pack_digest": pack[PACK_DIGEST_FIELD],
        "repository_full_name": source["repository_full_name"],
        "source_commit_sha": source["source_commit_sha"],
        "repository_snapshot_digest": request["repository_snapshot_digest"],
        "selected_file_count": pack["selected_file_count"],
        "selected_paths": [item["path"] for item in pack["selected_entries"]],
        "selected_total_context_bytes": pack["selected_total_context_bytes"],
        "codeai_disposition": pack["codeai_disposition"],
        "operating_mode": pack["operating_mode"],
        "route_receipt_recorded": True,
        "semantic_context_pack_emitted": True,
        "selective_retrieval_performed": True,
        "full_repository_forwarded": False,
        "repository_snapshot_read_only": True,
        "provider_invoked": False,
        "verification_runner_invoked": False,
        "repository_mutation_performed": False,
        "git_effect_performed": False,
        "network_access_performed": False,
        "secret_access_performed": False,
        "candidate_selected": False,
        "candidate_selection_authority_granted": False,
        "execution_authority_granted": False,
        "merge_authority_granted": False,
        "deployment_authority_granted": False,
        "repository_content_treated_as_truth": False,
        "semantic_match_treated_as_correctness_proof": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
    }
    return seal(value, RECEIPT_DIGEST_FIELD)


def build_codeai_selective_repository_semantic_context_pack(
    *,
    source_observation_receipt: Any,
    repository_files: Any,
    context_request: Any,
    context_policy: Any,
) -> CodeAISelectiveRepositorySemanticContextResult:
    source = _mapping(source_observation_receipt)
    repository = _mapping(repository_files)
    request = _mapping(context_request)
    policy = _mapping(context_policy)
    issues: list[str] = []

    if source is None:
        issues.append("source_observation_receipt_not_mapping")
    else:
        issues.extend(_validate_source_receipt(source))
    if repository is None:
        issues.append("repository_files_not_mapping")
    else:
        issues.extend(_validate_repository(repository))
    if request is None:
        issues.append("context_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if policy is None:
        issues.append("context_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))

    if issues or None in (source, repository, request, policy):
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
        )

    assert source is not None and repository is not None
    assert request is not None and policy is not None

    effect_fields = (
        "allow_repository_mutation",
        "allow_network_access",
        "allow_secret_access",
        "allow_candidate_selection_authority",
        "allow_execution_authority",
    )
    if any(policy[field] is True for field in effect_fields):
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, ("context_policy_effect_or_authority_enabled",), None, None
        )

    correspondence = (
        (
            "source_receipt_digest_mismatch",
            request["expected_source_observation_receipt_digest"],
            source[SOURCE_RECEIPT_DIGEST_FIELD],
        ),
        (
            "repository_full_name_mismatch",
            policy["expected_repository_full_name"],
            source["repository_full_name"],
        ),
        (
            "source_commit_sha_mismatch",
            policy["expected_source_commit_sha"],
            source["source_commit_sha"],
        ),
        (
            "repository_snapshot_digest_mismatch",
            request["repository_snapshot_digest"],
            canonical_digest(repository),
        ),
    )
    mismatch = tuple(issue for issue, expected, observed in correspondence if expected != observed)
    if mismatch:
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, mismatch, None, None
        )

    evaluation = int(policy["evaluation_epoch"])
    created = int(request["request_created_epoch"])
    if not evaluation - int(policy["maximum_request_age"]) <= created <= evaluation:
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, ("context_request_window_invalid",), None, None
        )
    if len(request["query_terms"]) > int(policy["maximum_query_terms"]):
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, ("context_query_term_budget_exceeded",), None, None
        )
    repository_bytes = len(canonical_json(repository).encode("utf-8"))
    if repository_bytes > int(policy["maximum_repository_snapshot_bytes"]):
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, ("repository_snapshot_budget_exceeded",), None, None
        )
    for prefix in request["target_path_prefixes"]:
        if not any(
            _path_has_prefix(prefix.rstrip("/"), allowed)
            for allowed in policy["allowed_repository_path_prefixes"]
        ):
            return CodeAISelectiveRepositorySemanticContextResult(
                STATUS_BLOCKED, ("target_path_prefix_not_allowed:" + prefix,), None, None
            )
        if any(
            _path_has_prefix(prefix.rstrip("/"), denied)
            for denied in policy["forbidden_repository_path_prefixes"]
        ):
            return CodeAISelectiveRepositorySemanticContextResult(
                STATUS_BLOCKED, ("target_path_prefix_forbidden:" + prefix,), None, None
            )

    pack, pack_issues = _build_pack(source, repository, request, policy)
    if pack is None:
        return CodeAISelectiveRepositorySemanticContextResult(
            STATUS_BLOCKED, pack_issues, None, None
        )
    receipt = _receipt(source, request, policy, pack)
    return CodeAISelectiveRepositorySemanticContextResult(
        STATUS_READY, (), pack, receipt
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAISelectiveRepositorySemanticContextResult",
    "build_codeai_selective_repository_semantic_context_pack",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
