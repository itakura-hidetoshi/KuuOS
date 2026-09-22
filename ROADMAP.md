# KuuOS / 空OS Roadmap

**Theorem baseline: 2026-09-22 JST · integrated through v3.33**

This roadmap records proved results, explicit hypotheses, countermodel scope, and theorem-sized exit criteria. Versions identify mathematical units; they do not by themselves certify the final universality claim.

## 1. Authority and reproducible baseline

```text
canonical branch:                 main
latest theorem-bearing merge:     PR #1710, v3.33
mathematical baseline:            d5747268c38fef1b24ad7e9b5fa5fb3bf7c11455
post-merge main before docs:      d5747268c38fef1b24ad7e9b5fa5fb3bf7c11455
validated PR head:                ba17572f2058819cd084d14dd31ac8678b446a3d
exact-head gate:                  #2532 / run 35690347773
terminal conclusion:              completed / success
Strict Lean receipt:              success
exact-head terminal receipt:      success
CI synthetic merge checkout:      e345655b329d34f8aab88778a75e582ea33747e7
Lean:                            leanprover/lean4:v4.30.0-rc2
Mathlib:                         5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

References: [merged PR #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710), [theorem baseline](https://github.com/itakura-hidetoshi/KuuOS/commit/d5747268c38fef1b24ad7e9b5fa5fb3bf7c11455), [exact-head CI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35690347773), and [v3.33 source](formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean).

The v3.33 run completed its focused target and dependencies with return code `0` and passed the dependency-manifest check. Its synthetic checkout tested the validated PR head with the v3.32 base `c59c7aa4e6435a2172344dfaf2843937a86a89d8`; it is not the final merge commit. Historical imported-module linter warnings remain. A focused success is not a fresh `KuuOSFormal` aggregate success.

`main` equaled the mathematical baseline immediately after merging #1710. This docs-only refresh can move the branch pointer without moving that baseline. Never use the embedded snapshot instead of a fresh GitHub read at the start of new work.

```text
fresh exact canonical SHA
  > formal Lean artifacts
  > README / ROADMAP
  > CI / runtime receipts
  > history / memory
```

PR #1651 historically integrated the former v2.69–v3.14 frontier; it is not the current working Draft. The v3.31, v3.32 and v3.33 layers are integrated by #1708, #1709 and #1710 respectively. The separate validation-only PR #1558 remains outside this theorem authority. Do not merge it, mark it Ready for review, or enable auto-merge.

## 2. North star and distinct completion levels

Construct the correct higher carrier and prove a mapping property schematically of the form:

```text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X).
```

The final package needs existence, factorization, essential uniqueness, coherent naturality, descent compatibility, auxiliary-choice independence, and the appropriate equivalence of presentations. Nontrivial obstruction must be corrected under stated authority or retained explicitly, not erased.

Keep separate:

```text
a local route equation
a closed incidence triangle
one globally compatible local correction family
one coherent quotient transport
higher-localization factorization (Stage I)
coherent universal data (Stage II)
final DO carrier and representation theorem
```

The canonical spine is established through v3.33. General Stage-I existence, Stage-II universality, and the final representation theorem are not thereby complete.

## 3. Retained canonical spine through v3.14

| Range | Established contribution |
| --- | --- |
| v2.0–v2.10 | Localization and W + J sectors; Cat-valued/higher stack descent; `HigherLocalizationFactorization` interface. |
| v2.11–v2.42 | Strict/weak/coherent distinctions, modification triangles, correction, and the E/R/A obstruction normal form. |
| v2.43–v2.55 | Structural sufficient E/R routes and a restricted Stage-I sector where W is already base-isomorphic. |
| v2.56–v2.58 | Pointwise W-adjoint-equivalence data, finite free-path evaluation, and `Nonempty` isomorphisms between evaluations of quotient-equal paths. |
| v2.59–v2.68 | Exact quotient/comparison coherence data, local choices, thin sufficient sectors, five defects, gauge normal forms, generated 2-cells and holonomy. |
| v2.69 | Octahedral countermodel to weak admissibility implying generated-holonomy triviality. This does not refute factorization. |
| v2.70–v2.95 | Filtered obstruction and correctability, correction authority, extensional correction power, reachability, lattice operations, and constructive/classical distinctions. |
| v2.96–v3.04 | Return to factorization: compatible five-face correction; split into three quotient equations and two comparison equations; quotient `gId/gComp` data separated from comparison `gIso`. |
| v3.05–v3.14 | Quotient coboundary/transport equivalence, correction loci, the witness quantifier gap, finite dependent footprints, and shared-coordinate keys. |

The retained sufficient implication is

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R.
```

