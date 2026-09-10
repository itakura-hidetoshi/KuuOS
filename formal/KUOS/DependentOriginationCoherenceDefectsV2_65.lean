import KUOS.DependentOriginationFiberIsoThinV2_64

namespace KUOS.DependentOriginationCoherenceDefectsV2_65

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61

universe u v uH vH uC vC

/-!
# Automorphism-valued general-W coherence defects v2.65

The v2.61 layer reduces general-W factorization to five coherence equations,
and v2.64 proves that only invertible 2-dimensional isotropy can obstruct those
equations.  This file makes that statement algebraic.

For two parallel invertible arrows `η θ : X ⟶ Y` in an arbitrary category we
define their defect

```text
δ(η, θ) = η⁻¹ ≪≫ θ : Y ≅ Y.
```

The defect is the identity automorphism exactly when `η = θ`.

We then apply this construction to the three quotient-pseudofunctor laws and,
after those three defects vanish and therefore construct the actual quotient
pseudofunctor, to the two StrongTrans comparison laws.  Thus the dependency is
not circular: the comparison defects are defined only after the transport
defects have produced the required pseudofunctor carrier.

The resulting `FiveCoherenceDefectsTrivial` proposition is a concrete
natural-automorphism-valued obstruction criterion.  Its vanishing constructs the
complete v2.60 coherent package, hence a genuine v2.10 higher-localization
factorization and a coherent extension of the original v2.61 pointwise choices.

No thinness hypothesis, strictification hypothesis, new axiom, `sorry`, or
choice-as-coherence principle is used here.
-/

/-- Difference of two parallel invertible arrows as an automorphism of their
common codomain. -/
noncomputable def parallelIsoDefect
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (η θ : X ⟶ Y) [IsIso η] [IsIso θ] : Y ≅ Y :=
  (asIso η).symm ≪≫ asIso θ

/-- The parallel-arrow defect vanishes exactly when the two invertible arrows
are equal. -/
theorem parallelIsoDefect_eq_refl_iff
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (η θ : X ⟶ Y) [IsIso η] [IsIso θ] :
    parallelIsoDefect η θ = Iso.refl Y ↔ η = θ := by
  constructor
  · intro h
    have hhom : (asIso η).inv ≫ θ = 𝟙 Y := by
      simpa [parallelIsoDefect] using congrArg Iso.hom h
    calc
      η = η ≫ 𝟙 Y := by simp
      _ = η ≫ ((asIso η).inv ≫ θ) := by rw [hhom]
      _ = (η ≫ (asIso η).inv) ≫ θ := by simp only [Category.assoc]
      _ = θ := by simp
  · intro h
    subst θ
    simp [parallelIsoDefect]

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-! ## The three quotient-transport defects -/

/-- Associativity defect of an arbitrary v2.61 pointwise composition choice. -/
noncomputable def quotientAssociatorDefect
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :=
  parallelIsoDefect
    ((L.mapComp (f ≫ g) h).hom ≫
      (L.mapComp f g).hom ▷ quotientRepresentativeMap W R D h ≫
      (α_
        (quotientRepresentativeMap W R D f)
        (quotientRepresentativeMap W R D g)
        (quotientRepresentativeMap W R D h)).hom ≫
      quotientRepresentativeMap W R D f ◁ (L.mapComp g h).inv ≫
      (L.mapComp f (g ≫ h)).inv)
    (eqToHom (by simp))

/-- Left-unit defect of the pointwise quotient transport. -/
noncomputable def quotientLeftUnitorDefect
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y : W.Localization} (f : X ⟶ Y) :=
  parallelIsoDefect
    ((L.mapComp (𝟙 X) f).hom ≫
      (L.mapId X).hom ▷ quotientRepresentativeMap W R D f ≫
      (λ_ (quotientRepresentativeMap W R D f)).hom)
    (eqToHom (by simp))

/-- Right-unit defect of the pointwise quotient transport. -/
noncomputable def quotientRightUnitorDefect
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y : W.Localization} (f : X ⟶ Y) :=
  parallelIsoDefect
    ((L.mapComp f (𝟙 Y)).hom ≫
      quotientRepresentativeMap W R D f ◁ (L.mapId Y).hom ≫
      (ρ_ (quotientRepresentativeMap W R D f)).hom)
    (eqToHom (by simp))

