import KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteExchangeMateNaturalityV5_133

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133.Generic

set_option autoImplicit false
noncomputable section

/-!
# F36-C/v5.133: finite native quotient-arrow paths and ORIGINAL lax mates

No F26 comparison path is substituted for a F28 quotient-category
arrow. The entire finite chain is composed natively and then carried
through the ORIGINAL F33 bridge into the ORIGINAL F25 kernel-Hom
and unchanged lax right-mate boundaries. Every G-cell may be
noninvertible; the original F comparison retains its inverse ISO.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- ALL finite-length (including zero) left/right exchange pastings
preserve the two independently defined original F33 mate boundaries
and their cross-boundary modification square after arbitrary original
comparison prefixes. The required path equality is obtained from the
structural-induction proof F36-A, not by postulating coherence. -/
theorem finiteHorizontalExchangeOriginalMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : finiteKernelQuotientChain aF bF aG bG x y)
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
    let routeLR := L.map p.composite ≫ exchange.hom.app y
    let routeRL := exchange.hom.app x ≫ R.map p.composite
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) := by
  exact mateBoundaries_of_equal_quotient_postcomposition
    dσ dθ Γ f basePath _ _
    (kernelHorizontalExchangeFiniteNaturality
      aF bF aG bG uF uG vF vG p)

/-- Finite exchange routes are IDENTICAL in the original F25
KernelHom quotient, before applying either mate-boundary function. -/
theorem finiteHorizontalExchangeOriginalKernelClass
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : finiteKernelQuotientChain aF bF aG bG x y)
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
      (L.map p.composite ≫ exchange.hom.app y)) =
      kernelCategoryHomToKernelHom (basePath ≫
        (exchange.hom.app x ≫ R.map p.composite)) := by
  exact congrArg (fun t => kernelCategoryHomToKernelHom (basePath ≫ t))
    (kernelHorizontalExchangeFiniteNaturality
      aF bF aG bG uF uG vF vG p)

/-- Exact original F-ISO and arbitrary forward G-cell compression
of both finite exchange pastings agrees, including after any prefix. -/
theorem finiteHorizontalExchangeOriginalCompression
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : finiteKernelQuotientChain aF bF aG bG x y)
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
    (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫
        (L.map p.composite ≫ exchange.hom.app y)) =
    (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫
        (exchange.hom.app x ≫ R.map p.composite)) := by
  exact congrArg
    (fun t => (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫ t))
    (kernelHorizontalExchangeFiniteNaturality
      aF bF aG bG uF uG vF vG p)

/-- The mate modification remains independent of EVERY finite binary
parenthesization of the very same native F28 quotient-arrow sequence. -/
theorem bracketedHorizontalExchangeOriginalMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG : C}
    (uF : F.obj X ⟶ aF) (uG : G.obj X ⟶ aG)
    (vF : bF ⟶ F.obj Y) (vG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Bracketing x y)
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
    let routeLR := L.map p.evaluated ≫ exchange.hom.app y
    let routeRL := exchange.hom.app x ≫ R.map p.evaluated
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) ∧
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLR) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeRL) := by
  simpa only [Chain.Bracketing.evaluated_eq_flattened] using
    (finiteHorizontalExchangeOriginalMateNaturality
      dσ dθ Γ f uF uG vF vG p.flattened basePath)

#print axioms finiteHorizontalExchangeOriginalMateNaturality
#print axioms finiteHorizontalExchangeOriginalKernelClass
#print axioms finiteHorizontalExchangeOriginalCompression
#print axioms bracketedHorizontalExchangeOriginalMateNaturality

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteExchangeMateNaturalityV5_133
