#!/usr/bin/env python3
"""
MemoryOS JSON Governance Guard v0.1

Non-authoritative CI guard for MemoryOS JSON surfaces.
CI pass != theorem authority.
JSON persistence != memory sovereignty.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

REQUIRED_CURRENT = [
    "run_status.json",
    "policy/report.json",
    "policy/signature_eval.json",
    "lockset/lockset.json",
    "registry/registry.json",
    "mandala/alerts.json",
    "mandala/anchor_skeleton.json",
    "mandala/drift.json",
]

REQUIRED_PREV = [
    "mandala/anchor_skeleton.json",
    "mandala/drift.json",
]

DEFAULT_THRESHOLD = 0.6


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def read_json(path: Path) -> tuple[Optional[Any], Optional[str]]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, "missing"
    except json.JSONDecodeError as e:
        return None, f"json_decode_error:{e.msg}:line={e.lineno}:col={e.colno}"
    except Exception as e:
        return None, f"read_error:{type(e).__name__}:{e}"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def scan_json_syntax(root: Path) -> list[dict[str, Any]]:
    problems: list[dict[str, Any]] = []
    if not root.exists():
        return [{"path": str(root), "problem": "root_missing"}]
    for p in sorted(root.rglob("*.json")):
        _, err = read_json(p)
        if err:
            problems.append({"path": str(p), "problem": err})
    return problems


def rel_exists(root: Path, rel: str) -> dict[str, Any]:
    p = root / rel
    return {"path": rel, "exists": p.exists(), "sha256": sha256_bytes(p.read_bytes()) if p.exists() else None}


def extract_anchor_set(obj: Any) -> set[str]:
    if obj is None:
        return set()
    if isinstance(obj, list):
        return {str(x) for x in obj}
    if isinstance(obj, dict):
        for key in ("anchors", "anchor_ids", "anchor_skeleton", "items", "nodes"):
            value = obj.get(key)
            if isinstance(value, list):
                out: set[str] = set()
                for item in value:
                    if isinstance(item, str):
                        out.add(item)
                    elif isinstance(item, dict):
                        for id_key in ("id", "anchor", "name", "key"):
                            if id_key in item:
                                out.add(str(item[id_key]))
                                break
                        else:
                            out.add(json.dumps(item, ensure_ascii=False, sort_keys=True))
                    else:
                        out.add(str(item))
                return out
        out: set[str] = set()

        def walk(prefix: str, value: Any) -> None:
            if isinstance(value, dict):
                for k, v in value.items():
                    walk(f"{prefix}/{k}" if prefix else str(k), v)
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    walk(f"{prefix}[{i}]", v)
            else:
                out.add(prefix)

        walk("", obj)
        return out
    return {str(obj)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def dig(obj: Any, path: Iterable[str], default: Any = None) -> Any:
    cur = obj
    for part in path:
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def count_alerts(alerts_obj: Any, run_status: Any) -> int:
    direct = dig(run_status, ["alerts_count"], None)
    if isinstance(direct, int):
        return direct
    if isinstance(alerts_obj, dict):
        if isinstance(alerts_obj.get("alerts_count"), int):
            return alerts_obj["alerts_count"]
        if isinstance(alerts_obj.get("alerts"), list):
            return len(alerts_obj["alerts"])
    if isinstance(alerts_obj, list):
        return len(alerts_obj)
    return 0


def count_signature_failures(sig_obj: Any, run_status: Any) -> int:
    direct = dig(run_status, ["signature_fail_count"], None)
    if isinstance(direct, int):
        return direct
    if isinstance(sig_obj, dict):
        for key in ("signature_fail_count", "fail_count", "failed_count"):
            if isinstance(sig_obj.get(key), int):
                return sig_obj[key]
        checks = sig_obj.get("checks")
        if isinstance(checks, list):
            return sum(1 for c in checks if isinstance(c, dict) and c.get("ok") is False)
    return 0


def sign_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    body = canonical_json(payload)
    key = os.environ.get("MEMORYOS_JSON_GOVERNANCE_HMAC_KEY")
    if key:
        return {
            "algorithm": "HMAC-SHA256",
            "key_source": "MEMORYOS_JSON_GOVERNANCE_HMAC_KEY",
            "signature": hmac.new(key.encode("utf-8"), body, hashlib.sha256).hexdigest(),
            "authority": "local_integrity_only_not_identity_signature",
        }
    return {
        "algorithm": "SHA256-CANONICAL-JSON",
        "key_source": "none",
        "signature": sha256_bytes(body),
        "authority": "local_integrity_only_unsigned_identity",
    }


def build_followup(reason_codes: list[str], metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "bundle_id": "memoryos_json_governance_followup_candidate_v0_1",
        "created_at": utc_now(),
        "signed": False,
        "authority": "advisory_only",
        "reason_codes": reason_codes,
        "metrics": metrics,
        "proposed_actions": [
            "pin_missing_or_renamed_json_surfaces",
            "fix_anchor_aliases_without_rewriting_history",
            "preserve_prev_current_comparison_visibility",
            "keep_signature_failures_visible",
            "do_not_convert_ci_pass_into_truth_authority",
        ],
    }


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--current", default="memoryos/ops/current")
    ap.add_argument("--prev", default="memoryos/ops/prev")
    ap.add_argument("--out-dir", default="_memoryos_json_governance")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--never-fail", action="store_true")
    args = ap.parse_args(argv)

    repo = Path(args.repo_root).resolve()
    current = (repo / args.current).resolve()
    prev = (repo / args.prev).resolve()
    out = (repo / args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    syntax_problems = scan_json_syntax(current) + scan_json_syntax(prev)
    current_checks = [rel_exists(current, rel) for rel in REQUIRED_CURRENT]
    prev_checks = [rel_exists(prev, rel) for rel in REQUIRED_PREV]
    missing_current = [c["path"] for c in current_checks if not c["exists"]]

    run_status, run_err = read_json(current / "run_status.json")
    report, report_err = read_json(current / "policy/report.json")
    sig_eval, sig_err = read_json(current / "policy/signature_eval.json")
    alerts, alerts_err = read_json(current / "mandala/alerts.json")
    cur_anchor, cur_anchor_err = read_json(current / "mandala/anchor_skeleton.json")
    prev_anchor, prev_anchor_err = read_json(prev / "mandala/anchor_skeleton.json")

    cur_set = extract_anchor_set(cur_anchor)
    prev_set = extract_anchor_set(prev_anchor)
    anchor_j = jaccard(prev_set, cur_set)

    chain_ok = bool(dig(run_status, ["chain_ok"], False)) and not missing_current
    alerts_count = count_alerts(alerts, run_status)
    signature_fail_count = count_signature_failures(sig_eval, run_status)
    policy_verdict = dig(report, ["verdict"], dig(report, ["policy_verdict"], "UNKNOWN"))

    reason_codes: list[str] = []
    if syntax_problems:
        reason_codes.append("json_syntax_problem")
    if missing_current:
        reason_codes.append("required_current_json_missing")
    if not chain_ok:
        reason_codes.append("chain_not_ok")
    if anchor_j < args.threshold:
        reason_codes.append("anchor_skeleton_jaccard_below_threshold")
    if alerts_count > 0:
        reason_codes.append("alerts_present")
    if signature_fail_count > 0:
        reason_codes.append("signature_failures_present")
    if policy_verdict not in ("PASS", "CONDITIONAL_PASS_OBSTRUCTION_VISIBLE"):
        reason_codes.append("policy_verdict_not_pass")

    metrics = {
        "chain_ok": chain_ok,
        "anchor_skeleton_jaccard": anchor_j,
        "current_anchor_count": len(cur_set),
        "prev_anchor_count": len(prev_set),
        "alerts_count": alerts_count,
        "signature_fail_count": signature_fail_count,
        "policy_verdict": policy_verdict,
        "missing_current_count": len(missing_current),
        "syntax_problem_count": len(syntax_problems),
    }

    status = "PASS" if not reason_codes else "FAIL_CANDIDATE_REQUIRED"
    receipt: dict[str, Any] = {
        "schema": "kuos.memoryos.json_governance.receipt.v0_1",
        "created_at": utc_now(),
        "status": status,
        "authority": "ci_validation_only_non_authoritative",
        "repo_root": str(repo),
        "current": args.current,
        "prev": args.prev,
        "threshold": args.threshold,
        "metrics": metrics,
        "reason_codes": reason_codes,
        "current_checks": current_checks,
        "prev_checks": prev_checks,
        "syntax_problems": syntax_problems,
        "read_errors": {
            "run_status": run_err,
            "policy_report": report_err,
            "signature_eval": sig_err,
            "alerts": alerts_err,
            "current_anchor": cur_anchor_err,
            "prev_anchor": prev_anchor_err,
        },
        "invariants": [
            "ci_pass_is_not_truth_authority",
            "json_persistence_is_not_memory_sovereignty",
            "append_only_followup_for_failures",
            "no_hidden_uncertainty",
            "same_root_visibility_required",
        ],
    }
    receipt["local_integrity_signature"] = sign_payload(receipt)
    write_json(out / "memoryos_json_governance_receipt.json", receipt)

    if reason_codes:
        candidate = build_followup(reason_codes, metrics)
        write_json(out / "followup_bundle_candidate" / "candidate.json", candidate)
        signed = dict(candidate)
        signed["signed"] = True
        signed["signature_scope"] = "local_integrity_only_not_identity_or_release_authority"
        signed["local_integrity_signature"] = sign_payload(candidate)
        write_json(out / "followup_bundle_candidate" / "signed_append_only_followup.json", signed)

    print(json.dumps({"status": status, "metrics": metrics, "reason_codes": reason_codes}, ensure_ascii=False, sort_keys=True))
    if status != "PASS" and not args.never_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
