# KuuOS MemoryOS Qi-WORLD Validation and Release Matrix v0.36

## 目的

v0.36 は、v0.35 の MemoryOS Qi-WORLD Blocker Integration に対する検証意味を固定する。

新しい MemoryOS 権限、Blocker discharge 権限、WORLD commit 権限、truth authority、execution authority は追加しない。

対象は次の統合である。

```text
Qi Process Tensor history
+ Qi-WORLD Cross-Cycle Blocker Theory v1.5
+ Authorized Atomic WORLD Store v0.34
→ MemoryOS Qi-WORLD Blocker Integration v0.35
```

v0.36 は、各検証が何を保証し、何を保証しないかを文書、manifest、validator、unit test、CI workflow、central runtime full check に固定する。

## 構成行列

| component | version | source files | manifest | validator | tests | Lean module | formal root | workflow |
|---|---|---|---|---|---|---|---|---|
| MemoryOS Qi-WORLD Blocker Integration | v0.35 | `runtime/kuuos_memoryos_qi_world_blocker_integration_v0_35.py` | `manifests/kuuos_memoryos_qi_world_blocker_integration_v0_35.json` | `scripts/check_memoryos_qi_world_blocker_integration_v0_35.py` | `tests/test_memoryos_qi_world_blocker_integration_v0_35.py` | `KUOS.OpenHorizon.MemoryOSQiWorldBlockerIntegrationKernelV0_35` | `formal/KUOS.lean` | `memoryos-qi-world-blocker-integration-v0-35.yml` |
| Validation and Release Matrix | v0.36 | v0.35 の全対象 | `manifests/kuuos_memoryos_qi_world_validation_matrix_v0_36.json` | `scripts/check_memoryos_qi_world_validation_matrix_v0_36.py` | `tests/test_memoryos_qi_world_validation_matrix_v0_36.py` | v0.35 の既存定理を参照 | v0.35 の登録を検査 | `memoryos-qi-world-validation-matrix-v0-36.yml` |

## 検証層

### Static registration

次を検査する。

- v0.35 の runtime、manifest、validator、tests、documentation、Lean module、formal root、workflow が存在する。
- fail-closed boundary を示す固定語が残る。
- v0.35 の形式定理が formal root に登録される。

成功は、登録面と固定境界が存在することを意味する。

成功は、runtime behavior の完全性、経験的真理、実行許可を意味しない。

### Runtime unit regression

次を検査する。

- structurally exact inactive blocker evidence は quarantine される。
- structural blocker corruption は reject される。
- blocked capability inventory mismatch は reject される。
- WORLD generation と fragment の append-only 条件が保たれる。
- snapshot tampering は検出される。

成功は、宣言された回帰例が通ることを意味する。

成功は、将来の全入力が安全であること、blocker が discharge されたこと、WORLD state が真であることを意味しない。

### Upstream source validation

次の upstream validator を実行する。

```text
v0.23 Non-Markov Cognitive Loop
v1.5 Qi-WORLD Cross-Cycle Blocker Theory
v0.34 Authorized Atomic WORLD Commit
```

成功は、v0.35 が参照する source contract の登録整合性を意味する。

成功は、source evidence の経験的正しさ、cross-cycle authority、MemoryOS による WORLD mutation を意味しない。

### Lean typed boundary

次を strict build する。

```text
KUOS.OpenHorizon.MemoryOSQiWorldBlockerIntegrationKernelV0_35
KuuOSFormal
```

成功は、typed non-authority boundary が `sorry` なしでコンパイルされることを意味する。

成功は、経験的真理、制度的 authorization、物理的 persistence を証明しない。

### Central runtime regression

v0.36 checker を現行の `run_kuuos_runtime_full_check_v0_48.py` に登録する。

成功は、現在の central regression chain が v0.36 matrix と v0.35 integration を受理することを意味する。

成功は、truth、execution permission、blocker discharge を意味しない。

## Failure classes

v0.36 は少なくとも次を可視化する。

- stale digest
- replay duplication
- substituted source packet
- blocker certificate structural error
- inactive blocker evidence
- blocked capability inventory mismatch
- memory root overwrite attempt
- WORLD store identity change
- WORLD root lineage change
- WORLD generation regression
- WORLD fragment change without generation
- authority promotion from validation
- test fixture inventory inconsistency

未知の failure は fail closed とする。

## 旧 unit-test log の分類

初期の失敗ログには、`complete=False` fixture が内部的に矛盾した blocker inventory を生成し、`blocker_inventory_mismatch` で停止した例がある。

これは現行 v0.35 runtime の回帰ではない。

原因は、fixture が全 blocker を inactive のまま残しながら、missing blocker として `world_identity_blocker` だけを申告したことである。

現行 test は、全 blocker を active に初期化し、`world_identity_blocker` だけを inactive にする。

したがって、この旧ログは次に分類する。

```text
TEST_FIXTURE_INCONSISTENCY
current runtime regression = false
```

旧ログの存在だけから blocker quarantine の失敗を再宣言しない。

## Proof status

```text
runtime behavior
  = runtime-validated over declared regression cases

formal boundary
  = Lean-derived typed boundary

source evidence
  = validator-checked supplied artifacts

empirical truth
  = not established

physical persistence
  = not established
```

## Non-authority boundary

```text
CI pass ≠ truth
CI pass ≠ execution permission
CI pass ≠ blocker discharge
validation matrix ≠ WORLD commit authority
validation matrix ≠ memory overwrite authority
validation matrix ≠ plan activation
validation matrix ≠ ActOS invocation
```

## Validation

```bash
PYTHONPATH=. python scripts/check_memoryos_qi_world_validation_matrix_v0_36.py
PYTHONPATH=. python -m unittest -v \
  tests.test_memoryos_qi_world_validation_matrix_v0_36

PYTHONPATH=. python scripts/check_memoryos_qi_world_blocker_integration_v0_35.py
PYTHONPATH=. python -m unittest -v \
  tests.test_memoryos_qi_world_blocker_integration_v0_35

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.MemoryOSQiWorldBlockerIntegrationKernelV0_35

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

## Honest classification

```text
machine-readable validation and release matrix for
MemoryOS Qi process history, contextual blocker evidence,
and sourced WORLD generations,
with explicit pass meanings, explicit nonclaims,
known regression classification, and no authority escalation
```
