# KuuOS / 空OS

**独立の空も、空を縁起から捉えた一つのプレゼンテーションでしかない。** KuuOSは、この一つの提示を含む、縁起・空・仮名・中道・空の空の問いを、表示・交代・観測・比較・降下・障害の構成と証明において探究する研究です。

> **状態基準：2026-10-20 JST。** 公開正本は `main`。F112の大規模な独立移行は別の[Draft親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)にあり、**mainへのマージは未了**です。以下では、mainに統合済みの定理、研究ブランチで検証済みの定理、未証明の義務を区別します。

## 縁起から捉えた空の、一つのプレゼンテーション

『中論』における縁起・空・仮名・中道を踏まえ、**独立Kuuは空を縁起から捉えた一つのプレゼンテーション**として構成します。Grayを使わない構成に移ったことは、空の唯一の定義や、空を支配する究極の形式を発見したことではありません。選ばれた対象・境界・表示経路・交代関係・観測・商・証明は、それぞれの条件と関係に依存します。**空を語るこの構成も、実体視の対象にしない**という問いは、型と関係をどう選び、何を同一視し、どの情報が失われ、何が他の提示へ運ばれずに残るかという数学的構成そのものに働きます。

- **独立の空も一つのプレゼンテーションです。** 現在の `Kuu.Presentation` は縁起から空を捉えるために選ばれた関係・表示に相対的な構成です。これを空そのものの唯一の姿とせず、別の提示への変換、比較可能な条件、比較できない場合の障害まで対象にします。
- **Grayに依存しないことは、新しい空を絶対化することではありません。** ここでの「独立」は、今の定理にGrayの特定の構造を必須条件として持ち込まないという意味です。Grayを用いる旧来の提示もその条件の下で扱い、独立Kuuをそれに代わる実体にしません。
- **普遍商の「普遍」は選ばれた条件に相対的です。** 指定したグラフ・平行経路・関係を尊重する関手の範囲での普遍性であり、空を一意に規定する無条件な普遍性ではありません。
- **Leanの定理も提示の条件と共に読みます。** 型・仮定を明示した証明の厳密性は維持しつつ、異なる提示へのtransport、成立するgluing、情報の忘却や非降下のobstructionを調べます。どの提示を採用したかという前提自体を忘れません。

参照する原典：龍樹『中論』観四諦品第二十四（縁起・空・仮名・中道）および観行品第十三（空を見解として執着することへの戒め）。

## まず知っておくこと

- **このリポジトリの既定ビルド入口は `lake build KuuOSFormal`。** `lake build` もこの既定ターゲットを用います。既存の**107個の公開root**と新しい独立Kuu／Qi成果は、同一のLeanパッケージに属します。`KuuOSStrict` は内部のimport集約です。既定入口が一つであるのはビルド管理上の取り決めであり、**空の唯一性を意味しません**。
- **現在選択している独立Kuuの形式化ではGrayを成立条件にしません。** ただしGrayを含む歴史的な定理の証明実績は元の型・仮定のまま保持し、`formal/KUOS/` の公開成果を消去・一括除外・無効扱いしません。`legacy/v5.291/` は履歴を再現するための保存版であり、現行の定理ソースを置き換えません。
- **mathlibを積極的に利用します。** Grayから独立することとmathlibを使わないことは無関係です。`import Mathlib` も個別のmathlib importも許されます。
- **CIのGREENが確かめる範囲を明示します。** 具体的なLean宣言、`#print axioms`、そのコミットのexact-head CIを証拠とし、未マージPRの証明をmainに存在する成果として記述しません。

## 選ばれた数学的提示：境界・関係・商

現行の一つのLeanモデルでは、**境界（始点・終点）を持つ表示経路**と、**平行な経路間に明示した交代関係**を原始データとして選びます。観測値が等しいことを原始的な経路の同一性とはせず、指定した関係の合成閉包・同値閉包から商を構成します。

~~~text
境界付き生成グラフ・型付き自由経路
               ↓
明示した交代関係とその合成／同値閉包
               ↓
指定した関係に相対的なKuu商（経路の区別と同一視）
               ↓
