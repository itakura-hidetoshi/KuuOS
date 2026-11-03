# F112-P94D3GK5BK／Qi v4.30 — 真正反転深さ多項式の有限整数観測忠実性

**正式証明記録：2026年11月4日 JST。** 唯一のcanonical theorem-bearing branchは [itakura-hidetoshi/KuuOS main](https://github.com/itakura-hidetoshi/KuuOS)。strict 空、独立Kuu→Qi、元F54二Nat添字・二圏・Blocks・元F55 Type値証拠履歴、公開root107を維持。既存Lean定理ファイルは変更しない。

## 1. 独立GK5BK — 異なるd+1整数評価点での多項式値の一意性

- [独立定理PR #3058](https://github.com/itakura-hidetoshi/KuuOS/pull/3058) **MERGED**。最終exact-source HEAD `b94f1a2ea44da421830fac001b2be719b8f5f446`、test-merge `aabe806c944dcfebeb7a09f0db66e89aafdb938f`、squash `86393f21cba782559c427b7a2a8be1bd0ab9518e`。三者のGit tree **`c2e9888b1a1bd11451f3afe638356c393c8cc16c`一致**。
- [exact-source CI #41724819896](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41724819896)：**Strict Lean 9,278/9,278、Governance 30/30 SUCCESS**。新規15宣言の`#print axioms`に`sorryAx`なし、標準`propext`・`Classical.choice`・`Quot.sound`以内。新規ファイル・公開`KuuOSFormal`双方ビルド成功。
- [独立Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BKFiniteSampleRigidity.lean)：342行。真正P92B証拠と真正元P77四セル商の`Polynomial Int`値を対象とする。

固定mathlib `Polynomial.eq_of_natDegree_lt_card_of_eval_eq'`（指定mathlib SHAの`Mathlib/Algebra/Polynomial/Roots.lean`）を、元のF54依存型に沿って利用。任意の二つの真正P92B三証拠`f,g`の多項式`P_f,P_g∈ℤ[X]`、次数上界`d`、異なる整数点の集合`S:Finset Int`について

```text
natDegree(P_f) ≤ d,   natDegree(P_g) ≤ d,   card(S) = d+1,
(∀ z ∈ S, P_f.eval z = P_g.eval z) → P_f=P_g.
```

を形式化した。さらに`{0,1,…,d}`という**具体的な整数格子のFinset.image**を構成し、Nat→Int単射性から`card=d+1`をLeanで証明。各真正GK5BI Int係数とGK5BJ Nat係数が復元され、次数境界の下で「有限評価の一致⇔Nat係数全体の一致」を証明した。一つのNat係数でも異なれば、**任意のd+1個の異なる整数点**に必ず評価値の相違が存在する。

元F55の真正P77源四セル商上でも、独立GK5BGの`Polynomial Int`値の降下とGK5BJ Nat係数の降下を使い、同様の有限評価・全係数同値を証明した。**これは商上の多項式値の一致であって、元P77商類そのものの一致も、型付きP94A四セルの存在も導かない**。P94A四セルは全整数評価を保存するが、その逆は主張しない。

**CIの修正履歴：** 初回[CI #41724182111](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41724182111)では`Function.Injective (fun k:Nat => (k:Int))`のラムダ適用の形式が`exact_mod_cast`に認識されず、Lean elaborationで失敗した。変更Leanファイル全文と固定mathlib補題を確認し、`change (i:Int) = (j:Int) at h`を加えて明示的にβ簡約してからキャストを証明した。数学的命題・仮定・既存証明に変更なし。上記最終CIで成功。

## 2. Qi v4.30 — 真正北C60での有限整数観測の識別力

- [Qi統合PR #3059](https://github.com/itakura-hidetoshi/KuuOS/pull/3059) **MERGED**。exact-source HEAD `5cb7fb7713322ee736125206d5127f1cd2aa075e`、test-merge `55cae9567140c8234ccf7ff524a732cd60275a6d`、squash `22b47d04303a60c14cf09487ede4702302bf0d74`。三者Git tree **`07e94497fb846a9c9dbab0d73d1290cd612e4a98`一致**。
- [exact-source CI #41725853171](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41725853171)：**Strict Lean 10,205/10,205、Governance 30/30 SUCCESS**。新規12宣言公理監査に`sorryAx`なし、Lean warning/error 0/0。
- [Qi Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BKNorthFiniteSampleRigidityV4_30.lean)：303行。独立GK5BKをimportし、Kuu定理ソースは変更しない。

真正北C60の元F54 long→short Homにある任意の元F55証拠の構造像と、同じF54 Homにある元P77源四セル商の**多項式値**に、GK5BK有限整数観測定理を適用した。

具体例1：北pentagon元primitiveの選択構造像の多項式は`P=1`、真正元double-inverseとF55右単位拡張は`P=X²`。双方`natDegree≤2`で、**任意の3個の異なる整数評価点**で必ず少なくとも一つの値が異なる。特に点0では`1`対`0`。元P77商類の相違は別途、以前のGK5BI/J真正商係数から証明済み。

具体例2：同じ真正北C60の**選択P92B endomorphism loop対**には

```text
A(X)=X³+2,   B(X)=2X²+X.
A(-1)=B(-1)=1,   A(1)=B(1)=3,   A(2)=B(2)=10.
A(0)=2 ≠ 0=B(0).
```

が成立する。双方`natDegree≤3`なので、**任意の4個の異なる整数評価点**で識別できることをLean4で証明し、旧`(-1,1,2)`の三点が盲点となる一方、`{-1,0,1,2}`という4点で障害を観測できることを形式化した。このloop対は元original→φ seam反例ではなく、P94A四セルを新しく構成する主張もない。

## 3. 変更しない権限境界と次の研究

元P89 BadPair/source-mapの反射は既存の**条件付き同値**に留まる。真正北C60第五Dart物理閉路と証拠型付きP94A比較を同一視しない。GK5BHの`W=1`条件は局所seamの必要条件であり十分性を証明しない。GK5AY全域seam、GK5BA kit、P94A全域正規形、元P89無条件faithfulness/nonfaithfulness、Gray・hyperdescentは未証明。

**次GK5BL（仮称）：** GK5BKの有限観測**一意性**を踏まえ、異なる整数サイトの評価値から`ℚ[X]`上のLagrange/Vandermonde補間を構成し、元の整数・非負Nat係数へ戻るための必要な整合条件を形式化する。補間多項式の存在／一意性と、整数値係数性・真正元F55 Type証拠の実現可能性は分けて扱う。

公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/open/unmerged、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。append-only、no new axioms/sorry/admit/native_decide。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
