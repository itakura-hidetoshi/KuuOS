import KUOS.DependentOriginationCoherenceDefectsV2_65

namespace KUOS.DependentOriginationGaugeObstructionV2_66

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationCoherenceDefectsV2_65

universe u v uH vH uC vC

/-!
# Gauge orbit of the general-W coherence obstruction v2.66

Version 2.65 turns the remaining general-`W` coherence problem into five explicit
automorphism-valued defects attached to a pointwise choice bundle `L`.
This layer removes the accidental dependence on which pointwise witnesses were
chosen.

There are three kinds of local witnesses in v2.61: `mapId`, `mapComp`, and
`mapIso`.  Two witnesses of the same kind have the same source and target, so
they differ by a unique *chosen* automorphism of their common target once the two
witnesses themselves are fixed.  We package those right-acting automorphisms as
a gauge between pointwise choice bundles.

The main statements are:

* the generic defect obeys the expected two-sided gauge transformation law;
* every two v2.61 pointwise choice bundles are gauge-related, so the choice
  space is one gauge orbit;
* a coherent v2.60 package projects to a pointwise choice whose five v2.65
  defects vanish;
* therefore existence of coherent general-`W` data is equivalent to
  gauge-trivializability of the canonical v2.61 pointwise choice.

This does not assert that the gauge-trivialization exists from weak
`W`-admissibility alone.  It identifies the remaining unrestricted problem as a
well-defined obstruction problem on a single gauge orbit.
-/

/-! ## Generic gauge law for the automorphism-valued defect -/

/-- Right-changing the two parallel invertible arrows by automorphisms `a,b`
changes their defect by `a⁻¹ δ b`. -/
theorem parallelIsoDefect_postcompose
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (η θ : X ⟶ Y) [IsIso η] [IsIso θ]
    (a b : Y ≅ Y) :
    parallelIsoDefect (η ≫ a.hom) (θ ≫ b.hom) =
      a.symm ≪≫ parallelIsoDefect η θ ≪≫ b := by
  apply Iso.ext
  simp only [parallelIsoDefect, Iso.trans_hom, Iso.symm_hom, asIso_hom,
    asIso_inv, IsIso.inv_comp, Category.assoc]
  simp

/-- Common precomposition does not change the defect. -/
theorem parallelIsoDefect_precompose
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (η θ : X ⟶ Y) [IsIso η] [IsIso θ]
    (a : X ≅ X) :
    parallelIsoDefect (a.hom ≫ η) (a.hom ≫ θ) =
      parallelIsoDefect η θ := by
  apply Iso.ext
  simp only [parallelIsoDefect, Iso.trans_hom, Iso.symm_hom, asIso_hom,
    asIso_inv, IsIso.inv_comp, Category.assoc]
  simp

/-- Simultaneous right gauge change acts on the defect by conjugation. -/
theorem parallelIsoDefect_postcompose_same
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (η θ : X ⟶ Y) [IsIso η] [IsIso θ]
    (a : Y ≅ Y) :
    parallelIsoDefect (η ≫ a.hom) (θ ≫ a.hom) =
      a.symm ≪≫ parallelIsoDefect η θ ≪≫ a :=
  parallelIsoDefect_postcompose η θ a a

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-! ## Gauge transformations between v2.61 pointwise choices -/

/-- A gauge from one pointwise choice bundle to another.

