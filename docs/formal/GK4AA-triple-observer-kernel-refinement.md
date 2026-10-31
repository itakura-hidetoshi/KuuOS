# F112-P94D3GK4AA — 真正F54三成分観測・第二kernel圏・忘却関手の可算無限ファイバー

**2026-10-31 JST** — Repository `itakura-hidetoshi/KuuOS`、唯一の定理正本は canonical `main`。

- **定理PR [#2787](https://github.com/itakura-hidetoshi/KuuOS/pull/2787) — MERGED**
- 定理squash SHA `78a4ea2ea9fff4b7b04a0b7076e39e9898d0ffe3`（定理マージ直後のmain HEADと完全一致）
- 最終exact-source PR HEAD `b5096469f96d371df4e52bf7124f9cf9eb5b6ac6`
- [Strict Lean / Governance exact-source CI #41175744716](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41175744716) **SUCCESS**：Strict Lean **3740/3740**、Governance **5/5**、新規Lean**4ファイル・72個の`#print axioms`対象**、公理依存は `propext` / `Classical.choice` / `Quot.sound` 以内、`sorryAx` **0**、変更Lean warning/error **0/0**。
- 検証対象：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

## 正本構造：Q、S、K_AA、K_Xは別々の商

元F54の全依存型経路`DepthRotationRoute`と元P92B Type値3-cell証明は変更しない。

- **Q**：元P92B比較証拠の存在商。結合律・左右単位は依然未証明であり、**QをCategoryにしない**。
- **S**：独立F54構造比較商。元の比較に加えて全14個の構造seamを保持する、既存GK4Iの真正圏。
- **K_AA**：元Qを**三成分観測の等式kernel**でさらに商にした、別個のGK4S第二商。今回、真正Mathlib Categoryを構成。
- **K_X**：GK4Yで定義済みの `(Bool,Int)` 観測kernel第二商。K_AAからの忘却は**真正の別圏間関手**。

`Q→S`、`S→K_AA`、`K_AA→K_X` の比較方向・authorityを守る。観測値の等号から元P92B Type値3-cellを決して生成しない。

## I. 真正三成分観測と全seam保存

[三成分観測 Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAThreeComponentObserver.lean)：

```text
NativeGK4AAValue := (Bool × Int) × Nat

O_AA(r) := ((nativeGK4GRawGrade(r), r.gk4wCastCharge),
             r.gk4zBackwardCount)
unit := ((true,0),0)
((b,c),k) ⋆ ((d,e),l) := ((b && d,c+e),k+l)
```

最初の二成分はGK4X、最後のNat値はGK4Zの**元F54 `RotationEdge.backward` 真正Type値証拠数**であり、単なる新規shadowではない。GK4Zの元F55全9・元P92B全9・F54構造seam全14・拡張構造比較全3構成子のsoundnessを継承して、別個の`Quotient.lift`によるQおよびSへの降下を証明。真正合成での加法則・Boolean積、左右文脈での観測不変、真の14-seamでの同値保存、実零経路の単位、Q→S可換性をLeanで検証。

## II. 真正第二kernelと比較関手

[真の商間比較 Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AATripleComparison.lean)：

- 真正seam保存から `nativeGK4AATripleComparison : S → K_AA` が各依存型Homで存在・全射。
- 同じ構造Hom上で比較像が一致する必要十分条件は、**GK4X二成分観測値が一致、かつGK4Z後ろ向き回転数が一致**すること。
- 各Homの比較写像が単射となる必要十分条件は、同じHom上の三成分観測自体の単射性。
- 別の一対象値圏 `NativeGK4AAValuePoint` への構造圏関手を構築し、旧GK4X値圏への厳密な射影因子化を証明。

[第二kernel圏 Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAKernelCategory.lean)：

- `NativeGK4AAEnhancedKernelStage` の各Homは真の `K_AA` 第二商であり、元のQとは**違う型**。
- その結合律・左右単位は真正到達三成分観測とその結合的値域演算から証明。元Qの未証明圏公理を**一切利用しない**。
- `S→K_AA` Mathlib Functor（各Hom全射）と、`K_AA→NativeGK4AAValuePoint` Functor（各Hom単射）を形式化し、後者と前者の合成は実三成分構造観測と一致。

## III. 強化で識別できる真正balanced F54回転塔

GK4Zの実Type値経路 `R_0=B, R_(k+1)=C;R_k` は、元F54の本物の前後局所回転backtrackと実`castDepths`証拠だけから構成したもの。`k : Nat`ごとに

```text
rotationCount(R_k) = 2*(k+1)
castCharge(R_k) = -2
backwardCount(R_k) = k+1
O_X([R_k]_S) = (false,-2)
O_AA([R_k]_S) = ((false,-2),k+1)
```

したがって**相異なる全Nat添字**はK_AAで別の真正二段kernel商類へ写るが、旧K_Xへ射影すると**すべて同じ類**に写る。これにより旧GK4X観測の具体的な情報損失を三成分で解消したことを証明。

[真の忘却圏と可算無限ファイバー Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAKernelForgetful.lean)：

- `K_AA→K_X` は、元Qの同じ実証拠類から誘導される別個のMathlib Functor。対象・射において`S→K_AA→K_X`はGK4Yの既存`S→K_X`と厳密に一致。
- 任意の**実LocalRotationが証言された**F45自己Homについて、この忘却関手は非単射。
- 上記`R_0`の真の旧K_X類上に定義した`K_AA→K_X`のファイバーは **`Cardinal.aleph0`**。下界はNatからの実R_k二段目商類単射、上界はK_AAから**Countable `(Bool×Int)×Nat`値域**への真正単射。元D/E圏に一般のCountable仮定は不要。
- 真正C60北六角形 `northHexagonNativeLeftRotation` について、上記可算無限ファイバーと忘却非単射を無条件でLean証明。

## CI修正の構造理由

初回のexact-source CI #41175506675では、新規KernelForgetfulファイルの`nativeGK4AAForgetBackward_not_injective`内で`rot`を**証明本体だけ**から参照していたため、Leanのsection-variable自動束縛に含まれず、`Unknown identifier rot`、続いて北側例の型不一致が発生。エラー行以外も4ファイル全文、imports、元GK4X/GK4Y/GK4Zの依存シグネチャとpinned mathlibを確認し、定理文に`(rot : KuuNativeF45Tree.LocalRotation p before after)`を明示的に導入して修正。最終HEADで修正版Strict Lean 3740/3740とGovernance 5/5が成功し、エラー・sorryAxを除去した。前3ファイルは初回からコンパイル成功。

## 未証明の範囲と運用

**三成分観測による `S→K_AA` の全域忠実性／圏同値は未証明。** 今回の非忠実性は**別の忘却関手 `K_AA→K_X`**についての結果であり、両者を混同しない。

元P92B商Qの結合律・左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict n、hyperdescentは未証明として維持。strict空を中心に、独立Kuuは空の一presentation。Gray圏は再導入しない。append-only / tighten-only / same-root / overwrite-forbidden、公開root107を保持。保護PR #1558はDraft/OPEN/未マージのまま。

**次候補 GK4AB**：三成分をすべて一致させながら構造商Sで異なる真正Type値経路が存在するか（または追加条件下で単射か）を、元seamと実証拠履歴に照らして探索。比較の全域忠実性を仮定しない。
