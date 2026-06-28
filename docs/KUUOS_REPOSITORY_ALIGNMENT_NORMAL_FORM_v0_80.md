# KuuOS Repository Alignment Normal Form v0.80

## 目的

v0.80は、v0.79の有限構造候補が停止し、候補の適用順序に依存せず同じ構造正規形へ到達するかを検証します。

```text
RepositorySnapshot
→ 全admissible候補を列挙
→ 各shadow successorを再観測
→ 到達可能状態を有限探索
→ terminal集合を比較
→ normal-form certificate
```

外部承認は要求しません。

## 厳密減少

各admissible遷移には次を要求します。

```text
target weighted defect score
<
source weighted defect score
```

同じscoreの横移動やscore増加を探索辺に含めません。

scoreは自然数なので、厳密減少列は無限に継続できません。

## 有限探索

探索はsnapshot digestで状態を同一視します。

既に観測したdigestは再展開しません。

`max_states`を超える場合は`alignment_state_bound_exceeded`としてfail closedします。

状態上限へ到達した結果を、収束証明として扱いません。

## terminal

admissible successorを持たないsnapshotをterminalとします。

terminal scoreは0とは限りません。

有限catalogで修復不能な欠陥が残る場合、正のscoreを持つ固定点になり得ます。

したがってcertificateは次を分離します。

- terminalであること
- scoreが0であること
- terminalが一意であること

## 合流性

到達可能なterminal snapshot digestが一つだけの場合、探索範囲内で候補順序は合流します。

```text
unique_terminal = true
```

決定的選択経路の最終digestが、その一意terminalと一致することも別に検証します。

## certificate

certificateは次を保持します。

- 初期snapshot digestとscore
- 探索したsnapshot digest集合
- 全遷移digest
- terminal digest集合とscore
- 状態数と遷移数
- 全遷移の厳密減少
- 全terminalの固定点性
- terminal一意性
- 決定的経路との一致

## fixture

v0.79 fixtureには独立した四つの構造欠陥があります。

その到達可能状態は16、遷移は32です。

全適用順序は同じscore 0のterminalへ到達します。

決定的経路のscore列は次です。

```text
70 → 50 → 30 → 10 → 0
```

## live repository

v0.78とv0.79の明示contract spineについて、現在のrepositoryはscore 0です。

したがってlive certificateは次になります。

```text
explored states = 1
explored transitions = 0
unique terminal = current snapshot
```

## 非主張

v0.80は次を主張しません。

- 未登録の任意候補についての合流性
- 無制限repository探索
- score 0と真理の同一視
- GitHubへの直接書込み
- CI成功による数学的または制度的権威
