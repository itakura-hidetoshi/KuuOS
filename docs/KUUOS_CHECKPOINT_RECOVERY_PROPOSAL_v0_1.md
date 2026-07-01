# KuuOS Checkpoint Recovery Proposal v0.1

## 位置づけ

KuuOS Checkpoint Recovery Proposal v0.1は、完了済みの段階的repository mutation roadmapとは別の、独立した非mutation系列です。

この層はv1.25ではありません。

v1.24から新しいrepository mutation authorityを継承しません。

## 入力

proposalは、受理済みのKuuOS Repository Checkpoint Reflog v1.24 resultをsource evidenceとして受け取ります。

次を完全に再確認します。

- v1.24 result digest。
- v1.24 accepted status。
- v1.21 publicationとv1.23 sandbox reflectionの受入状態。
- repository identity。
- Git-directory fingerprint。
- checkpoint reference namespace。
- checkpoint OID。
- checkpoint reflogの一件性と完全一致。
- object、reference、index、working tree、other reflog、push、signingのeffect accounting。

## proposalの内容

proposalは次を固定します。

- source checkpoint reference。
- source checkpoint OID。
- 比較対象となるtarget reference。
- requestor identity。
- compare-only objective。
- rationale digest。
- proposal time。
- source v1.24 result digest。
- policy digest。

proposalはtarget repository stateをまだ観測しません。

source-target comparisonは後続層です。

## 必須の後続gate

valid proposalは、少なくとも次を要求します。

```text
accepted v1.24 checkpoint evidence
→ recovery proposal
→ independent source-target comparison
→ external review
→ bounded recovery authorization request
→ explicit authorization decision
```

proposal単独では後続段階を省略できません。

## 非権限境界

```text
recovery proposal != source-target comparison
recovery proposal != external review
recovery proposal != authorization request
recovery proposal != authorization decision
recovery proposal != recovery execution
recovery proposal != branch update
recovery proposal != force update
recovery proposal != history rewrite
recovery proposal != remote push
recovery proposal != v1.25 mutation authority
```

この層はGit commandを実行しません。

repositoryを変更しません。

reference、object database、index、working tree、reflog、remote、push、signingへ書き込みません。

## fail-closed条件

次の場合はproposalを`CHECKPOINT_RECOVERY_PROPOSAL_REJECTED`とします。

- v1.24 result digestが一致しない。
- v1.24 resultが受理状態ではない。
- source repository bindingがallowlistと一致しない。
- source checkpoint referenceが`refs/kuuos/checkpoints/`外である。
- target referenceがallowlist外である。
- target referenceがcheckpoint namespaceに属する。
- sourceとtargetが同一である。
- requestorが未承認である。
- objectiveがcompare-onlyではない。
- rationaleが欠落または上限超過である。

rejected proposalは比較、review、authorization、executionへ進みません。

## 決定性

同一のsource result、policy、target、requestor、objective、rationale、proposal timeからは同一proposalを構成します。

proposal digestは完全なproposal payloadから計算します。

改変されたproposalは再計算照合で拒否します。

## 形式境界

Lean moduleは次を型付きで固定します。

- valid proposalがsource evidenceとbindingを要求すること。
- valid proposalがsource-target comparisonを未実行のまま要求すること。
- external reviewとexplicit authorization decisionが必要であること。
- recovery authorityを付与しないこと。
- Git実行とrepository mutationを行わないこと。
- v1.24 mutation系列を継続しないこと。
- 同一入力に対する決定性。

Lean成功は、外部review、制度的承認、live recovery execution、repository復元の正当性を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_checkpoint_recovery_proposal_v0_1

PYTHONPATH=. python3 \
  runtime/kuuos_checkpoint_recovery_proposal_check_v0_1.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSCheckpointRecoveryProposalV0_1
```
