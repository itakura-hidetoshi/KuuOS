# WORLD Araki Relative Entropy Bridge v0.34

v0.34 extends the v0.33 modular-state and relative-flow bridge with extended-nonnegative Araki relative entropy, local restriction monotonicity, and a three-state Connes cocycle chain rule.

```text
reference state φ, comparison state ψ, third state χ
  → local relative entropy S_O(ψ || φ) ∈ [0,∞]
  → global relative entropy S(ψ || φ)
  → O₁ ≤ O₂ implies S_O₁(ψ || φ) ≤ S_O₂(ψ || φ)
  → [Dχ:Dφ]_t = [Dχ:Dψ]_t [Dψ:Dφ]_t
```

Lean directly verifies:

- nonnegativity of local and global entropy values by the order structure of `ℝ≥0∞`;
- local entropy bounded by the global entropy;
- local data processing along WORLD-region inclusions;
- transitive data processing over nested regions;
- equality of local entropy on order-equivalent regions;
- vanishing self-relative entropy;
- the three-state Connes cocycle chain rule;
- reversal of cocycle order after taking adjoints;
- left and right unitarity of the additional pairwise cocycles.

The logarithmic relative modular operator formula, its domain, lower semicontinuity, monotonicity under normal unital completely positive maps, entropy-zero faithfulness, and the Petz equality/recovery theorem remain explicit analytic proof receipts.

Runtime does not construct the relative modular logarithm, compute Araki entropy, claim the normal-UCP theorem, construct a Petz recovery map, or update WORLD.
