import KUOS.DependentOriginationCountableAssociatorStabilizationV3_39

namespace KUOS.DependentOriginationCollisionSectorPreservationV3_40

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientDefectOrbitV3_06
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationCountableAssociatorStabilizationV3_39

universe u v uH vH

set_option autoImplicit false

/-!
# Semantic preservation of the middle-identity collision sector v3.40

Every composition key is inspected by a middle-identity associator. Thus no
leading-coordinate schedule can avoid the footprints of that entire sector.
Freezing all collision coordinates is not the appropriate bridge to v3.39.

Instead, the two unitor equations for one and the same gauge imply its
middle-identity associator equation. The proof reverses the algebraic direction
used in v3.26. The middle identity map is already identical on both sides;
there is no need to reflect an equality through double whiskering. The
bicategory triangle and associator naturality give a common invertible suffix,
which can be cancelled in the ordinary hom-category. The dependent outer
mapComp coordinates are related by their actual eqToHom transport square.

Consequently the v3.38 unitor seed corrects every middle-identity associator,
and v3.39 preserves this semantic correction even while its updates can touch
the collision footprints. One gauge corrects all unitors, all middle-identity
associators, and the prescribed fresh countable schedule.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Every leading key lies in a concrete middle-identity collision footprint.
This statement uses actual localization arrows, not an abstract incidence model. -/
theorem leadingCoordinate_mem_middleIdentityFootprint (a : AssociatorTask W) :
    RouteFootprintContains W (.associator (a.f ≫ a.g) (𝟙 a.Z) a.h)
      (associatorTaskLeadingCoordinate W a) := by
  change QuotientGaugeCoordinate.composition (a.f ≫ a.g) a.h =
      .composition ((a.f ≫ a.g) ≫ 𝟙 a.Z) a.h ∨ _
  exact Or.inl (by rw [Category.comp_id])

