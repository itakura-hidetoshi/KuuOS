# KuuOS / 空OS Roadmap

**2026-09-22 JST · canonical through v3.32 · v3.33 validated at PR #1710, not yet merged**

This roadmap records established results, their explicit hypotheses, countermodel scope, integration status, and theorem-sized exit criteria. A version number, a successful CI run, and a canonical merge describe different facts.

## 1. Authority and reproducible baselines

### Integrated theorem line

```text
canonical branch:                 main
latest theorem-bearing merge:     PR #1709, v3.32
mathematical baseline:            c59c7aa4e6435a2172344dfaf2843937a86a89d8
validated PR head:                47da65d74fcd062b10f8bcbea8954e0e800a3cfc
exact-head gate:                  #2530 / run 35687280701
workflow conclusion:              completed / success
Strict Lean receipt:              success
exact-head terminal receipt:      success
```

References: [merged PR #1709](https://github.com/itakura-hidetoshi/KuuOS/pull/1709), [mathematical baseline](https://github.com/itakura-hidetoshi/KuuOS/commit/c59c7aa4e6435a2172344dfaf2843937a86a89d8), [v3.32 CI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35687280701), and [v3.32 source on main](formal/KUOS/DependentOriginationCertifiedQuotientSectorClosureV3_32.lean).

### Validated, unmerged theorem line

```text
PR:                              #1710, v3.33
state at observation:            Draft / open / merged=false
branch:                          formal/dependent-origination-quotient-split-directional-separation-v333
validated exact head:            ba17572f2058819cd084d14dd31ac8678b446a3d
base:                            c59c7aa4e6435a2172344dfaf2843937a86a89d8
exact-head gate:                  #2532 / run 35690347773
workflow conclusion:              completed / success
Strict Lean receipt:              success
exact-head terminal receipt:      success
```

References: [PR #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710), [validated v3.33 source](https://github.com/itakura-hidetoshi/KuuOS/blob/ba17572f2058819cd084d14dd31ac8678b446a3d/formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean), and [v3.33 CI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35690347773).

Both lines use:

```text
Lean:                            leanprover/lean4:v4.30.0-rc2
Mathlib:                         5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

`main` equaled the mathematical baseline before this documentation refresh. Documentation-only commits can move that pointer without advancing the theorem frontier. This refresh does not merge #1710 or add its source to main. Re-observe both branch pointers and PR state before continuing; neither these dated tables nor an older CI run supersedes GitHub's current state.

```text
fresh exact canonical SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > CI / runtime receipts
  > history / memory
```

PR #1651 historically integrated the former v2.69–v3.14 frontier; it is not the current working Draft. The separate validation-only PR #1558 remains outside the theorem line. Its standing policy is unchanged: no merge, no Ready for review, and no auto-merge.

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
final DO carrier and representation theorem.
```

The canonical spine is integrated through v3.32. The additional v3.33 split criterion is validated but unmerged. Neither result completes general Stage-I existence, Stage-II universality, or the final representation theorem.

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
| v3.05–v3.14 | Quotient coboundary/transport equivalence, correction loci, witness quantifier gap, finite dependent footprints, and shared-coordinate keys. |

The retained sufficient implication is

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R.
```

The v2.69 truth test prevents replacing its hypothesis by weak admissibility without further work. The correction program addresses that gap rather than abandoning the factorization question.

## 4. Completed extension and correlation analysis: v3.15–v3.21

### A1.12 — Pairwise finite extension: integrated v3.15

[Source](formal/KUOS/DependentOriginationPairwiseFiniteExtensionV3_15.lean)

```text
AgreeOnRouteFootprintOverlap W R D s t Qs Qt
  <-> CompatibleOnRouteOverlap W R D s t Qs Qt.
```

The proof patches the actual dependent `mapIdGauge/mapCompGauge` families. It uses classical footprint membership, not a new gluing axiom. Pair extension is no longer an open milestone.

### A1.13 — Gluing one compatible family: integrated v3.16

[Source](formal/KUOS/DependentOriginationGlobalFootprintGluingV3_16.lean)

```text
HasFiniteFootprintAmalgamation W R D
  <-> HasGloballyCompatibleLocalCorrectionFamily W R D.
```

One simultaneously selected correcting family, equal on every pairwise shared coordinate, glues by an explicit global coordinate selector. Classical selection is visible. No compactness, convexity, Helly theorem, or finiteness of all route states is assumed.

The remaining quantifier distinction is

```text
for every s, choose Qs;
for each t, choose a Qt compatible with that Qs
```

versus

```text
choose one Qlocal for all states;
every pair in that same family is compatible.
```

The first condition permits the witness for `t` to depend on the anchor `s`. It does not supply the second by logic alone.

### A1.14 — Abstract countermodels and conditional correlation routes

| Layer | Result |
| --- | --- |
| [v3.17](formal/KUOS/DependentOriginationPairwiseCorrelationCountermodelV3_17.lean) | Finite Boolean parity model: nested pairwise witnesses exist, but a global compatible family does not. |
| [v3.18](formal/KUOS/DependentOriginationSharedCoordinateRigidityV3_18.lean) | Nested pairwise witnesses plus shared-coordinate rigidity imply a global family and amalgamation. |
| [v3.19](formal/KUOS/DependentOriginationSharedCoordinateNormalizerV3_19.lean) | A supplied overlap-preserving gauge-fixing normalizer, preserving correction and yielding normalized shared rigidity, suffices. |
| [v3.20](formal/KUOS/DependentOriginationOverlapStarTransitivityV3_20.lean) | Nested pairwise witnesses plus overlap-star transitivity suffice; the empty route-state case is included. |
| [v3.21](formal/KUOS/DependentOriginationCylinderLocalityCountermodelV3_21.lean) | The parity model also has footprint-cylinder locality, which therefore does not by itself supply correlation. |

These countermodels concern abstract finite-footprint predicates. They do not instantiate an actual raw-system failure of `HigherLocalizationFactorization`. Conversely, the extra structures in v3.18–v3.20 are not asserted to exist automatically.

## 5. Integrated route equations and representative sectors: v3.22–v3.32

### A1.15 — Actual unitor and associator rigidity: v3.22–v3.25

[v3.22](formal/KUOS/DependentOriginationUnitorPartialRigidityV3_22.lean): within a corrected unitor locus, equality of the identity coordinate forces equality of its composition coordinate.

[v3.23](formal/KUOS/DependentOriginationAssociatorThreeOfFourRigidityV3_23.lean): for two gauges correcting one associator route, equality at `(f,g)`, `(g,h)`, and `(f,g ≫ h)` forces equality at `(f ≫ g,h)`, hence on that footprint. This is the proved orientation, not a claim that arbitrary whiskering can be cancelled in every orientation.

[v3.24](formal/KUOS/DependentOriginationUnitorStarTransitivityV3_24.lean): homogeneous stars close for three left unitors sharing a source, or three right unitors sharing a target. Their common-identity incidence is essential; an unrelated anchor could make overlap agreement vacuous.

[v3.25](formal/KUOS/DependentOriginationMixedUnitorRigidityV3_25.lean): actual left/right-unitor equations close mixed endpoint overlap when the common identity gauge agrees, including the identity/identity composition overlap.

### A1.16 — The genuine mixed incidence triangle: v3.26

[Source](formal/KUOS/DependentOriginationAssociatorUnitorTriangleResidualV3_26.lean)

```text
associator f (𝟙 Y) g
  -- shares gComp(f,𝟙 Y) with rightUnitor f
  -- shares gComp(𝟙 Y,g) with leftUnitor g

rightUnitor f and leftUnitor g share gId(Y).
```

Under correction of all three routes and both anchor-overlap agreements, triangle coherence gives equality after `Phi(eta) = F ◁ (eta ▷ G)`, with `F` and `G` the outer quotient representatives. The first result is double-whiskered equality, not unconditional literal equality of the middle identity gauge.

`MiddleIdentityWhiskerSeparating` is injectivity of this action. It closes the endpoint overlap. It is neither a global gluing axiom nor a universally assumed property; its kernel relation requires no linear structure.

### A1.17 — Concrete directional separation: v3.27–v3.28

[v3.27](formal/KUOS/DependentOriginationAssociatorUnitorWEdgeSeparationV3_27.lean) obtains separation from equivalences of both outer representative functors. Images of raw W-arrows provide a concrete sector.

[v3.28](formal/KUOS/DependentOriginationAssociatorUnitorOneSidedSeparationV3_28.lean) proves the more general sufficient criterion

```text
F.toFunctor.EssSurj + G.toFunctor.Faithful
  -> MiddleIdentityWhiskerSeparating W R D f g.
```

Essential surjectivity supports left-whiskering cancellation on natural transformations; faithfulness supports right-whiskering cancellation. The equivalence criterion factors through this one. Necessity of these conditions for separation is not asserted.

### A1.18 — Finite free-path propagation: v3.29

[Source](formal/KUOS/DependentOriginationFreePathDirectionalPropagationV3_29.lean)

Generator-level directional properties propagate through finite paths under the corresponding all-generator hypothesis. Formal W-inverse letters evaluate through chosen equivalences. Ordinary letters carry the relevant raw-functor property. This is path-level propagation, not itself a quotient-descent theorem.

### A1.19 — Selected-word certificates: v3.30

[Source](formal/KUOS/DependentOriginationQuotientRepresentativeDirectionalClosureV3_30.lean)

The all-generator assumptions are localized to the evaluated word using the inductive `PathEdgesSatisfy` evidence. Ordinary-letter EssSurj/Faithful certificates on `Quot.out f` and `Quot.out g` imply the semantic properties of the selected evaluations, then separation, then the actual mixed-triangle endpoint overlap under the unchanged three correction equations and two anchor agreements.

This remains a sufficient criterion and is now a special case of v3.31, not the latest canonical frontier.

### A1.20 / N1b — Quotient-equal semantic transport: completed in v3.31

[Source](formal/KUOS/DependentOriginationQuotientDirectionalPropertyTransportV3_31.lean) · [merged PR #1708](https://github.com/itakura-hidetoshi/KuuOS/pull/1708)

For fixed `W`, `R`, and `D`, reuse `equalInLocalization_hasEvaluationIso` from v2.58. Convert the local `Cat.Hom` isomorphism with `Cat.Hom.toNatIso`, then transport EssSurj and Faithful in both directions with Mathlib.

```text
[p] = [q] -> (EssSurj(eval p) <-> EssSurj(eval q))
[p] = [q] -> (Faithful(eval p) <-> Faithful(eval q)).
```

The exit criterion of the old N1b milestone is met. Only proposition-valued consequences are extracted from `Nonempty Iso`; no coherent family of evaluation isomorphisms is selected by these proofs.

### A1.21 / N2 — One good representative: completed in v3.31

The same module defines `HasOrdinaryEssSurjRepresentative` and `HasOrdinaryFaithfulRepresentative`. A certificate on any one representative transfers its semantic property to the selected `Quot.out` evaluation. The chosen-word certificates imply the new existential certificates.

The result reaches

```text
one good representative on each side
  -> left EssSurj + right Faithful
  -> MiddleIdentityWhiskerSeparating
  -> mixed-triangle endpoint overlap,
```

where the last step still needs the three corrected-route equations and both anchor agreements. Neither the certificate definition nor its existence selects a coherent transport family. The certificates contain no `D` or `Quot.out`, while the evaluated functors use the fixed `D`.

### A1.22 / N2 closure — Multiplicative certificate sectors: completed in v3.32

[Source](formal/KUOS/DependentOriginationCertifiedQuotientSectorClosureV3_32.lean) · [merged PR #1709](https://github.com/itakura-hidetoshi/KuuOS/pull/1709)

For an arbitrary path-category relation `r` and edge predicate `P`, `certifiedQuotientSector r P` consists of quotient arrows admitting at least one `P`-certified path. `pathEdgesSatisfy_comp` proves concatenation closure. The sector contains identities and is closed under composition, packaged as `MorphismProperty.IsMultiplicative`.

For every multiplicative `S`, the generic leastness theorem states

```text
certifiedQuotientSector r P <= S
  <-> forall edges e, P e -> S(quotient.map e.toPath).
```

Specialization gives both directional certificate sectors their identity/composition laws and generator tests. Composable certified pieces yield separation for the composed outer arrows via v3.31.

The quotient relation is arbitrary. No relation-invariance of the letterwise certificate is used. Minimality means least among multiplicative properties containing the specified generator images, not equivalence with semantic EssSurj/Faithful. Arbitrary-factor and inverse closure are not established.

## 6. Validated v3.33 and the remaining immediate units

### A1.23 / N3 progress — Semantic sectors and split separation: validated, unmerged

[Exact source](https://github.com/itakura-hidetoshi/KuuOS/blob/ba17572f2058819cd084d14dd31ac8678b446a3d/formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean) · [PR #1710](https://github.com/itakura-hidetoshi/KuuOS/pull/1710)

The v3.33 module reuses v2.61's local identity/composition isomorphism-existence results to prove semantic identity and composition laws. The resulting `quotientEssSurjSector` and `quotientFaithfulSector` are multiplicative and contain the corresponding certified sectors. Neither equality nor strict containment of these sectors is claimed.

It also proves directional reflection and its split consequence:

```text
EssSurj(eval(f ≫ g))  -> EssSurj(eval g)
Faithful(eval(f ≫ g)) -> Faithful(eval f)

s : Y ⟶ X, s ≫ f = 𝟙 Y -> EssSurj(eval f)
r : Z ⟶ Y, g ≫ r = 𝟙 Y -> Faithful(eval g)

both split equations
  -> MiddleIdentityWhiskerSeparating W R D f g.
```

The actual mixed-triangle theorem follows with all three correcting gauges and both anchor agreements still explicit. These are semantic, quotient-level sufficient conditions, not reflection of properties to every factor or letter, and not strict pseudofunctoriality.

Focused CI and both exact-head receipts succeeded for the listed head. The proof unit is checked; its integration is pending. It must not be described as either absent/unimplemented or already canonical.

### N0 — Integrate the validated v3.33 unit

Re-observe #1710's state, exact head, base, changed files, and completed receipts. If the head or base changed, use the current validation rather than the dated receipt above. Merge using the expected head, then re-observe main and record the theorem-bearing merge. Documentation-only merges do not complete this milestone.

### N1a — Syntactic certificate behavior remains a separate question

The old N1b/N2 semantic transport and representative-existence milestones are complete. Do not rebuild them as open work.

If needed for an algorithm or a stronger certificate theorem, study the ordinary-letter predicate under `id`, `comp`, `Winv₁`, and `Winv₂`, including both directions and relation contexts. Factorwise properties imply a composite property; the converse is not automatic. v3.33's directional semantic reflection is not a letterwise-invariance theorem.

Exit criterion: explicit preservation statements or a counterexample for the particular syntactic implication being tested. This is not a prerequisite retroactively imposed on v3.31/v3.32.

### N3 — Truth-test separation beyond the established sufficient conditions

v3.33 advances the positive side with quotient sections/retractions. The remaining task is to derive additional cancellation/detection conditions, or exhibit an actual Cat-valued generated example with two distinct middle 2-cells sharing the same double-whiskered image.

Exit criterion: an additional separating theorem or a concrete noninjectivity witness. Failure of a certificate, a split equation, EssSurj, or Faithful alone is not such a witness. Even noninjectivity would require a further bridge to incompatible actual correction data before implying factorization failure.

### N4 — Correlate witnesses using actual incidence geometry

Extend the route-specific results to the incidence sectors needed for one global compatible family. Potential routes are an actual overlap-preserving normalizer, a star-transitivity theorem with the necessary incidence hypotheses, or a directly constructed correlated family.

Both local correcting-witness existence and simultaneous compatibility must be justified. Additional separating sectors, their composition closure, and closure of one mixed triangle do not by themselves supply either requirement for all routes.

Exit criterion:

```text
explicit hypotheses on the actual generated route system
  -> HasGloballyCompatibleLocalCorrectionFamily W R D
  -> HasFiniteFootprintAmalgamation W R D
  -> coherent quotient transport via the established bridges.
```

Reuse the proved v3.15/v3.16 patching constructions. The unresolved step is the input family and its correlation, not gluing once that family exists.

### N5 — The two comparison equations and general Stage I

After the quotient stage, solve or characterize the two comparison `gIso` equations from the v3.02–v3.04 split and assemble the exact factorization interface.

```text
IsHigherWAdmissible W R
  -> HasHigherLocalizationFactorization (W := W) R
```

remains the broad research target. Exit criterion: general existence under the stated admissibility, or an exact obstruction characterization with every extra condition explicit. If a different higher carrier is needed, construct it and prove its comparison with the ordinary localization sector; nontrivial holonomy alone does not establish that need.

## 7. Stage II and the remaining universality tracks

### Track A2 — Coherent Stage-II universality

Construct chosen factorizations, comparison triangles from competitors, modifications, higher naturality, and presentation transport. `HasCoherentWeakHigherLocalizationUniversalProperty W R` is distinct from Stage-I existence. A carrier identification cannot be hidden in notation.

### Track B — Axis E: essential uniqueness

Retain `HigherWeakEssentialUniquenessObstruction` from the v2.42 E/R/A normal form and the sufficient v2.43–v2.54 routes. Derive natural detector families, cancellation hypotheses, or representability/contractibility conditions rather than adding them as unexplained inputs.

Exit criterion: essential uniqueness under a reusable set of explicit structural assumptions.

### Track C — Axis R: fixed coherent route

Retain `HigherFixedChosenForwardModificationTriangleObstruction`, stored correction equations, and arrowwise coherence equations. Compare this modification-triangle problem with correction-power semantics without collapsing distinct categorical levels.

Exit criterion: a checked equivalence between vanishing of the specified obstruction and existence of the required coherent correction/extension.

### Track D — Weak/coherent alignment

Assemble coherent existence and control of Axes E/R using the existing normal form. This is global theorem assembly, not a consequence of a local cancellation result.

### Track E — Minimal dependent-origination principles

Candidate principles remain contextuality, compositional transport, higher coherence, presentation invariance, descent, obstruction, and non-reification/authority boundaries. Separate mathematical data, properties, derivable conditions, and philosophical interpretations. Use countermodels to test non-implications and distinguish constructive proofs from classical selectors.

### Tracks F–H — Correct carrier, construction, representation

Do not preselect an ordinary category, bicategory, higher category, stack, scaled-simplicial object, or orthogonality completion as the final carrier solely by analogy. Decide through theorems about retained transport, correction, and truncation.

Construct `DO(C,W,J,H)` with presentation and choice independence, descent and coherence compatibility, and explicit obstruction semantics. A natural mapping/representation theorem with essential uniqueness completes the north star.

## 8. Parallel mathematical and AI workstreams

Parallel mathematical tracks remain fundamental-groupoid descent, information loss under quotient/truncation, scaled-simplicial higher realization, and cross-realization comparisons. Curvature-sensitive transport is not silently identified with ordinary homotopy-groupoid transport; each truncation needs a comparison theorem.

| AI workstream | Required behavior |
| --- | --- |
| Model migration | Carry semantic invariants, provenance, authority constraints, regression checks, canary promotion, and rollback evidence. |
| Memory integration | Check compatibility, retain contradiction witnesses and explicit obstructions, and avoid silent overwrite. |
| Retrieval | Use least-sufficient bounded escalation; unknown adequacy fails closed; retrieval is not entailment. |
| Multi-agent coordination | Distinguish pairwise valid handoffs from one globally compatible decision family and track authorized correction capabilities. |
| Control plane | Preserve `observe -> represent -> retrieve -> plan -> decide -> act -> re-observe -> verify`. |

Formal results guide these designs; they do not establish production safety or authorize external actions. No host or model receives automatic WORLD-commit, truth, rollback-proof, or memory-overwrite authority.

## 9. Verification and proof-engineering continuity

### Focused targets and their scope

On the canonical v3.32 tree:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCertifiedQuotientSectorClosureV3_32
```

In a checkout of the validated #1710 head `ba17572f2058819cd084d14dd31ac8678b446a3d`:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
```

The aggregate `KuuOSFormal` target is separate. The recorded focused receipts, including their dependencies, are not a fresh aggregate-validation claim. Historical imported-module linter warnings remain. Runtime validation is also separate: `PYTHONPATH=. python3 runtime/kuuos_current_check.py`.

The v3.32 and v3.33 CI runs used synthetic merge checkouts `bd777d163db93a94712dc4f96a97407a389f850d` and `e345655b329d34f8aab88778a75e582ea33747e7`. They published receipts on their respective PR heads; neither synthetic SHA is a final merge commit. Keep head, base, run, checkout, and final merge distinct.

At reentry, read PR state before waiting on CI. If merged, do not return to an old run. If its head changes, update the tracked SHA/run/job. Use completed logs for failures and the current-head receipts for success. Re-observe main after any merge. No continuing post-chat monitoring is implied.

### Lessons retained from v3.26–v3.33

**Dependent equality and recursion.** Keep `eqToHom` transport explicit; use small typed equalities, `congrArg`, and limited reassociation. Imported declarations do not export the caller's `open` commands. Preserve `autoImplicit false`, the inductive `PathEdgesSatisfy` uniform parameters and `@P`, and its actual recursor binders. Induct on the evidence and reduce evaluator `cons` directly when appropriate.

**Original quiver versus path-category quiver.** `X.as : Paths V` must not make constructor inference choose the path-category quiver instead of the original edge quiver. v3.32's explicit form is `@PathEdgesSatisfy.nil V Q (@P) X.as`.

**Ordinary versus strict implicit endpoints.** The older certificates use ordinary implicit `{X Y}` arguments; partial application can insert endpoint metavariables. At higher-order `MorphismProperty` boundaries, retain the full family explicitly:

```lean
((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
  HasOrdinaryEssSurjRepresentative W R f) : MorphismProperty W.Localization)
```

A postfix type annotation or fully qualified API name alone did not fix this boundary. New semantic sector definitions in v3.33 are declared directly as `MorphismProperty`.

**Pass existing evidence rather than rediscover it.** v3.32 names `[hS : S.IsMultiplicative]` and passes `hS` explicitly across the `W.Localization`/generic `Quotient` carrier boundary. Composition proofs similarly pass existing EssSurj/Faithful witnesses to the pinned Mathlib declarations.

**Normalize natural-isomorphism endpoints before property transport.** v3.33's four errors came from requesting instances on `(𝟙 C).toFunctor` or `(F ≫ G).toFunctor`. Typed `have eNat : ... := Cat.Hom.toNatIso e` declarations expose the ordinary identity/composite functors. This preserves the quotient composition isomorphism; it does not replace it by a strict equality or assume coherence.

References: Lean's [implicit parameters](https://lean-lang.org/doc/reference/latest/Terms/Functions/), [instance synthesis](https://lean-lang.org/doc/reference/latest/Type-Classes/Instance-Synthesis/), and [type ascription](https://lean-lang.org/doc/reference/latest/Terms/Type-Ascription/); pinned Mathlib [MorphismProperty](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/MorphismProperty/Basic.lean), [localization construction](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Localization/Construction.lean), and [Cat wrappers](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/CategoryTheory/Category/Cat.lean). The pinned revision, not an unverified latest API name, governs the proofs.

No Lean source, dependency, compiler option, or workflow is changed by this documentation refresh. A docs-only successful gate is not a new mathematical validation.

## 10. Non-implications and completion criteria

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
some certified representative -> every representative certified
certificate-sector minimality -> exact semantic characterization
semantic composite property -> that property for every factor or letter
failure of a sufficient criterion -> noninjectivity
noninjectivity alone -> general factorization failure
validated unmerged PR -> canonical integration
conditional Stage-I result -> coherent universal property
runtime or model output -> canonical theorem authority.
```

Completion requires correctly scoped and formally checked existence, coherent factorization, essential uniqueness, presentation invariance, descent compatibility, higher coherence, explicit obstruction/correction boundaries, and a natural representation theorem.

Keep the labels distinct: **proved**, **conditionally proved**, **classical**, **constructive**, **abstractly refuted**, **open**, **validated/unmerged**, **canonical/integrated**, **validation-only**, **interpretive**, and **operational**.
