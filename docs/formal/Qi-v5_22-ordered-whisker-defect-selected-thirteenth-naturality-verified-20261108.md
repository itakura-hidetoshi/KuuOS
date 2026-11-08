# Qi v5.22 — 順序付きwhiskering defectと選択第十三セルの自然性square

## 0. 正本・exact-source Lean 4独立再観測

2026年11月8日 JST。唯一のcanonical repository `itakura-hidetoshi/KuuOS`、
branch `main`。Qi v5.21の定理PR #3294・正式記録PR #3295をともにMERGED済みの
`dc2c7154c9b40d42ffe39b73ae2e9d69cba4949f`から継承。
真正元F55/P77/GK5CG、第六〜第十二セルの全raw Type・元の証拠履歴・元の
数値不変量・独立KuuOSStrictを一切変更していない。

| 項目 | 独立確認済み |
|---|---|
| 定理PR | [#3296](https://github.com/itakura-hidetoshi/KuuOS/pull/3296) **MERGED** |
| source HEAD | `c5cd386253aebc3699d4ed34f7ec4600b28a8099` |
| test-merge HEAD | `27ca6a0c508206b6faa2407bef0153cd82ea6c3f` |
| squash / theorem main | `6b5afe078c550ea2766acfef8c010b7d77dff644` |
| source/test-merge/squash Git tree | **`7cdb4b33956c81584b532a67160ee7d5f3131cb7` 完全一致** |
| exact-source CI | [#42433184371](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42433184371) **SUCCESS** |
| Strict Lean | **10,335 / 10,335 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規 `#print axioms` | **26 / 26**（公理不要14・標準公理のみ12） |
| 依存する標準公理 | 必要な宣言だけ`propext`・`Quot.sound` |
| `sorryAx` / 非標準新公理 | **なし／なし** |
| 変更Lean warning/error | **0 / 0** |
| 追加範囲 | 新規Leanモジュール＋公開集約import一行、既存ソース削除0 |
| Lean/mathlib | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root／保護PR | `KuuOSFormal` root107、#1558 Draft/OPEN/未マージ維持 |

[Lean 4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77OrderedWhiskerDefectNaturalityV5_22.lean)。

## 1. 順序付き履歴の真正defect証明書

元第十セル `MixedUnitAssocTenCell`の生の順序付きBool履歴
`mixedTenWhiskerRawTrace`を保持する。
新しい `OrderedWhiskerDefect(source,target)` は、
`whiskerPrefix : List Bool`と真正等式
`exact_target : target = whiskerPrefix ++ source`を持つ別Typeの証明書。

二つの実際のdefect
`A : OrderedWhiskerDefect(a,b)`、
`B : OrderedWhiskerDefect(b,c)`の連結は

\[
\boxed{
\operatorname{prefix}(B\circ A)
  =\operatorname{prefix}(B)\mathbin{+\!+}\operatorname{prefix}(A)
}
\]

という**後から適用した操作の前置**順序になる。
`orderedWhiskerDefectId`、
`orderedWhiskerDefectComp`、
`orderedWhiskerDefectComp_prefix`、
`orderedWhiskerDefect_length`を構成・証明。
`rw`で依存した証明書そのもののindexを変えることを避け、
`congrArg`により型を保ったままリスト等式を合成する。

元の真正左／右whiskeringでは

\[
\begin{aligned}
\operatorname{Trace}_{10}(L(\xi))
 &= [\mathrm{false}]\mathbin{+\!+}\operatorname{Trace}_{10}(\xi),\\
\operatorname{Trace}_{10}(R(\xi))
 &= [\mathrm{true}]\mathbin{+\!+}\operatorname{Trace}_{10}(\xi).
\end{aligned}
\]

二重適用した真正元第十セルでは

\[
\boxed{
\begin{aligned}
\operatorname{Trace}_{10}(L(R(\xi)))
  &= [0,1]\mathbin{+\!+}T,\\
\operatorname{Trace}_{10}(R(L(\xi)))
  &= [1,0]\mathbin{+\!+}T.
\end{aligned}
}
\]

`doubleWhiskerDefect_orderedValues`はこの厳密な生履歴を証明し、
`doubleWhiskerDefect_notCommutative`で**順序列の非等号**を証明。
一方、長さはともに`2+T.length`で、
`doubleWhiskerDefect_lengthCollision`は**同じNat計数では
左右順序を区別できない**ことを明示する。
`doubleWhiskerDefect_actualFrameOrder`はこれを実元第十一セル
framed packetに接続する。traceは商で消去しない。

## 2. 元第十二セルの両方向の真正二重whiskering

任意の**旧v5.17実在第十二セル証拠**

\[
T : \mathrm{MixedExchangeInverseTwelveCell}(H,K)
\]

と、型付き第七セル文脈`before,after`を入力する。
旧第十二セル自体が持つ真正`whiskerLeft`／
`whiskerRight`原始だけから、二つの別fiberの型付き証拠を構成：

`originalTwelfthRightThenLeft` =
`whiskerLeft before (whiskerRight T after)`、

`originalTwelfthLeftThenRight` =
`whiskerRight (whiskerLeft before T) after`。

この両者は**同じ元旧十二セルTypeの平行証拠ではない**。
元第七〜第十一セルの括弧付けと元十セル履歴が違うので、
暗黙のEq-rec・証拠捏造・元の証拠型の変更を行わない。

各々を元v5.18 `FramedEleven`へpackし、
`framedTwelfthRightThenLeft`／
`framedTwelfthLeftThenRight`で
既存`FramedDoubleWhiskerTwelveCell.previous`へ移す。

## 3. 真正framed自然性squareと二つの非同一12D経路

旧第十二セル`T:H⇒K`の各二重whiskeringと、
v5.18の真正`doubleWhisker`を四辺に置く。
次の2つのframed第十二セル合成証拠が、
**同じ始終点**を正確に持つ。

\[
\begin{aligned}
P_{\mathrm{upper}} &: L(R(H))
 \xRightarrow{\mathrm{old}(T)} L(R(K))
 \xRightarrow{\mathrm{doubleWhisker}(K)} R(L(K)),\\
P_{\mathrm{lower}} &: L(R(H))
 \xRightarrow{\mathrm{doubleWhisker}(H)} R(L(H))
 \xRightarrow{\mathrm{old}(T)} R(L(K)).
\end{aligned}
\]

`framedWhiskerSquareUpperRoute`と
`framedWhiskerSquareLowerRoute`を
元の真正型付き構成子だけで実装した。

`framedWhiskerSquareRoutes_rawDistinct`により
\(P_{\mathrm{upper}}\ne P_{\mathrm{lower}}\)を
**旧framed十二セルの生構文として**証明。
同一framed端点は生十二セル証明値の一致を意味しない。

さらに`framedWhiskerSquare_noInheritedDiagonal`は、
任意の元第十一セル`H,K`に対し、

\[
\boxed{
\neg\operatorname{Nonempty}\!
\left(\mathrm{FramedInheritedTwelfth}
  (L(R(H)),R(L(K)))\right)
}
\]

を、元の完全spine観測と互いに異なる`[0,1]`対`[1,0]`traceから
証明した。旧同一fiber第十二セルによる対角比較は
**旧第十二セル証拠`T`が存在しても成立しない**。
元第八セルsource/targetの真正`EightCell.associate`比較は
この障害とは独立に存在する。

## 4. 新しい選択第十三セルの最小生成元

新しい別presentation
`SelectedWhiskerNaturalityThirteen`を定義。
**新規局所生成元は`naturality`一種類のみ**で、
全元第十二セル`T`と文脈`before/after`から
\(P_{\mathrm{upper}}\Rrightarrow P_{\mathrm{lower}}\)
を生成する。ほかは`strict`・`reverse`・`chain`という
形式的比較閉包だけ（計四構成子）。

`selectedWhiskerNaturality_relativeNecessity`は、
新選択13D比較の存在と、元framed12Dの**raw非等号**を同時に証明。
`selectedWhiskerNaturality_boundaryAndObstruction`は
元第八セルの両端の真正compatibility、13D選択比較の存在、
旧第十二セル対角比較の不存在を同時に与える。

`originalExchangeRightCancellationThirteenCompletion`では、
実在する元v5.17
`MixedExchangeInverseTwelveCell.cancelExchangeRight`
（十一セル逆元往復から反射への**非自明**な真正12D比較）を使い、
13D生成元が本当にinhabitedであることを示す。

`selectedWhiskerNaturality_noRawEqualityInterpreter`により、
新13D比較のすべてを元のframed第十二セル**厳密Eq**に送る
万能な解釈関数は存在しないとLean4で証明。

**注意：これは選択13D presentationへの局所比較の追加であって、
元F55/P77/GK5CGに第十三セルがもともと存在した証明でも、
任意の旧高次coherence／thinness／全商からのraw履歴復元でもない。**

## 5. 初回・第2回Lean記法エラーの構造的修正

初回CI [#42432518822](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42432518822)：
`prefix`はLean4の記法宣言用予約語であり、structure field名に直接
使用するとパーサが失敗し、下流で未知fieldや`sorryAx`診断が連鎖した。
元定理を弱めず、`whiskerPrefix`へ名前を統一した。

第2回CI [#42432813355](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42432813355)：
`rw [A.exact_target]`が依存した`B : OrderedWhiskerDefect b c`の
添字`b`まで書換えようとして、不正なmotiveを生成した。
`rw [D.exact_target]`も`D`のindex依存に同様の問題。
`congrArg`を用いて必要な`List Bool`等式だけを作用させ、
元の依存証明書の型を不変に保つ修正を行った。

第3回CI #42433184371は全10,335 Leanジョブと
Governance30ジョブSUCCESS。全26宣言の公理監査は標準だけで
`sorryAx`なし。従って失敗段階の`sorryAx`表示は
未解決構文・型エラーの診断であり、新しい公理による穴埋めではない。

## 6. 数学的authority境界と次段階

Qi v5.22は、元証拠の順序付きdefect、非同一12D自然性経路、
選択13D最小比較の存在を切り分けた。
第八セルcompatibleから旧fiber Eqを導かず、
`FramedInheritedTwelfth`と`FramedDoubleWhiskerTwelveCell`、
新`SelectedWhiskerNaturalityThirteen`の三つのauthorityを混同しない。

**Qi v5.23の候補：** 新13D自然性の
`strict/reverse/chain`を越えた、元第十二セルの合成との
互換性・二重whiskeringの3つ以上の文脈を含む
critical cube／選択14D obstructionの構成。
元Typeの保存、局所可降下性、商情報損失を引き続き区別する。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、固定Lean/mathlib pin、保護PR #1558を変更しない。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
