# Qi v5.12 — 真正五角形往復・恒等比較の最小九セル補完と高次critical overlap

## 0. 唯一の正本とexact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical `main`。Qi v5.11の独立 `FourfoldMixedNineCell` と元P77/GK5CG sourceの型付き証拠をそのまま継承する。

| 項目 | 検証済み状態 |
|---|---|
| 定理PR | [#3276](https://github.com/itakura-hidetoshi/KuuOS/pull/3276) **MERGED** |
| 定理squash | `14f39d2200e6e4e0f2c9ec6daba818086bd25063` |
| exact-source CI | [#42377984007](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42377984007) **SUCCESS** |
| Strict Lean | **10,325 / 10,325 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 47新規宣言の公理監査 | `propext`、`Classical.choice`、`Quot.sound`、または公理不要 |
| `sorryAx` | なし |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `9fe20a2a5cff0cec2123f53660d45349c52d4d2e` |
| test-merge HEAD | `6fdb4c0ee628efc417a18de955159b037c2d557d` |
| source/test-merge Git tree | **`5e9c968772c0821dd81187a6390c595f220e2d79`一致** |
| Lean/mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 / root | `KuuOSFormal` / **107維持** |
| 保護PR | #1558 Draft / OPEN / 未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77PentagonRoundtripUnitMinimalNinthCompletionV5_12.lean) · [Qi v5.11正式記録](Qi-v5_11-original-fourfold-mixed-minimal-ninth-completion-verified-20261107.md)。

## 1. 新規九セル比較が埋める正確なobstruction

元の八セル生成元 `PentagonAssocEightCell.fourfoldPentagon` に対して

```lean
ninthPentagonRoundtrip l r
ninthPentagonReflexive l r
```

は、元 `SevenRewrite` の始点・終点を等しくする**同一添字の異なる生の八セル証明値**である。

Qi v5.11の既証明定理 `ninthPentagonRoundtrip_noNineComparison` は、その二つを旧 `FourfoldMixedNineCell` では比較不能とした。理由は原始P-event数が2と0で異なるためである。

Qi v5.12は、独立presentation

```lean
PentagonCancelNineCell W l r q q'
```

へ次の**一種類だけ**の新たな原始生成元を追加する。

```lean
PentagonCancelNineCell.cancelPentagon
```

その添字はこの真正な二八セル証拠そのものである。全ての旧 `FourfoldMixedNineCell` の証拠は `previous` で保持し、反転・鎖・第八セルの反転・合成・左右whisker・逆文脈を型付き閉包として構成する。

`pentagonCancelNineCell_strictlyNew` は新しい比較の存在、旧文法での比較不存在、元八セルstrict Eqの不存在を同時に証明。`pentagonCancelNineCell_noPreviousInterpreter` と `pentagonCancelNineCell_noRawEqualityInterpreter` は旧比較・raw strict Eqへの普遍的解釈が存在しないことを明示する。旧ソースの証拠値は上書きしない。

## 2. 新九セル商の厳密な粗化と観測量の境界

新しい選択Setoid `pentagonCancelNinthSetoid` と商 `pentagonCancelNinthClass` を構成した。旧九セルで同値だった元八セル証拠は新商でも同値になる（`oldNinthClass_descendsToPentagonCancel`）。一方、五角形の往復と反射比較は、**旧九セル商では別クラス、新商では同一クラス**になる（`pentagonCancelNinthClass_strictlyNew`）。

元全八セル証拠への左逆復元の不存在も `pentagonCancelNinthClass_noRawRetraction` にて形式化した。

旧P出現回数の生観測は

\[
N_P(\mathrm{Roundtrip}_P)=2,\qquad N_P(\mathrm{Reflexive}_P)=0.
\]

新商で両者が同値になる以上、`pentagonCancelNinthClass_noPentagonCountDescent` によって、P出現回数そのものを忠実に商へ降下させることは不可能。

一方、全新九セル構成子について構造帰納法で

\[
\boxed{\ N_M(q)=N_M(q'),\qquad N_P(q)\equiv N_P(q')\pmod 2\ }
\]

を証明した。対応する定理は `pentagonCancelNineCell_preservesMixedCount` と `pentagonCancelNineCell_preservesPentagonParity`。

これは任意の二八セルの比較が可能という意味ではない。実際の `Quotient.lift` でNat値として定義した `pentagonCancelNinthMixedCount`、`pentagonCancelNinthPentagonParity` に対し、代表元上の計算も形式証明している。

## 3. 最小補完の後でも残る真正M-obstruction

元 `MixedResidueEightCell.mixedResidue` を用いて、

```lean
ninthMixedRoundtrip l r
ninthMixedReflexive l r
```

を同一の真正七セル端点で構成。原始M出現回数は前者が2、後者が0となる。

新しい九セルの**全構成子がM出現回数を保存**するため、

\[
\boxed{
\neg\operatorname{Nonempty}
\bigl(\mathrm{PentagonCancelNineCell}
(\mathrm{MixedRoundtrip},\mathrm{MixedReflexive})\bigr)
}
\]

を `ninthMixedRoundtrip_noPentagonCancelComparison` で証明。`ninthMixedRoundtrip_distinctCancelClass` によって新商でも両者は非同値。`pentagonCancelNineCell_notGloballyThin` により、この選択された九セルpresentationで任意の並行八セル証拠を比較可能にする解釈も否定した。

**Pの往復だけを埋め、Mの往復は埋めていない。** obstructionを隠してglobal thinnessへ飛躍していない。

## 4. 新しい五角形消去 × 旧P/M交換の真正高次critical overlap

元七セル `fourfoldMixedResidueFirst l r` は、真正四重五角形の三結合子履歴と元mixedResidue第一履歴の`congrComp`で構成された実際の型付き値である。

同じ元第七セルの端点に、五角形の往復と反射比較を合成文脈として持ち上げた

```lean
fourfoldMixedPentagonRoundtripNW
fourfoldMixedPentagonReflexiveNW
```

の二第八セル証拠を構成。`fourfoldMixedPentagonCancelNW` は、今回の唯一の新九セル `cancelPentagon` をこの元mixedResidue文脈に入れた真正Type値である。

さらに、Qi v5.11の旧原始`interchange`を含む `fourfoldMixedCriticalPThenM`、`fourfoldMixedCriticalMThenP` との型付き連鎖から、同じ生第八セル始終点を持つ四頂点と四辺を構成した。

```text
TopLeft  -- interchange (old) --> TopRight
   |                                 |
 cancel(new)                       cancel(new)
   |                                 |
BottomLeft -- interchange (old) --> BottomRight
```

`fourfoldMixedCancelCriticalDiamond` は四辺と一つの完成経路を真正九セルTypeで証明した。完成経路は二つ存在する。

```lean
fourfoldMixedCancelThenInterchange l r
fourfoldMixedInterchangeThenCancel l r
```

これらを**生九セル証明値**として識別する原始イベントtraceを構成した。旧 `interchange` は`false`、新 `cancelPentagon` は`true`である。

\[
\begin{aligned}
\operatorname{trace}(\mathrm{CancelThenInterchange})&=[\mathrm{cancel},\mathrm{interchange}],\\
\operatorname{trace}(\mathrm{InterchangeThenCancel})&=[\mathrm{interchange},\mathrm{cancel}].
\end{aligned}
\]

`fourfoldMixedCancelInterchangeTraceValues` は両式を定義上の等式として証明。さらに `fourfoldMixedCancelInterchangeRawNineGap` が二つの**元の生九セル証明strict Eqの不成立**を証明した。

これは新しい**第十セル比較が存在しない**という定理ではなく、次の第十セルcoherence検討のための正確なraw証拠境界である。

## 5. 元P77/GK5CGの保存

`pentagonActualRoundtripUnitNinthCompletion` は任意の元P77 final raw indexで、本来の `pentagonFinalConservativeLoop`、`pentagonLongConservativeFiveCell`、`pentagonShortConservativeFiveCell` を用いて新九セルのType値存在を構成する。

同時に既証明 `¬ PentagonAdjoinedSixCellEqualityInterpreter` を維持し、元F55/P77/GK5CGの自由証拠値、元七セル・八セル・九セルの全独立presentationを変更しない。四重五角形 × mixedResidue の元七セルにおけるV/R/U法2観測量保存も維持する。

## 6. Lean4初回失敗の全文点検と正規化修正

初回CI [#42377679964](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42377679964) のStrict Leanは次の3件で失敗した。

1. `ninthPentagonRoundtrip_rawGap` 内の `congrArg (fun q => ...)` は、`rw`が期待する展開済みの項と構文的に一致せず、`change`によるβ正規化が必要だった。
2. `pentagonCancelNineCell_preservesPentagonParity` の新生成元分岐で、`rw`がすでに目標を閉じた後に`decide`が残り、`No goals to be solved` を生じた。
3. `pentagonCancelNinthRoundtripParityValues` のP偶奇計算は`rfl`だけでは閉じず、既証明の`ninthPentagonRoundtripVsReflexiveCounts`による明示的書換えが必要だった。

上記だけを修正したHEAD `9fe20a2a5cff0cec2123f53660d45349c52d4d2e` はCI #42377984007で10,325/10,325 SUCCESS。全47宣言の公理出力を再取得し、新規に`sorryAx`がないことを独立確認した。元定理の弱化、未解決課題の非表示、追加公理、旧定義の変更は行っていない。

## 7. 次の厳密課題：Qi v5.13

今回、選択された九セル文法では「P往復消去」は補完できたが「M往復消去」は比較不能であり、P消去と旧交換の九セル二経路も生の証明として異なる。

次段階では**元M往復の最小九セル比較と既存のP消去との干渉**を型付きで探索する。新しい比較を付加しても旧sourceやraw証明を上書きせず、どの観測量が新商に降下するか、どの高次obstructionが残るかを順に証明する。任意並行八セルのglobal thinness、元source strict Eq、自由九セルの生同一視は仮定しない。
