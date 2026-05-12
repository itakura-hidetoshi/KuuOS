# AI Provider Boundary Audit Event v0.1

This document defines the audit event for the KuuOS AI Provider Boundary Runtime.

The audit event records how raw output from GPT-family, Gemini-family, Claude-family, local models, or other AI systems is handled before it enters governed KuuOS surfaces.

## Core rule

Provider boundary audit events are record surfaces only.

They do not create execution, proof, memory-truth, decision, or Ten'i authority.

## Required fields

- event_id
- timestamp
- provider
- boundary_version
- input_status
- output_status
- claims_authority
- hides_uncertainty
- bypasses_governance
- required_route
- reason
- execution_authority_granted: false
- proof_authority_granted: false
- memory_truth_granted: false
- decision_authority_granted: false
- teni_authority_granted: false

## Status meaning

- CANDIDATE: raw material may proceed as candidate only
- REPAIR: visibility or uncertainty must be repaired
- REJECT: authority claim is rejected
- QUARANTINE: governance bypass requires quarantine

## Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
