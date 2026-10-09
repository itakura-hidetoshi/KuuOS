# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, presentation-sensitive equivalence, higher coherence, descent, exact universal properties and explicit obstructions.

**Founder and copyright holder / 創始者・著作権者:** **Hidetoshi Itakura / 板倉英俊**. See [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE). Public repository access does **not** itself grant permission to reproduce, adapt, train on, redistribute or commercialize this work.

> An observation is not a global truth. Which relations survive a justified change of context or presentation? When can compatible local data descend, and where does an obstruction prevent that descent?

## Status / 現在地 — v5.106 (2026-10-10 JST)

**Latest confirmed theorem-bearing canonical `main`: [PR #2069 / v5.106 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2069), commit `1aac4e4fef8d3c7f500095cc7b047a7e8baf6782`. F1–F10 are CLOSED within their precisely stated KuuOS/actual-lift specifications.** The v5.101 carrier proves the *original* forward and reverse swallowtail equations on one unchanged F/G/η/ε datum; v5.102–v5.106 connect its chosen objectwise equivalences and naturality squares to native mathlib bicategorical adjunctions and mates, preserving the genuinely non-strict `G.mapComp`.

**日本語要約：** F1–F5（v5.101まで）では元の forward/reverse swallowtail を同じデータ上で証明しました。F6（v5.102）は選択済み同値を mathlib `Bicategory.Adjunction`／`Adj.Hom` に接続、F7（v5.103）は保存データから元の同値を復元、F8（v5.104）は元の η/ε 自然性の mate と逆変換・2-cell 自然性を証明、F9（v5.105）は mate の垂直／水平合成と元の compositor 補正を整合させ、F10（v5.106）は **target 側の `R_E.mapComp` 補正を右 mate の貼り合わせへ明示的に移送**しました。F/G/η/ε・対象ごとの同値・triangulator は再選択していません。

| Milestone | Status | Authoritative Lean artifact |
| --- | --- | --- |
| Base: original F/G, η/ε and two triangle contractions | **Constructed / proved** (historically before swallowtail closure) | [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean), [v5.58](formal/KUOS/DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.lean), [v5.59](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.lean) |
| F1: original global/canonical forward interchanger comparison | **PROVED** | [v5.86](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86.lean) |
| F2: naturality of the original forward four-cell family | **PROVED** | [v5.87](formal/KUOS/DependentOriginationForwardCanonicalNaturalityV5_87.lean) |
| F3: original forward swallowtail (canonical/global) | **PROVED** — `actualLiftForwardSwallowtail` / `actualLiftForwardGlobalSwallowtail` | [v5.93](formal/KUOS/DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean), [PR #2053](https://github.com/itakura-hidetoshi/KuuOS/pull/2053) |
| F4: original counit-centered reverse swallowtail | **PROVED** — `actualLiftReverseSwallowtail` | [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean), [PR #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) |
| F5: both original swallowtails on one actual-lift coherent carrier | **PROVED** — `actualLiftCoherentBiadjunctionDatum` | [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean), [PR #2062](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |
| F6: chosen equivalences as native mathlib adjuncts | **PROVED** — `Generic.nativeAdjunctionOfEquivalence`, source/target `actualLift*NativeAdjHom` | [v5.102](formal/KUOS/DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.lean), [PR #2065](https://github.com/itakura-hidetoshi/KuuOS/pull/2065) |
| F7: lossless reconstruction of the original equivalences | **PROVED** — `Generic.originalEquivalenceRoundtrip_eq` and recovered source/target equivalences | [v5.103](formal/KUOS/DependentOriginationNativeAdjunctionLosslessReturnV5_103.lean), [PR #2066](https://github.com/itakura-hidetoshi/KuuOS/pull/2066) |
| F8: original unit/counit naturality squares as right mates | **PROVED** — unmate/recovered/2-cell naturality | [v5.104](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesV5_104.lean), [PR #2067](https://github.com/itakura-hidetoshi/KuuOS/pull/2067) |
| F9: vertical/horizontal mate composition and source `mapComp` agreement | **PROVED** — `actualLiftSourceUnitMateComp_native`; target compositor retained on the left | [v5.105](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105.lean), [PR #2068](https://github.com/itakura-hidetoshi/KuuOS/pull/2068) |
| F10: explicit target compositor-corrected RIGHT mate pasting | **PROVED** — `actualLiftTargetCounitMateComp_correctedRight` | [v5.106](formal/KUOS/DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106.lean), [PR #2069](https://github.com/itakura-hidetoshi/KuuOS/pull/2069) |

**Formal scope:** v5.101 `Generic.CoherentBiadjunctionDatum` is the *explicit KuuOS coherent carrier*: original base, original two interchangers and proofs of both typed swallowtail laws. F6–F10 add objectwise mathlib adjunction/mate interfaces and precisely compositor-corrected original naturality, **not** an unconditional equivalence with arbitrary tricategorical/Gray-categorical definitions, a global pseudofunctor-level `Bicategory.Adjunction`, arbitrary invertibility of mates, cross-presentation descent, or runtime/AI correctness. The earlier v5.57 “coherent biequivalence certificate” is a historical triangle-level API; v5.101 supplied the independently proved swallowtails.

## Exact authority and reproducibility / 正本と検証

The following is the **latest verified theorem-bearing snapshot before this documentation-only update**. A docs-only merge moves live `main` but does not replace the v5.106 Lean theorem-bearing baseline. Freshly re-observe the canonical SHA for subsequent work.

| Item | Exact value / evidence |
| --- | --- |
| Repository / canonical branch | **itakura-hidetoshi/KuuOS / main** |
| Latest theorem-bearing merge | **`1aac4e4fef8d3c7f500095cc7b047a7e8baf6782`** — [PR #2069 merged](https://github.com/itakura-hidetoshi/KuuOS/pull/2069) |
| Validated v5.106 PR source HEAD | **`210814f700252163e4ae13794cae595625ff4ed4`** |
| Exact-head GitHub Actions | [Run 37999962448 — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37999962448) |
| Strict Lean validation | Job **114055427705 — SUCCESS**, **8732/8732** selected module/dependency build |
| Governance / audit summary | Job **114055925178 — SUCCESS** |
| MCP Lean / MCP CI completion receipts | Jobs **114055925139 / 114055968137 — SUCCESS** |
| Changed v5.106 Lean file diagnostics | **0 warnings / 0 errors**; 5 `#print axioms` declarations with **no `sorryAx`** |
| Compiler | **leanprover/lean4:v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** — [lake-manifest.json](lake-manifest.json) |

The exact-head Strict Lean check validates the **selected v5.106 module and its transitive imported dependencies**, not every repository target or workflow and not a deployed interactive AI system. The selected v5.106 declarations use conventional Lean axioms (`propext`, `Classical.choice`, `Quot.sound`) and **no `sorryAx`**, `sorry`, `admit` or newly introduced axiom. Pre-existing warnings from imported files must not be conflated with the **zero warnings/errors in the changed module**.

**Authority order / 権威の優先順位:**

~~~text
fresh exact canonical GitHub main SHA
  > actual Lean declarations and proofs at that SHA
  > README / ROADMAP
  > matching exact-head CI, governance and MCP completion receipts
  > historical notes, previous conversations and memory
~~~

**Protected validation-only lane:** [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558), Lean 4.31 validation, remains **OPEN / DRAFT / not merged** (observed head `3a09839782ea82661ddbf8e13a0fd08e893079b4`). It is not theorem authority: **never mark ready, auto-merge or merge**.

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

In particular, **two invertible triangle contractions alone did not give the two swallowtail laws**. Those obligations were discharged separately. In v5.101 the five fields of `Generic.CoherentBiadjunctionDatum` are the original datum, the forward interchanger, the reverse interchanger, and *both* proof fields; see [the exact v5.101 source](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean).

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
| **v5.102 / v5.103** | **F6/F7 CLOSED:** chosen equivalences ↔ native mathlib adjunctions, lossless reconstruction of original stored data |
| **v5.104 / v5.105** | **F8/F9 CLOSED:** source/target native right mates; unmate, 2-cell naturality, vertical/horizontal composition and source compositor correction |
| **v5.106** | **F10 CLOSED:** typed target `R_E.mapComp`-corrected right-mate vertical paste, via `whisker_exchange` and `mateEquiv_vcomp` |

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

The converse does **not** hold in general. Neither v5.101 nor the additional native mathlib mate interfaces through v5.106 establish arbitrary raw-morphism liftability, presentation-independent descent, or unrestricted equivalence across atlases.

## Reproduce the theorem-bearing result

Checkout the **v5.106 theorem-bearing SHA** (not the later docs-only commit) and use the pinned Lean/mathlib environment:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 1aac4e4fef8d3c7f500095cc7b047a7e8baf6782

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106
~~~

This selected target imports v5.105 and earlier dependencies. For the independently established swallowtail endpoints, also check:

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93 \
  KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
~~~

Broader all-formal and runtime checks require **separate** independent validation; their success does not follow from the selected F10 receipt:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Remaining research and runtime boundaries / 次の課題

**Completed within the stated scope:** F1–F10, including the original actual-lift forward/reverse swallowtails, the KuuOS coherent carrier, chosen objectwise mathlib adjunctions, exact mate/unmate recovery, and compositor-corrected source/target mate pasting.

**Not yet established:** an F11 identity/`mapId`-corrected mate coherence theorem (proposed next formal target); unrestricted external tricategorical/Gray-categorical equivalence; cross-presentation descent and higher universal mapping properties without additional hypotheses; and empirical correctness of GitHub/MCP-backed AI, retrieval, runtime or website behavior. These require independently typed statements, actual proofs and exact-head evidence.

See [ROADMAP.md](ROADMAP.md) for the detailed theorem ledger and next steps, [GOVERNANCE.md](GOVERNANCE.md) for operational boundaries, [CITATION.cff](CITATION.cff) for citation and [LICENSE](LICENSE) for rights.
