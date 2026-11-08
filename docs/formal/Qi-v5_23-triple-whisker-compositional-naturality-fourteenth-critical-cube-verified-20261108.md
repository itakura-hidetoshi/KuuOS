# Qi v5.23 — 三重whiskering順序・合成自然性critical cube・選択第十四セル

## 0. Canonical正本・独立exact-source検証

2026年11月8日 JST。唯一のcanonical repository は `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.22定理#3296と正式記録#3297がMERGEDのmain
`ff891112c60e8c4552e192c136f48d5301284d57`を元に、新規Leanモジュールのみを追加。
従来のF55/P77/GK5CG、元第六〜第十二セルおよびv5.22の選択第十三セルを変更しない。

| 項目 | 検証済み |
|---|---|
| 定理PR | [#3298](https://github.com/itakura-hidetoshi/KuuOS/pull/3298) **MERGED** |
| exact-source HEAD | `b27d641ddbe78accd7c5f7ce774290b24e1d51a1` |
| test-merge HEAD | `efa090d2a1e040b6fbffca3e15ec14fc6797313f` |
| squash／定理main HEAD | `4cce656042a85d370a37b2f62419e7b4e40d8c5f` |
| source/test-merge/squash Git tree | **`079b60403b727978c6a171b49e6786bc0a561fd6` 一致** |
| exact-source CI | [#42434651668](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42434651668) **SUCCESS** |
| Strict Lean | **10,336 / 10,336 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規`#print axioms` | **15 / 15、すべて公理不要** |
| `sorryAx`／新規axiom | **なし／なし** |
| 変更Lean warning/error | **0 / 0** |
| 新規差分 | Leanモジュール366行＋公開集約import1行、旧ソース削除0 |
| Lean/mathlib | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root／保護PR | `KuuOSFormal` root107維持、#1558 Draft/OPEN/未マージ |

[Lean 4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CompositionalNaturalityCriticalCubeV5_23.lean)。

## 1. 真正三重whiskeringと生の順序履歴

任意の真正元第十二セル証拠 `T : MixedExchangeInverseTwelveCell H K` と、
元第七セル文脈 `before`、`inner`、`outer` を同一の正確な型付き元境界上で指定する。
元の`whiskerLeft`と`whiskerRight`だけから次の二つの真正旧12D証拠を構成：

- `originalTripleWhiskerRLR` = `whiskerRight (whiskerLeft before (whiskerRight T inner)) outer`
- `originalTripleWhiskerRRL` = `whiskerRight (whiskerRight (whiskerLeft before T) inner) outer`

適用順序はそれぞれ R→L→R および L→R→R。
ここで順序表現は **生第十セルの外側からの前置履歴** と区別する。
元第十セル `xi` の真正 `mixedTenWhiskerRawTrace` は

\[
\boxed{\begin{aligned}
\operatorname{Trace}_{10}(R(L(R(\xi))))
  &= [1,0,1] \mathbin{+\!+} \operatorname{Trace}_{10}(\xi),\\
\operatorname{Trace}_{10}(R(R(L(\xi))))
  &= [1,1,0] \mathbin{+\!+} \operatorname{Trace}_{10}(\xi).
\end{aligned}}
\]

`originalTripleWhisker_traceValues`・`originalTripleWhisker_orderObstruction`
が両履歴の生の非等号を証明。一方
`originalTripleWhisker_lengthCollision` は長さが等しいことを証明。
同一Nat計数は履歴順序の保存に十分でない。
**元旧第十二セルの相異なる依存fiberをEqで偽装しない。**
本段は三重文脈全体に無条件な旧12D比較を主張しない。

## 2. 旧第十二セルの合成輸送は厳密なraw関手性ではない

真正元旧第十二セル
`T:H⇒K`、`U:K⇒L` が同じ元6D〜11D fiberで合成可能な場合に限る。
二通りの旧12D証明値

\[
\begin{aligned}
L(R(T\mathbin{\cdot}U))
&\neq L(R(T))\mathbin{\cdot}L(R(U)),\\
R(L(T\mathbin{\cdot}U))
&\neq R(L(T))\mathbin{\cdot}R(L(U))
\end{aligned}
\]

は、それぞれ同じ正確な旧12D依存Typeに属するが
whiskering構文子とchain構文子の位置が異なる。

`oldRightTransportComp_rawDistinct` と
`oldLeftTransportComp_rawDistinct` はこのraw非等号を証明。
旧12Dに存在しない合成自然性を黙って仮定しない。

