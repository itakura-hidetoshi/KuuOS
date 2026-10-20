import KUOS.Architecture.QiWuxingCyclicGroupPathsV3_1

/-!
# Typed Wuxing path observation congruence (v3.2)

The v3.1 map records (phase displacement, primitive event count). Here we
turn equality of those measurements into an explicitly DECLARED congruence
on the free typed path category. Composition preserves it, so Kuu's
category quotient is exactly the observer-induced identification.

This quotient identifies different mixed-order paths, but does not identify
a single control arrow with two generation arrows, since their counts differ.
In contrast, Kuu's identity presentation preserves both distinctions.

This is a finite categorical observation model, not an ontological path
equality, a physical gauge quotient, or clinical/execution authority.
-/

namespace KUOS.Architecture.WuxingCyclicPaths

open CategoryTheory

set_option autoImplicit false

universe u v

/-- Explicitly declared replacement: two parallel paths may be identified
precisely when the phase-and-event-count observation agrees. -/
def shiftObservationRelations : Kuu.Relations FivePhase :=
  fun {_ _} f g => pathShift f = pathShift g

/-- For parallel paths the phase displacement is already fixed by endpoints.
Therefore shift observation equality means exactly equal primitive event count. -/
theorem shiftObservationRelations_iff_length {p q : FivePhase}
    (f g : Quiver.Path p q) :
    shiftObservationRelations f g ↔ f.length = g.length := by
  change (q - p, f.length) = (q - p, g.length) ↔ f.length = g.length
  simp

