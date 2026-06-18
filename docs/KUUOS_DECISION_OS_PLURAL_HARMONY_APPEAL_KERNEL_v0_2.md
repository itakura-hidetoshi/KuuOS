# KuuOS DecisionOS Plural Harmony and Appeal Kernel v0.2

DecisionOS v0.2 is an additive layer above DecisionOS v0.1. It evaluates the same admissible option field from multiple stakeholder-local value sections, preserves disagreement, validates protective veto claims against mission-bound constraints, computes broad-acceptability signals, and keeps appeals append-only.

```text
v0.20 Mission Contract
  + BeliefOS v0.3
  + DecisionOS v0.1 committed decision basis
  + stakeholder-local value sections
  -> DecisionOS v0.2 plural harmony and appeal
  -> CONSENSUS_CANDIDATE / NEGOTIATE / APPEAL / HANDOVER / HOLD / REJECT / QUARANTINE
  -> future-only plural decision basis
  -> v0.21 Replan
```

DecisionOS v0.2 does not execute an action, grant a host license, turn consensus into truth, or allow one stakeholder's raw veto signal to become sovereign authority.

## 1. Additive boundary

v0.1 remains frozen as the source of:

- admissible option IDs;
- option dimension intervals;
- excluded options and reasons;
- robust-dominance relations;
- retained alternatives;
- decision basis digest;
- mission and belief source digests.

v0.2 stores the exact v0.1 state and decision-basis digests and never rewrites the v0.1 ledger.

## 2. Strict plural cycle

```text
BIND_V01
  -> REGISTER_STAKEHOLDERS
  -> EVALUATE_PLURALITY
  -> VALIDATE_VETOES
  -> AGGREGATE
  -> EXPLAIN
  -> APPEAL_WINDOW
  -> ADJUDICATE
  -> COMMIT
```

Phase skipping, stale digest use, event-index regression, time regression, replay mutation, and source-option expansion are rejected.

## 3. Stakeholder sections

Each stakeholder section declares:

```text
stakeholder_id
role
weight
profile_weights
minimum_acceptable_value
disagreement_point
protected_constraint_digests
veto
appeal_right
```

`profile_weights` are nonnegative and sum to one across the DecisionOS v0.1 positive and negative dimensions. A stakeholder's interval utility for option `a` is:

```text
H_i.lower(a)
  = sum positive_profile_weight * positive_lower
    - sum negative_profile_weight * negative_upper

H_i.upper(a)
  = sum positive_profile_weight * positive_upper
    - sum negative_profile_weight * negative_lower
```

The intervals remain explicit. Stakeholder values are not collapsed into a single universal value ontology.

## 4. Veto as a boundary signal

A raw veto claim contains:

```text
option_id
constraint_digest
evidence_digest
reason_digest
```

It excludes an option only when all conditions hold:

```text
constraint_digest is mission-bound
constraint_digest is registered as protected for that stakeholder
option_id is in the v0.1 admissible field
evidence_digest is present
claim is structurally valid
```

Such a claim becomes a `validated_protective_veto`. An unvalidated veto remains visible as an objection but grants no unilateral authority.

```text
raw veto != sovereign authority
validated protective veto != truth
validated protective veto -> option exclusion from consensus set
```

## 5. Broad acceptability

For each option and stakeholder:

```text
supports_i(a) = H_i.lower(a) >= minimum_acceptable_value_i
opposes_i(a)  = H_i.upper(a) <  minimum_acceptable_value_i
uncertain_i(a) otherwise
```

The kernel records support, opposition, and uncertainty weights.

A broadly acceptable option requires:

```text
no validated protective veto
support_weight >= minimum_support_weight
opposition_weight <= maximum_opposition_weight
minimum stakeholder lower utility >= minimum_worst_case_value
```

These are hard plural gates, not advisory scores.

## 6. Aggregation without total-value sovereignty

Three distinct signals are retained.

### Weighted median

The weighted median of stakeholder interval midpoints represents a robust center of expressed acceptability. It is not a truth estimate.

### Nash surplus

