# Qi v5.81 — 真正whiskering／raw反転の配置履歴障害（Lean4形式証明・実公理監査）

2026年11月10日 JST。対象は元の真正contextual18D依存Type証拠、元selected19の5構成子と別Typeで与えた新raw-congruent selected19の7構成子、実際に供給された同一端点fiberの元Type値・真正商である。「空」「縁起」との対応は命名・解釈層にとどまり、証明された等式や商の普遍的意味であるとは主張しない。

## 1．canonical正本と正式統合の来歴

- Repository: `itakura-hidetoshi/KuuOS`、canonical `main`。研究起点はQi v5.80正式統合済みHEAD `a6e835f3eca23cb0cca4b4e6ee611744d913a5b9`。
- [定理PR #3473](https://github.com/itakura-hidetoshi/KuuOS/pull/3473) **MERGED**。追加したのは `formal/KUOS/Architecture/QiWuxingGK5CHP77WhiskerReversePlacementResidualV5_81.lean` の新規1ファイル（768行、44宣言、44個の独立`#print axioms`）。既存Lean定理・仮定・比較構成子の変更削除なし。
- 定理認証source `1963d24bd4e08da044f0c121359fd4ad56fcc9e1`、test-merge `2c2cda6be4dea05110a80ee0fecadb391b93eb5b`、squash `3f37ac7246a33829521386a4c29e567380d1d9c2`。三者のGit treeは `9a8510863c55147136895dfc5c7235ea980a0fe9` と一致。
- [公開import PR #3474](https://github.com/itakura-hidetoshi/KuuOS/pull/3474) **MERGED**。`formal/KuuOSFormal.lean`に`import KUOS.Architecture.QiWuxingGK5CHP77WhiskerReversePlacementResidualV5_81`を1行追加。既存import 688件すべて維持、公開root107不変。
- 公開認証source `d8a65a3d59f77801d73df0d48b742b4fc28d0bf6`、test-merge `f206bb9506c85f10370244e85a87195ac2979765`、squash `dfa51b5238c756034e30f452ab73fa9fab376657`。三者のGit treeは `b82733e887ded785bb1dfbe3a1475af64dd2bbeb` と一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` を固定。validation-only [保護PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。

## 2．初期証拠対の失敗を保存したobstruction

元の外側7D whiskering列`List Bool`は、whiskeringの左／右と出現順を記録する。ただしこの列の一致は、v5.80完全観測の一致を意味しない。

真正の`N→N`を一つ供給し、`S = strict N`とすると、当初検討した
- `U = whiskerLeft before F G (reverse S)`
- `V = reverse (whiskerLeft before F G S)`

は同じwhiskered `N'→N'` fiberでも、**すでに認証済みの`TopReverseFlag`がそれぞれ0と1**である。同様に右whiskeringについても0対1で区別される。したがって、これらを「v5.80完全観測が等しい反例」と呼ぶことはできない。

初回CI [#42757546906](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42757546906)では完全観測の等式を`rfl`で処理しようとして失敗した。次の [#42758221615](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42758221615)、[#42758832191](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42758832191)で積型分解と`funext`を進めた結果、残る第九観測座標のTopReverseFlagの不一致が明示された。これは単純なLean4構文エラーではなく、元証拠対に対する数学的障害である。

`selectedWhiskerLeft_unmaskedTopFlagObstruction`と`selectedWhiskerRight_unmaskedTopFlagObstruction`を新たに形式化し、旧観測の不一致を**隠さず保存**した。既存TopReverseFlagの定義・商降下・旧新比較の生成元を変更せずに修正した。

## 3．真正の同一fiberで成立するstrict-prefix証拠対

真に与えられた`SevenRewrite before`、対応する`ContextFrameEleven F,G`、元17D端点`N`に対して`N' = whiskerLeft before F G N`、`S' = strict N'`と置く。元の依存Type18D構成子だけで真正`N'→N'`証拠
```text
A = chain S' (whiskerLeft before F G (reverse (strict N)))
B = chain S' (reverse (whiskerLeft before F G (strict N)))
```
を作る。右の場合も、真に供給された`after`と`N' = whiskerRight F G N after`に対し、同じ`strict N'`を両者の外側左子として置く。

**共通strict-prefix**により両者の最上位は真正raw `chain`となり、以前の0対1のTopReverseFlag障害は同一値0に揃う。旧19D比較の適用範囲を拡張するのではなく、元の型付き18D証拠を新たに構成した。

元九変量観測（TopReverseFlagを含む）、二本の**全Nat→Nat祖先塔／連続run塔**、ordered反転run、元旧18D継承根・完全内部括弧、反転siteとイベント語、v5.77 strict-only最大枝形、v5.78反転祖先深度、v5.79左右経路、v5.80 inherited-guarded raw treeの**完全な直積観測**が、この両証拠で等しいことをLean4で証明した。無限塔の等式は各次数から`funext`で構成する。有限サンプルに弱めていない。

## 4．新しい独立観測と真正商での識別

別定義の非結合`SelectedWhiskerPlacementTree`は、真正継承旧18D値の内部構文観測`source`、raw `strict`、左右`whisker`ラッパー、raw `reversed`、raw `joined`を保存する。直下の厳密な`source`と`strict`の単位2式のみ簡約し、raw反転・whiskerとの一般単位律や結合律を課さない。元証拠のType値自体をこの独立構文で置き換えない。

共通strict-prefix付きの真正証拠では新観測が
```text
left A : joined strict (left (reversed strict))
left B : joined strict (reversed (left strict))
right A: joined strict (right (reversed strict))
right B: joined strict (reversed (right strict))
```
となり、各対は自由補助構文として異なる。

新観測が元旧selected19の全5構成子、新`SelectedRawCongruentNineteen`の全7構成子で保存されることを各Type値比較に関する帰納法で証明。**元旧商・独立新商それぞれへの`Quotient.lift`**、旧→新射影との因子化、v5.80 guarded treeへのforgetful projectionも証明した。

したがって、供給された各真正whiskered `N'→N'` fiberに限って、二つの新7構成子商クラスの不一致、元新Type19D比較の不存在、**v5.80完全商観測の非単射性**、新商クラスを完全観測から復元するdecoderの不存在が形式的に成立する。これは生構文文字列の違いから商の違いを推測した結果ではない。

## 5．exact-source Lean4と公理の実監査

- [定理CI #42760200340](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42760200340)：**terminal SUCCESS**。Scoped Strict Lean **9,133/9,133**、Governance・Core Autonomy **SUCCESS**、独立exact-head completion receipt **SUCCESS**。変更Lean error／warning 0／0。
- [公開CI #42762351012](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42762351012)：**terminal SUCCESS**。KuuOSFormal Strict Lean **10,394/10,394**、選択全30ジョブ **SUCCESS**、独立exact-head completion receipt **SUCCESS**。
- 定理・公開CIの新規**44/44宣言**の実`#print axioms`出力を再照合。**公理不要14／標準`propext`・`Quot.sound`のみ30**。新規`sorryAx`なし。これは対象44宣言の監査であり、全mathlibや他系統の公理依存についての大域主張ではない。
- 定理・公開のsource／test-merge／squash各Git treeはそれぞれ一致。GitHub Actionsでの成功と本記録は、元ソースの型付き定理・公理出力を超える数学的全域完全性を意味しない。

## 6．範囲、未認証、次段

成立条件は、実際に与えられた`SevenRewrite`と`ContextFrameEleven`および真正17D端点`N`に限る。任意のwhiskering文脈の無条件存在、任意異端点fiberの居住性、旧新商の大域分類・忠実復元、20D gluing、WORLD横断降下、制度的・実行権限は**未認証（NO_DATA）**として残す。

**Qi v5.82候補**：新しくwhiskering順序を保持した完全観測でも残る証拠差があるか、二重whiskeringの入れ子位置、供給された元旧18D証拠の内部差、および局所降下条件を独立に調べる。v5.81の証拠対は新観測で区別されるため、そのまま次段の非単射反例に流用しない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
