# MemoryOS lineage quotient, dependency-adjusted confidence, and minimal revocation cut certificate kernel v0.1

## Frontier

This artifact advances MemoryOS from v0.68 provenance DAG admission to
MemoryOS v0.69 lineage-aware evidence aggregation.

The new layer adds four bounded capabilities:

1. source-lineage duplicate detection,
2. a quotient from raw evidence records to independent lineage roots,
3. dependency-adjusted exact-rational confidence,
4. a finite minimal revocation-cut certificate.

## Literature grounding

The construction binds five additional primary-source records:

- TierMem, *From Lossy to Verified* (`arXiv:2602.17913`),
- MemIR, *Mitigating Provenance-Role Collapse* (`arXiv:2605.25869`),
- *Governed Shared Memory for Multi-Agent LLM Systems* (`arXiv:2606.24535`),
- *Manufactured Confidence* (`arXiv:2606.29279`),
- *Episodic-to-Semantic Consolidation Without Identity Drift*
  (`arXiv:2607.01988`).

These papers motivate provenance-linked evidence, typed source roles,
governed propagation, protection against confidence inflation, and
deterministic auditable consolidation. They do not prove the KuuOS Lean
theorems.

## Lineage quotient

Raw record count is not treated as independent-source count.

Each evidence record contains:

- evidence identifier,
- lineage-root identifier,
- surface confidence,
- root confidence,
- a lineage weight budget,
- parent evidence identifiers.

Two distinct records with the same lineage root are duplicate evidence for
independence accounting even when one is a rewritten or consolidated copy.

The canonical profile contains:

- 12 raw evidence records,
- 8 independent lineage roots,
- 4 duplicate-lineage pairs,
- 5 quotient cases.

## Dependency-adjusted confidence

For each lineage root with budget `w` and multiplicity `m`, every stored copy
receives adjusted weight `w / m`. Therefore the copy weights sum back to `w`.

All copies use the confidence attached to the lineage root, not confidence
introduced by a later rewrite. The aggregate is the exact-rational weighted
average over lineage roots.

| Case | Naive repeated-source confidence | Lineage-adjusted confidence |
|---|---:|---:|
| language | `14/15` | `9/10` |
| repository frontier | `1` | `1` |
| safe retrieval policy | `53/60` | `17/20` |
| memory operations | `4/5` | `11/15` |
| authority boundary | `1` | `1` |

The strict reductions in the language, policy, and operations cases are
confidence-inflation prevention. Values equal to one cannot inflate further,
but still remain single-lineage and are flagged as load-bearing.

## Actual Lean package

`MemoryOSLineageQuotientRevocationCutV0_69.lean` proves:

- reflexivity, symmetry, and transitivity of same-lineage evidence,
- a duplicate lineage cannot count as independent evidence,
- splitting one lineage budget across two dependent copies conserves weight,
- root-scoped contribution is invariant under surface-confidence rewriting,
- duplicate-pair root contribution conservation,
- nonnegativity and unit-interval bounds for lineage-adjusted confidence,
- the canonical bridge cut blocks every retained legacy revocation path,
- the empty cut does not block those paths,
- the singleton bridge cut is erasure-minimal.

## Minimal revocation cut

The v0.68 legacy chain is:

```text
policy-legacy-root
  -> policy-legacy-derived
      -> policy-legacy-downstream
```

The finite path family from the revoked root to affected descendants is:

```text
[root, derived]
[root, derived, downstream]
```

Candidate cuts are subsets of `{derived, downstream}`. The unique
minimum-cardinality cut is `{policy-legacy-derived}`.

Its cardinality is one. Removing its only member leaves the empty set, which
does not block either path. The cut is an invalidation frontier, not deletion:
all source records, provenance paths, and digests remain available for audit.

## Load-bearing memory

Independent lineage count, rather than raw copy count, controls the
load-bearing flag.

- language: two independent lineages,
- retrieval policy: two independent lineages,
- memory operations: two independent lineages,
- repository frontier: one lineage, review flag retained,
- authority boundary: one lineage, review flag retained.

A duplicate summary never supplies redundancy for its own source.

## Trust boundary

The fail-closed runtime rejects:

- a changed v0.68 source certificate or collection digest,
- a raw copy presented as an independent source,
- promotion of rewritten surface confidence,
- altered dependency-adjusted confidence,
- a nonminimal cut presented as minimal,
- source deletion during revocation,
- candidate selection or execution authority,
- unexpected claims.

## Authority boundary

MemoryOS v0.69 remains future-only, read-only, and advisory.

Lineage quotienting is not DecisionOS candidate ranking. Confidence adjustment
is not truth authority. A minimal revocation cut does not delete evidence,
commit decisions, synthesize plans, activate tools, execute actions, or mutate
persistent WORLD state.
