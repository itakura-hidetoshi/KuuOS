# KuuOS / 空OS

**空・縁起・関係・文脈・presentationの交代可能性・高次圏論・obstruction-aware descent** を研究する数学体系、およびそのLean 4形式化・AI推論runtimeの研究です。

> **KuuOSの縁起の一般理論は、C60の導入以前から構築されてきました。C60から一般化を一から始めるのではありません。**
>
> 空は、異なる表示を無条件に同一視することでも、一つの数学的構造を「空そのもの」と固定することでもありません。数学・構成・観測・比較の方法自体も縁によって成立するという「空の空」を問い続けます。

English: KuuOS develops a general mathematical program for dependent origination, contextual transport, presentation localization, effective descent, higher coherence, and explicit obstructions. The later C60 geometry is a concrete testbed, **not the origin or unique model of the general theory**.

**研究・著作権者 / Founder and copyright holder:** 板倉英俊 / Hidetoshi Itakura. [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff).

## 研究の全体像：一般理論が先、C60は後から導入した検証の場

研究は二つの相互に照らし合う方向から進みます。

1. **既存の一般理論を継承・深化する。** C60以前からのcontext、transport、refinement、presentation-independent localization、sheaf/stack descent、bicategorical・simplicial coherence、operadicな複数条件、obstruction、普遍性、およびactual-lift / biadjunctionの形式的成果を、その原型・仮定・定理名のまま保持します。
2. **真正C60と独立Kuuで具体的に検証する。** 有限だが非自明な入射幾何・raw高次証拠・位相・曲率・非降下を使い、一般理論の仮定が実際に成立するか、何を失うか、どの厳密法則が障害に遭うかを調べます。独立Kuuはこの作業に便利な一つのpresentationであって、「唯一の空」ではありません。

~~~text
C60以前からの縁起の一般理論（v0 → v1 → v2 → v4/v5）
  context / transport / W-localization / J-descent / higher coherence
  universality / obstructions / biadjunction / proof-relevant paths
                      ⇅ 具体化・反例・比較・一般理論への反映
真正C60・独立Kuu（後から導入した有限幾何による検証）
  incidence / paths / raw 2・3-cell / quotient / phase / obstruction
                      ↓ 未証明部分を厳密に追究
非自明な証拠を保持する局所strict 3圏 → 大域strict 3圏 → strict n圏
                      ↓ 別途必要な比較・モデル化の証明
                 (∞,3)-hyperdescent
                      ↓ 適用範囲と仮定を明確に一般化
                  縁起の一般理論の深化
~~~

この図は**研究上の証明計画**であり、後半の矢印がすでにLeanで成立したという主張ではありません。一般理論はC60からしか得られないものではなく、C60の成果が一般理論へ逆向きに検証・修正を促します。

## C60以前に構築した縁起の一般理論（生きた定理群）

以下は新しい独立Kuuの前史として退けるものではなく、**現在も同じ公開Leanパッケージに属する数学的成果**です。それぞれのソースに明示された条件の範囲で扱います。

