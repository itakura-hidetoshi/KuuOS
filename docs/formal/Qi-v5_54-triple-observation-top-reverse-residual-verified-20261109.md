# Qi v5.54 — 三変量共同観測の残存最外層raw反転障害（Lean4形式監査正本）

正式記録日：2026-11-09 JST

## 1. 正本と分離したexact-source検証

Repository：`itakura-hidetoshi/KuuOS`、canonical branch：`main`。本成果物は既存元18D/19D真正Type値証拠、元比較、v5.50独立raw合同性、v5.53の7構成子保存定理を**変更しない新モジュール**：
[Qi v5.54 Lean全文](https://github.com/itakura-hidetoshi/KuuOS/blob/main/formal/KUOS/Architecture/QiWuxingGK5CHP77TripleTopReverseResidualV5_54.lean)。

- [定理PR #3392](https://github.com/itakura-hidetoshi/KuuOS/pull/3392)：**MERGED**。source `71f121ba27cd537576b601071823b8bb7c141685`、test merge `30f9da9406273a0015f7eb402521713efb69d28a`、squash `399074e8f4f4b9d81dda9743b124c9b86064b226`。共通Git tree `e7271a12d90214792a8b78cb23bb46541180a39c`。
- [定理exact-source CI #42551576053](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42551576053)：**completed SUCCESS**。Scoped Strict Lean **9,106 / 9,106**。Governance選択5/5 SUCCESS、16宣言の実際の`#print axioms`、公理不要9・Lean標準公理のみ7、`sorryAx`なし、変更Lean error/warning 0/0。exact-head受領書2件SUCCESS。
- [公開import PR #3393](https://github.com/itakura-hidetoshi/KuuOS/pull/3393)：**MERGED**。source `4081fcc34aa33906b557ed75e5a4c20e4619a645`、test merge `17ea3f1aced9de2fcd12429d12cd8414f9cc5f79`、squash `57a20113422d654a74f6ab13444332f48e8717ef`。共通Git tree `804cfb7dd525c2b4596c17ab1a27f8f4327643c5`。既存import完全保持、`formal/KuuOSFormal.lean`に**1行追加・削除0**。
- [公開CI #42552010285](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42552010285)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,367 / 10,367**、Governance **32 / 32 SUCCESS**、exact-head受領書2件SUCCESS。公開root107維持。

## 2. Lean4で証明された数学的構成

同一の元16D fiber、真正17D端点`J,N`、実在する元18D Type値証拠`M : SelectedContextualEighteen W l r J N`を与える。元の比較を広げたり非型付き値で置換せず、**既存の真正raw構成子だけ**から

```lean
A(M) = .reverse (.reverse M)
B(M) = .chain A(M) (.strict N)
```

を同じ`J→N` fiberに構成する。次を型付きで証明した：

1. `selectedTripleResidual_traceEq`：完全ordered raw `List Bool` traceが一致。
2. `selectedTripleResidual_reverseCountEq`：raw反転構成子の総数が一致。
3. `selectedTripleResidual_adjacentCountEq`：隣接raw反転回数も一致。
4. 新商に対する実際の`Quotient.lift`値の三変量観測 `selectedRawCongruentTraceReverseAdjacentObservation` が両者で一致。
5. 同じv5.53で7構成子保存性を認証済みの商観測 `TopReverseFlag` は `A(M)` で**1**、`B(M)` で**0**。したがって `selectedTripleResidual_classDistinct` により新商クラスが相異なり、`SelectedRawCongruentNineteen A(M) B(M)` のType値証拠も存在しない。
6. よって、各々に**実在する入力Mが与えられた**exact `J→N` fiber上で、三変量共同観測は非単射。商全体を三変量から復元する左逆decoderは存在せず、さらに最外層反転フラグ自体も三変量のみから復元する関数が存在しない。
7. 指定された17D端点`J`の真正raw `strict J`を入力すれば、`J→J` endomorphism fiberの非単射性はこの入力の存在について無条件に構成できる。
8. 第4観測 `TopReverseFlag` を付加した4変量は**この具体的な証拠対**を区別する。ただし四変量が新商全体を分類するという主張は含まない。

### 三変量と最外層フラグを分離する論理

```text
M : genuine raw 18D evidence J -> N
A := reverse (reverse M)
B := chain A (strict N)

orderedTrace(A)         = orderedTrace(B)
rawReverseCount(A)      = rawReverseCount(B)
adjacentReverseCount(A) = adjacentReverseCount(B)

TopReverseFlag(A) = 1, TopReverseFlag(B) = 0
TopReverseFlag respects all 7 comparison constructors
=> newClass(A) != newClass(B)
=> no new Type-valued comparison A ~ B
=> triple quotient observation is noninjective
=> no left-inverse decoder, nor TopReverseFlag decoder
   (only for an actually inhabited, fixed J->N fiber).
```

**観測／証明／解釈の分離：** 3変量の一致は生syntaxの検査だけでなくLean商観測の等式。クラス不等は既証明の新商不変量を使ったLean4定理であり、比較関係の不在まで形式化されている。「証拠履歴を失わずに識別不能性を表示する」という空OS上の位置づけは命名／解釈層であり、数学的同一性・自動的な大域権威を証明していない。

## 3. 新規16宣言の公理監査

| 宣言 | `#print axioms` |
| --- | --- |
| `selectedTripleResidualLeft` | なし |
| `selectedTripleResidualRight` | なし |
| `selectedTripleResidual_traceEq` | `propext` |
| `selectedTripleResidual_reverseCountEq` | なし |
| `selectedTripleResidual_adjacentCountEq` | なし |
| `selectedTripleResidual_leftTopReverse` | なし |
| `selectedTripleResidual_rightTopReverse` | なし |
| `selectedTripleResidual_threeObservedEq` | `propext` |
| `selectedTripleResidual_classDistinct` | なし |
| `selectedTripleResidual_noComparison` | `Quot.sound` |
| `selectedRawCongruentTriple_notInjective` | `propext` |
| `selectedRawCongruentTriple_noDecoder` | `propext` |
| `selectedRawCongruentTriple_noTopFlagDecoder` | `propext` |
| `selectedRawCongruentTriple_endomorphismNotInjective` | `propext` |
| `selectedRawCongruentTripleTopReverseObservation` | なし |
| `selectedRawCongruentFour_residualDistinguished` | なし |

計16件＝**9宣言公理不要、7宣言はLean標準`propext`または`Quot.sound`のみ**。新規公理なし・`sorryAx`なし。これは当該16宣言の監査結果であり、既存KuuOSFormal全依存の公理がすべて標準のみとの主張ではない。

## 4. 非認証境界・次段

未認証：4変量`(orderedTrace, reverseCount, adjacentReverseCount, topReverseFlag)`の商全体に対する単射性・完全復元、元I6全成分の新商降下、任意異なる`J,N` fiberのinhabitance、異16D fiber間のwhiskering、20D gluing・higher coherence、独立WORLDの数学的同一視や実行権限への昇格。

次段 **Qi v5.55**：第4観測を加えても残る元証拠対を探すか、その4変量の忠実性条件を別途形式検証する。どちらも本v5.54正本では未認証（NO_DATA）。新しい5番目の不変量を発見したと主張せず、元の真正Type値証拠と構成経路を保持する。

原ファイル・既存証明・root107・固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`・保護PR #1558 Draft／OPEN／未マージ維持。append-only／tighten-only／overwrite-forbidden／same-root。本正式記録のPRはdocs-onlyでありStrict Leanを再実行しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