/-- The observation relation is stable under simultaneous path composition. -/
theorem shiftObservationRelations_comp {p q r : FivePhase}
    {f f' : Quiver.Path p q} {g g' : Quiver.Path q r}
    (hf : shiftObservationRelations f f')
    (hg : shiftObservationRelations g g') :
    shiftObservationRelations (f.comp g) (f'.comp g') := by
  change pathShift f = pathShift f' at hf
  change pathShift g = pathShift g' at hg
  change pathShift (f.comp g) = pathShift (f'.comp g')
  rw [pathShift_comp, pathShift_comp, hf, hg]

/-- A genuine categorical congruence, not an automatic equality of paths.
The v3.1 composition law supplies pre- and postcomposition stability. -/
instance shiftObservationRelations_congruence :
    Congruence shiftObservationRelations where
  equivalence := by
    intro p q
    constructor
    · intro f
      rfl
    · intro f g h
      exact h.symm
    · intro f g k hfg hgk
      exact hfg.trans hgk
  comp_left := by
    intro p q r left f g h
    change pathShift f = pathShift g at h
    change pathShift (left.comp f) = pathShift (left.comp g)
    rw [pathShift_comp, pathShift_comp, h]
  comp_right := by
    intro p q r f g right h
    change pathShift f = pathShift g at h
    change pathShift (f.comp right) = pathShift (g.comp right)
    rw [pathShift_comp, pathShift_comp, h]

/-- The quotient projection identifies exactly observationally equal
parallel paths: no further path replacements are silently introduced. -/
theorem shiftObservation_projection_exact {p q : FivePhase}
    (f g : Quiver.Path p q) :
    (Kuu.project FivePhase shiftObservationRelations).map f =
        (Kuu.project FivePhase shiftObservationRelations).map g ↔
      pathShift f = pathShift g := by
  exact Quotient.functor_map_eq_iff shiftObservationRelations f g

/-- Equivalently, the categorical quotient equates precisely the parallel
typed paths with the same primitive event count. -/
theorem shiftObservation_projection_iff_length {p q : FivePhase}
    (f g : Quiver.Path p q) :
    (Kuu.project FivePhase shiftObservationRelations).map f =
        (Kuu.project FivePhase shiftObservationRelations).map g ↔
      f.length = g.length := by
  exact (shiftObservation_projection_exact f g).trans
    (shiftObservationRelations_iff_length f g)

/-- Even Kuu's composition/equivalence closure does not add extra
identifications beyond the declared observational kernel. -/
theorem shiftObservation_replaceable_exact {p q : FivePhase}
    (f g : Quiver.Path p q) :
    Kuu.Replaceable shiftObservationRelations f g ↔
      pathShift f = pathShift g := by
  exact (Kuu.project_exact shiftObservationRelations f g).symm.trans
    (shiftObservation_projection_exact f g)

/-- The mixed-order, equal-length paths are identified by the
DECLARED shift-observation quotient. -/
theorem mixed_paths_identified_by_shift_observation (p : FivePhase) :
    (Kuu.project FivePhase shiftObservationRelations).map
        (generationControlPath p) =
      (Kuu.project FivePhase shiftObservationRelations).map
        (controlGenerationPath p) := by
  apply (shiftObservation_projection_exact _ _).2
  exact mixed_typed_paths_same_shift p

/-- The observer quotient is not faithful on parallel typed paths:
equal shift images need not imply equality of the original paths. -/
theorem shift_observation_projection_not_injective (p : FivePhase) :
    ¬ Function.Injective
      (fun f : Quiver.Path p
          (generationPhase (generationPhase (generationPhase p))) =>
        (Kuu.project FivePhase shiftObservationRelations).map f) := by
  intro h
  exact mixed_typed_paths_distinct p
    (h (mixed_paths_identified_by_shift_observation p))

/-- A direct control event and two generation events have the same phase
effect, but different counts, so the shift-observation quotient separates them. -/
theorem direct_control_survives_shift_observation (p : FivePhase) :
    (Kuu.project FivePhase shiftObservationRelations).map
        (directControlPath p) ≠
      (Kuu.project FivePhase shiftObservationRelations).map
        (twoGenerationPath p) := by
  intro h
  have hlen :=
    (shiftObservation_projection_iff_length
      (directControlPath p) (twoGenerationPath p)).mp h
  change (1 : Nat) = 2 at hlen
  omega

/-- The identity Kuu presentation retains both paths while only the
additional declared observation relation collapses their order. -/
theorem mixed_paths_identity_vs_observation (p : FivePhase) :
    ((Kuu.project FivePhase shiftObservationRelations).map
        (generationControlPath p) =
      (Kuu.project FivePhase shiftObservationRelations).map
        (controlGenerationPath p)) ∧
      ((Kuu.project FivePhase (Kuu.identityRelations FivePhase)).map
        (generationControlPath p) ≠
      (Kuu.project FivePhase (Kuu.identityRelations FivePhase)).map
        (controlGenerationPath p)) :=
  ⟨mixed_paths_identified_by_shift_observation p,
    mixed_paths_survive_identity_presentation p⟩

/-- A categorical observer factors uniquely through the quotient when
(and only for this theorem: assuming) it respects declared shift relations.
This uses the independent Kuu quotient's universal property. -/
theorem shift_observer_existsUnique
    {D : Type u} [Category.{v} D]
    (F : FreePhaseCategory ⥤ D)
    (h : ∀ (p q : FivePhase) (f g : Quiver.Path p q),
      pathShift f = pathShift g → F.map f = F.map g) :
    ∃! G : Kuu.Space FivePhase shiftObservationRelations ⥤ D,
      Kuu.project FivePhase shiftObservationRelations ⋙ G = F := by
  apply Kuu.observer_existsUnique shiftObservationRelations F
  intro p q f g hfg
  exact h p q f g hfg

#print axioms shiftObservationRelations_iff_length
#print axioms shiftObservationRelations_comp
#print axioms shiftObservation_projection_exact
#print axioms shiftObservation_projection_iff_length
#print axioms shiftObservation_replaceable_exact
#print axioms mixed_paths_identified_by_shift_observation
#print axioms shift_observation_projection_not_injective
#print axioms direct_control_survives_shift_observation
#print axioms mixed_paths_identity_vs_observation
#print axioms shift_observer_existsUnique

end KUOS.Architecture.WuxingCyclicPaths
