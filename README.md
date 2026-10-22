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
- [F112-P67 #2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438)：真正F54のdisjoint-square比較を**Type値の証拠**として構成し、各比較証拠から元の型付きF55 raw 3-cellを復元。比較クラスの等号はこの証拠の`Nonempty`と同値であり、具体的証明履歴を選ぶ操作ではない。実C60の左先・右先回転順序が比較クラスで等しくなる一方、元のF54経路は異なり、**その同一視を行う任意の写像は単射になれない**ことを証明。選択された非零交換位相とraw証明履歴は別データとして保持。
- [F112-P68 #2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439)：全９構成子を再帰的に検査し、真正五角形生成元を含まない**squareOnly**なF55 raw証拠をType値で保持するcontext閉包比較を構成。P67比較クラスから新クラスへの写像、**左右F54 contextの商上の作用**と元の経路への正確な整合、実C60六角形の交換比較をLean4で証明。五角形生成元はsquareOnlyの原始生成元から除外。P67とP68が同値であることや全3-Homの輸送までは主張しない。
- [F112-P69 #2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441)：P68のF54比較クラスを始点・終点に持つ型付きF55高次射パッケージを構成。元の２つのF54代表経路と真正F55 raw 3-cellをType値で保持し、元の履歴保存と比較クラス等号から得られる比較証拠の存在を証明。**代表元の一意な選択・新しい高次圏の全合成は未証明。**
- [F112-P70 #2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442)：選択された真正squareOnly比較証拠による**両端代表元の輸送**と、中間比較証拠を指定した**高次射の合成**をType値raw F55構文で実装。選択shadowの加法公式を証明。実C60六角形では同じ商クラスを両端に持つ恒等3射（位相0）が交換正方形で輸送されると、元のraw証明項の位相が1に変化することを証明。**選択証拠に依存した合成を、代表元独立な全合成と混同しない。**
- [F112-P71 #2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444)：P70代表元変更から生成する高次射の輸送同値関係と商を構成し、商での等号の必要十分性を証明。輸送同値な元の高次射でraw shadowが異なれば、**元の数値shadowを全代表元で保つ商への因子化は不可能**という限定されたno-goを証明。真正C60の位相差と輸送同値を接続。ただし補正付き・gradedな高次Homは否定しない。
- [F112-P72 #2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446)：P70の**選択された真正比較証拠**による代表元輸送・中間経路のbridge合成で、元raw shadowに加わる成分を明示して補正。２段階の輸送で補正値が整合する加法cocycle公式と、真正C60交換正方形で補正前位相1・補正後位相0を証明。補正は証拠選択に依存し、P71無補正shadowの商への因子化ではない。
- [F112-P73 #2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447)：P68の`squareOnly`判定を全９raw構成子で帰納的に解析し、比較証拠の**五角形chargeが0**であることを証明。P70の左右代表元変更とbridge付き合成、P71輸送同値の全４生成規則で元の五角形整数chargeが保存されることを示し、P71商上の真正なcharge観測関数を構成。真正C60の非零交換位相とは独立に成立。
- [F112-P74 #2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448)：元の整数線形観測`a×五角形charge + b×交換charge`について、**元の交換chargeを1だけ変化させる輸送が存在する固定されたP71商では、全代表元と一致する無補正readoutが存在する必要十分条件は`b=0`**と証明。十分性はP73の五角形chargeから構成し、必要性は実際の輸送同値と加法性から導出。真正C60交換正方形で交換charge 0→1を確認。すべてのgraded高次観測を分類したとは主張しない。
- [F112-P75 #2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450)：P71の輸送４生成規則を**真正のType値graded輸送履歴**として持ち上げ、元F55 shadow全３座標（五角形整数・交換整数・奇偶位相）の加法gradeを保持。輸送履歴に対するshadow加法の健全性、固定raw両端でのgrade一意性、閉路grade0、Prop値P71輸送関係とgraded証拠の存在の必要十分性を証明。真正C60の交換正方形でgradeの交換整数+1・奇位相非零を確認。**raw履歴の同一視、全3-Hom構成、strict interchangeを主張しない。**
- [F112-P76 #2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451)：真正F55 squareOnly比較証拠の縦合成、二段階代表元輸送と合成比較の**正規化自由経路・全選択shadowでの整合性**を証明。旧bridgeと新bridgeの差分を実証拠の加法として正確に記録し、**比較経路の等号を明示的に仮定した場合に限り**合成経路等号を導出。真正C60交換正方形のraw履歴は単位左合成と異なるが、正規化経路・shadowは一致。raw 4-cellの無条件存在やstrict interchangeは未証明。
- [F112-P77 #2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452)：真正九構成子F55 raw 3証明間に**Type値の八生成規則による縦4-cell証拠**（反射・対称・推移・左右whisker・左右単位・結合）を構成。P59正規化経路と選択shadowへの健全性を**別々に証明**し、P62単位合同と接続。4-cell証拠の存在だけを関係とする正確なSetoid・商を作り、実C60のraw非同一な二証明間の4-cellを構成。全ての同値shadow・同値経路から証拠が得られるとは言わない。
- [F112-P78 #2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453)：P77の**真正4-cell合同による縦合成のwell-definedness**を証明し、元のF54経路上に、P77商をHomとする別の明示的Mathlib `Category`構造を実装。単位・結合はP77のraw4-cell証拠から証明し、正規化経路と全shadow観測の合成保存を証明。**局所的な厳密な縦合成のみ**であり、水平interchange・大域strict 3/nは未証明。
- [F112-P79 #2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455)：**P77のraw4-cell合同では水平単位律を満たせないことを証明**。元F55の真の恒等3射２つを水平合成したraw証明のP59正規化経路長は２、結果経路のraw恒等3射は０。したがってP77のType値4-cellは存在せず、その厳密商クラスも非同一。左右contextの単位も同様に長さ１対０で障害がある。一方、P62の構文由来`unitOnly`経路合同ではすべて関係すること、両raw証明のfull shadowは一致することを示し、真正C60六角形の二つの独立F54 associatorで具体化。**P77の厳密な経路等号を保ったまま水平単位4-cellを追加することは不可能**だが、より弱いP62相対の証拠付きcoherenceは排除しない。
- [F112-P80 #2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457)：P79の厳密P59経路等号に関するno-goを保持したまま、**新しいType値raw4-cell presentation**に、旧P77証拠の明示的埋込み・水平単位・左右context単位の３生成規則を追加し、反射・対称・推移・左右縦whiskerへ閉じた。全証拠についてP62の構文由来単位経路**合同への健全性**と、F55原full shadow保存を独立に証明。実証拠存在によるSetoid・商のexact kernel、縦合成の4-cell適合性、shadow readoutの因子化を構成。真正C60で**旧P77商は非同一、新P80商は同一**と証明。P80は選択された新presentationであり、元raw歴史やP77 no-goを消してはいない。
- [F112-P81 #2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459)：P80の**新しいP62相対Type値4-cell商**について、実際の左右whisker証拠から縦合成のwell-definednessを証明。旧P77の単位・結合4-cellをP80へ明示的に埋め込み、F54原経路上に**別の厳密な局所縦Mathlib Category**を構成した。選択F55 full shadowの加法性・単位零を証明。旧P77商から新P80商への**raw履歴を変えない全射**を定義し、縦合成・shadowの保存、真正C60での**非単射性**と、新P80商へのP59証明ラベル付き自由経路の厳密readout**非降下**を証明。P77合同は変更せず、P62相対coherenceとP59経路等号を混同しない。

- [F112-P82 #2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461)：P80の**全9種類のType値4-cell生成規則**に保存される、元F55 raw構文由来の独立Nat不変量を構成（旧P77の8生成規則についても別に保存を証明）。元の**縦左単位4-cell** `id ≫ f ~ f` の両代表元を同じ右raw恒等3-cellと元F55の方法で水平合成すると、非単位・非`trans`原証明について不変量が**1対2**となる。したがって水平合成後の**P80 Type値4-cellは存在せず、P80商クラスも異なる**ことを、実際の北側C60五角形のpentagon 3-cellを用いてLean4で証明。これにより、**選択したP80商へ元F55水平合成は一般には降下しない**。これはP80 presentationの不足を示すものであり、P62の構文的合同やstrict 3圏一般の不可能性ではない。

- [F112-P83 #2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463)：mathlibの`Quiver.Path.addWeight`を利用し、P82の**raw構文由来Nat不変量**を元F55の型付きP59自由経路全体へ拡張した。元F55の9構成子に沿った正規化の厳密保存と、**P62単位経路合同の全5生成規則**に対する保存を証明。そのため、P82の真正縦左単位4-cellを左右の同じ恒等証明と水平合成して得た2つのfree pathは、不変量**1対2**によって**P62でも比較不能**であり、P62 Mathlib商でも異なることをそのexact kernelから証明。真正C60北五角形の原pentagonを用いた実例も形式化。**既存P62の健全性を維持したまま、不足するcontext 4-cellを単純追加することはこの実例で不可能**。これは既存P62/P80の選択についてのobstructionであり、一般のstrict 3圏や空の不可能性ではない。

- [F112-P84 #2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465)：旧P62のunit-only経路合同とP80のType値raw4-cell証拠を**変更せず**、別の**P84水平4-cell証拠付きType依存free-path合同**を構成した。旧P62証拠、同値律、縦経路合成の合同に加え、**任意の真正P80 Type値4-cellを左右から原F55 raw 3-cellで水平whiskerする2つの比較規則**を明示。全7生成規則で元F55 full shadowが保存されることを証明し、mathlibのCongruence・厳密な局所CategoryTheory.Quotient・**商のexact witness kernel**・原shadowへの因子化を完成。旧P62商から新P84商への自然な比較関手と、原P59自由経路→旧P62商→新P84商の厳密な可換三角形も形式化した。P82/P83の比較は**旧P62商で非同一、新P84商では同一**となることを両商のexact kernelから証明し、真正C60北五角形でstrict enlargementを確認。旧P62/P80のobstructionは消去していない。

- [F112-P85 #2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467)：旧P80 Type値4-cellと原F55 raw証明履歴を保持し、**左右の水平whiskeringを証拠付き生成規則とする別のType値4-cell presentation**を構成。旧P80埋込み・反射/対称/推移・左右縦whisker・左右水平whiskerの**全8生成規則**について、**新P84の真正typed path合同への健全性**とF55 full shadow保存を独立に証明。実証拠の存在だけをkernelとするSetoid/商を構成し、元F54 routeを対象とする別の厳密な**局所縦Mathlib Category**を旧P77の実単位・結合4-cellにより構成。旧P80商から新P85商への全射と、元F55水平合成の**P80商×P80商→P85商という代表元独立の二入力演算**を真正左右4-cell証拠で証明。真正C60北五角形で旧P80商は非同一、新P85商は同一。旧P82・P83のobstructionは否定されず、旧P62への全面的健全性は主張しない。

- [F112-P86 #2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)：旧P84経路合同と旧P85のType値4-cellを**変更せず**、左右context・pre/post F54 route・左右水平whiskeringの6種類の真正P85証拠付き比較を持つ**新P86経路合同（11生成規則）**と、その上の**新P86 Type値raw4-cell（12生成規則）**を構成。両者について元F55 full shadow保存を別々に証明し、新Type値4-cellの新経路合同健全性・証拠存在に基づくSetoid/商のexact kernelを形式化。経路合同側では厳密な局所Mathlib Category商、旧P84→新P86経路商の比較関手と可換因子化を構成。Type値4-cell側では元F54経路上の別の厳密局所縦Category、旧P85→新P86商の全射・縦合成保存、**P85商→P86商の左右context・pre/postcomposeの4種類の代表元独立輸送**および**旧P85商×旧P85商→新P86商**の真正証拠付き水平二入力演算を実装。真正C60北五角形の旧P85 4-cellを実際の左F45 contextに輸送するType値証拠とP86商等号も証明した。P82/P83の旧presentationに関するno-goは保持する。

- [F112-P87 #2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471)：P86の「旧P85商×旧P85商→新P86商」という段階的輸送から進み、**P87の真正Type値4-cell自身に左右context・pre/post F54 route・左右水平whiskeringを再帰的に施せる新presentation**を構成した。旧P86証拠を保持する12生成規則で原F55 full shadow保存と二入力の真正4-cell証拠を証明。対応するP87型付き経路合同（11生成規則）のfull shadow健全性・厳密な局所Mathlib Category商・source witness exact kernel・旧P86経路商からの比較関手と可換因子化を形式化。P87 4-cellをP87経路合同に健全と証明し、実4-cell証拠をkernelとするSetoid商、**厳密局所縦Category**、旧P86 4-cell商からの全射・縦合成保存を証明。さらに、**P87商→P87商の左右context・pre/postcomposeの全4演算**と**P87商×P87商→P87商への元F55水平合成の代表元独立な自己閉包**を構成。水平単位は旧P80の真正Type値単位4-cellから導出し、全full shadowの水平加法性を検証。元F55のinterchange二辺のfull shadow一致も証明したが、これを4-cell証拠の存在やstrict interchangeと同一視しない。P66のC60 disjoint squareにおける元F54二経路の非同一性・odd phaseは保持される。

- [F112-P88 #2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473)：原F55の9構成子に対する非可換`List Bool`ソース語を構成。縦合成の連結・左右contextによる`false`/`true`ラベル化を記録し、P77/P80/P85/P86/P87の**全Type値4-cell生成規則**で保存されることをLeanで証明した。型付き中間因子`f₂`と`g₁`が構文上非単位（語が非空）なら、縦・水平二順序の語は`L(f₁)++L(f₂)++R(g₁)++R(g₂)`と`L(f₁)++R(g₁)++L(f₂)++R(g₂)`で一致せず、**真正P87 Type値4-cellの非存在とP87商での厳密な非等号**が成立する。`p88_word_nil_iff_unitOnly`と真正C60北五角形・六角形disjoint squareの原始語も検証。これは**現在のP87 presentationに対する条件付きno-go**であり、strict 3圏一般の不可能性やC60上の任意の4因子の実現を主張しない。原full shadow一致は依然必要条件のみ。

**P88で現在のP87 presentationのstrict interchange obstructionを証明しました。** 原ソースの非可換語がP87の全4-cell比較で保存されるため、非単位の中間因子を持つ真正型付きinterchange二辺は、同一P87商で等しくなりません。**次のP89ではP87の成果を変更せず、別のType値4-cell presentationにinterchangeの明示的な生成比較を加える場合の型・full shadow・経路対象・保存量の必要条件を証明**します。新presentationでは旧P88語は一般に不変ではないことを正確に記録し、F54の別経路対象とC60の非零奇位相を無条件に同一視しません。P89の新生成子を追加しただけで局所strict 3圏全法則や高次coherenceが完成したとは扱いません。独立Kuuは縁起から空を捉える一つのpresentationであり、C60以前のW/J/H一般化と空の空の理論を保持します。大域strict 3/n圏、(∞,3)-hyperdescentはなお未証明です。

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

- **公開統合正本：** [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。F112親PR #2339はMERGED。P79 #2455：Lean **9687/9687**・17宣言、P80 #2457：**9688/9688**・14宣言、P81 [#2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459)：**9689/9689**・13宣言を`KuuOSFormal`統合入口で検証し、いずれも新規`sorryAx`なし・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts 2/2 SUCCESS後にsquash MERGED。P81統合SHA `5c9925528d8a90239375104a2ac1a5e71e483559`。続くP82 [#2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461)は **9690/9690**・新規公理監査**10/10**（`sorryAx`なし）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P82統合SHA `f7a876996cebd940ea3d8bbacaa75e51ac781422`。P83 [#2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463)：**9691/9691**・公理監査**10/10**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P83統合SHA `7bd530e28551881198c3c61e22b6163c9025753e`。P84 [#2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465)は **9692/9692**・新規公理監査**18/18**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P84統合SHA `90be8065f5b4b682f239c7bfd220e48ab2c97f27`。P85 [#2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467)は **9693/9693**・新規公理監査**18/18**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P85統合SHA `19c787422a3c234c0a4e5e8777d1730deb56313e`。P86 [#2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)は **9695/9695**・新規公理監査**37/37**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・新規Leanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P86数学統合SHA `2efbce7af262c9c8203bc7e3fc6c24a3c6139e73`。P87 [#2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471)は **9698/9698**・新規公理監査 **39/39**（`sorryAx`なし。`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root全件保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P87数学統合SHA `32cbcd465a932d0b66524ab56026880d6fdf1227`。P87の3モジュールも単一公開入口`formal/KuuOSFormal.lean`から直接import。P88 [#2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473)は **9700/9700**・新規公理監査**18/18**（`sorryAx`なし）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance [#39769469429](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/39769469429) SUCCESS・completion receipts **2/2 SUCCESS**後にsquash MERGED（SHA `2eef23640dcc4f30144d2a7b13489c0d72165d99`）。P88A/Bも同じ公開入口から直接importし、内部`KuuOSStrict`は別の定理正本ではない。
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
