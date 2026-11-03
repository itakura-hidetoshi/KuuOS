# F112-P94D3GK5BF／Qi v4.25 — 反転深さ重みによる同一F54 Hom内の局所seam障害

**正式証明記録：2026年11月3日 JST。** [KuuOS canonical main](https://github.com/itakura-hidetoshi/KuuOS)。strict 空 authority、独立Kuu→Qi、公開root107。元F54双Nat・二圏・Blocksと元F55 Type値証拠履歴を保存。

## 1. 独立GK5BFの形式化と検証

- [独立定理PR #3043](https://github.com/itakura-hidetoshi/KuuOS/pull/3043) **MERGED**。exact-source HEAD 6046c54269e14e4b2b178fb65e748e260d201943、test-merge be846bc7b542d59f26f54aa243d7e649f2675293、squash d5ced0fc31a306b02b58823e034783c27392b599。三者のGit treeは 474826129810b64cdc11012d23a459c85e741f14 で一致。
- [exact-source CI #41631574051](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41631574051)：**Strict Lean 9,268/9,268 SUCCESS、Governance 30/30 SUCCESS**。新規24宣言の公理監査にsorryAxなし。必要な既存公理依存はpropext・Classical.choice・Quot.sound以内。
- [Lean正本](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFDoubleInversionWeightObstruction.lean)。独立Kuuにのみ追加し、公開KuuOSFormalへappend-only import済み。

GK5BBのunsigned wrapper総数 N はP92B.symmで不変、GK5BEのsigned原始grade S はP92B.symmで符号反転する。GK5BFはそれらより詳しい**反転深さ重み W : P92B → Nat**を新規導入する。W(original(f))=1、W(refl)=W(assocNaturality)=0、W(symm(u))=2W(u)、W(trans(u,v))=W(u)+W(v)。F45/F54 contextで重みを保存し、真正水平合成でも加法的。選択symmの深さkにあるoriginal-wrapperは重み2^kを持つ。

P93Cの全16構成子、P94Aの全19構成子について、真正のType値四セルがWの値を保存することをLean4帰納法で証明した。P94Aの追加horizontalUnit・leftContextUnit・rightContextUnitもそれぞれ検証。

従って局所seamの存在には、N(φ(f))=1、S(φ(f))=1、W(φ(f))=1 の**三条件が必要**である。三条件が十分であるとは主張しない。

## 2. 同一F54 Hom内の厳密な反例

真正北C60の元pentagon原始F55証拠を p とし、元F55二重反転 c := symm(symm(p)) をとる。pとcは**同じ元F54 long→short始点・終点**を持つ真正の証拠であり、構文は異なる。

原始pではφ(p)=original(p)で、真正P94A.refl seamが実在する。二重反転cでは以下が同時に成立する：

    N(φ(c)) = 1
    S(φ(c)) = +1
    W(original(c)) = 1
    W(φ(c)) = 4
    ¬ Nonempty(SeamAt(c))

よって**N=S=1という二つの数値必要条件は十分でない**ことを同一F54 Homの元証拠で形式的に反証した。逆向きの別Homに移動しただけの現象ではない。

さらにGK5AJの元P77→選択P93C真正四セル移送と各不変量保存を使い、N=S=1の二条件ゲート、およびN=S=W=1の三条件ゲートを、実際のP77 source四セル商上のPropへQuotient.liftで降下させた。

元pと二重反転cは**同じF54 Hom内でも異なるP77商クラス**であり、元pのクラスは局所seamが正、元cのクラスは負。元cから有限P77四セル証明語で到達可能な全source証拠はseam不存在。

## 3. Qi v4.25 — 二重反転＋真正右単位の統合

- [Qi v4.25 PR #3044](https://github.com/itakura-hidetoshi/KuuOS/pull/3044) **MERGED**。exact-source HEAD 50141de1dd3cb9b54a7b7237b4e3a097e793bf39、test-merge cf02ba1c3c81c7c08a79afd4731eeec200f5a310、squash 84d547945860831c16a326c4e0897a4fd269f60f。三者のGit treeは 0ee10d7560b6e51cc047132437c063cbe089f0ea で一致。
- [exact-source CI #41632314737](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41632314737)：**Strict Lean 10,195/10,195 SUCCESS、Governance 30/30 SUCCESS**。新規11宣言の公理監査にsorryAxなし。
- [Qi Lean正本](../../formal/KUOS/Architecture/QiWuxingGK5BFNorthDoubleInverseClassV4_25.lean) を公開KuuOSFormalへ追加済み。

元F55証拠 c' := trans(symm(symm(p)), ident(short)) を新たにとる。cとc'は真のP77.rightUnit四セルの逆に沿って結ばれ、長さ1の真正P77有限語を持つ。よってP77商クラス等号 [c]=[c'] を構成した。

元c'でもN(φ(c'))=S(φ(c'))=1、W(φ(c'))=4であり、選択P94A局所直接seamは不存在。一方pのP77クラスには局所seamが実在し、元pとc'のP77商クラスが同一でないことをLean4で証明した。**弱い二条件が両クラスで真でも、seam存在性は異なり、強い第三のweight条件が両者を分離**する。

真正北C60五行物理Dartの第五周回と元P89のBadPair反射条件を独立に維持する。WはP92B proof構文の不変量であり、陰陽物理量や元pentagon電荷を意味しない。

## 4. 継承すべき境界・次の研究

成立したのは、P94A全19構成子に対するW保存、同一F54 HomでのN=S=1の不十分性、P77商上の二条件・三条件の降下、正負クラスの厳密な相違である。

**未証明・非主張**：N=S=W=1の一般十分性、P94A全四セルの正規化、元P89の無条件faithfulness/nonfaithfulness、GK5AY全域seam、GK5BA全構成子kit、内部source-image障害の消去、Type値seam証明書のcanonical同一視、Gray復元。

**次のF112-P94D3GK5BG（仮称）**：重み2^kを**反転深さ分布の生成多項式 P_f(X)=∑_k a_k X^k** に拡張し、N=P(1)、S=P(-1)、W=P(2)を比較する。全P94A構成子保存とP77商への降下を個別に証明し、必要条件と十分条件を引き続き分離する。

Lean v4.30.0-rc2、固定mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ維持。append-only、no Gray、sorry、admit、native_decide、新公理なし。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
