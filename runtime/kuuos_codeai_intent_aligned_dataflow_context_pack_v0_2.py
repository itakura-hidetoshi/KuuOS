#!/usr/bin/env python3
from __future__ import annotations

import ast
from collections import deque
from dataclasses import dataclass
import re
from pathlib import PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_checks_v0_2 import (
    canonical_digest,
    canonical_json,
    path_has_prefix,
    role_for_path,
    language_for_path,
    seal,
    validate_policy,
    validate_repository,
    validate_request,
    validate_source_receipt,
)
from runtime.kuuos_codeai_intent_aligned_dataflow_context_pack_schema_v0_2 import (
    DISPOSITION_BUILT,
    MODE_CONTEXT_ONLY,
    PACK_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    QUERY_NODE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SCHEMA_VERSION,
    SELECTED_FILE_DIGEST_FIELD,
    SOURCE_RECEIPT_DIGEST_FIELD,
    STATUS_BLOCKED,
    STATUS_READY,
    CodeAIIntentAlignedDataflowContextResult,
)

_LEAN_IMPORT = re.compile(r"^\s*import\s+([A-Za-z0-9_.'/-]+)")
_LEAN_DECL = re.compile(
    r"^\s*(?:private\s+|protected\s+)?(?:noncomputable\s+)?"
    r"(?:def|theorem|lemma|structure|inductive|abbrev|class|instance)\s+"
    r"([A-Za-z_][A-Za-z0-9_'.]*)"
)
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_'.]*")
_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_'-]*")


@dataclass(frozen=True)
class SemanticFacts:
    symbols: tuple[str, ...]
    imports: tuple[str, ...]
    calls: tuple[str, ...]
    type_refs: tuple[str, ...]
    dataflow_edges: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Candidate:
    path: str
    content: str
    role: str
    language: str
    facts: SemanticFacts
    matched_terms: tuple[str, ...]
    matched_hypotheses: tuple[str, ...]
    matched_target_symbols: tuple[str, ...]
    score: int


def _blocked(*issues: str) -> CodeAIIntentAlignedDataflowContextResult:
    return CodeAIIntentAlignedDataflowContextResult(
        status=STATUS_BLOCKED,
        issues=tuple(sorted(set(issues))),
        context_pack=None,
        receipt=None,
    )


def _name(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        left = _name(node.value)
        return f"{left}.{node.attr}" if left else node.attr
    if isinstance(node, ast.Subscript):
        return _name(node.value)
    return None


def _names_in(node: ast.AST | None) -> set[str]:
    if node is None:
        return set()
    result: set[str] = set()
    for item in ast.walk(node):
        if isinstance(item, ast.Name):
            result.add(item.id)
        elif isinstance(item, ast.Attribute):
            named = _name(item)
            if named:
                result.add(named)
    return result


def _python_facts(content: str) -> SemanticFacts:
    tree = ast.parse(content)
    symbols: set[str] = set()
    imports: set[str] = set()
    calls: set[str] = set()
    type_refs: set[str] = set()
    edges: set[tuple[str, str]] = set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.add(node.name)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs):
                    type_refs.update(_names_in(arg.annotation))
                type_refs.update(_names_in(node.returns))
        elif isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.add(module)
            for alias in node.names:
                imports.add(f"{module}.{alias.name}" if module else alias.name)
        elif isinstance(node, ast.Call):
            named = _name(node.func)
            if named:
                calls.add(named)
        elif isinstance(node, ast.AnnAssign):
            type_refs.update(_names_in(node.annotation))

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            sources = _names_in(node.value)
            targets: set[str] = set()
            for target in node.targets:
                targets.update(_names_in(target))
            for source in sources:
                for target in targets:
                    if source != target:
                        edges.add((source, target))
        elif isinstance(node, ast.AnnAssign):
            sources = _names_in(node.value)
            targets = _names_in(node.target)
            for source in sources:
                for target in targets:
                    if source != target:
                        edges.add((source, target))
        elif isinstance(node, ast.Return):
            for source in _names_in(node.value):
                edges.add((source, "return"))

    return SemanticFacts(
        symbols=tuple(sorted(symbols)),
        imports=tuple(sorted(item for item in imports if item)),
        calls=tuple(sorted(calls)),
        type_refs=tuple(sorted(type_refs)),
        dataflow_edges=tuple(sorted(edges)),
    )


