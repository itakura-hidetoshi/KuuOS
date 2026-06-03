# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![All Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/all_governance_validation.yml/badge.svg)
![Qi Motion Chain](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/qi_motion_chain_validation.yml/badge.svg)
![Ten'i Observability](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/teni_observability_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)
![Validator Tiering Policy](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/validator_tiering_policy_validation.yml/badge.svg)

**KuuOS / 空OS** is a public governance, verification, memory, and bounded-runtime architecture for relational AI systems.

It treats AI outputs, memories, plans, world-model predictions, proof-facing artifacts, Qi readouts, and action proposals as **conditioned candidates**. They are not self-authorizing truth, proof, diagnosis, treatment authorization, institutional authority, or execution authority.

空OSは、LLM・記憶・世界モデル・計画・判断・証明候補・気の観測値・実行候補を、直接の真理や権限としてではなく、**縁起的に条件づけられた候補**として扱うための公開アーキテクチャです。

Current public status, June 2026: this repository is a **governance-gated, validation-backed, proof-facing, memory-aware, non-authoritative bounded-runtime surface**. It includes public contracts, validators, release packets, Lean-facing formal surfaces, Qi / IndraNet bridges, non-Markovian process traces, runtime receipts, validator tiering, and GitHub/CI-facing review paths.

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
plan success != execution permission
reflection summary != root rewrite
audit != infinite escalation
```

KuuOS keeps the following path explicit:

```text
generation
  -> observation
  -> evidence
  -> validation
  -> governance
  -> receipt
  -> bounded advisory operation
```

No stage silently becomes final truth, proof authority, medical authority, institutional authority, memory overwrite authority, or unrestricted execution authority.

---

## 2. What KuuOS Is

KuuOS is a layered architecture for keeping high-capacity AI systems aligned with trace, boundary, context, memory, and non-authority.

Its public core is organized around:

- **空 / Emptiness** — no output, module, proof artifact, memory, runtime result, or Qi readout has independent self-authority.
- **縁起 / Dependent Origination** — every claim arises through support, provenance, relation, condition, history, observation, and transport.
- **二諦 gap / Two Truths Gap** — conventional validation and ultimate meaning are not collapsed.
- **中道 / Middle Way** — avoid both reification and erasure.
- **気 / Qi** — a relational process field connecting observation, memory, transport, recoverability, order-sensitivity, and IndraNet gauge flow.
- **和 / Harmony** — coordination remains valid only while harm, uncertainty, dissent, cost, and boundaries stay visible.
- **観照 / Observation** — observation is a sensor surface, not a direct action license.
- **監査 / Audit** — audit preserves traceability and receipts, but must remain proportionate, finite, and boundary-aware.
- **記憶 / Memory** — memory is append-only lineage and reconstruction support, not belief sovereignty.
- **形式検証 / Formal Verification** — Lean/mathlib-facing surfaces are proof support, not theorem authority by themselves.

空OSの中心は「AIに何をさせるか」ではなく、**AIの候補・観測・記憶・証明・判断・実行境界を混同しないこと**です。

---

## 3. Current Public Status

This repository currently includes:

- public specifications and governance contracts
- validation scripts and validation cases
- release packets, manifests, and chain indexes
- boundary and non-authority policy documents
- GPT GitHub integration rules
- Lean-facing formal and proof-facing surfaces
- MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS boundary discipline
- Qi / IndraNet / physical quantum Qi bridge surfaces
- Qi motion chain from Samvrti Qi observation to observe-only bounded motion candidates
- State IO examples and runtime daemon examples
- Qi process-tensor summaries and non-Markovian trace visibility
- active-inference feature compilation, precision geometry, EFE landscape, policy-flow advisories, and bounded reentry gates
- validator tiering for runtime hot-path checks, local checks, CI checks, governance checks, release checks, and finality checks
- anti-loop governance for repeated AI error patterns and over-audit failure modes

It does **not** currently claim to be:

- a production AGI runtime
- an autonomous execution engine
- an externally accepted mathematical proof repository by itself
- a replacement for professional diagnosis, treatment decision, practitioner judgment, institutional authority, or legal authority
- a standalone diagnosis or treatment authorization system
- a medical act authorization system
- a Qi-based execution authorization system
- a system where CI, validation, generated text, runtime ticks, memory persistence, or summary receipts become truth by themselves

The medical boundary around Qi is modality-neutral. It does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid. It separates repository validation from professional diagnosis, treatment decision, and medical act authorization.

---

## 4. Read First

For first-time reviewers:

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md
docs/QUICKSTART_v0_1.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
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

For boundary and release review:

```text
GOVERNANCE.md
RELEASE_NOTES_v0_1.md
RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md
docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md
docs/V0_1_RELEASE_READINESS_CHECKLIST.md
docs/CLAIM_LEVEL_TAXONOMY_v0_1.md
docs/THEOREM_AND_REFERENCE_BOUNDARY_MATRIX_v0_1.md
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

A passing check is a **consistency receipt**. It is not truth, theorem authority, standalone diagnosis authority, standalone treatment authorization, medical act authorization, Qi-based execution authority, institutional authority, or unrestricted execution authority.

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

Audit also does not erase harmony.

```text
observation != escalation
audit trigger != infinite audit
tighten-only != automatic grave mode
hold/reobserve/repair/handover are first-class nonexecute outcomes
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

It is designed to catch AI self-authorization, repetitive wrong-code loops, premature closure, reflection overreach, memory overwrite, and CI bypass.

Key surfaces:

```text
docs/AI_YOGACARA_TENI_LAYER_INDEX_v0_1.md
docs/AI_YOGACARA_RUNTIME_ADAPTER_CONTRACT_v0_1.md
docs/AI_RAW_TO_GOVERNED_OPERATION_PATH_v0_1.md
docs/AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
```

### 8.3 Qi / IndraNet / Physical Quantum Qi

Qi is treated as a relational field and process surface, not as a substance and not as authority.

It connects emptiness and dependent origination to operational flow: observation, memory, WORLD transport, non-Markovian process structure, recoverability, and IndraNet gauge dynamics.

IndraNet is not a flat graph. It is a gauge-structured relational network whose flow, transport, and process constraints are mediated through Qi-facing surfaces.

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

Key files:

```text
runtime/
manifests/kuuos_runtime_manifest_v0_1.json
manifests/kuuos_validator_tiering_policy_v0_1.json
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

MemoryOS is moving toward non-Markovian, reconstructive, ecology-aware memory management: trace, scar, holonomy, relapse lineage, process continuity, and collective reconstruction are preserved without turning memory into sovereign belief.

### 8.6 Invariant Governance Pipeline

Transformations must preserve non-authority, two truths gap, Qi non-substantiality, harm visibility, audit proportionality, and provenance.

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

### 8.7 Formal Verification / Lean / mathlib Bridge

KuuOS includes Lean-facing and proof-facing bridge surfaces.

Boundary:

```text
Lean file != completed theorem
mathlib alignment != external mathematical acceptance
CI pass != theorem truth
formal stub != proof completion
GPT summary != proof authority
```

The long-term direction is to map KuuOS invariants into Lean/mathlib-compatible theorem targets while preserving the distinction between proof support, theorem completion, and external review.

### 8.8 Physics-Facing Bridges

KuuOS includes physics-facing bridges to MGAP4D, Qi, IndraNet, Super-Relativity, and Superstring / brane / membrane layers.

Boundary:

```text
bridge document != proof
physical analogy != theorem
candidate equation != accepted physics
simulation/validation != empirical confirmation
```

Canonical proof-facing repository for MGAP4D work:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

---

## 9. Governance Modes

KuuOS uses visible nonexecute outcomes instead of silent closure.

```text
PASS         allowed only inside declared scope
HOLD         stop and preserve state
REPAIR       produce a bounded repair candidate
REOBSERVE    gather more evidence before promotion
HANDOVER     route to a declared human/institutional/proof owner
REJECT       deny the candidate
QUARANTINE   isolate unsafe or boundary-breaking artifacts
```

Observation-only surfaces, including Slack-style observation channels, are not decision surfaces. They may provide awareness, but they do not sign final release, medical action, theorem authority, or institutional commitment.

---

## 10. Contribution Boundary

Contributions are welcome when they improve:

- documentation clarity
- validation reproducibility
- non-authority preservation
- Lean/proof-facing discipline
- bounded-runtime inspectability
- memory and process trace visibility
- Qi boundary clarity
- anti-loop and repeated-error repair
- audit proportionality and harmony

Contributions must not silently open:

```text
autonomous execution authority
standalone diagnosis authority
standalone treatment authorization
medical act authorization
institutional authority
final theorem authority
memory overwrite authority
CI-pass-as-truth
validator-pass-as-truth
runtime-tick-as-execution-authority
```

See `GOVERNANCE.md`, `CONTRIBUTING.md`, and `ROADMAP.md` before proposing structural changes.

---

## 11. License, Citation, and Attribution

Use `CITATION.cff` for citation metadata.

KuuOS / 空OS is authored and maintained by Hidetoshi Itakura / 板倉英俊 unless otherwise stated in repository files.

This README is an orientation surface. The authoritative repository state is the versioned file set, validation cases, manifests, packets, CI receipts, and governance documents in this repository.