関手・自然変換、文脈切片、transport・比較
               ↓
整合すれば降下と貼り合わせ／整合しなければ障害を保持
~~~

中心となるLeanファイル：

| 層 | 実装・証明の範囲 |
|---|---|
| [`Kuu.Presentation`](formal/Kuu/Presentation.lean) | 自由経路、宣言された関係、商射影の核の正確な記述、文脈に沿う交代、適合する観測関手の一意因子化 |
| [`Kuu.Strict`](formal/Kuu/Strict.lean) | 関手・自然変換の単位と合成、交換則の厳密な計算、比較の降下 |
| [`Kuu.Incidence`](formal/Kuu/Incidence.lean) | 文脈圏上の切片図式、Grothendieck総圏、制限・合成の整合 |
| [`Kuu.Checks`](formal/Kuu/Checks.lean) | 指定した交代が成立する例と、指定していない平行経路が崩壊しない例 |

この構成は、**他の空の表現を排除する最終的な基礎ではありません**。また、非自明な証明関連3-cellを備えた大域ストリクト3圏、任意高次圏、あるいは完全な実行runtimeが成立したという主張でもありません。

## mainに統合済み：五行とQi v3.1–v3.3

五行は `FivePhase = ZMod 5` 上の巡回構造で扱います。「相生」と「相剋」を、それぞれ位相の +1、+2 の作用として表現します。ただし**同じ到達位相を持つことと、その生成経路が同一であることは異なります**。

