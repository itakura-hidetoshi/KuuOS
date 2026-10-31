# F112-P94D3GK4AR — orderedMoment による第二行列対角成分の法16制約と厳格な固定ファイバー算術slice

**2026年10月31日 JST／GitHub MCP独立確認／canonical Lean4正本。**

GK4ARでは、GK4ADの**真正非可換orderedMoment**と第二GK4AH整数2×2行列の**左上成分**の間に、固定された旧観測類qの内部で成立する新しい合同式をLean4で証明した。GK4AOの行列式1・対角1 mod4・左下0 mod4、GK4APの右上mod4、GK4AQの左下mod16を**全て保持**する。旧観測値の一致から新しいType値3-cellを生成せず、元F54実経路・元P92B存在商Q・独立構造商S・真正K_AI・実際の忘却Fiber(q)を明確に区別する。

## 1. GitHub MCP正本・exact-source CI receipt

| 項目 | 確定値 |
|---|---|
| 定理PR | [#2821](https://github.com/itakura-hidetoshi/KuuOS/pull/2821) — MERGED |
| final exact-source HEAD | `aadaffffc728e623bd8dcd21e91ffb8be07af6a4` |
| CI test-merge checkout SHA | `59debf9dbe2c4e19e3e0b1ee4afa6f03a01dcbb8` |
| source / CI / 定理squash共通Git tree | `3012191846e2c2332d4674c69287b89c065ac988` |
| 定理squash SHA、統合直後canonical main HEAD | `61e8f7483eaa6cd72df7fd03b37963b22f27e645` |
| CI run | [#41198771601](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41198771601) — terminal SUCCESS |
| Strict Lean | **3776/3776 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 公理表示 | 新規 **33宣言**、`propext`・`Classical.choice`・`Quot.sound` 以内 |
| `sorryAx`／変更Lean warning・error | **0／0・0** |
| 変更 | append-only新規Lean **2ファイル**、既存Leanの上書き0、公開root107を維持 |
| 固定環境 | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft・OPEN・未マージ |

## 2. 元F54真正経路の対角成分の新しい必要条件

[GK4ARDiagonalMoment.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ARDiagonalMoment.lean) は、元GK4AD Type値`v=((charge,backwardCount),orderedMoment)`と元GK4AH完全行列`M=[[a,b],[c,d]]`を結び付ける。三角数`T:Nat→Int`を`T(0)=0, T(n+1)=T(n)+n`で定義し、

```text
T(a+b) = T(a)+T(b)+a*b
2*T(n) = n*(n-1)
T(n) = binomial(n,2)
```

を固定Lean4において実際に証明した。これはmathlibの未確認のchoose補題や整数除法に依存しない構成。

主定理は元F54経路rに対して

```text
M_AH(r).11 = 1+4*(orderedMoment_AD(r)+T(backwardCount_AD(r)))+16*t
```

を満たす整数tの存在。すなわち

```text
M_AH(r).11 ≡ 1+4*(orderedMoment_AD(r)+binomial(backwardCount_AD(r),2)) (mod16)
```

となる。GK4AQ/AP/AOの既存算術条件は`nativeGK4ARDiagonalLinked`の**一部として保持**。数え上げだけでなく、GK4AD本来の`m(uv)=m(u)+m(v)+charge(u)*beta(v)`という非可換Heisenberg積をそのまま使用した。

この公式の中心は、元GK4AH行列積の`(AB).11=A.11*B.11+A.12*B.21`にある。GK4APの`A.12≡charge_A+beta_A(mod4)`、GK4AQの`B.21≡4beta_B(mod16)`を使うと、右辺の交差項は`4*(charge_A+beta_A)*beta_B(mod16)`になる。一方、旧orderedMomentの交差項は`charge_A*beta_B`、三角数の加法コサイクルは`beta_A*beta_B`。ゆえに両者の和が一致する。

元のforward/backward LocalRotation Type証人、真のRotationChain中間F45木、二Nat cast、DepthRotationRoute全5構成子を帰納的に通過し、さらに既存の元F55全9・元P92B全9・独立seam全14・拡張比較全3に対する**実Type値保存証拠**を利用。元P92B存在商Qと独立構造商Sへ別々に降下させた。その後K_AIと`Fiber(q)`に移す。正本定理名：`nativeGK4ARTriangle_add`、`nativeGK4ARTriangle_double`、`nativeGK4ARDiagonalLinked_mul`、`nativeGK4ARRoute_sound`、`nativeGK4ARP92_sound`、`nativeGK4ARStructural_sound`、`nativeGK4ARKernel_sound`、`nativeGK4ARFiber_sound`。

## 3. 任意の旧qで GK4AQ slice の内部にさらに厳格な境界がある

[GK4ARStrictDiagonalSlice.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ARStrictDiagonalSlice.lean) で、旧qから得られる`ρ(q)=charge(q)+beta(q)`、`beta(q)=backwardCount(q)`、`m(q)=orderedMoment(q)`について

```text
Γ_AQ(q) = Γ_1(4) with
  M.12 ≡ ρ(q) mod4, M.21 ≡ 4*beta(q) mod16

Γ_AR(q) = Γ_AQ(q) with
  M.11 ≡ 1+4*(m(q)+T(beta(q))) mod16
```

を定義。全ての実到達第二行列像に対し

```text
AttainedMatrix(q) ⊆ Γ_AR(q) ⊊ Γ_AQ(q)
```

が成立する。厳格性を抽象的に仮定せず、`rho=ρ(q)`、`beta=beta(q)`として2つの**具体的整数行列**を構成した。

```text
Base(q)  = [[1+4*rho*beta, rho],
            [4*beta,       1]]

K        = [[5,4],[16,13]], det(K)=1

Twist(q) = Base(q) * K
```

BaseとTwistはどちらも`det=1`、旧APの右上mod4と旧AQの左下mod16条件を満たす。だが

```text
Twist(q).11 - Base(q).11
  = 4+16*rho*(beta+1)
```

なので両行列は左上成分が法16で**必ず4だけ異なる**。一つの`q`が要求する左上剰余に、両行列が同時に属することは不可能。実際にLeanで`by_cases`分岐を構成し、**任意qに対して旧AQ sliceに属するのに新AR sliceに属さない行列の存在**と、その行列の真正Fiber(q)での到達不能性を証明した。これは2行列が真正F54経路として実現するという主張ではない。

主定理名：`nativeGK4ARBaseTwist_not_both`、`nativeGK4ARStrictInsideAQ`、`nativeGK4ARUnattainableInsideAQ`、`nativeGK4ARSameFiber_diagonal_residue`。さらに元従属Fiber(q)を新sliceに単射で写し、**実際に到達した像に限定**した同値`nativeGK4ARRestrictedAttainedEquiv`を構成。

## 4. 未証明の境界と次GK4AS候補

GK4ARはGK4ANの各`q_k`の有限下界`Fin(2k+1)`、GK4ALの全ファイバー可算性、GK4AMの正数kでの既存有限族非網羅性、GK4AO/AP/AQの算術制約をいずれも維持。

引き続き未証明：**単一固定旧qファイバーが無限**、新AR slice全体への到達可能性、K_AI上の比較の全域忠実性／残余非忠実性、元P92B商Q自身の圏公理、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、Gray圏およびhyperdescent。

次段階GK4ASでは、行列式1と既存右上・左下・左上合同式から**右下成分の追加剰余制約が独立に得られるか**を検証する。また、同一固定旧qの有限／無限到達集合の研究は引き続き独立の問題として保持する。

© 2026 板倉英俊 / Hidetoshi Itakura。Apache-2.0。
