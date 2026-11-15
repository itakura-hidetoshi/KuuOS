"""MemoryOS × CodeAI: evidence-bound Lean repair failure/success learning.

GitHub pointers are evidence locations, never proof or action authority.
This module cannot run Lean, promote a branch, or mark CI complete.
Fail closed on conflicting/corrupt records, version drift, and unknown outcomes.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Mapping

VERSION = "kuuos_codeai_lean_failure_memoryos_v0_1"
REPOSITORY = "itakura-hidetoshi/KuuOS"
LEAN_VERSION = "leanprover/lean4:v4.30.0-rc2"
MATHLIB_REV = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
ENTRY_VERSION = "memoryos_codeai_lean_case_v0_1"
ZERO = "0" * 64
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
OUTCOMES = frozenset({
    "DIRECT_LEAN_FAILURE", "DIRECT_LEAN_SUCCESS",
    "LOCAL_MCP_SUCCESS", "INDEPENDENT_CI_SUCCESS",
    "NO_DATA",
})
TAXONOMY = (
    ("lean.invalidField", "API_FIELD_RESOLUTION", "Check owner namespace and pinned mathlib definition"),
    ("unknown identifier", "UNKNOWN_IDENTIFIER", "Read imports and exact imported declaration signature"),
    ("expected type must not contain free variables", "DEPENDENT_PROOF_ELABORATION",
     "Use a closed, explicitly typed proof term or reduce the index before tactic elaboration"),
    ("application type mismatch", "APPLICATION_TYPE_MISMATCH",
     "Compare source and target universes and dependent binder types"),
    ("type mismatch", "TYPE_MISMATCH", "Inspect complete signature, coercions and universe"),
    ("omega could not prove", "TACTIC_NONLINEAR_OR_UNAVAILABLE_HYPOTHESIS",
     "Expose relevant inequalities; do not assume arithmetic tactic proves geometric equality"),
    ("rfl failed", "DEFINITIONAL_EQUALITY_FAILURE", "Check definitional reduction versus propositional equality"),
    ("simp argument is unused", "UNUSED_SIMP_ARGUMENT", "Remove irrelevant simp lemma, check actual rewrite target"),
    ("simp_all made no progress", "TACTIC_NO_PROGRESS", "Prune impossible goals before simp; inspect residual goal"),
    ("tactic does nothing", "TACTIC_NO_PROGRESS", "Do not append tactics after all goals are closed"),
    ("no goals to be solved", "CLOSED_GOAL_TACTIC", "Remove redundant trailing tactics"),
    ("unsolved goals", "UNRESOLVED_GOAL", "Inspect Lean goal state, do not insert sorry or weaken theorem"),
    ("timeout at", "HEARTBEAT_TIMEOUT", "Decompose proof, avoid combinatorial simp explosion"),
    ("maximum number of heartbeats", "HEARTBEAT_TIMEOUT", "Decompose finite cases instead of only raising budgets"),
    ("universe", "UNIVERSE_OR_LEVEL", "Compare SSet.{0} and actual fixed type universes"),
    ("invalid field", "API_FIELD_RESOLUTION", "Check actual owner namespace"),
)
LOCATION = re.compile(r"^(?:.*[/\\])?[^/:\\]+\.lean:\d+:\d+:\s*(?:error(?:\([^)]*\))?:\s*)?", re.I)
REDACTION = re.compile(r"(gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]{16,})")

def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")).hexdigest()

def git_blob(content: str) -> str:
    raw = content.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def classify_error(line: str) -> dict[str, str]:
    if not isinstance(line, str):
        raise ValueError("Lean diagnostic is not text")
    redacted = REDACTION.sub("[REDACTED]", line.strip())
    text = LOCATION.sub("", redacted).strip()
    low = text.lower()
    family, suggestion = "UNCLASSIFIED", "NO_DATA; inspect complete Lean diagnostics"
    for phrase, key, remedy in TAXONOMY:
        if phrase in low:
            family, suggestion = key, remedy
            break
    # Location and environment-specific details never determine a reusable family.
    head = text.splitlines()[0][:240] if text else "NO_DATA"
    return {
        "family": family, "message": head,
        "signature": digest({"family": family, "head": head.lower()})[:24],
        "suggestion": suggestion,
        "causal_status": "UNVERIFIED_HYPOTHESIS",
    }

def validate_case(case: Mapping[str, Any]) -> None:
    required = {
        "schema", "id", "repository", "source_head", "source_tree",
        "imported_blob", "candidate_blob", "variant", "producer_run",
        "lean_version", "mathlib_rev", "outcome", "diagnostics",
        "mcp_receipt", "independent_run", "evidence_url", "causal_status",
    }
    if not isinstance(case, Mapping) or not required.issubset(case):
        raise ValueError("MemoryOS incomplete case; NO_DATA not promotable")
    if case["schema"] != ENTRY_VERSION or case["repository"] != REPOSITORY:
        raise ValueError("MemoryOS case schema/repository mismatch")
    for field in ("source_head", "source_tree", "imported_blob", "candidate_blob"):
        if not isinstance(case[field], str) or not SHA40.fullmatch(case[field]):
            raise ValueError("MemoryOS invalid Git SHA: " + field)
    if case["lean_version"] != LEAN_VERSION or case["mathlib_rev"] != MATHLIB_REV:
        raise ValueError("MemoryOS unpinned environment")
    if case["outcome"] not in OUTCOMES:
        raise ValueError("MemoryOS unknown outcome")
    if not isinstance(case["id"], str) or not case["id"] or not isinstance(case["variant"], str):
        raise ValueError("MemoryOS invalid id/variant")
    if case["id"] != "case:" + digest({k: v for k, v in case.items() if k != "id"})[:32]:
        raise ValueError("MemoryOS case content-address identity mismatch")
    if not isinstance(case["producer_run"], int) or case["producer_run"] <= 0:
        raise ValueError("MemoryOS missing producer run")
    if not isinstance(case["diagnostics"], list) or len(case["diagnostics"]) > 32:
        raise ValueError("MemoryOS diagnostic bounds invalid")
    for diag in case["diagnostics"]:
        if not isinstance(diag, Mapping) or diag.get("family") not in {x[1] for x in TAXONOMY} | {"UNCLASSIFIED"}:
            raise ValueError("MemoryOS diagnostic invalid")
        if not isinstance(diag.get("signature"), str) or len(diag["signature"]) != 24:
            raise ValueError("MemoryOS unsealed diagnostic")
    if case["causal_status"] not in {"UNVERIFIED_HYPOTHESIS", "OBSERVATIONAL_COMPARISON", "NO_DATA"}:
        raise ValueError("MemoryOS causal proof cannot be asserted by history")
    if not isinstance(case["mcp_receipt"], (dict, type(None))) or not isinstance(case["independent_run"], (int, type(None))):
        raise ValueError("MemoryOS proof receipt shape invalid")
    if case["outcome"] == "INDEPENDENT_CI_SUCCESS" and case["independent_run"] is None:
        raise ValueError("MemoryOS CI success without independent run")
    if case["outcome"] == "LOCAL_MCP_SUCCESS" and (
        not isinstance(case["mcp_receipt"], dict)
        or case["mcp_receipt"].get("verified_mcp_zero_errors") is not True
        or case["mcp_receipt"].get("second_direct_lean") is not True
    ):
        raise ValueError("MemoryOS local MCP success without exact direct/MCP receipt")
    if case["outcome"] != "INDEPENDENT_CI_SUCCESS" and case["independent_run"] is not None:
        raise ValueError("MemoryOS CI claim appears at wrong stage")
    if not isinstance(case["evidence_url"], str) or not case["evidence_url"].startswith(
        f"https://github.com/{REPOSITORY}/actions/runs/{case['producer_run']}"
    ):
        raise ValueError("MemoryOS GitHub evidence pointer mismatch")
    # A memory case can reference a successful CI but does not certify it.

def make_case(
    *, source_head: str, source_tree: str, imported_blob: str,
    variant: str, candidate_blob: str, producer_run: int,
    outcome: str, errors: list[str], mcp_receipt: dict | None = None,
    independent_run: int | None = None,
) -> dict[str, Any]:
    ds = [classify_error(s) for s in errors[:32]]
    item = {
        "schema": ENTRY_VERSION,
        "repository": REPOSITORY, "source_head": source_head,
        "source_tree": source_tree, "imported_blob": imported_blob,
        "candidate_blob": candidate_blob, "variant": variant,
        "producer_run": producer_run, "lean_version": LEAN_VERSION,
        "mathlib_rev": MATHLIB_REV, "outcome": outcome,
        "diagnostics": ds, "mcp_receipt": mcp_receipt,
        "independent_run": independent_run, "causal_status": "UNVERIFIED_HYPOTHESIS",
        "evidence_url": f"https://github.com/{REPOSITORY}/actions/runs/{producer_run}",
    }
    item["id"] = "case:" + digest(item)[:32]
    validate_case(item)
    return item

def cases_from_portfolio(portfolio: Mapping[str, Any], mcp: Mapping[str, Any],
                         producer_run: int) -> list[dict[str, Any]]:
    if not isinstance(portfolio, Mapping) or not isinstance(mcp, Mapping):
        raise ValueError("MemoryOS missing portfolio/MCP evidence")
    head = portfolio.get("source_head")
    tree = portfolio.get("source_tree")
    prior = portfolio.get("imported_v1103_blob")
    if not all(isinstance(x, str) and SHA40.fullmatch(x) for x in (head, tree, prior)):
        raise ValueError("MemoryOS producer source identity incomplete")
    if portfolio.get("source_restored") is not True or portfolio.get("git_write_performed") is not False:
        raise ValueError("MemoryOS producer wrote/mutated source")
    if portfolio.get("independent_ci_certified") is not False:
        raise ValueError("MemoryOS producer pretends to certify stage 4")
    rows = portfolio.get("candidates")
    if not isinstance(rows, list) or portfolio.get("candidate_count") != len(rows):
        raise ValueError("MemoryOS invalid candidate portfolio")
    if mcp.get("source_head") != head or mcp.get("candidate_count") != len(rows):
        raise ValueError("MemoryOS mismatched MCP lineage")
    result: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("MemoryOS malformed candidate")
        passed = (row.get("status") == "SUCCESS" and row.get("exit_code") == 0
                  and row.get("olean_exists") is True and row.get("error_count") == 0)
        if row.get("status") == "SUCCESS" and not passed:
            raise ValueError("MemoryOS false direct Lean success")
        if not isinstance(row.get("errors"), list) or not isinstance(row.get("error_count"), int):
            raise ValueError("MemoryOS missing errors")
        if passed and row["errors"]:
            raise ValueError("MemoryOS success has errors")
        if not passed and row["status"] in {"FAILURE", "TIMEOUT"} and row["error_count"] < 1:
            # Keep explicit NO_DATA; do not invent a diagnostic from a timeout.
            if row["status"] != "TIMEOUT":
                raise ValueError("MemoryOS failed but no diagnostic count")
        outcome = "DIRECT_LEAN_SUCCESS" if passed else (
            "DIRECT_LEAN_FAILURE" if row.get("status") in {"FAILURE", "TIMEOUT"} else "NO_DATA"
        )
        mcp_evidence = None
        if mcp.get("selected") == row.get("variant"):
            if not passed:
                raise ValueError("MemoryOS MCP selected failed direct Lean")
            if mcp.get("mcp_success") is True and mcp.get("mcp_errors") == 0 and mcp.get("second_direct_success") is True and mcp.get("selected_blob") == row.get("candidate_blob"):
                outcome = "LOCAL_MCP_SUCCESS"
                mcp_evidence = {"verified_mcp_zero_errors": True, "second_direct_lean": True}
        result.append(make_case(source_head=head, source_tree=tree,
            imported_blob=prior, variant=row["variant"], candidate_blob=row["candidate_blob"],
            producer_run=producer_run, outcome=outcome, errors=row["errors"],
            mcp_receipt=mcp_evidence))
    if not any(c["outcome"] in {"LOCAL_MCP_SUCCESS", "DIRECT_LEAN_SUCCESS"} for c in result):
        if mcp.get("mcp_success") is True or mcp.get("direct_lean_green"):
            raise ValueError("MemoryOS MCP invented a success")
    return result

def seal_event(case: Mapping[str, Any], previous_digest: str) -> dict[str, Any]:
    validate_case(case)
    if not SHA256.fullmatch(previous_digest):
        raise ValueError("MemoryOS bad previous chain digest")
    event = {"memory_kind": "repair_lineage_memory", "authority": "external_pointer_only",
             "previous_digest": previous_digest, "case": dict(case)}
    event["digest"] = digest(event)
    return event

def read_journal(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    previous, events, ids = ZERO, [], set()
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            raise ValueError("MemoryOS blank journal line")
        obj = json.loads(line)
        if not isinstance(obj, dict) or not isinstance(obj.get("case"), dict):
            raise ValueError("MemoryOS journal malformed")
        expected = obj.get("digest")
        if expected != digest({k: v for k, v in obj.items() if k != "digest"}):
            raise ValueError("MemoryOS journal tampering detected")
        if obj.get("previous_digest") != previous or obj.get("authority") != "external_pointer_only":
            raise ValueError("MemoryOS journal chain/authority mismatch")
        validate_case(obj["case"])
        if obj["case"]["id"] in ids:
            raise ValueError("MemoryOS duplicate immutable ID")
        ids.add(obj["case"]["id"])
        previous = expected
        events.append(obj)
    return events

def append_cases(path: str | Path, cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Append-only to an explicit artifact path; never writes Git or main."""
    p = Path(path)
    events = read_journal(p)
    ids = {e["case"]["id"] for e in events}
    previous = events[-1]["digest"] if events else ZERO
    new_lines = []
    for case in cases:
        validate_case(case)
        if case["id"] in ids:
            continue  # Idempotent exact replay; no overwrite or duplicate.
        evt = seal_event(case, previous)
        new_lines.append(json.dumps(evt, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        ids.add(case["id"])
        previous = evt["digest"]
    p.parent.mkdir(parents=True, exist_ok=True)
    if new_lines:
        with p.open("a", encoding="utf-8") as f:
            for line in new_lines:
                f.write(line)
    return {"appended": len(new_lines), "total": len(events) + len(new_lines),
            "last_digest": previous, "truth_authority": False,
            "proof_authority": False, "git_write": False}

def query_cases(
    cases: list[dict[str, Any]], *, source_head: str, imported_blob: str,
    source_tree: str | None = None, candidate_blob: str | None = None,
    lean_version: str = LEAN_VERSION, mathlib_rev: str = MATHLIB_REV,
) -> dict[str, Any]:
    exact, analogies, excluded = [], [], []
    for c in cases:
        validate_case(c)
        if c["repository"] != REPOSITORY or c["lean_version"] != lean_version or c["mathlib_rev"] != mathlib_rev:
            excluded.append(c["id"])
        elif (source_tree is not None and c["source_tree"] == source_tree
              and c["source_head"] == source_head and c["imported_blob"] == imported_blob):
            exact.append(c)
        else:
            analogies.append(c)
    blocked = [c["candidate_blob"] for c in exact
               if c["outcome"] == "DIRECT_LEAN_FAILURE"
               and (candidate_blob is None or c["candidate_blob"] == candidate_blob)]
    return {
        "status": "MEMORY_HINT_ONLY", "exact_cases": exact,
        "analogies": analogies, "excluded": excluded,
        "avoid_exact_candidate_blobs": sorted(set(blocked)),
        "history_is_proof": False, "memory_grants_execution": False,
        "preference_implies_descent": False,
    }

def route_candidates(
    candidates: Mapping[str, str], cases: list[dict[str, Any]],
    *, source_head: str, source_tree: str, imported_blob: str,
) -> tuple[dict[str, str], dict[str, Any]]:
    """Only identical source-bound previously FAILED blobs are quarantined.
    Cross-commit resemblance is a visible hint, not a rejection decision.
    """
    result, withheld = {}, []
    for variant, content in candidates.items():
        blob = git_blob(content)
        lookup = query_cases(cases, source_head=source_head, source_tree=source_tree,
                             imported_blob=imported_blob, candidate_blob=blob)
        if blob in lookup["avoid_exact_candidate_blobs"]:
            withheld.append({"variant": variant, "blob": blob, "reason": "EXACT_REPLAY_OF_DIRECT_LEAN_FAILURE"})
        else:
            result[variant] = content
    hints = sorted({
        d["family"] + ": " + d["suggestion"] for c in cases
        if c["outcome"] == "DIRECT_LEAN_FAILURE"
        for d in c["diagnostics"]
    })
    report = {"source_head": source_head, "retained": list(result),
              "quarantined": withheld, "analogical_hints": hints,
              "hint_status": "UNVERIFIED_CROSS_CONTEXT",
              "selects_proof": False, "independent_ci_certified": False}
    if not result:
        raise ValueError("MemoryOS exhausted: identical failed candidates cannot be silently replayed")
    return result, report

def read_seed(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("profile") != ENTRY_VERSION or not isinstance(data.get("cases"), list):
        raise ValueError("MemoryOS seed invalid")
    result = []
    seen = set()
    for c in data["cases"]:
        validate_case(c)
        if c["id"] in seen:
            raise ValueError("MemoryOS seed duplicated case")
        seen.add(c["id"]); result.append(c)
    return result
