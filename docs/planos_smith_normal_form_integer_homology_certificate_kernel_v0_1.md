# PlanOS Smith Normal Form and Integer Homology Certificate Kernel v0.1

## 位置づけ

PlanOS v1.15は、有限simplicial chain complexについて、

```text
C_2 -> C_1 -> C_0
```

の境界行列、`boundary_1 * boundary_2 = 0`、有理rank、有限Betti数、有限非boundary cycleを保持した。

PlanOS v1.16は、この有限chain complexを整数係数へ持ち上げる。

有限graphのspanning forestからfundamental cycle latticeを構成し、triangle boundaryをその整数cycle basisで表現する。そのpresentation matrixへSmith normal formを適用し、free rankとtorsion invariant factorsを保持する。

本層は保持された有限複体の整数homologyのみを扱う。planning space全体の整数homology、古典的Čech homologyとの同値、persistent homology、候補選択、実行判断は主張しない。

## 有限chain complex

入力は、

```text
vertex_records
oriented_edge_records
oriented_triangle_records
```

である。

各edgeはvertex IDの辞書順で正向きを固定する。

```text
boundary_1 [u,v] = [v] - [u]
```

各triangleもvertex IDの辞書順で正向きを固定する。

```text
boundary_2 [a,b,c]
= [b,c] - [a,c] + [a,b]
```

runtimeは両境界行列を整数で再構成し、

```text
boundary_1 * boundary_2 = 0
```

を検証する。

## Fundamental cycle lattice

edgeをID順で処理し、deterministicなspanning forestを構成する。

forestに追加されない各chord edge `e` について、tree内の一意pathと組み合わせたfundamental cycle `z_e` を構成する。

各cycleについて、

```text
boundary_1 z_e = 0
```

を独立に検証する。

component数を `c`、vertex数を `n`、edge数を `m` とすると、保持するcycle lattice rankは、

```text
m - n + c
```

である。

## Integer H1 presentation

fundamental cycle basisでは各basis vectorが固有のchord coefficient `1` を持つ。

そのため、各triangle boundaryのbasis coordinateは、各chord edge上のboundary coefficientとして読み出せる。

このcoordinate matrixを、

```text
P : Z^T -> Z^(m-n+c)
```

とする。

runtimeはcoordinateから元のtriangle boundaryを再構成し、edge basis上で完全一致することを要求する。

したがって、保持された有限複体のfirst integer homology presentationは、

```text
H_1 = Z^(m-n+c) / image(P)
```

である。

## Smith normal form

runtimeは整数presentation matrixへunimodular row operationとcolumn operationを適用し、正の非零対角列、

```text
d_1, d_2, ..., d_r
```

を再構成する。

Smith divisibility chainとして、

```text
d_1 | d_2 | ... | d_r
```

を要求する。

free rankは、

```text
free_rank(H_1) = cycle_lattice_rank - r
```

である。

`d_i > 1` の項をtorsion invariant factorとして保持する。

```text
H_1 ~= Z^free_rank
      (+) Z/d_i Z
```

本kernelはunimodular変換行列そのものをcertificateへ保持しない。対角化された行列とSmith invariant factorsのみを保持する。

## 基準有限複体

基準fixtureは6頂点、15辺、10三角形からなる有限simplicial complexを使用する。

```text
vertices = A, B, C, D, E, F
```

全15 edgeを保持する。

```text
AB AC AD AE AF
BC BD BE BF
CD CE CF
DE DF EF
```

triangleは、

```text
ABC ABD ACE ADF AEF
BCF BDE BEF CDE CDF
```

である。

各edgeはちょうど2つのtriangleに含まれ、有限なprojective-plane型triangulation witnessを形成する。

spanning treeは5 edge、chordは10 edgeである。

したがって、

```text
cycle_lattice_rank = 15 - 6 + 1 = 10
```

である。

presentation matrixのSmith diagonalは、

```text
1, 1, 1, 1, 1, 1, 1, 1, 1, 2
```

となる。

したがって、保持された有限複体では、

```text
H_0 = Z
H_1 = Z/2Z
H_2 = 0
```

である。

これは保持された有限複体の整数homologyであり、planning space全体に昇格しない。

## Digest binding

次をcanonical digestへ固定する。

```text
vertex records
oriented edge records
oriented triangle records
claimed Smith diagonal
expected H0 free rank
expected H1 free rank
expected H2 free rank
expected torsion invariant factors
```

入力改変後に古いdigestを再利用した場合は拒否する。

## Fail-closed条件

次の場合はcertificateを生成しない。

```text
source v1.15 digest欠落
source v1.14 digest欠落
input digest不一致
vertex / edge / triangle schema不正
重複IDまたは重複source digest
edgeの未知vertex参照
triangleの未知vertex参照
triangle boundary edge欠落
basis size上限超過
boundary_1 * boundary_2 != 0
fundamental cycleのboundary非零
triangle boundaryのcycle basis再構成不一致
computed Smith diagonalの整除鎖不成立
computed Smith rankとrational rankの不一致
claimed Smith diagonal不一致
期待free rank不一致
期待torsion invariant factor不一致
非正または非整数のinvariant factor
```

## 固定境界

```text
finite integer homology != planning-space integer homology
Smith diagonal != global topological invariant
Z/2 witness != automatic plan rejection
torsion invariant != ethical obstruction
finite triangulation != manifold identification
unimodular diagonalization != retained basis change authority
integer homology != persistent homology
finite Cech lineage != classical Cech homology equivalence
topological evidence != activation authorization
WORLD-conditioned topology != WORLD mutation
```

本層はsource certificateとpersistent WORLD stateを変更しない。

```text
source_chain_homology_certificate_not_mutated = true
source_nerve_certificate_not_mutated = true
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
PYTHONPATH=. python3 scripts/check_planos_smith_normal_form_integer_homology_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_16.lean
```
