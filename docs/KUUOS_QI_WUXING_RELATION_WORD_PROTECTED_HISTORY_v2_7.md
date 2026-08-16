# KuuOS Qi Wuxing Relation-Word Protected History v2.7

## Status

Append-only successor to Qi Wuxing Generation-Control Coherence v2.6.

Exact base:

`main@f5b7fee3d41d839c7b2eaf0bf72a419c655f4e8c`

The v2.6 layer formalized single canonical Wuxing relations as protected shifts

`WuxingShift = ZMod 5 × Nat`

with phase displacement in the first coordinate and protected Fibonacci-history event count in the second coordinate. v2.7 lifts that structure to arbitrary finite relation words.

## Mathematical core

For a finite word `w = [r₁, …, rₙ]`, define

`S(w) = S(r₁) + … + S(rₙ)`.

The strict Lean layer proves:

1. `S(u ++ v) = S(u) + S(v)`.
2. Every canonical relation contributes exactly one protected-history event.
3. `(S(w)).history_events = length(w)`.
4. Executing a word is exactly the v2.6 action of its total shift.
5. `A_(u ++ v)(x) = A_v(A_u(x))`.
6. Word execution advances protected Fibonacci history by exactly `length(w)` events.
7. A phase-closed word has phase displacement zero.
8. Every nonempty word has a nonzero protected shift.
9. Therefore every nonempty phase-closed word has a protected-history residue: zero phase displacement, positive event count, and nonzero total protected shift.
10. Words with different lengths have different protected shifts even if their phase projections agree.

The canonical example is

`[control, insult]`.

Its `ZMod 5` phase displacement vanishes, but its protected-history event count is `2`. Thus phase cancellation does not erase relational history.

Likewise, `[control]` and `[generation, generation]` have the same phase projection but distinct protected shifts because their event counts are `1` and `2`.

## KuuOS reading

- **空**: a phase endpoint alone is not reified as the whole process.
- **縁起**: finite relational composition retains dependence on the actual sequence of events.
- **二諦**: the phase projection is a conventional quotient of richer protected-history structure, not the whole structure.
- **中道**: phase cancellation is retained without collapsing protected history, while history is not promoted to an independent substance.

## Fixed boundaries

This layer does **not** claim:

- that five phases are five substances;
- that protected-history event count is a Qi quantity;
- that equal phase endpoint means equal temporal or causal process;
- that a phase-closed word is physical gauge holonomy;
- that classical Wuxing is Yang-Mills gauge theory, `SU(2)_3`, or anyon physics;
- that finite formal composition supplies a validated biological or clinical dynamics;
- that formal compilation grants clinical, execution, WORLD, truth, or external theorem authority.

The update is append-only / tighten-only. v2.6 is imported and not modified.
