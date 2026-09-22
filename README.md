# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophy, mathematical presentations, formal proofs, and operational systems inform one another without being treated as interchangeable evidence.

## Canonical snapshot — 2026-09-22 JST

| Item | Verified reference |
| --- | --- |
| Canonical branch | `main` |
| Latest integrated theorem layer | **v3.30 — quotient-representative directional closure** |
| Latest theorem-bearing merge | [PR #1706](https://github.com/itakura-hidetoshi/KuuOS/pull/1706), merged 2026-09-22 |
| Theorem baseline; `main` at observation | `1b4cf22eb8e8b5ffc70c490093534ff95ff2a081` |
| Validated #1706 PR head | `0c2ead10cc002150d47f3e0ba7a4e5da65b3db88` |
| Exact-head governance run | [Gate #2523 / run 35679072189](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35679072189), completed / success |
| Exact-head receipts | Strict Lean formal validation = success; exact-head terminal = success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

This is a dated snapshot, not a permanently current branch pointer. Later **documentation-only** commits may advance `main` without advancing the theorem baseline. Re-observe GitHub before continuing work. The source of the latest result is [the v3.30 Lean module](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean).

Authority order is:

```text
fresh exact canonical GitHub SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > CI and runtime receipts
  > history / memory
```

The formerly separate v2.69–v3.14 frontier was integrated by [PR #1651](https://github.com/itakura-hidetoshi/KuuOS/pull/1651). It is historical promotion provenance, **not the current Draft frontier**. The higher-localization spine now continues through v3.30 on `main`.

## What 空 means here

空 is not interpreted as “nothing exists.” Its role is non-reification: a useful contextual presentation need not be an intrinsic substance or the only legitimate presentation.

```text
chosen presentation != intrinsic substance
local observation != global truth
retrieval score != entailment
runtime success != WORLD truth
formal encoding != unique philosophical interpretation
model generation != theorem authority
```

The bridge from 空 to 縁起 retains context, relations, admissible transport, higher coherence, descent, obstruction, and correction authority. KuuOS keeps interpretive connections to Madhyamaka, Yogācāra, Huayan, Tiantai, 陰陽, 五行, 道, 理・気, 礼, and 天人相関 without silently identifying them with one formalism.

The philosophical layer asks about relation, dependence, transformation, and non-reification. The mathematical layer studies those questions through categories, bicategories, pseudofunctors, localization, gauge freedom, holonomy, descent, and universal properties. The operational layer applies bounded observation, planning, action, and renewed verification. These are related layers, not a ranking of philosophical and mathematical authority.

## Latest result: from actual representative words to mixed-triangle closure

Let `R` be the raw Cat-valued higher contextual system and `D` its pointwise chosen W-adjoint-equivalence data. The representative evaluation is fixed by the existing construction:

```text
quotientRepresentativeMap W R D f
  = (freePathEvaluator W R D).map (Quot.out f).
```

For composable quotient arrows `f : X ⟶ Y` and `g : Y ⟶ Z`, v3.30 inspects **only the ordinary letters occurring in their chosen representative words**:

```text
ordinary letters in Quot.out f evaluate to essentially-surjective functors
ordinary letters in Quot.out g evaluate to faithful functors
```

Formal W-inverse letters need no additional directional assumption: `D` evaluates them as inverse functors of chosen equivalences. The new `PathEdgesSatisfy` inductive predicate carries edge-by-edge evidence; induction on that evidence propagates the relevant property through the finite word.

The precise sufficient route is:

```text
QuotientRepresentativeOrdinaryEssSurj W R f
+ QuotientRepresentativeOrdinaryFaithful W R g
    |
    v
(quotientRepresentativeMap W R D f).toFunctor.EssSurj
+ (quotientRepresentativeMap W R D g).toFunctor.Faithful
    |
    v
MiddleIdentityWhiskerSeparating W R D f g
```

Essential surjectivity on the left means that every middle-fiber object is reached up to isomorphism; faithfulness on the right means that equality of morphisms can be reflected back. Neither outer functor is required to be an equivalence.

This closes the particular incidence triangle

```text
anchor:         associator f (𝟙 Y) g
right endpoint: rightUnitor f
left endpoint:  leftUnitor g
```

**provided** its three local gauges satisfy their actual correction equations and each endpoint agrees with the anchor on their shared footprint. Under those hypotheses, the two endpoints agree on their full shared footprint.

Main v3.30 declarations:

```text
freePathEvaluator_map_essSurj_of_pathEdges
freePathEvaluator_map_faithful_of_pathEdges
quotientRepresentativeMap_essSurj_of_representative_ordinary
quotientRepresentativeMap_faithful_of_representative_ordinary
middleIdentityWhiskerSeparating_of_representative_words
associatorAnchor_unitor_overlapStar_triangle_of_representative_words
```

These are **sufficient, representative-word conditions**. The theorem does not claim that every quotient arrow satisfies them, that failure of a word condition proves an obstruction, or that closing this one triangle yields a globally compatible correction family.

## Canonical formal spine

The earlier layers remain part of the program, not superseded claims of a completed universal object.

| Layers | Established role |
| --- | --- |
| v2.0–v2.10 | Ordinary localization, W + J sectors, stack descent, and the higher-localization factorization interface. |
| v2.11–v2.54 | Weak/coherent distinctions, correction and modification triangles, the E/R/A obstruction normal form, and structural sufficient routes. |
| v2.55–v2.68 | Restricted existence, W-adjoint equivalences, free-path evaluation, quotient-equal path isomorphisms, the five-law coherence package, generated 2-cells and holonomy. |
| v2.69–v2.95 | Octahedral truth test; obstruction, correctability, authority, extensional correction power, and constructive/classical boundaries. |
| v2.96–v3.04 | Correction returns to exact factorization: five compatible gauge equations split into three quotient equations and two comparison equations. |
| v3.05–v3.14 | Quotient correction loci, witness-correlation gap, finite dependent-coordinate footprints, and literal shared-coordinate keys. |
| v3.15–v3.21 | Explicit pair extension and global gluing from one compatible family; abstract correlation countermodels; rigidity, normalization, and star-transitivity sufficient criteria. |
| v3.22–v3.30 | Actual route-equation rigidity, mixed-triangle residual, directional cancellation, finite-path propagation, and the `Quot.out` word bridge. |

### Holonomy, correction, and factorization

The retained v2.68 sufficient route is:

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R.
```

The v2.69 countermodel shows that weak W-admissibility does **not** force this holonomy-triviality hypothesis. It does **not** show that factorization is impossible. The subsequent correction theory returns to the exact factorization interface rather than treating nontrivial holonomy as automatic failure.

At the quotient stage, a gauge consists of the dependent `gId/gComp` families. The comparison family `gIso` belongs to the subsequent two-equation comparison lift.

### Gluing results already closed, and the gap that remains

[v3.15](formal/KUOS/DependentOriginationPairwiseFiniteExtensionV3_15.lean) constructs a common extension of two actual quotient gauges from literal shared-coordinate agreement:

```text
AgreeOnRouteFootprintOverlap
  <-> CompatibleOnRouteOverlap.
```

[v3.16](formal/KUOS/DependentOriginationGlobalFootprintGluingV3_16.lean) constructs the global coordinate patch once **one simultaneous, pairwise-compatible correcting family** is supplied:

```text
HasFiniteFootprintAmalgamation
  <-> HasGloballyCompatibleLocalCorrectionFamily.
```

Classical footprint decisions and coordinate selectors are explicit. Neither result imports compactness, convexity, topology, or a Helly principle.

The remaining distinction is between witnesses that may depend on the chosen anchor and one family compatible for every pair at once. The [v3.17 finite Boolean countermodel](formal/KUOS/DependentOriginationPairwiseCorrelationCountermodelV3_17.lean) refutes the upgrade from nested pairwise witnesses by logic alone. [v3.21](formal/KUOS/DependentOriginationCylinderLocalityCountermodelV3_21.lean) shows that footprint-cylinder locality alone does not repair it. These are **abstract finite-footprint countermodels**, not a constructed failure of factorization for an actual KuuOS raw system.

v3.18–v3.20 supply conditional routes through shared-coordinate rigidity, an overlap-preserving gauge-fixing normalizer, or overlap-star transitivity. The task is to derive suitable structure from actual route equations, not assume the global compatibility sought.

### Actual route equations: v3.22–v3.30

| Layer | Result and scope |
| --- | --- |
| [v3.22](formal/KUOS/DependentOriginationUnitorPartialRigidityV3_22.lean) | Within a corrected unitor locus, fixing the identity gauge fixes its composition gauge. |
| [v3.23](formal/KUOS/DependentOriginationAssociatorThreeOfFourRigidityV3_23.lean) | One proved three-of-four orientation: equality at `(f,g)`, `(g,h)`, and `(f,g ≫ h)` forces equality at `(f ≫ g,h)`. It is not a blanket assertion of every orientation. |
| [v3.24](formal/KUOS/DependentOriginationUnitorStarTransitivityV3_24.lean) | Homogeneous unitor stars close with the actual common-identity incidence: same-source left unitors or same-target right unitors. |
| [v3.25](formal/KUOS/DependentOriginationMixedUnitorRigidityV3_25.lean) | Mixed left/right unitor overlap closes once the shared identity gauge agrees, including the identity/identity composition overlap. |
| [v3.26](formal/KUOS/DependentOriginationAssociatorUnitorTriangleResidualV3_26.lean) | The mixed associator/unitor equations force double-whiskered equality. Literal middle-identity equality follows under injectivity of that action. |
| [v3.27](formal/KUOS/DependentOriginationAssociatorUnitorWEdgeSeparationV3_27.lean) | Outer representative equivalences give injectivity; images of raw W-arrows supply a concrete automatic sector. |
| [v3.28](formal/KUOS/DependentOriginationAssociatorUnitorOneSidedSeparationV3_28.lean) | The sufficient criterion requires only left essential surjectivity and right faithfulness. |
| [v3.29](formal/KUOS/DependentOriginationFreePathDirectionalPropagationV3_29.lean) | Generator-level directional properties propagate through finite free paths. Ordinary and formal-inverse generators are separated explicitly. |
| [v3.30](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean) | Conditions are localized to ordinary letters of the actual selected `Quot.out` words and connected to mixed-triangle closure. |

In v3.26, with `F` and `G` the outer representatives, the action is

```text
Phi(eta) = F ◁ (eta ▷ G).
```

The unconditionally derived equality is an equality **after** this action, under the stated local correction and anchor-overlap hypotheses. The residual concerns injectivity of `Phi`; no extra linear structure is being assumed by calling it a kernel relation.

## Next mathematical boundary

The immediate work after v3.30 has two distinct levels:

**Syntactic certificates.** Does the ordinary-letter predicate survive changing a representative by `id`, `comp`, `Winv₁`, or `Winv₂`? Track both directions of a relation; do not infer a property of each factor merely from a property of its composite.

**Semantic evaluation.** Use the existing v2.58 isomorphism between evaluations of quotient-equal paths to formulate representative-independent directional criteria. A useful next theorem can transfer a certificate from some suitable representative to the selected representative without claiming that every representative has the same letterwise certificate.

After that, enlarge the actual incidence sectors where correction witnesses correlate, build one globally compatible family, and discharge the comparison `gIso` equations. Failure of a sufficient certificate is not proof of a nontrivial double-whiskering kernel.

The following general targets remain open in this snapshot:

```text
IsHigherWAdmissible W R
  -> HasHigherLocalizationFactorization (W := W) R

IsHigherWAdmissible W R
  -> HasCoherentWeakHigherLocalizationUniversalProperty W R
```

Stage-I factorization, Stage-II coherent universality, Axes E/R, and the final representation theorem are different milestones. See [ROADMAP.md](ROADMAP.md) for their exit criteria.

## Dependent Origination Universality Program

The north star is an explicitly constructed carrier, schematically

```text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X),
```

with the correct higher variance, factorization, essential uniqueness, naturality, descent compatibility, and presentation invariance. Here `C` is the context carrier, `W` specifies intended equivalences, `J` the descent data, and `H` the higher-coherence data.

**The final universal object and representation theorem are not yet proved.** A localization, quotient, stackification, or semantic reduction is not promoted to that object without its mapping property.

## AI and operational realization

The same distinctions guide bounded systems engineering:

```text
model / prompt / index migration -> presentation transport
partial memory integration      -> compatibility and descent
contradictory evidence           -> explicit obstruction
multi-agent coordination        -> higher coherence
different remediation powers    -> authority-relative correction
```

These are engineering interpretations and design directions, not deployment guarantees established by the Lean theorems. Local agreement must not be confused with a single globally correlated family of decisions. Whether a discrepancy is hard also depends on the corrections actually authorized.

The runtime architecture includes bounded observation and verification, PlanOS, DecisionOS, MemoryOS, CodeAI, GitHub MCP reentry, dependent-origination adapters, and Adaptive Retrieval. Its control route is:

```text
observe -> represent -> retrieve -> plan -> decide -> act -> re-observe -> verify
```

Adaptive Retrieval retains the least-sufficient policy:

```text
R0 lexical; R1 lexical + bounded rewrite; R2 semantic on demand;
R3 hybrid; R4 pre-embedded semantic; R5 bounded relational / GraphRAG.
```

Choose the least complex mode explicitly assessed as adequate. Unknown adequacy fails closed; explicit inadequacy across all modes yields `NO_DATA` and a next-observation target. Retrieval, entailment, execution, and authority remain separate.

## Reproduction and verification

The pinned environment is recorded in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json). The focused v3.30 target is:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30
```

The aggregate formal target can be checked separately:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

A focused target receipt is not a claim that a fresh aggregate build was run. The effect-free runtime entry point is:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a mathematical theorem. A CI receipt applies to its exact head and recorded selection. A PR synthetic merge SHA in a build receipt must not be mistaken for the PR's working head. Queued or running checks are not success.

## Development and authority boundaries

PR **#1558** is the separate **validation-only Lean 4.31 line**. Its standing policy remains: no merge, no Ready for review, and no auto-merge; compatibility evidence is not canonical theorem advancement. This documentation update does not change that policy.

```text
no sorry / admit / placeholder theorem authority
no new axiom substituted for the target theorem
no silent assumption weakening or carrier identification
no Classical.choice => coherence inference
no stale-head CI promoted to current-head success
fresh canonical verification after merge
```

```text
same quotient arrow != same retained 2-cell derivation
local Nonempty Iso != a coherent choice of transports
pointwise inverses != pseudofunctor coherence
nontrivial generated holonomy != factorization impossible
abstract correlation countermodel != an actual-system counterexample
word certificate != necessary semantic criterion
one closed incidence triangle != global star transitivity
Stage-I factorization != Stage-II universality
execution host != truth, WORLD-commit, or memory-overwrite authority
```

**Current research sentence:** KuuOS has carried actual mixed associator/unitor correction from a double-whiskering residual to a checked, path-local sufficient criterion on the chosen quotient words. The next step is representative-independent directional reasoning and broader witness correlation, followed by the comparison lift and higher universal-property program.
