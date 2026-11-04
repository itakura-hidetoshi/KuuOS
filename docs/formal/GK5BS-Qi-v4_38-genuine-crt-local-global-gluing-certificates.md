# GK5BS／Qi v4.38 — 真正CRT局所・大域再合成と北C60の構造的seam分離

2026年11月4日 JST ／ F112-P94D3GK5BS ／ Qi v4.38 ／ 独立定理・真正北C60統合 **MERGED**

## 1. 正本・exact-source検証

| 項目 | 独立GK5BS | Qi v4.38 |
|---|---|---|
| PR | [#3082](https://github.com/itakura-hidetoshi/KuuOS/pull/3082) MERGED | [#3083](https://github.com/itakura-hidetoshi/KuuOS/pull/3083) MERGED |
| 最終exact-source HEAD | `6445154df559174ff4658a092f0b9bfc69544afb` | `fb2dcd30fc038caaec7528d83fab616cc87e0676` |
| squash SHA | `e4feab9e2d0ac2f2c5229be966eba570cf9ff816` | `274653fd542b38cc2e9d9e6fdcc62cb1cf3d78bb` |
| source/test-merge/squash Git tree | `2ce511ec443f48fe43849491b2396882af01f08e` | `c2c55f9735e059407de26e84edd2bf1c77ce052b` |
| exact-source CI | [#41778920532](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41778920532) | [#41779618580](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41779618580) |
| Strict Lean | **9,294/9,294 SUCCESS** | **10,221/10,221 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規定理の公理監査 | **16定理・sorryAxなし** | **16定理・sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立GK5BS Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BSCRTLocalGlobalGluing.lean)：真正CRT環同型、任意局所代表の整数再合成・一意性、加法乗法、元整数分子のCRT零判定。
- [Qi v4.38 Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BSNorthCRTGluingV4_38.lean)：真正元F55・P77多項式値、北primitive／double inverse・二P92Bループへの型付き移送、局所seam正負の同時証明。
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)：既存定理の命題を変更せず、独立・Qi新規importのみ追記。公開root **107維持**。

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は Draft／OPEN／未マージ。

## 2. 独立GK5BS：真のCRT環同型と構成的整数代表

固定mathlib `Mathlib.Data.ZMod.QuotientRing` の実際の定義 `ZMod.equivPi` を用い、任意の `d:Nat` について次を**環同型**として構成した。

```text
ZMod(d!) ≃+* Π (p : (d!).primeFactors), ZMod(p^((d!).factorization p)).
```

`d=0,1` で `d!=1`、素因数集合が空の場合も型付きの同じ構成の適用範囲。異なる素数冪は相互素なので、この有限族の剰余類は**任意に、独立して**指定可能である。

`residues : Π p, ZMod(p^v_p(d!))` に対して、具体的な `CRTGlue d residues : ZMod(d!)`、整数代表 `CRTGlueInt`、正規化された自然数代表 `CRTGlueNat<d!` を構成し、各成分の厳密な再現と次の必要十分条件を証明した。

```text
(∀p, (z : ZMod(p^v_p(d!))) = residues(p))
  ↔ (d! : Int) ∣ (z - CRTGlueInt(d, residues)).
```

したがって全局所条件を満たす整数代表は**法d!で一意**。さらに、CRTの逆像は環同型であるため、局所代表の加法と乗法を忠実に保つ。ここでの再合成は純粋に算術的な局所・大域descentであって、型付き構造の同一性は含まない。

## 3. 元GK5BQ整数分子との同一性

任意の真正整数観測列 `v:Nat→Int`、整数前進差分と符号付きStirling係数からGK5BQが構成した同じ整数分子を使う。

```text
N_(d,j)(v)=Σ_(k=0)^d (d!/k!)·Δ^k v(0)·s(k,j) ∈ Int
```

各素数冪での**同じNの剰余値**を独立CRTの入力として組み合わせると、結果が `N mod d!` と厳密に一致することをLean4で証明した。したがって

```text
CRTGlue(d, observedLocalNumerator(d,j,v)) = 0
  ↔ (d! : Int) ∣ N_(d,j)(v).
```

元GK5BP Newton補間、ならびに元GK5BL真正Lagrange補間が整数係数 `Int[X]` 原像を持つことと、すべての係数 `j≤d` に対する**CRT glue=0** が必要十分。整数係数原像が存在しない場合は、少なくとも一つの `j` で真正CRT合同類が非零であることを証明した。任意の整数値標本を整数係数と取り違えず、零・負の整数分子も対象とする。

初回独立CIはLean4予約語 `local` のbinder使用、固定mathlib `ZMod.equivPi` の明示法引数、型同義語の `abbrev`、およびZMod型注釈の閉じ括弧の記法エラーを修復。既存Lean定理の命題・条件を弱めず、最終exact-sourceで16定理が全て `sorryAx` なしと検証された。

## 4. Qi v4.38：真正北C60への適用とauthority境界

真正F54二Nat／二圏／Blocks、元F55 Type値証拠の履歴を保持。元F55証拠 `f` は既存のP92B構造画像 `gk5bgDepthPolynomial : Int[X]` の**値**を与えるだけであり、一般CRTから新しい元F55証拠を作らない。元F55/P77商類でも既存の**降下多項式値のみ**にCRT零証明書を移送し、元Type商類の同一性を結論しない。

- 真正primitive `P=1` と、別の真正double inverse＋F55右単位 `P=X²` は、元`{0,1,2}`、`d=2` の全係数についてCRT glue=0。
- 真正選択P92Bの二つの独立endo-loop `P=X³+2`、`Q=2X²+X` は元`{0,1,2,3}`、`d=3` の全係数について独立にCRT glue=0。
- **定理 `fivefoldGK5BSNorthBothCRTZeroButOppositeSeams`：** 実際のprimitiveとdouble inverseは**双方とも算術的CRT gluingが成立**する一方、元original→phi局所seamは前者で存在し、後者では存在しない。よって算術的gluingは構造的seam成立の十分条件ではない。
- 真正北第五Dart物理C60 gaugeと元P89 BadPairに関する**条件付き**反射は、算術的CRTとは独立に従前の定理から継承。

したがって、新しい元F55 Type源、P77商類一致、P94A四セル、GK5AY全域seam、`W=1→seam`、P89無条件反射、GK5BA kit、Gray圏復元は結論しない。strict 空／独立Kuu→Qiは別authorityを保持する。

## 5. 次の形式化境界

**GK5BT（仮称）**：今回の相互素な真正素数冪CRTから、**非互いに素な法**（重なった局所被覆）の剰余代表へ進む。二つの法 `m,n` に対する共通部分 `gcd(m,n)` 上のcompatibilityを、`a ≡ b (mod gcd(m,n))` という具体的obstructionとして示し、条件付きで法 `lcm(m,n)` へ再合成する。元F55 Type値／P94A四セル／P89反射／GK5AY seamの構造的gluingを引き続き別課題とする。**GK5BTは次研究構想であり、まだ成立済みではない。**

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
