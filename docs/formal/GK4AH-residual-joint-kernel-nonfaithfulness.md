# F112-P94D3GK4AH — 積観測の残余非忠実性と第二行列表現

**2026-10-31 JST**。唯一の定理正本は itakura-hidetoshi/KuuOS のcanonical main。append-only／tighten-only／same-rootで元の証明と歴史を維持。

- [定理PR #2801](https://github.com/itakura-hidetoshi/KuuOS/pull/2801) **MERGED**。
- 最終定理exact-source HEAD：afdd0096b42e8fcc527417d530be3c12d1c1b1d5。
- 定理squash SHA＝マージ直後canonical main HEAD：3532a723478362c14d88fc1f24b8bf8c33f41d72（GitHub MCPで一致確認）。
- [CI #41184959463](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41184959463)：**Strict Lean 3756/3756 SUCCESS、Governance 5/5 SUCCESS**。append-only Lean 2ファイル・公理表示48宣言、標準propext／Classical.choice／Quot.sound以内、sorryAx 0、変更Lean warning/error 0/0。
- Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft/OPEN/未マージ。

## 1. 旧四成分＋行列の積観測

前段GK4AGで、真の元F54依存型sourceから四成分 O_AE と非可換行列 M_AF を併せた O_AG(r)=(O_AE(r),M_AF(r)) を作った。第二kernel商 K_AG は、元P92B Type値存在商QをO_AGの値の一致でさらに割ったもの。独立構造比較商Sとは別のpresentationであり、真正S→K_AG比較はHom全射だが、その忠実性は未証明だった。

## 2. 第二非可換整数2×2行列不変量

[新行列表現Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AHAlternativeMatrixInvariant.lean)は、実元F54のcastDepths・実forward・実backward LocalRotationを保存して、次の異なる表現を導入。

~~~text
C  = [[ 1, 1],[0,1]]       -- true original double-Nat cast
F  = [[ 1,-1],[0,1]]       -- true original forward
R4 = [[ 1, 0],[4,1]]       -- true original backward, different evaluation
C*F = I                    -- true original F54 associator
B4 = F*R4 = [[-3,-1],[4,1]]
~~~

旧GK4AFでは R1=[[1,0],[1,1]]、旧B1=F*R1=[[0,-1],[1,1]] で B1³=-I、B1⁶=I。この有限位数は真のF54の比較関係そのものではなく、**旧行列表現が課す余分な等式**である。新B4=-I+N、N=[[-2,-1],[4,2]] は N²=0、N≠0で、整数行列上ではB4の任意の正の冪が単位行列にはならない。

新不変量は元の全5 DepthRotationRoute構成子、RotationEdge／RotationChainと両型付き文脈を直接観測し、元F55全9、元P92B全9（真正assocNaturalityを含む）、独立構造seam全14、拡張比較全3の**元Type値証拠ごとの保存性**を確認した。元Qおよび独立Sにそれぞれ独立にQuotient.liftで降下、Q→S比較との可換性とS合成・単位の行列値保存も証明。元Qを未証明の圏に変更せず、観測一致から元P92BのType値3-cellを生成しない。

## 3. 真正F54型付き経路の反例

[非忠実性Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AHJointResidualNonfaithfulness.lean)では実 rot:LocalRotation p before after を取り、真の二Nat cast自己経路 C と、元forward/backward回転証拠からなる真の自己backtrack B から次の同じ型付きF54自己Homの二経路を構成。

~~~text
u = C;B;B;B;B;B;B;C  = C;B^6;C
v = B;B;B;C;C;B;B;B  = B^3;C^2;B^3
~~~

元GK4ADのcastは charge=+1、forwardはcharge=-1、backwardはcharge=-1かつbackwardCount=1。よってB全体は charge=-2、backwardCount=1、内部moment=-1。**正しい全四成分値**と旧行列値は次のとおり。

~~~text
O_AE(u) = O_AE(v) = (false, -10, 6, -30)
M_AF(u) = M_AF(v) = [[1,2],[0,1]]
~~~

実際に元F54の完全依存型経路を評価するLean定理で、各数値と全積観測O_AGの完全一致を確認した。しかし新しい保存不変量は

~~~text
M_AH(u) = [[ -11,-16],[-24,-35]]
M_AH(v) = [[-155,-64],[264,109]]
~~~

と異なる。この新不変量はSの元構造seamをすべて保存するので、**[u]_S ≠ [v]_S**。一方、K_AGはO_AG等値による真正第二商なので **F_AG([u]_S)=F_AG([v]_S)**。

**結論：本物のS→K_AG比較関手は、実LocalRotationを持つ任意のF54型付き自己Homで非忠実。元のC60北側六角形northHexagonNativeLeftRotationについても無条件に証明した。** 旧行列の周期性を取り除いた単独の新不変量が、この特定の障害を検出しているのであって、Sの全域分類は主張していない。

## 4. Lean4エラー原因とexact-source修正

初回source HEAD 14319e6eb869ed09d765cec361b498993c9c75d3／[CI #41184707394](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41184707394)では新行列表現ファイル全体（元F55/P92B/14 seam/3 extended保存を含む）がコンパイル成功。第二ファイルも元S非同値・新旧行列・K_AG比較非忠実性をコンパイルしたが、四成分の数値表示補題2件だけrfl失敗。

理由は旧GK4ADの原始記号のchargeを取り違え、誤って四成分を (false,-2,6,-6) と記述したため。元ソースの nativeGK4ADCast=((1,0),0)、nativeGK4ADForward=((-1,0),0)、nativeGK4ADBackward=((-1,1),0) を照合し、正しく (false,-10,6,-30) に修正。元の組観測一致・主定理は最初からrflで成立していたため、この修正は証明の仮定を弱めない。

修正後exact-source HEAD afdd0096b42e8fcc527417d530be3c12d1c1b1d5、[CI #41184959463](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41184959463)：**3756/3756 Strict Lean SUCCESS、Governance全5/5 SUCCESS**。48宣言のaxiom表示は標準3公理以内、sorryAx 0、変更Lean warning/error 0/0。その後squashマージしてmain HEADと同一SHA 3532a723478362c14d88fc1f24b8bf8c33f41d72を独立確認。

## 5. 次段階GK4AI（未証明）

今回の厳密な結論は**S→K_AGの残余非忠実性**であり、新しい第三観測 O_AI(r)=(O_AE(r),M_AF(r),M_AH(r)) の第二kernel商K_AIはまだ構成していない。次はS→K_AI→K_AG→K_AEの実比較・忘却関手と再度の残余obstructionを検査する。行列値の追加だけでS→K_AI全域の忠実性は結論できない。元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは引き続き未証明、Gray圏は非導入。

著作権 © 2026 板倉英俊 / Hidetoshi Itakura。
