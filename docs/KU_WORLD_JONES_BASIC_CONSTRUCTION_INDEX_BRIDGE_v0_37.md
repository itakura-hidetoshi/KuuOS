# WORLD Jones Basic Construction, Relative Commutant, and Index Bridge v0.37

v0.37 extends the v0.36 conditional-expectation bridge with the algebraic Jones basic construction and a finite-index package.

```text
N ⊆ A with conditional expectation E_N
  → Jones projection e_N
  → e_N² = e_N and e_N* = e_N
  → e_N a e_N = E_N(a)e_N
  → basic construction ⟨A,e_N⟩
  → relative commutant N′ ∩ A
  → finite quasi-basis
  → central index element
  → scalar Jones index [A:N] ≥ 1
```

Lean directly verifies:

- idempotence and self-adjointness of the Jones projection;
- the compression identity for arbitrary algebra elements;
- the reduced compression identity on the sufficient subalgebra;
- containment of the sufficient subalgebra and Jones projection in the basic construction;
- containment of finite sandwiches `b e_N c`;
- the relative-commutant membership characterization;
- membership of the Jones projection and index element in the relative commutant;
- left and right finite quasi-basis reconstruction;
- the quasi-basis formula for the index element;
- self-adjointness and centrality of the index element;
- scalar realization of the index element;
- positivity of the Jones index and the bundled finite-index package.

Von Neumann closure of the generated basic construction, the Hilbert-space realization of the Jones projection, canonical and Markov traces, Pimsner–Popa finite index, quasi-basis independence of the Watatani index, statistical dimension, finite-dimensionality of the relative commutant, and tower iteration remain explicit analytic proof receipts.

Runtime does not construct the Jones projection, execute the basic construction, claim the finite-index theorem, or update WORLD.
