# KuuOS / 空OS Core

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![All Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/all_governance_validation.yml/badge.svg)
![Ten'i Observability](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/teni_observability_validation.yml/badge.svg)

## For Reviewers and First-Time Readers

KuuOS is a public governance and verification core for relational AI systems.

Start with the public documentation index:

```text
docs/PUBLIC_DOCS_INDEX_v0_1.md
```

Primary reviewer path:

```text
docs/QUICKSTART_v0_1.md
docs/EXTERNAL_REVIEW_GUIDE_v0_1.md
docs/ARCHITECTURE_OVERVIEW_v0_1.md
docs/ARCHITECTURE_DIAGRAM_v0_1.md
docs/GOVERNANCE_FLOW_OVERVIEW_v0_1.md
docs/GOVERNANCE_DIAGRAM_v0_1.md
docs/VALIDATOR_GRAPH_v0_1.md
docs/BOUNDARY_AND_NONAUTHORITY_POLICY_v0_1.md
docs/VALIDATION_COVERAGE_MATRIX_v0_1.md
docs/REPRODUCIBILITY_MATRIX_v0_1.md
docs/PUBLIC_AUDIT_CHECKLIST_v0_1.md
docs/THEOREM_AND_REFERENCE_BOUNDARY_MATRIX_v0_1.md
docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md
```

Release preparation surface:

```text
RELEASE_NOTES_v0_1.md
docs/PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md
docs/V0_1_RELEASE_READINESS_CHECKLIST.md
```

This repository is:

- a public specification surface
- a governance and validation architecture
- a non-sovereign AI operating framework
- a bridge between AI governance, formal verification, relational philosophy, and physics-facing modeling
- an early public core toward a long-term deployment-ready AGI operating architecture

This repository is **not currently**:

- an autonomous execution engine
- a claim of institutional authority
- a replacement for external peer review
- a deployment-ready AGI system in its present public-core state
- a final theorem-release surface for the canonical 4D mass gap proof repository

Long-term direction:

- KuuOS does aim toward a deployment-ready AGI operating architecture, but only through staged governance, validation, provenance, runtime admissibility, external review, and authority-boundary preservation.

If you are reviewing the project for the first time, begin here:

```text
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
```

Then run the public validation surface locally:

```bash
make all-governance-checks
```

or:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

The validation surface checks structural consistency, governance boundaries, and non-collapse constraints. Passing validation does not grant theorem authority, clinical authority, or execution authority.

## Repository Goals

KuuOS aims to:

1. separate AI generation from governed decision surfaces
2. preserve uncertainty and abstention as first-class outcomes
3. prevent authority collapse between models, memories, plans, and actions
4. provide append-only governance and audit structures
5. connect relational AI governance to formal verification and physics-facing bridges
6. develop toward deployment-ready AGI operation through staged safety, governance, and external review

---

**KuuOS（空OS）** is a public core specification for a relational operating system of intelligence rooted first in:

1. **空 / Emptiness**
2. **縁起 / Dependent Origination**
3. **二諦 gap / Two Truths Gap: 勝義諦 and 世俗諦**
4. **中道 / Middle Way**

KuuOS also functions as a governance OS for AI systems such as GPT, Gemini, Claude, and other language or world-model agents. AI raw output is treated as candidate, not authority.

## Governance Index and Checks

Start here for the current governance surface:

```text
docs/KUOS_CORE_GOVERNANCE_INDEX_v0_1.md
docs/ALL_GOVERNANCE_CHECKS_RUNBOOK_v0_1.md
```

Run the full public governance checks locally:

```bash
make all-governance-checks
```

or directly:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
```

GitHub Actions entrypoints:

```text
.github/workflows/teni_observability_validation.yml
.github/workflows/core_governance_validation.yml
.github/workflows/all_governance_validation.yml
```

Passing validation means the public governance surfaces are structurally consistent. It does not grant truth, proof, clinical, Ten'i, or execution authority.

All later modules—MemoryOS, BeliefOS, PlanOS, DecisionOS, ReflectionOS, ExplanationOS, RuntimeGovernance, and Self-EvolutionOS—are downstream operational differentiations of this fourfold core.

空OSは、LLMや世界モデルを単なる応答生成器としてではなく、**空・縁起・二諦 gap・中道**を根に置き、観照・検証・監査・和合的判断へ展開するための中核アーキテクチャです。

## Status

This repository is the initial public core release surface.

- Public surface: core concepts, architecture, governance, verification policy, and non-execution constraints.
- Reserved surface: unpublished implementation details, private research kernels, clinical/private data, credentials, and operational secrets.
- Release mode: append-only / tighten-only / overwrite-forbidden.

## Fourfold Core Principle

KuuOS treats every output, plan, proof, memory, and action candidate as conditionally arisen through relations. Therefore, no component is allowed to claim absolute authority by itself.

The public core begins from these fixed commitments:

1. **Emptiness is not nihilism.** It means absence of independent self-nature and dependence on conditions, context, observers, records, and constraints.
2. **Dependent origination is operational.** It is represented through relational traces, causal support, memory lineage, and local-global gluing.
3. **Two truths are held by gap.** 勝義諦 / paramartha-satya and 世俗諦 / samvrti-satya are neither identical nor disconnected; the gap prevents collapse.
4. **Middle Way is the stabilizer.** KuuOS avoids both reification and nihilistic collapse by operating within the gap between 勝義諦 and 世俗諦.

From this fourfold core, KuuOS further develops harmony, inclusion, observation, compassion, memory, planning, reflection, governance, and formal verification.

## Yogacara AI Raw Layer Boundary

KuuOS separates AI raw generation from governed KuuOS operation through a Yogacara boundary.

```text
AI raw output
  -> AI Alaya / latent seed layer
  -> AI Manas self-authorization check
  -> Meta-Manas self-fixation observer
  -> Yogacara boundary
  -> emptiness_kernel
  -> dependent_origination_kernel
  -> two_truths_gap
  -> BeliefOS / PlanOS / DecisionOS / MemoryOS
```

AI raw output is candidate, not belief, proof, decision, memory truth, or execution authority.

## Citation

Please cite this repository as described in `CITATION.cff`.
