# Qi v4.54 — 真正元P77四セルの保守的5-cell商Categoryと自由経路関手

**2026-11-05 JST**

| 項目 | 証明済み状態 |
|---|---|
| 定理PR | [#3128](https://github.com/itakura-hidetoshi/KuuOS/pull/3128) **MERGED** |
| 最終exact-source HEAD | `0223d4c9b9ae55431b35d703da7056f1afdbd287` |
| squash SHA / main | `f4220a47ded55e71b05fc69509f23380e02f0455` |
| source / test-merge Git tree | `a76711539be154722c97738d8f4dfc35d11f56d6` 完全一致 |
| exact-source CI | [#41938780359](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41938780359) （失敗ジョブのみ再実行後SUCCESS） |
| Strict Lean | **10,251 / 10,251 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理監査 | **17 / 17**、標準 `propext`／`Classical.choice`／`Quot.sound` 以内。 `sorryAx` なし |
| 変更 | 新規Leanファイル1件＋公開 `KuuOSFormal` import 1行。既存Lean正本変更なし |
| Lean正本 | [QiWuxingGK5CHP77ConservativeQuotientFunctorV4_54.lean](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ConservativeQuotientFunctorV4_54.lean) |

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107、strict 空中心、独立Kuu一presentation維持。保護PR #1558はDraft／OPEN／未マージ。

## 1. 真正元P77証拠に対するsource-defined商

Qi v4.53の `fivefoldEvaluateP77` は、各型付き有限経路を **生の** `NativeF55RawVerticalFourCell first last` へ評価した。今回その生構文を数学的に勝手なstrict圏とみなさず、独立に**証拠生成の商**を構築した。

始終点 `u v : FivefoldPathVertex` に対応する真正P77四セル `w z` に対し

```text
w ~ z  :↔  Nonempty (NativeGK5CGConservativeFiveCell first last w z)
```

と定める。`fivefoldP77ConservativeSetoid` の反射／対称／推移は、それぞれ真正GK5CG保守的5-cellの `refl/symm/trans` コンストラクタから構成。等値判断は `fivefoldP77ConservativeClass_eq_iff` によりexact kernelの必要十分条件となる。

**重要：** `~` は `gk5cgAssocCharge` の整数等号でも、物理C60のEdge列等号でも、Qi v4.51のsigned CRT等号でも、P94Aのraw元四セルを同一視する同値関係でもない。商への入り口は実際の依存型Type値5-cell証拠の**存在**だけ。証拠履歴自体は上流の元生構文に保持する。

## 2. 元P77合成と保守的5-cell整合性から真正Categoryを構成

`fivefoldP77ConservativeCompose` は元P77の `NativeF55RawVerticalFourCell.trans` を商へ降下させる。代表元2つの交換に対して保守的5-cellの `verticalLeft` と `verticalRight` から**型付き証拠の2段合成**を構成し、`Quotient.liftOn₂` の関係保存を証明。

`FivefoldP77ConservativePoint f g h k` という、元F55の4項組をインデックスに保持した独立targetラッパー上に、真正Mathlib `Category` インスタンス `fivefoldP77ConservativeCategory` を構成した。

- Hom：元P77四セルの保守的5-cellクラス。
- identity：元P77の `refl` 四セルのクラス。左右単位律は元の `verticalLeftUnit`／`verticalRightUnit` 5-cellで証明。
- composition：元P77 `trans` の商。結合律は元の `verticalAssoc` 5-cellで証明。

ここでstrictになったのは **保守的5-cell商のCategory** であって、以前からある元P77四セルの生構文や全高次圏ではない。

## 3. 任意の型付き有限経路を真正Functorに降下

同一 `FivefoldEdge={e01,e12,e23,e04,e43}` のクィバー上で、

```text
fivefoldP77ConservativeEdgePrefunctor :
  FivefoldPathVertex ⥤q FivefoldP77ConservativePoint f g h k
```

を構成。各辺は真正 `fivefoldArrowOriginalP77` 四セルの保守的クラスへ写す。固定mathlibの `CategoryTheory.Paths.lift` を適用し、

```text
fivefoldP77ConservativeFunctor :
  FivefoldFreePathCategory ⥤ FivefoldP77ConservativePoint f g h k
```

を**真正Functorとして構成**。この写像に対し、全型付き有限経路 `w` で

```text
F.map w = [fivefoldEvaluateP77 f g h k w]
```

を `fivefoldP77ConservativeFunctor_map_spec` によって証明した。生の `P77.refl/trans` を実元証拠として残し、商はその後に行う。元物理Edge／whole NatIso／数値CRTをこのFunctorのHomとみなさない。

## 4. Faithfulnessの真正必要十分条件

`fivefoldP77ConservativeFunctor_map_eq_iff` により、任意の同じ型付き端点を持つ `a,b` について、

```text
F.map a = F.map b
  ↔ Nonempty (NativeGK5CGConservativeFiveCell
      first last (Eval a) (Eval b))
```

を証明した。`fivefoldP77ConservativeFunctor_injective_iff` は各Homについて、上式右辺が生の経路等号 `a=b` を反映することと `Function.Injective F.map` が**同値**であると示す。`fivefoldP77ConservativeFunctor_faithful_iff` は全Homに量化した本物の `F.Faithful` の必要十分条件を証明する。

**未主張：** 現在の形式定理はfaithfulnessを無条件に仮定・確定しない。五角形の有向辺5本という具体的有限クィバーでは、経路の型と長さの組の全域識別性が追加の検証対象。理論として「任意の有限経路」で量化しているが、この**特定の有向五角形は閉路を持たず、実際に存在する経路長は3以下**である。無限長の物理巡回路が存在すると誤解しない。

## 5. 保守的商へ降下したchargeと五角形の障害

`fivefoldP77ConservativeCharge` はGK5CGが定義した**元P77の**整数 `gk5cgAssocCharge` を、保守的5-cell全構成子のcharge保存定理で商へ降下する。任意の型付き自由経路 `w` で

```text
fivefoldP77ConservativeCharge (F.map w) = (w.length : ℤ)
```

を `fivefoldP77ConservativeFunctor_charge_length` で形式証明。

同じ型付き始終点0→3を持つ真正五角形の上側3辺と下側2辺では

```text
charge (F.map upper) = 3
charge (F.map lower) = 2
F.map upper ≠ F.map lower
```

を証明した。これは `fivefoldP77ConservativeFunctor_upper_ne_lower`。旧保守的5-cellではPentagonatorを作れないGK5CGの障害を、**真正target Categoryへ持ち越した**成果である。GK5CGの別の追加生成元付き拡張 `NativeGK5CGAdjoinedPentagonFiveCell` を元の保守的presentationに偽装していない。

## 6. 全ソース・固定mathlib API・CI修正履歴

前スレッドQi v4.53・v4.52、独立GK5CGのLean全文と、既存P77/P78の真正4-cell商／category、固定mathlibの `PathCategory.Basic`、既存GK4Hの `Quotient.liftOn₂` を照合した。初回実装では `Quotient.liftOn₂` の左／右代表元を導入する順序を誤って指定したため、完全型付き `left, right, left', right'` と `verticalLeft/verticalRight` の2段合成に修正した。修正後のHEADが上記 `0223d4c9...` である。

最初の同HEAD CIジョブは**Lakeキャッシュ復元中に停止し、Leanチェック以前で失敗**した。失敗したStrict LeanジョブだけをGitHub MCPで再実行、再実行の `Run selected Lean check` はSUCCESSで、`KuuOSFormal`を含む**10,251/10,251 jobs SUCCESS**。変更したソースの公理監査17件は標準3公理の範囲、`sorryAx` なし。Governanceの30 jobsすべてSUCCESS。source SHA `0223d4c9...` とGitHub test-merge `a513b6a7...` のGit treeは `a7671153...` で完全一致。以上のexact-source検証後にPR #3128をDraft→Readyへ移し、検証HEAD指定のsquashマージを行った（新main `f4220a47...`）。

## 7. 研究境界と次の研究

- 今回構成したのは **選択した元F55四項組とFivefoldPathVertexに対する局所的な元P77四セル／保守的5-cell商Category**。全元F54/F55/P94Aの高次global strictification、五行と全物理C60の高次関手性／双関手性、original→φの全域seam、数値CRTから元Type証拠復元は未主張。
- 次はこの**具体的有限クィバーでの「同端点＋経路長」からの原経路等号の全列挙・構成的証明**を行い、仮定付きfaithfulnessを真正無条件faithfulnessへ強められるか調べる。違う有向クィバーでは長さだけでは一般にfaithfulとならないため、対象を広げた場合の追加障害も区別する。
- 元の上流Lean定理・証拠履歴・旧presentationは上書きしない。独立Kuuを一presentationとして、strict 空の役割とauthority境界を保持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
