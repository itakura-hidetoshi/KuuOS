# GK5BV／Qi v4.40 — 一般有限CRTの必要十分条件と真正北C60 seam境界

2026年11月4日 JST ／ F112-P94D3GK5BV ／ Qi v4.40 ／ **独立・Qi両定理MERGED**

## 1. 唯一の正本・exact-source検証

| 項目 | 独立GK5BV | Qi v4.40 |
|---|---|---|
| 定理PR | [#3089](https://github.com/itakura-hidetoshi/KuuOS/pull/3089) MERGED | [#3090](https://github.com/itakura-hidetoshi/KuuOS/pull/3090) MERGED |
| final exact-source HEAD | `866d3c0ebf19dd803556a7b1f335ef1ee3b7c027` | `a1c7044b3a4db127dc68dcad82b91d2a459944fc` |
| squash SHA | `6329d44d462f2b6e05285e7d2daacaafca1a09a3` | `371a0382fb87b9767939c8ac7f4bdaf73810428a` |
| source/test-merge/squash Git tree | `f63022b6ade5704aab2b864e90ea6bf4b2068f77` | `577cede9fd66bf91c84e36d89f21a0e1cae51c08` |
| exact-source CI | [#41795872887](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41795872887) | [#41796657558](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41796657558) |
| Strict Lean | **9,299/9,299 SUCCESS** | **10,226/10,226 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 公理依存 | **新規9定理、sorryAxなし** | **新規14定理、sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立Lean4定理](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BVGeneralFiniteCRTDescent.lean)
- [Qi v4.40 Lean4接続](../../formal/KUOS/Architecture/QiWuxingGK5BVNorthGeneralFiniteCRTV4_40.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)：旧定理変更なし、独立・Qi各新規importをappend-only追加。公開root107維持。

固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ維持。

## 2. GK5BV — 有限個の重なる法に対する完全CRT降下

前段GK5BUでは「大域解⇒すべてのpairwise gcd整合性」「失敗組があれば解なし」「解は有限lcmを法に一意」「局所法が支配的なら構成可能」までを証明していた。**GK5BVは支配的局所法という仮定を撤去し、必要十分条件を完成**した。

真の任意有限添字集合`s:Finset ι`、任意の自然数法`mᵢ:Nat`、独立局所代表`aᵢ:Nat`について

```text
(∀ i∈s, ∀ j∈s, aᵢ ≡ aⱼ [MOD gcd(mᵢ,mⱼ)])
   ↔
(∃ x:Nat, ∀ i∈s, x ≡ aᵢ [MOD mᵢ]).
```

を固定mathlibで**無条件にLean4形式証明**した。互いに素、非零法、支配的局所法、元F55 Type源の存在などの仮定なし。空の有限集合も包含する。

主要補題は任意`a,b,c:Nat`についての

```text
gcd(lcm(a,b),c) = lcm(gcd(a,c),gcd(b,c)).
```

ゼロを含む場合を個別処理し、非零の場合には固定mathlibの`Nat.factorization_gcd`・`Nat.factorization_lcm`・`Nat.factorization_inj`と分配格子の点ごとのmin/max恒等式を使用した。これを`Finset.lcm`へ帰納的に拡張した上で、現在の大域代表と新しい局所法の共通部分上の整合性を導出し、前段GK5BTの真正`Nat.chineseRemainder'`で逐次再合成した。存在証明に追加公理や架空の剰余代表はない。

`L = Finset.lcm s m` とすると、すべての大域解は**法Lで一意**。`Classical.choose`は証明済み存在定理からのみ代表を選択し、その`x % L`はすべての局所条件を保持する。`L≠0`なら正規化解は`0≤x%L<L`。法0の局所条件が存在する場合も、mod0を等号と解釈した同じ一般定理が成立する。

さらに

```text
¬ ∃ global x
 ↔ ∃ i∈s, ∃ j∈s, ¬(aᵢ ≡ aⱼ [MOD gcd(mᵢ,mⱼ)])
```

の有限obstruction必要十分条件を証明。**数値的な局所・大域descend可能性と元F55 Type-valued seamは同一概念ではない。**

### CI修正記録

初回CIはゼロケースの等式向き2箇所、`Finsupp`格子演算と汎用`DistribLattice`インスタンスの型差異、`GCDMonoid.lcm`／`Nat.lcm`の補題適用名違いが原因。左右対称化、`Finsupp.inf_apply`／`sup_apply`の点wise min/max証明、固定mathlib`lcm_eq_nat_lcm`による橋渡しに修正。既存定理と新規定理の数学的仮定・結論は弱めず、最終CIで9定理全て`sorryAx`なし。

## 3. Qi v4.40 — 真正北C60の数値値と元seamを分離

元GK5BQの**実際の符号付き整数分子**`N_(d,j)(v)∈Int`から各局所法について`N.natAbs % mᵢ`を観測する。一般GK5BVの有限CRTで再合成した正規化大域代表は、元の`N.natAbs`と**法`Finset.lcm`で同じ合同類**である。したがって

```text
normalized finite CRT glue ≡ 0 (mod Finset.lcm)
 ↔ (Finset.lcm:ℤ) ∣ N_(d,j)(v).
```

ここで絶対値表現が残すのは元**符号付き整数Nの整除判定**であり、元符号を剰余列から復元できるという主張ではない。

実際の整数係数多項式`P:Int[X]`について`natDegree(P)≤d`、**`Finset.lcm moduli ∣ d!`**を明示すれば、全`j≤d`で有限CRT合成類が零になる。元F55 Type値の真正北証拠では既存のP92B整数深度多項式**値**、元F55/P77商類では既に降下した整数多項式**値**にのみこの条件付き定理を適用した。

- 元primitive`P=1`と別のdouble inverse＋元F55右単位`P=X²`は、上述の有限lcm整除条件の下、双方とも全係数で数値的有限CRT gluingが成立する。
- **`fivefoldGK5BVNorthBothFiniteZeroButOppositeSeams`**：この二つの真正元F55 Type値証拠はともに算術的有限CRT零だが、元original→phiの局所seamは前者で**存在**、後者では**不存在**。数値gluingは構造的Type seamの十分条件ではない。
- 独立局所例の`Fin 3`で、法`4,6,9`、代表`1,3,0`は実際に大域代表`9`を持つことを型付き証明。これらの法は互いに素でなく、単独で他の全てを支配する局所法もない。元`Finset.lcm`の合同類としての一意性も証明。
- 真正北第五Dart物理C60と元P89 BadPair**条件付き**反射は旧来のType定理から継承。数値合同条件から新しい元F55 source、P77商類同一性、P94A四セル、GK5AY全域seam、P89無条件反射、`W=1→seam`、GK5BA kit、Grayを導出しない。

## 4. 次の研究境界

**GK5BW（仮称）**：今回の必要十分条件と正規化大域代表から、有限局所剰余系の**環としてのfiber product／互換族**と大域`ZMod(L)`の間の実際の環同型、局所制限・再合成の加法／乗法自然性、obstructionの型付き境界を検討。数学的な数値環同型と元F55 Type証拠・4セル・seamの構造的再構成は引き続き別課題。この時点では次研究計画であって証明済みではない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
