# KuuOS Observability Dependent-Origination Overlap v7.6

## Purpose

v7.6 keeps the observability line inside the KuuOS dependent-origination program.

The question is not whether a provenance graph is connected.

The question is:

> When two conditions overlap, do their restricted presentations agree on the common part, and what does that agreement actually license?

The answer is deliberately weaker than global descent.

```text
pairwise overlap compatibility
!=
global descent
```

This distinction is already present in the formal KuuOS spine and is now reflected in the bounded runtime.

## Formal references

### v3.13 — pairwise overlap compatibility

`DependentOriginationQuotientGaugeFootprintOverlapV3_13.lean` defines pairwise compatibility by existence of one local extension agreeing with two local restrictions on their respective footprints.

It proves concrete consequences on literally shared coordinates.

The key point is that pairwise compatibility is only a local condition.

### v3.16 — global compatible family

`DependentOriginationGlobalFootprintGluingV3_16.lean` separates nested pairwise witnesses from one simultaneously chosen family of local corrections that agrees on all overlaps.

For that concrete quotient-gauge setting, one globally compatible chosen family can be glued.

The important quantifier distinction is:

```text
for each pair, some compatible choices
```

versus

```text
one family of choices compatible for every pair
```

v7.6 preserves that distinction and does not promote pairwise overlap evidence to global amalgamation.

## Inputs

v7.6 consumes:

1. the v7.4 dependent-origination descent packet;
2. the v7.5 restriction packet.

Both are digest-bound in the v7.6 plan.

The v7.5 packet must itself point back to the exact v7.4 packet digest.

Thus the observation chain remains:

```text
v7.4 presentation/descent
        |
        v
v7.5 conditioning-family restriction
        |
        v
v7.6 overlap compatibility
```

## Common restriction

For two conditioning families

```text
C1
C2
```

v7.6 forms only their common presentation set:

```text
C1 ∩ C2
```

and compares the bounded restriction data there.

It does not compare unrelated presentations merely because they occur in the same larger sector.

### One shared presentation

If

```text
C1 ∩ C2 = {B}
```

the overlap is a single common presentation.

The runtime calls this:

```text
overlap_trivial_single_presentation
```

The shared presentation itself is the common restriction witness.

### Nontrivial overlap

If

```text
C1 ∩ C2 = {B, C}
```

the runtime also compares every bounded local semantic comparison among the shared presentations.

For a valid common restriction, the two family restrictions must present the same local relation as the canonical v7.4 sector.

If they do:

```text
overlap_compatible
```

If they disagree:

```text
overlap_restriction_mismatch
```

## Pairwise overlap does not imply global descent

The characteristic v7.6 case is:

```text
C1 = {A, B}
C2 = {B, C}

C1 restriction: compatible
C2 restriction: compatible
C1 ∩ C2 = {B}: compatible

but

A/C = disjoint
```

v7.5 already classifies this as a higher gluing obstruction.

v7.6 now strengthens the diagnosis:

```text
pairwise_overlap_compatible_but_global_descent_obstructed
```

This is a useful positive statement about the obstruction.

It says the failure is **not** located at the literal overlaps of the selected conditioning families.

At the same time, v7.6 does not infer a hidden cause, a global object, or a missing edge.

The result stays in dependent-origination language:

```text
local conditioned restrictions agree
but their generated presentation class still does not descend
```

## Overlap projection integrity

For a nontrivial overlap, v7.6 checks two things.

First, each family restriction must agree with the canonical v7.4 bounded semantics on the overlap.

Second, the two projected restrictions must agree with one another.

This catches a crossed or corrupted local presentation even when upstream status fields incorrectly say `restriction_compatible`.

The result is:

```text
overlap_restriction_mismatch
```

rather than silently accepting the upstream label.

## Unresolved overlap

If either local restriction is held because its observations are incomplete or transient, the overlap becomes:

```text
overlap_held
```

This propagates as a partial dependent-origination state rather than false agreement or false obstruction.

## Empty overlap

Two conditioning families can both occur in a larger sector without sharing a presentation directly.

Then:

```text
no_shared_presentation
```

is recorded.

Absence of overlap is not disagreement.

## No graph collapse

The primary runtime surfaces remain:

```text
presentations
conditioning families
restrictions
overlaps
descent sectors
obstructions
```

The packet fixes:

```text
primary_model_is_graph = false
global_collapse_performed = false
```

The runtime never needs to reinterpret the structure as nodes and edges.

## Authority boundary

v7.6 is a finite runtime consistency layer.

It does not prove the formal v3.13, v3.16, or v4.61 results and does not replace them.

The packet fixes:

```text
python_formal_theorem_authority = false
formal_v3_13_overlap_theorem_replaced = false
formal_v3_16_global_gluing_theorem_replaced = false
formal_v4_61_higher_coherence_replaced = false
```

## Validation

The focused checker covers:

1. singleton overlap inside a stable descent sector;
2. nontrivial two-presentation overlap with equal local semantics;
3. pairwise-compatible overlap with global descent obstruction;
4. an overlap projection mismatch;
5. an unresolved overlap;
6. stale restriction-packet digest rejection.

The checker also verifies that pairwise overlap compatibility never sets a global-descent conclusion by itself.

## Next dependent-origination step

The next step should refine the quantifier-order issue identified formally in v3.16.

The runtime currently knows:

```text
each selected conditioning family is locally valid
and pairwise overlaps can be checked
```

The next question is:

> Is there one simultaneously selected family of local presentations whose restrictions agree on every overlap at once?

That is a **simultaneous compatible-family** problem, not a graph problem.

A v7.7 layer can therefore distinguish:

```text
pairwise-compatible witnesses
```

from

```text
one globally selected overlap-compatible family
```

without yet claiming formal global amalgamation.
