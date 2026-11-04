# GK5BZ／Qi v4.44 — 真正多変数整数多項式の有限CRT自然性・北C60での型付き接続

2026年11月4日 JST ／ F112-P94D3GK5BZ・Qi v4.44 ／ **独立・Qi両定理MERGED**

## 1. 唯一の正本とexact-source検証

| 項目 | 独立GK5BZ | Qi v4.44 |
|---|---|---|
| 定理PR | [#3101](https://github.com/itakura-hidetoshi/KuuOS/pull/3101) MERGED | [#3102](https://github.com/itakura-hidetoshi/KuuOS/pull/3102) MERGED |
| exact-source HEAD | `08fe86d88477622f360a69514d3ad96ee76c4ec9` | `a944470a2724324380877214329378fc2e2b1dc9` |
| squash SHA | `cd4556e78ac1155d212f2ef288ca708ec4f2d4e6` | `76d524112a5fa70654d4a74f96eead4268465e05` |
| source／test-merge／squash Git tree | `2ffc830f6163019a0921936615f7221dfd19bc63` | `71ca2eedf11015f40260fbdf94899be2bf2f4121` |
| exact-source CI | [#41820694348](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41820694348) | [#41822401269](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41822401269) |
| Strict Lean | **9,307／9,307 SUCCESS** | **10,234／10,234 SUCCESS** |
| Governance | **30／30 SUCCESS** | **30／30 SUCCESS** |
| 公理監査 | **新規16定理、sorryAxなし** | **新規12定理、sorryAxなし** |
| 変更Lean warning/error | **0／0** | **0／0** |

- [独立GK5BZ Lean4](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BZMultivariableCRTNaturality.lean)
- [Qi v4.44 Lean4](../../formal/KUOS/Architecture/QiWuxingGK5BZNorthMultivariableCRTV4_44.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)

検証・マージ後canonical main HEAD：`76d524112a5fa70654d4a74f96eead4268465e05`。公開root107、固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。既存Lean定理ファイルは不変更で、新規モジュールと公開importだけをappend-only追加。

## 2. 独立GK5BZ — 多変数整数多項式・真正有限CRT環同型の自然性

前段GK5BWで、任意有限添字集合`s`、任意自然数法`mᵢ`、その`Lₛ=Finset.lcm s m`に対して、元のgcd重なりで互換な局所ZMod依存積のSubring`Rₛ`と大域`ZMod Lₛ`の**真正環同型**`Φₛ : ZMod Lₛ ≃+* Rₛ`を証明済み。GK5BXは被覆包含`u⊆t⊆s`に沿う大域制限`qₛₜ`、局所制限`ρₛₜ`についてRingHomの恒等・合成・自然性を証明した。GK5BYは一変数`Polynomial Int`の評価にこれらを接続した。

GK5BZでは任意の変数型`σ`に対する**真正`MvPolynomial σ Int`**を使う。具体的な有限変数は`σ=Fin n`であり、`n=0`も含む。固定mathlib `MvPolynomial.eval₂Hom`と`MvPolynomial.ringHom_ext`から大域・互換局所の双方へ真正な多変数評価`RingHom`を構成し、加法・乗法、係数・変数を保持する。

```text
Φₛ (P(xs)) = P(Φₛ ∘ xs)
qₛₜ (P(xs)) = P(qₛₜ ∘ xs)
ρₛₜ (P(as)) = P(ρₛₜ ∘ as)
```

これらを**環準同型の等式として**証明し、三段被覆`u⊆t⊆s`について二段制限・直接制限・CRT再合成が可換となる定理も形式化した。任意の元符号付き整数変数`zs:σ→Int`について、最初に整数環上で多変数評価してから`ZMod Lₛ`へ射影する操作と、各整数を射影後に多変数評価する操作は同値。有限変数`Fin n`の系も含む。

互いに素性・非零性・正値・支配的局所法・非空被覆・多項式次数・階乗整除は、これらの多変数自然性の前提ではない。`ZMod 0 = ℤ`および空の変数集合・空の被覆も含む。

### Lean4修正記録

初回Leanエラーは`MvPolynomial.ringHom_ext`の`C`／`X`ゴールで、評価・合成写像の簡約が不足していた。固定mathlibの`MvPolynomial.eval₂Hom_C`／`eval₂Hom_X'`／`RingHom.comp_apply`を使って明示展開した。最後の三段図式の不要な`congr 1`を、既証明等式に対する`congrArg`へ修正。中間のCI選別成果物欠落は定理の数学的障害ではなく、次ランで選別を成功させてLeanを再検証した。新規有限変数の符号付き評価系も追加し、最終CIで新規16定理すべて`sorryAx`なし。定理の前提や結論を弱めず修正した。

## 3. Qi v4.44 — 真正北C60の元符号付き整数多変数値とF55の境界

元GK5BQの**真正符号付き整数分子**`N(d,j,v):Int`を、それぞれ独立の有限変数`i:Fin n`に対して`N(d,indices(i),values)`として代入する。任意の`Q:MvPolynomial (Fin n) Int`をこの元値に評価した結果と、`ZMod Lₛ`上での多変数評価およびGK5BWの互換局所剰余Subringでの評価は一致する。加法・乗法、任意一段・二段被覆制限も真正Lean等式で成立。絶対値代理`natAbs`は使わない。

実際の元F55 Type証拠は、primitive原証拠（元P92B整数多項式値`P=1`）と、double inverse＋F55右単位の別証拠（元P92B整数多項式値`P=X²`）をそれぞれ保持する。両者とも数値的な有限多変数CRT自然性を持ち、既証明の**明示的条件`2≤d`・`Lₛ∣d!`**の下で、部分被覆`u`の元整数深度多項式のCRT零証明書も共有する。しかし元original→phiの**構造的seamは前者で存在、後者で不存在**。同じ型付き定理でこのobstructionを区別して保持する。

重要：最後のCRT零は既存の**元P92B整数深度多項式**についての条件付き定理である。任意の外側多変数多項式`Q`が零になるとは主張しない。また数値的多変数gluingは元F55 Type証拠やP77商類等号、P94A四セル、GK5AY全域seam、P89無条件反射、`W=1→seam`を再構成しない。元F54二Nat・二圏・Blocks、元F55 Type値履歴、真正第五Dart北C60物理gauge、条件付きP89障害を別authorityとして維持する。

## 4. 次段階（研究計画、未形式化）

**GK5CA（仮称）**：任意の有限変数集合`Fin n`について、変数再分類・代入写像とCRT多変数評価の整合性（`MvPolynomial`の変数置換と制限・評価の可換性）を型付き自然変換として強化する。数値的descentの関係を保ちながら、元F55 Type-valued sourceや高次セルへの無条件持上げを主張しない。

strict 空／独立Kuu→Qi、append-only、公開root107、固定Lean/mathlib、保護PR #1558 Draft／OPEN／未マージを保持。Gray・GK5BA kitを追加しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
