import KUOS.DependentOriginationCollisionAbsorptionReductionV3_49

namespace KUOS.DependentOriginationLeftIdentitySemanticRecoveryV3_50

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
open KUOS.DependentOriginationCollisionSectorPreservationV3_40
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCollisionAbsorptionReductionV3_49

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Semantic recovery of the left-identity collision sector v3.50

v3.49 reduces every non-middle collision residual satisfying the directional
cancellation hypotheses `Epi a.f` and `Mono a.g` to an actual left-identity
associator

```text
associator (𝟙 X) g h.
```

This layer truth-tests that remaining geometry against one fixed quotient
gauge.  The result is the left-hand analogue of the semantic idea used in
v3.40, but the coherence route is different.

For a single gauge `Q`, correction of the two left-unit routes at `g` and
`g ≫ h` already forces correction of `associator (𝟙 X) g h`.  The proof uses
only the exact route equations, dependent `eqToHom` transport for
`𝟙 X ≫ g = g`, and the native bicategory identities

* `associator_naturality_left`;
* `leftUnitor_naturality`;
* `leftUnitor_whiskerRight`;
* `whisker_exchange`.

Thus the left-identity associator contributes no new compatibility equation
once the same gauge already corrects all left unitors.

Combining with v3.49 closes the epi/mono-reducible collision residual under a
common unitor gauge.  No epi/mono hypothesis is manufactured from collision,
and arbitrary collision residuals outside that cancellation sector remain
explicit.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- The two left-unitor equations of one and the same quotient gauge imply
its left-identity associator equation. -/
theorem leftIdentityAssociator_corrected_of_leftUnitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Z T : W.Localization} (g : X ⟶ Z) (h : Z ⟶ T)
    (hLeftG :
      Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hLeftGH :
      Q ∈ quotientRouteCorrectionLocus W R D (.leftUnitor (g ≫ h))) :
    Q ∈ quotientRouteCorrectionLocus W R D
      (.associator (𝟙 X) g h) := by
  let P := quotientRepresentativeMap W R D (𝟙 X)
  let G := quotientRepresentativeMap W R D g
  let H := quotientRepresentativeMap W R D h
  let K := quotientRepresentativeMap W R D (g ≫ h)
  let S := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q

  change quotientLeftUnitorDefect W R D S g = Iso.refl _ at hLeftG
  change quotientLeftUnitorDefect W R D S (g ≫ h) = Iso.refl _ at hLeftGH
  have hLG :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D S g).1 hLeftG
  have hLGH :=
    (quotientLeftUnitorDefect_eq_refl_iff W R D S (g ≫ h)).1 hLeftGH

  let eG :
      quotientRepresentativeMap W R D ((𝟙 X) ≫ g) ⟶ G :=
    eqToHom (by simp [G])
  let eGH :
      quotientRepresentativeMap W R D ((𝟙 X) ≫ (g ≫ h)) ⟶ K :=
    eqToHom (by simp [K])
  let eA :
      quotientRepresentativeMap W R D (((𝟙 X) ≫ g) ≫ h) ⟶
        quotientRepresentativeMap W R D ((𝟙 X) ≫ (g ≫ h)) :=
    eqToHom (by simp)
  let eTransport :
      quotientRepresentativeMap W R D (((𝟙 X) ≫ g) ≫ h) ⟶ K :=
    eqToHom (by simp [K])

  change
    (S.mapComp (𝟙 X) g).hom ≫
        (S.mapId X).hom ▷ G ≫
        (λ_ G).hom = eG at hLG
  change
    (S.mapComp (𝟙 X) (g ≫ h)).hom ≫
        (S.mapId X).hom ▷ K ≫
        (λ_ K).hom = eGH at hLGH

  /- Naturality of the dependent mapComp family transports the leading
  mapComp witness along 𝟙≫g=g.  This is transport bookkeeping, not an
  associator-coherence assumption on S. -/
  have hMapCompTransport :
      (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
          (eG ▷ H) ≫
          (S.mapComp g h).inv =
        eTransport := by
    have hNat :=
      eqToHom_iso_hom_naturality_assoc
        (fun k : X ⟶ Z => S.mapComp k h)
        (Category.id_comp g)
        (S.mapComp g h).inv
    simpa [eG, eTransport, G, H, K] using hNat

  have hEqToHomTransport :
      eA ≫ eGH = eTransport := by
    simp [eA, eGH, eTransport]

  have hOuterTransport :
      (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
          (eG ▷ H) ≫
          (S.mapComp g h).inv =
        eA ≫ eGH :=
    hMapCompTransport.trans hEqToHomTransport.symm

  have hExchange :
      (P ◁ (S.mapComp g h).inv) ≫
          ((S.mapId X).hom ▷ K) =
        ((S.mapId X).hom ▷ (G ≫ H)) ≫
          (𝟙 _ ◁ (S.mapComp g h).inv) := by
    exact whisker_exchange (S.mapId X).hom (S.mapComp g h).inv

  have hLeftNaturality :
      (𝟙 _ ◁ (S.mapComp g h).inv) ≫
          (λ_ K).hom =
        (λ_ (G ≫ H)).hom ≫
          (S.mapComp g h).inv := by
    exact leftUnitor_naturality (S.mapComp g h).inv

  have hAssociatorNaturality :
      (((S.mapId X).hom ▷ G) ▷ H) ≫
          (α_ (𝟙 _) G H).hom =
        (α_ P G H).hom ≫
          ((S.mapId X).hom ▷ (G ≫ H)) := by
    simpa [P] using
      associator_naturality_left (S.mapId X).hom G H

  have hLeftWhisker :
      (λ_ G).hom ▷ H =
        (α_ (𝟙 _) G H).hom ≫
          (λ_ (G ≫ H)).hom :=
    leftUnitor_whiskerRight G H

  have hStructural :
      (α_ P G H).hom ≫
          P ◁ (S.mapComp g h).inv ≫
          (S.mapId X).hom ▷ K ≫
          (λ_ K).hom =
        (((S.mapId X).hom ▷ G) ▷ H) ≫
          ((λ_ G).hom ▷ H) ≫
          (S.mapComp g h).inv := by
    calc
      (α_ P G H).hom ≫
          P ◁ (S.mapComp g h).inv ≫
          (S.mapId X).hom ▷ K ≫
          (λ_ K).hom =
          (α_ P G H).hom ≫
            (S.mapId X).hom ▷ (G ≫ H) ≫
            (𝟙 _ ◁ (S.mapComp g h).inv) ≫
            (λ_ K).hom := by
              have hx := congrArg
                (fun k => (α_ P G H).hom ≫ k ≫ (λ_ K).hom)
                hExchange
              simpa only [Category.assoc] using hx
      _ =
          (α_ P G H).hom ≫
            (S.mapId X).hom ▷ (G ≫ H) ≫
            (λ_ (G ≫ H)).hom ≫
            (S.mapComp g h).inv := by
              have hx := congrArg
                (fun k =>
                  (α_ P G H).hom ≫
                    ((S.mapId X).hom ▷ (G ≫ H)) ≫ k)
                hLeftNaturality
              simpa only [Category.assoc] using hx
      _ =
          (((S.mapId X).hom ▷ G) ▷ H) ≫
            (α_ (𝟙 _) G H).hom ≫
            (λ_ (G ≫ H)).hom ≫
            (S.mapComp g h).inv := by
              have hx := congrArg
                (fun k =>
                  k ≫ (λ_ (G ≫ H)).hom ≫
                    (S.mapComp g h).inv)
                hAssociatorNaturality.symm
              simpa only [Category.assoc] using hx
      _ =
          (((S.mapId X).hom ▷ G) ▷ H) ≫
            ((λ_ G).hom ▷ H) ≫
            (S.mapComp g h).inv := by
              have hx := congrArg
                (fun k =>
                  (((S.mapId X).hom ▷ G) ▷ H) ≫
                    k ≫ (S.mapComp g h).inv)
                hLeftWhisker.symm
              simpa only [Category.assoc] using hx

  have hLGwhisk :
      ((S.mapComp (𝟙 X) g).hom ▷ H) ≫
          (((S.mapId X).hom ▷ G) ▷ H) ≫
          ((λ_ G).hom ▷ H) =
        eG ▷ H := by
    have hx := congrArg (fun η => η ▷ H) hLG
    simpa only [comp_whiskerRight, Category.assoc] using hx

  change quotientAssociatorDefect W R D S (𝟙 X) g h = Iso.refl _
  apply
    (quotientAssociatorDefect_eq_refl_iff
      W R D S (𝟙 X) g h).2
  change
    (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
        (S.mapComp (𝟙 X) g).hom ▷ H ≫
        (α_ P G H).hom ≫
        P ◁ (S.mapComp g h).inv ≫
        (S.mapComp (𝟙 X) (g ≫ h)).inv =
      eA

  apply
    (cancel_mono
      ((S.mapComp (𝟙 X) (g ≫ h)).hom ≫
        (S.mapId X).hom ▷ K ≫
        (λ_ K).hom)).1

  calc
    ((S.mapComp ((𝟙 X) ≫ g) h).hom ≫
        (S.mapComp (𝟙 X) g).hom ▷ H ≫
        (α_ P G H).hom ≫
        P ◁ (S.mapComp g h).inv ≫
        (S.mapComp (𝟙 X) (g ≫ h)).inv) ≫
        ((S.mapComp (𝟙 X) (g ≫ h)).hom ≫
          (S.mapId X).hom ▷ K ≫
          (λ_ K).hom) =
      (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
        (S.mapComp (𝟙 X) g).hom ▷ H ≫
        (α_ P G H).hom ≫
        P ◁ (S.mapComp g h).inv ≫
        (S.mapId X).hom ▷ K ≫
        (λ_ K).hom := by
          simp
    _ =
      (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
        (S.mapComp (𝟙 X) g).hom ▷ H ≫
        (((S.mapId X).hom ▷ G) ▷ H) ≫
        ((λ_ G).hom ▷ H) ≫
        (S.mapComp g h).inv := by
          have hx := congrArg
            (fun k =>
              (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
                ((S.mapComp (𝟙 X) g).hom ▷ H) ≫ k)
            hStructural
          simpa only [Category.assoc] using hx
    _ =
      (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
        (eG ▷ H) ≫
        (S.mapComp g h).inv := by
          have hx := congrArg
            (fun k =>
              (S.mapComp ((𝟙 X) ≫ g) h).hom ≫
                k ≫ (S.mapComp g h).inv)
            hLGwhisk
          simpa only [Category.assoc] using hx
    _ = eA ≫ eGH := hOuterTransport
    _ =
      eA ≫
        ((S.mapComp (𝟙 X) (g ≫ h)).hom ≫
          (S.mapId X).hom ▷ K ≫
          (λ_ K).hom) := by
            have hx := congrArg (fun k => eA ≫ k) hLGH.symm
            simpa only [Category.assoc] using hx

/-- Every actual left-identity task is semantically corrected by a gauge that
already corrects all unitors. -/
theorem leftIdentityTask_corrected_of_unitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (a : AssociatorTask W)
    (hLeft : IsLeftIdentityAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rcases hLeft with ⟨X, Z, T, g, h, rfl⟩
  simpa [associatorTaskRoute, leftIdentityAssociatorTask] using
    (leftIdentityAssociator_corrected_of_leftUnitors
      W R D Q g h
      (hUnit X (.left g))
      (hUnit X (.left (g ≫ h))))

/-- Under the v3.49 directional cancellation hypotheses, the remaining
collision residual is corrected by the already common unitor gauge. -/
theorem collisionResidual_corrected_of_epi_mono_of_unitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (a : AssociatorTask W) [Epi a.f] [Mono a.g]
    (hResidual : CollisionResidualAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact leftIdentityTask_corrected_of_unitors
    W R D Q hUnit a
      (collisionResidual_isLeftIdentity_of_epi_mono W a hResidual)

/-- If cancellation is available on every actual collision residual, then the
v3.47 nonresidual + fresh-boundary common-gauge result extends to every
associator task. -/
theorem corrects_all_associators_of_boundaryCompatible_of_collisionCancellation
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hNonresidual :
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a))
    (hBoundaryCompatible :
      ∀ a : AssociatorTask W,
        FreshBoundaryAssociatorTask W a →
          AssociatorLeadingCompatible W R D Q a.f a.g a.h)
    (hCancellation :
      ∀ a : AssociatorTask W,
        CollisionResidualAssociatorTask W a →
          Epi a.f ∧ Mono a.g) :
    ∀ a : AssociatorTask W,
      Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  intro a
  by_cases hResidual : CollisionResidualAssociatorTask W a
  · rcases hCancellation a hResidual with ⟨hEpi, hMono⟩
    letI : Epi a.f := hEpi
    letI : Mono a.g := hMono
    exact collisionResidual_corrected_of_epi_mono_of_unitors
      W R D Q hUnit a hResidual
  · exact
      corrects_all_except_collisionResidual_of_boundaryCompatible
        W R D Q hNonresidual hBoundaryCompatible a hResidual

/-!
## Boundary after v3.50

The left-identity sector created by v3.49 is not a new local obstruction.
For one fixed gauge, its associator equation is a consequence of the two
left-unitor equations at `g` and `g ≫ h`, together with native bicategory
coherence and dependent equality transport.

Therefore the collision residual closes wherever its first arrow is epi and
its middle arrow is mono.  More generally, if those cancellation instances are
available for every actual collision residual, then the v3.47 common-gauge
coverage plus fresh-boundary compatibility extends to all associator tasks.

This does not prove the cancellation premise from weak admissibility, from
coordinate collision, or from arbitrary localization geometry.  Collision
residuals without the required epi/mono witnesses remain open.  Nor are
fresh-boundary compatibility, schedule independence, seed independence,
W/R/D independence, comparison-gauge equations, general Stage I, Stage II, or
final DO universality inferred here.

Protected validation-only #1558 is untouched.
-/

end

end KUOS.DependentOriginationLeftIdentitySemanticRecoveryV3_50
