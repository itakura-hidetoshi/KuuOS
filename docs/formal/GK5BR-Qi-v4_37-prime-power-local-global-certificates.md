# GK5BR／Qi v4.37 — 素数冪局所・大域階乗整除と真正北C60のseam独立性

2026年11月4日 JST ／ F112-P94D3GK5BR ／ Qi v4.37 ／ 定理・Qi統合の両PR **MERGED**

## 1. 唯一の正本とexact-source検証

| 項目 | 独立GK5BR | Qi v4.37 |
|---|---|---|
| 定理PR | [#3079](https://github.com/itakura-hidetoshi/KuuOS/pull/3079) MERGED | [#3080](https://github.com/itakura-hidetoshi/KuuOS/pull/3080) MERGED |
| 検証済みHEAD | `ef1d28dbe9e226c1104ddeb5c8047d551559ce69` | `1282db0df613ce2d74dda1cd41047c4ba8f763f1` |
| squash SHA | `46857444d52483d0f17f6ae39a5d619bc5a418d7` | `7c1a58256039f607d842e0aec324d46c48de310f` |
| source / test-merge / squash tree | `c316626b1dfa2a38c58cc191d97836c0bb54fc65` | `9425248dcf20862473a73cb35108749ca7492a23` |
| exact-source CI | [#41773693409](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41773693409) | [#41774281250](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41774281250) |
| Strict Lean | **9,292/9,292 SUCCESS** | **10,219/10,219 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規公理監査 | **12定理／sorryAxなし** | **13定理／sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立Kuu Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BRPrimePowerLocalGlobal.lean)：真正GK5BQ整数分子の有限局所・大域同値、整数合同、障害の必要十分な局所証拠。
- [Qi v4.37 Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BRNorthPrimePowerV4_37.lean)：真正北F55/P77、多項式値と元seam正負を接続。
- [公開集約 KuuOSFormal](../../formal/KuuOSFormal.lean)：既存公開定理を改変せず両importを追加。公開root **107維持**。

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は Draft／OPEN／未マージ。

## 2. 独立GK5BRの数学的成果

GK5BQが真正の整数観測 `v : Nat → Int`、実際のmathlib前進差分 `Δ^k v(0)`、固定mathlibの符号付き第一種Stirling係数から構成した**同じ整数分子**

```text
N_(d,j)(v) = ∑_(k=0)^d (d!/k!) · Δ^k v(0) · s(k,j) ∈ ℤ
```

を一切変更しない。素数 `p`、固定mathlib `Nat.factorization (d!) p` で `e_p = v_p(d!)` とする。分子が負または0でも成立する、完全な有限局所・大域同値を形式化した。

```text
(d! : Int) ∣ N_(d,j)(v)
  ↔ ∀ p ∈ (d!).primeFactors,
        ((p ^ e_p : Nat) : Int) ∣ N_(d,j)(v)
  ↔ ∀ p ∈ (d!).primeFactors,
        N_(d,j)(v) % (p ^ e_p : Int) = 0
```

従って真正Newton補間 `Q_d(v)` に対して、全係数に関する**必要十分な局所から大域への持ち上げ**を得た。

```text
(∃ P : Int[X], P.map(Int→Rat) = Q_d(v))
  ↔ ∀ j ∈ range(d+1), ∀ p ∈ (d!).primeFactors,
        N_(d,j)(v) ≡ 0 (mod p ^ e_p)
```

真正GK5BL Lagrange補間にも同じ同値。整数係数持ち上げが存在しないことと、**ある有限の係数index jおよび素因数pにおいて局所整除が失敗する**ことの必要十分性を構成した。素数冪の異なる提示は全て同じ実整数分子を検査するため、算術的compatibilityは明示的に保たれる。局所定理は型付きF55 source復元ではない。

初回独立CIでは固定Leanの非推奨 `push_neg` を `push Not` に置換し、正規化後の `A ↔ A` を `rfl` で閉じた。定理命題・仮定を弱めず、12定理の公理依存を `propext`／`Classical.choice`／`Quot.sound` のみとして検証した。

## 3. Qi v4.37 — 真正北C60への型付き接続

元の真正F54二Nat・二圏・BlocksとF55 Type値履歴を維持し、真正元F55証拠 `f` から**既にある**P92B構造画像の `gk5bgDepthPolynomial : Int[X]` を観測源として有限局所証明書を得た。真正F55/P77元商 `q` では**既に降下した整数多項式の値のみ**を利用し、P77 Type商類の同一性は結論しない。

- 真正北primitive `P=1` と真正double inverse＋F55右単位 `P=X²` は、それぞれの真のsource履歴を維持したまま `d=2`、観測 `{0,1,2}`、`2!=2` の局所素数冪証明書を満たす。
- 二つの真正選択P92B endo-loop `P=X³+2`、`Q=2X²+X` は、`d=3`、`{0,1,2,3}`、`3!=6` の独立な局所証明書を満たす。
- **重要な分離定理 `fivefoldGK5BRNorthBothLocalButOppositeSeams`：** primitiveとdouble inverseの双方はそれぞれの素数冪局所条件を全て満たすが、元original→phi seamの存在判定はそれぞれ正・負。よって算術的整係数性だけでは元F55 Type値の構造的seamは生じない。

真正北第五Dart物理C60 gauge、および元P89 BadPairに関する**条件付き**反射の既存定理は算術的再合成とは独立に保持する。特に新規F55 Type source、P77商類一致、P94A四セル、全GK5AY seam、`W=1⇒seam`、無条件P89反射、GK5BA kit、Gray圏は導出しない。

## 4. 次の研究境界

**GK5BS（仮称）**：同じ整数分子の整除判定を越え、素数冪剰余類について**別々に与えられた局所representative**がある場合のcompatibilityと明示的CRT（中国剰余定理）再合成を、固定mathlibで型付き構成する。得られた数値的CRT gluingと元F55 source証拠・P94A四セル／seamの構造的gluingを引き続き分離する。これは次段階の構想であって、現時点でCRT統合定理を成立済みとは主張しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