/-- Associator defect is trivial iff the exact v2.59 associativity law holds. -/
theorem quotientAssociatorDefect_eq_refl_iff
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    quotientAssociatorDefect W R D L f g h = Iso.refl _ ↔
      (L.mapComp (f ≫ g) h).hom ≫
          (L.mapComp f g).hom ▷ quotientRepresentativeMap W R D h ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            (quotientRepresentativeMap W R D h)).hom ≫
          quotientRepresentativeMap W R D f ◁ (L.mapComp g h).inv ≫
          (L.mapComp f (g ≫ h)).inv =
        eqToHom (by simp) := by
  unfold quotientAssociatorDefect
  exact parallelIsoDefect_eq_refl_iff _ _

/-- Left-unitor defect is trivial iff the exact v2.59 left-unit law holds. -/
theorem quotientLeftUnitorDefect_eq_refl_iff
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    quotientLeftUnitorDefect W R D L f = Iso.refl _ ↔
      (L.mapComp (𝟙 X) f).hom ≫
          (L.mapId X).hom ▷ quotientRepresentativeMap W R D f ≫
          (λ_ (quotientRepresentativeMap W R D f)).hom =
        eqToHom (by simp) := by
  unfold quotientLeftUnitorDefect
  exact parallelIsoDefect_eq_refl_iff _ _

/-- Right-unitor defect is trivial iff the exact v2.59 right-unit law holds. -/
theorem quotientRightUnitorDefect_eq_refl_iff
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    quotientRightUnitorDefect W R D L f = Iso.refl _ ↔
      (L.mapComp f (𝟙 Y)).hom ≫
          quotientRepresentativeMap W R D f ◁ (L.mapId Y).hom ≫
          (ρ_ (quotientRepresentativeMap W R D f)).hom =
        eqToHom (by simp) := by
  unfold quotientRightUnitorDefect
  exact parallelIsoDefect_eq_refl_iff _ _

/-- Vanishing of the three automorphism-valued quotient defects. -/
structure QuotientTransportDefectsTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) : Prop where
  associator :
    ∀ {X Y Z T : W.Localization}
      (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T),
      quotientAssociatorDefect W R D L f g h = Iso.refl _
  leftUnitor :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      quotientLeftUnitorDefect W R D L f = Iso.refl _
  rightUnitor :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      quotientRightUnitorDefect W R D L f = Iso.refl _

/-- Vanishing of the first three defects constructs the actual coherent quotient
transport while preserving exactly the pointwise `mapId` and `mapComp` choices. -/
noncomputable def coherentQuotientTransportDataOfTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (h : QuotientTransportDefectsTrivial W R D L) :
    CoherentQuotientTransportData (W := W) R D where
  mapId := L.mapId
  mapComp := L.mapComp
  map₂_associator := by
    intro X Y Z T f g k
    exact
      (quotientAssociatorDefect_eq_refl_iff W R D L f g k).mp
        (h.associator f g k)
  map₂_left_unitor := by
    intro X Y f
    exact
      (quotientLeftUnitorDefect_eq_refl_iff W R D L f).mp
        (h.leftUnitor f)
  map₂_right_unitor := by
    intro X Y f
    exact
      (quotientRightUnitorDefect_eq_refl_iff W R D L f).mp
        (h.rightUnitor f)

/-! ## The two comparison defects, defined after transport vanishing -/

/-- Comparison map iso obtained from the original pointwise presentation choice,
now typed against the genuine quotient pseudofunctor constructed from the first
three vanishing defects. -/
noncomputable def comparisonMapIsoOfTrivialTransportDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    {X Y : Context} (f : X ⟶ Y) :
    (restrictedCoherentQuotientSystem W R D
      (coherentQuotientTransportDataOfTrivialDefects W R D L hQ)).map f.toLoc ≅
      R.map f.toLoc := by
  change quotientRepresentativeMap W R D (W.Q.map f) ≅ R.map f.toLoc
  exact L.mapIso f

