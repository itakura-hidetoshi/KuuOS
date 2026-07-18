# KuuOS CodeAI Autonomous Verification Execution v0.1

Status: additive bounded execution sibling

Version: v0.1

Predecessor: CodeAI Autonomous Isolated Candidate Application v0.1

Evidence consumer: CodeAI Independent Verification v0.1

## 1. Purpose

This surface executes a sealed verification plan against the exact isolated
repository snapshot produced for one selected Candidate Patch. Execution is
performed only through a runner-neutral adapter and only after exact receipt,
candidate, artifact, repository, commit, snapshot, request, plan, and policy
correspondence has been established.

```text
selected Candidate Patch receipt
  + isolated application receipt
  + exact resulting isolated repository snapshot
  + sealed verification plan
  + fresh sealed execution request
  + bounded execution policy
  + runner-neutral adapter
  -> bounded per-check execution evidence
  -> sealed evidence bundle
  -> Independent Verification v0.1 compatible evidence projection
  -> sealed verification execution receipt
```

The stage closes the gap between preparing a verification workspace and actually
collecting verification execution evidence. It does not decide correctness and
it does not acquire repository or merge authority.

## 2. Required correspondence

Before the runner adapter is called, the kernel verifies exact correspondence for:

- Candidate Patch receipt digest;
- isolated application receipt digest;
- candidate digest;
- patch artifact digest;
- source repository snapshot digest;
- resulting isolated repository snapshot digest;
- repository full name;
- source commit SHA;
- verification plan digest;
- execution request digest and freshness;
- execution policy digest.

Any mismatch blocks all runner calls.

## 3. Verification plan

A plan is a sealed ordered list of checks. Each check declares:

- a stable check identifier;
- an executable;
- ordered arguments;
- a work directory inside the isolated workspace;
- a per-check timeout;
- accepted exit codes;
- an explicit environment map.

The policy independently restricts allowed check identifiers, executable
prefixes, work-directory prefixes, and environment keys. The plan is therefore
data, not authority.

## 4. Bounded execution policy

The policy bounds:

- command count;
- per-check timeout;
- aggregate timeout;
- stdout bytes per check;
- stderr bytes per check;
- aggregate output bytes;
- repository path count;
- repository snapshot size;
- request age.

The v0.1 policy requires all of the following to be false:

- network access;
- secret access;
- live repository access;
- Git operations.

A plan that requests a disallowed executable, work directory, environment key, or
budget blocks before execution.

## 5. Runner-neutral adapter

The adapter receives an immutable contract containing the admitted command and a
copy of the resulting isolated repository snapshot. It is not given a live
repository handle, Git capability, secret capability, or network capability.

The adapter reports:

- runner and session identifiers;
- check identifier;
- exit code;
- stdout and stderr;
- duration;
- timeout state;
- exception type;
- start and completion epochs;
- whether network, secret, live-repository, or Git effects occurred.

Adapter exceptions are isolated to the affected check. Already collected sibling
evidence is retained and later checks remain eligible to run while budgets allow.

## 6. Evidence semantics

Every check produces a sealed record containing:

- invocation digest;
- exit code and accepted exit codes;
- stdout and stderr digests;
- bounded excerpts;
- original byte counts;
- truncation flags;
- duration;
- timeout and exception state;
- effect-report fields;
- runner-result rejection reasons;
- record digest.

A timeout, exception, malformed result, disallowed effect, non-accepted exit code,
or output-budget violation is failed evidence. None is interpreted as success.

The ordered records are sealed into an evidence bundle with exact passed and
failed check accounting.

## 7. Independent Verification projection

The surface emits a projection compatible with CodeAI Independent Verification
v0.1. The projection binds the evidence to the Candidate Patch receipt and carries
check accounting, runner evidence digests, provenance metadata, and a declared
passed or failed outcome.

Independent Verification remains a separate governed stage. Producing compatible
evidence is not equivalent to accepting it, treating it as truth, or granting
merge authority.

## 8. Runtime failure behavior

Static correspondence, freshness, policy, plan, and budget failures block before
runner invocation.

Runtime failures are recorded rather than erased:

- a nonzero exit becomes failed evidence;
- a timeout becomes failed evidence;
- an adapter exception becomes failed evidence;
- a malformed adapter result becomes rejected evidence;
- a reported network, secret, live-repository, or Git effect becomes rejected
  evidence;
- per-check output excess is truncated and marked failed;
- aggregate output excess aborts remaining calls and seals the evidence collected
  so far.

## 9. Preserved boundaries

```text
execution != correctness
tests passing != proof
verification evidence != merge authority
runner exception != success
verification plan != execution authority
runner adapter != live repository capability
isolated verification execution != live patch application
execution receipt != Git authority
execution receipt != deployment authority
execution receipt != secret authority
execution receipt != successor-stage authority
```

The stage does not select candidates, modify the live filesystem, alter Git refs,
create branches or commits, push, create pull requests, merge, deploy, obtain
secrets, enable network access, or automatically invoke a successor stage.

## 10. Validation

The implementation includes:

- an integration checker for generation, portfolio selection, isolated application,
  bounded verification execution, and Independent Verification evidence intake;
- 13 fail-closed unit tests covering successful execution, failed exits, timeout,
  exception isolation, exact correspondence, snapshot drift, freshness, command
  budgets, executable admission, environment allowlists, effect rejection, output
  bounds, evidence projection, and no-authority invariants;
- a strict Lean formal root;
- a dedicated GitHub Actions workflow that also compiles the full `KuuOSFormal`
  baseline.
