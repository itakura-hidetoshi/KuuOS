import KUOS.DependentOriginationC60KuuWitnessedGrothendieckSourceEquivalenceV5_288
import KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281
import Mathlib.CategoryTheory.Localization.Predicate

namespace KUOS.DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
open KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278
open KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281
open KUOS.DependentOriginationC60KuuWitnessedSourceDiagramBeckChevalleyV5_287
open KUOS.DependentOriginationC60KuuWitnessedGrothendieckSourceEquivalenceV5_288
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.289 / F112 part 17 — localized witnessed original F47 source total categories

The BASE of this construction is ONLY the ACTUAL physical F69
overlap-WITNESSED finite-path category introduced in v5.278.
All its arrows, not the noninvertible old F69 incidence poset arrows,
are localized using the genuine pinned Mathlib Gabriel-Zisman
construction already proved universal in v5.281.

For each independently selected family of odd ORIGINAL F42 face
two-cells, the fully native ORIGINAL F47 Cat-valued diagram
inverts EVERY genuine witnessed arrow (proved in v5.280/v5.281).
For every two such families P,Q, the genuine diagram NatIso on
all arbitrary finite witnessed paths (v5.287) extends to a
NATURAL ISOMORPHISM of the two canonically localized diagrams.

This is obtained from Mathlib's actual localization
2-dimensional universal property, Localization.liftNatIso,
not by inventing inverse arrows in the old F69 incidence
category or identifying original raw F42/F54 proof witnesses.

The induced Grothendieck total source categories over the
LOCALIZED witnessed-path base are isomorphic and equivalent,
STRICTLY preserving that precise localized base on objects
and arrows. Their source-change functor is compatible with
pullback along the original genuine witnessed localization
functor (Mathlib Grothendieck.pre_comp_map).

This is still not original F42/F54/F55 RAW SOURCE descent on
ALL 60+90+32 original F69 incidence sites. F55's nine-constructor
Delta nonlift, F77 phase nonreconstruction, and the signed
original F68 north pentagon curvature -5 remain independent.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section WitnessedLocalizedSource
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

/-- The ORIGINAL F47 source diagram on genuine witnessed paths
has a canonical *strict* Mathlib factorization through their
own actual localization. This is NOT the original F69 poset. -/
theorem c60F123TwoOriginalF47Diagrams_factor
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    (c60F115WitnessedLocalizationQ C ⋙
        c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P =
      c60F112WitnessedF47Diagram t₁ t₂ left right C P) ∧
    (c60F115WitnessedLocalizationQ C ⋙
        c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C Q =
      c60F112WitnessedF47Diagram t₁ t₂ left right C Q) :=
  ⟨c60F115OriginalF47Localization_factors t₁ t₂ left right C P,
    c60F115OriginalF47Localization_factors t₁ t₂ left right C Q⟩

/-- Main theorem: the TRUE original full-phase source diagram
NatIso (v5.287) uniquely extends through the TRUE
Gabriel–Zisman localization of the genuine witnessed
C60 physical-overlap path category, via pinned Mathlib
Localization.liftNatIso. The original Int×Int charges
and independent ZMod2 phase have not been projected out. -/
def c60F123LocalizedWitnessedF47DiagramNatIso
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P ≅
      c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C Q :=
  by
    letI :
        (c60F115WitnessedLocalizationQ C).IsLocalization
          (⊤ : MorphismProperty (C60F112WitnessedEdge C)) :=
      c60F115WitnessedLocalization_universal C
    letI : Localization.Lifting
        (c60F115WitnessedLocalizationQ C)
        (⊤ : MorphismProperty (C60F112WitnessedEdge C))
        (c60F112WitnessedF47Diagram t₁ t₂ left right C P)
        (c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P) :=
      ⟨eqToIso
        (c60F115OriginalF47Localization_factors
          t₁ t₂ left right C P)⟩
    letI : Localization.Lifting
        (c60F115WitnessedLocalizationQ C)
        (⊤ : MorphismProperty (C60F112WitnessedEdge C))
        (c60F112WitnessedF47Diagram t₁ t₂ left right C Q)
        (c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C Q) :=
      ⟨eqToIso
        (c60F115OriginalF47Localization_factors
          t₁ t₂ left right C Q)⟩
    exact Localization.liftNatIso
      (c60F115WitnessedLocalizationQ C)
      (⊤ : MorphismProperty (C60F112WitnessedEdge C))
      (c60F112WitnessedF47Diagram t₁ t₂ left right C P)
      (c60F112WitnessedF47Diagram t₁ t₂ left right C Q)
      (c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P)
      (c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C Q)
      (c60F121WitnessedF47DiagramSourceNatIso t₁ t₂ left right C P Q)

