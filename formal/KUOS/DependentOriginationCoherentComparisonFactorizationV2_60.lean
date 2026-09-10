import KUOS.DependentOriginationCoherentQuotientTransportV2_59

namespace KUOS.DependentOriginationCoherentComparisonFactorizationV2_60

open CategoryTheory
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58
open KUOS.DependentOriginationCoherentQuotientTransportV2_59

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Coherent presentation comparison and factorization v2.60

Version 2.59 isolates the three pseudofunctor coherence equations needed to
turn the quotient-representative assignment into a genuine pseudofunctor on
`W.Localization`, and therefore into the exact localized higher-system carrier
used by v2.10.

The remaining v2.10 obligation is the comparison

```text
restrict(coherentQuotientLocalizedHigherSystem W R D T) ⟶ R.
```

The object fibers on the two sides are definitionally the same.  Thus the
comparison components can be fixed to identity functors.  For every base arrow
`f`, v2.58 already implies existence of an invertible 2-cell between the map of
the restricted quotient representative and `R.map f`: the representative
`Quot.out (W.Q.map f)` and the ordinary generator `ψ₁ W f` have equal images in
the localization quotient.

Consequently the only genuinely additional comparison coherence is a
simultaneous choice of those arrow isomorphisms satisfying the two nontrivial
StrongTrans laws for identities and composition.  This file packages exactly
those two equations and proves that, together with v2.59 coherent quotient
transport, they construct an actual `HigherLocalizationFactorization` in the
original v2.10 interface.

No existence of the five coherence laws (three from v2.59 and two here) is
asserted from weak `W`-admissibility alone.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Restriction of the v2.59 localized pseudofunctor back to the original
context category.  This abbreviation is used to keep the comparison formulas
readable. -/
noncomputable abbrev restrictedCoherentQuotientSystem
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) :
    RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH) :=
  restrictHigherLocalizedSystem W
    (coherentQuotientLocalizedHigherSystem W R D T)

/-- The restricted v2.59 system has exactly the original fiber category on every
raw context object. -/
@[simp] theorem restrictedCoherentQuotientSystem_obj
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (X : Context) :
    (restrictedCoherentQuotientSystem W R D T).obj (.mk X) =
      R.obj (.mk X) := by
  rfl

/-- On a raw arrow `f`, restriction of the v2.59 quotient pseudofunctor is
exactly evaluation of the chosen representative of `W.Q.map f`. -/
@[simp] theorem restrictedCoherentQuotientSystem_map
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    {X Y : Context} (f : X ⟶ Y) :
    (restrictedCoherentQuotientSystem W R D T).map f.toLoc =
      quotientRepresentativeMap W R D (W.Q.map f) := by
  rfl

/-- Pointwise existence of the comparison 2-isomorphism is already forced by
v2.58 and therefore introduces no new mathematical assumption.

The chosen representative of `W.Q.map f` and the ordinary generator `ψ₁ W f`
map to the same localized arrow.  Their free-path evaluations are thus
naturally isomorphic, while evaluation of `ψ₁ W f` is definitionally `R.map f`
by v2.57. -/
theorem presentationArrow_hasMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    {X Y : Context} (f : X ⟶ Y) :
    Nonempty
      ((restrictedCoherentQuotientSystem W R D T).map f.toLoc ≅
        R.map f.toLoc) := by
  change Nonempty
    ((freePathEvaluator W R D).map (Quot.out (W.Q.map f)) ≅
      R.map f.toLoc)
  rw [← freePathEvaluator_map_ordinary W R D f]
  apply equalInLocalization_hasEvaluationIso W R D
  change Quot.mk _ (Quot.out (W.Q.map f)) = W.Q.map f
  exact Quot.out_eq _

/-- Turn an isomorphism between the two arrow maps into the StrongTrans
naturality isomorphism when both object components are fixed to identities. -/
noncomputable def identityComponentNaturalityIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    {X Y : Context} (f : X ⟶ Y)
    (e :
      (restrictedCoherentQuotientSystem W R D T).map f.toLoc ≅
        R.map f.toLoc) :
    (restrictedCoherentQuotientSystem W R D T).map f.toLoc ≫
          𝟙 (R.obj (.mk Y)) ≅
      𝟙 (R.obj (.mk X)) ≫ R.map f.toLoc :=
  (ρ_ ((restrictedCoherentQuotientSystem W R D T).map f.toLoc)) ≪≫
    e ≪≫
    (λ_ (R.map f.toLoc)).symm

/-- The exact comparison-coherence package still missing after v2.59.

For each base arrow we choose one of the pointwise isomorphisms whose existence
was proved above.  The only additional laws are exactly StrongTrans
compatibility with identities and composition.  Naturality with respect to
2-cells requires no independent field because the source is locally discrete. -/
structure CoherentPresentationComparisonData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) where
  /-- Chosen comparison isomorphism for each raw context arrow. -/
  mapIso :
    ∀ {X Y : Context} (f : X ⟶ Y),
      (restrictedCoherentQuotientSystem W R D T).map f.toLoc ≅
        R.map f.toLoc
  /-- Identity coherence for the identity-component strong comparison. -/
  naturality_id :
    ∀ X : Context,
      (identityComponentNaturalityIso W R D T
          (𝟙 X) (mapIso (𝟙 X))).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapId (.mk X)).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapId (.mk X)).hom ▷
            (𝟙 (R.obj (.mk X))) ≫
          (λ_ (𝟙 (R.obj (.mk X)))).hom ≫
          (ρ_ (𝟙 (R.obj (.mk X)))).inv
  /-- Composition coherence for the identity-component strong comparison. -/
  naturality_comp :
    ∀ {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z),
      (identityComponentNaturalityIso W R D T
          (f ≫ g) (mapIso (f ≫ g))).hom ≫
          (𝟙 (R.obj (.mk X))) ◁ (R.mapComp f.toLoc g.toLoc).hom =
        ((restrictedCoherentQuotientSystem W R D T).mapComp
            f.toLoc g.toLoc).hom ▷ (𝟙 (R.obj (.mk Z))) ≫
          (α_ _ _ _).hom ≫
          (restrictedCoherentQuotientSystem W R D T).map f.toLoc ◁
            (identityComponentNaturalityIso W R D T
              g (mapIso g)).hom ≫
          (α_ _ _ _).inv ≫
          (identityComponentNaturalityIso W R D T
            f (mapIso f)).hom ▷ R.map g.toLoc ≫
          (α_ _ _ _).hom

