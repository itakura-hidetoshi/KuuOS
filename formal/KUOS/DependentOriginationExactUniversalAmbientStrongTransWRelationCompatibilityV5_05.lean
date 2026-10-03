import Mathlib.Tactic.CategoryTheory.Slice
import Mathlib.CategoryTheory.Bicategory.Strict.Pseudofunctor
import KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05

open CategoryTheory
open CategoryTheory.Functor
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# W-inverse relation compatibility v5.05

The v4.98 inverse naturality constructor is characterized by an exact
fully-faithful preimage specification.  Here we use that specification together
with the unit/counit equalities of a localized isomorphism to close the two
remaining localization generators.

The generic statements are made for an arbitrary isomorphism in the localized
base.  The declared W-arrow cases are then immediate specializations to
Localization.Construction.wIso.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The locally discrete 2-isomorphism recording hom followed by inv equals
identity for a localized base isomorphism. -/
noncomputable def higherLocalizedIsoHomInvRelation
    {X Y : LocalizedContext W} (e : X ≅ Y) :
    e.hom.op.op.toLoc ≫ e.inv.op.op.toLoc ≅
      𝟙 (LocallyDiscrete.mk (op (op X))) :=
  eqToIso (by
    apply Discrete.ext
    simp)

/-- The locally discrete 2-isomorphism recording inv followed by hom equals
identity for a localized base isomorphism. -/
noncomputable def higherLocalizedIsoInvHomRelation
    {X Y : LocalizedContext W} (e : X ≅ Y) :
    e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc ≅
      𝟙 (LocallyDiscrete.mk (op (op Y))) :=
  eqToIso (by
    apply Discrete.ext
    simp)

/-- Functorial cancellation when an inverse-like morphism is already
composed with a following morphism.  The cancellation equality is supplied
explicitly so this lemma works directly with Cat 2-cell components, without
passing through the NatIso conversion and relying on definitional unfolding. -/
theorem functor_map_cancel_comp_assoc
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ X) (r : X ⟶ Z)
    (hfg : f ≫ g = 𝟙 X)
    {T : D} (h : H.obj Z ⟶ T) :
    H.map f ≫ H.map (g ≫ r) ≫ h =
      H.map r ≫ h := by
  rw [H.map_comp]
  simp only [Category.assoc]
  rw [← H.map_comp_assoc, hfg, H.map_id, Category.id_comp]

/-- Functorial cancellation of an inverse-like pair when the second
morphism is already composed with one following morphism.  Unlike the reassociated
version below, this has no ambient tail metavariable, so it is stable under
`slice_lhs` on exactly two factors. -/
theorem functor_map_cancel_comp
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ X) (r : X ⟶ Z)
    (hfg : f ≫ g = 𝟙 X) :
    H.map f ≫ H.map (g ≫ r) = H.map r := by
  rw [← H.map_comp]
  rw [← Category.assoc, hfg, Category.id_comp]

/-- Functorial cancellation of an inverse-like pair after applying a functor. -/
theorem functor_map_cancel
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y : C} (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X) :
    H.map f ≫ H.map g = 𝟙 (H.obj X) := by
  rw [← H.map_comp, hfg, H.map_id]

/-- Functorial cancellation of two explicitly supplied inverse-like
morphisms inside a longer composite.  Keeping the component morphisms explicit
avoids coercion-sensitive matching through NatIso wrappers. -/
theorem functor_map_cancel_assoc
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y : C} (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    {T : D} (h : H.obj X ⟶ T) :
    H.map f ≫ H.map g ≫ h = h := by
  rw [← H.map_comp_assoc, hfg, H.map_id, Category.id_comp]

/-- Cancel an isomorphism immediately after a fixed prefix morphism.
This is the exact shape produced by `slice_lhs` at the final G-side transport
boundary, where the prefix transport and `hom` are already left-associated. -/
theorem comp_iso_hom_inv_cancel
    {C : Type*} [Category C]
    {W X Y : C} (r : W ⟶ X) (e : X ≅ Y) :
    (r ≫ e.hom) ≫ e.inv = r := by
  rw [Category.assoc, e.hom_inv_id, Category.comp_id]

/-- Bicategorical hom form of the v4.98 fully-faithful specification.
This is the exact rewrite shape needed inside the v4.99 composition formula. -/
theorem higherLocalizedStrongTransNaturality_invOfIso_spec_hom
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    F.map e.hom.op.op.toLoc ◁
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp).hom =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom.toCatHom₂ := by
  apply Cat.Hom₂.ext
  change
    Functor.whiskerLeft
        (F.map e.hom.op.op.toLoc).toFunctor
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp).hom.toNatTrans =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom
  exact congrArg Iso.hom
    (higherLocalizedStrongTransNaturality_invOfIso_spec
      (W := W) gamma e hp)

