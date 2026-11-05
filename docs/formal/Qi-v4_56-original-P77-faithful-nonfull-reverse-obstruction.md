# Qi v4.56 — 真正元P77保守的5-cell商関手のFullness必要十分条件と逆向き証拠障害

**2026-11-05 JST**

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3132](https://github.com/itakura-hidetoshi/KuuOS/pull/3132) **MERGED** |
| 最終exact-source HEAD | `211ba667ebebc7f1930698882eff94bc4086c8ee` |
| 定理squash/main SHA | `faa5f5213cbdaeec653500997b7306be97b5c329` |
| source/test-merge tree | `be12b671ad295cfe61a0e0bf4e032aabd13211c9` 完全一致 |
| exact-source CI | [#41950414210](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41950414210) |
| Strict Lean | **10,253 / 10,253 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **10 / 10**、`propext`／`Classical.choice`／`Quot.sound` のみ、`sorryAx` なし |
| 変更 | [新規Lean1ファイル](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FullnessReverseObstructionV4_56.lean)＋公開 `KuuOSFormal` のimport1行 |

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107、strict空中心、独立Kuu一presentation、保護PR #1558 Draft/open/unmerged。すべての元F54/F55/P77/P94A証拠履歴、真正C60物理Edgeと符号付き整数CRTのauthorityは独立に保持。

## 1. 厳密な研究対象と区別

Qi v4.53が型付き自由経路`Quiver.Path`を元F55/P77の**生のType値付き四セル証拠**に評価し、v4.54が元GK5CG**保守的Type値5-cellの存在のみ**を同値関係として商を構成した。v4.55で、その真正Categoryへの関手

```text
F : FivefoldFreePathCategory ⥤ FivefoldP77ConservativePoint f g h k
```

は無条件 `Faithful` と形式証明済み。今回v4.56では、同じ上流の四セル・5-cell構成と関手を一切書き換えず、**Full（各Hom上の全射性）**を調べる。Faithfulは単射、Fullは全射であり別物。自由圏と元P77生構文を同じ型とせず、保守的商で成立したcategory lawsだけを利用する。

## 2. 元P77四証拠に関するFullnessの必要十分条件

元の2カテゴリー、2つのNat深さ、Blocksと4つの合成可能元F55証拠 `f,g,h,k` を任意に保持。任意の`u,v : FivefoldPathVertex`と、その始終点の元P77生証拠`w`について、

```text
Reachable ([w])
  ↔ ∃ path : Quiver.Path u v,
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k path) w)
```

を `fivefoldP77ConservativeClass_reachable_iff` によって証明。左辺は**真正Functor.map像**、右辺は**元証拠のType値を保存する保守的5-cellの存在**であり、charge等号や数値CRTの等号ではない。主定理 `fivefoldP77ConservativeFunctor_full_iff_originalReachable` は全`u,v,w`に量化して

```text
F.Full ↔
  ∀ u v (w : ORIGINAL P77 four-proof u→v),
    ∃ path : Quiver.Path u v,
      Nonempty (ConservativeFiveCell (Eval path) w)
```

を形式証明。逆方向は真正target Homが **original 5-cell setoid quotient** であることを`Quotient.inductionOn`で代表元へ還元し、型付き証拠から`Functor.Full`を構成する。上流の5-cellを「存在すると仮定」した無条件Fullではない。

## 3. 全targetに適用できる負のチャージ到達障害

元GK5CGの真正整数`gk5cgAssocCharge` は保守的5-cellの**全コンストラクタ**で保存され、v4.54にて`fivefoldP77ConservativeCharge`として商に降下済み。元の5本の有向`FivefoldEdge`だけからなる任意の自由経路`path`は、`charge(F.map path)=(path.length : ℤ) ≥ 0`。

`fivefoldP77Conservative_negativeCharge_not_reachable` は任意のtargetクラス`z`に対して、

```text
charge(z) < 0 ⇒ ¬ Reachable(z)
```

を形式証明した。これは不必要な全域証拠不在を仮定せず、**負のchargeが具体的なobstruction**になるという一般的な定理である。逆方向、非負chargeなら必ず到達可能、は主張しない。

## 4. 真正元P77の逆向きe01四セルが非Fullを証明する

正方向の真正`FivefoldPathArrow e01 : 0→1`は、旧v4.53の`fivefoldArrowOriginalP77`により**元P77四セル値**を持ち、chargeが`+1`である。元のP77の本物の `NativeF55RawVerticalFourCell.symm` を適用すると、target圏のフェーズ **1→0** に逆向きの元四セルが存在する：

```text
fivefoldP77OriginalReverse01 f g h k :
  FivefoldP77ConservativeClasses f g h k (phase 1) (phase 0)
```

これは「新しいFivefoldEdgeの逆辺」を自由クィバーに追加したのではない。**元P77四セル自身の真正反転コンストラクタ**から生まれるtargetだけの証拠である。

`fivefoldP77OriginalReverse01_charge` は旧GK5CG`symm`の符号反転を使い、`charge(reverse01)=-1`を証明。`fivefoldP77OriginalReverse01_not_reachable` は前節の普遍的負charge障害より、このtargetクラスに元自由経路のpreimageが存在しないことを無条件に証明した。

より強いType値版 `fivefoldP77OriginalReverse01_noSourceFiveCell` は、任意の仮定上の同端点経路`path : 1→0`から評価した元P77四セルと、この逆向き元証拠との間に**保守的5-cell証拠は存在しない**と示す。数値の長さのみを元証拠と同一視していない。

## 5. 無条件 Faithful かつ NonFull

`fivefoldP77ConservativeFunctor_not_full` は真正mathlib `Functor.Full.map_surjective` の定義を使い、上記1→0の逆向きtarget証拠が全射のはずだとすれば矛盾を得る。

`fivefoldP77ConservativeFunctor_faithful_and_not_full`：

```text
(fivefoldP77ConservativeFunctor f g h k).Faithful ∧
¬ (fivefoldP77ConservativeFunctor f g h k).Full
```

を全元F55合成可能四項組で形式証明。

**数学的意味：** 元FivefoldEdgeの5本から作る自由経路の区別は、真正P77保守的Categoryに移しても失われない。しかし、targetには元四セル`symm`由来の追加のHomが実在し、全Homを源5辺の合成だけでは生成できない。**忠実さは成立しても充満性は成立しない。** 旧元証拠の欠如を補うため勝手に歴史的pentagonatorを宣言したのではない。

## 6. 全ファイル・固定mathlib API・CI修正履歴

既存v4.53〜v4.55新規Lean全文、GK5CGの保守的5-cell全構成子とcharge保存、v3.5元`FivefoldEdge`、固定mathlib `Functor/FullyFaithful.lean` の`Full`定義/`map_surjective`、P77/P78元商証拠を照合。

初回HEAD `9c219446ca57803085a9f364047a6642920250c9`、[CI #41949329227](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41949329227) は本体Leanで次の3系統を検出：
- `Quotient.inductionOn` のtargetラッパー分解後、`hreach u v w` が`u : FivefoldIndex`を受ける型不一致。真正`FivefoldPathVertex`へ`⟨u⟩`、`⟨v⟩`で戻した。
- 負charge証明の`omega`で、依存型の隠れた引数が関数式として正規化されず不等式の一致を認識しない。適切な`lt_of_eq_of_lt`による証明へ変更した。
- `rw`が閉じた目標へ続く余分な`norm_num`を削除した。

第2HEAD `d6e2c3d760365e9289e7759b2460aa70804e10b1` の[CI #41949837835](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41949837835) では残り1件、`rw [←hcharge]`が異なる暗黙引数のため同一に見える式をマッチできず失敗。この箇所を`lt_of_eq_of_lt hcharge hz`による**等式→不等式推移の直接証明**へ修正し、元の数学的仮定／結論を変更しなかった。

最終exact-source HEAD `211ba667...` の[CI #41950414210](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41950414210) で**Strict Lean 10,253 / 10,253 SUCCESS**、新規10件`#print axioms`は標準3公理以内で`sorryAx`なし、Governance30/30・独立公開API成功。source/test-merge tree`be12b671...`一致をMCPで確認し、検証済みHEADを指定してsquash MERGED（`faa5f521...`）。

## 7. 次の数学的境界

この時点で、指定した5本の元FivefoldEdgeから元P77保守的商Categoryへの関手は**FaithfulかつNonFullと完全確定**。今後の研究は元P77 targetに「足りないすべての証拠を、保存的に生成せよ」と無条件に仮定するのでなく、真正経路像`Im(F)`を別に定義して、そこでの**fully faithful factorization**と、元targetへ戻る射がfullでない理由を別々に形式化することが自然。元P77四セルのsymm、保守的5-cell、元P94A比較、独立Kuu／strict空、C60物理構造は別authorityのまま維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
