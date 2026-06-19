# WORLD Modular State, KMS Equilibrium, and Relative Modular Flow Bridge v0.33

v0.33 extends the v0.32 standard-form modular-flow bridge with two normalized states, a positive inverse temperature, a KMS strip continuation, a relative modular flow, and a Connes cocycle.

```text
reference state φ and comparison state ψ
  → β-KMS strip continuation F_ab(z)
  → real boundary F_ab(t) = φ(a σ_t(b))
  → imaginary boundary F_ab(t+iβ) = φ(σ_t(b) a)
  → relative modular flow σ_t^(ψ|φ)
  → Connes cocycle u_t = [Dψ:Dφ]_t
```

Lean directly verifies:

- normalization of both states;
- positivity of the inverse temperature;
- modular stationarity of the reference state;
- KMS lower and upper boundary formulas;
- the special identities `F_ab(0) = φ(ab)` and `F_ab(iβ) = φ(ba)`;
- the relative-flow group law and left/right inverse laws;
- comparison-state stationarity under the relative flow;
- the Connes cocycle identity `u_(s+t) = u_s σ_s(u_t)`;
- twisted inverse identities obtained from the cocycle law;
- left and right unitarity of `u_t`;
- cocycle implementation `σ_t^(ψ|φ)(a) = u_t σ_t(a) u_t*`;
- multiplication, star, and local weak-closure preservation.

Normality, faithfulness, positivity of the state functionals, strip analyticity and boundedness, relative Tomita closability, relative polar decomposition, positive self-adjointness of the relative modular operator, and the Connes Radon–Nikodym theorem remain explicit proof receipts.

Runtime does not construct the analytic continuation, relative Tomita operator, or relative modular operator, and does not claim the Connes theorem or update WORLD.