/-- Generic hom-inv compatibility: composing a supplied forward naturality
with the canonical v4.98 inverse naturality gives exactly the canonical
identity naturality transported along the hom-inv relation. -/
theorem higherLocalizedStrongTransNaturality_hom_inv_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        e.hom.op.op.toLoc e.inv.op.op.toLoc
        hp
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedIsoHomInvRelation (W := W) e)
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op X)))) := by
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext x
  have hspec := congrArg
    (fun η => η.app x)
    (congrArg Iso.hom
      (higherLocalizedStrongTransNaturality_invOfIso_spec
        (W := W) gamma e hp))
  change
    (higherLocalizedStrongTransNaturality_invOfIso
        (W := W) gamma e hp).hom.toNatTrans.app
          ((F.map e.hom.op.op.toLoc).toFunctor.obj x) =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom.app x at hspec
  simp only
    [higherLocalizedStrongTransNaturality_comp_hom,
      higherLocalizedStrongTransNaturalityTransport_hom,
      higherLocalizedStrongTransNaturality_id_hom,
      Cat.Hom₂.comp_app, Cat.whiskerLeft_app, Cat.whiskerRight_app]
  rw [hspec]
  dsimp
    [higherLocalizedStrongTransInverseWhiskeredSquare,
      higherLocalizedIsoHomInvRelation]
  simp only
    [Pseudofunctor.mapComp', Iso.trans_hom, Iso.trans_inv,
      PrelaxFunctor.map₂Iso_eqToIso, PrelaxFunctor.map₂_eqToHom,
      eqToIso.hom, eqToIso.inv]
  simp only
    [Cat.Hom.toNatTrans_comp, NatTrans.comp_app, CategoryTheory.Functor.map_comp,
      Category.id_comp, Category.comp_id]
  simp only [← Cat.Hom.toNatIso_hom, ← Cat.Hom.toNatIso_inv]
  slice_lhs 1 2 =>
    apply functor_map_cancel_comp
    exact Iso.hom_inv_id_app
      (Cat.Hom.toNatIso
        (F.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc)) x
  simp only [Category.assoc]
  slice_lhs 5 6 =>
    apply functor_map_cancel
    exact Iso.inv_hom_id_app (Cat.Hom.toNatIso hp) x
  simp only [Category.id_comp]
  slice_lhs 4 5 =>
    apply comp_iso_hom_inv_cancel
      (e := (Cat.Hom.toNatIso
        (G.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc)).app
          ((higherLocalizedStrongTransExtensionApp
            (W := W) gamma (.mk (op (op X)))).toFunctor.obj x))


