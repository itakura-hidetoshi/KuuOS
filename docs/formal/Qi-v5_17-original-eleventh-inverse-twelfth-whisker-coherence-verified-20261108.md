# Qi v5.17 — 真正第十一セルの左右逆元往復と最小第十二セル・whiskering整合

## 0. 正本・検証証跡

2026年11月8日 JST。唯一のcanonical repositoryは `itakura-hidetoshi/KuuOS`、branchは `main`。
Qi v5.16の形式証明を一切変更せず、独立第十二セルモジュールを追加した。

| 項目 | exact-source確定値 |
|---|---|
| 定理PR | [#3286](https://github.com/itakura-hidetoshi/KuuOS/pull/3286) **MERGED** |
| 定理squash | `580f757b87f2857cc83f08f25d01d715b78e3e05` |
| exact-source CI | [#42422300901](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42422300901) **SUCCESS** |
| Strict Lean | **10,330 / 10,330 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理監査 | 新規28宣言の`#print axioms`：公理不要または`propext`／`Classical.choice`／`Quot.sound`のみ |
| `sorryAx` | なし |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `0538a76081132a1ce6fa2ddac44cdfd07d900d13` |
| CI test-merge | `695a5175cdcbd9733b8b035d26e5422c2c012b49` |
| 一致Git tree | **`ad73b9aed37b9e06d76401313d3b339ec7f1ef7c`** |
| Lean | v4.30.0-rc2 |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開Lean集約 | `KuuOSFormal`、root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ維持 |

[新規Lean 4全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ExchangeInverseMinimalTwelfthV5_17.lean)
および[公開aggregate](../../formal/KuuOSFormal.lean)が検証対象である。
今回の定理PRは独立Leanモジュール745行＋集約import1行のみで、既存定理ファイル・物理source・旧証拠構成子はすべて無変更。

## 1. 型付き十一セル逆元往復の二方向

v5.16で導入した唯一の新規第十一セルの交換原始を

\[
\Xi\colon\Theta_{EU}\Longrightarrow\Theta_{UE}
\]

とする。`Theta`は元のQi v5.15で生成された二つの**生の第十セル型付き証拠**であり、
両者のstrict raw Eqは以前から偽である。

第十一セルでの反転・連鎖により、真正の左右往復

\[
\begin{aligned}
L_R&=\Xi\star\Xi^{-1}
  \colon\Theta_{EU}\Longrightarrow\Theta_{EU},\\
L_L&=\Xi^{-1}\star\Xi
  \colon\Theta_{UE}\Longrightarrow\Theta_{UE}
\end{aligned}
\]

をそれぞれ構成した。

対応Lean API：

- `twelfthOriginalExchangeRightLoop`／`twelfthOriginalExchangeLeftLoop`
- `twelfthOriginalExchangeRightRawGap`／`twelfthOriginalExchangeLeftRawGap`

どちらのループも各元端点における`mixedExchangeUnitElevenCell_refl`とは**raw 11Dで厳密に異なる**。第十二セルを設けてもそのraw Eqは書換えない。

## 2. 最小の独立第十二セルpresentation

`MixedExchangeInverseTwelveCell`は、同じ元の第十セル始終点 `xi zeta` の**二つの生第十一セル値** `H K` を比較する、新たな`Type`値文法である。

追加したprimitiveは四種類に限定する。

1. `cancelExchangeRight`：`L_R`と右端点の第十一反射証拠を比較。
2. `cancelExchangeLeft`：`L_L`と左端点の第十一反射証拠を比較。
3. `whiskerLeftStrict`：`whiskerLeft before (strict rfl)`と、whisker済みの元第十セル証拠の`strict rfl`を比較。
4. `whiskerRightStrict`：右whiskerについて同じ整合を要求。

その他十五構成子は、strict／reverse／chainおよび既存第十一セルの反転・連鎖・十セル反転と合成・九セル文脈・左右whiskering・inverse/composite文脈への**型付き閉包**だけである。計十九構成子。

選択されたSetoid `mixedExchangeInverseTwelfthSetoid` と商`mixedExchangeInverseTwelfthClass`について、比較可能性とクラス一致の必要十分条件を証明した。
元の左右往復は選択商では対応する反射と一致するが、raw eleventh witnessの同一性には戻らない。

`mixedExchangeInverseTwelfthClass_noRawRetraction`により、この選択商から**全生第十一セル証拠への左逆復元**は存在しない。

## 3. 左右whiskeringの本物の局所critical pair

`twelfthLeftWhiskerStrictCritical`と`twelfthRightWhiskerStrictCritical`は、いずれも以下を同時に示す：

- whiskerした第十一反射の**raw証拠**と、whisker済み第十セル上の新しい反射証拠はstrict Eqで異なる。
- しかし二つの証拠は新設の**型付き第十二セル**で比較できる。

既存の第十二セル比較をwhiskerした後で、これらのstrict整合generatorを連鎖することにより

- `twelfthLeftWhiskeredCancellation`
- `twelfthRightWhiskeredCancellation`

を構成した。これは単なる同型視や下位証拠の書換えではない。

**未解決境界：**「左whiskerしてから右」と「右whiskerしてから左」は、下位のraw ninth/eighth/ten証拠インデックスまで一致するとは限らない。二重whiskerのinterchangerを無条件に設けると、未証明の局所compatibilityを捨てるため、**今回は導入しない**。

## 4. 生第十一セル履歴に残る独立不変量

`eleventhTenSymmEventCount`を元の第十一セル証拠について構造再帰で定義する。

\[
N_{\mathrm{tenSymm}}(H)
=\#\{\text{original eleven-cell tenSymm wrappers in }H\}.
\]

単位・反転・whiskeringによる再包囲は元の構成子の出現回数を適切に保存し、`tenSymm`だけが1を加える。連鎖・合成の下では加法的である。

`mixedExchangeInverseTwelveCell_preservesTenSymmCount` は**全十九第十二セル構成子**を構造帰納法で覆い、選択比較

\[
\Omega\colon H\Rrightarrow K
\quad\Longrightarrow\quad
N_{\mathrm{tenSymm}}(H)=N_{\mathrm{tenSymm}}(K)
\]

を形式証明する。

さらに `mixedExchangeInverseTwelfthTenSymmCount` が本物の`Quotient.lift`であり、代表元評価式も検証された。

特に元の実在する十セルcritical witness `pmLeftUnitCriticalExchangeThenUnit` について、
`twelfthOriginalTenSymmStrictLoop`と対応する第十一反射の値は

\[
\boxed{
N_{\mathrm{tenSymm}}
\bigl(\mathrm{tenSymm}(\mathrm{strict\;rfl})\bigr)=1,
\qquad
N_{\mathrm{tenSymm}}(\mathrm{strict\;rfl})=0.
}
\]

したがって二つは新しい第十二セルによって**比較不能**であり、商のクラスも異なる。
`mixedExchangeInverseTwelveCell_notGloballyThin`により、選択第十二セルはglobal thinにならない。

この非比較は**今回選択した第十二セル文法に相対的**であり、任意の高次圏における一般不可能性を宣言するものではない。

## 5. 元の証拠とauthority境界

`mixedExchangeInverseTwelveCell_retainsOriginalTenthObstructions`は、v5.16の本物の十セル往復で残った独立計数 `(2,0)`対`(0,0)`、`(0,2)`対`(0,0)` に基づく**旧第十一セル比較の不存在**を保存する。第十二セルの追加は旧十一セル構成子を増やさない。

`pentagonActualOriginalExchangeTwelfthCompletion`は、任意の真正P77 final raw indexで、元GK5CG長短五セルType値を供給し、新たな十二セル存在と、元`PentagonAdjoinedSixCellEqualityInterpreter`不存在を同時に構成する。

保存原則：**append-only／tighten-only／overwrite-forbidden／same-root**。新presentationでの比較を旧raw証拠の同一性、普遍的coherence、higher authorityの昇格へ読み替えない。

## 6. 次段Qi v5.18

研究課題は、元のwhiskering済みraw境界を忘れずに

\[
(\mathrm{left}\circ\mathrm{right})\quad\text{対}\quad
(\mathrm{right}\circ\mathrm{left})
\]

の**局所インデックス付きinterchanger候補**を構成することである。
まず十・十一セル境界が一致する場合と一致しない場合を分け、十一セル／十二セルの二経路のcritical overlapを調べる。必要な比較だけを局所追加し、より低次の元証拠、保存観測量、残存obstructionを継続追跡する。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊。Apache-2.0。
