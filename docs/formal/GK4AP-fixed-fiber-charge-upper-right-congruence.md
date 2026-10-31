# F112-P94D3GK4AP — 固定旧類ごとの第二行列の法4剰余とΓ₁(4)内部の到達障害

**2026年10月31日 JST／真正元F54型付きsourceに関するLean4証明・canonical main。**

GK4AOでは、真正GK4AH第二整数行列が必ず det=1、対角成分1 mod4、左下成分0 mod4を満たすことを証明した。GK4APではそれを強め、第二行列の右上成分を**旧GK4ADのchargeとbackwardCountに結び付ける**。したがって旧GK4AG観測類qを固定すると、任意の到達第二行列に課される法4剰余が固定される。さらに、Γ₁(4)には属するが同じqファイバーで到達しない具体的行列を、**任意のqに対し構成**した。元Q圏公理や新規Type値3-cellは仮定していない。

## 1．GitHub MCP exact-source証拠

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#2817](https://github.com/itakura-hidetoshi/KuuOS/pull/2817) — MERGED |
| final exact-source HEAD | `7431559538875af41f332230d7796181601bf012` |
| CI test-merge checkout SHA | `7b5634cc4cdeaff2e75bf551208fa4cd81eb73db` |
| source／CI／squash共通Git tree | `8d89572c86d281eba3ac068c2b1de7d2abcaca31` |
| 定理squash・統合直後main HEAD | `13363c70ea953a18dc0acaa5d4a138090990f576` |
| 最終CI | [#41195563521](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41195563521) — terminal SUCCESS |
| Strict Lean | **3772/3772 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 新規公理表示 | **25宣言**、標準 `propext`・`Classical.choice`・`Quot.sound` 以内 |
| `sorryAx`／変更Lean warning/error | **0／0/0** |
| 変更ファイル | append-only新規Lean 2ファイル、既存Lean変更0、公開root107維持 |
| 固定環境 | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft／OPEN／未マージ |

## 2．旧GK4ADと第二GK4AHの間の新しいcompatibility

[GK4APLinkedObserverResidue.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4APLinkedObserverResidue.lean) は、元Type値F54経路rについて

```text
charge_AD(r)        : ℤ
backwardCount_AD(r) : ℕ
M_AH(r)             : Mat₂×₂(ℤ)
upperRight(M_AH(r)) = charge_AD(r) + (backwardCount_AD(r):ℤ) + 4*t
```

となる整数tの存在を証明。右上成分の合同関係は

```text
b(M_AH(r)) ≡ charge_AD(r) + backwardCount_AD(r) (mod 4)
```

に相当する。これは、**元GK4ADの非可換ordered moment等を捨てて元観測類を同一視する操作ではない**。GK4APの述語 `nativeGK4APLinked` は、GK4AOの**全てのΓ₁(4)必要条件を保持**したまま、この追加の右上成分条件を課す。

証明では、真正F54の三つの生成子（元の二Nat cast `C=[[1,1],[0,1]]`、実forward `F=[[1,-1],[0,1]]`、実backward `R4=[[1,0],[4,1]]`）とゼロ鎖をそれぞれ検査。`nativeGK4APLinked_mul` は真正非可換 `nativeGK4ADCombine` と `nativeGK4AHMul` に対して保存されることを、GK4AOの対角成分 `1+4u` の整数証人に基づいて直接証明する。元RotationEdge・中間木RotationChain・DepthRotationRoute全5構成子から再帰して、元F55 9／元P92B 9／独立構造seam 14／拡張比較3の**既存Type値soundness**を通じて元Qと独立Sに**別々に降下**。さらに真正K_AIの全ての元へ移す。元Q自身の未証明結合律・単位律は使用しない。

## 3．同一旧類qを固定すると右上成分剰余も固定される

実際の旧`K_AG`類qの旧GK4AD成分から

```text
ρ(q) = charge_AD(q) + (backwardCount_AD(q):ℤ)
Γ₁(4)^(q) = {M ∈ Γ₁(4) | ∃t∈ℤ, M.upperRight = ρ(q)+4*t}
```

と定義する。真の従属型

```text
Fiber(q) = {z : K_AI(first,last) // U_AI,AG(z)=q}
```

に対して、新たに以下をLeanで証明。

```text
AttainedMatrix(q) ⊆ Γ₁(4)^(q) ⊆ Γ₁(4)
∀x y : Fiber(q), ∃t : ℤ,
  M_AH(x).upperRight = M_AH(y).upperRight + 4*t
```

宣言：`nativeGK4APFiber_sound`、`nativeGK4APAttained_subset_slice`、`nativeGK4APSameFiber_upper_residue`。これは**同じ旧観測類qという文脈でのみ**共通剰余を結論する。異なるqの右上成分に共通の剰余を要求しない。

## 4．Γ₁(4)内部でも、任意のqに必ず存在する到達不能行列

[GK4APFixedFiberArithmeticSlice.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4APFixedFiberArithmeticSlice.lean) において、任意の旧qごとに次を定義。

```text
N(q) = [[1, ρ(q)+1],[0,1]]
det(N(q)) = 1
N(q) ∈ Γ₁(4)
```

しかし仮に`N(q)`が`Fiber(q)`に到達すれば、

```text
ρ(q)+1 = ρ(q)+4*t
```

となり、整数tに対して不可能。従って

```text
N(q) ∉ Γ₁(4)^(q)
N(q) ∉ AttainedMatrix(q)
Γ₁(4)^(q) ⊊ Γ₁(4)    （すべてのqで成立）
```

を証明した。前段GK4AOで用いた行列`[[1,0],[1,1]]`はΓ₁(4)の外にある到達不能例だった。GK4APの新しい`N(q)`は**Γ₁(4)の内部**にあり、固定ファイバー文脈を考慮すると、なお到達不能であるという、より強い障害である。

`nativeGK4APRestrictedFiberEmbedding` と `nativeGK4APRestrictedAttainedEquiv` によって、真正Fiberはそのq依存算術sliceの実際の到達部分集合と正確にEquiv。ただしslice全体への全射や完全正規形は主張しない。

## 5．初回Lean失敗の構造的理由と修正

初回CIで検出されたのは**2箇所のelaboration/tactic mismatch**。
- 非可換積の整数恒等式で、`nativeGK4APOldUpperResidue`を展開せずに`ring`を適用し、整数chargeとNat backwardCountへの変換が見えず未解決になった。証明の数学的仮定は変えず、`simp only [nativeGK4APOldUpperResidue] at htu htv`で必要な等式だけ明示した。
- 元Fiber比較で`congrArg`後に残った `(fun v => v.1.2)(...)`と直接の射影`(...).1.2`が`rw`の構文照合で一致しなかったため、`change`により元GK4AIの依存型署名どおり明示的にβ展開した。

修正版最終sourceのCI #41195563521で **3772/3772 SUCCESS／Governance 5/5 SUCCESS／公理標準3以内／sorryAx0／変更警告・エラー0/0** を確認。失敗した中間CIを成功証拠として採用しない。

## 6．GK4AQ候補と未証明境界

GK4APは、GK4ANの各`q_k`内の`Fin(2k+1)`下界、GK4AL全ファイバー可算性、GK4AM全正数kの有限族非網羅性、GK4AOのΓ₁(4)必要条件をいずれも保持する。

引き続き未証明：**一つの固定旧qファイバーの無限性**、Γ₁(4)^(q)全域到達・完全値域分類、`S→K_AI`全域忠実性／非忠実性、元P92B商Q自身の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、Gray圏、hyperdescent。観測値の一致から元Type値3-cellを捏造しない。

次段階は、固定qを保ったまま第二行列にさらに独立な非可換不変量を課せるか、あるいは現在のΓ₁(4)^(q)の中に無限個の実到達値が存在するかを研究する。

© 2026 板倉英俊 / Hidetoshi Itakura。Apache-2.0。
