# Qi v5.14 — 元P/M九セルcritical diamondの最小第十セル比較と残余九セル合成障害

## 0. 正本・exact-source検証

2026年11月8日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.13までの真正元F55/P77/GK5CG型付きsource・自由七／八／九セル証拠を変更せず、独立した第十セルpresentationのみを追加した。

| 項目 | 検証済み状態 |
|---|---|
| 定理PR | [#3280](https://github.com/itakura-hidetoshi/KuuOS/pull/3280) **MERGED** |
| 定理squash | `be2f4a481d0dfcd1e75091f4603ef491a22d40dc` |
| exact-source CI | [#42418086443](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42418086443) **SUCCESS** |
| Strict Lean | **10,327 / 10,327 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 22宣言の`#print axioms` | 公理不要、または`propext`／`Classical.choice`／`Quot.sound`のみ |
| `sorryAx` | なし |
| 変更Lean error/warning | **0 / 0** |
| source HEAD | `a656618b836d8cd2088109dcdd0e8c1d42d6714c` |
| test-merge HEAD | `0369fca99c00bc541e97816087444d40b6c4aba0` |
| source/test-merge Git tree | `453864c3d3784b1097fabe0536d93a782ebc55b8` **完全一致** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 / root | `KuuOSFormal` / 107維持 |
| 保護PR #1558 | Draft／OPEN／未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77PMCriticalDiamondMinimalTenthComparisonV5_14.lean) · [前段Qi v5.13正式証明記録](Qi-v5_13-original-mixed-roundtrip-ninth-completion-verified-20261108.md)

## 1. 元九セルP/M完成経路と独立第十セル

Qi v5.13における真正八セル始終点の同一性を保った二つの生九セル証明は、九セルの生成元順序で区別できる：

\[
\alpha_{PM}=\mathrm{originalDoubleCancellationPThenM}(l,r),\qquad
\alpha_{MP}=\mathrm{originalDoubleCancellationMThenP}(l,r).
\]

それぞれの原始traceは `[true, false]` と `[false, true]` である。前段の定理`originalDoubleCancellationRawNineGap`により、**元の生九セルType値はstrictに不等**。

今回の独立Type

```lean
MixedInterchangeTenCell W l r alpha beta
```

には、一種類だけの新しい非strict生成元

```lean
MixedInterchangeTenCell.exchangePM
```

を置く。その二端点は上記の元九セル証拠値そのもの。ほかは`strict`、`symm`、`trans`、九セル逆・連鎖、八セル反転・連鎖・whisker・inverse・compositeという**型付き文脈閉包のみ**。

`mixedInterchangeTenCell_relativeNecessity`は新比較の存在と元の生九セルstrict Eq不存在を同時に証明。`mixedInterchangeTenCell_noRawEqualityInterpreter`で、全新十セル証拠を生九セルEqに変換する普遍解釈を否定した。

**数学的意味：** 新しいpresentationを追加したのであり、古い元Type値証拠を改変・消去・定義上同一視していない。この相対的最小性は、すべての高次モデルにおける比較の唯一性／普遍性を主張しない。

## 2. 選択第十セル商と降下不能な順序履歴

`mixedInterchangeTenthSetoid`、`mixedInterchangeTenthClass`を、元の九セルType上の実際の`Nonempty (MixedInterchangeTenCell ...)`から構成した。`mixedInterchangeTenthClass_eq_iff`で、商等号と新第十セル比較可能性の同値を証明。

\[
\boxed{[\alpha_{PM}]_{10}=[\alpha_{MP}]_{10}}
\quad\text{かつ}\quad
\boxed{\alpha_{PM}\neq\alpha_{MP}\text{（生のType値）}}.
\]

従って元の九セル原始イベントの順序付きリストをそのまま商へ降下させる観測者は存在しない（`mixedInterchangeTenthClass_noTraceDescent`）。また商から元の九セル生証拠すべてへ左逆復元する写像も存在しない（`mixedInterchangeTenthClass_noRawRetraction`）。

## 3. 十セル追加後も残る新たな高次obstruction

新しいNat値構文的観測量`tenthResidualNineChainCharge`を、**元の自由九セル証拠**上に定義した。

- v5.12由来`previous`と新原始`cancelMixed`は、この特定観測では各0。
- 真正九セル`chain`構成子は左右の値の和に **+1**。
- 九セル逆向きや単独文脈は値を保持、`chainContext`／`compositeContext`では左右の値を加える。

二つの元critical-diamond九セル証拠はともにこの値が1。`mixedInterchangeTenCell_preservesNinthChainCharge`が、**新第十セルの全12構成子**について構造帰納法で保存を証明する。`mixedInterchangeTenthNinthChainCharge`はNat値の真正`Quotient.lift`。

他方、元の九セル反射証拠を二つ自由連鎖した場合と一つだけの場合には、

\[
\boxed{Q_{10}(\mathrm{refl}_9;\mathrm{refl}_9)=1,\qquad
Q_{10}(\mathrm{refl}_9)=0.}
\]

`tenthDoubleReflexive_noInterchangeTenComparison`と`tenthDoubleReflexive_distinctInterchangeClass`で、**同じ元八セル始終点でも新第十セルの比較は存在しない**ことを証明した。`mixedInterchangeTenCell_notGloballyThin`により、選択した第十セルpresentationのglobal thinnessは否定される。

これは新しい自由九セル構文に対する相対的obstructionであり、将来さらに独立した比較を付加する可能性を排除しない。

Qi v5.13の元八セル整数不変量`ninthResidualChainCharge`による **2対0** の非比較証明も保持する（`mixedInterchangeTenCell_retainsEighthObstruction`）。第十セルを追加しても、存在しなかった元九セル証拠が自動生成されるわけではない。

## 4. 元P77/GK5CG真正Type値sourceへの特殊化

`pentagonActualPMCriticalDiamondTenthCompletion`は、任意の真正P77 final raw patch tree indexで、元GK5CGのlong/short五セルType値から第十セル生成元を具体的に実現し、同時に旧`PentagonAdjoinedSixCellEqualityInterpreter`の不存在を保持する。

元F55/P77/GK5CG、独立旧六・七・八・九セル文法は変更しない。新しい十セル商と元のsource等式を混同しない。

## 5. 継承すべき次段課題

Qi v5.15では、今回まだ比較できない九セル自由連鎖と反射の間の候補第十セル／第十一セルを無条件で増やす前に、**九セルchainのunit・associativity法則を付加するとどの観測量が降下不能になるか**を分離する。さらに選択十セル同士の二つの貼り合わせ順序を型付きで区別し、真正第十一セルに進むべきcritical pairを限定する。

新比較によって古いraw証拠のstrict Eq、元sourceの一括昇格、普遍thinnessを宣言しない。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊。Apache-2.0。
