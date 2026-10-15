import KUOS.DependentOriginationC60KuuArbitraryPhysicalRefinementTowersV5_273

namespace KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuObservedGluingOriginalPhaseCurvatureV5_268
open KUOS.DependentOriginationC60KuuPhaseReconstructionObstructionV5_269
open KUOS.DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270
open KUOS.DependentOriginationC60KuuArbitraryPhysicalRefinementTowersV5_273
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.274 / F112 second stage — independent ORIGINAL F42 face-site source

The F108 both-face model already used TWO DIFFERENT genuine C60
pentagon/hexagon generators, but assigned both physical upper face
SITES a single common F42 horizontal composite. F112/v5.273 later
proved arbitrarily deep ACTUAL F106 physical restrictions and F77
observed Cech histories; that cannot by itself restore source data.

Here two independent, proof-relevant original F42 cells are assigned
to the TWO ACTUAL, DIFFERENT face sites at an original physical edge.
Each has its own correctly typed original face-base loop boundary.
An actual C60 base-to-base original Quiver.Path moves only the second
cell into the first cell's base for constructing a well-typed F51
interchanger between distinct horizontal ORIGINAL F42 expressions.

The odd-degree hypotheses are EXPLICIT for arbitrary chosen F42 cells,
and PROVED for the canonical original two polygon generators.
We prove that every such genuine two-face source comparison has:
  - real original F42 source/target boundaries, not synthetic faces;
  - TWO zero integer charges but independent phase ONE in original F51;
  - a nonidentity full-phase native Gray morphism;
  - identity image after the explicitly intentional F77 projection.

Finally keep the ORIGINAL, separately typed F54 rotation routes and
F55 flag-square source arrow on the same true physical edge. Its
independent F68 north pentagon second signed curvature is -5, nonzero,
and forbids uncorrected global vertex-gauge descent, despite the
arbitrary finite F77-observed physical refinement coherence.

This is not a source-wide F42/F54/F55 three-descent theorem.
In particular it does not turn an F51 exchange and an original F55
square into one interchangeable 3-Hom, or assert that different
original face-base path types are definitionally equal.
-/

/-- EXACT original F42 raw source type at one REAL incident
pentagon/hexagon site: distinct sides retain their different
original Quiver.Path boundaries and face bases. -/
def C60F112OriginalFaceSlot
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (side : Bool) : Type :=
  C60F42PresentedFaceCell
    (c60F41PhysicalFaceBoundaryLoop
      (c60F48AdjacentRealFace (C.edge i) side)).2
    Quiver.Path.nil

/-- A new independent ORIGINAL F42 label at EACH of two genuine
face sites, with native odd degree separately justified.
Second base is not identified with the first; only the
typed original bridge will subsequently connect their paths. -/
structure C60F112IndependentOddFacePair
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) where
  first : C60F112OriginalFaceSlot C i false
  second : C60F112OriginalFaceSlot C i true
  first_odd : c60F43FaceDegree first = (1 : ZMod 2)
  second_odd : c60F43FaceDegree second = (1 : ZMod 2)

/-- Two real ORIGINAL polygonal source generators, with their
own F42 path witnesses, satisfy the separate odd-degree laws. -/
def c60F112CanonicalOddFacePair
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F112IndependentOddFacePair C i where
  first := c60F48AdjacentFaceTwoCell (C.edge i) false
  second := c60F48AdjacentFaceTwoCell (C.edge i) true
  first_odd := rfl
  second_odd := rfl

/-- Each separate original face site is an ACTUAL F106 incidence
object, not merely a boolean substitute for the surface. -/
def c60F112PhysicalFaceSite
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (side : Bool) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) :=
  c60F108BothFaceStarPolygon C i side