The gauge acts on the right of each chosen local isomorphism.  The three
`fac` fields state that the target pointwise choice is obtained by that action.
No coherence equation is imposed on the gauge itself: these are precisely the
zero-dimensional local witness changes whose higher compatibility is measured
by the v2.65 defects. -/
structure PointwiseChoiceGauge
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L L' : PointwiseGeneralWChoiceData (W := W) R D) where
  mapIdGauge :
    ∀ X : W.Localization,
      (𝟙 (R.obj (.mk X.as.obj))) ≅ 𝟙 (R.obj (.mk X.as.obj))
  mapId_fac :
    ∀ X : W.Localization,
      L.mapId X ≪≫ mapIdGauge X = L'.mapId X
  mapCompGauge :
    ∀ {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      (quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g) ≅
        (quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g)
  mapComp_fac :
    ∀ {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      L.mapComp f g ≪≫ mapCompGauge f g = L'.mapComp f g
  mapIsoGauge :
    ∀ {X Y : Context} (f : X ⟶ Y),
      R.map f.toLoc ≅ R.map f.toLoc
  mapIso_fac :
    ∀ {X Y : Context} (f : X ⟶ Y),
      L.mapIso f ≪≫ mapIsoGauge f = L'.mapIso f

/-- Any two pointwise choices have an explicit gauge between them: take the
right quotient `e⁻¹ e'` in each local Iso torsor. -/
noncomputable def pointwiseChoiceGaugeBetween
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L L' : PointwiseGeneralWChoiceData (W := W) R D) :
    PointwiseChoiceGauge W R D L L' where
  mapIdGauge X := (L.mapId X).symm ≪≫ L'.mapId X
  mapId_fac X := by
    apply Iso.ext
    simp
  mapCompGauge f g := (L.mapComp f g).symm ≪≫ L'.mapComp f g
  mapComp_fac f g := by
    apply Iso.ext
    simp
  mapIsoGauge f := (L.mapIso f).symm ≪≫ L'.mapIso f
  mapIso_fac f := by
    apply Iso.ext
    simp

/-- Gauge-equivalence of pointwise choice bundles. -/
def PointwiseChoicesGaugeEquivalent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L L' : PointwiseGeneralWChoiceData (W := W) R D) : Prop :=
  Nonempty (PointwiseChoiceGauge W R D L L')

/-- The pointwise-choice space is a single gauge orbit. -/
theorem pointwiseChoicesGaugeEquivalent_all
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L L' : PointwiseGeneralWChoiceData (W := W) R D) :
    PointwiseChoicesGaugeEquivalent W R D L L' :=
  ⟨pointwiseChoiceGaugeBetween W R D L L'⟩

/-- In particular gauge-equivalence is reflexive. -/
theorem pointwiseChoicesGaugeEquivalent_refl
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    PointwiseChoicesGaugeEquivalent W R D L L :=
  pointwiseChoicesGaugeEquivalent_all W R D L L

/-- Gauge-equivalence is symmetric. -/
theorem pointwiseChoicesGaugeEquivalent_symm
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {L L' : PointwiseGeneralWChoiceData (W := W) R D}
    (_ : PointwiseChoicesGaugeEquivalent W R D L L') :
    PointwiseChoicesGaugeEquivalent W R D L' L :=
  pointwiseChoicesGaugeEquivalent_all W R D L' L

/-- Gauge-equivalence is transitive. -/
theorem pointwiseChoicesGaugeEquivalent_trans
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {L₁ L₂ L₃ : PointwiseGeneralWChoiceData (W := W) R D}
    (_ : PointwiseChoicesGaugeEquivalent W R D L₁ L₂)
    (_ : PointwiseChoicesGaugeEquivalent W R D L₂ L₃) :
    PointwiseChoicesGaugeEquivalent W R D L₁ L₃ :=
  pointwiseChoicesGaugeEquivalent_all W R D L₁ L₃

/-! ## Recovering vanishing defects from coherent data -/

/-- The pointwise projection of a coherent v2.60 package has vanishing three
quotient-transport defects. -/
noncomputable def quotientTransportDefectsTrivialOfCoherentData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : CoherentGeneralWFactorizationData (W := W) R D) :
    QuotientTransportDefectsTrivial W R D
      (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H) where
  associator f g h := by
    apply
      (quotientAssociatorDefect_eq_refl_iff W R D
        (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H)
        f g h).2
    simpa [pointwiseChoiceDataOfCoherentGeneralWFactorizationData] using
      H.transport.map₂_associator f g h
  leftUnitor f := by
    apply
      (quotientLeftUnitorDefect_eq_refl_iff W R D
        (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H) f).2
    simpa [pointwiseChoiceDataOfCoherentGeneralWFactorizationData] using
      H.transport.map₂_left_unitor f
  rightUnitor f := by
    apply
      (quotientRightUnitorDefect_eq_refl_iff W R D
        (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H) f).2
    simpa [pointwiseChoiceDataOfCoherentGeneralWFactorizationData] using
      H.transport.map₂_right_unitor f

/-- Rebuilding coherent transport from the projected pointwise data and the
vanishing defects returns the original transport.  Only proof fields can differ,
and those are propositionally irrelevant. -/
theorem reconstructedTransportOfCoherentData_eq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : CoherentGeneralWFactorizationData (W := W) R D) :
    coherentQuotientTransportDataOfTrivialDefects W R D
        (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H)
        (quotientTransportDefectsTrivialOfCoherentData W R D H) =
      H.transport := by
  cases H with
  | mk T C =>
      cases T
      rfl

/-- The same projected coherent package has vanishing two StrongTrans comparison
defects on the reconstructed quotient carrier. -/
noncomputable def comparisonDefectsTrivialOfCoherentData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : CoherentGeneralWFactorizationData (W := W) R D) :
    ComparisonDefectsTrivial W R D
      (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H)
      (quotientTransportDefectsTrivialOfCoherentData W R D H) where
  identity X := by
    apply
      (comparisonIdentityDefect_eq_refl_iff W R D
        (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H)
        (quotientTransportDefectsTrivialOfCoherentData W R D H) X).2
    have hT := reconstructedTransportOfCoherentData_eq W R D H
    simpa [pointwiseChoiceDataOfCoherentGeneralWFactorizationData,
      comparisonNaturalityIsoOfTrivialTransportDefects,
      comparisonMapIsoOfTrivialTransportDefects, hT] using
      H.comparison.naturality_id X
  composition f g := by
    apply
      (comparisonCompositionDefect_eq_refl_iff W R D
        (pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H)
        (quotientTransportDefectsTrivialOfCoherentData W R D H) f g).2
    have hT := reconstructedTransportOfCoherentData_eq W R D H
    simpa [pointwiseChoiceDataOfCoherentGeneralWFactorizationData,
      comparisonNaturalityIsoOfTrivialTransportDefects,
      comparisonMapIsoOfTrivialTransportDefects, hT] using
      H.comparison.naturality_comp f g

/-- Every complete coherent package therefore determines a pointwise choice with
all five explicit v2.65 defects trivial. -/
theorem exists_fiveTrivialDefects_of_hasCoherentGeneralWFactorizationData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : HasCoherentGeneralWFactorizationData W R D) :
    ∃ L : PointwiseGeneralWChoiceData (W := W) R D,
      FiveCoherenceDefectsTrivial W R D L := by
  rcases h with ⟨H⟩
  refine
    ⟨pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H,
      quotientTransportDefectsTrivialOfCoherentData W R D H, ?_⟩
  exact comparisonDefectsTrivialOfCoherentData W R D H

/-- Conversely v2.65 already constructs coherent data from a pointwise choice
whose five defects vanish.  Hence the existence problems are equivalent. -/
theorem hasCoherentGeneralWFactorizationData_iff_exists_fiveTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasCoherentGeneralWFactorizationData W R D ↔
      ∃ L : PointwiseGeneralWChoiceData (W := W) R D,
        FiveCoherenceDefectsTrivial W R D L := by
  constructor
  · exact exists_fiveTrivialDefects_of_hasCoherentGeneralWFactorizationData W R D
  · rintro ⟨L, hL⟩
    exact ⟨coherentGeneralWFactorizationDataOfFiveTrivialDefects W R D L hL⟩

/-! ## Gauge-trivializability and the canonical v2.61 choice -/

/-- A pointwise choice is gauge-trivializable when some gauge-related choice has
all five v2.65 defects trivial. -/
def FiveDefectGaugeTrivializable
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L₀ : PointwiseGeneralWChoiceData (W := W) R D) : Prop :=
  ∃ L : PointwiseGeneralWChoiceData (W := W) R D,
    PointwiseChoicesGaugeEquivalent W R D L₀ L ∧
      FiveCoherenceDefectsTrivial W R D L

