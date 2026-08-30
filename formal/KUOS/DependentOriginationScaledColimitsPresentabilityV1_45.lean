import KUOS.DependentOriginationScaledSmallObjectArgumentV1_44
import Mathlib.AlgebraicTopology.SimplicialSet.Presentable
import Mathlib.CategoryTheory.Limits.Preserves.Filtered

namespace KUOS.DependentOriginationScaledColimitsPresentabilityV1_45

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open CategoryTheory.SmallObject
open HomotopicalAlgebra
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledTerminalRLPV1_41.ScaledSSet
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationScaledSmallObjectArgumentV1_44

universe u

/-!
# Scaled colimits, presentability, and the small-object argument v1.45

Version 1.44 reduced the final small-object input to categorical/presentability
properties of `ScaledSSet`.  This file constructs those properties directly.

The key observation is that the KuuOS scaling structure is deliberately light:
it is only a predicate on 2-simplices containing the two degenerate families.
Therefore a colimit of scaled simplicial sets is obtained by taking the
underlying simplicial-set colimit and equipping it with the least scaling that
contains

* all degenerate 2-simplices; and
* every image of a thin 2-simplex from a diagram object.

This construction makes the forgetful functor `ScaledSSet ⥤ SSet` preserve
colimits.  On the other hand, every canonical horn-cylinder generator has
*minimal* scaling.  Hence maps from its source are exactly underlying
simplicial maps.  Since the underlying horn-cylinder attachment is a
subcomplex of the finite simplicial set `Δ[n] × Δ[1]`, it is finite and hence
finitely presentable in Mathlib.

These facts instantiate Mathlib's small-object argument at `Cardinal.aleph0`.
Thus the canonical generated pair `(T.rlp.llp, T.rlp)` is a native weak
factorization system without any remaining KuuOS factorization certificate.
-/

namespace ScaledSSet

/-! ## Forgetful and minimally-scaled functors -/

/-- Forget the scaling. -/
def forget : ScaledSSet.{u} ⥤ SSet.{u} where
  obj X := X.carrier
  map f := f.map
  map_id := by intro X; rfl
  map_comp := by intro X Y Z f g; rfl

/-- Equip a simplicial set with the minimal scaling. -/
def minimallyScale : SSet.{u} ⥤ ScaledSSet.{u} where
  obj X := ScaledSSet.of X (minimalScaling X)
  map f :=
    { map := f
      scaled := minimalScaling_map _ f }
  map_id := by
    intro X
    apply ScaledMap.ext
    rfl
  map_comp := by
    intro X Y Z f g
    apply ScaledMap.ext
    rfl

/-- Maps out of a minimally-scaled simplicial set are exactly underlying
simplicial maps. -/
def minimalHomEquiv (A : SSet.{u}) (X : ScaledSSet.{u}) :
    (minimallyScale.obj A ⟶ X) ≃ (A ⟶ X.carrier) where
  toFun f := f.map
  invFun f :=
    { map := f
      scaled := minimalScaling_map X.scaling f }
  left_inv f := by
    apply ScaledMap.ext
    rfl
  right_inv f := rfl

/-- The previous equivalence is natural in the scaled target. -/
def minimalCoyonedaIso (A : SSet.{u}) :
    coyoneda.obj (op (minimallyScale.obj A)) ≅
      forget ⋙ coyoneda.obj (op A) :=
  NatIso.ofComponents
    (fun X =>
      { hom := TypeCat.ofHom (fun f => f.map)
        inv := TypeCat.ofHom (fun f =>
          ({ map := f
             scaled := minimalScaling_map X.scaling f } : minimallyScale.obj A ⟶ X))
        hom_inv_id := by
          ext f
          rfl
        inv_hom_id := by
          ext f
          rfl })
    (by
      intro X Y f
      ext g
      rfl)

/-! ## Explicit colimits -/

section Colimits

variable {J : Type u} [Category.{u} J]

/-- The least scaling on the underlying colimit containing every thin
2-simplex coming from every object of the diagram. -/
@[reducible]
noncomputable def colimitScaling
    (D : J ⥤ ScaledSSet.{u})
    [HasColimit (D ⋙ forget)] :
    ScaledSimplicialSet (colimit (D ⋙ forget)) where
  thin := fun t =>
    (∃ x : (colimit (D ⋙ forget)) _⦋1⦌,
      (colimit (D ⋙ forget)).σ 0 x = t) ∨
    (∃ x : (colimit (D ⋙ forget)) _⦋1⦌,
      (colimit (D ⋙ forget)).σ 1 x = t) ∨
    ∃ (j : J) (x : (D.obj j).carrier _⦋2⦌),
      (D.obj j).scaling.thin x ∧
        ((colimit.ι (D ⋙ forget) j).app _ x = t)
  thin_sigma_zero := by
    intro x
    exact Or.inl ⟨x, rfl⟩
  thin_sigma_one := by
    intro x
    exact Or.inr (Or.inl ⟨x, rfl⟩)