/-- The component form of the strict-source pseudofunctor triangle for an
inverse pair, oriented so that the hom side ends at the target mapId.  This is
the coherence hidden in the long inv-hom component calculation below. -/
theorem pseudofunctor_inverse_pair_triangle_hom_app
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (p : a ⟶ b) (q : b ⟶ a)
    (hpq : p ≫ q = 𝟙 a) (hqp : q ≫ p = 𝟙 b)
    (x : H.obj a) :
    (H.mapComp' q p (𝟙 b) hqp).hom.toNatTrans.app
          ((H.map p).toFunctor.obj x) ≫
        (H.map p).toFunctor.map
          ((H.mapComp' p q (𝟙 a) hpq).inv.toNatTrans.app x) ≫
      (H.map p).toFunctor.map ((H.mapId a).hom.toNatTrans.app x) =
    (H.mapId b).hom.toNatTrans.app ((H.map p).toFunctor.obj x) := by
  have h :=
    H.mapComp'₀₁₃_inv_comp_mapComp'₀₂₃_hom_app
      p q p (𝟙 a) (𝟙 b) p hpq hqp (by simp) x
  simp only [Cat.Hom.comp_toFunctor, Functor.comp_obj]
  slice_lhs 1 2 =>
    rw [← h]
  simp only [Category.assoc]
  rw [Pseudofunctor.mapComp'_comp_id_inv_app_assoc,
    Pseudofunctor.mapComp'_id_comp_hom_app_assoc,
    ← CategoryTheory.Functor.map_comp,
    Cat.Hom.inv_hom_id_toNatTrans_app,
    CategoryTheory.Functor.map_id]
  simp

/-- The inverse component form of the same strict-source pseudofunctor triangle,
oriented so that the source mapId inverse is cancelled first. -/
theorem pseudofunctor_inverse_pair_triangle_inv_app
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (p : a ⟶ b) (q : b ⟶ a)
    (hpq : p ≫ q = 𝟙 a) (hqp : q ≫ p = 𝟙 b)
    (x : H.obj a) :
    (H.map p).toFunctor.map ((H.mapId a).inv.toNatTrans.app x) ≫
        (H.map p).toFunctor.map
          ((H.mapComp' p q (𝟙 a) hpq).hom.toNatTrans.app x) ≫
      (H.mapComp' q p (𝟙 b) hqp).inv.toNatTrans.app
        ((H.map p).toFunctor.obj x) =
    (H.mapId b).inv.toNatTrans.app ((H.map p).toFunctor.obj x) := by
  have h :=
    H.mapComp'₀₂₃_inv_comp_mapComp'₀₁₃_hom_app
      p q p (𝟙 a) (𝟙 b) p hpq hqp (by simp) x
  simp only [Cat.Hom.comp_toFunctor, Functor.comp_obj]
  slice_lhs 2 3 =>
    rw [← h]
  rw [Pseudofunctor.mapComp'_id_comp_inv_app_assoc,
    Pseudofunctor.mapComp'_comp_id_hom_app,
    ← CategoryTheory.Functor.map_comp_assoc,
    Cat.Hom.inv_hom_id_toNatTrans_app,
    CategoryTheory.Functor.map_id]
  simp

/-- Expand the preceding hom triangle from mapComp' to the concrete mapComp and
the two equality 2-cells carried by a localized isomorphism. -/
theorem higherLocalizedPseudofunctor_iso_inv_hom_triangle_hom_app
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (x : H.obj (.mk (op (op X)))) :
    (H.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).hom.toNatTrans.app
          ((H.map e.hom.op.op.toLoc).toFunctor.obj x) ≫
        (H.map e.hom.op.op.toLoc).toFunctor.map
          ((H.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc).inv.toNatTrans.app x ≫
            (H.map₂
              (higherLocalizedIsoHomInvRelation (W := W) e).hom).toNatTrans.app x) ≫
        (H.map e.hom.op.op.toLoc).toFunctor.map
          ((H.mapId (.mk (op (op X)))).hom.toNatTrans.app x) =
    (H.map₂ (higherLocalizedIsoInvHomRelation (W := W) e).hom).toNatTrans.app
          ((H.map e.hom.op.op.toLoc).toFunctor.obj x) ≫
      (H.mapId (.mk (op (op Y)))).hom.toNatTrans.app
        ((H.map e.hom.op.op.toLoc).toFunctor.obj x) := by
  let p := e.hom.op.op.toLoc
  let q := e.inv.op.op.toLoc
  let a := LocallyDiscrete.mk (op (op X))
  let b := LocallyDiscrete.mk (op (op Y))
  have hpq : p ≫ q = 𝟙 a := by
    apply Discrete.ext
    dsimp [p, q, a]
    simp
  have hqp : q ≫ p = 𝟙 b := by
    apply Discrete.ext
    dsimp [p, q, b]
    simp
  have h :=
    pseudofunctor_inverse_pair_triangle_hom_app
      (W := W) H p q hpq hqp x
  let k :=
    (Cat.Hom.toNatIso
      (H.map₂Iso (higherLocalizedIsoInvHomRelation (W := W) e))).app
        ((H.map p).toFunctor.obj x)
  have hk_inv :
      k.inv =
        (H.map₂ (higherLocalizedIsoInvHomRelation (W := W) e).inv).toNatTrans.app
          ((H.map p).toFunctor.obj x) := by
    rfl
  have hcompact :
      k.inv ≫
          (H.mapComp q p).hom.toNatTrans.app ((H.map p).toFunctor.obj x) ≫
        (H.map p).toFunctor.map
            ((H.mapComp p q).inv.toNatTrans.app x ≫
              (H.map₂
                (higherLocalizedIsoHomInvRelation (W := W) e).hom).toNatTrans.app x) ≫
          (H.map p).toFunctor.map
            ((H.mapId a).hom.toNatTrans.app x) =
        (H.mapId b).hom.toNatTrans.app ((H.map p).toFunctor.obj x) := by
    rw [hk_inv]
    simp only
      [p, q, Pseudofunctor.mapComp',
        Iso.trans_hom, Iso.trans_inv, Cat.Hom.toNatTrans_comp,
        NatTrans.comp_app, PrelaxFunctor.map₂Iso_eqToIso,
        eqToIso.hom, eqToIso.inv] at h
    simpa only
      [p, q, a, b, higherLocalizedIsoHomInvRelation,
        higherLocalizedIsoInvHomRelation, PrelaxFunctor.map₂_eqToHom,
        eqToIso.hom, eqToIso.inv, Category.assoc] using h
  have hcancel := (Iso.inv_comp_eq k).1 hcompact
  have hk_hom :
      k.hom =
        (H.map₂ (higherLocalizedIsoInvHomRelation (W := W) e).hom).toNatTrans.app
          ((H.map p).toFunctor.obj x) := by
    rfl
  rw [hk_hom] at hcancel
  simpa only [p, q, a, b] using hcancel

/-- Expand the inverse triangle to the concrete mapComp and equality 2-cells.
The final equality 2-cell is kept explicitly on the right, exactly as required
by the transported inv-hom identity candidate. -/
theorem higherLocalizedPseudofunctor_iso_inv_hom_triangle_inv_app
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (x : H.obj (.mk (op (op X)))) :
    (H.map e.hom.op.op.toLoc).toFunctor.map
          ((H.mapId (.mk (op (op X)))).inv.toNatTrans.app x) ≫
        (H.map e.hom.op.op.toLoc).toFunctor.map
          ((H.map₂ (higherLocalizedIsoHomInvRelation (W := W) e).inv).toNatTrans.app x) ≫
      (H.map e.hom.op.op.toLoc).toFunctor.map
          ((H.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc).hom.toNatTrans.app x) ≫
        (H.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).inv.toNatTrans.app
          ((H.map e.hom.op.op.toLoc).toFunctor.obj x) =
    (H.mapId (.mk (op (op Y)))).inv.toNatTrans.app
          ((H.map e.hom.op.op.toLoc).toFunctor.obj x) ≫
      (H.map₂ (higherLocalizedIsoInvHomRelation (W := W) e).inv).toNatTrans.app
        ((H.map e.hom.op.op.toLoc).toFunctor.obj x) := by
  let p := e.hom.op.op.toLoc
  let q := e.inv.op.op.toLoc
  let a := LocallyDiscrete.mk (op (op X))
  let b := LocallyDiscrete.mk (op (op Y))
  have hpq : p ≫ q = 𝟙 a := by
    apply Discrete.ext
    dsimp [p, q, a]
    simp
  have hqp : q ≫ p = 𝟙 b := by
    apply Discrete.ext
    dsimp [p, q, b]
    simp
  have h :=
    pseudofunctor_inverse_pair_triangle_inv_app
      (W := W) H p q hpq hqp x
  let k :=
    (Cat.Hom.toNatIso
      (H.map₂Iso (higherLocalizedIsoInvHomRelation (W := W) e))).app
        ((H.map p).toFunctor.obj x)
  have hk_hom :
      k.hom =
        (H.map₂ (higherLocalizedIsoInvHomRelation (W := W) e).hom).toNatTrans.app
          ((H.map p).toFunctor.obj x) := by
    rfl
  have h' :
      (H.map p).toFunctor.map ((H.mapId a).inv.toNatTrans.app x) ≫
          (H.map p).toFunctor.map
            ((H.map₂ (higherLocalizedIsoHomInvRelation (W := W) e).inv).toNatTrans.app x) ≫
        (H.map p).toFunctor.map
            ((H.mapComp p q).hom.toNatTrans.app x) ≫
          (H.mapComp q p).inv.toNatTrans.app ((H.map p).toFunctor.obj x) ≫
            k.hom =
        (H.mapId b).inv.toNatTrans.app ((H.map p).toFunctor.obj x) := by
    rw [hk_hom]
    simpa only
      [p, q, a, b, Pseudofunctor.mapComp',
        Iso.trans_hom, Iso.trans_inv, Cat.Hom.toNatTrans_comp,
        NatTrans.comp_app, CategoryTheory.Functor.map_comp,
        Category.assoc, higherLocalizedIsoHomInvRelation,
        higherLocalizedIsoInvHomRelation,
        PrelaxFunctor.map₂Iso_eqToIso, PrelaxFunctor.map₂_eqToHom,
        eqToIso.hom, eqToIso.inv] using h
  have hk_cancel :
      ((H.map p).toFunctor.map ((H.mapId a).inv.toNatTrans.app x) ≫
          (H.map p).toFunctor.map
            ((H.map₂ (higherLocalizedIsoHomInvRelation (W := W) e).inv).toNatTrans.app x) ≫
        (H.map p).toFunctor.map
            ((H.mapComp p q).hom.toNatTrans.app x) ≫
          (H.mapComp q p).inv.toNatTrans.app ((H.map p).toFunctor.obj x)) ≫
            k.hom =
        (H.mapId b).inv.toNatTrans.app ((H.map p).toFunctor.obj x) := by
    simpa only [Category.assoc] using h'
  have hfinal :
      (H.map p).toFunctor.map ((H.mapId a).inv.toNatTrans.app x) ≫
          (H.map p).toFunctor.map
            ((H.map₂ (higherLocalizedIsoHomInvRelation (W := W) e).inv).toNatTrans.app x) ≫
        (H.map p).toFunctor.map
            ((H.mapComp p q).hom.toNatTrans.app x) ≫
          (H.mapComp q p).inv.toNatTrans.app ((H.map p).toFunctor.obj x) =
        (H.mapId b).inv.toNatTrans.app ((H.map p).toFunctor.obj x) ≫
          k.inv :=
    (Iso.eq_comp_inv k).2 hk_cancel
  simpa only [p, q, a, b, k, Cat.Hom.toNatIso_inv] using hfinal

/-- Generic inv-hom compatibility.  We compare after precomposition by the
forward image of the localized isomorphism; this is faithful because that image
is an equivalence.  The proof is then split into the two strict-source
pseudofunctor inverse-pair triangles and ordinary naturality of the supplied
forward square. -/
theorem higherLocalizedStrongTransNaturality_inv_hom_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        e.inv.op.op.toLoc e.hom.op.op.toLoc
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp)
        hp =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedIsoInvHomRelation (W := W) e)
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op Y)))) := by
  letI : (F.map e.hom.op.op.toLoc).toFunctor.IsEquivalence :=
    pseudofunctor_map_of_isIso_isEquivalence F e.hom.op.op
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply
    ((whiskeringLeft
      (F.obj (.mk (op (op X))))
      (F.obj (.mk (op (op Y))))
      (G.obj (.mk (op (op Y))))).obj
        (F.map e.hom.op.op.toLoc).toFunctor).map_injective
  apply NatTrans.ext
  funext x
  have hspec := congrArg
    (fun η => η.app x)
    (congrArg Iso.hom
      (higherLocalizedStrongTransNaturality_invOfIso_spec
        (W := W) gamma e hp))
  change
    (higherLocalizedStrongTransNaturality_invOfIso
        (W := W) gamma e hp).hom.toNatTrans.app
          ((F.map e.hom.op.op.toLoc).toFunctor.obj x) =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom.app x at hspec
  simp only
    [Functor.whiskeringLeft_obj_map, Functor.whiskerLeft_app,
      higherLocalizedStrongTransNaturality_comp_hom,
      higherLocalizedStrongTransNaturalityTransport_hom,
      higherLocalizedStrongTransNaturality_id_hom,
      Cat.Hom₂.comp_app, Cat.whiskerLeft_app, Cat.whiskerRight_app]
  rw [hspec]
  dsimp
    [higherLocalizedStrongTransInverseWhiskeredSquare,
      higherLocalizedIsoInvHomRelation]
  simp only
    [Pseudofunctor.mapComp', Iso.trans_hom, Iso.trans_inv,
      PrelaxFunctor.map₂Iso_eqToIso, PrelaxFunctor.map₂_eqToHom,
      eqToIso.hom, eqToIso.inv]
  simp only
    [Cat.Hom.toNatTrans_comp, NatTrans.comp_app,
      CategoryTheory.Functor.map_comp, Category.id_comp, Category.comp_id]
  let p := e.hom.op.op.toLoc
  let q := e.inv.op.op.toLoc
  let aX := (higherLocalizedStrongTransExtensionApp
    (W := W) gamma (.mk (op (op X)))).toFunctor
  let aY := (higherLocalizedStrongTransExtensionApp
    (W := W) gamma (.mk (op (op Y)))).toFunctor
  let Fp := (F.map p).toFunctor
  let Fq := (F.map q).toFunctor
  let Gp := (G.map p).toFunctor
  let Gq := (G.map q).toFunctor
  let mFpre :=
    (F.mapComp p q).inv.toNatTrans.app x ≫
      (F.map₂
        (higherLocalizedIsoHomInvRelation (W := W) e).hom).toNatTrans.app x
  let mF :=
    mFpre ≫ (F.mapId (.mk (op (op X)))).hom.toNatTrans.app x

  have hhp := hp.hom.toNatTrans.naturality mF
  have hhp' :
      hp.hom.toNatTrans.app (Fq.obj (Fp.obj x)) ≫
          Gp.map (aX.map mFpre) ≫
        Gp.map (aX.map
          ((F.mapId (.mk (op (op X)))).hom.toNatTrans.app x)) =
        aY.map (Fp.map mFpre) ≫
          aY.map (Fp.map
            ((F.mapId (.mk (op (op X)))).hom.toNatTrans.app x)) ≫
          hp.hom.toNatTrans.app x := by
    simpa only
      [mF, Functor.comp_map, CategoryTheory.Functor.map_comp,
        Category.assoc] using hhp.symm
  dsimp [p, q, aX, aY, Fp, Fq, Gp, Gq, mFpre] at hhp'
  simp only
    [higherLocalizedIsoHomInvRelation, eqToIso.hom,
      PrelaxFunctor.map₂_eqToHom] at hhp'
  simp only [Category.assoc]
  slice_lhs 2 4 =>
    exact hhp'

  have hFtri :=
    higherLocalizedPseudofunctor_iso_inv_hom_triangle_hom_app
      (W := W) F e x
  have hFtriCompact :
      (F.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).hom.toNatTrans.app
            ((F.map e.hom.op.op.toLoc).toFunctor.obj x) ≫
          (F.map e.hom.op.op.toLoc).toFunctor.map mFpre ≫
        (F.map e.hom.op.op.toLoc).toFunctor.map
          ((F.mapId (.mk (op (op X)))).hom.toNatTrans.app x) =
      (F.map₂
          (higherLocalizedIsoInvHomRelation (W := W) e).hom).toNatTrans.app
            ((F.map e.hom.op.op.toLoc).toFunctor.obj x) ≫
        (F.mapId (.mk (op (op Y)))).hom.toNatTrans.app
          ((F.map e.hom.op.op.toLoc).toFunctor.obj x) := by
    dsimp [mFpre, p, q]
    exact hFtri
  have hFmapped :=
    congrArg
      (fun m =>
        (higherLocalizedStrongTransExtensionApp
          (W := W) gamma (.mk (op (op Y)))).toFunctor.map m)
      hFtriCompact
  simp only [CategoryTheory.Functor.map_comp] at hFmapped
  dsimp [mFpre] at hFmapped
  simp only
    [higherLocalizedIsoHomInvRelation, higherLocalizedIsoInvHomRelation,
      eqToIso.hom, PrelaxFunctor.map₂_eqToHom] at hFmapped
  slice_lhs 1 3 =>
    exact hFmapped

  have hGcomp :=
    (G.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).inv.toNatTrans.naturality
      (hp.inv.toNatTrans.app x)
  have hGcomp' :
      (G.map e.hom.op.op.toLoc).toFunctor.map
            ((G.map e.inv.op.op.toLoc).toFunctor.map
              (hp.inv.toNatTrans.app x)) ≫
        (G.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).inv.toNatTrans.app
          ((higherLocalizedStrongTransExtensionApp
            (W := W) gamma (.mk (op (op Y)))).toFunctor.obj
              ((F.map e.hom.op.op.toLoc).toFunctor.obj x)) =
      (G.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).inv.toNatTrans.app
          ((G.map e.hom.op.op.toLoc).toFunctor.obj
            ((higherLocalizedStrongTransExtensionApp
              (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) ≫
        (G.map
          (e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc)).toFunctor.map
            (hp.inv.toNatTrans.app x) := by
    simpa only [Functor.comp_map] using hGcomp
  slice_lhs 5 6 =>
    exact hGcomp'

  have hGtri :=
    higherLocalizedPseudofunctor_iso_inv_hom_triangle_inv_app
      (W := W) G e
      ((higherLocalizedStrongTransExtensionApp
        (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)
  have hGtriCompact :
      (G.map e.hom.op.op.toLoc).toFunctor.map
            ((G.mapId (.mk (op (op X)))).inv.toNatTrans.app
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) ≫
        (G.map e.hom.op.op.toLoc).toFunctor.map
          ((G.map₂
              (higherLocalizedIsoHomInvRelation (W := W) e).inv).toNatTrans.app
                ((higherLocalizedStrongTransExtensionApp
                  (W := W) gamma (.mk (op (op X)))).toFunctor.obj x) ≫
            (G.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc).hom.toNatTrans.app
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) ≫
          (G.mapComp e.inv.op.op.toLoc e.hom.op.op.toLoc).inv.toNatTrans.app
            ((G.map e.hom.op.op.toLoc).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) =
      (G.mapId (.mk (op (op Y)))).inv.toNatTrans.app
            ((G.map e.hom.op.op.toLoc).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) ≫
        (G.map₂
          (higherLocalizedIsoInvHomRelation (W := W) e).inv).toNatTrans.app
            ((G.map e.hom.op.op.toLoc).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) := by
    rw [(G.map e.hom.op.op.toLoc).toFunctor.map_comp]
    exact hGtri
  simp only
    [higherLocalizedIsoHomInvRelation, higherLocalizedIsoInvHomRelation,
      eqToIso.hom, eqToIso.inv, PrelaxFunctor.map₂_eqToHom] at hGtriCompact
  slice_lhs 4 6 =>
    exact hGtriCompact

  let tG :
      𝟭 (G.obj (.mk (op (op Y)))) ⟶
        (G.map (e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc)).toFunctor :=
    (G.mapId (.mk (op (op Y)))).inv.toNatTrans ≫
      (G.map₂
        (higherLocalizedIsoInvHomRelation (W := W) e).inv).toNatTrans
  have ht := tG.naturality (hp.hom.toNatTrans.app x)
  have ht' := congrArg
    (fun m =>
      m ≫
        (G.map
          (e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc)).toFunctor.map
            (hp.inv.toNatTrans.app x))
    ht
  have hGsuffix :
      hp.hom.toNatTrans.app x ≫
          (G.mapId (.mk (op (op Y)))).inv.toNatTrans.app
            ((G.map e.hom.op.op.toLoc).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) ≫
        (G.map₂
          (higherLocalizedIsoInvHomRelation (W := W) e).inv).toNatTrans.app
            ((G.map e.hom.op.op.toLoc).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)) ≫
          (G.map
            (e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc)).toFunctor.map
              (hp.inv.toNatTrans.app x) =
        (G.mapId (.mk (op (op Y)))).inv.toNatTrans.app
            ((higherLocalizedStrongTransExtensionApp
              (W := W) gamma (.mk (op (op Y)))).toFunctor.obj
                ((F.map e.hom.op.op.toLoc).toFunctor.obj x)) ≫
          (G.map₂
            (higherLocalizedIsoInvHomRelation (W := W) e).inv).toNatTrans.app
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma (.mk (op (op Y)))).toFunctor.obj
                  ((F.map e.hom.op.op.toLoc).toFunctor.obj x)) := by
    simpa only
      [tG, NatTrans.comp_app, Functor.id_map, Category.assoc,
        ← CategoryTheory.Functor.map_comp,
        ← Cat.Hom.toNatIso_hom, ← Cat.Hom.toNatIso_inv,
        Iso.hom_inv_id_app, CategoryTheory.Functor.map_id,
        Category.comp_id] using ht'
  simp only
    [higherLocalizedIsoInvHomRelation, eqToIso.inv,
      PrelaxFunctor.map₂_eqToHom] at hGsuffix
  slice_lhs 3 6 =>
    exact hGsuffix


/-! ## Declared W-arrow specializations -/

/-- The v4.97 presentation naturality rewritten at the exact localized
Q.map arrow used by Localization.Construction.wIso. -/
noncomputable def higherLocalizedStrongTransWForwardNaturalityV5_05
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (w : X ⟶ Y) :
    F.map (W.Q.map w).op.op.toLoc ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op (W.Q.obj Y)))) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op (W.Q.obj X)))) ≫
        G.map (W.Q.map w).op.op.toLoc := by
  simpa [higherPresentationUnitFunctor] using
    (higherLocalizedStrongTransPresentationNaturality
      (W := W) gamma w.toLoc)

