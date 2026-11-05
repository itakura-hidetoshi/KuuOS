# Qi v4.70 — 元P77の証拠付き段分割・統合と指定因子のobstruction

## 統合と検証

- 日付: 2026-11-06 JST
- canonical base: `7191cdb14f73fdcb1821ad1a0f61d586eb0ff53e`
- 定理PR: [#3162](https://github.com/itakura-hidetoshi/KuuOS/pull/3162) — MERGED
- 検証HEAD: `db43afd65369fdcfe4abfc02019195fd049b82bf`
- 定理squash: `e2dfb3044e4412a74c743c2991cc3995e5e3269a`
- exact-source CI: [CI #42061853790](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42061853790)
- Strict Lean: **10,267/10,267 SUCCESS**
- Governance: **30/30 SUCCESS**
- 新規39宣言の公理依存出力: **全39件が標準公理のみ、sorryAxなし**
- 変更Lean warning/error: **0/0**
- source/test-merge Git tree: `dc879246f45009832f621c6c9a17a6859c6cd1c2` — 完全一致
- 公開root: **107**、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`
- 保護PR #1558: **Draft/open/unmerged**

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CertifiedSegmentSubdivisionV4_70.lean) · [前段v4.69](Qi-v4_69-original-P77-patch-presentation-naturality.md)

## 1. 表示細分から、実際のsource段分割へ

v4.69では、既存の型付き段境界を保ったままrawパッチ族の添字型や代表を変更した。v4.70は、実際の中間source頂点と段数を変更する段分割・統合を扱う。その際、各新しい段のsource証拠を明示的なデータとして要求する。

有限依存鎖を $C=(B_1,\ldots,B_n)$、各段の添字型を $I_j$ とする。新規 `FivefoldP77RawPatchChainIndex` は全段の添字の有限積を保持し、`fivefoldP77RawPatchChainRaw` は各組に対する元raw四セルの合成を作る。

$$
I_C=I_1\times\cdots\times I_n\times\mathbf{1},\qquad
R_C(i_1,\ldots,i_n,*)=
R_1(i_1)\mathbin{;}\bigl(R_2(i_2)\mathbin{;}\cdots
\bigl(R_n(i_n)\mathbin{;}\mathrm{refl}\bigr)\cdots\bigr).
$$

空鎖では $I_C=\mathbf{1}$、raw値は元の恒等四セルとなる。全ての段の添字型は既存定義により非空なので、有限積も非空である。これをraw族とする `CompositeBlock(C)` は、**全ての添字の組と、その実際の元raw合成**を含む。

## 2. 全代表を実現するgluingと、表示変更の自然性

元の証拠Type $W(C)$ は、各段の真正source経路と全raw代表についての元P77商評価等式を保持する。`fivefoldP77RawPatchChainPath_eval_all` は、元source経路を連結した値が、全ての添字の組について $R_C$ の元P77商クラスに評価されることを証明する。

$$
\forall w:W(C),\ \forall i:I_C,\qquad
F(\operatorname{Path}_C(w))=[R_C(i)].
$$

したがって、常に具体的なgluing $W(C)\to W(\operatorname{CompositeBlock}(C))$ を構成できる。粗いパッチ族 $B$ に対するv4.69の双方向比較

$$
c:\operatorname{BlockComparison}(\operatorname{CompositeBlock}(C),B)
$$

が与えられる場合は、各比較先を覆う元GK5CG Type値五セルを用いて

$$
G_c:W(C)\longrightarrow W(B),\qquad
G_c(w).\mathrm{val}=\operatorname{Path}_C(w)
$$

を得る。このsource経路保存は定義的である。既存の元五セル履歴は比較データ側に保持される。証拠Subtype内の商評価等式はPropであり、五セル履歴そのものがSubtypeに格納されるとは主張しない。

細い鎖・粗い族の両方の表示を変更したとき、与えられた両側の比較に対して次の四角形も可換になる。

$$
G_{c'}(E_{\mathrm{fine}}(w))=
E_{\mathrm{coarse}}(G_c(w)).
$$

この証明は実際のsource経路の等式に帰着する。完全な分割可能性や、五セル履歴の一律同一視は仮定しない。

## 3. 無条件に成立するのは、細分証拠を伴う総空間との同値

固定した粗い証拠 $q:W(B)$ に対し、指定された鎖 $C$ による細分のfiberを

$$
\operatorname{Fib}_C(q)=
\{w:W(C)\mid\operatorname{Path}_C(w)=q.\mathrm{val}\}
$$

と定義する。これは細い各段のsource証拠を実際のType値として持つ。`fivefoldP77RawPatchSubdivisionTotalEquiv` は、比較データ $c$ の下で、証拠の存在を追加仮定せずに次を構成する。

$$
\boxed{
W(C)\simeq\sum_{q:W(B)}\operatorname{Fib}_C(q)
}
$$

順方向は $w\mapsto(G_c(w),w,\mathrm{refl})$、逆方向は格納された細い証拠の射影である。逆法則は、gluingが実際の連結source経路を持つこととSubtypeの外延性から証明する。$W(C)$ が空でも成立する。

固定した $q:W(B)$ のfiberについては、既存の全段の元五セルoverlapとsource-anchor条件を用い、正確な必要十分条件を証明する。

$$
\boxed{
\operatorname{Nonempty}(\operatorname{Fib}_C(q))
\iff\operatorname{Compatible}(C)
}
$$

逆方向ではcompatibilityから得た細い証拠をglueし、元P77の真正なFaithful性から既に証明された粗いsource証拠の一意性で $q$ と一致させる。粗い証拠が存在するという条件だけで、指定された細い因子の証拠が存在するとは結論しない。

## 4. 因子別の実証拠を与えた可逆分割

実際の $w_0:W(C)$ を与えると、`fivefoldP77RawPatchSubdivisionEquiv` は

$$
E_{c,w_0}:W(B)\simeq W(C)
$$

を構成する。分割写像は供給された $w_0$ を返し、逆写像は上の実際のgluing $G_c$ である。これはsource証拠TypeのSubsingleton性を使う構成であり、粗い経路から未知の因子を新たに探索・生成するアルゴリズムではない。供給された因子別証拠と元Faithful性により、次を形式証明する。

$$
G_c(E_{c,w_0}(q))=q,\qquad
E_{c,w_0}(G_c(w))=w,\qquad
\operatorname{Path}_C(E_{c,w_0}(q))=q.\mathrm{val}.
$$

この三式によって、条件付き分割が元の粗い証拠・各細分証拠・全source経路を正確に保持することが明示される。

## 5. 切断木、表示変更と任意有限の段変更

単一の粗いブロックを空tail付きの切断木に埋め込み、mathlibの `Equiv.prodPUnit` とv4.68の正規化同値を用いて、比較データと実際のfine witnessを備えた任意の細い切断木への同値を構成する。正規化後の細い証拠と、直接鎖を分割して得た証拠が一致する。

新規 `FivefoldP77RawPatchSubdivisionRoute` は、v4.69の表示変更・recut履歴、実際のfine witnessと元五セル比較を持つ段分割、逆操作による統合、有限合成、左右の文脈をType値として保持する。段分割の構成子には毎回真正な因子別証拠が必要である。

| 形式証明した対象 | 内容 |
|---|---|
| 正規化 | 切断木の分割同値と鎖への正規化が可換 |
| 任意有限の許された混合履歴 | 同じ始点木・終点木を持つ履歴が誘導するLean `Equiv` は一致 |
| 表示変更との自然性 | 粗・細の表示変更と段分割からなる四角形が可換 |
| 元source経路 | 変更後の `Quiver.Path` は元の全経路と厳密に等しい |
| 元P77証拠付き部分Hom | `FivefoldP77PartialDomain` の値そのものが一致 |
| 元商の合成・部分復元 | 実現された商合成が一致し、元source経路を厳密に復元 |
| 指定因子のcompatibility・obstruction | 証拠付き操作の下で必要十分条件と障害を保存 |

段分割後のraw鎖や段数が元と等しいとは主張しない。履歴の独立性が同一視するのは誘導されたsource証拠写像であり、raw四セル・五セルの履歴データ自体ではない。

## 6. 具体的な反例：全体の到達可能性は因子別証拠を含意しない

元の順向き辺e01に対応するraw四セルを $a:0\to1$ とする。targetには元のraw逆 $a^{-1}:1\to0$ がある。これをsourceの逆辺として追加せず、指定された細い鎖を

$$
C_{\mathrm{bad}}=(a^{-1},a):1\longrightarrow0\longrightarrow1
$$

と取る。統合rawは実際には右端の恒等四セルを含む $a^{-1};(a;\mathrm{refl}_1)$ である。元GK5CGの右単位五セルと逆消去五セルを合成することで、このrawから $\mathrm{refl}_1$ への真正な五セルを構成する。したがって統合パッチ族は、**vertex 1のnil source経路**で実現できる。

一方、最初の段 $a^{-1}$ は既存v4.56の `fivefoldP77OriginalReverse01_not_reachable` によりsource原像を持たない。よって次を証明する。

$$
\boxed{
\operatorname{Nonempty}(W(\operatorname{CompositeBlock}(C_{\mathrm{bad}})))
\ \land\ \neg\operatorname{Nonempty}(W(C_{\mathrm{bad}}))
}
$$

さらに、その具体的なnil粗証拠の指定細分fiberが空であることも証明する。粗い恒等合成の構成には、chargeの等式ではなく元の実際の五セルを使う。細分不存在には元の有向source障害を再利用する。

## 7. 証明範囲と検証記録

新規732行のモジュールと公開集約のimport 1行を追加し、旧Lean本文・既存宣言名・固定toolchain・mathlib manifest・公開root構成を保持した。新規ソース全文を数学的設計とLean/APIの二系統で独立にレビューし、境界例も別に照合した。最終HEADについて、固定Strict Leanの10,267件、ビルド後のcanonical manifest検査、実際の39宣言の公理依存出力、変更Lean診断0/0を確認した。全32 current workflow jobsと全41 current check runs（40 success・1 expected skip）、Governance 30/30、二つのexact-head完了ステータスまで完了を確認した。

初回実装では、再帰定義内のsectionパラメータ指定と3か所のドット直後の改行がLeanのelaboration／構文エラーになった。新規ソース全文と依存定義・固定mathlib APIを照合し、明示的パラメータ束縛とフィールド記法を修正した。数学的な仮定・結論や旧証明は変更していない。旧[PR #3161](https://github.com/itakura-hidetoshi/KuuOS/pull/3161)は、branch更新後もPR内部の旧HEAD／test-merge参照が残ったため未マージで閉じ、同一の修正版コミットからPR #3162を作成した。

最終[CI #42061853790](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42061853790)ではStrict Leanと全選択チェックが通過した後、完了ステータス送信時のGitHub HTTP 500で集約jobだけが失敗した。その集約jobのみを再実行し、attempt 2で全体SUCCESSと両完了receiptの送信成功を確認した。再試行のためのソース変更やLean再ビルドは行っていない。

sourceとtest-mergeのtree完全一致を確認し、検証済みHEADを明示してsquashマージした。統合後canonical mainのtreeも同一であることを再観測した。

全targetのfullness、全targetからの無条件な因子復元、比較データの無条件存在、一般siteのsheaf降下、任意rewrite戦略の停止性は今回の結論に含めない。新しいsource逆辺、pentagonator、Grayを追加しない。strict 空を中心とし、独立Kuuは一つのpresentationとして、元F55/P77/P94A・物理C60 Gauge・北C60 CRTのauthorityを維持する。

**次の候補Qi v4.71：** 段ごとの表示比較と再括弧付けから、統合パッチ族の比較データを元五セルとして再帰的に構成する。比較の存在を入力する今回の形式から、具体的な比較構成と反復細分の整合性へ進み、因子別source証拠とobstruction境界を引き続き保持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
