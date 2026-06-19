# WORLD Conditional Expectation, Sufficient Subalgebra, and Takesaki Bridge v0.36

v0.36 extends the v0.35 Petz-recovery bridge with a sufficient subalgebra and a state-pair preserving conditional expectation.

```text
sufficient subalgebra N ⊆ A
  → conditional expectation E_N : A → A
  → E_N(A) ⊆ N and E_N|_N = id
  → E_N² = E_N
  → fixed points = image = N
  → N-bimodule law
  → state-pair preservation
  → recovered channel = E_N
  → modular invariance σ_t(N) ⊆ N
```

Lean directly verifies:

- range containment in the sufficient subalgebra;
- pointwise fixation of the sufficient subalgebra;
- idempotence of the conditional expectation;
- fixed-point and image characterizations of the subalgebra;
- star closure and star preservation;
- left, right, and two-sided bimodule laws;
- exact preservation of the reference and comparison states;
- identification of the v0.35 coarse channel with the conditional expectation;
- identification of the Petz recovered channel with the conditional expectation;
- fixation of sufficient-subalgebra elements by the recovered channel;
- relative-entropy equality inherited from v0.35;
- modular-flow invariance of the sufficient subalgebra.

Positivity, complete positivity, normality, weak closedness, faithfulness and normality of the reference state, the Takesaki equivalence, uniqueness of the state-preserving expectation, and entropy-equality iff sufficiency remain explicit analytic proof receipts.

Runtime does not construct the conditional expectation, claim the Takesaki theorem, claim the sufficient-subalgebra theorem, or update WORLD.
