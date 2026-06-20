# KuuOS Non-Markov Cognitive Loop Kernel v0.23

## Purpose

v0.23 reconnects the previously completed KuuOS cognition modules into one bounded, history-bearing loop.

```text
BeliefOS local plurality and coherence residue
→ PlanOS bounded proposal and recovery route
→ ObserveOS effect-grounded observation debt
→ VerifyOS independent falsification and verdict
→ future-only strategy delta
→ MemoryOS append-only episode
→ Qi Process Tensor history replay
→ next bounded cognition cycle
```

The v0.22 exact belief snapshot remains necessary, but it is no longer treated as sufficient. A plan now receives both:

- the exact current observation-belief state
- the non-Markov operation, observation-backaction, residue, recoverability, and memory history

No history-derived projection grants execution, truth, verification, memory overwrite, world rewrite, clinical, theorem, or final-commitment authority.

## BeliefOS integration

The kernel uses the Context Gerbe Coherence semantics rather than collapsing all evidence into a global winner.

For prerequisite claims, it computes a conservative confidence interval:

```text
coherent lower = max(0, base confidence - coherence defect)
coherent upper = min(1, base confidence + coherence defect)
```

Contradictions, unknown claims, stale claims, and retained contradiction residues increase the defect. The defect widens uncertainty; it does not veto, grant authority, globally trivialize the local charts, or declare absolute truth.

## ObserveOS integration

The process-tensor summary and recoverability projection feed the existing observation-debt scheduler.

Possible observation routes are:

```text
matched
inconclusive
divergent
conflicted
```

Expected plan observations are compared with actual observation labels. Missing temporal evidence opens observation or reobservation debt. Observation is explicitly distinct from verification and never promotes a claim directly to truth.

## VerifyOS integration

The v0.22 independent verification receipt is translated into the existing VerifyOS route semantics:

```text
verified_success                  → passed
contradicted / regression        → failed
all other verification outcomes  → indeterminate
```

Every route creates a learning debt. A passed route closes verification debt but still does not become absolute truth. A failed route preserves counterevidence and requests corrective planning. An indeterminate route preserves verification debt and requests reobservation.

## PlanOS integration

The integrated route is selected from verification, observation debt, recoverability, and suspension state:

```text
passed + expected observations present → complete_candidate
failed verification                    → replan
indeterminate or missing evidence       → reobserve
unsafe recovery or hold blocker         → suspend_revalidate
suspended renewal route                 → renew_or_escalate
suspended rerotation route              → rerotate_required
```

These are proposal and handoff routes only. They grant no ActOS execution, host access, or memory overwrite authority.

When suspension recovery is selected, the prior PlanOS rule is preserved:

- old session is closed
- old session is not resumed
- a new activation/session is required
- rerotation requires a new lineage

## MemoryOS integration

The kernel uses the existing Qi–MemoryOS append-writeback and retrieval-replay adapters.

Each episode preserves:

- mission, chart, plan, and verification lineage
- Qi process-tensor trace digest
- observation debt
- recoverability projection
- safe reentry context
- local step outcomes
- future-only strategy delta

Memory is append-only. The kernel emits a validated append receipt but does not falsely claim that durable external persistence occurred. The companion store supplies the actual local append-only ledger:

```text
initial.json
snapshot.json
nonmarkov-cognitive-loop-ledger.jsonl
```

Recovery is replay-safe. Snapshot mismatch fails closed, and repair is explicit.

## Qi Process Tensor integration

The physical quantum Qi process-tensor runtime is used as a non-authoritative multi-time structure.

The accepted packet must preserve:

- at least two ordered operations
- observation backaction
- environment and process memory
- temporal correlations
- visible tail residues
- non-Markov history dependence
- Qi as history-bearing relational flow

The current snapshot does not replace the process history. Qi remains context and flow, not truth, verification, causality, ontology, or execution authority.

## Bounded credit assignment

Local step outcomes receive bounded credit in `[-1, 1]`.

```text
succeeded    → retain_candidate
failed       → repair_or_deprioritize
unknown      → request_observation
not_observed → preserve_unresolved
```

When verification has not passed, positive step credit is capped at `0.5`. This prevents local execution success from being promoted into mission success.

The resulting strategy delta is:

- future-only
- not automatically applied
- incapable of mutating the current plan
- incapable of mutating the current belief root
- incapable of overwriting memory
- candidate weighting, not truth

## Formal boundary

The Lean module imports and composes completed theorems from:

- `BeliefOS.ContextGerbeCoherenceV0_3`
- `ObserveOS.ReplanLineageObservationEnvelopeV0_2`
- `VerifyOS.ReplanLineageVerificationEnvelopeV0_2`
- `PlanOS.SuspensionRecoveryRouterV0_17`
- `OpenHorizon.SemanticPlannerVerifierKernelV0_22`

The final theorem `nonmarkov_cognitive_loop_boundary` jointly preserves:

- BeliefOS plurality and no global winner
- observation ≠ verification
- verification ≠ truth
- future-only, non-automatic learning
- proposal-only planning
- append-only process memory
- history not replaced by snapshot
- Qi context without authority
- suspension recovery without execution, host, or overwrite authority

## Validation

```bash
PYTHONPATH=. python scripts/check_nonmarkov_cognitive_loop_v0_23.py
PYTHONPATH=. python -m unittest -v tests.test_nonmarkov_cognitive_loop_v0_23
PYTHONPATH=. python scripts/check_semantic_planner_verifier_v0_22.py
PYTHONPATH=. python scripts/check_observation_belief_state_v0_21.py
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.NonMarkovCognitiveLoopKernelV0_23
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