/-- A nonempty natural-number schedule cannot avoid all middle-identity
footprints. This obstructs coordinate avoidance, not semantic correction. -/
theorem not_countableSchedule_avoids_all_middleIdentity
    (tasks : ℕ → AssociatorTask W) :
    ¬ (∀ (i : ℕ) {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      ¬ RouteFootprintContains W (.associator f (𝟙 Y) g)
        (associatorTaskLeadingCoordinate W (tasks i))) := by
  intro hAvoid
  exact hAvoid 0 ((tasks 0).f ≫ (tasks 0).g) (tasks 0).h
    (leadingCoordinate_mem_middleIdentityFootprint W (tasks 0))

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- The actual two unitor equations of a single gauge imply its
middle-identity associator equation. Neither freshness nor separation of
double whiskering is needed in this direction. -/
theorem middleIdentityAssociator_corrected_of_unitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hRight : Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hLeft : Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g)) :
    Q ∈ quotientRouteCorrectionLocus W R D (.associator f (𝟙 Y) g) := by
  let F := quotientRepresentativeMap W R D f
  let P := quotientRepresentativeMap W R D (𝟙 Y)
  let G := quotientRepresentativeMap W R D g
  let S := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q

  change quotientRightUnitorDefect W R D S f = Iso.refl _ at hRight
  change quotientLeftUnitorDefect W R D S g = Iso.refl _ at hLeft
  have hR := (quotientRightUnitorDefect_eq_refl_iff W R D S f).1 hRight
  have hL := (quotientLeftUnitorDefect_eq_refl_iff W R D S g).1 hLeft

  let eA :
      quotientRepresentativeMap W R D ((f ≫ 𝟙 Y) ≫ g) ⟶
        quotientRepresentativeMap W R D (f ≫ (𝟙 Y ≫ g)) :=
    eqToHom (by simp)
  let eR : quotientRepresentativeMap W R D (f ≫ 𝟙 Y) ⟶ F :=
    eqToHom (by simp [F])
  let eL : quotientRepresentativeMap W R D (𝟙 Y ≫ g) ⟶ G :=
    eqToHom (by simp [G])

  change (S.mapComp f (𝟙 Y)).hom ≫
      F ◁ (S.mapId Y).hom ≫ (ρ_ F).hom = eR at hR
  change (S.mapComp (𝟙 Y) g).hom ≫
      (S.mapId Y).hom ▷ G ≫ (λ_ G).hom = eL at hL

  -- This square is dependent coordinate transport, not assumed coherence of S.
  have hOuterTransport :
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
        eA ≫ (S.mapComp f (𝟙 Y ≫ g)).hom ≫ F ◁ eL = eR ▷ G := by
    have h := eqToHom_iso_inv_naturality_assoc
      (fun k : X ⟶ Y => S.mapComp k g)
      (Category.comp_id f) (S.mapComp f g).hom
    simpa [eA, eR, eL, F, G] using h

  have hRwhisk :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫
        (F ◁ (S.mapId Y).hom) ▷ G ≫ (ρ_ F).hom ▷ G = eR ▷ G := by
    have h := congrArg (fun η => η ▷ G) hR
    simpa only [comp_whiskerRight, Category.assoc] using h
  have hLwhisk :
      F ◁ (S.mapComp (𝟙 Y) g).hom ≫
        F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom = F ◁ eL := by
    have h := congrArg (fun η => F ◁ η) hL
    simpa only [whiskerLeft_comp, Category.assoc] using h

  have hTriangle :
      (ρ_ F).hom ▷ G = (α_ F (𝟙 _) G).hom ≫ F ◁ (λ_ G).hom :=
    (triangle_assoc_comp_left F G).symm
  have hNaturality :
      (F ◁ (S.mapId Y).hom) ▷ G ≫ (α_ F (𝟙 _) G).hom =
        (α_ F P G).hom ≫ F ◁ ((S.mapId Y).hom ▷ G) := by
    simpa only [P] using associator_naturality_middle F (S.mapId Y).hom G
  have hStructural :
      (F ◁ (S.mapId Y).hom) ▷ G ≫ (ρ_ F).hom ▷ G =
        (α_ F P G).hom ≫
          F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom := by
    calc
      (F ◁ (S.mapId Y).hom) ▷ G ≫ (ρ_ F).hom ▷ G =
          (F ◁ (S.mapId Y).hom) ▷ G ≫
            ((α_ F (𝟙 _) G).hom ≫ F ◁ (λ_ G).hom) := by rw [hTriangle]
      _ = ((F ◁ (S.mapId Y).hom) ▷ G ≫
            (α_ F (𝟙 _) G).hom) ≫ F ◁ (λ_ G).hom := by
              simp only [Category.assoc]
      _ = ((α_ F P G).hom ≫
            F ◁ ((S.mapId Y).hom ▷ G)) ≫ F ◁ (λ_ G).hom := by
              exact congrArg (fun k => k ≫ F ◁ (λ_ G).hom) hNaturality
      _ = (α_ F P G).hom ≫
            F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom := by
              simp only [Category.assoc]

  have hRightNormalized :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom ≫
        F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom = eR ▷ G := by
    have h := congrArg
      (fun k => (S.mapComp f (𝟙 Y)).hom ▷ G ≫ k) hStructural.symm
    calc
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom ≫
          F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom =
          (S.mapComp f (𝟙 Y)).hom ▷ G ≫
            (F ◁ (S.mapId Y).hom) ▷ G ≫ (ρ_ F).hom ▷ G := by
              simpa only [Category.assoc] using h
      _ = eR ▷ G := hRwhisk

  have hLeftViaTransport :
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫ eA ≫
        (S.mapComp f (𝟙 Y ≫ g)).hom ≫ F ◁ (S.mapComp (𝟙 Y) g).hom ≫
        F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom = eR ▷ G := by
    let pre := (S.mapComp (f ≫ 𝟙 Y) g).inv ≫
      eA ≫ (S.mapComp f (𝟙 Y ≫ g)).hom
    have h := congrArg (fun k => pre ≫ k) hLwhisk
    calc
      (S.mapComp (f ≫ 𝟙 Y) g).inv ≫ eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫ F ◁ (S.mapComp (𝟙 Y) g).hom ≫
          F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom = pre ≫ (F ◁ eL) := by
            simpa only [pre, Category.assoc] using h
      _ = eR ▷ G := by
            simpa only [pre, Category.assoc] using hOuterTransport

  -- The suffix is invertible because it is made from mapId and a unitor.
  -- Cancel composition with it; do not assume double-whiskering injectivity.
  have hBridge :
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom =
        (S.mapComp (f ≫ 𝟙 Y) g).inv ≫ eA ≫
          (S.mapComp f (𝟙 Y ≫ g)).hom ≫ F ◁ (S.mapComp (𝟙 Y) g).hom := by
    apply (cancel_mono
      (F ◁ ((S.mapId Y).hom ▷ G) ≫ F ◁ (λ_ G).hom)).1
    simpa only [Category.assoc] using hRightNormalized.trans hLeftViaTransport.symm

  change quotientAssociatorDefect W R D S f (𝟙 Y) g = Iso.refl _
  apply (quotientAssociatorDefect_eq_refl_iff W R D S f (𝟙 Y) g).2
  change (S.mapComp (f ≫ 𝟙 Y) g).hom ≫
      (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom ≫
      F ◁ (S.mapComp (𝟙 Y) g).inv ≫ (S.mapComp f (𝟙 Y ≫ g)).inv = eA
  calc
    (S.mapComp (f ≫ 𝟙 Y) g).hom ≫
        (S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom ≫
        F ◁ (S.mapComp (𝟙 Y) g).inv ≫ (S.mapComp f (𝟙 Y ≫ g)).inv =
        (S.mapComp (f ≫ 𝟙 Y) g).hom ≫
          ((S.mapComp f (𝟙 Y)).hom ▷ G ≫ (α_ F P G).hom) ≫
          F ◁ (S.mapComp (𝟙 Y) g).inv ≫ (S.mapComp f (𝟙 Y ≫ g)).inv := by
            simp only [Category.assoc]
    _ = (S.mapComp (f ≫ 𝟙 Y) g).hom ≫
          ((S.mapComp (f ≫ 𝟙 Y) g).inv ≫ eA ≫
            (S.mapComp f (𝟙 Y ≫ g)).hom ≫ F ◁ (S.mapComp (𝟙 Y) g).hom) ≫
          F ◁ (S.mapComp (𝟙 Y) g).inv ≫ (S.mapComp f (𝟙 Y ≫ g)).inv := by
            rw [hBridge]
    _ = eA := by simp

/-- The unitor seed already corrects the entire middle-identity sector.
The nested pairwise premise is retained, not replaced by separate local existence. -/
theorem exists_unitor_middleIdentitySeed_of_pairwiseShared
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      ∀ (X Y Z : W.Localization) (f : X ⟶ Y) (g : Y ⟶ Z),
        Q ∈ quotientRouteCorrectionLocus W R D (.associator f (𝟙 Y) g) := by
  rcases exists_unitorSeed_of_pairwiseShared W R D H with ⟨Q, hUnit⟩
  refine ⟨Q, hUnit, ?_⟩
  intro X Y Z f g
  exact middleIdentityAssociator_corrected_of_unitors W R D Q f g
    (hUnit Y (.right f)) (hUnit Y (.left g))

/-- Interior sequential completion preserves middle-identity correction
semantically through the unchanged unitors, not by avoiding collision footprints. -/
theorem countableAssociatorGauge_middleIdentity_corrected
    (tasks : ℕ → AssociatorTask W) (Q0 : GeneratedQuotientGaugeParameters W R D)
    (hSafe : CountableForwardNoninterference W tasks)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i)))
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q0 ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    countableAssociatorGauge W R D tasks Q0 hSafe ∈
      quotientRouteCorrectionLocus W R D (.associator f (𝟙 Y) g) := by
  apply middleIdentityAssociator_corrected_of_unitors W R D
    (countableAssociatorGauge W R D tasks Q0 hSafe) f g
  · exact (countableAssociatorGauge_unitor_corrected_iff
      W R D tasks Q0 hSafe hInterior (.right f)).2 (hUnit Y (.right f))
  · exact (countableAssociatorGauge_unitor_corrected_iff
      W R D tasks Q0 hSafe hInterior (.left g)).2 (hUnit Y (.left g))

