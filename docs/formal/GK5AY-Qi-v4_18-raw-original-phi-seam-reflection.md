# F112-P94D3GK5AY / Qi v4.18 — raw-originalと再帰φのseam・真正北C60の反射障害

**正式証明記録：2026年11月3日 JST。** Repository: `itakura-hidetoshi/KuuOS`。canonical theorem-bearing branch: `main`。既存の元F54双Nat・二圏・Blocks・F55 Type証拠・元P89 4-cellと、選択P92B/P93C/P94A、観測shadow、物理C60 gaugeは**別presentation**。strict 空 authority、**独立Kuu → Qi**、append-only／same-root（公開root **107**）、保護PR **#1558 Draft/OPEN/未マージ**を維持。Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**。

## 1. 確定済みPR・exact-source Lean CI

| 項目 | 検証済み記録 |
| --- | --- |
| 独立Kuu GK5AY | [PR #3022](https://github.com/itakura-hidetoshi/KuuOS/pull/3022) **MERGED** |
| GK5AY exact-source HEAD | `d61c1d6fd7498e43dae1b5ae42c489af600bccec` |
| GK5AY squash/main SHA | `d85c73d5845836c3a06e89a17bfebb7fd055e7cf` |
| GK5AY exact-source CI | [Governance #41594594525](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41594594525) **30/30 SUCCESS** |
| GK5AY Strict Lean | **9,254/9,254 SUCCESS** |
| GK5AY公理検証 | **15宣言**、`sorryAx`なし |
| Qi v4.18 | [PR #3023](https://github.com/itakura-hidetoshi/KuuOS/pull/3023) **MERGED** |
| Qi v4.18 exact-source HEAD | `98a743b0a777b8e8484e0d25722ce1f4c9b309ae` |
| Qi v4.18 squash/main SHA | `a098054e0647665141af877a4d3f0b7cea166523` |
| Qi v4.18 exact-source CI | [Governance #41605181371](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41605181371) **30/30 SUCCESS** |
| Qi v4.18 Strict Lean | **10,181/10,181 SUCCESS** |
| Qi公理検証 | **11宣言**、`sorryAx`なし |

両PRの最終CIで変更Leanファイルのcompiler errorは0。原始型・既存元P89/P92B/P93C/P94Aのsource APIと旧定理は変更なし。新規公理・`sorry`・`admit`・`native_decide`・Gray再構築・無条件高次gluingなし。検証ソースHEADとマージsquash SHAは混同しない。

## 2. 数学的焦点：P93C.old raw-original と GK5AIの再帰φは異なる

元F55の真正3-proof `f` について、選択P93Cの`old`生成元は元P89四セルの端点を`P92B.original(f)`／`P92B.original(g)`という**rawな全体wrapper**で受け取る。一方、GK5AIの真正構造写像`φ(f)`は元F55の**全9構成子**に対して再帰的に定義され、例えば元合成を選択側の合成へ、元恒等を選択側のreflへ写す。`P92B.original f = φ(f)` を定義的な等式として扱えない。

実際、真正北四段C60長短経路にある`nativeGK5AINorthPentagonWithIdentity`（元pentagon四段の後に元F55右恒等を合成した実在3-proof）について、

    P92B.original(nativeGK5AINorthPentagonWithIdentity)
      ≠ φ(nativeGK5AINorthPentagonWithIdentity)

がrawな選択P92Bの**Type値付き証明構成子の相違**としてLean4で成立する。両者の間に4-cellが存在しないという主張はしていない。

## 3. 本当に必要なseamは4-cell証明書（無条件存在ではない）

独立GK5AYは`NativeGK5AYOriginalPhiSeam first last`という真正依存型の**条件付き証明書**を定義する。各元F55 `f`ごとに

    bridge(f) : P94A(P92B.original(f), φ(f))

という**選択P94A四セルのType値付き証拠**を要求する。このレコードが無条件に inhabited だとは主張しない。`Nonempty Seam` iff 全元F55証拠に橋の真正P94A証拠が存在する、という正確なpointwise存在条件を証明した。

これにより任意の実際のraw P93C証拠`w : P93C(original(f),original(g))`から、

    P94A(φ(f), φ(g)) :=
      symm(bridge(f)) ; P94A.old(w) ; bridge(g)

を作る。等号で端点を置き換えるのではなく、本物の両端の高次比較を合成する。元P89証拠を`P93C.old`へ埋め込む場合もこの区別を保つ。

## 4. 真正元P89反射・局所obstruction・非単射性の正確な条件

同じ元F54 route slotの元F55証拠`f,g`を固定し、raw P93C四セル`w`とseam証明書が**実際に与えられる**場合、

    GK5AQBadPair(f,g)
      ↔ ¬ Nonempty(OriginalP89FourCell(f,g))

がLean4で成立する。選択P94A比較は本当のseamと`w`からすでに構成できるため、残る非反射障害は元P89証拠の欠損である。

また、生のP93C比較がありながら元P89四セルが存在しない場合を`RawP93Obstruction`と厳密に定義する。**raw P93C全面反射 iff RawP93Obstruction不存在**は、seamの有無とは独立して成立する。seamと実在raw障害が両方与えられた場合だけ、元P89→P94A四セル商写像が**ある正確なF54 route slotで非単射**になる。逆に元source class mapが単射でseamがあるなら、そのslotのraw P93C比較は元P89に反射する。元sourceの無条件faithfulness／nonfaithfulnessは未証明のまま保持する。

さらに、`P93C.old`が元P89四セルを本当に受け取っていても、そのraw`P92B.original`端点が再帰的φの像外であれば、GK5AUの内部source-holeは存在し得る。元4-cellがあることとrawな選択3-proofがφ像内にあることは別条件である。

## 5. Qi v4.18：真正北C60への11宣言

新規Qi Leanモジュールは、実際の北四段pentagon long/shortの元F54双Nat・Blocks・元F55証拠に以上を特殊化した：

1. `fivefoldGK5AYNorthSeam_nontrivial`：北のraw証拠と再帰φの非同一性＋**与えられた**seam四セル。
2. `fivefoldGK5AYNorthRawP93ToStructural`：真のraw P93C四セルをseam経由でφ端点P94Aへ移送。
3. `fivefoldGK5AYNorthRawP93_bad_iff_noP89`：選択raw比較のBadPair iff 元P89欠損。
4. `fivefoldGK5AYNorthP89Old_both`：真正元P89四セルとselected P94A四セルを併存させる。
5. `fivefoldGK5AYNorthRawObstruction_noninjective`：**与えられた**raw障害とseamがF54 slotの非単射性を導く。
6. `fivefoldGK5AYNorthPhysicalSeamGate`：4-cell seam条件と第五around Dart閉路・04／43物理向き・条件付き非単射性iffの併存。
7. `fivefoldGK5AYNorthPhysicalRawObstructionGate`：raw障害が存在する**場合のみ**の非単射と物理境界。
8. `fivefoldGK5AYNorthRawReflects_iff_noObstruction`：全面raw反射 iff raw障害なし。
9. `fivefoldGK5AYNorthRawComparison_reflect_or_bad`：seam＋実在raw比較なら元P89証拠またはGK5AQ BadPair。
10. `fivefoldGK5AYNorthRawReflects_of_allInjective`：**全F54 route slotの元class map単射を明示仮定した場合**にraw P93C全面反射。
11. `fivefoldGK5AYNorthPhysicalRawReflection_of_allInjective`：10の条件付き反射と第5Dart閉路・04/43方向・条件付き非単射性の整合性。

物理的五行gauge frameはseam四セルや元P89証拠、source class map単射性を生成しない。

## 6. Lean4エラーの根本原因と修正履歴

独立GK5AY初回 [Governance #41594170326](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41594170326) は、証明書フィールド名に予約語`at`を用いた構文解析失敗と、依存型forallの`intro`形式の問題があった。フィールド名を`bridge`に改め、全依存型添字を保持した導入構文へ修正した結果、最終exact-source HEAD `d61c1d6f...`で全Lean検証成功。

Qi v4.18初回 [Governance #41604664430](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41604664430) は、`have hreflect := ...` が完全な`∀`依存型のraw反射命題を推論しきれず、経路添字の未解決メタ変数が残るという1件のtype mismatchを報告した。修正では

    have hreflect : nativeGK5AYRawP93Reflects
        fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast :=
      fivefoldGK5AYNorthRawReflects_of_allInjective data allInjective

と明示し、定理仮定・結論・元定義は一切変更しなかった。最終source HEAD `98a743b0a777b8e8484e0d25722ce1f4c9b309ae`で**10,181/10,181 Strict Lean、30/30 Governance SUCCESS**、11公理監査・`sorryAx`なし。

## 7. 次：GK5AZ（仮称）

選択P93C raw originalと再帰φの橋が必要なこと、実際のseamを**条件として与えれば**選択raw比較をφ端点へ移送できること、欠けた元P89 4-cellが厳密な障害となることが定まった。次は、証明書全体を無条件に仮定しない**構成子別seam成立条件／局所obstruction**、さらにGK5AXの元P89 vertical unit/assoc 3 family反射証明書とGK5AWの8種contextの合成整合性を精査する。実際のP92B.originalと再帰φの接続がどの構成子で直接構成でき、どこで新規高次証拠が必要かを分離する。無条件の全P94A normal form、元P89非単射性、Gray復元、無条件高次gluingは先取りしない。

**Lean sources:** [GK5AY独立](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AYOriginalStructuralPhiSeamGate.lean)、[Qi v4.18](../../formal/KUOS/Architecture/QiWuxingGK5AYNorthOriginalPhiSeamV4_18.lean)、[前回GK5AX／Qi v4.17](GK5AX-Qi-v4_17-original-vertical-primitive-reflection-certificates.md)。
