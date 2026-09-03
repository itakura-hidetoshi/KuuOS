import KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76

namespace KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationScaledCartesianIntervalCylinderV1_52
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73
open KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76

universe u

noncomputable section

set_option backward.isDefEq.respectTransparency false

/-!
# Opposite endpoint A-cell and the full endpoint transfinite certificate v1.77

The boundary-prism inclusion is already one raw A/B transfinite composition by
v1.76.  The remaining endpoint map is the pushout of one literal standard
A-cell, up to explicit scaled isomorphism.  We then prepend that raw A-step to
the v1.76 natural-number sequence, rather than assuming that arbitrary
transfinite compositions are closed under binary composition.
-/

/-! ## The least-generated endpoint source is the ambient pullback source -/

theorem standardTypeAEndpointInducedProductPullbackScaling_le_generated
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScalingLE
      (standardTypeAEndpointInducedProductPullbackScaling g)
      (standardTypeAEndpointGeneratedPushoutScaling g) := by
  intro t ht
  rcases
      (SSet.Subcomplex.mem_unionProd_iff
        (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) t.val).mp t.property with
    hendpoint | hhorn
  · let x :
        ((Δ[g.n] : SSet.{u}) ⊗
          (intervalEndpoint g.endpoint : SSet.{u})).obj (op ⦋2⦌) :=
      ⟨t.val.1, ⟨t.val.2, hendpoint⟩⟩
    have hxmap :
        (SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌) x = t := by
      apply Subtype.ext
      rfl
    refine Or.inr (Or.inr (Or.inl ⟨x, ?_, hxmap⟩))
    change
      (standardTypeAEndpointInducedProductPullbackScaling g).thin
        ((SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌) x)
    rw [hxmap]
    exact ht
  · let x :
        ((SSet.horn g.n g.i : SSet.{u}) ⊗ Δ[1]).obj (op ⦋2⦌) :=
      ⟨⟨t.val.1, hhorn⟩, t.val.2⟩
    have hxmap :
        (SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌) x = t := by
      apply Subtype.ext
      rfl
    refine Or.inr (Or.inr (Or.inr ⟨x, ?_, hxmap⟩))
    change
      (standardTypeAEndpointInducedProductPullbackScaling g).thin
        ((SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint)).app
            (op ⦋2⦌) x)
    rw [hxmap]
    exact ht

theorem standardTypeAEndpointGeneratedPushoutScaling_eq_induced
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutScaling g =
      standardTypeAEndpointInducedProductPullbackScaling g :=
  scaling_eq_of_le_antisymm
    (standardTypeAEndpointGeneratedPushoutScaling_le_induced g)
    (standardTypeAEndpointInducedProductPullbackScaling_le_generated g)

def standardTypeAEndpointAmbientSourceScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint) : SSet.{u}) :=
  pullbackScaling
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling
    ((SSet.horn g.n g.i).unionProd
      (intervalEndpoint g.endpoint)).ι

theorem standardTypeAEndpointGeneratedPushoutScaling_eq_ambient
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutScaling g =
      standardTypeAEndpointAmbientSourceScaling g := by
  rw [standardTypeAEndpointGeneratedPushoutScaling_eq_induced g]
  unfold standardTypeAEndpointInducedProductPullbackScaling
  unfold standardTypeAEndpointCylinderProductScaling
  unfold standardTypeAEndpointAmbientSourceScaling
  change
    pullbackScaling
        (cartesianProductScaling
          (standardTypeASimplexScaling g.i)
          (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u})))
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint)).ι =
      pullbackScaling
        (simplexCylinderScaling (standardTypeASimplexScaling g.i))
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint)).ι
  exact congrArg
    (fun s => pullbackScaling s
      ((SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint)).ι)
    (cartesianProductScaling_interval_eq_simplexCylinderScaling
      (standardTypeASimplexScaling g.i)
      (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u})))

def standardTypeAEndpointAmbientSource
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((SSet.horn g.n g.i).unionProd
      (intervalEndpoint g.endpoint) : SSet.{u})
    (standardTypeAEndpointAmbientSourceScaling g)

def standardTypeAEndpointGeneratedSourceIsoAmbient
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutSource g ≅
      standardTypeAEndpointAmbientSource g :=
  scalingEqualityIso
    (standardTypeAEndpointGeneratedPushoutScaling g)
    (standardTypeAEndpointAmbientSourceScaling g)
    (standardTypeAEndpointGeneratedPushoutScaling_eq_ambient g)

/-! ## The interval boundary is the two disjoint endpoints -/

theorem intervalEndpoint_zero_eq_face_one :
    intervalEndpoint (0 : Fin 2) =
      SSet.stdSimplex.face ({(1 : Fin 2)}ᶜ) := by
  unfold intervalEndpoint
  rw [SSet.stdSimplex.face_singleton_compl]
  apply congrArg SSet.Subcomplex.ofSimplex
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k
  rfl

theorem intervalEndpoint_one_eq_face_zero :
    intervalEndpoint (1 : Fin 2) =
      SSet.stdSimplex.face ({(0 : Fin 2)}ᶜ) := by
  unfold intervalEndpoint
  rw [SSet.stdSimplex.face_singleton_compl]
  apply congrArg SSet.Subcomplex.ofSimplex
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k
  rfl

