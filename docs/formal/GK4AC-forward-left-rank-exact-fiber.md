# F112-P94D3GK4AC — 真正F45左結合rankと逆回転ゼロ障害の除去

**2026-10-31 JST** — 定理正本 `itakura-hidetoshi/KuuOS` の canonical `main`。

**定理PR [#2791](https://github.com/itakura-hidetoshi/KuuOS/pull/2791) MERGED**。最終exact-source HEAD `9f7ad594782025cc55f0d0bf01f1bd6ed984e6a3`、定理squash SHA（マージ直後main HEADと完全一致）`f77277798860d4bbd8fbb6d557e7fefb7870f314`。[Strict Lean/Governance CI #41178066934](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41178066934) は **3743/3743 Strict Lean SUCCESS、Governance 5/5 SUCCESS**。新規2ファイル・26件の`#print axioms` は `propext`・`Classical.choice`・`Quot.sound` 以内、`sorryAx=0`、変更Lean warning/error **0/0**。固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

## 1. 真正F45二分木に基づく左結合rank

[原型付きLean証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ACForwardRank.lean)は、真のF45二圏・四Blocks・両Nat depthと実葉をそのまま保ち、自然数値の`L(T)`と`W(T)`を定義：

~~~text
L(refl/leaf) = 1
L(node A B) = L(A)+L(B)
W(refl/leaf) = 0
W(node A B) = W(A)+W(B)+L(A)
L(T)>0
~~~

真正F54 `LocalRotation.assoc`の正方向`((A B) C)→A (B C)`は**WをL(A)だけ厳密に減少**させ、従って`W(after)+1≤W(before)`。元`LocalRotation`全3構成子（assoc・leftContext・rightContext）で、対応する両Nat castと葉数保存を含めて形式化した。`RotationEdge.backward`は元Type値証拠であり、自由な逆射を勝手に付加しない。

中間木を全保持する真正`RotationChain`と元`DepthRotationRoute`全5構成子（chain・double-depth cast・trans・left/right context）について、

~~~text
backwardCount(r)=0
  ⇒ W(last)+rotationCount(r) ≤ W(first)
~~~

を証明した。ゆえに同一元F45木`T`に戻る型付き自己経路では

~~~text
r : DepthRotationRoute T T
backwardCount(r)=0 ⇒ rotationCount(r)=0
~~~

である。これは**真の物理前向き回転だけでは非自明な閉路を構成できない**というrank障害であり、元P92B証拠存在商Qの圏公理を利用しない。

## 2. GK4ABの唯一の例外を除去し、真正Nat同値を構築

[第二kernelのLean証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ACExactPositiveFiber.lean)は、元F54完全Type値証拠から導かれた上記の不等式を実`K_AA`第二商の自己Homへ降下させ、**後向き回転数0の任意の実三成分kernel類はBoolean物理grade=true**と証明。

一方、元F54の真正前向き＋後向きbacktrackと実`castDepths`から構成したGK4Zの実経路塔`R_k`は、元`K_X`二段kernel商において全段が同じ値`(false,-2)`を持つ。

従って、元`[R_0]_{K_X}`を固定した**別の実二段目商間**`K_AA→K_X`の真正ファイバー`F`では、`backwardCount(z)=0`は`grade(z)=false`と矛盾し、GK4ABの唯一残るゼロ階層は**空**。GK4ABで既に証明済みの「全正整数階層は、ただ一つの元Type値`R_k`により代表される」と組み合わせて、

~~~text
nativeGK4ACBalancedTowerFiberEquiv :
  Nat ≃ NativeGK4AAForgetFiber rot
k ↦ [R_k]_(K_AA)
~~~

を本物のLean `Equiv.ofBijective`で構成した。逆回転数の到達範囲は厳密に正の全自然数であり、全実商類の元F54塔添字の一意性も証明。真正C60北側六角形`northHexagonNativeLeftRotation`についても無条件に`Nat ≃ F`とゼロ層空性を証明している。

**権限境界**：元P92B証拠存在商`Q`、独立構造比較商`S`、三成分第二商`K_AA`、旧二成分第二商`K_X`はそれぞれ別の型。三成分の値の一致から元P92B Type値3-cellを生成しない。**`S→K_AA`の全域忠実性はなお未証明**で、ここで得た`K_AA→K_X`ファイバーの完全同値とは異なる。元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは依然未証明。

## 3. Lean失敗の構造的原因・再検証

初回CI #41177522941 と2回目 #41177802441 は、元F54の左右文脈に対する2か所の`omega`不成功。型付き`rotationCount(leftContext path later)`と`rotationCount(path)`が、`simp only`だけでは算術戦術に同一の数として渡らなかった。最終変更では両文脈で**元constructorのまま`...rotationCount = path.rotationCount := rfl`**を別の等式として示し、`rw`で書き換えた後に`omega`へ渡した。変更Lean2ファイル全文、imports、GK4ABからの商シグネチャ、元F54構文およびpinを照合した修正版HEADで**3743/3743**、全Governance成功、公理依存は標準3以内、警告・エラー・sorryAxは0となった。

## 4. 次のGK4ADの未解決事項

三成分`O_AA=(grade,castCharge,backwardCount)`が独立構造商`S`上で忠実か、または元Type値の別履歴を識別できないかを、原F54比較証拠・本来のseamと共に検証する。局所`K_AA→K_X`ファイバー同型のみで`S→K_AA`のfaithfulnessを推論しない。strict空中心・独立Kuuは一presentation・Gray非再導入・append-only/tighten-only/same-root/overwrite-forbidden・公開root107、保護PR #1558 Draft/OPEN/未マージを維持。
