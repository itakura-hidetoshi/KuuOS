# CodeAI Independent Test Strengthening v0.1

## Purpose

CodeAI Independent Test Strengthening v0.1 is roadmap step 6.

It receives the exact sealed output of Typed Error Classification and converts the observed error families, novelty states, and descriptive repair routes into a deterministic set of independent test obligations.

The surface strengthens the verification plan. It does not generate test code, invoke a test runner, pass or fail a candidate, repair code, rank candidates, select a candidate, or mutate Git state.

## Authoritative roadmap

```text
1. Baseline and Replay Evaluation
2. Selective Repository Semantic Context Pack
3. Typed Structured Edit IR
4. Candidate Static Admissibility Preflight
5. Typed Error Classification
6. Independent Test Strengthening
7. Evidence-Weighted Selection and Abstention
8. Version-Bound Repair Memory
9. Maintainability Trajectory Gate
```

## Pipeline position

```text
Typed Structured Edit IR
→ Candidate Static Admissibility Preflight
→ Typed Error Classification
→ Independent Test Strengthening
→ externally executed independent verification evidence
→ Evidence-Weighted Selection and Abstention
```

The pre-existing Independent Verification Envelope remains the evidence-recording boundary. This surface supplies the strengthened obligations that an independent verifier must satisfy; it does not replace or execute that envelope.

## Inputs

The kernel consumes five sealed inputs:

1. the exact Typed Error Classification;
2. its exact route receipt;
3. an independent test capability catalog;
4. a strengthening request;
5. a deny-by-default strengthening policy.

The request and policy bind the repository, source commit, classification digest, classification-receipt digest, and capability-catalog digest.

## Capability catalog

The capability catalog describes available independent verification capabilities without invoking them.

Every capability binds:

- check kind;
- runner profile;
- evidence format;
- independent-runner availability;
- isolated-execution availability;
- mutation capability;
- falsification capability.

A catalog is rejected when it claims test generation, test execution, verification authority, repository mutation, or Git effects.

## Baseline obligations

Every candidate receives three obligations, including candidates with no static findings:

- `source_lineage_replay`;
- `deterministic_reconstruction`;
- `changed_path_coverage`.

This prevents a candidate from bypassing independent test planning merely because static preflight found no error.

## Typed-family obligations

Each observed typed family adds a corresponding independent obligation.

| Typed family | Strengthened obligation |
|---|---|
| `operation_conflict` | `operation_collision_replay` |
| `materialization` | `materialization_replay` |
| `syntax` | `parse_negative_control` |
| `dependency` | `dependency_closure` |
| `testing` | `test_plan_completeness` |
| `policy_marker` | `policy_marker_scan` |
| `semantic_noop` | `material_effect_assertion` |

Multiple errors of the same family within one candidate are consolidated into one obligation with all linked fingerprints preserved.

## Novel-error falsification

Every error marked `novel_to_replay_baseline` requires `novelty_falsification`.

The catalog must report a falsification-capable independent isolated runner for this obligation.

Novelty is not a probability, quality score, ranking weight, or selection preference. It only expands the required independent challenge set.

## Error-free mutation probe

A candidate with no static error receives `error_free_mutation_probe`.

The probe requires a mutation-capable independent isolated runner. Its purpose is to demonstrate that the proposed verification harness can detect an intentionally seeded fault rather than merely report a vacuous pass.

`no_static_error_observed` remains distinct from correctness.

## Route-specific obligations

The three descriptive repair routes remain distinct:

| Typed repair route | Strengthened obligation |
|---|---|
| `local_candidate_repair` | `local_repair_regression` |
| `external_evidence_required` | `external_evidence_binding` |
| `current_ir_unmaterializable` | `unmaterializability_reproduction` |

A route-specific obligation is not permission to repair, obtain external authority, reject a candidate, or modify the current IR.

## Candidate preservation

Every source candidate remains present and in the original sequence.

Each candidate plan records:

- exact source candidate digest;
- source classification;
- source typed-error count;
- source error fingerprints;
- ordered obligations;
- exact obligation count;
- whether an error-free mutation probe is required;
- whether a novel-error falsification challenge is required;
- explicit negative test-generation, test-execution, selection, and verifier-invocation flags.

