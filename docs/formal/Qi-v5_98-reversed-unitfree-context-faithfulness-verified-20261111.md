# Qi v5.98 — 反転を伴う真正1-unit・unit-free文脈における局所共同観測忠実性（Lean4形式認証）

2026年11月11日 JST。canonical正本：`itakura-hidetoshi/KuuOS` の `main`。
本記録は定理文・原始元依存型・証明来歴・未認証範囲を分離する。空・縁起・二諦・中道との関連は命名／解釈の層であり、これらの哲学的対応がLean4で証明されたという主張ではない。

## 1. 正本・形式環境・統合PR

- 唯一のcanonical branch：`main`。v5.97三段階統合後の基準HEAD：`8efbe2be7dc068b004106cafa4ded5365845aad8`。
- 定理PR [#3527](https://github.com/itakura-hidetoshi/KuuOS/pull/3527) **MERGED**。新規モジュール [`QiWuxingGK5CHP77ReversedUnitFreeContextFaithfulnessV5_98.lean`](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ReversedUnitFreeContextFaithfulnessV5_98.lean) 1件のみ、GitHub最終差分415行追加・既存削除0、実`#print axioms`17件。
- 定理の認証済み最終source HEAD：`ebede9886e96be5d2c5a24c4a66ed324be9ff0ac`。定理統合後main HEAD：`34ca6a6c236ef1d21b7bb62278bf2eb919d5681f`。
- 公開import PR [#3528](https://github.com/itakura-hidetoshi/KuuOS/pull/3528) **MERGED**。`formal/KuuOSFormal.lean` に新規import1行のみ追加、既存行削除0、公開root107維持。公開認証source HEAD：`5a0f3c8739754bc97bcb7724f461624a771f7496`。公開統合後main HEAD：`57e2f623060a01b4969e868841c10e32af76cb94`。
- Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`** を不変更。元17D／18D／19D依存型、旧5／新7比較構成子、既存証明を不変更。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージを維持。
- append-only／tighten-only／overwrite-forbidden／same-root。

## 2. 対象を制限した理由と真の元raw証拠

元の真正依存型 `SelectedLocalEighteen W l r J N` において、v5.97の `selectedV597OriginalPrimitiveUnit l r M` が成立する元 `M : J → N` を固定する。すなわち、v5.73の元内部括弧が文字通り `oldUnitLeft` または `oldUnitRight` である**単独元unit葉**に限る。真正unit数は1で、v5.92の完全型付きSigma payloadは元証拠 `M` 自身を保存する。

独立に、v5.88のunit-free構文 `t : SelectedV588UnitFreeTerm` を使用する。これはstrictだけではなく、元reverseと二変数chainを任意の非結合括弧配置で含めることができるが、元unit葉は含まない。v5.88埋め込みは本当の17D添字`J→J`または`N→N`を持つ旧18D値を構成する。

この二要素から、既存の真正元rawコンストラクタで次の2族を構成する：

```text
Left(t,M)  := reverse (chain (UnitFreeRawEmbed J t) M) : N → J
Right(t,M) := reverse (chain M (UnitFreeRawEmbed N t)) : N → J
```

新しい18D証拠型を作らず、原始unit payloadを架空のラベル・代理型へ置換しない。いずれも外側reverseを含む真正の元旧18D証拠であり、unit数は厳密に1である。

## 3. Lean4で検証された局所結果

- `selectedV598UnitFree_historyNil`：任意のv5.88 unit-free構文から得た元旧18D証拠の完全型付き元unit履歴は空リスト。
- `selectedV598ReverseLeft_bracket`／`selectedV598ReverseRight_bracket`：v5.73の元非結合括弧観測は、外側reverse・左右chain配置・unit-free構文全体・元unit葉の内部括弧を保持する。
- `selectedV598ReverseLeft_history`／`selectedV598ReverseRight_history`：左右いずれのunit-free文脈の追加・外側reverseも、原始unit葉`M`の完全なv5.92 Sigma unit payload履歴を変更しない。
- `selectedV598ReverseLeft_oneUnit`／`selectedV598ReverseRight_oneUnit`：真正元unit数は左右とも1。
- `selectedV598ReverseLeft_jointEq_iff`／`selectedV598ReverseRight_jointEq_iff`：同じ方向の2値と同じ真正依存型`J→N`の原始unit葉`M,L`について、
  `(Bracket(A)=Bracket(B) ∧ History(A)=History(B)) ↔ (t=u ∧ M=L)`。
- `selectedV598ReverseLeft_rawEq_iff`／`selectedV598ReverseRight_rawEq_iff`：同じ限定族では**元の真正raw証拠値そのものの等号**が`(t=u ∧ M=L)`と同値。元19D商クラスの等号に言い換えていない。
- `selectedV598Mixed_bracketNe`／`selectedV598Mixed_rawNe`：単独unit葉とunit-free文脈を左右で逆配置すれば、元括弧・元raw値は一致しない。
- `selectedV598Mixed_historyEq_iff_sourceEq`／`selectedV598Mixed_samePrimitive_historyGap`：左右の配置を変えても完全型付き履歴はunit葉の元sourceを復元するが、配置そのものを同一化しない。

この結果はv5.94の線形strict前置／後置から、入れ子reverseと非結合chainを持つ**unit-free文脈＋単独unit葉＋外側reverse**へ拡張する。**すべての一般的な1-unit元旧18D証拠を覆うものではない**。

## 4. CI失敗・修正・機械認証の経路

- 初回の実型検査 [CI #42970224307](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42970224307) はFAILURE。新規Leanファイルの230／265行で`injection`が等号目標を解決した後に余分な`exact ht`を続けたため、`No goals to be solved`が2件発生した。未完了証明から`sorryAx`を含む公理出力が一時的に現れた。
- 修正は**新規Leanファイル内のその2行の削除のみ**。定理文、元の依存型定義、既存証明、Lean/mathlib pinを変更せず、修正版exact-source [定理CI #42970801962](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42970801962) は**completed／SUCCESS**。
- 定理CI Scoped Strict Lean **9,150／9,150 SUCCESS**、17／17公理監査（公理不要4、`propext`のみ9、`propext`＋`Quot.sound`のみ4）。新規`sorryAx`なし、対象Lean error／warning 0／0。Governance／独立Core／workflow整合性／summaryすべてSUCCESS。
- 定理のsource／test-merge／squash後main Git treeは **`d2eaa241ebf30183f67b47cb092a9c3c30b274c4`** で一致。
- 公開import exact-source [公開CI #42971723540](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42971723540) **completed／SUCCESS**：公開KuuOSFormal依存閉包 **10,411／10,411 Strict Lean SUCCESS**、Governance **30／30 SUCCESS**、実17件公理監査同上、変更Lean warning／errorなし、`sorryAx`なし。
- 公開import source／test-merge／squash後main Git treeは **`750e9882bc2dac115007b1f2f0c82670acc54b52`** で一致。

## 5. 残余障害（NO_DATA）と次段の境界

- v5.93の**真正同一`J→N`fiber・unit数1・同じv5.73元内部括弧・異なる元raw証拠**の存在／不可能性は依然 **NO_DATA**。
- このv5.98定理が示すのは、原始unit葉の値をSigma履歴に保存した、制限された2種の反転文脈での局所復元である。すべての1-unit旧18D内部の非自明なreverse/chain再帰の網羅的な復元は未認証。
- 旧5／新7の元19D比較関係全域の同値、異fiber間の証拠同一化やgluing、WORLD／20D大域降下、AIの行為権限はここからは導けない。局所faithfulnessを無条件に大域化しない。
- 次のQi v5.99候補は、真正1-unit元証拠の任意のchain枝に生じる**中間17D添字**と一つの元unit payloadを保ちつつ、局所復元のために追加すべき添字／再帰位置情報を特定し、復元不能箇所を独立obstructionとして残すことである。
