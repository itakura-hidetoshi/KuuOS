# Qi v5.30 — 真正左右第七セル文脈の交換比較・13D自然性cube・選択15D単位coherence

2026年11月8日 JST。canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.29 の定理PR #3315、公開import #3316、正式記録 #3317 のMERGED正本を継承した。
元F55/P77/GK5CG、元6D〜14D証拠Type値、v5.23〜v5.29の選択presentationを変更しない。

## 1. 完了した正本・検証記録

| 項目 | GitHub MCPとexact-source成果物で確認済み |
|---|---|
| v5.30 定理PR | [#3318](https://github.com/itakura-hidetoshi/KuuOS/pull/3318) **MERGED** |
| 定理source HEAD | `bf4d4bb188de486bfc057bd39ce0070a45d84a2b` |
| 定理test-merge | `c787035eb429ee5af18581a5c03171681a6768b7` |
| 定理squash main | `712e41d936b85bf0232b590a1fda965b2a36194c` |
| 定理source／test-merge／squash Git tree | **`83579f1c2e25ba859abc78795b5280c2e2f84495` 完全一致** |
| 定理exact-source CI | [#42449687383](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42449687383) **completed/SUCCESS** |
| Scoped Strict Lean | **9,082 / 9,082 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 新規宣言公理依存監査 | **33/33**：公理不要23件・標準公理のみ10件 |
| 使用する標準公理 | `propext`、`Quot.sound` のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 変更Lean error/warning | **0/0** |
| 定理差分 | 新規Lean 719行追加、既存ファイル削除・変更0 |
| 公開集約PR | [#3319](https://github.com/itakura-hidetoshi/KuuOS/pull/3319) **MERGED** |
| 公開集約source HEAD | `53d983135f0f82cd7dd7aeec4d67094314e0c66e` |
| 公開集約test-merge | `6ddb7a475ed3ee208f140639b1c49d4ba6fd8024` |
| 公開集約squash main | `487c5d4c4853db40e10475efcc6e1248f9ef52e2` |
| 公開集約source／test-merge／squash Git tree | **`ae0b9760b48b065d224fc022154ac57aacaa03ea` 完全一致** |
| 公開集約exact-source CI | [#42450021010](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42450021010) **completed/SUCCESS** |
| KuuOSFormal全体 Strict Lean | **10,343 / 10,343 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開集約差分 | `formal/KuuOSFormal.lean`へのimport1行、削除0 |
| 公開root／保護PR | root107維持、#1558 Draft/OPEN/未マージ |
| toolchain | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedContextNaturalityCubeV5_30.lean)。

定理CIの`lean-formal/receipt.json`は `status=passed`、`return_code=0`、
`git_sha=c787035eb429ee5af18581a5c03171681a6768b7`、
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77MixedContextNaturalityCubeV5_30` を記録。
ログ末尾は `Build completed successfully (9082 jobs)`。
公開集約側の`receipt.json`も`status=passed`、`return_code=0`、
`git_sha=6ddb7a475ed3ee208f140639b1c49d4ba6fd8024`、
`build KuuOSFormal`、`Build completed successfully (10343 jobs)`を記録。
対象限定9,082と公開集約10,343は別の検証範囲であり、混同しない。

## 2. 真正左右文脈の異なる二順序

元第六セル境界の添字が整合する真正第七セル`before:b⇒c`、
`after:d⇒e`、元第十一セル証拠`F,G:c⇒d`と、
新選択第十二セル`P:F→G`を固定する。

生の`L_before(R_after(F))`と`R_after(L_before(F))`は
異なる元第十一セルの履歴を持ち、raw Eqを仮定できない。
`selectedMixedBoundaryBridge`は、v5.18の真正`FramedDoubleWhiskerTwelveCell.doubleWhisker`を
v5.25とv5.27の**二段previous**に保存し、次の第十二セル比較を生成する：

\[
\beta_F:L(R(F))\xRightarrow{12}R(L(F)).
\]

さらに`selectedMixedLeftAfterRight`と`selectedMixedRightAfterLeft`で
それぞれの真正文脈に沿った第十二セル証拠を作り、

\[
\begin{aligned}
U_P&=\beta_F\circ R(L(P)),\\
D_P&=L(R(P))\circ\beta_G
\end{aligned}
\]

を同じ**型付き**始終点`L(R(F))→R(L(G))`の第十二セル経路として実装した。

`selectedMixedRoutes_rawDistinct`は`selectedTwelfthFirstAtomTag`により
`U_P`の先頭原子が1、`D_P`の先頭原子が4であることから
**raw12D proof termsの非等号**を証明した。
一方`selectedMixedBoundary_quotientCompatible`は真正`β_F`から
選択12D端点**商上の等号**を導く。生証拠のEqとは別の主張である。

## 3. 独立選択第十三セルと旧証拠の保持

`SelectedMixedInterchangerThirteen`は独立の選択13D比較Type。
`inherited`はv5.29`SelectedContextualThirteen`のすべての証拠値を保持し、
`selectedMixedThirteen_inherited_injective`はraw証拠埋込みの単射を形式証明。

新規の局所生成元`mixed`は真正第七セル`before,after`、元第十一セルの
**同一第六セル境界**`F,G`、既存選択12D値`P`を厳密な添字として要求し、

\[
\boxed{I_P:U_P\Rrightarrow_{13}D_P}
\]

を選択比較として追加する。`strict/reverse/chain/prepend/append`および
元の型付き左右七セル`whiskerLeft/whiskerRight`を構文閉包する。
任意の旧13D比較のstrict equalityや旧v5.23生成元への自動降下を主張しない。

## 4. 真正13D比較を使う混合自然性square

さらにv5.29の実際の第十三セル比較`C:P⇒Q`を固定する。
`selectedMixedLeftAfterRightThirteen`／`selectedMixedRightAfterLeftThirteen`は
元の第七セル添字が一致する場合だけCを左右に輸送する。

これと二つの`I_P,I_Q`から、始終点`U_P⇒D_Q`が厳密に一致する二本の
真正第十三セル経路を構成する：

\[
\begin{aligned}
N_{\rm upper}&=(\beta_F\ast R(L(C)))\,;\, I_Q,\\
N_{\rm lower}&=I_P\,;\,(L(R(C))\ast\beta_G).
\end{aligned}
\]

`selectedMixedThirteenFirstAtomTag`は`N_upper`の先頭原子タグ6、
`N_lower`は1を返すため、
`selectedMixedNaturality_rawDistinct`は生13D非等号を証明。

新規`SelectedMixedNaturalityFourteen`の`criticalMixed`は
真正の局所条件を満たす場合だけ両経路の**選択14D比較**を構成。
`selectedMixedNaturality_conditionalCube`はその存在と生13D非等号を同時に証明する。
v5.29の14D証拠、および旧v5.23の元選択14D証拠はそれぞれ型付きで包含され、
両段の単射性まで形式証明。さらに選択14Dの真正左右七セル閉包を保持。

## 5. 選択第十五セルの局所単位coherenceとobstruction

同じ自然性14D証拠の前後に14D`strict`を貼り付ける二つの構文
`selectedMixedFourteenUnitPrepend`および`selectedMixedFourteenUnitAppend`を構成。
`selectedMixedFourteenFirstAtomTag`は先頭原子2と1を識別し、
`selectedMixedFourteenUnit_rawDistinct`は二本の生14D証拠の非等号を証明。

独立`SelectedMixedCoherenceFifteen`は、この**一種類の局所真正混合単位critical pair**
だけに`criticalUnit`を追加し、`strict/reverse/chain`による閉包を構成する。
`selectedMixedFifteen_conditionalUnitCube`は選択15D比較の存在と生14D非等号を同時に証明。
`selectedMixedFourteen_noRawEqualityInterpreter`、
`selectedMixedFifteen_noRawEqualityInterpreter`は、
選択高次比較をraw13D/14D Eqへ読み替える普遍的な解釈が不可能であることを示す。

旧v5.29の`HasOriginalTwelveEndpoints`は、旧v5.23真正12D証拠の
二段`previous`包含像に一致する**生値**を要求する必要条件。
混合下側経路はタグ4で、旧埋込みのタグ1と相容れない。
`selectedMixedRoutes_noOriginalEndpoints`が、この特定混合比較の
**旧raw12D起点への厳密liftが不能**であることを形式証明する。
しかし第十二セルの商上の弱い互換性までは失われない。
したがって「生Eq障害」と「商上互換性」は同時に成立する。

## 6. 成果のauthority境界と次段

今回の成果は**独立選択**13D・14D・15Dでの、
実在する第七セル文脈と元11D・選択12D/13D値に条件付けた局所比較である。
旧13D/14Dのraw Eq、元の14D比較の完全自然性、
任意の第十五セルtricategory coherence、全presentationのstrictification、
旧sourceへの全面的descentではない。

次段Qi v5.31：選択15D比較のさらに上の左右文脈作用、
異なる混合critical pairの多重貼り合わせ・非可換な経路履歴、
自然性の選択的商降下と残るobstructionを探索する。
append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
