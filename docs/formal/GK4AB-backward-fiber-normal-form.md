# F112-P94D3GK4AB — 真正三成分kernelの逆回転数による局所完全正規形

**2026-10-31 JST** — 唯一の定理正本は `itakura-hidetoshi/KuuOS` canonical `main`。

- 定理[PR #2789](https://github.com/itakura-hidetoshi/KuuOS/pull/2789) **MERGED**
- 最終exact-source HEAD `0972b7c6943fec53c39b8122420f8c277a14772c`
- 定理squash SHA（マージ直後のcanonical main HEADと完全一致）`decd01552f25d5367d775eaaa3ec43609e6ae619`
- [exact-source Strict Lean/Governance #41176694544](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41176694544): **Strict Lean 3741/3741 SUCCESS、Governance 5/5 SUCCESS**、新規Leanファイル1・新規`#print axioms`宣言20、依存公理は`propext`・`Classical.choice`・`Quot.sound`以内、`sorryAx`なし、変更Lean warning/error **0/0**。
- Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

## 権限境界と真正Type値経路

[形式証明Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ABBackwardFiberNormalForm.lean)は、元F54`DepthRotationRoute`の真正Type値経路を保持し、元P92B比較証拠存在商`Q`、独立F54構造比較商`S`、実三成分第二商`K_AA`、旧二成分第二商`K_X`を混同しない。すべての依存型F45 Hom境界、D/E二圏、四Blocks、二つのNat depthを保持。観測値一致から元P92B Type値3-cellを製造しない。

## I. 全依存型Hom上のkernelファイバー分類

任意の真正F45型付き境界`first,last`と、実`K_X`二段kernel商類`q`に対して、

```text
F_q := { z : K_AA(first,last) // ForgetBackward(z) = q }
beta(z) := (GenuineTripleKernelValue(z)).2 : Nat
```

を定義。`nativeGK4ABFiberBackward_injective`は**betaの単射性**を証明する。理由は、`F_q`では旧二成分`(Bool,Int)`が固定されており、第三成分`backwardCount`まで一致すれば三成分観測値全体が等しく、既存の`K_AA→三成分真正到達値`の単射により実`K_AA`類が一致するため。

より強く`nativeGK4ABFixedFiberEquivRange`で

```text
F_q ≃ Set.range beta ⊆ Nat
```

を真正Lean Equivとして構築した。特に**任意の実二段目忘却ファイバーはCountable**であり、元の任意D/E圏の一般Countableや真正14D無条件Countableは仮定しない。`Set.range`は実際に到達した整数だけで、すべてのNatが実現すると仮定しない。

`nativeGK4ABKernelBackward_compose`で真正`K_AA`圏の合成に対するNat加法性と単位0を証明。`S→K_AA`に沿った第三成分もGK4Zの真正`S` backwardCountと一致する。

## II. 真正F54 balanced towerが正の全階層を尽くす

任意の実`rot : KuuNativeF45Tree.LocalRotation p before after`について、GK4Zで元F54`RotationEdge.forward`・`RotationEdge.backward`と実二Nat `castDepths`証拠から構成した自己経路塔`R_k`の真正`K_AA`商類を`T_k`と置く。

```text
O_X(R_k) = (false,-2)         -- 旧K_Xで全段同一
O_AA(R_k) = ((false,-2),k+1) -- 新K_AAで全段異なる
beta(T_k) = k+1
```

`F := ForgetBackward^{-1}([R_0]_{K_X})` は、元二段商における**真の型付きファイバー**。本GK4ABで、任意`z : F`について

```text
beta(z) = 0
   OR
exists k : Nat, z = T_k
```

および

```text
(exists k, z = T_k)  IFF  beta(z) > 0
```

を形式化した。これは無限個の単射例を持つというGK4AAより厳密で、**正の全逆回転数での完全なファイバー正規形**である。

## III. 唯一残るゼロ階層 obstruction の必要十分条件

`nativeGK4ABLocalFiber_zero_unique`により、`beta(z)=0`を満たす実`F`商類は**存在したとしても高々1つ**。

`nativeGK4ABLocalFiber_backward_range`は正確に

```text
range(beta) = {n : Nat | n > 0 OR (n = 0 AND exists z:F, beta(z)=0)}
```

と証明。`nativeGK4ABLocalFiber_tower_surjective_iff`は

```text
Surjective(T : Nat -> F)
  IFF
forall z : F, beta(z) != 0
```

を証明。右辺が成立すれば`nativeGK4ABLocalFiber_tower_bijective_if_no_zero`で**真正元F54 balanced towerの全ファイバー上の全単射**を得る。

**重要：`beta=0`の実類が存在しないことはGK4ABでまだ未証明。** したがってファイバーが本当に`Nat`そのものと同値であるとの無条件主張はしない。可算無限性自体はGK4AAで既に証明済み。真正C60北側六角形についても、本GK4ABの正値正規形の無条件な特殊化を検証した。

## CI・Lean記法修正の構造理由

初回exact-source #41176520603 は、`↔`証明で`Function.Injective`を引数の等式に適用する際の明示的`intro`不足、また関数ラムダで包まれたファイバー射影をベータ展開せず`rw`したことによる3件のLean elaborationエラーで失敗。変更Leanファイル全文・imports・既存GK4AAの関数シグネチャを確認し、`intro h; ... h`、`change`での型付き射影展開を修正。修正版HEADで3741/3741およびGovernance 5/5全SUCCESS。旧Leanファイルは一切変更せず、append-onlyのまま。

## 次段階GK4AC：物理回転の向きと単調rank

`beta=0`でも`O_X=(false,-2)`となる実F54自己経路が存在するかを判定する。候補は、F45の二分木で左枝の葉数を使った自然数のrank`W`を構成し、真正前向きLocalRotationでは`W`が厳密減少、castDepthsでは不変、左右文脈では単調性保存と証明すること。これにより`backwardCount(r)=0`の元F54型付き自己経路で`rotationCount(r)>0`が不可能となれば、ゼロ障害が排除され、`Nat ≃ F`を無条件で得る。ただしこれは**まだ証明されていない研究方針**である。

GK4AA→GK4ABは`K_AA→K_X`忘却の厳密分類。**`S→K_AA`の全域忠実性は依然未証明**で、別の問題として保持。元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentも未証明。strict空中心、独立Kuu一presentation、Gray非再導入、公開root107、保護PR #1558 Draft/OPEN/未マージ、append-only/tighten-only/same-root/overwrite-forbiddenを保持。
