# CodeAI Intent-Aligned Dataflow Context Pack v0.2

## Purpose

This stage evolves `CodeAI Selective Repository Semantic Context Pack v0.1` from bounded lexical and symbol-aware repository selection into an explicitly traceable retrieval process:

```text
intent
  -> candidate hypotheses
  -> target symbols
  -> imports / calls / type references
  -> dataflow edges
  -> bounded context pack
```

The output is a read-only, content-addressed evidence object. It does not select a patch, execute a candidate, mutate a repository, or grant any later-stage authority.

## Why this follows the temporal holdout corpus

PR #1328 fixed a temporal development/holdout boundary before later retrieval, verification, memory, or routing improvements are evaluated. This PR changes the retrieval evidence surface, not the holdout corpus. Later comparative evaluation can therefore bind this v0.2 context pack to the frozen corpus rather than silently adapting against holdout cases.

The design follows the repository-level retrieval findings used in the preceding paper-grounded plan:

- repository context should be retrieved iteratively rather than as one static in-file window;
- dependency and dataflow structure provide stronger cross-file evidence than lexical proximity alone;
- intent and candidate hypotheses should remain visible in the retrieval trace;
- every expansion step should remain bounded and reproducible.

This implementation does not claim that the reference fixture is representative or that dataflow retrieval alone improves patch correctness. It creates the measurable artifact required to test those claims later.

## Inputs

### Source observation receipt

The stage consumes the existing read-only intent repository observation receipt. It must bind the repository full name, exact source commit SHA, repository tree digest, read-only observation mode, and absence of repository mutation.

### Request

The request binds:

- natural-language intent and initial query terms;
- candidate hypotheses;
- hypothesis-local query terms and expected symbols;
- target path prefixes and target symbols;
- required context roles;
- exact repository snapshot digest;
- expected source receipt digest;
- request creation epoch.

Every candidate hypothesis has its own digest. Re-sealing only the outer request cannot hide a modified hypothesis.

### Policy

The policy binds:

- exact repository and commit;
- allowed and forbidden path prefixes;
- supported suffixes;
- snapshot, file, excerpt, query, hypothesis, dependency-depth, selection, and total-context budgets;
- minimum intent evidence score and request freshness;
- required dependency-path and symbol-digest evidence;
- explicit denial of mutation, network, secret, selection, and execution authority.

## Semantic extraction

### Python

The Python extractor uses the standard-library AST to collect function/class symbols, imports, call targets, annotation type references, and assignment/return dataflow edges.

For example:

```python
subtotal = compute_subtotal(items)
taxed_total = apply_tax(subtotal, tax_rate)
return taxed_total
```

produces evidence including:

```text
compute_subtotal -> subtotal
items -> subtotal
apply_tax -> taxed_total
subtotal -> taxed_total
tax_rate -> taxed_total
taxed_total -> return
```

### Lean

The Lean extractor collects imports, declarations, identifiers appearing in declaration types and bodies, and declaration-local dependency/dataflow evidence. It is a bounded static evidence extractor, not a Lean elaborator. Strict Lean compilation remains an independent CI surface.

### Text fallback

Documentation and bounded text files may contribute lexical/type-reference terms when the policy allows text fallback. Text fallback does not invent executable symbols or dataflow.

## Query lineage

The reference pack contains six sealed query nodes:

1. one `intent` node;
2. two `hypothesis` nodes;
3. one `symbol` expansion node;
4. one `dependency` expansion node;
5. one `dataflow` expansion node.

Every non-intent node names its parent node IDs. Every node seals its stage, parent IDs, normalized terms, source references, and node digest. The lineage therefore records why a term entered retrieval instead of exposing only the final selected files.

## Candidate scoring and dependency expansion

A candidate file receives bounded evidence weight from initial intent-term matches, hypothesis matches, target-symbol matches, requested path/role matches, and observed dataflow edges. Structural path/role bonuses cannot create a seed by themselves; at least one intent term, hypothesis, or target symbol must match.

