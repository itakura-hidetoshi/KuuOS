# Qi v5.49 — 真正19D単位3形と型付きraw文脈の合同性・降下条件：Lean4正式証明記録

記録日：2026-11-09 JST

## 1. 根拠と現行正本

Repository: `itakura-hidetoshi/KuuOS`、canonical branch: `main`。
本記録が根拠とする定理・公開集約の統合済みmain HEADは `4331d77435139483fad55522841c5f0084c436c0`。

- [定理PR #3377](https://github.com/itakura-hidetoshi/KuuOS/pull/3377) — MERGED、統合SHA `7689ba5a79389a4c28f855cc99f000b3d246dfe4`。
- [公開import PR #3378](https://github.com/itakura-hidetoshi/KuuOS/pull/3378) — MERGED、統合SHA `4331d77435139483fad55522841c5f0084c436c0`。
- [Lean形式証明全文](https://github.com/itakura-hidetoshi/KuuOS/blob/7689ba5a79389a4c28f855cc99f000b3d246dfe4/formal/KUOS/Architecture/QiWuxingGK5CHP77ContextCongruenceGatesV5_49.lean) — 新規396行のみ。既存定理・構成子・元証拠を変更しない。
- 公開集約 `formal/KuuOSFormal.lean` — importを1行追加、既存全importを保持。

現行 `SelectedLocalNineteen` は元の5構成子（`strict`、`unitPrepend`、`unitAppend`、比較の `reverse`、比較の `chain`）のまま。原 `SelectedContextualEighteen` のraw `reverse` / raw `chain` に対する一般合同性は追加しない。

## 2. 型付き直接単位3形

実際に与えられた元 `M : SelectedLocalEighteen W l r J N` の同じ厳密17D endpoints `J→N` に対し：

```lean
variant inherited := .inherited M
variant prepend   := .chain (.strict J) (.inherited M)
variant append    := .chain (.inherited M) (.strict N)
```

新しい `SelectedNineteenDirectUnitVariant` は有限の表示選択であり、新しい19D比較生成元ではない。`selectedNineteenDirectUnitComparison` は三つの任意の組に対し、元の `SelectedLocalNineteen` のType値証拠を `unitPrepend` / `unitAppend` / 比較の対称・推移によって実際に構成する。

証明された関係：

```text
RawVariant : {inherited, prepend, append} → original raw18D typed fiber
Function.Injective RawVariant
Normal(RawVariant s) = inherited M            (all s)
[RawVariant s]₁₉ = [RawVariant t]₁₉             (all s,t)
¬ Function.Injective (fun s => [RawVariant s]₁₉)
```

raw構文が異なることは`selectedNineteenDirectUnitShapeTag`で元の構成子を観測して区別した。タグは**元19D商に降下する不変量ではない**。商の同一視が元raw構文の等号を意味することはない。

## 3. 局所的な非合同性の真正反例

元の比較 `prepend(M) ≃ inherited(M)` が存在する一方、次の元raw操作で囲んだ2証拠間には真正19D比較が存在しない：

- `raw reverse`：`reverse(prepend(M))` と `reverse(inherited(M))`。
- `strict-right raw chain`：`chain(prepend(M), strict N)` と `chain(inherited(M), strict N)`。
- `strict-left raw chain`：`chain(strict J, prepend(M))` と `chain(strict J, inherited(M))`。

各結論はv5.48の `selectedNineteenNormal_respects` と、異なる元raw構成子の不一致から導出される。比較証拠それ自体を対称にする`SelectedLocalNineteen.reverse`や、比較を合成する`SelectedLocalNineteen.chain`が失敗したわけではない。

さらに下記の必要十分条件へ接続し、この3つの**指定された元raw操作そのもの**を延長する商上の関数は（元の旧18D証拠Mが与えられた厳密fiberで）存在しないと証明した。あらゆる操作・あらゆるfiberで商写像が不可能とは主張していない。

## 4. 降下の必要十分条件（exact typed fiber）

`f : Raw(J,N) → Raw(S,T)` は、同じ基底の依存型indicesを保持したまま、指定された入力endpoint pairから指定された出力endpoint pairへのraw変換とする。

```text
(∀ {M L}, SelectedLocalNineteen M L →
          Nonempty (SelectedLocalNineteen (f M) (f L)))
  ↔ ∃ g : Quot(J,N) → Quot(S,T),
      ∀ M, g([M]) = [f(M)]
```

これが `selectedNineteenRawMap_descends_iff`。左辺は真正19D Type値比較を、少なくともNonemptyとして保存する条件であり、Quotient.liftの整合条件を証明する。逆向きも商の等式から`Quotient.exact`で従う。

v5.48の元raw証拠の型付き正規形を用いた同値な条件は：

```text
∀ M L, Normal(M) = Normal(L) →
       Normal(f M) = Normal(f L)
```

この保存条件と商への降下可能性の同値を`selectedNineteenRawMap_normalGate`で証明した。異なるdependent endpoint fiberのraw証拠同士を直接等号で同一視したわけではない。

## 5. 認証来歴

| 対象 | 結果 |
| --- | --- |
| 最終定理exact-source CI | [#42531490568](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42531490568) — SUCCESS |
| Scoped Strict Lean | **9,101 / 9,101** SUCCESS |
| 定理Governance | **5 / 5** SUCCESS |
| 新規宣言公理監査 | **19 / 19**、公理不要6、標準公理のみ13 |
| `sorryAx` | なし |
| 変更Lean error / warning | **0 / 0** |
| 公開exact-source CI | [#42532010897](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42532010897) — SUCCESS |
| KuuOSFormal Strict Lean | **10,362 / 10,362** SUCCESS |
| 公開Governance | **32 / 32** SUCCESS |

定理source HEAD `2621db24b79a101125cd09de868ad5c73872e11f`、test-merge `835f1ac6f2276e8ab0680126e1a8a1ca1c9fe234`、squash/統合 `7689ba5a79389a4c28f855cc99f000b3d246dfe4` のtreeは全て `081f8d72ac73282751991c79d59de3872fb360fe` で一致。

公開import source HEAD `c989345b0673e9b487e79bc388eb4ea2af19d441`、squash/統合 `4331d77435139483fad55522841c5f0084c436c0`、共通tree `aa23dc75bb63fb442fca8235eaef9a4fca6c2e5b`。source／test-merge／squash一致。

初回CI [#42530365376](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42530365376) の型エラー4件は、dependent raw構文の異種等号と、raw-map descent証明における暗黙fiber添字の未固定から生じた。元の構文形の有限観測タグと依存型の明示で修正した。

次回CI [#42530792303](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42530792303) では元raw構文の単射性証明中の `simp` による展開が4000000 heartbeatsを消費し失敗。`maxHeartbeats`を引き上げず、9個の有限constructor casesとtag値の明示的照合へ変更し、最終CIを成功させた。定理の仮定・依存関係・元証拠は一切緩めていない。

## 6. 全19宣言の機械的公理監査

最終CIの `#print axioms` 19宣言を逐一照合。公理依存はLeanの標準 `propext`・`Quot.sound` に限られ、非標準公理も `sorryAx` もない。`Classical.choice` は今回の19宣言に現れなかった。

| 宣言 | 公理依存 |
| --- | --- |
| `SelectedNineteenDirectUnitVariant` | なし |
| `selectedNineteenDirectUnitRaw` | なし |
| `selectedNineteenDirectUnitToInherited` | なし |
| `selectedNineteenDirectUnitComparison` | なし |
| `selectedNineteenDirectUnit_normal` | `propext` |
| `selectedNineteenDirectUnit_classEqual` | `Quot.sound` |
| `selectedNineteenDirectUnitShapeTag` | `propext` |
| `selectedNineteenDirectUnit_rawInjective` | `propext` |
| `selectedNineteenDirectUnit_classNotInjective` | `Quot.sound` |
| `selectedNineteenRawReverse_unitObstruction` | `propext` |
| `selectedNineteenRawRightStrict` | なし |
| `selectedNineteenRawRightStrict_unitObstruction` | `propext` |
| `selectedNineteenRawLeftStrict` | なし |
| `selectedNineteenRawLeftStrict_unitObstruction` | `propext` |
| `selectedNineteenRawMap_descends_iff` | `propext, Quot.sound` |
| `selectedNineteenRawMap_normalGate` | `propext, Quot.sound` |
| `selectedNineteenRawReverse_noDescent` | `propext, Quot.sound` |
| `selectedNineteenRawRightStrict_noDescent` | `propext, Quot.sound` |
| `selectedNineteenRawLeftStrict_noDescent` | `propext, Quot.sound` |

## 7. 権限境界と次の研究

構文タグのraw-level差異を商不変量と取り違えない。局所的比較・局所的非降下を、全域の不可能性や高次gluingへ昇格させない。必要条件と十分条件の提示は、適用権限やraw作用の構成そのものを保証しない。

固定toolchain `leanprover/lean4:v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、F55/P77/GK5CGおよび既存Type値証拠の保存、保護PR #1558 Draft／OPEN／未マージを維持。append-only／tighten-only／overwrite-forbidden／same-root。

次段Qi v5.50では、元の19D商を壊さず、typed raw context操作の安定化に**必要な追加比較生成元と、その最小の閉包・compatibility条件**を検討する。新presentationへ追加するなら旧presentationと別物として区別し、既存の不可能性を黙って消さない。

本PRは形式証明記録・README・ROADMAPのみを追加追記するdocs-only変更であり、Lean・import・workflow・固定pinは変更しない。
