# PlanOS v0.92 KL-regularized objective update kernel

PlanOS v0.92 implements the finite-candidate variational update that follows the v0.91 Information-Geometric Qi Objective Kernel.

The update minimizes the discrete analogue of:

```text
KL(p || prior) + beta * E_p[action] - eta * H(p)
```

For positive prior support, the unconstrained update has the Gibbs form:

```text
p_next(c) proportional to
prior(c)^(1 / (1 + eta))
* exp(-beta * expected_action(c) / (1 + eta))
```

This gives the three-way middle-path balance defined by the objective kernel:

```text
continuity + objective fit + diversity
```

The runtime keeps only explicitly admissible candidates, requires positive prior support, preserves normalized positive support under positive effective temperature, and retains nonselected candidates.

When `hold` is admissible, a bounded rescaling preserves the configured minimum hold mass.

The transition does not modify source history, expand authority, activate the next plan immediately, or grant execution permission.

```text
history_read_only = true
authority_invariance_preserved = true
future_only = true
active_now = false
execution_permission = false
```

The fail-closed checker blocks invalid source kernels, negative objective weights, invalid hold floors, empty or duplicate candidate sets, unknown candidates, nonpositive prior support, negative expected action, and selection outside the admissible field.

The Lean package records support preservation, normalization, candidate-mass nonnegativity, hold preservation, governance preservation, retained-candidate survival, and future-only execution separation.