theorem intervalEndpoint_eq_face_rev (ε : Fin 2) :
    intervalEndpoint ε =
      SSet.stdSimplex.face ({ε.rev}ᶜ) := by
  fin_cases ε
  · simpa using intervalEndpoint_zero_eq_face_one
  · simpa using intervalEndpoint_one_eq_face_zero

theorem intervalEndpoint_inf_rev_eq_bot (ε : Fin 2) :
    intervalEndpoint ε ⊓ intervalEndpoint ε.rev =
      (⊥ : (Δ[1] : SSet.{u}).Subcomplex) := by
  fin_cases ε
  · change
      intervalEndpoint (0 : Fin 2) ⊓ intervalEndpoint (1 : Fin 2) = ⊥
    rw [intervalEndpoint_zero_eq_face_one,
      intervalEndpoint_one_eq_face_zero,
      SSet.stdSimplex.face_inter_face]
    simp
  · change
      intervalEndpoint (1 : Fin 2) ⊓ intervalEndpoint (0 : Fin 2) = ⊥
    rw [intervalEndpoint_one_eq_face_zero,
      intervalEndpoint_zero_eq_face_one,
      SSet.stdSimplex.face_inter_face]
    simp

theorem intervalBoundary_eq_endpoint_zero_sup_one :
    (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
      intervalEndpoint 0 ⊔ intervalEndpoint 1 := by
  apply le_antisymm
  · rw [SSet.boundary_eq_iSup]
    refine iSup_le ?_
    intro i
    fin_cases i
    · rw [← intervalEndpoint_one_eq_face_zero]
      exact le_sup_right
    · rw [← intervalEndpoint_zero_eq_face_one]
      exact le_sup_left
  · exact sup_le
      (intervalEndpoint_le_boundary 0)
      (intervalEndpoint_le_boundary 1)

theorem intervalBoundary_eq_endpoint_sup_rev (ε : Fin 2) :
    (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
      intervalEndpoint ε ⊔ intervalEndpoint ε.rev := by
  fin_cases ε
  · change
      (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
        intervalEndpoint (0 : Fin 2) ⊔ intervalEndpoint (1 : Fin 2)
    exact intervalBoundary_eq_endpoint_zero_sup_one
  · change
      (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
        intervalEndpoint (1 : Fin 2) ⊔ intervalEndpoint (0 : Fin 2)
    simpa [sup_comm] using intervalBoundary_eq_endpoint_zero_sup_one

/-! ## The ordinary missing-endpoint square -/

def standardTypeAEndpointOppositeCornerSubcomplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex :=
  (SSet.horn g.n g.i).prod (intervalEndpoint g.endpoint.rev)

def standardTypeAEndpointOppositeSimplexSubcomplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex :=
  (⊤ : (Δ[g.n] : SSet.{u}).Subcomplex).prod
    (intervalEndpoint g.endpoint.rev)

def standardTypeAEndpointOppositeCarrierBicartSq
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    SSet.Subcomplex.BicartSq
      (standardTypeAEndpointOppositeCornerSubcomplex g)
      (standardTypeAEndpointOppositeSimplexSubcomplex g)
      ((SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint))
      (standardTypeABoundaryPrismSubcomplex g) where
  sup_eq := by
    rw [standardTypeABoundaryPrismSubcomplex,
      intervalBoundary_eq_endpoint_sup_rev g.endpoint]
    ext d ⟨x, y⟩
    change
      ((x ∈ Set.univ ∧ y ∈ (intervalEndpoint g.endpoint.rev).obj d) ∨
        (y ∈ (intervalEndpoint g.endpoint).obj d ∨
          x ∈ (SSet.horn g.n g.i).obj d)) ↔
        ((y ∈ (intervalEndpoint g.endpoint).obj d ∨
          y ∈ (intervalEndpoint g.endpoint.rev).obj d) ∨
          x ∈ (SSet.horn g.n g.i).obj d)
    simp only [Set.mem_univ, true_and]
    tauto
  inf_eq := by
    ext d ⟨x, y⟩
    change
      ((x ∈ Set.univ ∧ y ∈ (intervalEndpoint g.endpoint.rev).obj d) ∧
        (y ∈ (intervalEndpoint g.endpoint).obj d ∨
          x ∈ (SSet.horn g.n g.i).obj d)) ↔
        (x ∈ (SSet.horn g.n g.i).obj d ∧
          y ∈ (intervalEndpoint g.endpoint.rev).obj d)
    have hdis :
        ¬ (y ∈ (intervalEndpoint g.endpoint).obj d ∧
          y ∈ (intervalEndpoint g.endpoint.rev).obj d) := by
      intro h
      have hm :
          y ∈ (intervalEndpoint g.endpoint ⊓
            intervalEndpoint g.endpoint.rev).obj d := h
      rw [intervalEndpoint_inf_rev_eq_bot g.endpoint] at hm
      simpa using hm
    simp only [Set.mem_univ, true_and]
    tauto

noncomputable def standardTypeAEndpointOppositeCarrier_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₃)
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₂)
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq g).le₃₄)
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq g).le₂₄) :=
  (standardTypeAEndpointOppositeCarrierBicartSq g).isPushout.flip

/-! ## Product with an endpoint is the literal standard A cell -/

