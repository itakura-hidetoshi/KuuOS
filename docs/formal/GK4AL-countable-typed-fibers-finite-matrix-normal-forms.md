# F112-P94D3GK4AL — 真正忘却ファイバーの可算性と条件付き有限行列正規形

**2026-10-31 JST／canonical main**。元F45の任意の完全依存型Homに対し、真正第二商 `K_AI → K_AG` の各ファイバーの可算性を、既存GK4AJの第二行列単射からLean4形式化した。GK4AKで得た任意大有限下界と矛盾せず、両者を一つの真正ファイバーに結び付ける。GK4AKのroot README／ROADMAP未同期分も、本GK4AL文書PRで合わせて同期する。

## 1. 正本・exact-sourceとCI

| 項目 | 確認結果 |
|---|---|
| 定理PR | [#2809](https://github.com/itakura-hidetoshi/KuuOS/pull/2809) MERGED |
| final source HEAD | `ef696a52c417306d3c7c37cfcc32dd3ba0e0aa44` |
| CI実checkout（test-merge） | `a69bbc6b01c655645ca95e54b707b2dcf62816e9` |
| source／checkout／squash共通Git tree | `b8f1caa585eeab43fa856dda8142a6dd6d2eebf8` |
| 定理squash SHA・マージ直後main HEAD | `6bbf03a04ee972399d54828d915e8f739698bcd5` |
| 最終exact-source CI | [#41190283756](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41190283756) attempt 1 |
| Strict Lean | **3765/3765 SUCCESS** |
| Governance | **5/5ジョブ SUCCESS** |
| 変更 | append-only新規Lean 2ファイル、既存Lean変更0 |
| 新規公理表示 | **14宣言**・`propext`, `Classical.choice`, `Quot.sound` の標準3以内 |
| `sorryAx`／変更Lean warning/error | **0／0/0** |
| 固定環境 | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

GitHub MCPで上記source・test-merge・squashのGit tree完全一致を独立確認。既存API検査、workflow integrity、Strict Lean、GovernanceすべてターミナルSUCCESS。初稿で使用した可算性補題名`Countable.of_injective`は、固定Mathlibの実際の`Function.Injective.countable`へソース全体の依存を確認して修正した。初稿のCIはソース更新でキャンセルされたため、その完了判定は使用せず、上記修正版final HEADだけを判断に使用した。

## 2. すべての真正型付きファイバーの可算性

[真正ファイバーの可算性Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ALCountableFibers.lean)は元の型付き木`first`, `last`と、任意の旧K_AG類`q`に対して定義済みの本当の従属型

```text
Fiber(q) := {z : K_AI(first,last) // U_AI,AG(z) = q}
```

から、元GK4AH第二整数行列`M_AH(z)`への**単射**を作り、

```text
Countable Fiber(q)
```

をLean定理`nativeGK4ALFiberCountable`として証明する。行列型`NativeGK4AHMatrix=(Int×Int)×(Int×Int)`は可算。GK4AJの`nativeGK4AJFiberMatrix_injective`を直接使うため、LocalRotation、実F54単位律や元Qの圏公理は不要。さらに`nativeGK4ALKernelHomCountable`により、任意の元F45型付きHomの**K_AI全Hom自体が可算**である。

`nativeGK4ALAttainedMatrixSet`は実際に到達する第二行列値の集合（`Set.range`）。`nativeGK4ALFiberAttainedMatrixEquiv`は次の正確な同値を再利用して証明する。

```text
Fiber(q) ≃ { M : NativeGK4AHMatrix //
             M ∈ Set.range (nativeGK4AJFiberMatrix first last q) }
```

これは**全整数行列が到達することを意味しない**。観測値を単なる自由な整数4組と同一視しない。

## 3. GK4AKとの結合：任意の有限下界を持つ可算ファイバー

[真正有限族・正規形条件Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ALFiniteMatrixNormalForms.lean)は、元F54真正LocalRotationを固定し、GK4AKの

```text
W_k(j) = B^(6j) ; C ; B^(12(k-j)) ; C ; B^(6j)
0 ≤ j ≤ k
```

を再利用する。これらは単一の旧観測類`q_k`に忘却されるが、第二行列から

```text
L(M_AH(W_k(j))) = 8 - 192 * (k - j)
L([[a,b],[c,e]]) = 4*b + 2*e - 2*a - c
```

という整数線形decoderで添字を復元できる。従って任意kについて本当の到達行列集合への

```text
Fin(k+1) ↪ NativeGK4AHMatrix
Fin(k+1) ≃ {M // ∃ j : Fin(k+1), M_AH(W_k(j)) = M}
```

を作る。ここでの同値は**構成された有限部分族に対してのみ**であり、全ファイバーとの同値を無条件に主張しない。

主定理`nativeGK4AL_arbitrary_finite_countable_fiber`は

```text
∀ k : Nat, ∃ q_k : K_AG(before,before),
  Countable (Fiber(q_k)) ∧ Nonempty (Fin(k+1) ↪ Fiber(q_k))
```

を、真正元F54の型付き源経路から証明。さらに`nativeGK4ALPhysicalNorth_arbitrary_finite_countable_fiber`は**真のC60北側六角形**に無条件で特殊化する。

## 4. 「有限族が全体を尽くす」と言えるための正確な障害

`nativeGK4ALFamilyCovers rot k`は、選んだ`Fin(k+1)`経路族が実際の`Fiber(q_k)`へ**全射**であるという**追加命題**として定義する。Lean定理`nativeGK4ALFamilyCovers_iff_matrixCover`は、次の必要十分条件を証明する。

```text
FamilyCovers(k) ↔
  ∀ z : Fiber(q_k),
    ∃ j : Fin(k+1), M_AH(z) = M_AH(W_k(j))
```

この条件は第二行列のファイバー内単射により厳密に成立し、逆向きも失われない。**被覆条件そのものは証明していない**。その仮定が与えられた場合に限り、`nativeGK4ALExactFiniteFiberEquivOfCover`は

```text
FamilyCovers(k) → Fin(k+1) ≃ Fiber(q_k)
```

を返す。従って、ファイバー全体のexact cardinalityや構成族の網羅性は現段階では未知のままである。

## 5. 境界／次候補

- 今回の定理は「各ファイバーは高々可算」かつ「サイズはファイバー間で一様に有限有界ではない」という**両立する二主張**である。異なるkのターゲットq_kはGK4AKで相異なることも証明済み。一つの固定ファイバーが無限であることは今回の結論ではない。
- `S→K_AI`の全域忠実性、全整数行列の到達可能性、`q_k`ファイバーの正確な元数、元P92B Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、Gray圏およびhyperdescentは**未証明**。
- 次候補**GK4AM（未証明）**：固定した真の旧類qについて無限個の元F54真正経路を同時に載せられるかを検討し、有限族の非網羅性の証人または到達値の具体的制限を探す。有限下界の非一様性から単一無限ファイバーを推論しない。

前段の[GK4AK詳細証明](GK4AK-unbounded-finite-forgetful-fibers.md)・[#2807定理PR](https://github.com/itakura-hidetoshi/KuuOS/pull/2807)も本証明と合わせて保持。公開root107、strict空中心・独立Kuuは一presentation、Gray非再導入、保護検証PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを維持。

© 2026 板倉英俊 / Hidetoshi Itakura。
