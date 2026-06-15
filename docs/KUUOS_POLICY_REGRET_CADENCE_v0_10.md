# KuuOS Policy-Regret and Counterfactual Cadence Controller v0.10

## Purpose

v0.10 learns whether the previously chosen policy mode was locally inferior to a
credible alternative and returns that bounded regret to the next policy cadence.

```text
realized v0.9 policy outcome
  + historical mode values
  + discounted pending shadow alternatives
  + newly compatible delayed outcomes
  -> confidence-discounted bounded regret
  -> experiment / reobserve / exploit regret credits
  -> adapted v0.9 thresholds and intervals
  -> exactly one v0.9 child cycle
```

The controller is not a passive report. Its output directly changes the next v0.9
child plan. It can make experimentation or reobservation earlier when those modes have
repeatedly been missed, and can make both later when exploitation has repeatedly been
the better credible alternative.

## Upstream stack

```text
v0.1   Open-Horizon Telos Genesis
v0.2   Open-Horizon Commitment Gauge
v0.3   Active Gauge Intervention Loop
v0.4   Renewable Gauge Supervisor
v0.5   Event Source and Adapter Federation
v0.6   Adapter Capability Gauge
v0.7   Adapter Portfolio and Shadow Comparison
v0.8   Bounded Portfolio Experiment Scheduler
v0.9   Experiment Outcome and Policy Scheduler
v0.10  Policy-Regret and Counterfactual Cadence Controller
```

## Chosen value

The chosen policy mode is grounded in the actual v0.9 outcome.

```text
experiment
  -> chosen value = realized net experiment value

reobserve
  -> chosen value = realized local observe utility

exploit
  -> chosen value = realized baseline utility
```

No preview or unexecuted mode is used as the chosen value.

## Counterfactual alternatives

For each unchosen mode, v0.10 combines three evidence sources.

### 1. Historical realized value

```text
experiment -> mean realized net experiment value
reobserve  -> mean realized reobserve utility
exploit    -> mean realized exploit utility
```

Historical confidence increases with the number of actual mode executions.

### 2. Pending shadow alternatives

A pending v0.7/v0.8 shadow prediction may contribute:

```text
predicted utility × prediction confidence × pending_shadow_discount
```

The discount is mandatory. Pending evidence remains a prediction and cannot become an
outcome or capability update.

Shadow actions are mapped to policy alternatives:

```text
observe / hold / freeze -> reobserve alternative
other local actions     -> experiment alternative
```

### 3. Delayed compatible outcomes

A resolved shadow prediction contributes its actual later observed utility and original
prediction confidence. Only exact context- and step-compatible resolutions qualify.

Each resolved prediction ID is processed by v0.10 once. Step-incompatible predictions
remain pending and are not counted as delayed outcomes.

## Credibility

A mode estimate combines historical and shadow evidence through confidence-weighted
averaging. An alternative can create regret only when:

```text
alternative confidence >= minimum_counterfactual_confidence
```

The estimate retains explicit markers:

```text
counterfactual_estimate_not_truth = true
unexecuted_alternative_not_outcome = true
```

These markers separate epistemic estimation from actual execution history without
preventing the estimate from changing cadence.

## Bounded regret

For the best credible unchosen mode:

```text
positive_gap = max(
  0,
  alternative_value - chosen_value - regret_tolerance
)

bounded_regret = min(
  maximum_regret_per_cycle,
  alternative_confidence * positive_gap
)
```

Therefore regret is:

- nonnegative;
- confidence-discounted;
- tolerance-aware;
- bounded per cycle;
- zero when no credible alternative is better.

## Regret credits

The controller keeps three context-local credits:

```text
experiment_regret_credit
reobserve_regret_credit
exploit_regret_credit
```

Before adding new regret, all credits decay:

```text
credit <- regret_credit_decay × credit
```

The best missed alternative receives:

```text
credit[alternative] += regret_credit_learning_rate × bounded_regret
```

The chosen mode may receive a small subtraction, preventing stale support from
remaining indefinitely when it repeatedly loses to another credible mode.

All credits are clamped to `[0, 1]`.

## Cadence adaptation

### Pressure thresholds

Experiment threshold:

```text
base experiment threshold
  - regret_threshold_gain × experiment_regret_credit
  + exploit_resistance_gain × exploit_regret_credit
```

Reobserve threshold:

```text
base reobserve threshold
  - regret_threshold_gain × reobserve_regret_credit
  + exploit_resistance_gain × exploit_regret_credit
```

Both are clamped to explicit minimum and maximum thresholds.

Consequences:

```text
missed experiment opportunity
  -> experiment threshold decreases

missed reobserve opportunity
  -> reobserve threshold decreases

missed exploit opportunity
  -> both thresholds increase
```

### Minimum intervals

Experiment interval:

```text
base interval
  - experiment regret reduction
  + exploit regret extension
```

Reobserve interval:

```text
base interval
  - reobserve regret reduction
  + exploit regret extension
```

Each interval remains between an explicit integer minimum and maximum.

## Child execution

Every v0.10 invocation produces:

```text
kuuos_policy_regret_cadence_decision_v0_10.json
kuuos_policy_regret_cadence_child_plan_v0_10.json
kuuos_policy_regret_cadence_child_license_v0_10.json
```

The child run ID is:

```text
<regret_run_id>:policy
```

The adapted child is a complete v0.9 plan. v0.9 then performs its normal preview,
selects `experiment`, `reobserve`, or `exploit`, and executes one v0.8 child cycle.

Thus the execution chain remains:

```text
v0.10 regret cadence
  -> v0.9 policy mode
  -> v0.8 experiment or baseline
  -> v0.7 portfolio/shadow
  -> v0.6 capability gauge
  -> v0.5 adapter federation
  -> v0.4 supervisor
  -> v0.3 local intervention
  -> v0.2 gauge transport
  -> v0.1 telos
```

