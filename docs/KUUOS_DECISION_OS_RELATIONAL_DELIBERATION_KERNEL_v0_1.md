# KuuOS DecisionOS Relational Deliberation Kernel v0.1

DecisionOS v0.1 converts a mission-bound BeliefOS basis into an auditable decision candidate without collapsing belief into truth, comparison into a universal ranking, or decision into execution.

```text
v0.20 Persistent Mission Contract
        +
BeliefOS v0.3 Context-Gerbe Coherence
        +
optional v0.8-v0.12 policy / regret / horizon advisory receipts
        ↓
DecisionOS v0.1 relational deliberation
        ↓
SELECT_CANDIDATE / OBSERVE / EXPERIMENT_RECOMMENDED
/ HOLD / REPAIR / ESCALATE / REJECT / QUARANTINE
        ↓
future-only decision basis
        ↓
v0.21 Replan
        ↓
Plan
```

DecisionOS is not an actuator. A selected candidate is not an applied action, host license, clinical order, institutional approval, or truth certificate.

## 1. Fivefold foundation

### Emptiness

No option, score, preference, route, or selected candidate possesses self-grounded authority.

```text
decision != truth
decision != action
decision != license
score != value-in-itself
winner != universal winner
```

### Dependent Origination

A decision exists only relative to:

- mission contract and current mission-state digests;
- BeliefOS receipt and its uncertainty/counterevidence;
- declared decision context;
- option set;
- hard constraints;
- stakeholders;
- time horizons;
- reversible and irreversible consequences;
- available authority and required external licenses;
- counterfactual and regret evidence;
- Qi process history.

### Two Truths

At the conventional level, DecisionOS may produce an operationally usable decision basis. At the ultimate level, the result remains non-reified, revisable, context-local, and non-sovereign.

### Middle Way

The kernel avoids both:

- premature collapse: selecting one option when uncertainty or conflict remains material;
- nihilistic erasure: refusing all responsible choice merely because certainty is unavailable.

### Qi process tensor

Qi is used only as non-Markov process context for timing, recovery trajectory, reversibility, transition continuity, and stakeholder resonance. It cannot become truth authority, moral veto, clinical order, execution license, or universal priority.

## 2. Strict deliberation cycle

```text
FRAME
  ↓
GENERATE
  ↓
CONSTRAIN
  ↓
EVALUATE
  ↓
CHALLENGE
  ↓
QI_CONDITION
  ↓
TWO_TRUTHS_CHECK
  ↓
MIDDLE_WAY_GATE
  ↓
DECIDE
  ↓
COMMIT
```

Only this order is permitted. Phase skipping, event-index regression, stale state digests, time regression, and replay mutation are rejected.

## 3. Authority sources

### Mission authority

The v0.20 Mission Contract remains the source of purpose, prohibitions, scope, budget, reserve, and authority boundaries. DecisionOS stores exact digests and does not reinterpret or enlarge them.

### Epistemic authority

BeliefOS supplies a conditional belief basis with uncertainty, counterevidence, context transport, path dependence, and coherence defects. DecisionOS may use the basis but may not promote it to truth.

### Advisory policy evidence

Existing v0.8-v0.12 components may contribute bounded advisory receipts:

- experiment eligibility and information gain;
- experiment / reobserve / exploit posterior;
- bounded policy regret;
- short / medium / long horizon credits;
- horizon-gauge arbitration.

These receipts remain advisory. They cannot bypass Mission Contract constraints, DecisionOS hard gates, Replan, or host-license execution boundaries.

## 4. Option representation

Every option declares:

```text
option_id
option_digest
action_class
requires_external_license
requires_human_review
mission_allowed
prohibited
estimated_cost
estimated_risk
recoverability
reversibility
positive value intervals
negative value intervals
supporting / opposing evidence digests
stakeholder digests
```

The initial action classes are:

```text
observe
experiment
exploit
repair
hold
escalate
local_action
```

They are semantic candidates only. DecisionOS does not execute them.

## 5. Hard constraint gate

An option is admissible only when all required gates hold:

```text
mission_allowed = true
prohibited = false
estimated_cost <= decision_budget
estimated_risk <= maximum_risk
recoverability >= minimum_recoverability
reversibility >= minimum_reversibility
required evidence is present
option does not claim new authority
```

An external license may still be required after selection. DecisionOS never fabricates it.

## 6. Interval-valued evaluation

Positive dimensions include:

```text
mission_alignment
expected_benefit
information_gain
recoverability
reversibility
stakeholder_fit
qi_process_compatibility
```

Negative dimensions include:

```text
expected_harm
cost_burden
delay_risk
uncertainty_burden
```

