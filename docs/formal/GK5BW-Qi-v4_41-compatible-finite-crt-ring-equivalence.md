# GK5BW／Qi v4.41 — 一般有限CRTの互換剰余環同型・真正北C60符号付き自然性

2026年11月4日 JST ／ F112-P94D3GK5BW・Qi v4.41 ／ **独立・Qi両定理MERGED**

## 1. 正本、定理、CIの独立検証

| 項目 | 独立 GK5BW | Qi v4.41 |
|---|---|---|
| 定理PR | [#3092](https://github.com/itakura-hidetoshi/KuuOS/pull/3092) MERGED | [#3093](https://github.com/itakura-hidetoshi/KuuOS/pull/3093) MERGED |
| exact-source HEAD | `d7302189f869f996cdb987e268842d6356ec8d39` | `3f23f806ac372018623522d09162910a3da23f7b` |
| squash SHA | `c991b6954c0892ab13062552885d2f009cb92c29` | `7f6cc9c963b18a7e76c03ab08551a1b27dccc6cb` |
| source／test-merge／squash Git tree | `2f89b7e1c73c0550e4ed8e69697f799cbf38faaf` | `fd9599b4dbc0c9f22d026b8e8f465b0f775e839f` |
| exact-source CI | [#41800156014](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41800156014) | [#41801723083](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41801723083) |
| Strict Lean | **9,301/9,301 SUCCESS** | **10,228/10,228 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規 `#print axioms` | **7定理、sorryAxなし** | **8定理、sorryAxなし** |
| 変更Lean warning/error | **0/0** | **0/0** |

正式ソース： [独立GK5BW Lean4](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BWFiniteCRTRingEquiv.lean)、[Qi v4.41 Lean4](../../formal/KUOS/Architecture/QiWuxingGK5BWNorthCompatibleCRTRingV4_41.lean)、[公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)。

検証済み最新canonical main HEAD：`7f6cc9c963b18a7e76c03ab08551a1b27dccc6cb`。Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`を固定。公開root107・保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを保持。既存Lean theorem sourceは改変せず、各新規モジュールと公開集約の追記のみ。

## 2. GK5BW — 互換な有限局所剰余族の真の環同型

任意の有限添字集合`s:Finset ι`、任意の自然数法`m:ι→Nat`について、`L=s.lcm m`。局所値の**依存積** `(i:{i // i∈s}) → ZMod (m i)` のうち、各二局所のgcd上への真正`ZMod.castHom`射影が一致するものを`nativeGK5BWCompatibleSubring s m`として実際の`Subring`に構成した。

数学的定理：

```text
ZMod (Finset.lcm s m) ≃+*
  nativeGK5BWCompatibleSubring s m
```

この同型は単なる大域代表`∃x`ではない。大域環から局所環への成分ごとの`ZMod.castHom`を**RingHom**として定義し、局所互換性、加法・乗法・単位元の保存、単射性、全射性を証明し、`RingEquiv.ofBijective`へ接続した。全局所値からの単射は`Finset.lcm_dvd`と`ZMod.intCast_eq_intCast_iff_dvd_sub`に基づく。

**ゼロ法と空被覆も含む。** `L=0`の場合は元の被覆に法0の実サイトが存在することを`Finset.lcm_eq_zero_iff`で取り出し、`ZMod 0`の真正**符号付き整数**代表で全局所を再構成する。`L≠0`ではすべての局所法が非零となり、既証明GK5BVの一般有限非互いに素CRTから自然数大域代表を構成する。互いに素、非零、非空、支配的サイトの仮定は一切加えていない。

CI修正履歴：独立GK5BW初回の`Subring.one_mem'`簡約と、`ZMod.castHom`・`ZMod.cast`間の型照合、法0のgcd正規化に伴うLean4 elaboration問題を、固定mathlibの`ZMod.cast_intCast`／`ZMod.cast_natCast`／`ZMod.cast_id`を明示して修正。数学的な命題・仮定・結論は不変。最終9,301ジョブ成功、公理監査7定理`sorryAx`なし。

## 3. Qi v4.41 — 真正北C60符号付き整数値と有限被覆制限の自然性

元GK5BQの**同一の符号付き整数**`nativeGK5BQClearedNumerator d j values : Int`を、絶対値ではなく直接`ZMod L`へ移し、独立GK5BWの実際の環同型により互換な局所剰余族へ写した。各元局所サイトでの座標は元整数の`ZMod (mᵢ)`への**符号を保つ剰余射影**と一致し、同型の逆写像で元の**数値合同類**を回収する。

任意の有限部分被覆`t⊆s`で、`lcm_t | lcm_s`を証明し、局所互換剰余環から部分被覆への真正`RingHom`を構成。大域`ZMod`側の`ZMod.castHom`と局所側の被覆制限が可換となる**環同型の自然性**を、固定mathlibの`RingHom.ext_zmod`で型付き証明した。元符号付き整数numeratorの局所座標は部分被覆への制限後も一致する。

さらに、実際の元F55 primitive original source（深度多項式`P=1`）と、真正double inverse＋元F55右単位source（`P=X²`）について、双方とも全有限非互いに素CRTの数値環同型を利用できるが、元original→phiの構造的seam判定は**前者が存在／後者が不存在**であることを1つの型付き定理として保持した。既存の`lcm_s | d!`と`2≤d`の明示的条件下では両者の数値的有限CRT零証明書も同時に成立する。

CI修正履歴：初回Qiの2箇所の`NativeC60FivePhaseGauge`未解決は既存名前空間のopen不足であり、既存の`KUOS.Architecture.WuxingCyclicPaths`を参照して修正。仮定を変更せず最終10,228ジョブSUCCESS・8定理`sorryAx`なし。

## 4. 構造的 authority 境界と次の研究

`ZMod L ≃+* compatible local ring`は**数値／環のdescent**であり、元F55 Type値のsource、P77商類の等号、P94A四セル、GK5AYの全域seam、P89無条件反射、`W=1→seam`を証明するものではない。元F54の真正二Nat・二圏・Blocks、F55のType値履歴、真正北C60第五Dart物理gauge、条件付きP89障害を別authorityとして保存する。Gray圏の復元・GK5BA kitは追加しない。strict 空と独立Kuu→Qiを同一視しない。

**次GK5BX（研究計画、未証明）：** 真正環同型と有限被覆制限の自然性を、有限包含の合成／恒等に関する擬関手的コヒーレンス、必要なら元整数多項式値の評価自然性へ拡張する。その際も算術的descentからの元F55 Type gluingを推論せず、obstructionを別定理として保持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
