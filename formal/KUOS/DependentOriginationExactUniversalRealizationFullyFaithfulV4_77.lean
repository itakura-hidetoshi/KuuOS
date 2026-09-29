import KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
import Mathlib.CategoryTheory.Functor.FullyFaithful

namespace KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77

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
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Local full faithfulness of DO₂ realization v4.77

v4.76 proves uniqueness of compatible source 2-cells from their DO₂ component.
Here we construct the missing raw component, without assuming fullness.

For Cat-valued pseudofunctors on an arbitrary bicategory, precomposition by a
pointwise-equivalence strong transformation is surjective on modifications.
Mathlib's functor-category preimage supplies each component. Naturality follows
by faithful precomposition, the naturality of the given modification, and the
naturality of the chosen component across the comparison's invertible square.
No global quasi-inverse strong transformation is assumed.

Applied to the stored presentation comparison, this constructs the raw part of
any prescribed DO₂ 2-cell after conjugating by the two comparison squares.
Together with v4.76 it gives a hom-set Equiv and actual locally fully faithful
realization. In particular every DO₂ isomorphism between already realized source
1-cells lifts to a source isomorphism.

This is not essential surjectivity on 1-cells or a final mapping biequivalence.
Object-equivalence and prescribed raw unit/counit identifications remain separate
from the local 2-cell construction proved here.
-/

universe u v uH vH uB vB wB

section Pointwise

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {R S T : Pseudofunctor B Cat.{vH, uH}}

/-- The composite comparison constraint evaluated in Cat. The three
associators have identity components, but these identities must be simplified,
not discarded by an assumption that the entire bicategory is definitionally strict. -/
private theorem compositeNaturality_app
    (c : R ⟶ S) (r : S ⟶ T) {U V : B} (p : U ⟶ V) (x : R.obj U) :
    ((c ≫ r).naturality p).hom.toNatTrans.app x =
      (r.app V).toFunctor.map ((c.naturality p).hom.toNatTrans.app x) ≫
        (r.naturality p).hom.toNatTrans.app ((c.app U).toFunctor.obj x) := by
  change
    𝟙 _ ≫ (r.app V).toFunctor.map ((c.naturality p).hom.toNatTrans.app x) ≫
      𝟙 _ ≫ (r.naturality p).hom.toNatTrans.app ((c.app U).toFunctor.obj x) ≫
        𝟙 _ = _
  simp only [Category.id_comp, Category.comp_id]

variable (c : R ⟶ S)
variable (hc : ∀ U : B, (c.app U).toFunctor.IsEquivalence)
variable {r s : S ⟶ T}

/-- Choose a component by Mathlib fullness of precomposition by an equivalence. -/
def pointwiseWhiskerPreimage (tau : c ≫ r ⟶ c ≫ s) (U : B) :
    (r.app U).toFunctor ⟶ (s.app U).toFunctor := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  exact ((Functor.whiskeringLeft
    (R.obj U) (S.obj U) (T.obj U)).obj (c.app U).toFunctor).preimage
      (tau.as.app U).toNatTrans

/-- Each component is a genuine preimage, not only isomorphic to one. -/
theorem pointwiseWhiskerPreimage_spec (tau : c ≫ r ⟶ c ≫ s) (U : B) :
    Functor.whiskerLeft (c.app U).toFunctor (pointwiseWhiskerPreimage c hc tau U) =
      (tau.as.app U).toNatTrans := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  exact ((Functor.whiskeringLeft
    (R.obj U) (S.obj U) (T.obj U)).obj (c.app U).toFunctor).map_preimage
      (tau.as.app U).toNatTrans

/-- Evaluation of the component preimage equation. -/
private theorem pointwiseWhiskerPreimage_app
    (tau : c ≫ r ⟶ c ≫ s) (U : B) (x : R.obj U) :
    (pointwiseWhiskerPreimage c hc tau U).app ((c.app U).toFunctor.obj x) =
      (tau.as.app U).toNatTrans.app x :=
  congrArg
    (fun eta : (c.app U).toFunctor ⋙ (r.app U).toFunctor ⟶
        (c.app U).toFunctor ⋙ (s.app U).toFunctor => eta.app x)
    (pointwiseWhiskerPreimage_spec c hc tau U)

