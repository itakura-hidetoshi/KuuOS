# Physical Quantum Qi SK/FV Action v0.2A

This addendum deepens the SK/FV part of Physical Quantum Qi v0.2.  It defines the concrete system action, influence-kernel conditions, fluctuation-dissipation relation, and Markov / non-Markov boundary.

This is equation-level content, not a new authority surface.  It grants no proof, ontology, clinical, execution, commit, belief-root commit, memory-overwrite, world-root-rewrite, truth, or safety-override authority.

---

## A1. Concrete system action `S_sys`

The internal Qi system is treated as a gauge-covariant open-history degree of freedom `q(t)` or field `q(x)`.  The minimal finite-dimensional action is:

```math
S_{\mathrm{sys}}[q;A]
=
\int_0^T dt
\left[
\frac12 g_{ij}(q,\theta)D_tq^iD_tq^j
- V_{\mathrm{Qi}}(q,\theta)
+ a_i(q,\theta)\dot q^i
\right]
+S_{\mathrm{geom}}[q,\theta].
```

The covariant time derivative is:

```math
D_tq^i = \dot q^i + (A_t)^i{}_j q^j.
```

The Qi potential decomposes as:

```math
V_{\mathrm{Qi}}(q,\theta)
=V_{\mathrm{rel}}(q)+V_{\mathrm{phase}}(q;\theta)+V_{\mathrm{barrier}}(q;\Delta_{\mathrm{gap}}).
```

The barrier component must not be interpreted as a Qi source.  It is a stability floor on admissible `K_perp` histories:

```math
V_{\mathrm{barrier}}(q;\Delta_{\mathrm{gap}})
\ge
\frac12\Delta_{\mathrm{gap}}\|\Pi_\perp q\|^2,
\qquad
\Delta_{\mathrm{gap}}\ge\frac{33}{20}
```

when MGAP4D internal normalized units are invoked.

The field version is:

```math
S_{\mathrm{sys}}[q;A]
=
\int_{\mathcal M} d^dx\sqrt{|g|}
\left[
\frac12G_{ij}(q,\theta)D_\mu q^iD^\mu q^j
-V_{\mathrm{Qi}}(q,\theta)
\right]
+
\int_{\mathcal M} q^*\omega_{\mathrm{Qi}}.
```

The term `q^* omega_Qi` records geometric / Berry-like operation-order residue.  If this history-sensitive term is erased, the object may still be a reduced `PhysicalQi` candidate, but it cannot certify `FullPathQi`.

Required `S_sys` fields:

```text
kinetic_metric_declared
covariant_derivative_declared
potential_decomposition_declared
barrier_floor_declared
barrier_not_qi_source_declared
geometric_history_term_declared
```

Rejected claims:

```text
S_sys_without_covariant_derivative
barrier_claimed_as_qi_source
operation_order_geometry_erased
```

---

## A2. Influence action and kernel conditions

The SK/FV influence action is:

```math
S_{\mathrm{IF}}[q_+,q_-]
=
\int_0^Tdt\int_0^Tdt'\,
\Delta q(t)D_R(t,t')\Sigma q(t')
+
\frac{i}{2}\int_0^Tdt\int_0^Tdt'\,
\Delta q(t)N(t,t')\Delta q(t').
```

with

```math
\Delta q(t)=q_+(t)-q_-(t),
\qquad
\Sigma q(t)=\frac{q_+(t)+q_-(t)}2.
```

The required kernel conditions are:

### Causality

```math
D_R(t,t')=0\quad\text{for}\quad t<t'.
```

### Noise symmetry

```math
N(t,t')=N(t',t).
```

### Positive semidefinite noise

```math
\int dt\,dt'\,f(t)N(t,t')f(t')\ge0
```

for all real test functions `f` in the declared domain.

### Spectral consistency

```math
D_R(t,t')-D_A(t,t')=D_\rho(t,t'),
\qquad
D_A(t,t')=D_R(t',t).
```

### Closed-time-path normalization

```math
S_{\mathrm{IF}}[q,q]=0,
\qquad
Z_{\mathrm{Qi}}[J,J]=1
```

