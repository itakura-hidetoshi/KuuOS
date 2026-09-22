import KUOS.DependentOriginationWCompositeSplitSeparationV3_34
import Mathlib.Tactic.Choose

namespace KUOS.DependentOriginationUnitorWitnessCorrelationV3_35

open CategoryTheory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationGlobalFootprintGluingV3_16
open KUOS.DependentOriginationUnitorStarTransitivityV3_24
open KUOS.DependentOriginationMixedUnitorRigidityV3_25

universe u v uH vH

set_option autoImplicit false

/-!
# Simultaneous unitor witness correlation v3.35

The actual unitor incidence system has one distinguished object per route:
its identity coordinate. Every composition coordinate in that route has the
same middle object. Thus routes based at different objects cannot overlap.

For each object X, use leftUnitor (identity X) as an anchor. The nested
pairwise predicate supplies one family relative to this anchor. The concrete
v3.24/v3.25 left/right correction equations make that family pairwise
compatible. Families at different objects then coexist without new overlap
conditions. Classical choice selects each object anchor and each unitor
witness once; it does not infer a simultaneous solution of associator clauses.

The last bridge reuses v3.16. It removes all unitor/unitor overlap tests from
a full selected correcting family, but explicitly retains every overlap
involving an associator. No all-route star transitivity is postulated.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The two kinds of unitor route based at one identity object. -/
inductive UnitorRouteAt (X : W.Localization) : Type (max u v) where
  | left {Y : W.Localization} (f : X ⟶ Y)
  | right {Y : W.Localization} (f : Y ⟶ X)

/-- Embed the unitor subsystem into the actual three-route system. -/
def unitorRouteState {X : W.Localization} :
    UnitorRouteAt W X → ThreeQuotientRouteState W
  | .left f => .leftUnitor f
  | .right f => .rightUnitor f

/-- A coordinate remembers the middle object of a composable pair, or the
object of an identity. This projection avoids dependent-key cancellation. -/
def quotientCoordinateMiddle : QuotientGaugeCoordinate W → W.Localization
  | .identity X => X
  | .composition (Y := Y) _ _ => Y

/-- Every coordinate in a unitor footprint lies over its identity object. -/
theorem quotientCoordinateMiddle_eq_of_unitor_mem
    {X : W.Localization} (s : UnitorRouteAt W X)
    (c : QuotientGaugeCoordinate W)
    (hc : RouteFootprintContains W (unitorRouteState W s) c) :
    quotientCoordinateMiddle W c = X := by
  cases s with
  | left f =>
      change c = .composition (𝟙 X) f ∨ c = .identity X at hc
      rcases hc with hc | hc <;> subst c <;> rfl
  | right f =>
      change c = .composition f (𝟙 X) ∨ c = .identity X at hc
      rcases hc with hc | hc <;> subst c <;> rfl

/-- Actual overlap forces the two unitor identity objects to be equal. -/
theorem unitor_objects_eq_of_shared_coordinate
    {X Y : W.Localization} (s : UnitorRouteAt W X)
    (t : UnitorRouteAt W Y) (c : QuotientGaugeCoordinate W)
    (hs : RouteFootprintContains W (unitorRouteState W s) c)
    (ht : RouteFootprintContains W (unitorRouteState W t) c) : X = Y := by
  exact (quotientCoordinateMiddle_eq_of_unitor_mem W s c hs).symm.trans
    (quotientCoordinateMiddle_eq_of_unitor_mem W t c ht)

/-- Every unitor based at X contains the identity coordinate of X. -/
theorem unitor_identity_mem {X : W.Localization} (s : UnitorRouteAt W X) :
    RouteFootprintContains W (unitorRouteState W s) (.identity X) := by
  cases s <;> simp [unitorRouteState, RouteFootprintContains]

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- The four homogeneous/mixed cases reuse the actual unitor equations. -/
theorem unitor_overlap_of_corrected_of_mapIdGauge_eq
    {X : W.Localization} (s t : UnitorRouteAt W X)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ : Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hQ' : Q' ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W t))
    (hId : Q.mapIdGauge X = Q'.mapIdGauge X) :
    AgreeOnRouteFootprintOverlap W R D
      (unitorRouteState W s) (unitorRouteState W t) Q Q' := by
  cases s with
  | left f =>
      cases t with
      | left g =>
          exact leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
            W R D f g Q Q' hQ hQ' hId
      | right g =>
          exact leftUnitor_rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
            W R D f g Q Q' hQ hQ' hId
  | right f =>
      cases t with
      | left g =>
          exact rightUnitor_leftUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
            W R D f g Q Q' hQ hQ' hId
      | right g =>
          exact rightUnitor_agreeOnRouteFootprintOverlap_of_corrected_of_mapIdGauge_eq
            W R D f g Q Q' hQ hQ' hId

/-- Literal overlap with the identity anchor fixes the unitor identity value. -/
theorem mapIdGauge_eq_of_unitor_anchor_overlap
    {X : W.Localization} (s : UnitorRouteAt W X)
    (Q0 Q : GeneratedQuotientGaugeParameters W R D)
    (h : AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor (𝟙 X)) (unitorRouteState W s) Q0 Q) :
    Q0.mapIdGauge X = Q.mapIdGauge X := by
  exact h (.identity X)
    (by simp [RouteFootprintContains]) (unitor_identity_mem W s)

