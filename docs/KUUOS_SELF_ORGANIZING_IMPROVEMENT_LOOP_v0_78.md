# KuuOS Self-Organizing Improvement Loop v0.78

## 目的

v0.78は、KuuOSの構造を継続的に観測し、有限候補をshadowで比較し、再観測によって保持またはrollbackする自己改良ループです。

主経路は次です。

```text
観測
→ 構造診断
→ 有限候補生成
→ shadow比較
→ 暫定採用
→ 再観測
→ 保持またはrollback
```

外部承認は要求しません。

旧来のreview moduleは履歴および別用途の統治経路として残りますが、v0.78のループからは参照しません。

## 構造状態

構造状態は、正規化された有限個の構造座標として表します。

各状態は次を保持します。

- revision
- 構造座標
- 保護座標
- lineage
- canonical digest

保護座標には、authority、audit、provenance、rollbackなどの憲法的境界を割り当てられます。

候補生成は保護座標を変更しません。

## 観測

観測contextは、各構造座標のtargetとweightを保持します。

観測scoreは次です。

```text
E(x | c) = Σ_i w_i (x_i - target_i)^2
```

scoreは有限context上の構造的不整合量です。

低いscoreをtruthと同一視しません。

## 構造診断

診断は、観測値とtargetの差から構造圧力を計算します。

```text
pressure_i = weight_i × (target_i - observed_i)
```

保護座標に圧力が存在する場合は記録しますが、候補変更には含めません。

変更候補はmutable coordinateだけから生成します。

## 有限候補生成

候補生成は有限catalogです。

policyは次を固定します。

- 最大候補数
- 一候補の最大変更座標数
- 有限step fraction
- 比較許容差

候補は診断圧力へ有限step fractionを掛けて生成します。

自由なコード生成や無制限な探索は行いません。

## shadow比較

各候補はsourceとは別のimmutable stateとして具体化します。

有限個のshadow context上で、sourceとcandidateを同じ条件で観測します。

候補は次を満たす場合だけ内部選択対象になります。

- 全shadow contextで非悪化
- 少なくとも一contextで厳密改善
- 保護座標の完全保存
- source digest binding
- 変更数上限

選択順序は決定的です。

```text
aggregate candidate score
→ changed coordinate count
→ canonical candidate digest
```

外部reviewer、review license、approval receiptは使用しません。

## 暫定採用と再観測

shadowで選択された候補は、revisionを一つ進めた暫定stateとして構成します。

その後、独立したreobservation contextでsourceと暫定stateを再観測します。

再観測で非悪化が確認され、保護座標が保存されている場合だけ暫定stateを保持します。

確認できない場合は同じcycle内でsourceを返します。

```text
shadow通過 + 再観測通過 → ADOPTED
shadow通過 + 再観測失敗 → ROLLED_BACK
候補なし                     → NO_CHANGE
```

## 自己改良の意味

v0.78の自己改良は、返却されるimmutable stateが新しいrevisionを持つことです。

runtime関数は外部host stateやrepository fileを直接書き換えません。

上位runnerは返却stateとcycle receiptを保存し、次cycleのsourceとして使用できます。

したがって、自己改良は可能ですが、隠れた副作用による自己書換えではありません。

## 作用境界

cycle receiptは次を固定します。

```text
finite_candidate_generation = true
external_approval_required = false
authority_widening_performed = false
host_state_write_performed = false
```

外部承認を除外しても、保護座標、有限性、shadow比較、再観測、rollbackを除外しません。

## 既存系列との関係

v0.78は次の資産を概念的に継承します。

- v0.60：憲法的保護座標
- v0.62：有限候補
- v0.66：isolated shadow
- v0.67：有限比較
- v0.76：rollback lineage

次は主経路に含めません。

- v0.63：外部candidate review
- v0.69：external evidence review
- v0.74：external memory selection review

## 検証

runtime検証は次を確認します。

- 観測から診断へのdigest binding
- 保護座標を除外した有限候補生成
- shadow context順序に依存しない決定的選択
- 再観測による採用
- 再観測失敗時のsource復元
- 安定状態でのNO_CHANGE
- 外部承認不要
- authority wideningなし
- host writeなし

## 次段階

次段階は、repository module graph、workflow graph、formal import graphを構造座標へ変換する観測adapterです。

このadapterにより、v0.78の同じループをKuuOS repository全体へ適用できます。
