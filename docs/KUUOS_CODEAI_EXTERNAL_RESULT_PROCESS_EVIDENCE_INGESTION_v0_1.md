# CodeAI External Result and Process-Evidence Ingestion v0.1

## Purpose

This stage follows **Bounded Official Harness Execution v0.1**. It consumes the completed workflow and content-addressed evidence artifact without re-running the harness. It ingests one aggregate result and one process-evidence record into a read-only receipt.

The disposition is either:

- `external_result_process_evidence_ingestion_admitted`;
- `external_result_process_evidence_ingestion_held`.

Admission means the exact completed external run has been bound, verified, reduced to aggregate evidence, and ingested without exposing gold material, test names, or raw logs to candidate generation or repair memory. Admission does not mean the issue was solved.

## Exact predecessor evidence

```text
controller main = 30d6d57fe8b6681aa8e11404a774d0500076d497
predecessor workflow run = 29894633457
predecessor workflow head = 13ac5c618d934e3812ca70cd3791a374a2058f6f
predecessor artifact id = 8520539325
predecessor artifact digest = sha256:27f69ffd9a982956d2bbc2aaeecc9e45ed527ea522afda324e0e3665b634c5a2
instance = sympy__sympy-20590
prediction digest = 9a2aeff25ca565214ecbae781f20df4c23eea20db72b135702aa56d5de238050
external observation digest = 689b63a246192b45af75f512aba7478ad87db7aba90689d96fc0aa91bc28cbca
```

This historical predecessor artifact was originally uploaded to GitHub Actions, but its short-lived retention has expired; see the explicit reobservation section below. No raw report, test output or instance log is committed.

## Measured result

The completed official harness run observed:

```text
patch exists = true
patch applied = true
evaluation completed = true
resolved = false
FAIL_TO_PASS success = 0
FAIL_TO_PASS failure = 1
PASS_TO_PASS success = 21
PASS_TO_PASS failure = 0
execution errors = 0
```

The admitted outcome disposition is `measured_unresolved`. This is an evidence-bearing result, not a protocol failure and not a correctness claim.

## Process evidence

The ingestion binds the completed workflow, unexpired artifact metadata, Docker use, image and container availability, clean patch application, completed evaluation, stable before/after diff, container and image cleanup, report observation, log observation, and external network use.

The runtime kernel does not execute Docker or the harness. It only consumes completed evidence.

## Aggregate-only boundary

The committed result contains counts and digests only. It excludes:

- gold patch contents;
- test patch contents;
- raw test names;
- raw report body;
- raw test output;
- raw instance log;
- candidate-generation feedback;
- repair-memory feedback;
- model-selection or threshold-tuning authority.

The next comparison stage must be separately governed. This receipt grants no baseline-comparison or ablation authority by itself.

## BLOCK versus HOLD

Structural BLOCK includes malformed or extra fields, invalid seals, exact-binding mismatch, predecessor-manifest digest mismatch, stale evidence, invalid SHA values, and workflow/artifact identity mismatch.

Valid HOLD includes an unadmitted predecessor, missing patch or evaluation evidence, execution errors, expired artifacts, missing report or logs, raw test-name or gold inclusion, raw-log commitment, kernel-side harness execution, candidate or memory feedback, repository mutation, Git authority, and correctness overclaim.

## Reference result

- decision: `external_result_process_evidence_ingestion_admitted`;
- outcome: `measured_unresolved`;
- execution valid: `true`;
- ingestion pack: `f1c2a5d24c4d1a54e2e539ca7fef7c409c10aae83b4f5815174674b7df8db9e6`;
- receipt: `3e1711fa4aa26feb8a19feb8829f44ceb06a0e7a23f1bbf32c8db67615f3191f`.

## Formal kernel

The Lean surface defines `Binding`, `IngestionPlan`, `ResultEvidence`, `ProcessEvidence`, `IngestionEvidence`, `ExactBinding`, `PlanAggregateOnly`, `ResultComplete`, `ProcessComplete`, `IsolationPreserved`, `BoundaryPreserved`, and `IngestionAdmitted`.

It proves that missing patches, incomplete evaluation, raw test-name inclusion, gold-material inclusion, repair-memory feedback, kernel-side harness execution, repository mutation, and correctness claims forbid admission. The actual unresolved specialization is admitted.

## Fixed boundaries

```text
measured unresolved != protocol failure
execution valid != issue solved
aggregate counts != raw test labels
process evidence != repair memory
artifact download for validation != repository commitment
external harness evidence != kernel execution authority
ingestion receipt != comparison authority
ingestion receipt != repository mutation or Git authority
```

## Next stage

The next separately governed stage is **Baseline-versus-CodeAI and Ablation Comparison v0.1**. It must consume admitted aggregate result receipts, preregister comparison cohorts and metrics, and preserve holdout and authority boundaries.

## Historical artifact expiration and explicit reobservation (2026-10-16 JST)

The original evidence identifiers above describe a **historical, immutable
reference case**. Workflow run `29894633457` uploaded artifact `8520539325`
on 2026-07-22 with a 14-day retention period; that artifact is not currently
available from GitHub Actions. The earlier statement that the artifact "remains"
in Actions storage does **not** apply to the current date. Its original content
must never be inferred from a hash or silently replaced.

A distinct, genuine bounded official harness run completed successfully on
2026-10-16, with a preserved artifact that was independently downloaded and
verified before creating the new binding. The new evidence is **not** the July
artifact, and is never presented as a restoration of it:

| Provenance | Fresh independent observation |
|---|---|
| Workflow run / attempt | `38878097337` / `1` |
| Source HEAD | `613060a35533b380850850eb021409864edd5f18` |
| Artifact ID | `12039184115` |
| Artifact name | `codeai-bounded-official-external-v0-1-38878097337-1` |
| Artifact ZIP SHA256 | `edf52f8719af6e810944a52e57868e00cdbefa1613da520da23cb9cf362639d0` |
| Sealed observation digest | `7d802950cb7ffa266ac19ed043d1b7b77a8057873a3a52061bbee745e51fdb17` |
| Report SHA256 | `35493c1b427e375b3352d51e19a007d3602f23d6a45563ed14857dffb4f5c52f` |

The immutable reobservation binding lives in
`ci/codeai_external_evidence_reobserved_20261016.json`, **separate from** the
historical reference constants, manifests and examples. The workflow downloads
this exact new artifact and its GitHub metadata, checks the exact successful
run, SHA and attempt, the unexpired artifact ID/name/digest, all three evidence
file SHA256 digests, the sealed observation, the pinned non-gold prediction,
and the aggregate test outcome. It reconstructs a new request revision and
separately sealed ingestion receipt under the original restrictive v0.1 policy.

The committed files contain binding metadata and aggregate-only observations.
Raw test output, report, and process logs are downloaded only into the
transient CI workspace and are never committed. The result is still
**measured unresolved**, not a successful repair or an authorization for
comparison, training, mutation or Git effects.

The renewed GitHub Actions artifact itself is time-limited (as currently
recorded, to 2026-10-30 UTC). Any future expiration remains a **real failed
precondition**, not a reason to bypass the check. Renewal requires another
independent, successful run and a newly reviewed exact provenance binding;
previous receipts remain separate historical records.
