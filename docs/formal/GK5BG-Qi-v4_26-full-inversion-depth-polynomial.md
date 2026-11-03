# F112-P94D3GK5BG／Qi v4.26 — 反転深さ生成多項式とP94A四セル障害

**2026年11月3日 JST、正式証明記録。** Repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)。唯一のtheorem-bearing canonical branchは `main`。strict 空 authority、独立Kuu→Qi、元F54双Nat・二圏・Blocks、元F55 Type-valued証明項と公開root107を保持する。

## 1. 独立Kuu GK5BG — 多項式全体の保存と真正P77値降下

- [独立定理PR #3046](https://github.com/itakura-hidetoshi/KuuOS/pull/3046) **MERGED**。
- 最終exact-source HEAD `e0c56fa7aa15bdf45fde386a30e7b2ef90bb00d2`、CI test-merge `d811982df1f64c8ffaded953ad31616b4f8da7bd`、main squash `95311d1dd48ca4f74ab1daf53d81baf1c47a2ad2`。三者のGit treeは **`5287de584b97c7fc36cdbcd1147d5d0adabb0af5`** で一致。
- [exact-source Strict Lean／Governance #41636095545](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41636095545)：**9,270 / 9,270 SUCCESS、Governance 30 / 30 SUCCESS**。新規`#print axioms`25宣言、`sorryAx`なし。公理依存はLean既存の`propext`・`Classical.choice`・`Quot.sound`以内。変更Leanエラー／警告なし。
- [独立GK5BG Lean正本](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BGDepthGeneratingPolynomial.lean)を公開`KuuOSFormal`へappend-only import済み。

元F55原始`original`の選択P92B`symm`入れ子深さ分布を、Mathlibの**`Polynomial Int`そのもの**として定義する：

```text
P(original(f))         = 1
P(refl(r))             = 0
P(assocNaturality(...))= 0
P(symm(u))             = P(u) * X
P(trans(u,v))          = P(u) + P(v)
P(horizontal(u,v))     = P(u) + P(v)
P(F45/F54 context(u))  = P(u)
```

真正P93C全16構成子および選択P94A全19構成子のType値四セルについて **`P(u)=P(v)`** を帰納的に証明した。これには旧P89のoriginal両端、水平・縦貼合、interchange、P94A追加horizontalUnit／leftContextUnit／rightContextUnitが含まれる。

既存の別々の整数／自然数不変量は、**Mathlib Polynomial.evalによる正確な特殊化**として次の全称定理で一致する（自然数は必要箇所で整数へcast）：

```text
P_f(1)  = N_f  (GK5BB unsigned original-wrapper count)
P_f(-1) = S_f  (GK5BE signed original-wrapper grade)
P_f(2)  = W_f  (GK5BF inversion-depth weight)
```

既存GK5AJの真正元P77→選択P93C四セル移送と新しい多項式保存則を結び、**P(phi(f))が実際のP77元F55四セル商上へ `Polynomial Int`値としてQuotient.liftされる**ことを証明。単なるProp（存在性）や三数値shadowだけの降下ではない。

元の局所直接seam `P94A(original(f),phi(f))` が実在すれば、`P(phi(f))=1` が必要となる。この**多項式必要条件の十分性は証明していない**。

## 2. 同一北C60 Homにおける局所seam正負の多項式分離

真正北C60のpentagon原始F55証拠`p`と、元F55二重反転`c:=symm(symm(p))`は、同一の元F54 long→short Homに属する。

```text
P(phi(p)) = 1
P(phi(c)) = X^2
P(original(c)) = 1
N(phi(c)) = S(phi(c)) = 1
W(phi(c)) = 4
```

`p`の直接局所seamは`P94A.refl`で実在するが、`c`の直接seamは多項式保存則に反するため**不存在**。さらに同じHom内の元P77商クラスで、二つの`Polynomial Int`値が異なると証明している。旧`N=S=1`という弱い必要条件の十分性を否定したGK5BFを、値全体の比較に強化した。

## 3. 三数値評価がすべて同じでも異なるP92B証拠

元F55の真正identity wrapperを使い、**同じF54 endomorphism route上の二つの実際の選択P92B Type-valued 3証拠**`A,B`を構成した。それらの生成多項式は

```text
P_A(X) = X^3 + 2
P_B(X) = 2 X^2 + X
```

であり、**同時に**

```text
P_A(1) = P_B(1) = 3
P_A(-1) = P_B(-1) = 1
P_A(2) = P_B(2) = 10
P_A(0) = 2  !=  P_B(0) = 0
```

が成立。よって`N,S,W`三数値観測が一致しても多項式全体が異なり、P94Aの全19構成子保存則から**`¬ Nonempty(P94A(A,B))`**をLean4で証明した。これらはあくまでも**選択P92Bエンドループ**であって元F55`original→phi`局所seamの反例と取り違えない。

## 4. Qi v4.26 — 真正北C60の型付き適用

- [Qi v4.26 PR #3047](https://github.com/itakura-hidetoshi/KuuOS/pull/3047) **MERGED**。
- 最終exact-source HEAD `b1e0c9933121e48c45ff6f0adfc3bad50044962e`、test-merge `9a1f1f04f1a749d77005280c8a422f95a2fc9625`、main squash `f2c7dd7064b801fb5954c0c4b2026b7362c903dc`。三者のGit treeは **`ad2be874c3f4b16059f6c1edb91ce5ff4855be8a`** で一致。
- [exact-source Strict Lean／Governance #41637182427](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41637182427)：**10,197 / 10,197 SUCCESS、Governance 30 / 30 SUCCESS**。新規`#print axioms`12宣言、`sorryAx`なし。変更Leanエラー／警告なし。
- [Qi v4.26 Lean正本](../../formal/KUOS/Architecture/QiWuxingGK5BGNorthPolynomialSeamV4_26.lean)を公開`KuuOSFormal`へ追加済み。

独立GK5BGの多項式降下を用い、北C60元pentagonの局所正クラスには定数1、元二重反転＋真正右identityの局所負クラスには`X^2`が対応することを、実際の元P77四セルを通じて証明した。さらに北pentagon短F54経路上の同一端点P92Bループ`A,B`について三数値が一致・多項式が不一致・P94A四セルが不存在という定理を追加。

真正北C60物理五行gaugeの第五around Dart閉路と元P89反射BadPairの**条件付きiff**は独立のまま。選択構文の多項式を物理的な五行量と同一視しない。

## 5. 数学的な境界と次の研究

**証明成立：** P92B生成多項式、P93C全16／P94A全19構成子での保存、N/S/W三特殊値との完全一致、P77商への多項式値降下、同一北C60 Hom正負の区別、三数値一致でもP94A比較不可能な型付き証拠。

**非主張：** `P(phi(f))=1`の一般的十分性、全P94A正規化、元P89無条件faithfulness／nonfaithfulness、GK5AY全域seam、GK5BA constructor kit、内部source-image障害の解消、Type値seam証明書のcanonical同一視、Gray復元、高次hyperdescentの完成。

**次の研究 F112-P94D3GK5BH（仮称）：** 多項式の係数`a_k`を完全な非負の反転深さ分布として形式化し、任意評価点での保存と次数・係数に関する定量的なobstructionを導く。さらに元F55構文クラスにおける`P(phi(f))=1`を満たす領域と真のseam存在領域の差を検討する。今までの厳密なauthority境界を緩めない。

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。append-only／overwrite-forbidden、no Gray/sorry/admit/native_decide/new axioms。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