| 系列 | 数学的到達点と正確な範囲 | 代表的なLeanソース |
| --- | --- | --- |
| **v0–v1：縁起と関係のtransport** | Contextの圏、状態関手、合成に沿うtransport、不変readout、文脈的descent、複数条件のoperadic構成・高次比較の入口。物理的因果の実証は含まない。 | [FunctorialTransport v0.1](formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean) · [CoreSpine v1.7](formal/KUOS/DependentOriginationCoreSpineV1_7.lean) |
| **v1：nerve・scaled horn・homotopy** | Duskin nerveとhigher coherence。v1.33はhorn境界のhomotopyとstrict fillerを区別し、homotopyからstrict fillerへのrectificationを明示的な追加条件として切り分けた。 | [ScaledHornHomotopyDescent v1.33](formal/KUOS/DependentOriginationScaledHornHomotopyDescentV1_33.lean) |
| **v2.0：presentationの普遍性** | 許容する変更`W`の局所化`C[W⁻¹]`、`W`を同型へ送る関手の普遍的因子化、および同一普遍性を持つcarrier間の圏同値。`W`以外のすべての表示変更を自動的に反転するわけではない。 | [PresentationUniversality v2.0](formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean) |
| **v2.1–v2.7：descentとW+J分類** | Grothendieck topology `J`、sheafの局所大域条件、局所化後のsheafと元の適合する文脈系との**圏同値**。`H`まで含む最終完成を意味しない。 | [WJCategoryEquivalence v2.7](formal/KUOS/DependentOriginationWJCategoryEquivalenceV2_7.lean) |
| **v2.8–v2.13：Cat値stackと高次局所化** | Cat値擬関手の被覆に対する実効stack descent、precoverageの閉包条件下での特徴付け。厳密に`W`を反転する`C ⥤ Cat`に対する局所化の存在・一意性を証明。任意の弱い擬関手の普遍的高次局所化やhyperdescentは未証明。 | [HigherStackDescent v2.8](formal/KUOS/DependentOriginationHigherStackDescentV2_8.lean) · [StrictHigherUniversality v2.13](formal/KUOS/DependentOriginationStrictHigherUniversalityV2_13.lean) |
| **v4.00–v5.101：obstructionと高次普遍性** | 非因子化・局所化・明示的障害・exact-universal比較、実際の`F,G,η,ε`・triangulator・前後swallowtailを積み上げ、**同じoriginal actual-lift datum**上でcoherent biadjunction carrierを構成。一般のstrict 3圏を完成させたわけではない。 | [CoherentBiadjunctionActualLift v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) |
| **v5.102–v5.153：高次の具体的証明構文** | mates、二軸のType値履歴・交換類・完全normal form、任意有限長の回転木、五角形・正方形3-cell提示。**raw証拠を観測商へ写すと非忠実になる**実際の反例と復元不可能性を証明。 | [F55 raw cells](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean) · [F56 observation nonfaithfulness](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean) |

これらは**縁起の一般化がC60以前から実際に進んでいた証拠**です。「C60でstrict 3圏を証明してから初めて一般理論に着手する」という順序にはしません。一方、それぞれをそのまま厳密な大域3圏や`(∞,3)`-hyperdescentの完成証明とも呼びません。

歴史的な詳細・定理の成立範囲・原型を残した[旧README v5.291](docs/legacy/README-v5.291.md)と[旧ROADMAP v5.291](docs/legacy/ROADMAP-v5.291.md)も参照してください。**歴史的定理は`formal/KUOS/`の現行ソースでも生きています。`legacy/`への隔離・一括廃止ではありません。**

## 空の空・presentation・Grayの位置づけ

- **どのpresentationも空そのものではありません。** 古いF94/F95の荷電と位相を伴う商、現在の独立Kuu商、Qiの経路観測合同、C60のraw証拠も、それぞれ特定の関係と観測に相対的です。異なる表示が交換可能なら保存量と比較写像を証明し、交換できないなら差異とobstructionを保持します。
- **Gray圏をstrict 3圏の代替にしません。** Gray圏が与える弱いinterchange/coherenceは、KuuOSが次に要求するstrictな3次元合成律・交換律を証明したことにはなりません。研究上のstrict 3圏目標を「Gray圏ならできる」と弱めて完了扱いしません。
- **過去のGray・bicategoricalな数学を消しません。** 既存の証明は元の型と仮定のまま保存・利用します。ただし独立Kuuの原始構成や、これからのstrict 3/n圏の証明根拠としてGray固有の公理を密輸入しません。
- **strict 3圏の証明も空の唯一性の証明ではありません。** それは現在の研究経路に設定した不可欠な数学的到達目標です。成立を証明できなければ不足条件・no-go・非零obstructionをそのまま提示し、証拠を消す商や法則のすり替えで解決済みにしません。
- **mathlibを積極的に使用します。** 高次圏・局所化・sheaf・simplicial/homotopy・代数的トポロジーなどの定理を再利用します。Gray非依存とmathlib非依存は無関係です。

## 現在のC60・独立Kuu実験とstrict 3圏の未解決境界

C60では元の正二十面体に由来する**60 Dart、90 Edge、32 Polygon（12五角形・20六角形）、360 incidence flags**を用います。この有限幾何は、以前に構築した高次理論を**具体的・真正な境界と証拠のもとで試験する場**です。