The negative v2.69 truth test prevents replacing its hypothesis by weak admissibility without further work. The correction program addresses that gap rather than abandoning the original factorization question.

## 4. Completed extension and correlation analysis: v3.15–v3.21

### A1.12 — Pairwise finite extension: proved in v3.15

[Source](formal/KUOS/DependentOriginationPairwiseFiniteExtensionV3_15.lean)

```text
AgreeOnRouteFootprintOverlap W R D s t Qs Qt
  <-> CompatibleOnRouteOverlap W R D s t Qs Qt.
```

The proof patches the actual dependent `mapIdGauge/mapCompGauge` families. It uses classical footprint membership, not a new gluing axiom. The old v3.14 pair-extension question is no longer an open milestone.

### A1.13 — Gluing a single compatible family: proved in v3.16

[Source](formal/KUOS/DependentOriginationGlobalFootprintGluingV3_16.lean)

```text
HasFiniteFootprintAmalgamation W R D
  <-> HasGloballyCompatibleLocalCorrectionFamily W R D.
```

One simultaneously selected correcting family, equal on every pairwise shared coordinate, glues by an explicit global coordinate selector. Classical selection is visible. No compactness, convexity, Helly theorem, or finiteness of all route states is assumed.

This is **not** the claim that arbitrary pairwise existential witnesses automatically form such a family. In the nested condition, the witness for route `t` may depend on the anchor `s`:

```text
for every s, choose Qs;
for each t, choose a Qt compatible with that Qs
```

versus

```text
choose one Qlocal for all states;
every pair in that one family is compatible.
```

### A1.14 — Abstract no-go and conditional correlation routes

| Layer | Result |
| --- | --- |
| [v3.17](formal/KUOS/DependentOriginationPairwiseCorrelationCountermodelV3_17.lean) | A finite Boolean parity model has nested pairwise witnesses but no globally compatible family. |
| [v3.18](formal/KUOS/DependentOriginationSharedCoordinateRigidityV3_18.lean) | Nested pairwise witnesses plus shared-coordinate rigidity imply a global family and amalgamation. |
| [v3.19](formal/KUOS/DependentOriginationSharedCoordinateNormalizerV3_19.lean) | An explicitly supplied gauge-fixing normalizer preserving correction and overlap, with normalized shared rigidity, suffices. |
| [v3.20](formal/KUOS/DependentOriginationOverlapStarTransitivityV3_20.lean) | Nested pairwise witnesses plus overlap-star transitivity suffice; the empty route-state case is included. |
| [v3.21](formal/KUOS/DependentOriginationCylinderLocalityCountermodelV3_21.lean) | The parity model also has footprint-cylinder locality: that locality alone cannot supply correlation or star transitivity. |

The v3.17/v3.21 countermodels concern abstract finite-footprint predicates. They do not instantiate a failure of `HigherLocalizationFactorization` for an actual raw contextual system. Conversely, v3.18–v3.20 do not assert their additional structures automatically exist in every actual system.

## 5. Actual route equations and directional closure: v3.22–v3.33

### A1.15 — Actual unitor and associator rigidity

[v3.22](formal/KUOS/DependentOriginationUnitorPartialRigidityV3_22.lean): inside a corrected left/right unitor locus, equality of the identity coordinate forces equality of the corresponding composition coordinate.

[v3.23](formal/KUOS/DependentOriginationAssociatorThreeOfFourRigidityV3_23.lean): for two gauges correcting one associator route, equality of the coordinates