/-- Pointwise preimages satisfy modification naturality. Faithful
precomposition lets us check the equation on the image of the comparison;
component naturality moves across its invertible constraint. -/
private theorem pointwiseWhiskerPreimage_naturality
    (tau : c ≫ r ⟶ c ≫ s) {U V : B} (p : U ⟶ V) :
    Functor.whiskerLeft (S.map p).toFunctor (pointwiseWhiskerPreimage c hc tau V) ≫
        (s.naturality p).hom.toNatTrans =
      (r.naturality p).hom.toNatTrans ≫
        Functor.whiskerRight (pointwiseWhiskerPreimage c hc tau U)
          (T.map p).toFunctor := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  apply ((Functor.whiskeringLeft
    (R.obj U) (S.obj U) (T.obj V)).obj (c.app U).toFunctor).map_injective
  apply NatTrans.ext
  -- `NatTrans.ext` leaves equality of the dependent component functions,
  -- not a universally quantified goal that `intro` could introduce.
  funext x
  change
    (pointwiseWhiskerPreimage c hc tau V).app
        ((S.map p).toFunctor.obj ((c.app U).toFunctor.obj x)) ≫
      (s.naturality p).hom.toNatTrans.app ((c.app U).toFunctor.obj x) =
    (r.naturality p).hom.toNatTrans.app ((c.app U).toFunctor.obj x) ≫
      (T.map p).toFunctor.map
        ((pointwiseWhiskerPreimage c hc tau U).app ((c.app U).toFunctor.obj x))
  have ht := congrArg
    (fun eta : R.map p ≫ (c ≫ r).app V ⟶ (c ≫ s).app U ≫ T.map p =>
      eta.toNatTrans.app x) (tau.as.naturality p)
  change
    (tau.as.app V).toNatTrans.app ((R.map p).toFunctor.obj x) ≫
        ((c ≫ s).naturality p).hom.toNatTrans.app x =
      ((c ≫ r).naturality p).hom.toNatTrans.app x ≫
        (T.map p).toFunctor.map ((tau.as.app U).toNatTrans.app x) at ht
  rw [compositeNaturality_app c s p x, compositeNaturality_app c r p x,
    ← pointwiseWhiskerPreimage_app c hc tau V ((R.map p).toFunctor.obj x),
    ← pointwiseWhiskerPreimage_app c hc tau U x] at ht
  -- Fix the component endpoints before applying categorical laws. Explicit
  -- proof terms avoid `rw`/`simp` matching across the Cat/functor wrappers.
  let alpha := pointwiseWhiskerPreimage c hc tau V
  let y₀ := (c.app V).toFunctor.obj ((R.map p).toFunctor.obj x)
  let y₁ := (S.map p).toFunctor.obj ((c.app U).toFunctor.obj x)
  let kIso : y₀ ≅ y₁ := (Cat.Hom.toNatIso (c.naturality p)).app x
  let k : y₀ ⟶ y₁ := kIso.hom
  let rIso := (r.app V).toFunctor.mapIso kIso
  let rMap := rIso.hom
  let sMap := (s.app V).toFunctor.map k
  let rNat := (r.naturality p).hom.toNatTrans.app ((c.app U).toFunctor.obj x)
  let sNat := (s.naturality p).hom.toNatTrans.app ((c.app U).toFunctor.obj x)
  let tail := (T.map p).toFunctor.map
    ((pointwiseWhiskerPreimage c hc tau U).app ((c.app U).toFunctor.obj x))
  -- Retain the actual mapped isomorphism instead of rediscovering `Epi rMap`
  -- through local aliases and the Cat wrappers by typeclass search.
  apply (Iso.cancel_iso_hom_left rIso (alpha.app y₁ ≫ sNat) (rNat ≫ tail)).1
  calc
    rMap ≫ (alpha.app y₁ ≫ sNat) = (rMap ≫ alpha.app y₁) ≫ sNat :=
      (Category.assoc rMap (alpha.app y₁) sNat).symm
    _ = (alpha.app y₀ ≫ sMap) ≫ sNat :=
      eq_whisker (alpha.naturality k) sNat
    _ = alpha.app y₀ ≫ (sMap ≫ sNat) :=
      Category.assoc (alpha.app y₀) sMap sNat
    _ = (rMap ≫ rNat) ≫ tail := ht
    _ = rMap ≫ (rNat ≫ tail) := Category.assoc rMap rNat tail

