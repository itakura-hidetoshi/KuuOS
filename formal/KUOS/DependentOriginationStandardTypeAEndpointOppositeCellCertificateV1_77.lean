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
# Opposite endpoint A-cell and full endpoint transfinite certificate v1.77

The boundary-prism inclusion is one raw A/B transfinite composition by v1.76.
Here the missing opposite endpoint is attached by one literal standard type-A
cell.  The whole endpoint map is then represented by one natural-number
transfinite composition obtained by prefixing that A-step to the v1.76
alternating sequence.  No binary-composition closure of arbitrary transfinite
compositions is assumed.
-/

/-! ## The generated endpoint source equals the ambient cylinder pullback -/

theorem standardTypeAEndpointInducedProductPullbackScaling_le_generated
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScalingLE
      (standardTypeAEndpointInducedProductPullbackScaling.{u} g)
      (standardTypeAEndpointGeneratedPushoutScaling.{u} g) := by
  intro t ht
  rcases
      (SSet.Subcomplex.mem_unionProd_iff
        (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint) t.val).mp t.property with
    hendpoint | hhorn
  · let x :
        ((Δ[g.n] : SSet.{u}) ⊗
          (intervalEndpoint.{u} g.endpoint : SSet.{u})).obj (op ⦋2⦌) :=
      ⟨t.val.1, ⟨t.val.2, hendpoint⟩⟩
    have hxmap :
        (SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint)).app
            (op ⦋2⦌) x = t := by
      apply Subtype.ext
      rfl
    refine Or.inr (Or.inr (Or.inl ⟨x, ?_, hxmap⟩))
    change
      (standardTypeAEndpointInducedProductPullbackScaling.{u} g).thin
        ((SSet.Subcomplex.unionProd.ι₁
          (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint)).app
            (op ⦋2⦌) x)
    rw [hxmap]
    exact ht
  · let x :
        ((SSet.horn g.n g.i : SSet.{u}) ⊗ Δ[1]).obj (op ⦋2⦌) :=
      ⟨⟨t.val.1, hhorn⟩, t.val.2⟩
    have hxmap :
        (SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint)).app
            (op ⦋2⦌) x = t := by
      apply Subtype.ext
      rfl
    refine Or.inr (Or.inr (Or.inr ⟨x, ?_, hxmap⟩))
    change
      (standardTypeAEndpointInducedProductPullbackScaling.{u} g).thin
        ((SSet.Subcomplex.unionProd.ι₂
          (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint)).app
            (op ⦋2⦌) x)
    rw [hxmap]
    exact ht

theorem standardTypeAEndpointGeneratedPushoutScaling_eq_induced
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutScaling.{u} g =
      standardTypeAEndpointInducedProductPullbackScaling.{u} g :=
  scaling_eq_of_le_antisymm
    (standardTypeAEndpointGeneratedPushoutScaling_le_induced.{u} g)
    (standardTypeAEndpointInducedProductPullbackScaling_le_generated.{u} g)

def standardTypeAEndpointAmbientSourceScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint.{u} g.endpoint) : SSet.{u}) :=
  pullbackScaling
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling
    ((SSet.horn g.n g.i).unionProd
      (intervalEndpoint.{u} g.endpoint)).ι

theorem standardTypeAEndpointGeneratedPushoutScaling_eq_ambient
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutScaling.{u} g =
      standardTypeAEndpointAmbientSourceScaling.{u} g := by
  rw [standardTypeAEndpointGeneratedPushoutScaling_eq_induced.{u} g]
  unfold standardTypeAEndpointInducedProductPullbackScaling
  unfold standardTypeAEndpointCylinderProductScaling
  unfold standardTypeAEndpointAmbientSourceScaling
  unfold scaledSimplexCylinder
  change
    pullbackScaling
        (cartesianProductScaling
          (standardTypeASimplexScaling g.i)
          (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u})))
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint.{u} g.endpoint)).ι =
      pullbackScaling
        (simplexCylinderScaling (standardTypeASimplexScaling g.i))
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint.{u} g.endpoint)).ι
  exact congrArg
    (fun s => pullbackScaling s
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint.{u} g.endpoint)).ι)
    (cartesianProductScaling_interval_eq_simplexCylinderScaling
      (standardTypeASimplexScaling g.i)
      (ScaledSimplicialSet.maximal (Δ[1] : SSet.{u})))

def standardTypeAEndpointAmbientSource
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((SSet.horn g.n g.i).unionProd
      (intervalEndpoint.{u} g.endpoint) : SSet.{u})
    (standardTypeAEndpointAmbientSourceScaling.{u} g)

noncomputable def standardTypeAEndpointGeneratedSourceIsoAmbient
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutSource.{u} g ≅
      standardTypeAEndpointAmbientSource.{u} g :=
  scalingEqualityIso
    (standardTypeAEndpointGeneratedPushoutScaling.{u} g)
    (standardTypeAEndpointAmbientSourceScaling.{u} g)
    (standardTypeAEndpointGeneratedPushoutScaling_eq_ambient.{u} g)

/-! ## The interval boundary is the disjoint union of its endpoints -/

theorem intervalEndpoint_zero_eq_face_one :
    intervalEndpoint.{u} (0 : Fin 2) =
      SSet.stdSimplex.face ({(1 : Fin 2)}ᶜ) := by
  unfold intervalEndpoint
  rw [SSet.stdSimplex.face_singleton_compl]
  apply congrArg SSet.Subcomplex.ofSimplex
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k
  rfl

theorem intervalEndpoint_one_eq_face_zero :
    intervalEndpoint.{u} (1 : Fin 2) =
      SSet.stdSimplex.face ({(0 : Fin 2)}ᶜ) := by
  unfold intervalEndpoint
  rw [SSet.stdSimplex.face_singleton_compl]
  apply congrArg SSet.Subcomplex.ofSimplex
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k
  rfl

theorem intervalEndpoint_eq_face_rev (ε : Fin 2) :
    intervalEndpoint.{u} ε =
      SSet.stdSimplex.face ({ε.rev}ᶜ) := by
  fin_cases ε
  · simpa using intervalEndpoint_zero_eq_face_one.{u}
  · simpa using intervalEndpoint_one_eq_face_zero.{u}

