import KUOS.DependentOriginationCoherentComparisonFactorizationV2_60

namespace KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60

universe u v uH vH

/-!
# Pointwise general-W local choices v2.61

The v2.60 layer proves that five coherence laws are sufficient to build the
actual v2.10 `HigherLocalizationFactorization`: three laws for quotient
pseudofunctoriality and two laws for the strong comparison back to the raw
system.

This file removes one possible ambiguity from that frontier.  The unresolved
issue is not existence of the individual comparison isomorphisms occurring in
those laws.  Given the v2.56 pointwise adjoint-equivalence data, v2.58 already
forces all of the following pointwise isomorphism types to be inhabited:

* the quotient representative of an identity versus the identity functor;
* the quotient representative of a composite versus the composite of the two
  representative evaluations;
* the quotient representative of a raw presentation arrow versus `R.map f`.

We prove those three existence statements explicitly and use classical choice to
bundle one simultaneous pointwise selection.  No coherence of that arbitrary
selection is claimed.

Finally, we project every v2.60 coherent five-law package to its underlying
pointwise selection and define the fiber predicate saying that a pointwise
selection admits a coherent extension.  Thus the remaining obstruction is
formalized as existence of a coherently extendable point in an already inhabited
space of local choices, rather than as missing local data.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The quotient representative of an identity has evaluation naturally
isomorphic to the identity functor.

This is a direct v2.58 application: `Quot.out (𝟙 X)` and the identity path have
the same image under the quotient functor. -/
theorem quotientIdentity_hasMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (X : W.Localization) :
    Nonempty
      (quotientRepresentativeMap W R D (𝟙 X) ≅
        𝟙 (R.obj (.mk X.as.obj))) := by
  change Nonempty
    ((freePathEvaluator W R D).map (Quot.out (𝟙 X)) ≅
      𝟙 (R.obj (.mk X.as.obj)))
  have hq :
      (Quotient.functor (Localization.Construction.relations W)).map
          (Quot.out (𝟙 X)) =
        (Quotient.functor (Localization.Construction.relations W)).map
          (𝟙 X.as) := by
    calc
      (Quotient.functor (Localization.Construction.relations W)).map
          (Quot.out (𝟙 X)) = 𝟙 X := by
            change Quot.mk _ (Quot.out (𝟙 X)) = 𝟙 X
            exact Quot.out_eq _
      _ =
          (Quotient.functor (Localization.Construction.relations W)).map
            (𝟙 X.as) := by
            simpa using
              ((Quotient.functor
                (Localization.Construction.relations W)).map_id X.as).symm
  rcases equalInLocalization_hasEvaluationIso W R D hq with ⟨e⟩
  exact ⟨by simpa only [Functor.map_id] using e⟩

/-- The quotient representative of a composite has evaluation naturally
isomorphic to the composite of the two representative evaluations.

Again no new coherence hypothesis is used: `Quot.out (f ≫ g)` and
`Quot.out f ≫ Quot.out g` represent the same localized arrow. -/
theorem quotientComposition_hasMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    Nonempty
      (quotientRepresentativeMap W R D (f ≫ g) ≅
        quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g) := by
  change Nonempty
    ((freePathEvaluator W R D).map (Quot.out (f ≫ g)) ≅
      (freePathEvaluator W R D).map (Quot.out f) ≫
        (freePathEvaluator W R D).map (Quot.out g))
  have hq :
      (Quotient.functor (Localization.Construction.relations W)).map
          (Quot.out (f ≫ g)) =
        (Quotient.functor (Localization.Construction.relations W)).map
          (Quot.out f ≫ Quot.out g) := by
    calc
      (Quotient.functor (Localization.Construction.relations W)).map
          (Quot.out (f ≫ g)) = f ≫ g := by
            change Quot.mk _ (Quot.out (f ≫ g)) = f ≫ g
            exact Quot.out_eq _
      _ =
          (Quotient.functor (Localization.Construction.relations W)).map
              (Quot.out f) ≫
            (Quotient.functor (Localization.Construction.relations W)).map
              (Quot.out g) := by
            change
              f ≫ g =
                Quot.mk _ (Quot.out f) ≫ Quot.mk _ (Quot.out g)
            rw [Quot.out_eq, Quot.out_eq]
      _ =
          (Quotient.functor (Localization.Construction.relations W)).map
            (Quot.out f ≫ Quot.out g) := by
            exact
              ((Quotient.functor
                (Localization.Construction.relations W)).map_comp
                  (Quot.out f) (Quot.out g)).symm
  rcases equalInLocalization_hasEvaluationIso W R D hq with ⟨e⟩
  exact ⟨by simpa only [Functor.map_comp] using e⟩

/-- The representative of the localized image of every raw arrow has evaluation
naturally isomorphic to the original pseudofunctor map.

This is the v2.60 pointwise comparison theorem with the dependence on coherent
transport removed from its statement: the proof only uses v2.58 quotient
relation existence. -/
theorem presentationRepresentative_hasMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) :
    Nonempty
      (quotientRepresentativeMap W R D (W.Q.map f) ≅
        R.map f.toLoc) := by
  change Nonempty
    ((freePathEvaluator W R D).map (Quot.out (W.Q.map f)) ≅
      R.map f.toLoc)
  rw [← freePathEvaluator_map_ordinary W R D f]
  apply equalInLocalization_hasEvaluationIso W R D
  change Quot.mk _ (Quot.out (W.Q.map f)) = W.Q.map f
  exact Quot.out_eq _

