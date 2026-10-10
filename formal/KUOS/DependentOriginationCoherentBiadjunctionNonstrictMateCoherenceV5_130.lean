import KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130

namespace KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic

set_option autoImplicit false
noncomputable section

/-!
# F33/v5.130: native F32 coherence after ACTUAL nonstrict F.mapId/mapComp

Original F.mapId / F.mapComp remain the original *invertible* structural
comparisons while G.toOplax.mapId / mapComp remain their original forward
(potentially noninvertible) 2-cells. Neither is collapsed to an identity.

The original F28 category quotient to F25 finite-chain kernel Hom bridge
allows us to prepend these native nonstrict pseudofunctor comparisons
to TWO independently composed F32 pentagon/triangle quotient routes.
Their resulting original lax-right-mate boundaries agree, and BOTH
compressed F/G comparison pairs agree, without choosing any inverse
on G or any new objectwise adjunction.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The actual F29 original mapId lift commutes with the F28-to-F25
bridge, and retains the EXACT F-side structural iso and the
potentially noninvertible G-side original identity comparison. -/
theorem originalMapIdCategory_composite
    (X : B) {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (q :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X))) :
    quotientComposite
        (originalMapIdQuotientPrepend (F := F) (G := G) X
          (kernelCategoryHomToKernelHom q)) =
      ((F.mapId X).trans
        ((quotientCompositeFunctor (F.obj X) (F.obj X)
          (G.obj X) (G.obj X)).map q).1,
       G.toOplax.mapId X ≫
        ((quotientCompositeFunctor (F.obj X) (F.obj X)
          (G.obj X) (G.obj X)).map q).2) := by
  rw [originalMapIdQuotientPrepend_composite,
    kernelCategoryHomToKernelHom_composite]

/-- Original nonstrict mapComp retains F.mapComp and the forward
G.toOplax.mapComp, after conversion from any genuine F28 category arrow. -/
theorem originalMapCompCategory_composite
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (q :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z))) :
    quotientComposite
        (originalMapCompQuotientPrepend (F := F) (G := G) f g
          (kernelCategoryHomToKernelHom q)) =
      ((F.mapComp f g).trans
        ((quotientCompositeFunctor (F.obj X) (F.obj Z)
          (G.obj X) (G.obj Z)).map q).1,
       G.toOplax.mapComp f g ≫
        ((quotientCompositeFunctor (F.obj X) (F.obj Z)
          (G.obj X) (G.obj Z)).map q).2) := by
  rw [originalMapCompQuotientPrepend_composite,
    kernelCategoryHomToKernelHom_composite]

/-- Equality of genuine F28 quotient-CATEGORY arrows is preserved
through the ORIGINAL mapId comparison and BOTH actual lax-right-mate
boundary pastings, together with the F/G compressed comparison pair. -/
theorem originalMapIdMateBoundaries_of_equal_category_arrows
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (q r :
      (⟨⟨𝟙 (F.obj X), 𝟙 (G.obj X)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj X) (G.obj X) (G.obj X)))
    (h : q = r) :
    quotientLeftMateBoundary dσ dθ Γ (𝟙 X)
      (originalMapIdQuotientPrepend (F := F) (G := G) X
        (kernelCategoryHomToKernelHom q)) =
    quotientRightMateBoundary dσ dθ Γ (𝟙 X)
      (originalMapIdQuotientPrepend (F := F) (G := G) X
        (kernelCategoryHomToKernelHom r)) ∧
    quotientComposite
      (originalMapIdQuotientPrepend (F := F) (G := G) X
        (kernelCategoryHomToKernelHom q)) =
    quotientComposite
      (originalMapIdQuotientPrepend (F := F) (G := G) X
        (kernelCategoryHomToKernelHom r)) := by
  subst r
  exact ⟨originalMapIdQuotientMateNaturality dσ dθ Γ X _, rfl⟩

/-- Equality of arbitrary quotient-category arrows is preserved
through the ORIGINAL nonstrict mapComp comparison and the exact
separately descended left/right lax mate boundaries. -/
theorem originalMapCompMateBoundaries_of_equal_category_arrows
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (q r :
      (⟨⟨F.map f ≫ F.map g, G.map f ≫ G.map g⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Z) (G.obj X) (G.obj Z)))
    (h : q = r) :
    quotientLeftMateBoundary dσ dθ Γ (f ≫ g)
      (originalMapCompQuotientPrepend (F := F) (G := G) f g
        (kernelCategoryHomToKernelHom q)) =
    quotientRightMateBoundary dσ dθ Γ (f ≫ g)
      (originalMapCompQuotientPrepend (F := F) (G := G) f g
        (kernelCategoryHomToKernelHom r)) ∧
    quotientComposite
      (originalMapCompQuotientPrepend (F := F) (G := G) f g
        (kernelCategoryHomToKernelHom q)) =
    quotientComposite
      (originalMapCompQuotientPrepend (F := F) (G := G) f g
        (kernelCategoryHomToKernelHom r)) := by
  subst r
  exact ⟨originalMapCompQuotientMateNaturality dσ dθ Γ f g _, rfl⟩

#print axioms originalMapIdCategory_composite
#print axioms originalMapCompCategory_composite
#print axioms originalMapIdMateBoundaries_of_equal_category_arrows
#print axioms originalMapCompMateBoundaries_of_equal_category_arrows

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionNonstrictMateCoherenceV5_130
