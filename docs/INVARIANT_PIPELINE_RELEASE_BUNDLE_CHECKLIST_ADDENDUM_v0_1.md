# Invariant Pipeline Release Bundle Checklist Addendum v0.1

This addendum extends release and PR review for the invariant pipeline release bundle manifest.

Before release or merge, verify:

- make invariant-pipeline-build-bundle can generate the bundle manifest.
- make invariant-pipeline-validate-bundle passes.
- make invariant-pipeline-checks passes.
- make all-governance-checks passes.
- The generated manifest contains all required invariant pipeline files.
- Each listed file SHA256 matches repository content.
- The bundle root hash recomputes from ordered path and SHA256 pairs.
- The bundle root is not treated as the audit hash-chain root.
- The bundle manifest is not treated as WORM export receipt.
- The bundle manifest is not treated as execution, proof, clinical, truth, or Ten'i authority.

Boundary:

Release bundle integrity is a file-set integrity surface only.

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
