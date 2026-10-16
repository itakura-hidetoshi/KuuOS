import KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281
import Mathlib.CategoryTheory.Groupoid.FreeGroupoidOfCategory
import Mathlib.CategoryTheory.Quotient

namespace KUOS.DependentOriginationC60KuuF69ZigzagKernelQuotientFreeGroupoidV5_282

open CategoryTheory
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279
open KUOS.DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280
open KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.282 / F112 stage 10 — the genuine raw zigzag kernel and groupoid completion

We DO NOT conflate the original physical F69 incidence poset, the
F113 free forward/backward zigzag category, and either localization.

1. Mathlib's FreeGroupoid of the ORIGINAL F69 incidence category is
   equivalent to the Gabriel–Zisman localization at all ORIGINAL
   arrows. This gives a genuine categorical universal equivalence,
   not an unverified claim that raw zigzag words are already inverse.
2. The kernel relation on RAW F113 zigzags is induced by their
   verified functor into the original F69 localization. The Mathlib
   QUOTIENT of this kernel has a canonical faithful representation
   and the actual strict universal property for functors respecting
   EXACTLY this relation.
3. Genuine old incidence id/comp and formal backtracking are
   explicitly identified ONLY after the indicated quotient.
   In the original free zigzag, even a two-leg backtrack remains
   a nonempty proof-carrying geometric path.

The groupoid completion is a categorical equivalence between two
FORMAL LOCALIZATIONS of original F69; no equivalence between the raw
zigzag and the localized groupoid is asserted without proving the
necessary quotient fullness. F47 source gluing and F68 curvature
are separate from this universal groupoid classification.
-/

/-! ## I. Free groupoid and genuine old-incidence localization -/

/-- Groupoid completion of the unchanged ORIGINAL F69 category. -/
abbrev C60F116OriginalF69FreeGroupoid :=
  FreeGroupoid C60F69PhysicalCellSite

/-- The original F69 category localizes at ALL its genuine arrows,
also as a true free groupoid in the pinned Mathlib. -/
theorem c60F116OriginalF69FreeGroupoid_isLocalization :
    (FreeGroupoid.of C60F69PhysicalCellSite).IsLocalization
      (⊤ : MorphismProperty C60F69PhysicalCellSite) := by
  infer_instance

/-- Both standard constructions have the SAME localization
universal property and are canonically equivalent. -/
def c60F116OriginalF69FreeGroupoidEquivalence :
    C60F116OriginalF69FreeGroupoid ≌ C60F115OriginalF69Localization :=
  Localization.uniq
    (FreeGroupoid.of C60F69PhysicalCellSite)
    ((⊤ : MorphismProperty C60F69PhysicalCellSite).Q)
    (⊤ : MorphismProperty C60F69PhysicalCellSite)

/-- Compatibility on each genuinely existing original F69
incidence Hom is a natural ISOMORPHISM, not a raw word identity. -/
def c60F116OriginalF69FreeGroupoidComparison :
    (FreeGroupoid.of C60F69PhysicalCellSite) ⋙
        c60F116OriginalF69FreeGroupoidEquivalence.functor ≅
      c60F115OriginalF69LocalizationQ :=
  Localization.compUniqFunctor
    (FreeGroupoid.of C60F69PhysicalCellSite)
    ((⊤ : MorphismProperty C60F69PhysicalCellSite).Q)
    (⊤ : MorphismProperty C60F69PhysicalCellSite)

/-- The universal comparison functor is a category equivalence. -/
theorem c60F116OriginalF69GroupoidComparison_isEquivalence :
    c60F116OriginalF69FreeGroupoidEquivalence.functor.IsEquivalence :=
  c60F116OriginalF69FreeGroupoidEquivalence.isEquivalence_functor

/-! ## II. Precise original-F69-localization kernel of RAW zigzags -/

/-- Two F113 freely generated zigzags are observationally
interchangeable here IFF their actual original F69-localized
arrows coincide. There is no collapse of the source syntax. -/
def c60F116RawZigzagKernel : HomRel C60F113ZigzagSite :=
  c60F115F69ZigzagLocalizationFunctor.homRel

/-- The true Mathlib quotient of FREE F69 incidence zigzags by
their proved localization kernel. This is not original F69. -/
abbrev C60F116RawZigzagKernelQuotient :=
  CategoryTheory.Quotient c60F116RawZigzagKernel

/-- Canonical quotient functor from the raw F69 zigzag category. -/
def c60F116RawZigzagKernelQ :
    C60F113ZigzagSite ⥤ C60F116RawZigzagKernelQuotient :=
  CategoryTheory.Quotient.functor c60F116RawZigzagKernel

