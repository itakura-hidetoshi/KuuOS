import KUOS.DependentOriginationFiberHomThinV2_63

namespace KUOS.DependentOriginationFiberIsoThinV2_64

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationFiberFunctorTwoThinV2_62
open KUOS.DependentOriginationFiberHomThinV2_63

universe u v uH vH

/-!
# Fiber-core / invertible-2-cell coherence v2.64

Versions 2.62 and 2.63 close the general-`W` higher-localization factorization
whenever all relevant 2-cells are unique.  That hypothesis is stronger than the
five coherence equations actually need.

Every 2-cell appearing in the three quotient-pseudofunctor equations and the two
StrongTrans equations is invertible: the equations are built only from the homs
of `Iso`s, associators, unitors, whiskerings of invertible 2-cells, vertical
composition, and `eqToHom`.  Consequently it is enough that *invertible* parallel
2-cells be unique.  Arbitrary noninvertible natural transformations may remain
highly nontrivial.

This file formalizes that sharper sufficient sector in three equivalent-looking
layers of increasing intrinsicity:

* `IsFiberFunctorIsoThin R`: between any two functors connecting image fibers,
  there is at most one natural isomorphism;
* `IsFiberCoreThin R`: inside each image fiber, between any two objects there is
  at most one isomorphism;
* `IsFiberAutomorphismTrivial R`: every object in every image fiber has only the
  identity automorphism.

The last condition already implies the middle one: two isomorphisms `A ≅ B`
differ by an automorphism of `A`.  The middle condition implies the first
pointwise, by extensionality of natural transformations.

Under any of these conditions, weak `W`-admissibility yields the genuine v2.10
`HigherLocalizationFactorization`.  This strictly sharpens the interpretation of
the remaining unrestricted obstruction: noninvertible 2-cells are irrelevant to
these five laws; the possible obstruction lives in invertible 2-dimensional
isotropy.

No unrestricted factorization theorem is asserted in this file.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The relevant functor hom-categories are thin only on their maximal subgroupoids:
for fixed image fibers and fixed functors `F,G`, the type of 2-isomorphisms
`F ≅ G` is a subsingleton.

This is weaker than `IsFiberFunctorTwoThin`: noninvertible natural transformations
need not be unique. -/
def IsFiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ (X Y : Context)
    (F G : R.obj (.mk X) ⟶ R.obj (.mk Y)),
    Subsingleton (F ≅ G)

/-- Each image fiber has a thin core groupoid: between any two objects of one
fiber there is at most one isomorphism.  Noninvertible morphisms are unrestricted. -/
def IsFiberCoreThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ (X : Context) (A B : R.obj (.mk X)), Subsingleton (A ≅ B)

/-- Every object in every image fiber has trivial automorphism group.

Because an automorphism type is always inhabited by `Iso.refl`, subsingleton here
means exactly that every automorphism is the identity. -/
def IsFiberAutomorphismTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ (X : Context) (A : R.obj (.mk X)), Subsingleton (A ≅ A)

/-- Full v2.62 2-thinness implies invertible-2-cell thinness. -/
theorem isFiberFunctorIsoThin_of_fiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hthin : IsFiberFunctorTwoThin R) :
    IsFiberFunctorIsoThin R := by
  intro X Y F G
  refine ⟨?_⟩
  intro e₁ e₂
  apply Iso.ext
  exact hthin X Y F G e₁.hom e₂.hom

/-- Thin fibers from v2.63 have trivial automorphism groups. -/
theorem isFiberAutomorphismTrivial_of_fiberHomThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hthin : IsFiberHomThin R) :
    IsFiberAutomorphismTrivial R := by
  intro X A
  letI : Quiver.IsThin (R.obj (.mk X)) := hthin X
  infer_instance

