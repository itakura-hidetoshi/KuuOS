# Qi v5.19 — framed第十二セルのexact-fiber降下条件と非因子化障害

## 0. 正本・exact-source CIの独立再観測

2026年11月8日 JST。Repository `itakura-hidetoshi/KuuOS`、唯一のcanonical branch `main`。
元のF55/P77/GK5CG、独立第六〜第十二セルのraw Type値、全依存履歴を無変更のまま、
v5.18で追加したframed比較と真正の同一fiber第十二セルの間にある条件付き降下を形式化した。

| 項目 | 形式検証済み |
|---|---|
| 定理PR | [#3290](https://github.com/itakura-hidetoshi/KuuOS/pull/3290) MERGED |
| 定理squash | `9bc03722a611e07fb91fd7b30fcaf8ec0ce69b82` |
| exact-source CI | [#42428479556](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42428479556) SUCCESS |
| Strict Lean | **10,332 / 10,332 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規宣言の`#print axioms` | **41 / 41**（無公理33、標準公理のみ8） |
| 依存する公理 | 必要な宣言のみ`propext`、`Quot.sound`、`Classical.choice` |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `960f91cda415c99ae1e2e0314e9a3f46efa1fbc6` |
| 検証test-merge | `5fef35f719d4b5a5d8243d700f53c43bd397ced2` |
| source/test-merge Git tree | **`d0000649e17f5cfcb49443e5815478f46a465223` 完全一致** |
| 公開集約 | `KuuOSFormal`、root107維持 |
| Lean | v4.30.0-rc2 |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft／OPEN／未マージ維持 |

[Lean 4全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FramedExactFiberDescentV5_19.lean)。
実装は独立した新規Leanモジュール657行＋公開集約import 1行のみ。既存ソースはすべて保存。

## 1. 第十一セル証拠と生の下位境界を分離

`FramedElevenExactSpine W l r`は、元の`FramedEleven`から
最上位の生第十一セル証拠`H`だけを外し、元第六〜第十セルの
全ての依存したraw indexと元証拠を別の`Type`として保存する。
`framedElevenExactSpine`／`framedElevenSpinePack`で元packetを復元できることは
`framedElevenSpinePack_exact`で証明済み。

生のspine (S,T)について、真正の`S = T`があるときだけ

\[
\operatorname{transport}_{e}:
\mathrm{ElevenWitness}(S)\longrightarrow\mathrm{ElevenWitness}(T)
\]

を`framedElevenSpineTransport`で構成する。
これはLeanの等式帰納法に基づく本当の型付き輸送であり、
v5.18の第八セルassociatorの存在を`Eq`へ昇格させるものではない。

## 2. exact-fiber降下の必要十分条件

`FramedExactSpineTwelfth`は、下位spineの真正な等式と、輸送された
生第十一セル証拠間の**元v5.17第十二セル証拠**を保持する依存structureである。

`FramedExactFiberTwelfthLift F G`の存在は

\[
\boxed{
\exists e:S(F)=S(G),\quad
\mathrm{MixedExchangeInverseTwelveCell}
  (\operatorname{transport}_{e}H_F,H_G).
}
\]

これを、新しい原始を含まない独立文法
`FramedInheritedTwelfth`（strict／previous／reverse／chain、計4構成子）
と比較した。`previous`は既存の元v5.17第十二セル証拠を丸ごと持つ。

`framedInheritedTwelfth_iff_exactFiber`により、**このinherited-only文法に限って**
新たな型付き比較の存在と上記exact-fiber条件が同値であると形式証明した。
`framedExactFiberTransport_reverse`／`framedExactFiberTransport_chain`で
等式輸送後の反転・連鎖を元第十二セル構成子から構成する。

特に指定した元同一fiberの2つの第十一セル証拠`H,K`については

\[
\boxed{
\mathrm{InheritedFramedTwelve}(\mathrm{frame}(H),\mathrm{frame}(K))
\quad\Longleftrightarrow\quad
\mathrm{OriginalTwelve}(H,K)\ \text{がinhabited}.
}
\]

対応する`framedExactFiberLift_onOriginal_iff`と
`framedInheritedTwelfth_onOriginal_iff`は、元Typeを改変せず証明している。
**注意：完全なv5.18 framed第十二セル比較の全てがexact-fiberへ降下するとは主張していない。**

## 3. 本物の二重whiskeringは境界比較可能だがexact一致しない

v5.18の元二重whiskering
`doubleWhiskerLeftAfterRightFrame`／`doubleWhiskerRightAfterLeftFrame`
には、第七セルrawの括弧付けの相違がある。
このsource/targetの両方には元の`EightCell.associate`による真正第八セル比較が存在する。

しかし、元第十セルのraw Bool履歴は

\[
T_L=[\mathrm{left},\mathrm{right}]\mathbin{+\!+}T,
\qquad
T_R=[\mathrm{right},\mathrm{left}]\mathbin{+\!+}T.
\]

したがって`doubleWhiskerExactSpineGap`は、**全ての元の型付き二重whiskering文脈**
において生spineの厳密な等式が成立しないことを証明する。
`doubleWhiskerEightCompatible_notExactSpine`は、真正第八セルの
2つのcompatibleな境界証拠と、spineのstrict不一致を同時に構成する。

元のv5.16 `exchangeUnit`を使う具体的な元critical pairでは

`originalDoubleWhisker_noExactFiberLift`／`originalDoubleWhisker_notInherited`
がexact輸送と旧比較だけの非存在を証明する一方、
v5.18の新`doubleWhisker`生成元ではframed比較が存在する。
`framedDoubleWhisker_strictBeyondExact`は、この選択framed商の拡大が
**旧same-fiber第十二セルより本当に強い**ことを証明する。
`framedDoubleWhisker_noUniversalExactTransport`は全比較の普遍的同一fiber化を排除する。

## 4. 完全spine観測の可降下性と商写像の非単射性

旧比較のみで閉じた`framedInheritedTwelfthSetoid`と`framedInheritedTwelfthClass`を構成。
`framedInheritedTwelfth_preservesSpine`から、
完全なraw下位添字を`Type`値で読み出す

`framedInheritedSpineObserver`

を真正の`Quotient.lift`で構成した。
これは新しいprimitiveのない商では完全spine観測が正しく降下することを示す。

一方、`framedInheritedToFullQuotient`は、この旧商から
v5.18の新しい`FramedDoubleWhiskerTwelveCell`選択商への
自然な商写像である。元critical pairは新商で一致するが、
旧商ではspine観測が異なる。従って

\[
\boxed{
\neg\operatorname{Injective}
  (Q_{\mathrm{inherited}}\to Q_{\mathrm{framed}})
}
\]

を`framedInheritedToFullQuotient_notInjective`でLean証明した。

さらに`framedExactSpine_noFactorThroughFullQuotient`は、
**旧商の完全spine観測が新商を経由して因子化できない**ことを明示する。
`framedInheritedToFullQuotient_noLeftInverse`で全左逆復元の不存在も示した。

この非因子化がv5.19の中心的なobstructionである：
高次比較の追加によって新商へ降下した情報と、
もはや降下できない元source証拠履歴を区別する。

## 5. 残存障害、元P77特殊化、authority境界

元v5.17の`tenSymm(strict rfl)`と`strict rfl`の1対0障害は、
`framedExactFiber_retainsTenSymmObstruction`で保持する。
新しい商を構成しても無条件のglobal thinnessを導いていない。

`pentagonActualExactFiberObstruction`は、**任意の元P77 final raw index**の
真正GK5CG long/short五セルType値を使い、framed比較の存在と、
exact-fiber liftの不存在、および元`PentagonAdjoinedSixCellEqualityInterpreter`
不存在を同時に形式化する。元のF55/P77/GK5CG sourceの証拠を代替構成していない。

運用原則：append-only／tighten-only／overwrite-forbidden／same-root。
独立空・strict空・選択商を無条件に同一視せず、
obstructionとauthorityの違いを明示する。

## 6. 初回CIでのLean 4記法・型エラーの学習と修正

初回CI [#42427708052](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42427708052)：
等式`S=T`は`Prop`であり、`Sigma`の`Type`側のindexとして
直接使用した記述に型不一致。さらに元P77特殊化に括弧余剰があった。
命題と仮定を変更せず、`alignment : S=T`とその証拠に依存する
`comparison : ...`をフィールドに持つ`FramedExactSpineTwelfth`へ改めた。

二回目CI [#42428047003](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42428047003)：
隣接した2つのLean文書コメントによる構文解析エラーのみ。
全41宣言の本体と公理依存が監査ログに現れる一方、
構文エラーが残るため正式検証とは認めず、余分なコメントを除去。
三回目CI [#42428479556](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42428479556)で
全10,332 LeanジョブとGovernance30ジョブがSUCCESS。
新41宣言の依存に`sorryAx`・追加非標準公理は存在しない。

## 7. 次段Qi v5.20

次はexact-equalityの条件を緩めずに、元の八セルassociatorを
第九／第十／第十一セルの具体的な型付きtransportで橋渡しできる局所条件と、
その条件が不十分な場合の新しいobstructionを分類する。
新framed比較の存在だけから`Eq`や下位の旧source authorityを
導くことなく、各presentationの証拠を独立に保持する。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊。Apache-2.0。
