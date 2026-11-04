# GK5CC／Qi v4.47 — 任意有限長・型可変の多変数整数多項式代入鎖と真正CRT自然性

2026年11月4日 JST ／ F112-P94D3GK5CC・Qi v4.47 ／ **独立・Qi定理ともMERGED**

## 1. 正本・exact-source CI・Git tree監査

| 項目 | 独立GK5CC | Qi v4.47 |
|---|---|---|
| 定理PR | [#3110](https://github.com/itakura-hidetoshi/KuuOS/pull/3110) MERGED | [#3111](https://github.com/itakura-hidetoshi/KuuOS/pull/3111) MERGED |
| exact-source HEAD | `8c43d50304ceb5877f8d4a0b2394ec468c88c631` | `c8d1a0c9b97aedc91cef1ef0d3a4c5795e37c135` |
| squash SHA | `8c829c020c6211e1ec1b36fe867509436ea911d5` | `cb702bac382c79c36b0f2eb7c2f3b96b8239db57` |
| source／test-merge／squash tree | `8261494c97bc5a50fac5b328fba237e50591852d` | `b4bc1ce80e68b2deda53482bec0ebf77a7c7ec66` |
| exact-source CI | [#41840895134](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41840895134) | [#41842396869](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41842396869) |
| Strict Lean | **9,313／9,313 SUCCESS** | **10,240／10,240 SUCCESS** |
| Governance | **30／30 SUCCESS** | **30／30 SUCCESS** |
| 新規定理公理監査 | **12定理、sorryAxなし** | **9定理、sorryAxなし** |

- [独立GK5CC Lean4形式証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CCTypedFiniteSubstitutionCRTNaturality.lean)
- [Qi v4.47 Lean4形式証明](../../formal/KUOS/Architecture/QiWuxingGK5CCNorthTypedFiniteChainCRTV4_47.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)

最終Qiマージ後canonical main HEAD：`cb702bac382c79c36b0f2eb7c2f3b96b8239db57`。固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。既存Lean定理ファイルは変更せず、独立とQiの新規ファイル＋公開集約importのみ。

## 2. 独立GK5CC — 任意有限長・型付き代入鎖の真正RingHom構成

元GK5BW／BX／BZ／CA／CBを型付き継承。任意の変数型族`α : Nat → Type u`と、各段の真正整数多変数多項式代入`steps i : α i → MvPolynomial (α (i+1)) Int`を用いる。

```text
nativeGK5CCTypedChainHom steps start length :
  MvPolynomial (α start) Int →+*
  MvPolynomial (α (start + length)) Int
```

長さ0では`RingHom.id`、長さ`length+1`では型付き`nativeGK5CCStepSubstitutionHom (steps (start+length))`を直前までの鎖に合成する。変数の型も個数も途中で変化してよく、同一型への単純な反復写像に退化させない。

これを元の大域`ZMod L_s`と本物の互換局所`R_s`の`MvPolynomial.eval₂Hom`へ合成する。全有限長について、後続1段の大域／局所逐次評価、**CRT環同型の厳密RingHom自然性**、任意有限被覆の大域／局所制限`RingHom`自然性、三段`u⊆t⊆s`の全体`RingHom`可換性が証明された。初期変数を任意非単射`f : σ → α start`で再分類しても三段図式は可換。終端`zs : α(start+length)→Int`は元整数環で代入鎖を評価してから`ZMod L_s`へ射影する値と一致する。法0、空被覆、空変数、負係数、非互いに素を排除しない。

## 3. Qi v4.47 — genuine north signed C60と元F55 Type境界

各段の変数型を`Fin (arity i)`とし、`arity : Nat→Nat`は任意とする。元の`fivefoldGK5BZNorthSignedCoordinates`は各終端変数に、元GK5BQの`nativeGK5BQClearedNumerator d (indices v) values : Int`を符号付きのまま割り当てる。新しい元F55 Typeソースや`natAbs`代理は作らない。

任意有限長の真正代入鎖について、元`Int`評価・大域`ZMod L_s`評価・gcd互換局所CRT Subring評価・CRT環同型・一段／三段被覆制限・任意非単射初期変数再分類を型付きLean定理で接続する。

二つの真正元F55 Type証拠（primitive `P=1`とdouble inverse＋元右単位`P=X²`）は、同じ数値的有限CRT鎖の自然性を満たしても、元original→phi構造的seamの判定はそれぞれ**存在／不存在**となる。既存条件`2≤d`および`L_s ∣ d!`で保証されるCRT零は、元のP92B整数深度多項式についての条件付き算術定理に限定され、任意の外側代入多項式の零を意味しない。数値gluingからF55 Type源、P77等号、P94A四セル、無条件P89反射、普遍GK5AY seam、`W=1→seam`は導かない。

## 4. Lean4修正記録と次研究境界

独立GK5CC初回CI #41840341829 では三段CRT証明の終端で、大域評価と局所互換評価をつなぐ一段の自然性が不足した。全文と既存`nativeGK5BZMultivariableCRTTower_natural`／`nativeGK5BZCRTMvEval_apply`の型を照合し、両定理を連続する`calc`に明示して修正。最終CI #41840895134 で12定理sorryAxなし。Qi v4.47初回CI #41841833634 は整数値の`ZMod`型変換の閉じ括弧が1個不足する構文エラーであり、同一命題・仮定のまま補正しCI #41842396869 で9定理sorryAxなし。いずれも定理の前提弱化を行っていない。

strict 空、独立Kuu→Qi、元F54二Nat・二圏・Blocks、元F55 Type履歴、真正北C60物理gaugeとP89条件付きBadPair境界を別authorityとして維持。追加公理、`sorry`、`admit`、`native_decide`、Gray／GK5BA kitなし。

**次GK5CD（未形式化）：** 任意長鎖を途中で切る分割点の連結・結合則とCRT RingHom自然性を型付き証明へ拡張する。finite-lengthの再帰・局所大域整合から、任意分割の構造的compositionへ進める。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
