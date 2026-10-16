import KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23

namespace KUOS.DependentOriginationUnitorStarTransitivityV3_24

open CategoryTheory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationPairwiseFiniteExtensionV3_15
open KUOS.DependentOriginationOverlapStarTransitivityV3_20
open KUOS.DependentOriginationUnitorPartialRigidityV3_22

universe u v uH vH

/-!
# Actual homogeneous unitor star transitivity v3.24

v3.20 isolates overlap-star transitivity as a sufficient witness-correlation
criterion.  v3.22 then proves that each corrected unitor locus is graph-like:
inside a fixed left- or right-unitor route, the identity-gauge coordinate
determines the corresponding composition-gauge coordinate.

The full unitor-only restriction of v3.20 is still too strong without an
incidence hypothesis: an anchor footprint can be disjoint from two endpoint
footprints, making both anchor-overlap assumptions vacuous while the endpoints
may still overlap.

This file proves the first actual route-specific triangle-closing statements,
with the literal common-coordinate incidence made explicit:

* three left-unitors with the same source object;
* three right-unitors with the same target object.

For either family, compatibility with one common anchor forces equality of the
shared identity coordinate between the two endpoints.  v3.22 upgrades that
identity equality to the composition equality whenever the endpoint
composition coordinates themselves coincide, hence the complete endpoint
footprint overlap agrees.

No abstract rigidity axiom is added.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Two corrected left-unitors with the same source object agree on every
literally shared footprint coordinate as soon as their common identity-gauge
coordinate agrees. -/
theorem leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : X ⟶ Z)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ : Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor f))
    (hQ' : Q' ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor f) (.leftUnitor g) Q Q' := by
  intro c hc hc'
  simp only [RouteFootprintContains] at hc hc'
  rcases hc with hc | hc
  · subst c
    rcases hc' with hc' | hc'
    · cases hc'
      simpa [quotientGaugeCoordinateValue] using
        leftUnitor_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
          W R D f Q Q' hQ hQ' hId
    · cases hc'
  · subst c
    rcases hc' with hc' | hc'
    · cases hc'
    · cases hc'
      simpa [quotientGaugeCoordinateValue] using hId

/-- Two corrected right-unitors with the same target object agree on every
literally shared footprint coordinate as soon as their common identity-gauge
coordinate agrees. -/
theorem rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Z Y : W.Localization}
    (f : X ⟶ Y) (g : Z ⟶ Y)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ : Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQ' : Q' ∈ quotientRouteCorrectionLocus W R D (.rightUnitor g))
    (hId : Q.mapIdGauge Y = Q'.mapIdGauge Y) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.rightUnitor g) Q Q' := by
  intro c hc hc'
  simp only [RouteFootprintContains] at hc hc'
  rcases hc with hc | hc
  · subst c
    rcases hc' with hc' | hc'
    · cases hc'
      simpa [quotientGaugeCoordinateValue] using
        rightUnitor_mapCompGauge_eq_of_corrected_of_mapIdGauge_eq
          W R D f Q Q' hQ hQ' hId
    · cases hc'
  · subst c
    rcases hc' with hc' | hc'
    · cases hc'
    · cases hc'
      simpa [quotientGaugeCoordinateValue] using hId

/-- A left-unitor star with common source object closes its endpoint triangle.

The anchor itself need not be used through its correction equation: the two
anchor-overlap hypotheses already correlate the endpoint identity coordinates.
The endpoint correction equations are exactly what v3.22 uses to close any
additional shared composition coordinate. -/
theorem leftUnitor_overlapStar_triangle
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : X ⟶ Z) (h : X ⟶ T)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor h))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor f) (.leftUnitor g) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor f) (.leftUnitor h) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor g) (.leftUnitor h) Qt Qu := by
  have hstId :
      Qs.mapIdGauge X = Qt.mapIdGauge X := by
    simpa [quotientGaugeCoordinateValue] using
      hst (.identity X)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hsuId :
      Qs.mapIdGauge X = Qu.mapIdGauge X := by
    simpa [quotientGaugeCoordinateValue] using
      hsu (.identity X)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  exact
    leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D g h Qt Qu hQt hQu (hstId.symm.trans hsuId)

