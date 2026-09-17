# CI Completion Receiver Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a second GitHub-native CI-completion wake-up path using source-workflow `repository_dispatch`, short bounded exact-run polling, and a producer-specific PR comment recognized by the existing ChatGPT Work task.

**Architecture:** Producer A remains the existing `workflow_run: completed` notifier. Producer B is initiated by a finalizer job inside the source PR CI, sends a same-repository `repository_dispatch`, and a trusted default-branch receiver workflow verifies the exact original run and current PR head before posting a second wake-up comment. Producer B deduplicates only its own retries; Producer A and Producer B intentionally produce separate PR activity events while Work deduplicates processing by exact run identity.

**Tech Stack:** GitHub Actions, GitHub REST API, Python 3.12 standard library, `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-17-ci-completion-receiver-design.md`

## Global Constraints

- Repositories: exactly `itakura-hidetoshi/KuuOS` and `itakura-hidetoshi/4d-mass-gap`.
- Source workflows: `KuuOS PR Governance Gate` and `PR Lean Fast Check`.
- Dispatch event type: `chatgpt_ci_completion_dispatch_v0_1`.
- Producer B marker contains `CHATGPT_CI_COMPLETION_PUSH_V0_1` but includes `producer=repository_dispatch_v0_1`.
- Producer B must not deduplicate against Producer A's marker.
- Dispatch/wake-up comments are not CI truth or merge/write authority.
- Polling is bounded to the fixed `run_id / run_attempt / head_sha`; never search or substitute another run.
- No Slack, Vercel receiver, or hourly polling automation.
- Existing Work durable handoff `CHATGPT_CI_VERIFIED_HANDOFF_V0_1` is unchanged.
- KuuOS PR #1558 remains validation-only and must never be merged/ready/auto-merged.

---

### Task 1: Producer B core script — tests first

**Files in each repository:**
- Create: `tests/test_chatgpt_ci_completion_dispatch_v0_1.py`
- Create: `scripts/chatgpt_ci_completion_dispatch_v0_1.py`

**Interfaces:**

```python
validate_dispatch_payload(payload: dict, repository: str) -> DispatchIdentity | None
verify_run(identity: DispatchIdentity, run: dict) -> bool
producer_marker(identity: DispatchIdentity) -> str
build_comment(identity: DispatchIdentity, run: dict, *, polling_used: bool) -> str
process_event(event: dict, github: GitHubApiLike, *, sleep_fn, delays: tuple[float, ...]) -> dict
```

- [ ] Write failing tests for valid KuuOS/4d payloads and malformed repo/workflow/run/attempt/SHA values.
- [ ] Run `python3 -m unittest -v tests.test_chatgpt_ci_completion_dispatch_v0_1` and verify RED because the script does not exist.
- [ ] Implement only payload validation and immutable identity dataclass; run tests GREEN for validation subset.
- [ ] Add failing tests for fresh exact-run identity mismatch and `event != pull_request`.
- [ ] Implement exact-run verification.
- [ ] Add failing test for poll sequence `in_progress -> completed`, recording `polling_used=true`.
- [ ] Add failing test for bounded poll exhaustion with no comment.
- [ ] Implement fixed-run bounded polling using injected `sleep_fn` and delays; no latest-run search.
- [ ] Add failing tests for current PR head mismatch.
- [ ] Add failing tests proving Producer B's own marker deduplicates, while a Producer A marker does not suppress Producer B.
- [ ] Implement PR verification, producer-specific marker, packet/comment body, own-marker dedupe and comment creation.
- [ ] Run the full test module with 0 failures/errors.
- [ ] Commit the tests and script as one reviewed TDD unit.

Producer B exact marker:

```text
<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 producer=repository_dispatch_v0_1 run_id=<run_id> attempt=<attempt> pr=<pr> -->
```

Packet version: `chatgpt_ci_completion_push_v0_3`.

---

### Task 2: Receiver workflow in KuuOS

**Files:**
- Create: `.github/workflows/chatgpt-ci-completion-dispatch-v0-1.yml`

- [ ] Add `on.repository_dispatch.types: [chatgpt_ci_completion_dispatch_v0_1]`.
- [ ] Set permissions to `actions: read`, `contents: read`, `issues: write`, `pull-requests: read`.
- [ ] Checkout trusted `main` with `persist-credentials: false`.
- [ ] Run the focused receiver unit tests before processing the event.
- [ ] Execute `scripts/chatgpt_ci_completion_dispatch_v0_1.py --event "$GITHUB_EVENT_PATH"` with `GH_TOKEN=${{ github.token }}` and the current repository.
- [ ] Publish a non-authority job summary including whether bounded polling was used.
- [ ] Static-review that no PR code is checked out under write permissions.

