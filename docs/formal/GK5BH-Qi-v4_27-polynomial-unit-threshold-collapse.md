# F112-P94D3GK5BH／Qi v4.27 — 多項式の単位閾値とGK5BFの三条件の正確な同値

**正式証明記録：2026年11月4日 JST。** 唯一のcanonical theorem-bearing branch: [itakura-hidetoshi/KuuOS main](https://github.com/itakura-hidetoshi/KuuOS)。strict 空 authority、独立Kuu→Qi、元F54双Nat・二圏・Blocks・元F55 Type値証明履歴、公開root107を維持。

## 1. 独立Kuu GK5BH — P=1 iff W=1

- [定理PR #3049](https://github.com/itakura-hidetoshi/KuuOS/pull/3049) **MERGED**。最終exact-source HEAD `b956f7ee9eb110b8dfecadab0302b13c5ce011f3`、独立test-merge `04059ad30de4dd551791c60effca7fa874671916`、main squash `6cab22f0d78784794e9ede119daf26dffed211e7`。source/test-merge/squash Git tree **`3cfdbd21e3ded251867df896cdfe33d1185d93e6` 一致**。
- [exact-source CI #41699640942（attempt 2）](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41699640942)：**Strict Lean 9,272 / 9,272 SUCCESS、Governance 30 / 30 SUCCESS**。10宣言の`#print axioms`で`sorryAx`なし（既存標準の`propext`・`Classical.choice`・`Quot.sound`のみ）。
- [独立Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BHUnitPolynomialWeightOne.lean)を公開`KuuOSFormal`へappend-only import。初回CIはLakeキャッシュ復元ステップで失敗しLean本体は未実行。GitHub MCPによって失敗ジョブのみ再実行し、attempt 2で実際にLean本体の9,272/9,272を成功させた。証明本文の緩和や新公理による回避は行っていない。

GK5BGで得られた本物のP92B証拠`f`の深さ分布多項式`P_f(X) ∈ ℤ[X]`は、original一個で定数1、選択symmでXを掛け、trans/水平貼り合わせで加法となる。GK5BFの`W(f)∈ℕ`は`P_f(2)`に対応する。原始発生は非負の回数として計数され、符号相殺によって重み1が人工的に生じることはない。

全P92B九構成子への真正依存型帰納法で、`W(f)=0 → P_f(X)=0`と`W(f)=1 → P_f(X)=1`を**同時に証明**。逆向きはGK5BGのMathlib評価`P_f(2)=↑W(f)`から従う。従って任意の元F54依存型端点について

```text
P_f(X)=1  ↔  W(f)=1.
W(f)=1    →  N(f)=1 ∧ S(f)=1.
(N(f)=1 ∧ S(f)=1 ∧ W(f)=1) ↔ W(f)=1.
```

が成立。ここで`N=P(1)`はGK5BBのunsigned count、`S=P(-1)`はGK5BEのsigned grade、`W=P(2)`はGK5BFのinverse-depth weight。

## 2. P77商への実際の降下と十分性の境界

GK5BGの`nativeGK5BGPolyOnP77Class`は、元P77真正四セルで関係付けた元F55 source-classを`Polynomial Int`値に送る実際の`Quotient.lift`。GK5BFの`nativeGK5BFThreeGatesOnP77Class`は同じ真の商上のProp。GK5BHは任意の同型依存F54 source-class`q`について

```text
ThreeGatesOnP77Class(q) ↔ (PolyOnP77Class(q) = 1).
```

を形式化した。

これは**局所seamを検査する必要条件の閾値1**での厳密な一致であり、`W=1`または`P=1`から新しいP94A四セルを生成する十分性は含まない。GK5BGの二つの真正P92B endo-loop証拠は依然、`N=3,S=1,W=10`が一致しても`X³+2 ≠ 2X²+X`なので四セル不存在となる。**任意の選択P94A四セル比較**に関しては、多項式全体が三つの数値評価より識別力を持つ。両例を混同しない。

## 3. Qi v4.27 — 真正北C60への接続

- [Qi v4.27定理PR #3050](https://github.com/itakura-hidetoshi/KuuOS/pull/3050) **MERGED**。exact-source HEAD `f54b4daabc4bbb19bebde572566d92fa309fef82`、test-merge `01b68f41d562f8f66153f06b1b06eab65e841231`、main squash `425430954483c288c14980aa4ffb2661549cdb28`。三者Git tree **`fc325547d6dbd058f314d748a26598c66bb2e1b6` 一致**。
- [exact-source CI #41701233426](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41701233426)：**Strict Lean 10,199 / 10,199 SUCCESS、Governance 30 / 30 SUCCESS**。新規7宣言の`#print axioms`で`sorryAx`なし、依存公理は`propext`・`Classical.choice`・`Quot.sound`以内。
- [Qi Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BHNorthUnitPolynomialGateV4_27.lean)を`KuuOSFormal`へ追加済み。

真正北C60の元F54 long→short Homにおいて、任意の真正元F55証拠`f`について`P_φ(f)=1 ↔ W(φ(f))=1`、任意のP77源四セル商`q`について三条件商述語と多項式定数1商述語の同値を証明。元pentagonとその真正右単位拡張は`W=1`、かつ独立に構成した局所seamが存在。元double-inverseとその右単位拡張は`W=4`、局所seamは不存在。同一F54端点でもP77商類は区別されたまま。

真正北P92B endo-loopの二つの証拠は`W=10`で**閾値1の外**にあり、全多項式の識別力の厳密さを保つ。元P89 BadPair、物理第五around Dart閉路との関係は条件付きのままであり、ポリノミアル評価から物理的四セルを構成したという主張はない。

## 4. 次の研究

**次の独立GK5BI（仮称）**：P92B原始wrapper発生の反転深さ`k`ごとの係数`a_k`を明示的に取り出し、`P_f(X)=∑_k a_k X^k`の証拠関連自然数係数の有限supportとP94A各構成子での係数保存を形式化する。必要な非負性と商降下を真正の元F54依存型で維持し、有限数値評価で失われる情報を定量的に分類する。多項式定数1や`W=1`の十分性を主張しない。

**未証明・非主張：** GK5AY全域seam、GK5BA全構成子kit、元F55 identity seam、元P89無条件faithfulness／nonfaithfulness、全P94A無条件正規化、Type値seam証明書の商上canonical同一視、Gray復元、hyperdescent。固定Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/OPEN/未マージ。append-only、no sorry/admit/native_decide/new axioms。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