noncomputable def intervalEndpointIsoStdZero (ε : Fin 2) :
    (Δ[0] : SSet.{u}) ≅ (intervalEndpoint ε : SSet.{u}) :=
  SSet.stdSimplex.faceSingletonComplIso ε.rev ≪≫
    SSet.Subcomplex.eqToIso (intervalEndpoint_eq_face_rev ε).symm

noncomputable def intervalEndpointIsTerminal (ε : Fin 2) :
    IsTerminal (intervalEndpoint ε : SSet.{u}) :=
  IsTerminal.ofIso SSet.stdSimplex.isTerminalObj₀
    (intervalEndpointIsoStdZero ε)

noncomputable def subcomplexProdIntervalEndpointIso
    {X : SSet.{u}}
    (A : X.Subcomplex)
    (ε : Fin 2) :
    (A.prod (intervalEndpoint ε) : SSet.{u}) ≅ (A : SSet.{u}) :=
  SSet.Subcomplex.prodIso A (intervalEndpoint ε) ≪≫
    whiskerLeftIso (A : SSet.{u})
      ((intervalEndpointIsTerminal ε).uniqueUpToIso
        CartesianMonoidalCategory.isTerminalTensorUnit) ≪≫
    ρ_ (A : SSet.{u})

noncomputable def standardTypeAEndpointOppositeCornerCarrierIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointOppositeCornerSubcomplex g : SSet.{u}) ≅
      (SSet.horn g.n g.i : SSet.{u}) :=
  subcomplexProdIntervalEndpointIso
    (SSet.horn g.n g.i) g.endpoint.rev

noncomputable def standardTypeAEndpointOppositeSimplexCarrierIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointOppositeSimplexSubcomplex g : SSet.{u}) ≅
      (Δ[g.n] : SSet.{u}) :=
  subcomplexProdIntervalEndpointIso
      (⊤ : (Δ[g.n] : SSet.{u}).Subcomplex) g.endpoint.rev ≪≫
    SSet.Subcomplex.topIso (Δ[g.n] : SSet.{u})

@[simp]
theorem standardTypeAEndpointOppositeCornerCarrierIso_hom_app_val
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (d : SimplexCategoryᵒᵖ)
    (z : (standardTypeAEndpointOppositeCornerSubcomplex g : SSet.{u}).obj d) :
    ((standardTypeAEndpointOppositeCornerCarrierIso g).hom.app d z).val =
      z.val.1 := by
  simp [standardTypeAEndpointOppositeCornerCarrierIso,
    subcomplexProdIntervalEndpointIso]

@[simp]
theorem standardTypeAEndpointOppositeSimplexCarrierIso_hom_app
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (d : SimplexCategoryᵒᵖ)
    (z : (standardTypeAEndpointOppositeSimplexSubcomplex g : SSet.{u}).obj d) :
    (standardTypeAEndpointOppositeSimplexCarrierIso g).hom.app d z =
      z.val.1 := by
  simp [standardTypeAEndpointOppositeSimplexCarrierIso,
    subcomplexProdIntervalEndpointIso]

def pullbackScalingIso
    {X Y : SSet.{u}}
    (e : X ≅ Y)
    (sY : ScaledSimplicialSet Y) :
    ScaledSSet.of X (pullbackScaling sY e.hom) ≅
      ScaledSSet.of Y sY where
  hom :=
    { map := e.hom
      scaled := pullbackScaling_map _ _ }
  inv :=
    { map := e.inv
      scaled := by
        intro t ht
        change sY.thin (e.hom.app (op ⦋2⦌) (e.inv.app (op ⦋2⦌) t))
        rw [← NatTrans.comp_app_apply, e.inv_hom_id]
        exact ht }
  hom_inv_id := by
    apply ScaledSSet.ScaledMap.ext
    exact e.hom_inv_id
  inv_hom_id := by
    apply ScaledSSet.ScaledMap.ext
    exact e.inv_hom_id

def standardTypeAEndpointOppositeCornerScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      (standardTypeAEndpointOppositeCornerSubcomplex g : SSet.{u}) :=
  pullbackScaling (standardTypeAHornScaling g.i)
    (standardTypeAEndpointOppositeCornerCarrierIso g).hom

def standardTypeAEndpointOppositeSimplexScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      (standardTypeAEndpointOppositeSimplexSubcomplex g : SSet.{u}) :=
  pullbackScaling (standardTypeASimplexScaling g.i)
    (standardTypeAEndpointOppositeSimplexCarrierIso g).hom

def standardTypeAEndpointOppositeCorner
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    (standardTypeAEndpointOppositeCornerSubcomplex g : SSet.{u})
    (standardTypeAEndpointOppositeCornerScaling g)

def standardTypeAEndpointOppositeSimplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    (standardTypeAEndpointOppositeSimplexSubcomplex g : SSet.{u})
    (standardTypeAEndpointOppositeSimplexScaling g)

def standardTypeAEndpointOppositeCornerIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeCorner g ≅
      standardTypeAScaledHorn
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) :=
  pullbackScalingIso
    (standardTypeAEndpointOppositeCornerCarrierIso g)
    (standardTypeAHornScaling g.i)

def standardTypeAEndpointOppositeSimplexIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeSimplex g ≅
      standardTypeAScaledSimplex
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) :=
  pullbackScalingIso
    (standardTypeAEndpointOppositeSimplexCarrierIso g)
    (standardTypeASimplexScaling g.i)

/-! ## Lift the carrier square to a scaled pushout -/

