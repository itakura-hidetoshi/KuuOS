# Qi v5.64 — 任意有限祖先次数サンプリングの非単射性：Lean4形式監査記録

2026年11月9日 JST。対象は **既存の祖先塔の有限個の任意次数観測** であって、無関係な任意の統計量・全WORLDの貼合・実行権限ではない。この文書は機械検証済みLean成果物とCI記録の説明であり、それ自体を証明の代用にしない。

## 正本・来歴と独立検証

- Repository: `itakura-hidetoshi/KuuOS`。canonical `main`。出発したv5.63のmain HEAD: `a5df2fdedcd3964aa02f667c30578345b3cb2213`。
- 定理 [PR #3422](https://github.com/itakura-hidetoshi/KuuOS/pull/3422) **MERGED**。新規Leanモジュール `formal/KUOS/Architecture/QiWuxingGK5CHP77ArbitraryFiniteAncestorSamplingV5_64.lean` のみ **279行追加、削除0**。正本元18D Type、旧selected19比較、新seven-generator合同性、他のLean、workflow、pinには変更なし。
- 定理source HEAD `321051fd0d995bc29426c6d72f9eae3f78cbdf03`、統合squash `af0af03baa5ef6a20aaf9b0598abf48e78c2932e`。source／test-merge／squash Git tree `3609c28b5796c1c14082b3af30900d649f498744` 完全一致。
- [定理exact-source CI #42610951099](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42610951099)：**completed SUCCESS**。Scoped Strict Lean **9,116 / 9,116**、Governance **5 / 5**、変更Lean error/warning **0 / 0**、exact-head source/terminal受領書 **2件SUCCESS**。
- 公開 [PR #3423](https://github.com/itakura-hidetoshi/KuuOS/pull/3423) **MERGED**。`formal/KuuOSFormal.lean`にimport **1行追加・削除0**。source HEAD `078321192b729d0a4270904774980be14d9a9b9f`、squash `7ff89eeeafc976a786b06fa701fe68e6a2c8686d`。source／test-merge／squash Git tree `c5ee475ef35584adc2c8ac36b310fab67a162b35` 一致。
- [公開exact-source CI #42611507731](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42611507731)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,377 / 10,377**、Governance **30 / 30**、exact-head受領書 **2件SUCCESS**。変更Lean error/warning **0 / 0**。
- 固定Lean `v4.30.0-rc2`、固定mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107維持**、保護 [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) **Draft／OPEN／未マージ**。

## 証明した対象：任意の有限List Natの祖先次数

v5.63は、任意自然数nについて真正の元18D証拠対が存在し、`C₀..Cₙ₊₆` が一致する一方、次の`Cₙ₊₇`は**ちょうど2異なる**ことを形式証明した。今回は観測次数が連続するという制約を外した。

```text
indices : List Nat                 -- 任意の有限長、順序・重複を許容
budget([])       = 0
budget(a :: as)  = a + budget(as)
∀ k ∈ indices, k ≤ budget(indices)
```

この有限予算を`b`とし、v5.63の元Type値から構成済みの`b`回反転位置交換対を取る。真正の `M : SelectedContextualEighteen W l r J N` が**実際に与えられた**同一fiberで、`chain M L_b`と`chain M R_b`を使う。

新しく定義した実際の商観測：

[
\mathrm{Obs}_{S}(q)
=
\bigl(\mathrm{Obs}_{9}(q),[C_k(q)]_{k\in S}\bigr)
]

ここで`S`はListとしての添字列であり、同じ値の重複や順序を保持する。v5.59の`selectedAncestorTowerOnNewQuotient`は個々の次数ごとに本来の新7構成子商への`Quotient.lift`を形式証明済みである。

**形式証明した結論**：

1. `selectedFiniteSampleBudget_mem_le`：有限に指定された全添字は構成的budget以下。
2. `selectedFiniteSampleFiber_selectedEq`：全サンプル次数の元18D計数は一致。
3. `selectedFiniteSampleFiber_nextGap`：`C_(budget+7)`は右が左より正確に2大きい。
4. `selectedFiniteSampleFiber_classDistinct`：本来の独立した新7構成子商クラスは異なる。
5. `selectedRawCongruentFiniteSampleObservation`：旧九観測＋有限List次数の商観測を実際に定義。
6. `selectedFiniteSampleMapEq`、`selectedFiniteSampleFiber_observedEq`：元raw値の点ごとの等式から、実際の商観測値の全一致を構成。
7. `selectedRawCongruentFiniteSample_notInjective` と `selectedRawCongruentEveryFiniteSample_notInjective`：**任意の有限添字リスト**について、供給された真正fiberでは非単射。
8. `selectedRawCongruentFiniteSample_endomorphismNotInjective`：指定Jの`strict J`でJ→Jの非単射を構成。
9. `selectedRawCongruentFiniteSample_noNextDecoder`、`selectedRawCongruentFiniteSample_noClassDecoder`：この観測から次次数計数または全新商クラスを完全復元する関数は存在しない。

空リストも許す。空リストは既存九観測だけとなり、証明はv5.63の`n=0`真正証拠を保持する。任意の大きな自然数や非連続サンプルも元証拠から具体的に構成される。

## 公理監査・証明の層

新Leanファイルの**全15宣言**へ`#print axioms`を実装し、定理CIと公開CIで実ログを取得。

- **公理なし4宣言**：`selectedFiniteSampleBudget`、`selectedFiniteSampleFiberLeft`、`selectedFiniteSampleFiberRight`、`selectedRawCongruentFiniteSampleObservation`。
- **標準公理だけ11宣言**：残りは`propext`／`Quot.sound`だけ。新規sorryAxなし、変更Lean warning/error 0/0。
- ビルド受領書：`Build completed successfully (9116 jobs)`／`(10377 jobs)`。
- ここで証明されたのは**有限の祖先塔座標のサンプリングが真正新商の完全同定にならないこと**であり、「空」「縁起」の哲学的な解釈がLeanで証明されたという主張ではない。

## 未認証の障害・今後の課題

- **NO_DATA**：祖先塔とは無関係の任意有限統計量を加えたときの識別限界、無限全次数の同時観測による商完全分類、元旧I6の非降下成分を含む他の比較、任意異端点fiberの実在、異fiber whiskering／20D gluing／独立WORLDの貼合、制度的権威。
- 次の課題は、**無限塔全体の忠実性を無根拠に決めず**、新7構成子商上での独立な追加不変量、または有限サンプリングと元Type履歴の関係を局所的に検証すること。
- v5.51の旧`LeftNestedCount`の新商非降下障害を消さない。旧selected19商と新商を同一視しない。
- append-only／tighten-only／overwrite-forbidden／same-root を維持。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