/-- Existence of coherent comparison data remains an explicit proposition. -/
def HasCoherentPresentationComparisonData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) : Prop :=
  Nonempty (CoherentPresentationComparisonData (W := W) R D T)

/-- The v2.60 comparison data constructs the actual strong transformation from
restriction of the localized system to the original raw pseudofunctor. -/
noncomputable def coherentPresentationComparison
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (C : CoherentPresentationComparisonData (W := W) R D T) :
    restrictedCoherentQuotientSystem W R D T ⟶ R := by
  refine
    { app := fun X => 𝟙 (R.obj X)
      naturality := ?_
      naturality_id := ?_
      naturality_comp := ?_ }
  · intro X Y f
    rcases X with ⟨X⟩
    rcases Y with ⟨Y⟩
    simpa using
      identityComponentNaturalityIso W R D T f.as (C.mapIso f.as)
  · intro X
    rcases X with ⟨X⟩
    simpa using C.naturality_id X
  · intro X Y Z f g
    rcases X with ⟨X⟩
    rcases Y with ⟨Y⟩
    rcases Z with ⟨Z⟩
    simpa using C.naturality_comp f.as g.as

/-- The comparison components are exactly identity functors. -/
@[simp] theorem coherentPresentationComparison_app
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (C : CoherentPresentationComparisonData (W := W) R D T)
    (X : Context) :
    (coherentPresentationComparison W R D T C).app (.mk X) =
      𝟙 (R.obj (.mk X)) := by
  rfl

/-- Coherent quotient transport plus coherent presentation comparison constructs
an actual v2.10 higher-localization factorization. -/
noncomputable def coherentQuotientHigherLocalizationFactorization
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (C : CoherentPresentationComparisonData (W := W) R D T) :
    HigherLocalizationFactorization (W := W) R where
  lift := coherentQuotientLocalizedHigherSystem W R D T
  comparison := coherentPresentationComparison W R D T C
  comparison_isEquivalence := by
    intro X
    change (𝟭 (R.obj (.mk X))).IsEquivalence
    infer_instance

/-- Direct existence theorem in the original v2.10 interface. -/
theorem hasHigherLocalizationFactorization_of_coherentTransportComparison
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (C : CoherentPresentationComparisonData (W := W) R D T) :
    HasHigherLocalizationFactorization (W := W) R :=
  ⟨coherentQuotientHigherLocalizationFactorization W R D T C⟩

/-- Package the complete five-law general-W coherence frontier: three quotient
pseudofunctor laws from v2.59 and two comparison laws from v2.60. -/
structure CoherentGeneralWFactorizationData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) where
  /-- Coherent descent of representative maps to the quotient pseudofunctor. -/
  transport : CoherentQuotientTransportData (W := W) R D
  /-- Coherent identity-component comparison back to the original raw system. -/
  comparison :
    CoherentPresentationComparisonData (W := W) R D transport

/-- Existence of the complete five-law coherence package. -/
def HasCoherentGeneralWFactorizationData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  Nonempty (CoherentGeneralWFactorizationData (W := W) R D)

/-- The five-law package is sufficient for the genuine v2.10 factorization. -/
theorem hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : HasCoherentGeneralWFactorizationData W R D) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases h with ⟨H⟩
  exact
    hasHigherLocalizationFactorization_of_coherentTransportComparison W R D
      H.transport H.comparison

/-- Specialization to the canonical pointwise adjoint-equivalence data produced
by weak `W`-admissibility.

This theorem does not assert existence of the five-law data; it states the
precise remaining sufficient hypothesis after the unconditional v2.56--v2.58
construction. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_coherentData
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (h : HasCoherentGeneralWFactorizationData W R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
    W R (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) h

/-!
## Boundary fixed by v2.60

The general-`W` existence problem is now decomposed into an unconditional part
and an exact finite coherence frontier:

```text
IsHigherWAdmissible W R
  → pointwise adjoint equivalences                         [v2.56]
  → free-path evaluation                                  [v2.57]
  → pointwise quotient-relation comparison Iso existence [v2.58]

plus

  3 quotient-pseudofunctor coherence laws                [v2.59 datum]
  2 strong-comparison coherence laws                     [v2.60 datum]
  --------------------------------------------------------------------
  → HigherLocalizationFactorization W R                  [proved here].
```

Thus neither construction of the localized pseudofunctor from coherent
transport nor construction of the final v2.10 factorization from the five-law
package remains open.

What is still open is the genuinely mathematical existence theorem saying that
the pointwise relation isomorphisms furnished by weak admissibility admit a
simultaneous choice satisfying all five equations.  This file does not assume
that arbitrary `Classical.choice` witnesses are coherent and does not claim

```text
IsHigherWAdmissible W R
  ⇒ HasHigherLocalizationFactorization W R
```

without the explicitly displayed coherence package.
-/

end KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
