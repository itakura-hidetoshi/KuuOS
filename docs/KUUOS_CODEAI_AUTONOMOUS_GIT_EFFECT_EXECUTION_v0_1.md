# CodeAI Autonomous Git Effect Execution v0.1

## Status

Additive bounded operational adapter.

This stage is the execution successor of **CodeAI Autonomous Git Lifecycle v0.1**. The lifecycle kernel issues at most one active lease for one exact phase. This stage consumes that lease once, invokes one structured adapter, records effect evidence, and advances a sealed replay registry.

```text
active one-effect lifecycle receipt
+ sealed effect request
+ deny-by-default policy
+ sealed replay registry
+ structured Git/GitHub adapter
  -> exact phase / repository / branch / head correspondence
  -> one adapter invocation
  -> completed / failed / evidence-quarantined outcome
  -> lease and nonce consumption
  -> monotone next registry
  -> sealed execution receipt
```

## Supported phases

Exactly five effect-bearing lifecycle phases are executable:

1. `local_commit`
2. `push_branch`
3. `create_pull_request`
4. `mark_pull_request_ready`
5. `merge_pull_request`

`await_required_checks`, `complete`, and `none` are not executable.

## Lease consumption and replay closure

The source receipt must be sealed, active, future-only, and grant exactly one authority bit corresponding to its disposition, operating mode, and `next_effect_phase`. It must record no force push, branch deletion, admin bypass, deployment, secret access, checks-wait hold, or human handover.

The request preserves the lifecycle id, executor, repository, source commit, base/head branches, remote, merge method, change-set digest, commit-message digest, and effect phase. A lifecycle receipt digest or nonce already in the registry is rejected before adapter invocation.

Once an admitted invocation begins, the lease is consumed regardless of outcome:

- `completed`: exact effect-specific evidence confirms completion;
- `failed`: bounded adapter failure with no confirmed effect;
- `evidence_quarantined`: malformed, forbidden, over-budget, or internally contradictory evidence.

A failed or quarantined attempt cannot reuse the lease. Fresh observation and a fresh lifecycle receipt are required.

## Structured subprocess adapter

The adapter maps the invocation to exact commands. It does not accept arbitrary shell fragments.

### Local commit

```text
git rev-parse HEAD
-> exact source SHA check
git commit --no-gpg-sign -m <bound message>
git rev-parse HEAD
git rev-parse HEAD^
```

### Push

```text
git rev-parse HEAD
-> exact pinned head check
git push --porcelain <remote> HEAD:refs/heads/<head-branch>
```

No force flag is available.

### Pull request creation

```text
gh pr create
  --repo <bound repository>
  --base <bound base>
  --head <bound head>
  --title <bound title>
  --body-file -
  --draft
```

The adapter re-observes PR number, URL, draft status, head SHA, and base branch.

### Readiness

```text
gh pr ready <bound PR number> --repo <bound repository>
```

The PR is re-observed and must no longer be Draft.

### Merge

```text
gh pr merge <bound PR number>
  --repo <bound repository>
  --merge | --squash | --rebase
  --match-head-commit <bound head SHA>
```

The adapter never supplies `--admin` or `--delete-branch`. It re-observes the merged head and merge commit.

## Opaque token boundary

Remote GitHub phases may consume an opaque `GH_TOKEN` through the process environment. Token material is not accepted as a request field or command argument, and evidence must record:

```text
secret_material_read = false
token_material_emitted = false
```

Opaque token use is capability consumption, not authority to inspect or emit the token.

## Merge gate inheritance

Merge is admitted only when the lifecycle receipt already records a non-Draft PR, all required checks successful, no pending or failed checks, mergeability, zero unresolved blockers, and a head SHA pin. The adapter repeats the head pin with `--match-head-commit`.

## Fixed boundaries

```text
lifecycle lease != effect execution
effect request != general Git authority
one invocation != reusable capability
failed attempt != retry authority
quarantined evidence != confirmed no-effect
checks passed != correctness proof
merge completed != truth
opaque token use != secret material read
commit authority != push authority
push authority != PR authority
PR authority != readiness authority
readiness authority != merge authority
```

The receipt grants no automatic successor effect, deployment authority, general Git authority, or general successor-stage authority.

## Artifacts

- kernel: `runtime/kuuos_codeai_autonomous_git_effect_execution_v0_1.py`
- types: `runtime/kuuos_codeai_autonomous_git_effect_execution_types_v0_1.py`
- validation: `runtime/kuuos_codeai_autonomous_git_effect_execution_validation_v0_1.py`
- subprocess adapter: `runtime/kuuos_codeai_git_subprocess_effect_adapter_v0_1.py`
- checker: `scripts/check_codeai_autonomous_git_effect_execution_v0_1.py`
- tests: `tests/test_kuuos_codeai_autonomous_git_effect_execution_v0_1.py`, `tests/test_kuuos_codeai_git_subprocess_effect_adapter_v0_1.py`
- example: `examples/codeai_autonomous_git_effect_execution_v0_1.json`
- manifest: `manifests/kuuos_codeai_autonomous_git_effect_execution_v0_1.json`
- formal kernel: `formal/KUOS/CodeAI/AutonomousGitEffectExecutionV0_1.lean`
- formal root: `formal/KuuOSCodeAIAutonomousGitEffectExecutionV0_1.lean`
- workflow: `.github/workflows/codeai-autonomous-git-effect-execution-v0-1.yml`

## Validation

The dedicated workflow compiles Python, validates JSON, runs 15 fail-closed and command-mapping tests, performs a real local commit in a disposable repository, verifies exact non-force push and Draft PR/readiness/head-pinned merge command construction, and strictly compiles both the new Lean root and `KuuOSFormal`. The workflow itself performs no live GitHub write effect.
