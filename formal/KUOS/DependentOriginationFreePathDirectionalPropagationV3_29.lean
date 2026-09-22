import KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28

namespace KUOS.DependentOriginationFreePathDirectionalPropagationV3_29

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57

universe u v uH vH

set_option autoImplicit false

/-!
# Free-path directional propagation v3.29

v3.28 shows that the mixed associator/unitor residual vanishes when the left
outer representative is essentially surjective and the right outer
representative is faithful.  The next question is whether these two directional
properties can be read from the generated localization word itself.

The free localization source is the path category on
`Localization.Construction.LocQuiver W`.  Every path is generated from

* the identity path, and
* right-composition by a single quiver edge.

The v2.57 evaluator is exactly `Quiv.lift`, so one-edge paths evaluate to the
corresponding generator functor and path composition evaluates to functor
composition.

This file packages the two directional properties at generator level and proves
that each propagates through arbitrary finite free paths.  No quotient relation
or path-independence theorem is used.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The evaluation of one localization-quiver generator is essentially
surjective. -/
def GeneratorEvaluatesEssSurj
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y) : Prop :=
  ((localizedGeneratorPrefunctor W R D).map e).toFunctor.EssSurj

/-- The evaluation of one localization-quiver generator is faithful. -/
def GeneratorEvaluatesFaithful
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y) : Prop :=
  ((localizedGeneratorPrefunctor W R D).map e).toFunctor.Faithful

/-- Generic one-edge evaluation formula for the v2.57 free-path evaluator. -/
@[simp]
theorem freePathEvaluator_map_generator
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y) :
    (freePathEvaluator W R D).map ((Paths.of _).map e) =
      (localizedGeneratorPrefunctor W R D).map e := by
  change
    𝟙 _ ≫ (localizedGeneratorPrefunctor W R D).map e =
      (localizedGeneratorPrefunctor W R D).map e
  simp

/-- If every generator evaluation is essentially surjective, then every finite
free localization path evaluates to an essentially-surjective functor. -/
theorem freePathEvaluator_map_essSurj_of_generators
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hgen :
      ∀ {X Y : Localization.Construction.LocQuiver W} (e : X ⟶ Y),
        GeneratorEvaluatesEssSurj W R D e)
    {X Y : Paths (Localization.Construction.LocQuiver W)}
    (p : X ⟶ Y) :
    ((freePathEvaluator W R D).map p).toFunctor.EssSurj := by
  refine Paths.induction
    (P := fun {A B} q =>
      ((freePathEvaluator W R D).map q).toFunctor.EssSurj)
    ?_ ?_ p
  · intro V
    rw [(freePathEvaluator W R D).map_id]
    change (𝟭 _ : _ ⥤ _).EssSurj
    infer_instance
  · intro U V T q e hq
    rw [(freePathEvaluator W R D).map_comp]
    rw [freePathEvaluator_map_generator W R D e]
    letI :
        ((freePathEvaluator W R D).map q).toFunctor.EssSurj := hq
    letI :
        ((localizedGeneratorPrefunctor W R D).map e).toFunctor.EssSurj :=
      hgen e
    change
      (((freePathEvaluator W R D).map q).toFunctor ⋙
        ((localizedGeneratorPrefunctor W R D).map e).toFunctor).EssSurj
    infer_instance

/-- If every generator evaluation is faithful, then every finite free
localization path evaluates to a faithful functor. -/
theorem freePathEvaluator_map_faithful_of_generators
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hgen :
      ∀ {X Y : Localization.Construction.LocQuiver W} (e : X ⟶ Y),
        GeneratorEvaluatesFaithful W R D e)
    {X Y : Paths (Localization.Construction.LocQuiver W)}
    (p : X ⟶ Y) :
    ((freePathEvaluator W R D).map p).toFunctor.Faithful := by
  refine Paths.induction
    (P := fun {A B} q =>
      ((freePathEvaluator W R D).map q).toFunctor.Faithful)
    ?_ ?_ p
  · intro V
    rw [(freePathEvaluator W R D).map_id]
    change (𝟭 _ : _ ⥤ _).Faithful
    infer_instance
  · intro U V T q e hq
    rw [(freePathEvaluator W R D).map_comp]
    rw [freePathEvaluator_map_generator W R D e]
    letI :
        ((freePathEvaluator W R D).map q).toFunctor.Faithful := hq
    letI :
        ((localizedGeneratorPrefunctor W R D).map e).toFunctor.Faithful :=
      hgen e
    change
      (((freePathEvaluator W R D).map q).toFunctor ⋙
        ((localizedGeneratorPrefunctor W R D).map e).toFunctor).Faithful
    infer_instance

/-- Every formal inverse generator evaluates to an equivalence, hence in
particular is essentially surjective. -/
theorem formalInverse_generatorEvaluatesEssSurj
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    GeneratorEvaluatesEssSurj W R D
      (Sum.inr ⟨w, hw⟩) := by
  change
    (PointwiseWAdjointEquivalenceData.inverse W D w hw).toFunctor.EssSurj
  change (D.chosen w hw).inverse.EssSurj
  infer_instance

/-- Every formal inverse generator also evaluates to a faithful functor. -/
theorem formalInverse_generatorEvaluatesFaithful
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (w : X ⟶ Y) (hw : W w) :
    GeneratorEvaluatesFaithful W R D
      (Sum.inr ⟨w, hw⟩) := by
  change
    (PointwiseWAdjointEquivalenceData.inverse W D w hw).toFunctor.Faithful
  change (D.chosen w hw).inverse.Faithful
  infer_instance

/-- On an ordinary generator, the generator-level essentially-surjective
condition is exactly the same condition on the original raw pseudofunctor map. -/
theorem ordinary_generatorEvaluatesEssSurj_iff
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) :
    GeneratorEvaluatesEssSurj W R D
        (Sum.inl f) ↔
      (R.map f.toLoc).toFunctor.EssSurj := by
  rfl

/-- On an ordinary generator, the generator-level faithful condition is exactly
the same condition on the original raw pseudofunctor map. -/
theorem ordinary_generatorEvaluatesFaithful_iff
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) :
    GeneratorEvaluatesFaithful W R D
        (Sum.inl f) ↔
      (R.map f.toLoc).toFunctor.Faithful := by
  rfl

/-!
## Frontier after v3.29

The v3.28 directional hypotheses now have a free-path calculus.

* identity paths have both properties;
* formal W-inverse generators have both because they evaluate to inverse
  functors of chosen equivalences;
* ordinary generators carry exactly the corresponding property of the raw
  pseudofunctor map;
* composition propagates each property through arbitrary finite words.

Thus the remaining issue is no longer finite-word propagation.  It is to relate
these path-level properties to the chosen quotient representative
`Quot.out f` used by `quotientRepresentativeMap`.

The next theorem unit should specialize the two propagation theorems to
`Quot.out f` and formulate explicit sufficient conditions on the ordinary
generators occurring in that representative word.  That will connect the
v3.29 free-path calculus back to the v3.28 mixed-triangle closure criterion
without asserting that arbitrary raw arrows are essentially surjective or
faithful.
-/

end KUOS.DependentOriginationFreePathDirectionalPropagationV3_29
