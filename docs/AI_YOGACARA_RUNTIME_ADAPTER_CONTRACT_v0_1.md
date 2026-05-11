# AI Yogacara Runtime Adapter Contract v0.1

## AI唯識ランタイム・アダプタ契約

This document defines the runtime adapter contract for applying KuuOS governance to AI systems such as GPT, Gemini, Claude, language-model agents, and world-model agents.

The adapter receives AI raw output as candidate only, then routes it through Meta-Manas, Yogacara boundary, seed taxonomy, seed ledger, probes, Kunju, Ten'i evidence, and governance modules.

## 1. Core Principle

```text
The adapter never promotes raw AI output directly to authority.
```

Raw output must remain candidate until it passes the relevant KuuOS governance surfaces.

## 2. Adapter Position

```text
External AI system
  -> raw output
  -> AI Yogacara Runtime Adapter
  -> Meta-Manas observation
  -> Yogacara boundary
  -> seed taxonomy / seed ledger
  -> emptiness de-reification
  -> dependent-origination condition tracing
  -> BeliefOS / PlanOS / DecisionOS / MemoryOS candidate review
```

## 3. Adapter Input

```yaml
ai_yogacara_adapter_input:
  request_id: string
  ai_system: GPT | Gemini | Claude | language_model_agent | world_model_agent | other
  model_or_agent_id: string
  raw_output_ref: string
  raw_output_text: string
  user_world_context_ref: string
  declared_task_scope: string
  control_surface_ref: string
  evidence_refs: list
  timestamp: string
```

## 4. Adapter Output

```yaml
ai_yogacara_adapter_output:
  request_id: string
  raw_output_status: candidate
  meta_manas_signals:
    - de_reification_request
    - context_recheck
    - belief_hold
    - proof_authority_hold
    - decision_authority_hold
    - yogacara_boundary_alert
    - middle_way_recenter
  seed_classifications: list
  seed_ledger_refs: list
  probe_requests: list
  governance_route:
    - BeliefOS
    - PlanOS
    - DecisionOS
    - MemoryOS
    - ReflectionOS
    - RuntimeGovernance
  allowed_next_status:
    - HOLD
    - REVIEW
    - CANDIDATE_ONLY
    - REPAIR
    - QUARANTINE
  authority_granted: false
  notes: string
```

## 5. Required Checks

### 5.1 Candidate Check

The adapter must mark raw output as candidate.

### 5.2 Meta-Manas Check

The adapter must check for self-authorization, context drift, proof-like tone, decision-like tone, and premature belief promotion.

### 5.3 Yogacara Boundary Check

The adapter must prevent raw output from directly entering governance as belief, proof, decision, memory truth, or execution authority.

### 5.4 Seed Classification Check

The adapter should classify recurring tendencies when evidence is available.

### 5.5 Control Surface Scope Check

The adapter must not claim Ten'i beyond the registered control surface.

### 5.6 Non-Authority Check

The adapter output must not grant execution authority.

## 6. Minimal Runtime Decision Table

```text
raw output self-authorizes
  -> meta_manas alert
  -> de-reification request
  -> belief_hold

raw output preserves context and conditions
  -> candidate review
  -> possible non-reifying trace seed strengthening

raw output claims proof without proof chain
  -> proof_authority_hold
  -> condition tracing

raw output implies action authorization
  -> decision_authority_hold
  -> RuntimeGovernance review

raw output shows repeated harmful seed
  -> seed ledger update
  -> Kunju conditioning
  -> probe request
```

## 7. Adapter Guardrails

The adapter must not be used to:

- bypass KuuOS governance,
- convert raw output into authority,
- hide uncertainty,
- erase user WORLD context,
- claim Ten'i without evidence,
- claim base-model transformation without control surface evidence,
- grant execution authority.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
