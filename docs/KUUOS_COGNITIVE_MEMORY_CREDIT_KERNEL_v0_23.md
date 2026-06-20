# KuuOS Cognitive Memory Consolidation and Bounded Credit Assignment v0.23

## Purpose

v0.23 integrates previously established KuuOS components instead of introducing a second belief, observation, verification, planning, or memory authority.

```text
ObserveOS v0.2 observation lineage
+ VerifyOS v0.2 bounded verdict lineage
+ BeliefOS v0.1-v0.3 local and plural belief surface
+ Semantic Planner / Verifier v0.22
+ MemoryOS append-only process history
+ Qi process tensor non-Markov context
→ cognitive memory consolidation
→ bounded non-causal step credit
→ future-only BeliefOS candidate
→ future-only PlanOS strategy candidate
→ append-only MemoryOS episode
```

## Ownership

```text
observation record          = ObserveOS
verification verdict        = VerifyOS
local/plural belief surface = BeliefOS
memory lineage              = MemoryOS
non-Markov process context  = Qi process tensor
replan synthesis            = PlanOS
candidate selection         = DecisionOS
execution                   = ActOS
```

v0.23 owns only consolidation, bounded correlational credit, and candidate construction.

## ObserveOS boundary

The consolidation kernel accepts an ObserveOS lineage envelope only when:

- an observation is recorded;
- `observation_not_verification = true`;
- verification remains required;
- mission, chart, and plan lineage are compatible;
- no truth, verification, execution, or memory-overwrite authority is acquired.

The observation is evidence input. It is not itself a success verdict.

## VerifyOS boundary

The VerifyOS envelope must preserve:

- a bounded verdict;
- the source observation identity;
- the v0.22 verification receipt identity;
- `learning_required = true`;
- `learning_must_be_future_only = true`;
- `automatic_learning = false`;
- no truth, causal, execution, automatic-learning, or memory-overwrite authority.

Counterevidence from failed, contradicted, regressed, and unknown criteria is retained.

## BeliefOS use

BeliefOS remains a chart-local and plurality-preserving belief surface. v0.23 reads:

- current claim statuses;
- supporting evidence;
- opposing evidence;
- unknown evidence;
- contradiction residues;
- optional v0.3 context-gerbe coherence receipts.

It emits only a future belief-release candidate:

```text
candidate
observe
repair
hold
```

The candidate preserves locality, plurality, counterevidence, and the absence of global trivialization. It does not directly release or overwrite belief.

## Qi process tensor use

Qi supplies process-history context:

- transition continuity;
- memory continuity;
- non-Markov visibility;
- hysteresis;
- memory horizon;
- observation debt;
- recovery and transition readiness.

Qi changes temporal weighting and future strategy preference. It does not determine truth, causality, belief release, plan activation, or execution.

## Bounded credit assignment

Each semantic-plan step receives a signed credit in the closed interval:

```text
-1 <= signed_credit <= 1
```

Credit is derived from:

- the bounded verification outcome;
- criterion coverage;
- verification confidence;
- Qi-conditioned temporal distance;
- observation debt;
- memory horizon and hysteresis.

Every credit packet states:

```text
causal_claim = false
future_only = true
active_now = false
```

Therefore credit is a bounded correlational learning surface, not a causal proof or automatic policy update.

## PlanOS use

The strategy candidate route is one of:

```text
verified success + high readiness → strengthen
verified success                 → continue
partial or inconclusive          → reobserve
contradiction                    → repair
regression                       → hold
human review required            → hold
```

Every candidate requires:

```text
PlanOS synthesis
DecisionOS selection
next-cycle activation boundary
ActOS execution license
```

A v0.23 candidate is never active in the current cycle.

## MemoryOS use

The first episode is a declared MemoryOS genesis episode. Later episodes retrieve prior append-only process-tensor entries using the existing MemoryOS replay surface.

Committed entries preserve:

- plan and belief digests;
- ObserveOS and VerifyOS lineage;
- verification and credit digests;
- counterevidence;
- process-tensor and non-Markov traces;
- observation-debt and recoverability traces;
- safe-reentry and mission lineage.

The store uses:

```text
initial.json
snapshot.json
cognitive-memory-ledger.jsonl
```

It provides append-only writes, digest chaining, idempotent replay, duplicate-episode rejection, ledger reconstruction, fail-closed snapshot mismatch, and explicit snapshot repair.

## Core invariants

```text
ObserveOS observation != VerifyOS verdict
VerifyOS verdict != absolute truth
MemoryOS persistence != belief authority
Qi context != authority
credit != causal proof
learning delta != replan activation
PlanOS candidate != active plan
active plan != execution permission
memory append != memory overwrite
```

## Formal surface

Lean proves:

- signed credit remains in `[-1, 1]`;
- credit can remain explicitly non-causal;
- future-only credit is inactive now;
- memory persistence is not belief authority;
- learning delta is not replan activation;
- the combined ObserveOS, VerifyOS, BeliefOS, MemoryOS, Qi, PlanOS, non-overwrite, non-execution, and non-automatic-learning boundary.

## Validation

```bash
PYTHONPATH=. python scripts/check_cognitive_memory_credit_v0_23.py
PYTHONPATH=. python -m unittest -v tests.test_cognitive_memory_credit_v0_23
PYTHONPATH=. python scripts/check_semantic_planner_verifier_v0_22.py
PYTHONPATH=. python scripts/check_observation_belief_state_v0_21.py
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.CognitiveMemoryCreditKernelV0_23
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

## Next dependency

```text
v0.24 Transactional Tool / Connector Fabric
+ World-Effect Reconciliation
```
