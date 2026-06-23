# WORLD Kū Vacuum and OS Hilbert Completion Bridge v0.49

v0.49 extends the WORLD v0.48 read-only mathematical sidecar with an analytic vacuum layer built from a supplied Osterwalder–Schrader reflection-positive completion.

```text
positive-time observables
  → reflection-positive sesquilinear form
  → null directions
  → quotient class map
  → completed complex Hilbert carrier H_OS
  → constant-observable class Ω_OS = [1]
  → standard-form identification Ω_Kū
  → normalized positive vacuum state
  → gauge, modular-time, and physical-time invariance
  → zero-energy vacuum sector
```

The exact WORLD is not identified with the Hilbert carrier or with the vacuum vector.

The analytic vacuum is not the zero vector and is not a metaphysical definition of Kū.

## Reflection-positive input

The bridge receives a positive-time observable type and a complex-valued form

```text
(F, G)_OS.
```

The supplied positivity condition is

```text
Re (F, F)_OS >= 0.
```

It also receives the exact null set

```text
N_OS = {F | (F, F)_OS = 0}.
```

The quotient and completion theorem remain explicit analytic receipts.

Runtime does not construct the quotient, complete an infinite-dimensional space, or infer reflection positivity from samples.

## Completed Hilbert carrier

The bridge carries a completed complex Hilbert space `H_OS`, a class map from positive-time observables, and the inner-product identity

```text
<[F], [G]> = (F, G)_OS.
```

The class of the constant observable is

```text
Ω_OS = [1].
```

It is supplied with unit norm.

## Standard-form vacuum

A complex linear isometric equivalence identifies `H_OS` with the existing v0.32 standard-form Hilbert carrier.

The transported constant class is required to equal the existing cyclic and separating vector:

```text
Ω_Kū = U_OS Ω_OS = Ω_standard.
```

Lean directly derives:

```text
||Ω_Kū|| = 1
Ω_Kū != 0
Ω_Kū belongs to the natural cone
```

The cyclic and separating receipts are inherited from the standard-form bridge.

## Vacuum state

The normalized positive vacuum state is represented by

```text
ω_Kū(a) = <Ω_Kū, π(a) Ω_Kū>.
```

The bridge requires:

```text
ω_Kū(1) = 1
Re ω_Kū(a* a) >= 0.
```

A typed gauge action is supplied, together with

```text
ω_Kū(g · a) = ω_Kū(a).
```

This is an analytic state functional.

It is not truth authority, execution authority, or a replacement for WORLD evidence.

## Vacuum ray and vacuum sector

The physical state represented by the vacuum is its phase ray

```text
[Ω_Kū] = {z Ω_Kū | |z| = 1}.
```

The zero-energy vacuum sector is

```text
V_Kū = {ψ | ψ is in Dom(H) and H ψ = 0}.
```

Lean verifies that `Ω_Kū` belongs to both the vacuum ray and the vacuum sector.

v0.49 does not require the vacuum sector to be one-dimensional.

Degenerate or plural vacuum sectors remain permitted so that the analytic layer does not force multi-WORLD collapse.

## Modular and physical time

The existing modular unitary flow fixes the analytic vacuum:

```text
U_mod(t) Ω_Kū = Ω_Kū.
```

A separate supplied physical-time star-algebra flow and unitary implementation also fix the vacuum:

```text
U_phys(t) Ω_Kū = Ω_Kū.
```

The two flows are not identified.

```text
modular time != physical time
```

Self-adjointness of the physical Hamiltonian, Stone generation, and the physical cluster property remain analytic receipts.

## Lean-direct surface

Lean directly verifies:

- OS-form positivity access;
- exact null-set characterization access;
- unit norm of the OS vacuum;
- identification with the standard-form cyclic and separating vector;
- unit norm and nonvanishing of the transported vacuum;
- natural-cone membership;
- vacuum-ray membership;
- zero-energy vacuum-sector membership;
- normalized positive vacuum-state access;
- gauge invariance of the vacuum state;
- modular-vacuum invariance;
- physical-time group, isometry, covariance, and vacuum-invariance consequences;
- analytic-receipt, runtime-boundary, and representation-boundary packages.

## Fixed boundary

```text
Kū != zero vector
WORLD != vacuum vector
Hilbert vacuum != metaphysical Kū
modular time != physical time
vacuum state != truth authority
vacuum sector != WORLD collapse
validation != truth
candidate != authority
```

The v0.49 bridge is a hash-addressable, proof-facing, read-only analytic sidecar.

It does not update WORLD, execute the Hamiltonian, execute physical time, construct the OS completion, or declare a unique vacuum.
