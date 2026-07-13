# PlanOS Finite Wasserstein Fréchet Barycenter and Dispersion Certificate Kernel v0.1

## 位置づけ

PlanOS v1.19は、2つの有限persistence diagram間の有限 `p`-Wasserstein transportをexact doubled-integer arithmeticで再計算した。

PlanOS v1.20は、入力を有限diagram family

```text
D_1, ..., D_m
```

へ拡張し、有限列挙されたbarycenter candidate集合についてweighted Fréchet functional、finite minimizer tie set、consensus transport、dispersionをcertificate化する。

この層は、全persistence-diagram空間上のWasserstein barycenter存在・一意性を主張しない。有限候補集合内の決定的再計算だけを行う。

## Source lineage binding

各source diagramは次へ束縛される。

```text
PlanOS v1.17 persistent-homology certificate digest
PlanOS v1.18 bottleneck-stability certificate digest
PlanOS v1.19 p-Wasserstein transport certificate digest
```

source certificate、source diagram、persistent WORLD stateは変更しない。

## Exact rational weights

各source weightは、正の整数numerator `w_a` と共通denominator `Q` で保持する。

```text
w_a / Q
```

本kernelでは、

```text
sum_a w_a = Q
```

を要求する。

浮動小数点weightは使用しない。

## Finite Fréchet functional

有限candidate diagram `B` とsource diagram `D_a` の間で、v1.19の有限dynamic programmingを再利用し、

```text
T_p(B, D_a) = (2 W_p(B, D_a))^p
```

をexact integerで再計算する。

weighted Fréchet functionalは、共通denominator付きで

```text
F_p(B)
  = (1 / Q) * sum_a w_a T_p(B, D_a)
```

とする。

certificateではnumerator

```text
F_num(B) = sum_a w_a T_p(B, D_a)
```

を主値として保持し、`F_num(B) / Q` をexact rationalとして保持する。

## Finite minimizer and tie set

有限候補集合

```text
B_1, ..., B_k
```

について、

```text
minimum_num = min_j F_num(B_j)
```

を再計算する。

minimizer tie setは、

```text
{ B_j | F_num(B_j) = minimum_num }
```

である。

代表candidateはtie set内のcandidate ID辞書順最小とする。

```text
representative = lexical_min(minimizer_tie_set)
```

これはcertificate representationの決定性を与えるだけで、planning candidateの選択・ranking・activationではない。

有限候補集合内のminimizerが1個である場合に限り、

```text
finite_candidate_minimizer_unique = true
```

とする。

全diagram空間上のbarycenter uniquenessは常に未主張である。

## Consensus transport

各source diagramから代表candidateへの有限optimal transportを再計算する。

各sourceについて以下を保持する。

```text
source ID
weight numerator
transport p-power
weighted contribution numerator
maximum edge cost
integer root bracket
full matching
homology dimension別power contribution
```

無限intervalは無限intervalとのみmatching可能であり、対角線へ送らない。

## Dispersion certificate

代表candidate `B*` に対し、dispersion numeratorは

```text
Disp_num
  = sum_a w_a T_p(B*, D_a)
```

である。

これは有限candidate Fréchet minimum numeratorと一致する。

source contributionは

```text
Contribution_a = w_a T_p(B*, D_a)
```

であり、

```text
sum_a Contribution_a = Disp_num
```

を検証する。

`Disp_num = 0` の場合、正weightと自然数powerにより、全source contributionが0であることを検証する。

## Maximum source deviation

source別transport p-powerの最大値

```text
max_a T_p(B*, D_a)
```

と、それを達成する全source IDを保持する。

無理根をdecimal近似せず、各source transportについてinteger root bracketを保持する。

## Weighted moment profile

consensus matching edge costを `c_{a,e}` とする。

order `r = 1, ..., p` について、

```text
M_r_num
  = sum_a w_a sum_e c_{a,e}^r
```

を再計算する。

`r = p` では、

```text
M_p_num = Disp_num
```

を検証する。

## Weighted consensus tail profile

各threshold `T` について、source別matchingのtail countを重み付けし、

```text
N_T_num
  = sum_a w_a * #{e | c_{a,e} >= T}
```

を保持する。

さらに、

```text
N_T_num * T^p <= Disp_num
```

をexact integerで検証する。

unweighted edge countも観察用に保持するが、candidate rankingには使わない。

## Reference fixture

