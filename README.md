# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**創案者・著作権者 / Founder and copyright holder: 板倉英俊（Hidetoshi Itakura）**

**KuuOS（空OS）**は、空（実体視しないこと）と縁起（条件による関係成立）を、文脈依存の観測・推論・表現の変換・整合性・降下（descent）・障害（obstruction）・普遍性として取り扱う研究アーキテクチャです。

KuuOS is a public-facing research architecture for context-sensitive reasoning, dependent origination, non-reification, coherent transport, exact presentations, obstruction and universal properties. It is **not** a replacement for an LLM's trained model weights, and a formal result does not by itself certify an AI application.

> 文脈や表示を正当な方法で変えたとき、何が不変か。局所的な観測はいつ比較・貼り合わせ可能で、どこで障害に阻まれるか。

## 現在地 / Formal status — v5.101（2026-10-09 JST）

**Lean/mathlib 上で、元の actual-lift データに対する F3・F4 の両 swallowtail 法則、および両法則を保持する F5 の KuuOS coherent biadjunction carrier を証明・構成しました。**

| 到達点 | 確定した内容 | Lean 正本 |
| --- | --- | --- |
| 元の随伴的データ | actual-lift を保持する F、非 strict な G、元の η・ε、二つの triangle StrongTrans と可逆 modification | [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean)・[v5.58](formal/KUOS/DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.lean)・[v5.59](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.lean) |
| F1・F2 | 元の四セルと global Iso の component 一致、元の四セル族の modification naturality | [v5.86](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86.lean)・[v5.87](formal/KUOS/DependentOriginationForwardCanonicalNaturalityV5_87.lean) |
| **F3: forward swallowtail** | 元の four-cell に対する pointwise、canonical、global の法則を証明 | [v5.93](formal/KUOS/DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean) · [PR #2053](https://github.com/itakura-hidetoshi/KuuOS/pull/2053) |
| **F4: reverse swallowtail** | counit-centered の元の四セルを汎用四セルと同一視し、pointwise・modification naturality・元の v5.66 predicate を証明 | [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean) · [PR #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) |
| **F5: coherent biadjunction** | **同一の元データ**から、両 interchanger と F3・F4 の証明を含む `Generic.CoherentBiadjunctionDatum` を構成 | [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) · [PR #2062](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |

v5.101 で実際に型検査された主要宣言は `Generic.CoherentBiadjunctionDatum`、`actualLiftCoherentBiadjunctionDatum`、`actualLiftCoherentBiadjunctionDatum_base`、`actualLiftCoherentBiadjunction_exists` です。構造体には、元の `IncoherentBiadjunctionDatum`、元の forward/reverse interchanger、およびそれぞれの **v5.65/v5.66 の predicate の証明**が格納されています。

**成立範囲の境界：**「coherent biadjunction」は **この KuuOS の型付き二つの swallowtail interface を満たす carrier** を意味します。任意の双圏に対する一律の存在、別定義の tricategorical adjunction との比較同値、無条件の普遍写像原理、AI runtime 全体の正しさまでを主張するものではありません。古い v5.57 の `CoherentBiequivalence` 名は互換性のため維持されており、F3/F4 の新しい証拠は v5.93 / v5.100 / v5.101 にあります。

## 正本と再現性 / Authority and reproducibility

| 対象 | 固定された証拠 |
| --- | --- |
| Repository / canonical branch | [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) · **main** |
| **v5.101 theorem-bearing merge** | `53e8ceaa3d50cb18c1e8278dc64b845f8b648896` — [PR #2062](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |
| v5.101 exact PR HEAD | `e01bb1776b7a2139504c27022541e495caebf8f8` |
| Exact-head CI | [Run 37928590324 — SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37928590324) |
| Strict Lean | Job **113813495613** · **8,727/8,727** SUCCESS · 変更対象 warning/error **0** |
| Governance / workflow integrity | Jobs **113823296377 / 113813495683** — SUCCESS |
| MCP Lean / MCP CI completion | Jobs **113823296498 / 113823358524** — SUCCESS |
| Printed proof axioms | v5.101 の対象宣言で `sorryAx` なし、新規公理なし |
| Lean | **leanprover/lean4:v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** — [lake-manifest.json](lake-manifest.json) |

この SHA は **文書更新前に確認した最新 theorem-bearing main** です。README/ROADMAP のみの後続マージによって main の SHA が進んでも、数学的基準点と証明内容を混同しません。CI は **選択した v5.101 ターゲットとその依存関係**を strict 設定で検証したもので、全 aggregate target・外部サービス・AI runtime の網羅的検証ではありません。

権威の順序：

~~~text
fresh exact canonical main SHA
  > その SHA に存在する Lean 宣言と証明
  > README / ROADMAP
  > 同じ head に対応した CI・Governance・MCP receipts
  > 過去の概要・会話上の継承情報
~~~

**隔離すべき検証 PR：** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は Lean 4.31 の **validation-only** lane です。**OPEN / DRAFT / 未マージ**を維持し、Ready for review・自動マージ・マージを行いません。v5.101 の theorem authority とは無関係です。

## 数学的構成 / Actual-lift formal core

固定する atlas とラベル：

~~~lean
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

~~~text
L = ExactLiftableClassificationObject     (actual-lift を保持する 1-cell)
E = ExactUniversalClassificationObject

F   : L -> E                              (元の strict projection)
G   : E -> L                              (非 strict な pseudofunctor)
η   : Id_L => F ; G                       (元の source unit)
ε   : G ; F => Id_E                       (元の target counit)

T_F : F => F                              (forward triangle)
T_G : G => G                              (reverse triangle)
C_F : T_F ~= Id_F                         (可逆 modification)
C_G : T_G ~= Id_G                         (可逆 modification)

Σ_F = 元の unit-centered forward interchanger
Σ_R = 元の counit-centered reverse interchanger
F3  : Σ_F = forwardTriangulatorPaste
F4  : Σ_R = reverseTriangulatorPaste
F5  : 同一の datum と Σ_F, Σ_R, F3, F4 の coherent carrier
~~~

ここで `;` は既存の pseudofunctor 合成に対応する記法です。対象 Y ごとに元の同値 `eY : F(GY) ≃ Y` を保ち、G の実際の lift は target 1-cell `k : Y → Z` に対して `(eY.hom ; k) ; eZ.inv` を保持します。**G.mapId・G.mapComp・associator・unitor と、異なる対象で選ばれた同値を勝手に同一視しません。**

F3 の帰着では元の forward four-cell と triangulator paste、F4 では元の `eps.naturality` と `ConjugationCounit.naturalityIso` の対応を示します。v5.100 の具体的な actual-lift 展開では、一般の双圏上で先に型付けした恒等セル補題を特殊化し、v5.99 の左三角恒等式を使用しました。F5 は新しい unit/counit や代替 interchanger を選び直していません。

過去の障害理論の到達点も維持します：

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

**逆は一般には成立しません。** 局所的な同値から任意の raw morphism の lift や、表現・履歴・provenance を消去した大域的不変性は導けません。

## 統合マイルストーン / Milestones

| 版 | 検証済みの主題 |
| --- | --- |
| v4.00–v4.48 | 非因子化、Stage-II obstruction、有限 carrier、再帰・逆極限・向き・descent |
| v4.49–v5.36 | exact-universal な分類、presentation-sensitive な localization、普遍化・実現・高次比較 |
| v5.37–v5.57 | actual-lift bicategory、元の F/G、unit/counit、両 triangle と可逆 modification |
| v5.58–v5.66 | native triangulator、incoherent datum、non-strict whiskering、F3/F4 の型付き predicate |
| v5.67–v5.87 | forward four-cell、非 strict な mapComp、global interchanger、whole-record naturality |
| v5.88–v5.93 | forward residual の還元と厳密な消去、**F3 成立** |
| v5.94–v5.99 | reverse target paste、元の counit 四セル、generic naturality と三角恒等式 |
| **v5.100** | **F4 成立**：元の actual-lift reverse pointwise・naturality・swallowtail |
| **v5.101** | **F5 成立**：元データと両 swallowtail を一つの coherent carrier に統合 |

各版の証明対象・PR・未解決境界については [ROADMAP.md](ROADMAP.md) に整理しています。

## 思考原則 / KuuOS reasoning route

空は「何も存在しない」という意味ではなく、観測・表示・推論を無条件の実体にしないという方法論です。実務上は次の順序を取ります。

1. 観測と推測を分離する。
2. 適用する文脈・権威・権限を特定する。
3. 複数の presentation を保持する。
4. 関係・履歴・出典・世界ラベルを追跡する。
5. 局所情報の compatibility を確認する。
6. transport / descent / gluing の正当性を判定する。
7. obstruction と適用できない境界を明示する。
8. 行為の authority とデータ使用権限を確認する。
9. 根拠のある最小限の行為を選ぶ。
10. 結果を再観測して判断を更新する。

この順序は研究・運用上の設計原則であり、LLM が常に正しく実装したことを保証する定理ではありません。

## 再現手順 / Selected Lean verification

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 53e8ceaa3d50cb18c1e8278dc64b845f8b648896

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true \
     build KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
~~~

必要な場合は F3・F4 を個別に確認できます。

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93 \
  KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100
~~~

全形式化や runtime の検証は、上記 receipt とは**別の範囲**です。

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

## 今後の研究と運用境界

F1–F5 の KuuOS 固有の証明課題は完了しています。次は (1) 別の tricategorical / biadjunction 定式化との**型付き比較定理**、(2) 異なる presentation をまたぐ追加の descent・普遍写像原理、(3) formal certificate と runtime・MCP・AI 対話の独立した統合テストが候補です。いずれも現時点で自動的に証明済み・運用保証済みとはみなしません。

## 著作権・引用 / Copyright and citation

**© 2026 Hidetoshi Itakura / 板倉英俊. All rights reserved.** 公開リポジトリであることは、転載・改変・二次利用・モデル学習・再配布・商用利用などの許諾を意味しません。閲覧・引用を超える利用は [LICENSE](LICENSE) および [COPYRIGHT.md](COPYRIGHT.md) に従ってください。

研究の記述には [CITATION.cff](CITATION.cff)、権限と運用ルールには [GOVERNANCE.md](GOVERNANCE.md)、今後の証明と実装の区別には [ROADMAP.md](ROADMAP.md) を参照してください。
