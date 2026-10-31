# F112-P94D3GK4AE — 真正四成分観測・非可換第二kernel圏・順序moment忘却の非忠実性

**2026-10-31 JST**。定理正本：`itakura-hidetoshi/KuuOS` の canonical `main`。

- **[定理PR #2795](https://github.com/itakura-hidetoshi/KuuOS/pull/2795) MERGED**
- 最終exact-source HEAD：`26ae50769b959e2d9b0a27af6196773f9d952deb`
- 定理squash SHA＝マージ直後canonical main HEAD：`1480dc47852cfe6a3224e0811e7dec1a377d01b3`（GitHub MCPで完全一致）。
- [exact-source CI #41181371095](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41181371095)：**Strict Lean 3749/3749 SUCCESS、Governance 5/5 SUCCESS**。新規Lean4ファイル・新規`#print axioms`69宣言。依存は標準`propext`、`Classical.choice`、`Quot.sound`以内。**sorryAx 0、変更Lean warning/error 0/0**。
- 固定Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107、strict空中心・独立Kuuは一presentation・Gray再導入なし。保護PR #1558 Draft/OPEN/未マージ。

## 1. 本来のF54 Type値証拠から四成分観測を構成

[四成分観測のLean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEFourObserver.lean)は、GK4ADの非可換順序付きmomentを用いて、真正元F54経路`r`に

~~~text
O_AE(r) =
  (grade(r), (castCharge(r), backwardCount(r), orderedMoment(r)))
NativeGK4AEValue = Bool × ((Int × Nat) × Int)
~~~

を定義。値域の積は、Bool.andとGK4ADの非可換Heisenberg型積である：

~~~text
(g,(c,b,m)) ⋄ (h,(d,e,n)) =
  (g && h, (c+d, b+e, m+n+c*e))
unit = (true,(0,0,0))
~~~

結合律・左右単位と、`O_AE`の真正原F54合成・元F45左右文脈に対する厳密な整合性をLeanで証明。元F55全9、P92B全9（本物のassociator自然性を含む）、構造seam全14、拡張構造比較全3についてGK4ADで証明済みの元Type値soundnessを利用し、`Q`元P92B証拠存在商と独立構造商`S`へ**別々に降下**。元`Q→S`可換性と本来の構造商合成に対する非可換積保存を証明する。元P92Bの存在商`Q`そのものに未証明の圏公理を追加しない。

## 2. 四成分から旧三成分への射影は定理であり仮定ではない

[元F54観測の整合・S→K_AE比較Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEComparison.lean)は、GK4ADで構成した元F54順序付き値の最初の2座標が、**本物の元GK4W castChargeとGK4Z backwardCountに一致**することを、元`RotationEdge`全方向・任意の中間木を持つ`RotationChain`・`DepthRotationRoute`全5構成子で帰納的に証明する。

~~~text
raw.gk4adValue.1 =
  (raw.gk4wCastCharge, raw.gk4zBackwardCount)
forgetMomentValue(O_AE(raw)) = O_AA(raw)
~~~

これは既存の別々に構成したQ/Sの商観測の一致を検証する橋であり、観測値だけで元のType値3-cellを生成する主張ではない。さらにGK4Tの実14 seam条件から真正`S→K_AE`比較を構成し、**比較がHom全射**であることと、「比較像の等号 iff 真正四成分観測値の等号」を証明。真正構造圏`S`から四成分値の一対象Mathlib圏への関手も実装。

## 3. 本物の第二P92B観測kernel圏 K_AE

[真正四成分第二kernel圏Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEKernelCategory.lean)は、元P92B証拠存在商`Q`を四成分観測値一致でさらに商にした**本物のGK4S第二商`K_AE`**を定義し、Mathlib Categoryの左右単位と結合律を、元`Q`の未証明の圏公理を一切使用せず、**到達四成分値の非可換結合律・単位律から**証明。真正`S→K_AE`比較はHomごとに全射。`K_AE→`四成分値のMathlib観測関手はHomごとに単射であり、到達像への忠実性を持つ。これは`S→K_AE`の忠実性を証明したことではない。

## 4. 新しい本物の忘却関手 K_AE→K_AA は非忠実

[真正第二商間の忘却Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEKernelForgetful.lean)は、上記の射影整合定理を使って`K_AE→K_AA`の**well-definedな商写像とMathlib関手**を構成。これはHomごとに全射で、構造商`S`からの両比較関手の正準三角形が可換になる。

GK4ADで作った実元F54型付き経路`C;B`（二Nat cast、前向き＋逆向きbacktrack）と`B;C`は、既存三成分`O_AA=((false,-1),1)`では等しいが、GK4ADの非可換`orderedMoment`がそれぞれ`0`と`-1`。したがって真正第二商`K_AE`では相異なるが、`K_AA`への像が一致する：

~~~text
[u]_(K_AE) ≠ [v]_(K_AE)
ForgetMoment([u]_(K_AE)) = ForgetMoment([v]_(K_AE))
~~~

よって**本物の`K_AE→K_AA`忘却関手は、真正F54局所回転を持つ任意の型付き自己Hom上で非忠実**。実際のC60北側六角形の`northHexagonNativeLeftRotation`でも無条件に成立。GK4ACの別の`K_AA→K_X`ファイバー`Nat≃Fiber`、GK4ADの別の`S→K_AA`非忠実性と整合するが、**`S→K_AE`全域忠実性は今回未証明**である。

## 5. CIのエラーとLean記法・依存関係の修正

初回 exact-source CI #41180654899 は、四成分比較の`Bool`射影に`Bool×Int`を取り出したLean型不一致と大文字・小文字不一致の公理表示名2か所で失敗。比較ファイルを修正した後の #41180893741 では、本物の第二商圏ソースが自動転記された未定義`nativeGK4AEQuadComparison`を参照していたため、実際の`nativeGK4AEComparison`に修正し、比較の単射性必要十分条件を追加。#41181122967 では、忘却関手の2か所で、商代表元が`⟦q⟧`表示のまま、`nativeGK4SKernelClass`を使う定理と`rw`が一致しなかった。そこで元のGK4AAの証明構造と対応させて`change`で型付き商代表元・元P92B四→三観測の定義を明示。これらは追加公理・観測の同一視ではなく、Lean elaborationとdefinitional equalityの修正。

最終exact-source HEADで4新規Leanファイルを全文・imports・依存シグネチャとともに検証し、Strict Lean 3749/3749とGovernance 5/5すべてSUCCESS、sorryAxなし、警告・エラー0。

## 6. 権限境界・次段階

元`Q`・独立構造商`S`・四成分第二商`K_AE`・三成分第二商`K_AA`・旧二成分第二商`K_X`は各々異なるpresentation。今回証明したのは`K_AE→K_AA`の非忠実性および`K_AE`の真正第二圏構成であり、`S→K_AE`の全域忠実性は**未解決**。元P92B`Q`の結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentも未証明。

**次候補GK4AF（未証明）**：同一四成分観測値を持つが異なる独立`S`類を生む、原F54のより高次の順序・文脈・反復履歴不変量の構成、または忠実性の必要十分条件を調べる。決して四成分だけで全局所構造を同一視しない。

著作権 © 2026 板倉英俊 / Hidetoshi Itakura。append-only、tighten-only、same-root、overwrite-forbidden、strict空中心、独立Kuu一presentation、Gray非再導入を保持。