def standardTypeAEndpointOppositeCellHom
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeCorner g ⟶
      standardTypeAEndpointOppositeSimplex g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₂
  scaled := by
    intro t ht
    change (standardTypeAEndpointOppositeCornerScaling g).thin t at ht
    unfold standardTypeAEndpointOppositeCornerScaling at ht
    have hA := standardTypeAHornInclusion_scaled g.i
      ((standardTypeAEndpointOppositeCornerCarrierIso g).hom.app
        (op ⦋2⦌) t) ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeAEndpointOppositeSimplexCarrierIso g).hom.app
          (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₂).app
              (op ⦋2⦌) t))
    simpa using hA

noncomputable def standardTypeAEndpointOppositeCellArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Arrow.mk (standardTypeAEndpointOppositeCellHom g) ≅
      Arrow.mk (standardTypeAScaledHornGeneratorHom
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)) := by
  refine Arrow.isoMk
    (standardTypeAEndpointOppositeCornerIso g)
    (standardTypeAEndpointOppositeSimplexIso g) ?_
  apply ScaledSSet.ScaledMap.ext
  change
    (standardTypeAEndpointOppositeCornerCarrierIso g).hom ≫
        (SSet.horn g.n g.i).ι =
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₂) ≫
        (standardTypeAEndpointOppositeSimplexCarrierIso g).hom
  ext d t
  change
    ((standardTypeAEndpointOppositeCornerCarrierIso g).hom.app d t).val =
      (standardTypeAEndpointOppositeSimplexCarrierIso g).hom.app d
        ((SSet.Subcomplex.homOfLE
          (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₂).app d t)
  rw [standardTypeAEndpointOppositeCornerCarrierIso_hom_app_val,
    standardTypeAEndpointOppositeSimplexCarrierIso_hom_app]
  rfl

theorem standardTypeAEndpointOppositeCellHom_mem_coproductsABC
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})))
      (standardTypeAEndpointOppositeCellHom g) := by
  have hA :
      (MorphismProperty.coproducts.{u}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})))
        (standardTypeAScaledHornGeneratorHom
          (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAGenerator_mem_ABC
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g))
  exact
    ((MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).arrow_mk_iso_iff
      (standardTypeAEndpointOppositeCellArrowIso g)).2 hA

def standardTypeAEndpointOppositeCornerToAmbientSource
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeCorner g ⟶
      standardTypeAEndpointAmbientSource g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₃
  scaled := by
    intro t ht
    change (standardTypeAEndpointOppositeCornerScaling g).thin t at ht
    unfold standardTypeAEndpointOppositeCornerScaling at ht
    have hA := standardTypeAHornInclusion_scaled g.i
      ((standardTypeAEndpointOppositeCornerCarrierIso g).hom.app
        (op ⦋2⦌) t) ht
    change
      (standardTypeASimplexScaling g.i).thin
        (((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint)).ι.app (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq g).le₁₃).app
              (op ⦋2⦌) t)).1
    simpa using hA

def standardTypeAEndpointOppositeSimplexToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeSimplex g ⟶
      standardTypeABoundaryPrism g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq g).le₂₄
  scaled := by
    intro t ht
    change (standardTypeAEndpointOppositeSimplexScaling g).thin t at ht
    unfold standardTypeAEndpointOppositeSimplexScaling at ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeABoundaryPrismSubcomplex g).ι.app (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq g).le₂₄).app
              (op ⦋2⦌) t)).1
    simpa using ht

def standardTypeAEndpointAmbientSourceToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointAmbientSource g ⟶
      standardTypeABoundaryPrism g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq g).le₃₄
  scaled := by
    intro t ht
    change
      (scaledSimplexCylinder
        (standardTypeASimplexScaling g.i)).scaling.thin
        ((standardTypeABoundaryPrismSubcomplex g).ι.app (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq g).le₃₄).app
              (op ⦋2⦌) t))
    change
      (scaledSimplexCylinder
        (standardTypeASimplexScaling g.i)).scaling.thin
        (((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint)).ι.app (op ⦋2⦌) t) at ht
    rw [← NatTrans.comp_app_apply, SSet.Subcomplex.homOfLE_ι]
    exact ht

