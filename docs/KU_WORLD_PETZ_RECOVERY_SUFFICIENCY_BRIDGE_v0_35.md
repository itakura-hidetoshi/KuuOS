# WORLD Petz Recovery, Sufficiency, and Equality-Case Bridge v0.35

v0.35 extends the v0.34 Araki-relative-entropy bridge with a coarse channel, a Petz recovery map, exact recovery of the distinguished state pair, and the equality case of data processing.

```text
normal UCP channel Φ
  → Petz recovery R_Petz
  → recovered channel Q = R_Petz ∘ Φ
  → exact recovery of φ and ψ
  → Q² = Q from the channel-range projection law
  → S(ψ∘Φ || φ∘Φ) = S(ψ || φ)
```

Lean directly verifies:

- unitality of `Q` from unitality of `Φ` and `R_Petz`;
- exact recovery of the reference and comparison states;
- sufficiency of the recovered channel for the distinguished state pair;
- the channel-range projection law `Φ(R_Petz(Φ(a))) = Φ(a)`;
- idempotence `Q(Q(a)) = Q(a)`;
- preservation of every local weak closure by `Φ`, `R_Petz`, and `Q`;
- the data-processing bound;
- the reverse bound supplied by the equality witness;
- the exact relative-entropy equality package.

Normality, positivity, and complete positivity of the channel and recovery map, the analytic Petz formula, equality iff recovery, sufficiency iff recovery, modular intertwining, and uniqueness on the relevant support remain explicit proof receipts.

Runtime does not construct the normal UCP channel or Petz map, claim the equality/sufficiency theorem, or update WORLD.
