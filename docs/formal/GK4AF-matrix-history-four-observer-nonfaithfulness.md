# F112-P94D3GK4AF — 元F54行列履歴と四成分観測の残余非忠実性

**2026-10-31 JST**。唯一の定理正本は `itakura-hidetoshi/KuuOS` canonical `main`。

- **[定理PR #2797](https://github.com/itakura-hidetoshi/KuuOS/pull/2797) MERGED**。
- 最終exact-source HEAD：`0ba7499f91ef1420f705d35ec46097f3aff634d1`。
- 定理squash SHA＝定理マージ直後main HEAD：`53526634b254907320426876bd0f19cd5a05f768`。GitHub MCPで完全一致を独立再確認済み。
- [exact-source Strict Lean/Governance CI #41182480085](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41182480085)：**Strict Lean 3751/3751 SUCCESS、Governance 5/5 SUCCESS**。新規Lean2ファイル・`#print axioms` 42宣言、公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内。**sorryAx 0、変更Lean warning/error 0/0**。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107維持、strict空中心、独立Kuu一presentation、Gray非再導入。保護PR #1558 Draft/OPEN/未マージ。

## 1. 真正F54 Type値履歴を保存する非可換整数2×2行列値

[行列不変量のLeanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AFMatrixInvariant.lean)は、完全依存型の元F45二圏・四Blocks・両Nat depth・実C60葉を失わず、全ての真正F54`RotationEdge`、中間木を保持した`RotationChain`、原`DepthRotationRoute`の5構成子を行列値へ写す。

値域`NativeGK4AFMatrix=(Int×Int)×(Int×Int)`には、実行列積と単位行列を明示的に定義し、**4つの整数多項式等式によって積の結合律**を、別に左右単位をLean4で証明した。

~~~text
C : original double-Nat cast = [[1, 1], [0, 1]]
F : actual forward rotation = [[1,-1], [0, 1]]
R : actual backward rotation = [[1, 0], [1, 1]]
I : genuine chain identity = [[1, 0], [0, 1]]

C * F = I      -- true F54 assoc comprises one cast then one forward
B := F * R     -- genuine two-edge original physical backtrack
~~~

`F54.assoc`の像が厳密に`I`となる点が重要。元F55のpentagon両辺は`I`、disjointSquare両辺は実前進回転`F*F`。元P92Bのassociator-naturalityは**元u,v,wの順序を変えず**、既存の結合律と`C*F=I`で検証する。

その上で**元F55全9構成子、元P92B全9構成子（本物のassocNaturalityを含む）、F54構造seam全14構成子、拡張比較全3構成子**に対する保存性を、各々の**元Type値証拠**上で証明。元P92B証拠存在商`Q`と別の独立構造比較商`S`のそれぞれへ`Quotient.lift`を構成、元`Q→S`正準比較の可換性と`S`の真正合成・単位における行列値の乗法性を形式化する。観測の一致から元のP92B Type値3-cellを作ることはない。

## 2. 真正四成分kernelの残余非忠実性を決定

[真の反例と比較写像のLeanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AFResidualNonfaithfulness.lean)では、元F54の真正局所回転`rot:LocalRotation p before after`、真正`B := nativeGK4FBacktrack rot`と`C := nativeGK4WCastRoute before`から、同一F45型付き自己Homの本物の2経路を構成する。

~~~text
u = C ; B ; B ; C
v = B ; C ; C ; B
~~~

元GK4AEの四成分観測は双方で**完全に一致**：

~~~text
O_AE(u) = O_AE(v) = (false, ((-2, 2), -2))
    -- grade=false, castCharge=-2, backwardCount=2, moment=-2
~~~

しかし新しい整数行列評価は**厳密に異なる**：

~~~text
M(u) = [[ 0,-1],[1,1]]
M(v) = [[-1,-1],[3,2]]
~~~

両者の左上成分がそれぞれ`0`と`-1`なので、元`Q`および独立構造商`S`上の行列値保存により**`[u]_S ≠ [v]_S`**とLean証明。一方、真正第二`K_AE`比較では四成分観測値一致が像の一致と必要十分なので**`F_AE([u]_S)=F_AE([v]_S)`**。従って、**真正`S→K_AE`比較関手は元F54局所回転が実在する任意の自己Homで非忠実**。実C60北側六角形`northHexagonNativeLeftRotation`にも無条件で特殊化した。

この結論は、GK4ACの別の`Nat≃Fiber(K_AA→K_X,[R_0])`、GK4ADの`S→K_AA`非忠実性、GK4AEの`K_AE→K_AA`非忠実性のそれぞれと両立するが、商の`Q`、`S`、`K_AE`、`K_AA`、`K_X`を同一視してはいない。

## 3. CI不成功からのLean記法修正とexact-source検証

初回[CI #41182235164](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41182235164)では、新規行列不変量1ファイル目（実積結合律・全9/9/14/3構成子保存・元Q/S降下）は**コンパイル成功**、2ファイル目の商類相異証明2件のみが不成功だった。原因は、Leanの`congrArg (fun M => M.1.1)`で得た算術矛盾が、まだタプル射影のままで`omega`に渡ったため。「行列左上成分`0=-1`」の型付きdefinitional unfoldingが算術戦術の前提へ渡っていなかった。

最終修正では該当2か所へ

~~~lean
have hentry := congrArg (fun m : NativeGK4AFMatrix => m.1.1) hv
change (0 : Int) = (-1 : Int) at hentry
omega
~~~

を採用。両変更Leanファイル全文・imports・元F54/元P92B/structural比較のdependent signatures・pinned Lean/mathlibを照合し、修正版HEADで**3751/3751 SUCCESS、Governance全5/5 SUCCESS、sorryAxなし、warning/error 0/0**を得た。古いLean証明を上書きせずappend-only。

## 4. 次のGK4AGの研究境界（未証明）

既存真正四成分`O_AE`と新しい行列値`M`を組み合わせる別の第二観測kernel商`K_AG`を構成し、真正`S→K_AG→K_AE`比較・忘却関手を厳密化する候補がある。ただし行列値と四成分値が等価・完全忠実であるとは推論せず、`S→K_AG`の残余障害を別途調べる。元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明。

著作権 © 2026 板倉英俊 / Hidetoshi Itakura。append-only／tighten-only／same-root／overwrite-forbidden、strict空中心／独立Kuu一presentation／Gray非再導入を保持。
