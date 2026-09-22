# KuuOS / 空OS Roadmap

**Theorem baseline: 2026-09-22 JST · integrated through v3.30**

This roadmap records proved results, explicit hypotheses, countermodel scope, and theorem-sized exit criteria. Versions identify mathematical units; they do not by themselves certify the final universality claim.

## 1. Authority and reproducible baseline

```text
canonical branch:                 main
latest theorem-bearing merge:     PR #1706, v3.30
mathematical baseline:            1b4cf22eb8e8b5ffc70c490093534ff95ff2a081
validated PR head:                0c2ead10cc002150d47f3e0ba7a4e5da65b3db88
exact-head gate:                  #2523 / run 35679072189
terminal conclusion:              completed / success
Strict Lean receipt:              success
exact-head terminal receipt:      success
Lean:                            leanprover/lean4:v4.30.0-rc2
Mathlib:                         5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

References: [merged PR #1706](https://github.com/itakura-hidetoshi/KuuOS/pull/1706), [theorem baseline](https://github.com/itakura-hidetoshi/KuuOS/commit/1b4cf22eb8e8b5ffc70c490093534ff95ff2a081), [exact-head CI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35679072189), and [v3.30 source](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean).

`main` equaled the mathematical baseline when observed for this refresh. Subsequent docs-only commits can move its pointer without moving the theorem frontier. Never use the embedded snapshot instead of a fresh GitHub read at the start of new work.

```text
fresh exact canonical SHA
  > formal Lean artifacts
  > README / ROADMAP
  > CI / runtime receipts
  > history / memory
```

PR #1651 historically integrated the former v2.69–v3.14 frontier; it is not the current working Draft. The separate validation-only PR #1558 remains outside this theorem authority. Do not merge it, mark it Ready for review, or enable auto-merge.

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

The canonical spine is established through v3.30. General Stage-I existence, Stage-II universality, and the final representation theorem are not thereby complete.

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

## 5. Actual route equations and directional closure: v3.22–v3.30

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

`MiddleIdentityWhiskerSeparating` is the explicit injectivity condition for this action. It closes the endpoint overlap; it is not an abstract global gluing axiom and is not assumed universally.

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

The module proves:

```text
ordinary EssSurj certificate on Quot.out f
  -> (quotientRepresentativeMap W R D f).toFunctor.EssSurj

ordinary Faithful certificate on Quot.out g
  -> (quotientRepresentativeMap W R D g).toFunctor.Faithful

both certificates
  -> MiddleIdentityWhiskerSeparating W R D f g

both certificates + three actual corrections + two anchor agreements
  -> full overlap agreement of the right/left-unitor endpoints.
```

The last theorem is

```text
associatorAnchor_unitor_overlapStar_triangle_of_representative_words.
```

This is the current integrated theorem frontier. It introduces no new quotient relation, universal path-independence hypothesis, or separation axiom.

## 6. Immediate theorem units after v3.30

These are proposed next milestones, not claims that a v3.31 module already exists.

### N1 — Separate word certificates from semantic invariance

A predicate on `Quot.out f` is well-defined once that selector is fixed. It is not thereby an intrinsic certificate independent of the chosen representative.

Treat two problems separately:

**N1a: relation-level behavior of the letterwise certificates.** Check `id`, `comp`, `Winv₁`, and `Winv₂`, then the required compositions and contexts of those relations. Track direction: properties of both factors imply the corresponding property of a composite; the converse must be proved or refuted, not inferred. A failure of syntactic invariance need not be a failure of semantic invariance.

**N1b: transport of the evaluated property.** Use the v2.58 isomorphism-existence result for quotient-equal path evaluations and the relevant Mathlib transport lemmas for essential surjectivity and faithfulness. Package the proof at the current pinned revision, keeping `Cat.Hom`, functors, and natural isomorphisms explicit.

Exit criterion: checked lemmas explaining exactly how a directional evaluation property is transferred between quotient-equal paths, independently of whether their letterwise certificates match.

### N2 — A suitable representative, not necessarily Quot.out

Define a sufficient quotient-level condition by existence of a representative with the appropriate ordinary-letter certificate. Transport its evaluated property to the actual selected representative using N1b.

Desired shape, schematic only:

```text
there exists p representing f with ordinary EssSurj letters
  -> selected evaluation of f is EssSurj

