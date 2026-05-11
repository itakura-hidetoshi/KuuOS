# Invariant Pipeline Release Attestation v0.1

This document defines the release attestation surface for the KuuOS invariant pipeline.

The attestation binds these integrity roots into one reviewable record:

- release bundle root hash
- invariant pipeline audit hash-chain root
- invariant pipeline WORM export receipt root reference
- generated manifest policy

## 1. Core Rule

The release attestation is an integrity summary surface only.

It does not create execution, proof, clinical, truth, or Ten'i authority.

## 2. Generated Attestation

Generated path:

- specs/invariant_pipeline_release_attestation_v0_1.generated.json

Builder:

- scripts/build_invariant_pipeline_release_attestation_v0_1.py

Validator:

- scripts/validate_invariant_pipeline_release_attestation_v0_1.py

## 3. Required Fields

The generated attestation includes:

- id
- version
- generated_at
- bundle_manifest_path
- bundle_root_hash
- audit_hash_chain_path
- audit_hash_chain_root_hash
- worm_receipt_path
- worm_receipt_source_ledger_root_hash
- generated_manifest_policy_path
- authority_note
- non_authority_flags

## 4. Required Boundaries

The attestation must preserve:

- execution_authority_granted: false
- proof_authority_granted: false
- clinical_authority_granted: false
- truth_authority_granted: false
- teni_authority_granted: false

## 5. Validation Command

Run:

- make invariant-pipeline-attest
- make invariant-pipeline-checks
- make all-governance-checks

## 6. Guardrails

The release attestation must not be used as:

- execution authority
- proof authority
- clinical authority
- truth proof
- Ten'i proof
- replacement for evidence
- replacement for audit hash-chain
- replacement for WORM export receipt
- replacement for governance review

## 7. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
