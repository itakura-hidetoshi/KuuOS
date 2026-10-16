import KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeTwoStageNaturalityV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionTwoStageExchangeMateNaturalityV5_132

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeMateModificationV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeTwoStageNaturalityV5_132.Generic

set_option autoImplicit false
noncomputable section

/-!
# F35/v5.132: native two-stage exchange NATURALITY through ORIGINAL lax right mates

The F34 mixed left/right exchange square can be vertically pasted for
TWO genuine F28 quotient CATEGORY arrows with an intermediate object.
We now prove the entire two-stage square preserves BOTH unchanged F33
right-mate boundary pastes; the intermediate whiskering functor is
applied separately at each stage, NOT replaced by a strict functor.
The G-side comparison remains arbitrary/noninvertible.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Both full original lax right-mate pastes and their crossed
modification square agree between two genuine VERTICALLY PASTED
F34 naturality routes, even after arbitrary original prefix paths. -/
theorem twoStageHorizontalExchangeOriginalMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y z : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y) (r : y ⟶ z)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG vF vG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF (F.obj Y)
        aG (G.obj Y) uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    let routeLR := (L.map q ≫ L.map r) ≫ exchange.hom.app z
    let routeRL := exchange.hom.app x ≫ (R.map q ≫ R.map r)
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) := by
  simpa only [Functor.map_comp] using
    (horizontalExchangeOriginalMateModificationNaturality dσ dθ Γ f
      uF uG vF vG (q ≫ r) basePath)

/-- The original finite-path quotient KERNEL HOM agrees for both
distinct two-stage mixed exchange routes after any original prefix;
this is stronger than merely comparing their mate boundary values. -/
theorem twoStageHorizontalExchangeOriginalKernelClass
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y z : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y) (r : y ⟶ z)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG vF vG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF (G.obj X) bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y) uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    kernelCategoryHomToKernelHom (basePath ≫
      ((L.map q ≫ L.map r) ≫ exchange.hom.app z)) =
      kernelCategoryHomToKernelHom (basePath ≫
        (exchange.hom.app x ≫ (R.map q ≫ R.map r))) := by
  simpa only [Functor.map_comp] using
    (horizontalExchangeOriginalKernelClassNaturality
      (F := F) (G := G) f uF uG vF vG (q ≫ r) basePath)

#print axioms twoStageHorizontalExchangeOriginalMateNaturality
#print axioms twoStageHorizontalExchangeOriginalKernelClass

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionTwoStageExchangeMateNaturalityV5_132
