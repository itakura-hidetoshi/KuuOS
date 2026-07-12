# PlanOS State-Dependent Metric Jet and Levi-Civita Certificate Kernel v0.1

## Purpose

PlanOS v1.05 introduced the native coupled positive-definite metric

```text
G_QHC = D_QH + B^T B
```

on a finite Plan coordinate chart. PlanOS v1.06 makes that metric locally state-dependent:

```text
G = G(theta, Q, H, W)
```

where `theta` is the Plan state point, `Q` is the Qi condition, `H` is the read-only history condition, and `W` is the read-only WORLD condition.

The v1.06 certificate consumes one bounded first metric jet:

```text
g_ij
(g^-1)^ij
partial_k g_ij
```

and reconstructs the unique Levi-Civita connection represented in that finite chart.

## Christoffel reconstruction

The first-kind Christoffel symbol is

```text
Gamma_ijk
= 1/2 (partial_j g_ik + partial_k g_ij - partial_i g_jk)
```

and the raised symbol is

```text
Gamma^i_jk = (g^-1)^il Gamma_ljk
```

The runtime independently verifies:

```text
g_ij = g_ji
partial_k g_ij = partial_k g_ji
g^-1 g = I
g g^-1 = I
Gamma^i_jk = Gamma^i_kj
nabla_k g_ij = 0
```

Thus torsion-freeness and metric compatibility are not supplied as unchecked flags; they are recomputed from the bounded jet.

## Bounded first-order parallel transport

For a candidate tangent vector `v` and a small chart displacement `dtheta`, the kernel computes

```text
v'^i = v^i - Gamma^i_jk dtheta^j v^k
```

and the geodesic acceleration

```text
a^i = -Gamma^i_jk v^j v^k
```

The displaced metric is predicted to first order:

```text
g'_ij = g_ij + partial_k g_ij dtheta^k
```

Metric compatibility implies preservation of metric norm to first order. The runtime therefore checks the finite residual

```text
|g'_ij v'^i v'^j - g_ij v^i v^j|
```

against an explicit bound.

## State and lineage binding

The certificate binds:

```text
source PlanOS v1.05 metric certificate digest
Plan coordinate schema
Plan state point theta
Qi state digest
history state digest
WORLD state digest
metric matrix
inverse metric matrix
first metric derivatives
candidate tangent field
candidate source digests
```

All structured inputs are canonicalized before digest comparison.

## Fail-closed conditions

The kernel rejects:

```text
missing or stale source digests
coordinate-schema mismatch
state-context mismatch
metric-jet digest mismatch
candidate tangent digest mismatch
nonsymmetric or non-positive-definite metric
invalid inverse metric
nonsymmetric metric derivative
zero state-dependent jet
metric derivative bound violation
nontrivial connection absence
Christoffel bound violation
torsion residual
metric-compatibility residual
empty or duplicate candidate tangent field
candidate coordinate mismatch
nonfinite tangent or displacement
transport displacement bound violation
first-order norm-defect bound violation
```

## Formal theorem package

The Mathlib package proves directly from the first-kind formula:

```text
Gamma_ijk = Gamma_ikj
partial_k g_ij = Gamma_jki + Gamma_ikj
```

under symmetry of `partial_k g_ij` in the metric indices.

It also proves:

```text
raised Christoffel torsion-freeness
zero-displacement transport identity
zero-connection transport identity
zero-connection geodesic acceleration
constant metric jet -> zero Levi-Civita connection
```

## Fixed boundaries

```text
connection != candidate selection
parallel transport != action execution
geodesic acceleration != command
metric compatibility != empirical truth
WORLD-conditioned metric jet != WORLD mutation
history-conditioned metric jet != history sovereignty
```

The layer retains the entire candidate tangent field and performs no selection.

```text
candidate_tangent_field_retained = true
decision_selection_performed = false
```

It remains read-only and future-only.

```text
source_metric_not_mutated = true
persistent_world_state_unchanged = true
history_read_only = true
future_only = true
active_now = false
execution_permission = false
```

## Validation

```bash
PYTHONPATH=. python3 scripts/check_planos_state_dependent_metric_jet_levi_civita_certificate_kernel_v0_1.py
PYTHONPATH=. python3 runtime/kuuos_current_check.py --profile planos
lake env lean formal/KuuOSPlanOSV1_06.lean
```
