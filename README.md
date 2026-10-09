# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, presentation-sensitive equivalence, higher coherence, descent, exact universal properties and explicit obstructions.

**Founder and copyright holder / 創始者・著作権者:** **Hidetoshi Itakura / 板倉英俊**. See [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE). Public repository access does **not** itself grant permission to reproduce, adapt, train on, redistribute or commercialize this work.

> An observation is not a global truth. Which relations survive a justified change of context or presentation? When can compatible local data descend, and where does an obstruction prevent that descent?

## Status / 現在地 — v5.101 (2026-10-09 JST)

**Theorem-bearing canonical `main` is integrated through v5.101: [PR #2062 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2062).**

**F3 forward swallowtail, F4 reverse swallowtail and F5 KuuOS-defined coherent biadjunction carrier are now proved in Lean/mathlib for the original actual-lift data.** The v5.101 record contains the **same** F, genuinely non-strict G, unit η, counit ε, two native invertible triangulator modifications, and the independently constructed original forward and reverse interchangers. Both fields are proofs of the **original v5.65 and v5.66 swallowtail predicates**, not newly chosen replacement equalities.

**日本語要約：** v5.93 で F3（順方向）、v5.100 で F4（逆方向）を証明し、v5.101 で同一の actual-lift 構造に両者を統合しました。従来の F/G/η/ε・選択された対象同値・非strict な G.mapId/G.mapComp は保持しています。旧版にあった「F4／F5 未証明」という記述は現在には該当しません。

| Milestone | Status | Authoritative Lean artifact |
| --- | --- | --- |
| Base: F/G, η/ε and both original triangle contractions | **Constructed and proved**; original incoherent carrier, not yet a swallowtail statement at v5.59 | [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean), [v5.58](formal/KUOS/DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.lean), [v5.59](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.lean) |
| F1: original global-to-canonical four-cell comparison | **PROVED** | [v5.86](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86.lean) |
| F2: naturality of the original forward four-cell family | **PROVED** | [v5.87](formal/KUOS/DependentOriginationForwardCanonicalNaturalityV5_87.lean) |
| F3: original forward swallowtail (canonical and global) | **PROVED**, `actualLiftForwardSwallowtail` / `actualLiftForwardGlobalSwallowtail` | [v5.93](formal/KUOS/DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean), [PR #2053](https://github.com/itakura-hidetoshi/KuuOS/pull/2053) |
| F4: original counit-centered reverse swallowtail | **PROVED**, `actualLiftReverseSwallowtail` plus pointwise and naturality | [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean), [PR #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) |
| F5: both equations on one unchanged actual-lift datum | **PROVED**, `actualLiftCoherentBiadjunctionDatum` and `actualLiftCoherentBiadjunction_exists` | [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean), [PR #2062](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |

**Formal scope:** `Generic.CoherentBiadjunctionDatum` is the **explicit KuuOS structure defined in v5.101**, consisting of the existing `IncoherentBiadjunctionDatum`, both original interchangers, and proof fields for both typed KuuOS swallowtail laws. This is a formal, witnessed result for the actual-lift construction. It is **not** by itself a formal equivalence with every alternative definition of tricategorical/Gray-categorical biadjunction, an unrestricted higher universal mapping principle, or a guarantee about the behavior of an AI runtime. The historically named v5.57 “coherent biequivalence certificate” remains the earlier triangle-level API; v5.101 supplies the subsequently proved swallowtail layer.

## Exact authority and reproducibility / 正本と検証

This is the **theorem-bearing snapshot before the current documentation-only update**; a docs merge moves `main` without changing the Lean theorem-bearing baseline.

| Item | Exact value or receipt |
| --- | --- |
| Repository / canonical branch | **itakura-hidetoshi/KuuOS / main** |
| Latest verified theorem-bearing merge | **53e8ceaa3d50cb18c1e8278dc64b845f8b648896** — [PR #2062 merged](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |
| Validated v5.101 PR source head | **e01bb1776b7a2139504c27022541e495caebf8f8** |
| Exact-head CI | [GitHub Actions run 37928590324 — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37928590324) |
| Strict Lean formal validation | Job **113813495613** — **8,727/8,727**, success |
| Governance + workflow consolidation | Jobs **113823296377** + **113813495683** — success |
| MCP Lean / MCP CI completion receipts | Jobs **113823296498** / **113823358524** — success |
| Changed Lean file diagnostics | **0 warnings, 0 errors; no `sorryAx`** in printed v5.101 declarations |
| Compiler | **leanprover/lean4:v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** — [lake-manifest.json](lake-manifest.json) |

The strict receipt verifies the **selected v5.101 module with its imported dependency build**, not every aggregate target, every workflow or an interactive KuuOS/AI deployment. `#print axioms` for the final declarations reports conventional Lean axioms (`propext`, `Classical.choice`, `Quot.sound`) and **no `sorryAx`**; no new axiom was inserted to obtain the result.

**Authority order / 権威の優先順位:**

~~~text
fresh exact canonical GitHub main SHA
  > actual Lean definitions, theorem statements, and proofs at that SHA
  > README / ROADMAP
  > matching exact-head CI, governance and MCP receipts
  > historical notes, previous conversations and memory
~~~

**Protected lane:** [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558), Lean 4.31 validation-only, stays **OPEN / DRAFT / not merged** (last observed head: `3a09839782ea82661ddbf8e13a0fd08e893079b4`). It is **not** theorem authority; **never mark ready, auto-merge or merge** this PR.

## Mathematical construction / 数学的構成

The actual-lift construction keeps world and presentation labels explicit and uses the aligned atlas:

~~~lean
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

The same original choices are retained throughout:

~~~text
L = ExactLiftableClassificationObject   (actual-lift-carrying 1-cells)
E = ExactUniversalClassificationObject

F   : L -> E                              (native strict projection)
G   : E -> L                              (genuinely non-strict)
η   : Id_L => F ; G                       (original source unit)
ε   : G ; F => Id_E                       (original target counit)

T_F : F => F                              (original forward triangle)
T_G : G => G                              (original reverse triangle)
C_F : T_F ~= Id_F                         (invertible modification)
C_G : T_G ~= Id_G                         (invertible modification)

Σ_F : original unit-centered forward interchanger
Σ_R : original counit-centered reverse interchanger

F3: Σ_F = forwardTriangulatorPaste
F4: Σ_R = reverseTriangulatorPaste
F5: original data + Σ_F + Σ_R + proofs of both equations
~~~

For each target object `Y`, the actual quasi-inverse uses the **fixed** equivalence `eY : F(GY) ≃ Y`. Its stored action on a target 1-cell `k : Y → Z` includes the genuine transported actual lift:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

The second selected equivalence at `G(Y)` need not coincide with `eY`; the proofs preserve these choices. The non-strict `G.mapId`, `G.mapComp`, associators and unitors are never silently replaced by strict identities.

In particular, **two invertible triangle contractions alone did not give the two swallowtail laws**. Those obligations were discharged separately. In v5.101 the four fields of `Generic.CoherentBiadjunctionDatum` are the original datum, the forward interchanger, the reverse interchanger, and *both* proof fields; see [the exact v5.101 source](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean).

## Formal milestone map / 形式化の履歴

| Milestones | Theorem-bearing achievements |
| --- | --- |
| v4.00–v4.48 | Nonfactorization and Stage-II obstructions, incidence/capacity, finite/inverse-limit carriers, orientation and descent |
| v4.49–v5.36 | Exact-universal targets, localized classification, labels and compatible presentations, realization and unit/counit infrastructure |
| v5.37–v5.57 | Actual-lift bicategory; original F/G; chosen object equivalences; η/ε; original two triangle contractions |
| v5.58–v5.70 | Native functor-bicategory triangulators, incoherent carrier, non-strict comparison cells, both typed swallowtail interfaces |
| v5.71–v5.87 | Global forward interchanger, native middle naturality, original four-cell equality and modification naturality (F1/F2) |
| v5.88–v5.93 | Original forward paste/residual, genuine conjugation coherence, original canonical/global F3 proved |
| v5.94–v5.97 | Original reverse paste and counit-centered four-cell, typed reverse naturality and pointwise reduction |
| v5.98–v5.99 | Generic reverse four-cell and left-triangle cancellation for **two distinct** chosen equivalences |
| **v5.100** | **F4 proved** for original actual lifts; reverse pointwise, modification naturality, global predicate |
| **v5.101** | **F5 proved** as a KuuOS coherent biadjunction record using original F3 and F4 laws |

The exact reverse series is [v5.94](formal/KUOS/DependentOriginationReverseSwallowtailTargetPasteExpansionV5_94.lean) → [v5.95](formal/KUOS/DependentOriginationReverseSwallowtailCounitFourCellV5_95.lean) → [v5.96](formal/KUOS/DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96.lean) → [v5.97](formal/KUOS/DependentOriginationReverseSwallowtailSingleResidualV5_97.lean) → [v5.98](formal/KUOS/DependentOriginationReverseConjugationFourCellV5_98.lean) → [v5.99](formal/KUOS/DependentOriginationReverseConjugationFourCellTriangleV5_99.lean) → [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean) → [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean).

## 空・縁起 as a reasoning discipline

“空” means **non-reification**, not nonexistence. An observation is not automatically a global truth; an equivalence does not erase the chosen presentation or provenance; compatible local views still require transport, descent and gluing hypotheses.

KuuOS operational reasoning distinguishes:

1. Observation from inference and the active context from background assumptions.
2. Multiple presentations, world labels, histories and provenance.
3. Compatibility of local information and conditions for transport/descent.
4. Explicit obstructions, authority boundaries and minimal authorized actions.
5. Re-observation after acting and revision when evidence changes.

This is a **research and engineering discipline**, not proof that an LLM has adopted KuuOS as its underlying trained weights or that it may take actions without authorization.

Earlier obstruction results retain their *one-way* implication:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The converse does **not** hold in general. v5.101 does not establish arbitrary raw-morphism liftability, presentation-independent descent, or unrestricted equivalence across atlases.

## Reproduce the theorem-bearing result

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 53e8ceaa3d50cb18c1e8278dc64b845f8b648896

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
~~~

For the two independently proved swallowtail modules:

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93 \
  KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100
~~~

Broader formal builds and software/runtime checks are separate tests and must receive their own evidence:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Remaining research and runtime boundaries / 次の課題

**Completed within their precise scope:** F1–F5 and the original actual-lift two-swallowtail KuuOS coherent carrier.

**Still separate tasks:** (1) comparison with external tricategorical/Gray-categorical notions under explicitly stated hypotheses; (2) stronger cross-presentation descent and higher universal mapping results; (3) empirical integration of the formal authority and reasoning discipline into GitHub/MCP-backed interactive AI; (4) separately validated end-to-end runtime and website behavior. Do not promote these into Lean theorems without their own types, proofs and exact receipts.

See [ROADMAP.md](ROADMAP.md) for the detailed theorem ledger and next steps, [GOVERNANCE.md](GOVERNANCE.md) for operational boundaries, [CITATION.cff](CITATION.cff) for citation and [LICENSE](LICENSE) for rights.
