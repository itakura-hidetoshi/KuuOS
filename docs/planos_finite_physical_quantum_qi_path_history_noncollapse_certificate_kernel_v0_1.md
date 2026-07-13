# PlanOS Finite Physical Quantum Qi Path-History Noncollapse Certificate v0.1

## 位置づけ

PlanOS v1.20は、有限diagram familyに対するweighted Fréchet functional、有限barycenter candidate、consensus transport、dispersionをexactに再計算した。

PlanOS v1.21は、その代表値を計画空間そのものと同一視しない。

計画空間の基底表現を単純なbranch treeではなく、有限のPhysical Quantum Qi path-history ensembleとして保持する。

```text
finite path histories
  -> shared prefixes
  -> branching
  -> reconvergence
  -> loops when present
  -> scenario marginals
  -> exact finite phase interference
  -> non-collapse certificate
```

branchはpath-history familyから導出される局所観察量であり、branch treeを計画空間の存在論にはしない。

## Physical Quantum Qiとの接続

KuuOSのPhysical Quantum Qi Path Integralは、

```text
Z_Qi = Integral D gamma exp(i S_Qi[gamma] / hbar)
```

およびEuclidean form

```text
Z_Qi(beta) = Integral D gamma exp(-S_Qi_E[gamma] / hbar)
```

として、関係的flow historyのweighted sumを表す。

v1.21は連続path integral全体を主張しない。有限・有界なpath-history familyについてexact certificateを構成する。

## Formal Euclidean generating polynomial

浮動小数点指数関数を導入せず、有限history `gamma` のaction levelを `S_gamma ∈ N`、weight numeratorを `w_gamma ∈ N` として、

```text
Z_Qi(q) = sum_gamma w_gamma q^(S_gamma)
```

を形式多項式として保持する。

各action level `s` の係数は、

```text
c_s = sum_{gamma : S_gamma = s} w_gamma
```

である。

`q` の数値評価、温度選択、sampling、path選択は行わない。

## Exact finite phase

初版では位相を有限 `Z_2` phaseで保持する。

```text
phase_mod2 = 0 -> positive amplitude
phase_mod2 = 1 -> negative amplitude
```

同一terminal stateへ到達するhistory family `Gamma_y` に対し、

```text
A_y = sum_{gamma in Gamma_y} (-1)^(phase_gamma) w_gamma
```

をexact integerで再計算する。

さらに、

```text
total_weight_y = sum_gamma w_gamma
cancellation_y = total_weight_y - |A_y|
coherent_intensity_y = A_y^2
incoherent_intensity_y = sum_gamma w_gamma^2
interference_delta_y
  = coherent_intensity_y - incoherent_intensity_y
```

を保持する。

これは有限phase certificateであり、一般の複素振幅、Born rule、実在する量子計算過程を主張しない。

## State and Qi flow

各stateは以下を保持する。

```text
state_id
source_digest
world_slice_digest
integer Qi coordinate
```

各transitionは以下を保持する。

```text
transition_id
from_state_id
to_state_id
nonnegative action increment
integer Qi flux increment
source_digest
```

Qi fluxは独立に検証する。

```text
qi_flux_increment
  = qi_coordinate(to) - qi_coordinate(from)
```

したがってpath上のQi flowは単なるlabelではなく、state差分に束縛される。

## Finite path histories

各historyは以下を保持する。

```text
history_id
scenario_id
positive rational weight numerator
Z_2 phase
ordered transition IDs
source plan digest
```

全historyは同一initial stateを共有する。historyは有限長であり、transition adjacencyを厳密に検証する。

```text
to(left_transition) = from(right_transition)
```

graph全体がacyclicであることは要求しない。有限history内部でstateが反復する場合、loop historyとして保持する。

## Branching and reconvergence

branch pointは、使用されたhistory subgraphで複数の異なるsuccessorを持つstateである。

```text
branch(state) iff #{successor states} > 1
```

reconvergence pointは、複数の異なるpredecessorを持つstateである。

```text
reconvergence(state) iff #{predecessor states} > 1
```

branch treeではreconvergenceが自然に表現できず、同じ後続構造を複製する。v1.21は一般の有限directed path-history graphを保持するため、再合流を壊さない。

## Shared-prefix profile

history pairごとにstate sequenceの共有prefix長を再計算する。

```text
shared_prefix_length(gamma_a, gamma_b)
```

