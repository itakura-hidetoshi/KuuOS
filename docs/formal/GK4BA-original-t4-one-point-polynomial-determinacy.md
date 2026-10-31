# F112-P94D3GK4BA — 真正F54型付き経路の一点多項式決定性

2026-11-01 JST。**canonical main の形式定理としてMERGED**。参照する正本は `itakura-hidetoshi/KuuOS` の `main`、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

## 1. 研究結果と正確な主張

以前の GK4AV・GK4AW は真正F54依存型経路 `r` の非可換多項式行列 `P_r(X) ∈ Mat₂(ℤ[X])` を構成し、`det P_r(X)=1` と次数上界を証明した。GK4AX は `N>max(β(u),β(v))` 個の相異なる整数評価での一致から多項式一致を示していた。

GK4AY/GK4AZ では、元の `C=[[1,1],[0,1]]`、`F=C⁻¹`、`R(4)=[[1,0],[4,1]]` に対する整数格子上の二つのせん断変換 `U_n(x,y)=(x+2ny,y)` と `L_n(x,y)=(x,y+2nx)` を使い、mathlibのping-pong補題から **`ℤ * ℤ ↪ Perm(ℤ²)`** をLean4で形式化した。

GK4BAではそれを**実際の元F54の完全依存型構成子へ輸送**した。元の同じ型付き始点・終点の経路 `u,v` について、

```text
P_u(4) = P_v(4)   ↔   P_u(X) = P_v(X)
```

を証明。特に元の旧AH行列の一致のみで多項式行列全体が一致する。

```text
M_AH(u) = M_AH(v)  ⇒  P_u(X) = P_v(X).
```

元P92B存在商 `Q` と、**別の独立構造比較商 `S`** に対しても、それぞれ既存の真正商降下に基づく独立の同じ定理を形式化した。

したがって、**旧AF・旧AHの二つの行列評価は一致するが全多項式行列が異なる真正F54型付き経路の組は存在しない**。過去の「有限二評価では失われる多項式履歴」という研究候補は成立しないと確定した。

この定理は「多項式不変量の一致」に関するもの。元の `DepthRotationRoute` Type値経路の等式や、F55/P92Bの元Type値 3-cell 証拠を新たに構成して**いない**。

## 2. Lean定理の正本ファイル

- [GK4BA OriginalWord](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAOriginalWord.lean): 元`RotationEdge`正逆、元`RotationChain`、`castDepths`・`trans`・左右文脈を含む元`DepthRotationRoute`の全5構成子から、GK4AZと**同じ** `ℤ*ℤ` 自由積語 `gk4baWord` を作る。整数語作用への忠実性。
- [GK4BA PolyCyclic](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAPolyCyclic.lean): `ℤ[X]^2` の上下多項式せん断の実置換と整数パラメータによる2つの群準同型。下側の加法証明を独立補題 `nativeGK4BAPolyLowerShear_add` へ分離。
- [GK4BA PolyShears](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAPolyShears.lean): 二つの群準同型から元自由積の多項式作用を構成し、旧生成子 `C,F,R(X)` と単位行列との一致を証明。
- [GK4BA PolynomialWordAction](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAPolynomialWordAction.lean): 元F54経路・鎖・全Type値構成子の帰納法により、自由積語の多項式作用と元GK4AV行列`P_r(X)`の作用が一致する。したがって同じ自由積語は同じ多項式行列を与える。
- [GK4BA IntegerWordAction](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAIntegerWordAction.lean): 元`P_r(4)`の整数行列作用とGK4AZ自由積作用の可換性。偶数第一座標の格子上の作用一致を整数格子全体へ引き上げる加法性。
- [GK4BA OnePointDeterminacy](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAOnePointDeterminacy.lean): 真正F54型付き経路・原P92B商Q・独立Sへの一点決定性、および二評価衝突不存在。

## 3. 証明の構造（新しい公理なし）

```text
P_u(4) = P_v(4)
      ↓  元F54全構成子の整数作用可換性
free-product words act equally on (2x,y)
      ↓  整数線形性、2倍を使うキャンセル
free-product words act equally on all ℤ²
      ↓  GK4AZのLean4 ping-pong単射
w(u) = w(v) in ℤ*ℤ
      ↓  多項式作用の元F54全帰納法
P_u(X) = P_v(X)
```

