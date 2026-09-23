import KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52

namespace KUOS.DependentOriginationFreshBoundaryRightIdentityReductionV3_53

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
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCollisionObjectGeometryV3_48
open KUOS.DependentOriginationCollisionAbsorptionReductionV3_49
open KUOS.DependentOriginationLeftIdentitySemanticRecoveryV3_50
open KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Fresh-boundary right-identity reduction v3.53

v3.47 proves that a fresh but unitor-visible associator has its leading
composition coordinate equal to one of two literal unit-composition keys:

* `composition (𝟙 A) k`;
* `composition k (𝟙 B)`.

These two branches are not semantically symmetric.

The second branch forces the third associator arrow itself to be an identity.
This layer proves that the resulting right-identity associator

```text
associator f g (𝟙 Z)
```

is already corrected by one fixed gauge as soon as that same gauge corrects
the right-unit routes at `g` and `f ≫ g`.  This is the right-hand analogue
of v3.50's left-identity semantic recovery, and it uses only the actual defect
equations plus native bicategory coherence.

The first branch instead forces the composite `f ≫ g` to be identity.  We
retain that branch explicitly rather than pretending it is another ordinary
unitor route.

Consequently the v3.47 fresh-boundary compatibility hypothesis can be reduced
to the composite-identity branch only.  No claim is made here that
`f ≫ g = 𝟙` itself forces correction.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Package the right-identity associator shape. -/
def rightIdentityAssociatorTask
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    AssociatorTask W where
  X := X
  Y := Y
  Z := Z
  T := Z
  f := f
  g := g
  h := 𝟙 Z

/-- The sector in which the third associator arrow is literally an identity. -/
def IsRightIdentityAssociatorTask (a : AssociatorTask W) : Prop :=
  ∃ (X Y Z : W.Localization) (f : X ⟶ Y) (g : Y ⟶ Z),
    a = rightIdentityAssociatorTask W f g

/-- Package the other unit-visible leading branch: after the dependent endpoint
identifications, the first two associator arrows compose to identity. -/
def IsCompositeIdentityAssociatorTask (a : AssociatorTask W) : Prop :=
  ∃ (X Y T : W.Localization)
      (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T),
    f ≫ g = 𝟙 X ∧
      a =
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W)

/-- A leading coordinate equal to a left-unit composition key forces the
composite of the first two associator arrows to be identity. -/
theorem leading_eq_leftUnitComposition_isCompositeIdentity
    (a : AssociatorTask W)
    (hLeft :
      ∃ (A B : W.Localization) (k : A ⟶ B),
        associatorTaskLeadingCoordinate W a =
          .composition (𝟙 A) k) :
    IsCompositeIdentityAssociatorTask W a := by
  rcases hLeft with ⟨A, B, k, hEq⟩
  rcases a with ⟨X, Y, Z, T, f, g, h⟩
  change
    (QuotientGaugeCoordinate.composition (f ≫ g) h :
      QuotientGaugeCoordinate W) =
        QuotientGaugeCoordinate.composition (𝟙 A) k at hEq
  have hSource := congrArg (quotientCoordinateSource W) hEq
  have hMiddle := congrArg (quotientCoordinateMiddle W) hEq
  have hTarget := congrArg (quotientCoordinateTarget W) hEq
  change X = A at hSource
  change Z = A at hMiddle
  change T = B at hTarget
  subst A
  subst Z
  subst B
  have hMorph :=
    compositionCoordinate_eq_sameEndpoints W hEq
  exact ⟨X, Y, T, f, g, h, hMorph.1, rfl⟩

