import Mathlib.Tactic.Group
import KUOS.DependentOriginationGeneratedHolonomyCountermodelLoopV2_69

namespace KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68
open KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68

/-!
# Evaluation of the octahedral generated loop v2.69

The direct route evaluates to the unique nontrivial scalar `zeta`.  The route
around the other seven faces evaluates to the identity.  The only apparently
choice-dependent terms in the long route are the two inserted formal-inverse
pairs.  We do not inspect the implementation of the chosen pointwise inverse.
Instead, naturality of the counit of an arbitrary chosen equivalence shows that
its inverse functor acts trivially on the morphisms of the one-object `C2`
groupoid.  Consequently left and right whiskering preserve scalar components,
and the two inverse-pair contributions cancel as a commutator in the abelian
group `C2`.

This produces an explicit nontrivial generated relation-loop holonomy for the
canonical pointwise data selected from weak admissibility.  The conclusion is
narrow: weak admissibility does not force `GeneratedHolonomyTrivial`.
-/

/-- The scalar component of the evaluation of a generated localization 2-cell
at the unique object of the countermodel fiber. -/
noncomputable def counterEvaluationScalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell allMorphisms p q) : C2 :=
  (generatedLocalization2CellEvaluationIso
      allMorphisms counterSystem D α).hom.toNatTrans.app
    (SingleObj.star C2)

/-- The forward functor in each chosen equivalence still acts literally as
the identity on the one-object countermodel. -/
theorem chosenForward_map_eq
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (w : X ⟶ Y) (hw : allMorphisms w)
    {A B : CounterFiber} (x : A ⟶ B) :
    (D.chosen w hw).functor.map x = x := by
  rw [D.chosen_functor w hw, counterSystem_map_toFunctor]
  rfl

/-- Any inverse functor selected by pointwise admissibility acts identically on
`C2` morphisms.  This uses only counit naturality and commutativity of `C2`, not
the implementation of `Functor.asEquivalence`. -/
theorem chosenInverse_map_eq
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (w : X ⟶ Y) (hw : allMorphisms w)
    (x : SingleObj.star C2 ⟶ SingleObj.star C2) :
    (PointwiseWAdjointEquivalenceData.inverse
      allMorphisms D w hw).toFunctor.map x = x := by
  let y : SingleObj.star C2 ⟶ SingleObj.star C2 :=
    (D.chosen w hw).inverse.map x
  let c : SingleObj.star C2 ⟶ SingleObj.star C2 :=
    (D.chosen w hw).counitIso.hom.app (SingleObj.star C2)
  change y = x
  have hnat := (D.chosen w hw).counitIso.hom.naturality x
  simp only [Functor.comp_map, Functor.id_map] at hnat
  rw [chosenForward_map_eq D w hw ((D.chosen w hw).inverse.map x)] at hnat
  change y ≫ c = c ≫ x at hnat
  have hmul : (c : C2) * (y : C2) = (x : C2) * (c : C2) := by
    simpa only [SingleObj.comp_as_mul] using hnat
  rw [mul_comm (x : C2) (c : C2)] at hmul
  exact mul_left_cancel hmul

/-- Every free localization word acts identically on `C2` morphisms. -/
theorem counterFreePathEvaluator_map_eq
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} (p : X ⟶ Y)
    (x : SingleObj.star C2 ⟶ SingleObj.star C2) :
    ((freePathEvaluator allMorphisms counterSystem D).map p).toFunctor.map x = x := by
  induction p using Paths.induction with
  | id =>
      rw [(freePathEvaluator allMorphisms counterSystem D).map_id]
      change (𝟭 CounterFiber).map x = x
      rfl
  | comp p e hp =>
      rw [Functor.map_comp, Cat.Hom.comp_toFunctor, Functor.comp_map, hp]
      have hgen :
          (freePathEvaluator allMorphisms counterSystem D).map
              ((Paths.of (Localization.Construction.LocQuiver allMorphisms)).map e) =
            (localizedGeneratorPrefunctor allMorphisms counterSystem D).map e := by
        simp [freePathEvaluator]
      rw [hgen]
      rcases e with f | w
      · change (counterSystem.map f.toLoc).toFunctor.map x = x
        rw [counterSystem_map_toFunctor]
        rfl
      · exact chosenInverse_map_eq D w.1 w.2 x

/-- On the countermodel, every free-path object evaluates to the same
one-object target category. -/
@[simp] private theorem counterFreePathEvaluator_obj
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    (X : LocalizationPaths allMorphisms) :
    (freePathEvaluator allMorphisms counterSystem D).obj X =
      Cat.of CounterFiber := by
  rfl

