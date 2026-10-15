import KUOS.DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280
import Mathlib.CategoryTheory.Localization.Predicate

namespace KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278
open KUOS.DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279
open KUOS.DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.281 / F112 ninth stage — actual localization and unique F47 factorization

There are THREE DIFFERENT typed categories in this development:
* original physical F69 incidence POSSET: only genuine oriented incidences;
* F113 FREE INCIDENCE ZIGZAG: actual old incidence inequalities and
  FORMAL reverse generators, without cancellation or functor laws imposed;
* the genuine mathlib Gabriel–Zisman LOCALIZATION of the ORIGINAL F69
  incidence category at all old arrows, where formal inverses and
  composition/identity relations are imposed by a quotient.

A raw formal zigzag is NOT an arrow of the original F69 poset.
Its canonical interpretation in the localization DOES respect its
own raw concatenation, but is NOT an isomorphism of free path categories:
identity generators and backtracking remain distinct in the raw syntax.

Independently, the proven original F47 mixed source Cat diagram on the
real witnessed physical-overlap path category INVERTS every witnessed
arrow via v5.280 reverse-source functors. Thus it FACTORS UNIQUELY
through the mathlib localization of this actual witnessed category.
Both Int charges and the independent ZMod2 phase remain untouched.

The localized original F69 incidence geometry and the localized
witnessed F47 diagram are explicitly distinct. NO Cat-valued
functor on all old F69 vertices/edges/faces is invented, and we
do not claim global effective F42/F54/F55 source descent.
F55 Delta non-lift, F110 phase non-reconstruction, and F68
signed north-pentagon curvature -5 remain unaffected.
-/

/-! ## I. The ACTUAL old F69 category localized at its old arrows -/

/-- Gabriel–Zisman localization of the UNCHANGED original
C60 F69 vertex/edge/face incidence category, at ALL old arrows. -/
abbrev C60F115OriginalF69Localization :=
  (⊤ : MorphismProperty C60F69PhysicalCellSite).Localization

/-- The old incidence poset embeds by a genuine localization functor,
not by the fiction that opposite incidences already exist. -/
def c60F115OriginalF69LocalizationQ :
    C60F69PhysicalCellSite ⥤ C60F115OriginalF69Localization :=
  (⊤ : MorphismProperty C60F69PhysicalCellSite).Q

/-- The ORIGINAL F69 localization has actual mathlib universality. -/
theorem c60F115OriginalF69Localization_universal :
    c60F115OriginalF69LocalizationQ.IsLocalization
      (⊤ : MorphismProperty C60F69PhysicalCellSite) := by
  change ((⊤ : MorphismProperty C60F69PhysicalCellSite).Q).IsLocalization _
  infer_instance

universe uT vT
variable {T : Type uT} [Category.{vT} T]

/-- Strict factorization for EVERY functor on old F69 sites
inverting every old actual incidence arrow. -/
theorem c60F115OriginalF69Localization_factor
    (F : C60F69PhysicalCellSite ⥤ T)
    (hF : (⊤ : MorphismProperty C60F69PhysicalCellSite).IsInvertedBy F) :
    c60F115OriginalF69LocalizationQ ⋙
      Localization.Construction.lift F hF = F := by
  exact Localization.Construction.fac F hF

/-- STRICT uniqueness of the localized extension, not merely
an existence of mutually inverse generators. -/
theorem c60F115OriginalF69Localization_unique
    (F G : C60F115OriginalF69Localization ⥤ T)
    (h : c60F115OriginalF69LocalizationQ ⋙ F =
      c60F115OriginalF69LocalizationQ ⋙ G) : F = G :=
  Localization.Construction.uniq F G h

/-! ## II. Genuine old F69 forward/reverse zigzags enter localization -/

/-- Interpret EACH formally oriented genuine old F69 incidence
leg as a morphism in the honest localization. Backward legs
use the canonical localization inverse, NEVER an old F69 arrow. -/
def c60F115F69ZigzagToLocalizationHom
    {s t : C60F69PhysicalCellSite} :
    C60F113IncidenceZigzag s t →
      (c60F115OriginalF69LocalizationQ.obj s ⟶
        c60F115OriginalF69LocalizationQ.obj t)
  | .nil _ => 𝟙 _
  | .forward h rest =>
      c60F115OriginalF69LocalizationQ.map (homOfLE h) ≫
        c60F115F69ZigzagToLocalizationHom rest
  | .backward h rest =>
      Localization.Construction.wInv
        (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
        (homOfLE h) (by trivial) ≫
        c60F115F69ZigzagToLocalizationHom rest

/-- Reinterpretation respects arbitrary concatenation of
actual F69-oriented zigzag words. -/
theorem c60F115F69ZigzagToLocalization_append
    {s t u : C60F69PhysicalCellSite}
    (p : C60F113IncidenceZigzag s t)
    (q : C60F113IncidenceZigzag t u) :
    c60F115F69ZigzagToLocalizationHom
        (c60F113ZigzagAppend p q) =
      c60F115F69ZigzagToLocalizationHom p ≫
        c60F115F69ZigzagToLocalizationHom q := by
  induction p with
  | nil _ =>
      change c60F115F69ZigzagToLocalizationHom q =
        𝟙 _ ≫ c60F115F69ZigzagToLocalizationHom q
      exact (Category.id_comp _).symm
  | forward h rest ih =>
      change
        c60F115OriginalF69LocalizationQ.map (homOfLE h) ≫
          c60F115F69ZigzagToLocalizationHom
            (c60F113ZigzagAppend rest q) =
        (c60F115OriginalF69LocalizationQ.map (homOfLE h) ≫
          c60F115F69ZigzagToLocalizationHom rest) ≫
          c60F115F69ZigzagToLocalizationHom q
      rw [ih]
      exact (Category.assoc _ _ _).symm
  | backward h rest ih =>
      change
        Localization.Construction.wInv
            (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
            (homOfLE h) (by trivial) ≫
          c60F115F69ZigzagToLocalizationHom
            (c60F113ZigzagAppend rest q) =
        (Localization.Construction.wInv
            (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
            (homOfLE h) (by trivial) ≫
          c60F115F69ZigzagToLocalizationHom rest) ≫
          c60F115F69ZigzagToLocalizationHom q
      rw [ih]
      exact (Category.assoc _ _ _).symm

/-- The genuine ORIGINAL incidence-based free zigzag category
maps to the LOCALIZED old F69 category: there is still no
site-preserving projection into the UNLOCALIZED old F69 poset. -/
def c60F115F69ZigzagLocalizationFunctor :
    C60F113ZigzagSite ⥤ C60F115OriginalF69Localization where
  obj X := c60F115OriginalF69LocalizationQ.obj X.site
  map := fun {_ _} p => c60F115F69ZigzagToLocalizationHom p
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z p q
    exact c60F115F69ZigzagToLocalization_append p q

/-- A synthetic OLD F69 reflexive generator remains nonempty
in the raw free zigzag category: old F69 identity laws have
not been silently imposed at the syntax level. -/
theorem c60F115RawF69IdentityLeg_nonempty
    (s : C60F69PhysicalCellSite) :
    C60F113IncidenceZigzag.forward (le_refl s)
        (C60F113IncidenceZigzag.nil s) ≠
      C60F113IncidenceZigzag.nil s := by
  intro h
  cases h

/-- This same raw one-leg F69 reflexivity becomes identity
ONLY in the actual localized category. -/
theorem c60F115OriginalF69ReflexiveLeg_localized
    (s : C60F69PhysicalCellSite) :
    c60F115F69ZigzagToLocalizationHom
        (C60F113IncidenceZigzag.forward (le_refl s)
          (C60F113IncidenceZigzag.nil s)) =
      𝟙 (c60F115OriginalF69LocalizationQ.obj s) := by
  have hid : (homOfLE (le_refl s) : s ⟶ s) = 𝟙 s :=
    Subsingleton.elim _ _
  change c60F115OriginalF69LocalizationQ.map
      (homOfLE (le_refl s)) ≫ 𝟙 _ = 𝟙 _
  rw [hid, Functor.map_id, Category.id_comp]

/-- Two REAL physical-edge overlap legs pass through their
original common F69 vertex or face inside the localization. -/
def c60F115WitnessedToOriginalF69Localization
    {n : Nat} (C : C60F108BothFaceContexts n) :
    C60F112WitnessedEdge C ⥤ C60F115OriginalF69Localization :=
  c60F113WitnessedToF69Zigzag C ⋙
    c60F115F69ZigzagLocalizationFunctor

/-! ## III. The witnessed original full-phase F47 diagram localizes -/

abbrev C60F115WitnessedLocalization
    {n : Nat} (C : C60F108BothFaceContexts n) :=
  (⊤ : MorphismProperty (C60F112WitnessedEdge C)).Localization

def c60F115WitnessedLocalizationQ
    {n : Nat} (C : C60F108BothFaceContexts n) :
    C60F112WitnessedEdge C ⥤ C60F115WitnessedLocalization C :=
  (⊤ : MorphismProperty (C60F112WitnessedEdge C)).Q

theorem c60F115WitnessedLocalization_universal
    {n : Nat} (C : C60F108BothFaceContexts n) :
    (c60F115WitnessedLocalizationQ C).IsLocalization
      (⊤ : MorphismProperty (C60F112WitnessedEdge C)) := by
  change (((⊤ : MorphismProperty (C60F112WitnessedEdge C)).Q)).IsLocalization _
  infer_instance

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalF47Localization
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- Every REAL witnessed physical overlap path maps to an
ISOMORPHISM of ORIGINAL F47 source quotient categories in Cat.
The proof uses both v5.280 literal round-trip identities and
does not erase either integer charge or the ZMod2 phase. -/
theorem c60F115WitnessedF47Diagram_inverts
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    (⊤ : MorphismProperty (C60F112WitnessedEdge C)).IsInvertedBy
      (c60F112WitnessedF47Diagram t₁ t₂ left right C P) := by
  intro X Y p hp
  change IsIso
    ((c60F112WitnessedF47Transport t₁ t₂ left right C P p).toCatHom)
  refine ⟨⟨(c60F112WitnessedF47Transport t₁ t₂ left right C P
      (c60F114ReverseWitnessedPath p)).toCatHom, ?_, ?_⟩⟩
  · apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor,
      Cat.Hom.id_toFunctor] using
      (c60F114WitnessedF47RoundTrip_rightInverse
        t₁ t₂ left right C P p)
  · apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor,
      Cat.Hom.id_toFunctor] using
      (c60F114WitnessedF47RoundTrip_leftInverse
        t₁ t₂ left right C P p)

/-- The exact ORIGINAL source-F47 Cat-valued diagram factors
through the localization of the WITNESSED path category. -/
def c60F115LocalizedOriginalF47Diagram
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    C60F115WitnessedLocalization C ⥤ Cat :=
  Localization.Construction.lift
    (c60F112WitnessedF47Diagram t₁ t₂ left right C P)
    (c60F115WitnessedF47Diagram_inverts t₁ t₂ left right C P)

/-- STRICT factorization on the genuine Cat-valued original
F47 diagram, preserving the two integer charges and phase. -/
theorem c60F115OriginalF47Localization_factors
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F115WitnessedLocalizationQ C ⋙
      c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P =
        c60F112WitnessedF47Diagram t₁ t₂ left right C P := by
  exact Localization.Construction.fac
    (c60F112WitnessedF47Diagram t₁ t₂ left right C P)
    (c60F115WitnessedF47Diagram_inverts t₁ t₂ left right C P)

/-- ANY OTHER strict localized F47 diagram extending the exact
old source functor is EQUAL to the uniquely constructed lift.
In particular this is a UNIVERSAL PROPERTY, not a raw path
cancellation convention. -/
theorem c60F115OriginalF47Localization_unique
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (F : C60F115WitnessedLocalization C ⥤ Cat)
    (hF : c60F115WitnessedLocalizationQ C ⋙ F =
      c60F112WitnessedF47Diagram t₁ t₂ left right C P) :
    F = c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P := by
  apply Localization.Construction.uniq
  rw [hF, c60F115OriginalF47Localization_factors]

#check c60F113NoOriginalIncidenceProjection
#check c60F112WitnessedF47Path_originalF55Nonlift
#check c60F112WitnessedF47Total_originalCurvatureObstruction

#print axioms c60F115OriginalF69Localization_universal
#print axioms c60F115OriginalF69Localization_factor
#print axioms c60F115OriginalF69Localization_unique
#print axioms c60F115F69ZigzagToLocalization_append
#print axioms c60F115F69ZigzagLocalizationFunctor
#print axioms c60F115RawF69IdentityLeg_nonempty
#print axioms c60F115OriginalF69ReflexiveLeg_localized
#print axioms c60F115WitnessedLocalization_universal
#print axioms c60F115WitnessedF47Diagram_inverts
#print axioms c60F115OriginalF47Localization_factors
#print axioms c60F115OriginalF47Localization_unique

end OriginalF47Localization
end
end KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281
