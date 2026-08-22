#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
from typing import Any, Iterable, Mapping

VERSION = "kuuos_github_ci_completion_reentry_v1_1"
READY = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_EVENT_READY"
BLOCKED = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_EVENT_BLOCKED"
VERIFIED = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED"
VERIFY_BLOCKED = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFY_BLOCKED"

_COMPLETED = "completed"
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_TERMINAL_CONCLUSIONS = {
    "success", "failure", "cancelled", "timed_out", "neutral", "skipped",
    "stale", "action_required", "startup_failure",
}


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _i(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _names(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _workflow_run_event(raw: Mapping[str, Any]) -> dict[str, Any]:
    run = _m(raw.get("workflow_run")); repo = _m(raw.get("repository"))
    return {"source":"workflow_run","action":str(raw.get("action","")),"repository":str(repo.get("full_name","")),"run_id":_i(run.get("id"),0),"workflow_name":str(run.get("name","")),"head_sha":str(run.get("head_sha","")).lower(),"head_branch":str(run.get("head_branch","")),"status":str(run.get("status","")),"conclusion":run.get("conclusion"),"run_event":str(run.get("event","")),"required_job_names":[],"required_step_names":[]}


def _repository_dispatch_event(raw: Mapping[str, Any]) -> dict[str, Any]:
    payload = _m(raw.get("client_payload"))
    return {"source":"repository_dispatch","action":"completed","repository":str(payload.get("repository","")),"run_id":_i(payload.get("run_id"),0),"workflow_name":str(payload.get("workflow_name","")),"head_sha":str(payload.get("head_sha","")).lower(),"head_branch":str(payload.get("head_branch","")),"status":str(payload.get("status","")),"conclusion":payload.get("conclusion"),"run_event":str(payload.get("run_event","")),"required_job_names":_names(payload.get("required_job_names")),"required_step_names":_names(payload.get("required_step_names"))}


def normalize_event(raw: Mapping[str, Any], event_name: str | None = None) -> dict[str, Any]:
    if event_name == "workflow_run" or (event_name is None and isinstance(raw.get("workflow_run"), Mapping)):
        return _workflow_run_event(raw)
    if event_name == "repository_dispatch" or (event_name is None and isinstance(raw.get("client_payload"), Mapping)):
        return _repository_dispatch_event(raw)
    return {"source":str(event_name or "unknown"),"action":"","repository":"","run_id":0,"workflow_name":"","head_sha":"","head_branch":"","status":"","conclusion":None,"run_event":"","required_job_names":[],"required_step_names":[]}


def compile_completion_event(raw: Mapping[str, Any], *, event_name: str | None = None, repository_allowlist: Iterable[str] = (), workflow_allowlist: Iterable[str] = ()) -> dict[str, Any]:
    event = normalize_event(raw, event_name); blockers: list[str] = []
    repos = {str(x) for x in repository_allowlist if str(x)}; workflows = {str(x) for x in workflow_allowlist if str(x)}
    if event["source"] not in {"workflow_run","repository_dispatch"}: blockers.append("event_source_not_supported")
    if event["action"] != _COMPLETED: blockers.append("event_action_not_completed")
    if "/" not in event["repository"]: blockers.append("repository_invalid")
    if repos and event["repository"] not in repos: blockers.append("repository_not_allowlisted")
    if event["run_id"] <= 0: blockers.append("run_id_invalid")
    if not event["workflow_name"]: blockers.append("workflow_name_missing")
    if workflows and event["workflow_name"] not in workflows: blockers.append("workflow_not_allowlisted")
    if _SHA40.fullmatch(event["head_sha"]) is None: blockers.append("head_sha_invalid")
    if event["status"] != _COMPLETED: blockers.append("workflow_run_not_completed")
    if event["conclusion"] not in _TERMINAL_CONCLUSIONS: blockers.append("workflow_conclusion_not_terminal")
    event_packet = {"version":VERSION,"status":READY if not blockers else BLOCKED,"event":event,"event_digest":_digest(raw),"signal_is_success_evidence":False,"fresh_mcp_reobservation_required":True,"blockers":blockers,"boundary":{"github_event_is_wakeup_signal_only":True,"github_event_does_not_prove_ci_success":True,"mcp_fresh_observation_required_before_reentry":True,"reentry_does_not_grant_merge_or_write_authority":True}}
    reobserve_request: dict[str, Any] = {}
    if not blockers:
        reobserve_request = {"version":"qi_github_actions_ci_completion_reobserve_request_v1_1","reobserve_allowed":True,"observation_kind":"workflow_run_jobs","repo_full_name":event["repository"],"run_id":event["run_id"],"commit_sha":event["head_sha"],"source_commit_sha":event["head_sha"],"expected_head_sha":event["head_sha"],"expected_workflow_name":event["workflow_name"],"expected_conclusion":event["conclusion"],"required_job_names":event["required_job_names"],"required_step_names":event["required_step_names"],"source_event_digest":_digest(event_packet),"fresh_mcp_reobservation_required":True}
    return {"event_packet":event_packet,"reobserve_request":reobserve_request}


def _steps(jobs: list[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    out: list[Mapping[str, Any]] = []
    for job in jobs:
        raw = job.get("steps", [])
        if isinstance(raw, list): out.extend(step for step in raw if isinstance(step, Mapping))
    return out


def verify_fresh_reobservation(event_packet: Mapping[str, Any], *, observed_run: Mapping[str, Any], observed_jobs: list[Mapping[str, Any]]) -> dict[str, Any]:
    blockers: list[str] = []; packet = _m(event_packet); event = _m(packet.get("event"))
    if packet.get("status") != READY: blockers.append("event_packet_not_ready")
    if packet.get("signal_is_success_evidence") is not False: blockers.append("event_signal_must_not_be_success_evidence")
    if packet.get("fresh_mcp_reobservation_required") is not True: blockers.append("fresh_mcp_reobservation_requirement_missing")
    if str(observed_run.get("repository", event.get("repository", ""))) != str(event.get("repository", "")): blockers.append("observed_repository_mismatch")
    if _i(observed_run.get("id"),0) != _i(event.get("run_id"),0): blockers.append("observed_run_id_mismatch")
    if str(observed_run.get("name","")) != str(event.get("workflow_name","")): blockers.append("observed_workflow_name_mismatch")
    if str(observed_run.get("head_sha","")).lower() != str(event.get("head_sha","")).lower(): blockers.append("observed_head_sha_mismatch")
    if str(observed_run.get("status","")) != _COMPLETED: blockers.append("observed_workflow_not_completed")
    if observed_run.get("conclusion") != event.get("conclusion"): blockers.append("observed_conclusion_mismatch")
    jobs = [job for job in observed_jobs if isinstance(job, Mapping)]
    if not jobs: blockers.append("fresh_jobs_missing")
    if any(str(job.get("status","")) != _COMPLETED for job in jobs): blockers.append("observed_job_not_completed")
    required_jobs = _names(event.get("required_job_names"))
    if required_jobs:
        by_name = {str(job.get("name","")):job for job in jobs}
        for name in required_jobs:
            job = by_name.get(name)
            if job is None: blockers.append(f"required_job_missing:{name}")
            elif str(job.get("status","")) != _COMPLETED: blockers.append(f"required_job_not_completed:{name}")
    required_steps = _names(event.get("required_step_names")); all_steps = _steps(jobs)
    if required_steps:
        by_name = {str(step.get("name","")):step for step in all_steps}
        for name in required_steps:
            step = by_name.get(name)
            if step is None: blockers.append(f"required_step_missing:{name}")
            elif str(step.get("status","")) != _COMPLETED: blockers.append(f"required_step_not_completed:{name}")
            elif step.get("conclusion") is None: blockers.append(f"required_step_conclusion_missing:{name}")
    route = "blocked"
    if not blockers: route = "verified_success" if event.get("conclusion") == "success" else "verified_non_success"
    return {"version":VERSION,"status":VERIFIED if not blockers else VERIFY_BLOCKED,"route":route,"repository":event.get("repository"),"run_id":event.get("run_id"),"head_sha":event.get("head_sha"),"workflow_name":event.get("workflow_name"),"event_conclusion":event.get("conclusion"),"fresh_mcp_reobservation":True,"merge_authority_granted":False,"write_authority_granted":False,"blockers":blockers,"evidence_digest":_digest({"event_packet":packet,"observed_run":observed_run,"observed_jobs":jobs})}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True)+"\n")


def _self_check() -> None:
    sha = "a"*40
    valid = {"action":"completed","repository":{"full_name":"itakura-hidetoshi/KuuOS"},"workflow_run":{"id":42,"name":"KuuOS Runtime Full Check","head_sha":sha,"head_branch":"main","status":"completed","conclusion":"success","event":"push"}}
    compiled = compile_completion_event(valid,event_name="workflow_run",repository_allowlist=["itakura-hidetoshi/KuuOS"],workflow_allowlist=["KuuOS Runtime Full Check"]); packet = compiled["event_packet"]
    assert packet["status"] == READY and packet["signal_is_success_evidence"] is False and compiled["reobserve_request"]["run_id"] == 42
    verified = verify_fresh_reobservation(packet,observed_run={"repository":"itakura-hidetoshi/KuuOS","id":42,"name":"KuuOS Runtime Full Check","head_sha":sha,"status":"completed","conclusion":"success"},observed_jobs=[{"name":"runtime","status":"completed","conclusion":"success","steps":[{"name":"check","status":"completed","conclusion":"success"}]}])
    assert verified["status"] == VERIFIED and verified["route"] == "verified_success" and verified["merge_authority_granted"] is False
    mismatched = verify_fresh_reobservation(packet,observed_run={"repository":"itakura-hidetoshi/KuuOS","id":42,"name":"KuuOS Runtime Full Check","head_sha":"b"*40,"status":"completed","conclusion":"success"},observed_jobs=[{"name":"runtime","status":"completed","conclusion":"success"}])
    assert mismatched["status"] == VERIFY_BLOCKED and "observed_head_sha_mismatch" in mismatched["blockers"]
    pending = dict(valid); pending["action"] = "requested"; blocked = compile_completion_event(pending,event_name="workflow_run")
    assert blocked["event_packet"]["status"] == BLOCKED and "event_action_not_completed" in blocked["event_packet"]["blockers"]


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--self-check",action="store_true"); parser.add_argument("--event"); parser.add_argument("--event-name"); parser.add_argument("--output-dir",default=".kuuos/github-ci-completion-reentry-v1-1"); parser.add_argument("--repository",action="append",default=[]); parser.add_argument("--workflow",action="append",default=[]); args = parser.parse_args()
    if args.self_check:
        _self_check(); print("KUUOS_GITHUB_CI_COMPLETION_REENTRY_V1_1_SELF_CHECK_OK"); return 0
    if not args.event: parser.error("--event is required unless --self-check is used")
    raw = json.loads(pathlib.Path(args.event).read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping): raise SystemExit("event payload must be a JSON object")
    compiled = compile_completion_event(raw,event_name=args.event_name,repository_allowlist=args.repository,workflow_allowlist=args.workflow); out = pathlib.Path(args.output_dir)
    _write_json(out/"qi_github_actions_ci_completion_event_packet.json",compiled["event_packet"])
    if compiled["reobserve_request"]: _write_json(out/"qi_github_actions_status_reobserve_request.json",compiled["reobserve_request"])
    print(compiled["event_packet"]["status"]); return 0 if compiled["event_packet"]["status"] == READY else 2


if __name__ == "__main__": raise SystemExit(main())