/-- Equality transport between objects of the one-object target is the
unit scalar. -/
@[simp] private theorem singleObj_eqToHom_eq_one
    {A B : CounterFiber} (h : A = B) :
    (eqToHom h : A ⟶ B) = (1 : C2) := by
  subst B
  exact SingleObj.id_as_one C2 A

private theorem eqToHom_comp_eq
    {A B C D : CounterFiber}
    (h₁ : A = B) (m : B ⟶ C) (h₂ : C = D) :
    eqToHom h₁ ≫ m ≫ eqToHom h₂ = m := by
  subst B
  subst D
  simp

@[simp]
theorem counterEvaluationScalar_refl
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} (p : X ⟶ Y) :
    counterEvaluationScalar D (GeneratedLocalization2Cell.refl p) = 1 := by
  rfl

@[simp] theorem counterEvaluationScalar_ofEq
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} {p q : X ⟶ Y}
    (h : p = q) :
    counterEvaluationScalar D
      (generatedLocalization2CellOfEq allMorphisms h) = 1 := by
  subst q
  rfl

@[simp]
theorem counterEvaluationScalar_trans
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} {p q r : X ⟶ Y}
    (α : GeneratedLocalization2Cell allMorphisms p q)
    (β : GeneratedLocalization2Cell allMorphisms q r) :
    counterEvaluationScalar D (GeneratedLocalization2Cell.trans α β) =
      counterEvaluationScalar D β * counterEvaluationScalar D α := by
  rfl

@[simp] theorem counterEvaluationScalar_reendpoint
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms}
    {p q p' q' : X ⟶ Y}
    (hp : p' = p) (hq : q = q')
    (α : GeneratedLocalization2Cell allMorphisms p q) :
    counterEvaluationScalar D (counterReendpointCell hp hq α) =
      counterEvaluationScalar D α := by
  unfold counterReendpointCell
  simp only [counterEvaluationScalar_trans, counterEvaluationScalar_ofEq,
    one_mul, mul_one]

@[simp]
theorem counterEvaluationScalar_symm
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell allMorphisms p q) :
    counterEvaluationScalar D (GeneratedLocalization2Cell.symm α) =
      (counterEvaluationScalar D α)⁻¹ := by
  apply eq_inv_of_mul_eq_one_right
  simpa only [counterEvaluationScalar, SingleObj.comp_as_mul,
    SingleObj.id_as_one] using
    (Cat.Hom.inv_hom_id_toNatTrans_app
      (generatedLocalization2CellEvaluationIso
        allMorphisms counterSystem D α)
      (SingleObj.star C2))

@[simp]
theorem counterEvaluationScalar_whiskerLeft
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y Z : LocalizationPaths allMorphisms}
    (k : X ⟶ Y) {p q : Y ⟶ Z}
    (α : GeneratedLocalization2Cell allMorphisms p q) :
    counterEvaluationScalar D
        (generatedLocalization2CellWhiskerLeft allMorphisms k α) =
      counterEvaluationScalar D α := by
  unfold counterEvaluationScalar
  rw [generatedLocalization2CellEvaluationIso_whiskerLeft_hom]
  simp only [Iso.trans_hom, Iso.symm_hom, eqToIso.hom, eqToIso.inv,
    Cat.Hom₂.comp_app, whiskerLeftIso_hom, Cat.whiskerLeft_app,
    Cat.eqToHom_app]
  have hY := counterFreePathEvaluator_obj D Y
  have hZ := counterFreePathEvaluator_obj D Z
  cases hY
  cases hZ
  calc
    _ = (generatedLocalization2CellEvaluationIso
          allMorphisms counterSystem D α).hom.toNatTrans.app
          (((freePathEvaluator allMorphisms counterSystem D).map k).toFunctor.obj
            (SingleObj.star C2)) := by
      exact eqToHom_comp_eq _ _ _
    _ = (generatedLocalization2CellEvaluationIso
          allMorphisms counterSystem D α).hom.toNatTrans.app
          (SingleObj.star C2) := by
      exact congrArg
        (fun T : CounterFiber =>
          (generatedLocalization2CellEvaluationIso
            allMorphisms counterSystem D α).hom.toNatTrans.app T)
        (Subsingleton.elim _ _)

