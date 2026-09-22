# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophy, mathematical presentations, formal proofs, and operational systems inform one another without being treated as interchangeable evidence.

## Current status — 2026-09-22 JST

**Integrated on `main`: v3.32. Validated but not integrated: v3.33 / PR #1710, still Draft/open/unmerged.** This documentation refresh does not merge the theorem PR or change any Lean source.

| Item | Verified reference |
| --- | --- |
| Canonical branch | `main` |
| Latest integrated theorem layer | **v3.32 — certified quotient sector closure and minimality** |
| Latest theorem-bearing merge | [PR #1709](https://github.com/itakura-hidetoshi/KuuOS/pull/1709) |
| Mathematical baseline; main before this docs refresh | `c59c7aa4e6435a2172344dfaf2843937a86a89d8` |
| Validated #1709 PR head | `47da65d74fcd062b10f8bcbea8954e0e800a3cfc` |
| v3.32 validation | [Gate #2530 / run 35687280701](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35687280701), completed/success; Strict Lean and exact-head terminal receipts both success |
| Validated, unmerged theorem layer | **v3.33 — quotient split directional separation**, [PR #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710) |
| Validated #1710 PR head | `ba17572f2058819cd084d14dd31ac8678b446a3d` |
| v3.33 validation | [Gate #2532 / run 35690347773](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35690347773), completed/success; Strict Lean and exact-head terminal receipts both success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

This is a dated snapshot, not a permanently current branch pointer. Documentation-only commits can advance `main` without advancing the mathematical baseline. A successful PR check does not put that PR's declarations on `main`. The v3.33 source is therefore linked at its [validated exact head](https://github.com/itakura-hidetoshi/KuuOS/blob/ba17572f2058819cd084d14dd31ac8678b446a3d/formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean), not as a main-branch file.

Authority order:

```text
fresh exact canonical GitHub SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > CI and runtime receipts
  > history / memory
```

The former v2.69–v3.14 frontier was integrated by [PR #1651](https://github.com/itakura-hidetoshi/KuuOS/pull/1651). It is historical promotion provenance, not a current unmerged Draft. The separate Lean 4.31 validation-only PR #1558 remains outside the canonical theorem line.

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

## Latest canonical results: one good representative and its composition algebra

Let `R` be the raw Cat-valued higher contextual system and `D` its pointwise chosen W-adjoint-equivalence data. The existing representative evaluation remains

```text
quotientRepresentativeMap W R D f
  = (freePathEvaluator W R D).map (Quot.out f).
```

This definition alone does not make the selected evaluation a coherent pseudofunctor.

### v3.31 — semantic transport and existence of a certified representative

[Source on main](formal/KUOS/DependentOriginationQuotientDirectionalPropertyTransportV3_31.lean) · [merged PR #1708](https://github.com/itakura-hidetoshi/KuuOS/pull/1708)

For fixed `W`, `R`, and `D`, v2.58 already supplies `Nonempty Iso` between evaluations of paths equal in the localization. v3.31 uses that isomorphism locally to prove both equivalences:

```text
[p] = [q]
  -> (EssSurj(eval p) <-> EssSurj(eval q))
  -> (Faithful(eval p) <-> Faithful(eval q)).
```

Here the two conclusions are separate consequences of the same quotient equality. No coherent family of isomorphisms is selected by this proposition-valued transport.

The sufficient conditions are now **existence of one suitable representative**, rather than conditions on the particular `Quot.out` word:

```text
HasOrdinaryEssSurjRepresentative W R f
  := there exists p representing f whose ordinary letters evaluate to EssSurj functors

HasOrdinaryFaithfulRepresentative W R g
  := there exists q representing g whose ordinary letters evaluate to Faithful functors.
```

Formal W-inverse letters require no extra directional assumption: their evaluations are inverse functors of the equivalences supplied by `D`. v3.30's inductive `PathEdgesSatisfy` evidence propagates the ordinary-letter conditions through each witness path. v3.31 then transports the resulting semantic property to the actual selected representative.

Consequently:

```text
one EssSurj-certified representative of f
+ one Faithful-certified representative of g
    |
    v
(quotientRepresentativeMap W R D f).toFunctor.EssSurj
+ (quotientRepresentativeMap W R D g).toFunctor.Faithful
    |
    v
MiddleIdentityWhiskerSeparating W R D f g.
```

The existential certificates contain no choice of `D` or `Quot.out`. The evaluated functors still use `D`; independence of that additional choice is not asserted here. A certificate on `Quot.out` remains a special case, not a necessary condition.

### v3.32 — identity, composition, and generator-level minimality

[Source on main](formal/KUOS/DependentOriginationCertifiedQuotientSectorClosureV3_32.lean) · [merged PR #1709](https://github.com/itakura-hidetoshi/KuuOS/pull/1709)

For any relation `r` on a path category and any edge predicate `P`, define the quotient morphism property schematically by

```text
S_P(f) := exists p, quotient.map p = f and PathEdgesSatisfy P p.
```

Certified paths concatenate. The quotient functor preserves composition. Hence `S_P` contains identities and is closed under composition, with a Mathlib `MorphismProperty.IsMultiplicative` instance. This needs **no invariance of the letterwise predicate under the quotient relation**.

For every multiplicative morphism property `S`, v3.32 also proves the generator test:

```text
S_P <= S
  <-> every P-certified generator image belongs to S.
```

Thus `S_P` is the least multiplicative property containing those generator images. Specialization gives identity/composition closure and the same minimality test for both v3.31 existence-certificate sectors. Composing certified outer arrows preserves the sufficient double-whiskering separation criterion.

This is minimality of a generated certificate sector, **not** a characterization of all semantically EssSurj or Faithful evaluations. It does not give arbitrary-factor or inverse closure, and does not make a non-certified arrow a noninjectivity witness.

## Validated next layer: v3.33, not yet on main

[PR #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710) · [validated source at ba17572f](https://github.com/itakura-hidetoshi/KuuOS/blob/ba17572f2058819cd084d14dd31ac8678b446a3d/formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean)

The checked module moves from word certificates to semantic properties of quotient evaluations. For fixed `W`, `R`, and `D`, it proves that these semantic EssSurj/Faithful sectors contain identities, are closed under composition, and contain the corresponding certified sectors. It does not assert equality or strict containment of those sectors.

The local identity and composition isomorphisms from v2.61 also give **directional reflection**:

```text
EssSurj(eval(f ≫ g))  -> EssSurj(eval g)
Faithful(eval(f ≫ g)) -> Faithful(eval f).
```

These directions must not be reversed or applied to every letter of a representative word. In particular, for `f : X ⟶ Y`, `g : Y ⟶ Z`, a section and a retraction in the actual quotient give:

```text
s : Y ⟶ X,  s ≫ f = 𝟙 Y  -> EssSurj(eval f)
r : Z ⟶ Y,  g ≫ r = 𝟙 Y  -> Faithful(eval g)
                                  |
                                  v
             MiddleIdentityWhiskerSeparating W R D f g.
```

No word certificate or two-sided equivalence is required by this split criterion. The four original instance-synthesis errors were repaired by giving `Cat.Hom.toNatIso` explicit functor-level identity/composition endpoints before property transport. The corrected module has completed its focused validation; canonical integration remains a separate step.

## What the separation results close

For composable quotient arrows `f` and `g`, the actual incidence triangle is

```text
anchor:         associator f (𝟙 Y) g
right endpoint: rightUnitor f
left endpoint:  leftUnitor g.
```

The anchor shares `gComp(f,𝟙 Y)` with the right endpoint and `gComp(𝟙 Y,g)` with the left endpoint; the endpoints share `gId(Y)`.

v3.26 derives equality after the action

```text
Phi(eta) = F ◁ (eta ▷ G),
```

where `F` and `G` are the outer quotient representatives. `MiddleIdentityWhiskerSeparating` states injectivity of this action. No extra linear structure is assumed by referring to its kernel relation.

Under any proved sufficient separation criterion, the endpoint overlap closes **provided all three gauges satisfy their actual correction equations and both endpoint gauges agree with the anchor on their shared footprints**. Those five hypotheses are retained by the v3.30, v3.31, and validated v3.33 triangle theorems. Closing this triangle is not a theorem about all route stars or existence of one globally compatible correction family.

## Canonical formal spine

| Layers | Established role |
| --- | --- |
| v2.0–v2.10 | Ordinary localization, W + J sectors, stack descent, and the higher-localization factorization interface. |
| v2.11–v2.54 | Weak/coherent distinctions, correction and modification triangles, the E/R/A obstruction normal form, and structural sufficient routes. |
| v2.55–v2.68 | Restricted existence, W-adjoint equivalences, free-path evaluation, quotient-equal path isomorphisms, the five-law coherence package, generated 2-cells and holonomy. |
| v2.69–v2.95 | Octahedral truth test; obstruction, correctability, authority, extensional correction power, and constructive/classical boundaries. |
| v2.96–v3.04 | Correction returns to exact factorization: five compatible gauge equations split into three quotient equations and two comparison equations. |
| v3.05–v3.14 | Quotient correction loci, witness-correlation gap, finite dependent-coordinate footprints, and literal shared-coordinate keys. |
| v3.15–v3.21 | Pair extension and gluing from one compatible family; abstract correlation countermodels; rigidity, normalization, and star-transitivity sufficient criteria. |
| v3.22–v3.30 | Actual route-equation rigidity, mixed-triangle residual, directional cancellation, finite-path propagation, and the `Quot.out` word bridge. |
| v3.31 | Semantic EssSurj/Faithful transport between quotient-equal path evaluations; one good representative suffices for separation and the mixed triangle. |
| v3.32 | Certified quotient sectors contain identities, are composition-closed, and satisfy a generator-level minimality theorem. |

**v3.33 is intentionally not listed as canonical:** it is the validated, unmerged layer described above.

### Actual route-equation milestones retained

| Layer | Result and scope |
| --- | --- |
| [v3.22](formal/KUOS/DependentOriginationUnitorPartialRigidityV3_22.lean) | Within a corrected unitor locus, fixing the identity gauge fixes its composition gauge. |
| [v3.23](formal/KUOS/DependentOriginationAssociatorThreeOfFourRigidityV3_23.lean) | One three-of-four orientation: equality at `(f,g)`, `(g,h)`, and `(f,g ≫ h)` forces equality at `(f ≫ g,h)`, not automatically every orientation. |
| [v3.24](formal/KUOS/DependentOriginationUnitorStarTransitivityV3_24.lean) | Homogeneous unitor stars close with their actual common-identity incidence. |
| [v3.25](formal/KUOS/DependentOriginationMixedUnitorRigidityV3_25.lean) | Mixed left/right-unitor overlap closes when the shared identity gauge agrees. |
| [v3.26](formal/KUOS/DependentOriginationAssociatorUnitorTriangleResidualV3_26.lean) | Actual mixed-triangle equations yield double-whiskered equality; injectivity gives literal middle-identity equality. |
| [v3.27](formal/KUOS/DependentOriginationAssociatorUnitorWEdgeSeparationV3_27.lean) | Outer representative equivalences suffice; images of raw W-arrows provide a concrete sector. |
| [v3.28](formal/KUOS/DependentOriginationAssociatorUnitorOneSidedSeparationV3_28.lean) | Only left EssSurj and right Faithful are required for the sufficient cancellation argument. |
| [v3.29](formal/KUOS/DependentOriginationFreePathDirectionalPropagationV3_29.lean) | Generator-level directional properties propagate through finite free paths. |
| [v3.30](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean) | Ordinary-letter certificates on actual selected words connect to mixed-triangle closure. |

### Holonomy, correction, and gluing

The retained v2.68 sufficient route is

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R.
```

The v2.69 countermodel shows that weak W-admissibility does not force this holonomy-triviality hypothesis. It does not show that factorization is impossible. Subsequent correction theory returns to the exact factorization interface. Quotient gauges use dependent `gId/gComp` families; the later comparison lift uses `gIso`.

[v3.15](formal/KUOS/DependentOriginationPairwiseFiniteExtensionV3_15.lean) already constructs a common extension of two actual quotient gauges:

```text
AgreeOnRouteFootprintOverlap <-> CompatibleOnRouteOverlap.
```

[v3.16](formal/KUOS/DependentOriginationGlobalFootprintGluingV3_16.lean) already glues one simultaneously selected, pairwise-compatible correcting family:

```text
HasFiniteFootprintAmalgamation
  <-> HasGloballyCompatibleLocalCorrectionFamily.
```

The remaining issue is not the patching operation. It is obtaining one family compatible for all pairs, rather than witnesses that may depend on a chosen anchor. The [v3.17](formal/KUOS/DependentOriginationPairwiseCorrelationCountermodelV3_17.lean) and [v3.21](formal/KUOS/DependentOriginationCylinderLocalityCountermodelV3_21.lean) Boolean countermodels refute such an upgrade from abstract finite-footprint logic or footprint-cylinder locality alone. They are not actual-system factorization counterexamples. v3.18–v3.20 supply additional-structure sufficient routes; the actual route-equation program must justify the structure it uses.

## Next mathematical boundary

The former ROADMAP N1b and N2 tasks are no longer missing: **v3.31 solves quotient-equal evaluation-property transport and existence of one good representative; v3.32 adds identity/composition closure and minimality.** Letterwise certificate invariance is a separate syntactic question and was not needed for these results.

The immediate integration step is to re-observe #1710's head, base, and completed checks before promoting its validated v3.33 results. This docs-only update does not perform that promotion. Subsequent mathematical work concerns additional separating/detecting conditions or actual noninjectivity witnesses, simultaneous correction-witness correlation across the required incidence geometry, and the two comparison `gIso` equations.

The following general targets remain research goals:

```text
IsHigherWAdmissible W R
  -> HasHigherLocalizationFactorization (W := W) R

IsHigherWAdmissible W R
  -> HasCoherentWeakHigherLocalizationUniversalProperty W R.
```

Stage-I factorization, Stage-II coherent universality, Axes E/R, and the final representation theorem are distinct milestones. See [ROADMAP.md](ROADMAP.md) for completed units and the remaining exit criteria.

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

The pinned environment is recorded in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json). On the canonical v3.32 source tree, the latest focused target is:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCertifiedQuotientSectorClosureV3_32
```

The validated v3.33 target exists at #1710's exact head, not on main in this snapshot. In a checkout of `ba17572f2058819cd084d14dd31ac8678b446a3d`, run:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
```

The aggregate formal target is a separate check:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

The recorded focused receipts include their dependencies; they are not a claim of a fresh aggregate build or repository-wide warning elimination. Historical imported-module linter warnings remain. The effect-free runtime entry point is:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a mathematical theorem. CI receipts apply to their exact head and recorded selection. The v3.32/v3.33 workflows built synthetic merge checkouts `bd777d163db93a94712dc4f96a97407a389f850d` and `e345655b329d34f8aab88778a75e582ea33747e7`, respectively, and attached receipts to their PR heads. Neither synthetic SHA is a final merge commit. A docs-only CI success is not fresh Lean validation.

## Development and authority boundaries

PR **#1558** is the separate **validation-only Lean 4.31 line**. Its standing policy remains: no merge, no Ready for review, and no auto-merge. Compatibility evidence is not canonical theorem advancement.

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
some certified representative != every representative certified
word certificate != necessary semantic criterion
one closed incidence triangle != global star transitivity
validated PR head != integrated canonical theorem
Stage-I factorization != Stage-II universality
execution host != truth, WORLD-commit, or memory-overwrite authority
```

**Current research sentence:** KuuOS has integrated representative-independent directional certificates and their identity/composition/minimality algebra through v3.32. The validated v3.33 branch adds semantic composition and directional reflection, yielding separation from quotient sections/retractions. Global witness correlation, the comparison lift, and the final coherent universal property remain distinct research steps.
