import KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
import Mathlib.AlgebraicTopology.SimplicialSet.PushoutProduct
import Mathlib.CategoryTheory.LiftingProperties.ParametrizedAdjunction

namespace KUOS.DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open MonoidalCategory
open Simplicial
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50

universe u

/-!
# Standard type-(A) native Leibniz lifting mate v1.51

Version 1.50 identified the restricted induced attachment family with the
endpoint pushout-product geometry built from `Subcomplex.unionProd`.  This file
connects that geometry to the native Leibniz machinery already present in the
pinned Mathlib revision.

For a type-(A) horn inclusion `i` and an endpoint inclusion `e`, the v1.40
union-product square is packaged as a `Functor.PushoutObjObj` for the curried
tensor bifunctor.  Its native Leibniz inclusion is proved to be exactly the
underlying map of the v1.50 scaled endpoint pushout-product.

The closed structure on simplicial sets then gives the native lifting mate

```text
(i square e) has LLP against p
  iff
 e has LLP against the Leibniz pullback-hom of i and p.
```

This is a theorem of the pinned Mathlib `ParametrizedAdjunction` interface.
No model-structure closure statement is inserted here.  The result exposes the
precise pullback-hom condition that can be used to prove the stability input
isolated in v1.50.
-/

/-! ## The v1.40 union product as a native Leibniz pushout -/

/-- The endpoint union-product square, packaged in Mathlib's native
`PushoutObjObj` interface for the tensor bifunctor. -/
noncomputable def standardTypeAEndpointLeibnizSquare
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (curriedTensor (SSet.{u})).PushoutObjObj
      (SSet.horn g.n g.i).ι
      (intervalEndpoint g.endpoint).ι :=
  SSet.Subcomplex.unionProd.pushoutObjObj
    (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)

/-- The native Leibniz inclusion of the packaged square is exactly the
ordinary inclusion of the endpoint union-product subcomplex. -/
theorem standardTypeAEndpointLeibnizSquare_ι
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointLeibnizSquare g).ι =
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint)).ι := by
  change
    (SSet.Subcomplex.unionProd.pushoutObjObj
      (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).ι = _
  exact SSet.Subcomplex.unionProd.pushoutObjObj_ι
    (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)

/-- Hence the native Leibniz inclusion is the underlying map of the v1.50
scaled endpoint pushout-product. -/
theorem standardTypeAEndpointLeibnizSquare_ι_eq_endpointPushoutProductMap
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointLeibnizSquare g).ι =
      (standardTypeAEndpointPushoutProductHom g).map := by
  exact standardTypeAEndpointLeibnizSquare_ι g

/-! ## The native pullback-hom mate -/

/-- The Leibniz pullback-hom square associated to a type-(A) horn inclusion
and an arbitrary simplicial-set map `p`. -/
noncomputable def standardTypeAHornPullbackHomSquare
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {X Y : SSet.{u}}
    (p : X ⟶ Y) :
    (MonoidalClosed.internalHom (C := SSet.{u})).PullbackObjObj
      (SSet.horn g.n g.i).ι p :=
  Functor.PullbackObjObj.ofHasPullback
    (MonoidalClosed.internalHom (C := SSet.{u}))
    (SSet.horn g.n g.i).ι p

/-- Native lifting-mate equivalence for the exact underlying map of the v1.50
standard type-(A) endpoint pushout-product. -/
theorem standardTypeAEndpointPushoutProduct_hasLiftingProperty_iff
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {X Y : SSet.{u}}
    (p : X ⟶ Y) :
    HasLiftingProperty
        (standardTypeAEndpointPushoutProductHom g).map p ↔
      HasLiftingProperty
        (intervalEndpoint g.endpoint).ι
        (standardTypeAHornPullbackHomSquare g p).π := by
  rw [← standardTypeAEndpointLeibnizSquare_ι_eq_endpointPushoutProductMap g]
  exact
    ParametrizedAdjunction.hasLiftingProperty_iff
      (MonoidalClosed.internalHomAdjunction₂ (C := SSet.{u}))
      (standardTypeAEndpointLeibnizSquare g)
      (standardTypeAHornPullbackHomSquare g p)

/-- The pullback-hom lifting condition implies lifting against the endpoint
pushout-product. -/
theorem standardTypeAEndpointPushoutProduct_lifting_of_pullbackHom
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {X Y : SSet.{u}}
    (p : X ⟶ Y)
    (h : HasLiftingProperty
      (intervalEndpoint g.endpoint).ι
      (standardTypeAHornPullbackHomSquare g p).π) :
    HasLiftingProperty
      (standardTypeAEndpointPushoutProductHom g).map p :=
  (standardTypeAEndpointPushoutProduct_hasLiftingProperty_iff g p).2 h

/-- Conversely, lifting against the endpoint pushout-product gives the exact
native pullback-hom lifting condition. -/
theorem standardTypeAHornPullbackHom_lifting_of_endpointPushoutProduct
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {X Y : SSet.{u}}
    (p : X ⟶ Y)
    (h : HasLiftingProperty
      (standardTypeAEndpointPushoutProductHom g).map p) :
    HasLiftingProperty
      (intervalEndpoint g.endpoint).ι
      (standardTypeAHornPullbackHomSquare g p).π :=
  (standardTypeAEndpointPushoutProduct_hasLiftingProperty_iff g p).1 h

/-!
The type-(A) attachment frontier is therefore now expressed by native Mathlib
Leibniz data:

```text
v1.40 unionProd pushout
  -> Functor.PushoutObjObj for curriedTensor
  -> native Leibniz inclusion
  = underlying v1.50 endpoint pushout-product map
  -> ParametrizedAdjunction.hasLiftingProperty_iff
  -> endpoint LLP against the horn pullback-hom.
```

The next mathematical step is to transport this underlying mate through the
scaled lifting interfaces and prove the required right-class pullback-hom
stability for the chosen external scaled-anodyne presentation.  That step can
now refer to a concrete native pullback object rather than an abstract
pushout-product stability predicate.
-/

end KUOS.DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51
