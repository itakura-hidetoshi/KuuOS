# KuuOS CodeAI Autonomous Isolated Candidate Application v0.1

Status: additive isolated-materialization sibling

Version: v0.1

Predecessor: CodeAI Autonomous Candidate Portfolio Selection v0.1

## 1. Purpose

This surface converts one governed selected Candidate Patch target into a
deterministic **isolated repository text snapshot** for independent verification.
It applies the selected canonical unified diff to a supplied read-only source
snapshot in memory and records exact source/result correspondence.

```text
selected independent-verification target
  + sealed candidate-selection receipt
  + canonical read-only repository text snapshot
  + sealed isolated-application request
  + bounded isolated-application policy
  -> deterministic in-memory patch application
  -> isolated resulting snapshot and digest
  -> application receipt for verification-workspace preparation
```

The output is not a live checkout, working tree, index, Git tree object, branch,
commit, push, pull request, merge, or deployment. It is a value-level snapshot
that a separate verifier may materialize in an isolated environment.

## 2. Boundary

Autonomous Candidate Portfolio Selection v0.1 chooses one verification target but
does not apply it. This sibling owns the next narrow transformation: it proves
correspondence, parses the canonical unified diff, applies hunks to an in-memory
copy, and emits a sealed receipt.

It does not:

- write the supplied source mapping;
- write a live filesystem;
- modify a Git index, object database, ref, branch, or commit;
- execute tests or verification commands;
- assert correctness;
- issue verification, execution, merge, deployment, or secret authority.

## 3. Inputs

The runtime consumes five values:

1. a sealed Autonomous Candidate Portfolio Selection v0.1 receipt whose route
   selected one candidate for independent verification;
2. the corresponding `SelectedVerificationCandidate` value;
3. a canonical read-only mapping from repository-relative paths to UTF-8 text;
4. a sealed isolated-application request;
5. a sealed isolated-application policy.

The source snapshot supports text only. Paths must be canonical repository paths.
Text must contain no NUL or CR and must be empty or LF-terminated.

## 4. Request

The request binds:

- stable request identifier and revision;
- exact source selection receipt digest;
- exact selected candidate digest;
- exact source repository snapshot digest;
- purpose `independent_verification_workspace`;
- requesting actor;
- request creation epoch;
- canonical request digest.

A stale or mismatched request blocks before parsing or application.

## 5. Policy

The sealed policy binds:

- expected selection receipt, candidate, artifact, repository, commit, and source
  snapshot digests;
- source and result path-count budgets;
- source and result byte budgets;
- patch-byte and changed-path budgets;
- allowed and forbidden changed-path prefixes;
- explicit permission for add, modify, and delete operations;
- exact changed-path accounting requirement;
- evaluation epoch and maximum request age.

The v0.1 default posture is fail closed. Unsupported paths, operations, sizes,
ages, formats, and correspondence all block.

## 6. Selection correspondence

Before parsing the patch, the runtime requires exact agreement among:

- selection receipt selected candidate ID;
- selection receipt selected candidate digest;
- selection receipt selected patch artifact digest;
- selection receipt selected upstream rank;
- `SelectedVerificationCandidate` fields;
- canonical Candidate Patch digest;
- canonical Candidate Patch receipt digest;
- actual patch artifact digest and byte length;
- request and policy bindings.

Selection correspondence is not correctness. It only establishes that the
materialized artifact is exactly the artifact selected upstream.

## 7. Unified diff profile

v0.1 accepts the canonical text profile emitted by Autonomous Unified Diff
Candidates v0.1:

- `diff --git a/<path> b/<path>` sections;
- optional `new file mode 100644` or `deleted file mode 100644`;
- canonical `---` and `+++` labels;
- one or more standard unified-diff hunks;
- context, addition, and deletion body lines;
- no rename, binary, submodule, mode-change, or no-newline marker.

Each path may appear once. Add, modify, and delete labels must match the declared
operation exactly.

## 8. Deterministic hunk application

For each section the runtime:

1. resolves the old source text from the input snapshot;
2. checks every hunk start and declared old/new line count;
3. checks every context and deletion line against the source;
4. constructs the new text from copied context and additions;
5. requires canonical LF output;
6. applies the result to a copy of the mapping;
7. verifies exact changed, added, modified, and deleted path accounting.

Any context or deletion mismatch blocks. Fuzzy application and offset search are
intentionally absent in v0.1.

## 9. Result and receipt

A successful result contains:

- a new repository text mapping;
- source and resulting snapshot digests;
- source and resulting path counts and byte sizes;
- exact changed/add/modify/delete paths;
- content digests for resulting changed paths;
- tombstones for deleted paths;
- a sealed isolated-application receipt.

The input mapping remains unchanged.

## 10. Stable invariants

```text
selected candidate != applied live patch
isolated patch application != repository mutation
isolated snapshot != Git tree object
verification workspace ready != verification executed
materialization != verification
materialization != correctness proof
application receipt != execution authority
application receipt != Git authority
application receipt != deployment or secret authority
```

## 11. Failure modes

The route blocks on, among other conditions:

- selection receipt tamper or unsupported route;
- selected candidate or Candidate Patch receipt tamper;
- artifact digest or byte-count mismatch;
- source snapshot digest mismatch;
- repository or source commit mismatch;
- stale request;
- source/result/patch/change budget excess;
- forbidden or unallowed changed paths;
- disallowed add, modify, or delete operation;
- malformed unified diff;
- repeated path;
- invalid labels or hunk counts;
- context or deletion mismatch;
- changed-path accounting mismatch;
- noncanonical resulting text.

Blocked routes return no resulting snapshot and no success receipt.

## 12. Formal surface

The Lean package records that a valid materialization receipt:

- prepares an isolated verification workspace;
- leaves the input and live repository unchanged;
- performs no Git effect;
- executes no verification;
- grants no successor authority;
- treats neither the selected candidate nor materialization as correctness.

## 13. Implementation map

- Runtime: `runtime/kuuos_codeai_autonomous_isolated_candidate_application_v0_1.py`
- Checker: `scripts/check_codeai_autonomous_isolated_candidate_application_v0_1.py`
- Tests: `tests/test_kuuos_codeai_autonomous_isolated_candidate_application_v0_1.py`
- Example: `examples/codeai_autonomous_isolated_candidate_application_v0_1.json`
- Manifest: `manifests/kuuos_codeai_autonomous_isolated_candidate_application_v0_1.json`
- Lean kernel: `formal/KUOS/CodeAI/AutonomousIsolatedCandidateApplicationV0_1.lean`
- Lean root: `formal/KuuOSCodeAIAutonomousIsolatedCandidateApplicationV0_1.lean`
- Workflow: `.github/workflows/codeai-autonomous-isolated-candidate-application-v0-1.yml`

## 14. Conditional next stages

Later siblings may execute a declared verification command plan against the
isolated snapshot, bind resulting evidence to this application receipt, generate
a repair/regeneration loop, or provide rollback receipts for live application.
Those capabilities remain unowned here.
