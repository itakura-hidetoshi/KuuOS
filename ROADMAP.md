# KuuOS / 空OS — Formal Research Roadmap

**更新：2026-10-21 JST。研究史を訂正し、C60以前からの縁起の一般化を主軸に戻したロードマップ。**

> **一般理論 → C60による具体的検証 → 一般理論の改善・strict高次化 → (∞,3)-hyperdescent。**
> 
> C60は縁起の一般化の起点ではない。独立Kuuも一つのpresentationであり、strict 3圏を証明できたとしても唯一の「空」ではない。定理の型・仮定・obstructionを失わず、一般化の数学的根拠を段階的に増やす。

この文書は[README](README.md)を補い、**検証済みの一般的定理／後から導入したC60の個別定理／条件付きの帰結／未証明の到達目標**を分離します。過去の定理を「C60研究の前準備」として書き換えたり、Gray非依存化のために既存成果を廃止したりしません。

## 0. 正本・依存・証明の判定

| 区分 | 正確な位置づけ |
| --- | --- |
| 公開統合正本 | [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。歴史的`formal/KUOS/`と現行`formal/Kuu/`、Qiを**同一Leanパッケージ**に含む。 |
| 独立Kuu F112研究 | [Draft親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)、`formal/v5-293-f112-independent-total-change`。mainとは別の研究ブランチ。 |
| F112確認範囲 | 2026-10-21の観測では子PR [P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421)まで研究親に統合済み。最新のHEAD・CIは動くため、PR・コミットから再確認する。 |
| 既存定理の証拠 | 実際のLean宣言・型と仮定・`#print axioms`・対応するexact-head CI。`sorryAx`、`sorry`、`admit`、新たな未証明公理による補完は禁止。 |
| 数学的区別 | raw Type-valued証拠、Prop証明、選択した商、観測、物理的解釈は互いに無条件には同一視しない。 |
| 公開入口・toolchain | `lake build KuuOSFormal`（`lake build`も同じ）。既存107公開rootは維持。Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。 |
| 別レーン | PR #1558（Lean 4.31）はvalidation-only、Draft・未マージ。F112親PR #2339もDraftのまま扱う。 |

GitHub正本・Lean成果・README/ROADMAP・CI・歴史的スナップショットにはそれぞれ異なる役割があります。**ドキュメント編集は新しい数学的証明やF112のmain統合を意味しません。**

## 1. 最初から存在する一般理論を研究の幹として継承する

KuuOSの原初の問いは、C60の60頂点・90辺・32面ではなく、**関係や文脈の変化に沿う縁起、presentationを越える普遍性、局所大域整合性、障害、非実体化**です。これらの一般構成は後のC60以前から前進していました。

### 1.1 既存の形式的成果（C60を必要としない数学的骨格）

| 時系列 | 代表的な実装・証明 | 到達範囲／言い換えてはいけないこと |
| --- | --- | --- |
| v0–v1.7 | [FunctorialTransport v0.1](formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean)、[ContextualCore v1.0](formal/KUOS/DependentOriginationContextualCoreV1_0.lean)、[CoreSpine v1.7](formal/KUOS/DependentOriginationCoreSpineV1_7.lean) | 文脈圏上の状態の関手的transport、不変意味、refinementと2-cell、operadic複数入力。選択した構造の定理であり、任意の臨床・物理的因果の実証ではない。 |
| v1.21–v1.40 | [GlobalDuskinScaledNerve v1.21](formal/KUOS/DependentOriginationGlobalDuskinScaledNerveV1_21.lean)、[ScaledHornHomotopyDescent v1.33](formal/KUOS/DependentOriginationScaledHornHomotopyDescentV1_33.lean) | 高次simplicial比較、horn/homotopyとrectificationの厳密な分離。`horn homotopy`だけからstrict fillerを捏造しない。 |
| v2.0 | [PresentationUniversality v2.0](formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean) | `W`局所化の普遍因子化と普遍的carrier間の圏同値。`W`を同型へ送るという明示的な仮定が必要。 |
| v2.1–v2.7 | [WJCategoryEquivalence v2.7](formal/KUOS/DependentOriginationWJCategoryEquivalenceV2_7.lean) | `W`-invertingな文脈系の`J`-descentと局所化上のType値sheaf圏の同値。一般`H`は別課題。 |
| v2.8–v2.13 | [HigherStackDescent v2.8](formal/KUOS/DependentOriginationHigherStackDescentV2_8.lean)、[StrictHigherUniversality v2.13](formal/KUOS/DependentOriginationStrictHigherUniversalityV2_13.lean) | Cat値stackの被覆descentの同値判定と、強い`W.IsInvertedBy`下でのCat値局所化普遍性。任意弱擬関手の高次局所化や`(∞,3)`-hyperdescentまで証明したわけではない。 |
| v4.00–v5.36 | [旧ROADMAP `2](docs/legacy/ROADMAP-v5.291.md#2-obstruction-localization-and-exact-classification-foundations--v400v536) | 明示的な非因子化・capacity/incidence障害、presentation-sensitive descent、exact-universal分類、actual-liftへ進む一般的条件。結果の有効範囲は各Lean型に相対的。 |
| v5.37–v5.101 | [CoherentBiadjunctionActualLift v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) | 元の`F,G,η,ε`、前後triangulatorとswallowtailの両方を**同一original datum**で証明。これは任意のrawソースのstrict 3圏への自動的な昇格ではない。 |
| v5.102–v5.153 | [F44交換類 v5.141](formal/KUOS/DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.lean)、[F55高次cell v5.152](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean)、[F56非忠実性 v5.153](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean) | 選択した2軸のraw/quotient、有限高次証拠、normal form、異なるrawの観測像一致と非復元を証明。Gray的なweak合成をstrict 3圏の完成と読まない。 |

**重要な継承規則：** これらを再証明してからC60へ進む必要はありません。歴史的な証明の原型・依存・文脈を維持し、**新たなstrict 3/n圏に移すために必要な比較・保存定理だけ**を追加します。既存のGray/Bicategoryに依存する証明はその型で正当な歴史的成果ですが、将来のstrict 3圏の未証明公理を代行しません。

### 1.2 以前からの一般化の骨格

明示する文脈圏`C`、許容presentation変更`W`、被覆位相`J`、高次coherence`H`に対し、研究対象は概念的に

\[
\mathrm{DO}(C,W,J,H)
\]

です。`W`の局所化、`J`のsheaf/stack、`H`の高次比較は**それぞれ異なる義務**です。v2.0やv2.7に既証明の性質を、`H`全体やhyperdescentの無条件な存在へ飛躍させません。

また、空の空に従って`\mathrm{DO}`それ自体も唯一のpresentationにはしません。異なる`(C,W,J,H)`の間の輸送・同値・障害を研究対象に含めます。

## 2. C60という後発の具体的検証：成果と不足を明確化する

真正C60幾何は原正二十面体から導いた60 Dart、90 Edge、32 Polygon（12五角形・20六角形）、360入射flagsを持ちます。一般的に進めていた高次法則・descent・障害の議論を、**見せかけの任意の例ではなく、検証可能な有限物理的入射上で試す**ために選んだpresentationです。

| 具体的な到達段階 | 本当にある成果 | なお必要なもの |
| --- | --- | --- |
| 独立基礎`Kuu.Presentation`、`Kuu.Strict`、`Kuu.Incidence` | 選択した自由経路の指定関係商・観測因子化、functor/natural transformationの**strict 2次元法則**、文脈切片・総圏。 | 証明関連3射を保持した局所strict 3圏の全公理。 |
| F112 P1–P26 | 原幾何とF69 zigzag・局所化、整数chain/ホモロジー、raw証拠の非降下、別位相への非一意性を実際のC60に構成。 | 類似した観測結果から全raw高次証拠の復元を仮定しない。 |
| F112 P27–P53 | 研究親[PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)上で歴史的ソースの独立比較と真正面relatorの整理を継続。P53は全32原面relatorを用いる原F42面商→F69の無条件因子化に到達。 | 別presentationの原3-Hom全体を勝手に同型としない。 |
| F112 P54–P57 | [P55 #2417](https://github.com/itakura-hidetoshi/KuuOS/pull/2417)、[P56 #2418](https://github.com/itakura-hidetoshi/KuuOS/pull/2418)、[P57 #2419](https://github.com/itakura-hidetoshi/KuuOS/pull/2419)・[#2420](https://github.com/itakura-hidetoshi/KuuOS/pull/2420)：raw F55の九生成子、完全source transport、水平自然性、選んだshadowの忠実な圏関手、非復元と別位相のobstruction。 | chosen shadowが唯一の空であることや、raw 3-cellがすでにstrict 3圏であること。 |
| **F112 P58** [#2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421) | **全raw F55項について左右strict単位律がliteralには失敗し、全合成可能三項についてraw結合律の二括弧が区別される**ことを構文の数え上げで証明。Mathlibの独立した自由経路圏を構成。 | 自由経路圏が非自明な3-Homを保持する大域strict 3圏である、という未証明の飛躍。 |

P58の[実際のソース](formal/Kuu/F112/PolygonNativeF55RawStrictificationBoundary.lean)は**F112研究ブランチ**にあり、現段階でmainからの相対リンクではなく[研究親ブランチ](https://github.com/itakura-hidetoshi/KuuOS/tree/formal/v5-293-f112-independent-total-change/formal/Kuu/F112)から参照してください。上表のP段階は研究親内の成果であって、`main`に既に含まれるとは主張しません。

## 3. 最優先の新規数学：局所proof-relevant strict 3圏

**目標:** C60を一つの具体例として含み得る一般的な高次source`\mathcal K`に、globularな`0,1,2,3`射の型付き境界と合成を設け、**strict 3圏の全公理をLean4で証明**する。

必要な義務：

1. **境界とglobularity**：全射の`source/target`、2/3射の平行性、各方向の合成可能性を型で保証する。
2. **合成・単位・結合律**：`\circ_i`を定義し、すべての定義可能な段階でstrictな左右単位・結合の等式を証明する。元のraw語のliteralな等式とは混同しない。
3. **全interchange**：異なる`i<j`方向の合成について、弱いinterchanger 3射ではなく厳密な等式を証明する。Gray圏のcoherenceを証明の代用品にしない。
4. **非自明性・source情報**：raw証拠、原F54/F55履歴、位相・曲率・障害を失うか否かを**個別の保存/非保存定理**で記載する。単に全3射を同一視した圏ではこの研究目標を達成しない。
5. **最小の整合関係またはno-go**：P58で証明したraw law obstructionを出発点とし、どの明示した関係ならstrict化が成立するかを構成する。望む非自明な情報と両立しなければ、不可能性・必要条件・obstructionを定理として保持する。

**完了基準:** 本物の3-cellと全globular境界、合成・単位・結合・交換のLean定理、`#print axioms`、情報保存/損失定理、exact-head CI。**自由path 1圏を作っただけ、2次元のstrict interchangeだけ、Gray圏の可逆interchangerだけでは未完了**です。

## 4. 既存の一般的W/J/H定理とstrict 3圏の接続

局所strict 3圏を構成した後に初めて一般理論を「開始」するのではありません。すでにある一般的な`W/J/H`とstrict高次ソースの間に**比較の橋**を追加します。

- `W`を尊重する実際の高次source-change・localizationの存在と普遍性を示す。`W`-同値とraw同一性を区別する。
- `J`の被覆・refinementのもとで、2/3射を保つrestrictionとoverlap比較を構成する。既存のType値sheafやCat値stackの定理は、その**正確な範囲だけ**で再利用する。
- `H`には既存のbicategorical/scaled-horn・original actual-lift/swallowtailの定理を参照し、strict 3/n圏への比較が存在する場合にのみ移送する。すでに存在するweak-to-strict等価を仮定しない。
- あるpresentationで証明済みの法則が別のpresentationへ移る必要十分条件、あるいは明示的obstructionを求める。

**完了基準:** 少なくとも二つの具体的・異なるpresentation間に実際の型付き比較写像があり、既存の普遍性・降下条件について保存される範囲と失われる範囲がLeanで証明されていること。

## 5. 大域strict 3圏の構成：有限Čechから大域の証明へ

文脈site`(\mathcal C,J)`上の局所strict 3圏`\mathcal K_3(U)`と重なりへのrestrictionを与え、実際の大域対象を構成します。

1. 2つの局所表示のoverlap上の**sourceの証拠に忠実な比較**。同じ観測値だけでは原3射を同一視しない。
2. 三重以上のoverlapで、局所合成とtransportのstrict整合を証明。曲率・非零cocycleを消してしまう形式的な貼り合わせは禁止。
3. 局所データと大域データの比較`\mathcal K_3(U)\to Desc(\{U_i\})`について、対象だけでなく高次mapping層の完全性・忠実性・実効性を検証する。
4. 障害がある場合、exact obstruction class・補正の要否・補正を選んだ場合の非一意性を明示する。既存のC60曲率や非liftを一律にゼロと扱わない。

**完了基準:** 対象から3射までの大域的な厳密合成、cover/refinement下の制限、必要なdescent・glue定理、または正確なno-go。C60の有限ČechやCat値stackの結果の言い換えだけでは未完了です。

## 6. 大域strict n圏：nを変えても証明が保たれる構造

固定3次元での証明を出発点とし、任意有限`n≥3`に対するglobular `n`-categoryの定義、すべての方向の合成`\circ_i`、単位・結合・交換の帰納的な証明を目指します。

- 次元`n`で追加される境界・高次合成・交換を、先行次元の整合性と矛盾せず定義する。
- `n`に関する帰納法のstepで必要なcoherenceを**公理の単純な仮定ではなく**、構成・定理にする。
- 構成を特定のC60幾何へ閉じ込めず、選択した文脈、局所化、被覆、presentation変更に相対化する。
- strictnessのために非自明なsourceをすべて殺す構成は採用せず、保存量・反例・障害を報告する。

**完了基準:** 指定したソースの種類について`n`を自由に変えられるLean構造・合成定理・具体例との非退化な比較が存在すること。「3圏の定義を形式的に複製しただけ」では未完了。

## 7. (∞,3)-圏への比較：strict n圏からの飛躍を禁止する

一般の`(∞,3)`圏では4次以上の射は可逆です。strict n圏の列を作れば**そのまま一般の`(∞,3)`圏になる**とも、任意の弱い高次圏を完全strict化できるとも主張しません。

- 対象とモデル（例：適切な高次Segal/nerveモデル）を明確に選び、何を`(\infty,3)`-equivalenceと呼ぶか定義する。
- 0〜3次のstrictデータを保つ比較構成、4次以上の可逆/coherentデータの生成と整合性を明示する。
- モデル変更とpresentation変更の間でtransportされる情報、失われる情報、obstructionを証明する。
- 過去のDuskin/scaled-horn成果を再利用できる部分と、strict 3/nからは自動的に導けない部分を区別する。

**完了基準:** 選んだモデル内の`(\infty,3)`圏の証人と、strictソースに関する型付き比較・本質的性質のLean定理。Gray圏で代用しない。

## 8. (∞,3)-hyperdescent：最終的な新規証明目標

適切なsite`(\mathcal C,J)`と`(\infty,3)`圏値の文脈系`\mathcal F`を厳密に定義し、任意の対象`U`と対象とするhypercover`U_\bullet\to U`について、

\[
\boxed{\quad
\mathcal F(U)\;\simeq\;
\operatorname*{holim}_{[n]\in\Delta}\mathcal F(U_n)
\quad}
\]

を、使用する高次圏モデルの意味で証明することを目標とします。

必要な区別と義務：

- 普通の`W`局所化・`J`のsheaf・Cat値stack・有限Čech descentと、**hypercover全体に対する高次hyperdescent**は異なる。
- rootからdescent-dataへの比較が`(\infty,3)`-equivalenceであることを、対象側の実効性と高次mapping`(\infty,2)`の同値性の両方で確認する。
- hypercoverのrefinement、presentation変更、localizationに沿う不変性・比較・障害を示す。
- 必要な条件（site、hypercompleteness、modelの存在、局所glue条件等）を**仮定として明記**するか、実際の対象で証明する。条件を空の普遍法則として密輸入しない。

**完了基準:** 独立した`(\infty,3)`-hyperdescent定理、正確な全仮定、非自明なsource例、仮定を外した際の明確なobstructionまたは境界。単なる名前・interface・`sorry`のない公理化では未完了。

## 9. その先：縁起の一般化と「空の空」

この最終目標は、C60についてだけhyperdescentを成立させることではありません。任意に選択した一定のクラスの`(\mathcal C,W,J,H)`について**何が一般的に成立し、何が追加条件に依存し、何が不可能なのか**を証明することです。

- C60以外の文脈とpresentationsにも定理を移し、各適用範囲を明示する。
- 複数presentationの間のtransport/coherence/descentの比較定理を証明する。
- obstructionを消去せず、成立しない条件やnon-liftも一般化の一部として保持する。
- **独立Kuu、strict 3/n圏、`(\infty,3)`-hyperdescentそのものも一つの数学的presentationに相対的**という問いを研究から排除しない。「空の空」を特別な唯一の公理・固定対象に置き換えない。

この一連の数学的成果から中観の哲学全体の「証明」を自動的に結論しません。同時に、哲学的な問いと数学的構成を切り離してしまうのでもありません。

## 10. 実装優先順位、CI、既存成果の保存

**次の証明作業の優先順位:** F112-P58の**実際のraw strict-law obstruction** → 最小限で証拠を保つ厳密3次元合成候補・必要条件／no-go → 既存一般的W/J/H普遍性との比較 → 大域化 → 高次`n` → `(\infty,3)`モデル橋 → hyperdescent。並行してC60以前の一般理論の既存定理を使い続けます。

**絶対に行わないこと:** Gray圏でstrict 3圏の未証明法則を置換して完了と言うこと、旧約107公開rootの一括削除、歴史的な数学を`legacy/`だけに押し込むこと、strict性を得るために全raw証拠を無条件に潰すこと、未証明の存在条件を新公理へ置くこと、F112親PR #2339をmainに勝手にマージすること。

**証明と検証:** `formal/KuuOSFormal.lean`を通常の公開入口として維持。部分ビルドは同一パッケージの開発時の時間短縮だけです。対象ファイル全文・import閉包・mathlib定理・Lean形式の原因を調べ、正本コミットのexact-head CIと`#print axioms`を確認します。共有cacheと重複ジョブ削減を進めても、必要な公理監査・検証を抜きません。

~~~bash
python3 scripts/check_public_proof_roots.py
python3 scripts/run_kuu_foundation_check.py
lake exe cache get   # キャッシュが本当に不足する場合だけ
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

`KuuOSStrict`は内部import集約にすぎず、旧定理やmathlibを使わない特殊な「空の正本」ではありません。Lean4の証明／runtime／AI入出力／権限・行為／実証データはそれぞれ異なる保証範囲です。

## 11. 継承用の参照先

- [現行README](README.md) — 研究の目的・全体像・成果の入り口
- [旧README v5.291](docs/legacy/README-v5.291.md)、[旧ROADMAP v5.291](docs/legacy/ROADMAP-v5.291.md) — 長い一般的・歴史的証明台帳と原型
- [F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) — 現在の独立Kuu/C60作業正本（Draft、未マージ）
- [F112-P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421) — raw strict-law obstructionと別の自由path envelope
- [`AGENTS.md`](AGENTS.md) — 現行のpublic root・mathlib・Gray依存・ビルド境界
- [`formal/KUOS/`](formal/KUOS/) — 過去から継続する一般的なLean数学
- [`formal/Kuu/`](formal/Kuu/) — 現在の独立Kuuの具体的な構成

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
