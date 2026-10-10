import KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130

namespace KUOS.DependentOriginationCoherentBiadjunctionF32NonstrictPentagonTriangleMatesV5_130

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130.Generic

set_option autoImplicit false
noncomputable section

/-!
# F33 / v5.130 — concrete F32 Pentagon/Triangle × F29 mapId/mapComp

For EACH of the two independent F32 higher-coherence diagrams,
we compare the two exact original F28 quotient pastes AFTER prepending
the untouched original (possibly nonstrict) F.mapId/G.toOplax.mapId
or F.mapComp/G.toOplax.mapComp. BOTH of the originally descended F25
lax-right-mate boundaries agree ACROSS the different routes and their
real compressed F-ISO / G-forward-cell pairs agree. F is inverted only
where guaranteed by the original pseudofunctor structural ISO; no
invertibility requirement on arbitrary G comparison arrows is introduced.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Real F32 PENTAGON long/short paths are identical AFTER
the unchanged F29 original nonstrict MapId, with equality of BOTH mate
boundaries and the entire original F/G compressed comparison pair. -/
theorem originalPentagonMapIdMateCompatibility
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {bF cF dF bG cG dG : C}
    (uF : F.obj X ⟶ bF) (vF : bF ⟶ cF)
    (wF : cF ⟶ dF) (zF : dF ⟶ F.obj X)
    (uG : G.obj X ⟶ bG) (vG : bG ⟶ cG)
    (wG : cG ⟶ dG) (zG : dG ⟶ G.obj X)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      (⟨⟨(((uF ≫ vF) ≫ wF) ≫ zF), (((uG ≫ vG) ≫ wG) ≫ zG)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X))) :
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom))
    quotientLeftMateBoundary dσ dθ Γ (𝟙 X) longClass =
        quotientRightMateBoundary dσ dθ Γ (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass := by
  exact originalMapIdMateBoundaries_of_equal_category_arrows dσ dθ Γ X
    (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom)
    (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom)
    (congrArg (fun t => basePath ≫ t.hom)
      (kernelQuotientPentagon uF vF wF zF uG vG wG zG))

/-- Real F32 PENTAGON long/short paths are identical AFTER
the unchanged F29 original nonstrict MapComp, with equality of BOTH mate
boundaries and the entire original F/G compressed comparison pair. -/
theorem originalPentagonMapCompMateCompatibility
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {bF cF dF bG cG dG : C}
    (uF : F.obj X ⟶ bF) (vF : bF ⟶ cF)
    (wF : cF ⟶ dF) (zF : dF ⟶ F.obj Z)
    (uG : G.obj X ⟶ bG) (vG : bG ⟶ cG)
    (wG : cG ⟶ dG) (zG : dG ⟶ G.obj Z)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      (⟨⟨(((uF ≫ vF) ≫ wF) ≫ zF), (((uG ≫ vG) ≫ wG) ≫ zG)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z))) :
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom))
    quotientLeftMateBoundary dσ dθ Γ (f ≫ g) longClass =
        quotientRightMateBoundary dσ dθ Γ (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass := by
  exact originalMapCompMateBoundaries_of_equal_category_arrows dσ dθ Γ f g
    (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom)
    (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom)
    (congrArg (fun t => basePath ≫ t.hom)
      (kernelQuotientPentagon uF vF wF zF uG vG wG zG))

/-- Real F32 TRIANGLE long/short paths are identical AFTER
the unchanged F29 original nonstrict MapId, with equality of BOTH mate
boundaries and the entire original F/G compressed comparison pair. -/
theorem originalTriangleMapIdMateCompatibility
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {bF bG : C}
    (uF : F.obj X ⟶ bF) (vF : bF ⟶ F.obj X)
    (uG : G.obj X ⟶ bG) (vG : bG ⟶ G.obj X)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      (⟨⟨((uF ≫ 𝟙 bF) ≫ vF), ((uG ≫ 𝟙 bG) ≫ vG)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X))) :
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom))
    quotientLeftMateBoundary dσ dθ Γ (𝟙 X) longClass =
        quotientRightMateBoundary dσ dθ Γ (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass := by
  exact originalMapIdMateBoundaries_of_equal_category_arrows dσ dθ Γ X
    (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom)
    (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom)
    (congrArg (fun t => basePath ≫ t.hom)
      (kernelQuotientTriangle uF vF uG vG))

/-- Real F32 TRIANGLE long/short paths are identical AFTER
the unchanged F29 original nonstrict MapComp, with equality of BOTH mate
boundaries and the entire original F/G compressed comparison pair. -/
theorem originalTriangleMapCompMateCompatibility
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {bF bG : C}
    (uF : F.obj X ⟶ bF) (vF : bF ⟶ F.obj Z)
    (uG : G.obj X ⟶ bG) (vG : bG ⟶ G.obj Z)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      (⟨⟨((uF ≫ 𝟙 bF) ≫ vF), ((uG ≫ 𝟙 bG) ≫ vG)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z))) :
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom))
    quotientLeftMateBoundary dσ dθ Γ (f ≫ g) longClass =
        quotientRightMateBoundary dσ dθ Γ (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass := by
  exact originalMapCompMateBoundaries_of_equal_category_arrows dσ dθ Γ f g
    (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom)
    (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom)
    (congrArg (fun t => basePath ≫ t.hom)
      (kernelQuotientTriangle uF vF uG vG))
#print axioms originalPentagonMapIdMateCompatibility
#print axioms originalPentagonMapCompMateCompatibility
#print axioms originalTriangleMapIdMateCompatibility
#print axioms originalTriangleMapCompMateCompatibility

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionF32NonstrictPentagonTriangleMatesV5_130
