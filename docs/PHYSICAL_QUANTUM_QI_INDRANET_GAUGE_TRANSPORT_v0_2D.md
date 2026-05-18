# Physical Quantum Qi IndraNet Gauge Transport v0.2D

This addendum geometrizes IndraNet transport for Physical Quantum Qi v0.2.  IndraNet is not a graph-only relation model. It is a gauge-transport geometry with a connection, curvature, parallel transport, holonomy/Wilson loop, and explicit scope drift / residue accounting.

This is an equation-level and geometry-target tightening. It grants no proof, ontology, clinical, execution, commit, belief-root commit, memory-overwrite, world-root-rewrite, truth, or safety-override authority.

---

## D1. IndraNet gauge bundle and connection `A_mu`

Let `M_scope` be a declared local scope manifold or site chart for the Qi/IndraNet transport problem.  Let `E -> M_scope` be a vector bundle, principal bundle, or sheaf-compatible transport bundle carrying local Qi/current states.

The IndraNet gauge connection is

```math
A = A_\mu dx^\mu,
\qquad
A_\mu(x) \in \mathfrak g.
```

For a local section `s`, the covariant derivative is

```math
D_\mu s = \partial_\mu s + A_\mu s.
```

For adjoint-valued currents,

```math
D_\mu J^\mu = \nabla_\mu J^\mu + [A_\mu,J^\mu].
```

`A_mu` is the minimal geometric datum required for IndraNet transport.  A graph edge without `A_mu` is not IndraNet gauge transport.

Required fields:

```text
scope_manifold_or_site_declared
bundle_E_declared
gauge_group_or_algebra_declared
A_mu_declared
covariant_derivative_declared
current_representation_declared
```

Rejected claims:

```text
graph_edge_claimed_as_gauge_transport
transport_without_connection
current_transport_without_representation
```

---

## D2. Curvature `F_munu`

The curvature of the IndraNet connection is

```math
F_{\mu\nu}
=
\partial_\mu A_\nu
-
\partial_\nu A_\mu
+[A_\mu,A_\nu].
```

Equivalently,

```math
F=dA + A\wedge A.
```

Curvature measures noncommutative path-dependence.  If

```math
F_{\mu\nu}=0
```

on a simply connected patch, transport is locally flat.  If `F_munu` is nonzero, different paths may yield different transported Qi/current states.

Required fields:

```text
F_munu_defined
curvature_domain_declared
noncommutative_term_declared
flatness_status_declared
curvature_visibility_declared
```

Rejected claims:

```text
path_independence_claim_with_nonzero_curvature
curvature_erasure
flat_transport_claim_without_flatness_status
```

---

## D3. Path-ordered transport `U_gamma`

For a path

```math
\gamma:[0,1]\to M_{\mathrm{scope}},
```

IndraNet parallel transport is

```math
U_\gamma
=\mathcal P\exp\left(-\int_\gamma A_\mu dx^\mu\right).
```

A local state or current is transported by

```math
s(\gamma(1)) = U_\gamma s(\gamma(0)).
```

or, in the appropriate representation,

```math
J(\gamma(1)) = \mathrm{Ad}_{U_\gamma}J(\gamma(0)).
```

`U_gamma` is path-dependent unless curvature/holonomy conditions remove the dependence.  Therefore transport claims must declare the path or path family.

Required fields:

```text
path_gamma_declared
path_ordering_declared
U_gamma_defined
transport_representation_declared
path_family_or_single_path_declared
```

Rejected claims:

```text
transport_without_path
path_order_erasure
path_independence_without_flatness_or_holonomy_bound
```

---

## D4. Wilson loop / holonomy `W(C)`

For a closed loop `C`, the holonomy is

```math
U_C=\mathcal P\exp\left(-\oint_C A\right).
```

The Wilson loop is

```math
W(C)=\operatorname{Tr}\,\mathcal P\exp\left(-\oint_C A\right).
```

`W(C)` records whether transport around a closed loop returns to the same gauge state or carries residual twist.  In an IndraNet setting, this is the correct replacement for naive cyclic graph consistency.

A holonomy residue can be defined by

```math
\mathcal R_{\mathrm{hol}}(C)
=\|U_C-I\|.
```

or by a trace-normalized Wilson mismatch:

```math
\mathcal R_W(C)
=\left|\frac{1}{d}\operatorname{Tr}U_C-1\right|.
```

Required fields:

```text
closed_loop_C_declared
U_C_defined
W_C_defined
holonomy_residue_declared
holonomy_tolerance_declared
```

Rejected claims:

```text
cycle_consistency_without_holonomy
Wilson_loop_erasure
holonomy_residue_hidden
```

---

## D5. Scope drift

Transport is always scoped.  Let `S_0` be the source scope and `S_1` the target scope.  Let `Phi_gamma` be the transport-induced scope map.

Scope drift is the mismatch between intended and transported scope:

```math
\Delta_{\mathrm{scope}}(\gamma)
=d_{\mathrm{scope}}\left(\Phi_\gamma(S_0),S_1\right).
```

For sheaf-compatible charts, if `rho_i^j` denotes restriction maps, a local drift can be represented as

```math
\Delta_{\mathrm{scope}}^{ij}
=\|\rho_i^j(s_i)-s_j\|.
```

Scope drift is not a cosmetic metadata difference.  It can invalidate a transport claim when the transported object no longer lives in the declared target scope.

Required fields:

```text
source_scope_declared
target_scope_declared
scope_map_declared
scope_metric_or_mismatch_declared
scope_drift_value_or_bound_declared
scope_drift_tolerance_declared
```

Rejected claims:

```text
scope_free_transport_claim
scope_drift_erasure
transport_to_target_without_scope_compatibility
```

---

## D6. Total transport residue

The total IndraNet transport residue is a vector or bundle of residues:

```math
\mathcal R_{\mathrm{transport}}
=
(\mathcal R_{\mathrm{hol}},
\mathcal R_{\mathrm{curv}},
\mathcal R_{\mathrm{scope}},
\mathcal R_{\mathrm{path}},
\mathcal R_{\mathrm{rep}},
\mathcal R_{\mathrm{boundary}}).
```

A scalar score may be declared only after weights are explicit:

```math
R_{\mathrm{transport}}
=
\alpha_h\mathcal R_{\mathrm{hol}}
+\alpha_c\mathcal R_{\mathrm{curv}}
+\alpha_s\mathcal R_{\mathrm{scope}}
+\alpha_p\mathcal R_{\mathrm{path}}
+\alpha_r\mathcal R_{\mathrm{rep}}
+\alpha_b\mathcal R_{\mathrm{boundary}}.
```

The vector residue is authoritative over the scalar summary.  A small scalar score cannot hide a large component residue.

Required fields:

```text
transport_residue_vector_declared
holonomy_residue_declared
curvature_residue_declared
scope_residue_declared
path_residue_declared
representation_residue_declared
boundary_residue_declared
scalar_residue_weights_declared_if_scalar_used
component_residue_visibility_declared
```

Rejected claims:

```text
residue_scalar_hides_component_failure
holonomy_residue_erasure
scope_residue_erasure
representation_residue_erasure
```

---

## D7. Gauge-transport validity gate

IndraNet gauge transport is valid as a transport candidate only when:

```text
A_mu declared
F_munu declared
path gamma declared
U_gamma declared
scope source/target declared
holonomy or Wilson residue declared
scope drift declared
transport residue visible
```

It is rejected when:

```text
graph-only relation is claimed as IndraNet transport
A_mu is missing
path gamma is missing
F_munu is hidden
scope drift is hidden
holonomy/Wilson residue is hidden
component residue is collapsed into a scalar
```

Even when valid, IndraNet gauge transport is still a routing/evidence surface.  It grants no execution, commit, proof, truth, ontology, clinical, memory-overwrite, or world-root-rewrite authority.

---

## D8. Minimal packet keys

```text
scope_manifold_or_site_declared
bundle_E_declared
gauge_group_or_algebra_declared
A_mu_declared
covariant_derivative_declared
F_munu_defined
curvature_visibility_declared
path_gamma_declared
path_ordering_declared
U_gamma_defined
closed_loop_C_declared
W_C_defined
holonomy_residue_declared
source_scope_declared
target_scope_declared
scope_drift_value_or_bound_declared
transport_residue_vector_declared
component_residue_visibility_declared
graph_only_transport_rejected
nonauthority_boundary_declared
```
