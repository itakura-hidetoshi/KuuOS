# KuuOS Observability Invariant Carrier v7.8

## Purpose

v7.8 takes the decisive step after v7.7 presentation invariance.

v7.7 establishes:

```text
different presentations
+
same invariant
->
presentation-independent descent is allowed
```

v7.8 turns that into an explicit canonical runtime map.

The central rule is:

```text
CarrierId(p)
=
H(
  invariant_projection_id,
  invariant_schema_digest,
  invariant_digest(p)
)
```

Nothing presentation-local enters the carrier identity.

## What disappears

The following may differ without changing the carrier element:

- provider;
- presentation ID;
- sector ID;
- raw log structure;
- source digest;
- timestamp layout;
- local transport path;
- MCP implementation.

If the chosen invariant projection gives the same invariant value, the canonical carrier element is literally the same runtime identifier.

This is the desired meaning of:

```text
presentation-independent
```

rather than merely “checked by a stricter auditor.”

## Canonical runtime map

The runtime now has an explicit map:

```text
presentation
    |
    | invariant projection
    v
invariant digest
    |
    v
canonical carrier element
```

Two presentations with the same invariant digest under the same projection/schema receive exactly the same carrier element ID.

Thus:

```text
p != q
provider(p) != provider(q)
sector(p) != sector(q)

but

I(p) = I(q)

=>

Carrier(p) = Carrier(q)
```

## Cross-sector identification

The carrier identity does not depend on sector identity.

Therefore even two independently formed v7.7 sectors map to the same carrier element when their invariants agree.

This matters because presentation independence should not be accidentally limited by how the runtime happened to partition observations into sectors.

A sector is evidence for invariance.

It is not part of the invariant itself.

## Distinct invariants remain distinct

v7.8 does not erase real semantic differences.

If:

```text
I(p) != I(q)
```

then their carrier element IDs differ.

If v7.7 says the presentations are related but invariant values differ, the corresponding sector remains obstructed rather than being forcibly collapsed.

## Held invariants

If a presentation has not yet produced an invariant value, its canonical image is undefined.

The runtime preserves:

```text
carrier_factorization_held
```

rather than assigning a placeholder carrier element.

This keeps absence of invariant information distinct from invariant equality.

## Relation to formal presentation universality v2.0

The formal reference is:

```text
formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean
```

There the canonical presentation-independent completion is Mathlib's localization:

```text
W.Localization
```

with canonical map:

```text
W.Q : Context ⥤ W.Localization
```

and a genuine universal mapping property:

```text
(W.Localization ⥤ Target)
  ≌
W.FunctorsInverting Target
```

The formal theorem also gives essential uniqueness of alternative localization carriers up to equivalence compatible with the canonical maps.

v7.8 does **not** claim this theorem for the runtime hash carrier.

The runtime carrier is only a finite structural shadow:

```text
presentation
-> invariant
-> canonical carrier element
```

The packet explicitly records:

```text
python_formal_universality_authority = false
formal_v2_0_universal_property_replaced = false
```

## Why the carrier identity uses the projection ID

The same raw value under two different semantic questions need not mean the same thing.

Therefore:

```text
same invariant payload
+
different invariant projection
```

does not automatically define the same carrier element.

Carrier identity includes:

```text
invariant_projection_id
invariant_schema_digest
invariant_digest
```

This keeps the semantic question explicit while erasing presentation-local detail.

## Sector factorization

For each v7.7 sector:

### Invariant sector

If every member has the same canonical carrier image:

```text
factors_through_invariant_carrier
```

### Held sector

If one or more canonical images are unavailable:

```text
carrier_factorization_held
```

### Obstructed sector

If related presentations map to multiple carrier elements:

```text
carrier_factorization_obstructed
```

### Local-only sector

A singleton presentation still has a canonical image:

```text
local_presentation_canonical_image
```

but this alone is not a nontrivial quotient theorem.

## Non-reification

The carrier is not treated as an intrinsic substance.

The relevant statements are only:

```text
same invariant -> same carrier element
different invariant -> distinct carrier element
```

for one chosen invariant projection.

Thus:

```text
carrier element != thing-in-itself
invariant projection != ultimate truth
presentation quotient != metaphysical substance
```

## Validation

The focused checker verifies:

1. GitHub, Vercel, and Supabase presentations with the same invariant all map to one carrier element;
2. the same invariant maps to the same carrier element across different sectors;
3. changing only presentation IDs does not change the carrier ID;
4. changing the invariant projection does change carrier identity;
5. different invariants remain distinct;
6. held invariants produce partial canonical maps;
7. stale v7.7 packet binding fails closed.

The key regression test is:

> **carrier identity must be a function of the invariant, not of the presentation.**
