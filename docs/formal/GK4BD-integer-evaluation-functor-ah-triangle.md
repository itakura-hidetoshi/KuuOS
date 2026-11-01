# F112-P94D3GK4BD — 真正K_AIからの整数評価関手と旧AH関手の厳密一致

2026-11-01 JST。canonical main / [GK4BD定理PR #2849](https://github.com/itakura-hidetoshi/KuuOS/pull/2849) **MERGED**。

## 1. 数学的結論

GK4BC は既存の真正第二kernel圏 K_AI 上の多項式行列関手 P̄ を構成した。GK4BD では任意の整数 t に対し、2×2整数多項式行列をその各成分の値へ写す **真のMathlib関手**を構成する。

- 多項式値圏のHomは Mat₂(ℤ[X])、整数値圏のHomは Mat₂(ℤ)。いずれも **全行列をもつ一対象圏**であり、元F54経路から実際に到達する部分集合と混同しない。
- eval_t : Mat₂(ℤ[X]) → Mat₂(ℤ) は順序付きの行列積および単位行列を保存する。
- 真正K_AI上に P̄ ⋙ eval_t をMathlibの関手合成で構成する。
- **t=4 の関手合成が既存K_AIの旧AH成分観測関手と、Homごとの一致だけでなくFunctorの等式として一致する**。
- 元構造商S→K_AIの実比較関手を介した任意整数t評価は、従来の真正S側GK4AU整数行列族と一致する。t=4では元S側AH行列が正確に回収される。

中心定理：

\`\`\`text
nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4 =
  nativeGK4BDOldAHFunctor p ma mb pa pb
\`\`\`

この等式は**元Type値経路の同一性ではない**。元P92B商Q自身の結合律・単位律や新たな3-cellは使用していない。整数評価関手のfaithfulness、K_AI多項式関手のfaithfulnessも主張しない。

## 2. Lean4新規10宣言

[正式Lean全文](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BDIntegerEvaluationFunctor.lean)。

1. \`nativeGK4BDIntegerMatrixCategory\` — 既存AH整数行列積と単位で一対象圏を構成。
2. \`nativeGK4BDIntegerEvaluationFunctor\` — 任意整数tの全多項式行列評価を実Functorとして構成。
3. \`nativeGK4BDIntegerEvaluationFunctor_map\` — 任意多項式行列でのmap計算式。
4. \`nativeGK4BDKAIIntegerEvaluationFunctor\` — GK4BCの真正K_AI多項式値関手と評価関手を合成。
5. \`nativeGK4BDKAIIntegerEvaluationFunctor_map\` — 真正依存型K_AI Hom上の計算式。
6. \`nativeGK4BDOldAHFunctor\` — 既存AI三成分観測の最後のAH行列を取り出す、真正K_AI圏上の関手。
7. \`nativeGK4BDKAIIntegerEvaluation_four_map\` — 全K_AI Homにおけるt=4のAH成分回収。
8. \`nativeGK4BDKAIIntegerEvaluation_four_triangle\` — **Functor全体の厳密な等式**。
9. \`nativeGK4BDKAIIntegerEvaluation_structural\` — 任意整数tで独立構造商Sと実際に可換。
10. \`nativeGK4BDKAIIntegerEvaluation_four_structural\` — 既存S上の旧AH観測との厳密な一致。

### Lean4 elaboration 修正

初回の \`Functor.ext\` は目標にMathlibの \`eqToHom\` 型付き両端輸送を挿入するため、Hom値の単純な等式を \`exact\` できなかった。旧・新Functorsの値対象はともに唯一の \`star\` なので、\`eqToHom_refl\`、\`Category.id_comp\`、\`Category.comp_id\` で輸送を恒等へ正規化した。これは数学的仮定の追加ではなく、Lean4の依存型等式のelaborationに即した修正である。変更ファイル全文・imports・dependent signaturesを検査した。

## 3. exact-source証拠

| 項目 | GitHub MCP確認 |
|---|---|
| 定理PR | [#2849](https://github.com/itakura-hidetoshi/KuuOS/pull/2849) MERGED |
| 最終source HEAD | \`e1ac6051a020b352aea28bd10f91071d7d64cb64\` |
| 最終test-merge HEAD | \`c92e96270309238ef05f4679b010c5bb8ce2fded\` |
| 両者Git tree | \`50948f48c413b0c1bed56229ba40ab8e8acbe05c\` 完全一致 |
| [GitHub Actions #41254632718](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41254632718) | **Strict Lean 3798/3798 SUCCESS / Governance terminal SUCCESS** |
| #print axioms | 新規10宣言、すべて標準3公理 \`propext\`、\`Classical.choice\`、\`Quot.sound\` 以内 |
| sorryAx | 0 |
| 定理squash SHA・マージ時のmain HEAD | \`1ebc72839b29e50e649484766cdf8c7741df4a1e\` |

Lean v4.30.0-rc2、mathlib \`5450b53e5ddc75d46418fabb605edbf36bd0beb6\` を維持。公開root107維持、保護PR #1558 Draft／OPEN／未マージ。

## 4. Authority／残るobstruction

真正F54の元F55全9・元P92B全9・独立構造seam全14などの比較証拠を変更していない。元Qと独立Sを同一視せず、既存K_AI上で得られた関手だけを扱う。strict空中心・独立Kuuは一presentation、Gray非再導入。

未証明なのは元Q自身の結合律・左右単位、元Type値歴史的完全同値、K_AI→多項式値のfaithfulness、固定単一旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescent。任意の整数tの評価関手を構成できたことは、任意の多項式値の元F54実現可能性を意味しない。

Append-only／tighten-only／overwrite-forbidden／same-root107。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
