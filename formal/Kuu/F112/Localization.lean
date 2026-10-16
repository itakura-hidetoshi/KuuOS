import Kuu.F112.Zigzag
import Mathlib.CategoryTheory.Localization.Predicate
import Mathlib.CategoryTheory.Quotient

/-!
# F112 / genuine original C60 incidence zigzag localization (independent)

The actual Site is a physical incidence POSSET with its original oriented
arrows. ZigzagSite is a different freely generated category of typed original
incidence legs and formal inverses. The Gabriel–Zisman localization imposes
the inverse/identity laws and the exact kernel quotient. No original raw
F42/F54/F55 cells or Gray observations are identified in this construction.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- The actual original 60/90/32 physical incidence category's localization. -/
def siteLocalizationQ : Site ⥤ PhysicalLocalization :=
  (⊤ : MorphismProperty Site).Q

theorem siteLocalization_universal :
    siteLocalizationQ.IsLocalization (⊤ : MorphismProperty Site) := by
  change ((⊤ : MorphismProperty Site).Q).IsLocalization _
  infer_instance

universe uT vT
variable {T : Type uT} [Category.{vT} T]

/-- Every functor inverting real physical incidence morphisms factors
through this localization; this does not invert arrows inside Site. -/
theorem siteLocalization_factor
    (F : Site ⥤ T)
    (hF : (⊤ : MorphismProperty Site).IsInvertedBy F) :
    siteLocalizationQ ⋙ Localization.Construction.lift F hF = F :=
  Localization.Construction.fac F hF

theorem siteLocalization_unique
    (F G : PhysicalLocalization ⥤ T)
    (h : siteLocalizationQ ⋙ F = siteLocalizationQ ⋙ G) :
    F = G := Localization.Construction.uniq F G h

/-- Each *raw* formal incidence leg has a genuinely typed interpretation
in the actual Gabriel–Zisman localization of the real C60 geometry. -/
def zigzagToLocalization {s t : Site} :
    Zigzag s t →
      (siteLocalizationQ.obj s ⟶ siteLocalizationQ.obj t)
  | .nil _ => 𝟙 _
  | .forward h rest =>
      siteLocalizationQ.map (homOfLE h) ≫ zigzagToLocalization rest
  | .backward h rest =>
      Localization.Construction.wInv
        (W := (⊤ : MorphismProperty Site))
        (homOfLE h) (by trivial) ≫ zigzagToLocalization rest

/-- Raw concatenation is interpreted as true categorical composition,
without cancelling any raw symbols. -/
theorem zigzagToLocalization_append
    {s t u : Site} (p : Zigzag s t) (q : Zigzag t u) :
    zigzagToLocalization (append p q) =
      zigzagToLocalization p ≫ zigzagToLocalization q := by
  induction p with
  | nil _ =>
      change zigzagToLocalization q = 𝟙 _ ≫ zigzagToLocalization q
      exact (Category.id_comp _).symm
  | forward h rest ih =>
      change siteLocalizationQ.map (homOfLE h) ≫
          zigzagToLocalization (append rest q) =
        (siteLocalizationQ.map (homOfLE h) ≫ zigzagToLocalization rest) ≫
          zigzagToLocalization q
      rw [ih]
      exact (Category.assoc _ _ _).symm
  | backward h rest ih =>
      change
        Localization.Construction.wInv
            (W := (⊤ : MorphismProperty Site))
            (homOfLE h) (by trivial) ≫
          zigzagToLocalization (append rest q) =
        (Localization.Construction.wInv
            (W := (⊤ : MorphismProperty Site))
            (homOfLE h) (by trivial) ≫
          zigzagToLocalization rest) ≫ zigzagToLocalization q
      rw [ih]
      exact (Category.assoc _ _ _).symm

/-- The actual finite raw zigzag *category* has an exact localization
functor, distinct from the original physical incidence poset. -/
def zigzagLocalizationFunctor : ZigzagSite ⥤ PhysicalLocalization where
  obj X := siteLocalizationQ.obj X.site
  map := fun {_ _} p => zigzagToLocalization p
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z p q
    exact zigzagToLocalization_append p q


/-- A genuine original incidence generator maps to its actual localization
arrow, including the (nondefinitional) preorder identity of the input Hom. -/
theorem rawForward_localized {s t : Site} (f : s ⟶ t) :
    zigzagToLocalization (forward f) = siteLocalizationQ.map f := by
  have hf : (homOfLE (leOfHom f) : s ⟶ t) = f :=
    Subsingleton.elim _ _
  change siteLocalizationQ.map (homOfLE (leOfHom f)) ≫ 𝟙 _ =
    siteLocalizationQ.map f
  rw [hf, Category.comp_id]