- [`Kuu.Presentation`](formal/Kuu/Presentation.lean)：選ばれた境界付き自由経路と明示的な関係に相対的な商、核、観測関手の因子化。
- [`Kuu.Strict`](formal/Kuu/Strict.lean)：関手・自然変換の結合律、単位律、2次元のstrict interchange。**これはglobal proof-relevant strict 3圏の証明ではありません。**
- [`Kuu.Incidence`](formal/Kuu/Incidence.lean)：文脈に沿う切片図式とGrothendieck総圏。
- [F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)：Grayを原始基礎としない真正C60のF42/F54/F55、局所化、型付き高次証拠の移行。**MERGED：現在はmainに統合済み**。
- [F112-P56 #2418](https://github.com/itakura-hidetoshi/KuuOS/pull/2418)–[P57 #2420](https://github.com/itakura-hidetoshi/KuuOS/pull/2420)：独立F55九生成子のraw輸送、水平自然性、selected shadowのfaithfulnessと失われるraw情報を区別。
- [F112-P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421)：raw F55構文はそのままでは**strictな左右単位律・結合律を満たさない**ことをnode-countで証明。mathlibの自由経路圏を別途構成。
- [F112-P59 #2423](https://github.com/itakura-hidetoshi/KuuOS/pull/2423)、[P60 #2424](https://github.com/itakura-hidetoshi/KuuOS/pull/2424)・[#2425](https://github.com/itakura-hidetoshi/KuuOS/pull/2425)、[修復 #2428](https://github.com/itakura-hidetoshi/KuuOS/pull/2428)：垂直raw単位・合成を自由経路の空経路・連結へ正規化し、残る７種を証明依存生成辺として保持。自由経路の正規化関手と選択されたshadow観測への因子化を証明。数値観測からraw履歴は一般には復元できない。
- [F112-P61 #2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426)：垂直正規化された水平合成は２辺の経路。２つのraw単位セルを水平合成しても空経路にはならないという**限定された水平単位律obstruction**を示す。大域strict 3圏の不可能性ではない。
- [F112-P62 #2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429)：９構成子を再帰的に検査した**単位生成raw構文**だけを対象に、型付き自由経路合同関係を生成。垂直経路合成との整合性と選択されたshadowへの健全性を証明し、P61の水平単位経路と空経路がこの関係で結ばれることを証明。真正C60の五角形・六角形生成元は単位構文から除外。**水平合成の全関手性・交換律・大域strict 3圏はなお未証明。**
- [F112-P63 #2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431)：９構成子の再帰から`unitOnly`のF54始終点が同一であることを証明。mathlibの`Paths.lift`で左右contextの**証明依存raw自由経路関手**を構成し、垂直合成と単位生成構文の保存、context付きraw単位とstrict単位のP62関係を証明。raw生成履歴は消去しない。
- [F112-P64 #2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432)：P62の明示的な型付き合同関係をmathlibの`Congruence`・`CategoryTheory.Quotient`で**実際の垂直商圏**として構成。商圏の射の等号とP62関係の必要十分性、P61水平単位の商圏上の単位等式、選択されたshadow観測の因子化、raw生成元の観測量保存を証明。**選択shadowと一致するraw証明項を一括同一視する商ではない。**
- [F112-P65 #2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434)：P59によって**単一の生成辺として残る**unit-only raw証明セルを明示的に区別し、真正C60の証明履歴を保持する型付きunit wordを構成。P62関係の全５規則がP63の左右context関手で保存されることを証明し、mathlib `CategoryTheory.Quotient.lift`によりP64の最小商圏へ**左右２つの関手を実際に降下**させた。商関手との等式を双方で証明。raw `ident`生成辺全体の無条件消去やshadow値による同一視は行わない。
- [F112-P66 #2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436)：P64の単位生成合同商は**3射の射集合に作用し、F54の経路対象を同一視しない**ことを一般の２軸Nat深さで証明。実C60六角形の左右順序の異なるF54回転経路は商圏上でも異なる対象であり、それらを結ぶ真正F55交換正方形3射は残存する。選択されたshadowの交換位相`1 : ZMod 2`も非零のまま保存。これはP62〜P65だけから**厳密なinterchange等式を導けない**という現在のpresentationの具体的障害であり、一般的strict 3圏の不可能性定理ではない。

**次の数学的関門はP67以降のF54経路比較・水平双関手性です。** P65では商圏への左右context降下、P66では真正C60の異なる回転順序がP64の経路対象として区別され、非自明な交換正方形3射が存続することを証明しました。したがって、strict interchangeには、3射の単位合同関係とは別に、**F54経路対象間の適切な比較・必要条件・合法な型付き関係**が必要です。その同一視で失う原履歴・非零位相を明示するまでは、２変数の水平合成・全結合律・interchangeの完成を主張しません。大域strict 3/n圏とhyperdescentは引き続き未証明です。

## 五行・Qiも別の具体的presentation

mainで統合済みのQi v3.1–v3.3では`FivePhase = ZMod 5`を用い、相生を`+1`、相剋を`+2`の作用として表現します。同じ到達位相と同じ生成履歴は同一ではありません。

[Qi v3.1 #2366](https://github.com/itakura-hidetoshi/KuuOS/pull/2366)は忠実な巡回作用と型付き自由経路、[v3.2 #2369](https://github.com/itakura-hidetoshi/KuuOS/pull/2369)は明示した観測合同、[v3.3 #2371](https://github.com/itakura-hidetoshi/KuuOS/pull/2371)は到達可能観測圏との圏同値を証明します。観測合同が元の全履歴を回復するとは言いません。五行群論は臨床・物理現象の因果的実証と混同しません。

## これからの証明目標：strict 3/n圏から(∞,3)-hyperdescentへ

1. **一般理論の継承と照合：** 上記の`W/J/H`、普遍性、stack、scaled-horn、obstruction、actual-liftの定理を保持し、strict化に必要な強化・比較条件を洗い出す。
2. **局所strict 3圏：** 真正C60を含む具体例および一般的な文脈ソースに対して、証明関連3射のデータと厳密なinterchangeを形式化する。raw自由構文・path envelope・選択した商を混同しない。
3. **大域strict 3圏、strict n圏：** 真正なoverlap上のtransport、制限、三重以上の整合、gluingと高次結合律を証明し、globular strict n構造へ拡張する。C60上の証明を他の文脈に無条件には外挿しない。
4. **`(∞,3)`への橋：** strict n圏の列が自動的に一般の`(∞,3)`圏になるとは仮定しない。4射以上の可逆性、coherentな比較、使用モデルでの普遍性を別途証明する。
5. **hyperdescent：** 適切な高次値`F`とhypercover `U• → U`に対して`F(U) ≃ holim F(U•)`を証明する。普通のsheaf/stack・有限Čech descentを言い換えるだけでは不十分。
6. **一般化と空の空：** 文脈・被覆・presentationを変えた際にどの定理が保存されるか、どの障害が残るかを分類する。完成した構造も絶対的な「空」として実体化しない。

より詳しい証明義務・完了条件は[ROADMAP](ROADMAP.md)を参照してください。

## 正本、ビルド、検証

- **公開統合正本：** [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。[F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)はMERGED。2026-10-22 JST、P65 [#2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434)（9673/9673）に続き、P66 [#2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436)もexact-head Governance SUCCESS・Lean **9674/9674**・P66公理監査7宣言に`sorryAx`なし・completion receipts 2/2 SUCCESSを確認してsquash MERGED。P66統合SHA：`d41cfe8d24f430d9ae2dba49bceea1b834e7faaa`。以後のHEADはGitHubで再確認します。
- **唯一の通常ビルド入口：** `lake build` = `lake build KuuOSFormal`。既存**107公開root**と独立Kuu・Qiを一つのパッケージで保持。`KuuOSStrict`は内部import集約で、独立した権威や「唯一の空」ではありません。
- **ツールチェーン：** Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。PR #1558（Lean 4.31）はvalidation-only・未マージ。
- **証明の判定：** 実際のLean宣言とその型・仮定、`#print axioms`、対象commitのexact-head CIを根拠とします。`sorryAx`、`sorry`、`admit`や未証明の新公理で目標を埋めません。歴史的なmathlib/finite `native_decide`依存は正確に区別します。
- **CI高速化：** 共有cache、差分モジュールの部分ビルド、不要な重複実行の削減は可。ただし旧公開rootの削除や証明義務の弱化で高速化しません。

~~~bash
python3 scripts/run_kuu_foundation_check.py
lake exe cache get  # 初回・必要なキャッシュがないときだけ
lake build KuuOSFormal # warningAsErrorはlakefile.tomlで既定設定。sorryAxは#print axiomsで監査。
~~~

AI推論runtimeの方向は **観測 → 文脈・複数presentation → 輸送と2/3-cell比較 → 整合する場合のdescent/glue、しない場合のobstruction保持 → 権限確認 → 行為または再観測** です。この推論設計も実行保証・臨床的実証・全LLM出力の形式的正しさとは区別します。

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