theorem standardTypeAEndpointOppositeGeneratedScaling_eq_boundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    generatedPushoutScaling
      (standardTypeAEndpointAmbientSourceScaling g)
      (standardTypeAEndpointOppositeSimplexScaling g)
      (standardTypeAEndpointAmbientSourceToBoundary g).map
      (standardTypeAEndpointOppositeSimplexToBoundary g).map =
        standardTypeABoundaryPrismScaling.{u} g := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    rcases ht with hmin | ⟨x, hx, rfl⟩ | ⟨y, hy, rfl⟩
    · exact
        (minimalScaling_map
          (standardTypeABoundaryPrismScaling.{u} g) (𝟙 _)) t hmin
    · exact (standardTypeAEndpointAmbientSourceToBoundary g).scaled x hx
    · exact (standardTypeAEndpointOppositeSimplexToBoundary g).scaled y hy
  · intro t ht
    have hmem' :
        t.val ∈
          (standardTypeAEndpointOppositeSimplexSubcomplex g ⊔
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint g.endpoint))).obj (op ⦋2⦌) := by
      rw [(standardTypeAEndpointOppositeCarrierBicartSq g).sup_eq]
      exact t.property
    have hmem :
        t.val ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint g.endpoint)).obj (op ⦋2⦌) ∨
          t.val ∈
            (standardTypeAEndpointOppositeSimplexSubcomplex g).obj (op ⦋2⦌) := by
      change
        t.val ∈
            (standardTypeAEndpointOppositeSimplexSubcomplex g).obj (op ⦋2⦌) ∨
          t.val ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint g.endpoint)).obj (op ⦋2⦌) at hmem'
      exact hmem'.symm
    rcases hmem with hsource | hopposite
    · let x :
          ((SSet.horn g.n g.i).unionProd
            (intervalEndpoint g.endpoint) : SSet.{u}).obj (op ⦋2⦌) :=
        ⟨t.val, hsource⟩
      have hxmap :
          (standardTypeAEndpointAmbientSourceToBoundary g).map.app
            (op ⦋2⦌) x = t := by
        apply Subtype.ext
        rfl
      refine Or.inr (Or.inl ⟨x, ?_, hxmap⟩)
      change
        (scaledSimplexCylinder
          (standardTypeASimplexScaling g.i)).scaling.thin
          (((SSet.horn g.n g.i).unionProd
            (intervalEndpoint g.endpoint)).ι.app (op ⦋2⦌) x)
      change
        (scaledSimplexCylinder
          (standardTypeASimplexScaling g.i)).scaling.thin
          ((standardTypeABoundaryPrismSubcomplex g).ι.app
            (op ⦋2⦌) t) at ht
      simpa using ht
    · let x :
          (standardTypeAEndpointOppositeSimplexSubcomplex g : SSet.{u}).obj
            (op ⦋2⦌) :=
        ⟨t.val, hopposite⟩
      have hxmap :
          (standardTypeAEndpointOppositeSimplexToBoundary g).map.app
            (op ⦋2⦌) x = t := by
        apply Subtype.ext
        rfl
      refine Or.inr (Or.inr ⟨x, ?_, hxmap⟩)
      change (standardTypeAEndpointOppositeSimplexScaling g).thin x
      unfold standardTypeAEndpointOppositeSimplexScaling
      rw [standardTypeAEndpointOppositeSimplexCarrierIso_hom_app]
      change
        (standardTypeASimplexScaling g.i).thin
          (((standardTypeABoundaryPrismSubcomplex g).ι.app
            (op ⦋2⦌) t).1) at ht
      simpa using ht

noncomputable def standardTypeAEndpointOpposite_scaled_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (standardTypeAEndpointOppositeCornerToAmbientSource g)
      (standardTypeAEndpointOppositeCellHom g)
      (standardTypeAEndpointAmbientSourceToBoundary g)
      (standardTypeAEndpointOppositeSimplexToBoundary g) := by
  have h :
      IsPushout
        (standardTypeAEndpointOppositeCornerToAmbientSource g)
        (standardTypeAEndpointOppositeCellHom g)
        (generatedPushoutInl
          (standardTypeAEndpointAmbientSourceScaling g)
          (standardTypeAEndpointOppositeSimplexScaling g)
          (standardTypeAEndpointAmbientSourceToBoundary g).map
          (standardTypeAEndpointOppositeSimplexToBoundary g).map)
        (generatedPushoutInr
          (standardTypeAEndpointAmbientSourceScaling g)
          (standardTypeAEndpointOppositeSimplexScaling g)
          (standardTypeAEndpointAmbientSourceToBoundary g).map
          (standardTypeAEndpointOppositeSimplexToBoundary g).map) :=
    generatedPushout_isPushout
      (standardTypeAEndpointOppositeCornerToAmbientSource g)
      (standardTypeAEndpointOppositeCellHom g)
      (standardTypeAEndpointAmbientSourceToBoundary g).map
      (standardTypeAEndpointOppositeSimplexToBoundary g).map
      (standardTypeAEndpointOppositeCarrier_isPushout g)
  have hScaling :
      generatedPushoutScaling
          (standardTypeAEndpointAmbientSourceScaling g)
          (standardTypeAEndpointOppositeSimplexScaling g)
          (standardTypeAEndpointAmbientSourceToBoundary g).map
          (standardTypeAEndpointOppositeSimplexToBoundary g).map =
        standardTypeABoundaryPrismScaling.{u} g :=
    standardTypeAEndpointOppositeGeneratedScaling_eq_boundary g
  let eBoundary :
      generatedPushoutTarget
          (standardTypeAEndpointAmbientSourceScaling g)
          (standardTypeAEndpointOppositeSimplexScaling g)
          (standardTypeAEndpointAmbientSourceToBoundary g).map
          (standardTypeAEndpointOppositeSimplexToBoundary g).map ≅
        standardTypeABoundaryPrism g :=
    scalingEqualityIso
      (generatedPushoutScaling
        (standardTypeAEndpointAmbientSourceScaling g)
        (standardTypeAEndpointOppositeSimplexScaling g)
        (standardTypeAEndpointAmbientSourceToBoundary g).map
        (standardTypeAEndpointOppositeSimplexToBoundary g).map)
      (standardTypeABoundaryPrismScaling.{u} g)
      hScaling
  refine h.of_iso
    (Iso.refl (standardTypeAEndpointOppositeCorner g))
    (Iso.refl (standardTypeAEndpointAmbientSource g))
    (Iso.refl (standardTypeAEndpointOppositeSimplex g))
    eBoundary ?_ ?_ ?_ ?_
  · simp
  · simp
  · change
      generatedPushoutInl
          (standardTypeAEndpointAmbientSourceScaling g)
          (standardTypeAEndpointOppositeSimplexScaling g)
          (standardTypeAEndpointAmbientSourceToBoundary g).map
          (standardTypeAEndpointOppositeSimplexToBoundary g).map ≫ eBoundary.hom =
        𝟙 _ ≫ standardTypeAEndpointAmbientSourceToBoundary g
    rw [Category.id_comp]
    apply ScaledSSet.ScaledMap.ext
    change
      (standardTypeAEndpointAmbientSourceToBoundary g).map ≫
          (scalingEqualityIso
            (generatedPushoutScaling
              (standardTypeAEndpointAmbientSourceScaling g)
              (standardTypeAEndpointOppositeSimplexScaling g)
              (standardTypeAEndpointAmbientSourceToBoundary g).map
              (standardTypeAEndpointOppositeSimplexToBoundary g).map)
            (standardTypeABoundaryPrismScaling.{u} g)
            hScaling).hom.map =
        (standardTypeAEndpointAmbientSourceToBoundary g).map
    rw [scalingEqualityIso_hom_map]
    exact Category.comp_id _
  · change
      generatedPushoutInr
          (standardTypeAEndpointAmbientSourceScaling g)
          (standardTypeAEndpointOppositeSimplexScaling g)
          (standardTypeAEndpointAmbientSourceToBoundary g).map
          (standardTypeAEndpointOppositeSimplexToBoundary g).map ≫ eBoundary.hom =
        𝟙 _ ≫ standardTypeAEndpointOppositeSimplexToBoundary g
    rw [Category.id_comp]
    apply ScaledSSet.ScaledMap.ext
    change
      (standardTypeAEndpointOppositeSimplexToBoundary g).map ≫
          (scalingEqualityIso
            (generatedPushoutScaling
              (standardTypeAEndpointAmbientSourceScaling g)
              (standardTypeAEndpointOppositeSimplexScaling g)
              (standardTypeAEndpointAmbientSourceToBoundary g).map
              (standardTypeAEndpointOppositeSimplexToBoundary g).map)
            (standardTypeABoundaryPrismScaling.{u} g)
            hScaling).hom.map =
        (standardTypeAEndpointOppositeSimplexToBoundary g).map
    rw [scalingEqualityIso_hom_map]
    exact Category.comp_id _