theorem intervalEndpoint_inf_rev_eq_bot (ε : Fin 2) :
    intervalEndpoint.{u} ε ⊓ intervalEndpoint.{u} ε.rev =
      (⊥ : (Δ[1] : SSet.{u}).Subcomplex) := by
  fin_cases ε
  · change
      intervalEndpoint.{u} (0 : Fin 2) ⊓
          intervalEndpoint.{u} (1 : Fin 2) = ⊥
    rw [intervalEndpoint_zero_eq_face_one.{u},
      intervalEndpoint_one_eq_face_zero.{u},
      SSet.stdSimplex.face_inter_face]
    have h :
        ({(1 : Fin 2)}ᶜ ⊓ {(0 : Fin 2)}ᶜ : Finset (Fin 2)) = ∅ := by
      ext i
      fin_cases i <;> simp
    simpa [h]
  · change
      intervalEndpoint.{u} (1 : Fin 2) ⊓
          intervalEndpoint.{u} (0 : Fin 2) = ⊥
    rw [intervalEndpoint_one_eq_face_zero.{u},
      intervalEndpoint_zero_eq_face_one.{u},
      SSet.stdSimplex.face_inter_face]
    have h :
        ({(0 : Fin 2)}ᶜ ⊓ {(1 : Fin 2)}ᶜ : Finset (Fin 2)) = ∅ := by
      ext i
      fin_cases i <;> simp
    simpa [h]

theorem intervalBoundary_eq_endpoint_zero_sup_one :
    (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
      intervalEndpoint.{u} 0 ⊔ intervalEndpoint.{u} 1 := by
  apply le_antisymm
  · rw [SSet.boundary_eq_iSup]
    refine iSup_le ?_
    intro i
    fin_cases i
    · change
        SSet.stdSimplex.face ({(0 : Fin 2)}ᶜ) ≤
          intervalEndpoint.{u} 0 ⊔ intervalEndpoint.{u} 1
      rw [← intervalEndpoint_one_eq_face_zero.{u}]
      exact le_sup_right
    · change
        SSet.stdSimplex.face ({(1 : Fin 2)}ᶜ) ≤
          intervalEndpoint.{u} 0 ⊔ intervalEndpoint.{u} 1
      rw [← intervalEndpoint_zero_eq_face_one.{u}]
      exact le_sup_left
  · exact sup_le
      (intervalEndpoint_le_boundary.{u} 0)
      (intervalEndpoint_le_boundary.{u} 1)

theorem intervalBoundary_eq_endpoint_sup_rev (ε : Fin 2) :
    (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
      intervalEndpoint.{u} ε ⊔ intervalEndpoint.{u} ε.rev := by
  fin_cases ε
  · change
      (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
        intervalEndpoint.{u} (0 : Fin 2) ⊔
          intervalEndpoint.{u} (1 : Fin 2)
    exact intervalBoundary_eq_endpoint_zero_sup_one.{u}
  · change
      (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) =
        intervalEndpoint.{u} (1 : Fin 2) ⊔
          intervalEndpoint.{u} (0 : Fin 2)
    simpa [sup_comm] using intervalBoundary_eq_endpoint_zero_sup_one.{u}

/-! ## The ordinary opposite-endpoint pushout square -/

def standardTypeAEndpointOppositeCornerSubcomplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex :=
  (SSet.horn g.n g.i).prod (intervalEndpoint.{u} g.endpoint.rev)

def standardTypeAEndpointOppositeSimplexSubcomplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex :=
  (⊤ : (Δ[g.n] : SSet.{u}).Subcomplex).prod
    (intervalEndpoint.{u} g.endpoint.rev)

def standardTypeAEndpointOppositeCarrierBicartSq
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    SSet.Subcomplex.BicartSq
      (standardTypeAEndpointOppositeCornerSubcomplex.{u} g)
      (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g)
      ((SSet.horn g.n g.i).unionProd (intervalEndpoint.{u} g.endpoint))
      (standardTypeABoundaryPrismSubcomplex.{u} g) where
  sup_eq := by
    rw [standardTypeABoundaryPrismSubcomplex,
      intervalBoundary_eq_endpoint_sup_rev.{u} g.endpoint]
    ext d z
    rcases z with ⟨x, y⟩
    have hopp :
        (x, y) ∈
            (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g).obj d ↔
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d := by
      simp only [standardTypeAEndpointOppositeSimplexSubcomplex,
        SSet.Subcomplex.prod_obj,
        CategoryTheory.Subfunctor.top_obj, Set.top_eq_univ]
      change
        (x ∈ Set.univ ∧
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d) ↔
        y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d
      simp only [Set.mem_univ, true_and]
    have hsource :
        (x, y) ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint.{u} g.endpoint)).obj d ↔
          y ∈ (intervalEndpoint.{u} g.endpoint).obj d ∨
            x ∈ (SSet.horn g.n g.i).obj d :=
      SSet.Subcomplex.mem_unionProd_iff
        (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint) (x, y)
    have hendpoint :
        y ∈
            (intervalEndpoint.{u} g.endpoint ⊔
              intervalEndpoint.{u} g.endpoint.rev).obj d ↔
          y ∈ (intervalEndpoint.{u} g.endpoint).obj d ∨
            y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d := by
      rw [CategoryTheory.Subfunctor.max_obj, Set.mem_union]
    have htarget :
        (x, y) ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint.{u} g.endpoint ⊔
                intervalEndpoint.{u} g.endpoint.rev)).obj d ↔
          (y ∈ (intervalEndpoint.{u} g.endpoint).obj d ∨
            y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d) ∨
            x ∈ (SSet.horn g.n g.i).obj d := by
      rw [SSet.Subcomplex.mem_unionProd_iff, hendpoint]
    rw [CategoryTheory.Subfunctor.max_obj, Set.mem_union,
      hopp, hsource, htarget]
    tauto
  inf_eq := by
    ext d z
    rcases z with ⟨x, y⟩
    have hdis :
        ¬ (y ∈ (intervalEndpoint.{u} g.endpoint).obj d ∧
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d) := by
      intro h
      have hm :
          y ∈ (intervalEndpoint.{u} g.endpoint ⊓
            intervalEndpoint.{u} g.endpoint.rev).obj d := by
        rw [CategoryTheory.Subfunctor.min_obj]
        exact h
      rw [intervalEndpoint_inf_rev_eq_bot.{u} g.endpoint] at hm
      simpa using hm
    have hopp :
        (x, y) ∈
            (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g).obj d ↔
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d := by
      simp only [standardTypeAEndpointOppositeSimplexSubcomplex,
        SSet.Subcomplex.prod_obj,
        CategoryTheory.Subfunctor.top_obj, Set.top_eq_univ]
      change
        (x ∈ Set.univ ∧
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d) ↔
        y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d
      simp only [Set.mem_univ, true_and]
    have hsource :
        (x, y) ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint.{u} g.endpoint)).obj d ↔
          y ∈ (intervalEndpoint.{u} g.endpoint).obj d ∨
            x ∈ (SSet.horn g.n g.i).obj d :=
      SSet.Subcomplex.mem_unionProd_iff
        (SSet.horn g.n g.i) (intervalEndpoint.{u} g.endpoint) (x, y)
    have hcorner :
        (x, y) ∈
            (standardTypeAEndpointOppositeCornerSubcomplex.{u} g).obj d ↔
          x ∈ (SSet.horn g.n g.i).obj d ∧
            y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d := by
      simp only [standardTypeAEndpointOppositeCornerSubcomplex,
        SSet.Subcomplex.prod_obj]
      change
        (x ∈ (SSet.horn g.n g.i).obj d ∧
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d) ↔
        x ∈ (SSet.horn g.n g.i).obj d ∧
          y ∈ (intervalEndpoint.{u} g.endpoint.rev).obj d
      rfl
    rw [CategoryTheory.Subfunctor.min_obj, Set.mem_inter_iff,
      hopp, hsource, hcorner]
    tauto

