import KUOS.DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289
import KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225

namespace KUOS.DependentOriginationC60KuuCurvedIncidenceSourceDescentCriterionV5_290

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.290 / F112 part 18 — conditional original-incidence curved source effectivity

The verified v5.289 original-F47 source equivalences are over the
LOCALIZED category of actual overlap-WITNESSED C60 physical-edge paths.
They do NOT automatically extend to the unrelated ORIGINAL F69 poset
consisting of 60 original vertices, 90 physical edges and 32 original
pentagons/hexagons.

The original F71 interface requires a *supplied* Cat-valued functor
on ALL of that F69 incidence category and prescribed original
four-boundary F47 fibres at its 90 edges.  We do not assert existence
of such a functor, let alone a raw original F42/F54/F55 3-stack.

This stage proves the precise remaining *separate* curvature criterion:
  I. An explicitly chosen original 60-vertex Gray potential gives a
     canonical affine physical 90-edge correction.
  II. ALL and ONLY valid curvature-cancelling repairs arise in this
     manner: the correction space has an explicit affine description
     over the genuine vertex gauges, not an ad hoc zero curvature.
  III. Every valid correction is NONZERO and must contribute exactly
     +5 to the NORTH actual pentagon's second integer charge, cancelling
     the verified ORIGINAL curvature -5 on that oriented face.
  IV. Given any independently SUPPLIED original F71 full-incidence
     Cat diagram, one can construct a *corrected* vertex-descent
     certificate, with exact original 360 flag triangle coherence.
     Conversely, forgetting the corrected certificate returns its
     required F71 incidence extension. Thus inhabitation of the new
     corrected INTERFACE is EQUIVALENT to inhabitation of the still
     unconstructed original F71 full-incidence interface, without
     manufacturing that missing source data.
  V. The verified localized-witnessed F47 total equivalence and this
     conditional curved original incidence extension can coexist,
     but neither replaces the other's physical category or source
     grammar.

The uncorrected variant remains IMPOSSIBLE. This is a concrete
necessary/sufficient theorem for the CELLULAR GRAY cochain part,
conditioned on the independent Cat-valued original F69 extension,
not a proof of unconstrained original F42/F54/F55 higher-source
3-descent.  Old F55 Delta nine-constructor nonlift, lost F77 phase
and nonzero north original signed F68 second charge -5 persist.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalCurvedIncidenceCriterion
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

/-! ## I. All physical corrections are explicitly vertex-gauge affine -/

/-- A CHOSEN physical vertex gauge specifies its unique edge
correction relative to the ACTUAL, curved, original 90-edge
Gray field. No source F42/F54/F55 Hom is equated. -/
def c60F124GaugeSpecifiedPhysicalCorrection
    (sigma : C60F67Atlas)
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  phi.comp c60IntegralBoundaryOne -
    c60F68AtlasEdgeCochain t₁ t₂ left right sigma

/-- ANY explicitly given original vertex gauge and its
AFFINE physical correction satisfy the FULL 90-edge gauge
equation. This is a source-cochain theorem, NOT a claim
that F69 vertex/face F47 source fibres already exist. -/
theorem c60F124GaugeSpecifiedPhysicalCorrection_descends
    (sigma : C60F67Atlas)
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    c60F68AtlasEdgeCochain t₁ t₂ left right sigma +
      c60F124GaugeSpecifiedPhysicalCorrection
        t₁ t₂ left right sigma phi =
      phi.comp c60IntegralBoundaryOne := by
  unfold c60F124GaugeSpecifiedPhysicalCorrection
  abel

/-- The ORIGINAL physically signed 32-face curvature
is cancelled by the actual boundary of every gauge-specified
repair, not just by its sum over the whole C60 surface. -/
theorem c60F124GaugeSpecifiedPhysicalCorrection_cancelsCurvature
    (sigma : C60F67Atlas)
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma +
      (c60F124GaugeSpecifiedPhysicalCorrection
        t₁ t₂ left right sigma phi).comp
        c60IntegralBoundaryTwo = 0 := by
  apply (c60F68AffineCorrection_descent_iff
    t₁ t₂ left right sigma
    (c60F124GaugeSpecifiedPhysicalCorrection
      t₁ t₂ left right sigma phi)).2
  exact ⟨phi,
    c60F124GaugeSpecifiedPhysicalCorrection_descends
      t₁ t₂ left right sigma phi⟩

