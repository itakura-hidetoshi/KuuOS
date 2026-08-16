# KuuOS Qi Wuxing Phase-Projection Quotient/Kernel v2.8

## Status

Append-only successor to Qi Wuxing Relation-Word Protected History v2.7.

Exact base:

`main@6ccf8775d285c15bdd1f3c203290209250d6c864`

v2.7 proved that finite relation words can close in the `FivePhase = ZMod 5`
coordinate while retaining nonzero protected-history shift.  v2.8 turns that
information loss into an explicit projection/kernel/quotient structure.

## Mathematical core

The protected shift space remains

`WuxingShift = FivePhase × Nat`.

Define the additive phase projection

`π : WuxingShift →+ FivePhase`

by `π(z, n) = z`.

The strict Lean layer proves:

1. `π` is surjective.
2. `ker π` is exactly the shifts with zero phase displacement.
3. Every phase-closed relation word has total shift in `ker π`.
4. Every nonempty phase-closed word supplies a nonzero kernel element.
5. In particular, `[control, insult]` is a nonzero kernel witness.
6. Therefore `π` is not injective.
7. Equality after phase projection defines an equivalence relation
   `SamePhaseShift` compatible with addition.
8. The quotient of protected shifts by this observational equivalence is
   equivalent, as a type, to `FivePhase`.
9. Equality with the zero quotient class is equivalent to kernel membership.
10. `[control]` and `[generation, generation]` become equal in the phase
    quotient while remaining distinct protected shifts.

Thus the phase endpoint is literally a quotient-level observable of a richer
protected-history structure.  The kernel records precisely the information
that can disappear under phase observation without being zero in the richer
space.

## KuuOS reading

- **空**: equality in the phase quotient is not reified as equality of the full
  process-bearing shift.
- **縁起**: nonzero protected-history residue remains dependent on the actual
  relational composition even when phase displacement cancels.
- **二諦**: phase observation is represented as a mathematically explicit
  conventional quotient of a richer architecture-level structure.
- **中道**: phase equivalence is retained exactly where valid, while neither
  phase identity nor protected history is promoted to an independent
  substance.

## Fixed boundaries

This layer does **not** claim:

- that five phases are substances;
- that protected-history count is a Qi quantity;
- that the quotient is a physical gauge quotient;
- that `ker π` is a physical vacuum sector, gauge orbit, conserved charge, or
  causal hidden variable;
- that classical Wuxing is Yang-Mills gauge theory, `SU(2)_3`, or anyon
  physics;
- that quotient equivalence means equality of temporal, causal, biological, or
  clinical processes;
- that the finite formal structure supplies a validated biological or clinical
  dynamics;
- that formal compilation grants clinical, execution, WORLD, truth, or
  external theorem authority.

The update is append-only / tighten-only.  v2.7 and all earlier layers are
imported and not modified.