/-- A common gauge for all unitors, all middle-identity associators, and
one fresh safe countable schedule. No new separation or collision-avoidance
premise is added to v3.39. All three conclusions refer to the same gauge. -/
theorem exists_commonGauge_for_middleIdentity_and_countableSchedule_of_pairwiseShared
    (H : HasPairwiseSharedCoordinateCompatibleLocalCorrections W R D)
    (tasks : ℕ → AssociatorTask W)
    (hFresh : ∀ i : ℕ,
      FreshAssociatorLeadingCoordinate W (tasks i).f (tasks i).g (tasks i).h)
    (hSafe : CountableForwardNoninterference W tasks)
    (hInterior : ∀ i : ℕ, ¬ UnitorVisibleCoordinate W
      (associatorTaskLeadingCoordinate W (tasks i))) :
    ∃ Q : GeneratedQuotientGaugeParameters W R D,
      (∀ X (s : UnitorRouteAt W X),
        Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      (∀ (X Y Z : W.Localization) (f : X ⟶ Y) (g : Y ⟶ Z),
        Q ∈ quotientRouteCorrectionLocus W R D (.associator f (𝟙 Y) g)) ∧
      ∀ i : ℕ, Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W (tasks i)) := by
  rcases exists_commonGauge_for_countableSchedule_of_pairwiseShared
    W R D H tasks hFresh hSafe hInterior with ⟨Q, hUnit, hTasks⟩
  refine ⟨Q, hUnit, ?_, hTasks⟩
  intro X Y Z f g
  exact middleIdentityAssociator_corrected_of_unitors W R D Q f g
    (hUnit Y (.right f)) (hUnit Y (.left g))

/-!
## Boundary

This resolves semantic correction of the middle-identity collision sector
once a common unitor gauge is available. It does not make its leading key
fresh, freeze its composition coordinates, or prove equality of identity
values belonging to different gauges. The v3.26-v3.34 separation direction
for distinct endpoint witnesses and all its hypotheses remain unchanged.

Other collision shapes, existence of a fresh/interior/noninterfering ordering,
coverage of arbitrary associators, schedule/seed/W/R/D independence, unrestricted
all-route correlation, Stage I, Stage II and final universality remain separate.
No compiler/dependency pins, earlier theorem statements or workflows are changed.
-/

end KUOS.DependentOriginationCollisionSectorPreservationV3_40