/-- The physical edge's two original upper face sites are DISTINCT
already in the genuine F69/F106 geometric category. -/
theorem c60F112PhysicalFaceSites_distinct
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    c60F112PhysicalFaceSite C i false ≠
      c60F112PhysicalFaceSite C i true := by
  intro h
  have hv := congrArg Subtype.val h
  change
    C60F69PhysicalCellSite.face
      (c60F48AdjacentRealFace (C.edge i) false) =
    C60F69PhysicalCellSite.face
      (c60F48AdjacentRealFace (C.edge i) true) at hv
  injection hv with hf
  exact (c60F108BothPolygonFaces_distinct C i) hf

/-- The second ORIGINAL face site is moved to the first face's
base by the genuine C60 prior/bridge path, never by an assumed
equality between different raw polygon-loop boundaries. -/
def c60F112SecondFaceBridged
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    C60F42PresentedFaceCell
      ((C.bridge i).comp
        (c60F41PhysicalFaceBoundaryLoop
          (c60F48AdjacentRealFace (C.edge i) true)).2)
      ((C.bridge i).comp Quiver.Path.nil) :=
  .whiskerLeft (C.bridge i) P.second

/-- First-original-site then second-original-site pasting,
whiskered to the REAL physical edge endpoint path pair. -/
def c60F112IndependentPairLeft
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    C60F42PresentedFaceCell
      ((c60F108BothFacePatchFamily C).p i)
      ((c60F108BothFacePatchFamily C).q i) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      (P.first.horizontalLeftFirst (c60F112SecondFaceBridged C i P)))
    (C.suffix i)

/-- Independent second-first source F42 expression, not an
unconditional equation between two raw original source cells. -/
def c60F112IndependentPairRight
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    C60F42PresentedFaceCell
      ((c60F108BothFacePatchFamily C).p i)
      ((c60F108BothFacePatchFamily C).q i) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      (P.first.horizontalRightFirst (c60F112SecondFaceBridged C i P)))
    (C.suffix i)

/-- TRUE original F43/F51 interchanger between the two
different original F42 site labels, retaining ALL raw
source boundary witnesses even before the quotient. -/
def c60F112IndependentPairExchange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    C60F51PresentedThreeCell
      (c60F112IndependentPairLeft C i P)
      (c60F112IndependentPairRight C i P) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      (.original
        (.interchange P.first (c60F112SecondFaceBridged C i P))))
    (C.suffix i)

/-- ORIGINAL proof-relevant F51 categorical 3-Hom, not a
bare equality of quotient charges or untyped native cell. -/
def c60F112IndependentPairExchangeHom
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (⟨c60F112IndependentPairLeft C i P⟩ :
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i)) ⟶
    (⟨c60F112IndependentPairRight C i P⟩ :
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i)) :=
  c60F51Of (c60F112IndependentPairExchange C i P)

/-- ALL separate degree-one source site labels retain ZERO
independent integer F51 exchange charge but phase ONE. This
is an ORIGINAL F43 computation, not an F77 assertion. -/
theorem c60F112IndependentPairExchange_components
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F51Eval (c60F112IndependentPairExchangeHom C i P)).charge =
        (0 : Int × Int) ∧
    (c60F51Eval (c60F112IndependentPairExchangeHom C i P)).phase =
        (1 : ZMod 2) := by
  constructor
  · rfl
  · change
      c60F43FaceDegree P.first * c60F43FaceDegree P.second =
        (1 : ZMod 2)
    rw [P.first_odd, P.second_odd]
    simp

/-- Although the canonical two-face model is a special case,
the new pair structure permits independent typed original F42
words with the same genuine geometric boundary and degree. -/
theorem c60F112CanonicalPairExchange_eq_original
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    c60F112IndependentPairExchange C i
        (c60F112CanonicalOddFacePair C i) =
      c60F108BothFaceOriginalExchange C i := rfl