noncomputable def standardTypeAEndpointOppositeCarrier_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₃)
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₂)
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₃₄)
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₂₄) :=
  (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).isPushout.flip

/-! ## Product with an endpoint is the literal standard A cell -/

noncomputable def intervalEndpointIsoStdZero (ε : Fin 2) :
    (Δ[0] : SSet.{u}) ≅ (intervalEndpoint.{u} ε : SSet.{u}) :=
  SSet.stdSimplex.faceSingletonComplIso.{u} ε.rev ≪≫
    SSet.Subcomplex.eqToIso (intervalEndpoint_eq_face_rev.{u} ε).symm

noncomputable def intervalEndpointIsTerminal (ε : Fin 2) :
    IsTerminal (intervalEndpoint.{u} ε : SSet.{u}) :=
  IsTerminal.ofIso SSet.stdSimplex.isTerminalObj₀
    (intervalEndpointIsoStdZero.{u} ε)

noncomputable def subcomplexProdIntervalEndpointIso
    {X : SSet.{u}}
    (A : X.Subcomplex)
    (ε : Fin 2) :
    (A.prod (intervalEndpoint.{u} ε) : SSet.{u}) ≅ (A : SSet.{u}) :=
  SSet.Subcomplex.prodIso A (intervalEndpoint.{u} ε) ≪≫
    whiskerLeftIso (A : SSet.{u})
      ((intervalEndpointIsTerminal.{u} ε).uniqueUpToIso
        CartesianMonoidalCategory.isTerminalTensorUnit) ≪≫
    ρ_ (A : SSet.{u})

noncomputable def standardTypeAEndpointOppositeCornerCarrierIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointOppositeCornerSubcomplex.{u} g : SSet.{u}) ≅
      (SSet.horn g.n g.i : SSet.{u}) :=
  subcomplexProdIntervalEndpointIso.{u}
    (SSet.horn g.n g.i) g.endpoint.rev

noncomputable def standardTypeAEndpointOppositeSimplexCarrierIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g : SSet.{u}) ≅
      (Δ[g.n] : SSet.{u}) :=
  subcomplexProdIntervalEndpointIso.{u}
      (⊤ : (Δ[g.n] : SSet.{u}).Subcomplex) g.endpoint.rev ≪≫
    SSet.Subcomplex.topIso (Δ[g.n] : SSet.{u})

@[simp]
theorem standardTypeAEndpointOppositeCornerCarrierIso_hom_app_val
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (d : SimplexCategoryᵒᵖ)
    (z : (standardTypeAEndpointOppositeCornerSubcomplex.{u} g : SSet.{u}).obj d) :
    ((standardTypeAEndpointOppositeCornerCarrierIso.{u} g).hom.app d z).val =
      z.val.1 := by
  simp [standardTypeAEndpointOppositeCornerCarrierIso,
    subcomplexProdIntervalEndpointIso]
  rfl

@[simp]
theorem standardTypeAEndpointOppositeSimplexCarrierIso_hom_app
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (d : SimplexCategoryᵒᵖ)
    (z : (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g : SSet.{u}).obj d) :
    (standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom.app d z =
      z.val.1 := by
  simp [standardTypeAEndpointOppositeSimplexCarrierIso,
    subcomplexProdIntervalEndpointIso]
  rfl

noncomputable def pullbackScalingIso
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
      (standardTypeAEndpointOppositeCornerSubcomplex.{u} g : SSet.{u}) :=
  pullbackScaling (standardTypeAHornScaling g.i)
    (standardTypeAEndpointOppositeCornerCarrierIso.{u} g).hom

def standardTypeAEndpointOppositeSimplexScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g : SSet.{u}) :=
  pullbackScaling (standardTypeASimplexScaling g.i)
    (standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom

def standardTypeAEndpointOppositeCorner
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    (standardTypeAEndpointOppositeCornerSubcomplex.{u} g : SSet.{u})
    (standardTypeAEndpointOppositeCornerScaling.{u} g)

def standardTypeAEndpointOppositeSimplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g : SSet.{u})
    (standardTypeAEndpointOppositeSimplexScaling.{u} g)

noncomputable def standardTypeAEndpointOppositeCornerIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeCorner.{u} g ≅
      standardTypeAScaledHorn
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) :=
  pullbackScalingIso.{u}
    (standardTypeAEndpointOppositeCornerCarrierIso.{u} g)
    (standardTypeAHornScaling g.i)

noncomputable def standardTypeAEndpointOppositeSimplexIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeSimplex.{u} g ≅
      standardTypeAScaledSimplex
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) :=
  pullbackScalingIso.{u}
    (standardTypeAEndpointOppositeSimplexCarrierIso.{u} g)
    (standardTypeASimplexScaling g.i)

/-! ## Lift the carrier square to a scaled pushout -/

def standardTypeAEndpointOppositeCellHom
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeCorner.{u} g ⟶
      standardTypeAEndpointOppositeSimplex.{u} g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₂
  scaled := by
    intro t ht
    change (standardTypeAEndpointOppositeCornerScaling.{u} g).thin t at ht
    unfold standardTypeAEndpointOppositeCornerScaling at ht
    have hA := standardTypeAHornInclusion_scaled g.i
      ((standardTypeAEndpointOppositeCornerCarrierIso.{u} g).hom.app
        (op ⦋2⦌) t) ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom.app
          (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₂).app
              (op ⦋2⦌) t))
    simpa using hA

noncomputable def standardTypeAEndpointOppositeCellArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Arrow.mk (standardTypeAEndpointOppositeCellHom.{u} g) ≅
      Arrow.mk (standardTypeAScaledHornGeneratorHom
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)) := by
  refine Arrow.isoMk
    (standardTypeAEndpointOppositeCornerIso.{u} g)
    (standardTypeAEndpointOppositeSimplexIso.{u} g) ?_
  apply ScaledSSet.ScaledMap.ext
  change
    (standardTypeAEndpointOppositeCornerCarrierIso.{u} g).hom ≫
        (SSet.horn g.n g.i).ι =
      (SSet.Subcomplex.homOfLE
        (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₂) ≫
        (standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom
  ext d t
  change
    ((standardTypeAEndpointOppositeCornerCarrierIso.{u} g).hom.app d t).val =
      (standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom.app d
        ((SSet.Subcomplex.homOfLE
          (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₂).app d t)
  rw [standardTypeAEndpointOppositeCornerCarrierIso_hom_app_val.{u},
    standardTypeAEndpointOppositeSimplexCarrierIso_hom_app.{u}]
  rfl

def standardTypeAEndpointOppositeCornerToAmbientSource
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeCorner.{u} g ⟶
      standardTypeAEndpointAmbientSource.{u} g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₃
  scaled := by
    intro t ht
    change (standardTypeAEndpointOppositeCornerScaling.{u} g).thin t at ht
    unfold standardTypeAEndpointOppositeCornerScaling at ht
    have hA := standardTypeAHornInclusion_scaled g.i
      ((standardTypeAEndpointOppositeCornerCarrierIso.{u} g).hom.app
        (op ⦋2⦌) t) ht
    change
      (standardTypeASimplexScaling g.i).thin
        (((SSet.horn g.n g.i).unionProd
          (intervalEndpoint.{u} g.endpoint)).ι.app (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₁₃).app
              (op ⦋2⦌) t)).1
    simpa using hA

def standardTypeAEndpointOppositeSimplexToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointOppositeSimplex.{u} g ⟶
      standardTypeABoundaryPrism.{u} g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₂₄
  scaled := by
    intro t ht
    change (standardTypeAEndpointOppositeSimplexScaling.{u} g).thin t at ht
    unfold standardTypeAEndpointOppositeSimplexScaling at ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom.app
          (op ⦋2⦌) t) at ht
    rw [standardTypeAEndpointOppositeSimplexCarrierIso_hom_app.{u}] at ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeABoundaryPrismSubcomplex.{u} g).ι.app (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₂₄).app
              (op ⦋2⦌) t)).1
    simpa using ht

def standardTypeAEndpointAmbientSourceToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointAmbientSource.{u} g ⟶
      standardTypeABoundaryPrism.{u} g where
  map := SSet.Subcomplex.homOfLE
    (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₃₄
  scaled := by
    intro t ht
    change
      (scaledSimplexCylinder
        (standardTypeASimplexScaling g.i)).scaling.thin
        ((standardTypeABoundaryPrismSubcomplex.{u} g).ι.app (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            (standardTypeAEndpointOppositeCarrierBicartSq.{u} g).le₃₄).app
              (op ⦋2⦌) t))
    change
      (scaledSimplexCylinder
        (standardTypeASimplexScaling g.i)).scaling.thin
        (((SSet.horn g.n g.i).unionProd
          (intervalEndpoint.{u} g.endpoint)).ι.app (op ⦋2⦌) t) at ht
    rw [← NatTrans.comp_app_apply, SSet.Subcomplex.homOfLE_ι]
    exact ht

theorem standardTypeAEndpointOppositeGeneratedScaling_eq_boundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    generatedPushoutScaling
      (standardTypeAEndpointAmbientSourceScaling.{u} g)
      (standardTypeAEndpointOppositeSimplexScaling.{u} g)
      (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
      (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map =
        standardTypeABoundaryPrismScaling.{u} g := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    rcases ht with hmin | ⟨x, hx, rfl⟩ | ⟨y, hy, rfl⟩
    · exact
        (minimalScaling_map
          (standardTypeABoundaryPrismScaling.{u} g) (𝟙 _)) t hmin
    · exact (standardTypeAEndpointAmbientSourceToBoundary.{u} g).scaled x hx
    · exact (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).scaled y hy
  · intro t ht
    have hmem' :
        t.val ∈
          (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g ⊔
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint.{u} g.endpoint))).obj (op ⦋2⦌) := by
      rw [(standardTypeAEndpointOppositeCarrierBicartSq.{u} g).sup_eq]
      exact t.property
    have hmem :
        t.val ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint.{u} g.endpoint)).obj (op ⦋2⦌) ∨
          t.val ∈
            (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g).obj
              (op ⦋2⦌) := by
      change
        t.val ∈
            (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g).obj
              (op ⦋2⦌) ∨
          t.val ∈
            ((SSet.horn g.n g.i).unionProd
              (intervalEndpoint.{u} g.endpoint)).obj (op ⦋2⦌) at hmem'
      exact hmem'.symm
    rcases hmem with hsource | hopposite
    · let x :
          ((SSet.horn g.n g.i).unionProd
            (intervalEndpoint.{u} g.endpoint) : SSet.{u}).obj (op ⦋2⦌) :=
        ⟨t.val, hsource⟩
      have hxmap :
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map.app
            (op ⦋2⦌) x = t := by
        apply Subtype.ext
        rfl
      refine Or.inr (Or.inl ⟨x, ?_, hxmap⟩)
      change
        (scaledSimplexCylinder
          (standardTypeASimplexScaling g.i)).scaling.thin
          (((SSet.horn g.n g.i).unionProd
            (intervalEndpoint.{u} g.endpoint)).ι.app (op ⦋2⦌) x)
      change
        (scaledSimplexCylinder
          (standardTypeASimplexScaling g.i)).scaling.thin
          ((standardTypeABoundaryPrismSubcomplex.{u} g).ι.app
            (op ⦋2⦌) t) at ht
      simpa using ht
    · let x :
          (standardTypeAEndpointOppositeSimplexSubcomplex.{u} g : SSet.{u}).obj
            (op ⦋2⦌) :=
        ⟨t.val, hopposite⟩
      have hxmap :
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map.app
            (op ⦋2⦌) x = t := by
        apply Subtype.ext
        rfl
      refine Or.inr (Or.inr ⟨x, ?_, hxmap⟩)
      change
        (standardTypeASimplexScaling g.i).thin
          ((standardTypeAEndpointOppositeSimplexCarrierIso.{u} g).hom.app
            (op ⦋2⦌) x)
      rw [standardTypeAEndpointOppositeSimplexCarrierIso_hom_app.{u}]
      change
        (standardTypeASimplexScaling g.i).thin
          (((standardTypeABoundaryPrismSubcomplex.{u} g).ι.app
            (op ⦋2⦌) t).1) at ht
      simpa using ht

