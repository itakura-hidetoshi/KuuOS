# KuuOS Connection Improvement Candidate v0.62

## 目的

v0.62は、v0.61で固定したObserveOS、VerifyOS、MemoryOS間の接続について、有限個の置換候補を評価します。

出力は接続更新の候補だけです。

source bundle、OS場、ledger、MemoryOS capsuleは変更しません。

## 候補評価

候補接続は次を満たす必要があります。

```text
connection domain preserved
gauge group preserved
OS fields preserved
source digests preserved
changed-link budget respected
total OS curvature nonincreasing
protected memory-holonomy observables preserved
rollback digest bound to source bundle
candidate only
no state write
```

設定により、曲率の厳密な減少も要求できます。

## 保護するホロノミー観測量

ObserveOSからVerifyOS、MemoryOSを経てObserveOSへ戻る閉路について、次を保存します。

```text
Wilson observable
holonomy defect
memory-channel return energy
```

これはホロノミー元そのものの完全な共役類分類を主張しません。

## 有限探索

各有向接続には、外部から有限replacement catalogを与えます。

source接続も各候補集合へ自動的に含めます。

全直積の大きさには上限を置きます。

admissibleな候補は、次の辞書式順序で選択します。

```text
minimum total OS curvature
minimum changed-link count
minimum canonical connection digest
```

admissibleな候補が存在しない場合は、`PRESERVE_SOURCE_CONNECTION`を返します。

## 具体例

二つの接続が同じチャネル内置換を持つ場合、その積が恒等になることがあります。

```text
U_OV = s
U_VM = s
U_MO = 1
s² = 1
```

このとき閉路ホロノミーは恒等のままです。

両接続を恒等へ置き換えることで、ObserveOSからVerifyOSへの認識残差と、VerifyOSからMemoryOSへの検証残差を同時に下げられる場合があります。

この候補も直接適用せず、receiptとして返します。

## Lean形式化

Leanでは接続候補に次を保持します。

```text
source curvature
candidate curvature
source holonomy
candidate holonomy
fixed-domain propositions
rollback proposition
candidate-only proposition
no-state-write proposition
```

admissibilityは曲率非増大、ホロノミー一致、全境界命題から構成します。

また、曲率とホロノミーがゲージ不変観測量なら、sourceとcandidateを同じ局所ゲージ変換で移した後も、曲率順序とホロノミー一致が保存されることを証明します。

## 検証状態

Python runtime、境界試験、manifest、専用Lean rootは成功しています。

同一headに対する通常のstrict formal validationでも、全形式面のcompileが成功しています。

## 非主張

v0.62は接続の自動配備を行いません。

曲率ゼロをtruthと同一視しません。

連続主束上の最適化や完全なホロノミー共役類分類を主張しません。
