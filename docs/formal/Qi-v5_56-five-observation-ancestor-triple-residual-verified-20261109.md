# Qi v5.56 — 五変量共同観測の残余raw反転祖先三重鎖障害（Lean4形式監査正本）

正式記録日：2026-11-09 JST

## 1. Canonical source と exact-source CI

Repository：`itakura-hidetoshi/KuuOS`。Canonical branch：`main`。元の真正18D Type証拠、元selected19 Type値比較、独立v5.50の新7構成子比較、およびv5.55までの元成果物を**一切書き換えず**、新Leanモジュールを追加した。

[Qi v5.56 Lean形式証明全文](https://github.com/itakura-hidetoshi/KuuOS/blob/main/formal/KUOS/Architecture/QiWuxingGK5CHP77FiveObservationAncestorTripleV5_56.lean)

- [定理PR #3398](https://github.com/itakura-hidetoshi/KuuOS/pull/3398)：**MERGED**。新Lean336行、削除0。Source HEAD `e7f17185329b74283adbf90430a2da374e4ed7b1`、main統合 `71523f6f0caa2e1c9f1125d0c0cfea1bed013464`、source/test-merge/squash 共通Git tree `25cfb55625f732972b094ca9e720f910ab8b6d5d`。
- [Exact-source CI #42561415850](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42561415850)：**completed SUCCESS**。Scoped Strict Lean **9,108/9,108**、Governance **5/5**、新規宣言19/19の`#print axioms`実監査、公理なし11・標準公理のみ8、新規`sorryAx`なし、変更Lean error／warning 0/0、exact-head status受領書2件SUCCESS。
- [公開import PR #3399](https://github.com/itakura-hidetoshi/KuuOS/pull/3399)：**MERGED**。Source HEAD `f267daf276968e3a21893ba1ae6b79a6e7296042`、main統合 `cd54f8cc648c87c5ba05b35a78a1f72001ce0193`、source/test-merge/squash Git tree `ba28737744364736f2fc6b5f3dbfab775a85b065`一致。`formal/KuuOSFormal.lean`への新規import1行、削除0。
- [公開exact-source CI #42561942569](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42561942569)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,369/10,369**、Governance **32/32**、exact-head受領書2件SUCCESS、変更Lean error/warning 0/0。公開root107を保持。

## 2. 6番目の独立した商観測

元の型付き18D raw構文で、反転構成子の**順序付き祖先・子孫三重鎖**を数える新観測 `ReverseAncestorTripleCount` を定義した。元v5.55の祖先**対**数 `P` と区別する。再帰則：

```text
T(reverse M) = T(M) + P(M)
T(chain M L) = T(M) + T(L)
T(strict N) = 0
T(inherited old18) = 0   -- 元Type値内部は不透明な葉として保持
```

旧19D比較の5構成子と、新v5.50比較の7構成子を**それぞれ構造帰納法で全件検証**。新`rawReverse`ケースでは、Tの帰納法仮定だけでなく、v5.55で認証済みの祖先対数Pの保存を併用した。元商・新商に独立の真正 `Quotient.lift`を構成し、元商→新商の射影について厳密な因子化を証明した。

## 3. 真正raw証拠における五変量非単射

同じ16D fiber上の型付き17D端点 `J,N`、真正元18D raw証拠 `M:J→N` が**与えられる場合に限り**、元証拠Mを消さずに以下を構成：

```text
A(M) = chain M [ reverse (reverse (chain
                     (reverse (reverse (strict N)))
                     (reverse (reverse (strict N))))) ]

B(M) = chain M [ reverse (chain
                     (reverse (strict N))
                     (reverse (reverse (reverse (reverse (strict N)))))) ]
```

角括弧は明示したN→N suffixの読みやすさのために置いたもので、Leanコードは元の `.chain`・`.reverse`・`.strict` 構成子だけで実装する。両suffixの計数は以下の通り：

| 生構文観測 | Aのsuffix | Bのsuffix |
| --- | ---: | ---: |
| 総raw反転数 | 6 | 6 |
| 隣接raw反転数 | 3 | 3 |
| 反転祖先対数 P | 11 | 11 |
| suffix最外層反転flag | 1 | 1 |
| 反転祖先三重鎖 T | **8** | **10** |

このN→N suffixをMに右合成した後も、既存の**五変量** `(orderedTrace, ReverseCount, AdjacentReverseCount, TopReverseFlag, ReverseAncestryCount)` は新商の真正クラス上で等しい。注意：合成後の最外層flagは両者とも0であり、表中のsuffixの値1を元の全構文の値へ取り違えない。

反対に、新たな`T`の値は `T(B(M))=T(A(M))+2` で異なる。Tが新7構成子不変であるため、次がLean4形式証明済み：

1. 新商の真正商クラス `[A(M)] ≠ [B(M)]`。
2. `SelectedRawCongruentNineteen A(M) B(M)` の真正Type値比較は存在しない。
3. 実際にMの存在が与えられた**同一exact J→N fiber**で、五変量観測は非単射。
4. 五変量から新商全クラスへ戻る左逆decoderは存在せず、Tだけのdecoderも存在しない。
5. 指定Jの`strict J`を使う J→J の非単射性は構成可能。
6. 第六観測Tは今回の**具体的対**を区別するが、新商全体の完全分類は証明していない。

空OS的な解釈は「有限個の一致する観測を元証拠の完全復元へ不正に昇格しない」という限定的な位置づけ。Leanが証明した数学的内容と、「空」「縁起」の命名・解釈層を混同しない。

## 4. 新規19宣言の公理監査

| 新規Lean宣言 | `#print axioms` |
| --- | --- |
| `selectedContextEighteenReverseAncestorTripleCount` | なし |
| `selectedLocalNineteen_preservesReverseAncestorTriple` | なし |
| `selectedRawCongruent_preservesReverseAncestorTriple` | なし |
| `selectedNineteenReverseAncestorTripleOnQuotient` | なし |
| `selectedRawCongruentReverseAncestorTripleOnQuotient` | なし |
| `selectedRawCongruentReverseAncestorTriple_onClass` | なし |
| `selectedRawCongruentReverseAncestorTriple_factorsOld` | `Quot.sound` |
| `selectedFiveAncestorTripleLeft` | なし |
| `selectedFiveAncestorTripleRight` | なし |
| `selectedFiveAncestorTriple_fiveObservedEq` | なし |
| `selectedFiveAncestorTriple_countDiff` | なし |
| `selectedFiveAncestorTriple_classDistinct` | `propext, Quot.sound` |
| `selectedFiveAncestorTriple_noComparison` | `propext, Quot.sound` |
| `selectedRawCongruentFive_notInjective` | `propext, Quot.sound` |
| `selectedRawCongruentFive_noDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentFive_noTripleDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentFive_endomorphismNotInjective` | `propext, Quot.sound` |
| `selectedRawCongruentFiveTripleObservation` | なし |
| `selectedRawCongruentSix_tripleDistinguished` | `propext, Quot.sound` |

計19宣言。**公理なし11件、Lean標準 `propext`/`Quot.sound` のみ8件**、新公理および`sorryAx`なし。結果はこの19宣言の監査であり、既存の全mathlib/他系統の公理依存まで拡大しない。

## 5. 未認証（NO_DATA）と次段

未認証：**6変量の全商単射性・完全復元**、全任意17D異端点fiberのinhabitance、旧I6全成分の新商降下、異16D fiber間whiskeringの互換、無条件高次20D gluing、元WORLD間の数学的同一視、外部行為・実行権限。

**Qi v5.57（未認証課題）**：祖先三重鎖も含む六変量で区別できない真正18D証拠対があるか、または局所的忠実性を条件付きで証明できるかを検討する。証明されていない候補はNO_DATAのまま残す。

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージ、append-only／tighten-only／overwrite-forbidden／same-rootを維持。このPRはdocs-onlyのためStrict Leanは再実行しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
