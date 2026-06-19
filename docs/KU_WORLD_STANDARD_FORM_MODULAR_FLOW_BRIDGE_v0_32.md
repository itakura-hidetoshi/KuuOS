# WORLD Standard Form and Modular Flow Bridge v0.32

v0.32 extends the v0.31 local von Neumann bicommutant net with an abstract standard-form Hilbert carrier and modular dynamics.

```text
local von Neumann carrier M(O)
  → faithful star representation on a complex Hilbert space H
  → cyclic and separating vector Ω
  → Tomita operator receipt
  → polar decomposition receipt S = J Δ^(1/2)
  → modular conjugation J
  → modular flow σ_t
  → modular unitary implementation U_t
```

Lean directly verifies:

- `J² = 1` and norm preservation;
- conjugate-linearity data for `J`;
- pointwise fixing of the natural cone;
- involutivity of the algebraic commutant transport;
- `σ_0 = id`;
- `σ_(s+t) = σ_s ∘ σ_t`;
- `σ_t⁻¹ = σ_(-t)`;
- preservation of multiplication and star;
- invariance of each local weak closure under `σ_t`;
- `U_(s+t) = U_s U_t` and norm preservation;
- covariance `U_t π(a) = π(σ_t(a)) U_t`;
- invariance of the natural cone under `U_t`.

The analytic claims that the Tomita operator is closable, admits the required polar decomposition, has a positive self-adjoint modular operator, and yields a standard form are supplied as proof receipts. Runtime does not construct or execute these unbounded operators and does not claim the standard-form theorem.

WORLD remains distinct from the standard-form Hilbert carrier. Multi-world noncollapse and the two-truths gap remain explicit.
