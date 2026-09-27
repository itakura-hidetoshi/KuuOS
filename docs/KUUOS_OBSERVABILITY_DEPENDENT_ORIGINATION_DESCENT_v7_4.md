# KuuOS Observability Dependent-Origination Descent v7.4

## 1. Why this is not a graph layer

v7.4 replaces the previously considered provenance-graph direction with the actual KuuOS dependent-origination structure.

The primary objects are not nodes and edges.

They are:

```text
presentations
conditioning families
presentation relation
local compatibility
descent sectors
obstruction witnesses
```

The runtime therefore asks:

```text
Which local observations are presentations of a shared conditioned context?
Do the related presentations remain locally compatible?
Can their bounded meaning descend presentation-independently?
If not, what exact obstruction prevents descent?
```

This is the runtime analogue of the KuuOS dependent-origination spine.

## 2. Formal reference

The theorem-level reference remains Lean.

### v4.49

`DependentOriginationAbstractPresentationDescentV4_49.lean` abstracts the core pattern:

```text
many representatives
+ presentation relation
+ quotient carrier
+ semantic data
+ presentation invariance
=> descent

related presentations
+ unequal semantics
=> explicit descent obstruction
```

Its exact theorem is stronger than this Python runtime layer because it proves quotient factorization and the exact obstruction criterion in Lean.

### v4.61

`DependentOriginationExactUniversalRestrictionWhiskeringV4_61.lean` has already moved the higher theorem line to preservation of left/right 2-cell whiskering across the presentation-unit restriction boundary.

v7.4 does not emulate or replace that theorem.

It records:

```text
runtime_descent_is_formal_theorem_proof = false
formal_v4_49_factorization_theorem_replaced = false
formal_v4_61_higher_coherence_replaced = false
```

The Python runtime is therefore a structurally aligned execution layer, not theorem authority.

## 3. Presentation

Every bounded provider observation is treated as a presentation.

For example:

```text
GitHub Actions CI observation
Vercel runtime observation
Supabase log observation
Neon branch observation
```

are not four substances and not four competing truths.

They are local presentations with explicit provenance.

The output preserves them individually under `presentations`.

No provider is privileged as the ultimate source.

## 4. Conditioning family — 縁

v7.3 supplies exact shared-context evidence such as:

- the same commit SHA;
- the same workflow run ID;
- the same deployment ID;
- the same request ID;
- the same trace ID;
- the same explicit correlation ID;
- the same artifact digest.

v7.4 does not reinterpret these identifiers as causes.

Instead each exact shared witness generates a **conditioning family**.

Conceptually:

```text
presentation A
       \
        shared exact condition
       /
presentation B
```

becomes:

```text
condition family C
presentations conditioned by C = {A, B}
```

The condition is relational evidence only.

It is explicitly non-reified:

```text
conditioning_relation_is_not_substance = true
```

Identifier values remain hidden. v7.4 receives only the hashed evidence already produced by v7.3 and hashes the condition representation again into a condition-family digest.

## 5. Generated presentation relation

If A and B share one exact condition, and B and C share another exact condition, then the runtime generates a presentation relation whose equivalence closure contains:

```text
[A] ~ [B] ~ [C]
```

This is not a claim that A, B and C are identical observations.

It means only that the available exact-context witnesses place them in one quotient-like presentation class for the purpose of testing descent.

This follows the formal KuuOS logic:

```text
representatives first
relation second
quotient/descent only when justified
```

rather than constructing one global object first and attaching observations to it afterward.

## 6. Local compatibility before descent

The transitive closure of conditioning evidence is not enough.

Suppose:

```text
A ~ B
B ~ C
```

The runtime must still re-observe the local semantic compatibility of:

```text
A/B
B/C
A/C
```

inside the generated class.

This is the important difference from a naive connectivity model.

### Successful descent

If every pair inside the generated class is temporally compatible:

```text
overlap
or
within_tolerance
```

the sector receives:

```text
descent_status = descended_contextual_presentation
```

and a deterministic `descended_presentation_id`.

The descended ID is an address for the quotient-like runtime presentation.

It is not a substance.

### Explicit obstruction

If a related presentation class contains:

```text
temporal_relation = disjoint
```

v7.4 retains:

```text
obstruction_kind =
  related_presentations_temporally_disjoint
```

and refuses descent.

This is the runtime form of the KuuOS rule:

> relation does not license quotient collapse when semantic compatibility fails.

### Held descent

If the local semantics are unavailable because of:

```text
insufficient_time_metadata
source_obstruction
missing_pair_presentation
```

the runtime does not guess.

It returns:

```text
descent_status = descent_held
```

This preserves the possibility of later descent after re-observation.

## 7. Isolated presentations

A presentation that shares no exact conditioning witness with another presentation remains:

```text
descent_status = local_presentation_only
```

This is not an error.

Dependent origination does not require every observation to collapse into one universal context.

Thus:

```text
local presentation != failed global model
```

## 8. Descent sectors rather than one global world

v7.4 can produce several independent sectors:

```text
Sector 1 -> descends
Sector 2 -> held
Sector 3 -> obstructed
Sector 4 -> local-only
```

It never automatically forms:

```text
one global observability object
```

The boundary is explicit:

```text
global_collapse_performed = false
many_presentations_preserved = true
```

This is closer to the KuuOS dependent-origination program than a provenance graph.

## 9. Empty / non-reified reading

The runtime interpretation is:

```text
presentation != intrinsic substance
provider != ultimate authority
condition != intrinsic cause
descent class != underlying thing-in-itself
local compatibility != global truth
runtime success != theorem authority
```

What is retained is the relation-conditioned ability of semantics to descend.

That is exactly why obstruction is first-class data rather than an exception to be erased.

## 10. Relationship to v7.0–v7.3

The observability chain is now:

```text
v7.0
bounded GitHub re-observation
        |
        v
v7.1
multiple local provider presentations
        |
        v
v7.2
bounded local temporal semantics
        |
        v
v7.3
exact conditioning witnesses
        |
        v
v7.4
dependent-origination presentation relation
        |
        +-- local compatibility
        |
        +-- descent
        |
        +-- held descent
        |
        +-- explicit obstruction
```

The resulting structure is not primarily a graph.

It is a family of presentations whose relational conditions may or may not permit descent.

## 11. Validation cases

The focused checker proves the runtime invariants for representative finite cases:

1. A–B and B–C exact conditions generate one transitive presentation class; A–C compatibility allows descent.
2. The same transitive class with A–C temporal incompatibility produces an explicit obstruction.
3. A provider-local obstruction holds descent open rather than forcing success or failure.
4. An isolated presentation remains local while another sector descends successfully.
5. A stale v7.3 packet digest is rejected.
6. A v7.3 packet bound to the wrong v7.2 temporal packet is rejected.
7. The emitted runtime packet contains no `nodes`, `edges`, or `graph` representation.

These Python checks establish runtime structural consistency only.

They do not replace the Lean theorem chain.

## 12. Next descent

The next step should stay inside dependent origination rather than returning to graph language.

The natural v7.5 target is:

```text
descent sectors
    +
overlapping conditioning families
    +
restriction compatibility
    +
higher local coherence
    ->
multi-sector descent compatibility
```

That would bring the observability runtime closer to the theorem frontier around restriction and higher compatible cells while preserving the authority boundary:

```text
runtime structure != Lean proof
```
