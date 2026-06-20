# KuuOS Qi–WORLD Indra Transport Receipt Intake v1.7

## Purpose

v1.6 emitted a protected request for seven classes of external analytic transport evidence. v1.7 adds the corresponding receipt intake.

The intake validates receipt structure and binding. It does not decide whether the external analytic claims are mathematically or physically true.

```text
v1.6 protected transport request
→ seven external analytic receipts
→ hash / dependency / lineage validation
→ schema-complete receipt set
→ external semantic review still required
```

## Required receipt classes

The intake requires exactly one receipt of each kind, in this order:

1. `NORMAL_STAR_ISOMORPHISM`
2. `PSEUDOFUNCTOR_REALIZATION`
3. `STACK_DESCENT`
4. `BRANCH_TRANSPORT`
5. `COHERENCE_TWO_CELL`
6. `HISTORY_DEPENDENT_PHASE`
7. `CONTINUUM_NONMARKOV_CONNECTION`

Each receipt carries an external proof-object digest and an external verifier-receipt digest.

The test suite uses clearly marked synthetic fixtures to exercise the schema. Those fixtures are not analytic proofs.

## Common binding

Every receipt must bind to the same canonical v1.6 fields:

- v1.6 request-receipt digest;
- transport-request digest;
- WORLD v0.42 bridge-state digest;
- source and target WORLD-projection digests;
- source and target patch IDs;
- exact two-patch path;
- overlap-evidence request digest;
- branch ID;
- cross-cycle process-lineage digest;
- complete Qi history digest.

A receipt from another request, patch pair, branch, lineage, or history is rejected even when its own digest is recomputed.

## Dependency chain

The intake validates the receipt dependencies:

```text
normal star-isomorphism
→ pseudofunctor realization
→ stack descent
→ branch transport
→ coherence two-cell
→ history-dependent phase
→ continuum non-Markov connection
```

Branch transport also binds the normal, pseudofunctor, and stack receipts. Coherence binds pseudofunctor and branch transport. The history phase binds branch transport and coherence.

Receipt timestamps must be strictly increasing in the required order.

## Disposition

A complete intake has the disposition:

```text
EXTERNAL_ANALYTIC_RECEIPTS_HASH_BOUND_SEMANTIC_REVIEW_REQUIRED
```

This means:

- all seven receipt classes are present;
- their own hashes are valid;
- their request and transport bindings are consistent;
- their dependency chain is valid;
- branch and history preservation are declared;
- semantic review remains external.

It does **not** mean that the runtime verified a normal star-isomorphism, pseudofunctor, stack descent, continuum connection, or physical transport.

## Runtime rejection cases

The validator rejects:

- a missing receipt class;
- duplicate or reordered receipt classes;
- a receipt bound to another v1.6 request;
- patch, branch, lineage, or history substitution;
- a malformed dependency chain;
- a missing proof-object or verifier-receipt digest;
- a runtime claim of semantic validity;
- a runtime claim that transport was realized;
- a claim that a gauge connection or physical holonomy was computed;
- exact-WORLD identity, WORLD mutation, branch collapse, or history overwrite.

## Non-authority boundary

For every external receipt:

```text
receipt_grants_execution = false
receipt_grants_truth = false
receipt_issues_authority = false
receipt_constructs_runtime_gauge_connection = false
receipt_computes_physical_holonomy = false
receipt_identifies_exact_world = false
receipt_updates_world = false
receipt_collapses_world_branches = false
receipt_overwrites_history = false
runtime_asserts_semantic_validity = false
```

For the intake itself:

```text
intake_grants_execution = false
intake_grants_truth = false
intake_issues_authority = false
intake_realizes_transport = false
intake_constructs_gauge_connection = false
intake_computes_physical_holonomy = false
intake_identifies_exact_world = false
intake_updates_world = false
intake_collapses_world_branches = false
intake_overwrites_history = false
intake_performs_semantic_review = false
```

## Interpretation

v1.7 completes the request/receipt protocol at the evidence-transport layer:

```text
request issued
→ external receipts supplied
→ receipt set hash-bound and dependency-checked
→ semantic validity remains an external responsibility
```

The bridge improves traceability without converting documentary evidence into truth, authority, physical transport, or exact-WORLD identity.
