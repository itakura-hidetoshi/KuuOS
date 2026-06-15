#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import json, os, pathlib, time
from typing import Any, Mapping
from runtime.kuuos_indra_qi_licensed_plural_routing_dry_run_core_v0_21 import (
    DECISIONS, LEDGER_VERSION, REQUIRED_BOUNDARY, STATE_VERSION,
    analyze_dry_run, evaluate_dry_run, mapping, sha, state_digest, valid_digest,
    validate_license, validate_plan, validate_report, validate_sources,
)

VERSION="indra_qi_licensed_plural_routing_dry_run_v0_21"
READY="INDRA_QI_LICENSED_PLURAL_ROUTING_DRY_RUN_V0_21_READY"
BLOCKED="INDRA_QI_LICENSED_PLURAL_ROUTING_DRY_RUN_V0_21_BLOCKED"

@dataclass(frozen=True)
class Result:
    version:str; status:str; packet_id:str; runtime_root:str
    dry_run_program_id:str; dry_run_id:str; world_model_id:str
    source_plural_routing_decision:str; decision:str
    recommendation_only:bool; routing_activated:bool
    source_world_state_digest:str; source_plural_routing_proposal_digest:str
    source_plural_routing_state_digest:str; source_plural_routing_recommendation_digest:str
    plural_routing_dry_run_report_digest:str; plural_routing_dry_run_state_digest:str
    ledger_record_digest:str; blockers:list[str]

def read(path:pathlib.Path)->dict[str,Any]:
    try: value=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError): return {}
    return dict(value) if isinstance(value,Mapping) else {}

def readl(path:pathlib.Path)->list[dict[str,Any]]:
    if not path.is_file(): return []
    out=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        try: value=json.loads(line)
        except json.JSONDecodeError: value={"_invalid":True}
        out.append(dict(value) if isinstance(value,Mapping) else {"_invalid":True})
    return out

def write(path:pathlib.Path,payload:Mapping[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(dict(payload),ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    os.replace(tmp,path)

def append(path:pathlib.Path,payload:Mapping[str,Any])->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload),ensure_ascii=False,sort_keys=True)+"\n")

def validate_ledger(rows:list[dict[str,Any]],program:str,world:str,blockers:list[str])->list[dict[str,Any]]:
    prev="GENESIS"; runs=set(); pairs=set(); reports=set()
    for i,row in enumerate(rows):
        run=str(row.get("dry_run_id",""))
        pair=(str(row.get("source_plural_routing_proposal_digest","")),str(row.get("source_plural_routing_recommendation_digest","")))
        report=str(row.get("plural_routing_dry_run_report_digest",""))
        ok=(row.get("version")==LEDGER_VERSION and valid_digest(row,"record_digest")
            and row.get("prev_record_digest")==prev and row.get("dry_run_program_id")==program
            and row.get("world_model_id")==world and run and run not in runs
            and all(pair) and pair not in pairs and report and report not in reports)
        if row.get("_invalid") or not ok: blockers.append(f"dry_run_ledger_record_{i}_invalid")
        runs.add(run); pairs.add(pair); reports.add(report); prev=str(row.get("record_digest",""))
    return rows

