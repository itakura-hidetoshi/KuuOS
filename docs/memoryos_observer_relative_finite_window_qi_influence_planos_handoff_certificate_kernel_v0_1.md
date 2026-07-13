# MemoryOS v0.41 Observer-Relative Finite-Window Qi Influence PlanOS Handoff

## Position

MemoryOS v0.40 records an observer-relative, append-only past and proves a finite
non-Markov witness.  MemoryOS v0.41 closes the next read-only edge of the temporal
cycle by compiling that past into a source-bound influence packet for the future
PlanOS v1.23 history family.

```text
MemoryOS v0.40 complete observer-relative ledger
  -> suffix finite-window projection
  -> exact visible residue for the discarded prefix
  -> candidate-specific Qi history influence functional
  -> future-only advisory PlanOS handoff
```

The layer does not select, rank, prune, activate, execute, or mutate a plan.

## Canonical components

Each v0.40 record is projected into the ordered integer component vector

```text
body
boundary
leak
observation
holonomy
recovery
rollback
lockin
residue
```

Observer identity, event identity, source record digest, record order, translation
residue visibility, and observation/backaction visibility remain attached to the
projection.

## Finite-window projection

Let the complete ordered record ledger be

```text
R = (r_0, ..., r_{n-1})
```

and let the retained suffix window have length `L`:

```text
W_L = (r_{n-L}, ..., r_{n-1})
```

The discarded prefix is not deleted.  Its exact componentwise residue is

```text
rho_tail = sum_{i < n-L} h(r_i)
```

The supplied tail residue must equal this exact sum.  Hidden, altered, or omitted
tail residue is rejected.

Therefore:

```text
finite-window projection != Markov replacement
```

## Exact influence functional

For PlanOS history `p`, lag weights `k_l`, record component vectors `h_l`, and
history-specific coupling vector `g_p`, v0.41 computes

```text
I_p
  = sum_l k_l <g_p, h_l>
  + <g_p, rho_tail>
```

and the advisory conditioned action numerator

```text
S_p^memory = S_p^base + I_p
```

All arithmetic is exact integer arithmetic.  The common positive action
denominator is preserved.

## Reference witness

For the two-record suffix window, lag weights `[3, 2]`, and the reference coupling
for `plan-history-a`:

```text
window influence = 34
tail influence   = 9
total influence  = 43
base action       = 11
conditioned action = 54
window-only action = 45
```

Hence the visible tail changes the candidate action by exactly `9`:

```text
54 - 45 = 9
```

The finite suffix alone is therefore not identified with the full non-Markov
history.

## PlanOS support preservation

The candidate coupling family must cover exactly the history identifiers retained
by the PlanOS v1.23 partial-dephasing certificate.  Output order is the source
PlanOS order.

```text
all source histories retained = true
history pruning performed = false
history ranking performed = false
representative selected = false
plan selection performed = false
```

Influence values may differ between histories, but v0.41 does not interpret those
values as a decision or argmin.

## Source binding

The MemoryOS source receipt binds:

- the v0.40 schema and accepted certificate digest
- complete record identifiers and digests
- observer identifiers
- translation identifiers
- the exact v0.40 record-ledger digest
- the v0.40 temporal-cycle digest
- the finite non-Markov witness

The PlanOS source receipt binds:

- the v1.23 schema and input digest
- the complete retained history support
- non-pruning, non-ranking, and non-selection state

Any source substitution, record reordering, record-digest substitution, observer
substitution, or candidate-support substitution is rejected.

## Fail-closed cases

The checker rejects:

- invalid source schema or non-accepted source receipt
- invalid v0.40 ledger digest
- record ID, digest, observer, or sequence substitution
- hidden translation residue
- hidden observation/backaction contribution
- invalid or all-zero lag weights
- window length outside the bounded record family
- altered discarded-tail residue
- PlanOS candidate coupling support mismatch
- claim substitution
- pruning, ranking, representative selection, plan selection, decision commit,
  activation, execution, source mutation, WORLD mutation, verification, or truth
  authority claims

## Mathlib theorem surface

The formal module provides:

- exact component contraction
- exact lag-weighted finite-window contraction
- exact tail-residue contribution
- reference window influence `34`
- reference tail influence `9`
- reference full influence `43`
- reference conditioned action `54`
- the identity

```text
conditionedAction - windowOnlyAction = componentDot couplings tailResidue
```

- nonzero tail implies the full conditioned action differs from the window-only
  action
- complete PlanOS support preservation
- non-authority and read-only boundaries

## Fixed boundaries

```text
MemoryOS projection != source-history replacement
finite window != Markov semantics
tail compression != tail deletion
influence functional != causal truth
conditioned action != candidate ranking
conditioned action != plan selection
history support preservation != decision commit
advisory handoff != activation
advisory handoff != execution
runtime validation != verification result
```
