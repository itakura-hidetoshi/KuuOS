# KuuOS CodeAI Verification-Guided Candidate Repair and Regeneration v0.1

## Status

This profile is an additive, proposal-only CodeAI stage. It consumes failed or
runtime-budget-aborted verification execution evidence, reduces it to bounded
feedback, and invokes the existing provider-neutral candidate regeneration
kernel. It never treats a failed check as truth, a required edit, or authority.

## Route

```text
supported Candidate Patch receipt
  + isolated application receipt
  + failed / aborted Autonomous Verification Execution receipt
  + sealed execution evidence bundle
  + Independent Verification evidence projection
  + source generation and observation lineage
  + read-only source repository snapshot
  + fresh sealed repair request
  + bounded repair-feedback policy
  + provider-neutral generation adapters
  -> normalized bounded feedback
  -> Autonomous Candidate Regeneration v0.1
  -> zero or more novel, unselected, unverified candidates
  -> sealed repair-regeneration receipt
```

## Exact lineage admission

The runtime rejects the route unless all of the following correspond exactly:

- verification execution receipt digest;
- execution evidence bundle digest;
- independent-verification evidence digest;
- source Candidate Patch receipt digest;
- source isolated-application receipt digest;
- source generation receipt digest;
- source observation receipt digest;
- candidate and patch-artifact digests;
- repository full name and source commit SHA;
- source repository snapshot digest;
- verification, evidence, candidate, application, and generation cross-links;
- repair request and repair policy digests;
- selected candidate membership in the source seed lineage.

Only `verification_execution_completed_with_failures` and
`verification_execution_aborted_by_runtime_budget` are repairable source
dispositions. A passed verification execution is not routed through this
profile.

## Bounded feedback normalization

Each failed evidence record is reduced to:

- admitted check ID and execution status;
- bounded failure-reason identifiers;
- exit code, timeout flag, and exception type;
- stdout and stderr digests;
- separately bounded stdout and stderr excerpts;
- source evidence-record digest.

Raw full output is not forwarded. Check IDs, execution statuses, finding
labels, failure-reason prefixes, record count, reasons per record, excerpt
bytes, and total serialized feedback bytes are policy-bounded. Any mismatch or
budget excess blocks the route.

## Regeneration composition

The normalized feedback is embedded as context-only input to
`CodeAI Autonomous Candidate Regeneration v0.1`. The repair policy derives a
strict downstream regeneration policy that bounds:

- repair rounds;
- provider calls per round and in total;
- provider IDs and diversity axes;
- raw provider output and intent bytes;
- repository snapshot bytes;
- existing, added, combined, and unique candidate counts;
- allowed and forbidden repository path prefixes;
- request and response freshness.

Candidate and semantic patch duplication remain rejected by the downstream
regeneration kernel. The output candidates remain proposal-only, unselected,
unapplied, and unverified.

## Fixed boundaries

```text
verification failure != repair truth
failed check != required edit
repair feedback != authority
repair regeneration != correction
new candidate != verified patch
tests passing after repair != proof
repair ranking != selection
evidence-guided novelty != requirement satisfaction
repair loop != live repository mutation
repair receipt != successor authority
```

The policy must deny network, secret, live-repository, and Git-operation
capabilities. The receipt records no selection, verification, execution,
merge, deployment, secret, or successor-stage authority.

## Outputs

The runtime returns:

1. a sealed normalized feedback object;
2. the downstream Autonomous Candidate Regeneration result;
3. a sealed verification-guided repair-regeneration receipt.

The receipt records exact source digests, bounded counts, the downstream
regeneration receipt digest, route facts, non-effect facts, and non-authority
facts.

## Validation

```bash
PYTHONPATH=. python3 \
  scripts/check_codeai_verification_guided_candidate_repair_regeneration_v0_1.py

PYTHONPATH=. python3 -m unittest \
  tests.test_kuuos_codeai_verification_guided_candidate_repair_regeneration_v0_1

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSCodeAIVerificationGuidedCandidateRepairRegenerationV0_1

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
