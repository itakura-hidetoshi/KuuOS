# F112-P94D3GK4AQ — 真正第二行列の左下成分法16と旧q依存の厳格算術slice

**2026-10-31 JST／canonical Lean4正本の証明・exact-source CI receipt。**

GK4AOでは第二整数行列の行列式1・対角1 mod4・左下0 mod4、GK4APでは旧charge+backwardCountが右上mod4を決めることを証明した。GK4AQは既存の条件を**一切弱めず**、本物の元F54 Type値経路における**左下成分のmod16剰余が旧backwardCountから決定される**という、さらに強いcompatibilityを証明した。元Q自身の未証明圏公理・新Type値3-cell・Gray圏は使用しない。

## 1．正本・GitHub MCPによるexact-source receipt

| 項目 | 確定結果 |
|---|---|
| 定理PR | [#2819](https://github.com/itakura-hidetoshi/KuuOS/pull/2819) — MERGED |
| final exact-source HEAD | `916381bd659e8fdf2a8b3ab951c5e1a33b8e8eb6` |
| CI test-merge checkout SHA | `7cd2220d26109490c52f7b7be663e8916959a194` |
| source／CI／定理squash共通Git tree | `6a561b27089c7f06260d4e1aa63fbc4c2668b7da` |
| 定理squash・統合直後main HEAD | `3297bbc78b4cc7309505bb43dacf800121493967` |
| CI | [#41197378209](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41197378209) — terminal SUCCESS |
| Strict Lean | **3774/3774 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 公理表示 | **新規27宣言**、`propext`、`Classical.choice`、`Quot.sound`の標準3以内 |
| `sorryAx`／変更Lean warning/error | **0／0/0** |
| 変更対象 | append-only新規Lean2ファイル、既存Leanの上書きなし、公開root107維持 |
| 固定環境 | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft／OPEN／未マージ |

## 2．真正F54の非可換履歴から下左mod16を証明

[GK4AQLowerLeftResidue.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AQLowerLeftResidue.lean) は、元GK4ADのcharge・backwardCount・orderedMomentを持つType値観測 `v` と、元GK4AHの完全2×2整数行列 `M` の間に、次の条件を定義した。

```text
AQLowerLinked(v,M) :=
  APLinked(v,M) ∧
  ∃t:ℤ, M.lowerLeft = 4*(v.backwardCount:ℤ) + 16*t
```

`APLinked`はGK4AO `Γ₁(4)`全制約に加えて `M.upperRight ≡ v.charge+v.backwardCount (mod4)` を保持するので、GK4AQは**厳密な追加制約**である。

真正F54生成子は二Nat cast `C=[[1,1],[0,1]]`、forward `F=[[1,-1],[0,1]]`、実LocalRotation後退 `R4=[[1,0],[4,1]]`。同一sourceに存在する元GK4AD非可換結合 `nativeGK4ADCombine` と真のGK4AH行列積について、旧後退回数の加法性を使う。具体的に、両行列の対角 `B11=1+4a`, `A22=1+4d` と下左 `A21=4β_A+16u`, `B21=4β_B+16v` より、

```text
(AB)21 = A21*B11 + A22*B21
       = 4*(β_A+β_B) + 16*(整数)
```

をLeanの整数環等式で証明。これが `nativeGK4AQLowerLinked_mul`。真正RotationEdge・中間F45木RotationChain・DepthRotationRoute全5構成子（chain/cast/trans/left/right contexts）まで帰納して `nativeGK4AQRoute_sound` を得る。

GK4AD/GK4AHがすでに証明した元F55全9、元P92B全9、独立構造seam全14、拡張比較3の**実Type値比較保存性**を継承して、元P92B存在商Qと独立Sへの別個の降下、真正第二商K_AI、任意の元F45依存型Hom・固定旧類qの`Fiber(q)`への伝播を証明。`nativeGK4AQP92_sound`、`nativeGK4AQStructural_sound`、`nativeGK4AQKernel_sound`、`nativeGK4AQFiber_sound` がその正本宣言である。観測値等式から存在しないType-cellを作っていない。

## 3．固定旧類qでの新しい厳密な算術境界

真の旧K_AG類qのGK4AD観測から

```text
ρ(q) = charge(q)+backwardCount(q)
β(q) = backwardCount(q)
Γ₁(4)^(q) = {M ∈ Γ₁(4) | M12≡ρ(q) (mod4)}
Γ₁(4)^(q,16) = {M∈Γ₁(4)^(q) | M21≡4β(q) (mod16)}
```

と置く。GK4AQにより、**任意のq**について

```text
AttainedMatrix(q) ⊆ Γ₁(4)^(q,16) ⊆ Γ₁(4)^(q) ⊊ Γ₁(4)
∀ x y : Fiber(q), ∃t:ℤ,
    M_AH(x).lowerLeft = M_AH(y).lowerLeft + 16*t
```

を証明した。これは同一qファイバーの真正像に関する局所命題である。異なる旧類にこの剰余の一致を要求しない。

## 4．従来GK4AP q-sliceの内部でも到達不能な行列

[GK4AQStrictLowerSlice.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AQStrictLowerSlice.lean) は任意のqに対し、明示的整数行列

```text
N(q) =
  [[1, ρ(q)],
   [4*(β(q)+1), 1+4*(β(q)+1)*ρ(q)]]
```

を構成する。`det N(q)=1`、対角成分`1 mod4`、左下`0 mod4`、右上`ρ(q) mod4`なので**以前のGK4AP `Γ₁(4)^(q)`には属する**。しかし

```text
N(q)21=4*(β(q)+1)
```

は新条件`4β(q)+16t`を満たせない。従って

```text
Γ₁(4)^(q,16) ⊊ Γ₁(4)^(q)
N(q) ∉ Γ₁(4)^(q,16)
N(q) ∉ AttainedMatrix(q)
```

が全qで証明された。単に`Γ₁(4)`にないという前段GK4AO型の反例より強い。真正`Fiber(q)`から新しい厳格算術sliceへの単射と、**実到達像に限定した**同値もLeanで構成（`nativeGK4AQRestrictedFiberEmbedding`、`nativeGK4AQRestrictedAttainedEquiv`）。新slice全体への全射・完全正規形は主張しない。

## 5．Lean elaboration修正と証明境界

初回CIでは、上記`N(q)`の右下成分の`4*((β+1)*ρ)`と`(4*(β+1))*ρ`について、`simp`後に括弧位置の異なる同一整数積が残った。**数論上の矛盾ではなく、乗法結合律の正規化不足**。当該新規Leanファイルの該当1行に`<;> ring`を追加し、全変更Leanソースとimportsを確認した。最終CIで**3774/3774 SUCCESS／Governance 5/5 SUCCESS／新規27宣言標準3公理以内／sorryAx0／変更Lean warning/error0/0**。中間失敗CIを成功証拠にしない。

GK4AQはGK4ALの任意ファイバー可算性、GK4ANの`Fin(2k+1) ↪ Fiber(q_k)`、GK4AMの正数kでの`¬FamilyCovers(k)`、GK4AO/GK4APの全算術制約を保持する。

未証明：**一つの固定旧qファイバーの無限性**、新`Γ₁(4)^(q,16)`全体の到達性、全整数行列の実現、S→K_AI全域忠実性／残余非忠実性、元P92B商Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、Gray、hyperdescent。

**次候補GK4AR（未証明）**：旧orderedMomentを用いて対角成分の法16等をさらに絞れるか、固定q内の無限族またはその有限性障害を別個に研究する。

© 2026 板倉英俊 / Hidetoshi Itakura。Apache-2.0。
