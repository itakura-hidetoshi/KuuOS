# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophy, mathematical presentations, formal proofs, and operational systems inform one another without being treated as interchangeable evidence.

## Canonical snapshot — 2026-09-23 JST

| Item | Verified reference |
| --- | --- |
| Canonical branch | `main` |
| Latest integrated theorem layer | **v3.52 — global localization cancellation from source complements** |
| Latest theorem-bearing merge | [PR #1733](https://github.com/itakura-hidetoshi/KuuOS/pull/1733), merged 2026-09-23 JST |
| Theorem baseline | `7e01b3cfe468dbf870f13ded04f85e2595ecb81f` |
| Pre-docs-refresh `main` | `7e01b3cfe468dbf870f13ded04f85e2595ecb81f` |
| Validated #1733 PR head | `380565c1a09d182272136525bc0d8868f4cda9c7` |
| Exact-head governance run | [run 35801551701](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35801551701), completed / success |
| Exact-head receipts | Strict Lean formal validation = success; exact-head terminal = success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

This is a dated theorem snapshot, not a permanently current branch pointer. A **documentation-only** merge after this snapshot may advance `main` without advancing the theorem baseline. Re-observe GitHub before continuing formal work.

Authority order remains:

```text
fresh exact canonical GitHub SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > CI and runtime receipts
  > history / memory
```

The formerly separate v2.69–v3.14 frontier is integrated history. The canonical theorem spine now continues through v3.52. The separate Lean 4.31 validation-only PR #1558 remains **open / Draft / unmerged** and outside theorem authority; it must not be merged, marked Ready for review, or auto-merged.

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

## Latest result: collision cancellation is global under explicit source-complement geometry

The canonical v3.41–v3.52 sequence has narrowed the quotient-stage associator problem from an undifferentiated collision residual to explicit, separately testable mechanisms.

The current strongest collision result is v3.52. Define source-level hypotheses saying that every raw arrow can be completed on the left or right to a composite in `W`:

```text
HasLeftWCompositeComplements W
HasRightWCompositeComplements W
```

v3.34 constructs split epi / split mono localization arrows from such source composites. v3.52 then uses Mathlib's canonical localization induction

```lean
Localization.Construction.morphismProperty_eq_top
```

to globalize those properties from source images, formal `W`-inverses, and composition to **every morphism of `W.Localization`**. Consequently, under both global source-complement hypotheses,

```text
every localization arrow is Epi
every localization arrow is Mono
```

and the categorical cancellation assumptions used in v3.49–v3.50 are available for every actual collision residual.

This closes the following chain:

```text
actual non-middle leading collision
  -> object degeneracy                         [v3.48]
  -> absorption equations                      [v3.49]
  -> left-identity associator under Epi/Mono   [v3.49]
  -> corrected by common left unitors          [v3.50]
  -> Epi/Mono supplied by source W-composites  [v3.51]
  -> global Epi/Mono under source complements  [v3.52]
```

The resulting v3.52 adapter

```lean
corrects_all_associators_of_boundaryCompatible_of_sourceComplements
```

says that, for one fixed quotient gauge, the existing common-unitor correction, nonresidual correction, fresh-boundary compatibility equations, and the two global source-complement hypotheses together imply correction of **every associator task**.

This is an important closure theorem, but it is conditional. v3.52 does **not** prove the global source-complement hypotheses from weak admissibility, and it does **not** make fresh-boundary compatibility automatic.

## N4 progression: actual incidence, schedules, boundary equations, and collision closure

The canonical progression after v3.40 is:

| Layer | Integrated result |
| --- | --- |
| [v3.41](formal/KUOS/DependentOriginationAssociatorIncidenceDecompositionV3_41.lean) | Decomposes actual associator incidence into middle identity, fresh/interior, and residual sectors using literal dependent `QuotientGaugeCoordinate` equalities. |
| [v3.42](formal/KUOS/DependentOriginationFreshInteriorGlobalCoverageV3_42.lean) | Shows finite/countable/global safe fresh-interior coverage gives one common gauge correcting every nonresidual associator. |
| [v3.43](formal/KUOS/DependentOriginationFiniteRankedScheduleV3_43.lean) | Constructs finite forward-noninterfering schedules from an actual dependency rank that strictly decreases along dependency. |
| [v3.44](formal/KUOS/DependentOriginationCountableRankedEnumerationV3_44.lean) | Turns a rank-monotone injective enumeration into a safe countable schedule. |
| [v3.45](formal/KUOS/DependentOriginationLowerRankFinitenessV3_45.lean) | Proves finite lower-rank coverage is necessary for the chosen countable rank-monotone scheduling strategy. |
| [v3.46](formal/KUOS/DependentOriginationLocallyFiniteRankedEnumerationV3_46.lean) | Derives a greedy countable rank-monotone enumeration from finite rank sublevels; countability is proved rather than assumed. |
| [v3.47](formal/KUOS/DependentOriginationFreshBoundaryCompatibilityV3_47.lean) | Reduces each fresh/unitor-visible boundary residual to one exact leading-coordinate compatibility equation. |
| [v3.48](formal/KUOS/DependentOriginationCollisionObjectGeometryV3_48.lean) | Projects literal leading-coordinate collisions to unavoidable adjacent object degeneracy. |
| [v3.49](formal/KUOS/DependentOriginationCollisionAbsorptionReductionV3_49.lean) | Extracts absorption equations and reduces the non-middle collision residual to a left-identity associator under ordinary Epi/Mono cancellation. |
| [v3.50](formal/KUOS/DependentOriginationLeftIdentitySemanticRecoveryV3_50.lean) | Proves `associator (𝟙 X) g h` is semantically corrected by the same gauge once the left-unit routes at `g` and `g ≫ h` are corrected. |
| [v3.51](formal/KUOS/DependentOriginationWCompositeCollisionClosureV3_51.lean) | Supplies the v3.49 Epi/Mono hypotheses for source-presented residual tasks from concrete `W`-composite split data. |
| [v3.52](formal/KUOS/DependentOriginationGlobalCancellationFromSourceComplementsV3_52.lean) | Uses Mathlib localization induction to globalize source-complement cancellation to every localization arrow, removing the per-task source-presentation requirement under explicit global source geometry. |

The earlier v3.35–v3.40 common-unitor and same-gauge middle-identity results remain part of this chain. v3.41–v3.52 do not replace them; they use them as the already correlated coherence sector.

## Canonical formal spine

| Layers | Established role |
| --- | --- |
| v2.0–v2.10 | Ordinary localization, W + J sectors, stack descent, and the higher-localization factorization interface. |
| v2.11–v2.54 | Weak/coherent distinctions, correction and modification triangles, the E/R/A obstruction normal form, and structural sufficient routes. |
| v2.55–v2.68 | Restricted existence, W-adjoint equivalences, free-path evaluation, quotient-equal path isomorphisms, the five-law coherence package, generated 2-cells and holonomy. |
| v2.69–v2.95 | Octahedral truth test; obstruction, correctability, authority, extensional correction power, and constructive/classical boundaries. |
| v2.96–v3.04 | Five compatible gauge equations split into three quotient equations and two comparison equations. |
| v3.05–v3.14 | Quotient correction loci, witness-correlation gap, finite dependent-coordinate footprints, and literal shared-coordinate keys. |
| v3.15–v3.21 | Explicit pair extension and gluing from one compatible family; countermodels; rigidity and star-transitivity sufficient criteria. |
| v3.22–v3.34 | Actual route-equation rigidity, mixed-triangle residual, directional cancellation, free-path propagation, semantic representative transport, split-arrow and source-`W)-composite separation. |
| v3.35–v3.40 | Common unitor correlation, boundary reduction, fresh completion, finite/countable stabilization, and same-gauge middle-identity semantic recovery. |
| v3.41–v3.47 | Actual incidence decomposition, ranked scheduling, local-finiteness/countability, and exact fresh-boundary compatibility. |
| v3.48–v3.52 | Collision object geometry, absorption cancellation, left-identity semantic recovery, source-`W)-composite closure, and global cancellation from source complements. |

