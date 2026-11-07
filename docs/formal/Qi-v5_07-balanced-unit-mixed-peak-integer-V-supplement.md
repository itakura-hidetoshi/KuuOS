# Qi v5.07 補完 — mixedResidue × balancedUnit の真正型付き局所比較と整数V非降下

## 0. 正本、継承境界、検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical `main`。
正式な Qi v5.07 定理は [#3237](https://github.com/itakura-hidetoshi/KuuOS/pull/3237)、正式記録は [#3239](https://github.com/itakura-hidetoshi/KuuOS/pull/3239)。本記録はこれらを置き換えず、重複する旧 [#3238](https://github.com/itakura-hidetoshi/KuuOS/pull/3238) から**非重複の命題のみ**を抽出して追加証明したもの。

| 項目 | exact-source 確認結果 |
|---|---|
| 定理補完PR | [#3240](https://github.com/itakura-hidetoshi/KuuOS/pull/3240) MERGED |
| 定理squash SHA | `2e812f7518a3b4eaab474db663625d2d3ee51173` |
| 継承した検証済みmain | `12ecd76b9c036c7119447c6143fb8ebccd45629e` |
| 検証source HEAD | `0ee833e687b934389f52ed4d924c473bfec58ca9` |
| test-merge HEAD | `a1c0c4dda75acf9c15389fb20a35bab7fedd9b7f` |
| exact-source CI | [#42336330332](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42336330332) SUCCESS |
| Strict Lean | **10,307 / 10,307 SUCCESS** |
| Governance Gate | **30 / 30 SUCCESS** |
| 新規11宣言の公理依存 | `propext`、`Classical.choice`、`Quot.sound` のみ、または公理依存なし |
| sorryAx | **なし** |
| 変更Lean warning/error | **0 / 0** |
| source/test-merge | GitHub compareでファイル差分 **0** |
| Lean / mathlib pin | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約とroot | `KuuOSFormal`、公開root **107維持** |
| 保護PR #1558 | **Draft / OPEN / 未マージ** |

[追加Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedResidueBalancedUnitSupplementV5_07.lean) ·
[元Qi v5.07正式証明記録](Qi-v5_07-original-P77-mixed-residue-minimal-higher-completion.md)

## 1. 数学的成果

### 整数 V は新しい商に降下しない

Qi v5.06 で構成した **同じ真正六セル両端に対する七セル履歴** `sevenMixedResidueFirst/Second` は、元の整数 `sevenTotalReductionCharge` が **3対5**、一方 Qi v5.07 の新しい `MixedResidueEightCell.mixedResidue(w)` で比較可能。

追加定理 `mixedResidueHistoryClass_noIntegerVDescent` は、整数Vが新商の代表元に依存しない観測量である、という任意の普遍命題を反証する。旧 `V mod 4` の非降下は既存のQi v5.07定理が証明済みで、本補完は **整数V** についてさらに明示的に切り分ける。既証明の `V mod 2`、`R mod 2`、`U mod 2` の降下は保持する。

### mixedResidue × balancedUnit の真正critical pair

元 v5.03 `BalancedUnitEightCell.balancedUnit` の実在する型付き比較を、元 v5.05 の `DoubleCompositeEightCell.previous` と、現行 `MixedResidueEightCell.previous` によって厳密に輸送する。

`mixedResidueBalancedFirst/Second` は、元 v5.06 の `sevenMixedResidueFirst/Second` を元balanced-unitの七セル両経路と型付き合成した**具体的な履歴**である。新しい原始比較生成元は追加しない。

形式証明された結論：

- `mixedResidueBalanced_fill`: **新** `MixedResidueEightCell` 内に比較証拠が存在。
- `mixedResidueBalanced_noPrevious`: 旧 `DoubleCompositeEightCell` 内では元 `V mod 4` 保存障害により比較証拠が不存在。
- `mixedResidueBalanced_newVsOld`: 新比較の存在・旧比較の不存在・新商で保存される `V mod 2` の一致を同時に証明。
- `mixedResidueBalanced_classGap`: 旧商では異なる二classが、現行新商では同じclassになることを証明。

この `balancedUnit` overlap は、元 Qi v5.07 で形式証明済みの `unitDiamond` overlap とは独立した具体例である。ただし **新しい商や新しい八セル原始生成元を導入したわけではない**。

### 選択した局所critical familyの閉包

`MixedResidueBalancedCriticalPeak` は、既存の `MixedResidueCriticalPeak` と今回の `mixedBalanced` の二つを基底に、reverse、chain、左右whisker、inverseContext、compositeContextの型付き閉包を持つ。

`mixedResidueBalancedCriticalPeak_fill` は**すべての当該構成子**について構造帰納し、`joinable` と `classEq` で局所合流と商class一致を証明する。任意の平行七セル履歴の比較可能性、global thinness、独立九セル、元sourceのstrict Eqは主張しない。

## 2. #3238 失敗全文の検査と統合境界

旧PR #3238の新規Lean **783行、43宣言すべて**と依存Qi v5.06、統合済みQi v5.07 のソース・CIを照合した。

- 失敗CI [#42332655036](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42332655036) の主原因は旧ファイル570–585行の `sevenTotalReductionParity (mixedResidueDoubleFirst w)` / `(...BalancedFirst w)` における依存型添字 `long` / `short` の推論不能。4式を `(long := long) (short := short)` 明示に修正し、旧PR head `ec402ae35a22b4cf9c2c6584119818cf8a8bdb9d` にコミットした。
- #3238 の43宣言のうち**30宣言の識別子**が既マージの正式 #3237 と重複。旧PRはmainと競合し、そのままマージ不可。#3238はDraft / OPEN / 未マージで維持し、修正と重複調査のコメントを記録した。
- 非重複のbalanced-unit overlapと整数V非降下のみを、新正本mainを基点に #3240 へ分離した。重複する `MixedResidueEightCell` 等の再宣言は一切しない。
- #3240の初回CI [#42336110088](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42336110088) では、追加11宣言の証明本体と公理監査は通り、`KuuOSFormal` import位置と非計算section末尾の2構文エラーを検出。両者を構文・スコープ規則に従い修正して、最終 [#42336330332](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42336330332) で全件SUCCESSを確認した。

この修正は **append-only / tighten-only / overwrite-forbidden / same-root** を遵守。元F55/P77/GK5CG、元自由七セルType、旧独立八セルType、strict Eq interpreterの障害を保持する。

## 3. 次の研究境界

次は Qi v5.08。現行 `MixedResidueEightCell` に保存される `(V mod 2, R mod 2, U mod 2)` では検出できない、真正かつ全構成子保存が証明可能な高次obstructionを探索する。

最初に既存 `mixedResidue` と `doubleComposite`、`unitDiamond`、`balancedUnit` などで合流済みの局所critical pairを除外する。局所比較不能性を証明できない限り、新しい独立presentationの生成元を追加しない。旧sourceのstrict Eqと新商Eqを決して同一視しない。
