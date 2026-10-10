import KUOS.DependentOriginationCoherentBiadjunctionActualLiftF33MateCoherenceV5_130

namespace KUOS.DependentOriginationCoherentBiadjunctionF33HorizontalMateWhiskeringV5_130

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientPentagonTriangleV5_129.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientMateBoundaryBridgeV5_130.Generic
open KUOS.DependentOriginationCoherentBiadjunctionPentagonTriangleMateNaturalityV5_130.Generic

set_option autoImplicit false
noncomputable section

/-!
# F33 / v5.130 — external horizontal whiskering preserves BOTH mate
boundaries across the ORIGINAL F32 quotient pentagon and triangle.

F30 independently supplies true left/right whiskering FUNCTORS on the
F28 comparison-kernel quotient categories. The original F32 long and
short coherence pastings remain equal after these actual functor maps.

F21 supplies genuine horizontal whiskering of the original lax mate
modification. We also prove that external whiskering of the WHOLE
original F25/F33 left and right mate boundary pastes preserves the
cross-route equality. This is NOT a new equality between independently
whiskered source pseudofunctors; the original F/G, eta/epsilon and lax
right-mate data remain fixed.
-/

namespace Generic

universe uC vC wC uB vB wB
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {B : Type uB} [Bicategory.{wB, vB} B]

/-- The F32 PENTAGON pastes remain equal after mapping through the
ACTUAL F30 left horizontal quotient functor, with the G-comparison
arrows still allowed to be noninvertible. -/
theorem pentagonF30LeftWhiskeringCoherence
    {aF bF cF dF eF aG bG cG dG eG : C}
    (uF : aF ⟶ bF) (vF : bF ⟶ cF) (wF : cF ⟶ dF) (zF : dF ⟶ eF)
    (uG : aG ⟶ bG) (vG : bG ⟶ cG) (wG : cG ⟶ dG) (zG : dG ⟶ eG)
    {pF pG : C} (outerF : pF ⟶ aF) (outerG : pG ⟶ aG) :
    (leftKernelQuotientWhiskerFunctor aF eF aG eG outerF outerG).map
      (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom =
    (leftKernelQuotientWhiskerFunctor aF eF aG eG outerF outerG).map
      (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom := by
  exact congrArg
    (fun t => (leftKernelQuotientWhiskerFunctor aF eF aG eG outerF outerG).map t)
    (congrArg Iso.hom (kernelQuotientPentagon uF vF wF zF uG vG wG zG))

/-- The F32 TRIANGLE remains equal after mapping through the actual
F30 RIGHT horizontal quotient functor, on both F and G components. -/
theorem triangleF30RightWhiskeringCoherence
    {aF bF cF aG bG cG : C}
    (uF : aF ⟶ bF) (vF : bF ⟶ cF)
    (uG : aG ⟶ bG) (vG : bG ⟶ cG)
    {pF pG : C} (outerF : cF ⟶ pF) (outerG : cG ⟶ pG) :
    (rightKernelQuotientWhiskerFunctor aF cF aG cG outerF outerG).map
      (kernelTriangleLongIso uF vF uG vG).hom =
    (rightKernelQuotientWhiskerFunctor aF cF aG cG outerF outerG).map
      (kernelTriangleShortIso uF vF uG vG).hom := by
  exact congrArg
    (fun t => (rightKernelQuotientWhiskerFunctor aF cF aG cG outerF outerG).map t)
    (congrArg Iso.hom (kernelQuotientTriangle uF vF uG vG))

variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The full ORIGINAL F25 left mate boundary of the long F32
pentagon and the original RIGHT mate boundary of the short route
remain equal after independent OUTER horizontal left/right whiskering
of their complete 2-cell pastes. The original G cell is not inverted. -/
theorem pentagonOriginalMateBoundary_whiskerBoth
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
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)))
    {e e' : C} (outerLeft : e ⟶ G.obj X) (outerRight : F.obj Y ⟶ e') :
    (outerLeft ◁ kernelCategoryLeftMateBoundary dσ dθ Γ f
        (basePath ≫ (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom)) ▷ outerRight =
    (outerLeft ◁ kernelCategoryRightMateBoundary dσ dθ Γ f
        (basePath ≫ (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom)) ▷ outerRight := by
  exact congrArg (fun t => (outerLeft ◁ t) ▷ outerRight)
    (pentagonOriginalMateBoundaryCompatibility dσ dθ Γ f
      uF vF wF zF uG vG wG zG basePath).2.2

/-- The same TWO external whiskers preserve the original F25/F33
lax right-mate equality across the F32 TRIANGLE, without demanding
G-side comparison isomorphisms or identifying nonstrict mapId cells. -/
theorem triangleOriginalMateBoundary_whiskerBoth
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
        compressionKernelCategory (F.obj X) (F.obj Y) (G.obj X) (G.obj Y)))
    {e e' : C} (outerLeft : e ⟶ G.obj X) (outerRight : F.obj Y ⟶ e') :
    (outerLeft ◁ kernelCategoryLeftMateBoundary dσ dθ Γ f
        (basePath ≫ (kernelTriangleLongIso uF vF uG vG).hom)) ▷ outerRight =
    (outerLeft ◁ kernelCategoryRightMateBoundary dσ dθ Γ f
        (basePath ≫ (kernelTriangleShortIso uF vF uG vG).hom)) ▷ outerRight := by
  exact congrArg (fun t => (outerLeft ◁ t) ▷ outerRight)
    (triangleOriginalMateBoundaryCompatibility dσ dθ Γ f
      uF vF uG vG basePath).2.2