/-- A simultaneous pointwise selection of all local isomorphisms that occur in
the five-law v2.60 coherence frontier.

There are deliberately no equations in this structure.  It records only local
choices. -/
structure PointwiseGeneralWChoiceData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) where
  /-- Identity comparison choice on the localization quotient. -/
  mapId :
    ∀ X : W.Localization,
      quotientRepresentativeMap W R D (𝟙 X) ≅
        𝟙 (R.obj (.mk X.as.obj))
  /-- Composition comparison choice on the localization quotient. -/
  mapComp :
    ∀ {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      quotientRepresentativeMap W R D (f ≫ g) ≅
        quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g
  /-- Raw-arrow comparison choice back to the original pseudofunctor. -/
  mapIso :
    ∀ {X Y : Context} (f : X ⟶ Y),
      quotientRepresentativeMap W R D (W.Q.map f) ≅
        R.map f.toLoc

/-- The space of pointwise choices is always inhabited once the v2.56
pointwise adjoint-equivalence data is available.

`Classical.choice` is used only to pick witnesses from the v2.58 `Nonempty`
statements.  No coherence property of the selected witnesses is inferred. -/
noncomputable def pointwiseGeneralWChoiceData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    PointwiseGeneralWChoiceData (W := W) R D where
  mapId X := Classical.choice (quotientIdentity_hasMapIso W R D X)
  mapComp f g := Classical.choice (quotientComposition_hasMapIso W R D f g)
  mapIso f := Classical.choice (presentationRepresentative_hasMapIso W R D f)

/-- Existence form of the pointwise-choice theorem. -/
theorem nonempty_pointwiseGeneralWChoiceData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    Nonempty (PointwiseGeneralWChoiceData (W := W) R D) :=
  ⟨pointwiseGeneralWChoiceData W R D⟩

/-- Weak `W`-admissibility therefore already supplies a simultaneous pointwise
selection of every local isomorphism appearing in the five-law frontier. -/
noncomputable def pointwiseGeneralWChoiceDataOfAdmissible
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R) :
    PointwiseGeneralWChoiceData (W := W) R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) :=
  pointwiseGeneralWChoiceData W R
    (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)

/-- Forget all five coherence equations from a v2.60 coherent factorization
package, retaining only its underlying pointwise local choices. -/
noncomputable def pointwiseChoiceDataOfCoherentGeneralWFactorizationData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : CoherentGeneralWFactorizationData (W := W) R D) :
    PointwiseGeneralWChoiceData (W := W) R D where
  mapId := H.transport.mapId
  mapComp := H.transport.mapComp
  mapIso := by
    intro X Y f
    simpa using H.comparison.mapIso f

/-- A pointwise local selection admits a coherent extension when it is exactly
the underlying local selection of some complete v2.60 five-law package. -/
noncomputable def HasCoherentExtension
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) : Prop :=
  ∃ H : CoherentGeneralWFactorizationData (W := W) R D,
    pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H = L

/-- The complete v2.60 coherence package is equivalent to existence of a
pointwise local selection admitting a coherent extension.

The right-hand side separates the already-solved local-choice existence problem
from the genuinely higher extension problem. -/
theorem hasCoherentGeneralWFactorizationData_iff_exists_coherentlyExtendablePointwiseData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    HasCoherentGeneralWFactorizationData W R D ↔
      ∃ L : PointwiseGeneralWChoiceData (W := W) R D,
        HasCoherentExtension W R D L := by
  constructor
  · rintro ⟨H⟩
    refine
      ⟨pointwiseChoiceDataOfCoherentGeneralWFactorizationData W R D H, ?_⟩
    exact ⟨H, rfl⟩
  · rintro ⟨L, H, hHL⟩
    exact ⟨H⟩

/-- Any coherently extendable pointwise selection therefore yields the genuine
v2.10 higher-localization factorization. -/
theorem hasHigherLocalizationFactorization_of_coherentlyExtendablePointwiseData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (L : PointwiseGeneralWChoiceData (W := W) R D)
    (hL : HasCoherentExtension W R D L) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases hL with ⟨H, hHL⟩
  exact
    hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
      W R D ⟨H⟩

/-!
## Boundary fixed by v2.61

The unconditional general-`W` chain now reaches a simultaneous pointwise choice:

```text
IsHigherWAdmissible W R
  → pointwise adjoint equivalences                         [v2.56]
  → free-path evaluation                                  [v2.57]
  → local quotient-relation Iso existence                [v2.58]
  → simultaneous choices of mapId / mapComp / mapIso     [v2.61]
```

Hence the remaining issue is not the existence of any local inverse or local
comparison.  Formally, the local-choice space is inhabited.  The missing theorem
is that at least one point in that space admits a coherent extension satisfying
exactly the three v2.59 pseudofunctor equations and two v2.60 StrongTrans
equations.

Equivalently, what remains open is the implication

```text
IsHigherWAdmissible W R
  ⇒ ∃ L : PointwiseGeneralWChoiceData,
       HasCoherentExtension W R D L.
```

Once such an extension is provided, v2.60 and the theorem above produce
`HigherLocalizationFactorization W R` without any further construction.

No arbitrary `Classical.choice` witness is claimed to be coherent.  No
strictification, stackification, new axiom, `sorry`, or `admit` is introduced.
-/

end KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