同じType値比較は元のF55全9、元P92B全9、独立構造seam全14、拡張比較3を含めて既存の証明を保持。数学的に異なる商`Q`, `S`, `K_AI`を同一視しない。元`Q`自身の未証明結合律・単位律は使わない。

## 4. exact-source CI と正本マージ

| 成果 | source HEAD | Strict Lean | 最終結果 |
|---|---|---|---|
| [PR #2840](https://github.com/itakura-hidetoshi/KuuOS/pull/2840) | `b0c480e3da157a04cb8af9eefeed8d7fac788fac` | [#41250464410](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41250464410) 3793/3793 SUCCESS | main squash `435e6282e492724df7d851ff1bf3a40d4a4f1621` |
| [PR #2838](https://github.com/itakura-hidetoshi/KuuOS/pull/2838) | `6cf46a73839f7ad9c71beba4386480d41ffc11c3` | [#41250474736](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41250474736) 3795/3795 SUCCESS | squash `fc9c8e140175a737c3596a69c9b074b76a1a9d5b` **作業ブランチへ** |
| [PR #2843](https://github.com/itakura-hidetoshi/KuuOS/pull/2843) | `5e1b355e5a417c554ba607b1b819aa66778cabde` | [#41252864048](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41252864048) 3795/3795 SUCCESS | **canonical main squash** `c4e20c3f2676dc8033010cfa024678b345649a38` |

#2840のsource/test-merge treeは `70bf56ef392bed8b138c97e76017835e564b3171` で一致。#2838のsource/test-merge treeおよび#2843のsource/test-merge treeは**全て** `b3e1ed4d2b0f84d79ffba05df0e608603caab001` で一致する。

#2838は当時のbaseが `formal/f112-p94d3gk4ba-polynomial-stage` に設定されていたため、一度その作業ブランチへマージされた。そのままcanonical `main`のマージと誤認せず、まったく同じLean blobの整数経路作用と一点決定性を現行`main`へ新規追加した **#2843** で改めてexact-head検証・squashマージした。

最終PR #2843はStrict Lean、独立Kuu、workflow integrity、Governance terminalすべてSUCCESS。元変更Leanの警告・エラー0/0、全新規`#print axioms`標準`propext`/`Classical.choice`/`Quot.sound`以内、`sorryAx`ゼロ。公開root107と固定Lean/mathlibを維持。

## 5. 過去のCI失敗とLean4上の学習事項

初期CIでは各一体型のLean証明がrunner停止（exit143）となり、完了したエラーメッセージを返さなかった。最小分離後、下側の多項式せん断群準同型で `(kernel) deterministic timeout` を検出。多項式正規化と`Equiv.ext`のdefinitional equality展開を分離し、`nativeGK4BAPolyLowerShear_add` を明示して群準同型証明へ参照する構造に修正。既存依存ファイルの書換え・新規の公理・`sorry`による埋め合わせは行わない。

最終実装では元の依存型署名、古い証明コンストラクタの全体、固定mathlib APIを確認し、変更Leanファイル全文がexact-head Strict Leanに成功した。

## 6. 次の研究フロンティア

**GK4BB（未証明）**：既存二次kernel `K_AI` の観測値には元の旧AH行列が成分として含まれる。GK4BAの一点決定性により、`P_r(X)` 全族が `K_AI` のkernel商へ**代表元に依存せず降下することが数学的に従う**。`NativeGK4SKernelClasses (nativeGK4AIP92Family ...)` での明示的 `Quotient.lift`、元Q/Sとの可換性、評価4の厳密回収、代表元独立性と一意性をLean4で形式化する。これは `K_AI` に追加で元Type値3-cellを導入することではない。

未証明を維持：固定単一旧類ファイバー無限性、算術slice全域到達、元Q結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、hyperdescent。

append-only／tighten-only／overwrite-forbidden／same-root107、strict空中心・独立Kuu一presentation・Gray再導入なし。保護PR #1558はDraft・OPEN・未マージ。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