theorem standardTypeAEndpointAmbientSourceToBoundary_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointAmbientSourceToBoundary g) := by
  unfold standardABCRawCellularStep
  exact
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts_mk
      (standardTypeAEndpointOpposite_scaled_isPushout g)
      (standardTypeAEndpointOppositeCellHom_mem_coproductsABC g)

/-! ## Return to the actual v1.55 source -/

noncomputable def standardTypeAEndpointToBoundaryPrismArrowIsoAmbient
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Arrow.mk (standardTypeAEndpointToBoundaryPrism g) ≅
      Arrow.mk (standardTypeAEndpointAmbientSourceToBoundary g) := by
  refine Arrow.isoMk
    (standardTypeAEndpointGeneratedSourceIsoAmbient g)
    (Iso.refl _) ?_
  apply ScaledSSet.ScaledMap.ext
  change
    (standardTypeAEndpointGeneratedSourceIsoAmbient g).hom.map ≫
        (standardTypeAEndpointAmbientSourceToBoundary g).map =
      (standardTypeAEndpointToBoundaryPrism g).map
  unfold standardTypeAEndpointGeneratedSourceIsoAmbient
  rw [scalingEqualityIso_hom_map, Category.id_comp]
  rfl

local instance standardTypeAEndpointRawStep_respectsIso :
    (standardABCRawCellularStep :
      MorphismProperty (ScaledSSet.{u})).RespectsIso := by
  unfold standardABCRawCellularStep
  infer_instance

theorem standardTypeAEndpointToBoundaryPrism_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointToBoundaryPrism g) := by
  exact
    ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
      (standardTypeAEndpointToBoundaryPrismArrowIsoAmbient g)).2
      (standardTypeAEndpointAmbientSourceToBoundary_mem_rawCellular g)

theorem standardTypeAEndpointToBoundaryPrism_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointToBoundaryPrism g) := by
  unfold standardABCStrongCellularClosure
  exact
    MorphismProperty.le_transfiniteCompositions.{u}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAEndpointToBoundaryPrism_mem_rawCellular g)

/-! ## Prepend the endpoint A-step to the v1.76 alternating sequence -/

def standardTypeAEndpointFullObj
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ℕ → ScaledSSet.{u}
  | 0 => standardTypeAEndpointGeneratedPushoutSource g
  | n + 1 => standardTypeABoundaryPrismAlternatingObj g n

noncomputable def standardTypeAEndpointFullStep
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (n : ℕ) →
      standardTypeABoundaryPrismScaledCatHom
        (standardTypeAEndpointFullObj g n)
        (standardTypeAEndpointFullObj g (n + 1))
  | 0 =>
      standardTypeAEndpointToBoundaryPrism g ≫
        (standardTypeABoundaryPrismAlternatingBotIso g).inv
  | n + 1 => standardTypeABoundaryPrismAlternatingStep g n

