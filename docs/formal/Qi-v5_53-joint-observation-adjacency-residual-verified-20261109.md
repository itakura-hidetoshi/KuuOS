# Qi v5.53 — ordered trace／raw反転総数の共同観測限界と隣接反転障害（Lean4形式監査正本）

正式記録日：2026-11-09 JST

## 1. Canonical正本と分離した検証

Repository：`itakura-hidetoshi/KuuOS`。branch：`main`。唯一の元ソース証拠とLean4形式定理は新しい独立モジュール：
[Qi v5.53 Lean全文](https://github.com/itakura-hidetoshi/KuuOS/blob/main/formal/KUOS/Architecture/QiWuxingGK5CHP77JointObservationResidualV5_53.lean)。
既存の元18D・旧19D Type値証拠／v5.50新7構成子比較／v5.51・v5.52定理は変更していない。

- [定理PR #3389](https://github.com/itakura-hidetoshi/KuuOS/pull/3389)：**MERGED**（squash `20f9ccfd33d894c15115c8ac669f5ddf0a7171e4`）。Source HEAD `77624d31510ca00f98e55e1760252ca7a6218218`、test-merge `d41a24821f578949d7f4019c83b3a7825775ccc5`、squashは全てGit tree `d72434cff7e23659b718f6f91cd0be346ceecf9a`。
- [定理exact-source CI #42548681357](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42548681357)：**completed SUCCESS**。Scoped Strict Lean **9,105 / 9,105**、Governance **5 / 5**、exact-head受領書2件SUCCESS。新規20宣言の公理監査（公理不要12、標準公理のみ8）、`sorryAx`なし、変更Lean error／warning 0 / 0。
- [公開import PR #3390](https://github.com/itakura-hidetoshi/KuuOS/pull/3390)：**MERGED**（squash `7a1acd2021de701d1fb63ce357ab8644b5154cd2`）。新規import 1行、削除0。Source HEAD `682235505f6cb31164bbbf45ff44edb8265ce5b9`、test-merge `58cfae9fa08b7000a9888c5d3d561ccd01134f40`、squashは全てGit tree `aeb6947c3e594e1bc369a1aed2e9c1cf22bc2bcb`。
- [公開exact-source CI #42549196684](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42549196684)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,366 / 10,366**、Governance **30 / 30**、exact-head受領書2件SUCCESS。元公開importとroot107は維持。

## 2. 実際に形式証明した構成

新comparison `SelectedRawCongruentNineteen` の7構成子は `inherited`・`strict`・`reverse`・`chain`・`rawReverse`・`rawChainRight`・`rawChainLeft`。この7種の構造帰納法により：

1. `selectedContextEighteenTopReverseFlag` を導入。元19D比較でも新7種比較でも不変。保存するのはraw最外層が反転かどうかの**フラグだけ**で、元 `TopTag` 全体ではない。
2. v5.47から保存した真正raw隣接反転回数 `selectedContextEighteenAdjacentReverseCount` の**7構成子すべてに対する不変性**を証明。特に新`rawReverse`では、既証明の隣接回数等式と新しい最外層反転フラグの等式を同時に用いた。
3. 新商の`TopReverseFlag`と`AdjacentReverseCount`に真正 `Quotient.lift` を構成。旧19D商→新商の全射射影に沿い、旧隣接反転回数観測が正しく因子化することを証明。
4. 新商上のordered `List Bool` traceとraw反転総数`Nat`の真正共同観測 `selectedRawCongruentTraceReverseObservation` を構成し、旧商との因子化も証明。
5. v5.47で既に存在する元18D raw対 `selectedAdjacentReverseLeft/Right M` を**変更なしに再利用**。完全ordered traceとraw反転総数が一致し、さらに元6変量の値も一致するが、隣接反転回数は1異なる。新商では隣接回数が保存されるため、この二つは別の商クラスである。
6. この二点間に、新しい`SelectedRawCongruentNineteen`の実際のType値比較は存在しない。したがって共同観測は与えられたraw証拠を持つfiberで単射でなく、共同観測から商クラスを完全回復するdecoderも存在しない。
7. 与えられた17D端点`J`の真正raw strict identityから、`J→J` fiberの共同観測非単射性も確定。**全ての異なるJ,N fiberのinhabitanceを主張しない。**
8. 第3観測（隣接反転回数）を追加した `(orderedTrace, reverseCount, adjacentReverseCount)` は**この具体的な二点を区別する**。その3変量だけで新商全体を分類・忠実復元できるとの主張ではない。

### 具体的な論理構造

```text
同一の元16D fiber、真正17D endpoints J,N、
実在する元18D証拠 M を与える。

A := selectedAdjacentReverseLeft  M
B := selectedAdjacentReverseRight M

orderedTrace(A) = orderedTrace(B)
reverseCount(A) = reverseCount(B)
rawSix(A) = rawSix(B)
adjacentReverseCount(A) = adjacentReverseCount(B) + 1

新比較の7構成子はadjacentReverseCountを保存する
⇒ newClass(A) ≠ newClass(B)
⇒ ¬ Nonempty (SelectedRawCongruentNineteen ... A B)
⇒ (orderedTrace, reverseCount) は新商上で非単射
⇒ 共同観測のみから全クラスを戻すdecoderは存在しない。
```

最終結論の権威はLean4の定理と指定の固定CIに限定。既存の6変量はこのpairのraw値として一致するが、v5.51で`LeftNestedCount`の降下不能を示しているため、**旧I6全体を新商の不変量と扱わない。**

## 3. 新規20宣言の公理監査

| 宣言 | `#print axioms` |
| --- | --- |
| `selectedContextEighteenTopReverseFlag` | なし |
| `selectedLocalNineteen_preservesTopReverseFlag` | なし |
| `selectedRawCongruent_preservesTopReverseFlag` | なし |
| `selectedRawCongruent_preservesAdjacentReverseCount` | なし |
| `selectedRawCongruentTopReverseOnQuotient` | なし |
| `selectedRawCongruentAdjacentReverseOnQuotient` | なし |
| `selectedRawCongruentAdjacentReverse_onClass` | なし |
| `selectedRawCongruentAdjacentReverse_factorsOld` | `Quot.sound` |
| `selectedRawCongruentTraceReverseObservation` | なし |
| `selectedRawCongruentTraceReverse_onClass` | なし |
| `selectedRawCongruentTraceReverse_factorsOld` | `Quot.sound` |
| `selectedRawCongruentTraceReverse_adjacentEq` | なし |
| `selectedRawCongruent_adjacent_classDistinct` | `propext, Quot.sound` |
| `selectedRawCongruent_adjacent_noComparison` | `propext, Quot.sound` |
| `selectedRawCongruentTraceReverse_notInjective` | `propext, Quot.sound` |
| `selectedRawCongruentTraceReverse_noDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentTraceReverse_endomorphismNotInjective` | `propext, Quot.sound` |
| `selectedRawCongruentTraceReverseAdjacentObservation` | なし |
| `selectedRawCongruentTriple_adjacentDistinguished` | `propext, Quot.sound` |
| `selectedRawCongruent_adjacent_rawSixEq` | なし |

計20件＝公理不要12件＋Lean標準公理のみ8件。追加公理0、`sorryAx`なし。

## 4. 未認証の障害と次段

未証明：任意の16D・17D fiberがinhabitedであること、新商の全クラスの可算性・完全分類、3変量共同観測の大域的単射性または忠実復元、旧I6全成分の新商降下、異なる元fiber間のwhiskering、無条件高次gluing／20D coherence、独立WORLDの同一視。

Qi v5.54候補は、**新3変量でなお区別できない具体的二点が存在するか**、または旧I6の各成分の降下可否を**1成分ずつ**調べる課題。どちらも本記録では未認証（NO_DATA）。選好による局所結果の大域化を行わない。

既存 Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージを保持。append-only／tighten-only／overwrite-forbidden／same-root。この正式記録PRはdocs-onlyのためStrict Leanを再実行しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
