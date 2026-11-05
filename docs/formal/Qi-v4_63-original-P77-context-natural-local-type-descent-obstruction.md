# Qi v4.63 — 真正元P77の文脈自然性・Type値局所降下・復元障害の分離

**2026年11月5日 JST**。KuuOS strict 空を中心とし、独立Kuuは一つのpresentation。元の証拠authorityと履歴を残す append-only／same-root／旧証明上書き禁止。

| 項目 | 確定した検証状態 |
|---|---|
| Repository / branch | `itakura-hidetoshi/KuuOS` / `main` |
| 定理PR | [#3147](https://github.com/itakura-hidetoshi/KuuOS/pull/3147) **MERGED** |
| 継承元 | Qi v4.62 定理 [#3145](https://github.com/itakura-hidetoshi/KuuOS/pull/3145)・正式記録 [#3146](https://github.com/itakura-hidetoshi/KuuOS/pull/3146) MERGED |
| 正本基点 | `0769050bae1263b4d1e1cc60177a69cf9212fee0` |
| 最終exact-source HEAD | `c250fdca602901c12df49b03409173300f257088` |
| 定理squash / main | `f77b2b4e67c9234d2a9908ee2f680b5f0ced24f9` |
| exact-source CI | [#41994826578](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41994826578) |
| Strict Lean | **10,260 / 10,260 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **12件**、`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| source/test-merge Git tree | `b8b6cfa2a90bd3df0a3b47f98eb6ee682efb4eaa` **完全一致** |
| 定理ファイル | [Qi v4.63 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextLocalDescentObstructionV4_63.lean) |
| 公開集約 | `formal/KuuOSFormal.lean`へのimport 1行追加のみ、公開root107維持 |
| 固定Lean/mathlib | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR | validation-only [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ維持 |

## 1. 元source・元P77全target・証拠付き像圏のauthority

元`FivefoldEdge`有向自由経路圏 `FivefoldFreePathCategory`、真正F55/P77 Type値四セルを元GK5CG保守的Type値五セルの存在で商にした全target `FivefoldP77ConservativePoint`、そして元source到達可能性の**実証拠付き**像圏 `FivefoldP77ImagePoint` は別の型と権限を保持する。v4.62の `FivefoldP77PartialDomain` は、元全target商の各Homクラスに元source有限経路の到達可能性証拠を付けた依存Subtypeであり、数値chargeで定義しない。

v4.58のsource/像の真正Mathlib圏同値、v4.60の具体的元型付き経路復元Functor、v4.61の準逆比較NatIso、v4.62の三角恒等式と復元一意性をそのまま継承した。v4.63は元sourceの前後文脈と、真のType値五セルによる局所互換条件を追加し、元のfull targetへの全域復元を主張しない。

## 2. 到達可能Homでの左右文脈自然性

`pre : Quiver.Path s u`、`A : FivefoldP77PartialDomain u v`、`suffix : Quiver.Path v t` とし、`F`を元source→元P77証拠付き像のFunctor、`R`をv4.62の実際のtyped partial recoveryとする。

```text
R(F(pre) ≫ A)                    = pre.comp (R A)
R(A ≫ F(suffix))                 = (R A).comp suffix
R((F(pre) ≫ A) ≫ F(suffix))     = (pre.comp (R A)).comp suffix
```

新規定理 `fivefoldP77PartialRecovery_left_context`、`_right_context`、`_both_contexts` で、端点が正しい元型付き経路の**等式**として形式検証した。既存の元P77保守的Functorの評価式により、元全target商のsource到達性も前後文脈合成で保存される（`fivefoldP77OriginalContext_reachable`）。

`fivefoldP77OriginalContext_missing_reflects` は「ある前後文脈での合成が未到達なら、中間Homも未到達」という保存性の対偶に限る。全targetの任意の中間Homからのキャンセル、または未到達性の任意文脈への保存という、証明されていない逆向き命題は導入していない。

## 3. 真正元GK5CG Type値五セルによるHom-wise局所descent

同一の元型付き端点 `u,v` に属する元F55/P77生四セルの非空添字族 `raw : I → FivefoldP77LocalRaw u v` を用いる。主定理 `fivefoldP77LocalTypeDescent_iff` は、以下の厳密な必要十分条件を与える。

```text
(∃ path : Quiver.Path u v,
  ∀ i : I, P77Functor.map path = P77ConservativeClass (raw i))
↔
((∀ i j : I, Nonempty (GK5CGConservativeFiveCell (raw i) (raw j))) ∧
 (∃ i : I, ∃ path : Quiver.Path u v,
   Nonempty (GK5CGConservativeFiveCell (EvaluateP77 path) (raw i))))
```

左辺は単一の**真正元source型付き自由経路**が全patchの元P77商クラスへ一致評価されることである。右辺には (1) 全パッチ間の実際のType値五セル重なり互換性と、(2) **少なくとも一つのパッチ**の本物のsource経路到達Type値五セル証拠を要する。個々のパッチでchargeだけを一致させる条件には弱化していない。

証明は、元の`fivefoldP77ConservativeClass_eq_iff`でType値五セルを商等式へ正確に移し、元の`fivefoldP77ConservativeFunctor_map_spec`で任意の評価済みsource経路を元クラスへ移す。逆向きには、同じsource path評価から任意patchへ元GK5CG五セル互換性で移送する。さらに`fivefoldP77LocalTypeDescent_unique`は既証明の真正Faithful Functorで、全patchを復元するsource pathが **存在すれば一意（∃!）** であることを証明した。

**成立範囲：** 同じ型付きHomでの非空パッチ族に対する証拠付き局所gluingである。一般位相空間上の被覆や任意siteでのsheaf descentを証明したという意味ではない。重なりのType値五セルと、少なくとも一つのsource certificateを必須とする。

## 4. charge可視障害とType値復元障害の厳密な分離

`fivefoldP77Obstruction_charge_or_type_gap`では元P77生四セル`w`のsource復元不能を、次の二つの場合の正確な選言として形式化した。

1. 元の符号付きchargeが **0未満** または **3超** であり、元有向自由経路の長さ制約だけで到達不能を検出できる。
2. chargeは`0 ≤ Q(w) ≤ 3`を満たすが、任意の元有向有限経路`path`に対して、`EvaluateP77(path)`から`w`へ向かう真正保守的GK5CG Type値五セル証拠が**存在しない**。

単なるcharge範囲外を「すべての復元障害」と混同しない。具体例として、真正元P77逆`e01`（端点1→0）は`Q=-1`でchargeから検出できる。一方で真正元P77「逆`e01`＋上3辺−下2辺」のクラスは **`Q=0` にもかかわらず** 同じ端点1→0の元source有向自由経路から到達できない。`fivefoldP77Obstruction_negativeReverse_charge_detected`、`_zeroReverse_charge_silent`、`_two_original_reverses_split` は、二つの実際の元P77四セル商クラスの相違とType値復元障害を保持している。

## 5. Lean4記法修正とexact-source監査

PR #3147は初回CIの構文・rewrite診断を受けて、**変更Leanファイル全文・imports・依存定義・固定mathlibのFunctor API**を照合し、命題の条件を弱めずに証明を修正した。主要なLean4上の修正内容は (a) `prefix`予約語を束縛変数名に使わない、(b) dependent Homの証拠付き`Subtype`に対するrewriterの推論が不足する場合、既定理を明示型付き`have`と`congrArg`で適用する、(c) `Functor.map_comp`の等式を右文脈へのpostcompositionと混同せず`congrArg`で移す、(d) 両側自然性は既証明の左右自然性を`Eq.trans`で合成する、である。

最終exact-source HEAD `c250fdca602901c12df49b03409173300f257088`のCI #41994826578 で完全Strict Lean 10,260/10,260成功。元ソース・test-merge Git tree完全一致、変更Lean warning/error0/0、新規12件の`#print axioms`は`propext/Classical.choice/Quot.sound`のみで`sorryAx`なし。過去の失敗ログは最終証明の証拠として扱わない。

## 6. 保存した研究境界と次の候補

- 保護PR #1558はDraft/open/unmerged。公開root107と pinned Lean/mathlib維持。
- 元F55/P77/P94A、独立Kuu、真正C60物理Gauge、北C60 CRTはそれぞれ別authority。型、証拠、歴史を暗黙同一視しない。
- 全元P77 targetのfullness、逆向きsource辺の捏造、chargeだけからType値五セルを再構成する操作はしない。新しいpentagonator、Gray圏復元、無条件なsheaf降下も追加しない。
- **Qi v4.64候補：** 同一Hom内の有限パッチから、元有向辺の任意長文脈列・複数の型付き部分経路へ局所証拠を配分し、その合成整合性の必要十分条件および失敗する具体的Type値障害を証明する。元P77 targetへの全域回収を仮定しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
