# Physical Quantum Qi DPI Recoverability v0.2C

This addendum theoremizes the DPI recoverability layer of Physical Quantum Qi v0.2.  It defines the DPI gap, Qi recoverability score, irreversibility burden, recovery margin, and the repair/rollback decision gate.

This is an equation-level and theorem-target tightening. It grants no proof, ontology, clinical, execution, commit, belief-root commit, memory-overwrite, world-root-rewrite, truth, or safety-override authority.

---

## C1. States, channel, and relative entropy

Let `rho` and `sigma` be density operators on a declared Qi information state space.  Let

```math
\mathcal E : \mathcal D(\mathcal H) \to \mathcal D(\mathcal K)
```

be a completely positive trace-preserving channel representing coarse-graining, observation, transport, membrane crossing, or environment tracing.

The quantum relative entropy is

```math
D(\rho\Vert\sigma)
=\operatorname{Tr}\rho(\log\rho-\log\sigma)
```

when `supp(rho) subset supp(sigma)`, and `+infty` otherwise.

Required fields:

```text
rho_declared
sigma_declared
channel_E_declared
CPTP_channel_declared
relative_entropy_declared
support_condition_declared
```

Rejected claims:

```text
DPI_claim_without_states
DPI_claim_without_channel
relative_entropy_without_support_condition
```

---

## C2. DPI gap `Delta_DPI`

Data processing gives

```math
D(\rho\Vert\sigma)
\ge
D(\mathcal E(\rho)\Vert\mathcal E(\sigma)).
```

Define the DPI gap:

```math
\Delta_{\mathrm{DPI}}
=
D(\rho\Vert\sigma)
-D(\mathcal E(\rho)\Vert\mathcal E(\sigma)).
```

Thus

```math
\Delta_{\mathrm{DPI}}\ge0.
```

`Delta_DPI` is the information loss caused by the declared channel.  Larger `Delta_DPI` means greater lost distinguishability and weaker recoverability.

The equality case is special:

```math
\Delta_{\mathrm{DPI}}=0
\iff
\exists\ \mathcal R\ \text{CPTP such that}\
\mathcal R\mathcal E(\rho)=\rho,
\quad
\mathcal R\mathcal E(\sigma)=\sigma
```

under the standard sufficiency/recovery condition.

Required fields:

```text
Delta_DPI_defined
DPI_nonnegative_declared
DPI_channel_loss_interpretation_declared
DPI_equality_recovery_condition_declared
```

Rejected claims:

```text
negative_Delta_DPI_without_diagnostic
DPI_loss_erasure
recovery_claim_ignores_DPI_gap
```

---

## C3. Qi recoverability score `R_Qi`

The Qi recoverability score is defined as a monotone decreasing function of the DPI gap:

```math
R_{\mathrm{Qi}}
=\exp(-\Delta_{\mathrm{DPI}}).
```

Therefore

```math
0<R_{\mathrm{Qi}}\le1.
```

and

```math
\Delta_{\mathrm{DPI}}=0 \Rightarrow R_{\mathrm{Qi}}=1.
```

This score is not authority.  It is evidence for how much of the pre-channel distinguishability can be recovered in principle.

If a Fawzi-Renner style lower bound is used, a fidelity-based recovery witness may also be declared:

```math
D(\rho\Vert\sigma)-D(\mathcal E(\rho)\Vert\mathcal E(\sigma))
\ge
-2\log F\left(\rho,\mathcal R_{\sigma,\mathcal E}(\mathcal E(\rho))\right).
```

The packet may then store

```math
F_{\mathrm{rec}}
=F\left(\rho,\mathcal R_{\sigma,\mathcal E}(\mathcal E(\rho))\right).
```

as an optional witness, but not as a replacement for `Delta_DPI`.

Required fields:

```text
R_Qi_defined
R_Qi_range_declared
R_Qi_monotone_in_Delta_DPI_declared
optional_recovery_fidelity_witness_declared_if_used
```

Rejected claims:

```text
R_Qi_without_Delta_DPI
recoverability_score_grants_authority
fidelity_witness_replaces_DPI_gap
```

---

## C4. Irreversibility burden `eta_Qi`

Recoverability is not determined by `Delta_DPI` alone.  Physical Quantum Qi also carries entropy production and lock-in burden.

Define

```math
\eta_{\mathrm{Qi}}
=\Delta_{\mathrm{DPI}}
+\Sigma
+C_{\mathrm{lockin}}
+C_{\mathrm{mem}}
+C_{\mathrm{obs}}.
```

where:

- `Sigma` is entropy production,
- `C_lockin` is path-dependent lock-in cost,
- `C_mem` is non-Markov memory burden,
- `C_obs` is observation/intervention burden.

All terms must be nonnegative unless a signed diagnostic convention is explicitly declared:

```math
\Sigma\ge0,
\quad
C_{\mathrm{lockin}}\ge0,
\quad
C_{\mathrm{mem}}\ge0,
\quad
C_{\mathrm{obs}}\ge0.
```

The burden is therefore normally nonnegative:

```math
\eta_{\mathrm{Qi}}\ge0.
```

Required fields:

```text
eta_Qi_defined
entropy_production_declared
lockin_cost_declared
memory_burden_declared
observation_burden_declared
nonnegative_burden_terms_declared
```

Rejected claims:

```text
eta_Qi_without_entropy_production
lockin_ignored
nonMarkov_memory_burden_ignored
observation_burden_ignored
negative_burden_without_convention
```

---

## C5. Recovery margin `delta_rec`

The recovery margin is

```math
\delta_{\mathrm{rec}}
=R_{\mathrm{Qi}}-\eta_{\mathrm{Qi}}.
```

The sign of `delta_rec` gates recovery claims:

```math
\delta_{\mathrm{rec}}>0
\Rightarrow
\text{repair/rollback may be evaluated}.
```

```math
\delta_{\mathrm{rec}}\le0
\Rightarrow
\text{repair/rollback claim is blocked}.
```

This is a gate, not a command to repair.  Positive `delta_rec` opens evaluation; it does not grant execution authority.

Required fields:

```text
delta_rec_defined
delta_rec_sign_declared
delta_rec_positive_opens_evaluation_declared
delta_rec_nonpositive_blocks_recovery_declared
nonauthority_boundary_declared
```

Rejected claims:

```text
repair_claim_without_delta_rec
rollback_claim_without_delta_rec
positive_delta_rec_claimed_as_execution_authority
```

---

## C6. Repair/rollback decision theorem targets

### Theorem C6.1: DPI nonnegativity gate

```math
\Delta_{\mathrm{DPI}}\ge0.
```

If a packet declares `Delta_DPI < 0`, the packet is invalid unless it explicitly marks the value as a numerical diagnostic error.

### Theorem C6.2: Recoverability range

```math
0<R_{\mathrm{Qi}}\le1.
```

### Theorem C6.3: Nonnegative burden

If all burden components are nonnegative, then

```math
\eta_{\mathrm{Qi}}\ge0.
```

### Theorem C6.4: Recovery gate

```math
\delta_{\mathrm{rec}}>0
\Rightarrow
\mathrm{RecoveryEvaluationOpen}.
```

```math
\delta_{\mathrm{rec}}\le0
\Rightarrow
\mathrm{RecoveryBlocked}.
```

### Theorem C6.5: Non-authority theorem

```math
\mathrm{RecoveryEvaluationOpen}
\nRightarrow
\mathrm{ExecutionAuthority}.
```

That is, a positive recovery margin allows DecisionOS / PlanOS evaluation, but cannot itself execute repair or rollback.

---

## C7. Runtime decision gate

The runtime decision function is:

```text
input:
  Delta_DPI
  Sigma
  C_lockin
  C_mem
  C_obs

compute:
  R_Qi = exp(-Delta_DPI)
  eta_Qi = Delta_DPI + Sigma + C_lockin + C_mem + C_obs
  delta_rec = R_Qi - eta_Qi

if Delta_DPI < 0:
  REJECT unless numerical_diagnostic_error_declared
elif delta_rec > 0:
  status = recovery_evaluation_open
else:
  status = recovery_blocked

always:
  execution_authority = false
  commit_authority = false
  memory_overwrite_authority = false
  world_root_rewrite_authority = false
```

The correct interpretation is:

```text
positive delta_rec
  = enough recoverability margin to evaluate repair/rollback
  != automatic rollback
  != memory overwrite
  != world root rewrite
  != execution authority
```

---

## C8. Minimal packet keys

```text
rho_declared
sigma_declared
channel_E_declared
CPTP_channel_declared
relative_entropy_declared
support_condition_declared
Delta_DPI_defined
Delta_DPI_value_declared
DPI_nonnegative_declared
R_Qi_defined
R_Qi_value_declared
R_Qi_range_declared
eta_Qi_defined
Sigma_declared
C_lockin_declared
C_mem_declared
C_obs_declared
nonnegative_burden_terms_declared
delta_rec_defined
delta_rec_value_declared
delta_rec_sign_declared
repair_rollback_gate_declared
nonauthority_boundary_declared
```