theorem standardTypeAEndpointFullStep_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointFullStep g n) := by
  cases n with
  | zero =>
      change
        (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
          (standardTypeAEndpointToBoundaryPrism g ≫
            (standardTypeABoundaryPrismAlternatingBotIso g).inv)
      apply MorphismProperty.RespectsIso.postcomp
      exact standardTypeAEndpointToBoundaryPrism_mem_rawCellular g
  | succ n =>
      change
        (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
          (standardTypeABoundaryPrismAlternatingStep g n)
      exact standardTypeABoundaryPrismAlternatingStep_mem_rawCellular g n

@[reducible]
noncomputable def standardTypeAEndpointFullFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} :=
  Functor.ofSequence (standardTypeAEndpointFullStep g)

@[simp]
theorem standardTypeAEndpointFullFunctor_map_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullFunctor g).map
        (homOfLE (Nat.le_add_right n 1)) =
      standardTypeAEndpointFullStep g n := by
  unfold standardTypeAEndpointFullFunctor
  exact
    Functor.ofSequence_map_homOfLE_succ
      (C := ScaledSSet.{u})
      (X := standardTypeAEndpointFullObj g)
      (standardTypeAEndpointFullStep g) n

noncomputable def standardTypeAEndpointFullToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (n : ℕ) →
      standardTypeABoundaryPrismScaledCatHom
        (standardTypeAEndpointFullObj g n)
        (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
  | 0 => standardTypeAEndpointScaledLeibnizPushoutProductHom g
  | n + 1 => standardTypeABoundaryPrismAlternatingToCylinder g n

theorem standardTypeAEndpointFullStep_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeAEndpointFullStep g n ≫
        standardTypeAEndpointFullToCylinder g (n + 1) =
      standardTypeAEndpointFullToCylinder g n := by
  cases n with
  | zero =>
      change
        (standardTypeAEndpointToBoundaryPrism g ≫
            (standardTypeABoundaryPrismAlternatingBotIso g).inv) ≫
          standardTypeABoundaryPrismAlternatingToCylinder g 0 =
        standardTypeAEndpointScaledLeibnizPushoutProductHom g
      rw [Category.assoc]
      have htail := (standardTypeABoundaryPrismRawTransfiniteComposition g).fac
      change
        (standardTypeABoundaryPrismAlternatingBotIso g).inv ≫
            standardTypeABoundaryPrismAlternatingToCylinder g 0 =
          standardTypeABoundaryPrismToCylinder g at htail
      rw [htail]
      exact standardTypeAEndpointLeibniz_factor_boundaryPrism g
  | succ n =>
      change
        standardTypeABoundaryPrismAlternatingStep g n ≫
            standardTypeABoundaryPrismAlternatingToCylinder g (n + 1) =
          standardTypeABoundaryPrismAlternatingToCylinder g n
      exact standardTypeABoundaryPrismAlternatingStep_toCylinder g n

theorem standardTypeAEndpointFullToCylinder_succ_naturality
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullFunctor g).map
          (homOfLE (Nat.le_add_right n 1)) ≫
        standardTypeAEndpointFullToCylinder g (n + 1) =
      standardTypeAEndpointFullToCylinder g n ≫
        ((Functor.const ℕ).obj
          (scaledSimplexCylinder (standardTypeASimplexScaling g.i))).map
            (homOfLE (Nat.le_add_right n 1)) := by
  rw [standardTypeAEndpointFullFunctor_map_succ,
    Functor.const_obj_map, Category.comp_id]
  exact standardTypeAEndpointFullStep_toCylinder g n

@[reducible]
noncomputable def standardTypeAEndpointFullCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeAEndpointFullFunctor g) :=
  Cocone.mk
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    (NatTrans.ofSequence
      (F := standardTypeAEndpointFullFunctor g)
      (G := (Functor.const ℕ).obj
        (scaledSimplexCylinder (standardTypeASimplexScaling g.i)))
      (standardTypeAEndpointFullToCylinder g)
      (standardTypeAEndpointFullToCylinder_succ_naturality g))

theorem standardTypeAEndpointFullCocone_step
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor g))
    (n : ℕ) :
    standardTypeAEndpointFullStep g n ≫ s.ι.app (n + 1) =
      s.ι.app n := by
  have h := s.w (homOfLE (Nat.le_add_right n 1))
  change
    (standardTypeAEndpointFullFunctor g).map
          (homOfLE (Nat.le_add_right n 1)) ≫ s.ι.app (n + 1) =
      s.ι.app n ≫ 𝟙 _ at h
  rw [standardTypeAEndpointFullFunctor_map_succ] at h
  exact h.trans (Category.comp_id _)

@[reducible]
noncomputable def standardTypeAEndpointFullTailCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor g)) :
    Cocone (standardTypeABoundaryPrismAlternatingFunctor g) :=
  Cocone.mk s.pt
    (NatTrans.ofSequence
      (F := standardTypeABoundaryPrismAlternatingFunctor g)
      (G := (Functor.const ℕ).obj s.pt)
      (fun n => s.ι.app (n + 1))
      (fun n => by
        rw [standardTypeABoundaryPrismAlternatingFunctor_map_succ,
          Functor.const_obj_map, Category.comp_id]
        simpa [standardTypeAEndpointFullStep] using
          standardTypeAEndpointFullCocone_step g s (n + 1)))

