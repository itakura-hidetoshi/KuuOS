# KuuOS OpenClaw Supervisor v0.5

## 目的

v0.1〜v0.4 で作った制御・観測部品を「置いてあるコード」から「一つの fail-closed 運用ループ」にまとめる。

```text
OpenClaw tool call
      |
      v
kuuos-control native plugin v0.1
      |
      | before_tool_call
      v
KuuOS loopback policy service v0.1
      |
      +--------------------- execution decision boundary
      |
OpenClaw Gateway / agent loop
      |
      +--> live WebSocket hints v0.4
      |         |
      |         +--> gap / reconnect / subscription error
      |                   |
      |                   v
      +----------> audit.activity.list reconciliation v0.3
                            |
                            v
                 ObserveOS / verification debt
```

v0.5 の closed-loop readiness は

```text
control healthy + fresh Gateway hello + initial audit reconciliation
```

に加えて、起動前 doctor で `kuuos-control` の `before_tool_call` / `after_tool_call` runtime registration、
Gateway RPC、audit read、v0.4 exact dependencies が確認できたときだけ発行する。

ただし

```text
closed-loop ready != WORLD truth
closed-loop ready != ObserveOS commit
closed-loop ready != verification
closed-loop ready != PlanOS completion
closed-loop ready != rollback proof
```

である。

## OpenClaw 2026.8.1 hook startup intent

`kuuos-control` は typed hook を登録する hook-only plugin なので、現行 OpenClaw の startup selection と明示的に整合させる。

```json
"activation": {
  "onStartup": true,
  "onCapabilities": ["hook"]
}
```

すなわち

```text
activation.onCapabilities = ["hook"]
```

を manifest に固定する。

これは plugin allow/deny/enable policy を迂回しない。plugin は引き続き明示的に install/enable される必要がある。

## install-plugin

repository checkout から OpenClaw に local linked plugin として載せるための effectful subcommand を用意する。

実際に使う OpenClaw native flow は

```text
openclaw plugins validate --entry <KuuOS/integrations/openclaw> --json
openclaw plugins install --link <KuuOS/integrations/openclaw> --force
openclaw plugins enable kuuos-control
```

である。

v0.5 は勝手に実行しない。必ず

```bash
python3 runtime/kuuos_openclaw_supervisor_v0_5.py \
  install-plugin \
  --approve-install
```

を要求する。

Gateway restart も別 authority とする。明示的に

```bash
python3 runtime/kuuos_openclaw_supervisor_v0_5.py \
  install-plugin \
  --approve-install \
  --approve-restart
```

とした場合だけ

```text
openclaw gateway restart --safe
```

を行う。

managed Gateway の config reload が plugin installation 後に自動 restart する環境もあるが、それを推測して WORLD receipt にしない。

## doctor

read-only doctor は次を要求する。

```text
openclaw --version
openclaw plugins list --json
openclaw plugins inspect kuuos-control --runtime --json
openclaw gateway status --deep --require-rpc --json
openclaw gateway call audit.activity.list --params {"limit":1} --json
```

`plugins list` は cold inventory にすぎないため、それだけで保護中とは判定しない。

v0.5 doctor は

```text
plugins inspect kuuos-control --runtime --json
```

に `before_tool_call` と `after_tool_call` が現れることを必須にする。

さらに `integrations/openclaw/event-stream/node_modules` の

```text
@openclaw/gateway-client 2026.8.1
@openclaw/gateway-protocol 2026.8.1
```

を exact に確認する。未導入なら repository を変更せず、

```bash
cd integrations/openclaw/event-stream
npm install
```

を要求して停止する。

## run

通常起動:

```bash
python3 runtime/kuuos_openclaw_supervisor_v0_5.py run
```

順序は次。

```text
1. doctor を全て通す
2. v0.1 control service を 127.0.0.1:8765 で起動
3. /health の fresh success を待つ
4. v0.4 subscriber を起動
5. 起動前 ledger offset より後の fresh connection hello を待つ
6. v0.3 audit sync を実行
7. completedWindow=true を確認
8. 初めて closed-loop-ready receipt を出す
9. periodic audit reconciliation を継続
10. gap/reconnect/subscription error では追加 audit reconciliation を早期発火
```

fresh hello を必須にするため、過去の `gateway-event-hints.jsonl` に hello が残っていても readiness には使わない。

## fail-closed supervision

required runtime component は

```text
v0.1-control
v0.4-live-events
v0.3-audit-reconciliation
```

である。

```text
required component failure -> supervisor stops policy service
```

とする。

したがって default `failClosed=true` を維持する `kuuos-control` plugin では、supervisor が ready でない状態を
「KuuOS を迂回して実行継続」に変えず、次に観測された tool call は policy unavailable として block される。

この設計は rollback ではない。外部世界で既に起きた effect を消したとは主張しない。

## audit reconciliation

通常は 60 秒ごとに v0.3 を同期する。

次の live receipt が出た場合は、10 秒の debounce を挟んで追加 reconciliation を起動する。

```text
connection sequence gap
run sequence gap
connection close
connect error
reconnect paused
subscription error
event projection error
```

v0.3 が page budget を使い切って `resumeRequired=true` を返した場合、v0.5 は ready loop を継続しない。
これは partial history を complete と誤認しないためである。

## credential boundary

v0.5 supervisor 自身は Gateway bearer token を CLI 引数として扱わない。
v0.4 device pairing/token storage は既存の host-owned contract を使う。

v0.5 `run` は `KUUOS_OPENCLAW_TOKEN` が設定されている場合、installed plugin 側と secret が一致することを証明できないため起動を拒否する。
既定の loopback policy service は token 無しで使用する。

remote Gateway は v0.5 では対象外。

```text
local-Gateway only
```

v0.4 単体には明示 opt-in `wss://` remote capability が残るが、closed-loop supervisor は audit CLI target と live target の同一性を十分に証明できる local configuration に限定する。

## pairing

v0.4 subscriber の KuuOS device identity が初回 pairing を要求する場合、fresh hello は出ない。
その場合 supervisor は ready を発行せず停止する。
OpenClaw host 側で current pairing request を確認・承認してから再起動する。

```text
openclaw devices list
openclaw devices approve <requestId>
```

pairing request の id を KuuOS が勝手に推測・承認しない。

## 実機導入について

この PR/CI は repository implementation と CI validation を行う。

```text
actual machine installation is not performed by repository CI
```

したがって PR が green でも、利用者の実 OpenClaw machine に plugin が install/enable/pair/restart 済みとは主張しない。
実機では `install-plugin` →必要なら pairing→ `doctor` → `run` の順で確認する。

## Authority boundary

全 supervisor receipt は

```text
worldCommitAuthority = false
truthPromotionAuthority = false
observeCommitAuthority = false
verificationAuthority = false
planCompletionAuthority = false
automaticPlanCompletion = false
rollbackProofAuthority = false
automaticRollback = false
memoryOverwriteAuthority = false
```

を保持する。

`closed-loop-ready` は operational readiness receipt であり、世界についての命題の真偽を決めない。

## Validation

```bash
python3 scripts/check_openclaw_supervisor_v0_5.py
python3 tests/test_openclaw_supervisor_v0_5.py
```

Lean boundary:

```text
formal/KUOS/ObserveOS/OpenClawSupervisorV0_5.lean
```
