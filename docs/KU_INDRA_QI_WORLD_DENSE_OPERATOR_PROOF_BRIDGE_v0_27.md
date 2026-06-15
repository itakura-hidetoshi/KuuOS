# Kū–Indra WORLD Dense Operator Formal Bridge v0.27

v0.27 connects the exact v0.26 real-ℓ² analytic state to a typed Lean interface for a dense domain, symmetric core, closability, a closed realization certificate, a global Rayleigh lower bound, and a spectral lower-bound certificate.

Runtime validates module identity and obligation completeness. It does not establish a concrete unbounded-operator theorem. A concrete model must instantiate the Lean structure and supply every certificate.

## Formal instance order

```text
NormedAddCommGroup H
InnerProductSpace ℝ H
CompleteSpace H
```

## Bound theorem interface

```text
worldL2DenseCore_dense
worldL2Diagonal_symmetric
worldL2Diagonal_closable_obligation
worldL2Diagonal_realization_obligation
worldL2Rayleigh_global_lower_bound
worldL2Spectrum_lower_bound_obligation
```

WORLD is not identified with the Hilbert carrier. The observation map may remain nonlinear, noninjective, and nonsurjective. The bridge grants no operator execution, WORLD update, external actuation, or truth authority.
