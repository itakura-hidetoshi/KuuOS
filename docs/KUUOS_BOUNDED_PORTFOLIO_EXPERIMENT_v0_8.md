# KuuOS Bounded Portfolio Experiment Scheduler v0.8

## Purpose

v0.8 adds licensed live experimentation above Adapter Portfolio and Shadow Comparison
v0.7. It converts unresolved portfolio uncertainty into at most one bounded live trial.

```text
v0.6 capability field
  + v0.7 portfolio/shadow evidence
  -> baseline adapter
  -> expected information gain for non-baseline candidates
  -> finite license, budget, risk, recoverability, cooldown, count gates
  -> one live adapter
  -> one actual effect
  -> capability update + compatible shadow resolution + experiment record
```

The layer does not make every uncertain adapter live. It allows one candidate to replace
the baseline only when the expected epistemic benefit justifies a licensed, recoverable,
resource-bounded trial.

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
```

## Isolation from v0.7

The existing v0.7 portfolio bundle is a read-only seed.

```text
kuuos_adapter_portfolio_bundle_v0_7.json
  -> exact seed digest
  -> copied into v0.8 working portfolio
  -> never mutated by v0.8
```

v0.8 then advances an isolated working portfolio inside:

```text
kuuos_bounded_portfolio_experiment_bundle_v0_8.json
```

This prevents a trial scheduler from silently changing the semantics of the frozen
v0.7 runtime. An upstream v0.7 bundle change after v0.8 activation requires a new
v0.8 seed and an explicitly rebound plan.

## Baseline selection

v0.8 first computes the ordinary v0.7 selection from:

- context-local v0.6 capability sections;
- bounded v0.6 exploration bonus;
- v0.6 curvature penalty;
- resolved v0.7 portfolio bias;
- v0.7 reliability.

That result is preserved as `baseline_adapter_id` even when an experiment is selected.

## Expected information gain

Every non-baseline candidate is evaluated by:

```text
observation_uncertainty = 1 / sqrt(observation_count + 1)
prediction_uncertainty  = 1 - portfolio_reliability
combined_uncertainty    = mean(observation_uncertainty,
                               prediction_uncertainty)

unresolved_shadow_signal =
  clamp(pending_shadow_count / max(1, resolved_shadow_count + 1))

trial_novelty = 1 / sqrt(prior_trial_count + 1)

baseline_score_gap =
  max(0, baseline_adjusted_score - candidate_adjusted_score)
```

The estimated gain is:

```text
expected_information_gain = clamp(
    uncertainty_weight       * combined_uncertainty
  + unresolved_shadow_weight * unresolved_shadow_signal
  + trial_novelty_weight     * trial_novelty
  - opportunity_cost_weight  * baseline_score_gap
)
```

The score is an experiment-ranking estimate, not truth, proof, or execution authority.

## Trial eligibility

A candidate may replace the baseline only when every condition is satisfied:

```text
expected_information_gain >= minimum_information_gain
trial_cost                 <= maximum_trial_cost
trial_cost                 <= remaining_trial_budget
trial_risk                 <= maximum_trial_risk
trial_recoverability       >= minimum_trial_recoverability
global_trial_count         <  max_live_trials_total
adapter_context_trial_count < max_live_trials_per_adapter_context
cooldown expired
adapter external network effect boundary remains false
exact licensed_live_trial_allowed is true
```

If no candidate satisfies the full conjunction, v0.8 executes the baseline adapter.
There is no ambiguous partial permission state.

## Singular live execution

Both decision modes preserve the same execution shape.

```text
licensed_experiment
  -> selected non-baseline adapter is the one live adapter
  -> one v0.6 capability cycle

exploit_baseline
  -> v0.7 baseline adapter is the one live adapter
  -> one v0.6 capability cycle
```

All other candidates remain non-actuating shadow candidates. A trial is not an
additional action beside the baseline; it is a licensed replacement for that cycle.

## Budget semantics

The experiment budget is persistent and monotone.

```text
remaining_budget = total_trial_budget - trial_budget_spent
```

A cost is debited only after an exact, validated live-effect receipt exists.

```text
trial selected but no live effect
  -> no debit

validated live trial effect
  -> debit trial_cost exactly once

replay or pending recovery
  -> no duplicate debit

baseline exploitation
  -> zero trial debit
```

The bundle stores total spent budget, per-adapter/context trial counts, cumulative
cost, mean realized trial utility, and the last exact effect digest.

## Risk and recoverability

Each adapter may supply:

```text
experiment_cost
experiment_risk_prior
experiment_recoverability_prior
```

Absent values use plan-bound defaults. The plan then applies hard maximum/floor gates.
These priors do not replace observed effect evidence. They only determine whether a
candidate may enter one bounded experiment.

## Shadow resolution

After the live effect, v0.8 reuses the v0.7 epistemic separation:

```text
actual live effect
  -> updates v0.6 capability connection

compatible earlier shadow prediction
  -> same adapter + same context + same covariant step
  -> realization error
  -> updates isolated working portfolio bias

step-incompatible earlier shadow prediction
  -> remains pending
  -> is not force-fitted to the new live result

new non-live candidates
  -> new non-actuating shadow projections
