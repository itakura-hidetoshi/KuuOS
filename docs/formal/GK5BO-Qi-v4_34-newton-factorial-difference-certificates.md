# GK5BO／Qi v4.34 — Gregory–Newton有限差分・階乗証明書の正式Lean4証明記録

2026年11月4日 JST ／ 独立F112-P94D3GK5BO ／ Qi v4.34 ／ **定理・統合ともにMERGED**

## 1. Canonical source／CI／Git tree

| 検証項目 | 独立GK5BO | Qi v4.34 |
|---|---|---|
| PR | [#3070](https://github.com/itakura-hidetoshi/KuuOS/pull/3070) **MERGED** | [#3071](https://github.com/itakura-hidetoshi/KuuOS/pull/3071) **MERGED** |
| exact-source HEAD | `4101468e4b1592d3087155321108c96f024578db` | `4d3ce8b4bce70a13ba5bd04a4f19c274af975b0b` |
| test-merge | `139e385c1580910e1e6edc912e03d04bd4ef87f1` | `93930a93a321e4d0764026aaf160a54c5c589437` |
| squash SHA | `5920a4d423c2baf466cb789be206614dde413c0a` | `a1b339082906ca8dd6ce478fb73f610275cce236` |
| source / test-merge / squash tree | `3b2fd899cad623c414ddd0c2509b6a7c505ffaf7` | `12bd1d27401df53d6fb44d7df0975f2f53b930a5` |
| exact-source CI | [#41747472161](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41747472161) | [#41748169015](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41748169015) |
| Strict Lean | **9,286 / 9,286 SUCCESS** | **10,213 / 10,213 SUCCESS** |
| Governance | **30 / 30 SUCCESS** | **30 / 30 SUCCESS** |
| 新規公理監査 | **12宣言／sorryAxなし** | **9宣言／sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立GK5BO Lean4](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BOForwardDifferenceFactorial.lean)：新規266行、定義2件と監査付き12定理。
- [Qi v4.34 Lean4](../../formal/KUOS/Architecture/QiWuxingGK5BONorthFactorialDifferenceV4_34.lean)：新規230行、監査付き9定理。
- [公開集約](../../formal/KuuOSFormal.lean)：いずれも新しいimport一行のみappend。元のLean定理とF54／F55 Type値履歴に変更なし。

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107保持。保護PR #1558はDraft／OPEN／未マージ。

## 2. 独立GK5BO：数学的定理と権限境界

固定mathlib `Mathlib.Algebra.Group.ForwardDiff` の**真正** `fwdDiff` 演算子／Gregory–Newton公式を活用した。任意の有理多項式 `Q:Polynomial Rat` と自然数 `k` について、有限切断

```text
Q_{≤k} := ∑ j ∈ Finset.range (k+1), Polynomial.monomial j (Q.coeff j)
```

を定義し、すべての`j≤k`で元係数保存、`natDegree(Q_{≤k})≤k`をLean4で証明。固定mathlibの最高次差分定理と低次数消滅定理を両方用いて、`Q.coeff k=0` の場合も含む次の全次数恒等式を得た。

```text
Δ^k (Q_{≤k})(0) = (k! : Rat) * Q.coeff k
```

さらに、実際の有理多項式全体のGregory–Newton整数格子公式 `Q(n)=∑_{k=0}^n choose(n,k)·Δ^k Q(0)`、有限切断の`k`回差分を節点`0,…,k`で計算する符号付き二項和を形式化。

**有限support必要十分条件**：

```text
(∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q)
  ↔ ∀ k ∈ Q.support, ∃ z : Int,
       (k.factorial : Rat) * (z : Rat) = Δ^k(Q_{≤k})(0).
```

右辺の整数`z`は実際の数学的係数証拠であり、GK5BMの有限support多項式構成から左辺の存在を復元する。一係数の階乗差分障害は、Int[X]持ち上げ不存在を保証する。**切断しない整数値観測だけでは整係数性を保証しない**：例として `X(X−1)/2` は整数点で整数値だが、単項式基底の`X²`係数は`1/2`である。この例は数学的説明であり、今回の新規Lean命題に独立の反例宣言を追加したものではない。

## 3. Qi v4.34：真正北C60と元Type値履歴

真の元F54 long→short のF55三証拠 `f`、および元F55/P77四セル商 `q`に対して、GK5BJ非負Nat深さ係数・GK5BM Nat持ち上げの既存実証から、補間した **多項式値** の階乗有限差分条件を導いた。P77商類の一致、F55の新しいType値証拠、P94A四セル、元original→phi局所seamの逆像は構成・主張しない。

真正北C60の元primitive `P=1`、元double inverse＋元F55右単位 `P=X²` は整数三サイト `{0,1,2}`、選択真正P92B endo-loop `A=X³+2`・`B=2X²+X` は四サイト `{-1,0,1,2}` からの補間に対して、それぞれ有限階乗差分証明書を取得。一般有理観測の完全同値性・一係数障害も移送。

真正北C60第五Dart物理閉路、元P89 source-map BadPair条件付き反射、原始正／二重反転負の既存局所seam結果を別のType付き定理として保持。`W=1⇒seam`、全GK5AY seam、GK5BA kit、P94A全正規形、Gray圏復元、無条件P89反射は証明・主張していない。

## 4. CI修正履歴と次の開始基点

独立GK5BO初回CI #41747123403は、有限cutoffの次数上界証明で`j ≠ i`と`i = j`の不一致によりLeanの簡約が残った。**新規Lean全文・依存元・固定mathlibの`Polynomial.coeff_monomial`**を確認し、不等号を`i ≠ j`に正規化して修正した。定理・数学的仮定は変更していない。修正後Lean 9,286/9,286、Qi v4.34初回Lean 10,213/10,213ともにSUCCESS。新規公理依存は`propext`、`Classical.choice`、`Quot.sound`に限定され、`sorryAx`なし。

**次GK5BP（仮称）**：整数観測列から直接`Δ^k f(0)`を計算し、Newton基底から通常の単項式基底への符号付きStirling係数変換／階乗整除を明示し、切断多項式係数を先に知らない場合の判定へ進める。型付きF55の実現可能性は係数値とは独立に維持。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
