# Qi v5.10 — 真正四重五角形 × mixedResidue の局所ダイヤモンドと生八セル障害

## 0. 正本・exact-source検証

2026年11月7日 JST。Repository: `itakura-hidetoshi/KuuOS`、canonical branch: `main`。
Qi v5.09の証明済み原始生成元`fourfoldPentagon`と、Qi v5.07の元`mixedResidue`を、真正元P77/GK5CGに由来する自由七セル履歴の同一始終点で組み合わせる。

| 項目 | 確定値 |
|---|---|
| 定理PR | [#3272](https://github.com/itakura-hidetoshi/KuuOS/pull/3272) **MERGED** |
| 定理squash | `4f497a027b34e0ef085e260f027fe6247b71c839` |
| exact-source CI | [#42373798805](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42373798805) **SUCCESS** |
| Strict Lean | 選択Lean本体 **SUCCESS**、公開集約含む |
| Governance | **30 / 30 SUCCESS** |
| 新規17宣言 | `#print axioms`監査、標準公理 `propext`、`Classical.choice`、`Quot.sound` のみ、または公理不要 |
| `sorryAx` | なし |
| source HEAD | `9dc7b15c6b1c70d85fb5b40f6c5aee5e7aa86523` |
| test-merge HEAD | `f041c3054863e80f82e8198c1b5c2c695f7717c3` |
| source/test-merge Git tree | `f3da187cd1482d24f6b020577e218e98fc15bc31` **完全一致** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 / root | `KuuOSFormal` / 107維持 |
| 保護PR | #1558 Draft / OPEN / 未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FourfoldMixedCriticalDiamondV5_10.lean) · [Qi v5.09正式記録](Qi-v5_09-original-P77-fourfold-pentagon-minimal-eighth-completion-verified-20261107.md) · [元PR #3238照合記録](Qi-v5_07-PR3238-canonical-V2-parity-reconciliation-verified-20261107.md)

## 1. 本当に同じ自由六セル始終点を持つ四頂点

Qi v5.08で構成・区別された元四重五角形の七セル履歴を

- `H₃ := sevenFourfoldInversePentagonThree l r`（結合子3回）
- `H₂ := sevenFourfoldInversePentagonTwo l r`（結合子2回）

と置く。Qi v5.06/v5.07の真正混合残差の二履歴を

- `M₁ := sevenMixedResidueFirst (long := l) (short := r) r`
- `M₂ := sevenMixedResidueSecond (long := l) (short := r) r`

と置く。

`SevenRewrite.congrComp`によって次の四頂点を構成する。

```text
NW = H₃ ⊗ M₁         NE = H₂ ⊗ M₁
SW = H₃ ⊗ M₂         SE = H₂ ⊗ M₂
```

各値は **実際の元`SevenRewrite` Typeの値** であり、新しい比較に合わせて自由六セル始終点を後付けで同一視していない。
`NW = fourfoldMixedResidueFirst l r`、`SE = fourfoldMixedResidueSecond l r` はQi v5.09の真正値を再使用する。

## 2. 新しい一原始生成元と旧比較の局所合流

次の四つの比較を、添字付き`PentagonAssocEightCell`と既存`MixedResidueEightCell`で構成する。

```text
       NW ── P(new) ──> NE
        |                 |
      M(old)            M(old)
        |                 |
        v                 v
       SW ── P(new) ──> SE
```

- 北辺 `fourfoldMixedCriticalNorth`：実際の`fourfoldPentagon`と旧反射比較を`compositeContext`で結合。
- 西辺 `fourfoldMixedCriticalOldWest`：元`mixedResidue`と旧反射比較だけで構成。
- 東辺 `fourfoldMixedCriticalOldEast`：同じ旧`mixedResidue`で構成。
- 南辺 `fourfoldMixedCriticalSouth`：同じ一種類の新`fourfoldPentagon`で構成。

`fourfoldMixedCriticalNorth_noOld`と`fourfoldMixedCriticalSouth_noOld`は、旧文法での北辺・南辺比較の不存在を証明する。証明はQi v5.09の既証明対角線不可能性`fourfoldMixedResidue_noPrevious`と、旧東辺・西辺を合成した**導出**であり、追加仮定でも新公理でもない。

`fourfoldMixedCriticalLocalDiamond`は四辺の具体的な型付き証拠と二つの旧比較不存在をまとめて証明。`fourfoldMixedCriticalClassDiamond`は新しく**選択した**七セル履歴商の四頂点が同一クラスになることを証明する。元七セルType値のstrict Eqは主張しない。

二つの実際の八セル完成経路

```lean
fourfoldMixedCriticalPThenM l r
fourfoldMixedCriticalMThenP l r
```

はどちらも`PentagonAssocEightCell W l r NW SE`を持つ。

## 3. 残る高次obstructionの正確な意味

`mixedResiduePrimitiveTrace`は旧八セル生証拠に現れる本来の`mixedResidue`生成元だけを順番に記録する。
`pentagonAssocPrimitiveTrace`は、新八セル生証拠において`fourfoldPentagon`を`true`、旧`mixedResidue`を`false`として記録する。旧反射比較などの他の生成元から、架空の新しい原始比較イベントを作らない。

実際に

```lean
pentagonAssocPrimitiveTrace (fourfoldMixedCriticalPThenM l r)
  = [true, false]
pentagonAssocPrimitiveTrace (fourfoldMixedCriticalMThenP l r)
  = [false, true]
```

を`rfl`で検証し、`fourfoldMixedCriticalRawEightGap`で

\[
\boxed{
\mathrm{PThenM}(l,r)\ne\mathrm{MThenP}(l,r)
}
\]

を**生の自由八セル証明Typeのstrict Eqとして**証明した。

これは「七セルの二分岐は新商で局所合流する」が「その二つの八セル証明自体はstrict Eqでない」ことを意味する。ここから**九セル比較が存在しない、あるいは全てのモデルで高次coherenceが不可能**とは導けない。イベント順序traceが将来の九セル比較の不変量であるとも仮定しない。

## 4. 降下する観測量・source境界

`fourfoldMixedCriticalParityCompatibility`はv5.09の全構成子保存定理から

\[
V_2(NW)=V_2(SE),\quad
R_2(NW)=R_2(SE),\quad
U_2(NW)=U_2(SE)
\]

を導く。Qi v5.09の`Quotient.lift`による三観測の降下はそのまま保持される。他方、旧結合子指紋 `Phi` はv5.09の新七セル商では降下しないままである。観測降下、元証拠履歴、独立八セル値、将来の九セル比較問題を区別する。

元F55/P77/GK5CG定義、全独立presentation、既存`MixedResidueEightCell`、元`PentagonAssocEightCell`、元七セル商、Lean/toolchain/workflowは**変更なし**。追加は新規Leanファイル1件と`KuuOSFormal`へのimport 1行のみ。

## 5. CI初回失敗の構造的理由と修正履歴

初回CI [#42373499281](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42373499281) は冒頭のドキュメントコメントに`three-/two-associator`と書いたことで、内部の`-/`がLean4のブロックコメントを途中終了させ、6行目で`unexpected identifier; expected command`を発生した。本文の17宣言は全て公理出力まで評価されていた。

この一箇所だけを`three- and two-associator`に修正したcommit `9dc7b15c6b1c70d85fb5b40f6c5aee5e7aa86523`で再検証を行い、上記CI #42373798805で全30ジョブSUCCESS。定義の縮小、仮定追加、`sorry`、公理化、以前のsource変更による回避は行っていない。

## 6. 次の厳密課題

**Qi v5.11候補：** 二つの自由八セル完成経路を型付きで比較する**独立した最小九セル**を検討し、その際にどの高次の不変量が保たれ、どの順序traceが新しい商で失われるかを区別する。全ての任意parallel八セル間の比較可能性やglobal thinnessを導入しない。元の型付き二経路と原始生成元の履歴を保持し、obstructionを明示した条件付きdescentから進める。
