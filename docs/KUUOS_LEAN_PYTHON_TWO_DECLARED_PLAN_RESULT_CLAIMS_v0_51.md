# Lean→Python v0.51 — 二つの申告補助証拠の一致と障害

Canonical base `73a15b3da05d26af95203d446ea557fd7b54bbd9`。Lean `v4.30.0-rc2`、
mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

**研究候補であり、実Lean CI認証前には証明済みと主張しない。**

## 原本型の条件付き形式化

原本PlanOS v1.03のLean型とv0.50の`EvidenceMatchesOriginal`を直接import。
新規`DeclaredPlanResultClaim`は申告されたclaim ID・issuer label・
二つのソースdigest・型付き結果証拠からなる。
issuer labelは**文字列**であり、暗号学的認証も発行主体の独立性も保証しない。

- 二つの補助証拠が**同じ原本Lean証明書と一致する証明を別途持つ**
  場合、その3結果Finsetは完全に一致する
- 来歴・異議・少数意見のどれかに相違があれば、両方が同一原本と
  正確に一致することは不可能（条件付き）
- v0.49のinert／widened原本型証明書を使い、同じと申告された
  source digest文字列から結果集合の一致は**導けない**ことを示す
- 結果の一致、ラベル数、発行者の自称、参照digestだけでは、
  Python全体の意味論、真正性、降下、実行権限を付与しない

## Python読み取り専用監査

二つの申告レコード`first`／`second`を元VerifyOS／PlanOS証明書に
結び付けて、まずそれぞれv0.50の局所整合性検査を通す。

- 欠けた申告は`NO_DATA`、型や原本digestの不一致等は`BLOCKED`
- 各申告が局所整合していて、結果3集合が一致すれば
  `PROPOSAL_ONLY_TWO_DECLARED_PLAN_RESULT_CLAIMS_AGREE`
- 局所整合する二つの申告に差異があれば
  `OBSTRUCTION_TWO_DECLARED_PLAN_RESULT_SETS_DISAGREE`
  として**異なる集合、フィールド名、申告ID・自称issuer名を消さずに保持**
- claim IDが異なることは**独立発行者の証明にならない**
- どの状態も原本PlanOSの未出力結果集合`NO_DATA`を解消しない
- original source kernelの再実行、MemoryOS書込、World変更、
  ActOS実行、GitHub操作をPython監査器は行わない

新規18件の負例を含む実カーネル回帰と、元ファイルのGit blob照合を追加。
公開proof root、Lean原本、固定Lake manifest、既存workflowを一切変更しない。

## 認証と限界

PR側でStrict Lean・`#print axioms`全8宣言・Python Runtime、
公開API・exact-head Governance・source/test-merge Git tree一致を確認する。
別個のcanonical main限定Lean CIはv0.50原本型を直接再ビルド。
局所認証を全体`KuuOSFormal`SUCCESSへ転用しない。

append-only／tighten-only／overwrite-forbidden／same-root。
保護PR #1558 Draft/Open/未マージ。
Preference ⇏ Descent ⇏ Authority。