def _lean_facts(content: str) -> SemanticFacts:
    symbols: set[str] = set()
    imports: set[str] = set()
    calls: set[str] = set()
    type_refs: set[str] = set()
    edges: set[tuple[str, str]] = set()
    current_symbol: str | None = None

    for raw_line in content.splitlines():
        line = raw_line.split("--", 1)[0]
        import_match = _LEAN_IMPORT.match(line)
        if import_match:
            imports.add(import_match.group(1))
        decl_match = _LEAN_DECL.match(line)
        if decl_match:
            current_symbol = decl_match.group(1)
            symbols.add(current_symbol)
            tail = line[decl_match.end() :]
            before_rhs, separator, rhs = tail.partition(":=")
            type_refs.update(
                item for item in _IDENTIFIER.findall(before_rhs) if item != current_symbol
            )
            if separator:
                identifiers = _IDENTIFIER.findall(rhs)
                calls.update(identifiers)
                for source in identifiers:
                    if source != current_symbol:
                        edges.add((source, current_symbol))
            continue
        if current_symbol and line.strip() and not line.lstrip().startswith(("namespace ", "end ", "open ")):
            identifiers = _IDENTIFIER.findall(line)
            calls.update(identifiers)
            for source in identifiers:
                if source != current_symbol:
                    edges.add((source, current_symbol))

    return SemanticFacts(
        symbols=tuple(sorted(symbols)),
        imports=tuple(sorted(imports)),
        calls=tuple(sorted(calls)),
        type_refs=tuple(sorted(type_refs)),
        dataflow_edges=tuple(sorted(edges)),
    )


def _text_facts(content: str) -> SemanticFacts:
    words = tuple(sorted(set(_WORD.findall(content))))
    return SemanticFacts(symbols=(), imports=(), calls=(), type_refs=words[:64], dataflow_edges=())


def _facts(path: str, content: str, allow_text_fallback: bool) -> SemanticFacts:
    suffix = PurePosixPath(path).suffix.lower()
    if suffix == ".py":
        return _python_facts(content)
    if suffix == ".lean":
        return _lean_facts(content)
    if allow_text_fallback:
        return _text_facts(content)
    return SemanticFacts((), (), (), (), ())


def _normalize_terms(items: Iterable[str]) -> tuple[str, ...]:
    normalized = {item.strip().lower() for item in items if item.strip()}
    return tuple(sorted(normalized))


