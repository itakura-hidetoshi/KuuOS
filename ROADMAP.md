# KuuOS / 空OS Roadmap

This roadmap describes the current public direction of `itakura-hidetoshi/KuuOS` as of June 16, 2026.

KuuOS is an append-only, governance-gated, validation-backed, proof-facing, memory-aware, Qi-process-aware, **gauge-theoretic**, and bounded executable runtime architecture for relational AI systems.

The roadmap is organized around two simultaneous movements:

1. **Public repository maturity** — keep governance, validation, runtime, Qi, memory, proof-facing, GitHub/CI, gauge-control, and boundary surfaces understandable and reproducible.
2. **Controlled KuuOS baseline projection** — project the broader KuuOS baseline into public artifacts without collapsing local section, chart, validation, runtime, proof, medical, institutional, memory, GitHub, or execution authority.

The current architectural direction is explicitly gauge-theoretic:

```text
context = local chart
policy state = local section
compatible context relation = chart overlap
context change = transition function
section movement = parallel transport
disagreement = curvature / cocycle defect
path-dependent retained history = holonomy
```

KuuOS does not use a global context graph, universal context winner, central node, or shortest-path policy as its governing model.

---

## 0. Non-Authority and Non-Collapse Boundary

This roadmap does not open unrestricted autonomous authority.

The following remain closed unless a later, explicitly versioned and reviewed release opens them:

```text
unrestricted autonomous execution authority
arbitrary shell execution authority
arbitrary network execution authority
global-context-graph authority
shortest-path-as-policy authority
local-section-as-global-truth
chart-overlap-as-permanent-edge
curvature-as-veto
cocycle-defect-as-prohibition
holonomy-as-sovereign-memory
standalone diagnosis authority
standalone treatment authorization
medical act authorization
institutional authority
final theorem authority
unreviewed AGI deployment authority
Qi-based intervention authority
CI-pass-as-truth
validator-pass-as-truth
runtime-tick-as-execution-authority
allowlisted-action-as-arbitrary-execution-authority
finite-sequence-runner-as-unbounded-agent
GitHub Actions live adapter as repository authority
GPT-summary-as-proof
world-model-prediction-as-fact
memory-persistence-as-belief-sovereignty
plan-success-as-execution-permission
reflection-summary-as-root-rewrite
audit-trigger-as-infinite-escalation
```

This boundary is medical-modality neutral. It does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid.

All phases preserve:

```text
append-only lineage
additive projection
same-root required for protected surfaces
overwrite forbidden
fail-closed validation behavior
non-authority preservation
local-chart preservation
plurality floor preservation
residue visibility
provenance preservation
bounded runtime operation
allowlist discipline
validator tier separation
audit proportionality
harmony and visible cost
```

`tighten-only` remains a local, bounded, contextual tool rather than an automatic root principle or grave-escalation rule.

---

## 1. Current Public Baseline

### 1.1 Public Core Governance v0.1

Status: **active public baseline**