/-- The new independently site-indexed F51 source interchange
has the SAME complete native arrow as F77's phase-one generator;
the source still records two distinct original F42 boundary words. -/
theorem c60F112IndependentPair_nativePhaseGenerator
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F51Eval (c60F112IndependentPairExchangeHom C i P)) =
      (c60F77PhaseGenerator GrayGrade.unit :
        GrayGrade.unit ⟶ GrayGrade.unit) := by
  apply GradedThreeCell.ext
  · exact (c60F112IndependentPairExchange_components C i P).1
  · exact (c60F112IndependentPairExchange_components C i P).2

/-- An original fully phase-aware F51 interchange is genuinely
NONIDENTITY even when its exact F77 observer cannot distinguish it. -/
theorem c60F112IndependentPair_native_nonidentity
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    c60F51Eval (c60F112IndependentPairExchangeHom C i P) ≠
      (𝟙 GrayGrade.unit : GrayGrade.unit ⟶ GrayGrade.unit) := by
  rw [c60F112IndependentPair_nativePhaseGenerator]
  exact c60F110UnitNativeExchange_ne_identity

/-- Its F77 image is identity, by the actual Mathlib F77
congruence quotient. The erased source exchange phase is
NOT silently declared equal to zero before applying F77. -/
theorem c60F112IndependentPair_F77_identity
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    c60F77Projection.map
        (c60F51Eval (c60F112IndependentPairExchangeHom C i P)) =
      𝟙 (c60F77Projection.obj GrayGrade.unit) := by
  rw [c60F112IndependentPair_nativePhaseGenerator]
  exact c60F77PhaseGenerator_collapses GrayGrade.unit

/-- SOURCE/OBSERVATION BOUNDARY: true distinct original face
sites and a nonidentity original phase-one F51 arrow coexist
with an identity arrow AFTER the F77 projection. -/
theorem c60F112IndependentFaceSites_sourceObservedBoundary
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    c60F112PhysicalFaceSite C i false ≠
        c60F112PhysicalFaceSite C i true ∧
    c60F51Eval (c60F112IndependentPairExchangeHom C i P) ≠
        (𝟙 GrayGrade.unit : GrayGrade.unit ⟶ GrayGrade.unit) ∧
    c60F77Projection.map
        (c60F51Eval (c60F112IndependentPairExchangeHom C i P)) =
      𝟙 (c60F77Projection.obj GrayGrade.unit) :=
  ⟨c60F112PhysicalFaceSites_distinct C i,
    c60F112IndependentPair_native_nonidentity C i P,
    c60F112IndependentPair_F77_identity C i P⟩

/-! ## Exact original F54/F55 boundary and independent F68 obstruction -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineF54F55Boundary
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

/-- ORIGINAL categorical F55 square, with typed F54 rotation
route boundaries, is realized on the very same physical C60
edge used by the independent F42 face pair. The two DIFFERENT
source grammars have not been identified with each other. -/
theorem c60F112IndependentFaces_actualF55Boundary
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F51Eval (c60F112IndependentPairExchangeHom C i P)).phase =
        (1 : ZMod 2) ∧
    c60F44OriginalF55GrayFunctor.map
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right (C.edge i)) =
      c60AllNinetyGrayCell t₁ t₂ left right (C.edge i) := by
  exact ⟨(c60F112IndependentPairExchange_components C i P).2,
    c60F46PhysicalFlagOriginalF55Arrow_fullNative
      t₁ t₂ left right (C.edge i)⟩

/-- The original F54/F55 90-edge physical curvature obstruction is
simultaneously present: a finite F77 observer history cannot make
the F68 original signed north-pentagon second charge -5 vanish. -/
theorem c60F112IndependentFaces_originalCurvature_obstruction
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i)
    (sigma : C60F67Atlas) :
    c60F77Projection.map
        (c60F51Eval (c60F112IndependentPairExchangeHom C i P)) =
          𝟙 (c60F77Projection.obj GrayGrade.unit) ∧
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) ∧
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma ≠ 0 ∧
    (¬ ∃ vertexGauge :
        C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
        c60F68AtlasEdgeCochain t₁ t₂ left right sigma =
          vertexGauge.comp c60IntegralBoundaryOne) := by
  refine ⟨c60F112IndependentPair_F77_identity C i P, ?_, ?_, ?_⟩
  · exact c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma
  · exact c60F68PhysicalPatchCurvature_ne_zero
      t₁ t₂ left right sigma
  · exact c60F110UncorrectedPhysicalGauge_impossible
      t₁ t₂ left right sigma

