# Qi v4.60 — 真正元P77証拠付き像からの型付き有限経路復元関手

**2026-11-05 JST**。strict 空中心、独立Kuuは一presentation。append-only／same-root／overwrite forbidden。

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3141](https://github.com/itakura-hidetoshi/KuuOS/pull/3141) **MERGED** |
| 直前正本 | Qi v4.59 定理 #3139・正式記録 #3140 MERGED、main `5c186c56f61420621a1645ba66d76f85df9dbfaa` |
| 検証済みexact-source HEAD | `05e2ca86be6da56e73a7ace3187df23c9575db70` |
| 定理squash/main | `cf44b19f94aafd6f2f5b002e34d937ac16014c96` |
| source/test-merge Git tree | `4ccb259bfbd080bfec53de974e6ecb6e31817e80` **完全一致** |
| exact-source CI | [#41978185134](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41978185134) |
| Strict Lean | **10,257 / 10,257 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **17件**、標準公理 `propext`／`Classical.choice`／`Quot.sound` のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| 固定環境 | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 | `KuuOSFormal`、公開root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |
| 形式ソース | [Qi v4.60 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CertifiedImagePathRecoveryV4_60.lean) ＋公開import 1行 |

## 1. 正本の構造とauthority境界

Qi v4.53の真正`FivefoldEdge`有向5辺`e01/e12/e23/e04/e43`からの自由経路圏`FivefoldFreePathCategory`と、Qi v4.54で元F55/P77の**真正型付き四セル**を元GK5CG conservative **Type値5-cellの存在証拠**によって商にした元target圏を保持する。

Qi v4.57の`FivefoldP77ImagePoint`は、元P77商クラスと**本物の元有限経路による到達可能性の証拠**をHomに持つ。Qi v4.58はこのsource→certified imageが実際のMathlib圏同値であることを示した。v4.59はchargeがゼロでも元target全体には未到達な真正P77証拠が存在することを証明している。

今回の復元は**証拠付き像に限定**される。数値charge、P94A shadow、C60物理EdgeやRingHom等号から元F55/P77のType値四セル・五セルを生成するものではない。

## 2. 元P77商像Homの唯一の経路正規形

像Hom `A : FivefoldP77ImageHom ... X Y` に対して元の到達証拠を使用し、`fivefoldP77ImageRecoverPath`が

\[
w_A:\operatorname{Quiver.Path}(X.vertex,Y.vertex)
\]

を選び、`fivefoldP77ImageRecoverPath_spec`で真正元P77商targetにおける正確な評価

\[
F_{\mathrm{P77}}(w_A)=A.val
\]

を形式証明する。さらに`fivefoldP77ImageRecoverPath_unique`により、同じ元P77商クラスを評価で与える元型付き有限経路は**唯一**である。これはv4.55の真正Faithfulから証明し、chargeから経路を推測するわけではない。

`Classical.choose`でProp値到達証拠の存在からpathを選ぶため、復元関手は非計算的である。実行可能なアルゴリズムとしての証拠抽出や、全target上の計算を主張しない。

## 3. 真正Functor、恒等射・合成、両方向の復元

`fivefoldP77ImageRecoverPath_id`と`fivefoldP77ImageRecoverPath_comp`は

\[
w_{\mathrm{id}_X}=\mathrm{nil}_X,\qquad
w_{A\circ B}=w_A\circ w_B
\]

を元の依存型端点・元P77商合成に沿って証明する。これからMathlibの実際のFunctor

\[
\operatorname{Recover}:
\operatorname{Im}(F)\longrightarrow\mathcal P_5
\]

（`fivefoldP77ImageRecoveryFunctor`）を構成した。

`fivefoldP77ImageRecovery_left_obj/map`と`fivefoldP77ImageRecovery_right_obj/map`は、source→image→sourceとimage→source→imageが**それぞれの元対象と全Homに対して厳密に恒等**となることを証明する。これは関手の対象・Hom作用ごとの等式であり、v4.58のchoice依存の`Equivalence.inverse`との**定義的等号**を新たに主張していない。

さらに`fivefoldP77ImageHomPathEquiv`は、各型付き端点で

\[
\operatorname{Quiver.Path}(X.vertex,Y.vertex)
\simeq
\operatorname{Hom}_{\operatorname{Im}(F)}(X,Y)
\]

という真正Type値`Equiv`を構成する。これは数値chargeの同値ではない。

## 4. 元GK5CG chargeと経路長の関手的整合

`fivefoldP77ImageRecoverPath_charge_length`は全ての証拠付き像Homについて

\[
Q(A.val)=\bigl(\operatorname{length}(w_A):\mathbb Z\bigr)
\]

を証明する。`fivefoldP77ImageRecoverPath_comp_charge`は実際の像Hom合成において、復元した元経路を合成してから測った長さと元chargeを照合する。

`fivefoldP77ImageRecoverPath_zero_charge_endpoints`により、像Homのchargeが0なら復元経路の長さは0で、元型付き端点が一致する。これは**像に既に所属する**場合の主張であり、元P77全targetのchargeだけから到達性を推論しない。

## 5. 全元P77 targetへの回収不可能性

`fivefoldP77NoGlobalHomRecovery`は、全ての元P77保守的商クラスに対し、そのクラスを厳密に評価で再現する型付き元有限経路を返す**全域section**が存在しないことを証明する。

反例はQi v4.59で構成した真正元P77四セル

\[
z_0=e_{01}^{-1}\circ U\circ L^{-1}:1\to0,
\qquad Q(z_0)=-1+3-2=0
\]

である。元有向自由経路ではchargeが長さなので、もし評価で`z_0`を与える元経路があれば長さは0となり、端点`1\ne0`に矛盾する。

このno-goは指定された元P77商ターゲットへの**正確な評価を保つ復元**についてのもので、無関係な別の圏同値一般を否定するものではない。

## 6. Leanエラー修正の構造理由

初回CIでは、像対象のラッパーとFunctorのHom式を混ぜた`calc`において、Leanの`Trans Eq Eq`の中間型が合致しなかった。二回目CIでは、元`Quiver.Path.comp`が文字どおりのカテゴリー合成記法とは一致せず、`rw [Functor.map_comp]`のパターン認識が失敗した。

**元v4.57の検証済み証明と依存シグネチャを参照**し、恒等射は元商クラスへの真の`map_id`、合成則は元商クラスでの明示的`map_comp`等式連鎖に変更した。17宣言の定理命題・元P77/五セルauthority・公理境界・元数学的仮定を一切弱めず、3回目CIで固定Leanによる全10,257ジョブ成功を得た。

## 7. 次の研究境界

**確定**：真正元P77 source-certified像の各Homについて、本物の型付き有限経路を非計算的に一意復元し、Functor・Hom Equiv・charge=lengthを保存できる。全元P77 targetへは正確な評価を保持した全域sectionを延長できない。

**次の焦点（Qi v4.61）**：復元とv4.58既存の準逆Functorとの具体的な自然同型、元型付き五角形の上経路／下経路の復元正規形、元P77全targetへの部分的なextension/descentの正確なobstruction。元F54/F55/P77/P94A・真正C60・北C60 CRTは別authorityとして保持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
