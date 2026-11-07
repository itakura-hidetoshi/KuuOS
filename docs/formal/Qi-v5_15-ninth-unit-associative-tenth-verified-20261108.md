# Qi v5.15 — 九セル単位・結合第十セル補完、P/M独立不変量、真正第十一セルcritical overlap

## 0. 正本・exact-source検証

2026年11月8日 JST。repository `itakura-hidetoshi/KuuOS` / canonical branch `main`。
Qi v5.14で導入した真正P/M交換第十セルと、元F55/P77/GK5CG・独立六・七・八・九セルの生のType値証拠をすべて保存して、新しい独立第十セルpresentationを追加した。

| 項目 | 確認済み状態 |
|---|---|
| 定理PR | [#3282](https://github.com/itakura-hidetoshi/KuuOS/pull/3282) **MERGED** |
| 定理squash | `f8a741e609565ded35e138d147a402fc57f91409` |
| exact-source CI | [#42419530339](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42419530339) **SUCCESS** |
| Strict Lean | **10,328 / 10,328 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規37宣言の`#print axioms` | 公理不要または`propext`・`Classical.choice`・`Quot.sound`のみ |
| `sorryAx` | なし |
| 変更Leanのerror/warning | **0 / 0** |
| source HEAD | `c563190990ecbc9fcf50591645ca8a6394f1dac3` |
| test-merge HEAD | `02c8ca80cf1c87f4e6d15d74d078f1586956bd34` |
| source/test-merge Git tree | `e0de74bb292e082bf1e5af59d337f3f68df6347b` **完全一致** |
| Lean/mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約/root | `KuuOSFormal` / 107維持 |
| 保護PR #1558 | Draft / OPEN / 未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77NineCellUnitAssociativeTenthV5_15.lean) · [Qi v5.14正式記録](Qi-v5_14-original-pm-ninth-diamond-minimal-tenth-verified-20261108.md)

## 1. 九セル自由合成の単位律・結合律を独立第十セルとして補完

Qi v5.14で検証済みの第十セル比較`MixedInterchangeTenCell`は、元P/M消去順序の交換のみを新原始とし、自由九セル合成の単位・結合律はまだ証明していなかった。

今回、旧第十セル証拠すべてを`previous`で保持する独立Typeを構成した。

```lean
MixedUnitAssocTenCell W l r alpha beta
```

**新規比較生成元はちょうど三種類：**

- 左単位：`leftUnit alpha` — `chain (refl q) alpha` と `alpha` の型付き第十セル
- 右単位：`rightUnit alpha` — `chain alpha (refl q')` と `alpha` の型付き第十セル
- 結合則：`assoc alpha beta gamma` — `chain (chain alpha beta) gamma` と `chain alpha (chain beta gamma)` の型付き第十セル

残りは厳密な証拠の`strict`、旧証拠`previous`、第十セルの向き反転・連鎖、九セル反転・連鎖、八セルの逆向き・連鎖・whisker・合成文脈の型付き閉包。新文法は全15種類の構成子を持つ。

`mixedUnitAssocTenCell_strictlyNew`は、旧第十セル文法では比較不能だった**真正元九セル反射2個の連鎖 vs 反射1個**を新`leftUnit`で比較できることを示す。旧文法への普遍比較復元（`mixedUnitAssocTenCell_noPreviousInterpreter`）と生九セルstrict Eqへの普遍昇格（`mixedUnitAssocTenCell_noRawEqualityInterpreter`）はそれぞれ反証済み。

## 2. 旧九セル自由chain不変量の降下不能性

前段Qi v5.14で`Quotient.lift`へ降下していたNat値`tenthResidualNineChainCharge`は、自由九セル`chain`構文ごとに+1を数えていた。

\[
Q_{\mathrm{chain}}(1_9;1_9)=1,\qquad Q_{\mathrm{chain}}(1_9)=0.
\]

新第十セルの`leftUnit`により両証拠は同一商クラスになった。このため、**元の全生九セル証拠に同じ値を返す旧Qの忠実な新商への降下は存在しない**。これは`mixedUnitAssocTenthClass_noOldChainChargeDescent`で形式証明した。

旧比較の新商への降下は`mixedInterchangeTenthClass_descendsToUnitAssoc`、選択商の厳密な粗化は`mixedUnitAssocTenthClass_strictlyNew`。元証拠を消したわけではなく、**観測量の許容範囲が選択した比較法則に依存する**ことを証明した。

## 3. 新たなP/M独立出現回数の完全な保存と真正降下

元の九セル`mixedCancelNinePrimitiveTrace`は、真正な旧P消去と新M消去のイベントを`true/false`で区別する。新観測量を

\[
N_P(\alpha)=\#\{\mathrm{true\ in\ trace}(\alpha)\},
\qquad
N_M(\alpha)=\#\{\mathrm{false\ in\ trace}(\alpha)\}
\]

とした。

`mixedInterchangeTenCell_preservesCancellationCount`は前段第十セルの全12構成子、`mixedUnitAssocTenCell_preservesCancellationCount`は新文法の**全15構成子**について、任意`isP : Bool`の保存則を構造帰納法で証明している。

\[
\alpha\Rightarrow_{10}\beta
\Longrightarrow
N_P(\alpha)=N_P(\beta)\ \land\
N_M(\alpha)=N_M(\beta).
\]

`mixedUnitAssocTenthPCount`と`mixedUnitAssocTenthMCount`は、実際の`Quotient.lift`による二つの別個のNat値商観測者であり、代表元上の値もLeanで計算した。単に自由語の同じ書き方でしか成立しない宣言ではない。

## 4. 単位・結合補完後にも残る二つの独立障害

真正元のP消去およびM消去をそれぞれ往復させた生九セルループを構成した。

\[
\begin{aligned}
\lambda_P&=\mathrm{Pcancel};\mathrm{reverse}(\mathrm{Pcancel}),
&(N_P,N_M)(\lambda_P)&=(2,0),\\
\lambda_M&=\mathrm{Mcancel};\mathrm{reverse}(\mathrm{Mcancel}),
&(N_P,N_M)(\lambda_M)&=(0,2).
\end{aligned}
\]

対応する各元八セル端点上の反射九セル`1_9`は(0,0)。したがって、
`ninthOriginalPentagonLoop_noUnitAssocComparison`と`ninthOriginalMixedLoop_noUnitAssocComparison`で、**各往復ループと対応する反射九セルとの新第十セル非比較性**を形式証明。両者は別々の元八セル端点に置かれているため、両ループ相互の直接比較不能を主張しているのではない。

これより`mixedUnitAssocTenCell_notGloballyThin`でこの選択第十セルpresentationのglobal thinnessを否定した。元八セル側の自由chain由来の2対0非比較も`mixedUnitAssocTenCell_retainsEighthObstruction`で引き続き保存している。

**射程：** 九セルの逆向き`reverse`を持っていても、対応する逆元消去の第十セル比較を今回新規追加したわけではない。後続のgroupoid-completionの可能性は排除しない。

## 5. 真正第十一セルcritical overlap候補

旧v5.14 P/M交換と新`leftUnit`を重ねると、次の二経路は**まったく同じ生九セル始点・終点**を持つ。

\[
\begin{aligned}
\Theta_{E U}
&=(\mathrm{exchangePM\ in\ left\ context});\mathrm{leftUnit},\\
\Theta_{U E}
&=\mathrm{leftUnit};\mathrm{exchangePM}.
\end{aligned}
\]

真正な型付き十セル証拠はそれぞれ
`pmLeftUnitCriticalExchangeThenUnit`と`pmLeftUnitCriticalUnitThenExchange`で明示構成した。

新しい生十セル構文trace`mixedUnitAssocTenRawTrace`により、値はそれぞれ`[false,true]`と`[true,false]`。`pmLeftUnitCriticalRawTenGap`で**生のType値としてstrict不等**であることをLean4で証明した。

これは**第十一セル比較の候補を局所的に特定した**ものである。第十一セルの不存在・必然性・唯一性を証明したわけではない。

## 6. 元P77/GK5CG真正証拠境界

`pentagonActualNineUnitAssocTenthCompletion`は任意の真正P77 final raw indexについて、元GK5CG long/short Type値から九セル左単位第十セルを実現すると同時に、元`PentagonAdjoinedSixCellEqualityInterpreter`の不存在を保持した。

元F55/P77/GK5CG、旧六・七・八・九・十セル定義、公理・固定toolchainは一切変更しなかった。新商等号を元sourceのstrict等号には昇格させない。

## 7. 次段Qi v5.16

優先する第十一セル候補は、今回構成した**交換→単位**と**単位→交換**の二つの生十セル経路を結ぶ、独立した型付き比較とする。新比較後に、元十セル構文のどの履歴が商へ降下しなくなり、何が残るかを再度証明する。

引き続きappend-only / tighten-only / overwrite-forbidden / same-rootを守る。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊。Apache-2.0。