noncomputable def standardTypeAEndpointOppositeCarrier_scaled_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (standardTypeAEndpointOppositeCornerToAmbientSource.{u} g)
      (standardTypeAEndpointOppositeCellHom.{u} g)
      (standardTypeAEndpointAmbientSourceToBoundary.{u} g)
      (standardTypeAEndpointOppositeSimplexToBoundary.{u} g) := by
  have h :
      IsPushout
        (standardTypeAEndpointOppositeCornerToAmbientSource.{u} g)
        (standardTypeAEndpointOppositeCellHom.{u} g)
        (generatedPushoutInl
          (standardTypeAEndpointAmbientSourceScaling.{u} g)
          (standardTypeAEndpointOppositeSimplexScaling.{u} g)
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map)
        (generatedPushoutInr
          (standardTypeAEndpointAmbientSourceScaling.{u} g)
          (standardTypeAEndpointOppositeSimplexScaling.{u} g)
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map) :=
    generatedPushout_isPushout
      (standardTypeAEndpointOppositeCornerToAmbientSource.{u} g)
      (standardTypeAEndpointOppositeCellHom.{u} g)
      (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
      (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map
      (standardTypeAEndpointOppositeCarrier_isPushout.{u} g)
  have hScaling :
      generatedPushoutScaling
          (standardTypeAEndpointAmbientSourceScaling.{u} g)
          (standardTypeAEndpointOppositeSimplexScaling.{u} g)
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map =
        standardTypeABoundaryPrismScaling.{u} g :=
    standardTypeAEndpointOppositeGeneratedScaling_eq_boundary.{u} g
  let eBoundary :
      generatedPushoutTarget
          (standardTypeAEndpointAmbientSourceScaling.{u} g)
          (standardTypeAEndpointOppositeSimplexScaling.{u} g)
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map ≅
        standardTypeABoundaryPrism.{u} g :=
    scalingEqualityIso
      (generatedPushoutScaling
        (standardTypeAEndpointAmbientSourceScaling.{u} g)
        (standardTypeAEndpointOppositeSimplexScaling.{u} g)
        (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
        (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map)
      (standardTypeABoundaryPrismScaling.{u} g)
      hScaling
  refine h.of_iso
    (Iso.refl (standardTypeAEndpointOppositeCorner.{u} g))
    (Iso.refl (standardTypeAEndpointAmbientSource.{u} g))
    (Iso.refl (standardTypeAEndpointOppositeSimplex.{u} g))
    eBoundary ?_ ?_ ?_ ?_
  · simp
  · simp
  · change
      generatedPushoutInl
          (standardTypeAEndpointAmbientSourceScaling.{u} g)
          (standardTypeAEndpointOppositeSimplexScaling.{u} g)
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map ≫
          eBoundary.hom =
        standardTypeAEndpointAmbientSourceToBoundary.{u} g
    apply ScaledSSet.ScaledMap.ext
    change
      (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map ≫
          (scalingEqualityIso
            (generatedPushoutScaling
              (standardTypeAEndpointAmbientSourceScaling.{u} g)
              (standardTypeAEndpointOppositeSimplexScaling.{u} g)
              (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
              (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map)
            (standardTypeABoundaryPrismScaling.{u} g)
            hScaling).hom.map =
        (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
    rw [scalingEqualityIso_hom_map]
    exact Category.comp_id _
  · change
      generatedPushoutInr
          (standardTypeAEndpointAmbientSourceScaling.{u} g)
          (standardTypeAEndpointOppositeSimplexScaling.{u} g)
          (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
          (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map ≫
          eBoundary.hom =
        standardTypeAEndpointOppositeSimplexToBoundary.{u} g
    apply ScaledSSet.ScaledMap.ext
    change
      (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map ≫
          (scalingEqualityIso
            (generatedPushoutScaling
              (standardTypeAEndpointAmbientSourceScaling.{u} g)
              (standardTypeAEndpointOppositeSimplexScaling.{u} g)
              (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map
              (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map)
            (standardTypeABoundaryPrismScaling.{u} g)
            hScaling).hom.map =
        (standardTypeAEndpointOppositeSimplexToBoundary.{u} g).map
    rw [scalingEqualityIso_hom_map]
    exact Category.comp_id _

/-! ## Transport the whole pushout to the literal standard A generator -/

def standardTypeAEndpointStandardCornerToSource
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAScaledHorn
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) ⟶
      standardTypeAEndpointGeneratedPushoutSource.{u} g :=
  (standardTypeAEndpointOppositeCornerIso.{u} g).inv ≫
    standardTypeAEndpointOppositeCornerToAmbientSource.{u} g ≫
      (standardTypeAEndpointGeneratedSourceIsoAmbient.{u} g).inv

def standardTypeAEndpointStandardSimplexToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAScaledSimplex
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g) ⟶
      standardTypeABoundaryPrism.{u} g :=
  (standardTypeAEndpointOppositeSimplexIso.{u} g).inv ≫
    standardTypeAEndpointOppositeSimplexToBoundary.{u} g

theorem standardTypeAEndpointGeneratedSourceIsoAmbient_hom_boundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointGeneratedSourceIsoAmbient.{u} g).hom ≫
        standardTypeAEndpointAmbientSourceToBoundary.{u} g =
      standardTypeAEndpointToBoundaryPrism.{u} g := by
  apply ScaledSSet.ScaledMap.ext
  change
    (standardTypeAEndpointGeneratedSourceIsoAmbient.{u} g).hom.map ≫
        (standardTypeAEndpointAmbientSourceToBoundary.{u} g).map =
      (standardTypeAEndpointToBoundaryPrism.{u} g).map
  unfold standardTypeAEndpointGeneratedSourceIsoAmbient
  rw [scalingEqualityIso_hom_map]
  rfl

noncomputable def standardTypeAEndpointOpposite_scaled_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsPushout
      (standardTypeAEndpointStandardCornerToSource.{u} g)
      (standardTypeAScaledHornGeneratorHom
        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g))
      (standardTypeAEndpointToBoundaryPrism.{u} g)
      (standardTypeAEndpointStandardSimplexToBoundary.{u} g) := by
  refine (standardTypeAEndpointOppositeCarrier_scaled_isPushout.{u} g).of_iso
    (standardTypeAEndpointOppositeCornerIso.{u} g)
    (standardTypeAEndpointGeneratedSourceIsoAmbient.{u} g).symm
    (standardTypeAEndpointOppositeSimplexIso.{u} g)
    (Iso.refl (standardTypeABoundaryPrism.{u} g)) ?_ ?_ ?_ ?_
  · simp [standardTypeAEndpointStandardCornerToSource, Category.assoc]
  · exact (standardTypeAEndpointOppositeCellArrowIso.{u} g).hom.w.symm
  · rw [Iso.refl_hom, Category.comp_id]
    change
      standardTypeAEndpointAmbientSourceToBoundary.{u} g =
        (standardTypeAEndpointGeneratedSourceIsoAmbient.{u} g).inv ≫
          standardTypeAEndpointToBoundaryPrism.{u} g
    rw [← standardTypeAEndpointGeneratedSourceIsoAmbient_hom_boundary.{u} g]
    simp only [Category.assoc, Iso.inv_hom_id_assoc]
  · simp [standardTypeAEndpointStandardSimplexToBoundary, Category.assoc]

theorem standardTypeAEndpointToBoundaryPrism_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointToBoundaryPrism.{u} g) := by
  unfold standardABCRawCellularStep
  exact
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts_mk
      (standardTypeAEndpointOpposite_scaled_isPushout.{u} g)
      (MorphismProperty.le_coproducts
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})) _
        (standardTypeAGenerator_mem_ABC
          (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)))

theorem standardTypeAEndpointToBoundaryPrism_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointToBoundaryPrism.{u} g) := by
  unfold standardABCStrongCellularClosure
  exact
    MorphismProperty.le_transfiniteCompositions.{u}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAEndpointToBoundaryPrism_mem_rawCellular.{u} g)

/-! ## Prefix the endpoint A-step to the v1.76 alternating sequence -/

@[reducible]
def standardTypeAEndpointFullObj
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ℕ → ScaledSSet.{u} :=
  fun n =>
    match n with
    | 0 => standardTypeAEndpointGeneratedPushoutSource.{u} g
    | Nat.succ k =>
        (standardTypeABoundaryPrismAlternatingFunctor.{u} g).obj k

@[reducible]
noncomputable def standardTypeAEndpointFullStep
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (n : ℕ) →
      standardTypeABoundaryPrismScaledCatHom
        (standardTypeAEndpointFullObj.{u} g n)
        (standardTypeAEndpointFullObj.{u} g (n + 1)) := by
  intro n
  cases n with
  | zero =>
      exact
        standardTypeAEndpointToBoundaryPrism.{u} g ≫
          (standardTypeABoundaryPrismAlternatingBotIso.{u} g).inv
  | succ n =>
      exact
        (standardTypeABoundaryPrismAlternatingFunctor.{u} g).map
          (homOfLE (Nat.le_add_right n 1))

@[simp]
theorem standardTypeAEndpointFullStep_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointFullStep.{u} g 0 =
      standardTypeAEndpointToBoundaryPrism.{u} g ≫
        (standardTypeABoundaryPrismAlternatingBotIso.{u} g).inv := by
  rfl

@[simp]
theorem standardTypeAEndpointFullStep_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeAEndpointFullStep.{u} g (Nat.succ n) =
      (standardTypeABoundaryPrismAlternatingFunctor.{u} g).map
        (homOfLE (Nat.le_add_right n 1)) := by
  rfl

local instance standardTypeAEndpointRawStep_respectsIso :
    (standardABCRawCellularStep :
      MorphismProperty (ScaledSSet.{u})).RespectsIso := by
  unfold standardABCRawCellularStep
  infer_instance

theorem standardTypeAEndpointFullStep_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointFullStep.{u} g n) := by
  cases n with
  | zero =>
      rw [standardTypeAEndpointFullStep_zero]
      apply MorphismProperty.RespectsIso.postcomp
      exact standardTypeAEndpointToBoundaryPrism_mem_rawCellular.{u} g
  | succ n =>
      rw [standardTypeAEndpointFullStep_succ,
        standardTypeABoundaryPrismAlternatingFunctor_map_succ]
      exact standardTypeABoundaryPrismAlternatingStep_mem_rawCellular.{u} g n

@[reducible]
noncomputable def standardTypeAEndpointFullFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} :=
  Functor.ofSequence (standardTypeAEndpointFullStep.{u} g)

@[simp]
theorem standardTypeAEndpointFullFunctor_obj
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullFunctor.{u} g).obj n =
      standardTypeAEndpointFullObj.{u} g n := by
  rfl

@[simp]
theorem standardTypeAEndpointFullFunctor_map_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullFunctor.{u} g).map
        (homOfLE (Nat.le_add_right n 1)) =
      standardTypeAEndpointFullStep.{u} g n := by
  unfold standardTypeAEndpointFullFunctor
  exact
    Functor.ofSequence_map_homOfLE_succ
      (C := ScaledSSet.{u})
      (X := standardTypeAEndpointFullObj.{u} g)
      (standardTypeAEndpointFullStep.{u} g) n

@[reducible]
noncomputable def standardTypeAEndpointFullToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismScaledCatHom
      ((standardTypeAEndpointFullFunctor.{u} g).obj n)
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)) := by
  cases n with
  | zero =>
      exact standardTypeAEndpointScaledLeibnizPushoutProductHom.{u} g
  | succ n =>
      exact (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app n

@[simp]
theorem standardTypeAEndpointFullToCylinder_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointFullToCylinder.{u} g 0 =
      standardTypeAEndpointScaledLeibnizPushoutProductHom.{u} g := by
  rfl

@[simp]
theorem standardTypeAEndpointFullToCylinder_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n) =
      (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app n := by
  rfl

theorem standardTypeAEndpointFullToCylinder_succ_naturality
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullFunctor.{u} g).map
          (homOfLE (Nat.le_add_right n 1)) ≫
        standardTypeAEndpointFullToCylinder.{u} g (n + 1) =
      standardTypeAEndpointFullToCylinder.{u} g n ≫
        ((Functor.const ℕ).obj
          (scaledSimplexCylinder (standardTypeASimplexScaling g.i))).map
            (homOfLE (Nat.le_add_right n 1)) := by
  cases n with
  | zero =>
      rw [Functor.const_obj_map, Category.comp_id,
        standardTypeAEndpointFullFunctor_map_succ,
        standardTypeAEndpointFullStep_zero,
        standardTypeAEndpointFullToCylinder_zero,
        standardTypeAEndpointFullToCylinder_succ,
        Category.assoc]
      have htail :=
        (standardTypeABoundaryPrismRawTransfiniteComposition.{u} g).fac
      change
        (standardTypeABoundaryPrismAlternatingBotIso.{u} g).inv ≫
            (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app 0 =
          standardTypeABoundaryPrismToCylinder.{u} g at htail
      rw [htail]
      exact standardTypeAEndpointLeibniz_factor_boundaryPrism.{u} g
  | succ n =>
      rw [Functor.const_obj_map, Category.comp_id,
        standardTypeAEndpointFullFunctor_map_succ,
        standardTypeAEndpointFullStep_succ,
        standardTypeAEndpointFullToCylinder_succ,
        standardTypeAEndpointFullToCylinder_succ]
      have h :=
        (standardTypeABoundaryPrismAlternatingCocone.{u} g).w
          (homOfLE (Nat.le_add_right n 1))
      simpa only [Functor.const_obj_map, Category.comp_id] using h

@[reducible]
noncomputable def standardTypeAEndpointFullCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeAEndpointFullFunctor.{u} g) :=
  Cocone.mk
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    (NatTrans.ofSequence
      (F := standardTypeAEndpointFullFunctor.{u} g)
      (G := (Functor.const ℕ).obj
        (scaledSimplexCylinder (standardTypeASimplexScaling g.i)))
      (standardTypeAEndpointFullToCylinder.{u} g)
      (standardTypeAEndpointFullToCylinder_succ_naturality.{u} g))

