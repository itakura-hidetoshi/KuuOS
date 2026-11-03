# F112-P94D3GK5BJ／Qi v4.29 — Nat反転深さ係数の有限和と真正北C60のP77商証拠

**正式証明記録：2026年11月4日 JST。** 唯一のcanonical theorem-bearing branchは [itakura-hidetoshi/KuuOS main](https://github.com/itakura-hidetoshi/KuuOS)。strict 空、独立Kuu→Qi、元F54の二Nat添字・二圏・Blocks、元F55のType値証拠履歴、公開root107を維持する。文書はappend-only、過去定理に変更なし。

## 1. 独立GK5BJ — 非負整数から自然数値への真正変換

- [独立定理PR #3055](https://github.com/itakura-hidetoshi/KuuOS/pull/3055) **MERGED**。検証済みsource HEAD `aa2fd1c39c5889cc63894f4451d8b9d349dc8244`、test-merge `1532583edd3d4cf61a0db588fa2a97d90dcde5d7`、squash `869132e16a87821dbe82be1072b3e1801e99afb1`。source／test-merge／squash Git tree **`7b904ed7daf8d354f9b528e0e505b29129c96e05`一致**。
- [exact-source CI #41720830977](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41720830977)：**Strict Lean 9,276/9,276・Governance 30/30 SUCCESS**。新規20宣言の`#print axioms`で`sorryAx`なし。標準`propext`・`Classical.choice`・`Quot.sound`のみ。
- [独立Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BJNatDepthWeightedSums.lean)：354行、公開`KuuOSFormal`へのappend-only import。元GK5BIは変更しない。

GK5BIの全P92B真正証拠`f`に対する深さ`k`の整数係数`a_k(f):Int`について、すでに証明済みの`0≤a_k(f)`を使用し、**`b_k(f):Nat := Int.toNat (a_k(f))`** を導入した。すべての`k`について`(b_k(f):Int)=a_k(f)`が証明され、元の型付き証拠は維持される。反転と貼り合わせは

```text
b_0(symm f)=0,
b_(k+1)(symm f)=b_k(f),
b_k(trans f g)=b_k(f)+b_k(g).
```

を満たす。有限supportと、`natDegree(P_f)<k → b_k(f)=0`という**計算可能な深さ上界**を証明した。任意の`x:Int`に対する固定mathlib `Polynomial.eval_eq_sum`から、

```text
P_f(x) = ∑ k∈support(P_f), (b_k(f):Int) * x^k.
N(f)   = ∑ k∈support(P_f), b_k(f).
S(f)   = ∑ k∈support(P_f), (b_k(f):Int) * (-1)^k.
W(f)   = ∑ k∈support(P_f), b_k(f) * 2^k.
```

をLean4で形式化した。特に`N, W`は**Nat値の有限和**、`S`はInt値の交代和である。全係数は**真正P93C全16構成子／P94A全19構成子**の四セルで保存される。元のP77四セルについては、**Nat値の独立`Quotient.lift`** を構成し、既存のInt値降下のキャストとの一致、`natDegree`上界、商上の有限評価公式、**全Nat係数一致と全Polynomial Int一致との同値**を証明した。元F55のraw Type項を同一視したわけではない。

## 2. Qi v4.29 — 真正北C60の長→短F54 Homへ統合

- [Qi統合PR #3056](https://github.com/itakura-hidetoshi/KuuOS/pull/3056) **MERGED**。検証済みsource HEAD `00388111749990232d3b5cfe6b0b6895422a5fda`、test-merge `a63d0b58d94633e11b021724249832db191787ce`、squash `ae5c0f5dea2613f52c3f1074fbec5a35a9612ce1`。source／test-merge／squash tree **`a6924070fdd573592a133b69d77ff255d293cf35`一致**。
- [exact-source CI #41721667098](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41721667098)：**Strict Lean 10,203/10,203・Governance 30/30 SUCCESS**。新規15宣言の`#print axioms`で`sorryAx`なし、Leanファイルwarning/error 0/0、標準三公理のみ。
- [Qi v4.29 Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BJNorthNatDepthGradesV4_29.lean)：300行。独立GK5BJをimportし、Kuuの証明を上書きしない。

真正北C60の元F54 long→short Homにおいて、**任意の元F55証拠`f`** の選択構造像`φ(f)`に対し、N/S/Wの有限Nat係数和と`natDegree`上界が成立する。同じ元F54 Homの真正P77 sourceクラスについては、Nat値係数の商降下、Int値係数との整合、有限和による全多項式評価、Nat係数全体の同値判定を証明した。

北pentagon元primitiveは`b₀(φ(f))=1`、真正元double-inverse＋F55右単位は`b₀(φ(g))=0`なので、**一つのNat係数で元P77商類を厳密に識別**できる。別の二つの真正北P92B選択endo-loop証拠`A(X)=X³+2`・`B(X)=2X²+X`は、旧`N=3,S=1,W=10`が一致するにもかかわらず`b₀(A)=2`・`b₀(B)=0`となる。GK5BJのP94A係数保存から**選択P94A四セル不存在**が成立する。このloop対はoriginal→φ局所seamではなく、すべてのseam十分性の主張とは区別する。

## 3. 未証明の境界と次の研究

GK5BHの`P_f=1 ↔ W(f)=1`は依然、局所original→φ seamの**必要条件の同値**であり、`W=1→seam`の十分性は証明していない。今回のNat係数と有限和はP94A四セルの**保存不変量**だが、係数一致から四セルを構成する完全性はない。元P89 BadPair反射は条件付き、真正北第五Dart物理閉路とは証拠層を混同しない。GK5AY全域seam、GK5BA kit、全P94A正規形、元P89無条件faithfulness/nonfaithfulness、Gray、hyperdescentは未証明。

**次GK5BK（仮称）：** 有限な深さ上界`d=natDegree(P_f)`に制限した`d+1`個の整数評価点からの係数族の一意復元（有限評価の忠実性）を検討する。型付きP92B証拠・P77商を保持し、評価の一致からP94A四セルの存在を飛躍させない。

公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/open/unmerged、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、append-only、no new axioms/admit/native_decide。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