The retained sufficient implication

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R
```

is still valid, but v2.69 prevents replacing its premise by weak admissibility without additional proof. The later constructive program does not erase that truth test; it narrows the missing hypotheses and converts broad residuals into exact structural conditions.

## Next mathematical boundary: fresh-boundary closure and weaker cancellation certificates

The quotient-stage frontier is now much sharper than at v3.40.

First, v3.47 leaves an exact equation on each fresh but unitor-visible boundary task:

```text
current leading gauge value
  =
unique solved associator-leading value.
```

The next central question is whether this compatibility follows automatically from already correlated unitor / associator structure under reusable hypotheses, or whether it is a genuine remaining obstruction that must be retained explicitly.

Second, v3.52 uses strong **global** source-complement hypotheses to make every localization arrow epi/mono. This is a sufficient route, not a characterization. A natural refinement is to weaken it to local certificates only on the `Quot.out` words or representatives that actually occur in collision residuals, reusing the v3.29–v3.32 path and representative machinery.

The near-term theorem sequence is therefore:

```text
fresh-boundary compatibility
  -> automatic theorem under structural hypotheses
     OR exact residual obstruction

global source complements
  -> weaken to selected-word / representative cancellation certificates

sufficient quotient-stage all-associator correction
  -> solve the two comparison gIso equations
  -> assemble general Stage I higher-localization factorization
