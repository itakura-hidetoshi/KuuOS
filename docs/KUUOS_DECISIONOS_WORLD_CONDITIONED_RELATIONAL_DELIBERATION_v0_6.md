# DecisionOS WORLD条件付き関係的熟議 v0.6

## 位置づけ

本仕様は、DecisionOS v0.5が受理したPlanOS v1.02の候補分布を、関係的熟議へ接続する。

本層は候補を選択しない。

本層は、候補ごとの和、stakeholder、関係性、異論、少数側影響、不確実性を評価し、選択前の熟議場を形成する。

PlanOSが与える確率順位と遷移作用は助言情報として保持される。

確率一位または作用最小の候補を、そのままDecisionOSの選択結果へ昇格させない。

## 入力

入力はDecisionOS v0.5 intake receiptである。

このreceiptは、次を既に保持している。

* WORLD stateとrevisionとlineage
* 全候補のidentity
* 許容候補と不許容候補
* 候補確率質量
* PlanOSの助言順位
* Wa evidence
* stakeholder evidence
* relational evidence
* dissent evidence
* minority evidence
* 明示的不在証明

v0.6はsource digestを再計算する。

v0.6は候補別intake digestとevidence bundle digestも再計算する。

source receiptが選択済み状態へ昇格している場合、fail-closedで拒否する。

## 候補熟議入力

各候補は次の六次元プロファイルを持つ。

* wa_support
* stakeholder_support
* relational_support
* dissent_pressure
* minority_impact_risk
* uncertainty_burden

各値は0以上1以下である。

この六次元は単一効用へ強制的に縮約しない。

候補は正の支持軸と負担軸を同時に保持する。

## 関係的gate

許容候補には三つの支持gateを適用する。

* Wa support gate
* stakeholder support gate
* relational support gate

異論圧が閾値を超える場合、dissent reviewを要求する。

source intakeに異論証拠が存在する場合も、dissent reviewを要求する。

少数側影響リスクが閾値を超える場合、minority protection reviewを要求する。

source intakeに少数側証拠が存在する場合も、minority protection reviewを要求する。

不確実性負担が閾値を超える場合、uncertainty reviewを要求する。

review blockerが存在する場合、evidence completion reviewを要求する。

## 不許容候補

不許容候補を削除しない。

不許容候補は`nonadmissible_retained`として保持する。

不許容候補にはexclusion review digestを要求する。

これにより、制約による除外と候補identityの消去を分離する。

## 関係的部分順序

熟議可能な候補間では、六次元プロファイルに基づくPareto型部分順序を用いる。

候補Aが候補B以上の全支持軸を持ち、候補B以下の全負担軸を持ち、少なくとも一軸で厳密に良い場合、AはBを関係的に支配する。

支配されない候補集合をrelational frontierとする。

relational frontierは選択結果ではない。

relational frontierは、単一スコアで消去できない熟議対象集合である。

## PlanOS順位との関係

source probability massを保持する。

source combined transition actionを保持する。

source advisory rankを保持する。

ただし、これらは関係的部分順序の支配条件に使用しない。

したがって、PlanOS順位一位でも異論審査または少数側保護が必要であればfrontierへ自動昇格しない。

確率順位は未来経路分布の情報である。

関係的熟議は、候補が誰にどのような影響を与えるかの情報である。

両者を同一の尺度へ還元しない。

## required review field

required review fieldは次を統合する。

* relational frontier
* dissent review候補
* minority protection候補
* uncertainty review候補
* evidence blocked候補
* hold guardによって保持されるhold候補

この集合は選択候補集合ではない。

この集合はDecisionOSが次段階で明示的に扱う責任対象である。

## 熟議disposition

熟議結果は次のいずれかになる。

* minority_protection_review
* dissent_review
* evidence_completion_review
* uncertainty_review
* hold_guarded_relational_review
* no_relationally_reviewable_candidate
* single_relational_frontier_review
* plural_relational_frontier_review

dispositionは処理経路を示す。

dispositionは候補選択を意味しない。

## 責務境界

本層はDecisionOSが熟議責務を所有することを明示する。

本層は選択権限を生成しない。

本層は候補を選ばない。

本層はdecision receiptを発行しない。

本層はPlanOSの計画合成を行わない。

本層はActOSを呼び出さない。

## WORLD境界

WORLD model stateは変更しない。

WORLD predictionをtruthへ昇格させない。

WORLD mutation permissionを生成しない。

source WORLD binding、state、revision、lineageをreceiptへ保持する。

## 履歴とQiの境界

履歴はread-onlyである。

Qiは熟議条件を与えうるが、選択権限を与えない。

Qiは実行権限を与えない。

## 出力境界

出力はfuture-onlyの熟議receiptである。

`active_now`はfalseである。

`execution_permission`はfalseである。

`selected_candidate_id`は空文字列である。

`decision_selection_performed`はfalseである。

## 形式化

Lean形式層は次を証明対象とする。

* relational frontierはadmissible fieldの部分集合である
* required review fieldはsource candidate fieldの部分集合である
* 候補identityと代替候補が保持される
* source probabilityとsource actionは助言情報に留まる
* 関係的部分順序は単一スコア選択への短絡を禁止する
* Wa、stakeholder、関係性、異論、少数側が保持される
* 熟議は選択権限を与えない
* WORLD、履歴、Qiの境界が保持される
* 熟議receiptはdecision、計画合成、実行ではない

## 接続

本層までの接続は次となる。

```text
WORLD possibilities
→ PlanOS information-geometric path distribution
→ PlanOS selection-precondition certificate
→ DecisionOS evidence intake
→ DecisionOS relational deliberation field
```

次段階は、この熟議場から候補を選ぶためのDecisionOS selection justification層である。

その層でも、選択は実行を意味しない。
