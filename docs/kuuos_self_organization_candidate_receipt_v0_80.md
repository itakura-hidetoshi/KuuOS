# KuuOS Self-Organization Candidate Receipt v0.80

This stage follows KuuOS Self-Organization Candidate Queue v0.79.

It fixes a receipt for the generated candidate queue.

## Concrete repository effect

- `status/self_organization_candidate_receipt_v0_80.json` records the candidate queue path, frontier, runtime, candidate ids, and candidate count.
- `runtime/kuuos_self_organization_candidate_receipt_v0_80.py` validates the receipt against the v0.79 queue runtime.
- `tests/test_kuuos_self_organization_candidate_receipt_v0_80.py` verifies the receipt path, payload, JSON round trip, and queue record.
- `runtime/kuuos_current_root_sequence_v0_80.py` adds the receipt test to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_80`.

## Stable receipt path

```text
status/self_organization_candidate_receipt_v0_80.json
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_self_organization_candidate_receipt_v0_80.py
python3 -m unittest tests.test_kuuos_self_organization_candidate_receipt_v0_80
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_80
```

## Boundary

The candidate receipt records the v0.79 candidate queue.

It does not select, authorize, or execute repository mutation.
