import Kuu.F112.PolygonPhysicalFourBoundaryChargeFunctor
import Mathlib.Tactic.Abel

/-!
# F112-P33 — genuinely typed C60 physical-face / F55 rotation source and nonlift

P31 retained the authentic physical C60 F42 fan/disk and raw F55
hexagon rotation 3-cell as Type-valued source witnesses. Here we
separate TWO native higher-source grammars rather than presenting
two calibrations of the same F55 arrow as a historical F47 comparison:

* a FREE, explicitly newly adjoined unit-prefix 3-comparison between
  TWO distinct real F42 face fan proof trees on the first physical
  top-hexagon boundary side;
* the already constructed genuine F54/F55 six-sector disjoint-square
  3-cell between its precisely indexed raw two-axis rotation routes.

Both raw source witnesses, the whole physical F42 fan/disk and the
complete receiver calibration data are retained together. The
face-side shadow is explicitly supplied by an even-phase receiver;
it is NOT claimed to follow canonically from physical incidence.

For the north C60 source the mixed comparison needs a zero-charge,
NONZERO-phase correction. By the native F55 phase/charge parity
theorem this correction is NOT the shadow of ANY raw F55 higher cell
between the exact original source routes, nor of any arrow in the
chosen native F55 three-Hom quotient. Hence a mixed bridge requires
additional source/target data, not a secretly invented F55 arrow.

The old F47 physical-face 3-Hom and historical F68/F77 curvature
have NOT been imported or identified. No KUOS/Gray imports, added
axioms, sorry, admit or weakened public-root validation.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- Explicitly NEW Type-valued formal unit-comparison 3-source
between parallel genuine F42 physical face fan 2-proofs. The
constructor does not identify distinct raw witnesses. It does
NOT assert that the historical F47 physical 3-Hom has this grammar. -/
inductive NativePhysicalFanUnitThree :
    {s t : Site} → {p q : Zigzag s t} →
      PolygonFanRewrite p q → PolygonFanRewrite p q → Type where
  | ident {s t : Site} {p q : Zigzag s t}
      (w : PolygonFanRewrite p q) : NativePhysicalFanUnitThree w w
  | prefixIdentity {s t : Site} {p q : Zigzag s t}
      (w : PolygonFanRewrite p q) :
      NativePhysicalFanUnitThree w
        (PolygonFanRewrite.vertical (PolygonFanRewrite.ident p) w)
  | inverse {s t : Site} {p q : Zigzag s t}
      {w z : PolygonFanRewrite p q}
      (h : NativePhysicalFanUnitThree w z) :
      NativePhysicalFanUnitThree z w
  | trans {s t : Site} {p q : Zigzag s t}
      {w z v : PolygonFanRewrite p q}
      (h : NativePhysicalFanUnitThree w z)
      (k : NativePhysicalFanUnitThree z v) :
      NativePhysicalFanUnitThree w v

/-- Genuine first side of the actual C60 north-top hexagon: its
physical fan source is NOT a fictitious equality of raw paths. -/
def northHexagonFirstPhysicalFan :=
  polygonFanSector (.hexagon (.top 0)) (0 : Fin 6)
    (northHexagonNativeSector 0).2

/-- Same endpoints and real original C60 edge, with a raw identity
placed before the original F42 fan proof. The two source proofs are
different Type-valued trees. -/
def northHexagonFirstPhysicalFanWithUnit :=
  polygonFanSectorWithUnit (.hexagon (.top 0)) (0 : Fin 6)
    (northHexagonNativeSector 0).2

theorem northHexagonFirstPhysicalFan_raw_ne_unit :
    northHexagonFirstPhysicalFan ≠
      northHexagonFirstPhysicalFanWithUnit :=
  polygonFanSector_ne_withUnit (.hexagon (.top 0)) (0 : Fin 6)
    (northHexagonNativeSector 0).2

/-- A new, genuinely typed F42-face proof comparison with both
original F69 raw zigzag endpoints retained. -/
def northHexagonFirstPhysicalFaceThree :
    NativePhysicalFanUnitThree northHexagonFirstPhysicalFan
      northHexagonFirstPhysicalFanWithUnit :=
  .prefixIdentity northHexagonFirstPhysicalFan