/-- EXACT classification of ALL admissible original C60
physical curvature corrections: a correction cancels the
FULL signed face 2-cochain if and only if it is of the
explicit vertex-gauge affine form. This uses the proved
actual C60 H1 contraction, not an additional axiom. -/
theorem c60F124AllPhysicalCorrections_iff_vertexGauges
    (sigma : C60F67Atlas)
    (gamma : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma +
        gamma.comp c60IntegralBoundaryTwo = 0 ↔
      ∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
        gamma =
          c60F124GaugeSpecifiedPhysicalCorrection
            t₁ t₂ left right sigma phi := by
  constructor
  · intro hcancel
    obtain ⟨phi, hGauge⟩ :=
      (c60F68AffineCorrection_descent_iff
        t₁ t₂ left right sigma gamma).1 hcancel
    refine ⟨phi, ?_⟩
    unfold c60F124GaugeSpecifiedPhysicalCorrection
    calc
      gamma =
        (c60F68AtlasEdgeCochain t₁ t₂ left right sigma + gamma) -
          c60F68AtlasEdgeCochain t₁ t₂ left right sigma := by
            abel
      _ = phi.comp c60IntegralBoundaryOne -
          c60F68AtlasEdgeCochain t₁ t₂ left right sigma := by
            rw [hGauge]
  · rintro ⟨phi, rfl⟩
    exact c60F124GaugeSpecifiedPhysicalCorrection_cancelsCurvature
      t₁ t₂ left right sigma phi

/-- AFFINE PARAMETRIZATION around the EXISTING true physical
F55-tree correction. Any other admissible correction differs
from that canonical nonzero one by the boundary of the
difference of two genuine vertex potentials. -/
theorem c60F124GaugeSpecifiedRepair_affineOverCanonical
    (sigma : C60F67Atlas)
    (phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0) :
    c60F124GaugeSpecifiedPhysicalCorrection
        t₁ t₂ left right sigma phi =
      c60F68CanonicalPhysicalRepair t₁ t₂ left right sigma +
        (phi - c60F19TreeVertexGauge).comp
          c60IntegralBoundaryOne := by
  apply LinearMap.ext
  intro chain
  have hcanon :=
    congrArg (fun f : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 =>
      f chain)
      (c60F68CanonicalPhysicalRepair_realizesGlobalGauge
        t₁ t₂ left right sigma)
  simp only [LinearMap.add_apply, LinearMap.comp_apply] at hcanon
  simp only [c60F124GaugeSpecifiedPhysicalCorrection,
    LinearMap.sub_apply, LinearMap.comp_apply, LinearMap.add_apply]
  calc
    phi (c60IntegralBoundaryOne chain) -
        c60F68AtlasEdgeCochain t₁ t₂ left right sigma chain =
      c60F68CanonicalPhysicalRepair t₁ t₂ left right sigma chain +
        (phi (c60IntegralBoundaryOne chain) -
          (c60F68AtlasEdgeCochain t₁ t₂ left right sigma chain +
            c60F68CanonicalPhysicalRepair t₁ t₂ left right sigma chain)) := by
              abel
    _ = c60F68CanonicalPhysicalRepair
          t₁ t₂ left right sigma chain +
        (phi (c60IntegralBoundaryOne chain) -
          c60F19TreeVertexGauge (c60IntegralBoundaryOne chain)) := by
            rw [hcanon]

/-! ## II. The real north-pentagon charge forces nonzero repair -/

/-- ANY admissible physical 90-edge correction has EXACTLY
+5 on the original north pentagonal boundary's SECOND
INTEGER charge. It is forced by the original source
curvature -5, not chosen as an abstract phase. -/
theorem c60F124AnyAdmissibleCorrection_northSecondCharge
    (sigma : C60F67Atlas)
    (gamma : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0)
    (hcancel :
      c60F68PhysicalPatchCurvature t₁ t₂ left right sigma +
        gamma.comp c60IntegralBoundaryTwo = 0) :
    ((gamma.comp c60IntegralBoundaryTwo)
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
      (5 : ℤ) := by
  let north : C60IntegralTwoChains :=
    Finsupp.single (.aroundVertex .north) (1 : ℤ)
  have hEval := congrArg
    (fun f : C60IntegralTwoChains →ₗ[ℤ] GradedThreeCell 0 0 =>
      (f north).charge.2) hcancel
  have hcharge :
      (c60F68PhysicalPatchCurvature
        t₁ t₂ left right sigma north).charge.2 +
      ((gamma.comp c60IntegralBoundaryTwo) north).charge.2 =
      (0 : ℤ) := by
    simpa only [LinearMap.add_apply, grayNeutral_add_charge,
      Prod.add_def] using hEval
  have hNorth :=
    c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma
  change (c60F68PhysicalPatchCurvature
    t₁ t₂ left right sigma north).charge.2 = (-5 : ℤ) at hNorth
  rw [hNorth] at hcharge
  omega

/-- A correction that cancels the genuine physical signed
north-pentagon curvature can NEVER be zero. Zero repair would
contradict the actual original -5 charge, independently of
any optional F71 incidence extension or witnessed localization. -/
theorem c60F124AnyAdmissibleCorrection_nonzero
    (sigma : C60F67Atlas)
    (gamma : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0)
    (hcancel :
      c60F68PhysicalPatchCurvature t₁ t₂ left right sigma +
        gamma.comp c60IntegralBoundaryTwo = 0) :
    gamma ≠ 0 := by
  intro hzero
  obtain ⟨phi, hGauge⟩ :=
    (c60F68AffineCorrection_descent_iff
      t₁ t₂ left right sigma gamma).1 hcancel
  have hUnrepaired :
      c60F68AtlasEdgeCochain t₁ t₂ left right sigma =
      phi.comp c60IntegralBoundaryOne := by
    simpa [hzero] using hGauge
  have hFlat :=
    (c60F68PhysicalFlat_iff_vertexDescent
      t₁ t₂ left right sigma).2 ⟨phi, hUnrepaired⟩
  exact (c60F68PhysicalPatchCurvature_ne_zero
    t₁ t₂ left right sigma) hFlat

/-! ## III. Conditional entire ORIGINAL F69 incidence source + nonflat repair -/

/-- Proof-relevant CORRECTED F69 incidence source data.
The extension on all ORIGINAL 60/90/32 sites is INPUT,
never constructed by magic from the witnessed-path localization.
The additive correction and exact physical vertex gauge are
separately present: this is a precisely stated necessary
cellular Gray-cochain clause, NOT full raw F42/F54/F55
3-stack effectivity. -/
structure C60F124CurvedOriginalIncidenceDescent
    (sigma : C60F67Atlas) where
  extension : C60F71IncidenceExtension
    t₁ t₂ left right sigma
  correction :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0
  vertexGauge :
    C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0
  corrected_edges :
    c60F68AtlasEdgeCochain t₁ t₂ left right sigma +
      correction = vertexGauge.comp c60IntegralBoundaryOne

/-- Given ANY independently supplied full ORIGINAL F69
incidence Cat-valued source extension, the ACTUAL C60 F55
tree repair produces a concrete admissible corrected gauge.
No existence of the extension itself is claimed. -/
def c60F124CanonicalCorrectedIncidenceOfExtension
    (sigma : C60F67Atlas)
    (ext : C60F71IncidenceExtension
      t₁ t₂ left right sigma) :
    C60F124CurvedOriginalIncidenceDescent
      t₁ t₂ left right sigma where
  extension := ext
  correction := c60F68CanonicalPhysicalRepair
    t₁ t₂ left right sigma
  vertexGauge := c60F19TreeVertexGauge
  corrected_edges :=
    c60F68CanonicalPhysicalRepair_realizesGlobalGauge
      t₁ t₂ left right sigma

/-- The exact missing datum is the FULL original F69
Cat-valued incidence extension: since a canonical
NONZERO corrective physical Gray gauge already exists,
the corrected-interface has inhabitants IFF the supplied
full incidence extension interface does. Neither side's
nonemptiness is assumed or proved. -/
theorem c60F124CorrectedDescent_nonempty_iff_incidenceExtension
    (sigma : C60F67Atlas) :
    Nonempty (C60F124CurvedOriginalIncidenceDescent
        t₁ t₂ left right sigma) ↔
      Nonempty (C60F71IncidenceExtension
        t₁ t₂ left right sigma) := by
  constructor
  · rintro ⟨w⟩
    exact ⟨w.extension⟩
  · rintro ⟨ext⟩
    exact ⟨c60F124CanonicalCorrectedIncidenceOfExtension
      t₁ t₂ left right sigma ext⟩

/-- EVERY corrected original-incidence datum cancels the
entire signed 32-face physical curvature: its `correction`
satisfies the genuine cellular descent necessary condition. -/
theorem c60F124CorrectedIncidence_cancelsFullCurvature
    (sigma : C60F67Atlas)
    (data : C60F124CurvedOriginalIncidenceDescent
      t₁ t₂ left right sigma) :
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma +
      data.correction.comp c60IntegralBoundaryTwo = 0 :=
  (c60F68AffineCorrection_descent_iff
    t₁ t₂ left right sigma data.correction).2
    ⟨data.vertexGauge, data.corrected_edges⟩

/-- The corrected F69 source extension genuinely remains
CURVED in the original field: ANY correction is nonzero
and contributes precisely +5 on the north-pentagon boundary.
The old raw F55 Delta nonlift cannot be declared repaired
as a original source generator. -/
theorem c60F124CorrectedIncidence_forcedNonzeroNorthRepair
    (sigma : C60F67Atlas)
    (data : C60F124CurvedOriginalIncidenceDescent
      t₁ t₂ left right sigma) :
    data.correction ≠ 0 ∧
    ((data.correction.comp c60IntegralBoundaryTwo)
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (5 : ℤ) := by
  have hcancel :=
    c60F124CorrectedIncidence_cancelsFullCurvature
      t₁ t₂ left right sigma data
  exact ⟨c60F124AnyAdmissibleCorrection_nonzero
      t₁ t₂ left right sigma data.correction hcancel,
    c60F124AnyAdmissibleCorrection_northSecondCharge
      t₁ t₂ left right sigma data.correction hcancel⟩

/-- All 360 ORIGINAL vertex-edge-face incidence triangles
remain EXACTLY coherent for the genuine full-incidence
Cat diagram, conditionally on that diagram's supplied
existence, while the necessary physical correction remains
nonzero with second integer north charge +5.
This is not an uncorrected raw original 3-descent theorem. -/
theorem c60F124AllOriginalFlags_conditionalAndCurved
    (sigma : C60F67Atlas)
    (data : C60F124CurvedOriginalIncidenceDescent
      t₁ t₂ left right sigma) :
    (∀ (edge : TruncatedIcosahedralEdge) (endpoint side : Bool),
        data.extension.diagram.map
          (c60F71ActualFlagVertexEdgeHom edge endpoint) ≫
        data.extension.diagram.map
          (c60F71ActualFlagEdgeFaceHom edge side) =
        data.extension.diagram.map
          (c60F71ActualFlagVertexFaceHom edge endpoint side)) ∧
    data.correction ≠ 0 ∧
    ((data.correction.comp c60IntegralBoundaryTwo)
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (5 : ℤ) := by
  refine ⟨?_, (c60F124CorrectedIncidence_forcedNonzeroNorthRepair
    t₁ t₂ left right sigma data).1,
    (c60F124CorrectedIncidence_forcedNonzeroNorthRepair
      t₁ t₂ left right sigma data).2⟩
  intro edge endpoint side
  exact c60F71EveryRealPhysicalFlag_extension_coherent
    t₁ t₂ left right sigma data.extension edge endpoint side

/-- The OLD original incidence flat-descent specification
is EMPTY even though the new corrected interface has the
explicit canonical builder whenever a genuine full original
F69 source extension is separately supplied. These two
statements are not contradictory: the correction is NONZERO. -/
theorem c60F124UnrepairedPhysicalDescent_impossible
    (sigma : C60F67Atlas) :
    IsEmpty (C60F71UnrepairedEffectiveDescent
      t₁ t₂ left right sigma) :=
  c60F71NoUnrepairedEffectivePhysicalDescent
    t₁ t₂ left right sigma

#print axioms c60F124GaugeSpecifiedPhysicalCorrection_descends
#print axioms c60F124GaugeSpecifiedPhysicalCorrection_cancelsCurvature
#print axioms c60F124AllPhysicalCorrections_iff_vertexGauges
#print axioms c60F124GaugeSpecifiedRepair_affineOverCanonical
#print axioms c60F124AnyAdmissibleCorrection_northSecondCharge
#print axioms c60F124AnyAdmissibleCorrection_nonzero
#print axioms c60F124CanonicalCorrectedIncidenceOfExtension
#print axioms c60F124CorrectedDescent_nonempty_iff_incidenceExtension
#print axioms c60F124CorrectedIncidence_cancelsFullCurvature
#print axioms c60F124CorrectedIncidence_forcedNonzeroNorthRepair
#print axioms c60F124AllOriginalFlags_conditionalAndCurved
#print axioms c60F124UnrepairedPhysicalDescent_impossible

end OriginalCurvedIncidenceCriterion
end
end KUOS.DependentOriginationC60KuuCurvedIncidenceSourceDescentCriterionV5_290
