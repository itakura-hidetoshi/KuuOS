# Qi v5.43 — 19D二変量境界transportの厳密kernelと二重反転obstruction

2026年11月8日 JST。Canonical repository: `itakura-hidetoshi/KuuOS`、branch: `main`。本記録はQi v5.43の型付きLean4形式成果物とexact-source CIの範囲だけを認証する。既存F55/P77/GK5CG、元6D〜19DのType値証拠、独立selected presentation、公開root107、Lean/mathlib固定、保護PR #1558を変更しない。

## 1. GitHub MCPによる検証・統合の記録

| 項目 | GitHubで確認済みの結果 |
|---|---|
| 定理PR | [#3358](https://github.com/itakura-hidetoshi/KuuOS/pull/3358) MERGED |
| 定理source HEAD | `60ae70db7a48df743dfb7dfec64e6f87531d345e` |
| 定理test-merge HEAD | `7e10c14c8bc0e7cb1e1290b2370e026fa0cc0c67` |
| 定理squash main | `e9674294cd133ef3de99ae073ed7f7ed67aadd17` |
| 定理source／test-merge／squash Git tree | `f5a435173cfa298a6b13320b8581062b14f2ba98` 完全一致 |
| 定理exact-source CI | [#42481878276](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42481878276) SUCCESS |
| Scoped Strict Lean | **9,095 / 9,095 SUCCESS** |
| 定理Governance | **5 / 5 SUCCESS** |
| 新規宣言公理監査 | **27 / 27**（公理不要15、標準公理のみ12） |
| `sorryAx`／変更Lean error／warning | **なし／0／0** |
| 定理差分 | 新規Leanモジュール1件・564行追加、既存削除0 |
| 公開import PR | [#3359](https://github.com/itakura-hidetoshi/KuuOS/pull/3359) MERGED |
| 公開source HEAD | `851cdc0ad80f182327be611cd4f5a9379f5669ce` |
| 公開test-merge HEAD | `712bcc04aa69204372f4866d205b097e5a40b2cc` |
| 公開squash main | `cb7fa0919fbf8bd557712176d6ce1aa9068823ae` |
| 公開source／test-merge／squash Git tree | `c13201b3eaa826a42f5694958a6af25940c6dfdd` 完全一致 |
| 公開exact-source CI | [#42482312495](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42482312495) SUCCESS |
| 公開KuuOSFormal Strict Lean | **10,356 / 10,356 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開差分 | `formal/KuuOSFormal.lean`へimport1行追加、削除0 |
| 固定Lean | `v4.30.0-rc2` |
| mathlib pin | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Qi v5.43 Lean4定理全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77PairedNineteenObstructionV5_43.lean)。

## 2. 真正19D商上の二変量観測

元v5.37/v5.42の証明済み不変量、完全順序付き外側履歴`selectedNineteenTraceOnQuotient`と、`selectedNineteenActiveChainOnQuotient`を組にして

```text
I(q) = (length(Trace(q)), ActiveChain(q)) : Nat × Nat
```

を`selectedNineteenLengthActiveObservation`として各々の厳密な17D始終点fiberの真正19D商上に定義した。`selectedNineteenLengthActive_onClass`で元の生18D証拠値に対する計算則、`selectedNineteenLengthActive_eq_iff`で二つの成分がともに一致することと二変量観測Eqの同値を証明した。観測商を元Type値証拠同一性と同一視していない。

## 3. 二変量の一致を反映する実在する型付き境界

固定mathlibの`Nat.pair`（`Mathlib.Data.Nat.Pairing`）と既存の`selectedMixedLengthCode`で、指定LR証拠の二変量baseを0へ送り、残りを単射的に符号化する`selectedMixedPairedCode`を定義。`selectedMixedPairedCode_injective`を形式証明した。

真正RL18D証拠の既証明列`P_R(n)`へ、sourceの二変量符号を指数として渡す`selectedMixedPairedRawTransport`を構成。元の指定LR証拠は真正RL証拠に写り、`selectedMixedPairedAnchored`が実際の指定19D比較のType値を保持する。sourceの真正19D比較はTraceとActiveを保存するので、輸送先の真正`SelectedLocalNineteen.strict`により`selectedMixedPairedBoundary.localTransport`を構成した。

最も強い証明済みのkernel分類は、任意の同じLR 19D fiberの商クラス`q₁,q₂`についての

```text
descend_paired(q₁) = descend_paired(q₂)  ↔  I(q₁) = I(q₂)
```

（`selectedMixedPairedDescend_eq_iff_observation`）である。これは**この具体的なtransportについて**二変量の等値関係を保存・反映するという主張で、sourceとtargetの数値的二変量そのものの全域一致や全域swap自然性は主張しない。v5.42の同一fine trace・Active差1の厳密なX/strict-prepend(X)は、この新しい境界では像が異なる（`selectedMixedPairedDescend_separatesStrictPrepend`）。

## 4. 同一二変量fiberに残る厳密なobstruction

新たに生18D構文の`reverse`構成子の回数`selectedContextEighteenReverseCount`を数え、既存`SelectedLocalNineteen`の5構成子すべてがこの数を保存することを証明。これを`selectedNineteenReverseCountOnQuotient`で真正19D商へ降下した。

任意の真正生18D値Xに対し、同一依存fiberで`D(X) = reverse(reverse(X))`を構成すると、

```text
Trace(D(X)) = Trace(X)
ActiveChain(D(X)) = ActiveChain(X)
ReverseCount(D(X)) = ReverseCount(X) + 2
```

がLean4で成立する。従って`I([D(X)]) = I([X])`だが、`[D(X)]₁₉ ≠ [X]₁₉`であり、`selectedNineteenLengthActive_notInjective`で二変量観測の非単射性を元18D証拠が存在するfiberごとに証明した。これは選択した19D presentationに相対的な証明である。

二変量境界のkernelはIのEqと正確に一致するため、`selectedMixedPairedDescend_notInjective`が具体的境界の非単射性を証明。`selectedMixedPairedBoundary_noReflection`がその境界に全`SelectedLocalNineteen`比較を逆向きに反映するType値証明書を付与できないことを形式証明する。

## 5. 権威境界と未構成領域

**認証済み：** 二変量の真正19D商観測、Nat.pairによる型付きanchored LR→RL輸送、全source商クラスでのkernel iff観測二変量Eq、同一fine traceだがActiveが異なる証拠の分離、二重反転による同一二変量・異なる19D商クラスの実例、その具体的輸送の非忠実性、指定証拠でのcoarse swap観測Eq。

**未認証／NO_DATA：** 別の完全忠実な境界transportの一般的存在・不存在、全sourceについてのswap自然性、元の生Type値のEq、異fiber20D交換・無条件高次gluing。二変量反映や選好だけを元証拠一致・降下・行為権限へ昇格させない。

**次段Qi v5.44：** 真正19D商上のReverseCountを含む観測フィルトレーションの段階的強化と、より強い観測に対してなお残るType値比較障害を探索する。既存presentationに新たな逆元キャンセル公理・交換公理を加えず、未構成の一般忠実性はNO_DATAのまま保持する。

本ファイルはdocs-onlyの形式検証記録であり、Strict Leanを再実行する変更を含まない。append-only／tighten-only／overwrite-forbidden／same-root。
