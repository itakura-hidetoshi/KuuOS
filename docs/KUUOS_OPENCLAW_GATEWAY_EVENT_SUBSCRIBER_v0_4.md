# KuuOS OpenClaw Gateway Event Subscriber v0.4

## 位置づけ

v0.3 は `audit.activity.list` を pull し、OpenClaw の metadata-only audit activity を KuuOS の
append-only observation candidate として取り込む durable reconciliation path を作った。

v0.4 は、その上に低遅延 WebSocket observation hint 層を追加する。

```text
OpenClaw Gateway v4 WebSocket
  |  sessions.changed / session.message / session.operation / session.tool / agent
  v
KuuOS Gateway Event Subscriber v0.4
  |  privacy-reduced append-only live hints
  v
ObserveOS owner review
  |  gap / reconnect / bounded uncertainty
  v
v0.3 audit.activity.list reconciliation
  v
verification debt remains explicit
```

最重要の非同値:

```text
live event != durable history
live event != ObserveOS commit
live event != verification
live event != WORLD truth
live event != PlanOS completion
live event != rollback proof
WebSocket silence != non-occurrence proof
```

## Version pin

subscriber は OpenClaw の公開 package を exact pin する。

```text
@openclaw/gateway-client = 2026.8.1
@openclaw/gateway-protocol = 2026.8.1
wire protocol = 4
Node.js >= 22.19.0
```

一般 operator client は current wire version を exact negotiate するため、runtime は package-exported
`PROTOCOL_VERSION` を `minProtocol` と `maxProtocol` の両方に使う。

## Capability boundary

実装する capability だけを宣言する。

```text
SESSION_SCOPED_EVENTS
TOOL_EVENTS
```

capability は authorization ではない。
scope は読み取り専用の

```text
operator.read
```

だけを要求する。

v0.4 は approval resolution、chat send、session mutation、admin operation を行わない。

## Pairing and credential ownership

公開 Gateway client の host-owned device auth contract を使う。

KuuOS subscriber は独立 Ed25519 device identity を生成・保存する。

```text
~/.kuuos/openclaw/gateway-event-device-identity.json
~/.kuuos/openclaw/gateway-event-device-token.json
```

POSIX platform では directory を 0700、identity/token files を 0600 にする。

bootstrap credential は command line に載せない。
必要な場合のみ環境変数を使う。

```text
OPENCLAW_GATEWAY_BOOTSTRAP_TOKEN
OPENCLAW_GATEWAY_PASSWORD
```

初回 pairing が必要な場合は OpenClaw host で

```text
openclaw devices list
openclaw devices approve <requestId>
```

により current request を承認する。Gateway が mint した device token は host callback 経由で KuuOS の
private token file に保存され、scope upgrade は自動では行わない。

## Gateway URL policy

既定:

```text
ws://127.0.0.1:18789
```

URL に userinfo、query、fragment を許さない。
remote Gateway は `--allow-remote-gateway` が明示されたときだけ許可し、その場合も `wss://` を必須にする。
credential を URL に埋め込まない。

## Subscription lifecycle

`onEvent` listener は connection construction 時点で先に設置される。
各 `hello-ok` ごとに connection epoch を 1 増やし、毎回

```text
sessions.subscribe
```

を再発行する。これは reconnect 後に subscription が失われる OpenClaw contract に対応する。

明示された `--session-key` についてのみ

```text
sessions.messages.subscribe { key }
```

を再発行する。

任意 session の transcript subscription は自動発見・自動拡大しない。
`includeApprovals` も要求しない。

`sessions.subscribe` の snapshot 内容は保存せず row count だけを receipt に残す。
subscription activation と snapshot read の race では live event の方が新しい可能性があるため、snapshot を
live event に対する truth replacement として扱わない。

## Privacy projection

live events は audit ledger と異なり transcript content を含み得る。
したがって raw payload を一切 persist しない。

保存するのは allowlisted scalar metadata と identity digest のみ。

