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
mass_gap_33_20_floor_not_source
```

These keys are not mere metadata; they are the minimum equation-level content that distinguishes Physical Quantum Qi v0.2 from a symbolic or metaphorical Qi layer.
