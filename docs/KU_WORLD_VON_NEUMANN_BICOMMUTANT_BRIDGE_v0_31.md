# WORLD von Neumann Bicommutant Bridge v0.31

v0.31 extends the v0.30 local C⋆-net with algebraic commutants and bicommutants.

For a set of observables `S ⊆ A`, define

```text
S'  = {x | ∀ s ∈ S, sx = xs}
S'' = (S')'.
```

Lean proves the algebraic spine:

```text
S ⊆ S''
S ⊆ T  →  T' ⊆ S'
S ⊆ T  →  S'' ⊆ T''
S''' = S'
S'''' = S''.
```

For the local net `O ↦ A(O)`, the generated bicommutant carrier is

```text
M(O) = A(O)''.
```

The v0.30 isotony theorem lifts to

```text
O₁ ≤ O₂  →  M(O₁) ⊆ M(O₂).
```

Spacelike locality also survives bicommutant generation. If `O₁` and `O₂` are spacelike, every element of `M(O₁)` commutes with every element of `M(O₂)`.

The analytic identification

```text
weak-operator-closure(A(O)) = A(O)''
```

is not manufactured by runtime. It is represented as an external proof receipt. Runtime does not model the weak operator topology, construct a weak closure, execute unbounded operators, or update WORLD.

WORLD remains distinct from the von Neumann carrier, while multi-world noncollapse and the two-truths gap remain explicit.
