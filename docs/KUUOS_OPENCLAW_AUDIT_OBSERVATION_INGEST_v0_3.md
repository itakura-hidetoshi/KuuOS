# KuuOS OpenClaw Audit Observation Intake v0.3

## 位置づけ

v0.1 は OpenClaw の個別 tool call を KuuOS / ActOS の preflight gate に通した。
v0.2 は KuuOS から OpenClaw Gateway の run start / wait / abort / session observation を行う active controller を追加した。

v0.3 は閉ループの観測側を追加する。

```text
DecisionOS / PlanOS
        |
        v
      ActOS
        |
        v
KuuOS Gateway Controller v0.2
        |
        v
 OpenClaw Gateway / agent loop
        |
        +--> before_tool_call --> KuuOS Control Bridge v0.1
        |
        v
 audit.activity.list
        |
        v
KuuOS Audit Observation Intake v0.3
        |
        v
ObserveOS owner review / verification debt
        |
        v
MemoryOS-compatible append-only candidate lineage
```

OpenClaw は引き続き execution host であり、WORLD truth、ObserveOS commit、PlanOS completion、
rollback proof の authority ではない。

## Source boundary

v0.3 は OpenClaw Gateway の公式 `audit.activity.list` RPC のみを source とする。

```text
openclaw gateway call audit.activity.list --params <json> --json
```

この RPC は `operator.read` を要求し、結果は newest-first の metadata-only activity ledger である。
対象は次の lifecycle metadata。

```text
agent_run
tool_action
inbound_message
outbound_message
```

v0.3 は source を lossless compliance archive とみなさない。

```text
audit ledger = best effort
retention is bounded
absence of row != proof that no action occurred
```

したがって OpenClaw audit の欠落を WORLD の非発生証明、rollback 証明、verification 結果として使わない。

## Privacy-preserving projection

OpenClaw audit ledger 自体は prompt、message body、tool arguments、tool results、raw error text を持たない。
v0.3 はさらに future schema drift に対して fail-closed とし、`redaction = metadata_only` を必須にする。

保存対象は allowlist projection のみ。

```text
eventType
schemaVersion
eventId
sequence
sourceSequence
occurredAt
kind
action
status
redaction
agentId
runId
toolCallId
toolName
errorCode
direction
channel
conversationKind
outcome
deliveryKind
failureStage
durationMs
resultCount
reasonCode
```

`actor` は raw 値を保存せず digest 化する。
run/tool の `sessionKey` と `sessionId` も raw 値を保存せず digest 化する。
これは session key が platform account / peer identity を含み得るためである。

各 local candidate は元 event 全体の `sourceEventDigest` を保持するが、元 event 本文を複製しない。

## ObserveOS boundary

v0.3 の append-only record は

```text
openclaw_audit_observation_candidate
```

であり、ObserveOS の committed observation record ではない。

固定する非同値は次。

```text
OpenClaw audit row != ObserveOS commit
OpenClaw status succeeded != verification
OpenClaw status succeeded != PlanOS completion
OpenClaw failed/cancelled/timed_out != rollback proof
OpenClaw audit absence != non-occurrence proof
local candidate receipt != WORLD truth
local candidate receipt != memory overwrite authority
```

各 candidate は次を明示する。

```text
metadataOnly = true
bestEffortSource = true
observeOwnerReviewRequired = true
observeCommitPerformed = false
verificationRequired = true
verificationCreated = false
worldCommitAuthority = false
truthPromotionAuthority = false
planCompletionAuthority = false
automaticPlanCompletion = false
rollbackProofAuthority = false
automaticRollback = false
absenceProvesNonOccurrence = false
memoryOverwriteAuthority = false
```

## Append-only candidate ledger

既定:

```text
~/.kuuos/openclaw/audit-observation-candidates.jsonl
```

各 record は canonical JSON の SHA-256 digest と record id を持つ。
既存 candidate ledger が壊れている場合は silent skip せず fail-closed する。

`eventId` を stable dedup key として使う。

## Bounded pagination checkpoint

checkpoint:

```text
~/.kuuos/openclaw/audit-ingest-checkpoints.json
```

filter set ごとに digest key を分ける。

```text
maxSequence
resumeCursor
catchupHighWaterSequence
lastCompletedAtUnixNs
```

重要なのは、bounded poll が page budget に達したとき `maxSequence` を先へ進めないこと。

```text
partial pagination window
  -> resumeCursor を保存
  -> maxSequence は旧値を保持
  -> 次回同じ filter で cursor から再開

previous checkpoint 到達 or source exhausted
  -> catchup complete
  -> high-water sequence を maxSequence に commit
```

この checkpoint commit は ingest progress の局所状態であり WORLD commit ではない。

catch-up 中に新しい OpenClaw events が追加されても、
catch-up 開始時 high-water より新しい sequence は checkpoint 完了後の次回 top poll で取得される。

`--restart-catchup` はその filter set の pagination cursor だけを破棄して newest から再走査する。
既に保存した candidate は eventId dedup により再追加されない。

## Query filters

v0.3 は OpenClaw `audit.activity.list` の bounded filters を渡せる。

```text
--agent-id
--session-key
--run-id
--kind agent_run|tool_action|message
--status started|succeeded|failed|cancelled|timed_out|blocked|unknown
--direction inbound|outbound
--channel
--after-ms
--before-ms
--limit 1..500
--max-pages 1..200
```

`direction` / `channel` は message query にのみ意味がある。

filter の raw `sessionKey` は OpenClaw RPC 送信にだけ使い、checkpoint には raw 値を保存しない。
checkpoint key は canonical filter object の digest である。

## Usage

全 audit activity を同期する。

```bash
python3 runtime/kuuos_openclaw_audit_observation_ingest_v0_3.py sync
```

特定 run の metadata を同期する。

```bash
python3 runtime/kuuos_openclaw_audit_observation_ingest_v0_3.py \
  sync \
  --run-id <RUN_ID>
```

tool action のみ同期する。

```bash
python3 runtime/kuuos_openclaw_audit_observation_ingest_v0_3.py \
  sync \
  --kind tool_action
```

local state のみ確認する。

```bash
python3 runtime/kuuos_openclaw_audit_observation_ingest_v0_3.py status
```

bounded poll が incomplete の場合、出力は

```text
completedWindow = false
resumeRequired = true
resumeCursorStored = true
```

となる。同じ filter で再実行して catch-up を続ける。

## Validation

focused validator:

```bash
python3 scripts/check_openclaw_audit_observation_ingest_v0_3.py
```

unit tests:

```bash
python3 tests/test_openclaw_audit_observation_ingest_v0_3.py
```

Lean boundary:

```text
formal/KUOS/ObserveOS/OpenClawAuditObservationIntakeV0_3.lean
```

formal boundary は次を固定する。

```text
metadata-only source
best-effort source
absence is not non-occurrence proof
candidate is not ObserveOS commit
verification is not created
OpenClaw host status grants no WORLD truth
OpenClaw host status grants no PlanOS completion
OpenClaw host status grants no rollback proof
MemoryOS overwrite authority is not granted
```

## Honest classification

```text
bounded, metadata-only, append-only OpenClaw audit intake for ObserveOS owner review,
with privacy-reduced identity projection and resumable sequence/cursor catch-up,
but with no ObserveOS commit, verification result, WORLD truth promotion,
PlanOS completion, rollback proof, memory overwrite, or non-occurrence proof authority
```

## Frontier

v0.3 は stable pull-based ingestion を完成させる。

次段階 v0.4 では OpenClaw Gateway v4 の persistent WebSocket event subscription を追加し、
`session.message` / `session.operation` / `session.tool` / `sessions.changed` を low-latency observation hint
として扱える。ただし event stream は audit ledger の代替 authority とせず、v0.3 の audit catch-up を
durable reconciliation path として残す。
