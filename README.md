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
| Latest integrated theorem layer | **v3.33 — quotient split directional separation** |
| Latest theorem-bearing merge | [PR #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710), merged 2026-09-22 |
| Theorem baseline | `d5747268c38fef1b24ad7e9b5fa5fb3bf7c11455` |
| Post-#1710 `main`, observed before this docs refresh | `d5747268c38fef1b24ad7e9b5fa5fb3bf7c11455` |
| Validated #1710 PR head | `ba17572f2058819cd084d14dd31ac8678b446a3d` |
| Exact-head governance run | [Gate #2532 / run 35690347773](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35690347773), completed / success |
| Exact-head receipts | Strict Lean formal validation = success; exact-head terminal = success |
| CI checkout, not final merge | `e345655b329d34f8aab88778a75e582ea33747e7` — synthetic merge of the validated head with the v3.32 base |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

This is a dated snapshot, not a permanently current branch pointer. This **documentation-only** refresh can advance `main` without advancing the theorem baseline. Re-observe GitHub before continuing work. The latest result is [the v3.33 Lean module](formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean), building on the integrated [v3.31 representative transport](formal/KUOS/DependentOriginationQuotientDirectionalPropertyTransportV3_31.lean) and [v3.32 certified-sector algebra](formal/KUOS/DependentOriginationCertifiedQuotientSectorClosureV3_32.lean).

Authority order is:

```text
fresh exact canonical GitHub SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > CI and runtime receipts
  > history / memory
```

The formerly separate v2.69–v3.14 frontier was integrated by [PR #1651](https://github.com/itakura-hidetoshi/KuuOS/pull/1651). It is historical promotion provenance, **not the current Draft frontier**. The higher-localization spine now continues through v3.33 on `main`; #1708, #1709, and #1710 are integrated theorem history, not pending proof candidates.

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

## Latest result: semantic directional separation from one-sided inverses

Fix a raw Cat-valued higher contextual system `R` and pointwise W-adjoint-equivalence data `D`. Write

```text
E(f) = (quotientRepresentativeMap W R D f).toFunctor,

quotientRepresentativeMap W R D f
  = (freePathEvaluator W R D).map (Quot.out f).
```

For quotient arrows `f : X ⟶ Y` and `g : Y ⟶ Z`, v3.33 proves the following sufficient route using equations in the **actual localization**:

```text
s : Y ⟶ X,  s ≫ f = 𝟙 Y       r : Z ⟶ Y,  g ≫ r = 𝟙 Y
              |                              |
              v                              v
          E(f).EssSurj                    E(g).Faithful
                         |
                         v
       MiddleIdentityWhiskerSeparating W R D f g
```

Thus a split epimorphism on the left and a split monomorphism on the right suffice. No ordinary-letter certificate on `f`, `g`, their one-sided inverses, or their selected `Quot.out` words is required by this criterion. Neither outer evaluation is required to be an equivalence.

The proof uses the existing v2.61 local identity/composition isomorphisms and Mathlib transport of properties of naturally isomorphic functors. It proves semantic identity and composition laws, followed by **directional reflection**:

```text
E(f ≫ g).EssSurj   -> E(g).EssSurj
E(f ≫ g).Faithful  -> E(f).Faithful.
```

The directions are not reversed. These do not assert that every factor or every ordinary letter inherits the property. The local isomorphisms are used inside proofs of propositions; no coherent family of transports is selected, and no strict functor law `E(f ≫ g) = E(f) ⋙ E(g)` is asserted.

### The actual mixed triangle, with all its hypotheses

The separation result closes the particular incidence triangle

```text
anchor:         associator f (𝟙 Y) g
right endpoint: rightUnitor f
left endpoint:  leftUnitor g
```

**provided** three gauges `Qs`, `Qt`, `Qu` satisfy their respective corrected route equations, and `Qs` agrees with each endpoint gauge on the corresponding anchor overlap. Under those three correction hypotheses and two anchor-agreement hypotheses, `Qt` and `Qu` agree on the full endpoint overlap. The one-sided inverse equations do not construct those correcting gauges.

Main v3.33 declarations include:

```text
quotientRepresentativeMap_comp_essSurj_iff
quotientRepresentativeMap_comp_faithful_iff
quotientRepresentativeMap_essSurj_right_of_comp
quotientRepresentativeMap_faithful_left_of_comp
quotientRepresentativeMap_essSurj_of_section
quotientRepresentativeMap_faithful_of_retraction
middleIdentityWhiskerSeparating_of_section_retraction
associatorAnchor_unitor_overlapStar_triangle_of_section_retraction
```

## From representative words to quotient-level properties: v3.30–v3.33

Three levels must be distinguished: a certificate on a particular word, existence of at least one certified representative, and the semantic property of the evaluated functor.

| Layer | Proved contribution |
| --- | --- |
| [v3.30](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean) | `PathEdgesSatisfy` certificates on the ordinary letters of the actual `Quot.out` words imply the directional evaluation properties and mixed-triangle closure. |
| [v3.31](formal/KUOS/DependentOriginationQuotientDirectionalPropertyTransportV3_31.lean) | Quotient-equal paths have equivalent EssSurj/Faithful evaluation properties. Existence of one suitable representative suffices, even when the selected word has no supplied letterwise certificate. |
| [v3.32](formal/KUOS/DependentOriginationCertifiedQuotientSectorClosureV3_32.lean) | Each existence-certificate class contains identities, is closed under composition, and is the least multiplicative morphism property containing the corresponding certified generator images. |
| [v3.33](formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean) | Semantic EssSurj/Faithful classes are multiplicative and contain the certified classes; directional reflection gives the one-sided-inverse separation criterion. |

Formal W-inverse letters need no additional directional assumption: `D` evaluates them as inverse functors of chosen equivalences. Ordinary letters carry the corresponding raw evaluation condition.

For fixed `W`, `R`, `D`, v3.31 reuses `equalInLocalization_hasEvaluationIso` from v2.58 to transfer EssSurj and Faithful in both directions between evaluations of quotient-equal paths. `Nonempty Iso` is eliminated locally into a proposition. This settles semantic representative invariance, **not invariance of each letterwise certificate**, and does not by itself prove independence of all auxiliary choices such as `D`.

The v3.31 conditions are `HasOrdinaryEssSurjRepresentative` and `HasOrdinaryFaithfulRepresentative`. Their definitions contain no choice of `D` or `Quot.out`. In v3.32 the generic construction even permits an arbitrary relation on a path category: witness paths concatenate, so the letterwise predicate need not itself descend through that relation. For every multiplicative property `S`, containment is characterized by the generator test

```text
certifiedQuotientSector r P ≤ S
  <-> every P-certified generator has its quotient image in S.
```

In v3.33, `quotientEssSurjSector W R D` and `quotientFaithfulSector W R D` are the corresponding **semantic** morphism properties. The two `certified..._le_quotient...Sector` theorems establish containment. Equality or strict containment of these classes has not been established by these modules. Nor is the split criterion proved equivalent to membership in a certified class.

All these are sufficient routes to separation. Failure to supply a certificate, failure of a directional property, or absence of a one-sided inverse is not a noninjectivity witness.

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
| v3.31–v3.33 | Semantic representative invariance, multiplicative certified and semantic classes, directional reflection, and split-arrow mixed-triangle closure. |

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

### Actual route equations: retained v3.22–v3.30 results

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

The initially derived equality is an equality **after** this action, under the stated local correction and anchor-overlap hypotheses. The residual concerns injectivity of `Phi`; no extra linear structure is being assumed by calling it a kernel relation.

## Next mathematical boundary

The former ROADMAP targets **N1b** (semantic transfer between quotient-equal paths) and **N2** (one suitable representative) are now proved by v3.31; v3.32 supplies identity/composition closure and minimality of the certified classes. They must not be reopened as missing constructions. v3.33 advances **N3** with a further semantic separation criterion, but does not settle the entire remaining separation boundary.

The next work is to characterize the remaining actual cancellation/detection sectors, or construct genuine noninjectivity witnesses; then correlate correcting witnesses using the incidence geometry, reuse the v3.15/v3.16 gluing constructions, and discharge the comparison `gIso` equations. Relation-level behavior of the **syntactic** letterwise certificates (former N1a) remains a separate question, not a prerequisite for the semantic transport already proved.

The following general targets remain open in this snapshot:

```text
IsHigherWAdmissible W R
  -> HasHigherLocalizationFactorization (W := W) R

IsHigherWAdmissible W R
  -> HasCoherentWeakHigherLocalizationUniversalProperty W R
```

Stage-I factorization, Stage-II coherent universality, Axes E/R, and the final representation theorem are different milestones. See [ROADMAP.md](ROADMAP.md) for the updated exit criteria.

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

The pinned environment is recorded in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json). The focused v3.33 target is:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
```

The recorded #2532 run built this target and its dependencies, reported `Build completed successfully (8457 jobs).` with return code `0`, and passed the dependency-manifest check. Historical imported-module linter warnings remain; this is not a claim of repository-wide warning elimination.

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

A runtime result is not a mathematical theorem. A CI receipt applies to its exact head, base/checkout and recorded selection. A PR synthetic merge SHA in a build receipt is neither the PR's working head nor the final merge commit. Queued or running checks are not success. A docs-only gate does not add a new Lean validation.

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
word certificate is sufficient, not a proved necessary semantic criterion
certified-sector containment does not establish equality or strictness
one closed incidence triangle != global star transitivity
Stage-I factorization != Stage-II universality
execution host != truth, WORLD-commit, or memory-overwrite authority
```

**Current research sentence:** KuuOS now transports directional evaluation properties across quotient representatives, gives both certified and semantic classes a multiplicative algebra, and closes the actual mixed associator/unitor triangle under explicit split-arrow conditions and its original correction hypotheses. The next boundary is broader actual separation and simultaneous witness correlation, followed by the comparison lift and higher universal-property program.