```

Schedule independence, seed independence, and general `W/R/D` independence are not proved by the ranked constructions. They remain separate presentation-invariance questions rather than hidden consequences of existence.

After quotient-stage coverage is sufficient, the two comparison `gIso` equations from v3.02–v3.04 remain the next Stage-I assembly problem. Stage-II coherent universality and the final `DO(C,W,J,H)` representation theorem remain distinct later milestones.

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

The pinned environment is recorded in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json). The focused current theorem target is:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
```

For PR #1733, exact head

```text
380565c1a09d182272136525bc0d8868f4cda9c7
```

was validated by governance run [35801551701](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35801551701). The Strict Lean formal validation job, dependency-manifest verification, governance summary, Lean completion receipt, and exact-head terminal receipt all completed with `success`. That exact head was then merged as theorem commit

```text
7e01b3cfe468dbf870f13ded04f85e2595ecb81f
```

and the post-merge comparison with `main` was identical before this documentation refresh.

The aggregate formal target can be checked separately:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

The focused v3.52 receipt is **not** a claim that a fresh aggregate `KuuOSFormal` build was run. The effect-free runtime entry point remains:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a mathematical theorem. A CI receipt applies only to its exact head and recorded checkout. Queued/running checks are not success, an old-head success is not a new-head success, and a docs-only gate does not constitute theorem validation.

Recent proof-engineering lessons retained in the canonical workflow include:

- import does not open a namespace; short theorem names must be explicitly opened or qualified;
- dependent constructors may make `injection` expose object equalities / heterogeneous equalities before morphism fields; normalize dependent equalities before claiming homogeneous field equalities;
- typeclass search need not unfold packaged dependent projections far enough; use an explicit `change` to the literal carrier before `infer_instance`;
- lemmas such as `MorphismProperty.epimorphisms.iff` are functions of a morphism, so in term mode the morphism must be applied before `.mp` / `.1`;
- use typed `eqToHom` transport rather than silently identifying dependent composition coordinates;
- track CI by the exact current PR head, merge with an expected head SHA, and freshly compare post-merge `main`.

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

**Current research sentence:** KuuOS has now formalized an actual associator-incidence pipeline through v3.52: nonresidual fresh/interior tasks admit explicit ranked scheduling under stated finiteness hypotheses; fresh boundary tasks are reduced to exact leading-compatibility equations; non-middle collision residuals reduce through object geometry, absorption, and same-gauge unitor coherence; and global source-complement geometry supplies cancellation for every localization arrow. The principal remaining quotient-stage boundary is fresh-boundary compatibility together with weakening the strong global source-complement hypothesis. Comparison `gIso` equations and general Stage I remain separate after that, followed by coherent Stage II and the final dependent-origination representation theorem.