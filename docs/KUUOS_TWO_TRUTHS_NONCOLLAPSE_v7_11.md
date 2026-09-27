# KuuOS Two Truths Non-collapse v7.11

## Purpose

v7.11 prevents a new failure that becomes possible once presentation invariance gets strong.

The earlier chain can establish:

```text
different presentations
  -> same invariant
  -> same canonical carrier
  -> same carrier meaning
  -> same projection-choice-independent meaning
```

That is useful.

But it must not imply:

```text
therefore every conventional world is interchangeable
```

KuuOS already defines 二諦 as a non-collapse boundary between 勝義諦 and 世俗諦.

v7.11 makes that boundary explicit in the observability/dependent-origination runtime.

## The central rule

Two semantic subjects may share the same paramartha-level meaning:

```text
Paramartha(A) = Paramartha(B)
```

while their conventional operational worlds remain different:

```text
Samvrti(A) != Samvrti(B)
```

This is not an error.

It is a legitimate two-truths state.

The runtime records:

```text
same_paramartha_distinct_samvrti_worlds
```

and fixes:

```text
conventional_substitution_allowed = false
samvrti_distinction_required = true
samvrti_difference_is_error = false
```

## Example

Suppose two subjects descend to the same non-reifying invariant meaning.

One is instantiated in a clinical world:

```text
scope:
  clinical

operation:
  treat

conditions:
  patient present

governance:
  clinical authority

constraints:
  consent required
```

The other is instantiated in a research world:

```text
scope:
  research

operation:
  analyze

conditions:
  dataset present

governance:
  research authority

constraints:
  no direct patient care
```

Their paramartha carrier may be the same.

Their samvrti operational signatures are not.

The two truths boundary therefore preserves both:

```text
same ultimate non-reifying meaning
+
different conventional responsibility
```

The clinical and research worlds must not become operationally substitutable merely because the invariant carrier agrees.

## Paramartha in v7.11

The paramartha surface is not a highest substance.

It is the non-reifying semantic equivalence inherited from v7.10.

Operationally it answers:

```text
what presentation-dependent distinctions have ceased to matter
for this chosen invariant question?
```

It does not answer:

```text
what conventional action is appropriate?
```

That remains a samvrti question.

## Samvrti in v7.11

A conventional operational world is represented by a bounded signature over:

- conventional operational value;
- scope;
- conditions;
- governance boundary;
- action constraints;
- visible residuals;
- lineage digest.

The world label itself is not semantic identity.

Two differently named worlds can still have the same samvrti operational signature.

Conversely, two subjects sharing one paramartha carrier can have different samvrti signatures.

## Same paramartha, same samvrti

If two subjects have:

```text
same paramartha carrier
+
same samvrti operational signature
```

v7.11 records:

```text
same_paramartha_same_samvrti_operation
```

and conventional substitution is permitted.

This is the stronger condition needed for operational interchangeability.

## Same paramartha, distinct samvrti

If:

```text
same paramartha carrier
+
different samvrti operational signature
```

v7.11 records:

```text
same_paramartha_distinct_samvrti_worlds
```

This relation is valid and READY.

It is not an obstruction.

The difference is preserved because responsibility, scope, action and local conditions still matter conventionally.

## Unresolved samvrti

If paramartha equivalence is established but one samvrti surface is held or unavailable:

```text
same_paramartha_samvrti_unresolved
```

The runtime returns PARTIAL.

It does not infer either conventional equality or conventional difference.

## Middle Way

This implements the KuuOS middle-way bridge in both directions.

### Against reification

A samvrti world is not promoted to ultimate substance.

### Against nihilistic collapse

Paramartha equivalence cannot erase:

- responsibility;
- action constraints;
- local scope;
- lineage;
- residual uncertainty;
- conditioned operational differences.

Thus:

```text
paramartha equivalence
!=
permission to ignore samvrti
```

## Relation to the existing KuuOS core

The design directly matches:

```text
docs/KUOS_CORE_CHARTER_v0_1.md
docs/PARAMARTHA_SAMVRTI_MIDDLE_WAY_BRIDGE_v0_1.md
docs/SAMVRTI_QI_LAYER_v0_1.md
```

The existing bridge states that 世俗諦 is not false merely because it is conventional, and that emptiness must not erase responsibility, action, care or repair.

v7.11 turns that principle into an explicit runtime distinction.

## Relation to presentation invariance

The chain is now:

```text
presentation
  -> invariant
  -> presentation-independent carrier
  -> carrier-model independence
  -> invariant-projection-choice independence
  -> paramartha equivalence
  -> two-truths separation
  -> samvrti-preserving operation
```

The key correction is that the final arrow does not collapse back to one world.

Instead:

```text
one paramartha class
can support multiple samvrti worlds
```

provided those worlds remain explicitly conditioned and non-reified.

## Validation

The focused checker verifies:

1. same paramartha meaning plus different clinical/research worlds is READY, not an error;
2. conventional substitution is forbidden across different samvrti signatures;
3. same paramartha plus same samvrti signature permits substitution;
4. different world labels alone do not create conventional semantic difference;
5. held samvrti data yields PARTIAL rather than forced collapse;
6. raw conventional operational values are not persisted;
7. stale source binding is rejected.

The central law is:

> **勝義諦で同じでも、世俗諦の条件・作用・責任が違うなら、その差異は残さなければならない。**
