# KuuOS Adaptive Retrieval Policy v0.1

## 1. Purpose

KuuOS should not treat embeddings, vector databases, reranking, or GraphRAG as the default retrieval ontology. Retrieval machinery is a **context-dependent presentation choice** whose complexity must be justified by the evidence task.

This document introduces a bounded adaptive retrieval policy inspired by the engineering decision factors described in Rafael Pierre, **“RAG Is Simpler Than You Think: Six approaches to retrieval-based AI, from minimal to elaborate”** (Lighthouse, 2026-06-10): data freshness, corpus churn, query pattern, scale/performance, and team capability.

The KuuOS adaptation is deliberately stricter than a generic RAG recipe:

```text
retrieval mechanism != truth authority
retrieval score != entailment
embedding similarity != semantic proof
index freshness != source freshness
vector database != WORLD model
GraphRAG != global ontology
retrieved evidence != verified evidence
```

The source article's numerical examples are treated as engineering heuristics, not mathematical constants or theorem assumptions.

## 2. Least-sufficient-retrieval principle

KuuOS adopts the principle:

> **Use the least complex retrieval presentation that is adequate for the current query context, and escalate only when observed evidence shows that the simpler presentation is insufficient.**

Let a retrieval context be represented schematically by

```text
C_retrieval =
  freshness requirement
  × corpus churn
  × query pattern
  × corpus/access distribution
  × request scale
  × latency/cost budget
  × available operational capability
  × provenance requirement.
```

For a set of candidate retrieval modes `M`, define schematically

```text
Adequate : C_retrieval × M -> Prop
Complexity : M -> OrderedCost
```

and choose

```text
m* = minimal-complexity m such that Adequate(context, m).
```

If no admissible mode is adequate, the correct route is not uncontrolled expansion but

```text
HOLD / OBSERVE / NO_DATA
```

with an explicit next-observation target.

This is currently an architectural specification, not yet a Lean theorem package.

## 3. KuuOS retrieval ladder

The following six levels are a KuuOS synthesis. They are not asserted to reproduce the hidden ordering or full contents of the source article.

### R0 — lexical / full-text retrieval

Examples:

```text
BM25
PostgreSQL full-text search
Elasticsearch/OpenSearch lexical search
exact identifier lookup
```

Prefer this level when:

- exact terms, identifiers, codes, names, or proprietary terminology matter;
- queries are keyword-heavy;
- corpus size and request volume do not justify additional infrastructure;
- auditability and debuggability are primary;
- semantic expansion has not demonstrated measurable benefit.

KuuOS interpretation:

```text
lexical match = candidate evidence transport
lexical match != verified relevance
```

### R1 — lexical retrieval with bounded query rewriting

Use when users ask conversational questions but the corpus is still best addressed by exact or domain-specific terminology.

The rewriting layer may generate lexical variants, but must preserve:

- the original query;
- the rewritten query or queries;
- provenance of the rewrite;
- a bounded fan-out;
- the distinction between user intent and generated search terms.

```text
rewrite != user statement
rewrite != evidence
rewrite success != answer correctness
```

### R2 — semantic retrieval on demand

Use transient or on-the-fly embeddings when semantic matching is useful but full-corpus pre-embedding is poorly justified, especially when:

- the corpus changes rapidly;
- much of the corpus is rarely queried;
- a query-specific candidate set can first be narrowed lexically or structurally;
- embedding cost and staleness should remain bounded.

KuuOS should prefer **query-scoped semantic state** over turning the entire corpus into a permanent latent ontology.

### R3 — hybrid lexical + semantic retrieval

Use when both exact terminology and semantic similarity are materially important.

A hybrid result must retain its component evidence:

```text
lexical score
semantic score
fusion rule
source identifier
source version / timestamp where available
```

The fused ranking is a presentation-level convenience, not a truth scalar.

### R4 — stable-corpus pre-embedded retrieval

Pre-embedding is justified only when the corpus is sufficiently stable and the measured workload benefits from amortized indexing.

The policy should record:

- embedding model and version;
- chunking/segmentation policy if used;
- index build time;
- source snapshot or source-version boundary;
- stale-index detection;
- re-index trigger.

A model or chunking change is a **change of presentation** and must not silently inherit equivalence with the previous index.

### R5 — reranked relational / GraphRAG retrieval

Use the most elaborate layer only when the task actually depends on richer structure such as:

- multi-hop relations;
- declared paths or cycles;
- query-specific contextual transport;
- history-conditioned evidence;
- cross-source consistency/holonomy diagnostics;
- reranking that has demonstrated measurable value over simpler candidates.

This level connects to `KUUOS_GAUGE_QI_PROCESS_GRAPHRAG_v0_2.md`.

KuuOS keeps the existing boundary:

```text
query-specific graph != persistent global context graph
GraphRAG CANDIDATE != committed belief
persistent evidence != truth authority
```

## 4. Decision factors

### 4.1 Freshness

Freshness is evaluated at the source and retrieval-presentation levels separately.

```text
source freshness
index freshness
cache freshness
retrieval timestamp
```

must not be collapsed into one flag.

Fast-changing corpora favor cheap re-indexing, direct source retrieval, lexical search, or on-demand semantic processing. Stable corpora are better candidates for precomputed embeddings.

### 4.2 Corpus churn

The source article gives `>10%` daily change as an example of high churn. KuuOS records such a threshold only as a **calibration candidate**, never as a universal boundary.

A deployment should measure its own:

```text
changed documents / active corpus / time window
```

and use this to determine whether a full pre-embedding strategy creates unacceptable staleness or re-index cost.

