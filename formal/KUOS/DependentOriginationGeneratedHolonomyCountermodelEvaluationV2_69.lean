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

/-- Any inverse functor selected by pointwise admissibility acts identically on
`C2` morphisms.  This uses only counit naturality and commutativity of `C2`, not
the implementation of `Functor.asEquivalence`. -/
theorem chosenInverse_map_eq
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (w : X ⟶ Y) (hw : allMorphisms w) (x : C2) :
    (D.inverse w hw).toFunctor.map x = x := by
  change (D.chosen w hw).inverse.map x = x
  have hnat := (D.chosen w hw).counitIso.hom.naturality x
  rw [D.chosen_functor w hw, counterSystem_map_toFunctor] at hnat
  simp only [Functor.comp_map, Functor.id_map, SingleObj.comp_as_mul] at hnat
  rw [mul_comm x ((D.chosen w hw).counitIso.hom.app (SingleObj.star C2))] at hnat
  exact mul_left_cancel hnat

/-- Every free localization word acts identically on `C2` morphisms. -/
theorem counterFreePathEvaluator_map_eq
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} (p : X ⟶ Y) (x : C2) :
    ((freePathEvaluator allMorphisms counterSystem D).map p).toFunctor.map x = x := by
  induction p using Paths.induction with
  | id =>
      simp
  | comp p e hp =>
      rw [Functor.map_comp, Cat.Hom.comp_toFunctor, Functor.comp_map, hp]
      have hgen :
          (freePathEvaluator allMorphisms counterSystem D).map
              ((Paths.of (Localization.Construction.LocQuiver allMorphisms)).map e) =
            (localizedGeneratorPrefunctor allMorphisms counterSystem D).map e := by
        simpa [freePathEvaluator] using
          (Paths.lift_toPath
            (localizedGeneratorPrefunctor allMorphisms counterSystem D) e)
      rw [hgen]
      rcases e with f | w
      · change (counterSystem.map f.toLoc).toFunctor.map x = x
        rw [counterSystem_map_toFunctor]
        rfl
      · exact chosenInverse_map_eq D w.1 w.2 x

@[simp]
theorem counterEvaluationScalar_refl
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} (p : X ⟶ Y) :
    counterEvaluationScalar D (GeneratedLocalization2Cell.refl p) = 1 := by
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

@[simp]
theorem counterEvaluationScalar_symm
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : LocalizationPaths allMorphisms} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell allMorphisms p q) :
    counterEvaluationScalar D (GeneratedLocalization2Cell.symm α) =
      (counterEvaluationScalar D α)⁻¹ := by
  change
    (generatedLocalization2CellEvaluationIso
      allMorphisms counterSystem D α).inv.toNatTrans.app (SingleObj.star C2) =
      ((generatedLocalization2CellEvaluationIso
        allMorphisms counterSystem D α).hom.toNatTrans.app
          (SingleObj.star C2))⁻¹
  exact eq_inv_of_mul_eq_one_right (by
    simpa only [SingleObj.comp_as_mul, SingleObj.id_as_one] using
      (Cat.Hom.inv_hom_id_toNatTrans_app
        (generatedLocalization2CellEvaluationIso
          allMorphisms counterSystem D α)
        (SingleObj.star C2)))

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
  simp only [Cat.whiskerLeft_app]
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
  simp only [Cat.whiskerRight_app]
  exact counterFreePathEvaluator_map_eq D k _

/-- A retained composition generator evaluates to the scalar decorating exactly
that triangular face. -/
@[simp]
theorem compositionCell_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    counterEvaluationScalar D (compositionCell f g) = compScalar X Y Z := by
  rfl

/-- A change of parallel-arrow presentation carries no scalar. -/
@[simp]
theorem parallelArrowCell_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem)
    {X Y : OctahedralVertex} (f g : X ⟶ Y) :
    counterEvaluationScalar D (parallelArrowCell f g) = 1 := by
  subst g
  simp [parallelArrowCell, counterEvaluationScalar]

/-- The distinguished face carries the unique nontrivial scalar. -/
@[simp]
theorem counterDirectRoute_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D counterDirectRoute = zeta := by
  rfl

@[simp] theorem routeStep00_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep00 = 1 := by
  simp [routeStep00]

@[simp] theorem routeStep01_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep01 = 1 := by
  simp [routeStep01]

@[simp] theorem routeStep02_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep02 =
      (counterEvaluationScalar D (forwardInverseCell b11))⁻¹ := by
  simp [routeStep02]

@[simp] theorem routeStep03_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep03 = 1 := by
  simp [routeStep03]

@[simp] theorem routeStep04_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep04 = 1 := by
  simp [routeStep04]

@[simp] theorem routeStep05_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep05 = 1 := by
  simp [routeStep05]

@[simp] theorem routeStep06_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep06 =
      (counterEvaluationScalar D (inverseForwardCell a10))⁻¹ := by
  simp [routeStep06]

@[simp] theorem routeStep07_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep07 = 1 := by
  simp [routeStep07]

@[simp] theorem routeStep08_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep08 = 1 := by
  simp [routeStep08]

@[simp] theorem routeStep09_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep09 = 1 := by
  simp [routeStep09]

@[simp] theorem routeStep10_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep10 =
      counterEvaluationScalar D (forwardInverseCell b11) := by
  simp [routeStep10]

@[simp] theorem routeStep11_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep11 = 1 := by
  simp [routeStep11]

@[simp] theorem routeStep12_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep12 = 1 := by
  simp [routeStep12]

@[simp] theorem routeStep13_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep13 = 1 := by
  simp [routeStep13]

@[simp] theorem routeStep14_scalar
    (D : PointwiseWAdjointEquivalenceData (W := allMorphisms) counterSystem) :
    counterEvaluationScalar D routeStep14 =
      counterEvaluationScalar D (inverseForwardCell a10) := by
  simp [routeStep14]

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
    one_mul, mul_one]
  abel

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
  have hz : zeta = 1 := by
    simpa [counterEvaluationScalar] using hs
  exact zeta_ne_one hz

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
      (R : RawHigherContextualSystem
        (Context := OctahedralVertex) (uH := 0) (vH := 0))
      (hR : IsHigherWAdmissible allMorphisms R),
      GeneratedHolonomyTrivial allMorphisms R
        (pointwiseWAdjointEquivalenceDataOfAdmissible allMorphisms hR)) := by
  intro h
  exact counterSystem_not_generatedHolonomyTrivial
    (h counterSystem counterSystem_admissible)

end KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