/-- F32 pentagon structural paths agree after the ACTUAL F30
right horizontal functor as well: both orientations, including G's
arbitrary comparison direction, are preserved by the quotient map. -/
theorem pentagonF30RightWhiskeringCoherence
    {aF bF cF dF eF aG bG cG dG eG : C}
    (uF : aF ⟶ bF) (vF : bF ⟶ cF) (wF : cF ⟶ dF) (zF : dF ⟶ eF)
    (uG : aG ⟶ bG) (vG : bG ⟶ cG) (wG : cG ⟶ dG) (zG : dG ⟶ eG)
    {pF pG : C} (outerF : eF ⟶ pF) (outerG : eG ⟶ pG) :
    (rightKernelQuotientWhiskerFunctor aF eF aG eG outerF outerG).map
      (kernelPentagonLongIso uF vF wF zF uG vG wG zG).hom =
    (rightKernelQuotientWhiskerFunctor aF eF aG eG outerF outerG).map
      (kernelPentagonShortIso uF vF wF zF uG vG wG zG).hom := by
  exact congrArg
    (fun t => (rightKernelQuotientWhiskerFunctor aF eF aG eG outerF outerG).map t)
    (congrArg Iso.hom (kernelQuotientPentagon uF vF wF zF uG vG wG zG))

/-- The other F30 horizontal direction: the F32 triangle also
commutes with true LEFT whiskering of native kernel quotient arrows. -/
theorem triangleF30LeftWhiskeringCoherence
    {aF bF cF aG bG cG : C}
    (uF : aF ⟶ bF) (vF : bF ⟶ cF)
    (uG : aG ⟶ bG) (vG : bG ⟶ cG)
    {pF pG : C} (outerF : pF ⟶ aF) (outerG : pG ⟶ aG) :
    (leftKernelQuotientWhiskerFunctor aF cF aG cG outerF outerG).map
      (kernelTriangleLongIso uF vF uG vG).hom =
    (leftKernelQuotientWhiskerFunctor aF cF aG cG outerF outerG).map
      (kernelTriangleShortIso uF vF uG vG).hom := by
  exact congrArg
    (fun t => (leftKernelQuotientWhiskerFunctor aF cF aG cG outerF outerG).map t)
    (congrArg Iso.hom (kernelQuotientTriangle uF vF uG vG))

#print axioms pentagonF30LeftWhiskeringCoherence
#print axioms pentagonF30RightWhiskeringCoherence
#print axioms triangleF30LeftWhiskeringCoherence
#print axioms triangleF30RightWhiskeringCoherence
#print axioms pentagonOriginalMateBoundary_whiskerBoth
#print axioms triangleOriginalMateBoundary_whiskerBoth

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionF33HorizontalMateWhiskeringV5_130
