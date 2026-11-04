# GK5CB／Qi v4.46 — 二段真正多変数多項式代入・有限非互いに素CRT自然性

2026年11月4日 JST ／ F112-P94D3GK5CB・Qi v4.46 ／ **独立・Qi定理ともMERGED**

## 1. 唯一の正本・exact-source検証

| 項目 | 独立GK5CB | Qi v4.46 |
|---|---|---|
| 定理PR | [#3107](https://github.com/itakura-hidetoshi/KuuOS/pull/3107) MERGED | [#3108](https://github.com/itakura-hidetoshi/KuuOS/pull/3108) MERGED |
| exact-source HEAD | `01ec5c3e0d57370d231ef939e2daa25974070149` | `3fbecabfd9eab4c59d93c675fc0cde335c2b01c1` |
| squash SHA | `b7096c3c43fa70d00fc21bc307019e05a896b81a` | `38f8ffb2f10e4a2e96fc6f5fb7f13fe373f63236` |
| source/test-merge/squash Git tree | `43d1293a76eb775a5d35eb77f3fdb9ee0a74c556` | `0888ae38254aa9bf41e5757b80748620f1e2c330` |
| exact-source CI | [#41835862482](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41835862482) | [#41836760194](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41836760194) |
| Strict Lean | **9,311／9,311 SUCCESS** | **10,238／10,238 SUCCESS** |
| Governance | **30／30 SUCCESS** | **30／30 SUCCESS** |
| 新規定理公理監査 | **17定理、sorryAxなし** | **13定理、sorryAxなし** |
| 新規ソース | 506行 | 442行 |

- [独立GK5CB Lean4形式証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CBIteratedSubstitutionCRTTower.lean)
- [Qi v4.46 Lean4形式証明](../../formal/KUOS/Architecture/QiWuxingGK5CBNorthDoubleSubstitutionCRTV4_46.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)

最終Qi定理マージ後main HEADは`38f8ffb2f10e4a2e96fc6f5fb7f13fe373f63236`。Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`のexact-source検証で、独立17定理・Qi13定理の`#print axioms`に`sorryAx`はない。Leanジョブは全件SUCCESS。Git treeは両PRでsource/test-merge/squash一致。既存Lean定理ファイルは不変更で、新規モジュールと公開集約importだけを追加した。

## 2. 独立GK5CB — 二段代入の厳密なRingHom・CRT自然性

前段GK5BW（真正一般有限非互いに素CRT環同型`Φ_s: ZMod L_s ≃+* R_s`）、GK5BX（`q_{s,t}`、`ρ_{s,t}`の恒等・合成・CRT自然性）、GK5BZ（`MvPolynomial σ Int`大域／局所評価RingHom）、GK5CA（任意変数`rename`と多項式`bind₁`の自然性）をすべて型付き継承。

任意の`h:σ→MvPolynomial τ Int`, `k:τ→MvPolynomial υ Int`について、固定mathlibの`MvPolynomial.bind₁_comp_bind₁`／`bind₁_bind₁`・`eval₂Hom_bind₁`を接続し、実際の代入RingHomと評価RingHomの合成を証明する。

```text
bind_k(bind_h P) = bind_(i ↦ bind_k(h i)) P
ev_x(bind_k(bind_h P))
  = ev_(i ↦ ev_(j ↦ ev_x(k j))(h i)) P
CRT_u(q_su(ev_x(bind_k(bind_h P))))
  = ev_(i ↦ ev_(j ↦ ev_(CRT_u ∘ q_su ∘ x)(k j))(h i)) P
```

最後の等式は`u⊆t⊆s`の二段制限と同じ結果になる。さらに変数`f:σ→τ`（**非単射も含む**）を最初に再分類した場合も、`h∘f`に対応する局所多段代入と厳密に一致することを形式化。任意の符号付き整数変数`zs:υ→Int`について、整数環で先に二段代入・評価したのち剰余へ送る経路とも一致する。法0・非互いに素法・空被覆・空変数集合・負係数に対応し、次数・互いに素性・変数単射性は要求しない。

## 3. Qi v4.46 — 元GK5BQ真正signed numeratorを使う北C60接続

元の`fivefoldGK5BZNorthSignedCoordinates n d indices values : Fin n → Int`の各値は`nativeGK5BQClearedNumerator d (indices v) values`そのものであり、符号を落とさない。任意`Fin m → MvPolynomial (Fin p) Int`、`Fin p → MvPolynomial (Fin n) Int`の二段代入に対し、元`Int`評価、大域`ZMod L_s`、真正compatible-local Subring、RingHom自然性、三段`u⊆t⊆s` CRT塔、任意の非単射`Fin m→Fin r`再分類を統合する。

二つのTRUE ORIGINAL F55 Type証拠を区別する：
- primitive P=1：`Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell)`。
- double inverse＋元右単位P=X²：`¬ Nonempty (nativeGK5AZSeamAt fivefoldGK5BFNorthDoubleInverseRightUnit)`。

両者とも元数値的signed CRT代入塔は一致して整合するが、**Type-valued original→phi seam verdictは対立したまま**。既存条件`2≤d`, `L_s ∣ d!`の下での算術CRT零は、これまで証明済みの元P92B整数深度多項式にのみ適用する。任意の外側多変数多項式が零になるとは主張しない。数値gluingは新たな元F55 Type source、P77商類等号、P94A 4-cell、P89無条件反射、普遍GK5AY seam、`W=1→seam`を導かない。

## 4. 公開・依存・次研究

新規ソース全文と実際のGK5BW/BX/BZ/CA宣言、固定mathlibの`MvPolynomial`演算を使用してコンパイルした。独立・Qiとも初回exact-source CIでビルド・公理監査成功、命題の弱化なし。strict 空／独立Kuu→Qi、元F54二Nat／二圏／Blocks、元F55 Type値証拠履歴、真正北C60物理gaugeと条件付きP89障害を別authorityとして保持する。公開root107、保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft/open/unmergedを維持。Gray/GK5BA kitや追加公理/sorry/admit/native_decideを導入しない。

次GK5CC（未形式化）では、任意有限長の代入鎖に対する評価の結合自然性と同時被覆CRT図式を一般化し、元F55 Type証拠の非復元境界を維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