/-- Both source and target F42 face 2-cell proof witnesses are
sound in the REAL physical C60 F69 localization. -/
theorem northHexagonFirstPhysicalFaceThree_localized :
    zigzagToLocalization
      (polygonRawSide (.hexagon (.top 0)) (0 : Fin 6)
        (northHexagonNativeSector 0).2) =
    zigzagToLocalization
      (polygonConeRawSide (.hexagon (.top 0)) (0 : Fin 6)
        (northHexagonNativeSector 0).2) :=
  northHexagonFirstPhysicalFan.localized_sound

/-- A dependent joint SOURCE packet. The physical face comparison
is between genuine F42 proof trees; the rotation higher source is
the actual six-sector F55 raw 3-cell with its two original F54 paths.
Nothing here is a Prop-erased proxy or a charge-only replacement. -/
structure NativeC60PhysicalMixedSource where
  physical : PolygonSourcePresentation (.hexagon (.top 0))
  faceStep :
    NativePhysicalFanUnitThree
      (physical.sector (0 : Fin 6) (northHexagonNativeSector 0).2)
      (PolygonFanRewrite.vertical
        (PolygonFanRewrite.ident
          (polygonRawSide (.hexagon (.top 0)) (0 : Fin 6)
            (northHexagonNativeSector 0).2))
        (physical.sector (0 : Fin 6) (northHexagonNativeSector 0).2))
  rotationStep :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.hexagon (.top 0))
      northHexagonNativeSquareLeft northHexagonNativeSquareRight

/-- An ACTUAL original physical C60 fan/disk and a distinct raw
F42 face higher proof are paired with a genuine F55 six-sector
rotation 3-cell, not with its charge or an erased Prop witness. -/
def northHexagonPhysicalMixedSource : NativeC60PhysicalMixedSource where
  physical := canonicalPolygonSource (.hexagon (.top 0))
  faceStep := northHexagonFirstPhysicalFaceThree
  rotationStep := northHexagonNativeF55SquareCell

/-- Even at the full Type-valued source level, the physical F42
primitive differs from its identity-prefixed witness. -/
theorem northHexagonPhysicalMixedSource_faceProof_noncollapse :
    northHexagonPhysicalMixedSource.physical.sector
        (0 : Fin 6) (northHexagonNativeSector 0).2 ≠
      PolygonFanRewrite.vertical
        (PolygonFanRewrite.ident
          (polygonRawSide (.hexagon (.top 0)) (0 : Fin 6)
            (northHexagonNativeSector 0).2))
        (northHexagonPhysicalMixedSource.physical.sector
          (0 : Fin 6) (northHexagonNativeSector 0).2) :=
  northHexagonFirstPhysicalFan_raw_ne_unit

/-- Every actual top-hexagon physical F42 sector in the source
is kernel-sound regardless of later target-phase calibration. -/
theorem NativeC60PhysicalMixedSource.allSectors_kernel
    (S : NativeC60PhysicalMixedSource) (i : Fin 6) :
    zigzagKernelQ.map
      (polygonRawSide (.hexagon (.top 0)) i
        (northHexagonNativeSector i).2) =
    zigzagKernelQ.map
      (polygonConeRawSide (.hexagon (.top 0)) i
        (northHexagonNativeSector i).2) :=
  (S.physical.sector i (northHexagonNativeSector i).2).kernel_sound

/-- The independent source still contains the genuine Type-valued
disk proof closing the entire physical hexagon boundary. -/
theorem NativeC60PhysicalMixedSource.disk_kernel
    (S : NativeC60PhysicalMixedSource) :
    zigzagKernelQ.map (polygonRawLoop (.hexagon (.top 0))) =
      zigzagKernelQ.map
        (Zigzag.nil
          (Site.vertex (cyclicBoundaryDart (.hexagon (.top 0)) 0))) :=
  S.physical.disk.kernel_sound