/-- A leading coordinate equal to a right-unit composition key forces the
third associator arrow to be identity. -/
theorem leading_eq_rightUnitComposition_isRightIdentity
    (a : AssociatorTask W)
    (hRight :
      ∃ (A B : W.Localization) (k : A ⟶ B),
        associatorTaskLeadingCoordinate W a =
          .composition k (𝟙 B)) :
    IsRightIdentityAssociatorTask W a := by
  rcases hRight with ⟨A, B, k, hEq⟩
  rcases a with ⟨X, Y, Z, T, f, g, h⟩
  change
    (QuotientGaugeCoordinate.composition (f ≫ g) h :
      QuotientGaugeCoordinate W) =
        QuotientGaugeCoordinate.composition k (𝟙 B) at hEq
  have hSource := congrArg (quotientCoordinateSource W) hEq
  have hMiddle := congrArg (quotientCoordinateMiddle W) hEq
  have hTarget := congrArg (quotientCoordinateTarget W) hEq
  change X = A at hSource
  change Z = B at hMiddle
  change T = B at hTarget
  subst A
  subst B
  subst T
  have hMorph :=
    compositionCoordinate_eq_sameEndpoints W hEq
  have hh : h = 𝟙 Z := hMorph.2
  subst h
  exact ⟨X, Y, Z, f, g, rfl⟩

