# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, presentation-sensitive equivalence, higher coherence, descent, exact universal properties and explicit obstructions.

**Founder and copyright holder / 創始者・著作権者:** **Hidetoshi Itakura / 板倉英俊**. See [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE). Public repository access does **not** itself grant permission to reproduce, adapt, train on, redistribute or commercialize this work.

> An observation is not a global truth. Which relations survive a justified change of context or presentation? When can compatible local data descend, and where does an obstruction prevent that descent?


## Status / 現在地 — v5.154 · 2026-10-11 JST

**Latest verified theorem-bearing canonical `main`:** [PR #2134 / v5.154 F57-D MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2134), **`77f68f513189a73dd31e15a4004d4426257eb95f`**, freshly confirmed identical to `main` HEAD. **F1–F57-D are closed only in their individual precise Lean theorem scopes**. The geometric C60 pentagon/flag-square incidence gluing and F55 typed route labelling do NOT already establish independent Gray/tricategorical 3-cell semantics, unrestricted descent or infinite-stage convergence.

**日本語要約：** F1–F5は元のF/G・source η・target εと正逆swallowtail、F6–F39はnative adjunction/mate、元のF19 chosen-mate圏と独立のF28比較核商圏、F40–F46は操作順序を保持するType-valued F19/F28履歴と独立軸隣接交換によるF44商、そのF46分類を構築しました。F47–F53は本来のF45段階列、依存する二軸のNat深さ輸送、任意有限の二分木括弧付け、F44商上の5頂点pentagonを証明しました。F54は任意の左右文脈の局所回転と有限`RotationChain`を構成。**F55／v5.152では、異なる長さを持つ3回転・2回転pentagon経路と独立回転squareを具体的に構築し、`DepthRotationRoute.PresentedCell`を自由なType-valued高次関係の型として導入しました。すべての経路における2軸の深さ輸送後のF44商・完全履歴保存、および元のchosen right mateと実際のsource η／target εへの整合性をLeanで証明しました。** 異なる生の経路は同一視せず、外部tricategoryの3-cell実現は未証明です。 **F56／v5.153では、自由な`PresentedCell`を独立に指定した高次対象へ解釈する条件付き`HigherCellTarget`を構築し、貼り合わせ・左右文脈の解釈整合性と3対2の回転数を一律に保存できない障害を証明しました。元のF44交換商と二軸の全履歴に基づく実際の`F44ObservedCell`モデルを構成し、各固定境界で`PUnit`と同値であること、高次証拠を単射的に復元できないこと、さらにこの観測のみを経由する任意の解釈先で非忠実となる条件付き障害をLeanで証明しました。** **F57／v5.154では過去のv3.83–v3.90切頂二十面体（60頂点、90辺、12五角形、20六角形、頂点図5.6.6）を再接続しました。F57-Aは各辺の二端点×二隣接面からなる実際の四旗squareを構築し、五角形・六角形の共有辺を証明しました。F57-Bは元のC60五角形の5辺へF55の5つの型付き回転辺（長経路3・短経路2、向きの差を保持）を直接ラベル付け。F57-Cは任意の二つのF55深さ輸送付き経路の独立な2順序squareを構成しF44商と両軸全履歴の保存を証明、各幾何辺へ貼りました。F57-Dは隣接square間の同一dart・同一五角形面の旗の一致と最後から最初への閉路を証明しました。**

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
| Real C60 face/incidence geometry and five-edge signed original F55 pentagon | **v5.154 / F57-A/B**: reuses v3.83–v3.90 real 60V/90E/12P/20H C60 geometry. Each real truncated edge gives four distinct (endpoint dart, incident face) flags; each existing five-edge pentagon side has an adjacent pentagon/hexagon shared-edge flag square. The five geometric sides are labelled by five **actual typed F55 associativity rotations**, with long 3 edges forward and short 2 edges reversed relative to geometric boundary orientation. [F57-A flags](formal/KUOS/DependentOriginationTruncatedIcosahedralFlagSquaresV5_154.lean), [F57-B labels](formal/KUOS/DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154.lean), [PR #2131](https://github.com/itakura-hidetoshi/KuuOS/pull/2131), [PR #2132](https://github.com/itakura-hidetoshi/KuuOS/pull/2132) |
| F55-independent-depth square paths and actual cyclic C60 square-collar pasting | **v5.154 / F57-C/D**: two genuinely typed F19/F28 depth-aware finite route orders, exact count equality, separately proved original F44 exchange quotient and COMPLETE typed native histories; attach those square path pairs to every real C60 pentagon/hexagon shared edge. Consecutive geometric four-flag squares share the SAME incident (dart, pentagon face) corner flag, including cyclic slot s4→s0. [F57-C1](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45IndependentDepthSquaresV5_154.lean), [F57-C2](formal/KUOS/DependentOriginationTruncatedIcosahedralPentagonIndependentSquarePastingV5_154.lean), [F57-D](formal/KUOS/DependentOriginationTruncatedIcosahedralCyclicSquareCollarGluingV5_154.lean), [PR #2133](https://github.com/itakura-hidetoshi/KuuOS/pull/2133), [PR #2134](https://github.com/itakura-hidetoshi/KuuOS/pull/2134) |

**Scope boundary / 数学的境界：** F57 gives genuine finite C60 five-edge pentagons and **vertex–face incidence** four-flag squares, signed label maps into original F55 Type-valued rotation routes, two independently ordered depth-aware path squares, and proven **shared corner flags** of the cyclic five-square collar. C60 itself has NO quadrilateral polygonal faces; adjacent collar squares need not share their neighboring hexagon face. Equality of square endpoints in F44 or combinatorial flag gluing alone does NOT realize external Gray/tricategorical 3-cells or avoid F56-E's nonfaithfulness no-go for interpretations factoring only through F44 observations. Separate native 3-cell realization, coherence/interchange, original η/ε comparison and higher descent remain open.

## Exact authority and reproducibility / 正本と検証

| Item | Exact verified value |
| --- | --- |
| Repository / canonical branch | **[itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) / `main`** |
| **Latest theorem-bearing canonical `main` and F57 PR merge** | **`77f68f513189a73dd31e15a4004d4426257eb95f`**, [PR #2134 CLOSED/MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2134) |
| Latest validated F57-D PR source HEAD | **`e3a7c163056ce942e8732ddbc1c542df734fb947`** |
| Exact-head PR workflow | [Run **38110300250 — SUCCESS**](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38110300250) |
| Strict Lean validation | Job **114384304290 — SUCCESS**, **8863/8863** selected imported Lean build |
| Governance / audit | Job **114384611780 — SUCCESS** |
| MCP Lean / MCP CI completion receipts | Jobs **114384611746 / 114384636117 — SUCCESS** |
| Changed F57-D Lean diagnostics / axioms | **1 new Lean file**, **0 warnings / 0 errors**, **7/7 `#print axioms`**, no `sorryAx`/`sorry`/`admit`/new axiom |
| Pinned compiler | **Lean v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| Pinned mathlib | **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`** — [lake-manifest.json](lake-manifest.json) |

The exact-head receipt covers F57-D changed Lean module plus its imported dependency closure, not every repository workflow, running website or LLM model. Earlier F57-A/B/C have separate exact-head GREEN receipts; a later docs-only merge changes current `main` but does not add new mathematical theorems or replace the F57-D theorem-bearing SHA.

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
| **v5.154** | **F57 / [#2131](https://github.com/itakura-hidetoshi/KuuOS/pull/2131) [#2132](https://github.com/itakura-hidetoshi/KuuOS/pull/2132) [#2133](https://github.com/itakura-hidetoshi/KuuOS/pull/2133) [#2134](https://github.com/itakura-hidetoshi/KuuOS/pull/2134):** genuine old C60 finite incidence flag squares and pentagon/hexagon shared edges; actual five F55 one-rotation signed path labels on each pentagonal boundary; two disjoint independent F55 depth-aware path orderings with F44/full F19/F28 history certificates; **cyclic shared-corner flag gluing of all five C60 edge squares**. External higher Gray/tricategory 3-cell comparison remains unproved |

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

The converse does **not** hold in general. Neither v5.101 nor the finite original F19/F28 mate/exchange refinements through v5.154 establish arbitrary raw-morphism liftability, presentation-independent descent, or unrestricted equivalence across atlases.


## Reproduce the theorem-bearing result / 再現

Check out the **v5.154 F57 theorem-bearing commit**; do not confuse any later docs-only merge with a new proof:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 77f68f513189a73dd31e15a4004d4426257eb95f
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
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellFactorizationNoGoV5_153 \
  KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154 \
  KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45IndependentDepthSquaresV5_154 \
  KUOS.DependentOriginationTruncatedIcosahedralPentagonIndependentSquarePastingV5_154 \
  KUOS.DependentOriginationTruncatedIcosahedralCyclicSquareCollarGluingV5_154
~~~

Selected F57-D build evidence: [CI #38110300250](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38110300250), **8863/8863**, **7/7** final `#print axioms` and zero changed-file diagnostics. Other independent exact-head F57 receipts: [#38109064983](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38109064983) (F57-A, 8511/8511, 12 checks); [#38109672930](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38109672930) (F57-B, 8860/8860, 15 checks); [#38110046529](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38110046529) (F57-C, 8862/8862, 12 checks). Selected strict CI does not certify all possible runtime or model behavior; see [ROADMAP.md](ROADMAP.md).

For a broader **independent** build or runtime smoke test (not implied by the F53 theorem receipt):

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Remaining research and runtime boundaries / 次の課題

**Completed under precisely typed fixed-presentation hypotheses:** F1–F57-D. In addition to F1–F56's original actual-lift swallowtails, F19/F28 independent complete histories, original F44 quotient, genuine F55 pentagon/square route evidence and F56 observational no-go, F57-A–D now proves real C60 edge-four-flag geometry, complete five-edge labelled original Type-valued rotation pentagons, independently composed original depth-aware two-order squares with F44/full-history certificates, and all FIVE cyclic corner-flag gluing equalities, including closure.

**Next formal frontier — F58 / v5.155, NOT YET PROVED at this snapshot:** realize and compare the real F57 C60 pentagon-square cyclic incidence pasting in an independently specified path-sensitive higher-cell target with genuine original F/G/η/ε mate data. Prove target-level pentagon/square interchange/whiskering and any two-dimensional/three-dimensional coherence under explicit hypotheses; do NOT identify geometric flags with native Gray/tricategory 3-cells or claim global biequivalence merely from matching finite incidence and F44 observations. The original F56-E observation-factorization obstruction still applies.

**Other open work:** unrestricted tricategorical/Gray-categorical coherence and comparison equivalence, transport/descent across independently chosen presentations or labels, an unconditional higher universal mapping principle, infinite-stage convergence/uniform finite depth, and the empirical correctness/completeness of GitHub/MCP indexing, AI dialogue and interactive runtime/website behavior. These need separate explicit statements and independent receipts.

See [ROADMAP.md](ROADMAP.md), [GOVERNANCE.md](GOVERNANCE.md), [CITATION.cff](CITATION.cff), [LICENSE](LICENSE) and [COPYRIGHT.md](COPYRIGHT.md). Current docs describe the research; they neither enlarge usage rights nor grant unauthorized actions.
