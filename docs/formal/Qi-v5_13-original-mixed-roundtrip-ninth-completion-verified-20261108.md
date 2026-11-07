# Qi v5.13 — 元mixedResidue往復・恒等九セル最小補完と残余自由合成障害

## 0. 正本・exact-source検証

2026年11月8日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.12の真正九セルP往復最小補完と、元のF55/P77/GK5CG・独立七セル／八セル証拠を保持する。

| 項目 | 検証済み状態 |
|---|---|
| 定理PR | [#3278](https://github.com/itakura-hidetoshi/KuuOS/pull/3278) **MERGED** |
| 定理squash | `6907e22a7c6a766fc6b63b2a69e92eea4f088d2c` |
| exact-source CI | [#42396353401](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42396353401) **SUCCESS** |
| Strict Lean | **10,326 / 10,326 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 47宣言の`#print axioms` | `propext`／`Classical.choice`／`Quot.sound`または公理不要 |
| `sorryAx` | なし |
| 変更Lean warning/error | **0 / 0** |
| source HEAD | `da11640fe2550c00ed40a04a4199d08752c546e8` |
| test-merge HEAD | `203c3785f150131b5f9ed849193ff6ce9dde177f` |
| source/test-merge Git tree | `270ba51ded710e6e44c7bd262e0cc0b84101b6a2` **完全一致** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 / root | `KuuOSFormal` / 107維持 |
| 保護PR #1558 | Draft／OPEN／未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedRoundtripUnitMinimalNinthCompletionV5_13.lean) · [前段Qi v5.12正式証明記録](Qi-v5_12-original-pentagon-roundtrip-unit-ninth-completion-verified-20261107.md)

## 1. 真正M往復の厳密な障害から独立九セル補完へ

前段Qi v5.12の元`SevenRewrite`二端点が一致する生の第八比較

```lean
ninthMixedRoundtrip l r
ninthMixedReflexive l r
```

は、元`mixedResidue`生成元の出現回数が **2対0** で区別できる。前段では全`PentagonCancelNineCell`構成子がM回数を保存するため、これらの間の**旧九セル比較の不存在**を形式証明済みである。

今回は、旧九セル文法を変更せず、独立の新Type

```lean
MixedCancelNineCell W l r q q'
```

にただ一種類の真正な原始比較

```lean
MixedCancelNineCell.cancelMixed
```

を構成。その添字は上記の元八セル二証明値そのものである。全既存`PentagonCancelNineCell`比較は`previous`で保持し、向き反転、連鎖、八セル比較の逆向き・合成・whisker・逆文脈の型付き閉包だけを許可した。

`mixedCancelNineCell_strictlyNew` は新比較の存在・旧比較不存在・元生八セルstrict Eq不存在を一つの定理として証明する。旧九セルや元strict Eqへの普遍的解釈は`mixedCancelNineCell_noPreviousInterpreter`と`mixedCancelNineCell_noRawEqualityInterpreter`で反証した。

これは**選択された独立の新九セルpresentationの存在**を示すものであり、元F55/P77/GK5CGに最初から存在するcanonical九セルを発見した、あるいは元八セルを厳密に等置した、という主張ではない。

## 2. 選択商の厳密な粗化と観測量の降下

`mixedCancelNinthSetoid`と`mixedCancelNinthClass`を真正な元八セル証拠Typeの上に定義した。旧九セル商の等しい元証拠は新九セル商でも等しくなる（`pentagonCancelNinthClass_descendsToMixedCancel`）。今回の真正M往復・反射対は旧商では別クラス、新商では同クラスとなる（`mixedCancelNinthClass_strictlyNew`）。

この新商から元の**全生八セル証拠**への左逆復元を否定する`mixedCancelNinthClass_noRawRetraction`も形式証明。

M回数は、この新たな具体的比較で

\[
N_M(\mathrm{MixedRoundtrip})=2,\qquad N_M(\mathrm{Reflexive})=0
\]

となるため、同じ新商で両者を同値にしたとき、元のM回数を忠実に降下させられない（`mixedCancelNinthClass_noMixedCountDescent`）。

しかし**PとMの回数の偶奇**は全新九セル構成子で保存される：

\[
\boxed{
N_P(q)\equiv N_P(q')\pmod2,\qquad
N_M(q)\equiv N_M(q')\pmod2.
}
\]

`mixedCancelNineCell_preservesPentagonParity`と`mixedCancelNineCell_preservesMixedParity`は全構成子の構造帰納法によるもので、単に代表元上の例を示したものではない。真正のNat値`Quotient.lift`で

```lean
mixedCancelNinthPentagonParity
mixedCancelNinthMixedParity
```

を構成し、双方の代表元計算も証明した。偶奇一致から任意の比較可能性を推論しない。

## 3. P/M両往復を補完しても残る、新たな整数値obstruction

独立の構文的観測量`ninthResidualChainCharge`を、元の自由八セルType上に定義した。

- 元の四重五角形一生成元`fourfoldPentagon`の寄与は\(-1\)。
- 元の旧`mixedResidue`イベントは1個につき\(-1\)。
- 自由八セル`chain`構成子は左右の値の和に **+2** を加える。
- 八セルの逆向きや単独文脈は値を保存し、`compositeContext`は加法的に振る舞う。

これにより、元P/Mの相殺という選択に対し、別個に自由合成の構文履歴を追跡できる。

全ての旧`FourfoldMixedNineCell`、前段`PentagonCancelNineCell`、今回`MixedCancelNineCell`の**全構成子**に関して、この整数が保存されることを三段の構造帰納法で証明：

```lean
fourfoldMixedNineCell_preservesResidualChainCharge
pentagonCancelNineCell_preservesResidualChainCharge
mixedCancelNineCell_preservesResidualChainCharge
```

したがってこの値も`mixedCancelNinthResidualCharge`として真正`Quotient.lift`で新商へ降下する。

ここで、元の反射八セル証拠\(\mathrm{Id}_8\)と、その自由八セル合成\(\mathrm{Id}_8;\mathrm{Id}_8\)は同じ**元七セル始終点**を持つにもかかわらず、

\[
\boxed{
\begin{aligned}
Q(\mathrm{Id}_8;\mathrm{Id}_8)&=2,\\
Q(\mathrm{Id}_8)&=0.
\end{aligned}}
\]

そのため`ninthDoubleReflexive_noMixedCancelComparison`によって、今回の新九セル文法には両者間の比較が**存在しない**と証明した。新商でも区別され（`ninthDoubleReflexive_distinctMixedCancelClass`）、任意並行八セルを比較可能とするglobal thinnessも成立しない（`mixedCancelNineCell_notGloballyThin`）。

重要な点：この反例はP/Mの出現回数がともに0であっても成立し、単なるP/M回数の保存からは見えない自由合成のobstructionである。既存の選択文法に関する否定定理であって、将来別に追加される高次比較の普遍的不存在ではない。

## 4. P往復消去 × M往復消去の真正高次critical overlap

真正元P77/GK5CGに由来する`fourfoldMixedResidueFirst l r`という元七セル履歴を持つ**同じ元七セル始終点**で、次の四つの元八セル証拠を構成した。

```text
Top     = (P-roundtrip) ⊗ (M-roundtrip)
MidP    = (P-reflexive) ⊗ (M-roundtrip)
MidM    = (P-roundtrip) ⊗ (M-reflexive)
Bottom  = (P-reflexive) ⊗ (M-reflexive)
```

上→MidPとMidM→下には、前段の真正`cancelPentagon`を`previous`として用いる。上→MidMとMidP→下は今回の新`cancelMixed`を真正合成文脈に入れたもの。

`originalDoubleCancellationLocalDiamond`によって四辺と完成経路の型付き九セル証拠を構成した。同じ端点の二経路

```lean
originalDoubleCancellationPThenM l r
originalDoubleCancellationMThenP l r
```

について、旧`cancelPentagon`を`true`、今回の`cancelMixed`を`false`とする生九セルイベントtraceを新規定義（旧P/M`interchange`はこの特定観測では記録しない）。

\[
\operatorname{trace}(P;M)=[\mathrm{Pcancel},\mathrm{Mcancel}],
\quad
\operatorname{trace}(M;P)=[\mathrm{Mcancel},\mathrm{Pcancel}].
\]

`originalDoubleCancellationTraceValues`は2つを定義上の等式として証明し、`originalDoubleCancellationRawNineGap`は元の**生九セル証明がstrict Eqではない**ことを形式証明した。

ここから「第十セル比較が存在しない」とは推論しない。二つの九セル証拠を接続する**独立した第十セルcoherence**が次の局所課題となる。

## 5. 元sourceを保持した真正P77 final raw indexへの特殊化

`pentagonActualMixedRoundtripNinthCompletion`は任意の元P77最終raw indexで、実際の`pentagonFinalConservativeLoop`、`pentagonLongConservativeFiveCell`、`pentagonShortConservativeFiveCell`を用いて今回の新比較のType値存在を構成する。

同時に、元の`¬ PentagonAdjoinedSixCellEqualityInterpreter`も保持し、既存F55/P77/GK5CG・六セル・七セル・八セル・旧九セルpresentationを一切変更しない。

## 6. Lean4検証・運用と次段階

今回の新規Leanモジュールは851行、47宣言を監査した。初回exact-source CIは再修正不要で**全30ジョブSUCCESS**（Strict Lean 10,326件）。新宣言の`sorryAx`なし、変更Lean warning/error 0/0、source/test-merge tree完全一致。

**Qi v5.14候補：** P/M両往復消去の二つの生九セル完成経路を、最小の独立した**第十セル比較**として構成し、その構造的保存量と新たなobstructionを分離する。元八セル・九セルのstrict Eqや任意並行高次証拠の全局thinnessは仮定しない。
