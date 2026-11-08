# Qi v5.45 — 真正19D四変量境界とreverse-left順序obstruction

2026年11月8日 JST。正本は `itakura-hidetoshi/KuuOS` の `main`。本書は現行selected 19D比較presentationの下で実際にLean4が証明した範囲に限る。元F55/P77/GK5CG、生6D〜19DのType値証拠、独立した各selected presentation、公開root107、固定Lean/mathlib、保護PR #1558を維持する。

## 1. GitHub MCPによる形式成果物とCI認証

| 項目 | 認証済み |
|---|---|
| 定理PR | [#3364](https://github.com/itakura-hidetoshi/KuuOS/pull/3364) MERGED |
| 定理source HEAD | `38e696e2b7b7e98fd6e4c00dbf84610be39cbaf1` |
| 定理test-merge | `f6d55b30ddc8641e3170fa892af160ae22ac1621` |
| 定理squash main | `c588b62e15db04a5a5392dfd90dd0936b83d01f0` |
| 定理source／test-merge／squash Git tree | `5f8ace985761ca5ace8ba0c89df39ae932fe6d21` 完全一致 |
| 定理exact-source CI | [#42488399450](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42488399450) SUCCESS |
| Scoped Strict Lean | **9,097 / 9,097 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 公理監査 | **32 / 32**（公理不要17／標準公理のみ15） |
| `sorryAx`／変更Lean error／warning | **なし／0／0** |
| 定理差分 | 新規Lean1ファイル573行追加、既存削除0 |
| 公開import PR | [#3366](https://github.com/itakura-hidetoshi/KuuOS/pull/3366) MERGED |
| 公開source HEAD | `0c1415c289745145a45a43989bb5a8e59ee48e1f` |
| 公開test-merge | `26067dea4a94a71412286d30bab037c9fb9dd555` |
| 公開squash main | `142acd580369c944d7b425da980c3dae657f2a74` |
| 公開source／test-merge／squash Git tree | `6c4045ed5934f37cb87831fa87baff17435d7188` 完全一致 |
| 公開exact-source CI | [#42488848341](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42488848341) SUCCESS |
| 公開KuuOSFormal Strict Lean | **10,358 / 10,358 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開変更 | `formal/KuuOSFormal.lean` import1行追加、削除0 |
| 固定Lean | `v4.30.0-rc2` |
| mathlib pin | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Qi v5.45 Lean4定理全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FourNineteenReverseLeftObstructionV5_45.lean)。

## 2. 四変量の真正19D商観測

従来の三変量 `I₃=(length(Trace),ActiveChain,ReverseCount)` に、v5.44で証明済みの `LeftNestedCount` を追加した。

```text
I₄(q) = (I₃(q), LeftNestedCount(q))
```

`selectedLocalNineteen_preservesFour`は既存比較5構成子の保存を示し、`selectedNineteenFourObservation`は各厳密な17D dependent endpoint fiberの19D商へ降下する。`selectedNineteenFour_onClass`と`selectedNineteenFour_eq_iff`で生18D値との計算則と成分同値を証明。四変量を元のType値証拠Eqへ昇格させていない。

## 3. 四変量を区別する真正LR→RL型付き境界

入れ子の`Nat.pair`と既存`selectedMixedLengthCode`により`selectedMixedFourCode_injective`を証明。真正RL証拠の既存列`selectedMixedRightTracePower`へ四変量の単射符号を送る`selectedMixedFourRawTransport`を構成。元LRの真正`SelectedLocalNineteen`証拠を入力とし、targetの`strict`比較を返す`selectedMixedFourBoundary.localTransport`も実装した。`selectedMixedFourAnchored`は指定LR証拠と真正RL証拠の接続を保持する。

この**具体的な輸送**の商降下についてのみ、Lean4で

```text
descend_four(q₁) = descend_four(q₂) ↔ I₄(q₁) = I₄(q₂)
```

を`selectedMixedFourDescend_eq_iff_observation`として証明した。これによりv5.44の真の括弧付け異証拠対は今回の新境界で分離される（`selectedMixedFourDescend_separatesAssoc`）。ただし source と target で四変量の数値が全域で一致することや、一般の19D比較反映は主張しない。

## 4. 同一四変量でも異なる真正19D証拠

新しいraw18D不変量`selectedContextEighteenReverseLeftCount`は、`chain`の左辺の先頭構成子が`reverse`である節点を数える。旧`SelectedLocalNineteen`の5構成子がこれを保存することを証明し、`selectedNineteenReverseLeftOnQuotient`で商へ降下した。

任意の真正18D証拠`X : J → N`の同じ依存fiber内で、

```text
A(X) = chain (chain (strict J) (reverse (strict J))) X
B(X) = chain (chain (reverse (strict J)) (strict J)) X
```

を構成。これらは**完全ordered exterior traceが等しく、四変量`I₄`も同じ**だが

```text
ReverseLeftCount(B(X)) = ReverseLeftCount(A(X)) + 1
```

となる。`selectedNineteenStrictReverse_classDistinct`は元の真正19D商クラス`[A(X)]₁₉ ≠ [B(X)]₁₉`を証明。`selectedNineteenStrictReverse_noLocal`はその間の真正`SelectedLocalNineteen` Type値比較が存在しないことも証明した。`selectedNineteenFour_notInjective`は任意のinhabited raw18D exact fiberで四変量観測の非単射性を示す。

この証明を真正LR二重輸送の原証拠に適用して、四変量境界の像が両者を同一視すること、具体的境界が非単射であり全19D比較の反映証明書を持たないことをそれぞれ証明した。`selectedMixedFourAnchored_chosenSwap`は指定点のcoarse swap観測のみを保証する。

## 5. 権威境界・次段

**認証済み：** 四変量の19D商上観測、型付き非定数anchored LR→RL境界の実構成、像Eq iff source四変量Eq、v5.44の括弧付け対の識別、第五不変量ReverseLeftCount、同一完全trace・同一四変量・異なる真正19D商クラスという反例、この具体的四変量境界の非忠実性。

**未認証／NO_DATA：** 別の忠実LR→RL境界の存在・不存在、全域swap自然性、異なる元Type値の生Eq、無条件20D交換・gluing。観測等値を元の証拠同一性に固定しない。特定の境界の非単射性から一般的な不可能性を推論しない。

**次段Qi v5.46：** 第五不変量ReverseLeftCountを追加した観測と、より強い数値的符号化の境界輸送を検討する。残る証拠履歴や自然性条件を独立して検証し、未認証部分はNO_DATAで保持する。

本ファイルはdocs-only。Strict Leanは意図的にSKIPし、Governance・Coreと正確なGit treeの一致を検証する。append-only／tighten-only／overwrite-forbidden／same-root。
