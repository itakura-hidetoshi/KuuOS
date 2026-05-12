# AI Provider Boundary Audit WORM Export Receipt v0.1

This document defines the WORM export receipt for the AI Provider Boundary audit hash-chain ledger.

The receipt records the exported hash-chain root for provider-neutral raw AI output boundary decisions.

## Core rule

WORM export preserves provider boundary lineage.

It does not create execution, proof, memory-truth, decision, or Ten'i authority.

## Receipt fields

- id
- version
- exported_at
- source_ledger
- source_ledger_root_hash
- exported_entry_count
- export_mode
- retention_policy
- object_lock_mode
- non_authority_note
- execution_authority_granted: false
- proof_authority_granted: false
- memory_truth_granted: false
- decision_authority_granted: false
- teni_authority_granted: false

## Fixture

- specs/ai_provider_boundary_audit_worm_export_receipt_fixture_v0_1.json

## Validation

- python3 scripts/validate_ai_provider_boundary_audit_worm_export_receipt_v0_1.py
- make ai-yogacara-checks
- make all-governance-checks

## Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