/-- The canonical v4.98 inverse naturality, with its forward input normalized
to the exact Q.map presentation above. -/
noncomputable def higherLocalizedStrongTransWInverseNaturalityV5_05
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    F.map (Localization.Construction.wInv w hw).op.op.toLoc ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op (W.Q.obj X)))) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            (.mk (op (op (W.Q.obj Y)))) ≫
        G.map (Localization.Construction.wInv w hw).op.op.toLoc :=
  higherLocalizedStrongTransNaturality_invOfIso
    (W := W) gamma
    (Localization.Construction.wIso w hw)
    (higherLocalizedStrongTransWForwardNaturalityV5_05
      (W := W) gamma w)

/-- Winv₁ specialization: Q(w) followed by wInv(w) reduces to canonical
identity naturality at Q(X). -/
theorem higherLocalizedStrongTransNaturality_Winv1_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        (W.Q.map w).op.op.toLoc
        (Localization.Construction.wInv w hw).op.op.toLoc
        (higherLocalizedStrongTransWForwardNaturalityV5_05
          (W := W) gamma w)
        (higherLocalizedStrongTransWInverseNaturalityV5_05
          (W := W) gamma w hw) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedIsoHomInvRelation
          (W := W) (Localization.Construction.wIso w hw))
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op (W.Q.obj X))))) := by
  exact
    higherLocalizedStrongTransNaturality_hom_inv_transport
      (W := W) gamma
      (Localization.Construction.wIso w hw)
      (higherLocalizedStrongTransWForwardNaturalityV5_05
        (W := W) gamma w)

