# Physical Quantum Qi Equations v0.2

This document gives the equation-level content for Physical Quantum Qi v0.2.

It is an additive deepening of `Physical Quantum Qi Runtime v0.1`.  The purpose is not to add another audit shell, but to define the physical objects used by the v0.2 modules:

1. SK/FV Qi path integral,
2. Qi current and Ward/leak identity,
3. DPI recoverability margin,
4. IndraNet gauge transport,
5. KuString-Qi emergence from relational difference.

The non-authority boundary remains unchanged: these equations do not grant proof, ontology, clinical, execution, belief-commit, memory-overwrite, world-root-rewrite, or safety-override authority.

---

## 1. SK/FV Qi path integral

Qi is not a one-time snapshot.  It is a history-sensitive open-system path surface.

The v0.2 generating functional is

```math
Z_{\mathrm{Qi}}[J_+,J_-]
=
\int \mathcal D q_+\,\mathcal D q_-
\exp\left\{
 iS_{\mathrm{sys}}[q_+]
-iS_{\mathrm{sys}}[q_-]
+iS_{\mathrm{IF}}[q_+,q_-]
+i\int_0^T (J_+(t)q_+(t)-J_-(t)q_-(t))\,dt
\right\}.
```

Here:

- `q_+` is the forward branch,
- `q_-` is the backward branch,
- `J_+`, `J_-` are source terms for observation or intervention,
- `S_sys` is the effective internal Qi-system action,
- `S_IF` is the Feynman-Vernon influence action.

Define

```math
\Delta q(t)=q_+(t)-q_-(t),
\qquad
\Sigma q(t)=\frac{q_+(t)+q_-(t)}{2}.
```

The influence action is represented by

```math
S_{\mathrm{IF}}[q_+,q_-]
=
\int_0^T\!dt\int_0^T\!dt'\,
\Delta q(t)D_R(t,t')\Sigma q(t')
+
\frac{i}{2}
\int_0^T\!dt\int_0^T\!dt'\,
\Delta q(t)N(t,t')\Delta q(t').
```

where:

- `D_R(t,t')` is the memory/dissipation kernel,
- `N(t,t')` is the noise kernel,
- the real part carries response and memory,
- the imaginary part carries decoherence and fluctuation cost.

The minimum SK/FV evidence required for `FullPathQi` is:

```text
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

The following is rejected:

```text
Markov_snapshot_claimed_as_FullPathQi
path_integral_without_history
operation_order_erasure
```

---

## 2. Qi current and Ward/leak identity

Qi current is not asserted by naming a flow.  It is defined as a response to a gauge connection.

Let `A_mu` be the IndraNet gauge connection.  The Qi current is

```math
J^\mu_{\mathrm{Qi}}(x)
=
\frac{\delta S_{\mathrm{Qi}}}{\delta A_\mu(x)}.
```

Equivalently, at the generating functional level,

```math
\langle J^\mu_{\mathrm{Qi}}(x)\rangle
=
\frac{1}{i}\frac{\delta \log Z_{\mathrm{Qi}}}{\delta A_\mu(x)}.
```

The covariant derivative is

```math
D_\mu = \partial_\mu + [A_\mu,\cdot].
```

Closed case:

```math
D_\mu\langle J^\mu_{\mathrm{Qi}}\rangle=0.
```

Open case:

```math
D_\mu\langle J^\mu_{\mathrm{Qi}}\rangle
=
\langle\mathcal L_{\mathrm{leak}}\rangle
+
\mathcal A_{\mathrm{anom}}.
```

where:

- `L_leak` records open-system leakage,
- `A_anom` records anomaly or symmetry-break residue,
- both must be declared or explicitly zeroed.

The following is rejected:

```text
flow_without_conservation_or_leak
current_without_domain
anomaly_erasure
```

---

## 3. DPI recoverability margin

Recoverability is a quantitative margin, not a label.

For two states `rho`, `sigma` and a channel `E`, define the DPI gap:

```math
\Delta_{\mathrm{DPI}}
=
D(\rho\Vert\sigma)
-
D(\mathcal E(\rho)\Vert\mathcal E(\sigma)).
```

The Qi recovery score is

```math
\mathcal R_{\mathrm{Qi}}
=
\exp(-\Delta_{\mathrm{DPI}}).
```

The irreversibility burden is

```math
\eta_{\mathrm{Qi}}
=
\Delta_{\mathrm{DPI}}
+
\Sigma
+
C_{\mathrm{lockin}}.
```

where:

- `Sigma` is entropy production,
- `C_lockin` is path-dependent lock-in cost.

The recoverability margin is

```math
\delta_{\mathrm{rec}}
=
\mathcal R_{\mathrm{Qi}}-
\eta_{\mathrm{Qi}}.
```

Runtime rule:

```text
if delta_rec > 0:
    repair_or_rollback_claim may be evaluated