/-- The total category of ORIGINAL F47 3-Homs, now indexed by
the GENUINE LOCALIZATION of the witnessed physical-overlap
path base, not the old noninvertible F69 incidence poset. -/
abbrev c60F123LocalizedWitnessedF47Total
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :=
  Grothendieck (c60F115LocalizedOriginalF47Diagram
    t₁ t₂ left right C P)

/-- Lift the actual localized ORIGINAL source diagram NatIso
to a functor of its localized Grothendieck total categories. -/
def c60F123LocalizedWitnessedTotalSourceChange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F123LocalizedWitnessedF47Total t₁ t₂ left right C P ⥤
      c60F123LocalizedWitnessedF47Total t₁ t₂ left right C Q :=
  Grothendieck.map
    (c60F123LocalizedWitnessedF47DiagramNatIso
      t₁ t₂ left right C P Q).hom

/-- The source change never changes an object of the genuine
localization's physical base: it re-presents only its
ORIGINAL independent F42/F54/F55 source fibre. -/
theorem c60F123LocalizedTotalSourceChange_obj_base
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (X : c60F123LocalizedWitnessedF47Total t₁ t₂ left right C P) :
    ((c60F123LocalizedWitnessedTotalSourceChange
      t₁ t₂ left right C P Q).obj X).base = X.base := rfl

/-- The base Hom of every localized total source 3-arrow
is literally unchanged, including actual FORMAL inverses
of the original physical witnessed-path morphisms. -/
theorem c60F123LocalizedTotalSourceChange_map_base
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {X Y : c60F123LocalizedWitnessedF47Total t₁ t₂ left right C P}
    (f : X ⟶ Y) :
    ((c60F123LocalizedWitnessedTotalSourceChange
      t₁ t₂ left right C P Q).map f).base = f.base := rfl

/-- STRICT compatibility of the localized source-change total
functor with the correct localized physical-witness projection. -/
theorem c60F123LocalizedTotalSourceChange_overBase
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F123LocalizedWitnessedTotalSourceChange
        t₁ t₂ left right C P Q ⋙
      Grothendieck.forget
        (c60F115LocalizedOriginalF47Diagram
          t₁ t₂ left right C Q) =
    Grothendieck.forget
      (c60F115LocalizedOriginalF47Diagram
        t₁ t₂ left right C P) :=
  Grothendieck.functor_comp_forget

/-- Pinned Mathlib provides an EXACT Beck–Chevalley
reindexing square between first LOCALIZING the real
witness-path base and then changing ORIGINAL F42 source
presentations, versus first changing those presentations
and then pushing forward along the SAME localization Q.

The equality lives between genuine Grothendieck TOTAL
FUNCTORS and does not assert the old F69 site poset
already had inverses or original-source effective descent. -/
theorem c60F123LocalizedTotalSourceChange_precompQ
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    Grothendieck.pre
        (c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C P)
        (c60F115WitnessedLocalizationQ C) ⋙
      c60F123LocalizedWitnessedTotalSourceChange
        t₁ t₂ left right C P Q =
    Grothendieck.map
        (Functor.whiskerLeft (c60F115WitnessedLocalizationQ C)
          (c60F123LocalizedWitnessedF47DiagramNatIso
            t₁ t₂ left right C P Q).hom) ⋙
      Grothendieck.pre
        (c60F115LocalizedOriginalF47Diagram t₁ t₂ left right C Q)
        (c60F115WitnessedLocalizationQ C) :=
  Grothendieck.pre_comp_map
    (c60F115WitnessedLocalizationQ C)
    (c60F123LocalizedWitnessedF47DiagramNatIso
      t₁ t₂ left right C P Q).hom

