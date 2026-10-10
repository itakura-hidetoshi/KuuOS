import KUOS.DependentOriginationCoherentBiadjunctionActualLiftPentagonTriangleV5_129
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftNonstrictKernelV5_126

namespace KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F33 / v5.130: bridge genuine F28 quotient-CATEGORY arrows to ORIGINAL lax mate boundaries

The mate boundaries of F25 are defined on finite-comparison-chain
kernel Hom classes. F28 has a separate, real mathlib Quotient CATEGORY
with composable arrows. Here we connect those constructions without
identifying their types by fiat: pass a genuine quotient-category arrow
through the full faithful F28 compression functor, then use the original
F25 singleton quotient class. This gives exact original left/right mate
boundary operations on ACTUAL arrows of the F28 quotient category.

Both boundaries factor through the SAME F-ISO / arbitrary G 2-cell pair,
so composable arbitrary quotient arrows retain their genuine inverse-on-F
and forward-on-G orientations. No new G inverses or strictification.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Actual bridge from an arrow in the ORIGINAL F28 mathlib quotient
CATEGORY to the original F25 finite-chain kernel Hom. This is not a
replacement category or an assumed equivalence of ambient bicategories. -/
def kernelCategoryHomToKernelHom
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (q :
      (⟨⟨fF, fG⟩⟩ : compressionKernelCategory aF bF aG bG) ⟶
      (⟨⟨kF, kG⟩⟩ : compressionKernelCategory aF bF aG bG)) :
    KernelHom fF fG kF kG :=
  compositeClass ((quotientCompositeFunctor aF bF aG bG).map q)

/-- The bridge conserves EXACTLY both original compressed components:
F is a genuine 2-isomorphism, G is an arbitrary forward 2-cell. -/
theorem kernelCategoryHomToKernelHom_composite
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (q :
      (⟨⟨fF, fG⟩⟩ : compressionKernelCategory aF bF aG bG) ⟶
      (⟨⟨kF, kG⟩⟩ : compressionKernelCategory aF bF aG bG)) :
    quotientComposite (kernelCategoryHomToKernelHom q) =
      (quotientCompositeFunctor aF bF aG bG).map q := by
  exact quotientComposite_compositeClass _

/-- The original left lax-right-mate boundary, evaluated on a
GENUINE F28 quotient CATEGORY arrow rather than a chosen finite path. -/
def kernelCategoryLeftMateBoundary
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :=
  quotientLeftMateBoundary dσ dθ Γ f (kernelCategoryHomToKernelHom q)

/-- Independently descended ORIGINAL right lax-right-mate boundary on
the SAME actual quotient-category arrow. -/
def kernelCategoryRightMateBoundary
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :=
  quotientRightMateBoundary dσ dθ Γ f (kernelCategoryHomToKernelHom q)

/-- Actual F25 mate boundary normalizes through the full F28
quotient-CATEGORY composite, keeping the genuine inverse F comparison. -/
theorem kernelCategoryLeftMateBoundary_eq_compressed
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryLeftMateBoundary dσ dθ Γ f q =
      compressedMateLeftBoundary dσ dθ Γ f
        ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map q) := by
  rw [kernelCategoryLeftMateBoundary, quotientLeftMateBoundary_eq_compressed,
    kernelCategoryHomToKernelHom_composite]
  rfl

/-- The original independent RIGHT mate boundary likewise factors
through the genuine F28 quotient-category compression. -/
theorem kernelCategoryRightMateBoundary_eq_compressed
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryRightMateBoundary dσ dθ Γ f q =
      compressedMateRightBoundary dσ dθ Γ f
        ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map q) := by
  rw [kernelCategoryRightMateBoundary, quotientRightMateBoundary_eq_compressed,
    kernelCategoryHomToKernelHom_composite]
  rfl

/-- The UNCHANGED F22 mate naturality extends to every real quotient
category arrow, not merely a finite-path quotient representative. -/
theorem kernelCategoryMateNaturality
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryLeftMateBoundary dσ dθ Γ f q =
      kernelCategoryRightMateBoundary dσ dθ Γ f q :=
  quotientMateNaturality dσ dθ Γ f (kernelCategoryHomToKernelHom q)

/-- Actual concatenation of two native F28 quotient arrows acts
on mate boundaries by the authentic F inverse-ISO composition and the
genuine potentially NONINVERTIBLE forward G comparison composition. -/
theorem kernelCategoryLeftMateBoundary_comp
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y} {kG lG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)))
    (r :
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨lF, lG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryLeftMateBoundary dσ dθ Γ f (q ≫ r) =
      compressedMateLeftBoundary dσ dθ Γ f
        (((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map q).1.trans
          ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map r).1,
         ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map q).2 ≫
         ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map r).2) := by
  rw [kernelCategoryLeftMateBoundary_eq_compressed, Functor.map_comp]
  rfl

/-- The RIGHT boundary has the identical original F/G composition
orientation for arbitrary concatenations, despite different mate pastes. -/
theorem kernelCategoryRightMateBoundary_comp
    {F G : Pseudofunctor B C}
    {σ θ : Pseudofunctor.StrongTrans F G}
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y} {kG lG : G.obj X ⟶ G.obj Y}
    (q :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)))
    (r :
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨lF, lG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryRightMateBoundary dσ dθ Γ f (q ≫ r) =
      compressedMateRightBoundary dσ dθ Γ f
        (((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map q).1.trans
          ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map r).1,
         ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map q).2 ≫
         ((quotientCompositeFunctor (F.obj X) (F.obj Y)
          (G.obj X) (G.obj Y)).map r).2) := by
  rw [kernelCategoryRightMateBoundary_eq_compressed, Functor.map_comp]
  rfl

#print axioms kernelCategoryHomToKernelHom
#print axioms kernelCategoryHomToKernelHom_composite
#print axioms kernelCategoryLeftMateBoundary
#print axioms kernelCategoryRightMateBoundary
#print axioms kernelCategoryLeftMateBoundary_eq_compressed
#print axioms kernelCategoryRightMateBoundary_eq_compressed
#print axioms kernelCategoryMateNaturality
#print axioms kernelCategoryLeftMateBoundary_comp
#print axioms kernelCategoryRightMateBoundary_comp

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130
