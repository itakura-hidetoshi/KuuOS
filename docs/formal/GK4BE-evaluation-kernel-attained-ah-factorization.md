# F112-P94D3GK4BE — 真正K_AIにおける整数評価の核一致と到達AH像への一意因子化

2026-11-01 JST。canonical \`main\`、[定理PR #2851](https://github.com/itakura-hidetoshi/KuuOS/pull/2851) **MERGED**。

## 1. 中心定理 — 元F54の真正観測・既存第二商に限定

GK4BAが証明した元F54の\`t=4\`一点決定性、GK4BBの既存第二kernel \`K_AI\` への全多項式行列\`P̄\`の\`Quotient.lift\`、GK4BCの真のMathlib関手、GK4BDの整数評価関手を統合する。

同じ真正F54型付き始点・終点に対する\`u,v∈K_AI(first,last)\`について、次がLean4で成立する。

\`\`\`text
P̄(u) = P̄(v)
    ↔ eval₄(P̄(u)) = eval₄(P̄(v))
    ↔ ∀ (t : Int), evalₜ(P̄(u)) = evalₜ(P̄(v))
\`\`\`

したがって、**K_AI上の全多項式観測の核・旧AH一点評価の核・全整数評価の共通核が一致**する。これは\`u=v\`や元Type値経路自体の等式を意味しない。旧AH成分だけによる\`K_AI\`クラスの識別も証明されていない。

Functorレベルでは、各真正\`K_AI\` Hom上で\`eval₄\`の核がすべての\`evalₜ\`の核に含まれ、全整数評価Functorの共通核は旧AH Functorの核と一致する。同じHomに対し元多項式Functorの核も旧AH Functorの核と一致する。

## 2. 到達AH像への条件付き因子化と一意性

各型付き\`first,last\`について、実際に到達する行列像のみを定めた。

\`\`\`text
NativeGK4BEAttainedAH first last =
  { A : NativeGK4AHMatrix //
      ∃ z : NativeGK4SKernelClasses ... first last,
        (nativeGK4AIKernelValue first last z).2 = A }
\`\`\`

本物の\`K_AI\`類をこの像に送る\`nativeGK4BEAttainedAHClass\`は全射である。この像上に任意整数\`t\`の評価写像\`nativeGK4BEAttainedEval\`を構成した。定義は選択された実在の代表類を使うが、GK4BAの一点決定性により代表元の選択に依存しない。

\`\`\`text
nativeGK4BEAttainedEval(t, AH(z)) = evalₜ(P̄(z))
nativeGK4BEAttainedEval(4, A) = A
\`\`\`

すべての元\`K_AI\`類でこの代表計算式を満たす写像は**一意**。これは各Homの到達像上での局所的・条件付き普遍性であり、任意の整数2×2行列への到達や元Q自身の圏構造、元Type値3-cellを構成するものではない。

元P92B存在商Qと独立構造商Sについても**別々に**旧AH一致が全整数評価一致を含意することを証明した。元QとSを同一視せず、真正F55/P92B比較および元構造seamを保持する。

## 3. 形式化した16宣言

[正式Lean全文](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BEEvaluationKernelFactor.lean)。

- \`nativeGK4BEFour_determines_all\`、\`nativeGK4BEPolynomial_eq_iff_four\`、\`nativeGK4BEAll_eq_iff_four\`、\`nativeGK4BEAll_eq_iff_polynomial\`：真正K_AI観測の核一致
- \`NativeGK4BEAttainedAH\`、\`nativeGK4BEAttainedAHClass\`、\`nativeGK4BEAttainedAHClass_surjective\`：元AH行列の実到達像と実在証拠
- \`nativeGK4BEAttainedEval\`、\`nativeGK4BEAttainedEval_class\`、\`nativeGK4BEAttainedEval_four\`、\`nativeGK4BEAttainedEval_unique\`：各整数評価の因子化、旧AH恒等・一意性
- \`nativeGK4BEFunctor_four_kernel_subset\`、\`nativeGK4BEFunctor_family_kernel_iff_four\`、\`nativeGK4BEFunctor_polynomial_kernel_iff_AH\`：本物のMathlib関手の各Hom核
- \`nativeGK4BEP92_four_determines_all\`、\`nativeGK4BEStructural_four_determines_all\`：元Q／独立Sの別々の保存定理

## 4. exact-source検証とLean4記法の修正

| 項目 | GitHub MCP確認 |
|---|---|
| 定理PR | [#2851](https://github.com/itakura-hidetoshi/KuuOS/pull/2851) MERGED |
| 最終source HEAD | \`1721e3c02a93a011f63f932af589cce89aac01f6\` |
| 最終test-merge HEAD | \`bbe7b3b17c05e9077f465543c15f737d6a332db7\` |
| 両Git tree | \`41b55bcc9f437ce987815f61dd269b8d90cab8d8\` 完全一致 |
| [GitHub Actions #41255562142](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41255562142) | **Strict Lean 3799/3799 SUCCESS・Governance terminal SUCCESS** |
| 宣言・公理 | 新規16宣言、すべて\`propext\`・\`Classical.choice\`・\`Quot.sound\`の標準3以内 |
| sorryAx | 0 |
| 定理squash=マージ時canonical main | \`9249514545fcaa542538f82cdfc1f6e7b740112e\` |

初回sourceの唯一のLean失敗は、\`nativeGK4BEFunctor_family_kernel_iff_four\` において\`simp only\`が関手全体の等式をHom上の等式に書き換えなかったこと。既存GK4BDの\`nativeGK4BDKAIIntegerEvaluation_four_map\`を各Homで使い、両向きとも\`calc\`による明示的な等式連鎖へ修正した。修正後は上記の新しいexact-source CIを再実行し、失敗なしで完了した。changed Leanは新規ファイル全文・imports・dependent signaturesを確認。

## 5. authority・未証明項目

Lean v4.30.0-rc2、mathlib \`5450b53e5ddc75d46418fabb605edbf36bd0beb6\` 固定。strict空中心、独立Kuuは一つのpresentation。公開root107を維持、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

依然として、元Q自身の結合律・左右単位、元Type値歴史的完全型付き同値、K_AI多項式関手のfaithfulness、固定単一旧類ファイバーの無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは未証明。

append-only／tighten-only／overwrite-forbidden／same-root107。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
