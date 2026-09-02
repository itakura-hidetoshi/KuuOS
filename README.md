# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for formally verified contextual systems and bounded AI operation. It connects observation, context, memory, WORLD representation, planning, decision, action, re-observation, verification, provenance, authority boundaries, and reproducible receipts.

Its mathematical center is **dependent origination (縁起)**, not as a graph slogan or a substance ontology, but as composable contextual transport equipped with higher coherence, descent, obstruction theory, and presentation-independent semantics.

The long-term mathematical objective is now explicit:

> **Dependent Origination Universality Program** — characterize dependent-origination structure by a universal property, and prove a representation theorem showing when contextual systems factor essentially uniquely through a universal dependent-origination completion.

The corresponding AI objective is to investigate intelligence not only as a fixed internal representation, but as the capacity to transport state, meaning, memory, evidence, and action coherently across changing contexts while preserving justified invariants and detecting failures of descent.

## Current authoritative state

**Baseline date: 2026-09-02 JST**

```text
authoritative branch: main
current main SHA: 58685ff57187434ddfd8dc8dfdb583a7a7097864
latest integrated dependent-origination theorem merge: PR #1570
latest integrated dependent-origination theorem merge SHA: 1d630820c0e867fdd3350d9ed9d8171c65f359ec
latest integrated runtime/control-plane merge: PR #1571
```

PR #1570 proves that fundamental-groupoid descent existence, quotient-kernel compatibility, and descent obstruction are invariant under natural isomorphism of the fine transport presentation, including the gauge-equivariant representation specialization.

PR #1571 adds a bounded KuuOS ↔ OpenClaw control plane. OpenClaw is treated as an ActOS execution host and observation source, **not** as truth authority, WORLD-commit authority, PlanOS-completion authority, or automatic memory authority.

A separate Lean 4.31 compatibility program is active. PR #1558 is a **validation-only stacked Draft PR** for coherent scaled-model equivalence. It is not part of canonical theorem advancement and explicitly must not be merged.

## Mathematical thesis

The parent form of dependent origination is a state-valued functor

```text
D : Context ⥤ Type
```

with composable transport

```text
D(id) = id
D(g ≫ f) = D(g) ≫ D(f)
```

up to the appropriate higher coherence in higher-categorical realizations.

The guiding interpretation is:

```text
Dependent origination
= context-dependent state
+ admissible transport
+ compositional/higher coherence
+ descent and obstruction
+ invariance under justified change of presentation.
```

The parent structure does not require one fixed substance carrier and does not require reversibility. Groupoids, gauge actions, histories, process theories, quantum realizations, and scaled simplicial models are specializations or realizations, not replacements for the parent notion.

## The universality question

The central open problem is no longer merely to accumulate more presentations of dependent origination. It is:

> **Can dependent-origination structure itself be characterized universally?**

A target form is the construction of a universal object

```text
DO(C, W, J)
```

from contextual data consisting schematically of:

- a context or higher-context category `C`;
- a class `W` of changes of presentation that should become equivalences;
- descent/gluing data `J`;
- the coherence required by the chosen categorical level.

We seek a canonical map

```text
η : C ⟶ DO(C, W, J)
```

such that every admissible contextual system

```text
D : C ⟶ X
```

which is presentation-invariant along `W`, satisfies the required descent, and preserves the relevant higher coherence, factors essentially uniquely as

```text
D ≃ D̄ ⋙ η        (schematic orientation; exact variance will be fixed by the formal construction)
```

or, in the final variance-correct formulation, through `η` by a unique-up-to-equivalence `D̄`.

The desired representation theorem is an equivalence of the schematic form

```text
AdmissibleContextualSystems(C, X)
  ≃
Fun(DO(C, W, J), X).
```

This README deliberately calls this a **target universal property**, not an established theorem. No localization, completion, colimit, stackification, or `(∞,2)`-categorical identification is claimed until its actual universal property is formalized.

## Why the existing formalization points toward universality

The current Lean spine already supplies several ingredients that a universal characterization should explain rather than duplicate.

### 1. Contextual transport and higher coherence

