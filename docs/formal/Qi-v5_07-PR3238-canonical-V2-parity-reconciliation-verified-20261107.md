# Qi v5.07 — PR #3238の正本照合とV法2・U偶奇補助API統合

## 正本／統合結果

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。

この記録は、当初DraftでCI不成功だった [PR #3238](https://github.com/itakura-hidetoshi/KuuOS/pull/3238) を、すでに検証・統合されたQi v5.07の正本定理PR #3237と補完PR #3240、およびQi v5.08定理PR #3242に照合して、**重複定義を統合せず、未統合の補助APIだけを同じ#3238からマージした**正式記録である。

| 検証項目 | 結果 |
|---|---|
| 対象PR | [#3238](https://github.com/itakura-hidetoshi/KuuOS/pull/3238) **MERGED** |
| 正本main基点 | `973b5cd0bfa3af4ad546bdd3c25495e5e9517b50` |
| 旧Draft HEAD | `ec402ae35a22b4cf9c2c6584119818cf8a8bdb9d` |
| 重複解消コミット（PR head） | `11a2d4b5f56d30d2897c0f4a40490619583c64da` |
| PR head両親 | 旧Draft HEAD／正本main（Git履歴追記・forceなし） |
| 定理squash SHA | `4caa219f55f69874c6745e64df1100c7395680dd` |
| exact-source CI | [#42370963952](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42370963952) **SUCCESS** |
| Strict Lean | **10,321／10,321 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | **7宣言**、`propext`・`Classical.choice`・`Quot.sound` のみ |
| `sorryAx` | **なし** |
| 変更Lean warning／error | **0／0** |
| source/test-merge Git tree | `de4e966a6cbd86e4230c75d26e19d8a3977565f1` **完全一致** |
| source HEAD | `11a2d4b5f56d30d2897c0f4a40490619583c64da` |
| CI test-merge HEAD | `9f43c96261ae99a4e0ae50630b372df7e01d1d4e` |
| Lean/mathlib pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、root **107不変** |
| 保護PR #1558 | **Draft／OPEN／未マージ不変** |

[今回のLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedResidueV2CompatibilityPR3238.lean) · [元Qi v5.07定理](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedResidueMinimalHigherCompletionV5_07.lean) · [Qi v5.07補完](Qi-v5_07-balanced-unit-mixed-peak-integer-V-supplement.md)

## 変更前の失敗と数学的重複

旧PR #3238 の新規Lean **783行・43宣言全文**と、その依存するQi v5.06／v5.07の定義および失敗CI #42332655036 を照合した。最初のLean elaboration失敗は、旧570–585行で `sevenTotalReductionParity` の引数に対する型付き `long`・`short` 添字推論が不足したこと。4式で `(long := long) (short := short)` を明示し、旧HEAD `ec402ae35a22b4cf9c2c6584119818cf8a8bdb9d` に修正済み。

ただし、**旧43宣言中30宣言は既マージの正本#3237と同名**であり、両者を読み込むと旧・新の独立 `MixedResidueEightCell` 定義や商が衝突する。旧実装のうち数学的に固有のbalanced-unit mixed peakと整数V非降下は、別途#3240（証明）／#3241（記録）でマージ・形式検証済み。さらにQi v5.08の自由四重五角形obstructionは#3242／#3244で検証済み。

**本PRの統合済み差分**は、旧Leanの重複ファイルを再導入せず、既存sourceを一文字も上書きしない**新規補助Leanモジュール115行＋`KuuOSFormal` import1行**のみ。旧Draftの原ファイルはGit履歴の親コミットに保持した。現在のmainに再配置・再命名された別の競合する八セルTypeは存在しない。

## 形式的成果：残る未統合APIを再利用可能にした

新規モジュール `QiWuxingGK5CHP77MixedResidueV2CompatibilityPR3238.lean` は、すでに証明された真正 `sevenMixedResidueFirst/Second` を、現行選択商 `mixedResidueHistorySetoid` 上でそのまま扱う。

- `sevenMixedResidue_totalParityValues`：真正V=3・5の両履歴でV法2が1という旧APIを、正本のvParityValues定理へ厳密接続。
- `mixedResidueEightCell_preservesTotalReductionParity`：現行比較全構成子の保存証明を、正本 `mixedResidueEightCell_preservesVParity` から再利用。
- `mixedResidueHistoryV2`：**整数値 `ℤ` のV法2代表観測量**を、現行の**同一** `MixedResidueHistory` 商に `Quotient.lift` で降下。
- `mixedResidueHistoryV2_onClass`：元七セル履歴の具体的代表における計算則。
- `mixedResidueHistoryUnitCountParity` および `..._onClass`：旧名のBool U偶奇観測量を、正本 `mixedResidueHistoryUnitParity` と定義的に同一視。
- `mixedResidueHistoryV2_boolCompatibility`：**全商class**で `decide(mixedResidueHistoryV2 q = 1)=mixedResidueHistoryVParity q` を証明。

数学的には次を正確に区別する：

```text
元のSevenRewrite raw Type値 ≠ 高次商class
ℤ値V mod 2 observer       ↔ Bool値V mod 2 observer（互換性は定理）
新しい比較生成元          0個
新しい九セル              0個
元source strict Eq昇格    なし
```

今回の`Quotient.lift`は、元の自由七セルのstrict Eqを証明するものでも、元F55/P77/GK5CG sourceの同一視を認可するものでもない。

## 次段

Qi v5.08で証明済みの新しい元四重結合子の構文的指紋 `Φ` と、現行法2 observerを区別して保持する。次のQi v5.09では、この五角形高次obstructionを充填する**独立presentationの最小比較生成元と局所critical pair**について、真正元sourceとの整合性・旧比較の保持・新商での不変量の可否を証明する。無条件のglobal thinness、新たな九セル存在、strict Eq昇格は仮定しない。

運用：append-only／tighten-only／overwrite-forbidden／same-root。
