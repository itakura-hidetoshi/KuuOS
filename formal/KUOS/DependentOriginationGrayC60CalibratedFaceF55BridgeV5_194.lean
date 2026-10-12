import KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
import KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193

namespace KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60BraidedThreeSectorV5_188
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F46 / v5.194 — native categorical FACE/F55 bridge with exact calibration

The original C60 face-3-Hom category and F54/F55 original rotation
3-Hom category are mathematically DIFFERENT dependent source categories.
F59-F40 built the TRUE 182-position C60 categorical Gray target,
and F59-F44/45 built the genuine 3-Hom categories plus faithful
whiskering functors on BOTH original source systems.

Here a second independently type-correct LOCALIZATION FUNCTOR puts
any original C60 *polygonal FACE* source 3-morphism at exactly one
real C60 physical edge site, just as F59-F46's new original
F54/F55 source functor does, retaining all native integer charges
and the independent ZMod2 interchanger phase. Both functors now
reach exactly the SAME 182-site GrayGrade category.

At the genuine north pentagon, take the ORIGINAL five-edge face
2-morphism twice. Its *C60 face* three-cell interchange is
(0,0; phase1). At the actual adjacent north around edge,
the genuine ORIGINAL F54/F55 flag square source 3-morphism is
(0,1; phase1). These are not identified: the source C60
polygonal face 2-cell and original F54 rotation 2-cell
are not the same typed source.

Instead construct a UNIQUE *target receiver calibration*
of full native type (0,1;phase0) such that the
C60 face interchanger PLUS calibration equals the genuine
edge-localized F55 source square, in ALL integer and phase
components. The actual original C60 geometric four-flag
incidence carrier is proved and its FIRST polygonal face
really is the north pentagon.

A key boundary insight: the native calibration is NOT an image
of any genuine original F55 PresentedCell on any specified
fixed F54 endpoint routes, because ALL NINE original F55
source constructors obey the already proved F55 phase lock
phase = square-charge mod2. Our receiver has phase0 but
square charge1. Thus a full nondegenerate C60 Gray 3-functor
cannot identify the two source 3-cell types using phase alone:
a genuinely NEW, correctly globular mixed comparison
generator/receiver or a stronger source construction is
required. We record its EXACT value and uniqueness rather
than postulating a missing source 3-cell or a fake square face.

This is an honest physical 3-Hom cospan into the same true native
categorical target, NOT a completed globally nondegenerate
Gray 3-functor. Stage-II omega and historical Wang Bi semantics
remain distinct from this verified algebraic receiver.
-/

/-! ## I. C60 face 3-Hom localizes into its ACTUAL physical edge -/

/-- ORIGINAL C60 face-2-cell based 3-Hom Mathlib functor, with
exact FULL native Gray image only at the chosen real C60
edge, and true identity at the 181 other original sites. -/
def c60F46EdgeLocalizedFaceFunctor
    (edge : TruncatedIcosahedralEdge)
    {a b : IcosahedralDart} {p q : Quiver.Path a b} :
    C60F42PresentedFaceCell p q ⥤ C60GrayIndexedTwoThreeCategory where
  obj _ := c60GrayPhysicalUnit
  map := fun {_ _} f site =>
    if site = C60GrayPhysicalSite.edge edge then
      c60F44FaceThreeGrayFunctor.map f
    else (𝟙 GrayGrade.unit)
  map_id := by
    intro faceCell
    funext site
    by_cases hs : site = C60GrayPhysicalSite.edge edge
    · subst site
      simp only [CategoryTheory.Pi.id_apply]
      exact c60F44FaceThreeGrayFunctor.map_id faceCell
    · simp only [CategoryTheory.Pi.id_apply, if_neg hs]
      rfl
  map_comp := by
    intro α β γ f g
    funext site
    by_cases hs : site = C60GrayPhysicalSite.edge edge
    · subst site
      simp only [CategoryTheory.Pi.comp_apply]
      exact c60F44FaceThreeGrayFunctor.map_comp f g
    · simp only [CategoryTheory.Pi.comp_apply, if_neg hs]
      exact (Category.id_comp (𝟙 GrayGrade.unit)).symm

