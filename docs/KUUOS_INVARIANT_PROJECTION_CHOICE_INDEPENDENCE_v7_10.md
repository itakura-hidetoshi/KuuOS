# KuuOS Invariant Projection Choice Independence v7.10

## Purpose

v7.10 moves presentation independence one level higher.

v7.7 removed dependence on provider/raw presentation once a chosen invariant was fixed.

v7.8 made the canonical carrier depend only on that invariant.

v7.9 removed dependence on the concrete runtime model used to encode that carrier.

v7.10 now asks:

> Does the meaning still depend on which valid invariant projection was chosen?

The answer is not obtained by demanding literal equality of the local invariant values.

Instead:

```text
projection A local invariant
        \
         -> common normalized observable
        /
projection B local invariant
```

and only the normalized observable is tested for choice independence.

## Projection choice is itself a presentation

Suppose the same operational situation can be described by two invariant projections.

Projection A:

```json
{"status": "success"}
```

Projection B:

```json
{"exit_code": 0}
```

These local invariant values are not equal.

v7.10 does not reject that difference.

If both map to:

```json
{"release": "same", "terminal": "success"}
```

under one explicitly declared normalized observable, they carry the same choice-independent meaning.

Thus:

```text
local invariant equality
is not required
```

and:

```text
projection ID
does not define semantic identity
```

## Common normalized observable

Every v7.10 input family declares exactly one:

```text
normalized_observable_id
normalized_schema_digest
```

Each projection presentation has its own:

```text
projection_id
projection_schema_digest
comparison_certificate_digest
```

and for each semantic subject contributes:

```text
local_invariant_value
normalized_observable_value
```

The runtime compares only the normalized observable values across projection choices.

Raw values are never copied to the output.

## Choice-independent descent

For a semantic subject x and projection choices P₁,...,Pₙ:

```text
N(P₁(x)) = N(P₂(x)) = ... = N(Pₙ(x))
```

implies:

```text
projection_choice_invariant
```

and one carrier element:

```text
choice-independent-invariant-...
```

whose identity depends only on:

```text
normalized_observable_id
normalized_schema_digest
normalized_observable_digest
```

It does not depend on projection ID.

## Why this is not stricter auditing

The intended behavior is permissive with respect to presentation.

Different local invariant values are allowed.

Different projection schemas are allowed.

Different projection names are allowed.

Different comparison certificates are allowed.

The only question is whether those different presentations preserve the same higher observable.

So the runtime law is:

```text
different invariant presentations
+
same normalized observable
->
same higher meaning
```

not:

```text
different presentations
->
reject more aggressively
```

## Obstruction

If:

```text
N(P₁(x)) != N(P₂(x))
```

for the same semantic subject and same normalized observable definition, v7.10 records:

```text
projection_choices_disagree_after_common_normalization
```

This is a genuine choice-dependence obstruction.

The obstruction occurs only after the two local invariants have been compared in the same normalized semantic codomain.

## Held state

If one projection is missing, held, or unavailable, but the observed projections do not disagree, v7.10 returns:

```text
projection_choice_invariance_held
```

Missing evidence is not converted into semantic disagreement.

## Formal correspondence to v1.28

The formal reference is:

```text
DependentOriginationNormalizationChoiceInvariantV1_28.lean
```

There, two normalization choices are not required to be literally equal.

They are connected by explicit coherent comparison data, and coherent observables are proved to take the same value across the two choices.

The theorem-level pattern is:

```text
different normalized representatives
+
strong coherent comparison
+
coherent observable
->
same observable value
```

The v7.10 runtime shadow is:

```text
different invariant projections
+
comparison certificate provenance
+
one common normalized observable
->
same normalized observable digest
```

v7.10 does not construct or verify Mathlib strong transformations, adjoint equivalences, or naturality isomorphisms.

Lean remains theorem authority.

## Relation to v7.7-v7.9

The runtime chain is now:

```text
provider presentation
  ->
chosen invariant projection                    v7.7
  ->
canonical invariant carrier                    v7.8
  ->
replaceable carrier model                      v7.9
  ->
replaceable invariant projection choice        v7.10
  ->
choice-independent normalized meaning
```

Each step erases one layer of accidental presentation.

## Validation

The focused checker verifies:

1. different local invariant values can descend to one normalized meaning;
2. renaming projection IDs and changing local invariant representations does not change the choice-independent carrier;
3. disagreement after common normalization is an obstruction;
4. held projection data keeps choice independence undecided rather than false;
5. a subject missing from one projection produces held, not obstruction;
6. the normalized observable identity must be fixed uniformly by the plan;
7. raw local invariant and normalized observable values are not persisted.

The central law is:

> **the invariant projection itself is only another presentation unless its output has been shown to descend to a common normalized observable.**
