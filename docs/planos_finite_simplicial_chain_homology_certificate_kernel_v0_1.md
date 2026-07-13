# PlanOS Finite Simplicial Chain Complex and Homology Certificate Kernel v0.1

## 位置づけ

PlanOS v1.14は、有限normal-ball coverから有限nerve、Čech 2-simplex、edge-valid path、elementary triangle homotopy moveを構成した。

PlanOS v1.15は、その有限simplicial dataを整数係数chain complexへ写し、境界作用素、cycle、boundary、有限有理Betti数、有限first-homology obstructionを再計算する。

本層が扱うのは、明示された有限複体だけである。

空間全体のhomology、古典的Čech homologyとの同値、torsion、persistent homology、planning-space全体の位相不変量は主張しない。

## 有限simplicial basis

頂点、edge、triangleの自由整数加群を、

```text
C_0 = Z<V>
C_1 = Z<E>
C_2 = Z<T>
```

として保持する。

各edgeは頂点IDを辞書順に正規化し、`[u,v]`、`u < v`を正向きとする。各triangleも`[a,b,c]`、`a < b < c`へ正規化する。

## 境界作用素

正向きedgeについて、

```text
∂₁[u,v] = [v] - [u]
```

正向きtriangleについて、

```text
∂₂[a,b,c] = [b,c] - [a,c] + [a,b]
```

とする。

runtimeは、頂点×edge行列 `boundary_one_matrix` と、edge×triangle行列 `boundary_two_matrix` を独立に再構成し、

```text
boundary_one_matrix * boundary_two_matrix = 0
```

をexact integer arithmeticで検証する。

## CycleとBoundary

保持された1-chainを、

```text
z = sum_e n_e e
```

とする。cycle条件は`∂₁z = 0`である。

exact cycleには明示的2-chain `c` を結合し、

```text
z = ∂₂c
```

を整数ベクトルとして照合する。

## 有限有理rankとBetti数

境界行列rankは `fractions.Fraction` を用いたexact Gaussian eliminationにより、`Q` 上で計算する。

```text
rank_1 = rank_Q(∂₁)
rank_2 = rank_Q(∂₂)
```

有限Betti数は、

```text
b_0 = |V| - rank_1
b_1 = |E| - rank_1 - rank_2
b_2 = |T| - rank_2
```

として再計算する。

## 非boundary cycle witness

cycle `z` が `im ∂₂` に属さないことは、拡大行列を用いて、

```text
rank_Q([∂₂ | z]) > rank_Q(∂₂)
```

で検証する。

これは保持された有限複体上で、`z` が非零の有理first-homology classを表すことを証明するが、空間全体のhomology classには昇格しない。

## Euler–Poincaré整合

runtimeは、

```text
χ = |V| - |E| + |T|
χ_Betti = b_0 - b_1 + b_2
```

を独立に再計算し、一致を要求する。

## 基準fixture

頂点は、

```text
A, B, C, D
```

edgeは、

```text
AB, AC, AD, BC, CD
```

triangleは、

```text
ABC
```

である。

triangle境界は、

```text
∂₂(ABC) = AB - AC + BC
```

であり、`cycle-boundary-ABC` は明示的boundaryである。

一方、

```text
cycle-hole-ACD = AC - AD + CD
```

はcycleであり、`ABC`の有理倍のboundaryではない。

rankとBetti数は、

```text
rank_Q(∂₁) = 3
rank_Q(∂₂) = 1
(b_0,b_1,b_2) = (1,1,0)
```

である。

Euler characteristicは、

```text
4 - 5 + 1 = 0 = 1 - 1 + 0
```

で一致する。

## Coefficient bound

chain coefficientはboolを除く整数に限定し、絶対値上限を明示する。基準fixtureでは、

```text
maximum_absolute_chain_coefficient = 4
```

である。

未知basis ID、非整数係数、上限超過係数は拒否する。

## Digest binding

次をcanonical digestへ固定する。

```text
vertices
oriented edges
oriented triangles
one-chains
two-chains
exactness witnesses
nontriviality witnesses
```

各recordは固有IDとsource digestを持つ。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source v1.14 nerve certificate digest欠落
source v1.13 finite-cover certificate digest欠落
input digest不一致
頂点・edge・triangle basis不足
重複IDまたは重複source digest
edge loop
重複unoriented edge
triangle boundary edge欠落
未知basis coefficient
非整数chain coefficient
chain coefficient上限超過
宣言された1-chainがcycleでない
exact cycleと2-chain boundaryの不一致
exact cycleのfilling欠落
nontrivial witnessがrational boundary imageに属する
nontrivial cycleのrank witness欠落
Q以外のnontriviality coefficient field
boundary squared非零
有限Betti数不整合
Euler–Poincaré不整合
```

## 固定境界

```text
finite chain complex != planning-space chain complex
finite Betti number != global Betti number
nonboundary in retained complex != global topological obstruction
rational homology != integral homology
rational rank != torsion computation
finite Cech chain data != classical Cech homology equivalence
homology witness != candidate rejection
homology witness != activation authorization
WORLD-conditioned topology != WORLD mutation
```

本層はsource certificateとpersistent WORLD stateを変更しない。

```text
source_nerve_certificate_not_mutated = true
source_finite_cover_certificate_not_mutated = true
persistent_world_state_unchanged = true
```

選択を行わず、read-onlyかつfuture-onlyである。

```text
decision_selection_performed = false
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_finite_simplicial_chain_homology_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_15.lean
```
