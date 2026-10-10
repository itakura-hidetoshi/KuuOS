import KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonInterchangeV5_134
import KUOS.DependentOriginationCoherentBiadjunctionStagewiseHexagonMateNaturalityV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonOriginalMatesV5_134

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionStagewiseQuotientMixedHexagonV5_132.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonInterchangeV5_134.Generic

set_option autoImplicit false
noncomputable section

/-!
# F37-B/v5.134 — F28 finite-path × F35 four-step hexagon × ORIGINAL mates

Use the explicit F37 two-dimensional naturality interchange, then
evaluate BOTH unmodified F25/F33 lax right-mate boundaries on the
same ACTUAL F28 quotient-category arrow after arbitrary original
comparison prefixes. The F-side 2-isomorphisms and forward,
potentially NONINVERTIBLE, G comparison 2-cells are unchanged.

The second natural transformation in the extended result is allowed
to be NONINVERTIBLE; this does not assert an ambient bicategory
biequivalence or unquotiented compression faithfulness.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- F37 interchange descends for ANY finite original F28 quotient
path to left, right and CROSS boundaries of the ORIGINAL lax mate. -/
theorem finiteStagewiseHexagonOriginalMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
        (vF ≫ uF) (vG ≫ uG)
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    let routeLong := L.map p.composite ≫ hexagon.hom.app y
    let routeShort := hexagon.hom.app x ≫ R.map p.composite
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
        kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeShort) ∧
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeShort) ∧
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeShort) := by
  exact mateBoundaries_of_equal_quotient_postcomposition dσ dθ Γ f
    basePath _ _ ((kernelStagewiseHexagonFiniteInterchange
      aF bF aG bG uF uG vF vG wF wG p).1)

/-- The two routes coincide in the ORIGINAL F25 finite-chain KernelHom
class BEFORE evaluation by either F33 mate boundary. -/
theorem finiteStagewiseHexagonOriginalKernelClass
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
        (vF ≫ uF) (vG ≫ uG)
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    kernelCategoryHomToKernelHom (basePath ≫
      (L.map p.composite ≫ hexagon.hom.app y)) =
      kernelCategoryHomToKernelHom (basePath ≫
        (hexagon.hom.app x ≫ R.map p.composite)) := by
  exact congrArg (fun t => kernelCategoryHomToKernelHom (basePath ≫ t))
    ((kernelStagewiseHexagonFiniteInterchange
      aF bF aG bG uF uG vF vG wF wG p).1)

/-- Both original compressed comparison cells (invertible F, forward G)
are identical for the independently pasted finite-stage hexagons. -/
theorem finiteStagewiseHexagonOriginalCompression
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
      leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
        (vF ≫ uF) (vG ≫ uG)
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫
        (L.map p.composite ≫ hexagon.hom.app y)) =
    (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫
        (hexagon.hom.app x ≫ R.map p.composite)) := by
  exact congrArg
    (fun t => (quotientCompositeFunctor (F.obj X) (F.obj Y)
      (G.obj X) (G.obj Y)).map (basePath ≫ t))
    ((kernelStagewiseHexagonFiniteInterchange
      aF bF aG bG uF uG vF vG wF wG p).1)

/-- Even after a SECOND arbitrary natural transformation, the full
F37 two-dimensional diagram respects BOTH original F25/F33 mate
boundaries, including their crossed modification equation. -/
theorem finiteStagewiseHexagonVerticalOriginalMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    (T : compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory (F.obj X) (F.obj Y)
        (G.obj X) (G.obj Y))
    (β :
      (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
        leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
          (vF ≫ uF) (vG ≫ uG)) ⟶ T)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    let routeLong := (L.map p.composite ≫ hexagon.hom.app y) ≫ β.app y
    let routeShort := hexagon.hom.app x ≫
      (β.app x ≫ T.map p.composite)
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
        kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeShort) ∧
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeShort) ∧
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ routeLong) =
        kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ routeShort) := by
  exact mateBoundaries_of_equal_quotient_postcomposition dσ dθ Γ f
    basePath _ _ (kernelStagewiseHexagonFiniteVerticalPasting
      aF bF aG bG uF uG vF vG wF wG T β p)

/-- Equality already holds in the original F25 KernelHom quotient
BEFORE applying the original mate to a two-dimensional paste. -/
theorem finiteStagewiseHexagonVerticalOriginalKernelClass
    {X Y : B} (f : X ⟶ Y)
    {aF bF aG bG eF eG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : F.obj X ⟶ eF) (vG : G.obj X ⟶ eG)
    (wF : bF ⟶ F.obj Y) (wG : bG ⟶ G.obj Y)
    (T : compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory (F.obj X) (F.obj Y)
        (G.obj X) (G.obj Y))
    (β :
      (rightKernelQuotientWhiskerFunctor aF bF aG bG wF wG ⋙
        leftKernelQuotientWhiskerFunctor aF (F.obj Y) aG (G.obj Y)
          (vF ≫ uF) (vG ≫ uG)) ⟶ T)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Path x y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)) ⟶
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG
        (vF ≫ uF) (vG ≫ uG) ⋙
        rightKernelQuotientWhiskerFunctor (F.obj X) bF
          (G.obj X) bG wF wG).obj x)) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG
      (vF ≫ uF) (vG ≫ uG) ⋙
      rightKernelQuotientWhiskerFunctor (F.obj X) bF
        (G.obj X) bG wF wG
    let hexagon := kernelMixedHexagonStagewiseLongNatIso
      aF bF aG bG uF uG vF vG wF wG
    kernelCategoryHomToKernelHom (basePath ≫
      ((L.map p.composite ≫ hexagon.hom.app y) ≫ β.app y)) =
    kernelCategoryHomToKernelHom (basePath ≫
      (hexagon.hom.app x ≫ (β.app x ≫ T.map p.composite))) := by
  exact congrArg (fun t => kernelCategoryHomToKernelHom (basePath ≫ t))
    (kernelStagewiseHexagonFiniteVerticalPasting
      aF bF aG bG uF uG vF vG wF wG T β p)

#print axioms finiteStagewiseHexagonOriginalMateNaturality
#print axioms finiteStagewiseHexagonOriginalKernelClass
#print axioms finiteStagewiseHexagonOriginalCompression
#print axioms finiteStagewiseHexagonVerticalOriginalMateNaturality
#print axioms finiteStagewiseHexagonVerticalOriginalKernelClass

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteHexagonOriginalMatesV5_134
