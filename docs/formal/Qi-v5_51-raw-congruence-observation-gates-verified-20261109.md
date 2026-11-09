# Qi v5.51 — 新raw文脈合同性商での順序付き観測保存と元19D情報の降下障害

正式記録日：2026-11-09 JST

## 1. 正本・機械検証の出典

唯一のcanonical正本は `itakura-hidetoshi/KuuOS` の `main`。Qi v5.50までの元selected19比較、元18D〜19D Type値証拠、すべての独立presentation、公開root107は書き換えない。

- [定理PR #3383](https://github.com/itakura-hidetoshi/KuuOS/pull/3383) **MERGED**：`1abe67ee1f2dadf75914eaf367274e56bc65ad97`。
- [公開import PR #3384](https://github.com/itakura-hidetoshi/KuuOS/pull/3384) **MERGED**：`1ad71c858a900d6ff9d44fef614e5b8ce3ba03a0`。
- [新規Lean4モジュール全文](https://github.com/itakura-hidetoshi/KuuOS/blob/1abe67ee1f2dadf75914eaf367274e56bc65ad97/formal/KUOS/Architecture/QiWuxingGK5CHP77RawCongruenceObservationsV5_51.lean)。新規1ファイル220行、削除0。
- [Qi v5.50の形式記録](Qi-v5_50-typed-raw-congruence-completion-verified-20261109.md)。v5.50で元19D商から新しい文脈合同商への全射と、与えられた元18D witnessによる非単射を証明済み。

本段階の証明は、v5.50の新Type値比較 `SelectedRawCongruentNineteen` を対象とする。これは旧 `SelectedLocalNineteen` の改変でも同一型への別名でもない。

## 2. 新presentationの7構成子すべてについての保存

独立の新Type値比較の構成子は `inherited`、`strict`、`reverse`、`chain`、`rawReverse`、`rawChainRight`、`rawChainLeft` の正確に7種類。

`selectedRawCongruent_preservesTrace` は、指定の同一16D fiber・真正17D始終点 `J,N` とraw18D証拠 `M,L` について

```text
A : SelectedRawCongruentNineteen ... J N M L
------------------------------------------------
selectedContextEighteenTrace l r M
  = selectedContextEighteenTrace l r L
```

を、7構成子全部に対する構造帰納法で証明する。元19D比較からの `inherited` では旧保存定理を使用し、raw反転は既存traceを変えず、raw左右合成ではそれぞれ固定したtrace列との結合 `++` による合同性を使う。ordered traceは単なる長さやイベント個数ではなく `List Bool` の**順序付き全履歴**である。

`selectedRawCongruentTraceOnQuotient` は新しい商上に実際の `Quotient.lift` を構成。`selectedRawCongruentTrace_onClass` は元raw代表に対する評価式、`selectedRawCongruentTrace_factorsOld` は旧商から新商への全射射影と旧trace観測の正確な因子化等式を証明する。

## 3. raw反転構成子回数も保存される

`selectedRawCongruent_preservesReverseCount` は、真のraw `reverse` 構文節点の数 `selectedContextEighteenReverseCount` について同じ7構成子帰納法を実施する。

比較証拠の反転 `reverse` は元rawを変更せず、`rawReverse` は両辺の回数に各1を加え、`rawChainRight`／`rawChainLeft` は固定raw文脈の回数を両辺へ同じ側から加える。

`selectedRawCongruentReverseCountOnQuotient` は新商への正真正銘の `Quotient.lift`、`selectedRawCongruentReverseCount_onClass` はクラス上の評価式である。

重要：保存するのはraw反転**回数**であり、任意の二重反転 `reverse(reverse M)=M` を新商で同一視したわけではない。

## 4. 保存されない旧観測と正規代表の障害

元18D証拠 `M : SelectedLocalEighteen ... J N` が実際に与えられたfiberに限り、

```text
A = chain (chain (strict J) (inherited M)) (strict N)
B = chain (inherited M) (strict N)
```

を構成する。これらはv5.50の新しい `rawChainRight` 比較では同一視されるが、v5.44の元 `LeftNestedCount` は `A` で1、`B` で0となる。

- `selectedRawCongruent_leftNested_changes`：この二つのraw計数値は等しくない（公理不要）。
- `selectedRawCongruent_leftNested_noDescent`：新商上に、このraw左入れ子計数を**全raw代表について保持する観測関数は存在しない**。`Quot.sound` によるクラス同一視と計数非一致を接続した。
- `selectedRawCongruent_oldNormal_noDescent`：同様に、旧v5.48の正確な型付きselected19正規代表 `selectedNineteenNormal` も、新しい商を通じて全代表に対し再現する関数としては降下できない。v5.49の旧raw反転非合同性障害を保持して証明。

元v5.47の旧6変量 `I6` は `LeftNestedCount` を含むため、**旧I6をそのまま新商の不変量と宣言できない**。ただし他の各変量を個別にすべて分類したわけではない。また当該証拠 `M` が存在しないfiberに勝手に反例を拡張しない。

ここで実証されたのは、「失われる計数・正規代表」と「なお保存されるordered trace・raw反転回数」を分離できることである。元raw証拠を置換して障害を隠す修復ではない。

## 5. exact-source検証とtree一致

| 検証 | 確認した結果 |
| --- | --- |
| 定理exact-source CI | [#42538653834](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42538653834) **SUCCESS** |
| 定理Scoped Strict Lean | **9,103 / 9,103 SUCCESS** |
| 定理Governance | **5 / 5 SUCCESS** |
| 新規10宣言公理監査 | **7件公理なし、3件標準公理のみ、sorryAxなし** |
| 変更Lean warning/error | **0 / 0** |
| 定理exact-head 2受領書 | **SUCCESS / SUCCESS** |
| 公開import exact-source CI | [#42539127337](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42539127337) **SUCCESS** |
| 公開KuuOSFormal Strict Lean | **10,364 / 10,364 SUCCESS** |
| 公開Governance | **32 / 32 SUCCESS** |
| 公開exact-head 2受領書 | **SUCCESS / SUCCESS** |

定理source HEAD `44614462a0b2ab253307d8b6c8c1f3f450ac0650`、test-merge `e71af5b4f7806d6ab0bd0cb4e70e4b67044e2651`、統合main `1abe67ee1f2dadf75914eaf367274e56bc65ad97` は共通Git tree `137d9e2cf6d2b6ab8ef7eefa79917a32b72b49b1`。

公開import source HEAD `8e372eec8a9d5716209549eabd1c704b3c0f50d4`、test-merge `d7cce332c5939c45144d7567d7e9cc31d6b89671`、統合main `1ad71c858a900d6ff9d44fef614e5b8ce3ba03a0` は共通Git tree `ee49e69c8524b52683c6019a309ae88ac6899025`。

初回定理CI [#42538244197](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42538244197) は再帰的 `simp` の `whnf` heartbeat超過6件により失敗。新構成子の計算規則を `exact` と `congrArg` による定義上の等式へ改め、追加公理・仮定の変更・heartbeat増大なしに修正後CI成功。失敗時の `sorryAx` はLeanの失敗した証明項に対する診断であり、修正後は不在。

## 6. 公理監査10件（新規宣言）

| Lean宣言 | `#print axioms` |
| --- | --- |
| `selectedRawCongruent_preservesTrace` | なし |
| `selectedRawCongruentTraceOnQuotient` | なし |
| `selectedRawCongruentTrace_onClass` | なし |
| `selectedRawCongruentTrace_factorsOld` | `Quot.sound` |
| `selectedRawCongruent_preservesReverseCount` | なし |
| `selectedRawCongruentReverseCountOnQuotient` | なし |
| `selectedRawCongruentReverseCount_onClass` | なし |
| `selectedRawCongruent_leftNested_changes` | なし |
| `selectedRawCongruent_leftNested_noDescent` | `Quot.sound` |
| `selectedRawCongruent_oldNormal_noDescent` | `propext, Quot.sound` |

既存数学的定義・元Type値証拠・新旧商の区別、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージを維持する。

## 7. 研究の境界／次段

証明されたのは、**指定された同一16D fiberの真正17D端点における**二つの保存観測と、真正旧18D証拠が与えられたfiberにおける旧観測・旧正規形の非降下である。

次の数学的課題は、既存v5.43 `selectedContextEighteenDoubleReverse_reverseCount`（raw二重反転で計数が2増える）とv5.51の新商 `ReverseCount` 降下を接続し、**新商でもなお区別される二重反転証拠**を独立した定理として形式化すること、および他の旧5変量の新商への降下可否を1変量ずつ分類すること。この追加の「新商での二重反転類の不一致」は**本v5.51モジュールの独立定理としては未実装**であり、形式証明済みの10宣言と混同しない。

異なる元16D fiber間のwhiskering、20D coherence、一般の高次gluing、全fiberのinhabitance・比較可能性、元19D証拠の忠実回復は未認証（NO_DATA）。局所的な商の降下を大域的権限に昇格しない。運用：append-only／tighten-only／overwrite-forbidden／same-root。

本記録はdocs-onlyであり、新たなLeanソース・import・CI workflow・pinを変更しない。docs-only CIではStrict Leanを走らせない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
