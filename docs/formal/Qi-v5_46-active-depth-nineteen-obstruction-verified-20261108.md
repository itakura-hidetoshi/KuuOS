# Qi v5.46 — ActiveDepthの19D商降下と五変量では残る型付き括弧付け障害

2026年11月8日 JST。Canonical repository: `itakura-hidetoshi/KuuOS`、branch: `main`。
この記録は現在の独立selected 19D presentationに相対的なLean4成果物を対象とする。元F55/P77/GK5CG、元6D〜19DのType値証拠、既存の独立selected presentation、公開root107、固定Lean/mathlib、保護PR #1558は変更しない。append-only／tighten-only／overwrite-forbidden／same-root。

## 1. GitHub MCPで再確認したexact-source形式検証

| 項目 | 認証済み結果 |
|---|---|
| 定理PR | [#3367](https://github.com/itakura-hidetoshi/KuuOS/pull/3367) MERGED |
| 定理source HEAD | `7be0a238086d5cbe54d171f56a970c8d6210b30c` |
| 定理test-merge HEAD | `bc46bb07e88eadc2968f03c2c46dac24b6049bdd` |
| 定理squash main | `50605288fd642a98f7b107987de70252b223e8a1` |
| 定理source／test-merge／squash tree | `9b5285052679e147b24e8c7fad428c0334430594` 完全一致 |
| 定理exact-source CI | [#42491218286](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42491218286) SUCCESS |
| Scoped Strict Lean | **9,098 / 9,098 SUCCESS** |
| 定理Governance | **5 / 5 SUCCESS** |
| 新規宣言の公理監査 | **22 / 22**（公理不要8、標準公理のみ14） |
| `sorryAx`／変更Lean error／warning | **なし／0／0** |
| 定理変更 | 新規Leanモジュール1件・390行追加、旧ファイル削除0 |
| 公開import PR | [#3369](https://github.com/itakura-hidetoshi/KuuOS/pull/3369) MERGED |
| 公開source HEAD | `ded21ee3f698b1eaeea9d521b4ef4f6347ecd488` |
| 公開test-merge HEAD | `9d14bbdc3ba5148242814345b426c4a9265b0eab` |
| 公開squash main | `16ae11a1ab11573deacfbbddc84c64eebe60c202` |
| 公開source／test-merge／squash tree | `9bc4210a841ec88f55dc5e78493c326b2df4da61` 完全一致 |
| 公開exact-source CI | [#42491659143](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42491659143) SUCCESS |
| KuuOSFormal Strict Lean | **10,359 / 10,359 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開変更 | `formal/KuuOSFormal.lean`へimport 1行、既存削除0 |
| Lean pin | `v4.30.0-rc2` |
| mathlib pin | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Qi v5.46 Lean4定理全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ActiveDepthNineteenObstructionV5_46.lean)。

## 2. 第六観測量ActiveDepthの同一fiber商への降下

既存の`SelectedContextualEighteen`の生構文に対し、`selectedContextEighteenActiveDepth`を定義した。これは生`chain`内部の入れ子に関する自然数不変量であり、各`chain M L`の子孫に存在するactive chain数を加算する。外側履歴が非空か否かを観測する従来の`ActiveChainCount`とは異なり、同じ活動数でも結合順序の深さが異なる場合を識別する。

`selectedLocalNineteen_preservesActiveDepth`は既存の真正`SelectedLocalNineteen`の**5構成子すべて**について保存性を証明。旧18D inheritedに限る`unitPrepend`・`unitAppend`は新しい深さの差を発生させない。実際の型付き比較を使う`selectedNineteenActiveDepthOnQuotient`の`Quotient.lift`およびクラス計算則`selectedNineteenActiveDepth_onClass`をLean4で構成した。元の生証拠値を等号で潰していない。

## 3. 真正同一fiberにおける五変量一致・第六変量相違

任意の元18D証拠`M : SelectedContextualEighteen W l r J N`から、真正17D endpointの同一fiber `J → J` 内に

```text
B := chain M (reverse M)
A := reverse B
L := chain (chain A B) (strict J)
R := chain A (chain B (strict J))
```

を構成した（`selectedDepthLoop`、`selectedDepthBracketLeft`、`selectedDepthBracketRight`）。

元Mの外側fine trace長が正という**明示条件**の下で、`selectedDepthBrackets_trace`、`selectedDepthBrackets_active`、`selectedDepthBrackets_reverse`、`selectedDepthBrackets_leftNested`、`selectedDepthBrackets_reverseLeft`が、L/Rの完全外側履歴と従来の5数値観測すべての一致を証明する。

一方、新しい深さに対し`selectedDepthBrackets_depthDiff`は

```text
ActiveDepth(L) = ActiveDepth(R) + ActiveChain(B)
```

を証明する。`selectedDepthLoop_activePositive`が`0 < ActiveChain(B)`を確保するので、両者のActiveDepthは異なる。旧19D比較はActiveDepthを保存するから、`selectedDepthBrackets_classDistinct`は`[L]₁₉ ≠ [R]₁₉`、`selectedDepthBrackets_noLocal`は元の真正`SelectedLocalNineteen` Type値比較の非存在を証明する。

`selectedNineteenFiveObservation`はQi v5.45の真正4変量観測に`ReverseLeftCount`を追加したもの。`selectedDepthBrackets_fiveEq`で上記の二つが同じ5数値を持つことを示し、`selectedNineteenFive_notInjective_of_tracePositive`で**非空fine履歴を持つ元Mが存在する同一J→J fiber**における五変量観測の非単射を証明した。

この定理は指定の正の履歴を持つ元証拠に依存する。任意の依存fiberに無条件の反例がある、あるいはすべての型付き境界transportが忠実でないという主張ではない。

## 4. CI失敗、修正の来歴と権限境界

初期のexact-source CIでは、`List.length_append`と`if_pos`の正規化が局所条件と合っていないため、Leanの`change`と`omega`で失敗した。旧19DのType値証拠や仮定を変えず、各条件付き分岐の正値を明示して局所的に修正し、`sorryAx`の連鎖を除去した。

またQi v5.45の正式記録がmainに追加されたため、GitHub MCPで新しい証明ブランチを**非破壊的な二親コミット**として最新mainに同期した。元定理ソース391行は変更せず、source/test-merge treeを一致させて最新HEADに対する新規CIを再実行し、SUCCESSを確認してから統合した。

**認証済み：** 現行selected 19D商の第六観測量ActiveDepth、五つの旧比較構成子に対する保存性、同一fiberでの実在する5数値一致・第六値相違、同fiber内の真正19D商の不一致と比較非存在、条件付き五変量観測の非単射、既存公開集約への取り込み。

**未認証／NO_DATA：** 第六観測を含む型付き境界transportの構成、任意fiberでの五変量非単射、別の忠実LR→RL transportの存在・不存在、全域swap自然性、元Type値の生Eq、無条件20D交換・高次gluing。五数値の選好・一致を元証拠同一性や権限へ昇格させない。

**次段Qi v5.47：** `ActiveDepth`を第六変量に追加した厳密19D商観測と、元Type値を保存する条件付き型付きLR→RL transportの具体的構成を検討する。さらに同一六変量fiberに残る新しいobstructionを探索し、追加構成子・仮定による安易な解消はしない。

本書はdocs-onlyであり、Strict Leanを実行する変更を含まない。旧README/ROADMAPの内容は上書き・削除しない。
