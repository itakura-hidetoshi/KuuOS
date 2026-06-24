# WORLD v0.56 Araki Hessian physical realization

## 対象

WORLD v0.56は、v0.55の真空情報幾何を、無限次元標準形上のAraki指数弧とOsterwalder–Schrader物理Hilbert空間へ接続する。

対象は、σ有限von Neumann代数の標準形、忠実正規な真空基準状態、有界自己共役生成子による指数弧、完成複素Hilbert空間、OS反射陽性から得られる正時間代表元である。

任意の無界生成子は対象に含めない。

## 解析経路

有界生成子 h と k が作る指数弧を γ_t と η_s とする。

Araki相対エントロピーの第一変分を次で表す。

```text
∂t S(η_s || γ_t)|t=0 = ω(h) - η_s(h)
```

期待値応答を次で表す。

```text
d/ds η_s(h)|s=0 = BKM(k,h)
```

したがって、負の混合二階微分は次になる。

```text
-∂s∂t S(η_s || γ_t)|s=t=0 = BKM(k,h)
```

この射程は、Jan Naudts, Exponential arcs in manifolds of quantum states, arXiv:2209.12761, Section 14に対応する。

## Lean微分核

`ArakiBoundedExponentialArcKernel` は、指数弧上の期待値関数と基準点微分を保持する。

第一変分を次で定義する。

```text
F_{k,h}(s) = ω(h) - η_s(h)
```

Araki Hessianを次で定義する。

```text
H_Araki(k,h) = - deriv F_{k,h}(0)
```

Leanは `HasDerivAt.const_sub` と `HasDerivAt.deriv` を用いて次を証明する。

```text
H_Araki(k,h) = BKM(k,h)
```

BKM pairingの対称性と非負性から、Hessianの対称性と対角非負性も導く。

## 真空量子Fisher計量

有界生成子 h をv0.55の接ベクトル u_h へ写す。

```text
BKM(k,h) = g_QF,θ_Kū(u_k,u_h)
```

これにより次が成立する。

```text
H_Araki(k,h)
= BKM(k,h)
= g_QF,θ_Kū(u_k,u_h)
= Hess_θ_Kū S_Araki(u_k,u_h)
```

## Hilbert空間上の励起

接観測量を A_h とし、励起を次で定義する。

```text
Ψ_h = π(A_h) Ω_Kū
```

v0.55の真空励起Gram同定から次を得る。

```text
H_Araki(k,h) = Re ⟨Ψ_k, Ψ_h⟩
```

## OS反射形式

各生成子に正時間観測量代表元 a_h^+ を対応させる。

```text
U_OS [a_h^+] = Ψ_h
```

OS内積の定義から次をLeanで導く。

```text
H_Araki(k,h) = Re E_OS(a_k^+,a_h^+)
```

対角成分は反射陽性により非負である。

## 無限次元性

物理Hilbert担体には次を型として要求する。

```text
InfiniteDimensional ℂ H_phys
```

このbridgeは有限行列状態空間への縮約ではない。

## 証明済み範囲

Leanが直接証明する範囲は、第一変分の微分、負の混合HessianとBKM pairingの一致、Hessianの対称性と非負性、量子Fisher計量への輸送、Araki Hessian shadowへの輸送、完成Hilbert励起Gram形式への輸送、OS reflection form実部への輸送である。

## 残る基礎形式化

第一原理からの完全形式化には、von Neumann代数の標準形、自然正錐、相対Tomita作用素、相対モジュラー作用素、非有界作用素の対数、Araki摂動理論、指数弧の存在とFréchet微分、Kubo–Mori変換の積分表示、OS再構成定理の基礎実装が必要である。

v0.56は、有界生成子Hessian同定後の情報幾何と物理Hilbert空間への接続をLean定理として閉じる。

## 固定境界

```text
bounded-generator theorem != arbitrary unbounded-generator theorem
infinite-dimensional carrier != full operator-algebra foundation
physical realization != WORLD identity
Araki Hessian != truth authority
BKM metric != ontology
OS representative != execution authority
modular time != physical time
```
