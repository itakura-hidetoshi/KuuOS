# Qi–WORLD Cross-Cycle Blocker Theory v1.5

## Position

v1.4 constructs the next native BeliefOS → DecisionOS → plural → Wa → PlanOS
branch from a completed v1.3 cycle. v1.5 does not replace or mutate that
receipt. It derives a separate blocker certificate from it.

```text
validated cross-cycle receipt v1.4
→ component blocker vectors
→ pointwise meet
→ composed blocker certificate
→ block unlicensed transition or quarantine
```

## Blocker vector

The seven required blockers are:

1. `present_activation_blocker`
2. `execution_authority_blocker`
3. `memory_overwrite_blocker`
4. `world_identity_blocker`
5. `truth_authority_blocker`
6. `same_cycle_self_loop_blocker`
7. `multi_world_collapse_blocker`

Each component surface starts from the all-true identity and changes only the
blockers it can witness. The final vector is the pointwise Boolean meet of the
receipt, PlanOS, Qi process, WORLD projection, lineage, and authority vectors.

## Algebra

For blocker vectors `a`, `b`, and `c`:

```text
a ∧ b = b ∧ a
(a ∧ b) ∧ c = a ∧ (b ∧ c)
a ∧ a = a
a ∧ ⊤ = a
```

Thus blocker composition is a meet-semilattice. A composed blocker is active
only when every contributing surface preserves that boundary.

## Fail-closed rule

```text
all blockers active
→ disposition = BLOCKED_UNLICENSED_CROSS_CYCLE_TRANSITION

at least one blocker inactive
→ disposition = QUARANTINE_BLOCKER_EVIDENCE_INCOMPLETE
```

No missing blocker is repaired by another Qi, PlanOS, WORLD, or authority
surface.

## Binding surfaces

- Present activation: next ActOS has not started and no ActOS artifact exists.
- Execution: the bridge, Qi receipt, and blocker issue no execution authority.
- Memory: the prior cycle is immutable and `BeliefActivation.memory_overwrite`
  is false.
- WORLD identity: the projection is read-only, nonfinal, and cannot update the
  exact WORLD.
- Truth: candidate projection does not become fact authority.
- Cycle separation: a committed PlanOS state is not recursive same-cycle ActOS
  invocation.
- Noncollapse: the two-truths gap and multi-WORLD noncollapse remain visible.

## Boundedness

The blocker is local to this cross-cycle transition. It is contextual,
repairable by new evidence, and may only block or request further probing. It
is not a root principle, moral veto, truth source, execution license, plan
commit, or irreversible tightening mechanism.

## Fixed boundary

```text
blocker certificate ≠ execution authority
blocker success ≠ plan activation
blocker failure ≠ silent repair
WORLD projection ≠ exact WORLD
Qi process visibility ≠ causal authority
cross-cycle plan ≠ same-cycle ActOS start
```
