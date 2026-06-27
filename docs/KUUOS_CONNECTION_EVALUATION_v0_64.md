# KuuOS Connection Evaluation v0.64

## 目的

v0.64は、v0.63でreviewされた接続候補を、有限個の`OSGaugeBundle` snapshot上で再評価します。

候補接続をproductionへ適用しません。

各snapshotでは場とsource digestを変更せず、接続だけを候補へ置き換えて比較します。

## 完全束縛

評価は次へ完全に束縛されます。

```text
source bundle
v0.62 proposal
v0.63 admission receipt
selected candidate receipt
candidate connection
rollback target
```

v0.63 receipt自体のdigestも再計算します。

## case評価

各caseで次を検査します。

```text
same gauge group
same connection domain
same fields
same source bindings
candidate curvature does not increase
memory holonomy observables are preserved
```

少なくとも一caseで曲率の厳密減少を要求できます。

## 総合判定

全caseがadmissibleであり、必要な厳密改善が観測された場合だけ、`READY_FOR_CONNECTION_STAGING_REVIEW`を返します。

このstatusもproduction適用許可ではありません。

```text
production apply ready = false
state write performed = false
authority widened = false
```

## Lean形式化

Leanではcase admissibilityと有限評価のsafe predicateを定義します。

safe評価から、全digest binding、staging review限定、production適用否定、state write否定、authority widening否定を導きます。