---

### Task 3: Source finalizer in KuuOS Governance Gate

**File:**
- Modify: `.github/workflows/pr-governance-gate.yml`

- [ ] Add finalizer job `chatgpt-completion-dispatch` with `needs: [governance-gate]` and `if: always() && github.event_name == 'pull_request'`.
- [ ] Give this job `contents: write` only.
- [ ] POST same-repository `/dispatches` with event type `chatgpt_ci_completion_dispatch_v0_1` and payload:
  - repository `${{ github.repository }}`
  - pull_request `${{ github.event.pull_request.number }}`
  - run_id `${{ github.run_id }}`
  - run_attempt `${{ github.run_attempt }}`
  - head_sha `${{ github.event.pull_request.head.sha }}`
  - head_branch `${{ github.event.pull_request.head.ref }}`
  - workflow `KuuOS PR Governance Gate`
- [ ] Capture HTTP status in the step summary. Notification dispatch failure must not change the substantive governance result to failure; the finalizer exits successfully after recording a failed dispatch.
- [ ] Add/extend a static test that checks the exact event type, fields, pull-request-only condition and non-fatal dispatch behavior.

---

### Task 4: Equivalent 4d-mass-gap Producer B

**Branch:** create `infra/chatgpt-ci-completion-dispatch-v0-1` from fresh `main`.

**Files:**
- Create: `tests/test_chatgpt_ci_completion_dispatch_v0_1.py`
- Create: `scripts/chatgpt_ci_completion_dispatch_v0_1.py`
- Create: `.github/workflows/chatgpt-ci-completion-dispatch-v0-1.yml`
- Modify: `.github/workflows/pr-lean-fast-check.yml`

- [ ] Port the already-green core script/tests without changing behavioral contract.
- [ ] Add receiver workflow with the same trusted-default-branch/read-actions/write-issues boundary.
- [ ] Add `chatgpt-completion-dispatch` finalizer with `needs: [pr-lean-fast-check]`, pull-request-only condition and job-level `contents: write`.
- [ ] Payload workflow is exactly `PR Lean Fast Check`.
- [ ] Notification dispatch failure is summarized but does not overwrite the Lean check result.
- [ ] Run the focused Python tests.
- [ ] Open a Draft PR to `main`.

---

### Task 5: Fresh PR CI verification and merge sequencing

- [ ] Fresh-observe KuuOS PR #1660 exact head and `KuuOS PR Governance Gate` status/jobs/steps.
- [ ] Fresh-observe the 4d infrastructure PR exact head and `PR Lean Fast Check` status/jobs/steps.
- [ ] Repair any CI errors until exact heads are GREEN.
- [ ] Review changed-file scope and secret scan.
- [ ] Merge each bounded infrastructure PR only after fresh GREEN, exact-head verification, mergeability and repository governance conditions are satisfied.
- [ ] Re-observe default-branch pointers after merge.

Receiver workflows triggered by `repository_dispatch` must exist on the default branch before end-to-end testing.

---

### Task 6: Controlled end-to-end test after merge

For each repository:

- [ ] Trigger one harmless PR CI run on an exact known head.
- [ ] Verify Producer A can create its current wake-up comment.
- [ ] Verify source finalizer emits `repository_dispatch`.
- [ ] Verify Producer B fresh-reads the exact source run and creates its producer-specific wake-up comment.
- [ ] Verify the PR contains both Producer A and Producer B comments for the same run identity when both paths succeed.
- [ ] Verify Work processes that identity only once and writes one `CHATGPT_CI_VERIFIED_HANDOFF_V0_1` receipt.
- [ ] Verify normal Chat can read the handoff and fresh-reobserve the exact run.

---

### Task 7: Completion verification

- [ ] Run receiver unit tests fresh in both repositories.
- [ ] Inspect exact workflow files on merged default branches.
- [ ] Confirm no hourly backstop automation is enabled.
- [ ] Confirm no Slack or Vercel receiver dependency was introduced.
- [ ] Confirm Producer A remains unchanged and functional.
- [ ] Confirm Producer B uses no PAT/secret for same-repository dispatch.
- [ ] Record exact merge SHAs and the controlled E2E run IDs in the handoff summary.
