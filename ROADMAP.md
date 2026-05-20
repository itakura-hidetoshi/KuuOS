# KuuOS / 空OS Roadmap

This roadmap describes the current public direction of `itakura-hidetoshi/KuuOS`.

KuuOS has moved beyond a small public-core surface. It is now an append-only, governance-gated, proof-carrying AI operating architecture spanning:

```text
Fourfold Core
AI Yogacara / Ten'i
GPT GitHub integration
MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS boundary discipline
Mandala Multi-WORLD governance
Bodhisattva / Paramita / repair routing
Dukkha mathematical and Qi-mode surfaces
Qi / IndraNet / Physical Quantum Qi
Qi motion chain
medical-modality-neutral Qi boundary
Invariant Governance Pipeline
Super-Relativity invariant bridge
Emptiness / Dependent Origination / Two Truths runtime audit chain
Superstring / brane / membrane emptiness bridge
MGAP4D / 4D mass gap proof-facing bridge
Lean-facing formal surfaces
release packets, manifests, chain indexes, theorem maps, validation cases, and CI validators
```

The roadmap therefore shifts from:

```text
single public-core release surface
```

to:

```text
multi-surface governance OS with proof-carrying release discipline
```

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
Qi motion candidate as standalone diagnosis
Qi motion candidate as standalone treatment authorization
Qi motion candidate as medical act authorization
CI-pass-as-truth
validator-pass-as-truth
GPT-summary-as-proof
world-model-prediction-as-fact
memory-persistence-as-belief-sovereignty
```

This boundary is medical-modality neutral: it does not state that biomedicine is superior, that Qi is false, or that East Asian medical reasoning is invalid.

All roadmap phases preserve:

```text
append-only
tighten-only by default
overwrite forbidden
destructive replacement forbidden
same-root required for protected surfaces
fail-closed validation behavior
non-authority preservation
provenance preservation
```

---

## 1. Current Public Baseline

Status: **active public baseline**

Current baseline surfaces:

```text
README.md
ROADMAP.md
GOVERNANCE.md
CONTRIBUTING.md
CITATION.cff
COPYRIGHT.md
LICENSE
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md
```

Repository structure:

```text
.github/
benchmarks/
chain_indexes/
contracts/
docs/
examples/
formal/
lean/
manifests/
packets/
roadmap/
scripts/
specs/
src/
tests/
theorem_maps/
validation_cases/
validators/
```

Primary validation:

```bash
make all-governance-checks
```

Major lane validation:

```bash
make core-governance-checks
make gpt-github-integration-checks
make memoryos-github-external-memory-checks
make qi-motion-chain-checks
make physical-quantum-qi-deepening-checks
make invariant-pipeline-checks
make emptiness-two-truths-runtime-audit-checks
make superstring-emptiness-sbm-checks
```

Current interpretation:

```text
validation pass = structural consistency receipt
validation pass != truth
validation pass != proof
validation pass != diagnosis authority
validation pass != treatment authorization
validation pass != execution authority
```

---

## 2. Phase A — Public Orientation Refresh

Status: **current priority**

Goal:

```text
Make the repository understandable to first-time reviewers, other AI systems,
formal-methods readers, governance reviewers, and medical / integrative medicine reviewers.
```

Tasks:

- keep `README.md` as the top-level orientation surface
- keep `ROADMAP.md` aligned with the integrated repository, not only MGAP4D
- make the current major lanes visible:
  - Fourfold Core
  - AI Yogacara / Ten'i
  - GPT GitHub integration
  - MemoryOS / BeliefOS / PlanOS / DecisionOS / ReflectionOS boundary discipline
  - Qi / IndraNet / Qi motion chain
  - medical-modality-neutral Qi boundary
  - invariant governance
  - Super-Relativity
  - Superstring / brane / membrane
  - MGAP4D bridge
- shorten the first-review path:
  - `README.md`
  - `ROADMAP.md`
  - `docs/QUICKSTART_v0_1.md`
  - `docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md`
  - `docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md`
  - `docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md`
  - `make all-governance-checks`
- preserve non-authority wording throughout the top-level docs

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
Turn scattered public surfaces into navigable release packages.
```

Tasks:

- consolidate release notes and package manifests
- add release navigation from README and docs index
- group release surfaces into:
  - public core package
  - AI Yogacara / Ten'i package
  - GPT GitHub integration package
  - MemoryOS GitHub external memory package
  - Qi motion chain package
  - Physical Quantum Qi deepening package
  - medical-modality-neutral Qi boundary package
  - invariant governance package
  - emptiness / two truths runtime audit package
  - superstring / brane / membrane package
  - MGAP4D proof-facing bridge package
- ensure each public release package has:
  - version
  - author
  - date
  - purpose
  - validator
  - known limitations
  - non-authority statement
  - upstream/downstream relation
  - reproducibility note

Acceptance criteria:

```text
Every release-facing surface has:
- release note or packet
- manifest or chain index
- validator command
- boundary statement
- traceable lineage
```

---

## 4. Phase C — Validation Matrix and CI Hardening

Status: **next**

