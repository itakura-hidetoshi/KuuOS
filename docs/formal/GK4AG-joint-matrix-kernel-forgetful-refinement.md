# F112-P94D3GK4AG — 四成分・非可換行列の積観測と真正第二kernel商

**2026-10-31 JST**。唯一の定理正本は `itakura-hidetoshi/KuuOS` の canonical `main`。GK4AF以前の定理・表示・歴史を上書きせず、append-only／tighten-only／same-rootで追加した。

- **[定理PR #2799](https://github.com/itakura-hidetoshi/KuuOS/pull/2799) MERGED**。
- 最終定理exact-source HEAD：`735e9db16d3130a5df36431d073575393cbb5ff7`。
- 定理squash SHA＝マージ直後canonical main HEAD：`29832485498d1ded71a9cbd9eadf3cf07085ffa2`（GitHub MCPで完全一致）。
- [exact-source CI #41183798699](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41183798699) **Strict Lean 3754/3754 SUCCESS、Governance 5/5 SUCCESS**。新規Lean3ファイル、`#print axioms` **46宣言**。依存は標準 `propext`・`Classical.choice`・`Quot.sound` 以内、`sorryAx=0`、変更Leanファイルのwarning/error **0/0**。
- Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**。公開root 107、strict空中心、独立Kuuは空の一presentation、Gray圏非再導入、保護検証PR #1558 Draft／OPEN／未マージ。

## 1. 元F54からの積観測は真正な非可換値

[積観測と独立Q/S降下のLeanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGProductObservation.lean)：

```text
O_AG(r) = (O_AE(r), M(r))
NativeGK4AGValue := NativeGK4AEValue × NativeGK4AFMatrix
(u,A) ⋄ (v,B) := (nativeGK4AECombine u v, nativeGK4AFMul A B)
unit := (nativeGK4AEUnit, nativeGK4AFOne)
```

元GK4AEの真正四成分は `Bool × ((Int×Nat)×Int)` で、積は順序momentに交差項を含む。元GK4AFの整数2×2行列は、真正F54 `castDepths`・前方向`RotationEdge`・逆方向`RotationEdge`を、順序を保った行列積に写す。`nativeGK4AGCombine_assoc`・左右単位は二成分それぞれの**既証定理から直接**形式化し、値の可換化や行列のtrace/determinantへの圧縮を行わない。

元F54依存型 `DepthRotationRoute` の合成・左右文脈での観測を証明し、実際の元P92B証拠存在商 `Q` と独立構造比較商 `S` に **別個に**`nativeGK4AGP92`・`nativeGK4AGStructural`を構成。`Q→S`比較との可換性、元P92B合成の観測積保存、元独立S合成の観測積保存、元F54全14構造seamとの整合を証明した。

成分定理が保存する元Type値比較の範囲は、元F55全9構成子・元P92B全9構成子（真正assocNaturality含む）・独立構造seam全14・拡張構造比較全3。GK4AGはその正本証明を使うものであり、数値観測の一致から元P92BのType値3-cellを作らない。

## 2. 新しい真正第二kernel商 `K_AG`

[真正第二kernel圏とS比較関手のLeanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGKernelCategory.lean)：

```text
K_AG(first,last) :=
    Q(first,last) / (q ~ r iff O_AG(q) = O_AG(r))
```

`NativeGK4SKernelClasses (nativeGK4AGP92Family p D E)`として、元F54型付き境界にある真正**元P92B証拠存在商Qの第二商**を構成した。元Qそのものは圏公理が未証明なので、Qの結合律・単位律を仮定せず、GK4Sの**到達可能観測値 image の合成**を輸送し、値域の積の結合律・単位律から`Category (NativeGK4AGKernelStage ...)`を証明。

- `nativeGK4AGComparisonFunctor : S ⥤ K_AG` を元構造商SのMathlib圏から構成、各実型付きHomで **全射**。
- `nativeGK4AGKernelValueFunctor` を別の非可換積値圏へ構成し、各Homで **単射**。これは第二商のkernel定義から出る忠実性であり、`S→K_AG`全域の忠実性ではない。
- `nativeGK4AGComparison_eq_iff` はS比較で類が一致する必要十分条件を、真正元Sでの組観測一致に還元する。

## 3. 真正忘却関手 `K_AG→K_AE` と狭義の精密化

[元四成分商への忘却関手と反例のLeanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGForgetful.lean)。

新第二商 `K_AG` のクラスから、**行列観測だけ**を忘れて旧四成分商`K_AE`へ写す`nativeGK4AGForgetMatrixFunctor`を真正Mathlib関手として構成。元P92Bの同じ実証拠類を表現元として用い、全Homで全射、真正単位・合成を保存し、次の比較図式が全Homで可換と証明：

```text
     S  ─────F_AG────→  K_AG
      ╲                  │
       ╲ F_AE            │ U_AG,AE  (Hom-surjective)
        ╲                ▼
         └────────────→ K_AE
```

本物の元F54局所回転 `rot:LocalRotation p before after`、二Nat cast自己経路`C`、実前後方向backtrack`B`から、GK4AFで既証の真の依存型自己経路を再利用：

```text
u = C; B; B; C
v = B; C; C; B
O_AE(u) = O_AE(v) = (false,-2,2,-2)
M(u) = [[ 0,-1],[1,1]]
M(v) = [[-1,-1],[3,2]]
```

したがって：

```text
F_AG([u]_S) ≠ F_AG([v]_S)
U_AG,AE(F_AG([u]_S)) = U_AG,AE(F_AG([v]_S))
```

すなわち、真正`K_AG→K_AE`は **局所非忠実**で、真正C60北側六角形 `northHexagonNativeLeftRotation` でも無条件のHom非単射をLean4で証明。GK4AFが証明した`S→K_AE`の残余非忠実性を、この行列成分が具体的に修復して分離する。ただし残りすべての`S`非同値類が区別できるとまでは推論しない。

## 4. 厳密な権限境界と次段階

`S→K_AG` の全域忠実性は **未証明**。`nativeGK4AGComparison_injective_iff_joint` では、任意の固定型付きHomで

```text
Function.Injective (S → K_AG)
    ↔ Function.Injective (S → NativeGK4AGValue)
```

という局所必要十分条件だけを証明した。値域は観測の全値ではなく、実元F54から到達可能なimageである。元P92B `Q` の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentはすべて未証明として保持する。

**次候補GK4AH（未証明）**：同じ組観測 `(O_AE,M)` を持つが独立構造Sで異なる真の元F54型付き経路が存在するか、存在しないとするための限定的な忠実性条件を、非可換表現・局所文脈・比較証拠の差から独立に検査する。

## 5. Lean4修正履歴、exact-source receipt

初回source HEAD `b9d9dabb2ce3e34ce07a8cae0c0d7846a2477a30`・[CI #41183588516](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41183588516)では、最初の積観測Leanが成功する一方、二番目の`nativeGK4AGKernelValue_compose`で`rw [nativeGK4AGKernelCompose_class]`が失敗。原因は`Quotient.inductionOn₂`後のゴールが`⟦q⟧`と表示され、補題の`nativeGK4SKernelClass ... q`との表層書換対象をLeanが認識しなかったこと。数学的な等式の破綻ではない。

そのため、既存GK4AEの確定した商類合成の書き方に揃え、型付き境界と実観測familyを明示する

```lean
change nativeGK4AGKernelValue t₁ t₃
  (nativeGK4AGKernelCompose t₁ t₂ t₃
    (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q)
    (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₂ t₃ r)) =
  nativeGK4AGCombine
    (nativeGK4AGKernelValue t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q))
    (nativeGK4AGKernelValue t₂ t₃
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₂ t₃ r))
```

を追加してから`rw`を適用。同型の問題が潜む忘却関手側も同時に修正した。変更した3Leanファイル全文、imports、元F54/F55/P92B/構造seam依存署名とpinned mathlibを確認し、修正後exact-source `735e9db16d3130a5df36431d073575393cbb5ff7`・[CI #41183798699](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41183798699)では **Strict Lean 3754/3754 SUCCESS、Governance全5/5 SUCCESS**、`#print axioms` 46宣言が標準3公理以内、`sorryAx=0`、変更Lean warning/error 0/0。squashマージ後のmain HEADは`29832485498d1ded71a9cbd9eadf3cf07085ffa2`。

著作権 © 2026 板倉英俊 / Hidetoshi Itakura。元の研究体系・数学・証明・比較のauthorityは正本のLeanファイル、exact-head CI、Git SHAの順に置く。
