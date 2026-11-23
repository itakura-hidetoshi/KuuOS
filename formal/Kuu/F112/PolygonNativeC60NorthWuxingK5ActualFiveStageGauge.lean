import Kuu.F112.PolygonNativeC60NorthWuxingK5TripleGaugeBridge
import Kuu.F112.PolygonNativeF55P94DK5FiveStageTypedShell
import Mathlib.Tactic

/-!
# Original north C60 F45 five-stage, five-phase and genuine typed K5

Use the five already constructed original north C60 F45 leaves, including
the physical fifth sector, instead of assuming the five input witnesses.
The physical Qi, incidence and typed K5 gauge actions remain distinct.
The two new statements do NOT equate them or construct a 14D/15D filler,
a global descent or a new C60 face.
-/
namespace Kuu.F112.Physical
open CategoryTheory
open KUOS.Architecture
open KUOS.Architecture.WuxingCyclicPaths
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uA
variable {A : Type uA} [AddCommGroup A]

/-- Original concrete F45 fivefold instantiation of the certified
C60 north Wuxing/K5 gauge obstruction, not an assumed generic stage. -/
theorem nativeC60NorthWuxingK5_actualFiveStage_obstruction
    (frame : NativeC60FivePhaseGauge)
    (phase : FivePhase)
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    (g : NativeF55P94CWord) :
    slotIndex (nativeC60GaugeSlot frame .north (generationPhase phase)) =
      slotIndex (nativeC60GaugeSlot frame .north phase) + 1 ∧
    slotIndex (nativeC60GaugeSlot frame .north (controlPhase phase)) =
      slotIndex (nativeC60GaugeSlot frame .north phase) + 2 ∧
    nativeC60FaceGaugeCurvature
        (nativeC60GaugeTransform field phi) (.pentagon .north) =
      nativeC60FaceGaugeCurvature field (.pentagon .north) ∧
    nativeF55P94CWordToShadow
      (nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage
        northNativeF45FifthStage)) = 0 ∧
    nativeK5NaturalityCount
      (nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage
        northNativeF45FifthStage)) = 1 ∧
    nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage
        northNativeF45FifthStage)
        ∉ nativeK5P94ATypedNormalClosure Site Site := by
  exact nativeC60NorthWuxingK5_threeGauge_obstructions
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage
    northNativeF45FifthStage frame phase field phi g

/-- Physical five sectors are retained for all fourteen original
K5 bracketings, alongside the genuine typed nine-face obstruction. -/
theorem nativeC60NorthWuxingK5_actualFiveSectors_and_gauge
    (i : Fin 14)
    (frame : NativeC60FivePhaseGauge)
    (phase : FivePhase)
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    (g : NativeF55P94CWord) :
    (northK5TypedVertex i).2.2.sectors =
      [firstFourPolygonSector (.pentagon .north) 0,
       firstFourPolygonSector (.pentagon .north) 1,
       firstFourPolygonSector (.pentagon .north) 2,
       firstFourPolygonSector (.pentagon .north) 3,
       northK5FifthSector] ∧
    nativeK5NaturalityCount
      (nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage
        northNativeF45FifthStage)) = 1 ∧
    nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage
        northNativeF45FifthStage)
        ∉ nativeK5P94ATypedNormalClosure Site Site := by
  have h := nativeC60NorthWuxingK5_actualFiveStage_obstruction
    frame phase field phi g
  exact ⟨northK5TypedVertex_physical_five_sectors i, h.2.2.2.2⟩

#print axioms nativeC60NorthWuxingK5_actualFiveStage_obstruction
#print axioms nativeC60NorthWuxingK5_actualFiveSectors_and_gauge

end
end Kuu.F112.Physical
