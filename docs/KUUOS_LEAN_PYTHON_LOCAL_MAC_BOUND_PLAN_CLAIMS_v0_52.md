# Lean→Python v0.52 — 共有鍵MACとPlanOS補助証拠の真正性境界

Canonical base: `c31c0fcf6a010c6c01ce4a6e8ad832ba409c5d0a`.
固定Lean `v4.30.0-rc2`、
mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

## 条件分離

原本PlanOS v1.03のPython証明書に、3つの結果集合
（来歴・異議・少数意見）は個別のフィールドとして出力されない。
v0.51は二つの申告証拠の一致・矛盾を保持し、原本Leanへの一致証明を
申告の一致から導かない。

v0.52で初めて、**受信証拠以外から検証者が事前に供給した共有秘密鍵**
に対するHMAC-SHA256検証をPython標準ライブラリで実装する。
鍵はユーザー申告や受信レコードから読み出さない。タグ入力を
domain／schema／slot／鍵ID／context／sequence／nonce／申告内容の
完全正準JSONに束縛し、`hmac.compare_digest`で検証する。

ここで確認できるのは、**検証者が指定した鍵に対する局所的なMAC整合**のみ。
HMACは共通鍵方式であり、誰が発行したかの非否認証明ではない。
事前配置した鍵そのものの真正性は、この関数では証明できない。
二つの異なる鍵IDであっても、独立した二主体の存在は証明されない。

## 三つの権威境界

1. **MAC検証の成功**：鍵と完全な入力バイト列の局所整合。鍵ID、
   context、sequenceは検証者が別途与える。同一pairのnonce重複や、
   異なる鍵IDの不在はfail-closed
2. **二申告集合の一致**：v0.51の局所投影。矛盾は全フィールドとともに
   obstructionとして保存し、MAC成功による上書きを禁止
3. **原本との一致**：v0.50の`EvidenceMatchesOriginal`という独立の
   Lean証明が必要。MAC検証から自動構成されない

Python判定は欠落 `NO_DATA`、無効 `BLOCKED`、局所MAC検査成功の
一致 `MAC_CHECKED_LOCAL_AGREEMENT_PROPOSAL_ONLY`、
局所MAC検査成功の矛盾 `MAC_CHECKED_LOCAL_DISAGREEMENT_OBSTRUCTION`。
すべての結果で元PlanOS出力の3集合は`NO_DATA`のまま。

## 未認証事項

- HMAC-SHA256の暗号学的安全性をLeanで証明したわけではない
- 鍵の供給経路、発行者の独立性、nonce・sequenceの世界横断的な
  再利用禁止、replayの継続記録は未確認
- 現行実装では同一証拠を別の関数呼び出しへ再提出できる。
  これはテストで確認しており、falseなreplay protectionを主張しない
- 原本PlanOSの実行事実、過去の因果履歴、外部発行主体の認証、
  Lean↔Python普遍的意味論、全OSの大域降下、ホスト実行権限は未証明

## 独立検証

原本Lean型とv0.51の証明を直接importし、形式側ではMAC成功報告の
Boolに権限を与えず、元証明書の一致条件下の結論だけを証明。
新規Lean5宣言の`#print axioms`、固定Strict Lean、
GitHub原本blobの静的固定照合、元カーネル6経路、MAC正負例と
read-only、累積Runtime、公開API、Exact-head Governance、test-merge
Git tree一致、統合後の独立push CIを実際に確認する。

既存の原本Lean・Python・Lake・107公開proof rootsは書換禁止。
保護PR #1558はDraft/Open／未マージ。全体KuuOSFormalとの
局所認証の非同一性を保つ。

append-only／tighten-only／overwrite-forbidden／same-root。
Preference ⇏ Descent ⇏ Authority。
