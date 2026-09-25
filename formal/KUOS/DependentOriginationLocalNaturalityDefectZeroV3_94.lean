import KUOS.DependentOriginationHexagramCrossingCorrectionV3_93
import Mathlib

namespace KUOS.DependentOriginationLocalNaturalityDefectZeroV3_94

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryFactorizationParityV3_74
open KUOS.DependentOriginationLocalizedCompositorNaturalityV3_77
open KUOS.DependentOriginationHexagramCrossingCorrectionV3_93

set_option autoImplicit false

noncomputable section

/-!
# Local naturality defects vanish v3.94

v3.93 isolates the six crossing-correction total as the only place where a
nonzero recursive inner obstruction can enter after the naive endpoint
coboundary has vanished.

A natural first candidate is the failure of one localized compositor
naturality square.  But v3.77 already proves those squares commute exactly.

This file packages the additive four-term naturality defect and proves it is
identically zero for arbitrary localization arrows and arbitrary source-fiber
connectors.  It then specializes this fact to the two existing middle-switch
naturality squares ending at H0 and H1.

Therefore the required nonzero crossing correction cannot be the defect of an
individual naturality square.  It must arise, if at all, from how several
individually commuting squares are pasted or descended globally around the
hexagram.
-/

/-- Additive defect of one localized compositor naturality square.

The grouping is chosen to match the v3.77 equality
comp(A)+comp(B) = mapped(u)+twiceMapped(u).
-/
noncomputable def counterFactorizationLocalizedCompNaturalityDefectAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) : ZMod 2 :=
  (counterFactorizationLocalizedCompAddAt H T f g A +
      counterFactorizationLocalizedCompAddAt H T f g B) +
    (counterFactorizationLocalizedMappedSourceAddAt H T (f ≫ g) u +
      counterFactorizationLocalizedTwiceMappedSourceAddAt H T f g u)

/-- Every local compositor naturality defect is zero. -/
theorem counterFactorizationLocalizedCompNaturalityDefectAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (T : OctahedralVertex)
    {X Y : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ allMorphisms.Q.obj T)
    {A B : CounterFactorizationLocalizedFiber H X}
    (u : A ⟶ B) :
    counterFactorizationLocalizedCompNaturalityDefectAdd
        H T f g u = 0 := by
  unfold counterFactorizationLocalizedCompNaturalityDefectAdd
  exact CharTwo.add_eq_zero.mpr
    (counterFactorizationLocalizedCompAdd_pair_eq_transport_square
      H T f g u)

/-- The known middle-switch naturality square ending at H0, viewed as a local
defect. -/
noncomputable def counterFactorizationMiddleSwitchB10NaturalityDefectAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationLocalizedCompNaturalityDefectAdd
    H H0 counterMiddleSwitch (allMorphisms.Q.map b10)
    (counterFactorizationMiddleConnectorM0 H A0 A1)

/-- The known middle-switch naturality square ending at H1. -/
noncomputable def counterFactorizationMiddleSwitchB11NaturalityDefectAdd
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) : ZMod 2 :=
  counterFactorizationLocalizedCompNaturalityDefectAdd
    H H1 counterMiddleSwitch (allMorphisms.Q.map b11)
    (counterFactorizationMiddleConnectorM0 H A0 A1)

@[simp] theorem counterFactorizationMiddleSwitchB10NaturalityDefectAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationMiddleSwitchB10NaturalityDefectAdd H A0 A1 = 0 := by
  unfold counterFactorizationMiddleSwitchB10NaturalityDefectAdd
  exact counterFactorizationLocalizedCompNaturalityDefectAdd_eq_zero
    H H0 counterMiddleSwitch (allMorphisms.Q.map b10)
    (counterFactorizationMiddleConnectorM0 H A0 A1)

@[simp] theorem counterFactorizationMiddleSwitchB11NaturalityDefectAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationMiddleSwitchB11NaturalityDefectAdd H A0 A1 = 0 := by
  unfold counterFactorizationMiddleSwitchB11NaturalityDefectAdd
  exact counterFactorizationLocalizedCompNaturalityDefectAdd_eq_zero
    H H1 counterMiddleSwitch (allMorphisms.Q.map b11)
    (counterFactorizationMiddleConnectorM0 H A0 A1)

/-- The sum of the two currently available middle-switch naturality defects is
also zero. -/
theorem counterFactorizationMiddleSwitch_knownNaturalityDefectsAdd_eq_zero
    (H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem)
    (A0 : CounterFactorizationFiber H L0)
    (A1 : CounterFactorizationFiber H L1) :
    counterFactorizationMiddleSwitchB10NaturalityDefectAdd H A0 A1 +
      counterFactorizationMiddleSwitchB11NaturalityDefectAdd H A0 A1 = 0 := by
  rw [
    counterFactorizationMiddleSwitchB10NaturalityDefectAdd_eq_zero H A0 A1,
    counterFactorizationMiddleSwitchB11NaturalityDefectAdd_eq_zero H A0 A1
  ]
  exact zero_add 0

/-!
## Boundary after v3.94

The obvious local source of a crossing correction has been ruled out.

Every localized compositor naturality square has zero additive defect, and the
two existing middle-switch specializations at H0 and H1 are individually zero.
Hence the nonzero six-crossing total required by v3.93, if it exists, cannot
come from violating local naturality.

The remaining locus is global pasting/descent:

* choose several individually commuting local coherence squares;
* transport them around the two interlaced triangles;
* compare the two global pastings at the six crossings;
* measure the mismatch after all locally exact contributions cancel.

The next theorem unit should define this global-pasting comparison explicitly.
That is the natural candidate for the recursive crossing correction and keeps
the obstruction at the level of higher coherence rather than local failure.
-/

end

end KUOS.DependentOriginationLocalNaturalityDefectZeroV3_94