unless an explicit postselection or leak-conditioned normalization is declared.

Required `S_IF` kernel fields:

```text
D_R_causal
N_symmetric
N_positive_semidefinite
spectral_consistency_declared
SK_normalization_declared
leak_or_postselection_normalization_declared_if_used
```

Rejected claims:

```text
kernel_without_causality
noise_without_positive_semidefinite_condition
spectral_kernel_erasure
SK_normalization_missing
```

---

## A3. Fluctuation-dissipation relation

For stationary thermal environments at inverse temperature `beta`, the frequency-domain relation is:

```math
N(\omega)
=
\coth\left(\frac{\beta\omega}{2}\right)\operatorname{Im}D_R(\omega).
```

If the convention uses the spectral kernel `D_rho`, the equivalent declaration is:

```math
N(\omega)
=\frac12\coth\left(\frac{\beta\omega}{2}\right)D_\rho(\omega).
```

The packet must declare which convention is used.

For non-equilibrium or non-stationary environments, strict thermal FDR is replaced by a bounded residual:

```math
\mathcal R_{\mathrm{FDR}}(\omega)
=
N(\omega)
-
\coth\left(\frac{\beta_{\mathrm{eff}}(\omega)\omega}{2}\right)
\operatorname{Im}D_R(\omega).
```

The rule is:

```text
if thermal_stationary_environment:
    require FDR_residual_zero_or_within_tolerance
else:
    require FDR_residual_declared_and_bounded
```

Required FDR fields:

```text
environment_stationarity_declared
thermal_or_nonequilibrium_declared
FDR_convention_declared
FDR_residual_status_declared
FDR_residual_bound_declared_if_nonequilibrium
```

Rejected claims:

```text
thermal_noise_claim_without_FDR
FDR_violation_hidden_as_noise
nonequilibrium_environment_without_residual_bound
```

---

## A4. Markov / non-Markov boundary

A Markov approximation is valid only when the memory kernel is effectively local:

```math
D_R(t,t')\approx 2\gamma\partial_t\delta(t-t'),
\qquad
N(t,t')\approx 2\gamma T\delta(t-t').
```

More generally, define memory time:

```math
\tau_{\mathrm{mem}}
=
\frac{\int_0^\infty d\tau\,\tau\|D_R(\tau)\|}
{\int_0^\infty d\tau\,\|D_R(\tau)\|}.
```

The Markov reduction is admissible only if:

```math
\tau_{\mathrm{mem}}/\tau_{\mathrm{sys}} < \varepsilon_{\mathrm{M}}.
```

The non-Markov regime is required if:

```math
\tau_{\mathrm{mem}}/\tau_{\mathrm{sys}}\ge\varepsilon_{\mathrm{NM}}
```

or if operation-order residue is non-negligible:

```math
\left\|\mathcal T[\mathcal O_1\mathcal O_2]
-\mathcal T[\mathcal O_2\mathcal O_1]\right\|>\varepsilon_{\mathrm{ord}}.
```

A Markov-reduced object cannot certify `FullPathQi` unless the reduction receipt preserves:

```text
original_kernel_digest
memory_time_bound
operation_order_residue
FDR_status
lost_history_terms
```

Required boundary fields:

```text
memory_time_declared
system_time_declared
markov_threshold_declared
nonmarkov_threshold_declared
operation_order_residue_declared
markov_reduction_receipt_declared_if_used
```

Rejected claims:

```text
Markov_snapshot_claimed_as_FullPathQi
nonMarkov_history_reduced_without_receipt
operation_order_erasure
```

---

## A5. Runtime consequence

`FullPathQi` requires all of:

```text
S_sys_concrete_form
S_IF_kernel_conditions
FDR_status
Markov_nonMarkov_boundary
SK_plus_branch
SK_minus_branch
FV_influence_functional
memory_kernel
noise_kernel
observation_backaction
noncommutative_operation_history
path_measure_normalization
boundary_conditions
leak_identity_on_paths
```

If any A-field is missing, the result may remain `PhysicalQi` or lower, but must not be promoted to `FullPathQi`.
