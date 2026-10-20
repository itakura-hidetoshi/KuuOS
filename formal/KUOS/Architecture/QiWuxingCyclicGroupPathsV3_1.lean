import Kuu.Presentation
import KUOS.Architecture.QiWuxingPhaseObservationUniversalPropertyV3_0

/-!
# Five-phase cyclic action and free typed relation paths (v3.1)

The cyclic group `FivePhase = ZMod 5` acts faithfully and transitively by
phase translations. Generation is translation by one and control by two.

The *action* of one control step equals two generation steps, but their
source arrows are different: a single control arrow versus a two-arrow path
in the mathlib free path category. The observation
`pathShift : Quiver.Path p q → FivePhase × Nat` remembers the phase
displacement and arrow count and respects composition, but still forgets
the order of mixed relation words.

Independent Kuu presentations do not collapse these paths unless a
replacement relation is explicitly declared. This file introduces no
Gray dependency, physical gauge interpretation or clinical authority.
-/

namespace KUOS.Architecture.WuxingCyclicPaths

set_option autoImplicit false

/-- The regular translation action of the five-cycle as permutations. -/
def rotation (delta : FivePhase) : FivePhase ≃ FivePhase where
  toFun p := p + delta
  invFun p := p - delta
  left_inv := by
    intro p
    simp
  right_inv := by
    intro p
    simp

/-- The neutral displacement acts as the identity permutation. -/
@[simp] theorem rotation_zero :
    rotation 0 = Equiv.refl FivePhase := by
  ext p
  simp [rotation]

/-- Adding displacements composes the corresponding permutations. -/
theorem rotation_add (a b : FivePhase) :
    rotation (a + b) = (rotation a).trans (rotation b) := by
  ext p
  change p + (a + b) = (p + a) + b
  abel

/-- A rotation is uniquely determined by its displacement. -/
theorem rotation_injective : Function.Injective rotation := by
  intro a b h
  have hzero :=
    congrArg (fun f : FivePhase ≃ FivePhase => f (0 : FivePhase)) h
  simpa [rotation] using hzero

/-- Every phase is obtained from any other phase by some rotation. -/
theorem rotation_transitive (p q : FivePhase) :
    ∃ delta : FivePhase, rotation delta p = q := by
  refine ⟨q - p, ?_⟩
  change p + (q - p) = q
  abel

/-- The abstract generator rotates by one phase. -/
theorem rotation_generation (p : FivePhase) :
    rotation 1 p = generationPhase p := rfl

/-- The controlling generator rotates by two phases. -/
theorem rotation_control (p : FivePhase) :
    rotation 2 p = controlPhase p := rfl

/-- The controlling rotation equals two consecutive generative rotations. -/
theorem rotation_control_eq_generation_twice (p : FivePhase) :
    rotation 2 p = rotation 1 (rotation 1 p) := by
  change p + 2 = (p + 1) + 1
  ring

/-- Five generative displacements return the phase coordinate. -/
theorem five_generative_displacements_return (p : FivePhase) :
    rotation (5 : FivePhase) p = p := by
  simp [rotation]

/-- Generation and control represent different group elements. -/
theorem rotation_generation_ne_control : rotation 1 ≠ rotation 2 := by
  intro h
  have hneq : (1 : FivePhase) ≠ 2 := by decide
  exact hneq (rotation_injective h)

/-- Typed primitive interactions: a control arrow remains a single arrow even
though its target is also reached by two generative arrows. -/
inductive Arrow : FivePhase → FivePhase → Type
  | generation (p : FivePhase) : Arrow p (generationPhase p)
  | control (p : FivePhase) :
      Arrow p (generationPhase (generationPhase p))

instance : Quiver FivePhase where
  Hom := Arrow

/-- The unrestricted free category on the typed five-phase interaction quiver. -/
abbrev FreePhaseCategory := CategoryTheory.Paths FivePhase