| mainに存在する成果 | 具体的内容 | ソース |
|---|---|---|
| **Qi v3.1** · [PR #2366](https://github.com/itakura-hidetoshi/KuuOS/pull/2366) | 五相の忠実・推移的な巡回作用、生成・制御の型付き自由経路、制御1歩と生成2歩の非同一性、経路順序を忘れる観測の例 | [Lean](formal/KUOS/Architecture/QiWuxingCyclicGroupPathsV3_1.lean) |
| **Qi v3.2** · [PR #2369](https://github.com/itakura-hidetoshi/KuuOS/pull/2369) | 位相変位とイベント数の観測が等しいときに**明示的に宣言する**経路合同、正確な商、順序情報を失う非忠実性 | [Lean](formal/KUOS/Architecture/QiWuxingPathObservationCongruenceV3_2.lean) |
| **Qi v3.3** · [PR #2371](https://github.com/itakura-hidetoshi/KuuOS/pull/2371) | 到達可能なイベント数を射とする観測圏、fullだがfaithfulでない観測、誘導商関手のfull・faithful・essentially surjectiveと圏同値 | [Lean](formal/KUOS/Architecture/QiWuxingReachableObservationCategoryV3_3.lean) |

v3.3の結論は、**宣言した観測合同によるKuu商と、構成した到達可能観測圏との圏同値**です。すべての元の経路履歴が回復できるという結論ではありません。五行の数学モデルを物理的ゲージ場・生物学的効果・臨床判断の実証と混同しません。

## F112研究ブランチ：真正C60と高次証拠

[PR #2339 — 独立Kuu移行](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) は **OPEN / Draft / main未マージ**です。2026-10-20時点の研究ブランチ確認SHAは `fdf1d281aa8af7caed488e5a2e41cd7c16140726`。その下で検証した成果を、mainの成果とは区別して記載します。

| F112内の到達点 | 内容 |
|---|---|
| **真正な幾何・型付きソース** | 元の正二十面体から60個のDart、90本のEdge、32個のPolygon（12五角形・20六角形）を構成。真正なincidence、360個のvertex–edge–face flag、F69 zigzag・局所化と型付き経路の比較 |
| **F36/F40と歴史的境界の比較** | 新旧のコンストラクタ・形状、真正な面の向きと符号付き境界の対応を証明。歴史的な証拠のProp化によって失われる生のType情報は区別して保持 |
| **P17–P23** | 整数係数の真正C60チェイン複体を構築し、歴史的複体とのチェイン同型、基本2サイクル、`H₂ ≅ ℤ` と符号付き自然性を形式化 |
| **P24–P25** | 物理的な辺・面・根付き経路に基づく整数チェイン収縮：`H₀ ≅ ℤ`、`H₁ = 0`、`H₂ ≅ ℤ`。北側Dartの非境界性とaugmentationの核の同定 |
| **P26** · [PR #2373](https://github.com/itakura-hidetoshi/KuuOS/pull/2373) | 実際のC60 sourceで、F41の証明関連情報がProp証拠へ完全には降下しないこと、およびF55の同じ整数電荷に偶・奇の異なる位相較正を与えられることを証明 |

P26の独立した[Leanソース](https://github.com/itakura-hidetoshi/KuuOS/blob/fdf1d281aa8af7caed488e5a2e41cd7c16140726/formal/Kuu/F112/PolygonNativeHigherDescentObstructions.lean)は、exact-head CI [#39409634477](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/39409634477)でLean 1294/1294、6件の公理監査、`sorryAx`なしを確認しています。ただし**P26は研究ブランチ内の個別モジュールとして検証されており、`KuuOSStrict` の標準import集約への登録は別途必要**です。

**証明されていないこと：** 歴史的F47/F55の全proof-relevant 3-Homを新しいソースと完全同型にしたという結論、古いF68曲率・F77位相障害と新しい観測量の同一視、任意の大域3-descentの有効性。新しい局所非降下定理は、旧Gray理論の障害を自動的に輸送したものではありません。

## ビルドと検証

固定環境：**Lean `v4.30.0-rc2`**、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`（コミット済み`lake-manifest.json`）。Lean 4.31用[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)は検証専用・未マージです。

~~~bash
# 独立Kuuの依存境界、legacy保存、登録の回帰検査
python3 scripts/run_kuu_foundation_check.py

# 初回や必要なキャッシュが無い場合だけ実行
lake exe cache get

# 同一パッケージの標準入口（既存の公開証明も保持）
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

部分ビルドは開発効率のためのものです。例えばF112研究ブランチのP26を単独で検証するときは、Lakeの個別モジュールターゲット `lake build +Kuu.F112.PolygonNativeHigherDescentObstructions` を使用できます。**これは別の数学体系や公開rootの設置ではありません。**

CIはexact-headごとのLean検証、公理監査、独立基礎の依存境界、107公開rootの継承、legacy保存、Governanceを区別して監査します。[PR #2376](https://github.com/itakura-hidetoshi/KuuOS/pull/2376) のキャッシュ再利用・重複ビルド抑制はmainに統合済み。F112親ブランチへの追加の小型ビルドキャッシュ整備は[PR #2375](https://github.com/itakura-hidetoshi/KuuOS/pull/2375)で進行中であり、完了扱いしません。

## 推論・実行上の境界

研究上は、**観測 → 文脈に依存した複数の表示 → transport・比較 → 整合なら降下とglue／不整合ならobstructionを残す → 権限確認 → 行為または再観測**を一つの操作的手順として用います。この手順も固定の「空の定義」ではなく、具体的な文脈と結果に照らして組み替え可能な提示です。

この数学的指針は、現行のPython／各OS runtimeのすべての動作がLean4で正当化されたこと、LLMがKuuOS状態遷移を必ず通過する本番サービスが完成したこと、外部システムの操作が承認されたことを意味しません。既存runtimeの実装・テストと、その独立Kuu基礎による厳密な形式的保証を分離します。

## 研究計画と履歴

- [現在のROADMAP](ROADMAP.md)
- [F112独立移行の詳細記録](https://github.com/itakura-hidetoshi/KuuOS/blob/fdf1d281aa8af7caed488e5a2e41cd7c16140726/docs/F112_INDEPENDENT_MIGRATION_LEDGER.md)（初期の19段階移行表。後続のP段階についてはPR #2339を優先）
- [独立基礎の設計](docs/superpowers/specs/2026-10-16-independent-kuu-foundation-design.md)と[実装時の境界](AGENTS.md)
- [v5.291以前のREADME](docs/legacy/README-v5.291.md)・[ROADMAP](docs/legacy/ROADMAP-v5.291.md)

[LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff)

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
