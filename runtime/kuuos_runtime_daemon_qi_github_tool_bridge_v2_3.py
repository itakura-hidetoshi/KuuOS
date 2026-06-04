#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import base64
import hashlib
import json
import os
import pathlib
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class QiGitHubToolBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    plan_path: str
    receipt_path: str
    audit_path: str
    mode: str
    repository_full_name: str
    applied_count: int
    skipped_count: int
    blocked_count: int
    records: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _actions(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = plan.get("actions", [])
    return [dict(item) for item in raw if isinstance(item, Mapping)] if isinstance(raw, list) else []


def _headers(token: str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "kuuos-qi-github-tool-bridge-v2-3",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _request(method: str, url: str, token: str, payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(dict(payload), ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_headers(token), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"github_http_{exc.code}:{body[:240]}") from exc


def _repo_api(repository: str, suffix: str) -> str:
    return f"https://api.github.com/repos/{repository}{suffix}"


def _ensure_allowed(plan: Mapping[str, Any], action: Mapping[str, Any], blockers: list[str]) -> None:
    allowed_repo = str(plan.get("repository_full_name", ""))
    action_repo = str(action.get("repository_full_name", allowed_repo))
    if not allowed_repo:
        blockers.append("repository_missing")
    if action_repo != allowed_repo:
        blockers.append("action_repository_mismatch")
    allowed_base = str(plan.get("allowed_base_branch", plan.get("base_branch", "main")))
    base = str(action.get("base_branch", plan.get("base_branch", allowed_base)))
    if base != allowed_base:
        blockers.append("base_branch_not_allowed")


def _mock_call(action: Mapping[str, Any]) -> dict[str, Any]:
    kind = str(action.get("kind", ""))
    digest = _sha(action)
    if kind == "create_branch":
        return {"branch": action.get("branch"), "sha": action.get("sha"), "mock": True, "digest": digest}
    if kind in {"create_file", "update_file", "file_patch"}:
        return {"path": action.get("path"), "commit_sha": digest[:40], "mock": True}
    if kind == "create_pr":
        return {"number": int(action.get("mock_pr_number", 1)), "head_sha": action.get("head_sha", digest[:40]), "mock": True}
    if kind == "merge_pr":
        return {"merged": True, "sha": action.get("expected_head_sha", digest[:40]), "mock": True}
    return {"mock": True, "unknown": kind, "digest": digest}


def _real_call(repository: str, action: Mapping[str, Any], token: str) -> dict[str, Any]:
    kind = str(action.get("kind", ""))
    if kind == "create_branch":
        branch = str(action.get("branch", ""))
        sha = str(action.get("sha", ""))
        if not branch or not sha:
            raise RuntimeError("create_branch_requires_branch_and_sha")
        return _request("POST", _repo_api(repository, "/git/refs"), token, {"ref": f"refs/heads/{branch}", "sha": sha})
    if kind in {"create_file", "update_file", "file_patch"}:
        path = str(action.get("path", ""))
        branch = str(action.get("branch", ""))
        content = str(action.get("content", ""))
        message = str(action.get("message", f"Qi GitHub tool bridge {kind}"))
        if not path or not branch:
            raise RuntimeError("file_action_requires_path_and_branch")
        payload: dict[str, Any] = {"message": message, "content": base64.b64encode(content.encode("utf-8")).decode("ascii"), "branch": branch}
        if action.get("sha"):
            payload["sha"] = str(action.get("sha"))
        return _request("PUT", _repo_api(repository, f"/contents/{path}"), token, payload)
    if kind == "create_pr":
        head = str(action.get("head", action.get("branch", "")))
        base = str(action.get("base", action.get("base_branch", "main")))
        title = str(action.get("title", "Qi GitHub tool bridge PR"))
        body = str(action.get("body", ""))
        if not head or not base:
            raise RuntimeError("create_pr_requires_head_and_base")
        return _request("POST", _repo_api(repository, "/pulls"), token, {"title": title, "head": head, "base": base, "body": body, "draft": bool(action.get("draft", False))})
    if kind == "merge_pr":
        pr_number = int(action.get("pr_number", 0) or 0)
        expected_head_sha = str(action.get("expected_head_sha", ""))
        merge_method = str(action.get("merge_method", "merge"))
        if pr_number <= 0 or not expected_head_sha:
            raise RuntimeError("merge_requires_pr_number_and_expected_head_sha")
        return _request("PUT", _repo_api(repository, f"/pulls/{pr_number}/merge"), token, {"merge_method": merge_method, "sha": expected_head_sha})
    raise RuntimeError(f"unknown_action_{kind}")


def build_qi_github_tool_bridge(*, runtime_context: Mapping[str, Any], bridge_license_packet: Mapping[str, Any], transport: Callable[[str, Mapping[str, Any], str], dict[str, Any]] | None = None) -> QiGitHubToolBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(bridge_license_packet)
    blockers: list[str] = []
    warnings: list[str] = []
    records: list[dict[str, Any]] = []
    root = _root(ctx.get("runtime_root"), blockers)
    plan_path = root / "github_tool_bridge_plan.json"
    receipt_path = root / "github_tool_bridge_receipt.json"
    audit_path = root / "github_tool_bridge_audit.jsonl"
    if ctx.get("qi_github_tool_bridge_enabled") is not True:
        blockers.append("qi_github_tool_bridge_enabled_not_true")
    if ctx.get("apply_github_tool_bridge") is not True:
        blockers.append("apply_github_tool_bridge_not_true")
    if lic.get("license_status") != "QI_GITHUB_TOOL_BRIDGE_LICENSE_READY":
        blockers.append("github_tool_bridge_license_not_ready")
    for name in ["plan_read_allowed", "external_action_allowed", "receipt_write_allowed", "audit_append_allowed"]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))
    plan = _read_json(plan_path)
    repository = str(plan.get("repository_full_name", ""))
    mode = str(plan.get("mode", ctx.get("mode", "mock")))
    execute = ctx.get("execute_external_actions") is True and plan.get("execute_external_actions") is True
    if mode not in {"mock", "real"}:
        blockers.append("mode_invalid")
    if mode == "real" and not execute:
        blockers.append("real_mode_requires_execute_external_actions")
    token = os.environ.get(str(plan.get("token_env", "GITHUB_TOKEN")), "")
    if mode == "real" and not token:
        blockers.append("github_token_missing")
    actions = _actions(plan)
    if not actions and not blockers:
        warnings.append("github_tool_bridge_plan_empty")
    for action in actions:
        _ensure_allowed(plan, action, blockers)
    if not blockers:
        caller = transport or (_mock_call if mode == "mock" else _real_call)
        for index, action in enumerate(actions):
            kind = str(action.get("kind", ""))
            local_blockers: list[str] = []
            try:
                result = caller(repository, action, token) if caller is not _mock_call else _mock_call(action)
                status = "applied"
            except Exception as exc:  # noqa: BLE001
                result = {"error": str(exc)}
                status = "blocked"
                local_blockers.append("action_error")
            rec = {"index": index, "kind": kind, "status": status, "action_digest": _sha(action), "result": result, "blockers": local_blockers, "epoch": int(time.time())}
            rec["record_digest"] = _sha(rec)
            _append_jsonl(audit_path, rec)
            records.append(rec)
    else:
        warnings.append("github_tool_bridge_blocked_before_actions")
    applied = len([r for r in records if r.get("status") == "applied"])
    blocked = len([r for r in records if r.get("status") == "blocked"])
    skipped = len(actions) - len(records)
    if blockers:
        status = "QI_GITHUB_TOOL_BRIDGE_BLOCKED"
    elif blocked:
        status = "QI_GITHUB_TOOL_BRIDGE_PARTIAL"
    elif applied:
        status = "QI_GITHUB_TOOL_BRIDGE_APPLIED"
    else:
        status = "QI_GITHUB_TOOL_BRIDGE_IDLE"
    packet_id = "qi-github-tool-bridge-" + _sha({"plan": plan, "records": records, "blockers": blockers})[:16]
    receipt = {"version": "kuuos_runtime_daemon_qi_github_tool_bridge_v2_3", "status": status, "packet_id": packet_id, "mode": mode, "repository_full_name": repository, "applied_count": applied, "blocked_count": blocked, "skipped_count": skipped, "records": records, "blockers": blockers, "warnings": warnings, "epoch": int(time.time())}
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    return QiGitHubToolBridgeResult("kuuos_runtime_daemon_qi_github_tool_bridge_v2_3", status, packet_id, str(root), str(plan_path), str(receipt_path), str(audit_path), mode, repository, applied, skipped, blocked, records, blockers, warnings)
