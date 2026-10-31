# F112-P94D3GK4AW — 元F54多項式係数消失と真正backtrack次数境界の鋭さ

2026年10月31日 JST。GK4AVの整数多項式行列の形式化をそのまま引き継ぐ。元Type値経路・比較・商・公開rootを変更せず、証明できたことだけ追補する。

## 1. 正本・exact-source検証

| 項目 | 確認結果 |
|---|---|
| Repository / canonical branch | itakura-hidetoshi/KuuOS / main |
| 定理PR | [#2831](https://github.com/itakura-hidetoshi/KuuOS/pull/2831) — MERGED |
| 最終source HEAD | f4c4de036bfd6d52814e313d5699c5a8fad4b9ae |
| 実CI test-merge checkout | 64dff6e436cba4484412b6d35de1b5cc7aafa6fb |
| source / test-merge / squash共通Git tree | 70db370eb1a46c9db32ddf9a4e98593fdf73db28 |
| 定理squash / 統合直後main HEAD | eb9b5235be076e8a1eb6e12bb501672b3a2a9b0d |
| exact-source CI | [#41207446279](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41207446279) — terminal SUCCESS |
| Strict Lean | **3784/3784 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 公理表示 | 新規10宣言・標準propext / Classical.choice / Quot.sound以内、sorryAx 0 |
| 変更Lean warnings / errors | **0 / 0** |
| 新規Lean | [GK4AWPolynomialCoeffSharp.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AWPolynomialCoeffSharp.lean) |
| 固定toolchain | Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 公開root | 107維持、従来Lean本文未変更 |
| 保護PR #1558 | Draft / OPEN / unmerged |

Authority：canonical main exact HEAD → Lean定理本文 → exact-source CI → README / ROADMAP → 履歴。

## 2. 真正経路の高次係数消失

元GK4ADのbackwardCountを β(r)、GK4AVの多項式行列を P_r(X) とすると

    ∀ n > β(r), ∀ i,j∈{1,2}, [X^n] P_{r,ij}(X) = 0.

固定mathlib Polynomial.natDegree_le_iff_coeff_eq_zero を全4成分に用い、ゼロ多項式も扱う。

- nativeGK4AWRoute_coeff_zero：真正F54完全依存型経路。
- nativeGK4AWP92_coeff_zero：元P92B存在商Q。
- nativeGK4AWStructural_coeff_zero：独立構造商S。

GK4AVの既証次数定理を再利用し、3つのType値主体を区別する。観測等式から新たな元3-cellは生成しない。

## 3. 元LocalRotationによる上界達成

元F54の実 LocalRotation rot を用いる、前向き・逆向き二辺の真正自己経路
B = nativeGK4FBacktrack rot の多項式行列は

    P_B(X) = [[1-X,-1],[X,1]],  β(B)=1.

従ってその左下成分は X であり、

    natDegree(P_B,21)=1=β(B).

nativeGK4AWBacktrack_polynomial は抽象行列語ではなく元F54の実経路を展開して計算。
nativeGK4AWBacktrack_backwardCount は元逆向き構成子の数を計算し、
nativeGK4AWBacktrack_lowerLeft_natDegree と nativeGK4AWBacktrack_degree_sharp は
次数上界の達成を証明。nativeGK4AWPhysicalNorth_degree_sharp は実C60北側へ無条件特殊化。

すべての経路で次数等号が成立するという主張ではない。

## 4. 次段階のobstruction（未形式化）

- 同一の有限二評価 P_u(1)=P_v(1)、P_u(4)=P_v(4) かつ P_u(X)≠P_v(X) を満たす真正F54経路の存在は未証明。
- むしろ、C(4)=[[1,1],[0,1]] と R(4)=[[1,0],[4,1]] は実対角共役でSanov型の自由生成行列 [[1,2],[0,1]], [[1,0],[2,1]] に移る。F=C^{-1}。この三生成子の語の範囲では t=4 の評価だけでも全多項式語を区別できる可能性がある。次はこの障害を元F54構成とLeanで精査する。GK4AWの既証定理に含めない。
- 既存K_AIへの多項式全族降下、固定単一旧類ファイバー無限性、算術slice全域到達、元Q未証明圏公理、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、hyperdescentは引き続き未証明。

append-only / tighten-only / overwrite-forbidden / same-root107。strict空中心・独立Kuuはpresentationの一つ。Gray再導入なし。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
