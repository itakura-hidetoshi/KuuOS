# F112-P94D3GK4AO — 真正F54第二行列の行列式・合同制約と到達不能行列

**2026-10-31 JST／canonical Lean定理正本／GitHub MCP exact-source再確認。**

GK4AHの本物の元F54依存型経路から得られる整数2×2第二行列は、任意の形式的整数行列ではない。GK4AOでは元F54の全構成子から実際の整数行列を直接帰納的に評価し、**行列式1と Γ₁(4) 型の合同条件**を証明した。さらに行列式1でも到達不能な具体的行列を示し、GK4ALの「実際に到達する第二行列値の集合」に厳密な算術的必要条件を与える。条件の十分性は主張しない。

## 1. 正本／exact-source CI receipt

| 項目 | GitHub MCP確認結果 |
|---|---|
| 定理PR | [#2815](https://github.com/itakura-hidetoshi/KuuOS/pull/2815) — MERGED |
| 最終exact-source HEAD | `4ec9d203faf04b55052eda50ee62e9049653f846` |
| CI test-merge checkout SHA | `4707d513eff5c9efa345956a3b867e6cf0816336` |
| source／CI／定理squash共通Git tree | `46662c1bba4d875a0da646980957e161fe97ddf3` |
| 定理squash SHA・定理統合直後main HEAD | `d8e471901e47a34c1e4a56058789e27a3f937552` |
| exact-source CI | [#41194437867](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41194437867) terminal SUCCESS |
| Strict Lean | **3770/3770 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 公理表示 | **新規27宣言**、`propext`・`Classical.choice`・`Quot.sound` 以内 |
| `sorryAx` | **0** |
| 変更Lean warning/error | **0/0** |
| 変更 | **append-only新規Lean 2ファイル**、既存Lean変更なし・公開root107維持 |
| 固定環境 | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft／OPEN／未マージ |

元F54の証明正本はcanonical `main` のLean本文に置く。README・ROADMAPは解説用の後続文書であり、Lean定理やexact-source CIを置換しない。

## 2. 生成子から算術的必要条件を証明

[GK4AOIntegralCongruence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AOIntegralCongruence.lean) は `NativeGK4AHMatrix=(Int×Int)×(Int×Int)` に対し、

```text
det([[a,b],[c,d]]) = a*d - b*c
IntegralCongruence(M) :=
  det(M)=1
  ∧ (∃x∈ℤ, a=1+4x)
  ∧ (∃y∈ℤ, c=4y)
  ∧ (∃z∈ℤ, d=1+4z)
```

という元のType値に依存しない整域算術制約を定義した。これは標準的な記号でいえば `Γ₁(4)` の合同条件に対応する。既存GK4AHの正確な非可換積 `nativeGK4AHMul` について、**4成分の整数多項式等式から det(uv)=det(u)det(v)** を証明。さらに合同条件を満たす2行列の積が再び条件を満たすことを、対角・下左成分それぞれの整数証人を具体的に構成して証明する。

真正元F54の生成子：

```text
C  = [[1,1],[0,1]]   -- two-Nat original cast
F  = [[1,-1],[0,1]]  -- genuine forward rotation
R4 = [[1,0],[4,1]]   -- genuine backward rotation
I  = [[1,0],[0,1]]
```

はいずれも合同条件を満たす。これは当該生成子の**行列表現**に関する事実であり、元F54に抽象自由generatorを追加したのではない。

`nativeGK4AORotationEdge_sound`、`nativeGK4AORotationChain_sound`、`nativeGK4AODepthRotationRoute_sound` によって、実際の中間F45木を保つ RotationEdge／RotationChain と、すべての元 `DepthRotationRoute` 5構成子（chain・castDepths・trans・leftContext・rightContext）へ帰納的に伝播する。

## 3. 元Q、独立S、新K_AIおよび任意ファイバーへの厳密な伝播

GK4AHの元F55全9・元P92B全9・独立構造seam全14・拡張比較3の**実Type値保存証拠**をそのまま使用し、元P92Bの存在商 `Q` と独立構造商 `S` を別々に観測。元Q自身の結合律／左右単位は仮定しない。

Lean宣言：
- `nativeGK4AOP92_sound`
- `nativeGK4AOStructural_sound`
- `nativeGK4AOKernel_sound`
- `nativeGK4AOFiber_sound`
- `nativeGK4AOAttainedMatrix_subset`

任意の元F45完全依存型Hom `first,last` と旧類 `q:K_AG(first,last)` に対して、GK4AJ/GK4ALの本物の

```text
Fiber(q) = {z : K_AI(first,last) // U_AI,AG(z)=q}
Attained(q) = range (M_AH|Fiber(q))
```

は

```text
Attained(q) ⊆ {M : Mat₂×₂(ℤ) | IntegralCongruence(M)}
```

を満たす。元の観測値等式から新しいType値3-cellを生成してはいない。

## 4. 行列式1だけでは到達できない — 具体的反例

[GK4AORestrictedMatrixImage.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AORestrictedMatrixImage.lean) は

```text
N = [[1,0],[1,1]]
det(N)=1
```

を定義した。左下成分1は4で割り切れないため、`¬ IntegralCongruence(N)` を `omega` で証明。この一つの行列は、**どの真正元F54経路、どの元P92B Q類、どの独立構造S類、どの新K_AI類、どの実旧qの忘却ファイバーでも到達不能**である。

すなわち

```text
det(M)=1  は到達性の必要条件だが十分条件ではない。
```

加えて、全ての真正 `Fiber(q)` は合同条件を満たす行列型へ単射で写り、**実際に到達する部分集合とのみ Equiv** を持つ（`nativeGK4AORestrictedFiberMatrixEmbedding` と `nativeGK4AORestrictedAttainedFiberEquiv`）。`Γ₁(4)` 全体への全射、任意の整数2×2行列の実現、完全な値域分類は未証明である。

## 5. Lean elaboration failure 修正経緯

初回PRソースで `RotationChain` 帰納法の `| refl _ =>` に対して、固定Leanのconstructor alternativeは**追加pattern引数0個**を期待し、`Too many variable names provided` と報告した。構造的理由は当該コンストラクタのpattern引数の arity 不一致である。変更ファイル全文・imports・原GK4AH定義・既存署名を確認し、`| refl =>` へ修正した。この最終sourceで **3770/3770 SUCCESS**、27宣言は標準3公理以内・`sorryAx=0`・変更Lean warning/error0/0 を確認。初回失敗CIは成功証拠として使用しない。

## 6. 現在の数学的境界と次候補GK4AP

GK4AOはGK4ANまでの**各q_kの2k+1点埋め込み**、GK4ALの全ファイバー可算性、GK4AMの正数kでの`¬FamilyCovers(k)`を弱めない。固定単一ファイバーの無限性、既存有限族の全体濃度、`Γ₁(4)` 全域到達性、`S→K_AI`全域忠実性／非忠実性、元P92B Q自体の圏公理、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、Gray圏、hyperdescentは**未証明**。

次段階GK4AP候補：固定旧qの到達行列集合を `Γ₁(4)` 内部でさらに絞る、不変量と同じqに無限個の異なる真正行列を載せる可能性を区別して検討する。有限サンプルの一致だけで完全値域分類や元Type値比較証拠を導かない。

© 2026 板倉英俊 / Hidetoshi Itakura。Apache-2.0。
