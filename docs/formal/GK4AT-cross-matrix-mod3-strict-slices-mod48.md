# F112-P94D3GK4AT — 二つの真正行列観測の法3整合性、厳格な固定旧類slice、法48剰余

2026年10月31日 JST。GK4ASは既存条件の帰結でありAS=ARだった。一方、GK4ATは旧K_AG類が既に保持する第一行列AFと第二行列AHの関係を使い、任意の固定旧類で算術候補を真に絞る。

## 正本と検証

| 項目 | 確定値 |
|---|---|
| 定理PR | [#2825](https://github.com/itakura-hidetoshi/KuuOS/pull/2825) MERGED |
| final source HEAD | `7b79d067a9b8aa8174df7357860de839d3ba6b29` |
| 実際のCI checkout | `91aabe754c4660cbddf9fd77c33f69459dc4bbcb` |
| 定理squash／統合直後main HEAD | `895f6520a4ea2afc06d75f626ff0b721c73d89de` |
| 三者共通Git tree | `8847ec9b69cbeb5e416919c2cb5daabcb18494e2` |
| exact-source CI | [#41201974238](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41201974238) terminal SUCCESS |
| Strict Lean | **3779/3779 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 新規証明 | 2 Leanファイル、28公理依存表示宣言 |
| 公理 | propext・Classical.choice・Quot.sound以内、sorryAx0 |
| 変更Lean warning／error | 0／0 |
| 固定環境 | Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root | 107維持、既存Lean本文の変更なし |

Lean原文：
- [GK4ATCrossMatrixModThree.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ATCrossMatrixModThree.lean)
- [GK4ATStrictJointArithmeticSlice.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ATStrictJointArithmeticSlice.lean)

## 1．独立した二観測は法3で全成分一致する

第一行列AFと第二行列AHのcast Cおよびforward Fは一致する。backwardはそれぞれ

```text
R_AF = [[1,0],[1,1]]
R_AH = [[1,0],[4,1]].
```

従って両者は法3で一致する。固定mathlibのInt.ModEq.add／mulを使い、真正の順序付き行列積に関する整合性を証明した。元F54のforward/backward RotationEdge、中間木RotationChain、DepthRotationRouteのchain／castDepths／trans／leftContext／rightContext全5構成子について

```text
M_AF(r) ≡ M_AH(r) (mod3), entrywise
```

が成立する。元F55/P92Bと独立構造seamに対する既存の実Type値保存証明を使い、元Qと独立Sへ別々に降下。真正K_AI、任意の固定旧K_AG類qの実忘却ファイバーにも適用した。数値の一致から新しいType値3-cellを作ることはない。

## 2．任意固定旧qで、本当に厳格な算術slice

旧qはAD値だけでなくAF行列全体P(q)を既に保持する。

```text
Gamma_AT(q) = {M in Gamma_AS(q) | M ≡ P(q) (mod3), entrywise}
AttainedMatrix(q) ⊆ Gamma_AT(q) ⊊ Gamma_AS(q) = Gamma_AR(q) ⊊ Gamma_AQ(q).
```

すべての先行条件を保持した連言であり、弱い観測への置換ではない。

厳格性には既存の真正忘却写像K_AI→K_AGの全射性を使い、任意qの実到達行列M=[[a,b],[c,d]]を一つ取る。算術行列U(16)=[[1,16],[0,1]]による右移動は

```text
M U(16) = [[a,16a+b],[c,16c+d]].
```

行列式、a mod16、b mod4、c mod16、d mod16は元AS条件を保つ。一方、MとM U(16)が同じP(q) mod3に一致すると、16a≡16c≡0 mod3、従ってa≡c≡0 mod3となりad−bc=1に矛盾する。よってM U(16)は旧AS slice内にありながら新AT slice外にある。

**Mは実到達だが、M U(16)は到達不能を示す算術証人であり、新しい元F54経路として実現すると主張しない。** 真正ファイバーからAT sliceへの埋込みもLean4で証明した。AT全域への全射は主張しない。

## 3．同じファイバーでの法48・法12合同

先行AR/AQ/ASの法16と法3を、固定mathlibのInt.modEq_and_modEq_iff_modEq_mulにより結合する。任意の同一旧qファイバー内の二点x,yについて、

```text
a(x) ≡ a(y) (mod48)
c(x) ≡ c(y) (mod48)
d(x) ≡ d(y) (mod48)
b(x) ≡ b(y) (mod12).
```

右上だけは元APが法4だったため法12となる。全成分を法48とする主張ではない。

## 4．Lean記法修正と証拠の区別

初回CI #41201283764では、独自のnativeGK4ATModThree述語に対するby decideがDecidable合成に失敗した。全変更ファイル、imports、依存する型付き署名、固定mathlibのInt.ModEq APIを確認し、四つの具体生成子について述語・Int.ModEq・行列定義を明示的に展開するnorm_numへ修正した。定理の仮定や結論は変更していない。

最終CIでは新規両ファイルのBuilt、全28宣言の公理依存、sorryAx0、変更Lean warning/error0/0をダウンロードした実receiptと完全ログで確認した。CI runnerヘッダーのCommitと実checkoutを混同せず、receipt.jsonのgit_shaとGit treeを照合している。

## 5．未証明境界と次段階

固定単一旧qファイバーの無限性、算術slice全域の到達、元Q自身の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、hyperdescentは引き続き未証明。

**次はGK4AU（候補、未形式化）。** 第一・第二行列を共通の整数パラメータ付き観測として扱えるか、真正比較証拠の保存を確認しながら研究する。既存条件の帰結と独立obstructionを引き続き区別する。

Append-only／tighten-only／same-root107。strict空中心、独立Kuuは空の一presentation。Gray非再導入。保護PR #1558はDraft・OPEN・未マージを維持。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