/-- Therefore every fresh-boundary task lies in exactly the two semantic shapes
relevant for the next reduction.  No morphism identity is inferred without
first normalizing the dependent coordinate equality. -/
theorem freshBoundary_reduces_to_compositeIdentity_or_rightIdentity
    (a : AssociatorTask W)
    (hBoundary : FreshBoundaryAssociatorTask W a) :
    IsCompositeIdentityAssociatorTask W a ∨
      IsRightIdentityAssociatorTask W a := by
  rcases freshBoundary_leading_is_unitComposition W a hBoundary with
    hLeft | hRight
  · exact Or.inl
      (leading_eq_leftUnitComposition_isCompositeIdentity W a hLeft)
  · exact Or.inr
      (leading_eq_rightUnitComposition_isRightIdentity W a hRight)

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- The two right-unitor equations of one fixed gauge imply its
right-identity associator equation. -/
theorem rightIdentityAssociator_corrected_of_rightUnitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hRightG :
      Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor g))
    (hRightFG :
      Q ∈ quotientRouteCorrectionLocus W R D (.rightUnitor (f ≫ g))) :
    Q ∈ quotientRouteCorrectionLocus W R D
      (.associator f g (𝟙 Z)) := by
  let F := quotientRepresentativeMap W R D f
  let G := quotientRepresentativeMap W R D g
  let P := quotientRepresentativeMap W R D (𝟙 Z)
  let K := quotientRepresentativeMap W R D (f ≫ g)
  let S := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q

  change quotientRightUnitorDefect W R D S g = Iso.refl _ at hRightG
  change quotientRightUnitorDefect W R D S (f ≫ g) = Iso.refl _ at hRightFG
  have hRG :=
    (quotientRightUnitorDefect_eq_refl_iff W R D S g).1 hRightG
  have hRFG :=
    (quotientRightUnitorDefect_eq_refl_iff W R D S (f ≫ g)).1 hRightFG

  let eG :
      quotientRepresentativeMap W R D (g ≫ 𝟙 Z) ⟶ G :=
    eqToHom (by simp [G])
  let eK :
      quotientRepresentativeMap W R D ((f ≫ g) ≫ 𝟙 Z) ⟶ K :=
    eqToHom (by simp [K])
  let eFG :
      quotientRepresentativeMap W R D (f ≫ (g ≫ 𝟙 Z)) ⟶ K :=
    eqToHom (by simp [K])
  let eA :
      quotientRepresentativeMap W R D ((f ≫ g) ≫ 𝟙 Z) ⟶
        quotientRepresentativeMap W R D (f ≫ (g ≫ 𝟙 Z)) :=
    eqToHom (by simp)

  change
    (S.mapComp g (𝟙 Z)).hom ≫
        G ◁ (S.mapId Z).hom ≫
        (ρ_ G).hom = eG at hRG
  change
    (S.mapComp (f ≫ g) (𝟙 Z)).hom ≫
        K ◁ (S.mapId Z).hom ≫
        (ρ_ K).hom = eK at hRFG

  /- Naturality of the dependent family k ↦ mapComp f k along g≫𝟙=g.
  This is only equality transport; no associator law for S is assumed. -/
  have hMapCompTransport :
      (S.mapComp f (g ≫ 𝟙 Z)).hom ≫
          F ◁ eG =
        eFG ≫ (S.mapComp f g).hom := by
    have hNat :=
      eqToHom_iso_hom_naturality
        (fun k : Y ⟶ Z => S.mapComp f k)
        (Category.comp_id g)
    simpa [eG, eFG, F, G, K] using hNat

  have hEqToHomTransport :
      eA ≫ eFG = eK := by
    simp [eA, eFG, eK]

  have hOuterTransport :
      eA ≫
          (S.mapComp f (g ≫ 𝟙 Z)).hom ≫
          F ◁ eG =
        eK ≫ (S.mapComp f g).hom := by
    calc
      eA ≫
          (S.mapComp f (g ≫ 𝟙 Z)).hom ≫
          F ◁ eG =
        eA ≫ eFG ≫ (S.mapComp f g).hom := by
          have hx := congrArg (fun k => eA ≫ k) hMapCompTransport
          simpa only [Category.assoc] using hx
      _ = eK ≫ (S.mapComp f g).hom := by
          rw [hEqToHomTransport]

  have hRGwhisk :
      F ◁ (S.mapComp g (𝟙 Z)).hom ≫
          F ◁ (G ◁ (S.mapId Z).hom) ≫
          F ◁ (ρ_ G).hom =
        F ◁ eG := by
    have hx := congrArg (fun η => F ◁ η) hRG
    simpa only [whiskerLeft_comp, Category.assoc] using hx

  have hAssocNaturality :
      (F ≫ G) ◁ (S.mapId Z).hom ≫
          (α_ F G (𝟙 _)).hom =
        (α_ F G P).hom ≫
          F ◁ (G ◁ (S.mapId Z).hom) := by
    simpa only [P] using
      associator_naturality_right F G (S.mapId Z).hom

  have hExchange :
      (K ◁ (S.mapId Z).hom) ≫
          ((S.mapComp f g).hom ▷ 𝟙 _) =
        ((S.mapComp f g).hom ▷ P) ≫
          ((F ≫ G) ◁ (S.mapId Z).hom) := by
    exact whisker_exchange (S.mapComp f g).hom (S.mapId Z).hom

  have hRightComp :
      (ρ_ (F ≫ G)).hom =
        (α_ F G (𝟙 _)).hom ≫
          F ◁ (ρ_ G).hom :=
    rightUnitor_comp F G

  have hRightNaturality :
      ((S.mapComp f g).hom ▷ 𝟙 _) ≫
          (ρ_ (F ≫ G)).hom =
        (ρ_ K).hom ≫
          (S.mapComp f g).hom :=
    rightUnitor_naturality (S.mapComp f g).hom

  have hStructural :
      ((S.mapComp f g).hom ▷ P) ≫
          (α_ F G P).hom ≫
          F ◁ (G ◁ (S.mapId Z).hom) ≫
          F ◁ (ρ_ G).hom =
        (K ◁ (S.mapId Z).hom) ≫
          (ρ_ K).hom ≫
          (S.mapComp f g).hom := by
    calc
      ((S.mapComp f g).hom ▷ P) ≫
          (α_ F G P).hom ≫
          F ◁ (G ◁ (S.mapId Z).hom) ≫
          F ◁ (ρ_ G).hom =
        ((S.mapComp f g).hom ▷ P) ≫
          ((F ≫ G) ◁ (S.mapId Z).hom) ≫
          (α_ F G (𝟙 _)).hom ≫
          F ◁ (ρ_ G).hom := by
            have hx := congrArg
              (fun k =>
                ((S.mapComp f g).hom ▷ P) ≫
                  k ≫ F ◁ (ρ_ G).hom)
              hAssocNaturality.symm
            simpa only [Category.assoc] using hx
      _ =
        (K ◁ (S.mapId Z).hom) ≫
          ((S.mapComp f g).hom ▷ 𝟙 _) ≫
          (α_ F G (𝟙 _)).hom ≫
          F ◁ (ρ_ G).hom := by
            have hx := congrArg
              (fun k =>
                k ≫ (α_ F G (𝟙 _)).hom ≫
                  F ◁ (ρ_ G).hom)
              hExchange.symm
            simpa only [Category.assoc] using hx
      _ =
        (K ◁ (S.mapId Z).hom) ≫
          ((S.mapComp f g).hom ▷ 𝟙 _) ≫
          (ρ_ (F ≫ G)).hom := by
            have hx := congrArg
              (fun k =>
                (K ◁ (S.mapId Z).hom) ≫
                  ((S.mapComp f g).hom ▷ 𝟙 _) ≫ k)
              hRightComp.symm
            simpa only [Category.assoc] using hx
      _ =
        (K ◁ (S.mapId Z).hom) ≫
          (ρ_ K).hom ≫
          (S.mapComp f g).hom := by
            have hx := congrArg
              (fun k => (K ◁ (S.mapId Z).hom) ≫ k)
              hRightNaturality
            simpa only [Category.assoc] using hx

  change quotientAssociatorDefect W R D S f g (𝟙 Z) = Iso.refl _
  apply
    (quotientAssociatorDefect_eq_refl_iff
      W R D S f g (𝟙 Z)).2
  change
    (S.mapComp (f ≫ g) (𝟙 Z)).hom ≫
        (S.mapComp f g).hom ▷ P ≫
        (α_ F G P).hom ≫
        F ◁ (S.mapComp g (𝟙 Z)).inv ≫
        (S.mapComp f (g ≫ 𝟙 Z)).inv =
      eA

  /- Cancel one common invertible suffix.  Its first two factors undo the two
  inverse mapComp factors in the associator equation; the remaining factors
  are exactly the right-unitor suffix at g. -/
  apply
    (cancel_mono
      ((S.mapComp f (g ≫ 𝟙 Z)).hom ≫
        F ◁ (S.mapComp g (𝟙 Z)).hom ≫
        F ◁ (G ◁ (S.mapId Z).hom) ≫
        F ◁ (ρ_ G).hom)).1

  calc
    ((S.mapComp (f ≫ g) (𝟙 Z)).hom ≫
        (S.mapComp f g).hom ▷ P ≫
        (α_ F G P).hom ≫
        F ◁ (S.mapComp g (𝟙 Z)).inv ≫
        (S.mapComp f (g ≫ 𝟙 Z)).inv) ≫
        ((S.mapComp f (g ≫ 𝟙 Z)).hom ≫
          F ◁ (S.mapComp g (𝟙 Z)).hom ≫
          F ◁ (G ◁ (S.mapId Z).hom) ≫
          F ◁ (ρ_ G).hom) =
      (S.mapComp (f ≫ g) (𝟙 Z)).hom ≫
        (S.mapComp f g).hom ▷ P ≫
        (α_ F G P).hom ≫
        F ◁ (G ◁ (S.mapId Z).hom) ≫
        F ◁ (ρ_ G).hom := by
          simp
    _ =
      (S.mapComp (f ≫ g) (𝟙 Z)).hom ≫
        (K ◁ (S.mapId Z).hom) ≫
        (ρ_ K).hom ≫
        (S.mapComp f g).hom := by
          have hx := congrArg
            (fun k =>
              (S.mapComp (f ≫ g) (𝟙 Z)).hom ≫ k)
            hStructural
          simpa only [Category.assoc] using hx
    _ = eK ≫ (S.mapComp f g).hom := by
          have hx := congrArg
            (fun k => k ≫ (S.mapComp f g).hom)
            hRFG
          simpa only [Category.assoc] using hx
    _ =
      eA ≫
        (S.mapComp f (g ≫ 𝟙 Z)).hom ≫
        F ◁ eG := hOuterTransport.symm
    _ =
      eA ≫
        (S.mapComp f (g ≫ 𝟙 Z)).hom ≫
        F ◁ (S.mapComp g (𝟙 Z)).hom ≫
        F ◁ (G ◁ (S.mapId Z).hom) ≫
        F ◁ (ρ_ G).hom := by
          have hx := congrArg
            (fun k =>
              eA ≫
                (S.mapComp f (g ≫ 𝟙 Z)).hom ≫ k)
            hRGwhisk.symm
          simpa only [Category.assoc] using hx

