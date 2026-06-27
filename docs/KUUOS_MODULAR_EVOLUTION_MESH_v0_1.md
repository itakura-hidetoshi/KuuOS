# KuuOS Modular Evolution Mesh v0.1

## 状態

この段階は、空OSを型付き能力モジュールの依存グラフとして構成するための非実行基盤です。

既存runtimeの挙動、権限、状態、effect経路は変更しません。

自己組織化候補の生成、自己変更の自動承認、production配備は行いません。

## 目的

現在の空OSは、ObserveOS、VerifyOS、MemoryOSなどの意味論的な所有権分離を持っています。

一方で、実装は版番号付きPythonファイル、validator、manifest、Lean rootが個別に増える構造です。

v0.1は、意味論上の分離を実装上のモジュール契約へ写像します。

```text
fixed constitutional boundary
→ typed module contract
→ capability registry
→ dependency graph
→ append-only composition receipt
```

## 追加した基盤

### Module Contract

各モジュールは次を宣言します。

- 一意なmodule IDとversion。
- 主能力と提供能力。
- 必要能力。
- 所有する状態。
- 所有してはならない状態。
- 購読eventと生成event。
- authority surface。
- validator。
- rollback target。
- 文書とformal module。

contract検証は、protected ownership、所有権矛盾、authority surface違反、active providerの曖昧性をfail closedで拒否します。

### Capability Registry

registryはmanifest directoryからmodule contractを読み込みます。

同一内容の再登録は冪等replayとして扱います。

同一module IDを異なる内容で再登録する操作は拒否します。

同じ能力に複数のactive providerが存在する状態も拒否します。

registryへの登録は実行権限を付与しません。

### Dependency Graph

resolverは要求能力から必要moduleを再帰的に解決します。

不足能力と循環依存はfail closedで拒否します。

v0.1の登録構成では次の順序を自動生成します。

```text
ObserveOS
→ VerifyOS
→ MemoryOS
```

依存解決はモジュールを実行せず、現在policyを変更しません。

### Append-only Ledger

共通ledgerはJSONL event、sequence、predecessor digest、event digestを保持します。

同じevent IDと同じ内容の再投入は冪等replayになります。

同じevent IDを異なる内容で再利用する操作は拒否します。

期待headと実際headが異なる更新はstale-stateとして拒否します。

hash chainの改ざんも検出します。

ledger eventは真理権限、検証権限、実行権限を持ちません。

## 初期登録モジュール

### ObserveOS

ObserveOSは`observation.candidate`と`observation.receipt`を提供します。

観測証拠を所有しますが、検証結果、実行license、WORLD真理、現在cycleのpolicy activationを所有しません。

### VerifyOS

VerifyOSは`verification.disposition`と`verification.receipt`を提供します。

検証結果を所有しますが、実行license、effect実行、WORLD真理、現在cycleのpolicy activationを所有しません。

### MemoryOS

MemoryOSは`memory.retrieval`と`memory.lineage`を提供します。

記憶系譜を所有しますが、状態変更、検証結果、実行license、WORLD真理、現在cycleのpolicy activationを所有しません。

## 形式化境界

Lean module `KUOS.Modular.CapabilityContractV0_1`は、authority surfaceと最小module contractを定義します。

次を直接証明します。

```text
registry discovery does not grant self-license
candidate-only module does not gain execution authority
candidate-only module does not gain truth authority
candidate-only module does not activate present-cycle policy
read-only module does not mutate present-cycle policy
```

この形式化は、Python runtimeの全挙動、外部effect、自己改良の有効性を証明しません。

## 検証

```bash
PYTHONPATH=src:. python3 scripts/check_modular_evolution_mesh_v0_1.py
PYTHONPATH=src:. python3 -m unittest -v tests.test_modular_evolution_mesh_v0_1
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSModularEvolutionMeshV0_1
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

## 非権限境界

```text
module discovery != activation
registration != execution license
dependency resolution != effect execution
ledger receipt != truth
shadow candidate != active implementation
learning delta != present-cycle mutation
self-organization proposal != self-modification authorization
```

## 次段階

次段階では、既存ObserveOS、VerifyOS、MemoryOSを直接importする上位経路を、互換adapterを介したcapability lookupへ段階的に置換します。

置換前後の出力はshadow comparisonで比較します。

現行経路は比較期間中も正本として維持します。

構成変更候補は、既存のGoverned Self-Modification Gate v0.26へ渡し、sandbox、regression、formal checks、bounded canary、rollback境界を通過した場合だけ昇格候補になります。
