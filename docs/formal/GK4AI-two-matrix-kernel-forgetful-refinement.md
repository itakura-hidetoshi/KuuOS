# F112-P94D3GK4AI — 真正二行列積観測の第二kernel商と忘却関手

**2026-10-31 JST。** 唯一の定理正本は itakura-hidetoshi/KuuOS の canonical main。前段GK4AHまでのLean定理・README・ROADMAPの履歴を保持し、append-only / tighten-only / same-rootで新規3Leanファイルを追加した。

- [定理PR #2803](https://github.com/itakura-hidetoshi/KuuOS/pull/2803) **MERGED**。
- 最終定理exact-source HEAD：7c6f5822d6ae1285dd4350473ff88eddd583f4e0。
- 定理squash SHA＝定理マージ直後canonical main HEAD：74a2e656afd72a4796fd322d7602f9f904e0a15a（GitHub MCPで一致を独立確認）。
- [exact-source CI #41185737418](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41185737418)：**Strict Lean 3759/3759 SUCCESS、Governance 5/5 SUCCESS**。新規3Leanファイル・公理表示47宣言、依存公理は標準propext / Classical.choice / Quot.sound以内、**sorryAx 0、変更Lean warning/error 0/0**。
- Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6、公開root107、strict空中心・独立Kuuは空の一presentation、Gray再導入なし、保護検証PR #1558 Draft/OPEN/未マージ。

## 1. 真正F54の積観測

[元F54／Q／S三重観測Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIProductObservation.lean)は、GK4AEの実四成分、GK4AFの最初の非可換整数2×2行列、GK4AHの第二の独立行列評価を単なる数え上げではなく、真の順序付き積として統合した。

~~~text
O_AE(r) = (physical Bool grade, Int castCharge, Nat backwardCount,
           Int orderedMoment)
M_AF(r) = original GK4AF typed 2×2 integer matrix
M_AH(r) = alternate GK4AH typed 2×2 integer matrix
O_AG(r) = (O_AE(r), M_AF(r))
O_AI(r) = (O_AG(r), M_AH(r))

NativeGK4AIValue := NativeGK4AGValue × NativeGK4AHMatrix
(U,A) * (V,B) := (nativeGK4AGCombine U V, nativeGK4AHMul A B)
unit := (nativeGK4AGUnit, nativeGK4AHOne)
~~~

GK4AG/AF/AHで既に元Type値比較に沿って証明済みの各保存性を成分ごとに利用し、積の結合律・左右単位、元P92B証拠存在商Q・独立構造比較商Sへの**別々の降下**、Q→S正準比較との可換性、元F54合成と左右依存型文脈の観測整合性、独立構造seam全14の保存性をLean4で証明した。元F55全9、元P92B全9（実assocNaturality含む）、拡張比較全3の元Type値証拠は証明済みの成分観測から継承する。観測値の一致だけから元P92BのType値3-cellを発明しない。

## 2. 真正第二kernel商 K_AI の圏構造

[第二kernel圏Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIKernelCategory.lean)では、真の元P92B Type値証拠存在商Qの、**新観測O_AIの等値関係**による独立第二商を構成した。

~~~text
K_AI(first,last) := Q(first,last) / (q ~ r iff O_AI(q)=O_AI(r))
~~~

元Qの圏公理はなお未証明であるため、元Qの結合律や左右単位を仮定せず、既存GK4Sの到達可能観測値imageの合成を経由してK_AI上のMathlib Categoryを構築。真正単位・合成・結合律・左右単位律を証明。

元の独立S圏からの Functor S→K_AI は各実型付きHomで**全射**。K_AIから別のjoint値圏へのFunctorsは、kernelがまさに観測値一致で定義されているため各Homで**単射**。この後者の忠実性から、前者S→K_AIの忠実性を推論しない。比較のHom単射性が成立する必要十分条件は、元S型付きHomにおける新O_AI観測の単射性である。

## 3. 旧K_AGへの本物の忘却関手と非忠実性

[真正忘却関手・C60反例Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIForgetful.lean)は、実際の元P92B同一代表を用いたFunctor K_AI→K_AGを構成し、各Hom全射、単位・合成保存、真正S→K_AGとの可換性を証明した。さらに既存のK_AG→K_AEを経由した複合の整合性も確認：

~~~text
S --F_AI--> K_AI --U_AI,AG--> K_AG --U_AG,AE--> K_AE
 \______________________F_AG___/           |
  \______________________F_AE______________/
~~~

GK4AHで既に証明した**本物の元F54 LocalRotationとcastDepths**に由来する同一依存型自己Homの2経路を再使用する。

~~~text
C := actual original double-Nat castDepths
B := true forward/backward F54 LocalRotation backtrack

u = C;B^6;C
v = B^3;C^2;B^3

O_AE(u)=O_AE(v)=(false,-10,6,-30)
M_AF(u)=M_AF(v)=[[1,2],[0,1]]

M_AH(u)=[[-11,-16],[-24,-35]]
M_AH(v)=[[-155,-64],[264,109]]
~~~

新積観測O_AIは2つの旧行列／四成分に新しい行列を足すので、K_AIでは u と v が区別される。一方、K_AGへの行列忘却後は同一視される。

~~~text
F_AI([u]_S) ≠ F_AI([v]_S)
U_AI,AG(F_AI([u]_S)) = U_AI,AG(F_AI([v]_S))
~~~

よって**真正忘却Functor K_AI→K_AG は実F54局所回転を持つ任意の自己Homで非忠実**。真正物理C60北側六角形 northHexagonNativeLeftRotation でもLean4で無条件に証明された。独立構造商S→K_AIが全域忠実という結論ではない。

## 4. 正本・CI・Lean依存検証

新規Leanモジュールは (1) GK4AIProductObservation、(2) GK4AIKernelCategory、(3) GK4AIForgetful の3件。いずれも既存の完全依存型sourceと元Q・独立S定義を別々に参照し、mathlibのQuotient・Category・Functorを利用する。

[exact-source workflow #41185737418](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41185737418) の最終HEAD 7c6f5822d6ae1285dd4350473ff88eddd583f4e0 で**3759/3759全Lean targets SUCCESS、Governance全5/5 SUCCESS**。実行ログ内の新規全47個の #print axioms は標準3公理のみ、sorryAxなし、変更ファイルwarning/error 0/0。今回はLean elaboration errorを生じず初回exact-sourceで全ジョブ成功。定理PR #2803をsquashマージ後、SHA 74a2e656afd72a4796fd322d7602f9f904e0a15a がcanonical main HEADと完全一致したことをGitHub MCPで確認した。

## 5. 次の研究段階 GK4AJ（未証明）

GK4AIで確定したのは二つの独立行列を加えた真正第二kernel圏K_AIの圏・関手構成と、K_AI→K_AGの局所非忠実性である。**独立構造商S→K_AIの忠実性は引き続き未証明**。次は実元F54の非可換履歴に対し、二つの行列が揃っても残る真のType値構造商の衝突を探索するか、限定した自由モノイド・群の文脈で観測が忠実となる必要十分条件を証明する。単なる追加行列から自動的にfaithfulnessや完全同値を主張しない。

元P92B Q自身の結合律／左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescent、Gray圏再導入は引き続き未証明・禁止の境界として保持する。

© 2026 板倉英俊 / Hidetoshi Itakura。
