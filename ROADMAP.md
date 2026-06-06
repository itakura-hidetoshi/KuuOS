# KuuOS / 空OS Roadmap

This roadmap describes the current public direction of `itakura-hidetoshi/KuuOS` as of June 2026.

KuuOS has moved beyond a small public-core documentation surface. It is now an append-only, governance-gated, validation-backed, proof-facing, memory-aware, Qi-process-aware, and bounded executable runtime architecture for relational AI systems.

The roadmap is organized around two simultaneous movements:

1. **Public repository maturity** — make the current governance, validation, runtime, Qi, memory, proof-facing, GitHub/CI, and boundary surfaces understandable and reproducible.
2. **Controlled KuuOS baseline projection** — gradually project the larger KuuOS baseline into public artifacts without collapsing candidate, validation, runtime, proof, medical, institutional, memory, GitHub, or execution authority.

---

## 0. Non-Authority Boundary

This roadmap does not open unrestricted autonomous authority.

The following remain closed unless a later, explicitly versioned, externally reviewed release opens them:

```text
unrestricted autonomous execution authority
arbitrary shell execution authority
arbitrary network execution authority
standalone diagnosis authority
standalone treatment authorization
medical act authorization
institutional authority
final theorem authority
unreviewed AGI deployment authority
Qi-based intervention authority
Qi motion candidate as standalone diagnosis or treatment authorization
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

All phases below preserve:

```text
append-only
tighten-only by default, but not automatic grave escalation
overwrite forbidden
same-root required for protected surfaces
fail-closed validation behavior
non-authority preservation
provenance preservation
bounded runtime operation
allowlist discipline
validator tier separation
audit proportionality
harmony and visible cost
```

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
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
```

Validation:

```bash
make core-governance-checks
make all-governance-checks
```

Purpose:

```text
Expose the public core.
Define non-authority.
Make validation reproducible.
Give reviewers a stable entry path.
```

### 1.2 Emptiness / Dependent Origination / Two Truths Runtime Audit Chain

Status: **active public audit-chain surface**

Core rule:

```text
runtime audit chain structural consistency is not theorem authority
hash-chain continuity is not truth
two truths non-collapse barrier must not reify ultimate truth
audit must not silently become infinite escalation
```

Validation:

```bash
make emptiness-two-truths-runtime-audit-checks
make emptiness-superposition-noncollapse-checks
```

### 1.3 Qi / IndraNet / Physical Quantum Qi

Status: **active bridge, motion-chain, process-tensor, and deepening surface**

Core direction:

```text
Qi is a relational field, not a substance.
Qi is not denied by the medical boundary.
East Asian medical reasoning is not denied by the medical boundary.
Biomedicine is not privileged by the wording.
IndraNet is gauge-structured, not a flat graph.
Process / memory / transport / recoverability surfaces remain first-class.
Qi motion is evidence-bound, licensed by validated type, and observe-only.
```

Validation:

```bash
make qi-motion-chain-checks
make physical-quantum-qi-runtime-checks
make physical-quantum-qi-dynamics-checks
make physical-quantum-qi-motion-pipeline-checks
make physical-quantum-qi-deepening-checks
```

### 1.4 KuuOS Bounded Runtime v0.1

Status: **active bounded non-authoritative runtime surface**

Current direction:

```text
Runtime is bounded.
Runtime is non-authoritative.
Runtime is receipt-producing.
Runtime may advance State IO by bounded ticks.
Runtime may execute allowlisted bounded actions.
Runtime does not open arbitrary execution authority.
Runtime does not open truth, theorem, clinical, memory-overwrite,
repository, or final-commitment authority.
```

Validation:

```bash
python3 scripts/run_kuuos_runtime_full_check_v0_1.py
```

### 1.5 Qi Process Tensor Cycle / Trend / Reliability Surface

Status: **active runtime maturity surface**

Current chain:

```text
cycle supervisor receipts + audit history + trajectory packet
  -> cycle trend summary
  -> trend class
  -> recommendation
  -> reliability score
  -> trend-adaptive supervisor packet
  -> trend-adaptive bounded supervisor run
```

Validation:

```bash
python scripts/check_qi_process_tensor_cycle_trend_summary_v3_9.py
python scripts/check_qi_trend_adaptive_supervisor_packet_v4_0.py
python scripts/check_qi_trend_adaptive_supervisor_run_v4_1.py
```

Acceptance criteria:

```text
A reviewer can see whether runtime cycles are stable, blocked, hold-dominant,
no-progress, or insufficient-history without converting trend into authority.
```

### 1.6 Allowlisted Executable Action Surface

Status: **active bounded executable surface**

Current chain:

```text
qi_executable_action_packet
  -> executable action dispatcher
  -> exactly one allowlisted action

qi_executable_action_sequence_packet
  -> executable action sequence runner
  -> finite declared sequence
  -> stop on completion or first blocked action
```

Validation:

```bash
python scripts/check_qi_executable_action_dispatcher_v4_2.py
python scripts/check_qi_executable_action_sequence_runner_v4_3.py
```

Acceptance criteria:

```text
A reviewer can identify the action allowlist, see the finite sequence,
inspect receipts, and verify that blocked actions stop the sequence.
```

### 1.7 GitHub Actions / PR Live-Loop Surface

Status: **active bounded repository-operation surface**

Current direction:

```text
GitHub/CI integration is becoming a bounded live-loop surface.
It can prepare connector requests, adapt connector results, collect PR/workflow
snapshots, and prepare bounded policy decisions.
It cannot grant repository authority by itself.
It cannot merge, rerun, or mutate without explicit downstream authority.
```

Current public chain:

```text
PR live query packet
  -> PR live request planner
  -> connector request packet
  -> connector result packet
  -> PR live result adapter
  -> raw PR info / workflow-runs packet
  -> live snapshot collector
  -> policy decision / action-prepared packet
  -> receipt + audit JSONL
```

Validation:

```bash
python scripts/check_qi_github_actions_pr_live_request_planner_v7_5.py
python scripts/check_qi_github_actions_pr_live_result_adapter_v7_6.py
```

Acceptance criteria:

```text
A reviewer can see the requested GitHub action, expected result file,
adapted packet, policy decision, action-prepared state, blockers, warnings,
and stop reason without treating the live-loop as repository authority.
```

### 1.8 MemoryOS / Non-Markovian Memory Baseline Projection

Status: **active internal baseline; public projection in progress**

Core direction:

```text
Memory is append-only lineage and reconstructive support.
Memory is not belief authority.
Memory is not root overwrite authority.
Memory must preserve trace, scar, holonomy, relapse lineage, process continuity,
collective reconstruction, and uncertainty visibility.
```

Near-term next steps:

```text
Create public MemoryOS index surfaces.
Expose non-Markovian memory examples through validation cases.
Document process-tensor memory linkage.
Separate memory persistence from belief promotion.
Add reviewer examples for relapse, scar, reobserve, repair, and handover.
```

### 1.9 MGAP4D / Formal Verification / Lean Bridge

Status: **active proof-facing bridge surface**

Boundary:

```text
KuuOS references canonical proof-facing repositories and formal surfaces.
KuuOS does not independently grant final theorem authority.
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

---

## 2. Phase A — Public Orientation Alignment

Status: **current priority**

Goal:

```text
Keep README and ROADMAP aligned with the v7.6 public state:
bounded runtime, Qi process tensor cycle maturity, allowlisted executable actions,
and GitHub Actions PR live-loop adapters.
```

Tasks:

- keep `README.md` as the top-level public orientation surface
- keep `ROADMAP.md` as the current integrated repository map
- replace stale wording that implies there is no executable runtime surface
- keep the stronger boundary: executable surface exists, but is bounded and non-authoritative
- keep MGAP4D references as canonical proof-facing bridges, not the whole roadmap
- expose Qi process tensor trend summary and reliability scoring
- expose trend-adaptive supervisor packet/run
- expose allowlisted action dispatcher and finite sequence runner
- expose GitHub Actions PR live request/result adapter path
- keep validator tiering visible
- expose audit proportionality and anti-infinite-audit rules

Acceptance criteria:

```text
A new reviewer can identify what KuuOS is, what it is not, how to run checks,
where the Qi motion/runtime/GitHub live-loop surfaces are, and why validation,
runtime ticks, allowlisted actions, and PR live adapters are not authority.
```

---

## 3. Phase B — Bounded Executable Runtime Consolidation

Status: **next**

Goal:

```text
Make bounded executable runtime operation reproducible, inspectable, and clearly non-authoritative.
```

Tasks:

- add or confirm Makefile aliases for v3.9 / v4.0 / v4.1 / v4.2 / v4.3 / v7.5 / v7.6 checks
- document the executable action allowlist
- document the finite sequence runner packet schema
- document stop-on-first-blocked-action semantics
- make receipt and audit JSONL paths visible
- distinguish bounded tick, allowlisted action, finite sequence, connector request, connector result adaptation, policy-prepared action, and actual repository mutation
- keep authority flags false unless a downstream explicit authority layer is introduced

Acceptance criteria:

```text
A reviewer can run checks, inspect outputs, and verify bounded tick behavior,
allowlisted action behavior, finite sequence behavior, PR live-loop adaptation,
stop reasons, and false authority flags.
```

---

## 4. Phase C — GitHub Actions Live-Loop Hardening

Status: **next**

Goal:

```text
Turn the PR live-loop into a safe, connector-explicit, audit-visible repository-operation surface.
```

Tasks:

- document the query packet
- document connector request packets
- document raw connector result packets
- document result adapter behavior
- document live snapshot collector behavior
- document policy-decision classes
- separate request planning, connector invocation, result adaptation, snapshot collection, policy recommendation, and actual mutation authority
- add examples for all-green workflows, failed workflows, pending workflows, draft PRs, closed PRs, mergeability unknown, missing head SHA, and stale connector results
- prevent live-loop output from being treated as merge authority

Acceptance criteria:

```text
A reviewer can follow a PR from query packet to connector request,
result adapter, workflow snapshot, policy decision, and stop reason without
a hidden repository mutation.
```

---

## 5. Phase D — Release Surface Consolidation

Status: **next**

Goal:

```text
Turn scattered public surfaces into navigable release packages.
```

Tasks:

- consolidate release notes and package manifests
- ensure each public release package has release note, manifest, validation command, limitations, non-authority statement, and reproducibility note
- add release navigation from README
- separate public release package, proof-facing bridge package, runtime adapter package, audit-chain package, validation fixture package, Qi motion chain package, bounded runtime package, executable action package, GitHub Actions PR live-loop package, medical-modality-neutral Qi boundary package, and MemoryOS projection package
- preserve append-only lineage

Acceptance criteria:

```text
Every release-facing surface has version, author, date, purpose, validator,
boundary statement, and upstream/downstream relation.
```

---

## 6. Phase E — Validation Matrix and CI Hardening

Status: **next**

Goal:

```text
Make validator coverage visible and reproducible.
```

Tasks:

- build a compact validation matrix: command, touched files, invariant checked, expected output, failure class
- classify failure modes: fixture mismatch, validator drift, non-authority weakening, runtime route mismatch, Qi evidence overpromotion, runtime tick overpromotion, allowlisted action overpromotion, sequence runner unboundedness, PR live-loop repository-authority leakage, recursive invocation leakage, memory-to-belief overpromotion, audit escalation loop, repeated AI wrong-code loop, Lean/formal surface failure, and environment drift
- keep stdlib-only Python validator policy where possible
- avoid hidden dependency on local private files
- keep GitHub Actions and local commands aligned

Acceptance criteria:

```text
A reviewer can reproduce the governance, runtime, Qi trend, executable sequence,
and PR live-loop checks and understand what each pass means and does not mean.
```

---

## 7. Phase F — Qi Process Tensor / Runtime Reentry Maturity

Status: **parallel track**

Goal:

```text
Stabilize Qi process tensor as the bounded-runtime memory/process spine without turning it into authority.
```

Tasks:

- preserve process history, transition continuity, memory continuity, non-Markovian memory, and missing-process-requirement visibility
- keep process tensor summaries compact but inspectable
- maintain trend classes and reliability score semantics
- maintain reentry planning as advisory
- keep reentry license gate explicit
- prevent recursive daemon self-invocation
- keep bounded tick executor to declared State IO ticks
- keep allowlisted executable actions explicit
- add reviewer examples for failure, hold, reobserve, quarantine, blocked action, and denial

Acceptance criteria:

```text
Qi process tensor can guide bounded runtime posture, but cannot grant truth,
theorem, clinical, final-commitment, memory-overwrite, repository, or unrestricted execution authority.
```

---

## 8. Phase G — MemoryOS Public Projection

Status: **parallel priority**

Goal:

```text
Project the non-Markovian, reconstructive, ecology-aware MemoryOS baseline into
public repository surfaces in a controlled, additive, non-authoritative way.
```

Candidate surfaces:

```text
MemoryOS public index
append-only memory lineage boundary
non-Markovian process trace examples
scar / holonomy / relapse lineage examples
collective reconstructive recall examples
memory-to-belief separation validator
memory reobserve / repair / handover examples
Qi process tensor memory linkage examples
```

Rules:

```text
Memory persistence cannot become belief sovereignty.
Memory repair cannot become root overwrite.
Memory recall cannot erase uncertainty.
Collective reconstruction cannot silently overwrite individual lineage.
```

---

## 9. Phase H — OS Bridge Projection

Status: **planned additive projection**

Goal:

```text
Project the broader KuuOS baseline into public repository surfaces in a controlled,
additive, non-authoritative manner.
```

Candidate projection lanes:

```text
MemoryOS ecology and append-only memory boundary
BeliefOS causal belief surface and identifiability gap taxonomy
WorldModel process tensor / observation-intervention reciprocity surface
PlanOS hierarchical temporal lattice and rollback corridors
DecisionOS generative front and validated adjudication boundary
ReflectionOS scalable oversight and institutional-public governance
CausalSurface semantic mapping and bridge discipline
HybridControl continuous-discrete governance bridge
Yin-Yang / Wuxing / Qi tensor runtime surfaces
Witness / LocalGlobal / Boundary bridge surfaces
Recovery Governance surfaces
```

Rules:

```text
No internal baseline is silently projected as public authority.
Each projection needs a manifest, validator, validation cases, boundary statement, and release note.
Reflection summaries cannot rewrite world roots.
WorldModel predictions cannot become facts.
DecisionOS candidates cannot become commits without gate validation.
MemoryOS persistence cannot become belief sovereignty.
PlanOS success cannot become execution permission.
Witness shells cannot bypass proof spine.
Local validation cannot silently become global truth.
```

---

## 10. Phase I — Formal Verification Bridge Maturity

Status: **parallel track**

Goal:

```text
Make proof-facing and governance-facing surfaces distinct but connected.
```

Tasks:

- keep KuuOS formal bridge separate from canonical theorem repositories
- route proof-facing claims through formal invariant spine, Lean/mathlib-facing theorem targets, CI checks, external review gates, and theorem boundary statements
- prevent `formal_file_not_proof_by_itself`, `lean_stub_not_theorem_completion`, `mathlib_mapping_not_theorem_authority`, `ci_pass_not_theorem_truth`, `validator_pass_not_mathematical_acceptance`, and `GPT_summary_not_proof_authority`
- add theorem-target maps only with explicit scope
- keep MGAP4D / Super-Relativity / Superstring bridges proof-facing, not authority-opening

---

## 11. Phase J — Audit Proportionality and Harmony Repair

Status: **current correction track**

Goal:

```text
Prevent audit and tighten-only rules from becoming automatic grave escalation,
infinite monitoring, or disharmonious governance behavior.
```

Tasks:

- define finite audit budgets by surface and risk class
- expose stop reasons for audit termination
- distinguish observation from escalation
- add hold / reobserve / repair / handover as normal, non-punitive outcomes
- add grave-mode criteria only for explicit severe boundary violations
- prevent low-risk validator drift from triggering high-severity audit loops
- document visible cost, proportionality, and harmony constraints

---

## 12. Phase K — Public Reviewer Experience

Status: **ongoing**

Goal:

```text
Make KuuOS legible to several audiences without flattening its structure.
```

Reviewer lanes:

```text
first-time AI governance reviewer
formal methods / Lean reviewer
runtime engineer
memory-system reviewer
East Asian medicine / integrative medicine reviewer
physics-facing proof reviewer
GitHub / CI maintainer
```

Tasks:

- keep README short enough to orient
- keep ROADMAP structured by phase
- add compact diagrams where useful
- preserve Japanese and English orientation
- avoid turning deep internal baselines into unreviewable public noise
- use append-only addenda for new surfaces

---

## 13. Long-Term Direction

KuuOS is moving toward a public architecture where:

```text
AI generation remains candidate-level.
Memory remains lineage and reconstructive support.
Belief remains calibrated and evidence-bound.
Planning remains rollback-aware and non-authoritative.
Decision remains boundary-owned and receipt-producing.
Reflection remains repair-facing, not root-rewriting.
Qi remains relational/process-facing, not substance or license.
Formal verification remains proof-facing, not self-authorizing.
Runtime remains bounded and receipt-producing.
Allowlisted execution remains finite and non-authoritative.
GitHub/CI live-loop remains connector-explicit and non-authoritative.
Audit remains proportional and finite.
```

The long-term goal is not to make an AI that simply acts more freely.

The goal is to make a relational AI architecture in which:

```text
claims know their support,
plans know their boundary,
memories know their lineage,
proofs know their status,
Qi readouts know their non-authority,
runtime knows its stop conditions,
actions know their allowlist,
GitHub/CI adapters know their repository boundary,
and governance knows when not to escalate.
```

---

## 14. Current Priority Summary

```text
1. Keep README and ROADMAP aligned with v7.6 public runtime state.
2. Consolidate bounded executable runtime documentation.
3. Harden GitHub Actions PR live-loop request/result adapter path.
4. Consolidate runtime and validator tiering documentation.
5. Project MemoryOS non-Markovian memory surfaces carefully.
6. Add anti-loop repair for repeated wrong-code AI behavior.
7. Strengthen Lean/mathlib bridge without claiming theorem authority.
8. Preserve Qi motion as observe-only and medical-modality neutral.
9. Prevent audit from becoming infinite or disharmonious.
10. Keep all public projections additive, bounded, and non-authoritative.
```
