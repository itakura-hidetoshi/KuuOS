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
| Latest integrated theorem layer | **v3.40 — semantic preservation of the middle-identity collision sector** |
| Latest theorem-bearing merge | [PR #1719](https://github.com/itakura-hidetoshi/KuuOS/pull/1719), merged 2026-09-22 |
| Theorem baseline | `243e6e2a990ddb319e84f3722478539641d0a5e3` |
| Pre-docs-refresh `main` | `243e6e2a990ddb319e84f3722478539641d0a5e3` |
| Validated #1719 PR head | `e6f8dc72a5188aa3c5b913d89351711232d2201a` |
| Exact-head governance run | [run 35715231469](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35715231469), completed / success |
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

The formerly separate v2.69–v3.14 frontier is integrated history. The canonical theorem spine now continues through v3.40. The separate Lean 4.31 validation-only PR #1558 remains **open / Draft / unmerged** and outside theorem authority; it must not be merged, marked Ready for review, or auto-merged.

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

## Latest result: collision-sector preservation through one common gauge

The latest theorem layer does **not** remove the middle-identity collision by manufacturing a fresh pivot. v3.37 already proved that the genuine route

```text
associator f (𝟙 Y) g
```

fails the fresh-leading-coordinate condition. v3.40 instead proves that this collision sector can be recovered semantically from unitors when the same quotient gauge is used.

For one gauge `Q`, the central implication is:

```text
Q corrects rightUnitor f
Q corrects leftUnitor g
--------------------------------
Q corrects associator f (𝟙 Y) g
```

Formally this is `middleIdentityAssociator_corrected_of_unitors` in
[DependentOriginationCollisionSectorPreservationV3_40.lean](formal/KUOS/DependentOriginationCollisionSectorPreservationV3_40.lean).

The proof uses the actual right- and left-unitor equations of the same adjusted family, Mathlib bicategory triangle coherence, associator naturality, explicit `eqToHom` transport for dependent outer composition coordinates, and ordinary categorical cancellation of an invertible suffix. It does **not** assume injectivity of double whiskering on two unrelated endpoint gauges.

That distinction preserves the earlier v3.26–v3.34 separation results. Those layers ask when independently chosen correcting witnesses can be forced to agree. v3.40 runs in the opposite direction: once one common gauge already carries both unitor equations, their shared identity correction is literally the same value.

v3.40 also proves an incidence obstruction to the naïve freezing strategy: every scheduled leading composition key occurs in some middle-identity associator footprint. Therefore a nonempty update schedule cannot avoid **all** middle-identity footprints. The bridge is semantic preservation of correction, not global footprint avoidance.

The resulting common-gauge theorem is:

```lean
exists_commonGauge_for_middleIdentity_and_countableSchedule_of_pairwiseShared
```

Under the same nested pairwise premise used in v3.39, together with per-task freshness, forward noninterference, and unitor-interiority for one prescribed countable schedule, one gauge simultaneously corrects:

```text
all left/right unitors
all middle-identity associators  associator f (𝟙 Y) g
every task in the prescribed countable fresh schedule
```

No countable enumeration of all middle-identity associators is needed.

## N4 progression: from local incidence to simultaneous witnesses

The recent canonical spine is:

| Layer | Integrated result |
| --- | --- |
| [v3.33](formal/KUOS/DependentOriginationQuotientSplitDirectionalSeparationV3_33.lean) | Semantic EssSurj/Faithful sectors, directional reflection, and split-arrow sufficient separation. |
| [v3.34](formal/KUOS/DependentOriginationWCompositeSplitSeparationV3_34.lean) | Constructs split epi/mono localization arrows from source composites in `W`; strengthens the concrete separation route without assuming new coherence. |
| [v3.35](formal/KUOS/DependentOriginationUnitorWitnessCorrelationV3_35.lean) | Correlates the entire actual unitor subsystem into one compatible family and hence one common unitor gauge under the nested pairwise premise. |
| [v3.36](formal/KUOS/DependentOriginationAssociatorUnitorBoundaryReductionV3_36.lean) | Separates unitor-visible boundary tests from residual associator-interior overlap tests. |
| [v3.37](formal/KUOS/DependentOriginationFreshAssociatorCompletionV3_37.lean) | Solves one actual associator by a unique leading-coordinate update when that leading key is fresh; explicitly shows middle-identity freshness fails. |
| [v3.38](formal/KUOS/DependentOriginationFiniteAssociatorScheduleV3_38.lean) | Sequentially processes a finite fresh forward-noninterfering schedule into one common gauge while preserving all unitors. |
| [v3.39](formal/KUOS/DependentOriginationCountableAssociatorStabilizationV3_39.lean) | Extends one prescribed safe schedule to `ℕ) by exact dependent-coordinate stabilization, not compactness or a topological limit. |
| [v3.40](formal/KUOS/DependentOriginationCollisionSectorPreservationV3_40.lean) | Adds the whole middle-identity collision sector to that same common gauge semantically through preserved unitor equations. |

The combined picture is therefore no longer merely “pairwise local witnesses versus a global family.” There is now a concrete constructive sector in which simultaneous witness correlation has been built.

## Canonical formal spine

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
| v3.31–v3.34 | Semantic representative invariance, certified/semantic multiplicative sectors, directional reflection, split-arrow criteria, and source-`W)-composite realizations. |
| v3.35–v3.40 | Actual unitor correlation, boundary reduction, fresh local associator completion, finite/countable sequential stabilization, and semantic preservation of the middle-identity collision sector. |

