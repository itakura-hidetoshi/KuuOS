# WORLD v0.60 四大相転移宣言

## 目的

WORLD v0.59は、地大、水大、火大、風大を非負の読み取り専用診断座標として構成した。

しかし、診断座標が存在することと、相転移が発生したことは同じではない。

WORLD v0.60は、四大相転移を宣言するための証人を、自由エネルギー、スペクトルギャップ、固定点代数の三系統へ分離する。

## 系のデータ

相転移系は実パラメータ`λ`に依存し、次を持つ。

- 四大診断`Q(λ)`。
- 自由エネルギー`F(λ)`。
- 非負スペクトルギャップ`Δ(λ)`。
- 固定点部分代数`A_fix(λ)`。

固定点代数は、実際のvon Neumann固定点代数を受け取れるように、抽象代数の`Subalgebra`として保持する。

## 自由エネルギー証人

臨界値`λc`における自由エネルギー証人を次で定義する。

```text
ContinuousAt F λc
and
not AnalyticAt ℝ F λc
```

この層では、自由エネルギーは連続だが解析性を失う場合を扱う。

単なる不連続関数を、この証人へ自動昇格させない。

自由エネルギー非解析性は、ギャップ閉鎖や固定点代数変化から自動推論しない。

## ギャップ閉鎖証人

臨界値`λc`におけるギャップ閉鎖証人を次で定義する。

```text
ContinuousAt Δ λc
Δ(λc) = 0
and
for every ε > 0,
there exists λ with
0 < |λ - λc| < ε
and
0 < Δ(λ)
```

系全体では`0 ≤ Δ(λ)`を要求する。

したがって、臨界点でゼロとなり、任意に近い穿孔近傍に正のギャップを持つ連続な閉鎖を表す。

ギャップが恒等的にゼロである場合は、この証人を満たさない。

## 固定点代数変化証人

臨界値`λc`における固定点代数変化を局所的に定義する。

任意の`ε > 0`に対して、臨界点の左側と右側に`λL`と`λR`が存在し、次を満たす。

```text
λc - ε < λL < λc < λR < λc + ε
A_fix(λL) ≠ A_fix(λR)
```

これは、離れた二点の代数が異なるだけでは不十分であることを明示する。

臨界点へ任意に近い両側で固定点代数が変化する必要がある。

## 四大座標変化

四大診断は、証明フィールドを除いた座標snapshotへ射影する。

```text
Qcoord(λ)
=
(Earth(λ), Water(λ), Fire(λ), Air(λ))
```

四大座標変化も固定点代数変化と同じ局所両側条件で定義する。

相転移の三証人が成立しても、四大座標が変化しない場合は、四大相転移とは宣言しない。

## 宣言階層

### 相転移候補

次のいずれか一つと四大座標変化がある場合に限り、相転移候補を構成する。

- 自由エネルギー非解析性。
- ギャップ閉鎖。
- 固定点代数変化。

候補は宣言ではない。

### 整合相転移候補

三証人のうち任意の二つと四大座標変化がある場合、整合相転移候補を構成する。

二証人が一致しても、第三証人を暗黙に補わない。

### 四大相転移宣言

厳格な四大相転移宣言は、次の四条件をすべて要求する。

```text
free-energy nonanalyticity
and
spectral-gap closure
and
fixed-point-algebra change
and
four-great-coordinate change
```

Lean構造体は四証人を独立フィールドとして保持する。

宣言から整合候補への忘却写像と、宣言から候補への忘却写像を定義する。

整合候補から候補への忘却写像も定義する。

逆向きの自動昇格写像は定義しない。

## 四大との対応

WORLD v0.60は、三証人を地大、水大、火大、風大へ一対一対応させない。

自由エネルギー非解析性、ギャップ閉鎖、固定点代数変化は、四大座標を宣言するための独立な相転移証人である。

四大座標は相転移後の構造分類を与えるが、単独では相転移を証明しない。

## 非権限境界

```text
single witness != phase-transition declaration
concordant pair != strict declaration
four-great coordinate change != thermodynamic nonanalyticity
spectral-gap closure != free-energy nonanalyticity
fixed-point-algebra change != spectral-gap closure
phase-transition declaration != material ontology
phase-transition declaration != empirical confirmation
phase-transition declaration != execution authority
```

この層は読み取り専用である。

PlanOS objective、ActOS authority、臨床判断、物理実験の代替を生成しない。

## 今後の実現入力

具体的な物理系へ適用するには、次を別途供給する必要がある。

- 熱力学極限で定義された自由エネルギー。
- Hamiltonianまたはtransfer operatorのスペクトルギャップ。
- 力学またはMarkov作用素の固定点代数。
- v0.59四大診断への具体的写像。

有限体積で解析的な自由エネルギーだけを用いて、熱力学的相転移を宣言してはならない。

有限サイズの小さいギャップだけを用いて、ギャップ閉鎖を宣言してはならない。

固定点代数の表現変更だけを用いて、代数自体の変化を宣言してはならない。
