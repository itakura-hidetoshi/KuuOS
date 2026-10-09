# KuuOS / 空OS — Formal Roadmap

**更新基準：2026-10-09 JST · theorem-bearing v5.101 · [PR #2062 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2062)**

**確定した現在地：** KuuOS の original actual-lift に対して、F1（global / canonical component 比較）、F2（forward naturality）、**F3（forward swallowtail）**、**F4（reverse swallowtail）**、**F5（両方の法則を含む `CoherentBiadjunctionDatum` の構成）**は証明済みです。以前の「F4・F5 は open」という記述は **v5.100–v5.101 の統合によって解消**されました。

この文書は数学的な **Lean 証明・証明環境・適用境界・今後の課題**を分離した ledger です。実装名の `coherent` は当該 KuuOS の型付き interface に関するものであり、すべての tricategorical 定義や AI runtime の安全性・正確性を一括して証明する意味ではありません。

## 0. Canonical authority / 正本と検証 receipt

| 項目 | 正本・receipt |
| --- | --- |
| Repository / branch | [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) / **main** |
| 最終 theorem-bearing merge（文書更新前） | **`53e8ceaa3d50cb18c1e8278dc64b845f8b648896`** |
| F3 | [v5.93 · PR #2053 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2053) |
| F4 | [v5.100 · PR #2061 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) |
| F5 | [v5.101 · PR #2062 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |
| v5.101 validated PR HEAD | **`e01bb1776b7a2139504c27022541e495caebf8f8`** |
| Exact-head workflow | [37928590324 — completed / success](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37928590324) |
| Strict Lean | Job **113813495613** · **8,727/8,727** SUCCESS |
| 変更ファイル diagnostics | warning **0** / error **0** |
| Workflow consolidation / Governance | **113813495683 / 113823296377** SUCCESS |
| MCP Lean / MCP CI receipts | **113823296498 / 113823358524** SUCCESS |
| `#print axioms` | v5.101 の4宣言に **`sorryAx` なし**。新規公理・`sorry`・`admit` なし |
| Lean / mathlib | **v4.30.0-rc2** / **5450b53e5ddc75d46418fabb605edbf36bd0beb6** |

Exact-head CI は選択した `KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101` と必要な依存関係を検証しました。**リポジトリ全ターゲットや runtime テストをその receipt で検証したわけではありません。**

Authority order:

~~~text
fresh exact main SHA
  > 該当 SHA の形式 Lean 宣言・型・証明
  > README / ROADMAP
  > same-head strict CI・Governance・MCP receipts
  > 歴史的サマリー・過去の会話
~~~

後続の **docs-only merge は canonical main の SHA を進めますが、theorem-bearing baseline を自動的には変更しません。**

**独立検証 lane：** [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は Lean 4.31 validation-only。**OPEN / DRAFT / 未マージ**を維持します。Ready 化・auto-merge・merge は禁止。現在の pinned v5.101 数学的正本とは分離します。

## 1. Mathematical scope / 原データと何を証明したか

対象は同じ atlas と明示した二種類のラベル上の actual-lift 分類です。

~~~lean
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

~~~text
L := ExactLiftableClassificationObject
E := ExactUniversalClassificationObject

F   : L -> E                元の strict forward projection
G   : E -> L                元の non-strict quasi-inverse
η   : Id_L => F ; G
ε   : G ; F => Id_E

T_F : F => F                forward triangulator
T_G : G => G                reverse triangulator
C_F : T_F ~= Id_F           invertible modification
C_G : T_G ~= Id_G           invertible modification
~~~

`IncoherentBiadjunctionDatum` は、元の Whitehead/unit/counit certificate と上記の二つの native triangulator をまとめたものです（[v5.59](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.lean)）。ここでは **まだ** swallowtail の証明フィールドを持ちません。

~~~text
Σ_F : ForwardSwallowtailInterchanger datum
Σ_R : ReverseSwallowtailInterchanger datum

F3 : ForwardSwallowtailPredicate datum Σ_F
F4 : ReverseSwallowtailPredicate datum Σ_R

F5 : CoherentBiadjunctionDatum L E
     = {datum, Σ_F, Σ_R, F3, F4}
~~~

- **Σ_F** は original v5.68 four-cell の自然性を証明して得られた v5.87 canonical Iso。
- **Σ_R** は original v5.95 counit-centered 四セルの naturality から v5.96 の constructor で作った Iso。
- 両者の等式は v5.65/v5.66 で定義した **元の predicate**。単に新しい Iso を triangulator paste と定義して等式を自明化していません。
- 対象 Y の chosen equivalence **eY : F(GY) ≃ Y**、transport `(eY.hom ; k) ; eZ.inv`、非 strict な G の `mapId`・`mapComp` と元の unit/counit を保持します。
- `actualLiftCoherentBiadjunctionDatum_base` はこのベースが元の v5.59 の datum と **定義上等しい**ことを示します。

**射程の限界：** これは **KuuOS が指定した双圏・元の actual-lift と二つの swallowtail interface の coherent carrier の存在**です。別の tricategory の普遍的な biadjunction 定義への翻訳・比較、任意の context に関する無条件の存在定理、全ての presentation を消去する descent や汎用的な自然変換計算を主張しません。

## 2. Status ledger — F1–F5

| 義務 | ステータス | 実際の証明・内容 |
| --- | --- | --- |
| **F1** | **CLOSED v5.86** | `actualLiftGlobalCanonicalComponentAgreement`：v5.83 global Iso の component と元の v5.68 four-cell が一致 |
| **F2** | **CLOSED v5.87** | `actualLiftForwardSwallowtailOriginalNaturality` と元の canonical Iso = global Iso |
| **F3** | **CLOSED v5.93** | `actualLiftForwardSwallowtailPointwise`、`actualLiftForwardSwallowtail`、`actualLiftForwardGlobalSwallowtail` |
| **F4** | **CLOSED v5.100** | `actualLiftReverseFourCell_hom_eq_generic`、`actualLiftReverseExpandedResidual`、`actualLiftReversePointwise`、`actualLiftReverseNaturality`、`actualLiftReverseSwallowtail` |
| **F5** | **CLOSED v5.101** | `Generic.CoherentBiadjunctionDatum`、`actualLiftCoherentBiadjunctionDatum`、`actualLiftCoherentBiadjunctionDatum_base`、`actualLiftCoherentBiadjunction_exists` |

F1/F2 の問題は pointwise な 2-cell 計算と **modification の whole-record naturality**を混同できないことでした。F3 と F4 は元の四セルを保持し、対応する triangulator paste との等式を証明しています。F5 は両者を**共通の** v5.59 datum に格納します。

## 3. Earlier foundations — obstruction, classification, actual lifts

| 版 | 継続して有効な成果 |
| --- | --- |
| v4.00–v4.12 | C₂ nonfactorization と `ZMod 2` 上の Stage-II 障害。自明な比較不可能性を具体化 |
| v4.13–v4.48 | Incidence/capacity obstruction、recursive/inverse-limit carrier、向き・descent・次元 |
| v4.49–v5.08 | presentation-sensitive な exact-universal 分類、局所化、高次制約、restriction universality |
| v5.09–v5.36 | ambient/label-sensitive 分類、Whitehead・unit/counit・triangle、exact-liftability と presentation witnesses |
| v5.37–v5.42 | actual-lift を保存した 1-cell、source bicategory L、forward F |
| v5.43–v5.48 | hom equivalence、固定 eY、非 strict な G と元の比較セル |
| v5.49–v5.57 | η・ε、forward/reverse triangle、両方の invertible modification、同一データの統合 certificate |

正の含意は一方向です。

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

**一般に逆は偽です。** raw morphism の任意の lift、互いに独立した presentation choice の同一視、根拠のない global descent は追加仮定なしに成立しません。

**歴史的な名前について：** v5.57 の `CoherentBiequivalence` certificate は両 triangle までのデータを保持します。そのファイルが当時すでに F3/F4 を証明していた、という意味ではありません。高次 swallowtail の証拠は v5.93、v5.100、v5.101 に分けて収められています。

## 4. Native triangulators and forward naturality — v5.58–v5.87

| 版 | 数学的接続 |
| --- | --- |
| v5.58–v5.60 | native triangulator pair、incoherent datum、水平合成の下での構造保持 |
| v5.61–v5.63 | StrongTrans の pre-/postcomposition、非 strict な `H.mapId` / `H.mapComp` を保つ correction |
| [v5.64](formal/KUOS/DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.lean) | source/target での horizontal triangulator paste |
| [v5.65](formal/KUOS/DependentOriginationForwardSwallowtailPredicateV5_65.lean)・[v5.66](formal/KUOS/DependentOriginationReverseSwallowtailPredicateV5_66.lean) | forward / reverse の正確な型付き swallowtail predicate を定義（**当時**は証明なし） |
| v5.67–v5.70 | η self-naturality、元の forward four-cell、modification naturality の型付き障害 |
| v5.71–v5.78 | global unit / counit whiskering、reassociation、元の `G.mapComp` 因子 |
| v5.79–v5.82 | middle StrongTrans の objectwise と naturality の違いを解消 |
| v5.83–v5.85 | global invertible forward Iso、eqToIso transport、五段階の component 計算 |
| **v5.86** | 全五段の v5.83 global Iso と v5.68 original interchanger の pointwise 同一視 |
| **v5.87** | 元の forward four-cell naturality、canonical `isoMk` と global Iso の一致 |

v5.83 の global forward interchanger は、v5.78 の mapComp 因子と v5.77 の reassociated counit 因子を、証明済みの三つの endpoint/middle equality transport によって接続しています。**v5.86 は component の一致、v5.87 は modification naturality の一致を証明**しました。どちらもその時点では F3 の swallowtail そのものではありませんでした。

## 5. F3 complete — original forward swallowtail (v5.88–v5.93)

| 版・PR | 役割 |
| --- | --- |
| [v5.88 / #2047](https://github.com/itakura-hidetoshi/KuuOS/pull/2047) | v5.65 forward predicate を元の四セル = source triangulator paste へ iff 帰着 |
| [v5.89 / #2049](https://github.com/itakura-hidetoshi/KuuOS/pull/2049) | 元の contraction と G.mapId を展開 |
| [v5.90 / #2050](https://github.com/itakura-hidetoshi/KuuOS/pull/2050) | exact residual を分離 |
| [v5.91 / #2051](https://github.com/itakura-hidetoshi/KuuOS/pull/2051) | reverse contraction を既存 Iso 法則で消去 |
| [v5.92 / #2052](https://github.com/itakura-hidetoshi/KuuOS/pull/2052) | 選ばれた二つの**異なる**随伴同値について generic four-cell / triangle coherence |
| **[v5.93 / #2053](https://github.com/itakura-hidetoshi/KuuOS/pull/2053)** | 元の actual-lift へ特殊化し、pointwise・canonical・global forward predicate を証明 |

定理正本：[DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean](formal/KUOS/DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean)。

~~~text
(original v5.68 four-cell).hom
  = (unit η) ◁ (original sourceHorizontalPaste).hom
~~~

これは単なる iff 簡約ではなく、**元のデータについて実際に証明した等式**です。

## 6. F4 complete — original reverse swallowtail (v5.94–v5.100)

| 版・PR | 成果（すべてマージ済み） |
| --- | --- |
| [v5.94 / #2054](https://github.com/itakura-hidetoshi/KuuOS/pull/2054) | [元の target triangulator paste の展開](formal/KUOS/DependentOriginationReverseSwallowtailTargetPasteExpansionV5_94.lean) |
| [v5.95 / #2056](https://github.com/itakura-hidetoshi/KuuOS/pull/2056) | [元の counit-centered reverse 四セルと可逆性](formal/KUOS/DependentOriginationReverseSwallowtailCounitFourCellV5_95.lean) |
| [v5.96 / #2057](https://github.com/itakura-hidetoshi/KuuOS/pull/2057) | [modification naturality・pointwise predicate・元の expanded residual](formal/KUOS/DependentOriginationReverseSwallowtailPointwiseBoundaryV5_96.lean) |
| [v5.97 / #2058](https://github.com/itakura-hidetoshi/KuuOS/pull/2058) | [pointwise 成立から naturality が従うことの証明](formal/KUOS/DependentOriginationReverseSwallowtailSingleResidualV5_97.lean) |
| [v5.98 / #2059](https://github.com/itakura-hidetoshi/KuuOS/pull/2059) | [二つの異なる随伴同値 e, d に対する generic reverse four-cell](formal/KUOS/DependentOriginationReverseConjugationFourCellV5_98.lean) |
| [v5.99 / #2060](https://github.com/itakura-hidetoshi/KuuOS/pull/2060) | [左三角恒等式に基づく `reverseConjugationFourCell_cancelled` の証明](formal/KUOS/DependentOriginationReverseConjugationFourCellTriangleV5_99.lean) |
| **[v5.100 / #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061)** | **[actual-lift への特殊化と元の F4 predicate の証明](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean)** |

v5.100 で閉じた Lean 宣言：

- **`actualLiftReverseFourCell_hom_eq_generic`** — 元の四セル = 汎用 reverse four-cell。
- **`actualLiftReverseExpandedResidual`** — 元の `F.mapId` と triangle contraction を保持した residual。
- **`actualLiftReversePointwise`** — 元の reverse interchanger と target paste の pointwise 等式。
- **`actualLiftReverseNaturality`** — 元の四セル族から成る modification の自然性。
- **`actualLiftReverseSwallowtail`** — **v5.66 の元の global reverse predicate**。

証明方針は元の `eps.naturality` と `ConjugationCounit.naturalityIso` を対応づけ、strict F に属する `mapComp/mapId` の比較を**元の型に即して**消去し、非 strict G と二つの equivalence choice を保持するものです。恒等 2-cell の合成律は、複雑な actual-lift 展開後に `rfl` を強制するのではなく、**一般の bicategory 上で型付けして証明した補題を特殊化**しました。

[PR #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) の exact-head CI [37927797880](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37927797880)：**8,726/8,726 SUCCESS**、変更ファイル warning/error 0、`sorryAx` なし。マージ後の theorem-bearing SHA は `14dded7bc28949dba555769070fefbe6a805b550`。

## 7. F5 complete — common coherent biadjunction carrier (v5.101)

正本：[DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) · [PR #2062](https://github.com/itakura-hidetoshi/KuuOS/pull/2062)。

~~~text
Generic.CoherentBiadjunctionDatum B C
  datum                : IncoherentBiadjunctionDatum B C
  forwardInterchanger  : ForwardSwallowtailInterchanger datum
  reverseInterchanger  : ReverseSwallowtailInterchanger datum
  forward_swallowtail  : ForwardSwallowtailPredicate datum forwardInterchanger
  reverse_swallowtail  : ReverseSwallowtailPredicate datum reverseInterchanger
~~~

**実際の構成と証明：**

1. `actualLiftCoherentBiadjunctionDatum`：元の v5.59 datum、v5.87 の forward canonical Iso、v5.96 の reverse original Iso、および v5.93/v5.100 の双方の証明を格納。
2. `actualLiftCoherentBiadjunctionDatum_base`：格納された datum が元の v5.59 datum と **`rfl` で一致**することを証明。
3. `actualLiftCoherentBiadjunction_exists`：**この同一の actual-lift source/target に対する carrier の `Nonempty`** を証明。

この F5 は F3/F4 を別の抽象的なモデルに置き換えるのではなく、**元の随伴・両 triangulator と両元 interchanger を保存した状態で同時に成立させる**ことが中心です。KuuOS 内の F1–F5 はこれで CLOSED です。

v5.101 の exact-head strict CI [37928590324](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37928590324) は **8,727/8,727 SUCCESS**、対象変更ファイル warning/error 0、printed axioms に `sorryAx` なし。main への merge SHA は `53e8ceaa3d50cb18c1e8278dc64b845f8b648896`。

## 8. Beyond F5 — unproved or independently validated frontiers

F5 の完成は無条件に「すべての高次問題が解消した」という意味ではありません。今後の候補を**証明済みの F1–F5 と混ぜずに**記載します。

### A. 他の高次随伴定義との正確な比較

任意の tricategorical / biadjunction interface へ KuuOS の `CoherentBiadjunctionDatum` を移す場合には、その対象・1/2/3-cell・variance・associator / unitor・interchanger・coherence の定義を固定し、型付き比較と保存定理を新たに証明する必要があります。**F5 それ自体はその外部比較定理ではありません。**

### B. Universal mapping / presentation descent

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C, W, J, H), X)
~~~

この模式的な式は **無条件の一般定理ではありません**。source/target、適用する morphism class、presentation と labels、descent の compatibility、真正な actual-lift の存在条件を固定してください。

~~~text
fixed-presentation equivalence
  != coherent transport between presentations
  != valid descent/gluing
  != presentation-independent global invariant
~~~

Stage-II obstruction、finite carrier、inverse-limit と新しい F5 の接続は、証明すべき仮定を明示したうえで行います。

### C. AI・runtime・MCP と独立した検証

KuuOS の reasoning route（観測と推論の分離、文脈と出典の保持、compatibility、descent、obstruction、authority、最小限の行為、再観測）を retrieval・対話・操作に適用することは **実装と評価の課題**です。Lean が F5 を証明したことから、AI の推論全体や runtime、ウェブサイト、アクセス権限、臨床利用の安全性は自動的に導かれません。機能ごとに独立した受入条件・検証記録が必要です。

## 9. Lean / mathlib proof-engineering lessons

- **数学上の等式と definitional equality は異なる。** v5.100 では元の counit naturality と generic naturality の同一視に `rfl` を無理に使わない。
- **元のデータを保つ。** 特に G.mapId / G.mapComp、`eps.naturality`、元の `eY` / `e(FGY)`、associator/unitor と exact-lift の wrapper を strict 化しない。
- **Hom category を具体的に型付けする。** `Pseudofunctor.StrongTrans.homCategory` と Lean universe の順序を対応させる。
- **Pointwise と whole-record naturality を分離する。** v5.79–v5.82 と v5.96–v5.100 の教訓。
- **構造的な小補題を先に証明する。** 一般 bicategory 上で `Category.assoc`、`Category.comp_id`、`Category.id_comp`、whiskering の単位律、`Iso.ext` を適用し、その後 actual-lift に特殊化する。
- **`bicategory` tactic の適用条件を明示する。** 巨大な concrete wrapper から構造を自動推論させると失敗する場合がある。
- **結合方向と型を確認する。** `rw` が失敗したら 2-cell の括弧付け、right whiskering と middle identity の位置を先に確認する。
- **変更ファイル全文と依存 API を確認する。** `sorryAx` は未解決ゴールの伝播でも発生するため、型検査と `#print axioms` を両方確認する。warningAsError 下では未使用 simp 引数も修正対象。
- **CI は権威そのものではなく exact-head receipt。** merge と main SHA の fresh 再観測が必要。docs-only 更新による SHA と theorem-bearing SHA を区別する。

## 10. Reproduction, maintenance and rights

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 53e8ceaa3d50cb18c1e8278dc64b845f8b648896

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true \
     build KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
~~~

個別の forward/reverse 定理も検証できます。

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93 \
  KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100
~~~

全 formal aggregate と runtime は、別の validation scope です。

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

README/ROADMAP の文書変更は theorem-bearing result を再定義しません。後続 PR では **fresh main → actual Lean artifact → docs → exact-head CI** の順に照合し、追加の数学的主張がない docs-only commit を theorem-bearing と呼ばないでください。

**© 2026 板倉英俊 / Hidetoshi Itakura. All rights reserved.** 公開表示はコピー・再配布・改変・派生利用・モデル学習・商用利用の許諾ではありません。出典：[README.md](README.md)、[COPYRIGHT.md](COPYRIGHT.md)、[LICENSE](LICENSE)、[GOVERNANCE.md](GOVERNANCE.md)、[CITATION.cff](CITATION.cff)。