def _query_nodes(request: Mapping[str, Any], candidates: Sequence[Candidate]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []

    def add(stage: str, node_id: str, parent_ids: list[str], terms: Iterable[str], source_refs: Iterable[str]) -> None:
        body = {
            "node_id": node_id,
            "stage": stage,
            "parent_ids": sorted(parent_ids),
            "terms": list(_normalize_terms(terms)),
            "source_refs": sorted(set(source_refs)),
        }
        nodes.append(seal(body, QUERY_NODE_DIGEST_FIELD))

    add("intent", "q-intent", [], request["initial_query_terms"], ["request.intent_text"])
    hypothesis_ids: list[str] = []
    for hypothesis in request["candidate_hypotheses"]:
        node_id = "q-hypothesis-" + hypothesis["hypothesis_id"]
        hypothesis_ids.append(node_id)
        add(
            "hypothesis",
            node_id,
            ["q-intent"],
            hypothesis["query_terms"],
            ["hypothesis:" + hypothesis["hypothesis_id"]],
        )
    symbol_terms = list(request["target_symbols"])
    symbol_refs: list[str] = ["request.target_symbols"]
    for hypothesis in request["candidate_hypotheses"]:
        symbol_terms.extend(hypothesis["expected_symbols"])
        symbol_refs.append("hypothesis:" + hypothesis["hypothesis_id"])
    add("symbol", "q-symbol", hypothesis_ids or ["q-intent"], symbol_terms, symbol_refs)
    dependency_terms: list[str] = []
    dataflow_terms: list[str] = []
    dependency_refs: list[str] = []
    dataflow_refs: list[str] = []
    for candidate in candidates:
        dependency_terms.extend(candidate.facts.imports)
        dependency_terms.extend(candidate.facts.calls)
        dependency_terms.extend(candidate.facts.type_refs)
        if candidate.facts.imports or candidate.facts.calls or candidate.facts.type_refs:
            dependency_refs.append(candidate.path)
        for source, target in candidate.facts.dataflow_edges:
            dataflow_terms.extend((source, target))
            dataflow_refs.append(candidate.path)
    add("dependency", "q-dependency", ["q-symbol"], dependency_terms, dependency_refs)
    add("dataflow", "q-dataflow", ["q-dependency"], dataflow_terms, dataflow_refs)
    return nodes


def _symbol_index(candidates: Sequence[Candidate]) -> dict[str, tuple[str, ...]]:
    index: dict[str, set[str]] = {}
    for candidate in candidates:
        for symbol in candidate.facts.symbols:
            index.setdefault(symbol, set()).add(candidate.path)
            index.setdefault(symbol.split(".")[-1], set()).add(candidate.path)
    return {key: tuple(sorted(value)) for key, value in index.items()}


def _module_index(candidates: Sequence[Candidate]) -> dict[str, str]:
    index: dict[str, str] = {}
    for candidate in candidates:
        path = PurePosixPath(candidate.path)
        if path.suffix == ".py":
            module = ".".join(path.with_suffix("").parts)
            index[module] = candidate.path
            index[path.stem] = candidate.path
        elif path.suffix == ".lean":
            module = ".".join(path.with_suffix("").parts)
            if module.startswith("formal."):
                module = module[len("formal.") :]
            index[module] = candidate.path
            index[path.stem] = candidate.path
    return index


def _neighbors(candidate: Candidate, symbols: Mapping[str, tuple[str, ...]], modules: Mapping[str, str]) -> tuple[str, ...]:
    result: set[str] = set()
    for imported in candidate.facts.imports:
        if imported in modules:
            result.add(modules[imported])
        leaf = imported.split(".")[-1]
        if leaf in modules:
            result.add(modules[leaf])
    for reference in (*candidate.facts.calls, *candidate.facts.type_refs):
        leaf = reference.split(".")[-1]
        result.update(symbols.get(reference, ()))
        result.update(symbols.get(leaf, ()))
    result.discard(candidate.path)
    return tuple(sorted(result))


def _shortest_paths(
    candidates: Sequence[Candidate],
    seed_paths: set[str],
    maximum_depth: int,
) -> dict[str, list[str]]:
    by_path = {candidate.path: candidate for candidate in candidates}
    symbols = _symbol_index(candidates)
    modules = _module_index(candidates)
    paths: dict[str, list[str]] = {seed: [seed] for seed in seed_paths if seed in by_path}
    queue: deque[tuple[str, int]] = deque((seed, 0) for seed in sorted(paths))
    while queue:
        current, depth = queue.popleft()
        if depth >= maximum_depth:
            continue
        for neighbor in _neighbors(by_path[current], symbols, modules):
            proposed = paths[current] + [neighbor]
            if neighbor not in paths or len(proposed) < len(paths[neighbor]):
                paths[neighbor] = proposed
                queue.append((neighbor, depth + 1))
    return paths


def _resolved_dependency_paths(
    candidate: Candidate,
    candidates: Sequence[Candidate],
    maximum_depth: int,
) -> list[list[str]]:
    all_paths = _shortest_paths(candidates, {candidate.path}, maximum_depth)
    return [
        path
        for target, path in sorted(all_paths.items())
        if target != candidate.path and len(path) > 1
    ]


def _excerpt(content: str, maximum_bytes: int) -> str:
    encoded = content.encode("utf-8")
    if len(encoded) <= maximum_bytes:
        return content
    clipped = encoded[:maximum_bytes]
    while True:
        try:
            text = clipped.decode("utf-8")
            break
        except UnicodeDecodeError:
            clipped = clipped[:-1]
    return text.rstrip("\n") + "\n"


def _candidate(
    path: str,
    content: str,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> Candidate:
    role = role_for_path(path)
    language = language_for_path(path)
    facts = _facts(path, content, policy["allow_text_fallback"])
    searchable = "\n".join(
        [
            path,
            content,
            *facts.symbols,
            *facts.imports,
            *facts.calls,
            *facts.type_refs,
            *(f"{source} {target}" for source, target in facts.dataflow_edges),
        ]
    ).lower()
    all_terms = _normalize_terms(request["initial_query_terms"])
    matched_terms = tuple(term for term in all_terms if term in searchable)
    matched_hypotheses: list[str] = []
    for hypothesis in request["candidate_hypotheses"]:
        hypothesis_terms = _normalize_terms(hypothesis["query_terms"])
        expected = tuple(symbol.lower() for symbol in hypothesis["expected_symbols"])
        if any(term in searchable for term in hypothesis_terms) or any(symbol in searchable for symbol in expected):
            matched_hypotheses.append(hypothesis["hypothesis_id"])
    target_symbols = tuple(symbol for symbol in request["target_symbols"] if symbol.lower() in searchable)
    prefix_match = any(path_has_prefix(path, prefix) for prefix in request["target_path_prefixes"])
    role_match = role in request["required_roles"]
    score = (
        3 * len(matched_terms)
        + 4 * len(matched_hypotheses)
        + 5 * len(target_symbols)
        + (2 if prefix_match else 0)
        + (1 if role_match else 0)
        + min(3, len(facts.dataflow_edges))
    )
    return Candidate(
        path=path,
        content=content,
        role=role,
        language=language,
        facts=facts,
        matched_terms=matched_terms,
        matched_hypotheses=tuple(sorted(matched_hypotheses)),
        matched_target_symbols=tuple(sorted(target_symbols)),
        score=score,
    )


def build_intent_aligned_dataflow_context_pack(
    *,
    request: Mapping[str, Any],
    policy: Mapping[str, Any],
    repository_snapshot: Mapping[str, str],
    source_observation_receipt: Mapping[str, Any],
) -> CodeAIIntentAlignedDataflowContextResult:
    issues: list[str] = []
    issues.extend(validate_request(request))
    issues.extend(validate_policy(policy))
    issues.extend(validate_repository(repository_snapshot))
    issues.extend(validate_source_receipt(source_observation_receipt))
    if issues:
        return _blocked(*issues)

    if policy["allow_repository_mutation"]:
        issues.append("context_policy_repository_mutation_forbidden")
    if policy["allow_network_access"]:
        issues.append("context_policy_network_access_forbidden")
    if policy["allow_secret_access"]:
        issues.append("context_policy_secret_access_forbidden")
    if policy["allow_candidate_selection_authority"]:
        issues.append("context_policy_candidate_selection_authority_forbidden")
    if policy["allow_execution_authority"]:
        issues.append("context_policy_execution_authority_forbidden")
    if source_observation_receipt["repository_full_name"] != policy["expected_repository_full_name"]:
        issues.append("source_observation_receipt_repository_mismatch")
    if source_observation_receipt["source_commit_sha"] != policy["expected_source_commit_sha"]:
        issues.append("source_observation_receipt_commit_mismatch")
    if request["expected_source_observation_receipt_digest"] != source_observation_receipt[SOURCE_RECEIPT_DIGEST_FIELD]:
        issues.append("context_request_source_receipt_digest_mismatch")
    snapshot_digest = canonical_digest(repository_snapshot)
    if request["repository_snapshot_digest"] != snapshot_digest:
        issues.append("context_request_repository_snapshot_digest_mismatch")
    if source_observation_receipt["tree_digest"] != snapshot_digest:
        issues.append("source_observation_receipt_tree_digest_mismatch")
    if policy["evaluation_epoch"] < request["request_created_epoch"]:
        issues.append("context_request_from_future")
    elif policy["evaluation_epoch"] - request["request_created_epoch"] > policy["maximum_request_age"]:
        issues.append("context_request_stale")
    if len(request["candidate_hypotheses"]) > policy["maximum_hypotheses"]:
        issues.append("context_request_hypothesis_budget_exceeded")
    all_query_terms = set(_normalize_terms(request["initial_query_terms"]))
    for hypothesis in request["candidate_hypotheses"]:
        all_query_terms.update(_normalize_terms(hypothesis["query_terms"]))
    if len(all_query_terms) > policy["maximum_query_terms"]:
        issues.append("context_request_query_term_budget_exceeded")

    snapshot_bytes = sum(len(content.encode("utf-8")) for content in repository_snapshot.values())
    if snapshot_bytes > policy["maximum_repository_snapshot_bytes"]:
        issues.append("repository_snapshot_byte_budget_exceeded")
    if len(repository_snapshot) > policy["maximum_candidate_files"]:
        issues.append("repository_snapshot_candidate_file_budget_exceeded")

    filtered: list[tuple[str, str]] = []
    for path, content in sorted(repository_snapshot.items()):
        if any(path_has_prefix(path, prefix) for prefix in policy["forbidden_repository_path_prefixes"]):
            issues.append("repository_file_forbidden_prefix:" + path)
            continue
        if not any(path_has_prefix(path, prefix) for prefix in policy["allowed_repository_path_prefixes"]):
            issues.append("repository_file_outside_allowed_prefix:" + path)
            continue
        if PurePosixPath(path).suffix.lower() not in policy["supported_file_suffixes"]:
            issues.append("repository_file_unsupported_suffix:" + path)
            continue
        if len(content.encode("utf-8")) > policy["maximum_file_bytes"]:
            issues.append("repository_file_byte_budget_exceeded:" + path)
            continue
        filtered.append((path, content))
    if issues:
        return _blocked(*issues)

    candidates: list[Candidate] = []
    for path, content in filtered:
        try:
            candidates.append(_candidate(path, content, request, policy))
        except (SyntaxError, ValueError) as exc:
            return _blocked("repository_semantic_parse_failed:" + path + ":" + exc.__class__.__name__)

    minimum_score = policy["minimum_intent_evidence_score"]
    seed_paths = {
        candidate.path
        for candidate in candidates
        if candidate.score >= minimum_score
        and (candidate.matched_terms or candidate.matched_hypotheses or candidate.matched_target_symbols)
    }
    if not seed_paths:
        return _blocked("no_intent_aligned_context_seed")
    dependency_paths = _shortest_paths(candidates, seed_paths, policy["maximum_dependency_depth"])
    eligible = [candidate for candidate in candidates if candidate.path in dependency_paths]
    eligible.sort(key=lambda item: (-item.score, len(dependency_paths[item.path]), item.path))
    selected = eligible[: policy["maximum_selected_files"]]

    selected_files: list[dict[str, Any]] = []
    total_context_bytes = 0
    for candidate in selected:
        excerpt = _excerpt(candidate.content, policy["maximum_excerpt_bytes"])
        excerpt_bytes = len(excerpt.encode("utf-8"))
        if total_context_bytes + excerpt_bytes > policy["maximum_total_context_bytes"]:
            continue
        path_evidence = dependency_paths.get(candidate.path, [])
        symbol_digest = canonical_digest(list(candidate.facts.symbols))
        if policy["require_dependency_path"] and not path_evidence:
            continue
        if policy["require_symbol_digest"] and not symbol_digest:
            continue
        resolved_dependency_paths = _resolved_dependency_paths(
            candidate, candidates, policy["maximum_dependency_depth"]
        )
        body = {
            "path": candidate.path,
            "role": candidate.role,
            "language": candidate.language,
            "content_digest": canonical_digest(candidate.content),
            "symbol_digest": symbol_digest,
            "symbols": list(candidate.facts.symbols),
            "imports": list(candidate.facts.imports),
            "calls": list(candidate.facts.calls),
            "type_refs": list(candidate.facts.type_refs),
            "dataflow_edges": [list(edge) for edge in candidate.facts.dataflow_edges],
            "matched_terms": list(candidate.matched_terms),
            "matched_hypotheses": list(candidate.matched_hypotheses),
            "matched_target_symbols": list(candidate.matched_target_symbols),
            "dependency_path": path_evidence,
            "resolved_dependency_paths": resolved_dependency_paths,
            "intent_evidence_score": candidate.score,
            "excerpt": excerpt,
            "excerpt_digest": canonical_digest(excerpt),
            "excerpt_bytes": excerpt_bytes,
        }
        selected_files.append(seal(body, SELECTED_FILE_DIGEST_FIELD))
        total_context_bytes += excerpt_bytes

    if not selected_files:
        return _blocked("no_context_within_output_budget")
    selected_roles = {item["role"] for item in selected_files}
    missing_roles = set(request["required_roles"]).difference(selected_roles)
    if missing_roles:
        return _blocked("required_context_roles_missing:" + ",".join(sorted(missing_roles)))

    query_lineage = _query_nodes(request, candidates)
    context_pack_body = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "operating_mode": MODE_CONTEXT_ONLY,
        "codeai_disposition": DISPOSITION_BUILT,
        "repository_full_name": policy["expected_repository_full_name"],
        "source_commit_sha": policy["expected_source_commit_sha"],
        "source_observation_receipt_digest": source_observation_receipt[SOURCE_RECEIPT_DIGEST_FIELD],
        "request_digest": request[REQUEST_DIGEST_FIELD],
        "policy_digest": policy[POLICY_DIGEST_FIELD],
        "query_lineage": query_lineage,
        "selected_files": selected_files,
        "budget_evidence": {
            "repository_snapshot_bytes": snapshot_bytes,
            "repository_candidate_file_count": len(repository_snapshot),
            "selected_file_count": len(selected_files),
            "total_context_bytes": total_context_bytes,
            "maximum_selected_files": policy["maximum_selected_files"],
            "maximum_total_context_bytes": policy["maximum_total_context_bytes"],
            "maximum_dependency_depth": policy["maximum_dependency_depth"],
        },
        "repository_observation_read_only": True,
        "repository_mutation_performed": False,
        "network_access_performed": False,
        "secret_material_read": False,
        "candidate_selection_authority_granted": False,
        "execution_authority_granted": False,
        "correctness_claimed": False,
        "completeness_claimed": False,
        "representativeness_claimed": False,
    }
    context_pack = seal(context_pack_body, PACK_DIGEST_FIELD)
    receipt = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "codeai_disposition": DISPOSITION_BUILT,
            "operating_mode": MODE_CONTEXT_ONLY,
            "repository_full_name": policy["expected_repository_full_name"],
            "source_commit_sha": policy["expected_source_commit_sha"],
            "context_pack_digest": context_pack[PACK_DIGEST_FIELD],
            "request_digest": request[REQUEST_DIGEST_FIELD],
            "policy_digest": policy[POLICY_DIGEST_FIELD],
            "selected_file_count": len(selected_files),
            "query_lineage_node_count": len(query_lineage),
            "repository_observation_read_only": True,
            "repository_mutation_performed": False,
            "network_access_performed": False,
            "secret_material_read": False,
            "candidate_selection_authority_granted": False,
            "execution_authority_granted": False,
        },
        RECEIPT_DIGEST_FIELD,
    )
    return CodeAIIntentAlignedDataflowContextResult(
        status=STATUS_READY,
        issues=(),
        context_pack=context_pack,
        receipt=receipt,
    )


__all__ = [
    "build_intent_aligned_dataflow_context_pack",
    "canonical_digest",
    "canonical_json",
]
