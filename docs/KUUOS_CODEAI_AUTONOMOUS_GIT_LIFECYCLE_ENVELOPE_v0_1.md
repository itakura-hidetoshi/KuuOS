# KuuOS CodeAI Autonomous Git Lifecycle Envelope v0.1

Status: additive orchestration adapter

Version: v0.1

Predecessor: CodeAI Autonomous Trajectory Synthesis Envelope v0.1

## 1. Purpose

This surface enables a CodeAI executor to progress autonomously through a
bounded Git lifecycle:

```text
local commit
  -> branch push
  -> pull request creation
  -> pull request readiness
  -> required checks
  -> merge gate
  -> pull request merge
  -> completion receipt
```

Each evaluation authorizes at most one next effect. The source trajectory does
not grant Git authority. Authority comes from the exact sealed lifecycle request
and policy, after current effect evidence has been validated.

## 2. Relationship to existing repository surfaces

This profile does not replace the Repository External Approval v0.90 through
Object Materialization Receipt v0.95 series, the v0.96 through v1.24 live Git
mutation series, or Qi PR Merge Gate v2.1.

Those surfaces retain their own validator-owned branches. This adapter provides
a CodeAI-specific orchestration state machine for a conventional development
branch and hosted pull request. An executor may use existing KuuOS live Git
adapters where their narrower contracts apply and may use Git/GitHub operations
only after this surface emits the matching one-effect lease.

## 3. Owned and unowned effects

The policy may own these bounded effects:

- one local commit on an allowed non-base branch;
- one non-force push of the pinned commit to an allowed remote;
- one pull request targeting an allowed base branch;
- marking that exact pull request ready;
- one merge of the pinned head after required gates pass.

The surface never authorizes:

- force push;
- remote branch deletion;
- admin merge or branch-protection bypass;
- deployment or release;
- secret access;
- arbitrary repository, branch, remote, or merge-method selection;
- human notification or external-authority handover.

## 4. Preserved invariants

```text
trajectory receipt != Git authority
one lifecycle receipt <= one next-effect lease
commit authority != push authority
push authority != pull-request authority
pull-request creation != merge authority
checks pending != checks passed
checks passed != correctness proof
mergeable != merged
merged != truth
remote Git effect != human handover
force push / admin bypass / branch deletion != autonomous recovery
```

Every route records the observed prior effects separately from the newly granted
next effect. The kernel itself does not invoke Git or GitHub:

```text
effect_execution_performed_by_kernel = false
```

The autonomous executor is responsible for consuming the lease once and then
returning fresh sealed lifecycle state evidence.

## 5. Inputs

### 5.1 Source trajectory receipt

Only a digest-valid CodeAI Autonomous Trajectory Synthesis v0.1 receipt with:

```text
autonomous_deliberation_candidate_synthesized
autonomous_read_only
verification_outcome = passed
trajectory_complete_for_available_receipts = true
```

is supported. Repair and reverification trajectories cannot enter publication.
The source must report no prior Git effect or successor authority.

### 5.2 Lifecycle request

The sealed request binds:

- lifecycle, revision, session, nonce, and executor identities;
- source trajectory, repository, and source commit;
- base branch, head branch, remote, merge method;
- exact change-set and commit-message digests;
- requested commit, push, pull request, and merge effects;
- destructive-effect and human-handover requests;
- request time and replay lineage.

### 5.3 Lifecycle state

The sealed state is evidence about effects already observed. It records:

- local commit and parent SHA;
- pushed head SHA;
- pull request number, URL digest, draft state, head, and base;
- required-check partitions;
- mergeability and unresolved blockers;
- merge head and resulting merge commit;
- forbidden effect observations;
- observation provenance and time.

The state is monotone. A later phase cannot be true unless every required prior
phase is true and exactly bound.

### 5.4 Lifecycle policy

The sealed policy fixes:

- source trajectory, repository, and source commit;
- authorized executors;
- allowed base branches, head prefixes, remotes, and merge methods;
- required check names;
- per-effect enablement;
- destructive-effect prohibitions;
- non-draft, mergeability, head-pin, and blocker requirements;
- explicit automerge license;
- request and state freshness windows.

## 6. Preflight

Every input uses an exact field set, strict types, and a canonical digest.
Missing, extra, ill-typed, or digest-mismatched data returns `blocked` without a
route receipt.

## 7. Route order

The first matching route wins.

