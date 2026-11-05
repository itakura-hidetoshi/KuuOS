# Qi v4.74 — 元P77の終端証拠による階層的細分認証とraw順序図式

## 0. 検証済み正本

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS、canonical branch：main。
- 継承基点：Qi v4.73、4123b496b11a4e8f11d58b2cafbbff571555aa4c。
- 定理PR：[ #3170 ](https://github.com/itakura-hidetoshi/KuuOS/pull/3170) — MERGED。
- exact-source検証HEAD：bb8e6576d012fe8857c77070fef053c03dd8fc6c。
- 定理squash：18f464aaf2f672fe305f800a725f77be97e32aea。
- source/test-merge Git tree：fe0fa9418b95e842f48c9f9692a14727230345c8 — 完全一致。
- [exact-source CI #42120339598](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42120339598)：SUCCESS。
- Strict Lean：**10,271 / 10,271 SUCCESS**。
- Governance：**30 / 30 SUCCESS**。
- 新規26宣言の実公理出力：標準公理のみ、sorryAx 0。
- 変更Lean warning/error：0/0。
- Lean：v4.30.0-rc2、mathlib：5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、root107、保護PR #1558 Draft／OPEN／未マージ。

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TerminalCertifiedRefinementHierarchyV4_74.lean) · [v4.73正式記録](Qi-v4_73-original-P77-certified-mixed-subdivision-five-cell.md)

## 1. 研究上の前進

v4.73は、元source証拠を備えた混合細分routeを入力し、そこから真正raw五セル比較を構成した。今回扱うのは、各細分に必要なsource証拠をまだ補っていない有限の細分計画である。

計画Pは、各局所変更の真正GK5CG Type値五セル比較、元sourceの始終点、途中の切断木、recut・表示変更・左右文脈・合成順序をすべて保持する。今回、最終的な細い木Tの真正因子別source証拠から、計画Pに指定された中間段すべての証拠と、既存v4.70の証拠付きrouteそのものを帰納構成する。

核心は次の二つである。

$$
w_T\in W(T)
\quad\Longrightarrow\quad
\operatorname{Certify}(P,w_T):
\operatorname{SubdivisionRoute}(S,T),
$$

$$
\boxed{
\operatorname{AllCompatible}(P)
\iff
\operatorname{Compatible}(T).
}
$$

最終木の証拠は、粗い全体の商等式ではなく、指定された最終因子すべてに対する真正source証拠である。

## 2. 未認証計画と証拠付き履歴

新しい帰納Type FivefoldP77RawPatchRefinementPlan は以下を持つ。

| 計画構成子 | 保存するデータ |
|---|---|
| presentation | 既存の有限recut・被覆表示変更の履歴 |
| subdivide | 粗ブロック、細い切断木、両者の実際のraw五セル比較 |
| trans | 連続する二つの計画とその真の中間木 |
| left | 共通右文脈と左部分の計画 |
| right | 共通左文脈と右部分の計画 |

未認証のsubdivideには自由な逆構成子を設けない。fine witnessのない細分を逆向きに扱って、粗い証拠だけからfine witnessを生成することを防ぐ。presentation内部の逆操作は、既に真正証拠同値を持つ既証明の操作である。

認証後には既存SubdivisionRouteの逆が使用可能になる。この段階分けは数学的な存在条件による。

## 3. 終端から全中間段への実際のgluing

Pullback(P)は、終端証拠Typeから始点証拠Typeへの写像である。証拠Typeが空でも関数としては定義される。

$$
\operatorname{Pullback}(P):W(T)\to W(S).
$$

単一細分では、終端木を既存TreeNormalizeEquivで正規化し、SubdivisionGlueで元の粗ブロックへ貼り合わせ、BlockTreeEquivの逆で元の粗い一段木へ戻す。

連続計画P:S→M、Q:M→Tでは、

$$
\operatorname{Pullback}(P;Q)(w)
=
\operatorname{Pullback}(P)
\bigl(\operatorname{Pullback}(Q)(w)\bigr).
$$

したがって中間Mの証拠は、終端Tの証拠と後半Qから実際に生成される。左右文脈では真正Type値証拠の積の該当成分にだけ操作を適用する。

Pullback_pathは、元の型付きQuiver.Pathが厳密に一致することを帰納証明する。数値chargeや商クラスの一致に縮約しない。Pullback_certifiedにより、元source到達証拠付きP77部分Homも保存される。

## 4. 各段のsource証拠を補う認証構成

Certify(P,w_T)は、元のv4.70 SubdivisionRouteの値を返す。新たな任意routeや同値を仮定しない。

transでは先に後半計画のPullbackを実行し、中間証拠を前半の認証に使用する。subdivideには最終木から正規化した実際のfine witnessを渡す。この再帰により、既存routeの各subdivide構成子の中に真正fine witnessが収まる。

構成されたrouteで復元した始点証拠を前向きに移送すると、供給した終端証拠が回収される。ここでsource証拠Typeの一意性は既証明の元source faithfulnessから用いる。raw五セルTypeをsubsingletonにはしていない。

## 5. 同じ計画の五セル値を認証前後で保存

計画だけから構成できるraw comparisonをC(P)とする。これは全raw添字の両方向写像と、その各添字に対応する選択済みGK5CG五セル値を持つ。

今回のCertify_rawは、構造全体の等式

$$
\boxed{
\operatorname{RawComparison}
\bigl(\operatorname{Certify}(P,w_T)\bigr)
=
C(P)
}
$$

を証明する。

これは**同じPの二つの解釈**の一致である。認証で補われるsource証拠は、既存raw解釈の選択済み五セルを変更しない。異なる計画P,Qや、左右の異なる順序の五セル履歴が等しいとは主張しない。

この結果とv4.73のnaturalityから、実際の元raw gluingも可換となる。

$$
E_{C(P)}
\bigl(G_S(\operatorname{Pullback}(P)(w_T))\bigr)
=
G_T(w_T).
$$

## 6. 全階層compatibilityと認証の必要十分条件

AllCompatible(P)は、各初等操作の両端、transで保存した双方の部分計画、左右文脈の未変更因子のcompatibilityを再帰的に要求する。

終端のfactorwise compatibilityから全段のsource証拠がPullbackで得られるため、

$$
\operatorname{AllCompatible}(P)
\iff \operatorname{Compatible}(T)
$$

が成立する。さらに、

$$
\neg\operatorname{AllCompatible}(P)
\iff \operatorname{Obstructed}(T).
$$

真正粗証拠w_Sを持つ場合には、より具体的な認証条件を証明する。

$$
\boxed{
\begin{aligned}
&\exists r:S\to T,\quad
r\text{ は証拠付きroute},\quad
\operatorname{RawComparison}(r)=C(P)
\\
&\qquad\iff\quad \operatorname{Compatible}(T).
\end{aligned}
}
$$

ここでは元計画の選択済みraw五セル比較をそのまま保持するrouteの存在まで扱う。粗い証拠だけで指定した終端因子の条件を推論しない。

## 7. 独立する左右細分の実順序図式

局所計画L:L₀→L₁とR:R₀→R₁から、左先行LRと右先行RLの両方を実際に構成する。

| 順序 | 中間木 | 終端証拠から得る中間source証拠 |
|---|---|---|
| LR | node(L₁,R₀) | (w_L, Pullback(R)(w_R)) |
| RL | node(L₀,R₁) | (Pullback(L)(w_L), w_R) |

両者が復元する粗い証拠は、定義的に同じ

$$
(\operatorname{Pullback}(L)(w_L),
\operatorname{Pullback}(R)(w_R))
$$

である。順序部分のこれらの等式はrflで成立し、source証拠のsubsingleton性で押しつぶしていない。

全終端raw添字組(i,j)に対して、両順序の前向き添字写像は同じ組(φ_L(i),φ_R(j))へ到達する。後向きの両coverage写像も成分ごとに一致する。coverage写像が互いに逆であることは仮定しない。

RawSquareは、同じraw四セル始点・終点を持つ**二つの真正GK5CG五セル値の組**を返す。実際の元verticalLeft、verticalRight、transを通る履歴を残す。さらに、その一方の逆と他方を合成した真正五セルloopも構成する。このloopをreflと等しいとは主張しない。

## 8. 因子別obstructionの具体例

元の逆e01→順e01という二段の指定因子分解に対して、未認証RefinementPlanを実構成する。統合されたraw四セルには真正nil source証拠があるが、逆向きの指定source段には原像がない。

今回のReverseForwardRefinementPlan_obstructedは、この実計画のAllCompatibleが成立しないことを証明する。計画の存在、真正raw五セル比較の存在、粗いsource証拠の存在から、失われたfine source証拠を生成しない。

## 9. 公開宣言・実装範囲

新規Leanファイル一件とKuuOSFormalのimport一行を追加。全26宣言について、実際のLean #print axioms出力を確認した。

1. `FivefoldP77RawPatchRefinementPlan`
2. `fivefoldP77RawPatchRefinementPlanRawComparison`
3. `fivefoldP77RawPatchRefinementPlanPullback`
4. `fivefoldP77RawPatchRefinementPlanPullback_path`
5. `fivefoldP77RawPatchRefinementPlanCertify`
6. `fivefoldP77RawPatchRefinementPlanCertify_raw`
7. `fivefoldP77RawPatchRefinementPlanCertify_terminal`
8. `fivefoldP77RawPatchRefinementPlanRawGlue`
9. `fivefoldP77RawPatchRefinementPlanPullback_certified`
10. `fivefoldP77RawPatchRefinementPlan_sourceCompatible`
11. `fivefoldP77RawPatchRefinementPlanAllCompatible`
12. `fivefoldP77RawPatchRefinementPlan_allCompatible_iff`
13. `fivefoldP77RawPatchRefinementPlan_obstructed_iff`
14. `fivefoldP77RawPatchRefinementPlan_certification_iff`
15. `fivefoldP77ReverseForwardRefinementPlan`
16. `fivefoldP77ReverseForwardRefinementPlan_obstructed`
17. `fivefoldP77RawPatchRefinementLeftThenRight`
18. `fivefoldP77RawPatchRefinementRightThenLeft`
19. `fivefoldP77RawPatchRefinementOrder_forwardIndex`
20. `fivefoldP77RawPatchRefinementOrder_backwardIndex`
21. `fivefoldP77RawPatchRefinementOrderRawSquare`
22. `fivefoldP77RawPatchRefinementOrderRawLoop`
23. `fivefoldP77RawPatchRefinementOrder_pullback`
24. `fivefoldP77RawPatchRefinementOrder_intermediate`
25. `fivefoldP77RawPatchRefinementLeftThenRight_certify`
26. `fivefoldP77RawPatchRefinementRightThenLeft_certify`

既存Lean本文、定理の名前・仮定・結論、固定Lean/mathlib、CI workflows、公開root107を維持。strict空を中心とし、独立Kuuはpresentation、元F55/P77/P94A・物理C60・北C60 CRTはそれぞれの出典・型を保持する。

## 10. 検証と次の段階

初回CI [#42119709213](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42119709213)は二つの実装上の原因で失敗した。

1. 公開集約の新importを末尾のモジュール説明コメントの後に置いた。固定Leanの /-! モジュール文書は通常の空白コメントではなくコマンドであり、そこでimportヘッダーが終了する。既存v4.73のimport直後、モジュール説明の前へ新importを配置した。既存集約の本文は保持した。
2. Pullbackのpresentation枝で、関数Typeが必要な箇所へ裸のEquiv.symm値をexactで渡した。この箇所では関数へのcoercionが挿入されず、後続の経路保存証明も失敗した。fun witness => equiv.symm witness と明示的に適用する関数へ変更した。失敗時のsorryAxはLeanのエラー回復による未完成定義の伝播であり、最終成功ログで全26宣言から消失したことを確認した。

新規ファイル全文、公開集約全文、元v4.68〜4.73の依存シグネチャ、固定mathlibのEquiv API、固定LeanのmoduleDoc parserを照合して修正した。定理の仮定・結論は不変。修正コミットはbb8e6576d012fe8857c77070fef053c03dd8fc6c。

参考一次資料：[固定Lean v4.30.0-rc2のCommand parser](https://github.com/leanprover/lean4/blob/v4.30.0-rc2/src/Lean/Parser/Command.lean)、[固定mathlibのEquiv定義](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/Logic/Equiv/Defs.lean)、[Lean公式・Source Files and Modules](https://lean-lang.org/doc/reference/latest/Source-Files-and-Modules/)、[Lean公式・Coercing to Function Types](https://lean-lang.org/doc/reference/latest/Coercions/Coercing-to-Function-Types/)。

最終CI #42120339598でworkflow・job・Lean stepの終了を確認し、全10,271ビルド、Governance30件、新規公理出力26件、変更ファイルのwarning/error 0/0、source/test-merge Git tree一致を再観測した。検証済みHEADを指定してsquashマージした。

次のQi v4.75候補は、任意有限個の独立した因子計画に対し、隣接交換による細分順序変更とrecutを組み合わせた実比較diagramを構成すること。今回の二因子の原始順序図式を再利用し、全添字の対応、元source経路、指定階層obstructionを保持する。異なるraw五セル履歴を等置する新たなhigher coherenceは別の証明課題である。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
