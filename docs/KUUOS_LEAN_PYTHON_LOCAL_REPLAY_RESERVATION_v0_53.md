# KuuOS Lean→Python v0.53 — 二申告の局所replay台帳と原子追記

Canonical main基点は `e31b4d527267a4c34cb69a0ecc0ed436eae6cfad`。
Lean `v4.30.0-rc2`、mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`を固定する。

## この段階で新たに扱う障害

v0.52は、事前配布された共有鍵とのHMAC-SHA256整合を局所的に
検査した。しかし**別の呼出しで同じMACを再提出しても通過**し、
実行事実・発行者・独立性・因果時刻の証明にはならない。

v0.53は、v0.52の**二つのMAC検証成功**を先行条件として、
呼出側が明示した`pathlib.Path`のSQLiteファイルへ、
二つの観測を単一`BEGIN IMMEDIATE`トランザクションで追記する。
これはもとのPlanOS実装を変更しない**独立した書込層**である。

データベースにはsecretを格納しない。各観測に
key ID、context、sequence、nonce、正準MAC対象のSHA-256、
前行digestと現行digestを保存する。列の`UNIQUE`制約で、
同じkey/context/sequenceおよび同じkey/nonceの再登録を拒否する。
二番目が衝突すれば**第一番目のINSERTもrollback**し、
受理と効果を混同しない。

既存テーブルのschemaを照合し、外部triggerや先行行のchain改変が
あればfail-closed。表に`UPDATE`や`DELETE`を実装しない。
ただしSQLiteは物理的にはページを書き換え、ファイルを保持するOSや
管理者に対する不可変性は**証明しない**。

## 判定

- `NO_DATA`：別途検証鍵や台帳パスがない
- `BLOCKED`：MAC／形式／台帳schema／chain等の不一致
- `LOCAL_ATOMIC_REPLAY_LEDGER_RECORDED_PROPOSAL_ONLY`：二つが
  局所MAC検査に成功し、集合も一致して、新規二観測の書込commitを確認
- `LOCAL_ATOMIC_REPLAY_LEDGER_RECORDED_OBSTRUCTION`：MACは局所
  検査成功だが、来歴／異議／少数意見の差異を**obstructionとして保持**して記録
- `LOCAL_ATOMIC_REPLAY_COLLISION_OBSTRUCTION`：同一ローカル台帳で
  既出のkey/sequenceまたはkey/nonceがあり、追加INSERTをrollback

### 限定事項

台帳パスは検証者が**別途指定する信頼済みローカルディレクトリ**。
発行者の証明ではなく、ファイルの制御とOSの原子トランザクションを
仮定した局所的なreplay防止である。

別ホストの台帳、ファイルのバックアップ復元、秘密鍵の漏洩、
管理者によるDBの置換、再計算された全chainは防がない。
今後、外部に認証済みchain rootや複数管理者の同期がないまま
`globalReplayProtected`をtrueにしてはいけない。

原本PlanOSの3結果Finsetはなお未出力で`NO_DATA`。
外部発行者、世界の時間、証明項`EvidenceMatchesOriginal`、
普遍的Lean↔CPython一致、全OSの降下・ホスト実行権限は未証明。

## 形式証明

固定Mathlibと原本PlanOS型、v0.52 Leanを直接importする。
新規Leanは、有限Finsetモデルで二つのkeyを
既存台帳へ追記する際、freshなら先行情報を保持し、
freshでなければ状態を**変更しない**ことを示す。
LeanはSQLiteの原子性やHMAC安全性を証明しない。

全新規11宣言について`#print axioms`、固定Leanビルド、
原本Git blob照合、Python実カーネル6経路、
SQLiteの再open／並行／rollback／tamperingと原本非変更の回帰、
独立CI・Governance・source/test merge tree一致で認証する。

append-only／tighten-only／overwrite-forbidden／same-root。
保護PR #1558はDraft/Open/未マージ。
Preference ⇏ Descent ⇏ Authority。
