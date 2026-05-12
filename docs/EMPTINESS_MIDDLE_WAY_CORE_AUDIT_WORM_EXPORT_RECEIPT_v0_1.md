# Emptiness Middle Way Core Audit WORM Export Receipt v0.1

This document defines the WORM export receipt for the Emptiness / Dependent Origination / Two Truths / Middle Way core audit hash-chain ledger.

The receipt records the exported hash-chain root for core boundary decisions about reification, nihilism, two-truths collapse, hidden lineage, and hidden harm.

## Core rule

WORM export preserves core audit lineage.

It does not create execution, proof, truth, essence, or Ten'i authority.

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
- truth_authority_granted: false
- essence_authority_granted: false
- teni_authority_granted: false

## Fixture

- specs/emptiness_middle_way_core_audit_worm_export_receipt_fixture_v0_1.json

## Validation

- python3 scripts/validate_emptiness_middle_way_core_audit_worm_export_receipt_v0_1.py
- make core-governance-checks
- make all-governance-checks

## Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