/-- The LOCALIZED genuine witnessed F47 Grothendieck TOTAL
CATEGORIES are actually ISOMORPHIC as Cat objects, not
just equipped with unspecified 1-sided source transports.
The inverse functor arises from the INVERSE of the real
localized diagram-level source NatIso and respects the
same real localized physical base. -/
def c60F123LocalizedWitnessedTotalCatIso
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    Cat.of (c60F123LocalizedWitnessedF47Total
      t₁ t₂ left right C P) ≅
      Cat.of (c60F123LocalizedWitnessedF47Total
        t₁ t₂ left right C Q) where
  hom := (Grothendieck.map
    (c60F123LocalizedWitnessedF47DiagramNatIso
      t₁ t₂ left right C P Q).hom).toCatHom
  inv := (Grothendieck.map
    (c60F123LocalizedWitnessedF47DiagramNatIso
      t₁ t₂ left right C P Q).inv).toCatHom
  hom_inv_id := by
    let e := c60F123LocalizedWitnessedF47DiagramNatIso
      t₁ t₂ left right C P Q
    apply Cat.Hom.ext
    change Grothendieck.map e.hom ⋙ Grothendieck.map e.inv = 𝟭 _
    calc
      _ = Grothendieck.map (e.hom ≫ e.inv) :=
        (Grothendieck.map_comp_eq e.hom e.inv).symm
      _ = Grothendieck.map (𝟙 _) := by rw [e.hom_inv_id]
      _ = 𝟭 _ := Grothendieck.map_id_eq
  inv_hom_id := by
    let e := c60F123LocalizedWitnessedF47DiagramNatIso
      t₁ t₂ left right C P Q
    apply Cat.Hom.ext
    change Grothendieck.map e.inv ⋙ Grothendieck.map e.hom = 𝟭 _
    calc
      _ = Grothendieck.map (e.inv ≫ e.hom) :=
        (Grothendieck.map_comp_eq e.inv e.hom).symm
      _ = Grothendieck.map (𝟙 _) := by rw [e.inv_hom_id]
      _ = 𝟭 _ := Grothendieck.map_id_eq

/-- Source presentation change induces a REAL equivalence of
localized physical-witnessed F47 total categories, not a
hypothetical original F69-wide Gray three-stack. -/
def c60F123LocalizedWitnessedTotalEquivalence
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F123LocalizedWitnessedF47Total t₁ t₂ left right C P ≌
      c60F123LocalizedWitnessedF47Total t₁ t₂ left right C Q :=
  Cat.equivOfIso
    (c60F123LocalizedWitnessedTotalCatIso t₁ t₂ left right C P Q)

/-- The localized total EQUIVALENCE remains exactly over the
correct physical witnessed-path LOCALIZATION, never over
the original F69 noninvertible incidence category. -/
theorem c60F123LocalizedWitnessedTotalEquivalence_overBase
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    (c60F123LocalizedWitnessedTotalEquivalence
      t₁ t₂ left right C P Q).functor ⋙
      Grothendieck.forget
        (c60F115LocalizedOriginalF47Diagram
          t₁ t₂ left right C Q) =
    Grothendieck.forget
      (c60F115LocalizedOriginalF47Diagram
        t₁ t₂ left right C P) :=
  c60F123LocalizedTotalSourceChange_overBase t₁ t₂ left right C P Q

/-- Even AFTER the genuine witnessed-path localization and
the total category equivalence, the ORIGINAL nine-constructor
F55 Delta remains nonliftable and the original signed
north-pentagon second charge is -5. No unsupported physical
F68 flatness or raw F42/F54/F55 effectivity is inferred. -/
theorem c60F123LocalizedTotal_originalCurvedObstruction
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j)
    (sigma : C60F67Atlas) :
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) ∧
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma ≠ 0 ∧
    (¬ ∃ vertexGauge :
        C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F68AtlasEdgeCochain t₁ t₂ left right sigma =
        vertexGauge.comp c60IntegralBoundaryOne) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j)).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j)).rotationStep) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j (Q j)).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C j (Q j)).rotationStep) :=
  c60F122WitnessedF47Totals_curvedSourceObstruction
    t₁ t₂ left right C P Q path sigma

#print axioms c60F123TwoOriginalF47Diagrams_factor
#print axioms c60F123LocalizedWitnessedF47DiagramNatIso
#print axioms c60F123LocalizedTotalSourceChange_obj_base
#print axioms c60F123LocalizedTotalSourceChange_map_base
#print axioms c60F123LocalizedTotalSourceChange_overBase
#print axioms c60F123LocalizedTotalSourceChange_precompQ
#print axioms c60F123LocalizedWitnessedTotalCatIso
#print axioms c60F123LocalizedWitnessedTotalEquivalence
#print axioms c60F123LocalizedWitnessedTotalEquivalence_overBase
#print axioms c60F123LocalizedTotal_originalCurvedObstruction

end WitnessedLocalizedSource
end
end KUOS.DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289
