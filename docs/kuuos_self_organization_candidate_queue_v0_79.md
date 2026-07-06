# KuuOS Self-Organization Candidate Queue v0.79

This stage follows KuuOS README Surface Exposure v0.78.

It adds a proposal-only candidate queue derived from the current surface.

## Concrete repository effect

- `status/self_organization_candidate_queue_v0_79.json` stores generated self-organization candidates.
- `runtime/kuuos_self_organization_candidate_queue_v0_79.py` validates the queue against the current surface entrypoint and surface index.
- `tests/test_kuuos_self_organization_candidate_queue_v0_79.py` verifies the queue path, payload, JSON round trip, proposal-only mode, and candidate ids.
- `runtime/kuuos_current_root_sequence_v0_79.py` adds the candidate queue test to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_79`.

## Stable candidate queue path

```text
status/self_organization_candidate_queue_v0_79.json
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_self_organization_candidate_queue_v0_79.py
python3 -m unittest tests.test_kuuos_self_organization_candidate_queue_v0_79
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_79
```

## Boundary

The candidate queue proposes next stages.

It does not select, authorize, or execute repository mutation.
