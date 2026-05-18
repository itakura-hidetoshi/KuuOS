# Physical Quantum Qi Ward/Leak Identity v0.2B

This addendum physicalizes the Ward/leak identity used by Physical Quantum Qi v0.2.  The goal is to make `J_Qi`, `D_mu J^mu`, the leak term, and anomaly/residue terms explicit physical objects rather than audit labels.

This is an equation-level tightening. It grants no proof, ontology, clinical, execution, commit, belief-root commit, memory-overwrite, world-root-rewrite, truth, or safety-override authority.

---

## B1. Qi current as gauge-response current

Let the effective Qi action be

```math
S_{\mathrm{eff}}
=
S_{\mathrm{sys}}[q;A]
+S_{\mathrm{IF}}[q_+,q_-;A]
+S_{\partial}^{\mathrm{Qi}}[X,B,A,\delta_{\mathrm{rel}}]
+S_{\mathrm{YM}}[A]
+S_{\mathrm{rel}}[\delta,A].
```

The Qi current is defined by variation with respect to the IndraNet gauge connection:

```math
J_{\mathrm{Qi}}^\mu(x)
=
\frac{1}{\sqrt{|g|}}\frac{\delta S_{\mathrm{eff}}}{\delta A_\mu(x)}.
```

In closed-time-path form, the physical current is the branch-antisymmetric source response evaluated at equal sources:

```math
\langle J_{\mathrm{Qi}}^\mu(x)\rangle
=
\left.\frac{1}{i\sqrt{|g|}}
\frac{\delta \log Z_{\mathrm{Qi}}[J_+,J_-;A]}{\delta A_{\Delta\mu}(x)}\right|_{A_+=A_-=A}.
```

where

```math
A_{\Delta\mu}=A_{+\mu}-A_{-\mu},
\qquad
A_{\Sigma\mu}=\frac{A_{+\mu}+A_{-\mu}}2.
```

This definition prevents `J_Qi` from becoming an arbitrary named flow. If no action or generating functional variation is declared, there is no physical `J_Qi` claim.

Required fields:

```text
S_eff_declared
A_mu_variation_declared
metric_density_factor_declared
CTP_branch_current_declared
current_domain_declared
```

Rejected claims:

```text
J_Qi_named_without_variation
flow_label_without_action
current_without_domain
```

---

## B2. Current decomposition

The current decomposes according to the part of the action that responds to `A_mu`:

```math
J_{\mathrm{Qi}}^\mu
=J_{\mathrm{sys}}^\mu
+J_{\partial}^\mu
+J_{\mathrm{rel}}^\mu
+J_{\mathrm{IF}}^\mu
+J_{\mathrm{YM}}^\mu.
```

The boundary current is

```math
J_{\partial}^\mu(x)
=
\int_{\partial\Sigma}
\chi(\delta_{\mathrm{rel}})
\partial_\tau X^\mu(\tau)
\delta^{(d)}(x-X(\tau))\,d\tau.
```

The relation-difference current is

```math
J_{\mathrm{rel}}^\mu
=\frac{1}{\sqrt{|g|}}\frac{\delta S_{\mathrm{rel}}}{\delta A_\mu}
\sim
G^{ij}(\theta)\delta_jD^\mu\delta_i.
```

The open-system influence current is

```math
J_{\mathrm{IF}}^\mu
=\frac{1}{\sqrt{|g|}}\frac{\delta S_{\mathrm{IF}}}{\delta A_\mu}.
```

`J_IF` is where environment-induced memory, dissipation, noise, and backaction enter the current balance. Erasing `J_IF` while retaining SK/FV language is invalid.

Required fields:

```text
J_boundary_declared
J_rel_declared
J_IF_declared
open_system_current_component_declared
```

Rejected claims:

```text
current_decomposition_missing
open_system_current_erased
boundary_current_erased
```

---

## B3. Covariant divergence and closed Ward identity

The gauge-covariant divergence is

```math
D_\mu J^\mu
=
\nabla_\mu J^\mu+[A_\mu,J^\mu].
```

For a closed, gauge-invariant Qi sector, infinitesimal gauge variation gives the Ward identity:

```math
D_\mu J_{\mathrm{Qi}}^\mu=0.
```

This is valid only when all of the following hold:

```text
closed_sector
no_trace_out_environment
no_boundary_flux
no_anomaly
gauge_variation_invariant
```

A closed conservation claim is rejected if the packet also declares open-system tracing, unresolved boundary flux, or anomaly residue.

---

## B4. Open Ward/leak identity

For open systems, the covariant divergence is not forced to vanish. It splits into accounted leak and anomaly/residue:

