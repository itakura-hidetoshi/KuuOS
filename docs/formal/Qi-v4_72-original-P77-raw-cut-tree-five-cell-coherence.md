# Qi v4.72 — 真正元P77 raw切断木の五セル正規化と有限recut自然性

## 0. 正本・検証

- 日付：2026-11-06 JST。
- Repository：itakura-hidetoshi/KuuOS、canonical branch：main。
- 継承元：Qi v4.68（有限cut tree／recut）、Qi v4.69（各段の真正五セル比較）、Qi v4.70（細分・統合）、Qi v4.71（真正統合パッチ五セル）。
- 定理PR：[ #3166 ](https://github.com/itakura-hidetoshi/KuuOS/pull/3166) — **MERGED**。
- 開始main：0d9dd753d83adcf8b53b2d3084a6de4cc174e46f。
- 修正後exact-source検証HEAD：17f0124f60c9bdf1d509d08fa67512836fee4789。
- 定理squash：8421b313e63450699f488c5fda8dc4c00833b781。
- source/test-merge Git tree：37273a70c0d16c5dc0ece14bbe46e57a1b6652dd — **完全一致**。
- テストmerge：464807eecaee76a27ecc4af05fcdd86297ec28e5。
- exact-source [CI #42108956252](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42108956252) — **SUCCESS**。
- Strict Lean：**10,269 / 10,269**。
- Governance：**30 / 30 SUCCESS**。
- 新規19宣言すべての実際の公理出力：propext／Classical.choice／Quot.soundのみ、**sorryAx 0**。
- 変更Lean warning/error：**0 / 0**。
- 32 workflow jobsすべてterminal、41 checksすべてterminal（40 success／1 expected skip）。
- GitHub exact-head Strict Lean／terminal完了ステータス：両方success。
- Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、root107、保護PR #1558 Draft／OPEN／未マージ。

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77RawCutTreeFiveCellCoherenceV4_72.lean) · [v4.71正式証明記録](Qi-v4_71-original-P77-composite-family-five-cell-naturality.md) · [v4.70正式証明記録](Qi-v4_70-original-P77-certified-segment-subdivision.md)

## 1. 新しい問い：証拠付き経路ではなくraw四セルそのものを比較する

v4.68では有限切断木Tに元rawパッチ列の平坦化N(T)があり、証拠Typeには実際のEquivがある。v4.69では異なるパッチ族の真正GK5CG五セル比較を保持する。v4.71では各段の五セルから**正規化済みの統合パッチ族**に対する真正五セル比較を構成した。

しかし、切断木の各nodeでraw四セルを実際に合成すると、その括弧付けは平坦化の右結合的なraw値と構文的には異なる。両者を単にsource証拠写像の一意性やcharge等式で同一視することは元Type値歴史の削除に相当する。

今回、**任意のraw切断木に対して真正な元五セル値を構成し、括弧付きraw値を正規形の元raw値へ比較する**。

## 2. 全パッチ添字の積を保持する依存Equiv

型付き元rawパッチ鎖L:u→vとR:v→wを考える。新定義 fivefoldP77RawPatchChainAppendIndexEquiv は、両側の実際の全添字を結ぶ。

$$
\boxed{
(I_L\times I_R)\simeq I_{L\mathbin{+\!\!+}R}
}
$$

nil左鎖の場合はPUnitとの積に対する明示的逆、consの場合は固定mathlibのEquiv.prodAssocとEquiv.prodCongrを用いて帰納構成する。

型付き切断木Tの添字Typeを

$$
I_{\mathrm{leaf}(C)}=I_C,\qquad
I_{\mathrm{node}(L,R)}=I_L\times I_R
$$

と定義する。新たな fivefoldP77RawPatchTreeIndexNormalizeEquiv は全ての中間型付き境界とraw添字を保持したまま

$$
N_I(T):I_T\simeq I_{N(T)}
$$

を構成する。全葉の添字が非空なら全tree添字も非空になることを別途証明した。

## 3. 括弧付き元raw四セルと真正五セルの帰納構成

従来のRawPatchChainRawは、各鎖の右結合されたraw四セル合成を保持する。新定義 fivefoldP77RawPatchTreeRaw では括弧付き切断木そのもののraw四セル合成を保持する。

$$
R_{\mathrm{leaf}(C)}(i)=R_C(i),
\qquad
R_{\mathrm{node}(L,R)}(i,j)=
R_L(i)\mathbin{;}R_R(j).
$$

付随する重要定理は、元GK5CG保守的五セルTypeの実際の値

$$
\boxed{
\nu_T(i):
\operatorname{GK5CGCell}\bigl(
R_T(i),
R_{N(T)}(N_I(T)(i))
\bigr)
}
$$

を**任意有限treeと全添字**について構成することである。

まずchain appendについて、空左鎖では元のverticalLeftUnit五セルを逆向きに使用する。consの場合にはtailの帰納五セルを左からwhiskerし、元のverticalAssocを逆向きに合成する。

$$
R_{L+\!\!+R}(N_{L,R}(i,j))
\xRightarrow{\;\text{真の五セル}\;}
R_L(i)\mathbin{;}R_R(j).
$$

tree nodeでの帰納段階は、左部分treeの五セルをverticalLeftで、右部分treeの五セルをverticalRightで実際に貼り合わせ、appendの五セルを必要な向きに接続する。単にsource経路の等号を後付けで置くのではない。

これは元F55/P77のraw四セルgrammarと、元GK5CGの保守的五セルgrammarの間の型付き構成である。**新しいpentagonator生成元は導入しない**。

## 4. raw treeごとの統合パッチ族と両方向比較

新規 FivefoldP77RawPatchTreeRawBlock は、treeにおける全添字と括弧付きraw四セルを持つ実際の粗いパッチ族を作る。

fivefoldP77RawPatchTreeRawNormalizeComparison では、上記N_I(T)の前・逆両写像と、実際のν_T(i)、ν_T(i)の逆五セルを結合し、v4.69の真正な双方向BlockComparison構造を構成する。

$$
\boxed{
\mathrm{BlockComparison}
\bigl(\mathrm{RawBlock}(T),\mathrm{CompositeBlock}(N(T))\bigr)
}
$$

両方の全代表に元Type値五セルが実在する。途中のraw括弧が異なっても、元パッチ・元source境界を消去せず、元保守的P77商の比較に導ける。

## 5. 任意有限recutと異なる表示比較への拡張

異なる木S、Tについて、それぞれの平坦化元鎖を結ぶv4.69の実際のChainComparison c が与えられれば、前節の両正規化比較とv4.71の統合族比較を、元GK5CG五セルの垂直合成で貼り合わせる。

$$
\mathrm{RawBlock}(S)
\xRightarrow{\;\nu_S\;}
\mathrm{CompositeBlock}(N(S))
\xRightarrow{\;\mathrm{Comp}(c)\;}
\mathrm{CompositeBlock}(N(T))
\xRightarrow{\;\nu_T^{-1}\;}
\mathrm{RawBlock}(T).
$$

この真正比較は fivefoldP77RawPatchTreeRawComparison によって構成する。

また、元v4.68の任意有限CutRoute r:S→T がある場合は、既証明の厳密な平坦化等式N(S)=N(T)から反射的なChainComparisonを構成し、上記のraw比較へ挿入する。結果として、任意有限recut・再括弧付け・左右文脈に対して**括弧付きraw四セル族間の本物の五セル比較**が得られる。recutの存在しない異なるraw列間に無条件比較があるとは主張しない。

## 6. 実際のsource証拠・gluingと自然性

元のtree証拠 w:W(T) がある場合は、v4.68の証拠正規化とv4.70の実際のCompositeGlueを組み合わせ、今回の真正BlockComparisonを逆向きに通して元raw tree族へのgluing

$$
G_T:W(T)\to W(\mathrm{RawBlock}(T))
$$

を構成する。新定理 fivefoldP77RawPatchTreeRawGlue_val は

$$
\boxed{
G_T(w).\mathrm{val}=\operatorname{Path}_T(w)
}
$$

を元の型付きQuiver.Pathの等式として証明する。

したがって表示比較の四角形は

$$
E_{\mathrm{raw}(c)}\bigl(G_S(w)\bigr)
=
G_T\bigl(E_{\mathrm{tree}(c)}(w)\bigr)
$$

で可換となる。同様にCutRoute r によるrecutについて

$$
E_{\mathrm{raw}(r)}\bigl(G_S(w)\bigr)
=
G_T\bigl(E_r(w)\bigr)
$$

を形式証明した。いずれもsource側の元経路がそのまま保存される。独立した比較履歴が誘導する元BlockWitness上のEquivは一致するが、raw五セル履歴それ自体の等号は導かない。

## 7. 局所obstructionと段分割の境界

今回の五セル正規化は**rawの括弧付けを変える**ものであり、source経路を存在しない段に付け足すものではない。v4.68の指定因子別obstruction定理を継承し、元CutRouteによってその因子の証拠不存在が解消しないことを確認した。

v4.70の逆e01と順e01の合成を例に取れば、粗い統合族はnil source経路を持ち得るが、指定された逆向き細分因子はsourceに原像がない。今回の括弧付け正規化がその因子別障害を消すことはない。

v4.70の一般の段分割・統合をraw切断木の新構成子へ拡張してすべての反復細分順序を直接比較する仕事は、次段v4.73に残す。したがって無条件の全target fullness、任意targetのfactor逆復元、新しいsource逆辺、一般siteのsheaf descent、raw五セル履歴の一律同一視、新pentagonator・Grayは主張しない。

## 8. 新規19宣言

1. fivefoldP77RawPatchChainAppendIndexEquiv
2. fivefoldP77RawPatchChainAppendRawFiveCell
3. FivefoldP77RawPatchTreeIndex
4. fivefoldP77RawPatchTreeIndexNormalizeEquiv
5. fivefoldP77RawPatchTreeRaw
6. fivefoldP77RawPatchTreeRawNormalizeFiveCell
7. fivefoldP77RawPatchTreeIndex_nonempty
8. fivefoldP77RawPatchTreeRawBlock
9. fivefoldP77RawPatchTreeRawNormalizeComparison
10. fivefoldP77RawPatchTreeRawComparison
11. fivefoldP77RawPatchChainComparisonRefl
12. fivefoldP77RawPatchChainComparisonOfEq
13. fivefoldP77RawPatchCutRouteRawComparison
14. fivefoldP77RawPatchTreeRawGlue
15. fivefoldP77RawPatchTreeRawGlue_val
16. fivefoldP77RawPatchTreeRawGlue_presentation_natural
17. fivefoldP77RawPatchTreeRawGlue_recut_natural
18. fivefoldP77RawPatchTreeRawComparison_equiv_independent
19. fivefoldP77RawPatchTreeRaw_obstruction_recut

## 9. 初回CI失敗とLean 4記法の修正理由

初回HEAD 21c39f4ebbdd766ea64aa80ae6cf436b048f68c5 のCI #42108164651では、新しい最初の定義 fivefoldP77RawPatchChainAppendIndexEquiv の帰納仮定ihに予期せず右鎖引数が残った。これは左の依存型鎖に関するinductionで、右鎖が型依存により一般化されたためである。

元の固定mathlib Equiv.prodAssoc/Equiv.prodCongrに渡すべきIHは単なるihではなく、実際の右鎖を明示した ih right である。続くappend raw五セルの再帰も同じ依存型一般化により ih right rest j が必要だった。

また verticalLeftUnit は複数の5-cell／4-cell grammarに存在するため、逆操作 symm を付けた括弧内ではドット記法から意図したconstructerを推論できなかった。そこで完全修飾された NativeGK5CGConservativeFiveCell.verticalLeftUnit を明示した。

変更は新規モジュールのこれらの箇所に限定し、既存定理の仮定・結論・実五セルの向きを弱めたり変更したりしない。修正後のHEAD 17f0124f60c9bdf1d509d08fa67512836fee4789 は Strict Lean 10,269/10,269で成功し、19公理出力は標準公理のみ、sorryAxなしとなった。

## 10. Git tree・authority

新規447行のLeanファイルと公開集約KuuOSFormalへのimport1行だけを追加した。旧Lean本文、既存定理署名、toolchain、mathlib pin、workflowを不変にした。正本mainへ検証済みHEADを指定してsquashマージし、Git tree 37273a70c0d16c5dc0ece14bbe46e57a1b6652ddが検証済みsource/test-mergeと一致することを再観測した。

strict 空中心と独立Kuu presentation、元F55/P77/P94A・物理C60 Gauge・北C60 CRTのauthorityと元Type値履歴を保持する。今回の比較は保守的五セルgrammar内のものであり、元のペンタゴン上経路と下経路を同一視する新pentagonator証拠ではない。

## 11. 次の段階

**Qi v4.73候補：** 証拠付き段分割を含めた反復細分順序と、今回構成した真正raw tree比較・recut・表示変更を接続する。実際のfine witnessと元GK5CG比較値を明示したまま、局所compatibility・指定因子別obstruction・source経路と部分Homの自然性を形式化する。未証明の一般sheaf降下や元四セル歴史の一律同一視はしない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