def build_licensed_plural_routing_dry_run(
    *, runtime_context:Mapping[str,Any], plural_routing_dry_run_plan:Mapping[str,Any],
    plural_routing_dry_run_license:Mapping[str,Any], plural_routing_dry_run_report:Mapping[str,Any],
)->Result:
    ctx=mapping(runtime_context); plan=dict(mapping(plural_routing_dry_run_plan))
    lic=mapping(plural_routing_dry_run_license); report=dict(mapping(plural_routing_dry_run_report))
    blockers=[]; root_value=ctx.get("runtime_root")
    root=pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value or root==pathlib.Path("/").resolve(): blockers.append("runtime_root_invalid")
    if ctx.get("indra_qi_licensed_plural_routing_dry_run_v0_21_enabled") is not True: blockers.append("dry_run_enabled_not_true")
    if ctx.get("apply_indra_qi_licensed_plural_routing_dry_run_v0_21") is not True: blockers.append("dry_run_apply_not_true")

    validate_plan(plan,blockers)
    world=read(root/"ku_indra_qi_noncommutative_mandala_world_state.json")
    proposal=read(root/"indra_qi_bounded_plural_shadow_routing_proposal_v0_20.json")
    source_state=read(root/"indra_qi_bounded_plural_shadow_routing_state_v0_20.json")
    source_rec=read(root/"indra_qi_bounded_plural_shadow_routing_recommendation_v0_20.json")
    source=validate_sources(world,proposal,source_state,source_rec,plan,blockers)
    ticks=validate_report(report,plan,source,blockers); validate_license(lic,plan,report,source,blockers)

    program=str(plan.get("dry_run_program_id","")); run=str(plan.get("dry_run_id","")); world_id=str(plan.get("world_model_id",""))
    ledger_path=root/"indra_qi_licensed_plural_routing_dry_run_ledger_v0_21.jsonl"
    prior=validate_ledger(readl(ledger_path),program,world_id,blockers)
    pair=(str(source.get("proposal_digest","")),str(source.get("recommendation_digest","")))
    report_sha=str(report.get("plural_routing_dry_run_report_digest",""))
    if any(r.get("dry_run_id")==run or (r.get("source_plural_routing_proposal_digest"),r.get("source_plural_routing_recommendation_digest"))==pair
           or r.get("plural_routing_dry_run_report_digest")==report_sha for r in prior):
        blockers.append("dry_run_replay_detected")
    prior_state=read(root/"indra_qi_licensed_plural_routing_dry_run_state_v0_21.json")
    if prior_state and not valid_digest(prior_state,"plural_routing_dry_run_state_digest"): blockers.append("dry_run_prior_state_digest_invalid")
    if prior_state and prior_state.get("last_source_plural_routing_state_digest")==source.get("state_digest"):
        blockers.append("dry_run_source_plural_routing_state_not_advanced")

    analysis=analyze_dry_run(ticks,plan,source); evaluation=evaluate_dry_run(analysis,str(source.get("source_decision","")))
    decision=str(evaluation.get("decision","hold_for_observation"))
    if decision not in DECISIONS: blockers.append("dry_run_decision_invalid")
    if blockers:
        decision="quarantine_recommended"; evaluation={"decision_reasons":["fail_closed_on_validation_or_integrity_loss"],"dry_run_ready":False}

    now=int(time.time())
    sf={"source_world_state_digest":str(source.get("world_digest","")),
        "source_plural_routing_proposal_digest":str(source.get("proposal_digest","")),
        "source_plural_routing_state_digest":str(source.get("state_digest","")),
        "source_plural_routing_recommendation_digest":str(source.get("recommendation_digest","")),
        "plural_routing_dry_run_report_digest":report_sha}
    brief={k:v for k,v in analysis.items() if k!="tick_results"}
    summary={"version":"indra_qi_licensed_plural_routing_dry_run_summary_v0_21","dry_run_program_id":program,
        "dry_run_id":run,"world_model_id":world_id,"source_plural_routing_decision":str(source.get("source_decision","")),
        **sf,"replica_input_digest":str(report.get("replica_input_digest","")),"dry_run_analysis":analysis,
        "isolated_replica_stream_only":True,"routing_activated":False,"live_route_enabled":False,
        "winner_selected":False,"external_actuation_enabled":False,"world_update_enabled":False,
        "recommendation_only":True,"epoch":now}
    summary["plural_routing_dry_run_summary_digest"]=sha(summary)
    authority={"direct_routing_activation_authority":False,"direct_winner_selection_authority":False,
        "direct_lineage_selection_authority":False,"direct_lineage_execution_authority":False,
        "direct_world_update_authority":False,"direct_external_actuation_authority":False,
        "direct_promotion_authority":False,"direct_rollback_authority":False,
        "direct_quarantine_authority":False,"truth_authority":False}
    rec={"version":"indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21","dry_run_program_id":program,
        "dry_run_id":run,"world_model_id":world_id,"source_plural_routing_decision":str(source.get("source_decision","")),
        "decision":decision,"decision_reasons":list(evaluation.get("decision_reasons",[])),
        "dry_run_ready":bool(evaluation.get("dry_run_ready")),"routing_activated":False,"winner_selected":False,
        "plural_routing_dry_run_summary_digest":summary["plural_routing_dry_run_summary_digest"],
        "dry_run_analysis":brief,**sf,"recommendation_only":True,"dry_run_not_routing_activation":True,
        **authority,"boundary":dict(REQUIRED_BOUNDARY),"epoch":now}
    rec["plural_routing_dry_run_recommendation_digest"]=sha(rec)
    ledger={"version":LEDGER_VERSION,"record_type":"licensed_plural_routing_dry_run","dry_run_program_id":program,
        "dry_run_id":run,"world_model_id":world_id,**sf,"source_proposal_run_id":str(source.get("source_proposal_run_id","")),
        "source_plural_routing_decision":str(source.get("source_decision","")),
        "plural_routing_dry_run_summary_digest":summary["plural_routing_dry_run_summary_digest"],
        "dry_run_analysis":brief,"decision":decision,"routing_activated":False,"winner_selected":False,
        "recommendation_only":True,"prev_record_digest":str(prior[-1].get("record_digest","GENESIS")) if prior else "GENESIS",
        "boundary":{**REQUIRED_BOUNDARY,"source_files_unchanged":True,"no_routing_activated":True,
                    "no_winner_selected":True,"no_lineage_executed_live":True,
                    "no_world_transition_executed":True,"no_external_actuation_executed":True},"epoch":now}
    ledger["record_digest"]=sha(ledger)
    state={"version":STATE_VERSION,"dry_run_program_id":program,"world_model_id":world_id,"last_dry_run_id":run,
        "last_source_world_state_digest":sf["source_world_state_digest"],
        "last_source_plural_routing_proposal_digest":sf["source_plural_routing_proposal_digest"],
        "last_source_plural_routing_state_digest":sf["source_plural_routing_state_digest"],
        "last_source_plural_routing_recommendation_digest":sf["source_plural_routing_recommendation_digest"],
        "last_plural_routing_dry_run_report_digest":report_sha,
        "latest_source_plural_routing_decision":str(source.get("source_decision","")),
        "latest_plural_routing_dry_run_decision":decision,
        "latest_plural_routing_dry_run_summary_digest":summary["plural_routing_dry_run_summary_digest"],
        "latest_dry_run_analysis":brief,"latest_dry_run_record_digest":ledger["record_digest"],
        "prev_plural_routing_dry_run_state_digest":str(prior_state.get("plural_routing_dry_run_state_digest","GENESIS")) if prior_state else "GENESIS",
        "boundary":{"dry_run_state_only":True,"isolated_replica_stream_only":True,"routing_activated":False,
                    "winner_selected":False,"recommendation_only":True,"multi_world_noncollapse_preserved":True},
        "epoch":now}
    state["plural_routing_dry_run_state_digest"]=state_digest(state)
    status=READY if not blockers else BLOCKED
    receipt={"version":VERSION,"status":status,"dry_run_program_id":program,"dry_run_id":run,"world_model_id":world_id,
        "source_plural_routing_decision":str(source.get("source_decision","")),"decision":decision,
        "routing_activated":False,"winner_selected":False,"recommendation_only":True,**sf,
        "plural_routing_dry_run_summary_digest":summary["plural_routing_dry_run_summary_digest"] if not blockers else "",
        "plural_routing_dry_run_state_digest":state["plural_routing_dry_run_state_digest"] if not blockers else str(prior_state.get("plural_routing_dry_run_state_digest","")),
        "ledger_record_digest":ledger["record_digest"] if not blockers else "","blockers":blockers,
        "boundary":{**REQUIRED_BOUNDARY,"dry_run_observation_committed":not blockers},"epoch":now}
    receipt["packet_id"]="indra-qi-licensed-plural-routing-dry-run-"+sha(receipt)[:16]
    if not blockers:
        write(root/"indra_qi_licensed_plural_routing_dry_run_summary_v0_21.json",summary)
        write(root/"indra_qi_licensed_plural_routing_dry_run_recommendation_v0_21.json",rec)
        write(root/"indra_qi_licensed_plural_routing_dry_run_state_v0_21.json",state); append(ledger_path,ledger)
    if lic.get("receipt_write_allowed") is True: write(root/"indra_qi_licensed_plural_routing_dry_run_receipt_v0_21.json",receipt)
    if lic.get("audit_append_allowed") is True:
        append(root/"indra_qi_licensed_plural_routing_dry_run_audit_v0_21.jsonl",{**receipt,"audit_record_digest":sha(receipt)})
    return Result(VERSION,status,str(receipt["packet_id"]),str(root),program,run,world_id,
        str(source.get("source_decision","")),decision,True,False,sf["source_world_state_digest"],
        sf["source_plural_routing_proposal_digest"],sf["source_plural_routing_state_digest"],
        sf["source_plural_routing_recommendation_digest"],report_sha,
        state["plural_routing_dry_run_state_digest"] if not blockers else str(prior_state.get("plural_routing_dry_run_state_digest","")),
        ledger["record_digest"] if not blockers else "",blockers)
