# Qi v5.71 — 単位簡約括弧まで観測しても残る inherited 証拠来歴（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は**真正の元18D依存Type値**と、同じ17D二端点上の**独立した旧5構成子selected19／新7構成子raw合同性商**である。数学的な保存・非単射の定理と、「空」「縁起」などの命名・哲学的解釈は別の層であり、後者はLean4証明の対象ではない。

## 正本・変更範囲・来歴

- Repository: `itakura-hidetoshi/KuuOS`; canonical branch: `main`。前段Qi v5.70の統合済み HEAD `8d717df8ecaecf9129305d2c6becd2c8363870ee` を基礎にした。
- [定理PR #3443](https://github.com/itakura-hidetoshi/KuuOS/pull/3443) **MERGED**。新規Leanファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77InheritedProvenanceAfterBracketV5_71.lean` **1件だけ追加**。元18D、元旧19D、元新7構成子比較、公理や既存ファイルを改変しない。
- 定理認証source `b9c205433039e6ec1d5d33b5bf6b673a7f3c193c`、test-merge `f97cb692e19476c4a4d8d8cf6c372d031ebba371`、squash `799b82d3aa1fb5413b93735440b3b9f735bf3f91`。三者のGit tree `352fbf5338afdd3b3f1fe3805592522b9257baa7` が完全一致。
- [公開import PR #3444](https://github.com/itakura-hidetoshi/KuuOS/pull/3444) **MERGED**。公開集約 `formal/KuuOSFormal.lean` にv5.71 importを**1行だけ**追加。既存import・公開root107を保持。
- 公開認証source `781f1a817ac281c2b6b7208459bba8f7d66e2c75`、test-merge `f64955e448031d30f22cfe343cb4dcca9bccdbf2`、squash `d1c8603ae9a271733b0ba979757c2251d9de3355`。三者のGit tree `f10f2ac8c42e07ef61f237e9bc79e28d8135ca15` が完全一致。
- 固定Lean **v4.30.0-rc2**、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。

## 何が本当に商に降下するか

元の `SelectedContextualEighteen` を構造再帰して、旧18D真正値を保持する `inherited` 葉の**個数**を `selectedContextEighteenInheritedLeafCount` として独立定義した。構成子への作用は：

~~~text
inherited(_)        ↦ 1
strict(_)           ↦ 0
whiskerLeft/Right A ↦ Count(A)
reverse A           ↦ Count(A)
chain A B           ↦ Count(A) + Count(B)
~~~

旧 `SelectedLocalNineteen` の**5構成子** `strict`、`unitPrepend`、`unitAppend`、`reverse`、`chain` で保存される。新 `SelectedRawCongruentNineteen` の**7構成子** `inherited`、`strict`、`reverse`、`chain`、`rawReverse`、`rawChainRight`、`rawChainLeft` に対しても全件構造帰納法で保存される。実際の両19D Type値比較に基づいて、旧商・新商への独立 `Quotient.lift` と、旧→新projectionの因子化を証明した。

対照的に、元18D raw構文の `strict` 節点数は商不変量ではない。元の真正19D `unitPrepend M` は `chain (strict J) (inherited M)` と `inherited M` を比較するが、そのraw strict節点数は **1対0** である。したがって新7構成子商からraw strict節点数を全域復号する関数は**存在しない**。失われる履歴を、不正な大域化によって商に押し込まない。

## Qi v5.70の括弧観測まで追加しても残る真正反例

任意の真正17D端点 `N` の元18D endomorphism fiber `N→N` で、元の本物の構成子を使って：

~~~lean
A := SelectedContextualEighteen.reverse (.strict N)
B := SelectedContextualEighteen.reverse
       (.inherited (SelectedLocalEighteen.strict N))
~~~

を構成する。 `A`、`B` はいずれも本来の依存18D Type値であり、単なる観測用proxyではない。

- 既存**九観測**、全自然数次数 `Nat → Nat` の**祖先塔**、全自然数次数 `Nat → Nat` の**直接連続反転数塔**、完全な**順序付きraw反転ラン長列**が同一。
- v5.70の**単位簡約した非結合的括弧構造**も、両者とも `reversed unit` で一致する。
- しかし真正 `inherited` 葉の個数は `Count(A)=0`、`Count(B)=1` と異なる。この新しい商不変量の値が異なるため、**新7構成子商のクラスが異なり、新19D Type値比較は存在しない**。

さらに真正の元18D証拠 `M:J→N` が**与えられている場合**に限り、`chain M A` と `chain M B` を**同じJ→N exact fiber**へ構成する。既存二重無限観測＋順序付きrun＋括弧構造は一致し、継承葉数だけ1ずれたままなので、拡張された商観測の**非単射**、継承葉数decoder不存在、全商クラスdecoder不存在が成立する。指定 `J→J` では元の `strict J` が実在するため、endomorphism版を得る。異端点fiberの任意非空性を仮定しない。

## CI・公理監査

- 初回[定理CI #42702482799](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42702482799) は**FAILURE**。元の二つの `by decide` が依存型自由変数を含む未正規化目標に直接適用されたため、Leanで型検査できなかった。この未認証sourceを統合していない。
- 修正は二つの証明内で目標を `change (1 : Nat) ≠ 0` と `change (0 : Nat) ≠ 1` に明示的正規化してから `decide` を呼ぶだけ。前提・主張・元証拠・比較生成元を変更しない。
- 修正版[exact-source 定理CI #42703283304](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42703283304) **completed SUCCESS**：Scoped Strict Lean **9,123/9,123**、Governance **5/5 SUCCESS**、変更Lean error／warning **0/0**、新規sorryAxなし。
- [公開exact-source CI #42704282810](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42704282810) **completed SUCCESS**：KuuOSFormal Strict Lean **10,384/10,384**、Governance **30/30 SUCCESS**、変更Lean error／warning **0/0**、新規sorryAxなし。
- 新規**31宣言すべて**に `#print axioms` を設定。両CIの実際のLeanログで照合し、**19宣言は公理依存なし**、**12宣言は標準 `propext`・`Quot.sound` の範囲のみ**。新規任意公理はない。
- CI SUCCESSは、固定環境とこの証明範囲での形式型検査結果であり、全WORLDの真理や実行権限に自動的には昇格しない。

## 証明の境界・次段

- この新不変量は、**継承した旧18D証拠の出現個数**のみを記録する。異なる`inherited`の**元証拠値そのものの等式・完全識別**、raw `strict`履歴全体の降下、すべての新商クラス分類は証明していない。
- v5.71で「継承葉数」まで追加した後の完全識別性は**NO_DATA**。次段は、継承旧18D葉の**値・順序**をどう扱うと商の比較規則と両立するか、または限定構文の忠実性を独立に調べる。
- 20D gluing、異WORLD貼合、無条件の異端点fiber非空性、制度的な行為権限はいずれも未認証（NO_DATA）。生の18D raw構文と商クラスを混同しない。
- append-only／tighten-only／overwrite-forbidden／same-root。元Type値・独立した旧新19D比較・公開root107・固定Lean/mathlib・保護#1558 Draft／OPEN／未マージを維持。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