After seed selection, the stage resolves bounded dependency paths through module imports, imported symbols, call targets, type references, and declarations defined in other candidate files.

Each selected file contains:

- its shortest path from an intent-aligned seed;
- additional resolved dependency paths starting at that file;
- content, symbol, excerpt, and selected-evidence digests;
- symbols, imports, calls, type references, and dataflow edges;
- matched terms, hypotheses, and target symbols;
- evidence score and bounded excerpt.

## Reference fixture

The deterministic fixture models one order-total tax dataflow across Python runtime orchestration, Python pricing implementation, a Python test, Lean pricing and order-pipeline references, documentation, and one unrelated configuration file.

The context pack selects six relevant files and excludes the unrelated config. Its compact projection records:

```text
query lineage nodes:       6
selected files:            6
symbol digests:            6
resolved dependency paths: 7
dataflow edges:            26
snapshot bytes:            1578
context bytes:             1539
```

These counts describe only the committed reference fixture.

## Fail-closed conditions

The stage blocks without context pack or receipt on malformed shape, digest mismatch, repository/commit mismatch, snapshot/tree mismatch, stale or future request, budget overflow, forbidden or out-of-scope path, unsupported suffix, semantic parse failure, absence of an intent-aligned seed, missing required role, or forbidden mutation/network/secret/selection/execution authority.

## Fixed boundary

```text
context retrieval != patch selection
context retrieval != candidate execution
context retrieval != correctness proof
context retrieval != complete repository understanding
context retrieval != representative evaluation
context receipt != Git authority
context receipt != successor-stage authority
```

The output explicitly records read-only observation, no mutation, no network access, no secret read, no selection or execution authority, and no correctness, completeness, or representativeness claim.

## Formal surface

The generic Lean kernel defines query stages and parent-grounded query nodes, evidence items with score/byte/symbol/dependency provenance, bounded-pack predicates, evidence-grounding predicates, and a no-effect/no-overclaim boundary.

The actual specialization proves by computation that the reference query lineage is grounded, the six evidence items satisfy selected-file and byte budgets, every evidence item is grounded, and the boundary is preserved.

## Surfaces

| Surface | Path |
|---|---|
| Runtime schema | `runtime/kuuos_codeai_intent_aligned_dataflow_context_pack_schema_v0_2.py` |
| Runtime checks | `runtime/kuuos_codeai_intent_aligned_dataflow_context_pack_checks_v0_2.py` |
| Runtime kernel | `runtime/kuuos_codeai_intent_aligned_dataflow_context_pack_v0_2.py` |
| Fixture builder | `scripts/build_codeai_intent_aligned_dataflow_context_pack_fixture_v0_2.py` |
| Fixture projection | `scripts/project_codeai_intent_aligned_dataflow_context_pack_fixture_v0_2.py` |
| Checker | `scripts/check_codeai_intent_aligned_dataflow_context_pack_v0_2.py` |
| Tests | `tests/test_kuuos_codeai_intent_aligned_dataflow_context_pack_v0_2.py` |
| Example | `examples/codeai_intent_aligned_dataflow_context_pack_v0_2.json` |
| Manifest | `manifests/kuuos_codeai_intent_aligned_dataflow_context_pack_v0_2.json` |
| Formal kernel | `formal/KUOS/CodeAI/IntentAlignedDataflowContextPackV0_2.lean` |
| Formal root | `formal/KuuOSCodeAIIntentAlignedDataflowContextPackV0_2.lean` |
| Workflow | `.github/workflows/codeai-intent-aligned-dataflow-context-pack-v0-2.yml` |

## Validation

The dedicated workflow validates Python compilation, JSON syntax, deterministic compact reconstruction, 26 dedicated tests, predecessor v0.1 context-pack tests, temporal holdout corpus tests, canonical Lake manifest, the strict dedicated Lean root, and strict full `KuuOSFormal`.

Failure artifacts are uploaded only after a completed failing job.
