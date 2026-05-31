# MemoryOS JSON Governance

This directory stores the repository-pinned JSON receipt surface for the MemoryOS weekly strict routine.

The GitHub Actions workflow `.github/workflows/memoryos-json-governance.yml` treats these JSON files as operational evidence only:

- CI pass is not theorem authority.
- Local integrity signatures are not external identity signatures.
- Memory persistence is not belief sovereignty.
- Drift numbers are not claimed unless the JSON receipt exists.
- Follow-up bundles are candidates, not releases.

## Required current JSON

```text
memoryos/ops/current/run_status.json
memoryos/ops/current/policy/report.json
memoryos/ops/current/policy/signature_eval.json
memoryos/ops/current/lockset/lockset.json
memoryos/ops/current/registry/registry.json
memoryos/ops/current/mandala/anchor_skeleton.json
memoryos/ops/current/mandala/drift.json
memoryos/ops/current/mandala/alerts.json
```

## Required prev comparison JSON

```text
memoryos/ops/prev/mandala/anchor_skeleton.json
memoryos/ops/prev/mandala/drift.json
```

The `prev` and `current` trees are intentionally explicit so GitHub Actions can detect unsafe drift without inventing unseen values.