@[simp]
theorem counterEvaluationScalar_whiskerRight
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y Z : LocalizationPaths allMorphisms}
    {p q : X ⟶ Y} (k : Y ⟶ Z)
    (α : GeneratedLocalization2Cell allMorphisms p q) :
    counterEvaluationScalar D
        (generatedLocalization2CellWhiskerRight allMorphisms k α) =
      counterEvaluationScalar D α := by
  unfold counterEvaluationScalar
  rw [generatedLocalization2CellEvaluationIso_whiskerRight_hom]
  simp only [Iso.trans_hom, Iso.symm_hom, eqToIso.hom, eqToIso.inv,
    Cat.Hom₂.comp_app, whiskerRightIso_hom, Cat.whiskerRight_app,
    Cat.eqToHom_app]
  have hX := counterFreePathEvaluator_obj D X
  have hY := counterFreePathEvaluator_obj D Y
  have hZ := counterFreePathEvaluator_obj D Z
  cases hX
  cases hY
  cases hZ
  calc
    _ = ((freePathEvaluator allMorphisms counterSystem D).map k).toFunctor.map
          ((generatedLocalization2CellEvaluationIso
            allMorphisms counterSystem D α).hom.toNatTrans.app
            (SingleObj.star C2)) := by
      exact eqToHom_comp_eq _ _ _
    _ = (generatedLocalization2CellEvaluationIso
          allMorphisms counterSystem D α).hom.toNatTrans.app
          (SingleObj.star C2) := by
      exact counterFreePathEvaluator_map_eq D k _

/-- Component of the concrete compositor at the unique target object. -/
@[simp] theorem counterMapComp_hom_app_star
    (X Y Z : OctahedralVertex) :
    (counterMapComp X Y Z).hom.toNatTrans.app (SingleObj.star C2) =
      compScalar X Y Z := by
  unfold counterMapComp scalarCompIso
  change
    (scalarIdNatIso (compScalar X Y Z)).hom.app (SingleObj.star C2) ≫
        (𝟭 CounterFiber).rightUnitor.inv.app (SingleObj.star C2) =
      compScalar X Y Z
  rw [scalarIdNatIso_hom_app_star]
  rw [Functor.rightUnitor_inv_app]
  exact Category.comp_id _

/-- A retained composition generator evaluates to the scalar decorating exactly
that triangular face. -/
@[simp]
theorem compositionCell_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    counterEvaluationScalar D (compositionCell f g) = compScalar X Y Z := by
  unfold counterEvaluationScalar compositionCell
  rw [generatedLocalization2CellEvaluationIso_ofGenerating_hom]
  change (counterMapComp X Y Z).hom.toNatTrans.app
    (SingleObj.star C2) = compScalar X Y Z
  exact counterMapComp_hom_app_star X Y Z

/-- A change of parallel-arrow presentation carries no scalar. -/
@[simp]
theorem parallelArrowCell_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f g : X ⟶ Y) :
    counterEvaluationScalar D (parallelArrowCell f g) = 1 := by
  unfold parallelArrowCell
  exact counterEvaluationScalar_ofEq D _

/-- The distinguished face carries the unique nontrivial scalar. -/
@[simp]
theorem counterDirectRoute_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D counterDirectRoute = zeta := by
  unfold counterDirectRoute
  rw [compositionCell_scalar, compScalar_L0_M0_H0]

@[simp] theorem routeStep00_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep00 = 1 := by
  unfold routeStep00
  exact parallelArrowCell_scalar D _ _

@[simp] theorem routeStep01_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep01 = 1 := by
  unfold routeStep01
  rw [compositionCell_scalar, compScalar_L0_M1_H0]

@[simp] theorem routeStep02_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep02 =
      (counterEvaluationScalar D (forwardInverseCell b11))⁻¹ := by
  unfold routeStep02
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft,
    counterEvaluationScalar_symm]

@[simp] theorem routeStep03_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep03 = 1 := by
  unfold routeStep03
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_symm,
    compositionCell_scalar, compScalar_L0_M1_H1, inv_one]

@[simp] theorem routeStep04_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep04 = 1 := by
  unfold routeStep04
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight]
  exact parallelArrowCell_scalar D _ _

@[simp] theorem routeStep05_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep05 = 1 := by
  unfold routeStep05
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    compositionCell_scalar, compScalar_L0_M0_H1]

@[simp] theorem routeStep06_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep06 =
      (counterEvaluationScalar D (inverseForwardCell a10))⁻¹ := by
  unfold routeStep06
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft,
    counterEvaluationScalar_symm]

@[simp] theorem routeStep07_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep07 = 1 := by
  unfold routeStep07
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft,
    counterEvaluationScalar_symm,
    compositionCell_scalar, compScalar_L1_M0_H1, inv_one]

@[simp] theorem routeStep08_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep08 = 1 := by
  unfold routeStep08
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft]
  exact parallelArrowCell_scalar D _ _

@[simp] theorem routeStep09_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep09 = 1 := by
  unfold routeStep09
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft,
    compositionCell_scalar, compScalar_L1_M1_H1]

