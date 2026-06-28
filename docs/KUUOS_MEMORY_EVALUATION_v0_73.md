# KuuOS Memory Evaluation v0.73

## 目的

v0.73は、v0.72の非マルコフMemoryOS接続について、有限個の変形候補を同一条件で評価し、決定的に一件を選択します。

候補生成、候補検証、候補評価、選択証拠を分離します。

## 有限memory family

有限familyは、source memory kernel digestへ束縛された候補集合です。

```text
F = {delta K_1, delta K_2, ..., delta K_n}
```

family内のmember IDは一意でなければなりません。

全memberは同じsource kernel digestへ束縛されなければなりません。

## v0.72検証

各memberは、v0.72の`validate_nonmarkov_candidate`による完全検証を通過しなければなりません。

memory部分加群、semantic projector、protected部分、authority filtration、pathwise Leibniz則、履歴依存性、ゲージ共変性、rollbackの条件を継承します。

## memory return score

評価量は、有限履歴上のmemory寄与のFrobenius二乗和です。

```text
E(K,h_t) = sum_i ||K_i(h_t)||_F^2
```

signed permutation gaugeの前後でscoreが一致することをruntimeで検査します。

低いscoreをtruthと同一視しません。

## 決定的選択

受理された候補は次の順で比較します。

```text
1. memory return score
2. changed term count
3. canonical member digest
```

この順序により、familyの入力順序に依存しない選択を行います。

受理可能な候補が存在しない場合はsource kernelを保持します。

source bindingが一致しない場合もfail closedとします。
