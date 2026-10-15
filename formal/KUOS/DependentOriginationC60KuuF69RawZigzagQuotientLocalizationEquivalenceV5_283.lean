import KUOS.DependentOriginationC60KuuF69ZigzagKernelQuotientFreeGroupoidV5_282
import Mathlib.CategoryTheory.Localization.Construction
import Mathlib.CategoryTheory.PathCategory.Basic

namespace KUOS.DependentOriginationC60KuuF69RawZigzagQuotientLocalizationEquivalenceV5_283

open CategoryTheory
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279
open KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281
open KUOS.DependentOriginationC60KuuF69ZigzagKernelQuotientFreeGroupoidV5_282

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.283 / F112 stage 11 — full raw-zigzag localization presentation

The v5.282 kernel quotient of the REAL ORIGINAL F69 directed incidence
forward/backward words had a proved faithful functor into the true
Gabriel–Zisman localization. Faithfulness does NOT alone give
categorical equivalence. Here we discharge the missing FULLNESS and
ESSENTIAL SURJECTIVITY using the actual constructors of Mathlib's
localization path quiver, rather than assuming an abstract equivalence.

The old F69 original category stays a poset. The free F113 zigzag
still contains original, nonempty incidence/backtracking witnesses;
they are identified ONLY by an explicit categorical quotient.
This yields an equivalence of that *quotient* with the genuine old
F69 localization and hence the Mathlib FreeGroupoid, not an
equivalence of the raw unquotiented zigzag category.
No original source F42/F54/F55 global effective descent is asserted.
-/

/-! ## I. Decode the REAL original F69 localization path generators -/

/-- The precise mathlib quiver with FORWARD actual F69 Hom
and formally inverse copies of original arrows. -/
abbrev C60F117OriginalF69LocalizationQuiver :=
  Localization.Construction.LocQuiver
    (⊤ : MorphismProperty C60F69PhysicalCellSite)

/-- Every ACTUAL original F69 localization quiver generator has
a raw F113 representation with the original physical endpoints. -/
def c60F117LocalGeneratorToRawZigzag :
    C60F117OriginalF69LocalizationQuiver ⥤q C60F113ZigzagSite where
  obj X := ⟨X.obj⟩
  map := by
    intro X Y f
    rcases f with f | ⟨g, hg⟩
    · exact c60F116RawForward f
    · exact c60F116RawBackward g

/-- Every finite localizing-quiver path has a raw proof-carrying
original F69 forward/backward zigzag interpretation. -/
def c60F117LocalizationPathsToRawZigzag :
    Paths C60F117OriginalF69LocalizationQuiver ⥤
      C60F113ZigzagSite :=
  Paths.lift c60F117LocalGeneratorToRawZigzag

