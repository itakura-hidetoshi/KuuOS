# F112-P94D3GK4AV — 真正F54整数多項式行列、SL₂(ℤ[X])、次数とbackwardCount

2026年10月31日 JST。GK4AUの整数パラメータ関数族を、実際に整数係数多項式の行列として形式化する。既存の観測やType値比較証拠を上書きせず、元F54全5構成子、元F55/P92B比較、独立構造seamを保存する。

## 1．定理正本・GitHub MCP exact-source記録

| 項目 | 確認結果 |
|---|---|
| Repository／唯一のcanonical branch | itakura-hidetoshi/KuuOS／main |
| 定理PR | [#2829](https://github.com/itakura-hidetoshi/KuuOS/pull/2829) — MERGED |
| 最終source HEAD | 66d2c7cd4975d32b481a90dde160716ffed00cfa |
| 実CI test-merge checkout | cea32d3ff12550ff0847b6283f07ae0c2271043f |
| 定理squash／統合直後main HEAD | 5fa543a03d39687426844efe117e2473a2b1e939 |
| source／CI checkout／定理squash共通Git tree | f2304229aa5bdafa3b78ef345b1c0975b72b7de7 |
| exact-source CI | [GitHub Actions #41206335465](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41206335465) — terminal SUCCESS |
| Strict Lean | **3783/3783 SUCCESS**、GK4AV 2 Lean files Built |
| Governance | **5/5 SUCCESS**、exact-head terminal receipt SUCCESS |
| 公理依存 | 新規 **65宣言**の#print axiomsはpropext・Classical.choice・Quot.sound以内、sorryAx 0 |
| 変更Lean warnings／errors | **0／0** |
| 固定環境 | Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 差分 | append-only新規Lean2、旧Lean証明ファイル本文の変更なし、公開root107維持 |
| 保護PR | [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft・OPEN・未マージ |

Authority：canonical main exact HEAD → Lean定理本文 → exact-source CI → README／ROADMAP → 過去の要約。

## 2．本物の多項式行列観測

[PolynomialInvariant.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AVPolynomialInvariant.lean) は型付き実F54経路の整数多項式行列を直接定義する。

~~~~text
NativeGK4AVValue := (Polynomial Int × Polynomial Int) ×
                    (Polynomial Int × Polynomial Int)

C(X) = [[1,1],[0,1]]
F(X) = [[1,-1],[0,1]]
R(X) = [[1,0],[X,1]]
C(X) * F(X) = I
~~~~

積は上記2×2行列の本当の順序付き非可換積。castDepthsは元の二Nat cast、forward/backwardは元のLocalRotation型付き証拠である。任意の形式的な文字列を元F54経路に置き換えない。真正RotationEdge・RotationChain・DepthRotationRoute（chain/castDepths/trans/leftContext/rightContext全5構成子）上に定義する。

元F55 9・元P92B 9・独立構造seam 14・拡張比較3の、実際のType値比較証拠を用い、**多項式全成分の等式**が保存されることを証明。元P92B存在商Qと独立構造商Sへ別々に降下、Q→Sの可換性、S合成・単位保存を証明済み。観測の等式から逆向きにType値3-cellを作らない。

## 3．整数パラメータ族との厳密一致

[DegreeEvaluation.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AVDegreeEvaluation.lean) で、4成分の整数多項式を同じ整数tで評価する写像を定義し、行列積との整合性を示した。全真正原始辺・途中木・5経路構成子、元Q・独立Sで、

~~~~text
eval_t(P_r(X)) = M_GK4AU(r,t)   for every t: Int
eval_1(P_r(X)) = M_AF(r)
eval_4(P_r(X)) = M_AH(r)
~~~~

が厳密に成立する。全族を勝手にK_AIへ降下するのではなく、元Qと独立Sで保持された観測の特殊化だけを主張する。GK4AUの法kに関する必要十分分類、GK4ATの法3および同一旧q内法48・法12制約を維持する。

## 4．行列式1を多項式環そのもので証明

~~~~text
det(P_r(X)) = P_11(X)*P_22(X) - P_12(X)*P_21(X) = 1 ∈ ℤ[X]
~~~~

を、原始生成子の直接評価と行列式乗法性から帰納的に証明した。単に各整数tの行列式が1であるという評価後の事実より、**多項式としての恒等式**を証明している。元Q・独立Sでも別々に成立する。これは多項式行列のSL₂(ℤ[X])への像の必要条件であり、任意のSL₂(ℤ[X])行列を元F54で実現するという主張ではない。

## 5．多項式次数の真正backwardCount上界

旧GK4ADの正本Valueは ((charge,beta),orderedMoment) で、betaは実経路に沿ったbackward RotationEdgeのNat計数。GK4AVでは各成分のPolynomial.natDegreeについて、真正実経路rで

~~~~text
for all i,j ∈ {1,2}:
    natDegree(P_r(X)[i,j]) ≤ beta_AD(r)
~~~~

を証明した。これは帰納的な単語長の推測ではなく、元の依存型経路に実際に属するbackwardCountを使う。const C/Fのdegree=0、R(X)のdegree≤1、行列積の各成分に対して

~~~~text
natDegree(p+q) ≤ max(natDegree p, natDegree q)
natDegree(p*q) ≤ natDegree p + natDegree q
~~~~

という固定mathlibの証明済みAPIを用いて構成。元Q・独立Sでも、それぞれ正本の旧GK4AD値と新多項式行列の整合性を証明済み。これは上界であり、全ての経路で等号が成立するとは主張しない。0多項式のnatDegreeが0である場合にも成立。

## 6．Lean記法エラーと正規化の構造的理由

初回CI #41205637447 は、従前のInt値行列ではdefinitional equalityで済んだassoc/pentagon/disjoint squareが、Polynomial Intの非自明な加法・乗法のため同じように簡約されない問題を示した。まず真正assocの形を展開し、Polynomial上の明示的なcast-forward単位律で証明。2回目CI #41205928292でassoc通過後、元の長いpentagon経路と2通りのdisjointSquareの評価が同じ理由で残った。3回目では、F54の実型付き経路を展開し、長短pentagonの共有する単位因子とsquareの同一順序付きforward積を明示正規化した。

元Type値比較の証拠や定理の署名は弱めていない。changed Lean 2ファイル全文・imports・dependent signatures・pinned mathlib natDegree APIを点検した。最終CI 3783/3783と65宣言の標準3公理以内表示、sorryAx0、変更Lean warning/error0/0をGitHubのexact-source証拠から確認。

## 7．未証明境界と次候補

**未証明：** 多項式族の既存K_AIへの無条件降下（K_AIは旧t=1,4など有限の観測値だけで定義され、全多項式の等式を保証しない）、固定単一旧qファイバーの無限性、すべてのSL₂(ℤ[X])多項式の到達、元Q自身の結合律・左右単位、歴史的完全型付き同値、14D無条件Countable、19D filler、global strict、hyperdescent。

**GK4AW候補（未形式化）：** 全成分の係数消失の明示化と実LocalRotation backtrackにおける次数上界の鋭さを調査し、さらに既存のt=1,4二点値が一致しても多項式族全体は異なる真正F54経路が存在するかを、実証拠を用いて検討する。存在性は未証明。

Append-only／tighten-only／overwrite-forbidden／same-root107。strict空を中心に保持し独立Kuuは空の一presentation。Gray非再導入、保護PR #1558未マージ維持。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
