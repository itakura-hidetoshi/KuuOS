import Mathlib.CategoryTheory.Bicategory.Adjunction.Cat
import Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo
import Mathlib.CategoryTheory.Equivalence

namespace KUOS.DependentOriginationPointwiseInverseNaturalityV4_81

open CategoryTheory
open CategoryTheory.Functor
open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Constructing inverse naturality squares from pointwise equivalences v4.81

v4.80 reduces arbitrary DO2 one-cell lifting to a coherent retraction of the
chosen presentation comparison. Here we begin constructing that retraction
from the EXISTING pointwise-equivalence hypothesis, not from an assumed inverse
StrongTrans or from assumed liftability.

For a Cat-valued strong transformation c : R --> S on any base bicategory,
choose the Mathlib inverse functor d_U of each component c_U. For every base
one-cell p : U --> V, construct an actual natural isomorphism

  S(p) >> d_V ~= d_U >> R(p).

Precomposition by c_U is fully faithful. Its preimageIso lifts the square
obtained by conjugating c's naturality isomorphism with the chosen component
units. The lifted isomorphism satisfies the unit comparison equation exactly;
that equation determines it uniquely, including its inverse.

This file proves existence and uniqueness of the inverse naturality squares,
not yet their coherence with identities, composites, or base two-cells. Thus it
does NOT yet assemble a StrongTrans, a global invertible modification, the
v4.80 retraction, or unconditional P1. The next step is to use the exact unit
equation and uniqueness to prove those coherence laws. No source object is
strengthened and no weak admissibility hypothesis is promoted to exactness.

The module is independent of the KuuOS history spine: the construction is valid
for arbitrary Cat-valued pseudofunctors, not only for the chosen presentations.
-/

universe uB vB wB uH vH

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {R S : Pseudofunctor B Cat.{vH, uH}}
variable (c : R ⟶ S)
variable (hc : ∀ U : B, (c.app U).toFunctor.IsEquivalence)

/-- Choose the component equivalence from the given IsEquivalence proof. -/
def pointwiseInverseEquivalence (U : B) : R.obj U ≌ S.obj U := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  exact (c.app U).toFunctor.asEquivalence

/-- The inverse component, with no global inverse transformation as input. -/
abbrev pointwiseInverseComponent (U : B) : S.obj U ⥤ R.obj U :=
  (pointwiseInverseEquivalence c hc U).inverse

/-- Retain the actual chosen unit rather than just its existence. -/
def pointwiseInverseUnitIso (U : B) :
    𝟭 (R.obj U) ≅ (c.app U).toFunctor ⋙ pointwiseInverseComponent c hc U :=
  (pointwiseInverseEquivalence c hc U).unitIso

/-- The component counit is available too; the square construction below uses
only the units and fullness of precomposition. -/
def pointwiseInverseCounitIso (U : B) :
    pointwiseInverseComponent c hc U ⋙ (c.app U).toFunctor ≅ 𝟭 (S.obj U) :=
  (pointwiseInverseEquivalence c hc U).counitIso

variable {U V : B}

