import KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61

namespace KUOS.DependentOriginationFiberFunctorTwoThinV2_62

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61

universe u v uH vH

/-!
# Fiber-functor 2-thin coherence v2.62

Version 2.61 proves that, once the v2.56 pointwise adjoint-equivalence data is
available, the complete space of local isomorphism choices occurring in the
general-`W` factorization problem is inhabited.  What remains is exactly five
coherence equations: three quotient-pseudofunctor equations and two
StrongTrans equations.

This file isolates a clean sufficient condition under which those five equations
are automatic.  We say that the image fibers of `R` are *fiber-functor
2-thin* when any two parallel 2-morphisms between functors connecting two image
fibers are equal.  Equivalently, each relevant hom-category of `Cat` is thin on
those objects.

Under this hypothesis every two sides of every v2.59/v2.60 coherence equation
are parallel 2-morphisms in one of these thin hom-categories, so they agree by
2-thinness.  Therefore an arbitrary v2.61 pointwise choice upgrades to a full
coherent five-law package and hence to the genuine v2.10
`HigherLocalizationFactorization`.

The hypothesis is intentionally explicit and strong.  It is not asserted for an
arbitrary raw higher contextual system.  The point of the theorem is to identify
precisely that the remaining obstruction is 2-dimensional coherence rather than
existence of local inverses or local comparison isomorphisms.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Parallel 2-morphisms between any two functors connecting image fibers of
`R` are unique.

The objects `X` and `Y` range over the original context category, while `F` and
`G` range over 1-morphisms in `Cat`, i.e. functors between the corresponding
fiber categories. -/
def IsFiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ (X Y : Context)
    (F G : R.obj (.mk X) ⟶ R.obj (.mk Y))
    (η θ : F ⟶ G), η = θ

/-- Under fiber-functor 2-thinness, every pointwise v2.61 identity/composition
choice automatically satisfies the three v2.59 pseudofunctor coherence laws.

No special property of the chosen `mapId` or `mapComp` witnesses is needed:
the two sides of each law are merely parallel 2-cells in a thin hom-category. -/
noncomputable def coherentQuotientTransportDataOfFiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberFunctorTwoThin R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    CoherentQuotientTransportData (W := W) R D where
  mapId := L.mapId
  mapComp := L.mapComp
  map₂_associator := by
    intro X Y Z T f g h
    exact hthin X.as.obj T.as.obj _ _ _ _
  map₂_left_unitor := by
    intro X Y f
    exact hthin X.as.obj Y.as.obj _ _ _ _
  map₂_right_unitor := by
    intro X Y f
    exact hthin X.as.obj Y.as.obj _ _ _ _

/-- Under the same 2-thinness hypothesis, the raw-arrow comparison choices from
v2.61 automatically satisfy the two StrongTrans coherence laws of v2.60.

The comparison components remain the identity functors, exactly as in v2.60. -/
noncomputable def coherentPresentationComparisonDataOfFiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberFunctorTwoThin R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    CoherentPresentationComparisonData (W := W) R D
      (coherentQuotientTransportDataOfFiberFunctorTwoThin W R D hthin L) where
  mapIso := by
    intro X Y f
    change quotientRepresentativeMap W R D (W.Q.map f) ≅ R.map f.toLoc
    exact L.mapIso f
  naturality_id := by
    intro X
    exact hthin X X _ _ _ _
  naturality_comp := by
    intro X Y Z f g
    exact hthin X Z _ _ _ _

/-- Fiber-functor 2-thinness upgrades *any* pointwise local choice bundle to the
complete five-law coherent factorization datum of v2.60. -/
noncomputable def coherentGeneralWFactorizationDataOfFiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberFunctorTwoThin R)
    (L : PointwiseGeneralWChoiceData (W := W) R D) :
    CoherentGeneralWFactorizationData (W := W) R D where
  transport :=
    coherentQuotientTransportDataOfFiberFunctorTwoThin W R D hthin L
  comparison :=
    coherentPresentationComparisonDataOfFiberFunctorTwoThin W R D hthin L

/-- Consequently the complete five-law coherence package exists whenever the
image fiber-functor hom-categories are 2-thin. -/
theorem hasCoherentGeneralWFactorizationData_of_fiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberFunctorTwoThin R) :
    HasCoherentGeneralWFactorizationData W R D := by
  exact
    ⟨coherentGeneralWFactorizationDataOfFiberFunctorTwoThin W R D hthin
      (pointwiseGeneralWChoiceData W R D)⟩

/-- Main v2.62 theorem: pointwise adjoint-equivalence data plus 2-thinness is
sufficient for an actual general-`W` higher-localization factorization.

The local identity/composition/presentation isomorphisms are supplied
unconditionally by v2.61; 2-thinness supplies exactly the five missing equations. -/
theorem hasHigherLocalizationFactorization_of_fiberFunctorTwoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberFunctorTwoThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_hasCoherentGeneralWFactorizationData
    W R D
      (hasCoherentGeneralWFactorizationData_of_fiberFunctorTwoThin W R D hthin)

/-- Weak `W`-admissibility supplies the v2.56 pointwise adjoint-equivalence
data.  Thus, in the 2-thin image-fiber sector, weak admissibility alone closes
the whole general-`W` factorization route. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_fiberFunctorTwoThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (hthin : IsFiberFunctorTwoThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiberFunctorTwoThin W R
    (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) hthin

/-!
## Boundary fixed by v2.62

The formally proved implication in this layer is

```text
IsHigherWAdmissible W R
+ IsFiberFunctorTwoThin R
        ↓
pointwise local Iso choices                        [v2.56--v2.61]
        ↓
all 3 quotient-pseudofunctor equations are unique parallel 2-cells
all 2 StrongTrans equations are unique parallel 2-cells
        ↓
CoherentGeneralWFactorizationData
        ↓
HigherLocalizationFactorization W R.
```

This is a genuine sufficient theorem, not a restatement of the desired
factorization as input data.  It also sharpens the interpretation of the open
general case: once local choices exist, the obstruction disappears whenever the
relevant 2-cell spaces are propositions.

What remains open without `IsFiberFunctorTwoThin` is the unrestricted coherence
existence theorem

```text
IsHigherWAdmissible W R
  ⇒ HasCoherentGeneralWFactorizationData W R D
```

or an equivalent bicategorical localization/strictification theorem that
constructs those coherent transports.  No such unrestricted claim is made here.
-/

end KUOS.DependentOriginationFiberFunctorTwoThinV2_62
