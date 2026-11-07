# Qi v5.16 — 真正P/M交換×九セル単位の最小第十一セル補完と独立十セル障害

## 0. 正本とexact-source検証

2026年11月8日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
前段Qi v5.15の独立第十セル、元F55/P77/GK5CGおよび旧六・七・八・九セルの真正Type値証拠を改変せず、新しい独立第十一セルpresentationを追加した。

| 項目 | 確認済み状態 |
|---|---|
| 定理PR | [#3284](https://github.com/itakura-hidetoshi/KuuOS/pull/3284) **MERGED** |
| 定理squash | `5e6658dd84283f30dcaee83c34e680063466e73a` |
| exact-source CI | [#42420855556](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42420855556) **SUCCESS** |
| Strict Lean | **10,329 / 10,329 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 29宣言の`#print axioms` | 公理不要または`propext`、`Classical.choice`、`Quot.sound`のみ |
| `sorryAx` | なし |
| 変更Leanのerror/warning | **0 / 0** |
| source HEAD | `fa236e2404293ef3b6e7b7a2c0f2a87201eeb149` |
| test-merge HEAD | `cc23e23e14f18f8c3b28ffc757a58120b256cbb9` |
| source/test-merge Git tree | `f25e70506a0c6bdbadb9e81b86401663cf82690d` **完全一致** |
| Lean/mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約/root | `KuuOSFormal` / 107維持 |
| 保護PR #1558 | Draft／OPEN／未マージ |

[Lean証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77PMUnitExchangeMinimalEleventhV5_16.lean) · [前段Qi v5.15正式記録](Qi-v5_15-ninth-unit-associative-tenth-verified-20261108.md)

## 1. 元の型付き十セルcritical pairを独立第十一セルで比較

Qi v5.15で元P/M交換と九セル左単位の間に、同じ**生九セル始終点**を持つ二つの**生十セル証拠**を構成済み：

```lean
pmLeftUnitCriticalExchangeThenUnit l r
pmLeftUnitCriticalUnitThenExchange l r
```

`pmLeftUnitCriticalRawTenGap`は両者が**生Type値として厳密に異なる**ことを示す。今回この実際の二端点間に、新しい独立Type

```lean
MixedExchangeUnitElevenCell W l r xi zeta
```

を定義し、**ちょうど一種類だけの新しい非strict比較生成元**`exchangeUnit`を付加した。残りはstrict、十一セル反転・連鎖、および既存十セルのsymm・trans・nineReverse・nineChain・reverseContext・chainContext・whiskerLeft/Right・inverseContext・compositeContextの**型付き閉包**。合計14種類の構成子。

`mixedExchangeUnitElevenCell_relativeNecessity`は、新比較の存在と元生十セルstrict Eqの不存在を同時に証明。`mixedExchangeUnitElevenCell_noRawEqualityInterpreter`は、選択した新第十一セル証拠の一般的な生十セル等号解釈が存在しないことを証明した。

**重要な限定：** これは独立した高次比較presentationへの原始生成元の追加であり、元sourceに以前からこの生成元が存在していたという主張ではない。任意の高次coherence・普遍thinnessを仮定しない。

## 2. 選択第十一セル商と十セル順序traceの非降下

`mixedExchangeUnitEleventhSetoid`は元の平行十セル証拠Type上の`Nonempty (MixedExchangeUnitElevenCell ...)`を同値関係として用いる。`mixedExchangeUnitEleventhClass_eq_iff`でクラス等号と第十一セル比較可能性を必要十分条件として証明。

元の十セル値に対して、

\[
\boxed{[\Theta_{EU}]_{11}=[\Theta_{UE}]_{11}}
\quad\text{ただし}\quad
\boxed{\Theta_{EU}\ne\Theta_{UE}\quad\text{(raw Type)}}
\]

が成立する。

元の原始十セルtraceはそれぞれ`[false,true]`（旧比較→新単位）と`[true,false]`（新単位→旧比較）で異なる。このリストを全代表元に忠実な形で新商に降下させる関数は存在しない（`mixedExchangeUnitEleventhClass_noRawTraceDescent`）。また全元十セル証拠へ復元する左逆は存在しない（`mixedExchangeUnitEleventhClass_noRawRetraction`）。

ここで「商で等しい」と「生の元証拠が等しい」は独立した命題のまま保持した。

## 3. 新たな二つのNat値観測量の降下

元十セル`mixedUnitAssocTenRawTrace`を追跡し、新観測量を

\[
N_{\mathrm{old}}(\Xi)=\#\{\mathrm{false\ in\ trace}(\Xi)\},
\qquad
N_{\mathrm{unit}}(\Xi)=\#\{\mathrm{true\ in\ trace}(\Xi)\}
\]

として定義した。`false`はv5.14由来の`previous`第十セル証拠wrapper、`true`はv5.15で新規追加した左・右単位第十セル生成元を数える。`assoc`や`strict`はこの**特定の二成分観測**では0を寄与する。古い第十セル証拠の内部履歴まで数える観測量と混同しない。

今回の新生成元で比較した二経路は、いずれも

\[
\bigl(N_{\mathrm{old}},N_{\mathrm{unit}}\bigr)=(1,1)
\]

であり順序は異なるが計数は等しい。

`mixedExchangeUnitElevenCell_preservesTenthEventCount`は、**全14種類の第十一セル構成子について**任意のBool選択に対する計数保存を構造帰納法で証明した。特に反転・連鎖、九セル・十セルの合成文脈と対応づく。

`mixedExchangeUnitEleventhOldCount`と`mixedExchangeUnitEleventhUnitCount`は本物のNat値`Quotient.lift`であり、代表元への評価等式も形式証明された。単に二つの例で値が等しいという主張ではない。

## 4. 第十一セル追加後にも残る二つの独立障害

一つ目は、**元のP/M交換の十セル証拠を逆向きと連結した真正往復**：

```lean
eleventhOriginalPMTenRoundtrip l r
```

同じ九セル始終点を持つ反射十セルと比較すると

\[
(N_{\mathrm{old}},N_{\mathrm{unit}})
=(2,0)\quad\text{対}\quad(0,0).
\]

二つ目は、**真正九セル左単位の十セル証拠とその逆向きによる往復**：

```lean
eleventhOriginalUnitTenRoundtrip l r
```

その九セル始終点での反射十セルと比較すると

\[
(N_{\mathrm{old}},N_{\mathrm{unit}})
=(0,2)\quad\text{対}\quad(0,0).
\]

これらは元九セル始終点の異なる**二つの局所fiber**上の反例であり、両往復ループ間の直接比較を主張しない。

`eleventhOriginalPMTenRoundtrip_noComparison`と`eleventhOriginalUnitTenRoundtrip_noComparison`でそれぞれの**第十一セル比較不存在**を、全構成子保存不変量から証明した。選択十一セル商の異なるクラス・`mixedExchangeUnitElevenCell_notGloballyThin`も形式証明済み。

今回、新しい逆元消去十一セルを追加していない。将来その種の独立比較を追加すれば、この二成分計数が降下不能となりうる。今回の障害は**選択した十一セル文法に相対的**であり、任意の高次圏で逆向き証拠を相殺できないという普遍定理ではない。

先行の九セル・八セル証拠の非比較は`mixedExchangeUnitElevenCell_retainsNinthObstruction`／`mixedExchangeUnitElevenCell_retainsEighthObstruction`として保持した。第十一セル比較だけから存在しない下位証拠を生成しない。

## 5. 元P77/GK5CG真正Type値sourceへの特殊化

`pentagonActualPMUnitEleventhCompletion`は、任意の真正P77 final raw indexで、元GK5CG long/short五セルType値によって今回の独立第十一セル比較が実在することを構成し、同時に旧`PentagonAdjoinedSixCellEqualityInterpreter`の不存在を保持する。

元F55/P77/GK5CGと旧独立六・七・八・九・十セルのLean定義・型付き履歴は一切変更していない。

## 6. 次段Qi v5.17

第十一セル後の新課題は、選択した十一セル文法における**十セル逆元往復の比較障害**と、十一セル交換生成元の左右whiskering／二つの貼り合わせ履歴の高次critical pairの区別である。

次の独立十二セル候補は、元の型付き十一セル証拠から具体的な平行二経路を構成し、その生十二次比較が必要な理由・残存障害を先に明示して絞り込む。無条件のthinness、元source strict Eq、任意の高次coherenceを導入しない。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊。Apache-2.0。