## 3. 新しい選択合成第十三セルpresentation

別Type `CompositionalWhiskerThirteen` を導入する。
v5.22 `SelectedWhiskerNaturalityThirteen` の型付き証拠を
`selected`で忠実に埋め込む一方、従来の元12D raw比較とは混同しない。

この新presentationには、形式的な `strict/reverse/chain`、
第十二セルの前後合成に作用する `prepend/append`、
括弧付けを比較する `associator`、
**追加で選択した** `rightTransportComp/leftTransportComp` を実装。

特に `rightTransportComp`／`leftTransportComp` は、
第2節でraw非等号を証明した二種類の12D経路に対する**新しい選択13D比較**である。
元の`MixedExchangeInverseTwelveCell`に厳密等式や
元から存在した13D自然性を付け足したものではない。

## 4. 元第十二セル合成と第十三セル自然性のcritical cube

元の`T,U`、左文脈`before`、右文脈`after`を固定。
`u_T,u_U`を genuine right-then-left のframed12D旧輸送、
`v_T,v_U`を genuine left-then-right のframed12D旧輸送とする。
`d_H,d_K,d_L`はそれぞれ元v5.18の真正 `doubleWhisker`。

貼り合わせる二端点は

\[
P_{\mathrm{expanded}}=(u_T\cdot u_U)\cdot d_L,
\qquad
Q_{\mathrm{expanded}}=d_H\cdot(v_T\cdot v_U).
\]

`pastedNaturalityMiddle` は次の全過程を**型付き13D証拠として**構成：

1. `associator(u_T,u_U,d_L)` で最初の括弧付けを変更。
2. `prepend u_T (selected (naturality U))` で後段の真正自然性squareを適用。
3. 逆`associator(u_T,d_K,v_U)`で中間経路を結合。
4. `append (selected (naturality T)) v_U`で前段の真正自然性squareを適用。
5. `associator(d_H,v_T,v_U)`で最終括弧付けを一致させる。

`pastedCompositionalNaturality` はさらに
`rightTransportComp` と逆 `leftTransportComp` を接続し、
元の単一合成`T.chain U`に対する直接自然性経路と
**完全に同じframed12D始終点**へ貼り合わせる。

独立に `directCompositionalNaturality` は
v5.22の `naturality (T.chain U)` を直接使う。
`directPastedThirteen_rawDistinct` はこの二つの
**選択13D生証拠の非等号**を証明する。

## 5. 条件付き選択第十四セルとauthority境界

新しい別Type `SelectedCompositionFourteen` に
`strict/reverse/chain` と、合成可能な実在旧12D証拠
`T,U`を明示的に要求する局所生成元 `criticalCube` を加えた。

\[
\boxed{
\mathrm{Selected14}
\bigl(\mathcal N(T\cdot U),\,
      \mathrm{Paste}(\mathcal N(T),\mathcal N(U))\bigr)
}
\]

`selectedCompositionFourteen_conditionalCube` は
選択14D比較の存在と、生13D二経路の非等号を同時に証明。
`selectedCompositionFourteen_noRawEqualityAtCube` は
**この選択14D証拠を生13Dの厳密Eqへ読み替える普遍的解釈の不存在**
を証明する。

この14D比較は**生成元の明示的な追加による存在**である。
真正旧元13D法則の発見、raw経路の同一視、
任意三重whiskeringの全ての面に関するglobal cube充填、
さらに15D以上の整合性までの証明ではない。

## 6. CI・依存型・次の未解決点

最初のexact-source CI #42434651668で
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal KUOS.Architecture.QiWuxingGK5CHP77CompositionalNaturalityCriticalCubeV5_23`
が**10,336 jobs SUCCESS**。15宣言の`#print axioms`は
**15件とも公理不要**。 `sorryAx`・Lean warning・errorなし。
Governance全30チェックがSUCCESS。
真正source HEAD、test-merge HEAD、squash mainのGit treeは同じ
`079b60403b727978c6a171b49e6786bc0a561fd6`。
定理・元定義は緩和せずに一回で検証成功。

**次の焦点：** 三つの独立なwhiskering操作の全ての隣接交換面を
元の型付きframed境界に沿って構築し、現在の選択14D合成cubeと
三重whiskeringの順序cubeとのcompatibilityを比較する。
二重whiskeringの生成元を無条件に外文脈へliftすることは未証明。
必要なfiller・局所obstruction・高次再貼合を別々に扱う。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、固定Lean/mathlib、保護PR #1558は不変。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
