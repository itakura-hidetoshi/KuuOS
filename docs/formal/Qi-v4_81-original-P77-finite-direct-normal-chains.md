# Qi v4.81 — 元P77の真正有限型付き直接正規形鎖・連結観測整合性

## 0. 唯一の正本と検証

2026年11月6日 JST。Repository: `itakura-hidetoshi/KuuOS`、canonical branch: `main`。

| 項目 | 確定結果 |
|---|---|
| 継承基点 | Qi v4.80、main `cd04a947d0b6c4348670b191b4eb65fa7b571ec5` |
| 定理PR | [#3185](https://github.com/itakura-hidetoshi/KuuOS/pull/3185) — MERGED |
| 最終exact-source HEAD | `c83ae4fbc928c4e31ee9b33c5213d13ee01a14fc` |
| 定理squash | `005d9654498940e350a83fb848b4bc9d1f9d463d` |
| source/test-merge/squash共通Git tree | `c3dd2ec984140267865268616f7168c9ea768a38`、完全一致 |
| exact-source CI | [#42169039909](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42169039909) — completed/SUCCESS |
| Strict Lean | **10,280 / 10,280 SUCCESS** |
| Strict Lean job | `127732404990` completed/success、実Lean step 14 completed/success |
| Governance全job | **30/30 completed/success** |
| 実公理出力 | 新規22宣言 **22/22**、標準公理のみ、`sorryAx` なし |
| 変更Lean warning/error | **0/0** |
| Pin | Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開・保護 | KuuOSFormal、root107保持、PR #1558 validation-only Draft/OPEN/未マージ |

[新規Leanファイル全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FiniteDirectNormalChainsV4_81.lean) · [Qi v4.80正式記録](Qi-v4_80-original-P77-direct-front-normal-associativity-units.md)

## 1. 真正有限型付き正規形鎖

v4.80では任意3連結の元Type値正規形に対し観測上の結合則・左右単位則を証明していた。v4.81は有限長を任意に拡張し、途中の元Family・部分State・元ReassocRoute・Scheduleを失わない型付き列を構成する。

`DirectNormalChain f g h k F s G t` は二つの構成子を持つ。

- `nil F s`: 任意の部分状態に存在する、真正の空鎖。完成状態は仮定しない。
- `cons N rest`: 元の`FrontNormal F s M m`と、厳密に一致する中間Family／部分Stateから始まる後続鎖。中間値は依存型添字と真正Type値データに残る。

`directChainPlan`はこの実鎖を、旧`FivefoldP77RawPatchRefinementPlan`へ逐次コンパイルする。空鎖にも既存の元`recut.refl`を用いる。各リンクの`frontPlan`が本来持つ元GK5CG五セル値を別の恒等値へ置き換えない。

`directChainFold`は末尾にv4.80の真正`directNormalUnit`を置き、`directComposeFrontNormal`で右再帰合成する。これも元の鎖そのものとは**別のType値**である。

`directChainSingleton`は単一の実正規形を元一要素鎖に埋め込み、そのfoldが元正規形と三観測で一致することを`directChainSingleton_observed`で証明する。構成子や五セル履歴の等式は不要である。

## 2. 任意有限鎖の正当性

主定理`directChainFold_observed`は、任意の実鎖Cについて、

```text
PlanObservedEq (frontPlan (directChainFold C)) (directChainPlan C)
```

を形式証明する。これは全域の三成分、すなわち、

- 最終raw添字すべてのforwardIndex一致。
- 開始raw添字すべてのbackwardIndex一致。
- 最終真正source witnessすべてについて元source Type値pullback一致。

を同時に表す。元の局所Plan、Type値、source witnessをsubsingleton性で消去せず、一般refinement coverageの全単射性も仮定しない。

証明は元鎖の構造帰納による。空鎖ではv4.80の`directNormalUnit_observed`、consではv4.79の`directComposeFrontNormal_observed`とv4.77の`planObservedEq_comp`・帰納仮定を合成する。

## 3. 連結と任意分割の整合性

`directChainAppend C₁ C₂`は、同じ実中間Family／部分Stateで二つの鎖を連結する。

**鎖の構成子についてのみ**、`directChainAppend_nil_left`、`directChainAppend_nil_right`、`directChainAppend_assoc`は元Type値の厳密等式を証明する。これらを正規形の`ReassocRoute`語の厳密な結合則と読み替えない。

`directChainPlan_append_observed`は元Planの逐次合成を三観測で保持する。主定理`directChainFold_append_observed`は、任意の元鎖C₁,C₂について、

```text
Obs (frontPlan (directChainFold (directChainAppend C₁ C₂)))
 = Obs (frontPlan (directComposeFrontNormal
     (directChainFold C₁) (directChainFold C₂)))
```

をLean4で形式証明する。証明は連結後foldの観測、元Plan連結の観測、両部分foldの観測、二正規形の直接合成観測の四段を、元`PlanObservedEq`の合同性・対称性・推移性で結ぶ。

したがって実鎖の任意の**一つの分割点**について、分割前後の全raw添字・元source復元は一致する。任意の二分括弧付け木を明示し、それらの真正五セルのhigher coherenceを示すのは別の課題である。

## 4. 元GK5CG五セル・source認証・obstruction

- `directChainFold_forward`、`directChainFold_backward`、`directChainFold_pullback`：上記三観測の全域投影を個別の定理として公開。
- `directChainFold_rawSquare`、`directChainFold_rawLoop`：元鎖Planとfoldの元GK5CG五セル値を**二つ別々に保持**し、証明済みforward一致でraw四セル端点を合わせ、元のloop値を構成する。loop自明性／高次セルの存在は主張しない。
- `directChainFold_path`、`directChainFold_certified`：両側が元Quiver.Pathと真正source認証付きP77部分Homを保存。
- `directChainFold_certify_raw`：与えた真正最終source証拠で両側をそれぞれ認証したraw比較が、その**同じ側**の選択済み比較と一致。異なる側の元五セル値同士の等式は証明しない。
- `directChainFold_allCompatible_iff`と`directChainFold_obstructed_iff`：両側の全段compatibility／その否定が、**共通の最終因子木**`tree G t`のcompatibility／obstructionにそれぞれ同値である。

任意の細分Stepを横断した全中間状態間でobstructionが不変、欠けたsource証拠を生成する、正規化の単射性、五セルloopが自明といった結論には拡張しない。

## 5. 検証、実公理、失敗修正

新規Leanファイル1件（395行の差分）、公開集約`formal/KuuOSFormal.lean`のimport 1行のみを追加。既存定理ファイル・toolchain pin・mathlib manifest・workflow・runtime・公開rootは変更していない。

新規22宣言は`DirectNormalChain`、`directChainPlan`、`directChainFold`、`directChainSingleton`、`directChainSingleton_observed`、`directChainFold_observed`、`directChainAppend`、`directChainAppend_nil_left`、`directChainAppend_nil_right`、`directChainAppend_assoc`、`directChainPlan_append_observed`、`directChainFold_append_observed`、`directChainFold_forward`、`directChainFold_backward`、`directChainFold_pullback`、`directChainFold_rawSquare`、`directChainFold_rawLoop`、`directChainFold_path`、`directChainFold_certified`、`directChainFold_certify_raw`、`directChainFold_allCompatible_iff`、`directChainFold_obstructed_iff`である。

最終実`#print axioms` 22件の依存は`propext`・`Classical.choice`・`Quot.sound`のみ。`sorryAx`、追加公理、変更Lean warning/errorは0。

初回ソース`81438128e794d6099f4f98e2cadcd1d5ea95f7a6`の[CI #42168507367](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42168507367)は、185行`directChainAppend_assoc`で`Application type mismatch`となり失敗した。依存型帰納法により`ih`は第二の鎖`C₂`を受け取る全称関数だったが、その引数を省いて等式証明として使おうとしていた。修正は`ih`を`ih C₂`と適用するのみ。Lean4エラーログ、変更Lean全文、元型・imports・依存定理、固定pinを照合し、定理文・仮定・結論は不変にした。

修正HEAD `c83ae4fbc928c4e31ee9b33c5213d13ee01a14fc`の[CI #42169039909](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42169039909)でStrict Lean **10,280/10,280**、workflow全30 jobs、実Lean step14すべてSUCCESS。22件の実公理出力は標準公理のみ、変更Lean warning/error0/0、Git tree一致を確認し、検証済みHEADを指定してsquashマージした。初回失敗CIを成功証拠として流用しない。

## 6. 継続研究

Qi v4.82候補は、真正有限鎖の全二分括弧付けを保持する型付き構文`DirectNormalBracket`を導入し、元の順序付き鎖へのflatten一致を条件に任意の二括弧付けの全raw添字／source pullbackの観測同値を証明する。元五セル値・loopを同一視せず、higher pentagon coherenceを無根拠に付加しない。

strict 空中心、独立Kuu＝presentation、元Type値・source証拠・authority・obstruction、same-root、append-onlyを継続。旧scheduled MGAP pollerの`state_store_missing`は別のruntime状態ストア問題であり混在させない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