/-- Assemble the pointwise preimages into an actual modification. -/
def pseudofunctorWhiskerLeftPreimage (tau : c ≫ r ⟶ c ≫ s) : r ⟶ s where
  as :=
    { app U := (pointwiseWhiskerPreimage c hc tau U).toCatHom₂
      naturality p := by
        apply Cat.Hom₂.ext
        exact pointwiseWhiskerPreimage_naturality c hc tau p }

/-- The assembled modification recovers the prescribed whiskered one exactly. -/
theorem pseudofunctorWhiskerLeftPreimage_spec (tau : c ≫ r ⟶ c ≫ s) :
    c ◁ pseudofunctorWhiskerLeftPreimage c hc tau = tau := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro U
  apply Cat.Hom₂.ext
  exact pointwiseWhiskerPreimage_spec c hc tau U

include hc in
/-- Precomposition by a pointwise equivalence is full on modifications, for
Cat-valued pseudofunctors on any bicategory. -/
theorem pseudofunctorWhiskerLeft_surjective_of_pointwiseEquivalence :
    Function.Surjective (fun eta : r ⟶ s => c ◁ eta) := by
  intro tau
  exact ⟨pseudofunctorWhiskerLeftPreimage c hc tau,
    pseudofunctorWhiskerLeftPreimage_spec c hc tau⟩

-- Exercise the assembled modification over an arbitrary base bicategory.
example (tau : c ≫ r ⟶ c ≫ s) :
    c ◁ pseudofunctorWhiskerLeftPreimage c hc tau = tau :=
  pseudofunctorWhiskerLeftPreimage_spec c hc tau

end Pointwise

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Fullness of the raw comparison functor follows from the presentation
comparison's existing pointwise-equivalence field. -/
instance exactUniversalRawComparisonFunctor_full
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalRawComparisonFunctor (W := W) A X Y).Full where
  map_surjective {r s} := by
    change Function.Surjective (fun eta : r ⟶ s => X.presentation.comparison ◁ eta)
    apply pseudofunctorWhiskerLeft_surjective_of_pointwiseEquivalence
      (c := X.presentation.comparison) (r := r) (s := s)
    intro U
    rcases U with ⟨U⟩
    exact X.presentation.comparison_isEquivalence U

variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
variable {f g : ExactUniversalRawMorphism (W := W) A X Y}

/-- Construct the unique compatible source 2-cell over a prescribed DO₂
2-cell. The inverse of the first comparison square gives the raw lifting target. -/
def exactUniversalCompletion2Preimage (ell : f.lift ⟶ g.lift) : f ⟶ g := by
  let F := exactUniversalRawComparisonFunctor (W := W) A X Y
  let square : F.obj f.raw ⟶ F.obj g.raw :=
    f.comparison_square.inv ≫
      (restrictHigherLocalizedModification (W := W) ell.hom ▷
        Y.presentation.comparison) ≫ g.comparison_square.hom
  refine
    { raw := F.preimage square
      lift := ell
      compatibility := ?_ }
  change
    (restrictHigherLocalizedModification (W := W) ell.hom ▷
        Y.presentation.comparison) ≫ g.comparison_square.hom =
      f.comparison_square.hom ≫ F.map (F.preimage square)
  -- Specialize inverse cancellation to the stored comparison explicitly.
  -- This avoids asking `simp` to infer that isomorphism through the wrappers.
  calc
    _ = f.comparison_square.hom ≫ square :=
      (f.comparison_square.hom_inv_id_assoc
        ((restrictHigherLocalizedModification (W := W) ell.hom ▷
          Y.presentation.comparison) ≫ g.comparison_square.hom)).symm
    _ = f.comparison_square.hom ≫ F.map (F.preimage square) :=
      congrArg (fun m : F.obj f.raw ⟶ F.obj g.raw =>
        f.comparison_square.hom ≫ m) (F.map_preimage square).symm