/-- The chosen physical face receiver is EXTERNAL target data:
its compatibility with the independent F55 even-phase interpretation
is a proved field rather than an arbitrary equation between raw F42
and F55 witnesses. Odd-phase rotation calibration is independent. -/
structure NativeC60PhysicalMixedCalibration where
  source : NativeC60PhysicalMixedSource
  faceValue : KuuNativeF55Shadow
  faceSound :
    faceValue = source.rotationStep.interpret
      (nativeF55EvenPhaseTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))
  rotationValue : KuuNativeF55Shadow
  rotationSound :
    rotationValue = source.rotationStep.interpret
      (nativeF55FullShadowTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))
  compareBefore : KuuNativeF55Shadow
  compareAfter : KuuNativeF55Shadow

/-- Four-boundary mixed calibration equation, with a separate
physical-face target interpretation and real native rotation
interpretation. Source proof relevance does not imply this equation. -/
def NativeC60PhysicalMixedCalibration.Calibrated
    (B : NativeC60PhysicalMixedCalibration) : Prop :=
  B.faceValue + B.compareAfter =
    B.compareBefore + B.rotationValue

def northHexagonPhysicalMixedCalibrated :
    NativeC60PhysicalMixedCalibration where
  source := northHexagonPhysicalMixedSource
  faceValue := northHexagonEvenShadow
  faceSound := rfl
  rotationValue := northHexagonOddShadow
  rotationSound := rfl
  compareBefore := 0
  compareAfter := northHexagonOddShadow - northHexagonEvenShadow

/-- Exactly the same Type-valued real C60 physical F42 face 3-source
and F55 rotation raw source, but with no extra mixed 3-comparison
correction. The frame is valid data; calibration is not automatic. -/
def northHexagonPhysicalMixedUncorrected :
    NativeC60PhysicalMixedCalibration :=
  { northHexagonPhysicalMixedCalibrated with compareAfter := 0 }

/-- The mixed square closes only after the required receiver-supplied
full-shadow comparison; proof by additive abelian-group coherence. -/
theorem northHexagonPhysicalMixedCalibrated_valid :
    northHexagonPhysicalMixedCalibrated.Calibrated := by
  change northHexagonEvenShadow +
      (northHexagonOddShadow - northHexagonEvenShadow) =
      (0 : KuuNativeF55Shadow) + northHexagonOddShadow
  abel

/-- Without extra comparison correction, the SAME physical source
cannot furnish the mixed four-boundary commutativity certificate. -/
theorem northHexagonPhysicalMixedUncorrected_not_calibrated :
    ¬ northHexagonPhysicalMixedUncorrected.Calibrated := by
  intro h
  have hEq : northHexagonEvenShadow = northHexagonOddShadow := by
    change northHexagonEvenShadow + (0 : KuuNativeF55Shadow) =
        (0 : KuuNativeF55Shadow) + northHexagonOddShadow at h
    simpa only [add_zero, zero_add] using h
  exact northHexagonEvenOddShadow_phase_ne (congrArg Prod.snd hEq)

/-- The two full comparison frames have IDENTICAL complete raw
physical fan/disk and F55 3-cell sources, yet opposite calibration
truth values. -/
theorem northHexagonPhysicalMixed_source_eq :
    northHexagonPhysicalMixedCalibrated.source =
      northHexagonPhysicalMixedUncorrected.source := rfl

/-- A source-only predicate cannot universally recover mixed
four-boundary calibration even from the entire un-erased Type-valued
physical fan/disk, unit-comparison 3-source and genuine F55 raw cell. -/
theorem northHexagonPhysicalMixed_no_source_only_calibration :
    ¬ ∃ Q : NativeC60PhysicalMixedSource → Prop,
      ∀ B : NativeC60PhysicalMixedCalibration,
        (Q B.source ↔ B.Calibrated) := by
  rintro ⟨Q, hQ⟩
  have hyes :
      Q northHexagonPhysicalMixedCalibrated.source :=
    (hQ northHexagonPhysicalMixedCalibrated).2
      northHexagonPhysicalMixedCalibrated_valid
  have hzero :
      Q northHexagonPhysicalMixedUncorrected.source := by
    rw [← northHexagonPhysicalMixed_source_eq]
    exact hyes
  exact northHexagonPhysicalMixedUncorrected_not_calibrated
    ((hQ northHexagonPhysicalMixedUncorrected).1 hzero)

