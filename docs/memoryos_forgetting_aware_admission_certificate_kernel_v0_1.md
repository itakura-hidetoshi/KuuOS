# MemoryOS v0.67 — forgetting-aware contradiction-safe memory admission

## Purpose

MemoryOS v0.67 evolves the accepted v0.66 mathematical frontier into a bounded memory-management layer informed by current agent-memory research. The layer is append-only, provenance-bound, query-conditioned, contradiction-aware, forgetting-aware, and non-executing.

It does not treat semantic similarity as sufficient authority to inject a memory into downstream reasoning.

## Literature binding

The runtime certificate binds the following primary sources by stable arXiv identifier:

- `arXiv:2506.06326` — *Memory OS of AI Agent*: hierarchical storage and explicit storage/update/retrieval/generation operations.
- `arXiv:2505.00675` — *Rethinking Memory in AI*: consolidation, updating, indexing, forgetting, retrieval, and compression as atomic memory operations.
- `arXiv:2502.12110` — *A-MEM*: dynamic indexing, linking, and memory evolution.
- `arXiv:2504.19413` — *Mem0*: salient extraction, consolidation, scalable retrieval, and graph memory.
- `arXiv:2601.03543` — *EvolMem*: multi-dimensional, multi-session memory evaluation.
- `arXiv:2602.16313` — *MemoryArena*: coupled Memory–Agent–Environment evaluation rather than isolated recall.
- `arXiv:2604.20006` — *From Recall to Forgetting*: explicit penalty for reuse of obsolete or invalidated memory.
- `arXiv:2606.06054` — *Beyond Similarity*: memory search as a trust boundary and query-conditioned admission.

The literature records are provenance inputs, not imported theorem authority.

## Formal archive model

A memory record carries:

- key,
- value,
- scope,
- natural-number version,
- validity flag.

For records `older` and `newer`, `Supersedes older newer` means:

1. the keys agree,
2. the values differ,
3. the newer version is strictly greater,
4. the newer record is valid.

A record is `Effective` exactly when:

1. it is present in the finite append-only archive,
2. it is valid,
3. no archive record supersedes it.

A record is `QueryAdmissible` only when it is effective, its scope equals the query scope, and it satisfies the supplied query predicate.

## Actual Lean theorems

The formal package proves:

- every admitted record is present, valid, scope-exact, and query-matching;
- an admitted record has no superseder;
- a superseded record is not effective and cannot be admitted;
- append-only insertion retains every prior record;
- appending a non-superseding record preserves prior effectiveness;
- appending a superseding record invalidates the older record's effectiveness without deleting it;
- if a finite archive has any admissible record, a freshest admissible witness exists using `Finset.max'`;
- forgetting-aware loss is nonnegative when both components are nonnegative;
- zero obsolete-reuse penalty recovers ordinary recall loss;
- positive obsolete-reuse penalty strictly increases the loss.

## Runtime profile

The exact runtime contains:

- 8 literature provenance records;
- 10 append-only memory records;
- 3 supersession edges;
- 6 effective records;
- 6 query-conditioned admission cases;
- 6 freshest admissible witnesses;
- 4 exact-rational forgetting-aware loss cases;
- 8 full-rank transport commutation records;
- 4 singular atomic retention records;
- 3 rank-one source boundaries.

The canonical archive intentionally includes:

- three obsolete records retained in the archive but excluded from admission;
- one invalid record excluded from admission;
- six effective records admitted only under exact scope and query-key matches.

## Forgetting semantics

Forgetting is represented as loss of admissibility, not destructive erasure. The historical record remains append-only and provenance-addressable. This preserves auditability while preventing obsolete content from entering the active retrieval surface.

The exact-rational evaluation ledger uses

`forgettingAwareLoss = recallError + obsoleteReusePenalty`.

This is a bounded certificate inspired by forgetting-aware evaluation; it is not a claim that the repository implements the full Memora benchmark or its published FAMA metric.

## Trust boundary

The query-conditioned gate requires all of:

- record validity,
- absence of a valid newer contradiction,
- exact scope match,
- exact query-condition match.

Semantic similarity alone does not grant admission. Admission does not trigger planning, decision, activation, tool use, or execution.

## Source binding

The certificate verifies and binds the accepted MemoryOS v0.66 certificate, including:

- derivative and curvature profile digest;
- continuous stationarity input digest;
- finite-grid comparison and bounded-optimizer ledgers;
- Marton inputs;
- full-rank and singular transport records;
- DecisionOS candidate IDs;
- PlanOS history IDs;
- quotient-coordinate probe IDs;
- relational frontier, required-review, dissent, and minority-protection sets.

## Fail-closed behavior

The checker rejects:

- altered v0.66 source records or source digests;
- archive version tampering;
- obsolete-memory admission claims;
- cross-scope leakage claims;
- admission-triggered action claims;
- candidate-selection claims;
- unexpected claims;
- certificate digest substitution.

## Authority boundary

MemoryOS v0.67 remains future-only, read-only, and advisory. It does not:

- rank, prune, or select DecisionOS candidates;
- commit decisions or issue decision receipts;
- synthesize plans;
- activate or execute actions;
- mutate v0.66, DecisionOS, or persistent WORLD state;
- claim verification truth;
- grant truth authority.