### 4.3 Query pattern

Classify the query before choosing the retrieval presentation:

```text
EXACT
LEXICAL
CONVERSATIONAL
SEMANTIC
RELATIONAL
MIXED
UNKNOWN
```

Examples:

```text
"invoice #12345"        -> EXACT / LEXICAL
"reset password"        -> LEXICAL
"how do I regain access"-> CONVERSATIONAL / SEMANTIC
multi-hop relation query -> RELATIONAL
```

`UNKNOWN` should not automatically select the most complex path. It should prefer a conservative candidate and collect evaluation evidence.

### 4.4 Scale and performance

The source article offers rough bands of `<1K`, `1K–10K`, and `>10K` queries/day as examples for deciding when optimization may become worthwhile.

KuuOS treats these only as provisional engineering priors. The actual decision should depend on measured:

```text
p50 / p95 latency
throughput
index build time
cache hit rate
embedding cost
rerank cost
retrieval failure rate
operator burden
```

### 4.5 Operational capability

A retrieval architecture that cannot be inspected, reproduced, repaired, or safely operated is not superior merely because it is more sophisticated.

Capability includes:

```text
ability to inspect why a result matched
ability to reproduce an index
ability to detect stale embeddings
ability to version models
ability to evaluate retrieval quality
ability to repair a corrupted index
ability to preserve provenance
```

## 5. Mission Cycle integration

Adaptive retrieval belongs inside the existing KuuOS mission cycle rather than outside it.

```text
Plan
  classify query context
  choose least-sufficient candidate retrieval mode
  declare budgets and escalation conditions

Act
  execute only the licensed retrieval operation

Observe
  capture result set, provenance, scores, timestamps, and failures

Verify
  evaluate adequacy, freshness, lineage, contradictions, and source authority

Learn
  record future-only evidence about which retrieval presentation was adequate

Replan
  retain, simplify, or escalate the retrieval mode
```

No retrieval mode directly grants:

```text
WORLD commit authority
belief authority
decision authority
execution authority
clinical authority
theorem authority
```

## 6. NO_DATA and fail-closed behavior

Retrieval failure must be represented explicitly.

Examples:

```text
no matching source
index stale beyond declared tolerance
source version unavailable
rewrite fan-out exhausted
semantic model unavailable
provenance incomplete
hybrid components disagree materially
GraphRAG path/cycle evidence incomplete
```

These should route to a bounded state such as:

```text
NO_DATA
HOLD
OBSERVE
REPAIR
QUARANTINE
```

rather than silently broadening the search, hallucinating a bridge, or promoting similarity to truth.

## 7. Evaluation before escalation

A mode escalation must be evidence-based. Candidate metrics include:

```text
exact-match success
known-answer retrieval recall
source-level precision
semantic-query success
identifier preservation
latency
cost
index staleness
provenance completeness
contradiction rate
operator-debuggability
```

The preferred comparison is paired and query-specific:

```text
Does R(n+1) materially improve adequacy over R(n)
under the same query set and authority boundary?
```

If not, retain the simpler mode.

## 8. Dependent-origination interpretation

Adaptive retrieval fits the KuuOS dependent-origination program naturally.

A retrieval representation is not the intrinsic meaning of the corpus. It is one contextual presentation through which evidence is transported.

```text
source corpus
   ↓ presentation
lexical index / embedding index / hybrid index / query graph
   ↓ retrieval transport
candidate evidence
   ↓ verification / descent
contextual semantic use
```

This yields several research directions:

### Presentation invariance

When two retrieval presentations are justified equivalents, which query-level semantic invariants are preserved?

### Descent

When overlapping retrieval modes return compatible local evidence, when does a coherent global evidence state exist?

### Obstruction

Contradictory lexical, semantic, or relational retrieval results should be representable as an explicit obstruction rather than erased by ranking.

### Non-reification

An embedding coordinate, vector index, BM25 score, graph path, or reranker score must not be promoted to intrinsic semantic substance merely because it is computationally convenient.

This is a direct operational instance of the KuuOS `DO7 Non-reification` direction.

## 9. Integration with Gauge–Qi Process GraphRAG

`Gauge–Qi Process GraphRAG v0.2` remains a downstream, bounded evidence-transport mechanism.

The new policy inserts a precondition:

```text
query context
  -> adaptive retrieval policy
  -> lexical / rewritten / semantic / hybrid / pre-embedded candidate set
  -> only when relational evidence is justified:
       Gauge–Qi Process GraphRAG
  -> BeliefOS evidence packet
  -> Replan-only adoption
```

This prevents GraphRAG from becoming the universal first retrieval step and preserves its intended query-specific role.

## 10. Source-specific heuristics retained as non-authoritative calibration notes

The attached source motivates the following initial calibration hypotheses:

```text
high corpus churn example       >10% changes/day
simple workload example         <1,000 queries/day
selective optimization example  1,000–10,000 queries/day
full optimization candidate     >10,000 queries/day
```

KuuOS does **not** hard-code these values as universal constants. Each deployment must establish empirical thresholds from its own latency, cost, freshness, and quality measurements.

## 11. Public boundary

Adaptive Retrieval Policy v0.1 is an architectural and governance layer. It does not claim that one retrieval technique is universally optimal, that embeddings encode intrinsic meaning, that BM25 is always sufficient, that GraphRAG is always superior for relational questions, or that a retrieval benchmark establishes truth.

Its central invariant is:

```text
simplest adequate presentation first
+ explicit escalation evidence
+ provenance-preserving transport
+ fail-closed NO_DATA
+ no retrieval mechanism receives truth authority.
```
