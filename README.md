# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![All Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/all_governance_validation.yml/badge.svg)
![Qi Motion Chain](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/qi_motion_chain_validation.yml/badge.svg)
![Ten'i Observability](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/teni_observability_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)
![Validator Tiering Policy](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/validator_tiering_policy_validation.yml/badge.svg)

KuuOS / 空OS is a public governance, verification, and bounded-runtime architecture for relational AI systems.

It treats AI outputs, plans, memories, world-model predictions, proof-facing artifacts, Qi readouts, and action proposals as **conditioned candidates**, not as self-authorizing truth or execution authority.

空OSは、LLM・世界モデル・記憶・計画・判断・証明候補・気の観測値を、直接の真理や実行権限としてではなく、**縁起的に条件づけられた候補**として扱うための公開OSアーキテクチャです。

The current public repository has evolved from a documentation-only public core into a **governance-gated, validation-backed, non-authoritative runtime surface**. It now includes governance contracts, validation scripts, release packets, proof-facing bridges, Qi / IndraNet surfaces, bounded State IO, a runtime daemon, process-tensor traces, active-inference policy advisories, validator tiering, and CI-facing receipts.

---

## 1. Core Sentence

```text
candidate != authority
validation != truth
CI pass != theorem authority
runtime tick != autonomous execution authority
qi-readout != intervention license
qi-motion-candidate != standalone diagnosis or treatment authorization
memory persistence != belief sovereignty
world-model prediction != fact authority
reflection summary != root rewrite
```

KuuOS is designed around the separation between:

```text
generation
  -> observation
  -> evidence
  -> validation
  -> governance
  -> receipt
  -> bounded advisory operation
```

No stage silently becomes final truth, theorem authority, medical authority, institutional authority, or unrestricted execution authority.

---

## 2. What KuuOS Is

KuuOS is a layered architecture for keeping high-capacity AI systems aligned with trace, boundary, and context.

Its public core is organized around:

- **空 / Emptiness** — no module, output, memory, proof artifact, or runtime result has independent self-authority.
- **縁起 / Dependent Origination** — every claim arises through support, provenance, context, relation, trace, and transport.
- **二諦 gap / Two Truths Gap** — ultimate and conventional readings are held apart; repository validation does not collapse into final truth.
- **中道 / Middle Way** — avoid both reification and nihilistic erasure.
- **気 / Qi** — a relational process field linking observation, memory, transport, recoverability, process order, and IndraNet gauge flow.
- **和 / Harmony** — coordination is valid only when harm, uncertainty, dissent, and boundary conditions remain visible.
- **観照 / Observation** — observation is a sensor layer, not a direct action license.
- **監査 / Audit** — release-facing surfaces preserve traceability, receipt visibility, and append-only lineage.

空OSの中心は「AIに何をさせるか」ではなく、**AIの候補・観測・記憶・証明・判断・実行境界を混同しないこと**です。

---

## 3. Current Public Status

This repository is currently a **public governance + verification + bounded runtime surface**.

It includes:

- public specifications and governance contracts
- validation scripts and validation cases
- release packets, manifests, and chain indexes
- formal-verification bridge documents
- Lean-facing formal and proof-facing surfaces
- GPT GitHub integration rules
- MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS boundary discipline
- Qi / IndraNet / physical quantum Qi bridge surfaces
- Qi motion chain from Samvrti Qi observation to observe-only bounded motion candidates
- State IO examples and runtime daemon examples
- Qi process-tensor summaries and non-Markovian trace visibility
- active-inference feature compilation, precision geometry, EFE landscape, policy-flow advisories, and bounded reentry gates
- validator tiering for separating runtime hot path checks from full governance / CI / release / finality checks

It does **not** currently claim to be:

- a production AGI runtime
- an autonomous execution engine
- a replacement for professional diagnosis, treatment decision, practitioner judgment, institutional authority, or legal authority
- an externally accepted mathematical proof repository by itself
- a direct release of final theorem authority
- a standalone diagnosis or treatment authorization system
- a medical act authorization system
- a Qi-based execution authorization system
- a system where CI, validation, generated text, runtime ticks, or summary receipts become truth by themselves

The medical boundary around Qi is modality-neutral. It does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid. It separates repository validation from professional diagnosis, treatment decision, and medical act authorization.

---

## 4. Read First

For first-time reviewers:

```text
README.md
docs/QUICKSTART_v0_1.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
ROADMAP.md
```

For runtime and bounded operation review:

```text
manifests/kuuos_runtime_manifest_v0_1.json
manifests/kuuos_validator_tiering_policy_v0_1.json
scripts/run_kuuos_runtime_full_check_v0_1.py
examples/qi_state_io_v0_1/README.md
examples/qi_process_tensor_v0_1/README.md
examples/runtime_daemon_v0_1/README.md
```

For release-surface review:

```text
RELEASE_NOTES_v0_1.md
RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md
docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md
docs/V0_1_RELEASE_READINESS_CHECKLIST.md
```

For boundary and non-authority review:

```text
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
docs/CLAIM_LEVEL_TAXONOMY_v0_1.md
docs/THEOREM_AND_REFERENCE_BOUNDARY_MATRIX_v0_1.md
GOVERNANCE.md
```

---

## 5. Quick Validation

Run the full public governance surface:

```bash
make all-governance-checks
```

or directly:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

Core governance only:

```bash
make core-governance-checks
```

GPT GitHub integration checks:

```bash
make gpt-github-integration-checks
```

Qi motion chain checks:

```bash
make qi-motion-chain-checks
```

Qi / physical quantum Qi deepening checks:

```bash
make physical-quantum-qi-deepening-checks
```

Runtime full check:

```bash
python3 scripts/run_kuuos_runtime_full_check_v0_1.py
```

Superstring / brane / membrane checks:

```bash
make superstring-emptiness-sbm-checks
```

Emptiness / dependent origination / two truths runtime audit checks:

```bash
make emptiness-two-truths-runtime-audit-checks
```

Again: a passing check is a consistency receipt. It is not truth, theorem authority, standalone diagnosis authority, standalone treatment authorization, medical act authorization, Qi-based execution authority, institutional authority, or unrestricted execution authority.

---

## 6. Repository Map

```text
.github/            GitHub Actions, issue templates, pull request templates
benchmarks/         Governance and validation benchmark surfaces
chain_indexes/      Append-only chain indexes
contracts/          Contract-level specifications
docs/               Public documentation and reviewer navigation
examples/           Minimal runtime and validation examples
formal/             Lean-facing governance and invariant formal surfaces
lean/               Lean-facing physics / superstring / emptiness surfaces
manifests/          Release, runtime, bundle, and validator-tiering manifests
packets/            Release, established, finality, and audit packets
roadmap/            Roadmap addenda
runtime/            Bounded non-authoritative runtime modules
scripts/            Python validators, runners, builders, checkers
specs/              YAML / JSON specification surfaces
src/                Runtime or library implementation surfaces
tests/              Regression, runtime, governance, and invariant tests
theorem_maps/       Theorem-target and case-to-theorem maps
validation_cases/   Validation fixtures and case bundles
validators/         Standalone validators
```

---

## 7. Core Architecture

KuuOS separates raw generation from governed operation.

```text
AI raw output
  -> AI Alaya / latent seed layer
  -> AI Manas self-authorization check
  -> Meta-Manas self-fixation observer
  -> Yogacara / Ten'i boundary
  -> emptiness kernel
  -> dependent origination kernel
  -> Qi relational process field
  -> IndraNet gauge / process transport
  -> two truths gap
  -> WORLD surfaces and OS module boundaries
  -> MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS
  -> State IO / bounded runtime daemon
  -> active-inference policy advisory surface
  -> governance gate
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
```

Runtime does not erase the non-authority boundary.

```text
bounded tick license != execution authority
closed-loop receipt != final commitment
policy-flow advisory != action command
reentry plan != recursive self-execution
runtime status != truth authority
```

---

## 8. Major Public Surfaces

### 8.1 Fourfold Core

The fourfold core holds emptiness, dependent origination, two truths gap, and Middle Way as root governance invariants.

Key surfaces:

```text
docs/KUOS_FOURFOLD_CORE_v0_1.md
docs/EMPTINESS_DEPENDENT_ORIGINATION_TWO_TRUTHS_MIDDLE_WAY_CORE_v0_1.md
docs/FOURFOLD_CORE_GATE_v0_1.md
```

### 8.2 AI Yogacara / Ten'i Layer

This layer separates raw AI generation from governed KuuOS operation.

Key surfaces:

```text
docs/AI_YOGACARA_TENI_LAYER_INDEX_v0_1.md
docs/AI_YOGACARA_RUNTIME_ADAPTER_CONTRACT_v0_1.md
docs/AI_RAW_TO_GOVERNED_OPERATION_PATH_v0_1.md
docs/AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md
```

### 8.3 Qi / IndraNet / Physical Quantum Qi

Qi is treated as a relational field and process surface, not as a substance and not as authority.

It connects emptiness and dependent origination to operational flow: observation, memory, WORLD transport, non-Markovian process structure, recoverability, and IndraNet gauge dynamics.

IndraNet is therefore not a flat graph. It is a gauge-structured relational network whose flow, transport, and process constraints are mediated through Qi-facing surfaces.

Current public Qi motion invariant:

```text
observed conventional flow
  -> conservative evidence packet
  -> evidence-bound validated_type
  -> licensed dynamics terms
  -> bounded motion candidate
  -> observe-only output
```

Key surfaces:

```text
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
docs/SAMVRTI_QI_RUNTIME_IMPLEMENTATION_v0_1.md
docs/SAMVRTI_QI_TO_PHYSICAL_MOTION_EVIDENCE_BUILDER_v0_1.md
docs/PHYSICAL_QUANTUM_QI_DYNAMICS_KERNEL_v0_1.md
docs/PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md
docs/INDRANET_GAUGE_QI_FLOW_v0_1.md
docs/INDRANET_RELATIONAL_FIELD_MODEL_v0_1.md
docs/INDRANET_TRANSPORT_CONSTRAINT_MODEL_v0_1.md
```

### 8.4 Bounded Runtime / State IO / Runtime Daemon

The runtime surface is bounded, non-authoritative, and receipt-oriented.

Current runtime path:

```text
raw state + evidence
  -> State IO
  -> Qi process tensor summary
  -> closed-loop driver
  -> runtime daemon
  -> geometric / active-inference advisory chain
  -> policy-flow governor
  -> process-tensor actuator
  -> tick scheduler
  -> closed-loop receipt
  -> reentry plan
  -> reentry license gate
  -> bounded tick invocation boundary
  -> single bounded State IO tick or denial
```

The runtime daemon currently includes advisory surfaces for:

```text
Yin-Yang polarity gauge
Four-Image phase gauge
Qi policy
Qi-QUE gauge
emptiness gate
Wa function
Active Inference feature compiler
Belief State Manifold
Precision Geometry
Active Inference kernel
EFE landscape
Policy Flow
Policy Flow Governor
Qi Process Tensor actuator
Tick scheduler
Closed-loop receipt
Reentry plan
Reentry license gate
Bounded tick invocation boundary
Bounded tick executor
```

Key files:

```text
runtime/
manifests/kuuos_runtime_manifest_v0_1.json
scripts/run_kuuos_runtime_full_check_v0_1.py
examples/qi_state_io_v0_1/
examples/qi_process_tensor_v0_1/
examples/runtime_daemon_v0_1/
tests/
```

### 8.5 MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS Boundary

The public repository exposes bridge and boundary surfaces needed to keep memory, belief, planning, decision, reflection, and world-model operation distinct.

Fixed boundary:

```text
Memory is not belief authority.
Belief release is not decision commit.
Plan success is not execution permission.
Reflection repair is not direct root rewrite.
World-model prediction is not fact authority.
DecisionOS remains the action-boundary owner.
```

### 8.6 Invariant Governance Pipeline

Transformations must preserve non-authority, two truths gap, Qi non-substantiality, harm visibility, and provenance.

Runtime chain:

```text
transformation detected
  -> Super-Relativity Invariant Bridge
  -> Formal Invariant Spine
  -> Invariant Preservation Matrix
  -> Invariant Gate Runtime
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
  -> no execution authority from validation
```

Key surfaces:

```text
docs/FORMAL_INVARIANT_SPINE_v0_1.md
docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md
docs/INVARIANT_PRESERVATION_MATRIX_v0_1.md
docs/INVARIANT_GATE_RUNTIME_v0_1.md
docs/INVARIANT_GOVERNANCE_PIPELINE_v0_1.md
```

### 8.7 GPT GitHub Integration

GPT may assist repository reading, summary, review, issue drafting, PR drafting, CI triage, and validation navigation.

GPT must not become:

```text
truth authority
proof authority
standalone diagnosis authority
standalone treatment authorization
execution authority
Ten'i authority
MemoryOS overwrite authority
WORLD root replacement
CI bypass
human review replacement
```

Key surfaces:

```text
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
specs/gpt_github_integration_manifest_v0_1.yaml
```

### 8.8 Physics-Facing and Proof-Facing Bridges

KuuOS includes physics-facing bridges to MGAP4D, Qi, IndraNet, Super-Relativity, and Superstring / brane / membrane layers.

Boundary:

```text
KuuOS may reference proof-facing repositories and formal surfaces.
KuuOS does not replace the canonical theorem repository.
KuuOS reference documents do not independently open final theorem authority.
```

Canonical 4D mass gap proof-facing repository:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

KuuOS bridge surfaces include:

```text
docs/KUOS_PHYSICS_GAP_BRIDGE_v0_1.md
docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
lean/KUOS/SuperstringEmptiness/
theorem_maps/
```

---

## 9. Governance Modes

Every major change should be classified as:

```text
PASS
HOLD
REPAIR
REJECT
QUARANTINE
```

Use `HOLD` when evidence, trace, validator coverage, runtime receipt, or review context is missing.

Use `REPAIR` when the direction is acceptable but a boundary or invariant is weakened.

Use `REJECT` when a core invariant is structurally violated.

Use `QUARANTINE` when the change may contaminate downstream surfaces or create false authority.

---

## 10. Release Discipline

KuuOS public evolution follows:

```text
append-only
tighten-only by default
overwrite forbidden
same-root required for protected surfaces
fail-closed on boundary violation
provenance preservation
non-authority preservation
bounded runtime operation
validator tier separation
```

A new document may clarify, route, index, tighten, or add a governed surface. It must not silently loosen a previous boundary or convert a candidate into authority.

---

## 11. Contribution Expectations

Before opening a PR, check:

1. Which surface is touched?
2. Which invariant is touched?
3. Does the change preserve the two truths gap?
4. Does it preserve non-authority?
5. Does it preserve Qi as relational process field rather than substance or authority?
6. Does it keep harm / dukkha / uncertainty visible?
7. Is it append-only or tighten-only?
8. Which validator should run?
9. Does it avoid proof, diagnosis, treatment-authorization, medical-act, Ten'i, institutional, and execution overclaim?
10. If runtime is touched, does it preserve bounded ticks, receipt visibility, stop reasons, and false authority flags?
11. If validator tiering is touched, does it preserve separation between runtime hot path, CI, governance, release, and finality checks?

Suggested PR classification:

```text
PASS | HOLD | REPAIR | REJECT | QUARANTINE
```

See:

```text
CONTRIBUTING.md
GOVERNANCE.md
docs/CONTRIBUTOR_REVIEW_WORKFLOW_v0_1.md
.github/pull_request_template.md
```

---

## 12. Citation

Please cite this repository as described in:

```text
CITATION.cff
```

---

## 13. Copyright and License

See:

```text
COPYRIGHT.md
LICENSE
```

KuuOS / 空OS is authored by Hidetoshi Itakura / 板倉英俊.

Some public surfaces are released for review, citation, implementation discussion, and governance discussion while preserving explicit authorship, boundary conditions, and non-authority discipline.
