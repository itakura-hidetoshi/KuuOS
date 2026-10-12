# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a research architecture for dependent origination (縁起), non-reification (空), context-sensitive reasoning, presentation-sensitive equivalence, higher coherence, descent, exact universal properties and explicit obstructions.

**Founder and copyright holder / 創始者・著作権者:** **Hidetoshi Itakura / 板倉英俊**. **License / ライセンス:** [Apache License, Version 2.0](LICENSE) (SPDX: `Apache-2.0`). Covered KuuOS source code, Lean formalizations, and documentation may be used, copied, modified, and redistributed—including commercially—under the license's terms. See [NOTICE](NOTICE) for attribution and [COPYRIGHT.md](COPYRIGHT.md) for scope and historical provenance. Copyright ownership remains with the contributor(s); this is an open-source license grant.

> An observation is not a global truth. Which relations survive a justified change of context or presentation? When can compatible local data descend, and where does an obstruction prevent that descent?


## Status / 現在地 — v5.208 · F59-F59-A/B · 2026-10-13 JST

**Latest verified theorem-bearing baseline / 最新の定理を含む正本:** **[PR #2219 — v5.208 / F59-F59-A/B MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2219)**, theorem-bearing squash merge SHA **`225ba4ff68aaf7215d58c3596a5e0d21f401a317`**, independently re-observed equal to canonical `main` immediately after merge. Previous v5.207 F58 [#2217](https://github.com/itakura-hidetoshi/KuuOS/pull/2217) remains a mathematical dependency; documentation-only commits advance canonical `main` without adding a new theorem. Apache-2.0 licensing under [#2210](https://github.com/itakura-hidetoshi/KuuOS/pull/2210) remains unchanged.

**Exact-source-tree formal validation:** [GitHub Actions #38309591977](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38309591977) — **completed SUCCESS** on final PR source head `bcb189ab348eda17920726f711354686797006f2`. GitHub Actions checked its temporary merge commit `3f4bbc48f9629380238cb4c94f2c5a5e30f11187` with the **identical Git tree** `45a23f5a918f92e00d6b577f197bcf0d4e2cdc72`, verified separately against the actual PR source HEAD. Strict Lean **9014/9014**, changed-file warnings/errors **0/0**, **14 `#print axioms`** across two v5.208 files, no `sorryAx`/new axioms; Governance and MCP Lean/CI receipts all **SUCCESS**. Inherited finite C60 `native_decide` dependencies are not newly asserted axioms.

**日本語要約：** 元の `F/G/η/ε`、swallowtail、独立F19/F28の履歴と商、実C60 60頂点・90辺・12五角形・20六角形、元F42/F43および独立F54/F55の型付き証明項を保持しています。v5.202のF52商圏での真の3射五角形・三角形、v5.203の元F43交換自然変換、v5.204のF47混合圏全Homの完全忠実性と元F55 no-lift、v5.205〜206の文脈移送・三表示コサイクルを継承。**v5.207／F59-F58-A/B**では、元F42左/右 `Quiver.Path` 文脈移送と独立F54/F55木文脈の前後でF47混合面選択を行う2経路が、**四つの型付き境界タグを保持する3-Hom射として交換する**と証明しました。依存型Hom transportを明示し、Mathlib **左右Beck–Chevalley NatIso**を構成。さらに全90実物理辺・実際の2隣接五角形/六角形それぞれの**異なるC60閉路基点**に特殊化し、全4旗標の入射性を確認。どちらの元F42/F54左右文脈化後も**元のF55全9生成子からの新設 `Δ=(0,1;0)` の持ち上げは不可能**です。元F55北五角形の非平坦性と大域no-vertex-gaugeは存続し、無条件descentを意味しません。

**v5.208／F59-F59-A/B 新規証明：** 二つの**連続する元F42 Quiver.Path文脈**と、独立した二つの**元F54/F55 bracket-tree文脈**を左右それぞれで型付きのまま合成しました。Mathlibの関手結合子と左右のiso-whiskeringを明示し、F58の2つのBeck–Chevalley自然同型から**二段のsource-level NatIso**と全Hom射の自然性を構成しました。中間F43/F55の完全native像の一致を証明して正しい第二段F47面変更関手を作り、実C60全90物理辺で異なる2隣接原多角形面の閉路基点に特殊化しました。いずれの2段文脈の後も、新設 `Δ=(0,1;0)` は元F55の全9構成子から持ち上がりません。**ただし直接連結した元F42経路／元F54木との同一性と三段のpentagon整合性は未証明**であり、今後のF59-F60課題です。

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
| **[v5.204 / F59-F55-A/B](https://github.com/itakura-hidetoshi/KuuOS/pull/2211)** | 元の2隣接C60実面間の新設F47混合4境界圏移送が4対象と全3-Homで全単射。90辺×両面で元F54左右回転境界の全9構成子F55語は新設 `Δ=(0,1;0)` を実現できず、元F55辺場に大域頂点ゲージは存在しない。原F42/F54の原構文同一視と無条件descentは未証明。 |
| **[v5.205 / F59-F56-A/B](https://github.com/itakura-hidetoshi/KuuOS/pull/2213)** | 同じ元F54経路型の新設F47混合4境界圏で恒等・往復・三表示コサイクルの**型付き3射等式・Mathlib NatIso**。元F42の左右Quiver.Path文脈と独立元F54/F55木文脈の忠実な異型混合4境界関手を構成。大域幾何学的descentは未証明。 |
| **[v5.206 / F59-F57-A/B](https://github.com/itakura-hidetoshi/KuuOS/pull/2215)** | **三つすべての元F42面経路と元F54独立回転境界型が異なる**混合F47四境界移送について、全Homのfullness＋faithfulness・4対象位置全単射、往復・三表示コサイクルの**Mathlib NatIso**をLean証明。元F42の左右実経路と元F54/F55の左右木文脈の合成関手はfull and faithful、どちらの文脈化後も実際のF47混合比較は成立するが元のF55 9生成子からの`Δ`持ち上げは不可能。符号付き非平坦性と境界出自を保持。 |
| **[v5.207 / F59-F58-A/B](https://github.com/itakura-hidetoshi/KuuOS/pull/2217)** | 元F42の左右の独立した実経路／元F54木文脈とF47混合面変更との**両順序を、依存型Hom transport込みで型付き3-Hom射の等式として比較**。Mathlib **左右Beck–Chevalley NatIso**を構成。**全90実C60物理辺×2隣接原面**で別々の閉路基点を保持して特殊化し、本当の四旗標入射・2原面の相違を維持。両側で元F55の9構成子から新設 `Δ=(0,1;0)` を得ることは不可能。大域原F42/F54/F55 Gray 3-圏や無条件の幾何descentは未証明。 |
| **[v5.208 / F59-F59-A/B](https://github.com/itakura-hidetoshi/KuuOS/pull/2219)** | **二段連続**する元F42実経路と独立元F54/F55木文脈の左右source-level BC貼り合わせNatIso。Mathlib関手結合子とiso-whiskering、全Hom自然性、完全native像による二段目F47混合面選択。**実C60全90辺×2隣接原面**に特殊化し、二段後の元F55全9構成子からの補正 `Δ` 非持ち上げをLean証明。直接合成された原構文との比較、三文脈pentagon、大域descentは未証明。 |

**Status vocabulary:** “PROVED” means the **stated Lean declaration** and its hypotheses, not a blanket claim over all presentations. “Adjoined” indicates genuinely new source generators; “graded envelope” is not a fully faithful reconstruction of raw F42/F54/F55 higher source syntax.


## Exact authority and reproducibility / 正本と検証

| Item | Verified evidence |
| --- | --- |
| Repository | **[itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)** · canonical branch `main` |
| Latest theorem-bearing merge | **`225ba4ff68aaf7215d58c3596a5e0d21f401a317`** · [#2219 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2219), distinct from later docs-only SHA |
| Validated PR source | `bcb189ab348eda17920726f711354686797006f2` · source tree equals tested merge tree `45a23f5a918f92e00d6b577f197bcf0d4e2cdc72` |
| Exact-source-tree CI | [#38309591977 — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38309591977) |
| Strict Lean job | `115011859612` · **9014/9014 SUCCESS** · changed-file warning/error **0/0** |
| Governance / MCP receipts | Governance `115012620238`, MCP Lean `115012620254`, MCP CI `115012681045` · **all SUCCESS** |
| Changed-file axiom inspection | **14 `#print axioms`** across two new v5.208 modules; no `sorryAx`/new axiom; inherited C60 finite `native_decide` dependencies noted |
| Toolchain | [Lean `v4.30.0-rc2`](lean-toolchain); [mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`](lake-manifest.json) |
| Protected experimental lane | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) · **OPEN / DRAFT / NOT MERGED** (Lean 4.31 validation only) |

**Authority order:** freshly observed exact GitHub canonical SHA → actual formal Lean declarations and their imported dependencies → README/ROADMAP → exact-head CI, governance and MCP receipts → prior discussion and history. A documentation-only commit must not be represented as a newly proved theorem. Each PR's source HEAD and the post-merge `main` SHA are different objects and must be reported separately.

**Scientific scope:** A successful selected Lean build verifies the selected formal dependency closure. It does **not** certify every repository workflow, mathematical claim not encoded in Lean, external Gray 3-equivalence, the behavior of a hosted AI runtime, or the weights of an underlying language model. Rights to use and redistribute licensed original material are governed by [LICENSE](LICENSE), [NOTICE](NOTICE), and [COPYRIGHT.md](COPYRIGHT.md); open-source permission is distinct from proof or deployment authority.

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
| **v5.204 / F55-A/B** | **[#2211](https://github.com/itakura-hidetoshi/KuuOS/pull/2211)**: proof-relevant raw F47 transport yields full and faithful functors and bijection of the four mixed boundary positions across real incident C60 faces; forward/backward Mathlib face-choice biface source functors and typed square transport for all 90 real edges. On all 180 actual sites, no old original F55 nine-generator PresentedCell between the exact original F54 square routes can replace the newly adjoined mixed comparison. Proves a fully faithful LOCAL source atlas **together with a GLOBAL original-F55 vertex-gauge no-go**, retaining north second charge `−5`. [Fullness](formal/KUOS/DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204.lean), [original F55 no-go](formal/KUOS/DependentOriginationGrayC60F55MixedDescentObstructionV5_204.lean). |
| **v5.205 / F56-A/B** | **[#2213](https://github.com/itakura-hidetoshi/KuuOS/pull/2213)**: genuine mixed F47 kernel-quotient typed identity/round-trip/three-frame cocycle on every 3-Hom with natural isomorphisms; distinct original F42 left/right 1-path whiskering and original F54/F55 bracket-route context functors connected through correctly typed mixed four-boundary functors, including source mixed-square compatibility. **No arbitrary original raw-source equivalence and no global nonflat F55 descent.** | [cocycle](formal/KUOS/DependentOriginationGrayC60F55MixedCocycleV5_205.lean); [contexts](formal/KUOS/DependentOriginationGrayC60F55MixedOriginalContextV5_205.lean) |
| **v5.206 / F57-A/B** | **[#2215](https://github.com/itakura-hidetoshi/KuuOS/pull/2215)** extends F56's faithful **cross-original F42/F54 context functor** to a bijection on four F47 mixed boundary tags and all parallel 3-Homs, and extends its cocycle to THREE INDEPENDENT original F54 route types (plus three original F42 paths). Both roundtrip and three-context transitions yield genuine typed Mathlib NatIso. True independent original F42 left/right path and original F54/F55 left/right tree contexts are now full/faithful, and neither can make the adjoined `Δ` an original nine-generator F55 PresentedCell despite their genuine mixed source square. [Cross-original cocycle](formal/KUOS/DependentOriginationGrayC60F55CrossRotationCocycleV5_206.lean), [context no-lift](formal/KUOS/DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206.lean). |
| **v5.207 / F58-A/B** | **[#2217](https://github.com/itakura-hidetoshi/KuuOS/pull/2217)**: source-aware **left/right Beck–Chevalley natural isomorphisms** comparing original F42 Quiver.Path / independent original F54/F55 bracket-tree contextual whiskering before/after F47 mixed face-choice; full four-tag dependent Hom casts and genuine source 3-Hom equality in the existing F47 full-native-kernel quotient. Specialized to **all 90 genuine physical C60 edges and each pair of true adjacent original polygon faces**, with **independent face-loop base darts** and certified original four-flag incidence. Original nine-constructor F55 Δ non-lift persists after both contexts. [general source NatIso](formal/KUOS/DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207.lean), [physical incidence](formal/KUOS/DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207.lean). |

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

The converse does **not** hold in general. Even the proved fixed-presentation swallowtails, the original F19/F28 mate/exchange histories, and the C60 graded Gray work through v5.207/F58-A/B do not establish arbitrary raw-morphism liftability, presentation-independent descent, or unrestricted equivalence across atlases.


## Reproduce the theorem-bearing result / 再現

Check out the **theorem-bearing SHA** rather than a later docs-only `main`. Build the exact v5.207 general original F42/F54 Beck–Chevalley and physical ninety-edge incidence modules plus their imported source proof closure under the pinned toolchain:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 88ff04cd6d3bfe5e6ad2f335b4f6b40aefe5e4fe
cat lean-toolchain
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207 \
  KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
~~~

Corresponding exact-head [CI #38293817765](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38293817765): **9012/9012**, changed Lean warnings/errors **0/0**, **16 `#print axioms`**, no `sorryAx`/new axioms; Strict Lean, Governance and MCP Lean/CI receipts **all SUCCESS**. This validates the selected typed F47 source comparisons, not original unquotiented F42/F54/F55 global gluing, unconditional physical descent or deployed runtime correctness.

A broader whole-project formal build and runtime check are independent tasks, **not implied** by this selected CI receipt:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## Remaining research and runtime boundaries / 次の課題

**Next theorem frontier — v5.208 / F59-F59:** v5.207/F58 [#2217](https://github.com/itakura-hidetoshi/KuuOS/pull/2217) now proves left/right original F42/F54 contextual **Beck–Chevalley NatIso** with actual two-face incidence at all 90 physical C60 edges and independently based paths. Next prove a genuinely typed **two-successive-context cube/pasting compatibility** for the source Beck–Chevalley squares, compare independent original left/right context order with accurate `Quiver.Path.comp_assoc` transports and original F54 bracket trees, and evaluate local-to-global conditions without erasing signed F55 curvature. ADJOINED F47 `Δ=(0,1;0)` cannot be backdated as an original nine-constructor F55 cell. A globally faithful raw F42/F54/F55 Gray 3-category, arbitrary original-source interchange, and unconditional descent remain OPEN.

**Further obligations:** globally coherent and faithful original F42–F54/F55 mixed 0/1/2/3-source realization; target-level pentagon/square/whiskering and Gray exchange with the *same original boundaries*; a genuinely correct interpretation or explicitly recorded obstruction for the added `Δ=(0,1;0)` (not produced by the old nine F55 constructors); preservation of original nonzero face curvature, lawful transport and conditional/descent checks. Unrestricted tricategorical/Gray-categorical equivalence, presentation-independent global descent, infinite convergence and universal mapping claims remain open unless stated by separate exact Lean declarations.

**Runtime:** `LLM + KuuOS reasoning runtime + formal authority layer` is a research integration architecture. GitHub formal artifacts do not establish that KuuOS is baked into an LLM's trained parameters, that a chat app loads every theorem, or that external actions were authorized. Runtime integration, version provenance, access/consent boundaries and empirical tests require separate evidence.

See [ROADMAP.md](ROADMAP.md), [GOVERNANCE.md](GOVERNANCE.md), [CITATION.cff](CITATION.cff), [LICENSE](LICENSE), [NOTICE](NOTICE), and [COPYRIGHT.md](COPYRIGHT.md). **Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Licensed under Apache-2.0.** Redistribution, adaptation, and commercial use are permitted subject to the license's conditions; no additional prohibition on AI training is imposed by this project license. No scientific, clinical, or operational authorization follows from the copyright license.
