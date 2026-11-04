# GK5BX／Qi v4.42 — 有限CRT環同型の被覆制限・合成・三段コヒーレンス

2026年11月4日 JST ／ F112-P94D3GK5BX・Qi v4.42 ／ **独立・Qi両定理MERGED**

## 1. 唯一の正本とexact-source形式検証

| 項目 | 独立GK5BX | Qi v4.42 |
|---|---|---|
| 定理PR | [#3095](https://github.com/itakura-hidetoshi/KuuOS/pull/3095) MERGED | [#3096](https://github.com/itakura-hidetoshi/KuuOS/pull/3096) MERGED |
| exact-source HEAD | `666cb554977a84b61298589d55255d38a9fa40d5` | `859b1da202cb2a2df63808eee92e5704e68be4df` |
| squash SHA | `115bd0a3f3f05dd1441cd651e84e24287dce8dc0` | `b3068230e8c6c2160d1045764f73558df6ebf616` |
| source／test-merge／squash Git tree | `0fba0c457a1b8aa01ca18d0e32461388dddc057b` | `0f0feb3204bb3646f0a986e805b4d105ad5ebc70` |
| CI | [#41812872432](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41812872432) | [#41813790217](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41813790217) |
| Strict Lean | **9,303/9,303 SUCCESS** | **10,230/10,230 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規定理の `#print axioms` | **11定理、sorryAxなし** | **12定理、sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

正式ソース：[GK5BX独立Lean4](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BXFiniteCRTRestrictionCoherence.lean)、[Qi v4.42 Lean4](../../formal/KUOS/Architecture/QiWuxingGK5BXNorthCRTTowerNaturalityV4_42.lean)、[公開Lean集約](../../formal/KuuOSFormal.lean)。新規Leanモジュールとappend-only公開importのみで、既存Lean定理ソース・元F55 Type歴史・root107を変更していない。

canonical main 定理マージ後HEAD：`b3068230e8c6c2160d1045764f73558df6ebf616`。Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。

## 2. GK5BX：一般有限互換CRT環の真の制限コヒーレンス

GK5BWの真正環同型 `Φ_s : ZMod(L_s) ≃+* R_s` を使用する。有限被覆`u⊆t⊆s`の任意の自然数法（零法、互いに素でない法、空被覆を含む）について、各`L_s=Finset.lcm s moduli`。gcd上で互換な局所ZMod値の依存積Subringを`R_s`とする。

- 真の有限LCM整除：`L_t ∣ L_s`。ここから大域制限`q_(s,t):ZMod L_s →+* ZMod L_t`を固定mathlib`ZMod.castHom`で定義。
- 真の局所互換Subring制限`ρ_(s,t):R_s →+* R_t`を構成。元のZMod値をそのまま部分被覆へ制限し、全pairwise gcd互換性、加法・乗法・単位元を保つ。
- **RingHom恒等・合成の文字どおりの等式**：`ρ_(s,s)=id`、`ρ_(t,u)∘ρ_(s,t)=ρ_(s,u)`、`q_(s,s)=id`、`q_(t,u)∘q_(s,t)=q_(s,u)`。
- **自然性の可換四角形**：`Φ_t ∘ q_(s,t) = ρ_(s,t) ∘ Φ_s`を`RingHom`の等式として証明。さらに`Φ_t⁻¹ ∘ ρ_(s,t) = q_(s,t) ∘ Φ_s⁻¹`の値に対する逆自然性を証明。三段被覆の全体図式についても真正`RingHom`等式でコヒーレンスを確認。
- 上記に新たな非零性・coprime・支配的法・非空被覆・元F55 Type sourceの存在仮定はない。適用対象は数値的CRT環であって、元F55 Type-valued seamの存在を構成しない。

初回CIのLean4記法エラーは`Subset.refl s`を`HasSubset.Subset.refl`として誤解決した3箇所に限られた。いずれも真正`Finset`包含証明`fun _ hi => hi`で修正し、定理の仮定・結論はそのまま保持。最終exact-source CIで11定理の公理依存にsorryAxなし。

## 3. Qi v4.42：真正北C60の元符号付き整数値・三段自然性

元GK5BQの真正`nativeGK5BQClearedNumerator d j values : Int`を**符号付きのまま**`ZMod L_s`へ埋め込み、GK5BWの元compatible CRT ringへ写す。前段Qi v4.41の一段自然性を、今回の**二段被覆制限**へ拡張した。

- 真の元符号付きnumeratorの大域`ZMod`合同類は一段制限、二段制限後も元の整数から直接作った最終局所合同類と一致する。元compatible局所剰余環全体でも同じ等式が成立。
- 一般整数多項式`P : Polynomial Int`について`P.natDegree ≤ d`と`L_s ∣ d!`なら、全有限部分被覆`t⊆s`で既存のCRT零証明書が成立する。整除の移送は真の`L_t ∣ L_s`と除法の推移に基づく。
- **真正元F55 Type sourceの二つの異なる値**：primitive `P=1`とdouble inverse＋元F55右単位`P=X²`の元P92B整数深度多項式**値**それぞれに、同じ二段CRT ring制限自然性を適用。条件`2≤d`・`L_s|d!`の下、双方が部分被覆`u`でCRT零である一方、元original→phi構造的seamはprimitiveで**存在**し、double inverseでは**不存在**という既証明の元Type境界を同じ型付き定理に保つ。

これらは元F55のType source・P77商類等号・P94A 4-cellの復元ではなく、元F55 Type履歴に結び付いた**既存の整数値**に対する数値的自然性である。真正北第五Dart物理C60・条件付きP89 BadPair反射を同一視しない。旧定理依存と独立Kuu→Qiのauthority境界を維持する。

## 4. 次の研究境界

**GK5BY（研究計画、未証明）**：有限被覆CRT環系の自然性を、整数多項式の評価と加算・乗算のより一般の演算に対する可換性、有限図式の自然変換の高次構造へ広げる。必要な係数・次数・法の条件を明示し、数値的descendから元F55 Type-valued sourceやP94A四セル、全GK5AY seamを無条件に復元しない。

strict 空／独立Kuu→Qi、元F54二Nat・二圏・Blocks、元F55 Type履歴、公開root107、保護PR #1558 Draft/open/unmerged、固定Lean/mathlibを保持。Gray、GK5BA kit、W=1→seamを追加しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