Goal:

```text
Make validator coverage visible, reproducible, and interpretable.
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
- keep stdlib-only Python validators where possible
- align GitHub Actions, `Makefile`, docs, and validator scripts
- add clear pass/fail interpretation for reviewers

Acceptance criteria:

```text
A reviewer can reproduce the main validation commands and understand:
1. what each check covers
2. what each check does not cover
3. which authority remains closed after a pass
4. which file or invariant caused a failure
```

---

## 5. Phase D — Qi / IndraNet / Process Tensor Maturity

Status: **parallel track**

Goal:

```text
Mature Qi as a relational process field while preserving non-substantiality and non-authority.
```

Tasks:

- keep Qi as open relational process field, not scalar stock or substance
- keep IndraNet as gauge-structured relational transport, not flat graph
- keep process tensor / non-Markovian memory surfaces visible
- maintain Physical Quantum Qi deepening checks
- preserve Qi OS handoff boundaries
- keep no-return risk, recoverability, and transport residue visible
- prevent Samvrti Qi acceptance from becoming FullPathQi promotion
- prevent Qi motion candidate from becoming diagnosis, treatment authorization, medical act authorization, or execution authority

Acceptance criteria:

```text
Qi-facing public docs and validators preserve:
- Qi non-substantiality
- IndraNet gauge structure
- evidence-bound motion chain
- observe-only output
- medical-modality-neutral wording
- authority-boundary completion
```

---

## 6. Phase E — MemoryOS / GPT-Alaya / External Memory Boundary

Status: **parallel track**

Goal:

```text
Keep governed memory, AI latent tendency, and GitHub external memory separate.
```

Tasks:

- clarify that MemoryOS is a governed memory/release surface, not GPT-Alaya itself
- treat GPT-Alaya / AI Alaya as latent generative tendency layer
- keep Ten'i distinct from MemoryOS update, style change, and prompt compliance
- mature `memoryos-github-external-memory-checks`
- define GitHub as external memory / public trace surface, not internal proof authority
- prevent repository persistence from becoming belief sovereignty
- keep append-only lineage, provenance, and review gates visible

Acceptance criteria:

```text
A reviewer can distinguish:
MemoryOS record
AI Alaya tendency
Ten'i evidence
GitHub external memory
belief authority
decision authority
```

---

## 7. Phase F — Formal Verification and Theorem Boundary Bridge

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
  - theorem boundary statement
  - external review gate
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

Acceptance criteria:

```text
KuuOS can cite and route proof-facing artifacts without becoming the theorem repository itself.
```

---

## 8. Phase G — Documentation Site and Reviewer Experience

Status: **next**

Goal:

```text
Make KuuOS learnable by humans and other AI systems.
```

Tasks:

- maintain `mkdocs.yml` and docs navigation
- add diagrams only when they preserve boundary wording
- provide reviewer paths:
  - quickstart path
  - governance path
  - formal verification path
  - Qi / IndraNet path
  - medical boundary path
  - GitHub / GPT integration path
- keep Japanese and English explanations aligned where possible
- keep conceptual terms exact:
  - 空
  - 縁起
  - 気
  - 二諦
  - 中道
  - 和
  - 観照
  - 監査

Acceptance criteria:

```text
A first-time reader can move from README to a runnable validator without losing the non-authority boundary.
```

---

## 9. Phase H — External Review and Publication Bridge

Status: **future**

Goal:

```text
Prepare public artifacts for external review without overclaiming authority.
```

Tasks:

- separate:
  - repository validation
  - formal proof check
  - theorem claim
  - external acceptance
  - release note
  - citation package
- keep Zenodo / GitHub / paper-facing artifacts traceable
- define public theorem boundary statements explicitly
- keep medical, institutional, and execution boundaries closed unless separately reviewed and opened
- maintain author, copyright, and citation metadata

Acceptance criteria:

```text
External reviewers can identify:
1. what artifact is being reviewed
2. what authority it has
3. what authority it does not have
4. what validator or proof surface supports it
5. what remains unresolved
```

---

## 10. Near-Term Checklist

```text
[ ] Keep README and ROADMAP synchronized with current repository structure.
[ ] Add or update release package navigation.
[ ] Add a validation matrix document.
[ ] Keep Qi motion chain in all-governance checks.
[ ] Keep Physical Quantum Qi deepening checks visible.
[ ] Keep MemoryOS external memory checks visible.
[ ] Keep medical-modality-neutral Qi boundary visible.
[ ] Keep MGAP4D bridge as proof-facing reference, not final theorem authority.
[ ] Keep GPT GitHub integration bounded by non-authority.
[ ] Keep docs and Makefile command names aligned.
[ ] Keep all public evolution append-only / tighten-only.
```

---

## 11. Development Rule

The roadmap follows the same rule as the public KuuOS core:

```text
append-only
tighten-only by default
overwrite forbidden
destructive replacement forbidden
same-root required
fail-closed on boundary violation
```

---

## 12. Version

```text
Version: v0.2-public-orientation
Date: 2026-05-20
Author: Hidetoshi Itakura / 板倉英俊
```
