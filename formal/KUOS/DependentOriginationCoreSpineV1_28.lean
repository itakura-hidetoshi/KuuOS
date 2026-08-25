import KUOS.DependentOriginationCoreSpineV1_27
import KUOS.DependentOriginationNormalizationChoiceInvariantV1_28

namespace KUOS.DependentOriginationCoreSpineV1_28

/-!
# Dependent-origination core spine v1.28

The parent dependent-origination definition remains unchanged. Version 1.28
removes the choice of strictly-unitary normal representative from the
presentation-independent invariant, subject only to explicit comparison data
that the pinned Mathlib revision can actually express.

The higher-categorical chain is now

```text
general BicategoricalModelEquivalence B C
  + StrictlyUnitaryNormalizationCertificate
  -> chosen normal representative
  -> direct global Duskin transport                       -- v1.27

normal representatives E₁, E₂
  + NormalizationChoiceComparison E₁ E₂
  -> native strong-naturality isomorphisms on 1-cells
  -> native strong-naturality squares on 2-cells
  -> coherent observables agree
  -> transported intrinsic 2-cell invertibility agrees
```

The crucial point is that normalization independence is not expressed as
literal equality of normal pseudofunctors. The correct invariant relation is
coherent bicategorical equivalence:

```text
E₁(f) ≫ η_Y  ≅  η_X ≫ E₂(f)
```

and for every `α : f -> g`,

```text
(E₁.map₂ α ▷ η_Y) ; η_g
  =
η_f ; (η_X ◁ E₂.map₂ α).
```

Every observable that descends through these coherent changes therefore has a
normalization-independent value. In particular, because the local hom functors
of both model equivalences are categorical equivalences, they preserve and
reflect `IsIso`; hence invertibility of every transported intrinsic 2-cell is
independent of which normal representative is chosen.

The pinned Mathlib revision still does not construct normalizations or bundled
icons automatically. Those existence/comparison problems remain explicit
certificates rather than hidden assumptions. The next remaining global step is
to transport the full scaling/horn structure and to show independence of those
higher choices as well.
-/

end KUOS.DependentOriginationCoreSpineV1_28
