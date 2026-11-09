# Qi v5.55 — 四変量共同観測の残余反転祖先・子孫関係障害（Lean4形式監査正本）

正式記録日：2026-11-09 JST

## 1. Canonical正本、独立証明PR、公開CI

Repository：`itakura-hidetoshi/KuuOS`、canonical branch：`main`。本研究は、真正18D元証拠・旧19D比較・v5.50の独立新7構成子raw合同性・既存v5.53/v5.54の証明を変更せず、別モジュールを追加した。

- [Qi v5.55 Lean4形式証明全文](https://github.com/itakura-hidetoshi/KuuOS/blob/main/formal/KUOS/Architecture/QiWuxingGK5CHP77FourObservationAncestryResidualV5_55.lean)
- [定理PR #3395](https://github.com/itakura-hidetoshi/KuuOS/pull/3395) **MERGED**。source HEAD `55f35f05a8fe39aef8f291813a7e783767d4bed4`、synthetic test-merge `48e340046fc6e12215316ea49e19ccf6f16eb40e`、squash `47c09bfce6612de49812e752c01f2f4a2b67f7ff`、共通Git tree `94fb03a4408cc2d188309f5c61aec9bbb0f279be`。
- [定理exact-source CI #42558981152](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42558981152) **completed SUCCESS**。Scoped Strict Lean **9,107/9,107**、Governance **5/5**、新規19宣言`#print axioms`全件確認（11宣言公理不要、8宣言は標準`propext`/`Quot.sound`のみ）、新規`sorryAx`なし、変更Lean error/warning 0/0、exact-head受領書2件SUCCESS。
- [公開import PR #3396](https://github.com/itakura-hidetoshi/KuuOS/pull/3396) **MERGED**。source HEAD `e4d18d8780a2227370204b91ccfb70d3c0154580`、squash `4cb58b6eea2910e13178bc2b62fc5eea3236ca6d`、source/test-merge/squashのGit tree `6b1df3b540cb68b45b510e3c6d7b871f7f4b6f6c`一致。公開集約 `formal/KuuOSFormal.lean` にimport **1行追加・削除0**、元import順序・公開root107は保持。
- [公開exact-source CI #42560305685](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42560305685) **completed SUCCESS**。KuuOSFormal Strict Lean **10,368/10,368**、Governance **32/32**、exact-head受領書2件SUCCESS、対象Lean error/warning 0/0。Public Proof Roots RestorationもSUCCESS。

## 2. 新しい五番目の観測量

元の型付き17D端点 `J,N` と真正raw証拠 `M : SelectedContextualEighteen W l r J N` が与えられた場合のみ構成する。反転の祖先・子孫順序対の数 `ReverseAncestryCount` を再帰的に定義し、`reverse` 構成子では

```text
P(reverse M) = P(M) + ReverseCount(M)
P(chain M L) = P(M) + P(L)
```

とする。既存raw `inherited` は元証拠を勝手に展開せず不透明な葉として扱い、`strict` は0。元19Dの5構成子および**独立v5.50の7構成子すべて**について不変性をLeanの構造帰納法で証明した。特に`rawReverse`では`P`の帰納法仮定とv5.51の既証明`ReverseCount`不変性を同時に使用する。元19D商と新商それぞれに真正`Quotient.lift`を作り、旧商→新商の射影に沿う因子化を証明。

## 3. 真正18D証拠対による四変量非単射性

与えた元証拠`M:J→N`を一切変更せず、その右側の`N→N`部分に既存raw構成子だけを付けて、

```lean
A(M) := .chain M (.chain (.reverse (.strict N)) (.reverse (.strict N)))
B(M) := selectedAdjacentReverseRight l r M
      -- .chain M (.reverse (.chain (.strict N) (.reverse (.strict N))))
```

を構成した。Bはv5.47の保存済み**同一**raw証拠値を使用し、両項とも同一の真正fiber `J→N` に属する。

**四変量** `(orderedTrace, ReverseCount, AdjacentReverseCount, TopReverseFlag)` は、新商の実際の商クラス上で完全一致することを証明。一方、祖先・子孫関係数だけは

```text
ReverseAncestryCount(B(M)) = ReverseAncestryCount(A(M)) + 1
```

となる。第五変量が新7構成子で保存されるため：

- 新商 `selectedRawCongruentClass A(M) ≠ selectedRawCongruentClass B(M)`。
- `SelectedRawCongruentNineteen A(M) B(M)` の真正Type値比較は存在しない。
- **実在する証拠Mが与えられたexact J→N fiberに限り**四変量観測は非単射で、すべての商クラスを復元する関数は存在しない。
- その四変量だけから`ReverseAncestryCount`を復元する関数も存在しない。
- 指定17D端点`J`の真正`strict J`によって、endomorphism `J→J`上の非単射性を別途証明。
- 第五変量を加えた観測は**この具体的な対のみ**を区別する。五変量の全商分類は未証明。

この違いは、数値化する観測だけから元の高次証拠履歴を復元する際の、限定された形式的なobstructionである。「空」「縁起」との対応づけは命名・解釈層であり、証明された数学的結論とは分離する。

## 4. 新規19宣言の実公理監査

| 新規宣言 | `#print axioms` |
| --- | --- |
| `selectedContextEighteenReverseAncestryCount` | なし |
| `selectedLocalNineteen_preservesReverseAncestry` | なし |
| `selectedRawCongruent_preservesReverseAncestry` | なし |
| `selectedNineteenReverseAncestryOnQuotient` | なし |
| `selectedRawCongruentReverseAncestryOnQuotient` | なし |
| `selectedRawCongruentReverseAncestry_onClass` | なし |
| `selectedRawCongruentReverseAncestry_factorsOld` | `Quot.sound` |
| `selectedFourAncestryLeft` | なし |
| `selectedFourAncestryRight` | なし |
| `selectedFourAncestry_fourObservedEq` | なし |
| `selectedFourAncestry_countDiff` | なし |
| `selectedFourAncestry_classDistinct` | `propext, Quot.sound` |
| `selectedFourAncestry_noComparison` | `propext, Quot.sound` |
| `selectedRawCongruentFour_notInjective` | `propext, Quot.sound` |
| `selectedRawCongruentFour_noDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentFour_noAncestryDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentFour_endomorphismNotInjective` | `propext, Quot.sound` |
| `selectedRawCongruentFourAncestryObservation` | なし |
| `selectedRawCongruentFive_ancestryDistinguished` | `propext, Quot.sound` |

計19件：**公理なし11件・Lean標準`propext`または`Quot.sound`のみ8件**、新公理・`sorryAx`なし。これは**新規19宣言の監査**であり、旧依存全体が同じ公理集合のみを使うとの主張ではない。

## 5. 未認証範囲と次の研究課題

**未認証（NO_DATA）**：第五観測を加えた五変量全体の単射性・完全分類、任意の異なる17D端点 `J,N` fiberのinhabitance、元I6全成分の新商降下、異なる元16D fiber間のwhiskering互換、無条件20D gluing、真正higher coherence、独立WORLD間の同一視、科学的・制度的実行権限。

Qi v5.56では、反転祖先計数も含めた五変量で区別不能な真正証拠対を構成できるか、またはその限定された忠実性条件を調べる。未認証の推測は結果へ昇格しない。

現行固定：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、KuuOSFormal 公開root107、保護PR #1558 Draft／OPEN／未マージ、append-only／tighten-only／overwrite-forbidden／same-root。この文書はdocs-onlyでありStrict Leanは再実行しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