/-- Trivial automorphism groups force the whole core groupoid of each fiber to be
thin: any two isomorphisms `A ≅ B` differ by an automorphism of `A`. -/
theorem isFiberCoreThin_of_automorphismTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (htriv : IsFiberAutomorphismTrivial R) :
    IsFiberCoreThin R := by
  intro X A B
  refine ⟨?_⟩
  intro e₁ e₂
  apply Iso.ext
  letI : Subsingleton (A ≅ A) := htriv X A
  have hloop : e₁ ≪≫ e₂.symm = Iso.refl A :=
    Subsingleton.elim _ _
  have hhom : e₁.hom ≫ e₂.inv = 𝟙 A := by
    simpa using congrArg Iso.hom hloop
  calc
    e₁.hom = e₁.hom ≫ 𝟙 B := by simp
    _ = e₁.hom ≫ (e₂.inv ≫ e₂.hom) := by rw [e₂.inv_hom_id]
    _ = (e₁.hom ≫ e₂.inv) ≫ e₂.hom := by simp
    _ = (𝟙 A) ≫ e₂.hom := by rw [hhom]
    _ = e₂.hom := by simp

/-- Fiber-core thinness is enough to make natural isomorphisms between any two
functors into a given image fiber unique.

The proof descends a Cat 2-isomorphism to its natural transformation, then to each
component.  Each component is an isomorphism in the target fiber, hence unique by
`IsFiberCoreThin`. -/
theorem isFiberFunctorIsoThin_of_fiberCoreThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hcore : IsFiberCoreThin R) :
    IsFiberFunctorIsoThin R := by
  intro X Y F G
  refine ⟨?_⟩
  intro e₁ e₂
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext A
  letI : Subsingleton
      (F.toFunctor.obj A ≅ G.toFunctor.obj A) :=
    hcore Y (F.toFunctor.obj A) (G.toFunctor.obj A)
  exact congrArg Iso.hom
    (Subsingleton.elim
      (asIso (e₁.hom.toNatTrans.app A))
      (asIso (e₂.hom.toNatTrans.app A)))

/-- A convenient consequence: v2.63 fiber-hom thinness implies the weaker
fiber-core thinness through trivial automorphism groups. -/
theorem isFiberCoreThin_of_fiberHomThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hthin : IsFiberHomThin R) :
    IsFiberCoreThin R :=
  isFiberCoreThin_of_automorphismTrivial R
    (isFiberAutomorphismTrivial_of_fiberHomThin R hthin)

/-- In an invertible-2-cell-thin functor hom-category, any two parallel invertible
2-cells agree.

This is the exact equality principle needed for all five v2.59/v2.60 coherence
laws. -/
theorem eq_of_isIso_of_fiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hiso : IsFiberFunctorIsoThin R)
    (X Y : Context)
    {F G : R.obj (.mk X) ⟶ R.obj (.mk Y)}
    (η θ : F ⟶ G) [IsIso η] [IsIso θ] :
    η = θ := by
  letI : Subsingleton (F ≅ G) := hiso X Y F G
  exact congrArg Iso.hom (Subsingleton.elim (asIso η) (asIso θ))

/-- Invertible-2-cell thinness upgrades any v2.61 pointwise identity/composition
choices to the three coherent quotient-pseudofunctor laws of v2.59.

Unlike v2.62, no equality of arbitrary noninvertible 2-cells is assumed. -/
noncomputable def coherentQuotientTransportDataOfFiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    CoherentQuotientTransportData (W := W) R D where
  mapId := L.mapId
  mapComp := L.mapComp
  map₂_associator := by
    intro X Y Z T f g h
    apply eq_of_isIso_of_fiberFunctorIsoThin R hiso X.as.obj T.as.obj
  map₂_left_unitor := by
    intro X Y f
    apply eq_of_isIso_of_fiberFunctorIsoThin R hiso X.as.obj Y.as.obj
  map₂_right_unitor := by
    intro X Y f
    apply eq_of_isIso_of_fiberFunctorIsoThin R hiso X.as.obj Y.as.obj

