# Qi v4.62 — 真正元P77の三角恒等式と証拠付き部分経路復元

**2026年11月5日 JST**。strict 空中心、独立Kuuは一presentation。append-only／same-root／旧定理上書き禁止。

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3145](https://github.com/itakura-hidetoshi/KuuOS/pull/3145) **MERGED** |
| 継承元 | Qi v4.61 定理 #3143、正式記録 #3144、`main` `79f08ecda52a9ae1c0ae94a9b4f6ddcba4c44365` |
| exact-source HEAD | `9774e7701d189d47a197619fc54dd85ea04d1f3b` |
| 定理squash / main | `134468649fefb28f7aa3ec7e54edd7af3f7cc3ed` |
| source/test-merge Git tree | `e6be6e268d77b7cf5436b30c7959751341fcf62e` **完全一致** |
| exact-source CI | [#41988984274](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41988984274) |
| Strict Lean | **10,259 / 10,259 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **17件**、`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| 新規証明ソース | [Qi v4.62 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TriangleCompatiblePartialRecoveryV4_62.lean) ＋`formal/KuuOSFormal.lean`の追加import１行 |
| 固定Lean/mathlib | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開・保護 | `KuuOSFormal`、公開root107、validation-only PR #1558 Draft/open/unmerged |

## 1. 継承する本来の証拠・authority

元Qi v4.53の有向`FivefoldEdge`五本からなる自由経路圏`FivefoldFreePathCategory`と、元F55/P77真正Type値四セルを元GK5CG保守的Type値五セルの証拠で商にした全ターゲット圏`FivefoldP77ConservativePoint`を区別する。

Qi v4.57の`FivefoldP77ImagePoint`は、元P77の**真正保守的四セル商クラス**に、元有向有限経路での到達可能性証拠を持つ広部分圏。v4.58はsource↔像圏のMathlib圏同値を構成し、v4.59は全P77 targetの逆向き四セルとchargeゼロの逆向き+五角形ループがいずれも像の外であることを証明した。v4.60は像Homから元型付き経路を厳密に復元するFunctorを構成し、v4.61は旧圏同値準逆`Q`と復元Functor`R`間に真正NatIso `θ:Q≅R`を証明している。

**全元P77 target・証拠付き像・元自由経路は別authority**。数値chargeの一致から元四セル／五セルのType証拠を復元しない。元P94A、独立Kuu、実際のC60物理Edge、北C60 CRTも同一視しない。

## 2. 元unit/counit三角恒等式を真正回収へ輸送

Qi v4.58の真の同値`E`が持つunit `η` とcounit `ε`、Qi v4.61の比較自然同型 `θ : Q ≅ R` について、元sourceの任意の型付き対象`u`で

\[
\boxed{\eta_u\gg\theta_{F(u)}
  = \mathrm{nil}_u : \operatorname{Quiver.Path}(u,u)}
\]

を`fivefoldP77Recovery_unit_comparison_triangle`として形式証明した。

重要なのは、`u : FivefoldPathVertex`そのものにCategoryの恒等射記法`𝟙 u`を使うのではなく、**真正元source自由経路**`Quiver.Path.nil`を終端項にすることである。

証明は、`θ`が元counitから復元Functorを通じて作られたことを用い、

\[
F(\eta_u\gg\theta_{F(u)})
=F(\eta_u)\gg\epsilon_{F(u)}
=\mathrm{id}_{F(u)}
=F(\mathrm{nil}_u)
\]

と元target上で結ぶ。最後に既証明`fivefoldP77ImageFactor_faithful`の`map_injective`によって元sourceの型付き経路等式に戻す。これが`Functor.map_comp`／`map_id`の自動簡約に頼り切らない真正の三角恒等式接続である。

また任意の元像対象`X`に対して、

\[
\boxed{F(\theta_X)=\epsilon_X}
\]

を`fivefoldP77Recovery_comparison_reflects_counit`で証明。`fivefoldP77Recovery_oldTriangle_newInverse_split`は両法則を組で保持する。choice依存の準逆が**定義的に等しい**という主張は行わず、NatIsoによる比較と元の三角法則を区別した。

## 3. 元P77 targetの部分復元領域の厳密な定義

元の型付き両端点`u,v`に対する部分領域は

\[
\operatorname{Dom}_{u,v}
=\bigl\{z:\operatorname{Hom}_{\mathrm{P77}}(u,v)
  \,\big|\,\operatorname{Reachable}_{\mathrm{source}}(z)\bigr\}
\]

とする。`FivefoldP77PartialDomain`は、元P77保守的商クラスそのものと**本物の元有限経路による到達証明**を持つ依存Subtypeである。charge区間で定義した集合ではない。

`fivefoldP77PartialHomPathEquiv`は、任意の元端点について、真正型付き自由経路とのType値同値

\[
\operatorname{Quiver.Path}(u,v)\simeq\operatorname{Dom}_{u,v}
\]

を与える。部分復元`fivefoldP77PartialRecoverPath`とその`_spec`／`_unique`は、元P77商クラスに再評価すると元のクラスそのものとなり、元sourceの型付き経路が一意であることを証明する。

恒等射・合成についても`_id`／`_comp`により真正経路として整合し、`_charge_length`は**到達証拠付き領域に限り**

\[
Q_{\mathrm{P77}}(A.val)
=\bigl(\operatorname{length}(\operatorname{Recover}(A)):\mathbb Z\bigr)
\]

を形式証明。非計算的な`Classical.choose`による元の到達証明の選択であり、一般数値からType値証拠を計算的に生成する構成ではない。

## 4. Type値五セルが復元可能性の正確な判定境界

`fivefoldP77PartialDomain_lift_iff`は、任意の元P77保守的商クラス`z`について、部分領域にlift可能であることと**元sourceからの到達可能性**が同値であることを証明した。

さらに任意の元F55/P77生の四セル`w`について、`fivefoldP77PartialDomain_originalFiveCell_iff`は次をLean4で証明する：

\[
\boxed{
\begin{aligned}
&[w]\in\operatorname{Dom}_{u,v}\\
&\quad\Longleftrightarrow\\
&\exists\,\gamma:\operatorname{Quiver.Path}(u,v),\;
\operatorname{Nonempty}\bigl(
\operatorname{GK5CGConsFiveCell}(F(\gamma),w)\bigr).
\end{aligned}}
\]

右辺は元の真正**Type値保守的五セル証拠の存在**であって、整数chargeの範囲評価や合同条件ではない。

## 5. 全元P77 targetとのobstruction

`fivefoldP77PartialDomain_negativeReverse_missing`は、元P77の真正逆向き`e01^{-1}:1→0`（charge -1）が部分領域に存在しないことを証明する。`fivefoldP77PartialDomain_zeroReverse_missing`は、別の真正四セル

\[
z_0=e_{01}^{-1}\circ U\circ L^{-1}:1\to0,
\quad Q_{\mathrm{P77}}(z_0)=-1+3-2=0
\]

も部分領域に存在しないことを証明する。**chargeが許容範囲に入っていても復元可能とは限らない**。

`fivefoldP77TrianglePartialRecovery_exact_boundary`は、到達可能性による正確な部分回収領域の特徴付けと、**元P77全targetを元source有限経路へ評価を保って全域回収するsectionが存在しないこと**を併記する。元P77四セル構文への新逆辺追加や全targetとの圏同値を主張しない。

## 6. Lean記載法とCIの修正履歴

初回の型エラーでは`FivefoldPathVertex`に対する`𝟙 u`がCategory instanceを要求し、元自由経路の恒等射`Quiver.Path.nil`とは直接一致しなかった。次段階では`map_id`／`map_comp`と元unit/counitの等式を`simpa`だけで接続できなかった。

最終ソースでは**元targetでの`F.map`等式連鎖を明示し、元の圏同値の三角等式を使った後、`Functor.Faithful.map_injective`で元sourceへ戻す**。定理の主張や仮定は弱めていない。最終exact-source CI #41988984274は17件の公理監査を含めて全10,259ジョブSUCCESS、変更Lean warning/errorは0/0。source/test-merge Git tree同一、検証済みHEAD指定でsquash MERGED。

## 7. 次の研究境界

**確定した成果**：元P77の真正証拠付き像圏に関して、v4.58圏同値の三角恒等式とv4.61準逆比較が整合し、元targetの部分回収領域は元sourceのType値到達証拠の存在で厳密に特徴付けられた。

**未主張**：全元P77 targetへの無条件回収、未知のoriginal→φ seam、元上下経路を同一視する新pentagonator、CRT数値からの元証拠復元、C60物理辺と元P77四セルの型同一視。

**次の焦点：Qi v4.63**。到達可能なHomでの部分正規化の文脈依存自然性、部分領域の生成元・合成閉性と局所descentの必要十分条件、全targetの障害をcharge検出・元Type値証拠復元不可に分離する。旧source証拠と保護条件を維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
