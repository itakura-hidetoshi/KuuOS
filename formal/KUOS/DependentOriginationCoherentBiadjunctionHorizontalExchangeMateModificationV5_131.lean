import KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeMateModificationV5_131

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic

set_option autoImplicit false
noncomputable section

/-!
# F34/v5.131 — NATURAL mixed whiskering exchange × original right-mate modification

The new F34 quotient natural isomorphism has TWO distinct naturality
paths for every genuine comparison-kernel quotient-category morphism.
Given ANY native quotient prefix beginning at the ORIGINAL F.map(f)
and G.map(f), both paths induce separately defined ORIGINAL F25/F33
lax-right-mate boundaries. We prove equality of (1) left boundaries,
(2) right boundaries, (3) the CROSS-boundary modification square, and
(4) their actual original compressed F-ISO / forward G-2-cell pair.

This is a quantified naturality-square statement in the genuine F28
quotient category, not merely the pointwise observation that
associators exist. The original right-mate modification is unchanged.
No invertibility assumption on the original G comparison 2-cell.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- GENUINE F34 modification-naturality square for the unchanged
original mate. The mixed F30 whiskering naturality square is pasted
after an arbitrary quotient path from the original F.map(f), G.map(f).
Both independently descended mate boundaries AND their cross-square
agree for the two distinct naturality routes. -/
theorem horizontalExchangeOriginalMateModificationNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
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
      (leftKernelQuotientWhiskerFunctor aF (F.obj Y)
        aG (G.obj Y) uF uG).map
          ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q)
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) := by
  exact mateBoundaries_of_equal_quotient_postcomposition
    dσ dθ Γ f basePath _ _
    (kernelQuotientHorizontalExchangeNaturality aF bF aG bG
      uF uG vF vG q)

/-- The two F34 naturality routes have the SAME actual F25 finite
comparison kernel Hom class, not merely the same mate-boundary image. -/
theorem horizontalExchangeOriginalKernelClassNaturality
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
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
      (leftKernelQuotientWhiskerFunctor aF (F.obj Y)
        aG (G.obj Y) uF uG).map
          ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q)
    kernelCategoryHomToKernelHom (basePath ≫ routeLR) =
      kernelCategoryHomToKernelHom (basePath ≫ routeRL) := by
  exact congrArg
    (fun t => kernelCategoryHomToKernelHom (basePath ≫ t))
    (kernelQuotientHorizontalExchangeNaturality aF bF aG bG
      uF uG vF vG q)

/-- The two F34 exchange routes have exactly the same original
F27 compressed pair of F 2-ISO and arbitrary forward G 2-cell, even
after arbitrary composition with a genuine original quotient path. -/
theorem horizontalExchangeOriginalCompressionNaturality
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (q : x ⟶ y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
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
      (leftKernelQuotientWhiskerFunctor aF (F.obj Y)
        aG (G.obj Y) uF uG).map
          ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q)
    (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫ routeLR) =
    (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫ routeRL) := by
  exact congrArg
    (fun t => (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫ t))
    (kernelQuotientHorizontalExchangeNaturality aF bF aG bG
      uF uG vF vG q)

#print axioms horizontalExchangeOriginalMateModificationNaturality
#print axioms horizontalExchangeOriginalKernelClassNaturality
#print axioms horizontalExchangeOriginalCompressionNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalExchangeMateModificationV5_131