/-- Since all local choices form one gauge orbit, gauge-trivializability is
independent of the chosen base point. -/
theorem fiveDefectGaugeTrivializable_iff_exists_fiveTrivialDefects
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L₀ : PointwiseGeneralWChoiceData (W := W) R D) :
    FiveDefectGaugeTrivializable W R D L₀ ↔
      ∃ L : PointwiseGeneralWChoiceData (W := W) R D,
        FiveCoherenceDefectsTrivial W R D L := by
  constructor
  · rintro ⟨L, hGauge, hL⟩
    exact ⟨L, hL⟩
  · rintro ⟨L, hL⟩
    exact ⟨L, pointwiseChoicesGaugeEquivalent_all W R D L₀ L, hL⟩

/-- Main obstruction theorem of v2.66: coherent general-`W` factorization data
exist exactly when any fixed pointwise choice is gauge-trivializable. -/
theorem hasCoherentGeneralWFactorizationData_iff_gaugeTrivializable
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L₀ : PointwiseGeneralWChoiceData (W := W) R D) :
    HasCoherentGeneralWFactorizationData W R D ↔
      FiveDefectGaugeTrivializable W R D L₀ := by
  rw [hasCoherentGeneralWFactorizationData_iff_exists_fiveTrivialDefects W R D]
  exact
    (fiveDefectGaugeTrivializable_iff_exists_fiveTrivialDefects W R D L₀).symm

