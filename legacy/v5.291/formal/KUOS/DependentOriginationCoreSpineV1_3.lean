import KUOS.DependentOriginationCoreSpineV1_2
import KUOS.DependentOriginationDirectedCofinalSemanticsV1_3

namespace KUOS.DependentOriginationCoreSpineV1_3

/-!
# Dependent-origination core spine v1.3

This non-quantum aggregate extends the contextual parent through directed and
cofinal refinement semantics:

```text
context category
  -> state-valued functor
  -> composable contextual transport
  -> contextual refinement and overlap coherence
  -> optional state descent / invariant semantic descent
  -> refinement-of-refinement and exact descent transitivity
  -> directed refinement net
  -> coherent state family on all refinement stages
  -> unique invariant semantic value
  -> order-cofinal semantic criterion
  -> state recovery from a cofinal lens only with explicit local separation
```

The parent notion still does not assume a groupoid, Grothendieck site, sheaf,
stack, categorical colimit, quantum process tensor, Choi matrix, Hamiltonian,
spectral gap, or physical Yang--Mills theorem.

The main structural boundary is now explicit:

```text
cofinality + invariant readout
  => semantic value is fully determined on any cofinal refinement lens

cofinality alone
  !=> root-state recovery

cofinality + local-state separation
  => root-state recovery can be tested on the cofinal lens.
```

Thus semantic stability under indefinitely finer contextual conditioning does
not require silently reintroducing one global substance-like carrier.
-/

end KUOS.DependentOriginationCoreSpineV1_3