```math
D_\mu J_{\mathrm{Qi}}^\mu
=\mathcal L_{\mathrm{leak}}
+\mathcal A_{\mathrm{anom}}
+\mathcal R_{\mathrm{res}}.
```

Equivalently, the validated open Ward/leak residual is

```math
\mathcal W_{\mathrm{leak}}
=
D_\mu J_{\mathrm{Qi}}^\mu
-\mathcal L_{\mathrm{leak}}
-\mathcal A_{\mathrm{anom}}
-\mathcal R_{\mathrm{res}}.
```

The open identity closes only when

```math
\mathcal W_{\mathrm{leak}}=0
```

within the declared tolerance.

If `W_leak` is nonzero, the packet may remain an observation or repair candidate, but it cannot claim closed `PhysicalQi` or `FullPathQi`.

Required fields:

```text
open_or_closed_case_declared
D_mu_J_declared
L_leak_declared
A_anom_declared_or_zero
R_res_declared_or_zero
W_leak_residual_declared
W_leak_tolerance_declared
```

Rejected claims:

```text
open_system_claim_without_leak_term
leak_residual_hidden
closed_conservation_claim_with_open_trace
```

---

## B5. Physical meaning of the leak term

The leak term is not a moral or audit failure. It is the physically accounted current leaving or entering the chosen Qi subsystem because the subsystem boundary is open.

It can contain:

```math
\mathcal L_{\mathrm{leak}}
=\mathcal L_{\mathrm{env}}
+\mathcal L_{\partial B}
+\mathcal L_{\mathrm{membrane}}
+\mathcal L_{\mathrm{coarse}}
+\mathcal L_{\mathrm{measure}}.
```

where:

- `L_env` is exchange with traced-out environmental degrees of freedom,
- `L_partialB` is flux through brane or membrane boundary,
- `L_membrane` is cross-layer leakage through a KuuOS membrane,
- `L_coarse` is loss induced by coarse-graining / RG projection,
- `L_measure` is measurement or intervention backaction.

A typical boundary flux contribution is

```math
\mathcal L_{\partial B}(x)
=\int_{\partial B} n_\mu J_{\mathrm{Qi}}^\mu\,d\Sigma.
```

A coarse-graining leak can be represented abstractly by

```math
\mathcal L_{\mathrm{coarse}}
=\left(D_\mu J^\mu\right)_{\mathrm{micro}}
-\Pi_{\mathrm{coarse}}\left(D_\mu J^\mu\right)_{\mathrm{micro}}.
```

An intervention backaction leak can be represented by

```math
\mathcal L_{\mathrm{measure}}
=\frac{\delta S_{\mathrm{IF}}^{\mathrm{measure}}}{\delta \alpha_{\mathrm{probe}}}.
```

The core rule is:

```text
leak accounted -> open Ward/leak identity may close
leak hidden -> PhysicalQi / FullPathQi claim blocked
```

---

## B6. Anomaly and residue

The anomaly term is reserved for symmetry-breaking residue that cannot be treated as ordinary boundary leak:

```math
\mathcal A_{\mathrm{anom}}
=\mathcal A_{\mathrm{gauge}}
+\mathcal A_{\mathrm{measure}}
+\mathcal A_{\mathrm{regularization}}
+\mathcal A_{\mathrm{topological}}.
```

The residual term captures known but not-yet-closed mismatch:

```math
\mathcal R_{\mathrm{res}}
=\mathcal R_{\mathrm{holonomy}}
+\mathcal R_{\mathrm{translation}}
+\mathcal R_{\mathrm{scope}}
+\mathcal R_{\mathrm{kernel}}.
```

`A_anom` and `R_res` must be either explicitly zero or explicitly bounded. They must not be hidden inside `L_leak` if their physical origin is symmetry-breaking or unresolved mismatch.

Required fields:

```text
anomaly_origin_declared_or_zero
residue_origin_declared_or_zero
anomaly_bound_declared_if_nonzero
residue_bound_declared_if_nonzero
```

Rejected claims:

```text
anomaly_erasure
residue_erasure
symmetry_break_hidden_as_leak
```

---

## B7. Runtime consequence

`PhysicalQi` requires either:

```text
closed Ward identity: D_mu J_Qi^mu = 0
```

or:

```text
open Ward/leak identity: D_mu J_Qi^mu - L_leak - A_anom - R_res = 0
```

with all terms declared and tolerance-bound.

`FullPathQi` further requires the SK/FV v0.2A conditions. Therefore:

```text
J_Qi without action variation -> reject
D_mu J without open/closed case -> hold or reject
open trace without leak term -> reject
nonzero W_leak residual -> cannot certify PhysicalQi / FullPathQi
anomaly hidden as ordinary leak -> reject
```
