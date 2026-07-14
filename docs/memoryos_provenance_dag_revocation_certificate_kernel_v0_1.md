# MemoryOS provenance DAG, confidence aggregation, and revocation certificate kernel v0.1

## Frontier

This artifact advances MemoryOS from v0.67 forgetting-aware admission to
MemoryOS v0.68 provenance-aware admission.

The source certificate remains append-only and contradiction-safe. The new
layer adds four bounded capabilities:

1. a version-increasing provenance DAG,
2. conflict components equipped with a partial rather than forced-total order,
3. exact-rational multi-source confidence aggregation,
4. revocation propagation from an ancestor to all dependent descendants.

## Literature continuity

The layer retains the eight primary-source records bound by v0.67:

- Memory OS of AI Agent (`arXiv:2506.06326`),
- Rethinking Memory in AI (`arXiv:2505.00675`),
- A-MEM (`arXiv:2502.12110`),
- Mem0 (`arXiv:2504.19413`),
- EvolMem (`arXiv:2601.03543`),
- MemoryArena (`arXiv:2602.16313`),
- From Recall to Forgetting / Memora (`arXiv:2604.20006`),
- Beyond Similarity / MemGate (`arXiv:2606.06054`).

The new construction operationalizes dynamic linking, graph memory,
forgetting-aware evaluation, and trustworthy query-conditioned retrieval
without claiming that any cited paper proves the KuuOS formal theorems.

## Provenance node

Each finite node contains:

- node identifier,
- claim key and value,
- source identifier,
- scope,
- version,
- exact rational confidence,
- validity and revocation flags,
- a finite set of parent node identifiers.

A direct dependency `parent -> child` is accepted only when:

- the parent identifier occurs in the child's parent set,
- `parent.version < child.version`,
- parent and child have the same scope.

The strict version inequality makes a directed cycle impossible.

## Actual Lean package

`MemoryOSProvenanceDAGRevocationV0_68.lean` proves:

- conflict symmetry,
- direct dependency irreflexivity,
- reflexivity and transitivity of provenance precedence,
- every nontrivial provenance path strictly raises version,
- antisymmetry of provenance precedence,
- impossibility of a strict provenance cycle,
- transitive propagation of revocation effects,
- admission failure in the presence of any revoked ancestor,
- direct revoked-parent exclusion,
- nonnegativity and unit-interval bounds for exact weighted confidence.

The path relation is therefore a partial order. It is deliberately not a total
order: two contradictory sources may remain incomparable when neither depends
on the other.

## Exact runtime profile

The canonical profile contains:

- 15 provenance nodes,
- 9 direct edges,
- 10 strict ancestor/descendant pairs,
- 2 contradiction components,
- 3 revocation-affected nodes,
- 4 exact multi-source confidence records,
- 5 query-conditioned admissions,
- 8 full-rank transport records,
- 4 singular atomic transport records,
- 3 rank-one source boundaries.

The exact aggregate confidences are:

- language synthesis: `9/10`,
- repository frontier: `1`,
- safe retrieval-policy synthesis: `17/20`,
- memory-operation synthesis: `11/15`.

No floating-point confidence calculation is used.

## Revocation semantics

The canonical revoked root is the legacy similarity-only retrieval policy.
Its direct child and grandchild remain in the append-only archive, but all
three are excluded from active admission.

Revocation therefore means:

- preserve source and dependent history,
- preserve provenance paths and digests,
- block the revoked node,
- block every reachable descendant,
- do not erase audit evidence.

The independent query-conditioned policy branch remains admissible because it
has no dependency path from the revoked root.

## Conflict partial order

Two finite contradiction components are retained:

- project frontier,
- retrieval policy.

The project frontier is ordered from v0.67 to v0.68 by an explicit dependency.
The legacy retrieval-policy branch is internally ordered, while the safe
query-conditioned branch is intentionally incomparable with the revoked
legacy branch. Confidence does not manufacture a dependency edge.

## Trust boundary

The certificate rejects:

- non-version-increasing edges,
- cycles,
- unknown parents,
- cross-scope dependencies,
- altered source or collection digests,
- admission of a revoked descendant,
- deletion of a source record during revocation,
- altered confidence aggregates,
- similarity-only admission,
- candidate-selection or execution authority claims,
- unexpected claims.

## Authority boundary

MemoryOS v0.68 is future-only, read-only, and advisory.

Provenance precedence is not DecisionOS candidate ranking. Confidence
aggregation is not truth authority. Revocation propagation does not mutate
persistent WORLD state, delete source history, activate tools, synthesize
plans, commit decisions, or execute actions.