/-- The scaled object carried by the underlying simplicial-set colimit. -/
noncomputable def colimitObj
    (D : J ⥤ ScaledSSet.{u})
    [HasColimit (D ⋙ forget)] : ScaledSSet.{u} :=
  ScaledSSet.of (colimit (D ⋙ forget)) (colimitScaling D)

/-- The canonical colimit leg is scaled by construction. -/
noncomputable def colimitLeg
    (D : J ⥤ ScaledSSet.{u})
    [HasColimit (D ⋙ forget)]
    (j : J) : D.obj j ⟶ colimitObj D where
  map := colimit.ι (D ⋙ forget) j
  scaled := by
    intro t ht
    exact Or.inr (Or.inr ⟨j, t, ht, rfl⟩)

/-- The explicit scaled colimit cocone. -/
noncomputable def colimitCocone
    (D : J ⥤ ScaledSSet.{u})
    [HasColimit (D ⋙ forget)] : Cocone D where
  pt := colimitObj D
  ι :=
    { app := colimitLeg D
      naturality := by
        intro j j' f
        apply ScaledMap.ext
        exact colimit.w (D ⋙ forget) f }

/-- The explicit scaled cocone is universal. -/
noncomputable def colimitCoconeIsColimit
    (D : J ⥤ ScaledSSet.{u})
    [HasColimit (D ⋙ forget)] : IsColimit (colimitCocone D) where
  desc s :=
    { map := colimit.desc (forget.mapCocone s)
      scaled := by
        intro t ht
        rcases ht with ⟨x, rfl⟩ | ⟨x, rfl⟩ | ⟨j, x, hx, rfl⟩
        · rw [SSet.σ_naturality_apply _ 0 x]
          exact s.pt.scaling.thin_sigma_zero _
        · rw [SSet.σ_naturality_apply _ 1 x]
          exact s.pt.scaling.thin_sigma_one _
        · have h := (s.ι.app j).scaled hx
          simpa [forget, colimitCocone, colimitLeg, colimitObj] using h }
  fac s j := by
    apply ScaledMap.ext
    simp [colimitCocone, colimitLeg, colimitObj, forget]
  uniq s m hm := by
    apply ScaledMap.ext
    apply colimit.hom_ext
    intro j
    have h := congrArg ScaledMap.map (hm j)
    simpa [colimitCocone, colimitLeg, colimitObj, forget] using h

/-- The underlying cocone of the explicit scaled colimit is the ordinary
simplicial-set colimit cocone. -/
noncomputable def forgetColimitCoconeIsColimit
    (D : J ⥤ ScaledSSet.{u})
    [HasColimit (D ⋙ forget)] :
    IsColimit (forget.mapCocone (colimitCocone D)) := by
  simpa [forget, colimitCocone, colimitLeg, colimitObj] using
    (colimit.isColimit (D ⋙ forget))

/-- Every colimit shape available in simplicial sets is available in scaled
simplicial sets. -/
noncomputable instance hasColimitsOfShape
    [HasColimitsOfShape J SSet.{u}] : HasColimitsOfShape J ScaledSSet.{u} where
  has_colimit D :=
    HasColimit.mk ⟨colimitCocone D, colimitCoconeIsColimit D⟩

/-- The forgetful functor preserves all such colimits. -/
noncomputable instance forget_preservesColimitsOfShape
    [HasColimitsOfShape J SSet.{u}] :
    PreservesColimitsOfShape J (forget : ScaledSSet.{u} ⥤ SSet.{u}) where
  preservesColimit {D} :=
    preservesColimit_of_preserves_colimit_cocone
      (colimitCoconeIsColimit D)
      (forgetColimitCoconeIsColimit D)

end Colimits

/-- Scaled simplicial sets have all small colimits because simplicial sets do. -/
noncomputable instance hasColimits : HasColimits (ScaledSSet.{u}) where
  has_colimits_of_shape J := by infer_instance

/-- Forgetting the scaling preserves all small colimits. -/
noncomputable instance forget_preservesColimits :
    PreservesColimits (forget : ScaledSSet.{u} ⥤ SSet.{u}) where
  preservesColimitsOfShape := by infer_instance

/-- The scaled category is locally small in the same universe. -/
instance locallySmall : LocallySmall.{u} (ScaledSSet.{u}) := by
  infer_instance

/-! ## Finite presentability of minimally-scaled finite simplicial sets -/

