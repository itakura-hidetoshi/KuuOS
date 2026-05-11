# Invariant Pipeline Release Bundle Navigation Addendum v0.1

This addendum points readers to the invariant pipeline release bundle manifest.

Core file:

- docs/INVARIANT_PIPELINE_RELEASE_BUNDLE_MANIFEST_v0_1.md

Builder and validator:

- scripts/build_invariant_pipeline_release_bundle_manifest_v0_1.py
- scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py

Generated manifest path:

- specs/invariant_pipeline_release_bundle_manifest_v0_1.generated.json

Commands:

- make invariant-pipeline-build-bundle
- make invariant-pipeline-validate-bundle
- make invariant-pipeline-checks
- make all-governance-checks

Boundary:

The release bundle root proves file-set integrity only. It does not replace the audit hash-chain root, the WORM export receipt, evidence, governance review, or runtime validation.

The bundle root does not create execution, proof, clinical, truth, or Ten'i authority.

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
