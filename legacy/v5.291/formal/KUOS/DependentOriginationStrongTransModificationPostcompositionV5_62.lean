import KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61

namespace KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

set_option autoImplicit false

noncomputable section

/-!
# Postcomposition of StrongTrans and modifications v5.62

v5.61 constructs the precomposition half of the horizontal-whiskering
interface.  This file constructs the complementary non-strict
postcomposition operation.

For a StrongTrans alpha : F => G and a pseudofunctor H, the component of the
postcomposed transformation is H.map (alpha.app a).  Its naturality square is
the image under H of alpha.naturality, padded by H's native compositors.

The delicate points are exactly the non-strict ones:

* the identity law must retain both F.mapId and G.mapId;
* the composition law must retain both F.mapComp and G.mapComp;
* a modification is mapped by H.map₂, and its naturality is obtained by
  mapping the old modification square;
* invertibility is preserved using H.map₂_comp and H.map₂_id.

No identity-StrongTrans comparison is added here.  In general,
postcomposition of the identity StrongTrans has components H.map (𝟙 _), while
the native identity StrongTrans has components 𝟙 _.  Relating them requires
H.mapId and is therefore a separate coherence theorem, not definitional
equality.  Consequently triangulator postcomposition is intentionally deferred.
-/

namespace MappedSquarePostcomposition

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (H : Pseudofunctor B C)