```text
(f,g), (g,h), (f,g ≫ h)
```

forces equality at `(f ≫ g,h)`, hence on that associator footprint. This is the proved orientation; cancellation through arbitrary whiskering must not be silently inferred for other orientations.

[v3.24](formal/KUOS/DependentOriginationUnitorStarTransitivityV3_24.lean): homogeneous stars close for three left unitors sharing a source, or three right unitors sharing a target. The common-identity incidence is essential: a disjoint anchor could otherwise make anchor agreements vacuous.

[v3.25](formal/KUOS/DependentOriginationMixedUnitorRigidityV3_25.lean): actual left/right unitor equations resolve mixed endpoint overlap when the common identity gauge agrees, including the nontrivial identity/identity composition overlap.

### A1.16 — The genuine mixed incidence triangle: v3.26

[Source](formal/KUOS/DependentOriginationAssociatorUnitorTriangleResidualV3_26.lean)

```text
associator f (1_Y) g
  -- shares gComp(f,1_Y) with rightUnitor f
  -- shares gComp(1_Y,g) with leftUnitor g

rightUnitor f and leftUnitor g share gId(Y).
```

Under actual correction of all three routes and the two anchor-overlap agreements, bicategory triangle coherence gives equality after

```text
Phi(eta) = F ◁ (eta ▷ G),
```

where `F` and `G` are the outer quotient representatives. The first theorem is double-whiskered equality, not unconditional literal equality of the middle identity correction.

`MiddleIdentityWhiskerSeparating` is the explicit injectivity condition for this action. It closes the endpoint overlap; it is not an abstract global gluing axiom and is not assumed universally. The word “kernel” here denotes the equality relation of this map, not an assumed linear structure.

### A1.17 — Concrete sufficient separation sectors: v3.27–v3.28

[v3.27](formal/KUOS/DependentOriginationAssociatorUnitorWEdgeSeparationV3_27.lean) obtains separation when both outer representative functors are equivalences. The generated presentation comparison and the W-adjoint-equivalence data prove this for outer arrows `W.Q.map f`, `W.Q.map g` with `W f` and `W g`.

[v3.28](formal/KUOS/DependentOriginationAssociatorUnitorOneSidedSeparationV3_28.lean) proves the more general sufficient criterion:

```text
F.toFunctor.EssSurj + G.toFunctor.Faithful
  -> MiddleIdentityWhiskerSeparating W R D f g.
```

Precomposition is cancellable on natural transformations because the left functor is essentially surjective; postcomposition is cancellable because the right functor is faithful. The v3.27 equivalence criterion factors through these conditions. This is not an asserted necessary-and-sufficient characterization of separation.

### A1.18 — Finite free-path propagation: v3.29

[Source](formal/KUOS/DependentOriginationFreePathDirectionalPropagationV3_29.lean)

Generator-level essential surjectivity or faithfulness propagates to every finite free path under the corresponding all-generator hypothesis. Identity paths have both properties. Formal W-inverse generators have both through the chosen equivalences. An ordinary generator has exactly the relevant property of its raw functor evaluation.

This is a path-level result, not a quotient-descent theorem.

### A1.19 — Actual selected-word bridge: v3.30

[Source](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean)

The all-generator hypotheses are replaced by certificates for the particular word being evaluated. `PathEdgesSatisfy` is an inductive, dependent predicate with identity and edge-extension constructors. Formal-inverse letters impose no extra condition; ordinary letters carry the raw directional condition.

```text
ordinary EssSurj certificate on Quot.out f -> E(f).EssSurj
ordinary Faithful certificate on Quot.out g -> E(g).Faithful
both certificates -> MiddleIdentityWhiskerSeparating W R D f g
```

Here and below, `E(f) := (quotientRepresentativeMap W R D f).toFunctor`, for fixed `W`, `R`, `D`. The endpoint-overlap theorem also retains the three actual correction hypotheses and the two anchor agreements. The selected-word result remains proved; it is now a special case of v3.31's existence criterion.

