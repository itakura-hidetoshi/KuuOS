import Kuu.F112.Localization
import Mathlib.CategoryTheory.Localization.Construction
import Mathlib.CategoryTheory.PathCategory.Basic

/-!
# F112 / FULL exact raw-zigzag kernel quotient over true C60 physical sites

Faithfulness of the kernel quotient's representation is not enough. Decode
each of pinned Mathlib's localization-quiver generators into genuinely
physical forward/backward F69 incidence zigzags. Fullness and essential
surjectivity then yield a genuine equivalence of the *exact quotient*
with the true localized original physical-incidence category.
No equivalence of uncancelled raw words is asserted.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

abbrev PhysicalLocalizationQuiver :=
  Localization.Construction.LocQuiver (⊤ : MorphismProperty Site)

/-- Each genuine Mathlib localization-quiver generator is one of our
proof-relevant incidence legs, or one formally reversed incidence leg. -/
def localizationGeneratorToRaw : PhysicalLocalizationQuiver ⥤q ZigzagSite where
  obj X := ⟨X.obj⟩
  map := by
    intro X Y f
    rcases f with f | ⟨g, hg⟩
    · exact forward f
    · exact backward g

/-- Arbitrary finite paths decode to real typed physical zigzag words. -/
def localizationPathsToRaw :
    Paths PhysicalLocalizationQuiver ⥤ ZigzagSite :=
  Paths.lift localizationGeneratorToRaw

/-- The *entire* functor from localization paths is the native Mathlib
path-to-localization quotient; not merely an objectwise agreement. -/
theorem localizationPaths_triangle :
    localizationPathsToRaw ⋙ zigzagLocalizationFunctor =
      CategoryTheory.Quotient.functor
        (Localization.Construction.relations (⊤ : MorphismProperty Site)) := by
  refine Paths.ext_functor rfl ?_
  intro X Y f
  rcases f with f | ⟨g, hg⟩
  · change zigzagToLocalization (forward f) = siteLocalizationQ.map f
    exact rawForward_localized f
  · change zigzagToLocalization (backward g) =
      Localization.Construction.wInv (W := (⊤ : MorphismProperty Site)) g hg
    exact rawBackward_localized g

instance zigzagLocalization_full : zigzagLocalizationFunctor.Full where
  map_surjective := by
    rintro ⟨X⟩ ⟨Y⟩ f
    refine Quot.inductionOn f ?_
    intro p
    refine ⟨localizationPathsToRaw.map p, ?_⟩
    have h := Functor.congr_hom localizationPaths_triangle p
    change
      zigzagLocalizationFunctor.map (localizationPathsToRaw.map p) =
        𝟙 _ ≫ (CategoryTheory.Quotient.functor
          (Localization.Construction.relations
            (⊤ : MorphismProperty Site))).map p ≫ 𝟙 _ at h
    simpa only [Category.id_comp, Category.comp_id] using h

instance zigzagLocalization_essSurj : zigzagLocalizationFunctor.EssSurj where
  mem_essImage Y :=
    ⟨(⟨Y.as.obj⟩ : ZigzagSite), ⟨eqToIso rfl⟩⟩

instance zigzagKernelLift_full : zigzagKernelLift.Full where
  map_surjective := by
    rintro ⟨X⟩ ⟨Y⟩ f
    obtain ⟨p, hp⟩ := zigzagLocalization_full.map_surjective f
    refine ⟨zigzagKernelQ.map p, ?_⟩
    have h := Functor.congr_hom zigzagKernel_factors p
    have hc :
        zigzagKernelLift.map (zigzagKernelQ.map p) =
          zigzagLocalizationFunctor.map p := by
      change
        zigzagKernelLift.map (zigzagKernelQ.map p) =
          𝟙 _ ≫ zigzagLocalizationFunctor.map p ≫ 𝟙 _ at h
      simpa only [Category.id_comp, Category.comp_id] using h
    exact hc.trans hp

instance zigzagKernelLift_essSurj : zigzagKernelLift.EssSurj where
  mem_essImage Y :=
    ⟨zigzagKernelQ.obj (⟨Y.as.obj⟩ : ZigzagSite), ⟨eqToIso rfl⟩⟩

instance zigzagKernelLift_isEquivalence : zigzagKernelLift.IsEquivalence where
  faithful := zigzagKernelLift_faithful
  full := inferInstance
  essSurj := inferInstance

/-- The exact relation kernel quotient is equivalent to the genuine
localization of original C60 F69. Raw zigzag remains distinct! -/
def zigzagKernelEquivalence :
    ZigzagKernelQuotient ≌ PhysicalLocalization :=
  zigzagKernelLift.asEquivalence

/-- Thus the exact quotient also represents the original physical
incidence category's Mathlib free groupoid completion. -/
def zigzagFreeGroupoidEquivalence :
    ZigzagKernelQuotient ≌ PhysicalFreeGroupoid :=
  zigzagKernelEquivalence.trans physicalFreeGroupoidEquivalence.symm

theorem zigzagKernelEquivalence_triangle :
    zigzagKernelQ ⋙ zigzagKernelEquivalence.functor =
      zigzagLocalizationFunctor :=
  zigzagKernel_factors

#print axioms localizationPaths_triangle
#print axioms zigzagLocalization_full
#print axioms zigzagLocalization_essSurj
#print axioms zigzagKernelLift_full
#print axioms zigzagKernelLift_essSurj
#print axioms zigzagKernelLift_isEquivalence
#print axioms zigzagKernelEquivalence
#print axioms zigzagFreeGroupoidEquivalence
#print axioms zigzagKernelEquivalence_triangle

end
end Kuu.F112.Physical
