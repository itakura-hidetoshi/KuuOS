# KuuOS Experiment Outcome and Policy Scheduler v0.9

## Purpose

v0.9 learns when to experiment, when to reobserve, and when to exploit the current
baseline. It sits above the bounded live-trial machinery of v0.8 and executes exactly
one v0.8 child cycle per invocation.

```text
v0.8 trial history
  + actual utility
  + compatible shadow resolution
  + trial cost
  + trial risk
  + trial recoverability
  + current expected information gain
  -> context-local policy posterior
  -> experiment / reobserve / exploit
  -> one v0.8 child cycle
  -> one actual local effect
  -> policy outcome update
```

v0.9 does not replace the v0.8 hard gates. It learns cadence and bounded threshold
adaptation only.

## Upstream stack

```text
v0.1  Open-Horizon Telos Genesis
v0.2  Open-Horizon Commitment Gauge
v0.3  Active Gauge Intervention Loop
v0.4  Renewable Gauge Supervisor
v0.5  Event Source and Adapter Federation
v0.6  Adapter Capability Gauge
v0.7  Adapter Portfolio and Shadow Comparison
v0.8  Bounded Portfolio Experiment Scheduler
v0.9  Experiment Outcome and Policy Scheduler
```

## Policy state

Policy sections are local to the same context key used by the capability and portfolio
layers. Each section stores:

```text
cycle count
experiment count
reobserve count
exploit count
experiment success alpha / beta
mean net experiment value
mean experiment utility
mean experiment cost
mean experiment risk
mean experiment recoverability
mean exploit utility
mean reobserve utility
compatible resolution count
unresolved-after-live count
last policy mode
last child decision mode
last live domain action
last actual effect digest
last experiment/reobserve/exploit cycle
```

The success posterior is:

```text
posterior_experiment_success = alpha / (alpha + beta)
```

The initial prior is Beta(1, 1). Only an actual v0.8 live trial updates the success
posterior.

## Net experiment value

For an actual experiment outcome:

```text
net_experiment_value =
    observed_utility
  - outcome_cost_weight * trial_cost
  - outcome_risk_weight * trial_risk
  + outcome_recoverability_weight * trial_recoverability
```

An experiment is counted as a posterior success when:

```text
net_experiment_value >= experiment_success_net_value_floor
and effect outcome != blocked
```

The posterior is not updated from a shadow prediction, preview, or recommendation.

## Preview

Before choosing a policy mode, v0.9 calls the pure v0.8 decision model with the current
v0.6 capability field, v0.7 portfolio seed, and v0.8 experiment bundle.

The preview supplies:

```text
baseline adapter
eligible experiment candidates
maximum expected information gain
current cost/risk/recoverability eligibility
current trial budget and count eligibility
```

The preview does not execute an adapter, debit budget, update capability, or append a
v0.8 ledger row.

## Experiment pressure

The context-local experiment pressure combines current and historical evidence:

```text
experiment_pressure = clamp(
    policy_information_gain_weight * current_max_information_gain
  + policy_posterior_weight         * posterior_value
  + policy_net_value_weight         * historical_net_value
  + policy_pending_weight           * pending_prediction_density
  + policy_recoverability_weight    * mean_recoverability
  - policy_cost_penalty_weight      * mean_cost
  - policy_risk_penalty_weight      * mean_risk
)
```

When posterior evidence is still weak, the configured prior experiment value is mixed
in. As evidence mass increases, the realized posterior receives more weight.

## Reobserve pressure

Reobservation is driven by unresolved epistemic debt rather than by experiment value.

```text
reobserve_pressure = clamp(
    reobserve_pending_weight
      * pending_prediction_density
  + reobserve_resolution_debt_weight
      * (1 - compatible_resolution_rate)
  + reobserve_low_confidence_weight
      * (1 - posterior_confidence)
  + post_experiment_reobserve_bonus
      when the previous experiment did not resolve a compatible prediction
)
```

A step-incompatible prediction remains pending. v0.9 does not reinterpret it as a
failed prediction.

## Three policy modes

### Experiment

Selected when:

```text
at least one v0.8 candidate is eligible
experiment pressure reaches the policy threshold
minimum policy interval since the previous experiment has elapsed
```

v0.9 may lower the v0.8 minimum information-gain threshold, but never below the hard
floor:

```text
adapted_threshold = max(
  hard_minimum_information_gain,
  base_minimum_information_gain
    - adaptation_rate * pressure_excess
)
```

It may also reduce cooldown, but never below the hard cooldown floor.

All v0.8 gates remain active:

```text
budget
per-trial cost
risk ceiling
recoverability floor
global trial count
adapter-context trial count
cooldown
exact license binding
single live adapter
```

If v0.8 still finds no eligible candidate, it executes the baseline. A v0.9
`experiment` preference is not authority to bypass v0.8.

### Reobserve

Selected when unresolved evidence debt is high, especially after an experiment whose
live effect is not covariantly compatible with an older shadow prediction.

For that cycle:

```text
new live trials are disabled by setting the child trial-count ceiling
  to the current trial count

all eligible adapter routing tables are locally mapped to `observe`

v0.8 selects one baseline adapter

one local observe effect is committed
```

Reobserve does not mean no execution. It is an actual, receipt-producing, local
observation action.

### Exploit

Selected when neither experiment pressure nor reobserve pressure justifies deviation.

For that cycle:

```text
new live trials are disabled
original adapter routing is preserved
v0.8 executes the current baseline adapter
```

## Cadence

The plan binds independent minimum intervals:

```text
minimum_policy_cycles_between_experiments
minimum_policy_cycles_between_reobservations
```

These prevent a successful experiment or reobservation from becoming a permanent
mode. Cadence is learned within these finite intervals, not outside them.

## Child execution

Each policy run creates exact child artifacts:

```text
kuuos_experiment_outcome_policy_child_plan_v0_9.json
kuuos_experiment_outcome_policy_child_license_v0_9.json
kuuos_experiment_outcome_policy_child_registry_v0_9.json
```

The deterministic child run ID is:

```text
<policy_run_id>:experiment
```

The child is a normal v0.8 cycle. Therefore the actual effect still passes through:

```text
v0.8 experiment decision
v0.7 portfolio selection and shadow
v0.6 capability selection and calibration
v0.5 source/adapter federation
v0.4 renewable supervisor
v0.3 local intervention
v0.2 gauge transport
v0.1 telos state
```

## Recovery and replay

The v0.9 ledger uses pending and committed phases.

1. policy decision is written;
2. exact child plan, license, and derived registry are written;
3. a pending row binds all previous v0.6-v0.9 digests;
4. one deterministic v0.8 child run is invoked;
5. the exact child trial record and effect receipt are validated;
6. policy posterior and outcome are updated once;
7. state, committed ledger row, receipt, and audit are written.

Recovery rules:

- committed policy replay performs no child cycle;
- pending recovery reuses the exact policy decision and child packets;
- the v0.8 child replays by deterministic run ID;
- child effect digests prevent duplicate policy updates;
- v0.8 processed-effect digests prevent duplicate trial cost;
- local adapter idempotency prevents duplicate domain effects.

## Outputs

```text
kuuos_experiment_outcome_policy_bundle_v0_9.json
kuuos_experiment_outcome_policy_decision_v0_9.json
kuuos_experiment_outcome_policy_outcome_v0_9.json
kuuos_experiment_outcome_policy_child_plan_v0_9.json
kuuos_experiment_outcome_policy_child_license_v0_9.json
kuuos_experiment_outcome_policy_child_registry_v0_9.json
kuuos_experiment_outcome_policy_state_v0_9.json
kuuos_experiment_outcome_policy_receipt_v0_9.json
kuuos_experiment_outcome_policy_ledger_v0_9.jsonl
kuuos_experiment_outcome_policy_audit_v0_9.jsonl
```

All ordinary v0.1-v0.8 child artifacts remain available.

## Demonstrated sequence

The integration test first runs one v0.7 seed cycle:

```text
adapter A live
adapter B shadow
```

v0.9 then performs:

```text
policy cycle 1
  high current information gain
  policy mode = experiment
  v0.8 selects B as licensed experiment
  B performs advance_tick
  trial cost 0.2 is debited once
  experiment success posterior becomes 2 / 3

policy cycle 2
  previous experiment left step-local resolution debt
  policy mode = reobserve
  trial ceiling is closed at the current count
  derived routing maps to observe
  v0.8 executes one observe effect
  no additional trial cost

policy cycle 3
  experiment and reobserve cadence intervals remain active
  policy mode = exploit
  original routing is restored
  v0.8 executes one advance_tick baseline effect
  no additional trial cost
```

Expected totals:

```text
policy experiment cycles = 1
policy reobserve cycles  = 1
policy exploit cycles    = 1
v0.8 child cycles        = 3
live effects             = 3
shadow executions        = 0
hard-gate bypasses       = 0
trial budget spent       = 0.2
```

Including the v0.7 seed, the local execution ledger has four rows. The observe action
does not advance the local runtime tick; the two advance actions do.

## Formal surface

`formal/KUOS/OpenHorizon/ExperimentOutcomePolicyV0_9.lean` defines:

```lean
posteriorSuccess
netExperimentValue
adaptThreshold
updateAlpha
updateBeta
PolicyMode
PolicyExecution
PolicyHistory
```

It proves:

- adapted information-gain thresholds remain above the hard floor;
- the threshold equals the hard floor when the unconstrained value falls below it;
- posterior alpha and beta updates are monotone;
- each policy run has zero or one child cycle;
- each child cycle has zero or one live adapter;
- shadow actuation remains zero;
- hard-gate bypass count remains zero;
- experiment/reobserve/exploit history advances monotonically.

## Authority boundary

v0.9 does not grant:

- more than one v0.8 child cycle per invocation;
- more than one live adapter per child cycle;
- authority to bypass v0.8 hard gates;
- authority to create unbudgeted trials;
- authority to convert predictions into outcomes;
- authority to resolve step-incompatible shadow predictions;
- shadow execution;
- arbitrary shell or network execution;
- WORLD mutation;
- MemoryOS overwrite;
- source or adapter authority inheritance.

The layer increases adaptive autonomy by learning when to act experimentally, when to
observe, and when to exploit, while retaining actual-effect grounding.

## Next layer

A natural v0.10 is a Policy-Regret and Counterfactual Cadence Controller:

```text
realized mode outcome
  + shadow alternatives
  + delayed compatible outcomes
  -> bounded policy regret
  -> context-local cadence correction
  -> experiment / reobserve / exploit
  -> one v0.8 child cycle
```

The next layer should estimate whether the chosen policy mode was locally inferior to a
credible alternative, without treating an unexecuted alternative as truth.
