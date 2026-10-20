import Kuu.F112.PolygonNativeHistoricalProofBoundary
import Kuu.F112.PolygonNativeF55PhaseChoice

/-!
# F112-P26 — two genuinely typed local descent obstructions

First obstruction (proof relevance): an actual native F41 split and
insertNil raw trace share their old-shaped Prop-step evidence, despite
being different Type-valued witnesses. Even the predicate that singles
out the primitive split cannot descend through this evidence erasure.
The result holds in the genuinely constructed north C60 Site frame.

Second obstruction (phase calibration): the same native C60 hexagon
F55 six-sector square has identical signed pentagon/square charges in
the independent even- and odd-phase receivers, but differing ZMod2
phases. There is NO single charge-only decoder compatible with BOTH
independently valid receivers. This is a precise failure of local
charge-only descent, not an identification with the historical F55
nonlift or F68/F77 braided curvature.

No Gray or historical KUOS imports; no extra axioms or sorry.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- The predicate distinguishing the raw split primitive from a
different, same-endpoint raw insertion cannot be a predicate of
erased historical-shaped Prop evidence, even at exact depth one. -/
theorem nativeF41DoubleNil_splitPredicate_noDescent
    {x y : C} (p : KuuNativeBlocks x y) :
    ¬ ∃ (descends : KuuNativeHistoricalAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) → Prop),
      ∀ h : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p),
        (descends h.toHistorical ↔ h = nativeF41DoubleNilSplitTrace p) := by
  rintro ⟨descends, hdesc⟩
  have hsplit :
      descends (nativeF41DoubleNilSplitTrace p).toHistorical :=
    (hdesc (nativeF41DoubleNilSplitTrace p)).2 rfl
  have hinsert :
      descends (nativeF41DoubleNilInsertTrace p).toHistorical := by
    rw [← nativeF41DoubleNil_toHistorical_eq p]
    exact hsplit
  have heq :
      nativeF41DoubleNilInsertTrace p =
        nativeF41DoubleNilSplitTrace p :=
    (hdesc (nativeF41DoubleNilInsertTrace p)).1 hinsert
  exact nativeF41DoubleNilSplitTrace_ne_insert p heq.symm

/-- The evidence non-descent arises on the genuine north pentagon
physical C60 Site two-axis frame, not a hypothetical source. -/
theorem northPentagon_splitPredicate_noDescent :
    ¬ ∃ (descends : KuuNativeHistoricalAxisTrace 1
        (nativeF41DoubleNilSource
          northPentagonNativeDualAxisFrame.firstAxis)
        (nativeF41DoubleNilTarget
          northPentagonNativeDualAxisFrame.firstAxis) → Prop),
      ∀ h : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource
          northPentagonNativeDualAxisFrame.firstAxis)
        (nativeF41DoubleNilTarget
          northPentagonNativeDualAxisFrame.firstAxis),
        (descends h.toHistorical ↔
          h = nativeF41DoubleNilSplitTrace
            northPentagonNativeDualAxisFrame.firstAxis) :=
  nativeF41DoubleNil_splitPredicate_noDescent
    northPentagonNativeDualAxisFrame.firstAxis

/-- The even-phase interpretation of the real six-sector C60
hexagon native F55 square in its original Site categories. -/
def northHexagonEvenShadow : KuuNativeF55Shadow :=
  northHexagonNativeF55SquareCell.interpret
    (nativeF55EvenPhaseTarget (D := Site) (E := Site)
      (.hexagon (.top 0)))

/-- The independently odd-calibrated interpretation of exactly
the SAME raw six-sector C60 F55 square. -/
def northHexagonOddShadow : KuuNativeF55Shadow :=
  northHexagonNativeF55SquareCell.interpret
    (nativeF55FullShadowTarget (D := Site) (E := Site)
      (.hexagon (.top 0)))

/-- Signed generator charges agree, on precisely the same raw
C60 source 3-cell rather than an assumed abstract shadow object. -/
theorem northHexagonEvenOddShadow_charge_eq :
    northHexagonEvenShadow.1 = northHexagonOddShadow.1 :=
  northHexagonNativeF55Square_phase_not_forced_by_charge.1

/-- The same C60 source is assigned DIFFERENT odd braided phase
by the two independently valid target calibrations. -/
theorem northHexagonEvenOddShadow_phase_ne :
    northHexagonEvenShadow.2 ≠ northHexagonOddShadow.2 :=
  northHexagonNativeF55Square_phase_not_forced_by_charge.2

/-- An attempted common phase recovery function from the signed
integral pentagon/square charge, simultaneously compatible with
both fully typed F55 target receivers for the actual C60 square. -/
structure NorthHexagonSharedChargeOnlyPhaseDescent where
  decode : (Int × Int) → ZMod 2
  even_agrees :
    decode (northHexagonEvenShadow.1) = northHexagonEvenShadow.2
  odd_agrees :
    decode (northHexagonOddShadow.1) = northHexagonOddShadow.2

/-- Nontrivial LOCAL CHARGE-ONLY DESCENT OBSTRUCTION: no such
universal charge-to-phase function is compatible with both valid
real-source receivers, since the charge is equal and phase unequal.
This does not conflate the original F55/F68/F77 higher obstruction
with integral homology or force the native odd target to be canonical. -/
theorem northHexagon_noSharedChargeOnlyPhaseDescent :
    ¬ Nonempty NorthHexagonSharedChargeOnlyPhaseDescent := by
  rintro ⟨h⟩
  have hphase :
      northHexagonEvenShadow.2 = northHexagonOddShadow.2 := by
    calc
      northHexagonEvenShadow.2 =
          h.decode (northHexagonEvenShadow.1) := h.even_agrees.symm
      _ = h.decode (northHexagonOddShadow.1) :=
          congrArg h.decode northHexagonEvenOddShadow_charge_eq
      _ = northHexagonOddShadow.2 := h.odd_agrees
  exact northHexagonEvenOddShadow_phase_ne hphase

#print axioms nativeF41DoubleNil_splitPredicate_noDescent
#print axioms northPentagon_splitPredicate_noDescent
#print axioms northHexagonEvenOddShadow_charge_eq
#print axioms northHexagonEvenOddShadow_phase_ne
#print axioms northHexagon_noSharedChargeOnlyPhaseDescent

end
end Kuu.F112.Physical
