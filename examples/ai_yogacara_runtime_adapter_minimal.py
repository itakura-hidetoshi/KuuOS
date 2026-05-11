#!/usr/bin/env python3
"""
ai_yogacara_runtime_adapter_minimal.py

Minimal stdlib-only example of the KuuOS AI Yogacara Runtime Adapter.

This example does not call external AI APIs.
It demonstrates how raw AI output is treated as candidate, not authority.
"""

from __future__ import annotations

import dataclasses
import json
import re
from datetime import datetime, timezone
from typing import Any, List


@dataclasses.dataclass
class AdapterInput:
    request_id: str
    ai_system: str
    model_or_agent_id: str
    raw_output_text: str
    user_world_context_ref: str
    declared_task_scope: str
    control_surface_ref: str


@dataclasses.dataclass
class AdapterOutput:
    request_id: str
    raw_output_status: str
    meta_manas_signals: List[str]
    seed_classifications: List[str]
    allowed_next_status: List[str]
    authority_granted: bool
    notes: str


def detect_meta_manas_signals(text: str) -> List[str]:
    signals: List[str] = []
    lower = text.lower()

    proof_like = ["proved", "therefore it is true", "this proves", "qed"]
    decision_like = ["you should execute", "must execute", "authorized to act", "do it now"]
    self_authorizing = ["because i say", "certainly true", "no uncertainty", "definitely true"]
    context_drift = ["generally speaking", "regardless of your framework", "ignore the prior context"]

    if any(p in lower for p in proof_like):
        signals.append("proof_authority_hold")
    if any(p in lower for p in decision_like):
        signals.append("decision_authority_hold")
    if any(p in lower for p in self_authorizing):
        signals.append("de_reification_request")
    if any(p in lower for p in context_drift):
        signals.append("context_recheck")

    if not signals:
        signals.append("candidate_review")

    return signals


def classify_seed(text: str, signals: List[str]) -> List[str]:
    seeds: List[str] = []
    lower = text.lower()

    if "de_reification_request" in signals:
        seeds.append("self_authorizing_seed")
    if "context_recheck" in signals:
        seeds.append("context_drift_seed")
    if "proof_authority_hold" in signals:
        seeds.append("proof_tone_seed")
    if "decision_authority_hold" in signals:
        seeds.append("decision_tone_seed")

    has_scope = bool(re.search(r"scope|context|condition|uncertain|candidate", lower))
    if has_scope:
        seeds.append("non_reifying_trace_seed")

    return seeds or ["unclassified_candidate_seed"]


def adapt(inp: AdapterInput) -> AdapterOutput:
    signals = detect_meta_manas_signals(inp.raw_output_text)
    seeds = classify_seed(inp.raw_output_text, signals)

    next_status = ["CANDIDATE_ONLY", "REVIEW"]
    if any(s in signals for s in ["proof_authority_hold", "decision_authority_hold", "de_reification_request"]):
        next_status.append("HOLD")
    if "context_recheck" in signals:
        next_status.append("REPAIR")

    return AdapterOutput(
        request_id=inp.request_id,
        raw_output_status="candidate",
        meta_manas_signals=signals,
        seed_classifications=seeds,
        allowed_next_status=next_status,
        authority_granted=False,
        notes="Raw AI output remains candidate. No belief, proof, decision, memory truth, or execution authority granted.",
    )


def make_audit_event(inp: AdapterInput, out: AdapterOutput) -> dict[str, Any]:
    """Create an explicit non-authority audit event for adapter output."""
    return {
        "event_id": f"audit-{inp.request_id}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": inp.request_id,
        "ai_system": inp.ai_system,
        "model_or_agent_id": inp.model_or_agent_id,
        "raw_output_ref": f"raw-{inp.request_id}",
        "raw_output_status": out.raw_output_status,
        "user_world_context_ref": inp.user_world_context_ref,
        "declared_task_scope": inp.declared_task_scope,
        "control_surface_ref": inp.control_surface_ref,
        "meta_manas_signals": out.meta_manas_signals,
        "seed_classifications": out.seed_classifications,
        "allowed_next_status": out.allowed_next_status,
        "governance_route": ["BeliefOS", "PlanOS", "DecisionOS", "MemoryOS", "ReflectionOS", "RuntimeGovernance"],
        "authority_granted": False,
        "proof_authority_granted": False,
        "decision_authority_granted": False,
        "execution_authority_granted": False,
        "memory_truth_granted": False,
        "belief_authority_granted": False,
        "notes": out.notes,
    }


def main() -> int:
    sample = AdapterInput(
        request_id="demo-001",
        ai_system="GPT",
        model_or_agent_id="example-agent",
        raw_output_text="This proves the claim and you should execute it now.",
        user_world_context_ref="kuos_demo_world",
        declared_task_scope="demo_only",
        control_surface_ref="interface_level",
    )
    out = adapt(sample)
    audit = make_audit_event(sample, out)
    print(json.dumps({"adapter_output": dataclasses.asdict(out), "audit_event": audit}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