/-- Every actual right-identity task is semantically corrected by a gauge that
already corrects all unitors. -/
theorem rightIdentityTask_corrected_of_unitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (a : AssociatorTask W)
    (hRight : IsRightIdentityAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rcases hRight with ⟨X, Y, Z, f, g, rfl⟩
  simpa [associatorTaskRoute, rightIdentityAssociatorTask] using
    (rightIdentityAssociator_corrected_of_rightUnitors
      W R D Q f g
      (hUnit Z (.right g))
      (hUnit Z (.right (f ≫ g))))

/-- Under a common unitor gauge, a fresh-boundary obstruction can survive only
in the composite-identity branch. -/
theorem freshBoundaryLeadingObstruction_isCompositeIdentity_of_unitors
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (a : AssociatorTask W)
    (hObstruction : FreshBoundaryLeadingObstruction W R D Q a) :
    IsCompositeIdentityAssociatorTask W a := by
  have hBoundary : FreshBoundaryAssociatorTask W a := hObstruction.1
  rcases
      freshBoundary_reduces_to_compositeIdentity_or_rightIdentity
        W a hBoundary with hComposite | hRight
  · exact hComposite
  · have hCorrect :=
      rightIdentityTask_corrected_of_unitors
        W R D Q hUnit a hRight
    have hCompatible :=
      (freshBoundaryTask_corrected_iff_leadingCompatible
        W R D Q a hBoundary).1 hCorrect
    exact False.elim (hObstruction.2 hCompatible)

/-- It is enough to impose the v3.47 compatibility equation only on
fresh-boundary tasks in the composite-identity branch.  The right-identity
branch is regenerated semantically from the common right unitors. -/
theorem corrects_all_associators_of_compositeBoundaryCompatible_of_sourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hNonresidual :
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a))
    (hCompositeBoundaryCompatible :
      ∀ a : AssociatorTask W,
        FreshBoundaryAssociatorTask W a →
          IsCompositeIdentityAssociatorTask W a →
            AssociatorLeadingCompatible W R D Q a.f a.g a.h)
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∀ a : AssociatorTask W,
      Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  apply
    corrects_all_associators_of_boundaryCompatible_of_sourceComplements
      W R D Q hUnit hNonresidual
  · intro a hBoundary
    rcases
        freshBoundary_reduces_to_compositeIdentity_or_rightIdentity
          W a hBoundary with hComposite | hRightIdentity
    · exact hCompositeBoundaryCompatible a hBoundary hComposite
    · have hCorrect :=
        rightIdentityTask_corrected_of_unitors
          W R D Q hUnit a hRightIdentity
      exact
        (freshBoundaryTask_corrected_iff_leadingCompatible
          W R D Q a hBoundary).1 hCorrect
  · exact hLeft
  · exact hRight

/-!
## Boundary after v3.53

The v3.47 fresh-boundary obstruction is now smaller.

The branch in which the leading key is right-unit-visible is an actual
right-identity associator and is automatically corrected by the already common
right-unit equations.  Any remaining fresh-boundary obstruction must therefore
lie over the strict source equation

```text
f ≫ g = 𝟙.
```

This is not yet a proof that the composite-identity branch is corrected.  Even
under v3.52, where all localization arrows are epi and mono from global source
complements, the equation `f ≫ g = 𝟙` does not by itself identify either
factor with an identity, and the associator equation still contains the
nontrivial `mapComp f g` coordinate.

The next theorem unit should truth-test whether this remaining branch can be
closed from split/isomorphism data plus already correlated unitors, or whether
it carries an independent compatibility obstruction.

No weak-admissibility derivation of source complements, schedule/seed/W/R/D
independence, comparison `gIso` equations, general Stage I, Stage II, or final
DO universality is asserted.  Protected validation-only #1558 is untouched.
-/

end

end KUOS.DependentOriginationFreshBoundaryRightIdentityReductionV3_53
