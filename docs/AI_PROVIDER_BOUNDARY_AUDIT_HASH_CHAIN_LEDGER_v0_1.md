# AI Provider Boundary Audit Hash-Chain Ledger v0.1

This document defines the append-only hash-chain ledger for AI Provider Boundary audit events.

The ledger records provider-neutral boundary decisions for raw AI outputs before they enter governed KuuOS surfaces.

## Core rule

Provider boundary audit lineage is a record surface only.

It does not create execution, proof, memory-truth, decision, or Ten'i authority.

## Ledger entry fields

Each JSONL entry contains:

- sequence
- previous_hash
- event
- event_hash
- entry_hash

## Hash rules

- event_hash = sha256(canonical_json(event))
- entry_hash = sha256(canonical_json({sequence, previous_hash, event_hash}))
- entry[n].previous_hash == entry[n-1].entry_hash
- first previous_hash = GENESIS

## Required non-authority fields

- execution_authority_granted: false
- proof_authority_granted: false
- memory_truth_granted: false
- decision_authority_granted: false
- teni_authority_granted: false

## Fixture

- specs/ai_provider_boundary_audit_hash_chain_fixture_v0_1.jsonl

## Validation

- python3 scripts/validate_ai_provider_boundary_audit_hash_chain_v0_1.py
- make ai-provider-boundary-checks
- make ai-yogacara-checks
- make all-governance-checks

## Version

Version: v0.1
Date: 2026-05-12
Author: Hidetoshi Itakura / 板倉英俊
