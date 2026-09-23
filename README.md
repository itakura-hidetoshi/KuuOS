# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, correction, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

Its central question is:

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, what obstructs that process, and which universal property characterizes the invariant content?

Philosophy, mathematical presentations, formal proofs, and operational systems inform one another without being treated as interchangeable evidence.

## Canonical theorem snapshot — 2026-09-23 JST

| Item | Current reference |
| --- | --- |
| Canonical branch | `main` |
| Canonical theorem frontier | **v3.66 — countermodel quotient representatives collapse to identity 1-cells** |
| Latest theorem-bearing merge | [PR #1748](https://github.com/itakura-hidetoshi/KuuOS/pull/1748) |
| Canonical theorem merge SHA | `8f1a5006dd43afb6d4c9b8ae583ed6f5abab78d9` |
| Validated v3.66 PR head | `383dd616ef9b15c1ecfcac23fd8de4f65b4bc6fa` |
| v3.66 exact-head governance run | [35847500021](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35847500021), completed / success |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

Theorem authority is fixed:

```text
fresh exact canonical GitHub SHA
  > formal Lean artifacts at that SHA
  > README / ROADMAP
  > exact-head CI receipts
  > history / memory
```

A documentation-only merge may advance `main` without advancing the theorem baseline. Re-observe GitHub before continuing formal work.

The separate Lean 4.31 validation-only PR **#1558** remains **open / Draft / unmerged** and outside theorem authority. It must not be merged, marked Ready for review, or auto-merged.

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

The bridge from 空 to 縁起 retains context, relations, admissible transport, higher coherence, descent, obstruction, correction, and authority. KuuOS keeps interpretive connections to Madhyamaka, Yogācāra, Huayan, Tiantai, 陰陽, 五行, 道, 理・気, 礼, and 天人相関 without silently identifying them with one formalism.

The philosophical layer asks about relation, dependence, transformation, and non-reification. The mathematical layer studies those questions through categories, bicategories, pseudofunctors, localization, gauge freedom, holonomy, descent, and universal properties. The operational layer applies bounded observation, planning, action, and renewed verification. These are related layers, not a hierarchy in which one invalidates the others.

## Current mathematical result

The canonical v3.53–v3.65 sequence has substantially sharpened the quotient-coherence truth test.

The key conclusion at v3.65 is a **same-gauge separation theorem** for the concrete v2.69 octahedral `C2` model:

```text
there exists Q such that

  Q corrects every left/right unitor

but

  Q does not correct every associator
  and therefore does not correct every quotient route.
```

Equivalently, for this concrete model,

```text
all unitors corrected at Q
  !=>
all associators corrected at the same Q.
```

This is a genuine formal separation, but it is deliberately **not** a global uncorrectability theorem. It does not show that every gauge fails, nor that a different gauge cannot correct all quotient routes.

The distinction is now explicit:

```text
one bad fixed gauge exists
  !=
no fully coherent gauge exists.
```

That remaining existential question is the current frontier.

## Canonical progression v3.53–v3.65

| Layer | Integrated result |
| --- | --- |
| [v3.53](formal/KUOS/DependentOriginationFreshBoundaryRightIdentityReductionV3_53.lean) | Reduces a fresh-boundary task to right-identity geometry or a composite-identity sector. |
| [v3.54](formal/KUOS/DependentOriginationCompositeIdentityInversePairReductionV3_54.lean) | Under the established cancellation hypotheses, a composite-identity task becomes a two-sided inverse-pair task. |
| [v3.55](formal/KUOS/DependentOriginationInversePairBoundaryObstructionV3_55.lean) | Defines the exact inverse-pair fresh-boundary leading obstruction and proves its equivalence with failure of correction on that task. |
| [v3.56](formal/KUOS/DependentOriginationInversePairRepresentativeEquivalenceV3_56.lean) | Shows the quotient representatives of an inverse pair are essentially surjective and faithful, hence representative semantics are not the residual defect. |
| [v3.57](formal/KUOS/DependentOriginationSourceComplementsGroupoidV3_57.lean) | Global source-complement hypotheses force the localization to be a groupoid and all quotient representative maps to be equivalences. |
| [v3.58](formal/KUOS/DependentOriginationGroupoidHolonomySeparationV3_58.lean) | Shows that groupoid localization + representative equivalences can coexist with nontrivial generated holonomy in the v2.69 model. |
| [v3.59](formal/KUOS/DependentOriginationInversePairSuffixPerturbationV3_59.lean) | Isolates a suffix coordinate whose perturbation can preserve the entire unitor boundary while changing the associator equation. |
| [v3.60](formal/KUOS/DependentOriginationNontrivialSuffixObstructionV3_60.lean) | From an isolated inverse-pair suffix, a nontrivial exact gauge fiber, a faithful representative, and one common-unitor gauge, constructs a fixed gauge carrying the exact v3.55 obstruction. |
| [v3.61](formal/KUOS/DependentOriginationCounterGaugeFiberNontrivialV3_61.lean) | Proves the concrete `C2` composition gauge fiber is nontrivial at every composition coordinate by a central `zeta` automorphism. |
| [v3.62](formal/KUOS/DependentOriginationInversePairIncidenceV3_62.lean) | Reduces the inverse-pair fresh-boundary/incidence bookkeeping to simple object separation plus inverse equations. |
| [v3.63](formal/KUOS/DependentOriginationOctahedralInversePairV3_63.lean) | Instantiates that geometry in the actual v2.69 octahedral localization and supplies the exact nontrivial dependent gauge fiber. |
| [v3.64](formal/KUOS/DependentOriginationUniversalUnitorGaugeV3_64.lean) | Constructs a common gauge correcting **all unitors** without assuming one, then derives a concrete fixed-gauge inverse-pair fresh-boundary obstruction. |
| [v3.65](formal/KUOS/DependentOriginationFixedGaugeUnitorAssociatorSeparationV3_65.lean) | Packages the concrete same-gauge separation: all unitors can be corrected while at least one associator and the total route family remain uncorrected at that same gauge. |

The progression should be read as a truth test, not as a monotone march toward a predetermined negative answer. Each layer narrows what the actual remaining obstruction can be.

## Canonical v3.66 — identity quotient representatives

PR [#1748](https://github.com/itakura-hidetoshi/KuuOS/pull/1748) was validated GREEN at exact head

```text
383dd616ef9b15c1ecfcac23fd8de4f65b4bc6fa
```

with Strict Lean and exact-head terminal receipts both successful in run [35847500021](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35847500021).

It was merged as canonical theorem commit `8f1a5006dd43afb6d4c9b8ae583ed6f5abab78d9`.

v3.66 proves, in the same concrete `C2` countermodel, that every free localization word and therefore every selected quotient representative 1-cell is literally equal to the identity `Cat` 1-cell:

```text
generated relation-loop holonomy is nontrivial

while

every quotient representative 1-cell = identity.
```

This is stronger than the earlier v3.58 statement that every representative is merely an equivalence.

The consequence is conceptually important: any remaining failure of a fully corrected quotient gauge cannot be blamed on the 1-cell assignment. The unresolved question is now concentrated in the simultaneous choice of the **2-cell comparison data** `mapId` / `mapComp` and their associator/unitor coherence equations.

## Exact next frontier — v3.67

The quotient-stage existence problem is already represented in the repository by equivalent formulations:

```text
ThreeQuotientRoutesJointlyCorrectable W R D

      <=>

exists one quotient gauge Q
that corrects every ThreeQuotientRouteState

      <=>

(commonQuotientRouteCorrectionLocus W R D).Nonempty

      <=>

HasCoherentQuotientTransportData W R D.
```

For the concrete v2.69 `C2` model, the next theorem unit must determine which side is true.

After v3.66 the preferred truth-test is:

```text
all quotient representatives are identity 1-cells
        |
        v
try to construct explicit coherent mapId/mapComp 2-isomorphisms
        |
        +--> success:
        |      fully corrected quotient gauge exists;
        |      v3.65 is genuinely gauge-specific
        |
        `--> failure with theorem:
               isolate a gauge-independent 2-cell obstruction
               surviving every gauge choice.
```

Nontrivial generated holonomy alone is **not** enough to conclude failure. That non-implication is retained as a hard rule.

## Canonical formal spine

| Layers | Established role |
| --- | --- |
| v2.0–v2.10 | Ordinary localization, `W` + `J` sectors, stack descent, and the higher-localization factorization interface. |
| v2.11–v2.54 | Weak/coherent distinctions, modification and correction triangles, E/R/A obstruction normal form, and structural sufficient routes. |
| v2.55–v2.68 | Pointwise `W`-adjoint equivalences, free-path evaluation, quotient-equal path isomorphisms, exact quotient/comparison coherence packages, generated 2-cells, and holonomy. |
| v2.69–v2.95 | Octahedral `C2` truth test; nontrivial generated holonomy, correctability, authority, and constructive/classical boundaries. |
| v2.96–v3.14 | Five gauge equations split into three quotient equations and two comparison equations; correction loci and exact dependent gauge coordinates. |
| v3.15–v3.34 | Local-family gluing, actual route-equation rigidity, mixed-triangle residuals, path/representative transport, split-arrow and source-composite cancellation. |
| v3.35–v3.52 | Common unitor correlation, fresh completion, scheduling/stabilization, collision geometry, semantic recovery, and global cancellation from source complements. |
| v3.53–v3.58 | Fresh-boundary reduction to inverse-pair geometry; representative equivalence/groupoid closure; separation from generated holonomy. |
| v3.59–v3.63 | Exact suffix perturbation, nontrivial dependent gauge fibers, incidence reduction, and concrete octahedral inverse-pair instantiation. |
| v3.64–v3.65 | Universal common-unitor gauge and concrete fixed-gauge separation between unitor correction and associator/total-route correction. |
| v3.66 | In the concrete C2 model, every free-path evaluation and selected quotient representative 1-cell is literally identity, localizing the remaining problem to 2-cell coherence. |

## Stage-I boundary after quotient coherence

Even a positive answer to the current quotient-gauge problem would not finish general Stage I.

The v3.02–v3.04 split remains:

```text
five-face generated correction
  =
three quotient pseudofunctor coherence equations
  +
two comparison gIso equations.
```

Therefore:

```text
fully coherent quotient transport
  !=
complete higher-localization factorization.
```

Once the quotient carrier is constructed or characterized, the two comparison equations must still be solved or isolated as explicit residual obstructions.

## Dependent Origination Universality Program

The long-range target remains an explicitly constructed carrier, schematically

```text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X),
```

with the correct higher variance, factorization, essential uniqueness, naturality, descent compatibility, and presentation invariance.

**The final universal object and representation theorem are not yet proved.**

A localization, quotient, stackification, semantic reduction, or one successful factorization is not promoted to `DO(C,W,J,H)` without the required mapping property.

## AI and operational interpretation

The same distinctions guide bounded systems engineering:

```text
model / prompt / index migration -> presentation transport
partial memory integration      -> compatibility and descent
contradictory evidence           -> explicit obstruction
multi-agent coordination        -> higher coherence
different remediation powers    -> authority-relative correction
```

These are engineering interpretations, not deployment guarantees derived from the Lean theorems.

The operational route remains:

```text
observe -> represent -> retrieve -> plan -> decide -> act -> re-observe -> verify
```

Retrieval, entailment, execution, theorem authority, and WORLD-state authority remain separate.

## Reproduction and verification

Canonical v3.65 target:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationFixedGaugeUnitorAssociatorSeparationV3_65
```

Canonical v3.66 target:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationCounterRepresentativeIdentityV3_66
```

For the validated v3.66 PR head

```text
383dd616ef9b15c1ecfcac23fd8de4f65b4bc6fa
```

was validated by run [35847500021](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/35847500021), including Strict Lean formal validation, dependency-manifest verification, governance summary, Lean completion receipt, and exact-head terminal receipt, then merged as `8f1a5006dd43afb6d4c9b8ae583ed6f5abab78d9`.

The aggregate formal target remains a separate check:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Runtime validation remains separate:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

A runtime result is not a theorem. A docs-only successful gate is not theorem validation. A CI receipt applies only to its recorded exact head.

## Proof-engineering lessons retained

Recent formalization has reinforced several rules:

- **Import is not open.** A transitive import does not put short names into scope; open the actual defining namespace or qualify the name.
- **Keep `autoImplicit false`.** Unknown identifiers should fail closed rather than silently become new implicit variables.
- **Do not overuse `simpa using` on already-simpable isomorphism laws.** It can simplify the source proposition farther than the target; use direct `exact` or controlled `simp only`.
- **Dependent equality needs the intended extensionality API.** For functors, `Functor.hext` expects object equality plus heterogeneous map equality; use equality proof `.heq` rather than invented conversion names.
- **Make hidden carriers explicit when typeclass search stalls.** v3.66 uses the fact that `SingleObj M` is `Unit` instead of asking Lean to infer a hidden `Subsingleton`.
- **Prefer bundled isomorphisms over separately unfolded hom/inv terms.** This prevents simplification from erasing the structure needed by inverse laws.
- **Use typed equality transport rather than pretending dependent coordinates are definitionally equal.**
- **Track exact PR heads, not merge refs or stale runs.** Merge only after current-head Strict Lean and terminal receipts are successful.
- **A theorem receipt validates that exact head only.** After every code change, old receipts are stale.

## No-go implications

Do not promote the following without a theorem:

```text
import -> namespace opened
local Nonempty Iso -> coherent global choice
Classical.choice -> pentagon/unit laws
weak admissibility -> generated holonomy triviality
nontrivial generated holonomy -> factorization impossible
representative equivalence -> coherent quotient transport
groupoid localization -> trivial holonomy

one bad gauge -> every gauge fails
fixed-gauge associator obstruction -> global uncorrectability
all unitors corrected at Q -> all associators corrected at Q
v3.65 separation -> common correction locus empty

v3.66 identity representatives -> coherence equations automatic
identity 1-cell assignment -> unique or trivial 2-cell coherence
fully coherent quotient transport -> both comparison gIso equations
Stage-I factorization -> Stage-II universality
docs-only CI -> theorem validation
runtime success -> theorem authority
```

## Current research sentence

**KuuOS has reduced the concrete octahedral quotient-coherence truth test from broad generated-holonomy nontriviality to an exact same-gauge 2-cell coherence question: canonical v3.65 proves that a gauge can correct all unitors yet fail an associator, while canonical v3.66 shows every selected quotient representative 1-cell is nevertheless literally identity. The next decisive step is to construct a fully coherent quotient gauge explicitly or prove a gauge-independent 2-cell obstruction that survives every gauge choice.**
