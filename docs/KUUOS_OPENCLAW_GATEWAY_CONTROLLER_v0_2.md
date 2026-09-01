# KuuOS OpenClaw Gateway Controller v0.2

## 位置づけ

v0.1 は OpenClaw の `before_tool_call` を KuuOS / ActOS の bounded invocation gate に接続した。
v0.2 は逆方向の active control を追加し、KuuOS から OpenClaw Gateway の agent run を
開始・観測・待機・停止できるようにする。

```text
DecisionOS / PlanOS
        |
        v
      ActOS
        |
        v
KuuOS Gateway Controller v0.2
        |
        | agent / agent.wait / sessions.abort / sessions.list
        v
OpenClaw Gateway
        |
        v
OpenClaw agent loop
        |
        | before_tool_call
        v
KuuOS Control Bridge v0.1
```

このため active control と tool-level enforcement は同じ authority chain の両方向になる。

## OpenClaw RPC boundary

controller は OpenClaw 内部 module を import しない。
公式 CLI の low-level RPC helper を使用する。

```text
openclaw gateway call <method> --params <json> --json
```

使用する RPC は次の4つだけ。

```text
agent
agent.wait
sessions.abort
sessions.list
```

### agent

run start は side effect candidate なので KuuOS preflight を必須にする。

最小 payload:

```json
{
  "message": "...",
  "idempotencyKey": "kuuos-..."
}
```

必要に応じて `sessionKey`, `agentId`, `timeout` を追加する。
成功時は Gateway の canonical `runId` を保存する。

### agent.wait

```json
{
  "runId": "...",
  "timeoutMs": 30000
}
```

wait timeout は observation timeout であり run cancel ではない。

### sessions.abort

exact control surface として

```json
{
  "key": "agent:main:main",
  "runId": "..."
}
```

を使用できる。`runId` 単独または `key` 単独も Gateway が許す場合はそのまま送る。
abort は effectful control なので KuuOS preflight と explicit `--approve` を要求する。

### sessions.list

read-only observation として session index を取得する。

## KuuOS preflight

`start` と `abort` は v0.1 control service の `/v1/preflight` に先に通す。

```text
KuuOS decision = allow
  -> Gateway RPC

KuuOS decision = approval
  -> controller stops unless --approve
  -> --approve records allow-once resolution
  -> Gateway RPC

KuuOS decision = deny
  -> no Gateway RPC
```

controller が直接 OpenClaw に接続しても、OpenClaw agent の tool calls は v0.1 native plugin の
`before_tool_call` gate を再び通る。したがって run-start authorization と individual tool
authorization は別 receipt として保持される。

## receipt model

controller receipt:

```text
~/.kuuos/openclaw/gateway-controller-receipts.jsonl
```

record kinds:

```text
gateway_agent_start_authorized
gateway_agent_start_receipt
gateway_agent_wait_receipt
gateway_abort_authorized
gateway_abort_receipt
gateway_sessions_observation
gateway_controller_error
```

全 receipt は次を保持する。

```text
worldCommitAuthority = false
truthPromotionAuthority = false
automaticPlanCompletion = false
automaticRollback = false
```

Gateway start/abort result は host-control receipt であり WORLD truth ではない。

## 使用例

まず v0.1 control service と OpenClaw Gateway を起動する。

```bash
python3 runtime/kuuos_openclaw_control_server_v0_1.py
openclaw gateway start
```

session を観測する。

```bash
python3 runtime/kuuos_openclaw_gateway_controller_v0_2.py sessions
```

run start の preflight を確認する。

```bash
python3 runtime/kuuos_openclaw_gateway_controller_v0_2.py \
  start \
  --session-key agent:main:main \
  --message 'KuuOS bounded task'
```

policy が approval を返した場合、同一 command に `--approve` を追加して one-shot authorization を記録する。

```bash
python3 runtime/kuuos_openclaw_gateway_controller_v0_2.py \
  --approve \
  start \
  --session-key agent:main:main \
  --message 'KuuOS bounded task' \
  --wait-ms 30000
```

既存 run を観測する。

```bash
python3 runtime/kuuos_openclaw_gateway_controller_v0_2.py \
  wait --run-id <RUN_ID> --wait-ms 30000
```

exact run を停止する。

```bash
python3 runtime/kuuos_openclaw_gateway_controller_v0_2.py \
  --approve \
  abort \
  --session-key agent:main:main \
  --run-id <RUN_ID>
```

## security boundary

v0.2 は arbitrary remote Gateway URL を直接受け付けない。
`--port` で local Gateway port を指定するか、OpenClaw 自身の canonical config を使う。

これにより token/password を controller の command line に複製しない。
remote Gateway を使う場合も OpenClaw 側 config / credential handling を authoritative とする。

controller 自体は KuuOS policy service にのみ loopback HTTP で接続する。
`KUUOS_OPENCLAW_TOKEN` が設定されていれば v0.1 service と同じ Bearer token を使用する。

## authority non-equivalences

```text
Gateway run accepted != plan completed
Gateway run terminal ok != WORLD truth
Gateway abort != rollback proof
agent.wait timeout != run failure
controller receipt != theorem authority
controller receipt != clinical authority
```

## 完成した双方向 control plane

v0.1 + v0.2 で次が成立する。

```text
KuuOS -> OpenClaw
  run start
  run wait / observation
  exact abort

OpenClaw -> KuuOS
  pre-tool-call authorization
  host effect receipt
  observation / verification debt
```

これにより OpenClaw は KuuOS の autonomous authority ではなく、KuuOS / ActOS の
bounded execution host として制御される。

## frontier

次段階では Gateway event subscription と audit ledger を KuuOS ObservationOS / MemoryOS に
接続し、run lifecycle と tool action を event-driven に取り込む。
