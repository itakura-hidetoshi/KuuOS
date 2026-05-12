# Emptiness Middle Way Core Audit Hash-Chain Ledger v0.1

This document defines the append-only hash-chain ledger for Emptiness / Dependent Origination / Two Truths / Middle Way core audit events.

The ledger records decisions about reification, nihilism, two-truths collapse, hidden lineage, and hidden harm.

## Core rule

The audit hash-chain is a record lineage only.

It does not create execution, proof, truth, essence, or Ten'i authority.

## Ledger fields

Each JSONL entry contains:

- sequence
- previous_hash
- event
- event_hash
- entry_hash

## Hash rules

- event_hash = sha256(canonical_json(event))
- entry_hash = sha256(canonical_json({sequence, previous_hash, event_hash}))
- first previous_hash = GENESIS

## Fixture

- specs/emptiness_middle_way_core_audit_hash_chain_fixture_v0_1.jsonl

## Validation

- python3 scripts/validate_emptiness_middle_way_core_audit_hash_chain_v0_1.py
- make core-governance-checks
- make all-governance-checks

## Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