theorem c60F46EdgeLocalizedFace_atRealEdge
    (edge : TruncatedIcosahedralEdge)
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    ((c60F46EdgeLocalizedFaceFunctor edge).map f) (.edge edge) =
      c60F44FaceThreeGrayFunctor.map f := by
  simp [c60F46EdgeLocalizedFaceFunctor]

theorem c60F46EdgeLocalizedFace_faithful
    (edge : TruncatedIcosahedralEdge)
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (h : (c60F46EdgeLocalizedFaceFunctor edge).map f =
      (c60F46EdgeLocalizedFaceFunctor edge).map g) : f = g := by
  have he := congrArg
    (fun m : (c60F46EdgeLocalizedFaceFunctor edge).obj α ⟶
       (c60F46EdgeLocalizedFaceFunctor edge).obj β =>
      m (.edge edge)) h
  change ((c60F46EdgeLocalizedFaceFunctor edge).map f) (.edge edge) =
    ((c60F46EdgeLocalizedFaceFunctor edge).map g) (.edge edge) at he
  rw [c60F46EdgeLocalizedFace_atRealEdge,
      c60F46EdgeLocalizedFace_atRealEdge] at he
  exact c60F44FaceThreeGrayFunctor_faithful he

/-! ## II. Exact, unique native F55-to-C60 face receiver -/

/-- The missing boundary-comparison RECEIVER as an explicit
independent native F59 neutral 3-cell. Its FIRST and SECOND
integer F58 charges are (0,1), but its independent phase is
ZERO. This is NOT asserted to be a genuine original F55 cell. -/
def c60F46FaceF55ComparisonCalibration : GradedThreeCell 0 0 :=
  ⟨rfl, (0, 1), 0⟩

theorem c60F46FaceF55ComparisonCalibration_components :
    c60F46FaceF55ComparisonCalibration.charge =
      ((0 : Int), (1 : Int)) ∧
    c60F46FaceF55ComparisonCalibration.phase =
      (0 : ZMod 2) := ⟨rfl, rfl⟩

/-- The independent C60 north pentagon exchange (0,0;1)
PLUS the precise native comparison receiver (0,1;0) is
the ACTUAL original F55 square generator (0,1;1).
Equality is checked in ALL three independent target
coordinates, not by projecting to phase or square charge. -/
theorem c60F46NativeNorthFaceF55_calibrated :
    c60F43NorthPentagonInterchange.toNative +
      c60F46FaceF55ComparisonCalibration =
        originalF55BraidedSquareGenerator := by
  apply GradedThreeCell.ext
  · change ((0 : Int), (0 : Int)) + ((0 : Int), (1 : Int)) =
      ((0 : Int), (1 : Int))
    simp
  · change (1 : ZMod 2) + (0 : ZMod 2) = (1 : ZMod 2)
    simp

/-- This receiver is uniquely determined by an EXACT full
Gray 3-cell equality, not by an arbitrary philosophic
identification of the two distinct original source
higher cells or phase-only compensation. -/
theorem c60F46NativeNorthFaceF55_calibration_unique
    (receiver : GradedThreeCell 0 0) :
    (c60F43NorthPentagonInterchange.toNative + receiver =
        originalF55BraidedSquareGenerator) ↔
      receiver = c60F46FaceF55ComparisonCalibration := by
  constructor
  · intro h
    have hh :
        c60F43NorthPentagonInterchange.toNative + receiver =
          c60F43NorthPentagonInterchange.toNative +
            c60F46FaceF55ComparisonCalibration :=
      h.trans c60F46NativeNorthFaceF55_calibrated.symm
    exact add_left_cancel hh
  · rintro rfl
    exact c60F46NativeNorthFaceF55_calibrated

/-! ## III. An ACTUAL north C60 physical flag site comparison -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineNorthC60Flag
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- This is a real original north C60 pentagon/hexagon incidence
edge square, certified independently of the original F54/F55
rotation-square 3-cell decoration. It is NOT a C60 quadrilateral
polygonal surface face. -/
theorem c60F46NorthFlagSquare_firstOriginalFace :
    (c60F46PhysicalFourFlagSquare
        (.around ⟨.north, .s0⟩)).firstFace =
      (.aroundVertex .north) := rfl