/-- The original F69 localization representation descends to
the exact raw-zigzag kernel quotient without extra assumptions. -/
def c60F116RawZigzagKernelLift :
    C60F116RawZigzagKernelQuotient ⥤ C60F115OriginalF69Localization :=
  CategoryTheory.Quotient.lift c60F116RawZigzagKernel
    c60F115F69ZigzagLocalizationFunctor
    (by
      intro X Y p q hpq
      exact hpq)

/-- STRICT factorization of the true original-F69 zigzag
transport across the exact kernel quotient. -/
theorem c60F116RawZigzagKernel_factors :
    c60F116RawZigzagKernelQ ⋙ c60F116RawZigzagKernelLift =
      c60F115F69ZigzagLocalizationFunctor := by
  exact CategoryTheory.Quotient.lift_spec _ _ _

/-- The factorizing functor is UNIQUE among all functors with
this identical original F69 localized effect. -/
theorem c60F116RawZigzagKernel_unique
    (F : C60F116RawZigzagKernelQuotient ⥤
      C60F115OriginalF69Localization)
    (hF : c60F116RawZigzagKernelQ ⋙ F =
      c60F115F69ZigzagLocalizationFunctor) :
    F = c60F116RawZigzagKernelLift := by
  exact CategoryTheory.Quotient.lift_unique _ _ _ F hF

/-- The kernel quotient makes NO additional distinctions disappear
beyond equality of the actual original F69 localized images. -/
theorem c60F116RawZigzagKernel_exact
    {X Y : C60F113ZigzagSite} (p q : X ⟶ Y) :
    c60F116RawZigzagKernelQ.map p =
        c60F116RawZigzagKernelQ.map q ↔
      c60F115F69ZigzagLocalizationFunctor.map p =
        c60F115F69ZigzagLocalizationFunctor.map q := by
  constructor
  · intro h
    have hh := congrArg (fun f => c60F116RawZigzagKernelLift.map f) h
    have hc :
        (c60F116RawZigzagKernelQ ⋙ c60F116RawZigzagKernelLift).map p =
          (c60F116RawZigzagKernelQ ⋙ c60F116RawZigzagKernelLift).map q := by
      simpa only [Functor.comp_map] using hh
    rw [c60F116RawZigzagKernel_factors] at hc
    exact hc
  · intro h
    exact CategoryTheory.Quotient.sound c60F116RawZigzagKernel h

/-- The exact quotient image into the genuine F69 localization
is faithful, as the kernel theorem demonstrates. -/
theorem c60F116RawZigzagKernelLift_faithful :
    c60F116RawZigzagKernelLift.Faithful := by
  constructor
  rintro ⟨X⟩ ⟨Y⟩ ⟨p⟩ ⟨q⟩ hpq
  exact (c60F116RawZigzagKernel_exact p q).2 hpq

/-! ## III. Which original F69 word relations do we quotient? -/

/-- ONE actual forward ORIGINAL F69 incidence arrow,
stored as a noncancelled free zigzag word. -/
def c60F116RawForward
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    C60F113IncidenceZigzag s t :=
  .forward (leOfHom f) (.nil t)

/-- One FORMALLY REVERSED old F69 incidence Hom, not an old
reverse arrow: it exists only in the new free zigzag category. -/
def c60F116RawBackward
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    C60F113IncidenceZigzag t s :=
  .backward (leOfHom f) (.nil s)

/-- A raw forward generator represents exactly the original
old-incidence arrow mapped by the universal localization. -/
theorem c60F116RawForward_localized
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    c60F115F69ZigzagToLocalizationHom (c60F116RawForward f) =
      c60F115OriginalF69LocalizationQ.map f := by
  have hf : (homOfLE (leOfHom f) : s ⟶ t) = f :=
    Subsingleton.elim _ _
  change c60F115OriginalF69LocalizationQ.map (homOfLE (leOfHom f)) ≫ 𝟙 _ =
    c60F115OriginalF69LocalizationQ.map f
  rw [hf, Category.comp_id]

