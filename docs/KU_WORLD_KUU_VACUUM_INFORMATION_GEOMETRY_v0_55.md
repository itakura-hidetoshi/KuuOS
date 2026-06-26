# WORLD v0.55 Kū vacuum information geometry

## 目的

WORLD v0.55は、v0.54で導入した中心真空状態を、既存の非可換情報幾何の基準点として固定する。

完成Hilbert空間上の真空ベクトルを Ω_Kū とする。

中心基準状態を次で表す。

```text
ω_Kū(a) = ⟨Ω_Kū, π(a) Ω_Kū⟩
```

各情報幾何パッチ i に真空基準パラメータ θ_Kū(i) を置く。

このパラメータはWORLDそのものではない。

これは状態比較のために選ばれた局所座標上の原点である。

## 中心経路

```text
completed Hilbert vacuum Ω_Kū
→ central vacuum state ω_Kū
→ vacuum parameter origin θ_Kū
→ Araki relative-entropy Hessian
→ BKM / quantum Fisher metric
→ Hilbert excitation Gram form
→ coarse tangent
→ Petz-recovered tangent
→ orthogonal information-loss decomposition
```

## 真空発散

パラメータ θ から真空基準点への情報発散を次で定義する。

```text
D_Kū(i, θ) = D_Bregman(i, θ, θ_Kū(i))
```

既存の量子Bregman発散と情報幾何発散の一致から、次が成り立つ。

```text
0 ≤ D_Kū(i, θ)
D_Kū(i, θ) = 0 ↔ θ = θ_Kū(i)
```

零発散は、同一の情報幾何チャート内で基準パラメータに一致したことだけを意味する。

零発散からWORLDの存在論的同一性を導かない。

## Araki相対エントロピー

真空基準Araki相対エントロピーを、真空基準量子Bregman発散へ束縛する。

```text
S_Araki(θ || θ_Kū) = D_Kū(i, θ)
```

この有限bridgeでは、非負性と零点分離をLeanが直接導く。

実際の無限次元von Neumann代数上での二階微分可能性とHessian同定は、明示的な解析receiptとして保持する。

## 励起方向と量子Fisher計量

接ベクトル u を接観測量 A_u へ移し、完成Hilbert空間上の励起方向を次で定義する。

```text
Ψ_u = π(A_u) Ω_Kū
```

実内積Gram形式を、真空基準点における量子Fisher計量へ束縛する。

```text
Re ⟨Ψ_u, Ψ_v⟩ = g_QF,θ_Kū(u, v)
```

v0.44のAraki Hessian同定により、同じ量は次にも一致する。

```text
g_QF,θ_Kū(u, v)
= Hess_θ_Kū S_Araki(u, v)
```

したがって、Hilbert空間上の励起方向と状態多様体上の接方向が、同じ二次形式によって比較される。

## Petz回復と情報損失

粗視化接写像を C とし、Petz接回復写像を R_P とする。

回復接ベクトルを次で置く。

```text
u_rec = R_P C u
```

残差情報損失を次で定義する。

```text
L_Kū(i, u)
= g_QF,θ_Kū(u - u_rec, u - u_rec)
```

既存のPetz直交射影構造から、次を得る。

```text
0 ≤ L_Kū(i, u)
L_Kū(i, u) = 0 ↔ u is Petz-recoverable
```

さらに量子Fisher計量は、回復成分と残差成分へPythagoras分解される。

```text
g_QF,θ_Kū(u, u)
= L_Kū(i, u) + g_QF,θ_Kū(u_rec, u_rec)
```

接観測量に戻すと、回復接ベクトルは作用素レベルのPetz回復チャネルと一致する。

## 双対アファイン座標

自然座標と期待値座標は、真空基準点で零になるよう中心化する。

```text
η(θ_Kū) = 0
μ(θ_Kū) = 0
```

指数射影と混合射影は、真空基準点を固定する。

この固定性は、真空が制御目標であることを意味しない。

これは選択された基準点が情報射影によって移動しないことを表す。

## ゲージ共変性

真空基準パラメータは、パッチ間輸送に対して共変である。

```text
transport(i, j, θ_Kū(i)) = θ_Kū(j)
```

このため、局所チャートが変わっても中心基準状態の役割は保たれる。

## 固定境界

```text
vacuum parameter != exact WORLD
vacuum origin != absolute truth
vacuum origin != control objective
zero divergence != ontological identity
quantum Fisher metric != ontology
Petz recovery != execution authority
excitation direction != WORLD creation
modular time != physical time
information geometry remains read-only
```

## 証明範囲

Leanは有限bridge上の型付き等式、非負性、零点分離、Petz回復可能性、Pythagoras分解、射影固定性、境界receiptを検証する。

実際のAraki相対エントロピーの二階微分、標準形接空間の完全同定、励起チャートの稠密性、無限次元状態多様体、物理的実現は解析receiptとして残る。
