# KuuOS / 空OS — Formal Research Roadmap

**更新：2026-10-22 JST。C60以前の縁起一般理論・107公開rootを保持し、F112-P86までの新P86経路合同・真正Type値context/pre/post/horizontal4-cell証拠、厳密局所縦Category、P85→P86輸送・P85×P85→P86水平降下とC60の実証拠を反映。**

> **一般理論 → C60による具体的検証 → 一般理論の改善・strict高次化 → (∞,3)-hyperdescent。**
> 
> C60は縁起の一般化の起点ではない。独立Kuuも一つのpresentationであり、strict 3圏を証明できたとしても唯一の「空」ではない。定理の型・仮定・obstructionを失わず、一般化の数学的根拠を段階的に増やす。

この文書は[README](README.md)を補い、**検証済みの一般的定理／後から導入したC60の個別定理／条件付きの帰結／未証明の到達目標**を分離します。過去の定理を「C60研究の前準備」として書き換えたり、Gray非依存化のために既存成果を廃止したりしません。

## 0. 正本・依存・証明の判定

| 区分 | 正確な位置づけ |
| --- | --- |
| 公開統合正本 | [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。歴史的`formal/KUOS/`と現行`formal/Kuu/`、Qiを**同一Leanパッケージ**に含む。 |
| 独立Kuu F112研究 | [親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)は**MERGED**。かつての`formal/v5-293-f112-independent-total-change`は移行作業の履歴であり、現在の正本はmain。 |
| F112確認範囲 | **P86 [#2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)までmain統合済み**。P79：9687/9687・17宣言、P80：9688/9688・14宣言、P81：9689/9689・13宣言、P82：9690/9690・10宣言、P83：9691/9691・10宣言、P84：9692/9692・18宣言、P85：9693/9693・18宣言、P86：**9695/9695・37宣言**。各PRは新規`sorryAx`なし・対象Leanエラー/警告0・exact-head Governance・107公開root保全・completion receipts 2/2 SUCCESS。P85統合SHA `19c787422a3c234c0a4e5e8777d1730deb56313e`、P86統合SHA `2efbce7af262c9c8203bc7e3fc6c24a3c6139e73`。P86の両モジュールとも単一公開`KuuOSFormal`から直接import済み。 |
| 既存定理の証拠 | 実際のLean宣言・型と仮定・`#print axioms`・対応するexact-head CI。`sorryAx`、`sorry`、`admit`、新たな未証明公理による補完は禁止。 |
| 数学的区別 | raw Type-valued証拠、Prop証明、選択した商、観測、物理的解釈は互いに無条件には同一視しない。 |
| 公開入口・toolchain | `lake build KuuOSFormal`（`lake build`も同じ）。既存107公開rootは維持。Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。 |
| 別レーン | PR #1558（Lean 4.31）はvalidation-only、Draft・未マージ。Lean/mathlibの正式な固定環境は上記のまま。 |

GitHub正本・Lean成果・README/ROADMAP・CI・歴史的スナップショットには異なる役割がある。**P86までのmain統合はGitHub上のMERGED commitとexact-head CIにより確認済み**。文書編集を数学的証明の代替とせず、C60以前の縁起一般化成果も維持する。

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
| v4.00–v5.36 | [旧ROADMAP §2](docs/legacy/ROADMAP-v5.291.md#2-obstruction-localization-and-exact-classification-foundations--v400v536) | 明示的な非因子化・capacity/incidence障害、presentation-sensitive descent、exact-universal分類、actual-liftへ進む一般的条件。結果の有効範囲は各Lean型に相対的。 |
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
| F112 P27–P53 | [統合済み親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)で歴史的ソースの独立比較と真正面relatorを整理。P53は全32原面relatorを用いる原F42面商→F69の無条件因子化に到達。 | 別presentationの原3-Hom全体を勝手に同型としない。 |
| F112 P54–P57 | [P55 #2417](https://github.com/itakura-hidetoshi/KuuOS/pull/2417)、[P56 #2418](https://github.com/itakura-hidetoshi/KuuOS/pull/2418)、[P57 #2419](https://github.com/itakura-hidetoshi/KuuOS/pull/2419)・[#2420](https://github.com/itakura-hidetoshi/KuuOS/pull/2420)：raw F55の九生成子、完全source transport、水平自然性、選んだshadowの忠実な圏関手、非復元と別位相のobstruction。 | chosen shadowが唯一の空であることや、raw 3-cellがすでにstrict 3圏であること。 |
| **F112 P58** [#2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421) | **raw F55のliteral単位律・結合律の失敗**を構文の数え上げで証明し、mathlib自由経路圏を別途構成。 | raw証拠とstrict経路の同一視は禁止。 |
| **F112 P59** [#2423](https://github.com/itakura-hidetoshi/KuuOS/pull/2423) | ９構成子の垂直正規化：raw単位→空経路、raw垂直合成→連結、その他７構成子→個別生成辺。 | 垂直strict化から水平単位・交換は導けない。 |
| **F112 P60** [#2424](https://github.com/itakura-hidetoshi/KuuOS/pull/2424)・[#2425](https://github.com/itakura-hidetoshi/KuuOS/pull/2425)・[修復 #2428](https://github.com/itakura-hidetoshi/KuuOS/pull/2428) | mathlib自由経路正規化関手と、選択された`(ℤ×ℤ)×ℤ/2ℤ` shadowへの整合性。raw証明履歴が一般に非復元であることを区別。 | 数値shadow商をstrict 3圏の完成形にしない。 |
| **F112 P61** [#2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426) | 水平合成の垂直正規形は２辺。raw単位同士を水平合成すると長さ２で、空経路とはliteralに異なる。selected shadowでは値0。 | P61は現presentationの障害であり、大域strict 3圏no-goではない。 |
| **F112 P62** [#2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429) | ９構成子の再帰的な**単位生成構文**から、同じ型付きF54両端を持つ自由経路の関係を生成。反射・対称・推移・垂直合成の合同性、選択された観測への健全性、P61水平単位と空経路の**関係上の同値**をLean4で証明。真正C60 pentagon/hexagon生成子は単位生成構文から除外。 | 水平合成の任意の代表元に対する合同性、結合律、全interchange、global strict 3/nは未証明。 |
| **F112 P63** [#2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431) | 全９構成子に対して単位生成raw証明のF54始終経路が同じになることを再帰的に証明。左右contextをmathlib自由経路関手として構成し、垂直合成と原raw生成元の輸送、`unitOnly`保存、左右context付き単位セルのP62関係を証明。 | raw context自由経路関手がP62の**全ての**合同関係を保存することはまだ未証明。選択shadowの等号では代用しない。 |
| **F112 P64** [#2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432) | P62関係に対しmathlibの`Congruence`実装と`CategoryTheory.Quotient`を構成。`Q(f)=Q(g) ↔ f∼unit g`という等号反映、P61水平単位の商圏での等号、既存chosen shadowへの因子化と生成元観測の保存を証明。 | これは**垂直**商圏であり、水平の代表元独立性、全interchange、globular strict 3/n圏はまだ成立としない。 |
| **F112 P65** [#2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434) | raw `ident`生成辺とP59正規化後のunit-only単一生成辺を区別する`NativeF55UnitWord`を構成。全９構成子の正規化、typed unit wordのP62関係上の単位性、左右contextによるword保存、**P62の全５生成規則の左右context保存**を証明。mathlibの商圏`Quotient.lift`で左右作用をP64最小商圏へ降下させ、正確な因子化等式を得た。 | 左右各１変数の降下は完了。ただし**２変数の水平双関手性、水平合成の結合律、真のinterchange、strict 3/n圏**は未証明。 |
| **F112 P66** [#2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436) | P64の商関手は元の型付きF54経路**対象に単射**であり、任意の真正F54局所回転対の左先・右先交換経路は商圏でも異なる対象。真正C60六角形についても非同一性を証明。一方で両対象を結ぶF55 disjointSquare 3射は残り、その選択された交換位相は非零。 | **F54対象の厳密interchangeはP62–P65の3射単位合同だけでは導出不能**。適切な2-route比較、必要条件、その新たな関係で何が失われるかを先に定理化する。global strict 3/n不可能性とは言わない。 |
| **F112 P67** [#2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438) | ４構成子（単位・対称・推移・真正disjoint-square）の**Type値F54経路比較証拠**を構成。各証拠から真正F55 raw cellへ写像できる。比較の存在命題だけをSetoid化し、商クラス等号の必要十分性、実C60での左右順序同一視、同一視する任意の目標写像の非単射性、元の非零交換位相とraw履歴の存続を証明。 | クラス等号は具体的raw証明を一意に選ばない。P67関係が全contextに閉じることや全Hom輸送は未証明。 |
| **F112 P68** [#2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439) | ９構成子を検査し、五角形原始生成元を除く**squareOnlyの証明依存Type値rawセル**からcontext閉包比較商を構成。P67商→P68商、左右F54 contextのwell-definedな写像と代表元整合、真正C60交換比較を証明。 | P67商との同値・忠実性は未証明。route対象の商だけでは3-Homのtransport・globular strict 3圏・全interchangeを得ない。 |
| **F112 P69** [#2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441) | P68比較クラス上のF54代表経路とType値F55 raw 3-cellを保持する高次射の依存型構造。元raw証明項保存と、クラス等号から得られるsquareOnly証拠の存在を証明。 | クラス等号から証明項を正準に選ぶこと・高次Homの代表元独立な合成は未証明。 |
| **F112 P70** [#2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442) | 両端squareOnly証拠で選択した代表元変更と、中間比較証拠付きの高次射の合成を構成。原raw履歴と選択shadowの加法公式。実C60の恒等射（位相0）は交換正方形に沿って輸送すると位相1となり、両端の比較クラスは同じ。 | 合成は比較証拠の**選択依存**。原shadowを経路クラス等号だけから一意に復元してはならない。 |
| **F112 P71** [#2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444) | P70の選択証拠付き代表元変更から輸送同値・Setoid・商を構成。商等号の必要十分条件、同値な高次射でraw shadowが異なる場合には無補正のshadow readoutが全代表元上で商へ降下しないという一般的必要条件/no-goを証明。真正C60の輸送同値と位相差を確認。 | **原shadowの無補正な因子化に関する限定no-go**。補正付き・gradedな輸送、全Homの高次coherence、strict 3/n圏は未証明であり不可能とも主張しない。 |
| **F112 P72** [#2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446) | 比較証拠付き代表元変更・bridge付き縦合成によるshadow付加項を実際のF55 raw証明から導出し、補正公式、２段階輸送cocycle、真正C60交換正方形の補正前非零・補正後位相0を証明。 | 補正は証拠を選ぶgraded presentationの情報であり、P71の無補正商で全shadowが降下したとは言わない。 |
| **F112 P73** [#2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447) | 全９構成子にわたる`squareOnly`証明セルの五角形整数charge 0、P70左右輸送・bridge合成の五角形charge保存、P71輸送同値の全４規則での保存を証明。P71商上に五角形charge readoutを実際に`Quotient.lift`で構成。 | 全shadowは非降下、選択された交換位相は変更可能。五角形chargeの降下をすべての高次情報の復元と同一視しない。 |
| **F112 P74** [#2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448) | 元の符号付き整数線形観測`aP+bS`について、交換整数chargeを1だけ変化させる輸送同値対が存在する**固定されたP71商**では、全元代表値と一致する無補正商readoutの存在が`b=0`と必要十分と証明。真正C60の恒等F55 raw証明の交換charge0→交換正方形沿い輸送で1を検証。 | 分類対象は選択した２整数線形観測。補正付き/graded/torsor Hom、高次合成全体、strict 3/n・hyperdescentはまだ未証明。 |
| **F112 P75** [#2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450) | 既存P71輸送４生成規則を真正F55 Type値証拠を保持したshadow-grade付き輸送履歴に持ち上げた。健全性（終点shadow＝始点shadow＋grade）、同一raw両端のgrade一意性、閉路grade0、P71のProp輸送関係とgraded履歴のNonemptyの必要十分性、真正C60整数交換charge+1と非零奇位相を証明。 | gradeの唯一性はraw履歴の等号・証拠の標準選択ではない。真正bridge合成・高次interchangeのcoherenceと局所strict 3圏は未証明。 |
| **F112 P76** [#2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451) | 元のsquareOnly比較証拠をType値で縦合成し、二段階代表元輸送の正規化経路・全shadowの整合性、bridge移行時の正確なfull-shadow差分を証明。**明示的なbridge正規化経路一致の条件下**で全合成経路が一致する定理。実C60のraw履歴非同一と正規化同値を区別。 | bridge経路の一致やraw4-cellの存在を無条件には導いていない。局所・大域strict 3/nは未証明。 |
| **F112 P77** [#2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452) | 8規則の真正Type値raw F55 vertical 4-cell、縦単位・結合・左右whisker、P59正規化経路と全shadowへの各独立健全性、P62単位合同への片方向射、明示証拠存在を正確なkernelとするSetoid・Quotientを構成。実C60のraw非同一なsource履歴を4-cellで比較。 | 単なるshadow等号やpath等号から4-cell証拠が得られるという逆は未証明。水平interchangeも未証明。 |
| **F112 P78** [#2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453) | P77 source4-cell合同への縦合成の適合性から、元のF54 route上のHomをP77商とする**明示的Mathlib Category**を構成。原raw単位・合成および真正4-cell結合証拠による厳密な縦単位・結合法則。P59正規化自由経路とfull shadowの厳密加法性も証明。 | 既存Categoryインスタンスを置換しない独立presentation。水平二変数合成・interchange、4-cell間coherence、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P79** [#2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455) | 元のF55水平恒等合成と合成後恒等のP59経路長が２対０であることから、P77 Type値raw4-cell**非存在**と厳密商クラス非同一性を証明。左右F54 context単位も１対０の障害。全shadowの一致だけではraw4-cellが得られず、P62の構文由来単位合同では各対を比較できる。真正C60六角形の独立左右F54回転を用いて具体化。 | P77の厳密path等号を保つ4-cell拡張で水平単位律を満たすことは不可能。P80で別のP62-relative Type値4-cell候補を構成済み。大域strict 3/nやhyperdescentの不可能性とは異なる。 |
| **F112 P80** [#2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457) | 旧P77の真正Type値4-cellを保持したうえで、水平単位・左右context単位を**新たなType値4-cell生成規則**として明示し、反射/対称/推移/左右縦whisker閉包を構成。全生成規則のP62構文的unit-path合同への健全性と原full F55 shadow保存、縦合成適合性、実証拠存在をexact kernelとするSetoid商・shadow因子化を証明。真正C60で旧P77商の非同一性と新P80商の同一性を併記。 | 新しい比較は選択されたpresentationであり、旧P77 path equalityのno-goを覆さない。P81で新商上の局所縦Categoryを完成。一方、一般水平2変数合成はP82で現P80商への非降下を証明。interchange、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P81** [#2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459) | 新P80のType値4-cellに基づく縦合成well-definednessと厳密な局所Mathlib `Category`を構成。原F55 full shadowの合成保存・単位零、旧P77→P80の実証拠由来全射・縦合成/全shadow保存、真正C60での非単射性、P59厳密自由経路readoutの新商への非降下をLeanで証明。 | 単一公開KuuOSFormalへ直接import。旧P77・P79の障害を保持。水平双変数合成についてP82で現P80商への非降下を証明。interchange、4-cell間coherence、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P82** [#2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461) | 元F55 raw構文から独立したNat値不変量を定義し、旧P77の8生成規則とP80の全9種類のType値4-cell生成規則すべてで保存することを証明。旧P77の縦左単位4-cell `id ≫ f ~ f` に元の水平合成（右側は同じ恒等3-cell）を施すと、非単位・非`trans`の`f`では不変量が**1対2**となり、**P80の4-cell非存在と商クラス非同一性**を証明。真正C60北五角形のpentagon 3-cellと型付き右恒等経路で実現。 | **現P80商には元F55水平合成が一般には降下しない**ことが確定。P80以外の比較presentation、P62合同一般、strict 3圏一般のno-goではない。今後のcontext輸送・高次比較証拠・その健全性とstrict interchangeは未証明。 |
| **F112 P83** [#2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463) | mathlib `Quiver.Path.addWeight`によりP82 raw Nat不変量を元F55型付きP59 free pathへ拡張。原raw 9構成子と正規化の適合性、P62 unit-only合同の5生成規則すべての保存をLeanで証明した。P82で見つけたP80旧左単位4-cellの水平合成後の2つの真正raw証明は不変量が1と2で、**P62経路合同でも関係せず、P62のMathlib商でも非同一**とexact kernelから証明。真正C60北五角形へ具体化。 | **追加context 4-cellを旧P62に健全と主張することは、この例では不可能。** P80だけでなく、必要な比較について旧P62合同も不足。P62の全関係が無効という意味ではなく、P84で新しいpath合同とCategory商、旧P62からの比較関手、full shadow保存を形式化済み。ただし新Type値4-cellの一般context輸送は未証明。strict 3圏一般や縁起一般理論のno-goではない。 |
| **F112 P84** [#2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465) | **P62とP80を変更しない別presentation**として、旧P62合同証拠・同値/縦合成合同・任意の真正P80 Type値4-cellの左右水平whiskeringを生成規則とする新型付きfree-path合同を構成。全7生成規則についてF55原full shadowを保存し、Mathlib `Congruence`・局所`CategoryTheory.Quotient`・**exact source-witness kernel**・shadowへの厳密因子化を形式化。旧P62商→新P84商の比較関手と原pathとの可換三角形、P82/P83比較の**旧商非同一・新商同一**を証明。真正C60北五角形で真の拡張。 | これは**path合同とその局所Category商**であり、P81のP80 4-cell商上の縦Categoryとは異なる。P85で旧P80 4-cellの左右水平作用をType値新4-cellとして証明しP84 path合同への健全性を検証。ただし新P85 4-cell自体の全context輸送、新P85同士の水平関手性、strict interchange、高次coherence、大域strict 3/n・hyperdescentは未証明。P83の旧P62 no-goを変更しない。 |
| **F112 P85** [#2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467) | 旧P80のType値4-cellを明示埋込みし、左右水平whiskeringを真正F55 raw証拠付き生成規則とする**新しいType値4-cell言語**を構成。全8生成規則の**新P84 path合同健全性**と原F55 full shadow保存、実証拠exact kernelのSetoid/商、元F54経路上の**厳密な局所縦Mathlib Category**を構成。旧P80→新P85全射と、元F55水平合成の**旧P80商×旧P80商→新P85商**への代表元に依存しない二入力降下を左右真正4-cell証拠で証明。C60北五角形で旧P80商非同一・新P85商同一。 | **二入力のwell-definednessのみ**であり、新P85商×新P85商への全水平関手性、縦合成とのstrict interchange、旧P85証拠に沿ったpre/post・左右context輸送はP86でP85→P86商として証明済み。新P86自身の全4-cell輸送は未証明。旧P62やP80のno-goを覆さず、新しいP84 path合同を比較の証拠層とする。局所strict 3圏全法則・大域strict 3/n・hyperdescent未証明。 |
| **F112 P86** [#2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469) | 元P84経路合同と元P85 Type値4-cellを変更せず、P85の実証拠を使う左右F55 context・前後F54 route・左右水平whiskeringの6操作を新生成規則とする**P86型付きfree-path合同（11規則）**と、同じ6作用をType値ソースに備えた**P86 4-cell言語（12規則）**を構成。全生成規則のF55 full shadow保存、新P86 Type値4-cellから新経路合同への健全性、経路側Mathlib Category商とfull shadow因子化・exact kernel、Type側Setoid/Quotientのexact kernelと厳密局所縦Categoryを証明。旧P84→P86経路商比較関手、旧P85→P86の全射・縦合成保存、**旧P85商から新P86商への左右context・pre/post代表元独立輸送**、さらに**旧P85商×旧P85商→新P86商の二入力水平降下**を真正Type値4-cellで構成。北側C60五角形の実証拠を追加の左contextへ輸送したP86証拠と商等号も証明。 | 旧P82/P83の否定定理は元presentationについてそのまま保持。**P86自身の4-cell生成規則すべてに対する再帰的context/水平閉包、P86×P86→P86の双変数関手性、strict interchange、4-cell高次coherence、大域strict 3/n・(∞,3)-hyperdescentは未証明**。P86局所縦Categoryを局所strict 3圏完成と混同しない。 |

P58–P86の新規ソースは**canonical mainに存在**します。[P58](formal/Kuu/F112/PolygonNativeF55RawStrictificationBoundary.lean)、[P59](formal/Kuu/F112/PolygonNativeF55RawVerticalNormalizationP59.lean)、[P60正規化関手](formal/Kuu/F112/PolygonNativeF55RawPathNormalizerFunctorP60.lean)、[P61](formal/Kuu/F112/PolygonNativeF55HorizontalStrictPathBoundaryP61.lean)、[P62](formal/Kuu/F112/PolygonNativeF55TypedUnitCongruenceP62.lean)、[P63](formal/Kuu/F112/PolygonNativeF55ContextPathActionsP63.lean)、[P64](formal/Kuu/F112/PolygonNativeF55StructuralUnitQuotientP64.lean)。追加[P65](formal/Kuu/F112/PolygonNativeF55ContextUnitDescentP65.lean)・[P66](formal/Kuu/F112/PolygonNativeF55C60InterchangeRouteObstructionP66.lean)・[P67](formal/Kuu/F112/PolygonNativeF55TypedSquareRouteComparisonP67.lean)・[P68](formal/Kuu/F112/PolygonNativeF55ContextSquareComparisonP68.lean)もmainにある。raw Type値の歴史、経路対象、単位合同関係、square比較クラス、選択shadowの役割と等号を混同しない。 追加[P69](formal/Kuu/F112/PolygonNativeF55HigherHomTransportBoundaryP69.lean)・[P70](formal/Kuu/F112/PolygonNativeF55HigherHomRepresentativeTransportP70.lean)・[P71](formal/Kuu/F112/PolygonNativeF55HigherTransportQuotientP71.lean)・[P72](formal/Kuu/F112/PolygonNativeF55TransportShadowCocycleP72.lean)・[P73](formal/Kuu/F112/PolygonNativeF55PentagonChargeTransportDescentP73.lean)・[P74](formal/Kuu/F112/PolygonNativeF55LinearChargeDescentP74.lean)・[P75](formal/Kuu/F112/PolygonNativeF55GradedTransportCoherenceP75.lean)もmain統合済み。 追加[P76](formal/Kuu/F112/PolygonNativeF55BridgeTransportPathCoherenceP76.lean)・[P77](formal/Kuu/F112/PolygonNativeF55RawVerticalFourCellP77.lean)・[P78](formal/Kuu/F112/PolygonNativeF55RawFourVerticalCategoryP78.lean)もmain統合済み。 追加[P79](formal/Kuu/F112/PolygonNativeF55RawFourHorizontalUnitObstructionP79.lean)もmainへ統合済み。 追加[P80](formal/Kuu/F112/PolygonNativeF55P62RelativeUnitFourCellP80.lean)もmain統合済み。 追加[P81](formal/Kuu/F112/PolygonNativeF55P80UnitFourVerticalCategoryP81.lean)もmainに存在し、単一公開`KuuOSFormal`から直接import済み。 追加[P82](formal/Kuu/F112/PolygonNativeF55P80HorizontalContextObstructionP82.lean)もmainに存在し、P80水平合成の非降下定理と真正C60実例を収録している。 追加[P83](formal/Kuu/F112/PolygonNativeF55P62HorizontalContextObstructionP83.lean)もmainに統合され、P62 path合同の不変量保存とC60の非比較定理を保管する。 追加[P84](formal/Kuu/F112/PolygonNativeF55P80HorizontalPathCongruenceP84.lean)もmainにあり、P80 4-cell証拠による新経路合同、正しいMathlib商、旧P62比較関手、真正C60 strict enlargementを含む。 追加[P85](formal/Kuu/F112/PolygonNativeF55P84HorizontalFourCellP85.lean)もmainへ統合され、新しいType値4-cellの水平証拠・P84 soundness・局所縦Category・旧P80からの二入力演算とC60 strict enlargementを収録する。 追加[P86経路合同](formal/Kuu/F112/PolygonNativeF55P86ContextPathCongruence.lean)と[P86真正Type値4-cell](formal/Kuu/F112/PolygonNativeF55P86ContextFourCell.lean)もmain統合済みで、両者を単一公開KuuOSFormalから直接importする。

## 3. 最優先の新規数学：局所proof-relevant strict 3圏

**目標:** C60を一つの具体例として含み得る一般的な高次source`\mathcal K`に、globularな`0,1,2,3`射の型付き境界と合成を設け、**strict 3圏の全公理をLean4で証明**する。

必要な義務：

1. **境界とglobularity**：全射の`source/target`、2/3射の平行性、各方向の合成可能性を型で保証する。
2. **合成・単位・結合律**：`\circ_i`を定義し、すべての定義可能な段階でstrictな左右単位・結合の等式を証明する。元のraw語のliteralな等式とは混同しない。
3. **全interchange**：異なる`i<j`方向の合成について、弱いinterchanger 3射ではなく厳密な等式を証明する。Gray圏のcoherenceを証明の代用品にしない。
4. **非自明性・source情報**：raw証拠、原F54/F55履歴、位相・曲率・障害を失うか否かを**個別の保存/非保存定理**で記載する。単に全3射を同一視した圏ではこの研究目標を達成しない。
5. **最小の整合関係またはno-go**：P77のraw4-cell/P78旧縦CategoryではP59自由経路等号を保存するため、P79で元水平単位律の障害が確定した。P80はそれを維持した別presentationとして水平・左右context単位のType値4-cellを明示的に追加し、P62構文的合同に健全。P81は新P80商上で厳密な局所縦Categoryを構成し、P77→P80全射・C60非単射性とP59厳密path readoutの新商への非降下を証明した。P82では元水平合成がP80合同を保存しないことを旧縦左単位の実4-cellと独立raw構文不変量で形式的に示し、真正C60北五角形で具体化した。P83ではその不足するcontext比較が元P62 unit-only path合同でも成立しないことをmathlibの加法的free-path不変量により証明した。P84では元P62/P80を改竄せず、新しいpath合同を真正P80 Type値4-cellの左右水平作用を生成規則として構成し、shadow保存・Mathlib Category商・exact kernel・旧P62比較関手・真正C60真拡張を証明した。P85では旧P80 Type値4-cellの任意の左右水平whiskeringを新しいType値4-cell証拠として構成し、P84 path合同への健全性、full shadow保存、局所厳密縦Category、旧P80商×旧P80商→新P85商の二入力well-definednessを証明。P86では旧P85 4-cellの左右context・pre/postルート・左右水平輸送を別のP86 path合同とType値4-cellで実装し、全生成規則のshadow保存・path健全性、二つの局所商/Category、および**P85×P85→P86の水平二入力降下**を実証した。P87以降でP86証拠自身の再帰的context/水平閉包・P86×P86の関手性、strict interchangeとその不足する高次比較証拠を判定する。

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

**次の証明作業の優先順位:** P79旧P77水平単位no-go、P80のP62相対Type値raw4-cell、P81の縦Category、P82/P83の旧presentationにおける厳密なobstruction、P84の新経路合同、P85の新Type値水平4-cellとP80×P80→P85演算、P86の**新context/route経路合同とType値4-cell・P85→P86四輸送・P85×P85→P86水平降下**を保存 → **P87：P86の12種類の真正Type値4-cell規則が左右context・pre/postcompose・水平合成に再帰的に適合するか証拠付きで判定。必要なら別presentationとC60 obstructionを明示し、P86×P86水平関手・interchangeを検討する** → 厳密局所strict 3圏全法則 → C60以前のW/J/H・縁起一般化成果との比較 → 大域strict 3/n → (∞,3)-hyperdescent。独立Kuuを唯一の空にせず一つのpresentationとして保持し、Grayに戻らない。

**絶対に行わないこと:** Gray圏でstrict 3圏の未証明法則を置換して完了と言うこと、旧約107公開rootの一括削除、歴史的な数学を`legacy/`だけに押し込むこと、strict性を得るために全raw証拠を無条件に潰すこと、未証明の存在条件を新公理へ置くこと、exact-head CIと公理監査を通さず未検証成果をmainに統合すること。

**証明と検証:** `formal/KuuOSFormal.lean`を通常の公開入口として維持。部分ビルドは同一パッケージの開発時の時間短縮だけです。対象ファイル全文・import閉包・mathlib定理・Lean形式の原因を調べ、正本コミットのexact-head CIと`#print axioms`を確認します。共有cacheと重複ジョブ削減を進めても、必要な公理監査・検証を抜きません。

~~~bash
python3 scripts/check_public_proof_roots.py
python3 scripts/run_kuu_foundation_check.py
lake exe cache get   # キャッシュが本当に不足する場合だけ
lake build KuuOSFormal # warningAsErrorはlakefile.toml既定。sorryAxは#print axiomsで確認。
~~~

`KuuOSStrict`は内部import集約にすぎず、旧定理やmathlibを使わない特殊な「空の正本」ではありません。Lean4の証明／runtime／AI入出力／権限・行為／実証データはそれぞれ異なる保証範囲です。

## 11. 継承用の参照先

- [現行README](README.md) — 研究の目的・全体像・成果の入り口
- [旧README v5.291](docs/legacy/README-v5.291.md)、[旧ROADMAP v5.291](docs/legacy/ROADMAP-v5.291.md) — 長い一般的・歴史的証明台帳と原型
- [F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) — 移行済み履歴（MERGED）。公開正本はmain。
- [F112-P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421) — raw strict-law obstructionと別の自由path envelope
- [F112-P61 #2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426) — 水平単位の非strictな自由経路境界
- [F112-P62 #2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429) — identity-generated typed path relation
- [F112-P63 #2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431) — genuine left/right typed context free-path functors（9671/9671 Lean SUCCESS）
- [F112-P64 #2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432) — minimal typed structural-unit quotient category（9672/9672 Lean SUCCESS）
- [F112-P65 #2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434) — two-sided contextual congruence preservation and exact quotient descent（9673/9673 Lean SUCCESS）
- [F112-P66 #2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436) — genuine C60 disjoint-square F54 route objects remain distinct and odd 3-cell survives（9674/9674 Lean SUCCESS）
- [F112-P67 #2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438) — Type-valued F54 square witness and exact comparison class / noninjective strict-target boundary（9675/9675 SUCCESS）
- [F112-P68 #2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439) — context-closed squareOnly Type witness and exact F54 class context actions（9676/9676 SUCCESS）
- [F112-P69 #2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441) — original proof-relevant F55 3-cell package over F54 comparison classes（9677/9677 SUCCESS）
- [F112-P70 #2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442) — witness-indexed higher-arrow transport and genuine C60 phase change（9678/9678 SUCCESS）
- [F112-P71 #2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444) — transport quotient and exact original chosen-shadow no-factor theorem（9679/9679 SUCCESS）
- [F112-P72 #2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446) — chosen-witness shadow correction and two-stage cocycle（9680/9680 SUCCESS）
- [F112-P73 #2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447) — pentagon integer charge descends through transport quotient（9681/9681 SUCCESS）
- [F112-P74 #2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448) — integer-linear signed charge descent iff square coefficient zero under true unit-square shift（9682/9682 SUCCESS）
- [F112-P75 #2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450) — source-history-retaining Type-valued graded transport, unique full charge and true C60 odd increment（9683/9683 SUCCESS）
- [F112-P76 #2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451) — genuine F55 bridge transport, conditional strict-path coherence, true C60 raw inequality（9684/9684 SUCCESS）
- [F112-P77 #2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452) — raw Type-valued 4-cell certificates and exact source-witness quotient（9685/9685 SUCCESS）
- [F112-P78 #2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453) — strictly associative local vertical category on actual raw 4-cell classes（9686/9686 SUCCESS）
- [F112-P79 #2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455) — original raw F55 horizontal-unit obstruction for P77 four-cell quotient, positive P62-relative witness and physical C60 specialization（9687/9687 SUCCESS）
- [F112-P80 #2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457) — Type-valued P62-relative horizontal/context unit 4-cell presentation, original source shadow conservation, exact witness quotient and real C60 strict enlargement（9688/9688 SUCCESS）
- [F112-P81 #2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459) — P62-relative P80 source four-cell strict local vertical category, surjective P77→P80 comparison, genuine C60 noninjectivity and no exact free-path readout（9689/9689 SUCCESS）
- [F112-P82 #2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461) — independent source-syntactic Nat invariant conserved by eight P77 and nine P80 Type-valued 4-cell constructors; genuine C60 north-pentagon horizontal counterexample to P80 quotient descent（9690/9690 SUCCESS、axioms 10/10、sorryAxなし）
- [F112-P83 #2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463) — mathlib additive path weight invariant sound for all five P62 congruence generators; actual C60 contextual horizontal counterexample survives original P62 quotient（9691/9691 SUCCESS、公理監査10/10、sorryAxなし）
- [F112-P84 #2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465) — distinct P80 horizontal-four-cell-witness-generated typed path congruence, exact Mathlib quotient, full shadow factorization, P62-to-P84 comparison functor, and strict C60 path quotient enlargement（9692/9692 SUCCESS、公理監査18/18、sorryAxなし）
- [F112-P85 #2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467) — proof-relevant Type-valued horizontal P80 4-cell transport sound for P84 path congruence, full shadow, local strict vertical Category and genuine C60 noninjective P80→P85 comparison（9693/9693 SUCCESS、公理監査18/18、sorryAxなし）
- [F112-P86 #2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469) — P85-witness-generated typed context/pre-post/horizontal P86 path congruence (11 rules) and P86 Type-valued four-cell (12 rules), both original full-shadow sound, exact local quotients, strict local vertical Category, P85 context actions and P85×P85→P86 horizontal descent, genuine C60 contextual witness（9695/9695 SUCCESS、新規公理監査37/37、sorryAxなし）
- [`AGENTS.md`](AGENTS.md) — 現行のpublic root・mathlib・Gray依存・ビルド境界
- [`formal/KUOS/`](formal/KUOS/) — 過去から継続する一般的なLean数学
- [`formal/Kuu/`](formal/Kuu/) — 現在の独立Kuuの具体的な構成

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
