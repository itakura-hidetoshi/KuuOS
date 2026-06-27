# KuuOS Connection Staging Package v0.65

## 目的

v0.65は、v0.64で有限評価を通過した接続候補を、不変のstaging packageへ封印します。

packageは接続を適用しません。

候補接続のpayloadと、候補を支えるdigest鎖を一つのreceiptへ固定します。

## 完全束縛

packageは次へ束縛されます。

```text
source bundle
v0.62 proposal
v0.63 admission receipt
v0.64 evaluation receipt
selected candidate receipt
candidate connection
rollback target
```

admission receiptとevaluation receiptは、package生成時に自己digestを再計算します。

candidate connection payloadも再計算し、selected candidate digestと一致させます。

rollback targetはsource bundle digestと一致しなければなりません。

## namespace

staging namespaceは`shadow/`で始まる必要があります。

`production/`その他のnamespaceはreadyになりません。

## package境界

ready packageは次を固定します。

```text
immutable envelope
candidate only
production apply allowed = false
state write allowed = false
authority widening allowed = false
```

Pythonのfrozen dataclassだけで深い不変性を主張しません。

内容の完全性はpackage digestとcandidate payload digestの再検証によって保証します。

## 検証経路

専用validatorは次を検査します。

```text
valid shadow package
non-shadow namespace rejection
payload tamper detection
rejected review cannot produce a ready package
```

## Lean形式化

Leanではpackage digest、source、proposal、admission、evaluation、candidate、rollbackのbindingを命題として保持します。

valid packageから、digest鎖の保存とshadow-only境界を導きます。
