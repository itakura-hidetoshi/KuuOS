# MemoryOS collusion, correlation-adjusted confidence, and weighted revocation cut certificate kernel v0.1

## Frontier

This artifact advances MemoryOS from v0.69 lineage-aware evidence aggregation to
MemoryOS v0.70 collusion-aware robust aggregation.

The layer adds four bounded capabilities:

1. multi-signal collusion detection across distinct lineage roots,
2. an exact correlation-adjusted effective independent-source count,
3. component-capped robust confidence aggregation,
4. a finite minimum-weight revocation-cut certificate on a branching DAG.

## Literature grounding

The construction binds five primary-source records:

- *Detecting Multi-Agent Collusion Through Multi-Agent Interpretability*
  (`arXiv:2604.01151`),
- *From Agent Traces to Trust* (`arXiv:2606.04990`),
- *Governed Collaborative Memory as Artificial Selection in LLM-Based
  Multi-Agent Systems* (`arXiv:2605.04264`),
- *Robust Aggregation of Correlated Information* (`arXiv:2106.00088`),
- *The Structure of Minimum Vertex Cuts* (`arXiv:2102.06805`).

These sources motivate multi-signal detection, provenance-bearing traces,
governed persistence, correlation-aware aggregation, and finite cut structure.
They do not prove the KuuOS formal theorems.

## Multi-signal collusion certificate

Four distinct lineage roots are retained:

- `source-a`, confidence `19/20`,
- `source-b`, confidence `19/20`,
- `source-c`, confidence `3/5`,
- `source-d`, confidence `7/10`.

A pair is marked as suspected collusion only when all of the following hold:

- the lineage roots are distinct,
- provenance overlap is at least `1/2`,
- behavioral correlation is at least `3/4`,
- synchronized support is present.

Only `source-a :: source-b` satisfies the full rule. No single signal is
sufficient by itself.

The exact profile contains:

- 4 source-agent records,
- 6 unordered pair-signal records,
- 1 suspected collusion pair,
- 3 resulting collusion components.

The component partition is:

```text
{source-a, source-b}
{source-c}
{source-d}
```

## Correlation-adjusted effective source count

The four sources have unit weights. The correlation matrix has diagonal one,
correlation `3/4` between `source-a` and `source-b`, and zero for every other
off-diagonal pair.

The exact effective count is

```text
n_eff = (sum w)^2 / (w^T R w)
      = 16 / (11/2)
      = 32/11.
```

The independent baseline is `4`. Positive pair correlation therefore reduces
the effective count from `4` to `32/11` without deleting any source record.

Raw source count is retained for audit, but it is not used as the independent
evidence count.

## Component-capped robust confidence

Naive equal-weight aggregation counts both members of the suspected component:

```text
(19/20 + 19/20 + 3/5 + 7/10) / 4 = 4/5.
```

The robust certificate gives the suspected component one total weight budget.
Its representative confidence is `19/20`; the two independent singleton
components retain `3/5` and `7/10`.

```text
(19/20 + 3/5 + 7/10) / 3 = 3/4.
```

The exact inflation removed is `1/20`.

This estimator is deliberately finite and bounded. It does not claim a general
optimal robust estimator for arbitrary dependence structures.

## Actual Lean package

`MemoryOSCollusionCorrelationWeightedCutV0_70.lean` proves:

- the collusion rule requires distinct lineages,
- the canonical multi-signal pair is detected,
- the benign canonical pair is rejected,
- four independent sources have effective count `4`,
- one `3/4` correlated pair gives effective count `32/11`,
- every positive value of the one-pair correlation parameter reduces the
  effective count below `4`,
- splitting a collusion-component budget across two copies conserves weight,
- the component contribution is conserved,
- naive confidence is exactly `4/5`,
- component-capped confidence is exactly `3/4`,
- the component-capped value remains in `[0,1]`,
- the canonical branch cut blocks every path,
- its weight is `2`, while the one-node hub cut has weight `3`,
- the two-node branch cut is the unique minimum-weight cut in the finite
  inclusion-minimal blocking family.

## Minimum-weight revocation cut

The branching revocation DAG is:

```text
legacy-root
  -> legacy-hub
       -> legacy-branch-a -> legacy-leaf-a
       -> legacy-branch-b -> legacy-leaf-b
```

Candidate-node costs are:

| Node | Cost |
|---|---:|
| `legacy-hub` | `3` |
| `legacy-branch-a` | `1` |
| `legacy-branch-b` | `1` |
| `legacy-leaf-a` | `2` |
| `legacy-leaf-b` | `2` |

The minimum-cardinality cut is `{legacy-hub}` with cardinality `1` and cost
`3`.

The unique minimum-weight cut is

```text
{legacy-branch-a, legacy-branch-b}
```

with cardinality `2` and total cost `2`.

This separates cardinality minimization from operational-cost minimization.
The cut is an invalidation frontier only: source records, paths, and digests
remain available for audit.

## Exact runtime profile

The canonical runtime emits:

- 5 literature records,
- 4 source-agent records,
- 6 pair-signal records,
- 1 suspected collusion pair,
- 3 collusion components,
- 10 upper-triangular correlation entries,
- 2 effective-count records,
- 1 robust-confidence record,
- 6 revocation nodes,
- 5 revocation edges,
- 2 revocation paths,
- 32 cut candidates,
- 1 unique minimum-weight cut,
- 8 full-rank transport records,
- 4 singular atomic records,
- 3 rank-one source boundaries.

All confidence, correlation, effective-count, and cut-weight calculations use
exact rational arithmetic.

## Trust boundary

The fail-closed runtime rejects:

- a changed v0.69 source certificate or collection digest,
- altered provenance-overlap or behavioral-correlation evidence,
- raw source count presented as effective independent count,
- collusive members counted as independent robust components,
- altered robust confidence,
- the minimum-cardinality hub cut presented as minimum-weight,
- source deletion during revocation,
- candidate selection or execution authority,
- unexpected claims.

## Authority boundary

MemoryOS v0.70 remains future-only, read-only, and advisory.

Collusion detection is not DecisionOS candidate ranking. Correlation adjustment
and robust confidence are not truth authority. The minimum-weight cut does not
delete source history, commit decisions, synthesize plans, activate tools,
execute actions, or mutate persistent WORLD state.