/-- The StrongTrans naturality iso determined by the pointwise comparison choice
after the quotient transport defects vanish. -/
noncomputable def comparisonNaturalityIsoOfTrivialTransportDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    {X Y : Context} (f : X ⟶ Y) :=
  identityComponentNaturalityIso W R D
    (coherentQuotientTransportDataOfTrivialDefects W R D L hQ)
    f (comparisonMapIsoOfTrivialTransportDefects W R D L hQ f)

/-- Identity coherence defect for the strong comparison. -/
noncomputable def comparisonIdentityDefect
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    (X : Context) :=
  let T := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
  parallelIsoDefect
    ((comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ (𝟙 X)).hom ≫
      (𝟙 (R.obj (.mk X))) ◁ (R.mapId (.mk X)).hom)
    ((restrictedCoherentQuotientSystem W R D T).mapId (.mk X)).hom ▷
        (𝟙 (R.obj (.mk X))) ≫
      (λ_ (𝟙 (R.obj (.mk X)))).hom ≫
      (ρ_ (𝟙 (R.obj (.mk X)))).inv

/-- Composition coherence defect for the strong comparison. -/
noncomputable def comparisonCompositionDefect
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :=
  let T := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
  parallelIsoDefect
    ((comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ (f ≫ g)).hom ≫
      (𝟙 (R.obj (.mk X))) ◁ (R.mapComp f.toLoc g.toLoc).hom)
    ((restrictedCoherentQuotientSystem W R D T).mapComp
        f.toLoc g.toLoc).hom ▷ (𝟙 (R.obj (.mk Z))) ≫
      (α_ _ _ _).hom ≫
      (restrictedCoherentQuotientSystem W R D T).map f.toLoc ◁
        (comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ g).hom ≫
      (α_ _ _ _).inv ≫
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ f).hom ▷
        R.map g.toLoc ≫
      (α_ _ _ _).hom

/-- Identity comparison defect is trivial exactly when the v2.60 identity law
holds for the induced pointwise comparison. -/
theorem comparisonIdentityDefect_eq_refl_iff
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    (X : Context) :
    comparisonIdentityDefect W R D L hQ X = Iso.refl _ ↔
      let T := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ (𝟙 X)).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapId (.mk X)).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapId (.mk X)).hom ▷
            (𝟙 (R.obj (.mk X))) ≫
          (λ_ (𝟙 (R.obj (.mk X)))).hom ≫
          (ρ_ (𝟙 (R.obj (.mk X)))).inv := by
  dsimp [comparisonIdentityDefect]
  exact parallelIsoDefect_eq_refl_iff _ _

/-- Composition comparison defect is trivial exactly when the v2.60 composition
law holds. -/
theorem comparisonCompositionDefect_eq_refl_iff
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
    comparisonCompositionDefect W R D L hQ f g = Iso.refl _ ↔
      let T := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
      (comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ (f ≫ g)).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapComp f.toLoc g.toLoc).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapComp
            f.toLoc g.toLoc).hom ▷ (𝟙 (R.obj (.mk Z))) ≫
          (α_ _ _ _).hom ≫
          (restrictedCoherentQuotientSystem W R D T).map f.toLoc ◁
            (comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ g).hom ≫
          (α_ _ _ _).inv ≫
          (comparisonNaturalityIsoOfTrivialTransportDefects W R D L hQ f).hom ▷
            R.map g.toLoc ≫
          (α_ _ _ _).hom := by
  dsimp [comparisonCompositionDefect]
  exact parallelIsoDefect_eq_refl_iff _ _

/-- Vanishing of the two comparison defects after the quotient defects vanish. -/
structure ComparisonDefectsTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L) : Prop where
  identity :
    ∀ X : Context,
      comparisonIdentityDefect W R D L hQ X = Iso.refl _
  composition :
    ∀ {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z),
      comparisonCompositionDefect W R D L hQ f g = Iso.refl _