there exists q representing g with ordinary Faithful letters
  -> selected evaluation of g is Faithful
  -> the v3.28 mixed-triangle closure criterion applies.
```

Exit criterion: a representative-independent sufficient sector closed under the operations actually proved. Do not replace “there exists a certified representative” by “every representative is certified,” or by a necessary condition, without proof.

### N3 — Truth-test the remaining separation boundary

For arrows outside the established sufficient sectors, either derive more general cancellation/detection conditions or construct an actual Cat-valued generated example with distinct middle 2-cells having the same double-whiskered image.

Exit criterion: a concrete proof of additional separation, or a verified noninjectivity witness. Failure of `EssSurj`, `Faithful`, or a letterwise certificate alone is not that witness. Nor would noninjectivity alone refute general factorization without an additional bridge to incompatible actual correction data.

### N4 — Correlate witnesses using the actual incidence geometry

Extend the route-specific v3.22–v3.30 results to the incidence sectors required for one global compatible family. Possible routes are an actual overlap-preserving normalizer, a suitable star-transitivity theorem with explicit incidence hypotheses, or another directly constructed correlated family.

Both ingredients must be accounted for: existence of the relevant correcting local witnesses and their simultaneous overlap compatibility. Do not silently assume either from weak admissibility.

Exit criterion:

```text
explicit hypotheses on the actual generated route system
  -> HasGloballyCompatibleLocalCorrectionFamily W R D
  -> HasFiniteFootprintAmalgamation W R D
  -> coherent quotient transport via the established bridges.
```

The v3.15/v3.16 patching constructions should be reused, not reclassified as unsolved.

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
  build KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30
```

The aggregate `KuuOSFormal` target is a separate check; the recorded focused receipt is not a fresh aggregate-validation claim. Runtime validation remains separate through `PYTHONPATH=. python3 runtime/kuuos_current_check.py`.

Retain the concrete lessons of v3.26–v3.30:

- Keep dependent equality transport explicit. Use typed intermediate equalities, `eqToHom` naturality, `congrArg`, and limited reassociation instead of blind rewriting deep inside dependent composites.
- Imported declarations do not export the caller's `open` commands. Open the required namespaces explicitly; use `autoImplicit false` in the new modules to expose unresolved names.
- Supply the dependent predicate to `Paths.induction` when inference is insufficient. Where available, pass composition witnesses directly to the pinned `Functor.essSurj_comp` and `Functor.Faithful.comp` declarations.
- In v3.30, preserve the exact higher-order predicate `@P` in the inductive family and the actual recursor binders. Induct on `PathEdgesSatisfy` evidence; reduce the evaluator's `cons` definition directly rather than forcing `map_comp` to match through wrappers.

No proof term, Lean option, dependency pin, or workflow is changed by this documentation refresh. A docs-only successful gate cannot substitute for a new theorem validation.

## 10. No-go rules and completion criteria

Do not promote these implications without a theorem:

```text
local Nonempty Iso -> coherent choice
Classical.choice -> pentagon/unit laws
weak Cat equivalence -> actual Cat isomorphism
ordinary localization universality -> automatic pseudofunctor descent
Quot.out choice -> coherent pseudofunctor
weak admissibility -> generated holonomy triviality
nontrivial holonomy -> factorization impossible
nested pairwise witnesses -> one globally compatible family
footprint locality -> witness correlation
abstract parity countermodel -> actual-system factorization failure
one incidence triangle -> global star transitivity
failed word certificate -> failed semantic property or nontrivial kernel
conditional Stage-I result -> coherent universal property
runtime or model output -> canonical theorem authority
```

Completion requires formally checked, correctly scoped existence, coherent factorization, essential uniqueness, presentation invariance, descent compatibility, higher coherence, explicit obstruction/correction boundaries, and a natural representation theorem.

Until then, keep the labels distinct: **proved**, **conditionally proved**, **classical**, **constructive**, **abstractly refuted**, **open**, **validation-only**, **interpretive**, and **operational**.