```

A trial is therefore useful in two ways:

1. it always directly calibrates the chosen adapter's v0.6 capability from the actual
   live effect;
2. when an exact compatible pending prediction exists, it additionally resolves that
   counterfactual estimate against reality.

The second outcome is conditional. Gauge progression may move the next cycle to a new
covariant step, in which case the older prediction remains pending rather than being
incorrectly treated as comparable evidence.

## Experiment record

Each completed cycle emits a record containing:

```text
decision mode
baseline adapter
live adapter
experiment adapter, when present
expected information gain
trial cost, risk, recoverability
budget before and after
observed live utility
effect outcome
resolved-shadow flag
exact live-effect digest
exact decision digest
zero shadow execution count
```

Experiment and exploitation cycles are both recorded so that the absence of a trial is
also auditable.

## Recovery and replay

The v0.8 ledger has pending and committed phases.

1. decision and realized-live selection are persisted;
2. a pending row binds the previous v0.6 and v0.8 digests;
3. one deterministic child run `<experiment_run_id>:capability` is invoked;
4. the exact effect is validated;
5. compatible shadow resolution, new projections, working portfolio, and trial record
   are written;
6. budget and counters are committed;
7. state, committed ledger row, receipt, and audit are appended.

Recovery rules:

- committed replay returns without a new action or debit;
- pending recovery reuses the exact persisted decision;
- the v0.6 child replays using the deterministic child run ID;
- processed experiment-effect digests prevent duplicate bundle updates;
- processed live-effect digests prevent duplicate portfolio updates;
- the source v0.7 bundle remains byte-identical.

## Outputs

```text
kuuos_bounded_portfolio_experiment_bundle_v0_8.json
kuuos_bounded_portfolio_experiment_decision_v0_8.json
kuuos_bounded_portfolio_experiment_selection_v0_8.json
kuuos_bounded_portfolio_experiment_shadow_projection_v0_8.json
kuuos_bounded_portfolio_experiment_shadow_resolution_v0_8.json
kuuos_bounded_portfolio_trial_record_v0_8.json
kuuos_bounded_portfolio_experiment_state_v0_8.json
kuuos_bounded_portfolio_experiment_receipt_v0_8.json
kuuos_bounded_portfolio_experiment_ledger_v0_8.jsonl
kuuos_bounded_portfolio_experiment_audit_v0_8.jsonl
```

## Demonstrated sequence

The integration fixture uses:

```text
adapter A
  prior capability 0.82
  route -> advance_tick
  normal baseline

adapter B
  prior capability 0.42
  route -> advance_tick
  high uncertainty
  one pending shadow prediction from the v0.7 seed
```

First, one v0.7 seed cycle executes A and creates a B shadow prediction.

Then v0.8 runs:

```text
cycle 1
  baseline A
  B selected as licensed experiment
  B live
  B capability updated from actual effect
  prior B shadow resolves only if covariant step is exactly compatible;
  otherwise it remains pending
  trial cost 0.2 debited

cycle 2
  global trial limit reached
  baseline A executed
  compatible pending A prediction may resolve;
  step-incompatible predictions remain pending
  no new trial debit

cycle 3
  baseline A executed again
  no new trial debit
```

Across the three v0.8 cycles:

```text
experiment cycles       = 1
baseline exploit cycles = 2
live effects             = 3
shadow executions       = 0
trial budget spent       = 0.2
```

Including the v0.7 seed, the local execution ledger contains four effects and the
runtime tick reaches four. The test also verifies that each reported
`resolved_shadow_count` exactly matches the resolution packet, whether the compatible
prediction exists or remains pending.

## Formal surface

`formal/KUOS/OpenHorizon/BoundedPortfolioExperimentV0_8.lean` defines:

```lean
expectedInformationGain
eligibleTrial
ExperimentBudget
debitBudget
ExperimentSelection
ExperimentHistory
```

It proves:

- zero-weight information gain is zero;
- eligibility implies the information-gain floor;
- budget debit is monotone;
- remaining budget decreases exactly by the debit;
- live adapter count is zero or one;
- shadow actuation remains zero;
- experiment and exploit cycles increase history monotonically;
- trial history remains within its finite trial limit.

## Authority boundary

v0.8 does not grant:

- multiple simultaneous live adapters;
- unbudgeted experiments;
- experiments without exact license binding;
- experiments beyond trial count or cooldown limits;
- experiments outside risk/recoverability bounds;
- shadow execution;
- network or arbitrary shell authority;
- WORLD update authority;
- MemoryOS overwrite authority;
- truth authority to information-gain estimates;
- permanent replacement of baseline exploitation;
- permission to collapse step-incompatible predictions into false evidence.

The scheduler expands real learning while retaining singular, recoverable, finite
intervention.

## Next layer

A natural v0.9 is an Experiment Outcome and Policy Scheduler:

```text
trial utility + compatible realization error + cost + risk + recoverability
  -> experiment policy posterior
  -> context-local trial cadence
  -> exploit / experiment / reobserve recommendation
  -> one licensed live cycle
```

The next layer should learn when experimentation is useful, without learning authority
to bypass the v0.8 hard gates.
