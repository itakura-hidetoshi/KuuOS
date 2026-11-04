# GK5BY／Qi v4.43 — 真正整数多項式評価・有限CRT環同型の自然性

2026年11月4日 JST ／ F112-P94D3GK5BY・Qi v4.43 ／ **独立・Qi両定理MERGED**

## 1. 唯一の定理正本とexact-source CI

| 項目 | 独立GK5BY | Qi v4.43 |
|---|---|---|
| 定理PR | [#3098](https://github.com/itakura-hidetoshi/KuuOS/pull/3098) MERGED | [#3099](https://github.com/itakura-hidetoshi/KuuOS/pull/3099) MERGED |
| exact-source HEAD | `5e327cff2ad144f303855d551f39532c245d8ae7` | `3c91cde9599ce53f2dc7e26c7b6089977ae87644` |
| squash SHA | `831c30e653d7326ccf37013b9728c57d8b3e503e` | `08248fccce41ae6de5d14c4f8cc85e850d50952f` |
| source／test-merge／squash Git tree | `c69b1d16b66972132bc40c50c8669a4e2c73a411` | `c76a7deb63c0c796b234d1c0f88981f2065af5c1` |
| exact-source CI | [#41815719110](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41815719110) | [#41816570697](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41816570697) |
| Strict Lean | **9,305/9,305 SUCCESS** | **10,232/10,232 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規 `#print axioms` | **13定理、sorryAxなし** | **11定理、sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立GK5BY Lean4](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BYIntPolynomialCRTNaturality.lean)
- [Qi v4.43 Lean4](../../formal/KUOS/Architecture/QiWuxingGK5BYNorthIntPolynomialCRTV4_43.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)：各新規Leanモジュールをappend-only import。既存Lean定理ファイルの変更なし。

定理マージ後canonical main：`08248fccce41ae6de5d14c4f8cc85e850d50952f`。固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107を維持。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2. 独立GK5BY — 任意の真正整数係数多項式のCRT自然性

前段GK5BWは任意有限被覆`s`・任意自然数法`m_i`に対し、`L_s=Finset.lcm s m`として、大域`ZMod L_s`と`gcd`重なりで互換な局所剰余族の真正`Subring`、`R_s`の間に環同型`Φ_s:ZMod L_s ≃+* R_s`を構成。GK5BXでは包含`u⊆t⊆s`に関する大域制限`q_st`・局所制限`ρ_st`の恒等／合成、`Φ`の自然性・逆自然性・三段塔をLean4で証明済み。

GK5BYでは**任意の真正`P:Polynomial Int`**に拡張し、各大域・局所環で`Polynomial.eval₂RingHom (Int.castRingHom _) x`を構成した。これにより各`x`について`P↦P(x)`は真正な**`RingHom`**であり、加法・乗法を保存する。固定mathlibの実定理`Polynomial.ringHom_eval₂_intCastRingHom`により、任意の有限被覆制限とCRT環同型について**`RingHom`同士の等式**：

```text
q_st(P(x)) = P(q_st(x))
ρ_st(P(a)) = P(ρ_st(a))
Φ_s(P(x)) = P(Φ_s(x))
```

を形式証明した。さらに`u⊆t⊆s`の二段制限を直接制限と比較し、大域・局所の各多項式評価塔およびCRT環同型全体の三段可換性を証明した。

元の任意の**符号付き整数**`z:Int`を先に`Polynomial Int`で評価してから`ZMod L_s`へ移した結果と、`ZMod L_s`内で`P`を評価する結果は**文字どおり等しい**。法0`ZMod 0=ℤ`・空被覆・非coprime・負係数を含み、次数上界・`L_s|d!`・支配的局所法などの仮定は不要。

### CI修正記録

最初のCIは最後の三段自然性の`rw`方向だけが逆で、書換え対象`Φ_t(q_st x)`が目標内に見つからないLean4 elaboration失敗だった。既存GK5BXの自然性`Φ_t(q_st x)=ρ_st(Φ_s x)`を逆向きに適用する`rw [← ...]`へ最小修正した。全358行の新規Leanソース、依存定義、固定mathlibの該当APIを照合し、数学的命題・前提条件・結論を変更せず最終CIで13定理全部`sorryAx`なし。

## 3. Qi v4.43 — 真正北C60の元符号付き整数numeratorでの多項式自然性

Qi v4.43は元GK5BQの**同一の真正符号付き整数分子**`nativeGK5BQClearedNumerator d j values : Int`を保持し、任意の別の整数係数多項式`Q:Int[X]`をその元整数に評価する。得られた真正整数`Q.eval N`の`ZMod L_s`合同類は、大域CRT上での多項式評価と一致し、GK5BW環同型を通した**元compatible局所剰余族全体**にも一致する。

元整数多項式`Q,R`に関する加法・乗法の保存、大域・局所への任意部分被覆制限、一段と二段の制限で同じ数値を再現する等式をLean4形式化した。対象となる元分子は`natAbs`表示で作り直さない。法0・空被覆を含む。

真正元F55の異なる二つのType証拠、primitive `P=1` と double inverse＋元F55右単位 `P=X²` の既存P92B整数深度多項式**値**を同じ外側の`Q`による算術塔へ投入した。二つの元Type証拠はいずれも数値的な三段CRT自然性を満たし、既存の明示的`2≤d`・`L_s|d!`の下で最小被覆の数値的CRT零証明書も維持する。一方、元original→phiの**構造的seamはprimitiveで存在、double inverseで不存在**。この境界は同一の型付きLean定理`fivefoldGK5BYNorthBothOuterPolynomialTowerButOppositeSeams`として保持した。

本成果は、数値的多項式の評価・演算・自然性から元F55 Type source、P77商類等号、P94A四セル、全GK5AY seam、P89無条件反射、`W=1→seam`を推論しない。元F54二Nat・二圏・Blocks、元F55 Type歴史、真正第五Dart北C60物理gauge、条件付きP89反射は別authorityとして保持する。

## 4. 次研究境界（未形式化）

**GK5BZ**：整数多項式の一変数評価自然性を、二変数／有限多変数の整数多項式、有限図式間の可換性および局所compatibility障害の型付き可視化へ拡張する余地を調べる。必要な型・自然変換・数値/構造authority境界を明示し、元F55 Type値復元を無条件に仮定しない。

strict 空・独立Kuu→Qi、root107、固定Lean/mathlib、保護PR #1558 Draft/open/unmergedを保持。Gray・GK5BA kitを追加しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