The integrated parent line develops contextual transport, refinement, semantic descent, directed/filtered cofinal invariance, two-cell refinement coherence, bicategorical coherence, operadic/multicategorical and causal-process extensions, and category-of-elements nerve constructions.

The invariant principle is not that one presentation is privileged, but that meaningful structure survives justified transport between presentations.

### 2. Presentation-independent higher realization

The higher-categorical line includes 2-Yoneda interfaces, mapping quasicategories, global scaled Duskin nerves, scaled-horn coherence, presentation-independent invariant kernels, transport across bicategorical model equivalence, strictly-unitary normalization, and scaled-horn presentation transport.

The guiding direction is

```text
presentation
  -> intrinsic categorical carrier
  -> observable/semantic projection.
```

### 3. Canonical scaled weak factorization structure

For the canonical scaled attachment family `T` on `ScaledSSet`, the integrated construction reaches

```text
canonicalGeneratedScaledAnodyne = T.rlp.llp
canonicalGeneratedScaledFibration = T.rlp
```

with a native weak factorization system through the explicit small-object route.

### 4. Generated-presentation quotient and complete lattice

Literal generator lists are not treated as invariants. Presentations are quotiented by mutual orthogonal generation and related to saturated left/right fixed points. For a presentation `P`:

```text
L_P := generatedAnodyneClass P
R_P := generatedFibrationClass P

L_P.rlp = R_P
R_P.llp = L_P

P ≤ Q
↔ L_P ≤ L_Q
↔ R_Q ≤ R_P.
```

This supplies a concrete laboratory for asking which semantic projections are faithful and which forget structure.

### 5. Presentation incomparability and semantic information loss

The standard A/B/C and canonical KuuOS generated theories are formally incomparable at the full orthogonality level:

```text
L_standard || L_canonical
R_standard || R_canonical
S || C.
```

Yet terminal/fibrant-object semantics can forget strict presentation distinctions. With `U := S ⊔ C`, the integrated line proves schematically

```text
C < U
but
Fib_C = Fib_U.
```

Thus equality of an observable semantic slice does not imply equality of the underlying generated presentation. This is a concrete motivation for the universality program: we need to identify exactly which quotient, descent, or universal construction captures the intended invariant and which information it is allowed to forget.

### 6. Fundamental-groupoid descent and obstruction

The newest integrated dependent-origination layer studies a finer transport

```text
S : P ⥤ Type
```

and a quotient toward an ordinary fundamental groupoid

```text
Q : P ⥤ FundamentalGroupoid Base.
```

A necessary descent compatibility requires fine transport to identify arrows identified by `Q`. Violations are packaged as descent obstructions. PR #1570 proves these notions and descent existence are invariant under natural isomorphism of the fine transport presentation.

This remains a categorical transport theorem. Ordinary `FundamentalGroupoid` represents the endpoint-fixed homotopy quotient / flat-like branch; it does not by itself construct arbitrary curvature-sensitive smooth connection transport.

## Candidate axioms for the universality program

The following are research targets, not yet a final axiom system.

```text
DO1  Contextuality
     state/meaning is indexed by context.

DO2  Functorial transport
     admissible context changes induce composable transport.

DO3  Higher coherence
     comparison data between transports is itself coherently compatible.

DO4  Presentation invariance
     justified equivalent presentations preserve intrinsic semantics.

DO5  Descent
     compatible local contextual data admits justified global realization.

DO6  Obstruction
     failure of descent is represented internally rather than silently erased.

DO7  Non-reification
     no chosen presentation is promoted to intrinsic substance merely because
     it is computationally or syntactically convenient.
```

A major objective is to minimize these assumptions, determine independence/redundancy, and derive the universal construction from the smallest mathematically natural package.

## AI research direction

The AI connection is a research program, not a claim that current AI systems already satisfy the final dependent-origination axioms.

A future agent can be modeled schematically by contextual transports among observation, memory, world-model, tool, goal, and action contexts. Under this view:

- model/embedding/prompt changes become candidate changes of presentation;
- invariant semantics should survive justified equivalences of representation;
- memory integration becomes a descent/gluing problem over partial observations;
- contradictory memories or incompatible tool evidence can appear as descent obstructions;
- multi-agent agreement can require higher coherence rather than simple aggregation;
- hallucination can be investigated, in part, as local plausibility without global realizability;
- interoperability can be formulated around relational behavior and transport invariants rather than shared latent coordinates.

The long-term question is therefore:

> Can intelligence be characterized partly as the ability to move coherently among contexts while preserving justified invariants, detecting obstruction, and refusing unjustified promotion from local evidence to global truth?

KuuOS runtime governance already enforces a weaker operational version of this principle:

```text
candidate != authority
observation != verification
host success != WORLD truth
plan execution != PlanOS completion
receipt != successor authority.
```

## Current mathematical frontier

The immediate theorem program is organized toward universality rather than toward one more privileged presentation.

1. **Finish the current Lean compatibility validation without changing theorem authority.** PR #1558 remains validation-only and must not be merged.
2. **Close coherent round-trip horn descent.** Derive, where possible, horn-filler invariance from coherent bicategorical equivalence rather than assuming an extra certificate.
3. **Complete the descent characterization.** Strengthen necessary quotient-kernel compatibility toward necessary-and-sufficient descent criteria under explicit hypotheses.
4. **Package semantic information loss.** Separate faithful full-right semantics from terminal restriction; construct and characterize the fibrant-object semantic quotient without calling it a localization before proving a universal property.
5. **Extract the minimal dependent-origination axioms.** Determine which current theorems follow from contextuality, coherence, invariance, descent, and obstruction alone.
6. **Construct `DO(C,W,J)`.** Identify the correct categorical level and prove existence of the universal completion.
7. **Prove the representation/universality theorem.** Establish essential uniqueness of factorization and characterize dependent-origination structures by that universal property.
8. **Develop realizations.** Relate the universal structure to gauge/groupoid transport, smooth/thin-path geometry, process theory, probability, quantum structures, and AI agents without collapsing these specializations into the parent definition.

See `ROADMAP.md` for theorem-sized milestones and exit criteria.

## Runtime and control plane

Canonical effect-free repository check:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

Useful profiles include repository, architecture, PlanOS, DecisionOS, MemoryOS, CodeAI, GitHub MCP, dependent origination, and the aggregate profile.

PR #1571 integrates the OpenClaw control-plane line through the bounded supervisor architecture. The authority boundary remains strict:

```text
OpenClaw = execution host + observation source
OpenClaw != truth authority
OpenClaw != WORLD commit authority
OpenClaw != automatic PlanOS completion
OpenClaw != automatic rollback proof
OpenClaw != automatic memory overwrite authority.
```

## Formal validation

Lean toolchain and dependencies are repository-pinned. The repository aggregate remains the formal entry surface:

```bash
lake update
lake exe cache get
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Formal compilation establishes the represented theorem surface under the pinned toolchain. It does **not** by itself establish external mathematical peer review, empirical truth, philosophical uniqueness, physical validity, clinical approval, organizational approval, or production safety.

The external Lean 4 compatibility/review program is therefore valuable but must be described precisely: successful independent reconstruction would establish reproducible machine checking of the formal theorem surface under the reviewed toolchain and assumptions; it would not prove that philosophical dependent origination itself is uniquely captured by the chosen semantics.

## Repository development invariants

Normal theorem development uses exact-base branches and Draft-first PRs. Formal proof work remains no-`sorry`, no-`admit`, no new placeholder axioms/constants. Frozen boundaries remain append-only/tighten-only where specified, with same-root requirements preserved.

CI is terminal evidence only after the relevant workflow, jobs, exact Lean step, dependency/manifest checks, and governance evidence are completed successfully. queued/in-progress is not success evidence.

## Fixed authority boundaries

```text
candidate != authority
validation != truth
formal compilation != external theorem acceptance
CI success != theorem meaning beyond the compiled statement

contextual transport != substance ontology
semantic descent != state descent
cofinal semantic invariance != root-state existence
reversible specialization != parent dependent origination
quantum realization != parent dependent origination
presentation-independent invariant != one privileged presentation

