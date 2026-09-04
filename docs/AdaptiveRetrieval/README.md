# KuuOS Adaptive Retrieval

Adaptive Retrieval is the bounded retrieval-selection subsystem for KuuOS. It turns the design in `docs/KUUOS_ADAPTIVE_RETRIEVAL_POLICY_v0_1.md` into an explicit repository structure without promoting retrieval machinery to truth, WORLD, belief, decision, clinical, or theorem authority.

## Position

```text
query / observation context
        |
        v
Adaptive Retrieval Policy
  R0 lexical
  R1 lexical + bounded rewrite
  R2 semantic on demand
  R3 hybrid lexical + semantic
  R4 pre-embedded semantic retrieval
  R5 bounded relational / GraphRAG
        |
        v
query-scoped evidence candidate
        |
        +--> VerifyOS / provenance checks
        |
        +--> GraphRAG v0.2 only when R5 is least-sufficient
        |
        +--> BeliefOS evidence packet
        |
        +--> Replan / DecisionOS under their own authority boundaries
```

The selector never performs network access, vector search, GraphRAG traversal, belief commit, WORLD commit, or action execution. It chooses a retrieval presentation from explicitly supplied adequacy assessments.

## Core invariant

```text
selected mode = least complex mode explicitly assessed as adequate
```

If adequacy is unknown for any mode, the policy fails closed rather than assuming that a more complex mode is justified. If all modes are explicitly inadequate, it returns `NO_DATA` with a next-observation target.

The policy therefore separates two questions:

```text
1. Is a retrieval presentation adequate for this query context?
2. Among adequate presentations, which is least complex?
```

The runtime kernel answers only question 2. Question 1 must be supported by external measurement, evaluation, policy, or evidence appropriate to the deployment.

## Retrieval ladder

| Rank | Mode | Intended role |
|---:|---|---|
| R0 | `LEXICAL` | exact identifiers, domain terms, lexical/full-text retrieval |
| R1 | `LEXICAL_REWRITE` | bounded query rewriting before lexical retrieval |
| R2 | `SEMANTIC_ON_DEMAND` | transient/query-specific semantic retrieval |
| R3 | `HYBRID` | lexical + semantic fusion |
| R4 | `PREEMBEDDED` | stable-corpus precomputed semantic index |
| R5 | `GRAPH_RELATIONAL` | bounded relation/path/cycle evidence, including Gauge-Qi Process GraphRAG |

R5 is not a universal default. If any simpler mode is adequate, least-sufficient selection prevents R5 from being chosen.

## Context record

The runtime context records dimensions that can matter to adequacy assessment without turning any one dimension into a universal threshold:

```text
query_id
freshness_requirement
corpus_churn
query_pattern
request_scale
latency_cost_budget
operational_capability
provenance_requirement
```

The source article's numerical examples, including daily churn and query-volume bands, remain calibration hypotheses only. They are deliberately absent from the selector logic.

## Authority boundaries

Every receipt keeps these false:

```text
truth_authority_granted
world_commit_authority_granted
belief_authority_granted
decision_authority_granted
execution_authority_granted
clinical_authority_granted
theorem_authority_granted
```

Additional invariants:

```text
retrieval score != entailment
embedding similarity != semantic proof
index freshness != source freshness
vector database != WORLD model
GraphRAG != global ontology
retrieved evidence != verified evidence
selection != execution
```

## Dependent-origination interpretation

Adaptive Retrieval is a concrete AI realization target for the KuuOS dependent-origination program.

A retrieval mechanism is treated as a context-dependent presentation rather than intrinsic substance:

```text
query context C
  -> retrieval presentation P_C
  -> transported candidate evidence E_C
```

This suggests four downstream research directions:

```text
presentation invariance
  justified changes of retrieval presentation preserve specified semantics

descent
  compatible evidence from overlapping retrieval presentations glues coherently

obstruction
  incompatible lexical / semantic / relational evidence is represented explicitly

non-reification
  no retrieval index or graph is identified with the WORLD itself
```

These are research directions unless and until formal theorems connect the runtime structures to the general dependent-origination spine.

## Repository map

```text
docs/KUUOS_ADAPTIVE_RETRIEVAL_POLICY_v0_1.md
  design specification and rationale

docs/AdaptiveRetrieval/README.md
  subsystem entry surface

runtime/kuuos_adaptive_retrieval_policy_v0_1.py
  deterministic effect-free selector and receipt validator

scripts/check_kuuos_adaptive_retrieval_policy_v0_1.py
  deterministic executable validation

tests/test_kuuos_adaptive_retrieval_policy_v0_1.py
  regression tests

manifests/kuuos_adaptive_retrieval_policy_v0_1.json
  machine-readable scope and authority boundaries

formal/KUOS/Retrieval/AdaptiveRetrievalPolicyV0_1.lean
  least-sufficient and non-authority contract

formal/KUOS/Retrieval.lean
  subsystem formal aggregate
```

## Validation

```bash
PYTHONPATH=. python3 scripts/check_kuuos_adaptive_retrieval_policy_v0_1.py
PYTHONPATH=. python3 -m unittest tests.test_kuuos_adaptive_retrieval_policy_v0_1
lake build KUOS.Retrieval.AdaptiveRetrievalPolicyV0_1
```

Formal compilation proves the represented contract only. It does not establish empirical retrieval quality, source truth, clinical validity, or a universal theorem about retrieval systems.