/-- Minimal scaling preserves finite presentability.  The proof uses the
natural identification of scaled Hom with underlying simplicial Hom together
with colimit preservation of the forgetful functor. -/
instance minimallyScaled_isFinitelyPresentable
    (A : SSet.{u}) [A.Finite] :
    IsFinitelyPresentable.{u} (minimallyScale.obj A) := by
  rw [isFinitelyPresentable_iff_preservesFilteredColimitsOfSize]
  refine
    { preserves_filtered_colimits := ?_ }
  intro J _ _
  haveI : IsFinitelyPresentable.{u} A := by infer_instance
  haveI : PreservesColimitsOfShape J (forget : ScaledSSet.{u} ⥤ SSet.{u}) := by
    infer_instance
  haveI : PreservesColimitsOfShape J (coyoneda.obj (op A)) := by
    infer_instance
  haveI : PreservesColimitsOfShape J
      (forget ⋙ coyoneda.obj (op A)) := by
    infer_instance
  exact preservesColimitsOfShape_of_natIso (minimalCoyonedaIso A).symm

end ScaledSSet

/-! ## Canonical generator sources are finitely presentable -/

/-- Every underlying horn-cylinder attachment is finite: it is a subcomplex of
`Δ[n] × Δ[1]`. -/
instance hornCylinderAttachment_finite
    (n : Nat) (i : Fin (n + 1)) (ε : Fin 2) :
    SSet.Finite (hornCylinderAttachment n i ε : SSet.{u}) := by
  infer_instance

/-- Therefore every source of a canonical scaled horn-cylinder generator is
finitely presentable in `ScaledSSet`. -/
instance minimallyScaledHornCylinderAttachment_isFinitelyPresentable
    (n : Nat) (i : Fin (n + 1)) (ε : Fin 2) :
    IsFinitelyPresentable.{u}
      (minimallyScaledHornCylinderAttachment n i ε : ScaledSSet.{u}) := by
  change IsFinitelyPresentable.{u}
    (ScaledSSet.minimallyScale.obj
      (hornCylinderAttachment n i ε : SSet.{u}))
  infer_instance

/-! ## The canonical small-object argument at aleph-zero -/

attribute [local instance] Cardinal.fact_isRegular_aleph0
  Cardinal.orderBotAleph0OrdToType

/-- The exact cardinal condition required by Mathlib holds at `aleph0` for the
canonical scaled horn-cylinder generators. -/
noncomputable instance canonicalScaled_isCardinalForSmallObjectArgument :
    MorphismProperty.IsCardinalForSmallObjectArgument.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u}))
      Cardinal.aleph0.{u} where
  preservesColimit {A B X Y} i hi f hf := by
    have hA : IsFinitelyPresentable.{u} A := by
      dsimp [scaledHornAttachmentGenerators] at hi
      cases hi with
      | mk g =>
          dsimp [scaledHornAttachmentGeneratorHom]
          infer_instance
    letI : IsFinitelyPresentable.{u} A := hA
    infer_instance

/-- Hence the canonical generators permit Mathlib's small-object argument with
no additional KuuOS certificate. -/
noncomputable instance canonicalScaled_hasSmallObjectArgument :
    MorphismProperty.HasSmallObjectArgument.{u}
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) :=
  ⟨Cardinal.aleph0, inferInstance, inferInstance, inferInstance⟩

/-- The v1.43 generated pair is therefore an unconditional native weak
factorization system. -/
noncomputable def canonicalGeneratedScaledWeakFactorizationSystem_unconditional :
    MorphismProperty.IsWeakFactorizationSystem
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (canonicalGeneratedScaledFibration : MorphismProperty (ScaledSSet.{u})) :=
  KUOS.DependentOriginationScaledSmallObjectArgumentV1_44.
    canonicalGeneratedScaledWeakFactorizationSystem_of_smallObject inferInstance

/-- The canonical generated left class has the expected cellular description
without any extra hypothesis. -/
theorem canonicalGeneratedScaledAnodyne_eq_cellularClosure_unconditional :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) =
      (MorphismProperty.transfiniteCompositions.{u}
        (MorphismProperty.coproducts.{u}
          (scaledHornAttachmentGenerators : MorphismProperty
            (ScaledSSet.{u}))).pushouts).retracts :=
  KUOS.DependentOriginationScaledSmallObjectArgumentV1_44.
    canonicalGeneratedScaledAnodyne_eq_cellularClosure inferInstance

/-!
The complete lifting-theoretic spine is now theorem-level:

```text
canonical horn-cylinder attachments T
  -> explicit scaled colimits
  -> forget : ScaledSSet -> SSet preserves colimits
  -> finite underlying attachment sources
  -> minimal-scaled sources are finitely presentable
  -> IsCardinalForSmallObjectArgument T aleph0
  -> HasSmallObjectArgument T
  -> HasFunctorialFactorization (T.rlp.llp) (T.rlp)
  -> IsWeakFactorizationSystem (T.rlp.llp) (T.rlp)
  -> T.rlp.llp = retracts(transfinite compositions(pushouts(coproducts(T)))).
```

No factorization, strictification, horn-family RLP, or presentability
certificate remains as an independent field in this route.
-/

end KUOS.DependentOriginationScaledColimitsPresentabilityV1_45