@[simp] theorem routeStep10_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep10 =
      counterEvaluationScalar D (forwardInverseCell b11) := by
  unfold routeStep10
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft]

@[simp] theorem routeStep11_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep11 = 1 := by
  unfold routeStep11
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerLeft,
    counterEvaluationScalar_symm,
    compositionCell_scalar, compScalar_L1_M1_H0, inv_one]

@[simp] theorem routeStep12_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep12 = 1 := by
  unfold routeStep12
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerLeft]
  exact parallelArrowCell_scalar D _ _

@[simp] theorem routeStep13_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep13 = 1 := by
  unfold routeStep13
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerLeft,
    compositionCell_scalar, compScalar_L1_M0_H0]

@[simp] theorem routeStep14_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep14 =
      counterEvaluationScalar D (inverseForwardCell a10) := by
  unfold routeStep14
  rw [counterEvaluationScalar_reendpoint,
    counterEvaluationScalar_whiskerRight,
    counterEvaluationScalar_whiskerLeft]

/-- The complete route around the seven untwisted faces evaluates to identity.
The two pointwise-adjoint inverse-pair scalars occur once positively and once
negatively, hence cancel in the abelian target group. -/
theorem counterSevenFaceRoute_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D counterSevenFaceRoute = 1 := by
  simp only [counterSevenFaceRoute, counterEvaluationScalar_trans,
    routeStep00_scalar, routeStep01_scalar, routeStep02_scalar,
    routeStep03_scalar, routeStep04_scalar, routeStep05_scalar,
    routeStep06_scalar, routeStep07_scalar, routeStep08_scalar,
    routeStep09_scalar, routeStep10_scalar, routeStep11_scalar,
    routeStep12_scalar, routeStep13_scalar, routeStep14_scalar,
    mul_one]
  rw [mul_comm
    (counterEvaluationScalar D (inverseForwardCell a10))
    (counterEvaluationScalar D (forwardInverseCell b11))]
  group

/-- The direct distinguished route and the seven-face route have different
canonical evaluations, already for arbitrary pointwise adjoint-equivalence
data. -/
theorem counterDirectRoute_ne_counterSevenFaceRoute_evaluation
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    generatedLocalization2CellEvaluationIso
        allMorphisms counterSystem D counterDirectRoute ≠
      generatedLocalization2CellEvaluationIso
        allMorphisms counterSystem D counterSevenFaceRoute := by
  intro h
  have hs := congrArg
    (fun e => e.hom.toNatTrans.app (SingleObj.star C2)) h
  change counterEvaluationScalar D counterDirectRoute =
    counterEvaluationScalar D counterSevenFaceRoute at hs
  rw [counterDirectRoute_scalar, counterSevenFaceRoute_scalar] at hs
  exact zeta_ne_one hs

/-- The explicit difference loop has nontrivial generated holonomy. -/
theorem counterGeneratedLoop_holonomy_ne_refl
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    generatedHolonomy allMorphisms counterSystem D counterGeneratedLoop ≠
      Iso.refl _ := by
  intro h
  have hdiff :
      generatedHolonomy allMorphisms counterSystem D
          (generatedLocalization2CellDifference
            allMorphisms counterDirectRoute counterSevenFaceRoute) =
        Iso.refl _ := by
    simpa [counterGeneratedLoop] using h
  have heq :=
    (generatedLocalization2CellEvaluationIso_eq_iff_differenceHolonomy_trivial
      allMorphisms counterSystem D counterDirectRoute counterSevenFaceRoute).2 hdiff
  exact counterDirectRoute_ne_counterSevenFaceRoute_evaluation D heq

/-- The canonical pointwise data extracted from weak admissibility do not have
trivial generated holonomy. -/
theorem counterSystem_not_generatedHolonomyTrivial :
    ¬ GeneratedHolonomyTrivial allMorphisms counterSystem counterD := by
  intro h
  exact counterGeneratedLoop_holonomy_ne_refl counterD
    (h (rawPath a00 ≫ rawPath b00) counterGeneratedLoop)

/-- Truth-test conclusion: weak pointwise admissibility alone does not force the
global generated-holonomy condition used in v2.68. -/
theorem weak_admissibility_does_not_force_generatedHolonomyTrivial :
    ¬ (∀
      (R : RawHigherContextualSystem.{0, 0, 0, 0}
        (Context := OctahedralVertex))
      (hR : IsHigherWAdmissible allMorphisms R),
      GeneratedHolonomyTrivial allMorphisms R
        (pointwiseWAdjointEquivalenceDataOfAdmissible allMorphisms hR)) := by
  intro h
  exact counterSystem_not_generatedHolonomyTrivial
    (h counterSystem counterSystem_admissible)

end KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
