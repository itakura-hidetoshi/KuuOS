# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, presentation-sensitive equivalence, higher coherence, descent, exact universal properties and explicit obstructions.

**Founder and copyright holder / 創始者・著作権者:** **Hidetoshi Itakura / 板倉英俊**. See [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE). Public repository access does **not** itself grant permission to reproduce, adapt, train on, redistribute or commercialize this work.

> An observation is not a global truth. Which relations survive a justified change of context or presentation? When can compatible local data descend, and where does an obstruction prevent that descent?


## Status / 現在地 — v5.203 · F59-F54 · 2026-10-12 JST

**Latest verified theorem-bearing baseline / 最新の定理を含む正本:** **[PR #2208 — v5.203 / F59-F54 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2208)**, theorem-bearing merge SHA **`e7b2fcf01946b1164dce278f52b9ab427ec85db6`** (re-observed as canonical `main` immediately after the squash merge). [#2206](https://github.com/itakura-hidetoshi/KuuOS/pull/2206) remains the v5.202/F53 original F42 pentagon/triangle ancestor. The docs-only PR may advance live `main` without adding a theorem.

**Exact-head formal validation:** [GitHub Actions #38235636769](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38235636769) — **SUCCESS** at exact final PR source `e216ca2cb65344f1c8a03e35e0e3b9811199ee54`: Strict Lean **9004/9004**, changed-file Lean warnings/errors **0/0**, **23 `#print axioms`** across two new modules, no `sorryAx` or new axiom, Governance and both MCP Lean/CI receipts **SUCCESS**. Inherited C60 `native_decide` dependencies remain separate from newly asserted axioms.

**日本語要約：** 既存のF/G/η/εとswallowtail、F19/F28の独立履歴、真正のC60（60頂点・90辺・12五角形・20六角形）、F42/F43の証明項・交換3射を維持しています。v5.197のgraded Gray 3-圏包絡モデル、v5.199の原F42水平/縦3-Hom関手、v5.200の結合子・単位子、v5.201の経路transport、v5.202の原F42の型付き五角形・三角形（F52 full-native-kernel商圏）を継承しました。**v5.203/F54**では、元のF43交換を真正の自然同型成分として保持し、左先行から右先行へのMathlib水平3-Hom自然変換と右先行関手を構成。C60の全90辺×両隣接面において、元F42/F43と独立した元F54/F55境界を保持する局所混合比較へ接続し、完全な整数電荷・位相を保つ一意補正 `Δ=(0,1;0)` を証明しました。**元のF55原3射の生成子がΔを与えたとは主張せず**、北五角形の局所非平坦性・descent障害を保存しています。

**重要な境界：** これは「元の全F42／F54／F55生成子を忠実に貼り合わせた完全な大域的・非退化Gray 3-圏」が成立したという意味ではありません。F47の混合補正 `Δ=(0,1;0)` は**新設の混合3射**であり、元のF55の9構成子からは得られません。元のF55辺場の北五角形局所曲率は非零のままです。Lean定理の範囲をAIモデルそのものの変更・実行時の正しさ・無条件のdescentと同一視しません。

| Verified frontier | What is established — and what is not |
| --- | --- |
| **F1–F57 / v5.93–v5.154** | 元の `F/G/η/ε`、swallowtail、独立F19/F28履歴、実F45回転経路、C60実幾何・5辺pentagonと四旗標。歴史と各Leanの詳細は下表および[ROADMAP](ROADMAP.md)。 |
| **F58 / v5.155 onward** | C60実5/6角面・32面符号付き境界、native Gray 3射、独立整数電荷・交換位相、H¹/H²/局所曲率の評価等を、各定理の型付き範囲で構築。**全域的な原表示の貼り合わせとは異なる**。 |
| **F59 / v5.156–v5.193** | `BraidedCategory GrayGrade`、C60 90辺の元のF55高次射ラベル、局所非平坦性と修復・位相拘束、陰陽・四象・六気などの型付き幾何写像、元のF42/F43局所面3-Homとwhiskeringを段階的に形式化。 |
| **[v5.194 / F59-F46](https://github.com/itakura-hidetoshi/KuuOS/pull/2194)** | 90実辺の四旗標と元のF55型付き3射の局所接続、C60 `(0,0;1)` 対 F55 `(0,1;1)`、一意の補正 `Δ=(0,1;0)`。 |
| **[v5.195 / F59-F47](https://github.com/itakura-hidetoshi/KuuOS/pull/2195)** | 4つの厳密な2射境界を持つ**新設の混合3-Hom圏**と忠実なGray関手。混合比較正方形、左右whiskering、Gray交換自然性。 |
| **[v5.196 / F59-F48](https://github.com/itakura-hidetoshi/KuuOS/pull/2196)** | 全90辺×両隣接実面での型付き混合比較と面選択変更関手。北五角形で補正場の第二整数電荷 `−5`・位相0、元のF55辺場の非平坦性を保持。 |
| **[v5.197 / F59-F49](https://github.com/itakura-hidetoshi/KuuOS/pull/2197)** | C60の60個の元の0対象・元の経路を保つgraded Gray 3-圏包絡モデル。Mathlibの3-Hom合成関手、交換3射、自然性、五角形・六角形等の整合性。**2射はgrade-completed**。 |
| **[v5.198 / F59-F50](https://github.com/itakura-hidetoshi/KuuOS/pull/2198)** | 元のF42証明項を保持する局所3-Hom・次数付き原2射圏、F43 3射の忠実関手、左右whiskering、全90辺の原F55比較。元の2射の相異と次数像の一致を区別。 |
| **[v5.199 / F59-F51](https://github.com/itakura-hidetoshi/KuuOS/pull/2199)** | 元のF43にはなかった任意の水平／縦コンテキスト3射合成を**明示的に付加**。元のF42証明項上の水平・縦3-HomをMathlib積圏関手にし、F49 Grayの整数電荷・位相と整合。 |
| **[v5.200 / F59-F52-A](https://github.com/itakura-hidetoshi/KuuOS/pull/2202)** | 元のF42証明項の2つのC60 path-index transport、型付き**新設**結合子・左右単位子、F52 3-Hom圏、F51の忠実包含、Mathlib水平積圏関手、**任意のF52 3射に対する結合子・単位子自然性**と元F43北五角形の非自明交換位相保持。**四因子pentagon／triangleは未証明**。 |
| **[v5.201 / F59-F53-A](https://github.com/itakura-hidetoshi/KuuOS/pull/2204)** | 既存F52の実C60経路に対する四因子pentagonの**2本のpath-equalityルート**とunit triangleの**2ルート**を構成し、元F42証明項と任意のF52型付き3射へtransport。Mathlib再添字関手・忠実性、および結合子と左右単位子の**source-aware同型**をLeanで証明。**3射のpentagon／triangle方程式そのものは未証明**。 |
| **[v5.202 / F59-F53-B/C](https://github.com/itakura-hidetoshi/KuuOS/pull/2206)** | 四つの元のF42証明項上に、**結合子3射の2段・3段五角形**と**結合子＋左単位子 対 右単位子の3射三角形**を実際のC60 path transport込みで構成。両等式を**F52 full-native-kernel商3-Hom**でLean証明。原3射語の構文的同一性や原F54/F55との大域貼り合わせは未証明。 |
| **[v5.203 / F59-F54](https://github.com/itakura-hidetoshi/KuuOS/pull/2208)** | 元F43交換3射による右先行Mathlib 3-Hom関手・元F43自然変換、位相1の非自明交換とF53五角形/三角形右先行文脈の整合。**90辺×両隣接面**で、元F52面交換と別型の元F54/F55回転3射を新設F47混合比較に接続し、完全native較正 `Δ=(0,1;0)`・一意性・元F55にないこと・北五角形の非平坦性を維持。大域的に忠実な原Gray 3-圏はなお未証明。 |

**Status vocabulary:** “PROVED” means the **stated Lean declaration** and its hypotheses, not a blanket claim over all presentations. “Adjoined” indicates genuinely new source generators; “graded envelope” is not a fully faithful reconstruction of raw F42/F54/F55 higher source syntax.


## Exact authority and reproducibility / 正本と検証

| Item | Verified evidence |
| --- | --- |
| Repository | **[itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)** · canonical branch `main` |
| Latest theorem-bearing merge | **`e7b2fcf01946b1164dce278f52b9ab427ec85db6`** · [#2208 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2208), not a later docs-only SHA |
| Validated PR source | `e216ca2cb65344f1c8a03e35e0e3b9811199ee54` |
| Exact-head CI | [#38235636769 — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38235636769) |
| Strict Lean job | `114765911782` · **9004/9004 SUCCESS** · changed-file warning/error **0/0** |
| Governance / MCP receipts | Governance `114766960521`, MCP Lean `114766960592`, MCP CI `114767013036` · **all SUCCESS** |
| Changed-file axiom inspection | **23 `#print axioms`** across two v5.203 modules; no `sorryAx`/new axiom; inherited C60 finite `native_decide` dependencies documented |
| Toolchain | [Lean `v4.30.0-rc2`](lean-toolchain); [mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`](lake-manifest.json) |
| Protected experimental lane | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) · **OPEN / DRAFT / NOT MERGED** (Lean 4.31 validation only) |

**Authority order:** freshly observed exact GitHub canonical SHA → actual formal Lean declarations and their imported dependencies → README/ROADMAP → exact-head CI, governance and MCP receipts → prior discussion and history. A documentation-only commit must not be represented as a newly proved theorem. Each PR's source HEAD and the post-merge `main` SHA are different objects and must be reported separately.

**Scientific scope:** A successful selected Lean build verifies the selected formal dependency closure. It does **not** certify every repository workflow, mathematical claim not encoded in Lean, external Gray 3-equivalence, the behavior of a hosted AI runtime, or the weights of an underlying language model. Copyright and usage limits remain governed by [COPYRIGHT.md](COPYRIGHT.md) and [LICENSE](LICENSE).

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


| **v5.155–v5.173** | **F58/F59:** original C60 90-edge F55 edge labels, 32 signed face boundaries, native `GrayGrade` braided category with independent `Int × Int` charge and `ZMod 2` phase, cellular H¹/H²/descent machinery, nonflat original north-pentagon curvature and precisely scoped repair/obstruction theorems. See [native braided target](formal/KUOS/DependentOriginationGrayNativeBraidedCategoryV5_156.lean), [signed face obstruction](formal/KUOS/DependentOriginationGrayC60ActualF55CurvatureRepairV5_167.lean). |
| **v5.170–v5.189** | **F59:** geometric and algebraic Yin–Yang/complex/four-image/six-qi/Wang Bi representations and genuine original C60 path-level Mathlib functors, with their explicit target/scope restrictions. See [Yin–Yang four images](formal/KUOS/DependentOriginationGrayC60YinYangFourImagesV5_170.lean), [Wang Bi descent](formal/KUOS/DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174.lean), [C60 native paths](formal/KUOS/DependentOriginationGrayC60NativePathFunctorV5_189.lean). |
| **v5.190–v5.193** | **F59:** original C60 proof-relevant F42 physical-face 2-cells; F43 source 3-cell interchanger, F44 categorical 3-Hom quotients; F45 genuine source 1-path left/right whiskering. [Original faces](formal/KUOS/DependentOriginationGrayC60PresentedFaceTwoCellsV5_190.lean), [original interchanger](formal/KUOS/DependentOriginationGrayC60PresentedInterchangerV5_191.lean), [3-Hom category](formal/KUOS/DependentOriginationGrayC60ThreeHomCategoriesV5_192.lean), [whiskering](formal/KUOS/DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193.lean). |
| **v5.194–v5.196** | **F59-F46–F48 / [#2194](https://github.com/itakura-hidetoshi/KuuOS/pull/2194) [#2195](https://github.com/itakura-hidetoshi/KuuOS/pull/2195) [#2196](https://github.com/itakura-hidetoshi/KuuOS/pull/2196):** real 90-edge, two-face F55 local comparisons; exact new mixed correction `Δ=(0,1;0)`; distinct typed original 2-cell boundaries, faithful local mixed category/functors, surviving nonflat north curvature. |
| **v5.197** | **F59-F49 / [#2197](https://github.com/itakura-hidetoshi/KuuOS/pull/2197):** original-C60-0/1-path **graded Gray 3-category envelope**, Mathlib coherent 3-Hom/tensor functors, native nonidentity exchange, five-/six-angle higher coherence in the stated graded model. [Gray source](formal/KUOS/DependentOriginationGrayC60GradedGrayThreeCategoryV5_197.lean), [certificate](formal/KUOS/DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197.lean). |
| **v5.198** | **F59-F50 / [#2198](https://github.com/itakura-hidetoshi/KuuOS/pull/2198):** source-aware F42 original proof-relevant 2-cell 3-Hom and faithful F43 Gray lift, decorated objects and left/right whiskering, all 90-edge F55 face comparison. [Original F43 lift](formal/KUOS/DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198.lean). |
| **v5.199** | **F59-F51 / [#2199](https://github.com/itakura-hidetoshi/KuuOS/pull/2199):** explicit **new** typed horizontal and vertical-context 3-cell constructors on original F42 sources, genuine Mathlib bifunctors and faithful original F43 inclusion, full graded Gray coherence. [Source constructors](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199.lean), [horizontal/vertical functors](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199.lean), [source-Gray coherence](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199.lean). |
| **v5.200** | **F59-F52-A / [#2202](https://github.com/itakura-hidetoshi/KuuOS/pull/2202):** adjoined typed source associator/unitor with exact two-path transport, full-native quotient 3-Hom and faithful F51 inclusion, horizontal bifunctor, associator/left/right unitor naturality, old north F43 exchange still odd. [Source](formal/KUOS/DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200.lean), [3-Hom](formal/KUOS/DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200.lean), [naturality](formal/KUOS/DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200.lean). Pentagons/triangles on four original words and F54/F55 global gluing remain open. |
| **v5.201 / F53-A** | **[#2204](https://github.com/itakura-hidetoshi/KuuOS/pull/2204):** exact C60 path pentagon/triangle 2-route equalities and F42 two-boundary / F52 3-arrow dependent transports; Mathlib faithful reindex functor; source-aware associator and unit **isomorphisms**. [Lean source](formal/KUOS/DependentOriginationGrayC60OriginalFacePentagonTransportV5_201.lean). Does **not** prove full source-3-arrow pentagon or triangle pasting. |
| **v5.202 / F53-B/C** | **[#2206](https://github.com/itakura-hidetoshi/KuuOS/pull/2206):** explicit source F42 4-face **two-step vs three-step 3-associator pentagon**, and genuine **associator + left unitor vs right unitor** source 3-arrow triangle, with actual original C60 1-path transport and faithful original F42 witness indices. Equalities proved in F52 full-native-kernel quotient. [Pentagon source](formal/KUOS/DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202.lean), [triangle source](formal/KUOS/DependentOriginationGrayC60OriginalFaceUnitTriangleV5_202.lean). Global original F54/F55 coherent gluing remains open. |
| **v5.203 / F54** | **[#2208](https://github.com/itakura-hidetoshi/KuuOS/pull/2208)**: old F43 original exchange source isomorphism and natural transformation from left-first to independently derived right-first horizontal F52 3-Hom bifunctor; original nonidentity phase and 202 pentagon/triangle coherence retained. At 180 real C60 edge/incident-face sites, explicit F52 original F43 face 3-arrow is calibrated to old F54/F55 rotation square through **new** F47 four-boundary mixed comparison `Δ`, unique full native value. Proven local equality and nonflat obstruction, **not** global all-original Gray 3-category. [F43 right-first](formal/KUOS/DependentOriginationGrayC60OriginalF43RightHorizontalV5_203.lean), [F55 bridge](formal/KUOS/DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203.lean). |

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

The converse does **not** hold in general. Even the proved fixed-presentation swallowtails, the original F19/F28 mate/exchange histories, and the C60 graded Gray work through v5.203/F54 do not establish arbitrary raw-morphism liftability, presentation-independent descent, or unrestricted equivalence across atlases.


## Reproduce the theorem-bearing result / 再現

Check out the **theorem-bearing SHA**, not a later docs-only `main`. Rebuild both v5.203 F54 Lean modules and their precise F43/F52/F53 and original F47 mixed-boundary import closure under the pinned toolchain:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout e7b2fcf01946b1164dce278f52b9ab427ec85db6
cat lean-toolchain
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationGrayC60OriginalF43RightHorizontalV5_203 \
  KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203
~~~

Corresponding exact-head [CI #38235636769](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38235636769): **9004/9004**, changed Lean warnings/errors **0/0**, **23 `#print axioms`** and no `sorryAx`; Governance and both MCP receipts **SUCCESS**. This certifies the selected imported Lean declarations, not arbitrary raw F54/F55 gluing, unconditional descent or deployed runtime correctness.

A broader whole-project formal build and runtime check are independent tasks, **not implied** by this selected CI receipt:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Remaining research and runtime boundaries / 次の課題

**Next theorem frontier — v5.204 / F59-F55:** v5.203/F54 [#2208](https://github.com/itakura-hidetoshi/KuuOS/pull/2208) now proves a source-typed **F43 natural exchange**, right-first F52 horizontal bifunctor and correct **local 180-site F43/F55 mixed cospans**. Next formalize higher composition, F43-F54/F55 mixed naturality and local-to-global gluing with actual four-boundary F47 data, explicitly test compatibility of neighbor transitions and signed face curvature, and retain obstruction when descent fails. The correction `Δ=(0,1;0)` does **not** exist as one of the original nine F55 constructors; original F42/F54/F55 source categories remain separate. A globally faithful, nondegenerate Gray 3-category and runtime soundness are NOT yet proved.

**Further obligations:** globally coherent and faithful original F42–F54/F55 mixed 0/1/2/3-source realization; target-level pentagon/square/whiskering and Gray exchange with the *same original boundaries*; a genuinely correct interpretation or explicitly recorded obstruction for the added `Δ=(0,1;0)` (not produced by the old nine F55 constructors); preservation of original nonzero face curvature, lawful transport and conditional/descent checks. Unrestricted tricategorical/Gray-categorical equivalence, presentation-independent global descent, infinite convergence and universal mapping claims remain open unless stated by separate exact Lean declarations.

**Runtime:** `LLM + KuuOS reasoning runtime + formal authority layer` is a research integration architecture. GitHub formal artifacts do not establish that KuuOS is baked into an LLM's trained parameters, that a chat app loads every theorem, or that external actions were authorized. Runtime integration, version provenance, access/consent boundaries and empirical tests require separate evidence.

See [ROADMAP.md](ROADMAP.md), [GOVERNANCE.md](GOVERNANCE.md), [CITATION.cff](CITATION.cff), [LICENSE](LICENSE) and [COPYRIGHT.md](COPYRIGHT.md). **Copyright © 2026 Hidetoshi Itakura / 板倉英俊; all rights reserved.** This document grants no new redistribution, commercial-use, adaptation or model-training rights.
