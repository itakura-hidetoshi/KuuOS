# GK5BQ／Qi v4.36 — 符号付きStirling同一性と真正整数観測の階乗整除証明書

2026年11月4日 JST ／ F112-P94D3GK5BQ ／ Qi v4.36 ／ 独立定理・北C60統合 **MERGED**

## 1. 正本・exact-source再現性

| 項目 | 独立GK5BQ | Qi v4.36 |
|---|---|---|
| 定理PR | [#3076](https://github.com/itakura-hidetoshi/KuuOS/pull/3076) MERGED | [#3077](https://github.com/itakura-hidetoshi/KuuOS/pull/3077) MERGED |
| 検証済みHEAD | `4ea15719bf4e8c2ef716e6c8d6a8a4b79ffc6e0a` | `a5ffb48a3a4e1419d6bfc1b4ed7f5b258cd0af42` |
| squash SHA | `e02876c5f937414cfd2ed54d944f14ff93d1bded` | `e32a0b8f6a3fd4c5b698a2ce3b512e2ceb590155` |
| Git tree（source / test-merge / squash一致） | `bdb1e44c4e051af997181caa8261de730592e2aa` | `8ba1a1b56a025b14fd297712753019ce5d48e7bb` |
| exact-source CI | [#41765361678](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41765361678) | [#41766217786](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41766217786) |
| Strict Lean | **9,290/9,290 SUCCESS** | **10,217/10,217 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規公理監査 | **10宣言／sorryAxなし** | **11宣言／sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立GK5BQ Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BQSignedStirlingDivisibility.lean)：真正下降階乗係数のStirling同一性、整数観測由来の分子と階乗整除必要十分条件。
- [Qi v4.36 Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BQNorthSignedStirlingV4_36.lean)：元の真正北C60証拠への11定理の接続。
- [公開集約](../../formal/KuuOSFormal.lean)：各新モジュールをappend-onlyでimport。元の定理命題・型付きF55証拠・公開root107は変更しない。

固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft／OPEN／未マージ。

## 2. 独立GK5BQの形式化結果

GK5BPが下降階乗多項式 `descPochhammer Int k` の真正単項式係数として定義した `s(k,j)` を、固定mathlib `Nat.stirlingFirst` に直接接続した。次の同一性を整数多項式の再帰と第一種Stirling数の再帰からLean4で証明。

```text
s(k,j) = (-1)^(k+j) · Nat.stirlingFirst(k,j)     （すべてのk,j）
s(k,j) = (-1)^(k-j) · Nat.stirlingFirst(k,j)     （j≤k）
```

一般の整数観測 `v:Nat→Int` に対し、本物のmathlib前進差分 `Δ^k v(0)` と非負整数 `d!/k!`（`k≤d`）を利用し、有限な**整数分子**

```text
N_(d,j)(v) =
  ∑_(k=0)^d (d!/k!) · Δ^k v(0) · s(k,j)   ∈ ℤ
```

を構成した。この分子は `Nat.stirlingFirst` を用いた符号付き有限和と厳密に等しい。GK5BPの真正Newton多項式 `Q_d(v)` について

```text
(d! : ℚ) · coeff(Q_d(v),j) = (N_(d,j)(v) : ℚ)
```

を証明した。したがって次の有限の**必要十分条件**が成立する。

```text
(∃ P : ℤ[X], P.map(Int→Rat) = Q_d(v))
  ↔ ∀ j ∈ range(d+1), (d! : ℤ) ∣ N_(d,j)(v).
```

この結論はGK5BL真正Lagrange補間にも移送済み。一つでも整除不成立の係数があれば、整数係数持ち上げの不存在が導かれる。**整数観測値だけで整係数性が従うとは主張しない**。例として `Q(X)=X(X-1)/2` は整数値を取るが `1/2` の係数を持つ。

## 3. Qi v4.36：真正北C60統合とType値境界

北C60の真正元F54／F55 Type値証拠 `f` の実際のP92B深さ多項式を観測源とし、上記の整除証明書を得た。真正元F55/P77四セル商 `q` では**既に商へ降下した多項式値**について同様の評価を行い、元P77商類の同一性を主張しない。

真正primitive `P=1`、double inverse＋真正F55右単位 `P=X²` は `{0,1,2}` 上で `2!` 整除、選択真正P92Bループ `A=X³+2`、`B=2X²+X` は `{0,1,2,3}` 上で `3!` 整除を、それぞれ独立Lean4定理として確認した。後者の4点は以前の `{-1,0,1,2}` と区別する。

元original→phi local seamの正負、真正北第五Dart閉路、元P89 source-mapのBadPair**条件付き**反射は係数証明書に吸収しない。係数整除だけから新しい元F55 Type証拠、P77商類一致、P94A四セル、`W=1⇒seam`、全GK5AY seam、GK5BA kit、無条件P89反射、Gray圏復元を推論していない。

## 4. 次段階

**GK5BR（仮称）**：`d!∣N_(d,j)(v)` の整除必要十分条件を、`d!` の素因数・素冪法 `p^e` ごとの有限な局所合同障害に分解する。各局所証明書のcompatibility、有限個の局所条件から全体整除条件への再合成、元観測値が不足する場合の障害を区別する。独立Kuu→Qiと真正Type値source authority境界を維持する。現段階では提案であり、未検証の次定理を成立済みとはしない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