Each dimension is an interval `[l,u]` in `[0,1]`. With nonnegative normalized weights, the conservative value interval is:

```text
value_lower
  = sum positive_weight * positive_lower
    - sum negative_weight * negative_upper

value_upper
  = sum positive_weight * positive_upper
    - sum negative_weight * negative_lower
```

The kernel preserves the interval. It does not replace it with a mandatory point estimate.

## 7. Partial order and robust dominance

Option `a` robustly dominates option `b` only when:

```text
value_lower(a) > value_upper(b) + dominance_margin
```

A `SELECT_CANDIDATE` route requires one admissible option to robustly dominate every other admissible option. Ties and overlapping intervals do not produce a hidden scalar winner.

The receipt preserves:

- the complete admissible set;
- excluded options and reasons;
- the robust-dominance relation;
- retained alternatives;
- worst-case regret bounds;
- all option intervals.

## 8. Counterfactual challenge

Before deciding, the kernel records:

```text
counterargument digests
missing-evidence digests
stakeholder objections
alternative option IDs
catastrophic-risk marker
unresolved normative-conflict marker
counterfactual receipt digests
```

An unexecuted alternative remains an estimate, not an outcome. Policy-regret evidence may alter deliberation but cannot become truth.

## 9. Decision routes

### SELECT_CANDIDATE

One option robustly dominates all other admissible options, hard constraints pass, challenge does not require escalation, and the Middle Way gate allows commitment.

### OBSERVE

Material uncertainty prevents robust selection and further observation is the responsible next basis.

### EXPERIMENT_RECOMMENDED

No option robustly dominates, but a bounded, recoverable, sufficiently informative experiment option exists. This is a recommendation to Replan, not a live-trial license.

### HOLD

Plurality remains unresolved and neither observation nor bounded experiment currently justifies progression.

### REPAIR

The option field, evidence basis, or deliberation surface is repairable but not ready for selection.

### ESCALATE

Human, clinical, institutional, legal, or other higher authority is required. DecisionOS does not impersonate that authority.

### REJECT

No admissible option remains under the mission-bound hard constraints.

### QUARANTINE

Digest failure, authority escalation, source inconsistency, or structural corruption is detected.

## 10. Middle Way gate

The gate stores bounded risks for:

```text
reification
nihilistic erasure
premature closure
responsibility abandonment
stakeholder exclusion
irreversibility
```

Selection is blocked when reification, premature closure, stakeholder exclusion, or irreversibility risk exceeds the configured gate. Deferral is redirected toward REPAIR or ESCALATE when nihilistic erasure or responsibility abandonment becomes excessive.

## 11. Commit semantics

A DecisionOS commit stores:

```text
decision route
selected option, when present
recommended option IDs
retained alternatives
decision basis digest
mission and belief source digests
constraint and evaluation artifacts
counterfactual challenge
Qi condition
Two Truths receipt
Middle Way receipt
append-only event history
predecessor and current state digests
```

Commit requires:

```text
future_only = true
memory_overwrite = false
decision_not_execution = true
activation_boundary = mission_replan_only
```

## 12. Persistent store

```text
decision-genesis.json
decision-ledger.jsonl
decision-snapshot.json
.decision-os.lock
```

The ledger is the append-only authority. The snapshot is a derived cache. The store provides:

- exclusive writer lock;
- digest-chained commits;
- fsync before snapshot replacement;
- atomic snapshot update;
- replay idempotence;
- stale-state and time-regression rejection;
- malformed-ledger and broken-chain rejection;
- explicit ledger-derived snapshot repair.

## 13. v0.21 Replan bridge

A committed decision basis is not active until v0.21 Replan binds it into the next Plan.

```text
DecisionOS COMMIT
        ↓
pending_replan_activation
        ↓
v0.21 Replan receipt
        ↓
next_plan_basis_digest
        ↓
Plan
```

The activation receipt still grants no execution authority. Actual effects remain downstream of v0.17+ host-license and invocation paths.

## 14. Formal surface

The Lean surface proves:

- typed strict phase order;
- event-index increase;
- conservative interval ordering;
- robust dominance implies strict interval separation;
- a selection certificate dominates every retained alternative;
- option plurality is retained before valid selection;
- Qi conditioning grants no authority;
- Two Truths separation and non-reification;
- Middle Way forbids both premature collapse and nihilistic erasure;
- decision commit is future-only and non-overwriting;
- decision does not grant truth or execution authority;
- Replan is required before activation;
- append-only recovery count matches committed decision count.

## 15. Public boundary

DecisionOS v0.1 is a structural and proof-facing deliberation kernel. It is not medical advice, treatment authorization, legal authority, institutional approval, theorem authority, host license, or unrestricted autonomous execution authority.
