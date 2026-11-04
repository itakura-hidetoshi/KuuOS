# GK5CA／Qi v4.45 — 真正多変数多項式の変数再分類・代入・北C60 CRT自然性

2026年11月4日 JST ／ F112-P94D3GK5CA・Qi v4.45 ／ **独立・Qi両定理MERGED**

## 1. 唯一の正本・exact-source CIとマージ結果

| 項目 | 独立GK5CA | Qi v4.45 |
|---|---|---|
| 定理PR | [#3104](https://github.com/itakura-hidetoshi/KuuOS/pull/3104) MERGED | [#3105](https://github.com/itakura-hidetoshi/KuuOS/pull/3105) MERGED |
| exact-source HEAD | `3fe3d7ece931a13bbdba2ca535e1d8bef0dc7dab` | `1ba2587b15c4aa80e3097c58219978b5109dfd50` |
| squash SHA | `1b8345ce5b5913cdb1cd18165bf776fc7d6bce69` | `7240ee551fbe968e1b439887b949443a55f31513` |
| source/test-merge/squash Git tree | `e2496d9eb72368612c82b0cb8f7a0ae4c1f55843` | `0a25fd7d4acf2c3fb4a1fa0b7823110b6a728780` |
| exact-source CI | [#41832026876](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41832026876) | [#41833223307](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41833223307) |
| Strict Lean | **9,309／9,309 SUCCESS** | **10,236／10,236 SUCCESS** |
| Governance | **30／30 SUCCESS** | **30／30 SUCCESS** |
| 新規公理監査 | **17定理、sorryAxなし** | **15定理、sorryAxなし** |

- [独立GK5CA形式証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CAVariableSubstitutionCRTNaturality.lean)
- [Qi v4.45形式証明](../../formal/KUOS/Architecture/QiWuxingGK5CANorthMvSubstitutionCRTV4_45.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)

全32定理は、固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`でexact-source検証済み。独立GK5CAでは全17定理の`#print axioms`が`propext`、`Classical.choice`、`Quot.sound`のみで、Qi v4.45の15定理も`sorryAx`なし。両PRとも既存Lean定理ファイルを変更せず、新規モジュールと公開集約への追記のみ。

検証・マージ後canonical main HEADは`7240ee551fbe968e1b439887b949443a55f31513`。公開root107は保持し、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2. 独立GK5CA — 任意変数再分類と整数多項式代入のCRT自然性

前段GK5BW／BX／BZの実装により、任意の有限`s`と自然数法系`m`に対し、真正な大域環`ZMod L_s`（`L_s`は`s`上のLCM）、gcd-compatible局所環のSubring`R_s`、CRT環同型`Φ_s : ZMod L_s ≃+* R_s`、被覆制限`q_st`／`ρ_st`、多変数評価RingHomが存在する。

GK5CAは任意の変数型`σ`, `τ`, `υ`を使い、非単射も許す`f:σ→τ`、任意の真正多項式代入`h:σ→MvPolynomial τ Int`について、固定mathlibの`MvPolynomial.eval₂Hom_rename`, `eval₂Hom_bind₁`, `bind₁_rename`, `bind₁_bind₁`と先行GK5BZ自然性を型付き接続した。

```text
eval_x(rename_f P) = eval_(x ∘ f) P
eval_x(bind_h P)   = eval_(i ↦ eval_x(h i)) P
Φ_s(eval_x(bind_h P)) = eval_(i ↦ Φ_s(eval_x(h i))) P
```

さらに被覆包含`u⊆t⊆s`に対して、最大被覆で代入・評価・CRT合成し二回制限する経路と、最小被覆へ変数を直接制限して代入多項式の値を評価・CRT合成する経路が一致する。任意符号付き整数変数`zs:τ→Int`を代入したとき、整数環上で先に多項式代入・評価した後で剰余環へ写す経路とも一致。負係数、非互いに素法、法0、空被覆、`Fin 0`、非単射変数写像を排除しない。

## 3. Qi v4.45 — original signed GK5BQ numeratorと真正北C60

`fivefoldGK5BZNorthSignedCoordinates n d indices values : Fin n → Int`の各座標は、元GK5BQで証明済みの真正符号付き整数分子`nativeGK5BQClearedNumerator d (indices v) values`そのもの。任意の`f : Fin m → Fin n`による再分類、および任意の`h : Fin m → MvPolynomial (Fin n) Int`による多項式代入について、同一元値の整数評価、実際の大域ZMod評価、真正compatible-local subring評価、CRT環同型、有限一段・三段被覆の可換性をLean4で検証した。

二つの真正別F55 Type証拠、primitive `P=1`とdouble inverse＋元右単位 `P=X²`は、どちらも同じ多変数代入数値CRT三段塔を満たす。しかし`Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell)`と`¬ Nonempty (nativeGK5AZSeamAt fivefoldGK5BFNorthDoubleInverseRightUnit)`は併記して区別する。後者を数値合同性から復元したり、前者を普遍化したりしない。既存条件`2≤d`、`L_s ∣ d!`は二つの元F55 witnessについてのこの統合定理の明示的仮定である。

**authority境界**：CRTによる数値的局所・大域gluingは、新たな元F55 Type source、P77商類等号、P94A四セル、P89無条件反射、普遍GK5AY seam、`W=1→seam`を意味しない。元F54二Nat・二圏・Blocks、元F55 Type履歴、北C60物理gauge、条件付きBadPair障害は既存の独立証拠のまま。

## 4. 修正・公開境界および次研究

固定mathlibの真正`rename`／`bind₁`の型とGK5BZ依存定義を全体照合してから実装。両PRの初回exact-source CIにおいてコンパイルと独立公理監査が成功したため、エラー回避のための定理命題・仮定の弱化は行っていない。変更Leanソースに`sorry`、`admit`、追加公理、`native_decide`なし。strict 空、独立Kuu→Qi、append-only、同一root107、固定Lean/mathlib、保護PR #1558 Draft/OPEN/未マージを維持し、Gray／GK5BA kitを追加しない。

次GK5CB（未形式化）では、代入の結合、変数系と被覆系の二方向自然性、original F55 structural obstructionとのauthority分離を一段強化する余地を調べる。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
