# Qi v4.80 — 元P77直接正規形合成の観測結合則・左右単位則

## 0. 唯一の正本と検証

2026年11月6日 JST、Repository：`itakura-hidetoshi/KuuOS`、canonical branch：`main`。

- 継承元：Qi v4.79、main `9f3616e236f1323d6e941f375bb0e3a4e1952165`（v4.79 README/ROADMAP同期後）。
- 定理PR：[**#3183 MERGED**](https://github.com/itakura-hidetoshi/KuuOS/pull/3183)。
- final exact-source HEAD：`31ee041ad0f94158dc23350bce5e67447bac9f1b`。
- test-merge commit：`1edc7b40e98268ffcd51f6c36c4d04f22277410e`。
- theorem squash／main統合時HEAD：`10ad0e1692bde25fd40d6d228bf264951080b538`。
- source／test-merge／squash Git tree：`2998a9ebc5027cb0e232095afa00712a92673c06`、完全一致。
- [exact-source CI #42166682062](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42166682062)：completed／**SUCCESS**。Governance workflow全30 jobs completed。
- Strict Lean job `127724774190` completed／SUCCESS、実Lean step14 completed／SUCCESS。**10,279／10,279 build success**。
- 新規**24宣言の実公理出力24／24**、標準公理のみ、`sorryAx`なし、変更Lean warning／error **0／0**。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開KuuOSFormal、root107保持。
- 保護PR #1558はvalidation-only Draft／OPEN／未マージ。

[新規Leanモジュール全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77DirectNormalAssociativityUnitsV4_80.lean) · [Qi v4.79正式記録](Qi-v4_79-original-P77-direct-front-normal-composition.md)

## 1. 直接合成の単位正規形

v4.79で、2つの真正`FrontNormal`の直接合成を、元`ReassocRoute.trans`と、第二routeによる第一`Schedule`の`reassocSchedule`移送・`append`で構成した。

今回、どの部分Family／状態`F,s`にも、**真正Type値**`directNormalUnit(F,s) = ⟨ReassocRoute.refl F, Schedule.nil F s⟩`を構成した。これは履歴商の形式的な単位ではなく、実在する元recutと元空Scheduleを保持する値である。

`frontPlan`で解釈した単位は、元の`recut.refl`を2回含むPlanになる。したがって元Planの構成子を単純に反射と等置せず、既存の`planObservedEq_left_refl`から**3観測に限った**単位同値を導いた。

`directCompose_leftUnit_observed`・`directCompose_rightUnit_observed`で、開始側および終了側の任意部分状態において、直接合成の左右単位を証明した。`directCompose_*Unit_history`は、元の`InterleavedHistory`の`historyPlan`と、正規化後の単位合成の全域観測一致を保持する。途中Step、元source Type値、最終部分状態を消去しない。

## 2. 任意3連結の直接正規形と観測結合則

任意の同一端点型で接続可能な三つの真正`FrontNormal` `N₁ : F₀s₀ → F₁s₁`、`N₂ : F₁s₁ → F₂s₂`、`N₃ : F₂s₂ → F₃s₃`について、

- `directAssocLeft N₁ N₂ N₃ := (N₁ ⋄ N₂) ⋄ N₃`
- `directAssocRight N₁ N₂ N₃ := N₁ ⋄ (N₂ ⋄ N₃)`

を**別々の真正Type値**として構成する。`directAssocLeft_route`と`directAssocRight_route`は、それぞれ元の左／右括弧付けReassocRoute語を**構成子どおり**保存する。

主定理`directCompose_assoc_observed`は、これらの`frontPlan`が元`PlanObservedEq`で一致することを証明する。既存のv4.79直接合成観測則、v4.77の`PlanObservedEq`の合成合同性・結合則・対称性・推移律を順に組み合わせ、命題の弱化やcoverageの全単射性を導入しない。`directCompose_observed_congr`は各入力の観測同値に対する二変数合成の整合性である。

主定理の観測は次を**すべての適切な全域**で含む。

- 最終木の全raw添字`i`について `forwardIndex(left,i) = forwardIndex(right,i)`。
- 開始木の全raw添字`j`について `backwardIndex(left,j) = backwardIndex(right,j)`。
- 最終木の全真正source witness`w`について `Pullback(left,w) = Pullback(right,w)`。

この真正source Type値等式をsubsingleton性で置き換えない。

## 3. GK5CG五セル、経路・認証とobstruction境界

- `directCompose_assoc_rawSquare`は証明済みforward一致に沿って、両括弧付けの**元GK5CG五セル値**のraw四セル端点を揃える。
- `directCompose_assoc_rawLoop`は両側の元五セル値による実loopを構成するが、その自明性／非自明性、五セル等式、新規高次セルの存在は主張しない。
- `directCompose_assoc_path`と`directCompose_assoc_certified`は、両Planのsource pullbackが元Quiver.Pathおよび真正source認証付きP77部分Homを保存することを確認する。
- `directCompose_assoc_certify_raw`は、最後の真正source値で各側を認証したraw比較が、**その同じ側**の選択済みraw比較と一致することを保持する。
- `directCompose_assoc_allCompatible_iff`／`directCompose_assoc_obstructed_iff`は、各合成Planの全階層compatibility／否定が、**同じ最終因子木**`tree F₃ s₃`のcompatibility／obstructionにそれぞれ同値であることを証明する。

終了状態`s₃`は完成状態に限定しない。元の全途中状態間でのobstruction不変、真正五セル値そのものの等式、loopの自明性、元route語の結合律・単位律の構成子的等式、higher coherenceは**未証明**として保持する。

## 4. 新規24宣言の実公理監査

以下は検証済みCIの`#print axioms`に現れた**実出力**を列挙したもの。新しい公理・`sorry`・`admit`は含まない。

| Lean宣言 | 実公理依存 |
|---|---|
| `directNormalUnit` | `propext`、`Quot.sound` |
| `directNormalUnit_route` | `propext`、`Quot.sound` |
| `directNormalUnit_schedule` | `propext`、`Quot.sound` |
| `directNormalUnit_observed` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_leftUnit_observed` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_rightUnit_observed` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_leftUnit_history` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_rightUnit_history` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_observed_congr` | `propext`、`Classical.choice`、`Quot.sound` |
| `directAssocLeft` | `propext`、`Quot.sound` |
| `directAssocRight` | `propext`、`Quot.sound` |
| `directAssocLeft_route` | `propext`、`Quot.sound` |
| `directAssocRight_route` | `propext`、`Quot.sound` |
| `directCompose_assoc_observed` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_forward` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_backward` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_pullback` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_rawSquare` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_rawLoop` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_path` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_certified` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_certify_raw` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_allCompatible_iff` | `propext`、`Classical.choice`、`Quot.sound` |
| `directCompose_assoc_obstructed_iff` | `propext`、`Classical.choice`、`Quot.sound` |

2つの匿名回帰`example`は、任意の部分状態の空履歴に左右単位を適用するもので、真正source witnessのinhabited／subsingletonを仮定しない。匿名exampleは公理監査の宣言数に含めていない。

## 5. CI失敗とLean4 elaboration修正

初回HEAD `1d02aa413e6da3f15f92a8992669b0703b883cab`の[CI #42166344525](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42166344525)は、変更Leanファイル344行・354行の`Function expected`で失敗した。

両方とも、`directCompose_*Unit_history f g h k _ (.nil family s)`と書いた匿名回帰例の余分なplaceholderが原因。実際の定理は履歴`H`が唯一の追加明示引数であり、`_`が`H`を先に消費するため、後続の`(.nil family s)`を**既に成立したProp証明項に関数適用する**形に誤 elaborationした。

修正は2例から余分な`_`を削除しただけ。変更Lean全文384行、依存importsとv4.77–v4.79の正確な定理引数、固定mathlib pin、実Leanエラーログ、公理出力を照合した。新規24定理・定義の文、仮定、結論、五セル履歴、source証拠は不変。初回CIは失敗のまま記録し、修正HEAD `31ee041ad0f94158dc23350bce5e67447bac9f1b`で新しいexact-source CIを実行した。

修正後CIは`10,279／10,279` build success、実公理24／24は標準公理だけ、変更Lean warning/error 0/0、source/test-merge/squash Git tree完全一致。検証済みHEADを指定して定理PR #3183をsquashマージした。

## 6. 次の問題

Qi v4.81候補は、観測結合則・左右単位の有限型付き鎖への反復合成と、異なる括弧付けの経路が同じ全raw添字／source pullbackに到達することの証明である。五セルloopやhigher pentagon coherenceの実証を観測の一致から飛躍して導かない。独立Kuuはpresentation、strict 空中心、元Type値・authority・obstructionの境界を維持する。

旧scheduled MGAP pollerの`state_store_missing`は別系統runtime状態ストア問題であり、このLean定理の検証には混在しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