noncomputable def standardTypeAEndpointFullCoconeIsColimit
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsColimit (standardTypeAEndpointFullCocone g) where
  desc s :=
    (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
      (standardTypeAEndpointFullTailCocone g s)
  fac s j := by
    cases j with
    | zero =>
        have htail :=
          (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).fac
            (standardTypeAEndpointFullTailCocone g s) 0
        have hstep := standardTypeAEndpointFullCocone_step g s 0
        change
          standardTypeAEndpointFullToCylinder g 0 ≫
              (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
                (standardTypeAEndpointFullTailCocone g s) =
            s.ι.app 0
        calc
          standardTypeAEndpointFullToCylinder g 0 ≫
                (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
                  (standardTypeAEndpointFullTailCocone g s) =
              (standardTypeAEndpointFullStep g 0 ≫
                  standardTypeAEndpointFullToCylinder g 1) ≫
                (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
                  (standardTypeAEndpointFullTailCocone g s) := by
                    rw [standardTypeAEndpointFullStep_toCylinder]
          _ = standardTypeAEndpointFullStep g 0 ≫
                (standardTypeAEndpointFullToCylinder g 1 ≫
                  (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
                    (standardTypeAEndpointFullTailCocone g s)) := by
                      simp only [Category.assoc]
          _ = standardTypeAEndpointFullStep g 0 ≫ s.ι.app 1 := by
                change
                  standardTypeABoundaryPrismAlternatingToCylinder g 0 ≫
                      (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
                        (standardTypeAEndpointFullTailCocone g s) =
                    s.ι.app 1 at htail
                rw [htail]
          _ = s.ι.app 0 := hstep
    | succ n =>
        have htail :=
          (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).fac
            (standardTypeAEndpointFullTailCocone g s) n
        change
          standardTypeABoundaryPrismAlternatingToCylinder g n ≫
              (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
                (standardTypeAEndpointFullTailCocone g s) =
            s.ι.app (n + 1)
        exact htail
  uniq s m hm := by
    apply (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).hom_ext
    intro n
    have hmn := hm (n + 1)
    have hdesc :=
      (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).fac
        (standardTypeAEndpointFullTailCocone g s) n
    change
      standardTypeABoundaryPrismAlternatingToCylinder g n ≫ m =
        standardTypeABoundaryPrismAlternatingToCylinder g n ≫
          (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
            (standardTypeAEndpointFullTailCocone g s)
    change
      standardTypeABoundaryPrismAlternatingToCylinder g n ≫ m =
        s.ι.app (n + 1) at hmn
    change
      standardTypeABoundaryPrismAlternatingToCylinder g n ≫
          (standardTypeABoundaryPrismAlternatingCoconeIsColimit g).desc
            (standardTypeAEndpointFullTailCocone g s) =
        s.ι.app (n + 1) at hdesc
    exact hmn.trans hdesc.symm

noncomputable def standardTypeAEndpointRawTransfiniteComposition
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty.TransfiniteCompositionOfShape
      (C := ScaledSSet.{u})
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      ℕ (standardTypeAEndpointScaledLeibnizPushoutProductHom g) where
  F := standardTypeAEndpointFullFunctor g
  isoBot := Iso.refl (standardTypeAEndpointGeneratedPushoutSource g)
  incl := (standardTypeAEndpointFullCocone g).ι
  isColimit := standardTypeAEndpointFullCoconeIsColimit g
  fac := by
    change
      (𝟙 (standardTypeAEndpointGeneratedPushoutSource g)) ≫
          standardTypeAEndpointFullToCylinder g 0 =
        standardTypeAEndpointScaledLeibnizPushoutProductHom g
    simp [standardTypeAEndpointFullToCylinder]
  map_mem j _ := by
    have hhom :
        (homOfLE (Order.le_succ j) : j ⟶ j + 1) =
          homOfLE (Nat.le_add_right j 1) :=
      Subsingleton.elim _ _
    rw [hhom, standardTypeAEndpointFullFunctor_map_succ]
    exact standardTypeAEndpointFullStep_mem_rawCellular g j

theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointScaledLeibnizPushoutProductHom g) := by
  unfold standardABCStrongCellularClosure
  have h :=
    (standardTypeAEndpointRawTransfiniteComposition g).ofOrderIso
      (orderIsoShrink.{u} ℕ).symm
  exact
    (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
      (W := (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})))
      (Shrink.{u} ℕ)) _ h.mem

theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointScaledLeibnizPushoutProductHom g) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_strongCellular g)

def standardABCTypeAEndpointLeibnizCellularCertificateConstructed :
    StandardABCTypeAEndpointLeibnizCellularCertificate.{u} where
  generators_le_cellular := by
    intro A B f hf
    dsimp [standardTypeAScaledLeibnizPushoutProductGenerators] at hf
    cases hf with
    | mk g =>
        exact standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_cellular g

theorem standardABCTypeAEndpointLeibnizStability_proved :
    StandardABCTypeAEndpointLeibnizStability.{u} :=
  standardABCTypeAEndpointLeibnizCellularCertificateConstructed.toLeibnizStability

theorem standardABCTypeAEndpointLeibnizLifting_proved :
    StandardABCTypeAEndpointLeibnizLifting.{u} :=
  standardABCTypeAEndpointLeibnizCellularCertificateConstructed.lifting

end

end KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
