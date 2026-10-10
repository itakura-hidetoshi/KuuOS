import KUOS.DependentOriginationCoherentBiadjunctionActualLiftNonstrictKernelV5_126

namespace KUOS.DependentOriginationCoherentBiadjunctionQuotientCategoryCompatibilityV5_126

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic

set_option autoImplicit false
noncomputable section

/-!
# F29 / v5.126: compatibility in the actual F28 quotient CATEGORY

The original F25 mapId/mapComp chain arrows are first sent through the
actual mathlib quotient-category functor and then through the F28
equivalence's forward functor. Their image is precisely their full F-ISO
and (possibly noninvertible) G comparison composite.

Whiskering of the resulting cells respects equality of real quotient
category arrows, not only equality of artificially selected paths.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}

/-- Nonstrict original mapId compares correctly after passage through
the genuine F28 quotient-category functor and its equivalence. -/
theorem originalMapIdQuotientCategory_compression (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (tail : BiComparisonChain (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :
    (quotientCompositeFunctor (F.obj X) (F.obj X)
      (G.obj X) (G.obj X)).map
      ((comparisonKernelQuotientFunctor (F.obj X) (F.obj X)
        (G.obj X) (G.obj X)).map
          (X := ⟨F.map (𝟙 X), G.map (𝟙 X)⟩)
          (Y := ⟨kF, kG⟩)
          (originalMapIdFiniteChain (F := F) (G := G) X tail)) =
      ((F.mapId X).trans tail.fComposite,
       G.toOplax.mapId X ≫ tail.gComposite) := by
  change
    ((comparisonKernelQuotientFunctor (F.obj X) (F.obj X)
        (G.obj X) (G.obj X) ⋙
      quotientCompositeFunctor (F.obj X) (F.obj X)
        (G.obj X) (G.obj X)).map
      (X := ⟨F.map (𝟙 X), G.map (𝟙 X)⟩)
      (Y := ⟨kF, kG⟩)
      (originalMapIdFiniteChain (F := F) (G := G) X tail)) =
      ((F.mapId X).trans tail.fComposite,
       G.toOplax.mapId X ≫ tail.gComposite)
  rw [compression_factors_through_kernel_quotient]
  exact Prod.ext
    (originalMapIdPrepend_composites (F := F) (G := G) X tail).1
    (originalMapIdPrepend_composites (F := F) (G := G) X tail).2

/-- Genuine mapComp and its noninvertible G component agree with
compression THROUGH the quotient CATEGORY, including arbitrary tails. -/
theorem originalMapCompQuotientCategory_compression
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (tail : BiComparisonChain (F.map f ≫ F.map g)
      (G.map f ≫ G.map g) kF kG) :
    (quotientCompositeFunctor (F.obj X) (F.obj Z)
      (G.obj X) (G.obj Z)).map
      ((comparisonKernelQuotientFunctor (F.obj X) (F.obj Z)
        (G.obj X) (G.obj Z)).map
          (X := ⟨F.map (f ≫ g), G.map (f ≫ g)⟩)
          (Y := ⟨kF, kG⟩)
          (originalMapCompFiniteChain (F := F) (G := G) f g tail)) =
      ((F.mapComp f g).trans tail.fComposite,
       G.toOplax.mapComp f g ≫ tail.gComposite) := by
  change
    ((comparisonKernelQuotientFunctor (F.obj X) (F.obj Z)
        (G.obj X) (G.obj Z) ⋙
      quotientCompositeFunctor (F.obj X) (F.obj Z)
        (G.obj X) (G.obj Z)).map
      (X := ⟨F.map (f ≫ g), G.map (f ≫ g)⟩)
      (Y := ⟨kF, kG⟩)
      (originalMapCompFiniteChain (F := F) (G := G) f g tail)) =
      ((F.mapComp f g).trans tail.fComposite,
       G.toOplax.mapComp f g ≫ tail.gComposite)
  rw [compression_factors_through_kernel_quotient]
  exact Prod.ext
    (originalMapCompPrepend_composites (F := F) (G := G) f g tail).1
    (originalMapCompPrepend_composites (F := F) (G := G) f g tail).2

/-- Equality of ACTUAL F28 quotient-category arrows preserves left
whiskering of the F ISO and arbitrary G 2-cell alike. -/
theorem quotientCategoryLeftWhiskering_respects_eq
    (aF bF aG bG : C)
    {a b : ComparisonPair aF bF aG bG} (c₁ c₂ : a ⟶ b)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (h : (comparisonKernelQuotientFunctor aF bF aG bG).map c₁ =
      (comparisonKernelQuotientFunctor aF bF aG bG).map c₂) :
    (Bicategory.whiskerLeftIso uF c₁.fComposite,
      uG ◁ c₁.gComposite) =
    (Bicategory.whiskerLeftIso uF c₂.fComposite,
      uG ◁ c₂.gComposite) := by
  obtain ⟨hf, hg⟩ :=
    (kernelQuotient_map_eq_iff aF bF aG bG c₁ c₂).mp h
  exact Prod.ext
    (congrArg (fun p => Bicategory.whiskerLeftIso uF p) hf)
    (congrArg (fun q => uG ◁ q) hg)

/-- Equality of genuine quotient-category arrows also preserves right
whiskering, with no G-side inverse or strict interchange assumption. -/
theorem quotientCategoryRightWhiskering_respects_eq
    (aF bF aG bG : C)
    {a b : ComparisonPair aF bF aG bG} (c₁ c₂ : a ⟶ b)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (h : (comparisonKernelQuotientFunctor aF bF aG bG).map c₁ =
      (comparisonKernelQuotientFunctor aF bF aG bG).map c₂) :
    (Bicategory.whiskerRightIso c₁.fComposite vF,
      c₁.gComposite ▷ vG) =
    (Bicategory.whiskerRightIso c₂.fComposite vF,
      c₂.gComposite ▷ vG) := by
  obtain ⟨hf, hg⟩ :=
    (kernelQuotient_map_eq_iff aF bF aG bG c₁ c₂).mp h
  exact Prod.ext
    (congrArg (fun p => Bicategory.whiskerRightIso p vF) hf)
    (congrArg (fun q => q ▷ vG) hg)

#print axioms originalMapIdQuotientCategory_compression
#print axioms originalMapCompQuotientCategory_compression
#print axioms quotientCategoryLeftWhiskering_respects_eq
#print axioms quotientCategoryRightWhiskering_respects_eq

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionQuotientCategoryCompatibilityV5_126
