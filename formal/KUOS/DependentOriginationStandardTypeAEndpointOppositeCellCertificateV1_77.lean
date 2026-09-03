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

/-!
# The missing opposite endpoint A-cell and the final standard A/B/C certificate v1.77

The boundary-prism inclusion is already one raw A/B transfinite composition by
v1.76.  Here the remaining endpoint map is exhibited as the pushout of the
literal standard type-(A) generator after transporting the opposite-endpoint
product square through explicit scaled isomorphisms.
-/

/-! ## The least-generated endpoint source is the ambient pullback source -/

theorem standardTypeAEndpointInducedProductPullbackScaling_le_generated
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScalingLE
      (standardTypeAEndpointInducedProductPullbackScaling g)
      (standardTypeAEndpointGeneratedPushoutScaling g) := by
  intro t ht
  have htmem :
      t.val ∈
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint)).obj (op ⦋2⦌) :=
    t.property
  rw [SSet.Subcomplex.mem_unionProd_iff] at htmem
  rcases htmem with hendpoint | hhorn
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
  rw [cartesianProductScaling_interval_eq_simplexCylinderScaling
    (standardTypeASimplexScaling g.i)
    (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u}))]
  rfl

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
  rfl

theorem intervalEndpoint_one_eq_face_zero :
    intervalEndpoint (1 : Fin 2) =
      SSet.stdSimplex.face ({(0 : Fin 2)}ᶜ) := by
  unfold intervalEndpoint
  rw [SSet.stdSimplex.face_singleton_compl]
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
  · rw [intervalEndpoint_zero_eq_face_one,
      intervalEndpoint_one_eq_face_zero,
      SSet.stdSimplex.face_inter_face]
    simp
  · rw [intervalEndpoint_one_eq_face_zero,
      intervalEndpoint_zero_eq_face_one,
      SSet.stdSimplex.face_inter_face]
    simp

theorem intervalBoundary_eq_endpoint_zero_sup_one :
    (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
      intervalEndpoint 0 ⊔ intervalEndpoint 1 := by
  rw [SSet.boundary_eq_iSup]
  apply le_antisymm
  · refine iSup_le ?_
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
  · simpa using intervalBoundary_eq_endpoint_zero_sup_one
  · simpa [sup_comm] using intervalBoundary_eq_endpoint_zero_sup_one

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
        rw [← NatTrans.comp_app_apply, e.hom_inv_id]
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
  ext d t
  apply Subtype.ext
  rfl

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
    have hmem :
        t.val ∈
          (((SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint)) ⊔
            standardTypeAEndpointOppositeSimplexSubcomplex g).obj
              (op ⦋2⦌) := by
      rw [(standardTypeAEndpointOppositeCarrierBicartSq g).sup_eq]
      exact t.property
    change
      t.val ∈
          ((SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint)).obj
            (op ⦋2⦌) ∨
        t.val ∈
          (standardTypeAEndpointOppositeSimplexSubcomplex g).obj
            (op ⦋2⦌) at hmem
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
      rw [hxmap]
      exact ht
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
  have h := generatedPushout_isPushout
    (standardTypeAEndpointOppositeCornerToAmbientSource g)
    (standardTypeAEndpointOppositeCellHom g)
    (standardTypeAEndpointAmbientSourceToBoundary g).map
    (standardTypeAEndpointOppositeSimplexToBoundary g).map
    (standardTypeAEndpointOppositeCarrier_isPushout g)
  rw [standardTypeAEndpointOppositeGeneratedScaling_eq_boundary g] at h
  simpa [generatedPushoutInl, generatedPushoutInr, generatedPushoutTarget,
    standardTypeAEndpointAmbientSourceToBoundary,
    standardTypeAEndpointOppositeSimplexToBoundary] using h

/-! ## Transport the scaled square so its top edge is the literal A generator -/

def standardTypeAEndpointLiteralHornToAmbientSource
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAScaledHorn
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) ⟶
      standardTypeAEndpointAmbientSource g :=
  (standardTypeAEndpointOppositeCornerIso g).inv ≫
    standardTypeAEndpointOppositeCornerToAmbientSource g

def standardTypeAEndpointLiteralSimplexToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAScaledSimplex
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) ⟶
      standardTypeABoundaryPrism g :=
  (standardTypeAEndpointOppositeSimplexIso g).inv ≫
    standardTypeAEndpointOppositeSimplexToBoundary g

noncomputable def standardTypeAEndpointLiteral_scaled_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (standardTypeAEndpointLiteralHornToAmbientSource g)
      (standardTypeAScaledHornGeneratorHom
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g))
      (standardTypeAEndpointAmbientSourceToBoundary g)
      (standardTypeAEndpointLiteralSimplexToBoundary g) := by
  apply (standardTypeAEndpointOpposite_scaled_isPushout g).of_iso
    (standardTypeAEndpointOppositeCornerIso g)
    (Iso.refl _)
    (standardTypeAEndpointOppositeSimplexIso g)
    (Iso.refl _)
  · simp [standardTypeAEndpointLiteralHornToAmbientSource, Category.assoc]
  · exact (standardTypeAEndpointOppositeCellArrowIso g).hom.w
  · simp
  · simp [standardTypeAEndpointLiteralSimplexToBoundary, Category.assoc]

local instance standardTypeAEndpointRawStep_respectsIso :
    (standardABCRawCellularStep :
      MorphismProperty (ScaledSSet.{u})).RespectsIso := by
  unfold standardABCRawCellularStep
  infer_instance

theorem standardTypeAEndpointAmbientSourceToBoundary_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointAmbientSourceToBoundary g) := by
  let P : MorphismProperty (ScaledSSet.{u}) :=
    MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  have hA :
      P (standardTypeAScaledHornGeneratorHom
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAGenerator_mem_ABC
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g))
  change P.pushouts (standardTypeAEndpointAmbientSourceToBoundary g)
  exact P.pushouts_mk
    (standardTypeAEndpointLiteral_scaled_isPushout g) hA

/-! ## Return to the actual v1.55 source -/

noncomputable def standardTypeAEndpointToBoundaryPrismArrowIsoAmbient
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Arrow.mk (standardTypeAEndpointToBoundaryPrism g) ≅
      Arrow.mk (standardTypeAEndpointAmbientSourceToBoundary g) := by
  refine Arrow.isoMk
    (standardTypeAEndpointGeneratedSourceIsoAmbient g)
    (Iso.refl _) ?_
  apply ScaledSSet.ScaledMap.ext
  ext d t
  rfl

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

/-- The next theorem will be replaced by the explicit prefixed transfinite
sequence once the literal opposite-endpoint pushout above is validated. -/
theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointScaledLeibnizPushoutProductHom g) := by
  have hcomp :=
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})).comp_mem
      (standardTypeAEndpointToBoundaryPrism g)
      (standardTypeABoundaryPrismToCylinder g)
      (standardTypeAEndpointToBoundaryPrism_mem_strongCellular g)
      (standardTypeABoundaryPrismToCylinder_mem_strongCellular g)
  simpa only [standardTypeAEndpointLeibniz_factor_boundaryPrism] using hcomp

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
