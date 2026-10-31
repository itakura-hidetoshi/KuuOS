# F112-P94D3GK4AU — 真正整数パラメータ行列族と合同条件の必要十分性

2026年10月31日 JST。既存の第一行列AF・第二行列AHを、同じ真正F54経路から得られる整数パラメータ付き観測族に統一した。既存行列を置換せず、パラメータ1・4で厳密に回収する。さらに、真正の局所回転が存在する同一自己Homでは、二つのパラメータで全経路の観測値が合同になる条件を必要十分に分類した。

## 1．定理正本・exact-source検証

| 項目 | 確定値 |
|---|---|
| 定理PR | [#2827](https://github.com/itakura-hidetoshi/KuuOS/pull/2827) — MERGED |
| final source HEAD | `4c96aa69f2e081d1e299a1ce5019aad31ac58b4a` |
| 実CI checkout | `1300b74e21d2c1b67617449df7810d568e975694` |
| 定理squash／統合直後main | `cf4679813e7f767af7d44bbd273de18661e3c2cf` |
| 三者共通Git tree | `5719f12b9bb2718a1dc9cfce40bb65d63578a7e2` |
| exact-source CI | [#41204182959](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41204182959) — terminal SUCCESS |
| Strict Lean | **3781/3781 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 新規証明 | **2 Leanファイル・55公理依存表示宣言** |
| 公理依存 | propext・Classical.choice・Quot.sound以内、sorryAx0 |
| 変更Lean warning／error | **0／0** |
| 固定環境 | Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root | 107維持、既存Lean証明本文の変更なし |

[パラメータ族と全比較保存のLean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AUParametricMatrixInvariant.lean)・[特殊化・行列式・合同必要十分条件のLean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AUParameterCongruence.lean)。Authorityは canonical main exact HEAD → Lean本文 → exact-source CI → 文書 → 過去要約。

## 2．同一真正sourceから得られる観測族

値の型は `NativeGK4AUValue := Int → NativeGK4AHMatrix`。掛け算は既存AHの検証済み整数2×2行列積を点ごとに適用する。原始生成子は

```text
C(t) = [[1,1],[0,1]]
F(t) = [[1,-1],[0,1]]
R(t) = [[1,0],[t,1]],     t in Int.
C(t)*F(t)=I.
```

元F54の実RotationEdge、途中木を保持するRotationChain、DepthRotationRouteのchain／castDepths／trans／leftContext／rightContext全5構成子から族を定義する。任意の記号文字列を真正経路の代わりに仮定しない。

元F55の9構成子、P92Bの9構成子、独立構造seamの14構成子、拡張比較の3構成子に対して、**族全体の関数としての等式**が保存されることを証明した。元P92B存在商Qと独立Sへ別々に降下し、Q→S比較との可換性、S上の合成・単位保存も証明済み。元Q自身の未証明圏公理は使わない。

## 3．既存の二観測の厳密な回収と行列式

全真正経路r、さらに元Qと独立Sの各類について

```text
M_r(1) = M_AF(r)
M_r(4) = M_AH(r)
det(M_r(t)) = 1, for every integer t.
```

を証明。これはtraceや合同類だけの一致ではなく、整数行列そのものの一致である。新族を導入しても既存のAF/AHおよびGK4ATまでの全定理を変更しない。

## 4．合同条件はパラメータ差の整除性で正確に決まる

固定mathlibのInt.ModEqの加法・乗法保存により、任意整数k,s,tについて

```text
s ≡ t (mod k)  implies  M_r(s) ≡ M_r(t) (mod k), entrywise,
```

を全真正経路r、元Qと独立Sの各類に証明した。k=0も含むInt.ModEqの意味での主張。

逆向きには、実際の `rot : LocalRotation p before after` を仮定する。この同じType値証拠をforward／backwardに使った既存の真正往復経路Bについて

```text
M_B(t) = [[1-t,-1],[t,1]].
```

したがって左下成分からt自身が読み取れる。この文脈の自己Hom H(before,before)では

```text
(for every r in H, M_r(s) ≡ M_r(t) mod k)
    iff s ≡ t mod k
    iff k divides t-s.
```

をLean4証明した。元Q自己Hom・独立S自己Homでもそれぞれ同じ必要十分条件を証明。真正C60 northの既存局所回転証拠による具体的特殊化も含む。**任意の自己Homに局所回転があると仮定してはいない。**

## 5．GK4ATの法3の最適性と観測族の区別

s=1,t=4とすると、局所回転を持つ同一真正自己Homで

```text
(for every r, M_AF(r) ≡ M_AH(r) mod k) iff k divides 3.
```

従って正の法について普遍的に使えるものは1と3であり、法3はこの意味で最適である。これは**同じ経路に対する二観測の比較**であり、GK4ATの「同じ旧qファイバー内の二経路では法48／法12で一致」とは異なる量化。両者は矛盾せず、以前の固定ファイバー制約はすべて維持する。

同じ真正S自己Hom上で、tを観測写像 `q ↦ M_q(t)` に送る対応が単射であることも証明した。これはパラメータが異なれば観測写像が異なるという意味であり、一つの観測写像が源の全履歴を忠実に区別するという意味ではない。

## 6．文脈を署名から消さないLean修正

初回CI #41203875080では、族全体の比較保存ファイルはBuiltしたが、後半の必要十分条件で `rot` がUnknown identifierとなった。Lean4の定理はヘッダーで使うsection変数を引数として採用し、証明中だけの変数は自動では取り込まない。型付き局所回転の存在を結論から読み取れないため、対象sectionに `include rot` を明示した。

これは空・縁起の扱いとしても重要で、パラメータを検出できるという結論は、実際に往復経路を構成できる文脈に依存する。その成立条件を消して無条件の性質として扱わない。変更Lean2本全文、imports、dependent signatures、固定mathlib APIを確認し、数学的に必要な証拠を正しい署名へ保持した。仮定を弱める修正は行っていない。

最終receipt.jsonのgit_shaと完全check.logで3781/3781成功・55公理表示・sorryAx0・変更Lean warning/error0/0を確認。CI runner自体のバージョンCommitと実checkout SHAは区別した。source／checkout／squashのGit tree一致も独立に照合した。

## 7．保持する境界と次段階

全整数パラメータ族は元Qと独立Sへ降下する。一方、t=1,4の二評価だけを含む既存K_AIへ**族全体も降下するとは証明していない**。二点での値の一致から全関数の一致を作らない。

固定単一旧qファイバーの無限性、算術slice全域到達、元Q自身の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、hyperdescentは引き続き未証明。GK4ATの厳格sliceと法48／法12制約は維持。

**次はGK4AV（候補・未形式化）。** この真正族を整数係数多項式行列へ持ち上げ、評価との整合、次数と元backwardCountの関係を検討する。二評価しか保持しない商への降下可能性は別問題として扱う。

Append-only／tighten-only／same-root107。strict空中心、独立Kuuは空の一presentation。Gray非再導入、保護PR #1558はDraft・OPEN・未マージを維持。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
