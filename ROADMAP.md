# KuuOS / 空OS Roadmap

This roadmap describes the current public direction of `itakura-hidetoshi/KuuOS`.

KuuOS has moved beyond a small public-core documentation surface. It is now an append-only, governance-gated, validation-backed, proof-facing, and bounded-runtime architecture for relational AI systems.

The roadmap is therefore organized around two simultaneous movements:

1. **Public repository maturity** — make the current governance, validation, runtime, Qi, proof-facing, and boundary surfaces understandable and reproducible.
2. **KuuOS internal baseline projection** — gradually mirror the larger KuuOS baseline into public artifacts without collapsing candidate, validation, runtime, proof, medical, institutional, or execution authority.

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
Qi motion candidate as standalone diagnosis or treatment authorization
CI-pass-as-truth
validator-pass-as-truth
runtime-tick-as-execution-authority
GPT-summary-as-proof
world-model-prediction-as-fact
memory-persistence-as-belief-sovereignty
reflection-summary-as-root-rewrite
```

This boundary is medical-modality neutral. It does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid.

All phases below preserve:

```text
append-only
tighten-only by default
overwrite forbidden
same-root required for protected surfaces
fail-closed validation behavior
non-authority preservation
provenance preservation
bounded runtime operation
validator tier separation
```

---

## 1. Current Public Baseline

### 1.1 Public Core Governance v0.1

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
Keep process-tensor and non-Markovian memory surfaces visible.
Maintain medical-modality-neutral wording in reviewer docs.
Do not convert Qi motion candidate into execution, standalone diagnosis, standalone treatment authorization, medical act authorization, or theorem authority.
```

### 1.6 KuuOS Bounded Runtime v0.1

Status: **active bounded non-authoritative runtime surface**

Core direction:

```text
Runtime is bounded.
Runtime is non-authoritative.
Runtime is receipt-producing.
Runtime may advance State IO by bounded ticks.
Runtime does not open autonomous execution authority.
Runtime does not open truth, theorem, clinical, memory-overwrite, or final-commitment authority.
```

Current runtime path:

```text
State IO
  -> Qi process tensor summary
  -> closed-loop driver
  -> runtime daemon
  -> geometric / active-inference advisory chain
  -> policy-flow governor
  -> process-tensor actuator
  -> bounded tick scheduler
  -> closed-loop receipt
  -> reentry plan
  -> reentry license gate
  -> bounded tick invocation boundary
  -> single bounded tick or explicit denial
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

Validation:

```bash
python3 scripts/run_kuuos_runtime_full_check_v0_1.py
```

Near-term next steps:

```text
Add a Makefile alias for runtime full check.
Expose runtime runbook in README.
Document bounded daemon operation separately from governance validation.
Keep validator tiering explicit.
Keep authority flags false.
Keep stop reasons visible.
```

### 1.7 Superstring / Brane / Membrane Emptiness Bridge

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

### 1.8 MGAP4D / Formal Verification Bridge

Status: **active proof-facing bridge surface**

Boundary:

```text
KuuOS references canonical proof-facing repositories and formal surfaces.
KuuOS does not independently grant final theorem authority.
CI pass does not equal mathematical acceptance.
Formal stub does not equal completed theorem.
GPT summary does not equal proof.
```

Canonical proof-facing repository:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

---

## 2. Phase A — Public Orientation Cleanup

Status: **current priority**

Goal:

```text
Make the repository understandable to first-time reviewers, other AI systems,
formal-methods readers, governance reviewers, runtime reviewers, and medical/integrative medicine reviewers.
```

Tasks:

- maintain `README.md` as the top-level public orientation surface
- maintain `ROADMAP.md` as the current integrated repository map
- keep MGAP4D references as canonical proof-facing bridges, not the whole roadmap
- add clear “what this is / what this is not” boundaries
- add bounded runtime status to the README
- add runtime full check to Quick Validation
- make validator tiering visible
- keep the first run path short:
  - `README.md`
  - `docs/QUICKSTART_v0_1.md`
  - `docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md`
  - `docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md`
  - `docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md`
  - `manifests/kuuos_runtime_manifest_v0_1.json`
  - `python3 scripts/run_kuuos_runtime_full_check_v0_1.py`
  - `make all-governance-checks`

Acceptance criteria:

```text
A new reviewer can identify:
1. what KuuOS is
2. what it is not
3. how to run checks
4. where the core index is
5. where the Qi motion chain is
6. where the runtime manifest is
7. where the medical-modality-neutral Qi boundary is
8. which surfaces are proof-facing only
9. which surfaces are runtime/governance-facing only
10. why validation is not authority
11. why runtime tick is not execution authority
12. why Qi is not denied by the medical boundary
```

---

## 3. Phase B — Runtime Surface Consolidation

Status: **next**

Goal:

```text
Make bounded runtime operation reproducible, inspectable, and clearly non-authoritative.
```

Tasks:

- add `make runtime-full-check`
- add `make runtime-manifest-checks`
- add `make validator-tiering-checks`
- write a runtime runbook for:
  - State IO
  - process-tensor summary
  - runtime daemon
  - status reader
  - active-inference advisory chain
  - policy-flow governor
  - bounded tick scheduler
  - closed-loop receipt
  - reentry license gate
  - bounded tick executor
- separate:
  - runtime hot path checks
  - local unit tests
  - CI checks
  - governance checks
  - release checks
  - finality checks
- make authority flags and stop reasons visible in reviewer docs

Acceptance criteria:

```text
A reviewer can run the runtime full check, inspect outputs, and verify:
- bounded tick behavior
- non-recursive invocation
- receipt visibility
- process tensor summary visibility
- stop reasons
- authority flags remain false
```

---

## 4. Phase C — Release Surface Consolidation

Status: **next**

Goal:

```text
Turn scattered public surfaces into navigable release packages.
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
  - bounded runtime package
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

