# CI Completion Receiver Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an independent Vercel-hosted raw GitHub `workflow_run.completed` receiver that redundantly emits the same idempotent ChatGPT wake-up comment as the existing GitHub Actions notifier for KuuOS and 4d-mass-gap.

**Architecture:** Keep the current GitHub Actions notifier as Producer A. Add Producer B under KuuOS source control, deployed into the existing Vercel project `kuuos-chat-work-mcp`, with a single authenticated webhook endpoint `/api/github/workflow-run`. Producer B verifies the exact workflow run via GitHub API, resolves the exact PR, and writes the existing canonical marker only when no identical marker is already present.

**Tech Stack:** Python 3.12, standard library HTTP/JSON/HMAC helpers where applicable, Vercel Python Functions, Vercel Connect GitHub app credentials/OIDC, GitHub REST API, `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-17-ci-completion-receiver-design.md`

## Global Constraints

- Supported repositories are exactly `itakura-hidetoshi/KuuOS` and `itakura-hidetoshi/4d-mass-gap`.
- Supported workflows are exactly `KuuOS PR Governance Gate` and `PR Lean Fast Check` respectively.
- Canonical wake-up marker remains `CHATGPT_CI_COMPLETION_PUSH_V0_1`.
- Wake-up comments are not CI truth and grant no merge/write authority.
- Exact identity uses repository + PR + run_id + run_attempt + head_sha.
- Producer B must fresh-read the exact GitHub run before commenting.
- No Slack dependency.
- No hourly polling backstop.
- Existing Work handoff `CHATGPT_CI_VERIFIED_HANDOFF_V0_1` remains unchanged.
- KuuOS PR #1558 remains non-mergeable by policy.

---

## File Structure

- Create `services/ci_completion_receiver/core.py` — pure validation, workflow allowlist, PR resolution, marker/packet construction.
- Create `services/ci_completion_receiver/github_api.py` — narrow GitHub REST client used by the receiver.
- Create `services/ci_completion_receiver/handler.py` — orchestration from verified webhook payload to deduplicated PR comment.
- Create `api/github/workflow-run.py` — Vercel Python Function route; authenticates inbound Vercel Connect/OIDC request, parses payload, delegates to handler.
- Create `tests/test_ci_completion_receiver_core.py` — pure TDD coverage for validation, PR resolution, marker and packet.
- Create `tests/test_ci_completion_receiver_handler.py` — behavior coverage using a fake GitHub client.
- Create `tests/test_ci_completion_receiver_route.py` — route-level request validation/authentication adapter tests.
- Create `pyproject.toml` additions only if the existing repository configuration requires explicit package discovery; otherwise avoid dependency expansion.
- Modify `docs/superpowers/specs/2026-09-17-ci-completion-receiver-design.md` only if implementation reveals a genuine contract mismatch.

---

### Task 1: Pure receiver core

**Files:**
- Create: `tests/test_ci_completion_receiver_core.py`
- Create: `services/ci_completion_receiver/__init__.py`
- Create: `services/ci_completion_receiver/core.py`

**Interfaces:**
- Produces `WorkflowIdentity`, `validate_event(payload)`, `resolve_pr_numbers(...)`, `comment_marker(...)`, and `build_wakeup_packet(...)`.
- No network access.

- [ ] **Step 1: Write failing tests for repository/workflow/status validation**

```python
from services.ci_completion_receiver.core import validate_event


def valid_payload(repo, workflow):
    return {
        "action": "completed",
        "repository": {"full_name": repo},
        "workflow_run": {
            "id": 123,
            "run_attempt": 1,
            "name": workflow,
            "status": "completed",
            "conclusion": "success",
            "head_sha": "a" * 40,
            "head_branch": "feature/x",
            "head_repository": {"full_name": repo},
            "pull_requests": [],
            "html_url": "https://github.com/example/actions/runs/123",
            "updated_at": "2026-09-18T00:00:00Z",
        },
    }


def test_accepts_kuuos_completed_workflow():
    identity = validate_event(valid_payload(
        "itakura-hidetoshi/KuuOS", "KuuOS PR Governance Gate"))
    assert identity.repository == "itakura-hidetoshi/KuuOS"
    assert identity.run_id == 123


def test_rejects_wrong_repository():
    assert validate_event(valid_payload("someone/else", "KuuOS PR Governance Gate")) is None


def test_rejects_wrong_workflow():
    assert validate_event(valid_payload("itakura-hidetoshi/KuuOS", "Other Workflow")) is None


def test_rejects_non_completed_status():
    payload = valid_payload("itakura-hidetoshi/KuuOS", "KuuOS PR Governance Gate")
    payload["workflow_run"]["status"] = "in_progress"
    assert validate_event(payload) is None
```

- [ ] **Step 2: Run the tests and verify RED**

Run: `python -m unittest -v tests.test_ci_completion_receiver_core`

Expected: import failure because `services.ci_completion_receiver.core` does not exist.

- [ ] **Step 3: Implement the minimal core validation types/functions**

