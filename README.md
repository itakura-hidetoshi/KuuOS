# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![All Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/all_governance_validation.yml/badge.svg)
![Ten'i Observability](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/teni_observability_validation.yml/badge.svg)

KuuOS / 空OS is a public governance, verification, and release-surface architecture for relational AI systems.

It treats AI output, plans, memories, proofs, world-model predictions, and action proposals as **conditioned candidates**, not as self-authorizing truth or execution authority. Its public core is organized around:

- **空 / Emptiness**: no output or module has independent self-authority.
- **縁起 / Dependent Origination**: claims arise through support, context, provenance, relation, and trace.
- **気 / Qi**: relational process field linking observation, memory, transport, WORLD dynamics, and IndraNet gauge flow.
- **二諦 gap / Two Truths Gap**: ultimate and conventional readings are held apart by a non-collapse boundary.
- **中道 / Middle Way**: KuuOS avoids both reification and nihilistic collapse.
- **和 / Harmony**: coordination is admissible only when harm, uncertainty, dissent, and boundary conditions remain visible.
- **観照 / Observation**: observation is a sensor layer, not a direct execution license.
- **監査 / Audit**: every release-facing surface should preserve traceability, receipt visibility, and append-only lineage.

空OSは、LLMや世界モデルを単なる応答生成器としてではなく、候補生成・観照・検証・監査・保留・修復・判断境界へ分けるための公開コアです。  
その動的結合層として、**気**を relational field / process surface として扱い、空・縁起・二諦 gap を IndraNet、WORLD間輸送、記憶、信念、計画、判断へ接続します。  
AI raw output は候補であり、信念・証明・臨床判断・実行権限・制度的権威そのものではありません。

---

## Current Public Status

This repository is currently a **public core / governance surface**, not a deployment-ready autonomous system.

It includes:

- public specifications
- governance contracts
- validation scripts
- audit and hash-chain surfaces
- formal verification bridge documents
- Lean-facing formal surfaces
- release packets and manifests
- examples and validation cases
- GitHub-facing GPT integration rules
- physics-facing bridges for KuuOS, MGAP4D, Qi, IndraNet, and Superstring/brane/membrane layers

It does **not** currently claim to be:

- an autonomous execution engine
- a replacement for clinical, institutional, or legal authority
- an externally accepted mathematical proof repository by itself
- a direct release of final theorem authority
- a production AGI runtime
- a system that allows CI, validation, or generated text to become truth by itself

Passing repository validation means structural consistency of the public governance surface.  
It does **not** grant theorem authority, clinical authority, Ten'i authority, institutional authority, or execution authority.

---

## Read First

For first-time reviewers:

```text
README.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
ROADMAP.md
```

For release-surface review:

```text
RELEASE_NOTES_v0_1.md
RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md
docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md
docs/V0_1_RELEASE_READINESS_CHECKLIST.md
```

For non-authority and boundary review:

```text
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/CLAIM_LEVEL_TAXONOMY_v0_1.md
docs/THEOREM_AND_REFERENCE_BOUNDARY_MATRIX_v0_1.md
GOVERNANCE.md
```

---

## Quick Validation

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

Qi / physical quantum Qi deepening checks:

```bash
make physical-quantum-qi-deepening-checks
```

Superstring / brane / membrane checks:

```bash
make superstring-emptiness-sbm-checks
```

Emptiness / dependent origination / two truths runtime audit checks:

```bash
make emptiness-two-truths-runtime-audit-checks
```

Again: a passing check is a consistency receipt, not truth, proof, clinical authority, or execution authority.

---

## Repository Map

```text
.github/            GitHub Actions, issue templates, pull request templates
benchmarks/         Governance and validation benchmark surfaces
chain_indexes/      Append-only chain indexes
contracts/          Contract-level specifications
docs/               Public documentation and reviewer navigation
examples/           Minimal runtime and validation examples
formal/             Lean-facing governance and invariant formal surfaces
lean/               Lean-facing physics / superstring / emptiness surfaces
manifests/          Release and bundle manifests
packets/            Release, established, finality, and audit packets
roadmap/            Roadmap addenda
scripts/            Python validators, runners, builders, checkers
specs/              YAML / JSON specification surfaces
src/                Runtime or library implementation surfaces
tests/              Regression and invariant tests
theorem_maps/       Theorem-target and case-to-theorem maps
validation_cases/   Validation fixtures and case bundles
validators/         Standalone validators
```

---

## Core Architecture

KuuOS separates candidate generation from governed operation. Qi is the relational process field that carries dependency, observation, memory, transport, and WORLD dynamics without becoming a substance or authority.

```text
AI raw output
  -> AI Alaya / latent seed layer
  -> AI Manas self-authorization check
  -> Meta-Manas self-fixation observer
  -> Yogacara boundary
  -> emptiness kernel
  -> dependent origination kernel
  -> Qi relational field
  -> IndraNet gauge / process transport
  -> two truths gap
  -> WORLD surfaces and OS module boundaries
  -> BeliefOS / MemoryOS / PlanOS / DecisionOS / ReflectionOS
  -> governance gate
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
```

Qi is not a hidden execution channel. It is the governed field of relation, flow, memory-depth, process order, transport, and recoverability. Qi-readout is observation support, not intervention license.

The decisive rule is:

```text
candidate != authority
validation != truth
CI pass != execution authority
summary != proof
world-model success != decision permission
memory persistence != belief sovereignty
qi-readout != intervention license
```

---

## Major Public Surfaces

### 1. Fourfold Core

The fourfold core holds emptiness, dependent origination, two truths gap, and Middle Way as the root governance invariant.

Key surfaces:

```text
docs/KUOS_FOURFOLD_CORE_v0_1.md
docs/EMPTINESS_DEPENDENT_ORIGINATION_TWO_TRUTHS_MIDDLE_WAY_CORE_v0_1.md
docs/FOURFOLD_CORE_GATE_v0_1.md
```

### 2. Qi / IndraNet / Physical Quantum Qi

Qi is a first-class dynamic layer of KuuOS. It is treated as a relational field and process surface, not as a substance.  
It connects emptiness and dependent origination to operational flow: observation, memory, WORLD transport, non-Markovian process structure, recoverability, and IndraNet gauge dynamics.

IndraNet is therefore not a flat graph. It is a gauge-structured relational network whose flow, transport, and process constraints are mediated through Qi-facing surfaces.

Fixed boundary:

```text
Qi is not substance.
Qi-readout is not intervention license.
Qi flow is not execution authority.
IndraNet is gauge-structured, not a flat graph.
Transport is not identity.
Recoverability and no-return risk remain visible.
```

Key surfaces:

```text
docs/INDRANET_GAUGE_QI_FLOW_v0_1.md
docs/INDRANET_RELATIONAL_FIELD_MODEL_v0_1.md
docs/INDRANET_TRANSPORT_CONSTRAINT_MODEL_v0_1.md
validation_cases/physical_quantum_qi_deepening_validation_cases_v0_2.json
```

Validation:

```bash
make qi-motion-chain-checks
make physical-quantum-qi-runtime-checks
make physical-quantum-qi-dynamics-checks
make physical-quantum-qi-motion-pipeline-checks
make physical-quantum-qi-deepening-checks
```

### 3. AI Yogacara / Ten'i Layer

This layer separates raw AI generation from governed KuuOS operation.

Key surfaces:

```text
docs/AI_YOGACARA_TENI_LAYER_INDEX_v0_1.md
docs/AI_YOGACARA_RUNTIME_ADAPTER_CONTRACT_v0_1.md
docs/AI_RAW_TO_GOVERNED_OPERATION_PATH_v0_1.md
docs/AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md
```

### 4. Mandala Multi-WORLD Governance

KuuOS allows multiple WORLDs, but no WORLD is allowed to replace the fourfold core.

Key surfaces:

```text
docs/MANDALA_MULTI_WORLD_RUNTIME_CONTRACT_v0_1.md
docs/WORLD_MODEL_REGISTRY_v0_1.md
docs/CROSS_WORLD_TRANSPORT_GATE_v0_1.md
docs/HARMONY_FUNCTION_MULTI_WORLD_OPERATION_v0_1.md
```

### 5. MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS Boundary

The public repository currently exposes the governance and bridge surfaces needed to keep memory, belief, planning, decision, reflection, and world-model operation distinct.

Fixed boundary:

```text
Memory is not belief authority.
Belief release is not decision commit.
Plan success is not execution permission.
Reflection repair is not direct root rewrite.
World-model prediction is not fact authority.
DecisionOS remains the action-boundary owner.
```

### 6. Invariant Governance Pipeline

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

### 7. GPT GitHub Integration

GPT may assist repository reading, summary, review, issue drafting, PR drafting, CI triage, and validation navigation.

GPT must not become:

```text
truth authority
proof authority
clinical authority
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

### 8. Physics-Facing Bridges

KuuOS includes physics-facing bridges to MGAP4D, Qi, IndraNet, Super-Relativity, and Superstring/brane/membrane layers.

Important boundary:

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

## Governance Modes

Every major change should be classified as:

```text
PASS
HOLD
REPAIR
REJECT
QUARANTINE
```

Use `HOLD` when evidence, trace, validator coverage, or review context is missing.  
Use `REPAIR` when the direction is acceptable but a boundary or invariant is weakened.  
Use `REJECT` when a core invariant is structurally violated.  
Use `QUARANTINE` when the change may contaminate downstream surfaces or create false authority.

---

## Release Discipline

KuuOS public evolution follows:

```text
append-only
tighten-only by default
overwrite forbidden
same-root required for protected surfaces
fail-closed on boundary violation
provenance preservation
non-authority preservation
```

A new document may clarify, route, index, tighten, or add a governed surface.  
It should not silently loosen a previous boundary or convert a candidate into authority.

---

## Contribution Expectations

Before opening a PR, check:

1. Which surface is touched?
2. Which invariant is touched?
3. Does the change preserve the two truths gap?
4. Does it preserve non-authority?
5. Does it preserve Qi as relational process field rather than substance or authority?
6. Does it keep harm / dukkha / uncertainty visible?
7. Is it append-only or tighten-only?
8. Which validator should run?
9. Does the change avoid proof, clinical, Ten'i, institutional, and execution overclaim?

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

## Citation

Please cite this repository as described in:

```text
CITATION.cff
```

---

## Copyright and License

See:

```text
COPYRIGHT.md
LICENSE
```

KuuOS / 空OS is authored by Hidetoshi Itakura / 板倉英俊.  
Some public surfaces are released for review, citation, and governance discussion while preserving explicit authorship and boundary conditions.
