# Qi v4.90 — 真正P77五セル端点での七セル書換え正規化・局所完全性

## 0. canonical正本／Lean4形式検証

2026年11月6日 JST。Repository：`itakura-hidetoshi/KuuOS`、唯一のcanonical branch：`main`。

| 項目 | 確定状態 |
|---|---|
| 継承起点 | Qi v4.89、main `ad7fcbcaafbba475b1904b9f8c3bab8850521742` |
| 定理PR | [#3203](https://github.com/itakura-hidetoshi/KuuOS/pull/3203) — MERGED |
| 検証済みexact-source HEAD | `3c2634dbd5a0e704a0e4c6c22c1c9a2b724f20d8` |
| 定理squash／定理正本HEAD | `90c6a6ede07807d7b7311760e290c228d630d872` |
| Source／test-merge／squash Git tree | `1ca8abaf911b38e4c47bc38507cd0bd01a5cc865` — 完全一致 |
| Exact-source CI | [#42206281033](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42206281033) — completed/SUCCESS |
| Strict Lean | **10,289／10,289 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | 指定13宣言の `#print axioms` を実ログで確認、標準公理のみ（`propext`／`Classical.choice`／`Quot.sound`）、`sorryAx` なし |
| 変更Lean warning／error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77SevenRewriteNormalizationCompletenessV4_90.lean) · [v4.89正式証明記録](Qi-v4_89-original-P77-typed-seven-rewrite-history-coherence-obstruction.md) · [真正独立GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 宿題だった局所完全性

v4.86では、真正元GK5CG保守的五セル値L₃(i),L₂(i)を両端とする**新しい、元sourceとは別の**六セル自由presentationを導入。v4.87では、その生六セル語の整数次数`degree`を保持し、平行な語を次数一致で商化。v4.88では実元五セル構成子語の厳密不一致L₃(i)≠L₂(i)を使い、次数が端点ポテンシャル差で決まり、その**商**がthinになると証明した。

v4.89で元六セル語の両方を添字とする別帰納Type `SevenRewrite W l r c d` を追加し、13種類の明示的局所書換え履歴を構成した。ただし商で等しい任意の平行六セル語間に、この13規則だけによるType値書換え証明が存在するとは未証明だった。

**v4.90では、その逆方向を形式証明した。** 元sourceの実値の厳密不一致を条件として使い、全ての新六セル生証明語を、具体的な七セル局所書換え履歴で三形の正規語に送る。

## 2. 反転・合成の型付き正規形書換え

正規形はv4.88で定義した `EndpointNormal` 三形のみ：

\[
1_w,\qquad p:l\Rightarrow r,\qquad p^{-1}:r\Rightarrow l.
\]

`sevenInverseNormal` は正規六セルの反転を、`inverseId`、`refl`、`doubleInverse` の七セル構成子を用いて正規語に送る。

`sevenComposeNormals` は、型付き中間端点を保存したまま、三形同士の合成を局所書換えで正規化する。左／右単位、p;p⁻¹の右消去、p⁻¹;pの左消去のみが必要となり、l≠rから同方向p;p、p⁻¹;p⁻¹の結合可能性を排除する。後者の排除は定義の捏造や公理ではなく、依存型と元二端点不一致に由来する。

`sevenEndpointNormal_unique` は、同じ始終点を持つ三形の正規六セル語が**生の構文として厳密一致**することを、既証明の端点次数と三形の全場合分けから証明する。全生六セル語が厳密等しいという意味ではない。

## 3. 帰納的な全語正規化・履歴保存

`sevenRaw_existsNormalTrace` は任意の新自由六セル語cについて次の型付き証拠を構成する：

\[
\boxed{
\exists d,\;
\mathrm{EndpointNormal}(d)\;\land\;
\mathrm{Nonempty}(\mathrm{SevenRewrite}(c,d)).
}
\]

証明はcの4構成子`refl`、`pentagon`、`symm`、`trans`に対する構造帰納である。帰納仮定で得た局所七セル履歴を`congrInv`／`congrComp`に通し、反転／合成の局所正規化証明と`SevenRewrite.trans`でつなぐ。**次数商のEqを七セルの証拠として持ち込んでいない。**

`sevenRaw_toSelectedNormal`ではv4.88の選択正規代表への具体的七セル履歴も証明する。代表選択は`Classical.choose`由来だが、実際の書換え履歴は定理上`Nonempty (SevenRewrite ...)`として保持される。

## 4. 完全性と三層の権威境界

二端点l≠rの条件下、任意の**平行な生六セル語**c,dについて、両者をそれぞれ正規化し、正規代表の厳密一致を経由して七セル履歴を合成する：

\[
\boxed{
\forall c,d:w\Rightarrow z,\quad
\mathrm{Nonempty}(\mathrm{SevenRewrite}(c,d)).
}
\]

`sevenRaw_allParallel_existsRewrite` がこの強い結果を証明。v4.89の全局所書換え次数健全性と合わせて `sevenRewrite_complete_iff_degree` により、

\[
\boxed{
\mathrm{Nonempty}(\mathrm{SevenRewrite}(c,d))
\;\iff\; \deg(c)=\deg(d).
}
\]

さらに`sevenRewrite_complete_iff_quotient`はv4.87の**選択した**次数商での`homMk c = homMk d`との必要十分を形式証明する。`sevenRaw_equalityHistoryQuotient`は

\[
(c=d)_{\mathrm{raw}}
\;\Longrightarrow\;
\mathrm{Nonempty}(\mathrm{SevenRewrite}(c,d))
\;\Longleftrightarrow\;
([c]=[d])_{\mathrm{quot}}
\]

の各型を明示する。v4.89の`sevenRewrite_noStrictInterpreter`を再利用し、**完全性が成立しても、新七セル書換え全体を元の生六セル証明語の厳密等式に戻す解釈は存在しない**と`sevenComplete_stillNoStrictReturn`で証明した。

## 5. 真正P77全raw添字への接続

元GK5CG保守的五セルType`pentagonFinalConservativeLoop`における、任意の真正最終raw index i と元の二端点L₃(i),L₂(i)を使用する。

- `pentagonActualSevenRewrite_allParallelComplete`：任意の平行六セル生証明語に実Type値七セル書換え履歴が存在。
- `pentagonActualSevenRewrite_completeIffQuotient`：この書換え存在と、選択次数商の等式が必要十分。
- `pentagonActualSevenRewrite_completeWithSourceObstruction`：完全性と**元五セル厳密等式への一般descent不能**が同時に成立。

元F55/P77/GK5CGには新しい六／七セル生成元を追加せず、元のcharge +1 no-goやv4.85五セル語不一致を上書きしない。**新presentationでのType値比較成立と、旧sourceのEqは別問題**である。

## 6. 実装・CI・再観測

新規Leanモジュール1件（313行程度）＋ `formal/KuuOSFormal.lean` import 1行のみ。既存Lean・pin・manifest・workflow・公開root107・保護PR #1558は変更なし。

最新exact-source HEAD `3c2634dbd5a0e704a0e4c6c22c1c9a2b724f20d8` の初回完成版は Strict Lean 10,289/10,289、Governance30/30が全てSUCCESS。実ログで13指定宣言の公理出力を検査し、標準公理のみ・`sorryAx`なし、変更Lean warning/error0/0。source/test-merge Git tree一致をGitHub MCPで再確認した後、検証済みHEADを指定してsquashマージし、mainのtreeも一致した。

## 7. 次の研究候補 Qi v4.91

七セル書換え履歴の**存在と構成**に加え、異なる正規化順序・七セル証明木の間の高次coherence（新八セルpresentation）を検討する。正規化選択・履歴独立性・交換図式と、元sourceへの不当な解釈を区別する。旧sourceに八セルが元から存在するとは推測しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