/-- Map an identity square whose two horizontal edges both carry genuine
identity comparisons.  This upgrades the one-sided identity theorem from
v5.54 without assuming either edge is definitionally an identity. -/
theorem twoSidedIdentity
    {x a : B}
    (r : x ⟶ x) (f : a ⟶ a) (u : x ⟶ a)
    (er : r ≅ 𝟙 x) (ef : f ≅ 𝟙 a)
    (n : r ≫ u ≅ u ≫ f)
    (h :
      n.hom ≫ u ◁ ef.hom =
        er.hom ▷ u ≫ (λ_ u).hom ≫ (ρ_ u).inv) :
    (MappedSquare.iso H r f u u n).hom ≫
        H.map u ◁ (H.map₂ ef.hom ≫ (H.mapId a).hom) =
      (H.map₂ er.hom ≫ (H.mapId x).hom) ▷ H.map u ≫
        (λ_ (H.map u)).hom ≫ (ρ_ (H.map u)).inv := by
  let n' : r ≫ u ≅ u ≫ 𝟙 a :=
    n ≪≫ Bicategory.whiskerLeftIso u ef
  have hn' :
      n'.hom =
        er.hom ▷ u ≫ (λ_ u).hom ≫ (ρ_ u).inv := by
    simpa only [n', Iso.trans_hom, Bicategory.whiskerLeftIso_hom] using h
  have hsquare :
      (𝟙 r) ▷ u ≫ n'.hom =
        n.hom ≫ u ◁ ef.hom := by
    simp only [n', Iso.trans_hom, Bicategory.whiskerLeftIso_hom,
      Bicategory.id_whiskerRight, Category.id_comp]
  have hmapped :=
    MappedSquare.naturality
      H r r f (𝟙 a) u u n n' (𝟙 r) ef.hom hsquare
  have hstep :
      (MappedSquare.iso H r f u u n).hom ≫
          H.map u ◁ H.map₂ ef.hom =
        (MappedSquare.iso H r (𝟙 a) u u n').hom := by
    simpa only [PrelaxFunctor.map₂_id, Bicategory.id_whiskerRight,
      Category.id_comp] using hmapped.symm
  rw [Bicategory.whiskerLeft_comp, ← Category.assoc, hstep]
  exact MappedSquare.identity H r u er n' hn'

/-- Map a modification square: the horizontal edges are fixed, while the two
vertical edges vary by 2-cells. -/
theorem verticalNaturality
    {x y a b : B}
    (r : x ⟶ y) (f : a ⟶ b)
    (u u' : x ⟶ a) (v v' : y ⟶ b)
    (n : r ≫ v ≅ u ≫ f)
    (n' : r ≫ v' ≅ u' ≫ f)
    (sigma : u ⟶ u') (tau : v ⟶ v')
    (h :
      r ◁ tau ≫ n'.hom =
        n.hom ≫ sigma ▷ f) :
    H.map r ◁ H.map₂ tau ≫
        (MappedSquare.iso H r f u' v' n').hom =
      (MappedSquare.iso H r f u v n).hom ≫
        H.map₂ sigma ▷ H.map f := by
  have hm := congrArg
    (fun t =>
      (H.mapComp r v).inv ≫ H.map₂ t ≫
        (H.mapComp u' f).hom) h
  dsimp only at hm
  rw [H.map₂_comp, H.map₂_comp, H.map₂_whisker_left,
    H.map₂_whisker_right] at hm
  simp only [Category.assoc] at hm
  rw [(H.mapComp r v).inv_hom_id_assoc,
    (H.mapComp u' f).inv_hom_id, Category.comp_id] at hm
  simpa only [MappedSquare.iso_hom, Category.assoc] using hm

end MappedSquarePostcomposition

namespace StrongTransPostcomposition

universe uB vB wB uC vC wC uD vD wD

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {D : Type uD} [Bicategory.{wD, vD} D]

variable {F G : Pseudofunctor B C}
variable (H : Pseudofunctor C D)
variable (alpha : Pseudofunctor.StrongTrans F G)

local instance sourceStrongTransHomCategory
    {P Q : Pseudofunctor B C} :
    Category (Pseudofunctor.StrongTrans P Q) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := C) (F := P) (G := Q)

local instance postcomposedStrongTransHomCategory
    {P Q : Pseudofunctor B D} :
    Category (Pseudofunctor.StrongTrans P Q) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := D) (F := P) (G := Q)

/-- The mapped naturality square, padded by H's two compositors. -/
def naturalityIso {a b : B} (f : a ⟶ b) :
    H.map (F.map f) ≫ H.map (alpha.app b) ≅
      H.map (alpha.app a) ≫ H.map (G.map f) :=
  MappedSquare.iso
    H
    (F.map f) (G.map f)
    (alpha.app a) (alpha.app b)
    (alpha.naturality f)

@[simp] theorem naturalityIso_hom {a b : B} (f : a ⟶ b) :
    (naturalityIso H alpha f).hom =
      (H.mapComp (F.map f) (alpha.app b)).inv ≫
        H.map₂ (alpha.naturality f).hom ≫
        (H.mapComp (alpha.app a) (G.map f)).hom :=
  rfl

/-- Naturality in a 2-cell is the mapped horizontal-square naturality from
v5.54. -/
theorem naturality_naturality
    {a b : B} {f g : a ⟶ b} (theta : f ⟶ g) :
    (Pseudofunctor.comp F H).map₂ theta ▷
        H.map (alpha.app b) ≫
        (naturalityIso H alpha g).hom =
      (naturalityIso H alpha f).hom ≫
        H.map (alpha.app a) ◁
          (Pseudofunctor.comp G H).map₂ theta := by
  exact
    MappedSquare.naturality
      H
      (F.map f) (F.map g)
      (G.map f) (G.map g)
      (alpha.app a) (alpha.app b)
      (alpha.naturality f) (alpha.naturality g)
      (F.map₂ theta) (G.map₂ theta)
      (alpha.naturality_naturality theta)

/-- Identity coherence retains both source and target mapId comparisons. -/
theorem naturality_id (a : B) :
    (naturalityIso H alpha (𝟙 a)).hom ≫
        H.map (alpha.app a) ◁
          ((Pseudofunctor.comp G H).mapId a).hom =
      ((Pseudofunctor.comp F H).mapId a).hom ▷
          H.map (alpha.app a) ≫
        (λ_ (H.map (alpha.app a))).hom ≫
        (ρ_ (H.map (alpha.app a))).inv := by
  exact
    MappedSquarePostcomposition.twoSidedIdentity
      H
      (F.map (𝟙 a)) (G.map (𝟙 a)) (alpha.app a)
      (F.mapId a) (G.mapId a)
      (alpha.naturality (𝟙 a))
      (alpha.naturality_id a)

/-- Composition coherence retains both source and target mapComp comparisons.

The v5.54 mapped-square composition theorem expects the target edge already
expanded as `G.map f ≫ G.map g`.  We therefore compose the old naturality
square with the original target compositor first, and separately prove that
mapping this enlarged square is the same as mapping the old square and then
using the target composite pseudofunctor's compositor. -/
theorem naturality_comp
    {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    (naturalityIso H alpha (f ≫ g)).hom ≫
        H.map (alpha.app a) ◁
          ((Pseudofunctor.comp G H).mapComp f g).hom =
      ((Pseudofunctor.comp F H).mapComp f g).hom ▷
          H.map (alpha.app c) ≫
        (α_ ((Pseudofunctor.comp F H).map f)
          ((Pseudofunctor.comp F H).map g)
          (H.map (alpha.app c))).hom ≫
        (Pseudofunctor.comp F H).map f ◁
          (naturalityIso H alpha g).hom ≫
        (α_ ((Pseudofunctor.comp F H).map f)
          (H.map (alpha.app b))
          ((Pseudofunctor.comp G H).map g)).inv ≫
        (naturalityIso H alpha f).hom ▷
          (Pseudofunctor.comp G H).map g ≫
        (α_ (H.map (alpha.app a))
          ((Pseudofunctor.comp G H).map f)
          ((Pseudofunctor.comp G H).map g)).hom := by
  let nfg :
      F.map (f ≫ g) ≫ alpha.app c ≅
        alpha.app a ≫ (G.map f ≫ G.map g) :=
    alpha.naturality (f ≫ g) ≪≫
      Bicategory.whiskerLeftIso (alpha.app a) (G.mapComp f g)
  have hnfg :
      nfg.hom =
        (F.mapComp f g).hom ▷ alpha.app c ≫
          (α_ (F.map f) (F.map g) (alpha.app c)).hom ≫
          F.map f ◁ (alpha.naturality g).hom ≫
          (α_ (F.map f) (alpha.app b) (G.map g)).inv ≫
          (alpha.naturality f).hom ▷ G.map g ≫
          (α_ (alpha.app a) (G.map f) (G.map g)).hom := by
    simpa only [nfg, Iso.trans_hom, Bicategory.whiskerLeftIso_hom] using
      alpha.naturality_comp f g
  have hbridge :
      (naturalityIso H alpha (f ≫ g)).hom ≫
          H.map (alpha.app a) ◁ H.map₂ (G.mapComp f g).hom =
        (MappedSquare.iso
          H
          (F.map (f ≫ g)) (G.map f ≫ G.map g)
          (alpha.app a) (alpha.app c)
          nfg).hom := by
    simp only [naturalityIso_hom, MappedSquare.iso_hom, nfg,
      Iso.trans_hom, Bicategory.whiskerLeftIso_hom,
      PrelaxFunctor.map₂_comp, H.map₂_whisker_left,
      Category.assoc]
    rw [(H.mapComp (alpha.app a) (G.map f ≫ G.map g)).inv_hom_id,
      Category.comp_id]
  have hmapped :=
    MappedSquare.composition
      H
      (F.map f) (F.map g) (F.map (f ≫ g))
      (G.map f) (G.map g)
      (alpha.app a) (alpha.app b) (alpha.app c)
      (F.mapComp f g)
      (alpha.naturality f)
      (alpha.naturality g)
      nfg
      hnfg
  change
    (naturalityIso H alpha (f ≫ g)).hom ≫
        H.map (alpha.app a) ◁
          (H.map₂ (G.mapComp f g).hom ≫
            (H.mapComp (G.map f) (G.map g)).hom) = _
  rw [Bicategory.whiskerLeft_comp, ← Category.assoc, hbridge]
  exact hmapped

/-- Postcompose an arbitrary StrongTrans by an arbitrary pseudofunctor. -/
def strongTrans :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp F H)
      (Pseudofunctor.comp G H) where
  app a := H.map (alpha.app a)
  naturality f := naturalityIso H alpha f
  naturality_naturality theta :=
    naturality_naturality H alpha theta
  naturality_id a := naturality_id H alpha a
  naturality_comp f g := naturality_comp H alpha f g

@[simp] theorem strongTrans_app (a : B) :
    (strongTrans H alpha).app a = H.map (alpha.app a) :=
  rfl

@[simp] theorem strongTrans_naturality
    {a b : B} (f : a ⟶ b) :
    (strongTrans H alpha).naturality f =
      naturalityIso H alpha f :=
  rfl

/-- Postcompose a modification.  The component is simply H.map₂ of the old
component; the proof maps the original modification square. -/
def modification
    {alpha beta : Pseudofunctor.StrongTrans F G}
    (Gamma : Pseudofunctor.StrongTrans.Modification alpha beta) :
    Pseudofunctor.StrongTrans.Modification
      (strongTrans H alpha)
      (strongTrans H beta) where
  app a := H.map₂ (Gamma.app a)
  naturality {a b} f :=
    MappedSquarePostcomposition.verticalNaturality
      H
      (F.map f) (G.map f)
      (alpha.app a) (beta.app a)
      (alpha.app b) (beta.app b)
      (alpha.naturality f) (beta.naturality f)
      (Gamma.app a) (Gamma.app b)
      (Gamma.naturality f)

@[simp] theorem modification_app
    {alpha beta : Pseudofunctor.StrongTrans F G}
    (Gamma : Pseudofunctor.StrongTrans.Modification alpha beta)
    (a : B) :
    (modification H Gamma).app a =
      H.map₂ (Gamma.app a) :=
  rfl

/-- Postcomposition preserves an invertible modification. -/
def iso
    {alpha beta : Pseudofunctor.StrongTrans F G}
    (e :
      @CategoryTheory.Iso
        (Pseudofunctor.StrongTrans F G)
        (Pseudofunctor.StrongTrans.homCategory
          (B := B) (C := C) (F := F) (G := G))
        alpha beta) :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.comp F H)
        (Pseudofunctor.comp G H))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := D)
        (F := Pseudofunctor.comp F H)
        (G := Pseudofunctor.comp G H))
      (strongTrans H alpha)
      (strongTrans H beta) where
  hom.as := modification H e.hom.as
  inv.as := modification H e.inv.as
  hom_inv_id := by
    apply Pseudofunctor.StrongTrans.homCategory.ext
    intro a
    change
      H.map₂ (e.hom.as.app a) ≫
          H.map₂ (e.inv.as.app a) =
        𝟙 (H.map (alpha.app a))
    have hcomponent :
        e.hom.as.app a ≫ e.inv.as.app a =
          𝟙 (alpha.app a) :=
      congrArg (fun m => m.as.app a) e.hom_inv_id
    rw [← PrelaxFunctor.map₂_comp, hcomponent, PrelaxFunctor.map₂_id]
  inv_hom_id := by
    apply Pseudofunctor.StrongTrans.homCategory.ext
    intro a
    change
      H.map₂ (e.inv.as.app a) ≫
          H.map₂ (e.hom.as.app a) =
        𝟙 (H.map (beta.app a))
    have hcomponent :
        e.inv.as.app a ≫ e.hom.as.app a =
          𝟙 (beta.app a) :=
      congrArg (fun m => m.as.app a) e.inv_hom_id
    rw [← PrelaxFunctor.map₂_comp, hcomponent, PrelaxFunctor.map₂_id]

end StrongTransPostcomposition

/-!
## Boundary after v5.62

Arbitrary non-strict postcomposition is now available for

* StrongTrans;
* modification;
* invertible modification.

Unlike precomposition, postcomposition does not send the identity StrongTrans
definitionally to the native identity StrongTrans: its object component is
H.map (𝟙 _), not 𝟙 _.  The missing comparison is canonically controlled by
H.mapId.  Constructing that invertible modification is the next coherence
step required before postcomposition can act on the triangulator package.
-/

#print axioms MappedSquarePostcomposition.twoSidedIdentity
#print axioms MappedSquarePostcomposition.verticalNaturality
#print axioms StrongTransPostcomposition.naturality_id
#print axioms StrongTransPostcomposition.naturality_comp
#print axioms StrongTransPostcomposition.strongTrans
#print axioms StrongTransPostcomposition.modification
#print axioms StrongTransPostcomposition.iso

end

end KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62
