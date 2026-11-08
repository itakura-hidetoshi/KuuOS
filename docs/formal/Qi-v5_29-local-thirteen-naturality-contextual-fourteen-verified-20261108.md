# Qi v5.29 — 局所第十三セルの前後貼り合わせ自然性、真正文脈閉包と旧第十四セルへの降下障害

2026年11月8日 JST。Canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.28定理 #3312・公開集約 #3313・正式記録 #3314 のMERGEDを継承。
元F55/P77/GK5CG、元6D〜14Dのすべての生証拠、v5.23/27/28の選択presentationは一切変更しない。

## 1. 正本・形式検証

| 項目 | GitHub MCPで検証した事実 |
|---|---|
| v5.29定理PR | [#3315](https://github.com/itakura-hidetoshi/KuuOS/pull/3315) **MERGED** |
| 定理source HEAD | `e7ac0e3105d9fd1980dedbdfda255e1b9108274e` |
| 定理test-merge | `43c293bb4dc07613a2830c05e0c2eecdde9de70d` |
| 定理squash main | `ccb5b0bc296695b05da83da6abba013458f41e53` |
| 上記三者のGit tree | **`84eef1c5120d532ec7ba1b219ac112211cf74926` 完全一致** |
| 定理exact-source CI | [#42448349862](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42448349862) **completed/SUCCESS** |
| Scoped Strict Lean | **9,081/9,081 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 新規宣言の公理監査 | **21/21**：15件公理不要、6件は標準`propext`のみ |
| sorryAx、新公理 | **なし／なし** |
| 変更Lean error/warning | **0/0** |
| 定理差分 | 新規Leanファイル1件、475行追加・削除0 |
| 公開集約PR | [#3316](https://github.com/itakura-hidetoshi/KuuOS/pull/3316) — 実行中、結果は追記 |
| 公開rootと保護PR | root107維持、#1558 Draft/OPEN/未マージ |

[Lean証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77LocalThirteenNaturalityV5_29.lean)。

証明検証はpinされたLean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`を使用。
Lean receipt (`lean-formal/receipt.json`) は `status=passed`、`return_code=0`、
`git_sha=43c293bb4dc07613a2830c05e0c2eecdde9de70d` を記録し、
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77LocalThirteenNaturalityV5_29`
が成功。検証ログ末尾は `Build completed successfully (9081 jobs)`。
新規21宣言の`#print axioms`に新公理・`sorryAx`はない。

## 2. 前後貼り合わせの二つの真正第十三セル経路

真正元第六セル境界が適合する`FramedEleven`の列`E,F,G,H`、
選択第十二セルの前方経路`A:E→F`、後方経路`B:G→H`、
平行第十二セル`P,Q:F→G`および局所第十三セル比較`C:P⇒Q`を固定する。

`selectedNaturalityDirect`は
```
append (prepend A C) B
```
であり、もう一つの`selectedNaturalityViaAssociators`は
```
associator A P B ; prepend A (append C B) ; reverse (associator A Q B)
```
である。両者の第十二セル境界は厳密に同じ
`((A.chain P).chain B)`と`((A.chain Q).chain B)`である。

一方、`selectedThirteenFirstAtomTag`による証拠構文の観測は
`Direct ↦ 7`、`ViaAssociators ↦ 8`で異なる。
`selectedNaturality_rawDistinct`が、この元Type値証拠の**生の非等号**を形式証明する。
この比較を自動のstrict化と解釈しない。

## 3. 真正第七セルの左右文脈による型付き閉包

別の独立した`SelectedContextualThirteen`を構成した。
`inherited`はv5.28の真正選択13D証拠を生値のまま保存し、単射性も形式証明。
追加`whiskerLeft/whiskerRight`はv5.27の真正第七セル文脈に従い、
**両端の元第六セル境界が厳密に一致する場合だけ**13D比較を型付きで移す。
`selectedContextual_leftEvidence/rightEvidence`で存在を証明。
非可換な構成順序の履歴をEqに潰さず、`strict/reverse/chain`も型付きで保存する。

## 4. 局所選択第十四セルの自然性square

別の`SelectedNaturalityFourteen`は、v5.28の選択14Dを`inherited`として保存し、
`tripleFourteenToNaturality`の単射性を証明。
旧v5.23の`SelectedCompositionFourteen`も
`originalFourteenToTriple`と`tripleFourteenToNaturality`の二段の包含で保持。
`oldFourteenToNaturality_injective`は生の旧14D証拠が区別可能なことを保証する。

新しい14D生成元は**実在する三連元第七セル文脈の局所2系列**に限定：
`localLeft`と`localRight`は、先の二つの前後貼り合わせ第十三セル経路を
独立選択の14Dで比較する。任意の13Dに対して未証明の自然性を付与しない。
選択された14Dにはさらに真正元七セル`whiskerLeft/whiskerRight`、
`strict/reverse/chain`の型付き閉包を設ける。
`selectedLocalLeft_naturality`と`selectedLocalRight_naturality`は
選択14Dの存在と生13Dの非等号を**同時に**証明する。

## 5. 新旧第十四セルの必要互換条件とobstruction

`HasOriginalTwelveEndpoints l r P Q`を、
元v5.23の`FramedDoubleWhiskerTwelveCell`の証拠値`U,V`が存在し、
二段の`previous`包含像が`P,Q`と**生のEq**で一致する、という条件として定義した。
これは旧選択14Dへ厳密に降下するための**必要条件**であって十分条件ではない。
`oldFourteen_hasOriginalEndpoints`は真正旧14Dの各証拠がこの条件を満たすと示す。

一方、v5.28の実在三連比較では元12D埋込みは先頭構成子タグ1、
左の`selectedLeftTripleInnerPasting`はタグ4、
右の`selectedRightTripleOuterPasting`はタグ9。
`selectedLeftTriple_noOldEndpoints`／`selectedRightTriple_noOldEndpoints`で
旧12Dからの**厳密な生値復元は不可能**と形式証明した。
これは商での同値を否定するものではなく、old proof Typeへの厳密なliftの障害である。

`selectedLocalLeft_noRawEqualityInterpreter`は、14D比較の存在から
異なる13D生値のEqを主張する任意の解釈が不可能であることを示す。

## 6. 成果の境界と次段

ここで示したのは**元の真正第七セル文脈と型付き12D証拠を条件とする選択13D/14Dの局所自然性**であり、
元のraw第十二〜十四セルのstrict Eq、任意13D比較の自然性、
完全な14D descent、全体的tricategory coherence、元証拠の自動復元ではない。

次のQi v5.30は、独立の左右文脈作用を重ねた混合square／cubeの
順序依存と、それらを比較する選択15Dの最小生成元の要否、
そして旧14Dの商レベルへの弱い互換条件（生値Eqとは区別）を検討する。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
