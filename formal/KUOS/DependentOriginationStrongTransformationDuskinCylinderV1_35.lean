import KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34
import Mathlib.CategoryTheory.Bicategory.Product
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open CategoryTheory.Prod
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34

universe u u₀ u₁ u₂ v v₀ v₁ v₂ w w₀ w₁ w₂

/-!
# Strong-transformation Duskin cylinder v1.35

A normal-lax cylinder gives a single global Duskin prism.  Bundled simplicial
maps are kept on the same-universe boundary already used by v1.27--v1.34;
degreewise normal-lax constructions remain universe-polymorphic.
-/

/-! ## Pairing normal lax functors -/

/-- Extensionality for 2-cells in Mathlib's product bicategory. -/
private theorem prodTwoCell_ext
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {X Y : B × C} {f g : X ⟶ Y} {η θ : f ⟶ g}
    (h₁ : η.1 = θ.1) (h₂ : η.2 = θ.2) : η = θ :=
  Prod.ext h₁ h₂

attribute [local ext] prodTwoCell_ext

/-- Pair normal lax functors with a common source into the product bicategory. -/
def normalLaxPair
    {A : Type u₀} [Bicategory.{w₀, v₀} A]
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryLaxFunctor A B)
    (G : StrictlyUnitaryLaxFunctor A C) :
    StrictlyUnitaryLaxFunctor A (B × C) :=
  StrictlyUnitaryLaxFunctor.mk'
  { obj := fun X => (F.obj X, G.obj X)
    map := fun f => F.map f ×ₘ G.map f
    map_id := by
      intro X
      ext <;> simp [F.map_id, G.map_id]
    map₂ := fun η => F.map₂ η ×ₘ G.map₂ η
    map₂_id := by
      intro X Y f
      ext <;> simp
    map₂_comp := by
      intro X Y f g h η θ
      ext <;> simp
    mapComp := fun f g => F.mapComp f g ×ₘ G.mapComp f g
    mapComp_naturality_left := by
      intro a b c f f' η g
      ext <;> simp
    mapComp_naturality_right := by
      intro a b c f g g' η
      ext <;> simp
    map₂_leftUnitor := by
      intro a b f
      ext <;> simp [F.map₂_leftUnitor, G.map₂_leftUnitor]
    map₂_rightUnitor := by
      intro a b f
      ext <;> simp [F.map₂_rightUnitor, G.map₂_rightUnitor]
    map₂_associator := by
      intro a b c d f g h
      ext <;> simp [F.map₂_associator, G.map₂_associator] }

attribute [local ext] StrictlyUnitaryLaxFunctor

/-- Pairing commutes with precomposition by another normal lax functor. -/
theorem normalLaxPair_precomp
    {A₀ : Type u₀} [Bicategory.{w₀, v₀} A₀]
    {A : Type u₁} [Bicategory.{w₁, v₁} A]
    {B : Type u₂} [Bicategory.{w₂, v₂} B]
    {C : Type*} [Bicategory C]
    (H : StrictlyUnitaryLaxFunctor A₀ A)
    (F : StrictlyUnitaryLaxFunctor A B)
    (G : StrictlyUnitaryLaxFunctor A C) :
    H.comp (normalLaxPair F G) =
      normalLaxPair (H.comp F) (H.comp G) := by
  ext
  · rfl
  all_goals
    · rw [heq_iff_eq]
      ext <;> simp [normalLaxPair]

/-! ## The interval as a normal lax functor -/

/-- A simplex of `Δ[1]` is exactly a normal lax functor `[n] -> [1]`. -/
def intervalNormalLax
    {J : SimplexCategoryᵒᵖ}
    (t : Δ[1].obj J) :
    StrictlyUnitaryLaxFunctor
      (DuskinOrdinal J.unop.len) (DuskinOrdinal 1) :=
  locallyDiscreteNormalLax
    (SimplexCategory.toCat.map (SSet.stdSimplex.objEquiv t)).toFunctor

