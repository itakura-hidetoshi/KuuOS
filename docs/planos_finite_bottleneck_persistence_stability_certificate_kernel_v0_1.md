# PlanOS finite bottleneck persistence stability certificate kernel v0.1

## Status

PlanOS v1.18 finite-diagram comparison layer.

This layer consumes two retained PlanOS v1.17 barcode certificates and produces a bounded, read-only certificate for:

- finite persistence-diagram normalization through dimension two,
- exact point-to-point and point-to-diagonal costs,
- deterministic optimal bottleneck matching,
- exact bottleneck distance encoded in doubled integer units,
- retained simplex-filtration endpoint bindings,
- a finite observed stability inequality against an explicitly recomputed filtration sup norm.

It does not mutate either source barcode certificate or WORLD state and grants no selection, activation, adapter, tool, or execution authority.

## Exact doubled-distance encoding

To avoid floating-point ambiguity, all persistence-diagram costs are stored as twice their mathematical value.

For finite points

```text
p = (birth_p, death_p)
q = (birth_q, death_q)
```

the point-to-point cost is

```text
cost_twice(p,q)
  = 2 * max(|birth_p - birth_q|, |death_p - death_q|).
```

For two infinite intervals, the cost is

```text
2 * |birth_p - birth_q|.
```

A finite point has diagonal cost

```text
cost_twice(p, diagonal) = death_p - birth_p.
```

Thus an interval of persistence two has mathematical diagonal distance one and stored doubled cost two.

An infinite interval cannot be matched to the diagonal.

## Finite optimal matching

Matching is performed independently in homological dimensions 0, 1, and 2.

For each dimension, bounded dynamic programming considers:

- point-to-point matches,
- left-point-to-diagonal matches for finite intervals,
- unmatched finite right points as diagonal-to-right matches.

Every source interval is used exactly once. Infinite points require infinite partners. The objective minimizes the maximum doubled edge cost. Ties are resolved deterministically by preferring point-to-point matches and then lexicographic interval identifiers.

The complete bottleneck distance is the maximum over all dimensions.

## Endpoint binding and perturbation records

Every barcode interval is bound to retained simplex identifiers:

- the birth simplex has the same dimension as the interval,
- a finite death simplex has dimension one higher,
- retained filtration values equal the interval birth and death coordinates.

A simplex perturbation record contains:

```text
simplex_id
dimension
filtration_a
filtration_b
source_simplex_digest_a
source_simplex_digest_b
```

The finite sup norm is recomputed as

```text
max_simplex |filtration_a - filtration_b|.
```

The source filtration-to-barcode derivation is not recomputed in v1.18; it remains provenance-bound to the two v1.17 certificate digests.

## Finite stability witness

The kernel verifies the instance-level inequality

```text
bottleneck_distance_twice <= 2 * filtration_sup_norm.
```

This is a finite observed witness for the retained diagrams and perturbation records. It is not promoted to the general persistence stability theorem.

## Reference diagrams

Diagram A contains:

```text
H0 [0,2)
H0 [0,infinity)
H1 [2,6)
```

Diagram B contains:

```text
H0 [1,3)
H0 [1,infinity)
H1 [3,7)
H1 [4,6)
```

The deterministic optimal matching is:

```text
A H0 [0,2)         -> B H0 [1,3)         cost_twice 2
A H0 [0,infinity)  -> B H0 [1,infinity)  cost_twice 2
A H1 [2,6)         -> B H1 [3,7)         cost_twice 2
diagonal           -> B H1 [4,6)         cost_twice 2
```

Therefore

```text
bottleneck_distance_twice = 2
bottleneck_distance = 1
filtration_sup_norm = 1
stability_budget_twice = 2
stability_slack_twice = 0
```

The extra finite H1 interval exercises actual diagonal matching.

## Fail-closed conditions

The certificate is blocked for, among other cases:

- missing source certificate digests,
- stale input digest,
- malformed or duplicate interval identifiers,
- malformed or duplicate simplex perturbation records,
- endpoint identifiers absent from perturbation records,
- birth/death dimension mismatch,
- birth/death filtration mismatch,
- an infinite interval without an infinite partner,
- incorrect optimal matching claims,
- incorrect doubled bottleneck distance,
- incorrect filtration sup norm,
- violation of the finite stability inequality,
- coordinate, interval-count, or simplex-record limits being exceeded.

## Formal package

`formal/KUOS/PlanOS/FiniteBottleneckPersistenceStabilityV1_18.lean` proves:

- doubled point-to-point cost is symmetric,
- finite diagonal doubled cost equals interval persistence,
- valid finite intervals have positive diagonal cost,
- infinite intervals cannot match the diagonal,
- a checked distance bound yields the finite stability witness,
- the reference matching has doubled bottleneck two,
- the extra interval `[4,6)` has doubled diagonal cost two,
- the reference comparison saturates the sup-norm budget,
- bottleneck and stability evidence grants no authority,
- the certificate remains finite, read-only, future-only, and inactive.

## Fixed boundaries

```text
finite diagram pair != all planning-space persistence diagrams
observed inequality != general persistence stability theorem
source barcode digest != source barcode recomputation
endpoint binding != proof of full filtration-to-barcode functoriality
bottleneck distance != Wasserstein distance
bottleneck distance != interleaving distance
long persistence != candidate utility
small distance != activation authorization
diagonal match != feature deletion authority
stability witness != plan selection
WORLD-conditioned topology != WORLD mutation
```

## Integration

The layer is connected through:

- runtime schema support,
- runtime bottleneck algebra support,
- certificate support facade,
- runtime certificate kernel,
- fail-closed checker,
- Mathlib package and versioned aggregate,
- machine-readable manifest,
- the integrated current PlanOS root.
