# KuuOS Qi Wuxing Generation–Control Coherence v2.6

## 位置づけ

この層は `Qi Yin–Yang Wuxing Fibonacci History Geometry v2.5` の上に、五行の生克方向、作用強度、履歴保持、composition coherence を加える加法的 architecture layer である。

v2.5 の固定境界を維持する。

- 五行は五つの固定物質ではなく `Z5` 上の関係的位相である。
- 位相が戻っても履歴は戻らない。
- Fibonacci 履歴係数は気の量、病勢、治療量ではない。
- 黄金比は臨床閾値ではない。
- 古典五行説を `SU(2)_3`、anyon、物理ゲージ理論と同一視しない。

v2.6 ではさらに、

```text
相生 = +1
相克 = +2
相侮 = -2
母   = -1
子   = +1
```

を `Z5` 上の関係方向として与える。

## 1. 生克の Z5 作用

五相を従来通り

```text
0 = 木
1 = 火
2 = 土
3 = 金
4 = 水
```

とする。

相生を `S`、相克を `K` とすると位相上は

```text
S(p) = p + 1 mod 5
K(p) = p + 2 mod 5
```

である。

したがって純粋な位相射影では

```text
K(p) = S(S(p))
```

となる。

しかし、これは「相克という一つの相互作用イベント」と「相生を二回経験した過程」が同一だという意味ではない。

## 2. 位相変位と履歴イベント数を分離する

v2.6 の履歴-aware shift は概念的に

```text
shift = (phase_delta, history_event_count)
```

である。

canonical relation は次のように置く。

```text
相生       = (+1, 1)
相克       = (+2, 1)
相侮       = (-2, 1)
母方向     = (-1, 1)
子方向     = (+1, 1)
```

このため、

```text
phase(相克) = phase(相生 + 相生)
```

だが、

```text
history_events(相克) = 1
history_events(相生 + 相生) = 2
```

であり、full shift は一致しない。

これは v2.5 の中心原理

```text
同じ相へ到達すること != 同じ履歴を持つこと
```

を生克へ拡張したものである。

## 3. 相侮は負の強度ではない

相侮は相克の逆向きの位相関係として

```text
W(p) = p - 2 mod 5
```

と置く。

したがって

```text
W(K(p)) = p
K(W(p)) = p
```

である。

ただし phase が戻っても history は消えない。

相克一回の後に相侮一回が起きた場合、位相は戻るが Fibonacci 履歴は二つの interaction event を保持する。

```text
phase:   p -> p+2 -> p
history: h -> advance(h) -> advance^2(h)
```

このため「逆作用が起きたから過去が取り消された」とは解釈しない。

## 4. 強度

作用強度は非負実数

```text
strength in R_{>=0}
```

として別に保持する。

明示的に与えた nominal strength `kappa` に対して、actual strength `a` を

```text
a < kappa   : under
 a = kappa   : balanced
 kappa < a   : over
```

と分類する。

ここで `kappa` はモデル内で明示的に与える比較基準であり、人体・病態・治療に対する普遍的閾値ではない。

### 相乗

相乗は新しい第六の方向ではなく、

```text
相克方向 + excessive strength
```

として定義する。

すなわち interaction `I` が

```text
relation(I) = control
nominal < strength(I)
```

を満たすとき structural overacting control と呼ぶ。

これは臨床診断を自動的に与えない。

### 相侮との区別

相侮は

```text
relation = insult (-2)
```

であり、相克の過剰強度ではない。

よって

```text
相乗 = direction +2, excessive strength
相侮 = direction -2
```

を明確に分離する。

## 5. Fibonacci 履歴

v2.5 の

```text
tau^2 = 1 + tau
(resolved, active) -> (active, resolved + active)
```

をそのまま再利用する。

v2.6 では位相変位の大きさと履歴イベント数を分ける。

相克は位相を二つ進めるが interaction event としては一回なので、history は一段だけ進む。

一方、相生を二回行えば history は二段進む。

したがって、位相の coarse projection だけでは区別できない二つの過程を history fibre が区別する。

## 6. coherence

history-aware shift を

```text
sigma = (delta_phase, n_history)
```

とし、二つの shift の合成を成分ごとの加法

```text
sigma + tau
```

とする。

状態作用を `A_sigma` とすると、v2.6 の中心 coherence は

```text
A_(sigma + tau)(x) = A_tau(A_sigma(x))
```

である。

位相側では `Z5` の加法結合則、履歴側では

```text
advance^(m+n)(h) = advance^n(advance^m(h))
```

によって成立する。

この等式を Lean/Mathlib で証明する。

## 7. 「中」の位置づけ

v2.6 では architecture 上の「中」を五相の一つの実体として追加しない。

特に

```text
中 = 土という固定実体
```

とは定義しない。

ここでの「中」は、異なる phase/history decomposition と interaction composition が矛盾なく貼り合うこと、すなわち

```text
coherence / compatibility
```

として読む。

土は `Z5` の phase index `2` として残る。

coherence は phase ではなく、作用全体が満たす性質である。

## 8. 数理的に証明するもの

formal module:

```text
formal/KUOS/Architecture/QiWuxingGenerationControlCoherenceV2_6.lean
```

では少なくとも次を constructive に閉じる。

1. `generationPhase (generationPhase p) = controlPhase p`
2. `insultPhase (controlPhase p) = p`
3. `controlPhase (insultPhase p) = p`
4. 母子 `-1/+1` の phase inverse
5. Fibonacci history iteration の加法則
6. history-aware shift の composition coherence
7. 相克と相生二回は phase projection が等しい
8. 相克と相生二回は full history-aware shift として異なる
9. 相克→相侮で phase は戻るが history は二段進む
10. nonnegative strength の under/balanced/over trichotomy
11. 相乗 = 相克 + excessive strength
12. 相侮は相乗とは別 relation
13. authority/reification boundary receipt

## 9. 固定境界

この層から次を推論してはならない。

```text
五行 = 五つの物質
土 = 普遍的・実体的な中
相克 +2 = 相生二回という同一の時間過程
逆方向作用 = 履歴消去
強度 = 気の量
nominal strength = 臨床閾値
相乗判定 = 臨床診断
古典五行 = SU(2)_3
古典五行 = 物理 Yang-Mills gauge theory
人体に Fibonacci anyon が存在する
runtime receipt = WORLD adoption
formal compilation = external theorem acceptance
validation = truth
selection = execution
```

## 10. 次の安全な拡張

v2.6 の次に進む場合は、まずこの relation/strength/history/coherence 層を保ったまま加法的に次を検討する。

- relation ごとの strength transport law
- normal range を一点ではなく interval/band とする一般化
- interaction graph ではなく groupoid/action としての source/target 明示
- observation-dependent strength estimate と latent strength の分離
- refinement/cross-scale compatibility
- 臓腑・六経・気血津液等への写像は別 adapter とし、同一視しない

特に、v2.6 の strength は分類値であり、未検証の物理・生物・臨床 dynamics を暗黙に導入しない。
