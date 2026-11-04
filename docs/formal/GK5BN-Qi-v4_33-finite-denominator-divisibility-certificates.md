# GK5BN／Qi v4.33 — 有限分母・整除証明書の正式Lean4証明記録

2026年11月4日 JST ／ F112-P94D3GK5BN ／ Qi v4.33 ／ **独立定理・Qi統合ともにMERGED**

## 1. 正本・検証・再現性

| 項目 | 独立GK5BN | Qi v4.33 |
|---|---|---|
| 定理PR | [#3067](https://github.com/itakura-hidetoshi/KuuOS/pull/3067) MERGED | [#3068](https://github.com/itakura-hidetoshi/KuuOS/pull/3068) MERGED |
| exact-source HEAD | `0cf5569b83e334b526da54d3b99bc6f8fbe379d6` | `f53afb41f4d8343a9f674c6636592cf74b862eee` |
| test-merge commit | `4358456ab20acfc5c66fa6f8453d7e35c69bab66` | `dd7af6720ac1f42c80f75d7178c1edb2d521dbbd` |
| squash SHA | `764b6365d00ea07519dde44e145fa9d5cf453622` | `8e42f6d44041b78d7bef6b2014c634693fcad91a` |
| source/test-merge/squash Git tree | `a7dc5e1570fb61f9d23930e6bdb20ceddbe004ef` | `b2c2eb6ada0e7b12e0c583e015e934b4edb57d32` |
| exact-source CI | [#41743613851](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41743613851) | [#41744468276](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41744468276) |
| Strict Lean | **9,284/9,284 SUCCESS** | **10,211/10,211 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 公理監査 | 新規11宣言、sorryAxなし | 新規10宣言、sorryAxなし |
| 変更Lean warning/error | 0/0 | 0/0 |

ソース：
- [独立GK5BN Lean4](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BNFiniteDivisibilityCertificates.lean) — 251行・11宣言
- [Qi v4.33 Lean4](../../formal/KUOS/Architecture/QiWuxingGK5BNNorthFiniteDivisibilityV4_33.lean) — 229行・10宣言
- [公開集約](../../formal/KuuOSFormal.lean) — 各新規モジュールへのappend-only import

主張を追加しただけで、元のF54／F55／P77／P94A定理の命題を変更していない。固定Lean `v4.30.0-rc2`・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107維持。保護PR #1558はDraft／OPEN／未マージ。

## 2. 独立GK5BN：有限supportへの整数係数判定の降下

元GK5BMの「全Nat係数が整数のRat像」という必要十分条件を、有理多項式の有限supportで検査できる形に強めた。

任意の `Q : Polynomial Rat` について、

```text
(∃ P : Int[X], P.map(Int.castRingHom Rat) = Q)
  ↔ ∀ k ∈ Q.support, (Q.coeff k).den = 1
```

すなわち、補間された多項式の非零係数だけを調べれば、全多項式の整係数性が決定する。係数が非整数の一つの点も検出すれば、`Int[X]` 持ち上げは不可能。GK5BLによる任意有限整数節点の真正 `Rat[X]` Lagrange補間にも同値性を適用した。

実際の整数多項式 `N : Int[X]` と **非零整数** `d` の証拠として

```text
Polynomial.C (d : Rat) * Q = N.map (Int.castRingHom Rat)
```

が与えられた場合は、

```text
(∃ P : Int[X], P.map(Int.castRingHom Rat) = Q)
  ↔ ∀ k ∈ N.support, d ∣ N.coeff k
```

が成り立つ。十分性はGK5BMの有限supportモノミアル和による真正多項式の構成へ接続される。整除失敗一件で不可能性証明書を得る。**分母消去等式を未検証の観測だけから仮定してはいない**。

特に、`X(X−1)/2` はどの整数点でも整数値を取りうるが、`X²` の係数は `1/2` なので `Int[X]` 係数ではない。したがって「整数値の標本 ⇒ 整係数」は成り立たない。数値観測と有理補間係数の実現可能性を区別する。

## 3. Qi v4.33：真正北C60への統合

真正北F54 long→shortの**元のType値F55証拠** `f` を入力として、GK5BJの真正Nat深さ係数とGK5BMのNat持ち上げを介し、GK5BL補間多項式の有限supportで分母がすべて1であることを証明した。真正元F55/P77四セル商 `q` にも適用したが、結論は元商から**降下した多項式値**についてのみであり、商類そのものの一致ではない。

元北primitive `P=1`、元二重反転＋真正F55右単位 `P=X²` は `{0,1,2}` の三サイト、選択P92B endo-loop `A=X³+2` と `B=2X²+X` は `{-1,0,1,2}` の四サイトで、それぞれ分母1の有限証明書を持つ。一般の有理観測データには有限分母判定、分母を払った整数分子の整除判定、失敗時のobstructionの必要十分条件を残した。

真正北C60物理第五Dart閉路とP89原source mapのBadPair条件付き反射は、係数証明書に置き換えない。元F55 Type値証明・P77証拠履歴と降下多項式は同一視せず、W=1⇒局所seam、全GK5AY seam、GK5BA kit、P94A正規形、無条件P89反射、Gray圏復元は証明・主張しない。

## 4. Lean4 elaboration修正履歴と次段階

独立GK5BN初回CI #41743084050は、`Int.castRingHom` を残した式から `Int` に `exact_mod_cast` する箇所の型正規化で失敗した。**Leanファイル全文・依存GK5BM・固定mathlib API**を照合し、`Int.coe_castRingHom` を明示してcast式を正規化した後に `exact_mod_cast` することで修復した。命題・仮定は変更せず、修正後11宣言の公理依存は `propext`・`Classical.choice`・`Quot.sound` のみ。Qi v4.33では初回からStrict Lean・Governance成功した。

次 **GK5BO（仮称）** は、前進有限差分・Newton補間基底・階乗整除／Stirling変換を用いて、有限観測からの検査条件を係数の整除証明書へ接続する。整数値性だけを整係数性と誤認せず、元F55 Type値の実現可能性は独立のobstructionとして残す。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