/-- Canonical gauge-trivializability proposition based at the unconditional
v2.61 pointwise choice. -/
def CanonicalGeneralWGaugeTrivializable
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  FiveDefectGaugeTrivializable W R D (pointwiseGeneralWChoiceData W R D)

/-- The complete coherent-data existence problem is therefore exactly the
canonical gauge-trivialization problem. -/
theorem hasCoherentGeneralWFactorizationData_iff_canonicalGaugeTrivializable
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasCoherentGeneralWFactorizationData W R D ↔
      CanonicalGeneralWGaugeTrivializable W R D :=
  hasCoherentGeneralWFactorizationData_iff_gaugeTrivializable W R D
    (pointwiseGeneralWChoiceData W R D)

/-- A canonical gauge trivialization yields the genuine v2.10 higher-localization
factorization. -/
theorem hasHigherLocalizationFactorization_of_canonicalGaugeTrivializable
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : CanonicalGeneralWGaugeTrivializable W R D) :
    HasHigherLocalizationFactorization (W := W) R := by
  have hC : HasCoherentGeneralWFactorizationData W R D :=
    (hasCoherentGeneralWFactorizationData_iff_canonicalGaugeTrivializable
      W R D).2 h
  exact
    hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
      W R D hC

/-- Weak `W`-admissibility reduces unrestricted factorization to one explicit
canonical gauge-obstruction proposition.  No vanishing of that proposition is
asserted here. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_canonicalGaugeTrivializable
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (hGauge : CanonicalGeneralWGaugeTrivializable W R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_canonicalGaugeTrivializable
    W R (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) hGauge

/-!
## Boundary fixed by v2.66

The unrestricted route is now organized as

```text
IsHigherWAdmissible W R
        ↓ v2.56--v2.61
canonical pointwise local choice L₀
        ↓
all pointwise choices lie in one explicit automorphism gauge orbit
        ↓
five automorphism-valued defects                         [v2.65]
        ↓
CanonicalGeneralWGaugeTrivializable W R D
        ↔
HasCoherentGeneralWFactorizationData W R D
        ↓
HigherLocalizationFactorization W R.
```

Thus arbitrary `Classical.choice` has disappeared from the *statement* of the
remaining obstruction: changing the local choice only moves within one explicit
gauge orbit.  The genuine open problem is whether weak `W`-admissibility forces
that orbit to meet the zero-defect locus.

The next mathematical step is not another thinness hypothesis.  It is to study
the gauge transformation of the three transport defects and two comparison
defects in enough detail to decide whether their obstruction class is always
trivial for the localization relations generated by `id`, `comp`, `Winv₁`, and
`Winv₂`, or whether extra 2-dimensional localization data is genuinely needed.

No unrestricted factorization claim, strictification claim, new axiom, `sorry`,
`admit`, or choice-as-coherence principle is introduced.
-/

end KUOS.DependentOriginationGaugeObstructionV2_66
