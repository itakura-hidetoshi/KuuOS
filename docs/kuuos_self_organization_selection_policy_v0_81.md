# KuuOS Self-Organization Selection Policy v0.81

This stage follows KuuOS Self-Organization Candidate Receipt v0.80.

It publishes a policy-only rule set for later candidate selection.

## Concrete repository effect

- `status/self_organization_selection_policy_v0_81.json` records ranking rules and tie-breaker policy.
- `runtime/kuuos_self_organization_selection_policy_v0_81.py` validates the policy against the v0.80 receipt runtime.
- `tests/test_kuuos_self_organization_selection_policy_v0_81.py` verifies the policy path, payload, JSON round trip, and policy-only boundary.
- `runtime/kuuos_current_root_sequence_v0_81.py` adds the policy test to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_81`.

## Stable policy path

```text
status/self_organization_selection_policy_v0_81.json
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_self_organization_selection_policy_v0_81.py
python3 -m unittest tests.test_kuuos_self_organization_selection_policy_v0_81
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_81
```

## Boundary

The selection policy defines ranking rules.

It does not choose, authorize, or apply a candidate.