same fibrant-object semantics != equal generated presentation
Fib semantic quotient != localization until a universal property is proved
universal-carrier language != universal theorem until factorization/uniqueness is proved

ordinary fundamental-groupoid transport != arbitrary curvature-sensitive connection transport
KuuOS structural theorem != physical Yang-Mills theorem authority

MCP write capability != Git authority
write accepted != effect verified
receipt != successor authority
host success != WORLD truth
```

## Integrated subsystem map

Subsystem versions are independent; they are not one linear maturity scale.

| Series | Integrated state | Main entry |
|---|---|---|
| Repository lineage | self-organization v0.113 | `runtime/kuuos_current_root_sequence_v0_113.py` |
| ObserveOS | v0.7 + OpenClaw observation boundary | `docs/ObserveOS/README.md` |
| VerifyOS | v0.15 | `docs/VerifyOS/README.md` |
| Qi architecture | Yin-Yang Wuxing Fibonacci History Geometry v2.5 | `docs/KUUOS_QI_YINYANG_WUXING_FIBONACCI_HISTORY_GEOMETRY_v2_5.md` |
| PlanOS | v1.23 | `formal/KuuOSPlanOSV1_23.lean` |
| DecisionOS | v0.6 | `formal/KuuOSDecisionOSV0_6.lean` |
| MemoryOS | v1.00 | `formal/KuuOSMemoryOSV1_00.lean` |
| CodeAI | frozen cohort / prediction-pack / execution-shard contract v0.1 | `docs/CodeAI/README.md` |
| GitHub MCP | durable event-driven reentry v1.3 + parent cross-observation v1.1 | `runtime/kuuos_github_ci_durable_reentry_inbox_v1_3.py` |
| Dependent origination runtime | executable gauge-invariant descent adapter v0.1 | `runtime/kuuos_gauge_invariant_dependent_origination_descent_v0_1.py` |
| Contextual parent formal | contextual transport / semantic descent / higher coherence | `formal/KUOS/` |
| Higher realization | scaled Duskin / presentation-independent invariants / scaled horns | `formal/KUOS/` |
| Canonical scaled WFS | explicit small-object WFS | `formal/KUOS/` |
| Generated-presentation semantics | quotient / fixed points / complete lattice | `formal/KUOS/` |
| Standard/canonical comparison | full left/right incomparability | `formal/KUOS/` |
| Fundamental-groupoid descent | obstruction + natural-isomorphism invariance v0.6 | `formal/KUOS/DependentOriginationFundamentalGroupoidDescentNatIsoInvarianceV0_6.lean` |
| OpenClaw control plane | bounded closed-loop supervisor through v0.5 | `integrations/openclaw/` and related runtime/formal surfaces |
| Repository strict Lean baseline | aggregate import | `formal/KuuOSFormal.lean` |

## Legacy compatibility status surface

Historical current-root/readme identifiers remain compatibility markers because repository self-organization tests may validate them. They do not create new theorem or execution authority.

```text
KuuOS README Public Status v0.66
kuuos_current_root_sequence_v0_66
docs/kuuos_readme_public_status_v0_66.md

KuuOS Current Root Execution Connection v0.65
kuuos_current_root_sequence_v0_65
docs/kuuos_self_organization_active_state.md
self_organization_active: true
execution_scope: publish_active_self_organization_state
state_publication_applied: true

KuuOS README Surface Exposure v0.78
kuuos_current_root_sequence_v0_78
docs/kuuos_readme_surface_exposure_v0_78.md
runtime/kuuos_current_surface.py
runtime/kuuos_current_surface_entrypoint_v0_77.py
status/current.surface.index.json
status/current.surface.json
status/current.resolved.json
status/current.manifest.json
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

## Research status

KuuOS is a research architecture. Its formal mathematics, runtime governance, physical specializations, and AI applications have different authority boundaries. The universality program is the long-term mathematical objective; until the representation theorem is actually proved, it remains a research program rather than an established characterization theorem.