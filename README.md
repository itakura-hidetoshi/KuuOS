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
| Latest integrated theorem layer | **v3.66 — countermodel quotient representatives are identity 1-cells** |
| Latest theorem-bearing merge | [PR #1748](https://github.com/itakura-hidetoshi/KuuOS/pull/1748), merged 2026-09-23 JST |
| Theorem baseline | `8f1a5006dd43afb6d4c9b8ae583ed6f5abab78d9` |
| Validated #1748 PR head | `383dd616ef9b15c1ecfcac23fd8de4f65b4bc6fa` |
| Exact-head governance run | [run 35847500021](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35847500021), completed / success |
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

The formerly separate v2.69–v3.14 frontier is integrated history. The canonical theorem spine now continues through v3.66. The separate Lean 4.31 validation-only PR #1558 remains **open / Draft / unmerged** and outside theorem authority; it must not be merged, marked Ready for review, or auto-merged.

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

## Latest result: the remaining concrete question is purely 2-cell coherence

The v3.53–v3.66 sequence has sharpened the fresh-boundary problem far beyond the v3.52 collision-closure result.

The current strongest concrete conclusion is:

```text
v2.69 C2 countermodel
+ all localization arrows invertible
+ every quotient representative functor an equivalence
+ every selected quotient representative 1-cell literally = identity
+ one fixed gauge corrects every unitor
+ another theorem gives a fixed gauge failing a selected associator
+ generated relation-loop 2-cell holonomy remains nontrivial
```

The last two bullets must be read carefully. v3.64–v3.65 prove that **there exists a bad fixed gauge** which corrects every unitor but does not correct every associator. They do **not** prove that every gauge fails, and they do **not** prove that no fully coherent quotient gauge exists.

v3.66 then removes the 1-cell assignment from the remaining concrete truth test:

```lean
counterQuotientRepresentativeMap_eq_identity
```

For every localization arrow in the concrete C2 model, the selected `Quot.out` representative evaluates to the identity `Cat.Hom`. This coexists with the already-proved nontrivial generated 2-cell holonomy.

Therefore the immediate frontier is no longer:

```text
can the quotient 1-cell assignment descend?
```

but:

```text
can mapId / mapComp 2-isomorphisms be chosen simultaneously
so that associator + left-unitor + right-unitor coherence all hold?
```

That is exactly the `CoherentQuotientTransportData` / joint-correction question.

## v3.53–v3.66: fresh-boundary reduction and concrete C2 truth test

| Layer | Integrated result |
| --- | --- |
| [v3.53](formal/KUOS/DependentOriginationFreshBoundaryRightIdentityReductionV3_53.lean) | Splits the fresh/unitor-visible boundary: the right-identity branch is semantically recovered from common right unitors; only the composite-identity branch remains. |
| [v3.54](formal/KUOS/DependentOriginationCompositeIdentityInversePairReductionV3_54.lean) | Under Epi/Mono cancellation, `f ≫ g = 𝟙` becomes a two-sided inverse pair. |
| [v3.55](formal/KUOS/DependentOriginationInversePairBoundaryObstructionV3_55.lean) | Names the exact remaining fresh-boundary obstruction: fresh boundary + inverse pair + failure of the solved leading equation. Representative EssSurj/Faithful separation is no longer the issue. |
| [v3.56](formal/KUOS/DependentOriginationInversePairRepresentativeEquivalenceV3_56.lean) | Upgrades quotient representatives of inverse-pair arrows to actual functor equivalences. |
| [v3.57](formal/KUOS/DependentOriginationSourceComplementsGroupoidV3_57.lean) | Left+right source complements force the entire ordinary localization to be a groupoid; all quotient representatives become equivalences. |
| [v3.58](formal/KUOS/DependentOriginationGroupoidHolonomySeparationV3_58.lean) | In the v2.69 `allMorphisms` model, groupoid localization + representative equivalence coexist with nontrivial generated holonomy. |
| [v3.59](formal/KUOS/DependentOriginationInversePairSuffixPerturbationV3_59.lean) | Shows that changing one isolated nontrivial suffix coordinate can preserve unitors and destroy one inverse-pair associator, given a corrected baseline. |
| [v3.60](formal/KUOS/DependentOriginationNontrivialSuffixObstructionV3_60.lean) | Removes the corrected-baseline assumption: common unitors + fresh inverse-pair geometry + a nontrivial isolated suffix fiber force existence of some bad fixed gauge. |
| [v3.61](formal/KUOS/DependentOriginationCounterGaugeFiberNontrivialV3_61.lean) | Proves directly that every composition-coordinate quotient-gauge fiber in the concrete C2 model is nontrivial. |
| [v3.62](formal/KUOS/DependentOriginationInversePairIncidenceV3_62.lean) | Reduces fresh-boundary and suffix-isolation incidence to simple object inequalities around an inverse pair. |
| [v3.63](formal/KUOS/DependentOriginationOctahedralInversePairV3_63.lean) | Constructs an explicit octahedral inverse-pair task using Mathlib localization `wIso/wInv`, distinct localization objects, and the exact nontrivial suffix fiber. |
| [v3.64](formal/KUOS/DependentOriginationUniversalUnitorGaugeV3_64.lean) | Proves that one fixed quotient gauge correcting **all** left/right unitors always exists; specializes this to the concrete C2 model and obtains an exact fixed-gauge inverse-pair obstruction. |
| [v3.65](formal/KUOS/DependentOriginationFixedGaugeUnitorAssociatorSeparationV3_65.lean) | Packages the same-gauge separation: all unitors corrected at `Q` does not force all associators, nor all quotient routes, corrected at the same `Q`. This is not global uncorrectability. |
| [v3.66](formal/KUOS/DependentOriginationCounterRepresentativeIdentityV3_66.lean) | Proves every free-path evaluation and every selected quotient representative 1-cell in the C2 model is literally the identity, while nontrivial generated 2-cell holonomy remains. |

This sequence changes the interpretation of the frontier. The concrete problem is now entirely two-dimensional: **simultaneous 2-cell coherence**, not 1-cell descent or representative equivalence.

## Earlier N4 progression retained: incidence, schedules, boundary equations, and collision closure

The v3.35–v3.52 chain remains essential infrastructure:

| Range | Established contribution |
| --- | --- |
| v3.35–v3.40 | Common unitor correlation, boundary reduction, unique fresh completion, finite/countable stabilization, and same-gauge middle-identity semantic recovery. |
| v3.41–v3.46 | Literal associator-incidence decomposition, safe ranked scheduling, lower-rank finiteness analysis, and locally finite countable enumeration. |
| v3.47 | Reduces each fresh/unitor-visible boundary task to one exact leading-coordinate equation. |
| v3.48–v3.50 | Turns coordinate collision into object degeneracy, absorption, and left-identity semantic recovery. |
| v3.51–v3.52 | Supplies collision cancellation from source `W)-composite data and globalizes Epi/Mono cancellation under explicit source-complement geometry. |

v3.53–v3.66 do not replace those results. They take the last v3.47/v3.52 boundary equation and push it through inverse-pair geometry into a concrete C2 truth test.

## Canonical formal spine

| Layers | Established role |
| --- | --- |
| v2.0–v2.10 | Ordinary localization, W + J sectors, stack descent, and the higher-localization factorization interface. |
| v2.11–v2.54 | Weak/coherent distinctions, correction and modification triangles, the E/R/A obstruction normal form, and structural sufficient routes. |
| v2.55–v2.68 | Restricted existence, W-adjoint equivalences, free-path evaluation, quotient-equal path isomorphisms, the five-law coherence package, generated 2-cells and holonomy. |
| v2.69–v2.95 | Octahedral C2 truth test; generated-holonomy nontriviality, correction authority, correctability, and constructive/classical boundaries. |
| v2.96–v3.04 | Five compatible gauge equations split into three quotient equations and two comparison equations. |
| v3.05–v3.14 | Quotient correction loci, witness-correlation gap, finite dependent-coordinate footprints, and literal shared-coordinate keys. |
| v3.15–v3.21 | Explicit pair extension and gluing from one compatible family; abstract countermodels; rigidity and star-transitivity sufficient criteria. |
| v3.22–v3.34 | Actual route-equation rigidity, mixed-triangle residual, directional cancellation, free-path propagation, semantic representative transport, split-arrow and source-`W)-composite separation. |
| v3.35–v3.40 | Common unitor correlation, fresh completion, schedule stabilization, and middle-identity semantic recovery. |
| v3.41–v3.52 | Actual incidence decomposition, ranked scheduling, fresh-boundary equation, collision absorption, left-identity recovery, and source-complement cancellation closure. |
| v3.53–v3.58 | Fresh-boundary right-identity reduction, inverse-pair reduction, representative equivalence, groupoid localization, and groupoid/holonomy separation. |
| v3.59–v3.63 | Isolated-suffix perturbation, abstract nontrivial-fiber obstruction, concrete C2 fiber nontriviality, incidence reduction, and an explicit octahedral inverse-pair task. |
| v3.64–v3.66 | Universal common-unitor gauge, fixed-gauge unitor/associator separation, and collapse of every concrete quotient representative 1-cell to identity. |

