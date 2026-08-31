import KUOS.DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54

namespace KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51
open KUOS.DependentOriginationScaledCartesianIntervalCylinderV1_52
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54

universe u

noncomputable section

/-!
# Standard type-(A) scaled Leibniz pushout v1.55

Versions v1.50-v1.54 separated three pieces which must now be recombined
categorically:

1. the ordinary `SSet` Leibniz square is the native `unionProd` pushout;
2. its least generated source scaling is explicit;
3. lifting for that least-generated endpoint map descends across the
   identity-underlying source enrichment to the induced type-(A) attachment.

This file proves that the least-generated source is the actual pushout in
`ScaledSSet` of the two restriction legs of the Leibniz square.  The proof uses
Mathlib's native `SSet.Subcomplex.unionProd.isPushout` universal property and
checks scaledness only on the four generators of the v1.53 scaling.
-/

/-! ## The four scaled objects of the Leibniz span -/

/-- The `Delta[n] x {epsilon}` leg with the restriction scaling from v1.53. -/
def standardTypeAEndpointSimplexEndpointObject
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((Δ[g.n] : SSet.{u}) ⊗
      (intervalEndpoint g.endpoint : SSet.{u}))
    (standardTypeAEndpointSimplexEndpointLegScaling g)

/-- The `Lambda_i^n x Delta[1]` leg with the restriction scaling from v1.53. -/
def standardTypeAEndpointHornIntervalObject
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((SSet.horn g.n g.i : SSet.{u}) ⊗ Δ[1])
    (standardTypeAEndpointHornIntervalLegScaling g)

/-- The corner scaling on `Lambda_i^n x {epsilon}`. -/
def standardTypeAEndpointCornerScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      ((SSet.horn g.n g.i : SSet.{u}) ⊗
        (intervalEndpoint g.endpoint : SSet.{u})) :=
  pullbackScaling
    (standardTypeAEndpointSimplexEndpointLegScaling g)
    ((SSet.horn g.n g.i).ι ▷
      (intervalEndpoint g.endpoint : SSet.{u}))

/-- The scaled corner object of the endpoint Leibniz span. -/
def standardTypeAEndpointCornerObject
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((SSet.horn g.n g.i : SSet.{u}) ⊗
      (intervalEndpoint g.endpoint : SSet.{u}))
    (standardTypeAEndpointCornerScaling g)

/-- The horn-coordinate map from the corner to `Delta[n] x {epsilon}`. -/
def standardTypeAEndpointCornerToSimplexEndpoint
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointCornerObject g ⟶
      standardTypeAEndpointSimplexEndpointObject g where
  map :=
    (SSet.horn g.n g.i).ι ▷
      (intervalEndpoint g.endpoint : SSet.{u})
  scaled := pullbackScaling_map _ _

/-- The endpoint-coordinate map from the corner to `Lambda_i^n x Delta[1]`. -/
def standardTypeAEndpointCornerToHornInterval
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointCornerObject g ⟶
      standardTypeAEndpointHornIntervalObject g where
  map :=
    (SSet.horn g.n g.i : SSet.{u}) ◁
      (intervalEndpoint g.endpoint).ι
  scaled := by
    intro t ht
    change
      (standardTypeAEndpointInducedProductPullbackScaling g).thin
        ((SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌)
            (((SSet.horn g.n g.i : SSet.{u}) ◁
              (intervalEndpoint g.endpoint).ι).app (op ⦋2⦌) t))
    change
      (standardTypeAEndpointInducedProductPullbackScaling g).thin
        ((SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌)
            ((((SSet.horn g.n g.i).ι ▷
              (intervalEndpoint g.endpoint : SSet.{u}))).app (op ⦋2⦌) t))
      at ht
    have hw := ConcreteCategory.congr_hom
      (congr_app (standardTypeAEndpointPushoutSquare g).w (op ⦋2⦌)) t
    change
      (SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌)
            ((((SSet.horn g.n g.i).ι ▷
              (intervalEndpoint g.endpoint : SSet.{u}))).app (op ⦋2⦌) t) =
        (SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌)
            (((SSet.horn g.n g.i : SSet.{u}) ◁
              (intervalEndpoint g.endpoint).ι).app (op ⦋2⦌) t)
      at hw
    rw [← hw]
    exact ht

/-- The first canonical leg into the least-generated union-product source. -/
def standardTypeAEndpointGeneratedInl
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointSimplexEndpointObject g ⟶
      standardTypeAEndpointGeneratedPushoutSource g where
  map :=
    SSet.Subcomplex.unionProd.ι₁
      (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)
  scaled := standardTypeAEndpointGeneratedPushout_inl_scaled g

/-- The second canonical leg into the least-generated union-product source. -/
def standardTypeAEndpointGeneratedInr
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointHornIntervalObject g ⟶
      standardTypeAEndpointGeneratedPushoutSource g where
  map :=
    SSet.Subcomplex.unionProd.ι₂
      (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)
  scaled := standardTypeAEndpointGeneratedPushout_inr_scaled g

/-- The scaled Leibniz square commutes because the underlying square is exactly
Mathlib's `unionProd` pushout square. -/
theorem standardTypeAEndpointGeneratedPushout_commutes
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointCornerToSimplexEndpoint g ≫
        standardTypeAEndpointGeneratedInl g =
      standardTypeAEndpointCornerToHornInterval g ≫
        standardTypeAEndpointGeneratedInr g := by
  apply ScaledSSet.ScaledMap.ext
  exact (standardTypeAEndpointPushoutSquare g).w

/-! ## Lift the underlying pushout universal property to `ScaledSSet` -/

/-- A compatible scaled square gives the ordinary simplicial compatibility
equation used by the native `unionProd` pushout. -/
theorem standardTypeAEndpointGeneratedPushout_compatibility_map
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    (f : standardTypeAEndpointSimplexEndpointObject g ⟶ W)
    (h : standardTypeAEndpointHornIntervalObject g ⟶ W)
    (w : standardTypeAEndpointCornerToSimplexEndpoint g ≫ f =
      standardTypeAEndpointCornerToHornInterval g ≫ h) :
    ((SSet.horn g.n g.i).ι ▷
        (intervalEndpoint g.endpoint : SSet.{u})) ≫ f.map =
      ((SSet.horn g.n g.i : SSet.{u}) ◁
        (intervalEndpoint g.endpoint).ι) ≫ h.map := by
  have hw := congrArg ScaledSSet.ScaledMap.map w
  change
    (((SSet.horn g.n g.i).ι ▷
        (intervalEndpoint g.endpoint : SSet.{u})) ≫ f.map) =
      (((SSet.horn g.n g.i : SSet.{u}) ◁
        (intervalEndpoint g.endpoint).ι) ≫ h.map) at hw
  exact hw

/-- The underlying simplicial desc map supplied by the native `unionProd`
pushout. -/
def standardTypeAEndpointGeneratedPushoutDescMap
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    (f : standardTypeAEndpointSimplexEndpointObject g ⟶ W)
    (h : standardTypeAEndpointHornIntervalObject g ⟶ W)
    (w : standardTypeAEndpointCornerToSimplexEndpoint g ≫ f =
      standardTypeAEndpointCornerToHornInterval g ≫ h) :
    ((SSet.horn g.n g.i).unionProd
      (intervalEndpoint g.endpoint) : SSet.{u}) ⟶ W.carrier :=
  (standardTypeAEndpointPushoutSquare g).desc
    f.map h.map
    (standardTypeAEndpointGeneratedPushout_compatibility_map g f h w)