/-- One anchor per object correlates a single family over all unitor routes.
Different objects are handled by the proved coordinate-middle projection,
not by an assumed global star condition. -/
theorem unitorFamily_pairwise_of_identity_anchors
    (Q0 : W.Localization → GeneratedQuotientGaugeParameters W R D)
    (Qlocal : (X : W.Localization) →
      UnitorRouteAt W X → GeneratedQuotientGaugeParameters W R D)
    (hCorrect : ∀ X s,
      Qlocal X s ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hAnchor : ∀ X s, AgreeOnRouteFootprintOverlap W R D
      (.leftUnitor (𝟙 X)) (unitorRouteState W s) (Q0 X) (Qlocal X s)) :
    ∀ X Y (s : UnitorRouteAt W X) (t : UnitorRouteAt W Y),
      AgreeOnRouteFootprintOverlap W R D
        (unitorRouteState W s) (unitorRouteState W t) (Qlocal X s) (Qlocal Y t) := by
  intro X Y s t c hsc htc
  have hXY : X = Y := unitor_objects_eq_of_shared_coordinate W s t c hsc htc
  subst Y
  have hs := mapIdGauge_eq_of_unitor_anchor_overlap
    W R D s (Q0 X) (Qlocal X s) (hAnchor X s)
  have ht := mapIdGauge_eq_of_unitor_anchor_overlap
    W R D t (Q0 X) (Qlocal X t) (hAnchor X t)
  exact unitor_overlap_of_corrected_of_mapIdGauge_eq W R D s t
    (Qlocal X s) (Qlocal X t) (hCorrect X s) (hCorrect X t)
    (hs.symm.trans ht) c hsc htc

/-- Only the stars at the actual identity unitors are needed for this sector. -/
def HasIdentityAnchoredUnitorWitnesses : Prop :=
  ∀ X : W.Localization,
    ∃ Q0 : GeneratedQuotientGaugeParameters W R D,
      Q0 ∈ quotientRouteCorrectionLocus W R D (.leftUnitor (𝟙 X)) ∧
      ∀ s : UnitorRouteAt W X,
        ∃ Q : GeneratedQuotientGaugeParameters W R D,
          Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) ∧
          AgreeOnRouteFootprintOverlap W R D
            (.leftUnitor (𝟙 X)) (unitorRouteState W s) Q0 Q

