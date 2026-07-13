# PlanOS Finite Filtration Persistent Homology Certificate Kernel v0.1

## 位置づけ

PlanOS v1.16 は、保持された有限 simplicial complex の整数 chain complex を構成し、Smith normal form から free rank と torsion invariant factors を再構成した。

PlanOS v1.17 は、その有限 complex を単一状態として扱うのではなく、simplex が段階的に追加される有限 filtration として扱う。

各 filtration stage では整数係数の Smith data を再計算し、filtration 全体では `F2` 境界行列の標準 column reduction から birth/death pairing、barcode interval、persistent Betti number を再構成する。

この層は有限 filtration のみを扱い、planning space 全体の persistent homology、整数 persistence module、zigzag persistence、stability theorem は主張しない。

## Filtered simplex records

各 simplex は固有 ID、filtration 値、source digest を保持する。

```text
vertex_id / edge_id / triangle_id
filtration
source_*_digest
```

edge は2頂点、triangle は3頂点を持つ。

全 simplex ID は dimension をまたいで一意でなければならない。

## Face closure と filtration monotonicity

edge の各頂点は存在し、

```text
filtration(vertex) <= filtration(edge)
```

を満たす。

triangle の3本の boundary edge はすべて存在し、

```text
filtration(edge) <= filtration(triangle)
```

を満たす。

filtration stage の列は、入力 simplex に実際に現れる filtration 値の狭義昇順列と一致しなければならない。

## Stagewise integer Smith data

各 stage `s` について、

```text
K_s = { simplex | filtration(simplex) <= s }
```

を構成する。

`K_s` ごとに整数境界写像、spanning forest、fundamental cycle basis、triangle-boundary presentation matrix を再構成する。

その presentation matrix に Smith normal form を適用し、次を保持する。

```text
stage
vertex_count
edge_count
triangle_count
h0_free_rank
h1_free_rank
h2_free_rank
h1_smith_diagonal
h1_torsion_invariant_factors
```

各 stage の整数 homology は独立に再計算される。

ただし、stage 間の整数 persistence module や module decomposition は計算しない。

## F2 persistent reduction

全 simplex を次の順に並べる。

```text
(filtration, dimension, simplex_id)
```

face closure と filtration monotonicity により、各 boundary simplex は対象 simplex より前に現れる。

`F2` 上の boundary column を左から順に reduction する。

```text
while low(column) is already paired:
    column := column XOR previous_column
```

reduced column が非零なら、その pivot simplex と現在の simplex を birth/death pair とする。

reduced column が零なら、その simplex は homology class の birth candidate となる。

後続 column の pivot になれば有限 interval、最後まで pair されなければ infinite intervalとなる。

## Barcode interval

各 interval は次を保持する。

```text
interval_id
dimension
birth
death | null
birth_simplex_id
death_simplex_id
```

有限 interval は半開区間、

```text
[birth, death)
```

として扱い、

```text
birth < death
```

を必須とする。

infinite interval は `death = null` とし、death simplex ID は空文字列に固定する。

## Persistent Betti number

stage `s` における dimension `k` の persistent Betti number は、

```text
birth <= s < death
```

を満たす有限 interval と、

```text
birth <= s
```

を満たす infinite interval の本数として再計算する。

## 基準 filtration

基準 fixture は3頂点、3辺、1三角形からなる。

### Stage 0

```text
vertices: A B C
```

```text
H0 = Z^3
H1 = 0
H2 = 0
```

### Stage 1

```text
edges: AB AC BC
```

三角形の one-skeleton が形成される。

```text
H0 = Z
H1 = Z
H2 = 0
```

### Stage 2

```text
triangle: ABC
```

one-cycle が充填される。

```text
H0 = Z
H1 = 0
H2 = 0
```

## Reference barcode

`F2` reduction は次を再構成する。

```text
H0: vertex-B -> edge-AB   [0,1)
H0: vertex-C -> edge-AC   [0,1)
H0: vertex-A -> infinity  [0,∞)
H1: edge-BC -> triangle-ABC [1,2)
```

したがって persistent Betti number は、

```text
stage 0: (beta0,beta1,beta2) = (3,0,0)
stage 1: (beta0,beta1,beta2) = (1,1,0)
stage 2: (beta0,beta1,beta2) = (1,0,0)
```

となる。

## Digest binding

canonical digest は次を固定する。

```text
filtered vertex records
filtered edge records
filtered triangle records
filtration stages
claimed stage Smith data
claimed barcode intervals
claimed persistent Betti data
```

source digest を変更した場合、旧 digest は一致しない。

## Fail-closed 条件

次の場合は certificate を生成しない。

```text
source certificate digest 欠落
input digest 不一致
空の vertex set
重複 simplex ID
重複 unoriented edge / triangle
filtration 値不正
filtration stage 不一致
edge の vertex 欠落
edge が vertex より早く出現
triangle boundary edge 欠落
triangle が edge より早く出現
maximum simplex count 超過
stage Smith claim 不一致
barcode claim 不一致
persistent Betti claim 不一致
非正の persistence lifetime
final integer H1 rank と F2 beta1 の不一致
```

## 固定境界

```text
finite barcode != planning-space persistent homology
F2 barcode != integer persistence module
stagewise Smith data != persistent Smith decomposition
barcode length != candidate utility
long-lived class != ethical priority
short-lived class != automatic noise
persistent interval != plan selection
persistent Betti number != activation authorization
WORLD-conditioned topology != WORLD mutation
```

本層は v1.16 integer-homology certificate と v1.14 nerve certificate を変更しない。

```text
source_integer_homology_certificate_not_mutated = true
source_nerve_certificate_not_mutated = true
persistent_world_state_unchanged = true
```

候補 identity を保持し、ranking や selection を行わない。

```text
barcode_does_not_rank_candidates = true
decision_selection_performed = false
```

read-only、future-only、inactive である。

```text
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_finite_filtration_persistent_homology_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_17.lean
```
