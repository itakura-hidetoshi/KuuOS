# KuuOS / 空OS — 数学的到達点と研究ROADMAP

> **2026-10-20 JST時点の確認記録。** canonical `main` の確認SHA：`a6f65142fef6324c6219867b6d5a0285a2b0004d`。F112研究親ブランチの確認SHA：`fdf1d281aa8af7caed488e5a2e41cd7c16140726`。SHAはこの日の観測値であり、将来の最新HEADを保証しません。現在値はそれぞれGitHubのbranch/PRで再観測してください。

## 権威と完了の定義

1. **正本はリポジトリ・ブランチ・exact commit SHAで識別する。** `main` は公開統合正本、[F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) の `formal/v5-293-f112-independent-total-change` はDraft・未マージの定理研究正本です。
2. **数学的な「証明済み」は実際のLean定理とその依存に限る。** `#print axioms` を確認し、`sorryAx`、新たな未証明公理、仮定のすり替えを許しません。CIのSUCCESSはexact-headに対応する検証の証拠ですが、定理の主張を拡張しません。
3. **公開rootと既存定理は保全する。** `main` の現行`lakefile.toml`には以前からの107公開rootがあり、標準入口は `KuuOSFormal` の一つです。`KuuOSStrict` は内部import集約であり、第2の数学体系ではありません。Gray固有の歴史的証明も元の型・仮定で保持しますが、新しい独立Kuuの前提にはしません。
4. **未マージの研究ブランチ上の結果はmainの成果と区別する。** 特定sourceが単独でstrict Leanビルドに成功していても、公開aggregateに取り込まれた、あるいは親PRがmainへ統合されたとは読み替えません。
5. **数学／runtime／権限を混同しない。** Lean形式化、Python等の回帰テスト、LLMとの接続、物理現象の実証、外部行為の承認は別の義務です。

## 到達点サマリー

