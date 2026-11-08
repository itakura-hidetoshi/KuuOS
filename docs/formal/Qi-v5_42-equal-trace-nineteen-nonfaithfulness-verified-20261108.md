# Qi v5.42 — 同一fine履歴の19D非同値・長さ境界transportのkernel完全分類

2026年11月8日 JST。Canonical repository: `itakura-hidetoshi/KuuOS`、branch: `main`。
前段Qi v5.41の定理 #3352・公開import #3353・正式記録 #3354はすべてMERGED。元F55/P77/GK5CG、元6D〜19DのType値証拠、過去の独立selected presentationと履歴、公開root107、固定Lean/mathlib、保護Draft PR #1558を変更しない。運用はappend-only／tighten-only／overwrite-forbidden／same-root。

## 1. GitHub MCP認証と形式成果物

| 項目 | 確認結果 |
|---|---|
| 定理PR | [#3355](https://github.com/itakura-hidetoshi/KuuOS/pull/3355) MERGED |
| 定理source HEAD | `43fdbeb150002619d7ca9807a269ac29c24f393b` |
| 定理test-merge HEAD | `ddbc5b213d8bb6d0ee70ffd3ee73128e88b6e75a` |
| 定理squash main | `d28e0b630820ad39b89583d09f7d8406ceac2a44` |
| 定理source／test-merge／squash Git tree | `8af90b11d1243ad4567c67304265b3fe6b1d1b4e` 完全一致 |
| 定理exact-source CI | [#42480163503](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42480163503) SUCCESS |
| Scoped Strict Lean | **9,094 / 9,094 SUCCESS** |
| Governance | 5 / 5 SUCCESS |
| 新規宣言公理監査 | 15 / 15（公理不要7件／標準公理のみ8件） |
| 新規sorryAx・変更Lean error／warning | なし／0／0 |
| 変更範囲 | 新規Lean1件・370行追加・既存ファイル削除0 |
| 公開import PR | [#3356](https://github.com/itakura-hidetoshi/KuuOS/pull/3356) MERGED |
| 公開source HEAD | `6a00d825f0061d8c30ba9b145a7819aa6252827e` |
| 公開test-merge HEAD | `830fb6c9d28fd3aa46dd90075b0944c5bc06891f` |
| 公開squash main | `4ed9c490846c04c5b8639e8df98e3d913bb4ed6c` |
| 公開source／test-merge／squash Git tree | `25870d130ca855f9cc2456cfc7b452882f659ad3` 完全一致 |
| 公開exact-source CI | [#42480594351](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42480594351) SUCCESS |
| KuuOSFormal全体Strict Lean | **10,355 / 10,355 SUCCESS** |
| 公開Governance | 30 / 30 SUCCESS |
| 公開差分 | `formal/KuuOSFormal.lean`にimport1行追加、削除0 |
| 固定Lean | `v4.30.0-rc2` |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4形式証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77EqualTraceNineteenNonfaithfulnessV5_42.lean)。

## 2. 元selected 19D比較が保存する新しい不変量

v5.37の独立`SelectedContextualEighteen`は`inherited`、`whiskerLeft`、`whiskerRight`、`strict`、`reverse`、`chain`の6構成子を持つ。既存`SelectedLocalNineteen`の5生成元は`strict`、元18D `inherited`への`unitPrepend`／`unitAppend`、比較の`reverse`／`chain`に限られる。

新しい`selectedContextEighteenActiveChainCount`は、raw18D構文の`chain`で左右の外側七セル順序履歴の連結が**空でないとき**だけ1を追加する自然数不変量である。旧`inherited`と`strict`は空の外側履歴を持つため、従来の19D単位貼合せの2生成元ではこの数が変わらない。`selectedLocalNineteen_preservesActiveChainCount`は5生成元すべてで保存することをLean4で証明。

`selectedNineteenActiveChainOnQuotient`は、この証明を使って真正同一fiberの19D証拠商に`Quotient.lift`で値を降下させる。既存の完全順序`List Bool` traceとは**別**の独立した商上観測であり、raw先頭constructor tagを大域化しない。

## 3. 同一完全fine履歴でも19D商で異なる真正証拠

真正元18D証拠Mから、既存v5.38の正しいLR二重文脈輸送 `X = selectedEighteenLeftAfterRight(M)` を取る。Xの外側履歴は `false :: true :: Trace(M)` なので長さが2以上。

同じ厳密な17D始終点の依存fiber内で、新しい生18D値 `Y = chain (strict source) X` を構成する（`selectedMixedLeftStrictPrepend`）。**新しい19D unit比較生成元は追加しない**。

`selectedMixedLeftStrictPrepend_trace`は `Trace(Y) = Trace(X)` を完全な順序付きリスト等式として証明する。一方`selectedMixedLeftStrictPrepend_activeChainCount`はXの外側履歴が非空なら `Active(Y) = Active(X) + 1` と証明する。真正19D比較はActiveを保存するため、`selectedMixedLeftStrictPrepend_classDistinct`は同一fiberで `[X]₁₉ ≠ [Y]₁₉` を証明し、`selectedMixedLeftStrictPrepend_noLocal`は両者間の真正`SelectedLocalNineteen` Type値比較の非存在まで示す。

ここでは**完全fine trace一致は19D商の証拠一致を意味しない**。同じ履歴長どころか履歴リスト全体が一致しても、局所19D比較が存在するとは限らない。この反例は元のselected presentationに相対的であり、別のpresentationでの比較まで否定するものではない。

## 4. v5.41の非定数transportのkernel完全分類

v5.41の実構成された`selectedMixedLengthBoundary M`はsourceの完全traceの**長さのみ**を符号化し、真正RL証拠列`selectedMixedRightTracePower`に送る。`selectedMixedLengthRawTransport_eq_of_length`は同じsource履歴長なら像のraw18D証拠値が一致することを示す。

v5.41で証明済みの長さ反映と組み合わせ、`selectedMixedLengthDescend_eq_iff_traceLength`は実際の異なる19D商型間で、任意のq₁,q₂に対して次の必要十分条件を証明する。

```text
descend_length(q₁) = descend_length(q₂)
    ↔ length(Trace(q₁)) = length(Trace(q₂))
```

したがって同じ完全履歴を持ちつつ元19D商で異なる前節の[X]と[Y]は、像で一致する（`selectedMixedLengthDescend_collapsesStrictPrepend`）。これにより`selectedMixedLengthDescend_notInjective`は、v5.41の**具体的な非定数**商輸送の非単射性をLean4で証明する。

`selectedMixedLengthBoundary_noReflection`および`selectedMixedFaithful_notLengthBoundary`は、この具体的境界では全source19D Type値比較を反映できず、v5.40の強い`SelectedMixedNineteenFaithfulBoundary.reflectLocal`を付けられないことを形式証明する。

## 5. 権威境界・次段

**認証済み：** 第2の真正19D商上観測ActiveChain、同一fine履歴・異なる19D商クラスの具体的構成、v5.41境界のkernel iff長さ、非定数かつ非単射の具体的実例、その境界に対する比較反映不可能性。

**未認証／NO_DATA：** **すべての**境界transportの非忠実性。とりわけ長さとActiveChainの両方を保つ別のtransportが元のすべてのType値19D比較を反映するかは未構成。全域swap自然性、真正異fiber20D高次交換、元証拠の生Eqも未認証。今回の一つの写像に対する非単射を一般の不可能性へ昇格させない。

**次段Qi v5.43：** `(length(Trace), ActiveChain)` の2変量の19D商観測を独立に構成し、これらを区別する非定数境界transportの型付き実装と、残る同一観測fiberのobstructionを検討する。完全なType値比較反映は別証明書のまま維持する。

本書はdocs-onlyの正式記録。Lean/import/workflow/固定pinは変更せず、文書専用Governance・Core Autonomyだけを検証する。
