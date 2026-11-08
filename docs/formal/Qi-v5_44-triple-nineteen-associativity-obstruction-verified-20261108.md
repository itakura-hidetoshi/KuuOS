# Qi v5.44 — 真正19D三変量境界transportと結合順序obstruction

2026年11月8日 JST。Canonical repository: `itakura-hidetoshi/KuuOS`、branch: `main`。
本書は既存のselected 19D presentationに相対的なLean4形式成果物を記録する。元F55/P77/GK5CG、元6D〜19D Type値証拠、別の独立selected presentation、公開root107、固定Lean/mathlib、保護PR #1558は変更しない。

## 1. GitHub MCPで確認した検証・統合

| 項目 | 結果 |
|---|---|
| 定理PR | [#3361](https://github.com/itakura-hidetoshi/KuuOS/pull/3361) MERGED |
| 定理source HEAD | `be9617d530061e7d75718e953fc48361ab5c3b67` |
| 定理test-merge | `f52233b4bd114f40ccb6b1339d154bb16ebe9a2a` |
| 定理squash main | `c9c81251f44d093330581eec8ed0f799c768250c` |
| source／test-merge／squash Git tree | `ff6443bf65332c269ba8627f808af3987d26c731` 完全一致 |
| 定理exact-source CI | [#42485095326](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42485095326) SUCCESS |
| Scoped Strict Lean | **9,096 / 9,096 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 公理監査 | **33 / 33**（公理不要14／標準公理のみ19） |
| `sorryAx`／変更Lean error／warning | **なし／0／0** |
| 定理変更 | 新規Lean1件633行追加、既存削除0 |
| 公開import PR | [#3362](https://github.com/itakura-hidetoshi/KuuOS/pull/3362) MERGED |
| 公開source HEAD | `3ae77ed545752f32c724840fd5deb0d6859e71bf` |
| 公開test-merge | `3993cc13475eec9658a085cb810eb50afa1f1092` |
| 公開squash main | `876d97109ca6e93200a102b15ef09952825c7e13` |
| 公開source／test-merge／squash Git tree | `f21ac36caa9dde481c47c3fc182f188357275bc1` 完全一致 |
| 公開exact-source CI | [#42485499436](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42485499436) SUCCESS |
| 公開KuuOSFormal Strict Lean | **10,357 / 10,357 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開変更 | `formal/KuuOSFormal.lean`にimport1行追加、削除0 |
| Lean pin | `v4.30.0-rc2` |
| mathlib pin | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Qi v5.44 Lean4定理全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TripleNineteenAssocObstructionV5_44.lean)。

## 2. 真正19D商の三変量観測

Qi v5.43までの`Trace`・`ActiveChain`・`ReverseCount`は、既存の真正`SelectedLocalNineteen`比較5構成子それぞれで保存される。これらを組み合わせ、

```text
I₃(q) = ((length(Trace(q)), ActiveChain(q)), ReverseCount(q))
```

を`selectedNineteenTripleObservation`として同一の17D依存端点fiberの19D証拠商上に構成。`selectedLocalNineteen_preservesTriple`、`selectedNineteenTriple_onClass`、`selectedNineteenTriple_eq_iff`で保存・評価・成分の必要十分条件を証明した。元raw 18D Type値Eqとは同一視していない。

## 3. 三変量を識別する具体的な型付きLR→RL transport

入れ子`Nat.pair`と既存`selectedMixedLengthCode`により`selectedMixedTripleCode`の単射性を証明。真正RL18D証拠から作る既存`selectedMixedRightTracePower`を使い、source三変量を指数に符号化した`selectedMixedTripleRawTransport`を構成した。`selectedMixedTripleBoundary.localTransport`は元の真正Type値19D比較を入力とし、輸送先の真正`strict`比較を実際に返す。`selectedMixedTripleAnchored`は指定LR証拠を元RL証拠へ輸送する比較を保持する。

商降下の像の同一性について、**この具体的境界**に限り

```text
descend_triple(q₁) = descend_triple(q₂)
   ↔ I₃(q₁) = I₃(q₂)
```

を`selectedMixedTripleDescend_eq_iff_observation`で証明した。v5.43では潰れていた`reverse (reverse X)`との差は、`selectedMixedTripleDescend_separatesDoubleReverse`で区別される。

**注意：** これはsource側の三変量の一致を像の19D商クラスの一致と対応させる分類であって、sourceの三変量とtargetの三変量が全域で同じ値になるという主張ではない。

## 4. 同一三変量を残す、真の括弧付け障害

`selectedContextEighteenLeftNestedCount`は、生18D構文の`chain`で左側がさらに`chain`である箇所を数える。既存`SelectedLocalNineteen`5構成子すべての保存を`selectedLocalNineteen_preservesLeftNestedCount`で構造帰納法により証明し、`selectedNineteenLeftNestedOnQuotient`で真正19D商へ降下した。

同一依存端点の真正生18D値`X`に対し、

```text
L(X) = chain (chain X (reverse X)) X
R(X) = chain X (chain (reverse X) X)
```

を構成。`Trace(L)=Trace(R)`と`ReverseCount(L)=ReverseCount(R)`は任意`X`で成立する。外側traceが非空なら`ActiveChain(L)=ActiveChain(R)`も成立する。一方`LeftNestedCount(L)=LeftNestedCount(R)+1`が常に成立し、元19D商では`[L]₁₉ ≠ [R]₁₉`、既存`SelectedLocalNineteen` Type値比較も非存在と証明。

真正LR二重文脈証拠のtraceは非空なので、この実例を元のLR 19D fiberで構成できる。`selectedMixedTripleDescend_notInjective`と`selectedMixedTripleBoundary_noReflection`は、**今回実装した三変量境界**が非単射で、完全19D比較反映を持たないことを証明。`selectedMixedTripleAnchored_chosenSwap`は指定点でのcoarse swap観測一致のみ認証する。

## 5. 初回CI失敗と修正理由

初回と再検証では、依存endpointの変わる`SelectedContextualEighteen`再帰をsection固定添字のまま扱ったことに由来するelaboration failure、および一般`simp`の展開・正値条件を指定しないためのActiveChain算術証明の失敗があった。再帰不変量を端点多相の明示的定義にし、算術を局所的な`change`・正値条件・`omega`に変更した。元のType値・仮定・旧定理には手を加えず、最終HEADのStrict LeanがSUCCESSとなった。エラーを`sorry`や追加公理で回避していない。

## 6. 認証境界と次段

**認証済み：** 19D三変量商観測、型付きanchored LR→RL境界、source三変量による具体的kernelの必要十分条件、二重反転差の識別、同一三変量・異なる19D商クラスの真正括弧付け障害、その境界の非忠実性と指定点swap観測。

**未認証／NO_DATA：** 別の忠実境界が存在するか否か、全域swap自然性、元raw Type値Eq、旧presentationを横断する20D交換、無条件gluing。局所証拠から一般の不可能性へ昇格させない。

**次段Qi v5.45：** `LeftNestedCount`を加えた四変量の商上観測を型付き境界へ運び、その新境界でも保持される比較障害と観測の限界を調べる。元Type値、独立presentation、運用権限境界は保持する。

本PRはdocs-onlyであり、Strict Leanは実行しない。append-only／tighten-only／overwrite-forbidden／same-root。
