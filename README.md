# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, presentation-sensitive equivalence, higher coherence, descent, exact universal properties and explicit obstructions.

**Founder and copyright holder / 創始者・著作権者:** **Hidetoshi Itakura / 板倉英俊**. See [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE). Public repository access does **not** itself grant permission to reproduce, adapt, train on, redistribute or commercialize this work.

> An observation is not a global truth. Which relations survive a justified change of context or presentation? When can compatible local data descend, and where does an obstruction prevent that descent?


## Status / 現在地 — v5.153 · 2026-10-11 JST

**Latest verified theorem-bearing canonical `main`:** [PR #2129 / v5.153 F56-E MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2129), **`482e325d35b8186d43b0d503ebaceb7e3a498036`**. GitHub MCP confirmed the PR merge SHA and exact theorem-bearing `main` HEAD coincide. **F1–F56-A–E are closed only within their original precisely typed KuuOS theorem scopes**; no unrestricted external tricategorical/Gray-categorical 3-cell realization, presentation-independent descent, infinite limit or AI runtime correctness is implied.

**日本語要約：** F1–F5は元のF/G・source η・target εと正逆swallowtail、F6–F39はnative adjunction/mate、元のF19 chosen-mate圏と独立のF28比較核商圏、F40–F46は操作順序を保持するType-valued F19/F28履歴と独立軸隣接交換によるF44商、そのF46分類を構築しました。F47–F53は本来のF45段階列、依存する二軸のNat深さ輸送、任意有限の二分木括弧付け、F44商上の5頂点pentagonを証明しました。F54は任意の左右文脈の局所回転と有限`RotationChain`を構成。**F55／v5.152では、異なる長さを持つ3回転・2回転pentagon経路と独立回転squareを具体的に構築し、`DepthRotationRoute.PresentedCell`を自由なType-valued高次関係の型として導入しました。すべての経路における2軸の深さ輸送後のF44商・完全履歴保存、および元のchosen right mateと実際のsource η／target εへの整合性をLeanで証明しました。** 異なる生の経路は同一視せず、外部tricategoryの3-cell実現は未証明です。 **F56／v5.153では、自由な`PresentedCell`を独立に指定した高次対象へ解釈する条件付き`HigherCellTarget`を構築し、貼り合わせ・左右文脈の解釈整合性と3対2の回転数を一律に保存できない障害を証明しました。元のF44交換商と二軸の全履歴に基づく実際の`F44ObservedCell`モデルを構成し、各固定境界で`PUnit`と同値であること、高次証拠を単射的に復元できないこと、さらにこの観測のみを経由する任意の解釈先で非忠実となる条件付き障害をLeanで証明しました。**

| Mathematical result | Proved scope / exact representative |
| --- | --- |
| Original coherent actual-lift carrier | **v5.101 / F5**, unchanged original F/G, η/ε and two separately proved swallowtails: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean), [PR #2062](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |
| Native objectwise adjunction and mate interfaces | **v5.102–v5.115 / F6–F18**; chosen equivalences, original source/target lax mates, `mapId`/`mapComp` and modification naturality: [PR #2080](https://github.com/itakura-hidetoshi/KuuOS/pull/2080) |
| Original two-sided mate category and quotient constructions | **v5.116–v5.136 / F19–F39**; genuine F28 compression-kernel quotient, two-sided nonstrict mate/hexagon/whiskering: [F19](formal/KUOS/DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.lean), [F28](formal/KUOS/DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.lean), [PR #2102](https://github.com/itakura-hidetoshi/KuuOS/pull/2102) |
| Proof-relevant original F19/F28 independent-axis refinement | **v5.137–v5.142 / F40–F45**; genuine original `Blocks` / `OneStep` / `OrderedInterleaving` and F44 generated exchange quotient, F45 native `AxisTrace`: [F44](formal/KUOS/DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.lean), [F45](formal/KUOS/DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142.lean) |
| Complete generated-exchange normal forms | **v5.143 / F46**: `ExchangeClass ≃ (AxisTrace F19 × AxisTrace F28)` at fixed endpoints/depths. **Only independent-axis adjacent swaps are quotiented**; distinct same-axis histories remain distinct: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionExchangeAxisPairEquivalenceV5_143.lean), [PR #2109](https://github.com/itakura-hidetoshi/KuuOS/pull/2109) |
| Actual original F45 routes, η/ε and finite composition | **v5.144–v5.148 / F47–F51**; original `Eq.mp`/`Nat.zero_add` casts, real chosen mate and source/target comparisons, quotient associativity/units and arbitrary finite stage chains: [F48](formal/KUOS/DependentOriginationCoherentBiadjunctionF45TransportedHistoryReconciliationV5_145.lean), [F51](formal/KUOS/DependentOriginationCoherentBiadjunctionArbitraryFiniteOriginalF45StagesV5_148.lean) |
| Arbitrary finite bracketing and fourfold pentagon | **v5.149–v5.150 / F52–F53**; genuine full binary ORIGINAL F45 paths; five vertices/five associator edges; long **3-edge** and short **2-edge** routes agree **in the F44 exchange quotient with both depth casts**, including original chosen mate and actual η/ε endpoint specializations: [F52](formal/KUOS/DependentOriginationCoherentBiadjunctionArbitraryBracketTreeV5_149.lean), [F53](formal/KUOS/DependentOriginationCoherentBiadjunctionFourfoldPentagonV5_150.lean), [PR #2116](https://github.com/itakura-hidetoshi/KuuOS/pull/2116) |
| Finite local associativity rotations in arbitrary F45 tree contexts | **v5.151 / F54**: actual `Type`-valued `LocalRotation` under arbitrary left/right contexts; `RotationEdge` with forward/backward witnesses; finite `RotationChain` with length, composition, reverse and contextual whiskering; preservation of the **original F44 quotient and both complete typed F19/F28 histories**, transported via original chosen right mate and actual source η / target ε: [local rotations](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45LocalRotationV5_151.lean), [finite chains](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45FiniteRotationChainsV5_151.lean), [η/ε](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftRotationV5_151.lean), [PR #2118](https://github.com/itakura-hidetoshi/KuuOS/pull/2118) |
| Concrete depth-aware rotation-path pentagon, square and presented higher cells | **v5.152 / F55-A–B**: the real F54 Type-valued edges produce a **3-step** long and **2-step** short pentagon with distinct raw witnesses; independently contextual rotations give a genuine square; `DepthRotationRoute.PresentedCell` is an explicitly **freely presented Type-valued 2D relation**, not an externally realized Gray/tricategory 3-cell. [pentagon routes](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45RotationDepthRoutesV5_152.lean), [square/cells](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean), [PR #2120](https://github.com/itakura-hidetoshi/KuuOS/pull/2120), [PR #2121](https://github.com/itakura-hidetoshi/KuuOS/pull/2121) |
| All-route quotient/history invariance and original mate/η/ε | **v5.152 / F55-C1–C3**: actual `DepthRotationRoute.depthEq`, `toExchangeClass_eq` and `axisHistories_eq` for every route constructor and two independent Nat casts; original F19 chosen right-mate and genuine F28 quotient functor compatibility, actual source η and target ε specializations. [invariants](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationInvariantsV5_152.lean), [chosen mate](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationMatesV5_152.lean), [actual η/ε](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftDepthRotationV5_152.lean), [PR #2122](https://github.com/itakura-hidetoshi/KuuOS/pull/2122), [PR #2123](https://github.com/itakura-hidetoshi/KuuOS/pull/2123) |
| Conditional interpretation and genuine F44 observational higher-cell model | **v5.153 / F56-A–C:** original `HigherCellTarget` with genuinely independent pentagon/square/pasting/whisker witnesses and a typed interpreter; `3 ≠ 2` count-preservation obstruction; original four-certificate `F44ObservedCell` target constructed using the F55 F44 exchange quotient and both entire F19/F28 histories. This is an **observational truncation**, not an external Gray/tricategory 3-cell realization. [conditional target](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ConditionalHigherCellTargetV5_153.lean), [pasting/no-go](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45HigherCellPastingObstructionV5_153.lean), [concrete observation](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ConcreteF44CellTargetV5_153.lean), [PR #2125](https://github.com/itakura-hidetoshi/KuuOS/pull/2125), [#2126](https://github.com/itakura-hidetoshi/KuuOS/pull/2126), [#2127](https://github.com/itakura-hidetoshi/KuuOS/pull/2127) |
| Precise higher observational information-loss and factorization no-go | **v5.153 / F56-D–E:** all fixed-boundary observed certificate structures are subsingletons and equivalent to `PUnit`; distinct raw F55 higher cells have identical observed interpretation. **Every map factoring solely through this F44/full-history observation is constant on fixed parallel paths and cannot faithfully reconstruct the raw Type-valued higher syntax.** [subsingleton/noninjectivity](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean), [conditional factorization obstruction](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellFactorizationNoGoV5_153.lean), [PR #2128](https://github.com/itakura-hidetoshi/KuuOS/pull/2128), [PR #2129](https://github.com/itakura-hidetoshi/KuuOS/pull/2129) |

**Scope boundary / 数学的境界：** F56-A's higher-cell interpreter is conditional on independently supplied target cells; F56-C's actual F44/F19/F28 model is only an observational truncation, and F56-D/E prove a **conditional nonfaithfulness obstruction for any interpretation factoring through it**. The free F55 Type-valued cells are NOT identified with externally specified tricategorical/Gray 3-cells, and the no-go does NOT exclude richer targets or legitimate independent coherence quotients. Original same-axis histories, original η/ε, separate F19/F28 categories and potentially noninvertible G.toOplax directions remain intact; no unrestricted global biequivalence or infinite convergence follows.

## Exact authority and reproducibility / 正本と検証

| Item | Exact verified value |
| --- | --- |
| Repository / canonical branch | **[itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) / `main`** |
| **Latest theorem-bearing canonical `main` and F56 PR merge** | **`482e325d35b8186d43b0d503ebaceb7e3a498036`**, [PR #2129 CLOSED/MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2129) |
| Latest validated F56-E PR source HEAD | **`43e455606731bcba225cd74240d889da5abe10c9`** |
| Exact-head PR workflow | [Run **38107828541** — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38107828541) |
| Strict Lean validation | Job **114377017783 — SUCCESS**, **8862/8862** selected dependency/module build |
| Governance / audit | Job **114377307113 — SUCCESS** |
| MCP Lean / MCP CI completion receipts | Jobs **114377307093 / 114377329449 — SUCCESS** |
| Changed F56-E Lean diagnostics / axioms | **1 new Lean file**, **0 warnings / 0 errors**, **4/4 `#print axioms`**, no `sorryAx`/`sorry`/`admit`/new axiom |
| Pinned compiler | **Lean v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| Pinned mathlib | **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`** — [lake-manifest.json](lake-manifest.json) |

The exact-head receipt covers the selected F56-E changed Lean module **and imported dependency closure**, not every repository workflow, runtime, interactive website or LLM model. After a later documentation-only merge, `main` changes but the mathematical theorem-bearing baseline remains the exact **F56-E merge `482e325d…`** until an independently verified theorem-bearing merge.

**Authority order:** fresh exact GitHub `main` SHA → actual Lean declarations and proofs at that SHA → README/ROADMAP → matching exact-head CI/governance/MCP receipts → historical notes.

**Protected validation-only lane:** [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) (Lean 4.31 experiment) was freshly checked **OPEN / DRAFT / NOT MERGED**. It is outside theorem authority; **do not mark ready, auto-merge or merge**.


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

| Version(s) | Verified mathematical progress |
| --- | --- |
| v4.00–v4.48 | Nonfactorization and Stage-II obstructions; incidence/capacity; finite and inverse-limit carriers; orientation/descent, under stated hypotheses |
| v4.49–v5.36 | Exact-universal targets, localized classification, presentation/label-aware realization, source/target unit-counit infrastructure |
| v5.37–v5.63 | Original actual-lift bicategory; F/G, η/ε, objectwise chosen equivalences, native triangle modifications and nonstrict comparisons |
| v5.64–v5.101 | Original forward/reverse swallowtail laws and **F5 coherent biadjunction carrier**: [v5.93](formal/KUOS/DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean), [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean), [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) |
| v5.102–v5.115 | **F6–F18:** native adjunctions/mates and unmate recovery, identity/composition corrections, original arbitrary modifications |
| v5.116–v5.124 | **F19–F27:** original chosen-mate presentation categories, finite comparison paths, two-sided nonstrict naturality and compression |
| v5.125–v5.136 | **F28–F39:** genuine compression-kernel quotient categories, quotient horizontal functors, associator/unitor/hexagon/pentagon-triangle coherence, finite two-axis mates |
| v5.137–v5.141 | **F40–F44:** original finite subdivision, primitive refinement traces, two-axis interleavings, genuine generated quotient by independent adjacent swaps |
| v5.142–v5.143 | **F45–F46:** proof-relevant independent histories and **`ExchangeClass ≃ (F19 history × F28 history)`**, exact exchange-equivalence iff native histories agree |
| v5.144–v5.146 | **F47–F49:** actual F19-first/F28-first normal paths, original F45 `Eq.mp` depth transport, original chosen mates and six source η/target ε paths |
| v5.147–v5.148 | **F50–F51:** true two-stage sequential composition, associativity/units with double Nat casts, arbitrary **finite** typed ORIGINAL F45 stage chain |
| v5.149 | **F52:** any finite full binary bracketing, compatibility with the original left-associated stage sequence, chosen mate and actual η/ε specialization |
| **v5.150** | **F53 / [PR #2116](https://github.com/itakura-hidetoshi/KuuOS/pull/2116):** explicit **five-vertex fourfold pentagon** (three-edge versus two-edge), double dependent Nat-depth casts, genuine F44 quotient and original F45 tree/mate/η/ε compatibility |
| **v5.151** | **F54 / [PR #2118](https://github.com/itakura-hidetoshi/KuuOS/pull/2118):** arbitrary original F45 local Type-valued associativity rotation evidence in left/right finite binary contexts; genuine finite bidirectional rotation chains with lengths, append/reverse, full F19/F28 history and original F44 quotient preservation, actual chosen right mate and source η / target ε descent |
| **v5.152** | **F55 / [#2120](https://github.com/itakura-hidetoshi/KuuOS/pull/2120) [#2121](https://github.com/itakura-hidetoshi/KuuOS/pull/2121) [#2122](https://github.com/itakura-hidetoshi/KuuOS/pull/2122) [#2123](https://github.com/itakura-hidetoshi/KuuOS/pull/2123):** actual 3-versus-2 pentagon paths and two-order independent square, typed freely presented path-cell generators, double-index `depthEq` and preserved F44 quotient/whole native axis histories, original chosen right mate and actual η/ε specialization. Higher external 3-cell realization NOT proved |
| **v5.153** | **F56 / [#2125](https://github.com/itakura-hidetoshi/KuuOS/pull/2125) [#2126](https://github.com/itakura-hidetoshi/KuuOS/pull/2126) [#2127](https://github.com/itakura-hidetoshi/KuuOS/pull/2127) [#2128](https://github.com/itakura-hidetoshi/KuuOS/pull/2128) [#2129](https://github.com/itakura-hidetoshi/KuuOS/pull/2129):** conditional independent higher-cell target/interpreter, typed whisker/paste equations, 3/2 count obstruction, actual F44/complete F19-F28 history observation target, `F44ObservedCell ≃ PUnit`, raw proof-term noninjectivity and no-recovery, universal factorization-conditional no-go. External Gray/tricategory 3-cell realization **NOT proved** |

The source of mathematical truth is **the typed Lean theorem and its exact dependencies**, not the version number or a generic assertion that all higher coherence has been proved.


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

The converse does **not** hold in general. Neither v5.101 nor the finite original F19/F28 mate/exchange refinements through v5.153 establish arbitrary raw-morphism liftability, presentation-independent descent, or unrestricted equivalence across atlases.


## Reproduce the theorem-bearing result / 再現

Check out the **v5.153 F56 theorem-bearing commit**; do not confuse a later docs-only merge with a new proof:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 482e325d35b8186d43b0d503ebaceb7e3a498036
cat lean-toolchain

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationCoherentBiadjunctionFourfoldPentagonV5_150 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45PentagonTreesV5_150 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalRightMatePentagonV5_150 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftPentagonLeftV5_150 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftPentagonRightV5_150 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45LocalRotationV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45FiniteRotationChainsV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationContextsV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationDepthRoutesV5_152 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationInvariantsV5_152 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationMatesV5_152 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftDepthRotationV5_152 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ConditionalHigherCellTargetV5_153 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45HigherCellPastingObstructionV5_153 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ConcreteF44CellTargetV5_153 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellFactorizationNoGoV5_153
~~~

Selected F56-E build evidence: [CI #38107828541](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38107828541), **8862/8862** selected imported Lean dependency modules, **4/4** final `#print axioms` and zero changed-file diagnostics; F56-D [CI #38107624498](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38107624498) was also GREEN with 6/6. Neither receipt certifies a broader independent all-repository check or an AI runtime. See [ROADMAP.md](ROADMAP.md) for F1–F56 theorem references and F57 research boundaries.

For a broader **independent** build or runtime smoke test (not implied by the F53 theorem receipt):

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Remaining research and runtime boundaries / 次の課題

**Completed under precisely typed fixed-presentation hypotheses:** F1–F56, within each stated theorem scope. In addition to F1–F55's original actual-lift swallowtails, chosen right mates, F44 quotient, concrete local rotation pentagon/square and free Type-valued cells, F56 proves a conditional target interpreter, explicit whisker/pasting equations, a literal 3-vs-2 count obstruction, a constructed F44/full-history observational model, **subsingleton observational fibers**, and **no faithful factorization through the observation for raw presented higher proof terms**.

**Next formal frontier — F57 / v5.154, NOT YET PROVED at this snapshot:** identify and construct a genuine **path-sensitive** higher target, carrying information beyond F44's subsingleton endpoint certificates. It should supply independently meaningful pentagon/square and coherent native whiskering/pasting laws, and a comparison with actual original F/G, source η and target ε. A merely self-referential free-cell model is not by itself an external tricategorical/Gray 3-cell realization. Any faithfulness or universality theorem requires its exact hypotheses and independent Lean receipts.

**Other open work:** unrestricted tricategorical/Gray-categorical coherence and comparison equivalence, transport/descent across independently chosen presentations or labels, an unconditional higher universal mapping principle, infinite-stage convergence/uniform finite depth, and the empirical correctness/completeness of GitHub/MCP indexing, AI dialogue and interactive runtime/website behavior. These need separate explicit statements and independent receipts.

See [ROADMAP.md](ROADMAP.md), [GOVERNANCE.md](GOVERNANCE.md), [CITATION.cff](CITATION.cff), [LICENSE](LICENSE) and [COPYRIGHT.md](COPYRIGHT.md). Current docs describe the research; they neither enlarge usage rights nor grant unauthorized actions.