/-- A right-unitor star with common target object closes its endpoint triangle. -/
theorem rightUnitor_overlapStar_triangle
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Z T Y : W.Localization}
    (f : X ⟶ Y) (g : Z ⟶ Y) (h : T ⟶ Y)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor g))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.rightUnitor h))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.rightUnitor g) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.rightUnitor h) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor g) (.rightUnitor h) Qt Qu := by
  have hstId :
      Qs.mapIdGauge Y = Qt.mapIdGauge Y := by
    simpa [quotientGaugeCoordinateValue] using
      hst (.identity Y)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  have hsuId :
      Qs.mapIdGauge Y = Qu.mapIdGauge Y := by
    simpa [quotientGaugeCoordinateValue] using
      hsu (.identity Y)
        (by simp [RouteFootprintContains])
        (by simp [RouteFootprintContains])
  exact
    rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
      W R D g h Qt Qu hQt hQu (hstId.symm.trans hsuId)

/-- Common-extension form of the left-unitor star-closing theorem. -/
theorem leftUnitor_compatibleOverlapStar_triangle
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : X ⟶ Z) (h : X ⟶ T)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor h))
    (hst : CompatibleOnRouteOverlap W R D
      (.leftUnitor f) (.leftUnitor g) Qs Qt)
    (hsu : CompatibleOnRouteOverlap W R D
      (.leftUnitor f) (.leftUnitor h) Qs Qu) :
    CompatibleOnRouteOverlap W R D
      (.leftUnitor g) (.leftUnitor h) Qt Qu := by
  apply compatibleOnRouteOverlap_of_agreeOnRouteFootprintOverlap W R D
  exact
    leftUnitor_overlapStar_triangle W R D f g h Qs Qt Qu hQt hQu
      ((compatibleOnRouteOverlap_iff_agreeOnRouteFootprintOverlap
        W R D _ _ _ _).1 hst)
      ((compatibleOnRouteOverlap_iff_agreeOnRouteFootprintOverlap
        W R D _ _ _ _).1 hsu)

/-- Common-extension form of the right-unitor star-closing theorem. -/
theorem rightUnitor_compatibleOverlapStar_triangle
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Z T Y : W.Localization}
    (f : X ⟶ Y) (g : Z ⟶ Y) (h : T ⟶ Y)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor g))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.rightUnitor h))
    (hst : CompatibleOnRouteOverlap W R D
      (.rightUnitor f) (.rightUnitor g) Qs Qt)
    (hsu : CompatibleOnRouteOverlap W R D
      (.rightUnitor f) (.rightUnitor h) Qs Qu) :
    CompatibleOnRouteOverlap W R D
      (.rightUnitor g) (.rightUnitor h) Qt Qu := by
  apply compatibleOnRouteOverlap_of_agreeOnRouteFootprintOverlap W R D
  exact
    rightUnitor_overlapStar_triangle W R D f g h Qs Qt Qu hQt hQu
      ((compatibleOnRouteOverlap_iff_agreeOnRouteFootprintOverlap
        W R D _ _ _ _).1 hst)
      ((compatibleOnRouteOverlap_iff_agreeOnRouteFootprintOverlap
        W R D _ _ _ _).1 hsu)

/-!
## Frontier after v3.24

The first actual v3.20 triangles close:

* left/left/left stars sharing one source identity coordinate;
* right/right/right stars sharing one target identity coordinate.

The proof mechanism is concrete:

anchor overlap
  => endpoint equality at the shared gId coordinate
  => v3.22 graph rigidity inside each corrected endpoint route
  => equality at any additionally shared gComp coordinate
  => complete endpoint overlap compatibility.

The mixed left/right case is deliberately not asserted here.  If a left and a
right footprint share only the identity coordinate, closure is immediate at
that key; but in the degenerate situation where their composition coordinates
also coincide, v3.22 gives two different graph equations (left and right) and
does not by itself identify their outputs.  That is the next actual coherence
question, rather than something to hide behind a stronger abstract axiom.
-/

end KUOS.DependentOriginationUnitorStarTransitivityV3_24
