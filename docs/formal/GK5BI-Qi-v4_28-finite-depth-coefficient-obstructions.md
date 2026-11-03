# F112-P94D3GK5BI／Qi v4.28 — 真正反転深さ係数の非負有限support・P77商降下・北C60障害

**正式証明記録：2026年11月4日 JST。** 唯一のcanonical theorem-bearing branchは [itakura-hidetoshi/KuuOS main](https://github.com/itakura-hidetoshi/KuuOS)。strict 空 authority、**独立Kuu→Qi**、元F54二つのNat添字・二圏・Blocks、元F55 Type値証拠履歴、公開root107を保持する。既存定理の変更はない。

## 1. 独立Kuu GK5BI — 反転深さごとの真正係数

- [独立定理PR #3052](https://github.com/itakura-hidetoshi/KuuOS/pull/3052) **MERGED**。exact-source HEAD `f9fc9ff6afd158306fb9116157a14a352c022520`、独立test-merge `be1ab99d159f9f872d4e5fa3ef5199625586f3ad`、squash `8334dac49490b39c7d2d4655e03a2483d665763b`。source/test-merge/squash Git tree **`59942538302de8ec40aa4d20cd30b609837cbda1` 一致**。
- [exact-source CI #41717206887](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41717206887)：**Strict Lean 9,274 / 9,274・Governance 30 / 30 SUCCESS**。新規17宣言の`#print axioms`で`sorryAx`なし（標準`propext`・`Classical.choice`・`Quot.sound`以内）。新規Leanファイル・公開KuuOSFormalともビルド成功。main push Lean Formal CI #41718004653もSUCCESS。
- [新規Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BIDepthCoefficientDescent.lean)：305行、独立Kuuの追加のみ（元のGK5BG/GK5BHは編集なし）。

GK5BGで形式化済みの真正`P92B`生成多項式 `P_f(X) ∈ ℤ[X]` に対して、各反転深さ `k : ℕ` の係数を **`a_k(f) := coeff(P_f,k) : ℤ`** と定義する。元のP92B証拠を生成する全九構成子の帰納法により、どの端点型・文脈・履歴についても

```text
∀ k, 0 ≤ a_k(f).
∃ S : Finset Nat, ∀ k ∉ S, a_k(f) = 0.
a_0(symm f) = 0;  a_(k+1)(symm f) = a_k(f).
a_k(trans f g) = a_k(f) + a_k(g).
```

をLean4証明。符号付き整数係数を**非負整数**と証明したのであり、任意のsigned polynomialを非負と仮定していない。元original wrapperは1、反転symmは`X`乗算、transは加算、型付きF45/F54文脈は保存される。

さらに、既にGK5BGで真正帰納法により証明された全**P93C 16構成子／P94A 19構成子**の多項式保存から、任意の`k`について`a_k(f)=a_k(g)`を導出。真のP77元四セルはGK5AJによって選択P93Cへ移送されるので、独立の**Int値 `Quotient.lift`** `CoeffOnP77Class(q,k)`を構成した。この値は既存の真正`PolyOnP77Class(q)`の`coeff k`と一致し、P77商上でも非負性と有限supportが成立する。

`∀k, a_k(f)=a_k(g)` と `P_f=P_g` は必要十分であり、P77商上にもこの同値を移した。したがって係数全体は多項式の全情報を保持する。一つの係数`a_k(f)≠a_k(g)`が判明すれば、選択P94A四セル`f⇒g`は存在しない。これは**必要な障害判定**であり、その逆方向の全P94A正規形は主張しない。

## 2. Qi v4.28 — 真正北C60の深さ0係数による識別

- [Qi統合PR #3053](https://github.com/itakura-hidetoshi/KuuOS/pull/3053) **MERGED**。exact-source HEAD `6163078d7cfe7230011cd7c06cf62d04a5ef65d8`、test-merge `4240d16ffa2256d6b40df2b10c28bfb871dfbee9`、squash `aaa04f5ad01fcc7d6adc81a9d520593ae2b43fa0`。source/test-merge/squash Git tree **`98f6af6eef624a6182e88236da16f1dbaf297edd` 一致**。
- [exact-source CI #41718379402](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41718379402)：**Strict Lean 10,201 / 10,201・Governance 30 / 30 SUCCESS**。新規13宣言の`#print axioms`で`sorryAx`なし、Lean warning/error 0/0、標準三公理以内。
- [新規Qi Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BINorthCoefficientDescentV4_28.lean)：272行。独立GK5BIをimportし、既存Kuu証明を上書きしない。

真正北C60の元F54 long→short Homにおけるあらゆるoriginal F55証拠`f`について、選択構造写像`φ(f)`の各係数は非負かつ有限support。全ての真正P77源四セル商類にも同様の結論を導出した。

同一真正F54 Homで、元pentagon source primitiveは `a₀(φ(f))=1`、元double inverseと**真正F55右単位拡張**は `a₀(φ(g))=0`。各値が元P77商へ正しく降下するので、この単一係数だけで両源商類が異なることがLean4で証明された。前者の局所P94A seam存在と後者の不存在は旧定理から引き継いだ別証拠であり、`a₀`値そのものからseamを構成したのではない。

また、真正北C60選択P92Bエンド三証拠の二つの多項式

```text
A(X) = X³ + 2,      a₀(A)=2,
B(X) = 2X² + X,     a₀(B)=0,
N(A)=N(B)=3, S(A)=S(B)=1, W(A)=W(B)=10.
```

をそのまま使い、**一つの係数障害**から両者を結ぶP94A四セル不存在を形式化した。この選択P92B loop対を元F55 original→φ seam反例と混同しない。北C60の真正第五Dart閉路と旧P89 BadPair／source-class-map反射は依然**条件付き同値**に留まる。

## 3. 数学的境界・次の研究

GK5BHの`P_f=1 ↔ W(f)=1`は局所original→φ seamの**必要条件の同値**であり、`W=1 → seam存在`の十分性はない。GK5BI/Qi v4.28は、一般P94A比較における**深さごとの非負・有限な証拠分布**を実装したが、全P94A正規形、全GK5AY seam、GK5BA kit、元P89無条件faithfulness/nonfaithfulness、Gray・hyperdescentは証明していない。

**次GK5BJ（仮称）：** 非負整数係数のNat値実装を元のInt係数と同値化し、有限support上の和から`N=P(1)`・`S=P(-1)`・`W=P(2)`の重み付き和公式と、最大反転深さの構成的上界を検討する。定量的係数証明書とP94A局所障害は保持し、一般seam十分性を先取りしない。

公開root107、保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/OPEN/未マージ、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。append-only、no new axioms/admit/native_decide。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
