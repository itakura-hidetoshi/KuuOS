# F112-P94D3GK5BM／Qi v4.32 — 有理補間係数の整係数・非負Nat係数の必要十分条件

**正式証明記録：2026年11月4日 JST。** 唯一のcanonical theorem-bearing branchは[ itakura-hidetoshi/KuuOS main ](https://github.com/itakura-hidetoshi/KuuOS)。strict 空 authority、独立Kuu→Qi、元F54二Nat／二圏／Blocksと元F55 Type値証拠履歴、公開root107を維持。append-only。

## 1. 独立GK5BM：有理多項式の係数持ち上げの必要十分条件

- [独立GK5BM PR #3064](https://github.com/itakura-hidetoshi/KuuOS/pull/3064) **MERGED**。最終exact-source HEAD `951f25bf3162743d6b8ecab8bd66fdb6ae93147e`、test-merge `ec7cf6cb3d125d712c5ae4b4f8ab1fac216e6306`、squash `3ed73fdbc9236bb24b73ebd5df08b9f216a04f59`。source/test-merge/squash Git tree **`d340d7ebeecad7c6657167b9bb80b938057b4885`一致**。
- [exact-source CI #41739642619](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41739642619)：**Strict Lean 9,282/9,282、Governance 30/30 SUCCESS**。新規11宣言の`#print axioms`で`sorryAx`なし。新規ファイル・公開集約ビルド成功、Lean warning/error 0/0。
- [独立Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BMIntegralNatLiftCertificates.lean)：248行、既存定理は変更なし。

GK5BLは異なる整数節点上の観測値から有理多項式`Q∈ℚ[X]`を構成したが、任意の整数値観測から整数係数性は自動的には従わない。GK5BMでは任意の`Q: Polynomial Rat`について、係数ごとに元の整数またはNatを与える条件を完全に区別した。

```text
(∃ P:ℤ[X], P.map(Int→Rat)=Q) ↔ ∀ k, ∃ z:ℤ, (z:Rat)=Q.coeff k.
(∃ P:ℕ[X], P.map(Nat→Rat)=Q) ↔ ∀ k, ∃ b:ℕ, (b:Rat)=Q.coeff k.
(∀ k, ∃ b:ℕ, (b:Rat)=Q.coeff k)
  ↔ ∀ k, (∃ z:ℤ, (z:Rat)=Q.coeff k) ∧ 0≤Q.coeff k.
```

**十分性は構成的**で、全係数の指定原像`c(k)`から有限supportを使い`P=∑_{k∈support(Q)}monomial(k,c(k))`を実際に構成し、`P.map=Q`を証明した。任意のLagrange補間についてもこの必要十分条件が成立する。負の有理係数や整数像にない係数が存在すれば、非負Nat係数多項式の持ち上げは不可能。

真正型付きP92B証拠`f`では、GK5BJの非負Nat発生回数`b_k(f)`とGK5BLの構成的補間定理から、真の整数観測を補間した`Rat[X]`に**Nat[X]多項式持ち上げの存在**を証明した。元F55/P77真正四セル商の降下した多項式値についても同様に構成した。ただし**Nat[X]多項式が存在することから、別の元F55 Type値証拠・P94A四セル・元P77商類の等しさを導かない**。

## 2. Qi v4.32：真正北C60への統合

- [Qi v4.32 PR #3065](https://github.com/itakura-hidetoshi/KuuOS/pull/3065) **MERGED**。exact-source HEAD `798b45f36998cd05bb4074c00e2bd2884bb3ad40`、test-merge `292a173c29e5e0fdb876a8bce9040414f0429a0b`、squash `4c0b318e275e5f7fed282ecc3be3d8bfacffc6c6`。三者tree **`80930d7c9e54d447d89529ad34285d8e6455162c`一致**。
- [exact-source CI #41740543233](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41740543233)：**Strict Lean 10,209/10,209、Governance 30/30 SUCCESS**。新規9宣言`#print axioms`で`sorryAx`なし、Lean warning/error 0/0。
- [Qi Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BMNorthIntegralNatLiftV4_32.lean)：219行、独立GK5BMをimportし既存定理を変更しない。

真正北C60の元F54 long→short Homに属する**あらゆる元F55証拠**について、選択構造像`φ(f)`の整数観測から補間した多項式が非負Nat係数の持ち上げを持つことを形式化。元P77 source四セル商に対しても、**商へ降下した多項式値**にNat係数持ち上げの存在を証明した。一般の有理観測データに対する必要十分条件も保持する。

具体的な真正北pentagon primitive`P=1`と元double inverse＋真正右F55単位`P=X²`は三点`{0,1,2}`でNat係数持ち上げを持つ。選択P92B endomorphism loop対`A=X³+2`・`B=2X²+X`は四点`{-1,0,1,2}`からそれぞれ持ち上がる。一方、`-X∈ℚ[X]`は深さ1の負係数を持ち**Nat係数へ持ち上がらない**という任意有理データの障害例もLeanで確認。選択endo-loopはoriginal→phi local seamの反例と混同しない。

## 3. 数学的な権限境界と次段階

整係数・非負Nat係数多項式の存在は、**元のF54/F55 Type値証明項の実現可能性**を意味しない。元P77商の値と商類そのものを同一視しない。P94A保存不変量の一致からP94A四セルは生成しない。GK5BH`W=1`は局所seamの必要条件のみであり十分性は未証明。旧P89 BadPair反射は条件付き、真正北C60第五Dart物理閉路と分離した。全GK5AY seam、GK5BA kit、Gray、hyperdescentは未証明。

**次GK5BN（仮称）：** 上記係数持ち上げの一意性・Nat係数の有限supportと、補間データの離散有限差分／整除証明書を結び、検証可能な整数性条件をより計算的に記述する。有限の整数値観測のみから整係数性を無条件に主張せず、元のType値実現可能性を独立obstructionとして維持する。

公開root107、保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/open/unmerged、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。既存定理上書き禁止、no sorry/admit/native_decide/new axioms。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
