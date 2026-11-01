# KuuOS / 空OS

**空・縁起・関係・文脈・presentationの交代可能性・高次圏論・obstruction-aware descent** を研究する数学体系、およびそのLean 4形式化・AI推論runtimeの研究です。

> **KuuOSの縁起の一般理論は、C60の導入以前から構築されてきました。C60から一般化を一から始めるのではありません。**
>
> 空は、異なる表示を無条件に同一視することでも、一つの数学的構造を「空そのもの」と固定することでもありません。数学・構成・観測・比較の方法自体も縁によって成立するという「空の空」を問い続けます。

English: KuuOS develops a general mathematical program for dependent origination, contextual transport, presentation localization, effective descent, higher coherence, and explicit obstructions. The later C60 geometry is a concrete testbed, **not the origin or unique model of the general theory**.

**研究・著作権者 / Founder and copyright holder:** 板倉英俊 / Hidetoshi Itakura. [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff).





## 最新のLean定理統合 — F112-P94D3GK5D / 2026-11-02 JST

**固定標的`T`の有限endofunctor木（GK5A/B/C）から、異なる真正Mathlib圏を順次通る型付き有限関手鎖へ一般化：任意有限木の本物の正規化経路、到達可能性の必要十分条件、whole NatIso経路独立性をLean4で証明 — [定理PR #2903](https://github.com/itakura-hidetoshi/KuuOS/pull/2903) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5DTypedManyCategoryFunctorChains.lean)・[正式証明記録](docs/formal/GK5D-many-category-typed-functor-chain-reachability.md)。

**数学的成果：** `C : I → Cat.{vT,uT}`の真正圏族に対し、始点・終点を依存型添字に持つ`TypedWord C i j`と`TypedTree C i j`を構成。単位・原子・型整合的貼合せに本物の`Functor.associator/leftUnitor/rightUnitor`、左右iso-whiskeringを用いて、全有限深度の標準右結合木への具体的書換え経路を帰納構成した。任意の同じ始点終点を持つ木`a,b`について`Nonempty(TypedPath C a b) ↔ TypedLeaves(a)=TypedLeaves(b)`を証明し、あらゆる実経路のwhole NatIsoが構成的正規化比較と一致する。順序付き**依存型葉列の等号**は偶然等しい合成関手という意味論的同値とは区別する。真正三段異種圏associatorも実NatIsoとして検証。

**exact-source：** 最終source `143c4e379c7dc4b41533411f510ef25c4ccad2aa`／test-merge `70db965347e98854e3a4eee591e647a980b13aca`／一致Git tree `08b422bbd30ed335858eaf07f9753e67687b9f4f`。[CI #41330331080](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41330331080) **Strict Lean 3825/3825、Independent Kuu・Workflow integrity・Governance terminal全SUCCESS**。16/16件の`#print axioms`は標準3公理`propext/Classical.choice/Quot.sound`以内、sorryAx0、変更Lean error/warning0/0。定理squash・main当時HEAD `cedb7970477393d625f00fc4e4cd5941c4e824f1`。

**次の研究GK5E（候補）：** 異種圏間の選択逆関手比較の型付き自然性・両端`eqToIso`輸送を、正確なcompatibility仮定の下で調べる。今回の証明は同一universe pair内の型付き有限関手鎖であり、異なるuniverse間の無制限合成、元F45の無条件faithfulness、原source-Q圏公理、raw F54/F55/P92B高次セル、全整数行列到達、global Gray、無制限hyperdescentは含まない。任意選択逆`Q_T`と明示逆`P_T`は定義的同一ではなく`κ_T`で比較する。Lean v4.30.0-rc2・mathlib pin不変、公開root107、保護PR #1558 Draft/OPEN/未マージ、strict空中心・独立Kuu一presentationを維持。以下GK5C以前の履歴は全保持する。

## 最新のLean定理統合 — F112-P94D3GK5C / 2026-11-01 JST

**任意有限endofunctor木から右結合の標準葉列木への本物のassociator/unitor書換え経路を帰納的に実構成し、任意2木の到達可能性が順序付き葉列一致と必要十分であることをLean4で証明 — [定理PR #2901](https://github.com/itakura-hidetoshi/KuuOS/pull/2901) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFiniteTreeNormalizationReachability.lean)・[正式証明記録](docs/formal/GK5C-constructive-finite-tree-normalization-reachability.md)。GK5A/GK5Bの固定標的`T`における真正有限endofunctor木を対象とし、元F45構造商・旧AH実到達圏・真の核両立部分圏・任意選択逆`Q_T`と明示逆`P_T`の区別は保持する。

**数学的成果：** 実書換え経路の左右whiskeringを帰納構成し、真正`Functor.associator/leftUnitor`による標準木のリスト連結経路、`rightUnitor.symm`による葉の拡張を組み合わせて、**任意有限木`t`から標準木`treeOfList(leaves t)`へ型付き真正経路を構成**。`pathIso(normalizePath(t))`を終点での本物の`eqToIso`輸送後にGK5Bの正規化NatIsoとwhole NatIso等式で一致させた。さらに**`Nonempty(RewritePath(a,b)) ↔ leaves(a)=leaves(b)`**を証明。逆方向は両木の正規化経路を合成・逆転して明示構成し、GK5Bの既証明経路独立性から任意の同じ型付き2経路がwhole NatIsoで一致する。GK4BU/GK5Aの選択逆関手`Θ`に対し、構成済み正規化経路と同葉比較経路の真正whole NatTrans四角、および両端の厳密`eqToIso`輸送も形式化（公開13宣言）。

**exact-source：** source `502c1e0f7d2d4e2adc68e6a55fd6d2018b626de1`／test-merge `e464e79ac0302db61f8ab74e71533b39fbd5f0e5`／一致Git tree `1e20f44546642bf3ceb3f834b8d05eff28269ded`。[CI #41307401462](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41307401462) **Strict Lean 3824/3824、Independent Kuu・Workflow integrity・Governance terminal全SUCCESS**。公開13/13宣言の`#print axioms`は標準3公理`propext/Classical.choice/Quot.sound`以内、sorryAx0、変更Lean error/warning0/0。定理squash・main当時HEAD `73ea3ac3e6f6c86d8ec7a21dff011a6a34d6d46f`。

**次の研究GK5D（仮称）：** 今回の固定`T`の有限endofunctor木の証明付き到達性・coherenceを普遍性として整理するか、複数の標的圏をまたぐ依存型有限関手鎖への段階的拡張を検討。元F45商の無条件faithfulness、source-Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray、無制限hyperdescentは未証明境界。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ、strict空中心・独立Kuu一presentationを維持。以下GK5B以前の記録は全て保持する。

## 最新のLean定理統合 — F112-P94D3GK5B / 2026-11-01 JST

**任意有限endofunctor木に対する本物のMathlib associator・左右unitor書換え経路を証拠付きで実構成し、同じ型付き始点・終点の全経路がwhole NatIsoとして一致することをLean4で証明 — [定理PR #2899](https://github.com/itakura-hidetoshi/KuuOS/pull/2899) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFiniteTreeRewritePathCoherence.lean)・[正式証明記録](docs/formal/GK5B-finite-tree-rewrite-path-coherence.md)。対象は固定した一つの真正Mathlib標的圏`T`での有限`T⥤T`二分木。元F45依存型構造商・実到達AH圏・GK4BM真のAH核両立部分圏・任意選択逆`Q_T`と明示逆`P_T`の区別を維持する。

**数学的成果：** 新しい依存型`NativeGK5BRewriteStep`と`NativeGK5BRewritePath`に真の`Functor.associator`、`leftUnitor`、`rightUnitor`、左右whiskering、経路反転・連結を保持し、各ステップ／経路の**実whole Mathlib NatIso**を構成。構造帰納法で`pathIso(p)=eqToIso(pathEq(p))`と証明し、**任意の同じ始点終点を持つ2経路のwhole NatIsoが厳密一致**することを確立した。さらに全経路の順序付き葉列保存、GK5A有限語への`eqToIso`付き正規化の経路整合性、選択逆関手`Θ`のGK4BU真正whole NatTrans可換四角と左右貼り合わせの経路独立性、両端の明示的輸送を形式化。単位除去と括弧変更の順序を入れ替える**実際の二経路**も個別に構成・whole NatIso一致を証明（17公開宣言＋2新帰納型）。証明範囲は**存在する書換え経路についての経路独立性**であり、任意木間の書換え経路の構成可能性までは主張しない。

**exact-source：** final source HEAD `afa157901a4cd9c3b6303a419f36055dad7c6ded`、test-merge `859461456c1fbda8b4b2520e411cec4daff1bccc`、**一致Git tree `0cef5f92477213381c90d5d069e5ea66f7738319`**。[CI #41306352193](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41306352193) **Strict Lean 3823/3823 SUCCESS、Independent Kuu／Workflow integrity／Governance terminalすべてSUCCESS**。17/17 `#print axioms`は標準3公理`propext, Classical.choice, Quot.sound`以内、sorryAx0、変更Lean error/warning0/0。初回CIの`→ A ≅ B`型記法を括弧付きで修正し、2回目CIの`rw`後の余分な`rfl`を除去。証明仮定・主張は緩めず、全文を再検証。定理squash／当時canonical main HEAD `8a8abead7636024d50c748887336d27037d30cbf`。

**次のGK5C候補：** GK5Bでは現存する経路の一致を証明したため、今度は任意有限木から右結合の葉列標準木へ**真正associator/unitor経路を実際に構成する正規化到達性**を検討する。原Sの無条件faithfulness、source-Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray/hyperdescentは未証明境界。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージ、strict空中心・独立Kuu一presentationを維持。以下GK5A以前の歴史記録は削除しない。

## 最新のLean定理統合 — F112-P94D3GK5A / 2026-11-01 JST

**五段14経路の個別証明を超え、任意有限二分木における実endofunctorの結合・単位挿入・選択逆関手比較を構造帰納法で形式化 — [定理PR #2897](https://github.com/itakura-hidetoshi/KuuOS/pull/2897) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFiniteEndofunctorTreeCoherence.lean)・[正式証明記録](docs/formal/GK5A-inductive-finite-endofunctor-tree-coherence.md)。対象は固定された一つの真正Mathlib標的圏`T`の有限`T⥤T`関手列であり、元F45型付き構造商・旧AH実到達像・真正核両立部分圏・GK4BM任意選択逆`Q_T`と明示逆`P_T`の比較境界は保持する。

**数学的成果：** 新帰納型`NativeGK5AFiniteTargetTree T`の単位・葉関手・二分貼り合わせを真正Mathlib関手に評価し、各節点でGK4BWの**実binaryPasting NatIso**を再帰構成。`nativeGK5AChosenInverse_treeIso_eq_direct`で**任意有限深度・任意括弧付けのwhole NatIsoが直接`Θ_(eval t)`と厳密一致**することを証明。GK4BUの真正標的自然変換に対するwhole NatTrans可換四角、任意深度の結合・左右単位則も証明。さらに`List (T⥤T)`と葉列への正規化、連結のwhole Functor等式、同じ順序の葉列を持つ任意二分木の比較が**両端`eqToIso`輸送を明記したwhole NatIso等式**になることを形式化。単なる定義上の同一視や原raw高次セルの仮定ではない。

**exact-source：** 最終source HEAD `c87edb4788dc07060372f9f5d6a97b1891d8a706`、test-merge `ccc48981a02a8ff233cf66db36ada860f33a4ca8`、**一致Git tree `c792db3e45f8aa05f8cd084af6e9a37e7f07c3ca`**。[CI #41304610405](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41304610405) **Strict Lean 3822/3822 SUCCESS、Independent Kuu・Workflow integrity・Governance terminal全SUCCESS**、新規16宣言に`#print axioms`16件、標準3公理`propext/Classical.choice/Quot.sound`以内、sorryAx0、変更Lean error/warning0/0。初回CIで空リストの左単位則に`simp`が不足したため、固定版Mathlib `Functor.id_comp`を明示し、仮定・結論を弱めず全ソース再検証。定理squash／当時main HEAD `6a74bc9ea979cd524e37d2fb13b9486fd5583d69`。

**次の研究GK5B（仮称）：** 任意有限木のassoc/unitor書換え経路の証拠付き正規化、または圏をまたぐ依存型有限標的鎖への範囲拡大。証明済みなのは固定標的`T`のendofunctor木であり、無制限多圏鎖・元Sの無条件faithfulness・source-Q圏公理・raw F54/F55/P92B Type値高次セル・全整数行列到達・global Gray/hyperdescentとは区別する。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、root107、保護PR #1558 Draft/OPEN、strict空中心・独立Kuu一presentationを維持。以下GK4BZ以前の歴史記録はすべて保持する。

## 最新のLean定理統合 — F112-P94D3GK4BZ / 2026-11-01 JST

**五段の任意標的変更におけるCatalan数14の真正NatIso貼り合わせ、二つの独立した単位関手の削除順序の全NatIso等式、全14経路に共通なwhole NatTrans変換をLean4で形式化 — [定理PR #2895](https://github.com/itakura-hidetoshi/KuuOS/pull/2895) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BZFiveTargetTwoUnitCoherence.lean)・[正式証明記録](docs/formal/GK4BZ-five-stage-fourteen-path-double-unit-coherence.md)。GK4BMの任意選択逆`Q_T`、GK4BP明示逆`P_T`、GK4BQ真正比較`κ_T:Q_T≅P_T`はそのまま、strictな`Q_T=P_T`は仮定しない。

**数学的成果：** 真正標的5段`R:T⥤U, S:U⥤V, L:V⥤W, M:W⥤X, N:X⥤Y`に対し、**5+2+2+5=14**の二分木括弧付けをGK4BWの真正binary pasting・GK4BV・GK4BTから全て実NatIsoとして構成。各々が直接の`Θ_(R⋙S⋙L⋙M⋙N)`とwhole NatIsoで厳密一致し、`Fin 14`索引の一つの定理と標的自然変換whole可換四角に統合。さらに`R⋙𝟭 U⋙S⋙𝟭 V⋙L`の**2個の独立した単位を左右どちらから先に除去しても、実Mathlib unitor/whiskeringで構成したwhole NatIsoが一致**することを証明。各除去順序のGK4BU選択逆比較NatTrans四角とその左右貼り合わせ全体が、全14経路で厳密一致（公開42宣言）。

**exact-source：** source HEAD `cc92f709586bac91d03aa1d190832a354470639c`、test-merge `8bb1421585e6a0d48bee4b459e9d29121d86ec3e`、**一致Git tree `ed8de1cf7bb61632e2daf0b264887410f76ef6eb`**。[CI #41303246207](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41303246207) **Strict Lean 3821/3821 SUCCESS・Independent Kuu／Workflow integrity／Governance terminal全SUCCESS**、42/42宣言の`#print axioms`は`propext, Classical.choice, Quot.sound`以内、sorryAx0、変更Lean error/warning0/0。定理squash／当時main HEAD `4ac0281675db8ae00b92e0e71bbe21027ddd6afb`。

**次の研究候補：** 有限長・同一標的のendofunctor鎖での帰納的coherence、2単位の隣接配置における除去順序、真のNatIso合成に関する標的自然性の強化。原F45圏Sの無条件忠実性、source-Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray／高次hyperdescentは未証明境界として保持。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージ、strict空中心・独立Kuu一presentationを維持。以下GK4BY以前の記録は削除しない。

## 最新のLean定理統合 — F112-P94D3GK4BY / 2026-11-01 JST

**標的変更の3段連鎖に単位関手を挿入する4位置×GK4BW pentagonの5実経路について、任意選択逆関手の真正whole NatIsoの完全一致、正逆unitorによる40件のwhole NatTrans四角、逆associator–unitor triangleをLean4で証明 — [定理PR #2893](https://github.com/itakura-hidetoshi/KuuOS/pull/2893) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BYChosenInverseUnitInsertionPentagonInverse.lean)・[正式証明記録](docs/formal/GK4BY-pentagon-unit-insertion-inverse-unitor-coherence.md)。

**数学的成果：** 真正`R:T⥤U`、`S:U⥤V`、`L:V⥤W`の前・中2か所・後のいずれかに`𝟭`を挿入し、固定版Mathlibの本物の`Functor.leftUnitor`、`Functor.rightUnitor`、whiskeringから4つの実NatIsoを構成。各挿入についてGK4BWで構成した**5つの実pentagon比較がすべて`Θ_(R⋙S⋙L)`とwhole NatIsoで厳密一致（20等式）**。さらに4×5経路のunitor.hom・.inv各々についてGK4BUの真正whole NatTrans可換四角を証明（正方向20・逆方向20）。実inverse associator–unitor triangle、その左右3段貼り合わせの可換性と結果の一致も証明。22公開宣言。選択逆`Q_T`と明示逆`P_T`の定義的同一性は仮定しない。

**exact-source：** final source HEAD `68257c0caf07d6f5be7d8f4aaf88d00e00846faa`、test-merge `fcedab4a7e98d406bbc15cdb707f4d762ab95bd5`、**一致Git tree `153e61366cfb20882c384abd11d1c9c9f6c66206`**。[CI #41301271737](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41301271737) **Strict Lean 3820/3820 SUCCESS・Independent Kuu・Workflow integrity・Governance terminal SUCCESS**。公開22/22宣言の公理依存は標準3公理`propext/Classical.choice/Quot.sound`のみ、sorryAx0、変更Lean error/warning0/0。初回CIの簡約後`True∧True`に`rfl`を適用した1か所を`simp`で修正し、全文を再検証。定理squash/main HEAD `a5978505b29ecaea3e80eab105d273fac1ebcb43`。

**次のGK4BZ（仮称）：** 複数単位の独立挿入と括弧付け変更の有限段coherence、条件付き有限段帰納的整理を検討。元F45構造圏Sの無条件忠実性、元source-Q圏公理、raw F54/F55/P92BのType値高次セル、未到達整数行列、global Gray、無制限hyperdescentは未証明。Lean v4.30.0-rc2／pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージ、strict空中心・独立Kuu一presentationを維持。以下GK4BX以前の履歴を完全保持する。

## 最新のLean定理統合 — F112-P94D3GK4BX / 2026-11-01 JST

**GK4BWの四段pentagon全5経路に対する標的自然変換のwhole NatTrans整合性と、Mathlibの本物の左右unitor／associator–unitor triangleとの混合coherenceをLean4で形式化 — [定理PR #2891](https://github.com/itakura-hidetoshi/KuuOS/pull/2891) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BXChosenInversePentagonNaturalityUnitorTriangle.lean)・[正式証明記録](docs/formal/GK4BX-four-target-pentagon-nattrans-unitor-triangle.md)。真正F45構造商、実到達旧AH像、AH核両立部分圏、任意選択逆関手`Q_T`、明示逆`P_T`と自然同型`κ_T:Q_T≅P_T`を変更しない。

**数学的成果：** 四つの標的自然変換`ρ,σ,τ,υ`を実whiskeringと垂直合成で合成し、四段標的変更の5つの真正GK4BW NatIso経路それぞれにwhole NatTrans可換四角を証明。さらに5経路の左右貼り合わせがそれぞれ**NatTrans全体の厳密等式**で一致する。GK4BWの左右単位比較を固定版Mathlib `Functor.leftUnitor`／`Functor.rightUnitor`の本物の射に接続し、`Functor.associator`とunitorの**triangleをwhole NatTrans等式**として証明。中間単位挿入の左括弧・右括弧による`Θ`比較および両可換四角も証明した（**公開15宣言**）。

**exact-source：** source HEAD `c1e5376acd72e85792efdd08b4b0be7dcfa1fe58`、test-merge `85149ae8920de7add72e9e44ac238daa66fb8537`、**一致Git tree `5a7e38f4c37b8e9687930e58a66f5a31e5cf10bc`**。[CI #41299912825](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41299912825) **Strict Lean 3819/3819 SUCCESS、Independent Kuu／Workflow integrity／Governance terminal SUCCESS**。新規15宣言すべて`#print axioms`で標準3公理`propext/Classical.choice/Quot.sound`以内、sorryAx0、変更Lean error/warning0/0。定理squash・canonical main HEAD `19058c78848ffa1198f1f1ea52889ab3b97c1970`。

**次の研究GK4BY（仮称）：** 真正逆unitorの自然性・単位挿入位置を増やした有限段混合coherence・一般有限段へ至る条件を調べる。ただし原Sの無条件faithfulness、source-Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray/hyperdescentは未証明境界。Lean v4.30.0-rc2／pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、root107、保護PR #1558 Draft/OPEN、strict空中心・独立Kuuは一presentation。以下GK4BW以前の履歴を完全保持する。

## 最新のLean定理統合 — F112-P94D3GK4BW / 2026-11-01 JST

**GK4BVの任意選択逆関手の二段標的合成の厳密整合性を、三段結合・四段pentagon・左右単位則・三方向の標的自然変換に拡張 — [定理PR #2889](https://github.com/itakura-hidetoshi/KuuOS/pull/2889) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BWChosenInverseHigherTargetPentagonUnit.lean)・[正式証明記録](docs/formal/GK4BW-chosen-inverse-target-pentagon-unit-coherence.md)。既存F45依存型構造商`S`、実到達旧AH観測圏`A_att`、真のAH核両立全充満部分圏`Comp_T`を固定し、GK4BMの任意選択逆`Q_T`とGK4BPの明示因子逆`P_T`を定義上同一視せずGK4BQの`κ_T:Q_T≅P_T`を用いる。

**型付き高次標的coherence：** 任意の`R:T⥤U`、`S:U⥤V`、`L:V⥤W`で、`(R,S)`を先に貼る3段NatIsoと`(S,L)`を先に貼る3段NatIsoを実際のMathlib比較として構成し、両方が直接の`Θ_(R⋙S⋙L)`に一致することを証明。さらに4段`R,S,L,M`の**5つの実NatIso括弧経路**それぞれを構成して`Θ_(R⋙S⋙L⋙M)`との厳密等式を示し、5頂点のpentagon整合性を証明した。二段比較に標的単位`𝟭`を挿入する**左右単位則**、第1/第2/第3段の本物の標的自然変換四角、3変換の水平合成について**左括弧から右括弧へまたぐwhole NatTrans可換四角**も形式化した（公開25宣言）。

**exact-source：** source `0097f7a692d8f74a61367b148dd325ba03e54091`、test-merge `80a21116fac82f0b3c58bb809c205fb9ad36db98`、一致Git tree `13afe4f849a7b5024ac57d5f2a754351a71258cb`。[CI #41297928591](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41297928591) **Strict Lean 3818/3818 SUCCESS・Independent Kuu・Workflow integrity・Governance terminal SUCCESS**、25公開宣言すべて`#print axioms`で標準3公理`propext/Classical.choice/Quot.sound`以内、`sorryAx`0、変更Lean error/warning 0/0。定理squash/main HEAD `91b2a9f9dd8287952defbf4657a76bbffc9d28bc`。

**次の研究GK4BX（仮称）：** 4段pentagonに対する独立の標的自然変換・unit coherenceを整理し、Mathlibの本物のunitor／associatorと選択逆比較のcompatibilityをさらに形式化する。原Sの無条件faithfulness、source-Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray/hyperdescentの未証明境界を維持する。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ、strict空中心・独立Kuu一presentation・Gray非再導入。以下GK4BV以前の履歴は保持する。

## 最新のLean定理統合 — F112-P94D3GK4BV / 2026-11-01 JST

**GK4BTで得た任意選択逆関手の真正標的変更NatIso `Θ_R`について、二段標的変更の貼り合わせ同型が直接の`Θ_(R⋙L)`とwhole Mathlib NatIsoで厳密に一致することをLean4で証明 — [定理PR #2887](https://github.com/itakura-hidetoshi/KuuOS/pull/2887) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BVChosenInverseCompositionCoherence.lean)・[正式証明記録](docs/formal/GK4BV-two-target-chosen-inverse-composition-coherence.md)。元F45の依存型独立構造商`S`、旧AHの真正実到達像`A_att`、GK4BMの厳密なAH核両立`ObjectProperty.FullSubcategory` `Comp_T`、明示因子逆`P_T`、任意選択逆`Q_T`を一切変更しない。GK4BQの`κ_T:Q_T≅P_T`、GK4BPの明示逆の厳密標的可換性、GK4BUの標的自然変換方向のwhole可換四角を再利用した。

**二段比較の完全一致：** 任意の`R:T⥤U`、`L:U⥤V`について、`eqToIso`による両端の厳密標的合成輸送、3か所のMathlib `Functor.associator`、`Θ_R`と`Θ_L`の左右whiskeringを貼り合わせた真正NatIso `Θ²_(R,L)` を構成し、**`Θ²_(R,L)=Θ_(R⋙L)`というwhole NatIsoの等式**を証明した。まず明示`P`の二段輸送が直接輸送`eqToIso`と一致することを証明し、一般ゲージ補題では`κ_V`の自然性、`κ_U.inv`と`κ_U.hom`の相殺、`κ_T.inv`の自然性を元の型のまま示して、結果を任意選択`Q`へ移送した（公開5宣言・private5補題）。`Q_T`の定義的strict標的自然性は仮定しない。

**exact-source：** source HEAD `6fd24887dee2ef1ec9b4760f2caa6a2160437a40`、test-merge `eab1c47bf15ee3d4f661fc44b93f10dece7264fb`、**一致Git tree `c06899e9f85283ed280bb120b123bc379c76f4e4`**。[CI #41296105367](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41296105367) **Strict Lean 3817/3817 SUCCESS・Independent Kuu・Workflow integrity・Governance terminal SUCCESS**、全5公開宣言の公理依存は`propext`／`Classical.choice`／`Quot.sound`以内、sorryAx0、changed Lean warnings/errors0/0。定理squash/main HEAD `b9818a9c74ca159c4a2ffce134a163e03df58246`。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ。

**次の研究GK4BW（仮称）：** GK4BVの二段標的合成・GK4BUの標的自然変換を統合し、三段合成のpentagon型coherenceとunit coherenceがどこまで真に導かれるか、associatorと等式輸送を保持して検証する。元Sの無条件忠実性、原Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray/hyperdescentは未証明境界のまま維持する。以下GK4BU以前の履歴を変更しない。

## 最新のLean定理統合 — F112-P94D3GK4BU / 2026-11-01 JST

**GK4BMの任意選択逆関手を比較するGK4BTの自然同型について、任意の標的自然変換 `ρ:R⟶R'` に関するwhole Mathlib NatTrans可換四角をLean4で証明 — [定理PR #2885](https://github.com/itakura-hidetoshi/KuuOS/pull/2885) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BUChosenInverseTargetNatTransCoherence.lean)・[正式証明記録](docs/formal/GK4BU-chosen-inverse-target-nattrans-coherence.md)。GK4BJの元F45型付き観測関手、旧AH**実到達**圏`A_att`、GK4BMの真正AH核両立`ObjectProperty.FullSubcategory`である`Comp_T`をそのまま使用。GK4BMの任意選択逆`Q_T`とGK4BPの明示因子逆`P_T`のGK4BQ比較`κ_T:Q_T≅P_T`を利用し、GK4BTで構成済みの`Θ_R:R_*^Comp⋙Q_U≅Q_T⋙R_*^A`が**標的自然変換方向にも整合**することを、実圏のwhole NatTrans等式として形式化した。

**型付き主定理：** `(ρ_*^Comp ▷ Q_U) ≫ Θ_R'.hom = Θ_R.hom ≫ (Q_T ◁ ρ_*^A)`。証明は`κ_U`との交換、GK4BPの厳密標的自然変換四角、`κ_T^{-1}`との交換を貼り合わせる。中間の`eqToIso`は定義上の恒等射とはみなさず、別に証明した**HEqとeqToHomの一般輸送補題**で真正に処理。恒等・垂直合成・水平interchange、および二段標的変更`T→U→V`の第1段・第2段それぞれの自然変換に関するwhole可換四角まで形式化した（**公開9宣言＋private補題1件**）。ただし任意選択`Q_T`の定義的strict標的自然性、また`Θ_(R⋙Q)`と`Θ_R,Θ_Q`の完全な貼り合わせ同一性は別命題として区別する。

**exact-source：** source HEAD `d49f8df5021562590e70db2640221aa20e7bc10d`、test-merge HEAD `3fe8cd56d664c5571f8b991adb6d6b6b5e5ca7c9`、**一致Git tree `d5f8b4cf33e8a5f072b936c2c4391b998ed72afd`**。[CI #41284678233](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41284678233) **Strict Lean 3816/3816 SUCCESS・Independent Kuu SUCCESS・Governance terminal SUCCESS**。全9公開宣言の公理依存は`propext`／`Classical.choice`／`Quot.sound`以内、sorryAx0、changed Lean warnings/errors 0/0。定理squash・main HEAD `118d5f2f4121cdc4465f8407ef5b6684ddeace94`。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ。

**次の課題：** `Θ_(R⋙Q)`と二段の`Θ_R,Θ_Q`の合成との間の依存型associator／eqToIso輸送まで含めた厳密なpseudonatural composition coherenceを検証する。元Sの無条件忠実性、元Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray/hyperdescentは未証明境界として維持する。以下GK4BT以前の履歴はすべて保持する。

## 最新のLean定理統合 — F112-P94D3GK4BT / 2026-11-01 JST

**真正標的自然変換の垂直合成・水平交換をGK4BSのwhole unit/counit可換性と統合し、GK4BMの任意選択逆関手について標的変更による真正Mathlib自然同型をLean4で構成 — [定理PR #2883](https://github.com/itakura-hidetoshi/KuuOS/pull/2883) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BTTargetInterchangeChosenInverse.lean)・[正式証明記録](docs/formal/GK4BT-target-interchange-chosen-inverse-transport.md)。元F45依存型独立構造商`S`と旧AHの**真正実到達**圏`A_att`、元AH観測核に両立するGK4BMの真正`ObjectProperty.FullSubcategory`である`Comp_T`を保持。GK4BOの標的作用`R:T⥤U`および自然変換`ρ:R⟶R'`・`σ:R'⟶R''`の恒等・垂直合成保存を、GK4BSの**whole adjointified unit/counit自然性**と結合し、実Mathlib NatTrans／compatible部分圏Homの垂直貼り合わせ可換式を形式化した。さらに`ρ:T→U`・`σ:U→V`の**水平二経路の真正interchange**を、実到達AH側とComp側の両whole target NatTransで示し、その合成に対応するunit/counitの可換四角を証明（新規11宣言）。

**選択逆関手の自然同型によるtransport：** GK4BMの`asEquivalence`が選ぶ任意の逆関手`Q_T`と、GK4BPの**明示的**因子逆関手`P_T`にはGK4BQの真正比較`κ_T:Q_T≅P_T`がある。GK4BPの厳密な`R_*^{Comp}⋙P_U=P_T⋙R_*^A`と`κ_T,κ_U`の左右whiskering、`eqToIso`を結合し、**任意Rについて`R_*^{Comp}⋙Q_U ≅ Q_T⋙R_*^A`というwhole Mathlib NatIso**を実構成。その自然性は任意の実`Comp_T`射で証明した。ただし`Q_T`の**定義上の厳密等式**や、`R`を変化させる標的自然変換`ρ`に関する比較Iso間のmodificationは未証明として保持する。

**exact-source：** final source HEAD `8672abb7b520ad7125c5d4aaa527561868d09713`、test-merge `40f4be75237ae32026c3a8dddde8de386c1f64c5`、**一致Git tree `f00c9e24f063996ff3c1a6b809c312685f0ad97a`**。[CI #41282614826](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41282614826) **Strict Lean 3815/3815 SUCCESS・Governance terminal SUCCESS・Independent Kuu/Workflow integrity SUCCESS**、全11宣言の公理依存は`propext`／`Classical.choice`／`Quot.sound`以内、sorryAx0、changed Lean errors/warnings0/0。定理squash/main統合時HEAD `de9693e0c8b1c4b2d6c86a1cf3a261638302cc53`。Lean v4.30.0-rc2・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ。

**次GK4BU：** `κ_T`を使う選択逆関手の標的比較Isoについて、`ρ:R⟶R'`に対する真のwhole NatTrans可換四角、恒等・垂直合成・水平交換・二段標的変更との整合性を厳密検証する。元S無条件faithfulness、原Q圏公理、raw F54/F55/P92B Type値高次セル、全整数行列到達、global Gray/hyperdescentは未証明境界として維持し、以下GK4BS以前の記録は履歴として保持する。

## 最新のLean定理統合 — F112-P94D3GK4BS / 2026-11-01 JST

**真正GK4BQのunit/counitの標的自然性を成分別からwhole Mathlib NatTransへ強化し、adjointify後unitと具体的unitの厳密一致をLean4で証明 — [定理PR #2881](https://github.com/itakura-hidetoshi/KuuOS/pull/2881) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BSWholeTargetNatTransCoherence.lean)・[正式証明記録](docs/formal/GK4BS-whole-target-nattrans-adjointified-unit.md)。元の真正F45型付き独立構造商`S`、旧AHの**実到達**圏`A_att`、GK4BMの正確なAH核両立`ObjectProperty.FullSubcategory`、GK4BPの明示逆関手`P_T`、GK4BQの前向き観測`C_T`と具体的unit/counitをそのまま保持。GK4BRの任意`R:T⥤U`と自然変換`ρ:R⟶R'`についての**対象ごとの可換式**を、`Functor.whiskerRight`と充満部分圏の`.hom`を使って**whole Mathlib NatTrans・本物の部分圏Homの厳密等式**に強化した。unit/counitの逆変換と二段標的変更`T→U→V`も含めて13宣言。

**新しいadjointify整合：** GK4BQの既証明**前向き三角恒等式**を、実到達AH対象`X`の元F45構造境界`X.original`において比較すると、adjointified unitの成分が`α.app X ≫ 𝟙 = 𝟙`を満たす。固定版Mathlibの`Category.comp_id`により`α.app X=𝟙`と証明し、**`nativeGK4BQTriangleUnitIso = nativeGK4BQExplicitUnitIso`というwhole NatIsoの厳密等式**を導いた。これにより`Equivalence.mk`が調整した**実際のunit**についても、任意Rの後合成・whole target-`ρ`可換四角・二段標的変更の整合性を形式化した。一般の圏同値すべてでadjointificationが恒等であるとは主張しない。GK4BMの任意選択逆関手の厳密標的自然性、元Sの無条件忠実性やraw F54/F55の未充填高次セルも推論しない。

**exact-source：** source HEAD `f39afbe1fb74e1ec7569f28828a62a890ef61503`、test-merge HEAD `8558cd9fd472d520b84ebd4bc3ce7a35c0404651`、**一致Git tree `eca8979b53d1dbf50fb8dd83cf7290584c7b3d59`**。[CI #41281159070](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41281159070) **Strict Lean 3814/3814・Governance terminal SUCCESS・Independent Kuu SUCCESS**、全13宣言の公理依存は`propext`／`Classical.choice`／`Quot.sound`以内、sorryAx0、変更Lean warning/error0/0。Lean v4.30.0-rc2・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、定理squash `584606a21dffc8e755d01ebfd6c4522e734a83bb`、保護PR #1558 Draft／OPEN／未マージ。

**次GK4BT：** whole unit/counitの標的自然変換`ρ`への可換四角を、恒等・垂直合成・二段の水平interchangeと統合し、可能な範囲で本物の2-categorical modificationを型付き形式化する。選択`asEquivalence`逆関手についてはGK4BQ自然同型を経由した比較に留め、元Q圏公理・unattained行列・global Gray/hyperdescentは未証明として保持。以下のGK4BR以前の記録はすべて履歴として維持する。

## 最新のLean定理統合 — F112-P94D3GK4BR / 2026-11-01 JST

**GK4BQの真正natural unit/counit Isoが、任意の標的関手・標的自然変換・二段標的変更と整合することをLean4で形式化 — [定理PR #2879](https://github.com/itakura-hidetoshi/KuuOS/pull/2879) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BRUnitCounitTargetCoherence.lean)・[正式証明記録](docs/formal/GK4BR-unit-counit-target-naturality.md)。元F45依存型独立構造商`S`、旧AH**実到達**圏`A_att`、GK4BMの真正AH核両立充満部分圏`Comp_T`を変更せず、前向き観測`C_T`とGK4BP**明示的**因子逆関手`P_T`に対するGK4BQの具体的`η_T:𝟭≅C_T⋙P_T`・`ε_T:P_T⋙C_T≅𝟭`を対象とした。任意の`R:T⥤U`について到達AH対象上のunit、元F45型付き構造対象上のcounitが`R.map`と可換であることを証明し、**whole NatIsoの具体的成分への作用**、任意の標的自然変換`ρ:R⟶R'`の実射で構成した**可換四角**、二段の標的変更`T→U→V`の整合性まで12宣言で証明した。

**成立範囲：** GK4BRはあくまで**具体的GK4BQ unit/counitの成分別標的自然性**を型付きMathlib射の厳密等式として確立した。GK4BQの`Equivalence.mk`が**adjointifyしたunit全体**についてのtarget-varying modificationや、GK4BMの任意選択`asEquivalence`逆関手のstrict標的自然性を推論しない。元Sの無条件忠実性、元Q圏公理、raw F54/F55/P92B Type値3-cell、全整数行列到達、global Gray/hyperdescentも未証明のまま維持する。

**exact-source：** source HEAD `90e7bb94fb3c977408356c845ba02bba4ec6cebf`、test-merge HEAD `bf3ac16a13dc88efa7a14af655328612b0610aa8`、**一致Git tree `fc4f5faaa54f093f44a50e2a9dbf1ed6e1631ebb`**。[CI #41279800486](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41279800486) **Strict Lean 3813/3813、Governance terminal SUCCESS、独立Kuu/Workflow integrity SUCCESS**。12宣言の公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAx0、changed Lean warning/error0/0。定理squash/main統合時HEAD `761e1fe327b1c0dfac1052e53a08bd0989566088`。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ。

**次GK4BS：** 得られた標的自然変換ごとの可換四角を、依存型輸送を明示したMathlib whole NatTrans/modified coherenceへ拡張し、adjointify後のunitについて成立する自然性の正確な範囲とobstructionを特定する。以下のGK4BQ以前は履歴として完全に保持する。

## 最新のLean定理統合 — F112-P94D3GK4BQ / 2026-11-01 JST

**真正元F45依存型独立構造商のAH核両立関手圏と旧AH実到達像の間で、GK4BPの明示逆関手のnatural unit/counit同型、両triangle coherence、およびGK4BM選択逆関手との自然同型をLean4で証明 — [定理PR #2877](https://github.com/itakura-hidetoshi/KuuOS/pull/2877) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BQExplicitEquivalenceNaturality.lean)・[正式証明記録](docs/formal/GK4BQ-explicit-equivalence-unit-counit.md)。元の真正観測`F:S⥤A_att`を前合成する`C_T:(A_att⥤T)⥤Compatible(S,T)`と、GK4BPで**明示的に構成済みの**因子化逆関手`P_T`について、元F45構造射の実前像およびGK4BK因子射保存を使って、**真正`𝟭≅C_T⋙P_T`、`P_T⋙C_T≅𝟭`のwhole Mathlib NatIso**を構成。単なる対象等式ではなく、到達AH上の全Hom、元S上の全Hom、対象間の自然変換を含む。

**両三角・逆関手の同型：** pinned Mathlib `CategoryTheory.Equivalence.mk`によって自然unitをadjointifyし、前向き・逆向き**両triangle恒等式**を真正Mathlib圏同値の定理として確認。`nativeGK4BQExplicitFunctorEquivalence`のforward/inverseはそれぞれ既存`C_T`と明示`P_T`と定義的に一致するが、GK4BMの`asEquivalence`が任意に選択した別の逆関手は**`Iso.isoInverseOfIsoFunctor`で得るwhole自然同型によってのみ比較**し、定義同一視しない（12宣言）。元Sの無条件忠実性、raw F54/F55 Type値3-cell、global Gray/hyperdescentは導入しない。

**exact-source：** source HEAD `b95a97ae2db1db770fe3fa3bfc8e92253040ca20`、test-merge HEAD `a3ed6f0cd3984cc31719258debdcb677c21b44b9`、**一致Git tree `8069956b19234e3aa33934840ea99d27970ff0b2`**。[CI #41279066499](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41279066499) **Strict Lean 3812/3812、Governance terminal SUCCESS、独立Kuu/Workflow integrity SUCCESS**。全12宣言の公理依存は`propext`/`Classical.choice`/`Quot.sound`以内、sorryAx0、changed Lean warning/error0/0。厳密なwhole functor等式の型依存輸送と、pinned mathlibの`Category.comp_id`・`Category.id_comp`・`CategoryTheory.Equivalence.mk`の名前解決を検証、数学的主張を弱めず、最後は`G.map f=G.map f`を`rfl`で閉じた。定理squash `d273406321365fbb5b32e82e651be64e16fde9bd`。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ。

**次GK4BR：** 既存GK4BO標的作用・GK4BP明示逆関手のstrict標的可換性を用い、今回の具体的unit/counitとadjointified unitの**標的関手・標的自然変換に関する整合性**を、成立する型付き範囲に限定して検証する。任意選択quasi-inverseは自然同型までの比較に留める。以下GK4BP以前は履歴として保持。

## 最新のLean定理統合 — F112-P94D3GK4BP / 2026-11-01 JST

**真正元F45独立構造商のAH核両立関手圏から旧AH実到達像への、明示的な逆Mathlib関手と標的自然変換への厳密整合性をLean4で形式化 — [定理PR #2875](https://github.com/itakura-hidetoshi/KuuOS/pull/2875) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BPExplicitInverseTargetNaturality.lean)・[正式証明記録](docs/formal/GK4BP-explicit-inverse-target-naturality.md)。GK4BKの真正実到達AH因子化`Factor(H)`を、任意の元AH核両立`S⥤T`関手`H,K`と実自然変換`η:H⟶K`に拡張し、元F45型付き境界`X.original`上の`η.hom.app`と真正元構造射前像`s`から自然性を証明。`Factor_T: Compatible(S,T) ⥤ (A_att⥤T)`という**独立に明示構成した本物のMathlib Functor**を取得、恒等・垂直合成を保存。GK4BMの`asEquivalence`が任意に選ぶ逆関手と**定義上同一とは主張しない**。

**厳密な双方向整合性：** `Factor_T ⋙ C_T`は各兼容対象`H`をwhole-Functor等式で`H`へ戻し、`C_T ⋙ Factor_T`は各真正実到達AH関手`G`をGK4BK一意性でwhole-Functor等式として`G`へ戻す（対象レベルの両三角）。元構造上の実自然変換成分も完全に回復。`R:T⥤U`に対して`R_*^{compatible} ⋙ Factor_U = Factor_T ⋙ R_*^{attained}`を**whole Mathlib Functorの厳密等式**で証明し、Homのright-whiskering、任意の`ρ:R⟶R'`の**whole NatTrans自然性四角**まで形式化（14宣言）。新明示逆関手についての**global unit/counit NatIsoとその三角恒等式は未実装**であり、対象レベルの等式と区別する。

**exact-source：** source HEAD `8637e2af4545d1143b0c7a85c13e0d7fda15a9b5`、test-merge HEAD `e6a88e87350aab3c27e27466c0d2e8ec00f308f6`、**一致tree `8cecacbfab355d00c05fbf7c9b313fb8315fc725`**。[CI #41276846796](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41276846796) **Strict Lean 3811/3811・Governance terminal SUCCESS**、独立Kuu／Workflow integrity SUCCESS、全14宣言の公理依存`propext`／`Classical.choice`／`Quot.sound`以内、sorryAx0、changed Lean warning/error0/0。定理squash・main統合HEAD `8c0f7a166d4156aefcc66b7e002501bcebba4cff`。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft/OPEN/未マージ。

**次GK4BQ：** 明示逆関手`Factor_T`とGK4BM前向き関手`C_T`の**真正natural unit/counit isomorphisms**、三角恒等式とGK4BMの任意選択quasi-inverseとの適切な自然同型による比較を研究。元Sの無条件忠実性、元Q圏公理、raw F54/F55/P92B Type値3-cell、全整数行列到達、高次global strict/hyperdescentは未解決のまま。以下のGK4BO以前の記録は保存する。

## 最新のLean定理統合 — F112-P94D3GK4BO / 2026-11-01 JST

**真正AH核両立関手圏における標的自然性を、一つのMathlib関手と厳密な交換法則として形式化 — [定理PR #2873](https://github.com/itakura-hidetoshi/KuuOS/pull/2873) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BOTargetActionFunctor.lean)・[正式証明記録](docs/formal/GK4BO-target-action-functor-interchange.md)。GK4BNの任意の標的関手`R:T⥤U`による真正後合成、および標的自然変換`ρ:R⟶R'`から得られる`NatTrans`を、`(T⥤U) ⥤ (Compatible(S,T)⥤Compatible(S,U))`という**一個の真正Mathlib Functor**に統合。元F45依存型独立構造商Sと旧AH**実到達像A**、真正`ObjectProperty.FullSubcategory`を変更せず、自然変換の恒等・垂直合成を関手公理として証明した（12宣言）。

**厳密な自然性・交換：** GK4BMの前向き圏同値と真正到達AH側の`Functor.whiskeringRight`との自然変換四角を**whole NatTransの等式**として確認し、`ρ:R⟶R'`、`σ:Q⟶Q'`の二段標的変更について**Mathlib`Functor.whiskerLeft_comp_whiskerRight`の真正交換法則**を形式化。対象・Homの全関手恒等・合成もGK4BNと整合させた。これは**有界な関手圏の自然変換の数学**であり、元raw F54 Type値3-cell、高次hyperdescent、Gray構造を追加しない。

**exact-source：** source HEAD `83bfde427ef364647863278a895c6c7d5ac14c77`、test-merge `f8772428faebd26217bed45235293213ad173cd2`、**一致tree `b6e5f2e5d3b70b9ad130529de2011b85c721d71a`**。[CI #41275594655](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41275594655) **Strict Lean 3810/3810・Governance terminal SUCCESS**、独立Kuu/Workflow integrity SUCCESS、全12宣言は標準3公理`propext/Classical.choice/Quot.sound`以内、sorryAx0、変更Lean warning/error0/0。初回CIの2か所は`NatTrans.ext`適用後に関数等式を`intro`で処理した誤りを`funext`へ修正、定理・仮定は不変。定理squash `57a089b6a22d38cf0c707973aa81671aaaf2f1df`。Lean v4.30.0-rc2／pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107・保護PR #1558 Draft/OPEN/未マージ。

**次GK4BP：** 明示的GK4BK因子関手と自然変換降下の標的自然性を、GK4BMのunit/counitとの整合まで**成立する範囲に限って**厳密化する。特に明示因子化のstrict等式と、任意に選んだquasi-inverseの自然同型を区別する。元Sの無条件忠実性、原Q圏公理、raw F54/F55/P92B値の未充填、高次global strict/hyperdescentは未証明のまま保持。以下のGK4BN以前は履歴として保存する。

## 最新のLean定理統合 — F112-P94D3GK4BN / 2026-11-01 JST

**真正実到達AH観測による関手圏同値の「標的圏に関する自然性」を、任意の標的関手・自然変換・恒等・合成までLean4で形式化 — [定理PR #2871](https://github.com/itakura-hidetoshi/KuuOS/pull/2871) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BNTargetPostcompositionNaturality.lean)・[正式証明記録](docs/formal/GK4BN-target-postcomposition-naturality.md)。既存GK4BMの真正圏同値`Fun(A_AH^att,T) ≌ Fun_AH-compatible(S,T)`の正方向関手`C_T`について、任意の標的圏`T,U`・実関手`R:T⥤U`により、元独立構造商の**AH核両立性が無条件に保存される**ことを証明。GK4BJの真正元F45依存型観測`F:S⥤A_AH^att`とpinned Mathlibの右whiskeringを使い、実到達AH関手圏と**真正`ObjectProperty.FullSubcategory`であるAH核両立関手圏**上のターゲット後合成関手を実構成した。

**厳密な可換性：** `R_*^A ⋙ C_U = C_T ⋙ R_*^{compat}` を、型付き対象と自然変換Hom双方について**whole Mathlib Functorの厳密等式**で証明（`nativeGK4BNPostcomp_precomposition_square`）。さらに任意の標的自然変換`ρ:R⟶R'`から実`NatTrans`を構成、Mathlib`whiskerLeft_comp_whiskerRight`による自然性、**whole NatTransの可換四角の厳密等式**、GK4BLの逆自然変換降下と`R`の厳密交換、GK4BKの実因子関手と`R`の厳密交換、標的恒等・二段後合成の厳密法則まで18宣言で証明。これは**標的圏に関する有界な関手・自然変換レベル**の結果で、未証明の高次coherenceやGray・hyperdescentを追加しない。

**exact-source：** 最終source HEAD `80bb2b64931a6f13107c089949856b7c3f0ac971`、test-merge HEAD `1fe834d5115d39560153f2fed4eee71695386e33`、**一致Git tree `e05c0f8bae3ba05ea38e7e81a6c4954883a0f1d8`**、[CI #41270237079](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41270237079) **Strict Lean 3809/3809・Governance terminal SUCCESS**、18宣言の公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAx0、変更Lean warning/error0/0。初回CIの`ObjectProperty.FullSubcategory`射と基底`NatTrans`の型不一致1か所は、射の`.hom`を明示して元の定理を一切弱めず修正、全文・imports・関連署名・pinned mathlib APIを再確認した。定理squash／main統合時HEAD `17a4b3e291d54ebd49b8e3bada589f5cab186b65`。Lean v4.30.0-rc2、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージ、strict空中心・独立Kuu一presentation・Gray非再導入。

**次GK4BO：** 任意の標的`R:T⥤U`と自然変換`ρ:R⟶R'`に対するGK4BNの真の作用を、**標的関手圏から対応する兼容関手圏間の関手圏へのMathlib関手**として統合し、`ρ`の恒等・垂直合成と交差自然性を型付き完全検証する。元S忠実性、原Q圏公理、raw Type値F54/F55/P92B source、全整数行列到達、真正14D無条件Countable、19D filler、global strict・hyperdescentは引き続き未証明。以下のGK4BM以前は歴史的記録として保持する。

## 最新のLean定理統合 — F112-P94D3GK4BM / 2026-11-01 JST

**真正実到達AH像上の関手圏と、元F45独立構造商のAH核両立関手充満部分圏との真正Mathlib圏同値を証明 — [定理PR #2869](https://github.com/itakura-hidetoshi/KuuOS/pull/2869) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BMCompatibleFunctorCategoryEquivalence.lean)・[正式証明記録](docs/formal/GK4BM-compatible-functor-category-equivalence.md)。任意の標的Mathlib圏`T`について、既存GK4BJ関手`F:S⥤A_AH^att`（元真正F45型付き独立構造商`S`→**実到達**旧AH行列圏）を前合成する関手が、`S⥤T`の**元AH観測核両立関手からなる真正`ObjectProperty.FullSubcategory`**への`Mathlib Functor.IsEquivalence`を構成することをLean4で証明した。GK4BKの各Hの厳密一意因子化で対象全射、GK4BLの自然変換降下Equivで全忠実性を証明し、`nativeGK4BMCompatibleFunctorEquivalence`で**真の`CategoryTheory.Equivalence`、逆Mathlib関手、unit/counit自然同型と三角恒等式**まで構成した。**`Fun(A_AH^att,T) ≌ Fun_AH-compatible(S,T)`**（15宣言）。対象は元AH観測核と両立する`S→T`関手に厳密に限定し、`S≌A_AH^att`や`S→T`全体との圏同値・raw F54 Type値3-cellの同一性は主張していない。

**exact-source：** source HEAD `5d80f02ad6fc470801b8779e1b88b19d2e966fbd`、test-merge HEAD `1209c1b1faab70b9190b3c489969721768ca987b`、**共通Git tree `6379880c8eeab06dfa1debb0f6e32eedfb3914e4`**。[CI #41269022170](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41269022170) **Strict Lean 3808/3808 SUCCESS・Governance terminal SUCCESS**、変更Lean1ファイルの15公理監査宣言は標準3公理`propext`・`Classical.choice`・`Quot.sound`以内、sorryAx0、warning/error0/0。定理squash／main統合時HEAD `c0625a9981756fa33c8309687c300dba973dcd8e`。Lean v4.30.0-rc2、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107維持、保護PR #1558 Draft／OPEN／未マージ、strict空中心・独立Kuu一presentation・Gray非再導入。

**次GK4BN：** GK4BMの真正圏同値について、標的圏`T`から`U`への任意の実関手による後合成の**compatibility保存・precompositionとの可換性・自然変換レベルの整合性**を形式化し、標的圏に関する2-自然性の正確な境界を評価する。元Q圏公理、S忠実性、全整数行列到達、真正14D無条件Countable、19D filler、global strict・hyperdescentは引き続き未証明。下段のGK4BL以前は当時の歴史的記録として残す。

## 最新のLean定理統合 — F112-P94D3GK4BL / 2026-11-01 JST

**実到達AH像への自然変換の一意降下と、precomposition関手のMathlib FullyFaithfulを証明 — [定理PR #2867](https://github.com/itakura-hidetoshi/KuuOS/pull/2867) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BLNaturalTransformationDescent.lean)・[正式証明記録](docs/formal/GK4BL-natural-transformation-attained-ah-descent.md)。GK4BJで確立した元F45依存型独立構造商`S`から**実到達**旧AH像圏`A_AH^att`への対象全射・各Hom全射関手`F:S⥤A_AH^att`について、任意の標的Mathlib圏`T`と任意の関手`G,H:A_AH^att⥤T`に対し、**`Nat(G,H) ≃ Nat(F ⋙ G,F ⋙ H)`**を元の型付きF45対象と真正S-Hom実前像から構成。自然変換の実降下、その自然性を全実到達AH射で証明し、`whiskerLeft`との両側逆、自然変換Equiv、**`nativeGK4BLPrecomposition_fullyFaithful`**、逆降下の恒等・垂直合成保存までLean4で形式化した。さらにGK4BKの証明済み普遍性と組み合わせ、precompositionの対象像が**元構造商AH観測核両立Functorに正確に一致**し、その因子関手が厳密に一意であることを証明（14宣言）。ここで`F ⋙ G`は通常の数学記法では`G ∘ F`、**S自身のfaithfulnessは未証明**。

**exact-source：** 最終source HEAD `552ceba6d198ae5dea904f54180eec8fc06837ff`、test-merge HEAD `2cc93f9a9999ef2a5ec0f6595b276e82f25ba14f`、**共通Git tree `bd5c5b367fee25b02d0b748dc1be835cd17b6a6e`**、[CI #41268260288](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41268260288) **Strict Lean 3807/3807 SUCCESS・Governance terminal SUCCESS**、新規14宣言の公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAx0、変更Lean warning/error0/0。定理squash／main当時HEAD `de974ee81059215aab4e32ea74c2ced273d1284c`。Lean v4.30.0-rc2、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft／OPEN／未マージ維持、strict空中心・独立Kuu一presentation・Gray非再導入。

**次GK4BM：** GK4BKの対象像`iff AH-kernel-compatible`とGK4BLの自然変換全忠実性を、**実到達AH圏のFunctor圏とS→TのAH核両立Functorのfull subcategory間の真正Mathlib圏同値**へ組み立てる。元構造商Sとの無条件圏同値や元Type値経路等号、元Q圏公理、全整数行列到達、真正14D無条件Countable、19D filler、global strict・hyperdescentは未証明のまま。以下のGK4BK以前の研究欄は当時の履歴として保持する。

## 最新のLean定理統合 — F112-P94D3GK4BK / 2026-11-01 JST

**真正独立構造商Sから実到達AH像への普遍因子化をMathlib関手の厳密等式・一意性まで形式化 — [定理PR #2865](https://github.com/itakura-hidetoshi/KuuOS/pull/2865) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BKUniversalAHFactorization.lean)・[正式証明記録](docs/formal/GK4BK-universal-attained-ah-kernel-factorization.md)。GK4BJで証明済みの元F45依存型独立構造商`S`から**真正実到達**旧AH行列圏`A_AH^att`への対象全射・各Hom全射関手`F`について、**任意の標的Mathlib圏T、任意の実Functor `H:S⥤T`** を対象に、元構造商の旧AH観測値が等しい全型付きHom対をHも同一視する条件を定式化。全元構造商Homの実前像を利用し、代表元に依存しない因子関手`G:A_AH^att⥤T`を実構成して単位・合成保存、**関手全体の等式`F ⋙ G = H`**、必要条件・十分条件、**`∃!G`の厳密一意性**をLeanで証明した（14宣言）。これは一般1圏のobserver-kernel universal descentであり、元SのAH忠実性、raw Type値経路同一性、元Q圏公理、全整数行列到達、高次hyperdescentを主張しない。

**exact-source：** 最終source `2aec9d7e09d70c2cee938387345a6b4a80841faa`、test-merge `9760cb4dd85798d55d7b40eaa8ad833310a0e151`、**一致Git tree `97a9a139e87794c5803b6654a9e9441f0638cb03`**、[CI #41267046208](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41267046208) **Strict Lean 3806/3806・Governance terminal SUCCESS**、新規14宣言標準3公理`propext`・`Classical.choice`・`Quot.sound`以内、sorryAx0、変更Lean warning/error0/0。Lean4依存型Functor.extの`eqToHom`輸送で初回〜第4回CIに検証失敗があり、pinned mathlibの`Functor.toPrefunctor_injective`と`Prefunctor.ext`により**同一の厳密関手等式**を証明して全ファイルを再検証。定理squash/main当時HEAD `693ffe9acd64fea561d7058b844e85ee2d869609`。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft・OPEN・未マージ維持、strict空中心・独立Kuu一presentation・Gray非再導入。

**次GK4BL：** GK4BKの対象関手に関する普遍性を**自然変換のAH核降下と自然性**へ拡張し、実到達AH圏から任意TへのFunctor圏とSからTへのAH核両立Functorの比較を精密化する。元Type値高次証拠やhyperdescentと同一視せずobstructionを残す。以下のGK4BJ以前の「次GK4BK」は当時の履歴記録であり、現在のfrontierは本欄とする。

## 最新のLean定理統合 — F112-P94D3GK4BJ / 2026-11-01 JST

**独立構造商S→真正実到達AH行列圏のFull・EssSurjおよび正確な観測核と圏同値条件を証明 — [定理PR #2863](https://github.com/itakura-hidetoshi/KuuOS/pull/2863) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BJStructuralAttainedAHDescent.lean)・[正式証明記録](docs/formal/GK4BJ-structural-attained-ah-exact-descent.md)。既存の真正F45境界型付き独立構造商`S`から既存第二kernel圏`K_AI`へのGK4AI関手と、GK4BIによる`K_AI ≌ 実到達AH行列圏`の正方向関手を**元のまま合成**。`nativeGK4BJStructuralAHFunctor`は実到達AH像に対して対象全射・各Hom全射であり、Mathlib `Full`・`EssSurj`を実証した。

**正確なkernel：** 同じ元Type値型付き始終点の任意の構造商射`u,v`について、**合成関手像が一致 iff 元構造商の実際の旧AH観測`nativeGK4AHStructuralValue u = nativeGK4AHStructuralValue v`**（`nativeGK4BJStructuralAH_eq_iff`）。したがって**`S → 実到達AH`が真の圏同値 iff 元構造商AH観測が全Homで単射**（`nativeGK4BJStructuralAH_isEquivalence_iff`）。Full・EssSurjは無条件証明したが、**S上のAH単射性自体は主張していない**。元Q圏公理、元Type値F54 raw等号、未到達の全整数行列、真正14D無条件Countable、19D filler、global strict、hyperdescent等は未証明のまま。

**exact-source：** source `84b6480c102bd4a27d597eb5c38602b9fac25594`、test-merge `b0ca6b57911c7032a807756eb0434f44e6d687ce`、**共通Git tree `5e949087e6a3dd85a623b1d5e3285622f2089d4e`**、[CI #41264909942](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41264909942) **Strict Lean 3805/3805 SUCCESS・Governance terminal SUCCESS**、変更Lean1ファイル10宣言、標準3公理以内、sorryAx0、warning/error0/0、定理squash `70ca44e911b59ef0a51f27318a3e5b7d2f099c09`。初回CIの`Function.Surjective`由来lambdaラッパーと`rw`照合不一致は、`change`で依存型等式を正規化して全文再検証。固定Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft・OPEN・未マージ維持、strict空中心・独立Kuu一presentation・Gray非再導入。

**次GK4BK：** これらのFull・対象全射・厳密観測kernelを使い、元構造商から任意の標的圏へのAH-kernel-compatible関手が**実到達AH圏を通って因子化するための普遍性**を、元型付き境界・合成・単位・必要な一意性まで形式化する。高次hyperdescentとは区別する。旧GK4BI欄はその時点の履歴として残す。

## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BG

**真正第二kernel K_AIのAH固定ファイバーは、同じ型付きHomと同じAH値で実際に到達する旧AE観測値の像と全単射になることをLean4で証明 — [定理PR #2856](https://github.com/itakura-hidetoshi/KuuOS/pull/2856) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BGResidualAEFiber.lean)・[証明／Lean宇宙修正記録](docs/formal/GK4BG-exact-ah-fiber-residual-ae.md)。GK4BAの一点決定性からAH一致が元GK4AF行列一致を強制するため、同じ真の型付きHomで **`M_AH(u)=M_AH(v)` の下、`u=v ↔ O_AE(u)=O_AE(v)`** を証明。さらに固定AH値の元K_AIファイバーと**実到達**残余AE像の双方向全単射、非自明ファイバーと異なる実到達AE値が存在することの必要十分条件を証明。GK4ACの真正F54物理rank制約を用い、後退回転数0の自己Homではgradeが`true`で、AH一致時の残余差は旧GK4AD順序付き履歴に限られると形式化。計12宣言。**同じAHの相異なるK_AI類の存在／不存在はなお未証明**であり、観測から元Type値3-cellを生成しない。

**exact-source：** 最終source `1375b66b29c2dc13d92abb42305c610abf17f5cf`、test-merge `db1160da9054d99c702944694b693f7eea4e3496`、Git tree `139e402b8f21d16ab3da577379eb840bf6246e26` 完全一致。[CI #41258432374](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41258432374) **Strict Lean 3801/3801・Governance terminal SUCCESS**、12宣言すべて標準3公理以内、sorryAx0。初回の実到達固定ファイバーに小さい`Type`を指定した宇宙レベル不一致を、元F54 Homの宇宙を保持する`Type (max (max uD uE) (max vD vE))`へ修正して全文再検証。定理squash `b7c172c39a3e55ee18dfb7215b6c4237fff00c5d`。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、root107・strict空中心・独立Kuu一presentation、Gray非再導入、保護#1558 Draft／OPEN／未マージ維持。

**限界：** 真のAH非忠実性もAH忠実性も断言しない。元Q圏公理・元Type値完全同値・固定単一旧類ファイバー無限性・算術slice全域到達・真正14D無条件Countable・19D filler・global strict・hyperdescentも未証明。以前の研究欄は履歴として残す。


## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BF

**元F54完全依存型経路の真正K_AI各Homの実到達AH行列を合成・単位付きMathlib Categoryとし、各Hom全射・整数行列値への忠実包含・任意整数評価関手の因子化をLean4で証明 — [定理PR #2854](https://github.com/itakura-hidetoshi/KuuOS/pull/2854) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BFAttainedAHCategory.lean)・[exact-source証明記録](docs/formal/GK4BF-attained-ah-category-evaluation-factor.md)。既存GK4BEの実在証拠付き`NativeGK4BEAttainedAH`を型付きHomに採用し、真正K_AI合成を使った閉性と整数行列積の結合律・単位律を証明。**`K_AI → AH_attained → Mat₂(ℤ)`** の前段は各Hom全射、後段は各Hom単射、合成は既存旧AH観測関手と完全に一致。前段のfaithfulnessは仮定しないで、その必要十分条件を障害判定として形式化。すべての整数`t`でGK4BEの一意評価を真のFunctorにし、K_AI評価関手の因子化、`t=4`での包含への一致を全関手等式として**16宣言**で形式化。元Qの未証明圏公理・Type値3-cell生成・任意行列到達は主張しない。

**exact-source：** source `a52a701341cc369b2211ea8111c83441b156b9ac`、test-merge `5875ff8652c124de7964568cdc79f05462335070`、両Git tree `78971c18d8a155fc4498fa402945826fec1d3565` 完全一致。[CI #41256478785](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41256478785) **Strict Lean 3800/3800・Governance terminal SUCCESS**、標準3公理以内・sorryAx0。定理squash `8c41653a55c28439bd4b1ec0ade255d34d41ef20`。固定Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft/OPEN未マージ維持。

**未証明：** 前段のfaithfulnessや元K_AI・元Type値歴史的完全同値、旧類固定単一ファイバー無限性、算術slice全域到達、元Q結合律・左右単位、真正14D無条件Countable、19D filler、global strict、hyperdescent。以前の研究欄は履歴として保持する。


## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BE

**真正K_AI上の全多項式観測・旧AH一点評価`t=4`・全整数評価の共通核が一致し、到達AH像上で任意整数評価が一意に因子化 — [定理PR #2851](https://github.com/itakura-hidetoshi/KuuOS/pull/2851) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BEEvaluationKernelFactor.lean)・[証明／修正記録](docs/formal/GK4BE-evaluation-kernel-attained-ah-factorization.md)。GK4BA一点決定性、GK4BB `Quotient.lift`、GK4BC関手性、GK4BD整数評価関手を結合して、同じ真正型付きHomの`u,v∈K_AI`に対する **`P̄(u)=P̄(v) ⇔ ev₄(P̄u)=ev₄(P̄v) ⇔ ∀t∈ℤ, evₜ(P̄u)=evₜ(P̄v)`** をLean4証明。各Homで真に到達する元AH行列の像のみを構成し、任意整数評価の代表元独立な写像とその一意性、`t=4`での恒等回収、元Q・独立Sでの別個の一点決定性を**16宣言**で形式化。これはK_AI類自体の同一性、faithfulnessや全整数行列への到達を意味しない。

**exact-source：** source `1721e3c02a93a011f63f932af589cce89aac01f6`、test-merge `bbe7b3b17c05e9077f465543c15f737d6a332db7`、Git tree `41b55bcc9f437ce987815f61dd269b8d90cab8d8` 完全一致、[CI #41255562142](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41255562142) **Strict Lean 3799/3799・Governance terminal SUCCESS**、全16宣言は標準3公理以内・sorryAx0。初回CIのFunctor核比較`simp`不一致は、既存`nativeGK4BDKAIIntegerEvaluation_four_map`のHom等式を明示する`calc`へ修正して解消。定理squash `9249514545fcaa542538f82cdfc1f6e7b740112e`。Lean v4.30.0-rc2／pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation・Gray非再導入、保護PR #1558 Draft/OPEN/未マージ維持。

**authority・限界：** 旧AHによる観測核一致は元Type値経路の同一性／3-cell生成／元Qの未証明圏公理を含まない。固定単一旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentも未証明。以前のGK4BDまでの研究欄は履歴として残す。


## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BD

**真正K_AIの全多項式行列関手から任意整数tの評価関手を構成し、t=4で元AH観測関手と厳密一致することをLean4で証明 — [定理PR #2849](https://github.com/itakura-hidetoshi/KuuOS/pull/2849) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BDIntegerEvaluationFunctor.lean)・[exact-source証明記録](docs/formal/GK4BD-integer-evaluation-functor-ah-triangle.md)。多項式行列Mat₂(ℤ[X])および整数行列Mat₂(ℤ)の各非可換行列積をHom合成とする一対象圏を区別して、全整数tの`eval_t`を真のMathlib Functorとして構成。既存GK4BCのK_AI→多項式値Functorに合成し、**`(P̄ ⋙ eval_4) = oldAHFunctor`** を真のFunctor等式としてLean証明。元構造商S→K_AIとの全整数t可換性、元SのAH t=4一致も証明。新規10宣言。元Q自身の未証明圏公理・元Type値3-cell・faithfulnessは主張しない。

**exact-source：** 最終source `e1ac6051a020b352aea28bd10f91071d7d64cb64`、test-merge `c92e96270309238ef05f4679b010c5bb8ce2fded`、Git tree `50948f48c413b0c1bed56229ba40ab8e8acbe05c` 完全一致。[CI #41254632718](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41254632718) **Strict Lean 3798/3798・Governance terminal SUCCESS**。10宣言公理依存は標準3以内、sorryAx0。初回のFunctor.extによるeqToHom輸送のelaboration mismatchは、`eqToHom_refl` と圏の単位律を用いて修正した。定理squash `1ebc72839b29e50e649484766cdf8c7741df4a1e`。Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ維持。

**限界：** 全整数評価の関手性は実際の元F54経路が任意の行列へ到達することを意味せず、K_AI→多項式Functorのfaithfulness、元Qの圏公理、元Type値完全同値、固定単一旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは未証明。以前のGK4BC以降の推奨予定は履歴として維持する。


## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BC

**既存K_AI上の真正全多項式行列が合成・単位を保存し、MathlibのFunctorとなることをLean4で証明 — [定理PR #2847](https://github.com/itakura-hidetoshi/KuuOS/pull/2847) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BCPolynomialFunctorAI.lean)・[厳密な証明記録](docs/formal/GK4BC-polynomial-functoriality-ai.md)。GK4BBの既存二次kernel `K_AI` への `Quotient.lift` で定義した `P̄` について、**`P̄(u∘v)=P̄(u)·P̄(v)`、`P̄(id)=I₂`** を、真正元P92B代表元の非可換行列観測保存から証明。さらに任意整数`t`の評価積保存、`t=4`で元AH積回収、一対象の整数多項式行列値圏、真のK_AI→多項式値Mathlib関手、独立構造商Sとの可換図式まで9宣言で形式化。元Qの未証明圏公理・Type値3-cellを仮定せず、関手のfaithfulnessも主張しない。

**exact-source：** source `f93b85e7a8759e6f32760ab975f6728483e1df8e`、test-merge `d2d061ef95a5c5bb68111af7cf2708d54d3ea639`、両Git tree `7b944c445e213662db7355e68989d29d774dca93` 完全一致、[CI #41253944040](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41253944040) **Strict Lean 3797/3797・Governance SUCCESS**、公理依存標準3以内・sorryAx0。squash正本 `b9ae3569a167c89b9b04d83ab53aceaf58412050`。Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuu一presentation・Gray非再導入・保護PR #1558 Draft/OPEN/未マージ維持。

**限界：** 多項式Functorのfaithfulness、元Qの結合律/左右単位、元Type値歴史的同値、固定単一旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは未証明。先行GK4BB欄は履歴として残す。


## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BB

**既存二次kernel `K_AI`への真正F54多項式行列全族の降下をLean4で証明 — [定理PR #2845](https://github.com/itakura-hidetoshi/KuuOS/pull/2845) MERGED。** [新Lean定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BBPolynomialDescentAI.lean)・[exact-source証明記録](docs/formal/GK4BB-existing-KAI-polynomial-descent.md)。GK4BAの**`P_u(4)=P_v(4) ⇔ P_u(X)=P_v(X)`**が示す一点決定性と、既存`K_AI`が`M_AH=P(4)`を実観測成分として保持する事実から、元P92B存在商Qの多項式`P_r(X)∈Mat₂(ℤ[X])`が既存`NativeGK4SKernelClasses (nativeGK4AIP92Family …)`へ降下することを、明示的`Quotient.lift`で証明。元Q代表元での元値一致、`X=4`評価でのAH厳密回収、多項式値一致`↔`AH一致、降下の一意性、別の独立構造商SからK_AIへの既存比較との可換性を**6宣言**で形式化した。これは`K_AI`クラス自体のAH一意性や元Type値3-cell生成を意味しない。

**exact-source：** HEAD`9617a45e331a52abd22ad2586be5216bc3360b7d`、test-merge`67840fc1e5404a453d360c3cdfd22e96a66d67e9`、両Git tree`579a1630f3226a98bf2d4ec3a0de979f6dc426f1`一致、[CI #41253344455](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41253344455) **Strict Lean 3796/3796・Governance SUCCESS**、標準3公理以内・sorryAx0・変更Lean error/warning0/0。squash正本SHA`2db3201782457854f7b5fdaeeeba4b086a273228`。固定Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuu一presentation・Gray非再導入、保護PR #1558 Draft/OPEN/未マージ維持。

**数学的な限界：** `K_AI`の元類がAHだけで一意になること、元Qの未証明結合律/左右単位、元Type値歴史的完全同値、単一固定旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは引き続き未証明。先行GK4BA欄の「次GK4BB（未証明）」は過去のスナップショットであり、この最新欄が現在の正本。

## 最新の研究追補 — 2026-11-01 JST / F112-P94D3GK4BA

**真正元F54依存型経路の全多項式行列は旧AH一点評価 `t=4` だけで決定する — [定理PR #2840](https://github.com/itakura-hidetoshi/KuuOS/pull/2840)・[#2838](https://github.com/itakura-hidetoshi/KuuOS/pull/2838)・[canonical-main統合 #2843](https://github.com/itakura-hidetoshi/KuuOS/pull/2843) 全MERGED。** [最終Lean定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAOnePointDeterminacy.lean)・[全文証明/CI記録](docs/formal/GK4BA-original-t4-one-point-polynomial-determinacy.md)。

GK4AY/GK4AZの実Leanで証明したSanov型 `ℤ*ℤ ↪ Perm(ℤ²)` を、元F54の全依存型 `RotationEdge`・`RotationChain`・`DepthRotationRoute` の元構成子へ輸送した。元多項式行列 `P_r(X)∈Mat₂(ℤ[X])` と本物の自由積語の多項式作用／整数`t=4`作用が可換であり、**`P_u(4)=P_v(4) ⇔ P_u(X)=P_v(X)`** を任意の同じ元Type値型付き始点・終点の経路についてLean4形式化。元P92B存在商Qと別の独立構造商Sでも、それぞれ同じ一点決定性を証明。旧AF/AH二評価一致なのに多項式が異なるという以前の研究候補は**不存在**。ただし、これは元Type値経路の同一性や新たな3-cell証拠ではない。

**exact-source CI:** #2840 source `b0c480e3da157a04cb8af9eefeed8d7fac788fac`、[CI #41250464410](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41250464410) **3793/3793 SUCCESS**、squash `435e6282e492724df7d851ff1bf3a40d4a4f1621`。#2838は最初作業ブランチへマージされたため、同一証明のmain統合#2843 source `5e1b355e5a417c554ba607b1b819aa66778cabde`、[CI #41252864048](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41252864048) **3795/3795 SUCCESS**、squash=canonical main `c4e20c3f2676dc8033010cfa024678b345649a38` を独立確認。2件ともGovernance SUCCESS・変更Lean warning/error0/0、標準3公理以内・sorryAx0、source/test-merge Git tree一致。公開root107、Lean/mathlib固定、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft/OPEN/未マージを維持。

**次GK4BB（未Lean証明）：** 既存`K_AI`のkernel観測には`M_AH=P(4)`が含まれるため、GK4BAから全多項式族が既存`K_AI`へ代表元独立に降下することが従う。明示的`Quotient.lift`と元Q/Sとの可換性、一意性を形式化する。元Q自身の未証明圏公理やType値3-cellを作らない。

## 最新の研究追補 — 2026-10-31 JST / F112-P94D3GK4AZ

**Sanov型整数せん断変換の真正ping-pong自由積単射 — [GK4AZ定理PR #2836](https://github.com/itakura-hidetoshi/KuuOS/pull/2836) MERGED。** [新Lean証明](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AZShearFreeProduct.lean)・[全証明記録](docs/formal/GK4AZ-shear-free-product-pingpong-injectivity.md)。元F54の真正多項式生成子`C=[[1,1],[0,1]]`、`F=C⁻¹`、`R(4)=[[1,0],[4,1]]`を整数座標`(u,v)↦(2u,v)`で移し、`U_n(x,y)=(x+2ny,y)`、`L_n(x,y)=(x,y+2nx)`を得る。[GK4AY PR #2835](https://github.com/itakura-hidetoshi/KuuOS/pull/2835) MERGEDで、二つの互いに素な非空錐`H={|x|>|y|}`・`V={|y|>|x|}`に対し、**全非零整数n（負も含む）で`U_n(V)⊆H`、`L_n(H)⊆V`**、可逆性、加法合成をLean証明。[GK4AY詳細](docs/formal/GK4AY-integral-shear-pingpong.md)。

GK4AZでは二つの`Multiplicative ℤ →* Equiv.Perm(ℤ×ℤ)`を実構成し、pairwise cone条件・巡回群の3元以上条件を証明。**固定mathlibの`Monoid.CoprodI.lift_injective_of_ping_pong`を適用して、`ℤ*ℤ ↪ Perm(ℤ²)`をLean4で証明した。Sanov自由性を新公理として仮定していない。** 初回CIの`Equiv.ext`／`Function`・`Pointwise`・`Cardinal`のスコープと逆作用簡約の誤りは変更Lean全文を確認して修正。GK4AY exact-source `2a74c109ade0fa898c334b5f4a3e58a0e80ae3fb`、squash `2218521799c635e627300b0434d9e57d40352d94`、[CI #41211527398](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41211527398) **3788/3788 SUCCESS**。GK4AZ final exact-source `1d77015d43f5e6a37ea17a17f7cf811b3ace5a03`、squash `16585324b45863be3a4cc3faabbf59bb9be7cda8`、[CI #41212234574](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41212234574) **3789/3789 SUCCESS**。両PR Governance SUCCESS、標準3公理以内・sorryAx0・変更Lean warning/error0/0、公開root107・固定pin・#1558 Draft/OPEN/未マージ維持。

**次はGK4BA（未証明）：** 上記`ℤ*ℤ`自由性と真正F54全依存型経路`P_r(X)`とのsource-word評価可換性をLean証明し、**`P_u(4)=P_v(4)⇒P_u(X)=P_v(X)`**を全真正経路へ移す。現時点では自由積の実Lean定理と、元F54の多項式全族一点決定性は異なる命題。元Type値3-cell・Q圏公理・既存K_AIへの全族降下・単一旧類ファイバー無限性は未証明。

## 最新の研究追補 — 2026-10-31 JST / F112-P94D3GK4AX

**真正F54多項式行列の有限評価決定性と旧AF/AH二評価の次数obstruction — [定理PR #2833](https://github.com/itakura-hidetoshi/KuuOS/pull/2833) MERGED。** [Lean証明](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AXFiniteEvaluationDeterminacy.lean)・[証明記録](docs/formal/GK4AX-finite-evaluation-polynomial-determinacy.md)。GK4AV/GK4AWの元Type値実経路の多項式行列 `P_r(X)∈Mat₂(ℤ[X])` と本物の `β(r)=backwardCount` の次数上界から、固定mathlib `Polynomial.eq_of_natDegree_lt_card_of_eval_eq` により、**相異なるN個の整数評価が一致し `N>max(β(u),β(v))` なら `P_u(X)=P_v(X)`** を証明。真正F54全依存型経路、元P92B存在商Q、独立構造商Sに**別々に形式化**。特に `β(u),β(v)≤1` なら旧AF=`P(1)`／AH=`P(4)` の二行列一致から多項式全体が一致する。二評価一致と多項式相異の**仮定が成立するなら `max β≥2` が必要**であることもLean証明したが、そのような反例の存在は主張しない。

**exact-source証拠：** 最終source HEAD `0dcf281ee6433674f30a7f56be337061eecf6a72`、test-merge `f4033c6fc438b5f54f29b56d79bbec0d750a3ce1`、両Git tree `2f7a50aaa539b01b717df841e6580289f1847f25` 完全一致、定理squash `222a7d003312ac1274211292d301897e62f2032e`。[CI #41208604553](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41208604553) **Strict Lean 3785/3785・Governance SUCCESS**、12宣言公理依存標準3以内、sorryAx0、変更Lean警告/エラー0/0。固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation・Gray非導入、保護PR #1558 Draft/OPEN/未マージを維持。

**次段階GK4AY（未形式化）：** 旧AHの**一点評価 `P_u(4)=P_v(4)` だけで任意の元F54多項式行列一致を結論できるか**を、Sanov自由部分群／pin済mathlibのping-pong補題を通して検証する。標準的群論では `C=[[1,1],[0,1]]` と `R(4)=[[1,0],[4,1]]` を実対角共役すればSanov自由生成子となり、`F=C⁻¹` なので、この単射性が有力。**ただし元F54経路→自由群語のLean輸送とSanov忠実性は未証明**。二評価衝突の存在を仮定したり、旧K_AIへの多項式全族降下・元Qの未証明圏公理・Type値3-cellを補ったりしない。

## 最新の研究追補 — 2026-10-31 JST / F112-P94D3GK4AW

**真正元F54整数多項式行列の高次係数消失と、物理backtrackでの次数上界達成をLean4で証明 — [定理PR #2831](https://github.com/itakura-hidetoshi/KuuOS/pull/2831) MERGED。** [新規GK4AW Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AWPolynomialCoeffSharp.lean)・[詳細検証記録](docs/formal/GK4AW-polynomial-coefficients-backtrack-sharp.md)。GK4AVで証明した元backwardCount β(r) による各成分の次数上界から、固定mathlib Polynomial.natDegree_le_iff_coeff_eq_zero を使い、**すべての n>β(r) について、多項式行列 P_r(X) の全4成分の X^n 係数が0**となることを証明。実際の元F54依存型経路、元P92B存在商Q、独立構造商Sを別々に保持した。

真正LocalRotationに由来する元F54二辺の実backtrack B では **P_B(X)=[[1-X,-1],[X,1]]、β(B)=1、natDegree(P_B,21)=1**。したがって従来の次数上界が少なくとも一つの真正経路で鋭い。実C60北側で無条件に証明。**一般の全経路に対する等号は主張しない。** 元Type値3-cellを観測一致から生成しない。

**定理正本と検証：** 最終source HEAD f4c4de036bfd6d52814e313d5699c5a8fad4b9ae、実test-merge 64dff6e436cba4484412b6d35de1b5cc7aafa6fb、共通Git tree 70db370eb1a46c9db32ddf9a4e98593fdf73db28、定理squash / 統合直後main eb9b5235be076e8a1eb6e12bb501672b3a2a9b0d。[CI #41207446279](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41207446279) は **Strict Lean 3784/3784、Governance 5/5 terminal SUCCESS**。新規10宣言の公理依存は標準3公理以内、sorryAx0、変更Lean warning/error0/0。公開root107・固定Lean/mathlib・保護PR #1558 Draft/OPEN/未マージ維持。

**次段階（未証明）：** 二点評価 (t=1,4) が一致して多項式全体のみ異なる元F54経路の存在は未証明。特に t=4 の C と R(4) はSanov自由生成対の対角共役であるため、**逆にこの三生成子ではそのような二点反例が存在しない可能性**を検査する。Sanov型の単射を元F54・Leanへ形式化するまで断定しない。既存K_AI全族降下、固定ファイバー無限性、算術slice全域到達、元Q圏公理、14D/19D/global strict/hyperdescentは未証明。

_以下のGK4AV「最新」見出しは当該PR時点の履歴スナップショット。現在のfrontierは上記GK4AW。_


## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AV

**元F54の真正整数多項式2×2行列不変量を構成し、元backwardCountによる全4成分の次数上界をLean4で証明 — [定理PR #2829](https://github.com/itakura-hidetoshi/KuuOS/pull/2829) MERGED。** [型付きF54多項式不変量・全比較保存Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AVPolynomialInvariant.lean)と[評価・行列式・次数証明Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AVDegreeEvaluation.lean)をappend-only新規2Leanファイル・65公理依存表示宣言で実装。元F54の真正cast C=[[1,1],[0,1]]、forward F=[[1,-1],[0,1]]、backward R(X)=[[1,0],[X,1]]を**ℤ[X]係数の非可換2×2行列積**に評価し、真正RotationEdge・中間木RotationChain・元DepthRotationRoute全5構成子、元F55 9/P92B 9/独立seam14/拡張3比較の全**Type値証拠**を保存。元Qと独立Sに**別々に**降下、S合成と単位も保存。元Qの未証明圏公理は使わない。

**多項式の厳密な結論：** 任意の真正型付きr、さらに元Q・独立Sで、**P_r(t)=M_GK4AU(r,t)（全整数t）、P_r(1)=M_AF(r)、P_r(4)=M_AH(r)、det P_r(X)=1∈ℤ[X]**。旧GK4ADの真正backwardCount β(r)に対し、**全4成分のPolynomial.natDegree(P_r,ij)≤β(r)** を固定mathlibのnatDegree加法・乗法上界で帰納的に証明。これは次数の上界であってすべての経路で等号を主張しない。多項式族が既存K_AIに降下するとは仮定せず、GK4ATまでの固定旧q算術sliceと法48／法12制約・GK4AUの合同必要十分条件を保持する。

**GK4AV exact-source：** source HEAD 66d2c7cd4975d32b481a90dde160716ffed00cfa、実CI checkout cea32d3ff12550ff0847b6283f07ae0c2271043f、定理squash／統合直後main 5fa543a03d39687426844efe117e2473a2b1e939、三者同Git tree f2304229aa5bdafa3b78ef345b1c0975b72b7de7。[CI #41206335465](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41206335465) **Strict Lean3783/3783 SUCCESS、Governance5/5 SUCCESS、65宣言標準3公理以内、sorryAx0・変更Lean warning/error0/0**。[GK4AV証明・Polynomialでのdefinitional equality修正・CI記録](docs/formal/GK4AV-polynomial-matrix-degree-backwardcount.md)。Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft・OPEN・未マージを維持。

**次はGK4AW（未形式化候補）：** 元backwardCountより高い次数係数の消失と真正backtrackによる上界の鋭さ、旧t=1,4評価だけでは区別できない多項式履歴の存在性を別々に研究する。固定旧q無限ファイバー、K_AIへの多項式全族降下、算術全域到達、元Q自身の圏公理、14D無条件Countable、19D filler、global strict・hyperdescent等は未証明。

> 以下のGK4AU以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AV。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AU

**真正F54の整数パラメータ行列族を構成し、既存AF・AHの厳密な回収と合同条件の必要十分性をLean4証明 — [定理PR #2827](https://github.com/itakura-hidetoshi/KuuOS/pull/2827) MERGED。** 元cast C=[[1,1],[0,1]]、forward F=[[1,-1],[0,1]]、backward R(t)=[[1,0],[t,1]]を同じ真正F54のType値経路上で評価する。値はInt→整数2×2行列であり、既存AHの行列積を点ごとに再利用。元F55の9・P92Bの9・独立seamの14・拡張比較の3構成子に対する**族全体の等式保存**を証明し、元Qと独立Sへ別々に降下、S合成・単位も保存した。

**全経路・元Q・独立Sで M_r(1)=M_AF(r)、M_r(4)=M_AH(r)、任意整数tでdet M_r(t)=1。** 既存二観測を置換せず、一つの族の二評価として回収する。任意整数法kでs≡t(mod k)なら全真正経路でM_r(s)≡M_r(t)(mod k)が全成分に成立する。

**真正局所回転rotを持つ同じ自己Homでは逆も成立： (∀r, M_r(s)≡M_r(t) mod k) ⇔ s≡t(mod k) ⇔ k∣(t−s)。** 本物のforward/backward往復BのM_B(t)=[[1−t,−1],[t,1]]がパラメータを検出する。元Q・独立Sでも別々に必要十分性を証明し、真正C60 northで具体化した。従ってAF/AH間で全経路に普遍的に使える法は**k∣3**に限る。これは同じ経路に対する異なる観測の比較であり、GK4ATの固定旧q内二経路の法48／法12一致とは別の量化である。パラメータからS上の観測写像への単射性も証明したが、一つの観測の忠実性は主張しない。

**GK4AU exact-source：** source `4c96aa69f2e081d1e299a1ce5019aad31ac58b4a`、実CI checkout `1300b74e21d2c1b67617449df7810d568e975694`、定理squash `cf4679813e7f767af7d44bbd273de18661e3c2cf`、共通tree `5719f12b9bb2718a1dc9cfce40bb65d63578a7e2`。[CI #41204182959](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41204182959) **Strict Lean3781/3781・Governance5/5 SUCCESS、新規2Lean・55宣言標準3公理以内、sorryAx0、変更Lean warning/error0/0**。[詳細証明・文脈を保持する署名修正・CI記録](docs/formal/GK4AU-parametric-family-sharp-modulus.md)。固定Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

**境界：族全体の既存K_AIへの降下は未証明。** t=1,4の二点での一致から全族の一致を生成しない。GK4ATまでの厳格sliceを維持し、固定単一旧q無限ファイバー・算術slice全域到達・元Q圏公理・歴史的完全型付き同値・14D無条件Countable・19D filler・global strict・hyperdescentは未証明のまま。

**次はGK4AV（候補・未形式化）。** 整数係数多項式行列への真正族の持ち上げ、評価との整合、次数と元backwardCountの関係を検討する。

> 以下のGK4AT以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AU。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AT

**真正F54の第一行列AFと第二行列AHが全成分で法3に一致することをLean4証明 — [定理PR #2825](https://github.com/itakura-hidetoshi/KuuOS/pull/2825) MERGED。** C・Fは同一、後退生成子の左下だけが1と4で異なることから、固定mathlibのInt.ModEqを用いて真正RotationEdge・RotationChain・DepthRotationRoute全5構成子上の整合性を証明。元P92B Qと独立構造Sへ別々に降下し、真正K_AIと任意固定旧K_AG類qに適用した。旧qが既に保持するAF行列P(q)により **M_AH≡P(q)(mod3)** が全成分で強制される。

**今回は非冗長な新obstruction：AttainedMatrix(q) ⊆ Γ_AT(q) ⊊ Γ_AS(q)=Γ_AR(q) ⊊ Γ_AQ(q)。** Γ_ATは従前ASの全条件と第一行列mod3の連言。既存忘却全射から取った実到達Mを算術的にM·U(16)へ移すとAS条件は保つが、mod3一致を保てば第一列がmod3で零となりdet=1に矛盾する。従って任意旧qで真の包含。**移動後の行列を元F54経路として実現するとは主張しない。** 真正Fiberから新sliceへの埋込みも証明した。

**同一旧q内の合同精度：左上・左下・右下は法48、右上は法12で一致。** 既存の法16（右上のみ法4）と新しい法3を、固定mathlibの互いに素な法の合同定理で結合した。全成分が法48になるという主張ではない。

**GK4AT exact-source：** source `7b79d067a9b8aa8174df7357860de839d3ba6b29`、実CI checkout `91aabe754c4660cbddf9fd77c33f69459dc4bbcb`、定理squash `895f6520a4ea2afc06d75f626ff0b721c73d89de`、三者共通tree `8847ec9b69cbeb5e416919c2cb5daabcb18494e2`。[CI #41201974238](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41201974238) **Strict Lean3779/3779・Governance5/5 SUCCESS、新規2Lean・28宣言標準3公理以内、sorryAx0、変更Lean warning/error0/0**。[詳細証明と修正・CI記録](docs/formal/GK4AT-cross-matrix-mod3-strict-slices-mod48.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107維持、strict空中心・独立Kuu一presentation・Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

**次はGK4AU（未形式化候補）。** 第一・第二行列の共通整数パラメータ付き観測を、真正比較証拠の保存から調べる。単一固定旧qの無限ファイバー、算術slice全域到達、元Q圏公理、歴史的完全型付き同値、14D無条件Countable、19D filler、global strict、hyperdescentは未証明。

> 以下のGK4AS以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AT。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AS

**真正F54第二整数行列の右下成分mod16が既存GK4AO〜GK4AR条件から強制されることをLean4で形式化 — [定理PR #2823](https://github.com/itakura-hidetoshi/KuuOS/pull/2823) MERGED。** [新規GK4AS証明Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ASForcedLowerDiagonal.lean) 1ファイル・18宣言。旧GK4ADのcharge χ、backwardCount β、orderedMoment m、三角数T(β)=β(β−1)/2、ρ=χ+β、s=m+T(β)に対して、真正GK4AH行列M=[[a,b],[c,d]]は **d≡1+4(ρβ−s) (mod16)** を満たす。行列式ad−bc=1、GK4ARの左上a≡1+4s(mod16)、GK4APの右上b≡ρ(mod4)、GK4AQの左下c≡4β(mod16)、GK4AOのd≡1(mod4)の**既存整数証人**を結合し、新しい右下整数証人を明示構成した。さらに **tr(M)=a+d≡2+4ρβ(mod16)** を証明。orderedMomentは対角和で相殺される。

**重要：これは独立の新obstructionではない。** 任意の整数2×2行列に対してGK4AS全条件とGK4AR全条件は必要十分に同値であり、任意固定旧qの算術sliceは **Γ_AS(q)=Γ_AR(q)**。従前の厳格包含 **AttainedMatrix(q) ⊆ Γ_AS(q)=Γ_AR(q) ⊊ Γ_AQ(q)** は維持するが、AS⊊ARという誤った包含は主張しない。元F54真正forward/backward RotationEdge・RotationChain・元DepthRotationRoute全5構成子、実P92B Q、独立S、真正K_AIと全旧qファイバーへの成立をLean4で証明済み。元Type値3-cellを観測値一致から生成せず、算術slice全域到達や固定無限ファイバーも仮定しない。

**GK4AS exact-source正本：** source HEAD b702e5b586c86751693d40fd0508c767b77bb735、定理squash／統合直後main HEAD 6fe4784a704e2da1e20a6c3204509a2357d028a9、両者同Git tree ecb50d22ea0d68aa7146ffe768fe9c5e0314328d。[CI #41199914582](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41199914582) **Strict Lean 3777/3777 SUCCESS・Governance 5/5 SUCCESS・18宣言公理標準3以内・sorryAx0・変更Lean warning/error0/0**。[GK4AS詳細証明・exact-source CI記録](docs/formal/GK4AS-forced-lower-right-mod16-trace-and-slice-equivalence.md)。Lean v4.30.0-rc2・mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuu一presentation・Gray非再導入、保護PR #1558はDraft／OPEN／未マージ。

**次候補GK4AT（未形式化）：** 法32以上の高精度合同または別の真正Type値観測による**非冗長な**obstructionを調査する。固定一旧qの無限ファイバー・元Q圏公理・歴史的完全型付き同値・14D無条件Countable・19D filler・global strict・hyperdescentは未証明。GK4AN有限下界、GK4AL全ファイバーCountable、GK4AM正k有限族非網羅結果を保持。

> 以下のGK4AR以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AS。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AR

**真正F54の非可換orderedMomentが第二整数行列の左上成分の法16剰余を決定することをLean4で証明 — [定理PR #2821](https://github.com/itakura-hidetoshi/KuuOS/pull/2821) MERGED。** [元F54全構成子の三角数・orderedMoment対角合同証明Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ARDiagonalMoment.lean)・[任意旧qのGK4AQ内さらに厳格な算術slice Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ARStrictDiagonalSlice.lean)をappend-only新規2Leanファイル・33宣言で形式化。旧GK4ADの `v=((charge,beta),moment)`、元GK4AH整数行列`M=[[a,b],[c,d]]`について、**`a≡1+4*(moment+binomial(beta,2))(mod16)`**を元F54真正forward/backward RotationEdge、中間F45木RotationChain、二Nat cast／trans／左右contextの全5構成子上で証明。三角数`T(0)=0, T(n+1)=T(n)+n`の加法コサイクル`T(u+v)=T(u)+T(v)+uv`と`2T(n)=n(n-1)`をLeanで証明し、旧Heisenberg履歴と本当のGK4AH非可換行列積の交差項が一致することを確認。元F55/P92Bの実Type値比較証拠を保持して元Q・独立Sへ別々に降下させ、真正K_AIと任意の固定旧K_AG類`q`の`Fiber(q)`へ伝播した。**GK4AO行列式1／Γ₁(4)、GK4AP右上mod4、GK4AQ左下mod16はすべて維持。**

**固定qの算術障害をさらに厳格化：** `Γ_AR(q)`をGK4AQまでの全条件に`M.11≡1+4*(moment(q)+T(beta(q)))(mod16)`を加えた集合とすると、**`AttainedMatrix(q) ⊆ Γ_AR(q) ⊊ Γ_AQ(q)`**を任意のqで証明。厳格性は`rho=charge(q)+beta(q)`として、どちらも前段AQ算術条件を満たす`Base=[[1+4rho*beta,rho],[4beta,1]]`と`Twist=Base*[[5,4],[16,13]]`を実際に整数行列として構成し、両左上成分の差`4+16rho(beta+1)`が法16で4となることから証明。少なくとも一方は新sliceに属さず、真正Fiber(q)にも到達不能。**これらの算術証人が元F54経路として実現するとは主張しない。** 真正ファイバーは実際に到達した新slice部分集合にのみEquiv。固定単一ファイバーの無限性とslice全域到達は未証明。

**GK4AR exact-source正本：** source HEAD `aadaffffc728e623bd8dcd21e91ffb8be07af6a4`、CI test-merge checkout `59debf9dbe2c4e19e3e0b1ee4afa6f03a01dcbb8`、定理squash／統合直後main `61e8f7483eaa6cd72df7fd03b37963b22f27e645`、三者共通Git tree `3012191846e2c2332d4674c69287b89c065ac988`。[CI #41198771601](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41198771601) **Strict Lean 3776/3776 SUCCESS・Governance 5/5 SUCCESS・33宣言標準3公理以内・sorryAx0・変更Lean warning/error0/0**。[GK4AR詳細証明とexact-source CI記録](docs/formal/GK4AR-ordered-moment-diagonal-mod16-strict-fiber-slices.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

**次候補GK4AS（未証明）：** 行列式1およびGK4ARまでの確定合同式から右下成分の法16剰余も導けるか検討し、同時に一つの固定旧qの無限ファイバー可能性を独立に研究する。GK4ANの`Fin(2k+1)↪Fiber(q_k)`、GK4AL全ファイバー可算性、GK4AMの`∀k>0,¬FamilyCovers(k)`は維持。元P92B Q自身の圏公理・14D無条件Countable・19D filler・global strict・hyperdescent等は未証明のまま。

> 以下のGK4AQ以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AR。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AQ

**元F54第二整数行列の左下成分が真正旧backwardCountの4倍に法16で一致することをLean4証明 — [定理PR #2819](https://github.com/itakura-hidetoshi/KuuOS/pull/2819) MERGED。** [元F54全構成子の下左mod16合同証明Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AQLowerLeftResidue.lean)・[任意旧qのGK4AP算術slice内部にあるさらに厳格な障害Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AQStrictLowerSlice.lean) をappend-only新規2Leanファイル・公理表示27宣言で形式化。真正GK4AH整数2×2行列`M=[[a,b],[c,d]]`と元GK4AD非可換Type値履歴のbackwardCount `β(r)`について、**`c≡4β(r)(mod16)`** を元forward/backward RotationEdge・実RotationChain・二Nat cast・trans・左右contextから直接帰納的に証明。元F55/P92B/構造seamの実Type値比較保存性を保持し、元P92B存在商Qと独立Sへ別々に降下、真正K_AI・全元F45依存型Hom・任意固定旧K_AG類qの忘却ファイバーへ伝播した。GK4AOの`det=1`・Γ₁(4)合同条件およびGK4APの**右上`b≡charge+β(mod4)`をすべて維持**。

**同じ旧qでの厳格な算術slice：** `ρ(q)=charge(q)+β(q)`とすれば、**`AttainedMatrix(q) ⊆ Γ₁(4)^(q,16) ⊊ Γ₁(4)^(q) ⊊ Γ₁(4)`**。ここで`Γ₁(4)^(q,16)`は従来の右上`b≡ρ(q)(mod4)`に加えて左下`c≡4β(q)(mod16)`を課す。実際、`N(q)=[[1,ρ(q)],[4(β(q)+1),1+4(β(q)+1)ρ(q)]]`は**従来GK4APのq依存sliceには属するが、今回の左下mod16制約を破るため同じ真正Fiber(q)では到達不能**とLean4証明。全qについてこの真の包含を確立。新slice内の**実到達部分集合だけ**との正確なFiber Equivも形式化。固定単一ファイバーの無限性やslice全域到達は未証明。

**GK4AQ exact-source正本：** 最終source HEAD `916381bd659e8fdf2a8b3ab951c5e1a33b8e8eb6`、CI test-merge checkout `7cd2220d26109490c52f7b7be663e8916959a194`、定理squash・マージ直後main `3297bbc78b4cc7309505bb43dacf800121493967`、共通Git tree `6a561b27089c7f06260d4e1aa63fbc4c2668b7da`。[CI #41197378209](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41197378209) **Strict Lean 3774/3774 SUCCESS、Governance 5/5 SUCCESS、新規27宣言標準3公理以内、sorryAx0、変更Lean warning/error0/0**。[GK4AQ詳細証明・初回Lean結合律正規化修正・CI receipt](docs/formal/GK4AQ-lower-left-mod16-fixed-fiber-arithmetic-slices.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107維持、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

**次のGK4AR候補（未証明）：** 旧orderedMomentと第二行列対角成分の法16の関係を検証するか、元F54真正経路を同一の旧qに無限個保持できるかを、実Type値証拠と正確な算術slice内で調べる。GK4ANの任意`Fin(2k+1)↪Fiber(q_k)`、GK4ALの全ファイバーCountable、GK4AMの`∀k>0,¬FamilyCovers(k)`を維持。元Q圏公理・歴史的完全同値・真正14D・19D filler・global strict・hyperdescentは別問題。

> 以下のGK4AP以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AQ。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AP

**真正の固定旧観測類qで、第二整数行列の右上成分の法4剰余が旧charge・backwardCountから一意に決定されることをLean4証明 — [定理PR #2817](https://github.com/itakura-hidetoshi/KuuOS/pull/2817) MERGED。** [元F54の旧GK4AD・新GK4AHの型付き結合合同式Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4APLinkedObserverResidue.lean)・[固定q算術sliceとΓ₁(4)内部の到達不能行列Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4APFixedFiberArithmeticSlice.lean)をappend-only新規2Leanで形式化。元F54真正二Nat cast・forward/backward RotationEdge、途中木RotationChain、元DepthRotationRoute全5構成子、元Q・独立S、真正K_AIと元の従属忘却Fiberまで証明した。GK4AOの`det M=1`・対角1 mod4・左下0 mod4というΓ₁(4)制約を**保持**し、さらに第二行列`M_AH=[[a,b],[c,d]]`の**`b ≡ charge_AD(r) + backwardCount_AD(r) (mod4)`**という新しい非可換観測compatibilityを証明。したがって旧`K_AG`類`q`を固定すると、`Fiber(q)`全体の実到達行列の右上成分剰余が`ρ(q)=charge(q)+backwardCount(q)`に固定される。

**Γ₁(4)内部の真正到達障害：** `Γ₁(4)^(q)={M∈Γ₁(4) | b(M)≡ρ(q)(mod4)}`とおくと、**`AttainedMatrix(q) ⊆ Γ₁(4)^(q) ⊊ Γ₁(4)`が任意のqで成立**。実際に`N(q)=[[1,ρ(q)+1],[0,1]]`は行列式1でΓ₁(4)に属するが、`Fiber(q)`には絶対に到達しないとLean証明。任意の固定q-fiberはこの算術slice内へ単射で埋め込まれ、実際に到達した部分像とのみEquiv。Γ₁(4)全域、slice全域の到達可能性、単一固定ファイバーの無限性は**未証明**。

**GK4AP exact-source正本：** 最終source HEAD `7431559538875af41f332230d7796181601bf012`、CI test-merge checkout `7b5634cc4cdeaff2e75bf551208fa4cd81eb73db`、定理squash・マージ直後canonical main `13363c70ea953a18dc0acaa5d4a138090990f576`、三者共通Git tree `8d89572c86d281eba3ac068c2b1de7d2abcaca31`。[CI #41195563521](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41195563521) **Strict Lean 3772/3772 SUCCESS、Governance 5/5 SUCCESS、新規25宣言は標準3公理以内、sorryAx0、変更Lean warning/error0/0**。[GK4AP詳細証明・Lean4記法修正とexact-source CI receipt](docs/formal/GK4AP-fixed-fiber-charge-upper-right-congruence.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心、独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

**次候補GK4AQ（未証明）：** `Γ₁(4)^(q)`内部の真の到達可能値を非可換履歴でさらに制限するか、固定された同一qファイバーで無限個の異なる元F54経路の行列像を構成できるかを独立検討する。GK4ANの`Fin(2k+1) ↪ Fiber(q_k)`、GK4ALの全ファイバー可算性、GK4AMの正数kでの`¬FamilyCovers(k)`は引き続き維持。元Q圏公理・歴史的完全型付き同値・真正14D・19D filler・global strict・hyperdescentは未証明のまま。

> 以下のGK4AO以前の「最新・次候補」は歴史時点のスナップショット。現行frontierはGK4AP。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AO

**元F54真正第二整数行列における行列式1・`Γ₁(4)`合同障害をLean4で証明 — [定理PR #2815](https://github.com/itakura-hidetoshi/KuuOS/pull/2815) MERGED。** [真正F54の行列式・合同条件Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AOIntegralCongruence.lean)と[実到達行列の制約・具体的到達不能例Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AORestrictedMatrixImage.lean)をappend-only新規2Leanで形式化。既存GK4AHの実元二Nat cast `C=[[1,1],[0,1]]`、実前後RotationEdge評価 `F=[[1,-1],[0,1]]`・`R4=[[1,0],[4,1]]` を用い、厳密な行列積の整数多項式展開から**任意の真正元F54行列 `M=[[a,b],[c,d]]` は `ad-bc=1`, `a≡d≡1(mod 4)`, `c≡0(mod 4)`** とLean4証明。元RotationEdge／中間木RotationChain／元F54経路全5構成子から、元P92B存在商Qと独立構造商Sへ別々に降下し、真正`K_AI`と任意の旧`K_AG`類`q`上の本当の`Fiber(q)`へ伝播。**GK4ALの到達第二行列値集合は`Γ₁(4)`型の合同条件を満たす部分に含まれる**。一方、行列式1の `[[1,0],[1,1]]` は左下成分が4の倍数でないので、**どの真正型付きHom／旧qファイバーでも到達不能**。これは行列式1だけでは不十分という具体的証明であり、`Γ₁(4)`の全行列が到達可能とは主張しない。実到達集合に対する制限付きの正確なfiber image EquivもLean4で構築。

**GK4AO exact-source正本：** final source HEAD `4ec9d203faf04b55052eda50ee62e9049653f846`、CI test-merge checkout `4707d513eff5c9efa345956a3b867e6cf0816336`、定理squash・定理統合直後main `d8e471901e47a34c1e4a56058789e27a3f937552`、三者共通Git tree `46662c1bba4d875a0da646980957e161fe97ddf3`。[CI #41194437867](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41194437867) **Strict Lean 3770/3770 SUCCESS・Governance 5/5 SUCCESS・新規27宣言標準3公理以内・sorryAx0・変更Lean warning/error0/0**。[GK4AO詳細証明・Lean記法修正・exact-source receipt](docs/formal/GK4AO-determinant-congruence-attained-matrix-obstructions.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ維持。

**次候補GK4AP（未証明）：** 真正旧類を固定して無限に異なる新行列を実現できるか、または新しい算術合同部分群内部のより強い到達制約を証明する。GK4ANの`Fin(2k+1)↪Fiber(q_k)`、GK4AL全ファイバーCountable、GK4AM正数kの有限族非網羅性と整合する。固定単一無限ファイバー、`Γ₁(4)`全域到達、元P92B Q圏公理、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、hyperdescentは引き続き未証明。

> 以下のGK4AN以前の「最新・次候補」は歴史スナップショット。現行frontierはGK4AO。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AN

**真正忘却ファイバーの有限下界を `k+1` から `2k+1` へ厳密に強化 — [定理PR #2813](https://github.com/itakura-hidetoshi/KuuOS/pull/2813) MERGED。** [真正F54奇数半backtrack族Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ANShiftedOddFamily.lean)・[偶奇統合Fin(2k+1)埋め込みLean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ANDoubledFiniteFibers.lean)をappend-only新規2Leanで構成。元F54 LocalRotationの真正 `B`、元二Nat cast `C`、`P=B⁶`、`H=B³` から、既存の偶数経路 `Pʲ C P²ᵈ C Pʲ`（j+d=k）と新規の奇数経路 `Pʲ H C P²ᵈ⁺¹ C H Pʲ`（j+d+1=k）を同一の実旧`q_k`ファイバーへ入れる。旧GK4AG観測全値を一致させたまま、GK4AH第二行列decoderは**偶数側 `8-192d`、奇数側 `-88-192d`** となり、偶奇各族内・族間の衝突が無い。この真の型付きsourceから**`∀k, Fin(2*k+1) ↪ Fiber(q_k)`**と **`Countable Fiber(q_k)`** をLean4証明。C60真正北六角形への無条件特殊化も証明。これは同一`q_k`内の有限下界であり、固定単一ファイバーの無限性、全体濃度や完全有限正規形は主張しない。

**GK4AN exact-source正本：** final source HEAD `7b122beae70e0d069c0b922f7b429d0da1b930f8`、CI test-merge checkout `3c8699e452fbf84598d7339118c02c1cddc04e53`、定理squash・定理直後main `d95fdece191605e413423c6efede04ac739b611c`、三者共通Git tree `70653a884faf43a83f9de7db846d858576b366e3`。[CI #41193236442](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41193236442) **Strict Lean 3769/3769 SUCCESS・Governance 5/5 SUCCESS・新規16宣言標準3公理以内・sorryAx0・変更Lean warning/error0/0**。[GK4AN詳細証明・初回elaboration修正と最終receipt](docs/formal/GK4AN-doubled-finite-typed-fiber-lower-bound.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心／独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージを保持。

**次段階GK4AO候補（未証明）：** 固定旧`q`内の無限個の真正像の成否を精査し、GK4AHの第二整数行列の行列式・合同制約など到達可能値の必要条件も形式化する。GK4AL可算性、GK4AMの正のkでのFamilyCovers反証は維持。元P92B Q自身の圏公理・歴史的完全型付き同値・真正14D無条件Countable・19D filler・global strict・hyperdescentは別問題として保持。

> 以下のGK4AM以前の「最新・次候補」は歴史時点の記録。現行frontierはGK4AN。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AM

**真正K_AI→K_AG忘却ファイバー内で、GK4AK有限族は全ての正のkに対して非網羅 — [定理PR #2811](https://github.com/itakura-hidetoshi/KuuOS/pull/2811) MERGED。** [k=1の真正元F54反例Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AMNoncoverage.lean)・[全正kへの一様化Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AMUniformNoncoverage.lean)をappend-only新規2Leanファイル・公理表示25宣言で形式化。GK4AJの実依存型経路`V=B³;C;B⁶;C;B³`はGK4AKの`q_1`に属し、既存有限族2点の第二行列decoder `-184`・`8`とは異なる`-88`を与えるため、**`¬FamilyCovers(1)`** を無条件で証明。さらに、実`LocalRotation`に由来する`H=B³`、`P=B⁶`から`V_d=H;C;P^(2d+1);C;H`を構成し、旧四成分＋第一行列が`q_(d+1)`と完全一致する一方、第二行列decoderは`-88-192d`である。GK4AK族の`8-192(d+1-j)`と一致しないので、**`∀k>0, ¬FamilyCovers(k)`をLean4証明**。真正C60北側六角形へ無条件特殊化。これは既存族がファイバーを尽くさないという定理であり、**一つの固定ファイバーの無限性はなお未証明**。

**GK4AM exact-source 正本：** 最終source HEAD `661cee6a92152f64d09ab8a72e6373f3db9cba6c`、CI checkout `8a38ef1efcc072d478e19e372c31aa1ab16fc79b`、定理squash・統合直後main `6ef7ccacce400f9ead9fadc5e92354c2c18397e7`、三者のGit treeが`f5c5595b08e19261d74a615ad31247d8e0a5a8b8`で完全一致。[CI #41191976426](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41191976426) **Strict Lean 3767/3767 SUCCESS・Governance 5/5 SUCCESS・25宣言標準3公理以内・sorryAx0・変更Lean warning/error 0/0**。[GK4AM詳細証明・Lean記法修正とCI receipt](docs/formal/GK4AM-uniform-positive-finite-family-noncoverage.md)。固定Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージ。

**GK4ALとの境界：** `FamilyCovers(k) → Fin(k+1) ≃ Fiber(q_k)`という条件付き定理はそのまま正しいが、GK4AMはk>0で仮定が偽と示す。各Fiberは高々可算かつファイバー径に一様な有限上界がないというGK4AK・GK4ALも保持。k=0の網羅性、全体の正確な濃度、単一固定無限ファイバー、`S→K_AI`全域忠実性／非忠実性、元Q圏公理、元Type値比較証拠にない3-cell、14D／19D／global strict／hyperdescentは依然未証明。

> 以下のGK4AL以前の「最新・次候補」はそれぞれ当時の歴史スナップショット。現行frontierはGK4AM。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AL

**すべての真正K_AI→K_AG忘却ファイバーの可算性と条件付き有限行列正規形 — [定理PR #2809](https://github.com/itakura-hidetoshi/KuuOS/pull/2809) MERGED。** [全元F45依存型Homの真正ファイバー可算性Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ALCountableFibers.lean)・[真正有限族の第二行列正規形と被覆条件Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ALFiniteMatrixNormalForms.lean)をappend-only新規2Leanファイルで形式化。任意の元F45 source/target・任意旧K_AG類qに対し、真正従属型 `Fiber(q)={z:K_AI | U_AI,AG(z)=q}` から整数2×2行列への単射を持つため、**`Countable Fiber(q)`** をLean証明。さらに全K_AI型付きHomもCountable、各Fiberは実際に到達した第二行列の集合と正確にEquiv。任意の元F54 LocalRotationの真正自己Homおよび物理C60北側六角形について、**任意kで同じ到達旧類q_kのファイバーは可算、かつ`Fin(k+1) ↪ Fiber(q_k)`**をLean4で証明。構成したk+1行列の完全な有限正規形を定理化し、それらが**ファイバー全体を尽くすこと**は「到達第二行列像がその有限族で被覆されること」と必要十分であると証明。全体との`Fin(k+1) ≃ Fiber(q_k)`はその追加被覆条件の下で**のみ**成立。固定単一ファイバーの無限性、被覆条件そのもの、全整数行列到達性、`S→K_AI`全域忠実性は**未証明**。

**前段GK4AKも正本へ同期 — [定理PR #2807](https://github.com/itakura-hidetoshi/KuuOS/pull/2807) MERGED：** 元F54真正の `W_k(j)=B^(6j);C;B^(12(k-j));C;B^(6j)` は旧四成分と第一行列が同じで、第二行列の整数decoder **`4b+2e-2a-c=8-192(k-j)`** で添字を分離。任意kで一つの真正到達ファイバーへの`Fin(k+1)`埋め込みを証明し、異なるkの旧類q_kも区別した。したがって**ファイバー径に一様な有限上界はない**。GK4AK [CI #41188601545](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41188601545) Strict Lean **3763/3763 SUCCESS**、Governance 5/5 SUCCESS、標準3公理のみ、sorryAx 0。[GK4AK証明・独立receipt](docs/formal/GK4AK-unbounded-finite-forgetful-fibers.md)。

**GK4AL exact-source正本：** final source HEAD `ef696a52c417306d3c7c37cfcc32dd3ba0e0aa44`、定理squash＝定理統合直後main HEAD `6bbf03a04ee972399d54828d915e8f739698bcd5`、[CI #41190283756](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41190283756) **Strict Lean 3765/3765 SUCCESS・Governance 5/5 SUCCESS・新規公理表示14宣言は標準3のみ・sorryAx 0・変更Lean warning/error 0/0**。[GK4AL詳細証明・Mathlib補題名修正・CI receipt](docs/formal/GK4AL-countable-typed-fibers-finite-matrix-normal-forms.md)。固定Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107・strict空中心／独立Kuu一presentation・Gray非再導入・保護PR #1558 Draft／OPEN／未マージ。

**次候補GK4AM（未証明）：** 固定された旧K_AG類一つに無限個の真正異なる第二行列を載せられるか、または追加到達制限から有限族非網羅性・正確な像を明らかにする。任意大有限下界から単一無限ファイバーを推論しない。元Qの結合律・単位律、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentも未証明のまま。

> 以下のGK4AJ以前の「最新・次候補」は当時の歴史スナップショット。現行frontierはGK4AL。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AJ

**真正忘却ファイバーの三類下界・第二行列到達像の正確な同値 — [定理PR #2805](https://github.com/itakura-hidetoshi/KuuOS/pull/2805) MERGED：** [元F54真正三経路Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AJTernaryPhysicalFiber.lean)・[真正第二行列ファイバー同値Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AJExactMatrixFiber.lean)をappend-only新規2Leanファイル・**公理表示35宣言**で形式化。元F54の本当の二Nat cast `C`と実`LocalRotation`の前後2回転backtrack `B`を用いる3つの**同一型付き自己Hom**の経路 `w0=C;B¹²;C`、`w1=B³;C;B⁶;C;B³`、`w2=B⁶;C²;B⁶`について、元四成分観測が三者とも厳密に**`(false,-22,12,-132)`**、旧GK4AF行列も三者とも**`[[1,2],[0,1]]`**になることをLean証明。旧行列に表現由来の`B1³=-I`・`B1⁶=I`があるため同一の旧第二商`K_AG`類となる。しかし真正Type値比較全F55/P92B/独立構造seamを保存する第二行列`M_AH`は、`w0=[[-23,-34],[-48,-71]]`、`w1=[[1561,638],[-2640,-1079]]`、`w2=[[-599,-274],[1104,505]]`で**pairwise異なる**。従って新`K_AI`に**相異なる少なくとも3類が一つの実旧`K_AG`忘却ファイバー上に存在**することをLean4で証明。元LocalRotationを持つ任意の真正自己Hom・物理C60北側六角形に特殊化した。

**一般の完全なファイバー値分類：** 任意の元F45型付きHom上の真正第二商の任意`x,y:K_AI`で、`x=y ↔ U_AI,AG(x)=U_AI,AG(y) ∧ M_AH(x)=M_AH(y)`を証明。固定された**実際に到達可能**な旧K_AG類`q`について、真正の型付き`Fiber(q)={x:K_AI | U(x)=q}`を構成し、第二行列観測が**そのFiber内で単射**であること、さらに`Fiber(q) ≃ {M_AH(x) | x∈Fiber(q)}`をMathlib `Equiv.ofBijective`で厳密に証明した。全整数2×2行列が実現するとは主張せず、元P92B Q自身の未証明圏公理、元`S→K_AI`の全域忠実性、歴史的完全同値、Gray圏、hyperdescentとは区別する。

**exact-source正本：** 最終定理source HEAD `537d38346b0fae76e7c4ca01bd2b010073211539`、定理squash SHA＝定理マージ直後canonical main HEAD `cf859a9eb1f77a3b36dcabd3319b795b43e96101`。[CI #41187062144](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41187062144) **Strict Lean 3761/3761 SUCCESS、Governance 5/5 SUCCESS、35宣言公理依存標準3以内、sorryAx 0、変更Lean warning/error 0/0**。前段[CI #41186504054](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41186504054)の初回DNS失敗から同じsourceで再試行し、Lean記法の`congrArg`関数適用展開と元`rot`引数束縛を修正。[詳細証明・元F54経路・CI修正・receipt](docs/formal/GK4AJ-ternary-forgetful-fiber-exact-matrix-image.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray再導入なし、保護PR #1558 Draft・OPEN・未マージ維持。

**次段階GK4AK（未証明）：** 三類から任意に大きな有限ファイバーへの構成・到達可能第二行列値の正規形、または元`S→K_AI`自体の忠実性／残余障害を元F54真正経路と比較証拠から独立検討する。元P92B Q自身の結合律・単位律、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明。

> 以下のGK4AI以前の「最新・次候補」はその時点の歴史的記録。現行frontierはGK4AJ。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AI

**真正二行列積観測の第二kernel圏と忘却関手をLean4で証明 — [定理PR #2803](https://github.com/itakura-hidetoshi/KuuOS/pull/2803) MERGED：** [GK4AI元Q/S積観測Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIProductObservation.lean)・[真正第二kernel圏Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIKernelCategory.lean)・[K_AI→K_AG忘却関手Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIForgetful.lean)をappend-only新規3Leanファイル・**公理表示47宣言**で形式化。元F54の四成分観測 `O_AE` と元GK4AF／GK4AHの非可換整数2×2行列値を合わせた**真正積観測 `O_AI(r)=(O_AE(r),M_AF(r),M_AH(r))`**を構成。元F55全9・元P92B全9（真正assocNaturality）、独立構造seam全14、拡張比較全3の実Type値保存性を成分ごとに継承し、元P92B存在商`Q`と独立構造商`S`へ別々に降下、正準`Q→S`可換性、元F54合成・左右文脈を証明した。値域は旧非可換積と第二行列積の直積であり、結合律・左右単位を厳密に形式化。

**新第二kernel圏・関手・真正C60非忠実性：** 元`Q`の新観測等値kernelによる別の真正第二商`K_AI`を、到達可能な値域imageの積からMathlib Categoryとして構成し、**元Q自身の未証明結合律・単位律を使用しない**。元`S→K_AI`比較Functorは各Hom全射、`K_AI→`新組観測値圏はHom単射。旧第二商`K_AG`への真正**忘却Functor`K_AI→K_AG`**は各Hom全射で、単位・合成と`S→K_AG`比較を保存、さらに既存`K_AG→K_AE`との複合可換性を証明。GK4AHの本物の元F54依存型自己経路`u=C;B⁶;C`、`v=B³;C²;B³`は旧四成分`(false,-10,6,-30)`と旧行列`[[1,2],[0,1]]`が一致するが、新行列は`[[-11,-16],[-24,-35]]`と`[[-155,-64],[264,109]]`で異なる。ゆえに**新`K_AI`では二類が異なり、旧`K_AG`で像が等しい**。`K_AI→K_AG`は任意の実F54 LocalRotationを持つ自己Homと真正C60北側六角形で**非忠実**。ただし`S→K_AI`の全域忠実性は**未証明**。

**exact-source正本：** 最終定理source HEAD `7c6f5822d6ae1285dd4350473ff88eddd583f4e0`、定理squash SHA＝定理マージ直後canonical main HEAD `74a2e656afd72a4796fd322d7602f9f904e0a15a`。[CI #41185737418](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41185737418) **Strict Lean 3759/3759 SUCCESS・Governance 5/5 SUCCESS・47宣言標準3公理以内・sorryAx 0・変更Lean warning/error 0/0**。新規3Leanファイルの初回exact-source検証で成功。[GK4AI詳細証明・圏／比較の権限境界・検証記録](docs/formal/GK4AI-two-matrix-kernel-forgetful-refinement.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定、公開root107、strict空中心／独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft・OPEN・未マージ維持。

**次段階GK4AJ（未証明）：** 元`S→K_AI`自体の忠実性を、真正F54型付きsourceと元Type値比較証拠から独立検討する。二行列値でも残る構造衝突、または有限生成文脈に限定した正確な忠実性条件を検証する。元P92B Q圏公理、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明として保持。

> 以下のGK4AH以前の「最新・次段階」は歴史時点の記録。現行frontierはGK4AI。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AH

**真正積観測への構造比較の残余非忠実性を証明 — [定理PR #2801](https://github.com/itakura-hidetoshi/KuuOS/pull/2801) MERGED：** [第二行列表現Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AHAlternativeMatrixInvariant.lean)・[真正F54反例Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AHJointResidualNonfaithfulness.lean)をappend-only新規2Leanファイル・公理表示48宣言で形式化。元GK4AGの積観測 O_AG=(O_AE,M_AF) の全値が一致しながら、独立構造商Sの元Type値経路が真に異なる反例を得た。元F54の二Nat cast C、実LocalRotationの前後2回転backtrack Bで真正同型付き自己経路 u=C;B⁶;C、v=B³;C²;B³ を構成。**O_AE(u)=O_AE(v)=(false,-10,6,-30)**、旧GK4AF行列 **M_AF(u)=M_AF(v)=[[1,2],[0,1]]** だが、新しい第二行列は **M_AH(u)=[[-11,-16],[-24,-35]]** と **M_AH(v)=[[-155,-64],[264,109]]** に分離する。新しい後向き行列R4=[[1,0],[4,1]]と正方向F=[[1,-1],[0,1]]、cast C=[[1,1],[0,1]]は真正assocの C*F=I を保持しつつ旧Bの B³=-I・B⁶=I という表現依存の有限位数を回避。

**元Type値比較証拠と忠実性境界：** 元F55全9、P92B全9（真正assocNaturality）、独立構造seam全14、拡張比較全3に対する新行列値保存性を帰納法で証明。元Qと独立Sへ別々に降下し、Q→S可換性とS合成・単位整合を確認。この第二行列で **[u]_S ≠ [v]_S** を証明する一方、GK4AGの真正第二kernel商では **F_AG([u]_S)=F_AG([v]_S)**。従って**本物の比較関手S→K_AGは、任意の実F54 LocalRotationを持つ自己Homでなお非忠実**。真正C60北側六角形についても無条件にLean証明。元P92B商Qの未証明圏公理や新しいType値3-cellは仮定していない。

**定理検証正本：** 最終exact-source HEAD `afdd0096b42e8fcc527417d530be3c12d1c1b1d5`、定理squash SHA＝マージ直後main HEAD `3532a723478362c14d88fc1f24b8bf8c33f41d72`。[CI #41184959463](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41184959463) **Strict Lean 3756/3756 SUCCESS、Governance 5/5 SUCCESS、48宣言標準3公理以内、sorryAx 0、変更Lean warning/error 0/0**。初回CIでは観測のcast電荷を誤読した四成分の具体数値補題2件のみ不成功。GK4AD原ソースを照合して正しい (false,-10,6,-30) に修正した。[詳細証明・数学的限界・exact-source receipt](docs/formal/GK4AH-residual-joint-kernel-nonfaithfulness.md)。Lean v4.30.0-rc2/mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心／独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft・OPEN・未マージ維持。

**次段階GK4AI（未証明）：** 真正 O_AI=(O_AE,M_AF,M_AH) の新しい第二kernel商K_AI、比較・忘却 S→K_AI→K_AG→K_AE の関手を元Q/S別々のauthorityを保って構成し、なお残る忠実性障害を独立検査する。元Qの結合律・左右単位、歴史的完全型付き同値、14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明。

> 以下のGK4AG以前の「最新・次段階」は履歴時点の記録。現行frontierはGK4AH。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AG

**元F54の四成分＋行列の積観測から真正第二kernel圏と忘却関手を構成 — [定理PR #2799](https://github.com/itakura-hidetoshi/KuuOS/pull/2799) MERGED：** [GK4AG元Q/S積観測Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGProductObservation.lean)・[真正第二kernel圏Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGKernelCategory.lean)・[旧K_AEへの忘却関手Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGForgetful.lean)をappend-only **3 Leanファイル・公理表示46宣言**で形式化。GK4AEの真正四成分`O_AE`とGK4AFの元F54非可換整数2×2行列`M`を組み合わせ、`O_AG(r)=(O_AE(r),M(r))`を構成した。値の積は四成分の非可換積と本物の行列積の直積であり、結合律・左右単位、元F54の合成・左右文脈、元P92B証拠存在商`Q`および独立構造商`S`への**別々の降下**、元`Q→S`可換性、構造seam全14の保存を証明。GK4AFで確認済みの元F55全9・P92B全9（真正assocNaturality）・拡張比較全3のType値証拠を維持し、新たな元P92B 3-cellを発明しない。

**真正第二kernel商と精密化：** 元`Q`に対して`O_AG`の**値一致**で作る別の第二kernel商`K_AG`を、到達可能な観測値の積からMathlibの真正Categoryに構成。元`Q`自体の未証明な結合律・単位律は使用しない。元独立構造圏`S→K_AG`の真正比較Functorは各Hom**全射**、`K_AG→`組観測値圏はHom**単射**。さらに**真正忘却Functor`K_AG→K_AE`**を構成し、各Hom全射、元`S→K_AE`比較との可換性と単位・合成保存を証明。GK4AFの真正依存型自己経路`u=C;B;B;C`、`v=B;C;C;B`は四成分`O_AE(u)=O_AE(v)=(false,-2,2,-2)`で一致するが、`M(u)=[[0,-1],[1,1]]`・`M(v)=[[-1,-1],[3,2]]`で異なる。従って**`[u]_{K_AG}≠[v]_{K_AG}`、しかし`K_AE`への像は等しい**。真正`K_AG→K_AE`は任意の実F54 LocalRotationを持つ自己Homで**非忠実**、実C60北側六角形でもLean4証明。`S→K_AG`の**全域忠実性は未証明**で、局所必要十分条件のみ提示。

**定理検証正本：** final exact-source HEAD `735e9db16d3130a5df36431d073575393cbb5ff7`、定理squash SHA＝マージ直後canonical main HEAD `29832485498d1ded71a9cbd9eadf3cf07085ffa2`。[CI #41183798699](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41183798699) **Strict Lean 3754/3754 SUCCESS、Governance 5/5 SUCCESS、公理表示46宣言は標準3公理以内、sorryAx 0、変更Lean warning/error 0/0**。初回CIの商類`⟦q⟧`表示に伴う`rw`不一致は`change`で型付き代表を明示して修正。[証明・CI修正・限界・exact-head receipt](docs/formal/GK4AG-joint-matrix-kernel-forgetful-refinement.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root 107、strict空中心／独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージを維持。

**次段階GK4AH（未証明）：** 真の独立構造商`S→K_AG`にまだ残る非忠実性を、元F54の型付き経路・非可換履歴・局所文脈・真正比較証拠から独立検証する。元P92B商Qの結合律・単位律、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentも未証明。

> 以下のGK4AF以前の「最新・次段階」は歴史的な当時の記録。現行frontierはGK4AG。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AF

**元F54の真の2×2整数行列履歴から四成分観測の残余非忠実性を証明 — [定理PR #2797](https://github.com/itakura-hidetoshi/KuuOS/pull/2797) MERGED：** [GK4AF真正行列不変量Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AFMatrixInvariant.lean)・[GK4AF真正S→K_AE非忠実性Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AFResidualNonfaithfulness.lean)を**append-only新規2Leanファイル・42宣言**で証明。元F54の真のType値 `castDepths`を`C=[[1,1],[0,1]]`、正方向実`LocalRotation`を`F=[[1,-1],[0,1]]`、負方向実回転を`R=[[1,0],[1,1]]`に写す**非可換整数2×2行列積**を導入。4成分の環等式で結合律、左右単位、**元F54の本物のassocの1 cast・1 forwardに対応する`C*F=I`**を証明。元の`RotationEdge`・中間木`RotationChain`・5構成子`DepthRotationRoute`の全依存型履歴を保持したまま、**本来のF55全9・P92B全9（実assocNaturalityを含む）・F54構造seam全14・拡張構造比較全3**のType値証拠の帰納法ですべて保存性を検証。元P92B存在商`Q`と独立構造商`S`へ**別々に降下**、正準`Q→S`比較との可換性・真正S合成の行列積保存を形式化。元P92Bの未証明圏公理や数字からType値3-cellを製造する仮定を使わない。

**GK4AFの真正反例（四成分では不忠実）：** 実`rot:LocalRotation p before after`がある場合、元F54の真の二Nat cast自己経路`C`と実前後回転backtrack`B=F*R`から**真正元F54型付き自己経路`u=C;B;B;C`と`v=B;C;C;B`**を構成。元GK4AEの**四成分`O_AE(u)=O_AE(v)=(false,-2,2,-2)`は完全一致**。しかし新しい行列値は**`M(u)=[[0,-1],[1,1]]`、`M(v)=[[-1,-1],[3,2]]`**で相異なる。全構造seamで行列値が保存されるため、**`[u]_S≠[v]_S`**である一方、真正第二商`K_AE`では像が一致する。したがって**本物の比較関手`S→K_AE`は実F54局所回転を持つ任意の型付き自己Homで非忠実**。真正C60北側六角形でも無条件に証明。これはGK4ACの異なる`K_AA→K_X`の完全`Nat`ファイバー、GK4ADの`S→K_AA`非忠実、GK4AEの`K_AE→K_AA`非忠実とそれぞれ両立する。

**定理検証正本：** 定理squash SHA＝定理マージ直後canonical main HEAD `53526634b254907320426876bd0f19cd5a05f768`、最終exact-source HEAD `0ba7499f91ef1420f705d35ec46097f3aff634d1`。[CI #41182480085](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41182480085) **Strict Lean 3751/3751 SUCCESS、Governance 5/5 SUCCESS、42宣言`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[詳細証明・Lean修正・CI receipt](docs/formal/GK4AF-matrix-history-four-observer-nonfaithfulness.md)。Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージ維持。

**次段階GK4AG（未証明）：** 真正四成分観測`O_AE`と新行列値`M`を合わせたさらなる第二kernel商を構成し、元の`S`・`Q`と異なる観測商を保った比較・忘却関手を検証する。**行列値を追加した後の全域faithfulnessは主張しない**。元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentも未証明。

> 以下のGK4AE以前の「最新・次候補」は歴史時点の記録。現行frontierはGK4AF。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AE

**元F54四成分非可換観測・真正第二kernel圏・順序moment忘却の非忠実性 — [定理PR #2795](https://github.com/itakura-hidetoshi/KuuOS/pull/2795) MERGED：** [GK4AE元四成分観測Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEFourObserver.lean)、[元F54観測同定・真正比較Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEComparison.lean)、[真正四成分第二kernel圏Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEKernelCategory.lean)、[真正順序moment忘却関手Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEKernelForgetful.lean)を**append-only新規Lean4ファイル・69宣言**で証明。

元F54真正Type値経路から四成分`O_AE(r)=(physicalGrade, castCharge, backwardCount, orderedMoment)`を構成。値域`Bool × ((Int×Nat)×Int)`の積は`(g,(c,b,m))⋄(h,(d,e,n))=(g&&h,(c+d,b+e,m+n+c*e))`であり、**非可換**。本来のF55全9、元P92B全9（実assocNaturality）、独立構造seam全14、拡張構造比較全3の実Type値保存証明を前提として、**元P92B証拠存在商Qと独立構造比較商Sへ別々に降下**し、元F54全構成子で合成・左右文脈の整合性を証明。さらにGK4ADで構成した順序付き観測の最初の2成分が**元GK4W castChargeおよびGK4Z backwardCountと本当に一致**することを、元RotationEdge/RotationChain/DepthRotationRouteに対する完全帰納法で証明。観測値の一致から元Type値P92B 3-cellは生成しない。

**新しい第二kernel商`K_AE`**は元`Q`から四成分観測値一致で構成した真正GK4S商であり、元`Q`の未証明圏公理を使わずに**Mathlibの結合律・左右単位を四成分値の非可換積から形式化**。`S→K_AE`比較はHom全射、`K_AE→`四成分値圏はHom単射。第四成分だけを忘れる**真正Mathlib関手`K_AE→K_AA`**を構成し、元の`S→K_AA`との可換性およびHom全射を証明。本物の元F54 Type値経路`u=cast;backtrack`、`v=backtrack;cast`では`O_AA(u)=O_AA(v)=((false,-1),1)`だが`orderedMoment(u)=0`、`orderedMoment(v)=-1`。したがって**`[u]_{K_AE}≠[v]_{K_AE}`なのに`K_AA`へは同一視され、真正`K_AE→K_AA`忘却関手は任意の実F54局所回転を持つ型付きself-Homで非忠実**。真正C60北側六角形にも特殊化。GK4ADの`S→K_AA`非忠実性、GK4ACの別の`K_AA→K_X`完全ファイバー同値とは区別する。**`S→K_AE`の全域忠実性は未証明**として保持する。

**定理検証正本：** 最終exact-source HEAD `26ae50769b959e2d9b0a27af6196773f9d952deb`、定理squash SHA＝マージ直後canonical main HEAD `1480dc47852cfe6a3224e0811e7dec1a377d01b3`。[Strict Lean/Governance #41181371095](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41181371095) **3749/3749 Strict Lean SUCCESS、Governance 5/5 SUCCESS、69宣言`#print axioms`標準3公理以内、sorryAx 0、変更Lean warning/error 0/0**。[証明・数学的権限境界・Lean記法修正履歴](docs/formal/GK4AE-four-component-observer-kernel-refinement.md)。Lean v4.30.0-rc2・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージ保持。

**次段階GK4AF（未証明）：** 四成分観測の同一値ファイバー内で真に異なる元構造商`S`類が残るか、元F54の文脈位置・非可換高次順序・原Type値履歴を用いて忠実性／障害を判定する。元P92B`Q`の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明。

> 以下のGK4AD以前の「最新」「次段階」は歴史記録。現在の形式化frontierはGK4AE。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AD

**真正三成分観測の残余非忠実性を非可換原F54履歴で解決 — [定理PR #2793](https://github.com/itakura-hidetoshi/KuuOS/pull/2793) MERGED：** [非可換順序付き履歴不変量Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ADOrderedHistoryInvariant.lean)・[三成分観測の真正非忠実性Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ADTripleNonfaithfulness.lean)を**append-only新規Lean2ファイル・36宣言**で証明。元F54の**実Type値`castDepths`と`RotationEdge.backward`の順序**を、`((castCharge,backwardCount),orderedMoment) : (Int×Nat)×Int`で記録。真正非可換演算`(c,b,m)⋄(d,e,n)=(c+d,b+e,m+n+c*e)`、単位`(0,0,0)`を構成。元の真正F54 assocが含む1 cast・1 forwardはこの値で単位になる一方、castとbackwardの順序は交換できない。**元F55全9、元P92B全9（本物のassocNaturalityを含む）、構造seam全14、拡張構造比較全3の実Type値構成子を個別帰納法でsoundness検証**し、新観測を`Q`元P92B証拠存在商と`S`独立構造商へ**別個に降下**。実`Q→S`可換、構造合成保存、構造単位も証明。原Type値3-cellを観測一致から生成しない。

**GK4ADの新しい真正反例：** 実`rot:LocalRotation p before after`から、元F54真正前後物理回転backtrack`B`と本物の`castDepths rfl rfl`経路`C`を用い、**実型付き自己経路`u=C;B`と`v=B;C`**を構成。元GK4AA三成分観測は**`O_AA(u)=O_AA(v)=((false,-1),1)`**と一致。しかし順序付き不変量は**`M(u)=0`、`M(v)=-1`**。この違いは全構造seamの下でも保存されるため**`[u]_S≠[v]_S`**、一方真正`K_AA`第二商では同一類となる。よって**真正独立構造圏`S→K_AA`比較関手は元F54局所回転を持つ任意の型付き自己Homで非忠実**。本当のC60北側六角形についても無条件に証明。これはGK4ACの別の`K_AA→K_X`忘却ファイバーの`Nat`完全同値とは異なる問題であり、両結果を混同しない。

**定理検証正本：** 定理squash SHA＝定理マージ直後canonical main HEAD `62586f3d26a2ad78e466ceef8a9473b8e0566f3a`、final exact-source HEAD `c2a1d6746cc4a07cdc28048b308d663b17044e4a`。[Strict Lean・Governance #41179319781](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41179319781) **Strict Lean 3745/3745 SUCCESS、Governance 5/5 SUCCESS、36宣言`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[詳細証明と検証記録](docs/formal/GK4AD-ordered-F54-history-triple-nonfaithfulness.md)。Lean v4.30.0-rc2・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージを保持。

**次段階GK4AE（未証明）：** 新しい順序付きmomentを追加する四成分の真正観測kernel商を構成して`S`との比較と旧`K_AA`への忘却を定理化し、その観測でも残る別の情報損失が存在するかを判定。元P92B商の結合律・単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明。

> 以下のGK4AC以前の「最新・次候補」は歴史時点の記録。現在の形式化frontierはGK4AD。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AC

**真正F54前向き回転rankによる逆回転0障害の除去と完全Natファイバー同値 — [定理PR #2791](https://github.com/itakura-hidetoshi/KuuOS/pull/2791) MERGED：** [GK4AC実F45左結合rank Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ACForwardRank.lean)と[GK4AC真正第二商ファイバー同値Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ACExactPositiveFiber.lean)を**append-only新規2Leanファイル・26宣言**で形式化。元F45の二圏・四Blocks・二Nat depth・型付き葉を保持し、`L(refl/leaf)=1`、`L(node A B)=L(A)+L(B)>0`と、`W(node A B)=W(A)+W(B)+L(A)`の真正自然数値**左結合rank**を構築。元の実`LocalRotation.assoc`で`((A B) C)→(A (B C))`は`W`を厳密に`L(A)≥1`だけ減少。元`LocalRotation`全3構成子、実`RotationEdge`・中間木`RotationChain`、二Nat cast、元`DepthRotationRoute`のchain/trans/左右文脈を元Type値のまま帰納法で検証して、**`backwardCount(r)=0 ⇒ W(last)+rotationCount(r)≤W(first)`**を証明。従って**真正F54の型付き自己経路で逆回転数0なら物理回転数も0**。

**GK4ABの唯一の残余障害を解消：** 真正K_AA第二商のself-Homでは`backwardCount=0⇒Boolean grade=true`。一方GK4Zの元F54本物のbalanced tower`R_k`は旧`K_X`にすべて`(false,-2)`で写る。したがって旧`[R_0]_{K_X}`上の本物の`K_AA→K_X`忘却ファイバーに**GK4ABが残した`backwardCount=0`の例外は存在しない**。GK4ABで既に証明した正階層完全正規形と合わせて、**真の元F54 Type値towerの写像`k↦[R_k]_{K_AA}`から`Nat ≃ Fiber(K_AA→K_X,[R_0])`の真正Lean Equivを構成**。実各ファイバー類の添字は一意。真正C60北側六角形も無条件に同じ同値とzero層空性を証明。これは`S→K_AA`の全域faithfulnessを主張しない。`Q`元P92B証拠存在商、`S`独立構造商、`K_AA/K_X`異なる二段目kernel商のauthorityを維持し、観測一致から元Type値P92B 3-cellを生成しない。

**定理検証正本：** 定理squash＝マージ直後canonical main HEAD `f77277798860d4bbd8fbb6d557e7fefb7870f314`、最終exact-source HEAD `9f7ad594782025cc55f0d0bf01f1bd6ed984e6a3`。[Strict Lean/Governance CI #41178066934](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41178066934) **3743/3743 Strict Lean SUCCESS、Governance 5/5 SUCCESS、26件`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[証明・CI記法修正記録](docs/formal/GK4AC-forward-left-rank-exact-fiber.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107、strict空中心・独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージ保持。

**次段階GK4AD（未証明）：** 真正`S→K_AA`が元F54構造商射に忠実か、さらに保存されない元Type値履歴・非忠実性が存在するかを独立に検証。元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明。

> 以下のGK4AB以前の「最新」「次段階」は歴史記録。現行の証明frontierはGK4AC。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AB

**真正逆回転数ファイバー正規形 [定理PR #2789](https://github.com/itakura-hidetoshi/KuuOS/pull/2789) MERGED：** [GK4AB新規Lean形式証明](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ABBackwardFiberNormalForm.lean)で、真正F54元Type値経路・元P92B商`Q`・独立構造商`S`・異なる二つの二段目観測kernel商`K_AA`と`K_X`を保持したまま、**全ての実F45型付き境界・任意の旧`K_X`類`q`**に対する実忘却ファイバー`F_q={z:K_AA | ForgetBackward(z)=q}`を分類。新しい`beta(z)=backwardCount(z):Nat`が**`F_q`上で単射**であり、真正Equiv `F_q ≃ Set.range(beta) ⊆ Nat` をLean4で証明。ゆえに元D/E圏の一般Countableを仮定せず、**すべての真正二段kernel忘却ファイバーがCountable**。`K_AA`圏の合成ではbetaが加法的、単位は0。**元P92B商Qを圏にしていない**。

**真正balanced towerの正値完全正規形：** 真正F54のType値`LocalRotation`証拠を持つ任意の元F45自己Homで、GK4Zの実物理前後回転・castDepthsにより構成した`R_k`は`O_X(R_k)=(false,-2)`、`O_AA(R_k)=((false,-2),k+1)`を満たす。旧`K_X`の実`[R_0]`類上の`K_AA`ファイバーでは、**後向き回転数が正である任意の商類`z`が、ただ一つの`[R_k]_{K_AA}`に一致**すると証明。`beta(z)=0`の層は存在しても高々**1類**。さらに**tower全射 iff このゼロ階層類が存在しない**という必要十分条件、実到達逆回転数範囲の厳密な式、真正C60北六角形での正値正規形を証明した。**ゼロ階層が実際に空であるかはGK4ABでは未証明**。元`S→K_AA`の全域忠実性も未証明のまま。

**定理検証正本：** 定理squash SHA（定理マージ直後のcanonical main HEAD）`decd01552f25d5367d775eaaa3ec43609e6ae619`、最終exact-source PR HEAD `0972b7c6943fec53c39b8122420f8c277a14772c`、[CI #41176694544](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41176694544) **Strict Lean 3741/3741 SUCCESS、Governance 5/5 SUCCESS、新規20宣言の`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[詳細証明・Lean記法修正記録](docs/formal/GK4AB-backward-fiber-normal-form.md)。Lean v4.30.0-rc2／固定mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージを保持。

**次段階GK4AC（未証明）：** 真正F45二分木の左結合rankなどを用い、**後向き回転0かつ前向き回転正の自己経路が不可能**であることを、型付き実F54局所回転・cast・trans・左右文脈の全構成子で検証。これが得られればGK4ABの唯一のゼロ障害を除き、当該`K_AA→K_X`ファイバーの`Nat`完全正規形を証明できる。元`S→K_AA`忠実性、元P92B商の結合律・単位律、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは依然未証明。

> 以下のGK4AA以前の「最新・次候補」は歴史記録。現在の形式化frontierはGK4AB。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4AA

**真正三成分観測・第二kernel圏 [定理PR #2787](https://github.com/itakura-hidetoshi/KuuOS/pull/2787) MERGED：** [三成分観測](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAThreeComponentObserver.lean)／[真正商間比較](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AATripleComparison.lean)／[三成分kernel圏](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAKernelCategory.lean)／[真正忘却関手](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAKernelForgetful.lean)を**append-only Lean4ファイル・72宣言**で証明。GK4Xの`(Bool,castCharge)`とGK4Zの元F54真正後向き回転Type値証拠個数を組み合わせ、**`O_AA(r)=((grade(r),castCharge(r)),backwardCount(r))`**を、元P92B証拠存在商`Q`と独立F54構造比較商`S`に**別個に降下**させた。元F54の合成・左右文脈・実全14構造seam保存・元Q→S可換性・単位観測を形式化（GK4Zの元F55全9・P92B全9・構造seam全14・拡張比較全3のsoundnessを継承）。観測値一致から元Type値3-cellを生成しない。

**真正第二商`K_AA`の圏と4関手：** 元P92B商`Q`とは別の**三成分観測kernel第二商**で、実到達観測値上の合成を使うMathlib Categoryの結合律・左右単位を証明。`S→K_AA`比較Functor（各Hom全射）、`K_AA→(Bool×Int)×Nat`値域Functor（各Hom単射）、別の`K_AA→K_X`忘却Functor（各Hom全射）、`S→(Bool×Int)×Nat`真正観測Functorを構成し、対象・射の厳密な因子化を証明。**元P92Bの結合律・左右単位は使わない**。

**新しい厳密な可算無限ファイバー：** GK4Zの真正F54 balanced回転塔`R_k`は`O_AA([R_k]_S)=((false,-2),k+1)`で、`K_AA`の異なる商類へ**Nat単射**。旧GK4X`K_X`では全段が同じ`(false,-2)`に写る。したがって**実局所回転証拠を持つ任意のF45自己Homにおいて忘却関手`K_AA→K_X`は非忠実**、その`R_0`像上の真正二段商ファイバーは**`Cardinal.aleph0`**。上界は`K_AA→(Bool×Int)×Nat`単射、下界は実Type値塔から。真正C60北六角形でも無条件に成立。**これは`S→K_AA`の非忠実性を示すものではなく、同比較の全域忠実性は引き続き未証明**。

**定理検証正本：** theorem squash SHA＝マージ直後canonical main HEAD `78a4ea2ea9fff4b7b04a0b7076e39e9898d0ffe3`、最終exact-source HEAD `b5096469f96d371df4e52bf7124f9cf9eb5b6ac6`、[CI #41175744716](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41175744716) **Strict Lean 3740/3740 SUCCESS、Governance 5/5 SUCCESS、72件`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[証明と修正理由の詳細](docs/formal/GK4AA-triple-observer-kernel-refinement.md)。Lean v4.30.0-rc2／固定mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107、strict空中心・独立Kuu一presentation、Gray再導入なし、保護PR #1558 Draft/OPEN/未マージを維持。

**次段階GK4AB（未証明）：** 三成分の同一観測値でなお異なる独立構造商類が存在するか、条件付き忠実性が成立するかを真正元F54証拠・seamから判定。元P92Bの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明。

> 以下のGK4Z以前の「最新・次候補」は統合時点の歴史記録。現行定理frontierはGK4AA。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4Z

**最新定理GK4Z [PR #2785](https://github.com/itakura-hidetoshi/KuuOS/pull/2785) MERGED：** [真正逆向きF54物理回転数の不変量](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ZBackwardCountInvariant.lean)・[同一強化観測値の無限残余構造商ファイバー](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ZResidualNonfaithfulness.lean)を新規Lean2ファイル・**40宣言**で証明。元F54の**実Type値`RotationEdge.backward`構成子の個数**を`backwardCount : original DepthRotationRoute → Nat`とし、chain・実Nat cast・縦合成・左右文脈を全て元の依存型のまま検証。**元F55全9構成子、独立元P92B全9構成子（真正associator-naturality含む）、F54構造seam全14構成子、拡張構造比較全3構成子**について個別帰納法で不変性を証明し、元P92B証拠存在商`Q`と独立構造比較商`S`に**それぞれ別個に降下**。元のType値3-cellを観測一致から生成しない。

**GK4X/GK4Y強化観測の残余非忠実性を具体的に証明：** 真正F54前向き＋後向き物理回転backtrack`B`は`rotationCount=2`、`backwardCount=1`、`castCharge=-2`。実`castDepths rfl rfl`を2個加えたbalanced loop`C`は`backwardCount=1`・`castCharge=0`・`rotationCount=2`。元F54証拠経路`R_0=B, R_{k+1}=C;R_k`を構成し、**`backwardCount(R_k)=k+1`、`castCharge(R_k)=-2`、`rotationCount(R_k)=2(k+1)`、`O_X([R_k]_S)=(false,-2)`**を全Nat kでLean証明。後向き回転不変量により`[R_i]_S ≠ [R_j]_S`（i≠j）であり、GK4X/K_Xの実二段目強化観測kernel商では全段**同じ像**。したがって、**実F54 local rotationを持つ任意の文脈で、真正GK4Yの構造圏→強化kernel圏比較関手は非忠実**。真正C60北側六角形では、この**同一強化観測値`(false,-2)`に対応する独立構造商の残余ファイバーは厳密に`Cardinal.aleph0`**と実構造Hom可算性とNat単射から証明。さらに実二段目kernelのある1類へ相異なる構造商類が無限個写ることを構成。この結果は元P92B商`Q`の結合律・単位律、元14D無条件Countable、19D fillerを主張しない。

**検証正本：** 定理squash＝定理マージ直後のcanonical `main` HEAD `f9e0c45fc18d2c1951b1c05579a3b90b87d00e5a`、final exact-source PR HEAD `85e393966e9040cb62c8dbff8eeea6104f912576`、[Strict Lean/Governance #41174633574](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41174633574) **3736/3736 SUCCESS、Governance 5/5 SUCCESS、40新宣言`#print axioms`標準3公理以内・sorryAxなし・変更Lean warning/error 0/0**。[GK4Z定理・修正記録](docs/formal/GK4Z-backward-residual-obstruction.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非導入、保護PR #1558 Draft/OPEN/未マージを維持。

**次段階GK4AA（未証明）：** 逆向き実F54回転数も組み込んだ`(Boolean,castCharge,backwardCount)`を真正P92B商・独立構造商・二段kernel商間の観測関手として検討し、まだ残る情報損失を分類。元P92B結合律・単位律、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明。

> 以下のGK4Y以前の「最新・次候補」は当時の記録。現在の形式化frontierはGK4Z。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4Y

**最新のLean定理統合 GK4Y [PR #2783](https://github.com/itakura-hidetoshi/KuuOS/pull/2783) MERGED：** [真正強化観測kernel圏](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4YEnhancedKernelCategory.lean)と[強化kernel→Boolean kernel忘却関手・可算無限ファイバー](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4YEnhancedKernelForgetful.lean)を**新規Lean2ファイル／39宣言**で形式化。元P92Bの真正Type値証拠存在商`Q`、独立GK4E構造比較商`S`、GK4Sの**相異なる二段目観測kernel商**`K_X = Q/∼_{(Bool,charge)}`と`K_B = Q/∼_{Bool}`を明確に区別。真正F45全型付き境界上で、**Homを実際の`K_X`第二商とする新しいMathlib Category**を構築。合成はGK4S真正到達観測像からの輸送、単位は元P92Bゼロ経路の実二段目商類、結合律は`(b,c)·(d,e)=(b&&d,c+e)`による。元`Q`で未証明の結合律・左右単位を仮定せず、**`K_X`上だけの左右単位律・結合律**をLeanで証明。

**3つの真正関手：** GK4I独立構造圏`S→K_X`比較Mathlib Functor（各Hom全射）、`K_X→Bool×Int`真正観測値Functor（各Hom単射・忠実、真正到達値のみ）、および**別個の二段目商間の`U:K_X→K_B`忘却Functor**（各Hom全射）を構成。対象・射双方で、`S→K_X→Bool×Int`がGK4Xの強化観測関手、`S→K_X→K_B`がGK4Uの旧Boolean関手に**厳密一致**すると証明。`S→K_X`の全域忠実性は未証明のまま。`U`については**すべての実在F45自己Homで非単射／非忠実**と証明。

**新しい可算無限定理：** GK4Wの**真正F54 `castDepths`塔**は`K_X`でも全部異なるが、`U`で全段が**旧Booleanの実ゼロ経路単位商類**に写る。この**真正二段目忘却写像の単位ファイバーは任意の実F45自己stageで厳密に`Cardinal.aleph0`**と形式化。上界は`K_X`から`Bool×Int`への真正単射と固定mathlibの`Function.Injective.countable`、下界はNat添字の実F54塔の単射から導出する。従来必要だったD/Eの全対象・Homの一般Countable仮定はこの結論には不要。真正C60北側六角形は無条件の実例。**これは元P92B商から独立構造商へのファイバーや真正14Dの無条件Countableを証明したものではない**。

定理squash SHA／マージ直後のcanonical `main` HEAD `986398ddace9566ef3df2f9852118a69bef267a8`、最終exact-source PR HEAD `c3adaa17fc3786f5c2fa067452167b270341caaf`、[Strict Lean/Governance CI #41173575821](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41173575821) **3734/3734 SUCCESS、Governance 5/5 SUCCESS、39宣言`#print axioms`標準3公理以内、`sorryAx`なし、変更Lean warning/error 0/0**。[GK4Y証明・検証記録](docs/formal/GK4Y-enhanced-kernel-category-forgetful.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心／独立Kuu一presentation、Grayなし、保護PR #1558 Draft/OPEN/未マージを維持。

**次段階GK4Z（未証明）：** GK4Y強化構造比較関手`S→K_X`の残存faithfulness obstructionを、同一`(Boolean,cast-charge)`観測値を持つ相異なる真正構造商類の有無として調査。真正元P92B結合律・左右単位、歴史的完全Type値同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentには拡張しない。

> 以下のGK4X以前の「最新・次候補」はそれぞれの歴史的スナップショット。現行の定理frontierはGK4Y。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4X

**最新の定理統合 GK4X [PR #2781](https://github.com/itakura-hidetoshi/KuuOS/pull/2781) MERGED：** [GK4X強化観測Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4XEnhancedObserver.lean) と[GK4X型付き関手・真正観測kernel比較Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4XEnhancedFunctor.lean)を新規追加。GK4Wで元F55全9・P92B全9・F54独立構造seam全14・拡張比較全3にわたるType値帰納法で証明した**実cast-charge = original `castDepths`個数 − 物理回転数**を、元P92B証拠存在商`Q`と独立GK4E構造商`S`の**両方へ別々に降下**。両商での原F54合成に対する加法性、`Q→S`の正準射との可換性、構造商単位のcharge 0を証明。元P92Bの未証明の結合律・単位律は使わない。

**真正Boolean×整数の強化観測：** `O_X(s)=(nativeGK4GStructuralGrade(s),nativeGK4XChargeStructural(s)) : Bool×Int` を、`(b,c)·(d,e)=(b&&d,c+e)`・単位`(true,0)`で形式化し、GK4Pの**真の元F54合成・左右文脈観測則**と**独立F54構造seam全保存**をLean証明。GK4Iの元F45依存型構造圏から**独立したBool×Int一対象Mathlib圏への真正Functor**と、旧Boolean圏への忘却Functorを作成し、対象・射の両方で従来のGK4I gradingと厳密に合成一致することを証明。Bool×Int圏は**周囲の値域圏であって真正到達像を無条件に埋め尽くすとは主張しない**。元Qとは別の**GK4S二段目観測kernel商 `K_{O_X}`**に対し、GK4Tの真正`S→K_{O_X}`比較写像、全射、**等式kernel ⇔ 2成分の観測値が一致**、単射性の必要十分条件を証明。これは値が等しいから元P92B Type値3-cellが生まれるという主張ではない。

**真正GK4W cast塔の改善：** `O_X(T_k)=(true,(k:Int))` を全Nat kで証明し、旧Booleanでは全段`true`へ潰れた**相異なる無限個の原F54構造商類**が強化観測、および実二段目`K_{O_X}`で**すべて相異なる**と形式化。具体的cast経路と構造ゼロ経路は旧Boolean値が同じでも強化観測値が異なる。**強化観測が全Homで忠実・全射・圏同値であるとの無条件主張はしていない。**

**証明正本：** theorem squash SHA／定理マージ直後のcanonical `main` HEAD `eaa66af512371fb9c8a051cd565188ec842bc809`、exact-source PR HEAD `36ceae9208e40c6dcb8bf6c6755639a112e8f155`、[Strict Lean・Governance CI #41172335888](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41172335888) **3732/3732 SUCCESS、Governance 5/5 SUCCESS、43新規宣言`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[GK4X検証記録](docs/formal/GK4X-enhanced-typed-observation.md)。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107維持、strict空中心・独立Kuu一presentation、Grayなし、保護PR #1558 Draft/OPEN/未マージ。

**次の研究候補 GK4Y（未証明）：** 真正`K_{O_X}`二段目商の合成・単位をMathlib Categoryへ明示的に構成し、GK4X強化観測との因子化および残余非忠実性を分類。元P92B商の結合律・左右単位・代替合成、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明として保持。

> 以下のGK4W以前の「最新」「次候補」は歴史的スナップショット。現行形式化frontierはGK4Xを優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4W

**最新定理GK4W [PR #2779](https://github.com/itakura-hidetoshi/KuuOS/pull/2779) MERGED：** [真正cast-charge不変量](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4WCastChargeInvariant.lean)・[真正構造商の無限Boolean fiberと非忠実性](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4WCastTowerNonfaithfulness.lean)を新規Lean2ファイルで証明。元F54構成子の**真の`castDepths`個数**と**真の物理回転数**の差を整数不変量 `charge(r)=castCount(r)-rotationCount(r)` として定義。元F55全9構成子（真正pentagonの3対2回転差にはcastも3対2）、新しい元P92B全9構成子（真正associator-naturalityを含む）、別個のF54構造seam全14構成子、拡張構造比較3構成子を**実Type値証拠帰納法**で検証し、chargeが独立GK4E構造比較商で保存されることを証明。元P92Bの3-cellを観測値から生成せず、元Q（証拠存在商）・独立S（構造比較商）・GK4S二段K_Bool（観測kernel商）のauthorityを分離。

**GK4Vで未解決だった忠実性問題を決定：** 実F54の`.castDepths rfl rfl tree`（charge 1、物理回転0）と真の`.chain (.refl tree)`（charge 0、物理回転0）は**構造商`S`では異なる**がGK4G Boolean gradeはともに`true`。GK4Vの`F(u)=F(v) ⇔ grade(u)=grade(v)`を利用し、GK4U構造圏→二段Boolean観測kernel圏の真正関手は**任意の実F45自己Homで非単射（非忠実）**とLean証明。これは元P92B→Boolean商の古い非単射性からの不正な反射ではない。さらに同じ真正castを`k`回合成する元F54 towerを構成し、**`charge(T_k)=k`、全`rotationCount(T_k)=0`、異なる`k`の独立構造商類は相異なる**と証明。真正C60北側六角形のBoolean-true独立構造商ファイバーは、既存の真正構造Hom CountableとこのNat単射から **cardinality `aleph0`** と証明。これは真正14Dの無条件Countableや元Q→Sの各ファイバーの可算性を主張しない。

**検証正本：** 定理squash SHA（マージ直後main HEAD）`a19ae676144ac5f1e40bd9443f43e776afcb9915`、exact-source PR HEAD `86b0ed53f0e214513f02050a34ff1e39d7fd2160`、[Strict Lean/Governance CI #41170191145](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41170191145) **3730/3730 Strict Lean SUCCESS、Governance 5/5 completed SUCCESS、30新規宣言`#print axioms`標準3公理以内、sorryAxなし、変更Lean warning/error 0/0**。[詳細GK4W receipt](docs/formal/GK4W-cast-charge-structural-nonfaithfulness.md)。Lean v4.30.0-rc2・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107維持、strict空中心・独立Kuu一presentation、Gray再導入なし、保護PR #1558 Draft/OPEN/未マージを保持。

**次の研究候補 GK4X（未証明）：** 真正構造商上に降下したcast-chargeとBooleanを組み合わせた**charge強化観測**の合成・単位保存を調べ、何を保ち何を失うかを分類。元P92B商の結合律・左右単位・別合成、歴史的P92B/F19/F28/F54/F55完全型付き同値、真正14D無条件Countable、元19D filler、global strict n、hyperdescentは未証明のまま。

> 以下のGK4V以前の「最新」「次候補」記述は歴史的記録。現行の定理frontierはGK4W。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4V

**最新の定理統合 GK4V [#2777](https://github.com/itakura-hidetoshi/KuuOS/pull/2777) MERGED：** [GK4V観測kernel定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4VBooleanFaithfulnessCriterion.lean)・[GK4V関手とC60判定](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4VBooleanFunctorSectionCriterion.lean)。元P92Bの真正Type値比較存在商`Q`、独立GK4E構造比較商`S`、GK4S二段目Boolean観測kernel商`K_Bool`の権限境界を保持し、**GK4Uの真正比較射`F:S→K_Bool`で`F(u)=F(v) ⇔ grade(u)=grade(v)`**を型付き全F45境界で証明。**`F`の各Homでの単射性 ⇔ 独立構造商GK4G Boolean gradingの同一Hom上の単射性**を確定。実際の`K_Bool`からGK4I一対象Boolean圏へのMathlib関手を構成して**各Homで単射**と証明し、GK4U比較関手と合成した際、GK4Iの既存Boolean gradingと**対象・射写像で厳密に一致**することを証明。これによって元P92B→Boolean kernel商の既知の非単射性を、独立構造商→kernel商の非単射性へ誤って反射しない。

**真正C60北側F45 tripleの完全判定条件：** GK4Gの**真正zero-route unit塔（true）と2物理回転backtrack（false）**からなる実Boolean sectionが全構造商自己Homを復元できることと、GK4U比較関手のそのHomにおける単射性が**必要十分**。実2射は構造商において異なるBoolean gradeを持ち、GK4Vでも像が異なることを証明。**同一Boolean gradeで異なる構造商2射の存在、または2sectionによる全構造商復元は未証明**なので、忠実・不忠実いずれも無条件には結論しない。これは型付きno-goの未解消のobstructionを正確に局所化した成果。

定理squash SHA＝直後のcanonical `main` HEAD `77c70548e85aa55d1fb958d9d1a4c8bb40b148a9`、exact-source HEAD `c62b8e8194d5b2cf583eb8b21d17e5990938fd59`、[CI #41169230707](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41169230707) **Strict Lean 3728/3728 SUCCESS・Governance 5/5 completed SUCCESS**。追加16宣言は`#print axioms`で`propext`・`Classical.choice`・`Quot.sound`以内、`sorryAx`なし、変更Lean warning/error 0/0。[GK4V検証記録](docs/formal/GK4V-boolean-faithfulness-criterion.md)。公開root107、Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft/OPEN/未マージを維持。

**次の研究候補 GK4W（未証明）：** 真正F54構造商内の**同一Boolean grade・異なる2射**の構成、あるいは既存2sectionによるHom全域復元を、元Type値証拠の全構成子と幾何を保持して検証。元P92B結合律・左右単位・別合成、歴史的型付き完全同値、真正14D無条件Countable、元19D filler、global strict n・hyperdescentは未証明として保持。

> 以下のGK4U以前の「最新」「次段階」は歴史的記録。現行の定理frontierはGK4Vを優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4U

**最新の定理統合 GK4U [#2775](https://github.com/itakura-hidetoshi/KuuOS/pull/2775) MERGED：** [Lean定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4UCompositionalKernelFunctor.lean) で、元P92B証拠存在商`Q`、独立GK4E構造比較商`S`、GK4S観測kernel二段目商`K_O`の**3種類のauthorityを同一視せず**、元GK4Hの真正合成保存射影`π:Q→S`とGK4Sの合成保存射影`κ:Q→K_O`の双方と可換な任意の比較写像`F:S→K_O`が**必然的に合成を保存**すると証明。GK4Pの真正F54合成・左右文脈観測則の下で、任意の真のF45三境界に対する**合成保存比較写像3つの存在 iff 全3境界でGK4Nの全真正Type値F54構造seam保存**という必要十分条件を形式化。合成整合性のための追加障害を偽って仮定しない。構造商の真正単位は比較写像で**元P92Bゼロ経路の観測kernel類**へ写るが、元P92Bの単位律は主張しない。

**Boolean観測の真正関手化：** GK4SのBoolean kernel商をHomとし、**GK4I元F45依存型stageを別の対象型で包んだ独立Mathlib Category**を構成。観測値域の`Bool.and`の結合律とGK4Rの真正到達像における左右単位律をGK4S同値経由で輸送し、圏の3公理を証明。GK4Iの独立構造比較圏からこのBoolean観測kernel圏への**真正Mathlib Functor**を構成して、各真正Homの射写像が**全射（full on every Hom）**と証明。これは忠実性・圏同値・元Type値P92B証拠復元を意味しない。GK4K `Option Nat`観測は元F54左単位seamの`some 2 ≠ some 1`によって、真正F45自己Homで三境界合成比較さえ存在しない。真正C60北側六角形F45 tripleでも**無条件の関手全射性／Option障害対照**を確定。

定理squash SHA＝直後のcanonical main HEAD `cee82f700c0040c179bacc7b586c6abfa8e3f806`、exact-source HEAD `a55d680488c5c9ac277fa9c5517eb821e845ea72`、[CI #41167812738](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41167812738) **Strict Lean 3726/3726 SUCCESS、Governance 5/5 completed SUCCESS**。新規19宣言`#print axioms`で標準`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし、変更Lean warning/error **0/0**。[GK4U検証記録](docs/formal/GK4U-compositional-kernel-functor.md)。公開root107、Lean v4.30.0-rc2・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、strict空中心／独立Kuu一presentation、no Gray、保護PR #1558 Draft/OPEN/未マージを維持。

**次の研究候補 GK4V（未証明）：** Boolean比較関手の忠実性障害を真正F54構造商の具体的な異なる類で判定し、GK4IのBoolean grading functorとの正確な関係を検討。元P92B商の結合律・左右単位、別合成、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明のまま。

> 以下のGK4T以前の「最新」「次候補」は歴史的スナップショットとして保持。現在の定理frontierはこのGK4Uを優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4T

**最新の定理統合 GK4T [#2773](https://github.com/itakura-hidetoshi/KuuOS/pull/2773) MERGED：** [新規Lean定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4TStructuralKernelComparison.lean) は、真正元P92B証拠存在商 `Q`、独立GK4E構造比較商 `S`、GK4Sの二段目観測kernel商 `K_O=Q/∼_O`という**相異なる3種類のauthority**を維持し、正準全射`π:Q→S`と`κ:Q→K_O`を可換にする比較写像`F:S→K_O`について、**存在 ⇔ 任意の真正F54 Type値構造seamで観測値が等しい（全14生成子の保存）**を証明。GK4Lの真正πファイバー一定性、GK4Nの任意B値観測降下必要十分条件、GK4Sの観測kernel商等式判定を連結し、`Quotient.lift`で比較写像を**代表元の恣意的選択なしに構成**。GK4E正準全射による一意性、`∃!`必要十分条件、比較写像の全射、**単射 ⇔ 観測等式が独立構造商等式を反映**、GK4Qの真正到達観測像への可換三角形も形式化。**真正GK4G Booleanでは全F45境界で比較写像が一意に存在するが、GK4K `Option Nat`では真正F54左単位seamの`some 2 ≠ some 1`により任意の実F45自己stageで存在しない**。真正C60北側六角形で無条件対照と、元P92B→Boolean kernel商の**非単射性**を同時に証明。これは元P92Bの結合律・単位律、元P92B Type値3-cellの観測値からの生成、独立構造商と観測kernel商の無条件同型を主張しない。

定理squash SHA＝マージ直後のcanonical `main` HEAD `74a22a0dfe54e253740a82374dca41240a0c93d9`、exact-source HEAD `e02ea84432050d55bc6672339d049a8bb6189bc0`、[CI #41166852221](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41166852221) **Strict Lean 3725/3725 SUCCESS／Governance 5/5 completed SUCCESS**。新規17宣言の`#print axioms`は`propext`・`Classical.choice`・`Quot.sound`以内、`sorryAx`なし、変更Lean warning/error **0/0**。[GK4T検証記録](docs/formal/GK4T-structural-to-kernel-comparison.md)を追加。公開root107維持、Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、strict空中心・独立Kuuは一presentation、Gray非再導入、保護PR #1558 Draft/OPEN/未マージを維持。

**後続研究候補（未証明）：** 構造商と観測kernel商での合成の整合性を、独立GK4Iの真正構造合成およびGK4P/GK4Sの観測則に対する明示的な条件付き主張として検討。元P92B商の結合律・左右単位、別合成、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明。

> 以下のGK4S以前の「最新」「次候補」記載はそれぞれの歴史的スナップショットとして保持。現行frontierはこのGK4Tを優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4S

**最新の定理統合 GK4S [#2771](https://github.com/itakura-hidetoshi/KuuOS/pull/2771) MERGED：** [Lean定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4SObserverKernelImageEquiv.lean) で、元F55/P92Bの**真正証拠存在商**の任意B値観測`O`について、独立D/Eカテゴリー・全Blocks・二Nat深さを保持した各F45境界上で、観測kernel関係`q∼r ⇔ O(q)=O(r)`を真正Setoidとして定義。その**元P92B商を更に観測kernelで割った二段目の商**`Q/∼_O`とGK4Qの**真正到達観測像**`Im(O)`の型付き同値 `Q/∼_O ≃ Im(O)` を、正準射・単射・全射の厳密証明から構成。**任意の型Cへの観測kernel因子分解の存在⇔観測値の等しいP92B類で写像値も等しい**を必要十分条件として証明し、因子の一意性も確定。GK4Pの真正合成観測則を用いて二段目の商にGK4Q像上の合成を輸送し、元GK4H P92B合成の射影整合性と、値域演算が結合的な場合の**二段目商上でのみの結合律**を証明。GK4Hの真正左単位障害が示す**異なる元P92B類の同一Boolean観測**から、元P92B→Boolean観測kernel商の正準射はすべての実F45 stageで**単射でない**と示し、真正C60北側六角形でも無条件例を確定。**観測値の等しさから元Type値P92B 3-cellを生成しない。二段目の観測kernel商は独立GK4E構造比較商とは別物であり、観測商の結合律・単位律を元P92Bへ反射しない。** 定理squash SHA `fb4508617d2561c31fd41ffd9927881e7b2c3148`、exact-source HEAD `deed48339f16e80dc27e2cddf0d653cf62c12313`、[CI #41165728126](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41165728126) **Strict Lean 3724/3724 SUCCESS・Governance 5/5 completed SUCCESS**、新規17宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。[GK4S検証記録](docs/formal/GK4S-observer-kernel-image-equivalence.md)を追加。

**次の研究候補 GK4T（未実装）：** **GK4Eの真正独立F54構造比較商 → 元P92B観測kernel二段目商**という向きの比較写像が存在する必要十分条件を、GK4Nの真正seam保存条件と接続して証明。Boolean観測では可能で、GK4K `Option Nat`では真正左単位seamが阻害するという対照を正確に述べる。元P92B結合律・単位、完全Type値同型、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明。strict空中心／独立Kuu一presentation、固定Lean/mathlib pin、公開root107、保護PR #1558 Draft/OPEN/未マージを維持。

> 以下のGK4R以前の「最新」「次段階」表記は当時の歴史的研究スナップショットとして保持。現在の定理frontierはこのGK4Sを優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4R

**最新の定理統合 GK4R [#2769](https://github.com/itakura-hidetoshi/KuuOS/pull/2769) MERGED：** [Lean定理](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4RObservedUnitsVsSourceNoGo.lean) で、GK4Qの真正P92B商由来到達観測像に対し、**GK4G Boolean像は結合律と左右単位を満たす**一方、**GK4K `Option Nat`像は結合律を満たすが左右単位が存在しない**ことをLean4で形式化した。Boolean像の単位は真の元P92Bゼロ経路 `nativeGK4H_p92Unit` の観測値`true`であり、任意の実F45境界の左右で単位として作用する。しかし**元P92B商そのものでは、任意候補の左右単位不存在（GK4J）が保持される**。非忠実な観測は単位律を元商へ反射しない。GK4K `Option Nat`像は`some 0`を含まず、真正GK4D単位塔から`some 1`を含む。任意の候補`none`は吸収的で、`some n (n>0)`は`some 1`との合成が`some(n+1)`になるので、左右単位候補はすべて排除される。真正物理C60北側六角形でも無条件の対照定理を証明。**像上の結合律は元P92B商の結合律の証明ではなく、元Type値3-cellや独立構造商と混同しない。** 定理squash SHA `02ababa76701f85f8b67812da8b49687fe17d127`、exact-source HEAD `966409d715e677cc86555cab2912ee16384ac6a6`、[CI #41164652884](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41164652884) **Strict Lean 3723/3723 SUCCESS・Governance 5/5 completed SUCCESS**、19宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。[詳細なGK4R検証記録](docs/formal/GK4R-observed-unit-contrast.md)。

**次の研究候補 GK4S（未実装）：** GK4Q観測像と元P92B商を観測kernelで割った真正商との同値・普遍性を型付きで確立し、像での代数則が元商へ反射しない正確な障害を追う。元P92B結合律・単位、完全歴史的Type値同型、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明を維持。strict空中心、独立Kuu一presentation、Lean/mathlib pin、公開root 107、保護PR #1558 Draft/OPEN/未マージを維持。

> 以下のGK4Q以前を「最新」と呼ぶ記載は、その時点の研究履歴として保持。現行の定理正本は本GK4R段落を優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4Q

**最新の定理統合 GK4Q [#2767](https://github.com/itakura-hidetoshi/KuuOS/pull/2767)：** [GK4Q Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4QDependentObservationImage.lean) は、元P92B商の任意の型付き観測関数族の**真正到達像**を各F45境界で構成し、その射影の全射性を証明。GK4Pの真正F54合成・左右文脈の3観測則から、GK4Hの**実P92B商合成**とP93の**実左右文脈作用**を観測像上へ誘導し、3作用の射影整合性・一意性を示した。値側の演算が結合的な場合は**像上のみ**結合律が成立する。これは元P92B商の結合律・単位律の証明ではない。GK4K実`Option Nat`像は`some 0`を含まず、構造商への降下は真正F54単位seamで引き続き阻害される。定理squash SHA＝現証明正本 `454d4c6a5c9b42b93bab6191a3d0c6043fd8a1a2`、exact-source `5f66b13637b6a905486b627b6a27872235a441f4`、[CI #41163191778](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41163191778) **Strict Lean 3722/3722・Governance 5/5 SUCCESS**、17宣言`#print axioms`、`sorryAx`なし、変更ファイルwarning/error 0/0。詳細は[GK4Q検証記録](docs/formal/GK4Q-dependent-observer-image.md)。

**直前の定理統合 GK4P [#2765](https://github.com/itakura-hidetoshi/KuuOS/pull/2765)：** [GK4P Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4PCompositionalObserverKernel.lean) は、真正F54合成・左右文脈の3観測則から、GK4Oで明示仮定とした**4つの等式kernel互換性**を導いた。これらの条件下で真正構造商への降下は基本7seam保存と必要十分。GK4G Boolean観測とGK4K `Option Nat`観測はともにkernel互換だが、後者は真正左単位seamの`some 2 ≠ some 1`によって**降下しない**。PR #2765 squash `ffba5bbc8934c9e3d2a2a4a1367b2e5a9cc2419f`、Strict Lean 3721/3721 SUCCESS。成果記録 [GK4P](docs/formal/GK4P-compositional-observer-kernel.md)。

**最新正本の境界：** strict空を中心に、独立Kuuは一つのpresentation。元Type値のF55/P92B比較と独立GK4E構造比較商を混同しない。公開root 107維持、Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft/open/unmerged。元P92B結合律・単位、真正14Dの無条件Countable、19D filler、global strict n、hyperdescentは未証明。**次の研究候補 GK4R**は像上の単位の存在/障害を元商と区別して精密化すること。

> 以下の「GK4O」を最新と呼ぶ記述や旧「次のGK4P」予定は、その時点の歴史的研究記録として保持する。現在の到達点は本GK4Q段落を優先する。

---

## 最新の研究状態 — 2026-10-31 JST / F112-P94D3GK4O

**最新の定理統合 GK4O [#2763](https://github.com/itakura-hidetoshi/KuuOS/pull/2763)：** GK4Nの**任意の元P92B商B値観測が独立構造商へ降下する必要十分条件＝全14真正F54 Type値構造seamの保存**を、型付き文脈間の観測関数族に拡張して整理した。真のF54 StructuralSeam全14のうち、**基本生成子7種類（reassoc・leftUnit・rightUnit・leftContextTrans・rightContextTrans・leftContextUnit・rightContextUnit）**を選び、残る反射・対称・推移3種類は等式の一般法則、前合成・後合成・左右context合同4種類は**観測値の等式kernelに対する4つの明示的な輸送互換条件**から導く。これら**4つのkernel compatibilityを追加仮定として明示した場合に限り**、`全14 seam保存 ⇔ 基本7 seam保存`を原F54 Type値seam全構成子の完全依存型帰納法で証明。さらにGK4Nの真正GK4E正準商全射による降下必要十分条件へ接続し、**同じ明示仮定の下で観測関数族の全境界での構造商降下 ⇔ 基本7条件**を確定。単一F45境界では左右contextが境界・Blocksを変更するため、**全F45・全Blocks・二Nat深さにわたる元P92B証拠存在商の観測関数族**を実際に定義。真のGK4G Boolean観測は全構造seamを保存し構造商へ降下する。一方、元GK4Kの`Option Nat`原始項数観測は、**真正F54左単位seamただ一つで`some 2≠some 1`となり、基本7条件の段階で既に不成立**。真正C60北側六角形F45三重Treeでも元GK4Nの局所obstructionが無条件に成立。**4つのkernel compatibilityが任意の観測に自動成立するとは主張せず、7生成子が最小であることも未証明**。元P92B結合律・別合成、歴史的完全型付き同型、真正14D無条件Countable、元19D filler、global strict n・hyperdescentは未証明。定理squash SHA `1370dce5a2a55a89ad4758911aea23597ce34050`、exact-source HEAD `b18ced002802ff865966c8a5e7a29501bd19a227`、[Strict Lean/Governance #41159766444](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41159766444) **3720/3720 scoped SUCCESS・Governance 5/5 completed SUCCESS**、新規17宣言公理依存`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。

**直前の定理統合 GK4N [#2761](https://github.com/itakura-hidetoshi/KuuOS/pull/2761)：** GK4Lの真正GK4E正準全射 `π:元P92B証拠存在商→独立F54構造比較商` に対し、**任意の値域型`B`・任意の元P92B商上の観測`O:P→B`が独立構造商へ降下する必要十分条件**をLean4で証明した。正確には、**`∃F:S→B, F∘π=O`であることと、あらゆる真正Type値F54構造seam `w:r⇒s` について `O([r])=O([s])`が成立することが同値**。元P92B証拠存在商上の観測はすでに元P92Bの全比較を保存するため、新しく検査すべき条件は**真正F54 StructuralSeam全14構成子**のみ。独立F55 StructuralComparisonの**元P92B・真正F54構造seam・推移合成の3構成子全体**について原Type値証拠帰納法で保存を証明し、GK4Lの全ファイバー一定性条件を使って厳密な商降下を構成。正準全射による**降下因子の一意性**も証明。さらに、元P92B商を取る前の**任意の生F54経路観測**については、**元P92B Type値比較とF54構造seamの両生成子族の保存が、構造商への降下と必要十分**と形式化した。GK4Gの物理回転数0/正Boolean gradeは全構造seamを保存する一方、**ただ一つの真正F54左単位seam**でGK4Kの原始項数`Option Nat`観測の`some 2`と`some 1`が分離し、降下不能の明示的局所obstructionになる。真正C60北六角形F45 tripleでいずれも無条件に成立。**対象は固定したGK4E独立構造商への降下であり、元P92B商の結合律、別合成、歴史的完全型付き同型、真正14D Countable、19D filler、global strict n・hyperdescentは未証明**。定理squash SHA `76eaf1c6c0ccb86ce7fd5e9e44ee74b9330df6d0`、exact-source HEAD `a1716b21a09bc70af3b41969590db93596ec5e65`、[Strict Lean/Governance #41158003474](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41158003474) **3719/3719 scoped SUCCESS・Governance 5/5 completed SUCCESS**、新規13宣言公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。

**直前の定理統合 GK4M [#2759](https://github.com/itakura-hidetoshi/KuuOS/pull/2759)：** GK4Lの真正GK4E正準全射`π : 元P92B証拠存在商 → 独立F54構造比較商`とGK4Kの条件付き原始項数`Option Nat`観測`O`に関して、**任意の行き先型`B`・任意の後処理`f : Option Nat → B`が`f ∘ O`として構造商へ降下する必要十分条件**を形式化した。正確には、任意の実在元F45自己経路stageにおいて **`∃ F, F ∘ π = f ∘ O ↔ ∀ n>0, f(some n)=f(some 1)`**。同値な正整数ペア間の値の完全一致条件も証明。必要性は**真正GK4D原F54単位塔`T_k`が全段同じ独立構造商類に落ちるが、観測`O([T_k])=some(k+1)`は全段異なる**ことから従う。十分性はGK4Gの**本物の構造商Boolean grading**を使い、`true↦f(some 1)`・`false↦f(none)`という具体的な二値写像を構成して証明。構造商への降下写像は**正準全射性により一意**で、任意の成立する候補はこのBoolean因子に一致する。`Option.isSome`は実際に降下し、GK4Kの`Option Nat`恒等後処理は降下不能。真正物理C60北側六角形F45 stageでも無条件に成立。**これはGK4Kの`Option Nat`に後処理を施した観測に限る完全分類であり、任意の原P92B観測全体がBooleanに限られることは主張しない**。原P92B結合律・別合成、歴史的P92B/F19/F28/F54/F55完全型付き同型、真正14D無条件Countable、元19D filler、global strict n・hyperdescentは未証明として保持。定理squash SHA `36e13ca4f961a9a528d5592878a60cb2cd2e4fe1`、exact-source HEAD `f533b3973981384ea3b06c524f9ee142d936fb4e`、[Strict Lean/Governance #41157123830](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41157123830) **3718/3718 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**。新規13宣言の公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。

**直前の定理統合 GK4L [#2757](https://github.com/itakura-hidetoshi/KuuOS/pull/2757)：** GK4Kが元P92B商で構成した**真正0物理回転の`Option Nat`原始項数観測**は、GK4Eの**元P92B証拠存在商→独立F54構造比較商**の実際の正準全射を通じては**決して降下できない**ことをLean4で証明。一般の型`B`への観測が正準全射に沿って降下する**必要十分条件＝各構造商ファイバー上で値が一定**を証明。元GK4D真正ゼロ回転単位塔`T_k`の原始項数は正確に`L(T_k)=k+1`、GK4K観測は`some(k+1)`となる。塔の全段は元GK4Dの真正F54左単位seamにより**同じ独立構造商類**へ写るが、観測値は全段で異なり、一つの構造商ファイバーには無限個の相異なる`some`値が残る。したがって**いかなる構造商上の`Option Nat`関数でも、元GK4K観測を正準全射で引き戻すことは不可能**。任意の実在F45 stageで`some n`が原P92B自己経路商で達成されるのは**ちょうど`n>0`**の場合と証明し、`none`の全stage存在は主張しない。対照的にGK4Gの**真の原始回転0/正の`Bool` gradeは構造商へ降下**できる。真正C60北側六角形F45 tripleで無条件のno-goを具体化。**これはこのGK4K観測とGK4E構造商に関する障害であり、すべての観測の降下不能、元P92Bの別合成・結合律、歴史的型付き同型、真正14D Countable、19D filler、global strict n・hyperdescentを示さない**。定理squash SHA `b8ba6b09cb37239e4f25d7ef66cafad3565596f4`、exact-source HEAD `c97c947ed2e80683a425848ca1b9eea90d13ea4c`、[Strict Lean/Governance #41156497624](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41156497624) **3717/3717 scoped SUCCESS・Governance 5/5 completed SUCCESS**、新規13宣言公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。

**直前の定理統合 GK4K [#2755](https://github.com/itakura-hidetoshi/KuuOS/pull/2755)：** GK4Jの真正元F54原始経路項数 `L(r)>0`・真正合成加法性、および元F55/P92B全9構成子の**真の物理原始回転数0に限るL保存**を、真正元P92B存在商上の**well-definedな`Option Nat`観測**へ降下させた。`R(r)=0`では`some (L(r))`、`R(r)>0`では`none`とし、元P92B比較の任意の真のType値証拠に関して代表元独立である。観測の一意性、`Option.isSome`とGK4G Bool gradeの完全一致、`some n`の厳密正値`n>0`、任意F45商Homに`some 0`が存在しないことを証明。GK4Hの**真正F54由来P92B商合成**は`some a ⋆ some b = some (a+b)`・`none`両側吸収のOption演算に厳密整合し、独立C60北六角形F45 Treeへ無条件に具体化した。`Option Nat`を原P92B商の別合成と取り違えず、正回転pentagonの項数保存、元P92B商の結合律、別合成の不存在、真正14D無条件可算性、19D filler、global strict n・hyperdescentは主張しない。**定理squash SHA `ef9e69c982706985a6dadfd72bd1199dde1531dd`、exact-source HEAD `c6e841c85a3a61ce0f65dfde3ee2a87c8319f3e4`、[Strict Lean/Governance #41155697783](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41155697783) 3716/3716 SUCCESS・Governance 5/5 completed SUCCESS、19宣言の公理依存は`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error 0/0。**

**最新の定理統合 GK4J [#2753](https://github.com/itakura-hidetoshi/KuuOS/pull/2753)：** GK4Hで証明した「元P92B商の**指定された真正F54ゼロ回転鎖は左右単位にならない**」という結果を、**どの元P92B同値類を選んでも真正F54由来の既存商合成の左右単位になれない**という候補独立のno-goへ強化した。単純なGK4Cゼロ鎖原子数だけでは、元F54の`castDepths rfl rfl`のように**原始回転数0・ゼロ鎖原子数0**の元証拠を排除できないため、真の元F54の**原始経路項数**`gk4jLeafCount`を新たに定義した。元`chain`および明示的な両Nat`castDepths`をそれぞれ原始項1個、`trans`を加法、左右contextを項数保存として完全依存型のまま定義し、**任意の元F54経路の項数は必ず正**と証明。真の元F55 9構成子・別元P92B 9構成子について、**真の物理回転数0という明示条件下では原始項数が保存**されることを元Type値証拠帰納法で形式化した。pentagon（3対2回転）、square（2対2回転）、新`assocNaturality`（真の+1 associatorを含む）は物理回転数0の境界に出現しないため、正回転のpentagonでの**全域的な原始項数保存は一切主張しない**。任意の原P92B商類`e`が左単位なら、実元F54`chain(refl tree)`との比較から`L(e)+1=1`が強制されるが、全元F54経路で`L(e)>0`により不可能。右単位についても独立に証明し、**両側単位候補・元F45 stage全体への一括単位割当の不存在**を確定した。真正C60北側六角形F45三重Treeでは**候補によらない無条件の左右単位不成立**と、別GK4I構造商の真正左右単位成立を同一型付き境界で対照。対象D/E・全Hom可算性はこのno-goには仮定不要。**否定はGK4Hの既存の真正F54由来P92B商合成に対してであり、別の合成の可能性、元P92B結合律、歴史的完全型付き同型、真正14D Countable、19D filler、高次descentを否定・証明したものではない**。定理squash SHA `daa94823b410ce5a1a31004b72d01951af8a6420`、exact-source HEAD `011d56a8496acf89c5c1619d926e784ee3dadfc0`。[Strict Lean/Governance #41150002368](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41150002368) **3715/3715 scoped SUCCESS・Governance 5/5 completed SUCCESS**。新規14宣言の公理依存は`propext`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。


**先行する構造圏構成 GK4I [#2751](https://github.com/itakura-hidetoshi/KuuOS/pull/2751)：** GK4Hの完全原F54構造比較商上の**依存型合成・結合律・左右単位律**を、mathlib `Category`の全公理へ統合した。対象`NativeGK4IStage`は選択したPolygon `p`、**独立D/Eカテゴリーの固定した真正原`ma/pa/mb/pb` Blocks**境界の下で、二つのNat深さ`n,m`と**完全な元`KuuNativeF45Tree p n m ma pa mb pb` Type値証拠**を保持するΣ型。射`NativeGK4IStructuralHom X Y`は同一の完全F45境界を持つ既存GK4Eの**`NativeF55StructuralComparison`元Type値証拠の存在を条件とする商**であり、raw F54経路そのものや3-cell証明Typeではない。`Category`の`id/comp/id_comp/comp_id/assoc`はGK4Hで元F54の実`reassoc/leftUnit/rightUnit`構造seamを使って独立に証明された演算・法則を直接継承し、新しい証拠や公理は仮定していない。さらに新しい**単一対象・Hom=`Bool`・単位=`true`・合成=`&&`**のmathlib圏を構成し、GK4Gの真のF54原始回転数0/正に基づく構造商Boolグレードが、**mathlibの本物の`Functor`**を定義することを、GK4Hの厳密合成乗法則と元F54ゼロ回転単位から証明した。**真正C60北六角形の元F45三重Tree**をこの実圏の対象とし、真の正逆2回転閉路を同対象の射として構成。関手は単位射を`true`、2回転閉路を`false`へ写すため非定数である。一般D/Eでは対象と**全HomファイバーのCountableを明示仮定**すると全構造HomがCountableで、真正C60 `Site×Site`北六角形では追加仮定なし。**元P92B witness-existence商は選んだ真正原F54ゼロ鎖の左右単位律を満たさない**というGK4Hのno-goを物理C60対象で併記し、そこへこの新しい構造圏インスタンスを誤移植しない。Bool関手のfaithfulnessや同値、構造商全体がBoolと同型、歴史的型付き同型、真正14D Countable、19D filler、高次hyperdescentは未証明。定理squash SHA `052ef7094b50721fbb06124fc7a1f7ab820b72df`、exact-source HEAD `ee1612fac5d26c08fbd22f1bf4223f9cff1f677b`。[Strict Lean/Governance #41148243850](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41148243850) **3714/3714 scoped SUCCESS・Governance 5/5 completed SUCCESS**。新規14宣言の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。


**先行する商の合成証明 GK4H [#2749](https://github.com/itakura-hidetoshi/KuuOS/pull/2749)：** GK4Gで**元F54真の原始回転数0/正**から厳密に降下させたBool値グレードを、**両Nat深さ・D/E独立カテゴリー・原Blocks・任意中間元F45 Treeを保持する真正F54縦合成**へ拡張した。真の回転数加法`rotationCount(trans u v)=rotationCount(u)+rotationCount(v)`により、**元raw証拠で`grade(u∘v)=grade(u) && grade(v)`**をLean4で証明。さらに**元P92B 9構成子の実`precompose/postcompose`**から、既存の元P92B witness-existence商上の**完全依存型合成**を`Quotient.liftOn₂`で構成した。別`NativeF55StructuralComparison`は独立の元3構成子`original/structural/trans`からなるため、元P92B pre/post と**真正元F54 StructuralSeam pre/post**の両方を使い、型値のpre/post輸送を3構成子へ再帰定義して別の構造比較商上にもwell-definedな合成を構成。**両商のBoolグレードはそれぞれ合成に対し`and`で乗法的、GK4E正準商全射は両商の合成を厳密保存**する。一方、独立の真正F54構造seam`reassoc/leftUnit/rightUnit`は**構造商の結合律と左右単位律**を与えるが、元P92B商ではGK4Cの証明により、**真正F54ゼロ鎖を単位とすると左右単位律は不成立**。左単位を挿入した後の元P92B商類と元類は**Boolグレードが厳密に一致するにもかかわらず、実際には異なる類**である。これを真正C60北側六角形の同一F45 tripleへ無条件に特殊化した。これは**構造商上の合成と元P92B商上の合成がそれぞれ定義できること**を述べるが、P92B商の結合律・単位律や歴史的型付き同型は主張しない。定理squash SHA `af35c85fe8c562c572f18fc4c14c333b4d1b1fcf`、exact-source HEAD `5041777925136ff9b9fba2e39f5f7d99dafc58e3`。[Strict Lean/Governance #41144576565](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41144576565) **3713/3713 scoped SUCCESS・Governance 5/5 completed SUCCESS**、新規21宣言の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。


**先行するBool降下 GK4G [#2747](https://github.com/itakura-hidetoshi/KuuOS/pull/2747)：** GK4Fの「真正元F54回転数が0か正か」の保存則を、**元P92B witness-existence商**と、別の**元F55 StructuralComparison witness-existence商**の双方に**原Type値境界を保持したままBool値グレーディングとして降下**した。任意の元F54経路`r`のグレードは`decide (r.rotationCount = 0)`であり、元P92B商から構造商へのGK4E正準全射`π`と厳密に`gradeP92B = gradeStructural ∘ π`が可換であることをLean4で証明した。構造商からBoolへの関数が全元F54代表経路で同じグレード値をとるならその降下は一意。さらに**実在する原F54 `LocalRotation`の証拠**から、真正0回転`chain(refl)`と真正正逆2回転backtrackを使い、両商にBoolからの明示sectionを構成し、`grade ∘ section = id_Bool`（Leanの`Function.LeftInverse grade section`）および二つのsectionと正準商全射の可換性を証明した。**これはグレードの分裂全射であり、構造商をBoolと同型にしたわけではない**。GK4Dの0回転unit塔とGK4Fの正回転backtrack塔の原P92B類を、二つの**グレードの全ファイバー**へそれぞれ単射し、GIの完全元証拠`DepthRotationRoute`可算性による上界と合わせ、**P92B商のBool=true/false両ファイバー全体がそれぞれ正確に`Cardinal.aleph0`**であると証明した。一般D/Eでは**対象および全HomファイバーのCountableを明示仮定**し、真正C60北側六角形の同一F45 tripleでは無条件。構造商自体は一般D/Eの明示条件でCountable、真正C60では無条件CountableでBoolへ全射するが、構造商全体の正確な濃度、残るF54 seam個別P92B充填、真正14D可算性やhigher fillerは導いていない。定理squash SHA `2c36b61edd36cb25002b5973129909a838a96881`、PR exact-source HEAD `a6f31151a4f101f2e99ecdb745fe5b10cfdbfe2d`。[Strict Lean/Governance #41143104538](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41143104538) **3712/3712 scoped SUCCESS・Governance 5/5 completed SUCCESS**、新規28宣言の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内、`sorryAx`なし、変更Lean warning/error **0/0**。


**直前の証明 GK4F [#2745](https://github.com/itakura-hidetoshi/KuuOS/pull/2745)：** 実際の元F54局所回転`LocalRotation`を**正方向→同じ元証拠に由来する逆方向**へ辿る原`RotationChain`二辺の閉路を構成した。元F55 `PresentedCell`の全9構成子、元P92Bの全9構成子（新`assocNaturality`を含む）、別`NativeF55StructuralComparison`全3構成子について、**本物のF54原始回転数が0か正か**を元証拠帰納法で保存することをLean4で証明。五角形の原回転数3対2を「数が等しい」と誤認せず、いずれも正であることを用いた。GK4Eで定義済みの真の構造比較商では、**ゼロ回転unit経路の類と、2回転backtrack経路の類は異なる**ため、その商は**非一点**である。さらに2回転backtrackにGK4Dのゼロ鎖塔を後合成し、元F54 `precompose/rightUnit/trans`による真のseamを構成。全段は同じ**第二の構造同値類**へ写る一方、異なる段の元P92B比較はUnitCountの保存により不存在。従って**異なる二つの構造商同値類の逆像それぞれに、正確に`Cardinal.aleph0`個の元P92B同値類**が存在する（一般D/Eでは対象・各Hom-fiberのCountableを明示仮定）。真正C60北側六角形の**同一のF45 triple**`node(node t₀ t₁)t₂`上では両ファイバーが無条件に可算無限で、2構造類の不一致もLean4で実証。**構造比較商全体の濃度を確定したものではない**。定理squash SHA `171667d16ac7cc475606f38d8049d30cdeb0db48`、exact-source HEAD `c090f5b1be6a13cc255656167450c4b58dc9015d`。[Strict Lean/Governance #41141435726](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41141435726) **3711/3711 scoped SUCCESS、Governance 5/5 completed SUCCESS**。新規17宣言は標準`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。

**直前の商の比較 GK4E [#2744](https://github.com/itakura-hidetoshi/KuuOS/pull/2744)：** 真の元P92B証拠存在からなる既存`nativeF55P92AssocRouteSetoid`と別の原`NativeF55StructuralComparison`存在からなる真の構造比較商を、同じ完全依存型元F45/F54境界で定義した。原P92B inclusionからの**商間の正準写像が全射であり単射ではない**ことを、GK4Dの無限unit証拠列と元Type値構造seamによって証明。一般D/Eの対象・各Hom-fiberのCountable条件下で元P92B自己経路**商全体**の濃度と、**一つの指定した構造同値類の逆像**の濃度を厳密に`Cardinal.aleph0`と証明し、真正C60北側六角形で無条件に特殊化。構造商自体がsingletonであると主張しない。定理squash SHA `c7707c7ebd7007e1a9c69226e5716804968b78ca`、exact-source HEAD `a8829dce24d8f3ddfb45c8eac073b7f928d509a8`。[CI #41140145072](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41140145072) **3710/3710 scoped SUCCESS、Governance 5/5 SUCCESS**。18宣言の公理依存は標準3公理以内・sorryAxなし。


**先行する無限元証拠塔 GK4D [#2742](https://github.com/itakura-hidetoshi/KuuOS/pull/2742)：** 任意の真正元F45 Tree `tree` について、元F54の真のゼロ回転鎖を反復して、両端点・元D/Eカテゴリー・原Blocks・二つのNat深さを保つ完全元Type値自己経路列 `T₀=chain(refl tree)`、`Tₙ₊₁=trans(chain(refl tree),Tₙ)` をLean4で構成し、GK4Cで証明した元P92B全9構成子保存の原子個数に対して `gk4cUnitCount(Tₙ)=n+1` を厳密に証明した。従って `ℕ ↪ DepthRotationRoute p tree tree` が単射であり、**全ての相異なる二つの塔段 `Tᵢ,Tⱼ` に元P92B Type値比較証拠は存在しない**。一方、元`NativeF54StructuralSeam.leftUnit`の再帰的貼合せ・逆・縦合成で**任意二段間の元構造seam Type値証拠が実在**し、別`NativeF55StructuralComparison`では全段が接続される。これは単なる有限幾何や数値shadowの一致ではなく、**有限C60上に元Type値構造比較でつながる無限族とP92Bの無限分離**を証明する結果である。さらに既存GI元`DepthRotationRoute`全依存型fiberの可算性（一般D/Eでは**対象と全HomファイバーのCountableを明示仮定**）と上記単射を結合し、F45自己経路fiberのCardinalが厳密に`Cardinal.aleph0`であることをLean4で証明。真正C60北側六角形の元`northHexagonNativeUnit 0`では**追加Countable仮定なしで正確に`ℵ₀`**。これは旧FJの14D Countable仮定除去や、19D filler・global strict n・hyperdescentを意味しない。定理squash SHA `ba1256195c23b0525b1fcd7755eea94b4e567d5a`、PR exact-source HEAD `e7798c97de3bf014e366c824de349c50e349c329`。[Strict Lean/Governance #41137844060](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41137844060) **3709/3709 scoped SUCCESS・5/5 jobs completed SUCCESS**、GK4D新規13宣言の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。


**先行する非充填証明 GK4C [#2740](https://github.com/itakura-hidetoshi/KuuOS/pull/2740)：** P92Aの**元F54ゼロ回転鎖の順序付き文脈語**からその要素数 `gk4cUnitCount` を抽出し、P92B新規`assocNaturality`を含む**全9構成子**がその個数を保存することを元Type値証拠のままLean4で証明した。真正F54 `NativeF54StructuralSeam.leftUnit/rightUnit`は元の反射的ゼロ回転鎖を1個増加させるため、**任意の元F54経路に対し、これらの2種類の構造seamには元P92B 3-cellが存在しない**。元F45 Treeが実在する任意の入力では、GK4の全seam P92B実現条件が**充足不能**となり、全体の依存型境界保存 `StructuralComparison → P92B` 戻し写像も存在しない。さらに真正C60北側六角形の`northHexagonNativeUnit 0`で、この**無条件の物理C60非存在定理**を特殊化した。GK4Bが示した「元P92Bを固定する戻し写像の非単射性」を越える**戻し写像そのものの非存在**だが、結論は元F45証拠が実在する文脈の選択した原presentationについてであり、14構成子のすべてがP92Bで非充填とも、任意の抽象Type同値が不可能とも主張しない。定理squash SHA `f1f634431c0f9bbac24c8cd2c36021f06dbc44f5`、exact-source HEAD `2373f8d924f8266a44355b23698fa1ad181e5b3d`、[Strict Lean/Governance CI #41134626302](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41134626302) **3708/3708 scoped SUCCESS、Governance 4/4 completed SUCCESS**。新規15宣言公理は標準`propext`・`Quot.sound`以内、`sorryAx`なし、変更Lean warning/error **0/0**。保護PR #1558 Draft/OPEN/未マージ、107公開root、strict空・独立Kuu・Gray非再導入を維持。


**先行する比較障害 GK4B [#2738](https://github.com/itakura-hidetoshi/KuuOS/pull/2738)：** GK4 [#2737](https://github.com/itakura-hidetoshi/KuuOS/pull/2737) は、元Type値 `NativeF55StructuralComparison` から元P92B `NativeF55P92AssocComparison` への**境界保存戻し写像**が存在する必要十分条件を、**元F54構造seam全証拠それぞれに、同じ依存型境界のP92B元証拠を選べること**としてLean4で証明した（一般D/E Obj・Hom可算性を仮定せず、存在条件そのものを明示）。選択条件が成り立つ場合、原P92B構成子の保存および`trans`の合成保存を元証拠のまま定義した。GK4B [#2738](https://github.com/itakura-hidetoshi/KuuOS/pull/2738)はさらに、**`original`と新規`structural`の元Type値構成子の非同一性**、任意の真正F54経路の`r→r`ファイバーで元P92B埋込みの**非全射性**、原P92Bを恒等に保持する任意の戻し写像の**非単射性**、GK4で構成される全戻し写像の非単射性を証明した。これは**元の埋込みを保つ等式反映／完全型付き逆写像に対するno-go**であり、無関係な抽象Type同値が一般に存在しないという主張ではない。**歴史的P92B/F19/F28/F54/F55の完全型付き同型、真正14D `NativeK5FifteenFourteenFiber W`無条件Countable、旧FJ exact `ℵ₀` の14D前提除去、真正19D filler・global strict n・hyperdescentは依然未証明**。GK4B exact-source HEAD `3d0ac8a8f71310e0bfb9cccfb9d517a260e2046f`、squash SHA `25977553a89aaeed80c487002646f5fc20c574fe`、[Strict Lean/Governance #41132991365](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41132991365) **3707/3707 scoped SUCCESS・5/5 completed SUCCESS**、新規4定理は**すべて公理依存なし・sorryAxなし・変更Lean warning/error 0/0**。直前GK4 exact-source HEAD `5b74d3a0633eefea16ab0548414bcfe00e0538f6`、squash SHA `61db8ce3acf2c2da3028ba59692c4dd7aaabf790`、[CI #41132457146](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41132457146) **3706/3706 SUCCESS、5/5 completed SUCCESS、新規5宣言すべて公理依存なし**。


**直前の可算性証明 GK3 [#2735](https://github.com/itakura-hidetoshi/KuuOS/pull/2735)：** 2026-10-31 JST時点、元Type値 `NativeF55P92AssocComparison` の全9構成子（`original/assocNaturality/refl/symm/trans/leftContext/rightContext/precompose/postcompose`）と、別の `NativeF55StructuralComparison` の全3構成子（`original/structural/trans`）を、それぞれ全F45/F54経路・D/E Blocks・両Nat深さ・元P92B／構造seam証拠を保持する**独立した有限型付き構文、依存型部分復号、厳密左逆**により可算化した。一般D/Eでは対象と各HomファイバーのCountableを明示仮定し、元証拠totalと各indexed fiberはCountable。物理C60 `Site×Site` と全Polygonでは無条件。**歴史的P92B/F19/F28/F54/F55との型付き同型、真正14D fiberの無条件Countable、旧FJ exact `ℵ₀` の14D前提除去、19D filler・global strict n・hyperdescentは未証明**。GK3 exact-source HEAD `53bf08db8737ebe75654a550a3e858d2a29d30d3`、定理squash SHA `26f8047ec4308e20aa6b9d3773efb374a57f9b6f`。[Strict Lean/Governance #41113045813](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41113045813) **3705/3705 scoped SUCCESS、5/5 jobs completed SUCCESS**、21新規定理公理は標準3公理以内・sorryAxなし、変更Lean warning/error **0/0**、source/merge-test差分0。


**C60は縁起一般理論の起点ではなく、原証拠・非可換ゲージ・descentの検証場です。** FJ旧輸送の真正有限非空AQ文脈での非忠実性と、別presentation FK–FMの全有限文脈での忠実性を共存させます。FO [#2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689)は全衝突核、FP [#2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690)は核商≃実像、FQ [#2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692)はファイバー代表元への根付き正規生成、FR [#2694](https://github.com/itakura-hidetoshi/KuuOS/pull/2694)は完全再帰spine、FS [#2696](https://github.com/itakura-hidetoshi/KuuOS/pull/2696)は証拠保持boundary keyと有限active support下の有限正規生成、FT [#2698](https://github.com/itakura-hidetoshi/KuuOS/pull/2698)は受信18Dキーの完全単射性・元DV像一致 iff キー等号を証明。**新たにFU [#2700](https://github.com/itakura-hidetoshi/KuuOS/pull/2700)は、旧FJの元の異なる15D Type値証拠を、真正17D境界を保つ `(.post)^n (.assoc refl refl refl)` という任意深さの元18D構文へ実際に持ち上げ、全ての非空有限AQ文脈で元18Dコード2字は区別されながら受信コード像が一致することをLean4証明しました。** 各深さ `n` に原の完全再帰深さ `n+1` の非自明なFQ根付き元コードが存在し、自然数から真正FS active-root source字母のSubtypeへの単射を構成したため、**旧FJ真正物理輸送の任意非空有限文脈でactive-root元字母型が無限**です。これは有限正規生成不可能や最小・独立正規生成の証明ではありません。元19D幾何充填や大域strict高次構造・hyperdescentも未証明です。

**FV [#2702](https://github.com/itakura-hidetoshi/KuuOS/pull/2702) の更新：** FUの「無限個の非自明な根付き元文字」という結果から、**核の非有限正規生成性**まで独立の一般群論的証明によって到達しました。任意の有限群語集合が使用する有限source字母の外から非自明rooted核元を一つ選ぶと、その文字の整数座標群準同型は全有限関係語と正規閉包を消しますが、この核元を消せません。よって任意の有限個の非可換群語では全核を正規生成できません。**旧FJ真正物理文脈の全非空有限AQ語について確定した結論**であり、元18D証拠を整数に置き換えたわけではありません。元のsigned非可換自由群と完全Type値18D証拠は保持しています。

**FW [#2704](https://github.com/itakura-hidetoshi/KuuOS/pull/2704) の更新：** 非可換自由群写像の像ファイバー根 `r_f` の冪等性を利用し、全active文字 `D_f={a | a≠r_f(a)}` の根付き差語 `d_a=[a][r_f(a)]⁻¹` を整数座標で対角・非対角分離しました。任意の元文字添字集合 `T` が根付き差語族で**全kernelを正規生成 iff `D_f⊆T`** と証明し、FSの正規生成族が全てのactive元について**正規閉包の意味で非冗長**かつ相異なることを確立。さらに任意の非可換群語集合 `R` が全kernelを正規生成するなら、各active文字を検出する群語が必ず `R` に存在します。任意群語の元字母有限支持から、**全kernelは可算正規生成 iff `D_f` は可算**という追加の必要十分条件も証明しました。FV/FUの旧FJ真正全非空物理AQ文脈での非有限正規生成性は保持。一方、真正物理active元文字型の可算性・最小正規生成濃度の正確値・核自身の自由基底・元19D幾何充填は未証明です。
**FX [#2706](https://github.com/itakura-hidetoshi/KuuOS/pull/2706) の新規到達：** 任意の元文字写像 `f:A→B` の元の非可換自由群写像について、全kernelを正規生成する任意の**群語集合R**の濃度は、非自明rooted source文字集合 `D_f={a | a≠r_f(a)}` の濃度以上であると証明しました。元のSource FreeGroup全体から `D_f→₀ℚ`（有理数有限支持自由加群）の乗法表示へ実際の群準同型を構成し、真のrooted元語を各標準基底へ写します。全核を正規生成する任意Rの像を線形に張った部分空間で割ると、Rを消す群準同型は全normal closureも消し、根付き差語からすべての標準基底が部分空間に属することを強制します。固定mathlibのrank定理から**`#D_f ≤ #R`**を有限・無限を問わず証明。FWで証明済みの根付きrelator単射性により、**濃度ちょうど`#D_f`の正規生成集合が実在**します。従って**全kernelの最小正規生成濃度=`#D_f`**が確定。旧FJ真正物理18Dで`D_f`が無限というFUの結論と組み合わせると最小濃度は無限ですが、元の依存型active文字型の正確な濃度（可算か非可算か）や元kernel自身の自由基底、真正19D幾何充填は未証明です。
**FY [#2708](https://github.com/itakura-hidetoshi/KuuOS/pull/2708) の新規到達：** FQで選んだ「同じ実像ファイバー内の代表元」が冪等であることから、任意の元source文字写像 `f:A→B` に対し **元のType値アルファベットそのものの同値** `A ≃ D_f ⊕ Set.range f` をLean4で構成しました。ここで `D_f={a | a≠r_f(a)}` は元の非root source文字であり、右項は全targetではなく**実際に受信される像ファイバーの集合**です。両文字型が同一universeの場合、**`#A = #D_f + #(range f)`**が成立し、さらに**`Countable A ↔ Countable D_f ∧ Countable (range f)`**を形式化。真正旧FJ元18D依存Type値コードの全てのAQ文脈へ特殊化し、FUの全非空物理AQ文脈におけるactive字母無限性とFXの最小正規生成Cardinalを接続しました。**元の完全18D source alphabetがCountableという明示的追加仮定の下で**、全元18D非可換DV kernelの最小正規生成濃度が正確に`ℵ₀`と証明されました。有限なC60幾何だけから元14D–18D証拠の可算性は従わず、**真正物理active字母の無条件の正確な濃度はまだ未決定**です。
**FZ [#2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) の到達：** 真の依存型raw17D経路totalが可算となる十分条件を、元17D対象Typeの可算性と**各raw17D証拠ファイバー**の可算性からLean4形式化し、実際の18D層オブジェクトTypeへ伝播しました。続いて元18D `assoc/post/pre` 生成子の**各依存型ファイバーも可算という別条件**から、元の完全18D sourceコードType全体の可算性を証明しました。これらの条件を真正FJ物理18Dへ直接特殊化し、全非空AQ文脈の最小正規生成濃度`ℵ₀`を条件付きで導出。さらに一般写像`f:A→B`で、実受信像が可算かつactive source文字が無限なら、**元source Typeが可算 iff 任意非可換群語の全kernel正規生成集合で濃度ちょうど`ℵ₀`のものが存在**をFXの鋭い下界とFYのsource型同値から証明しました。受信像が可算で元sourceが非可算なら、active文字も非可算という障害も証明。**18D再帰生成子ファイバーの可算性を下位の全14D–17D元構文から自動導出することは未証明**です。
**GA [#2712](https://github.com/itakura-hidetoshi/KuuOS/pull/2712) の新規到達：** 元の`NativeC60AXStep`四構成子`atom/refl/symm/trans`について、**元の依存型生成子・始域・終域を保持する有限構文符号化と部分復号器**をLean4で構成しました。任意の元raw証拠`p`が`decode(encode(p))=some(p)`を満たす厳密復元を証明し、元layer object Typeと全元primitive GenファイバーがCountableなら元raw経路total・全依存型経路ファイバーがCountableと確立。これを真正16D文脈閉包`List Bool`＋元primitive Type、17D三角形`Gen`の元raw16D両経路＋Prop証拠へ連鎖適用し、**元の下位AXオブジェクト・Genの可算性だけで真正raw17D全経路ファイバーを可算と証明**しました。真正FJ物理18Dでも、下位AX primitive小ささと**残る元18D `assoc/post/pre`再帰生成子ファイバー可算性**の明示条件だけで、完全元18D文字型Countable、および全非空AQ文脈の最小非可換正規生成Cardinal`ℵ₀`を導きました。最後の18D再帰ファイバー条件を無条件に落としたわけではありません。
**GB [#2714](https://github.com/itakura-hidetoshi/KuuOS/pull/2714) の確定成果：** GAで残っていた真正18Dの`NativeC60DREighteenAssocGen`三構成子`assoc/post/pre`について、**完全な元raw17D依存型証拠をatom tokenとして保持する別の有限構文木**を作り、型不適合な入力を拒否する部分復号器を実装しました。任意深度の元の18D再帰生成子に対して**`decode(encode r)=some(元source,target,r)`**をLean4帰納法で証明。従って、元raw17D証拠totalが可算なら元18D再帰生成子totalと各依存型Genファイバーは**実際に可算**と確定しました。さらにGAの16D閉包・17D三角形primitive・raw17D可算性伝播を合成し、**元lower AX object totalと各primitive Genファイバーの可算性だけ**から元の完全18D source文字Typeが可算と証明。真正旧FJ物理18Dのすべての非空有限AQ文脈で元全非可換DV核の最小正規生成濃度が`ℵ₀`となる定理へ接続し、以前必要だった**18D再帰Genファイバーの独立したCountable仮定を除去**しました。下位の真正14D–15Dカテゴリー・source証拠型の可算性自体は未証明であり、有限C60幾何だけから導いていません。
**GC [#2716](https://github.com/itakura-hidetoshi/KuuOS/pull/2716) の確定成果：** 元の真正物理K5 AX primitive `Gen x y` は、元の完全14D/15D AX base total中の15D証拠にProp値の端点等式を付加した依存型です。元の全Type値15D証拠と両14D端点を保持してProp値等式だけを忘れる**単射**を構成し、**`Countable (nativeK5AXBaseLayer W).Total`だけから元primitive Genの全依存型ファイバーのCountable**をLeanで証明。GA/GBと合成し、元18D source全体のCountable、真正旧FJの全非空有限AQ語で元DV非可換kernelの最小正規生成濃度`ℵ₀`を、AX base total Countableという単一条件下で形式化。さらに実14D fiber・元15D proof各ファイバーのCountableからbase total Countableとなる定理も証明。**9045/9045 Strict Lean SUCCESS、Governance 30/30 SUCCESS、5定理標準3公理以内、sorryAxなし。**
**GD [#2717](https://github.com/itakura-hidetoshi/KuuOS/pull/2717) の最新確定成果：** 元の観測保守的15D`atom/refl/symm/trans`構文と、実15D`NativeFifteenFamilyCell`の`conservative/exchange/symm/trans`構文を、**完全元14D両端点・元core15D Type値証拠・独立`List Bool` exchange添字を保存する有限符号へ再構成**しました。型不適合な接続は部分復号で拒否し、任意有限深さの元依存型証拠`p`で**`decode(encode(p))=some⟨(source,target),p⟩`**を証明。元14D fiber Countableだけから**元15D全ファイバー、元AX base total、元完全18D source全体Countable**と、真正旧FJ全非空有限AQ語の完全非可換核の最小正規生成濃度`ℵ₀`を導出。**9046/9046 Strict Lean SUCCESS、Governance 30/30 SUCCESS、9定理の標準3公理監査・sorryAxなし・変更Lean warning/error 0/0**。元14D証拠型自体と、任意inputカテゴリーHomの可算性はなお無条件に成立したとは宣言しない。
**GE [#2719](https://github.com/itakura-hidetoshi/KuuOS/pull/2719) の確定成果：** 元F112物理C60の `Dart`（60）、`Edge`（90）、`Polygon`（32）、`Site`（182）は既存の`Fintype`から`Countable`が導かれることをLeanで形式化しました。さらに真正Site incidence-category Hom、元の依存型`Zigzag s t`全ファイバーと両端点を含むtotal、元多角形上の`PolygonBracketTree`・`PolygonBracketRotation`・`PolygonBracketRoute`の全有限再帰構文と両端点を含むtotalの`Countable`を形式化しました。有限のセル添字だけでなく、**任意有限長の型付きraw証拠経路**まで対象にしています。GEでは元14D `NativeK5CoreFourteenCell`／`NativeK5StructuralFourteenCell`の直接`deriving Countable`も検査し、元7D–13D Type値証拠にCountableがないことをCIで確認しました。従って**元14D fiberの無条件Countableを証明したとは主張しません**。厳密な検証はPR source HEAD `8254f4920496819d7fc7dc6b0ba3c7154f16de52`、[Strict Lean #41019406316](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41019406316) **9047/9047 SUCCESS**、Governance **30/30 SUCCESS**、12宣言`#print axioms`は標準3公理以内・`sorryAx`なし、変更Lean warning/error **0/0**。
**GF [#2721](https://github.com/itakura-hidetoshi/KuuOS/pull/2721) の確定成果：** 真正`KuuNativePath`と`KuuNativeBlocks`の元の依存型証拠・全始域終域・カテゴリーHom・空ブロックを含む区切りを保持した、**有限構文符号化と型不整合を拒否する部分復号器**を構成しました。任意の元path／blocks `p` に対し `decode(encode(p))=some⟨source,target,p⟩` をLean4で証明。**カテゴリー対象型`Countable C`と全元Homファイバー`∀ x y:C, Countable (x ⟶ y)`**を明示条件として、元のpath総体／全indexed fiberとblocks総体／全indexed fiberのCountableを証明しました。GEの実C60有限`Site`とそのincidence Homに適用し、実物理Siteのpath・blocksの完全総体と全ファイバーがCountableになることを無条件に示しました。さらに**元C60 `PolygonNativeDualAxisFrame`の実際の2つの独立したブロック証拠と両端点・全多角形sectorを保持するtotal Countable**を証明。PR exact-source HEAD `a1d502dae5d63eda092fda50edd041e0f9135bfe`、[Strict Lean #41024678183](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41024678183) **9048/9048 SUCCESS**、Governance **30/30 SUCCESS**、13定理の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし・変更Lean warning/error 0/0。**一般D/EカテゴリーHomや真正7D–13D、14Dの元Type値証拠が無条件に可算になるとは主張しません。**
**GG [#2723](https://github.com/itakura-hidetoshi/KuuOS/pull/2723) の確定成果：** GFで可算化した真の元`KuuNativePath`・`KuuNativeBlocks`を用い、元`KuuNativeOneStep`の`split/insertNil/whisker`三構成子および元`KuuNativeAxisTrace`の`refl/snoc`任意深さ再帰構文を、**全Type値証拠・元カテゴリーHom・中間分割境界・正確な始域終域・Nat深さを保持する有限コードと依存型部分復号器**へ符号化しました。型不整合な中間ブロックでは復号が失敗し、元の正しい任意証拠では厳密な`decode(encode h)=some⟨元境界,元証拠h⟩`をLean4で証明。カテゴリー対象型`Countable C`と全元Homファイバー`∀ x y:C, Countable (x ⟶ y)`を明示した条件として、元OneStep／AxisTraceの全証拠totalと各依存型ファイバーのCountableを証明しました。GE/GFの真正C60 `Site`と実incidence Homに適用すると、これらすべてはC60入力に対して無条件にCountableです。[Strict Lean #41026975324](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41026975324) **9049/9049 SUCCESS**、Governance **30/30 SUCCESS**、GG12宣言の`#print axioms`は標準`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし、変更Lean warning/error 0/0。PR source HEAD `8bf0e8ea26ef60728c79608de2d42f6e6c631479`、定理squash SHA `5bdd7dcf6550660f632ae655b58e8559c7899c57`。真正F45/F55、7D–14DのType値証拠総体がこの結果だけで可算と確定したわけではありません。
**GH [#2725](https://github.com/itakura-hidetoshi/KuuOS/pull/2725) の確定成果：** 真の元`KuuNativeF45Tree`の`refl/leaf/node`三構成子を、真正C60多角形sector、元の二通りの実行順序、独立カテゴリーD/Eの全`KuuNativeAxisTrace`・中間`KuuNativeBlocks`と二つのNat深さを保存する有限構文に忠実に符号化しました。依存型部分復号ではカテゴリー始域終域・両軸の中間Blocksが一致しないnodeを拒否し、indexed復号は両Nat深さを含む完全境界不一致を拒否します。元の任意F45証拠に対する厳密な`decode(encode tree)=some⟨元境界,tree⟩`とindexed左逆を証明。対象型D/EのCountableと**各元HomファイバーのCountableを明示条件**として元F45 total／全indexed fiberの可算性をLean4証明し、真正C60の`Site × Site`ではGE・GF・GGから無条件に証明、全32実多角形にわたる証拠totalもCountableです。PR exact-source HEAD `d426eeb2a95aef5c561a160e44c24c12b085a95e`、[Strict Lean #41030788233](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41030788233) **3689/3689 scoped SUCCESS**、Governance gate completed SUCCESS、8定理の公理依存は`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし、変更Lean warning/error **0/0**、source/merge-test差分ファイル0。定理squash SHA `330aa4f6d63f5530b93f8d7b5182563b88c0555a`。**原F45のSite×Site特殊化は任意D/Eの無条件Hom可算性や元F55／7D–14D／真正14D fiber可算性の証明ではありません。**
**GI [#2727](https://github.com/itakura-hidetoshi/KuuOS/pull/2727) の確定成果：** GHの真正二カテゴリー`KuuNativeF45Tree`を土台に、元の`LocalRotation`（`assoc/leftContext/rightContext`）、方向付き`RotationEdge`（`forward/backward`）、任意有限`RotationChain`（`refl/snoc`）、そして`DepthRotationRoute`の全5構成子（`chain/castDepths/trans/leftContext/rightContext`）を、**元のD/E独立カテゴリー・全中間Blocks・全F45証拠・2つのNat深さと等式輸送・原証拠履歴**を保持する有限構文へ符号化しました。依存型部分復号は不一致なオブジェクト／Blocks／両深さ／中間Treeを拒否し、元の任意の正しい証拠について厳密な`decode(encode r)=some⟨元境界,r⟩`をLean4で証明しました。一般D/Eの**対象可算性と全Homファイバー可算性**を前提として、各元Type値証拠totalと依存型fiberのCountableを証明。真正物理C60の`Site×Site`と全Polygon総体ではGE–GHにより無条件に導出します。等式証拠はPropのまま`PLift`を介して有限Type構文へ持ち上げ、証拠の復号では`gradeProof.down.1/.2`で投影し、Propをパターン照合せず元の2つの輸送を復元します。定理squash SHA `e395b7f10c914c08bd9bcc84a0614b9663f2e84f`。exact-source HEAD `ab32039bd9fb9a8352e2da1aa96a13101900c853`、[Strict Lean / Governance #41042570393](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41042570393) **3692/3692 scoped SUCCESS／Governance全5ジョブSUCCESS**、24宣言の公理依存は`propext`・`Classical.choice`・`Quot.sound`のみ（無公理の1宣言を含む）、`sorryAx`なし、変更Lean warning/error **0/0**、source／merge-test差分ファイル0。元の歴史的F19/F28/F54/F55との型付き同型、真正14D Countable、元19D fillerや大域strict n・hyperdescentは依然として未証明です。
**GJ/GJ2 [#2729](https://github.com/itakura-hidetoshi/KuuOS/pull/2729)・[#2730](https://github.com/itakura-hidetoshi/KuuOS/pull/2730) の確定成果：** GJは真正二本の並行F54型`DepthRotationRoute`の総体と元F55の`pentagon`（4つの完全F45 stage）・`disjointSquare`（2つの完全LocalRotation証拠）の完全原始構文を構成し、一般D/Eの対象と**各HomファイバーのCountable**を仮定した可算性、および実C60 `Site×Site`への無条件適用を証明。GJ2はさらに独立F112の真正`KuuNativeF45Tree.DepthRotationRoute.PresentedCell`の**全9構成子**（`ident/pentagon/disjointSquare/symm/trans/leftContext/rightContext/precompose/postcompose`）を、すべての元Type値F45 Tree・F54経路・D/E Blocks・両Nat深さ・途中の3-cell証拠を保った有限再帰構文へ符号化。依存型の不一致を拒否する部分復号と、**全元3-cellについて厳密な`decode(encode c)=some⟨元境界,c⟩`**をLean4で証明し、真の元証拠総体・各indexed fiberのCountableを一般D/Eの明示可算条件から導出。実C60 `Site×Site`と全Polygonでは無条件。GJ2定理squash SHA `3d0ec687d9e73784b13e9b6cfccb4754b13e692a`、exact-source HEAD `1b90257bb2f989c248014d5f0730b075ea38b447`、[CI #41050927061](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41050927061) **3695/3695 scoped Strict Lean SUCCESS**、Governance **5/5 SUCCESS**、新規15定理の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内（無公理2件含む）、`sorryAx`なし、変更Lean warning/error **0/0**、source/merge-test差分ファイル0。**独立F112の提示F55であり、歴史的元P92B・F19/F28/F54/F55との同型や`NativeF55StructuralComparison`の可算性は未証明。真正14D `NativeK5FifteenFourteenFiber W` Countableの条件除去も未達。**
**GK [#2732](https://github.com/itakura-hidetoshi/KuuOS/pull/2732)／GK2 [#2733](https://github.com/itakura-hidetoshi/KuuOS/pull/2733) の確定成果：** 元F54の独立 NativeF54StructuralSeam は14構成子の真正Type値証拠であり、GJ2の元F55 PresentedCell（9構成子）と同一のpresentationではない。GKは元14構成子の全有限構文と元P92Bの新規assocNaturality生成子に必要な6つのF45 Tree・3つのF54経路・独立D/E Blocks/Nat深さを完全に保持する原子可算性を証明。GK2ではさらに真の14構成子すべての元F54再結合・単位・左右文脈・congruence・pre/post合成を、独立の依存型F45/F54入力証拠を保った有限構文へ符号化し、型不一致を拒否する部分復号と厳密な decode(encode w)=some⟨元境界,w⟩ を証明。一般D/Eの対象・各HomファイバーのCountableを前提として、元 NativeF54StructuralSeam **Type値証拠全体と各indexed fiberのCountable** を導出し、真のC60 Site×Siteと全Polygonでは無条件。GK2定理squash SHA f409773a969c529e8e635b7402cf28683f9d0d11、exact-source HEAD e7deae8c6f7612d4d22345bff19197c3dade4453、[Strict Lean/Governance #41055177820](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41055177820) **3701/3701 scoped SUCCESS**、Governance **5/5 completed SUCCESS**、23新規宣言の公理監査は標準propext・Classical.choice・Quot.soundのみ（無公理の原始解釈を含む）、sorryAxなし、変更Lean warning/error **0/0**、source／merge-test差分0。**GK2時点では別定義の NativeF55P92AssocComparison と NativeF55StructuralComparison は未証明だったが、その全構成子の厳密復号・CountableはGK3 #2735で証明済み。歴史的P92Bとの型付き同型や真正14D Countable、旧FJ exactℵ₀の14D仮定除去は引き続き未証明。**


| 項目 | 2026-10-31に確認した状態 |
| --- | --- |
| 定理の正本 | [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。公開統合入口は [`formal/KuuOSFormal.lean`](formal/KuuOSFormal.lean)（既存107公開rootを維持） |
| 直近の定理統合点 | **F112-P94D3GK4O / [PR #2763](https://github.com/itakura-hidetoshi/KuuOS/pull/2763) MERGED**。squash SHA `1370dce5a2a55a89ad4758911aea23597ce34050`。全F45境界にわたる元P92B商の観測関数族について、**kernelの前後合成・左右context互換性を4条件として明示した下で**、全14真正F54構造seam保存と7基本生成子保存が同値。GK4Nを用い独立構造商への全境界での降下と接続。GK4G Bool保存、GK4K Option Natの左単位seam障害。 |
| 直前の定理統合点 | **F112-P94D3GK4N / [PR #2761](https://github.com/itakura-hidetoshi/KuuOS/pull/2761) MERGED**。定理squash SHA `76eaf1c6c0ccb86ce7fd5e9e44ee74b9330df6d0`。任意の元P92B商観測は**真正F54構造seam全14を保存することiff独立構造商へ降下**。任意の生F54観測は元P92B比較とF54構造seamの二族を保存することiff独立構造商へ降下。全比較Type値帰納法、降下因子の一意性、Bool保存・原始Option項数の左単位seam局所obstructionを実証。 |
| 直前の定理統合点 | **F112-P94D3GK4M / [PR #2759](https://github.com/itakura-hidetoshi/KuuOS/pull/2759) MERGED**。定理squash SHA `36e13ca4f961a9a528d5592878a60cb2cd2e4fe1`。任意`f:Option Nat→B`がGK4K観測の後処理として構造商へ降下可能であることと、`f(some n)`が全正整数`n`にわたって一定であることの必要十分性。降下すればGK4Gの真正構造商Bool gradeを通る正準の一意な因子になる。 |
| 直前の定理統合点 | **F112-P94D3GK4L / [PR #2757](https://github.com/itakura-hidetoshi/KuuOS/pull/2757) MERGED**。定理squash SHA `b8ba6b09cb37239e4f25d7ef66cafad3565596f4`。真正GK4D単位塔`T_k`のGK4K Option Nat観測は`some(k+1)`で各段異なるのに、GK4E構造商では全段同一類。任意値域への降下必要十分条件を証明し、GK4K Option Natは構造商へ不降下、GK4G Bool gradeは降下可能と確定。 |
| 直前の定理統合点 | **F112-P94D3GK4K / [PR #2755](https://github.com/itakura-hidetoshi/KuuOS/pull/2755) MERGED**。定理squash SHA `ef9e69c982706985a6dadfd72bd1199dde1531dd`。GK4Jの物理回転数0条件付き項数不変量を、元P92B商の`Option Nat`値測定へ厳密降下。代表元独立、一意性、GK4G Bool gradeのrefinement、`some n → n>0`、`some 0`の像不存在、GK4H真正商合成と`some(a+b)`／`none`吸収則を証明。 |
| 直前の定理統合点 | **F112-P94D3GK4J / [PR #2753](https://github.com/itakura-hidetoshi/KuuOS/pull/2753) MERGED**。定理squash SHA `daa94823b410ce5a1a31004b72d01951af8a6420`。真の元F54の原始経路項数は全経路で正・合成加法的であり、真の物理回転数0の範囲で元F55全9・P92B全9構成子に保存される。これにより**元P92B商で任意の左単位・右単位候補が不可能**、全F45 stageへの圏単位割当も不可能とLean4で証明。構造商GK4Iは同じ物理C60境界で真正圏のまま。 |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| PR #2763の証明検証 | exact-source HEAD `b18ced002802ff865966c8a5e7a29501bd19a227` [CI #41159766444](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41159766444) **3720/3720 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**、17宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。 |
| PR #2761の証明検証 | exact-source HEAD `a1716b21a09bc70af3b41969590db93596ec5e65` [CI #41158003474](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41158003474) **3719/3719 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**、13宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。 |
| PR #2759の証明検証 | exact-source HEAD `f533b3973981384ea3b06c524f9ee142d936fb4e` [CI #41157123830](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41157123830) **3718/3718 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**、13宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。 |
| PR #2757の証明検証 | exact-source HEAD `c97c947ed2e80683a425848ca1b9eea90d13ea4c` [CI #41156497624](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41156497624) **3717/3717 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**、13宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。 |
| PR #2755の証明検証 | exact-source HEAD `c6e841c85a3a61ce0f65dfde3ee2a87c8319f3e4` [CI #41155697783](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41155697783) **3716/3716 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**。19宣言、標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。 |
| PR #2753の証明検証 | exact-source HEAD `011d56a8496acf89c5c1619d926e784ee3dadfc0` [CI #41150002368](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41150002368) **3715/3715 scoped Strict Lean SUCCESS・Governance 5/5 completed SUCCESS**、14宣言公理`propext`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。先行GK4I #2751（3714、14宣言）、GK4H #2749（3713、21宣言）、GK4G #2747（3712、28宣言）は独立receiptとして保持。 |
| 基礎・presentation | strict空を中心に据えるが、独立Kuuも空の一つのpresentation。`KuuOSStrict`は**内部import集約**であり、別の正本でも「唯一の空」でもない。Gray圏を新しいstrict証明の根拠として再導入しない |
| 次の定理作業 | **F112-P94D3GK4P（仮称）**：GK4Oで追加仮定とした4種類のkernel輸送互換性を、真正元F54/P92B合成則・左右context作用を保存する具体的観測の条件から導けるか研究する。任意観測に無条件で7条件還元できるとは仮定しない。元P92B結合律・別合成、真正14D Countable・元19D filler・global strict n・hyperdescentは未証明。 |

### 現行のC60 Type値証拠・非可換核の到達点

| 系列・統合PR | Leanで確立したこと | 越えていない境界 |
| --- | --- | --- |
| EX–FA [#2663](https://github.com/itakura-hidetoshi/KuuOS/pull/2663)–[#2666](https://github.com/itakura-hidetoshi/KuuOS/pull/2666) | 元の完全18D非可換pentagon欠損、有限符号付き19D**候補経路**の順序付き積、正規閉包・相対商、実際のDV 17D文脈輸送に沿う生成子別降下条件 | 相対19D presentationと元のC60幾何における実在19D充填を同一視しない |
| FB–FC [#2667](https://github.com/itakura-hidetoshi/KuuOS/pull/2667)–[#2668](https://github.com/itakura-hidetoshi/KuuOS/pull/2668) | 完全pentagon自由群証拠はDV輸送後も非自明。一方、明示的DX相対商では消える。完全コード関数`f_w`と自由群準同型`τ_w`の単射性同値、非自明核とコード衝突の同値 | 元の完全証拠の非自明性と選択相対商での零化を混同しない |
| FD–FE [#2669](https://github.com/itakura-hidetoshi/KuuOS/pull/2669)–[#2670](https://github.com/itakura-hidetoshi/KuuOS/pull/2670) | 真正17D対象の文脈衝突から元18Dコード衝突と非自明2文字核を構成。反射的associatorコード族で衝突の必要十分条件を証明。全有限文脈対象作用の単射性は2つの単独frame作用の単射性と同値。各`onObj/onCell`単射性は十分条件 | 任意のC60 frameで単射性が成立するとは証明していない |
| FF [#2671](https://github.com/itakura-hidetoshi/KuuOS/pull/2671) | `C_w`の単射性を**明示的な仮定**として、原raw17D全構成子の等式反映、元の両端点とraw17D証拠を含む18D**対象**全体の単射性を証明。空文脈の18D対象写像は無条件に単射 | 18D対象の単射性は18D**生成子**コードの単射性とは別 |
| FG [#2672](https://github.com/itakura-hidetoshi/KuuOS/pull/2672) | 元の18D生成子の`assoc/post/pre`タグは任意のDV文脈で保存され、異種セクター間のコード衝突と対応する2文字核が存在しない。完全コード・元の非可換自由群輸送の単射性は3セクター各々の忠実性と同値。17D文脈作用が単射なら、`assoc`の3経路および固定内側生成子に対する`pre/post`の17D引数が単射 | 可変な再帰的内側生成子の全単射性、および3セクターの忠実性の無条件成立は未証明 |
| FH [#2674](https://github.com/itakura-hidetoshi/KuuOS/pull/2674) | 可変な内側18D生成子と外側`pre/post`の元raw17D経路を同時に扱い、実17D文脈対象作用および固定内側ファイバーの忠実性を**仮定した場合**の共同単射性を証明。新規Lean定理の`#print axioms`は`propext`のみ | 元のすべての内側生成子ファイバーでこの仮定が成立すると断言しない |
| FI [#2675](https://github.com/itakura-hidetoshi/KuuOS/pull/2675) | 元18D生成子の入れ子`pre/post`から終端`assoc`までの**全再帰構成子列・深さ**は任意の真正有限C60文脈で無条件に保存。完全自由群上の非可換構成子列準同型の自然性と**全DV核の包含**を証明。Strict Lean 9949/9949 SUCCESS | 全構成子列は元raw17D引数まで記録するものではない。**同一列内のコード衝突・完全核分類はなお未証明** |
| FI（完全反映）[#2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676) | 元`assoc/post/pre`全帰納法で可変内側18D生成子・raw17D両端点・途中境界を保持し、`Injective(f_w) ↔ Injective(C_w) ↔ Injective(τ_w)`を証明。空文脈と2つのsingleton frameの忠実性判定。9950/9950 SUCCESS | この一般同値の物理的成否はframeの選択に依存。FJ旧frameは非空文脈で非単射、FMの別frameは全有限文脈で単射。元の幾何19D充填・旧核全分類は未証明 |
| FJ [#2679](https://github.com/itakura-hidetoshi/KuuOS/pull/2679) | 真正物理AQ `nativeK5AQWhiskerCell` が元15D保守的`refl`と`atom rfl rfl`の異なるType値証拠を同一像へ写すことを構成。元proof-bearing AX・17D singletonへ明示的に持ち上げ、任意の元Wと有限語wについて **`Injective(τ_w) ↔ w=[]`**、同じ非自明2文字欠損zが**すべての非空w**で`τ_w(z)=1`となることを証明。 | この非単射性は**選択された元15D AQ証拠構文・真正物理frame**の定理。任意の抽象F、別presentation、元14D幾何作用一般の非単射性や19D fillerの存在を主張しない |
| FK [#2681](https://github.com/itakura-hidetoshi/KuuOS/pull/2681) | 同じ元14D依存境界の上に、新しい保守的15D証拠の`refl/atom/symm/trans`構成子保存whiskeringおよび別のAX frameを構成。元の14D左右raw-whiskering単射性、FJの2証拠の新輸送による分離、**旧輸送 = 構成子忘却 ∘ 新輸送** の全raw15D経路についての同値、逆の復元不能性をLean証明。新輸送は全有限AQ語でFJ証拠の区別を保つ | FK段階で未証明だった全依存型Hom単射性はFLで証明済み。元のFJ非単射性・全核・19D幾何の障害は残る |
| FL [#2683](https://github.com/itakura-hidetoshi/KuuOS/pull/2683) | FKの別15D輸送で保守的core全構成子・独立`exchange`添字・外側`symm/trans`を型付きで等式反映。可変14D中間境界を`Sigma`で復元し、交換は`Option`射影と`HEq`で復元。全Homファイバー・任意有限AQ語・代替frame `onCell`単射性を証明。9953/9953 SUCCESS | FL時点で未解決だった新frameの`mapTotal`と17D/18Dへの忠実性は後続FM [#2685](https://github.com/itakura-hidetoshi/KuuOS/pull/2685)で解決。FJ旧no-goを保持 |
| FM [#2685](https://github.com/itakura-hidetoshi/KuuOS/pull/2685) | FK・FL別AQ輸送に対し、元14D `onObj`と全15D `onCell`の単射性を合成して`mapTotal`単射性を証明。16D raw構文の`atom/refl/symm/trans`を真の依存型中間境界・元generator provenanceを保って反映し、DR 17Dの全有限AQ文脈作用の単射性を確立。FIの同値から完全18Dコード・非可換自由群輸送の全有限文脈単射性と自明核を証明。9954/9954 SUCCESS | 旧FJ frameの非空文脈非単射性は変更なし。旧核の完全正規生成表示、旧新17D/18D間の自然比較、幾何19D充填・全strict高次構造は未証明 |
| FN [#2687](https://github.com/itakura-hidetoshi/KuuOS/pull/2687) | 保守的15D構成子忘却の冪等性・非単射性、全proof-bearing AX Total上での旧frame＝忘却∘新frame、全有限文脈での忘却の自然性、**非空全有限語での旧文脈＝忘却∘新文脈**をLean証明。17D identity・18D `assoc(refl,refl,refl)`の選択した真正Type値2証拠について旧像衝突／新像分離、旧受信18Dコードだけから新受信両像を復元する関数の不可能性、別々の非可換2文字元の旧核消滅／新全有限文脈生存を証明。9955/9955 SUCCESS | 旧新**全17D/18D閉包生成子**間の自然な比較関手は未構成。旧全kernelの正規生成表示・元19D幾何充填・全strict高次構造も未証明 |
| FO [#2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689) | 任意の `f:A→B` で `ker(FreeGroup.map f)` と全ソース文字の同じ像を持つ対の差語の正規閉包が一致。実際の完全18D DV輸送で全核を厳密表示し、任意非可換語の核所属・差語判定、受信器降下 iff 全コード衝突一致、非空FJ全核非自明／別FK/FL/FM全核自明を証明。9956/9956 Strict Lean SUCCESS、11定理公理監査 | 単一FJ欠損による全核正規生成、有限・最小生成集合、元の幾何的19D充填は未証明 |
| FP [#2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690) | FO全核正規閉包で割った非可換自由群と**実際の完全18D DV輸送像**の第一同型定理、代表元可換性、全コード衝突を尊重する受信器の像上への一意な群準同型因子化を証明。全射で標的全体の拡張が一意、非全射 `Empty→Bool` で全標的拡張が非一意という区別を形式化。9032 scoped jobs Strict Lean SUCCESS、11宣言公理監査 | 同型は**像部分群**についてで、全標的への無条件の全射・一意性、コード衝突の有限分類、真正19D Type値幾何充填を主張しない |
| FQ [#2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692) | 任意の `f:A→B` で全コード衝突対の正規閉包は、**実際の像の各ファイバーから選んだ根代表元と各source文字の差語**の正規閉包に一致。真正18Dの衝突対を元の`assoc/post/pre`3セクター内へ厳密分類し、原非可換自由群で3セクター関係和集合の正規閉包＝全核、根代表元のタグ保存、根付き正規商≃実輸送像、受信器の3セクター内一致 iff 像上の一意因子化をLean4証明。9033/9033 scoped Strict Lean SUCCESS、13公理監査 | 代表元の選択は非構成的であり、生成関係が有限・最小・独立とは未証明。異なる構成子セクター間の可換性も仮定しない。旧FJ欠損1元の全核生成、真正19D幾何充填は未証明 |
| FR [#2694](https://github.com/itakura-hidetoshi/KuuOS/pull/2694) | FG/FIの真正18D**全再帰spine保存**から、FO全コード衝突対＝全有限再帰spine同種衝突の和集合、全核＝その和集合の元の非可換群内正規閉包を証明。FQ代表元の全spine保存、根付き関係の全spine分割、受信器の実像上への一意な因子化 iff spine内の衝突一致 iff 各コードとファイバー根の一致。FHの真正依存型 `post/pre` 内側抽出により、外側衝突は内側輸送像の一致を必要とし、内側像の相違は外側衝突を排除。9034 scoped Strict Lean SUCCESS、12公理監査 | 全spineの種類と衝突関係の数は有限とは限らず、同一spine内の元17D引数の完全な一致分類や、有限・最小正規生成・真正19D充填は未証明。セクター間可換性も未仮定 |
| FS [#2696](https://github.com/itakura-hidetoshi/KuuOS/pull/2696) | 真正18D完全再帰spine、輸送後の元17D raw経路を含む始域/終域、全`post/pre`内側完全18Dコードを記録する実依存型境界キーを構成。全実コード衝突の同一キー局所化、全核＝同一キー衝突差語の正規閉包、異なるキーからの2文字核の排除、像上受信器のキー別一意降下必要十分条件を形式化。一般の`FreeGroup.map f`でファイバー根と一致する元の恒等関係を除外した全核の厳密正規表示、非自明根付き元集合が有限なら有限正規生成という十分条件を証明。9035 scoped Strict Lean SUCCESS／14公理監査 | **境界キー一致はDV像一致の十分条件とは未証明**。真正物理18D非自明根付き集合の有限性、最小/独立生成、単一既知FJ欠損の全核生成、元19D幾何充填も未証明 |
| FT [#2698](https://github.com/itakura-hidetoshi/KuuOS/pull/2698) | 真正context-CLOSED 18D受信生成子コードに対し、FSのType値境界キーの**無条件単射性**を証明。原17D raw `trans(trans f g)h`による`assoc`全3経路の復元、全依存端点可変の`post/pre`内側18Dコード＋source raw pathのsuffix/prefix復元、異種再帰spine分離を使う。従って真正元DVコードの輸送像一致 iff 境界キー一致を証明し、**元18D全非可換核＝キー等号のみで生成する最小正規閉包**、像上受信器のキー等号尊重 iff 一意因子化を確立。9036 scoped Strict Lean SUCCESS、FT11宣言の公理監査、核となる7宣言は公理依存なし | **元original17D raw証拠の一致を導いたわけではない。** 非自明rooted支持の物理的有限性／独立性／最小性、FJ既知1元の全核生成、幾何的19D充填は依然未証明。 |
| FU [#2700](https://github.com/itakura-hidetoshi/KuuOS/pull/2700) | 元の真正DR依存型18D構文上で、各元17D対象から `(.post)^n (.assoc refl refl refl)` 完全コードを任意の自然数深さに構成。元コードは17D元対象を保持し、再帰spine深さが厳密に `n+1`。元17D文脈対象に衝突があれば、同じ深さの異なる元コードの実DV受信像が一致。真正FJの元15D `conservative refl/atom`ペアに適用し、**全ての非空物理AQ文脈で、任意深さの異なる元コード衝突・各深さの非自明active-root元が存在**し、Nat→真正active-root source字母Subtypeの単射をLean証明。9037 scoped Strict Lean SUCCESS・11宣言公理監査 | active-root元字母型の無限性を確立。**全核が有限正規生成不可能であること、最小・独立正規生成数、FJ単一欠損の全核生成は未証明**。幾何19D充填も未証明 |
| FV [#2702](https://github.com/itakura-hidetoshi/KuuOS/pull/2702) | 任意 `f:A→B` について固定mathlib `Subgroup.IsNormalClosureFG` の厳密な必要十分条件：**`ker(FreeGroup.map f)` が有限正規生成 iff `{a | a ≠ r_f(a)}` が有限**。各元source字母の整数座標群準同型を`FreeGroup.lift`で構成し、任意1群語／有限群語集合の元字母有限支持を一般の非可換自由群で証明。有限関係語をすべて消す整数座標で支持外の非自明根付き核関係を検出し、任意の有限群語正規生成を否定。FUの実物理無限active元へ適用し、**旧FJの全非空有限AQ文脈の真正元18D DV全核が非有限正規生成**。9038 scoped Strict Lean SUCCESS／FV10宣言公理監査 | 最小正規ランクの正確な濃度・独立な正規生成基底、旧新presentation全対応、真正19D Type値幾何充填、大域strict高次構造は未証明 |
| FW [#2704](https://github.com/itakura-hidetoshi/KuuOS/pull/2704) | 選択した像ファイバー根の冪等性から、各active根付き差語に対する整数座標は対角+1・非対角0。従ってactive差語は他のrooted差語族の正規閉包の外にあり、全FS rooted familyはnormal-irredundantかつ単射。**`normalClosure({d_t : t∈T})=ker(FreeGroup.map f) ↔ D_f⊆T`**、任意の非可換正規生成関係語集合は各active座標を必ず検出し、**可算正規生成 iff `D_f` が可算**をLean証明。9039/9039 scoped Strict Lean SUCCESS、12宣言標準3公理内、Governance 30/30 SUCCESS | 元18D Type値・signed非可換核は保持。根付き添字族の非冗長性を、任意の群語集合の最小**Cardinal**や核自身の自由基底と取り違えない。真正旧FJ物理active source字母の可算性、単一FJ欠損での全核生成、元19D幾何充填・大域高次整合は未証明 |
| FX [#2706](https://github.com/itakura-hidetoshi/KuuOS/pull/2706) | 真正元source文字の非root集合 `D_f` を基底とする有理数有限支持自由加群 `D_f→₀ℚ` を構成。元のsigned非可換自由群からの群準同型で各rooted差語を厳密に標準基底へ写し、任意の群語集合Rのnormal closure＝全kernelなら、その座標像の線形span＝全自由加群。固定mathlibの自由加群rankとspan rank上界によって**任意Rの濃度`#R≥#D_f`（有限・無限とも）**を形式化し、FWのrooted map単射性による**ちょうど`#D_f`の正規生成族の存在**と統合。9040/9040 Strict Lean SUCCESS、7宣言の標準3公理監査、Governance 30/30 SUCCESS | 元kernelは非可換のまま、有理数座標は証明検出器。一般の最小正規生成濃度は確定したが、**旧FJ真正物理18D active元文字型の濃度が可算か非可算か**は別の未証明問題。核自身の自由基底、真正19D幾何充填・global strict/hyperdescentも未証明 |
| FY [#2708](https://github.com/itakura-hidetoshi/KuuOS/pull/2708) | 真のFQ像代表元を保持し、元sourceアルファベットの**型同値`A ≃ D_f ⊕ Set.range f`**、同一universeの正確な**Cardinal和`#A=#D_f+#(range f)`**、`Countable A ↔ Countable D_f ∧ Countable(range f)`を証明。元の真正18D DV source Type値コードへ同値と濃度境界を実際に特殊化し、全非空物理AQ文脈でのFU無限active文字＋FX exact正規生成Cardinalと接続。**元18D sourceコード型が可算という明示的条件の下で**最小正規生成濃度`ℵ₀`を厳密に導出。9041/9041 Strict Lean SUCCESS、10公理監査、Governance 30/30 SUCCESS | `Countable`は元14D–17D証拠の濃度からまだ無条件には証明していない。有限幾何≠有限・可算Type値証拠。真正19D filler・元kernel自由基底・大域strict/hyperdescentは未証明 |
| FZ [#2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) | 真正17D endpoint型と各raw17D `NativeC60AXStep`証拠ファイバーの可算性から実18D層object Typeの可算性を証明。さらに依存18D `assoc/post/pre`生成子ファイバーの可算性を加えると、元18D完全source文字Typeが可算になることを形式化。真正FJ物理18Dへ具体化し、全非空AQ語で最小正規生成Cardinal`ℵ₀`を明示的下位型条件下で証明。実受信像が可算でactive字母無限なら、**元source可算 iff exact`ℵ₀`の任意群語正規生成集合が存在**、実受信像可算でsource非可算ならactiveも非可算という障害を確立。9042/9042 Strict Lean SUCCESS、FZ9公理監査、Governance 30/30 SUCCESS | raw17D構文および18D再帰生成子ファイバーが実際に可算であるための元14D–16D primitive typeの十分条件はまだ閉じていない。有限C60幾何から可算性を推測しない。真正19D Type値幾何充填、kernel自由基底、strict高次化は未証明 |
| GA [#2712](https://github.com/itakura-hidetoshi/KuuOS/pull/2712) | 元の`atom/refl/symm/trans`四構成子の有限コードと、型不整合を拒否する真の依存型raw経路部分復号器を構成し、**decode∘encodeは元raw証拠に恒等**と形式化。元layer.Totalと元`S.Gen x y`ファイバーCountableから**元raw path totalと全ファイバーCountable**を証明。さらに元16D closed context Gen・raw16D全語・元DQ17D object・triangle Gen・全raw17D経路へのCountable伝播を、元lower AX primitive Countableの条件下で確立。旧FJ真正物理18Dでは、別途18D recursive Genファイバーが可算なら元source Countableと全非空AQ文脈の最小正規生成Cardinal`ℵ₀`が成立。9968/9968 Strict Lean SUCCESS、13定理の標準3公理監査、Governance 3/3 selected SUCCESS | 元`assoc/post/pre`再帰生成子ファイバーのCountableはまだ明示条件であり未証明。元の任意category Homを有限C60幾何だけから可算とはしない。別FK–FM忠実presentation、元19D Type値幾何充填・大域strict/hyperdescent未証明を保持 |
| GB [#2714](https://github.com/itakura-hidetoshi/KuuOS/pull/2714) | 元18D真正`assoc/post/pre`三構成子の全再帰深さを、元17D raw source/target・元証拠を保持するCountable有限構文へ符号化。型不一致を拒否する依存型部分復号を構成し、**decode∘encodeが元の18D生成子全体に恒等**とLean証明。したがって**元raw17D total Countable ⇒ 元18D再帰Gen total・全indexed Genファイバー Countable**。GAと合成して**元AX base objectと元primitive Gen Countable ⇒ original18D source全体Countable**を証明し、真正旧FJ非空有限AQ文脈における元非可換kernel最小正規生成数`ℵ₀`をこの下位2条件のみで確立。9044/9044 scoped Strict Lean SUCCESS、6定理の標準3公理監査、Governance 30/30 SUCCESS | **残るのは真正下位AX base object/primitive Genの可算性条件の充足証明**。有限C60幾何から一般カテゴリーHom・Type値14D証拠は可算と仮定しない。別FK–FM忠実presentation、幾何的19D充填、元kernel自由基底、global strict/hyperdescentは独立未証明 |
| GC [#2716](https://github.com/itakura-hidetoshi/KuuOS/pull/2716) | 真の物理K5 primitive `Gen x y` は元15D full AX base Totalへの証拠保存単射を持ち、**base Total Countableだけで各primitive Gen Countable**。元14Dと各15D証拠ファイバーCountableがbase Total Countableを含意。元18D source全体と旧FJ非空AQ核の最小正規生成数`ℵ₀`の明示条件を下位1つに縮約。9045/9045 Strict Lean SUCCESS、5定理標準3公理以内、Governance 30/30 SUCCESS | 14D・15D元Type値証拠のCountableは未証明、C60幾何からHomの小ささを推論しない |
| GD [#2717](https://github.com/itakura-hidetoshi/KuuOS/pull/2717) | 原conservative 15Dと実AQ family 15D構文を完全元証拠保存の有限構文・依存型部分復号で再構成。**decode∘encode左逆**、original full core/family total・全indexed 15D fiber Countableを証明。**元14D Type値fiber Countableだけ**で原AX base Total・元18D source Countableと旧FJ非空AQのexact正規生成Cardinal`ℵ₀`を確立。9046/9046 Strict Lean SUCCESS、9定理標準3公理監査、Governance 30/30 SUCCESS | 任意カテゴリーHom・元14D依存型fiberの可算性は未証明。元の非可換群・旧FJ非忠実／FK–FM忠実区別・幾何19D・大域高次整合の境界を保持 |
| GE [#2719](https://github.com/itakura-hidetoshi/KuuOS/pull/2719) | 真のF112物理C60の60 Dart・90 Edge・32 Polygon・182 SiteのFintype⇒Countable、Site incidence HomのCountable、元の全dependent raw Zigzag経路total、元polygon bracket tree・primitive rotation・有限routeと全typed totalのCountableをLean4で形式化。9047/9047 Strict Lean SUCCESS、12定理公理監査標準3公理以内、Governance 30/30 SUCCESS | 直接14D derivingは7D–13D真正Type値証拠のCountableインスタンスがないため成立せず、**`Countable (NativeK5FifteenFourteenFiber W)`は未証明**。有限C60幾何≠一般カテゴリーHomや証拠全体の可算性。 |
| GF [#2721](https://github.com/itakura-hidetoshi/KuuOS/pull/2721) | 任意対象可算・全Homファイバー可算の一般カテゴリーにおいて、元の`KuuNativePath`全射履歴と`KuuNativeBlocks`全空block／source partitionを保存する有限構文、依存型部分復号、`decode∘encode`左逆、元full total・全indexed fiber Countableを証明。実F112 C60 `Site` incidenceへ特殊化し、元path・blocks・`PolygonNativeDualAxisFrame`の全元証拠保存Countableを確定。9048/9048 Strict Lean SUCCESS、13公理監査、Governance 30/30 SUCCESS | 任意カテゴリーD/E Homの可算性、元F45/F55～7D–14D証拠TypeのCountableは未証明。flatなpath評価と元blocks証拠、旧FJ非忠実と別FK–FM忠実を混同しない。 |
| GG [#2723](https://github.com/itakura-hidetoshi/KuuOS/pull/2723) | 元`KuuNativeOneStep`三構成子と元`KuuNativeAxisTrace`任意有限長の全構文を、元path/blocks・全中間依存型証拠を保持する有限コードへ符号化。部分復号の型不一致拒否と厳密な`decode∘encode`左逆を証明し、元Obj可算・全Hom fiber可算から全source total・全依存型fiber Countableを形式化。実F112 C60 `Site`へ無条件特殊化。9049/9049 Strict Lean SUCCESS、12公理監査、Governance 30/30 SUCCESS | F45/F55と真正7D～14Dの全Type値証拠のCountableは未証明。元14Dの条件付き旧FJ exact`ℵ₀`を無条件化したわけではない。 |
| GH [#2725](https://github.com/itakura-hidetoshi/KuuOS/pull/2725) | 元`KuuNativeF45Tree`の`refl/leaf/node`、C60 sector、実行順序、独立D/E Trace・全中間Blocks・Nat深さを保持する再帰符号化と境界検査付き部分復号、厳密`decode∘encode`左逆。局所可算D/Eから元F45 totalと各fiber Countable、真正C60 `Site×Site`および全Polygon totalについて無条件Countable。**3689/3689 scoped Strict Lean SUCCESS・8公理監査・Governance gate SUCCESS** | 任意D/E Hom、元F45 DepthRotationRoute／F55／7D～14DのCountableは未証明。旧FJ exact`ℵ₀`の14D仮定は残る。 |
| GI [#2727](https://github.com/itakura-hidetoshi/KuuOS/pull/2727) | 元のF45二軸から`LocalRotation`3構成子・`RotationEdge`正逆・任意有限`RotationChain`・`DepthRotationRoute`5構成子へ、全中間Type値証拠と両Nat等式輸送を保持する有限コード／型不一致拒否部分復号／厳密左逆を証明。一般D/EのObjおよび各Hom可算性から全証拠total/fiber Countable、真正C60 `Site×Site`と全Polygonでは無条件に成立。**3692/3692 scoped Strict Lean SUCCESS、24宣言公理監査、Governance 5/5 SUCCESS** | 真正元F55比較、4D～14Dの完全証拠型可算性、任意D/E Hom可算性、旧FJ exact`ℵ₀`の14D条件除去は未証明。 |
| GJ [#2729](https://github.com/itakura-hidetoshi/KuuOS/pull/2729) | 元F55平行F54経路・4段階pentagonと2局所回転squareの真正Type値原始証拠を可算化。**3693/3693 scoped Strict Lean・Governance SUCCESS** | 残り7つの再帰構成子はGJ2で形式化 |
| GJ2 [#2730](https://github.com/itakura-hidetoshi/KuuOS/pull/2730) | 独立F112の元F55 `PresentedCell`全9構成子を原証拠保存の有限構文に符号化し、D/E・Blocks・F45・F54中間境界を検査する部分復号と厳密左逆、元Type値総体・各fiber Countable。一般D/EはObj＋各Hom可算条件、実C60 Site×Site／全Polygonは無条件。**3695/3695 scoped Strict Lean SUCCESS、15公理監査、Governance 5/5** | 別定義`NativeF55StructuralComparison`、歴史的F55同型、4D～14D原証拠のCountableは未証明 |
| GK [#2732](https://github.com/itakura-hidetoshi/KuuOS/pull/2732) | 元F54 NativeF54StructuralSeam 14構成子の全原証拠保持コードと、別P92B新自然性生成子の6 F45 Tree・3 F54経路・両Nat深さの完全原始可算性を証明。**3697/3697 scoped Strict Lean SUCCESS、8定理公理監査、Governance SUCCESS** | 元構造seam全証拠はGK2で可算化済み。別P92B全証拠とStructuralComparisonは未証明。 |
| GK2 [#2733](https://github.com/itakura-hidetoshi/KuuOS/pull/2733) | 独立元 NativeF54StructuralSeam 全14構成子に対する型付き原始データ、境界整合性を検査する部分復号、厳密左逆を証明。一般D/E Obj・各Hom可算条件下で元14構成子 Type値総体・各indexed fiber Countable、物理C60 Site×Site／全Polygonでは無条件。**3701/3701 scoped Strict Lean SUCCESS、23新規公理監査、Governance 5/5 SUCCESS** | GK2時点で別P92B・別F55構造比較の全証拠は未証明（GK3 #2735で解決）。歴史的P92B/F55との完全型付き同型は未証明。 |
| GK3 [#2735](https://github.com/itakura-hidetoshi/KuuOS/pull/2735) | **別定義の元P92B比較9構成子と独立元F55 StructuralComparison 3構成子**の完全なF45/F54/D/E Blocks・Nat深さ・構造seam元証拠を保持する型付き有限構文、境界不一致を拒否する部分復号、厳密左逆を証明。一般D/EのObj・各Hom可算条件下で双方の元total/fiber Countable、C60 Site×Site／全Polygonで無条件。**3705/3705 scoped Strict Lean SUCCESS、21新規定理の公理監査、Governance 5/5 SUCCESS** | GJ2 PresentedCell・GK2 StructuralSeam・GK3二種の比較元証拠は異なるpresentation。歴史的P92B/F19/F28/F54/F55との型付き同型、真正14D Countableは未証明。 |
| GK4 [#2737](https://github.com/itakura-hidetoshi/KuuOS/pull/2737) | 元`NativeF55StructuralComparison`の構造seam追加に対して、境界保存`NativeF55P92AssocComparison`戻し写像の存在 **iff** 全元F54構造seamが同一元境界のP92B証拠で実現可能。元P92B `.original`・垂直`trans`を保存する再帰的拡張を構成。**3706/3706 Strict Lean SUCCESS、5/5 Governance SUCCESS、5宣言公理依存なし** | P92Bによる全seam実現の無条件の証明ではなく、歴史的presentation同型でもない。 |
| GK4B [#2738](https://github.com/itakura-hidetoshi/KuuOS/pull/2738) | 元P92B `.original` と元F54 seam `.structural` の原Type値構成子非同一性、任意元F54経路で元P92B埋込みの非全射性、元P92B恒等保存戻し写像の非単射性、GK4からの具体的戻し写像の非単射性。**3707/3707 Strict Lean SUCCESS、5/5 Governance SUCCESS、新規4定理公理依存なし** | no-goは元埋込み保存という比較条件に相対的で、無関係な抽象Type同値や全seamのP92B非実現を主張しない。真正14D・19D・hyperdescentは未証明。 |
| GK4C [#2740](https://github.com/itakura-hidetoshi/KuuOS/pull/2740) | P92A元`p92UnitContextWords`の長さを使い、真のF54ゼロ鎖原子数がP92B全9構成子（新`assocNaturality`含む）で保存することを証明。真正F54`leftUnit/rightUnit`の原証拠は個数を+1するため元P92Bで無条件に充填不能。元F45証拠がある文脈で全構造比較→P92B戻し写像は存在せず、真正C60北側六角形で実証。**3708/3708 scoped Strict Lean SUCCESS、Governance 4/4 SUCCESS、15宣言標準公理以内** | 数値shadowや商ではなく元Type値障害。全14 seamがそれぞれ非充填とは示していない。真正14D/19D・大域strict/hyperdescentは未証明。 |
| GK4D [#2742](https://github.com/itakura-hidetoshi/KuuOS/pull/2742) | 任意の元F45証拠`tree`の真のF54ゼロ鎖tower `Tₙ`を元Type値で構成。全Nat添字に対する`unitCount(Tₙ)=n+1`、元経路への単射、相異なる段のP92B比較不存在、一方で任意2段間に元F54 StructuralSeamと独立F55 StructuralComparisonを構成。既存GIの厳密元Fiber Countableと合わせ、一般D/Eの明示Obj・Hom可算条件および真正C60北側六角形で**元F54自己経路fiberのCardinal=`ℵ₀`**。**3709/3709 scoped Strict Lean SUCCESS、Governance 5/5 completed SUCCESS、13宣言標準3公理以内** | これは元F54証拠ファイバーの濃度であり、真正14DのCountable、旧FJの正規生成濃度、元19D filler、全構造seam 14構成子のP92B充填可否を同一視しない。 |
| GK4E [#2744](https://github.com/itakura-hidetoshi/KuuOS/pull/2744) | 既存元P92B witness-existence商と元`NativeF55StructuralComparison` witness-existence商を同じF45/F54依存型境界で構成。原P92B inclusionが誘導する正準全射は非単射で、GK4Dの相異なるunit塔が真のP92B商で別類、構造商で一類に潰れる。元P92B商**全体**および**指定の一つの構造類の逆像**の濃度`ℵ₀`を、一般D/E明示Obj/Hom可算性および真正C60無条件で証明。**3710/3710 scoped Strict Lean・Governance 5/5 SUCCESS、18宣言標準3公理以内** | 構造商が一点である、あるいは元の全Type値証拠を回復できるとは主張しない。 |
| GK4F [#2745](https://github.com/itakura-hidetoshi/KuuOS/pull/2745) | 元`RotationEdge.forward/backward`由来の真正2回転閉路と0回転unitを元Type値で構成。元F55全9・P92B全9・構造比較全3構成子の**0/正回転数不変量**を証明し、構造比較商で異なる二類が実在。GK4Dゼロ鎖towerを元2回転閉路に後合成して**第二の異なる可算無限P92B商ファイバー**を導出、実C60の**同一北六角形F45 triple**で二構造類の逆像がそれぞれ`ℵ₀`と証明。**3711/3711 scoped Strict Lean、Governance 5/5 SUCCESS、17宣言標準3公理以内** | 構造商全体の濃度・全構造seam個別P92B充填、真正14D・19D・hyperdescentは未証明。 |
| GK4G [#2747](https://github.com/itakura-hidetoshi/KuuOS/pull/2747) | 原F54回転数`=0`を`Bool`へ決定化した実グレードが、元P92B商・別F55構造比較商の両方に**厳密降下**し、GK4E正準商全射`π`と可換。降下の代表値による**一意性**を証明。真正元F54局所回転の0-edge/2-edge証拠から両商でBoolへ**分裂全射を与えるsection**を構成、二sectionは正準全射と可換。0回転unit塔／正回転backtrack塔とGI可算性を用いて元P92B商**Bool両グレード全ファイバーそれぞれexact `ℵ₀`**。一般D/Eは明示Obj/各Hom可算仮定、真正C60北六角形で無条件。構造商はCountableかつBoolへ全射。**3712/3712 scoped Strict Lean・Governance 5/5 SUCCESS、28宣言標準3公理以内** | 商全体をBoolと同型とはしない。真正14D・19D・高次descentは未証明。 |
| GK4H [#2749](https://github.com/itakura-hidetoshi/KuuOS/pull/2749) | 真の元F54`trans`回転数加法と**`grade(trans u v)=grade(u) && grade(v)`**。原P92B全9のpre/postおよび元F54 StructuralSeam全14のpre/postを使い、別F55構造比較全3構成子の原Type値pre/post輸送を導出。両方の実証拠存在商で`Quotient.liftOn₂`による**完全依存型合成**のwell-definednessを証明し、Boolグレードの乗法性・GK4E正準全射の合成保存を確立。独立構造商の合成は元F54`reassoc/leftUnit/rightUnit` seamから**結合律・左右単位律**が成立。一方、元P92B商の真正ゼロ鎖unitは**左右単位律不能**であり、Boolが同値でも元P92B類は異なる。真正C60の同一北六角形F45 tripleへ無条件特殊化。**3713/3713 scoped Strict Lean、5/5 Governance SUCCESS、21宣言標準3公理以内** | P92B商の結合律や別の単位候補の不存在一般、歴史的型付き同型、真14D Countable・19D・global strict・hyperdescentを導かない。 |
| GK4I [#2751](https://github.com/itakura-hidetoshi/KuuOS/pull/2751) | 元F45完全Type値Treeと二Nat深さを固定した原D/E Blocks境界のΣ対象に束ね、既存の元`NativeF55StructuralComparison`証拠存在**商**をHomとしてmathlib `Category`を構成。`id/comp`および**結合律・左右単位律**はGK4Hの真正F54構造seamによる既証明法則を使用。新しい一対象`Bool`圏は単位`true`・合成`&&`で全公理証明。GK4G真のF54回転0/正グレードをGK4Hの乗法則から**mathlib実`Functor`**へ昇格。真正C60北六角形三重F45 stageで関手が単位→true、2回転backtrack→false、構造homのCountableも物理Site/Hom証明で確立。**3714/3714 scoped Strict Lean・Governance 5/5 SUCCESS、14宣言標準3公理以内** | 元P92B商の真正ゼロ鎖は左右単位律no-go。構造商≅Bool、関手faithfulness、歴史的型付き同型、真正14D/19D/hyperdescentは未証明。 |
| GK4J [#2753](https://github.com/itakura-hidetoshi/KuuOS/pull/2753) | 元F54の**真の原始経路項数**（chain・castDepths各1、trans加法、context保存）が全経路で**正**。元F55全9・元P92B全9生成子が**物理原始回転数0のsourceでは項数を保存**することを原Type値3-cell証拠帰納法で証明。正回転pentagon3対2は除外し全域保存は主張しない。任意の元F45 stage、任意元P92B自己経路商類`e`について**左単位も右単位も不可能**を真の反射経路との比較・項数加法から証明。全stage上の一括単位割当のno-go、真正C60北六角形での候補独立左右no-goと別GK4I構造商の左右単位を比較。**3715/3715 scoped Strict Lean・Governance 5/5 completed SUCCESS、14宣言標準2公理以内** | no-goは固定GK4H真正商合成だけ。別の合成、P92B結合律、歴史的同型、真正14D Countable・19D・hyperdescentを推論しない。 |
| GK4K [#2755](https://github.com/itakura-hidetoshi/KuuOS/pull/2755) | 真正F54原始leaf項数を物理回転数0のみ`some n`とする`Option Nat`観測が元P92B商へ厳密降下し、代表元で一意。`Option.isSome`はGK4G Bool gradeと一致。`some n`は正、`some 0`は原P92B商に存在しない。GK4Hの既存真正商合成は`some a⋆some b=some(a+b)`・`none`両側吸収を保存。物理C60北六角形に無条件特殊化。**3716/3716 scoped Strict Lean・Governance 5/5 completed SUCCESS、19宣言標準3公理以内。** | `Option Nat`は別の原P92B合成ではない。正回転pentagon項数保存、原P92B結合律、真正14D Countable・19D・hyperdescentは未証明。 |
| GK4L [#2757](https://github.com/itakura-hidetoshi/KuuOS/pull/2757) | GK4E正準全射`π`を介した任意値域観測の**降下必要十分条件＝π-fiber上一定**。元GK4D真正unit towerのGK4J primitive leafCountは`k+1`、GK4K Option Nat値は`some(k+1)`。全塔はGK4E構造商で同一類だが数値観測は単射、よってOption Nat観測はいかなる構造商関数からも引き戻せない。任意F45自己P92B商の`some n`達成は`n>0`と同値。GK4G Bool gradeは降下可能。真正C60北六角形で無条件。**3717/3717 scoped SUCCESS、Governance 5/5、13宣言標準3公理以内。** | 不降下は特定GK4K Option NatとGK4E構造商に限定。P92B別合成・結合律、真正14D Countable・19D・hyperdescent未証明。 |
| GK4M [#2759](https://github.com/itakura-hidetoshi/KuuOS/pull/2759) | 任意値域型`B`の`f:Option Nat→B`によるGK4K観測の後処理が、実GK4E正準全射を通じて構造商へ降下する**iff `∀n>0, f(some n)=f(some 1)`**を証明。全正整数ペア同値条件、実GK4G構造商Bool gradeを経由する明示的因子、正準全射による降下因子の一意性、`Option.isSome`の降下／恒等後処理不降下、真正C60北六角形で無条件特殊化。**3718/3718 scoped SUCCESS・Governance 5/5 completed SUCCESS、13宣言標準3公理以内。** | GK4K由来後処理のみの分類。元P92Bの任意観測や結合律・別合成、真正14D Countable・19D・hyperdescentは未証明。 |
| GK4N [#2761](https://github.com/itakura-hidetoshi/KuuOS/pull/2761) | **任意値域B・任意の元P92B商上観測**がGK4E独立構造商へ降下する iff、真正F54 Type値構造seam全14を保存（元P92B比較保存は商の定義で既知）。真のF55構造比較3構成子の全帰納・GK4Lの商ファイバー一定条件で証明し、因子の一意性も示す。**任意の生F54観測**なら元P92B全比較とF54全seamという二族保存が必要十分。GK4G Bool gradeは保存、GK4K Option Natは**真正左単位seamによる`some 2≠some 1`**で失敗、物理C60で無条件。**3719/3719 scoped SUCCESS・Governance 5/5 completed SUCCESS、13宣言標準3公理以内。** | 固定GK4E構造商についての条件。元P92B結合律・別合成、真正14D Countable・19D・hyperdescentは未証明。 |
| GK4O [#2763](https://github.com/itakura-hidetoshi/KuuOS/pull/2763) | 任意B値の元P92B観測を全F45境界・Blocks・二Nat深さにわたる関数族へ拡張。**観測等式kernelが真正前後合成・左右contextで保存される4条件を明示仮定した下で**、真のF54構造seam全14の保存が**基本7生成子（reassoc・左右unit・左右contextのtrans/unit）保存とiff**。GK4Nの真正GK4E降下条件と接続。Boolean gradeは全seam保存、Option Natは真正左単位seamで`some 2≠some 1`。**3720/3720 Strict Lean・Governance 5/5 SUCCESS、17宣言標準3公理以内。** | kernel互換性は任意観測の自動性を未証明、7生成子の最小性未証明。元P92B結合律・14D Countable・19D・hyperdescent未証明。 |

実際のDV完全コード写像を `f_w`、その非可換自由群準同型を `τ_w`、17D文脈対象作用を `C_w` とすると、証明済みの**条件の分離**は次です。

$$
\operatorname{Injective}(\tau_w)
\iff \operatorname{Injective}(f_w)
\iff I_{\mathrm{assoc}}(w)\land I_{\mathrm{post}}(w)\land I_{\mathrm{pre}}(w).
$$

さらに先行FI [#2675](https://github.com/itakura-hidetoshi/KuuOS/pull/2675)では、元の完全18D非可換自由群から**全入れ子構成子列**への自由群準同型 $S_{\mathrm{orig}}$ と、文脈閉包先の対応写像 $S_{\mathrm{closed}}$ を構成し、$S_{\mathrm{closed}}\circ\tau_w=S_{\mathrm{orig}}$ および **$\ker(\tau_w)\subseteq\ker(S_{\mathrm{orig}})$** を無条件に証明しました。この必要条件は最上位の3セクター判別より強い一方、同じ再帰列の元raw17D引数や生成子ファイバーの忠実性は保証しません。

後続FI [#2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676)で、この三セクター条件を元の17D文脈対象作用の単射性へ正確に還元しました。すなわち任意の固定有限文脈 $w$ について **$\operatorname{Injective}(\tau_w)\iff\operatorname{Injective}(f_w)\iff\operatorname{Injective}(C_w)$**。後続FJ [#2679](https://github.com/itakura-hidetoshi/KuuOS/pull/2679)は、具体的に`S=nativeK5AXKuuSignature W`、`F=nativeK5BCFrame W`とした**選択物理AQモデル**で、`C_w`（従って`τ_w`）は任意の**非空**有限語で**非単射**と証明しました。一方、空語での単射性はFIから従います。

**依然として未証明：** FNで選んだ17D identity・18D reflexive-associatorの**2証拠以外**について、旧新の異なる閉包生成子Type値全体をつなぐ構成子保存比較関手や自然性・higher coherence、旧FJの非可換自由群核の完全な正規生成表示、任意の別presentationでの忠実性、元のC60幾何での真正19D Type値充填、異なる高次証拠の同一性、大域strict 3/n圏、`(∞,3)`-hyperdescent。**DSの完全証拠保存no-go**と旧P62/P77/P80/P87/P88の各presentation固有の障害を維持します。

より具体的な優先順位とLeanファイルへの導線は[ROADMAP](ROADMAP.md)を参照してください。以下の長いP58–P91記録は歴史的な検証台帳として保持しており、**現在の最終段階ではありません**。

## 最新のLean定理統合 — F112-P94D3GK4BI / 2026-11-01 JST

**既存K_AIと真正実到達AH行列圏のMathlib圏同値を構成 — [定理PR #2861](https://github.com/itakura-hidetoshi/KuuOS/pull/2861) MERGED。** [Lean全文](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BIAttainedAHCategoryEquivalence.lean)・[正式証明記録](docs/formal/GK4BI-genuine-attained-ah-category-equivalence.md)。GK4BFで構成した元F54型付きHomの**実際に到達した**AH行列圏と既存第二kernel圏`K_AI`について、GK4BHの各Hom全単射を使い、真正F45境界を保持する対象Equiv、Hom Equivと両側逆、全忠実性、対象全射、Mathlib `Functor.IsEquivalence`を構成。**`nativeGK4BIAttainedAHEquivalence`** は真の `CategoryTheory.Equivalence` であり、その順方向は旧 `nativeGK4BFImageFunctor` と定義的に一致。逆Mathlib Functor、自然なunit/counit同型と三角恒等式までLean証明済み。全整数行列圏への同値、元Type値F54 raw経路の同一性、独立構造商Sの忠実性、元Q自身の未証明圏公理は主張しない。

**exact-source：** 最終source HEAD `e880646a2811e98ffc6cb04436520cdc7b4bd952`、test-merge HEAD `99e46f575cec532700870f7b4112d6a9c0092518`、**両者同一tree** `2d2e043b69a2f09f98196a0dc4a3826ccf7e1b04`、[CI #41263880913](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41263880913) **Strict Lean 3804/3804 SUCCESS、Governance terminal SUCCESS**。変更Lean1ファイルの14宣言が標準3公理 `propext`・`Classical.choice`・`Quot.sound` 以内（対象同値は公理依存なし）、sorryAx0、変更ファイルerror/warning 0/0。初回CIでは型クラス値を返す定義のLean4透明性規則によるエラーをpinned mathlib APIと照合し、`@[implicit_reducible]`で修正、再検証成功。定理squash SHA／当時canonical main `87f60307fc1441a8d7a8040758e9271f65ca3283`。

**残存境界：** 元Q圏公理、独立S→K_AI忠実性、元Type値完全同値、全整数行列到達、真正14D無条件Countable、19D filler、global strict、hyperdescent未証明。Lean v4.30.0-rc2／pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR #1558 Draft・OPEN・未マージ、strict空中心・独立Kuuは一presentation、Gray再導入なし。旧GK4BH欄の「次GK4BI」はその時点の履歴とし、この欄が確定済みの最新結果。

## 最新のLean定理統合 — F112-P94D3GK4BH / 2026-11-01 JST

**元F54真正型付きK_AIの旧AH観測忠実性を、first jet・物理rank・Boolean gradeから証明 — [前半 #2858](https://github.com/itakura-hidetoshi/KuuOS/pull/2858)、[後半 #2859](https://github.com/itakura-hidetoshi/KuuOS/pull/2859) ともにMERGED。** [first jet Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHFirstJetADRecovery.lean)・[grade/rank忠実性Lean](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHGradeRankFaithfulness.lean)・[正式証明記録](docs/formal/GK4BH-first-jet-grade-rank-ah-faithfulness.md)。真正F54の元多項式行列の係数から、旧GK4ADの符号付きcast charge・後退数・非可換順序付きmomentを復元し、GK4BAのt=4一点決定性で元AH一致から旧AD一致を証明。さらに実F54の後退数≤原始回転数とzero-rotationの元左rank保存、GK4AC前進rank不等式により **Boolean grade=true iff 後退数0かつ元始終点rank一致** を形式化した。

**主定理：** `nativeGK4BHKernel_AH_injective` は既存の第二kernel圏 `K_AI` の任意の型付きHomでAH値一致からHom等号を導く。旧AH関手の各Hom単射 `nativeGK4BHOldAHFunctor_injective_hom` と、実到達AH像へのGK4BF関手の各Hom全単射 `nativeGK4BHImageFunctor_bijective_hom` が成立。固定AHファイバーは高々一元、GK4BGの残余AH衝突は存在しない。**元Type値F54経路自身の同一性、独立構造商Sの忠実性、全整数行列圏への全射は含意しない。**

**exact-source：** #2858 source `d7aa7798a4a39e7450532dab02f0910c1c073adb`、test-merge `77fb5d2eefbc7fa1ae2c5d7b5e48ad990e092882`、tree `d1c3413213a8b8469cf8c8da93d71778035ae512`、[CI #41260074882](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41260074882) **Strict Lean 3802/3802・Governance SUCCESS**、12宣言、squash `93db9b5f77c8554f9fc52a7c7f057188de1b83a0`。#2859 source `2c16bad8e8a893c66dda68c28da1625c82bf6f83`、test-merge `3ae76d2513ad9748ff111fafe3754f5717373bbd`、tree `f87b3edba4497d24229339cd6c71685986c9e84e`、[CI #41260689362](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41260689362) **Strict Lean 3803/3803・Governance SUCCESS**、12宣言、squash `d4c435af91f4b4d9f605ee8739b6b758b79003d0`。合計24宣言は標準3公理以内、sorryAx0。canonical main `d4c435af91f4b4d9f605ee8739b6b758b79003d0`。Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、保護#1558 Draft／OPEN／未マージ維持。

**次GK4BI：** 既存の各Hom全単射と同じ真正型付き対象表示を使い、`K_AI ≌ 実到達AH行列圏` のMathlib圏同値を構成。逆Hom写像、逆関手の単位・合成保存と自然unit/counitを証明する。元Q圏公理、S忠実性、元Type値完全同値、全整数行列到達、真正14D無条件Countable、19D filler、global strict、hyperdescentはなお未証明。旧GK4BG欄の「GK4BH未形式化」は当時の履歴であり、この最新欄が現在の到達点を記録する。

## 研究の全体像：一般理論が先、C60は後から導入した検証の場

研究は二つの相互に照らし合う方向から進みます。

1. **既存の一般理論を継承・深化する。** C60以前からのcontext、transport、refinement、presentation-independent localization、sheaf/stack descent、bicategorical・simplicial coherence、operadicな複数条件、obstruction、普遍性、およびactual-lift / biadjunctionの形式的成果を、その原型・仮定・定理名のまま保持します。
2. **真正C60と独立Kuuで具体的に検証する。** 有限だが非自明な入射幾何・raw高次証拠・位相・曲率・非降下を使い、一般理論の仮定が実際に成立するか、何を失うか、どの厳密法則が障害に遭うかを調べます。独立Kuuはこの作業に便利な一つのpresentationであって、「唯一の空」ではありません。

~~~text
C60以前からの縁起の一般理論（v0 → v1 → v2 → v4/v5）
  context / transport / W-localization / J-descent / higher coherence
  universality / obstructions / biadjunction / proof-relevant paths
                      ⇅ 具体化・反例・比較・一般理論への反映
真正C60・独立Kuu（後から導入した有限幾何による検証）
  incidence / paths / raw 2・3-cell / quotient / phase / obstruction
                      ↓ 未証明部分を厳密に追究
非自明な証拠を保持する局所strict 3圏 → 大域strict 3圏 → strict n圏
                      ↓ 別途必要な比較・モデル化の証明
                 (∞,3)-hyperdescent
                      ↓ 適用範囲と仮定を明確に一般化
                  縁起の一般理論の深化
~~~

この図は**研究上の証明計画**であり、後半の矢印がすでにLeanで成立したという主張ではありません。一般理論はC60からしか得られないものではなく、C60の成果が一般理論へ逆向きに検証・修正を促します。

## C60以前に構築した縁起の一般理論（生きた定理群）

以下は新しい独立Kuuの前史として退けるものではなく、**現在も同じ公開Leanパッケージに属する数学的成果**です。それぞれのソースに明示された条件の範囲で扱います。

| 系列 | 数学的到達点と正確な範囲 | 代表的なLeanソース |
| --- | --- | --- |
| **v0–v1：縁起と関係のtransport** | Contextの圏、状態関手、合成に沿うtransport、不変readout、文脈的descent、複数条件のoperadic構成・高次比較の入口。物理的因果の実証は含まない。 | [FunctorialTransport v0.1](formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean) · [CoreSpine v1.7](formal/KUOS/DependentOriginationCoreSpineV1_7.lean) |
| **v1：nerve・scaled horn・homotopy** | Duskin nerveとhigher coherence。v1.33はhorn境界のhomotopyとstrict fillerを区別し、homotopyからstrict fillerへのrectificationを明示的な追加条件として切り分けた。 | [ScaledHornHomotopyDescent v1.33](formal/KUOS/DependentOriginationScaledHornHomotopyDescentV1_33.lean) |
| **v2.0：presentationの普遍性** | 許容する変更`W`の局所化`C[W⁻¹]`、`W`を同型へ送る関手の普遍的因子化、および同一普遍性を持つcarrier間の圏同値。`W`以外のすべての表示変更を自動的に反転するわけではない。 | [PresentationUniversality v2.0](formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean) |
| **v2.1–v2.7：descentとW+J分類** | Grothendieck topology `J`、sheafの局所大域条件、局所化後のsheafと元の適合する文脈系との**圏同値**。`H`まで含む最終完成を意味しない。 | [WJCategoryEquivalence v2.7](formal/KUOS/DependentOriginationWJCategoryEquivalenceV2_7.lean) |
| **v2.8–v2.13：Cat値stackと高次局所化** | Cat値擬関手の被覆に対する実効stack descent、precoverageの閉包条件下での特徴付け。厳密に`W`を反転する`C ⥤ Cat`に対する局所化の存在・一意性を証明。任意の弱い擬関手の普遍的高次局所化やhyperdescentは未証明。 | [HigherStackDescent v2.8](formal/KUOS/DependentOriginationHigherStackDescentV2_8.lean) · [StrictHigherUniversality v2.13](formal/KUOS/DependentOriginationStrictHigherUniversalityV2_13.lean) |
| **v4.00–v5.101：obstructionと高次普遍性** | 非因子化・局所化・明示的障害・exact-universal比較、実際の`F,G,η,ε`・triangulator・前後swallowtailを積み上げ、**同じoriginal actual-lift datum**上でcoherent biadjunction carrierを構成。一般のstrict 3圏を完成させたわけではない。 | [CoherentBiadjunctionActualLift v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) |
| **v5.102–v5.153：高次の具体的証明構文** | mates、二軸のType値履歴・交換類・完全normal form、任意有限長の回転木、五角形・正方形3-cell提示。**raw証拠を観測商へ写すと非忠実になる**実際の反例と復元不可能性を証明。 | [F55 raw cells](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean) · [F56 observation nonfaithfulness](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean) |

これらは**縁起の一般化がC60以前から実際に進んでいた証拠**です。「C60でstrict 3圏を証明してから初めて一般理論に着手する」という順序にはしません。一方、それぞれをそのまま厳密な大域3圏や`(∞,3)`-hyperdescentの完成証明とも呼びません。

歴史的な詳細・定理の成立範囲・原型を残した[旧README v5.291](docs/legacy/README-v5.291.md)と[旧ROADMAP v5.291](docs/legacy/ROADMAP-v5.291.md)も参照してください。**歴史的定理は`formal/KUOS/`の現行ソースでも生きています。`legacy/`への隔離・一括廃止ではありません。**

## 空の空・presentation・Grayの位置づけ

- **どのpresentationも空そのものではありません。** 古いF94/F95の荷電と位相を伴う商、現在の独立Kuu商、Qiの経路観測合同、C60のraw証拠も、それぞれ特定の関係と観測に相対的です。異なる表示が交換可能なら保存量と比較写像を証明し、交換できないなら差異とobstructionを保持します。
- **Gray圏をstrict 3圏の代替にしません。** Gray圏が与える弱いinterchange/coherenceは、KuuOSが次に要求するstrictな3次元合成律・交換律を証明したことにはなりません。研究上のstrict 3圏目標を「Gray圏ならできる」と弱めて完了扱いしません。
- **過去のGray・bicategoricalな数学を消しません。** 既存の証明は元の型と仮定のまま保存・利用します。ただし独立Kuuの原始構成や、これからのstrict 3/n圏の証明根拠としてGray固有の公理を密輸入しません。
- **strict 3圏の証明も空の唯一性の証明ではありません。** それは現在の研究経路に設定した不可欠な数学的到達目標です。成立を証明できなければ不足条件・no-go・非零obstructionをそのまま提示し、証拠を消す商や法則のすり替えで解決済みにしません。
- **mathlibを積極的に使用します。** 高次圏・局所化・sheaf・simplicial/homotopy・代数的トポロジーなどの定理を再利用します。Gray非依存とmathlib非依存は無関係です。

## 真正C60・独立Kuuの構成履歴とstrict 3圏の未解決境界

### C60の現在の前向き表示：入射グラフよりゲージ接続と真正Type値証拠を優先

[ゲージ移行方針・数学的監査](docs/C60_GAUGE_PRESENTATION_MIGRATION.md)を研究規則とする。真正C60の60 Dart・90 Edge・32 Polygon・360 flagsを変更せず、入射グラフの隣接やK₅の組合せ論的貼り合わせを高次coherenceの証明と取り違えない。[真正C60ゲージ場と32面曲率](formal/Kuu/F112/PolygonNativeC60PhysicalGaugeAtlas.lean)、[真正P92Bの非可換ゲージ障害](formal/Kuu/F112/PolygonNativeC60K5TypedGaugeCoherence.lean)、[Qi v3.4の位相枠](formal/KUOS/Architecture/QiWuxingNativeC60GaugeV3_4.lean)を比較表示として使う（[PR #2510](https://github.com/itakura-hidetoshi/KuuOS/pull/2510) MERGED）。有限グラフや歴史的Quiver、旧no-go、非零曲率は保存する。元のK₅形式的9面語と、実際のF54依存型境界を貼り合わせた3-cellを混同しない。

### 2026-10-24の証明履歴：真正K₅九面の向き・非可換境界・独立4次元生成子

[P94D3Q #2519](https://github.com/itakura-hidetoshi/KuuOS/pull/2519)・[P94D3R #2520](https://github.com/itakura-hidetoshi/KuuOS/pull/2520)は、P92Bの反転した自然性square2の真正F54構造的seamと、従来の全球shellingの向きの不整合を明示した。既存shellingに必要な構造的seamを仮定で埋めず、文脈深さ列の保存不変量により、その構造的presentationでの不可能性をLeanで証明した。8面の実Type値貼り合わせと反転square2は同じ始終F54経路を持つ平行3-cellであり、自然性数はそれぞれ+2、−1。

[P94D3S #2521](https://github.com/itakura-hidetoshi/KuuOS/pull/2521)は**square2の3-cell向きを明示的に再反転**し、元の面順序を保った真正Type値9面閉路を別の構造的presentation上に構成した。旧形式的9面語を `W_old`、最初の7面の群語を `S`、旧反転square2の語を `q` とすると、`W_old` の自然性数は1、真正貼り合わせ `W_typed` は3である。さらに非可換順序を保持して `W_typed · W_old⁻¹ = S · q⁻² · S⁻¹`、相対自然性数+2を証明した。**元の自然性数1の語自体が貼り合わせ可能になったとは主張しない。**

[P94D3T #2522](https://github.com/itakura-hidetoshi/KuuOS/pull/2522)は、この**実際に構成した**自然性数3の9面Type値3-cellを境界に持つ、別の独立4-cell生成子を宣言し、その完全な非可換語と旧P94A四射relatorの正規閉包をmathlibで構成した。旧核の真の拡大、旧F55 signed/odd shadowの降下、自然性数の非降下、共役作用・境界同変性・**正規核の代数的Peiffer恒等式**をLeanで証明した。生成子の宣言とその正規核の代数的Peifferは、**新しい4-cell Type値文法の任意whiskering/interchange coherenceの証明ではない**。旧P92Bへのdescent、元の形式的 `W_old` の真正4次元充填、局所・大域strict 3/n圏、`(∞,3)`-hyperdescentは未解決として残る。



C60では元の正二十面体に由来する**60 Dart、90 Edge、32 Polygon（12五角形・20六角形）、360 incidence flags**を用います。この有限幾何は、以前に構築した高次理論を**具体的・真正な境界と証拠のもとで試験する場**です。

- [`Kuu.Presentation`](formal/Kuu/Presentation.lean)：選ばれた境界付き自由経路と明示的な関係に相対的な商、核、観測関手の因子化。
- [`Kuu.Strict`](formal/Kuu/Strict.lean)：関手・自然変換の結合律、単位律、2次元のstrict interchange。**これはglobal proof-relevant strict 3圏の証明ではありません。**
- [`Kuu.Incidence`](formal/Kuu/Incidence.lean)：文脈に沿う切片図式とGrothendieck総圏。
- [F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)：Grayを原始基礎としない真正C60のF42/F54/F55、局所化、型付き高次証拠の移行。**MERGED：現在はmainに統合済み**。
- [F112-P56 #2418](https://github.com/itakura-hidetoshi/KuuOS/pull/2418)–[P57 #2420](https://github.com/itakura-hidetoshi/KuuOS/pull/2420)：独立F55九生成子のraw輸送、水平自然性、selected shadowのfaithfulnessと失われるraw情報を区別。
- [F112-P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421)：raw F55構文はそのままでは**strictな左右単位律・結合律を満たさない**ことをnode-countで証明。mathlibの自由経路圏を別途構成。
- [F112-P59 #2423](https://github.com/itakura-hidetoshi/KuuOS/pull/2423)、[P60 #2424](https://github.com/itakura-hidetoshi/KuuOS/pull/2424)・[#2425](https://github.com/itakura-hidetoshi/KuuOS/pull/2425)、[修復 #2428](https://github.com/itakura-hidetoshi/KuuOS/pull/2428)：垂直raw単位・合成を自由経路の空経路・連結へ正規化し、残る７種を証明依存生成辺として保持。自由経路の正規化関手と選択されたshadow観測への因子化を証明。数値観測からraw履歴は一般には復元できない。
- [F112-P61 #2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426)：垂直正規化された水平合成は２辺の経路。２つのraw単位セルを水平合成しても空経路にはならないという**限定された水平単位律obstruction**を示す。大域strict 3圏の不可能性ではない。
- [F112-P62 #2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429)：９構成子を再帰的に検査した**単位生成raw構文**だけを対象に、型付き自由経路合同関係を生成。垂直経路合成との整合性と選択されたshadowへの健全性を証明し、P61の水平単位経路と空経路がこの関係で結ばれることを証明。真正C60の五角形・六角形生成元は単位構文から除外。**水平合成の全関手性・交換律・大域strict 3圏はなお未証明。**
- [F112-P63 #2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431)：９構成子の再帰から`unitOnly`のF54始終点が同一であることを証明。mathlibの`Paths.lift`で左右contextの**証明依存raw自由経路関手**を構成し、垂直合成と単位生成構文の保存、context付きraw単位とstrict単位のP62関係を証明。raw生成履歴は消去しない。
- [F112-P64 #2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432)：P62の明示的な型付き合同関係をmathlibの`Congruence`・`CategoryTheory.Quotient`で**実際の垂直商圏**として構成。商圏の射の等号とP62関係の必要十分性、P61水平単位の商圏上の単位等式、選択されたshadow観測の因子化、raw生成元の観測量保存を証明。**選択shadowと一致するraw証明項を一括同一視する商ではない。**
- [F112-P65 #2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434)：P59によって**単一の生成辺として残る**unit-only raw証明セルを明示的に区別し、真正C60の証明履歴を保持する型付きunit wordを構成。P62関係の全５規則がP63の左右context関手で保存されることを証明し、mathlib `CategoryTheory.Quotient.lift`によりP64の最小商圏へ**左右２つの関手を実際に降下**させた。商関手との等式を双方で証明。raw `ident`生成辺全体の無条件消去やshadow値による同一視は行わない。
- [F112-P66 #2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436)：P64の単位生成合同商は**3射の射集合に作用し、F54の経路対象を同一視しない**ことを一般の２軸Nat深さで証明。実C60六角形の左右順序の異なるF54回転経路は商圏上でも異なる対象であり、それらを結ぶ真正F55交換正方形3射は残存する。選択されたshadowの交換位相`1 : ZMod 2`も非零のまま保存。これはP62〜P65だけから**厳密なinterchange等式を導けない**という現在のpresentationの具体的障害であり、一般的strict 3圏の不可能性定理ではない。
- [F112-P67 #2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438)：真正F54のdisjoint-square比較を**Type値の証拠**として構成し、各比較証拠から元の型付きF55 raw 3-cellを復元。比較クラスの等号はこの証拠の`Nonempty`と同値であり、具体的証明履歴を選ぶ操作ではない。実C60の左先・右先回転順序が比較クラスで等しくなる一方、元のF54経路は異なり、**その同一視を行う任意の写像は単射になれない**ことを証明。選択された非零交換位相とraw証明履歴は別データとして保持。
- [F112-P68 #2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439)：全９構成子を再帰的に検査し、真正五角形生成元を含まない**squareOnly**なF55 raw証拠をType値で保持するcontext閉包比較を構成。P67比較クラスから新クラスへの写像、**左右F54 contextの商上の作用**と元の経路への正確な整合、実C60六角形の交換比較をLean4で証明。五角形生成元はsquareOnlyの原始生成元から除外。P67とP68が同値であることや全3-Homの輸送までは主張しない。
- [F112-P69 #2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441)：P68のF54比較クラスを始点・終点に持つ型付きF55高次射パッケージを構成。元の２つのF54代表経路と真正F55 raw 3-cellをType値で保持し、元の履歴保存と比較クラス等号から得られる比較証拠の存在を証明。**代表元の一意な選択・新しい高次圏の全合成は未証明。**
- [F112-P70 #2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442)：選択された真正squareOnly比較証拠による**両端代表元の輸送**と、中間比較証拠を指定した**高次射の合成**をType値raw F55構文で実装。選択shadowの加法公式を証明。実C60六角形では同じ商クラスを両端に持つ恒等3射（位相0）が交換正方形で輸送されると、元のraw証明項の位相が1に変化することを証明。**選択証拠に依存した合成を、代表元独立な全合成と混同しない。**
- [F112-P71 #2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444)：P70代表元変更から生成する高次射の輸送同値関係と商を構成し、商での等号の必要十分性を証明。輸送同値な元の高次射でraw shadowが異なれば、**元の数値shadowを全代表元で保つ商への因子化は不可能**という限定されたno-goを証明。真正C60の位相差と輸送同値を接続。ただし補正付き・gradedな高次Homは否定しない。
- [F112-P72 #2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446)：P70の**選択された真正比較証拠**による代表元輸送・中間経路のbridge合成で、元raw shadowに加わる成分を明示して補正。２段階の輸送で補正値が整合する加法cocycle公式と、真正C60交換正方形で補正前位相1・補正後位相0を証明。補正は証拠選択に依存し、P71無補正shadowの商への因子化ではない。
- [F112-P73 #2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447)：P68の`squareOnly`判定を全９raw構成子で帰納的に解析し、比較証拠の**五角形chargeが0**であることを証明。P70の左右代表元変更とbridge付き合成、P71輸送同値の全４生成規則で元の五角形整数chargeが保存されることを示し、P71商上の真正なcharge観測関数を構成。真正C60の非零交換位相とは独立に成立。
- [F112-P74 #2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448)：元の整数線形観測`a×五角形charge + b×交換charge`について、**元の交換chargeを1だけ変化させる輸送が存在する固定されたP71商では、全代表元と一致する無補正readoutが存在する必要十分条件は`b=0`**と証明。十分性はP73の五角形chargeから構成し、必要性は実際の輸送同値と加法性から導出。真正C60交換正方形で交換charge 0→1を確認。すべてのgraded高次観測を分類したとは主張しない。
- [F112-P75 #2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450)：P71の輸送４生成規則を**真正のType値graded輸送履歴**として持ち上げ、元F55 shadow全３座標（五角形整数・交換整数・奇偶位相）の加法gradeを保持。輸送履歴に対するshadow加法の健全性、固定raw両端でのgrade一意性、閉路grade0、Prop値P71輸送関係とgraded証拠の存在の必要十分性を証明。真正C60の交換正方形でgradeの交換整数+1・奇位相非零を確認。**raw履歴の同一視、全3-Hom構成、strict interchangeを主張しない。**
- [F112-P76 #2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451)：真正F55 squareOnly比較証拠の縦合成、二段階代表元輸送と合成比較の**正規化自由経路・全選択shadowでの整合性**を証明。旧bridgeと新bridgeの差分を実証拠の加法として正確に記録し、**比較経路の等号を明示的に仮定した場合に限り**合成経路等号を導出。真正C60交換正方形のraw履歴は単位左合成と異なるが、正規化経路・shadowは一致。raw 4-cellの無条件存在やstrict interchangeは未証明。
- [F112-P77 #2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452)：真正九構成子F55 raw 3証明間に**Type値の八生成規則による縦4-cell証拠**（反射・対称・推移・左右whisker・左右単位・結合）を構成。P59正規化経路と選択shadowへの健全性を**別々に証明**し、P62単位合同と接続。4-cell証拠の存在だけを関係とする正確なSetoid・商を作り、実C60のraw非同一な二証明間の4-cellを構成。全ての同値shadow・同値経路から証拠が得られるとは言わない。
- [F112-P78 #2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453)：P77の**真正4-cell合同による縦合成のwell-definedness**を証明し、元のF54経路上に、P77商をHomとする別の明示的Mathlib `Category`構造を実装。単位・結合はP77のraw4-cell証拠から証明し、正規化経路と全shadow観測の合成保存を証明。**局所的な厳密な縦合成のみ**であり、水平interchange・大域strict 3/nは未証明。
- [F112-P79 #2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455)：**P77のraw4-cell合同では水平単位律を満たせないことを証明**。元F55の真の恒等3射２つを水平合成したraw証明のP59正規化経路長は２、結果経路のraw恒等3射は０。したがってP77のType値4-cellは存在せず、その厳密商クラスも非同一。左右contextの単位も同様に長さ１対０で障害がある。一方、P62の構文由来`unitOnly`経路合同ではすべて関係すること、両raw証明のfull shadowは一致することを示し、真正C60六角形の二つの独立F54 associatorで具体化。**P77の厳密な経路等号を保ったまま水平単位4-cellを追加することは不可能**だが、より弱いP62相対の証拠付きcoherenceは排除しない。
- [F112-P80 #2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457)：P79の厳密P59経路等号に関するno-goを保持したまま、**新しいType値raw4-cell presentation**に、旧P77証拠の明示的埋込み・水平単位・左右context単位の３生成規則を追加し、反射・対称・推移・左右縦whiskerへ閉じた。全証拠についてP62の構文由来単位経路**合同への健全性**と、F55原full shadow保存を独立に証明。実証拠存在によるSetoid・商のexact kernel、縦合成の4-cell適合性、shadow readoutの因子化を構成。真正C60で**旧P77商は非同一、新P80商は同一**と証明。P80は選択された新presentationであり、元raw歴史やP77 no-goを消してはいない。
- [F112-P81 #2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459)：P80の**新しいP62相対Type値4-cell商**について、実際の左右whisker証拠から縦合成のwell-definednessを証明。旧P77の単位・結合4-cellをP80へ明示的に埋め込み、F54原経路上に**別の厳密な局所縦Mathlib Category**を構成した。選択F55 full shadowの加法性・単位零を証明。旧P77商から新P80商への**raw履歴を変えない全射**を定義し、縦合成・shadowの保存、真正C60での**非単射性**と、新P80商へのP59証明ラベル付き自由経路の厳密readout**非降下**を証明。P77合同は変更せず、P62相対coherenceとP59経路等号を混同しない。

- [F112-P82 #2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461)：P80の**全9種類のType値4-cell生成規則**に保存される、元F55 raw構文由来の独立Nat不変量を構成（旧P77の8生成規則についても別に保存を証明）。元の**縦左単位4-cell** `id ≫ f ~ f` の両代表元を同じ右raw恒等3-cellと元F55の方法で水平合成すると、非単位・非`trans`原証明について不変量が**1対2**となる。したがって水平合成後の**P80 Type値4-cellは存在せず、P80商クラスも異なる**ことを、実際の北側C60五角形のpentagon 3-cellを用いてLean4で証明。これにより、**選択したP80商へ元F55水平合成は一般には降下しない**。これはP80 presentationの不足を示すものであり、P62の構文的合同やstrict 3圏一般の不可能性ではない。

- [F112-P83 #2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463)：mathlibの`Quiver.Path.addWeight`を利用し、P82の**raw構文由来Nat不変量**を元F55の型付きP59自由経路全体へ拡張した。元F55の9構成子に沿った正規化の厳密保存と、**P62単位経路合同の全5生成規則**に対する保存を証明。そのため、P82の真正縦左単位4-cellを左右の同じ恒等証明と水平合成して得た2つのfree pathは、不変量**1対2**によって**P62でも比較不能**であり、P62 Mathlib商でも異なることをそのexact kernelから証明。真正C60北五角形の原pentagonを用いた実例も形式化。**既存P62の健全性を維持したまま、不足するcontext 4-cellを単純追加することはこの実例で不可能**。これは既存P62/P80の選択についてのobstructionであり、一般のstrict 3圏や空の不可能性ではない。

- [F112-P84 #2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465)：旧P62のunit-only経路合同とP80のType値raw4-cell証拠を**変更せず**、別の**P84水平4-cell証拠付きType依存free-path合同**を構成した。旧P62証拠、同値律、縦経路合成の合同に加え、**任意の真正P80 Type値4-cellを左右から原F55 raw 3-cellで水平whiskerする2つの比較規則**を明示。全7生成規則で元F55 full shadowが保存されることを証明し、mathlibのCongruence・厳密な局所CategoryTheory.Quotient・**商のexact witness kernel**・原shadowへの因子化を完成。旧P62商から新P84商への自然な比較関手と、原P59自由経路→旧P62商→新P84商の厳密な可換三角形も形式化した。P82/P83の比較は**旧P62商で非同一、新P84商では同一**となることを両商のexact kernelから証明し、真正C60北五角形でstrict enlargementを確認。旧P62/P80のobstructionは消去していない。

- [F112-P85 #2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467)：旧P80 Type値4-cellと原F55 raw証明履歴を保持し、**左右の水平whiskeringを証拠付き生成規則とする別のType値4-cell presentation**を構成。旧P80埋込み・反射/対称/推移・左右縦whisker・左右水平whiskerの**全8生成規則**について、**新P84の真正typed path合同への健全性**とF55 full shadow保存を独立に証明。実証拠の存在だけをkernelとするSetoid/商を構成し、元F54 routeを対象とする別の厳密な**局所縦Mathlib Category**を旧P77の実単位・結合4-cellにより構成。旧P80商から新P85商への全射と、元F55水平合成の**P80商×P80商→P85商という代表元独立の二入力演算**を真正左右4-cell証拠で証明。真正C60北五角形で旧P80商は非同一、新P85商は同一。旧P82・P83のobstructionは否定されず、旧P62への全面的健全性は主張しない。

- [F112-P86 #2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)：旧P84経路合同と旧P85のType値4-cellを**変更せず**、左右context・pre/post F54 route・左右水平whiskeringの6種類の真正P85証拠付き比較を持つ**新P86経路合同（11生成規則）**と、その上の**新P86 Type値raw4-cell（12生成規則）**を構成。両者について元F55 full shadow保存を別々に証明し、新Type値4-cellの新経路合同健全性・証拠存在に基づくSetoid/商のexact kernelを形式化。経路合同側では厳密な局所Mathlib Category商、旧P84→新P86経路商の比較関手と可換因子化を構成。Type値4-cell側では元F54経路上の別の厳密局所縦Category、旧P85→新P86商の全射・縦合成保存、**P85商→P86商の左右context・pre/postcomposeの4種類の代表元独立輸送**および**旧P85商×旧P85商→新P86商**の真正証拠付き水平二入力演算を実装。真正C60北五角形の旧P85 4-cellを実際の左F45 contextに輸送するType値証拠とP86商等号も証明した。P82/P83の旧presentationに関するno-goは保持する。

- [F112-P87 #2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471)：P86の「旧P85商×旧P85商→新P86商」という段階的輸送から進み、**P87の真正Type値4-cell自身に左右context・pre/post F54 route・左右水平whiskeringを再帰的に施せる新presentation**を構成した。旧P86証拠を保持する12生成規則で原F55 full shadow保存と二入力の真正4-cell証拠を証明。対応するP87型付き経路合同（11生成規則）のfull shadow健全性・厳密な局所Mathlib Category商・source witness exact kernel・旧P86経路商からの比較関手と可換因子化を形式化。P87 4-cellをP87経路合同に健全と証明し、実4-cell証拠をkernelとするSetoid商、**厳密局所縦Category**、旧P86 4-cell商からの全射・縦合成保存を証明。さらに、**P87商→P87商の左右context・pre/postcomposeの全4演算**と**P87商×P87商→P87商への元F55水平合成の代表元独立な自己閉包**を構成。水平単位は旧P80の真正Type値単位4-cellから導出し、全full shadowの水平加法性を検証。元F55のinterchange二辺のfull shadow一致も証明したが、これを4-cell証拠の存在やstrict interchangeと同一視しない。P66のC60 disjoint squareにおける元F54二経路の非同一性・odd phaseは保持される。

- [F112-P88 #2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473)：原F55の9構成子に対する非可換`List Bool`ソース語を構成。縦合成の連結・左右contextによる`false`/`true`ラベル化を記録し、P77/P80/P85/P86/P87の**全Type値4-cell生成規則**で保存されることをLeanで証明した。型付き中間因子`f₂`と`g₁`が構文上非単位（語が非空）なら、縦・水平二順序の語は`L(f₁)++L(f₂)++R(g₁)++R(g₂)`と`L(f₁)++R(g₁)++L(f₂)++R(g₂)`で一致せず、**真正P87 Type値4-cellの非存在とP87商での厳密な非等号**が成立する。`p88_word_nil_iff_unitOnly`と真正C60北五角形・六角形disjoint squareの原始語も検証。これは**現在のP87 presentationに対する条件付きno-go**であり、strict 3圏一般の不可能性やC60上の任意の4因子の実現を主張しない。原full shadow一致は依然必要条件のみ。

- [F112-P89A #2475](https://github.com/itakura-hidetoshi/KuuOS/pull/2475)：**旧P87/P88を不変のまま**、旧P87 Type値証拠を埋め込む新たな真正P89 Type値4-cell presentationを構成。元F55の型付きinterchange二辺を比較する新しい**明示的interchange生成子**と旧12操作の再帰閉包を備え、全13生成規則の原F55 full shadow（整数charge・非零交換位相を含む）保存、真正source証拠存在をexact kernelとするSetoid/Quotient、旧P87→P89全射、新P89商でのraw interchange等号を証明。P88非可換語は非単位中間因子に対し新比較で保存不能と証明。**旧P87でinterchangeを証明したことにはならない**。

- [F112-P89B #2476](https://github.com/itakura-hidetoshi/KuuOS/pull/2476)：新P89商自身の厳密局所縦Mathlib `Category`、左右context・pre/post、P89×P89→P89の代表元独立な原F55水平二入力合成、真正P80単位証拠からの水平単位、原full shadowの加法保存を形式化。**任意の4つの合成可能なP89商クラスに対して、縦・水平合成のstrict interchange等式を証明**。型付き中間因子が非単位のとき旧P87商では非同一・新P89商では同一という条件付きstrict enlargementを証明した。**F54経路対象の異なるものの同一視、水平結合律、高次coherence、大域strict 3/nやhyperdescentは未証明**。

- [F112-P90A #2478](https://github.com/itakura-hidetoshi/KuuOS/pull/2478)：原F45木の内部節点数・根の左部分木節点数という独立不変量を作り、任意6つのNat深さ・両軸F19/F28 Blocksで**両軸Nat.add_assoc cast後も三項bracketingの原F45木は不等**と証明。一方、全物理sector列は一致し、真正Type値F54 associator route（原始回転1）が存在する。真正C60北五角形でも不等を確認。これは元の木の等号や全水平結合律の証明ではない。

- [F112-P90B #2479](https://github.com/itakura-hidetoshi/KuuOS/pull/2479)：任意3本の型付き原F54経路について、`((u⊗v)⊗w) ≫ assoc(after)`と`assoc(before) ≫ (u⊗(v⊗w))`を**同じF45境界の真正Type値F54経路**として構成。原始回転数一致を証明したが、最初の原ソース合成規則は`1`対`0`で**raw経路は不等**。その間の真正F55 `PresentedCell`は未充足の**型付き比較slot**としてのみ定義。inhabitantやcoherenceは仮定していない。

- [F112-P91A #2481](https://github.com/itakura-hidetoshi/KuuOS/pull/2481)：原F55九構成子すべてについて**F54原始回転数の差＝F55五角形整数電荷**をLeanで証明。P90Bの未充足associator自然性比較slotに真正F55証拠が存在するなら、両経路は同回転数なので**五角形整数電荷は0**でなければならない。さらに原F55交換整数電荷と奇位相のparity制約から、必要なfull shadow形状を明示。これは証拠存在・全水平結合律を証明したものではない。

- [F112-P91B #2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482)：真正原F55九構成子の**Type値証拠の存在をexact kernelとする別のF54経路対象商**を構成。P67のsquare-only商→新P91B商の全射と、旧P67商では回転数が降下する一方、新商では真正五角形の**3回転と2回転が同一視されるため回転数が降下不能**なことを厳密証明。元のC60北五角形はraw非同一・新商同一、真正F55証拠の電荷は元ソースに残る。P90Bの二経路の新商等号は**未充足F55比較slotの証拠存在と同値**であり、どちらも未証明。

**P91A/P91Bで、P89 strict interchangeの先に残るF54水平結合の必要条件と情報損失を明示しました。** P91Aの回転数差＝五角形電荷から、P90の真正F55 associator自然性証拠が存在する場合の五角形電荷0・交換電荷parity制約を証明。P91Bでは原F55 Type値証拠の存在だけからF54経路商を作り、P67のsquare-only商では保存できた原回転数が、F55 pentagonを含む新商には降下できないことを証明。**P90比較slotのinhabitant、水平結合律、4-cell coherence、globularityはなお未証明**であり、商クラス等号・原raw等号・真正証拠の選択を混同しません。旧P87/P88のno-go、新P89 interchange、原C60の非零奇位相、C60以前のW/J/Hと空の空、独立Kuuは一つのpresentationという原則を保持。Grayには戻りません。

## 五行・Qiも別の具体的presentation

mainで統合済みのQi v3.1–v3.3では`FivePhase = ZMod 5`を用い、相生を`+1`、相剋を`+2`の作用として表現します。同じ到達位相と同じ生成履歴は同一ではありません。

[Qi v3.1 #2366](https://github.com/itakura-hidetoshi/KuuOS/pull/2366)は忠実な巡回作用と型付き自由経路、[v3.2 #2369](https://github.com/itakura-hidetoshi/KuuOS/pull/2369)は明示した観測合同、[v3.3 #2371](https://github.com/itakura-hidetoshi/KuuOS/pull/2371)は到達可能観測圏との圏同値を証明します。観測合同が元の全履歴を回復するとは言いません。五行群論は臨床・物理現象の因果的実証と混同しません。

## これからの証明目標：strict 3/n圏から(∞,3)-hyperdescentへ

**GK4O [#2763](https://github.com/itakura-hidetoshi/KuuOS/pull/2763)まで完了：** GK4Nの任意P92B商観測の構造商降下条件を、全F45境界上の観測関数族・4つの明示kernel輸送互換性の下で、7つの原始構造seamチェックに帰着。反射・対称・推移の3法則と前後・左右contextの4合同を、真の原F54 Type値証拠帰納法で再構成した。**次はGK4P（仮称）：** 実際の合成・context保存則からkernel互換性を導く十分条件を調べ、追加仮定を明示的に管理する。元P92B結合律、真正14D Countable、19D filler、高次descentは未証明。

1. **一般理論の継承と照合：** 上記の`W/J/H`、普遍性、stack、scaled-horn、obstruction、actual-liftの定理を保持し、strict化に必要な強化・比較条件を洗い出す。
2. **局所strict 3圏：** 真正C60を含む具体例および一般的な文脈ソースに対して、証明関連3射のデータと厳密なinterchangeを形式化する。raw自由構文・path envelope・選択した商を混同しない。
3. **大域strict 3圏、strict n圏：** 真正なoverlap上のtransport、制限、三重以上の整合、gluingと高次結合律を証明し、globular strict n構造へ拡張する。C60上の証明を他の文脈に無条件には外挿しない。
4. **`(∞,3)`への橋：** strict n圏の列が自動的に一般の`(∞,3)`圏になるとは仮定しない。4射以上の可逆性、coherentな比較、使用モデルでの普遍性を別途証明する。
5. **hyperdescent：** 適切な高次値`F`とhypercover `U• → U`に対して`F(U) ≃ holim F(U•)`を証明する。普通のsheaf/stack・有限Čech descentを言い換えるだけでは不十分。
6. **一般化と空の空：** 文脈・被覆・presentationを変えた際にどの定理が保存されるか、どの障害が残るかを分類する。完成した構造も絶対的な「空」として実体化しない。

より詳しい証明義務・完了条件は[ROADMAP](ROADMAP.md)を参照してください。

## 正本、ビルド、検証

- **最新の統合証明receipt（2026-10-31）：** [F112-P94D3GK4O #2763](https://github.com/itakura-hidetoshi/KuuOS/pull/2763) squash MERGED、定理SHA `1370dce5a2a55a89ad4758911aea23597ce34050`、PR exact-source HEAD `b18ced002802ff865966c8a5e7a29501bd19a227`、[Strict Lean/Governance #41159766444](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41159766444) **3720/3720 scoped SUCCESS・Governance 5/5 completed SUCCESS**、17宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。
- **直前の統合証明receipt（2026-10-31）：** [F112-P94D3GK4N #2761](https://github.com/itakura-hidetoshi/KuuOS/pull/2761) squash MERGED、定理SHA `76eaf1c6c0ccb86ce7fd5e9e44ee74b9330df6d0`、PR exact-source HEAD `a1716b21a09bc70af3b41969590db93596ec5e65`、[Strict Lean/Governance #41158003474](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41158003474) **3719/3719 scoped SUCCESS・Governance 5/5 completed SUCCESS**、13宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。
- **直前の統合証明receipt（2026-10-31）：** [F112-P94D3GK4M #2759](https://github.com/itakura-hidetoshi/KuuOS/pull/2759) squash MERGED、定理SHA `36e13ca4f961a9a528d5592878a60cb2cd2e4fe1`、PR exact-source HEAD `f533b3973981384ea3b06c524f9ee142d936fb4e`、[Strict Lean/Governance #41157123830](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41157123830) **3718/3718 scoped SUCCESS・5/5 completed SUCCESS**、13宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。
- **直前の統合証明receipt（2026-10-31）：** [F112-P94D3GK4L #2757](https://github.com/itakura-hidetoshi/KuuOS/pull/2757) squash MERGED、定理SHA `b8ba6b09cb37239e4f25d7ef66cafad3565596f4`、PR exact-source HEAD `c97c947ed2e80683a425848ca1b9eea90d13ea4c`、[Strict Lean/Governance #41156497624](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41156497624) **3717/3717 scoped SUCCESS・5/5 completed SUCCESS**、13宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。
- **直前の統合証明receipt（2026-10-31）：** [F112-P94D3GK4K #2755](https://github.com/itakura-hidetoshi/KuuOS/pull/2755) squash MERGED、定理SHA `ef9e69c982706985a6dadfd72bd1199dde1531dd`、PR exact-source HEAD `c6e841c85a3a61ce0f65dfde3ee2a87c8319f3e4`、[Strict Lean/Governance #41155697783](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41155697783) **3716/3716 scoped SUCCESS、5/5 completed SUCCESS**、19宣言標準3公理以内、sorryAxなし、変更Lean warning/error **0/0**。
- **直前の統合証明receipt（2026-10-31）：** [F112-P94D3GK4J #2753](https://github.com/itakura-hidetoshi/KuuOS/pull/2753) squash MERGED、定理SHA `daa94823b410ce5a1a31004b72d01951af8a6420`、PR exact-source HEAD `011d56a8496acf89c5c1619d926e784ee3dadfc0`、[Strict Lean/Governance #41150002368](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41150002368) **3715/3715 scoped SUCCESS、5/5 completed SUCCESS**、14宣言`propext`・`Quot.sound`以内、sorryAxなし、変更Lean warning/error **0/0**。先行GK4I #2751（3714、14宣言）、GK4H #2749（3713、21宣言）、GK4G #2747（3712、28宣言）、GK4F #2745（3711、17宣言）は独立receipt保持。
- **文書・CIのauthority境界：** theorem-carrierはcanonical `main`上のLean宣言とその型・公理依存であり、README/ROADMAPの到達点やCIの緑表示は証明そのものの代わりではありません。docs-only変更に不要なStrict Leanを再実行して数学の成立を水増ししません。歴史的CI数値は下記の時点別台帳として保存します。

- **以前の統合・CI履歴（P79以降、各時点のreceipt）：** [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。F112親PR #2339はMERGED。P79 #2455：Lean **9687/9687**・17宣言、P80 #2457：**9688/9688**・14宣言、P81 [#2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459)：**9689/9689**・13宣言を`KuuOSFormal`統合入口で検証し、いずれも新規`sorryAx`なし・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts 2/2 SUCCESS後にsquash MERGED。P81統合SHA `5c9925528d8a90239375104a2ac1a5e71e483559`。続くP82 [#2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461)は **9690/9690**・新規公理監査**10/10**（`sorryAx`なし）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P82統合SHA `f7a876996cebd940ea3d8bbacaa75e51ac781422`。P83 [#2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463)：**9691/9691**・公理監査**10/10**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P83統合SHA `7bd530e28551881198c3c61e22b6163c9025753e`。P84 [#2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465)は **9692/9692**・新規公理監査**18/18**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P84統合SHA `90be8065f5b4b682f239c7bfd220e48ab2c97f27`。P85 [#2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467)は **9693/9693**・新規公理監査**18/18**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P85統合SHA `19c787422a3c234c0a4e5e8777d1730deb56313e`。P86 [#2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)は **9695/9695**・新規公理監査**37/37**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・新規Leanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P86数学統合SHA `2efbce7af262c9c8203bc7e3fc6c24a3c6139e73`。P87 [#2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471)は **9698/9698**・新規公理監査 **39/39**（`sorryAx`なし。`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root全件保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P87数学統合SHA `32cbcd465a932d0b66524ab56026880d6fdf1227`。P87の3モジュールも単一公開入口`formal/KuuOSFormal.lean`から直接import。P88 [#2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473)は **9700/9700**・新規公理監査**18/18**（`sorryAx`なし）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance [#39769469429](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/39769469429) SUCCESS・completion receipts **2/2 SUCCESS**後にsquash MERGED（SHA `2eef23640dcc4f30144d2a7b13489c0d72165d99`）。P88A/Bも同じ公開入口から直接import。P89A [#2475](https://github.com/itakura-hidetoshi/KuuOS/pull/2475)は **9701/9701**・公理監査**10/10**、P89B [#2476](https://github.com/itakura-hidetoshi/KuuOS/pull/2476)は **9702/9702**・公理監査**13/13**（いずれも`sorryAx`なし・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance SUCCESS・completion receipts **2/2 SUCCESS**）。P89A統合SHA `cab73a59bae36824c3dcb9a4a1b9ab3bcd804b06`、P89B統合SHA `59fa3d761c8133c621114d01c9567d4e2d09ad99`。P90A [#2478](https://github.com/itakura-hidetoshi/KuuOS/pull/2478)は **9703/9703**・公理監査**7/7**・統合SHA `4f77b8e7043b62d9cd95ee2505f28f272fe5684b`、P90B [#2479](https://github.com/itakura-hidetoshi/KuuOS/pull/2479)は **9704/9704**・公理監査**7/7**・統合SHA `43de1eaf5676614b879517bf0ca0e24207fc0f83`。両方とも`sorryAx`なし・Lean警告/エラー0・107公開root保全・exact-head Governance・completion receipts 2/2 SUCCESS。全モジュールを公開`KuuOSFormal`に直接importし、`KuuOSStrict`は内部集約のみ。
- **F112-P91 exact-head数学：** P91A [#2481](https://github.com/itakura-hidetoshi/KuuOS/pull/2481)は **9705/9705 SUCCESS**・公理監査**4/4**・squash SHA `153361ebc9bf4303ed9c79e931c768fc99a885af`。P91B [#2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482)は **9706/9706 SUCCESS**・公理監査**13/13**・squash SHA `8fd61aad78943f6c9c630a585450eac2b5246f90`。両PRとも`#print axioms`に`sorryAx`なし、変更ファイルLeanエラー/警告0、107公開root保全、Governance・completion receipts **2/2 SUCCESS**。
- **唯一の通常ビルド入口：** `lake build` = `lake build KuuOSFormal`。既存**107公開root**と独立Kuu・Qiを一つのパッケージで保持。`KuuOSStrict`は内部import集約で、独立した権威や「唯一の空」ではありません。
- **ツールチェーン：** Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。PR #1558（Lean 4.31）はvalidation-only・未マージ。
- **証明の判定：** 実際のLean宣言とその型・仮定、`#print axioms`、対象commitのexact-head CIを根拠とします。`sorryAx`、`sorry`、`admit`や未証明の新公理で目標を埋めません。歴史的なmathlib/finite `native_decide`依存は正確に区別します。
- **CI高速化：** 共有cache、差分モジュールの部分ビルド、不要な重複実行の削減は可。ただし旧公開rootの削除や証明義務の弱化で高速化しません。

~~~bash
python3 scripts/run_kuu_foundation_check.py
lake exe cache get  # 初回・必要なキャッシュがないときだけ
lake build KuuOSFormal # warningAsErrorはlakefile.tomlで既定設定。sorryAxは#print axiomsで監査。
~~~

AI推論runtimeの方向は **観測 → 文脈・複数presentation → 輸送と2/3-cell比較 → 整合する場合のdescent/glue、しない場合のobstruction保持 → 権限確認 → 行為または再観測** です。この推論設計も実行保証・臨床的実証・全LLM出力の形式的正しさとは区別します。

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
