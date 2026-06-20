# KuuOS OS–Qi Closed-Loop Integration v0.24

## Purpose

v0.24 connects the existing cognition and execution-facing OS modules without collapsing their ownership boundaries.

```text
ObserveOS
→ BeliefOS
→ MemoryOS v0.23
→ Qi Process Tensor
→ DecisionOS candidate selection
→ PlanOS synthesis / replan
→ VerifyOS
→ next-cycle context
```

The integration consumes the v0.22 semantic plan and independent verification receipts together with the v0.23 cognitive-memory consolidation receipt.

## Ownership

- ObserveOS records effect-grounded observations.
- BeliefOS owns local and plural belief release.
- MemoryOS owns append-only episodic and strategy-memory candidates.
- Qi Process Tensor supplies bounded non-Markov process context.
- DecisionOS selects among candidates.
- PlanOS synthesizes or repairs plans.
- VerifyOS independently verifies outcomes.
- ActOS alone owns licensed execution.

## Main improvement

Before v0.24, the individual components existed but the top-level cognition route did not explicitly bind their outputs into one typed next-cycle packet. v0.24 adds that binding while preserving all non-authority constraints.

The integrated receipt contains:

- exact plan, verification, observation-envelope and verification-envelope digests
- v0.23 belief, plan and memory candidates
- bounded credit-assignment references
- counterevidence references
- Qi process-tensor visibility and non-Markov memory visibility
- a DecisionOS candidate set that is not yet selected
- a PlanOS synthesis request that is not yet activated
- a future-only next-cycle context

## Qi Process Tensor role

Qi Process Tensor conditions the next cycle using:

- transition continuity
- memory continuity
- hysteresis
- memory horizon
- observation debt
- recovery / recoverability traces
- non-Markov process history

It is not treated as truth probability, causal authority, plan activation authority, or execution permission.

## Safety boundaries

```text
observation != verification
verification != absolute truth
memory append != memory overwrite
credit assignment != causal proof
learning delta != replan activation
plan synthesis != execution permission
execution success != mission success
```

The integration never selects a candidate, activates a plan, mutates a past cycle, overwrites memory, or executes an effect.

## Status routes

```text
consolidated             → decision_candidate_ready
reobserve_required       → reobserve_required
contradiction_preserved  → contradiction_preserved
human_review_required    → human_review_required
blocked                  → blocked
```

Contradiction and counterevidence are carried forward instead of being silently resolved.

## Validation

```bash
PYTHONPATH=. python scripts/check_os_qi_closed_loop_v0_24.py
PYTHONPATH=. python -m unittest -v tests.test_os_qi_closed_loop_v0_24
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.OSQiClosedLoopIntegrationV0_24
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