/-- On the ACTUAL genuine C60 hexagon the required face-to-rotation
comparison correction has ZERO signed integer pentagon/square charge. -/
theorem northHexagonPhysicalMixedCorrection_charge_zero :
    northHexagonPhysicalMixedCalibrated.compareAfter.1 =
      ((0 : Int), (0 : Int)) :=
  northHexagonFourCorrection_charge_zero

/-- But its independent ZMod 2 exchange phase is NONZERO. The mixed
bridge cannot forget it without changing the four-boundary square. -/
theorem northHexagonPhysicalMixedCorrection_phase_ne_zero :
    northHexagonPhysicalMixedCalibrated.compareAfter.2 ≠
      (0 : ZMod 2) :=
  northHexagonFourCorrection_phase_ne_zero

/-- The extra pure-phase mixed correction is NOT the shadow of a
native nine-constructor F55 raw 3-cell with the real hexagon F54
source/target routes. By native F55 parity, a zero square charge
forces zero phase. This is a strict local nonlift into the independent
F55 syntax, NOT a historical original F68/F77 obstruction. -/
theorem northHexagonPhysicalMixedCorrection_no_nativeF55_raw
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.hexagon (.top 0))
      northHexagonNativeSquareLeft northHexagonNativeSquareRight) :
    cell.nativeShadow ≠
      northHexagonPhysicalMixedCalibrated.compareAfter := by
  intro h
  have hcharge : cell.nativeShadow.1.2 = (0 : Int) := by
    have hs := congrArg
      (fun z : KuuNativeF55Shadow => z.1.2) h
    exact hs.trans
      (congrArg Prod.snd
        northHexagonPhysicalMixedCorrection_charge_zero)
  have hphase : cell.nativeShadow.2 = (0 : ZMod 2) := by
    have hcast :
        ((cell.nativeShadow.1.2 : Int) : ZMod 2) =
          (0 : ZMod 2) := by
      rw [hcharge]
      rfl
    exact cell.phase_squareParity.symm.trans hcast
  have hcorrect : northHexagonPhysicalMixedCalibrated.compareAfter.2 =
      (0 : ZMod 2) :=
    (congrArg Prod.snd h).symm.trans hphase
  exact northHexagonPhysicalMixedCorrection_phase_ne_zero hcorrect

/-- The same local obstruction persists in the actual chosen
full-shadow Mathlib F55 three-Hom quotient of real C60 rotations.
No existing original-shaped native F55 3-arrow can secretly serve as
the physical face/rotation pure-phase comparison bridge. -/
theorem northHexagonPhysicalMixedCorrection_no_nativeF55_hom
    (f : NativeF55ThreeHom
      northHexagonNativeSquareLeft northHexagonNativeSquareRight) :
    nativeF55ThreeEval f ≠
      northHexagonPhysicalMixedCalibrated.compareAfter := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact northHexagonPhysicalMixedCorrection_no_nativeF55_raw raw

#print axioms NativePhysicalFanUnitThree
#print axioms northHexagonFirstPhysicalFan_raw_ne_unit
#print axioms northHexagonFirstPhysicalFaceThree
#print axioms northHexagonFirstPhysicalFaceThree_localized
#print axioms NativeC60PhysicalMixedSource
#print axioms northHexagonPhysicalMixedSource_faceProof_noncollapse
#print axioms NativeC60PhysicalMixedSource.allSectors_kernel
#print axioms NativeC60PhysicalMixedSource.disk_kernel
#print axioms NativeC60PhysicalMixedCalibration
#print axioms northHexagonPhysicalMixedCalibrated_valid
#print axioms northHexagonPhysicalMixedUncorrected_not_calibrated
#print axioms northHexagonPhysicalMixed_source_eq
#print axioms northHexagonPhysicalMixed_no_source_only_calibration
#print axioms northHexagonPhysicalMixedCorrection_charge_zero
#print axioms northHexagonPhysicalMixedCorrection_phase_ne_zero
#print axioms northHexagonPhysicalMixedCorrection_no_nativeF55_raw
#print axioms northHexagonPhysicalMixedCorrection_no_nativeF55_hom

end
end Kuu.F112.Physical
