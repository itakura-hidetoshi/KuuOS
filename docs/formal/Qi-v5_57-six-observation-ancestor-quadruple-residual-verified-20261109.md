# Qi v5.57 — 六変量観測の残余raw反転祖先四重鎖障害（Lean4形式監査正本）

正式記録日：2026-11-09 JST

## 1. Canonical正本・分離した検証・統合履歴

Repository：`itakura-hidetoshi/KuuOS`。Canonical branch：`main`。元の真正18D Type値証拠・元selected19比較・独立v5.50の新7構成子raw合同性・これまでのすべての証明を変更しない独立モジュール：

[Qi v5.57 Lean4形式証明全文](https://github.com/itakura-hidetoshi/KuuOS/blob/main/formal/KUOS/Architecture/QiWuxingGK5CHP77SixObservationAncestorQuadrupleV5_57.lean)

- [定理PR #3401](https://github.com/itakura-hidetoshi/KuuOS/pull/3401)：**MERGED**。修正後source `4f65d68313f5a8273513f7144ce3a1a89742f5bd`、squash `b6c3ba4a5b0bd7f6ed05d773a4f2a699bed7416a`。Source/test-merge/squash共通Git tree `9aee0610479efcb65e285136d4d142f06fe82e92`。新規Lean1ファイル、既存Leanの変更なし。
- [定理exact-source CI #42563790860](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42563790860)：**completed SUCCESS**。Scoped Strict Lean **9,109/9,109**、Governance **5/5**、22宣言の実際の`#print axioms`、公理不要14・標準公理のみ8、`sorryAx`なし、変更Lean error/warning 0/0、2つのexact-head受領書ともSUCCESS。
- 初回draft HEAD `25b0875fff088f619809d3337513758871e88202` のCI #42563347629は失敗した。原因は**新規左右suffixの閉じ括弧各1文字不足**によるLean4構文エラー2件で、後続の`rfl`証明にも派生的な診断が出た。修正は新規Leanファイルの右括弧**計2文字追加のみ**。宣言のstatement、仮定、数学的raw証拠の構成意図、元ファイルは変更なし。修正後HEADで変更Leanファイル全文を再検証した。
- [公開import PR #3402](https://github.com/itakura-hidetoshi/KuuOS/pull/3402)：**MERGED**。Source HEAD `a6d9cf9480a1464aa97da0024292ed64d7c53755`、squash `90ae2680140a84b5745c62150e70a70fecb228c9`、source/test-merge/squash共通Git tree `08c8e1c686056d88d34b47beab244a1fa7058bde`。公開集約`formal/KuuOSFormal.lean`へimport **+1行、削除0**。
- [公開exact-source CI #42564385860](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42564385860)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,370/10,370**、Governance **32/32**、exact-head受領書2件SUCCESS、公開root107保持。

## 2. 新しい第7商不変量：四重反転祖先鎖数

従来の三重鎖計数を`T(M)`、今回の四重鎖計数を`Q(M)`とすると、真正raw構成子に対して以下の再帰的定義を持つ。

```text
Q(inherited old18) = 0  -- 元Type値内部を勝手に展開しない
Q(strict J) = 0
Q(reverse M) = Q(M) + T(M)
Q(chain M L) = Q(M) + Q(L)
```

局所whiskeringでは元の計数を保持するが、異なる16D fiber間の対応を新規に主張しない。元比較の5構成子と新v5.50比較の7構成子を**それぞれ構造帰納法で全件証明**。特に`rawReverse`ケースではQの帰納法仮定と、v5.56で既に認証した`T`の比較保存定理を合わせて使用した。元商・新商に別々の真正`Quotient.lift`を構成し、元商→新商の射影について因子化を証明した。

## 3. 真正18D raw反例と六変量非単射性

同一元16D fiber、真正17D端点 `J,N`、与えられた真正18D raw証拠 `M:J→N` に対し、

```text
A(M) = chain M (selectedSixQuadrupleSuffixLeft  N)
B(M) = chain M (selectedSixQuadrupleSuffixRight N)
```

を**同一型付きJ→N fiber**に構成。suffixそのものは元の`strict N`、`reverse`、`chain`だけを組み合わせた真正`N→N`証拠である。元のMを改変しない。

Lean4の`selectedSixQuadruple_suffixSignature`は、両suffixに対して次の計数を個別に証明した。

| raw構文観測 | Left suffix | Right suffix |
| --- | ---: | ---: |
| 総反転構成子数 | 7 | 7 |
| 隣接raw反転数 | 2 | 2 |
| 反転祖先対数 | 12 | 12 |
| 反転祖先三重鎖数 | 10 | 10 |
| 最外層raw反転フラグ | 0 | 0 |
| 反転祖先四重鎖数 | **3** | **5** |

両suffixの完全ordered traceは空。元のMに右合成した全raw値でも、新商の既存六変量 `(orderedTrace, ReverseCount, AdjacentReverseCount, TopReverseFlag, ReverseAncestryCount, ReverseAncestorTripleCount)` が一致することを真正の商観測で証明した。

しかし四重鎖数は

```text
Q(B(M)) = Q(A(M)) + 2
```

となる。このQが新7比較構成子すべてで保存されるため、次のLean4定理が成立する。

1. `newClass(A(M)) ≠ newClass(B(M))`。
2. `SelectedRawCongruentNineteen A(M) B(M)`の真正Type値証拠は存在しない。
3. **実在する入力Mが与えられた場合に限り**そのexact J→N fiberで六変量観測は非単射。
4. 六変量から商クラス全体へ戻る左逆decoderは存在せず、Qだけのdecoderも存在しない。
5. 指定端点Jの真正`strict J`を利用すれば、J→Jの非単射性を具体的に構成できる。
6. 第7観測Qを追加すると**この具体的対は区別できる**。七変量が新商全体を分類する証明ではない。

空OSとの「観測から元証拠へ不正に一般化しない」という対応は解釈・命名層。Leanが示した数学的な商不変性・反例・条件付き不可能性の形式証明と区別する。

## 4. 新規22宣言の実公理監査

| 宣言 | `#print axioms` |
| --- | --- |
| `selectedContextEighteenReverseAncestorQuadrupleCount` | なし |
| `selectedLocalNineteen_preservesReverseAncestorQuadruple` | なし |
| `selectedRawCongruent_preservesReverseAncestorQuadruple` | なし |
| `selectedNineteenReverseAncestorQuadrupleOnQuotient` | なし |
| `selectedRawCongruentReverseAncestorQuadrupleOnQuotient` | なし |
| `selectedRawCongruentReverseAncestorQuadruple_onClass` | なし |
| `selectedRawCongruentReverseAncestorQuadruple_factorsOld` | `Quot.sound` |
| `selectedSixQuadrupleSuffixLeft` | なし |
| `selectedSixQuadrupleSuffixRight` | なし |
| `selectedSixQuadruple_suffixSignature` | なし |
| `selectedSixQuadrupleLeft` | なし |
| `selectedSixQuadrupleRight` | なし |
| `selectedSixQuadruple_sixObservedEq` | なし |
| `selectedSixQuadruple_countDiff` | なし |
| `selectedSixQuadruple_classDistinct` | `propext, Quot.sound` |
| `selectedSixQuadruple_noComparison` | `propext, Quot.sound` |
| `selectedRawCongruentSix_notInjective` | `propext, Quot.sound` |
| `selectedRawCongruentSix_noDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentSix_noQuadrupleDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentSix_endomorphismNotInjective` | `propext, Quot.sound` |
| `selectedRawCongruentSixQuadrupleObservation` | なし |
| `selectedRawCongruentSeven_quadrupleDistinguished` | `propext, Quot.sound` |

**22件全件：14宣言は公理不要、8宣言はLean標準`propext`/`Quot.sound`のみ**。新公理0、`sorryAx`なし。既存の他全成果物まで同じ公理集合のみを用いるとは主張しない。

## 5. 明示的な未認証領域と次段

**NO_DATA**：七変量の新商全体に対する単射性・完全復元、任意の異17D端点J,N fiberのinhabitance、旧I6の全成分の新商への降下、元16D fiberを超えるwhiskering、20D higher coherence/gluing、独立WORLDや物理C60の数学的同一視、制度的・実行上の権限。

次段 **Qi v5.58**では、新たな七変量でも区別できない真正同fiber証拠対があるか、または限定的な忠実性条件が成り立つかを個別に調べる。過去の6変量の反例は第7観測で解消されるが、新商全体の忠実性が自動的に導かれるわけではない。

既存source・元Type値証拠・公開root107、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft/OPEN/未マージを保持。append-only／tighten-only／overwrite-forbidden／same-root。**このPRはdocs-onlyでありStrict Leanを再実行しない**。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
