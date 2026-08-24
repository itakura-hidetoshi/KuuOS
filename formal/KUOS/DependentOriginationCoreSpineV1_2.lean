import KUOS.DependentOriginationCoreSpineV1_1
import KUOS.DependentOriginationRefinementTransitivityV1_2

namespace KUOS.DependentOriginationCoreSpineV1_2

/-!
# Dependent-origination core spine v1.2

This non-quantum aggregate extends the contextual parent through compositional
refinement and transitive descent.

The structural hierarchy is now:

```text
context category
  -> state-valued functor
  -> composable contextual transport
  -> contextual refinement cover
  -> pairwise common refinement / overlap compatibility
  -> optional state descent
  -> invariant semantic descent
  -> refinement of each local chart
  -> flattening of two refinement stages
  -> exact transitivity of state descent
  -> transitivity of invariant semantic descent
```

The important boundary remains explicit:

```text
semantic descent
```

can persist through arbitrarily finer contextual conditioning without requiring
one global root-state witness.  Additional local separation assumptions show
that further refinement does not manufacture such a witness when none existed
at the preceding level.

No groupoid, quantum, Choi, process-tensor, Hamiltonian, spectral-gap, or
physical Yang--Mills assumption is part of this aggregate.
-/

end KUOS.DependentOriginationCoreSpineV1_2