| Priority | Disposition | Mode | Next phase |
|---:|---|---|---|
| 1 | `source_trajectory_receipt_repair_required` | `rejected` | `none` |
| 2 | `git_lifecycle_provenance_repair_required` | `rejected` | `none` |
| 3 | `git_lifecycle_state_evidence_repair_required` | `rejected` | `none` |
| 4 | `git_lifecycle_correspondence_repair_required` | `rejected` | `none` |
| 5 | `git_lifecycle_window_repair_required` | `rejected` | `none` |
| 6 | `git_lifecycle_replay_conflict_rejected` | `rejected` | `none` |
| 7 | `unsupported_git_lifecycle_scope_abstained` | `abstain` | `none` |
| 8 | `destructive_git_effect_rejected` | `rejected` | `none` |
| 9 | `human_handover_deferred` | `hold` | `none` |
| 10 | `git_lifecycle_state_repair_required` | `rejected` | `none` |
| 11 | `autonomous_git_lifecycle_completed` | `completed` | `complete` |
| 12 | `autonomous_local_commit_authorized` | `local_git_effect_authorized` | `local_commit` |
| 13 | `autonomous_branch_push_authorized` | `remote_git_effect_authorized` | `push_branch` |
| 14 | `autonomous_pull_request_creation_authorized` | `pull_request_effect_authorized` | `create_pull_request` |
| 15 | `autonomous_pull_request_readiness_authorized` | `pull_request_effect_authorized` | `mark_pull_request_ready` |
| 16 | `required_checks_pending_hold` | `awaiting_required_checks` | `await_required_checks` |
| 17 | `required_checks_failed_degraded` | `degraded_autonomy` | `await_required_checks` |
| 18 | `pull_request_merge_gate_hold` | `hold` | `await_required_checks` |
| 19 | `autonomous_pull_request_merge_authorized` | `merge_effect_authorized` | `merge_pull_request` |

## 8. Phase contracts

### 8.1 Local commit

The source commit is the required parent. The head branch must be different from
the base branch and match an allowed prefix. The receipt grants only local
commit authority.

### 8.2 Push

Push authority requires an observed 40-hex local commit whose parent is the
bound source commit. Only the allowed remote and head branch are in scope. Force
push remains forbidden.

### 8.3 Pull request

Pull request authority requires the remote branch head to equal the local
commit. The PR must bind the exact base and head. A draft PR receives a separate
readiness lease before checks are eligible for merge gating.

### 8.4 Checks

Once observed, required checks form an exact, duplicate-free partition of:

- successful;
- pending; and
- failed.

Pending checks produce hold. Failed checks produce degraded autonomy and no
merge authority. Success is a merge-gate condition, not correctness proof.

### 8.5 Merge

Merge authority requires all of the following:

- explicit automerge license;
- exact repository, base, head, remote, and merge method;
- non-draft PR;
- pinned PR head equal to the committed and pushed head;
- every required check successful;
- no pending or failed check;
- mergeable state;
- zero unresolved blockers;
- no force push, deletion, or admin bypass.

The authorization is for one merge attempt. A fresh post-merge state must bind
the merged head and a canonical merge commit SHA before the lifecycle becomes
complete.

## 9. Human handover boundary

Remote Git operations and PR merge are effect domains owned by this profile when
explicitly enabled. They are not treated as human handover.

An explicit human-handover request still produces:

```text
codeai_disposition = human_handover_deferred
human_handover_deferred = true
human_handover_performed = false
external_authority_handover_performed = false
```

## 10. Validation

The route checker covers all 19 dispositions. Unit tests cover every lifecycle
phase, destructive-effect rejection, handover deferral, tamper closure, and an
isolated real Git integration that consumes local commit and push leases against
a disposable bare remote.

The independent Lean root proves one-effect authority, phase separation, merge
gate obligations, destructive-effect exclusion, and the distinction between
source provenance and Git authority.

## 11. Implementation map

- Runtime:
  `runtime/kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1.py`
- Checker:
  `scripts/check_codeai_autonomous_git_lifecycle_envelope_v0_1.py`
- Tests:
  `tests/test_kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1.py`
- Example:
  `examples/codeai_autonomous_git_lifecycle_envelope_v0_1.json`
- Manifest:
  `manifests/kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1.json`
- Formal package:
  `formal/KUOS/CodeAI/AutonomousGitLifecycleEnvelopeV0_1.lean`
- Formal root:
  `formal/KuuOSCodeAIAutonomousGitLifecycleV0_1.lean`
- Workflow:
  `.github/workflows/codeai-autonomous-git-lifecycle-envelope-v0-1.yml`

The formal root remains independent and does not change the canonical current
root.