```text
runId
agentId
toolCallId
toolName
status
phase
action
kind
operationId
operation
reasonCode
errorCode
channel
direction
hasActiveRun
run seq / source timestamp
sessionKeyDigest
sessionIdDigest
activeRunIdDigests
payload top-level key names
content-field-presence flags
```

以下の値は保存しない。

```text
message body
messages
text / deltaText
content
prompt
tool args
result / output
raw error text
raw sessionKey / sessionId
raw hello snapshot
bootstrap token / password / device token
```

## Live hint ledger

既定:

```text
~/.kuuos/openclaw/gateway-event-hints.jsonl
```

record は append-only SHA-256 receipt を持つ。
主な record type:

```text
openclaw_gateway_event_hint
openclaw_gateway_connection_hello
openclaw_gateway_session_roster_subscribed
openclaw_gateway_session_messages_subscribed
openclaw_gateway_connection_sequence_gap
openclaw_gateway_run_sequence_gap
openclaw_gateway_connection_closed
openclaw_gateway_connect_error
openclaw_gateway_reconnect_paused
openclaw_gateway_subscription_error
```

全 live hint は

```text
lowLatencyHint = true
durableHistoryAuthority = false
auditReconciliationRequired = true
observeCommitPerformed = false
verificationCreated = false
worldCommitAuthority = false
truthPromotionAuthority = false
automaticPlanCompletion = false
automaticRollback = false
memoryOverwriteAuthority = false
```

を保持する。

## Sequence semantics

### outer WebSocket seq

outer event frame の `seq` は current connection 内だけの ordering であり reconnect で reset する。
subscriber は OpenClaw reference client の `onGap` callback を使い、gap を検出すると

```text
openclaw_gateway_connection_sequence_gap
+ auditReconciliationRequired = true
```

を記録する。

connection epoch を跨いで outer seq を比較しない。

### agent per-run seq

`agent` event payload の `seq` は run ごとの ordering である。
subscriber は run ごとの最高 seq を保持する。

```text
seq <= previous
  -> duplicate / stale hint として無視

seq > previous + 1
  -> run sequence gap receipt
  -> audit reconciliation required
```

run gap は WORLD divergence の証明ではない。

## sessions.changed semantics

`sessions.changed` の omission を field deletion と解釈しない。
OpenClaw contract 上、一部 event は invalidation signal にすぎないため、v0.4 は payload の complete session row を
構築しない。

`hasActiveRun` や exact active run ids が存在する場合だけ、その存在を hint として保存する。

## v0.3 reconciliation ownership

v0.4 は audit intake を置き換えない。

```text
WebSocket event = low-latency hint
v0.3 audit.activity.list = bounded reconciliation source
ObserveOS review = observation ownership
VerifyOS = verification ownership
WORLD = truth/update ownership
```

outer gap、run gap、reconnect、subscription error がなくても、live hint 自体は durable history authority を持たないため
`auditReconciliationRequired = true` を維持する。

## Usage

依存を exact install:

```bash
cd integrations/openclaw/event-stream
npm install
```

local Gateway:

```bash
node subscriber.mjs
```

特定 session の message / operation / tool hints も購読:

```bash
node subscriber.mjs --session-key agent:main:main
```

複数 session:

```bash
node subscriber.mjs \
  --session-key agent:main:main \
  --session-key agent:research:main
```

remote Gateway は明示かつ TLS 必須:

```bash
OPENCLAW_GATEWAY_URL=wss://gateway.example \
node subscriber.mjs --allow-remote-gateway
```

## Validation

```text
python3 scripts/check_openclaw_gateway_event_subscriber_v0_4.py
node integrations/openclaw/event-stream/test_projection.mjs
```

Lean boundary:

```text
formal/KUOS/ObserveOS/OpenClawGatewayEventHintV0_4.lean
```

## Honest classification

```text
low-latency, privacy-reduced, reconnect-aware OpenClaw Gateway event hint layer,
with exact package/wire pins and explicit audit reconciliation debt,
but with no durable-history, ObserveOS-commit, verification, WORLD-truth,
PlanOS-completion, rollback-proof, memory-overwrite, or silence/non-occurrence authority
```