/-- One primitive control event, represented by one typed arrow. -/
def directControlPath (p : FivePhase) :
    Quiver.Path p (generationPhase (generationPhase p)) :=
  (Quiver.Path.nil : Quiver.Path p p).cons (Arrow.control p)

/-- Two primitive generation events, represented by two typed arrows. -/
def twoGenerationPath (p : FivePhase) :
    Quiver.Path p (generationPhase (generationPhase p)) :=
  ((Quiver.Path.nil : Quiver.Path p p).cons (Arrow.generation p)).cons
    (Arrow.generation (generationPhase p))

@[simp] theorem directControlPath_length (p : FivePhase) :
    (directControlPath p).length = 1 := rfl

@[simp] theorem twoGenerationPath_length (p : FivePhase) :
    (twoGenerationPath p).length = 2 := rfl

/-- The two-step word "generation, then control" as a genuine typed path. -/
def generationControlPath (p : FivePhase) :
    Quiver.Path p (generationPhase (generationPhase (generationPhase p))) :=
  ((Quiver.Path.nil : Quiver.Path p p).cons (Arrow.generation p)).cons
    (Arrow.control (generationPhase p))

/-- The two-step word "control, then generation" has the same endpoints. -/
def controlGenerationPath (p : FivePhase) :
    Quiver.Path p (generationPhase (generationPhase (generationPhase p))) :=
  ((Quiver.Path.nil : Quiver.Path p p).cons (Arrow.control p)).cons
    (Arrow.generation (generationPhase (generationPhase p)))

@[simp] theorem generationControlPath_length (p : FivePhase) :
    (generationControlPath p).length = 2 := rfl

@[simp] theorem controlGenerationPath_length (p : FivePhase) :
    (controlGenerationPath p).length = 2 := rfl

/-- The first intermediate vertices after one generation and one control
are distinct because 1 and 2 are different in the cyclic group of order 5. -/
theorem generation_target_ne_control_target (p : FivePhase) :
    generationPhase p ≠ generationPhase (generationPhase p) := by
  intro h
  have hshift : p + (1 : FivePhase) = p + 2 := by
    calc
      p + 1 = generationPhase p := rfl
      _ = generationPhase (generationPhase p) := h
      _ = controlPhase p := generation_twice_phase_eq_control p
      _ = p + 2 := rfl
  have h12 : (1 : FivePhase) = 2 := add_left_cancel hshift
  exact (by decide : (1 : FivePhase) ≠ 2) h12

/-- The order of two interactions survives in the typed free path itself:
both paths have length two and the same endpoints, but different intermediate
vertices and therefore cannot be equal. -/
theorem mixed_typed_paths_distinct (p : FivePhase) :
    generationControlPath p ≠ controlGenerationPath p := by
  intro h
  unfold generationControlPath controlGenerationPath at h
  have hmid := Quiver.Path.obj_eq_of_cons_eq_cons h
  exact generation_target_ne_control_target p hmid

/-- Equal endpoints do not collapse different typed paths in the free category. -/
theorem directControlPath_ne_twoGenerationPath (p : FivePhase) :
    directControlPath p ≠ twoGenerationPath p := by
  intro h
  have hlen :=
    congrArg
      (fun path : Quiver.Path p (generationPhase (generationPhase p)) =>
        path.length) h
  change (1 : Nat) = 2 at hlen
  omega

/-- Observe a typed path only through its group displacement and event count. -/
def pathShift {p q : FivePhase} (path : Quiver.Path p q) : WuxingShift :=
  (q - p, path.length)

/-- The source phase acted on by the path displacement equals its target. -/
theorem pathShift_endpoint {p q : FivePhase} (path : Quiver.Path p q) :
    rotation (pathShift path).1 p = q := by
  change p + (q - p) = q
  abel

