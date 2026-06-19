# WORLD Noncommutative Operator-Algebra Module v0.29

v0.29 extends the WORLD analytic spine from a single dense self-adjoint operator receipt to a genuinely noncommutative observable algebra and relation bimodules.

```text
WORLD state
  → faithful global observable algebra A_world ⊂ End(H)
  → local observable algebras A_i
  → relation bimodules  _{A_i}E_{ij}_{A_j}
  → background algebra A_bg
  → action algebra A_act
```

The noncommutative content is not represented by a label alone. For witnesses `a b` with `ab ≠ ba`, the commutators `ab - ba` generate a nonzero real submodule

```text
[A,A]_ℝ = span_ℝ {ab - ba}
```

and faithfulness proves that its represented image in `Module.End ℝ H` is also nonzero.

Relations are encoded by commuting left and right representations

```text
L : A_i →ₐ[ℝ] End_ℝ(E_ij)
R : A_jᵐᵒᵖ →ₐ[ℝ] End_ℝ(E_ij)
L(a)(R(b)x) = R(b)(L(a)x).
```

This preserves directionality and prevents a relation from being collapsed into an attribute of either endpoint.

The extension preserves the existing boundaries:

- WORLD is not identified with the Hilbert or operator carrier;
- relation is not reduced to object attributes;
- multi-world noncollapse and the two-truths gap remain explicit;
- runtime does not execute an unbounded operator or claim the Lean proof.