/-- A reversed generator becomes the canonical *formal* inverse only after
localization, never an actual arrow in the physical incidence category. -/
theorem rawBackward_localized {s t : Site} (f : s ⟶ t) :
    zigzagToLocalization (backward f) =
      Localization.Construction.wInv (W := (⊤ : MorphismProperty Site))
        f (by trivial) := by
  have hf : (homOfLE (leOfHom f) : s ⟶ t) = f :=
    Subsingleton.elim _ _
  change Localization.Construction.wInv
      (W := (⊤ : MorphismProperty Site))
      (homOfLE (leOfHom f)) (by trivial) ≫ 𝟙 _ =
    Localization.Construction.wInv (W := (⊤ : MorphismProperty Site))
      f (by trivial)
  rw [hf, Category.comp_id]

/-- The REAL vertex-edge-face incidence triangle becomes its diagonal
under the *specific* localization; the two raw syntactic words remain
different by flagRawTwoStep_ne_diagonal. -/
theorem physicalFlagTwoStep_localized (e : Edge) (i j : Bool) :
    zigzagToLocalization (flagRawTwoStep e i j) =
      zigzagToLocalization (flagRawDiagonal e i j) := by
  change
    siteLocalizationQ.map (homOfLE (flag_vertex_edge e i)) ≫
      (siteLocalizationQ.map (homOfLE (flag_edge_face e j)) ≫ 𝟙 _) =
    siteLocalizationQ.map
      (homOfLE (le_trans (flag_vertex_edge e i) (flag_edge_face e j))) ≫ 𝟙 _
  rw [Category.comp_id, Category.comp_id]
  rw [← siteLocalizationQ.map_comp]
  exact congrArg siteLocalizationQ.map (Subsingleton.elim _ _)

/-- The raw kernel relation is defined by the actual Mathlib localization
functor, not by a new arbitrary equality or a Gray evaluation. -/
def zigzagKernel : HomRel ZigzagSite :=
  zigzagLocalizationFunctor.homRel

abbrev ZigzagKernelQuotient := CategoryTheory.Quotient zigzagKernel

def zigzagKernelQ : ZigzagSite ⥤ ZigzagKernelQuotient :=
  CategoryTheory.Quotient.functor zigzagKernel

/-- The exact localization interpretation descends uniquely through its
true kernel relation quotient, with no additional raw identifications. -/
def zigzagKernelLift : ZigzagKernelQuotient ⥤ PhysicalLocalization :=
  CategoryTheory.Quotient.lift zigzagKernel
    zigzagLocalizationFunctor (by intro X Y p q hpq; exact hpq)

theorem zigzagKernel_factors :
    zigzagKernelQ ⋙ zigzagKernelLift = zigzagLocalizationFunctor :=
  CategoryTheory.Quotient.lift_spec _ _ _

theorem zigzagKernel_unique (F : ZigzagKernelQuotient ⥤ PhysicalLocalization)
    (hF : zigzagKernelQ ⋙ F = zigzagLocalizationFunctor) :
    F = zigzagKernelLift :=
  CategoryTheory.Quotient.lift_unique _ _ _ F hF

theorem zigzagKernel_exact {X Y : ZigzagSite} (p q : X ⟶ Y) :
    zigzagKernelQ.map p = zigzagKernelQ.map q ↔
      zigzagLocalizationFunctor.map p = zigzagLocalizationFunctor.map q := by
  constructor
  · intro h
    have hh := congrArg (fun f => zigzagKernelLift.map f) h
    have hc :
        (zigzagKernelQ ⋙ zigzagKernelLift).map p =
          (zigzagKernelQ ⋙ zigzagKernelLift).map q := by
      simpa only [Functor.comp_map] using hh
    rw [zigzagKernel_factors] at hc
    exact hc
  · intro h
    exact CategoryTheory.Quotient.sound zigzagKernel h

/-- Equality in the exact kernel quotient is observationally faithful to
the genuine physical localization; it is NOT raw-word faithfulness. -/
theorem zigzagKernelLift_faithful : zigzagKernelLift.Faithful := by
  constructor
  rintro ⟨X⟩ ⟨Y⟩ ⟨p⟩ ⟨q⟩ hpq
  exact (zigzagKernel_exact p q).2 hpq


/-- The original geometric two-leg source is identified with its true
vertex-to-face diagonal only in the EXACT localization kernel quotient. -/
theorem physicalFlagTwoStep_kernel (e : Edge) (i j : Bool) :
    zigzagKernelQ.map (flagRawTwoStep e i j) =
      zigzagKernelQ.map (flagRawDiagonal e i j) := by
  apply (zigzagKernel_exact (flagRawTwoStep e i j) (flagRawDiagonal e i j)).2
  exact physicalFlagTwoStep_localized e i j

#print axioms siteLocalization_universal
#print axioms siteLocalization_factor
#print axioms siteLocalization_unique
#print axioms zigzagToLocalization_append
#print axioms rawForward_localized
#print axioms rawBackward_localized
#print axioms physicalFlagTwoStep_localized
#print axioms zigzagLocalizationFunctor
#print axioms zigzagKernel_factors
#print axioms zigzagKernel_unique
#print axioms zigzagKernel_exact
#print axioms zigzagKernelLift_faithful
#print axioms physicalFlagTwoStep_kernel
end
end Kuu.F112.Physical
