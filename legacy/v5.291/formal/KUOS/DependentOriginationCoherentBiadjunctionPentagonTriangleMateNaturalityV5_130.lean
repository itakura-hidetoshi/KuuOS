import KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130

namespace KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic

set_option autoImplicit false
noncomputable section

/-!
# F33 / v5.130 — genuine F32 structural coherence is invisible to BOTH
unchanged F25 lax right-mate boundaries on real F28 quotient-category paths.

We precompose the LONG or SHORT native pentagon/triangle structural
pasting with an arbitrary actual F28 quotient arrow starting at the
ORIGINAL F.map f / G.map f. Its G comparison may be NONINVERTIBLE.
The equality of the two F32 pastings induces equality of BOTH original
mate boundaries. Separately, original F22 naturality identifies the
left mate boundary with the right boundary of the other route.

This is genuine compatibility at the level of original mate pastings,
rather than equality of anonymous quotient Hom representatives.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Right-mate boundary comparison for TWO independently composed
arrows in the genuine F28 quotient CATEGORY. Both full mate pastes
depend only on the resulting quotient arrow, and ORIGINAL mate
naturality also identifies the CROSS-boundary comparison. -/
theorem mateBoundaries_of_equal_quotient_postcomposition
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y} {kG lG : G.obj X ⟶ G.obj Y}
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)))
    (r s :
      (⟨⟨kF, kG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨lF, lG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)))
    (h : r = s) :
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ r) =
      kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ s) ∧
    kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ r) =
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ s) ∧
    kernelCategoryLeftMateBoundary dσ dθ Γ f (basePath ≫ r) =
      kernelCategoryRightMateBoundary dσ dθ Γ f (basePath ≫ s) := by
  subst s
  exact ⟨rfl, rfl, kernelCategoryMateNaturality dσ dθ Γ f (basePath ≫ r)⟩

/-- F32 PENTAGON transports BOTH ORIGINAL lax mate boundaries through
the 3-stage and 2-stage comparison pastes in the genuine F28 quotient.
The original basePath is fully arbitrary, including a noninvertible G cell. -/
theorem pentagonOriginalMateBoundaryCompatibility
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {bF cF dF bG cG dG : C}
    (uF : F.obj X ⟶ bF) (vF : bF ⟶ cF)
    (wF : cF ⟶ dF) (zF : dF ⟶ F.obj Y)
    (uG : G.obj X ⟶ bG) (vG : bG ⟶ cG)
    (wG : cG ⟶ dG) (zG : dG ⟶ G.obj Y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨(((uF ≫ vF) ≫ wF) ≫ zF), (((uG ≫ vG) ≫ wG) ≫ zG)⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryLeftMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom) =
    kernelCategoryLeftMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom) ∧
    kernelCategoryRightMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom) =
    kernelCategoryRightMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom) ∧
    kernelCategoryLeftMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom) =
    kernelCategoryRightMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom) := by
  exact mateBoundaries_of_equal_quotient_postcomposition dσ dθ Γ f basePath
    (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom
    (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom
    (congrArg Iso.hom (kernelQuotientPentagon uF vF wF zF uG vG wG zG))

/-- F32 TRIANGLE transports BOTH ORIGINAL lax mate boundaries through
the 2-stage associator/left-unitor paste and the whiskered right-unitor
paste. The basePath retains its arbitrary G-side comparison direction. -/
theorem triangleOriginalMateBoundaryCompatibility
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {bF bG : C}
    (uF : F.obj X ⟶ bF) (vF : bF ⟶ F.obj Y)
    (uG : G.obj X ⟶ bG) (vG : bG ⟶ G.obj Y)
    (basePath :
      (⟨⟨F.map f, G.map f⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)) ⟶
      (⟨⟨(uF ≫ 𝟙 bF) ≫ vF, (uG ≫ 𝟙 bG) ≫ vG⟩⟩ :
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y))) :
    kernelCategoryLeftMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom) =
    kernelCategoryLeftMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom) ∧
    kernelCategoryRightMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom) =
    kernelCategoryRightMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom) ∧
    kernelCategoryLeftMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom) =
    kernelCategoryRightMateBoundary dσ dθ Γ f
      (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom) := by
  exact mateBoundaries_of_equal_quotient_postcomposition dσ dθ Γ f basePath
    (kernelTriangleLongIso uF vF uG vG).hom
    (kernelTriangleShortIso uF vF uG vG).hom
    (congrArg Iso.hom (kernelQuotientTriangle uF vF uG vG))

#print axioms mateBoundaries_of_equal_quotient_postcomposition
#print axioms pentagonOriginalMateBoundaryCompatibility
#print axioms triangleOriginalMateBoundaryCompatibility

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130