/-- The ordinary desc map is scaled for the least generated source scaling. -/
theorem standardTypeAEndpointGeneratedPushoutDescMap_scaled
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    (f : standardTypeAEndpointSimplexEndpointObject g ⟶ W)
    (h : standardTypeAEndpointHornIntervalObject g ⟶ W)
    (w : standardTypeAEndpointCornerToSimplexEndpoint g ≫ f =
      standardTypeAEndpointCornerToHornInterval g ≫ h) :
    IsScaledMap
      (standardTypeAEndpointGeneratedPushoutScaling g)
      W.scaling
      (standardTypeAEndpointGeneratedPushoutDescMap g f h w) := by
  intro t ht
  change
    (∃ x :
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint) : SSet.{u}).obj (op ⦋1⦌),
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint) : SSet.{u}).σ 0 x = t) ∨
    (∃ x :
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint) : SSet.{u}).obj (op ⦋1⦌),
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint) : SSet.{u}).σ 1 x = t) ∨
    (∃ x :
        ((Δ[g.n] : SSet.{u}) ⊗
          (intervalEndpoint g.endpoint : SSet.{u})).obj (op ⦋2⦌),
      (standardTypeAEndpointSimplexEndpointLegScaling g).thin x ∧
        (SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌) x = t) ∨
    ∃ x :
        ((SSet.horn g.n g.i : SSet.{u}) ⊗ Δ[1]).obj (op ⦋2⦌),
      (standardTypeAEndpointHornIntervalLegScaling g).thin x ∧
        (SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌) x = t
    at ht
  rcases ht with
    ⟨x, rfl⟩ | ⟨x, rfl⟩ | ⟨x, hx, rfl⟩ | ⟨x, hx, rfl⟩
  · rw [SSet.σ_naturality_apply
      (standardTypeAEndpointGeneratedPushoutDescMap g f h w) 0 x]
    exact W.scaling.thin_sigma_zero _
  · rw [SSet.σ_naturality_apply
      (standardTypeAEndpointGeneratedPushoutDescMap g f h w) 1 x]
    exact W.scaling.thin_sigma_one _
  · have hfac :
      (standardTypeAEndpointGeneratedPushoutDescMap g f h w).app
          (op ⦋2⦌)
          ((SSet.Subcomplex.unionProd.ι₁
            (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
              (op ⦋2⦌) x) =
        f.map.app (op ⦋2⦌) x := by
      change
        ((standardTypeAEndpointPushoutSquare g).desc
            f.map h.map
            (standardTypeAEndpointGeneratedPushout_compatibility_map
              g f h w)).app
            (op ⦋2⦌)
            ((SSet.Subcomplex.unionProd.ι₁
              (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
                (op ⦋2⦌) x) =
          f.map.app (op ⦋2⦌) x
      exact ConcreteCategory.congr_hom
        (congr_app
          ((standardTypeAEndpointPushoutSquare g).inl_desc
            f.map h.map
            (standardTypeAEndpointGeneratedPushout_compatibility_map
              g f h w))
          (op ⦋2⦌)) x
    rw [hfac]
    exact f.scaled x hx
  · have hfac :
      (standardTypeAEndpointGeneratedPushoutDescMap g f h w).app
          (op ⦋2⦌)
          ((SSet.Subcomplex.unionProd.ι₂
            (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
              (op ⦋2⦌) x) =
        h.map.app (op ⦋2⦌) x := by
      change
        ((standardTypeAEndpointPushoutSquare g).desc
            f.map h.map
            (standardTypeAEndpointGeneratedPushout_compatibility_map
              g f h w)).app
            (op ⦋2⦌)
            ((SSet.Subcomplex.unionProd.ι₂
              (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
                (op ⦋2⦌) x) =
          h.map.app (op ⦋2⦌) x
      exact ConcreteCategory.congr_hom
        (congr_app
          ((standardTypeAEndpointPushoutSquare g).inr_desc
            f.map h.map
            (standardTypeAEndpointGeneratedPushout_compatibility_map
              g f h w))
          (op ⦋2⦌)) x
    rw [hfac]
    exact h.scaled x hx

/-- The native `unionProd` desc map upgraded to a morphism of scaled
simplicial sets. -/
def standardTypeAEndpointGeneratedPushoutDesc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    (f : standardTypeAEndpointSimplexEndpointObject g ⟶ W)
    (h : standardTypeAEndpointHornIntervalObject g ⟶ W)
    (w : standardTypeAEndpointCornerToSimplexEndpoint g ≫ f =
      standardTypeAEndpointCornerToHornInterval g ≫ h) :
    standardTypeAEndpointGeneratedPushoutSource g ⟶ W where
  map := standardTypeAEndpointGeneratedPushoutDescMap g f h w
  scaled := standardTypeAEndpointGeneratedPushoutDescMap_scaled g f h w

@[simp, reassoc]
theorem standardTypeAEndpointGeneratedPushout_inl_desc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    (f : standardTypeAEndpointSimplexEndpointObject g ⟶ W)
    (h : standardTypeAEndpointHornIntervalObject g ⟶ W)
    (w : standardTypeAEndpointCornerToSimplexEndpoint g ≫ f =
      standardTypeAEndpointCornerToHornInterval g ≫ h) :
    standardTypeAEndpointGeneratedInl g ≫
        standardTypeAEndpointGeneratedPushoutDesc g f h w = f := by
  apply ScaledSSet.ScaledMap.ext
  change
    SSet.Subcomplex.unionProd.ι₁
        (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫
      standardTypeAEndpointGeneratedPushoutDescMap g f h w = f.map
  exact (standardTypeAEndpointPushoutSquare g).inl_desc
    f.map h.map
    (standardTypeAEndpointGeneratedPushout_compatibility_map g f h w)

@[simp, reassoc]
theorem standardTypeAEndpointGeneratedPushout_inr_desc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    (f : standardTypeAEndpointSimplexEndpointObject g ⟶ W)
    (h : standardTypeAEndpointHornIntervalObject g ⟶ W)
    (w : standardTypeAEndpointCornerToSimplexEndpoint g ≫ f =
      standardTypeAEndpointCornerToHornInterval g ≫ h) :
    standardTypeAEndpointGeneratedInr g ≫
        standardTypeAEndpointGeneratedPushoutDesc g f h w = h := by
  apply ScaledSSet.ScaledMap.ext
  change
    SSet.Subcomplex.unionProd.ι₂
        (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫
      standardTypeAEndpointGeneratedPushoutDescMap g f h w = h.map
  exact (standardTypeAEndpointPushoutSquare g).inr_desc
    f.map h.map
    (standardTypeAEndpointGeneratedPushout_compatibility_map g f h w)

/-- Uniqueness of a scaled desc map follows from uniqueness of the underlying
ordinary `unionProd` desc map. -/
theorem standardTypeAEndpointGeneratedPushout_hom_ext
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {W : ScaledSSet.{u}}
    {f h : standardTypeAEndpointGeneratedPushoutSource g ⟶ W}
    (h₁ : standardTypeAEndpointGeneratedInl g ≫ f =
      standardTypeAEndpointGeneratedInl g ≫ h)
    (h₂ : standardTypeAEndpointGeneratedInr g ≫ f =
      standardTypeAEndpointGeneratedInr g ≫ h) :
    f = h := by
  apply ScaledSSet.ScaledMap.ext
  apply (standardTypeAEndpointPushoutSquare g).hom_ext
  · have hm := congrArg ScaledSSet.ScaledMap.map h₁
    change
      SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫ f.map =
        SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫ h.map
      at hm
    exact hm
  · have hm := congrArg ScaledSSet.ScaledMap.map h₂
    change
      SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫ f.map =
        SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫ h.map
      at hm
    exact hm

/-- The v1.53 least-generated source is the actual categorical pushout of the
scaled endpoint Leibniz span in `ScaledSSet`. -/
def standardTypeAEndpointGeneratedPushout_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (standardTypeAEndpointCornerToSimplexEndpoint g)
      (standardTypeAEndpointCornerToHornInterval g)
      (standardTypeAEndpointGeneratedInl g)
      (standardTypeAEndpointGeneratedInr g) := by
  refine {
    w := standardTypeAEndpointGeneratedPushout_commutes g
    isColimit' := ⟨?_⟩
  }
  exact PushoutCocone.IsColimit.mk
    (standardTypeAEndpointGeneratedPushout_commutes g)
    (fun s => standardTypeAEndpointGeneratedPushoutDesc
      g s.inl s.inr s.condition)
    (fun s => standardTypeAEndpointGeneratedPushout_inl_desc
      g s.inl s.inr s.condition)
    (fun s => standardTypeAEndpointGeneratedPushout_inr_desc
      g s.inl s.inr s.condition)
    (by
      intro s m hm₁ hm₂
      apply standardTypeAEndpointGeneratedPushout_hom_ext g
      · rw [hm₁, standardTypeAEndpointGeneratedPushout_inl_desc]
      · rw [hm₂, standardTypeAEndpointGeneratedPushout_inr_desc])

/-! ## The canonical scaled Leibniz comparison map -/

/-- The target cylinder is the cartesian product of the standard scaled
simplex with the uniquely scaled interval. -/
theorem standardTypeAEndpointCylinder_is_scaledCartesianProduct
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    scaledCartesianProduct
        (scaledSimplex (standardTypeASimplexScaling g.i))
        (scaledInterval
          (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u}))) =
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  scaledSimplex_product_interval_eq_cylinder
    (standardTypeASimplexScaling g.i)
    (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u}))

/-- The natural map from the simplex-endpoint leg to the scaled cylinder. -/
def standardTypeAEndpointSimplexEndpointToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointSimplexEndpointObject g ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  standardTypeAEndpointGeneratedInl g ≫
    standardTypeAEndpointGeneratedPushoutProductHom g

/-- Its underlying map is the tensor of the simplex identity with the endpoint
inclusion. -/
theorem standardTypeAEndpointSimplexEndpointToCylinder_map
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointSimplexEndpointToCylinder g).map =
      (Δ[g.n] : SSet.{u}) ◁ (intervalEndpoint g.endpoint).ι := by
  change
    (standardTypeAEndpointGeneratedInl g).map ≫
        (standardTypeAEndpointGeneratedPushoutProductHom g).map =
      (Δ[g.n] : SSet.{u}) ◁ (intervalEndpoint g.endpoint).ι
  rw [standardTypeAEndpointGeneratedPushoutProductHom_map]
  change
    SSet.Subcomplex.unionProd.ι₁
        (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint)).ι =
      (Δ[g.n] : SSet.{u}) ◁ (intervalEndpoint g.endpoint).ι
  exact SSet.Subcomplex.unionProd.ι₁_ι
    (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)

/-- The natural map from the horn-interval leg to the scaled cylinder. -/
def standardTypeAEndpointHornIntervalToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointHornIntervalObject g ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  standardTypeAEndpointGeneratedInr g ≫
    standardTypeAEndpointGeneratedPushoutProductHom g

/-- Its underlying map is the tensor of the horn inclusion with the interval
identity. -/
theorem standardTypeAEndpointHornIntervalToCylinder_map
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointHornIntervalToCylinder g).map =
      (SSet.horn g.n g.i).ι ▷ (Δ[1] : SSet.{u}) := by
  change
    (standardTypeAEndpointGeneratedInr g).map ≫
        (standardTypeAEndpointGeneratedPushoutProductHom g).map =
      (SSet.horn g.n g.i).ι ▷ (Δ[1] : SSet.{u})
  rw [standardTypeAEndpointGeneratedPushoutProductHom_map]
  change
    SSet.Subcomplex.unionProd.ι₂
        (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint)).ι =
      (SSet.horn g.n g.i).ι ▷ (Δ[1] : SSet.{u})
  exact SSet.Subcomplex.unionProd.ι₂_ι
    (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)

/-- The two product-leg maps into the cylinder agree on the corner. -/
theorem standardTypeAEndpointCylinder_compatibility
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointCornerToSimplexEndpoint g ≫
        standardTypeAEndpointSimplexEndpointToCylinder g =
      standardTypeAEndpointCornerToHornInterval g ≫
        standardTypeAEndpointHornIntervalToCylinder g := by
  simpa only [standardTypeAEndpointSimplexEndpointToCylinder,
    standardTypeAEndpointHornIntervalToCylinder, Category.assoc] using
    congrArg
      (fun k => k ≫ standardTypeAEndpointGeneratedPushoutProductHom g)
      (standardTypeAEndpointGeneratedPushout_commutes g)

/-- The canonical scaled Leibniz pushout-product map obtained by the actual
`ScaledSSet` pushout universal property. -/
def standardTypeAEndpointScaledLeibnizPushoutProductHom
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutSource g ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  (standardTypeAEndpointGeneratedPushout_isPushout g).desc
    (standardTypeAEndpointSimplexEndpointToCylinder g)
    (standardTypeAEndpointHornIntervalToCylinder g)
    (standardTypeAEndpointCylinder_compatibility g)

/-- The categorical scaled Leibniz map is literally the v1.53 least-generated
endpoint map. -/
theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointScaledLeibnizPushoutProductHom g =
      standardTypeAEndpointGeneratedPushoutProductHom g := by
  apply (standardTypeAEndpointGeneratedPushout_isPushout g).hom_ext
  · change
      standardTypeAEndpointGeneratedInl g ≫
          (standardTypeAEndpointGeneratedPushout_isPushout g).desc
            (standardTypeAEndpointSimplexEndpointToCylinder g)
            (standardTypeAEndpointHornIntervalToCylinder g)
            (standardTypeAEndpointCylinder_compatibility g) =
        standardTypeAEndpointGeneratedInl g ≫
          standardTypeAEndpointGeneratedPushoutProductHom g
    rw [(standardTypeAEndpointGeneratedPushout_isPushout g).inl_desc]
    rfl
  · change
      standardTypeAEndpointGeneratedInr g ≫
          (standardTypeAEndpointGeneratedPushout_isPushout g).desc
            (standardTypeAEndpointSimplexEndpointToCylinder g)
            (standardTypeAEndpointHornIntervalToCylinder g)
            (standardTypeAEndpointCylinder_compatibility g) =
        standardTypeAEndpointGeneratedInr g ≫
          standardTypeAEndpointGeneratedPushoutProductHom g
    rw [(standardTypeAEndpointGeneratedPushout_isPushout g).inr_desc]
    rfl

/-- Hence its underlying simplicial map is the native union-product inclusion. -/
theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_map
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointScaledLeibnizPushoutProductHom g).map =
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint)).ι := by
  rw [standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated]
  exact standardTypeAEndpointGeneratedPushoutProductHom_map g

/-- The generated and induced endpoint maps have the same underlying map. -/
theorem standardTypeAEndpointGeneratedPushoutProductHom_map_eq_induced
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointGeneratedPushoutProductHom g).map =
      (standardTypeAEndpointPushoutProductHom g).map := by
  rw [standardTypeAEndpointGeneratedPushoutProductHom_map]
  rfl

/-- The scaled categorical Leibniz map has exactly Mathlib's native v1.51
Leibniz inclusion as underlying map. -/
theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_map_eq_native
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointScaledLeibnizPushoutProductHom g).map =
      (standardTypeAEndpointLeibnizSquare g).ι := by
  rw [standardTypeAEndpointScaledLeibnizPushoutProductHom_map]
  exact (standardTypeAEndpointLeibnizSquare_ι g).symm

/-- The pinned Mathlib parametrized-adjunction lifting mate applies to the
underlying map of the genuine scaled categorical Leibniz construction. -/
theorem standardTypeAEndpointScaledLeibniz_underlying_hasLiftingProperty_iff
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {X Y : SSet.{u}}
    (p : X ⟶ Y) :
    HasLiftingProperty
        (standardTypeAEndpointScaledLeibnizPushoutProductHom g).map p ↔
      HasLiftingProperty
        (intervalEndpoint g.endpoint).ι
        (standardTypeAHornPullbackHomSquare g p).π := by
  rw [standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated]
  rw [standardTypeAEndpointGeneratedPushoutProductHom_map_eq_induced]
  exact standardTypeAEndpointPushoutProduct_hasLiftingProperty_iff g p

/-! ## Generator and stability interfaces at the categorical level -/

/-- The genuine scaled categorical Leibniz pushout-products for standard
type-(A) horns and both interval endpoints. -/
def standardTypeAScaledLeibnizPushoutProductGenerators :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun g : StandardTypeAHornAttachmentGeneratorIndex =>
      standardTypeAEndpointScaledLeibnizPushoutProductHom g)

/-- Every categorical scaled Leibniz map lies in its generator property. -/
theorem standardTypeAScaledLeibnizPushoutProductGenerator_mem
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAScaledLeibnizPushoutProductGenerators :
      MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointScaledLeibnizPushoutProductHom g) :=
  MorphismProperty.ofHoms.mk g

/-- The categorical scaled Leibniz family is literally the v1.54
least-generated endpoint family. -/
theorem standardTypeAScaledLeibnizPushoutProductGenerators_eq_generated :
    (standardTypeAScaledLeibnizPushoutProductGenerators :
      MorphismProperty (ScaledSSet.{u})) =
    standardTypeAEndpointGeneratedPushoutProductGenerators := by
  apply le_antisymm
  · intro A B f hf
    dsimp [standardTypeAScaledLeibnizPushoutProductGenerators] at hf
    cases hf with
    | mk g =>
        rw [standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated]
        exact standardTypeAEndpointGeneratedPushoutProductGenerator_mem g
  · intro A B f hf
    dsimp [standardTypeAEndpointGeneratedPushoutProductGenerators] at hf
    cases hf with
    | mk g =>
        rw [← standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated]
        exact standardTypeAScaledLeibnizPushoutProductGenerator_mem g

/-- Stability under the actual scaled categorical Leibniz construction. -/
structure StandardTypeAScaledLeibnizPushoutProductStable
    (L : MorphismProperty (ScaledSSet.{u})) : Prop where
  pushoutProduct_mem :
    ∀ g : StandardTypeAHornAttachmentGeneratorIndex,
      L (standardTypeAScaledHornGeneratorHom
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)) →
      L (standardTypeAEndpointScaledLeibnizPushoutProductHom g)

namespace StandardTypeAScaledLeibnizPushoutProductStable

variable {L : MorphismProperty (ScaledSSet.{u})}

/-- Categorical Leibniz stability implies the v1.54 least-generated stability
interface. -/
def toGenerated
    (K : StandardTypeAScaledLeibnizPushoutProductStable L) :
    StandardTypeAEndpointGeneratedPushoutProductStable L where
  pushoutProduct_mem := by
    intro g hg
    rw [← standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated]
    exact StandardTypeAScaledLeibnizPushoutProductStable.pushoutProduct_mem
      K g hg

/-- Conversely the v1.54 least-generated stability interface is already
stability under the genuine categorical scaled Leibniz construction. -/
def ofGenerated
    (K : StandardTypeAEndpointGeneratedPushoutProductStable L) :
    StandardTypeAScaledLeibnizPushoutProductStable L where
  pushoutProduct_mem := by
    intro g hg
    rw [standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated]
    exact StandardTypeAEndpointGeneratedPushoutProductStable.pushoutProduct_mem
      K g hg

end StandardTypeAScaledLeibnizPushoutProductStable

/-- External type-(A) comparison data stated entirely with the genuine scaled
categorical Leibniz construction. -/
structure StandardTypeAExternalScaledLeibnizComparison
    (E : MorphismProperty (ScaledSSet.{u})) : Prop where
  typeAHorns_le_externalGenerated :
    (standardTypeAScaledHornGenerators : MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne E
  scaledLeibnizPushoutProductStable :
    StandardTypeAScaledLeibnizPushoutProductStable
      (externalGeneratedScaledAnodyne E)

namespace StandardTypeAExternalScaledLeibnizComparison

variable {E : MorphismProperty (ScaledSSet.{u})}

/-- The categorical comparison data supplies the exact v1.54 comparison
interface. -/
def toGeneratedPushoutComparison
    (K : StandardTypeAExternalScaledLeibnizComparison E) :
    StandardTypeAExternalGeneratedPushoutComparison E where
  typeAHorns_le_externalGenerated :=
    StandardTypeAExternalScaledLeibnizComparison.typeAHorns_le_externalGenerated K
  generatedEndpointPushoutProductStable :=
    StandardTypeAScaledLeibnizPushoutProductStable.toGenerated
      (StandardTypeAExternalScaledLeibnizComparison.scaledLeibnizPushoutProductStable K)

/-- Consequently the type-(A) induced attachments lie in the external
orthogonally generated left class. -/
theorem inducedTypeAAttachments_le_externalGenerated
    (K : StandardTypeAExternalScaledLeibnizComparison E) :
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne E :=
  StandardTypeAExternalGeneratedPushoutComparison.inducedTypeAAttachments_le_externalGenerated
    (toGeneratedPushoutComparison K)

/-- The v1.50 induced endpoint-pushout-product presentation is externally
generated as well. -/
theorem endpointPushoutProducts_le_externalGenerated
    (K : StandardTypeAExternalScaledLeibnizComparison E) :
    (standardTypeAEndpointPushoutProductGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      externalGeneratedScaledAnodyne E :=
  StandardTypeAExternalGeneratedPushoutComparison.endpointPushoutProducts_le_externalGenerated
    (toGeneratedPushoutComparison K)

end StandardTypeAExternalScaledLeibnizComparison

/-!
The type-(A) comparison is now categorical:

```text
ordinary Mathlib unionProd pushout
  -> restriction scalings on the three source pieces
  -> actual IsPushout in ScaledSSet
  -> canonical scaled Leibniz pushout-product map
  = v1.53 least-generated endpoint map
  -> underlying map = v1.51 native Leibniz inclusion
  -> native pullback-hom lifting mate
  -> v1.54 epi source-enrichment descent
  -> T_induced^(A) <= E.rlp.llp.
```
-/

end

end KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55
