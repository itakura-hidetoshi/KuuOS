import KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132 — four-stage native quotient Hexagon NATURALITY of
the original unmodified lax right-mate modification boundaries

F35-C's stagewise quotient NATURAL ISO has a genuine naturality
square for EVERY arrow of the F28 compression-kernel quotient, including
arbitrary NONINVERTIBLE G comparison cells. Precompose that square
with an arbitrary native comparison arrow starting at the ORIGINAL
F.map(f), G.map(f), and evaluate the unchanged F25/F33 mate boundaries
on both paths.

The original F.mapId/F.mapComp ISO and forward G.toOplax.mapId/mapComp
then preserve BOTH sides: no strictification, no new chosen adjuncts,
no G comparison inverses and no ambient biequivalence.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Full ORIGINAL lax right-mate modification coherence under the
ACTUAL F35 four-stage quotient HEXAGON NATURALITY square. Both mate
boundaries and the cross-boundary equality hold for arbitrary F/G
comparison morphisms and any original source 1-cell. -/
theorem kernelStagewiseHexagonOriginalMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map q) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Y)
        aG (G.obj Y) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map q)
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeShort) ∧
    kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeShort) ∧
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeShort) := by
  exact mateBoundaries_of_equal_quotient_postcomposition dσ dθ Γ f
    basePath _ _ ((kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG).hom.naturality q)

/-- ORIGINAL original mapId remains nonstrict after the true F35
four-stage quotient HEXAGON naturality square. Both original
lax right-mate boundaries and the COMPLETE F-ISO/G-forward-cell
comparison pair agree between the independently composed routes. -/
theorem kernelStagewiseHexagonOriginalMapIdMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj X) (wG : bG ⟶ G.obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map q) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj X)
        aG (G.obj X) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map q)
    let longClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapIdQuotientPrepend (F := F) (G := G) X
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary dσ dθ Γ (𝟙 X) longClass =
        quotientRightMateBoundary dσ dθ Γ (𝟙 X) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass := by
  exact originalMapIdMateBoundaries_of_equal_category_arrows dσ dθ Γ X _ _
    (congrArg (fun t => basePath ≫ t)
      ((kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG).hom.naturality q))

/-- ORIGINAL original mapComp remains nonstrict after the true F35
four-stage quotient HEXAGON naturality square. Both original
lax right-mate boundaries and the COMPLETE F-ISO/G-forward-cell
comparison pair agree between the independently composed routes. -/
theorem kernelStagewiseHexagonOriginalMapCompMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Z) (wG : bG ⟶ G.obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let hexagon := kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG
    let routeLong := (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG
            (vF ≫ uF) (vG ≫ uG)).map q) ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Z)
        aG (G.obj Z) (vF ≫ uF) (vG ≫ uG)).map
        ((rightKernelQuotientWhiskerFunctor aF bF aG bG
          wF wG).map q)
    let longClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeLong))
    let shortClass := originalMapCompQuotientPrepend (F := F) (G := G) f g
      (kernelCategoryHomToKernelHom (basePath ≫ routeShort))
    quotientLeftMateBoundary dσ dθ Γ (f ≫ g) longClass =
        quotientRightMateBoundary dσ dθ Γ (f ≫ g) shortClass ∧
      quotientComposite longClass = quotientComposite shortClass := by
  exact originalMapCompMateBoundaries_of_equal_category_arrows dσ dθ Γ f g _ _
    (congrArg (fun t => basePath ≫ t)
      ((kernelMixedHexagonStagewiseLongNatIso aF bF aG bG
      uF uG vF vG wF wG).hom.naturality q))
#print axioms kernelStagewiseHexagonOriginalMateNaturality
#print axioms kernelStagewiseHexagonOriginalMapIdMateNaturality
#print axioms kernelStagewiseHexagonOriginalMapCompMateNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132
