import KUOS.Architecture.QiWuxingPathObservationCongruenceV3_2
import Mathlib.CategoryTheory.Equivalence

/-!
# Reachable path-observation category (Qi v3.3)

Objects are five phases. A morphism is a reachable primitive-event count:
a natural number n is admitted from p to q only if a typed free path p ⟶ q
has length n. Composition adds counts, with witnesses proving closure.

The path observer is full but non-faithful. Its hom-relation is exactly the
v3.2 declared observation congruence. The induced quotient observer is fully
faithful and essentially surjective, giving a categorical equivalence.

Observation equality does not assert source-path or history equality.
-/

namespace KUOS.Architecture.WuxingCyclicPaths

open CategoryTheory

set_option autoImplicit false

/-- Observable objects retain the phase, not the source path history. -/
structure ObservedPhase where
  phase : FivePhase

/-- An observable arrow records a reachable number of primitive events. -/
def ObservedHom (p q : ObservedPhase) : Type :=
  { n : Nat // ∃ f : Quiver.Path p.phase q.phase, f.length = n }

/-- Observed arrows compose by adding event counts. -/
instance observedPhaseCategory : Category ObservedPhase where
  Hom := ObservedHom
  id p := ⟨0, ⟨Quiver.Path.nil, rfl⟩⟩
  comp f g := ⟨f.val + g.val, by
    obtain ⟨pf, hpf⟩ := f.property
    obtain ⟨pg, hpg⟩ := g.property
    refine ⟨pf.comp pg, ?_⟩
    rw [Quiver.Path.length_comp, hpf, hpg]⟩
  id_comp f := by
    apply Subtype.ext
    exact Nat.zero_add _
  comp_id f := by
    apply Subtype.ext
    exact Nat.add_zero _
  assoc f g h := by
    apply Subtype.ext
    exact Nat.add_assoc f.val g.val h.val

/-- A concrete observer from the typed free-path category. -/
def pathObservationFunctor : FreePhaseCategory ⥤ ObservedPhase where
  obj p := ⟨p⟩
  map f := ⟨f.length, ⟨f, rfl⟩⟩
  map_id p := by
    apply Subtype.ext
    rfl
  map_comp f g := by
    apply Subtype.ext
    exact Quiver.Path.length_comp f g

@[simp] theorem pathObservationFunctor_map_length {p q : FivePhase}
    (f : Quiver.Path p q) :
    (pathObservationFunctor.map f).val = f.length := rfl

/-- The kernel of the observer is exactly the declared v3.2 relation. -/
theorem pathObservationFunctor_map_eq_iff {p q : FivePhase}
    (f g : Quiver.Path p q) :
    pathObservationFunctor.map f = pathObservationFunctor.map g ↔
      pathShift f = pathShift g := by
  constructor
  · intro h
    apply (shiftObservationRelations_iff_length f g).2
    have hlen := congrArg Subtype.val h
    exact hlen
  · intro h
    apply Subtype.ext
    exact (shiftObservationRelations_iff_length f g).1 h

theorem pathObservationFunctor_kernel {p q : FivePhase}
    (f g : Quiver.Path p q) :
    pathObservationFunctor.homRel f g ↔
      shiftObservationRelations f g :=
  pathObservationFunctor_map_eq_iff f g

/-- Every admissible observable count has a typed path representative. -/
theorem pathObservationFunctor_surjective {p q : FivePhase}
    (h : pathObservationFunctor.obj p ⟶ pathObservationFunctor.obj q) :
    ∃ f : Quiver.Path p q, pathObservationFunctor.map f = h := by
  obtain ⟨f, hf⟩ := h.property
  refine ⟨f, ?_⟩
  apply Subtype.ext
  exact hf

instance pathObservationFunctor_full : pathObservationFunctor.Full where
  map_surjective := by
    intro p q h
    exact pathObservationFunctor_surjective h

/-- Mixed source paths have the same observed image but differ in history. -/
theorem pathObservationFunctor_not_injective (p : FivePhase) :
    ¬ Function.Injective
      (fun f : Quiver.Path p
          (generationPhase (generationPhase (generationPhase p))) =>
        pathObservationFunctor.map f) := by
  intro h
  apply mixed_typed_paths_distinct p
  apply h
  exact (pathObservationFunctor_map_eq_iff _ _).2
    (mixed_typed_paths_same_shift p)

/-- The observer respects precisely the explicitly declared Kuu relation. -/
private theorem pathObservationFunctor_respects :
    Kuu.Respects shiftObservationRelations pathObservationFunctor := by
  intro p q f g h
  exact (pathObservationFunctor_map_eq_iff f g).2 h

/-- Unique functor descending to the Kuu observational quotient. -/
def observationDescent :
    Kuu.Space FivePhase shiftObservationRelations ⥤ ObservedPhase :=
  Kuu.descend shiftObservationRelations pathObservationFunctor
    pathObservationFunctor_respects

theorem observationDescent_spec :
    Kuu.project FivePhase shiftObservationRelations ⋙ observationDescent =
      pathObservationFunctor := by
  unfold observationDescent
  exact Kuu.descend_spec shiftObservationRelations
    pathObservationFunctor pathObservationFunctor_respects

@[simp] theorem observationDescent_map_project {p q : FivePhase}
    (f : Quiver.Path p q) :
    observationDescent.map
        ((Kuu.project FivePhase shiftObservationRelations).map f) =
      pathObservationFunctor.map f := rfl

/-- Descent is injective on hom-sets: no further equations are introduced. -/
theorem observationDescent_hom_injective (p q : FivePhase) :
    Function.Injective
      (observationDescent.map :
        ((Kuu.project FivePhase shiftObservationRelations).obj p ⟶
          (Kuu.project FivePhase shiftObservationRelations).obj q) →
        (pathObservationFunctor.obj p ⟶ pathObservationFunctor.obj q)) := by
  intro f g
  revert g
  refine Quot.inductionOn f ?_
  intro f' g
  refine Quot.inductionOn g ?_
  intro g' hfg
  change pathObservationFunctor.map f' =
    pathObservationFunctor.map g' at hfg
  exact (shiftObservation_projection_exact f' g').2
    ((pathObservationFunctor_map_eq_iff f' g').1 hfg)

/-- Descent is surjective on every hom-set, by reachability. -/
theorem observationDescent_hom_surjective (p q : FivePhase)
    (h : pathObservationFunctor.obj p ⟶ pathObservationFunctor.obj q) :
    ∃ f : (Kuu.project FivePhase shiftObservationRelations).obj p ⟶
          (Kuu.project FivePhase shiftObservationRelations).obj q,
      observationDescent.map f = h := by
  obtain ⟨f, hf⟩ := pathObservationFunctor_surjective h
  refine ⟨(Kuu.project FivePhase shiftObservationRelations).map f, ?_⟩
  exact (observationDescent_map_project f).trans hf

instance observationDescent_faithful : observationDescent.Faithful where
  map_injective := by
    intro X Y f g h
    rcases X with ⟨p⟩
    rcases Y with ⟨q⟩
    exact observationDescent_hom_injective p q h

instance observationDescent_full : observationDescent.Full where
  map_surjective := by
    intro X Y h
    rcases X with ⟨p⟩
    rcases Y with ⟨q⟩
    exact observationDescent_hom_surjective p q h

instance observationDescent_essSurj : observationDescent.EssSurj where
  mem_essImage := by
    rintro ⟨p⟩
    exact ⟨⟨p⟩, ⟨Iso.refl _⟩⟩

/-- First-isomorphism form of the reachable path observation. -/
instance observationDescent_isEquivalence : observationDescent.IsEquivalence where
  faithful := inferInstance
  full := inferInstance
  essSurj := inferInstance

noncomputable def observationQuotientEquivalence :
    Kuu.Space FivePhase shiftObservationRelations ≌ ObservedPhase :=
  observationDescent.asEquivalence

#print axioms pathObservationFunctor_map_eq_iff
#print axioms pathObservationFunctor_kernel
#print axioms pathObservationFunctor_surjective
#print axioms pathObservationFunctor_not_injective
#print axioms observationDescent_spec
#print axioms observationDescent_map_project
#print axioms observationDescent_hom_injective
#print axioms observationDescent_hom_surjective
#print axioms observationQuotientEquivalence

end KUOS.Architecture.WuxingCyclicPaths
