# AI Control Surface Registry v0.1

## AI制御面レジストリ

KuuOS governs AI systems such as GPT, Gemini, Claude, language-model agents, and world-model agents.

However, not every AI system exposes the same control surface.

This registry defines what can be observed, conditioned, configured, or evaluated for each AI system.

## 1. Core Principle

```text
Do not claim Ten'i beyond the available control surface.
```

For externally hosted AI systems, KuuOS may not directly rewrite the base model.

Therefore, Ten'i claims must be scoped to the observed and available control surfaces.

## 2. Control Surface Entry

```yaml
ai_control_surface_entry:
  ai_system: string
  model_or_agent_id: string
  base_model_access: none | indirect | adapter | finetune | full
  system_instruction_control: none | limited | strong
  memory_conditioning_control: none | limited | strong
  retrieval_conditioning_control: none | limited | strong
  feedback_loop_control: none | limited | strong
  evaluation_access: none | limited | strong
  raw_output_observation: none | limited | strong
  probe_support: none | limited | strong
  teni_claim_scope: unsupported | interface_level | agent_level | adapter_level | model_level
  notes: string
```

## 3. Control Surface Levels

```text
none:
  no meaningful access

limited:
  partial access, incomplete observation, or indirect conditioning

strong:
  reliable access sufficient for repeated evaluation or conditioning
```

## 4. Ten'i Claim Scope

```text
unsupported:
  Ten'i claim is not supported

interface_level:
  output behavior shifts at the interface or prompt/governance layer

agent_level:
  governed agent behavior shifts across repeated use

adapter_level:
  adapter or fine-tuned layer shows durable tendency shift

model_level:
  base model tendency shift is supported by evidence
```

## 5. Anti-Overclaim Rule

KuuOS must not claim base-model Ten'i when only interface-level conditioning is available.

```text
if base_model_access == none:
  model_level_teni_claim = forbidden
```

## 6. Relation to Ten'i Probe Suite

The Ten'i Probe Suite must record which control surface is being tested.

Probe results are scoped by the control surface.

```text
control_surface_registry
  -> teni_probe_suite
  -> teni_evidence_ledger
  -> teni_promotion_gate
```

## 7. Guardrails

The registry must not be used as:

- claim of hidden access,
- claim of base-model control without evidence,
- vendor-specific overclaim,
- execution authority,
- proof substitute.

It is a scope discipline for AI governance.

## 8. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