/-- Vanishing comparison defects construct the exact v2.60 comparison data. -/
noncomputable def coherentPresentationComparisonDataOfTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hQ : QuotientTransportDefectsTrivial W R D L)
    (hC : ComparisonDefectsTrivial W R D L hQ) :
    CoherentPresentationComparisonData (W := W) R D
      (coherentQuotientTransportDataOfTrivialDefects W R D L hQ) where
  mapIso := comparisonMapIsoOfTrivialTransportDefects W R D L hQ
  naturality_id := by
    intro X
    exact
      (comparisonIdentityDefect_eq_refl_iff W R D L hQ X).mp
        (hC.identity X)
  naturality_comp := by
    intro X Y Z f g
    exact
      (comparisonCompositionDefect_eq_refl_iff W R D L hQ f g).mp
        (hC.composition f g)

/-- All five automorphism-valued defects vanish: first the three quotient
transport defects, then the two comparison defects on the resulting carrier. -/
def FiveCoherenceDefectsTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) : Prop :=
  ∃ hQ : QuotientTransportDefectsTrivial W R D L,
    ComparisonDefectsTrivial W R D L hQ

/-- Five defect vanishing constructs the complete v2.60 coherent package. -/
noncomputable def coherentGeneralWFactorizationDataOfFiveTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (h : FiveCoherenceDefectsTrivial W R D L) :
    CoherentGeneralWFactorizationData (W := W) R D := by
  rcases h with ⟨hQ, hC⟩
  exact
    { transport := coherentQuotientTransportDataOfTrivialDefects W R D L hQ
      comparison :=
        coherentPresentationComparisonDataOfTrivialDefects W R D L hQ hC }

/-- Vanishing of all five defects therefore gives the genuine higher-localization
factorization. -/
theorem hasHigherLocalizationFactorization_of_fiveTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (h : FiveCoherenceDefectsTrivial W R D L) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
    W R D ⟨coherentGeneralWFactorizationDataOfFiveTrivialDefects W R D L h⟩

/-- The constructed coherent package retains exactly the original v2.61 local
choice bundle. -/
theorem pointwiseChoiceData_of_fiveTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (h : FiveCoherenceDefectsTrivial W R D L) :
    pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D
      (coherentGeneralWFactorizationDataOfFiveTrivialDefects W R D L h) = L := by
  rcases h with ⟨hQ, hC⟩
  cases L
  rfl

/-- Hence five-defect vanishing is a genuine sufficient criterion for the exact
v2.61 coherent-extension predicate, not merely for some unrelated coherent
choice. -/
theorem hasCoherentExtension_of_fiveTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (h : FiveCoherenceDefectsTrivial W R D L) :
    HasCoherentExtension W R D L :=
  ⟨coherentGeneralWFactorizationDataOfFiveTrivialDefects W R D L h,
    pointwiseChoiceData_of_fiveTrivialDefects W R D L h⟩

/-!
## Boundary fixed by v2.65

For a fixed v2.61 pointwise local choice `L`, the coherence frontier is now
expressed by five explicit automorphism-valued defects:

```text
δ_assoc, δ_left, δ_right
        ↓ vanish
actual quotient pseudofunctor T
        ↓
δ_comparison_id, δ_comparison_comp
        ↓ vanish
CoherentGeneralWFactorizationData
        ↓
HigherLocalizationFactorization W R.
```

Thus the remaining unrestricted problem is no longer an unspecified request for
"coherence".  It is the concrete existence problem

```text
IsHigherWAdmissible W R
  ⇒ ∃ L : PointwiseGeneralWChoiceData,
       FiveCoherenceDefectsTrivial W R D L.
```

Version 2.64 is recovered conceptually because if the relevant invertible
2-isotropy is trivial, every defect automorphism is forced to be the identity.
In the unrestricted case these defects may be nontrivial, and the next problem is
to understand how they transform when the pointwise choices `mapId`, `mapComp`,
and `mapIso` are changed.  That is the precise gauge/obstruction-theoretic
frontier.

No claim is made here that an arbitrary pointwise choice has trivial defects, nor
that weak admissibility alone already proves their vanishing.
-/

end KUOS.DependentOriginationCoherenceDefectsV2_65