The retained sufficient implication

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R
```

is still valid. The converse direction is not established, and nontrivial generated holonomy is not by itself a proof of factorization impossibility.

## Current mathematical boundary: explicit coherent 2-cell transport

The next concrete theorem unit should truth-test an explicit

```lean
CoherentQuotientTransportData
  (W := allMorphisms)
  counterSystem
  counterD
```

using the v3.66 fact that every quotient representative 1-cell is identity.

There are two logically distinct possible outcomes.

### Outcome A — explicit coherent quotient transport exists

If explicit `mapId` and `mapComp` 2-isomorphisms satisfying the associator and two unitor laws can be constructed, then:

```text
nontrivial generated holonomy
+ existence of a bad common-unitor gauge
does not prevent
existence of a different fully coherent quotient gauge.
```

This would show that v3.65 is genuinely **gauge-specific**, not a global obstruction theorem.

### Outcome B — no coherent quotient transport exists

This cannot be concluded from v3.65. It would require a new **gauge-independent invariant** proving that every candidate gauge misses the common correction locus.

The already-established equivalences from v3.08–v3.11 remain the exact logical interface:

```text
ThreeQuotientRoutesJointlyCorrectable
  <-> one Q corrects every quotient route
  <-> commonQuotientRouteCorrectionLocus is nonempty
  <-> HasCoherentQuotientTransportData.