/-- The genuine original C60 north-pentagon F42 face 2-cell
exchange is localized at the SAME physical north around
edge where the real F54/F55 3-cell is localized. Their
images are related by the unique independent native receiver.
This is a constructive SAME-SITE comparison with correct
typed original source on BOTH sides, not a fake equality
of their distinct source 2-cell boundaries. -/
theorem c60F46NorthActualFlag_sitewise_calibrated :
    ((c60F46EdgeLocalizedFaceFunctor
        (.around ⟨.north, .s0⟩)).map
       (c60F44FaceThreeOf c60F43NorthPentagonInterchange))
          (.edge (.around ⟨.north, .s0⟩)) +
      c60F46FaceF55ComparisonCalibration =
    ((c60F46EdgeLocalizedF55Functor
        (.around ⟨.north, .s0⟩)).map
       (c60F46PhysicalFlagOriginalF55Arrow
          t₁ t₂ left right (.around ⟨.north, .s0⟩)))
          (.edge (.around ⟨.north, .s0⟩)) := by
  rw [c60F46EdgeLocalizedFace_atRealEdge,
      c60F46EveryActualFlagSquare_localizedF55]
  rw [c60AllNinetyGrayCell_eq]
  exact c60F46NativeNorthFaceF55_calibrated

/-- For the ACTUAL north C60 physical source square, the native
receiver is the UNIQUE higher target 3-cell making the full
integer-charge AND braided phase comparison commute. -/
theorem c60F46NorthActualFlag_sitewise_unique
    (receiver : GradedThreeCell 0 0) :
    (((c60F46EdgeLocalizedFaceFunctor
        (.around ⟨.north, .s0⟩)).map
       (c60F44FaceThreeOf c60F43NorthPentagonInterchange))
          (.edge (.around ⟨.north, .s0⟩)) +
      receiver =
    ((c60F46EdgeLocalizedF55Functor
        (.around ⟨.north, .s0⟩)).map
       (c60F46PhysicalFlagOriginalF55Arrow
          t₁ t₂ left right (.around ⟨.north, .s0⟩)))
          (.edge (.around ⟨.north, .s0⟩))) ↔
       receiver = c60F46FaceF55ComparisonCalibration := by
  rw [c60F46EdgeLocalizedFace_atRealEdge,
      c60F46EveryActualFlagSquare_localizedF55,
      c60AllNinetyGrayCell_eq]
  exact c60F46NativeNorthFaceF55_calibration_unique receiver

end GenuineNorthC60Flag

/-! ## IV. Exact original-F55 source condition on the receiver -/

/-- The independent native receiver has phase ZERO while
square charge is ONE: it is NOT phase-locked according to
the actual original all-NINE-F55 source charge law.
A new correctly typed mixed source 3-cell is required to
realize this receiver, rather than calling the native
receiver an original F55 source cell. -/
theorem c60F46FaceF55ComparisonCalibration_notOriginalF55Locked :
    c60F46FaceF55ComparisonCalibration ∉ c60F55PhaseLocked := by
  intro h
  change (0 : ZMod 2) = ((1 : Int) : ZMod 2) at h
  exact (by decide : (0 : ZMod 2) ≠ 1) h

/-- No ORIGINAL nine-constructor proof-relevant F55 source
3-cell, with ANY exact fixed original F54 endpoints, has
this mixed native receiver value. This is the precise
source-level limitation, not a refusal to construct the
genuine native target comparison above. -/
theorem c60F46FaceF55ComparisonCalibration_hasNoOriginalF55Source
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last} :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F55SourceNative cell =
        c60F46FaceF55ComparisonCalibration := by
  rintro ⟨cell, hcell⟩
  have hm := c60F55SourceNative_mem cell
  rw [hcell] at hm
  exact c60F46FaceF55ComparisonCalibration_notOriginalF55Locked hm

#print axioms c60F46EdgeLocalizedFaceFunctor
#print axioms c60F46EdgeLocalizedFace_faithful
#print axioms c60F46FaceF55ComparisonCalibration_components
#print axioms c60F46NativeNorthFaceF55_calibrated
#print axioms c60F46NativeNorthFaceF55_calibration_unique
#print axioms c60F46NorthFlagSquare_firstOriginalFace
#print axioms c60F46NorthActualFlag_sitewise_calibrated
#print axioms c60F46NorthActualFlag_sitewise_unique
#print axioms c60F46FaceF55ComparisonCalibration_notOriginalF55Locked
#print axioms c60F46FaceF55ComparisonCalibration_hasNoOriginalF55Source

end
end KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
