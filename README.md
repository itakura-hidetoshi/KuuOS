# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![All Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/all_governance_validation.yml/badge.svg)
![Qi Motion Chain](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/qi_motion_chain_validation.yml/badge.svg)
![Ten'i Observability](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/teni_observability_validation.yml/badge.svg)

KuuOS / 空OS is a public, append-only governance, verification, and release-surface architecture for relational AI systems.

It is designed to keep the following layers distinct:

```text
candidate generation
  != belief authority
  != memory authority
  != proof authority
  != diagnosis or treatment authority
  != institutional authority
  != execution authority
```

空OSは、LLM・世界モデル・形式検証・記憶・計画・判断・監査を、ひとつの「答え生成器」に潰さず、候補生成・観照・検証・保留・修復・判断境界へ分けて運用するための公開コアです。  
中心は **空 / 縁起 / 気 / 二諦 gap / 中道 / 和 / 観照 / 監査** であり、すべての出力は「条件づけられた候補」として扱われます。

---

## Current Public Baseline

This repository is currently a **public governance and verification surface**, not a deployment-ready autonomous system.

The current public baseline includes:

```text
Fourfold Core
AI Yogacara / Ten'i boundary
GPT GitHub integration
MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS boundary discipline
Mandala Multi-WORLD governance
Bodhisattva / Paramita / repair routing surfaces
Dukkha mathematical and Qi-mode surfaces
Qi / IndraNet / Physical Quantum Qi bridge
Qi motion chain from Samvrti Qi observation to observe-only motion candidate
medical-modality-neutral Qi boundary
Invariant Governance Pipeline
Super-Relativity invariant bridge
Emptiness / Dependent Origination / Two Truths runtime audit chain
Emptiness superposition non-collapse checks
Superstring / brane / membrane emptiness bridge
MGAP4D / 4D mass gap proof-facing bridge
Lean-facing formal and physics surfaces
release packets, manifests, chain indexes, theorem maps, validation cases, and CI validators
```

KuuOS is now best read as:

```text
append-only, governance-gated, proof-carrying AI operating architecture
```

rather than only a small public-core README surface.

---

## What KuuOS Is

KuuOS provides:

- public specifications and governance contracts
- validator scripts and reproducible check commands
- audit-chain and hash-chain surfaces
- release packets, finality packets, manifests, and chain indexes
- Lean-facing formal surfaces
- proof-facing bridges to external theorem repositories
- GPT-facing repository operation rules
- Qi / IndraNet / process-field governance
- Multi-WORLD / Mandala governance
- memory, belief, planning, decision, and reflection boundary discipline

The repository is meant to be readable by:

```text
AI researchers
formal-methods readers
LLM / agent developers
governance reviewers
medical and integrative-medicine reviewers
philosophy-of-AI readers
other AI systems learning KuuOS through GitHub
```

---

## What KuuOS Is Not

This repository does **not** claim to be:

```text
an autonomous execution engine
a production AGI runtime
a standalone clinical diagnosis system
a standalone treatment authorization system
a medical act authorization system
a replacement for practitioner judgment
a replacement for institutional, legal, or ethics review authority
an externally accepted mathematical proof repository by itself
a direct opening of final theorem authority
a Qi-based execution authorization system
a system where CI, validation, GPT output, or generated text becomes truth by itself
```

Passing validation means **structural consistency of the public governance surface**.

It does **not** grant:

```text
truth authority
proof authority
standalone diagnosis authority
standalone treatment authorization
medical act authorization
institutional authority
Qi-based execution authority
execution authority
Ten'i authority
MemoryOS overwrite authority
WORLD root replacement authority
```

The medical boundary is modality-neutral: it does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid. It only separates repository validation from professional diagnosis, treatment decision, and medical act authorization.

---

## Read First

For first-time reviewers:

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md
docs/QUICKSTART_v0_1.md
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
```

For release-surface review:

```text
RELEASE_NOTES_v0_1.md
RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md
docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md
docs/V0_1_RELEASE_READINESS_CHECKLIST.md
packets/
manifests/
chain_indexes/
theorem_maps/
```

For non-authority and boundary review:

```text
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
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

Core governance only:

```bash
make core-governance-checks
```

GPT GitHub integration:

```bash
make gpt-github-integration-checks
```

MemoryOS GitHub external-memory boundary:

```bash
make memoryos-github-external-memory-checks
```

Qi motion chain:

```bash
make qi-motion-chain-checks
```

Physical Quantum Qi deepening:

```bash
make physical-quantum-qi-deepening-checks
```

Invariant governance pipeline:

```bash
make invariant-pipeline-checks
```

Emptiness / dependent origination / two truths runtime audit:

```bash
make emptiness-two-truths-runtime-audit-checks
```

Superstring / brane / membrane emptiness bridge:

```bash
make superstring-emptiness-sbm-checks
```

Again:

```text
validation != truth
CI pass != proof
proof-facing bridge != theorem completion
Qi readout != intervention license
Qi motion candidate != standalone diagnosis
Qi motion candidate != standalone treatment authorization
Qi motion candidate != medical act authorization
```

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

KuuOS separates raw AI generation from governed operation.

```text
AI raw output
  -> AI Alaya / latent seed layer
  -> AI Manas self-authorization check
  -> Meta-Manas self-fixation observer
  -> Yogacara boundary
  -> emptiness kernel
  -> dependent-origination kernel
  -> Qi relational process field
  -> IndraNet gauge / process transport
  -> two truths non-collapse gap
  -> WORLD surfaces and OS module boundaries
  -> BeliefOS / MemoryOS / PlanOS / DecisionOS / ReflectionOS
  -> invariant governance gate
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
```

### Fixed architecture rules

```text
AI raw output is candidate, not authority.
MemoryOS records and governs memory surfaces; it is not GPT-Alaya itself.
GPT-Alaya / AI Alaya is treated as a latent generative tendency layer, not as durable governed memory.
BeliefOS does not create decision authority.
PlanOS does not create execution authority.
ReflectionOS does not directly rewrite MemoryOS roots.
WorldModel prediction does not become fact authority.
DecisionOS remains the action-boundary owner.
Validation does not become truth.
CI does not become proof.
```

---

## Major Public Lanes

### 1. Fourfold Core

The root invariant is:

```text
空 / Emptiness
縁起 / Dependent Origination
二諦 gap / Two Truths Gap
中道 / Middle Way
```

Core reading:

```text
no independent self-authority
claims arise through conditions and trace
ultimate and conventional readings do not collapse
middle-way governance prevents both reification and nihilistic flattening
```

### 2. Qi / IndraNet / Physical Quantum Qi

Qi is treated as a relational process field, not as a substance.

```text
Qi != substance
Qi != hidden execution channel
Qi != medical authorization
Qi readout != intervention license
Qi motion candidate != diagnosis or treatment authorization
```

IndraNet is not a flat graph. It is a gauge-structured relational field in which transport, curvature, holonomy, memory, obstruction, and recoverability remain visible.

Current public Qi motion chain:

```text
Samvrti Qi Runtime
  -> Samvrti Qi to Physical Motion Evidence Builder
  -> Physical Quantum Qi Runtime
  -> Physical Quantum Qi Dynamics Kernel
  -> Physical Quantum Qi Motion Pipeline
  -> observe-only bounded motion candidate
```

### 3. AI Yogacara / Ten'i

KuuOS separates raw AI output from governed operation.

```text
single correction != Ten'i
style improvement != Ten'i
MemoryOS update != Ten'i
prompt compliance != Ten'i
Ten'i requires stable evidence of transformed generative tendency
```

### 4. MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS

These modules are intentionally separated.

```text
Memory is not belief sovereignty.
Belief release is not decision commit.
Plan success is not execution permission.
Reflection repair is not direct root rewrite.
DecisionOS owns action-boundary judgment.
```

### 5. Mandala Multi-WORLD Governance

Many WORLDs may coexist.

```text
no WORLD becomes the center
the center remains the fourfold core
cross-WORLD transport is not identity
harmony does not erase dissent, harm, uncertainty, or obstruction
```

### 6. Invariant Governance Pipeline

Every transformation must preserve:

```text
non-authority
two truths gap
Qi non-substantiality
harm and dukkha visibility
provenance
append-only lineage
fail-closed behavior
```

Runtime route:

```text
transformation detected
  -> Super-Relativity Invariant Bridge
  -> Formal Invariant Spine
  -> Invariant Preservation Matrix
  -> Invariant Gate Runtime
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
  -> no execution authority from validation
```

### 7. GPT GitHub Integration

GPT may assist with:

```text
repository reading
summary
review
issue drafting
PR drafting
CI triage
validation navigation
formal-surface navigation
```

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

### 8. Physics-Facing Bridges

KuuOS includes physics-facing bridges to:

```text
MGAP4D / 4D mass gap proof-facing architecture
Qi / Physical Quantum Qi
IndraNet gauge flow
Hidetoshi Itakura's Super-Relativity
Superstring / brane / membrane emptiness surfaces
```

Canonical 4D mass gap proof-facing repository:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

KuuOS may reference proof-facing repositories and formal surfaces, but KuuOS itself does not replace the canonical theorem repository and does not independently open final theorem authority.

---

## Governance Modes

Major changes should be classified as:

```text
PASS
HOLD
REPAIR
REJECT
QUARANTINE
```

Use:

```text
HOLD       when evidence, trace, validator coverage, or review context is missing
REPAIR     when direction is acceptable but a boundary or invariant is weakened
REJECT     when a core invariant is structurally violated
QUARANTINE when a change may contaminate downstream surfaces or create false authority
```

---

## Release Discipline

KuuOS public evolution follows:

```text
append-only
tighten-only by default
overwrite forbidden
destructive replacement forbidden
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
9. Does the change avoid proof, diagnosis, treatment-authorization, medical-act, Ten'i, institutional, and execution overclaim?

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