source weightsは、

```text
source-A: 1/4
source-B: 2/4
source-C: 1/4
```

である。

candidate集合は、

```text
candidate-center
candidate-left
candidate-right
```

である。

`p = 2` のsource transport powersは以下となる。

```text
candidate-center: [12, 4, 12]
candidate-left:   [0, 16, 40]
candidate-right:  [40, 16, 0]
```

したがって、

```text
F_num(candidate-center)
  = 1*12 + 2*4 + 1*12
  = 32

F_num(candidate-left)
  = 1*0 + 2*16 + 1*40
  = 72

F_num(candidate-right)
  = 1*40 + 2*16 + 1*0
  = 72
```

有限候補集合内の唯一のminimizerは、

```text
candidate-center
```

である。

reference dispersionは、

```text
Disp_num = 32
Q = 4
Disp = 32/4 = 8
```

source contributionは、

```text
[12, 8, 12]
```

で、総和は32である。

最大source transport powerは12であり、

```text
source-A
source-C
```

が同率である。

weighted moment profileは、

```text
M_1_num = 16
M_2_num = 32
```

である。

weighted tail profileは、

```text
threshold 1:
  weighted count numerator = 8
  unweighted count = 7
  lower bound numerator = 8

threshold 2:
  weighted count numerator = 8
  unweighted count = 7
  lower bound numerator = 32

threshold 3:
  weighted count numerator = 0
  unweighted count = 0
  lower bound numerator = 0
```

threshold 2でtail p-power boundはdispersion numeratorを飽和する。

## Non-uniqueness fixture

同じ有限Fréchet functional値を持つcandidateを追加したfixtureでは、

```text
minimizer count = 2
finite_candidate_minimizer_unique = false
```

とし、代表はcandidate ID辞書順で決定する。

このrepresentativeは証拠のcanonicalizationだけを目的とする。

## Digest binding

canonical input digestは以下を束縛する。

```text
source diagram family
source certificate digests
integer weight numerators
common denominator
finite barycenter candidate set
candidate diagram digests
p exponent
consensus tail thresholds
claimed candidate functionals
claimed minimizer tie set
claimed lexical representative
claimed consensus source transports
claimed dispersion numerator
claimed maximum source deviation
claimed weighted moment profile
claimed consensus tail profile
```

## Fail-closed conditions

以下の場合はcertificateを生成しない。

```text
source family欠落
candidate set欠落
source v1.17/v1.18/v1.19 digest欠落
candidate diagram digest不一致
source ID重複
candidate ID重複
weight numerator非正
weight numerator総和とcommon denominator不一致
p非正または上限超過
coordinate上限超過
source count上限超過
candidate count上限超過
interval count上限超過
threshold count上限超過
threshold非正・非単調・重複
candidate functional claim改変
source transport power claim改変
minimizer tie set改変
representative candidate改変
consensus matching改変
dispersion改変
maximum source deviation改変
weighted moment改変
weighted tail改変
source contribution sum不一致
p-th momentとdispersion不一致
weighted tail p-power bound違反
source integer root bracket違反
input digest不一致
```

## Mathlib theorem surface

Strict Lean packageは以下を含む。

```text
weighted finite Fréchet numerator nonnegativity
finite minimizer witness lower-bound extraction
source contribution sum extraction
zero dispersion implies every source contribution is zero
weighted consensus tail p-power bound extraction
reference center functional numerator = 32
reference side functional numerators = 72
reference finite candidate minimum witness = 32
reference source contribution sum = 32
reference weighted moments = 16 and 32
reference threshold-two tail bound
barycenter/consensus/dispersion non-authority theorem
finite bounded future-only theorem
```

## Fixed boundaries

```text
finite candidate barycenter != global Wasserstein barycenter
finite candidate minimizer != global barycenter existence
finite tie-set singleton != global barycenter uniqueness
Fréchet minimizer != candidate utility optimum
consensus diagram != selected plan
low dispersion != activation authorization
high dispersion != automatic rejection
diagonal consensus != deletion authority
finite diagram family != planning population
lexical representative != planning selection
weighted moment != candidate ranking
weighted tail != candidate rejection
source transport != executable plan
WORLD-conditioned topology != WORLD mutation
```

## Authority boundary

この層は以下を保持する。

```text
read-only
future-only
inactive now
candidate selectionなし
candidate rankingなし
activationなし
execution permissionなし
```
