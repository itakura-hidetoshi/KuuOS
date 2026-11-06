# Qi v4.92 — 七セルcritical peakの八セル合流閉包と高次履歴商

## 0. canonical正本・exact-source Lean4形式検証

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、唯一canonical branch `main`。

| 項目 | 確認済み状態 |
|---|---|
| 前提 | Qi v4.91、main `a8271ec11242392bcb8400ed94e2ab04aef300dd` |
| 定理PR | [#3207](https://github.com/itakura-hidetoshi/KuuOS/pull/3207) — MERGED |
| 検証済みexact-source HEAD | `eb89aeb46bb48b4f0bae709519c5e57f5a481567` |
| 定理squash／正本HEAD | `2b5530832090defa9c804dcf1bef6268683b6a24` |
| source／test-merge／squash Git tree | `bf993473445a4e50a2d767c911ed3a2875bdbd11` — 完全一致 |
| Exact-source CI | [#42210838596](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42210838596) — SUCCESS |
| Strict Lean | **10,291／10,291 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 指定新規公理監査 | **18宣言**、標準公理のみ、`sorryAx`なし |
| 変更Lean warning／error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77EightCellCriticalPeakClosureV4_92.lean) · [Qi v4.91正式証明記録](Qi-v4_91-original-P77-eight-cell-local-coherence-zigzag-interchange.md) · [真正GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. v4.91からの数学的前進

Qi v4.91で新八セル`EightCell(H₁,H₂):Type`を生成した。任意の七セル履歴が比較できるとはしていない。v4.92は**八セル生成元を一つも追加せず**、既存22規則の組合せだけで合流可能な明示的critical peak族を形式化した。

原始的critical peakは正確に二種類に限定する。

1. `zigzag`：自由六セル語`(c;c⁻¹);c`から`c`への二つの異なる七セル履歴。左消去先行と、結合則を経由する右消去先行。
2. `independent`：合成された二つの独立六セル成分に対する七セル書換えの順序交換。

その他の生成規則は**これらのピークの型付き文脈閉包**であり、任意の平行七セル履歴の比較を認めるものではない。

## 2. 導出された八セル縦合成・交換の自然性

`eightCell_verticalPasting`は二つの八セル`E_s:s⇒s'`と`E_t:t⇒t'`があるとき、七セル合成の八セル比較

\[
\boxed{E_s\star E_t:\ (s;t)\Rightarrow(s';t')}
\]

を`whiskerRight`、`whiskerLeft`、`chain`だけで導く。これは新しい八セル生成元ではない。

`eightCell_interchangeNaturality`は、独立成分の七セル書換え`s,t`を、それぞれ既存八セルで`s',t'`に変形した場合、左先行`s,t`から右先行`s',t'`への八セルを具体的に構成する。v4.91の単一交換ダイヤモンドを**八セル級の自然性**に強める結果である。

## 3. 任意の型付き文脈でのzigzag合流安定性

`eightCell_zigzagWhiskered`は、同じ始終点を保持する任意の前置・後置七セル履歴によって二通りのzigzagを拡張しても、八セル比較が残ることを証明する。

さらに次の三種類の六セル生語文脈で同じ局所critical peakが合流する。

- `eightCell_zigzagInverseContext`：六セル反転`symm`下での比較。
- `eightCell_zigzagRightContext`：右六セル語との合成文脈。
- `eightCell_zigzagLeftContext`：左六セル語との合成文脈。

いずれも`EightCell.inverseContext`・`EightCell.compositeContext`を使う**導出証明**であり、元六セル語や七セル証明履歴を厳密同一視しない。

## 4. LocalCriticalPeakの帰納的閉包・限定的完全性

新しい`LocalCriticalPeak W l r H₁ H₂ : Type`は、上記二つの基本ピークに加え、反転・二つのピークの連鎖・前後七セルwhiskering・六セル反転／合成文脈・八セル縦合成への閉包を持つ（計9構成子）。全ての構成子は入力の**生の七セル履歴を添字に保持**する。

`localCriticalPeak_eightCell`は構造帰納で証拠の構成関数

\[
\boxed{
P:\mathrm{LocalCriticalPeak}(H_1,H_2)
\;\longmapsto\;
\mathrm{EightCell}(H_1,H_2)
}
\]

を与える。対応する`localCriticalPeak_joinable`はその`Nonempty`版である。これは**限定した局所critical peak族に対する構成的完全性**であり、全七セル履歴の八セル比較可能性は主張しない。

## 5. 八セル比較のSetoidと選択された履歴商

同じ六セル生語`c,d`を始終点に持つ七セル履歴`H₁,H₂`の上に

\[
H_1\sim_8 H_2\;:\!\iff\;
\operatorname{Nonempty}(\mathrm{EightCell}(H_1,H_2))
\]

を定義する。`eightHistorySetoid`は、既存`EightCell.reflexive`・`reverse`・`chain`からこの関係の反射・対称・推移を導出し、`Setoid (SevenRewrite c d)`を構成する。

`eightHistoryClass`はこのSetoidによる**別の新しい選択商**であり、元`SevenRewrite`を破壊的に変更しない。`eightHistoryClass_eq_iff`により

\[
\boxed{
[H_1]_8=[H_2]_8
\quad\Longleftrightarrow\quad
\operatorname{Nonempty}(\mathrm{EightCell}(H_1,H_2))
}
\]

が確立する。既証明のzigzag二履歴は

\[
\boxed{
[H_{\rm left}]_8=[H_{\rm right}]_8
\quad\land\quad
H_{\rm left}\ne H_{\rm right}.
}
\]

`localCriticalPeak_classEq`は、上記限定的critical peak族の合流から**履歴商での等式**を導出する。`eightHistoryClass_noStrictReturn`は商のEqから全七セル生構文の厳密Eqへ戻す普遍的解釈を否定する。

この新商は旧六セル次数商とは異なる層である。六セル生語、七セル生履歴、八セル比較の存在、八セル履歴商、元GK5CG sourceを混同しない。

## 6. 真正元P77全raw添字とauthority境界

`pentagonActualEightHistory_zigzagQuotientNotStrict`は元P77最終raw添字`i`のすべてについて、元GK5CG五セルの指定二端点を保持した新七セルzigzag二履歴が、新八セル商で一致しながら**生七セル構文では厳密不一致**であることを証明する。

`pentagonActualEightHistory_withSourceObstruction`は、その新履歴商の一致と、既証明の旧五セル`PentagonAdjoinedSixCellEqualityInterpreter`不存在を同時に示す。旧F55/P77/GK5CG sourceに新しい高次cell構成子を追加せず、元のcharge、strict non-collapse、source authorityを保存する。

## 7. 公理依存・Lean4監査

`#print axioms`を指定した18宣言すべてについてexact-source CIログで確認。最初の11宣言は**公理依存なし**。商等式を扱う5宣言は`propext`・`Quot.sound`、真正元P77へ移した2宣言は既存source依存の`propext`・`Classical.choice`・`Quot.sound`のみ。非標準公理、`sorryAx`なし。変更Lean warning/error0/0。

## 8. 次段階Qi v4.93候補

- `LocalCriticalPeak`に含まれていない実際の七セル書換えcritical pairを**具体例で抽出**し、追加の局所八セル整合性が必要か検証する。
- 特に七セルの結合・単位・逆元消去に現れる**重なったピーク**の解析。既存22生成規則で導出可能な場合と、追加生成元を必要とする場合を区別。
- 全任意七セル履歴の高次thin性や九セル証明履歴の同一性は未証明と明記し、元sourceへのdescent障害も保持する。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
