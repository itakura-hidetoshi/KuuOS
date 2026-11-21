# Lean→Python v0.50 — 原本PlanOS結果集合の明示的補助証拠

Canonical base: `5b0770a3c32c23f5fc6dd69b5f2dcbf09bee7656`。Lean `v4.30.0-rc2`。
mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
append-only／tighten-only／overwrite-forbidden／same-root。

## 検証対象

v0.49では、原本PlanOSが返していない3つのresulting Finsetを
限定投影から一意に復元できないことを、原本Lean型の2証明書で証明した。

v0.50では不足する3集合を**別の明示的補助証拠**として入力できる形式を設ける。
Lean `ExplicitPlanResultEvidence` は、従来の
`VisiblePlanSourceProjection` と来歴・異議・少数意見の結果集合からなる。
`EvidenceMatchesOriginal` に含まれる4等式が別途**証明された場合に限り**、
同じ補助証拠に結びついた元証明書の結果集合一致を示す。
v0.49のfreshな結果相違は、共通の完全一致証拠では成立できない。

これは復元の**条件付き十分性**であり、
Pythonが受け取った辞書から元のLean証明項を生成するものではない。

## Pythonの観測

元VerifyOS v0.4／PlanOS v1.03は変更しない。
元のv0.48検証とv0.49 `NO_DATA` を通過した組に限り、
申告された別入力を固定スキーマ・原本certificate digest・
集合の一意性・昇順・来歴／異議／少数意見の保存条件で検査する。

判定は明示的に3区分とする。

- `NO_DATA`：補助証拠の欠落
- `BLOCKED`：型、来歴、digestの局所的矛盾
- `PROPOSAL_ONLY_BOUNDED_SUPPLIED_PLAN_RESULT_EVIDENCE`：
  呼出側の申告内容が局所整合した場合。**原本PlanOSの実出力と
  認証済みという意味ではない。**

`original_plan_result_state = NO_DATA`、
`native_result_sets_observed = false`、
`external_issuer_authenticated = false` を変えない。
ダイジェストの自己一致は外部真正性や因果履歴の証明ではない。
Plan生成、World変更、Memory書込、Act実行権限は付与しない。

## CIと保護規律

新規Leanには固定mathlib Strict Leanと
個別7宣言公理監査が必須。Pythonの原本6経路、負例、
原本Git blob固定、公開root、Governance、Exact-head terminal、
提出HEAD／test merge Git tree一致を別々に検証する。
main全体`KuuOSFormal`の未認証は障害として残す。
保護PR #1558はDraft／OPEN／未マージ。

Preference ⇏ Descent ⇏ Authority。
