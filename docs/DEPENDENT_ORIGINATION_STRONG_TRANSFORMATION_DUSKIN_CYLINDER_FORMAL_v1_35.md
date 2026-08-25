# Dependent Origination — Strong-Transformation Duskin Cylinder v1.35

## Mathematical unit

This layer treats the passage from bicategorical strong equivalence to a global
Duskin prism as one construction rather than a sequence of hornwise choices.

For normal lax functors `P,Q : B -> C`, a certified cylinder

```text
B × [1] -> C
```

is evaluated on a Duskin simplex `σ : [n] -> B` and an interval simplex
`t : [n] -> [1]`.  Pairing `σ` and `t`, then postcomposing with the cylinder,
produces a mixed Duskin `n`-simplex in `C`.

The construction proves at once:

- reindexing compatibility in every simplicial degree;
- assembly of the mixed simplices into a map `N(B) × Δ[1] -> N(C)`;
- the two endpoint equations;
- hence a native pinned-Mathlib `SSet.Homotopy`.

## Native strong-transformation boundary

The v1.32 oplax-strong round-trip transformations

```text
G F ==> id_B
F G ==> id_C
```

are promoted exactly to Mathlib `Pseudofunctor.StrongTrans` values.

After v1.35 the remaining prism problem is entirely bicategorical:

```text
Pseudofunctor.StrongTrans P Q
  -> normal-lax cylinder B × [1] -> C.
```

Once that standard uncurrying is supplied, the global Duskin prism and all
hornwise homotopies follow automatically from theorem-level code.

## Rectification boundary

`ScaledHornHomotopyRectification` is intentionally not discharged here.
A simplicial homotopy between a boundary and a prescribed horn map does not in
general imply a strict filler with literal boundary equality.  Treating such a
rectification as automatic would risk a circular fibrancy argument.

Accordingly the presentation-independent spine now separates cleanly into:

1. bicategorical strong transformation -> normal-lax cylinder;
2. normal-lax cylinder -> global Duskin prism (v1.35, theorem-level);
3. global prism -> hornwise homotopies (v1.34, theorem-level);
4. homotopy filler -> strict filler only under an explicit rectification/lifting
   theorem (v1.33).
