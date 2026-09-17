# CI Completion Receiver Design v0.2

Date: 2026-09-18 JST
Status: approved implementation design
Scope: `itakura-hidetoshi/KuuOS` and `itakura-hidetoshi/4d-mass-gap`

## Goal

Reduce missed CI completion wake-ups without Slack and without an hourly polling task. GitHub remains the execution/source-of-truth layer. ChatGPT Work remains the event consumer, and every governed action still requires fresh GitHub MCP evidence.

## Existing path and failure surface

Producer A already exists in both repositories:

`source PR CI -> workflow_run: completed notifier -> PR comment -> ChatGPT Work`

The notifier emits a comment containing `CHATGPT_CI_COMPLETION_PUSH_V0_1`. The v0.2 resolver already handles the observed case where `workflow_run.pull_requests` is empty by resolving the PR from the exact completed head SHA.

Remaining risks are independent of that resolver:

- the downstream `workflow_run` notifier can fail or fail to launch,
- the Work delivery path can miss a bot-created PR comment,
- a single event path gives only one chance to wake Work.

The wake-up comment is never CI truth or merge/write authority.

## Rejected approaches

### Hourly polling

Rejected because the delay is operationally too large. Polling remains allowed only as a bounded secondary repair mechanism for an already fixed exact run identity.

### Slack

Rejected by user requirement.

### Vercel raw `workflow_run` receiver

Rejected after checking current Vercel Connect GitHub event support. The supported real-time GitHub channel surface does not provide a sufficiently strong contract for raw `workflow_run` delivery. Introducing a second external runtime would therefore add complexity without a reliable event guarantee.

## Selected architecture

Use two GitHub-native event paths that independently create two PR-comment wake-up events for the same exact source CI run.

### Producer A — existing `workflow_run` notifier

Keep the current `chatgpt-ci-completion-push-v0-1.yml` path unchanged except for compatibility fixes when required.

Producer A is triggered after GitHub marks the source workflow completed.

### Producer B — source-workflow finalizer + `repository_dispatch`

Add a finalizer job to the source CI workflow itself:

- KuuOS: `KuuOS PR Governance Gate`
- 4d-mass-gap: `PR Lean Fast Check`

For pull-request runs only, the finalizer sends a same-repository `repository_dispatch` event of type:

`chatgpt_ci_completion_dispatch_v0_1`

The dispatch payload fixes:

- repository,
- pull_request,
- source run_id,
- source run_attempt,
- exact PR head_sha,
- head_branch,
- source workflow name.

GitHub documents `repository_dispatch` as an explicit exception to normal `GITHUB_TOKEN` recursion prevention: a repository dispatch created with the repository token can start a new workflow run. Creating the dispatch requires `Contents: write`.

A dedicated default-branch receiver workflow consumes the dispatch. Because the source finalizer is still finishing when it sends the dispatch, the receiver may briefly observe the source run as `in_progress`. It may therefore bounded-poll only that exact `run_id / run_attempt / head_sha` with short backoff until the source run becomes terminal. It must never substitute another run or search for a newer run.

## Why Producer B is independent enough

Producer A depends on GitHub's downstream `workflow_run` event scheduling.

Producer B depends on an explicit `repository_dispatch` POST made by the source workflow itself and a separate receiver workflow on the default branch.

They share GitHub infrastructure but use different triggering mechanisms. A failure of the `workflow_run` notifier does not prevent the source finalizer from dispatching. A failure of Producer B does not affect Producer A.

## Deliberate duplicate wake-up comments

Producer A and Producer B must NOT deduplicate against each other.

The goal is two independent PR activity events so ChatGPT Work gets two chances to receive the completion wake-up. Existing Work logic already deduplicates processing using the exact identity:

`repository + pull_request + run_id + run_attempt + head_sha`

Producer B deduplicates only its own retry/replay marker.

Producer B marker:

`<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 producer=repository_dispatch_v0_1 run_id=<run_id> attempt=<run_attempt> pr=<pr> -->`

It intentionally contains the existing `CHATGPT_CI_COMPLETION_PUSH_V0_1` substring so the current Work task recognizes it without a trigger redesign.

Producer A retains its current marker.

## Producer B exact-run verification

The receiver must fresh-read the exact GitHub Actions run before writing a comment. The dispatch payload is only a wake-up request.

Required checks:

- repository equals the current repository,
- run_id is a positive integer and matches the fetched run,
- run_attempt is a positive integer and matches the fetched run,
- workflow name is exactly allowlisted for the repository,
- event is `pull_request`,
- exact head_sha matches the fetched run,
- status is `completed`,
- terminal conclusion is present,
- the PR number is positive,
- the PR current head repository is the same repository,
- the PR head SHA equals the dispatched head SHA before the comment is emitted.

If the PR has moved, Producer B records a stale/no-comment result. Work must not be woken for an obsolete exact head by this path.

## Bounded polling policy

Producer B may poll only because the dispatch is emitted before the source workflow can technically become completed.

