# CodeAI Environment Capsule and Livelock-Efficiency Gate v0.1

## Purpose

This additive stage consumes the exact **Trajectory-Grounded Specialist Router Admission v0.1** manifest, a sealed environment capsule, and an observable state-transition trace. It emits one of two read-only dispositions:

- `progress_efficiency_admitted`: the capsule is exact and reproducible, the measured trajectory is cycle-free, and all progress/resource budgets are satisfied;
- `progress_efficiency_held`: the input is structurally valid, but reproducibility, livelock, progress, or efficiency requirements are not satisfied.

Malformed, tampered, stale, or version-mismatched inputs are blocked before a disposition is produced.

The output is a continuation hint only. It does not continue execution, invoke the selected specialist, mutate a repository, grant Git authority, or claim correctness.

## Research basis

The design specializes current 2026 primary work without inheriting stronger empirical claims:

1. **Process-Level Trajectory Evaluation for Environment Configuration in Software Engineering Agents** (ICLR 2026, OpenReview `Q8qgloDKUO`) separates setup planning, perception-driven diagnosis, feedback-driven repair, and final execution instead of relying only on terminal build/test success.
2. **MEnvAgent: Scalable Polyglot Environment Construction for Verifiable Software Engineering** (ICML 2026 spotlight, OpenReview `Mkal0hTCnh`) uses planning, execution, and verification for environment construction and demonstrates that environment handling is both a correctness and cost bottleneck.
3. **ResearchEnvBench: Benchmarking Agents on Environment Synthesis for Research Code Execution** (arXiv:2603.06739) identifies incomplete dependency resolution and brittle version coupling as dominant environment-synthesis failure modes.
4. **TraceFix: Repairing Agent Coordination Protocols with TLA+ Counterexamples** (arXiv:2605.07935) motivates explicit deadlock/livelock predicates and runtime monitoring rather than prompt-only assurances.
5. **Reducing Belief Deviation in Reinforcement Learning for Active Reasoning of LLM Agents** (ICLR 2026 oral, OpenReview `r8hzDA3pUY`) links state drift to repetitive, uninformative actions and supports truncating unproductive tails.
6. **ToolGate: Token-Efficient Pre-Call Control for Tool-Augmented Vision-Language Agents** (arXiv:2606.03054) motivates a distinct pre-call cost gate rather than executing every proposed tool action.
7. **Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents** (arXiv:2606.10209) motivates explicit token/runtime accounting and protection against stale-state accumulation.

KuuOS tightens these ideas into a deterministic contract: an environment is reusable only under exact bindings, and continuation is held whenever a measured cycle, repeated zero-progress transition, excessive no-progress streak, or resource-budget violation is present.

## Exact lineage and bindings

The request, policy, environment capsule, and progress trace bind:

- repository full name and exact source commit;
- source-tree digest;
- predecessor router-manifest, admission-pack, and receipt digests;
- selected specialist identity, kind, and active subtask;
- dependency slice and toolchain digests;
- environment, progress, and gate-policy contract digests.

The predecessor router manifest is independently canonicalized and must confirm:

- `specialist_route_admitted`;
- measurement-grounded routing;
- route-hint-only status;
- no specialist dispatch, candidate selection, execution authority, repository mutation, Git authority, or correctness claim.

Any mismatch blocks the gate.

## Environment capsule

The sealed capsule records:

- runner-image and operating-system digests;
- architecture;
- Python and Lean toolchains;
- dependency-manifest digest;
- workflow-definition digest;
- environment-variable digest;
- locale and timezone;
- network policy;
- immutable-root, dependency-lock, completeness, observation, and self-report status.

A valid but mutable, incomplete, unobserved, self-reported, network-enabled, or unlocked capsule produces a hold.

## State-transition progress trace

Every checkpoint records:

- consecutive step index and phase;
- before-state, action, observation, after-state, and observable-artifact digests;
- progress units;
- tool and model calls;
- input/output token units;
- wall-clock time;
- failed-action status.

The runtime derives all gate metrics from checkpoints rather than accepting self-reported aggregates.

## Livelock predicates

The gate derives:

- cycle count: a zero-progress transition returns to an already observed state;
- repeated zero-progress transitions: repeated `(state before, action, state after)` triples with no progress;
- maximum consecutive no-progress streak.

Continuation is held when any metric exceeds policy. A single terminal success claim cannot override process-level livelock evidence.

## Efficiency predicates

The gate enforces upper bounds for:

- steps;
- tool calls;
- model calls;
- token units;
- wall-clock time;
- failed actions.

It also enforces lower bounds for:

- total progress units;
- distinct observed states.

Efficiency is not success probability. It is a measured budget predicate over the sealed trace.

## Reference specialization

The reference source is PR #1332's merge commit:

- source commit: `8d4950e8a9cf197684ef70b86dd35682153449c1`;
- predecessor route: `specialist-formal-001` / `formal` / `verify`;
- predecessor admission pack: `fbd525e9fd5f68df0a52f540bdc97ffee1d728377947d77f76ea6b467ded2baa`;
- predecessor receipt: `1feee3b7102eb9b45b5b068337950f426de9217482918b7cdfdbb0c0be39298a`.

Measured reference trace:

- 6 steps;
- 9 tool calls;
- 6 model calls;
- 46,000 token units;
- 1,380,000 ms wall-clock time;
- 0 failed actions;
- 20 progress units;
- 7 distinct states;
- 0 cycles;
- 0 repeated zero-progress transitions;
- 0 maximum no-progress streak.

All capsule and budget predicates pass, producing `progress_efficiency_admitted` as a continuation hint only.

## Formal kernel

The Lean kernel defines:

- `SubtaskKind` and `SpecialistKind`;
- exact `Binding`;
- `EnvironmentCapsule`;
- `ProgressMetrics`;
- `Budget`;
- `GateEvidence`;
- `CapsuleReproducible`;
- `TraceGrounded`;
- `LivelockFree`;
- `Efficient`;
- `BoundaryPreserved`;
- `GateAdmitted`.

Generic theorems extract exact environment binding, grounded trace, livelock freedom, budget compliance, and boundary preservation. Separate theorems prove that repository-version mismatch, a detected cycle, repeated zero-progress excess, step-budget excess, and self-report-only traces forbid admission.

The actual specialization proves the reference evidence is admitted, while cycle, over-budget, and self-report variants are not.

## Fixed boundaries

```text
environment capsule != permission to reuse across versions
capsule equality != behavioral equivalence proof
continuation hint != continuation authority
livelock-free measurement != task completion proof
efficiency budget pass != correctness proof
progress units != probability of success
router admission != specialist dispatch
gate receipt != repository mutation authority
gate receipt != Git authority
self report != observable evidence
```
