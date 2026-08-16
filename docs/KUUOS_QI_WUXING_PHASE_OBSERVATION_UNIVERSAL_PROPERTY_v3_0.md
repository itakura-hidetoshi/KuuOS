# KuuOS Qi Wuxing Phase-Observation Universal Property v3.0

## Status

Append-only successor to Qi Wuxing AddCon First Isomorphism v2.9.

Exact base:

`main@e3db96ba072603fc7316fd673d09fb760cdf76b0`

v2.9 upgraded the phase observational quotient to Mathlib's additive congruence
quotient and proved

`(AddCon.ker phaseProjection).Quotient ≃+ FivePhase`.

v3.0 strengthens that statement to the universal property of phase observation.

## Mathematical core

The protected shift space remains

`WuxingShift = FivePhase × Nat`.

The additive phase projection remains

`phaseProjection : WuxingShift →+ FivePhase`.

For any target additive structure `P`, an additive observation

`obs : WuxingShift →+ P`

is called phase-compatible when

`AddCon.ker phaseProjection ≤ AddCon.ker obs`.

Equivalently, if two protected shifts have the same phase projection, then
`obs` gives them the same value.

The strict Lean layer proves two universal factorization statements.

First, through the additive quotient:

```text
∃! lift : PhaseAddQuotient →+ P,
  lift.comp phaseAddClass = obs
```

The witness is Mathlib's

`(AddCon.ker phaseProjection).lift obs h`,

and uniqueness is supplied by `AddCon.lift_unique`.

Second, through phase space itself:

```text
∃! factor : FivePhase →+ P,
  factor.comp phaseProjection = obs
```

The canonical witness evaluates `obs` on the zero-history representative
`(phase, 0)`. Because every protected shift is phase-equivalent to its
zero-history representative, phase compatibility proves the commuting diagram.
Surjectivity of `phaseProjection`, represented constructively by the same
zero-history section, gives uniqueness.

The layer also proves that phase compatibility is equivalent to existence of a
factor through `phaseProjection`.

## Consequences for protected history

The universal property makes the information-loss statement independent of any
particular target observation.

For every phase-compatible additive observation:

- every phase-closed relation word has the same observed value as the zero
  protected shift;
- a nonempty phase-closed word can still have nonzero protected shift;
- `[control, insult]` is observationally equal to zero for every such
  observation while remaining nonzero in protected-shift space;
- `[control]` and `[generation, generation]` are observationally equal for every
  such observation while their protected shifts remain distinct.

Thus the loss of protected-history information is not an artefact of one chosen
observable. It is forced by the universal property of factoring through phase
projection.

## KuuOS reading

- **空**: equality after phase observation is not reified as equality of the
  richer protected process.
- **縁起**: the full relational composition remains prior to quotienting, even
  when every phase-only additive observation identifies two shifts.
- **二諦**: the phase layer is characterized not only by a quotient but by its
  universal mapping property relative to phase-compatible observations.
- **中道**: valid phase-level identification is preserved exactly, without
  introducing negative history counts or converting protected history into a
  substance.

## Fixed boundaries

This layer does **not** claim:

- that five phases are substances;
- that protected-history count is a Qi quantity;
- that the additive quotient is a physical gauge quotient;
- that phase compatibility is gauge invariance in a physical field theory;
- that the kernel congruence is a vacuum sector, conserved charge, gauge orbit,
  or causal hidden variable;
- that classical Wuxing is Yang-Mills gauge theory, `SU(2)_3`, or anyon physics;
- that quotient equality is equality of temporal, causal, biological, or
  clinical processes;
- that the finite formal structure supplies validated biological or clinical
  dynamics;
- that formal compilation grants clinical, execution, WORLD, truth, or
  external theorem authority.

The update is append-only / tighten-only. v2.9 and all earlier layers are
imported and not modified.
