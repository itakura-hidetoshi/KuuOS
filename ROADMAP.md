# KuuOS / 空OS Roadmap

This roadmap describes the current public direction of `itakura-hidetoshi/KuuOS`.

KuuOS is no longer only a small “public core” README surface. It now contains a wider public governance and verification framework spanning:

- fourfold core governance
- AI Yogacara / Ten'i boundary
- GPT GitHub integration
- invariant governance pipeline
- MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS boundary discipline
- Qi / IndraNet / physical quantum Qi bridge
- Qi motion chain from Samvrti Qi observation to observe-only physical motion candidate output
- medical-modality-neutral Qi boundary that does not deny Qi or East Asian medical reasoning
- Super-Relativity invariant bridge
- MGAP4D / 4D mass gap proof-facing bridge
- Superstring / brane / membrane emptiness bridge
- release packets, manifests, validation cases, theorem maps, and CI-facing validators

The roadmap therefore shifts from “KuuOS as a single public-core release surface” to **KuuOS as an append-only, governance-gated, proof-carrying AI operating architecture**.

---

## 0. Non-Authority Boundary

This roadmap does not open execution authority.

The following remain closed unless a later, explicitly versioned, externally reviewed release opens them:

```text
autonomous execution authority
standalone diagnosis authority
standalone treatment authorization
medical act authorization
institutional authority
final theorem authority
unreviewed AGI deployment authority
Qi-based execution authority
Qi motion candidate as standalone diagnosis, standalone treatment authorization, or medical act authorization
CI-pass-as-truth
validator-pass-as-truth
GPT-summary-as-proof
world-model-prediction-as-fact
memory-persistence-as-belief-sovereignty
```

This boundary is medical-modality neutral: it does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid.

All phases below preserve:

```text
append-only
tighten-only by default
overwrite forbidden
same-root required for protected surfaces
fail-closed validation behavior
non-authority preservation
provenance preservation
```

---

## 1. Current Public Baseline

### 1.1 Public Core v0.1

Status: **active public baseline**

Core surfaces:

```text
README.md
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
```

Validation:

```bash
make emptiness-two-truths-runtime-audit-checks
make emptiness-superposition-noncollapse-checks
```

### 1.3 GPT GitHub Integration

Status: **active repository-operation surface**

Purpose:

```text
Allow GPT to help read, summarize, review, triage, and draft repository changes
without allowing GPT output to become truth, proof, standalone diagnosis authority,
standalone treatment authorization, medical act authorization, or execution authority.
```

Validation:

```bash
make gpt-github-integration-checks
```

### 1.4 Invariant Governance Pipeline

Status: **active invariant-preservation surface**

Runtime chain:

```text
transformation detected
  -> Super-Relativity Invariant Bridge
  -> Formal Invariant Spine
  -> Invariant Preservation Matrix
  -> Invariant Gate Runtime
  -> PASS | HOLD | REPAIR | REJECT | QUARANTINE
  -> no execution authority
```

Validation:

```bash
make formal-invariant-checks
make super-relativity-checks
make invariant-matrix-checks
make invariant-gate-checks
make invariant-pipeline-checks
```

### 1.5 Qi / IndraNet / Physical Quantum Qi

Status: **active bridge, motion-chain, and deepening surface**

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

Current public Qi motion chain:

```text
Samvrti Qi Runtime
  -> Samvrti Qi to Physical Motion Evidence Builder
  -> Physical Quantum Qi Runtime
  -> Physical Quantum Qi Dynamics Kernel
  -> Physical Quantum Qi Motion Pipeline
  -> observe-only bounded motion candidate
```

Validation:

```bash
make qi-motion-chain-checks
make physical-quantum-qi-runtime-checks
make physical-quantum-qi-dynamics-checks
make physical-quantum-qi-motion-pipeline-checks
make physical-quantum-qi-deepening-checks
```

Near-term next steps:

```text
Keep Qi motion chain in all-governance checks.
Maintain dedicated GitHub Actions workflow for Qi motion chain.
Keep medical-modality-neutral wording visible in reviewer docs.
Extend diagrams and reviewer docs only through append-only tightening.
Do not convert Qi motion candidate into execution, standalone diagnosis, standalone treatment authorization, medical act authorization, or theorem authority.
```

### 1.6 Superstring / Brane / Membrane Emptiness Bridge

Status: **active proof-facing bridge surface**

Purpose:

