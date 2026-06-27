# KuuOS Non-Markov Memory Connection v0.72

## 目的

v0.72は、v0.71の非可換Leibniz接続へ、read-only履歴から作用する有限MemoryOS kernelを加えます。

現在状態だけから次状態を定めるMarkov接続ではありません。

接続は現在切断と有限履歴の双方に依存します。

```text
nabla_i^K(m_t, h_t)
  = nabla_i^(0)(m_t) + K_i(h_t)
```

ここで、`h_t`は確定済みMemoryOS capsuleから読み出した履歴です。

## read-only履歴

履歴は次のimmutable構造です。

```text
history = (frame_tau1, frame_tau2, ..., frame_tauk)
```

各frameは次へ束縛されます。

- epoch
- local module section
- source MemoryOS capsule digest

履歴epochは厳密に増加しなければなりません。

全frameは同じcontext dimension、module rank、source capsule digestを持ちます。

候補生成と検証は履歴を変更しません。

## 有限履歴kernel

kernel termは次で表します。

```text
(direction, lag, operator)
```

接続への履歴寄与は、

```text
K_i(h_t)
  = sum_lag h_(t-lag) B_(i,lag)
```

です。

runtimeでは積分核を有限和として近似します。

```text
integral K(t,tau)m(tau)d tau
  -> sum_lag m_(t-lag) B_lag
```

## memory部分加群

kernel operatorはmemory部分加群だけに支持を持たなければなりません。

```text
B_(i,lag) = P_memory B_(i,lag) P_memory
```

さらに、次を要求します。

```text
[B_(i,lag), P_j] = 0
B_(i,lag)|M_protected = 0
B_(i,lag)(F^p M) subset F^p M
```

これにより、履歴kernelはObserve、Verify、Ethics、protected部分へ混合しません。

## pathwise Leibniz則

文脈代数要素`a`は、現在切断だけでなく履歴全体へ同時に左作用します。

```text
a . (m_t, h_t) = (a m_t, a h_t)
```

memory kernelは左加群線形なので、

```text
K_i(a h_t) = a K_i(h_t)
```

となります。

したがって、

```text
nabla_i^K(a m_t, a h_t)
  = delta_i(a)m_t + a nabla_i^K(m_t,h_t)
```

が成立します。

## kernel変形

source kernelを`K`とし、shadow変形を`delta K`とします。

```text
K' = K + delta K
```

`delta K`はsource kernel digestへ束縛されます。

変形は候補kernelを生成しますが、source kernelやMemoryOS capsuleを変更しません。

## 非マルコフ性のruntime検証

候補kernelにはlag 1より大きいtermを含めます。

同じ現在切断を固定したまま、古い履歴frameのmemory成分だけを変更し、接続出力が変わることを確認します。

この検査により、candidateが現在状態だけに依存するMarkov写像へ退化していないことを有限fixture上で確認します。

## ゲージ共変性

fiber gauge変換を`g`とします。

```text
m^g = m g^-1
B_(i,lag)^g = g B_(i,lag) g^-1
```

現在切断と全履歴frameへ同じ変換を作用させると、

```text
(nabla_i^K(m,h))^g
  = nabla_i^(K^g)(m^g,h^g)
```

が成立します。

許容ゲージ変換はv0.70から継承した意味射影とauthority filtrationを保存します。

## rollback

kernel rollbackは次の三条件で検証します。

- 代数的復元：`(K + delta K) - delta K = K`
- 構造的復元：module、history、direction、rankのbindingが一致
- 証拠的復元：recovered kernel digestがsource kernel digestと一致

## 外部receipt

次は履歴加群やkernelの要素にしません。

- source history digest
- source kernel digest
- candidate kernel digest
- decision
- validity epoch
- production permission
- execution status

これらはimmutable receiptとして外側から束縛します。

## 権限継承

v0.72は、v0.69で確定した`APPROVE_EVIDENCE`によるproduction適用権を変更しません。

v0.72の候補生成関数がsource履歴を書き換えないことと、承認後にproduction適用権が存在することは別の作用段階です。

## 実装

```text
runtime/kuuos_memory_history_v0_72.py
runtime/kuuos_nonmarkov_memory_kernel_v0_72.py
runtime/kuuos_nonmarkov_memory_connection_v0_72.py
runtime/kuuos_nonmarkov_candidate_validation_v0_72.py
scripts/check_kuuos_nonmarkov_memory_v072.py
formal/KUOS/WORLD/KuuOSNonMarkovMemoryConnectionV0_72.lean
formal/KuuOSFormalV0_72.lean
```

## Lean定理

- `historical_connection_satisfies_pathwise_leibniz`
- `memory_kernel_deformation_preserves_pathwise_leibniz`
- `memory_kernel_difference_is_history_linear`
- `sum_memory_kernels_preserves_filtration`
- `gauge_transform_preserves_memory_kernel_linearity`
- `rollback_memory_kernel_recovers_source`
- `valid_history_candidate_preserves_read_only_sources`

## fail-closed条件

次を拒否します。

- source history digest不一致
- source module digest不一致
- 必須lag frame欠損
- memory部分加群外へのkernel作用
- semantic projector非可換
- protected部分への作用
- authority filtration上昇
- pathwise Leibniz不成立
- ゲージ共変性不成立
- rollback不一致

## 境界

v0.72は有限履歴と有限行列kernelによる局所模型です。

次を主張しません。

- 連続時間積分核をruntimeで完成したこと
- 任意の無限履歴を扱えること
- 有限fixtureが全contextを覆うこと
- memory依存性がtruthを保証すること

## 次段階

自然な次段階は、有限kernel候補catalogからの探索です。

候補選択は、pathwise Leibniz、memory support、filtration、ゲージ不変量、rollbackを満たすkernel同値類上で行います。
