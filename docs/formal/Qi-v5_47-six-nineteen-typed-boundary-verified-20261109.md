# Qi v5.47 — 六変量型付き19D境界のkernel分類と連続反転の残存障害

記録日：2026-11-09 JST

現行の独立selected 19D presentationを固定し、実際に与えられた元Type値証拠と厳密endpoint fiberの範囲で認証する。構造と「空」「縁起」の対応づけは解釈であり、以下のLean定理とは区別する。

## 1. 正本と実行検証

- [定理PR #3371](https://github.com/itakura-hidetoshi/KuuOS/pull/3371)：MERGED。新規Leanモジュール1件、594行、既存削除0。
- [公開import PR #3372](https://github.com/itakura-hidetoshi/KuuOS/pull/3372)：MERGED。`formal/KuuOSFormal.lean`へのimport 1行追加、既存削除0。
- [認証済みLean全文](https://github.com/itakura-hidetoshi/KuuOS/blob/0615df018cc5e794b07037f3531f7306d0bd9cad/formal/KUOS/Architecture/QiWuxingGK5CHP77SixNineteenTypedBoundaryV5_47.lean)。
- [認証済み公開集約](https://github.com/itakura-hidetoshi/KuuOS/blob/0744205e15edf0c3fb51b3ba7d15233dc412883b/formal/KuuOSFormal.lean)。

| 検証 | 定理の独立検証 | 公開集約の独立検証 |
| --- | --- | --- |
| exact-source CI | [#42524549959](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42524549959) SUCCESS | [#42525454553](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42525454553) SUCCESS |
| Strict Lean | 9,099 / 9,099 | KuuOSFormal 10,360 / 10,360 |
| Governance workflow jobs | 5 / 5 SUCCESS | 32 / 32 SUCCESS |
| 変更Lean error / warning | 0 / 0 | 0 / 0 |
| `sorryAx` | なし | ログ内になし |

公開Governanceは`per_page=100`で全32件を取得し、全件の`completed/success`を確認した。先頭ページのみの件数を総数とはしていない。同じ公開source HEADの補助workflowは8件SUCCESS、`Independent Kuu Foundation`はSKIPPED。これは実行済みのKuuOSFormal Strict Leanとは別の判定である。

| Git来歴 | 定理 | 公開import |
| --- | --- | --- |
| source HEAD | `6ce992471b01b360bb13cae059a076cdc3d88d6b` | `4d54b067c6cf0987bdb077a6ee2f932188fb3595` |
| test-merge HEAD | `9ea479a26bea666163131ffbcd430fa8b4c07450` | `cd91e8268aaaf1557e352b66dfbb3cb3f903036d` |
| squash / main統合SHA | `0615df018cc5e794b07037f3531f7306d0bd9cad` | `0744205e15edf0c3fb51b3ba7d15233dc412883b` |
| 上記3状態に共通するGit tree | `e92233964f6dc77ce797ebdba60e8ff310470b3f` | `0f66925eee79a8d9d0ed0efdc0146b9e3836a5fd` |

基点はQi v5.46正式完了main `8cbb6cfb33e90e0d28a5bf283b87b944d8257d69`。定理と公開importは別PR・別CIで認証し、それぞれsource / test-merge / squashのGit tree一致をGitHubの一次状態で確認した。

## 2. 六変量を反映する型付き境界

現行の独立selected 19D presentationにおいて、各厳密17D endpoint fiberの真正19D商上に

`I6 = (|Trace|, ActiveChainCount, ReverseCount, LeftNestedCount, ReverseLeftCount, ActiveDepth)`

を構成した。各成分の既存保存定理を組み合わせるため、新しい19D比較構成子や公理は必要ない。

元の型付きMと左右の文脈を与えたとき、真正LR fiberから独立した真正RL fiberへのraw transportを構成した。6変量の入れ子Nat.pair符号を、既存の真正RL trace-powerに渡す。指定LR証拠の六変量を基点として、その六変量の符号を0にする。指定LR証拠の輸送像は、元のRL証拠そのものに一致する。同じ六変量を持つ別のsource証拠も同じ符号0を持つ。sourceの真正19D比較は6変量を保存し、その像が同じRL raw証拠になることから、targetの真正strict比較を構成する。

輸送先のtrace長は`(2 * code + 1) * |Trace(R)|`であり、左右whiskeringを持つ指定RL証拠Rの履歴長は正。したがってtarget商クラスの一致から符号の一致を復元でき、さらにNat.pairの単射性からsourceの6変量が一致する。逆向きは同じ符号なら同じraw輸送像になることで従う。

証明された厳密なkernel分類は `T6(q1)=T6(q2) ↔ I6(q1)=I6(q2)`。これは6数値のsource情報の反映であり、target側の同名6数値がsource側と座標ごとに同じという主張ではない。全域swap自然性とも区別する。

## 3. 同一六変量でも残る連続反転の証拠差

任意に与えられた元証拠`M : J → N`に対し、`S = strict N`とおく。

```
A = chain S (reverse (reverse S))
B = reverse (chain S (reverse S))
L = chain M A
R = chain M B
```

A/Bはともに厳密N→N fiber内の元raw18D証拠であり、L/Rは同じ厳密J→N fiberに属する。元Mはそのまま残る。両者の完全ordered fine traceと6変量は一致する。元Mのtrace非空条件は、この構成には不要。

追加観測`AdjacentReverseCount`は、raw18Dのreverseノードの子が直ちにreverseノードである箇所を数える。whiskeringでは再帰、chainでは加算、strict/inheritedでは0とする。現行の真正19D比較5構成子すべてで保存されることを証明し、同一fiberの19D商へ降下させた。

上記L/Rでは `AdjacentReverseCount(L) = AdjacentReverseCount(R) + 1`。したがって真正19D商クラスは異なり、L/R間の真正Type値19D比較は存在しない。6変量観測は、実際の元証拠Mを与えられるfiberで非単射。具体的なT6も同じ6変量の二クラスを同じ像へ送り、完全なType値比較反映は持てない。

## 4. 境界と次段

結論は現行の独立selected 19D presentationと、今回具体化した6変量境界についてのもの。全fiberの居住性、別の忠実境界の存在・不存在、全域swap自然性、元raw Type値の同一視、無条件20D交換・gluingは導かない。

次段Qi v5.48では、数値観測をさらに増やすだけでなく、既存19D比較が同一視する元構文の範囲と完全な比較反映の条件を調べる。元証拠・元構成子を残して、構文的分類または型付き正規化の可能性を検討する。

## 5. 公理監査と保存条件

新規35宣言の`#print axioms`をすべて照合した。**35 / 35、公理不要19件、標準公理のみ16件、`sorryAx`なし。** 標準公理の集合は`propext`・`Classical.choice`・`Quot.sound`の範囲に限られる。以下の「なし」は、当該宣言のLean公理依存リストが空であることを表す。

| 宣言 | 公理依存 |
| --- | --- |
| `selectedContextEighteenSix` | なし |
| `selectedLocalNineteen_preservesSix` | なし |
| `selectedNineteenSixObservation` | なし |
| `selectedNineteenSix_onClass` | なし |
| `selectedNineteenSix_eq_iff` | なし |
| `selectedNineteenSix_depthBracketsDistinct` | `propext`、`Quot.sound` |
| `selectedMixedSixCode` | なし |
| `selectedMixedSixCode_injective` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixRawTransport` | なし |
| `selectedMixedSixRawTransport_chosen` | `propext` |
| `selectedMixedSixRaw_eq_of_observation` | なし |
| `selectedMixedSixBoundary` | なし |
| `selectedMixedSixAnchored` | `propext` |
| `selectedMixedSixAnchored_chosenClass` | `propext`、`Quot.sound` |
| `selectedMixedSixRaw_reflectObservation` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixDescend_eq_iff_observation` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixAnchored_chosenSwap` | `propext`、`Quot.sound` |
| `selectedContextEighteenAdjacentReverseCount` | なし |
| `selectedLocalNineteen_preservesAdjacentReverseCount` | なし |
| `selectedNineteenAdjacentReverseOnQuotient` | なし |
| `selectedNineteenAdjacentReverse_onClass` | なし |
| `selectedAdjacentReverseLeft` | なし |
| `selectedAdjacentReverseRight` | なし |
| `selectedAdjacentReverse_trace` | なし |
| `selectedAdjacentReverse_rawSixEq` | なし |
| `selectedAdjacentReverse_sixEq` | なし |
| `selectedAdjacentReverse_countDiff` | なし |
| `selectedAdjacentReverse_classDistinct` | `propext`、`Quot.sound` |
| `selectedAdjacentReverse_noLocal` | `propext`、`Quot.sound` |
| `selectedNineteenSix_notInjective` | `propext`、`Quot.sound` |
| `selectedMixedSixDescend_separates_of_depth_ne` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixDescend_separatesStrictReverse` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixDescend_collapsesAdjacentReverse` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixDescend_notInjective` | `propext`、`Classical.choice`、`Quot.sound` |
| `selectedMixedSixBoundary_noReflection` | `propext`、`Classical.choice`、`Quot.sound` |

統合担当は変更Lean全文594行と依存シグネチャ、公理出力全件を確認した。独立レビューはcore 17宣言、integration 5宣言のソース検査と、残存障害の型付きendpoint・六変量一致・分離観測の構成検査を行った。独立レビュー単独で全35宣言を再コンパイルしたとは主張しない。機械検証は上記exact-source CIによる。

元F55/P77/GK5CG、既存6D〜19D、元raw Type値証拠と構成子を保持。新規axiom、証拠の数値への置換、異なるendpoint間のraw同一視は導入していない。公開rootは107、Leanは`v4.30.0-rc2`、mathlibは`5450b53e5ddc75d46418fabb605edbf36bd0beb6`を維持する。保護PR #1558はDraft / OPEN / 未マージのまま。

本記録とREADME・ROADMAPの追記はdocs-onlyとして独立PRにする。Leanファイルやpinは変更せず、docs-onlyのStrict LeanはSKIPPEDを期待する。記録PR自身の実行結果・exact-head判定・統合treeの確認は、そのPRの検証記録に残す。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