## 5. Phase D — Validation Matrix and CI Hardening

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
  - runtime tick overpromotion
  - recursive invocation leakage
  - authority flag regression
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
python3 scripts/run_kuuos_runtime_full_check_v0_1.py
```

and understand what each pass means and does not mean.

---

## 6. Phase E — Qi Process Tensor / Runtime Reentry Maturity

Status: **parallel track**

Goal:

```text
Stabilize Qi process tensor as the bounded-runtime memory/process spine without turning it into authority.
```

Tasks:

- preserve process history visibility
- preserve transition continuity visibility
- preserve memory continuity visibility
- preserve non-Markovian memory visibility
- preserve missing-process-requirement reporting
- keep process tensor summaries compact but inspectable
- maintain reentry planning as advisory
- keep reentry license gate explicit
- prevent recursive daemon self-invocation
- keep bounded tick executor to one licensed State IO tick
- add reviewer examples for failure, hold, reobserve, quarantine, and denial

Acceptance criteria:

```text
Qi process tensor can guide bounded runtime posture,
but cannot grant truth, theorem, clinical, final-commitment, memory-overwrite,
or unrestricted execution authority.
```

---

## 7. Phase F — OS Bridge Projection

Status: **planned additive projection**

Goal:

```text
Project the broader KuuOS baseline into public repository surfaces in a controlled, additive, non-authoritative manner.
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
```

Acceptance criteria:

```text
Each OS bridge projection has:
- public artifact name
- source baseline reference
- scope boundary
- validator
- failure cases
- non-authority clause
- release packet
```

---

## 8. Phase G — Formal Verification Bridge Maturity

Status: **parallel track**

Goal:

```text
Make proof-facing and governance-facing surfaces distinct but connected.
```

Tasks:

- keep KuuOS formal bridge separate from canonical theorem repositories
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
- add theorem-target maps only with explicit scope
- keep MGAP4D / Super-Relativity / Superstring bridges proof-facing, not authority-opening

MGAP4D relation:

```text
Canonical proof-facing repository:
https://github.com/itakura-hidetoshi/4d-mass-gap

KuuOS role:
reference bridge, governance boundary, release routing, theorem-boundary discipline
```

---

## 9. Phase H — Reviewer Experience and External Audit Readiness

Status: **planned**

Goal:

```text
Make KuuOS readable, reproducible, and reviewable by humans and AI systems without simplifying away its boundary discipline.
```

Tasks:

- add a reviewer index by audience:
  - general AI safety / governance reviewer
  - formal methods reviewer
  - runtime engineer
  - Qi / East Asian medicine reviewer
  - physics-facing reviewer
  - GitHub / CI reviewer
- add diagrams for:
  - fourfold core
  - Qi / IndraNet process tensor path
  - runtime daemon bounded tick loop
  - non-authority gates
  - proof-facing vs runtime-facing separation
- keep diagram labels short and English-friendly for broad review
- add reproducibility recipes
- add failure-mode examples
- add “what a pass does not mean” callouts

Acceptance criteria:

```text
A reviewer can inspect the repository without confusing:
- candidate with authority
- validation with truth
- runtime tick with execution authority
- Qi readout with intervention license
- formal bridge with theorem completion
- medical boundary with denial of Qi
```

---

## 10. Long-Term Direction

KuuOS aims to become a public, formally constrained AI operating architecture where:

```text
raw model output is candidate only
memory is append-only and non-sovereign
belief is evidence-bound
world-model prediction is advisory
planning is reversible and rollback-aware
decision is multi-value and gate-validated
reflection is advisory and non-rewriting
Qi is relational process field
IndraNet is gauge-structured
runtime is bounded and receipt-producing
validation is reproducible but non-authoritative
formal proof surfaces remain theorem-boundary aware
```

The public repository should eventually provide:

```text
clear entry path
stable release packages
runtime examples
formal bridge documents
validator matrix
CI reproducibility
boundary taxonomy
non-authority receipts
OS bridge manifests
reviewer-facing diagrams
```

---

## 11. Final Roadmap Rule

KuuOS development remains:

```text
additive-only
tighten-only by default
overwrite forbidden
same-root required
fail-closed on boundary violation
candidate never self-authorizes
validation never becomes truth by itself
runtime never becomes autonomous authority by itself
```