/-- Fullness of the actual DO₂ realization, not merely its comma embedding. -/
instance exactUniversalCompletion2HomFunctor_full :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).Full where
  map_surjective {f g} ell :=
    ⟨exactUniversalCompletion2Preimage (W := W) A (f := f) (g := g) ell, rfl⟩

/-- The data-bearing Mathlib fully faithful interface. -/
def exactUniversalCompletion2HomFullyFaithful :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).FullyFaithful :=
  Functor.FullyFaithful.ofFullyFaithful _

/-- Exact equivalence of the source and realized 2-cell types. -/
def exactUniversalTwoCellEquivLift : (f ⟶ g) ≃ (f.lift ⟶ g.lift) where
  toFun eta := eta.lift
  invFun := exactUniversalCompletion2Preimage (W := W) A
  left_inv _ := exactUniversalCompletion2_map_injective (W := W) A rfl
  right_inv _ := rfl

/-- Every realized 2-cell has exactly one compatible source 2-cell over it. -/
theorem existsUnique_exactUniversalTwoCell_of_lift (ell : f.lift ⟶ g.lift) :
    ∃! eta : f ⟶ g, eta.lift = ell := by
  refine ⟨exactUniversalCompletion2Preimage (W := W) A ell, rfl, ?_⟩
  intro eta he
  apply exactUniversalCompletion2_map_injective (W := W) A
  exact he

/-- Mathlib lifts an arbitrary realized isomorphism between existing source
1-cells. No raw isomorphism or compatibility equation is an extra input. -/
def exactUniversalSourceIsoOfLift (ell : f.lift ≅ g.lift) : f ≅ g :=
  (exactUniversalCompletion2HomFunctor (W := W) A X Y).preimageIso
    (X := f) (Y := g) ell

/-! ## Regression checks: no extra fullness or compatibility hypotheses. -/

example : (exactUniversalRawComparisonFunctor (W := W) A X Y).Full :=
  inferInstance

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).Full :=
  inferInstance

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).Faithful :=
  inferInstance

example (ell : f.lift ⟶ g.lift) :
    (exactUniversalCompletion2Preimage (W := W) A ell).lift = ell := rfl

example (eta : f ⟶ g) :
    (exactUniversalTwoCellEquivLift (W := W) A).symm
      ((exactUniversalTwoCellEquivLift (W := W) A) eta) = eta :=
  (exactUniversalTwoCellEquivLift (W := W) A).symm_apply_apply eta

example (ell : f.lift ⟶ g.lift) :
    (exactUniversalTwoCellEquivLift (W := W) A)
      ((exactUniversalTwoCellEquivLift (W := W) A).symm ell) = ell :=
  (exactUniversalTwoCellEquivLift (W := W) A).apply_symm_apply ell

example (ell : f.lift ≅ g.lift) : Nonempty (f ≅ g) :=
  ⟨exactUniversalSourceIsoOfLift (W := W) A ell⟩

-- A lifted isomorphism must realize to the prescribed one, not just exist.
example (ell : f.lift ≅ g.lift) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).mapIso
      (exactUniversalSourceIsoOfLift (W := W) A ell) = ell := by
  apply Iso.ext
  exact (exactUniversalCompletion2HomFunctor (W := W) A X Y).map_preimage ell.hom

example (ell : f.lift ⟶ g.lift) :
    ∃! eta : f ⟶ g, eta.lift = ell :=
  existsUnique_exactUniversalTwoCell_of_lift (W := W) A ell

#print axioms pointwiseWhiskerPreimage_naturality
#print axioms pseudofunctorWhiskerLeft_surjective_of_pointwiseEquivalence
#print axioms exactUniversalCompletion2HomFullyFaithful
#print axioms exactUniversalTwoCellEquivLift
#print axioms exactUniversalSourceIsoOfLift

end

end KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