/-- Winv₂ specialization: wInv(w) followed by Q(w) reduces to canonical
identity naturality at Q(Y). -/
theorem higherLocalizedStrongTransNaturality_Winv2_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        (Localization.Construction.wInv w hw).op.op.toLoc
        (W.Q.map w).op.op.toLoc
        (higherLocalizedStrongTransWInverseNaturalityV5_05
          (W := W) gamma w hw)
        (higherLocalizedStrongTransWForwardNaturalityV5_05
          (W := W) gamma w) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedIsoInvHomRelation
          (W := W) (Localization.Construction.wIso w hw))
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op (W.Q.obj Y))))) := by
  exact
    higherLocalizedStrongTransNaturality_inv_hom_transport
      (W := W) gamma
      (Localization.Construction.wIso w hw)
      (higherLocalizedStrongTransWForwardNaturalityV5_05
        (W := W) gamma w)

/-! ## Regression checks -/

#print axioms higherLocalizedIsoHomInvRelation
#print axioms higherLocalizedIsoInvHomRelation
#print axioms functor_map_cancel_comp
#print axioms functor_map_cancel
#print axioms functor_map_cancel_comp_assoc
#print axioms functor_map_cancel_assoc
#print axioms comp_iso_hom_inv_cancel
#print axioms higherLocalizedStrongTransNaturality_invOfIso_spec_hom
#print axioms pseudofunctor_inverse_pair_triangle_hom_app
#print axioms pseudofunctor_inverse_pair_triangle_inv_app
#print axioms higherLocalizedPseudofunctor_iso_inv_hom_triangle_hom_app
#print axioms higherLocalizedPseudofunctor_iso_inv_hom_triangle_inv_app
#print axioms higherLocalizedStrongTransNaturality_hom_inv_transport
#print axioms higherLocalizedStrongTransNaturality_inv_hom_transport
#print axioms higherLocalizedStrongTransWForwardNaturalityV5_05
#print axioms higherLocalizedStrongTransWInverseNaturalityV5_05
#print axioms higherLocalizedStrongTransNaturality_Winv1_transport
#print axioms higherLocalizedStrongTransNaturality_Winv2_transport

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05
