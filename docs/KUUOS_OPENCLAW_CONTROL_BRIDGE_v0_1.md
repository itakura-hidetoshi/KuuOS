# KuuOS OpenClaw Control Bridge v0.1

## 目的

OpenClaw を KuuOS の下位実行ホストとして接続し、OpenClaw の tool invocation を
KuuOS / ActOS の bounded adapter invocation 境界の下に置く。

これは「KuuOS を OpenClaw の system prompt に書く」だけの統合ではない。
OpenClaw native plugin の `before_tool_call` gate を利用して、外部作用候補を
KuuOS control service の preflight に通す。

## authority direction

```text
DecisionOS / PlanOS
        |
        v
      ActOS
        |
        | bounded authorization / exact operation binding
        v
KuuOS OpenClaw control service
        |
        | allow / approval / deny
        v
OpenClaw native plugin
        |
        | before_tool_call
        v
OpenClaw tool host
        |
        | after_tool_call host receipt
        v
KuuOS observation + verification debt
        |
        v
WORLD commit authority (separate)
```

OpenClaw は DecisionOS でも WORLD でもない。OpenClaw の host receipt を WORLD truth に
自動昇格させない。

## KuuOS / ActOS invariants

v0.1 は既存 ActOS bounded adapter invocation の意味を保つ。

```text
adapter invocation != WORLD commit
host receipt != WORLD truth
host receipt != automatic plan completion
host receipt != automatic rollback

automatic truth promotion = false
automatic plan completion = false
automatic rollback = false
```

外部作用が記録された場合は

```text
observation required = true
verification required = true
```

を残す。

## OpenClaw enforcement

`integrations/openclaw/index.mjs` は typed plugin hook を使う。

### before_tool_call

各 tool call について KuuOS service の `/v1/preflight` に bounded envelope を送る。

KuuOS decision:

- `allow`: call を継続
- `approval`: OpenClaw plugin approval を要求
- `deny`: call を block
- service unavailable / malformed decision: default `failClosed=true` なら block

OpenClaw 側の sandbox、owner-only core-tool、exec approval 等はそのまま残る。
KuuOS は既存 host policy を越える権限を与えない。

### after_tool_call

結果を `/v1/post-effect` に送り canonical host receipt を記録する。

`after_tool_call` は observation hook なので、receipt 記録失敗によって既に起きた effect を
巻き戻せない。失敗時は observation / verification debt を open のまま残す。

## security boundary

- policy URL はデフォルト `http://127.0.0.1:8765`
- 非 loopback URL は `allowRemotePolicyUrl=true` を明示しない限り拒否
- tool payload 内の secret-like key は plugin と server の両方で redaction
- payload は bounded
- v0.1 control server 自体は非 loopback bind を拒否
- `KUUOS_OPENCLAW_TOKEN` を設定した場合は Bearer token を要求

## 現時点の OpenClaw 境界

OpenClaw の `before_tool_call` は model-visible / host-emitted tool call の直前 gate として使う。
ただし、ある tool の内部で最終的に解決される nested operation を、すべて共通の
「effect 直前」フックで再捕捉できるとは仮定しない。

したがって v0.1 の claim は:

```text
KuuOS gates OpenClaw tool calls observed by before_tool_call.
```

であり、

```text
KuuOS intercepts every possible nested host side effect.
```

ではない。

nested effect 完全捕捉は、各 effectful adapter の個別 policy または OpenClaw 側の
より深い pre-effect primitive が必要。

## install

KuuOS repository root から control service を起動する。

```bash
python3 runtime/kuuos_openclaw_control_server_v0_1.py
```

別 terminal で plugin を link install / enable する。

```bash
openclaw plugins install --link ./integrations/openclaw --force
openclaw plugins enable kuuos-control
openclaw gateway restart
openclaw plugins inspect kuuos-control --runtime --json
```

plugin config の既定値は loopback service を使うため、最初は追加設定なしでよい。

Bearer token を使う場合:

```bash
export KUUOS_OPENCLAW_TOKEN='replace-with-a-local-secret'
```

同じ値を OpenClaw の `plugins.entries.kuuos-control.config.policyToken` に設定する。

## policy modes

control service:

```bash
python3 runtime/kuuos_openclaw_control_server_v0_1.py --policy-mode approval
python3 runtime/kuuos_openclaw_control_server_v0_1.py --policy-mode owner-strict
python3 runtime/kuuos_openclaw_control_server_v0_1.py --policy-mode observe
```

`approval` が default。

- read-only set: allow
- effectful / unknown tool: approval

`owner-strict` は host-derived requester が明示的に non-owner の場合、effectful tool を deny。
requester identity が欠落していることを owner の証明として扱わない。

`observe` は bring-up / compatibility test 用で、全 call を allow し receipt のみ記録する。
本番の KuuOS control claim には `approval` またはより厳しい policy を使う。

## receipts

append-only JSONL:

```text
~/.kuuos/openclaw/receipts.jsonl
```

各 record は SHA-256 digest と receipt id を持つ。

record kind:

- `openclaw_preflight`
- `openclaw_approval_resolution`
- `openclaw_host_receipt`

これらは execution / observation receipts であり WORLD truth receipt ではない。

## v0.2 frontier

次の大きな単位は OpenClaw Gateway controller を KuuOS 側へ追加し、

```text
KuuOS -> Gateway session/run start
KuuOS -> Gateway run cancel
Gateway events -> KuuOS observation
```

まで双方向 control-plane 化すること。

v0.1 の tool gate を先に固定することで、v0.2 の active control が KuuOS authorization を
迂回しない土台を作る。
