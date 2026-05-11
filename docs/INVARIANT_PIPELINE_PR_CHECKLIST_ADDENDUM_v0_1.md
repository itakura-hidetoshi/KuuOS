# Invariant Pipeline PR Checklist Addendum v0.1

This addendum extends the KuuOS pull request checklist for invariant pipeline audit lineage changes.

For PRs touching invariant pipeline files, verify:

- make invariant-pipeline-checks passes.
- make all-governance-checks passes.
- Matrix, Gate, Pipeline, Audit Event, Hash-Chain, and WORM receipt validators pass.
- The hash-chain root is stable or the root change is explicitly explained.
- The WORM receipt root matches the computed hash-chain root.
- Non-authority fields remain false.
- No audit lineage field is used as execution, proof, clinical, truth, or Ten'i authority.

Current public fixture root:

306539394814c591b1cfb559f117a844afe1cddc6c05850c51255631998ac4c9

Boundary:

A PR may add audit visibility, but it must not add hidden authority.

Version: v0.1
Date: 2026-05-11
Author: Hidetoshi Itakura / 板倉英俊