@[simp]
theorem standardTypeAEndpointFullCocone_ι_app
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullCocone.{u} g).ι.app n =
      standardTypeAEndpointFullToCylinder.{u} g n := by
  rfl

theorem standardTypeAEndpointFullCocone_step
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    (standardTypeAEndpointFullFunctor.{u} g).map
          (homOfLE (Nat.le_add_right n 1)) ≫
        s.ι.app (n + 1) =
      s.ι.app n := by
  have h := s.w (homOfLE (Nat.le_add_right n 1))
  simpa only [Functor.const_obj_map, Category.comp_id] using h

@[reducible]
noncomputable def standardTypeAEndpointFullTailObjIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingFunctor.{u} g).obj n ≅
      (standardTypeAEndpointFullFunctor.{u} g).obj (Nat.succ n) := by
  exact Iso.refl _

@[reducible]
noncomputable def standardTypeAEndpointFullTailLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    standardTypeABoundaryPrismScaledCatHom
      ((standardTypeABoundaryPrismAlternatingFunctor.{u} g).obj n) s.pt := by
  exact s.ι.app (Nat.succ n)

theorem standardTypeAEndpointFullTailLeg_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingFunctor.{u} g).map
          (homOfLE (Nat.le_add_right n 1)) ≫
        standardTypeAEndpointFullTailLeg.{u} g s (Nat.succ n) =
      standardTypeAEndpointFullTailLeg.{u} g s n := by
  have h := standardTypeAEndpointFullCocone_step.{u} g s (Nat.succ n)
  rw [standardTypeAEndpointFullFunctor_map_succ,
    standardTypeAEndpointFullStep_succ] at h
  simpa only [standardTypeAEndpointFullTailLeg, Nat.add_one] using h

theorem standardTypeAEndpointFullTailLeg_succ_naturality
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingFunctor.{u} g).map
          (homOfLE (Nat.le_add_right n 1)) ≫
        standardTypeAEndpointFullTailLeg.{u} g s (Nat.succ n) =
      standardTypeAEndpointFullTailLeg.{u} g s n ≫
        ((Functor.const ℕ).obj s.pt).map
          (homOfLE (Nat.le_add_right n 1)) := by
  rw [Functor.const_obj_map, Category.comp_id]
  exact standardTypeAEndpointFullTailLeg_succ.{u} g s n

@[reducible]
noncomputable def standardTypeAEndpointFullTailCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g)) :
    Cocone (standardTypeABoundaryPrismAlternatingFunctor.{u} g) :=
  Cocone.mk s.pt
    (NatTrans.ofSequence
      (F := standardTypeABoundaryPrismAlternatingFunctor.{u} g)
      (G := (Functor.const ℕ).obj s.pt)
      (standardTypeAEndpointFullTailLeg.{u} g s)
      (standardTypeAEndpointFullTailLeg_succ_naturality.{u} g s))

@[simp]
theorem standardTypeAEndpointFullTailCocone_ι_app
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    (standardTypeAEndpointFullTailCocone.{u} g s).ι.app n =
      standardTypeAEndpointFullTailLeg.{u} g s n := by
  simp only [standardTypeAEndpointFullTailCocone, NatTrans.ofSequence_app]