## What v0.10 may change

v0.10 may change only:

```text
v0.9 experiment pressure threshold
v0.9 reobserve pressure threshold
v0.9 minimum experiment interval
v0.9 minimum reobserve interval
```

It does not directly select an adapter or domain action. Those remain actual child
runtime decisions.

## Preserved execution constraints

The complete v0.9 and v0.8 validations still run after adaptation. Therefore v0.10
cannot bypass:

```text
v0.8 trial budget
per-trial cost ceiling
risk ceiling
recoverability floor
global and adapter-context trial counts
trial cooldown
exact digest-bound license
one live adapter
compatible-step-only resolution
```

An experiment-supporting regret credit can make a trial earlier, but only when v0.9
selects experiment and v0.8 finds a fully eligible candidate.

## State

Each context-local regret section stores:

```text
cycle count
positive / zero regret counts
cumulative and mean bounded regret
three mode regret credits
best-alternative counts by mode
delayed compatible evidence count
pending counterfactual evidence count
last child mode and chosen value
last best alternative and confidence
last bounded regret
last adapted thresholds and intervals
last child policy outcome digest
last child effect digest
```

The bundle also stores processed child policy outcome digests and processed delayed
resolution IDs.

## Recovery and replay

The v0.10 ledger uses pending and committed phases.

1. adapted regret decision is written;
2. exact v0.9 child plan and license are written;
3. pending ledger row binds previous v0.6-v0.10 digests;
4. one deterministic v0.9 child run executes;
5. exact child policy outcome is validated;
6. counterfactual alternatives and bounded regret are computed;
7. regret bundle, state, committed row, receipt, and audit are written.

Recovery rules:

- committed replay starts no child cycle;
- pending recovery reuses the exact adapted plan;
- v0.9 child replay prevents duplicate descendant execution;
- processed policy outcome digests prevent duplicate regret;
- processed resolution IDs prevent duplicate delayed evidence;
- v0.8 prevents duplicate trial debit;
- local adapter idempotency prevents duplicate domain effects.

## Outputs

```text
kuuos_policy_regret_cadence_bundle_v0_10.json
kuuos_policy_regret_cadence_decision_v0_10.json
kuuos_policy_regret_cadence_outcome_v0_10.json
kuuos_policy_regret_cadence_child_plan_v0_10.json
kuuos_policy_regret_cadence_child_license_v0_10.json
kuuos_policy_regret_cadence_state_v0_10.json
kuuos_policy_regret_cadence_receipt_v0_10.json
kuuos_policy_regret_cadence_ledger_v0_10.jsonl
kuuos_policy_regret_cadence_audit_v0_10.jsonl
```

All v0.1-v0.9 descendant artifacts remain available.

## Demonstrated sequence

The integration fixture begins with one v0.7 seed cycle:

```text
A live
B shadow
```

Then v0.10 executes four child policy cycles.

```text
cycle 1
  no prior regret credit
  child mode = experiment
  B performs advance_tick
  trial cost 0.2 debited once

cycle 2
  child mode = reobserve
  one local observe effect
  exploit is the best credible alternative
  positive exploit regret is recorded

cycle 3
  exploit regret raises experiment and reobserve thresholds
  exploit regret extends both minimum intervals
  child mode = exploit
  one advance_tick effect

cycle 4
  decayed exploit regret remains positive
  experiment interval remains above its base value
  child mode remains exploit
  one advance_tick effect
```

Expected totals:

```text
v0.10 cycles              = 4
v0.9 child cycles         = 4
experiment children       = 1
reobserve children        = 1
exploit children          = 2
positive regret cycles    >= 1
counterfactual outcomes   = 0
shadow executions         = 0
hard-gate bypasses        = 0
trial budget spent        = 0.2
```

Including the v0.7 seed, the local execution ledger has five rows. The observe action
does not advance the runtime tick; the four advance actions produce a final tick of
four.

## Formal surface

`formal/KUOS/OpenHorizon/PolicyRegretCadenceV0_10.lean` defines:

```lean
confidenceDiscountedRegret
adaptThresholdBounded
adaptIntervalBounded
RegretAlternative
RegretExecution
RegretHistory
```

It proves:

- bounded regret is nonnegative under nonnegative confidence and maximum;
- bounded regret never exceeds its configured maximum;
- adapted thresholds remain inside lower and upper bounds;
- adapted intervals remain inside lower and upper bounds;
- each v0.10 run invokes zero or one v0.9 child;
- each descendant cycle has zero or one live adapter;
- counterfactual outcome count remains zero;
- shadow actuation remains zero;
- hard-gate bypass count remains zero;
- regret history advances monotonically.

## Authority boundary

v0.10 grants no authority to:

- execute more than one v0.9 child per invocation;
- convert an unexecuted alternative into an outcome;
- use a low-confidence alternative to create regret;
- count the same delayed resolution twice;
- bypass v0.9 mode selection;
- bypass v0.8 eligibility or budget;
- execute shadow candidates;
- inherit source or adapter authority;
- perform arbitrary shell or network execution;
- mutate WORLD;
- overwrite MemoryOS.

The layer adds active counterfactual learning while keeping the distinction between
realized effect and estimated alternative explicit.

## Next layer

A natural v0.11 is a Delayed Credit and Multi-Horizon Policy Controller:

```text
immediate regret
  + delayed compatible outcomes
  + multi-cycle commitment progress
  + recovery cost
  -> short / medium / long horizon credits
  -> horizon-aware policy cadence
  -> one v0.9 child cycle
```

The next layer should prevent immediate utility from dominating delayed commitment
success, while retaining actual-effect grounding and finite credit assignment.
