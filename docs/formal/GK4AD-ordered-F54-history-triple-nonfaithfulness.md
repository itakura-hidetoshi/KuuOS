# F112-P94D3GK4AD — 元F54非可換履歴と真正三成分観測の残余非忠実性

**2026-10-31 JST** — 定理正本 `itakura-hidetoshi/KuuOS`、canonical `main`。

- **[定理PR #2793](https://github.com/itakura-hidetoshi/KuuOS/pull/2793) MERGED**。
- 最終exact-source HEAD `c2a1d6746cc4a07cdc28048b308d663b17044e4a`。
- 定理squash SHA＝定理マージ直後のmain HEAD `62586f3d26a2ad78e466ceef8a9473b8e0566f3a`（GitHub MCPで完全一致）。
- [exact-source CI #41179319781](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41179319781)：**Strict Lean 3745/3745 SUCCESS、Governance 5/5 SUCCESS**。新規Lean2ファイル、36宣言の `#print axioms` は `propext`／`Classical.choice`／`Quot.sound` 以内。**sorryAx 0、変更Lean warning/error 0/0**。
- Lean `v4.30.0-rc2`、mathlib pin `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107維持、Grayを再導入せず、保護PR #1558 Draft/OPEN/未マージ。

## 1. 真正原F54履歴に対する非可換観測

[GK4ADOrderedHistoryInvariant Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ADOrderedHistoryInvariant.lean)は、元F54の実`RotationEdge.forward`、`RotationEdge.backward`と二Nat`castDepths`を保持した上で、整数値順序momentを追加する。

値域 `NativeGK4ADValue := (Int × Nat) × Int` を、`((charge,backwardCount),orderedMoment)`として解釈し、演算

~~~text
(c,b,m) ⋄ (d,e,n) = (c+d, b+e, m+n+c*e)
unit = (0,0,0)
cast = (1,0,0)
forward = (-1,0,0)
backward = (-1,1,0)
~~~

を定める。この演算は結合的・単位的だが**非可換**。`cast ⋄ forward = unit` は真正F54原assocが「1 cast、1 forward」を含むことに正確に対応する。真正`RotationChain`は途中の全原F45木・原Type値回転方向を保持し、元`DepthRotationRoute`のchain、cast、trans、leftContext、rightContextをすべて直接帰納的に観測する。

**真正比較証拠の全構成子を個別検証**：

- 元F55全9構成子（3対2 pentagon、2対2 disjointSquare、symm/trans、左右文脈、pre/postcompositionを含む）。
- 元P92B全9構成子（真正associator-naturalityを含む）。非可換な`u,v,w`の並びを入れ替えず、同じ順序の結合律と原assoc値unitでsoundnessを導く。
- 元F54構造seam全14構成子と拡張構造比較全3構成子。

従ってこの新しい順序付き観測は、元P92B証拠存在商`Q`と独立構造比較商`S`に**別々にQuotient.liftで降下**。元`Q→S`正準射との可換性、実構造商合成の非可換積保存、構造単位を形式化。元Type値3-cellは観測値一致から**生成しない**。

## 2. 同じ三成分観測だが異なる実構造商類を構成

[GK4ADTripleNonfaithfulness Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ADTripleNonfaithfulness.lean)は、実際に証言された元F54 `rot : LocalRotation p before after`から真正前進・逆向き物理backtrack`B : DepthRotationRoute before before`を使用。実`C := castDepths rfl rfl before`も同じ元F54 self-endpointを持つ。

~~~text
u = trans C B
v = trans B C
~~~

この2本は元F54の実Type値証拠履歴として完全に型付き、かつ実三成分観測が厳密に一致する。

~~~text
O_AA([u]_S) = O_AA([v]_S) = ((false,-1),1)
orderedValue(u) = ((-1,1), 0)
orderedValue(v) = ((-1,1),-1)
~~~

順序付き不変量`orderedMoment`が**元P92B全比較および構造seam全比較を通じて保存**されるため、元`Q`と独立構造商`S`の双方で実際に`[u]≠[v]`と証明。しかしGK4AAの真の`S→K_AA`比較は`O_AA`の値が同じであることと像の同値が必要十分なので、

~~~text
[u]_S ≠ [v]_S
F_AA([u]_S) = F_AA([v]_S)
~~~

**よって`S→K_AA`は実F54局所回転を持つ任意の型付き自己Homで非単射・非忠実**。本当のC60北側六角形`northHexagonNativeLeftRotation`にも無条件で適用する。

## 3. GK4ACとの差異と権限境界

GK4ACで得た`Nat ≃ Fiber(K_AA→K_X,[R_0]_{K_X})`は**異なる二つの第二商**を比較する完全ファイバー同値。一方GK4ADは**独立構造商`S`から三成分第二商`K_AA`への比較の非忠実性**を新しく確定する。両者は矛盾しない。`Q`・`S`・`K_AA`・`K_X`を混同せず、歴史的元F19/F28/F54との無条件完全同値は主張しない。

元P92B商Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは依然未証明。strict空中心、独立Kuuは一presentation、Gray非再導入、append-only／tighten-only／same-root／overwrite-forbiddenを維持。

## 4. 検証と次段階

GK4ADの最終2新規Leanファイルは**初回からexact-source Strict Lean 3745/3745 SUCCESS**。新しい依存公理・sorry・変更ファイルのwarning/errorを認めない。定理マージ後、README/ROADMAPは別docs-only PRで更新する。

**次候補 GK4AE（未証明）：** 非可換orderedMomentを四成分観測に組み込み、元`Q`・`S`・新しい観測kernel商を区別した新比較関手と忘却関手を構成し、なお残る非忠実性があるかを検証する。全域忠実性は予断しない。