/-- Conjugate the original naturality square into the image of precomposition.
All eight factors have explicit endpoints and retain the functor associators
and unitors, whose components will be simplified only after evaluation. -/
def pointwiseInverseWhiskeredSquare (p : U ⟶ V) :
    (c.app U).toFunctor ⋙
        ((S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V) ≅
      (c.app U).toFunctor ⋙
        (pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor) :=
  (Functor.associator (c.app U).toFunctor (S.map p).toFunctor
      (pointwiseInverseComponent c hc V)).symm ≪≫
    isoWhiskerRight (Cat.Hom.toNatIso (c.naturality p)).symm
      (pointwiseInverseComponent c hc V) ≪≫
    Functor.associator (R.map p).toFunctor (c.app V).toFunctor
      (pointwiseInverseComponent c hc V) ≪≫
    isoWhiskerLeft (R.map p).toFunctor (pointwiseInverseUnitIso c hc V).symm ≪≫
    Functor.rightUnitor (R.map p).toFunctor ≪≫
    (Functor.leftUnitor (R.map p).toFunctor).symm ≪≫
    isoWhiskerRight (pointwiseInverseUnitIso c hc U) (R.map p).toFunctor ≪≫
    Functor.associator (c.app U).toFunctor (pointwiseInverseComponent c hc U)
      (R.map p).toFunctor

/-- Construct the inverse naturality isomorphism by Mathlib's fully faithful
precomposition. These explicit endpoints are objects of a FUNCTOR category. -/
def pointwiseInverseNaturalityIso (p : U ⟶ V) :
    (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V ≅
      pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  exact ((whiskeringLeft (R.obj U) (S.obj U) (R.obj V)).obj
    (c.app U).toFunctor).preimageIso
      (X := (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V)
      (Y := pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor)
      (pointwiseInverseWhiskeredSquare c hc p)

/-- Recover the entire prescribed forward natural transformation exactly. -/
theorem pointwiseInverseNaturalityIso_hom_spec (p : U ⟶ V) :
    whiskerLeft (c.app U).toFunctor (pointwiseInverseNaturalityIso c hc p).hom =
      (pointwiseInverseWhiskeredSquare c hc p).hom := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  exact ((whiskeringLeft (R.obj U) (S.obj U) (R.obj V)).obj
    (c.app U).toFunctor).map_preimage
      (X := (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V)
      (Y := pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor)
      (pointwiseInverseWhiskeredSquare c hc p).hom

/-- The inverse also recovers exactly, using the reversed source endpoints. -/
theorem pointwiseInverseNaturalityIso_inv_spec (p : U ⟶ V) :
    whiskerLeft (c.app U).toFunctor (pointwiseInverseNaturalityIso c hc p).inv =
      (pointwiseInverseWhiskeredSquare c hc p).inv := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  exact ((whiskeringLeft (R.obj U) (S.obj U) (R.obj V)).obj
    (c.app U).toFunctor).map_preimage
      (X := pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor)
      (Y := (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V)
      (pointwiseInverseWhiskeredSquare c hc p).inv

/-- Recovery as a complete natural isomorphism, not merely on its objects. -/
theorem pointwiseInverseNaturalityIso_spec (p : U ⟶ V) :
    isoWhiskerLeft (c.app U).toFunctor (pointwiseInverseNaturalityIso c hc p) =
      pointwiseInverseWhiskeredSquare c hc p := by
  apply Iso.ext
  exact pointwiseInverseNaturalityIso_hom_spec c hc p

/-- On the image of c_U, the inverse square has the explicit unit formula. -/
theorem pointwiseInverseNaturalityIso_hom_app (p : U ⟶ V) (x : R.obj U) :
    (pointwiseInverseNaturalityIso c hc p).hom.app ((c.app U).toFunctor.obj x) =
      (pointwiseInverseComponent c hc V).map
          ((c.naturality p).inv.toNatTrans.app x) ≫
        (pointwiseInverseUnitIso c hc V).inv.app ((R.map p).toFunctor.obj x) ≫
          (R.map p).toFunctor.map ((pointwiseInverseUnitIso c hc U).hom.app x) := by
  have h := NatTrans.congr_app (pointwiseInverseNaturalityIso_hom_spec c hc p) x
  change
    (pointwiseInverseNaturalityIso c hc p).hom.app ((c.app U).toFunctor.obj x) =
      𝟙 _ ≫ (pointwiseInverseComponent c hc V).map
          ((c.naturality p).inv.toNatTrans.app x) ≫
        𝟙 _ ≫ (pointwiseInverseUnitIso c hc V).inv.app
          ((R.map p).toFunctor.obj x) ≫
        𝟙 _ ≫ 𝟙 _ ≫ (R.map p).toFunctor.map
          ((pointwiseInverseUnitIso c hc U).hom.app x) ≫ 𝟙 _ at h
  simpa only [Category.id_comp, Category.comp_id] using h

/-- The concrete equation needed for the component units to form a modification
once the inverse StrongTrans laws have been assembled. -/
def InverseNaturalityUnitCompatible (p : U ⟶ V)
    (nu : (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V ≅
      pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor) : Prop :=
  ∀ x : R.obj U,
    (pointwiseInverseComponent c hc V).map
        ((c.naturality p).hom.toNatTrans.app x) ≫
      nu.hom.app ((c.app U).toFunctor.obj x) =
    (pointwiseInverseUnitIso c hc V).inv.app ((R.map p).toFunctor.obj x) ≫
      (R.map p).toFunctor.map ((pointwiseInverseUnitIso c hc U).hom.app x)

/-- The constructed inverse squares satisfy the unit equation; compatibility
is a proved output, not an extra hypothesis used in the construction. -/
theorem pointwiseInverseNaturalityIso_unitCompatible (p : U ⟶ V) :
    InverseNaturalityUnitCompatible c hc p (pointwiseInverseNaturalityIso c hc p) := by
  intro x
  let k := (pointwiseInverseComponent c hc V).mapIso
    ((Cat.Hom.toNatIso (c.naturality p)).app x)
  let tail :=
    (pointwiseInverseUnitIso c hc V).inv.app ((R.map p).toFunctor.obj x) ≫
      (R.map p).toFunctor.map ((pointwiseInverseUnitIso c hc U).hom.app x)
  calc
    _ = k.hom ≫ (k.inv ≫ tail) :=
      congrArg
        (fun m :
          (pointwiseInverseComponent c hc V).obj
              ((S.map p).toFunctor.obj ((c.app U).toFunctor.obj x)) ⟶
            (R.map p).toFunctor.obj
              ((pointwiseInverseComponent c hc U).obj ((c.app U).toFunctor.obj x)) =>
          k.hom ≫ m)
        (pointwiseInverseNaturalityIso_hom_app c hc p x)
    _ = tail := k.hom_inv_id_assoc tail

/-- Unit compatibility determines the inverse square uniquely. Faithfulness
checks equality after precomposition, and mapped original naturality isomorphisms
can be cancelled without rediscovering Epi instances through aliases. -/
theorem pointwiseInverseNaturalityIso_unique (p : U ⟶ V)
    (nu : (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V ≅
      pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor)
    (hnu : InverseNaturalityUnitCompatible c hc p nu) :
    nu = pointwiseInverseNaturalityIso c hc p := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  apply Iso.ext
  apply ((whiskeringLeft (R.obj U) (S.obj U) (R.obj V)).obj
    (c.app U).toFunctor).map_injective
  apply NatTrans.ext
  funext x
  change nu.hom.app ((c.app U).toFunctor.obj x) =
    (pointwiseInverseNaturalityIso c hc p).hom.app ((c.app U).toFunctor.obj x)
  let k := (pointwiseInverseComponent c hc V).mapIso
    ((Cat.Hom.toNatIso (c.naturality p)).app x)
  apply (Iso.cancel_iso_hom_left k _ _).1
  exact (hnu x).trans (pointwiseInverseNaturalityIso_unitCompatible c hc p x).symm

/-- Each inverse naturality square exists uniquely from pointwise equivalence
alone. This is not yet the full collection of StrongTrans coherence laws. -/
theorem existsUnique_pointwiseInverseNaturalityIso (p : U ⟶ V) :
    ∃! nu : (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V ≅
        pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor,
      InverseNaturalityUnitCompatible c hc p nu := by
  refine ⟨pointwiseInverseNaturalityIso c hc p,
    pointwiseInverseNaturalityIso_unitCompatible c hc p, ?_⟩
  intro nu hnu
  exact pointwiseInverseNaturalityIso_unique c hc p nu hnu

/-! ## Regression checks: pointwise inputs only; both isomorphism directions. -/

example (U : B) : (pointwiseInverseEquivalence c hc U).functor =
    (c.app U).toFunctor := rfl

example (U : B) :
    𝟭 (R.obj U) ≅ (c.app U).toFunctor ⋙ pointwiseInverseComponent c hc U :=
  pointwiseInverseUnitIso c hc U

example (U : B) :
    pointwiseInverseComponent c hc U ⋙ (c.app U).toFunctor ≅ 𝟭 (S.obj U) :=
  pointwiseInverseCounitIso c hc U

example (p : U ⟶ V) :
    (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V ≅
      pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor :=
  pointwiseInverseNaturalityIso c hc p

example (p : U ⟶ V) :
    isoWhiskerLeft (c.app U).toFunctor (pointwiseInverseNaturalityIso c hc p) =
      pointwiseInverseWhiskeredSquare c hc p :=
  pointwiseInverseNaturalityIso_spec c hc p

example (p : U ⟶ V) :
    whiskerLeft (c.app U).toFunctor (pointwiseInverseNaturalityIso c hc p).inv =
      (pointwiseInverseWhiskeredSquare c hc p).inv :=
  pointwiseInverseNaturalityIso_inv_spec c hc p

example (p : U ⟶ V) :
    InverseNaturalityUnitCompatible c hc p (pointwiseInverseNaturalityIso c hc p) :=
  pointwiseInverseNaturalityIso_unitCompatible c hc p

example (p : U ⟶ V) :
    ∃! nu : (S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V ≅
        pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor,
      InverseNaturalityUnitCompatible c hc p nu :=
  existsUnique_pointwiseInverseNaturalityIso c hc p

example (p : U ⟶ V) {x y : S.obj U} (h : x ⟶ y) :
    ((S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V).map h ≫
        (pointwiseInverseNaturalityIso c hc p).hom.app y =
      (pointwiseInverseNaturalityIso c hc p).hom.app x ≫
        (pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor).map h :=
  (pointwiseInverseNaturalityIso c hc p).hom.naturality h

example (p : U ⟶ V) {x y : S.obj U} (h : x ⟶ y) :
    (pointwiseInverseComponent c hc U ⋙ (R.map p).toFunctor).map h ≫
        (pointwiseInverseNaturalityIso c hc p).inv.app y =
      (pointwiseInverseNaturalityIso c hc p).inv.app x ≫
        ((S.map p).toFunctor ⋙ pointwiseInverseComponent c hc V).map h :=
  (pointwiseInverseNaturalityIso c hc p).inv.naturality h

#print axioms pointwiseInverseNaturalityIso
#print axioms pointwiseInverseNaturalityIso_spec
#print axioms pointwiseInverseNaturalityIso_inv_spec
#print axioms pointwiseInverseNaturalityIso_hom_app
#print axioms pointwiseInverseNaturalityIso_unitCompatible
#print axioms existsUnique_pointwiseInverseNaturalityIso

end

end KUOS.DependentOriginationPointwiseInverseNaturalityV4_81
