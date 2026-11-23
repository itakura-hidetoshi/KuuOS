import Kuu.F112.PolygonNativeC60NorthWuxingK5ActualFiveStageGauge
import Mathlib.Tactic

/-!
# Exact north-C60 five-phase chart → original physical F45 sector equivalence

This is an actual finite bijection from Qi's FivePhase = ZMod 5 (for an
arbitrary selected phase chart) to the five original physical north-C60
polygon boundary sectors used by the original K5 five F45 leaves.

The only bridge claimed is on the finite five-element CARRIER.
It does NOT equate Qi phase dynamics with actual graph dynamics,
physical 182-site gauge coboundaries with free-word conjugation, or
noncommutative higher-cell descent with a scalar fivefold rotation.
-/

namespace Kuu.F112.Physical

open KUOS.Architecture
open KUOS.Architecture.WuxingCyclicPaths
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Exactly the original five north C60 physical polygon sectors.
No replacement graph or extra side is introduced. -/
def northK5SectorOfSlot : Slot → PolygonBoundarySector (.pentagon .north)
  | .s0 => firstFourPolygonSector (.pentagon .north) 0
  | .s1 => firstFourPolygonSector (.pentagon .north) 1
  | .s2 => firstFourPolygonSector (.pentagon .north) 2
  | .s3 => firstFourPolygonSector (.pentagon .north) 3
  | .s4 => northK5FifthSector

/-- Two different original physical slots have distinct K5 F45 sectors. -/
theorem northK5SectorOfSlot_injective :
    Function.Injective northK5SectorOfSlot := by
  decide

/-- Every original north pentagon boundary sector is one of the five. -/
theorem northK5SectorOfSlot_surjective :
    Function.Surjective northK5SectorOfSlot := by
  decide

/-- Exact compatibility of the Qi phase chart with original physical
C60 sectors. Only the fivefold carrier is identified, NOT gauges. -/
def northK5PhaseSectorEquiv (frame : NativeC60FivePhaseGauge) :
    FivePhase ≃ PolygonBoundarySector (.pentagon .north) :=
  Equiv.ofBijective
    (fun phase => northK5SectorOfSlot (nativeC60GaugeSlot frame .north phase))
    ⟨by
      intro p q h
      exact nativeC60GaugeSlot_injective frame .north
        (northK5SectorOfSlot_injective h),
     by
      intro sector
      rcases northK5SectorOfSlot_surjective sector with ⟨slot, hs⟩
      rcases nativeC60GaugeSlot_surjective frame .north slot with ⟨phase, hp⟩
      exact ⟨phase, by simpa only [hp] using hs⟩⟩

/-- Distinct +1 (相生) and +2 (相剋) moves remain distinct *physical*
north-C60 boundary sectors after any chosen chart reframe. -/
theorem northK5PhaseSector_sheng_ne_ke
    (frame : NativeC60FivePhaseGauge) (phase : FivePhase) :
    northK5PhaseSectorEquiv frame (generationPhase phase) ≠
      northK5PhaseSectorEquiv frame (controlPhase phase) := by
  intro h
  have hp : generationPhase phase = controlPhase phase :=
    (northK5PhaseSectorEquiv frame).injective h
  have heq : phase + (1 : FivePhase) = phase + 2 := by
    simpa only [generationPhase, controlPhase] using hp
  have h12 : (1 : FivePhase) = 2 := add_left_cancel heq
  exact (by decide : (1 : FivePhase) ≠ 2) h12

/-- All 14 original K5 bracketings have exactly the source sectors
covered by the five-phase chart, without forgetting their F45 histories
or asserting any higher filler. -/
theorem northK5ActualFiveSectors_phase_chart_surjective
    (frame : NativeC60FivePhaseGauge) (i : Fin 14) :
    (northK5TypedVertex i).2.2.sectors =
      [firstFourPolygonSector (.pentagon .north) 0,
       firstFourPolygonSector (.pentagon .north) 1,
       firstFourPolygonSector (.pentagon .north) 2,
       firstFourPolygonSector (.pentagon .north) 3,
       northK5FifthSector] ∧
    Function.Surjective (northK5PhaseSectorEquiv frame) := by
  exact ⟨northK5TypedVertex_physical_five_sectors i,
    (northK5PhaseSectorEquiv frame).surjective⟩

#print axioms northK5SectorOfSlot_injective
#print axioms northK5SectorOfSlot_surjective
#print axioms northK5PhaseSectorEquiv
#print axioms northK5PhaseSector_sheng_ne_ke
#print axioms northK5ActualFiveSectors_phase_chart_surjective

end
end Kuu.F112.Physical