同じprefixを共有するhistoryを重複した独立branchとして扱わず、shared causal historyを保持する。

## Depth marginals

最大history長までの各depthでstate marginalを再計算する。短いhistoryはterminal stateに留まるものとして扱う。

各depth `d` で、

```text
sum_state weight_numerator(d, state) = common denominator
```

を保持する。

これにより、uncertainty support、temporary divergence、later reconvergence、terminal concentrationをhistoryを一つに選ばず観察できる。

## Scenario marginals

scenarioごとに、

```text
scenario weight numerator
common denominator
member history IDs
```

を保持する。

scenario marginalはscenario rankingではない。scenario weightが大きいことはactivation、selection、truthを意味しない。

## Non-collapse

v1.21の主要claimは最適pathを見つけることではない。

```text
retained history IDs = source history IDs
```

をexactに検証する。

次を行わない。

```text
argmin
representative history selection
history ranking
history pruning
candidate activation
execution
```

v1.20のbarycenter、consensus、dispersionはv1.21 ensemble上の統計量または観測量として参照できるが、ensembleを置換しない。

## Reference fixture

共通denominatorは6で、4本のhistoryを保持する。

```text
history-alpha-direct:
  weight 2, phase +, action 2
  root -> a -> terminal

history-beta-direct:
  weight 2, phase -, action 2
  root -> b -> terminal

history-alpha-rejoin:
  weight 1, phase +, action 3
  root -> a -> c -> terminal

history-beta-rejoin:
  weight 1, phase +, action 3
  root -> b -> c -> terminal
```

formal partition polynomialは、

```text
Z_Qi(q) = 4 q^2 + 2 q^3
```

となる。

terminalでのsigned amplitudeは、

```text
A_terminal = 2 - 2 + 1 + 1 = 2
```

したがって、

```text
total weight = 6
absolute amplitude = 2
phase cancellation = 4
coherent intensity = 4
incoherent intensity = 10
interference delta = -6
```

である。

depth marginalは、

```text
depth 0: root = 6/6
depth 1: a = 3/6, b = 3/6
depth 2: terminal = 4/6, c = 2/6
depth 3: terminal = 6/6
```

となる。

scenario marginalは、

```text
scenario-alpha = 3/6
scenario-beta  = 3/6
```

である。

branch pointsは `root`, `a`, `b`、reconvergence pointsは `c`, `terminal` である。

このfixtureは、単純なtreeでは自然に保持しにくい分岐後の再合流を明示的に含む。

## Fail-closed checks

checkerは少なくとも次を拒否する。

```text
weight denominator mismatch
Qi flux mismatch
broken transition adjacency
missing transition
incorrect retained history set
false argmin claim
false representative selection claim
false pruning claim
execution permission claim
source mutation claim
```

## Mathlib theorem surface

Strict Lean packageは以下を含む。

```text
formal action coefficient
finite Z_2 signed phase amplitude
phase cancellation numerator
coherent and incoherent intensity
exact history retention cardinality
finite marginal mass conservation
reconvergence without tree requirement
reference Z(q) coefficients 4 and 2
reference signed amplitude 2
reference cancellation 4
reference intensities 4 and 10
reference depth marginal mass conservation
reference branch and reconvergence positivity
non-collapse non-authority theorem
bounded read-only future-only theorem
```

## Fixed boundaries

```text
finite path-history family != all possible plans
formal Z_Qi(q) != evaluated physical partition function
Z_2 phase != arbitrary complex quantum phase
signed amplitude != empirical probability
interference witness != execution preference
large amplitude != selected plan
small amplitude != rejected plan
branch point != forced decision point
reconvergence != equivalence of plans
shared prefix != identical future
loop history != permission to repeat action
scenario marginal != scenario truth probability
barycenter observable != collapse of path ensemble
all histories retained != all histories activated
path integral representation != execution authority
WORLD-conditioned history != WORLD mutation
```

## Immutability

次は変更しない。

```text
PlanOS v1.14 path-homotopy certificate
PlanOS v1.20 barycenter and dispersion certificate
Physical Quantum Qi definition document
persistent WORLD state
source plan artifacts
```

## Authority boundary

本層は、

```text
finite
bounded
exact
read-only
future-only
inactive
non-collapsing
```

である。

candidate selection、ranking、pruning、activation、tool invocation、adapter invocation、external action、execution permissionを付与しない。
