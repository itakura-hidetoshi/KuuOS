# Qi v4.73 — 元P77の証拠付き混合細分と真正raw五セル比較

## 0. 検証済み正本

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS、canonical branch：main。
- 継承：Qi v4.68（有限recut）、v4.69（段別真正五セル比較）、v4.70（証拠付き段分割・統合と因子別障害）、v4.71（元統合パッチ族の真正五セル比較）、v4.72（raw切断木の真正五セル正規形）。
- 定理PR：[ #3168 ](https://github.com/itakura-hidetoshi/KuuOS/pull/3168) — MERGED。
- 定理基点：3493fefe780faa657e44a7341fc836c09e121651。
- exact-source検証HEAD：ccdef1ce8339a2c234e6f55ee2870fa2d54ec0d8。
- 定理squash：d476f2eae3b8115a3addbb4d0db68939e4b72d96。
- source/test-merge Git tree：6b70774a711a2fcff3599218908403f9d5ea077d — 完全一致。
- [exact-source CI #42116672588](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42116672588)：SUCCESS。
- Strict Lean：**10,270 / 10,270 SUCCESS**。
- Governance：**30 / 30 SUCCESS**。
- GitHub workflow jobs：32/32 terminal、check runs：41/41 terminal（40 success、1 expected skip）。
- exact-head Strict Lean／terminal status：両方success。
- 新規20宣言の実際の公理出力：propext／Classical.choice／Quot.sound のみ。**sorryAx 0**。
- 変更Lean warning/error：0/0。
- Lean：v4.30.0-rc2、mathlib：5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、root107、保護PR #1558 Draft／OPEN／未マージ。

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CertifiedMixedSubdivisionFiveCellV4_73.lean) · [v4.72正式記録](Qi-v4_72-original-P77-raw-cut-tree-five-cell-coherence.md) · [v4.70正式記録](Qi-v4_70-original-P77-certified-segment-subdivision.md)

## 1. 研究の位置づけと新しい問い

v4.72では、任意の型付き切断木Tにおける元raw四セルの括弧付き合成と、平坦化したraw鎖の正規形との間に、真正GK5CG保守的Type値五セルを帰納構成した。しかしv4.70の証拠付き段分割・統合は、元sourceの段数と中間頂点を実際に変更する操作である。

今回の中心は、**段数・中間頂点・raw括弧・raw表示を変える任意有限の証拠付き履歴そのものから、各両端のrawパッチ族を結ぶ本物のGK5CG五セルを構成できるか**という問いである。

元raw四セル、元五セル構成子、元source Quiver.Path、到達証拠付きP77部分Hom、元選択履歴は互いに権限境界を持つ別のデータである。結果を単なる数値chargeの一致や任意に仮定した証拠Type同値へ置き換えない。

## 2. 単一粗ブロックには真の右単位五セルがある

v4.70の粗い一段ブロックBを切断木へ埋め込むと、単なるBではなく

    BlockTree(B) = leaf(cons B (nil v))

となる。このraw添字は I_B×PUnit で、raw代表は B(i) ; refl_v となる。したがって raw tree block とBを定義的に同一視せず、元GK5CGの保守的な verticalRightUnit 五セルとその逆を用いる。

$$
B(i); \mathrm{refl}_v
\xRightarrow{\text{GK5CG right-unit}}
B(i).
$$

新規 fivefoldP77RawPatchBlockTreeRawComparison は、全てのiに対してこの五セルを前向きに、逆五セルを後向きに持ち、添字も双方向に明示する。

## 3. 一段粗木から任意細い切断木への真正五セル

細いtree Tの元raw鎖をN(T)、実際のraw合成ブロックをComp(N(T))とする。v4.70の細分生成元には、元の両方向比較

$$
c:\operatorname{Comparison}(\operatorname{Comp}(N(T)),B)
$$

と実際のfine source証拠が既に含まれている。

今回の fivefoldP77RawPatchTreeSubdivisionRawComparison は、次の三種類の**実際のGK5CG五セル比較**を合成する。

$$
\boxed{
\operatorname{RawBlock}(\operatorname{BlockTree}(B))
\xRightarrow{\;\mathrm{right\ unit}\;} B
\xRightarrow{\;c^{-1}\;} \operatorname{Comp}(N(T))
\xRightarrow{\;\nu_T^{-1}\;} \operatorname{RawBlock}(T).
}
$$

ここでν_Tはv4.72で構成した元raw切断木の真正五セル正規化である。全raw代表を覆う添字写像と元五セルType値を保持する。直接の「粗木＝細木」や、元raw四セルの構文等号は仮定しない。

このraw比較の構成は五セル比較データから可能だが、**証拠付きsubdivide route自体はv4.70に従い実際のfine source witnessを必要とする**。この二つは論理的に異なる。

## 4. 任意左右文脈では元五セルcongruenceを実構成

あるraw切断木S,Tの比較cが存在するとき、共通の右文脈Rを結合したnode(S,R)とnode(T,R)の比較を構成する。

$$
\alpha_j:R_S(\varphi(j))\Rightarrow R_T(j)
\quad\mapsto\quad
\operatorname{verticalLeft}(\alpha_j,R_R(k))
$$

を**すべての右添字k**について実行する。元raw五セルに対し、左と右のraw四セルを垂直congruenceで結ぶ操作である。後向きでも独立の比較五セルを同様に貼る。

共通の左文脈Lを持つnode(L,S)とnode(L,T)では、元の verticalRight 構成子を全左添字iに対して使う。

新規 fivefoldP77RawPatchTreeRawComparison_left/right は、元sourceの型付き中間頂点、すべてのrawパッチ添字組と真正五セル値を保持する。

## 5. 任意有限の証拠付き混合履歴にraw五セルを昇格

v4.70の既存の帰納Type FivefoldP77RawPatchSubdivisionRoute を新しく捏造せず、各コンストラクタを真正五セル比較へ翻訳する。

| 元の履歴生成元 | raw五セルの構成 |
|---|---|
| presentation | v4.72の真正raw tree比較 |
| recut | v4.72の元raw切断木の真正五セル比較 |
| subdivide | 前節の右単位・細分比較・raw正規化五セルの合成 |
| symm | 実際の元五セル比較の前後を反転 |
| trans | 双方向の元五セル比較を垂直合成 |
| left | 元のverticalLeftによる文脈congruence |
| right | 元のverticalRightによる文脈congruence |

これを v4.69のRawPatchPresentationRoute と v4.70のRawPatchSubdivisionRoute の二層で帰納構成し、

$$
\boxed{
r:\operatorname{SubdivisionRoute}(S,T)
\Longrightarrow
\operatorname{GK5CGComparison}(\operatorname{RawBlock}(S),\operatorname{RawBlock}(T))
}
$$

を得る。いずれも本物の元保守的五セルであり、任意にRawBlockEquivを入力しただけの定理ではない。

## 6. source証拠の存在に先立つraw保守的商比較

新規比較c_rは各jに対する前向き・後向きの真正五セル値を持つため、元GK5CGの既存商定理から

$$
[ R_S(\mathrm{forwardIndex}_r(j)) ]
=
[ R_T(j) ]
$$

および逆側の比較商等式を得る。この式は、与えられた正規化・比較・細分の五セルデータがある場合、個々のsource witnessを引数として要求しない。

さらに元GK5CGのassocCharge_soundにより元結合子chargeの一致が帰結として得られる。ただし**charge等号だけから元五セルを復元する逆方向**は用いない。

## 7. 実際のgluingと元source経路の自然性

source treeの真正証拠wがあるとき、v4.72の元raw tree gluingと今回のraw五セル比較、v4.70の混合履歴の証拠付きEquivは可換となる。

$$
\boxed{
E_{\mathrm{raw}(r)}(G_S(w))
=
G_T(E_r(w)).
}
$$

証明は、元のBlockComparisonEquivが全ての型付きsource Quiver.Pathをそのまま保持すること、RawGlueが元TreePathに等しいこと、v4.70のSubdivisionRoute_pathが同じ元経路を保存することから、Subtype.extで厳密に成立する。

さらに、元のFivefoldP77PartialDomainの値そのものが一致すること、逆routeの自然性、任意有限のraw比較の合成、同じ始点・終点を持つ異なる履歴の誘導したwitness Equivの一致を形式化した。全4辺が実在する証拠付き比較四角形の可換性も、元P77 source faithfulnessから既証明のwitness subsingleton性を用いて導く。

**重要：** ここで一致するのは誘導された証拠Typeの写像であり、選んだ元五セルの履歴自身ではない。元raw五セルを同一視する新higher coherenceやpentagonatorは今回追加しない。

## 8. 粗いobstructionと指定factorwise obstructionの分離

任意有限の許された証拠付きrouteでは、元rawブロックのcompatibilityが真正比較に沿って双方向に保存される。他方、元treeの指定factorwise compatibility・obstructionは既存v4.70の証拠付きrouteによって保存される。

ただし、**粗い元P77合成がsourceで到達可能であることは、指定した細い段分割がsourceで実現可能であることを含意しない**。

v4.70の具体例では、元逆e01:1→0と順e01:0→1を合成した粗rawは、元nil source経路で実現できる。しかし最初の指定逆向き段はsourceに原像がなく、細い二段証拠は空である。

今回、さらに強く次を証明した。

$$
\boxed{
\begin{aligned}
&\operatorname{Nonempty}(
\operatorname{GK5CGComparison}(
\operatorname{RawBlock}(\operatorname{BlockTree}(B)),
\operatorname{RawBlock}(\operatorname{leaf}C_{\mathrm{bad}})))\\
&\quad\land\\
&\neg\operatorname{Nonempty}(
\operatorname{SubdivisionRoute}(
\operatorname{BlockTree}(B),
\operatorname{leaf}C_{\mathrm{bad}})).
\end{aligned}
}
$$

左側の実五セルは、元right-unit五セルとv4.72の正規化五セルから構成できる。右側の不存在は、仮に証拠付きrouteがあればcoarse witnessをfine witnessへ移送でき、元逆e01のsource未到達定理に矛盾することから得る。

この事実により、**Type値raw五セル比較の存在と真正因子別descentの可能性の論理的差異**を、具体的な元データで保持できた。

## 9. 全20宣言と独立レビュー

1. fivefoldP77RawPatchBlockTreeRawComparison
2. fivefoldP77RawPatchTreeSubdivisionRawComparison
3. fivefoldP77RawPatchTreeRawComparison_left
4. fivefoldP77RawPatchTreeRawComparison_right
5. fivefoldP77RawPatchPresentationRouteRawComparison
6. fivefoldP77RawPatchSubdivisionRouteRawComparison
7. fivefoldP77RawPatchSubdivisionRoute_rawClass_forward
8. fivefoldP77RawPatchSubdivisionRoute_rawClass_backward
9. fivefoldP77RawPatchSubdivisionRoute_rawCharge_forward
10. fivefoldP77RawPatchSubdivisionRouteRawGlue_natural
11. fivefoldP77RawPatchSubdivisionRoute_rawCertified_natural
12. fivefoldP77RawPatchSubdivisionRouteRawGlue_symm_natural
13. fivefoldP77RawPatchSubdivisionRoute_rawCompatible_iff
14. fivefoldP77RawPatchSubdivisionRoute_fineObstructed_iff
15. fivefoldP77RawPatchSubdivisionRoute_rawEquiv_independent
16. fivefoldP77RawPatchSubdivisionRoute_rawEquiv_trans
17. fivefoldP77RawPatchSubdivisionRoute_rawSquare
18. fivefoldP77ReverseForward_noCertifiedMixedSubdivision
19. fivefoldP77ReverseForward_rawOnlyComparison
20. fivefoldP77ReverseForward_rawComparison_notCertifiedRoute

新規465行のLeanファイル一件と公開集約KuuOSFormalのimport1行のみを追加。旧Lean本文、既存定理の仮定・結論・名前、固定Lean/mathlib、CI workflows、public root107は不変とした。

## 10. exact-source成功と次の段階

CI #42116672588で固定Lean10,270/10,270、Governance30/30、実公理出力20件を確認した。変更Lean warning/errorは0/0、新規sorryAxはない。GitHub PR headとtest-merge treeが完全一致し、検証済みHEADを指定してsquashマージした。後続main commit d476f2eae3b8115a3addbb4d0db68939e4b72d96のGit treeも一致している。

研究のauthority境界は元F55/P77/P94Aと物理C60 Gauge、北C60 CRTで独立に保持する。strict 空中心、独立Kuuはpresentationであり、比較可能性を同一視命令に置換しない。

**Qi v4.74候補：** 連続する複数の証拠付き段分割順序について、実五セルを保持した比較diagramの構成と、粗・細・中間のcompatibilityを指定階層ごとに追跡する。比較履歴間のraw五セル同一性、無条件なsheaf descentや新pentagonator・Grayは導入しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