Implement a frozen dataclass `WorkflowIdentity` with fields:
`repository, workflow, run_id, run_attempt, head_sha, head_branch, conclusion, run_url, updated_at, direct_pr_numbers`.

`validate_event(payload)` must return `None` for any repository/workflow/status/head-repository mismatch and must require positive integer `run_id`/`run_attempt` plus a 40-hex-character `head_sha`.

- [ ] **Step 4: Add failing tests for exact PR resolution**

Cover direct PR list, empty list fallback association, wrong head SHA, wrong head repository, and deduplication.

- [ ] **Step 5: Run and verify those tests fail for missing behavior**

Run: `python -m unittest -v tests.test_ci_completion_receiver_core`

- [ ] **Step 6: Implement `resolve_pr_numbers`**

Signature:

```python
def resolve_pr_numbers(
    direct_pr_numbers: tuple[int, ...],
    associated_pull_requests: list[dict],
    *,
    head_sha: str,
    repository: str,
) -> list[int]: ...
```

Direct PRs win when non-empty. Fallback PRs require exact `head.sha` and `head.repo.full_name`.

- [ ] **Step 7: Add failing tests for marker and packet contract**

Assert exact marker:

```text
<!-- CHATGPT_CI_COMPLETION_PUSH_V0_1 run_id=123 attempt=1 pr=77 -->
```

and packet field `producer == "vercel_raw_webhook"`.

- [ ] **Step 8: Implement marker/packet builders and run GREEN**

Run: `python -m unittest -v tests.test_ci_completion_receiver_core`

Expected: all core tests pass.

- [ ] **Step 9: Commit**

Commit message: `Add tested CI completion receiver core`

---

### Task 2: Narrow GitHub REST adapter

**Files:**
- Create: `services/ci_completion_receiver/github_api.py`
- Create/extend: `tests/test_ci_completion_receiver_handler.py`

**Interfaces:**
- Produces class `GitHubApi` with methods:
  - `get_workflow_run(repository: str, run_id: int) -> dict`
  - `get_associated_pulls(repository: str, head_sha: str) -> list[dict]`
  - `list_issue_comments(repository: str, pr_number: int) -> list[dict]`
  - `create_issue_comment(repository: str, pr_number: int, body: str) -> dict`
- Authentication token is supplied at construction; no token logging.

- [ ] **Step 1: Write handler tests using a fake client before implementing production adapter**

Define a minimal fake implementing the four methods above. Tests assert network orchestration through the interface rather than urllib internals.

- [ ] **Step 2: Verify RED because handler is absent**

Run: `python -m unittest -v tests.test_ci_completion_receiver_handler`

- [ ] **Step 3: Implement `GitHubApi` using stdlib `urllib.request`**

Headers must include GitHub API version `2022-11-28`, JSON accept header, bearer token, and a fixed user-agent.

- [ ] **Step 4: Keep adapter minimal; run syntax/import checks**

Run: `python -m py_compile services/ci_completion_receiver/github_api.py`

- [ ] **Step 5: Commit**

Commit message: `Add GitHub API adapter for CI receiver`

---

### Task 3: Receiver orchestration and idempotency

**Files:**
- Create: `services/ci_completion_receiver/handler.py`
- Extend: `tests/test_ci_completion_receiver_handler.py`

**Interfaces:**
- Produces `process_workflow_run_event(payload: dict, github: GitHubApiLike) -> dict`.
- Result shape contains `outcome` with one of `ignored`, `identity_mismatch`, `no_pr`, `deduplicated`, `comment_created` and includes exact run metadata when accepted.

- [ ] **Step 1: Write failing test for fresh exact-run verification**

Webhook payload says run 123/head A; fake API returns run 123/head B. Assert outcome `identity_mismatch` and zero comment writes.

- [ ] **Step 2: Write failing test for empty PR list fallback**

Webhook direct PR list empty; fake associated pulls contains exact head/repo PR 77. Assert comment is written to PR 77.

- [ ] **Step 3: Write failing test for idempotency**

Fake comments already contain exact canonical marker. Assert outcome `deduplicated` and zero comment writes.

- [ ] **Step 4: Verify RED**

Run: `python -m unittest -v tests.test_ci_completion_receiver_handler`

- [ ] **Step 5: Implement minimal handler**

Processing order:
1. `validate_event`.
2. Fresh exact `get_workflow_run`.
3. Verify exact run_id/run_attempt/head_sha/name/status/repository.
4. Resolve PRs from webhook direct list or one associated-pulls request.
5. For each PR, search comments for exact marker.
6. Create one comment only when absent.

- [ ] **Step 6: Run handler tests GREEN**

Run: `python -m unittest -v tests.test_ci_completion_receiver_handler`

- [ ] **Step 7: Run core + handler tests together**

Run: `python -m unittest -v tests.test_ci_completion_receiver_core tests.test_ci_completion_receiver_handler`

- [ ] **Step 8: Commit**

Commit message: `Implement idempotent raw CI completion handler`

---

### Task 4: Vercel webhook route and authentication boundary

**Files:**
- Create: `api/github/workflow-run.py`
- Create: `tests/test_ci_completion_receiver_route.py`
- Modify/create only if needed: `requirements.txt` or `pyproject.toml`

