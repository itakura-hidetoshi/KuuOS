# Qi v4.83 — 元P77真正型付き五角形の二経路観測整合性

## 0. 唯一の正本・厳密な検証

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。

| 項目 | 最終結果 |
|---|---|
| 継承基点 | Qi v4.82、main `6a9e8b51757a0d9546b5e97401a390f10cd4c3db` |
| 定理PR | [#3189](https://github.com/itakura-hidetoshi/KuuOS/pull/3189) — **MERGED** |
| exact-source HEAD | `47e794f8cd3855f2de7f3e7000f86f12b80c96ed` |
| 定理squash SHA | `6447439c7c63bf15be041b63005d1183ca37ee78` |
| source/test-merge/squash Git tree | `4c9811b4d545bf87a066e4f8cdf9cc8a426affcf` — 完全一致 |
| exact-source CI | [#42173062119](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42173062119) — **completed/SUCCESS** |
| Strict Lean | **10,282 / 10,282 SUCCESS** |
| Strict Lean job | `127745243374` — completed/success、実Lean step 14 completed/success |
| Governance | **30 / 30 jobs completed/success** |
| 公理監査 | **新規39 / 39宣言、標準公理のみ**：`propext`・`Classical.choice`・`Quot.sound` |
| `sorryAx`／変更Lean warning/error | **なし／0/0** |
| 固定Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開・保護 | `KuuOSFormal`、root107維持、PR #1558 Draft／OPEN／未マージ |

[新規Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ActualTypedPentagonObservationV4_83.lean) · [Qi v4.82正式記録](Qi-v4_82-original-P77-typed-binary-normal-brackets.md)

## 1. 数学的対象：五つの真正二分括弧付け

v4.82は任意の有限型付き二分木の評価が、元の順序付き真正`DirectNormalChain`を右foldしたものと全域観測で一致することを証明済みである。

v4.83では4つの**任意の真正型付き部分木**`A,B,C,D₄`（各部分木は任意有限長・空木も可）について、5つの異なる元Type値二分木を定義する。

```text
V0 = (((A B) C) D₄)
V1 = ((A (B C)) D₄)
V2 = (A ((B C) D₄))
V3 = (A (B (C D₄)))
V4 = ((A B) (C D₄))
```

各部分木の中間`Family`・部分`State`は`DirectNormalBracketTree`の依存型添字で実際に一致している。葉は元の`FrontNormal`、再括弧付けrouteとScheduleは実際の構成子のまま保持される。次数・長さだけの抽象ペンタゴンや商で代替しない。

## 2. 元の順序付き鎖での五辺の厳密整合性

5つの真正局所回転は以下の有向辺を与える。

```text
       V0 → V1 → V2 → V3
        ╲             ↑
         →  V4  ─────┘
```

`pentagonFlatten01`、`pentagonFlatten12`、`pentagonFlatten23`、`pentagonFlatten04`、`pentagonFlatten43`は、各辺で**元の順序付き有限鎖そのものの厳密等式**を証明する。証明の核は既存の`bracketNode_assoc_flatten`（その根拠はv4.81の`directChainAppend_assoc`）と、元の左右部分木コンテキストへの`congrArg`である。元のsource chainは削除・再構成・商化しない。

2つの異なる経路から得た端点の元鎖等式は`pentagonFlatten_long`と`pentagonFlatten_short`として別々に保存する。ここでの**厳密等式は鎖の構成子レベルに限る**ので、評価後の`FrontNormal` route語の厳密結合則は主張しない。

## 3. 2経路の全域観測整合性

5辺で`bracketSameChain_observed`をそれぞれ適用し、全forward／backward raw index、および元source-witness Type値pullbackの同値を個別に証明する。

- `pentagonLong_observed`：3辺 `V0→V1→V2→V3` の観測証明を合成。
- `pentagonShort_observed`：2辺 `V0→V4→V3` の観測証明を合成。
- `pentagonTwoPaths_forward`、`pentagonTwoPaths_backward`、`pentagonTwoPaths_pullback`：2経路を**独立した証明項**として、同一の全域端点観測命題の2件の証明を明示する。

この数学的な意味は**観測レベルの五角図式可換性**である。`PlanObservedEq`の証明が同じ命題を確立することを、元五セルの2経路の合成そのものに関するhigher equalityと混同しない。五セル合成によるpentagonatorの存在は導かれない。

## 4. 真正GK5CG元五セル・source・compatibility・障害

- 五辺の`pentagonEdge**_rawSquare`と`pentagonEdge**_rawLoop`が、双方の元GK5CG五セルType値を持つraw squareと**非自明であり得るloop**を5辺ごとに保持する。選択五セル値の同一視・各loopの充填はしない。
- `pentagonEndpoint_rawSquare`、`pentagonEndpoint_rawLoop`は共通端点に対する元Type値を別途保持する。**五辺の五セル合成を作ったという主張ではない**。
- `pentagonEndpoint_path`、`pentagonEndpoint_certified`、`pentagonEndpoint_certify_raw`は元Quiver.Path、真正source-certified P77 partial Hom、各側の元raw比較を保持する。source witnessがsubsingletonである、任意の未存在source証拠を作れる、とは仮定しない。
- `pentagonEndpoint_allCompatible_iff`と`pentagonEndpoint_obstructed_iff`は両端点の全Plan compatibility／障害を共通の**最終因子木**に還元する。途中の任意refinementを横断する障害の一律不変性を主張しない。

## 5. 実装と検証方法

新規Leanモジュール（497行）1件と、既存`formal/KuuOSFormal.lean`へのimport 1行のみを追加。旧証明定理、元source、manifest、toolchain、Lean limit、workflow、runtime、公開rootのいずれも変更していない。

新規39宣言の`#print axioms`出力をGitHub MCPで実ログから数え、12件が`propext/Quot.sound`、27件が`propext/Classical.choice/Quot.sound`に依存。新規公理・`sorryAx`なし、変更Lean warning/error 0/0。初回exact-source CI `#42173062119`が全体SUCCESSとなり、実Lean step 14はcompleted/success。修正用の失敗CIはない。

`47e794f8cd3855f2de7f3e7000f86f12b80c96ed`のsource treeとGitHubのtest-merge treeを比較し、その後squash SHA `6447439c7c63bf15be041b63005d1183ca37ee78`のtreeまで同一性を独立確認した。検証済みHEADを指定してマージ済み。

## 6. 次の研究境界 — Qi v4.84候補

真正五角形の観測可換性は完了。一方で**元五セルについてのhigher coherenceが成立するか**は別である。次段階ではまず、既存GK5CG五セルの合成演算が、五辺のraw square／loopの値について**元のsource/target Typeと合成可能性**を持つかを検査する。そのうえで合成が構成できる範囲に限り、3辺経路と2辺経路の元Type値合成証明書を別々に定義し、一致または一致を妨げるobstructionを正確に形式化する。

観測同値だけから充填やloop自明性を推論せず、strict 空中心・独立Kuu＝presentation・same-root・append-only・tighten-only・obstruction-aware descentを継承する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
