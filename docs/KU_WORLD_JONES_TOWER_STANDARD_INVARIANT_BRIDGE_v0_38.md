# WORLD Jones Tower, Temperley–Lieb, and Standard Invariant Bridge v0.38

v0.38 extends the v0.37 Jones basic-construction bridge with a typed finite-stage Jones tower, a sequence of Jones projections, Temperley–Lieb relations, and lower/upper relative-commutant filtrations.

```text
N ⊆ M ⊆ M₁ ⊆ M₂ ⊆ ⋯
  → Jones projections e₀,e₁,e₂,…
  → eₙ² = eₙ and eₙ* = eₙ
  → eₙeₙ₊₁eₙ = [M:N]⁻¹eₙ
  → distant projections commute
  → N′ ∩ Mₙ and M′ ∩ Mₙ
  → standard invariant
  → principal graph / planar algebra receipts
```

Lean directly verifies:

- the stage-zero and stage-one identifications;
- monotonicity of the tower algebras;
- self-adjoint idempotence of every Jones projection;
- placement of `eₙ` in stage `n + 2` and every later stage;
- identification of `e₀` with the v0.37 Jones projection;
- both adjacent Temperley–Lieb triple-product relations;
- commutation of sufficiently separated Jones projections;
- membership of each Jones projection in the lower relative commutant at stage `n + 2`;
- nesting of the lower and upper relative-commutant filtrations;
- explicit lower and upper relative-commutant membership characterizations;
- positivity and nonvanishing of the loop parameter;
- the relation `δ² = [M:N]`;
- the formula identifying the Temperley–Lieb scalar with the inverse Jones index;
- a bundled standard-invariant package.

Recursive von Neumann basic construction at every stage, weak closure, canonical expectation tower, Markov trace extension, index constancy, factoriality, extremality, completeness of the standard invariant, principal-graph reconstruction, finite-depth characterization, and planar-algebra realization remain explicit analytic proof receipts.

Runtime does not construct the Jones tower, execute a Temperley–Lieb algebra, claim standard-invariant completeness, or update WORLD.
