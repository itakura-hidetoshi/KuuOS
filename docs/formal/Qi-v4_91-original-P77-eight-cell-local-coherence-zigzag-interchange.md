# Qi v4.91 — 真正P77五セル端点における七セル履歴の八セル局所coherence

## 0. canonical正本とexact-source検証

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、唯一canonical branch `main`。

| 項目 | 確認済み正本 |
|---|---|
| 継承起点 | Qi v4.90、main `eec7e476984697d4878f5092a56d509cea76cd4b` |
| 定理PR | [#3205](https://github.com/itakura-hidetoshi/KuuOS/pull/3205) — MERGED |
| 検証済みexact-source HEAD | `9b2b404308295d1b7a865b4d0cafe481e9fe954a` |
| 定理squash／正本HEAD | `d4482387d5bea54c31471caf3ddfd48921adc7f3` |
| source／test-merge／squash Git tree | `812adf606eefc012929d81403161d603e2a4d67b` — 完全一致 |
| exact-source CI | [#42208912882](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42208912882) — completed/SUCCESS |
| Strict Lean | **10,290／10,290 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | 指定10宣言すべて標準公理のみ、`sorryAx`なし |
| 変更Lean warning/error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77EightCellLocalCoherenceV4_91.lean) · [Qi v4.90正式証明記録](Qi-v4_90-original-P77-seven-cell-rewrite-normalization-local-completeness.md) · [元GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 新しい八セル比較Typeの位置づけ

- v4.86：元の真正GK5CG保守的五セル値を**指定二端点**に保持し、元sourceとは別の新しい六セル自由語presentationを追加。
- v4.87/4.88：新六セル構文次数、次数商、異なる元五セル端点での三形正規語を証明。
- v4.89：新六セル生語`c,d`の両方を添字とし、13個の具体的な局所書換え規則を持つ`SevenRewrite(c,d) : Type`を追加。
- v4.90：元五セル指定端点が異なる条件で、任意の平行な新六セル生語に**七セル書換え履歴の存在**を証明。**七セル履歴どうしの厳密同一性は証明していない。**
- **v4.91：二つの七セル履歴`H₁,H₂ : SevenRewrite(c,d)`をそのまま添字に保持する`EightCell(H₁,H₂) : Type`を追加。**

```lean
inductive EightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix
```

八セルは**無条件の七セルEq**ではなく、新しく自由生成された高次coherence証明の型である。七セル履歴を一律に比較する`allParallel`構成子を追加しておらず、全域的なcoherence完全性や八セルのthin性は主張しない。

## 2. 22個の明示的八セル生成規則

`EightCell`は以下の局所証拠だけで生成する。

1. 八セルの反射、反転、合成（`reflexive`, `reverse`, `chain`）。
2. 七セル履歴に対する左右whiskering、反転文脈、六セル反転・合成文脈へのcongruence（`whiskerLeft`, `whiskerRight`, `reverseContext`, `inverseContext`, `compositeContext`）。
3. 七セル合成の左／右単位、結合則、逆元左右消去、二重反転、恒等逆、合成逆（`unitLeft`, `unitRight`, `associate`, `cancelRight`, `cancelLeft`, `involute`, `inverseIdentity`, `inverseComposite`）。
4. 六セル反転・合成congruenceの恒等／合成保存（`inverseCongruenceIdentity`, `inverseCongruenceChain`, `compositeCongruenceIdentity`, `compositeCongruenceChain`）。
5. 互いに独立した局所七セル書換えの二通りの順序を比較する`interchange`。
6. `(c;c⁻¹);c` の二通りの縮約履歴を比較する`zigzagDiamond`。

最後の2つは**新しい八セル生成元として明示的に追加**した局所整合性であり、七セル構文の厳密Eqから出たものではない。

## 3. 形式証明された具体的zigzagダイヤモンド

任意の新六セル生語`c:w⇒z`について、共通の始点`(c;c⁻¹);c`から終点`c`までの次の**二つの実際の七セル導出語**を構成する。

- `H_left := trans (congrComp (inverseRight c) (refl c)) (leftUnit c)` — 左ペア`c;c⁻¹`を先に消す。
- `H_right := trans (assoc c (symm c) c) (trans (congrComp (refl c) (inverseLeft c)) (rightUnit c))` — 結合則で右ペア`c⁻¹;c`を先に消す。

Lean4により、次の両立が成立する。

\[
\boxed{
\operatorname{Nonempty}\bigl(\mathrm{EightCell}(H_{\mathrm{left}},H_{\mathrm{right}})\bigr)
\quad\land\quad
H_{\mathrm{left}}\ne H_{\mathrm{right}}.
}
\]

証明名：`sevenZigzagViaAssoc`、`sevenZigzag_twoHistories_notStrict`、`eightZigzagCoherence`、`eightZigzag_exists_notStrict`。

この`≠`は**新しく自由生成された七セル構文の厳密不一致**であり、二つの証明書の端点や商を変更する主張ではない。

## 4. 局所交換図式・高次整合性

七セル書換え`s:c⇒c'`と`t:d⇒d'`が六セル合成の互いに独立した成分に作用するとき、次の二通りの合成七セル履歴を比較する。

\[
\boxed{
\begin{aligned}
H_{L\to R} &=
(s\otimes\mathrm{id}_d)\,;\,
(\mathrm{id}_{c'}\otimes t),\\
H_{R\to L} &=
(\mathrm{id}_c\otimes t)\,;\,
(s\otimes\mathrm{id}_{d'}).
\end{aligned}
}
\]

`eightIndependentInterchange`は、これらの履歴の間の新しい`EightCell`を明示的に構成する。任意の七セル履歴が同一であると主張せず、指定された局所交換だけを証明書化している。

## 5. 厳密戻り障害と真正元sourceの境界

`eightCell_noStrictSevenInterpreter`は、**任意の八セルが元の二つの七セル履歴の厳密Eqを誘導する**という普遍的解釈を否定する。既存七セル`refl`と`trans (refl) (refl)`が異なる生構文である一方、`EightCell.unitLeft`がそれらを比較できることが反例となる。

`pentagonActualEightCell_zigzagDiamond`は任意の真正P77最終raw添字`i`に新八セルzigzag比較を移し、元GK5CG五セル値`L₃(i),L₂(i)`をそのまま保持する。`pentagonActualEightCell_withOriginalNoGo`は、八セルが存在しながらも既証明の元五セルEqualityInterpreter障害が存続することを同時に形式証明する。

**元F55/P77/GK5CGに新しい五／六／七／八セルsource構成子を加えていない。** strict空中心、独立Kuu=presentation、元Type値と依存履歴のauthority分離を維持。異なる六セル語や七セル履歴を勝手に厳密Eqへ戻さない。

## 6. axiom audit と検証範囲

新規10宣言の`#print axioms`をGitHub Actions実ログで確認。汎用八セル・zigzag・交換・strict不一致の8宣言は**公理依存なし**。真正P77全添字に移した2宣言のみ、元sourceの既存依存である`propext`、`Classical.choice`、`Quot.sound`を継承。非標準公理、`sorryAx`なし。固定ツールチェーンで`KuuOSFormal`と新規モジュールの全10,290 jobsが成功した。

元端点の異なる条件はv4.90までの全七セル書換え完全性の証明に必要だが、**v4.91の具体的局所八セルダイヤモンド自体は任意のW,l,rに対して構成される**。この区別を維持する。

## 7. 次段階Qi v4.92候補

- 八セル比較生成元の局所critical peakの分類、異なる七セル正規化履歴への適用範囲の拡大。
- 規則の交錯・包含で生じる具体的なcritical branchの高次合流証明。
- 任意七セル履歴間の全域coherenceは**証明目標**に留め、既存22生成元から帰納的に導出できる範囲と、追加生成元または条件を要する障害を区別。
- 元sourceへのdescent、七セル厳密Eq、八セルType証拠、選択次数商を混同しない。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