Core surfaces:

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md
CITATION.cff
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/KUOS_FOURFOLD_CORE_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
```

Validation:

```bash
make core-governance-checks
make all-governance-checks
```

Purpose:

```text
Expose the public core.
Define non-authority and non-collapse.
Make validation reproducible.
Give reviewers a stable entry path.
```

### 1.2 Emptiness / Dependent Origination / Two Truths Runtime Audit Chain

Status: **active public audit-chain surface**

```text
runtime structural consistency != theorem authority
hash-chain continuity != truth
two-truths barrier must not reify ultimate truth
audit must not silently become infinite escalation
```

Validation:

```bash
make emptiness-two-truths-runtime-audit-checks
make emptiness-superposition-noncollapse-checks
```

### 1.3 Qi / IndraNet / Physical Quantum Qi

Status: **active bridge, process-tensor, motion, and gauge-flow surface**

```text
Qi is a relational field, not a substance.
Qi is not denied by the medical boundary.
East Asian medical reasoning is not denied by the medical boundary.
Biomedicine is not privileged by the wording.
IndraNet is a higher gauge / holonomy field, not a flat graph.
Process, memory, transport, recoverability, and order sensitivity remain first-class.
Qi motion remains evidence-bound and scope-bound.
```

Validation:

```bash
make qi-motion-chain-checks
make physical-quantum-qi-runtime-checks
make physical-quantum-qi-dynamics-checks
make physical-quantum-qi-motion-pipeline-checks
make physical-quantum-qi-deepening-checks
```

### 1.4 KuuOS Bounded Runtime

Status: **active bounded non-authoritative runtime surface**

```text
Runtime is bounded.
Runtime is receipt-producing.
Runtime may advance declared State IO ticks.
Runtime may execute allowlisted bounded actions.
Runtime does not open arbitrary shell, network, truth, theorem, clinical,
memory-overwrite, repository, or final-commitment authority.
```

Validation:

```bash
python3 scripts/run_kuuos_runtime_full_check_v0_1.py
```

### 1.5 Qi Process Tensor / Trend / Reliability Surface

Status: **active runtime maturity surface**

```text
cycle supervisor receipts + audit history + trajectory packet
  -> cycle trend summary
  -> trend class
  -> recommendation
  -> reliability score
  -> bounded supervisor packet/run
```

The process tensor guides posture without becoming truth or action authority.

### 1.6 Allowlisted Executable Action Surface

Status: **active bounded executable surface**

```text
executable action packet
  -> allowlisted dispatcher
  -> exactly one declared action

finite sequence packet
  -> finite sequence runner
  -> completion or first blocked action
```

Validation:

```bash
python scripts/check_qi_executable_action_dispatcher_v4_2.py
python scripts/check_qi_executable_action_sequence_runner_v4_3.py
```

### 1.7 GitHub Actions / PR Adapter Surface

Status: **active bounded repository-operation surface**

```text
query packet
  -> connector request
  -> connector result
  -> result adapter
  -> workflow / PR snapshot
  -> bounded policy preparation
  -> receipt + audit
