# F112-P94D3GK4AJ — 真正三類忘却ファイバーと第二行列の到達像同値

**2026-10-31 JST**。唯一の定理正本は `itakura-hidetoshi/KuuOS` のcanonical `main`。

- [定理PR #2805](https://github.com/itakura-hidetoshi/KuuOS/pull/2805) **MERGED**。
- 定理最終exact-source HEAD `537d38346b0fae76e7c4ca01bd2b010073211539`。
- 定理squash SHA＝定理マージ直後canonical main HEAD `cf859a9eb1f77a3b36dcabd3319b795b43e96101`（GitHub MCPで確認）。
- [exact-source CI #41187062144](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41187062144)：**Strict Lean 3761/3761 SUCCESS、Governance 5/5 SUCCESS**、新規Lean2ファイル・`#print axioms` 35宣言、依存公理は標準`propext`、`Classical.choice`、`Quot.sound`以内、`sorryAx=0`、変更Lean warning/error **0/0**。
- Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心／独立Kuuは空の一presentation、Gray非再導入、保護検証PR #1558 Draft/OPEN/未マージ。append-only／tighten-only／same-root／overwrite-forbidden。

## 1. 元F54真正依存型sourceからの三類ファイバー

[元F54三経路・相異・忘却値のLeanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AJTernaryPhysicalFiber.lean)は、実際の`rot:KuuNativeF45Tree.LocalRotation p before after`から、同じ元F45型付き自己Homに属する物理backtrack`B`と、元のdouble-Nat castDepths自己経路`C`を使う。

~~~text
w0 = C ; B^12 ; C
w1 = B^3 ; C ; B^6 ; C ; B^3
w2 = B^6 ; C^2 ; B^6
~~~

これらは任意の記号文字列ではなく、全て元F54の`DepthRotationRoute.trans`、元`nativeGK4FBacktrack rot`と元`nativeGK4WCastRoute before`から構成した**真正依存型source経路**。元F55・P92BのType値比較やF54の独立構造seamを数値観測から作成しない。

真正四成分値と最初のGK4AF行列値（前段の積観測全体）は、3経路すべてで厳密に一致する：

~~~text
O_AE(w0) = O_AE(w1) = O_AE(w2) = (false, -22, 12, -132)
M_AF(w0) = M_AF(w1) = M_AF(w2) = [[1,2],[0,1]]
~~~

旧行列で元物理backtrackの像`B1`が`B1^3=-I`、`B1^6=I`となる、**表現由来の追加関係**がこの等値ファイバーを生む。しかし元Sでこの3経路を同一視するType値証拠が存在するとは推論しない。

一方、GK4AHから継承した独立の真正Type値保存行列`M_AH`は

~~~text
M_AH(w0) = [[ -23, -34], [ -48,  -71]]
M_AH(w1) = [[1561, 638], [-2640,-1079]]
M_AH(w2) = [[-599,-274], [1104,  505]]
~~~

と評価され、特に各左上成分 `-23`、`1561`、`-599` は相異なる。真正第二kernel商`K_AI`は積観測 `O_AI=(O_AE,M_AF,M_AH)` の値一致を元`Q`に課した商なので、三類`[w0]_{K_AI}`・`[w1]_{K_AI}`・`[w2]_{K_AI}`は**pairwise unequal**。他方、真正忘却`U_{AI,AG}:K_AI→K_AG`では旧積観測が一致するため**全3類が同じ旧K_AG値**へ写る。

したがって、元LocalRotationを持つ任意の真正自己Homで、**ひとつの実K_AGファイバーに少なくとも3個の相異なるK_AI類が存在**。元C60北側六角形`northHexagonNativeLeftRotation`についても独立に特殊化しLean4で証明。

## 2. 一般の元F45型付きHomにおける正確なファイバー分類

[任意の旧ファイバー上の第二行列像同値Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AJExactMatrixFiber.lean)では、任意の元F45の同じ型付きsource/targetに属する`x,y:K_AI`について

~~~text
x = y  iff
  (U_AI,AG(x) = U_AI,AG(y) AND M_AH(x) = M_AH(y))
~~~

をLean4で証明。これは前段K_AIの第二等値kernel定義と、`K_AI→`到達可能三重積観測値圏が各Homで単射という確定結果から導いたもので、元S→K_AI全域忠実性の仮定は不要。

固定された**実際に到達可能な旧K_AG類`q`**について

~~~text
Fiber(q) := {x : K_AI | U_AI,AG(x)=q}
SecondMatrix_q : Fiber(q) → IntegerMatrix2x2
~~~

を元の依存型Homごとに構成。`SecondMatrix_q`が単射であることを証明し、さらに

~~~text
Fiber(q) ≃ {m : IntegerMatrix2x2 | ∃ x : Fiber(q), SecondMatrix_q(x)=m}
~~~

という真正なLean `Equiv.ofBijective`を証明。値域は全整数行列ではなく、**そのファイバー内で元F54経路から到達した第二行列値の集合**である。三類実例はこの単射の正確な実観測証拠となる。

## 3. CI／Lean elaboration修正履歴

初回[workflow #41186504054](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41186504054)は、Leanインストール時に`release.lean-lang.org`のDNS解決に失敗。GitHub MCPからfailed jobsを**同じsource HEADのまま再実行**したところツールチェーン導入が成功し、初めてLeanソースへ到達した。そこで真正三経路の旧観測一致・第二行列値計算は成功した一方、3組の類相異証明の`rw`において、`congrArg (fun z => ...)`が未展開で、既存`nativeGK4AJClassN_matrix`補題のパターンと一致しない構文的elaboration failureが3件発生。さらに存在定理で元`rot`を宣言の型に書かずproof本体のみで使ったため、section変数の自動generalizationに含まれずunknown identifierとなった。

最終修正では、3件の相異証明に`change (nativeGK4AIKernelValue ...).2 = ... at hm`を先行させ、その後に既証の`nativeGK4AJClassN_matrix`で`rw`。存在定理には本物の`(rot : KuuNativeF45Tree.LocalRotation p before after)`を明示。数学的仮定を弱めず、全新規Leanファイル・imports・元F54構成子・元P92B/Q/S dependent signaturesを確認した。

最終exact-source HEAD `537d38346b0fae76e7c4ca01bd2b010073211539`で[CI #41187062144](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41187062144) **Strict Lean 3761/3761 SUCCESS、Governance全5ジョブSUCCESS、35宣言の公理依存標準3以内、sorryAx0、変更Lean warning/error0/0**。その後定理PR #2805をsquashマージして定理正本HEAD `cf859a9eb1f77a3b36dcabd3319b795b43e96101`を独立再確認。

## 4. 研究境界・次のGK4AK（未証明）

今回証明したのは**旧`K_AG`の一つの真正ファイバーに少なくとも三類の`K_AI`が存在する**こと、および**各ファイバーの第二行列到達像による正確な分類**。`S→K_AI`の全域忠実性・非忠実性は今回未決着。これらを混同せず、GK4AKでは例えば旧行列の周期から生成される大きな有限ファイバーのパラメータ族、または元F54の二行列を超えて区別されない本物のS類の探索を行う。

元P92B Q自体の未証明結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescent、Gray再導入は引き続き権限外・未証明として保持。

© 2026 板倉英俊 / Hidetoshi Itakura。
