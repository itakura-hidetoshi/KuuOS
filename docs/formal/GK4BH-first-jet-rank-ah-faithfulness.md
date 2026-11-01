# F112-P94D3GK4BH — 元F54の一次ジェット、物理rankと真正K_AIにおけるAH忠実性

**2026-11-01 JST。** 唯一の定理正本：`itakura-hidetoshi/KuuOS` の `main`。GK4BHは2つの独立exact-source定理PRで構成し、いずれもMERGED。

- [第一定理PR #2858](https://github.com/itakura-hidetoshi/KuuOS/pull/2858)：[元F54の一次ジェット／GK4AD全履歴復元Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHFirstJetADRecovery.lean)。
- [第二定理PR #2859](https://github.com/itakura-hidetoshi/KuuOS/pull/2859)：[原始物理rank・grade判定／真正AH忠実性Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHGradeRankFaithfulness.lean)。

## 1. 数学的正本 — 本物の元F54依存型ルートに限る

旧GK4ADの非可換順序付き値を `d=((c,b),m)`（`c: Int`、`b: Nat`、`m: Int`）とする。真正元F54型付き経路がもつ整数多項式行列 `P(X)` の**定数・一次係数だけ**から、次を復元する：

```text
b = coeff(P_21, 1)
c = coeff(P_12, 0) - b
m = coeff(P_11, 1) - triangle(b)

triangle(b) = b*(b-1)/2, b : Nat
```

正確な乗法不変量 `nativeGK4BHJetLinked` は次の6条件を持つ：

```text
coeff(P_11, 0) = 1
coeff(P_12, 0) = c + b
coeff(P_21, 0) = 0
coeff(P_22, 0) = 1
coeff(P_11, 1) = m + triangle(b)
coeff(P_21, 1) = b
```

元GK4ADの非可換則は

```text
((c,b),m) ⋆ ((d,e),n) = ((c+d,b+e),m+n+c*e)
```

であり、`nativeGK4ARTriangle_add` の `triangle(b+e)=triangle(b)+triangle(e)+b*e` が、原始多項式行列積の一次係数に含まれる交差項と**正確に一致**する。固定mathlibの `Polynomial.mul_coeff_zero` / `Polynomial.mul_coeff_one` で証明した。これは可換語数への置換ではない。

元のF54のforward/backwardの**実在する向き付きLocalRotation**、中間F45木付きRotationChain、真正二Nat casts、5構成子全て（transと左右依存文脈を含む）で証明済。GK4BAの `t=4` 一点決定性により、AH行列一致から元多項式全体が一致し、従ってこの6係数から **元GK4AD全体が一致**する。既存第二kernel `K_AI` の真のHomへも二重のQuotient帰納法で降下した。

## 2. 元F54物理rankによるBoolean gradeの完全判定

元F54の原始型付き始点・終点を `first,last` とする。原始の後退物理回転数は `b(r)`、全原始回転数は `rotationCount(r)`。既存GK4ACの `gk4acLeftRank` を用い、以下をLean4で証明した。

```text
b(r) <= rotationCount(r)
rotationCount(r) = 0 -> rank(first) = rank(last)

grade(r) = true
    <-> b(r) = 0 AND rank(first) = rank(last)
```

逆向きの含意にはGK4ACが元F54の全構文について既証明の `gk4acNoBackward_bound` を用いる。したがってBoolean gradeは元ADに含まれる後退数と、**同じ実在する型付きHomの始点・終点rank**だけで決まり、任意の記号自由積語に新しい型付きsourceループを仮構しない。これを真の`K_AI`第二kernelに降下した。

## 3. 主定理 — 元AH値は既存K_AIの各Hom上で単射

元の真の`K_AI`の同じ型付きHomにある`u,v`について：

```text
M_AH(u)=M_AH(v)  ->  u=v
```

証明の根拠は独立して以下の4成分である。

1. AH一致 → 多項式全族一致（既存GK4BA/GK4BB）。
2. AH一致 → 旧AF一致（既存GK4BG）。
3. 一次ジェット → charge・後退数・orderedMoment全部一致（GK4BH第一定理）。
4. 型付き始点・終点rankと後退数 → Boolean grade一致（GK4BH第二定理）。

元`NativeGK4AIValue`の全成分が一致するため、元第二kernel自身の既証明単射性 `nativeGK4AIKernelValue_injective` で **元のK_AI類が一致**する。従って `nativeGK4BDOldAHFunctor` は各Hom上でfaithfulである。

GK4BFの`K_AI -> AH_attained`像関手は、従来証明済のHom全射性と今回のHom単射性を併せ、**全型付きHom上で全単射**。各固定AH値のK_AIファイバーは `Subsingleton`、GK4BGで条件付きだった「異なる到達AE値の2件が同じAHへ落ちる」obstructionは、**元K_AI上では存在しない**ことを証明した。

これは**元Type値F54生経路の同一性ではなく、元Q自身の結合律・単位律や独立構造商`S -> K_AI`の忠実性を意味しない**。また任意の整数2×2行列がAH像へ到達するとも主張しない。

## 4. exact-source CIとLean4構文修正

| 監査項目 | 第一定理PR #2858 | 第二定理PR #2859 |
|---|---|---|
| 状態 | MERGED | MERGED |
| 最終source SHA | `d7aa7798a4a39e7450532dab02f0910c1c073adb` | `2c16bad8e8a893c66dda68c28da1625c82bf6f83` |
| test-merge SHA | `77fb5d2eefbc7fa1ae2c7d5b8e48ad990e092882` | `3ae76d2513ad9748ff111fafe3754f5717373bbd` |
| 共通Git tree | `d1c3413213a8b8469cf8c8da93d71778035ae512` | `f87b3edba4497d24229339cd6c71685986c9e84e` |
| exact-source CI | [#41260074882](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41260074882) | [#41260689362](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41260689362) |
| Strict Lean | **3802/3802 SUCCESS** | **3803/3803 SUCCESS** |
| Governance | **terminal SUCCESS** | **terminal SUCCESS** |
| 新規宣言・公理 | 12宣言、標準3公理以内 | 12宣言、標準3公理以内 |
| `sorryAx` | 0 | 0 |
| theorem squash SHA | `93db9b5f77c8554f9fc52a7c7f057188de1b83a0` | `d4c435af91f4b4d9f605ee8739b6b758b79003d0` |

初回第一定理の修正では、単純な`coeff(P_12,0)=charge`という**誤った候補**を、原始backwardの`charge=-1`かつ`P_12(0)=0`という実験で否定した。正しい`charge+b`と`moment+triangle(b)`の補正に置き換え、固定mathlibの係数APIで非可換積まで証明。Lean4の自動簡約に使われない `Polynomial.coeff_one` を明示し、`<;>`で目標消滅後の余分なタクティクを防いだ。

第二定理は初回の`RotationChain.refl`パターンに不要な引数名を与えた**記法の誤り**だけが残ったため、`| refl _ =>`を`| refl =>`に修正してexact-sourceを再検証。新規ファイル全文、imports、依存シグネチャ、公理依存を検査済み。

## 5. 保護条件と残る研究範囲

唯一の定理正本`main`、Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107を維持。strict空中心・独立Kuuは一presentation、Gray非再導入、保護PR #1558は Draft/OPEN/未マージ。

今回解消したのは**旧AHを用いたK_AI内部の観測非忠実性**。元Q自身の未証明圏公理、元SからK_AIへの非忠実性、真正F54 Type値3-cellの生成、元Type値完全同値、固定単一旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは残る。

次段階候補GK4BIは、Hom全単射である元K_AI→AH到達圏の関手を、真のMathlib `Equivalence` へ昇格させること。ただし元QやSの証明歴史同一性へ拡張しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
