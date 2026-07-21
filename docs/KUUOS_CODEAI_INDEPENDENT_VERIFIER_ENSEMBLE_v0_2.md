# CodeAI Independent Verifier Ensemble v0.2

## Purpose

This additive stage evolves the single independently reviewed verification envelope into a content-addressed ensemble of independently produced verification packets. It consumes one exact candidate/context lineage and several sealed verifier packets, validates their independence and coverage, and records a bounded consensus, failure, disagreement hold, or inconclusive hold.

The kernel does not execute verification, generate tests, modify a repository, select or reject a candidate, grant execution or Git authority, or prove correctness.

## Why an ensemble

One verifier can reproduce the same blind spots as the candidate producer, reuse the same prompt or memory, or cover only one check family. v0.2 therefore requires independent evidence across distinct organizations, sessions, verification methods, and four complementary families:

1. `type_and_formal`;
2. `behavioral_and_regression`;
3. `adversarial_and_falsification`;
4. `maintainability_and_static`.

The ensemble is not a popularity vote. Critical falsification overrides a pass quorum, and pass/fail conflict is held rather than averaged away.

## Independence dimensions

Each packet separately declares and seals:

- independence from the candidate producer;
- independence from peer verifiers;
- independent prompt lineage;
- independent repair-memory lineage;
- independent test-generation lineage;
- a distinct verifier, organization, session, and verification-method digest.

Policy decides which dimensions are mandatory. The reference policy requires all five.

## Evidence packet

Every packet binds:

- repository, exact source commit, candidate digest, and context-pack digest;
- verifier, reviewer, runner, organization, session, and nonce identities;
- check family, method, environment, toolchain, and protocol digests;
- a sorted exact partition of passed, failed, and skipped check identifiers;
- findings, severity, falsification, acceptance criteria, and declared outcome;
- verification window and isolated-execution evidence;
- negative kernel-execution, mutation, selection, execution-authority, Git-authority, and correctness-proof fields;
- a canonical SHA-256 digest.

## Consensus order

After all schema, digest, binding, freshness, coverage, independence, and authority checks pass, outcome selection is deterministic:

1. any critical failed packet when critical override is enabled → `consensus_fail`;
2. simultaneous passed and failed packets when conflict hold is enabled → `disagreement_hold`;
3. fail quorum reached → `consensus_fail`;
4. pass quorum reached with no inconclusive packet → `consensus_pass`;
5. otherwise → `inconclusive_hold`.

A completed failed consensus is evidence, not candidate rejection authority. A passed consensus is bounded verification evidence, not correctness proof or merge authorization.

## Reference ensemble

The reference fixture uses four independent packets:

| Family | Verifier | Organization | Checks |
|---|---|---|---|
| type/formal | formal-verifier | org-formal | strict Lean, Python type check |
| behavioral/regression | behavior-verifier | org-behavior | unit and property regression |
| adversarial/falsification | adversarial-verifier | org-adversarial | boundary and tamper falsification |
| maintainability/static | static-verifier | org-static | complexity and dead-code checks |

Reference result:

- verifier count: 4;
- organization count: 4;
- method count: 4;
- family coverage: 4/4;
- pass count: 4;
- fail count: 0;
- inconclusive count: 0;
- critical failure count: 0;
- consensus: passed;
- open verification debt: false;
- reference ensemble digest: `6faaa86813a1d72f9f12301024999b7c254a723135e6eb0e70e60da4a45cb218`;
- reference receipt digest: `44e8047d20981d68f0b9061c557771f22cfbe6002979266338941e8b551598b4`.

## Fail-closed boundaries

The stage blocks without ensemble or receipt on:

- missing/extra fields or malformed values;
- any request, policy, or packet digest mismatch;
- repository, source commit, candidate, or context mismatch;
- stale/future requests or evidence;
- excessive verification duration or skipped checks;
- unapproved verifier, reviewer, or runner;
- duplicate verifier, organization, session, evidence ID, or insufficient method diversity;
- missing required family;
- producer, peer, prompt, memory, or test-generation dependence;
- inconsistent check partition or outcome;
- kernel execution, repository mutation, candidate selection, execution authority, Git authority, secret/network permission, or correctness-proof escalation.

## Formal surface

The generic Lean kernel defines verifier verdicts, family evidence, independence, family coverage, pass/fail quorum, critical override, conflict hold, and no-authority boundaries. The actual four-verifier specialization proves the reference ensemble satisfies the acceptance predicate and preserves every fixed boundary.

## Surfaces

| Surface | Path |
|---|---|
| Schema | `runtime/kuuos_codeai_independent_verifier_ensemble_schema_v0_2.py` |
| Checks | `runtime/kuuos_codeai_independent_verifier_ensemble_checks_v0_2.py` |
| Runtime | `runtime/kuuos_codeai_independent_verifier_ensemble_v0_2.py` |
| Fixture | `scripts/build_codeai_independent_verifier_ensemble_fixture_v0_2.py` |
| Projection | `scripts/project_codeai_independent_verifier_ensemble_fixture_v0_2.py` |
| Checker | `scripts/check_codeai_independent_verifier_ensemble_v0_2.py` |
| Tests | `tests/test_kuuos_codeai_independent_verifier_ensemble_v0_2.py` |
| Example | `examples/codeai_independent_verifier_ensemble_v0_2.json` |
| Manifest | `manifests/kuuos_codeai_independent_verifier_ensemble_v0_2.json` |
| Formal kernel | `formal/KUOS/CodeAI/IndependentVerifierEnsembleV0_2.lean` |
| Formal root | `formal/KuuOSCodeAIIndependentVerifierEnsembleV0_2.lean` |
| Workflow | `.github/workflows/codeai-independent-verifier-ensemble-v0-2.yml` |

## Validation

The dedicated workflow runs Python compilation, JSON validation, deterministic projection checking, 26 dedicated positive/tamper/independence/quorum tests, predecessor verification/context/holdout tests, canonical Lake validation, strict dedicated Lean compilation, and strict full `KuuOSFormal` compilation.
