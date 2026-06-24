# WORLD Kū Vacuum Central Reference State v0.54

## 位置づけ

v0.54 は、完成OS Hilbert空間上の真空を、WORLD数学サイドカーの**中心基準状態**として明示する。

この真空は、「空」の解析的表現に限定しない。

同じ真空ベクトルと真空状態から、反射陽性、真空相関、モジュラー理論、相対エントロピー、Petz回復、励起状態を一つの解析経路へ接続する。

```text
OS reflection-positive form
→ completed Hilbert vacuum Ω_Kū
→ central reference state ω_Kū
→ vacuum n-point correlations
→ modular reference state
→ Araki relative entropy from ω_Kū
→ Petz recovery preserving ω_Kū
→ excitation vectors π(a)Ω_Kū
→ excited states ω_a
```

## 中心基準状態

中心基準状態は次である。

```text
ω_Kū(a) = <Ω_Kū, π(a) Ω_Kū>
```

v0.54では、v0.33のモジュラー基準状態を、この真空状態と完全に同定する。

```text
referenceState(a) = ω_Kū(a)
```

したがって、モジュラー不変性、KMS境界、相対モジュラー流、Connes cocycle、Araki相対エントロピー、Petz回復は、すべて同じ基準状態を参照する。

## 反射陽性との接続

正時間observableのOS形式を、中心基準状態の二点相関へ束縛する。

```text
(F,G)_OS = ω_Kū(ι(F)* ι(G))
```

ここで `ι` は正時間observableからWORLD observable代数への写像である。

この束縛により、反射陽性は中心基準状態の二点相関の非負性として読める。

```text
Re ω_Kū(ι(F)* ι(F)) >= 0
```

## 真空相関

順序付きn点相関を次で定義する。

```text
W_n(a₁,...,aₙ) = ω_Kū(a₁ ... aₙ)
```

二点相関は次である。

```text
W₂(a,b) = ω_Kū(a* b)
```

空リスト相関は規格化により1となる。

```text
W₀ = ω_Kū(1) = 1
```

## モジュラー理論

中心基準状態はモジュラー流に対して不変である。

```text
ω_Kū(σ_t(a)) = ω_Kū(a)
```

真空ベクトルもモジュラーユニタリで不変である。

```text
U_mod(t) Ω_Kū = Ω_Kū
```

モジュラー時間と物理時間は同一視しない。

物理時間についても、既存v0.49の別個の不変性を保持する。

```text
U_phys(t) Ω_Kū = Ω_Kū
```

## 相対エントロピー

v0.34の局所および大域Araki相対エントロピーを、中心真空状態に対する相対量として読む。

```text
S_region(ρ || ω_Kū)
S_global(ρ || ω_Kū)
```

Leanは次の有限順序結果を再利用する。

```text
0 <= S_region
S_region <= S_global
region₁ <= region₂ → S_region₁ <= S_region₂
```

Araki公式、相対モジュラー対数、下半連続性、一般UCPデータ処理は外部解析receiptのままである。

## Petz回復

v0.35の回復チャネルについて、中心真空状態の厳密回復を導く。

```text
ω_Kū(R_Petz(Φ(a))) = ω_Kū(a)
```

さらに、相対エントロピー等号を中心真空基準の等号として登録する。

```text
S_coarse(ρ || ω_Kū) = S_global(ρ || ω_Kū)
```

回復写像は実行権限、WORLD更新、真理権限を与えない。

## 励起状態

observable `a` が生成する励起ベクトルを次で定義する。

```text
|a> = π(a) Ω_Kū
```

その内積は真空二点相関に一致する。

```text
<a|b> = ω_Kū(a* b)
```

単位observableの励起は真空そのものである。

```text
|1> = Ω_Kū
```

非零重みを持つ励起について、正規化励起状態候補を次で定義する。

```text
ω_a(b) = ω_Kū(a* b a) / ω_Kū(a* a)
```

この励起状態は、新しいWORLDの生成や別世界へのcollapseを意味しない。

## 共変性

励起ベクトルはモジュラー時間と物理時間の双方で共変に移る。

```text
U_mod(t)|a> = |σ_t(a)>
U_phys(t)|a> = |α_t(a)>
```

ただし、二つの時間発展は分離したままである。

## Lean直接面

Leanは次を直接検証する。

- 中心基準状態の規格化、正性、ゲージ不変性。
- OS形式と中心二点相関の完全束縛。
- 反射陽性から中心二点相関非負性への移送。
- 空相関と一要素相関。
- モジュラー基準状態と真空状態の完全一致。
- 中心基準状態のモジュラー不変性。
- 励起ベクトル内積と二点相関の一致。
- 単位励起と真空の一致。
- モジュラー時間および物理時間に対する励起共変性。
- 励起状態の規格化。
- 真空基準相対エントロピーの非負性と局所データ処理。
- Petz回復による中心真空状態の厳密回復。
- 相対エントロピー等号。
- runtime非権限境界と表現境界。

## 外部解析receipt

次は外部解析receiptとして残す。

- OS商空間とHilbert完成の実構成。
- 真空相関の連続性と分布的拡張。
- 励起軌道の稠密性。
- 励起状態の正性および正規性の一般定理。
- Araki相対エントロピーが真空基準であることの解析的同定。
- Petz回復写像の解析公式と完全正性。
- モジュラー中心性の物理的実現。

## 固定境界

```text
central reference state != exact WORLD
central reference state != truth authority
central reference state != control objective
Kū != zero vector
WORLD != vacuum vector
vacuum sector need not be one-dimensional
excitation state != new WORLD
Petz recovery != execution authority
modular time != physical time
validation != external mathematical acceptance
```

v0.54は読み取り専用数学サイドカーである。

runtimeはOS完成、真空相関、モジュラー流、相対エントロピー、Petz写像、励起状態を計算または実行しない。