| 領域 | 確認済み到達点 | 正本の場所 | 現在の扱い |
|---|---|---|---|
| Kuuの原始表示・普遍商 | 境界付き自由経路、指定交代の閉包、`project_exact`、適合観測の一意因子化、厳密2次比較、文脈切片・総圏 | [`formal/Kuu/`](formal/Kuu) | **main統合済み** |
| 五行・Qi v3.1 | `ZMod 5` の巡回群作用、相生+1／相剋+2、型付き自由関係経路と順序の非崩壊 | [Lean v3.1](formal/KUOS/Architecture/QiWuxingCyclicGroupPathsV3_1.lean) · [#2366](https://github.com/itakura-hidetoshi/KuuOS/pull/2366) | **main統合済み** |
| Qi v3.2 | 経路の位相変位・イベント数の合同を宣言した観測商、非忠実な観測例 | [Lean v3.2](formal/KUOS/Architecture/QiWuxingPathObservationCongruenceV3_2.lean) · [#2369](https://github.com/itakura-hidetoshi/KuuOS/pull/2369) | **main統合済み** |
| Qi v3.3 | 到達可能観測圏、full/non-faithfulな観測、商関手がfull・faithful・essentially surjectiveであることによる圏同値 | [Lean v3.3](formal/KUOS/Architecture/QiWuxingReachableObservationCategoryV3_3.lean) · [#2371](https://github.com/itakura-hidetoshi/KuuOS/pull/2371) | **main統合済み** |
| F112：真正なC60幾何・局所化 | 60 Dart・90 Edge・32 Polygon、360 flags、F69 zigzag／kernel quotient／局所化、F36/F40形状比較 | [親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) | **研究ブランチで形式化、main未マージ** |
| F112：整数係数チェイン | 真正`C₂ → C₁ → C₀`の符号付き境界、チェイン同型、`H₂ ≅ ℤ`、収縮による`H₁ = 0`・`H₀ ≅ ℤ`と非境界な根 | [P23–P25](https://github.com/itakura-hidetoshi/KuuOS/pull/2372) · [#2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) | **研究ブランチで形式化、main未マージ** |
| F112：高次の局所的非降下 | Propへの証明情報消去の非忠実性、F55偶／奇位相受け手で共通の電荷のみの復号器が存在しないこと | [P26 #2373](https://github.com/itakura-hidetoshi/KuuOS/pull/2373) | **研究ブランチで厳密検証、main未マージ** |
| CI高速化 | mainでの共有キャッシュ・重複CodeAIビルド抑制、F112の重複CIジョブ整理 | [#2376](https://github.com/itakura-hidetoshi/KuuOS/pull/2376)・[#2374](https://github.com/itakura-hidetoshi/KuuOS/pull/2374) | **各対象ブランチへ統合済み** |
| F112子PR向けキャッシュ | mainの共有依存キャッシュ＋親F112の検証済み小型`.lake/build`＋PR差分を段階復元する設計 | [#2375](https://github.com/itakura-hidetoshi/KuuOS/pull/2375) | **OPEN・検証／統合待ち** |

**注意：** `H₀/H₁/H₂` はここで構成した**整数係数セル複体**の結果です。これだけでは歴史的F55の3-Hom、F68の符号付き曲率、F77の位相情報、あるいは任意の高次descentの成立・不成立は導けません。

## A. 既に完了した独立基礎の切替（main）

**完了したこと**

- 古い公開rootを一括してビルドから除外する措置を撤回し、既存107 rootと現行`formal/KUOS/` の公開証明を復旧・維持。
- 空の原始定義を`Kuu.Presentation` の境界付き表示と**指定された交代**に置き、観測関手の等値性を原始商関係の代用にしない。
- `Kuu.Strict` の厳密な関手・自然変換比較、`Kuu.Incidence` の文脈依存の切片・総圏、指定なしの経路が崩壊しないテスト例を実装。
- mathlibをそのまま使い、独立KuuからGray/F51/F77の実依存を外す。`import Mathlib`の禁止や`KUOS.*`全体の禁止は行わない。
- Qi v3.1–v3.3を[canonical `KuuOSFormal`](formal/KuuOSFormal.lean) に統合。観測圏同値の成立と、元の履歴を忘れる非忠実性を同時に表現。

**維持する条件：** 旧証明の再承認を新しい研究の前提にしない。既存定理の名前・型・仮定・実証範囲の変更は、個別の変更内容とその厳密検証でのみ行う。

## B. F112独立移行：P1–P26の到達点と次の義務

[F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) は引き続きDraftです。[初期19段階移行の記録](https://github.com/itakura-hidetoshi/KuuOS/blob/fdf1d281aa8af7caed488e5a2e41cd7c16140726/docs/F112_INDEPENDENT_MIGRATION_LEDGER.md)は歴史的義務の整理として保持します。後続のP段階の進捗・確定SHAは、親PRとその子PR・exact-head CIを優先します。

| 段階 | 形式化されたこと | まだ主張できないこと |
|---|---|---|
| **P1–P8** | F42/F45的な独立の型付き履歴、F36/F40形状、真正C60の各種source・incidenceとの部分比較 | Prop化して消える生の証拠が可逆に戻せるという主張 |
| **P9–P16** | 真正な90辺・32面と辺境界、向き付き五角形／六角形境界、整数係数2サイクルと歴史的符号比較 | 歴史的3-Homの完全な型同型や全大域貼り合わせ |
| **P17–P23** | 独立型の整数セル`ChainComplex`、基本類`H₂ ≅ ℤ`、新旧`ChainComplex`同型と全H₂類の符号付き自然性 | 3次元の幾何・物理的なF68曲率の一致 |
| **P24** · [#2370](https://github.com/itakura-hidetoshi/KuuOS/pull/2370) | 全90辺チェインで`d₂Q + Pd₁ = id`、`im d₂ = ker d₁`、`H₁ = 0`、`H₀ ≅ ℤ` | 高次証明履歴の復元 |
| **P25** · [#2372](https://github.com/itakura-hidetoshi/KuuOS/pull/2372) | `d₁P₀ + ιε = id`、`ker ε = im d₁`、真正な北側Dartの非境界性 | 任意のF47 source functorとの同一性 |
| **P26** · [#2373](https://github.com/itakura-hidetoshi/KuuOS/pull/2373) | 実際のC60でF41のraw証拠をPropへ消去する際の非単射性に起因する述語の非降下、偶／奇のF55受け手に共通の電荷のみの位相復元が不可能 | 歴史的F55/F68/F77のグローバル障害を既に比較／解消したという主張 |

P26の新規ソースは[Lean 1294/1294・公理監査6/6・`sorryAx`なし](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/39409634477)で検証済みです。ただし、**`KuuOSStrict` からの通常import登録は別の未了作業**です。個別ソースのstrictビルド、標準aggregate統合、親PRのmainマージを3つの別の判定として扱います。

### B1. 優先：証明関連sourceの型付き比較

- 歴史的F42/F45/F54/F55と独立Kuuのraw constructorを、実際の始域・終域・境界・中間履歴に沿って比較する。
- Prop証拠への消去が非単射であることは**既に証明された障害**。失われた証明対象が逆写像だけで再生できるという偽の「同値」を作らず、必要に応じて**Type-valued witnessを保つ拡充された比較対象**を構成する。
- F47の真正な3-Homと、F54の回転・四境界・同一物理面を含む高次sourceを型付きで実現し、globularity・貼り合わせ・interchangeを必要な範囲で**定理として**証明する。交換法則を未証明の公理として追加しない。
- これが完成するまで、現在のF112局所移行を歴史的F112全19段階の完全移植と呼ばない。

### B2. 優先：非自明な位相・曲率・descentの比較

- P26のF55偶／奇受け手は、同じ符号付き電荷から位相が一意に強制されない**具体的な反例**です。どの追加の較正データ・対象・自然性が位相を指定するかを明示する。
- 歴史的F55 `Δ` 非lift、F77位相消失、F68の符号付き曲率（歴史的な北側−5、修正+5）と新しい独立source上の量は、**型に忠実な写像と自然性を証明した場合にのみ**比較する。
- 独立Kuuの普遍商の降下と、実際のF47 sourceにおける高次descentの有効性を区別する。`obstruction ≠ 0`なら矛盾を隠すために消去せず、具体的な障害として記録する。
- **完了条件：** 実際のC60境界に立脚する証明関連source、選択した較正の根拠、新旧観測の互換性、必要な高次貼り合わせ、非消滅時の明示的な障害定理が揃うこと。

### B3. P26の標準aggregate登録とF112親PRの統合

- 新規P26を独立基礎の標準import経路に載せる際、既存の107公開rootを除外しない。局所定理だけがGREENでも全import後の新HEADがGREENとは限らないため、**追加後の新しいexact-head検証**を行う。
- ビルド時間を理由に別の公開`KuuOSStrict`ライブラリや補助的な「厳密系」を権威化しない。Lakeの`+Module`個別ビルドは一つのパッケージにおける局所検証に過ぎない。
- 親PR #2339をmainに統合するのは、未移植の義務と正確な数学的主張が明示され、旧rootを含む統合チェック・必要な公理監査・Governanceが**その統合対象HEADで**揃った後に限る。未完成の高次主張を完成済みと書き換えて進めない。

## C. Qiの次の形式化

mainで完了したのは五行の**具体的な型付き経路・観測合同・到達可能観測圏との圏同値**です。

今後の論点：

1. イベント数や位相変位では区別できない**生成順序・局所履歴・文脈**を保存する観測器や比較を明示的に構成する。
2. 指定する交代関係・観測器・商・降下可能性の各条件を分離し、観測による同一視を、宣言のない原始経路の同一性と混同しない。
3. 五行モデルを他の物理・生物学的モデルに接続する場合は、写像、尺度、検証可能な意味、適用範囲を別途定義する。既存の巡回群表現の証明から実証的因果や臨床適用を自動的には導かない。

## D. CI・再現性・runtime接続

### CI：検証を削らずに再利用を増やす

- `main` に統合済みの[PR #2376](https://github.com/itakura-hidetoshi/KuuOS/pull/2376)では、巨大なLakeキャッシュの共通化、不要な再`lake update`／再`cache get`、CodeAIワークフロー群の重複した全体ビルドを抑制。個々のチェックとexact-head権限境界は保持する。
- F112研究ブランチにマージ済みの[PR #2374](https://github.com/itakura-hidetoshi/KuuOS/pull/2374)は、重複した独立Kuu専用PR実行を整理し、通常Governance検証と手動`workflow_dispatch`監査の区別を保つ。
- 追加の[PR #2375](https://github.com/itakura-hidetoshi/KuuOS/pull/2375)は**OPEN**。mainの共有依存キャッシュ、検証済みF112親ブランチ`.lake/build`、子PR固有の差分キャッシュの3層設計を、監査成功と実測によって評価する。想定短縮量を既得成果とは書かない。
- 低速・赤CIを修正するときは、エラー行だけでなく対象モジュール全文、import閉包、Lakeターゲット選択、キャッシュ経路、取消・タイムアウト、`#print axioms`と最終receiptを調べる。過去のRED/CANCELLEDを成功済みの再利用根拠にしない。

### 標準の再現手順

~~~bash
python3 scripts/run_kuu_foundation_check.py
lake exe cache get  # 必要なキャッシュが存在しない場合だけ
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

- Lean：`v4.30.0-rc2`、mathlib：`5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
- 固定`lean-toolchain`と`lake-manifest.json`をコミット単位で確認する。Lean 4.31用[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はvalidation-only・未マージ。
- `native_decide`や既存公理の利用歴は元の証明の監査対象として区別し、独立Kuuの新しい証明を曖昧な`sorry`・`admit`・新たな未検証公理で埋めない。確認するのは各定理の**実際の公理依存**である。
- 標準ターゲットと局所ビルドのどちらを使っても、元の公開rootをビルドから削除することや、`legacy/v5.291`を現行ソースの代替とすることは許さない。

### runtime・LLM統合に進むための条件

観測 → 文脈 → 複数の表示・推論経路 → transportと比較 → 整合時の貼り合わせ／不整合時のobstruction保持 → authority判定 → 行為または再観測、という手順を**研究上の設計**として保持します。

実際のruntimeへ進む場合は、独立Kuuの形式的状態、実行可能な推論手続き、LLM入出力、観測データ、権限・監査記録を区別して接続し、再現できるend-to-endのテストと必要な形式的性質を別途証明します。現時点で、すべてのLLM生成がKuuOSによって形式的に保証される、あるいは全OS・臨床判断が検証済みであるとは主張しません。

## 更新規則と参照先

READMEは[現在の利用可能範囲](README.md)を示し、このROADMAPは**証明済み／研究ブランチ上の検証済み／未証明／CI未確認**を区別します。exact-headの状況が変わったら、該当する定理・PR・CIの根拠を示して両方を更新します。

[親F112研究PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) · [P26 #2373](https://github.com/itakura-hidetoshi/KuuOS/pull/2373) · [F112詳細移行記録](https://github.com/itakura-hidetoshi/KuuOS/blob/fdf1d281aa8af7caed488e5a2e41cd7c16140726/docs/F112_INDEPENDENT_MIGRATION_LEDGER.md) · [旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) · [実装時の境界](AGENTS.md)

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
