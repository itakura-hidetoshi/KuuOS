# KuuOS Observability Presentation Invariance v7.7

## 1. Correction of direction

v7.7 corrects the emphasis of the observability-dependent-origination line.

The goal is **not** to make the audit progressively stricter.

The decisive KuuOS property is:

```text
different presentation
        +
same invariant
        ->
presentation-independent meaning
```

The relevant formal law is the v4.49 presentation-descent theorem.

For a presentation relation `S` and a semantic map

```text
semantic : Presentation -> Semantic
```

the formal invariant is

```text
p ~ q -> semantic(p) = semantic(q)
```

and factorization through the presentation quotient is equivalent to that invariance.

v7.7 mirrors this structure at runtime.

## 2. What is a presentation here?

A GitHub Actions observation and a Vercel observation can look completely different:

```text
provider
log format
timestamps
source digest
runtime fields
transport path
```

Those differences are presentation-local.

v7.7 therefore does **not** require raw observations to be equal.

It does not require providers to be equal.

It does not require presentation-local metadata to be equal.

Those would merely turn KuuOS into an increasingly strict comparison system.

Instead, one explicit invariant projection is chosen and applied uniformly.

## 3. Invariant projection

The input declares:

```text
invariant_projection_id
invariant_schema_digest
```

and then gives one bounded invariant value for each presentation.

For example, a CI/deployment invariant projection might map very different provider presentations to:

```text
{
  terminal_class,
  release_semantic,
  artifact_identity_class
}
```

The exact projection is domain-specific.

The runtime requirement is only that **the same projection and the same schema are used for every presentation being compared**.

This prevents the false move:

```text
presentation A -> projection A
presentation B -> projection B
then compare the outputs
```

which would not establish presentation invariance.

## 4. Presentation invariance

For a related sector

```text
P = {p1, p2, ..., pn}
```

and one common invariant projection `I`:

```text
I(p1) = I(p2) = ... = I(pn)
```

is the runtime presentation-invariance condition.

If it holds, v7.7 emits:

```text
presentation_invariance_status =
  presentation_invariant

runtime_descent_conclusion =
  presentation_independent_descent
```

and constructs a finite quotient-invariant witness containing the common invariant digest.

The original presentations are not deleted.

They simply cease to matter for the descended invariant meaning.

## 5. Different presentations are allowed

A key test case is intentionally:

```text
GitHub presentation:
  provider = github_actions
  source_digest = A
  time window = t1

Vercel presentation:
  provider = vercel
  source_digest = B
  time window = t2

but

I(GitHub) = I(Vercel)
```

Then v7.7 descends.

This is the desired behavior.

The runtime explicitly records:

```text
provider_equality_required = false
raw_observation_equality_required = false
presentation_local_equality_required = false
invariant_match_erases_presentation_dependence = true
```

## 6. What v7.4-v7.6 now mean

The earlier runtime layers remain useful, but their authority is narrowed.

### v7.4

v7.4 generates candidate presentation sectors from conditioned relations.

Its earlier `descended_contextual_presentation` status is now interpreted as:

```text
preinvariance candidate
```

not final presentation-independent descent.

### v7.5

v7.5 checks restriction/local-to-global compatibility.

### v7.6

v7.6 checks overlap compatibility and preserves the distinction between pairwise overlap and global gluing.

These are all **compatibility data**.

They help determine whether presentations can reasonably be tested together.

But:

```text
compatibility != presentation invariance
```

and:

```text
shared context != equal invariant
temporal proximity != equal invariant
overlap agreement != equal invariant
```

Only v7.7 turns a related family into presentation-independent meaning.

## 7. Obstruction

If related presentations have different invariant values under the **same** invariant projection:

```text
p ~ q
I(p) != I(q)
```

v7.7 emits:

```text
related_presentations_have_unequal_invariants
```

and denies descent.

This is structurally the runtime analogue of the v4.49 obstruction:

```text
related presentations
+
unequal semantics
->
no quotient factorization
```

The runtime obstruction is still not a Lean proof of the abstract theorem.

## 8. Held invariance

If a presentation relation is known but one invariant has not yet been observed:

```text
I(p) = observed
I(q) = held
```

v7.7 does not classify the sector as invariant or variant.

It returns:

```text
presentation_invariance_held
```

This is not stricter auditing.

It simply means the information needed to decide presentation independence is absent.

## 9. Invariant values are not reified

The invariant projection itself is not treated as ultimate truth.

A projection selects the semantic quantity relevant to one descent question.

Different questions may legitimately use different invariant projections.

Therefore:

```text
invariant projection != substance
invariant projection != ultimate truth
quotient invariant witness != thing-in-itself
```

The point is not that one invariant describes everything.

The point is that **once one semantic invariant has been specified, its value should not depend on presentation**.

## 10. Privacy and bounded storage

The raw invariant values are used only during runtime comparison.

The output stores only their SHA-256 digests.

Thus the quotient witness is presentation-independent without duplicating the raw invariant payload.

## 11. Formal correspondence

The v4.49 formal theorem has:

```text
Presentation
Setoid Presentation
semantic : Presentation -> Semantic
IsPresentationInvariant
HasPresentationQuotientFactorization
HasPresentationDescentObstruction
```

The v7.7 runtime shadow is:

```text
Presentation
  = bounded MCP observation presentation

presentation relation
  = v7.4 generated presentation sector

semantic
  = one explicit invariant projection

IsPresentationInvariant
  = every related presentation has one common invariant digest

runtime quotient witness
  = one common invariant digest attached to the whole finite sector

runtime obstruction
  = related pair with unequal invariant digests
```

The correspondence is structural only.

Lean remains theorem authority.

## 12. Validation

The focused checker verifies:

1. different providers, different raw presentations, and different source digests still descend when the invariant matches;
2. related presentations with different invariant values are obstructed;
3. a missing invariant holds descent open rather than generating an obstruction;
4. a v7.4 preinvariance success cannot bypass invariant mismatch;
5. every presentation must use the same invariant projection;
6. raw invariant values are not persisted.

The central regression test is therefore not “reject more.”

It is:

> **permit descent across genuinely different presentations exactly when the chosen invariant is unchanged.**
