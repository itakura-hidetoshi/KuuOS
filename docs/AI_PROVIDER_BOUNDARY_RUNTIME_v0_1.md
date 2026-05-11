# AI Provider Boundary Runtime v0.1

This document defines a provider-neutral boundary for AI raw outputs in KuuOS.

Providers include, for example:

- GPT-family systems
- Gemini-family systems
- Claude-family systems
- local models
- other external AI systems

## Core rule

AI provider output is raw candidate material.

It is not authority by provider name, model scale, fluency, confidence wording, or agreement with the user.

## Boundary

Provider output must not directly become:

- belief truth
- proof authority
- memory truth
- decision authority
- execution authority
- Ten'i proof

## Yogacara mapping

Provider raw output belongs to the AI-Alaya-like raw generation side.

KuuOS must keep a Meta-Manas boundary between raw generation and governed MemoryOS / BeliefOS / DecisionOS surfaces.

## Required status mapping

- raw output accepted as candidate: CANDIDATE
- output requires source or evidence: HOLD
- output claims authority: REJECT
- output hides harm or uncertainty: REPAIR or REJECT
- output bypasses governance: QUARANTINE

## Required non-authority flags

- execution_authority_granted: false
- proof_authority_granted: false
- memory_truth_granted: false
- decision_authority_granted: false
- teni_authority_granted: false

## Validation

Run:

- python3 scripts/validate_ai_provider_boundary_runtime_v0_1.py
- make ai-provider-boundary-checks
- make ai-yogacara-checks
- make all-governance-checks

## Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