```

The next truth test should therefore target this existence question directly, rather than perturbing another single coordinate.

After the three quotient equations are settled, the two comparison `gIso` equations from the v3.02–v3.04 split remain the next Stage-I assembly problem.

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

These are engineering interpretations and design directions, not deployment guarantees established by the Lean theorems. Local agreement must not be confused with one globally correlated decision family. Whether a discrepancy is hard also depends on the corrections actually authorized.

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
  build KUOS.DependentOriginationCounterRepresentativeIdentityV3_66
```

For PR #1748, exact head

```text
383dd616ef9b15c1ecfcac23fd8de4f65b4bc6fa
```

was validated by governance run [35847500021](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35847500021). The Strict Lean formal validation job, dependency-manifest verification, governance summary, Lean completion receipt, and exact-head terminal receipt all completed with `success`. That exact head was merged as theorem commit

```text
8f1a5006dd43afb6d4c9b8ae583ed6f5abab78d9
```

and the post-merge comparison with `main` was identical before this documentation refresh.

The aggregate formal target can be checked separately:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

The focused v3.66 receipt is **not** a claim that a fresh aggregate `KuuOSFormal` build was run. The effect-free runtime entry point remains:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a mathematical theorem. A CI receipt applies only to its exact head and recorded checkout. Queued/running checks are not success, an old-head success is not a new-head success, and a docs-only gate does not constitute theorem validation.

### Recent proof-engineering lessons

- **Import is not open.** A transitive import makes declarations available in the environment but does not put their short names into scope. Open the defining namespace explicitly or use a qualified name.
- **Keep `autoImplicit false`.** Unknown identifiers should fail closed instead of silently becoming implicit variables.
- **Do not overuse `simpa using` on Iso laws.** A source proposition can simplify all the way to `True`; prefer direct `exact iso.hom_inv_id` / `inv_hom_id` when the target is definitionally the same theorem.
- **Name dependent witnesses.** For `Localization.Construction.wIso/wInv`, keeping the `W w` proof in one named definition avoids proof-argument mismatch in dependent terms.
- **Use `Functor.hext` intentionally.** Its map field is HEq because object equalities are dependent. In v3.66, `SingleObj C2 = Unit` was made explicit and ordinary equality was converted with `.heq`; hidden target typeclass search was avoided.
- **Use `Cat.Hom.ext` at the wrapper boundary.** Prove the underlying functor equality first, then lift it to equality of protected Cat 1-morphisms.
- **Dependent constructor injection remains hazardous.** Object equalities and HEq may appear before morphism-field equalities; normalize the dependent geometry first.
- **Typeclass search need not unfold packaged projections.** Use an explicit `change` to the literal carrier before `infer_instance` when necessary.
- **Use typed `eqToHom` transport.** Do not silently identify dependent composition coordinates.
- **Track CI by exact current head.** Re-read PR head, Strict Lean receipt, and exact-head terminal receipt before declaring GREEN; merge with an expected head SHA and fresh-compare `main`.

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
one bad fixed gauge != global uncorrectability
all unitors corrected at Q != all associators corrected at Q
identity quotient representatives != coherent mapId/mapComp automatically
groupoid localization != 2-cell coherence
abstract correlation countermodel != an actual-system counterexample
Stage-I factorization != Stage-II universality
execution host != truth, WORLD-commit, or memory-overwrite authority
```

**Current research sentence:** KuuOS has reduced the concrete v2.69 quotient-stage truth test to a pure 2-cell coherence problem: every selected quotient representative 1-cell is now proved to be identity, while generated 2-cell holonomy can remain nontrivial; the next decisive theorem is whether a fully coherent `mapId/mapComp` family exists, or whether a genuinely gauge-independent 2-cell obstruction survives every quotient gauge choice.