For stakeholder `i`:

```text
lower_surplus_i(a) = max(0, H_i.lower(a) - disagreement_point_i)
upper_surplus_i(a) = max(0, H_i.upper(a) - disagreement_point_i)
```

The lower and upper Nash products are stored. Zero surplus for one stakeholder remains visible rather than being averaged away.

### Max-min floor

```text
worst_case_lower(a) = min_i H_i.lower(a)
```

This prevents a high aggregate score from hiding a severely burdened stakeholder.

No one signal is allowed to erase the others. Ranking is lexicographic only inside the already broadly acceptable set:

```text
higher worst_case_lower
then higher lower Nash product
then higher weighted median
then stable option_id order
```

## 7. Routes

### CONSENSUS_CANDIDATE

Exactly one option is top-ranked among broadly acceptable options, has no validated veto, and no material appeal requires reopening.

### NEGOTIATE

Broadly acceptable options exist but plurality, close ranking, or unresolved stakeholder objections requires future-only adjustment.

### APPEAL

A material appeal with new evidence, protected-boundary relevance, or source inconsistency requires reopening. The prior decision remains historically intact.

### HANDOVER

Clinical, institutional, legal, human, or other higher authority is required.

### HOLD

No responsible progression is available, but the option field remains repairable or observable.

### REJECT

No option survives the plural hard gates.

### QUARANTINE

Source digest, option field, veto binding, or ledger integrity is invalid.

## 8. Explanation

The explanation packet preserves:

- every stakeholder utility interval for every option;
- support/opposition/uncertainty classification;
- weighted median;
- lower and upper Nash products;
- worst-case lower utility;
- validated and unvalidated veto claims;
- broadly acceptable set;
- ranking tuple;
- retained alternatives;
- stakeholder-ablation contributions;
- exact source digests.

For stakeholder ablation:

```text
contribution_i(a)
  = aggregate_with_all(a) - aggregate_without_i(a)
```

This is an explanation of aggregation sensitivity, not causal truth or moral worth.

## 9. Appeal semantics

Each appeal stores:

```text
appeal_id
stakeholder_id
target_option_id
reason_digest
evidence_digests
protected_boundary_claimed
source_inconsistency_claimed
materiality
```

Appeals are append-only. They cannot delete or rewrite a prior v0.1 or v0.2 decision. A material appeal changes only a future route and future Replan basis.

## 10. Persistent store

```text
plural-genesis.json
plural-ledger.jsonl
plural-snapshot.json
.decision-os-v02.lock
```

The ledger is authoritative; the snapshot is derived. The store provides exclusive writer locking, digest chaining, fsync-before-snapshot, atomic replacement, replay idempotence, stale-state rejection, malformed-ledger rejection, chain verification, restart recovery, and ledger-derived snapshot repair.

## 11. Replan bridge

A v0.2 commit requires:

```text
future_only = true
memory_overwrite = false
plural_decision_not_execution = true
consensus_not_truth = true
activation_boundary = mission_replan_only
```

Only `CONSENSUS_CANDIDATE`, `NEGOTIATE`, `APPEAL`, `HANDOVER`, and `HOLD` may create a future Replan basis. No route grants execution or clinical authority.

## 12. Formal surface

The Lean surface proves:

- strict typed phase order;
- strict event-index increase;
- stakeholder utility interval ordering;
- weighted support is bounded by total stakeholder weight;
- validated veto excludes consensus eligibility;
- raw veto grants no authority;
- Nash surplus and Nash product are nonnegative;
- worst-case lower utility is no greater than every stakeholder lower utility;
- consensus certificate implies no validated veto and broad-support gates;
- appeal append is strict and history-preserving;
- commit is future-only and non-overwriting;
- consensus grants neither truth nor execution authority;
- Replan is required before activation.

## 13. Public boundary

DecisionOS v0.2 is a structural, governance, and proof-facing plural deliberation layer. It is not majority-rule sovereignty, a moral truth oracle, clinical authorization, institutional approval, legal adjudication, host license, or autonomous execution authority.
