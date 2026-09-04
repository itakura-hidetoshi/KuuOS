# KuuOS / 空OS

![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for formally verified contextual systems and bounded AI operation. It connects observation, context, memory, WORLD representation, retrieval, planning, decision, action, re-observation, verification, provenance, authority boundaries, and reproducible receipts.

Its mathematical center is **dependent origination (縁起)**. Its interpretation of **空 (śūnyatā / emptiness)** is an anti-reification constraint: no model, representation, index, graph, memory state, runtime receipt, or preferred presentation receives intrinsic truth merely because it is convenient, executable, canonical, or locally successful.

The long-term mathematical objective is explicit:

> **Dependent Origination Universality Program** — characterize dependent-origination structure by a universal property, and prove a representation theorem showing when contextual systems factor essentially uniquely through a universal dependent-origination completion.

The corresponding AI objective is to study intelligence not only as a fixed internal representation, but as the capacity to transport state, meaning, evidence, memory, plans, and actions coherently across changing contexts while preserving justified invariants and exposing failures of descent.

## Documentation snapshot

**Baseline: 2026-09-04 JST**

This README was rewritten from the canonical main state based at:

```text
authoritative branch: main
documentation snapshot base SHA: c188314e60fbd03dd6044075a19c89ab95634aea
latest integrated dependent-origination theorem merge: PR #1570
latest integrated dependent-origination theorem merge SHA: 1d630820c0e867fdd3350d9ed9d8171c65f359ec
universality-program documentation integration: PR #1573
adaptive retrieval policy integration: PR #1574
adaptive retrieval subsystem integration: PR #1575
bounded OpenClaw control-plane integration: PR #1571
repository self-organization root: kuuos_current_root_sequence_v0_113
```

PR #1570 proves that fundamental-groupoid descent existence, quotient-kernel compatibility, and descent obstruction are invariant under natural isomorphism of the fine transport presentation, including the gauge-equivariant representation specialization.

PR #1573 reframed the public mathematical objective around dependent-origination universality rather than around one privileged presentation.

PR #1574 introduced the **least-sufficient adaptive retrieval policy**. PR #1575 integrated it as a bounded KuuOS subsystem with runtime, tests, manifest, formal contract, aggregate import, and cumulative runtime validation.

PR #1571 integrates a bounded KuuOS ↔ OpenClaw control plane. OpenClaw is treated as an execution host and observation source, **not** as truth authority, WORLD-commit authority, PlanOS-completion authority, or automatic memory authority.

A separate Lean 4.31 compatibility program remains active in PR #1558. It is a **validation-only stacked Draft PR** and explicitly must not be merged. The validation line began from the coherent scaled-model compatibility frontier and has since accumulated later scaled-simplicial validation work. Its CI state is compatibility evidence only; it is not canonical theorem authority.

## What “空” means in KuuOS

KuuOS does not formalize a metaphysical slogan that “nothing exists.” Its operational and mathematical use of emptiness is narrower and stricter:

```text
no chosen presentation = intrinsic substance by default
no local observation = global truth by default
no retrieval score = entailment by default
no runtime success = WORLD truth by default
no formal encoding = philosophical uniqueness by default
```

This motivates a recurring mathematical question:

> Which structure survives a justified change of presentation, and what universal property characterizes exactly that invariant content?

In this sense, the bridge from 空 to 縁起 is not a graph metaphor. It is the move from reified objects toward **context-indexed states, admissible transport, coherence, descent, obstruction, and invariance under justified equivalence**.

## Mathematical thesis

A parent form of dependent origination is a state-valued functor

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
+ compositional / higher coherence
+ descent and obstruction
+ invariance under justified change of presentation
+ non-reification of any one presentation.
```

The parent structure does not require one fixed substance carrier and does not require reversibility. Groupoids, gauge actions, histories, process theories, quantum realizations, retrieval systems, and scaled simplicial models are specializations or realizations, not replacements for the parent notion.

## The universality question

The central open problem is:

> **Can dependent-origination structure itself be characterized universally?**

A target form is a construction

```text
DO(C, W, J, H)
```

from contextual data consisting schematically of:

- a context or higher-context category `C`;
- a class `W` of presentation changes that should become equivalences;
- descent/gluing data `J`;
- higher-coherence structure `H` required by the chosen categorical level.

We seek a canonical map

```text
η : C ⟶ DO(C, W, J, H)
```

such that every admissible contextual system factors through `η` essentially uniquely. The desired representation theorem is schematically

```text
AdmissibleContextualSystems(C, X)
  ≃
Fun(DO(C, W, J, H), X).
```

This is a **target universal property**, not an established theorem. No localization, completion, colimit, stackification, fibrant replacement, or `(∞,2)`-categorical object is called “the” universal dependent-origination object until factorization, essential uniqueness, and the required naturality are actually proved.

## Integrated formal foundations

The canonical theorem spine already contains substantial structure that the universality theorem should explain rather than duplicate.

### Contextual transport and higher coherence

The integrated parent line develops contextual transport, refinement, semantic descent, directed/filtered cofinal invariance, two-cell refinement coherence, bicategorical coherence, operadic/multicategorical and causal-process extensions, and category-of-elements nerve constructions.

### Presentation-independent higher realization

The higher-categorical line includes 2-Yoneda interfaces, mapping quasicategories, global scaled Duskin nerves, scaled-horn coherence, presentation-independent invariant kernels, transport across bicategorical model equivalence, strictly-unitary normalization, and scaled-horn presentation transport.

The guiding direction is:

```text
presentation
  -> intrinsic categorical carrier
  -> observable / semantic projection.
```

### Canonical scaled weak factorization structure

For the canonical scaled attachment family `T` on `ScaledSSet`, the integrated construction reaches

```text
canonicalGeneratedScaledAnodyne = T.rlp.llp
canonicalGeneratedScaledFibration = T.rlp
```

with a native weak factorization system through the explicit small-object route.

### Generated-presentation quotient and complete lattice

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

### Presentation incomparability and semantic information loss

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

This is a concrete motivation for the universality program: equality of an observable semantic slice need not imply equality of the underlying generated presentation.

### Fundamental-groupoid descent and obstruction

The integrated descent layer studies a finer transport

```text
S : P ⥤ Type
```

and a quotient toward an ordinary fundamental groupoid

```text
Q : P ⥤ FundamentalGroupoid Base.
```

A necessary descent compatibility requires fine transport to identify arrows identified by `Q`. Violations are packaged as descent obstructions. PR #1570 proves that quotient-kernel compatibility, obstruction, and descent existence are invariant under natural isomorphism of the fine transport presentation.

Ordinary `FundamentalGroupoid` remains the endpoint-fixed homotopy quotient / flat-like branch; it does not by itself construct arbitrary curvature-sensitive smooth connection transport.

## Active formal-validation frontier

PR #1558 is intentionally separate from canonical theorem advancement.

The current stacked validation line is exercising later scaled-simplicial certificates in addition to the original coherent-model compatibility problem. The active proof engineering includes the standard Type-A endpoint / boundary-prism route in which the target map is represented by **one ℕ-indexed transfinite composition** obtained by prefixing a literal opposite-endpoint Type-A cell to the alternating boundary-prism sequence.

The intended certificate surface includes the Type-A endpoint cellularity/stability/lifting route without replacing it by an arbitrary binary-composition shortcut.

This work remains subject to the validation boundary:

```text
PR #1558 = validation-only
Draft = true
merge = forbidden
Ready-for-review = forbidden
auto-merge = forbidden
CI result = compatibility evidence only
```

Successful validation may justify a later clean theorem-preserving port onto a canonical development branch. It never makes PR #1558 itself mergeable authority.

## Candidate axioms for the universality program

The following are research targets, not yet a final axiom system.

```text
DO1  Contextuality
     state / meaning is indexed by context.

DO2  Functorial transport
     admissible context changes induce composable transport.

DO3  Higher coherence
     comparison data between transports is coherently compatible.

DO4  Presentation invariance
     justified equivalent presentations preserve intrinsic semantics.

DO5  Descent
     compatible local contextual data admits justified global realization.

DO6  Obstruction
     failure of descent is represented internally rather than silently erased.

DO7  Non-reification
     no selected presentation is promoted to intrinsic substance merely because
     it is convenient, canonical, executable, or observable.
```

A major objective is to minimize these assumptions, determine independence/redundancy, and derive the universal construction from the smallest mathematically natural package.

## Adaptive Retrieval — integrated AI realization layer

KuuOS now has an explicit bounded retrieval-selection subsystem.

```text
R0  lexical
R1  lexical + bounded rewrite
R2  semantic on demand
R3  hybrid lexical + semantic
R4  pre-embedded semantic retrieval
R5  bounded relational / GraphRAG
```

The formal and runtime invariant is:

```text
selected mode = least complex mode explicitly assessed as adequate
```

The selector does **not** decide empirical adequacy by itself. Adequacy must come from deployment evidence, measurement, evaluation, or policy. If adequacy is unknown, the runtime fails closed. If every mode is explicitly inadequate, the correct route is `NO_DATA` with an explicit next-observation target.

The Lean contract in `formal/KUOS/Retrieval/AdaptiveRetrievalPolicyV0_1.lean` proves, among other things, that a least-sufficient selection is adequate, that every strictly simpler mode is inadequate, and that relational/GraphRAG selection requires all simpler modes to be inadequate.

Every retrieval authority boundary denies truth, WORLD-commit, belief, decision, execution, clinical, and theorem authority.

```text
retrieval score != entailment
embedding similarity != semantic proof
index freshness != source freshness
vector database != WORLD model
GraphRAG != global ontology
retrieved evidence != verified evidence
selection != execution
```

See:

```text
docs/KUUOS_ADAPTIVE_RETRIEVAL_POLICY_v0_1.md
docs/AdaptiveRetrieval/README.md
runtime/kuuos_adaptive_retrieval_policy_v0_1.py
formal/KUOS/Retrieval/AdaptiveRetrievalPolicyV0_1.lean
```

Adaptive Retrieval is a concrete AI realization target for the dependent-origination program: retrieval mechanisms are treated as context-dependent presentations, while presentation invariance, evidence descent, contradiction/obstruction, and non-reification remain explicit research questions.

## AI research direction

The AI connection is a research program, not a claim that current AI systems satisfy the final dependent-origination axioms.

A future agent can be modeled schematically by contextual transports among observation, retrieval, memory, world-model, tool, goal, plan, and action contexts. Under this view:

- model/embedding/prompt/index changes become candidate changes of presentation;
- invariant semantics should survive justified equivalences of representation;
- memory integration becomes a descent/gluing problem over partial observations;
- contradictory memories, retrievals, or tool evidence can appear as descent obstructions;
- multi-agent agreement may require higher coherence rather than simple aggregation;
- hallucination can be investigated, in part, as local plausibility without justified global realization;
- interoperability can be formulated around relational behavior and transport invariants rather than shared latent coordinates.

The long-term AI question is:

> Can intelligence be characterized partly as the ability to move coherently among contexts while preserving justified invariants, detecting obstruction, and refusing unjustified promotion from local evidence to global truth?

KuuOS runtime governance already enforces a weaker operational form:

```text
candidate != authority
observation != verification
retrieval != truth
host success != WORLD truth
plan execution != PlanOS completion
receipt != successor authority
selection != execution.
```

## Current mathematical frontier

The immediate theorem program is organized toward universality rather than toward one more privileged presentation.

1. **Complete current Lean 4.31 validation without changing theorem authority.** PR #1558 remains validation-only and must not be merged.
2. **Finish the literal Type-A endpoint/full-transfinite route in the validation line.** Keep the endpoint cell, boundary-prism sequence, and whole map in one explicit transfinite-composition construction.
3. **Close coherent round-trip horn descent.** Derive horn-filler invariance from coherent bicategorical equivalence where possible rather than assuming redundant certificate data.
4. **Complete the descent characterization.** Strengthen quotient-kernel compatibility toward necessary-and-sufficient descent criteria under explicit hypotheses.
5. **Package semantic information loss.** Separate faithful full-right semantics from terminal restriction and characterize the fibrant-object semantic quotient without calling it a localization before proving a universal property.
6. **Extract minimal dependent-origination axioms.** Determine which current theorems follow from contextuality, coherence, invariance, descent, obstruction, and non-reification.
7. **Construct `DO(C,W,J,H)`.** Identify the correct categorical level and build a carrier that can support the mapping property.
8. **Prove the representation/universality theorem.** Establish factorization, essential uniqueness, naturality, and uniqueness of the universal carrier up to the appropriate equivalence.
9. **Develop realizations.** Relate the universal structure to gauge/groupoid transport, smooth/thin-path geometry, process theory, probability, quantum structures, adaptive retrieval, memory, and AI agents without collapsing specializations into the parent definition.

See `ROADMAP.md` for theorem-sized milestones and exit criteria.

## Runtime and control plane

Canonical effect-free repository check:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The runtime architecture includes bounded observation/verification, PlanOS, DecisionOS, MemoryOS, CodeAI, GitHub MCP durable reentry, OpenClaw integration, dependent-origination adapters, and Adaptive Retrieval.

OpenClaw remains explicitly bounded:

```text
OpenClaw = execution host + observation source
OpenClaw != truth authority
OpenClaw != WORLD commit authority
OpenClaw != automatic PlanOS completion
OpenClaw != automatic rollback proof
OpenClaw != automatic memory overwrite authority.
```

Adaptive Retrieval is bounded in the same style:

```text
retrieval mode selection = presentation choice
retrieval mode selection != source truth
retrieval mode selection != belief commit
retrieval mode selection != decision authority
retrieval mode selection != execution authority.
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

The Lean 4 compatibility/review program therefore has a precise role: successful independent reconstruction establishes reproducible machine checking of the formal theorem surface under the reviewed toolchain and assumptions. It does not prove that philosophical dependent origination is uniquely captured by the chosen semantics.

## Repository development invariants

Normal development uses exact-base branches and PR-based review. Formal proof work remains no-`sorry`, no-`admit`, no new `axiom`, and no placeholder constants used as theorem authority. Frozen boundaries remain append-only/tighten-only where specified, with same-root requirements preserved.

CI is terminal evidence only after the relevant workflow, jobs, exact Lean step, dependency/manifest checks, and governance evidence are completed successfully. `queued` / `in_progress` is never success evidence. Exact-head CI execution implies write-freeze for that proof head.

Validation-only PRs marked non-mergeable remain non-mergeable even if their CI becomes fully green.

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

retrieval score != entailment
embedding similarity != semantic proof
GraphRAG != global ontology
retrieved evidence != verified evidence

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
| Adaptive Retrieval | least-sufficient bounded selector v0.1 | `docs/AdaptiveRetrieval/README.md` |
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
| Lean 4.31 validation | validation-only stacked Draft PR #1558 | non-canonical compatibility evidence |
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

KuuOS is a research architecture. Its formal mathematics, runtime governance, retrieval systems, physical specializations, and AI applications have different authority boundaries.

The strongest long-term claim is deliberately still open:

> Under mathematically natural conditions, contextual relational systems may admit a universal dependent-origination characterization.

The repository has progressed far enough to make that a concrete formal research program, but not far enough to call it a proved representation theorem. The next phase is therefore not to multiply metaphors of 縁起, but to prove exactly **which contextual/coherent/descent structure is universal, under what hypotheses, and up to what equivalence**.
