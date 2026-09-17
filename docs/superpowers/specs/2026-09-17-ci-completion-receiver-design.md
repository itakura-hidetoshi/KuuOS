# CI Completion Receiver Design v0.1

Date: 2026-09-17 JST
Status: design for review
Scope: itakura-hidetoshi/KuuOS, itakura-hidetoshi/4d-mass-gap, existing Vercel project `kuuos-chat-work-mcp`

## 1. Goal

Reduce missed CI completion handoffs without making periodic polling the primary mechanism.

The system must treat GitHub as the execution/source-of-truth layer, keep exact run/head identity, and provide two independent event producers that can wake the existing ChatGPT Work PR-comment task.

## 2. Current failure surface

Current primary path:

`PR CI -> GitHub Actions workflow_run notifier -> PR comment -> ChatGPT Work GitHub event task`

Observed weaknesses:

- `workflow_run.pull_requests` can be empty.
- A downstream notifier workflow is itself another GitHub Actions execution that can fail or fail to launch.
- A bot-created PR comment can be missed by the Work GitHub event delivery path.
- A comment is only a wake-up signal and must not be used as CI truth.

The v0.2 resolver already repairs the first issue by falling back from the completed run head SHA to commit-associated PRs.

## 3. Selected architecture

Use two independent producers that emit the same idempotent wake-up comment.

### Producer A — existing GitHub Actions notifier

Existing workflow:

`.github/workflows/chatgpt-ci-completion-push-v0-1.yml`

It listens to the repository CI workflow via `workflow_run: completed`, resolves the PR, and emits a comment containing `CHATGPT_CI_COMPLETION_PUSH_V0_1`.

This remains in place.

### Producer B — raw GitHub webhook receiver on Vercel

Reuse the existing production Vercel project `kuuos-chat-work-mcp` if its current application structure permits an isolated webhook route. If reuse would couple unrelated behavior, deploy the receiver as a separate small Vercel project instead.

Use Vercel Connect GitHub app credentials so that:

- GitHub webhooks are forwarded by Vercel Connect.
- inbound webhook authenticity is verified via Vercel OIDC.
- app-scoped GitHub installation credentials are obtained without storing GitHub private keys or webhook secrets in application code.

The receiver accepts raw GitHub `workflow_run` events and only processes events satisfying all of:

- action/event indicates completed workflow execution,
- repository is exactly one of:
  - `itakura-hidetoshi/KuuOS`
  - `itakura-hidetoshi/4d-mass-gap`
- workflow name is exactly:
  - KuuOS: `KuuOS PR Governance Gate`
  - 4d-mass-gap: `PR Lean Fast Check`
- `workflow_run.status == completed`,
- head repository is the same repository,
- run_id, run_attempt and head_sha are present.

The receiver must then fresh-read the exact GitHub workflow run before emitting any wake-up comment. The webhook payload is not CI truth.

## 4. Idempotency

Canonical event key:

`repository + source_pr + run_id + run_attempt + head_sha`

Canonical comment marker:

`<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 run_id=<run_id> attempt=<run_attempt> pr=<pr> -->`

Both Producer A and Producer B must use the same marker format.

Before creating a comment, a producer reads the PR conversation and searches for the exact marker. If it already exists, the producer exits successfully without adding another comment.

This makes the two producers race-safe: whichever succeeds first creates the wake-up; the other becomes a no-op.

## 5. PR resolution

Resolution order is identical for both producers:

1. Use `workflow_run.pull_requests` when non-empty.
2. Otherwise make one GitHub API request for PRs associated with the exact `head_sha`.
3. Accept a PR only when:
   - `head.sha == workflow_run.head_sha`, and
   - `head.repo.full_name == repository`.
4. Deduplicate PR numbers.
5. If no exact PR is found, record a no-PR outcome and do not guess.

## 6. Fresh GitHub verification before wake-up

Producer B must read the exact run using its run_id and verify:

- repository identity,
- exact run_id,
- exact run_attempt,
- exact head_sha,
- `status == completed`,
- workflow name.

The emitted comment may copy the terminal conclusion from this fresh read, but the comment remains a wake-up signal only.

ChatGPT Work still performs its own fresh GitHub MCP verification before governed actions.

