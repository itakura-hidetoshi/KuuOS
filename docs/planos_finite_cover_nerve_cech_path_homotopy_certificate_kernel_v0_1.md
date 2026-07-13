# PlanOS Finite Cover Nerve, Čech Overlap, and Path Homotopy Certificate Kernel v0.1

## 位置づけ

PlanOS v1.13は、有限normal-ball集合、明示的overlap、局所測地線extension chain、有限window到達をbounded Hopf–Rinow witnessとして保持した。

PlanOS v1.14は、その有限coverを有限simplicial complexへ写す。

```text
normal ball          -> nerve vertex
pairwise overlap     -> nerve edge
triple overlap       -> Čech 2-simplex
ball transition path -> finite nerve path
triangle move        -> finite path homotopy witness
```

この層は保持された有限cover上の位相的整合だけを扱う。

古典的nerve theorem、coverとのhomotopy equivalence、基本群、全path homotopy class、大域位相不変量は主張しない。

## Nerve vertices

各vertexはv1.13由来のnormal ball recordである。

```text
ball_id
center
radius
source_injectivity_radius_lower_bound
chart_id
source_normal_ball_digest
```

各ballについて、

```text
0 < radius < source_injectivity_radius_lower_bound
```

を再検証する。

保持されたsampleは一つのvertexへ明示的に割り当てられ、割当ball内にstrictly containedであることを再計算する。

## Pairwise overlap edge

nerve edgeは、二つのnormal ballの明示的overlap witnessから構成する。

```text
edge_id
left_ball_id
right_ball_id
overlap_witness
source_overlap_digest
```

witnessを `w`、ball中心と半径を `(p_i,r_i)` とすると、

```text
r_left  - distance(p_left, w)  >= minimum_overlap_margin
r_right - distance(p_right, w) >= minimum_overlap_margin
```

を要求する。

自己loop、同一unordered pairの重複、重複source digestは拒否する。

## Čech 2-simplex

三つのballの共通部分候補を、明示的triple-overlap witnessで保持する。

```text
triangle_id
vertex_ball_ids
triple_overlap_witness
source_triple_overlap_digest
```

三頂点を `A,B,C` とすると、boundary edge

```text
AB
AC
BC
```

がすべてnerveに存在しなければならない。

triple witness `w_ABC` は三つすべてのball内で、

```text
min_i (r_i - distance(p_i,w_ABC))
>= minimum_triple_overlap_margin
```

を満たす。

これは有限Čech 2-simplex witnessであり、任意高次交差を含む完全Čech complexではない。

## Finite nerve path

pathはball IDの有限列である。

```text
path_id
vertex_sequence
source_path_digest
```

連続する全vertex pairがnerve edgeで結ばれていることを要求する。

stationary edge、存在しないball、欠落edgeは拒否する。

## Elementary triangle path homotopy

v1.14では、2-simplex boundaryに沿うelementary moveだけを扱う。

三角形 `A,B,C` に対し、

```text
[A,B,C] -> [A,C]
```

をtriangle contractionとして保持する。

逆方向はtriangle expansionである。

各moveについて、

```text
move_id
move_kind
source_path_id
target_path_id
triangle_id
source_move_digest
```

を保持する。

runtimeは、

```text
source start = target start
source finish = target finish
```

および、sourceとtargetが指定triangleによる一回の挿入または削除で一致することを再計算する。

## Connected finite nerve

reference root vertexから、保持された全vertexへedge pathで到達できることを有限graph traversalで検証する。

これは保持された有限nerveのconnectednessであり、元の計画空間全体の連結性ではない。

## 基準fixture

三つのnormal ballを使用する。

```text
A: center (0.0,0.0), radius 0.8
B: center (0.8,0.0), radius 0.8
C: center (0.4,0.6), radius 0.8
```

pairwise overlap edgeは、

```text
AB witness: (0.4,0.0)
AC witness: (0.2,0.3)
BC witness: (0.6,0.3)
```

である。

triple-overlap witnessは、

```text
ABC witness: (0.4,0.2)
```

である。

これにより、全三辺と2-simplex `ABC` を再構成する。

保持するpathは、

```text
path-long  = [A,B,C]
path-short = [A,C]
```

であり、

```text
[A,B,C] -> [A,C]
```

のtriangle contractionを検証する。

## Digest binding

次をcanonical digestへ固定する。

```text
coordinate schema
normal-ball records
covered samples
nerve edges
Čech triangles
nerve paths
path-homotopy moves
```

入力変更後に古いdigestを再利用した場合は拒否する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source v1.13 certificate digest欠落
source atlas digest欠落
input digest不一致
coordinate schema不正
ball不足または重複
normal-ball radius不正
sample未被覆または割当ball欠落
edge自己loopまたはpair重複
overlap margin不足
triangle頂点不正
triangle boundary edge欠落
triple-overlap margin不足
reference root欠落
有限nerve非連結
path edge欠落
path endpoint変更
triangle move不一致
重複IDまたはsource digest
非有限座標
```

## 固定境界

```text
finite nerve != planning space topology
pairwise overlap != chart equivalence
Čech 2-simplex != complete Čech complex
finite connected nerve != global connectedness
triangle move != complete path homotopy classification
finite path witness != fundamental group computation
local-to-global finite coherence != classical nerve theorem
geometric topology != candidate selection
geometric topology != activation authorization
WORLD-conditioned topology != WORLD mutation
```

次を明示的に保持する。

```text
finite_complex_only = true
classical_nerve_theorem_not_claimed = true
cover_homotopy_equivalence_not_claimed = true
fundamental_group_not_computed = true
global_path_homotopy_classification_not_claimed = true
global_topological_invariant_not_claimed = true
```

source v1.13 certificate、source atlas certificate、persistent WORLD stateを変更しない。

```text
source_finite_cover_certificate_not_mutated = true
source_atlas_certificate_not_mutated = true
persistent_world_state_unchanged = true
```

候補identityを保持し、選択を行わない。

```text
candidate_identity_retained = true
decision_selection_performed = false
```

read-onlyかつfuture-onlyである。

```text
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

## 検証

```bash
PYTHONPATH=. python3 scripts/check_planos_finite_cover_nerve_cech_path_homotopy_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_14.lean
```
