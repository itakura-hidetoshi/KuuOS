# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, coherence, descent, obstruction, exact presentations, and universal properties.

**Founder and copyright holder:** Hidetoshi Itakura / 板倉英俊. See [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE): public visibility does **not** grant a license to reproduce, adapt, train on, redistribute, or commercialize the materials.

> What remains invariant under justified changes of context and presentation? Which local observations can be transported, compared, and glued, and where do obstructions prevent descent?

## Status / 現在地 — v5.85 (2026-10-08 JST)

**Theorem-bearing canonical main is integrated through v5.85, [PR #2043](https://github.com/itakura-hidetoshi/KuuOS/pull/2043).**

The formal actual-lift classification program has progressed from explicit non-strict pseudofunctors, unit/counit, and invertible triangle contractions (v5.40–v5.63) to **native forward/reverse swallowtail predicates, original pointwise four-cell pastes, global invertible modifications, middle naturality, and generic component transport calculus** (v5.64–v5.85).

Most importantly, the current proved and unproved boundaries are separate:

| Result | Status | Evidence |
| --- | --- | --- |
| Original forward canonical four-cell interchanger at each source object | **Proved / constructed** | [v5.68](formal/KUOS/DependentOriginationForwardSwallowtailComponentInterchangerV5_68.lean) |
| Middle whole-StrongTrans naturality agreement, not merely objectwise equality | **Proved** | [v5.82](formal/KUOS/DependentOriginationForwardMiddleNaturalityPasteV5_82.lean) |
| Native **global invertible** forward interchanger, with equality-transport adapters | **Constructed** | [v5.83](formal/KUOS/DependentOriginationGlobalForwardSwallowtailInterchangerV5_83.lean) |
| Generic equality-transport and vertical-composition formulas on StrongTrans components | **Proved** | [v5.84](formal/KUOS/DependentOriginationForwardTransportComponentsV5_84.lean) |
| Generic five-stage transport formulas and the original four-cell = two-factor pointwise component paste | **Proved** | [v5.85](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean) |
| Full component identification of the **v5.83 global Iso** with the **v5.68 original four-cell interchanger** | **Open — named proposition, not theorem** | [ActualLiftGlobalCanonicalComponentAgreement, v5.85](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean) |
| Original forward and reverse swallowtail equations | **Open — predicates stated, equations not proved** | [v5.65](formal/KUOS/DependentOriginationForwardSwallowtailPredicateV5_65.lean), [v5.66](formal/KUOS/DependentOriginationReverseSwallowtailPredicateV5_66.lean) |

The v5.57 certificate's historical name is retained for compatibility. Neither that name nor the existence of native invertible triangle contractions establishes the missing **swallowtail** laws. KuuOS does **not** claim a newly proved coherent biadjunction, biadjoint biequivalence with swallowtail coherence, or a fully coherent tricategorical adjunction.

## Exact reproducibility / 正本と検証

| Authority or receipt | Exact reference |
| --- | --- |
| Repository / canonical branch | **itakura-hidetoshi/KuuOS / main** |
| Latest theorem-bearing merge | **4b1a117ded213562f37e5b5d3627bbf28410b05c** |
| Integrated theorem PR | [#2043, v5.85, merged](https://github.com/itakura-hidetoshi/KuuOS/pull/2043) |
| Validated exact PR head | **a1d66d8d9ab164527a2b00fb43c43a0018a50eea** |
| Exact-head PR CI | [Run #37773980229 — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37773980229) |
| Strict Lean / governance jobs | **113300216620 / 113301429843 — SUCCESS** |
| MCP Lean / MCP CI completion receipts | **113301429847 / 113301499488 — SUCCESS** |
| Selected target + dependency build | **8712/8712 jobs; return code 0** |
| Lean | **leanprover/lean4:v4.30.0-rc2** ([lean-toolchain](lean-toolchain)) |
| mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** ([lake-manifest.json](lake-manifest.json)) |

This receipt validates the **selected v5.85 Lean target and its dependencies** with strict warning/sorry handling; it does not by itself mean every aggregate target or AI runtime was rerun. A later **docs-only** merge can advance main without advancing this theorem-bearing baseline. Re-observe the exact main SHA before interpreting any new claims.

Formal authority order:

~~~text
fresh exact canonical GitHub commit SHA
  > formal Lean declarations at that exact commit
  > README / ROADMAP
  > matching exact-head CI, governance and completion receipts
  > historical summaries and conversation memory
~~~

The isolated [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is a **Lean 4.31 validation-only** lane: open, draft, unmerged (observed head: 3a09839782ea82661ddbf8e13a0fd08e893079b4). It is not theorem authority; **do not merge, mark ready for review, or auto-merge** it.

## 空・縁起 as a reasoning discipline

空 means **non-reification**, not that nothing exists. An observation is not automatically global truth; a representation is not an intrinsic substance; compatible local views still require a valid transport/gluing argument; an equivalence does not erase the chosen presentation or provenance.

KuuOS's operational route is:

1. Separate observations from inferences.
2. Identify the active context and authority.
3. Retain multiple presentations rather than choosing a single fictitious canonical view.
4. Track relations, history, provenance, and label/world binding.
5. Check compatibility of local information.
6. Evaluate whether descent or gluing is mathematically justified.
7. State exact obstructions instead of silently forcing a factorization.
8. Respect tool, data, and action-authorization boundaries.
9. Take only warranted actions.
10. Re-observe and update after acting.

These are research and operational principles, **not** a claim that an LLM has become infallible, that KuuOS is a trained foundation-model weight replacement, or that an AI is authorized to act without user permission.

## Formal classification and actual lifts

Keep external world and presentation labels explicit. The aligned atlas used by the actual-lift construction is:

~~~lean
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

The source and universal classification layers use the **same** stored data:

~~~text
L = ExactLiftableClassificationObject
    (actual-lift-carrying 1-cells)
E = ExactUniversalClassificationObject

F   : L -> E
G   : E -> L                    (genuinely non-strict)
eta : Id_L => F ; G
eps : G ; F => Id_E

T_F : F => F                    original forward triangle
T_G : G => G                    original reverse triangle
C_F : T_F ~= Id_F               invertible modification
C_G : T_G ~= Id_G               invertible modification
~~~

For Y in E, the quasi-inverse chooses once an equivalence eY : F(GY) ≃ Y and retains the actual-lift formula **(eY.hom ; k) ; eZ.inv** for k : Y -> Z. Its native mapId/mapComp, associators, and unitors are not strictified away.

The earlier obstruction chain still has a one-way implication:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

**The converse is false in general.** There is no assertion of arbitrary raw-morphism liftability, atlas-universe reindexing, or a presentation-independent identification without descent data.

## Integrated formal milestone map

| Milestones | Proven constructions and comparisons |
| --- | --- |
| v4.00–v4.48 | Nonfactorization, Stage-II obstruction, recursive/inverse-limit carriers, orientation and descent |
| v4.49–v5.36 | Exact-universal targets, presentation-sensitive classification, realization, hom equivalences, coherent ambient/local packages |
| v5.37–v5.57 | Actual-lift bicategory; F and G; fixed choices; unit/counit; both actual triangle pastes and contractions |
| v5.58–v5.63 | Native functor-bicategory triangulators, explicitly **incoherent** biadjunction datum, non-strict pre/postcomposition and mapId bridge |
| v5.64–v5.70 | Horizontal pastes; typed forward/reverse swallowtail predicates; unit self-naturality; original four-cell pointwise interchanger; explicit global-modification obstruction |
| v5.71–v5.78 | Postcomposition vertical coherence, unit and counit-whiskered interchangers, their global naturality/reassociation; original forward G.mapComp global factor |
| v5.79–v5.82 | Native endpoint equalities; nontrivial middle naturality obstruction and its resolution using original mapComp/naturality factors |
| v5.83–v5.84 | Native global invertible interchanger and generic StrongTrans component/equality-transport formulas |
| **v5.85** | **Generic five-stage transport calculus and original four-cell = two-factor pointwise component theorem; global-to-canonical comparison still open** |

Direct source endpoints: [v5.64](formal/KUOS/DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.lean), [v5.65](formal/KUOS/DependentOriginationForwardSwallowtailPredicateV5_65.lean), [v5.66](formal/KUOS/DependentOriginationReverseSwallowtailPredicateV5_66.lean), [v5.70](formal/KUOS/DependentOriginationForwardSwallowtailModificationObstructionV5_70.lean), [v5.77](formal/KUOS/DependentOriginationReassociatedSourceCounitInterchangerV5_77.lean), [v5.78](formal/KUOS/DependentOriginationActualLiftForwardMapCompGlobalV5_78.lean), [v5.79](formal/KUOS/DependentOriginationForwardSwallowtailNativeBoundaryV5_79.lean), [v5.82](formal/KUOS/DependentOriginationForwardMiddleNaturalityPasteV5_82.lean), [v5.83](formal/KUOS/DependentOriginationGlobalForwardSwallowtailInterchangerV5_83.lean), [v5.84](formal/KUOS/DependentOriginationForwardTransportComponentsV5_84.lean), [v5.85](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean).

## Why the v5.85 boundary matters

The native global Iso of v5.83 is a five-stage composite:

~~~text
(endpoint eqToIso)^-1
  ; globally whiskered G.mapComp (v5.78)
  ; middle whole-StrongTrans eqToIso (v5.82)
  ; reassociated counit-whiskered three-cell Iso (v5.77)
  ; endpoint eqToIso (v5.79)
~~~

The original v5.68 pointwise interchanger is a **four-cell** composite. v5.85 proves that its pointwise component equals:

~~~text
(global G.mapComp factor).hom.app X
  ; (global reassociated counit factor).hom.app X
~~~

The file also proves generic formulas for the three equality transports and for their five-stage composite, while keeping the exact **ActualLiftGlobalCanonicalComponentAgreement** as an **unproved Prop**. A generic transport theorem is not the same as a specialized global-canonical equality; pointwise comparison must still be connected to the original native global Iso without hiding coherence or choices.

The detailed next obligations and evidence are in [ROADMAP.md](ROADMAP.md).

## Reproduce the selected formal result

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 4b1a117ded213562f37e5b5d3627bbf28410b05c

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true \
     build KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85
~~~

Additional selected targets:

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68 \
  KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82 \
  KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83 \
  KUOS.DependentOriginationForwardTransportComponentsV5_84
~~~

Broader builds and runtime checks are **distinct** validation targets, not consequences of that CI receipt:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Research/runtime boundary and citation

Formal Lean declarations constrain what is mathematically justified. Runtime agents, retrieval pipelines, websites, and AI dialogues must separately manage observations, permissions, provenance, audit evidence, and re-observation; simply having a formal theorem does not mean a runtime uses it.

See [ROADMAP.md](ROADMAP.md) for the full milestone ledger and unresolved higher-coherence work, [GOVERNANCE.md](GOVERNANCE.md) for operating boundaries, [CITATION.cff](CITATION.cff) for citation, and [LICENSE](LICENSE) for usage rights.
