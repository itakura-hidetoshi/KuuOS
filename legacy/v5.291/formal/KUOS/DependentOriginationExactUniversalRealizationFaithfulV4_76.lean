import KUOS.DependentOriginationExactUniversalCompatibleIsoV4_75
import Mathlib.CategoryTheory.Equivalence

namespace KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalCompatibleIsoV4_75

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Local faithfulness of DO₂ realization v4.76

The v4.75 comma embedding remembers both components. Here the pointwise
category-equivalence property of the source presentation comparison shows that
the DO₂ component alone determines an already compatible source 2-cell.

At each context, Mathlib identifies precomposition by an equivalence as an
equivalence of functor categories. Its faithfulness cancels the whiskered raw
modifications. Cancelling the stored comparison isomorphism then proves local
faithfulness of the actual DO₂ realization projection, not merely the comma
embedding.

Consequently all equations between parallel compatible 2-cells, including
inverse laws and pasting squares, can be checked on the DO₂ side. A prescribed
DO₂ isomorphism has at most one source isomorphism above it. No universal-target
essential-uniqueness argument or new admissibility hypothesis is needed.

This is faithfulness, not fullness: it does not construct a compatible 2-cell
from an arbitrary DO₂ modification, nor the unit/counit cells of a source
object equivalence. Their existence and comparison squares remain obligations.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]

/-- Whiskering by a pointwise-equivalence raw comparison is injective on
modifications. This lemma is independent of localization and the chosen atlas. -/
theorem rawWhiskerLeft_injective_of_pointwiseEquivalence
    {R S T : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (c : R ⟶ S)
    (hc : ∀ U : Context, (c.app (.mk U)).toFunctor.IsEquivalence)
    {r s : S ⟶ T} :
    Function.Injective (fun eta : r ⟶ s => c ◁ eta) := by
  intro eta theta h
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro U
  rcases U with ⟨U⟩
  letI : (c.app (.mk U)).toFunctor.IsEquivalence := hc U
  apply Cat.Hom₂.ext
  apply ((Functor.whiskeringLeft
    (R.obj (.mk U)) (S.obj (.mk U)) (T.obj (.mk U))).obj
      (c.app (.mk U)).toFunctor).map_injective
  exact congrArg
    (fun m : c ≫ r ⟶ c ≫ s => (m.as.app (.mk U)).toNatTrans) h

variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The raw comparison functor is faithful by the already stored pointwise
category equivalences of the chosen source presentation. -/
instance exactUniversalRawComparisonFunctor_faithful
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalRawComparisonFunctor (W := W) A X Y).Faithful where
  map_injective {r s} :=
    rawWhiskerLeft_injective_of_pointwiseEquivalence
      X.presentation.comparison X.presentation.comparison_isEquivalence
      (r := r) (s := s)

variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
variable {f g : ExactUniversalRawMorphism (W := W) A X Y}

/-- The realized component determines an already compatible source 2-cell. -/
theorem exactUniversalCompletion2_map_injective :
    Function.Injective (fun eta : f ⟶ g => eta.lift) := by
  intro eta theta h
  apply ExactUniversalRawMorphismTwoCell.ext
  · apply (exactUniversalRawComparisonFunctor (W := W) A X Y).map_injective
    change (X.presentation.comparison ◁ eta.raw) =
      (X.presentation.comparison ◁ theta.raw)
    apply (cancel_epi f.comparison_square.hom).1
    calc
      f.comparison_square.hom ≫ (X.presentation.comparison ◁ eta.raw) =
          (restrictHigherLocalizedModification (W := W) eta.lift.hom ▷
            Y.presentation.comparison) ≫ g.comparison_square.hom :=
        eta.compatibility.symm
      _ = (restrictHigherLocalizedModification (W := W) theta.lift.hom ▷
            Y.presentation.comparison) ≫ g.comparison_square.hom := by
        -- Transport the equality through a fixed, typed function instead of
        -- asking `rw` to match the unreduced lambda application in `h`.
        exact congrArg
          (fun ell : f.lift ⟶ g.lift =>
            (restrictHigherLocalizedModification (W := W) ell.hom ▷
              Y.presentation.comparison) ≫ g.comparison_square.hom) h
      _ = f.comparison_square.hom ≫ (X.presentation.comparison ◁ theta.raw) :=
        theta.compatibility
  · exact h

/-- Local faithfulness of the actual DO₂ realization hom functor. -/
instance exactUniversalCompletion2HomFunctor_faithful :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).Faithful where
  map_injective {f g} :=
    exactUniversalCompletion2_map_injective (W := W) A (f := f) (g := g)

/-- All equality questions for parallel compatible 2-cells reflect to DO₂. -/
theorem exactUniversalTwoCell_eq_iff_lift_eq (eta theta : f ⟶ g) :
    eta = theta ↔ eta.lift = theta.lift := by
  constructor
  · intro h
    exact congrArg (fun m : f ⟶ g => m.lift) h
  · intro h
    -- Specialize injectivity to this equality; its universally quantified
    -- proof is not itself the fixed-pair implication expected here.
    exact exactUniversalCompletion2_map_injective (W := W) A h

