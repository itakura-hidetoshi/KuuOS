# KuuOS Delayed Credit and Multi-Horizon Policy Controller v0.11

## Purpose

v0.11 prevents immediate utility from dominating policy learning. It separates actual outcomes into short-, medium-, and long-horizon credits, adapts the base cadence supplied to v0.10, and executes exactly one v0.10 child.

```text
actual effect
  + v0.10 bounded regret
  + commitment progress
  + delayed compatible evidence
  + recovery cost
  + gauge terminal / curvature / holonomy state
  -> short / medium / long mode credits
  -> horizon-weighted cadence base
  -> one v0.10 child cycle
```

## Distinct horizons

Each context keeps independent credits for `experiment`, `reobserve`, and `exploit`.

### Short horizon

Short credit learns and decays rapidly. It receives realized chosen-mode value and current bounded regret assigned to a credible missed alternative.

### Medium horizon

Medium credit receives effect-grounded commitment progress, recovery cost as reobserve support, and newly compatible delayed evidence.

### Long horizon

Long credit activates only after a configured cycle count. It receives holonomy-weighted progress, terminal-section ratio as exploit support, persistent recovery cost as reobserve support, and delayed compatible evidence. It decays more slowly than short credit.

## Actual-effect grounding

Credit update requires the exact v0.3 effect receipt:

```text
progress_delta
observed_benefit
observed_harm
recoverability
confidence
continuation_signal
```

A preview, pending shadow, or unexecuted counterfactual cannot update horizon credit by itself.

## Commitment progress

```text
progress = clamp(
    progress_delta_weight    * progress_delta
  + observed_benefit_weight  * observed_benefit
  + terminal_ratio_weight    * terminal_section_ratio
  + effect_confidence_weight * effect_confidence
)
```

## Recovery cost

```text
recovery_cost = clamp(
    observed_harm_weight          * observed_harm
  + recoverability_deficit_weight * (1 - recoverability)
  + curvature_cost_weight         * mean_curvature_norm
  + repair_continuation_cost      when continuation is repair or reobserve
)
```

Recovery cost is not an automatic stop. It creates medium- and long-horizon reobserve credit.

## Gauge evidence

v0.11 reads the v0.2 commitment-gauge bundle:

```text
local section state
curvature norm
terminal-section ratio
holonomy depth
```

Terminal states are `flat_complete`, `handed_over`, and `superseded`. No global graph or dependency DAG is constructed.

## Credit update and aggregation

```text
credit[horizon, mode] <- clamp(
  decay[horizon] * credit[horizon, mode] + learning * evidence
)
```

For each mode:

```text
support(mode) = clamp(
    short_weight  * short_credit(mode)
  + medium_weight * medium_credit(mode)
  + long_weight   * long_credit(mode)
)
```

The three horizon values remain separately auditable after aggregation.

## Active cadence adaptation

```text
experiment base threshold
  = base - gain * experiment_support + resistance * exploit_support

reobserve base threshold
  = base - gain * reobserve_support + resistance * exploit_support
```

Base intervals are shortened by experiment/reobserve support and extended by exploit support. Thresholds and intervals remain within explicit lower and upper bounds.

The adapted values are written into a complete v0.10 child plan. v0.10 still performs regret adaptation, v0.9 still selects the policy mode, and v0.8 still checks all execution hard gates.

## Child chain

```text
v0.11 horizon credit
  -> v0.10 regret cadence
  -> v0.9 policy selection
  -> v0.8 trial / baseline
  -> v0.7 portfolio / shadow
  -> v0.6 capability gauge
  -> v0.5 federation
  -> v0.4 supervisor
  -> v0.3 local effect
  -> v0.2 commitment curvature update
```

Child run ID is `<horizon_run_id>:regret`.

## Recovery and replay

Before execution, v0.11 persists the horizon decision, exact v0.10 child plan/license, and pending ledger row. After execution it validates the exact v0.10 regret outcome, effect receipt, and updated gauge bundle before committing credit.

- committed replay starts no child cycle;
- pending recovery reuses exact child packets;
- processed regret-outcome digests prevent duplicate credit;
- processed effect digests prevent duplicate attribution;
- descendant replay prevents duplicate trial debit and local effects.

## Demonstrated sequence

```text
cycle 1: experiment
  short and medium experiment credit created
  long horizon inactive

cycle 2: reobserve
  prior experiment support lowers the v0.10 experiment base threshold
  medium and long reobserve credit created

cycle 3: exploit
  long exploit credit created

cycle 4: exploit
  short, medium, and long credits remain distinct
```

Expected invariants:

```text
v0.11 cycles = 4
v0.10 children = 4
experiment / reobserve / exploit = 1 / 1 / 2
live trials = 1
trial spend = 0.2
effectless credit updates = 0
multiple child cycles = 0
hard-gate bypasses = 0
```

## Outputs

The layer writes bundle, decision, outcome, exact child plan/license, state, receipt, append-only ledger, and audit files under the v0.11 names.

## Formal surface

`formal/KUOS/OpenHorizon/DelayedCreditMultiHorizonV0_11.lean` proves bounded credits and aggregate support, bounded threshold and interval adaptation, one v0.10 child, one descendant live adapter, and zero effectless updates, shadow actuation, and hard-gate bypass.

## Authority boundary

v0.11 grants no effectless credit update, counterfactual-to-outcome promotion, multiple child execution, v0.10/v0.9/v0.8 bypass, shadow execution, source or adapter authority inheritance, WORLD mutation, MemoryOS overwrite, or arbitrary shell/network authority.

## Next layer

v0.12 should be a Horizon Arbitration and Commitment Outcome Controller. It will handle genuine conflict among short, medium, and long horizons through bounded plural arbitration without collapsing them prematurely into one truth value.