```

The adapter does not acquire merge, rerun, mutation, or repository authority by itself.

### 1.8 MemoryOS / Non-Markovian Memory Baseline

Status: **active internal baseline; controlled public projection continues**

```text
Memory is append-only lineage and reconstructive support.
Memory is not belief authority.
Memory is not root overwrite authority.
Memory preserves trace, scar, holonomy, relapse lineage, process continuity,
collective reconstruction, and uncertainty visibility.
```

### 1.9 MGAP4D / Formal Verification / Lean Bridge

Status: **active proof-facing bridge surface**

```text
KuuOS references canonical proof-facing repositories and formal surfaces.
CI pass does not equal mathematical acceptance.
Formal stub does not equal completed theorem.
Lean file does not equal external theorem acceptance.
mathlib alignment is proof support, not final authority.
GPT summary does not equal proof.
```

Canonical proof-facing repository:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

### 1.10 Horizon Gauge Arbitration v0.12

Status: **implemented, validated, merged public baseline**

Purpose:

```text
Preserve short-, medium-, and long-horizon policy sections.
Measure their pairwise connection residuals.
Construct bounded arbitration curvature.
Perform active plurality-preserving parallel transport.
Start exactly one v0.11 child cycle.
Classify the realized commitment outcome.
Append replay-safe arbitration holonomy.
```

Current demonstrated sequence:

```text
experiment -> reobserve -> exploit -> exploit
```

Current invariants:

```text
weight sum = 1
all horizon weights >= plurality floor
one v0.11 child per v0.12 invocation
winner-take-all collapse count = 0
hard-gate bypass count = 0
committed replay produces no duplicate effect
stale bundle digest is rejected
```

Validation:

```bash
python scripts/check_horizon_gauge_arbitration_v0_12.py
```

Primary surfaces:

```text
docs/KUUOS_HORIZON_GAUGE_ARBITRATION_v0_12.md
runtime/kuuos_horizon_gauge_arbitration_core_v0_12.py
formal/KUOS/OpenHorizon/HorizonGaugeArbitrationV0_12.lean
```

### 1.11 Context Gauge Atlas v0.13

Status: **implemented transition kernel, persistence surfaces, local-lift surfaces, formal surface, and dedicated CI**

Purpose:

```text
Keep each context as a local chart.
Keep each policy state as a local section.
Use chart overlap to determine transition eligibility.
Parallel-transport only compatible local sections.
Record atlas curvature and cocycle defect without converting either into a veto.
Preserve chart-local state and non-Markov atlas holonomy.
Lift transported horizon weights toward one local v0.12 cycle.
```

Current classifications:

```text
isolated_chart
compatible_chart_transport
plural_atlas_transport
```

Current invariants:

```text
chart locality is preserved
no global context winner is created
transported horizon weights sum to 1
plurality floor remains visible
curvature and cocycle defect are bounded
processed child outcome / effect digests are not attributed twice
atlas holonomy advances append-only
```

Validation:

```bash
python scripts/run_context_gauge_atlas_v0_13.py
```

Primary surfaces:

```text
runtime/kuuos_context_gauge_atlas_transport_v0_13.py
runtime/kuuos_context_gauge_atlas_decision_v0_13.py
runtime/kuuos_context_gauge_atlas_lift_plan_v0_13.py
runtime/kuuos_context_gauge_atlas_lift_license_v0_13.py
formal/KUOS/OpenHorizon/ContextGaugeAtlasV0_13.lean
```

---

## 2. Phase A — Public Orientation Alignment

Status: **completed through v0.13; ongoing maintenance**

Goal:

```text
Keep README and ROADMAP aligned with the actual public baseline:
Qi and Memory surfaces, bounded executable runtime, v0.12 horizon gauge arbitration,
and v0.13 context gauge atlas transport.
```

Completed:

- README identifies KuuOS as gauge-theoretic rather than graph-theoretic;
- v0.12 and v0.13 badges, validation commands, primary files, and boundaries are visible;
- chart, section, overlap, transition, curvature, cocycle defect, and holonomy are defined for first-time reviewers;
- curvature is explicitly separated from veto authority;
- chart overlap is explicitly separated from graph edges;
- the canonical MGAP4D proof-facing boundary remains visible;
- bounded execution and repository adapters remain distinct from authority.

Maintenance criterion:

```text
No newly merged runtime or gauge layer may leave README and ROADMAP materially stale.
```

---

## 3. Phase B — Complete v0.13-to-v0.12 Local Gauge Execution

Status: **current next implementation priority**

Goal:

```text
Turn the validated v0.13 atlas transition kernel and local-lift surfaces into a
single replay-safe atlas invocation that starts exactly one v0.12 child cycle.
```

Tasks:

- add the v0.13 orchestration entrypoint;
- load current v0.12 and v0.13 state/bundle surfaces;
- bind source, root, registry, previous atlas state, and previous atlas bundle digests;
- persist atlas decision plus exact lifted v0.12 plan/license before child execution;
- execute exactly one v0.12 cycle;
- validate the exact child arbitration outcome and effect receipt;
- update only the target chart after realized effect evidence;
- append atlas outcome, state, committed ledger row, receipt, audit, and holonomy;
- recover pending runs using the exact saved transition and child packets;
- reject stale atlas digests before any child effect;
- demonstrate a multi-context sequence containing isolated, compatible, and plural transport cycles;
- retain `graph_semantics_forbidden` as a tested invariant.

Acceptance criteria:

```text
one v0.13 invocation -> zero or one v0.12 child
committed replay -> zero new child effects
pending recovery -> exact packet reuse
target chart only -> effect-grounded update
all transition residue remains visible
no global graph or context winner is created
```

---

## 4. Phase C — Gauge Atlas Composition and Holonomy Maturity

Status: **next**

Goal:

```text
Strengthen chart composition without replacing local transition functions with a graph.
```

Tasks:

- represent direct and composed transition functions explicitly;
- define finite cocycle composition checks on triple chart overlap;
- distinguish low-curvature compatible transport from persistent plural residue;
- preserve different transport paths in atlas holonomy;
- add recovery-cost and context-return examples;
- add bounded chart aging and reobservation rules without deleting historical lineage;
- formalize the relation between direct transport, composed transport, and cocycle defect;
- keep chart compatibility typed and context-specific.

Acceptance criteria:

```text
A reviewer can compare direct and composed local transports,
see the retained residue, and verify that no path is promoted to universal truth.
```

---

## 5. Phase D — Bounded Runtime and Repository Adapter Consolidation

Status: **parallel track**

Tasks:

- document executable action allowlists and finite sequence semantics;
- keep receipt and audit JSONL paths visible;
- distinguish bounded tick, local gauge transport, action preparation, actual effect, connector request, connector result, and repository mutation;
- add examples for failed, pending, blocked, stale, reobserve, repair, and handover outcomes;
- prevent PR adapter output from being treated as merge authority;
- align local commands and GitHub Actions checks.

---

## 6. Phase E — Validation Matrix and Release Consolidation

Status: **next**

Tasks:

- publish a compact validation matrix: command, files, invariant, output, failure class;
- include v0.12 and v0.13 failure classes;
- classify chart-overlap mismatch, stale atlas digest, cocycle overpromotion, curvature-veto leakage, local-to-global collapse, duplicate effect attribution, and graph-semantics leakage;
- ensure each release-facing package has a manifest, validation command, limitation statement, non-authority statement, and reproducibility note;
- keep stdlib-only Python checks where practical;
- preserve append-only release lineage.

---

## 7. Phase F — MemoryOS and Process-Tensor Integration

Status: **parallel priority**

Goal:

```text
Connect non-Markov process memory to chart-local gauge history without granting memory sovereignty.
```

Tasks:

- expose scar, relapse, reobserve, repair, and return-to-context examples;
- distinguish atlas holonomy from belief promotion;
- preserve individual chart lineage during collective reconstruction;
- prevent memory consolidation from erasing cocycle residue;
- connect Qi process tensor history to chart-local transport evidence;
- add memory-to-belief separation validators.

Rules:

```text
Memory persistence cannot become belief sovereignty.
Memory repair cannot become root overwrite.
Memory recall cannot erase uncertainty or chart residue.
Collective reconstruction cannot silently overwrite individual lineage.
```

---

## 8. Phase G — OS Bridge Projection

Status: **planned additive projection**

Candidate lanes:

```text
MemoryOS ecology and append-only lineage
BeliefOS causal belief surface and identifiability gaps
WorldModel observation-intervention reciprocity
PlanOS hierarchical temporal structure and rollback corridors
DecisionOS generative front and validated adjudication boundary
ReflectionOS repair and institutional-public governance
CausalSurface semantic mapping and bridge discipline
HybridControl continuous-discrete governance bridge
Yin-Yang / Wuxing / Qi tensor runtime surfaces
Witness / LocalGlobal / Boundary bridge surfaces
Recovery Governance surfaces
```

Projection rules:

```text
No internal baseline is silently projected as public authority.
Each projection needs a manifest, validator, cases, boundary statement, and release note.
Reflection summaries cannot rewrite world roots.
WorldModel predictions cannot become facts.
Decision candidates cannot become commits without gate validation.
Memory persistence cannot become belief sovereignty.
Plan success cannot become execution permission.
Local validation cannot silently become global truth.
```

---

## 9. Phase H — Formal Verification Bridge Maturity

Status: **parallel track**

Tasks:

- keep KuuOS formal surfaces distinct from canonical theorem repositories;
- expand v0.12 and v0.13 finite invariants;
- formalize bounded overlap, transition composition, cocycle defect, plurality floor, one-child execution, replay uniqueness, and holonomy monotonicity;
- route proof-facing claims through Lean/mathlib-facing theorem targets, CI, external review, and theorem-boundary statements;
- prevent formal-file, Lean-stub, mathlib-mapping, CI-pass, validator-pass, or GPT-summary overpromotion;
- keep MGAP4D, Super-Relativity, and superstring bridges proof-facing rather than authority-opening.

---

## 10. Phase I — Audit Proportionality and Harmony Repair

Status: **ongoing correction track**

Tasks:

- define finite audit budgets by surface and risk class;
- expose stop reasons for audit termination;
- distinguish observation, curvature, and residue from escalation;
- keep hold / reobserve / repair / handover as normal non-punitive outcomes;
- reserve grave-mode criteria for explicit severe boundary violations;
- prevent low-risk validator drift or nonzero curvature from triggering high-severity audit loops;
- preserve visible cost, proportionality, repairability, and harmony.

---

## 11. Public Reviewer Experience

Status: **ongoing**

Reviewer lanes:

```text
first-time AI governance reviewer
formal methods / Lean reviewer
runtime engineer
gauge-theory / local-global reviewer
memory-system reviewer
East Asian medicine / integrative medicine reviewer
physics-facing proof reviewer
GitHub / CI maintainer
```

Tasks:

- keep README concise enough to orient;
- keep ROADMAP structured by baseline and phase;
- use gauge-theory diagrams rather than graph diagrams for context transport;
- preserve Japanese and English orientation;
- add “what a pass does not mean” callouts;
- avoid turning deep internal baselines into unreviewable public noise;
- use append-only addenda for deep surfaces.

---

## 12. Long-Term Direction

KuuOS is moving toward a public architecture where:

```text
AI generation remains candidate-level.
Contexts remain local charts.
Policy states remain local sections.
Chart changes use typed transition functions.
Curvature and cocycle defects remain visible residue, not veto authority.
Holonomy remains path history, not sovereign truth.
Memory remains lineage and reconstructive support.
Belief remains calibrated and evidence-bound.
Planning remains rollback-aware and non-authoritative.
Decision remains boundary-owned and receipt-producing.
Reflection remains repair-facing, not root-rewriting.
Qi remains relational/process-facing, not substance or license.
Formal verification remains proof-facing, not self-authorizing.
Runtime remains bounded and receipt-producing.
Allowlisted execution remains finite and non-authoritative.
GitHub/CI adapters remain connector-explicit and non-authoritative.
Audit remains proportional, finite, repairable, and harmony-preserving.
```

The long-term goal is not to make an AI that simply acts more freely or searches a larger global graph.

The goal is to build a relational AI architecture in which:

```text
claims know their support,
sections know their chart,
transitions know their overlap,
curvature knows it is residue rather than prohibition,
plans know their boundary,
memories know their lineage,
proofs know their status,
runtime knows its stop conditions,
actions know their allowlist,
and governance knows when not to escalate.
```

---

## 13. Current Priority Summary

```text
1. Complete the replay-safe v0.13 orchestration that starts exactly one v0.12 child.
2. Demonstrate isolated, compatible, and plural chart transport across multiple contexts.
3. Preserve chart locality, plurality floor, cocycle residue, and atlas holonomy.
4. Keep graph semantics forbidden in context transport surfaces.
5. Expand Lean invariants for transition composition and cocycle defect.
6. Consolidate bounded executable runtime and repository-adapter documentation.
7. Project MemoryOS non-Markovian surfaces into chart-local gauge history carefully.
8. Strengthen validation matrices and release packages for v0.12/v0.13.
9. Preserve Qi and IndraNet as gauge/process fields and remain medical-modality neutral.
10. Prevent audit, curvature, or validation residue from becoming automatic escalation.
```