/-- One simultaneous correcting family, compatible on all unitor overlaps. -/
def HasGloballyCompatibleUnitorCorrectionFamily : Prop :=
  ∃ Qlocal : (X : W.Localization) →
      UnitorRouteAt W X → GeneratedQuotientGaugeParameters W R D,
    (∀ X s,
      Qlocal X s ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
    ∀ X Y (s : UnitorRouteAt W X) (t : UnitorRouteAt W Y),
      AgreeOnRouteFootprintOverlap W R D
        (unitorRouteState W s) (unitorRouteState W t) (Qlocal X s) (Qlocal Y t)

/-- The original nested pairwise hypothesis supplies every needed anchor star. -/
theorem identityAnchoredUnitorWitnesses_of_pairwiseShared
    (hPair : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D) :
    HasIdentityAnchoredUnitorWitnesses W R D := by
  intro X
  rcases hPair (.leftUnitor (𝟙 X)) with ⟨Q0, hQ0, hStar⟩
  exact ⟨Q0, hQ0, fun s => hStar (unitorRouteState W s)⟩

/-- Choose one witness per unitor, once, and use the actual incidence proof
for all pairs in that same family. Empty object types require no special case. -/
theorem globalUnitorFamily_of_identityAnchoredWitnesses
    (H : HasIdentityAnchoredUnitorWitnesses W R D) :
    HasGloballyCompatibleUnitorCorrectionFamily W R D := by
  classical
  choose Q0 _hQ0 hWitness using H
  choose Qlocal hCorrect hAnchor using hWitness
  exact ⟨Qlocal, hCorrect,
    unitorFamily_pairwise_of_identity_anchors W R D Q0 Qlocal hCorrect hAnchor⟩

/-- A compatible unitor family supplies the same objectwise anchor stars. -/
theorem identityAnchoredWitnesses_of_globalUnitorFamily
    (H : HasGloballyCompatibleUnitorCorrectionFamily W R D) :
    HasIdentityAnchoredUnitorWitnesses W R D := by
  rcases H with ⟨Qlocal, hCorrect, hPair⟩
  intro X
  refine ⟨Qlocal X (.left (𝟙 X)), hCorrect X (.left (𝟙 X)), ?_⟩
  intro s
  exact ⟨Qlocal X s, hCorrect X s, hPair X X (.left (𝟙 X)) s⟩

/-- The witness-correlation gap closes for this actual unitor subsystem. -/
theorem identityAnchoredUnitorWitnesses_iff_globalUnitorFamily :
    HasIdentityAnchoredUnitorWitnesses W R D ↔
      HasGloballyCompatibleUnitorCorrectionFamily W R D :=
  ⟨globalUnitorFamily_of_identityAnchoredWitnesses W R D,
    identityAnchoredWitnesses_of_globalUnitorFamily W R D⟩

/-- Nested all-route witnesses therefore correlate on all unitors, without
extra separation, normalizer, or all-route star-transitivity hypotheses. -/
theorem globalUnitorFamily_of_pairwiseShared
    (hPair : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D) :
    HasGloballyCompatibleUnitorCorrectionFamily W R D := by
  exact globalUnitorFamily_of_identityAnchoredWitnesses W R D
    (identityAnchoredUnitorWitnesses_of_pairwiseShared W R D hPair)

/-- The residual overlap tests for a full selected family: every pair with
an associator as its first route. Symmetry handles the other orientation. -/
def AssociatorOverlapTests
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
      (t : ThreeQuotientRouteState W),
    AgreeOnRouteFootprintOverlap W R D (.associator f g h) t
      (Qlocal (.associator f g h)) (Qlocal t)

/-- For one full correcting family, objectwise unitor anchors remove every
unitor/unitor test. Associator tests concern that very same family. -/
theorem globalFamily_of_unitorAnchors_of_associatorTests
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hCorrect : ∀ s, Qlocal s ∈ quotientRouteCorrectionLocus W R D s)
    (Q0 : W.Localization → GeneratedQuotientGaugeParameters W R D)
    (hAnchor : ∀ X (s : UnitorRouteAt W X),
      AgreeOnRouteFootprintOverlap W R D (.leftUnitor (𝟙 X))
        (unitorRouteState W s) (Q0 X) (Qlocal (unitorRouteState W s)))
    (hAssoc : AssociatorOverlapTests W R D Qlocal) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  have hUnit := unitorFamily_pairwise_of_identity_anchors W R D Q0
    (fun X s => Qlocal (unitorRouteState W s))
    (fun X s => hCorrect (unitorRouteState W s)) hAnchor
  refine ⟨Qlocal, hCorrect, ?_⟩
  intro s t
  cases s with
  | associator f g h => exact hAssoc f g h t
  | leftUnitor f =>
      cases t with
      | associator g h k =>
          exact (agreeOnRouteFootprintOverlap_symm W R D _ _ _ _).1
            (hAssoc g h k (.leftUnitor f))
      | leftUnitor g => exact hUnit _ _ (.left f) (.left g)
      | rightUnitor g => exact hUnit _ _ (.left f) (.right g)
  | rightUnitor f =>
      cases t with
      | associator g h k =>
          exact (agreeOnRouteFootprintOverlap_symm W R D _ _ _ _).1
            (hAssoc g h k (.rightUnitor f))
      | leftUnitor g => exact hUnit _ _ (.right f) (.left g)
      | rightUnitor g => exact hUnit _ _ (.right f) (.right g)

/-- Reuse the proved v3.16 gluing only after the same full family has passed
the residual associator tests. No new patching construction is required. -/
theorem finiteFootprintAmalgamation_of_unitorAnchors_of_associatorTests
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hCorrect : ∀ s, Qlocal s ∈ quotientRouteCorrectionLocus W R D s)
    (Q0 : W.Localization → GeneratedQuotientGaugeParameters W R D)
    (hAnchor : ∀ X (s : UnitorRouteAt W X),
      AgreeOnRouteFootprintOverlap W R D (.leftUnitor (𝟙 X))
        (unitorRouteState W s) (Q0 X) (Qlocal (unitorRouteState W s)))
    (hAssoc : AssociatorOverlapTests W R D Qlocal) :
    HasFiniteFootprintAmalgamation W R D := by
  exact hasFiniteFootprintAmalgamation_of_globalFamily W R D
    (globalFamily_of_unitorAnchors_of_associatorTests
      W R D Qlocal hCorrect Q0 hAnchor hAssoc)

/-!
## Boundary

Only the unitor subsystem has its nested-witness correlation proved here.
The full bridge retains correction of every route and associator overlap
tests for one and the same selected family. The unitor existence theorem
does not silently choose compatible associator witnesses for that family.

The v3.33/v3.34 separation results and their three correction/two anchor
hypotheses remain unchanged. General all-route correlation, comparison
coherence, Stage I, Stage II, and final universality are separate targets.
All contextual and choice parameters W/R/D remain fixed.
-/

end KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