else:
    repair_or_rollback_claim is blocked
```

Thus:

```math
\delta_{\mathrm{rec}}>0
\quad\Rightarrow\quad
\mathrm{RecoveryClaimAllowed},
```

```math
\delta_{\mathrm{rec}}\le 0
\quad\Rightarrow\quad
\mathrm{RecoveryClaimBlocked}.
```

The following is rejected:

```text
repair_claim_without_recovery_margin
DPI_loss_erasure
entropy_lockin_ignored
```

---

## 4. IndraNet gauge transport

IndraNet Qi transport is not graph-edge flow.  It is connection-dependent parallel transport.

The curvature is

```math
F_{\mu\nu}
=
\partial_\mu A_\nu
-
\partial_\nu A_\mu
+[A_\mu,A_\nu].
```

Transport along a path `gamma` is

```math
U_\gamma
=
\mathcal P
\exp\left(-\int_\gamma A_\mu dx^\mu\right).
```

For a closed loop `C`, the Wilson/holonomy residue is

```math
W(C)
=
\mathrm{Tr}\,\mathcal P
\exp\left(-\oint_C A\right).
```

Interpretation in KuuOS:

- `A_mu` gives cross-world connection,
- `F_munu` gives transport curvature,
- `U_gamma` gives path-dependent movement,
- `W(C)` gives residue after circulation,
- nontrivial holonomy indicates scope drift, residue, or translation distortion.

The following is rejected:

```text
graph_only_transport_claimed_as_Qi
transport_without_connection
holonomy_residue_erasure
```

---

## 5. KuString-Qi emergence from relational difference

Qi does not emerge directly from `K`.

The starting point is non-reified emptiness ground `K`.  The first operative object is a dependent-origination difference in the orthogonal conventional domain:

```math
\delta_{\mathrm{rel}}\in K^\perp.
```

A worldsheet mode is represented by

```math
X:\Sigma\to\mathcal M.
```

The string-mode action is

```math
S_{\mathrm{string}}
=
\frac{1}{4\pi\alpha'}
\int_\Sigma
h^{ab}g_{\mu\nu}(X)
\partial_aX^\mu\partial_bX^\nu
\sqrt h\,d^2\sigma
+
S_{\mathrm{rel}}[\delta_{\mathrm{rel}}].
```

The brane boundary condition is

```math
\partial\Sigma\subset B.
```

Gauge connection is induced by the projection

```math
A_\mu
=
\Pi_{\mathrm{gauge}}
(\partial X,B,\delta_{\mathrm{rel}}).
```

Qi current then appears as the gauge-response current

```math
J^\mu_{\mathrm{Qi}}
=
\frac{\delta S_{\mathrm{eff}}}{\delta A_\mu}.
```

The emergence lineage is therefore:

```text
K
  -> delta_rel in K_perp
  -> StringMode
  -> BraneBoundary
  -> A_mu
  -> F_munu
  -> J_Qi_mu
  -> Z_Qi
  -> Physical Quantum Qi
```

Forbidden collapses:

```text
K_identified_as_Qi
string_reified_as_substance
brane_reified_as_creator
mass_gap_claimed_as_Qi_source
```

The MGAP4D internal-normalized `33/20` gap is a stability floor for the `K_perp` world-phase domain.  It is not a Qi source.

---

## 5.1 Boundary coupling and gauge projection

The boundary term that couples string-boundary motion to the gauge connection is

```math
S_{\partial}^{\mathrm{Qi}}
=
\int_{\partial\Sigma}
\chi(\delta_{\mathrm{rel}})
A_\mu(X)\,dX^\mu
=
\int_{\partial\Sigma}
\chi(\delta_{\mathrm{rel}})
A_\mu(X)\partial_\tau X^\mu d\tau.
```

Here `chi(delta_rel)` is the coupling weight that measures how much the dependent-origination difference has condensed into transportable boundary form.  The gauge projection is not an arbitrary label; it is the map from boundary motion to connection data:

```math
A_\mu
=
\Pi_{\mathrm{gauge}}
\left[
\chi(\delta_{\mathrm{rel}})
\int_{\partial\Sigma}
K_\mu{}^a(X,B)\partial_aX\,d\tau
\right].
```

`K_mu^a(X,B)` is the boundary kernel that translates worldsheet tangent/normal motion into brane-gauge components.  Thus

```text
worldsheet boundary motion
  -> brane interface kernel
  -> gauge connection
```

is the actual content of `Pi_gauge`.

The effective action used for Qi current is

```math
S_{\mathrm{eff}}
=
S_{\mathrm{string}}
+S_{\partial}^{\mathrm{Qi}}
+S_{\mathrm{brane}}
+S_{\mathrm{YM}}
+S_{\mathrm{open}}
+S_{\mathrm{rel}}.
```

The Yang-Mills term is

```math
S_{\mathrm{YM}}
=-\frac{1}{4g^2}
\int_{\mathcal M}\mathrm{Tr}(F_{\mu\nu}F^{\mu\nu})\,d^dx.
```

The boundary current is then

```math
J^\mu_{\partial}(x)
=
\int_{\partial\Sigma}
\chi(\delta_{\mathrm{rel}})
\partial_\tau X^\mu(\tau)
\delta^{(d)}(x-X(\tau))d\tau.
```

This is the current density traced by dependent-origination difference moving along a brane boundary.

---

## 5.2 Qi current decomposition

The full Qi current decomposes as

```math
J^\mu_{\mathrm{Qi}}
=
J^\mu_{\partial}
+J^\mu_{\mathrm{rel}}
+J^\mu_{\mathrm{open}}
+J^\mu_{\mathrm{anom}}.
```

The relation-difference action is

```math
S_{\mathrm{rel}}
=
\int
\left[
\frac12G^{ij}(\theta)D_\mu\delta_iD^\mu\delta_j
-V_{\mathrm{rel}}(\delta)
\right]d^dx.
```

where

```math
D_\mu\delta_i=\partial_\mu\delta_i+(A_\mu)_i{}^j\delta_j.
```

The relation-difference current is

```math
J^\mu_{\mathrm{rel}}
=
\frac{\delta S_{\mathrm{rel}}}{\delta A_\mu}
\sim
G^{ij}(\theta)\delta_jD^\mu\delta_i.
```

The open-system current is obtained from the influence action:

```math
J^\mu_{\mathrm{open}}
=
\frac{\delta S_{\mathrm{IF}}}{\delta A_\mu}.
```

The anomaly/residue component `J_anom` carries non-erased residue from scope drift, translation distortion, membrane crossing, and nontrivial holonomy.  It must not be hidden inside a success label.

---

## 5.3 Relation-difference dynamics

A minimal equation of motion for the dependent-origination difference is

```math
\nabla_\mu\left(G^{ij}\partial^\mu\delta_j\right)
+
\frac{\partial V_{\mathrm{rel}}}{\partial\delta_i}
=
\mathcal S_i^{\mathrm{boundary}}.
```

The boundary source `S_boundary` closes the loop:

```text
delta_rel -> StringMode -> BraneBoundary -> A_mu -> J_Qi -> feedback to delta_rel.
```

This makes Qi emergence a coupled relation-boundary-gauge-current process, not a one-step production from emptiness.

---

## 5.4 Qi emergence phases

Physical Quantum Qi is phased, not instantaneous:

```text
NonQi
  -> PreQi
  -> ProtoQi
  -> BoundaryQi
  -> TransportQi
  -> PhysicalQi
  -> FullPathQi
```

The phase conditions are:

```text
NonQi:       no nonzero delta_rel in K_perp.
PreQi:       delta_rel in K_perp, but no StringMode.
ProtoQi:     StringMode exists, but no brane-boundary gauge projection.
BoundaryQi:  boundary coupling exists, but no complete gauge-current definition.
TransportQi: A_mu and F_munu exist, but J_Qi is not yet validated as variation of S_eff.
PhysicalQi:  J_Qi = delta S_eff / delta A_mu and Ward/leak accounting closes.
FullPathQi:  PhysicalQi plus SK/FV history, influence kernel, memory, noise, and backaction.
```

Equivalently,

```math
\phi
=
\Phi(\delta_{\mathrm{rel}},X,B,A_\mu,F_{\mu\nu},J^\mu,Z_{\mathrm{Qi}},\mathcal L_{\mathrm{leak}},\mathcal A_{\mathrm{anom}})
```

with

```text
phi in {NonQi, PreQi, ProtoQi, BoundaryQi, TransportQi, PhysicalQi, FullPathQi}.
```

A higher phase cannot be claimed if any lower constructive condition is missing.

---

## 5.5 PhysicalQi emergence criterion

A compact criterion is

```math
\mathrm{PhysicalQi}
\Longleftrightarrow
\left[
\delta_{\mathrm{rel}}\in K^\perp
\land
\delta_{\mathrm{rel}}\ne0
\land
\partial\Sigma\subset B
\land
A_\mu=\Pi_{\mathrm{gauge}}(\partial X,B,\delta_{\mathrm{rel}})
\land
J^\mu_{\mathrm{Qi}}=\frac{\delta S_{\mathrm{eff}}}{\delta A_\mu}
\land
\mathcal W_{\mathrm{leak}}=0
\right].
```

where

```math
\mathcal W_{\mathrm{leak}}=0
```

means either the closed Ward identity

```math
D_\mu J^\mu_{\mathrm{Qi}}=0
```

or the open Ward/leak identity

```math
D_\mu J^\mu_{\mathrm{Qi}}
-\mathcal L_{\mathrm{leak}}
-\mathcal A_{\mathrm{anom}}
=0.
```

The short definition is

```math
\mathrm{Qi}
=
\left[
\frac{\delta S_{\mathrm{eff}}}{\delta A_\mu}
\right]^{{\mathrm{SK/FV}}}_{\delta_{\mathrm{rel}}\in K^\perp,\ \partial\Sigma\subset B}.
```

In words: Physical Quantum Qi is the SK/FV history of a gauge-response current generated by string-brane-boundary projection of dependent-origination difference on `K_perp`.

---

## 6. Minimal equation packet keys

A v0.2 equation packet should expose at least these keys:

```text
Z_Qi_SKFV
S_sys
S_IF
Delta_q
Sigma_q
D_R_kernel
N_noise_kernel
J_Qi_variation_from_A
Ward_closed_identity
Ward_open_leak_identity
Delta_DPI
R_Qi
eta_Qi
delta_rec
A_mu
F_munu
U_gamma
W_C
K_non_reification
delta_rel_in_K_perp
StringMode_worldsheet
BraneBoundary
A_mu_projection_from_string_brane
J_Qi_from_effective_action
S_boundary_Qi
chi_delta_rel
boundary_kernel_K_mu_a
S_eff
S_YM
J_boundary
J_rel
J_open
J_anom
D_mu_delta
S_rel
relation_difference_eom
Qi_phase_label
PhysicalQi_emergence_criterion
Ward_leak_residual_zero
mass_gap_33_20_floor_not_source
```

These keys are not mere metadata; they are the minimum equation-level content that distinguishes Physical Quantum Qi v0.2 from a symbolic or metaphorical Qi layer.
