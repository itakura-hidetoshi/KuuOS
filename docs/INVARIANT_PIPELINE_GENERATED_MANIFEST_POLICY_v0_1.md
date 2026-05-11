# Invariant Pipeline Generated Manifest Policy v0.1

This document defines how KuuOS handles the generated invariant pipeline release bundle manifest.

Generated file:

- specs/invariant_pipeline_release_bundle_manifest_v0_1.generated.json

## 1. Core Rule

The generated manifest is a reproducible integrity artifact.

It is generated from repository files by:

- scripts/build_invariant_pipeline_release_bundle_manifest_v0_1.py

and validated by:

- scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py

## 2. Fresh-Build Default

The validator runs the builder first.

This prevents stale generated manifests from controlling validation results.

## 3. CI Behavior

In CI, the generated manifest may be created inside the workflow workspace.

The generated manifest does not need to grant authority or alter source semantics.

## 4. Local Behavior

In local development, running:

- make invariant-pipeline-build-bundle
- make invariant-pipeline-validate-bundle
- make invariant-pipeline-checks

may update the generated manifest file.

A root change should be reviewed when release content changes.

## 5. Authority Boundary

The generated manifest and bundle root are integrity surfaces only.

They do not create execution, proof, clinical, truth, or Ten'i authority.

They do not replace:

- audit hash-chain root
- WORM export receipt
- evidence
- governance review
- runtime validation

## 6. Version

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
