# Qi v4.88 — 真正P77五セル端点を持つ新六セルの端点別正規形と次数完全性

## 0. Canonical正本と検証

2026年11月6日 JST。Repository：`itakura-hidetoshi/KuuOS`。Canonical branch：`main`。

| 項目 | 正式確定値 |
|---|---|
| 継承元 | Qi v4.87、main `26d74973dc9082c7fc9ea7ea44139bcf964203a4` |
| 定理PR | [#3199](https://github.com/itakura-hidetoshi/KuuOS/pull/3199) — MERGED |
| Exact-source HEAD | `a3a66368ed4c2620454059e600d7a45aba3fd11b` |
| 定理squash／定理正本HEAD | `00339a2c52e73a04bf3ac60f110d2d860412d4b1` |
| Source／test-merge／squash Git tree | `92a146ec4054b8a5d3efb0791600cd7e6b36d3d3` — 完全一致 |
| Exact-source CI | [#42195483050](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42195483050) — completed/SUCCESS |
| Strict Lean | **10,287／10,287 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 公理監査 | 指定20宣言の`#print axioms`実出力を確認、標準公理のみ（`propext`、`Classical.choice`、`Quot.sound`） |
| `sorryAx`／変更Lean warning・error | なし／0・0 |
| Pin | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root・保護 | `KuuOSFormal`、root107維持、PR #1558 Draft/OPEN/未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77SixCellEndpointNormalFormsV4_88.lean) · [Qi v4.87正式記録](Qi-v4_87-original-P77-six-cell-proof-word-coherence-conditional-descent.md) · [真正独立GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 数学的対象と厳密な制限

旧GK5CG真正元五セルType `pentagonFinalConservativeLoop` と元P77 raw terminal i、実際の五角3辺・2辺五セル値 `L₃(i)`／`L₂(i)` を継承する。v4.85では**これらの元五セルType値の厳密不一致**を証明済み。v4.86の`PentagonAdjoinedSixCell`は明示的に別の自由六セルpresentationであり、元F55/P77/GK5CGには六セル生成元を追加していない。

v4.87は生六セル証明語のsigned degreeを導入し、同じ始点・終点を持つ証明語を次数一致で商化した。v4.88では、端点が異なるという真正条件から、**次数が端点だけに依存する**ことを証明した。元sourceで六セルや七セルが元から存在するとの主張ではない。

## 2. 端点ポテンシャルによる次数の決定

任意の型Wと異なる二端点l≠rに対し、新presentationのポテンシャルを
\[
H_r(w)=\begin{cases}
1 & (w=r),\\
0 & (w\ne r)
\end{cases}
\]
と定義する。Leanは`endpointHeight`の決定可能性に`Classical`を使用し、任意型Wの等号に決定性を**仮定として追加しない**。

`degree_eq_endpointHeight_sub` により、任意の型付き生六セル語 `c : AdjoinedSixCell W l r w z` について

\[
\boxed{\deg(c)=H_r(z)-H_r(w)}
\]

を構成子 `refl`・`symm`・`trans`・`pentagon` の完全帰納で形式証明した。ここから `allParallel_degreeCoherent` と `loop_degree_zero` を得る。元のF55/GK5CG四セル電荷と、新六セルの構文次数は区別する。

## 3. 到達性と三形の正規代表

任意の元Wの端点w,zで、新文法の比較可能性は次と必要十分である：

\[
\boxed{
\mathrm{Nonempty}(\mathrm{SixCell}(w,z))
\iff (w=z)\lor(w=l\land z=r)\lor(w=r\land z=l).
}
\]

`comparison_nonempty_iff_endpointShape` は`endpointsSupported`の帰納と、三種類の構成子証拠によってLean4で証明済み。

新`EndpointNormal`は`refl`、`pentagon`、`symm pentagon`の三形から成る。任意の生六セル語cについて、その端点を保ち次数整合する三形の代表dの存在を`exists_endpointNormal`で証明。`selectEndpointNormal`はこの存在証明から`Classical.choose`で代表を選択する**非計算的選択**であり、raw c=dという厳密等式は主張しない。

## 4. 新しいcoherence商における完全性と局所thin性

`homDegree`は`CoherentHom`から整数への次数不変量を定義し、合成・反転を保存することを`homDegree_comp`／`homDegree_inverse`で証明する。

`homDegree_eq_iff`は一般の平行する新商六セルq₁,q₂について

\[
\boxed{\deg(q_1)=\deg(q_2)\iff q_1=q_2}
\]

を示す。さらにl≠rなら`homDegree_eq_endpointHeight_sub`と`allParallel_coherentHom_eq`によって

\[
\forall q_1,q_2:\mathrm{CoherentHom}(w,z),\quad q_1=q_2
\]

となる。**全Homが非空**という主張ではない：`coherentHom_nonempty_iff_endpointShape`が非空条件を正確に分類する。`coherentHom_hasEndpointNormal`はすべての商クラスに上記三形の代表が存在することを証明し、`coherentHom_self_eq_id`は新商内の任意自己射が恒等射であることを示す。

## 5. 真正P77原点への形式化とsource authority

実際の任意元P77 raw terminal i、任意の元GK5CG五セル始終点w,zについて以下を新Leanモジュールで証明した：

- `pentagonActualSixCell_degree_endpointPotential`：真正端点のポテンシャル差による構文次数。
- `pentagonActualSixCell_allParallelCoherent`：平行する生六セル語の次数整合。
- `pentagonActualSixCell_allRawEndpointNormal`：任意の型付き生六セル語の三形代表存在。
- `pentagonActualSixCell_allParallelHom_eq`：商クラスの局所thin性。
- `pentagonActualSixCell_endpointComparison_unique`：異なる真正元五セル値L₃(i)、L₂(i)間で、新商比較クラスが非空かつ一意であることと、元の厳密不一致の同時保存。

これらは新presentationと選択した次数商の結果である。元GK5CGで六セル生成元が存在した証拠、元の五セルType値の等号、その他のhigher fillerの不存在の証明ではない。

## 6. CI修正理由と再現可能性

新規Leanモジュール446行程度＋`formal/KuuOSFormal.lean` import1行。旧定理・pin・manifest・workflow・公開root・保護PRは変更なし。

初回CIは、任意型Wの比較で`Decidable (w=r)`を自動合成できないことを検出。既存宣言を弱めず`endpointHeight`の定義内に`classical`を明示した。次の検証ではmathlibのタクティク推奨 `intro b hab` が`warningAsError=true`により失敗と判定されたため、証明の2つの`intro`を単一記法に整理した。いずれも数学的仮定は変更せず、最新HEADで全10,287 Lean jobs、Governance30/30、20件公理監査、Git tree一致が成功した後、指定HEADをsquashマージした。

## 7. Qi v4.89研究候補

現在の次数商は意図的にthinである。次段階では、商の同値と異なる**Type値の上位比較証拠**、正規化証拠履歴、別presentationのcompatibility、元sourceに押し戻すために本当に必要な条件を形式化する。全ての生六セル語の元証拠履歴とその商クラスを同一視しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
