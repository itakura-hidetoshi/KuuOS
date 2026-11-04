# GK5BT／Qi v4.39 — 重なりを持つCRTのgcd整合性・lcm再合成と北C60構造的障害

2026年11月4日 JST ／ F112-P94D3GK5BT ／ Qi v4.39 ／ 独立定理・Qi統合 **MERGED**

## 1. exact-source証明記録

| 項目 | 独立GK5BT | Qi v4.39 |
|---|---|---|
| PR | [#3085](https://github.com/itakura-hidetoshi/KuuOS/pull/3085) MERGED | [#3086](https://github.com/itakura-hidetoshi/KuuOS/pull/3086) MERGED |
| 検証済みHEAD | `344202e185b4dcfbe72918675161e0aa291a5db0` | `4bb8cb255ee3e596c3d7b4bc745c4cb04c99695e` |
| squash SHA | `ef7d5cacfb5e3081f21ea873f91bd2caf59957b0` | `e8cbdb1276f5f1fafc794a6a51036780296acf65` |
| source/test-merge/squash Git tree | `5e06c4f5bfc414e8dbcef3e32295e032cedcb380` | `05594190c1eed2bda07054b370fabe0d34f759c3` |
| exact-source CI | [#41785580270](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41785580270) | [#41787194501](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41787194501) |
| Strict Lean | **9,296/9,296 SUCCESS** | **10,223/10,223 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規公理監査 | **15定理、sorryAxなし** | **17定理、sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

- [独立GK5BT Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BTNoncoprimeCRTOverlapObstruction.lean)
- [Qi v4.39 Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BTNorthNoncoprimeCRTOverlapV4_39.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean) — 既存定理変更なし、新規2 import追記、公開root107維持

固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2. 独立GK5BT：条件付き重なりCRT

先行GK5BSの素数冪ごとの互いに素なCRT環同型を、共通因子を持つ任意の二法`m,n:Nat`に拡張する。重なり`gcd(m,n)`上での厳密な整合を、真のMathlib `Nat.ModEq` によって

```text
a ≡ b [MOD gcd(m,n)]
 ↔ ∃ x:Nat, x ≡ a [MOD m] ∧ x ≡ b [MOD n]
```

として必要十分に形式化した。一般に無条件の合成は成立しない。固定mathlib `Nat.chineseRemainder'`から実際に`x`を構成し、`Nat.mod_lcm`を用いて**全ての解が法`lcm(m,n)`で同じ合同類**に属することを証明。二法が非零なら`0≤x<lcm(m,n)`の正規化代表が一意。零法は対応する解の存在・同値の一般定理に含むが、厳密な上界には非零条件を明示する。

不整合`a % gcd(m,n) ≠ b % gcd(m,n)`は**大域代表の不存在と同値な算術的obstruction**。整合は加法と乗法に対して保存される。これは局所値の合成であり、元F55 Type値証拠の構造的gluingとは別。

元GK5BQの整数分子`N_(d,j)(v)∈Int`を一切改変せず、自然数の剰余合同として扱うため`|N|=N.natAbs`から二局所値を作る。二局所値は自動的にgcd上で一致し、再合成値は`|N|`と法lcmで一致する。符号を局所剰余から復元する主張はしない一方、

```text
glue(|N| mod m, |N| mod n) ≡ 0 (mod lcm(m,n))
  ↔ (lcm(m,n):Int) ∣ N
```

は元の**符号付き整数N**について必要十分。負値・零を含む実観測列の整除判定が失われない。

初回CIの`rintro ⟨x,hx,hy⟩`で、既に分解した合同条件にさらに`hx.1`・`hx.2`を適用したLean4 projection errorを、`hx`・`hy`に修正。命題・仮定を弱めず15定理を検証した。

## 3. Qi v4.39：真正北C60への接続

実際の元F55 Type値`f`からの既存P92B整数多項式の**値**、元F55/P77商`q`からの**降下多項式値**を別々に扱う。次数`natDegree(P)≤d`および明示的な`lcm(m,n)∣d!`の下、全`j≤d`の元GK5BQ整数分子は`d!`で割り切れるから、非互いに素な局所剰余の合成も**法lcmでゼロ**となる。仮定を隠して任意の二法でゼロになるとは主張しない。

- 重なる二法`m=2,n=6`：`gcd=2`、`lcm=6=(3!)`。真正元primitive`P=1`と元double inverse＋F55右単位`P=X²`は、4観測点`{0,1,2,3}`に拡張した双方の全係数でCRT零証明書を持つ。異なる元Type履歴を同一視しない。
- 真正選択P92Bループ`P=X³+2`と`Q=2X²+X`も、同じ4観測点・二法に対して別個のCRT零証明書を持つ。
- **分離定理`fivefoldGK5BTNorthBothOverlapZeroButOppositeSeams`：** 元primitiveとdouble inverseは双方`gcd=2`の重なり整合と`lcm=6`の大域算術再合成を満たすが、元original→phi seamは前者で存在、後者で不存在。この同じLean4定理により算術的gluingは元F55構造的seamの十分条件でない。
- 単純な数値例では`x≡1 (mod 4), x≡2 (mod 6)`はgcd上で不整合なので大域解がない。対照的に`x≡1 (mod 4), x≡3 (mod 6)`は整合し、正規化した大域代表は`x=9`とLean4で形式化した。

Qi初回CIの唯一の失敗は、定義別名`nativeGK5BTOverlapCompatible`のまま`decide`を呼んだ型クラス合成不足。合同式を実際の余りの等式に`change`で展開して計算し、17定理の条件・型付き主張を変更せず全検証を成功させた。

従来の真正第五Dart物理C60 gauge、条件付き元P89 BadPair反射、元F54二Nat・二圏・Blocks、F55 Type値履歴を保持。数値のCRT整合性から新規F55 Type源、P77商類等号、P94A四セル、全GK5AY seam、`W=1→seam`、P89無条件反射、Gray圏復元、GK5BA kitを導出しない。

## 4. 次の研究

**GK5BU（仮称）**：二つの重なり法から、任意の有限局所被覆`(mᵢ,aᵢ)`へ拡張する。全ての重なり`gcd(mᵢ,mⱼ)`上のpairwise compatibilityと、`lcmᵢmᵢ`上の単一大域代表の存在／一意性を、順次中国剰余合成とČech型の局所・大域整合性として形式化する。構造的F55 Type値・P94A四セルのobstructionは独立に残す。現時点では次研究目標であり、成立済みとは記録しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
