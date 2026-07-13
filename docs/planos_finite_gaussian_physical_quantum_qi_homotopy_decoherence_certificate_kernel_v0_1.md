# PlanOS Finite Gaussian Physical Quantum Qi Homotopy Decoherence Certificate v0.1

## 位置づけ

PlanOS v1.21は、計画空間を単一のbranch、代表path、barycenterへ潰さず、有限のPhysical Quantum Qi path-history ensembleとして保持した。

PlanOS v1.22は、その有限history familyを保持したまま、位相面を `Z_2` から `Z_4` へ拡張し、Gaussian integer amplitude、homotopy-class別振幅、decoherence前後の干渉をexact integer arithmeticで分離する。

```text
finite retained histories
  -> Z4 phase
  -> Gaussian amplitude in Z[i]
  -> endpoint coherent sum
  -> homotopy-class amplitude blocks
  -> exact decoherence mask
  -> histories still retained
```

最小action、dominant path、argmin、代表historyは計算しない。

## Exact Z4 phase

各history `gamma` は、

```text
phase_mod4 ∈ {0,1,2,3}
```

を持つ。

```text
0 ->  1
1 ->  i
2 -> -1
3 -> -i
```

weight numeratorを `w_gamma` とすると、Gaussian integer amplitudeは、

```text
a_gamma = w_gamma i^(phase_gamma) ∈ Z[i]
```

である。実部・虚部を整数対として保持し、三角関数、浮動小数点、複素近似は使用しない。

## Endpoint amplitude and interference

terminal state `y` に到達するhistory familyに対し、

```text
A_y = sum_{gamma -> y} a_gamma
```

をexactに再計算する。

```text
coherent_intensity_y = Re(A_y)^2 + Im(A_y)^2
incoherent_intensity_y = sum_gamma w_gamma^2
interference_delta_y = coherent_intensity_y - incoherent_intensity_y
```

coherent amplitudeが0でも、history familyは削除されない。完全相殺とhistory不在を区別する。

## Homotopy-class amplitude

各historyは、

```text
homotopy_class_id
source_homotopy_witness_digest
```

を保持する。class labelはPlanOS v1.14 path-homotopy certificate digestへ束縛される。

各terminal state・homotopy classごとに、

```text
A_[h],y = sum_{gamma -> y, class(gamma)=[h]} a_gamma
```

を再計算し、class内coherent intensityとclass内interferenceを保持する。

これは有限入力のdigest-bound classificationであり、全path空間のhomotopy classification theoremではない。

## Exact decoherence mask

初版ではcoherence block partitionをhomotopy class partitionと一対一に束縛する。

各block `b` のamplitudeを、

```text
A_b = sum_{gamma in b} a_gamma
```

とする。

pre-decoherence intensityは、

```text
I_pre = |sum_b A_b|^2
```

post-decoherence block intensityは、

```text
I_post = sum_b |A_b|^2
```

fully incoherent intensityは、

```text
I_incoherent = sum_gamma |a_gamma|^2 = sum_gamma w_gamma^2
```

である。

さらに、

```text
retained_within_block_interference = I_post - I_incoherent
discarded_cross_block_interference = I_pre - I_post
```

をexact integerで保持する。

```text
I_pre = I_post + discarded_cross_block_interference
I_post = I_incoherent + retained_within_block_interference
```

を検証する。

このmaskはcross-block interferenceの観測分離であり、history deletion、reweighting、rankingではない。

## Reference fixture

v1.21と同じ4本のpath historyを保持し、位相を次のように拡張する。

```text
history-alpha-direct:
  weight 2, phase 0, amplitude 2

history-beta-direct:
  weight 2, phase 2, amplitude -2

history-alpha-rejoin:
  weight 1, phase 1, amplitude i

history-beta-rejoin:
  weight 1, phase 3, amplitude -i
```

formal Euclidean generating polynomialは変わらない。

```text
Z_Qi(q) = 4 q^2 + 2 q^3
```

global endpoint amplitudeは、

```text
A_terminal = 2 - 2 + i - i = 0
```

したがって、

```text
I_pre = 0
I_incoherent = 2^2 + 2^2 + 1^2 + 1^2 = 10
interference_delta = -10
```

となる。

homotopy class別には、

```text
A_alpha = 2 + i
|A_alpha|^2 = 5

A_beta = -2 - i
|A_beta|^2 = 5
```

である。

homotopy-class decoherence後は、

```text
I_post = 5 + 5 = 10
retained_within_block_interference = 0
discarded_cross_block_interference = -10
```

となる。

global amplitudeが0でも、4本のhistory、2つのhomotopy class、2つのcoherence blockはすべて保持される。

## Structure retained from v1.21

以下を引き続き再計算する。

- state and transition digest binding
- integer Qi coordinates and exact Qi flux
- ordered path adjacency
- shared initial state
- formal action polynomial
- depth marginals and mass conservation
- scenario marginals
- branch points
- reconvergence points
- finite loops when present
- pairwise shared prefixes
- exact source-to-retained history identity

## Fail-closed validation

checkerは少なくとも次を拒否する。

- invalid `phase_mod4`
- weight denominator mismatch
- Qi flux mismatch
- broken transition adjacency
- missing homotopy witness digest
- one homotopy class split across multiple coherence blocks
- one coherence block mixing multiple homotopy classes
- incorrect amplitude or intensity claim
- incorrect retained-history claim
- false argmin, representative, pruning, activation, or execution claim

## Mathlib theorem surface

Strict Lean packageは次を含む。

- exact Z4 Gaussian phase components
- Gaussian amplitude real and imaginary sums
- squared Gaussian norm
- two-block norm/interference decomposition
- exact decoherence residual decomposition
- history, homotopy-class, coherence-block retention cardinality
- reference global amplitude `(0,0)`
- reference class amplitudes `(2,1)` and `(-2,-1)`
- reference pre intensity `0`
- reference post-decoherence intensity `10`
- reference incoherent intensity `10`
- reference discarded cross-block interference `-10`
- non-collapse non-authority theorem
- bounded read-only future-only theorem

## Fixed boundaries

```text
finite Z4 phase != arbitrary complex phase
Gaussian integer amplitude != empirical probability
homotopy class label != global homotopy classification theorem
decoherence block != complete physical environment model
zero coherent amplitude != absent history
discarded interference != deleted plan
post-decoherence intensity != execution preference
all histories retained != all histories activated
path integral evidence != execution authority
WORLD-conditioned history != WORLD mutation
```

v1.14、v1.20、v1.21、Physical Quantum Qi定義、source plans、persistent WORLD stateは変更しない。