Rules:

- exact run identity is fixed before polling,
- no latest-run search,
- no alternate run substitution,
- short bounded attempts with backoff,
- stop immediately when terminal,
- if the bound is exhausted, exit without a success comment,
- record whether polling was needed.

Normal Chat may also use bounded polling secondarily when an exact run is already known and event delivery is delayed. There is no hourly polling automation.

## Comment contract

Producer B packet version:

`chatgpt_ci_completion_push_v0_3`

Required JSON fields:

- `version`,
- `repository`,
- `pull_request`,
- `workflow`,
- `run_id`,
- `run_attempt`,
- `status`,
- `conclusion`,
- `head_sha`,
- `head_branch`,
- `run_url`,
- `updated_at`,
- `producer: repository_dispatch_v0_1`,
- `event_is_wakeup_signal_only: true`,
- `fresh_mcp_reobservation_required: true`,
- `polling_used`.

The comment grants no CI truth, merge authority, or write authority.

## Work and normal Chat behavior

The existing Work task `CI完了コメント受信` remains the consumer. It must:

1. parse either Producer A or Producer B comment,
2. deduplicate by exact run identity,
3. fresh-reobserve the exact run through GitHub MCP,
4. verify terminal jobs/steps and current repository authority,
5. write one durable `CHATGPT_CI_VERIFIED_HANDOFF_V0_1` receipt.

Normal Chat can read that durable handoff and fresh-check the exact run before continuing repository work.

## Existing re-entry infrastructure to reuse

KuuOS already contains `KuuOS GitHub CI Completion Reentry v1.1`, which accepts both `workflow_run` and `repository_dispatch` and formalizes the boundary that an event is not success evidence.

4d-mass-gap already contains a KuuOS completion sender/source inbox and demonstrates bounded completion packets plus durable source persistence.

The new ChatGPT Producer B should follow those existing exact-identity and non-authority principles rather than create a new external event subsystem.

## Security and authority

- Receiver workflow executes only trusted default-branch code.
- No PR code is executed with `issues: write` permission.
- Dispatch client payload is untrusted until the exact run and PR are re-read.
- Receiver permissions are limited to `actions: read`, `contents: read`, `issues: write`, and `pull-requests: read`.
- Source finalizer gets only the permission needed to create same-repository dispatch (`contents: write`).
- No secrets or PATs are required for same-repository dispatch.
- KuuOS PR #1558 remains validation-only and must never be merged, marked ready, or auto-merged.
- Existing theorem/formalization authority rules are unchanged.

## Failure behavior

- Dispatch POST failure: source CI validation result must not be converted to failure solely because notification failed; record the notification failure in the job summary.
- Invalid dispatch payload: no comment.
- Exact run identity mismatch: no comment.
- Nonterminal source run after bounded poll exhaustion: no comment; Producer A remains available.
- Current PR head mismatch: no comment.
- Producer B marker already present: deduplicated no-op.
- Producer A marker present but Producer B marker absent: Producer B still posts its own comment intentionally.
- Work processes one producer first: the second producer is ignored at the Work processing layer by exact identity.

## Testing

Implementation follows TDD.

Unit tests must cover:

1. valid KuuOS dispatch payload,
2. valid 4d-mass-gap dispatch payload,
3. wrong repository/workflow rejection,
4. invalid run/attempt/SHA rejection,
5. fresh source run identity mismatch,
6. `in_progress -> completed` bounded poll sequence,
7. bounded poll exhaustion,
8. current PR head mismatch,
9. Producer B own-marker deduplication,
10. Producer A marker does not suppress Producer B,
11. correct Producer B packet/marker fields.

Workflow/static tests must confirm:

- source finalizer runs only for `pull_request`,
- dispatch event type is exact,
- payload binds exact run/attempt/head/PR/workflow,
- receiver workflow exists on default branch after merge,
- receiver uses trusted default-branch script,
- source finalizer notification failure does not override substantive CI result.

## Rollout

1. Implement KuuOS Producer B in Draft PR #1660.
2. Implement equivalent 4d-mass-gap Producer B in a separate Draft PR.
3. Obtain fresh GREEN CI for exact PR heads.
4. Merge the bounded infrastructure PRs when governance conditions are met.
5. Trigger one controlled PR CI in each repository after receiver workflows exist on default branch.
6. Verify two producer comments can coexist for one exact run without duplicate Work processing.
7. Verify exactly one durable Work handoff for that exact identity.

## Acceptance criteria

- No Slack.
- No hourly polling automation.
- KuuOS and 4d-mass-gap each have Producer A and Producer B.
- Producer B can wake Work when Producer A's `workflow_run` notifier is absent or missed.
- Producer A remains unaffected if Producer B fails.
- Producer B retries/replays are idempotent to its own marker.
- Producer A and Producer B intentionally create separate PR activity events.
- Work deduplicates them by exact run identity.
- All governed actions still require fresh GitHub MCP evidence.