/-- For a fixed realized modification, two raw solutions of the comparison
square coincide. Existence of a solution is deliberately not assumed or claimed. -/
theorem exactUniversalRawComponent_unique_of_compatible
    (ell : f.lift ⟶ g.lift) (r s : f.raw ⟶ g.raw)
    (hr : (restrictHigherLocalizedModification (W := W) ell.hom ▷
        Y.presentation.comparison) ≫ g.comparison_square.hom =
      f.comparison_square.hom ≫ (X.presentation.comparison ◁ r))
    (hs : (restrictHigherLocalizedModification (W := W) ell.hom ▷
        Y.presentation.comparison) ≫ g.comparison_square.hom =
      f.comparison_square.hom ≫ (X.presentation.comparison ◁ s)) : r = s := by
  let eta : f ⟶ g := { raw := r, lift := ell, compatibility := hr }
  let theta : f ⟶ g := { raw := s, lift := ell, compatibility := hs }
  have h : eta = theta := exactUniversalCompletion2_map_injective (W := W) A rfl
  exact congrArg (fun m : f ⟶ g => m.raw) h

/-- A source isomorphism is determined by its realized forward 2-cell.
Unlike v4.75, no equality of the raw component needs to be supplied. -/
theorem exactUniversalSourceIso_eq_iff_lift_hom_eq (e d : f ≅ g) :
    e = d ↔ e.hom.lift = d.hom.lift := by
  constructor
  · intro h
    exact congrArg (fun i : f ≅ g => i.hom.lift) h
  · intro h
    apply Iso.ext
    exact exactUniversalCompletion2_map_injective (W := W) A h

/-- Inverse laws for already compatible cells can be checked after realization. -/
theorem exactUniversalTwoCell_comp_eq_id_iff
    (eta : f ⟶ g) (theta : g ⟶ f) :
    eta ≫ theta = 𝟙 f ↔ eta.lift ≫ theta.lift = 𝟙 f.lift :=
  exactUniversalTwoCell_eq_iff_lift_eq (W := W) A (eta ≫ theta) (𝟙 f)

/-- Commutativity of a square of compatible 2-cells reflects to DO₂.
This applies to pasting equations once their constituent cells are constructed. -/
theorem exactUniversalTwoCell_square_iff
    {h i : ExactUniversalRawMorphism (W := W) A X Y}
    (alpha : f ⟶ g) (beta : g ⟶ i)
    (gamma : f ⟶ h) (delta : h ⟶ i) :
    alpha ≫ beta = gamma ≫ delta ↔
      alpha.lift ≫ beta.lift = gamma.lift ≫ delta.lift :=
  exactUniversalTwoCell_eq_iff_lift_eq (W := W) A (alpha ≫ beta) (gamma ≫ delta)

/-! ## Regression checks: do not add raw-component equality as a hypothesis. -/

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).Faithful :=
  inferInstance

-- Exercise both the polymorphic injectivity API and its fixed-pair use.
example : Function.Injective (fun eta : f ⟶ g => eta.lift) :=
  exactUniversalCompletion2_map_injective (W := W) A

example (eta theta : f ⟶ g)
    (h : (fun m : f ⟶ g => m.lift) eta = (fun m : f ⟶ g => m.lift) theta) :
    eta = theta :=
  exactUniversalCompletion2_map_injective (W := W) A h

example (eta theta : f ⟶ g) (h : eta.lift = theta.lift) : eta = theta :=
  (exactUniversalTwoCell_eq_iff_lift_eq (W := W) A eta theta).2 h

example (eta : f ⟶ f) (h : eta.lift = 𝟙 f.lift) : eta = 𝟙 f := by
  apply (exactUniversalTwoCell_eq_iff_lift_eq (W := W) A eta (𝟙 f)).2
  change eta.lift = 𝟙 f.lift
  exact h

example (eta : f ⟶ g) (theta : g ⟶ f)
    (h : eta.lift ≫ theta.lift = 𝟙 f.lift) : eta ≫ theta = 𝟙 f :=
  (exactUniversalTwoCell_comp_eq_id_iff (W := W) A eta theta).2 h

example (e d : f ≅ g) (h : e.hom.lift = d.hom.lift) : e = d :=
  (exactUniversalSourceIso_eq_iff_lift_hom_eq (W := W) A e d).2 h

example {h i : ExactUniversalRawMorphism (W := W) A X Y}
    (alpha : f ⟶ g) (beta : g ⟶ i) (gamma : f ⟶ h) (delta : h ⟶ i)
    (hsquare : alpha.lift ≫ beta.lift = gamma.lift ≫ delta.lift) :
    alpha ≫ beta = gamma ≫ delta :=
  (exactUniversalTwoCell_square_iff (W := W) A alpha beta gamma delta).2 hsquare

#print axioms rawWhiskerLeft_injective_of_pointwiseEquivalence
#print axioms exactUniversalCompletion2_map_injective
#print axioms exactUniversalTwoCell_eq_iff_lift_eq
#print axioms exactUniversalSourceIso_eq_iff_lift_hom_eq

end

end KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
