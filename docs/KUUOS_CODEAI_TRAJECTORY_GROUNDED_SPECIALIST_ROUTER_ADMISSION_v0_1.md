# CodeAI Trajectory-Grounded Specialist Router Admission v0.1

## Purpose

This additive stage consumes the exact **Subtask-Level Version-Bound Memory v0.1** pack and a bounded partial software-engineering trajectory, then emits one of two read-only dispositions:

- `specialist_route_admitted`: one specialist route hint has sufficient measurement-grounded evidence and a policy-defined utility margin;
- `specialist_route_held`: no specialist is admissible or the leading candidates are too close.

Admission is not dispatch. The stage does not invoke a specialist, select or reject a patch, execute tools, mutate a repository, grant execution or Git authority, or claim correctness.

## Research basis

The design specializes five 2026 results without inheriting their stronger empirical claims:

1. **SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks** (arXiv:2607.00053) shows why routing from a partial trajectory can be strictly more informative than routing from the initial issue text alone.
2. **BOAD: Discovering Hierarchical Software Engineering Agents via Bandit Optimization** (ICLR 2026, OpenReview `O6stE173BD`) supports decomposition into specialized agents rather than one monolithic reasoning chain.
3. **Agentic Rubrics as Contextual Verifiers for SWE Agents** (ICLR 2026 AIWILD, OpenReview `edYwO6bEJD`) motivates repository-context-grounded criteria rather than generic or self-reported confidence.
4. **Process-Level Trajectory Evaluation for Environment Configuration in Software Engineering Agents** (ICLR 2026, OpenReview `Q8qgloDKUO`) motivates fine-grained process measurements in addition to terminal success.
5. **Safety Testing LLM Agents at Scale: From Risk Discovery to Evidence-Grounded Verification** (arXiv:2607.01793) motivates deterministic predicates grounded in observable artifacts and tool evidence rather than model self-report.

KuuOS makes the routing contract stricter: partial trajectory evidence is necessary but never sufficient without exact repository, memory-pack, dependency, toolchain, environment, subtask, and policy bindings.

## Exact bindings

The request, policy, trajectory, and each specialist evidence packet bind:

- repository full name and exact source commit;
- source-tree digest;
- predecessor memory-pack and memory-receipt digests;
- active subtask and subtask-contract digest;
- predecessor-output and dependency-slice digests;
- toolchain and environment digests;
- trajectory-contract and routing-policy digests.

A mismatch blocks the request or excludes the affected specialist.

## Measurement-grounded admission

A trajectory must satisfy all configured minimums:

- exploratory turns;
- repository observations;
- execution-derived signals;
- distinct grounding sources;
- observable artifact digests.

It must also be complete, include observed repository and test state, and not be self-report-only.

Each specialist evidence packet must:

- be bound to the exact request and trajectory digest;
- support the active subtask;
- use independent measurement;
- satisfy fit, reliability, age, and cost limits;
- preserve the no-effect/no-authority boundary.

Among eligible specialists, the leading utility score must exceed the runner-up by the policy margin. Otherwise the stage holds.

## Reference specialization

The reference query is the `verify` subtask at PR #1331's merge state.

- predecessor memory pack: `9826f4a6024cdad797c1acff2ead6156c93393f61f20a6f1bb7455f1c265c097`
- predecessor memory receipt: `8c566cfb36967262d50b0879b01df042e371e2196a5e0f34cc50a3c6e775b969`
- exploration turns: `4`
- observations: `7`
- execution signals: `2`
- grounding sources: `3`
- observable artifacts: `4`
- eligible specialists: `4`
- selected route hint: `specialist-formal-001`
- selected utility: `154`
- runner-up utility: `148`
- required margin: `5`

The selected route therefore has a margin of `6` and is admitted as a route hint only.

## Formal kernel

The Lean kernel defines:

- `SubtaskKind`;
- `SpecialistKind`;
- exact `Binding`;
- `Measurement`;
- `SpecialistEvidence`;
- `BoundaryPreserved`;
- `MeasurementGrounded`;
- `Utility`;
- `AdmissibleCandidate`;
- `Dominates`;
- `RouteAdmitted`.

Generic theorems extract exact binding, measurement grounding, non-self-report status, and boundary preservation from an admitted route. Separate theorems prove that repository-version mismatch, self-report-only measurement, and incomplete measurement forbid candidate admission.

The actual specialization proves that the formal specialist dominates the behavioral, adversarial, and maintainability alternatives at the configured margin, while a self-report-only variant is inadmissible.

## Fixed boundaries

```text
route admission != specialist dispatch
route hint != patch selection
route hint != patch rejection
partial trajectory != correctness proof
utility score != probability of success
memory usefulness != future success proof
measurement packet != execution authority
admission receipt != repository mutation authority
admission receipt != Git authority
self report != observable evidence
```