/-- Most explicit observed/source separation: arbitrarily long
actual physical C60 refinements and arbitrary independent finite
F77 Čech histories agree, WHILE separately indexed original F42
sites, original source phase and F68 signed curvature stay distinct.
Source-side F54/F55 global effective 3-descent is not inferred. -/
theorem c60F112IndependentFaces_towerObserved_obstructions
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I K : Finset (Fin n)}
    (tower : C60F112PhysicalTower I K)
    (i j : C60F111PhysicalChart K)
    (P : C60F112IndependentOddFacePair C i.1)
    (historyK : List (C60F111PhysicalChart K))
    (historyI : List (C60F111PhysicalChart I))
    (X : C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I)
    (sigma : C60F67Atlas) :
    HEq
      ((c60F111PhysicalTransitionChain C K i j historyK).app
        ((c60F112TowerRestrict C tower).obj X))
      ((c60F111PhysicalTransitionChain C I
        (c60F112TowerChart tower i)
        (c60F112TowerChart tower j) historyI).app X) ∧
    (c60F51Eval (c60F112IndependentPairExchangeHom C i.1 P)).phase =
      (1 : ZMod 2) ∧
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) ∧
    (¬ ∃ lift : C60F77NativeQuotient ⥤ GrayGrade,
        c60F77Projection ⋙ lift = 𝟭 GrayGrade) := by
  refine ⟨c60F112TowerAnyHistories_app C tower i j historyK historyI X,
    (c60F112IndependentPairExchange_components C i.1 P).2,
    c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma,
    c60F110NoFullNativeLeftInverseFunctor⟩

end GenuineF54F55Boundary

/-- Canonical REAL ninety physical edge family: independent
original polygonal F42 cell sites are present for every edge,
and its original source F51 arrow is still nonidentity while
the intentional F77 observer identifies it with identity. -/
theorem c60F112AllNinetyIndependentFaces_boundary
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    c60F112PhysicalFaceSite c60F108AllNinetyBothFaces i false ≠
        c60F112PhysicalFaceSite c60F108AllNinetyBothFaces i true ∧
    c60F51Eval
      (c60F112IndependentPairExchangeHom c60F108AllNinetyBothFaces i
        (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)) ≠
        (𝟙 GrayGrade.unit : GrayGrade.unit ⟶ GrayGrade.unit) ∧
    c60F77Projection.map
      (c60F51Eval
        (c60F112IndependentPairExchangeHom c60F108AllNinetyBothFaces i
          (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i))) =
      𝟙 (c60F77Projection.obj GrayGrade.unit) :=
  c60F112IndependentFaceSites_sourceObservedBoundary
    c60F108AllNinetyBothFaces i
    (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)

#print axioms c60F112PhysicalFaceSites_distinct
#print axioms c60F112IndependentPairExchange_components
#print axioms c60F112CanonicalPairExchange_eq_original
#print axioms c60F112IndependentPair_nativePhaseGenerator
#print axioms c60F112IndependentPair_native_nonidentity
#print axioms c60F112IndependentPair_F77_identity
#print axioms c60F112IndependentFaceSites_sourceObservedBoundary
#print axioms c60F112IndependentFaces_actualF55Boundary
#print axioms c60F112IndependentFaces_originalCurvature_obstruction
#print axioms c60F112IndependentFaces_towerObserved_obstructions
#print axioms c60F112AllNinetyIndependentFaces_boundary

end
end KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
