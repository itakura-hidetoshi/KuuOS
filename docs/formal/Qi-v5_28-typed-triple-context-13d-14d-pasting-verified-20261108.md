# Qi v5.28 — 三連真正文脈の型付き貼り合わせ・選択13D/14D比較

2026年11月8日 JST。唯一のcanonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.27の定理#3309・公開集約#3310・正式記録#3311のMERGEDを継承。旧F55/P77/GK5CGと元6D〜14Dの証拠Type値、以前の選択presentationは一切変更しない。

## 1. 正本とexact-source形式検証

| 項目 | GitHub MCPで再確認した状態 |
|---|---|
| 定理PR | [#3312](https://github.com/itakura-hidetoshi/KuuOS/pull/3312) **MERGED** |
| 定理source最終HEAD | `dc01ad57bd9b5226665368401862aa7efeac3151` |
| 定理test-merge | `80d0c44cfeae56e6ca6c2047003c59e314f0a251` |
| 定理squash main | `085fd3e4de25b1f7d4668dc5bc5f68fed5606291` |
| 上記3 commitのGit tree | **`ccbd473d55f6c9dac0376b9c9cf1ae64bdd73e1e` 完全一致** |
| 最終定理exact-source CI | [#42446718916](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42446718916) **completed/SUCCESS** |
| Scoped Strict Lean | **9,080 / 9,080 SUCCESS** |
| Governance | **選択5 / 5ジョブ SUCCESS** |
| 新規宣言公理依存監査 | **40 / 40**、33件公理不要・7件標準公理のみ |
| 使用する標準公理 | 対象宣言で `propext`・`Quot.sound` のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 変更Lean error / warning | **0 / 0** |
| 最終定理差分 | 新規Leanモジュール1件、620行追加／削除0 |
| 公開集約PR | [#3313](https://github.com/itakura-hidetoshi/KuuOS/pull/3313) **MERGED** |
| 公開集約exact-source CI | [#42447117936](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42447117936) **completed/SUCCESS** |
| KuuOSFormal Strict Lean | **10,341 / 10,341 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開集約source/test-merge/squash tree | **`9265f5dc9a1fa9f70a6f4ee148716054684d0a6e` 完全一致** |
| 公開集約squash main | `7f86d3b1f69b65268112407a376388741ac88487` |
| 公開集約差分 | import1行のみ、既存文字列削除0 |
| Lean / mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root／保護PR | root107維持、#1558 Draft／OPEN／未マージ |

[新規Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TripleContextHigherPastingV5_28.lean)。

対象限定ビルドの9,080と公開集約ビルド10,341は別の検証対象であり、混同しない。全40宣言の`#print axioms`をexact-sourceログで確認した。証明の採用・mainへの統合は双方のCI完了後とし、source/test-merge/squash tree一致までGitHubで確認した。

## 2. 元の第七セルを三回重ねる、二つの貼り合わせ

元の六セル境界が厳密に合う三つの独立した第七セル証拠

\[
u:a\Rightarrow b,\quad
v:b\Rightarrow c,\quad
t:c\Rightarrow d
\]

および真正の元第七〜第十一セル証拠値`F : ContextFrameEleven W l r d e`を固定する。
元第十一セルへの`contextFrameLeft`を三回適用することで

\[
X=L_u(L_v(L_t(F)))
\]

を構成する。次の二つの元第七セルの**括弧付け履歴**は別々に保持する：

\[
Y_L=L_{(u\circ v)\circ t}(F),
\qquad
Y_R=L_{u\circ(v\circ t)}(F).
\]

`selectedLeftTripleInnerPasting` は`X\to Y_R`、`selectedLeftTripleOuterPasting`は`X\to Y_L`の具体的な元選択12D証拠を作る。右文脈についても独立に`selectedRightTripleOuterPasting`と`selectedRightTripleInnerPasting`を構成。各証拠はv5.27の実際の`compLeft/compRight`を使い、必要な箇所では`whiskerLeft/whiskerRight`によって前後文脈へ運ぶ。

重要なauthority境界として、`Y_L`と`Y_R`を元の生の第十一セル証拠としてEqに置き換えてはいない。両者はそもそも`SevenRewrite.trans`の括弧付けが異なる。

## 3. 新しい第十二セル生成元を追加しない、型付きrebracketing

`selectedLeftTripleRebracket`は、真正の既存12D証拠の`reverse`と`chain`から

\[
\boxed{Y_L\xRightarrow{\;12\;}Y_R}
\]

を組み立てる。右文脈も同様である。この12D橋は**元の選択12Dの反転・合成から導出**され、別の12D associator生成元ではない。

二つのパスは、左では

\[
P_L:X\to Y_R,\qquad
Q_L:X\to Y_L\to Y_R
\]

であり、右でも`P_R,Q_R`を型付きで構成する。
ここで`Q_L`には`X\to Y_L\to X\to Y_R`という明示的な**戻り道**が含まれる。これは真正の12D文脈経路履歴であり、単に第七セル構文の結合則を仮定しているわけではない。
`selectedLeftTriple_rawDistinct`と`selectedRightTriple_rawDistinct`は、両経路の**生の12D証拠値が一致しない**ことを証明した。

## 4. 独立選択第十三セルと元v5.23の保持

`SelectedTriplePastingThirteen W l r P Q`を、始終点が一致する**実在v5.27選択12D経路**の間の新規比較Typeとして構成する。新しい局所比較は、真正三連の左・右文脈の2系列に限る`tripleLeft/tripleRight`である。`strict/reverse/chain/prepend/append/associator`の型付き構文閉包も明示した。

`originalFramedTwelveToSelected`は旧v5.23の真正framed12D値をv5.25・v5.27の2段の`previous`で保持し、`originalThirteenToTriple`は実際の`CompositionalWhiskerThirteen`証拠値を新Typeの`inheritedOld`に保持する。いずれの生証拠埋込みも単射を形式証明。

`selectedTripleLeft_higherWitness`と`selectedTripleRight_higherWitness`は、選択13D比較の存在と元の12D生経路の非等号を同時に証明する。
`selectedTripleLeft_noRawEqualityInterpreter`は、当該選択比較を`P=Q`の元raw証明と読む万能解釈ができないことを示す。

## 5. 条件付き選択第十四セル

`SelectedTriplePastingFourteen`を、平行な新13D比較証拠間の**別の選択比較Type**として構成。三連文脈の局所的な`tripleLeftUnit`・`tripleRightUnit`は、同じ13D証拠の前後に`strict`を貼った二通りの生13D経路を比較するための**明示的な選択生成元**であり、元のraw13D Eqではない。

`selectedTripleLeftFourteen_conditionalCube`と右側の同名定理は選択14D比較の存在と、生13D経路の非等号を同時に示す。`selectedTripleLeftFourteen_noRawEqualityInterpreter`は14D証拠が元13Dの厳密Eqを意味しないことを証明。

`originalFourteenToTriple`はv5.23で既証明の`SelectedCompositionFourteen`証拠を`inheritedOld`にそのまま保持し、raw証拠埋込みの単射性を証明する。新しい三連13D比較と旧v5.23の全14D比較が自動的に相互交換可能・自然同型であるとは主張していない。

## 6. 初回Lean失敗の型的原因と無弱化修正

初回Leanでは、右側の`selectedRightTriple_rawDistinct`および右側の`tripleRightThirteenUnit_rawDistinct`の`cases h`が、元第七セルの依存添字に関して`F.1 = F.s.trans u`を要求し、`Dependent elimination failed`となった。

追加の`selectedTwelfthFirstAtomTag`および`selectedThirteenFirstAtomTag`は、元の生証拠の構成子列の先頭原子的タグを`Nat`へ送る**raw証拠観測**である。`chain`に対しては左側の証拠をたどり、真正の`compLeft/compRight`と`whiskerLeft/whiskerRight`、13Dの`strict/tripleLeft/tripleRight`などを別々の有限値で識別する。等式があったと仮定した場合に`congrArg`で非依存型`Nat`の矛盾を導くので、元の依存添字を不正に消去する必要がない。

修正はこの2種類のタグ定義と該当非等号の証明本体、`#print axioms`監査追加に限る。元の三連12D構成、独立13D/14D生成元・仮定を弱めず、最終exact-source CIはすべてSUCCESS、`sorryAx`なし。

## 7. 次の研究境界

Qi v5.29では、今回の13D局所比較が任意の12D経路の前後貼り合わせ、および元v5.27の左右文脈作用とどの条件で自然に整合するかを探る。新たな14D coherenceを追加する場合も、元のType値証拠と旧v5.23選択14Dを保持し、互換条件、obstruction、別presentationのauthorityを明示する。

今回の結果は**元の第七セル構文の厳密結合則、旧raw第十一〜十四セル証拠のEq、全高次coherenceの完成を主張しない。** append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