/-- Path composition respects the additive phase/history shift structure. -/
theorem pathShift_comp {p q r : FivePhase}
    (first : Quiver.Path p q) (second : Quiver.Path q r) :
    pathShift (first.comp second) = pathShift first + pathShift second := by
  apply Prod.ext
  · change r - p = (q - p) + (r - q)
    abel
  · change (first.comp second).length = first.length + second.length
    exact Quiver.Path.length_comp first second

/-- The direct control arrow and the two-generation path have the same
group displacement, but different protected event counts. -/
theorem direct_control_two_generations_observation (p : FivePhase) :
    (pathShift (directControlPath p)).1 =
        (pathShift (twoGenerationPath p)).1 ∧
      pathShift (directControlPath p) ≠
        pathShift (twoGenerationPath p) := by
  constructor
  · rfl
  · intro h
    have hcount := congrArg Prod.snd h
    change (1 : Nat) = 2 at hcount
    omega

/-- The phase-plus-event-count projection identifies the two mixed-order
paths even though the typed paths themselves are unequal. -/
theorem mixed_typed_paths_same_shift (p : FivePhase) :
    pathShift (generationControlPath p) =
      pathShift (controlGenerationPath p) := by
  rfl

/-- With only identity replacements, the independent Kuu quotient also
preserves the distinction between the two differently ordered typed paths. -/
theorem mixed_paths_survive_identity_presentation (p : FivePhase) :
    (Kuu.project FivePhase (Kuu.identityRelations FivePhase)).map
        (generationControlPath p) ≠
      (Kuu.project FivePhase (Kuu.identityRelations FivePhase)).map
        (controlGenerationPath p) := by
  intro h
  have heq :=
    (Kuu.identity_projection_reflects
      (generationControlPath p) (controlGenerationPath p)).mp h
  exact mixed_typed_paths_distinct p heq

/-- This free-path distinction also survives the independent Kuu
presentation when only identity replacements are declared. -/
theorem direct_control_survives_identity_presentation (p : FivePhase) :
    (Kuu.project FivePhase (Kuu.identityRelations FivePhase)).map
        (directControlPath p) ≠
      (Kuu.project FivePhase (Kuu.identityRelations FivePhase)).map
        (twoGenerationPath p) := by
  intro h
  have heq :=
    (Kuu.identity_projection_reflects
      (directControlPath p) (twoGenerationPath p)).mp h
  exact directControlPath_ne_twoGenerationPath p heq

/-- Order remains a genuine piece of information in the relation-word source. -/
theorem mixed_relation_words_distinct :
    ([.generation, .control] : WuxingRelationWord) ≠
      [.control, .generation] := by
  decide

/-- The protected shift's commutative addition forgets mixed-word order,
despite retaining total event count. -/
theorem mixed_relation_words_same_shift :
    relationWordShift [.generation, .control] =
      relationWordShift [.control, .generation] := by
  simp [relationWordShift, add_comm]

/-- Equal additive shifts also give equal state actions: source words must
still be retained when the event order matters. -/
theorem mixed_relation_words_same_state_action (state : WuxingFibonacciState) :
    applyRelationWord [.generation, .control] state =
      applyRelationWord [.control, .generation] state := by
  rw [applyRelationWord_eq_applyShift, applyRelationWord_eq_applyShift,
    mixed_relation_words_same_shift]

#print axioms rotation_add
#print axioms rotation_injective
#print axioms rotation_transitive
#print axioms rotation_control_eq_generation_twice
#print axioms directControlPath_ne_twoGenerationPath
#print axioms generation_target_ne_control_target
#print axioms mixed_typed_paths_distinct
#print axioms mixed_typed_paths_same_shift
#print axioms mixed_paths_survive_identity_presentation
#print axioms pathShift_endpoint
#print axioms pathShift_comp
#print axioms direct_control_two_generations_observation
#print axioms direct_control_survives_identity_presentation
#print axioms mixed_relation_words_distinct
#print axioms mixed_relation_words_same_shift
#print axioms mixed_relation_words_same_state_action

end KUOS.Architecture.WuxingCyclicPaths