## Obligation records

Each obligation contains:

- candidate identity and sequence;
- obligation identity and sequence;
- category and check kind;
- linked source fingerprints;
- required evidence labels;
- runner profile and evidence format;
- independence and isolation requirements;
- mutation or falsification requirements;
- an independently sealed obligation digest.

Obligations do not contain a pass result and do not claim that a test has been generated or executed.

## Deterministic categories

The aggregate plan counts obligations in five categories:

- `baseline`;
- `error_specific`;
- `novelty`;
- `route`;
- `error_free`.

Counts are accounting information only. More obligations do not make a candidate better or worse.

## Fail-closed conditions

The kernel blocks on, among other conditions:

- malformed inputs;
- any digest mismatch;
- repository or source-commit mismatch;
- classification-receipt mismatch;
- stale or future requests;
- unresolved questions;
- authority claims;
- enabled test-generation, test-execution, ranking, selection, verification, repair, repository, execution, or Git authority;
- disabled exact-lineage or mandatory-strengthening requirements;
- missing baseline obligations;
- candidate or obligation budget overflow;
- missing required check capability;
- non-independent or non-isolated required runner;
- absent mutation capability for the error-free probe;
- absent falsification capability for novel errors;
- duplicate obligation identities;
- candidate sequence loss;
- source classification containing downstream effects or authority.

## Fixed boundaries

```text
strengthened test plan != generated test code
test obligation != test execution
test execution != test success
test success != correctness proof
obligation count != candidate quality
novelty challenge != ranking weight
route-specific obligation != repair authority
strengthening != ranking
strengthening != candidate selection
strengthening receipt != verification authority
strengthening receipt != execution authority
strengthening receipt != Git authority
```

## Effect boundary

This surface performs no:

- provider or LLM invocation;
- test-code generation;
- test execution;
- candidate application;
- ranking or selection;
- verification runner invocation;
- repair execution;
- repository mutation;
- network or secret access;
- execution lease issuance;
- Git operation;
- merge or deployment authorization.

## Formal surface

- `formal/KUOS/CodeAI/IndependentTestStrengtheningV0_1.lean`
- `formal/KuuOSCodeAIIndependentTestStrengtheningV0_1.lean`

The generic Lean layer proves:

- typed-family obligations are injective;
- route obligations are injective;
- the baseline obligation set has exactly three members;
- a well-formed receipt has at least three obligations per candidate;
- strengthened planning does not generate or execute tests;
- planning does not rank or select;
- planning grants no verification, repair, execution, or Git authority;
- novelty challenges do not become candidate quality scores;
- test coverage is not treated as correctness proof.

## Surfaces

| Surface | Path |
|---|---|
| Schema | `runtime/kuuos_codeai_independent_test_strengthening_schema_v0_1.py` |
| Checks | `runtime/kuuos_codeai_independent_test_strengthening_checks_v0_1.py` |
| Runtime | `runtime/kuuos_codeai_independent_test_strengthening_v0_1.py` |
| Fixture builder | `scripts/build_codeai_independent_test_strengthening_fixture_v0_1.py` |
| Deterministic checker | `scripts/check_codeai_independent_test_strengthening_v0_1.py` |
| Tests | `tests/test_kuuos_codeai_independent_test_strengthening_v0_1.py` |
| Example | `examples/codeai_independent_test_strengthening_v0_1.json` |
| Manifest | `manifests/kuuos_codeai_independent_test_strengthening_v0_1.json` |
| Formal kernel | `formal/KUOS/CodeAI/IndependentTestStrengtheningV0_1.lean` |
| Formal root | `formal/KuuOSCodeAIIndependentTestStrengtheningV0_1.lean` |
| Workflow | `.github/workflows/codeai-independent-test-strengthening-v0-1.yml` |

## Validation

The dedicated workflow validates:

- Python syntax;
- example and manifest JSON;
- deterministic reconstruction;
- dedicated fail-closed tests;
- Typed Error Classification and predecessor regressions;
- canonical Lake manifest;
- strict dedicated Lean root;
- strict full `KuuOSFormal`.

Failure diagnostics are uploaded only after a completed failing job.
