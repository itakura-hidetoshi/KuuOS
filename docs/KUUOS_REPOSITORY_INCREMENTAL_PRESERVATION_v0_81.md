# KuuOS Repository Incremental Preservation v0.81

## 目的

v0.81は、v0.80で得たrepository normal-form certificateを、main更新後に局所的に再検証する層です。

毎回すべての候補状態を探索するのではなく、変更された構造scopeだけを再探索します。

```text
前回normal-form certificate
→ 前回scope index
→ 現在scope index
→ digest差分
→ unchanged scope再利用
→ invalidated scope再探索
→ current normal-form preservation certificate
```

外部承認は要求しません。

## scope

scopeは二種類です。

### global scope

次を含みます。

- 累積runtime root
- aggregate Lean root
- lakefile
- opt-in manifest
- 明示inventory内のworkflow

このscopeが変化した場合は、repository全体を再探索します。

### contract scope

各opt-in manifestごとに次を含みます。

- manifest本体
- manifestが参照するruntime、test、validator、documentation
- 累積runtime root
- aggregate Lean root
- lakefile

contract固有のruntimeやtestだけが変化した場合、そのcontract scopeだけを再探索できます。

## fingerprint

各scopeは、member pathごとの存在状態と内容digestからfingerprintを構成します。

```text
scope digest
=
Digest(scope id, scope kind, member paths, member digests)
```

pathの追加、削除、内容変更は区別されます。

## certificate再利用

前回certificateは次を満たす場合だけ使用します。

- 前回snapshot digestへ束縛されている
- 前回scoreが0
- 前回snapshot自身が一意terminal
- 全terminalが固定点
- 決定的経路がterminalと一致

一致しないcertificateは`previous_normal_form_certificate_invalid`として拒否します。

## 増分判定

前回と現在のscope digestが等しいscopeは再利用します。

異なるcontract scopeだけを再探索します。

次の場合は全体再探索へ切り替えます。

- global scopeの変更
- contract scopeの追加
- contract scopeの削除

## preservation条件

増分certificateがnormal form維持を認める条件は次です。

- 前回certificateが有効
- 再利用scopeのdigestが同一
- 再探索scopeが現在snapshotのscore 0固定点
- 現在repository全体のscoreが0
- contract集合が変化していない

全体再探索の場合は、現在snapshot自身がscore 0の一意terminalであることを要求します。

## 変更例

### 無関係path

scopeに属さない文書が変化しても、全scopeを再利用します。

### 単一contract runtime

一つのruntime moduleだけが変化した場合、そのcontractだけを再探索します。

他contractとglobal scopeは再利用します。

### lakefile

lakefileは全contractに共有されるため、全体再探索します。

### workflow

workflow triggerの変更はglobal scopeを変更するため、全体再探索します。

### manifest参照pathの欠落

該当contractだけを再探索し、scoreが正ならnormal form維持を否定します。

## 非主張

v0.81は次を主張しません。

- 内容が同じでdigestが異なるscopeの自動同一視
- 明示inventory外のpathへの完全性
- score 0と真理の同一視
- GitHubへの直接書込み
- 外部承認による正当化
