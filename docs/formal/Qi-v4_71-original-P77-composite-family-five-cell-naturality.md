# Qi v4.71 — 真正元P77統合パッチ族の五セル比較と細分fiberの自然性

## 0. 定理正本・検証記録

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS、正本branch：main。
- 継承元：Qi v4.69の元rawパッチ表示比較、Qi v4.70の証拠付き段分割・統合。
- 定理PR：[ #3164 ](https://github.com/itakura-hidetoshi/KuuOS/pull/3164) — **MERGED**。
- 定理基点：e99d04d3c48d83b0bb099181b8cd1249dc6f8be9。
- 修正済みexact-source検証HEAD：cd409432e4f5f9c113d8c6b5bf1a74dbef673166。
- squash merge：2bb2ddd04b92ff18009b9fb54e20f1769fae49b3。
- source/test-merge tree：624c2f7091a77f3e1ad04ae267390c56a9d5b4b6 — 完全一致。
- テストmerge：0e6b9c940a82bb2dce47a3c70b8fee03c484e712。
- exact-source CI：[ #42104411499 ](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42104411499) — **SUCCESS**。
- Strict Lean：**10,268 / 10,268 SUCCESS**、Governance：**30 / 30 SUCCESS**。
- 32 workflow jobsすべてterminal、41 check runsすべてterminal（40 success、1 expected skip）。
- 新規17宣言の実際の公理出力：標準propext／Classical.choice／Quot.soundのみ、**sorryAx 0**。
- 変更Lean warning/error：**0/0**。両exact-head完了ステータス：success。
- Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、公開root107、保護PR #1558 Draft／OPEN／未マージ。

[新規Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CompositeFiveCellNaturalityV4_71.lean) · [前段v4.70](Qi-v4_70-original-P77-certified-segment-subdivision.md) · [前段v4.69](Qi-v4_69-original-P77-patch-presentation-naturality.md)

## 1. 研究目的とauthority境界

v4.69では、元の中間source頂点を変えずに各段のraw四セルパッチ族を比較する構造を構成した。各段の比較は両方向の添字写像と全代表に対する真正GK5CG Type値五セルを保持する。

v4.70では、任意有限段のraw四セルを全添字組について実際に合成し、真正source証拠を持つ場合に細い鎖から統合パッチ族へのgluingを構成した。しかし粗いsource到達可能性だけでは指定された細い因子のsource証拠がない場合がある。

v4.71では、段別の真正五セルから**統合パッチ族そのものの真正五セル比較を構成**する。比較構成は元source witnessの非空性を前提とせず、局所障害を型付きデータとして保持する。

## 2. 全添字組の双方向比較

同じ型付き中間境界を持つ有限依存鎖を C=(B₁,…,Bₙ) と C′=(B₁′,…,Bₙ′) とする。各段には前向きインデックス写像 φ_j と後向き写像 ψ_j があるが、互いに逆写像とは仮定しない。

$$
I_C=I_1\times\cdots\times I_n\times\mathbf 1,
\quad
I_{C'}=I'_1\times\cdots\times I'_n\times\mathbf 1.
$$

新規の fivefoldP77CompositeComparisonForwardIndex と fivefoldP77CompositeComparisonBackwardIndex は、各段の写像の再帰的積を構成する。

$$
\Phi:I_{C'}\to I_C,\qquad \Psi:I_C\to I_{C'}.
$$

元の非空添字Typeの全組を保持する。任意の組を省略したり、局所パッチを選択的に取り除いたりしない。

## 3. 元GK5CG五セルの実際の垂直貼り合わせ

各段のraw四セルを R_j と R'_j、前向きに与えられた真正五セルを

$$
\alpha_j(i):\operatorname{GK5CGCell}
\bigl(R_j(\varphi_j(i)),R'_j(i)\bigr)
$$

と表す。headとtailに分けた再帰の一段で、次の元の保守的五セル構成子を実際に使う。

$$
\boxed{
\alpha_{\mathrm{cons}}
=
\operatorname{verticalLeft}(\alpha_{\mathrm{head}},R_{\mathrm{tail}})
\mathbin{;}
\operatorname{verticalRight}(R'_{\mathrm{head}},\alpha_{\mathrm{tail}})
}
$$

空鎖の比較は元のrefl五セルで開始する。後向きにも各段の別の真正五セル値を使って同様に構成する。

新規定義 fivefoldP77CompositeComparisonForwardCell、fivefoldP77CompositeComparisonBackwardCell、fivefoldP77CompositeBlockComparison は、任意の全添字組に対して**元四セルの合成間の真正Type値五セル**を生成する。仮定していたのは段ごとの五セル比較であり、統合族間の比較の存在そのものではない。

## 4. 商等式および整数chargeの意味

元の五セルを構成した後、既存の fivefoldP77ConservativeClass_eq_iff によって、前向き全代表の元P77商等式

$$
[R_C(\Phi(i))]=[R_{C'}(i)]
$$

を証明する。同じく後向きの全代表にも等式を得る。

さらに元のassocCharge_sound定理により、実際に比較されたraw四セルの符号付き結合子chargeが等しい。

$$
Q_{\mathrm{GK5CG}}(R_C(\Phi(i)))
=
Q_{\mathrm{GK5CG}}(R_{C'}(i)).
$$

このchargeの等式は実五セルから導かれる帰結であり、数値chargeの一致から五セルが存在するという逆推論ではない。証拠付き元四セル・五セルの履歴は独立したType値データとして保持する。

## 5. gluing自然性：元source経路を保存

真正な因子別source証拠 w∈W(C) が存在する場合、v4.69の細い鎖の比較同値と、v4.70のgluing、今回の統合族比較は可換となる。

$$
\boxed{
E_{\mathrm{comp}(c)}(G_C(w))
=
G_{C'}(E_c(w)).
}
$$

Lean定理 fivefoldP77CompositeComparison_glue_natural は、段別比較による元Quiver.Pathの保存とSubtype外延性から、この等式を証明する。任意のwについて左右のsource経路が完全に一致し、元の有向source経路を新たに作ることはない。

## 6. 粗いcompatibilityと細いfactorwise compatibilityの分離

元五セル比較に沿い、粗い合成族のcompatibilityは

$$
\mathrm{Compatible}(\mathrm{CompositeBlock}(C))
\iff
\mathrm{Compatible}(\mathrm{CompositeBlock}(C'))
$$

として保存される。

同時に、段別の真正比較に沿う細いsource因子のcompatibilityとsource witnessの不存在も、別の定理で双方向に保存される。

$$
\mathrm{Compatible}(C)\iff\mathrm{Compatible}(C').
$$

粗い元source経路が存在することと、指定した段分割に沿って各因子の真正source経路が存在することは異なる。v4.70の逆e01・順e01の元raw合成は粗いnil source経路で復元できる一方、最初の指定逆向き因子は復元できない。このobstructionを今回の比較では消さない。

## 7. 固定粗証拠の細分fiber自然性

細い鎖の真正比較 c:C→C′、粗いパッチ族の真正比較 b:B→B′、固定された粗い証拠 q:W(B) が与えられた場合、v4.70の指定細分fiberは

$$
\mathrm{Fib}_{C,B}(q)
=\{w:W(C)\mid\mathrm{Path}_C(w)=q.\mathrm{val}\}
$$

と定義される。

新規の fivefoldP77SubdivisionFiberComparisonEquiv は、実際のType値で

$$
\boxed{
\mathrm{Fib}_{C,B}(q)\simeq
\mathrm{Fib}_{C',B'}(E_b(q))
}
$$

を構成する。前向き・逆向きに既存の真正chain Equivを使い、元source経路の等号もtransportする。左右の逆法則は実際にLeanで証明され、非空性の必要十分条件も得られる。

双方が空fiberであっても同値は成立する。しかし空fiberから新しい因子別source証拠を生み出すものではない。

## 8. 証拠付き細分routeの正確な境界

fivefoldP77CompositeComparisonAsSubdivisionRoute は、構成した真正統合族比較を段分割用に反転し、**実際のtarget fine witnessを追加で渡したとき**、v4.70のType値Finite Subdivision Routeを具体的に構成する。

この構成でsource pathの厳密保存と、実際の両側fine witnessが与えられた場合の元段別比較結果との一致を証明した。任意の粗いsource経路があるという事実だけでは、このrouteの生成元に必要なfine witnessは得られない。

## 9. 全17宣言

1. fivefoldP77CompositeComparisonForwardIndex
2. fivefoldP77CompositeComparisonBackwardIndex
3. fivefoldP77CompositeComparisonForwardCell
4. fivefoldP77CompositeComparisonBackwardCell
5. fivefoldP77CompositeBlockComparison
6. fivefoldP77CompositeComparison_class_forward
7. fivefoldP77CompositeComparison_class_backward
8. fivefoldP77CompositeComparison_charge_forward
9. fivefoldP77CompositeComparison_glue_natural
10. fivefoldP77CompositeComparison_coarseCompatible_iff
11. fivefoldP77CompositeComparison_fineCompatible_iff
12. fivefoldP77CompositeComparison_fineMissing_iff
13. fivefoldP77SubdivisionFiberComparisonEquiv
14. fivefoldP77SubdivisionFiberComparison_nonempty_iff
15. fivefoldP77CompositeComparisonAsSubdivisionRoute
16. fivefoldP77CompositeComparisonSubdivision_path
17. fivefoldP77CompositeComparisonSubdivision_agrees

新規Leanモジュールのみを追加し、公開集約KuuOSFormalにはimport一行だけを追記。旧Leanソース本文、既存宣言の型、旧定理の仮定、toolchain、mathlib manifest、workflowを変更しない。

## 10. 初回Leanエラーの構造理由と最小修正

初回HEAD b85af25c983594ae3208c295d0b91b022d47a0ff のCI #42103620455では、先行16宣言をLeanがコンパイルしたが、最後の定理で次の型クラス推論エラーが出た。

> failed to synthesize instance: Subsingleton (FivefoldP77RawPatchTreeWitness f g h k (FivefoldP77RawPatchCutTree.leaf target))

原因はChainWitnessの一意性を局所登録しても、結論で使うTreeWitness (.leaf target) のSubsingletonを型クラス推論が自動的に見つけなかったためである。新規ファイル全文とv4.68・v4.69・v4.70の依存定義と既存mathlib APIを照合した。

既存v4.68で形式証明済みの fivefoldP77RawPatchTree_witness_subsingleton によって結論の正確なTypeに局所instanceを明示した。修正は最後の証明の1 hunkのみ。数学的仮定・結論、五セル構成、既存のソースには変更がない。修正HEAD cd409432e4f5f9c113d8c6b5bf1a74dbef673166 は固定Leanで成功し、全17宣言の公理出力にsorryAxがなくなった。

## 11. exact-source検証とmain再観測

修正HEADのsource/test-merge Git treeは624c2f7091a77f3e1ad04ae267390c56a9d5b4b6で完全一致。CI #42104411499のStrict LeanとGovernance30/30、全32 workflow jobs、全41 check runs、両exact-head完了ステータスがSUCCESSになった。

検証済みHEADを指定してsquashマージし、定理main commit 2bb2ddd04b92ff18009b9fb54e20f1769fae49b3 のtreeが同じ624c2f7091a77f3e1ad04ae267390c56a9d5b4b6であることを独立再観測した。

## 12. 守る境界と次段階

strict 空を中心とし、独立Kuuを一つのpresentationとする。元F55/P77/P94A、物理C60 Gauge、北C60 CRTのauthorityと元のType値source履歴を保持する。今回、全targetのfullness、指定因子の無条件復元、chargeからの五セル生成、source逆辺、一般siteの無条件sheaf descent、新pentagonator・Gray復元を証明したとは主張しない。

**次段候補Qi v4.72：** 真正な統合比較と任意有限recut・再括弧化・反復細分を相互接続し、選んだ元比較履歴を消去せず、元source経路と部分Homの自然性・obstructionの保存を形式化する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
