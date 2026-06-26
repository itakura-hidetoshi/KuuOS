# WORLD v0.57 Algebraic Tomita closability

## 目的

WORLD v0.57は、v0.56で入力として残った相対モジュラー解析を第一原理側から構築する最初の段階である。

この段階では、相対モジュラー作用素そのものを仮定しない。

代数的Tomitaグラフの稠密定義域と可閉性を、Hilbert空間上の具体的なグラフ条件として分離する。

## 構成

左表現を `a ↦ aΩ`、対合を `a ↦ a⋆` とする。

代数的Tomitaグラフを次で定義する。

```text
G(S₀) = {(aΩ, a⋆Ω)}
```

真空ベクトルの分離性に対応する表現写像の単射性から、次を証明する。

```text
代表元からの独立性
グラフの右成分の一意性
S₀² = 1
```

左表現の稠密像から、代数的定義域の稠密性を得る。

## 可閉性

可閉性は次の標準条件で定義する。

```text
(0, z) ∈ closure G(S₀) ならば z = 0
```

右側の稠密な双対核 `bΩ` と、Tomita双対関係

```text
⟨a⋆Ω, bΩ⟩ = ⟨aΩ, b⋆Ω⟩
```

を用いる。

`aₙΩ → 0` かつ `aₙ⋆Ω → z` のとき、任意の右核ベクトルに対する `z` の内積が零になる。

右核の稠密性から `z = 0` を得る。

Leanでは、内積の連続性、極限の一意性、`DenseRange.eq_zero_of_inner_left`、`mem_closure_iff_seq_limit`を用いて、逐次条件からグラフ閉包の可閉性条件まで導く。

## Leanで直接証明する定理

```text
domain_dense
tomita_value_independent
graph_right_unique
graph_flip
tomita_value_sq
representative_sequential_closability
graph_sequentially_closable
graph_closable
```

## 厳密な射程

この核は、von Neumann代数の標準形、自然正錐、相対Tomita作用素、随伴作用素、極分解、相対モジュラー作用素をまだ構成しない。

`AlgebraicTomitaDualCore` の稠密表現と双対関係は、次段階で標準形と可換代数から具体化する必要がある。

したがってv0.57は、第一原理系列の可閉性補題を閉じる段階であり、Araki理論全体の完成ではない。
