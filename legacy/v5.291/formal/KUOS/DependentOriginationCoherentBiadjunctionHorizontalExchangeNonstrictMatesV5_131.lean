import KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeMateModificationV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeNonstrictMatesV5_131

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic

set_option autoImplicit false
noncomputable section

/-!
# F34/v5.131 — original nonstrict mapId/mapComp plus MIXED NATURAL exchange

The F34 mixed horizontal naturality square provides TWO genuinely
different comparison paths. Prepending the ORIGINAL F.mapId or
F.mapComp ISO and ORIGINAL forward G.toOplax.mapId/mapComp comparison
must preserve both the true lax right-mate boundary and the native
F-ISO/G arbitrary-cell compressed comparison. Here the resulting
equations are proved on real quotient CATEGORY arrows, not a
replacement strict or invertible-G construction.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Two mixed F30 naturality routes, followed by the unchanged
original nonstrict mapId comparison, have the same full original
left/right lax mate boundary and compressed F/G comparison cells. -/
theorem originalMapIdHorizontalExchangeMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj X) (vG : bG ⟶ G.obj X)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG vF vG).obj x)) :
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    let routeLR :=
      (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG vF vG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map q) ≫
        exchange.hom.app y
    let routeRL := exchange.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj X)
        aG (G.obj X) uF uG).map
          ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q)
    quotientLeftMateBoundary dσ dθ Γ (𝟙 X)
      (originalMapIdQuotientPrepend (F := F) (G := G) X
        (kernelCategoryHomToKernelHom (basePath ≫ routeLR))) =
      quotientRightMateBoundary dσ dθ Γ (𝟙 X)
        (originalMapIdQuotientPrepend (F := F) (G := G) X
          (kernelCategoryHomToKernelHom (basePath ≫ routeRL))) ∧
    quotientComposite
      (originalMapIdQuotientPrepend (F := F) (G := G) X
        (kernelCategoryHomToKernelHom (basePath ≫ routeLR))) =
      quotientComposite
        (originalMapIdQuotientPrepend (F := F) (G := G) X
          (kernelCategoryHomToKernelHom (basePath ≫ routeRL))) := by
  exact originalMapIdMateBoundaries_of_equal_category_arrows dσ dθ Γ X _ _
    (congrArg (fun t => basePath ≫ t)
      (kernelQuotientHorizontalExchangeNaturality aF bF aG bG
        uF uG vF vG q))

/-- Same genuine NATURAL exchange square, now retaining the untouched
original mapComp ISO and the forward, possibly noninvertible
G.toOplax.mapComp. The two routes' original mate pastings agree. -/
theorem originalMapCompHorizontalExchangeMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Z) (vG : bG ⟶ G.obj Z)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG vF vG).obj x)) :
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    let routeLR :=
      (rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG vF vG).map
          ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map q) ≫
        exchange.hom.app y
    let routeRL := exchange.hom.app x ≫
      (leftKernelQuotientWhiskerFunctor aF (F.obj Z)
        aG (G.obj Z) uF uG).map
          ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q)
    quotientLeftMateBoundary dσ dθ Γ (f ≫ g)
      (originalMapCompQuotientPrepend (F := F) (G := G) f g
        (kernelCategoryHomToKernelHom (basePath ≫ routeLR))) =
      quotientRightMateBoundary dσ dθ Γ (f ≫ g)
        (originalMapCompQuotientPrepend (F := F) (G := G) f g
          (kernelCategoryHomToKernelHom (basePath ≫ routeRL))) ∧
    quotientComposite
      (originalMapCompQuotientPrepend (F := F) (G := G) f g
        (kernelCategoryHomToKernelHom (basePath ≫ routeLR))) =
      quotientComposite
        (originalMapCompQuotientPrepend (F := F) (G := G) f g
          (kernelCategoryHomToKernelHom (basePath ≫ routeRL))) := by
  exact originalMapCompMateBoundaries_of_equal_category_arrows dσ dθ Γ f g _ _
    (congrArg (fun t => basePath ≫ t)
      (kernelQuotientHorizontalExchangeNaturality aF bF aG bG
        uF uG vF vG q))

#print axioms originalMapIdHorizontalExchangeMateNaturality
#print axioms originalMapCompHorizontalExchangeMateNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeNonstrictMatesV5_131
