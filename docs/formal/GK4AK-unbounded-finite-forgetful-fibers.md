# F112-P94D3GK4AK — 真正忘却ファイバーの任意大有限下界

**2026-10-31 JST。** 唯一の定理正本は `itakura-hidetoshi/KuuOS` の canonical `main`。GK4AJまでの正本を変更せず、元F54の真正型付き経路から新規Lean2ファイルを追加した。

## 正本と検証記録

| 項目 | 確認済みの値 |
|---|---|
| 定理PR | [#2807](https://github.com/itakura-hidetoshi/KuuOS/pull/2807) — MERGED |
| final source HEAD | `bd6b4d379cded78b6768d5a2392fbe57c2403a90` |
| CIの実checkout commit | `90f6557637fcacd8e82128b6833f1d87d261430d`（PR test-merge） |
| sourceとcheckoutの共通Git tree | `779064c2db71ac0da0b1e2afff3321b3b634a5cc` |
| 定理squash SHA／マージ直後main HEAD | `6a514bf30d0836a4ba67e18e6b65a694041c7a7f` |
| exact-source CI | [#41188601545](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41188601545), attempt 1 |
| Strict Lean | **3763/3763 SUCCESS** |
| Governance | **5/5 jobs completed SUCCESS** |
| 新規Lean | 2ファイル、既存Lean変更なし |
| 公理表示 | **36宣言、標準3公理以内** |
| sorryAx／変更Lean warning/error | **0／0/0** |
| Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

Strict Lean job `124500575154` の保存artifact `13037802181` を取得し、SHA-256 `487f2b503fb7ae2c58b59e377febd6d478d81abb802f672e44266b3e26ef3cd8` がGitHub記録と一致することを確認した。内部 `lean-formal/receipt.json` は return_code=0／status=passed、warningAsError=true／sorryAsError=true。完全なcheck.logには新規36宣言の公理依存があり、`propext`・`Classical.choice`・`Quot.sound`以外なし、sorryAxなし、新規ファイルのwarning/errorなし。

CIはPRのtest-merge commitをcheckoutしている。したがってsource SHAとcheckout SHAを同一視せず、両者の**Git tree完全一致**をGitHub MCPで別途検証した。定理squash commitのtreeも同一である。初回のexact-source検証で成功し、Lean修正・再実行は不要だった。

## 1. 証明した主定理

真正F54局所回転 `rot : LocalRotation p before after` を持つ固定された型付き自己Homで、任意の自然数kについて、実際に到達した旧観測商の類q_kと埋め込みを構成した。

~~~text
forall k : Nat,
  exists q_k : K_AG(before,before),
    Nonempty (Fin(k+1) ↪ Fiber(U_AI,AG, q_k))
~~~

ここで `U_AI,AG : K_AI → K_AG` はGK4AIで構成済みの真正忘却関手のHom写像。ファイバーはGK4AJの元依存型定義

~~~text
nativeGK4AJOldFiber before before q_k :=
  {z : K_AI(before,before) // nativeGK4AIForgetMatrix before before z = q_k}
~~~

そのものである。単なる行列の集合をファイバーと呼び替えたものではない。真正C60北側六角形の `northHexagonNativeLeftRotation` を用いた、すべてのkに対する無条件の特殊化も証明した。

## 2. 元F54の真正経路族

[元F54のパラメータ経路と観測計算Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AKParametricPhysicalWords.lean)では、元の二Nat castDepths自己経路をC、実前後2回転backtrackをB、P=B^6とする。

~~~text
W(j,d) = P^j ; C ; P^(2d) ; C ; P^j
       = B^(6j) ; C ; B^(12d) ; C ; B^(6j)

W_k(j) = W(j,k-j),  j : Fin(k+1).
~~~

前段で提案した `B^(3j) C B^(6(k-j)) C B^(3j)` の、パラメータを `(2k,2j)` とした偶数添字部分族である。旧行列の符号処理を避けつつ、k+1個の真正経路を確保できる。ゼロ冪は元 `RotationChain.refl` から作り、元Qの単位律は仮定しない。各合成は元 `DepthRotationRoute.trans` であり、型付き境界・元LocalRotation証拠を保持する。

P^nの観測をnについての帰納法で証明した。

~~~text
rotationCount(P^n) = 12n
AD(P^n) = ((-12n,6n), -36n^2)
M_AF(P^n) = I
M_AH(P^n) = [[1+12n,6n],[-24n,1-12n]]
~~~

## 3. 旧観測値はkだけで決まる

j+d=kのとき、元の四成分観測と完全な第一行列はjに依存しない。

~~~text
O_AE(W(j,d)) = (decide(k=0), 2-24k, 12k, 12k-144k^2)
M_AF(W(j,d)) = [[1,2],[0,1]]
~~~

k>0でBoolean gradeはfalse。k=0も除外せず、元のゼロ回転・2cast経路として正しく扱う。四成分のorderedMomentを落とした数え上げではなく、旧GK4AG積観測全体の等式を証明した。

`q_k` は `W(0,k)` の元S類を真正 `S→K_AG` 比較で写した値として定義する。ゆえにq_kの到達可能性は具体的な元F54経路で保証される。全jについて新K_AI類の忘却像がこの同じq_kになることを証明した。

## 4. 行列の一次結合による添字の復元

第二行列 `M_AH(W(j,d))=[[a,b],[c,e]]` から、線形写像

~~~text
L(M) = 4*b + 2*e - 2*a - c
~~~

を取ると、厳密に

~~~text
L(M_AH(W(j,d))) = 8 - 192*d
~~~

となる。行列全体の高次成分は相殺されるため、固定kに対してd=k-jを、従ってjを一意に回収できる。Leanでは元経路のsecond-matrix評価を帰納法で書き換え、整数環の等式を`ring`、有限添字の境界と差を`omega`で証明した。有限範囲の数値実験を一般の証明の代用にはしていない。

式の仕組みは、`N=[[-2,-1],[4,2]]`、`N^2=0`、`P=I-6N`として、行ベクトルr=(2,1)・列ベクトルs=(-1,2)^TがrN=0、Ns=0を満たすことからも説明できる。L(M)=rMsであり、外側のP^jを消して `r C (I-12dN) C s = 8-192d` が残る。これは証明の説明で、Leanの正本は `nativeGK4AKWord_decoder`。

## 5. 真正第二商への埋め込みと限定的な分離

[真正有限ファイバーの埋め込みLean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AKUnboundedFiniteFibers.lean)で構成した主要宣言：

~~~text
nativeGK4AKClass_forget
nativeGK4AKClass_decoder
nativeGK4AKClass_injective
nativeGK4AKStructuralFamily_injective
nativeGK4AKFiberEmbedding
nativeGK4AKOldTarget_value
nativeGK4AKOldTarget_injective
nativeGK4AK_arbitrary_finite_fiber
nativeGK4AKPhysicalNorth_arbitrary_finite_fiber
~~~

まず元SからK_AIへ写したクラス族の単射性を第二行列のdecoderで示す。これにより元Sの**この構成族に限った**単射性も従う。最後に忘却値等式を持つsubtype要素を構成し、本物の `Fin(k+1) ↪ Fiber(q_k)` を与える。観測値一致から元P92BのType値比較証拠を生成する操作は行っていない。

## 6. 結論の範囲と次段階

今回の結果は、忘却ファイバーの大きさに**一様な有限上限を置けない**ことを意味する。一方、q_kのbackwardCountは12kであり、異なるkのq_kは相異なることもLeanで証明した。

従って次の主張は今回の結果には含めない：

- 一つの固定ファイバーが無限であること。
- 構成したk+1類がファイバー全体を尽くすこと、または大きさがちょうどk+1であること。
- 元の独立構造商S→K_AIの全域忠実性、または残余非忠実性。

元Q自身の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentも依然未証明。公開root107、strict空中心／独立Kuu一presentation、Gray非再導入、保護検証PR #1558 Draft/OPEN/未マージを維持した。

**次候補GK4AL（未証明）：** GK4AJのファイバーから整数行列への単射を用いた各ファイバーの可算性と、構成した有限部分族の正規形・全ファイバーを尽くす条件を区別して形式化する。元S→K_AI自体の忠実性問題は別途保持する。

## 文書反映範囲

本記録はGK4AKの新規詳細文書として追加したもの。ルートREADME.md・ROADMAP.mdの既存履歴はこの文書追加では変更しておらず、トップのfrontier表記のGK4AK同期は別作業として残る。定理の正本・マージ状態は上記exact-sourceとcanonical mainのLeanファイルを優先する。

© 2026 板倉英俊 / Hidetoshi Itakura。
