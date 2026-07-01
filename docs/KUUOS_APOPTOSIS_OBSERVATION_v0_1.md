# KuuOS Apoptosis Observation v0.1

## 位置づけ

KuuOS Apoptosis Observation v0.1は、自己組織化系の生命周期を観測する独立した非mutation系列です。

この層は終結候補を発行しません。

権限失効、quiescence、terminal transition、tombstone、物理削除を実行しません。

## 定義

KuuOSにおけるアポトーシスは、役割を終えた構成要素について、依存関係、権限、証拠、保護状態を確認した後、独立したreviewとauthorizationを経て終結状態へ移行させる統治過程です。

単純な削除とは異なります。

```text
apoptosis != rollback
apoptosis != garbage collection
apoptosis != autophagy
apoptosis != quarantine
apoptosis != revocation
apoptosis != punishment
```

rollbackは以前の状態への復帰を扱います。

garbage collectionは到達不能資源の回収を扱います。

autophagyは内部要素の分解と再利用を扱います。

quarantineは隔離を扱います。

revocationは権限の失効を扱います。

apoptosisは構成単位の生命周期の終結を扱います。

## 対象

v0.1は次のsubject kindを扱います。

- module。
- agent。
- memory lineage。
- authority lineage。
- checkpoint。

subject kindの許可はpolicy allowlistで固定します。

## 入力証拠

観測入力は次を束縛します。

- subject identityとversion。
- provenance digest。
- dependency snapshot digest。
- authority snapshot digest。
- usage evidence digest。
- risk evidence digest。
- replacement evidence digest。
- evidence capture timeとobservation time。
- active dependency count。
- active authority count。
- active execution count。
- unresolved incident count。
- repeated failure count。
- inactivity duration。
- replacement verification。
- constitutional protection。
- institutional hold。

入力はdigestで完全に固定します。

## 劣化signal

v0.1は次を劣化signalとして分類します。

- verified replacement。
- policy threshold以上の反復失敗。
- policy threshold以上の長期不活動。
- 未解決incident。

signalは終結理由の確定ではありません。

```text
degradation signal != apoptosis candidate
observation != external review
observation != authorization
observation != execution
```

## 観測結果

結果は四状態です。

### `APOPTOSIS_OBSERVATION_NO_ACTION`

証拠が有効であり、保護対象ではなく、劣化signalがありません。

### `APOPTOSIS_OBSERVATION_REVIEW_RECOMMENDED`

証拠が有効であり、保護対象ではなく、一つ以上の劣化signalがあります。

この状態は次の独立gateを要求します。

```text
apoptosis observation
→ independent apoptosis candidate
→ dependency review
→ authority review
→ quiescence review
→ external review
→ bounded authorization request
→ explicit authorization decision
```

### `APOPTOSIS_OBSERVATION_PROTECTED`

subjectがconstitutional protected core、policy protected subject、またはinstitutional holdの対象です。

この状態は通常のapoptosis系列へ進みません。

protected coreの変更には独立したconstitutional amendmentが必要です。

### `APOPTOSIS_OBSERVATION_REJECTED`

policy、input digest、evidence freshness、evidence completeness、provenance、snapshot、subject kindのいずれかが不正です。

rejected observationは後続gateへ進みません。

## 非権限境界

```text
apoptosis observation != apoptosis candidate
apoptosis candidate != apoptosis authorization
apoptosis authorization != apoptosis execution
apoptosis execution != audit erasure
module termination != constitutional deletion
agent termination != evidence deletion
authority revocation != history rewrite
tombstone != physical deletion
```

v0.1では次が常にfalseです。

- apoptosis candidate issuance。
- authority revocation。
- quiescence transition。
- terminal transition。
- tombstone write。
- physical deletion。
- live Git execution。
- repository mutation。

## Protected core

少なくとも次はprotected subjectとして扱う必要があります。

- safety constitution。
- authority separation。
- audit log。
- provenance record。
- tombstone registry。
- external review requirement。
- apoptosis governance constraints。
- minimum recovery and appeal path。

protected subjectの一覧はpolicy digestへ含めます。

## 決定性

同一のinputとpolicyからは同一recordを構成します。

record digestは完全なrecord payloadから計算します。

改変されたrecordは再計算照合で拒否します。

## 形式境界

Lean moduleは次を型付きで固定します。

- review recommendationが独立した後続gateを要求すること。
- review recommendationがcandidateを発行しないこと。
- authority revocation、quiescence、terminal transition、tombstone、physical deletionを実行しないこと。
- protected subjectが通常のapoptosisへ進まないこと。
- valid observationがlive Git executionとrepository mutationを行わないこと。
- 同一入力に対する決定性。

Lean成功は、特定subjectの終結必要性、制度的承認、法的削除権限、live executionの安全性を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_observation_v0_1

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_observation_check_v0_1.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisObservationV0_1.lean
```