/-- A raw BACKWARD generator represents the FORMAL inverse in
the localized category and is not a genuine original F69 Hom. -/
theorem c60F116RawBackward_localized
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    c60F115F69ZigzagToLocalizationHom (c60F116RawBackward f) =
      Localization.Construction.wInv
        (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
        f (by trivial) := by
  have hf : (homOfLE (leOfHom f) : s ⟶ t) = f :=
    Subsingleton.elim _ _
  change
    Localization.Construction.wInv
      (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
      (homOfLE (leOfHom f)) (by trivial) ≫ 𝟙 _ =
      Localization.Construction.wInv
        (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
        f (by trivial)
  rw [hf, Category.comp_id]

/-- REAL original F69 composition is identified with concatenating
the two formally forward generators only AFTER localization. -/
theorem c60F116RawForward_comp_localized
    {s t u : C60F69PhysicalCellSite}
    (f : s ⟶ t) (g : t ⟶ u) :
    c60F115F69ZigzagToLocalizationHom
        (c60F116RawForward (f ≫ g)) =
      c60F115F69ZigzagToLocalizationHom
        (c60F113ZigzagAppend
          (c60F116RawForward f) (c60F116RawForward g)) := by
  rw [c60F115F69ZigzagToLocalization_append,
    c60F116RawForward_localized, c60F116RawForward_localized,
    c60F116RawForward_localized]
  exact c60F115OriginalF69LocalizationQ.map_comp f g

/-- A forward old arrow followed by its formal reverse is not
the empty word in raw geometry: exactly two legs persist. -/
theorem c60F116RawBacktrack_nonempty
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    c60F113ZigzagAppend
        (c60F116RawForward f) (c60F116RawBackward f) ≠
      C60F113IncidenceZigzag.nil s := by
  intro h
  have hh := congrArg c60F114F69ZigzagLength h
  simp [c60F113ZigzagAppend, c60F116RawForward,
    c60F116RawBackward, c60F114F69ZigzagLength] at hh

/-- The SAME two real original F69 legs become inverse precisely
under localization, where they are not a false original arrow. -/
theorem c60F116RawForward_backward_localized
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    c60F115F69ZigzagToLocalizationHom
        (c60F113ZigzagAppend
          (c60F116RawForward f) (c60F116RawBackward f)) =
      𝟙 (c60F115OriginalF69LocalizationQ.obj s) := by
  rw [c60F115F69ZigzagToLocalization_append,
    c60F116RawForward_localized,
    c60F116RawBackward_localized]
  exact (Localization.Construction.wIso
    (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
    f (by trivial)).hom_inv_id

/-- The reverse-then-forward path likewise cancels in the
localized category, but not in the old F69 poset or raw word. -/
theorem c60F116RawBackward_forward_localized
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    c60F115F69ZigzagToLocalizationHom
        (c60F113ZigzagAppend
          (c60F116RawBackward f) (c60F116RawForward f)) =
      𝟙 (c60F115OriginalF69LocalizationQ.obj t) := by
  rw [c60F115F69ZigzagToLocalization_append,
    c60F116RawBackward_localized,
    c60F116RawForward_localized]
  exact (Localization.Construction.wIso
    (W := (⊤ : MorphismProperty C60F69PhysicalCellSite))
    f (by trivial)).inv_hom_id

/-- Actual original-incidence backtracking is killed in the
EXACT universal kernel quotient, not the raw F113 syntax. -/
theorem c60F116RawBacktrack_quotient_identity
    {s t : C60F69PhysicalCellSite} (f : s ⟶ t) :
    c60F116RawZigzagKernelQ.map
        (c60F113ZigzagAppend
          (c60F116RawForward f) (c60F116RawBackward f)) =
      𝟙 (c60F116RawZigzagKernelQ.obj ⟨s⟩) := by
  have h := c60F116RawForward_backward_localized f
  have hh := (c60F116RawZigzagKernel_exact
    (c60F113ZigzagAppend
      (c60F116RawForward f) (c60F116RawBackward f))
    (C60F113IncidenceZigzag.nil s)).2 h
  exact hh.trans (c60F116RawZigzagKernelQ.map_id ⟨s⟩)

#print axioms c60F116OriginalF69FreeGroupoid_isLocalization
#print axioms c60F116OriginalF69FreeGroupoidEquivalence
#print axioms c60F116OriginalF69FreeGroupoidComparison
#print axioms c60F116RawZigzagKernel_factors
#print axioms c60F116RawZigzagKernel_unique
#print axioms c60F116RawZigzagKernel_exact
#print axioms c60F116RawZigzagKernelLift_faithful
#print axioms c60F116RawForward_localized
#print axioms c60F116RawBackward_localized
#print axioms c60F116RawForward_comp_localized
#print axioms c60F116RawBacktrack_nonempty
#print axioms c60F116RawForward_backward_localized
#print axioms c60F116RawBackward_forward_localized
#print axioms c60F116RawBacktrack_quotient_identity

end
end KUOS.DependentOriginationC60KuuF69ZigzagKernelQuotientFreeGroupoidV5_282
