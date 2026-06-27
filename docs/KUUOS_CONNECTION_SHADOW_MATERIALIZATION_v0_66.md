# KuuOS Connection Shadow Materialization v0.66

## 目的

v0.66は、v0.65の封印packageを、メモリ上のshadow bundleとして具体化します。

source bundleへ接続を書き込みません。

候補接続を持つ新しい`OSGaugeBundle`を構成し、source bundleの前後digestが一致することを確認します。

## 入力束縛

shadow materializationは次を再検証します。

```text
v0.65 package digest
source bundle digest
v0.62 proposal digest
selected candidate receipt
candidate connection payload
rollback source digest
shadow namespace
```

package内のcandidate payloadと、proposalが保持するcandidate connectionは同一digestでなければなりません。

## shadow検証

具体化したshadow bundleについて次を確認します。

```text
same gauge group
same connection domain
same fields
same source bindings
curvature does not increase
memory holonomy observables are preserved
```

## source不変性

source bundleの具体化前後digestを比較します。

一致した場合だけ`source_unchanged`をtrueにします。

rollback witnessは、packageのrollback digestが具体化前source bundle digestと一致し、sourceが不変である場合だけreadyになります。

## 固定境界

```text
shadow only
production apply ready = false
state write performed = false
authority widened = false
```

## 検証経路

専用validatorは次を検査します。

```text
valid shadow materialization
package tamper rejection
rejected review cannot materialize a shadow
```

## Lean形式化

Leanではpackage binding、candidate binding、rollback witness、source不変性、曲率非増大、記憶ホロノミー保存を命題として保持します。

valid shadow receiptから、source保存、観測量保存、isolated境界を導きます。