theorem standardTypeAEndpointFullTailObjIso_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
        standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n) =
      (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app n := by
  apply ScaledSSet.ScaledMap.ext
  rfl

theorem standardTypeAEndpointFullTailObjIso_toLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
        s.ι.app (Nat.succ n) =
      standardTypeAEndpointFullTailLeg.{u} g s n := by
  apply ScaledSSet.ScaledMap.ext
  rfl

theorem standardTypeAEndpointFullTailFac
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeAEndpointFullFunctor.{u} g))
    (n : ℕ) :
    standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n) ≫
        (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
          (standardTypeAEndpointFullTailCocone.{u} g s) =
      s.ι.app (Nat.succ n) := by
  apply (cancel_epi (standardTypeAEndpointFullTailObjIso.{u} g n).hom).1
  calc
    (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
          (standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n) ≫
            (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
              (standardTypeAEndpointFullTailCocone.{u} g s)) =
        ((standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
            standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n)) ≫
          (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
            (standardTypeAEndpointFullTailCocone.{u} g s) :=
      (Category.assoc _ _ _).symm
    _ = (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app n ≫
          (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
            (standardTypeAEndpointFullTailCocone.{u} g s) := by
      rw [standardTypeAEndpointFullTailObjIso_toCylinder.{u}]
    _ = (standardTypeAEndpointFullTailCocone.{u} g s).ι.app n :=
      (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).fac
        (standardTypeAEndpointFullTailCocone.{u} g s) n
    _ = standardTypeAEndpointFullTailLeg.{u} g s n := by
      rw [standardTypeAEndpointFullTailCocone_ι_app]
    _ = (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
          s.ι.app (Nat.succ n) :=
      (standardTypeAEndpointFullTailObjIso_toLeg.{u} g s n).symm

noncomputable def standardTypeAEndpointFullCoconeIsColimit
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsColimit (standardTypeAEndpointFullCocone.{u} g) where
  desc s :=
    (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
      (standardTypeAEndpointFullTailCocone.{u} g s)
  fac s j := by
    cases j with
    | zero =>
        have hnat :=
          standardTypeAEndpointFullToCylinder_succ_naturality.{u} g 0
        rw [Functor.const_obj_map, Category.comp_id] at hnat
        have htail := standardTypeAEndpointFullTailFac.{u} g s 0
        have htail' :
            standardTypeAEndpointFullToCylinder.{u} g 1 ≫
                (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
                  (standardTypeAEndpointFullTailCocone.{u} g s) =
              s.ι.app 1 := by
          simpa only [Nat.succ_eq_add_one] using htail
        have hstep := standardTypeAEndpointFullCocone_step.{u} g s 0
        rw [standardTypeAEndpointFullCocone_ι_app]
        calc
          standardTypeAEndpointFullToCylinder.{u} g 0 ≫
                (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
                  (standardTypeAEndpointFullTailCocone.{u} g s) =
              ((standardTypeAEndpointFullFunctor.{u} g).map
                    (homOfLE (Nat.le_add_right 0 1)) ≫
                  standardTypeAEndpointFullToCylinder.{u} g 1) ≫
                (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
                  (standardTypeAEndpointFullTailCocone.{u} g s) := by
                    rw [hnat]
          _ = (standardTypeAEndpointFullFunctor.{u} g).map
                  (homOfLE (Nat.le_add_right 0 1)) ≫
                (standardTypeAEndpointFullToCylinder.{u} g 1 ≫
                  (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
                    (standardTypeAEndpointFullTailCocone.{u} g s)) := by
                      simp only [Category.assoc]
          _ = (standardTypeAEndpointFullFunctor.{u} g).map
                  (homOfLE (Nat.le_add_right 0 1)) ≫
                s.ι.app 1 := by
                  exact congrArg
                    (fun q =>
                      (standardTypeAEndpointFullFunctor.{u} g).map
                          (homOfLE (Nat.le_add_right 0 1)) ≫ q)
                    htail'
          _ = s.ι.app 0 := hstep
    | succ n =>
        rw [standardTypeAEndpointFullCocone_ι_app]
        exact standardTypeAEndpointFullTailFac.{u} g s n
  uniq s m hm := by
    apply (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).hom_ext
    intro n
    have hmn := hm (Nat.succ n)
    rw [standardTypeAEndpointFullCocone_ι_app] at hmn
    have hdesc := standardTypeAEndpointFullTailFac.{u} g s n
    calc
      (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app n ≫ m =
          ((standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
            standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n)) ≫ m := by
        rw [standardTypeAEndpointFullTailObjIso_toCylinder.{u}]
      _ = (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
            (standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n) ≫ m) :=
        Category.assoc _ _ _
      _ = (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
            s.ι.app (Nat.succ n) := by
        rw [hmn]
      _ = (standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
            (standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n) ≫
              (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
                (standardTypeAEndpointFullTailCocone.{u} g s)) := by
        rw [hdesc]
      _ = ((standardTypeAEndpointFullTailObjIso.{u} g n).hom ≫
              standardTypeAEndpointFullToCylinder.{u} g (Nat.succ n)) ≫
            (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
              (standardTypeAEndpointFullTailCocone.{u} g s) :=
        (Category.assoc _ _ _).symm
      _ = (standardTypeABoundaryPrismAlternatingCocone.{u} g).ι.app n ≫
            (standardTypeABoundaryPrismAlternatingCoconeIsColimit.{u} g).desc
              (standardTypeAEndpointFullTailCocone.{u} g s) := by
        rw [standardTypeAEndpointFullTailObjIso_toCylinder.{u}]

@[reducible]
noncomputable def standardTypeAEndpointFullBotIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAEndpointFullFunctor.{u} g).obj ⊥ ≅
      standardTypeAEndpointGeneratedPushoutSource.{u} g := by
  exact Iso.refl _

noncomputable def standardTypeAEndpointRawTransfiniteComposition
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty.TransfiniteCompositionOfShape
      (C := ScaledSSet.{u})
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      ℕ (standardTypeAEndpointScaledLeibnizPushoutProductHom.{u} g) where
  F := standardTypeAEndpointFullFunctor.{u} g
  isoBot := standardTypeAEndpointFullBotIso.{u} g
  incl := (standardTypeAEndpointFullCocone.{u} g).ι
  isColimit := standardTypeAEndpointFullCoconeIsColimit.{u} g
  fac := by
    apply ScaledSSet.ScaledMap.ext
    rfl
  map_mem j _ := by
    have hhom :
        (homOfLE (Order.le_succ j) : j ⟶ j + 1) =
          homOfLE (Nat.le_add_right j 1) :=
      Subsingleton.elim _ _
    rw [hhom, standardTypeAEndpointFullFunctor_map_succ.{u}]
    exact standardTypeAEndpointFullStep_mem_rawCellular.{u} g j

theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointScaledLeibnizPushoutProductHom.{u} g) := by
  unfold standardABCStrongCellularClosure
  have h :=
    (standardTypeAEndpointRawTransfiniteComposition.{u} g).ofOrderIso
      (orderIsoShrink.{u} ℕ).symm
  exact
    (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
      (W := (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})))
      (Shrink.{u} ℕ)) _ h.mem

theorem standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAEndpointScaledLeibnizPushoutProductHom.{u} g) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_strongCellular.{u} g)

def standardABCTypeAEndpointLeibnizCellularCertificateConstructed :
    StandardABCTypeAEndpointLeibnizCellularCertificate.{u} where
  generators_le_cellular := by
    intro A B f hf
    dsimp [standardTypeAScaledLeibnizPushoutProductGenerators] at hf
    cases hf with
    | mk g =>
        exact standardTypeAEndpointScaledLeibnizPushoutProductHom_mem_cellular.{u} g

theorem standardABCTypeAEndpointLeibnizStability_proved :
    StandardABCTypeAEndpointLeibnizStability.{u} :=
  standardABCTypeAEndpointLeibnizCellularCertificateConstructed.toLeibnizStability

theorem standardABCTypeAEndpointLeibnizLifting_proved :
    StandardABCTypeAEndpointLeibnizLifting.{u} :=
  standardABCTypeAEndpointLeibnizCellularCertificateConstructed.lifting

end

end KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77