/-- Interval simplices reindex by precomposition, exactly as Duskin simplices do. -/
theorem intervalNormalLax_reindex
    {J J' : SimplexCategoryᵒᵖ}
    (f : J ⟶ J')
    (t : Δ[1].obj J) :
    intervalNormalLax (Δ[1].map f t) =
      (duskinReindex f).comp (intervalNormalLax t) := by
  have ht :
      SSet.stdSimplex.objEquiv (Δ[1].map f t) =
        f.unop ≫ SSet.stdSimplex.objEquiv t := by
    rfl
  rw [intervalNormalLax, intervalNormalLax, ht]
  simpa [duskinReindex, Functor.comp_def] using
    locallyDiscreteNormalLax_comp
      (SimplexCategory.toCat.map f.unop).toFunctor
      (SimplexCategory.toCat.map (SSet.stdSimplex.objEquiv t)).toFunctor

/-! ## Duskin maps induced by arbitrary normal lax functors -/

/-- Any same-universe normal lax functor induces a simplicial map of global Duskin nerves. -/
def normalLaxDuskinNerveMap
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (P : StrictlyUnitaryLaxFunctor B C) :
    duskinNerve B ⟶ duskinNerve C where
  app J := TypeCat.ofHom fun σ => σ.comp P
  naturality := by
    intro J J' f
    ext σ
    exact StrictlyUnitaryLaxFunctor.comp_assoc (duskinReindex f) σ P

@[simp] theorem normalLaxDuskinNerveMap_app
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (P : StrictlyUnitaryLaxFunctor B C)
    (J : SimplexCategoryᵒᵖ)
    (σ : (duskinNerve B).obj J) :
    (normalLaxDuskinNerveMap P).app J σ = σ.comp P := rfl

@[simp] theorem normalLaxDuskinNerveMap_id
    (B : Type u) [Bicategory.{w, v} B] :
    normalLaxDuskinNerveMap (StrictlyUnitaryLaxFunctor.id B) =
      𝟙 (duskinNerve B) := by
  ext J σ
  exact StrictlyUnitaryLaxFunctor.comp_id σ

/-- Duskin nerve transport converts normal-lax composition into simplicial composition. -/
theorem normalLaxDuskinNerveMap_comp
    {B C D : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C] [Bicategory.{w, v} D]
    (P : StrictlyUnitaryLaxFunctor B C)
    (Q : StrictlyUnitaryLaxFunctor C D) :
    normalLaxDuskinNerveMap (P.comp Q) =
      normalLaxDuskinNerveMap P ≫ normalLaxDuskinNerveMap Q := by
  ext J σ
  exact StrictlyUnitaryLaxFunctor.comp_assoc σ P Q

/-! ## Degreewise prism data -/

/-- Degreewise mixed Duskin simplices with reindexing and endpoint laws. -/
structure DuskinPrismFamily
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (P Q : StrictlyUnitaryLaxFunctor B C) where
  mixed :
    ∀ {J : SimplexCategoryᵒᵖ},
      (duskinNerve B).obj J → Δ[1].obj J → (duskinNerve C).obj J
  reindex :
    ∀ {J J' : SimplexCategoryᵒᵖ}
      (f : J ⟶ J') (σ : (duskinNerve B).obj J) (t : Δ[1].obj J),
      mixed ((duskinNerve B).map f σ) (Δ[1].map f t) =
        (duskinNerve C).map f (mixed σ t)
  endpoint_zero :
    ∀ (J : SimplexCategoryᵒᵖ) (σ : (duskinNerve B).obj J),
      mixed σ ((SSet.ι₀.app J σ).2) =
        (normalLaxDuskinNerveMap P).app J σ
  endpoint_one :
    ∀ (J : SimplexCategoryᵒᵖ) (σ : (duskinNerve B).obj J),
      mixed σ ((SSet.ι₁.app J σ).2) =
        (normalLaxDuskinNerveMap Q).app J σ

namespace DuskinPrismFamily

/-- Degreewise prism data assemble to one native simplicial homotopy. -/
noncomputable def toHomotopy
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {P Q : StrictlyUnitaryLaxFunctor B C}
    (H : DuskinPrismFamily P Q) :
    SSet.Homotopy
      (normalLaxDuskinNerveMap P)
      (normalLaxDuskinNerveMap Q) where
  h :=
    { app := fun J => TypeCat.ofHom fun x => H.mixed x.1 x.2
      naturality := by
        intro J J' f
        ext x
        exact H.reindex f x.1 x.2 }
  h₀ := by
    ext J σ
    exact H.endpoint_zero J σ
  h₁ := by
    ext J σ
    exact H.endpoint_one J σ
  rel := by
    cat_disch

end DuskinPrismFamily

/-! ## Evaluation of one normal-lax cylinder -/

/-- A certified normal-lax cylinder from `P` to `Q`. -/
structure NormalLaxDuskinCylinder
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (P Q : StrictlyUnitaryLaxFunctor B C) where
  cylinder : StrictlyUnitaryLaxFunctor (B × DuskinOrdinal 1) C
  endpoint_zero :
    ∀ {J : SimplexCategoryᵒᵖ} (σ : (duskinNerve B).obj J),
      (normalLaxPair σ (intervalNormalLax ((SSet.ι₀.app J σ).2))).comp cylinder =
        σ.comp P
  endpoint_one :
    ∀ {J : SimplexCategoryᵒᵖ} (σ : (duskinNerve B).obj J),
      (normalLaxPair σ (intervalNormalLax ((SSet.ι₁.app J σ).2))).comp cylinder =
        σ.comp Q

namespace NormalLaxDuskinCylinder

/-- Evaluate the cylinder on a Duskin simplex and an interval simplex. -/
def mixed
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {P Q : StrictlyUnitaryLaxFunctor B C}
    (H : NormalLaxDuskinCylinder P Q)
    {J : SimplexCategoryᵒᵖ}
    (σ : (duskinNerve B).obj J)
    (t : Δ[1].obj J) :
    (duskinNerve C).obj J :=
  (normalLaxPair σ (intervalNormalLax t)).comp H.cylinder

/-- A normal-lax cylinder supplies all prism reindexing laws automatically. -/
def toPrismFamily
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {P Q : StrictlyUnitaryLaxFunctor B C}
    (H : NormalLaxDuskinCylinder P Q) :
    DuskinPrismFamily P Q where
  mixed := H.mixed
  reindex := by
    intro J J' f σ t
    change
      (normalLaxPair ((duskinReindex f).comp σ)
          (intervalNormalLax (Δ[1].map f t))).comp H.cylinder =
        (duskinReindex f).comp
          ((normalLaxPair σ (intervalNormalLax t)).comp H.cylinder)
    rw [intervalNormalLax_reindex]
    rw [← normalLaxPair_precomp]
    exact StrictlyUnitaryLaxFunctor.comp_assoc
      (duskinReindex f) (normalLaxPair σ (intervalNormalLax t)) H.cylinder
  endpoint_zero := by
    intro J σ
    exact H.endpoint_zero σ
  endpoint_one := by
    intro J σ
    exact H.endpoint_one σ

/-- Hence every certified normal-lax cylinder induces a native `SSet.Homotopy`. -/
noncomputable def toHomotopy
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {P Q : StrictlyUnitaryLaxFunctor B C}
    (H : NormalLaxDuskinCylinder P Q) :
    SSet.Homotopy
      (normalLaxDuskinNerveMap P)
      (normalLaxDuskinNerveMap Q) :=
  H.toPrismFamily.toHomotopy

end NormalLaxDuskinCylinder

/-! ## Native strong transformations and the remaining uncurrying boundary -/

/-- Promote the source native oplax-strong counit of v1.32 to Mathlib's pseudofunctor strong form. -/
def sourcePseudoStrong
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    Pseudofunctor.StrongTrans
      (F.forward.toPseudofunctor.comp G.forward.toPseudofunctor)
      (Pseudofunctor.id B) :=
  Pseudofunctor.StrongTrans.mkOfOplax K.sourceCounit

/-- Target-side native pseudofunctor strong transformation. -/
def targetPseudoStrong
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    Pseudofunctor.StrongTrans
      (G.forward.toPseudofunctor.comp F.forward.toPseudofunctor)
      (Pseudofunctor.id C) :=
  Pseudofunctor.StrongTrans.mkOfOplax K.targetCounit

/-- The normalized source round-trip as an actual normal lax functor. -/
def sourceRoundTripNormalLax
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B) :
    StrictlyUnitaryLaxFunctor B B :=
  F.forward.toStrictlyUnitaryLaxFunctor.comp
    G.forward.toStrictlyUnitaryLaxFunctor

/-- The normalized target round-trip as an actual normal lax functor. -/
def targetRoundTripNormalLax
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B) :
    StrictlyUnitaryLaxFunctor C C :=
  G.forward.toStrictlyUnitaryLaxFunctor.comp
    F.forward.toStrictlyUnitaryLaxFunctor

/--
The exact remaining bicategorical construction: uncurry the two native strong
transformations into normal-lax cylinders.  No simplicial or horn data occur in
this interface.
-/
structure StrongQuasiInverseNormalLaxCylinder
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) : Prop where
  sourceCylinder :
    NormalLaxDuskinCylinder
      (sourceRoundTripNormalLax F G)
      (StrictlyUnitaryLaxFunctor.id B)
  targetCylinder :
    NormalLaxDuskinCylinder
      (targetRoundTripNormalLax F G)
      (StrictlyUnitaryLaxFunctor.id C)
  source_realizes_component :
    ∀ X : B,
      K.sourceCounit.app X = (sourcePseudoStrong K).app X
  target_realizes_component :
    ∀ X : C,
      K.targetCounit.app X = (targetPseudoStrong K).app X

namespace StrongQuasiInverseNormalLaxCylinder

/-- The source cylinder produces the global source Duskin prism. -/
noncomputable def sourcePrism
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {K : NormalizedCoherentQuasiInverse F G}
    (H : StrongQuasiInverseNormalLaxCylinder K) :
    SSet.Homotopy
      (normalLaxDuskinNerveMap (sourceRoundTripNormalLax F G))
      (𝟙 (duskinNerve B)) := by
  simpa using H.sourceCylinder.toHomotopy

/-- The target cylinder produces the global target Duskin prism. -/
noncomputable def targetPrism
    {B C : Type u} [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {K : NormalizedCoherentQuasiInverse F G}
    (H : StrongQuasiInverseNormalLaxCylinder K) :
    SSet.Homotopy
      (normalLaxDuskinNerveMap (targetRoundTripNormalLax F G))
      (𝟙 (duskinNerve C)) := by
  simpa using H.targetCylinder.toHomotopy

end StrongQuasiInverseNormalLaxCylinder

/-!
The v1.35 boundary is therefore:

```text
native Oplax.StrongTrans GF ==> id_B, FG ==> id_C
  -> native Pseudofunctor.StrongTrans
  -> normal-lax cylinder B × [1] -> B, C × [1] -> C
  -> one Duskin prism in each direction
  -> all hornwise homotopies
```

The standard uncurrying of a native strong transformation into its normal-lax
cylinder remains the exact lower bicategorical frontier; no arbitrary
bicategory is promoted to a fibrant scaled simplicial set here.
-/

end KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35