/-- Decoding original F69 localization generators and reencoding
them by the already constructed F113 source functor is EXACTLY
the canonical mathlib path-to-localization quotient functor.
This equality is on ENTIRE FUNCTORS, not just endpoint objects. -/
theorem c60F117LocalizationPaths_triangle :
    c60F117LocalizationPathsToRawZigzag ⋙
        c60F115F69ZigzagLocalizationFunctor =
      CategoryTheory.Quotient.functor
        (Localization.Construction.relations
          (⊤ : MorphismProperty C60F69PhysicalCellSite)) := by
  apply Paths.ext_functor
  · funext X
    rfl
  · intro X Y f
    rcases f with f | ⟨g, hg⟩
    · change
        c60F115F69ZigzagToLocalizationHom
          (c60F116RawForward f) =
        c60F115OriginalF69LocalizationQ.map f
      exact c60F116RawForward_localized f
    · change
        c60F115F69ZigzagToLocalizationHom
          (c60F116RawBackward g) =
        Localization.Construction.wInv
          (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
          g hg
      exact c60F116RawBackward_localized g

/-! ## II. Discharge FULLNESS and ESSENTIAL SURJECTIVITY, not assumptions -/

/-- Every Hom of the true old F69 localization has an ORIGINAL
proof-carrying F113 zigzag preimage. This directly uses the
actual quotient path representation of the localization. -/
instance c60F117RawF69ZigzagToLocalization_full :
    c60F115F69ZigzagLocalizationFunctor.Full where
  map_surjective := by
    rintro ⟨X⟩ ⟨Y⟩ f
    refine Quot.inductionOn f ?_
    intro p
    refine ⟨c60F117LocalizationPathsToRawZigzag.map p, ?_⟩
    have h := Functor.congr_hom c60F117LocalizationPaths_triangle p
    simpa only [Functor.comp_map] using h

/-- Every localized original physical F69 cell site comes
from a genuine old original vertex/edge/face site, with
no synthetic physical site introduced by the localization. -/
instance c60F117RawF69ZigzagToLocalization_essSurj :
    c60F115F69ZigzagLocalizationFunctor.EssSurj where
  mem_essImage Y :=
    ⟨(⟨Y.as.obj⟩ : C60F113ZigzagSite), ⟨eqToIso rfl⟩⟩

/-- Fullness passes to the exact localization-kernel quotient:
the same raw representative now descends via the quotient Q. -/
instance c60F117KernelLift_full :
    c60F116RawZigzagKernelLift.Full where
  map_surjective := by
    rintro ⟨X⟩ ⟨Y⟩ f
    obtain ⟨p, hp⟩ :=
      c60F117RawF69ZigzagToLocalization_full.map_surjective f
    refine ⟨c60F116RawZigzagKernelQ.map p, ?_⟩
    have h := Functor.congr_hom c60F116RawZigzagKernel_factors p
    exact (by simpa only [Functor.comp_map] using h).trans hp

/-- No genuine old physical F69 site is missed by the
exact localization-kernel quotient. -/
instance c60F117KernelLift_essSurj :
    c60F116RawZigzagKernelLift.EssSurj where
  mem_essImage Y :=
    ⟨c60F116RawZigzagKernelQ.obj
      (⟨Y.as.obj⟩ : C60F113ZigzagSite), ⟨eqToIso rfl⟩⟩

/-- The kernel quotient is FAITHFUL (v5.282), and now
FULL and essentially surjective from genuine old incidence
paths. Therefore the induced F69-localized representation
is a provable category EQUIVALENCE, not a claimed inversion
inside the original F69 poset or raw free zigzag syntax. -/
instance c60F117KernelLift_isEquivalence :
    c60F116RawZigzagKernelLift.IsEquivalence where
  faithful := c60F116RawZigzagKernelLift_faithful
  full := inferInstance
  essSurj := inferInstance

/-- MAIN THEOREM: the exact representation kernel quotient of
the F113 actual ORIGINAL F69 free zigzag category is genuinely
equivalent to the F69 Gabriel–Zisman localization. -/
def c60F117RawF69ZigzagKernelEquivalence :
    C60F116RawZigzagKernelQuotient ≌
      C60F115OriginalF69Localization :=
  c60F116RawZigzagKernelLift.asEquivalence

/-- And therefore this EXACT quotient of original F69 raw
incidence zigzags is equivalent to the Mathlib free groupoid
of the unchanged original directed F69 physical category. -/
def c60F117RawF69ZigzagFreeGroupoidEquivalence :
    C60F116RawZigzagKernelQuotient ≌
      C60F116OriginalF69FreeGroupoid :=
  c60F117RawF69ZigzagKernelEquivalence.trans
    c60F116OriginalF69FreeGroupoidEquivalence.symm

/-- All induced arrows in the quotient are interpreted by the
same original F69 localization functor; nothing is equated
before the explicitly named kernel quotient. -/
theorem c60F117ExactKernelEquivalence_triangle :
    c60F116RawZigzagKernelQ ⋙
        c60F117RawF69ZigzagKernelEquivalence.functor =
      c60F115F69ZigzagLocalizationFunctor :=
  c60F116RawZigzagKernel_factors

#print axioms c60F117LocalizationPaths_triangle
#print axioms c60F117RawF69ZigzagToLocalization_full
#print axioms c60F117RawF69ZigzagToLocalization_essSurj
#print axioms c60F117KernelLift_full
#print axioms c60F117KernelLift_essSurj
#print axioms c60F117KernelLift_isEquivalence
#print axioms c60F117RawF69ZigzagKernelEquivalence
#print axioms c60F117RawF69ZigzagFreeGroupoidEquivalence
#print axioms c60F117ExactKernelEquivalence_triangle

end
end KUOS.DependentOriginationC60KuuF69RawZigzagQuotientLocalizationEquivalenceV5_283
