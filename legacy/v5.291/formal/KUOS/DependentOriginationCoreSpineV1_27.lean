import KUOS.DependentOriginationCoreSpineV1_26
import KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27

namespace KUOS.DependentOriginationCoreSpineV1_27

/-!
# Dependent-origination core spine v1.27

The parent dependent-origination definition remains unchanged.  Version 1.27
advances the higher-categorical presentation-independent invariant from
cross-model intrinsic transport to direct global Duskin transport whenever the
chosen bicategorical model equivalence is presented by a strictly-unitary
pseudofunctor.

The new chain is

```text
StrictlyUnitaryBicategoricalModelEquivalence B C
  -> BicategoricalModelEquivalence B C                    -- forget normalization
  -> N_Duskin(B) -> N_Duskin(C)                           -- all simplicial degrees
  -> edge invariant transported exactly
  -> comparison transported with pseudofunctor coherence
  -> nondegenerate thin triangles remain thin
```

For a source Duskin triangle with comparison

```text
f ≫ g -> h,
```

the target comparison is exactly

```text
F(f) ≫ F(g)
  -> F(f ≫ g)        via `(F.mapComp f g).inv`
  -> F(h)            via `F.map₂` of the source comparison.
```

Thus the direct global presentation and the intrinsic v1.26 transport agree
up to precisely the canonical composition coherence forced by the
pseudofunctor.  The invariant is not changed by this normalization layer.

The remaining presentation problem is explicit: construct and compare
strictly-unitary normalizations for sufficiently general pseudofunctorial
biequivalence data, and then promote the current thinness theorem to a bundled
scaled map including degeneracies and horn-family transport.
-/

end KUOS.DependentOriginationCoreSpineV1_27