**Interfaces:**
- HTTP POST `/api/github/workflow-run`.
- Uses Vercel Connect/OIDC-authenticated GitHub channel credentials where available in the existing Python project; if the current project cannot expose Vercel Connect verification directly in Python, use the smallest supported Vercel authentication adapter and document the exact mechanism.
- Reject unauthenticated requests before parsing actions.

- [ ] **Step 1: Write failing route tests for method/auth/payload validation**

Cases:
- non-POST rejected,
- missing/invalid auth rejected,
- malformed JSON rejected,
- valid authenticated ignored event returns 2xx no-op,
- valid authenticated completed event delegates once.

- [ ] **Step 2: Run tests RED**

Run: `python -m unittest -v tests.test_ci_completion_receiver_route`

- [ ] **Step 3: Implement route adapter only**

The route must not contain business logic already covered by `handler.py`.

- [ ] **Step 4: Run route tests GREEN**

Run: `python -m unittest -v tests.test_ci_completion_receiver_route`

- [ ] **Step 5: Run all receiver tests**

Run: `python -m unittest -v tests.test_ci_completion_receiver_core tests.test_ci_completion_receiver_handler tests.test_ci_completion_receiver_route`

- [ ] **Step 6: Commit**

Commit message: `Add authenticated Vercel workflow-run route`

---

### Task 5: Deploy Producer B to existing Vercel project

**Files/Platform:**
- Vercel project: `kuuos-chat-work-mcp`
- Production route: `/api/github/workflow-run`

**Interfaces:**
- Deployment source must match the reviewed KuuOS branch content.
- Production project remains `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`.

- [ ] **Step 1: Verify all local/repository tests are green before deployment**

Use the exact full unittest command from Task 4.

- [ ] **Step 2: Deploy reviewed source to `kuuos-chat-work-mcp`**

Use the connected Vercel deployment capability. Do not create a second project unless the existing project cannot support the isolated route without breaking its current behavior.

- [ ] **Step 3: Verify deployment READY and route health**

GET or unsupported method may return 405/appropriate response; a signed/authorized synthetic ignored event must return 2xx no-op.

- [ ] **Step 4: Inspect runtime logs for receiver startup/runtime errors**

No uncaught exceptions or secret-bearing logs.

- [ ] **Step 5: Record deployment ID and production alias in PR #1660**

No secrets in comments.

---

### Task 6: Connect raw GitHub workflow-run webhooks

**Platform:**
- Vercel Connect GitHub app installation for both repositories.
- Event class: GitHub `workflow_run` completed events.

- [ ] **Step 1: Create or reuse one app-scoped GitHub Vercel Connect connector**

The connector must be installed for both target repositories and forward authenticated webhook requests to the production receiver route.

- [ ] **Step 2: Confirm event delivery scope**

Receiver itself remains the final allowlist for exact repositories/workflow names/status.

- [ ] **Step 3: Trigger a controlled completion event in KuuOS**

Re-run one safe existing successful CI job/run or create the smallest harmless PR-triggered CI event if rerun semantics do not emit the required webhook.

- [ ] **Step 4: Verify one canonical marker and no duplicate**

Confirm Producer A or B writes the marker and the second producer detects it.

- [ ] **Step 5: Repeat controlled test for 4d-mass-gap**

Use exact run/head verification.

---

### Task 7: End-to-end Work handoff verification

**Files/Platform:**
- Existing Work task `CI完了コメント受信`.
- GitHub PR conversation comments.

- [ ] **Step 1: Confirm Work consumes the canonical wake-up marker**

Use a controlled terminal run and observe the Work task result.

- [ ] **Step 2: Verify exact MCP re-observation**

Require same repository/run_id/run_attempt/head_sha and terminal job/step evidence.

- [ ] **Step 3: Verify exactly one durable handoff**

PR conversation must contain exactly one `CHATGPT_CI_VERIFIED_HANDOFF_V0_1` for that exact identity.

- [ ] **Step 4: Verify normal Chat can continue from the handoff**

Read the handoff through GitHub MCP and fresh-check the exact run before any governed action.

---

### Task 8: Final verification and integration

**Files:**
- Review all files changed in PR #1660.

- [ ] **Step 1: Run the full receiver test suite fresh**

Run:
`python -m unittest -v tests.test_ci_completion_receiver_core tests.test_ci_completion_receiver_handler tests.test_ci_completion_receiver_route`

Expected: 0 failures, 0 errors.

- [ ] **Step 2: Verify PR changed-file scope**

Only design/plan, receiver service, route, and receiver tests/configuration required by the implementation.

- [ ] **Step 3: Verify no forbidden secret material**

Search changed content for GitHub tokens, private keys, webhook secrets, raw authorization values.

- [ ] **Step 4: Verify live production receiver**

Production deployment READY; recent controlled webhook produced expected outcome; no duplicate wake-up marker.

- [ ] **Step 5: Keep PR Draft until end-to-end verification is complete**

Only then consider normal repository governance for readiness/merge.
