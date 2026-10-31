# F112-P94D3GK4AM — 真正固定旧類における有限族の一様な非網羅性

**2026-10-31 JST／Lean4形式証明・canonical main。**

GK4AKの有限部分族とGK4ALの条件付き有限正規形について、条件 **FamilyCovers(k)** が実際に偽になることを、元F54の本物の依存型自己経路により証明した。GK4AJで既に確立していた3点証人をk=1に結び、さらにすべての正のkへ一様化。単一固定ファイバーの無限性は証明していない。

## 1．唯一の正本と exact-source receipt

| 項目 | GitHub MCPで確認した結果 |
|---|---|
| 定理PR | [#2811](https://github.com/itakura-hidetoshi/KuuOS/pull/2811) — MERGED |
| 最終exact-source HEAD | `661cee6a92152f64d09ab8a72e6373f3db9cba6c` |
| CI test-merge checkout SHA | `8a38ef1efcc072d478e19e372c31aa1ab16fc79b` |
| source／CI／squash共通Git tree | `f5c5595b08e19261d74a615ad31247d8e0a5a8b8` |
| 定理squash＝マージ直後canonical main HEAD | `6ef7ccacce400f9ead9fadc5e92354c2c18397e7` |
| 最終exact-source CI | [#41191976426](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41191976426) — terminal SUCCESS |
| Strict Lean | **3767/3767 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 公理表示 | **新規25宣言**、依存は `propext`・`Classical.choice`・`Quot.sound` の標準3以内 |
| `sorryAx` / 変更Lean warning/error | **0 / 0/0** |
| 変更対象 | **append-onlyの新規Lean 2ファイル**、既存Lean修正なし、公開root107維持 |
| 固定 | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

GitHub MCPで最終source、実際のCI checkoutおよび定理squashのGit tree完全一致を確認した。PR #1558は検証専用のDraft／OPEN／未マージを保持。

## 2．k=1でGK4ALの被覆条件が実際に失敗する

[GK4AMNoncoverage.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AMNoncoverage.lean) はGK4AJの真正元F54経路 `V=B³;C;B⁶;C;B³` を再利用する。これは新たに導入した無型generatorではなく、もとの `LocalRotation`、依存型中間木、castをすべて持つ。実際の旧 `q_1` ファイバーに属し、旧四成分観測および第一行列が一致する。

GK4AKの2経路は `W_1(0)=C;B¹²;C` と `W_1(1)=B⁶;C²;B⁶`。GK4AHの**全第二整数2×2行列**の線形decoder

`L([[a,b],[c,e]])=4b+2e-2a-c`

は `L(W_1(0))=-184`、`L(V)=-88`、`L(W_1(1))=8` を返す。従って `V` の真正K_AI類は既存 `Fin(2)` 埋込像の外にあり、その行列も有限行列像の外にある。

Lean宣言：`nativeGK4AMMiddle_forget`、`nativeGK4AMMiddleFiberPoint`、`nativeGK4AMMiddle_decoder`、`nativeGK4AMMiddle_not_family`、`nativeGK4AMMiddle_matrix_not_range`、`nativeGK4AMFamilyCovers_one_false`、`nativeGK4AMPhysicalNorth_family_not_covers_one`。

結論：

```text
¬ nativeGK4ALFamilyCovers rot 1
```

実際のC60北側六角形にも特殊化。

## 3．すべての正のkに一様化

[GK4AMUniformNoncoverage.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AMUniformNoncoverage.lean) は真正LocalRotationの前後backtrack `B` と元cast `C` を用いて

```text
H = B³
P = B⁶
V_d = H ; C ; P^(2d+1) ; C ; H
k = d+1
```

を構成。旧GK4AF整数行列で `H=-I`、`P=I` だから、`V_d` の第一行列は `C²=[[1,2],[0,1]]`。元F54の実回転数と非可換四成分観測もGK4AKの `q_(d+1)` に一致する。

しかし第二行列で

```text
L(M_AH(V_d)) = -88 - 192d
L(M_AH(W_(d+1,j))) = 8 - 192*(d+1-j)
```

が成立。等しいなら `192j=96` を要求するため整数添字jには不可能。

従ってLeanは、単一k=1からさらに

```lean
theorem nativeGK4AMFamilyCovers_positive_false
    (k : Nat) (hk : 0 < k) :
    ¬ nativeGK4ALFamilyCovers rot k
```

および `nativeGK4AMPhysicalNorth_positive_family_noncoverage` を証明する。

これは**各正のkごとに、実際に到達したq_kファイバーに、既存k+1元の族に属さない点がある**という結論である。各 `q_k` はGK4AKにより異なる旧類であり、特定の `q_k` が無限集合であることは従わない。

## 4．GK4ALとの厳密な整合性

GK4ALの

```text
FamilyCovers(k) ↔ すべての実際の到達第二行列をGK4AK有限族で表せる
FamilyCovers(k) → Fin(k+1) ≃ Fiber(q_k)
```

は依然として**正しい条件付き定理**である。GK4AMはその仮定が `k>0` で満たされないと証明するので、条件を削除した無条件有限正規形や `|Fiber(q_k)|=k+1` を主張できない。各FiberがCountableであるGK4ALの結論、および任意大有限下界もそのまま保持する。k=0でのFamilyCovers成立／不成立は本定理の射程外。

特に以下は引き続き**未証明**：単一固定旧類に無限個の相異なる真正K_AI類が到達すること、全ファイバー正確な濃度、任意整数2×2行列の到達性、`S→K_AI`の全域忠実性／非忠実性、元P92B存在商Q自身の結合律／左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、Gray圏、hyperdescent。観測一致を元のType値比較証拠や新しい3-cellと取り違えない。

## 5．形式検証とLean記法修正

初回CIは `congrArg` に残った未beta簡約のラムダ適用形が `rw` の目標に一致しない elaboration failure で失敗した。両GK4AMファイルで `change` による明示的な式展開を追加して修正。2回目は `nativeGK4AKOldValue (d+1)` と `nativeGK4AKOldValue (0+(d+1))` の `rfl` が定義上等しくないため失敗し、`simp only [Nat.zero_add]` に修正した。最終HEADで**全Lean 3767/3767 SUCCESS、warning/error 0/0、sorryAx0**。失敗した中間CIは成功証拠として使用しない。

証明はすべて既存の元F55 9／P92B 9／独立構造seam 14／拡張比較3の実Type値保存性を持つ第二行列に基づく。strict空中心、独立Kuuは一presentation、root107維持、Gray非再導入。

© 2026 板倉英俊 / Hidetoshi Itakura。Apache-2.0。