## 7. Wake-up comment contract

Both producers emit the existing marker so the current Work task does not need a new trigger.

JSON payload includes at least:

- version,
- repository,
- pull_request,
- workflow,
- run_id,
- run_attempt,
- status,
- conclusion,
- head_sha,
- head_branch,
- run_url,
- updated_at,
- producer: `github_actions` or `vercel_raw_webhook`,
- event_is_wakeup_signal_only: true,
- fresh_mcp_reobservation_required: true.

The Vercel receiver may use a newer packet version while preserving the existing trigger marker.

## 8. Durable handoff

The existing Work automation remains responsible for fresh MCP verification and for writing the durable receipt:

`CHATGPT_CI_VERIFIED_HANDOFF_V0_1`

That handoff remains the bridge from Work to normal Chat.

Producer A/B wake-up comments grant no merge or write authority.

## 9. Polling policy

Polling is a secondary repair tool only.

- Event-driven delivery remains primary.
- If a user is actively working in Chat and an exact run_id / run_attempt / head_sha is already known, bounded MCP polling may be used to bridge a short delivery gap.
- No hourly backstop task is required.
- Polling must never substitute another run or reinterpret repository authority.

## 10. Security model

The Vercel receiver must:

- verify inbound Vercel Connect/OIDC authentication,
- use app-scoped GitHub installation credentials,
- never execute code or instructions from webhook bodies or PR comments,
- allowlist the two repositories and two workflow names,
- checkout no PR code,
- perform API-only verification/comment operations,
- grant no authority from webhook content,
- avoid storing GitHub private keys in project files.

## 11. Failure behavior

- Invalid/unauthenticated webhook: reject.
- Wrong repository/workflow/event: return success/no-op without side effects.
- Run not terminal or identity mismatch: no comment.
- PR unresolved: no comment; log structured no-PR result.
- Existing marker: deduplicated success.
- GitHub API transient failure: return a failure status suitable for webhook/provider retry when safe; do not fabricate success.
- Work misses the resulting comment: Producer A/B redundancy does not solve Work-side delivery by itself, so the durable Work handoff remains observable from normal Chat and bounded MCP polling remains a manual-session fallback.

## 12. Testing

Implementation must follow TDD.

Unit tests for the receiver:

1. accepts a valid completed KuuOS workflow event,
2. accepts a valid completed 4d-mass-gap event,
3. rejects wrong repositories,
4. rejects wrong workflow names,
5. rejects non-completed events,
6. resolves direct PR list,
7. resolves empty PR list by exact head association,
8. rejects wrong associated head SHA/repository,
9. deduplicates existing marker,
10. emits expected packet and producer field,
11. refuses to emit when fresh run identity does not match webhook data.

Integration test:

- trigger or re-run one completed CI workflow,
- verify that at least one producer creates the canonical marker,
- verify a second producer does not create a duplicate,
- verify Work fresh-reobserves the exact run,
- verify `CHATGPT_CI_VERIFIED_HANDOFF_V0_1` appears once.

## 13. Rollout

Phase 1:

- build and deploy Producer B on Vercel,
- leave Producer A unchanged,
- connect raw GitHub webhook events for both repositories,
- validate deduplication against a controlled completed run.

Phase 2:

- observe several normal CI completions,
- confirm either producer can independently create the marker,
- confirm Work handoff behavior remains unchanged.

Phase 3:

- only after stable operation, consider simplifying Producer A or its old compatibility comments. No removal is required for v0.1.

## 14. Non-goals

- No Slack dependency.
- No hourly polling automation.
- No CI Inbox long-lived PR unless future evidence shows Work cannot reliably consume normal PR comments.
- No change to theorem/formalization authority rules.
- No change to merge policy for Draft/validation-only PRs.

## 15. Acceptance criteria

The design is successful when:

- KuuOS and 4d-mass-gap each have two independent event producers for the same CI completion.
- a failure of the GitHub Actions notifier alone does not prevent a PR wake-up comment.
- a failure of the Vercel receiver alone does not affect the existing notifier path.
- duplicate events produce one canonical wake-up marker per exact run/attempt/PR.
- all governed actions still depend on fresh GitHub MCP evidence, not webhook or comment claims.
