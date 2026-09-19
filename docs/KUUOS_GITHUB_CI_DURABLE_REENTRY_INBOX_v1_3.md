# KuuOS GitHub CI Durable Reentry Inbox v1.3

## Purpose

v1.3 removes the normal-path dependency on conversational lifetime and on scheduled CI polling.

The existing source-side sender already emits a bounded `repository_dispatch` event when `itakura-hidetoshi/4d-mass-gap` finishes `PR Lean Fast Check`. The missing piece was durable storage between that event and a later MCP client activation.

v1.3 fills that gap:

```text
4d-mass-gap PR Lean Fast Check completes
→ source-side bounded repository_dispatch
→ KuuOS repository_dispatch receiver
→ exact source / workflow / canonical base / head SHA / job / step gate
→ deterministic inbox identity key
→ deduplicated open GitHub Issue
→ conversation may be absent for any length of time
→ later MCP client searches open pending inbox Issues
→ fresh GitHub MCP re-observation of exact run / job / step / head SHA
→ v1.1 verification
→ v1.3 acknowledgement compiler
→ comment receipt + close Issue
```

The durable Issue is not CI truth. It is not success evidence. It grants no merge authority and no write authority.

## Why GitHub Issue is the queue

A stateless MCP server is not an unsolicited notification bus. A ChatGPT conversation therefore cannot be relied on as the storage location for an event that occurs while the conversation is closed.

The repository itself is already an authorized, persistent coordination surface. An open GitHub Issue gives the re-entry signal all of the properties needed here:

- durable across conversation shutdown and restart;
- visible to the existing GitHub MCP `issues` toolset;
- naturally enumerable as pending work;
- independently acknowledgement-capable by comment + close;
- auditable in GitHub history;
- no separate database or polling daemon required for the preferred event-driven path.

The Issue title is deterministic:

```text
[KuuOS CI Reentry Pending] <sha256 exact-identity-key>
```

where the identity key binds:

```text
repository + workflow run ID + workflow name + exact head SHA
```

The workflow searches for the exact deterministic title before creation. Duplicate dispatches are therefore idempotent at the queue layer.

## Accepted source

The v1.3 compiler is intentionally narrow. It accepts only the sender contract already deployed for the mass-gap formalization path:

```text
source repository  = itakura-hidetoshi/4d-mass-gap
workflow           = PR Lean Fast Check
source event       = pull_request
status             = completed
canonical base     = formal/real-hilbert-uniform-coercive-strong-limit
required job       = Changed Lean fast check
required step      = Run changed Lean fast check
destination        = itakura-hidetoshi/KuuOS
sender version     = mgap4d_kuuos_ci_completion_sender_v0_1
```

Both success and terminal non-success conclusions are persisted. Failure is a valid wake-up event for repair/triage; it is never promoted to success.

The source sender must also explicitly carry:

```text
event_is_wakeup_signal_only = true
fresh_mcp_reobservation_required = true
```

A wrong base, wrong repository, wrong workflow, wrong required job/step binding, non-terminal state, malformed SHA, missing fresh-MCP boundary, or wrong destination fails closed before Issue creation.

## MCP pickup protocol

The consumer does not poll CI runs. It only asks the durable queue for unacknowledged work when an MCP-capable runtime is active.

Conceptually:

```text
search issues:
  repository = itakura-hidetoshi/KuuOS
  state      = open
  title      contains "[KuuOS CI Reentry Pending]"

for each pending issue:
  parse strict JSON body
  read mcp_reobserve_request
  freshly observe source workflow run and jobs through GitHub MCP
  verify v1.1 exact identity + completed required job + completed required step
  compile v1.3 ack
  if ack ready:
      add acknowledgement comment
      close issue
  else:
      leave issue open
```

The queue is therefore **event-driven on ingress and demand-driven on consumption**. No periodic CI status scan is required in the normal path.

## Acknowledgement rule

`runtime/kuuos_github_ci_durable_reentry_inbox_v1_3.py` provides `compile_ack(...)`.

It will permit closure only when the supplied v1.1 verification says all of the following:

```text
status = KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED
route ∈ {verified_success, verified_non_success}
fresh_mcp_reobservation = true
repository / run ID / workflow / head SHA exactly match the inbox record
merge_authority_granted = false
write_authority_granted = false
```

Thus:

```text
Issue exists
≠ CI verified

Issue says success
≠ CI verified

MCP consumer saw Issue
≠ CI verified

fresh exact MCP re-observation + v1.1 verification
→ acknowledgement is allowed

acknowledgement
≠ merge authority
≠ write authority
```

If verification fails or remains incomplete, the Issue stays open and survives the end of the conversation/runtime session.

## Relationship to v1.1 and v1.2

v1.1 remains the authoritative fresh-observation verification layer.

v1.2 is retained only as a credential-free public-GitHub fallback when the source-side cross-repository sender cannot dispatch to KuuOS. Its five-minute cron is not the preferred path.

Preferred path after v1.3:

```text
source completion event
→ repository_dispatch
→ durable Issue
→ later MCP pickup
```

Fallback path:

```text
v1.2 scheduled public observer
→ KuuOS self-dispatch
→ v1.1/v1.3 re-entry path
```

## ChatGPT boundary

This repository mechanism solves **event loss outside a conversation**. It does not claim that a stateless MCP server can spontaneously inject a message into an inactive ChatGPT conversation.

There are two valid activation models:

1. the next ChatGPT/MCP session begins by reading pending inbox Issues; or
2. an independently authorized always-on KuuOS/ChatGPT task runner activates the same MCP pickup protocol when desired.

In either model, the durable event already exists before the client wakes, so no CI-completion signal is lost merely because the conversation was closed.

## Runtime outputs

For event intake:

```text
ci_reentry_inbox_result.json
ci_reentry_inbox_record.json
ci_reentry_issue_spec.json
```

The workflow additionally writes:

```text
ci_reentry_issue_receipt.json
```

For acknowledgement compilation:

```text
ci_reentry_ack_spec.json
```

The Issue body is the exact JSON inbox record. No credential or token is written into the Issue, artifact, receipt, or summary.

## Formal boundary

`formal/KuuOSGitHubMCPServerBridgeV0_1/V1_3.lean` defines `DurableInboxReentryGate.Admitted` and proves that admission is impossible if:

- the event was not durably persisted;
- the pending item was not observed by the MCP consumer;
- fresh MCP re-observation is absent;
- the exact identity disagrees;
- acknowledgement is attempted before fresh verification;
- the durable signal is used as success evidence;
- merge authority is inferred;
- write authority is inferred.

## Validation

```bash
python3 runtime/kuuos_github_ci_durable_reentry_inbox_v1_3.py --self-check
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSGitHubMCPServerBridgeV0_1
```

The self-check covers success persistence, terminal-failure persistence, wrong canonical base rejection, missing fresh-MCP-boundary rejection, verified acknowledgement, unverified acknowledgement rejection, and wrong-head acknowledgement rejection.
