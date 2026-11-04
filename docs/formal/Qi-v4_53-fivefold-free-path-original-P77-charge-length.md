# Qi v4.53 — 真正五角形の任意有限経路と元F55/P77証拠のチャージ＝長さ定理

**2026-11-05 JST**

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3126](https://github.com/itakura-hidetoshi/KuuOS/pull/3126) **MERGED** |
| 定理exact-source HEAD | `3d9aa1922e666088817a5292b72df89539f19a58` |
| 定理squash SHA | `08650aff27deed6b86eb4a76ad278571568763cd` |
| exact-source CI | [#41935914077](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41935914077) |
| Strict Lean | **10,250 / 10,250 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **14 / 14標準公理のみ、sorryAx0** |
| 新規Leanソース | [QiWuxingGK5CHFivefoldFreePathOriginalP77V4_53.lean](../../formal/KUOS/Architecture/QiWuxingGK5CHFivefoldFreePathOriginalP77V4_53.lean) |
| 既存変更 | `KuuOSFormal` に import 1行のみ。他のLean正本変更なし |

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/open/unmerged。

## 1. 真正5辺の独立自由経路圏

Qi v4.52の唯一の`FivefoldIndex = FivePhase = ZMod 5`と`FivefoldEdge={e01,e12,e23,e04,e43}`を再利用。既存Qi v3.1はFivePhase上に相生・相剋の別のQuiverを定義しているため、そのインスタンスを上書きせず、`FivefoldPathVertex`という位相を保持する別の**wrapper**に、端点等式を含む`FivefoldPathArrow`を構成。

標準Mathlibの`FivefoldFreePathCategory := Paths FivefoldPathVertex`は真正自由経路圏。上三辺`e01≫e12≫e23`と下二辺`e04≫e43`は、同じ`0→3`にあるが長さ3・2で非等号と形式証明。既存Qi v3.5/GK5Xの全whole NatIso pentagonには変更しない。

## 2. 全有限経路を元P77四セルの真正Type値付き証拠へ評価

任意の元F54の2カテゴリー、2つのNat深さ、Blocks、元F55合成可能四項組`f,g,h,k`に対し、`fivefoldArrowOriginalP77`は各矢印を旧Qi v4.52の真正`NativeF55RawVerticalFourCell`へ写す。特に逆向きの`e04/e43`で既存元証拠の`symm`を保持する。

`fivefoldEvaluateP77`は`Quiver.Path.rec`による**元P77四セルの実際の証拠構文値**への全有限長評価。空経路を`P77.refl`、末尾辺追加を`P77.trans`として、元F55証拠の型付き始終端を維持する。元P77四セルの生構文自体をstrictなCategoryと偽っておらず、商や数値shadowへ替えない。

## 3. 新規中心定理

```text
∀ typed finite path w,
  assocCharge(fivefoldEvaluateP77 f g h k w) = (w.length : ℤ)
```

この定理を元P77の真正`assoc`・`symm`・`trans`・左右whiskeringの固定されたチャージ再帰から証明。結果として、
- **評価後の元P77四セル証拠の等号 ⇒ 元経路の長さの等号**。`fivefoldEvaluateP77_eq_implies_length`。
- 長さが同一端点経路を識別するという明示条件`LengthInjective`があれば、P77評価も単射。`fivefoldEvaluateP77_injective_of_length`。**この条件そのものの一般的な無条件成立を主張していない。**
- 二つの実五角形経路は元P77評価後も3対2の異なる整数チャージと異なるType証拠値を持つ。`fivefoldFreeTwoEvaluations_charge`、`fivefoldFreeTwoEvaluations_ne`。
- GK5CGの保守的五セルは整数チャージを保存するため、評価後の両経路間に**保守的5-cellは存在しない**。`fivefoldFreeTwoEvaluations_noConservativeFiveCell`。

## 4. 同じ自由経路のC60物理辺トレース

`fivefoldFreePhysicalTrace frame v path`は、元の真正C60五角形`(.pentagon v)`・任意局所ゲージ`frame`で、各生成辺が選ぶ**本物の`Edge.around`**を保存するListへ任意有限経路を写す。空経路は空列、`cons`では実辺1本追加。元物理ダートの接続正当性はQi v4.52の`fivefoldPhysicalEdge_joins`から継承。

```text
(fivefoldFreePhysicalTrace frame v path).length = path.length
```

とLeanで証明。元P77四セル評価のchargeと物理実辺数は同じ原自由経路に関して数値的に一致するが、P77四セルや物理Edgeを**等しいTypeとはしない**。

## 5. Lean4修正履歴と検証範囲

初回CI [#41935315502](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41935315502)では、固定mathlib`Quiver.Path.rec`の`cons`stepは`(path,edge,IH)`の3明示引数だが、当初誤って4引数として実装したため型不一致。後続`rfl`・`rw`エラーもこの根本原因の伝播。固定mathlib `Mathlib/Combinatorics/Quiver/Path.lean`・`Mathlib/CategoryTheory/PathCategory/Basic.lean`、既存GK5CF/CG、Qi v4.52ソース全文を照合し、stepの3引数化、完全指定の`NativeF55RawVerticalFourCell.trans`、証明チャージの`change`による関数適用正規化で修正。仮定・結論を一切弱めず、外部公理・`sorry`なし。最終CI [#41935914077](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41935914077)は10,250 / 10,250成功、14監査すべて標準公理の範囲。

数学的な限界：現段階の`fivefoldEvaluateP77`は**元P77生構文へのproof-valued path evaluator**であり、元P77を無条件strict圏とする関手ではない。新しく定義した`FivefoldFreePathCategory`自体は正真正銘のMathlib自由圏。保守的5-cellによる商を明示した真正target Category／faithful functorの無条件成立や、元P94Aでの5-cell、数値CRTからの元証拠復元、Gray全体・無制限高次descentを主張しない。

次研究：GK5CG保守的5-cellによる元P77四証拠の商をstrict target Categoryとして定義し、全有限経路の評価をその商へ実際にfunctorialに降下させる。その上でfaithfulnessの必要十分条件と、チャージが検出できない追加のobstructionを追う。元の`FivefoldIndex`・`FivefoldEdge`・original F54/F55・Qi v4.51 signed CRTを保全。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
