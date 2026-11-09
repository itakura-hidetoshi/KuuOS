# Qi v5.62 — 九変量の識別限界と真正C₇残余：形式検証記録

2026-11-09 JST／状態：**定理・公開importの独立exact-source CI SUCCESS、両PR MERGED**。この文書は証明後の監査記録であり、Leanの機械的な定理・実際のCI受領書を置換しない。

## 正本・形式成果物・認証来歴

- Repository: `itakura-hidetoshi/KuuOS`、正本branch `main`。着手時のQi v5.61統合済みmain HEAD `fcf798737a683af5b4e48aecb322d4720def6e9e`。
- [定理PR #3416](https://github.com/itakura-hidetoshi/KuuOS/pull/3416) **MERGED**。新規Leanファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77NineObservationSeventhAncestorResidualV5_62.lean`、361行追加・削除0。他のLean source・元Type証拠・比較生成元・workflowは変更なし。
- 定理source HEAD `252be9b80ffe779197d8660b9fd326e5270f25ec`、squash `bcb76f520dbaa2a127e6f8dea9181ff51c9b17f4`。source／test-merge／squash Git tree `9c744dc7e372952e0f4e64156d88fc8a9b870d5e` **完全一致**。
- [定理exact-source CI #42602535849](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42602535849) **completed SUCCESS**：Scoped Strict Lean **9,114 / 9,114**、Governance **5 / 5**、変更Lean error/warning **0 / 0**、source／terminal exact-head受領書2件SUCCESS。
- [公開import PR #3417](https://github.com/itakura-hidetoshi/KuuOS/pull/3417) **MERGED**。既存 `formal/KuuOSFormal.lean` に独立検証済みv5.62 importを**1行だけ挿入・削除0**、source HEAD `8de1283d097b26d703df28dcff99808c61467cef`、squash `8381b31cb677a2fbb66b98162f55c928ae83ec37`。source／test-merge／squash Git tree `56892b90441541f7d29d228e4c704c44ee97e5fc` **一致**。
- [公開exact-source CI #42603465031](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42603465031) **completed SUCCESS**：KuuOSFormal Strict Lean **10,375 / 10,375**、Governance **30 / 30**、exact-head受領書2件SUCCESS、変更Lean error/warning 0/0。
- 固定：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root **107維持**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) **Draft／OPEN／未マージ**。

## 数学的な構成と証明された範囲

元の従属型 `SelectedContextualEighteen W l r J N` と、独立した新7構成子比較 `SelectedRawCongruentNineteen` を保持する。v5.60の真正N→N証拠対を `L₆`、`R₆` と書く。v5.60・v5.61で以下はすでに機械検証済みだった。

```text
∀ k ≤ 5, Cₖ(L₆) = Cₖ(R₆)
C₆(R₆) = C₆(L₆) + 2
EightObservation(L₆) = EightObservation(R₆)
```

v5.62は**同じ元18D Typeの構成子**で、さらに一度反転配置を交換する。

```text
L₇ := chain (reverse L₆) R₆
R₇ := chain L₆ (reverse R₆)
```

ここでC₀=1は形式的seed（反転総数ではない）。新定理により、任意の指定された真正17D端点Nについて、

```text
∀ k ≤ 6, Cₖ(L₇) = Cₖ(R₇)
C₇(R₇) = C₇(L₇) + 2
```

が成立する。抽象型付き補題 `selectedAncestorShift_exactTwoGap` で差+2を移送し、巨大なv5.58原証拠を再展開していない。

八観測のうちC₁〜C₅と対応する旧計数は既証明の真正pointwise bridgeを使う。残るordered raw traceはraw reverseを移しても同じ、最上位reverse flagは両方chainゆえ0、隣接raw reverse数は**入力L₆/R₆の最上位flagがともに0であることを別途証明して**一致する。従って今回の`L₇,R₇`は既存の全八独立raw観測で一致し、加えて第九C₆も一致する。

**条件付きの実在fiber輸送**：元の真正証拠 `M : SelectedContextualEighteen W l r J N` が与えられた場合だけ、`chain M L₇` と `chain M R₇` を同じ元J→N fiberに作る。実際の新商の第九観測写像 `selectedRawCongruentNineObservation` はこの二つのクラスを識別できない。しかし新商に独立に降下済みのC₇はちょうど2異なるため、二つのクラスは相異なる。

形式証明された結論：

1. `selectedNineTowerFiber_nineObservedEq`：真正同一fiberの2クラスについて既存九成分の値がすべて一致。
2. `selectedNineTowerFiber_classDistinct`：同じ2クラスは新7構成子の商で相異なる（C₇の+2を利用）。
3. `selectedRawCongruentNine_notInjective`：元18D証拠Mが指定されたfiberで、九変量観測は非単射。
4. `selectedRawCongruentNine_endomorphismNotInjective`：指定Jについて真正`strict J`を使ったJ→J版。
5. `selectedRawCongruentNine_noSeventhDecoder`：九変量から新商不変量C₇を完全復元する関数は存在しない。
6. `selectedRawCongruentTenObservation`、`selectedRawCongruentTen_seventhDistinguished`：第十C₇商観測を実際に定義し、**この具体的対に限って**区別。

## 新規20宣言の機械的公理監査

新Leanファイルの新規20宣言すべてに `#print axioms` を付し、定理exact-source CIと公開CIの実ログを照合した。

- **公理依存なし（7）**：`selectedNineTowerShiftLeft`、`selectedNineTowerShiftRight`、`selectedEightTowerShift_bothTopZero`、`selectedNineTowerFiberLeft`、`selectedNineTowerFiberRight`、`selectedRawNineObservationValue`、`selectedRawCongruentTenObservation`。
- **標準公理のみ（13）**：上記以外の13宣言は、実ログで`propext`と`Quot.sound`のみ。新規`sorryAx`なし、新規axiom宣言なし。
- 変更Lean error／warning：**0 / 0**。`Build completed successfully (9114 jobs)` および `(10375 jobs)` を直接確認した。

## 残る障害・次段の最小課題

**未認証／NO_DATA**：第十観測による新商全体の完全復元、任意の有限塔prefixをすり抜ける証拠対の**全nにわたる具体的反復帰納族**、任意異なるJ,Nのfiber非空性、異fiber whiskeringや20D gluing、独立WORLDの大域貼合、制度的行為権限。

v5.59の条件付き `∀n` 定理から`∀n,∃witness`を推論してはならない。今回実際に構成・認証したのは**一段進めたn=7の真正対**まで。次段Qi v5.63では、N→N反復shiftの`Nat`再帰と各段のtop flag等式を明示し、任意有限次数のprefix衝突を帰納法で実際に構成できるかを検証する。

元Type値証拠と旧selected19商、新7構成子商は同一視しない。v5.51で既証明の旧LeftNestedCount／元19D正規代表の新商非降下障害も保持する。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
