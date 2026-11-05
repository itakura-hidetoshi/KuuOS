# Qi v4.69 — 元P77パッチ族の表示比較・細分と正規化の自然性

## 統合と検証

- 日付: 2026-11-06 JST
- canonical base: `79d4b4107d27879ce57c840aad28a061d98719d7`
- 定理PR: [#3159](https://github.com/itakura-hidetoshi/KuuOS/pull/3159) — MERGED
- 検証HEAD: `1e90a87677689ab4817d263bd2cade94a577fe41`
- 定理squash: `6e5fcd9a8af866b5c35f4940daf388963ca152dc`
- exact-source CI: [CI #42054492992](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42054492992)
- Strict Lean: **10,266/10,266 SUCCESS**
- Governance: **30/30 SUCCESS**
- 新規公理出力: **25件、標準公理のみ、sorryAxなし**
- 変更Lean warning/error: **0/0**
- source/test-merge Git tree: `2d4f5830a7718e05d6a08d1d8481936386ef1e0e` — 完全一致
- 公開root: **107**、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`
- 保護PR #1558: **Draft/open/unmerged**

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77PatchPresentationNaturalityV4_69.lean) · [前段v4.68](Qi-v4_68-original-P77-finite-cut-tree-normal-coherence.md)

## 1. 同じraw列から、元証拠で比較できる異なるパッチ族へ

v4.68は厳密に同じ順序付きraw列に対する任意有限の切断・再括弧付けを扱った。v4.69では、同一の実際の型付きsource境界において、添字型もraw四セル代表も異なり得るパッチ族を比較する。

元の族を $A:I\to\mathrm{Raw}(u,v)$、比較先を $B:J\to\mathrm{Raw}(u,v)$ とする。新しい `FivefoldP77RawPatchBlockComparison` は次をType値データとして保持する。

$$
s:J\to I,\quad
\alpha_j:\mathrm{GK5CGCell}(A_{s(j)},B_j),
\qquad
t:I\to J,\quad
\beta_i:\mathrm{GK5CGCell}(B_{t(i)},A_i).
$$

ここで五セルは元の `NativeGK5CGConservativeFiveCell` の実際の値である。数値chargeの一致やraw族の等式を仮定しない。二つの添字写像が互いに逆であることも要求しないが、**両側の全パッチに比較証拠がある**ことを要求する。反射・対称・推移の比較データも元の五セル構成子で構成する。

## 2. 被覆された細分と、真正source証拠の同値

細分写像 $r:J\to I$ が全射で、各 $j$ に元の五セル $A_{r(j)}\Rightarrow B_j$ が与えられれば、`fivefoldP77RawPatchBlockComparisonOfRefinement` が上記の双方向比較を構成する。逆方向の添字には各原像を選び、既存五セルの対称と原像の等式を使う。全射性はこの構成の十分条件であり、全ての双方向比較に必要な条件とは主張しない。

元のブロック証拠Typeは、実際のsource経路 $q:\mathrm{Quiver.Path}(u,v)$ と、全パッチについての元P77商評価等式を持つSubtypeである。比較から構成する

$$
E_c:W(A)\simeq W(B)
$$

は、**順方向・逆方向とも同じ $q$ をそのまま返す**。変更するのは、指定した元五セルから導く商評価の証明部分だけであり、経路保存は定義的に成立する。選ばれた五セル値は比較データ側に保持され、このwitness同値が五セル履歴自体を可逆に復元するとは主張しない。これにより元の全対五セルoverlapとsource-anchorによる $\mathrm{Compatible}(A)\leftrightarrow\mathrm{Compatible}(B)$ も得る。

被覆条件を欠いた一方向の対応だけから、逆写像やobstruction不変性を結論していない。元のパッチを落とすことで、指定された局所証拠の欠落を隠すことは許さない。

## 3. 任意有限の依存鎖と正規化の可換性

`FivefoldP77RawPatchChainComparison` は `nil/cons` によって空鎖と任意有限段を扱う。各段の実際の中間source頂点を保持し、段ごとに異なる添字型とraw族を比較できる。証拠輸送には固定mathlibの `Equiv.prodCongr` を使い、全段を結合した元の `Quiver.Path` が厳密に等しいことを証明する。

切断木 $S,T$ の正規化を $N(S),N(T)$、v4.68の正規化同値を $\nu_S,\nu_T$ とする。正規化後の鎖の実際の比較 $c$ が与えられると、

$$
E^{\mathrm{tree}}_c=\nu_T^{-1}\circ E^{\mathrm{chain}}_c\circ\nu_S
$$

を構成し、真正Type値証拠上で次を証明する。

$$
\boxed{\nu_T(E^{\mathrm{tree}}_c(w))
=E^{\mathrm{chain}}_c(\nu_S(w))}
$$

$N(S)=N(T)$ というraw鎖の等式は要求しない。一方、比較は同じ段境界の骨格を保つ。今回の細分は各段における**パッチ族の表示細分**であり、source区間への新たな頂点挿入を意味しない。

さらにsource側・target側の任意のv4.68 recut履歴と、それぞれの実際の表示比較から作る四角形が、誘導されるLean `Equiv` の等式として可換になる。

## 4. 表示変更と切断を混在させた任意有限履歴

新規 `FivefoldP77RawPatchPresentationRoute` は元recut、真正比較による表示変更、逆履歴、履歴合成、左右文脈をType値として保持する。各履歴の評価は、実際の切断同値・上記の比較同値・逆同値・同値合成・積同値で定義する。

同じ始点・終点の履歴 $r_1,r_2$ について、

$$
E(r_1)=E(r_2)
$$

を証明した。この等式は、以前から証明済みの真正P77 Faithful性に由来する**source証拠TypeのSubsingleton性**を使用する。履歴そのもの、選ばれた五セル値、任意のraw四セル／五セル証明を等しいとは主張しない。

任意の履歴 $r:S\to T$ と元証拠 $w$ に対し、次が保存される。

| 保存対象 | 形式証明した内容 |
|---|---|
| 元source経路 | $\mathrm{Path}_T(E(r)w)=\mathrm{Path}_S(w)$ |
| 元P77証拠付き部分Hom | $\mathrm{Certified}_T(E(r)w)=\mathrm{Certified}_S(w)$ |
| 元raw族からのP77商合成 | 真正source証拠を伴う場合に両側の合成値が一致 |
| 元の部分復元 | 変更後の部分Homから元の $\mathrm{Path}_S(w)$ を厳密に回収 |
| 全局所compatibility | $\mathrm{Compatible}(S)\leftrightarrow\mathrm{Compatible}(T)$ |
| 指定因子別obstruction | $\mathrm{Obstructed}(S)\leftrightarrow\mathrm{Obstructed}(T)$ |

## 5. 存在条件とobstruction境界

証拠の存在は、全指定段での元五セルoverlapとsource-anchorという既存の必要十分条件に従う。coherenceだけを示して存在を仮定し忘れる構成ではない。元に指定因子別のobstructionがあれば、許された任意有限の表示変更・被覆細分・recutを経ても比較先の証拠Typeは非空にならない。

この定理は別の全target因子分解に対する不可能性、全P77 targetのfullness、chargeからの元証拠構成、一般siteのsheaf降下を主張しない。また、異なるraw鎖全体に対する完全な比較存在判定や、任意rewrite戦略の停止性は今回の結果に含めない。

strict 空を中心に、独立Kuuは一つのpresentationとして維持する。元F55/P77/P94A・物理C60 Gauge・北C60 CRTのauthorityを同一視しない。新pentagonatorやGrayを追加しない。

## 6. 検証方法と次の課題

新規モジュールと公開集約import以外の旧Lean本文、固定toolchain、mathlib manifest、公開root構成を保持した。元v4.63–v4.68と真正五セルの定義、固定mathlib APIを照合し、独立した数学設計レビューと新規ソース全文レビューを行った。固定CIの全必須job、ビルド後manifest検査、完了receipt、実際の25件の公理出力、変更Lean診断、source/test-merge treeを確認した。

初回の検証HEADで全証明が通過し、定理文・仮定・旧証明の修正は不要だった。新規540行に対する二つの独立した全文レビュー（数学的設計とLean/API・意味論）は、ともに重大・重要問題なし。全32 workflow jobs、全41 current check runs、および二つのexact-head terminal receiptまで完了を確認した。元sourceとtest-mergeのtree一致を再確認して検証済みHEADを指定してsquashマージし、統合後mainのtreeも同一であることを確認した。

**次の候補Qi v4.70：** 真正な因子別source証拠を伴う段分割・統合へ進み、表示細分とsource区間細分の相互整合性を研究する。新しい中間頂点やその到達証拠を全target合成の等式だけから生成せず、必要な局所証拠とobstruction境界を明示する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