/-- The same invertible-2-cell uniqueness automatically closes the two
StrongTrans coherence equations from v2.60. -/
noncomputable def coherentPresentationComparisonDataOfFiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    CoherentPresentationComparisonData (W := W) R D
      (coherentQuotientTransportDataOfFiberFunctorIsoThin W R D hiso L) where
  mapIso := by
    intro X Y f
    change quotientRepresentativeMap W R D (W.Q.map f) ≅ R.map f.toLoc
    exact L.mapIso f
  naturality_id := by
    intro X
    apply eq_of_isIso_of_fiberFunctorIsoThin R hiso X X
  naturality_comp := by
    intro X Y Z f g
    apply eq_of_isIso_of_fiberFunctorIsoThin R hiso X Z

/-- Assemble all five laws from invertible-2-cell uniqueness. -/
noncomputable def coherentGeneralWFactorizationDataOfFiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    CoherentGeneralWFactorizationData (W := W) R D where
  transport :=
    coherentQuotientTransportDataOfFiberFunctorIsoThin W R D hiso L
  comparison :=
    coherentPresentationComparisonDataOfFiberFunctorIsoThin W R D hiso L

/-- Hence invertible-2-cell thinness alone guarantees existence of the complete
coherent general-`W` factorization package. -/
theorem hasCoherentGeneralWFactorizationData_of_fiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R) :
    HasCoherentGeneralWFactorizationData W R D := by
  exact
    ⟨coherentGeneralWFactorizationDataOfFiberFunctorIsoThin W R D hiso
      (pointwiseGeneralWChoiceData W R D)⟩

/-- Main functor-iso-thin theorem: pointwise adjoint equivalences plus uniqueness
of invertible parallel 2-cells yield a genuine higher-localization factorization. -/
theorem hasHigherLocalizationFactorization_of_fiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
    W R D
      (hasCoherentGeneralWFactorizationData_of_fiberFunctorIsoThin W R D hiso)

/-- Weak `W`-admissibility plus fiber-functor iso-thinness closes the complete
general-`W` factorization route. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_fiberFunctorIsoThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (hiso : IsFiberFunctorIsoThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiberFunctorIsoThin W R
    (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) hiso

/-- More intrinsic main theorem: weak admissibility plus thin core groupoids of
the image fibers suffice.  Fibers may still have arbitrarily many noninvertible
morphisms. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_fiberCoreThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (hcore : IsFiberCoreThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_admissible_and_fiberFunctorIsoThin
    W hR (isFiberFunctorIsoThin_of_fiberCoreThin R hcore)

/-- Sharp intrinsic sufficient theorem of this layer: it is enough that every
fiber object have trivial automorphism group.  No uniqueness assumption on
noninvertible morphisms is needed. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_trivialFiberAutomorphisms
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (htriv : IsFiberAutomorphismTrivial R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_admissible_and_fiberCoreThin
    W hR (isFiberCoreThin_of_automorphismTrivial R htriv)

/-!
## Boundary fixed by v2.64

The sufficient hierarchy is now

```text
IsFiberHomThin R                         [v2.63]
        ↓
IsFiberAutomorphismTrivial R
        ↓
IsFiberCoreThin R
        ↓
IsFiberFunctorIsoThin R
        ↓
all five coherence equations compare invertible parallel 2-cells
        ↓
CoherentGeneralWFactorizationData
        ↓
HigherLocalizationFactorization W R.
```

Thus v2.62's full 2-thinness is substantially stronger than necessary.  The five
actual coherence equations only see the core groupoids of the relevant Cat
hom-categories.  Noninvertible natural transformations do not contribute to this
obstruction.

The unrestricted problem is therefore sharpened again.  If the theorem fails to
follow by a canonical coherence construction in complete generality, the residual
ambiguity must come from nontrivial invertible 2-dimensional isotropy (equivalently,
choices differing by natural automorphisms), not from arbitrary 2-cells.

This file still does **not** claim

```text
IsHigherWAdmissible W R
  ⇒ HasHigherLocalizationFactorization W R
```

without an additional coherence/iso-thinness hypothesis.  No new axiom, `sorry`,
`admit`, placeholder, or choice-as-coherence principle is introduced.
-/

end KUOS.DependentOriginationFiberIsoThinV2_64