The retained sufficient implication

```text
GeneratedHolonomyTrivial W R D
  -> HasHigherLocalizationFactorization (W := W) R
```

is still valid, but v2.69 prevents replacing its premise by weak admissibility without additional proof. The later correction program does not erase that truth test; it develops constructive routes around explicit obstructions.

The v3.15/v3.16 finite patching machinery is also still available. What changed in v3.35–v3.40 is that a significant part of the required simultaneous family is now constructed from actual incidence equations rather than postulated globally.

## Next mathematical boundary: actual incidence decomposition

The next theorem unit is not “finite → countable → uncountable.” It is to classify the actual associator incidence geometry into sectors that are handled by different already-proved mechanisms:

```text
unitor-generated collision sector
  ⊔ fresh schedulable sector
  ⊔ residual obstruction sector
```

The intended interpretation is:

1. **Unitor-generated collision sector.** Routes such as `associator f (𝟙 Y) g` are not fresh, but their correction follows from the same common unitor gauge by v3.40.
2. **Fresh schedulable sector.** Associators satisfying the v3.37 freshness condition and admitting an ordering with v3.39 forward noninterference can be accumulated by exact coordinate stabilization.
3. **Residual obstruction sector.** Remaining collision patterns must stay explicit until a separation, alternative completion, or genuine obstruction theorem handles them.

The next formal task is to derive this decomposition from the **actual coordinate equalities and footprint incidence**, not from an abstract graph imposed from outside. In particular, merely proving a dependency relation well-founded is not enough to obtain an `ℕ)-schedule: a task can have infinitely many predecessors and therefore fail to occur at any finite stage. Any scheduling theorem must state the stronger local-finiteness / finite-rank / enumeration hypothesis it actually needs.

After a sufficiently broad quotient-stage common gauge is obtained, the two comparison `gIso` equations from v3.02–v3.04 remain the next Stage-I assembly problem. Stage-II coherent universality and the final `DO(C,W,J,H)` representation theorem remain distinct later milestones.

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

The pinned environment is recorded in [lean-toolchain](lean-toolchain) and [lake-manifest.json](lake-manifest.json). The focused v3.40 target is:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCollisionSectorPreservationV3_40
```

For PR #1719, exact head

```text
e6f8dc72a5188aa3c5b913d89351711232d2201a
```

was validated by governance run [35715231469](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35715231469). The Strict Lean formal validation job, dependency-manifest verification, governance summary, Lean completion receipt, and exact-head terminal receipt all completed with `success`. That exact head was then merged as theorem commit

```text
243e6e2a990ddb319e84f3722478539641d0a5e3
```

and the post-merge comparison with `main` was identical.

The aggregate formal target can be checked separately:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

The focused v3.40 receipt is **not** a claim that a fresh aggregate `KuuOSFormal` build was run. The effect-free runtime entry point remains:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a mathematical theorem. A CI receipt applies only to its exact head and recorded checkout. Queued/running checks are not success, an old-head success is not a new-head success, and a docs-only gate does not constitute theorem validation.

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

**Current research sentence:** KuuOS has now moved N4 from abstract pairwise compatibility to explicit simultaneous construction on two substantial actual sectors: all unitors plus the entire middle-identity collision sector, together with any prescribed fresh/interior/forward-noninterfering countable associator schedule. The next boundary is a theorem-level decomposition of the remaining actual associator incidence geometry into collision-derived, fresh-schedulable, and residual-obstruction sectors; comparison `gIso` equations and general Stage I follow after the quotient-stage coverage is sufficient.