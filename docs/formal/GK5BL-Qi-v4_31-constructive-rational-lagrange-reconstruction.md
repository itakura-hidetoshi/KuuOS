# F112-P94D3GK5BL／Qi v4.31 — 真正整数観測からの有理Lagrange構成的復元

**正式証明記録：2026年11月4日 JST。** 唯一のcanonical theorem-bearing branch: [itakura-hidetoshi/KuuOS main](https://github.com/itakura-hidetoshi/KuuOS)。strict 空 authority、独立Kuu→Qi、元F54の二Nat添字・二圏・Blocks、元F55 Type値証拠履歴、公開root107、保護PR #1558を維持する。既存Lean定理を上書きしない。

## 1. 独立Kuu GK5BL — 一意性から構成的補間へ

- [独立定理PR #3061](https://github.com/itakura-hidetoshi/KuuOS/pull/3061) **MERGED**。最終exact-source HEAD `aa2f64748cf919359464673b2f50dc884a0a38b0`、test-merge `626440810ed816e7b0913cdec4dd9c1a4b746fc3`、squash `48ea559ce749637f42150e92acfe3fdd704e9ed4`。三者Git tree **`a9d6befadf4b62cf5049d0d34857b8583ca989ee` 一致**。
- [exact-source CI #41728908990](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41728908990)：**Strict Lean 9,280/9,280・Governance 30/30 SUCCESS**。新規18宣言の`#print axioms`で`sorryAx`なし。依存公理は標準の`propext`・`Classical.choice`・`Quot.sound`以内。変更Leanファイルwarning/error 0/0。
- [独立Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BLLagrangeInterpolation.lean)：323行。公開`KuuOSFormal`にappend-only import。

GK5BKは、次数上界`d`の下で異なる整数サイト`d+1`個の評価の一致から`Int[X]`多項式の**一意性**を証明した。GK5BLは固定mathlibの真正[`Mathlib.LinearAlgebra.Lagrange`](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/LinearAlgebra/Lagrange.lean)を使い、`S:Finset Int`と値関数`y:Int→Rat`から、具体的な`Rat[X]`補間多項式を構成した。

```text
I_S,y(X) = ∑ i∈S, y(i) · ∏ j∈S, j≠i, (X-j)/(i-j).
degree(I_S,y) < card(S).
∀ i∈S, I_S,y(i)=y(i).
```

Int→Ratサイト写像は単射なので、Lagrange節点が重複しないことも証明した。任意の`P:Polynomial Int`が`natDegree(P)≤d`かつ`card(S)=d+1`を満たす場合、**真の整数評価を有理数へ写したデータ**の補間は

```text
I_S,(z ↦ (P.eval z : Rat)) = P.map (Int.castRingHom Rat).
coeff(I_S, k) = (P.coeff k : Rat),  ∀ k:Nat.
```

となる。観測値が`S`上で`P.eval`と一致すれば、サイト外での値は不要である。真正P92B三証拠`f`の場合、補間係数は**元のGK5BJ非負Nat値反転深さ係数`b_k(f)`をRatに埋め込んだ値**に厳密に一致し、非負性を証明した。

独立の元F55/P77 source four-cell quotientについても、GK5BGの真正降下多項式`PolyOnP77Class(q)`のRatへの係数埋め込みを同じく構成的に復元し、その係数はGK5BJのNat値`Quotient.lift`と一致する。

**真正証拠の権限境界：** 任意の有理データから補間多項式の存在は成立するが、整数係数性は一般には成立しない。ある係数がIntのRat埋め込みの像にないなら`Polynomial Int`の原像は存在しないことを証明した。整数係数・非負性が成立しても、元F55 Type値証拠の実現、元P77商類の一致、選択P94A四セルの存在は導かない。

**初回CI修正履歴：** [CI #41728354275](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41728354275)で`(P.eval z : Rat)`がInt結果のキャストではなくRat多項式の評価式として解釈され、型エラーとなった。これを`((P.eval z : Int) : Rat)`へ統一。また`Lagrange.interpolate_eq_sum`へ値関数を明示的に渡した。修正は新規Leanファイル内だけで、定理の仮定・結論を変更せず上記最終CIに成功した。

## 2. Qi v4.31 — 真正北C60の構成的復元と三点の盲点

- [Qi統合PR #3062](https://github.com/itakura-hidetoshi/KuuOS/pull/3062) **MERGED**。最終exact-source HEAD `0cdccb1aa2678b6c07349feda6d463e77c367c4d`、test-merge `2ea877996586aba0d0b42266a72515c1d7cf4fd6`、squash `909542a3a31a596c808403a08c780834f40856ba`。三者Git tree **`96a91934a296a4ab0d06ff72b8cc5bc8fb76c1f6` 一致**。
- [exact-source CI #41730985676](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41730985676)：**Strict Lean 10,207/10,207・Governance 30/30 SUCCESS**。新規11宣言の公理監査に`sorryAx`なし、warning/error 0/0。
- [Qi Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BLNorthLagrangeReconstructionV4_31.lean)：299行。独立GK5BLをimportし、独立Kuu定理は変更しない。

真正北C60の元F54 long→short Homにおける全元F55証拠について、選択構造像`φ(f)`の整数観測から、元の`Polynomial Int`のRat埋め込みと各非負Nat深さ係数を構成的に復元した。元P77 source four-cell商でも同じ結論を**降下した多項式値**について証明し、source商類・raw Type値証明項とは区別した。

**次数2の真正元証拠：** 元pentagon primitiveの`P=1`と元double-inverse＋真正F55右単位の`P=X²`は、固定整数格子`{0,1,2}`の3点からそれぞれ構成的に復元できた。双方のP77源商類は異なり、その証拠は従来のNat係数降下と区別して保持。

**次数3の選択P92B loop盲点：** 同じ真正北C60の二つの選択P92B endomorphism loopは

```text
A(X)=X³+2,    B(X)=2X²+X.
A(-1)=B(-1)=1; A(1)=B(1)=3; A(2)=B(2)=10.
A(0)=2 ≠ 0=B(0).
```

を満たす。GK5BLは、**旧三サイト`{-1,1,2}`から作った二つの有理Lagrange補間多項式が本当に一致する**ことを証明した。これは三サイトでは次数3の両方を復元できないという具体例である。一方、`{-1,0,1,2}`の四サイトからは互いに異なる補間多項式を構成し、両方の元の次数3多項式のRat埋め込みを正確に復元した。この二つのloop証拠は元original→φ局所seam反例ではない。

**Qi CI修正履歴：** [初回 #41729859456](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41729859456)では`congrArg`で得た多項式評価の関数適用がβ簡約されず、`rw`失敗。明示的`change`で正規化した。[次 #41730374355](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41730374355)では点0の型付きキャストのrewriteパターンが一致しなかった。最終的に補間節点の二つの評価等式を推移律で合成して修正した。数学的主張や既存証明を弱めず、最終CIは成功。

## 3. 残るobstructionと次の研究

整数値観測からの`Rat[X]`構成と、その係数が真の整数・非負Nat値へ降下する条件、さらに元のF55 Type値証拠を実現する問題を区別する。GK5BHの`W=1`は局所seamの必要条件に留まり十分性は証明しない。P94A全19構成子の不変量保存から四セル存在を逆向きに推定しない。元P89 BadPair反射は条件付き、真正北C60第五Dart物理閉路との証拠層を混同しない。GK5AY全域seam、GK5BA kit、Gray/hyperdescentは未証明。

**次GK5BM（仮称）：** 有理補間で構成した各係数の整数性判定（分母消去／格子上有限差分の整除条件）と、その上の非負Nat証拠との一致を条件付きで研究する。真正P92B証拠へ戻る際のobstructionとP77商への降下を明確に区別する。

公開root107、保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/open/unmerged、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、append-only、no new axioms/sorry/admit/native_decide。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