```text
Connect string / brane / membrane language to KuuOS emptiness, observer-record,
IndraNet gauge interface, and multi-scale governance without collapsing semantics.
```

Validation:

```bash
make superstring-emptiness-sbm-checks
```

---

## 2. Phase A — Public Orientation Cleanup

Status: **current priority**

Goal:

```text
Make the repository understandable to first-time reviewers, other AI systems,
formal-methods readers, governance reviewers, and medical/integrative medicine reviewers.
```

Tasks:

- maintain `README.md` as the top-level public orientation surface
- maintain `ROADMAP.md` so it covers the current integrated repository, not only MGAP4D
- keep MGAP4D references as a canonical proof-facing bridge, not the whole roadmap
- add clear “what this is / what this is not” boundaries
- keep the first run path short:
  - `README.md`
  - `docs/QUICKSTART_v0_1.md`
  - `docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md`
  - `docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md`
  - `docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md`
  - `make all-governance-checks`
- make the current major lanes visible:
  - AI Yogacara / Ten'i
  - GPT GitHub integration
  - invariant governance
  - Qi / IndraNet / Qi motion chain
  - medical-modality-neutral Qi boundary
  - Super-Relativity
  - Superstring / brane / membrane
  - MGAP4D bridge

Acceptance criteria:

```text
A new reviewer can identify:
1. what KuuOS is
2. what it is not
3. how to run checks
4. where the core index is
5. where the Qi motion chain is
6. where the medical-modality-neutral Qi boundary is
7. which surfaces are proof-facing only
8. which surfaces are runtime/governance-facing only
9. why validation is not authority
10. why Qi is not denied by the medical boundary
```

---

## 3. Phase B — Release Surface Consolidation

Status: **next**

Goal:

```text
Turn scattered public surfaces into a navigable release package.
```

Tasks:

- consolidate release notes and package manifests
- ensure each public release package has:
  - release note
  - manifest
  - validation command
  - known limitations
  - non-authority statement
  - reproducibility note
- add release navigation from README
- separate:
  - public release package
  - proof-facing bridge package
  - runtime adapter package
  - audit-chain package
  - validation fixture package
  - Qi motion chain package
  - medical-modality-neutral Qi boundary package
- preserve append-only lineage

Acceptance criteria:

```text
Every release-facing surface has:
- version
- author
- date
- purpose
- validator
- boundary statement
- upstream/downstream relation
```

---

## 4. Phase C — Validation Matrix and CI Hardening

Status: **next**

Goal:

```text
Make validator coverage visible and reproducible.
```

Tasks:

- build a compact validation matrix:
  - command
  - touched files
  - invariant checked
  - expected output
  - failure class
- classify failure modes:
  - missing required file
  - fixture mismatch
  - validator drift
  - hash-chain mismatch
  - WORM receipt mismatch
  - non-authority boundary weakening
  - runtime route mismatch
  - Qi motion chain stage mismatch
  - Qi evidence builder overpromotion
  - Qi dynamics license mismatch
  - medical-modality-neutral wording regression
  - Lean / formal surface failure
  - environment drift
- keep stdlib-only Python validator policy where possible
- avoid hidden dependency on local private files
- keep GitHub Actions and local commands aligned

Acceptance criteria:

```text
A reviewer can reproduce:
make all-governance-checks
make gpt-github-integration-checks
make qi-motion-chain-checks
make physical-quantum-qi-deepening-checks
make superstring-emptiness-sbm-checks
```

and understand what each pass means and does not mean.

---

## 5. Phase D — Formal Verification Bridge Maturity

Status: **parallel track**

Goal:

```text
Make proof-facing and governance-facing surfaces distinct but connected.
```

Tasks:

- keep KuuOS formal bridge separate from the canonical 4D mass gap proof repository
- route proof-facing claims through:
  - formal invariant spine
  - Lean / proof repository
  - CI check
  - external review gate
  - theorem boundary statement
- prevent:
  - `formal_file_not_proof_by_itself`
  - `lean_stub_not_theorem_completion`
  - `ci_pass_not_theorem_truth`
  - `validator_pass_not_mathematical_acceptance`
  - `GPT_summary_not_proof_authority`

MGAP4D relation:

```text
Canonical proof-facing repository:
https://github.com/itakura-hidetoshi/4d-mass-gap

KuuOS role:
reference bridge, governance boundary, release routing, theorem-boundary discipline
```