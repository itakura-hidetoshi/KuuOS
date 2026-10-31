# F112-P94D3GK4AS — 右下法16合同・trace合同・算術slice同一性

**2026年10月31日 JST／GitHub MCP正本確認／Lean4形式化。**

GK4ASは新しい独立obstructionではなく、既存GK4AO〜GK4ARの真正数学的帰結を確定する段階。元F54の真のType値経路、P92B存在商Q、独立構造S、真正K_AI、固定旧K_AG類qの実到達ファイバーを区別する。算術slice全域の到達は仮定しない。

## 1．定理正本・exact-source CI

| 項目 | 結果 |
|---|---|
| Repository／canonical branch | itakura-hidetoshi/KuuOS／main |
| GK4AS定理PR | [#2823](https://github.com/itakura-hidetoshi/KuuOS/pull/2823) MERGED |
| 最終source HEAD | b702e5b586c86751693d40fd0508c767b77bb735 |
| 定理squash SHA／統合直後main HEAD | 6fe4784a704e2da1e20a6c3204509a2357d028a9 |
| source／squash共通Git tree | ecb50d22ea0d68aa7146ffe768fe9c5e0314328d |
| exact-source CI | [GitHub Actions #41199914582](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41199914582) terminal SUCCESS |
| Strict Lean | **3777/3777 SUCCESS**、GK4AS新規ファイルBuilt |
| Governance | **5/5 SUCCESS**、exact-head terminal receipt SUCCESS |
| 新規Lean | 1ファイル・18宣言、既存Lean証明本文変更なし |
| 公理依存 | 全18宣言の表示は propext・Classical.choice・Quot.sound 以内 |
| sorryAx／変更Lean warning・error | **0／0・0**（warningAsError＋sorryAsError） |
| pin | Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 公開root・保護PR | 107維持／[#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft・OPEN・未マージ |

先行GK4AR [#2821](https://github.com/itakura-hidetoshi/KuuOS/pull/2821)、文書同期 [#2822](https://github.com/itakura-hidetoshi/KuuOS/pull/2822) はMERGED。Authority：canonical main exact HEAD → Lean本文 → exact-source CI → README／ROADMAP → 過去の記録。

## 2．既存合同式から強制される右下成分

[GK4AS新規Leanファイル](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ASForcedLowerDiagonal.lean) は旧GK4AD真正Type値を v=((charge,beta),moment)、rho=charge+beta、s=moment+T(beta)（T(n)=n(n−1)/2）とする。新GK4AH整数行列を M=[[a,b],[c,d]] とすると、GK4AO〜GK4ARの既存証明から整数 x,y,z,w が存在し、

~~~~text
a = 1+4*s+16*x
b = rho+4*y
c = 4*beta+16*z
d = 1+4*w
a*d-b*c=1
~~~~

を満たす。この5式は任意のAR条件充足行列に成立する必要条件であり、任意算術行列の元F54到達性は主張しない。

行列式を厳密に展開すると、

~~~~text
0 = (a*d-b*c)-1
  = 4*(w-rho*beta+s)
    +16*(x+s*w+4*x*w-rho*z-y*beta-4*y*z).
~~~~

明示的な整数証人として

~~~~text
t = -x-s*w-4*x*w+rho*z+y*beta+4*y*z
~~~~

と選べば、4*(w-(rho*beta-s)-4*t)=0 より w=rho*beta-s+4*t となる。従って

~~~~text
d = 1+4*(rho*beta-s)+16*t
d ≡ 1+4*((charge+beta)*beta-moment-T(beta)) (mod16).
~~~~

Lean4定理 nativeGK4ASRightDiagonal_forced はこの整数証人をring／omegaで証明し、未確認のmathlib合同式APIや外部仮定を使わない。

## 3．traceと独立obstructionではないことの厳密な区別

同じ左上合同式 a=1+4*s+16*x と加算すると、orderedMomentと三角数は消え、

~~~~text
a+d=2+4*rho*beta+16*(x+t)
tr(M) ≡ 2+4*(charge+beta)*beta (mod16).
~~~~

Lean定理 nativeGK4ASTrace_forced がこれを保証する。traceが旧charge・backwardCountのみで決まることは有用だが、既存GK4ARに独立に追加される算術障害ではない。

nativeGK4ASDiagonalLinked はAR既存条件と右下mod16条件の連言であり、Lean4で

~~~~text
nativeGK4ASDiagonalLinked v M ↔ nativeGK4ARDiagonalLinked v M
~~~~

を任意の整数2×2行列について証明した。従って任意の真の旧qに対し、

~~~~text
Gamma_AS(q)=Gamma_AR(q)
AttainedMatrix(q) ⊆ Gamma_AS(q)=Gamma_AR(q) ⊊ Gamma_AQ(q)
~~~~

である。AS⊊ARという存在しない新obstructionは主張しない。GK4ARで示した旧AQ内到達不能算術行列も引き続き有効。

## 4．真正Type値source、Q、独立S、K_AI、固定旧q

- nativeGK4ASEdge_sound／Chain_sound／Route_sound は実forward/backward RotationEdge、中間木RotationChain、元F54のchain・castDepths・trans・leftContext・rightContext全5構成子をGK4ARの正式証明から継承する。
- nativeGK4ASP92_sound と nativeGK4ASStructural_sound は真正F55/P92B比較証拠を保持する元Qと、実構造seamを持つ独立Sを別々に扱い、観測値一致から新しいType値比較を生成しない。
- nativeGK4ASKernel_sound／Fiber_sound は真正K_AIと任意の旧K_AG類qの実従属ファイバーに降下する。
- nativeGK4ASSlice_eq_AR／Attained_subset_slice／SameFiber_lowerDiagonal_residue／StrictInsideAQ を形式化。固定旧qの二つの実到達行列の右下成分は法16で等しい。

## 5．境界・次の候補

固定単一旧qファイバーの無限性、AR/AS slice全域への到達、元Q自身の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、hyperdescentはいずれも未証明。GK4AN有限下界、GK4AL全ファイバー可算性、GK4AM正k非網羅定理は保持する。

**GK4AT候補（未形式化）：** 真に独立した強化を求め、法32など高精度の合同式と真正非可換Type値履歴を検討する。行列式だけにより強制される合同式を新obstructionとは呼ばない。

Append-only／tighten-only／overwrite-forbidden／same-root107。strict空中心・独立Kuuは空の一presentation、Gray非再導入、保護PR #1558は未マージ維持。著作権 © 2026 Hidetoshi Itakura / 板倉英俊、Apache-2.0。