### A1.20 — Semantic representative invariance and one good word: v3.31

[Source](formal/KUOS/DependentOriginationQuotientDirectionalPropertyTransportV3_31.lean) · [merged #1708](https://github.com/itakura-hidetoshi/KuuOS/pull/1708)

The existing `equalInLocalization_hasEvaluationIso` supplies a local evaluation isomorphism whenever `[p] = [q]`. Transferring along its underlying natural isomorphism proves both directions of

```text
[p] = [q]
  -> (evaluation(p).EssSurj <-> evaluation(q).EssSurj)
  -> (evaluation(p).Faithful <-> evaluation(q).Faithful).
```

These are two conclusions from the same quotient equality, not extra hypotheses on the paths. `quotientRepresentativeMap_essSurj_iff_of_representative` and its faithful counterpart compare the selected evaluation with any specified representative. All isomorphism witnesses are used locally inside propositions; this is not a new coherent choice of a transport family.

The definitions `HasOrdinaryEssSurjRepresentative` and `HasOrdinaryFaithfulRepresentative` require **one** representing path with the corresponding ordinary-letter certificate. They do not refer to `D` or `Quot.out`. The selected-word certificates imply these existence conditions, which imply the semantic evaluation properties and hence the v3.28 separation/mixed-triangle conclusions with all original correction hypotheses.

**Former N1b and the existence/transport part of N2 are complete.** This is invariance under representatives for fixed `W`, `R`, `D`, not a claim of invariance of every letterwise certificate or independence of every auxiliary choice.

### A1.21 — Multiplicative certified classes and minimality: v3.32

[Source](formal/KUOS/DependentOriginationCertifiedQuotientSectorClosureV3_32.lean) · [merged #1709](https://github.com/itakura-hidetoshi/KuuOS/pull/1709)

`pathEdgesSatisfy_comp` proves concatenation of certified paths. For any relation `r` on a path category, `certifiedQuotientSector r P` consists of quotient arrows admitting a `P`-certified representative. It has a Mathlib `IsMultiplicative` instance: the empty path supplies identities and concatenated witnesses supply composition. No invariance of `P` under `r` is assumed.

For every multiplicative morphism property `S`, `certifiedQuotientSector_le_iff` proves

```text
certifiedQuotientSector r P ≤ S
  <-> forall e, P e -> S((Quotient.functor r).map e.toPath).
```

This is minimality among multiplicative properties containing those generator images. It specializes to both v3.31 existence conditions and gives separation for composites of certified outer arrows.

**The identity/composition closure part of former N2 is complete.** The minimality theorem is not a necessary characterization of semantic EssSurj/Faithful, and it asserts neither arbitrary-factor closure nor inverse closure of the certified classes.

### A1.22 — Semantic classes, directional reflection and split arrows: v3.33

[Source](formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean) · [merged #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710)

The v2.61 identity and composition isomorphism-existence results give semantic identity/composition laws without constructing a coherent quotient pseudofunctor:

```text
E(𝟙 X).EssSurj and E(𝟙 X).Faithful

E(f ≫ g).EssSurj  <-> (E(f) ⋙ E(g)).EssSurj
E(f ≫ g).Faithful <-> (E(f) ⋙ E(g)).Faithful.
```

Thus `quotientEssSurjSector W R D` and `quotientFaithfulSector W R D` are multiplicative morphism properties. The existing certified classes are contained in these semantic classes. **Neither equality nor strictness of these containments is established.** The semantic definitions retain `D`; no general auxiliary-choice-independence theorem is inferred.

The reflection directions are:

```text
E(f ≫ g).EssSurj  -> E(g).EssSurj
E(f ≫ g).Faithful -> E(f).Faithful.
```

Essential surjectivity uses an essential-image witness in the intermediate category; faithfulness uses Mathlib's `Functor.Faithful.of_comp`. No reversed reflection or letterwise reflection is asserted.

For `f : X ⟶ Y`, `g : Y ⟶ Z`, one-sided inverses in the actual quotient suffice:

```text
s : Y ⟶ X, s ≫ f = 𝟙 Y -> E(f).EssSurj
r : Z ⟶ Y, g ≫ r = 𝟙 Y -> E(g).Faithful

both equations -> MiddleIdentityWhiskerSeparating W R D f g.
```

The final theorem is `associatorAnchor_unitor_overlapStar_triangle_of_section_retraction`. It still requires the three correcting gauges, their three route equations and both anchor-overlap agreements. It does not construct these gauges. A split epimorphism on the left and a split monomorphism on the right require no word certificates for this proof, but their relation to the certified classes is not characterized here.

**N3 has advanced by a new sufficient criterion, not been closed globally.** No noninjectivity counterexample or general witness-correlation theorem is supplied by this layer.

## 6. Remaining theorem units after v3.33

### Milestone status: do not restart completed constructions

| Earlier target | Current status |
| --- | --- |
| N1a — letterwise behavior under quotient relations | Separate syntactic question; not required by the proved semantic transfer. |
| N1b — semantic property transfer between quotient-equal paths | **Proved in v3.31.** Reuse it. |
| N2 — one suitable representative and quotient-level closure | **Proved in v3.31–v3.32**, including identities, composition and generator minimality. |
| N3 — remaining separation boundary | **Partially advanced in v3.33** by semantic algebra, directional reflection and split arrows; broader characterization/truth tests remain. |
| N4 — actual simultaneous witness correlation | Open beyond the established route-specific sufficient results. |
| N5 — comparison equations and general Stage I | Open in the general stated admissibility. |

The following are proposed work units, not claims that a v3.34 or later theorem has been implemented.

### N1a — Keep syntactic certificate analysis separate

Study how letterwise certificates behave under `id`, `comp`, `Winv₁`, `Winv₂` and their contexts. Both certified factors imply a certified composite where the relevant hypotheses apply; recovering every factor's certificate from a composite is a different statement. Semantic representative invariance is already proved and must not be withheld pending this analysis.

Exit criterion: precise directional preservation/reflection statements or counterexamples for the syntactic predicate, without confusing them with failure of semantic EssSurj/Faithful or failure of separation.

### N3 — Characterize and truth-test the remaining actual separation boundary

Start from the **integrated** semantic identity/composition laws and split criterion, rather than reproving them. Develop further actual cancellation/detection conditions, reusable realizations of the split hypotheses, or a concrete Cat-valued generated example with distinct middle 2-cells and the same double-whiskered image.

Keep the classes distinct: a selected-word certificate; existence of one certified representative; semantic EssSurj/Faithful; an actual one-sided inverse; and double-whiskering injectivity. The containment of certified classes in semantic classes is proved, but equality, strictness, and converse relations to split conditions require their own theorems. Any independence claim beyond fixed-D representative transport also needs an explicit proof.

Exit criterion: a concrete additional separation theorem or verified noninjectivity witness in the actual generated setting. Failure of a certificate, EssSurj, Faithful, or a split hypothesis alone is not that witness. Noninjectivity alone would still not refute general factorization without a bridge to incompatible actual correction data.

### N4 — Correlate witnesses using the actual incidence geometry

Extend the route-specific v3.22–v3.33 results to the incidence sectors needed for one global compatible family. Possible routes are an actual overlap-preserving normalizer, a suitable star-transitivity theorem with explicit incidence hypotheses, or another directly constructed correlated family.

Both ingredients must be accounted for: existence of the relevant correcting local witnesses and their simultaneous overlap compatibility. Neither follows merely from having a sufficient cancellation criterion. Do not silently assume either from weak admissibility.

Exit criterion:

```text
explicit hypotheses on the actual generated route system
  -> HasGloballyCompatibleLocalCorrectionFamily W R D
  -> HasFiniteFootprintAmalgamation W R D
  -> coherent quotient transport via the established bridges.
```

Reuse the v3.15/v3.16 patching constructions. They are not the unresolved part of the correlation problem.

### N5 — The two comparison equations and general Stage I

After the quotient stage, solve or characterize the two remaining comparison `gIso` equations from the v3.02–v3.04 split. Assemble the result into the exact higher-localization factorization interface.

The broad open implication remains:

```text
IsHigherWAdmissible W R
  -> HasHigherLocalizationFactorization (W := W) R.
```

Exit criterion: either prove general existence under the stated admissibility, or provide a necessary/sufficient obstruction characterization with all extra conditions explicit. If a higher carrier is needed, construct it and prove a comparison with the ordinary localization sector; do not treat nontrivial holonomy alone as proof that it is needed.

## 7. Stage II and the remaining universality tracks

### Track A2 — Coherent Stage-II universality

Construct chosen factorizations, comparison triangles from competitors, modifications, higher naturality, and presentation transport.

```text
HasCoherentWeakHigherLocalizationUniversalProperty W R
```

is distinct from Stage-I existence. A carrier identification cannot be hidden in notation.

### Track B — Axis E: essential uniqueness

Retain `HigherWeakEssentialUniquenessObstruction` from the v2.42 E/R/A normal form and the sufficient v2.43–v2.54 routes. Derive natural detector families, cancellation hypotheses, or representability/contractibility conditions rather than merely adding them as unexplained inputs.

Exit criterion: essential uniqueness under a reusable set of explicit structural assumptions.

### Track C — Axis R: fixed coherent route

Retain `HigherFixedChosenForwardModificationTriangleObstruction`, the stored correction equations, and the arrowwise coherence equations. Compare this modification-triangle problem with the later correction-power semantics without collapsing different categorical levels.

Exit criterion: a checked equivalence between vanishing of the specified obstruction and existence of the required coherent correction/extension.

### Track D — Weak/coherent alignment

Assemble coherent existence and control of Axes E/R using the existing normal form. This is global theorem assembly, not a consequence of one local cancellation result.

### Track E — Minimal dependent-origination principles

The candidate principles remain contextuality, compositional transport, higher coherence, presentation invariance, descent, obstruction, and non-reification/authority boundaries. Separate mathematical data, properties, derivable conditions, and philosophical interpretations. Use countermodels to test non-implications and distinguish constructive results from classical selectors.

### Tracks F–H — Correct carrier, construction, representation

Do not preselect an ordinary category, bicategory, higher category, stack, scaled-simplicial object, or orthogonality completion as the final carrier solely by analogy. Decide through theorems about retained transport, correction, and truncation.

Then construct `DO(C,W,J,H)` with presentation and choice independence, descent and coherence compatibility, and explicit obstruction semantics. Only a natural mapping/representation theorem with essential uniqueness completes the north star.

## 8. Parallel mathematical and AI workstreams

The parallel mathematical tracks remain fundamental-groupoid descent, information loss under quotient/truncation, scaled-simplicial higher realization, and cross-realization comparisons. Curvature-sensitive transport is not silently identified with ordinary homotopy-groupoid transport; each truncation needs a comparison theorem.

AI realization continues along bounded, separately validated directions:

| Workstream | Required behavior |
| --- | --- |
| Model migration | Carry semantic invariants, provenance, authority constraints, regression checks, canary promotion, and rollback evidence. |
| Memory integration | Check compatibility, retain contradiction witnesses and explicit obstructions, and avoid silent overwrite. |
| Retrieval | Use least-sufficient bounded escalation; unknown adequacy fails closed; retrieval is not entailment. |
| Multi-agent coordination | Distinguish pairwise valid handoffs from one globally compatible decision family and track authorized correction capabilities. |
| Control plane | Preserve `observe -> represent -> retrieve -> plan -> decide -> act -> re-observe -> verify`. |

The formal results guide these designs; they do not establish production safety or authorize external actions. No host or model receives automatic WORLD-commit, truth, rollback-proof, or memory-overwrite authority.

## 9. Verification discipline and proof engineering

A reproducible focused command for the current theorem unit is:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
```

The aggregate `KuuOSFormal` target is a separate check; the recorded focused receipt is not a fresh aggregate-validation claim. Runtime validation remains separate through `PYTHONPATH=. python3 runtime/kuuos_current_check.py`. A docs-only successful gate cannot substitute for a new theorem validation.

Retain the concrete lessons of v3.26–v3.33:

- Keep dependent equality transport explicit. Use typed intermediate equalities, `eqToHom` naturality, `congrArg`, and limited reassociation instead of blind rewriting deep inside dependent composites. Open the needed namespaces explicitly and retain `autoImplicit false` in new modules.
- For `PathEdgesSatisfy`, preserve `@P`, the uniform parameters and actual recursor binders, and induct on its evidence. At `X.as : Paths V`, keep the original edge quiver explicit in the empty-path constructor: `@PathEdgesSatisfy.nil V Q (@P) X.as`. Reduce the evaluator's `cons` definition directly where appropriate.
- Ordinary implicit `{X Y}` arguments can be inserted during partial application. To pass the v3.31 predicates as a full `MorphismProperty`, bind `⦃X Y⦄` and the arrow explicitly before applying the predicate. A postfix type ascription or a fully qualified API name alone did not repair that higher-order boundary in v3.32.
- Across the `W.Localization`/generic `Quotient` boundary, pass already-given multiplicativity evidence explicitly instead of requiring instance search to rediscover it. The v3.32 leastness specializations use named `[hS : S.IsMultiplicative]` and an explicit `@... S hS` application.
- In v3.33, give `Cat.Hom.toNatIso` a typed `have` whose endpoints expose `𝟭 C` or `F.toFunctor ⋙ G.toFunctor` before property transport. Definitional equality of the wrapped expressions does not guarantee instance synthesis will find identity/composition evidence. Preserve the local evaluation isomorphism rather than replacing it by a strict functor law.

The latter points are recorded in the checked sources and the [#1709](https://github.com/itakura-hidetoshi/KuuOS/pull/1709) / [#1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710) diagnostic histories. General reference material: [Lean implicit parameters](https://lean-lang.org/doc/reference/latest/Terms/Functions/) and [instance synthesis](https://lean-lang.org/doc/reference/latest/Type-Classes/Instance-Synthesis/). The pinned source and completed pinned CI, rather than a moving documentation version, determine API compatibility.

For CI reentry, obtain the PR state and current head first. A merged PR must not return to waiting on an old run. Track runs and terminal receipts for the exact new head after each update; distinguish queued/running, completed failure and completed success. Inspect completed failure logs and whole affected modules before repairing. Merge with the expected head, then re-read and compare `main`. This document does not create background monitoring.

No proof term, Lean option, dependency pin, or workflow is changed by this documentation refresh.

## 10. No-go rules and completion criteria

Do not promote these implications without a theorem:

```text
local Nonempty Iso -> coherent choice
Classical.choice -> pentagon/unit laws
weak Cat equivalence -> actual Cat isomorphism
ordinary localization universality -> automatic pseudofunctor descent
Quot.out choice -> coherent pseudofunctor
fixed-D representative invariance -> all auxiliary-choice independence
weak admissibility -> generated holonomy triviality
nontrivial holonomy -> factorization impossible
nested pairwise witnesses -> one globally compatible family
footprint locality -> witness correlation
abstract parity countermodel -> actual-system factorization failure
one incidence triangle -> global star transitivity
failed word certificate -> failed semantic property or nontrivial kernel
certified ≤ semantic -> equality or strict containment
semantic composite property -> same property on every factor or letter
split-arrow separation -> existence of all correcting gauges
conditional Stage-I result -> coherent universal property
runtime or model output -> canonical theorem authority
```

Completion requires formally checked, correctly scoped existence, coherent factorization, essential uniqueness, presentation invariance, descent compatibility, higher coherence, explicit obstruction/correction boundaries, and a natural representation theorem.

Until then, keep the labels distinct: **proved**, **conditionally proved**, **classical**, **constructive**, **abstractly refuted**, **open**, **validation-only**, **interpretive**, and **operational**.
